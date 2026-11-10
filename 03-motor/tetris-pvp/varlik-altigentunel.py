"""HUMAN TETRIS 23. video (REF-078 HumanWarmUp, CO-OP 2 oyuncu) - ALTIGEN NEON TUNEL sahne varliklari, TEK serit. varlik.py calistirir (--mod altigentunel).

REF-078'de ne varsa (md. 22): koyu mor gece, ic ice neon altigen tunel (mavi + pembe), koyu mor yol, parlak pembe chevron basamaklar,
pembe neon korkuluk + ok dizileri, gri metal kafes kapi. "Coming Soon" tabelasi, sari duvar, Mission sayaci, "!" motorda.
varlik-neonkopru.py tabanli (ayni kanalin ayni kopru dunyasi); sehir / sahne kuleleri YOK (referansta yok), yerine altigen tunel.
"""

import random
YERLESIM.clear()
KAP = {"y": 8.6, "w": 7.4, "h": 3.6, "kule": 0.42, "kiris": 0.42}
KAM = {"z": 1.06, "egim": -3.0, "lens": 18.0, "sensor": 24.0}
YOL_W = 7.6
Y_SON = 9.4
PEMBE, MOR, MAVI = "#ff3fb0", "#8a3cff", "#3f7bff"
KAPAK = YALNIZ == "kapak"
POZLAMA = float(arg("--kapak-pozlama", "0"))
if KAPAK:                                                  # REF-078 kapak kompozisyonu: ufuk ~%46, kapi saga kacik, yol kadrajin alt yarisi
    KAM.update(z=float(arg("--kapak-z", "1.9")), egim=float(arg("--kapak-egim", "3.0")), x=float(arg("--kapak-x", "-1.4")),
               lens=float(arg("--kapak-lens", "18")))
    KAP["y"] = float(arg("--kapak-kapi-y", "9.0")); Y_SON = KAP["y"] + 0.8
TUNEL_Z = KAP["h"] / 2 + 0.4                               # altigenlerin merkezi: kapi acikliginin ortasi


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


def altigen_tunel():
    """REF-078: ic ice neon altigenler (tepe noktasi yukarida), sirayla pembe / mavi; sabit yaricap, derinlik perspektifle ic ice okunur"""
    guc = 9 if KAPAK else 5
    mp, mm = mat_emis("alt_pembe", lin(hex3(PEMBE)), guc), mat_emis("alt_mavi", lin(hex3(MAVI)), guc)
    R = 9.5
    for k, y in enumerate((11.5, 15, 19.5, 25, 32, 41, 52, 66, 84, 108)):
        m = mm if k % 2 else mp
        ks = [(R * math.sin(math.radians(60 * i)), y, TUNEL_Z + R * math.cos(math.radians(60 * i))) for i in range(6)]
        for i in range(6):
            boru(ks[i], ks[(i + 1) % 6], 0.11 + 0.012 * k, m)
    for k, y in enumerate((13, 22, 36, 58)):               # arada ince ikinci halka (referansta cift cizgi)
        m = mp if k % 2 else mm
        r2 = R * 0.9
        ks = [(r2 * math.sin(math.radians(60 * i)), y, TUNEL_Z + r2 * math.cos(math.radians(60 * i))) for i in range(6)]
        for i in range(6):
            boru(ks[i], ks[(i + 1) % 6], 0.05, m)


def yildizlar():
    rnd = random.Random(78)
    ms = [mat_emis("yildiz%d" % i, lin(hex3(r)), 6) for i, r in enumerate(("#ffd0f0", "#b0c8ff", "#ff7ad0"))]
    for i in range(170):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=rnd.uniform(0.12, 0.3), location=(rnd.uniform(-190, 190), 150, rnd.uniform(-40, 150)), segments=8, ring_count=6)
        bpy.context.active_object.data.materials.append(ms[i % 3])


def gok_katmani():
    sc = bos_sahne(w=1920, h=1080, ornek=min(ORNEK, 32))
    if KAPAK:
        sc.view_settings.exposure = POZLAMA
    kamera(sc)
    nt = sc.world.node_tree                                # gok: ufukta mor-pembe, tepede koyu mor (siyah degil: referans siyah orani dusuk)
    tc = nt.nodes.new("ShaderNodeTexCoord"); ay = nt.nodes.new("ShaderNodeSeparateXYZ"); ra = nt.nodes.new("ShaderNodeValToRGB")
    nt.links.new(tc.outputs["Generated"], ay.inputs[0]); nt.links.new(ay.outputs["Z"], ra.inputs[0])
    cr = ra.color_ramp
    alt, orta, ust = ("#c01490", "#7a0c8c", "#40066a") if KAPAK else ("#3a0a52", "#1c0534", "#0e0220")
    cr.elements[0].position = 0.0; cr.elements[0].color = (*lin(hex3(alt)), 1)
    cr.elements[1].position = 0.6; cr.elements[1].color = (*lin(hex3(ust)), 1)
    e = cr.elements.new(0.2); e.color = (*lin(hex3(orta)), 1)
    nt.links.new(ra.outputs["Color"], nt.nodes["Background"].inputs[0])
    nt.nodes["Background"].inputs[1].default_value = 1.0
    altigen_tunel(); yildizlar()
    yaz(sc, ON_EK + "gok.png")


def kopru_yol():
    yol = mat_emis("yol", lin(hex3("#3c0a56")), 1.0) if KAPAK else mat_metal("yol", lin(hex3("#12051c")), 0.55, metal=0.0)
    yuvarlak_kutu("yol", (0, (0.3 + Y_SON) / 2, -0.2), (YOL_W, Y_SON - 0.3, 0.4), yol, egim=0.05, seg=2)
    pembe = mat_emis("chev", lin(hex3("#ff2fa8")), 1.7)
    for yy, hw, kal in ((0.9, 1.75, 0.6), (2.3, 1.55, 0.48), (3.55, 1.38, 0.4), (4.65, 1.24, 0.33), (5.65, 1.12, 0.28), (6.55, 1.02, 0.24), (7.35, 0.94, 0.2)):
        d = hw * 0.42
        if KAPAK:                                          # REF-078 kapagi: genis, dolu parlak pembe chevron
            hw *= 1.35; kal *= 1.25; d = hw * 0.42
        kose = [(-hw, yy + d), (0, yy), (hw, yy + d), (hw, yy + d + kal), (0, yy + kal), (-hw, yy + d + kal)]
        if KAPAK:
            sekil("chev", kose, mat_emis("chev_ic", lin(hex3("#ff58c0")), 1.5), konum=(0, 0, 0.03))
            for i in range(6):
                boru((*kose[i], 0.04), (*kose[(i + 1) % 6], 0.04), 0.03, mat_emis("chev_k", lin(hex3("#ffb0e0")), 6))
            continue
        sekil("chev", kose, pembe, konum=(0, 0, 0.03))
    for s in (-1, 1):
        boru((s * (YOL_W / 2 - 0.06), 0.3, 0.03), (s * (YOL_W / 2 - 0.06), Y_SON, 0.03), 0.06, mat_emis("kenar%d" % s, lin(hex3(PEMBE)), 3))


def korkuluk():
    metal = mat_metal("kork_metal", lin(hex3("#7a2a8a")), 0.3, metal=0.5)
    okm = mat_emis("ok", lin(hex3("#ff7ad8")), 2.2)
    pem = mat_emis("kork_neon", lin(hex3(PEMBE)), 6 if KAPAK else 2.6)
    mor = mat_emis("kork_led", lin(hex3(MOR)), 3.5)
    kal = 0.06 if KAPAK else 0.035                         # REF-078 kapagi: kalin parlak korkuluk borulari
    for s in (-1, 1):
        x = s * (YOL_W / 2 + 0.25)
        hk = 1.25 if KAPAK else 0.95
        ys = [0.5 + i * 1.7 for i in range(int((KAP["y"] - 0.5) / 1.7) + 1)] + [KAP["y"]]
        for yy in ys:
            yuvarlak_kutu("dikme", (x, yy, hk / 2), (0.1, 0.1, hk), metal, egim=0.02, seg=2)
        for oran in ((1.0, 0.72, 0.44) if KAPAK else (1.0, 0.62)):
            boru((x, ys[0], hk * oran), (x, ys[-1], hk * oran), kal, pem)
        for j in range(int((ys[-1] - ys[0]) / 0.5)):       # altta kesikli mor LED serit
            y0 = ys[0] + j * 0.5
            boru((x, y0, 0.06), (x, y0 + 0.28, 0.06), 0.03, mor)
        if KAPAK:
            continue                                       # kapakta ok dizisi yok (referans kapakta korkuluk duz)
        for y0 in (0.9, 3.4, 6.0):                         # REF-078: korkulukta uclu ok dizisi <<< >>>
            for j in range(3):
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
    if KAPAK:                                              # REF-078 kapagi: kapida sari duvar (delik silueti kapak betiginde eklenir)
        ic = W_ / 2 - KK
        sari = mat_emis("sari_duvar", lin(hex3("#fff000")), 1.0)
        me = bpy.data.meshes.new("duvar"); me.from_pydata([(-ic, Y + 0.05, 0), (ic, Y + 0.05, 0), (ic, Y + 0.05, H_), (-ic, Y + 0.05, H_)], [], [[0, 1, 2, 3]]); me.update()
        ob = bpy.data.objects.new("duvar", me); bpy.context.collection.objects.link(ob); ob.data.materials.append(sari)


def kapi_susu():
    """kapi acikligini saran cift neon (TALIMATLAR §4: zengin kapi); kapakta yok (referans kapakta kapi yalin kafes)"""
    Y, W_, H_, KK = KAP["y"], KAP["w"], KAP["h"], KAP["kule"]
    ic = W_ / 2 - KK
    pem, mav = mat_emis("kap_pem", lin(hex3(PEMBE)), 4), mat_emis("kap_mav", lin(hex3(MAVI)), 3.6)
    for m, p in ((pem, 0.02), (mav, 0.12)):
        for a, b in (((-ic + p, Y - 0.25, 0.05), (-ic + p, Y - 0.25, H_ - p)), ((ic - p, Y - 0.25, 0.05), (ic - p, Y - 0.25, H_ - p)), ((-ic + p, Y - 0.25, H_ - p), (ic - p, Y - 0.25, H_ - p))):
            boru(a, b, 0.028, m)


def yol_ledleri():
    pem = mat_emis("yol_led", lin(hex3(PEMBE)), 3)
    mav = mat_emis("yol_mav", lin(hex3(MAVI)), 2.8)
    for s in (-1, 1):
        for j in range(16):
            y = 0.8 + j * 0.5
            boru((s * 2.95, y, 0.02), (s * 2.95, y + 0.26, 0.02), 0.022, mav if j % 2 else pem)


def serit_katmani():
    sc = bos_sahne(w=1920, h=1080, saydam=True, ornek=min(ORNEK, 64))
    if KAPAK:
        sc.view_settings.exposure = POZLAMA
    kam = kamera(sc)
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (*lin(hex3("#e0c8f0")), 1)
    sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.08
    Y = KAP["y"]
    kopru_yol(); korkuluk(); kapi()
    if not KAPAK:
        kapi_susu(); yol_ledleri()
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
log("bitti (altigentunel)", YERLESIM.get(ON_EK + "aciklik_p1"))
