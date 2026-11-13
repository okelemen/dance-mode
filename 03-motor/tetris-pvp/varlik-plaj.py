"""HUMAN TETRIS 26. video (REFERANSSIZ, 1v1) - GUNDUZ TROPIK PLAJ, CILALI 3D OYUN GORUNUMU. varlik.py calistirir (--mod plaj).

POZ-DUVARI TALIMATLAR §2b 3. mekan (kum, palmiye, dalga, gunes; OUT ani: kuma yuvarlanir) + §4 CILALI 3D OYUN GORUNUMU
(25'ten beri): canli doygun renk, tombul hatlar, parlak plastik / cilali yuzey, gercek isik-golge-parlama (Cycles), foto dokusu yok,
isiksiz duz renk (emission) yuzey yok. Gok dolu (Masaustu md. 7): bulut kumeleri, marti, ucurtma, sicak hava balonu.

Katmanlar 25 ile ayni (motor uyumu): gok.png = plajin uzak kismi + deniz + gok, serit-p1/p2.png = oyuncunun yakin kumu + serit
esyalari + kapi. Isik iki katmanda ayni olsun diye butun plaj serit sahnesinde de kurulur, uzak kismi holdout.
Gecis cizgisi y = GECIS. OUT ani motorda: karakter dis taraftaki kum yiginina yuvarlanir, kum sicrar.
Telif: genel plaj ogeleri; yazi, logo, marka yok.

Ciktilar: gok.png, serit-p1/p2.png, panel-p1/p2.png, yerlesim.json; kapak modu (--yalniz kapak): kapak-gok.png, kapak-serit-p1/p2.png
"""

import random
YERLESIM.clear()
KAPAK = YALNIZ == "kapak"
POZLAMA = float(arg("--pozlama", arg("--kapak-pozlama", "0")))
GUNES = float(arg("--gunes", "3.0"))
ON_EK = "kapak-" if KAPAK else ""
KAP = {"y": 8.0, "w": 3.4, "h": 3.7, "kalin": 0.34}
KAM = {"z": 2.3, "egim": 5.0, "lens": 18.0, "sensor": 24.0}
if KAPAK:
    KAM.update({"z": float(arg("--kapak-z", "2.0")), "egim": float(arg("--kapak-egim", "3.0")), "lens": float(arg("--kapak-lens", "16.0"))})
YOL_YARI = 2.6
GECIS = 11.0            # serit kumu burada biter, otesi gok.png
SAHIL = 19.0            # deniz kiyisi (islak kum -> kopuk -> deniz)
SERIT = {
    "p1": {"ana": "#1e8cff", "koyu": "#0a3fa8", "acik": "#8cc8ff"},
    "p2": {"ana": "#ff3aa8", "koyu": "#a8105e", "acik": "#ffa6d6"},
}
CANLI = ("#ff3b4e", "#ffcc1e", "#1e9cff", "#2fd06a", "#ff4fc0", "#ff8a1e", "#8a5aff", "#20d6d0")


# ------------------------------------------------------------------ sahne / isik
def plaj_sahnesi(w, h, saydam):
    sc = bos_sahne(w=w, h=h, saydam=saydam, ornek=ORNEK, doygun=True)
    sc.view_settings.view_transform = "Standard"           # 25 notu: AgX doygun renkleri pastele ceker
    sc.view_settings.exposure = POZLAMA
    sc.cycles.max_bounces = 6; sc.cycles.diffuse_bounces = 3; sc.cycles.glossy_bounces = 3
    sc.cycles.transmission_bounces = 2; sc.cycles.transparent_max_bounces = 8
    sc.cycles.use_light_tree = True
    # gok: kameranin gordugu doygun mavi degrade (ufuk turkuaz -> tepe koyu mavi); aydinlatmada daha dusuk guc
    nt = sc.world.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord"); sp = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Generated"], sp.inputs[0])
    rp = nt.nodes.new("ShaderNodeValToRGB"); el = rp.color_ramp.elements
    el[0].position = 0.0; el[0].color = (*lin(hex3("#9eeaff")), 1)
    el[1].position = 0.45; el[1].color = (*lin(hex3("#1f86ff")), 1)
    e2 = el.new(0.12); e2.color = (*lin(hex3("#5cc8ff")), 1)
    nt.links.new(sp.outputs["Z"], rp.inputs[0])
    lp = nt.nodes.new("ShaderNodeLightPath")
    bg_k = nt.nodes.new("ShaderNodeBackground"); bg_k.inputs[1].default_value = 1.0
    bg_i = nt.nodes.new("ShaderNodeBackground"); bg_i.inputs[1].default_value = 0.7
    nt.links.new(rp.outputs[0], bg_k.inputs[0]); nt.links.new(rp.outputs[0], bg_i.inputs[0])
    mx = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(lp.outputs["Is Camera Ray"], mx.inputs[0])
    nt.links.new(bg_i.outputs[0], mx.inputs[1]); nt.links.new(bg_k.outputs[0], mx.inputs[2])
    o = nt.nodes.new("ShaderNodeOutputWorld"); nt.links.new(mx.outputs[0], o.inputs[0])
    # oyun gorunumu: parlama noktalarinda yumusak hare
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
    kam.data.clip_end = 1500
    return kam


def isiklar():
    # gunes kameranin arkasindan, sag ustten: on yuzler aydinlik, golgeler ileri-sola duser (oyun gorunumu)
    bpy.ops.object.light_add(type="SUN", location=(0, 0, 30))
    g = bpy.context.active_object; g.data.energy = GUNES; g.data.angle = math.radians(1.5)
    g.data.color = lin(hex3("#fff3dc"))
    g.rotation_euler = Vector((-0.40, 0.55, -0.73)).to_track_quat("-Z", "Y").to_euler()


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


def mat_kum(ad, renk1, renk2, purluk=0.8, dalga=0.18):
    """prosedurel kum: iki ton gurultu + ruzgar dalgaciklari (wave bump) + ince tane; foto dokusu yok"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    ns = nt.nodes.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value = 0.35; ns.inputs["Detail"].default_value = 3
    nt.links.new(geo.outputs["Position"], ns.inputs["Vector"])
    rp = nt.nodes.new("ShaderNodeValToRGB")
    rp.color_ramp.elements[0].position = 0.35; rp.color_ramp.elements[1].position = 0.7
    rp.color_ramp.elements[0].color = (*lin(hex3(renk1)), 1); rp.color_ramp.elements[1].color = (*lin(hex3(renk2)), 1)
    nt.links.new(ns.outputs["Fac"], rp.inputs[0]); nt.links.new(rp.outputs[0], b.inputs["Base Color"])
    wv = nt.nodes.new("ShaderNodeTexWave"); wv.wave_type = "BANDS"; wv.bands_direction = "Y"
    wv.inputs["Scale"].default_value = 0.9; wv.inputs["Distortion"].default_value = 4.0; wv.inputs["Detail"].default_value = 2
    nt.links.new(geo.outputs["Position"], wv.inputs["Vector"])
    tn = nt.nodes.new("ShaderNodeTexNoise"); tn.inputs["Scale"].default_value = 400; tn.inputs["Detail"].default_value = 2
    nt.links.new(geo.outputs["Position"], tn.inputs["Vector"])
    ad_ = nt.nodes.new("ShaderNodeMath"); ad_.operation = "ADD"
    k1 = nt.nodes.new("ShaderNodeMath"); k1.operation = "MULTIPLY"; k1.inputs[1].default_value = 1.0
    k2 = nt.nodes.new("ShaderNodeMath"); k2.operation = "MULTIPLY"; k2.inputs[1].default_value = 0.25
    nt.links.new(wv.outputs["Fac"], k1.inputs[0]); nt.links.new(tn.outputs["Fac"], k2.inputs[0])
    nt.links.new(k1.outputs[0], ad_.inputs[0]); nt.links.new(k2.outputs[0], ad_.inputs[1])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = dalga; bp.inputs["Distance"].default_value = 0.03
    nt.links.new(ad_.outputs[0], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = purluk
    return m


def mat_deniz():
    """deniz: kiyida turkuaz -> acikta koyu mavi (y'ye gore), parlak, dalga bump"""
    m = bpy.data.materials.new("deniz"); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry"); sp = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(geo.outputs["Position"], sp.inputs[0])
    mr = nt.nodes.new("ShaderNodeMapRange"); mr.inputs["From Min"].default_value = SAHIL; mr.inputs["From Max"].default_value = SAHIL + 260
    nt.links.new(sp.outputs["Y"], mr.inputs["Value"])
    pw = nt.nodes.new("ShaderNodeMath"); pw.operation = "POWER"; pw.inputs[1].default_value = 0.45
    nt.links.new(mr.outputs[0], pw.inputs[0])
    rp = nt.nodes.new("ShaderNodeValToRGB"); el = rp.color_ramp.elements
    el[0].position = 0.0; el[0].color = (*lin(hex3("#4ff0dc")), 1)
    el[1].position = 1.0; el[1].color = (*lin(hex3("#0a56c8")), 1)
    e = el.new(0.18); e.color = (*lin(hex3("#14c8e6")), 1)
    e = el.new(0.5); e.color = (*lin(hex3("#0b8ae6")), 1)
    nt.links.new(pw.outputs[0], rp.inputs[0]); nt.links.new(rp.outputs[0], b.inputs["Base Color"])
    ns = nt.nodes.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value = 0.8; ns.inputs["Detail"].default_value = 6
    mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (0.35, 1.0, 1.0)
    nt.links.new(geo.outputs["Position"], mp.inputs[0]); nt.links.new(mp.outputs[0], ns.inputs["Vector"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.35; bp.inputs["Distance"].default_value = 0.05
    nt.links.new(ns.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = 0.12; b.inputs["Coat Weight"].default_value = 0.3
    return m


def renk_dilimli(o, mats, n, eksen="z"):
    """nesnenin yuzlerini aci dilimine gore malzemelere boler (semsiye, top, can simidi, balon seritleri)"""
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


def serit_mesh(ad, noktalar, gen, z, mat):
    """kiyi kopugu: noktalar boyunca dalgali serit"""
    v = []; f = []
    for i, (x, y) in enumerate(noktalar):
        w = gen(i / (len(noktalar) - 1))
        v += [(x, y - w / 2, z), (x, y + w / 2, z)]
        if i:
            f.append([2 * i - 2, 2 * i, 2 * i + 1, 2 * i - 1])
    me = bpy.data.meshes.new(ad); me.from_pydata(v, [], f); me.update()
    o = bpy.data.objects.new(ad, me); bpy.context.collection.objects.link(o); o.data.materials.append(mat)
    return o


# ------------------------------------------------------------------ PLAJ (her iki katmanda; serit sahnesinde uzak kisim holdout)
def plaj(serit_modu, rnd):
    kum = mat_kum("kum", "#f6d595", "#f0c47c")
    duz("kum_yakin", -80, 80, -4, GECIS, 0, kum)
    duz("kum_uzak", -80, 80, GECIS, SAHIL + 2.5, 0, kum)
    islak = mat_kum("islak", "#e2ad6c", "#d89f5e", purluk=0.25, dalga=0.05)
    duz("islak", -80, 80, SAHIL - 1.4, SAHIL + 2.5, 0.004, islak)
    deniz = mat_deniz()
    duz("deniz", -900, 900, SAHIL, 900, 0.02, deniz)
    kopuk = mat_pbr("kopuk", "#ffffff", 0.35, kaplama=0.3)
    for k, (dy, gen0) in enumerate(((0.15, 0.32), (1.6, 0.16), (3.6, 0.10))):
        n = 160; faz = rnd.uniform(0, 6.28)
        nok = [(-80 + 160 * i / n, SAHIL + dy + 0.25 * math.sin(i * 0.37 + faz) + 0.12 * math.sin(i * 1.3)) for i in range(n + 1)]
        serit_mesh("kopuk", nok, lambda q, g=gen0: g * (0.6 + 0.4 * abs(math.sin(q * 41))), 0.03 + 0.002 * k, kopuk)
    adalar(rnd); yelkenli((-38, 140, 0)); yelkenli((55, 210, 0), 1.4)
    gok_ogeleri(rnd)
    # kiyi boyunca palmiye siralari (iki yan), cankurtaran kulesi ortada
    for s in (-1, 1):
        for k, (x, y, h) in enumerate(((7.0, 9.5, 6.8), (9.5, 13.0, 7.6), (12.5, 10.0, 6.2), (15.5, 15.5, 8.0), (19.0, 12.0, 7.0),
                                        (23.0, 16.0, 7.8), (27.0, 13.5, 6.6))):
            palmiye((s * x, y, 0), h, s * rnd.uniform(0.15, 0.4) * (1 if k % 2 else -1) + s * 0.25, rnd)
    cankurtaran_kulesi((0, SAHIL - 3.2, 0))
    for (x, y, rk) in ((-9.5, 16.0, 0), (10.5, 16.8, 3), (-16.0, 17.4, 5), (17.0, 14.0, 1), (-5.2, 14.2, 4), (5.4, 15.2, 6)):
        semsiye((x, y), CANLI[rk], rnd)
        sezlong((x + 0.9, y - 0.4), CANLI[(rk + 3) % 8])
    voleybol_agi((-12.5, 13.5))
    for (x, y) in ((13.2, 12.2), (13.9, 12.4), (14.6, 12.1)):
        sorf((x, y), rnd)
    kum_kalesi((-3.6, 12.6)); kum_kalesi((4.2, 13.4), 0.8)
    for (x, y, r) in ((-24, SAHIL + 0.6, 1.2), (-21.5, SAHIL + 1.4, 0.8), (25, SAHIL + 0.8, 1.4), (22.5, SAHIL + 1.6, 0.7)):
        k_ = kure((x, y, 0.1), r, mat_pbr("kaya", "#8d8a93", 0.55, kaplama=0.2), sub=3); k_.scale = (1.3, 1.0, 0.7)
    for k in range(10):
        plaj_topu((rnd.uniform(-20, 20), rnd.uniform(12, 18), 0.0), rnd.uniform(0.18, 0.26), rnd)
    if serit_modu:                                               # yakin kum disinda her parca holdout
        for o in bpy.data.objects:
            if o.type == "MESH" and o.name.split(".")[0] not in ("kum_yakin",):
                o.is_holdout = True


def palmiye(taban, boy, egilme, rnd):
    """kivrik govde (halkali iki ton), sarkik genis yapraklar (orta damarli), hindistan cevizleri"""
    x0, y0, z0 = taban
    gv1 = mat_pbr("govde1", "#a8673a", 0.6, bump=(40, 0.3)); gv2 = mat_pbr("govde2", "#8a4f2a", 0.6, bump=(40, 0.3))
    n = 14; onc = Vector((x0, y0, z0)); r0 = 0.24
    for i in range(1, n + 1):
        t = i / n
        p = Vector((x0 + egilme * boy * t * t, y0 + 0.15 * boy * t * t, z0 + boy * t))
        b_ = boru(onc, p, r0 * (1 - 0.35 * t), gv1 if i % 2 else gv2)
        onc = p
    tepe = onc
    yap = [mat_pbr("yaprak1", "#29c447", 0.4, kaplama=0.35), mat_pbr("yaprak2", "#1fa23c", 0.4, kaplama=0.35)]
    nyap = 9
    for j in range(nyap):
        a = 2 * math.pi * j / nyap + rnd.uniform(-0.15, 0.15)
        d = Vector((math.cos(a), math.sin(a), 0)); dik = Vector((-math.sin(a), math.cos(a), 0))
        L = boy * rnd.uniform(0.42, 0.52); v = []; f = []; m = 12
        for i in range(m + 1):
            t = i / m
            c = tepe + d * (L * t) + Vector((0, 0, L * (0.45 * t - 0.95 * t * t)))
            w = L * 0.17 * math.sin(math.pi * min(1.0, t * 1.1)) ** 0.7
            v += [c - dik * w + Vector((0, 0, -0.06 * w)), c + Vector((0, 0, 0.05)), c + dik * w + Vector((0, 0, -0.06 * w))]
            if i:
                q = 3 * i
                f += [[q - 3, q, q + 1, q - 2], [q - 2, q + 1, q + 2, q - 1]]
        me = bpy.data.meshes.new("yaprak"); me.from_pydata(v, [], f); me.update()
        o = bpy.data.objects.new("yaprak", me); bpy.context.collection.objects.link(o); o.data.materials.append(yap[j % 2])
        sl = o.modifiers.new("kal", "SOLIDIFY"); sl.thickness = 0.03
        for p in o.data.polygons:
            p.use_smooth = True
    ce = mat_pbr("ceviz", "#6b3d1e", 0.45, kaplama=0.4)
    for j in range(4):
        a = j * 1.6
        kure((tepe.x + 0.22 * math.cos(a), tepe.y + 0.22 * math.sin(a), tepe.z - 0.25), 0.16, ce)


def cankurtaran_kulesi(konum):
    x, y, z = konum
    ahsap = mat_pbr("kule_a", "#f4f0e6", 0.35, kaplama=0.5)
    kir = mat_pbr("kule_k", "#ff3b4e", 0.3, kaplama=0.7)
    for dx in (-1.0, 1.0):
        for dy in (-0.8, 0.8):
            boru((x + dx * 1.15, y + dy * 1.15, 0), (x + dx * 0.85, y + dy * 0.85, 2.4), 0.09, ahsap)
    kutu("kule_taban", (x, y, 2.45), (2.4, 2.2, 0.16), ahsap, egim=0.04)
    kutu("kule_kabin", (x, y + 0.2, 3.35), (2.0, 1.6, 1.6), kir, egim=0.08, seg=4)
    kutu("kule_pencere", (x, y - 0.62, 3.5), (1.5, 0.05, 0.7), mat_pbr("kule_cam", "#1d3a5c", 0.1, kaplama=1.0), egim=0.02)
    me = bpy.data.meshes.new("cati")
    me.from_pydata([(x - 1.35, y - 0.9, 4.15), (x + 1.35, y - 0.9, 4.15), (x + 1.35, y + 1.3, 4.15), (x - 1.35, y + 1.3, 4.15), (x, y + 0.2, 4.85)],
                   [], [[0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4], [0, 3, 2, 1]]); me.update()
    o = bpy.data.objects.new("cati", me); bpy.context.collection.objects.link(o)
    renk_dilimli(o, [mat_pbr("cati1", "#ffffff", 0.3, kaplama=0.6), mat_pbr("cati2", "#ff3b4e", 0.3, kaplama=0.6)], 8)
    for i in range(7):                                         # rampa / merdiven
        boru((x - 0.5, y - 1.3 - i * 0.28, 2.3 - i * 0.33), (x + 0.5, y - 1.3 - i * 0.28, 2.3 - i * 0.33), 0.04, ahsap)
    for dx in (-0.5, 0.5):
        boru((x + dx, y - 1.2, 2.45), (x + dx, y - 3.3, 0.0), 0.05, ahsap)
    boru((x + 1.2, y + 0.2, 4.1), (x + 1.2, y + 0.2, 6.2), 0.035, ahsap)
    bayrak = mat_pbr("bayrak", "#ff3b4e", 0.5)
    me = bpy.data.meshes.new("bayrak"); me.from_pydata([(x + 1.2, y + 0.2, 6.15), (x + 2.2, y + 0.2, 5.95), (x + 1.2, y + 0.2, 5.6)], [], [[0, 1, 2]]); me.update()
    o = bpy.data.objects.new("bayrak", me); bpy.context.collection.objects.link(o); o.data.materials.append(bayrak)
    o.modifiers.new("k", "SOLIDIFY").thickness = 0.02
    can_simidi((x - 1.05, y - 0.62, 3.3))


def can_simidi(konum, rot=(math.radians(90), 0, 0), r=0.32):
    bpy.ops.mesh.primitive_torus_add(major_radius=r, minor_radius=r * 0.32, location=konum, rotation=rot, major_segments=32, minor_segments=12)
    o = bpy.context.active_object; bpy.ops.object.shade_smooth()
    renk_dilimli(o, [mat_pbr("simit1", "#ffffff", 0.25, kaplama=0.8), mat_pbr("simit2", "#ff3b4e", 0.25, kaplama=0.8)], 8)
    return o


def semsiye(xy, renk, rnd):
    x, y = xy
    egik = rnd.uniform(-0.15, 0.15)
    ust = (x + egik * 2.2, y, 2.5)
    boru((x, y, 0), ust, 0.035, mat_pbr("sem_dir", "#f2f2f2", 0.3, metal=0.5))
    bpy.ops.mesh.primitive_cone_add(vertices=16, radius1=1.35, radius2=0.05, depth=0.5, location=(ust[0], ust[1], ust[2] - 0.05))
    o = bpy.context.active_object; o.rotation_euler = (0, egik * 0.4, 0); bpy.ops.object.shade_smooth()
    renk_dilimli(o, [mat_pbr("sem_a" + renk, renk, 0.3, kaplama=0.6), mat_pbr("sem_b", "#ffffff", 0.3, kaplama=0.6)], 16)


def sezlong(xy, renk):
    x, y = xy
    cer = mat_pbr("sez_c", "#ffffff", 0.3, kaplama=0.6)
    kum_ = mat_pbr("sez_" + renk, renk, 0.35, kaplama=0.5)
    kutu("sez", (x, y, 0.32), (0.62, 1.3, 0.06), kum_, egim=0.025)
    o = kutu("sez_sirt", (x, y + 0.85, 0.62), (0.62, 0.7, 0.06), kum_, egim=0.025); o.rotation_euler = (math.radians(-55), 0, 0)
    for dx in (-0.28, 0.28):
        for dy in (-0.55, 0.55):
            boru((x + dx, y + dy, 0), (x + dx, y + dy, 0.3), 0.025, cer)


def voleybol_agi(xy):
    x, y = xy
    dir_ = mat_pbr("voley_d", "#ffcc1e", 0.3, kaplama=0.6); ag = mat_pbr("voley_ag", "#20242a", 0.6)
    for dx in (-2.8, 2.8):
        boru((x + dx, y, 0), (x + dx, y, 2.5), 0.05, dir_)
    kutu("ag_ust", (x, y, 2.38), (5.6, 0.03, 0.08), mat_pbr("ag_bant", "#ffffff", 0.4), egim=0)
    for i in range(29):
        boru((x - 2.8 + i * 0.2, y, 1.6), (x - 2.8 + i * 0.2, y, 2.34), 0.006, ag)
    for k in range(4):
        boru((x - 2.8, y, 1.62 + k * 0.24), (x + 2.8, y, 1.62 + k * 0.24), 0.006, ag)
    plaj_topu((x + 1.6, y - 1.0, 0), 0.22, random.Random(3))


def sorf(xy, rnd):
    x, y = xy
    renk = rnd.choice(CANLI)
    k = kure((x, y, 1.0), 1.0, mat_pbr("sorf_" + renk, renk, 0.2, kaplama=1.0), sub=3)
    k.scale = (0.28, 0.05, 1.05); k.rotation_euler = (math.radians(rnd.uniform(-8, 8)), 0, math.radians(rnd.uniform(-10, 10)))
    s_ = kutu("sorf_serit", (x, y - 0.04, 1.0), (0.06, 0.01, 1.7), mat_pbr("sorf_s", "#ffffff", 0.3, kaplama=0.8), egim=0.004, seg=1)
    s_.rotation_euler = k.rotation_euler


def kum_kalesi(xy, olcek=1.0):
    x, y = xy
    km = mat_kum("kale", "#ecb876", "#e2a965", purluk=0.7, dalga=0.05)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.55 * olcek, depth=0.5 * olcek, location=(x, y, 0.25 * olcek)); bpy.context.active_object.data.materials.append(km)
    for dx in (-0.45, 0.45):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.22 * olcek, depth=0.85 * olcek, location=(x + dx * olcek, y, 0.42 * olcek)); bpy.context.active_object.data.materials.append(km)
        bpy.ops.mesh.primitive_cone_add(radius1=0.26 * olcek, depth=0.35 * olcek, location=(x + dx * olcek, y, 1.0 * olcek)); bpy.context.active_object.data.materials.append(km)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.28 * olcek, depth=0.5 * olcek, location=(x, y, 0.75 * olcek)); bpy.context.active_object.data.materials.append(km)
    boru((x, y, 1.0 * olcek), (x, y, 1.5 * olcek), 0.012, mat_pbr("kale_d", "#ffffff", 0.4))
    me = bpy.data.meshes.new("kale_b"); me.from_pydata([(x, y, 1.5 * olcek), (x + 0.3, y, 1.42 * olcek), (x, y, 1.33 * olcek)], [], [[0, 1, 2]]); me.update()
    o = bpy.data.objects.new("kale_b", me); bpy.context.collection.objects.link(o); o.data.materials.append(mat_pbr("kale_bb", "#ff3b4e", 0.5))


def plaj_topu(konum, r, rnd):
    x, y, z = konum
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=(0, 0, 0), segments=24, ring_count=12)
    o = bpy.context.active_object; bpy.ops.object.shade_smooth()
    mats = [mat_pbr("top_%d" % i, c, 0.15, kaplama=1.0) for i, c in enumerate(("#ff3b4e", "#ffffff", "#1e9cff", "#ffcc1e", "#2fd06a", "#ffffff"))]
    renk_dilimli(o, mats, 6)
    o.location = (x, y, z + r); o.rotation_euler = (rnd.uniform(0, 3), rnd.uniform(0, 3), 0)


def adalar(rnd):
    ye = mat_pbr("ada", "#2fb14a", 0.6, bump=(2, 0.4)); ka = mat_kum("ada_kum", "#f2cf8c", "#eac07a", dalga=0.02)
    for (x, y, r, h) in ((-120, 330, 40, 14), (-70, 360, 26, 9), (150, 380, 55, 20), (90, 300, 18, 6)):
        k = kure((x, y, -h * 0.25), r, ye, sub=4); k.scale = (1.0, 0.5, h / r)
        k2 = kure((x, y - 2, -0.6), r * 1.08, ka, sub=4); k2.scale = (1.0, 0.5, 0.06)
        for j in range(int(r / 7)):
            palmiye((x + rnd.uniform(-r * 0.6, r * 0.6), y - r * 0.3, h * 0.35), rnd.uniform(5, 8), rnd.uniform(-0.3, 0.3), rnd)


def yelkenli(konum, olcek=1.0):
    x, y, z = konum
    g = kure((x, y, 0.4 * olcek), 3.0 * olcek, mat_pbr("tekne", "#ffffff", 0.3, kaplama=0.7), sub=3); g.scale = (1.0, 0.32, 0.25)
    boru((x, y, 0.5 * olcek), (x, y, 9 * olcek), 0.1 * olcek, mat_pbr("direk", "#c9cdd2", 0.3, metal=0.8))
    for (x1, renk) in ((2.6, "#ffffff"), (-2.0, "#ff3b4e")):
        me = bpy.data.meshes.new("yelken")
        me.from_pydata([(x, y, 9 * olcek), (x, y, 1.2 * olcek), (x + x1 * olcek, y, 1.2 * olcek)], [], [[0, 1, 2]]); me.update()
        o = bpy.data.objects.new("yelken", me); bpy.context.collection.objects.link(o); o.data.materials.append(mat_pbr("yel" + renk, renk, 0.45))
        o.modifiers.new("k", "SOLIDIFY").thickness = 0.05


def bulut(merkez, olcek, rnd):
    beyaz = mat_pbr("bulut", "#ffffff", 0.85)
    x, y, z = merkez
    for k in range(9):
        r = olcek * rnd.uniform(0.45, 0.85)
        dx = rnd.uniform(-1.5, 1.5) * olcek; dz = rnd.uniform(-0.2, 0.55) * olcek * (1 - abs(dx) / (2 * olcek))
        b = kure((x + dx, y + rnd.uniform(-0.4, 0.4) * olcek, z + dz), r, beyaz, sub=3); b.scale = (1.15, 0.8, 0.9)
    kure((x, y, z - 0.25 * olcek), olcek * 0.75, beyaz).scale = (2.4, 0.8, 0.45)     # duz taban


def marti(konum, olcek, rnd):
    x, y, z = konum
    k = rnd.uniform(0.2, 0.55)
    v = [(x, y, z), (x - 1.0 * olcek, y, z + k * olcek), (x - 1.9 * olcek, y + 0.1, z + (k - 0.25) * olcek),
         (x + 1.0 * olcek, y, z + k * olcek), (x + 1.9 * olcek, y + 0.1, z + (k - 0.25) * olcek), (x, y + 0.5 * olcek, z)]
    me = bpy.data.meshes.new("marti"); me.from_pydata(v, [], [[0, 1, 2, 5], [0, 5, 4, 3]]); me.update()
    o = bpy.data.objects.new("marti", me); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat_pbr("marti", "#ffffff", 0.5)); o.modifiers.new("k", "SOLIDIFY").thickness = 0.06 * olcek
    kure((x, y + 0.2 * olcek, z), 0.22 * olcek, mat_pbr("marti_g", "#f4f4f4", 0.5)).scale = (0.8, 1.8, 0.8)


def ucurtma(konum, renk1, renk2, olcek=1.0):
    x, y, z = konum
    v = [(x, y, z + 1.2 * olcek), (x + 0.85 * olcek, y, z), (x, y, z - 1.5 * olcek), (x - 0.85 * olcek, y, z), (x, y, z)]
    me = bpy.data.meshes.new("ucurtma"); me.from_pydata(v, [], [[0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4]]); me.update()
    o = bpy.data.objects.new("ucurtma", me); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat_pbr("uc1" + renk1, renk1, 0.35, kaplama=0.5)); o.data.materials.append(mat_pbr("uc2" + renk2, renk2, 0.35, kaplama=0.5))
    for i, p in enumerate(o.data.polygons):
        p.material_index = i % 2
    o.modifiers.new("k", "SOLIDIFY").thickness = 0.03
    ip = mat_pbr("uc_ip", "#ffffff", 0.5)
    onc = (x, y, z - 1.5 * olcek)
    for i in range(1, 7):
        p = (x + 0.35 * olcek * math.sin(i * 1.1), y, z - 1.5 * olcek - i * 0.55 * olcek)
        boru(onc, p, 0.012 * olcek, ip)
        k = kure(p, 0.13 * olcek, mat_pbr("uc_k%d" % (i % 3), CANLI[(i * 3) % 8], 0.35, kaplama=0.5)); k.scale = (1.6, 0.4, 0.7)
        onc = p


def balon(konum, olcek):
    x, y, z = konum
    bpy.ops.mesh.primitive_uv_sphere_add(radius=olcek, location=(0, 0, 0), segments=24, ring_count=14)
    o = bpy.context.active_object; bpy.ops.object.shade_smooth()
    renk_dilimli(o, [mat_pbr("hb%d" % i, c, 0.3, kaplama=0.6) for i, c in enumerate(("#ff3b4e", "#ffcc1e", "#1e9cff", "#ff8a1e"))], 12)
    o.location = (x, y, z); o.scale = (1.0, 1.0, 1.18)
    kutu("sepet", (x, y, z - olcek * 1.75), (olcek * 0.35, olcek * 0.35, olcek * 0.28), mat_pbr("sepet", "#9a5a2a", 0.7), egim=0.02 * olcek)
    for dx in (-1, 1):
        boru((x + dx * olcek * 0.17, y, z - olcek * 1.6), (x + dx * olcek * 0.45, y, z - olcek * 0.95), 0.015 * olcek, mat_pbr("halat", "#3a2a1e", 0.7))


def gok_ogeleri(rnd):
    """ekran dolu kurali (md. 7): bulut kumeleri butun gok boyunca, martilar, ucurtmalar, sicak hava balonlari"""
    for (x, y, z, o) in ((-150, 260, 70, 16), (-60, 300, 95, 20), (40, 280, 80, 17), (140, 250, 62, 15), (230, 320, 100, 22),
                         (-240, 320, 110, 22), (-100, 200, 40, 11), (95, 210, 45, 12), (0, 330, 120, 20), (-30, 220, 52, 10),
                         (190, 200, 30, 9), (-200, 230, 32, 10), (60, 360, 140, 26), (-140, 360, 150, 26)):
        bulut((x, y, z), o, rnd)
    for k in range(9):
        marti((rnd.uniform(-18, 18), rnd.uniform(26, 45), rnd.uniform(9, 17)), rnd.uniform(0.45, 0.7), rnd)
    ucurtma((-11.0, 34, 13.5), "#ff3b4e", "#ffcc1e", 1.3)
    ucurtma((12.5, 40, 15.5), "#1e9cff", "#2fd06a", 1.4)
    ucurtma((3.5, 60, 21.0), "#ff4fc0", "#8a5aff", 1.6)
    balon((-45, 130, 38), 5.0); balon((52, 160, 52), 6.0)


# ------------------------------------------------------------------ SERIT: oyuncu kumu + ip/samandira sinirlari + OUT kum yigini + kapi
def serit_esyalari(oyuncu, R, rnd):
    s_dis = -1 if oyuncu == "p1" else 1
    ip = mat_pbr("ip_" + oyuncu, "#f4f0e6", 0.6, bump=(120, 0.3))
    sam = [mat_pbr("sam_" + oyuncu, R["ana"], 0.2, kaplama=0.9), mat_pbr("sam_b", "#ffffff", 0.2, kaplama=0.9)]
    for x in (-1.6, 1.6):                                        # serit siniri: kumda ip + oyuncu renginde samandiralar
        boru((x, -4, 0.06), (x, KAP["y"] - 0.3, 0.06), 0.022, ip)
        y = -3.6; i = 0
        while y < KAP["y"] - 0.6:
            k = kure((x, y, 0.08), 0.1, sam[i % 2]); k.scale = (0.9, 1.5, 0.9); y += 0.55; i += 1
    boya = mat_pbr("ok_" + oyuncu, R["ana"], 0.35, kaplama=0.6)
    for y in (4.9, 6.4):                                          # kumda oyuncu renginde plastik yon oklari (seri sabiti)
        nok = [(-0.75, y - 0.45), (0, y), (0.75, y - 0.45), (0.75, y - 0.75), (0, y - 0.3), (-0.75, y - 0.75)]
        me = bpy.data.meshes.new("ok"); me.from_pydata([(a, b, 0.012) for a, b in nok], [], [list(range(6))]); me.update()
        o = bpy.data.objects.new("ok", me); bpy.context.collection.objects.link(o); o.data.materials.append(boya)
        o.modifiers.new("k", "SOLIDIFY").thickness = 0.02
    # OUT ani: dis tarafta yumusak kum yigini (karakter buraya yuvarlanir)
    km = mat_kum("yigin", "#f8dba0", "#f1c983", dalga=0.08)
    y_ = kure((s_dis * 2.75, 5.2, -0.15), 1.0, km, sub=4); y_.scale = (1.0, 1.8, 0.42)
    # dis tarafta plaj esyalari (havlu, kova-kurek, top / sorf, sogutucu, kum kalesi)
    if oyuncu == "p1":
        havlu((s_dis * 4.6, 6.2), R)
        kova((s_dis * 3.8, 8.4), "#ffcc1e")
        plaj_topu((s_dis * 4.2, 9.6, 0), 0.24, rnd)
        semsiye((s_dis * 5.6, 8.8), "#1e9cff", rnd)
    else:
        sogutucu((s_dis * 4.4, 6.6))
        kum_kalesi((s_dis * 3.9, 8.8), 0.75)
        sorf((s_dis * 5.6, 9.6), random.Random(7))
        semsiye((s_dis * 5.8, 7.6), "#ff3aa8", rnd)
    # ic tarafta (iki seridin ortasi, hakem yeri) kuma saplanmis kucuk cankurtaran bayragi
    boru((-s_dis * 2.6, 9.4, 0), (-s_dis * 2.6, 9.4, 1.3), 0.02, mat_pbr("bdir", "#ffffff", 0.4))
    me = bpy.data.meshes.new("ib"); me.from_pydata([(-s_dis * 2.6, 9.4, 1.3), (-s_dis * 2.6 - s_dis * 0.5, 9.4, 1.16), (-s_dis * 2.6, 9.4, 1.0)], [], [[0, 1, 2]]); me.update()
    o = bpy.data.objects.new("ib", me); bpy.context.collection.objects.link(o); o.data.materials.append(mat_pbr("ib", "#ffcc1e", 0.5))


def havlu(xy, R):
    x, y = xy
    for i, renk in enumerate((R["ana"], "#ffffff", R["ana"], "#ffffff", R["ana"])):
        kutu("havlu", (x, y - 0.8 + i * 0.4, 0.012), (1.0, 0.4, 0.02), mat_pbr("havlu%d" % i + renk, renk, 0.9, bump=(300, 0.2)), egim=0)


def kova(xy, renk):
    x, y = xy
    bpy.ops.mesh.primitive_cone_add(radius1=0.16, radius2=0.21, depth=0.3, location=(x, y, 0.15), vertices=24)
    bpy.context.active_object.data.materials.append(mat_pbr("kova", renk, 0.2, kaplama=0.9)); bpy.ops.object.shade_smooth()
    k = kutu("kurek", (x + 0.32, y - 0.1, 0.03), (0.12, 0.4, 0.03), mat_pbr("kurek", "#ff3b4e", 0.2, kaplama=0.9), egim=0.01)
    k.rotation_euler = (0, 0, 0.5)


def sogutucu(xy):
    x, y = xy
    kutu("sog", (x, y, 0.25), (0.75, 0.5, 0.5), mat_pbr("sog", "#20d6d0", 0.25, kaplama=0.8), egim=0.06)
    kutu("sog_k", (x, y, 0.53), (0.78, 0.53, 0.08), mat_pbr("sog_k", "#ffffff", 0.25, kaplama=0.8), egim=0.03)


def kapi(R):
    """sisme kemer kapi: oyuncu renginde tombul parlak direkler + beyaz serit halkalar; ustte sonuk LED tabela (motor PLAYER n yazar)"""
    Y, W_, H_, K = KAP["y"], KAP["w"], KAP["h"], KAP["kalin"]
    sisme = mat_pbr("kapi_s", R["ana"], 0.18, kaplama=1.0)
    beyaz = mat_pbr("kapi_b", "#ffffff", 0.2, kaplama=1.0)
    xk = W_ / 2 + K / 2
    for s in (-1, 1):
        yuvarlak_kutu("direk", (s * xk, Y, (H_ + K) / 2), (K, K, H_ + K), sisme, egim=0.15, seg=5)
        for z in (0.7, 1.7, 2.7):
            yuvarlak_kutu("halka", (s * xk, Y, z), (K + 0.04, K + 0.04, 0.14), beyaz, egim=0.06, seg=3)
        kum_ = mat_kum("kum_kapi", "#f6d595", "#f0c47c", dalga=0.05)
        k = kure((s * xk, Y, -0.05), 0.45, kum_); k.scale = (1.0, 1.0, 0.3)
    yuvarlak_kutu("kiris", (0, Y, H_ + K / 2), (W_ + 2 * K, K, K), sisme, egim=0.15, seg=5)
    for x in (-1.0, 0.0, 1.0):
        yuvarlak_kutu("halka_k", (x, Y, H_ + K / 2), (0.14, K + 0.04, K + 0.04), beyaz, egim=0.06, seg=3)
    yuvarlak_kutu("tabela", (0, Y, H_ + K + 0.5), (W_ * 0.85, 0.2, 0.7), mat_pbr("tabela", "#15171a", 0.35, metal=0.4), egim=0.05, seg=3)
    me = bpy.data.meshes.new("led_yuz"); a, b = W_ * 0.4, 0.28; z0 = H_ + K + 0.5
    me.from_pydata([(-a, Y - 0.11, z0 - b), (a, Y - 0.11, z0 - b), (a, Y - 0.11, z0 + b), (-a, Y - 0.11, z0 + b)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("led_yuz", me); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat_emis("led_yuz", lin(hex3(R["koyu"])), 1.2))
    for s in (-1, 1):
        boru((s * W_ * 0.3, Y, H_ + K), (s * W_ * 0.3, Y, H_ + K + 0.15), 0.02, mat_pbr("tel", "#cfd3d8", 0.3, metal=1.0))
        can_simidi((s * (xk + K / 2 + 0.05), Y - 0.05, 2.2), rot=(math.radians(90), 0, math.radians(90)), r=0.3)


def serit_katmani(oyuncu):
    R = SERIT[oyuncu]
    sc = plaj_sahnesi(960, 1080, True)
    kam = kamera(sc)
    rnd = random.Random(26 + (oyuncu == "p2"))
    isiklar()
    plaj(True, random.Random(26))
    serit_esyalari(oyuncu, R, rnd)
    kapi(R)
    Y, W_, H_ = KAP["y"], KAP["w"], KAP["h"]
    ic = W_ / 2
    bpy.context.view_layer.update()
    px = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-ic, Y, 0), (ic, Y, 0), (-ic, Y, H_), (ic, Y, H_))]
    xs = [p.x * 960 for p in px]; ys = [(1 - p.y) * 1080 for p in px]
    YERLESIM["aciklik_" + oyuncu] = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
    # OUT ani: kum yiginlarinin ekrandaki yeri; motor 22'nin "salon_" anahtar duzeni korunur (minder = kum yigini)
    mk = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-2.75, 5.2, 0.2), (2.75, 5.2, 0.2), (0, GECIS, 0))]
    d = {"minder_sol_x": round(mk[0].x * 960, 1), "minder_sag_x": round(mk[1].x * 960, 1),
         "minder_y": round((1 - mk[0].y) * 1080, 1), "gecis_y": round((1 - mk[2].y) * 1080, 1)}
    YERLESIM["salon_" + oyuncu] = d; YERLESIM["plaj_" + oyuncu] = d
    YERLESIM["yol"] = {"y_kapi": Y, "genislik": YOL_YARI * 2, "kam": KAM, "serit_w": 960}
    log("aciklik", oyuncu, YERLESIM["aciklik_" + oyuncu], d)
    yaz(sc, ON_EK + "serit-%s.png" % oyuncu)


def gok_katmani(ad):
    sc = plaj_sahnesi(1920, 1080, False)
    kamera(sc)
    isiklar()
    plaj(False, random.Random(26))
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
    for o_ in ("p1", "p2"):
        serit_katmani(o_)
if YALNIZ in ("hepsi", "poz"):
    poz_maskeleri()
if YALNIZ in ("hepsi", "sahne"):
    gok_katmani("gok.png")
    for o_ in ("p1", "p2"):
        serit_katmani(o_)
        panel(o_)
json.dump(YERLESIM, open(os.path.join(CIKTI, "yerlesim.json"), "w"), indent=1)
log("bitti (plaj)", YERLESIM.get("aciklik_p1"), YERLESIM.get("aciklik_p2"))
