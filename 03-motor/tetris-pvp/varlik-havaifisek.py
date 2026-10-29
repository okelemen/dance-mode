"""HUMAN TETRIS 11. video (REF-062 HumanWarmUp, CO-OP 2 oyuncu) - HAVAI FISEKLI GECE KOPRUSU sahne varliklari, TEK serit.

varlik.py tarafindan calistirilir (yardimcilar oradan gelir):
    blender -b --factory-startup -noaudio -P 03-motor/tetris-pvp/varlik.py -- --mod havaifisek --cikti cikti [--ornek 64] [--yalniz sahne]

REF-062'de ne varsa (CLAUDE.md md. 22): tunel YOK; kapkara gece gogu, yildiz tozu ve havai fisek dumani; ortada parlak KIRMIZI
kopru yol (kenarlarda pembe isik), yolda kameraya dogru buyuyen beyaz parlak chevron bantlar; pembe metal korkuluk, cam panellerde
akan altin cift oklar; beyaz kafes (truss) kapi, ust kirisin arkasinda koyu lacivert tugla bant. Havai fisekler, "Coming Soon"
tabelasi, P1/P2 neon ikonlari, "!" uyarisi ve duvarlar motorda (sahne8.html) cizilir - gok.png duragan zemindir.
Kamera REF-062 karesinden (t60): alcak ve neredeyse yatay; kapi acikligi ekranin ~%33 eni, ust kenar ~%32, alt kenar ~%65 boyda.

Ciktilar (sahne8.html 2B'de birlestirir, kamera sabit):
  gok.png        1920x1080  gece gogu (yildiz tozu, duman) - tam ekran, opak
  serit.png      1920x1080  kopru yol, chevron, korkuluk, kafes kapi (gokte saydam)
  yerlesim.json  aciklik_p1 (kapi acikligi, ekran px), yol
"""

YERLESIM.clear()
KAP = {"y": 8.6, "w": 7.4, "h": 3.6, "kule": 0.42, "kiris": 0.42}      # aciklik 6,56 x 3,6
KAM = {"z": 1.06, "egim": -3.0, "lens": 18.0, "sensor": 24.0}
YOL_W = 7.6
Y_SON = 9.4                     # sahne 2: kopru kapinin hemen arkasinda biter (REF-062)
KIRMIZI, PEMBE, ALTIN = "#d0102c", "#ff6fae", "#ffc23a"
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
    """yere yatik duz cokgen"""
    me = bpy.data.meshes.new(ad)
    me.from_pydata([(a, b, 0) for a, b in noktalar], [], [list(range(len(noktalar)))]); me.update()
    o = bpy.data.objects.new(ad, me); bpy.context.collection.objects.link(o)
    o.location = konum; o.data.materials.append(mat)
    return o


# ------------------------------------------------------------------ GOK katmani = gece gogu (yildiz tozu + duman)
def gece_perdesi():
    """kameranin karsisinda dev dik duzlem: koyu lacivert-siyah, voronoi yildiz tozu, soluk mor-gri duman (havai fisek artigi)"""
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 600, 120), rotation=(math.pi / 2, 0, 0))
    p = bpy.context.active_object; p.scale = (2600, 1500, 1)
    m = bpy.data.materials.new("gece"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord")
    # yildiz tozu: ince voronoi noktalari (iki olcek)
    em_top = None
    for olc, esik, guc in ((900.0, 0.035, 9.0), (320.0, 0.05, 5.0)):
        vo = nt.nodes.new("ShaderNodeTexVoronoi"); vo.feature = "F1"
        vo.inputs["Scale"].default_value = olc
        nt.links.new(tc.outputs["Generated"], vo.inputs["Vector"])
        cr = nt.nodes.new("ShaderNodeMapRange")
        cr.inputs["From Min"].default_value = esik; cr.inputs["From Max"].default_value = 0.0
        cr.inputs["To Min"].default_value = 0.0; cr.inputs["To Max"].default_value = guc
        nt.links.new(vo.outputs["Distance"], cr.inputs["Value"])
        em_top = cr if em_top is None else _topla(nt, em_top, cr)
    # duman: buyuk olcekli gurultu, soluk mor-gri, ust yarida yogun
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 4.5; nz.inputs["Detail"].default_value = 8
    nz.inputs["Roughness"].default_value = 0.62
    nt.links.new(tc.outputs["Generated"], nz.inputs["Vector"])
    dm = nt.nodes.new("ShaderNodeMapRange")
    dm.inputs["From Min"].default_value = 0.52; dm.inputs["From Max"].default_value = 0.82
    dm.inputs["To Min"].default_value = 0.0; dm.inputs["To Max"].default_value = 0.16
    nt.links.new(nz.outputs["Fac"], dm.inputs["Value"])
    taban = nt.nodes.new("ShaderNodeEmission"); taban.inputs[0].default_value = (*lin(hex3("#05040c")), 1)
    taban.inputs[1].default_value = 1.0
    duman = nt.nodes.new("ShaderNodeEmission"); duman.inputs[0].default_value = (*lin(hex3("#8a7a9c")), 1)
    nt.links.new(dm.outputs[0], duman.inputs[1])
    yildiz = nt.nodes.new("ShaderNodeEmission"); yildiz.inputs[0].default_value = (*lin(hex3("#fff4e4")), 1)
    nt.links.new(em_top.outputs[0], yildiz.inputs[1])
    a1 = nt.nodes.new("ShaderNodeAddShader"); nt.links.new(taban.outputs[0], a1.inputs[0]); nt.links.new(duman.outputs[0], a1.inputs[1])
    a2 = nt.nodes.new("ShaderNodeAddShader"); nt.links.new(a1.outputs[0], a2.inputs[0]); nt.links.new(yildiz.outputs[0], a2.inputs[1])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(a2.outputs[0], o.inputs[0])
    p.data.materials.append(m)


def _topla(nt, a, b):
    t = nt.nodes.new("ShaderNodeMath"); t.operation = "ADD"
    nt.links.new(a.outputs[0], t.inputs[0]); nt.links.new(b.outputs[0], t.inputs[1])
    return t


def gok_katmani():
    sc = bos_sahne(w=1920, h=1080, ornek=min(ORNEK, 32))
    if KAPAK:
        sc.view_settings.exposure = POZLAMA
    kamera(sc)
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (*lin(hex3("#05040c")), 1)
    sc.world.node_tree.nodes["Background"].inputs[1].default_value = 1.0
    gece_perdesi()
    if KAPAK:
        kapak_fisekleri()
    yaz(sc, ON_EK + "gok.png")


def kapak_fisekleri():
    """KAPAK: REF-062 kapaginda gokyuzu buyuk havai fisek patlamalariyla dolu (videoda motor ciziyor; kapakta 2B boyama yok -> Blender'da).
    Her patlama: merkezden isinsal ince isikli cizgiler + uclarinda parlak nokta; uzak duzlemde (y 300)."""
    rnd = random.Random(62)
    renkler = ["#ff5a4a", "#ffd24a", "#ff7ad8", "#ffffff", "#ff9a3a", "#c8a0ff"]
    for cx_, cz, R in ((-170, 120, 46), (150, 135, 52), (-60, 160, 34), (60, 95, 30), (-230, 60, 30), (235, 70, 34), (0, 205, 40)):
        renk = rnd.choice(renkler)
        m = mat_emis("fisek", lin(hex3(renk)), 7.0); uc = mat_emis("fisek_uc", lin(hex3("#fff6e0")), 14.0)
        for i in range(70):
            a = i / 70 * 2 * math.pi + rnd.uniform(-0.03, 0.03)
            r0, r1 = R * rnd.uniform(0.25, 0.45), R * rnd.uniform(0.8, 1.05)
            dz = -R * 0.12 * (r1 / R) ** 2                      # ucta hafif dusus
            a0 = (cx_ + math.cos(a) * r0, 300, cz + math.sin(a) * r0)
            a1 = (cx_ + math.cos(a) * r1, 300, cz + math.sin(a) * r1 + dz)
            boru(a0, a1, 0.25, m)
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.7, location=a1, segments=8, ring_count=4)
            bpy.context.active_object.data.materials.append(uc)


# ------------------------------------------------------------------ SERIT katmani (kopru yol + korkuluk + kafes kapi)
def kopru_yol():
    # sahne 1: yol pembe parliyordu (parlak yuzey pembe isiklari yansitti) -> daha mat, koyu kirmizi govde
    yol = mat_metal("yol", lin(hex3(KIRMIZI)), 0.42, metal=0.05)
    # sahne 2: REF-062'de kopru KAPIDA biter (arkasi karanlik gok) ve yolun ORTASI koyu serit, kirmizi yalniz kenarlarda
    yuvarlak_kutu("yol", (0, (0.3 + Y_SON) / 2, -0.2), (YOL_W, Y_SON - 0.3, 0.4), yol, egim=0.05, seg=2)
    koyu = mat_metal("yol_orta", lin(hex3("#140a10")), 0.35, metal=0.0)
    yuvarlak_kutu("orta", (0, (0.3 + Y_SON) / 2, 0.012), (3.9, Y_SON - 0.3, 0.02), koyu, egim=0.0, seg=1)
    beyaz = mat_emis("chev", lin(hex3("#fffaf4")), 6.0)
    # REF-062: tepesi KAMERAYA bakan, kameraya dogru buyuyen beyaz V bantlar (sahne 1'de ters cizildi; sahne 2: kucuktu)
    for yy, hw, kal in ((0.9, 1.75, 0.6), (2.3, 1.55, 0.48), (3.55, 1.38, 0.4), (4.65, 1.24, 0.33), (5.65, 1.12, 0.28), (6.55, 1.02, 0.24), (7.35, 0.94, 0.2)):
        d = hw * 0.42
        sekil("chev", [(-hw, yy + d), (0, yy), (hw, yy + d), (hw, yy + d + kal), (0, yy + kal), (-hw, yy + d + kal)], beyaz, konum=(0, 0, 0.03))
    for s in (-1, 1):
        boru((s * (YOL_W / 2 - 0.06), 0.3, 0.03), (s * (YOL_W / 2 - 0.06), Y_SON, 0.03), 0.05, mat_emis("kenar%d" % s, lin(hex3(PEMBE)), 6))


def korkuluk():
    metal = mat_metal("kork_metal", lin(hex3("#ff9ec4")), 0.25, metal=0.6)
    cam = mat_cam("kork_cam")
    okm = mat_emis("ok", lin(hex3(ALTIN)), 6)
    pem = mat_emis("kork_neon", lin(hex3(PEMBE)), 5)
    for s in (-1, 1):
        x = s * (YOL_W / 2 + 0.25)
        hk = 0.95
        ys = [0.5 + i * 1.7 for i in range(int((KAP["y"] - 0.5) / 1.7) + 1)] + [KAP["y"]]   # korkuluk da kapida biter
        for yy in ys:
            yuvarlak_kutu("dikme", (x, yy, hk / 2), (0.09, 0.09, hk), metal, egim=0.02, seg=2)
        yuvarlak_kutu("tirabzan", (x, (ys[0] + ys[-1]) / 2, hk + 0.02), (0.11, ys[-1] - ys[0], 0.08), metal, egim=0.03, seg=2)
        yuvarlak_kutu("orta", (x, (ys[0] + ys[-1]) / 2, hk * 0.55), (0.05, ys[-1] - ys[0], 0.05), metal, egim=0.01, seg=1)
        yuvarlak_kutu("cam", (x, (ys[0] + ys[-1]) / 2, hk / 2), (0.03, ys[-1] - ys[0], hk * 0.86), cam, egim=0.0, seg=1)
        boru((x, ys[0], 0.05), (x, ys[-1], 0.05), 0.03, pem)
        # REF-062: korkuluk camında kameraya bakan altin cift oklar (gruplar halinde)
        for y0 in (0.9, 3.4, 6.0):          # sahne 3: 8,8'deki grup korkuluk bittikten sonra havada kaliyordu
            for j in range(2):
                yy = y0 + j * 0.5
                pts = [(yy + 0.38, 0.16), (yy, 0.46), (yy + 0.38, 0.76), (yy + 0.6, 0.76), (yy + 0.22, 0.46), (yy + 0.6, 0.16)]
                me = bpy.data.meshes.new("ok"); me.from_pydata([(x - s * 0.04, a, b) for a, b in pts], [], [list(range(6))]); me.update()
                ob = bpy.data.objects.new("ok", me); bpy.context.collection.objects.link(ob); ob.data.materials.append(okm)


def kapi():
    """REF-062 beyaz kafes (truss) kapi: iki kule + ust kiris; kirisin arkasinda koyu lacivert tugla bant"""
    Y, W, H, KK, KR = KAP["y"], KAP["w"], KAP["h"], KAP["kule"], KAP["kiris"]
    # sahne 2: metal 0,95 cevredeki pembeyi yansitip kapiyi pembe gosterdi -> beyaz boyali metal
    ana = mat_metal("kapi_ana", lin(hex3("#f4f4fa")), 0.35, metal=0.2)
    ince = mat_metal("kapi_ince", lin(hex3("#dadbe6")), 0.4, metal=0.2)
    xk = W / 2 - KK / 2
    for s in (-1, 1):
        kafes_kule(s * xk, Y, 0.0, H + KR, KK, ana, ince)
    kafes_kiris(-xk, xk, Y, H + KR / 2, KR, ana, ince)
    tugla = mat_metal("tugla", lin(hex3("#1d2a52")), 0.6, metal=0.1)
    yuvarlak_kutu("bant", (0, Y + 0.25, H - 0.22), (W - 2 * KK, 0.1, 0.42), tugla, egim=0.01, seg=1)


def serit_katmani():
    sc = bos_sahne(w=1920, h=1080, saydam=True, ornek=min(ORNEK, 64))
    if KAPAK:
        sc.view_settings.exposure = POZLAMA
    kam = kamera(sc)
    # sahne 1: pembe dunya isigi kapiyi pembeye boyadi -> notr koyu dunya, kapiya beyaz isik
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (*lin(hex3("#d8d8e4")), 1)
    sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.12
    Y = KAP["y"]
    kopru_yol()
    korkuluk()
    kapi()
    # yol: ustten notr isik + yanlarda hafif pembe (REF-062 kirmizi yolda pembe kenar parlamasi), kapiya beyaz on isik
    isik("AREA", (0, 4, 6), 2200, lin(hex3("#fff4f0")), 8, yon=(0, 5, 0))
    isik("AREA", (-6, 6, 2.0), 500, lin(hex3(PEMBE)), 6, yon=(-2, 8, 0))
    isik("AREA", (6, 6, 2.0), 500, lin(hex3(PEMBE)), 6, yon=(2, 8, 0))
    isik("AREA", (0, Y - 3, 5), 1400, lin(hex3("#ffffff")), 5, yon=(0, Y, 2))
    W_, H_, KK = KAP["w"], KAP["h"], KAP["kule"]
    ic = W_ / 2 - KK
    bpy.context.view_layer.update()
    px = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-ic, Y, 0), (ic, Y, 0), (-ic, Y, H_), (ic, Y, H_))]
    xs = [p.x * 1920 for p in px]; ys = [(1 - p.y) * 1080 for p in px]
    YERLESIM[ON_EK + "aciklik_p1"] = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
    YERLESIM["yol"] = {"y_kapi": Y, "genislik": YOL_W, "kam": KAM, "serit_w": 1920}
    log("aciklik", YERLESIM[ON_EK + "aciklik_p1"])
    yaz(sc, ON_EK + "serit.png")


# ------------------------------------------------------------------ ana akis (havai fisek gecesi)
ON_EK = ""
if YALNIZ == "kapak":
    ON_EK = "kapak-"
    gok_katmani(); serit_katmani()
if YALNIZ in ("hepsi", "sahne"):
    gok_katmani()
    serit_katmani()
json.dump(YERLESIM, open(os.path.join(CIKTI, "yerlesim.json"), "w"), indent=1)
log("bitti (havaifisek)", YERLESIM.get("aciklik_p1"))
