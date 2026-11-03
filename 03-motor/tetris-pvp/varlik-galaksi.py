"""HUMAN TETRIS 17. video (REF-068 TetrisBounce, SOLO) - SYNTHWAVE GALAKSI IZGARASI sahne varliklari, TEK serit. varlik.py calistirir (--mod galaksi).

REF-068'de ne varsa (md. 22): bastan basa galaksi/bulutsu gogu (lacivert taban, mor-mavi bulutsu, camgobegi ve pembe parlamalar, yildiz tozu),
ufuktan kameraya uzanan koyu lacivert zeminde camgobegi-mavi-mor neon izgara, ufukta parlak cizgi, ortada gumus metal truss (kafes) kapi.
Kopru, korkuluk, chevron, sehir YOK. Pembe-sari duvar, START! karti, 3-2-1, "!", ovgu yazilari, MISSIONS ve maskot motorda.

Ciktilar:
  gok.png     1920x1080  bulutsu gok + izgara zemin (opak)
  serit.png   1920x1080  yalniz truss kapi (saydam)
  yerlesim.json  aciklik_p1 (kapinin ic acikligi, piksel) + kamera
Kapak (--yalniz kapak): ayni katmanlar "kapak-" on ekiyle; REF-068 kapaginda kapi buyuk ve saga kacik, ufuk daha asagida.
"""

YERLESIM.clear()
KAPAK = YALNIZ == "kapak"
POZLAMA = float(arg("--kapak-pozlama", "0"))
# video (sahne 1 dersi, REF-068 karesiyle yan yana): kapi genisligin ~%32'si (x %34-66, y %34-65), ufuk ~%60, kapi tabani ufkun hemen altinda.
# Ufuk kamerayi egerek degil lens kaydirmayla asagi alinir (shift_y): izgaranin boyuna cizgileri referanstaki gibi ufukta tek noktada birlesir.
KAP = {"y": 9.5, "w": 7.2, "h": 3.9, "kule": 0.42, "kiris": 0.42, "x": 0.0}
KAM = {"x": 0.0, "z": 0.9, "egim": 0.0, "lens": 18.0, "sensor": 24.0, "kaydir": 0.056}   # sahne 2: z 0,65 yakin izgarayi kalinlastiriyordu
if KAPAK:
    # REF-068 kapagi: kapi x %40-78, ust %33, alt %68 -> yakin ve saga kacik, ufuk ~%62
    # kapak 1: kapi genisligin %47'si (ref %38), ufuk %55 (ref %62), zemin fazla siyah (siyah oran 0,21, ref 0,085)
    KAP.update({"y": 9.3, "x": 2.7})
    KAM.update({"z": 0.8, "kaydir": 0.10})
IZ_YAKIN = "#22c8c0"    # ufka yakin enine cizgiler camgobegi
IZ_UZUN = "#3a2ee8"     # boyuna cizgiler mavi-mor
ZEMIN = "#16124a" if KAPAK else "#05061c"


def kamera(sc):
    rx = math.radians(90 - KAM["egim"])
    bpy.ops.object.camera_add(location=(KAM["x"], 0, KAM["z"]), rotation=(rx, 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.sensor_fit = "VERTICAL"; kam.data.sensor_height = KAM["sensor"]; kam.data.lens = KAM["lens"]
    kam.data.clip_end = 900
    kam.data.shift_y = KAM.get("kaydir", 0.0)
    return kam


def ramp(nt, girdi, duraklar):
    r = nt.nodes.new("ShaderNodeValToRGB"); cr = r.color_ramp
    cr.elements[0].position, cr.elements[0].color = duraklar[0][0], (*lin(hex3(duraklar[0][1])), 1)
    cr.elements[1].position, cr.elements[1].color = duraklar[-1][0], (*lin(hex3(duraklar[-1][1])), 1)
    for p, c in duraklar[1:-1]:
        e = cr.elements.new(p); e.color = (*lin(hex3(c)), 1)
    nt.links.new(girdi, r.inputs[0])
    return r


def math_(nt, op, *girdi):
    m = nt.nodes.new("ShaderNodeMath"); m.operation = op
    for i, x in enumerate(girdi):
        if x is None:
            continue
        if isinstance(x, (int, float)):
            m.inputs[i].default_value = x
        else:
            nt.links.new(x, m.inputs[i])
    return m.outputs[0]


def mix_renk(nt, fak, a, b, tip="MIX"):
    mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"; mx.blend_type = tip
    if isinstance(fak, (int, float)):
        mx.inputs[0].default_value = fak
    else:
        nt.links.new(fak, mx.inputs[0])
    for yuva, x in ((6, a), (7, b)):
        if isinstance(x, str):
            mx.inputs[yuva].default_value = (*lin(hex3(x)), 1)
        else:
            nt.links.new(x, mx.inputs[yuva])
    return mx.outputs[2]


# ------------------------------------------------------------------ GOK katmani = bulutsu + yildiz + izgara zemin
def bulutsu_gok():
    """REF-068 gogu: lacivert taban, iki katman gurultu -> mor/mavi bulutsu kollari, camgobegi ve pembe parlamalar, yildiz tozu"""
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 300, 140), rotation=(math.pi / 2, 0, 0))
    p = bpy.context.active_object; p.scale = (1100, 340, 1)   # sahne 2: ustte siyah bant kaliyordu (lens kaydirma)
    m = bpy.data.materials.new("bulutsu"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord")
    map_ = nt.nodes.new("ShaderNodeMapping"); map_.inputs["Scale"].default_value = (3.2, 1.0, 1.0)   # duzlem 1100x260: gurultuyu yuvarlak tut
    nt.links.new(tc.outputs["Generated"], map_.inputs[0])
    n1 = nt.nodes.new("ShaderNodeTexNoise"); n1.inputs["Scale"].default_value = 2.2; n1.inputs["Detail"].default_value = 9
    n1.inputs["Roughness"].default_value = 0.62; n1.inputs["Distortion"].default_value = 0.6
    nt.links.new(map_.outputs[0], n1.inputs["Vector"])
    n2 = nt.nodes.new("ShaderNodeTexNoise"); n2.inputs["Scale"].default_value = 5.5; n2.inputs["Detail"].default_value = 6
    n2.inputs["Roughness"].default_value = 0.55
    nt.links.new(map_.outputs[0], n2.inputs["Vector"])
    # sahne 1: gok bastan basa bulut gibiydi; REF-068'de taban koyu lacivert, bulutsu yer yer, yildiz cok
    renk = ramp(nt, n1.outputs["Fac"], [(0.34, "#060828"), (0.46, "#14207a"), (0.55, "#3236c0"), (0.63, "#7a3ee0"),
                                         (0.71, "#c45cf0"), (0.78, "#ff8ae0")])   # sahne 2: gok referanstan koyu ve camurluydu
    vurgu = ramp(nt, n2.outputs["Fac"], [(0.52, "#000000"), (0.64, "#1a62c8"), (0.78, "#52c8ff")])   # mavi-camgobegi parlamalar
    karisim = mix_renk(nt, 0.5, renk.outputs[0], vurgu.outputs[0], "SCREEN")
    # yildiz tozu: kucuk voronoi noktalari, iki olcek
    yildiz = None
    for olc, esik in ((320.0, 0.06), (120.0, 0.05), (45.0, 0.035)):
        v = nt.nodes.new("ShaderNodeTexVoronoi"); v.inputs["Scale"].default_value = olc; v.inputs["Randomness"].default_value = 1.0
        nt.links.new(map_.outputs[0], v.inputs["Vector"])
        nokta = math_(nt, "LESS_THAN", v.outputs["Distance"], esik)
        yildiz = nokta if yildiz is None else math_(nt, "MAXIMUM", yildiz, nokta)
    son = mix_renk(nt, yildiz, karisim, "#ffffff")
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs[1].default_value = 1.35; nt.links.new(son, em.inputs[0])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], o.inputs[0])
    p.data.materials.append(m)


def izgara_zemin():
    """REF-068 zemini: koyu lacivert, enine cizgiler camgobegi, boyuna cizgiler mavi-mor (dunya olcekli, 2,4 m aralik); ufukta parlak cizgi"""
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 150, 0))
    p = bpy.context.active_object; p.scale = (900, 300, 1)
    m = bpy.data.materials.new("izgara"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Object"], sep.inputs[0])
    hat = {}
    for eks, olc in (("X", 900), ("Y", 300)):   # sahne 2: 1,6 m hucre, cizgi hucrenin ~%3'u
        d = math_(nt, "ABSOLUTE", math_(nt, "SUBTRACT", math_(nt, "FRACT", math_(nt, "MULTIPLY", sep.outputs[eks], olc / 1.6)), 0.5))
        hat[eks] = math_(nt, "GREATER_THAN", d, 0.484)   # sahne 1-2: cizgiler kalin
    r = mix_renk(nt, hat["Y"], ZEMIN, IZ_YAKIN)          # enine (sabit Y) cizgiler
    r = mix_renk(nt, hat["X"], r, IZ_UZUN)               # boyuna (sabit X) cizgiler
    em = nt.nodes.new("ShaderNodeEmission"); nt.links.new(r, em.inputs[0])
    h = math_(nt, "MAXIMUM", hat["X"], hat["Y"])
    nt.links.new(math_(nt, "MULTIPLY_ADD", h, 2.6, 0.35), em.inputs[1])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], o.inputs[0])
    p.data.materials.append(m)
    # ufuk parlamasi: uzakta ince camgobegi-pembe serit
    boru((-900, 290, 0.2), (900, 290, 0.2), 1.6, mat_emis("ufuk", lin(hex3("#7fe8ff")), 2.2))


def gok_katmani():
    sc = bos_sahne(w=1920, h=1080, ornek=min(ORNEK, 48))
    if KAPAK:
        sc.view_settings.exposure = POZLAMA
    kamera(sc)
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (*lin(hex3("#05061a")), 1)
    sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.3
    bulutsu_gok(); izgara_zemin()
    sc.use_nodes = True
    nt2 = sc.node_tree; nt2.nodes.clear()
    rl = nt2.nodes.new("CompositorNodeRLayers")
    gl = nt2.nodes.new("CompositorNodeGlare"); gl.glare_type = "FOG_GLOW"; gl.threshold = 0.85; gl.size = 7; gl.mix = 0.2
    ou = nt2.nodes.new("CompositorNodeComposite")
    nt2.links.new(rl.outputs[0], gl.inputs[0]); nt2.links.new(gl.outputs[0], ou.inputs[0])
    yaz(sc, ON_EK + "gok.png")


# ------------------------------------------------------------------ SERIT katmani = yalniz truss kapi
def mat_metal(ad, renk, purluk=0.28):
    m = bpy.data.materials.new(ad); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*lin(hex3(renk)), 1); b.inputs["Metallic"].default_value = 0.9
    b.inputs["Roughness"].default_value = purluk
    b.inputs["Emission Color"].default_value = (*lin(hex3("#c8d4f0")), 1); b.inputs["Emission Strength"].default_value = 0.12
    return m


def kapi():
    Y, X, W_, H_, KK, KR = KAP["y"], KAP["x"], KAP["w"], KAP["h"], KAP["kule"], KAP["kiris"]
    ana = mat_metal("kapi_ana", "#d8dde8"); ince = mat_metal("kapi_ince", "#aeb6c6", 0.35)
    xk = W_ / 2 - KK / 2
    for s in (-1, 1):
        kafes_kule(X + s * xk, Y, 0.0, H_ + KR, KK, ana, ince)
        yuvarlak_kutu("ayak", (X + s * xk, Y, 0.06), (KK * 1.5, KK * 1.5, 0.12), ana, egim=0.02, seg=2)
    kafes_kiris(X - xk, X + xk, Y, H_ + KR / 2, KR, ana, ince)


def serit_katmani():
    sc = bos_sahne(w=1920, h=1080, saydam=True, ornek=min(ORNEK, 64))
    if KAPAK:
        sc.view_settings.exposure = POZLAMA
    kam = kamera(sc)
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (*lin(hex3("#8a7adf")), 1)   # metal mor-mavi gok yansitir
    sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.6
    kapi()
    isik("AREA", (KAP["x"], KAP["y"] - 6, 6), 260, lin(hex3("#e8eeff")), 8, yon=(0, 6, -2))
    isik("AREA", (KAP["x"], KAP["y"] + 4, 1), 120, lin(hex3("#3fe6ff")), 10, yon=(0, -4, 1))      # arkadan camgobegi kenar isigi
    Y, X, W_, H_, KK = KAP["y"], KAP["x"], KAP["w"], KAP["h"], KAP["kule"]
    ic = W_ / 2 - KK
    bpy.context.view_layer.update()
    px = [world_to_camera_view(sc, kam, Vector(p)) for p in ((X - ic, Y, 0), (X + ic, Y, 0), (X - ic, Y, H_), (X + ic, Y, H_))]
    xs = [p.x * 1920 for p in px]; ys = [(1 - p.y) * 1080 for p in px]
    YERLESIM[ON_EK + "aciklik_p1"] = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
    YERLESIM[ON_EK + "yol"] = {"y_kapi": Y, "x_kapi": X, "kam": KAM, "serit_w": 1920}
    log("aciklik", YERLESIM[ON_EK + "aciklik_p1"])
    yaz(sc, ON_EK + "serit.png")


ON_EK = ""
if YALNIZ in ("hepsi", "poz"):
    poz_maskeleri()
if YALNIZ == "kapak":
    ON_EK = "kapak-"
    gok_katmani(); serit_katmani()
if YALNIZ in ("hepsi", "sahne"):
    gok_katmani(); serit_katmani()
json.dump(YERLESIM, open(os.path.join(CIKTI, "yerlesim.json"), "w"), indent=1)
log("bitti (galaksi)", YERLESIM.get(ON_EK + "aciklik_p1"))
