"""HUMAN TETRIS 13. video (REF-064 HumanWarmUp, CO-OP) - NEON ISIK TUNELI sahne varliklari, TEK serit. varlik.py calistirir (--mod isiktuneli).

REF-064'te ne varsa (md. 22): iç ice dikdortgen neon cerceveler, yanlarda sari-pembe-yesil isik sutunlari, sicak metalik tunel duvarlari;
koyu asfalt yol, camgobegi chevron + kenar cizgisi, bronz kaldirim, camgobegi tirabzan + iki beyaz neon cubuklu korkuluk, beyaz kafes kapi.
P1/P2 ikonlari, "Coming Soon", "!", duvarlar ve tunelin renk degisimi motorda (sahne10.html).
"""

import random
YERLESIM.clear()
KAP = {"y": 8.6, "w": 7.4, "h": 3.6, "kule": 0.42, "kiris": 0.42}
KAM = {"z": 1.5, "egim": 0.0, "lens": 18.0, "sensor": 24.0}
YOL_W = 7.6
Y_SON = 9.4
T_W, T_H = 15.0, 11.0        # tunel ic olcusu
T_Y1 = 120.0
CAMGOBEGI = "#62f5e4"
RENKLER = ("#ffe21a", "#ff2f9a", "#3dff6a", "#ff7a1a", "#ffffff", "#c04dff")
KAPAK = YALNIZ == "kapak"
POZLAMA = float(arg("--kapak-pozlama", "0"))
RND = random.Random(64)


def kamera(sc):
    rx = math.radians(90 - KAM["egim"])
    bpy.ops.object.camera_add(location=(0, 0, KAM["z"]), rotation=(rx, 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.sensor_fit = "VERTICAL"; kam.data.sensor_height = KAM["sensor"]; kam.data.lens = KAM["lens"]
    kam.data.clip_end = 900
    return kam


def mat_metal(ad, renk, purluk, metal=0.95):
    m = bpy.data.materials.new(ad); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*renk, 1); b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = purluk
    return m


def sekil(ad, noktalar, mat, konum=(0, 0, 0)):
    me = bpy.data.meshes.new(ad)
    me.from_pydata([(a, b, 0) for a, b in noktalar], [], [list(range(len(noktalar)))]); me.update()
    o = bpy.data.objects.new(ad, me); bpy.context.collection.objects.link(o)
    o.location = konum; o.data.materials.append(mat)
    return o


# ------------------------------------------------------------------ GOK katmani = tunelin kendisi
def tunel_duvar():
    """yan duvar, tavan ve taban: sicak koyu metal, neonlari yansitir"""
    m = mat_metal("t_duvar", lin(hex3("#3a2410")), 0.28, metal=0.9)
    y0, y1 = -2.0, T_Y1
    for ad, p in (("sol", (-T_W, 0, -3)), ("sag", (T_W, 0, -3))):
        yuvarlak_kutu("t_" + ad, (p[0] + (-0.5 if p[0] < 0 else 0.5), (y0 + y1) / 2, T_H / 2), (1.0, y1 - y0, T_H + 8), m, egim=0.0, seg=1)
    yuvarlak_kutu("t_tavan", (0, (y0 + y1) / 2, T_H + 0.5), (2 * T_W + 2, y1 - y0, 1.0), m, egim=0.0, seg=1)
    yuvarlak_kutu("t_taban", (0, (y0 + y1) / 2, -3.5), (2 * T_W + 2, y1 - y0, 1.0), m, egim=0.0, seg=1)


def isik_sutunu(x, y, z0, z1, gen, rnd):
    """REF-064: boydan boya renk bantli parlak sutun (sari agirlikli, araya pembe/yesil/beyaz)"""
    z = z0
    while z < z1:
        boy = rnd.uniform(0.5, 1.8)
        r = rnd.choices(RENKLER, weights=(5, 2, 2, 2, 1.5, 1))[0]
        yuvarlak_kutu("sutun", (x, y, z + boy / 2), (gen, gen, boy), mat_emis("s" + r, lin(hex3(r)), rnd.uniform(5, 11)), egim=0.0, seg=1)
        z += boy


def cerceveler(rnd):
    """ic ice dikdortgen neon cerceveler + yanlarda isik sutunlari; uzaga dogru ufalir"""
    y, j = 11.0, 0
    while y < T_Y1 - 6:
        hw = 6.2 + 0.5 * (j % 2); hz = 7.2
        r = mat_emis("c%d" % (j % 4), lin(hex3(("#ffe21a", "#ff2f9a", "#3dff6a", "#ffffff")[j % 4])), 12)
        boru((-hw, y, hz), (hw, y, hz), 0.14, r)
        for s in (-1, 1):
            boru((s * hw, y, -1), (s * hw, y, hz), 0.14, r)
        y += 9.0; j += 1
    for s in (-1, 1):
        for x_, y_ in ((5.6, 7), (7.0, 5.4), (8.8, 4.2), (11.2, 3.2), (14.0, 2.5)):
            isik_sutunu(s * x_, y_ + 12, -1.5, 11.5, 0.4, rnd)
    for s in (-1, 1):                                      # REF-064: tavanda sari kirik neon cizgiler
        for i in range(5):
            a = (s * rnd.uniform(3, 11), rnd.uniform(16, 40), rnd.uniform(7, 10))
            b = (a[0] + s * rnd.uniform(1.5, 4), a[1], a[2] + rnd.uniform(-1.5, 1.5))
            boru(a, b, 0.07, mat_emis("kir", lin(hex3("#ffd21a" if i % 3 else "#ff3a2a")), 10))


def gok_katmani():
    rnd = random.Random(64)
    sc = bos_sahne(w=1920, h=1080, ornek=min(ORNEK, 48))
    if KAPAK:
        sc.view_settings.exposure = POZLAMA
    kamera(sc)
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (*lin(hex3("#2a1408")), 1)
    sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.6
    tunel_duvar(); cerceveler(rnd)
    for yy in (14, 28, 48):
        isik("AREA", (0, yy, 8), 1800, lin(hex3("#ffd080")), 8, yon=(0, yy, 0))
    sc.use_nodes = True
    nt2 = sc.node_tree; nt2.nodes.clear()
    rl = nt2.nodes.new("CompositorNodeRLayers")
    gl = nt2.nodes.new("CompositorNodeGlare"); gl.glare_type = "FOG_GLOW"; gl.threshold = 0.9; gl.size = 8; gl.mix = 0.1
    ou = nt2.nodes.new("CompositorNodeComposite")
    nt2.links.new(rl.outputs[0], gl.inputs[0]); nt2.links.new(gl.outputs[0], ou.inputs[0])
    yaz(sc, ON_EK + "gok.png")


# ------------------------------------------------------------------ SERIT katmani
def kopru_yol():
    yol = bpy.data.materials.new("yol"); yol.use_nodes = True
    nt = yol.node_tree; b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = 0.42; b.inputs["Metallic"].default_value = 0.0
    no = nt.nodes.new("ShaderNodeTexNoise"); no.inputs["Scale"].default_value = 90; no.inputs["Detail"].default_value = 8
    rm = nt.nodes.new("ShaderNodeValToRGB")                # asfalt: koyu gri + kahve benek
    rm.color_ramp.elements[0].position = 0.4; rm.color_ramp.elements[0].color = (*lin(hex3("#14110f")), 1)
    rm.color_ramp.elements[1].position = 0.68; rm.color_ramp.elements[1].color = (*lin(hex3("#4e3a2b")), 1)
    nt.links.new(no.outputs["Fac"], rm.inputs[0]); nt.links.new(rm.outputs[0], b.inputs["Base Color"])
    yuvarlak_kutu("yol", (0, (0.3 + Y_SON) / 2, -0.2), (YOL_W, Y_SON - 0.3, 0.4), yol, egim=0.03, seg=2)
    cam = mat_emis("chev", lin(hex3(CAMGOBEGI)), 1.9)
    for yy, hw, kal in ((0.9, 2.0, 0.62), (2.3, 1.78, 0.5), (3.55, 1.58, 0.42), (4.65, 1.42, 0.35), (5.65, 1.28, 0.28), (6.55, 1.16, 0.24), (7.35, 1.06, 0.2)):
        d = hw * 0.2                                       # REF-064: genis, basik V
        sekil("chev", [(-hw, yy + d), (0, yy), (hw, yy + d), (hw, yy + d + kal), (0, yy + kal), (-hw, yy + d + kal)], cam, konum=(0, 0, 0.03))
    kaldirim = mat_metal("kaldirim", lin(hex3("#6a4426")), 0.4, metal=0.3)
    for s in (-1, 1):
        boru((s * (YOL_W / 2 - 0.06), 0.3, 0.03), (s * (YOL_W / 2 - 0.06), Y_SON, 0.03), 0.045, mat_emis("kenar%d" % s, lin(hex3(CAMGOBEGI)), 2.6))
        yuvarlak_kutu("kaldirim", (s * (YOL_W / 2 + 0.28), (0.3 + Y_SON) / 2, 0.05), (0.5, Y_SON - 0.3, 0.14), kaldirim, egim=0.01, seg=1)


def korkuluk():
    metal = mat_metal("kork_metal", lin(hex3("#7a5a48")), 0.3, metal=0.7)
    tir = mat_emis("kork_tir", lin(hex3("#58d8d8")), 1.5)
    bey = mat_emis("kork_bey", lin(hex3("#fff0dc")), 3.2)
    for s in (-1, 1):
        x = s * (YOL_W / 2 + 0.34)
        hk = 1.0
        ys = [0.5 + i * 1.5 for i in range(int((KAP["y"] - 0.5) / 1.5) + 1)] + [KAP["y"]]
        for yy in ys:
            yuvarlak_kutu("dikme", (x, yy, hk / 2), (0.07, 0.07, hk), metal, egim=0.02, seg=2)
        yuvarlak_kutu("tirabzan", (x, (ys[0] + ys[-1]) / 2, hk), (0.11, ys[-1] - ys[0], 0.06), tir, egim=0.02, seg=2)
        for zz in (hk * 0.42, hk * 0.68):
            boru((x, ys[0], zz), (x, ys[-1], zz), 0.024, bey)


def kapi():
    Y, W_, H_, KK, KR = KAP["y"], KAP["w"], KAP["h"], KAP["kule"], KAP["kiris"]
    ana = mat_emis("kapi_ana", lin(hex3("#ffffff")), 1.4)
    ince = mat_emis("kapi_ince", lin(hex3("#f4f4f8")), 1.1)
    xk = W_ / 2 - KK / 2
    for s in (-1, 1):
        kafes_kule(s * xk, Y, 0.0, H_ + KR, KK, ana, ince)
    kafes_kiris(-xk, xk, Y, H_ + KR / 2, KR, ana, ince)


def serit_katmani():
    sc = bos_sahne(w=1920, h=1080, saydam=True, ornek=min(ORNEK, 64))
    if KAPAK:
        sc.view_settings.exposure = POZLAMA
    kam = kamera(sc)
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (*lin(hex3("#ffd8a8")), 1)
    sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.22
    Y = KAP["y"]
    kopru_yol(); korkuluk(); kapi()
    isik("AREA", (0, 4, 6), 160, lin(hex3("#ffb070")), 8, yon=(0, 5, 0))
    isik("AREA", (0, Y - 2, 5), 240, lin(hex3("#ffe0c0")), 5, yon=(0, Y, 0))
    W_, H_, KK = KAP["w"], KAP["h"], KAP["kule"]
    ic = W_ / 2 - KK
    bpy.context.view_layer.update()
    px = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-ic, Y, 0), (ic, Y, 0), (-ic, Y, H_), (ic, Y, H_))]
    xs = [p.x * 1920 for p in px]; ys = [(1 - p.y) * 1080 for p in px]
    YERLESIM[ON_EK + "aciklik_p1"] = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
    YERLESIM["yol"] = {"y_kapi": Y, "genislik": YOL_W, "kam": KAM, "serit_w": 1920}
    log("aciklik", YERLESIM[ON_EK + "aciklik_p1"])
    yaz(sc, ON_EK + "serit.png")


ON_EK = ""
if YALNIZ == "kapak":
    ON_EK = "kapak-"
    gok_katmani(); serit_katmani()
if YALNIZ in ("hepsi", "sahne"):
    gok_katmani(); serit_katmani()
json.dump(YERLESIM, open(os.path.join(CIKTI, "yerlesim.json"), "w"), indent=1)
log("bitti (isiktuneli)", YERLESIM.get("aciklik_p1"))
