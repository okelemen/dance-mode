"""HUMAN TETRIS 32. video (REF-084 yapi, 3 PLAYER BATTLE) - GUNDUZ NOEL OYUNCAK ATOLYESI, CILALI 3D OYUN GORUNUMU.
varlik.py calistirir (--mod atolye).

Mekan kullanici karari (19 Kas 2026): Noel oyuncak atolyesi, gunduz, ic mekan, KAR YOK (27 karli dag / 31 buzul tekrari olmasin);
OUT ani: karakter kapinin yanindaki dev hediye kutusu yiginina duser (kutular sacilir).
Icerik: gun isigi alan buyuk kemerli pencereler, ortada isikli dev Noel cami, raflarda oyuncak tren / tahta asker / ayicik / renkli
bloklar, tavana kadar dev hediye kutusu yiginlari, seker cubugu direkler, tavanda kirmizi kirisler + cam dali girlandlari + renkli
ampuller, tavandan sarkan altin yildizlar ve yilbasi toplari (ekran dolu kurali md. 7: "gok" = tavan, dolu).
§4 CILALI 3D OYUN GORUNUMU: doygun renk, tombul hatlar, cilali (coat) yuzey, gercek isik-golge (Cycles); foto dokusu yok,
isiksiz duz renk yok (ampul / pencere / LED tabela haric). §8 SOLUK YASAK: REF-084 kapagi doygunluk 0,627 / renklilik 0,565 ->
buyuk beyaz yuzey yok, duvar doygun kirmizi / yesil, zemin sicak cilali ahsap, kurdeleler altin.
Pist: uc oyuncak konveyor bandi (P1 mavi sol / P2 pembe orta / P3 yesil sag), kenarda altin silindir makaralar, sari yon oklari.
Kapi: oyuncu renginde ust uste hediye kutularindan direkler + kiris, altin kurdele, tepede dev fiyonk, ampul dizisi, LED tabela.

Katmanlar buzul (31) ile ayni mantik, 3 serit (balonpist 20 gibi 640 px): gok.png = butun atolye (1920),
serit-p1..p3.png = oyuncunun yakin konveyoru + kapi + yanindaki hediye yigini; isik ayni olsun diye butun oda serit katmaninda da
kurulur, oda holdout. Telif: genel Noel/oyuncak ogeleri; bilinen karakter, marka, logo, yazi yok.

Ciktilar: gok.png, serit-p1..p3.png (640x1080), panel-p1..p3.png, yerlesim.json;
kapak modu (--yalniz kapak): kapak-gok.png, kapak-serit-p1..p3.png
"""

import random
YERLESIM.clear()
KAPAK = YALNIZ == "kapak"
POZLAMA = float(arg("--pozlama", arg("--kapak-pozlama", "0")))
GUNES = float(arg("--gunes", "4.2"))
ON_EK = "kapak-" if KAPAK else ""
SERIT_W = 640
KAP = {"y": 8.0, "w": 2.7, "h": 3.5, "kalin": 0.5}
KAM = {"z": 2.2, "egim": 5.0, "lens": 18.0, "sensor": 24.0}
if KAPAK:
    KAM.update({"z": float(arg("--kapak-z", "2.0")), "egim": float(arg("--kapak-egim", "4.0")), "lens": float(arg("--kapak-lens", "15.0"))})
GECIS = 11.0            # serit konveyoru burada biter, otesi gok.png
ARKA_Y = 38.0           # arka duvar (pencereler + cam)
YAN_X = 22.0            # yan duvarlar (raflar)
TAVAN = 12.0
SERIT = {
    "p1": {"ana": "#1e7cff", "koyu": "#0a3fa8", "acik": "#8cc8ff", "iki": "#00b4ff"},
    "p2": {"ana": "#ff2aa0", "koyu": "#a8105e", "acik": "#ffa6d6", "iki": "#c020ff"},
    "p3": {"ana": "#18c840", "koyu": "#0a6a22", "acik": "#9cf0a8", "iki": "#00d890"},
}
HEDIYE = ("#e8102c", "#14a83a", "#ffc21a", "#8a2ae8", "#1e7cff", "#ff2aa0", "#ff6a10", "#00b8d8")
KURDELE = ("#ffd21e", "#ffd21e", "#e8102c", "#ffd21e", "#ff2aa0", "#ffd21e", "#14a83a", "#ffd21e")


# ------------------------------------------------------------------ sahne / isik
def atolye_sahnesi(w, h, saydam):
    sc = bos_sahne(w=w, h=h, saydam=saydam, ornek=ORNEK, doygun=True)
    sc.view_settings.view_transform = "Standard"           # 25 notu: AgX doygun renkleri pastele ceker
    sc.view_settings.exposure = POZLAMA
    sc.cycles.max_bounces = 6; sc.cycles.diffuse_bounces = 3; sc.cycles.glossy_bounces = 3
    sc.cycles.transmission_bounces = 2; sc.cycles.transparent_max_bounces = 8
    sc.cycles.use_light_tree = True
    bg = sc.world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (*lin(hex3("#ffd8a0")), 1); bg.inputs[1].default_value = 0.35   # sicak dolgu isigi
    sc.use_nodes = True; sc.render.use_compositing = True; ct = sc.node_tree; ct.nodes.clear()
    rl = ct.nodes.new("CompositorNodeRLayers"); gl = ct.nodes.new("CompositorNodeGlare"); co = ct.nodes.new("CompositorNodeComposite")
    gl.glare_type = "FOG_GLOW"; gl.quality = "HIGH"; gl.threshold = 1.3; gl.size = 7; gl.mix = 0.0
    ct.links.new(rl.outputs["Image"], gl.inputs[0]); ct.links.new(gl.outputs[0], co.inputs[0])
    if saydam:
        ct.links.new(rl.outputs["Alpha"], co.inputs[1])
    return sc


def kamera(sc, x=0.0):
    rx = math.radians(90 - KAM["egim"])
    bpy.ops.object.camera_add(location=(x, 0, KAM["z"]), rotation=(rx, 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.sensor_fit = "VERTICAL"; kam.data.sensor_height = KAM["sensor"]; kam.data.lens = KAM["lens"]
    kam.data.clip_end = 600
    return kam


def isiklar():
    """gunes pencerelerden iceri (duvar/tavan golge atmaz), tavanda sicak alan isiklari"""
    bpy.ops.object.light_add(type="SUN", location=(0, 0, 30))
    g = bpy.context.active_object; g.data.energy = GUNES; g.data.angle = math.radians(2.0)
    g.data.color = lin(hex3("#fff0d0"))
    g.rotation_euler = Vector((-0.35, 0.6, -0.72)).to_track_quat("-Z", "Y").to_euler()
    for (x, y) in ((-8, 6), (8, 6), (-10, 20), (10, 20), (0, 30)):
        isik("AREA", (x, y, TAVAN - 1.0), 900, lin(hex3("#ffe2b0")), 6, yon=(x, y, 0))


# ------------------------------------------------------------------ malzemeler
def mat_pbr(ad, renk, purluk, metal=0.0, kaplama=0.0, bump=None):
    m = bpy.data.materials.new(ad); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*lin(hex3(renk)), 1)
    b.inputs["Roughness"].default_value = purluk; b.inputs["Metallic"].default_value = metal
    b.inputs["Coat Weight"].default_value = kaplama; b.inputs["Coat Roughness"].default_value = 0.06
    if bump:
        nt = m.node_tree
        ns = nt.nodes.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value = bump[0]; ns.inputs["Detail"].default_value = 6
        bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = bump[1]; bp.inputs["Distance"].default_value = 0.02
        nt.links.new(ns.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    return m


def mat_tahta(ad, renk1, renk2, ara="#5a1a08", olcek=0.6, satir=0.12, gen=1.6):
    """cilali parke / tahta: tugla dokusuyla uzun tahtalar, iki sicak ton + koyu derz, hafif damar bump"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.inputs["Scale"].default_value = olcek; br.inputs["Mortar Size"].default_value = 0.01
    br.inputs["Brick Width"].default_value = gen; br.inputs["Row Height"].default_value = satir
    br.inputs["Color1"].default_value = (*lin(hex3(renk1)), 1); br.inputs["Color2"].default_value = (*lin(hex3(renk2)), 1)
    br.inputs["Mortar"].default_value = (*lin(hex3(ara)), 1)
    br.offset = 0.5; br.squash = 1.0
    nt.links.new(geo.outputs["Position"], br.inputs["Vector"])
    nt.links.new(br.outputs["Color"], b.inputs["Base Color"])
    ns = nt.nodes.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value = 30; ns.inputs["Detail"].default_value = 3
    nt.links.new(geo.outputs["Position"], ns.inputs["Vector"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.08; bp.inputs["Distance"].default_value = 0.01
    nt.links.new(ns.outputs["Fac"], bp.inputs["Height"])
    bp2 = nt.nodes.new("ShaderNodeBump"); bp2.inputs["Strength"].default_value = 0.4; bp2.inputs["Distance"].default_value = 0.02
    nt.links.new(br.outputs["Fac"], bp2.inputs["Height"]); nt.links.new(bp.outputs["Normal"], bp2.inputs["Normal"])
    nt.links.new(bp2.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = 0.35; b.inputs["Coat Weight"].default_value = 0.3; b.inputs["Coat Roughness"].default_value = 0.1
    b.inputs["Specular IOR Level"].default_value = 0.2
    return m


def mat_pencere(ad):
    """pencereden gorunen gunduz gogu: alttan acik camgobegi -> ustte doygun mavi (kendi isigi; emission serbest)"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord"); sp = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Generated"], sp.inputs[0])
    rp = nt.nodes.new("ShaderNodeValToRGB"); el = rp.color_ramp.elements
    el[0].position = 0.0; el[0].color = (*lin(hex3("#18c8ff")), 1)
    el[1].position = 1.0; el[1].color = (*lin(hex3("#0a50ff")), 1)
    nt.links.new(sp.outputs["Z"], rp.inputs[0])
    e = nt.nodes.new("ShaderNodeEmission"); e.inputs[1].default_value = 1.6
    nt.links.new(rp.outputs[0], e.inputs[0])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(e.outputs[0], o.inputs[0])
    return m


def duz(ad, x0, x1, y0, y1, z, mat):
    me = bpy.data.meshes.new(ad)
    me.from_pydata([(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new(ad, me); bpy.context.collection.objects.link(o); o.data.materials.append(mat)
    return o


def dik(ad, x0, x1, y, z0, z1, mat):
    me = bpy.data.meshes.new(ad)
    me.from_pydata([(x0, y, z0), (x1, y, z0), (x1, y, z1), (x0, y, z1)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new(ad, me); bpy.context.collection.objects.link(o); o.data.materials.append(mat)
    return o


def yan_dik(ad, x, y0, y1, z0, z1, mat):
    me = bpy.data.meshes.new(ad)
    me.from_pydata([(x, y0, z0), (x, y1, z0), (x, y1, z1), (x, y0, z1)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new(ad, me); bpy.context.collection.objects.link(o); o.data.materials.append(mat)
    return o


_MAT = {}


def M(ad, f):
    if ad not in _MAT:
        _MAT[ad] = f()
    return _MAT[ad]


def P(renk, purluk=0.3, kaplama=0.7, metal=0.0):
    """tekrar kullanilan cilali oyuncak plastik / boya"""
    return M("p%s_%s_%s" % (renk, purluk, metal), lambda: mat_pbr("p" + renk, renk, purluk, metal=metal, kaplama=kaplama))


def golgesiz(o):
    """duvar/tavan gunes golgesi atmaz (ic mekan gun isigi pencereden geliyor gibi)"""
    o.visible_shadow = False
    return o


# ------------------------------------------------------------------ oyuncaklar / Noel ogeleri
def hediye(konum, boyut, renk, kurdele, rnd, fiyonk=True):
    """cilali ambalajli tombul hediye kutusu: iki capraz kurdele bandi + ustte iki halkali fiyonk"""
    x, y, z = konum; bx, by, bz = boyut
    yuvarlak_kutu("hediye", (x, y, z + bz / 2), boyut, P(renk, 0.28, 0.8), egim=min(bx, by, bz) * 0.12, seg=3)
    km = P(kurdele, 0.25, 0.8, metal=0.35 if kurdele == "#ffd21e" else 0.0)
    yuvarlak_kutu("kurdele", (x, y, z + bz / 2), (bx * 0.16, by + 0.04, bz + 0.04), km, egim=0.01, seg=1)
    yuvarlak_kutu("kurdele", (x, y, z + bz / 2), (bx + 0.04, by * 0.16, bz + 0.04), km, egim=0.01, seg=1)
    if fiyonk:
        r = min(bx, by) * 0.22
        for s in (-1, 1):
            bpy.ops.mesh.primitive_torus_add(major_radius=r, minor_radius=r * 0.32, location=(x + s * r * 0.9, y, z + bz + r * 0.55),
                                             rotation=(math.pi / 2, s * 0.5, 0))
            o = bpy.context.active_object; o.data.materials.append(km); bpy.ops.object.shade_smooth()
        kure((x, y, z + bz + r * 0.3), r * 0.4, km, sub=2)


def hediye_yigini(merkez, gen, yuk, rnd, kat=5):
    """piramit gibi ust uste dev hediye kutulari (OUT yigini ve arka plan dolgusu)"""
    x0, y0 = merkez
    z = 0.0
    for k in range(kat):
        w = gen * (1 - 0.17 * k)
        n = max(1, int(w / (yuk * 0.9)))
        for i in range(n):
            b = rnd.uniform(0.75, 1.0) * w / n
            h = yuk * rnd.uniform(0.7, 1.05)
            j = rnd.randrange(len(HEDIYE))
            hediye((x0 - w / 2 + (i + 0.5) * w / n + rnd.uniform(-0.1, 0.1) * b, y0 + rnd.uniform(-0.3, 0.3) * yuk, z),
                   (b * 0.92, b * rnd.uniform(0.7, 0.95), h), HEDIYE[j], KURDELE[j], rnd, fiyonk=(k == kat - 1 or rnd.random() < 0.3))
        z += yuk * 0.82
        if w < yuk:
            break


def ayicik(konum, olcek, renk):
    x, y, z = konum; m = P(renk, 0.6, 0.15)
    g = kure((x, y, z + 0.5 * olcek), 0.45 * olcek, m); g.scale = (1.0, 0.85, 1.1)
    kure((x, y - 0.05 * olcek, z + 1.12 * olcek), 0.33 * olcek, m)
    for s in (-1, 1):
        kure((x + s * 0.24 * olcek, y, z + 1.38 * olcek), 0.12 * olcek, m)
        k = kure((x + s * 0.45 * olcek, y - 0.1 * olcek, z + 0.6 * olcek), 0.16 * olcek, m); k.scale = (1.0, 1.0, 1.6)
        a = kure((x + s * 0.22 * olcek, y - 0.25 * olcek, z + 0.12 * olcek), 0.17 * olcek, m); a.scale = (1.0, 1.4, 0.8)
    kure((x, y - 0.32 * olcek, z + 1.06 * olcek), 0.13 * olcek, P("#ffd8a0", 0.5, 0.2))
    yuvarlak_kutu("papyon", (x, y - 0.32 * olcek, z + 0.86 * olcek), (0.36 * olcek, 0.08 * olcek, 0.14 * olcek), P("#e8102c"), egim=0.03, seg=2)


def asker(konum, olcek, ceket):
    """tahta oyuncak asker: kirmizi/mavi ceket, siyah sapka, altin dugmeler"""
    x, y, z = konum
    yuvarlak_kutu("asker_bacak", (x, y, z + 0.35 * olcek), (0.32 * olcek, 0.22 * olcek, 0.7 * olcek), P("#1a2a8a"), egim=0.04 * olcek, seg=2)
    yuvarlak_kutu("asker_ceket", (x, y, z + 0.95 * olcek), (0.42 * olcek, 0.28 * olcek, 0.6 * olcek), P(ceket), egim=0.06 * olcek, seg=2)
    kure((x, y, z + 1.42 * olcek), 0.19 * olcek, P("#ffc8a0", 0.45, 0.4))
    bpy.ops.mesh.primitive_cylinder_add(radius=0.17 * olcek, depth=0.42 * olcek, location=(x, y, z + 1.74 * olcek), vertices=20)
    bpy.context.active_object.data.materials.append(P("#141820", 0.3)); bpy.ops.object.shade_smooth()
    for k in range(3):
        kure((x, y - 0.15 * olcek, z + (0.8 + 0.14 * k) * olcek), 0.035 * olcek, P("#ffd21e", 0.2, 0.8, metal=0.8), sub=1)


def tren(konum, olcek, renk):
    x, y, z = konum
    yuvarlak_kutu("tren_kabin", (x - 0.4 * olcek, y, z + 0.6 * olcek), (0.6 * olcek, 0.6 * olcek, 0.7 * olcek), P(renk), egim=0.06 * olcek, seg=2)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.3 * olcek, depth=0.9 * olcek, location=(x + 0.3 * olcek, y, z + 0.5 * olcek), rotation=(0, math.pi / 2, 0), vertices=24)
    bpy.context.active_object.data.materials.append(P("#14a83a")); bpy.ops.object.shade_smooth()
    boru((x + 0.5 * olcek, y, z + 0.75 * olcek), (x + 0.5 * olcek, y, z + 1.1 * olcek), 0.09 * olcek, P("#141820"))
    yuvarlak_kutu("tren_cati", (x - 0.4 * olcek, y, z + 0.98 * olcek), (0.75 * olcek, 0.72 * olcek, 0.08 * olcek), P("#ffd21e"), egim=0.03, seg=1)
    for dx in (-0.5, -0.1, 0.35, 0.65):
        for s in (-1, 1):
            bpy.ops.mesh.primitive_cylinder_add(radius=0.15 * olcek, depth=0.08 * olcek, location=(x + dx * olcek, y + s * 0.32 * olcek, z + 0.15 * olcek), rotation=(math.pi / 2, 0, 0), vertices=20)
            bpy.context.active_object.data.materials.append(P("#e8102c")); bpy.ops.object.shade_smooth()


def bloklar(konum, olcek, rnd):
    x, y, z = konum
    for k in range(4):
        for i in range(3 - k // 2):
            yuvarlak_kutu("blok", (x + (i - 1) * 0.42 * olcek + k * 0.1, y, z + 0.2 * olcek + k * 0.4 * olcek), (0.38 * olcek,) * 3,
                          P(rnd.choice(HEDIYE)), egim=0.04 * olcek, seg=2)
        if k >= 2:
            break


def top_(konum, r, renk):
    kure(konum, r, P(renk, 0.2, 0.9))


def seker_cubugu(taban, boy, rnd):
    """kirmizi-beyaz (beyaz yerine acik pembe: soluk olmasin) halkali seker cubugu direk + tepede kanca"""
    x, y, z = taban
    n = 10; r = boy * 0.06
    for i in range(n):
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=boy / n, location=(x, y, z + boy * (i + 0.5) / n), vertices=20)
        bpy.context.active_object.data.materials.append(P("#e8102c" if i % 2 == 0 else "#ffd0dc", 0.2, 0.9)); bpy.ops.object.shade_smooth()
    bpy.ops.mesh.primitive_torus_add(major_radius=boy * 0.14, minor_radius=r, location=(x + boy * 0.14, y, z + boy), rotation=(math.pi / 2, 0, 0))
    o = bpy.context.active_object; o.data.materials.append(P("#e8102c", 0.2, 0.9)); bpy.ops.object.shade_smooth()
    # kancanin yarisi: alt yariyi kirp (boolean yerine olcek): ustte yarim halka gibi gorunsun diye hafif one dondur
    o.scale = (1.0, 1.0, 1.0)


def yildiz_mesh(ad, merkez, r, mat, kal=0.15, don=0.0):
    x, y, z = merkez
    nok = []
    for k in range(10):
        a = math.pi / 2 + k * math.pi / 5 + don
        rr = r if k % 2 == 0 else r * 0.45
        nok.append((x + rr * math.cos(a), y, z + rr * math.sin(a)))
    me = bpy.data.meshes.new(ad); me.from_pydata(nok, [], [list(range(10))]); me.update()
    o = bpy.data.objects.new(ad, me); bpy.context.collection.objects.link(o); o.data.materials.append(mat)
    so = o.modifiers.new("k", "SOLIDIFY"); so.thickness = kal; so.offset = 0
    bv = o.modifiers.new("b", "BEVEL"); bv.width = kal * 0.3; bv.segments = 2; bv.limit_method = "NONE"
    return o


def noel_cami(taban, boy, rnd):
    """dev Noel cami: ust uste yesil koniler, renkli cilali toplar, yanan ampuller (emission), tepede altin yildiz"""
    x, y, z = taban
    bpy.ops.mesh.primitive_cylinder_add(radius=boy * 0.05, depth=boy * 0.1, location=(x, y, z + boy * 0.05), vertices=16)
    bpy.context.active_object.data.materials.append(P("#7a3a10", 0.6, 0.1))
    yaprak = M("cam_yaprak", lambda: mat_pbr("cam_yaprak", "#0a9a30", 0.5, kaplama=0.3, bump=(8, 0.35)))
    kat = [(0.08, 0.40, 0.36), (0.32, 0.33, 0.30), (0.54, 0.25, 0.25), (0.73, 0.17, 0.2)]
    for (z0, r, h) in kat:
        bpy.ops.mesh.primitive_cone_add(radius1=boy * r, radius2=boy * r * 0.15, depth=boy * h, location=(x, y, z + boy * (z0 + h / 2)), vertices=40)
        bpy.context.active_object.data.materials.append(yaprak); bpy.ops.object.shade_smooth()
    amp = [M("amp" + c, lambda c_=c: mat_emis("amp" + c_, lin(hex3(c_)), 6.0)) for c in ("#ffd21e", "#ff2a5a", "#2a8aff", "#30e060")]
    for (z0, r, h) in kat:
        for k in range(16):
            a = k * math.tau / 16 + rnd.uniform(-0.15, 0.15) - math.pi / 2
            t = rnd.uniform(0.2, 0.8); rr = boy * r * (1 - 0.85 * t); zz = z + boy * (z0 + h * t)
            if math.sin(a) > 0.3:            # arkada kalanlar gorunmez
                continue
            if k % 2 == 0:
                kure((x + rr * math.cos(a), y + rr * math.sin(a), zz), boy * 0.03, P(rnd.choice(HEDIYE), 0.15, 1.0), sub=2)
            else:
                kure((x + rr * math.cos(a), y + rr * math.sin(a), zz), boy * 0.012, rnd.choice(amp), sub=1)
    yildiz_mesh("cam_yildiz", (x, y - boy * 0.02, z + boy * 0.98), boy * 0.08, P("#ffd21e", 0.15, 0.9, metal=0.8), kal=boy * 0.02)


def girland(a, b, sarkma, rnd, n=22):
    """iki nokta arasinda sarkan cam dali girlandi (yesil yumak zinciri) + renkli yanan ampuller"""
    yes = M("girland", lambda: mat_pbr("girland", "#0a9a30", 0.55, kaplama=0.2, bump=(10, 0.4)))
    amp = [M("amp" + c, lambda c_=c: mat_emis("amp" + c_, lin(hex3(c_)), 6.0)) for c in ("#ffd21e", "#ff2a5a", "#2a8aff", "#30e060")]
    A, B = Vector(a), Vector(b)
    for k in range(n + 1):
        t = k / n
        p = A.lerp(B, t); p.z -= sarkma * 4 * t * (1 - t)
        kure(tuple(p), 0.32, yes, sub=2)
        if k % 2 == 1:
            kure((p.x, p.y - 0.25, p.z - 0.3), 0.1, amp[k // 2 % 4], sub=1)


def sarkan_sus(konum, ip, rnd, tur):
    x, y, z = konum
    boru((x, y, z + ip), (x, y, TAVAN), 0.015, P("#ffd21e", 0.3, 0.5, metal=0.6))
    if tur == "yildiz":
        yildiz_mesh("sus_yildiz", (x, y, z), rnd.uniform(0.5, 0.8), P("#ffd21e", 0.15, 0.9, metal=0.8), kal=0.12, don=rnd.uniform(-0.3, 0.3))
    else:
        kure((x, y, z), rnd.uniform(0.35, 0.55), P(rnd.choice(HEDIYE), 0.12, 1.0))
        bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.16, location=(x, y, z + 0.5), vertices=12)
        bpy.context.active_object.data.materials.append(P("#ffd21e", 0.2, 0.6, metal=0.8))


def raf_duvari(s, rnd):
    """yan duvar: yesil duvar + tahta raf katlari, raflar oyuncak dolu"""
    raf = M("raf", lambda: mat_tahta("raf", "#f0701a", "#e05a10", olcek=0.3, satir=0.3, gen=3.0))
    for z in (1.2, 3.4, 5.6, 7.8):
        yuvarlak_kutu("raf", (s * (YAN_X - 0.8), ARKA_Y / 2, z), (1.6, ARKA_Y, 0.18), raf, egim=0.04, seg=2)
        y = 2.0
        while y < ARKA_Y - 2:
            r_ = rnd.random(); xx = s * (YAN_X - 0.9)
            if r_ < 0.25:
                ayicik((xx, y, z + 0.09), rnd.uniform(0.9, 1.3), rnd.choice(("#c8641e", "#ff6a10", "#e8102c", "#8a2ae8")))
                y += 1.6
            elif r_ < 0.45:
                asker((xx, y, z + 0.09), 1.1, rnd.choice(("#e8102c", "#1e7cff")))
                y += 0.9
            elif r_ < 0.65:
                tren((xx, y, z + 0.09), 1.0, rnd.choice(("#e8102c", "#1e7cff", "#8a2ae8")))
                y += 2.0
            elif r_ < 0.85:
                bloklar((xx, y, z + 0.09), 1.0, rnd)
                y += 1.6
            else:
                j = rnd.randrange(len(HEDIYE))
                hediye((xx, y, z + 0.09), (1.1, 1.1, 1.0), HEDIYE[j], KURDELE[j], rnd)
                y += 1.6


# ------------------------------------------------------------------ ATOLYE (iki katmanda; serit sahnesinde oda holdout)
def atolye(serit_modu, rnd):
    _MAT.clear()
    zemin = mat_tahta("zemin", "#ff6a0a", "#f0500a", ara="#8a2004", olcek=0.35, satir=0.18, gen=2.4)
    duz("zemin_yakin", -YAN_X, YAN_X, -4, GECIS, 0, zemin)
    duz("zemin_uzak", -YAN_X, YAN_X, GECIS, ARKA_Y, 0, zemin)
    # duvarlar: arka doygun kirmizi, yanlar doygun yesil; altta tahta lambri; tavan koyu kirmizi + kirisler
    duvar_k = mat_pbr("duvar_k", "#d0102c", 0.6, kaplama=0.1, bump=(4, 0.1))
    duvar_y = mat_pbr("duvar_y", "#0a8a30", 0.6, kaplama=0.1, bump=(4, 0.1))
    golgesiz(dik("arka_duvar", -YAN_X, YAN_X, ARKA_Y, 0, TAVAN, duvar_k))
    for s in (-1, 1):
        golgesiz(yan_dik("yan_duvar", s * YAN_X, -4, ARKA_Y, 0, TAVAN, duvar_y))
    golgesiz(duz("tavan", -YAN_X, YAN_X, -4, ARKA_Y, TAVAN, mat_pbr("tavan", "#d0102c", 0.5, kaplama=0.1)))
    lam = M("lambri", lambda: mat_tahta("lambri", "#b04a12", "#9a3c0c", olcek=0.4, satir=0.5, gen=0.4))
    yuvarlak_kutu("lambri", (0, ARKA_Y - 0.15, 0.9), (2 * YAN_X, 0.3, 1.8), lam, egim=0.04, seg=2)
    kiris = M("kiris", lambda: mat_tahta("kiris", "#e8501a", "#d03c10", olcek=0.5, satir=0.4, gen=4.0))
    for y in range(2, int(ARKA_Y), 6):
        golgesiz(yuvarlak_kutu("kiris", (0, y, TAVAN - 0.35), (2 * YAN_X, 0.6, 0.7), kiris, egim=0.06, seg=2))
    # arka duvarda uc kemerli dev pencere (gunduz gogu), altin cerceve
    pen = mat_pencere("pencere"); cer = P("#ffc21a", 0.25, 0.6, metal=0.5)
    for x in (-13.0, 13.0, 0.0):
        w, h, z0 = 6.0, 7.0, 2.4
        dik("pencere", x - w / 2, x + w / 2, ARKA_Y - 0.05, z0, z0 + h, pen)
        bpy.ops.mesh.primitive_cylinder_add(radius=w / 2, depth=0.02, location=(x, ARKA_Y - 0.05, z0 + h), rotation=(math.pi / 2, 0, 0), vertices=48)
        bpy.context.active_object.data.materials.append(pen)
        for xx in (x - w / 2, x, x + w / 2):
            yuvarlak_kutu("cerceve", (xx, ARKA_Y - 0.2, z0 + h / 2), (0.3, 0.3, h), cer, egim=0.05, seg=2)
        for zz in (z0, z0 + h * 0.5, z0 + h):
            yuvarlak_kutu("cerceve", (x, ARKA_Y - 0.2, zz), (w + 0.3, 0.3, 0.3), cer, egim=0.05, seg=2)
        bpy.ops.mesh.primitive_torus_add(major_radius=w / 2, minor_radius=0.16, location=(x, ARKA_Y - 0.2, z0 + h), rotation=(math.pi / 2, 0, 0))
        bpy.context.active_object.data.materials.append(cer); bpy.ops.object.shade_smooth()
    # ortada dev Noel cami (orta pencerenin onunde), cevresinde hediye yiginlari
    noel_cami((0, ARKA_Y - 6, 0), 13.0, rnd)
    for (x, y, g, h) in ((-6, ARKA_Y - 4, 5, 1.4), (6, ARKA_Y - 4, 5, 1.4), (-17, 30, 7, 1.8), (17, 30, 7, 1.8),
                         (-11, 22, 4, 1.3), (11, 22, 4, 1.3), (-19, 16, 5, 1.6), (19, 16, 5, 1.6), (-8, 15, 3, 1.0), (8, 15, 3, 1.0)):
        hediye_yigini((x, y), g, h, rnd, kat=5)
    for s in (-1, 1):
        raf_duvari(s, rnd)
    # koridor boyunca seker cubugu direkler + aralarda girland
    for y in (13, 19, 25, 31):
        for s in (-1, 1):
            seker_cubugu((s * 5.2, y, 0), 3.4, rnd)
    for y in (13, 19, 25):
        for s in (-1, 1):
            girland((s * 5.2, y, 3.3), (s * 5.2, y + 6, 3.3), 0.8, rnd, n=12)
    # tavan: kirisler arasi capraz girlandlar + sarkan altin yildizlar ve yilbasi toplari (ekran dolu)
    for y in range(2, int(ARKA_Y) - 6, 6):
        girland((-YAN_X + 1, y, TAVAN - 0.8), (YAN_X - 1, y + 6, TAVAN - 0.8), 2.2, rnd, n=26)
        girland((YAN_X - 1, y, TAVAN - 0.8), (-YAN_X + 1, y + 6, TAVAN - 0.8), 2.2, rnd, n=26)
    for k in range(70):
        x = rnd.uniform(-YAN_X + 2, YAN_X - 2); y = rnd.uniform(5, ARKA_Y - 3)
        ip = rnd.uniform(1.0, 4.5)
        sarkan_sus((x, y, TAVAN - ip), ip - 0.2, rnd, "yildiz" if k % 3 == 0 else "top")
    # havada suzulen altin pirilti tanecikleri (yakinda)
    for k in range(40):
        kure((rnd.uniform(-10, 10), rnd.uniform(12, 30), rnd.uniform(1.5, 9.0)), rnd.uniform(0.05, 0.1), P("#ffd21e", 0.15, 0.9, metal=0.8), sub=1)
    if serit_modu:
        for o in bpy.data.objects:
            if o.type == "MESH" and o.name.split(".")[0] not in ("zemin_yakin",):
                o.is_holdout = True


# ------------------------------------------------------------------ SERIT: konveyor + kapi + OUT hediye yigini
def serit_esyalari(oyuncu, R, rnd):
    bant = M("bant" + oyuncu, lambda: mat_pbr("bant" + oyuncu, R["ana"], 0.45, kaplama=0.3, bump=(1.0, 0.0)))
    # konveyor govdesi (oyuncu renginde kenar) + bant (koyu oyuncu rengi, enine nervurlar)
    yuvarlak_kutu("konv_govde", (0, (GECIS - 4) / 2, 0.2), (2.7, GECIS + 4, 0.4), P(R["iki"], 0.25, 0.8), egim=0.08, seg=3)
    yuvarlak_kutu("konv_bant", (0, (GECIS - 4) / 2, 0.42), (2.2, GECIS + 4, 0.06), bant, egim=0.02, seg=1)
    y = -3.8
    while y < GECIS:
        yuvarlak_kutu("nervur", (0, y, 0.46), (2.15, 0.06, 0.03), P(R["iki"], 0.4, 0.2), egim=0.01, seg=1)
        y += 0.45
    for s in (-1, 1):                                                      # kenarda altin makaralar
        y = -3.6
        while y < KAP["y"] - 0.6:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.16, depth=0.26, location=(s * 1.42, y, 0.46), rotation=(0, math.pi / 2, 0), vertices=20)
            bpy.context.active_object.data.materials.append(P("#ffc21a", 0.2, 0.7, metal=0.7)); bpy.ops.object.shade_smooth()
            y += 0.7
    boya = P("#ffd21e", 0.3, 0.6)
    for y in (4.9, 6.4):                                                   # bantta sari yon oklari (seri sabiti)
        nok = [(-0.65, y - 0.4), (0, y), (0.65, y - 0.4), (0.65, y - 0.68), (0, y - 0.28), (-0.65, y - 0.68)]
        me = bpy.data.meshes.new("ok"); me.from_pydata([(a, b, 0.455) for a, b in nok], [], [list(range(6))]); me.update()
        o = bpy.data.objects.new("ok", me); bpy.context.collection.objects.link(o); o.data.materials.append(boya)
        o.modifiers.new("k", "SOLIDIFY").thickness = 0.02
    # OUT ani: kapinin iki yaninda dev hediye kutusu yigini (karakter buraya duser, kutular sacilir)
    for s in (-1, 1):
        hediye_yigini((s * 2.45, KAP["y"] + 0.4), 1.6, 0.75, random.Random({"p1": 5, "p2": 6, "p3": 7}[oyuncu] * 10 + s), kat=4)
    # bant onunde yerde birkac sacilmis kucuk hediye + top
    for s in (-1, 1):
        j = rnd.randrange(len(HEDIYE))
        hediye((s * 1.95, 2.4 + rnd.uniform(-0.3, 0.3), 0), (0.5, 0.5, 0.45), HEDIYE[j], KURDELE[j], rnd)
        top_((s * 1.9, 4.0, 0.22), 0.22, rnd.choice(HEDIYE))


def kapi(R):
    """hediye kutusu kapi: iki yanda oyuncu renginde ust uste dort kutu (altin kurdele), ustte uzun kutu kiris, tepede dev altin
    fiyonk, kirisin altinda ampul dizisi, ustte sonuk LED tabela (motor PLAYER n yazar)"""
    Y, W_, H_, K = KAP["y"], KAP["w"], KAP["h"], KAP["kalin"]
    ana, ak = R["ana"], R["acik"]
    xk = W_ / 2 + K / 2
    rnd = random.Random(7)
    for s in (-1, 1):
        z = 0.0
        for i in range(4):
            h = (H_ + K) / 4
            hediye((s * xk, Y, z), (K + 0.06 * (i % 2), K + 0.06 * (i % 2), h - 0.03), ana if i % 2 == 0 else R["iki"], "#ffd21e", rnd, fiyonk=False)
            z += h
    hediye((0, Y, H_), (W_ + 2 * K + 0.2, K, K), ana, "#ffd21e", rnd, fiyonk=False)
    km = P("#ffd21e", 0.2, 0.9, metal=0.6)
    for s in (-1, 1):                                                      # dev fiyonk
        bpy.ops.mesh.primitive_torus_add(major_radius=0.42, minor_radius=0.13, location=(s * 0.38, Y - 0.05, H_ + K + 0.35), rotation=(math.pi / 2, s * 0.45, 0))
        bpy.context.active_object.data.materials.append(km); bpy.ops.object.shade_smooth()
        k = kure((s * 0.25, Y - 0.1, H_ + K - 0.15), 0.1, km, sub=2); k.scale = (1.0, 0.5, 3.0); k.rotation_euler = (0, s * 0.4, 0)
    kure((0, Y - 0.1, H_ + K + 0.3), 0.16, km, sub=2)
    ampul = [M("amp" + c, lambda c_=c: mat_emis("amp" + c_, lin(hex3(c_)), 6.0)) for c in ("#ffd21e", "#ff2a5a", "#2a8aff", "#30e060")]
    for i in range(9):
        xx = -W_ / 2 + W_ * i / 8
        kure((xx, Y - K / 2 - 0.1, H_ - 0.3 - 0.12 * math.sin(math.pi * i / 8)), 0.07, ampul[i % 4], sub=2)
    yuvarlak_kutu("tabela", (0, Y - 0.3, H_ + K + 1.15), (W_ * 0.85, 0.2, 0.62), mat_pbr("tabela", "#15171a", 0.35, metal=0.4), egim=0.05, seg=3)
    me = bpy.data.meshes.new("led_yuz"); a, b = W_ * 0.4, 0.24; z0 = H_ + K + 1.15
    me.from_pydata([(-a, Y - 0.41, z0 - b), (a, Y - 0.41, z0 - b), (a, Y - 0.41, z0 + b), (-a, Y - 0.41, z0 + b)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("led_yuz", me); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat_emis("led_yuz", lin(hex3(R["koyu"])), 1.2))


def mat_parlama_kis():
    """buyuk yuzeylerde beyaz yansima doygunlugu yiyor (30/31 dersi) -> zemin/duvar/tavan specular dusuk"""
    for m in bpy.data.materials:
        if not m.use_nodes or "Principled BSDF" not in m.node_tree.nodes:
            continue
        ad = m.name.split(".")[0]
        if ad.startswith(("zemin", "duvar", "tavan", "lambri", "kiris", "bant")):
            b = m.node_tree.nodes["Principled BSDF"]
            b.inputs["Specular IOR Level"].default_value = 0.08
            b.inputs["Coat Weight"].default_value = 0.0


def serit_katmani(oyuncu):
    R = SERIT[oyuncu]
    sc = atolye_sahnesi(SERIT_W, 1080, True)
    kam = kamera(sc)
    rnd = random.Random({"p1": 31, "p2": 32, "p3": 33}[oyuncu])
    isiklar()
    atolye(True, random.Random(32))
    serit_esyalari(oyuncu, R, rnd)
    kapi(R)
    Y, W_, H_ = KAP["y"], KAP["w"], KAP["h"]
    ic = W_ / 2
    bpy.context.view_layer.update()
    px = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-ic, Y, 0), (ic, Y, 0), (-ic, Y, H_), (ic, Y, H_))]
    xs = [p.x * SERIT_W for p in px]; ys = [(1 - p.y) * 1080 for p in px]
    YERLESIM["aciklik_" + oyuncu] = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
    # OUT ani: hediye yigininin ekrandaki yeri; motor anahtar duzeni (minder = yigin)
    mk = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-2.45, Y + 0.4, 0.8), (2.45, Y + 0.4, 0.8), (0, GECIS, 0))]
    d = {"minder_sol_x": round(mk[0].x * SERIT_W, 1), "minder_sag_x": round(mk[1].x * SERIT_W, 1),
         "minder_y": round((1 - mk[0].y) * 1080, 1), "gecis_y": round((1 - mk[2].y) * 1080, 1)}
    YERLESIM[ON_EK + "atolye_" + oyuncu] = d
    YERLESIM[ON_EK + "yol"] = {"y_kapi": Y, "kam": KAM, "serit_w": SERIT_W}
    log("aciklik", oyuncu, YERLESIM["aciklik_" + oyuncu], d)
    mat_parlama_kis()
    yaz(sc, ON_EK + "serit-%s.png" % oyuncu)


def gok_katmani(ad):
    sc = atolye_sahnesi(1920, 1080, False)
    kamera(sc)
    isiklar()
    atolye(False, random.Random(32))
    mat_parlama_kis()
    yaz(sc, ad)


def panel(oyuncu):
    sc = bos_sahne(w=1100, h=904, saydam=True, ornek=4)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0), rotation=(math.radians(90), 0, 0))
    p = bpy.context.active_object; p.scale = (6, 6, 1); bpy.ops.object.transform_apply(scale=True)
    p.data.materials.append(mat_emis("p", (1, 1, 1), 1.0))
    bpy.ops.object.camera_add(location=(0, -10, 0), rotation=(math.radians(90), 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.type = "ORTHO"; kam.data.ortho_scale = 5
    yaz(sc, "panel-%s.png" % oyuncu)


if KAPAK:
    gok_katmani("kapak-gok.png")
    for o_ in ("p1", "p2", "p3"):
        serit_katmani(o_)
if YALNIZ in ("hepsi", "poz"):
    poz_maskeleri()
if YALNIZ in ("hepsi", "sahne"):
    gok_katmani("gok.png")
    for o_ in ("p1", "p2", "p3"):
        serit_katmani(o_)
        panel(o_)
json.dump(YERLESIM, open(os.path.join(CIKTI, "yerlesim.json"), "w"), indent=1)
log("bitti (atolye)", YERLESIM.get("aciklik_p1"), YERLESIM.get("aciklik_p2"), YERLESIM.get("aciklik_p3"))
