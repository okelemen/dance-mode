"""HUMAN TETRIS 12. video (REF-063 HumanWarmUp, 1 oyuncu) - NEON KOPRU sahne varliklari, TEK serit. varlik.py calistirir (--mod neonkopru).

REF-063'te ne varsa (md. 22): kapkara gece, koyu mor yol, parlak pembe chevron basamaklar, cift neon pembe korkuluk, altinda mor LED serit,
korkulukta pembe cift oklar, gri metal kafes kapi. Lazer yildizlar, isik toplari, "Coming Soon", "!" ve duvarlar motorda (sahne9.html).
"""

import random
YERLESIM.clear()
KAP = {"y": 8.6, "w": 7.4, "h": 3.6, "kule": 0.42, "kiris": 0.42}
KAM = {"z": 1.06, "egim": -3.0, "lens": 18.0, "sensor": 24.0}
YOL_W = 7.6
Y_SON = 9.4
PEMBE, MOR = "#ff3fb0", "#8a3cff"
KAPAK = YALNIZ == "kapak"
POZLAMA = float(arg("--kapak-pozlama", "0"))
if KAPAK:                                                  # REF-063 kapak kompozisyonu: ufuk %46, kapi saga kacik ve daha uzak
    KAM.update(z=1.35, egim=3.0, x=-1.5)
    KAP["y"] = 10.4; Y_SON = 11.2


def kamera(sc):
    rx = math.radians(90 - KAM["egim"])
    bpy.ops.object.camera_add(location=(KAM.get("x", 0), 0, KAM["z"]), rotation=(rx, 0, 0))
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
    m = mat_emis("lazer", lin(hex3("#ff6ac4")), 14.0)
    for a, b in (((-260, 300, 40), (-40, 300, 215)), ((-40, 300, 215), (70, 300, 80)), ((70, 300, 80), (280, 300, 190)), ((-180, 300, 150), (120, 300, 230))):
        boru(a, b, 1.5, m)


def gok_katmani():
    sc = bos_sahne(w=1920, h=1080, ornek=min(ORNEK, 16))
    if KAPAK:
        sc.view_settings.exposure = POZLAMA
    kamera(sc)
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (*lin(hex3("#0b0212")), 1)
    sc.world.node_tree.nodes["Background"].inputs[1].default_value = 1.0
    if KAPAK:
        kapak_lazer()
        nt = sc.world.node_tree                            # gok ufukta sicak pembe, tepede koyu mor (referans siyah orani 0,11)
        tc = nt.nodes.new("ShaderNodeTexCoord"); ay = nt.nodes.new("ShaderNodeSeparateXYZ"); ra = nt.nodes.new("ShaderNodeValToRGB")
        nt.links.new(tc.outputs["Generated"], ay.inputs[0]); nt.links.new(ay.outputs["Z"], ra.inputs[0])
        cr = ra.color_ramp; cr.elements[0].position = 0.0; cr.elements[0].color = (*lin(hex3("#e0206e")), 1)
        cr.elements[1].position = 0.55; cr.elements[1].color = (*lin(hex3("#2a0628")), 1)
        e = cr.elements.new(0.2); e.color = (*lin(hex3("#7a1250")), 1)
        nt.links.new(ra.outputs["Color"], nt.nodes["Background"].inputs[0])
    yaz(sc, ON_EK + "gok.png")


def kopru_yol():
    yol = mat_emis("yol", lin(hex3("#4a0c4c")), 1.0) if KAPAK else mat_metal("yol", lin(hex3("#0d0414")), 0.55, metal=0.0)
    yuvarlak_kutu("yol", (0, (0.3 + Y_SON) / 2, -0.2), (YOL_W, Y_SON - 0.3, 0.4), yol, egim=0.05, seg=2)
    pembe = mat_emis("chev", lin(hex3("#ff2fa8")), 1.7)
    for yy, hw, kal in ((0.9, 1.75, 0.6), (2.3, 1.55, 0.48), (3.55, 1.38, 0.4), (4.65, 1.24, 0.33), (5.65, 1.12, 0.28), (6.55, 1.02, 0.24), (7.35, 0.94, 0.2)):
        d = hw * 0.42
        sekil("chev", [(-hw, yy + d), (0, yy), (hw, yy + d), (hw, yy + d + kal), (0, yy + kal), (-hw, yy + d + kal)], pembe, konum=(0, 0, 0.03))
    for s in (-1, 1):
        boru((s * (YOL_W / 2 - 0.06), 0.3, 0.03), (s * (YOL_W / 2 - 0.06), Y_SON, 0.03), 0.06, mat_emis("kenar%d" % s, lin(hex3(PEMBE)), 3))


def korkuluk():
    metal = mat_metal("kork_metal", lin(hex3("#3a1a4a")), 0.3, metal=0.5)
    okm = mat_emis("ok", lin(hex3("#ff3fb8")), 1.8)
    pem = mat_emis("kork_neon", lin(hex3(PEMBE)), 2.6)
    mor = mat_emis("kork_led", lin(hex3(MOR)), 3.5)
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



# ------------------------------------------------------------------ DOLGU (kullanici 30 Eki 2026: "cok bos duruyor, konseptine gore doldur")
# Neon konseptinden: ufukta neon sehir, kopru altinda isikli izgara, yanlarda sahne kuleleri + spot + ok panelleri, kapida neon + ampul.
RND = random.Random(63)
NEON = ("#ff3fb0", "#19e0d0", "#8a3cff", "#ff8a2a")


def neon_sehir():
    govde = mat_metal("kule", lin(hex3("#1a0a30")), 0.5, metal=0.2)
    pencere = {r: mat_emis("pen" + r, lin(hex3(r)), 2.4) for r in NEON}
    for s in (-1, 1):
        for i in range(16):
            x = s * (8.5 + i * 3.3 + RND.uniform(-0.8, 0.8)); y = RND.uniform(22, 70)
            w, h = RND.uniform(2.2, 4.2), RND.uniform(5, 13) + i * 1.3
            yuvarlak_kutu("kule", (x, y, h / 2 - 2), (w, 2.5, h), govde, egim=0.01, seg=1)
            renk = pencere[RND.choice(NEON)]
            for dx in (-w / 2, w / 2):
                boru((x + dx, y - 1.3, -2), (x + dx, y - 1.3, h - 2), 0.05, renk)
            boru((x - w / 2, y - 1.3, h - 2), (x + w / 2, y - 1.3, h - 2), 0.05, renk)
            for j in range(int(h / 1.4)):                  # yatay pencere bantlari
                if RND.random() < 0.72:
                    zz = -1 + j * 1.4
                    a0 = x - w * 0.38; boru((a0, y - 1.3, zz), (a0 + w * RND.uniform(0.35, 0.76), y - 1.3, zz), 0.045, renk)


def neon_zemin():
    """kopru altinda, kenarlardan ufka uzanan isikli izgara"""
    mor = mat_emis("izgara", lin(hex3("#a03cff")), 2.2)
    for i in range(4, 28):
        for s in (-1, 1):
            x = s * i * 2.0
            boru((x, 1.0, -2.6), (x, 90, -2.6), 0.035, mor)
    for j in range(24):
        y = 2 + j ** 1.5 * 0.75
        for s in (-1, 1):
            boru((s * 8.0, y, -2.6), (s * 56, y, -2.6), 0.035, mor)


def sahne_kuleleri():
    ana = mat_metal("yk_ana", lin(hex3("#7e7e88")), 0.35, metal=0.6)
    ince = mat_metal("yk_ince", lin(hex3("#60606a")), 0.4, metal=0.6)
    spot = {r: mat_emis("spot" + r, lin(hex3(r)), 7) for r in NEON}
    pano = mat_metal("pano", lin(hex3("#12061e")), 0.5, metal=0.1)
    okm = mat_emis("pano_ok", lin(hex3("#ff3fb0")), 2.6)
    for s in (-1, 1):
        for x, y, h in ((6.6, 8.6, 5.2), (8.3, 6.4, 6.6)):
            kafes_kule(s * x, y, -0.2, h, 0.34, ana, ince)
            for j in range(4):                              # kule tepesinde spot sirasi
                r_ = spot[NEON[(j + (y > 7)) % 4]]
                bpy.ops.mesh.primitive_uv_sphere_add(radius=0.13, location=(s * x, y - 0.2, h - 0.3 - j * 0.6), segments=12, ring_count=8)
                bpy.context.active_object.data.materials.append(r_)
        # kapi yaninda ok panosu
        yuvarlak_kutu("pano", (s * 5.15, 8.7, 1.75), (1.3, 0.08, 3.1), pano, egim=0.01, seg=1)
        for j in range(4):
            z = 0.7 + j * 0.7
            boru((s * 4.75, 8.62, z), (s * 5.15, 8.62, z + 0.36), 0.04, okm)
            boru((s * 5.55, 8.62, z), (s * 5.15, 8.62, z + 0.36), 0.04, okm)


def kapi_susu():
    """kapi acikligini saran cift neon + ust kiris altinda ampul dizisi (TALIMATLAR §4: zengin kapi)"""
    Y, W_, H_, KK = KAP["y"], KAP["w"], KAP["h"], KAP["kule"]
    ic = W_ / 2 - KK
    pem, cam = mat_emis("kap_pem", lin(hex3("#ff3fb0")), 4), mat_emis("kap_cam", lin(hex3("#19e0d0")), 3.2)
    for m, p in ((pem, 0.02), (cam, 0.12)):
        for a, b in (((-ic + p, Y - 0.25, 0.05), (-ic + p, Y - 0.25, H_ - p)), ((ic - p, Y - 0.25, 0.05), (ic - p, Y - 0.25, H_ - p)), ((-ic + p, Y - 0.25, H_ - p), (ic - p, Y - 0.25, H_ - p))):
            boru(a, b, 0.028, m)


def yol_ledleri():
    pem = mat_emis("yol_led", lin(hex3("#ff3fb0")), 3)
    cam = mat_emis("yol_cam", lin(hex3("#19e0d0")), 2.4)
    for s in (-1, 1):
        for j in range(16):
            y = 0.8 + j * 0.5
            boru((s * 2.75, y, 0.02), (s * 2.75, y + 0.26, 0.02), 0.022, cam if j % 2 else pem)
    tepe = mat_emis("tepe", lin(hex3("#ffd0f0")), 5)
    for s in (-1, 1):
        x = s * (YOL_W / 2 + 0.25)
        for j in range(6):
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.085, location=(x, 0.5 + j * 1.7, 1.08), segments=12, ring_count=8)
            bpy.context.active_object.data.materials.append(tepe)


def serit_katmani():
    sc = bos_sahne(w=1920, h=1080, saydam=True, ornek=min(ORNEK, 64))
    if KAPAK:
        sc.view_settings.exposure = POZLAMA
    kam = kamera(sc)
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (*lin(hex3("#d8d8e4")), 1)
    sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.08
    Y = KAP["y"]
    if not KAPAK:                                          # REF-063 kapaginda sehir/kule yok (md. 22): kapak referansin sahnesi
        neon_zemin(); neon_sehir(); sahne_kuleleri()
    kopru_yol(); korkuluk(); kapi(); kapi_susu(); yol_ledleri()
    isik("AREA", (0, 4, 6), 120, lin(hex3("#ff9ad8")), 8, yon=(0, 5, 0))
    isik("AREA", (0, Y - 3, 5), 700, lin(hex3("#ffffff")), 5, yon=(0, Y, 2))
    W_, H_, KK = KAP["w"], KAP["h"], KAP["kule"]
    ic = W_ / 2 - KK
    bpy.context.view_layer.update()
    px = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-ic, Y, 0), (ic, Y, 0), (-ic, Y, H_), (ic, Y, H_))]
    xs = [p.x * 1920 for p in px]; ys = [(1 - p.y) * 1080 for p in px]
    YERLESIM[ON_EK + "aciklik_p1"] = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
    YERLESIM[ON_EK + "ampul_p1"] = []
    for i in range(23):                                    # ust kiris onunde ampul dizisi; motor (ampulCiz) yakip sondurur
        q = world_to_camera_view(sc, kam, Vector((-ic + i * 2 * ic / 22, Y - 0.3, H_ + 0.08)))
        YERLESIM[ON_EK + "ampul_p1"].append([round(q.x * 1920, 1), round((1 - q.y) * 1080, 1)])
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
