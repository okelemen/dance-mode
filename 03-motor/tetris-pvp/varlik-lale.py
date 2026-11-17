"""HUMAN TETRIS 30. video (REF-082 yapi, 1v1) - GUNDUZ YEL DEGIRMENLI LALE TARLASI, CILALI 3D OYUN GORUNUMU. varlik.py calistirir (--mod lale).

Mekan kullanici karari (17 Kas 2026): yel degirmenli lale tarlasi; OUT ani: karakter saman balyasi yiginina gomulur.
§4 CILALI 3D OYUN GORUNUMU: canli doygun renk, tombul hatlar, cilali yuzey, gercek isik-golge-parlama (Cycles); foto dokusu yok,
isiksiz duz renk (emission) yuzey yok (ampul/LED/fener haric). Gok dolu (Masaustu md. 7): bulut kumeleri, kus suruleri, kelebekler,
ucusan lale yapraklari; ufukta degirmenler + tepe sirtlari. §8 SOLUK YASAK: REF-082 kapagi doygunluk 0,620 / renklilik 0,560 -
lale siralari tam doygun (kirmizi, sari, turuncu, mor, pembe), cim canli yesil, gok doygun mavi.

Katmanlar orman (29) ile ayni (motor 23/26 uyumu): gok.png = degirmenler + tarla + kanal + gok, serit-p1/p2.png = oyuncunun yakin
tahta yolu + serit esyalari + kapi. Isik iki katmanda ayni olsun diye butun sahne serit katmaninda da kurulur, uzak kisim holdout.
Telif: genel kir/degirmen ogeleri; bilinen oyun/film tarlasi, yazi, logo, marka yok.

Ciktilar: gok.png, serit-p1/p2.png, panel-p1/p2.png, yerlesim.json; kapak modu (--yalniz kapak): kapak-gok.png, kapak-serit-p1/p2.png
"""

import random
YERLESIM.clear()
KAPAK = YALNIZ == "kapak"
POZLAMA = float(arg("--pozlama", arg("--kapak-pozlama", "0")))
GUNES = float(arg("--gunes", "4.8"))   # 17 Kas: mavi ortam isigi turuncu tahtayi soldurdu -> ortam 0,45 -> 0,22, gunes 4,0 -> 4,8
ON_EK = "kapak-" if KAPAK else ""
KAP = {"y": 8.0, "w": 3.4, "h": 3.7, "kalin": 0.55}
KAM = {"z": 2.3, "egim": 5.0, "lens": 18.0, "sensor": 24.0}
if KAPAK:
    KAM.update({"z": float(arg("--kapak-z", "2.0")), "egim": float(arg("--kapak-egim", "3.0")), "lens": float(arg("--kapak-lens", "16.0"))})
YOL_YARI = 2.6
GECIS = 11.0            # serit tahta yolu burada biter, otesi gok.png
DEGIRMEN_Y = 52.0       # yolun ucundaki buyuk yel degirmeni
KANAL_Y = (28.0, 31.0)  # tarlayi enine kesen kanal (yol uzerinde tahta kopru)
SERIT = {
    "p1": {"ana": "#1e8cff", "koyu": "#0a3fa8", "acik": "#8cc8ff"},
    "p2": {"ana": "#ff3aa8", "koyu": "#a8105e", "acik": "#ffa6d6"},
}
LALE = ("#ff1e3c", "#ffd21e", "#ff7a14", "#a040ff", "#ff3ab4", "#ff1e3c", "#ffffff", "#ffd21e")


# ------------------------------------------------------------------ sahne / isik
def lale_sahnesi(w, h, saydam):
    sc = bos_sahne(w=w, h=h, saydam=saydam, ornek=ORNEK, doygun=True)
    sc.view_settings.view_transform = "Standard"           # 25 notu: AgX doygun renkleri pastele ceker
    sc.view_settings.exposure = POZLAMA
    sc.cycles.max_bounces = 6; sc.cycles.diffuse_bounces = 3; sc.cycles.glossy_bounces = 3
    sc.cycles.transmission_bounces = 2; sc.cycles.transparent_max_bounces = 8
    sc.cycles.use_light_tree = True
    nt = sc.world.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord"); sp = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Generated"], sp.inputs[0])
    rp = nt.nodes.new("ShaderNodeValToRGB"); el = rp.color_ramp.elements
    el[0].position = 0.0; el[0].color = (*lin(hex3("#2ccaff")), 1)
    el[1].position = 0.40; el[1].color = (*lin(hex3("#0038d8")), 1)   # 17 Kas: parlaklik +0,07 -> koyu doygun tepe
    e2 = el.new(0.12); e2.color = (*lin(hex3("#0a8aff")), 1)
    nt.links.new(sp.outputs["Z"], rp.inputs[0])
    lp = nt.nodes.new("ShaderNodeLightPath")
    bg_k = nt.nodes.new("ShaderNodeBackground"); bg_k.inputs[1].default_value = 1.0
    bg_i = nt.nodes.new("ShaderNodeBackground"); bg_i.inputs[1].default_value = 0.22
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


def mat_tahta(ad, renk1, renk2, ara="#5a3416", olcek=1.0, satir=0.34):
    """tahta yol: tugla dokusuyla enine tahtalar (sira sira), her tahta kendi tonunda + koyu ara cizgi + damar bump; cilali vernik"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.inputs["Scale"].default_value = olcek; br.inputs["Mortar Size"].default_value = 0.012
    br.inputs["Brick Width"].default_value = 3.6; br.inputs["Row Height"].default_value = satir
    br.inputs["Color1"].default_value = (*lin(hex3(renk1)), 1); br.inputs["Color2"].default_value = (*lin(hex3(renk2)), 1)
    br.inputs["Mortar"].default_value = (*lin(hex3(ara)), 1)
    br.offset = 0.5; br.squash = 1.0
    nt.links.new(geo.outputs["Position"], br.inputs["Vector"])
    nt.links.new(br.outputs["Color"], b.inputs["Base Color"])
    mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (0.4, 8.0, 1.0)
    nt.links.new(geo.outputs["Position"], mp.inputs[0])
    dn = nt.nodes.new("ShaderNodeTexNoise"); dn.inputs["Scale"].default_value = 4.0; dn.inputs["Detail"].default_value = 4
    nt.links.new(mp.outputs[0], dn.inputs["Vector"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.25; bp.inputs["Distance"].default_value = 0.02
    nt.links.new(dn.outputs["Fac"], bp.inputs["Height"])
    bp2 = nt.nodes.new("ShaderNodeBump"); bp2.inputs["Strength"].default_value = 0.6; bp2.inputs["Distance"].default_value = 0.03
    nt.links.new(br.outputs["Fac"], bp2.inputs["Height"]); nt.links.new(bp.outputs["Normal"], bp2.inputs["Normal"])
    nt.links.new(bp2.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = 0.42; b.inputs["Coat Weight"].default_value = 0.35; b.inputs["Coat Roughness"].default_value = 0.15
    return m


def mat_saman(ad, renk1="#ffc400", renk2="#ff8c00"):
    """saman: dolanan (silindirde) seritler + lif bump; parlak altin sari"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    wv = nt.nodes.new("ShaderNodeTexWave"); wv.wave_type = "RINGS"; wv.inputs["Scale"].default_value = 6.0
    wv.inputs["Distortion"].default_value = 6.0; wv.inputs["Detail"].default_value = 3
    nt.links.new(geo.outputs["Position"], wv.inputs["Vector"])
    rp = nt.nodes.new("ShaderNodeValToRGB")
    rp.color_ramp.elements[0].color = (*lin(hex3(renk2)), 1); rp.color_ramp.elements[1].color = (*lin(hex3(renk1)), 1)
    nt.links.new(wv.outputs["Fac"], rp.inputs[0]); nt.links.new(rp.outputs[0], b.inputs["Base Color"])
    ns = nt.nodes.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value = 60; ns.inputs["Detail"].default_value = 6
    nt.links.new(geo.outputs["Position"], ns.inputs["Vector"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.5; bp.inputs["Distance"].default_value = 0.03
    nt.links.new(ns.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = 0.6; b.inputs["Coat Weight"].default_value = 0.15
    return m


def mat_su(ad, renk_yakin, renk_uzak):
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


def mat_lale_sira(ad, renk):
    """uzak lale sirasi: kendi renginde, cicek basi tumsekleri (voronoi bump) - uzakta tek tek lale gibi okunur"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    vo = nt.nodes.new("ShaderNodeTexVoronoi"); vo.inputs["Scale"].default_value = 3.0
    nt.links.new(geo.outputs["Position"], vo.inputs["Vector"])
    rp = nt.nodes.new("ShaderNodeValToRGB")
    rp.color_ramp.elements[0].position = 0.0; rp.color_ramp.elements[0].color = (*lin(hex3(renk)), 1)
    rp.color_ramp.elements[1].position = 0.75; rp.color_ramp.elements[1].color = (*lin(hex3("#18b030")), 1)
    nt.links.new(vo.outputs["Distance"], rp.inputs[0]); nt.links.new(rp.outputs[0], b.inputs["Base Color"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.8; bp.inputs["Distance"].default_value = 0.08
    inv = nt.nodes.new("ShaderNodeMath"); inv.operation = "SUBTRACT"; inv.inputs[0].default_value = 1.0
    nt.links.new(vo.outputs["Distance"], inv.inputs[1]); nt.links.new(inv.outputs[0], bp.inputs["Height"])
    nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = 0.35; b.inputs["Coat Weight"].default_value = 0.4; b.inputs["Coat Roughness"].default_value = 0.1
    return m


def duz(ad, x0, x1, y0, y1, z, mat):
    me = bpy.data.meshes.new(ad)
    me.from_pydata([(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new(ad, me); bpy.context.collection.objects.link(o); o.data.materials.append(mat)
    return o


_MAT = {}


def M(ad, f):
    if ad not in _MAT:
        _MAT[ad] = f()
    return _MAT[ad]


# ------------------------------------------------------------------ tek lale (sablon + bagli kopya: yuzlerce lale hizli kurulur)
_SABLON = {}


def lale_sablon(renk):
    """tombul lale: yumurta cicek basi (ust kenari 3 tac yaprak ucu) + sap + iki genis yaprak; tek nesne, sahne disi"""
    if renk in _SABLON:
        return _SABLON[renk]
    cm = M("lale" + renk, lambda: mat_pbr("lale" + renk, renk, 0.28, kaplama=0.8))
    ym = M("lale_yap", lambda: mat_pbr("lale_yap", "#25c23e", 0.4, kaplama=0.35))
    parca = []
    b = kure((0, 0, 0.62), 0.14, cm, sub=2); b.scale = (1.0, 1.0, 1.35); parca.append(b)
    for k in range(3):
        a = k * 2.094
        u = kure((0.07 * math.cos(a), 0.07 * math.sin(a), 0.78), 0.07, cm, sub=1); u.scale = (1.0, 1.0, 1.6); parca.append(u)
    parca.append(boru((0, 0, 0.0), (0, 0, 0.55), 0.025, ym))
    for s in (-1, 1):
        y_ = kure((s * 0.07, 0, 0.2), 0.08, ym, sub=1); y_.scale = (0.6, 0.35, 3.0); y_.rotation_euler = (0, s * 0.35, 0); parca.append(y_)
    bpy.ops.object.select_all(action="DESELECT")
    for p in parca:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parca[0]
    bpy.ops.object.join()
    o = bpy.context.active_object; o.name = "lale_sablon"
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    bpy.context.collection.objects.unlink(o)
    _SABLON[renk] = o
    return o


def lale_koy(renk, konum, olcek, rnd):
    s = lale_sablon(renk)
    o = s.copy(); o.data = s.data                     # bagli kopya: ayni mesh
    bpy.context.collection.objects.link(o)
    o.location = konum; o.scale = (olcek, olcek, olcek * rnd.uniform(0.9, 1.15))
    o.rotation_euler = (rnd.uniform(-0.08, 0.08), rnd.uniform(-0.08, 0.08), rnd.uniform(0, 6.28))
    return o


# ------------------------------------------------------------------ LALE TARLASI (iki katmanda; serit sahnesinde uzak kisim holdout)
def tarla(serit_modu, rnd):
    _MAT.clear(); _SABLON.clear()
    cim = mat_pbr("cim", "#18c42a", 0.55, kaplama=0.2, bump=(18, 0.25))
    duz("zemin_yakin", -80, 80, -4, GECIS, 0, cim)
    duz("zemin_uzak", -400, 400, GECIS, 500, 0, cim)
    yol = mat_tahta("tahta_yol", "#ff7a14", "#ff9a26", ara="#8a2a08")
    duz("tahta_yol_uzak", -2.6, 2.6, GECIS, KANAL_Y[0], 0.006, yol)
    duz("tahta_yol_uzak2", -2.6, 2.6, KANAL_Y[1], DEGIRMEN_Y - 4, 0.006, yol)
    kanal(rnd)
    # lale siralari: yola paralel renk seritleri (iki yanda), ufka kadar
    for s in (-1, 1):
        for i in range(34):
            x = s * (3.9 + i * 1.25)
            renk = LALE[(i + (s > 0) * 3) % len(LALE)]
            mat = M("sira" + renk, lambda r_=renk: mat_lale_sira("sira" + r_, r_))
            for (y0, y1) in ((14.0 if i < 8 else GECIS + 0.5, KANAL_Y[0] - 0.6), (KANAL_Y[1] + 0.6, 260.0)):
                yuvarlak_kutu("sira", (x, (y0 + y1) / 2, 0.5), (1.0, y1 - y0, 1.0), mat, egim=0.4, seg=3)
    # yakin siralar tek tek lale (gercek cicek basi) - yolun iki yaninda, y 11..14 arasi ve sira basi
    for s in (-1, 1):
        for i in range(8):
            x = s * (3.9 + i * 1.25)
            renk = LALE[(i + (s > 0) * 3) % len(LALE)]
            y = GECIS + 0.2
            while y < 14.0:
                for dx in (-0.22, 0.22):
                    lale_koy(renk, (x + dx + rnd.uniform(-0.05, 0.05), y, 0), rnd.uniform(1.4, 1.7), rnd)
                y += 0.42
    degirmen((0, DEGIRMEN_Y, 0), 17.0, 0.35)
    for (x, y, boy, a) in ((-30, 74, 13.0, 0.9), (34, 66, 12.0, 0.2), (-70, 120, 15.0, 0.55), (78, 128, 16.0, 1.1),
                           (-14, 150, 10.0, 0.0), (130, 170, 14.0, 0.7), (-140, 180, 15.0, 0.3)):
        degirmen((x, y, 0), boy, a)
    for k in range(18):                                                    # degirmenlerin dibinde saman balyalari
        x = rnd.choice((-1, 1)) * rnd.uniform(6, 40); y = rnd.uniform(36, 90)
        balya((x, y), rnd.uniform(0.9, 1.3), rnd.uniform(0, 3.14), rnd)
    for k in range(14):                                                    # ufukta yuvarlak agac kumeleri
        agac((-220 + k * 34 + rnd.uniform(-6, 6), rnd.uniform(200, 250), 0), rnd.uniform(14, 22), rnd)
    for (x, y, r, h) in ((-160, 320, 70, 34), (-30, 360, 60, 26), (110, 330, 80, 40), (240, 360, 70, 30), (-290, 360, 80, 36)):
        k_ = kure((x, y, 0), r, M("tepe", lambda: mat_pbr("tepe", "#2ec44a", 0.6, kaplama=0.15, bump=(1.5, 0.4))), sub=4)
        k_.scale = (1.5, 0.7, h / r)
    cit()
    gok_ogeleri(rnd)
    if serit_modu:
        for o in bpy.data.objects:
            if o.type == "MESH" and o.name.split(".")[0] not in ("zemin_yakin",):
                o.is_holdout = True


def kanal(rnd):
    """tarlayi enine kesen mavi kanal + yol uzerinde kemerli tahta kopru (korkuluk oyuncu renklerinde)"""
    y0, y1 = KANAL_Y
    su = mat_su("kanal", "#20d8ff", "#0a8cff")
    duz("kanal", -400, 400, y0, y1, 0.02, su)
    kenar = M("kanal_k", lambda: mat_pbr("kanal_k", "#7a4a26", 0.5, kaplama=0.2))
    for y in (y0, y1):
        yuvarlak_kutu("kanal_kenar", (0, y, 0.06), (800, 0.25, 0.2), kenar, egim=0.05, seg=1)
    tahta = M("kopru", lambda: mat_pbr("kopru", "#e09848", 0.45, kaplama=0.3, bump=(12, 0.2)))
    n = 9
    for i in range(n):
        t = i / (n - 1); y = y0 - 0.8 + t * (y1 - y0 + 1.6); z = 0.25 + 0.7 * math.sin(math.pi * t)
        yuvarlak_kutu("kopru_tahta", (0, y, z), (5.6, 0.42, 0.14), tahta, egim=0.04, seg=1)
    for s, R in ((-1, SERIT["p1"]), (1, SERIT["p2"])):
        bm = M("kor" + R["ana"], lambda r_=R["ana"]: mat_pbr("kor" + r_, r_, 0.3, kaplama=0.7))
        for i in range(n):
            t = i / (n - 1); y = y0 - 0.8 + t * (y1 - y0 + 1.6); z = 0.25 + 0.7 * math.sin(math.pi * t)
            boru((s * 2.75, y, z), (s * 2.75, y, z + 0.9), 0.06, bm)
        for i in range(n - 1):
            t0, t1 = i / (n - 1), (i + 1) / (n - 1)
            ya, yb = y0 - 0.8 + t0 * (y1 - y0 + 1.6), y0 - 0.8 + t1 * (y1 - y0 + 1.6)
            boru((s * 2.75, ya, 1.15 + 0.7 * math.sin(math.pi * t0)), (s * 2.75, yb, 1.15 + 0.7 * math.sin(math.pi * t1)), 0.07, bm)
    for k in range(6):                                                     # kanalda nilufer + ordek benzeri tombul kus yok: nilufer yapraklari
        x = rnd.choice((-1, 1)) * rnd.uniform(5, 30)
        n_ = kure((x, rnd.uniform(y0 + 0.5, y1 - 0.5), 0.04), 0.45, M("nil", lambda: mat_pbr("nil", "#2fd04a", 0.35, kaplama=0.5)), sub=2)
        n_.scale = (1.0, 1.0, 0.08)
        kure((x + 0.15, n_.location.y, 0.12), 0.12, M("nilc", lambda: mat_pbr("nilc", "#ff6ab8", 0.3, kaplama=0.7)), sub=2)


def degirmen(taban, boy, aci):
    """tombul yel degirmeni: hafif konik govde (beyaz siva + kirmizi tugla bant), koyu kubbe sapka, kapi/pencere,
    4 kanat (kafes cerceve + beyaz yelken), merkez gobek; kanatlar acisi 'aci'"""
    x, y, z = taban
    siva = M("deg_siva", lambda: mat_pbr("deg_siva", "#fff6ea", 0.45, kaplama=0.3, bump=(8, 0.15)))
    tugla = M("deg_tugla", lambda: mat_pbr("deg_tugla", "#e8362c", 0.4, kaplama=0.35, bump=(10, 0.2)))
    sapka = M("deg_sapka", lambda: mat_pbr("deg_sapka", "#2a5ad8", 0.35, kaplama=0.5))
    ahsap = M("deg_ahsap", lambda: mat_pbr("deg_ahsap", "#8a4e22", 0.5, kaplama=0.2))
    yelken = M("deg_yelken", lambda: mat_pbr("deg_yelken", "#fffdf6", 0.5, kaplama=0.2))
    gov_h = boy * 0.62
    bpy.ops.mesh.primitive_cone_add(radius1=boy * 0.16, radius2=boy * 0.11, depth=gov_h, location=(x, y, gov_h / 2), vertices=32)
    g = bpy.context.active_object; g.data.materials.append(siva); bpy.ops.object.shade_smooth()
    bpy.ops.mesh.primitive_cylinder_add(radius=boy * 0.165, depth=boy * 0.08, location=(x, y, boy * 0.04), vertices=32)
    bpy.context.active_object.data.materials.append(tugla); bpy.ops.object.shade_smooth()
    bpy.ops.mesh.primitive_torus_add(major_radius=boy * 0.135, minor_radius=boy * 0.012, location=(x, y, gov_h * 0.55))
    bpy.context.active_object.data.materials.append(tugla); bpy.ops.object.shade_smooth()
    s_ = kure((x, y, gov_h), boy * 0.13, sapka, sub=3); s_.scale = (1.0, 1.0, 0.8)
    yuvarlak_kutu("deg_kapi", (x, y - boy * 0.155, boy * 0.07), (boy * 0.07, 0.1, boy * 0.12), ahsap, egim=0.05, seg=2)
    for zz in (gov_h * 0.35, gov_h * 0.7):
        yuvarlak_kutu("deg_pen", (x, y - boy * 0.14 + zz * 0.0, zz), (boy * 0.045, 0.1, boy * 0.055), sapka, egim=0.03, seg=2)
    gy = y - boy * 0.16; gz = gov_h + boy * 0.02
    kure((x, gy, gz), boy * 0.035, ahsap, sub=2)
    L = boy * 0.5
    for k in range(4):
        a = aci + k * math.pi / 2
        d = Vector((math.cos(a), 0, math.sin(a))); dik = Vector((-math.sin(a), 0, math.cos(a)))
        merk = Vector((x, gy - 0.1, gz))
        boru(tuple(merk), tuple(merk + d * L), boy * 0.012, ahsap)
        # yelken: kolun bir yaninda dikdortgen (kafes cizgileri ahsap)
        p0 = merk + d * (L * 0.2); p1 = merk + d * L
        w = boy * 0.085
        me = bpy.data.meshes.new("yelken")
        me.from_pydata([tuple(p0), tuple(p1), tuple(p1 + dik * w), tuple(p0 + dik * w)], [], [[0, 1, 2, 3]]); me.update()
        o = bpy.data.objects.new("yelken", me); bpy.context.collection.objects.link(o); o.data.materials.append(yelken)
        o.modifiers.new("k", "SOLIDIFY").thickness = boy * 0.004
        for t in (0.2, 0.47, 0.73, 1.0):
            pa = merk + d * (L * t); boru(tuple(pa), tuple(pa + dik * w), boy * 0.005, ahsap)
        boru(tuple(p0 + dik * w), tuple(p1 + dik * w), boy * 0.006, ahsap)


def balya(xy, olcek, aci, rnd):
    x, y = xy
    sm = M("saman", lambda: mat_saman("saman"))
    bpy.ops.mesh.primitive_cylinder_add(radius=0.65 * olcek, depth=1.1 * olcek, location=(x, y, 0.65 * olcek), vertices=32,
                                        rotation=(0, math.pi / 2, aci))
    o = bpy.context.active_object; o.data.materials.append(sm)
    bv = o.modifiers.new("egim", "BEVEL"); bv.width = 0.12 * olcek; bv.segments = 3; bv.limit_method = "NONE"
    bpy.ops.object.shade_smooth()
    return o


def agac(taban, boy, rnd):
    x, y, z = taban
    for k in range(3):
        renk = ("#27c43e", "#1aa63a", "#4ad94a")[k]
        kk = kure((x + rnd.uniform(-0.3, 0.3) * boy, y, boy * 0.55 + rnd.uniform(-0.1, 0.15) * boy), boy * rnd.uniform(0.25, 0.33),
                  M("tac%d" % k, lambda r_=renk, k_=k: mat_pbr("tac%d" % k_, r_, 0.45, kaplama=0.3, bump=(3, 0.3))), sub=3)
        kk.scale = (1.15, 1.0, 0.9)


def cit():
    """tarla kenarinda (kanal onu) alcak beyaz ahsap cit - ufka kosan siralari cerceveler"""
    beyaz = M("cit", lambda: mat_pbr("cit", "#fffaf0", 0.45, kaplama=0.3))
    for s in (-1, 1):
        x0 = s * 46
        for k in range(26):
            y = 12 + k * 1.2
            if KANAL_Y[0] - 0.4 < y < KANAL_Y[1] + 0.4:
                continue
            yuvarlak_kutu("cit_d", (x0, y, 0.45), (0.14, 0.14, 0.9), beyaz, egim=0.04, seg=1)
        yuvarlak_kutu("cit_t", (x0, (12 + KANAL_Y[0]) / 2, 0.7), (0.08, KANAL_Y[0] - 12, 0.12), beyaz, egim=0.03, seg=1)


def bulut(merkez, olcek, rnd):
    beyaz = M("bulut", lambda: mat_pbr("bulut", "#f4fbff", 0.85))
    x, y, z = merkez
    for k in range(9):
        r = olcek * rnd.uniform(0.45, 0.85)
        dx = rnd.uniform(-1.5, 1.5) * olcek; dz = rnd.uniform(-0.2, 0.55) * olcek * (1 - abs(dx) / (2 * olcek))
        b = kure((x + dx, y + rnd.uniform(-0.4, 0.4) * olcek, z + dz), r, beyaz, sub=3); b.scale = (1.15, 0.8, 0.9)
    kure((x, y, z - 0.25 * olcek), olcek * 0.75, beyaz).scale = (2.4, 0.8, 0.45)


def kus(konum, olcek, renk, rnd):
    """tombul ucan kus: govde + iki kanat ucgeni + turuncu gaga"""
    x, y, z = konum
    g = kure((x, y, z), 0.4 * olcek, M("kus" + renk, lambda: mat_pbr("kus" + renk, renk, 0.35, kaplama=0.6)), sub=2); g.scale = (0.85, 1.5, 0.8)
    kure((x, y - 0.65 * olcek, z + 0.08 * olcek), 0.1 * olcek, M("gaga", lambda: mat_pbr("gaga", "#ff9a1e", 0.3, kaplama=0.7)), sub=2)
    k = rnd.uniform(0.3, 0.9)
    for s in (-1, 1):
        me = bpy.data.meshes.new("kanat")
        me.from_pydata([(x, y - 0.25 * olcek, z), (x + s * 1.6 * olcek, y, z + k * olcek), (x, y + 0.45 * olcek, z)], [], [[0, 1, 2]]); me.update()
        o = bpy.data.objects.new("kanat", me); bpy.context.collection.objects.link(o)
        o.data.materials.append(M("kus" + renk, lambda: mat_pbr("kus" + renk, renk, 0.35, kaplama=0.6))); o.modifiers.new("k", "SOLIDIFY").thickness = 0.05 * olcek


def kelebek(konum, olcek, renk):
    x, y, z = konum
    for s in (-1, 1):
        for (dz, w) in ((0.25, 1.0), (-0.3, 0.7)):
            k = kure((x + s * 0.45 * olcek, y, z + dz * olcek), 0.42 * olcek * w, M("kel" + renk, lambda: mat_pbr("kel" + renk, renk, 0.3, kaplama=0.8)), sub=2)
            k.scale = (1.0, 0.12, 0.8)
    boru((x, y, z - 0.4 * olcek), (x, y, z + 0.45 * olcek), 0.05 * olcek, M("kel_g", lambda: mat_pbr("kel_g", "#20242a", 0.5)))


def gok_ogeleri(rnd):
    """ekran dolu kurali (md. 7): bulut kumeleri, kus suruleri, kelebekler, ruzgarda ucusan lale yapraklari"""
    for (x, y, z, o) in ((-150, 260, 70, 16), (-60, 300, 95, 20), (40, 280, 80, 17), (140, 250, 62, 15), (230, 320, 100, 22),
                         (-240, 320, 110, 22), (0, 330, 120, 20),
                         (190, 200, 40, 9), (-200, 230, 42, 10), (60, 360, 140, 26), (-140, 360, 150, 26)):
        bulut((x, y, z), o, rnd)
    for k in range(12):
        kus((rnd.uniform(-22, 22), rnd.uniform(28, 55), rnd.uniform(9, 20)), rnd.uniform(0.6, 0.9),
            rnd.choice(("#ffffff", "#ffffff", "#ffd21e", "#ff7a14")), rnd)
    for k in range(14):
        kelebek((rnd.uniform(-9, 9), rnd.uniform(13, 24), rnd.uniform(1.8, 5.5)), rnd.uniform(0.25, 0.4),
                rnd.choice(("#ff3ab4", "#ffd21e", "#1e9cff", "#ff7a14", "#a040ff")))
    for k in range(40):                                                    # ucusan lale yapraklari
        renk = rnd.choice(LALE[:5])
        p = kure((rnd.uniform(-12, 12), rnd.uniform(12, 30), rnd.uniform(1.5, 8.0)), rnd.uniform(0.08, 0.14),
                 M("yap" + renk, lambda r_=renk: mat_pbr("yap" + r_, r_, 0.3, kaplama=0.7)), sub=1)
        p.scale = (1.0, 0.25, 1.6); p.rotation_euler = (rnd.uniform(0, 3), rnd.uniform(0, 3), rnd.uniform(0, 3))


# ------------------------------------------------------------------ SERIT: oyuncu tahta yolu + lale siniri + OUT saman yigini + kapi
def serit_esyalari(oyuncu, R, rnd):
    s_dis = -1 if oyuncu == "p1" else 1
    yol = mat_tahta("serit_yol", "#ff7a14", "#ff9a26", ara="#8a2a08")
    duz("serit_yol", -1.6, 1.6, -4, GECIS, 0.006, yol)
    kenar = M("bordur", lambda: mat_pbr("bordur", "#9a5a2a", 0.45, kaplama=0.3, bump=(14, 0.2)))
    for x in (-1.75, 1.75):                                                # serit siniri: alcak tahta bordur + oyuncu renginde laleler
        yuvarlak_kutu("bordur", (x, (KAP["y"] - 4) / 2 - 0.3, 0.12), (0.32, KAP["y"] + 3.4, 0.26), kenar, egim=0.08, seg=2)
        y = -3.4
        while y < KAP["y"] - 0.8:
            lale_koy(R["ana"], (x + (0.32 if x > 0 else -0.32), y, 0), 0.75, rnd)
            y += 0.8
    boya = mat_pbr("ok_" + oyuncu, R["ana"], 0.35, kaplama=0.6)
    for y in (4.9, 6.4):                                                   # tahta yolda oyuncu renginde boyali yon oklari (seri sabiti)
        nok = [(-0.75, y - 0.45), (0, y), (0.75, y - 0.45), (0.75, y - 0.75), (0, y - 0.3), (-0.75, y - 0.75)]
        me = bpy.data.meshes.new("ok"); me.from_pydata([(a, b, 0.014) for a, b in nok], [], [list(range(6))]); me.update()
        o = bpy.data.objects.new("ok", me); bpy.context.collection.objects.link(o); o.data.materials.append(boya)
        o.modifiers.new("k", "SOLIDIFY").thickness = 0.02
    # OUT ani: dis tarafta saman yigini (iki yuvarlak balya + kabarik gevsek saman tepesi; karakter buraya gomulur)
    cx, cy = s_dis * 2.95, 5.2
    sm = M("saman", lambda: mat_saman("saman"))
    yig = kure((cx, cy, 0.0), 1.15, sm, sub=4); yig.scale = (1.0, 1.7, 0.62)
    for k in range(14):
        a = rnd.uniform(0, 6.28)
        t_ = kure((cx + 0.9 * math.cos(a), cy + 1.5 * math.sin(a), rnd.uniform(0.05, 0.5)), rnd.uniform(0.2, 0.35), sm, sub=2)
        t_.scale = (1.3, 1.0, 0.7)
    balya((s_dis * 4.4, 7.4), 1.0, 0.4 * s_dis, rnd)
    balya((s_dis * 4.0, 3.2), 0.85, -0.3 * s_dis, rnd)
    # dis tarafta yakin lale siralari (tarla serit katmaninda da gorunsun): x 6..20, y -4..GECIS
    for i in range(12):
        x = s_dis * (6.2 + i * 1.25); renk = LALE[(i + 2) % len(LALE)]
        mat = M("sira" + renk, lambda r_=renk: mat_lale_sira("sira" + r_, r_))
        yuvarlak_kutu("sira_yakin", (x, (GECIS - 2.0) / 2, 0.5), (1.0, GECIS + 2.0, 1.0), mat, egim=0.4, seg=3)
    # dis tarafta kir esyalari: lale saksisi, ahsap kova, kisa cit
    for k, renk in enumerate(("#ffd21e", "#ff7a14", "#a040ff")):
        lale_koy(renk, (s_dis * (5.2 + 0.25 * k), 9.4 + 0.3 * k, 0), 1.3, rnd)
    yuvarlak_kutu("saksi", (s_dis * 5.4, 9.6, 0.25), (1.2, 0.8, 0.5), M("saksi", lambda: mat_pbr("saksi", "#d8562a", 0.4, kaplama=0.4)), egim=0.12, seg=2)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.28, depth=0.5, location=(s_dis * 3.9, 9.8, 0.25), vertices=20)
    bpy.context.active_object.data.materials.append(M("kova", lambda: mat_pbr("kova", "#2fa0ff" if oyuncu == "p1" else "#ffd21e", 0.3, kaplama=0.6)))
    # ic tarafta (hakem yeri) kucuk fener direkleri - fener kendi isigi (emission serbest)
    for yy in (2.5, 7.4):
        fener((-s_dis * 2.45, yy))


def fener(xy):
    x, y = xy
    boru((x, y, 0), (x, y, 1.2), 0.05, M("fen_g", lambda: mat_pbr("fen_g", "#2a3a4a", 0.4, metal=0.6)))
    yuvarlak_kutu("fen_k", (x, y, 1.36), (0.22, 0.22, 0.3), M("fen_c", lambda: mat_pbr("fen_c", "#2a3a4a", 0.4, metal=0.6)), egim=0.03, seg=1)
    kure((x, y, 1.36), 0.09, M("alev", lambda: mat_emis("alev", lin(hex3("#ffd27a")), 6.0)), sub=2)


def kapi(R):
    """ahsap ambar kapisi cercevesi: kirmizi boyali iki direk + kiris, beyaz capraz destek (ambar X'i), oyuncu renginde bantlar,
    kirisin ustunde ucgen catilik, ampul dizisi, ustte sonuk LED tabela (motor PLAYER n yazar)"""
    Y, W_, H_, K = KAP["y"], KAP["w"], KAP["h"], KAP["kalin"]
    kirmizi = mat_pbr("kapi_kirmizi", "#e2302a", 0.4, kaplama=0.45, bump=(10, 0.15))
    beyaz = mat_pbr("kapi_beyaz", "#fffaf0", 0.4, kaplama=0.4)
    boya = mat_pbr("kapi_boya", R["ana"], 0.25, kaplama=0.9)
    xk = W_ / 2 + K / 2
    for s in (-1, 1):
        yuvarlak_kutu("direk", (s * xk, Y, (H_ + K) / 2), (K, K, H_ + K), kirmizi, egim=0.1, seg=3)
        for z in (0.6, 1.6, 2.6):
            yuvarlak_kutu("bant", (s * xk, Y, z), (K + 0.06, K + 0.06, 0.16), boya, egim=0.05, seg=2)
        yuvarlak_kutu("kaide", (s * xk, Y, 0.15), (K + 0.3, K + 0.3, 0.3), beyaz, egim=0.08, seg=2)
        boru((s * (xk - K / 2), Y - K / 2 - 0.05, H_ - 0.9), (s * (xk - K / 2 - 0.9), Y - K / 2 - 0.05, H_), 0.07, beyaz)   # kose capraz destek
    yuvarlak_kutu("kiris", (0, Y, H_ + K / 2), (W_ + 2 * K + 0.3, K, K), kirmizi, egim=0.1, seg=3)
    yuvarlak_kutu("kiris_bant", (0, Y - K / 2 - 0.02, H_ + K / 2), (W_ + 2 * K, 0.06, 0.18), boya, egim=0.02, seg=1)
    for s in (-1, 1):                                                      # kiris ustunde ucgen catilik (beyaz kenarli)
        boru((s * (W_ / 2 + K + 0.2), Y, H_ + K), (0, Y, H_ + K + 1.15), 0.12, beyaz)
    ampul = M("ampul", lambda: mat_emis("ampul", lin(hex3("#ffe08a")), 5.0))
    for i in range(9):
        xx = -W_ / 2 + W_ * i / 8
        kure((xx, Y - K / 2 - 0.08, H_ - 0.05 - 0.12 * math.sin(math.pi * i / 8)), 0.07, ampul, sub=2)
    yuvarlak_kutu("tabela", (0, Y - 0.3, H_ + K + 0.5), (W_ * 0.85, 0.2, 0.7), mat_pbr("tabela", "#15171a", 0.35, metal=0.4), egim=0.05, seg=3)
    me = bpy.data.meshes.new("led_yuz"); a, b = W_ * 0.4, 0.28; z0 = H_ + K + 0.5
    me.from_pydata([(-a, Y - 0.41, z0 - b), (a, Y - 0.41, z0 - b), (a, Y - 0.41, z0 + b), (-a, Y - 0.41, z0 + b)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("led_yuz", me); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat_emis("led_yuz", lin(hex3(R["koyu"])), 1.2))
    rnd = random.Random(7 + (R["ana"] == SERIT["p2"]["ana"]))
    for s in (-1, 1):                                                      # direk diplerinde lale obekleri
        for k in range(5):
            lale_koy(LALE[(k + (s > 0)) % 5], (s * (xk + 0.5 + rnd.uniform(0, 0.4)), Y - 0.5 + rnd.uniform(-0.3, 0.3), 0), 1.0, rnd)


def mat_parlama_kis():
    """buyuk yuzeylerde (cim, tahta, saman, tepe, lale siralari) beyaz yansima doygunlugu yiyor -> specular/coat dusuk"""
    for m in bpy.data.materials:
        if not m.use_nodes or "Principled BSDF" not in m.node_tree.nodes:
            continue
        if m.name.split(".")[0].startswith(("cim", "tahta_yol", "serit_yol", "saman", "bordur", "tepe", "tac", "sira")):
            b = m.node_tree.nodes["Principled BSDF"]
            b.inputs["Specular IOR Level"].default_value = 0.18
            b.inputs["Coat Weight"].default_value = min(0.1, b.inputs["Coat Weight"].default_value)


def serit_katmani(oyuncu):
    R = SERIT[oyuncu]
    sc = lale_sahnesi(960, 1080, True)
    kam = kamera(sc)
    rnd = random.Random(30 + (oyuncu == "p2"))
    isiklar()
    tarla(True, random.Random(30))
    serit_esyalari(oyuncu, R, rnd)
    kapi(R)
    Y, W_, H_ = KAP["y"], KAP["w"], KAP["h"]
    ic = W_ / 2
    bpy.context.view_layer.update()
    px = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-ic, Y, 0), (ic, Y, 0), (-ic, Y, H_), (ic, Y, H_))]
    xs = [p.x * 960 for p in px]; ys = [(1 - p.y) * 1080 for p in px]
    YERLESIM["aciklik_" + oyuncu] = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
    # OUT ani: saman yiginin ekrandaki yeri; motor 22/23/26 anahtar duzeni korunur (minder = saman yigini)
    mk = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-2.95, 5.2, 0.4), (2.95, 5.2, 0.4), (0, GECIS, 0))]
    d = {"minder_sol_x": round(mk[0].x * 960, 1), "minder_sag_x": round(mk[1].x * 960, 1),
         "minder_y": round((1 - mk[0].y) * 1080, 1), "gecis_y": round((1 - mk[2].y) * 1080, 1)}
    for on in ("salon_", "plaj_", "orman_", "lale_"):
        YERLESIM[on + oyuncu] = d
    YERLESIM["yol"] = {"y_kapi": Y, "genislik": YOL_YARI * 2, "kam": KAM, "serit_w": 960}
    log("aciklik", oyuncu, YERLESIM["aciklik_" + oyuncu], d)
    mat_parlama_kis()
    yaz(sc, ON_EK + "serit-%s.png" % oyuncu)


def gok_katmani(ad):
    sc = lale_sahnesi(1920, 1080, False)
    kamera(sc)
    isiklar()
    tarla(False, random.Random(30))
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
log("bitti (lale)", YERLESIM.get("aciklik_p1"), YERLESIM.get("aciklik_p2"))
