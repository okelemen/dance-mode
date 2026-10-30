"""HUMAN TETRIS 12. video (REF-063 HumanWarmUp, 1 oyuncu) - NEON KOPRU sahne varliklari, TEK serit. varlik.py calistirir (--mod neonkopru).

REF-063'te ne varsa (md. 22): kapkara gece, koyu mor yol, parlak pembe chevron basamaklar, cift neon pembe korkuluk, altinda mor LED serit,
korkulukta pembe cift oklar, gri metal kafes kapi. Lazer yildizlar, isik toplari, "Coming Soon", "!" ve duvarlar motorda (sahne9.html).
"""

YERLESIM.clear()
KAP = {"y": 8.6, "w": 7.4, "h": 3.6, "kule": 0.42, "kiris": 0.42}
KAM = {"z": 1.06, "egim": -3.0, "lens": 18.0, "sensor": 24.0}
YOL_W = 7.6
Y_SON = 9.4
PEMBE, MOR = "#ff3fb0", "#8a3cff"
KAPAK = YALNIZ == "kapak"
POZLAMA = float(arg("--kapak-pozlama", "0"))


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


def kapak_lazer():
    """KAPAK: REF-063 kapaginda gokte pembe lazer cizgileri (videoda motor ciziyor; kapakta 2B boyama yok -> Blender'da)"""
    m = mat_emis("lazer", lin(hex3("#ff3fb0")), 9.0)
    for a, b in (((-260, 300, 40), (-40, 300, 215)), ((-40, 300, 215), (70, 300, 80)), ((70, 300, 80), (280, 300, 190)), ((-180, 300, 150), (120, 300, 230))):
        boru(a, b, 0.9, m)


def gok_katmani():
    sc = bos_sahne(w=1920, h=1080, ornek=min(ORNEK, 16))
    if KAPAK:
        sc.view_settings.exposure = POZLAMA
    kamera(sc)
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (*lin(hex3("#0b0212")), 1)
    sc.world.node_tree.nodes["Background"].inputs[1].default_value = 1.0
    if KAPAK:
        kapak_lazer()
    yaz(sc, ON_EK + "gok.png")


def kopru_yol():
    yol = mat_metal("yol", lin(hex3("#1a0a24")), 0.3, metal=0.1)
    yuvarlak_kutu("yol", (0, (0.3 + Y_SON) / 2, -0.2), (YOL_W, Y_SON - 0.3, 0.4), yol, egim=0.05, seg=2)
    pembe = mat_emis("chev", lin(hex3("#ff6ac4")), 5.0)
    for yy, hw, kal in ((0.9, 1.75, 0.6), (2.3, 1.55, 0.48), (3.55, 1.38, 0.4), (4.65, 1.24, 0.33), (5.65, 1.12, 0.28), (6.55, 1.02, 0.24), (7.35, 0.94, 0.2)):
        d = hw * 0.42
        sekil("chev", [(-hw, yy + d), (0, yy), (hw, yy + d), (hw, yy + d + kal), (0, yy + kal), (-hw, yy + d + kal)], pembe, konum=(0, 0, 0.03))
    for s in (-1, 1):
        boru((s * (YOL_W / 2 - 0.06), 0.3, 0.03), (s * (YOL_W / 2 - 0.06), Y_SON, 0.03), 0.06, mat_emis("kenar%d" % s, lin(hex3(PEMBE)), 8))


def korkuluk():
    metal = mat_metal("kork_metal", lin(hex3("#3a1a4a")), 0.3, metal=0.5)
    okm = mat_emis("ok", lin(hex3("#ff7ad0")), 6)
    pem = mat_emis("kork_neon", lin(hex3(PEMBE)), 7)
    mor = mat_emis("kork_led", lin(hex3(MOR)), 8)
    for s in (-1, 1):
        x = s * (YOL_W / 2 + 0.25)
        hk = 0.95
        ys = [0.5 + i * 1.7 for i in range(int((KAP["y"] - 0.5) / 1.7) + 1)] + [KAP["y"]]
        for yy in ys:
            yuvarlak_kutu("dikme", (x, yy, hk / 2), (0.08, 0.08, hk), metal, egim=0.02, seg=2)
        boru((x, ys[0], hk), (x, ys[-1], hk), 0.035, pem)
        boru((x, ys[0], hk * 0.62), (x, ys[-1], hk * 0.62), 0.025, pem)
        for j in range(int((ys[-1] - ys[0]) / 0.5)):       # REF-063: altta kesikli mor LED serit
            y0 = ys[0] + j * 0.5
            boru((x, y0, 0.06), (x, y0 + 0.28, 0.06), 0.03, mor)
        for y0 in (0.9, 3.4, 6.0):
            for j in range(2):
                yy = y0 + j * 0.5
                pts = [(yy + 0.38, 0.14), (yy, 0.36), (yy + 0.38, 0.58), (yy + 0.6, 0.58), (yy + 0.22, 0.36), (yy + 0.6, 0.14)]
                me = bpy.data.meshes.new("ok"); me.from_pydata([(x - s * 0.04, a, b) for a, b in pts], [], [list(range(6))]); me.update()
                ob = bpy.data.objects.new("ok", me); bpy.context.collection.objects.link(ob); ob.data.materials.append(okm)


def kapi():
    Y, W_, H_, KK, KR = KAP["y"], KAP["w"], KAP["h"], KAP["kule"], KAP["kiris"]
    ana = mat_metal("kapi_ana", lin(hex3("#8e8e98")), 0.35, metal=0.6)
    ince = mat_metal("kapi_ince", lin(hex3("#6e6e78")), 0.4, metal=0.6)
    xk = W_ / 2 - KK / 2
    for s in (-1, 1):
        kafes_kule(s * xk, Y, 0.0, H_ + KR, KK, ana, ince)
    kafes_kiris(-xk, xk, Y, H_ + KR / 2, KR, ana, ince)


def serit_katmani():
    sc = bos_sahne(w=1920, h=1080, saydam=True, ornek=min(ORNEK, 64))
    if KAPAK:
        sc.view_settings.exposure = POZLAMA
    kam = kamera(sc)
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (*lin(hex3("#d8d8e4")), 1)
    sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.08
    Y = KAP["y"]
    kopru_yol(); korkuluk(); kapi()
    isik("AREA", (0, 4, 6), 500, lin(hex3("#ff9ad8")), 8, yon=(0, 5, 0))
    isik("AREA", (0, Y - 3, 5), 1200, lin(hex3("#ffffff")), 5, yon=(0, Y, 2))
    W_, H_, KK = KAP["w"], KAP["h"], KAP["kule"]
    ic = W_ / 2 - KK
    bpy.context.view_layer.update()
    px = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-ic, Y, 0), (ic, Y, 0), (-ic, Y, H_), (ic, Y, H_))]
    xs = [p.x * 1920 for p in px]; ys = [(1 - p.y) * 1080 for p in px]
    YERLESIM[ON_EK + "aciklik_p1"] = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
    YERLESIM["yol"] = {"y_kapi": Y, "genislik": YOL_W, "kam": KAM, "serit_w": 1920}
    yaz(sc, ON_EK + "serit.png")


ON_EK = ""
if YALNIZ == "kapak":
    ON_EK = "kapak-"
    gok_katmani(); serit_katmani()
if YALNIZ in ("hepsi", "sahne"):
    gok_katmani(); serit_katmani()
json.dump(YERLESIM, open(os.path.join(CIKTI, "yerlesim.json"), "w"), indent=1)
log("bitti (neonkopru)", YERLESIM.get("aciklik_p1"))
