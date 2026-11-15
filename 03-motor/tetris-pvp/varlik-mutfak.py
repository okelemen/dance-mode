"""HUMAN TETRIS 28. video (REFERANSSIZ, CO-OP 2 oyuncu) - GUNDUZ DEV MUTFAK TEZGAHI, CILALI 3D OYUN GORUNUMU, TEK serit. varlik.py calistirir (--mod mutfak).

POZ-DUVARI TALIMATLAR §2b 5. mekan (karakterler minik, dev tabak/meyve; OUT ani: dev kasedeki joleye duser) + §4 CILALI 3D OYUN GORUNUMU:
canli doygun renk, tombul hatlar, parlak plastik / cilali yuzey, gercek isik-golge-parlama (Cycles), foto dokusu yok, isiksiz duz renk yok.
Kadrajin ustu dolu (Masaustu md. 7): fayans duvar, gunesli dev pencere + perde, dolaplar, raflarda kavanozlar, asili tencere/kepce, ucusan kopukler.
Soluk yasak (§8): buyuk alanlar doygun -> tezgah turkuaz cilali tas, duvar sari-turuncu fayans, pist sicak tahta; beyaz buyuk alan yok.

Katmanlar 27 (CO-OP) gibi: gok.png 1920x1080 = uzak tezgah + duvar + pencere, serit.png 1920x1080 saydam = yakin tezgah + kesme tahtasi pist + kapi.
Isik iki katmanda ayni olsun diye butun mutfak serit sahnesinde de kurulur, uzak kisim holdout (26 plaj yontemi).
yerlesim.json: aciklik_p1 (tek kapi), ampul_p1 (kiris ampulleri), dag (OUT jole kaseleri: sol/sag x, y, gecis y - motor 24 anahtar adi korunur).
Telif: genel mutfak / yiyecek ogeleri; yazi, logo, marka yok.
"""

import random
YERLESIM.clear()
KAPAK = YALNIZ == "kapak"
POZLAMA = float(arg("--pozlama", arg("--kapak-pozlama", "0")))
GUNES = float(arg("--gunes", "3.4"))
ON_EK = "kapak-" if KAPAK else ""
KAP = {"y": 8.6, "w": 7.4, "h": 3.7, "kalin": 0.55}       # CO-OP: iki kisilik genis kapi (27 ile ayni)
KAM = {"z": 2.3, "egim": 5.0, "lens": 18.0, "sensor": 24.0}
if KAPAK:
    KAM.update({"z": float(arg("--kapak-z", "2.0")), "egim": float(arg("--kapak-egim", "3.0")), "lens": float(arg("--kapak-lens", "16.0"))})
PIST = 3.9              # kesme tahtasinin yari genisligi
GECIS = 11.5            # serit tezgahi burada biter, otesi gok.png
DUVAR_Y = 60.0          # arka fayans duvar
CANLI = ("#ff3b4e", "#ffcc1e", "#1e9cff", "#2fd06a", "#ff4fc0", "#ff8a1e", "#8a5aff", "#20d6d0")
MAVI, PEMBE = "#1e8cff", "#ff3aa8"


# ------------------------------------------------------------------ sahne / isik
def mutfak_sahnesi(w, h, saydam):
    sc = bos_sahne(w=w, h=h, saydam=saydam, ornek=ORNEK, doygun=True)
    sc.view_settings.view_transform = "Standard"           # 25 notu: AgX doygun renkleri pastele ceker
    sc.view_settings.exposure = POZLAMA
    sc.cycles.max_bounces = 6; sc.cycles.diffuse_bounces = 3; sc.cycles.glossy_bounces = 3
    sc.cycles.transmission_bounces = 4; sc.cycles.transparent_max_bounces = 8
    sc.cycles.use_light_tree = True
    # dis gok (pencereden gorunur): doygun mavi degrade; ortam isigi sicak-acik (ic mekan, mavi golge az)
    nt = sc.world.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord"); sp = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Generated"], sp.inputs[0])
    rp = nt.nodes.new("ShaderNodeValToRGB"); el = rp.color_ramp.elements
    el[0].position = 0.0; el[0].color = (*lin(hex3("#4fd2ff")), 1)
    el[1].position = 0.45; el[1].color = (*lin(hex3("#0a62ff")), 1)
    e2 = el.new(0.12); e2.color = (*lin(hex3("#1aa6ff")), 1)
    nt.links.new(sp.outputs["Z"], rp.inputs[0])
    lp = nt.nodes.new("ShaderNodeLightPath")
    bg_k = nt.nodes.new("ShaderNodeBackground"); bg_k.inputs[1].default_value = 1.0
    bg_i = nt.nodes.new("ShaderNodeBackground"); bg_i.inputs[1].default_value = 0.55
    bg_i.inputs[0].default_value = (*lin(hex3("#fff0dc")), 1)  # ic ortam isigi sicak
    nt.links.new(rp.outputs[0], bg_k.inputs[0])
    mx = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(lp.outputs["Is Camera Ray"], mx.inputs[0])
    nt.links.new(bg_i.outputs[0], mx.inputs[1]); nt.links.new(bg_k.outputs[0], mx.inputs[2])
    o = nt.nodes.new("ShaderNodeOutputWorld"); nt.links.new(mx.outputs[0], o.inputs[0])
    sc.use_nodes = True; sc.render.use_compositing = True; ct = sc.node_tree; ct.nodes.clear()
    rl = ct.nodes.new("CompositorNodeRLayers"); gl = ct.nodes.new("CompositorNodeGlare"); co = ct.nodes.new("CompositorNodeComposite")
    gl.glare_type = "FOG_GLOW"; gl.quality = "HIGH"; gl.threshold = 1.3; gl.size = 7; gl.mix = 0.0
    ct.links.new(rl.outputs["Image"], gl.inputs[0]); ct.links.new(gl.outputs[0], co.inputs[0])
    if saydam:
        ct.links.new(rl.outputs["Alpha"], co.inputs[1])
    return sc


def kamera(sc):
    rx = math.radians(90 - KAM["egim"])
    bpy.ops.object.camera_add(location=(0, 0, KAM["z"]), rotation=(rx, 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.sensor_fit = "VERTICAL"; kam.data.sensor_height = KAM["sensor"]; kam.data.lens = KAM["lens"]
    kam.data.clip_end = 1500
    return kam


def isiklar():
    # gunes pencereden iceri (arkadan-yandan): uzun sicak golgeler, nesnelerde parlak kenar
    bpy.ops.object.light_add(type="SUN", location=(0, 0, 30))
    g = bpy.context.active_object; g.data.energy = GUNES; g.data.angle = math.radians(2.0)
    g.data.color = lin(hex3("#fff1d6"))
    g.rotation_euler = Vector((-0.35, 0.60, -0.72)).to_track_quat("-Z", "Y").to_euler()
    # mutfak tavan isigi: genis yumusak alan isigi (ic mekan dolgu, golgeler kapkara olmasin)
    bpy.ops.object.light_add(type="AREA", location=(0, 28, 40))
    a = bpy.context.active_object; a.data.energy = 12000; a.data.size = 40; a.data.color = lin(hex3("#fff4e6"))


# ------------------------------------------------------------------ malzemeler (plaj / dag ile ayni dil)
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


def mat_tas():
    """tezgah: doygun turkuaz cilali kuvars tas, iki ton gurultu damar; yansima az (26 notu: gok yansimasi griye yikar)"""
    m = bpy.data.materials.new("tezgah"); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    ns = nt.nodes.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value = 0.35; ns.inputs["Detail"].default_value = 5
    nt.links.new(geo.outputs["Position"], ns.inputs["Vector"])
    rp = nt.nodes.new("ShaderNodeValToRGB"); el = rp.color_ramp.elements
    el[0].position = 0.35; el[0].color = (*lin(hex3("#0fb4c4")), 1)
    el[1].position = 0.7; el[1].color = (*lin(hex3("#35d8e2")), 1)
    nt.links.new(ns.outputs["Fac"], rp.inputs[0]); nt.links.new(rp.outputs[0], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.18; b.inputs["Specular IOR Level"].default_value = 0.25
    b.inputs["Coat Weight"].default_value = 0.5; b.inputs["Coat Roughness"].default_value = 0.05
    return m


def mat_tahta(ad="tahta", r1="#f2a64a", r2="#d9822b", olcek=0.9):
    """sicak cilali tahta: dalga dokusu ile damar (prosedurel, foto dokusu yok)"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    wv = nt.nodes.new("ShaderNodeTexWave"); wv.wave_type = "BANDS"; wv.bands_direction = "X"
    wv.inputs["Scale"].default_value = olcek; wv.inputs["Distortion"].default_value = 4.0; wv.inputs["Detail"].default_value = 3
    nt.links.new(geo.outputs["Position"], wv.inputs["Vector"])
    rp = nt.nodes.new("ShaderNodeValToRGB"); el = rp.color_ramp.elements
    el[0].position = 0.2; el[0].color = (*lin(hex3(r1)), 1)
    el[1].position = 0.85; el[1].color = (*lin(hex3(r2)), 1)
    nt.links.new(wv.outputs["Fac"], rp.inputs[0]); nt.links.new(rp.outputs[0], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.35
    b.inputs["Coat Weight"].default_value = 0.35; b.inputs["Coat Roughness"].default_value = 0.1
    return m


def mat_fayans():
    """duvar: sari / turuncu buyuk fayans + krem derz (brick dokusu, kayiksiz) - dev olcek, tek fayans ~4 birim"""
    m = bpy.data.materials.new("fayans"); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sp = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(geo.outputs["Position"], sp.inputs[0])
    cb = nt.nodes.new("ShaderNodeCombineXYZ")
    nt.links.new(sp.outputs["X"], cb.inputs[0]); nt.links.new(sp.outputs["Z"], cb.inputs[1])
    br = nt.nodes.new("ShaderNodeTexBrick"); br.offset = 0.0
    br.inputs["Scale"].default_value = 0.25; br.inputs["Mortar Size"].default_value = 0.03
    br.inputs["Brick Width"].default_value = 1.0; br.inputs["Row Height"].default_value = 1.0
    br.inputs["Color1"].default_value = (*lin(hex3("#ffbe0a")), 1); br.inputs["Color2"].default_value = (*lin(hex3("#ff8a0a")), 1)   # 28 kapak olcumu: soluk -> doygun
    br.inputs["Mortar"].default_value = (*lin(hex3("#ffe2a0")), 1)
    nt.links.new(cb.outputs[0], br.inputs["Vector"])
    nt.links.new(br.outputs["Color"], b.inputs["Base Color"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.4; bp.invert = True
    nt.links.new(br.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = 0.2; b.inputs["Coat Weight"].default_value = 0.6; b.inputs["Coat Roughness"].default_value = 0.05
    return m


def mat_jele(ad, renk):
    """jole: doygun renk, yari saydam (transmission) + ic sacilma + cilali ust; titrek parlak"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*lin(hex3(renk)), 1)
    b.inputs["Roughness"].default_value = 0.05
    b.inputs["Transmission Weight"].default_value = 0.55; b.inputs["IOR"].default_value = 1.34
    b.inputs["Subsurface Weight"].default_value = 0.4; b.inputs["Subsurface Radius"].default_value = (0.6, 0.6, 0.6)
    b.inputs["Coat Weight"].default_value = 1.0; b.inputs["Coat Roughness"].default_value = 0.02
    return m


def mat_kopuk():
    """sabun kopugu: saydam, ince gokkusagi kenar (thin film yerine renkli yansima az)"""
    m = bpy.data.materials.new("kopuk"); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*lin(hex3("#e6f6ff")), 1)
    b.inputs["Roughness"].default_value = 0.0; b.inputs["Transmission Weight"].default_value = 1.0; b.inputs["IOR"].default_value = 1.05
    b.inputs["Coat Weight"].default_value = 1.0; b.inputs["Coat Tint"].default_value = (*lin(hex3("#ffb0ff")), 1)
    return m


def kutu(ad, merkez, boyut, mat, egim=0.03, seg=3):
    if egim > 0:
        return yuvarlak_kutu(ad, merkez, boyut, mat, egim=egim, seg=seg)
    bpy.ops.mesh.primitive_cube_add(size=1, location=merkez)
    o = bpy.context.active_object; o.name = ad; o.scale = boyut
    bpy.ops.object.transform_apply(scale=True)
    o.data.materials.append(mat)
    return o


def duz(ad, x0, x1, y0, y1, z, mat):
    me = bpy.data.meshes.new(ad)
    me.from_pydata([(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new(ad, me); bpy.context.collection.objects.link(o); o.data.materials.append(mat)
    return o


def silindir(konum, r, h, mat, v=40, r2=None, bevel=0.0):
    """taban konum[2]'de, yukari h"""
    x, y, z = konum
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, location=(x, y, z + h / 2), vertices=v)
    else:
        bpy.ops.mesh.primitive_cone_add(radius1=r, radius2=r2, depth=h, location=(x, y, z + h / 2), vertices=v)
    o = bpy.context.active_object; o.data.materials.append(mat)
    if bevel > 0:
        bv = o.modifiers.new("egim", "BEVEL"); bv.width = bevel; bv.segments = 4; bv.limit_method = "ANGLE"
    bpy.ops.object.shade_smooth()
    return o


def simit(konum, R, r, mat, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=konum, rotation=rot, major_segments=48, minor_segments=20)
    o = bpy.context.active_object; o.data.materials.append(mat); bpy.ops.object.shade_smooth()
    return o


# ------------------------------------------------------------------ dev yiyecekler / esyalar
def cilek(xy, s, rnd, z=0.0):
    x, y = xy
    k = kure((x, y, z + 0.95 * s), 1.0 * s, mat_pbr("cilek", "#ff2a3c", 0.25, kaplama=0.8, bump=(9 / s, 0.25)), sub=3)
    k.scale = (1.0, 1.0, 1.2); k.rotation_euler = (rnd.uniform(-0.3, 0.3), rnd.uniform(-0.3, 0.3), 0)
    yp = mat_pbr("yaprak", "#1fb84a", 0.35, kaplama=0.4)
    for i in range(6):                                            # yaprak tacı
        a = i * math.pi / 3
        o = kutu("yap", (x + math.cos(a) * 0.38 * s, y + math.sin(a) * 0.38 * s, z + 2.08 * s), (0.6 * s, 0.22 * s, 0.06 * s), yp, egim=0.05 * s)
        o.rotation_euler = (0, 0.35, a)
    boru((x, y, z + 2.05 * s), (x, y, z + 2.5 * s), 0.07 * s, yp)


def portakal(xy, s, z=0.0):
    x, y = xy
    kure((x, y, z + s), s, mat_pbr("portakal", "#ff8a14", 0.35, kaplama=0.6, bump=(14 / s, 0.35)), sub=3)
    kure((x, y, z + 1.97 * s), 0.12 * s, mat_pbr("sap", "#2f8a2a", 0.5))


def limon_dilimi(xy, s, rot=0.0):
    x, y = xy
    o = silindir((x, y, 0), 1.6 * s, 0.32 * s, mat_pbr("lim_kab", "#ffd21a", 0.3, kaplama=0.7), bevel=0.08 * s)
    o.rotation_euler = (0, 0, rot)
    silindir((x, y, 0.32 * s), 1.42 * s, 0.03 * s, mat_jele("lim_ic", "#fff06a"))
    bey = mat_pbr("lim_bey", "#fff8d8", 0.4)
    for i in range(8):                                            # dilim ciz gileri
        a = i * math.pi / 4 + rot
        boru((x, y, 0.35 * s), (x + math.cos(a) * 1.35 * s, y + math.sin(a) * 1.35 * s, 0.35 * s), 0.04 * s, bey)


def donut(xy, s, krema, rnd, z=0.0):
    x, y = xy
    simit((x, y, z + 0.55 * s), 1.3 * s, 0.6 * s, mat_pbr("hamur", "#e09a4a", 0.5, bump=(6 / s, 0.2)))
    k = simit((x, y, z + 0.78 * s), 1.3 * s, 0.5 * s, mat_pbr("krema" + krema, krema, 0.15, kaplama=1.0))
    k.scale = (1.02, 1.02, 0.85)
    for _ in range(26):                                           # seker serpintisi
        a = rnd.uniform(0, 2 * math.pi); rr = 1.3 * s + rnd.uniform(-0.35, 0.35) * s
        o = kutu("serp", (x + math.cos(a) * rr, y + math.sin(a) * rr, z + 1.2 * s), (0.28 * s, 0.07 * s, 0.07 * s),
                 mat_pbr("serp", CANLI[rnd.randrange(8)], 0.3, kaplama=0.8), egim=0.03 * s, seg=2)
        o.rotation_euler = (0, 0, rnd.uniform(0, math.pi))


def cupcake(xy, s, krema, rnd):
    x, y = xy
    k = silindir((x, y, 0), 1.0 * s, 1.3 * s, mat_pbr("kalip" + krema, CANLI[rnd.randrange(8)], 0.3, kaplama=0.7), v=24, r2=1.3 * s)
    kr = mat_pbr("ckrema" + krema, krema, 0.25, kaplama=0.8)
    for i, (r, z) in enumerate(((1.35, 1.55), (1.05, 2.1), (0.7, 2.55))):
        o = simit((x, y, z * s), r * s * 0.75, 0.32 * s, kr); o.rotation_euler = (0, 0, i)
    kure((x, y, 2.95 * s), 0.38 * s, mat_pbr("kiraz", "#e8102a", 0.15, kaplama=1.0))


def tabak(xy, s, rnd):
    x, y = xy
    silindir((x, y, 0), 7.2 * s, 0.25 * s, mat_pbr("tabak", "#f6f9ff", 0.12, kaplama=1.0), v=64, r2=8.6 * s, bevel=0.1 * s)
    simit((x, y, 0.3 * s), 8.3 * s, 0.22 * s, mat_pbr("tabak_kenar", "#1e7cff", 0.15, kaplama=1.0))
    for (dx, dy) in ((-2.4, -1.0), (1.8, -2.2), (0.4, 1.8), (3.2, 1.6), (-2.6, 2.6)):
        cilek((x + dx * s, y + dy * s), 1.05 * s, rnd, z=0.25 * s)
    yb = mat_pbr("yaban", "#3a3cff", 0.25, kaplama=0.8)
    for _ in range(9):
        kure((x + rnd.uniform(-5, 5) * s, y + rnd.uniform(-4, 4) * s, 0.75 * s), 0.5 * s, yb)


def kavanoz(xy, s, rnd, kapak="#ff3b4e", ic="kurabiye"):
    x, y = xy
    silindir((x, y, 0), 4.0 * s, 11.0 * s, mat_cam("kav_cam"), v=48, bevel=0.6 * s)
    silindir((x, y, 11.0 * s), 3.6 * s, 1.4 * s, mat_pbr("kav_kap" + kapak, kapak, 0.2, kaplama=1.0), v=48, bevel=0.3 * s)
    kure((x, y, 12.6 * s), 0.8 * s, mat_pbr("kav_top" + kapak, kapak, 0.2, kaplama=1.0))
    kur = mat_pbr("kurabiye", "#d98a3a", 0.55, bump=(3 / s, 0.4)); cik = mat_pbr("cikolata", "#4a2412", 0.3, kaplama=0.6)
    for i in range(7):
        z = 0.5 * s + i * 1.35 * s
        o = silindir((x + rnd.uniform(-1, 1) * s, y + rnd.uniform(-1, 1) * s, z), 2.4 * s, 0.6 * s, kur, v=32, bevel=0.2 * s)
        o.rotation_euler = (rnd.uniform(-0.35, 0.35), rnd.uniform(-0.35, 0.35), 0)
        for _ in range(4):
            a = rnd.uniform(0, 6.28)
            kure((o.location.x + math.cos(a) * 1.4 * s, o.location.y + math.sin(a) * 1.4 * s, z + 0.62 * s), 0.25 * s, cik)


def pankek(xy, s, rnd):
    x, y = xy
    hm = mat_pbr("pankek", "#f0a845", 0.45, kaplama=0.3, bump=(5 / s, 0.2))
    for i in range(6):
        silindir((x + rnd.uniform(-0.2, 0.2) * s, y, i * 0.75 * s), 3.2 * s, 0.7 * s, hm, v=40, bevel=0.3 * s)
    silindir((x, y, 4.5 * s), 3.0 * s, 0.12 * s, mat_jele("surup", "#c25a10"))
    kutu("tereyag", (x, y, 4.95 * s), (1.4 * s, 1.4 * s, 0.7 * s), mat_pbr("tereyag", "#ffe36a", 0.3, kaplama=0.6), egim=0.15 * s)


def tahta_kasik(a, b, s):
    tm = mat_tahta("kasik", "#e8a050", "#c97a30", 2.0)
    boru(a, b, 0.35 * s, tm)
    B = Vector(b); d = (B - Vector(a)).normalized()
    o = kure(tuple(B + d * 1.6 * s), 1.7 * s, tm); o.scale = (1.0, 1.0, 0.35)
    o.rotation_euler = d.to_track_quat("Y", "Z").to_euler()


def oklava(xy, s, rot):
    x, y = xy
    tm = mat_tahta("oklava", "#f0b060", "#d08a3a", 3.0)
    c = Vector((x, y, 0.9 * s)); d = Vector((math.cos(rot), math.sin(rot), 0))
    boru(tuple(c - d * 4.5 * s), tuple(c + d * 4.5 * s), 0.9 * s, tm)
    for sg in (-1, 1):
        boru(tuple(c + d * sg * 4.5 * s), tuple(c + d * sg * 6.2 * s), 0.35 * s, mat_pbr("oklava_u", "#ff3b4e", 0.25, kaplama=0.8))


def caydanlik(xy, s):
    x, y = xy
    kr = mat_pbr("caydanlik", "#ff3b4e", 0.12, kaplama=1.0)
    k = kure((x, y, 3.6 * s), 4.0 * s, kr, sub=4); k.scale = (1.0, 1.0, 0.85)
    silindir((x, y, 6.5 * s), 1.2 * s, 0.6 * s, kr)
    kure((x, y, 7.3 * s), 0.6 * s, mat_pbr("cay_top", "#15171a", 0.3, kaplama=0.8))
    boru((x - 3.4 * s, y, 3.0 * s), (x - 6.2 * s, y, 5.4 * s), 0.6 * s, kr)
    o = simit((x, y, 7.8 * s), 2.4 * s, 0.32 * s, mat_pbr("cay_kulp", "#15171a", 0.3, kaplama=0.8), rot=(math.radians(90), 0, 0))
    o.scale = (1.0, 1.0, 0.7)


def saksi(xy, s, rnd):
    x, y = xy
    silindir((x, y, 0), 2.2 * s, 3.4 * s, mat_pbr("saksi", "#ff6a2a", 0.3, kaplama=0.7), r2=2.8 * s, bevel=0.2 * s)
    yp = mat_pbr("feslegen", "#1fbf4a", 0.3, kaplama=0.5)
    for _ in range(16):
        a = rnd.uniform(0, 6.28); r = rnd.uniform(0.3, 1.8) * s
        o = kure((x + math.cos(a) * r, y + math.sin(a) * r, (3.6 + rnd.uniform(0, 3.2)) * s), rnd.uniform(0.9, 1.4) * s, yp)
        o.scale = (1.0, 0.55, 0.35); o.rotation_euler = (rnd.uniform(-0.6, 0.6), rnd.uniform(-0.6, 0.6), a)


def cirpici_kup(xy, s):
    x, y = xy
    silindir((x, y, 0), 2.6 * s, 6.0 * s, mat_pbr("kup", "#8a5aff", 0.2, kaplama=1.0), bevel=0.3 * s)
    met = mat_pbr("cirpici", "#d8dde3", 0.15, metal=1.0)
    for i in range(6):
        a = i * math.pi / 6
        o = simit((x, y, 11.0 * s), 1.6 * s, 0.07 * s, met, rot=(math.radians(90), 0, a)); o.scale = (1.0, 1.0, 2.6)
    boru((x, y, 4.0 * s), (x, y, 7.2 * s), 0.35 * s, mat_pbr("cir_sap", "#ff4fc0", 0.25, kaplama=0.8))
    boru((x - 1.8 * s, y + 0.5 * s, 3.0 * s), (x - 3.0 * s, y + 1.0 * s, 12.0 * s), 0.4 * s, mat_tahta("kup_kasik", "#e8a050", "#c97a30", 2.0))
    boru((x + 1.6 * s, y + 0.4 * s, 3.0 * s), (x + 2.8 * s, y + 0.8 * s, 11.0 * s), 0.3 * s, mat_pbr("spatula", "#2fd06a", 0.3, kaplama=0.8))
    kutu("spat_uc", (x + 2.95 * s, y + 0.85 * s, 12.2 * s), (1.6 * s, 0.3 * s, 2.0 * s), mat_pbr("spatula2", "#2fd06a", 0.3, kaplama=0.8), egim=0.25 * s)


# ------------------------------------------------------------------ arka duvar: fayans + pencere + dolaplar + raflar + asili tencere
def duvar(rnd):
    fy = mat_fayans()
    Y = DUVAR_Y
    PX0, PX1, PZ0, PZ1 = -17.0, 17.0, 11.0, 31.0                   # pencere boslugu
    kutu("duvar_sol", ((-140 + PX0) / 2, Y, 40), (140 + PX0, 1.0, 80), fy, egim=0)
    kutu("duvar_sag", ((140 + PX1) / 2, Y, 40), (140 - PX1, 1.0, 80), fy, egim=0)
    kutu("duvar_alt", (0, Y, PZ0 / 2), (PX1 - PX0, 1.0, PZ0), fy, egim=0)
    kutu("duvar_ust", (0, Y, (80 + PZ1) / 2), (PX1 - PX0, 1.0, 80 - PZ1), fy, egim=0)
    # pencere cercevesi (kirmizi cilali) + kayit
    cr = mat_pbr("cerceve", "#e8343f", 0.18, kaplama=1.0)
    for (cx, cz, w, h) in ((PX0, (PZ0 + PZ1) / 2, 1.4, PZ1 - PZ0 + 1.4), (PX1, (PZ0 + PZ1) / 2, 1.4, PZ1 - PZ0 + 1.4),
                           (0, PZ0, PX1 - PX0 + 1.4, 1.4), (0, PZ1, PX1 - PX0 + 1.4, 1.4),
                           (0, (PZ0 + PZ1) / 2, 0.7, PZ1 - PZ0), (0, (PZ0 + PZ1) / 2 + 2, PX1 - PX0, 0.7)):
        kutu("cerceve", (cx, Y - 0.6, cz), (w, 1.4, h), cr, egim=0.25)
    kutu("pervaz", (0, Y - 1.6, PZ0 - 0.4), (PX1 - PX0 + 4, 3.2, 0.8), cr, egim=0.25)
    # pervazda kucuk saksilar (dev olcekte bile pencere kenari dolu)
    for i, xx in enumerate((-12.0, -4.0, 5.0, 12.5)):
        silindir((xx, Y - 1.8, PZ0), 1.1, 1.6, mat_pbr("pv_saksi%d" % i, CANLI[(i * 3) % 8], 0.3, kaplama=0.7), r2=1.4)
        for _ in range(5):
            kure((xx + rnd.uniform(-0.8, 0.8), Y - 1.8 + rnd.uniform(-0.5, 0.5), PZ0 + 2.0 + rnd.uniform(0, 1.6)), rnd.uniform(0.5, 0.8),
                 mat_pbr("pv_cic%d" % i, ("#ff4fc0", "#ffcc1e", "#ff3b4e", "#8a5aff")[i], 0.35, kaplama=0.4))
    # perdeler: pembe, kivrimli (yan yana silindirler), ustte farbala
    pe = mat_pbr("perde", "#ff5fb8", 0.5, kaplama=0.2, bump=(2.0, 0.2))
    for s in (-1, 1):
        for i in range(7):
            x = s * (PX1 + 1.5 - i * 1.15)
            o = silindir((x, Y - 2.4, PZ0 - 2.0), 0.9, PZ1 - PZ0 + 6.0, pe, v=16); o.scale = (1.0, 0.6, 1.0)
    for i in range(14):
        kure((PX0 - 2 + i * (PX1 - PX0 + 4) / 13, Y - 2.6, PZ1 + 3.6), 1.6, pe).scale = (1.0, 0.6, 0.7)
    boru((PX0 - 5, Y - 2.4, PZ1 + 4.5), (PX1 + 5, Y - 2.4, PZ1 + 4.5), 0.35, mat_pbr("korniz", "#ffcc1e", 0.2, metal=0.6))
    # pencere disi: yesil tepeler, agaclar, bulutlar (gok dolu)
    for (x, y, r, h, renk) in ((-90, 220, 90, 90, "#2fb84a"), (40, 240, 110, 110, "#24a840"), (150, 230, 90, 80, "#3cc456"),
                               (-20, 190, 70, 70, "#4ad060")):
        k = kure((x, y, -h * 0.3), r, mat_pbr("tepe" + renk, renk, 0.5, kaplama=0.2), sub=3); k.scale = (1.0, 0.5, h / r)
    for (x, y, h) in ((-30, 170, 40), (-8, 175, 46), (14, 172, 38), (32, 178, 44), (-48, 182, 42)):
        boru((x, y, 0), (x, y, h * 0.5), 2.0, mat_pbr("govde", "#7a3f1e", 0.6))
        kure((x, y, h * 0.75), h * 0.32, mat_pbr("agac", "#1fae46", 0.45, kaplama=0.3), sub=3)
    for (x, y, z, o) in ((-30, 300, 95, 16), (10, 320, 120, 20), (45, 300, 85, 14), (-5, 280, 65, 10), (-50, 330, 140, 22)):
        bulut((x, y, z), o, rnd)
    # ust dolaplar (pencerenin iki yaninda): doygun turkuaz kapak + altin kulp; altlarinda raf + kavanozlar
    dl = mat_pbr("dolap", "#1e9cff", 0.2, kaplama=0.9); kl = mat_pbr("kulp", "#ffcc1e", 0.15, metal=0.8)
    for s in (-1, 1):
        for i in range(3):
            x = s * (PX1 + 9 + i * 14)
            kutu("dolap", (x, Y - 4.5, 34), (13.2, 8.0, 18), dl, egim=0.6, seg=4)
            kutu("dolap_pan", (x, Y - 8.55, 34), (10.5, 0.2, 15), mat_pbr("dolap_p", "#4ab8ff", 0.2, kaplama=0.9), egim=0.3)
            kutu("kulp", (x - s * 4.0, Y - 8.9, 30), (0.5, 0.6, 3.0), kl, egim=0.2)
    for s in (-1, 1):                                             # raf
        kutu("raf", (s * (PX1 + 23), Y - 3.0, 17.5), (40, 6.0, 0.8), mat_tahta("raf", "#e89a48", "#c87a30", 0.6), egim=0.2)
        for i in range(6):
            x = s * (PX1 + 6 + i * 6.4)
            h = rnd.uniform(4.0, 6.5); renk = CANLI[(i * 5 + (s > 0)) % 8]
            silindir((x, Y - 3.0, 17.9), 2.1, h, mat_cam("rk_cam"), v=24, bevel=0.3)
            silindir((x, Y - 3.0, 18.1), 1.85, h * 0.7, mat_pbr("rk_ic" + renk, renk, 0.35, kaplama=0.3), v=24)
            silindir((x, Y - 3.0, 17.9 + h), 2.0, 0.8, mat_pbr("rk_kap" + renk, CANLI[(i * 5 + 3) % 8], 0.2, kaplama=1.0), v=24, bevel=0.15)
    # asili ray + bakir tencere / kepceler (pencerenin onunde ustte)
    met = mat_pbr("ray", "#d8dde3", 0.2, metal=1.0); bak = mat_pbr("bakir", "#ff8a4a", 0.18, metal=1.0)
    boru((-30, Y - 10, 29.0), (30, Y - 10, 29.0), 0.35, met)
    for i, x in enumerate((-24, -15, -7, 7, 15, 24)):
        boru((x, Y - 10, 29.0), (x, Y - 10, 26.0 - (i % 2) * 1.5), 0.12, met)
        if i % 2 == 0:
            z = 22.0
            silindir((x, Y - 10, z), 2.6, 3.5, bak, bevel=0.3)
            boru((x, Y - 10, z + 3.5), (x, Y - 10, 26.0), 0.25, bak)
        else:
            boru((x, Y - 10, 24.5), (x, Y - 10, 19.0), 0.3, met)
            k = kure((x, Y - 10, 18.0), 1.5, met); k.scale = (1.0, 1.0, 0.55)
    # tavan girlandi: renkli ampuller dolap ustunden (kendi isigi olan nesne, emission serbest)
    for s in (-1, 1):
        for i in range(14):
            t = i / 13
            x = s * (PX1 + 3 + t * 40); z = 24.0 - 2.0 * math.sin(t * math.pi)
            kure((x, Y - 9.5, z), 0.6, mat_emis("girlant%d" % (i % 4), lin(hex3(("#ffcc1e", "#ff4fc0", "#20d6d0", "#ff8a1e")[i % 4])), 3.0))


def bulut(merkez, olcek, rnd):
    beyaz = mat_pbr("bulut", "#ffffff", 0.85)
    x, y, z = merkez
    for k in range(9):
        r = olcek * rnd.uniform(0.45, 0.85)
        dx = rnd.uniform(-1.5, 1.5) * olcek; dz = rnd.uniform(-0.2, 0.55) * olcek * (1 - abs(dx) / (2 * olcek))
        b = kure((x + dx, y + rnd.uniform(-0.4, 0.4) * olcek, z + dz), r, beyaz, sub=3); b.scale = (1.15, 0.8, 0.9)
    kure((x, y, z - 0.25 * olcek), olcek * 0.75, beyaz).scale = (2.4, 0.8, 0.45)


def kopukler(rnd):
    """havada uçusan sabun kopukleri (ekran dolu: ust bosluk)"""
    km = mat_kopuk()
    for _ in range(26):
        x = rnd.uniform(-45, 45); y = rnd.uniform(16, 52); z = rnd.uniform(6, 30)
        if abs(x) < 9 and y < 26:
            continue
        kure((x, y, z), rnd.uniform(0.8, 2.4), km)


# ------------------------------------------------------------------ MUTFAK (her iki katmanda; serit sahnesinde uzak kisim holdout)
def mutfak(serit_modu, rnd):
    ts = mat_tas()
    duz("tezgah_yakin", -90, 90, -4, GECIS, 0, ts)
    duz("tezgah_uzak", -400, 400, GECIS, DUVAR_Y, 0, ts)
    duvar(rnd)
    kopukler(rnd)
    # dev esyalar tezgahta (karakterler minik: 1 kisi ~1,8 birim)
    tabak((-24, 30), 1.0, rnd)
    kavanoz((25, 40), 1.0, rnd)
    pankek((-8, 46), 1.0, rnd)
    caydanlik((42, 48), 1.0)
    cirpici_kup((-42, 50), 1.0)
    saksi((-52, 32), 1.2, rnd)
    for (xy, s, kr) in (((12, 22), 1.3, "#ff6ad0"), ((17.5, 30), 1.5, "#5a2a14"), ((-14, 24), 1.2, "#ffcc1e")):
        donut(xy, s, kr, rnd)
    cupcake((-10, 17.5), 1.1, "#ffd0ec", rnd); cupcake((8.5, 36), 1.4, "#b8f0ff", rnd); cupcake((34, 24), 1.3, "#fff2a8", rnd)
    limon_dilimi((-4.5, 30), 1.2, 0.3); limon_dilimi((38, 33), 1.4, 1.0)
    portakal((30, 16), 1.8); portakal((-33, 18), 2.2); portakal((-30, 13.5), 1.4)
    cilek((-17, 15), 1.3, rnd); cilek((20, 14.5), 1.2, rnd); cilek((6, 26), 1.0, rnd)
    tahta_kasik((-46, 20, 0.4), (-30, 40, 0.4), 1.0)
    oklava((44, 19), 1.0, 0.5)
    if serit_modu:                                               # yakin tezgah disinda her parca holdout
        for o in bpy.data.objects:
            if o.type == "MESH" and o.name.split(".")[0] not in ("tezgah_yakin",):
                o.is_holdout = True


# ------------------------------------------------------------------ SERIT: kesme tahtasi pist + makaron sinir + oklar + OUT jole kaseleri
def makaron(konum, r, renk, ic="#ffe04a"):   # 28 kapak olcumu: krem dolgu soluk -> sari
    x, y, z = konum
    kab = mat_pbr("mak" + renk, renk, 0.4, kaplama=0.4, bump=(30, 0.15))
    for dz in (0.0, 0.62 * r):
        o = silindir((x, y, z + dz), r, 0.42 * r, kab, v=32, bevel=0.18 * r)
    silindir((x, y, z + 0.4 * r), 0.9 * r, 0.24 * r, mat_pbr("mak_ic" + ic, ic, 0.4, kaplama=0.3), v=32)


def serit_esyalari(rnd):
    kutu("tahta", (0, (KAP["y"] + 0.4 - 4) / 2, 0.03), (PIST * 2, KAP["y"] + 4.4, 0.06), mat_tahta("tahta", "#ff9418", "#f07808", 0.6), egim=0.02, seg=2)   # 28 onizleme 1: damar zebra gibi sertti -> yakin tonlar
    bay = {-1: MAVI, 1: PEMBE}
    for s in (-1, 1):                                            # pist kenarinda makaron siniri: solda mavi, sagda pembe (P1/P2 tarafi)
        y = -3.4
        i = 0
        while y < KAP["y"] - 0.2:
            renk = bay[s] if i % 2 == 0 else ("#ffcc1e" if s < 0 else "#2fd06a")
            makaron((s * (PIST + 0.45), y, 0.0), 0.42, renk); y += 0.95; i += 1
    ok = mat_pbr("ok", "#ffcc1e", 0.3, kaplama=0.7)             # tahta ustunde sari yon oklari (seri sabiti)
    for x in (-1.7, 1.7):
        for y in (4.6, 6.2):
            nok = [(x - 0.6, y - 0.4), (x, y), (x + 0.6, y - 0.4), (x + 0.6, y - 0.68), (x, y - 0.28), (x - 0.6, y - 0.68)]
            me = bpy.data.meshes.new("ok"); me.from_pydata([(a, b, 0.07) for a, b in nok], [], [list(range(6))]); me.update()
            o = bpy.data.objects.new("ok", me); bpy.context.collection.objects.link(o); o.data.materials.append(ok)
            o.modifiers.new("k", "SOLIDIFY").thickness = 0.02
    # OUT ani: iki dis tarafta dev jole kasesi (karakterler buraya duser) - sol mavi jole, sag pembe jole
    for s in (-1, 1):
        silindir((s * 5.6, 5.0, 0), 1.0, 1.0, mat_pbr("kase" + str(s), "#ffcc1e" if s < 0 else "#20d6d0", 0.1, kaplama=1.0), v=48, r2=1.65, bevel=0.1)
        simit((s * 5.6, 5.0, 1.0), 1.65, 0.1, mat_pbr("kase_k" + str(s), "#ff3b4e", 0.15, kaplama=1.0))
        j = kure((s * 5.6, 5.0, 1.0), 1.55, mat_jele("jole" + str(s), MAVI if s < 0 else PEMBE), sub=4); j.scale = (1.0, 1.0, 0.5)
        kure((s * 5.6, 5.0, 1.82), 0.22, mat_pbr("j_kiraz" + str(s), "#e8102a", 0.12, kaplama=1.0))
    # dis tarafta kucuk yiyecekler (dev olcekte bile yakin plan dolu)
    cilek((-7.6, 9.6), 0.75, rnd); portakal((7.8, 9.8), 0.9); donut((-7.2, 2.8), 0.55, "#ff6ad0", rnd); cupcake((7.2, 2.6), 0.55, "#b8f0ff", rnd)


def kapi():
    """makaron kuleli kemer: iki yanda ust uste renkli makaronlar; kiris bisküvi + pembe krema damlasi + serpinti; ustte sonuk LED tabela; ampul dizisi"""
    Y, W_, H_, K = KAP["y"], KAP["w"], KAP["h"], KAP["kalin"]
    xk = W_ / 2 + K / 2
    rk = ("#ff4fc0", "#20d6d0", "#ffcc1e", "#8a5aff", "#2fd06a")
    for s in (-1, 1):
        for i in range(5):                                       # 5 makaron x 0,85 = 4,25 (H+K)
            makaron((s * xk, Y, i * 0.85), 0.62, rk[(i + (s > 0) * 2) % 5])
        donut((s * xk, Y), 0.42, "#ff6ad0" if s < 0 else "#5a2a14", random.Random(7 + s), z=H_ + K + 0.02)
    bis = mat_pbr("biskuvi", "#e8a24a", 0.5, kaplama=0.2, bump=(8, 0.3))
    yuvarlak_kutu("kiris", (0, Y, H_ + K / 2), (W_ + 2 * K, K + 0.1, K), bis, egim=0.18, seg=5)
    kr = mat_pbr("kiris_krema", "#ff6ad0", 0.12, kaplama=1.0)
    yuvarlak_kutu("kiris_krema", (0, Y, H_ + K + 0.04), (W_ + 2 * K - 0.1, K + 0.18, 0.18), kr, egim=0.09, seg=4)
    r2 = random.Random(28)
    for i in range(11):                                          # kiris onunde krema damlalari
        x = -W_ / 2 + 0.2 + i * (W_ - 0.4) / 10
        L = 0.25 + 0.2 * r2.random()
        boru((x, Y - 0.36, H_ + K - 0.02), (x, Y - 0.36, H_ + K - L), 0.09, kr)
        kure((x, Y - 0.36, H_ + K - L), 0.11, kr)
    for _ in range(40):
        o = kutu("serp", (r2.uniform(-W_ / 2 - K, W_ / 2 + K), Y + r2.uniform(-0.3, 0.3), H_ + K + 0.14), (0.16, 0.05, 0.05),
                 mat_pbr("serp", CANLI[r2.randrange(8)], 0.3, kaplama=0.8), egim=0.02, seg=2)
        o.rotation_euler = (0, 0, r2.uniform(0, math.pi))
    yuvarlak_kutu("tabela", (0, Y, H_ + K + 0.75), (W_ * 0.6, 0.2, 0.7), mat_pbr("tabela", "#15171a", 0.35, metal=0.4), egim=0.05, seg=3)
    me = bpy.data.meshes.new("led_yuz"); a, b = W_ * 0.28, 0.28; z0 = H_ + K + 0.75
    me.from_pydata([(-a, Y - 0.11, z0 - b), (a, Y - 0.11, z0 - b), (a, Y - 0.11, z0 + b), (-a, Y - 0.11, z0 + b)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("led_yuz", me); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat_emis("led_yuz", lin(hex3("#0a3a6a")), 1.2))
    for s in (-1, 1):
        boru((s * W_ * 0.22, Y, H_ + K + 0.2), (s * W_ * 0.22, Y, H_ + K + 0.42), 0.02, mat_pbr("tel", "#cfd3d8", 0.3, metal=1.0))


def serit_katmani():
    sc = mutfak_sahnesi(1920, 1080, True)
    kam = kamera(sc)
    rnd = random.Random(28)
    isiklar()
    mutfak(True, random.Random(28))
    serit_esyalari(rnd)
    kapi()
    Y, W_, H_ = KAP["y"], KAP["w"], KAP["h"]
    ic = W_ / 2
    bpy.context.view_layer.update()
    px = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-ic, Y, 0), (ic, Y, 0), (-ic, Y, H_), (ic, Y, H_))]
    xs = [p.x * 1920 for p in px]; ys = [(1 - p.y) * 1080 for p in px]
    YERLESIM[ON_EK + "aciklik_p1"] = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
    YERLESIM[ON_EK + "ampul_p1"] = []
    for i in range(23):                                    # kiris onunde ampul dizisi; motor (ampulCiz) yakip sondurur
        q = world_to_camera_view(sc, kam, Vector((-ic + i * 2 * ic / 22, Y - 0.42, H_ + 0.05)))
        YERLESIM[ON_EK + "ampul_p1"].append([round(q.x * 1920, 1), round((1 - q.y) * 1080, 1)])
    mk = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-5.6, 5.0, 1.2), (5.6, 5.0, 1.2), (0, GECIS, 0))]
    YERLESIM["dag"] = {"yigin_sol_x": round(mk[0].x * 1920, 1), "yigin_sag_x": round(mk[1].x * 1920, 1),
                       "yigin_y": round((1 - mk[0].y) * 1080, 1), "gecis_y": round((1 - mk[2].y) * 1080, 1)}
    YERLESIM["yol"] = {"y_kapi": Y, "genislik": PIST * 2, "kam": KAM, "serit_w": 1920}
    log("aciklik", YERLESIM[ON_EK + "aciklik_p1"], YERLESIM["dag"])
    yaz(sc, ON_EK + "serit.png")


def gok_katmani(ad):
    sc = mutfak_sahnesi(1920, 1080, False)
    kamera(sc)
    isiklar()
    mutfak(False, random.Random(28))
    yaz(sc, ad)


if KAPAK:
    gok_katmani("kapak-gok.png")
    serit_katmani()
if YALNIZ in ("hepsi", "poz"):
    poz_maskeleri()
if YALNIZ in ("hepsi", "sahne"):
    gok_katmani("gok.png")
    serit_katmani()
json.dump(YERLESIM, open(os.path.join(CIKTI, "yerlesim.json"), "w"), indent=1)
log("bitti (mutfak)", YERLESIM.get(ON_EK + "aciklik_p1"))
