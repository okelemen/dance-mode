"""HUMAN TETRIS 15. video (REF-066 HumanWarmUp, CO-OP) - MAVI IZGARA TUNEL + BUZ KOPRU sahne varliklari, TEK serit. varlik.py calistirir (--mod kartunel).

REF-066'da ne varsa (md. 22): lacivert tunel, camgobegi neon izgara, ucta parlayan camgobegi derinlik; buz mavisi parlak kopru, beyaz kalin chevron,
beyaz dikmeli uc cubuklu korkuluk, beyaz kafes kapi. Hiz cizgileri, kar taneleri, P1/P2 ikonlari, "Coming Soon", "!" ve duvarlar motorda.
"""

YERLESIM.clear()
KAP = {"y": 8.6, "w": 7.2, "h": 3.6, "kule": 0.3, "kiris": 0.3}
KAM = {"z": 1.5, "egim": 0.0, "lens": 18.0, "sensor": 24.0}
YOL_W = 7.6
Y_SON = 9.4
T_W, T_H, T_Z0 = 15.0, 11.0, -3.0
T_Y1 = 120.0
IZGARA = "#2fd8e8"
KAPAK = YALNIZ == "kapak"
POZLAMA = float(arg("--kapak-pozlama", "0"))


def kamera(sc):
    rx = math.radians(90 - KAM["egim"])
    bpy.ops.object.camera_add(location=(0, 0, KAM["z"]), rotation=(rx, 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.sensor_fit = "VERTICAL"; kam.data.sensor_height = KAM["sensor"]; kam.data.lens = KAM["lens"]
    kam.data.clip_end = 900
    return kam


def mat_buz():
    m = bpy.data.materials.new("buz"); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*lin(hex3("#4a6ea8")), 1); b.inputs["Roughness"].default_value = 0.22
    b.inputs["Metallic"].default_value = 0.15
    b.inputs["Emission Color"].default_value = (*lin(hex3("#4a78b8")), 1); b.inputs["Emission Strength"].default_value = 0.22   # sahne 1: guverte chevronlari yutuyordu
    return m


def sekil(ad, noktalar, mat, konum=(0, 0, 0)):
    me = bpy.data.meshes.new(ad)
    me.from_pydata([(a, b, 0) for a, b in noktalar], [], [list(range(len(noktalar)))]); me.update()
    o = bpy.data.objects.new(ad, me); bpy.context.collection.objects.link(o)
    o.location = konum; o.data.materials.append(mat)
    return o


# ------------------------------------------------------------------ GOK katmani = izgara tunel
def tunel():
    koyu = mat_emis("t_koyu", lin(hex3("#0a2450")), 0.75)
    y0, y1 = -2.0, T_Y1
    for s in (-1, 1):
        yuvarlak_kutu("t_yan", (s * (T_W + 0.5), (y0 + y1) / 2, T_H / 2), (1.0, y1 - y0, T_H + 8), koyu, egim=0.0, seg=1)
    yuvarlak_kutu("t_tavan", (0, (y0 + y1) / 2, T_H + 0.5), (2 * T_W + 2, y1 - y0, 1.0), koyu, egim=0.0, seg=1)
    yuvarlak_kutu("t_taban", (0, (y0 + y1) / 2, T_Z0 - 0.5), (2 * T_W + 2, y1 - y0, 1.0), koyu, egim=0.0, seg=1)
    yuvarlak_kutu("t_son", (0, y1, T_H / 2), (2 * T_W + 2, 1.0, T_H + 8), mat_emis("t_son", lin(hex3("#1f9fb8")), 1.3), egim=0.0, seg=1)
    izg = mat_emis("izgara", lin(hex3(IZGARA)), 1.1)   # sahne 1: izgara REF-066 gore fazla parlak ve kalindi
    y = 6.0
    while y < T_Y1:                                        # enine halkalar
        for a, b in (((-T_W, y, T_Z0), (-T_W, y, T_H)), ((-T_W, y, T_H), (T_W, y, T_H)), ((T_W, y, T_H), (T_W, y, T_Z0))):
            boru(a, b, 0.035, izg)
        y += 4.0
    for z in (-1.0, 1.0, 3.0, 5.0, 7.0, 9.0):              # boyuna cizgiler, yan duvarlar
        for s in (-1, 1):
            boru((s * (T_W - 0.02), 2, z), (s * (T_W - 0.02), T_Y1, z), 0.035, izg)
    for x in range(-14, 15, 4):                            # boyuna cizgiler, tavan
        boru((x, 2, T_H - 0.02), (x, T_Y1, T_H - 0.02), 0.035, izg)


def gok_katmani():
    sc = bos_sahne(w=1920, h=1080, ornek=min(ORNEK, 48))
    if KAPAK:
        sc.view_settings.exposure = POZLAMA
    kamera(sc)
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (*lin(hex3("#061030")), 1)
    sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.5
    tunel()
    sc.use_nodes = True
    nt2 = sc.node_tree; nt2.nodes.clear()
    rl = nt2.nodes.new("CompositorNodeRLayers")
    gl = nt2.nodes.new("CompositorNodeGlare"); gl.glare_type = "FOG_GLOW"; gl.threshold = 0.8; gl.size = 8; gl.mix = 0.25
    ou = nt2.nodes.new("CompositorNodeComposite")
    nt2.links.new(rl.outputs[0], gl.inputs[0]); nt2.links.new(gl.outputs[0], ou.inputs[0])
    yaz(sc, ON_EK + "gok.png")


# ------------------------------------------------------------------ SERIT katmani
def kopru_yol():
    yuvarlak_kutu("yol", (0, (0.3 + Y_SON) / 2, -0.2), (YOL_W + 1.4, Y_SON - 0.3, 0.4), mat_buz(), egim=0.03, seg=2)
    bey = mat_emis("chev", lin(hex3("#d8f6ff")), 1.25)
    for yy, hw, kal in ((0.9, 2.5, 1.05), (2.45, 2.22, 0.85), (3.85, 1.98, 0.71), (5.05, 1.78, 0.6), (6.1, 1.6, 0.48), (7.05, 1.45, 0.4), (7.85, 1.33, 0.34)):
        d = hw * 0.28                                      # REF-066: genis, kalin beyaz V
        sekil("chev", [(-hw, yy + d), (0, yy), (hw, yy + d), (hw, yy + d + kal), (0, yy + kal), (-hw, yy + d + kal)], bey, konum=(0, 0, 0.03))


def korkuluk():
    bey = mat_emis("kork_bey", lin(hex3("#eaf4ff")), 1.3)
    for s in (-1, 1):
        x = s * (YOL_W / 2 + 0.55)
        hk = 1.05
        ys = [0.5 + i * 1.5 for i in range(int((KAP["y"] - 0.5) / 1.5) + 1)] + [KAP["y"]]
        for yy in ys:
            yuvarlak_kutu("dikme", (x, yy, hk / 2), (0.17, 0.17, hk + 0.1), bey, egim=0.02, seg=2)
        for zz in (hk * 0.36, hk * 0.66, hk):
            yuvarlak_kutu("cubuk", (x, (ys[0] + ys[-1]) / 2, zz), (0.07, ys[-1] - ys[0], 0.07), bey, egim=0.01, seg=1)


def kapi():
    Y, W_, H_, KK, KR = KAP["y"], KAP["w"], KAP["h"], KAP["kule"], KAP["kiris"]
    ana = mat_emis("kapi_ana", lin(hex3("#f4f8ff")), 0.95)
    ince = mat_emis("kapi_ince", lin(hex3("#dce8f6")), 0.8)
    xk = W_ / 2 - KK / 2
    for s in (-1, 1):
        kafes_kule(s * xk, Y, 0.0, H_ + KR, KK, ana, ince)
    kafes_kiris(-xk, xk, Y, H_ + KR / 2, KR, ana, ince)


def serit_katmani():
    sc = bos_sahne(w=1920, h=1080, saydam=True, ornek=min(ORNEK, 64))
    if KAPAK:
        sc.view_settings.exposure = POZLAMA
    kam = kamera(sc)
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (*lin(hex3("#bcd8ff")), 1)
    sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.25
    Y = KAP["y"]
    kopru_yol(); korkuluk(); kapi()
    isik("AREA", (0, 4, 6), 180, lin(hex3("#cfe4ff")), 8, yon=(0, 5, 0))
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
log("bitti (kartunel)", YERLESIM.get("aciklik_p1"))
