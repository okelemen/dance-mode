"""TETRIS MODE 7. video (REF-058, 2 oyunculu CO-OP) - synthwave GUN BATIMI sahne varliklari, TEK genis serit.

varlik.py tarafindan calistirilir (yardimcilar oradan gelir):
    blender -b --factory-startup -noaudio -P 03-motor/tetris-pvp/varlik.py -- --mod gunbatimi --cikti cikti [--ornek 64] [--yalniz sahne]

REF-058'de ne varsa (CLAUDE.md md. 22): ufukta cizgili dev turuncu gunes, magenta -> mor gok, sehir silueti, palmiye
siluetleri, magenta izgara deniz/zemin; ortada TEK yol: parlayan turuncu-pembe chevron basamaklar, kirmizi-pembe korkuluk,
korkuluk disinda beyaz neon oklar; kirmizi kafes (truss) kapi + PLAYER 1 & PLAYER 2 tabelasi (referanstaki robot maskotlar YOK).
Duvar paneli renk gecisli: A camgobegi -> mavi, B sari -> yesil.

Ciktilar (sahne6.html 2B'de birlestirir, kamera sabit):
  gok.png        1920x1080  gok + gunes + sehir + uzak palmiyeler + izgara zemin (tam ekran, opak)
  serit.png      1920x1080  yol, chevron, korkuluk, oklar, kapi, yakin palmiyeler (gokte saydam)
  panel-a/b.png  1600x900   renk gecisli duvar paneli (grup maskesiyle ayni 16:9 oran)
  yerlesim.json  aciklik_p1 (kapi acikligi, ekran px), ampul_p1, yol
"""

YERLESIM.clear()
KAP = {"y": 12.0, "w": 7.4, "h": 3.6, "kule": 0.5, "kiris": 0.5}      # aciklik 6,4 x 3,6 = 16:9 (panel/maske orani)
YOL_W = 4.8
KIRMIZI = "#ff2d55"


KAYMA = [0.0, 0.0]          # kapak: kamera x/y kaymasi (REF-058 kapaginda kapi sagda ve daha yakin)


def kamera(sc):
    rx = math.radians(90 - KAM["egim"])
    bpy.ops.object.camera_add(location=(KAYMA[0], KAYMA[1], KAM["z"]), rotation=(rx, 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.sensor_fit = "VERTICAL"; kam.data.sensor_height = KAM["sensor"]; kam.data.lens = KAM["lens"]
    kam.data.clip_end = 600
    return kam


def mat_sis(ad, renk, guc, alfa):
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    e = nt.nodes.new("ShaderNodeEmission"); e.inputs[0].default_value = (*renk, 1); e.inputs[1].default_value = guc
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mx = nt.nodes.new("ShaderNodeMixShader"); mx.inputs[0].default_value = alfa
    nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(e.outputs[0], mx.inputs[2])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(mx.outputs[0], o.inputs[0])
    m.blend_method = "BLEND"
    return m


def mat_duz(ad, renk, purluk=0.6, emis=0.0, emis_renk=None):
    m = bpy.data.materials.new(ad); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*renk, 1); b.inputs["Roughness"].default_value = purluk
    if emis:
        b.inputs["Emission Color"].default_value = (*(emis_renk or renk), 1); b.inputs["Emission Strength"].default_value = emis
    return m


def sekil(ad, noktalar, mat, duzlem="xz", konum=(0, 0, 0)):
    """duz cokgen: xz = kameraya donuk (siluet), xy = yere yatik"""
    me = bpy.data.meshes.new(ad)
    v = [(a, 0, b) if duzlem == "xz" else (a, b, 0) for a, b in noktalar]
    me.from_pydata(v, [], [list(range(len(v)))]); me.update()
    o = bpy.data.objects.new(ad, me); bpy.context.collection.objects.link(o)
    o.location = konum; o.data.materials.append(mat)
    return o


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


# ------------------------------------------------------------------ GOK katmani
def gok_duzlemi():
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 160, 25), rotation=(math.pi / 2, 0, 0))
    p = bpy.context.active_object; p.scale = (620, 60, 1)          # dunya z -5..55; ufuk (z~2,6) Generated Y ~0,13
    m = bpy.data.materials.new("gok"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    r = ramp(nt, sep.outputs["Y"], [(0.08, "#ff6ab8"), (0.16, "#f21cc8"), (0.32, "#c40fc0"), (0.55, "#6a0a8a"), (0.9, "#22053a")])
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs[1].default_value = 1.0; nt.links.new(r.outputs[0], em.inputs[0])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], o.inputs[0])
    p.data.materials.append(m)


def gunes():
    """REF-058 gunesi: ustte sari -> turuncu -> pembe, alt yarisi yatay seritlerle kesik (aradan gok gorunur)"""
    C = Vector((0, 150, 17)); R_ = 26
    bpy.ops.mesh.primitive_circle_add(vertices=128, radius=R_, fill_type="NGON", location=C, rotation=(math.pi / 2, 0, 0))
    g = bpy.context.active_object
    m = bpy.data.materials.new("gunes"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    Y = sep.outputs["Y"]
    r = ramp(nt, Y, [(0.0, "#ff2d8a"), (0.35, "#ff5a3a"), (0.62, "#ff9a2a"), (1.0, "#ffe25a")])
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs[1].default_value = 2.4; nt.links.new(r.outputs[0], em.inputs[0])
    # serit: alt %52'de, asagi indikce kalinlasan bosluklar
    fr = math_(nt, "FRACT", math_(nt, "MULTIPLY", Y, 13.0))
    esik = math_(nt, "MULTIPLY_ADD", math_(nt, "SUBTRACT", 0.52, Y), 0.9, 0.06)
    bosluk = math_(nt, "MULTIPLY", math_(nt, "LESS_THAN", fr, esik), math_(nt, "LESS_THAN", Y, 0.52))
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mx = nt.nodes.new("ShaderNodeMixShader"); nt.links.new(bosluk, mx.inputs[0])
    nt.links.new(em.outputs[0], mx.inputs[1]); nt.links.new(tr.outputs[0], mx.inputs[2])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(mx.outputs[0], o.inputs[0])
    m.blend_method = "BLEND"
    g.data.materials.append(m)
    for rr, c, gg in ((1.12, "#ff7ab8", 0.5), (1.4, "#ff3fc8", 0.18)):
        bpy.ops.mesh.primitive_circle_add(vertices=96, radius=R_ * rr, fill_type="NGON", location=C + Vector((0, 4 * rr, 0)), rotation=(math.pi / 2, 0, 0))
        bpy.context.active_object.data.materials.append(mat_sis("gunes_hale%.2f" % rr, lin(hex3(c)), gg * 5, 0.3))
    return C, R_


def sehir(rnd):
    """ufukta sehir silueti (koyu mor kuleler, seyrek pembe/camgobegi pencere)"""
    kule = mat_duz("kule", lin(hex3("#2a0638")), 0.9, emis=0.35, emis_renk=lin(hex3("#3a0a52")))
    pen = [mat_emis("pen%d" % i, lin(hex3(c)), 6) for i, c in enumerate(("#ff7ad8", "#7fe7ff", "#ffd27a"))]
    x = -150.0
    while x < 150:
        w = rnd.uniform(3, 8); h = rnd.uniform(3, 16) * (1.3 if abs(x) > 25 else 0.8)
        y = rnd.uniform(105, 118)
        yuvarlak_kutu("kule", (x, y, h / 2 - 0.5), (w, 4, h), kule, egim=0.05, seg=1)
        for j in range(int(h / 1.6)):
            for i_ in range(int(w / 1.4)):
                if rnd.random() < 0.18:
                    yuvarlak_kutu("pen", (x - w / 2 + 0.7 + i_ * 1.4, y - 2.05, 1 + j * 1.6), (0.5, 0.1, 0.7), rnd.choice(pen), egim=0.01, seg=1)
        x += w * rnd.uniform(0.9, 1.25)


def izgara_zemin():
    """REF-058 magenta izgara deniz/zemin: koyu mor yuzey, parlak magenta cizgiler (dunya olcekli, 2 m aralik)"""
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 100, 0))
    p = bpy.context.active_object; p.scale = (700, 200, 1)
    m = bpy.data.materials.new("izgara"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Object"], sep.inputs[0])
    # Object koordinati yerel (olcek oncesi): dunya = yerel * olcek -> aralik 2 m icin carpan olcek/2
    hat = []
    for eks, olc in (("X", 700), ("Y", 200)):
        d = math_(nt, "ABSOLUTE", math_(nt, "SUBTRACT", math_(nt, "FRACT", math_(nt, "MULTIPLY", sep.outputs[eks], olc / 2.4)), 0.5))
        hat.append(math_(nt, "GREATER_THAN", d, 0.45))
    h = math_(nt, "MAXIMUM", hat[0], hat[1])
    mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"; nt.links.new(h, mx.inputs[0])
    mx.inputs[6].default_value = (*lin(hex3("#1a0430")), 1); mx.inputs[7].default_value = (*lin(hex3("#ff2fd0")), 1)
    em = nt.nodes.new("ShaderNodeEmission"); nt.links.new(mx.outputs[2], em.inputs[0])
    guc = math_(nt, "MULTIPLY_ADD", h, 3.2, 0.6); nt.links.new(guc, em.inputs[1])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], o.inputs[0])
    p.data.materials.append(m)


def yaprak(L, a, ayna):
    """palmiye yapragi: egri, uca dogru incelen, alt kenari disli duz sekil (2B), a = cikis acisi"""
    ust, alt = [], []
    for i in range(13):
        s = i / 12
        x, z = L * s, -0.42 * L * s * s
        w = 0.13 * L * math.sin(math.pi * min(1, s * 1.1)) + 0.01
        ust.append((x, z + w * 0.35)); alt.append((x + (0.04 * L if i % 2 else 0), z - w))
    pts = ust + alt[::-1]
    ca, sa = math.cos(a), math.sin(a)
    pts = [(x * ca - z * sa, x * sa + z * ca) for x, z in pts]
    return [(-x, z) for x, z in pts] if ayna else pts


def palmiye(x, y, boy, mat, rnd):
    """siluet palmiye: hafif egik govde (boru dilimleri) + 9 yaprak (kameraya donuk duz sekiller)"""
    egim = rnd.uniform(-0.12, 0.12)
    p0 = Vector((x, y, 0)); n = 6
    for i in range(n):
        a = p0 + Vector((egim * boy * (i / n) ** 1.6, 0, boy * i / n))
        b = p0 + Vector((egim * boy * ((i + 1) / n) ** 1.6, 0, boy * (i + 1) / n))
        boru(a, b, boy * (0.035 - 0.012 * i / n), mat)
    tepe = p0 + Vector((egim * boy, 0, boy))
    L = boy * rnd.uniform(0.42, 0.55)
    for j, a in enumerate((0.55, 0.2, -0.15, -0.5, 0.9)):
        for ayna in (False, True):
            if j == 4 and ayna:
                continue
            sekil("yaprak", yaprak(L * rnd.uniform(0.8, 1.05), a + rnd.uniform(-0.08, 0.08), ayna), mat, konum=tepe + Vector((0, -0.05 * j, 0)))


def gok_katmani():
    rnd = random.Random(58)
    sc = bos_sahne(w=1920, h=1080, ornek=min(ORNEK, 64))
    kamera(sc)
    sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.1
    gok_duzlemi()
    C, R_ = gunes()
    sehir(rnd)
    izgara_zemin()
    ym = mat_emis("yildiz", (1, 1, 1), 6)
    for i in range(260):
        x, z = rnd.uniform(-300, 300), rnd.uniform(24, 55)
        if (Vector((x, 0, z)) - Vector((C.x, 0, C.z))).length < R_ * 1.5:
            continue
        kure((x, 155, z), rnd.uniform(0.15, 0.4), ym)
    siyah = mat_emis("palmiye_uzak", lin(hex3("#1a0428")), 0.0)
    for s in (-1, 1):                      # uzak palmiye siralari (yolun iki yaninda, ufka dogru)
        yy = 26.0
        while yy < 95:
            palmiye(s * rnd.uniform(12 + yy * 0.25, 20 + yy * 0.55), yy, rnd.uniform(7, 11), siyah, rnd)
            yy += rnd.uniform(5, 11)
    sc.use_nodes = True
    nt2 = sc.node_tree; nt2.nodes.clear()
    rl = nt2.nodes.new("CompositorNodeRLayers")
    gl = nt2.nodes.new("CompositorNodeGlare"); gl.glare_type = "FOG_GLOW"; gl.threshold = 0.9; gl.size = 8; gl.mix = 0.15
    ou = nt2.nodes.new("CompositorNodeComposite")
    nt2.links.new(rl.outputs[0], gl.inputs[0]); nt2.links.new(gl.outputs[0], ou.inputs[0])
    yaz(sc, ON_EK + "gok.png")


# ------------------------------------------------------------------ SERIT katmani (tek genis yol + kapi)
def chevron_yol(Y):
    yol = mat_duz("yol", lin(hex3("#2a0634")), 0.28, emis=0.05, emis_renk=lin(hex3("#4a0a5a")))
    yuvarlak_kutu("yol", (0, (0.3 + Y + 1.5) / 2, -0.2), (YOL_W, Y + 1.5 - 0.3, 0.4), yol, egim=0.1)
    ca = mat_emis("chev_a", lin(hex3("#ff9a3a")), 5.0)
    cb = mat_emis("chev_b", lin(hex3("#ff3f9a")), 4.6)
    adim, hw = 1.25, YOL_W / 2 - 0.25
    yy, j = 0.8, 0
    while yy < Y - 0.9:
        # tek parca V bant, tepe kameraya bakar (REF-058). Deneme 1: iki donuk kutu -> kollardan biri gorunmedi
        sekil("chev", [(-hw, yy + 0.75), (0, yy), (hw, yy + 0.75), (hw, yy + 1.09), (0, yy + 0.34), (-hw, yy + 1.09)],
              ca if j % 2 == 0 else cb, duzlem="xy", konum=(0, 0, 0.03))
        yy += adim; j += 1
    kenar = mat_emis("kenar", lin(hex3("#ff5ac8")), 6.0)
    for s in (-1, 1):
        boru((s * (YOL_W / 2 - 0.06), 0.3, 0.03), (s * (YOL_W / 2 - 0.06), Y + 1.4, 0.03), 0.05, kenar)


def korkuluk(Y):
    ana = mat_jole("kork", lin(hex3(KIRMIZI)), emis=0.22, purluk=0.2)
    acikm = mat_jole("kork_acik", acik(lin(hex3(KIRMIZI)), 0.4), emis=0.35, purluk=0.15)
    for s in (-1, 1):
        x = s * (YOL_W / 2 + 0.3)
        ys = [0.8 + i * 1.5 for i in range(int((Y - 0.8) / 1.5) + 1)]
        for yy in ys:
            yuvarlak_kutu("baba", (x, yy, 0.38), (0.3, 0.3, 0.76), ana, egim=0.05)
            yuvarlak_kutu("baslik", (x, yy, 0.8), (0.38, 0.38, 0.1), acikm, egim=0.03)
        for zz, kal in ((0.7, 0.14), (0.38, 0.1)):
            yuvarlak_kutu("tirabzan", (x, (ys[0] + ys[-1]) / 2, zz), (kal, ys[-1] - ys[0], kal), acikm if zz > 0.5 else ana, egim=0.03)


def yan_oklar():
    """REF-058: korkuluklarin disinda yere yatik beyaz neon cift oklar (kameraya dogru)"""
    m = mat_emis("ok", lin(hex3("#fff0fa")), 7.0)
    for s in (-1, 1):
        for y0 in (3.2, 6.0, 9.0):
            for j in range(2):
                yy = y0 + j * 0.55; x0 = s * (YOL_W / 2 + 2.0 + y0 * 0.12)
                pts = [(-0.7, 0.5), (0, 0), (0.7, 0.5), (0.7, 0.78), (0, 0.28), (-0.7, 0.78)]
                sekil("ok", [(x0 + px, yy + py) for px, py in pts], m, duzlem="xy", konum=(0, 0, 0.03))


def kapi():
    """REF-058 kirmizi kafes kapisi (yapi ayni) + PLAYER 1 & PLAYER 2 tabelasi, ampul dizisi, kose yildizlari, neon tup"""
    Y, W, H, KK, KR = KAP["y"], KAP["w"], KAP["h"], KAP["kule"], KAP["kiris"]
    R = lin(hex3("#e8203c"))
    ana = mat_jole("kapi_ana", R, emis=0.25, purluk=0.15)
    ince = mat_jole("kapi_ince", acik(R, 0.3), emis=0.35, purluk=0.15)
    koyum = mat_jole("kapi_koyu", lin(hex3("#3a0630")), emis=0.03)
    xk = W / 2 - KK / 2
    for s in (-1, 1):
        kafes_kule(s * xk, Y, 0.0, H + KR, KK, ana, ince)
        yuvarlak_kutu("taban", (s * xk, Y, 0.14), (KK + 0.35, KK + 0.35, 0.28), koyum, egim=0.06)
        for zz in (H, H + KR):
            yuvarlak_kutu("dugum", (s * xk, Y, zz), (KK * 0.55, KK * 0.55, KK * 0.55), ince, egim=0.08)
    kafes_kiris(-xk, xk, Y, H + KR / 2, KR, ana, ince)
    ic = W / 2 - KK
    neon = mat_emis("neon", lin(hex3("#ff6ad5")), 9.0)
    for a, b in (((-ic + 0.1, Y - 0.3, 0.05), (-ic + 0.1, Y - 0.3, H - 0.1)), ((ic - 0.1, Y - 0.3, 0.05), (ic - 0.1, Y - 0.3, H - 0.1)),
                 ((-ic + 0.1, Y - 0.3, H - 0.1), (ic - 0.1, Y - 0.3, H - 0.1))):
        boru(a, b, 0.05, neon)
    amp = mat_emis("ampul", lin(hex3("#ffe0b0")), 2.5)
    AMPUL = [Vector((-ic + 0.25 + i * (2 * ic - 0.5) / 16, Y - KK / 2 + 0.05, H - 0.06)) for i in range(17)]
    for s_ in (-1, 1):
        AMPUL += [Vector((s_ * xk, Y - KK / 2 - 0.05, 0.35 + j * (H - 0.45) / 9)) for j in range(10)]
    for q in AMPUL:
        kure(q, 0.075, amp)
    # tabela: kirisin onunde (kadraj ustu siniri), iki oyuncu birlikte -> "PLAYER 1 & PLAYER 2"
    yuvarlak_kutu("tabela", (0, Y - KK / 2 - 0.2, H + KR / 2), (3.6, 0.14, 0.56), koyum, egim=0.14, seg=6)
    yuvarlak_kutu("tabela_cerceve", (0, Y - KK / 2 - 0.14, H + KR / 2), (3.8, 0.12, 0.68), ince, egim=0.18, seg=6)
    try:
        font = bpy.data.fonts.load(os.path.join(KOK, "05-kapak/fontlar/TitanOne.ttf"))
        bpy.ops.object.text_add(location=(0, Y - KK / 2 - 0.29, H + KR / 2 - 0.02), rotation=(math.pi / 2, 0, 0))
        tx = bpy.context.active_object
        tx.data.body = "PLAYER 1 & PLAYER 2"; tx.data.font = font; tx.data.size = 0.34; tx.data.extrude = 0.04; tx.data.bevel_depth = 0.012
        tx.data.align_x = "CENTER"; tx.data.align_y = "CENTER"
        tx.data.materials.append(mat_emis("tabela_yazi", (1, 1, 1), 3.5))
    except Exception as e:
        log("tabela yazisi atlandi:", e)
    yildiz_m = mat_jole("yildiz", lin(hex3("#ffd23a")), emis=0.25)
    for s_ in (-1, 1):
        bpy.ops.mesh.primitive_circle_add(vertices=10, radius=0.4, fill_type="NGON", location=(s_ * xk, Y - KK / 2 - 0.15, H + KR + 0.25), rotation=(math.pi / 2, 0, 0))
        yo = bpy.context.active_object
        for i, v in enumerate(yo.data.vertices):
            if i % 2:
                v.co *= 0.45
        so = yo.modifiers.new("kal", "SOLIDIFY"); so.thickness = 0.22; so.offset = 0
        yo.data.materials.append(yildiz_m)
    yuvarlak_kutu("kaide", (0, Y - 0.55, 0.06), (W + 0.4, 0.7, 0.16), koyum, egim=0.06)
    boru((-W / 2 - 0.1, Y - 0.92, 0.12), (W / 2 + 0.1, Y - 0.92, 0.12), 0.035, neon)
    return AMPUL


def serit_katmani():
    rnd = random.Random(59)
    sc = bos_sahne(w=1920, h=1080, saydam=True, ornek=min(ORNEK, 64))
    kam = kamera(sc)
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (*lin(hex3("#ff4fb8")), 1)
    sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.25
    Y = KAP["y"]
    chevron_yol(Y)
    korkuluk(Y)
    yan_oklar()
    AMPUL = kapi()
    siyah = mat_emis("palmiye_yakin", lin(hex3("#14021f")), 0.0)
    for s in (-1, 1):                      # yakin palmiyeler: kapinin iki yaninda, kadrajin kenarinda
        for (dx, yy, b) in ((7.5, 16, 8.5), (10.5, 22, 9.5), (12.5, 30, 8.0)):
            palmiye(s * (dx + rnd.uniform(-0.6, 0.6)), yy + rnd.uniform(-1, 1), b * rnd.uniform(0.9, 1.1), siyah, rnd)
    isik("AREA", (0, -1.5, 6.5), 380, lin(hex3("#ffd6ee")), 6, yon=(0, Y * 0.6, 0))
    isik("AREA", (-4, 3, 3), 260, lin(hex3("#ff6ad5")), 3, yon=(0, Y, 2))
    isik("AREA", (4, 3, 3), 220, lin(hex3("#ffb45a")), 3, yon=(0, Y, 2))
    isik("AREA", (0, Y + 3, 6), 500, lin(hex3("#ff8ac8")), 5, yon=(0, Y, 1))
    W_, H_, KK = KAP["w"], KAP["h"], KAP["kule"]
    ic = W_ / 2 - KK
    bpy.context.view_layer.update()
    px = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-ic, Y, 0), (ic, Y, 0), (-ic, Y, H_), (ic, Y, H_))]
    xs = [p.x * 1920 for p in px]; ys = [(1 - p.y) * 1080 for p in px]
    YERLESIM[ON_EK + "aciklik_p1"] = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
    YERLESIM["ampul_p1"] = [[round(p.x * 1920, 1), round((1 - p.y) * 1080, 1)] for p in (world_to_camera_view(sc, kam, q) for q in AMPUL)]
    YERLESIM["yol"] = {"y_kapi": Y, "genislik": YOL_W, "kam": KAM, "serit_w": 1920}
    log("aciklik", YERLESIM[ON_EK + "aciklik_p1"])
    yaz(sc, ON_EK + "serit.png")


# ------------------------------------------------------------------ PANELLER (REF-058: renk gecisli, 16:9)
PANEL_RENK = {"a": ("#2af0e0", "#2a6bff"), "b": ("#fff23a", "#6dff3a")}


def panel_gunbatimi(tip):
    sc = bos_sahne(w=1600, h=900, saydam=True, ornek=min(ORNEK, 32))
    A, B = (lin(hex3(c)) for c in PANEL_RENK[tip])
    PW, PH = 5.0, 5.0 * 9 / 16
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    p = bpy.context.active_object; p.scale = (PW, 0.2, PH); bpy.ops.object.transform_apply(scale=True)
    bv = p.modifiers.new("egim", "BEVEL"); bv.width = 0.08; bv.segments = 6; bv.limit_method = "NONE"
    m = bpy.data.materials.new("panel"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sp = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Generated"], sp.inputs[0])
    t2 = math_(nt, "MULTIPLY", math_(nt, "MULTIPLY_ADD", sp.outputs["X"], 0.7, sp.outputs["Z"]), 0.6)
    r = ramp(nt, t2, [(0.05, PANEL_RENK[tip][0]), (0.95, PANEL_RENK[tip][1])])
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 300; nz.inputs["Detail"].default_value = 2
    nt.links.new(tc.outputs["Generated"], nz.inputs["Vector"])
    mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"; mx.blend_type = "OVERLAY"; mx.inputs[0].default_value = 0.12
    nt.links.new(r.outputs[0], mx.inputs[6]); nt.links.new(nz.outputs["Fac"], mx.inputs[7])
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs[1].default_value = 1.0; nt.links.new(mx.outputs[2], em.inputs[0])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], o.inputs[0])
    p.data.materials.append(m)
    bpy.ops.object.camera_add(location=(0, -10, 0), rotation=(math.radians(90), 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.type = "ORTHO"; kam.data.ortho_scale = PW + 0.04
    yaz(sc, "panel-%s.png" % tip)


# ------------------------------------------------------------------ ana akis (gunbatimi)
ON_EK = ""
if YALNIZ == "kapak":       # REF-058 kapagi: kapi kadrajin sag-ortasinda (x ~%62) ve biraz daha buyuk -> kamera sola + one kayar
    ON_EK = "kapak-"; KAYMA[0], KAYMA[1] = -2.35, 1.5
    gok_katmani(); serit_katmani()
if YALNIZ in ("hepsi", "sahne"):
    gok_katmani()
    serit_katmani()
    for t_ in PANEL_RENK:
        panel_gunbatimi(t_)
json.dump(YERLESIM, open(os.path.join(CIKTI, "yerlesim.json"), "w"), indent=1)
log("bitti (gunbatimi)", YERLESIM.get("aciklik_p1"))
