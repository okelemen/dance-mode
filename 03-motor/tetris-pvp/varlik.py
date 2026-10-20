"""TETRIS MODE PVP (REF-053) - sahne varliklari, Blender (headless) GitHub Actions'ta.

    blender -b --factory-startup -noaudio -P 03-motor/tetris-pvp/varlik.py -- --cikti cikti [--ornek 64] [--yalniz poz]

Referans (REF-053) ekranin iki yarisinda her oyuncunun KENDI seridini gosterir: parlak jole kafes kapi,
jole yol (chevron basamak, korkuluk babalari), arkada dolu gece goku; duvar = parlak jole panel, poz
panelde OYUK. Kullanici (17 Eki 2026): "konsept ayni olsun, renkleri degistir ... benzemesin".
Bizim renk: P1 ZUMRUT/LIME, P2 KEHRIBAR/TURUNCU; gok lacivert-camgobegi, altin fenerler + yesil kureler.

Ciktilar (sahne4.html bunlari 2B'de birlestirir; arka plan sabit, yalniz duvar buyur - referansta da kamera sabit):
  gok.png            1920x1080  gok (tam ekran)
  serit-p1.png       960x1080   P1 seridi (yol + kapi), gokte saydam
  serit-p2.png       960x1080   P2 seridi
  panel-p1.png       1100x904   P1 jole duvar paneli (saydam koseler)
  panel-p2.png
  poz/<ad>.png       900x740    duz siyah siluet maskesi (Mixamo govdesi, pozlar.json acilariyla bukulur)
  yerlesim.json      kapi acikliginin serit goruntusundeki piksel kutusu
"""
import bpy, os, sys, json, math, random
from mathutils import Vector, Matrix
from bpy_extras.object_utils import world_to_camera_view

argv = sys.argv[sys.argv.index("--") + 1:]
arg = lambda ad, v=None: argv[argv.index(ad) + 1] if ad in argv else v
KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CIKTI = os.path.abspath(arg("--cikti", "cikti"))
ORNEK = int(arg("--ornek", "64"))
YALNIZ = arg("--yalniz", "hepsi")          # hepsi | poz | sahne
os.makedirs(os.path.join(CIKTI, "poz"), exist_ok=True)
POZLAR = json.load(open(os.path.join(KOK, arg("--pozlar", "03-motor/tetris-pvp/pozlar.json")), encoding="utf-8"))["pozlar"]

RENK = {"p1": arg("--renk1", "#22e07a"), "p2": arg("--renk2", "#ff9a1f")}
# 3. video (REF-054): gokte dev galaksi sarmali + mor/sari kureler (--gok galaksi), kapilar blok kuleli (--kapi blok)
GOK = arg("--gok", "fener")
KAPI_TIP = arg("--kapi", "kafes")
# 4. video (REF-055): gokte dev halkali gezegen (--gok gezegen), duvar paneli parlak merkezli girdap (--panel girdap)
PANEL_TIP = arg("--panel", "jole")
YERLESIM = {}


def log(*a):
    print("[varlik]", *a, flush=True)


def hex3(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def lin(c):
    return tuple(((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c)


def acik(c, m):
    return tuple(x + (1 - x) * m for x in c)


def koyu(c, m):
    return tuple(x * (1 - m) for x in c)


# ------------------------------------------------------------------ temel
def bos_sahne(motor="CYCLES", w=1920, h=1080, saydam=False, ornek=None, doygun=True):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = motor
    if motor == "CYCLES":
        sc.cycles.device = "CPU"; sc.cycles.samples = ornek or ORNEK; sc.cycles.use_denoising = True
        # deneme 1: AgX doygun jole rengini pastele ceviriyordu (referans neon-doygun) -> Standard
        sc.view_settings.view_transform = "Standard" if doygun else "AgX"
    sc.render.resolution_x, sc.render.resolution_y = w, h
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = saydam
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA" if saydam else "RGB"
    wd = bpy.data.worlds.new("dunya"); sc.world = wd; wd.use_nodes = True
    bg = wd.node_tree.nodes["Background"]; bg.inputs[0].default_value = (*lin((0.02, 0.05, 0.10)), 1); bg.inputs[1].default_value = 0.6
    return sc


def mat_emis(ad, renk, guc):
    m = bpy.data.materials.new(ad); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    e = nt.nodes.new("ShaderNodeEmission"); e.inputs[0].default_value = (*renk, 1); e.inputs[1].default_value = guc
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(e.outputs[0], o.inputs[0])
    return m


def mat_jole(ad, renk, emis=0.04, purluk=0.12):
    """parlak jole/plastik: doygun renk, ust kaplama (coat), hafif ic isilti"""
    m = bpy.data.materials.new(ad); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*renk, 1)
    b.inputs["Roughness"].default_value = purluk
    b.inputs["Coat Weight"].default_value = 1.0
    b.inputs["Coat Roughness"].default_value = 0.03
    b.inputs["Subsurface Weight"].default_value = 0.0
    b.inputs["Subsurface Radius"].default_value = (0.4, 0.4, 0.4)
    b.inputs["Emission Color"].default_value = (*acik(renk, 0.3), 1)
    b.inputs["Emission Strength"].default_value = emis
    return m


def mat_cam(ad):
    m = bpy.data.materials.new(ad); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (1, 1, 1, 1)
    b.inputs["Roughness"].default_value = 0.0
    b.inputs["Transmission Weight"].default_value = 1.0
    b.inputs["IOR"].default_value = 1.33
    return m


def yuvarlak_kutu(ad, konum, boyut, mat, egim=0.08, seg=4):
    bpy.ops.mesh.primitive_cube_add(size=1, location=konum)
    o = bpy.context.active_object; o.name = ad; o.scale = boyut
    bpy.ops.object.transform_apply(scale=True)
    bv = o.modifiers.new("egim", "BEVEL"); bv.width = egim; bv.segments = seg; bv.limit_method = "NONE"
    o.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    return o


def boru(a, b, r, mat):
    a, b = Vector(a), Vector(b); d = b - a
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d.length, location=(a + b) / 2, vertices=20)
    c = bpy.context.active_object; c.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
    c.data.materials.append(mat); bpy.ops.object.shade_smooth()
    return c


def kure(konum, r, mat, sub=3):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=konum, segments=24, ring_count=12)
    o = bpy.context.active_object; o.data.materials.append(mat); bpy.ops.object.shade_smooth()
    return o


def isik(tip, konum, enerji, renk=(1, 1, 1), boy=2.0, yon=None):
    bpy.ops.object.light_add(type=tip, location=konum)
    L = bpy.context.active_object; L.data.energy = enerji; L.data.color = renk
    if tip == "AREA":
        L.data.size = boy
    if yon is not None:
        L.rotation_euler = (Vector(yon) - Vector(konum)).to_track_quat("-Z", "Y").to_euler()
    return L


def yaz(sc, ad):
    sc.render.filepath = os.path.join(CIKTI, ad)
    bpy.ops.render.render(write_still=True)
    log("yazildi", ad)


# ------------------------------------------------------------------ GOK (tam ekran)
def gok():
    sc = bos_sahne(w=1920, h=1080, ornek=min(ORNEK, 48))
    rnd = random.Random(53)
    # arka plan duzlemi: dikey gecis lacivert -> camgobegi + gurultulu bulutsu (nebula)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 60, 8), rotation=(math.pi / 2, 0, 0))
    p = bpy.context.active_object; p.scale = (150, 90, 1)
    m = bpy.data.materials.new("gok"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    rmp = nt.nodes.new("ShaderNodeValToRGB")
    cr = rmp.color_ramp
    G3 = GOK == "galaksi"
    G4 = GOK == "gezegen"
    G5 = GOK == "aurora"      # 6. video (REF-057): kuzey isigi + buzlu daglar + deniz
    # renk sirasi: (alt, ust, orta, bulutsu 1, bulutsu 2)
    # deneme 1 (gezegen): ust yarisi neredeyse siyahti, REF-055'te gok bastan basa bulutsu -> daha acik taban + guclu bulutsu
    GR = (("#4a86e8", "#120a46", "#2e2f9a", "#ff5ad8", "#3fe0ff") if G5 else
          ("#127a7e", "#0a1a3a", "#0d4a5e", "#2fd6c0", "#ff4f78") if G4 else
          ("#2a0f5e", "#05041c", "#120a3a", "#7a2bd6", "#d9c22b") if G3 else
          ("#0b5466", "#040824", "#0a2a4a", "#1fb5a0", "#d99a2b"))
    cr.elements[0].position = 0.0; cr.elements[0].color = (*lin(hex3(GR[0])), 1)
    cr.elements[1].position = 1.0; cr.elements[1].color = (*lin(hex3(GR[1])), 1)
    e2 = cr.elements.new(0.45); e2.color = (*lin(hex3(GR[2])), 1)
    nt.links.new(sep.outputs["Y"], rmp.inputs[0])
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 3.2; nz.inputs["Detail"].default_value = 6
    nz.inputs["Distortion"].default_value = 0.6
    nt.links.new(tc.outputs["Generated"], nz.inputs["Vector"])
    nr = nt.nodes.new("ShaderNodeValToRGB"); c2 = nr.color_ramp
    c2.elements[0].position = 0.40 if G4 else 0.52; c2.elements[0].color = (0, 0, 0, 1)
    c2.elements[1].position = 0.80; c2.elements[1].color = (*lin(hex3(GR[3])), 1)
    nt.links.new(nz.outputs["Fac"], nr.inputs[0])
    nz2 = nt.nodes.new("ShaderNodeTexNoise"); nz2.inputs["Scale"].default_value = 5.5; nz2.inputs["Detail"].default_value = 4
    nt.links.new(tc.outputs["Generated"], nz2.inputs["Vector"])
    nr2 = nt.nodes.new("ShaderNodeValToRGB"); c3 = nr2.color_ramp
    c3.elements[0].position = 0.50 if G4 else 0.60; c3.elements[0].color = (0, 0, 0, 1)
    c3.elements[1].position = 0.85; c3.elements[1].color = (*lin(hex3(GR[4])), 1)
    nt.links.new(nz2.outputs["Fac"], nr2.inputs[0])
    ad1 = nt.nodes.new("ShaderNodeMix"); ad1.data_type = "RGBA"; ad1.blend_type = "ADD"; ad1.inputs[0].default_value = 0.85 if G4 else 0.55
    nt.links.new(rmp.outputs[0], ad1.inputs[6]); nt.links.new(nr.outputs[0], ad1.inputs[7])
    ad2 = nt.nodes.new("ShaderNodeMix"); ad2.data_type = "RGBA"; ad2.blend_type = "ADD"; ad2.inputs[0].default_value = 0.6 if G4 else 0.35
    nt.links.new(ad1.outputs[2], ad2.inputs[6]); nt.links.new(nr2.outputs[0], ad2.inputs[7])
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs[1].default_value = 1.0
    nt.links.new(ad2.outputs[2], em.inputs[0])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], o.inputs[0])
    p.data.materials.append(m)
    # yildizlar
    ym = mat_emis("yildiz", (1, 1, 1), 8)
    for i in range(420):
        kure((rnd.uniform(-75, 75), rnd.uniform(50, 58), rnd.uniform(-20, 48)), rnd.uniform(0.05, 0.16), ym, sub=1)
    if G3:
        galaksi(rnd)
    if G4:
        gezegen(rnd)
    if G5:
        aurora(rnd)
    # yuzen fenerler (altin, ici isikli) - gogu dolduran ana oge (referanstaki denizanalarinin yerine bizim oge)
    gov = mat_emis("fener", lin(hex3("#ff8a1a")), 14.0)
    ust = mat_jole("fener_ust", lin(hex3("#7a3d10")), emis=0.0, purluk=0.3)
    for i in range(0 if (G3 or G4 or G5) else 46):
        x, y, z = rnd.uniform(-32, 32), rnd.uniform(18, 46), rnd.uniform(-6, 26)
        s = rnd.uniform(0.6, 1.4) * (y / 30)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.45 * s, depth=0.9 * s, location=(x, y, z), vertices=24)
        f = bpy.context.active_object; f.data.materials.append(gov)
        bv = f.modifiers.new("egim", "BEVEL"); bv.width = 0.18 * s; bv.segments = 5
        bpy.ops.object.shade_smooth()
        yuvarlak_kutu("kapak", (x, y, z + 0.5 * s), (0.62 * s, 0.62 * s, 0.12 * s), ust, egim=0.04 * s)
        isik("POINT", (x, y - 1.2 * s, z), 60 * s * s, lin(hex3("#ffb43a")))
    # yesil/camgobegi isik kureleri (bubble) + kucuk parilti
    for i in range(60):
        c = lin(hex3(rnd.choice(["#ff5ad8", "#6fd8ff", "#ffffff", "#b98cff"] if G5 else
                                ["#ff2d55", "#5a78ff", "#ffd27a", "#ffffff"] if G4 else
                                ["#b45cff", "#f5ff3d", "#ffffff"] if G3 else ["#3dffa8", "#2be0e0", "#b6ff5c"])))
        kure((rnd.uniform(-34, 34), rnd.uniform(16, 44), rnd.uniform(-8, 28)), rnd.uniform(0.15, 0.55), mat_emis("kure%d" % i, c, rnd.uniform(6, 12)))
    bpy.ops.object.camera_add(location=(0, -6, 9), rotation=(math.radians(90), 0, 0))
    kam = bpy.context.active_object; kam.data.lens = 26; sc.camera = kam
    sc.use_nodes = True
    nt2 = sc.node_tree; nt2.nodes.clear()
    rl = nt2.nodes.new("CompositorNodeRLayers")
    gl = nt2.nodes.new("CompositorNodeGlare"); gl.glare_type = "FOG_GLOW"; gl.threshold = 0.8; gl.size = 9; gl.mix = 0.25
    ou = nt2.nodes.new("CompositorNodeComposite")
    nt2.links.new(rl.outputs[0], gl.inputs[0]); nt2.links.new(gl.outputs[0], ou.inputs[0])
    yaz(sc, "gok.png")


# ------------------------------------------------------------------ SERIT (yol + kafes kapi), her oyuncu
KAM = {"z": 2.6, "egim": 10.5, "lens": 21.85, "sensor": 24.0}
KAPI = {"y": 8.0, "w": 6.0, "h": 4.1, "kiris": 0.5, "kule": 0.5}


def kafes_kule(x0, y0, z0, z1, kal, mat, ince):
    k = kal / 2
    for dx in (-k, k):
        for dy in (-k, k):
            boru((x0 + dx, y0 + dy, z0), (x0 + dx, y0 + dy, z1), 0.065, mat)
    n = max(2, int((z1 - z0) / kal))
    adim = (z1 - z0) / n
    for i in range(n):
        za, zb = z0 + i * adim, z0 + (i + 1) * adim
        for (ax, ay, bx, by) in ((-k, -k, k, -k), (k, -k, k, k), (k, k, -k, k), (-k, k, -k, -k)):
            boru((x0 + ax, y0 + ay, za), (x0 + bx, y0 + by, zb), 0.032, ince)
        for (ax, ay, bx, by) in ((-k, -k, k, -k), (k, -k, k, k), (k, k, -k, k), (-k, k, -k, -k)):
            boru((x0 + ax, y0 + ay, zb), (x0 + bx, y0 + by, zb), 0.032, ince)


def kafes_kiris(x0, x1, y0, z0, kal, mat, ince):
    k = kal / 2
    for dy in (-k, k):
        for dz in (-k, k):
            boru((x0, y0 + dy, z0 + dz), (x1, y0 + dy, z0 + dz), 0.065, mat)
    n = max(2, int((x1 - x0) / kal))
    adim = (x1 - x0) / n
    for i in range(n):
        xa, xb = x0 + i * adim, x0 + (i + 1) * adim
        for (ay, az, by_, bz) in ((-k, -k, -k, k), (-k, k, k, k), (k, k, k, -k), (k, -k, -k, -k)):
            boru((xa, y0 + ay, z0 + az), (xb, y0 + by_, z0 + bz), 0.032, ince)


def blok_kule(x0, y0, z0, z1, kal, mat, ince):
    """REF-054 kapisi bloklardan: ust uste yuvarlak bloklar (kendi tasarimimiz, civi/marka deseni yok) + ince capraz destek"""
    n = max(2, round((z1 - z0) / kal))
    adim = (z1 - z0) / n
    for i in range(n):
        z = z0 + (i + 0.5) * adim
        yuvarlak_kutu("blok", (x0, y0, z), (kal * 0.96, kal * 0.96, adim * 0.92), mat if i % 2 == 0 else ince, egim=0.1, seg=5)
    for i in range(n - 1):
        za, zb = z0 + (i + 0.5) * adim, z0 + (i + 1.5) * adim
        boru((x0 - kal * 0.5, y0 - kal * 0.52, za), (x0 + kal * 0.5, y0 - kal * 0.52, zb), 0.035, ince)


def blok_kiris(x0, x1, y0, z0, kal, mat, ince):
    n = max(2, round((x1 - x0) / kal))
    adim = (x1 - x0) / n
    for i in range(n + 1):
        yuvarlak_kutu("blok", (x0 + i * adim, y0, z0), (adim * 0.92, kal * 0.96, kal * 0.96), mat if i % 2 == 0 else ince, egim=0.1, seg=5)


def galaksi(rnd):
    """REF-054: gogun ortasinda dev galaksi sarmali (parlak cekirdek + iki kol, mor/sari/beyaz yildiz kumesi)"""
    cx_, cy_, cz_ = 0.0, 52.0, 16.0
    kure((cx_, cy_ + 1, cz_), 2.4, mat_emis("cekirdek", lin(hex3("#fff3c4")), 22))
    kure((cx_, cy_ + 2, cz_), 5.0, mat_emis("hale", lin(hex3("#c58cff")), 2.2))
    mats = [mat_emis("g%d" % i, lin(hex3(c)), e) for i, (c, e) in enumerate(
        (("#ffffff", 14), ("#f5ff3d", 12), ("#b45cff", 12), ("#ff7ae6", 10), ("#8fb4ff", 10)))]
    for kol in (0, math.pi):
        for i in range(520):
            u = rnd.random() ** 0.8
            r = 2.5 + u * 30
            a = kol + 2.6 * math.log(r / 2.5 + 1) * 1.9 + rnd.gauss(0, 0.22)
            x = cx_ + r * math.cos(a) + rnd.gauss(0, 0.9)
            z = cz_ + 0.55 * r * math.sin(a) + rnd.gauss(0, 0.6)
            kure((x, cy_ + rnd.uniform(-1, 1), z), rnd.uniform(0.07, 0.3) * (1.2 - u * 0.6), rnd.choice(mats), sub=1)


def gezegen(rnd):
    """REF-055: gogun ortasinda kapilarin arkasindan yukselen dev gezegen. Bizimki halkali, kizil-kehribar seritli
    (referansin pembe gezegeni yerine), altin parcacik halkasi + iki kucuk uydu."""
    cx_, cy_, cz_, R_ = 0.0, 50.0, 13.0, 13.0
    bpy.ops.mesh.primitive_uv_sphere_add(radius=R_, location=(cx_, cy_, cz_), segments=96, ring_count=48)
    g = bpy.context.active_object; bpy.ops.object.shade_smooth()
    g.rotation_euler = (math.radians(-18), math.radians(14), 0)
    m = bpy.data.materials.new("gezegen"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord")
    # deneme 1: Object koordinati (R=13) x olcek 2,4 -> nokta/moire deseni. Generated (0-1) + dusuk bozulma = gaz devi seritleri
    wv = nt.nodes.new("ShaderNodeTexWave"); wv.wave_type = "BANDS"; wv.bands_direction = "Z"
    wv.inputs["Scale"].default_value = 2.2; wv.inputs["Distortion"].default_value = 3.0; wv.inputs["Detail"].default_value = 3
    wv.inputs["Detail Scale"].default_value = 2.0
    nt.links.new(tc.outputs["Generated"], wv.inputs["Vector"])
    rp = nt.nodes.new("ShaderNodeValToRGB"); cr = rp.color_ramp
    # deneme 2: koyu bordo <-> acik sari seritler iki serit arasindaki dar boslukta "berber diregi" gibi okundu -> dar aralik
    cr.elements[0].position = 0.0; cr.elements[0].color = (*lin(hex3("#c2283f")), 1)
    cr.elements[1].position = 1.0; cr.elements[1].color = (*lin(hex3("#ffb070")), 1)
    for pos, c in ((0.35, "#e0405a"), (0.65, "#f26a4a")):
        e = cr.elements.new(pos); e.color = (*lin(hex3(c)), 1)
    nt.links.new(wv.outputs["Fac"], rp.inputs[0])
    # hacim: kenara dogru kararan (fresnel tersi) parlaklik -> duz disk degil kure okunur
    fr = nt.nodes.new("ShaderNodeLayerWeight"); fr.inputs["Blend"].default_value = 0.55
    kr = nt.nodes.new("ShaderNodeMath"); kr.operation = "SUBTRACT"; kr.inputs[0].default_value = 1.15
    nt.links.new(fr.outputs["Facing"], kr.inputs[1])
    gm = nt.nodes.new("ShaderNodeMath"); gm.operation = "MULTIPLY"; gm.inputs[1].default_value = 2.2
    nt.links.new(kr.outputs[0], gm.inputs[0])
    em = nt.nodes.new("ShaderNodeEmission")
    nt.links.new(rp.outputs[0], em.inputs[0]); nt.links.new(gm.outputs[0], em.inputs[1])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], o.inputs[0])
    g.data.materials.append(m)
    # hale: deneme 1'de 24 dilimli kure kose kose gorunuyordu -> 96 dilim, daha soluk
    bpy.ops.mesh.primitive_uv_sphere_add(radius=R_ * 1.08, location=(cx_, cy_ + 2.0, cz_), segments=96, ring_count=48)
    h_ = bpy.context.active_object; bpy.ops.object.shade_smooth()
    h_.data.materials.append(mat_emis("gezegen_hale", lin(hex3("#ff6a5a")), 0.45))
    # halka: altin/beyaz parcaciklar egik elips uzerinde
    mats = [mat_emis("h%d" % i, lin(hex3(c)), e) for i, (c, e) in enumerate((("#ffd27a", 9), ("#ffffff", 12), ("#ff8fa0", 8)))]
    for i in range(900):
        a = rnd.uniform(0, 2 * math.pi); r = R_ * rnd.uniform(1.35, 1.95)
        x = cx_ + r * math.cos(a); z = cz_ + 0.24 * r * math.sin(a) - 0.08 * r * math.cos(a)
        y = cy_ - 0.25 * r * math.sin(a)
        if y > cy_ and abs(x - cx_) < R_ * 0.95:      # gezegenin arkasinda kalan parcaciklar gorunmez, atla
            continue
        kure((x, y, z), rnd.uniform(0.08, 0.26), rnd.choice(mats), sub=1)
    for (x, z, r, c) in ((-24, 27, 2.2, "#5a78ff"), (22, 30, 1.4, "#ffe0c4")):
        kure((x, cy_ - 4, z), r, mat_emis("uydu", lin(hex3(c)), 3.0))


def aurora(rnd):
    """REF-057: gokte pembe/mor/camgobegi kuzey isigi perdeleri, ufukta karli buzlu daglar, onde parlak deniz + buz kutleleri."""
    renkler = ("#ff5ad8", "#9b6bff", "#3fe0ff", "#7dffd8")
    # deneme 1: 7 perde gogun tamamini dikey cizgiyle doldurdu (yagmur perdesi gibi) -> 4 perde, yalniz ust yari, yumusak
    # deneme 3: perdeler bulanik renkli bloklar gibi okundu -> Blender'da perde YOK; kuzey isigi sahne4.html'de
    # akan, hareketli seritler olarak cizilir (tema.kuzeyIsigi). Asagidaki dongu kalir ama calismaz.
    for i in range(0):
        x0, y0 = -36 + i * 24 + rnd.uniform(-6, 6), rnd.uniform(46, 54)
        bpy.ops.mesh.primitive_plane_add(size=1, location=(x0, y0, 22.5 + rnd.uniform(-1.5, 2)), rotation=(math.pi / 2, 0, rnd.uniform(-0.35, 0.35)))
        p = bpy.context.active_object; p.scale = (rnd.uniform(34, 48), rnd.uniform(8, 10), 1)      # deneme 2: z 31 kadraj ustune kacti
        bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.subdivide(number_cuts=40); bpy.ops.object.mode_set(mode="OBJECT")
        faz, gen = rnd.uniform(0, 6.28), rnd.uniform(1.5, 3.2)
        for v in p.data.vertices:                      # perde dalgasi: yerel x boyunca derinlik + yukseklikte kivrim
            v.co.z += gen * 0.06 * math.sin(v.co.x * 9 + faz) + 0.03 * math.sin(v.co.x * 23 + faz * 2)
        m = bpy.data.materials.new("aurora%d" % i); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
        tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Generated"], sep.inputs[0])
        rmp = nt.nodes.new("ShaderNodeValToRGB"); cr = rmp.color_ramp           # alt parlak -> ust saydam
        cr.elements[0].position = 0.0; cr.elements[0].color = (0, 0, 0, 1)
        cr.elements[1].position = 1.0; cr.elements[1].color = (0, 0, 0, 1)
        e = cr.elements.new(0.12); e.color = (1, 1, 1, 1)
        e = cr.elements.new(0.45); e.color = (0.35, 0.35, 0.35, 1)
        nt.links.new(sep.outputs["Y"], rmp.inputs[0])
        wv = nt.nodes.new("ShaderNodeTexWave"); wv.bands_direction = "X"; wv.inputs["Scale"].default_value = rnd.uniform(2.5, 4.0)
        wv.inputs["Distortion"].default_value = 1.4; wv.inputs["Detail"].default_value = 2
        nt.links.new(tc.outputs["Generated"], wv.inputs["Vector"])
        mu = nt.nodes.new("ShaderNodeMath"); mu.operation = "MULTIPLY"
        nt.links.new(rmp.outputs[0], mu.inputs[0]); nt.links.new(wv.outputs["Fac"], mu.inputs[1])
        mu2 = nt.nodes.new("ShaderNodeMath"); mu2.operation = "MULTIPLY"; mu2.inputs[1].default_value = 0.55
        nt.links.new(mu.outputs[0], mu2.inputs[0])
        em = nt.nodes.new("ShaderNodeEmission"); em.inputs[0].default_value = (*lin(hex3(renkler[i % 4])), 1); em.inputs[1].default_value = 2.0
        tr = nt.nodes.new("ShaderNodeBsdfTransparent")
        mx = nt.nodes.new("ShaderNodeMixShader")
        nt.links.new(mu2.outputs[0], mx.inputs[0]); nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2])
        o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(mx.outputs[0], o.inputs[0])
        m.blend_method = "BLEND"
        p.data.materials.append(m)
    # karli buzlu daglar: ufuk boyunca iki sira sivri koni kumesi (on sira daha acik/buz mavisi)
    kar = mat_jole("kar", lin(hex3("#f2f8ff")), emis=0.45, purluk=0.25)
    buz = mat_jole("buz", lin(hex3("#8cc8ff")), emis=0.35, purluk=0.18)
    for sira, (yy, zb, boy, mat) in enumerate(((44, -1.0, 14, buz), (36, -1.5, 9, kar))):
        x = -70.0
        while x < 70:
            h = rnd.uniform(0.5, 1.0) * boy; r = h * rnd.uniform(0.55, 0.85)
            bpy.ops.mesh.primitive_cone_add(vertices=rnd.choice([5, 6, 7]), radius1=r, depth=h, location=(x, yy + rnd.uniform(-2, 2), zb + h / 2),
                                            rotation=(0, 0, rnd.uniform(0, 3.14)))
            c = bpy.context.active_object; c.data.materials.append(mat)
            x += r * rnd.uniform(0.9, 1.4)
    # deniz: koyu mavi parlak yuzey (gok ve isik yansir) + yuzen buz kutleleri
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 22, -1.6)); d = bpy.context.active_object; d.scale = (160, 50, 1)
    dm = bpy.data.materials.new("deniz"); dm.use_nodes = True; b = dm.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*lin(hex3("#123a8a")), 1); b.inputs["Roughness"].default_value = 0.08
    b.inputs["Metallic"].default_value = 0.3
    d.data.materials.append(dm)
    isik("SUN", (0, 0, 30), 2.2, lin(hex3("#d6e4ff")), yon=(8, 40, 0))


def serit(oyuncu):
    sc = bos_sahne(w=960, h=1080, saydam=True)
    R = lin(hex3(RENK[oyuncu]))
    ana = mat_jole("ana", R, emis=0.08)
    acikm = mat_jole("acik", acik(R, 0.35), emis=0.15)
    koyum = mat_jole("koyu", koyu(R, 0.45), emis=0.02)
    ince = mat_jole("ince", acik(R, 0.1), emis=0.12)
    Y = KAPI["y"]
    # yol: kalin jole doseme (kamerdan kapiya ve biraz otesine)
    yuvarlak_kutu("yol", (0, (0.8 + Y + 2) / 2, -0.18), (4.4, Y + 2 - 0.8, 0.36), koyum, egim=0.12)
    yuvarlak_kutu("yol_ust", (0, (0.8 + Y + 2) / 2, 0.0), (3.9, Y + 2 - 0.8, 0.06), ana, egim=0.03)
    # yol kabarciklari: yuzeye yarim gomulu cam kureler (kullanici 17 Eki: "kabarciklarini ... nasil yaparsin").
    # Yon oklari sahne4.html'de hareketli cizilir (kameraya akar), burada yok.
    rnd = random.Random(21 if oyuncu == "p1" else 23)
    cam = mat_cam("yol_kabarcik")
    for i in range(70):
        r = rnd.choice([0.04, 0.06, 0.08, 0.1, 0.14, 0.2])
        kure((rnd.uniform(-1.85, 1.85), rnd.uniform(2.6, Y + 1.5), 0.03), r, cam)
    # korkuluk babalari + halat korkuluk (iki yanda)
    for s in (-1, 1):
        ys = [1.0 + i * 1.25 for i in range(int((Y - 1.0) / 1.25) + 1)]
        for yy in ys:
            yuvarlak_kutu("baba", (s * 2.35, yy, 0.32), (0.34, 0.34, 0.64), ana, egim=0.12)
            kure((s * 2.35, yy, 0.68), 0.15, acikm)
        boru((s * 2.35, ys[0], 0.46), (s * 2.35, ys[-1], 0.46), 0.05, ince)
        boru((s * 2.35, ys[0], 0.22), (s * 2.35, ys[-1], 0.22), 0.04, ince)
    # kafes kapi: iki kule + ust kiris + birlesim kupleri
    W, H, KK, KR = KAPI["w"], KAPI["h"], KAPI["kule"], KAPI["kiris"]
    xk = W / 2 - KK / 2
    for s in (-1, 1):
        (blok_kule if KAPI_TIP == "blok" else kafes_kule)(s * xk, Y, 0.0, H + KR, KK, ana, ince)
        yuvarlak_kutu("taban", (s * xk, Y, 0.12), (KK + 0.3, KK + 0.3, 0.24), koyum, egim=0.06)
        for zz in (H, H + KR):
            yuvarlak_kutu("dugum", (s * xk, Y, zz), (KK * 0.55, KK * 0.55, KK * 0.55), acikm, egim=0.08)
    (blok_kiris if KAPI_TIP == "blok" else kafes_kiris)(-xk, xk, Y, H + KR / 2, KR, ana, ince)
    # --- zenginlestirme (kullanici 17 Eki: "kapilar ... cok sade ... gorsel solen"):
    # neon tup acikligi cevreler, ampul dizisi (sahne4.html yakip sondurur), ust tabela, kose yildizlari, isikli kaide
    ic = W / 2 - KK
    neon = mat_emis("neon", acik(R, 0.35), 9.0)
    for a, b in (((-ic + 0.12, Y - 0.3, 0.05), (-ic + 0.12, Y - 0.3, H - 0.12)), ((ic - 0.12, Y - 0.3, 0.05), (ic - 0.12, Y - 0.3, H - 0.12)),
                 ((-ic + 0.12, Y - 0.3, H - 0.12), (ic - 0.12, Y - 0.3, H - 0.12))):
        boru(a, b, 0.045, neon)
    amp = mat_emis("ampul", lin(hex3("#fff1c4")), 2.5)
    AMPUL = []
    n_ust = 15
    for i in range(n_ust):
        x = -ic + 0.25 + i * (2 * ic - 0.5) / (n_ust - 1)
        AMPUL.append(Vector((x, Y - KK / 2 + 0.05, H - 0.06)))          # kirisin alt yuzu (tabela onde)
    for s_ in (-1, 1):
        for j in range(11):
            AMPUL.append(Vector((s_ * xk, Y - KK / 2 - 0.05, 0.35 + j * (H - 0.5) / 10)))
    for q in AMPUL:
        kure(q, 0.075, amp)
    # ust tabela: yuvarlak jole plaka + kabartma yazi
    # kadraj ustu ~5,2 m'de bitiyor: tabela kirisin ONUNDE (ustunde degil)
    yuvarlak_kutu("tabela", (0, Y - KK / 2 - 0.2, H + KR / 2), (2.3, 0.14, 0.56), koyum, egim=0.14, seg=6)
    yuvarlak_kutu("tabela_cerceve", (0, Y - KK / 2 - 0.14, H + KR / 2), (2.5, 0.12, 0.68), acikm, egim=0.18, seg=6)
    try:
        font = bpy.data.fonts.load(os.path.join(KOK, "05-kapak/fontlar/TitanOne.ttf"))
        bpy.ops.object.text_add(location=(0, Y - KK / 2 - 0.29, H + KR / 2 - 0.02), rotation=(math.pi / 2, 0, 0))
        tx = bpy.context.active_object
        tx.data.body = "PLAYER 1" if oyuncu == "p1" else "PLAYER 2"
        tx.data.font = font; tx.data.size = 0.38; tx.data.extrude = 0.04; tx.data.bevel_depth = 0.012
        tx.data.align_x = "CENTER"; tx.data.align_y = "CENTER"
        tx.data.materials.append(mat_emis("tabela_yazi", (1, 1, 1), 3.5))
    except Exception as e:
        log("tabela yazisi atlandi:", e)
    # kose yildizlari (jole, kule tepelerinde) + kure tepelikler
    yildiz_m = mat_jole("yildiz", lin(hex3("#ffd23a")), emis=0.25)
    for s_ in (-1, 1):
        bpy.ops.mesh.primitive_circle_add(vertices=10, radius=0.4, fill_type="NGON", location=(s_ * xk, Y - KK / 2 - 0.15, H + KR + 0.25), rotation=(math.pi / 2, 0, 0))
        yo = bpy.context.active_object
        bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.object.mode_set(mode="OBJECT")
        for i, v in enumerate(yo.data.vertices):
            if i % 2:
                v.co *= 0.45
        so = yo.modifiers.new("kal", "SOLIDIFY"); so.thickness = 0.22; so.offset = 0
        bv = yo.modifiers.new("egim", "BEVEL"); bv.width = 0.06; bv.segments = 4; bv.limit_method = "NONE"
        yo.data.materials.append(yildiz_m); bpy.ops.object.shade_smooth()

    # isikli kaide basamagi (kapinin onunde)
    yuvarlak_kutu("kaide", (0, Y - 0.55, 0.06), (W + 0.4, 0.7, 0.16), koyum, egim=0.06)
    boru((-W / 2 - 0.1, Y - 0.92, 0.12), (W / 2 + 0.1, Y - 0.92, 0.12), 0.035, neon)
    # isiklar
    isik("AREA", (0, -1.5, 6.5), 380, (1, 1, 1), 6, yon=(0, Y * 0.6, 0))
    isik("AREA", (-4, 3, 3), 260, acik(R, 0.2), 3, yon=(0, Y, 2))
    isik("AREA", (4, 3, 3), 220, lin(hex3("#7fe7ff")), 3, yon=(0, Y, 2))
    isik("AREA", (0, Y + 3, 6), 500, acik(R, 0.1), 5, yon=(0, Y, 1))
    # kamera
    rx = math.radians(90 - KAM["egim"])
    bpy.ops.object.camera_add(location=(0, 0, KAM["z"]), rotation=(rx, 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.sensor_fit = "VERTICAL"; kam.data.sensor_height = KAM["sensor"]; kam.data.lens = KAM["lens"]
    # kapi acikligi piksel kutusu (sahne4.html duvari buraya oturtur)
    ic = W / 2 - KK
    noktalar = [Vector((-ic, Y, 0)), Vector((ic, Y, 0)), Vector((-ic, Y, H)), Vector((ic, Y, H))]
    bpy.context.view_layer.update()
    px = [world_to_camera_view(sc, kam, p) for p in noktalar]
    xs = [p.x * 960 for p in px]; ys = [(1 - p.y) * 1080 for p in px]
    YERLESIM["aciklik_" + oyuncu] = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
    log("aciklik", oyuncu, YERLESIM["aciklik_" + oyuncu])
    YERLESIM["ampul_" + oyuncu] = [[round(p.x * 960, 1), round((1 - p.y) * 1080, 1)] for p in (world_to_camera_view(sc, kam, q) for q in AMPUL)]
    yaz(sc, "serit-%s.png" % oyuncu)


# ------------------------------------------------------------------ PANEL (jole duvar)
def mat_girdap(R):
    """REF-055 duvari: ortasi beyaz parlayan, oyuncu renginde sarmal girdap (boya firca dokulu), cevresi koyulasir"""
    m = bpy.data.materials.new("girdap"); m.use_nodes = True; nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    # sarmal (deneme 1'de RINGS ic ice halka = hedef tahtasi okunuyordu): s = sin(4*r + 2*aci + gurultu) -> iki kollu girdap,
    # gurultu firca izi verir. Panel on yuzu XZ duzleminde (Object koordinati, merkez 0).
    sp = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Object"], sp.inputs[0])
    at = nt.nodes.new("ShaderNodeMath"); at.operation = "ARCTAN2"
    nt.links.new(sp.outputs["Z"], at.inputs[0]); nt.links.new(sp.outputs["X"], at.inputs[1])
    uz = nt.nodes.new("ShaderNodeVectorMath"); uz.operation = "LENGTH"; nt.links.new(tc.outputs["Object"], uz.inputs[0])
    m1 = nt.nodes.new("ShaderNodeMath"); m1.operation = "MULTIPLY"; m1.inputs[1].default_value = 4.0
    nt.links.new(uz.outputs["Value"], m1.inputs[0])
    m2 = nt.nodes.new("ShaderNodeMath"); m2.operation = "MULTIPLY"; m2.inputs[1].default_value = 2.0
    nt.links.new(at.outputs[0], m2.inputs[0])
    gz = nt.nodes.new("ShaderNodeTexNoise"); gz.inputs["Scale"].default_value = 2.5; gz.inputs["Detail"].default_value = 8
    gz.inputs["Distortion"].default_value = 1.5; nt.links.new(tc.outputs["Object"], gz.inputs["Vector"])
    m3 = nt.nodes.new("ShaderNodeMath"); m3.operation = "MULTIPLY"; m3.inputs[1].default_value = 2.4
    nt.links.new(gz.outputs["Fac"], m3.inputs[0])
    t1 = nt.nodes.new("ShaderNodeMath"); t1.operation = "ADD"; nt.links.new(m1.outputs[0], t1.inputs[0]); nt.links.new(m2.outputs[0], t1.inputs[1])
    t2 = nt.nodes.new("ShaderNodeMath"); t2.operation = "ADD"; nt.links.new(t1.outputs[0], t2.inputs[0]); nt.links.new(m3.outputs[0], t2.inputs[1])
    sn = nt.nodes.new("ShaderNodeMath"); sn.operation = "SINE"; nt.links.new(t2.outputs[0], sn.inputs[0])
    wv = nt.nodes.new("ShaderNodeMath"); wv.operation = "MULTIPLY_ADD"; wv.inputs[1].default_value = 0.5; wv.inputs[2].default_value = 0.5
    nt.links.new(sn.outputs[0], wv.inputs[0])
    rp = nt.nodes.new("ShaderNodeValToRGB"); cr = rp.color_ramp
    cr.elements[0].position = 0.15; cr.elements[0].color = (*koyu(R, 0.25), 1)
    cr.elements[1].position = 0.9; cr.elements[1].color = (*acik(R, 0.7), 1)
    e = cr.elements.new(0.5); e.color = (*R, 1)
    nt.links.new(wv.outputs[0], rp.inputs[0])
    # merkez parlama: kuresel gecis (Object koordinati 0 merkezde)
    mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (0.42, 1.0, 0.5)
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    gr = nt.nodes.new("ShaderNodeTexGradient"); gr.gradient_type = "SPHERICAL"
    nt.links.new(mp.outputs[0], gr.inputs["Vector"])
    rp2 = nt.nodes.new("ShaderNodeValToRGB"); c2 = rp2.color_ramp
    c2.elements[0].position = 0.0; c2.elements[0].color = (0, 0, 0, 1)
    c2.elements[1].position = 0.75; c2.elements[1].color = (1, 1, 1, 1)
    nt.links.new(gr.outputs["Fac"], rp2.inputs[0])
    mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"; mx.blend_type = "SCREEN"
    nt.links.new(rp2.outputs[0], mx.inputs[0]); nt.links.new(rp.outputs[0], mx.inputs[6])
    mx.inputs[7].default_value = (1, 0.97, 0.95, 1)
    nt.links.new(mx.outputs[2], b.inputs["Base Color"])
    nt.links.new(mx.outputs[2], b.inputs["Emission Color"]); b.inputs["Emission Strength"].default_value = 0.55
    bm = nt.nodes.new("ShaderNodeBump"); bm.inputs["Strength"].default_value = 0.25
    nt.links.new(wv.outputs[0], bm.inputs["Height"]); nt.links.new(bm.outputs[0], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = 0.35
    b.inputs["Coat Weight"].default_value = 0.6; b.inputs["Coat Roughness"].default_value = 0.05
    return m


def panel(oyuncu):
    sc = bos_sahne(w=1100, h=904, saydam=True)
    R = lin(hex3(RENK[oyuncu]))
    PW, PH = 5.0, 4.1
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    p = bpy.context.active_object; p.scale = (PW, 0.25, PH); bpy.ops.object.transform_apply(scale=True)
    bv = p.modifiers.new("egim", "BEVEL"); bv.width = 0.22; bv.segments = 8; bv.limit_method = "NONE"
    bpy.ops.object.shade_smooth()
    if PANEL_TIP == "girdap":
        p.data.materials.append(mat_girdap(R))
        rnd = random.Random(7 if oyuncu == "p1" else 11)
        par = mat_emis("parilti", (1, 1, 1), 10.0)
        for i in range(60):
            kure((rnd.uniform(-PW / 2 + 0.2, PW / 2 - 0.2), -0.14, rnd.uniform(-PH / 2 + 0.2, PH / 2 - 0.2)), rnd.choice([0.02, 0.03, 0.04, 0.06]), par, sub=1)
        isik("AREA", (-3, -4, 4), 260, (1, 1, 1), 3, yon=(0, 0, 0))
        bpy.ops.object.camera_add(location=(0, -10, 0), rotation=(math.radians(90), 0, 0))
        kam = bpy.context.active_object; sc.camera = kam
        kam.data.type = "ORTHO"; kam.data.ortho_scale = PW + 0.08
        yaz(sc, "panel-%s.png" % oyuncu)
        return
    # jole: acik-orta renk dalgali seritler (wave texture) + kabarcik pürüzü
    m = bpy.data.materials.new("panel"); m.use_nodes = True; nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    wv = nt.nodes.new("ShaderNodeTexWave"); wv.wave_type = "BANDS"; wv.bands_direction = "DIAGONAL"
    wv.inputs["Scale"].default_value = 0.9; wv.inputs["Distortion"].default_value = 7.0; wv.inputs["Detail"].default_value = 3
    nt.links.new(tc.outputs["Object"], wv.inputs["Vector"])
    rp = nt.nodes.new("ShaderNodeValToRGB"); cr = rp.color_ramp
    cr.elements[0].position = 0.25; cr.elements[0].color = (*acik(R, 0.38), 1)
    cr.elements[1].position = 0.85; cr.elements[1].color = (*R, 1)
    nt.links.new(wv.outputs["Fac"], rp.inputs[0])
    nt.links.new(rp.outputs[0], b.inputs["Base Color"])
    bm = nt.nodes.new("ShaderNodeBump"); bm.inputs["Strength"].default_value = 0.35
    nt.links.new(wv.outputs["Fac"], bm.inputs["Height"]); nt.links.new(bm.outputs[0], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = 0.05
    b.inputs["Coat Weight"].default_value = 1.0; b.inputs["Coat Roughness"].default_value = 0.02
    b.inputs["Subsurface Weight"].default_value = 0.35
    b.inputs["Emission Color"].default_value = (*acik(R, 0.3), 1); b.inputs["Emission Strength"].default_value = 0.12
    p.data.materials.append(m)
    # kabarciklar (on yuzde yarim gomulu cam kureler)
    rnd = random.Random(7 if oyuncu == "p1" else 11)
    cam = mat_cam("kabarcik")
    for i in range(38):
        r = rnd.choice([0.05, 0.07, 0.09, 0.12, 0.18, 0.28])
        kure((rnd.uniform(-PW / 2 + 0.3, PW / 2 - 0.3), -0.13, rnd.uniform(-PH / 2 + 0.3, PH / 2 - 0.3)), r, cam)
    isik("AREA", (-3, -4, 4), 420, (1, 1, 1), 3, yon=(0, 0, 0))
    isik("AREA", (3.5, -3, -2), 200, acik(R, 0.2), 4, yon=(0, 0, 0))
    isik("AREA", (0, -3, 0), 60, (1, 1, 1), 8, yon=(0, 0, 0))
    bpy.ops.object.camera_add(location=(0, -10, 0), rotation=(math.radians(90), 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.type = "ORTHO"; kam.data.ortho_scale = PW + 0.08
    yaz(sc, "panel-%s.png" % oyuncu)


# ------------------------------------------------------------------ POZ MASKELERI
def kemik(arm, son):
    for b in arm.pose.bones:
        if b.name.endswith(":" + son) or b.name == son:
            return b
    raise KeyError(son)


def yon_vek(a, ileri):
    """ekran acisi -> dunya yonu (kamera -Y'de, +Y'ye bakar; ekran sag = +X, yukari = +Z).
    "geri": kameradan uzaga (onden diz cokmede baldir) - ekran duzlemi acisiyla cizilemiyordu."""
    if a == "geri":
        return Vector((0, 1, 0))
    r = math.radians(a)
    return Vector((math.sin(r), 0, -math.cos(r)))


def yonelt(arm, pb, d_dunya):
    bpy.context.view_layer.update()
    d = (arm.matrix_world.to_3x3().inverted() @ d_dunya).normalized()
    M = pb.matrix.copy()
    bas = M.translation.copy()
    cur = Vector(M.col[1][:3]).normalized()
    q = cur.rotation_difference(d)
    yeni = Matrix.Translation(bas) @ q.to_matrix().to_4x4() @ Matrix.Translation(-bas) @ M
    pb.matrix = yeni
    bpy.context.view_layer.update()


def dunya_kutusu(objs):
    xs, ys, zs = [], [], []
    dg = bpy.context.evaluated_depsgraph_get()
    for o in objs:
        oe = o.evaluated_get(dg); me = oe.to_mesh()
        for v in me.vertices:
            q = oe.matrix_world @ v.co
            xs.append(q.x); ys.append(q.y); zs.append(q.z)
        oe.to_mesh_clear()
    return Vector((min(xs), min(ys), min(zs))), Vector((max(xs), max(ys), max(zs)))


def poz_maskeleri():
    # Cycles + duz siyah emisyon (Workbench headless runner'da OpenGL baglami istiyor; Cycles her yerde calisir)
    sc = bos_sahne(motor="CYCLES", w=900, h=740, saydam=True, ornek=16)
    sc.frame_set(1)
    sc.cycles.use_denoising = False
    sc.view_settings.view_transform = "Standard"
    once = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=os.path.join(KOK, "02-hareketler/siluet-govde.fbx"), automatic_bone_orientation=False)
    yeni = [o for o in bpy.data.objects if o not in once]
    arm = [o for o in yeni if o.type == "ARMATURE"][0]
    mesler = [o for o in yeni if o.type == "MESH"]
    siyah = mat_emis("siluet", (0, 0, 0), 0.0)
    for m in mesler:
        m.data.materials.clear(); m.data.materials.append(siyah)
        for poly in m.data.polygons:
            poly.material_index = 0
    log("mesler", [m.name for m in mesler], "kemik", len(arm.pose.bones), "aksiyon", bool(arm.animation_data and arm.animation_data.action))
    # FBX bir dinlenme aksiyonu tasiyor: render aninda kare guncellemesi pozu sifirliyordu (deneme 1: 8 maske de duz durus)
    arm.animation_data_clear()
    for o in mesler:
        o.animation_data_clear()
    # yuzu kameraya: sol omuz +X'te
    pb = arm.pose.bones
    L = arm.matrix_world @ kemik(arm, "LeftArm").head; Rr = arm.matrix_world @ kemik(arm, "RightArm").head
    v = L - Rr; v.z = 0
    arm.rotation_euler.z -= math.atan2(v.y, v.x)
    bpy.context.view_layer.update()
    taban_rot = arm.rotation_euler.z
    bpy.ops.object.camera_add(location=(0, -12, 1), rotation=(math.radians(90), 0, 0))
    kam = bpy.context.active_object; sc.camera = kam; kam.data.type = "ORTHO"
    ASPECT = 900 / 740
    for ad, P in POZLAR.items():
        for b in pb:
            b.matrix_basis = Matrix.Identity(4)
        arm.rotation_euler.z = taban_rot + (math.radians(90) if P.get("yon") == "sag" else 0)
        bpy.context.view_layer.update()
        ileri = Vector((1, 0, 0)) if P.get("yon") == "sag" else Vector((0, -1, 0))
        g = P.get("govde", 180); ba = P.get("bas", 0)
        for k, aci in (("Spine", g), ("Spine1", g), ("Spine2", g), ("Neck", g + ba), ("Head", g + ba)):
            try:
                yonelt(arm, kemik(arm, k), yon_vek(aci, ileri))
            except KeyError:
                pass
        for taraf, anah in (("Left", "sol"), ("Right", "sag")):
            kol = P.get(anah + "Kol", [-12 if anah == "sag" else 12] * 2)
            yonelt(arm, kemik(arm, taraf + "Arm"), yon_vek(kol[0], ileri))
            yonelt(arm, kemik(arm, taraf + "ForeArm"), yon_vek(kol[1], ileri))
            yonelt(arm, kemik(arm, taraf + "Hand"), yon_vek(kol[1], ileri))
            bac = P.get(anah + "Bacak", [-3 if anah == "sag" else 3, 0])
            yonelt(arm, kemik(arm, taraf + "UpLeg"), yon_vek(bac[0], ileri))
            yonelt(arm, kemik(arm, taraf + "Leg"), yon_vek(bac[1], ileri))
            baldir = yon_vek(bac[1], ileri)
            if baldir.dot(ileri) < -0.5 or bac[1] == "geri":      # diz cokme: baldir geride yatay -> ayak da geriye, yere
                ayak = (baldir * 0.7 + Vector((0, 0, -0.7))).normalized()
            else:
                ayak = (ileri * 0.9 + baldir * 0.35).normalized()
            yonelt(arm, kemik(arm, taraf + "Foot"), ayak)
        alt, ust = dunya_kutusu(mesler)
        gen, yuk = ust.x - alt.x, ust.z - alt.z
        olc = 2.55                                   # cerceve yuksekligi (m): ayakta figur ~%72
        if yuk > olc * 0.92:
            olc = yuk / 0.92
        if gen > olc * ASPECT * 0.92:
            olc = gen / (ASPECT * 0.92)
        kam.data.ortho_scale = olc * ASPECT          # ortho_scale genis kenara (yatay) uygulanir
        kam.location = ((alt.x + ust.x) / 2, -12, alt.z - olc * 0.04 + olc / 2)
        bpy.context.view_layer.update()
        YERLESIM.setdefault("poz", {})[ad] = {"cerceve_m": round(olc, 3), "gen_m": round(gen, 3), "yuk_m": round(yuk, 3)}
        log("poz", ad, "gen", round(gen, 2), "yuk", round(yuk, 2), "cerceve", round(olc, 2))
        yaz(sc, "poz/%s.png" % ad)


# ------------------------------------------------------------------ ana akis
# 5. video (REF-056, 3 oyuncu, Halloween): ayri betik, buradaki yardimcilarla calisir
if arg("--mod", "pvp") == "boksor":       # 6. video (REF-057) acilis boksorleri
    exec(compile(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "boksor.py"), encoding="utf-8").read(), "boksor.py", "exec"))
elif arg("--mod", "pvp") == "cadi":
    exec(compile(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "varlik-cadi.py"), encoding="utf-8").read(), "varlik-cadi.py", "exec"))
else:
    if YALNIZ in ("hepsi", "poz"):
        poz_maskeleri()
    if YALNIZ in ("hepsi", "sahne"):
        gok()
        for o in ("p1", "p2"):
            serit(o)
            panel(o)
    json.dump(YERLESIM, open(os.path.join(CIKTI, "yerlesim.json"), "w"), indent=1)
    log("bitti", YERLESIM)
