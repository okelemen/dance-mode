"""HUMAN TETRIS 10. video (REF-061 HumanWarmUp, 1 oyuncu) - NEON KUP TUNELI sahne varliklari, TEK serit.

varlik.py tarafindan calistirilir (yardimcilar oradan gelir):
    blender -b --factory-startup -noaudio -P 03-motor/tetris-pvp/varlik.py -- --mod tunel --cikti cikti [--ornek 64] [--yalniz sahne]

REF-061'de ne varsa (CLAUDE.md md. 22): sivri tepeli altigen tunel, duvarlari/tavani metalik mor-gumus kuplerle kapli (aralarda parlak
kare isiklar), tunel boyunca tekrar eden pembe-mor neon altigen cerceveler, uzakta parlak lavanta sis; ortada kopru yol: koyu parlak
zemin (solda pembe, sagda camgobegi yansima), yolda beyaz chevron seritleri, korkuluk solda pembe / sagda camgobegi; gumus kafes (truss)
kapi. "Coming Soon" tabelasi, "!" uyarisi ve duvarlar motorda (sahne7.html) cizilir.

Ciktilar (sahne7.html 2B'de birlestirir, kamera sabit):
  gok.png        1920x1080  tunel (kupler, neon cerceveler, uzak sis) - tam ekran, opak
  serit.png      1920x1080  kopru yol, chevron, korkuluk, kafes kapi (tunelde saydam)
  yerlesim.json  aciklik_p1 (kapi acikligi, ekran px), yol
"""

YERLESIM.clear()
KAP = {"y": 11.0, "w": 7.4, "h": 3.6, "kule": 0.42, "kiris": 0.42}      # aciklik 6,56 x 3,6
# sahne 1 dersi: REF-061 kamerasi yatay (hafif yukari), kapi acikligi ekranin ~%25 eni, alt kenari ~%72 boyda
KAM = {"z": 2.6, "egim": -3.0, "lens": 18.0, "sensor": 24.0}
YOL_W = 7.6
T_R, T_Z = 10.5, 3.6            # tunel: sivri tepeli altigen, yaricap / merkez yuksekligi
T_Y0, T_Y1 = -4.0, 150.0
PEMBE, CAMGOBEGI, MOR = "#ff4fd8", "#3fe8ff", "#9b5bff"


def kamera(sc):
    rx = math.radians(90 - KAM["egim"])
    bpy.ops.object.camera_add(location=(0, 0, KAM["z"]), rotation=(rx, 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.sensor_fit = "VERTICAL"; kam.data.sensor_height = KAM["sensor"]; kam.data.lens = KAM["lens"]
    kam.data.clip_end = 600
    return kam


def mat_metal(ad, renk, purluk):
    m = bpy.data.materials.new(ad); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*renk, 1); b.inputs["Metallic"].default_value = 0.95
    b.inputs["Roughness"].default_value = purluk
    return m


def sekil(ad, noktalar, mat, konum=(0, 0, 0)):
    """yere yatik duz cokgen"""
    me = bpy.data.meshes.new(ad)
    me.from_pydata([(a, b, 0) for a, b in noktalar], [], [list(range(len(noktalar)))]); me.update()
    o = bpy.data.objects.new(ad, me); bpy.context.collection.objects.link(o)
    o.location = konum; o.data.materials.append(mat)
    return o


def altigen_koseler():
    """sivri tepeli altigen (x, z): tepe ve dip kose, yanlar dikey"""
    return [(T_R * math.cos(math.radians(90 + 60 * i)), T_Z + T_R * math.sin(math.radians(90 + 60 * i))) for i in range(6)]


# ------------------------------------------------------------------ GOK katmani = tunelin kendisi
def kup_kaplama(rnd):
    """6 yuzu kuplerle kapli tek mesh (binlerce kutu tek from_pydata -> hizli). Malzeme indeksi: 0-2 metal tonlari, 3-5 isikli kare."""
    K = altigen_koseler()
    v, f, mi = [], [], []

    def kutu(o, eu, ev, en, a, b, d, m):
        """o merkez (yuzde), eu/ev yuz eksenleri, en ice normal; a x b taban, d derinlik"""
        n0 = len(v)
        for s3 in (0, d):
            for su, sv in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                v.append(tuple(o + eu * (su * a / 2) + ev * (sv * b / 2) + en * s3))
        for q in ((0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)):
            f.append(tuple(n0 + i for i in q)); mi.append(m)

    for i in range(6):
        (x0, z0), (x1, z1) = K[i], K[(i + 1) % 6]
        A, B = Vector((x0, 0, z0)), Vector((x1, 0, z1))
        L = (B - A).length; eu = (B - A).normalized(); ev = Vector((0, 1, 0))
        orta = (A + B) / 2
        en = (Vector((0, 0, T_Z)) - Vector((orta.x, 0, orta.z))).normalized()
        if orta.z < 0.5:          # alt iki yuz koprunun altinda, gorunmuyor
            continue
        hucre = 0.62
        nu = int(L / hucre)
        y = T_Y0
        while y < T_Y1:
            ad = hucre * (1 + 0.8 * (y > 30) + 1.6 * (y > 70))       # uzakta seyrek (gorunmez ayrinti icin poligon harcama)
            for j in range(nu):
                if rnd.random() < 0.08:
                    continue
                u = (j + 0.5) / nu * L
                a, b = ad * rnd.uniform(0.55, 0.98), ad * rnd.uniform(0.55, 0.98)
                d = rnd.uniform(0.08, 0.9)
                o = A + eu * u + ev * (y + ad / 2) + en * rnd.uniform(-0.05, 0.25)
                m = 3 + rnd.randrange(3) if rnd.random() < 0.025 else rnd.randrange(3)   # kesit 1: 0,07 fazla parlak
                kutu(o, eu, ev, en, a, b, d, m)
            y += ad
    me = bpy.data.meshes.new("kupler"); me.from_pydata(v, [], f); me.update()
    for p, m in zip(me.polygons, mi):
        p.material_index = m
    o = bpy.data.objects.new("kupler", me); bpy.context.collection.objects.link(o)
    for ad_, c, p in (("m_lav", "#c4b6f2", 0.16), ("m_mor", "#7a58c8", 0.22), ("m_gum", "#e8e4f4", 0.12)):   # sahne 1: fazla mavi -> gumus/lavanta
        o.data.materials.append(mat_metal(ad_, lin(hex3(c)), p))
    for ad_, c, g in (("k_pem", "#ff8ae8", 7), ("k_cam", "#8af4ff", 7), ("k_bey", "#f4eeff", 9)):
        o.data.materials.append(mat_emis(ad_, lin(hex3(c)), g))
    log("kup", len(f) // 6)


def neon_cerceveler():
    K = altigen_koseler()
    mats = [mat_emis("neon_p", lin(hex3(PEMBE)), 12), mat_emis("neon_m", lin(hex3(MOR)), 12)]
    y, j = 3.0, 0
    while y < T_Y1 - 6:
        for i in range(6):
            (x0, z0), (x1, z1) = K[i], K[(i + 1) % 6]
            if (z0 + z1) / 2 < 0.5:
                continue
            boru((x0 * 0.97, y, T_Z + (z0 - T_Z) * 0.97), (x1 * 0.97, y, T_Z + (z1 - T_Z) * 0.97), 0.09, mats[j % 2])
        y += 7.0; j += 1


def uzak_sis():
    """tunelin sonu: parlak lavanta isik (REF-061 kadraj ortasinda beyazimsi derinlik)"""
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, T_Y1 - 2, T_Z), rotation=(math.pi / 2, 0, 0))
    p = bpy.context.active_object; p.scale = (T_R * 2, T_R * 2, 1)
    m = bpy.data.materials.new("sis"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord")
    gr = nt.nodes.new("ShaderNodeTexGradient"); gr.gradient_type = "SPHERICAL"
    mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Location"].default_value = (0.5, 0.5, 0); mp.inputs["Scale"].default_value = (1.6, 1.6, 1)
    nt.links.new(tc.outputs["Generated"], mp.inputs[0])
    sub = nt.nodes.new("ShaderNodeVectorMath"); sub.operation = "SUBTRACT"; sub.inputs[1].default_value = (0.8, 0.8, 0)
    nt.links.new(mp.outputs[0], sub.inputs[0]); nt.links.new(sub.outputs[0], gr.inputs[0])
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs[0].default_value = (*lin(hex3("#e8dcff")), 1)
    gu = nt.nodes.new("ShaderNodeMath"); gu.operation = "MULTIPLY"; gu.inputs[1].default_value = 2.2
    nt.links.new(gr.outputs["Fac"], gu.inputs[0]); nt.links.new(gu.outputs[0], em.inputs[1])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], o.inputs[0])
    p.data.materials.append(m)


def gok_katmani():
    rnd = random.Random(61)
    sc = bos_sahne(w=1920, h=1080, ornek=min(ORNEK, 64))
    kamera(sc)
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (*lin(hex3("#140828")), 1)
    sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.3
    kup_kaplama(rnd)
    neon_cerceveler()
    uzak_sis()
    # tunel icini metal kuplerde parlatan isiklar: pembe/mor/camgobegi alanlar boyunca
    for yy in (4, 14, 28, 45, 70):
        isik("AREA", (-3.5, yy, T_Z + 2), 900 + yy * 20, lin(hex3(PEMBE)), 4, yon=(-T_R, yy + 4, T_Z + 3))
        isik("AREA", (3.5, yy, T_Z + 2), 900 + yy * 20, lin(hex3(CAMGOBEGI)), 4, yon=(T_R, yy + 4, T_Z + 3))
        isik("AREA", (0, yy, T_Z - 1), 700 + yy * 15, lin(hex3("#c8b4ff")), 5, yon=(0, yy + 3, T_Z + T_R))
    isik("POINT", (0, T_Y1 - 12, T_Z), 22000, lin(hex3("#e0d0ff")))
    sc.use_nodes = True
    nt2 = sc.node_tree; nt2.nodes.clear()
    rl = nt2.nodes.new("CompositorNodeRLayers")
    gl = nt2.nodes.new("CompositorNodeGlare"); gl.glare_type = "FOG_GLOW"; gl.threshold = 0.9; gl.size = 8; gl.mix = 0.2
    ou = nt2.nodes.new("CompositorNodeComposite")
    nt2.links.new(rl.outputs[0], gl.inputs[0]); nt2.links.new(gl.outputs[0], ou.inputs[0])
    yaz(sc, ON_EK + "gok.png")


# ------------------------------------------------------------------ SERIT katmani (kopru yol + korkuluk + kafes kapi)
def kopru_yol():
    yol = bpy.data.materials.new("yol"); yol.use_nodes = True
    b = yol.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*lin(hex3("#1c1238")), 1); b.inputs["Roughness"].default_value = 0.12
    b.inputs["Metallic"].default_value = 0.3
    yuvarlak_kutu("yol", (0, (0.3 + T_Y1) / 2, -0.2), (YOL_W, T_Y1 - 0.3, 0.4), yol, egim=0.05, seg=2)
    beyaz = mat_emis("chev", lin(hex3("#f6f2ff")), 4.0)
    hw = YOL_W / 2 - 0.55
    hw = 1.5
    for yy in (2.2, 3.5, 4.8, 6.1, 7.4, 8.7, 10.0):
        # REF-061: tepesi kameraya bakan beyaz V bantlar (sahne 1'de ters cizilmisti)
        sekil("chev", [(-hw, yy + 0.62), (0, yy), (hw, yy + 0.62), (hw, yy + 0.96), (0, yy + 0.34), (-hw, yy + 0.96)], beyaz, konum=(0, 0, 0.03))
    for s, c in ((-1, PEMBE), (1, CAMGOBEGI)):
        boru((s * (YOL_W / 2 - 0.08), 0.3, 0.03), (s * (YOL_W / 2 - 0.08), T_Y1, 0.03), 0.04, mat_emis("kenar%d" % s, lin(hex3(c)), 7))


def korkuluk():
    metal = mat_metal("kork_metal", lin(hex3("#d8d0ff")), 0.2)
    cam = mat_cam("kork_cam")
    for s, c in ((-1, PEMBE), (1, CAMGOBEGI)):
        x = s * (YOL_W / 2 + 0.25)
        hk = 0.9
        neon = mat_emis("kork_neon%d" % s, lin(hex3(c)), 8)
        ys = [0.6 + i * 1.8 for i in range(int((60 - 0.6) / 1.8) + 1)]
        for yy in ys:
            yuvarlak_kutu("dikme", (x, yy, hk / 2), (0.07, 0.07, hk), metal, egim=0.02, seg=2)
        yuvarlak_kutu("tirabzan", (x, (ys[0] + ys[-1]) / 2, hk + 0.02), (0.1, ys[-1] - ys[0], 0.07), metal, egim=0.03, seg=2)
        yuvarlak_kutu("cam", (x, (ys[0] + ys[-1]) / 2, hk / 2), (0.03, ys[-1] - ys[0], hk * 0.86), cam, egim=0.0, seg=1)
        for zz in (0.06, hk - 0.06):
            boru((x, ys[0], zz), (x, ys[-1], zz), 0.03, neon)
        # REF-061: korkuluk camında kameraya bakan pembe '<<<' oklar (y-z duzleminde dik sekil)
        okm = mat_emis("ok%d" % s, lin(hex3("#ff7ae6")), 5)
        for y0 in (1.2, 4.0, 7.0):
            for j in range(3):
                yy = y0 + j * 0.45
                pts = [(yy + 0.35, 0.18), (yy, 0.45), (yy + 0.35, 0.72), (yy + 0.55, 0.72), (yy + 0.2, 0.45), (yy + 0.55, 0.18)]
                me = bpy.data.meshes.new("ok"); me.from_pydata([(x - s * 0.04, a, b) for a, b in pts], [], [list(range(6))]); me.update()
                ob = bpy.data.objects.new("ok", me); bpy.context.collection.objects.link(ob); ob.data.materials.append(okm)


def kapi():
    """REF-061 gumus kafes (truss) kapi: iki kule + ust kiris, ince capraz baglar"""
    Y, W, H, KK, KR = KAP["y"], KAP["w"], KAP["h"], KAP["kule"], KAP["kiris"]
    ana = mat_metal("kapi_ana", lin(hex3("#f0ecff")), 0.18)
    ince = mat_metal("kapi_ince", lin(hex3("#cfc6f0")), 0.25)
    xk = W / 2 - KK / 2
    for s in (-1, 1):
        kafes_kule(s * xk, Y, 0.0, H + KR, KK, ana, ince)
    kafes_kiris(-xk, xk, Y, H + KR / 2, KR, ana, ince)


def serit_katmani():
    sc = bos_sahne(w=1920, h=1080, saydam=True, ornek=min(ORNEK, 64))
    kam = kamera(sc)
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (*lin(hex3("#b89cff")), 1)
    sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.35
    Y = KAP["y"]
    kopru_yol()
    korkuluk()
    kapi()
    # yol yansimasi: solda pembe, sagda camgobegi (REF-061), kapiya ust isik
    isik("AREA", (-6, 6, 2.5), 1800, lin(hex3(PEMBE)), 6, yon=(-2, 8, 0))
    isik("AREA", (6, 6, 2.5), 1800, lin(hex3(CAMGOBEGI)), 6, yon=(2, 8, 0))
    isik("AREA", (-6, 20, 2.5), 2000, lin(hex3(PEMBE)), 6, yon=(-2, 24, 0))
    isik("AREA", (6, 20, 2.5), 2000, lin(hex3(CAMGOBEGI)), 6, yon=(2, 24, 0))
    isik("AREA", (0, Y - 4, 7), 900, lin(hex3("#f0e8ff")), 4, yon=(0, Y, 2))
    W_, H_, KK = KAP["w"], KAP["h"], KAP["kule"]
    ic = W_ / 2 - KK
    bpy.context.view_layer.update()
    px = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-ic, Y, 0), (ic, Y, 0), (-ic, Y, H_), (ic, Y, H_))]
    xs = [p.x * 1920 for p in px]; ys = [(1 - p.y) * 1080 for p in px]
    YERLESIM[ON_EK + "aciklik_p1"] = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
    YERLESIM["yol"] = {"y_kapi": Y, "genislik": YOL_W, "kam": KAM, "serit_w": 1920}
    log("aciklik", YERLESIM[ON_EK + "aciklik_p1"])
    yaz(sc, ON_EK + "serit.png")


# ------------------------------------------------------------------ ana akis (tunel)
ON_EK = ""
if YALNIZ == "kapak":
    ON_EK = "kapak-"
    gok_katmani(); serit_katmani()
if YALNIZ in ("hepsi", "sahne"):
    gok_katmani()
    serit_katmani()
json.dump(YERLESIM, open(os.path.join(CIKTI, "yerlesim.json"), "w"), indent=1)
log("bitti (tunel)", YERLESIM.get("aciklik_p1"))
