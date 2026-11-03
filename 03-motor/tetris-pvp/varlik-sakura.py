"""HUMAN TETRIS 16. video (REF-067 TetrisBounce, 1v1) - SAKURA KOPRUSU sahne varliklari, IKI RENKLI serit. varlik.py calistirir (--mod sakura).

REF-067'de ne varsa (md. 22): 2B cizim gorunumu -> Blender'da duz renk (emisyon) + Freestyle kontur cizgisi ("toon").
Sol serit tamamen MAVI, sag serit tamamen PEMBE: parlayan karolu kopru yolu (ortada cicekli plakalar), fenerli kalin korkuluk,
kendi renginde kalin cerceveli kafes kapi. Gok: mor -> pembe -> turuncu aksam, ustte ve yanlarda dolu sakura tacleri, yaprak, yildiz.
Alinmaz (telif, kullanici 3 Kas 2026): anime kiz, "TOMOYO", kanatli yildiz amblemi, ucan sari yaratik.
Girdapli kart, 3-2-1, HUD, yazi kartlari motorda / kapak betiginde.

Ciktilar:
  gok.png            1920x1080  aksam gogu + sakura (opak)
  serit-p1.png       960x1080   MAVI serit (gokte saydam)
  serit-p2.png       960x1080   PEMBE serit
  panel-p1/p2.png    1100x904   beyaz duz panel (girdap motorda)
  kapak modu (--yalniz kapak): kapak-gok.png, kapak-serit-p1.png, kapak-serit-p2.png (kapak kamerasi)
"""

import random
YERLESIM.clear()
KAP = {"y": 8.0, "w": 4.6, "h": 4.1, "kalin": 0.5}
KAM = {"z": 1.7, "egim": -1.2, "lens": 17.0, "sensor": 24.0}
YOL_YARI = 2.3
KAPAK = YALNIZ == "kapak"
POZLAMA = float(arg("--kapak-pozlama", "0"))
ON_EK = "kapak-" if KAPAK else ""
if KAPAK:   # REF-067 kapagi: kapi buyuk, tepesi ustten ~%20, tabani ~%78
    KAM["lens"] = 15.0; KAM["egim"] = 2.6; KAM["z"] = 1.5
CIZGI = (0.10, 0.03, 0.22)        # kontur rengi: koyu mor (referansin cizgisi siyah degil, koyu mor)
SERIT = {
    "p1": {"ana": "#18b8ff", "acik": "#9cf0ff", "koyu": "#0a4fc8", "zemin": "#1a86ff", "zemin_u": "#3a2a9a"},
    "p2": {"ana": "#ff32c8", "acik": "#ffb4ec", "koyu": "#b0108c", "zemin": "#f01ab0", "zemin_u": "#5a1a8a"},
}


def toon(sc, kalin=2.2):
    """REF-067 cizim gorunumu: her cismin dis hatti koyu mor kontur (Freestyle, Cycles'ta son islem)"""
    sc.render.use_freestyle = True
    sc.render.line_thickness_mode = "ABSOLUTE"; sc.render.line_thickness = kalin
    vl = sc.view_layers[0]; vl.use_freestyle = True
    fs = vl.freestyle_settings
    ls = fs.linesets[0] if len(fs.linesets) else fs.linesets.new("cizgi")
    ls.select_by_visibility = True; ls.select_by_edge_types = True
    ls.select_silhouette = True; ls.select_border = True; ls.select_crease = False
    if ls.linestyle is None:
        ls.linestyle = bpy.data.linestyles.new("cz")
    ls.linestyle.color = CIZGI; ls.linestyle.thickness = kalin


def kamera(sc):
    rx = math.radians(90 - KAM["egim"])
    bpy.ops.object.camera_add(location=(0, 0, KAM["z"]), rotation=(rx, 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.sensor_fit = "VERTICAL"; kam.data.sensor_height = KAM["sensor"]; kam.data.lens = KAM["lens"]
    kam.data.clip_end = 900
    return kam


def mat_dikey(ad, alt, ust, z0, z1, guc=1.0, eksen="Z"):
    """duz renk ama bir eksende iki ton gecis (cizimdeki boyama gibi)"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord"); sp = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Object"], sp.inputs[0])
    mr = nt.nodes.new("ShaderNodeMapRange"); mr.inputs["From Min"].default_value = z0; mr.inputs["From Max"].default_value = z1
    nt.links.new(sp.outputs[eksen], mr.inputs["Value"])
    rp = nt.nodes.new("ShaderNodeValToRGB"); nt.links.new(mr.outputs[0], rp.inputs[0])
    rp.color_ramp.elements[0].color = (*lin(hex3(alt)), 1); rp.color_ramp.elements[1].color = (*lin(hex3(ust)), 1)
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs[1].default_value = guc; nt.links.new(rp.outputs[0], em.inputs[0])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], o.inputs[0])
    return m


def parlat(sc, esik=1.0, boy=7, mix=0.12):
    sc.use_nodes = True; sc.render.use_compositing = True; nt = sc.node_tree; nt.nodes.clear()
    rl = nt.nodes.new("CompositorNodeRLayers"); g = nt.nodes.new("CompositorNodeGlare"); o = nt.nodes.new("CompositorNodeComposite")
    g.glare_type = "FOG_GLOW"; g.quality = "HIGH"; g.threshold = esik; g.size = boy; g.mix = mix
    nt.links.new(rl.outputs["Image"], g.inputs[0]); nt.links.new(g.outputs[0], o.inputs[0]); nt.links.new(rl.outputs["Alpha"], o.inputs[1])


def cicek(x, y, z, r, mat, orta, ekse="Z"):
    """5 yaprakli sakura cicegi: yassi kureler (yol plakasinda ve gokte ayni sekil)"""
    for i in range(5):
        t = i / 5 * 2 * math.pi + math.pi / 2
        if ekse == "Z":
            k = kure((x + math.cos(t) * r * 0.62, y + math.sin(t) * r * 0.62, z), r * 0.5, mat, sub=1); k.scale = (1, 1, 0.18)
        else:
            k = kure((x + math.cos(t) * r * 0.62, y, z + math.sin(t) * r * 0.62), r * 0.5, mat, sub=1); k.scale = (1, 0.18, 1)
    kure((x, y, z + (0.01 if ekse == "Z" else 0)), r * 0.22, orta, sub=1)


# ------------------------------------------------------------------ GOK: ortografik; x -960..960, z 0..1080
def gok_katmani(ad):
    sc = bos_sahne(w=1920, h=1080, ornek=min(ORNEK, 16))
    bpy.ops.object.camera_add(location=(0, -900, 540), rotation=(math.radians(90), 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.type = "ORTHO"; kam.data.ortho_scale = 1920; kam.data.clip_end = 3000
    toon(sc, 2.0)
    # aksam gogu: ustte koyu mor, ortada pembe-kirmizi, ufukta turuncu (REF-067 sol kenari)
    zem = bpy.data.materials.new("gok"); zem.use_nodes = True; nt = zem.node_tree; nt.nodes.clear()
    # 1. deneme: duzlem X'te 90 derece donuk, "Object Z" hep 0 -> gok tek renk koyu kaldi; Generated Y duzlemin dikeyi
    tc = nt.nodes.new("ShaderNodeTexCoord"); sp = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Generated"], sp.inputs[0])
    rp = nt.nodes.new("ShaderNodeValToRGB"); cr = rp.color_ramp; nt.links.new(sp.outputs["Y"], rp.inputs[0])
    cr.elements[0].position = 0.36; cr.elements[0].color = (*lin(hex3("#ffa040")), 1)
    cr.elements[1].position = 0.95; cr.elements[1].color = (*lin(hex3("#5a2ad0")), 1)
    e = cr.elements.new(0.50); e.color = (*lin(hex3("#ff4a8a")), 1)
    e = cr.elements.new(0.72); e.color = (*lin(hex3("#c03ad8")), 1)
    em = nt.nodes.new("ShaderNodeEmission"); nt.links.new(rp.outputs[0], em.inputs[0])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], o.inputs[0])
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 600, 540), rotation=(math.radians(90), 0, 0))
    p = bpy.context.active_object; p.scale = (2000, 1100, 1); bpy.ops.object.transform_apply(scale=True)
    p.data.materials.append(zem)
    rnd = random.Random(67)
    beyaz = mat_emis("yildiz", lin(hex3("#fff4ff")), 3.0)
    for _ in range(70):                                    # yildiz / isik tozu
        kure((rnd.uniform(-960, 960), 400, rnd.uniform(560, 1060)), rnd.choice((1.5, 2.2, 3.2)), beyaz, sub=1)
    # uzak tepeler + ufukta fener isiklari (bos ufuk kalmasin)
    tepe = mat_emis("tepe", lin(hex3("#4a1a6a")), 1.0)
    for i in range(9):
        x = -960 + i * 240 + rnd.uniform(-60, 60)
        k = kure((x, 300, 360), rnd.uniform(150, 230), tepe, sub=2); k.scale = (1.4, 0.3, 0.55)
    fener = mat_emis("ufuk_fener", lin(hex3("#ffd27a")), 4.0)
    for i in range(40):
        kure((rnd.uniform(-960, 960), 250, rnd.uniform(330, 420)), rnd.choice((2.5, 3.5)), fener, sub=1)
    # SAKURA TACI: ustte tam bant + yanlarda asagi sarkan kumeler; 3 pembe ton + mor golge
    tonlar = [mat_emis("sk%d" % i, lin(hex3(c)), g) for i, (c, g) in enumerate((("#ff9ae0", 1.2), ("#ff5ac8", 1.15), ("#e82aa8", 1.05), ("#9a2ad8", 1.0)))]
    dal = mat_emis("dal", lin(hex3("#2a0e3a")), 1.0)
    for sx in (-1, 1):                                     # dallar: kenardan ortaya
        boru((sx * 1000, 100, 760), (sx * 520, 100, 980), 16, dal)
        boru((sx * 760, 100, 860), (sx * 860, 100, 520), 11, dal)
        boru((sx * 600, 100, 960), (sx * 200, 100, 1040), 10, dal)
    n = 0
    while n < 520:
        x = rnd.uniform(-1000, 1000)
        kenar = abs(x) > 560
        z = rnd.uniform(470 if kenar else 760, 1120)
        if not kenar and z < 860 and rnd.random() < 0.45:
            continue
        y = rnd.uniform(-40, 80)
        r = rnd.uniform(26, 62)
        m = tonlar[3] if y > 50 else rnd.choice(tonlar[:3])
        kure((x, y, z), r, m, sub=2); n += 1
    ic = mat_emis("ck_ic", lin(hex3("#fff0fa")), 1.4); orta = mat_emis("ck_orta", lin(hex3("#ff4aa0")), 1.6)
    for _ in range(46):                                    # tacin onunde tek tek cicekler
        x = rnd.uniform(-960, 960); z = rnd.uniform(820, 1060) if abs(x) < 560 else rnd.uniform(520, 1060)
        cicek(x, -80, z, rnd.uniform(14, 22), ic, orta, ekse="Y")
    fener_dizisi(rnd)
    yaprak = mat_emis("yaprak", lin(hex3("#ffc8ee")), 1.3)
    for _ in range(110):                                   # ucusan yapraklar (her yukseklikte)
        k = kure((rnd.uniform(-960, 960), -100, rnd.uniform(120, 1000)), rnd.uniform(4, 8), yaprak, sub=1)
        k.scale = (1.0, 0.3, 0.55); k.rotation_euler = (0, rnd.uniform(0, math.pi), 0)
    if KAPAK:
        sc.view_settings.exposure = POZLAMA
    parlat(sc, esik=1.2, boy=8, mix=0.08)
    yaz(sc, ad)


def fener_dizisi(rnd):
    """1. denemede iki kapi arasi gok bos kaldi (kapak doygunlugu 0,55 / ref 0,62): ortadan sarkan iki sira kagit fener"""
    ip = mat_emis("ip", lin(hex3("#3a0e4a")), 1.0)
    renk = [mat_emis("kf%d" % i, lin(hex3(c)), 2.6) for i, c in enumerate(("#ffb03a", "#ff5a9a", "#ffe06a", "#ff7ad8"))]
    for z0, sark, n in ((800, 120, 15), (690, 90, 13)):
        onc = None
        for i in range(n + 1):
            q = i / n; x = -960 + q * 1920; z = z0 - sark * 4 * q * (1 - q)
            if onc:
                boru((onc[0], -60, onc[1]), (x, -60, z), 2.2, ip)
            onc = (x, z)
            if 0 < i < n:
                k = kure((x, -70, z - 26), 22, renk[i % 4], sub=2); k.scale = (0.85, 0.85, 1.15)
                yuvarlak_kutu("fc", (x, -70, z - 2), (16, 16, 6), ip, egim=2, seg=2)


# ------------------------------------------------------------------ SERIT: her oyuncunun kendi renginde
def zemin(R):
    yol = mat_dikey("yol", R["zemin"], R["zemin_u"], 0.0, KAP["y"] + 1, 1.0, eksen="Y")
    _sekil("zemin", [(-YOL_YARI, -0.6), (YOL_YARI, -0.6), (YOL_YARI, KAP["y"] + 0.4), (-YOL_YARI, KAP["y"] + 0.4)], yol)
    derz = mat_emis("derz", lin(hex3(R["acik"])), 2.4)
    for x in (-1.15, -0.55, 0.55, 1.15):                   # karo derzleri: parlak ince cizgi
        boru((x, -0.6, 0.004), (x, KAP["y"], 0.004), 0.014, derz)
    yy = 0.4
    while yy < KAP["y"]:
        boru((-YOL_YARI, yy, 0.004), (YOL_YARI, yy, 0.004), 0.014, derz); yy += 0.75
    plaka = mat_emis("plaka", lin(hex3(R["ana"])), 2.6)
    ic = mat_emis("plaka_ck", lin(hex3("#ffffff")), 3.0); orta = mat_emis("plaka_orta", lin(hex3(R["acik"])), 3.0)
    yy = 0.6
    while yy < KAP["y"] - 0.4:                             # REF-067: yolun ortasinda cicekli parlayan plakalar
        yuvarlak_kutu("plaka", (0, yy + 0.3, 0.02), (1.0, 0.62, 0.04), plaka, egim=0.08, seg=3)
        cicek(0, yy + 0.3, 0.06, 0.2, ic, orta)
        yy += 1.5
    yaprak = mat_emis("yer_yaprak", lin(hex3("#ffd4f2")), 1.6)
    rnd = random.Random(16)
    for _ in range(70):                                    # yolda dagilmis yapraklar
        k = kure((rnd.uniform(-YOL_YARI, YOL_YARI), rnd.uniform(-0.4, KAP["y"]), 0.02), rnd.uniform(0.035, 0.06), yaprak, sub=1)
        k.scale = (1.0, 0.6, 0.15)


def _sekil(ad, noktalar, mat, z=0.0):
    me = bpy.data.meshes.new(ad)
    me.from_pydata([(a, b, z) for a, b in noktalar], [], [list(range(len(noktalar)))]); me.update()
    o = bpy.data.objects.new(ad, me); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat)
    return o


def korkuluk(R):
    dikme = mat_dikey("dikme", R["koyu"], R["ana"], 0.0, 1.0, 1.3)
    kus = mat_emis("kus", lin(hex3(R["acik"])), 3.2)
    fener = mat_emis("fener", lin(hex3("#fff2c0")), 4.5)
    fener_c = mat_emis("fener_c", lin(hex3(R["koyu"])), 1.0)
    pano = mat_dikey("pano", R["koyu"], R["ana"], 0.0, 0.8, 1.1)
    nokta = mat_emis("pano_ck", lin(hex3("#ffe6fa")), 2.0); orta = mat_emis("pano_orta", lin(hex3(R["acik"])), 2.0)
    for s in (-1, 1):
        x = s * YOL_YARI
        y0, y1 = -0.4, KAP["y"] - 0.5
        n = 6
        for j in range(n + 1):
            yy = y0 + j * (y1 - y0) / n
            yuvarlak_kutu("dikme", (x, yy, 0.55), (0.3, 0.3, 1.1), dikme, egim=0.05, seg=2)
            yuvarlak_kutu("fener_cati", (x, yy, 1.26), (0.42, 0.42, 0.1), fener_c, egim=0.04, seg=2)
            yuvarlak_kutu("fener", (x, yy, 1.16), (0.26, 0.26, 0.2), fener, egim=0.04, seg=2)
            if j < n:
                ym = yy + (y1 - y0) / n / 2; L = (y1 - y0) / n - 0.36
                yuvarlak_kutu("pano", (x, ym, 0.42), (0.1, L, 0.62), pano, egim=0.03, seg=2)
                for q in (-0.25, 0.25):
                    kure((x - s * 0.07, ym + q * L, 0.45), 0.06, nokta, sub=1)
        boru((x, y0, 0.95), (x, y1, 0.95), 0.06, kus)
        boru((x, y0, 0.12), (x, y1, 0.12), 0.05, kus)


def kapi(R):
    Y, W_, H_, K = KAP["y"], KAP["w"], KAP["h"], KAP["kalin"]
    cerceve = mat_dikey("cerceve", R["ana"], R["acik"], 0.0, H_ + K, 1.6)
    ic = mat_emis("kafes", lin(hex3(R["acik"])), 2.2)
    xk = W_ / 2 - K / 2
    for s in (-1, 1):
        yuvarlak_kutu("kule", (s * xk, Y, (H_ + K) / 2), (K, K, H_ + K), cerceve, egim=0.12, seg=3)
        kafes_kule(s * (xk + 0.42), Y + 0.05, 0.0, H_ * 0.8, 0.3, ic, ic)
    yuvarlak_kutu("kiris", (0, Y, H_ + K / 2), (W_, K, K), cerceve, egim=0.12, seg=3)
    kafes_kiris(-xk, xk, Y + 0.05, H_ + K + 0.3, 0.3, ic, ic)


def serit_katmani(oyuncu):
    R = SERIT[oyuncu]
    sc = bos_sahne(w=960, h=1080, saydam=True, ornek=min(ORNEK, 24))
    sc.cycles.transparent_max_bounces = 16
    kam = kamera(sc)
    toon(sc, 2.4)
    zemin(R); korkuluk(R); kapi(R)
    Y, W_, H_, K = KAP["y"], KAP["w"], KAP["h"], KAP["kalin"]
    ic = W_ / 2 - K
    bpy.context.view_layer.update()
    px = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-ic, Y, 0), (ic, Y, 0), (-ic, Y, H_), (ic, Y, H_))]
    xs = [p.x * 960 for p in px]; ys = [(1 - p.y) * 1080 for p in px]
    YERLESIM["aciklik_" + oyuncu] = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
    YERLESIM["yol"] = {"y_kapi": Y, "genislik": YOL_YARI * 2, "kam": KAM, "serit_w": 960}
    log("aciklik", oyuncu, YERLESIM["aciklik_" + oyuncu])
    if KAPAK:
        sc.view_settings.exposure = POZLAMA
    parlat(sc, esik=1.4, boy=7, mix=0.1)
    yaz(sc, ON_EK + "serit-%s.png" % oyuncu)


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
log("bitti (sakura)", YERLESIM.get("aciklik_p1"), YERLESIM.get("aciklik_p2"))
