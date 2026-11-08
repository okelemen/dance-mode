"""HUMAN TETRIS 22. video (REF-077 TetrisBounce, 1v1) - NEON LUNAPARK PISTI sahne varliklari. varlik.py calistirir (--mod lunapark).

REF-077'de ne varsa (md. 22): koyu lacivert-mor yildizli gece gogu, pembe/mor kabarik bulutlar, sabun kabarciklari, sagda dev neon donme dolap
(pembe + sari cember, ortada kalp), solda mavi (P1), sagda pembe (P2) neon pist; kurdele fiyonklu korkuluk, kapi = neon truss kafes + ust
koselerde fiyonk; yolda neon basamak. Alinmaz (telif): anime kiz maskot. Kart, 3-2-1, HUD, maskot motorda / kapak betiginde.
Taban: varlik-lunapark.py (iki seritli yapi, ayni cikti dosyalari).

Ciktilar: gok.png, serit-p1/p2.png, panel-p1/p2.png, yerlesim.json; kapak modu (--yalniz kapak): kapak-gok.png, kapak-serit-p1/p2.png
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
    "p1": {"ana": "#1ab4ff", "acik": "#b0eaff", "koyu": "#0a50e0", "zemin": "#1a7cff", "zemin_u": "#0e1e6a"},
    "p2": {"ana": "#ff4fc8", "acik": "#ffc4f2", "koyu": "#b0108c", "zemin": "#f01ab4", "zemin_u": "#4a1060"},
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
    cr.elements[0].position = 0.0; cr.elements[0].color = (*lin(hex3("#4a2090")), 1)
    cr.elements[1].position = 1.0; cr.elements[1].color = (*lin(hex3("#0a0a40")), 1)
    e = cr.elements.new(0.45); e.color = (*lin(hex3("#2a1a7a")), 1)
    ns = nt.nodes.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value = 3.2; ns.inputs["Detail"].default_value = 8; ns.inputs["Roughness"].default_value = 0.62
    nt.links.new(tc.outputs["Generated"], ns.inputs["Vector"])
    nr = nt.nodes.new("ShaderNodeValToRGB"); c2 = nr.color_ramp; nt.links.new(ns.outputs["Fac"], nr.inputs[0])
    c2.elements[0].position = 0.38; c2.elements[0].color = (0, 0, 0, 1)
    c2.elements[1].position = 0.78; c2.elements[1].color = (*lin(hex3("#ff5ad8")), 1)
    e = c2.elements.new(0.55); e.color = (*lin(hex3("#3a6aff")), 1)
    e = c2.elements.new(0.66); e.color = (*lin(hex3("#9a4aff")), 1)
    ad = nt.nodes.new("ShaderNodeMix"); ad.data_type = "RGBA"; ad.blend_type = "ADD"; ad.inputs[0].default_value = 0.6
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
    cr.elements[1].position = 1.0; cr.elements[1].color = (*lin(hex3("#c8d8ff")), 1)   # kapak 1: beyaz mermer gibi -> mavi agirlikli
    for pos, c in ((0.35, "#2a6aff"), (0.55, "#ff3ab8"), (0.7, "#6a4aff"), (0.88, "#ff8ae0")):
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


def balon(konum, r, renk):
    return kure(konum, r, mat_kristal("balon", renk, 1.7, 0.1), sub=2)


def dolap(cx, cz, R, y):
    """REF-077 dev neon donme dolap: pembe + sari cember, 16 kol, kabinler, ortada kalp"""
    mr = mat_emis("dolap_p", lin(hex3("#ff4fc8")), 3.4); my = mat_emis("dolap_s", lin(hex3("#ffd23a")), 3.6)
    mc = mat_emis("dolap_c", lin(hex3("#5ad8ff")), 3.2); mb = mat_emis("dolap_b", lin(hex3("#ffffff")), 3.0)
    for rr, m_, kal in ((R, mr, 7.0), (R * 0.62, my, 5.0), (R * 0.28, mr, 4.0)):
        bpy.ops.mesh.primitive_torus_add(major_radius=rr, minor_radius=kal, location=(cx, y, cz), rotation=(math.pi / 2, 0, 0))
        bpy.context.active_object.data.materials.append(m_)
    cab = (mr, mc, my)
    for i in range(16):
        a = 2 * math.pi * i / 16
        boru((cx, y, cz), (cx + R * math.cos(a), y, cz + R * math.sin(a)), 2.8, (my, mr)[i % 2])
        kure((cx + R * math.cos(a), y - 4, cz + R * math.sin(a)), 17, cab[i % 3], sub=2)
        kure((cx + R * 0.62 * math.cos(a), y, cz + R * 0.62 * math.sin(a)), 7, mb, sub=1)
    kure((cx, y - 6, cz), 52, mr, sub=3); kure((cx, y - 10, cz), 34, my, sub=3)
    for s_ in (-1, 1):
        boru((cx, y, cz), (cx + s_ * R * 0.55, y, cz - R * 1.25), 6.0, mc)


def gok_katmani(ad):
    sc = bos_sahne(w=1920, h=1080, ornek=min(ORNEK, 16))
    bpy.ops.object.camera_add(location=(0, -900, 540), rotation=(math.radians(90), 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.type = "ORTHO"; kam.data.ortho_scale = 1920; kam.data.clip_end = 3000
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 600, 540), rotation=(math.radians(90), 0, 0))
    p = bpy.context.active_object; p.scale = (2000, 1100, 1); bpy.ops.object.transform_apply(scale=True)
    p.data.materials.append(mat_bulutsu())
    rnd = random.Random(77)
    beyaz = mat_emis("yildiz", lin(hex3("#ffffff")), 3.2)
    sari_y = mat_emis("yildiz_s", lin(hex3("#ffe27a")), 3.4)
    mavi_y = mat_emis("yildiz_m", lin(hex3("#9ad8ff")), 3.0)
    for _ in range(300):                                   # yildiz tozu: gok bos kalmaz (md. 7)
        kure((rnd.uniform(-960, 960), 450, rnd.uniform(0, 1080)), rnd.choice((1.2, 1.8, 2.6, 3.6)), rnd.choice((beyaz, beyaz, sari_y, mavi_y)), sub=1)
    # pembe-mor kabarik bulutlar (REF-077: solda ve altta)
    bulut_m = [mat_emis("bulut%d" % i, lin(hex3(c)), g) for i, (c, g) in enumerate((("#ff7ae0", 1.0), ("#c070ff", 0.9), ("#ff9ae8", 1.1)))]
    for (cx, cz, n, rr) in ((-760, 560, 9, 120), (-300, 470, 7, 100), (160, 430, 6, 90), (860, 470, 8, 110), (-880, 900, 6, 90), (-220, 960, 5, 80)):
        for _ in range(n):
            k = kure((cx + rnd.uniform(-rr * 1.3, rr * 1.3), 300 + rnd.uniform(-30, 30), cz + rnd.uniform(-rr * 0.5, rr * 0.5)),
                     rnd.uniform(rr * 0.45, rr * 0.9), rnd.choice(bulut_m), sub=3)
            k.scale = (1.2, 0.5, 0.8)
    # dev donme dolap (sag)
    dolap(640, 640, 330, 200)
    # sabun kabarciklari: solda ve ortada, her boyda
    renkler = ("#b8e8ff", "#ffb8f0", "#c8b8ff", "#ffffff")
    for _ in range(34):
        balon((rnd.uniform(-900, 260), 150, rnd.uniform(380, 1040)), rnd.choice((10, 16, 22, 30, 42)), rnd.choice(renkler))
    # ufukta parlak pembe / mavi isilti (korkuluklarin arkasi)
    for sx in (-1, 1):
        k = kure((sx * 780, 220, 360), 220, mat_emis("ufuk%d" % sx, lin(hex3("#ff6ad8" if sx > 0 else "#7ab8ff")), 0.9), sub=3); k.scale = (1.4, 0.2, 0.45)
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


def yay(x, y, z, boy, mat, mat_dugum):
    """kurdele fiyonk: iki yassi kulak + dugum + iki kuyruk (REF-077 korkuluk / kapi fiyonklari)"""
    for s_ in (-1, 1):
        k = kure((x, y + s_ * boy * 0.55, z), boy * 0.5, mat, sub=2); k.scale = (0.35, 1.0, 0.8)
        boru((x, y, z), (x, y + s_ * boy * 0.45, z - boy * 0.95), boy * 0.07, mat)
    kure((x, y, z), boy * 0.26, mat_dugum, sub=2)


def korkuluk(R):
    """fiyonklu neon korkuluk: kalin dikmeler + ust ve alt kordon, her aralikta kurdele fiyonk"""
    dikme = mat_kristal("dikme", R["ana"], 0.9, 0.4)
    yay_m = mat_kristal("yay", R["ana"], 1.5, 0.15)
    dug_m = mat_emis("dugum", lin(hex3(R["acik"])), 2.4)
    kus = mat_emis("kus", lin(hex3(R["acik"])), 1.8)
    for s in (-1, 1):
        x = s * YOL_YARI
        y0, y1 = -0.6, KAP["y"] + 4.0
        n = 7
        for j in range(n + 1):
            yy = y0 + j * (y1 - y0) / n
            yuvarlak_kutu("dikme", (x, yy, 0.55), (0.2, 0.2, 1.1), dikme, egim=0.05, seg=2)
            kure((x, yy, 1.16), 0.14, dug_m, sub=2)
            if j < n:
                L = (y1 - y0) / n
                yay(x, yy + L / 2, 0.62, 0.55, yay_m, dug_m)
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
    for s in (-1, 1):                                      # truss capraz cubuklari + ust kose fiyonklari (REF-077)
        z = KF * 0.5
        while z < zt - KF * 0.4:
            boru((s * xd - KF / 2, Y - 0.05, z), (s * xd + KF / 2, Y - 0.05, z + KF), 0.03, ince); z += KF
        yay(s * (xd + KF * 0.5), Y - 0.3, zt + 0.1, 1.0, mat_kristal("yay_k", R["ana"], 1.6, 0.12), mat_emis("dugum_k", lin(hex3(R["acik"])), 2.6))


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
log("bitti (lunapark)", YERLESIM.get("aciklik_p1"), YERLESIM.get("aciklik_p2"))
