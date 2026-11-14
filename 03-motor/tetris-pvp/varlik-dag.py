"""HUMAN TETRIS 27. video (REFERANSSIZ, CO-OP 2 oyuncu) - GUNDUZ KARLI DAG ZIRVESI, CILALI 3D OYUN GORUNUMU, TEK serit. varlik.py calistirir (--mod dag).

POZ-DUVARI TALIMATLAR §2b 4. mekan (kar, cam, teleferik; OUT ani: kar yiginina gomulur) + §4 CILALI 3D OYUN GORUNUMU:
canli doygun renk, tombul hatlar, parlak plastik / cilali yuzey, gercek isik-golge-parlama (Cycles), foto dokusu yok, isiksiz duz renk yok.
Gok dolu (Masaustu md. 7): bulut kumeleri, teleferik halatlari + kabinler, yamac parasutleri, sicak hava balonu.
Soluk yasak (§8, 14 Kas): kar beyazi buyuk alan -> pist turkuaz buz, golgeler gok mavisi, cam koyu yesil, kabin/bayrak/esya doygun.

Katmanlar 23 (CO-OP) gibi: gok.png 1920x1080 = uzak dag + gok, serit.png 1920x1080 saydam = yakin kar + buz pist + kapi.
Isik iki katmanda ayni olsun diye butun dag serit sahnesinde de kurulur, uzak kismi holdout (26 plaj yontemi).
yerlesim.json: aciklik_p1 (tek kapi), ampul_p1 (kiris ampulleri), dag (OUT kar yiginlari: sol/sag x, y, gecis y).
Telif: genel kis / kayak ogeleri; yazi, logo, marka yok.
"""

import random
YERLESIM.clear()
KAPAK = YALNIZ == "kapak"
POZLAMA = float(arg("--pozlama", arg("--kapak-pozlama", "0")))
GUNES = float(arg("--gunes", "3.4"))
ON_EK = "kapak-" if KAPAK else ""
KAP = {"y": 8.6, "w": 7.4, "h": 3.7, "kalin": 0.55}       # CO-OP: iki kisilik genis kapi (23: 7,4)
KAM = {"z": 2.3, "egim": 5.0, "lens": 18.0, "sensor": 24.0}
if KAPAK:
    KAM.update({"z": float(arg("--kapak-z", "2.0")), "egim": float(arg("--kapak-egim", "3.0")), "lens": float(arg("--kapak-lens", "16.0"))})
PIST = 3.9              # buz pistin yari genisligi
GECIS = 11.5            # serit kari burada biter, otesi gok.png
CANLI = ("#ff3b4e", "#ffcc1e", "#1e9cff", "#2fd06a", "#ff4fc0", "#ff8a1e", "#8a5aff", "#20d6d0")
MAVI, PEMBE = "#1e8cff", "#ff3aa8"


# ------------------------------------------------------------------ sahne / isik
def dag_sahnesi(w, h, saydam):
    sc = bos_sahne(w=w, h=h, saydam=saydam, ornek=ORNEK, doygun=True)
    sc.view_settings.view_transform = "Standard"           # 25 notu: AgX doygun renkleri pastele ceker
    sc.view_settings.exposure = POZLAMA
    sc.cycles.max_bounces = 6; sc.cycles.diffuse_bounces = 3; sc.cycles.glossy_bounces = 3
    sc.cycles.transmission_bounces = 2; sc.cycles.transparent_max_bounces = 8
    sc.cycles.use_light_tree = True
    # gok: doygun mavi degrade (26'nin canli goku); ortam isigi mavi -> kar golgeleri mavi (kar soluk gri olmasin)
    nt = sc.world.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord"); sp = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Generated"], sp.inputs[0])
    rp = nt.nodes.new("ShaderNodeValToRGB"); el = rp.color_ramp.elements
    el[0].position = 0.0; el[0].color = (*lin(hex3("#3fc8ff")), 1)
    el[1].position = 0.45; el[1].color = (*lin(hex3("#0a5aff")), 1)
    e2 = el.new(0.12); e2.color = (*lin(hex3("#1a9cff")), 1)
    nt.links.new(sp.outputs["Z"], rp.inputs[0])
    lp = nt.nodes.new("ShaderNodeLightPath")
    bg_k = nt.nodes.new("ShaderNodeBackground"); bg_k.inputs[1].default_value = 1.0
    bg_i = nt.nodes.new("ShaderNodeBackground"); bg_i.inputs[1].default_value = 0.5
    nt.links.new(rp.outputs[0], bg_k.inputs[0]); nt.links.new(rp.outputs[0], bg_i.inputs[0])
    mx = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(lp.outputs["Is Camera Ray"], mx.inputs[0])
    nt.links.new(bg_i.outputs[0], mx.inputs[1]); nt.links.new(bg_k.outputs[0], mx.inputs[2])
    o = nt.nodes.new("ShaderNodeOutputWorld"); nt.links.new(mx.outputs[0], o.inputs[0])
    sc.use_nodes = True; sc.render.use_compositing = True; ct = sc.node_tree; ct.nodes.clear()
    rl = ct.nodes.new("CompositorNodeRLayers"); gl = ct.nodes.new("CompositorNodeGlare"); co = ct.nodes.new("CompositorNodeComposite")
    gl.glare_type = "FOG_GLOW"; gl.quality = "HIGH"; gl.threshold = 1.4; gl.size = 7; gl.mix = 0.0   # kar parlakligi her yeri haresin diye esik 1,4
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
    bpy.ops.object.light_add(type="SUN", location=(0, 0, 30))
    g = bpy.context.active_object; g.data.energy = GUNES; g.data.angle = math.radians(1.5)
    g.data.color = lin(hex3("#fff1d6"))                     # sicak gunes, mavi golge: kar iki tonlu okunur
    g.rotation_euler = Vector((-0.40, 0.55, -0.73)).to_track_quat("-Z", "Y").to_euler()


# ------------------------------------------------------------------ malzemeler (plaj ile ayni dil)
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


def mat_kar(ad, renk1="#f4faff", renk2="#d6ecff", purluk=0.5, dalga=0.12):
    """prosedurel kar: iki ton gurultu (beyaz / acik buz mavisi) + yumusak tumsek + ince parilti; foto dokusu yok"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    ns = nt.nodes.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value = 0.4; ns.inputs["Detail"].default_value = 3
    nt.links.new(geo.outputs["Position"], ns.inputs["Vector"])
    rp = nt.nodes.new("ShaderNodeValToRGB")
    rp.color_ramp.elements[0].position = 0.35; rp.color_ramp.elements[1].position = 0.7
    rp.color_ramp.elements[0].color = (*lin(hex3(renk1)), 1); rp.color_ramp.elements[1].color = (*lin(hex3(renk2)), 1)
    nt.links.new(ns.outputs["Fac"], rp.inputs[0]); nt.links.new(rp.outputs[0], b.inputs["Base Color"])
    tm = nt.nodes.new("ShaderNodeTexNoise"); tm.inputs["Scale"].default_value = 1.6; tm.inputs["Detail"].default_value = 4
    nt.links.new(geo.outputs["Position"], tm.inputs["Vector"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = dalga; bp.inputs["Distance"].default_value = 0.05
    nt.links.new(tm.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = purluk
    b.inputs["Coat Weight"].default_value = 0.25; b.inputs["Coat Roughness"].default_value = 0.15   # parilti
    b.inputs["Subsurface Weight"].default_value = 0.15; b.inputs["Subsurface Radius"].default_value = (0.4, 0.7, 1.0)
    return m


def mat_buz():
    """pist: doygun turkuaz cilali buz, ince catlak/girdap bump, gok yansimasi az (26 deniz notu: yansima griye yikar)"""
    m = bpy.data.materials.new("buz"); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    ns = nt.nodes.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value = 0.7; ns.inputs["Detail"].default_value = 4
    nt.links.new(geo.outputs["Position"], ns.inputs["Vector"])
    rp = nt.nodes.new("ShaderNodeValToRGB"); el = rp.color_ramp.elements
    el[0].position = 0.3; el[0].color = (*lin(hex3("#12c8f0")), 1)
    el[1].position = 0.75; el[1].color = (*lin(hex3("#4fe8ff")), 1)
    nt.links.new(ns.outputs["Fac"], rp.inputs[0]); nt.links.new(rp.outputs[0], b.inputs["Base Color"])
    vr = nt.nodes.new("ShaderNodeTexVoronoi"); vr.feature = "DISTANCE_TO_EDGE"; vr.inputs["Scale"].default_value = 1.3
    nt.links.new(geo.outputs["Position"], vr.inputs["Vector"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.12; bp.inputs["Distance"].default_value = 0.02
    nt.links.new(vr.outputs["Distance"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = 0.1; b.inputs["Specular IOR Level"].default_value = 0.2
    b.inputs["Coat Weight"].default_value = 0.6; b.inputs["Coat Roughness"].default_value = 0.03
    return m


def renk_dilimli(o, mats, n, eksen="z"):
    for m_ in mats:
        o.data.materials.append(m_)
    vs = o.data.vertices; mrk = sum((v.co for v in vs), Vector()) / max(1, len(vs))
    for p in o.data.polygons:
        c = p.center - mrk
        a = math.atan2(c.y, c.x) if eksen == "z" else math.atan2(c.z, c.x)
        p.material_index = int(((a + math.pi) / (2 * math.pi)) * n) % len(mats)


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


def koni(konum, r, h, mat, r2=0.0, v=32):
    bpy.ops.mesh.primitive_cone_add(vertices=v, radius1=r, radius2=r2, depth=h, location=(konum[0], konum[1], konum[2] + h / 2))
    o = bpy.context.active_object; o.data.materials.append(mat); bpy.ops.object.shade_smooth()
    return o


# ------------------------------------------------------------------ DAG (her iki katmanda; serit sahnesinde uzak kisim holdout)
def dag(serit_modu, rnd):
    kar = mat_kar("kar")
    duz("kar_yakin", -90, 90, -4, GECIS, 0, kar)
    duz("kar_uzak", -400, 400, GECIS, 600, 0, kar)
    # zirve sirti: pistin iki yaninda yukselen kar tepeleri (ufku kapatir, ekran dolu)
    for (x, y, r, h) in ((-34, 60, 30, 9), (36, 70, 34, 11), (-70, 90, 40, 14), (78, 95, 44, 15), (0, 120, 50, 8)):
        k = kure((x, y, -h * 0.4), r, kar, sub=4); k.scale = (1.0, 0.6, h / r)
    siradaglar(rnd)
    gok_ogeleri(rnd)
    teleferik()
    # pistin iki yaninda cam ormani (koyu doygun yesil + kar sapkali)
    for s in (-1, 1):
        for k, (x, y, h) in enumerate(((6.6, 10.5, 3.6), (8.4, 13.5, 4.6), (10.8, 11.0, 3.4), (12.6, 16.0, 5.2), (15.5, 12.5, 4.0),
                                        (18.5, 17.0, 5.6), (21.5, 13.5, 4.2), (25.0, 18.0, 6.0), (28.5, 14.5, 4.6), (32.0, 20.0, 6.4),
                                        (9.5, 20.0, 5.0), (14.0, 24.0, 6.2), (20.0, 26.0, 6.6), (27.0, 30.0, 7.0))):
            cam((s * x + rnd.uniform(-0.4, 0.4), y + rnd.uniform(-0.6, 0.6), 0), h * rnd.uniform(0.9, 1.1), rnd)
    dag_evi((-9.5, 22.0), 1.0, "#e8343f"); dag_evi((11.5, 27.0), 1.2, "#1e8cff"); dag_evi((-17.0, 33.0), 1.3, "#ffb21e")
    kar_adam((-5.4, 14.6), 1.0, "#ff3b4e"); kar_adam((5.8, 15.6), 0.9, "#8a5aff")
    for (x, y, rk) in ((-6.8, 12.4, 0), (7.4, 13.0, 2), (-4.6, 18.5, 5), (4.4, 19.5, 3)):
        kayak_cifti((x, y), CANLI[rk], CANLI[(rk + 4) % 8])
    kizak((-7.8, 16.6), "#ff3b4e"); kizak((8.6, 17.6), "#2fd06a")
    if serit_modu:                                               # yakin kar disinda her parca holdout
        for o in bpy.data.objects:
            if o.type == "MESH" and o.name.split(".")[0] not in ("kar_yakin",):
                o.is_holdout = True


def siradaglar(rnd):
    """uzak sira daglar: doygun mor-mavi kaya govde + kar sapka; arkada daha soluk degil, daha mavi (hava derinligi rengi)"""
    for (x, y, r, h, renk) in ((-230, 420, 120, 150, "#4a5fd0"), (-90, 470, 140, 200, "#3f52c4"), (60, 440, 110, 165, "#5468dc"),
                               (200, 480, 150, 210, "#3a4cbc"), (330, 430, 110, 140, "#4a5fd0"), (-360, 460, 130, 170, "#4458cc"),
                               (-160, 340, 80, 95, "#6a62e0"), (130, 330, 85, 105, "#6f5ee0")):
        kaya = mat_pbr("kaya" + renk, renk, 0.55, kaplama=0.2, bump=(0.05, 0.6))
        koni((x, y, 0), r, h, kaya, v=9)
        oran = 0.42
        sap = koni((x, y, h * (1 - oran) - 0.5), r * oran * 1.03, h * oran + 0.6, mat_kar("kar_sap"), v=9)
        sap.rotation_euler = (0, 0, 0)


def cam(taban, boy, rnd):
    """tombul cam: uc kat koni (koyu doygun yesil, cilali) + her katin ust kenarinda kar tabakasi + kahve govde"""
    x, y, z = taban
    gv = mat_pbr("cam_g", "#7a3f1e", 0.6)
    boru((x, y, z), (x, y, z + boy * 0.25), boy * 0.06, gv)
    yes = (mat_pbr("cam1", "#0f8a46", 0.4, kaplama=0.35), mat_pbr("cam2", "#0b7a3c", 0.4, kaplama=0.35))
    kr = mat_kar("cam_kar", dalga=0.05)
    for i in range(3):
        t = i / 3
        r = boy * (0.38 - 0.09 * i); h = boy * (0.42 - 0.06 * i); z0 = z + boy * (0.18 + 0.24 * t)
        koni((x, y, z0), r, h, yes[i % 2], v=16)
        koni((x, y, z0 + h * 0.55), r * 0.5, h * 0.47, kr, v=16)      # ust kenarda kar sapka
    kure((x, y, z + boy * 1.0), boy * 0.04, kr)


def dag_evi(xy, olcek, cati_renk):
    x, y = xy; s = olcek
    ah = mat_pbr("ev_a", "#b0602e", 0.5, kaplama=0.3, bump=(30, 0.2))
    kutu("ev", (x, y, 1.1 * s), (3.0 * s, 2.4 * s, 2.2 * s), ah, egim=0.08 * s)
    kr = mat_kar("ev_kar", dalga=0.04); ct = mat_pbr("cati" + cati_renk, cati_renk, 0.3, kaplama=0.7)
    for sy in (-1, 1):
        o = kutu("cati", (x, y + sy * 0.75 * s, 2.75 * s), (3.5 * s, 1.75 * s, 0.18 * s), ct, egim=0.05 * s)
        o.rotation_euler = (math.radians(sy * 38), 0, 0)
        k = kutu("cati_kar", (x, y + sy * 0.75 * s, 2.92 * s), (3.55 * s, 1.6 * s, 0.16 * s), kr, egim=0.07 * s)
        k.rotation_euler = (math.radians(sy * 38), 0, 0)
    pen = mat_emis("ev_pen", lin(hex3("#ffc85a")), 2.2)       # icerde yanan lamba (kendi isigi olan nesne, §4)
    for dx in (-0.75, 0.75):
        kutu("pen", (x + dx * s, y - 1.22 * s, 1.3 * s), (0.6 * s, 0.04, 0.6 * s), pen, egim=0)
    kutu("kapi_e", (x, y - 1.22 * s, 0.55 * s), (0.6 * s, 0.05, 1.1 * s), mat_pbr("ev_k", "#6a3214", 0.5), egim=0)
    boru((x + 0.9 * s, y + 0.3 * s, 2.6 * s), (x + 0.9 * s, y + 0.3 * s, 3.7 * s), 0.18 * s, mat_pbr("baca", "#9a3a2a", 0.6))


def kar_adam(xy, s, atki):
    x, y = xy
    kr = mat_kar("adam", "#ffffff", "#e6f2ff", purluk=0.45, dalga=0.03)
    kure((x, y, 0.45 * s), 0.5 * s, kr); kure((x, y, 1.15 * s), 0.36 * s, kr); kure((x, y, 1.68 * s), 0.26 * s, kr)
    bpy.ops.mesh.primitive_cone_add(radius1=0.06 * s, depth=0.32 * s, location=(x, y - 0.36 * s, 1.68 * s), rotation=(math.radians(90), 0, 0))
    bpy.context.active_object.data.materials.append(mat_pbr("havuc", "#ff7a14", 0.35, kaplama=0.5))
    for dx in (-0.09, 0.09):
        kure((x + dx * s, y - 0.23 * s, 1.76 * s), 0.035 * s, mat_pbr("komur", "#15171a", 0.3, kaplama=0.6))
    bpy.ops.mesh.primitive_torus_add(major_radius=0.27 * s, minor_radius=0.07 * s, location=(x, y, 1.43 * s))
    o = bpy.context.active_object; bpy.ops.object.shade_smooth()
    renk_dilimli(o, [mat_pbr("atki" + atki, atki, 0.6, bump=(80, 0.2)), mat_pbr("atki_b", "#ffffff", 0.6)], 10)
    koni((x, y, 1.88 * s), 0.24 * s, 0.32 * s, mat_pbr("bere" + atki, atki, 0.6, bump=(80, 0.2)), r2=0.05 * s)
    kure((x, y, 2.24 * s), 0.07 * s, mat_pbr("ponpon", "#ffffff", 0.7))
    for sx in (-1, 1):
        boru((x + sx * 0.3 * s, y, 1.2 * s), (x + sx * 0.75 * s, y, 1.5 * s), 0.025 * s, mat_pbr("dal", "#6b3d1e", 0.6))


def kayak_cifti(xy, r1, r2):
    x, y = xy
    for dx, renk in ((-0.12, r1), (0.12, r1)):
        k = kutu("kayak", (x + dx, y, 0.85), (0.1, 0.04, 1.7), mat_pbr("kay" + renk, renk, 0.2, kaplama=1.0), egim=0.02, seg=2)
        k.rotation_euler = (0, math.radians(dx * 30), 0)
    for dx in (-0.4, 0.4):
        boru((x + dx, y + 0.1, 0), (x + dx * 1.2, y + 0.1, 1.25), 0.018, mat_pbr("baston" + r2, r2, 0.3, metal=0.4))


def kizak(xy, renk):
    x, y = xy
    kutu("kizak", (x, y, 0.28), (0.7, 1.3, 0.08), mat_pbr("kiz" + renk, renk, 0.25, kaplama=0.9), egim=0.03)
    for dx in (-0.32, 0.32):
        boru((x + dx, y - 0.75, 0.05), (x + dx, y + 0.65, 0.05), 0.035, mat_pbr("kiz_m", "#d8dde3", 0.2, metal=1.0))
        boru((x + dx, y - 0.75, 0.05), (x + dx, y - 0.85, 0.32), 0.035, mat_pbr("kiz_m2", "#d8dde3", 0.2, metal=1.0))


def teleferik():
    """iki halat hatti kadrajin ustunden gecer; renkli tombul kabinler (gok dolu kurali)"""
    cel = mat_pbr("tel_kule", "#ffcc1e", 0.3, metal=0.4, kaplama=0.5)
    hal = mat_pbr("halat", "#2a2e36", 0.5, metal=0.6)
    for (a, b, renkler) in (((-70, 45, 34), (70, 90, 58), ("#ff3b4e", "#1e9cff", "#ffcc1e", "#2fd06a", "#ff4fc0")),
                            ((-90, 120, 70), (60, 60, 40), ("#ff8a1e", "#8a5aff", "#20d6d0", "#ff3b4e"))):
        boru(a, b, 0.09, hal)
        for p in (a, b):
            boru((p[0], p[1], 0), (p[0], p[1], p[2]), 0.9, cel)
            kutu("kule_bas", (p[0], p[1], p[2] + 0.4), (4.5, 1.2, 0.8), cel, egim=0.2)
        A, B = Vector(a), Vector(b)
        for i, renk in enumerate(renkler):
            t = (i + 0.6) / (len(renkler) + 0.2)
            c = A.lerp(B, t)
            boru(c, c + Vector((0, 0, -2.2)), 0.08, hal)
            kab = mat_pbr("kab" + renk, renk, 0.2, kaplama=1.0)
            kutu("kabin", tuple(c + Vector((0, 0, -3.6))), (2.6, 2.2, 2.4), kab, egim=0.5, seg=5)
            kutu("kabin_cam", tuple(c + Vector((0, -1.12, -3.35))), (2.0, 0.05, 1.0), mat_pbr("kab_cam", "#1d3a5c", 0.08, kaplama=1.0), egim=0.1)
            kutu("kabin_cati", tuple(c + Vector((0, 0, -2.3))), (2.7, 2.3, 0.35), mat_kar("kab_kar", dalga=0.03), egim=0.15)


def bulut(merkez, olcek, rnd):
    beyaz = mat_pbr("bulut", "#ffffff", 0.85)
    x, y, z = merkez
    for k in range(9):
        r = olcek * rnd.uniform(0.45, 0.85)
        dx = rnd.uniform(-1.5, 1.5) * olcek; dz = rnd.uniform(-0.2, 0.55) * olcek * (1 - abs(dx) / (2 * olcek))
        b = kure((x + dx, y + rnd.uniform(-0.4, 0.4) * olcek, z + dz), r, beyaz, sub=3); b.scale = (1.15, 0.8, 0.9)
    kure((x, y, z - 0.25 * olcek), olcek * 0.75, beyaz).scale = (2.4, 0.8, 0.45)


def parasut(konum, olcek, renkler, rnd):
    """yamac parasutu: kavisli kanat (dilim dilim renkli) + ipler + kucuk pilot"""
    x, y, z = konum
    bpy.ops.mesh.primitive_uv_sphere_add(radius=olcek, location=(0, 0, 0), segments=32, ring_count=16)
    o = bpy.context.active_object; bpy.ops.object.shade_smooth()
    o.scale = (1.0, 0.28, 0.32); bpy.ops.object.transform_apply(scale=True)
    import bmesh
    bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < olcek * 0.12], context="VERTS")
    bm.to_mesh(o.data); bm.free()
    renk_dilimli(o, [mat_pbr("par%d%s" % (i, c), c, 0.35, kaplama=0.5) for i, c in enumerate(renkler)], 10, eksen="y")
    o.modifiers.new("k", "SOLIDIFY").thickness = 0.03 * olcek
    o.location = (x, y, z); o.rotation_euler = (0, rnd.uniform(-0.25, 0.25), 0)
    ip = mat_pbr("par_ip", "#3a3a3a", 0.6)
    for dx in (-0.8, -0.3, 0.3, 0.8):
        boru((x + dx * olcek, y, z + 0.1 * olcek), (x, y, z - 1.4 * olcek), 0.006 * olcek, ip)
    kure((x, y, z - 1.5 * olcek), 0.12 * olcek, mat_pbr("pilot", renkler[0], 0.4)).scale = (1.0, 1.0, 1.6)


def balon(konum, olcek):
    x, y, z = konum
    bpy.ops.mesh.primitive_uv_sphere_add(radius=olcek, location=(0, 0, 0), segments=24, ring_count=14)
    o = bpy.context.active_object; bpy.ops.object.shade_smooth()
    renk_dilimli(o, [mat_pbr("hb%d" % i, c, 0.3, kaplama=0.6) for i, c in enumerate(("#ff3b4e", "#ffcc1e", "#1e9cff", "#ff8a1e"))], 12)
    o.location = (x, y, z); o.scale = (1.0, 1.0, 1.18)
    kutu("sepet", (x, y, z - olcek * 1.75), (olcek * 0.35, olcek * 0.35, olcek * 0.28), mat_pbr("sepet", "#9a5a2a", 0.7), egim=0.02 * olcek)


def gok_ogeleri(rnd):
    """ekran dolu kurali (md. 7): bulut kumeleri butun gok boyunca, yamac parasutleri, sicak hava balonu"""
    for (x, y, z, o) in ((-150, 300, 140, 16), (-60, 340, 175, 20), (40, 320, 150, 17), (140, 290, 130, 15), (230, 360, 185, 22),
                         (-240, 360, 190, 22), (-100, 240, 95, 11), (95, 250, 100, 12), (0, 380, 210, 20), (-30, 260, 110, 10),
                         (190, 240, 85, 9), (-200, 270, 88, 10), (60, 420, 240, 26), (-140, 420, 250, 26)):
        bulut((x, y, z), o, rnd)
    parasut((-14, 52, 20), 2.6, ("#ff3b4e", "#ffcc1e", "#ffffff"), rnd)
    parasut((16, 64, 25), 3.0, ("#1e9cff", "#20d6d0", "#ffffff"), rnd)
    parasut((-4, 95, 34), 3.6, ("#ff4fc0", "#8a5aff", "#ffcc1e"), rnd)
    parasut((30, 110, 42), 3.4, ("#2fd06a", "#ffcc1e", "#ff8a1e"), rnd)
    balon((-52, 170, 62), 6.0); balon((60, 210, 80), 7.0)


# ------------------------------------------------------------------ SERIT: buz pist + kar setleri + slalom bayraklari + OUT kar yiginlari + kapi
def serit_esyalari(rnd):
    duz("buz", -PIST, PIST, -4, KAP["y"] + 0.4, 0.008, mat_buz())
    kr = mat_kar("set", dalga=0.08)
    for s in (-1, 1):                                            # pist kenarinda tombul kar seti
        y = -3.4
        while y < KAP["y"] - 0.2:
            k = kure((s * (PIST + 0.25), y, -0.05), rnd.uniform(0.42, 0.55), kr, sub=3); k.scale = (0.9, 1.4, 0.55); y += 0.9
    bay = {-1: mat_pbr("bay_m", MAVI, 0.3, kaplama=0.6), 1: mat_pbr("bay_p", PEMBE, 0.3, kaplama=0.6)}
    dir_ = mat_pbr("bay_d", "#ffffff", 0.3, kaplama=0.6)
    for s in (-1, 1):                                            # slalom bayraklari: solda mavi, sagda pembe (P1/P2 tarafi)
        for y in (1.6, 4.0, 6.4):
            x = s * (PIST + 0.8)
            boru((x, y, 0), (x, y, 1.5), 0.03, dir_)
            me = bpy.data.meshes.new("bay"); me.from_pydata([(x, y, 1.48), (x - s * 0.7, y, 1.3), (x, y, 1.0)], [], [[0, 1, 2]]); me.update()
            o = bpy.data.objects.new("bay", me); bpy.context.collection.objects.link(o); o.data.materials.append(bay[s])
            o.modifiers.new("k", "SOLIDIFY").thickness = 0.02
    ok = mat_pbr("ok", "#ffcc1e", 0.3, kaplama=0.7)             # buz ustunde sari yon oklari (seri sabiti)
    for x in (-1.7, 1.7):
        for y in (4.6, 6.2):
            nok = [(x - 0.6, y - 0.4), (x, y), (x + 0.6, y - 0.4), (x + 0.6, y - 0.68), (x, y - 0.28), (x - 0.6, y - 0.68)]
            me = bpy.data.meshes.new("ok"); me.from_pydata([(a, b, 0.016) for a, b in nok], [], [list(range(6))]); me.update()
            o = bpy.data.objects.new("ok", me); bpy.context.collection.objects.link(o); o.data.materials.append(ok)
            o.modifiers.new("k", "SOLIDIFY").thickness = 0.02
    # OUT ani: iki dis tarafta buyuk yumusak kar yigini (karakterler buraya gomulur)
    yg = mat_kar("yigin", "#ffffff", "#dceeff", dalga=0.1)
    for s in (-1, 1):
        y_ = kure((s * 5.4, 5.0, -0.2), 1.25, yg, sub=4); y_.scale = (1.0, 1.7, 0.55)
        kure((s * 5.0, 6.1, -0.1), 0.7, yg, sub=3).scale = (1.0, 1.2, 0.6)
    # dis tarafta kayak / kar esyalari
    kayak_cifti((-6.9, 8.6), "#ff3b4e", "#ffcc1e"); kayak_cifti((7.0, 8.2), "#1e9cff", "#2fd06a")
    kar_adam((-7.6, 10.2), 0.8, "#2fd06a"); kizak((7.8, 10.0), "#ffcc1e")


def kapi():
    """buz kristali kemer: tombul turkuaz cilali direkler + kar sapkalar + kirmizi-beyaz seritli halkalar; ustte sonuk LED tabela; ampul dizisi"""
    Y, W_, H_, K = KAP["y"], KAP["w"], KAP["h"], KAP["kalin"]
    buz = mat_pbr("kapi_buz", "#22d4ff", 0.08, kaplama=1.0)
    kir = mat_pbr("kapi_k", "#ff3b4e", 0.2, kaplama=1.0); bey = mat_pbr("kapi_b", "#ffffff", 0.2, kaplama=1.0)
    kr = mat_kar("kapi_kar", dalga=0.04)
    xk = W_ / 2 + K / 2
    for s in (-1, 1):
        yuvarlak_kutu("direk", (s * xk, Y, (H_ + K) / 2), (K, K, H_ + K), buz, egim=0.24, seg=6)
        for i, z in enumerate((0.6, 1.4, 2.2, 3.0)):
            yuvarlak_kutu("halka", (s * xk, Y, z), (K + 0.05, K + 0.05, 0.16), kir if i % 2 == 0 else bey, egim=0.06, seg=3)
        k = kure((s * xk, Y, -0.05), 0.55, kr); k.scale = (1.1, 1.1, 0.35)
        cam((s * (xk + 1.1), Y + 0.4, 0), 2.6, random.Random(5 + s))
    yuvarlak_kutu("kiris", (0, Y, H_ + K / 2), (W_ + 2 * K, K, K), buz, egim=0.24, seg=6)
    yuvarlak_kutu("kiris_kar", (0, Y, H_ + K + 0.08), (W_ + 2 * K + 0.1, K + 0.12, 0.22), kr, egim=0.1, seg=4)
    for i in range(9):                                           # kirisin altinda buz sarkitlari
        x = -W_ / 2 + 0.3 + i * (W_ - 0.6) / 8
        bpy.ops.mesh.primitive_cone_add(radius1=0.09, depth=0.38 + 0.12 * (i % 3), location=(x, Y - 0.05, H_ - 0.18 - 0.06 * (i % 3)), rotation=(math.radians(180), 0, 0), vertices=10)
        bpy.context.active_object.data.materials.append(buz); bpy.ops.object.shade_smooth()
    yuvarlak_kutu("tabela", (0, Y, H_ + K + 0.75), (W_ * 0.6, 0.2, 0.7), mat_pbr("tabela", "#15171a", 0.35, metal=0.4), egim=0.05, seg=3)
    me = bpy.data.meshes.new("led_yuz"); a, b = W_ * 0.28, 0.28; z0 = H_ + K + 0.75
    me.from_pydata([(-a, Y - 0.11, z0 - b), (a, Y - 0.11, z0 - b), (a, Y - 0.11, z0 + b), (-a, Y - 0.11, z0 + b)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("led_yuz", me); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat_emis("led_yuz", lin(hex3("#0a3a6a")), 1.2))
    for s in (-1, 1):
        boru((s * W_ * 0.22, Y, H_ + K + 0.2), (s * W_ * 0.22, Y, H_ + K + 0.42), 0.02, mat_pbr("tel", "#cfd3d8", 0.3, metal=1.0))


def serit_katmani():
    sc = dag_sahnesi(1920, 1080, True)
    kam = kamera(sc)
    rnd = random.Random(27)
    isiklar()
    dag(True, random.Random(27))
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
        q = world_to_camera_view(sc, kam, Vector((-ic + i * 2 * ic / 22, Y - 0.35, H_ + 0.05)))
        YERLESIM[ON_EK + "ampul_p1"].append([round(q.x * 1920, 1), round((1 - q.y) * 1080, 1)])
    mk = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-5.4, 5.0, 0.3), (5.4, 5.0, 0.3), (0, GECIS, 0))]
    YERLESIM["dag"] = {"yigin_sol_x": round(mk[0].x * 1920, 1), "yigin_sag_x": round(mk[1].x * 1920, 1),
                       "yigin_y": round((1 - mk[0].y) * 1080, 1), "gecis_y": round((1 - mk[2].y) * 1080, 1)}
    YERLESIM["yol"] = {"y_kapi": Y, "genislik": PIST * 2, "kam": KAM, "serit_w": 1920}
    log("aciklik", YERLESIM[ON_EK + "aciklik_p1"], YERLESIM["dag"])
    yaz(sc, ON_EK + "serit.png")


def gok_katmani(ad):
    sc = dag_sahnesi(1920, 1080, False)
    kamera(sc)
    isiklar()
    dag(False, random.Random(27))
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
log("bitti (dag)", YERLESIM.get(ON_EK + "aciklik_p1"))
