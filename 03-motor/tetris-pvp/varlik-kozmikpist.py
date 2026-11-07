"""HUMAN TETRIS 21. video (REF-075 TetrisBounce, 1v1 PVP) - KOZMIK CAM PIST sahne varliklari. varlik.py calistirir (--mod kozmikpist).

REF-075'te ne varsa (md. 22): ekran ikiye bolunur, sol serit tamamen CAMGOBEGI-MAVI (P1), sag serit tamamen PEMBE (P2).
Her seritte parlak cam karolu zemin, kapiya dogru dort cam chevron cubugu ("^" seklinde, kenarlari neon), iki yanda kristal
babali cam korkuluk; kapi cift cerceve: dista ustu iki sira kare izgarali neon kafes, icte kalin neon cerceve (kart acikligi).
Gok: mor-lacivert yildizli galaksi + bulutsu, ortada mavi/pembe girdapli dev gezegen, onunden gecen egik isik izleri,
koyu kucuk gezegenler (kenar isikli), turuncu kucuk gezegenler, solda halkali gezegen.
Alinmaz (telif): anime kiz maskot, kepenk uzerindeki anime amblem. Kart, kepenk, 3-2-1, HUD, maskot motorda / kapak betiginde.

Ciktilar:
  gok.png            1920x1080  galaksi gogu (opak)
  serit-p1.png       960x1080   MAVI serit (gokte saydam, kapi acikligi saydam)
  serit-p2.png       960x1080   PEMBE serit
  panel-p1/p2.png    1100x904   beyaz duz panel
  yerlesim.json      aciklik_p1/p2 (serit koordinati), kamera
  kapak modu (--yalniz kapak): kapak-gok.png, kapak-serit-p1.png, kapak-serit-p2.png (kapak kamerasi)
"""

import random
YERLESIM.clear()
KAPAK = YALNIZ == "kapak"
POZLAMA = float(arg("--kapak-pozlama", "0"))
ON_EK = "kapak-" if KAPAK else ""
# REF-075 karesi (seritte, 640 px): dis kafes ust ~%24, kart alt ~%68, dis kafes genisligi seridin ~%58'i
KAP = {"y": 8.0, "w": 3.4, "h": 3.7, "kalin": 0.32, "kafes": 0.62}
KAM = {"z": 2.3, "egim": 5.0, "lens": 18.0, "sensor": 24.0}
if KAPAK:   # REF-075 kapagi: kapi ust ~%26, kapilar daha yakin ve buyuk
    KAM.update({"z": float(arg("--kapak-z", "2.0")), "egim": float(arg("--kapak-egim", "3.0")), "lens": float(arg("--kapak-lens", "16.0"))})
YOL_YARI = 2.6
SERIT = {
    "p1": {"ana": "#1ad2ff", "acik": "#a8f2ff", "koyu": "#0a5ad8", "zemin": "#1a8cff", "zemin_u": "#14286a"},
    "p2": {"ana": "#ff2ad2", "acik": "#ffb0f0", "koyu": "#b0108c", "zemin": "#f01ab4", "zemin_u": "#4a1060"},
}


def kamera(sc):
    rx = math.radians(90 - KAM["egim"])
    bpy.ops.object.camera_add(location=(0, 0, KAM["z"]), rotation=(rx, 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.sensor_fit = "VERTICAL"; kam.data.sensor_height = KAM["sensor"]; kam.data.lens = KAM["lens"]
    kam.data.clip_end = 900
    return kam


def parlat(sc, esik=1.0, boy=7, mix=0.12, saydam=True):
    sc.use_nodes = True; sc.render.use_compositing = True; nt = sc.node_tree; nt.nodes.clear()
    rl = nt.nodes.new("CompositorNodeRLayers"); g = nt.nodes.new("CompositorNodeGlare"); o = nt.nodes.new("CompositorNodeComposite")
    g.glare_type = "FOG_GLOW"; g.quality = "HIGH"; g.threshold = esik; g.size = boy; g.mix = mix
    nt.links.new(rl.outputs["Image"], g.inputs[0]); nt.links.new(g.outputs[0], o.inputs[0])
    if saydam:
        nt.links.new(rl.outputs["Alpha"], o.inputs[1])


def mat_dikey(ad, alt, ust, z0, z1, guc=1.0, eksen="Z"):
    """emisyon, bir eksende iki ton gecis"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord"); sp = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Object"], sp.inputs[0])
    mr = nt.nodes.new("ShaderNodeMapRange"); mr.inputs["From Min"].default_value = z0; mr.inputs["From Max"].default_value = z1
    nt.links.new(sp.outputs[eksen], mr.inputs["Value"])
    rp = nt.nodes.new("ShaderNodeValToRGB"); nt.links.new(mr.outputs[0], rp.inputs[0])
    rp.color_ramp.elements[0].color = (*lin(hex3(alt)), 1); rp.color_ramp.elements[1].color = (*lin(hex3(ust)), 1)
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs[1].default_value = guc; nt.links.new(rp.outputs[0], em.inputs[0])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], o.inputs[0])
    return m


def mat_kristal(ad, renk, guc=1.3, saydam=0.45):
    """REF-075 cam/kristal: kendi renginde isilti + yari saydam govde; kenarda (fresnel) daha parlak"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    lw = nt.nodes.new("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.35
    gm = nt.nodes.new("ShaderNodeMapRange"); gm.inputs["To Min"].default_value = guc * 0.6; gm.inputs["To Max"].default_value = guc * 2.6
    nt.links.new(lw.outputs["Fresnel"], gm.inputs["Value"])
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs[0].default_value = (*lin(hex3(renk)), 1); nt.links.new(gm.outputs[0], em.inputs[1])
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mx = nt.nodes.new("ShaderNodeMixShader"); mx.inputs[0].default_value = 1 - saydam
    nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(mx.outputs[0], o.inputs[0])
    return m


# ------------------------------------------------------------------ GOK: ortografik; x -960..960, z 0..1080
def mat_bulutsu():
    """mor-lacivert gok + mavi/pembe bulutsu (gurultu) - REF-075 galaksisi"""
    m = bpy.data.materials.new("gok"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sp = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Generated"], sp.inputs[0])
    taban = nt.nodes.new("ShaderNodeValToRGB"); cr = taban.color_ramp; nt.links.new(sp.outputs["Y"], taban.inputs[0])
    cr.elements[0].position = 0.0; cr.elements[0].color = (*lin(hex3("#3a1a8a")), 1)
    cr.elements[1].position = 1.0; cr.elements[1].color = (*lin(hex3("#120a3a")), 1)
    e = cr.elements.new(0.45); e.color = (*lin(hex3("#2a1a7a")), 1)
    ns = nt.nodes.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value = 3.2; ns.inputs["Detail"].default_value = 8; ns.inputs["Roughness"].default_value = 0.62
    nt.links.new(tc.outputs["Generated"], ns.inputs["Vector"])
    nr = nt.nodes.new("ShaderNodeValToRGB"); c2 = nr.color_ramp; nt.links.new(ns.outputs["Fac"], nr.inputs[0])
    c2.elements[0].position = 0.38; c2.elements[0].color = (0, 0, 0, 1)
    c2.elements[1].position = 0.78; c2.elements[1].color = (*lin(hex3("#ff5ad8")), 1)
    e = c2.elements.new(0.55); e.color = (*lin(hex3("#3a6aff")), 1)
    e = c2.elements.new(0.66); e.color = (*lin(hex3("#9a4aff")), 1)
    ad = nt.nodes.new("ShaderNodeMix"); ad.data_type = "RGBA"; ad.blend_type = "ADD"; ad.inputs[0].default_value = 0.85
    nt.links.new(taban.outputs[0], ad.inputs[6]); nt.links.new(nr.outputs[0], ad.inputs[7])
    em = nt.nodes.new("ShaderNodeEmission"); nt.links.new(ad.outputs[2], em.inputs[0])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], o.inputs[0])
    return m


def mat_dev_gezegen():
    """ortadaki dev gezegen: mavi / pembe / beyaz girdapli (wave + gurultu bozulma), kenara dogru isiyan hale"""
    m = bpy.data.materials.new("dev_gezegen"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord")
    wv = nt.nodes.new("ShaderNodeTexWave"); wv.wave_type = "BANDS"; wv.bands_direction = "DIAGONAL"
    wv.inputs["Scale"].default_value = 1.6; wv.inputs["Distortion"].default_value = 9.0; wv.inputs["Detail"].default_value = 6
    wv.inputs["Detail Scale"].default_value = 2.4
    nt.links.new(tc.outputs["Generated"], wv.inputs["Vector"])
    rp = nt.nodes.new("ShaderNodeValToRGB"); cr = rp.color_ramp; nt.links.new(wv.outputs["Fac"], rp.inputs[0])
    cr.elements[0].position = 0.0; cr.elements[0].color = (*lin(hex3("#1a3ad8")), 1)
    cr.elements[1].position = 1.0; cr.elements[1].color = (*lin(hex3("#e8f0ff")), 1)
    for pos, c in ((0.3, "#3a8cff"), (0.5, "#ff4ac8"), (0.68, "#8a5aff"), (0.85, "#ff9ae8")):
        e = cr.elements.new(pos); e.color = (*lin(hex3(c)), 1)
    lw = nt.nodes.new("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.5
    gm = nt.nodes.new("ShaderNodeMapRange"); gm.inputs["To Min"].default_value = 1.1; gm.inputs["To Max"].default_value = 2.6
    nt.links.new(lw.outputs["Fresnel"], gm.inputs["Value"])
    em = nt.nodes.new("ShaderNodeEmission"); nt.links.new(rp.outputs[0], em.inputs[0]); nt.links.new(gm.outputs[0], em.inputs[1])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], o.inputs[0])
    return m


def mat_koyu_gezegen(ad, kenar):
    """koyu kucuk gezegen: ici koyu lacivert, kenari mavi/pembe isik (REF-075'teki siyah gezegenler)"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    lw = nt.nodes.new("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.25
    mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"
    mx.inputs[6].default_value = (*lin(hex3("#1a1640")), 1); mx.inputs[7].default_value = (*lin(hex3(kenar)), 1)
    nt.links.new(lw.outputs["Fresnel"], mx.inputs[0])
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs[1].default_value = 1.6; nt.links.new(mx.outputs[2], em.inputs[0])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], o.inputs[0])
    return m


def isik_izi(cx, cz, rx, rz, a0, a1, y, kal, mat, egim=0.0, n=40):
    """egik elips yayi boyunca ince isik izi (REF-075: dev gezegenin onunden gecen pembe/mavi cizgiler)"""
    onc = None
    for i in range(n + 1):
        a = a0 + (a1 - a0) * i / n
        x = cx + rx * math.cos(a); z = cz + rz * math.sin(a)
        x, z = cx + (x - cx) * math.cos(egim) - (z - cz) * math.sin(egim), cz + (x - cx) * math.sin(egim) + (z - cz) * math.cos(egim)
        if onc:
            boru((onc[0], y, onc[1]), (x, y, z), kal, mat)
        onc = (x, z)


def gok_katmani(ad):
    sc = bos_sahne(w=1920, h=1080, ornek=min(ORNEK, 16))
    bpy.ops.object.camera_add(location=(0, -900, 540), rotation=(math.radians(90), 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.type = "ORTHO"; kam.data.ortho_scale = 1920; kam.data.clip_end = 3000
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 600, 540), rotation=(math.radians(90), 0, 0))
    p = bpy.context.active_object; p.scale = (2000, 1100, 1); bpy.ops.object.transform_apply(scale=True)
    p.data.materials.append(mat_bulutsu())
    rnd = random.Random(75)
    beyaz = mat_emis("yildiz", lin(hex3("#ffffff")), 3.2)
    mavi_y = mat_emis("yildiz_m", lin(hex3("#9ad8ff")), 3.0)
    for _ in range(260):                                   # yildiz tozu: gok bos kalmaz (md. 7)
        kure((rnd.uniform(-960, 960), 450, rnd.uniform(0, 1080)), rnd.choice((1.2, 1.8, 2.6, 3.6)), rnd.choice((beyaz, beyaz, mavi_y)), sub=1)
    # dev gezegen: kapilarin arasinda, ustten tasar (REF-075: merkez ~x 0, ust kenara degiyor)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=360, location=(40, 300, 760), segments=96, ring_count=48)
    g = bpy.context.active_object; bpy.ops.object.shade_smooth(); g.rotation_euler = (math.radians(20), math.radians(-30), math.radians(15))
    g.data.materials.append(mat_dev_gezegen())
    bpy.ops.mesh.primitive_uv_sphere_add(radius=392, location=(40, 760, 760), segments=96, ring_count=48)   # 1. deneme: hale (y 320) planeti tamamen ortuyordu
    h_ = bpy.context.active_object; bpy.ops.object.shade_smooth(); h_.data.materials.append(mat_emis("hale", lin(hex3("#5a8aff")), 0.35))
    # isik izleri: gezegenin onunden sola-asagi egik gecen pembe ve mavi cizgiler
    izler = [mat_emis("iz%d" % i, lin(hex3(c)), e) for i, (c, e) in enumerate((("#ff5ad8", 5.0), ("#7ad8ff", 5.0), ("#ffffff", 6.0), ("#ff2a9a", 4.0)))]
    for i in range(9):
        isik_izi(60, 650, 620 + i * 26, 120 + i * 9, math.radians(190), math.radians(355), 100 - i, rnd.uniform(1.6, 4.2), izler[i % 4], egim=math.radians(-24))
    # koyu kucuk gezegenler + turuncu kucuk gezegenler (her yukseklikte; gok bos kalmaz)
    koyu_m = [mat_koyu_gezegen("kg%d" % i, c) for i, c in enumerate(("#7aa8ff", "#ff7ad8", "#b48cff"))]
    for (x, z, r) in ((160, 640, 46), (-260, 900, 30), (420, 980, 22), (640, 560, 60), (-700, 760, 26), (820, 860, 38),
                      (-480, 520, 20), (300, 420, 18), (-880, 980, 16), (900, 420, 28)):
        kure((x, 120, z), r, rnd.choice(koyu_m), sub=3)
    turuncu = [mat_koyu_gezegen("tg%d" % i, c) for i, c in enumerate(("#ff8a4a", "#ff5a5a"))]
    for _ in range(14):
        kure((rnd.uniform(-940, 940), 140, rnd.uniform(380, 1060)), rnd.uniform(6, 14), rnd.choice(turuncu), sub=2)
    # solda halkali gezegen
    kure((-760, 160, 520), 34, mat_koyu_gezegen("halkali", "#9ad8ff"), sub=3)
    halka = mat_emis("halka", lin(hex3("#c8e8ff")), 3.0)
    isik_izi(-760, 520, 78, 20, 0, 2 * math.pi, 150, 3.0, halka, egim=math.radians(-12), n=60)
    # ufukta parlak pembe isilti (korkuluklarin arkasi, REF-075 sol / sag kenar)
    for sx in (-1, 1):
        k = kure((sx * 780, 200, 360), 220, mat_emis("ufuk%d" % sx, lin(hex3("#ff6ad8" if sx > 0 else "#7ab8ff")), 0.9), sub=3); k.scale = (1.4, 0.2, 0.45)
    if KAPAK:
        sc.view_settings.exposure = POZLAMA
    parlat(sc, esik=1.3, boy=8, mix=0.1, saydam=False)
    yaz(sc, ad)


# ------------------------------------------------------------------ SERIT: her oyuncunun kendi renginde
def _sekil(ad, noktalar, mat, z=0.0):
    me = bpy.data.meshes.new(ad)
    me.from_pydata([(a, b, z) for a, b in noktalar], [], [list(range(len(noktalar)))]); me.update()
    o = bpy.data.objects.new(ad, me); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat)
    return o


def zemin(R):
    """parlak cam karo zemin: yakinda acik, kapiya dogru koyu; karo derzleri parlak cizgi"""
    yol = mat_dikey("yol", R["zemin"], R["zemin_u"], -0.6, KAP["y"] + 2, 1.15, eksen="Y")
    _sekil("zemin", [(-YOL_YARI - 3, -0.6), (YOL_YARI + 3, -0.6), (YOL_YARI + 3, KAP["y"] + 6), (-YOL_YARI - 3, KAP["y"] + 6)], yol)
    derz = mat_emis("derz", lin(hex3(R["acik"])), 1.2)
    x = -YOL_YARI
    while x <= YOL_YARI + 0.01:
        boru((x, -0.6, 0.004), (x, KAP["y"] + 2, 0.004), 0.007, derz); x += YOL_YARI / 2
    yy = -0.4
    while yy < KAP["y"] + 2:
        boru((-YOL_YARI, yy, 0.004), (YOL_YARI, yy, 0.004), 0.007, derz); yy += 1.3
    # yansima lekesi: yakinda zeminde parlak beyazimsi bant (REF-075 cam zemin parlamasi)
    k = kure((0, 0.8, -0.02), 1.6, mat_emis("parlama", lin(hex3(R["acik"])), 0.8), sub=3); k.scale = (1.6, 1.0, 0.02)


def chevron(R, y, gen, kol, kal=0.36):
    """REF-075 cam chevron cubugu: apeksi kapiya bakan tek parca "^" prizma; kristal govde + ust kenarlarda neon cizgi
    (1. deneme: iki doner kutu kol dagildi, kenara kaydi -> tek cokgen + solidify)"""
    gov = mat_kristal("chev", R["ana"], 1.0, 0.25)
    kenar = mat_emis("chev_k", lin(hex3(R["acik"])), 3.0)
    nok = [(-gen, y - kol), (0, y), (gen, y - kol), (gen, y - kol - kal), (0, y - kal), (-gen, y - kol - kal)]
    o = _sekil("chev", nok, gov, z=0.02)
    so = o.modifiers.new("kal", "SOLIDIFY"); so.thickness = 0.16; so.offset = 1.0
    for s in (-1, 1):
        boru((0, y, 0.19), (s * gen, y - kol, 0.19), 0.02, kenar)
        boru((0, y - kal, 0.19), (s * gen, y - kol - kal, 0.19), 0.014, kenar)


def korkuluk(R):
    """kristal babali cam korkuluk: kalin dikmeler + aralarda tombul babalar + ustte cam kupeste"""
    dikme = mat_kristal("dikme", R["ana"], 0.9, 0.4)
    baba = mat_kristal("baba", R["ana"], 0.8, 0.5)
    kus = mat_emis("kus", lin(hex3(R["acik"])), 1.8)
    for s in (-1, 1):
        x = s * YOL_YARI
        y0, y1 = -0.6, KAP["y"] + 4.0
        n = 7
        for j in range(n + 1):
            yy = y0 + j * (y1 - y0) / n
            yuvarlak_kutu("dikme", (x, yy, 0.55), (0.24, 0.24, 1.1), dikme, egim=0.05, seg=2)
            kure((x, yy, 1.16), 0.15, baba, sub=2)
            if j < n:
                L = (y1 - y0) / n
                for q in range(1, 5):
                    yb = yy + q * L / 5
                    kure((x, yb, 0.3), 0.08, baba, sub=2)
                    k = kure((x, yb, 0.58), 0.11, baba, sub=2); k.scale = (1, 1, 1.6)
                    boru((x, yb, 0.12), (x, yb, 0.92), 0.035, baba)
        boru((x, y0, 1.0), (x, y1, 1.0), 0.07, kus)
        boru((x, y0, 0.1), (x, y1, 0.1), 0.05, kus)


def kapi(R):
    """cift cerceve: icte kalin neon cerceve (kart acikligi), dista ustu iki sira kare izgarali neon kafes"""
    Y, W_, H_, K, KF = KAP["y"], KAP["w"], KAP["h"], KAP["kalin"], KAP["kafes"]
    neon = mat_dikey("cerceve", R["koyu"], R["ana"], 0.0, H_ + 1.6, 1.5)   # 1. deneme: acik ton 2,4 beyaza patladi
    ince = mat_emis("kafes", lin(hex3(R["ana"])), 2.8)
    xk = W_ / 2 + K / 2
    for s in (-1, 1):                                      # ic cerceve: iki kalin direk + ust kiris
        yuvarlak_kutu("direk", (s * xk, Y, (H_ + K) / 2), (K, K, H_ + K), neon, egim=0.05, seg=2)
    yuvarlak_kutu("kiris", (0, Y, H_ + K / 2), (W_ + 2 * K, K, K), neon, egim=0.05, seg=2)
    # dis kafes: iki yanda dikey kafes kolon + ustte iki sira kare izgara
    xd = xk + K / 2 + KF / 2
    zt = H_ + K + KF * 2
    for s in (-1, 1):
        x0 = s * xd
        for dx in (-KF / 2, KF / 2):
            boru((x0 + dx, Y - 0.05, 0.0), (x0 + dx, Y - 0.05, zt), 0.05, ince)
        z = KF * 0.5
        while z < zt:
            boru((x0 - KF / 2, Y - 0.05, z), (x0 + KF / 2, Y - 0.05, z), 0.035, ince); z += KF
    xa, xb = -xd - KF / 2, xd + KF / 2
    for z in (H_ + K, H_ + K + KF, zt):
        boru((xa, Y - 0.05, z), (xb, Y - 0.05, z), 0.05, ince)
    n = max(4, round((xb - xa) / KF))
    for i in range(n + 1):
        x = xa + i * (xb - xa) / n
        boru((x, Y - 0.05, H_ + K), (x, Y - 0.05, zt), 0.035, ince)


def serit_katmani(oyuncu):
    R = SERIT[oyuncu]
    sc = bos_sahne(w=960, h=1080, saydam=True, ornek=min(ORNEK, 24))
    sc.cycles.transparent_max_bounces = 24
    kam = kamera(sc)
    zemin(R); korkuluk(R); kapi(R)
    for y, gen, kol in ((1.0, 1.9, 0.9), (2.9, 1.75, 0.82), (4.7, 1.6, 0.75), (6.3, 1.45, 0.68)):
        chevron(R, y, gen, kol)
    Y, W_, H_ = KAP["y"], KAP["w"], KAP["h"]
    ic = W_ / 2
    bpy.context.view_layer.update()
    px = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-ic, Y, 0), (ic, Y, 0), (-ic, Y, H_), (ic, Y, H_))]
    xs = [p.x * 960 for p in px]; ys = [(1 - p.y) * 1080 for p in px]
    YERLESIM["aciklik_" + oyuncu] = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
    YERLESIM["yol"] = {"y_kapi": Y, "genislik": YOL_YARI * 2, "kam": KAM, "serit_w": 960}
    log("aciklik", oyuncu, YERLESIM["aciklik_" + oyuncu])
    if KAPAK:
        sc.view_settings.exposure = POZLAMA
    parlat(sc, esik=1.4, boy=7, mix=0.12)
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
log("bitti (kozmikpist)", YERLESIM.get("aciklik_p1"), YERLESIM.get("aciklik_p2"))
