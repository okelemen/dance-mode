"""HUMAN TETRIS 29. video (REFERANSSIZ, 1v1) - GUNDUZ ORMAN TAPINAGI, CILALI 3D OYUN GORUNUMU. varlik.py calistirir (--mod orman).

POZ-DUVARI TALIMATLAR §2b 6. (son) mekan: tas basamak, sarmasik, selale; OUT ani: camura / selale havuzuna kayar.
§4 CILALI 3D OYUN GORUNUMU: canli doygun renk, tombul hatlar, cilali yuzey, gercek isik-golge-parlama (Cycles); foto dokusu yok,
isiksiz duz renk (emission) yuzey yok (kendi isigi olan ampuller/LED haric). Gok dolu (Masaustu md. 7): bulut kumeleri, papagan
suruleri, kelebekler; ufuk boyunca orman tepeleri. §8 SOLUK YASAK: tas gri degil sicak kum-turuncu, yosun/cicek/su doygun.

Katmanlar plaj (26) ile ayni (motor 23 uyumu): gok.png = tapinak + selale + orman + gok, serit-p1/p2.png = oyuncunun yakin tas yolu +
serit esyalari + kapi. Isik iki katmanda ayni olsun diye butun sahne serit katmaninda da kurulur, uzak kismi holdout.
Gecis cizgisi y = GECIS. OUT ani motorda: karakter dis taraftaki camur birikintisine kayar, camur sicrar.
Telif: genel orman/tapinak ogeleri (basamakli tas yapi, sutun, sarmasik); bilinen oyun/film tapinagi, yazi, logo, marka yok.

Ciktilar: gok.png, serit-p1/p2.png, panel-p1/p2.png, yerlesim.json; kapak modu (--yalniz kapak): kapak-gok.png, kapak-serit-p1/p2.png
"""

import random
YERLESIM.clear()
KAPAK = YALNIZ == "kapak"
POZLAMA = float(arg("--pozlama", arg("--kapak-pozlama", "0")))
GUNES = float(arg("--gunes", "4.0"))   # 15 Kas: kapak 1 soluk/koyu (doygunluk 0,485 < 0,504, parlaklik 0,666)
ON_EK = "kapak-" if KAPAK else ""
KAP = {"y": 8.0, "w": 3.4, "h": 3.7, "kalin": 0.55}
KAM = {"z": 2.3, "egim": 5.0, "lens": 18.0, "sensor": 24.0}
if KAPAK:
    KAM.update({"z": float(arg("--kapak-z", "2.0")), "egim": float(arg("--kapak-egim", "3.0")), "lens": float(arg("--kapak-lens", "16.0"))})
YOL_YARI = 2.6
GECIS = 11.0            # serit tas yolu burada biter, otesi gok.png
TAPINAK_Y = 46.0        # basamakli tapinagin on yuzu
SERIT = {
    "p1": {"ana": "#1e8cff", "koyu": "#0a3fa8", "acik": "#8cc8ff"},
    "p2": {"ana": "#ff3aa8", "koyu": "#a8105e", "acik": "#ffa6d6"},
}
CANLI = ("#ff3b4e", "#ffcc1e", "#1e9cff", "#2fd06a", "#ff4fc0", "#ff8a1e", "#8a5aff", "#20d6d0")
CICEK = ("#ff3b4e", "#ffcc1e", "#ff4fc0", "#ff8a1e", "#8a5aff", "#ffffff")


# ------------------------------------------------------------------ sahne / isik
def orman_sahnesi(w, h, saydam):
    sc = bos_sahne(w=w, h=h, saydam=saydam, ornek=ORNEK, doygun=True)
    sc.view_settings.view_transform = "Standard"           # 25 notu: AgX doygun renkleri pastele ceker
    sc.view_settings.exposure = POZLAMA
    sc.cycles.max_bounces = 6; sc.cycles.diffuse_bounces = 3; sc.cycles.glossy_bounces = 3
    sc.cycles.transmission_bounces = 2; sc.cycles.transparent_max_bounces = 8
    sc.cycles.use_light_tree = True
    # gok: doygun mavi degrade (ufuk acik turkuaz -> tepe koyu mavi); aydinlatmada dusuk guc (plaj 14 Kas: ortam isigi soldurmasin)
    nt = sc.world.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord"); sp = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Generated"], sp.inputs[0])
    rp = nt.nodes.new("ShaderNodeValToRGB"); el = rp.color_ramp.elements
    el[0].position = 0.0; el[0].color = (*lin(hex3("#5fe0ff")), 1)
    el[1].position = 0.45; el[1].color = (*lin(hex3("#0a62ff")), 1)
    e2 = el.new(0.12); e2.color = (*lin(hex3("#1aa6ff")), 1)
    nt.links.new(sp.outputs["Z"], rp.inputs[0])
    lp = nt.nodes.new("ShaderNodeLightPath")
    bg_k = nt.nodes.new("ShaderNodeBackground"); bg_k.inputs[1].default_value = 1.0
    bg_i = nt.nodes.new("ShaderNodeBackground"); bg_i.inputs[1].default_value = 0.45
    nt.links.new(rp.outputs[0], bg_k.inputs[0]); nt.links.new(rp.outputs[0], bg_i.inputs[0])
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


def kamera(sc, x=0.0):
    rx = math.radians(90 - KAM["egim"])
    bpy.ops.object.camera_add(location=(x, 0, KAM["z"]), rotation=(rx, 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.sensor_fit = "VERTICAL"; kam.data.sensor_height = KAM["sensor"]; kam.data.lens = KAM["lens"]
    kam.data.clip_end = 1500
    return kam


def isiklar():
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


def mat_tas(ad, renk1, renk2, yosun="#3fbf3a", yosun_oran=0.30, olcek=0.6, purluk=0.55):
    """sicak tas: iki ton gurultu + yosun lekeleri (yuksek frekansli gurultuyle esik) + hafif bump; cilali (coat) oyun tasi"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    ns = nt.nodes.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value = olcek; ns.inputs["Detail"].default_value = 3
    nt.links.new(geo.outputs["Position"], ns.inputs["Vector"])
    rp = nt.nodes.new("ShaderNodeValToRGB")
    rp.color_ramp.elements[0].position = 0.35; rp.color_ramp.elements[1].position = 0.7
    rp.color_ramp.elements[0].color = (*lin(hex3(renk1)), 1); rp.color_ramp.elements[1].color = (*lin(hex3(renk2)), 1)
    nt.links.new(ns.outputs["Fac"], rp.inputs[0])
    yn = nt.nodes.new("ShaderNodeTexNoise"); yn.inputs["Scale"].default_value = olcek * 3.0; yn.inputs["Detail"].default_value = 4
    nt.links.new(geo.outputs["Position"], yn.inputs["Vector"])
    ye = nt.nodes.new("ShaderNodeValToRGB")
    ye.color_ramp.elements[0].position = 1.0 - yosun_oran - 0.04; ye.color_ramp.elements[1].position = 1.0 - yosun_oran + 0.04
    nt.links.new(yn.outputs["Fac"], ye.inputs[0])
    mx = nt.nodes.new("ShaderNodeMixRGB"); mx.inputs[2].default_value = (*lin(hex3(yosun)), 1)
    nt.links.new(ye.outputs[0], mx.inputs[0]); nt.links.new(rp.outputs[0], mx.inputs[1])
    nt.links.new(mx.outputs[0], b.inputs["Base Color"])
    tn = nt.nodes.new("ShaderNodeTexNoise"); tn.inputs["Scale"].default_value = 30; tn.inputs["Detail"].default_value = 3
    nt.links.new(geo.outputs["Position"], tn.inputs["Vector"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.18; bp.inputs["Distance"].default_value = 0.02
    nt.links.new(tn.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = purluk; b.inputs["Coat Weight"].default_value = 0.25; b.inputs["Coat Roughness"].default_value = 0.2
    return m


def mat_dosek(ad, renk1, renk2, harc="#8a5a2e", olcek=1.1):
    """tas dosek yol: voronoi hucreleri (tas plaka) + koyu harc cizgisi + yosun; plaka ici iki ton"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    vo = nt.nodes.new("ShaderNodeTexVoronoi"); vo.feature = "DISTANCE_TO_EDGE"; vo.inputs["Scale"].default_value = olcek
    nt.links.new(geo.outputs["Position"], vo.inputs["Vector"])
    vc = nt.nodes.new("ShaderNodeTexVoronoi"); vc.inputs["Scale"].default_value = olcek
    nt.links.new(geo.outputs["Position"], vc.inputs["Vector"])
    rp = nt.nodes.new("ShaderNodeValToRGB")
    rp.color_ramp.elements[0].color = (*lin(hex3(renk1)), 1); rp.color_ramp.elements[1].color = (*lin(hex3(renk2)), 1)
    nt.links.new(vc.outputs["Color"], rp.inputs[0])              # her plaka kendi tonunda
    hr = nt.nodes.new("ShaderNodeValToRGB")
    hr.color_ramp.elements[0].position = 0.03; hr.color_ramp.elements[1].position = 0.07
    nt.links.new(vo.outputs["Distance"], hr.inputs[0])
    mx = nt.nodes.new("ShaderNodeMixRGB"); mx.inputs[1].default_value = (*lin(hex3(harc)), 1)
    nt.links.new(hr.outputs[0], mx.inputs[0]); nt.links.new(rp.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], b.inputs["Base Color"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.45; bp.inputs["Distance"].default_value = 0.03
    nt.links.new(hr.outputs[0], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = 0.45; b.inputs["Coat Weight"].default_value = 0.35; b.inputs["Coat Roughness"].default_value = 0.15
    return m


def mat_su(ad, renk_yakin, renk_uzak, uzak=40.0):
    """havuz suyu: turkuaz, parlak, dalga bump"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    ns = nt.nodes.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value = 0.25; ns.inputs["Detail"].default_value = 2
    nt.links.new(geo.outputs["Position"], ns.inputs["Vector"])
    rp = nt.nodes.new("ShaderNodeValToRGB")
    rp.color_ramp.elements[0].color = (*lin(hex3(renk_yakin)), 1); rp.color_ramp.elements[1].color = (*lin(hex3(renk_uzak)), 1)
    nt.links.new(ns.outputs["Fac"], rp.inputs[0]); nt.links.new(rp.outputs[0], b.inputs["Base Color"])
    bn = nt.nodes.new("ShaderNodeTexNoise"); bn.inputs["Scale"].default_value = 2.5; bn.inputs["Detail"].default_value = 5
    nt.links.new(geo.outputs["Position"], bn.inputs["Vector"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.3; bp.inputs["Distance"].default_value = 0.05
    nt.links.new(bn.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = 0.12; b.inputs["Specular IOR Level"].default_value = 0.15
    return m


def mat_selale(ad):
    """akan su perdesi: dikey uzatilmis dalga bantlari (beyaz kopuk <-> turkuaz), parlak; foto dokusu yok"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (3.0, 3.0, 0.15)
    nt.links.new(geo.outputs["Position"], mp.inputs[0])
    ns = nt.nodes.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value = 1.4; ns.inputs["Detail"].default_value = 4
    nt.links.new(mp.outputs[0], ns.inputs["Vector"])
    rp = nt.nodes.new("ShaderNodeValToRGB"); el = rp.color_ramp.elements
    el[0].position = 0.38; el[0].color = (*lin(hex3("#18c8e6")), 1)
    el[1].position = 0.62; el[1].color = (*lin(hex3("#ffffff")), 1)
    nt.links.new(ns.outputs["Fac"], rp.inputs[0]); nt.links.new(rp.outputs[0], b.inputs["Base Color"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.4
    nt.links.new(ns.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = 0.1; b.inputs["Coat Weight"].default_value = 0.5
    return m


def duz(ad, x0, x1, y0, y1, z, mat):
    me = bpy.data.meshes.new(ad)
    me.from_pydata([(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new(ad, me); bpy.context.collection.objects.link(o); o.data.materials.append(mat)
    return o


def renk_dilimli(o, mats, n, eksen="z"):
    for m_ in mats:
        o.data.materials.append(m_)
    vs = o.data.vertices; mrk = sum((v.co for v in vs), Vector()) / max(1, len(vs))
    for p in o.data.polygons:
        c = p.center - mrk
        a = math.atan2(c.y, c.x) if eksen == "z" else math.atan2(c.z, c.x)
        p.material_index = int(((a + math.pi) / (2 * math.pi)) * n) % len(mats)


# ------------------------------------------------------------------ ORMAN TAPINAGI (iki katmanda; serit sahnesinde uzak kisim holdout)
_MAT = {}


def M(ad, f):
    """ayni malzemeyi tekrar tekrar kurmamak icin onbellek (yuzlerce agac yapragi)"""
    if ad not in _MAT:
        _MAT[ad] = f()
    return _MAT[ad]


def orman(serit_modu, rnd):
    _MAT.clear()
    cim = mat_pbr("cim", "#2fe03a", 0.55, kaplama=0.2, bump=(18, 0.25))
    duz("zemin_yakin", -80, 80, -4, GECIS, 0, cim)
    duz("zemin_uzak", -300, 300, GECIS, 400, 0, cim)
    yol = mat_dosek("tas_yol", "#ffa43a", "#ffc252", harc="#c8702c")
    duz("tas_yol_uzak", -2.6, 2.6, GECIS, TAPINAK_Y - 2, 0.006, yol)      # tapinaga uzanan tas yol (iki serit birlesir)
    tapinak((0, TAPINAK_Y, 0))
    selale((-26, 62, 0), rnd)
    for s in (-1, 1):                                                      # tapinaga cikan yol boyunca sarmasikli sutunlar
        for k, y in enumerate((16, 22, 28, 34, 40)):
            sutun((s * (4.2 + 0.2 * k), y, 0), 3.2 + 0.35 * k, rnd, devrik=(k == 2 and s == 1))
    for s in (-1, 1):                                                      # iki yanda tombul orman agaclari (katman katman)
        for k in range(16):
            x = s * rnd.uniform(9, 46); y = rnd.uniform(14, 75)
            if abs(x) < 9 + (y - 14) * 0.05:
                continue
            agac((x, y, 0), rnd.uniform(6.5, 11.0), rnd)
    for k in range(26):                                                    # ufuk: tepe sirtlari agac kubbeleri
        x = -220 + k * 17.6 + rnd.uniform(-5, 5)
        agac((x, rnd.uniform(110, 160), 0), rnd.uniform(16, 26), rnd, uzak=True)
    for (x, y, r, h) in ((-150, 230, 60, 38), (-40, 260, 55, 30), (90, 240, 70, 44), (200, 270, 62, 34), (-260, 280, 70, 40)):
        k_ = kure((x, y, 0), r, M("tepe", lambda: mat_pbr("tepe", "#23a83c", 0.6, kaplama=0.15, bump=(1.5, 0.4))), sub=4)
        k_.scale = (1.4, 0.7, h / r)
    for k in range(40):                                                    # yol kenarlarinda dev yaprak + cicek obekleri
        s = rnd.choice((-1, 1)); x = s * rnd.uniform(3.6, 9.0); y = rnd.uniform(11.5, 40)
        if rnd.random() < 0.55:
            dev_yaprak((x, y, 0), rnd.uniform(1.0, 1.8), rnd)
        else:
            cicek_obegi((x, y), rnd)
    gok_ogeleri(rnd)
    if serit_modu:                                                         # yakin zemin disinda her parca holdout
        for o in bpy.data.objects:
            if o.type == "MESH" and o.name.split(".")[0] not in ("zemin_yakin",):
                o.is_holdout = True


def tapinak(konum):
    """basamakli tas tapinak: 5 kat, on yuzde genis merdiven, tepede sutunlu kucuk oda + oyuncu renklerinde bayrak; sarmasik sarkar"""
    x, y, z = konum
    tas = mat_tas("tapinak", "#ff9a38", "#ffb94e", yosun_oran=0.28, olcek=0.25)
    koyu = mat_tas("tapinak_k", "#b8723a", "#cc8646", yosun_oran=0.2, olcek=0.3)
    katlar = 5; h = 2.6; W0, D0 = 34.0, 20.0
    for i in range(katlar):
        w = W0 - i * 5.6; d = D0 - i * 3.0
        yuvarlak_kutu("kat%d" % i, (x, y + D0 / 2 + i * 0.4, z + h * (i + 0.5)), (w, d, h), tas, egim=0.25, seg=3)
        yuvarlak_kutu("bant%d" % i, (x, y + D0 / 2 + i * 0.4 - d / 2 - 0.05, z + h * (i + 1) - 0.35), (w + 0.2, 0.5, 0.45), koyu, egim=0.12, seg=2)
    # on merdiven (kat yuksekligini gecen basamaklar)
    n = katlar * 7
    for i in range(n):
        yuvarlak_kutu("basamak", (x, y - 0.6 + i * (katlar * 1.2 / n) + 0.0, z + (i + 0.5) * (h * katlar / n)), (6.4, 1.3, h * katlar / n), koyu, egim=0.06, seg=2)
    # tepe odasi
    zt = z + h * katlar; yt = y + D0 / 2 + katlar * 0.4
    yuvarlak_kutu("oda", (x, yt, zt + 2.2), (8.0, 6.0, 4.4), tas, egim=0.3, seg=3)
    yuvarlak_kutu("oda_cati", (x, yt, zt + 4.8), (9.4, 7.2, 0.9), koyu, egim=0.3, seg=3)
    yuvarlak_kutu("oda_kapi", (x, yt - 3.02, zt + 1.7), (2.4, 0.1, 3.0), mat_pbr("oda_ic", "#3a2416", 0.8), egim=0.2, seg=3)
    for dx in (-3.2, 3.2):
        boru((x + dx, yt - 3.2, zt), (x + dx, yt - 3.2, zt + 4.3), 0.45, tas)
    for s, R in ((-1, SERIT["p1"]), (1, SERIT["p2"])):                     # tepede iki oyuncu renginde bayrak
        bx = x + s * 4.4
        boru((bx, yt - 3.0, zt + 5.2), (bx, yt - 3.0, zt + 9.0), 0.07, mat_pbr("bdir", "#f4f0e6", 0.4))
        me = bpy.data.meshes.new("bayrak")
        me.from_pydata([(bx, yt - 3.0, zt + 9.0), (bx + s * 2.2, yt - 3.0, zt + 8.4), (bx, yt - 3.0, zt + 7.6)], [], [[0, 1, 2]]); me.update()
        o = bpy.data.objects.new("bayrak", me); bpy.context.collection.objects.link(o)
        o.data.materials.append(mat_pbr("bayrak" + R["ana"], R["ana"], 0.35, kaplama=0.5)); o.modifiers.new("k", "SOLIDIFY").thickness = 0.05
    # kat kenarlarindan sarkan sarmasiklar
    rnd = random.Random(29)
    for i in range(katlar):
        w = W0 - i * 5.6; d = D0 - i * 3.0; yy = y + D0 / 2 + i * 0.4 - d / 2 - 0.3; zz = z + h * (i + 1)
        for k in range(9):
            xx = x + rnd.uniform(-w / 2 + 1, w / 2 - 1)
            if abs(xx - x) < 3.6:
                continue
            sarmasik((xx, yy, zz), rnd.uniform(1.2, h * 1.4), rnd)


def sarmasik(ust, boy, rnd):
    x, y, z = ust
    yp = [M("sar1", lambda: mat_pbr("sar1", "#2fd04a", 0.4, kaplama=0.35)), M("sar2", lambda: mat_pbr("sar2", "#1fae3a", 0.4, kaplama=0.35))]
    gv = M("sar_g", lambda: mat_pbr("sar_g", "#2c8a2a", 0.5))
    boru((x, y, z), (x + rnd.uniform(-0.2, 0.2), y - 0.05, z - boy), 0.04, gv)
    k = 0; t = 0.2
    while t < boy:
        kk = kure((x + 0.12 * math.sin(k * 1.7), y - 0.12, z - t), 0.16, yp[k % 2], sub=2); kk.scale = (1.3, 0.5, 1.0)
        t += 0.28; k += 1


def sutun(taban, boy, rnd, devrik=False):
    """sarmasikli tas sutun: tombul govde + bilezik bantlari + baslik; bazen devrilmis (yatik, yarim)"""
    x, y, z = taban
    tas = M("sutun", lambda: mat_tas("sutun", "#ff9e3a", "#ffbe55", yosun_oran=0.32, olcek=0.9))
    koyu = M("sutun_k", lambda: mat_tas("sutun_k", "#bd773c", "#d08e4c", yosun_oran=0.2, olcek=0.9))
    if devrik:
        o = boru((x - 1.6, y, 0.55), (x + 1.8, y + 0.6, 0.55), 0.55, tas)
        yuvarlak_kutu("kaide", (x - 2.2, y, 0.35), (1.6, 1.6, 0.7), koyu, egim=0.12, seg=2)
        return
    yuvarlak_kutu("kaide", (x, y, 0.3), (1.5, 1.5, 0.6), koyu, egim=0.12, seg=2)
    boru((x, y, 0.6), (x, y, boy), 0.52, tas)
    for zz in (1.2, boy * 0.6):
        bpy.ops.mesh.primitive_torus_add(major_radius=0.54, minor_radius=0.1, location=(x, y, zz)); bpy.context.active_object.data.materials.append(koyu)
        bpy.ops.object.shade_smooth()
    yuvarlak_kutu("baslik", (x, y, boy + 0.3), (1.5, 1.5, 0.6), koyu, egim=0.12, seg=2)
    for k in range(3):                                                    # sutuna dolanan sarmasik
        a0 = rnd.uniform(0, 6.28)
        for i in range(12):
            t = i / 11; a = a0 + t * 5.0
            kk = kure((x + 0.6 * math.cos(a), y + 0.6 * math.sin(a), 0.6 + t * (boy - 0.6)), 0.17,
                      M("sar1", lambda: mat_pbr("sar1", "#2fd04a", 0.4, kaplama=0.35)), sub=2)
            kk.scale = (1.2, 1.2, 0.6)


def agac(taban, boy, rnd, uzak=False):
    """tombul oyun agaci: kivrik kahverengi govde + 3-5 yuvarlak yesil tac kumesi (iki ton), yakindakilerde liana"""
    x, y, z = taban
    gv = M("agac_g", lambda: mat_pbr("agac_g", "#8a5226", 0.6, bump=(25, 0.25)))
    tonlar = (("tac1", "#27c43e"), ("tac2", "#1aa63a"), ("tac3", "#4ad94a"))
    if not uzak:
        boru((x, y, 0), (x + rnd.uniform(-0.6, 0.6), y, boy * 0.62), 0.32 + boy * 0.02, gv)
    zt = boy * 0.7
    for k in range(3 if uzak else rnd.randint(3, 5)):
        ad, renk = tonlar[rnd.randrange(3)]
        r = boy * rnd.uniform(0.22, 0.32)
        kk = kure((x + rnd.uniform(-0.3, 0.3) * boy, y + rnd.uniform(-0.15, 0.15) * boy, zt + rnd.uniform(-0.1, 0.15) * boy), r,
                  M(ad, lambda r_=renk, a_=ad: mat_pbr(a_, r_, 0.45, kaplama=0.3, bump=(3, 0.3))), sub=3)
        kk.scale = (1.15, 1.0, 0.9)
    if not uzak and rnd.random() < 0.6:                                   # meyve/cicek noktalari (renk)
        for k in range(4):
            kure((x + rnd.uniform(-0.3, 0.3) * boy, y - boy * 0.25, zt + rnd.uniform(-0.15, 0.1) * boy), boy * 0.035,
                 M("meyve%d" % (k % 3), lambda c=("#ff3b4e", "#ffcc1e", "#ff8a1e")[k % 3], k_=k: mat_pbr("meyve%d" % (k_ % 3), c, 0.3, kaplama=0.7)))


def dev_yaprak(taban, olcek, rnd):
    """monstera benzeri genis parlak yaprak demeti: yerden yukari kivrilan 4-6 yaprak"""
    x, y, z = taban
    yap = [M("dy1", lambda: mat_pbr("dy1", "#29c447", 0.35, kaplama=0.45)), M("dy2", lambda: mat_pbr("dy2", "#16a23a", 0.35, kaplama=0.45))]
    for j in range(rnd.randint(4, 6)):
        a = rnd.uniform(0, 2 * math.pi)
        d = Vector((math.cos(a), math.sin(a), 0)); dik = Vector((-math.sin(a), math.cos(a), 0))
        L = olcek * rnd.uniform(1.0, 1.5); v = []; f = []; m = 10
        for i in range(m + 1):
            t = i / m
            c = Vector((x, y, z)) + d * (L * 0.7 * t) + Vector((0, 0, L * (1.2 * t - 0.75 * t * t)))
            w = L * 0.32 * math.sin(math.pi * min(1.0, t * 1.05)) ** 0.6
            v += [c - dik * w + Vector((0, 0, -0.05 * w)), c + Vector((0, 0, 0.04)), c + dik * w + Vector((0, 0, -0.05 * w))]
            if i:
                q = 3 * i
                f += [[q - 3, q, q + 1, q - 2], [q - 2, q + 1, q + 2, q - 1]]
        me = bpy.data.meshes.new("yaprak"); me.from_pydata(v, [], f); me.update()
        o = bpy.data.objects.new("yaprak", me); bpy.context.collection.objects.link(o); o.data.materials.append(yap[j % 2])
        o.modifiers.new("kal", "SOLIDIFY").thickness = 0.03
        for p in o.data.polygons:
            p.use_smooth = True


def cicek_obegi(xy, rnd):
    x, y = xy
    yes = M("cy", lambda: mat_pbr("cy", "#2fbf45", 0.45, kaplama=0.3))
    kk = kure((x, y, 0.15), 0.55, yes, sub=2); kk.scale = (1.3, 1.0, 0.55)
    for k in range(rnd.randint(4, 7)):
        renk = rnd.choice(CICEK)
        kure((x + rnd.uniform(-0.6, 0.6), y + rnd.uniform(-0.4, 0.4), 0.42 + rnd.uniform(0, 0.15)), rnd.uniform(0.09, 0.14),
             M("cic" + renk, lambda r_=renk: mat_pbr("cic" + r_, r_, 0.3, kaplama=0.8)), sub=2)


def selale(konum, rnd):
    """yesil kaya ucurum + iki basamakli selale + turkuaz havuz + kopuk; havuz kenarinda tas kenar"""
    x, y, z = konum
    kaya = mat_tas("ucurum", "#4a9a52", "#5fb35a", yosun="#2fd04a", yosun_oran=0.45, olcek=0.35)
    for (dx, dy, r, h) in ((0, 6, 14, 26), (-12, 4, 11, 20), (11, 8, 10, 18), (-22, 10, 12, 16)):
        k = kure((x + dx, y + dy, 0), r, kaya, sub=4); k.scale = (1.0, 0.75, h / r)
    su = mat_selale("selale")
    for (zx, gen, z0, z1, yy) in ((0, 4.2, 9.0, 24.0, y - 4.4), (0, 6.0, 0.2, 9.4, y - 7.8)):
        me = bpy.data.meshes.new("selale")
        me.from_pydata([(x + zx - gen / 2, yy, z0), (x + zx + gen / 2, yy, z0), (x + zx + gen / 2, yy + 0.6, z1), (x + zx - gen / 2, yy + 0.6, z1)],
                       [], [[0, 1, 2, 3]]); me.update()
        o = bpy.data.objects.new("selale", me); bpy.context.collection.objects.link(o); o.data.materials.append(su)
        o.modifiers.new("k", "SOLIDIFY").thickness = 0.4
    yuvarlak_kutu("ara_cikinti", (x, y - 5.6, 8.8), (8.0, 3.4, 1.0), kaya, egim=0.4, seg=3)
    havuz = mat_su("havuz", "#1fe6d2", "#0aa0e0")
    bpy.ops.mesh.primitive_cylinder_add(radius=9.5, depth=0.1, location=(x, y - 12, 0.03), vertices=48)
    h_ = bpy.context.active_object; h_.scale = (1.3, 0.75, 1); h_.data.materials.append(havuz)
    kopuk = M("kopuk", lambda: mat_pbr("kopuk", "#ffffff", 0.35, kaplama=0.3))
    for k in range(18):
        a = rnd.uniform(-0.6, 0.6)
        kk = kure((x + a * 6, y - 8.6 + rnd.uniform(-0.6, 0.6), 0.25), rnd.uniform(0.4, 0.8), kopuk, sub=2); kk.scale = (1.2, 1.0, 0.45)
    kenar = M("kenar", lambda: mat_tas("kenar", "#d7964f", "#e8b06a", yosun_oran=0.35, olcek=1.2))
    for k in range(22):
        a = math.pi * (0.05 + 0.9 * k / 21)
        kk = kure((x + 12.4 * math.cos(a + math.pi), y - 12 + 7.2 * math.sin(a + math.pi), 0.2), rnd.uniform(0.7, 1.1), kenar, sub=2)
        kk.scale = (1.3, 1.0, 0.6)


def bulut(merkez, olcek, rnd):
    beyaz = M("bulut", lambda: mat_pbr("bulut", "#ffffff", 0.85))
    x, y, z = merkez
    for k in range(9):
        r = olcek * rnd.uniform(0.45, 0.85)
        dx = rnd.uniform(-1.5, 1.5) * olcek; dz = rnd.uniform(-0.2, 0.55) * olcek * (1 - abs(dx) / (2 * olcek))
        b = kure((x + dx, y + rnd.uniform(-0.4, 0.4) * olcek, z + dz), r, beyaz, sub=3); b.scale = (1.15, 0.8, 0.9)
    kure((x, y, z - 0.25 * olcek), olcek * 0.75, beyaz).scale = (2.4, 0.8, 0.45)


def papagan(konum, olcek, govde, kanat, rnd):
    """tombul ucan papagan: govde damla + iki kanat ucgeni (renkli) + sari gaga"""
    x, y, z = konum
    g = kure((x, y, z), 0.45 * olcek, M("pg" + govde, lambda: mat_pbr("pg" + govde, govde, 0.3, kaplama=0.7)), sub=2); g.scale = (0.8, 1.7, 0.8)
    kure((x, y - 0.75 * olcek, z + 0.1 * olcek), 0.3 * olcek, M("pg" + govde, lambda: mat_pbr("pg" + govde, govde, 0.3, kaplama=0.7)), sub=2)
    kure((x, y - 1.02 * olcek, z + 0.05 * olcek), 0.12 * olcek, M("gaga", lambda: mat_pbr("gaga", "#ffcc1e", 0.3, kaplama=0.7)), sub=2)
    k = rnd.uniform(0.3, 0.8)
    for s in (-1, 1):
        me = bpy.data.meshes.new("kanat")
        me.from_pydata([(x, y - 0.3 * olcek, z), (x + s * 1.8 * olcek, y, z + k * olcek), (x, y + 0.5 * olcek, z)], [], [[0, 1, 2]]); me.update()
        o = bpy.data.objects.new("kanat", me); bpy.context.collection.objects.link(o)
        o.data.materials.append(M("pk" + kanat, lambda: mat_pbr("pk" + kanat, kanat, 0.35, kaplama=0.6))); o.modifiers.new("k", "SOLIDIFY").thickness = 0.06 * olcek
    me = bpy.data.meshes.new("kuyruk")
    me.from_pydata([(x - 0.2 * olcek, y + 0.6 * olcek, z), (x + 0.2 * olcek, y + 0.6 * olcek, z), (x, y + 2.2 * olcek, z - 0.3 * olcek)], [], [[0, 1, 2]]); me.update()
    o = bpy.data.objects.new("kuyruk", me); bpy.context.collection.objects.link(o)
    o.data.materials.append(M("pk" + kanat, lambda: mat_pbr("pk" + kanat, kanat, 0.35, kaplama=0.6))); o.modifiers.new("k", "SOLIDIFY").thickness = 0.05 * olcek


def kelebek(konum, olcek, renk):
    x, y, z = konum
    for s in (-1, 1):
        for (dz, w) in ((0.25, 1.0), (-0.3, 0.7)):
            k = kure((x + s * 0.45 * olcek, y, z + dz * olcek), 0.42 * olcek * w, M("kel" + renk, lambda: mat_pbr("kel" + renk, renk, 0.3, kaplama=0.8)), sub=2)
            k.scale = (1.0, 0.12, 0.8)
    boru((x, y, z - 0.4 * olcek), (x, y, z + 0.45 * olcek), 0.05 * olcek, M("kel_g", lambda: mat_pbr("kel_g", "#20242a", 0.5)))


def gok_ogeleri(rnd):
    """ekran dolu kurali (md. 7): bulut kumeleri butun gok boyunca, papagan suruleri, kelebekler"""
    for (x, y, z, o) in ((-150, 260, 70, 16), (-60, 300, 95, 20), (40, 280, 80, 17), (140, 250, 62, 15), (230, 320, 100, 22),
                         (-240, 320, 110, 22), (-100, 200, 48, 11), (95, 210, 50, 12), (0, 330, 120, 20), (-30, 220, 58, 10),
                         (190, 200, 40, 9), (-200, 230, 42, 10), (60, 360, 140, 26), (-140, 360, 150, 26)):
        bulut((x, y, z), o, rnd)
    renkler = (("#ff3b4e", "#1e9cff"), ("#2fd06a", "#ffcc1e"), ("#1e9cff", "#ffcc1e"), ("#ff8a1e", "#2fd06a"), ("#8a5aff", "#ff4fc0"))
    for k in range(11):
        g, kn = renkler[k % len(renkler)]
        papagan((rnd.uniform(-20, 20), rnd.uniform(26, 50), rnd.uniform(9, 19)), rnd.uniform(0.6, 0.9), g, kn, rnd)
    for k in range(14):
        kelebek((rnd.uniform(-9, 9), rnd.uniform(13, 24), rnd.uniform(1.8, 5.5)), rnd.uniform(0.25, 0.4), rnd.choice(("#ff4fc0", "#ffcc1e", "#1e9cff", "#ff8a1e", "#8a5aff")))


# ------------------------------------------------------------------ SERIT: oyuncu tas yolu + tas sinir + oyuncu renginde fener + OUT camuru + kapi
def serit_esyalari(oyuncu, R, rnd):
    s_dis = -1 if oyuncu == "p1" else 1
    yol = mat_dosek("serit_yol", "#ffa43a", "#ffc252", harc="#c8702c")
    duz("serit_yol", -1.6, 1.6, -4, GECIS, 0.006, yol)
    sinir = mat_tas("sinir", "#f08a30", "#ffa640", yosun_oran=0.35, olcek=2.0)
    for x in (-1.75, 1.75):                                                # serit siniri: alcak tas bordur + oyuncu renginde cicekler
        yuvarlak_kutu("bordur", (x, (KAP["y"] - 4) / 2 - 0.3, 0.12), (0.32, KAP["y"] + 3.4, 0.26), sinir, egim=0.08, seg=2)
        y = -3.4; i = 0
        while y < KAP["y"] - 0.8:
            kure((x, y, 0.3), 0.12, M("cic_" + oyuncu, lambda: mat_pbr("cic_" + oyuncu, R["ana"], 0.25, kaplama=0.9)), sub=2)
            kure((x + 0.12, y + 0.18, 0.28), 0.08, M("cicb", lambda: mat_pbr("cicb", "#ffffff", 0.3, kaplama=0.8)), sub=2)
            y += 0.9; i += 1
    boya = mat_pbr("ok_" + oyuncu, R["ana"], 0.35, kaplama=0.6)
    for y in (4.9, 6.4):                                                   # tas yolda oyuncu renginde boyali yon oklari (seri sabiti)
        nok = [(-0.75, y - 0.45), (0, y), (0.75, y - 0.45), (0.75, y - 0.75), (0, y - 0.3), (-0.75, y - 0.75)]
        me = bpy.data.meshes.new("ok"); me.from_pydata([(a, b, 0.014) for a, b in nok], [], [list(range(6))]); me.update()
        o = bpy.data.objects.new("ok", me); bpy.context.collection.objects.link(o); o.data.materials.append(boya)
        o.modifiers.new("k", "SOLIDIFY").thickness = 0.02
    # OUT ani: dis tarafta parlak camur birikintisi (karakter buraya kayar)
    camur = mat_pbr("camur", "#7a4220", 0.12, kaplama=0.8, bump=(6, 0.35))
    c_ = kure((s_dis * 2.85, 5.2, -0.1), 1.0, camur, sub=4); c_.scale = (1.05, 1.9, 0.18)
    kenar = M("camur_k", lambda: mat_pbr("camur_k", "#5a3016", 0.4, kaplama=0.3))
    for k in range(9):
        a = 2 * math.pi * k / 9
        kk = kure((s_dis * 2.85 + 1.05 * math.cos(a), 5.2 + 1.9 * math.sin(a), 0.05), 0.2, kenar, sub=2); kk.scale = (1.3, 1.3, 0.6)
    # dis tarafta orman esyalari (dev yaprak, cicek, devrik tas, mantar)
    dev_yaprak((s_dis * 4.8, 7.0, 0), 1.5, rnd)
    cicek_obegi((s_dis * 4.0, 9.2), rnd)
    mantar((s_dis * 4.4, 4.0), "#ff3b4e" if oyuncu == "p1" else "#ffcc1e")
    t_ = yuvarlak_kutu("tas_blok", (s_dis * 5.6, 9.6, 0.4), (1.2, 1.0, 0.8), mat_tas("blok", "#e09a52", "#f0b866", yosun_oran=0.4, olcek=1.5), egim=0.15, seg=2)
    t_.rotation_euler = (0, 0, 0.3 * s_dis)
    # ic tarafta (hakem yeri) kucuk mesale direkleri - alevi kendi isigi (emission serbest)
    for yy in (2.5, 7.4):
        mesale((-s_dis * 2.45, yy))


def mantar(xy, renk):
    x, y = xy
    boru((x, y, 0), (x, y, 0.45), 0.09, M("man_g", lambda: mat_pbr("man_g", "#fff4e0", 0.4, kaplama=0.4)))
    k = kure((x, y, 0.5), 0.32, M("man" + renk, lambda: mat_pbr("man" + renk, renk, 0.2, kaplama=0.9)), sub=3); k.scale = (1.0, 1.0, 0.6)
    for a in (0.5, 2.1, 3.8, 5.2):
        kure((x + 0.2 * math.cos(a), y + 0.2 * math.sin(a), 0.62), 0.05, M("man_n", lambda: mat_pbr("man_n", "#ffffff", 0.3, kaplama=0.6)), sub=1)


def mesale(xy):
    x, y = xy
    boru((x, y, 0), (x, y, 1.2), 0.05, M("mes_g", lambda: mat_pbr("mes_g", "#7a4a22", 0.5)))
    bpy.ops.mesh.primitive_cone_add(radius1=0.06, radius2=0.16, depth=0.22, location=(x, y, 1.28))
    bpy.context.active_object.data.materials.append(M("mes_c", lambda: mat_pbr("mes_c", "#4a3a2a", 0.4, metal=0.6)))
    al = kure((x, y, 1.48), 0.13, M("alev", lambda: mat_emis("alev", lin(hex3("#ffb02e")), 6.0)), sub=2); al.scale = (0.9, 0.9, 1.5)


def kapi(R):
    """tas kemer kapi: iki tombul oymali tas sutun + kemer kirisi, oyuncu renginde boyali oyma bantlar, sarmasik, ampul dizisi,
    ustte sonuk LED tabela (motor PLAYER n yazar)"""
    Y, W_, H_, K = KAP["y"], KAP["w"], KAP["h"], KAP["kalin"]
    tas = mat_tas("kapi_tas", "#ff9e3a", "#ffbe55", yosun_oran=0.22, olcek=1.4)
    boya = mat_pbr("kapi_boya", R["ana"], 0.25, kaplama=0.9)
    xk = W_ / 2 + K / 2
    for s in (-1, 1):
        yuvarlak_kutu("direk", (s * xk, Y, (H_ + K) / 2), (K, K, H_ + K), tas, egim=0.14, seg=3)
        for z in (0.6, 1.6, 2.6):
            yuvarlak_kutu("oyma", (s * xk, Y, z), (K + 0.06, K + 0.06, 0.16), boya, egim=0.05, seg=2)
        yuvarlak_kutu("kaide", (s * xk, Y, 0.15), (K + 0.3, K + 0.3, 0.3), tas, egim=0.08, seg=2)
    yuvarlak_kutu("kiris", (0, Y, H_ + K / 2), (W_ + 2 * K + 0.3, K, K), tas, egim=0.14, seg=3)
    yuvarlak_kutu("kiris_bant", (0, Y - K / 2 - 0.02, H_ + K / 2), (W_ + 2 * K, 0.06, 0.18), boya, egim=0.02, seg=1)
    ampul = M("ampul", lambda: mat_emis("ampul", lin(hex3("#ffe08a")), 5.0))
    for i in range(9):                                                     # kiris altinda ampul dizisi (kendi isigi)
        xx = -W_ / 2 + W_ * i / 8
        kure((xx, Y - K / 2 - 0.08, H_ - 0.05 - 0.12 * math.sin(math.pi * i / 8)), 0.07, ampul, sub=2)
    rnd = random.Random(7 + (R["ana"] == SERIT["p2"]["ana"]))
    for s in (-1, 1):
        sarmasik((s * xk, Y - K / 2 - 0.05, H_ + K), H_ * 0.8, rnd)
    yuvarlak_kutu("tabela", (0, Y, H_ + K + 0.5), (W_ * 0.85, 0.2, 0.7), mat_pbr("tabela", "#15171a", 0.35, metal=0.4), egim=0.05, seg=3)
    me = bpy.data.meshes.new("led_yuz"); a, b = W_ * 0.4, 0.28; z0 = H_ + K + 0.5
    me.from_pydata([(-a, Y - 0.11, z0 - b), (a, Y - 0.11, z0 - b), (a, Y - 0.11, z0 + b), (-a, Y - 0.11, z0 + b)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("led_yuz", me); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat_emis("led_yuz", lin(hex3(R["koyu"])), 1.2))
    for s in (-1, 1):
        boru((s * W_ * 0.3, Y, H_ + K), (s * W_ * 0.3, Y, H_ + K + 0.15), 0.02, mat_pbr("tel", "#cfd3d8", 0.3, metal=1.0))


def serit_katmani(oyuncu):
    R = SERIT[oyuncu]
    sc = orman_sahnesi(960, 1080, True)
    kam = kamera(sc)
    rnd = random.Random(29 + (oyuncu == "p2"))
    isiklar()
    orman(True, random.Random(29))
    serit_esyalari(oyuncu, R, rnd)
    kapi(R)
    Y, W_, H_ = KAP["y"], KAP["w"], KAP["h"]
    ic = W_ / 2
    bpy.context.view_layer.update()
    px = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-ic, Y, 0), (ic, Y, 0), (-ic, Y, H_), (ic, Y, H_))]
    xs = [p.x * 960 for p in px]; ys = [(1 - p.y) * 1080 for p in px]
    YERLESIM["aciklik_" + oyuncu] = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
    # OUT ani: camur birikintisinin ekrandaki yeri; motor 22/23 "salon_" / "plaj_" anahtar duzeni korunur (minder = camur)
    mk = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-2.85, 5.2, 0.2), (2.85, 5.2, 0.2), (0, GECIS, 0))]
    d = {"minder_sol_x": round(mk[0].x * 960, 1), "minder_sag_x": round(mk[1].x * 960, 1),
         "minder_y": round((1 - mk[0].y) * 1080, 1), "gecis_y": round((1 - mk[2].y) * 1080, 1)}
    YERLESIM["salon_" + oyuncu] = d; YERLESIM["plaj_" + oyuncu] = d; YERLESIM["orman_" + oyuncu] = d
    YERLESIM["yol"] = {"y_kapi": Y, "genislik": YOL_YARI * 2, "kam": KAM, "serit_w": 960}
    log("aciklik", oyuncu, YERLESIM["aciklik_" + oyuncu], d)
    yaz(sc, ON_EK + "serit-%s.png" % oyuncu)


def gok_katmani(ad):
    sc = orman_sahnesi(1920, 1080, False)
    kamera(sc)
    isiklar()
    orman(False, random.Random(29))
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
log("bitti (orman)", YERLESIM.get("aciklik_p1"), YERLESIM.get("aciklik_p2"))
