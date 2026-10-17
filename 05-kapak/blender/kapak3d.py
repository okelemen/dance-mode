"""KAPAK 3B — Blender (headless) sahnesi. Masaustu CLAUDE.md md. 21 (tum videolar icin).

    blender -b --factory-startup -P kapak3d.py -- --ayar ayar.json --ornek 96 --cikti klasor

Ayar JSON: { "baslik": "TETRIS MODE", "font": "05-kapak/fontlar/TitanOne.ttf",
             "harf_renk": [[r,g,b],...], "panel_renk": [[r,g,b],[r,g,b]],
             "varyant": [ { "ad": "A", "klip": "02-hareketler/arms-up.fbx", "kare": "el_tepe",
                            "sol": ["2 Player","Co-op"], "sag": ["80 Walls","10 MIN"] }, ... ] }
kare: "el_tepe" (eller en yuksek) | "en_genis" (el/ayak yayilimi en buyuk) | sayi (klip karesi)

Sahne (referans: @HumanWarmUp kapaklari, olcum REFERANS-KANALLAR/10-HUMANWARMUP-KAPAK-OLCUM.md):
- ustte kamera onunde 3B kabartma baslik: harf harf parlak (coat) renk + beyaz ve koyu "ters kabuk" kontur
- yansimali koyu zemin, neon yol kenarlari, V ok seritleri, korkuluk direkleri, ufukta isikli sehir
- uzakta iki renkli duvar paneli (P1/P2) + icinde ayni pozun kucuk kopyasi
- on planda iki gercek insan bedenli siluet (Mixamo govde + poz klibi), siyah parlak + beyaz kabuk kontur
- arkadan pembe/mavi kontra isik, compositor Glare (Fog Glow) ile isik patlamasi
"""
import bpy, bmesh, json, math, os, sys, random
from mathutils import Vector, Euler

argv = sys.argv[sys.argv.index("--") + 1:]
arg = lambda ad, v=None: argv[argv.index(ad) + 1] if ad in argv else v
KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
AYAR = json.load(open(os.path.join(KOK, arg("--ayar")), encoding="utf-8"))
ORNEK = int(arg("--ornek", "96"))
CIKTI = os.path.abspath(arg("--cikti", "cikti"))
os.makedirs(CIKTI, exist_ok=True)
rnd = random.Random(51)


def log(*a):
    print("[kapak3d]", *a, flush=True)


# ------------------------------------------------------------------ malzemeler
def mat_emisyon(ad, renk, guc):
    m = bpy.data.materials.new(ad); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    e = nt.nodes.new("ShaderNodeEmission"); e.inputs[0].default_value = (*renk, 1); e.inputs[1].default_value = guc
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(e.outputs[0], o.inputs[0])
    return m


def mat_parlak(ad, renk, purluk=0.2, metal=0.0, coat=1.0, emis=0.0):
    m = bpy.data.materials.new(ad); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*renk, 1)
    b.inputs["Roughness"].default_value = purluk
    b.inputs["Metallic"].default_value = metal
    b.inputs["Coat Weight"].default_value = coat
    b.inputs["Coat Roughness"].default_value = 0.05
    if emis:
        b.inputs["Emission Color"].default_value = (*renk, 1)
        b.inputs["Emission Strength"].default_value = emis
    return m


def mat_kabuk(ad, renk, guc=1.0):
    """ters kabuk kontur: yalniz arka yuzler gorunur (Backfacing), on yuzler saydam"""
    m = bpy.data.materials.new(ad); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    g = nt.nodes.new("ShaderNodeNewGeometry")
    t = nt.nodes.new("ShaderNodeBsdfTransparent")
    e = nt.nodes.new("ShaderNodeEmission"); e.inputs[0].default_value = (*renk, 1); e.inputs[1].default_value = guc
    mx = nt.nodes.new("ShaderNodeMixShader")
    o = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(g.outputs["Backfacing"], mx.inputs[0])
    # ters kabukta kameraya en yakin yuzler (cevrilmis normal -> Backfacing=1) SAYDAM olmali, yalniz
    # siluetin kenarindan tasan uzak yuzler (Backfacing=0) renkli gorunur. (ilk render'da tersti: figur bembeyaz)
    nt.links.new(e.outputs[0], mx.inputs[1]); nt.links.new(t.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], o.inputs[0])
    return m


def kabuk_ekle(obj, kalinlik, mat):
    """objeye ters kabuk (Solidify, normal ters) — beyaz/koyu kontur"""
    obj.data.materials.append(mat)
    idx = len(obj.data.materials) - 1
    s = obj.modifiers.new("kabuk_%d" % idx, "SOLIDIFY")
    s.thickness = kalinlik; s.offset = 1.0; s.use_flip_normals = True; s.use_rim = False
    s.material_offset = idx
    return s


def hex3(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def lin(c):
    return tuple(((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c)


# ------------------------------------------------------------------ sahne temeli
def sahne_kur():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = ORNEK
    sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = 1280, 720
    sc.render.film_transparent = False
    sc.view_settings.view_transform = "AgX"
    try:
        sc.view_settings.look = "AgX - Punchy"
    except Exception:
        pass
    w = bpy.data.worlds.new("dunya"); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (*lin((0.06, 0.02, 0.12)), 1); bg.inputs[1].default_value = 1.0
    return sc


def kutu(ad, konum, boyut, mat):
    bpy.ops.mesh.primitive_cube_add(size=1, location=konum)
    o = bpy.context.active_object; o.name = ad; o.scale = boyut
    o.data.materials.append(mat); return o


def zemin_ve_yol(renk_kenar, renk_ok, renk_iki):
    bpy.ops.mesh.primitive_plane_add(size=400, location=(0, 100, 0))
    z = bpy.context.active_object; z.name = "zemin"
    z.data.materials.append(mat_parlak("zemin", lin((0.05, 0.02, 0.10)), purluk=0.12, metal=0.4, coat=0.6))
    # zemin izgarasi (ince emisyon cizgileri, yanlarda)
    izg = mat_emisyon("izgara", lin((0.55, 0.25, 0.9)), 1.2)
    for i in range(-30, 31):
        if abs(i) < 3: continue
        kutu("izgX%d" % i, (i * 1.6, 60, 0.005), (0.025, 120, 0.004), izg)
    for j in range(0, 70):
        kutu("izgY%d" % j, (0, j * 1.8, 0.004), (100, 0.025, 0.004), izg)
    # yol
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 60, 0.01))
    y = bpy.context.active_object; y.scale = (6.0, 140, 1)
    y.data.materials.append(mat_parlak("yol", lin((0.09, 0.05, 0.16)), purluk=0.18, metal=0.2, coat=0.8))
    # neon kenarlar
    for kx, rr in ((-3.1, renk_kenar), (3.1, renk_kenar)):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=140, location=(kx, 60, 0.07), rotation=(math.pi / 2, 0, 0))
        bpy.context.active_object.data.materials.append(mat_emisyon("kenar", rr, 18))
    # V oklari
    okm = mat_emisyon("ok", (1, 1, 1), 4)                       # referansta oklar beyaz
    for j in range(2, 40):
        yj = j * 3.0
        for s_ in (-1, 1):
            o = kutu("ok%d%d" % (j, s_), (s_ * 1.0, yj, 0.02), (2.1, 0.12, 0.01), okm)
            o.rotation_euler = (0, 0, s_ * math.radians(-18))
    # korkuluk direkleri + ust neon serit
    dm = mat_parlak("direk", lin((0.15, 0.13, 0.22)), purluk=0.3, metal=0.8, coat=0.2)
    for s_, rr in ((-1, renk_kenar), (1, renk_iki)):
        for j in range(0, 40):
            kutu("direk%d%d" % (s_, j), (s_ * 4.0, j * 3.0, 0.6), (0.08, 0.08, 1.2), dm)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=140, location=(s_ * 4.0, 60, 1.22), rotation=(math.pi / 2, 0, 0))
        bpy.context.active_object.data.materials.append(mat_emisyon("korkuluk", rr, 14))


def sehir():
    renkler = [lin(hex3(h)) for h in ("#ff4fa3", "#38bdf8", "#a855f7", "#22d3ee", "#facc15")]
    gov = mat_parlak("bina", lin((0.07, 0.04, 0.14)), purluk=0.5)
    pen = [mat_emisyon("pencere%d" % i, c, 3.0) for i, c in enumerate(renkler)]
    x = -60
    while x < 60:
        w_ = rnd.uniform(2, 6); h_ = rnd.uniform(4, 22)
        y_ = rnd.uniform(110, 140)
        if abs(x) < 7: h_ *= 0.5
        b = kutu("bina", (x, y_, h_ / 2), (w_, 3, h_), gov)
        # pencere seritleri (on yuzde ince emisyon)
        m = rnd.choice(pen)
        for k in range(int(h_ / 1.4)):
            if rnd.random() < 0.55:
                kutu("pnc", (x, y_ - 1.55, 0.8 + k * 1.4), (w_ * 0.8, 0.02, 0.18), m)
        if rnd.random() < 0.35:
            kutu("neon", (x, y_ - 1.56, h_), (w_, 0.03, 0.08), rnd.choice(pen))
        x += w_ + rnd.uniform(0.3, 1.8)
    # gezegen
    bpy.ops.mesh.primitive_uv_sphere_add(radius=9, location=(62, 170, 46), segments=48, ring_count=24)
    bpy.context.active_object.data.materials.append(mat_emisyon("gezegen", lin(hex3("#e05cc4")), 2.2))


def gok_ve_kemerler(renkler):
    """referanstaki gibi yolun ustunden gecen neon kemerler + yildizli gok (gok bos kalmaz)"""
    # havai fisek (referans: 5,9 Mn'luk kapak) — gokte isinsal patlamalar
    for j in range(6):
        cx_, cz_ = rnd.uniform(-26, 26), rnd.uniform(14, 30); cy_ = rnd.uniform(60, 90)
        fm = mat_emisyon("fisek%d" % j, lin(renkler[j % len(renkler)]), 14)
        for i in range(36):
            a1 = rnd.uniform(0, 2 * math.pi); a2 = rnd.uniform(-1.2, 1.2); L = rnd.uniform(2.5, 5.0)
            d = Vector((math.cos(a1) * math.cos(a2), 0.2 * math.sin(a2), math.sin(a1) * math.cos(a2)))
            bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=L, location=Vector((cx_, cy_, cz_)) + d * (L / 2 + 0.6))
            c = bpy.context.active_object; c.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
            c.data.materials.append(fm)
    ym = mat_emisyon("yildiz", (1, 1, 1), 6)
    for i in range(380):
        x = rnd.uniform(-160, 160); z = rnd.uniform(18, 120); y = rnd.uniform(180, 220)
        bpy.ops.mesh.primitive_ico_sphere_add(radius=rnd.uniform(0.12, 0.35), subdivisions=1, location=(x, y, z))
        bpy.context.active_object.data.materials.append(ym)


def paneller(renkler):
    cer = mat_parlak("cerceve", lin((0.75, 0.75, 0.82)), purluk=0.25, metal=1.0, coat=0.0)
    for s_, r in ((-1, renkler[0]), (1, renkler[1])):
        bpy.ops.mesh.primitive_plane_add(size=1, location=(s_ * 2.05, 18, 2.2), rotation=(math.pi / 2, 0, 0))
        p = bpy.context.active_object; p.scale = (4.0, 3.2, 1)
        p.data.materials.append(mat_emisyon("panel", lin(r), 3.0))
    # kafes (truss) kapi: iki dikme + ust kiris, capraz cubuklu — referanstaki metal cerceve
    def kafes(a, b, kal=0.09):
        a, b = Vector(a), Vector(b); d = b - a
        for off in ((-0.18, -0.18), (0.18, -0.18), (-0.18, 0.18), (0.18, 0.18)):
            pass
        bpy.ops.mesh.primitive_cylinder_add(radius=kal, depth=d.length, location=(a + b) / 2)
        c = bpy.context.active_object; c.rotation_euler = d.to_track_quat("Z", "Y").to_euler(); c.data.materials.append(cer)
    for x0 in (-4.5, 4.5):
        for dx in (-0.2, 0.2):
            for dyy in (-0.2, 0.2):
                kafes((x0 + dx, 18 + dyy, 0), (x0 + dx, 18 + dyy, 4.6))
        for k in range(8):
            z0 = k * 0.55
            kafes((x0 - 0.2, 17.8, z0), (x0 + 0.2, 18.2, z0 + 0.55), 0.04)
    for z0 in (4.4, 4.8):
        for dyy in (-0.2, 0.2):
            kafes((-4.7, 18 + dyy, z0), (4.7, 18 + dyy, z0))
    for k in range(16):
        x0 = -4.5 + k * 0.6
        kafes((x0, 17.8, 4.4), (x0 + 0.6, 18.2, 4.8), 0.04)


# ------------------------------------------------------------------ karakter
def fbx_al(yol):
    once = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=os.path.join(KOK, yol), automatic_bone_orientation=False)
    return [o for o in bpy.data.objects if o not in once]


def kare_sec(arm, kip, bas, son):
    """klipte istenen kareyi bul: el_tepe | en_genis"""
    sc = bpy.context.scene
    en_iyi, kr = -1e9, bas
    for f in range(bas, son + 1):
        sc.frame_set(f)
        pb = arm.pose.bones
        def w(n):
            return arm.matrix_world @ pb[n].head
        try:
            el = [w("mixamorig:LeftHand"), w("mixamorig:RightHand")]
            ay = [w("mixamorig:LeftFoot"), w("mixamorig:RightFoot")]
        except KeyError:
            return bas
        if kip == "el_tepe":
            puan = min(el[0].z, el[1].z)
        else:
            puan = (el[0] - el[1]).length + (ay[0] - ay[1]).length
        if puan > en_iyi:
            en_iyi, kr = puan, f
    return kr


KABUK_KARAKTER = 1.8


def karakter(klip, kip, siyah, kabuk_b, kabuk_d):
    yeni = fbx_al("02-hareketler/siluet-govde.fbx")
    arm = [o for o in yeni if o.type == "ARMATURE"][0]
    log("govde kemik ornek:", [b.name for b in arm.data.bones][:3], "olcek", tuple(round(x, 4) for x in arm.scale))
    mesler = [o for o in yeni if o.type == "MESH"]
    klipler = fbx_al(klip)
    karm = [o for o in klipler if o.type == "ARMATURE"][0]
    log("klip kemik ornek:", [b.name for b in karm.data.bones][:3])
    act = karm.animation_data.action
    arm.animation_data_create(); arm.animation_data.action = act
    for o in klipler:
        bpy.data.objects.remove(o, do_unlink=True)
    bas, son = int(act.frame_range[0]), int(act.frame_range[1])
    kr = int(kip) if str(kip).isdigit() else kare_sec(arm, kip, bas, son)
    bpy.context.scene.frame_set(kr)
    log("klip", klip, "kare", kr, "/", bas, son)
    for m in mesler:
        m.data.materials.clear()
        m.data.materials.append(siyah)
        kabuk_ekle(m, KABUK_KARAKTER, kabuk_b)          # mesh yerel birimi (Mixamo: cm)
    return arm, mesler, kr


def dunya_kutusu(objs):
    xs, ys, zs = [], [], []
    dg = bpy.context.evaluated_depsgraph_get()
    for o in objs:
        oe = o.evaluated_get(dg)
        me = oe.to_mesh()
        for v in me.vertices:
            p = oe.matrix_world @ v.co
            xs.append(p.x); ys.append(p.y); zs.append(p.z)
        oe.to_mesh_clear()
    return Vector((min(xs), min(ys), min(zs))), Vector((max(xs), max(ys), max(zs)))


# ------------------------------------------------------------------ yazi
def yazi_nesnesi(metin, font, boy, derinlik, egim):
    bpy.ops.object.text_add()
    t = bpy.context.active_object
    t.data.body = metin; t.data.font = font; t.data.size = boy
    t.data.extrude = derinlik; t.data.bevel_depth = egim; t.data.bevel_resolution = 3
    t.data.align_x = "CENTER"; t.data.align_y = "CENTER"
    bpy.ops.object.convert(target="MESH")
    return bpy.context.active_object


def harflere_bol(obj):
    bpy.ops.object.select_all(action="DESELECT"); obj.select_set(True); bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.separate(type="LOOSE"); bpy.ops.object.mode_set(mode="OBJECT")
    parcalar = [o for o in bpy.context.selected_objects]
    for p in parcalar:
        bpy.context.view_layer.objects.active = p
        bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
    # ayni harfin ic bosluk parcasi ayri ada olmaz (yuz baglidir); x'e gore sirala
    return sorted(parcalar, key=lambda o: o.location.x)


def parlak_baslik(kam, metin, font, renkler, yerel, boy, kabuk_b, kabuk_d, zipla=0.06):
    obj = yazi_nesnesi(metin, font, boy, derinlik=0.16 * boy, egim=0.03 * boy)
    harfler = harflere_bol(obj)
    for i, h in enumerate(harfler):
        r = lin(renkler[i % len(renkler)])
        h.data.materials.clear(); h.data.materials.append(mat_parlak("harf%d" % i, r, purluk=0.18, coat=1.0, emis=0.35))
        kabuk_ekle(h, 0.045 * boy, kabuk_b)
        kabuk_ekle(h, 0.11 * boy, kabuk_d)
        h.rotation_euler.z = math.radians(4 * (1 if i % 2 == 0 else -1))   # yazi duzleminde egilme
        h.location.y += zipla * boy * math.sin(i * 1.9)                     # yukari-asagi ziplama
    # kameraya bagla
    bpy.ops.object.select_all(action="DESELECT")
    for h in harfler:
        h.select_set(True)
    bpy.ops.object.empty_add(location=(0, 0, 0)); bos = bpy.context.active_object
    for h in harfler:
        h.parent = bos
    bos.parent = kam                                  # kamera yerelinde: yazi XY duzleminde, +Z kameraya bakar
    bos.location = yerel
    bos.rotation_euler = (0, 0, 0)
    return bos


def render_et(ad):
    sc = bpy.context.scene
    sc.use_nodes = True
    nt = sc.node_tree; nt.nodes.clear()
    rl = nt.nodes.new("CompositorNodeRLayers")
    gl = nt.nodes.new("CompositorNodeGlare"); gl.glare_type = "FOG_GLOW"; gl.threshold = 0.9; gl.size = 8; gl.mix = 0.15
    out = nt.nodes.new("CompositorNodeComposite")
    nt.links.new(rl.outputs[0], gl.inputs[0]); nt.links.new(gl.outputs[0], out.inputs[0])
    sc.render.filepath = os.path.join(CIKTI, ad + ".png")
    bpy.ops.render.render(write_still=True)
    log("yazildi", sc.render.filepath)


# ------------------------------------------------------------------ ana akis
for v in AYAR["varyant"]:
    sc = sahne_kur()
    kenar = lin(hex3(AYAR.get("kenar", "#22d3ee"))); ok = lin(hex3(AYAR.get("ok", "#f472b6"))); iki = lin(hex3(AYAR.get("iki", "#ff4fa3")))
    zemin_ve_yol(kenar, ok, iki)
    sehir()
    paneller([tuple(c) for c in AYAR["panel_renk"]])
    gok_ve_kemerler([hex3(h) for h in ("#ff4fa3", "#22d3ee", "#a855f7", "#38bdf8")])

    # Referansta siluet DUZ simsiyah (isik/golge yok) + duz beyaz kontur; 3B model yalniz SEKIL kaynagi
    # (kullanici 17 Eki: "normal siyah siluet olarak alman gerekiyor ... 3D yapman gerekmiyor").
    siyah = mat_emisyon("siluet", (0, 0, 0), 0.0)
    kab_b = mat_kabuk("kabuk_beyaz", (1, 1, 1), 1.6)
    kab_d = mat_kabuk("kabuk_koyu", lin((0.11, 0.03, 0.27)), 1.0)

    figurler = []
    for s_ in (-1, 1):
        arm, mesler, kr = karakter(v["klip"], v.get("kare", "el_tepe"), siyah, kab_b, kab_d)
        figurler.append((arm, mesler))
    # boyut/konum: govde boyu ~1.85 m; yuze donuk (Mixamo -> Blender: +Y ileri ise 180 cevir)
    for idx, (arm, mesler) in enumerate(figurler):
        s_ = -1 if idx == 0 else 1
        dg = bpy.context.evaluated_depsgraph_get()
        alt, ust = dunya_kutusu(mesler)
        boy = ust.z - alt.z
        olcek = 1.85 / max(boy, 1e-6)
        arm.scale = arm.scale * olcek
        bpy.context.view_layer.update()
        # ileri yon: ayak bilegi -> parmak
        pb = arm.pose.bones
        try:
            ileri = (arm.matrix_world @ pb["mixamorig:LeftToeBase"].head) - (arm.matrix_world @ pb["mixamorig:LeftFoot"].head)
        except KeyError:
            ileri = Vector((0, -1, 0))
        ileri.z = 0
        aci = math.atan2(ileri.x, -ileri.y) if ileri.length > 1e-6 else 0
        arm.rotation_euler.z -= aci                       # yuz -Y'ye (kameraya)
        arm.rotation_euler.z += math.radians(14) * (-s_)  # birbirine hafif donuk
        bpy.context.view_layer.update()
        alt, ust = dunya_kutusu(mesler)
        merkez = (alt + ust) / 2
        arm.location.x += s_ * 1.05 - merkez.x
        arm.location.y += 1.2 - merkez.y
        arm.location.z += -alt.z
        bpy.context.view_layer.update()
        log("figur", idx, "boy", round(boy * olcek, 2), "aci", round(math.degrees(aci), 1))

    # kontra isiklar
    for s_, r in ((-1, lin(hex3("#ff4fa3"))), (1, lin(hex3("#38bdf8")))):
        bpy.ops.object.light_add(type="AREA", location=(s_ * 3, 4.5, 3.0))
        L = bpy.context.active_object; L.data.energy = 900; L.data.color = r; L.data.size = 3
        L.rotation_euler = (math.radians(-70), 0, math.radians(180 + s_ * 30))
    bpy.ops.object.light_add(type="AREA", location=(0, -4, 6)); on = bpy.context.active_object
    on.data.energy = 250; on.data.size = 6; on.rotation_euler = (math.radians(35), 0, 0)

    # kamera: alcak, hafif yukari, genis aci (figurler dev, panel uzakta)
    bpy.ops.object.camera_add(location=(0, -1.9, 0.62), rotation=(math.radians(95), 0, 0))
    kam = bpy.context.active_object; kam.data.lens = 20; sc.camera = kam
    if not AYAR.get("yazi_3d", False):
        render_et("KAPAK-3D-" + v["ad"])
        continue
    font = bpy.data.fonts.load(os.path.join(KOK, AYAR["font"]))
    renk = [hex3(h) for h in AYAR["harf_renk"]]
    D = 1.8; f = D / 4.2                                # yazilar figurlerin ONUNDE (kameraya 1,8 m)
    parlak_baslik(kam, AYAR["baslik"], font, renk, (0, 1.32 * f, -D), 0.62 * f, kab_b, kab_d)
    sol, sag = v.get("sol", []), v.get("sag", [])
    for i, m in enumerate(sol):
        parlak_baslik(kam, m, font, [hex3(["#38bdf8", "#ff4fa3"][i % 2])], (-2.25 * f, (0.55 - i * 0.36) * f, -D), 0.27 * f, kab_b, kab_d, zipla=0.03)
    for i, m in enumerate(sag):
        parlak_baslik(kam, m, font, [hex3(["#facc15", "#4ade80"][i % 2])], (2.25 * f, (0.55 - i * 0.36) * f, -D), 0.27 * f, kab_b, kab_d, zipla=0.03)

    render_et("KAPAK-3D-" + v["ad"])
