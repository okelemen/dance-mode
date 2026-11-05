"""HUMAN TETRIS 18. video (REF-069 TetrisBounce, 2 oyuncu cift / CO-OP) - NEON YILDIZ SAHNESI varliklari, TEK serit. varlik.py calistirir (--mod yildizsahne).

REF-069'da ne varsa (md. 22): yildizli lacivert-mor gece gogu (cok renkli kare yildizlar, arti isiltilar), sag ustte ve solda camgobegi sarmal bulutlar,
ufukta lila-pembe bulut kumesi; kameraya dogru basamak basamak inen, ucu kameraya bakan (chevron) neon sahne katlari: ust yuzey koyu mavi,
kenarda pembe + camgobegi neon cizgi, uzerinde sari/pembe/camgobegi yildizlar; iki yanda kalin mavi direkli korkuluk (direk tepesinde sari yildiz,
pembe + camgobegi boru, yildizli pano); ortada mavi-pembe cerceveli kapi, ust koselerde sari kubbe lamba, tepede yildizli tac.
Alinmaz (telif): semsiyeli anime kiz maskot, kanatli sari yaratik. Kapi ekranindaki sonuk neon cift tabelasi, damali duvar karti, 3-2-1, level etiketi,
ilerleme cubugu ve kendi maskotumuz motorda / kapak betiginde.

Ciktilar:
  gok.png     1920x1080  gece gogu + sarmal bulutlar + ufuk bulutlari (opak)
  serit.png   1920x1080  sahne katlari + korkuluk + kapi (saydam)
  yerlesim.json  aciklik_p1 (kapinin ic acikligi, piksel) + kamera
Kapak (--yalniz kapak): ayni katmanlar "kapak-" on ekiyle; REF-069 kapaginda kapi buyuk ve saga kacik, direkler on planda.
"""

import random
import bmesh
YERLESIM.clear()
KAPAK = YALNIZ == "kapak"
POZLAMA = float(arg("--kapak-pozlama", "0"))
ON_EK = "kapak-" if KAPAK else ""
# REF-069 karesi (1280x720): kapi x %35-65, ust %32, alt %62; ufuk (korkuluk ucu) ~%55; katlar kapidan kameraya iner, en yakin kat alt kenari tasar.
KAP = {"y": 11.0, "x": 0.0, "w": 5.6, "h": 3.4, "z": 1.05, "kalin": 0.42}
KATLAR = [  # (on uc y, arka y, yari genislik, ust z) - kapidan kameraya
    (8.6, 11.6, 3.0, 1.05),
    (6.0, 8.6, 3.9, 0.70),
    (3.2, 6.0, 4.8, 0.35),
    (-0.5, 3.2, 5.8, 0.0),
]
KORK_X = 6.3          # korkuluk cizgisi
KAM = {"x": 0.0, "y": -2.6, "z": 3.3, "egim": 11.0, "lens": 17.0, "sensor": 24.0, "kaydir": 0.0}
if KAPAK:   # REF-069 kapagi: kapi x %38-73 (saga kacik), ust %28, alt %65; sol ve sag on planda dev yildizli direk
    KAM.update({"x": -1.9, "y": 3.4, "z": 2.6, "egim": 6.0, "lens": 16.0})   # kapak 1: x -1,3 / y 1,2 kapi x %44-66
MAVI, MAVI_K, PEMBE, CAMG, SARI = "#2f6cff", "#1a2fb8", "#ff3fd0", "#3fe8ff", "#ffd83a"


def kamera(sc):
    rx = math.radians(90 - KAM["egim"])
    bpy.ops.object.camera_add(location=(KAM["x"], KAM["y"], KAM["z"]), rotation=(rx, 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.sensor_fit = "VERTICAL"; kam.data.sensor_height = KAM["sensor"]; kam.data.lens = KAM["lens"]
    kam.data.clip_end = 900; kam.data.shift_y = KAM["kaydir"]
    return kam


def parlat(sc, esik=1.0, boy=7, mix=0.12, saydam=False):
    sc.use_nodes = True; sc.render.use_compositing = True; nt = sc.node_tree; nt.nodes.clear()
    rl = nt.nodes.new("CompositorNodeRLayers"); g = nt.nodes.new("CompositorNodeGlare"); o = nt.nodes.new("CompositorNodeComposite")
    g.glare_type = "FOG_GLOW"; g.quality = "HIGH"; g.threshold = esik; g.size = boy; g.mix = mix
    nt.links.new(rl.outputs["Image"], g.inputs[0]); nt.links.new(g.outputs[0], o.inputs[0])
    if saydam:
        nt.links.new(rl.outputs["Alpha"], o.inputs[1])


def mat_parlak(ad, renk, emis=0.35, purluk=0.18):
    """REF-069 sahne yuzeyleri: doygun renkli parlak plastik + kendi renginde isilti (karanlik sahnede rengi kaybolmasin)"""
    m = mat_jole(ad, lin(hex3(renk)), emis=emis, purluk=purluk)
    m.node_tree.nodes["Principled BSDF"].inputs["Emission Color"].default_value = (*lin(hex3(renk)), 1)
    return m


def yildiz(ad, konum, r, mat, kalin=0.12, yatik=False, aci=0.0, ic=0.45):
    """5 koseli yildiz prizmasi, yumusak kenar (REF-069 direk tepeleri, katlarin ustundeki yildizlar, kapi taci)"""
    me = bpy.data.meshes.new(ad); bm = bmesh.new()
    vs = []
    for i in range(10):
        t = math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * ic
        vs.append(bm.verts.new((math.cos(t) * rr, math.sin(t) * rr, 0)))
    yuz = bm.faces.new(vs)
    ex = bmesh.ops.extrude_face_region(bm, geom=[yuz])
    for v in [e for e in ex["geom"] if isinstance(e, bmesh.types.BMVert)]:
        v.co.z += kalin
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(ad, me); bpy.context.collection.objects.link(o)
    o.location = konum
    o.rotation_euler = (0, 0, aci) if yatik else (math.pi / 2, aci, 0)
    bv = o.modifiers.new("egim", "BEVEL"); bv.width = kalin * 0.35; bv.segments = 3; bv.limit_method = "NONE"
    o.data.materials.append(mat)
    return o


def cokgen(ad, noktalar, z0, z1, mat):
    """duz tabanli prizma (chevron kat)"""
    me = bpy.data.meshes.new(ad); bm = bmesh.new()
    alt = [bm.verts.new((x, y, z0)) for x, y in noktalar]
    yuz = bm.faces.new(alt)
    ex = bmesh.ops.extrude_face_region(bm, geom=[yuz])
    for v in [e for e in ex["geom"] if isinstance(e, bmesh.types.BMVert)]:
        v.co.z = z1
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(ad, me); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat)
    return o


# ------------------------------------------------------------------ GOK: ortografik; x -960..960, z 0..1080
def sarmal(cx, cz, r0, tur, kalin, mat, ic_mat, yon=1, y=0):
    """camgobegi sarmal bulut: arsimet sarmali boyunca kalin boru + ince acik ic cizgi (REF-069 piksel bulutlari)"""
    # kapak 1: kisa boru parcalari donuslerde disli gibi okunuyordu -> tek egri (bevel), yaricap uca dogru incelir
    n = int(tur * 60)
    for dy, olc, m in ((0, 1.0, mat), (-4, 0.3, ic_mat)):
        cu = bpy.data.curves.new("sarmal", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = kalin * olc; cu.bevel_resolution = 4
        sp = cu.splines.new("POLY"); sp.points.add(n)
        for i in range(n + 1):
            t = i / n * tur * 2 * math.pi; rr = r0 * (1 - i / n * 0.82)
            sp.points[i].co = (cx + yon * math.cos(t) * rr, y + dy, cz + math.sin(t) * rr, 1)
            sp.points[i].radius = 1 - i / n * 0.5
        o = bpy.data.objects.new("sarmal", cu); bpy.context.collection.objects.link(o); o.data.materials.append(m)


def gok_katmani():
    sc = bos_sahne(w=1920, h=1080, ornek=min(ORNEK, 16))
    bpy.ops.object.camera_add(location=(0, -900, 540), rotation=(math.radians(90), 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.type = "ORTHO"; kam.data.ortho_scale = 1920; kam.data.clip_end = 3000
    zem = bpy.data.materials.new("gok"); zem.use_nodes = True; nt = zem.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord"); sp = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Generated"], sp.inputs[0])
    rp = nt.nodes.new("ShaderNodeValToRGB"); cr = rp.color_ramp; nt.links.new(sp.outputs["Y"], rp.inputs[0])
    cr.elements[0].position = 0.30; cr.elements[0].color = (*lin(hex3("#3a1aa8")), 1)     # ufka dogru mor
    cr.elements[1].position = 0.95; cr.elements[1].color = (*lin(hex3("#0c0a48")), 1)     # tepede koyu lacivert
    em = nt.nodes.new("ShaderNodeEmission"); nt.links.new(rp.outputs[0], em.inputs[0])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], o.inputs[0])
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 600, 540), rotation=(math.radians(90), 0, 0))
    p = bpy.context.active_object; p.scale = (2000, 1100, 1); bpy.ops.object.transform_apply(scale=True)
    p.data.materials.append(zem)
    rnd = random.Random(69)
    # yildizlar: kare (piksel) noktalar, cok renkli; buyukleri arti isiltili
    renkler = [mat_emis("yz%d" % i, lin(hex3(c)), 3.2) for i, c in enumerate(("#ffffff", "#ff7ae0", "#7af0ff", "#ffe56a", "#b98cff"))]
    for _ in range(420):
        x, z = rnd.uniform(-960, 960), rnd.uniform(380, 1080)
        b = rnd.choice((3, 3, 4, 5, 6))
        yuvarlak_kutu("yz", (x, 300, z), (b, 1, b), rnd.choice(renkler), egim=0.0, seg=1)
    for _ in range(46):
        x, z = rnd.uniform(-960, 960), rnd.uniform(420, 1070); L = rnd.uniform(14, 30); m = rnd.choice(renkler)
        yuvarlak_kutu("isilti_y", (x, 280, z), (3, 1, L), m, egim=0.0, seg=1)
        yuvarlak_kutu("isilti_x", (x, 280, z), (L, 1, 3), m, egim=0.0, seg=1)
    for _ in range(14):   # kucuk 5 koseli yildizlar (pembe / sari)
        yildiz("gyz", (rnd.uniform(-940, 940), 260, rnd.uniform(450, 1050)), rnd.uniform(10, 18), rnd.choice(renkler[1:4]), kalin=2)
    # sarmal bulutlar: sag ustte buyuk kume, solda orta kume (REF-069), sol ustte kucuk
    bulut = mat_emis("bulut", lin(hex3("#2ad8ff")), 1.6); bulut_ic = mat_emis("bulut_ic", lin(hex3("#c8fbff")), 2.4)
    bulut_k = mat_emis("bulut_k", lin(hex3("#1a8ae0")), 1.2)
    for cx, cz, r0, tur, kal, yon in ((700, 900, 120, 1.6, 26, -1), (860, 760, 90, 1.4, 22, 1), (560, 1010, 70, 1.3, 18, 1),
                                      (-820, 640, 110, 1.5, 24, 1), (-640, 560, 70, 1.3, 18, -1), (-880, 980, 60, 1.2, 15, 1)):
        sarmal(cx, cz, r0, tur, kal, bulut, bulut_ic, yon=yon, y=0)
        k = kure((cx, 40, cz - r0 * 0.4), r0 * 0.9, bulut_k, sub=2); k.scale = (1.3, 0.2, 0.7)
    # ust ortada yuzen camgobegi hilal serit (REF-069 tepedeki neon kavis)
    hilal = mat_emis("hilal", lin(hex3("#3ff0ff")), 2.6)
    onc = None
    for i in range(13):
        q = i / 12; x = -170 + q * 340; z = 1035 - 40 * math.sin(q * math.pi)
        if onc:
            boru((onc[0], 0, onc[1]), (x, 0, z), 9 * (0.5 + math.sin(q * math.pi)), hilal)
        onc = (x, z)
    # ufuk: lila-pembe kabarik bulut kumesi (korkuluklarin arkasi bos kalmasin)
    lila = [mat_emis("lila%d" % i, lin(hex3(c)), g) for i, (c, g) in enumerate((("#d8b0ff", 1.1), ("#b880ff", 1.0), ("#ff80dc", 1.0)))]
    for i in range(34):
        x = -1000 + i * 60 + rnd.uniform(-20, 20)
        k = kure((x, rnd.uniform(100, 160), rnd.uniform(330, 470)), rnd.uniform(70, 130), rnd.choice(lila), sub=2); k.scale = (1.3, 0.3, 0.8)
    # ufukta isik huzmeleri (REF-069 kapinin iki yanindaki beyaz-mor parlama)
    # kapak 1: beyaz huzmeler sol altta cubuk gibi kaliyordu -> kaldirildi
    if KAPAK:
        sc.view_settings.exposure = POZLAMA
    parlat(sc, esik=1.2, boy=8, mix=0.12)
    yaz(sc, ON_EK + "gok.png")


# ------------------------------------------------------------------ SERIT: katlar + korkuluk + kapi (perspektif, saydam)
def katlar():
    ust = mat_parlak("kat_ust", "#2032c8", emis=0.55, purluk=0.08)
    yan = mat_emis("kat_yan", lin(hex3("#29c8ff")), 2.2)
    pem = mat_emis("kat_neon_p", lin(hex3(PEMBE)), 4.0)
    cam = mat_emis("kat_neon_c", lin(hex3("#7ef6ff")), 3.6)
    yz = [mat_emis("kat_yz%d" % i, lin(hex3(c)), 2.8) for i, c in enumerate((SARI, "#ff5ad8", "#4ae8ff"))]
    rnd = random.Random(18)
    for i, (y0, y1, w, z) in enumerate(KATLAR):
        d = w * 0.22
        pts = [(-w, y0 + d), (0, y0), (w, y0 + d), (w, y1), (-w, y1)]
        alt = KATLAR[i + 1][3] if i + 1 < len(KATLAR) else -0.6
        cokgen("kat%d_yan" % i, pts, alt - 0.02, z - 0.06, yan)
        cokgen("kat%d" % i, pts, z - 0.06, z, ust)
        for a, b in ((pts[0], pts[1]), (pts[1], pts[2])):                     # on kenar: pembe dis, camgobegi ic cizgi
            boru((a[0], a[1], z + 0.01), (b[0], b[1], z + 0.01), 0.06, pem)
            boru((a[0] * 0.9, a[1] + 0.32, z + 0.012), (b[0] * 0.9, b[1] + 0.32, z + 0.012), 0.035, cam)
        for s in (-1, 1):                                                       # yan kenar
            boru((s * w, y0 + d, z + 0.01), (s * w, y1, z + 0.01), 0.06, pem)
        n = 5 + i * 2                                                           # katin ustunde yildizlar (yatik, duz)
        for j in range(n):
            q = (j + 0.5) / n
            x = -w * 0.8 + q * w * 1.6
            yy = y0 + d * abs(x) / w + rnd.uniform(0.45, max(0.6, (y1 - y0) * 0.55))
            yildiz("kat_yz", (x, yy, z + 0.005), rnd.uniform(0.2, 0.32), yz[j % 3], kalin=0.04, yatik=True, aci=rnd.uniform(-0.3, 0.3))


def korkuluk():
    direk = mat_parlak("direk", MAVI, emis=0.5, purluk=0.15)
    halka = mat_emis("direk_halka", lin(hex3(PEMBE)), 3.2)
    tepe = mat_parlak("direk_tepe", "#c83cff", emis=0.6)
    syz = mat_parlak("direk_yz", SARI, emis=1.4, purluk=0.1)
    pano = mat_parlak("pano", "#2a3ae8", emis=0.6)
    pano_k = mat_emis("pano_k", lin(hex3(CAMG)), 2.6)
    pano_yz = mat_parlak("pano_yz", SARI, emis=1.2)
    bp = mat_emis("boru_p", lin(hex3(PEMBE)), 3.0)
    bc = mat_emis("boru_c", lin(hex3(CAMG)), 3.0)
    for s in (-1, 1):
        x = s * KORK_X
        ys = [-1.5, 1.4, 4.3, 7.2, 10.0, 12.4]
        for j, yy in enumerate(ys):
            h = 2.0
            yuvarlak_kutu("direk", (x, yy, h / 2), (0.62, 0.62, h), direk, egim=0.22, seg=4)
            boru((x, yy, h * 0.55 - 0.04), (x, yy, h * 0.55 + 0.04), 0.36, halka)
            yuvarlak_kutu("tepe", (x, yy, h + 0.09), (0.74, 0.74, 0.18), tepe, egim=0.08, seg=3)
            yildiz("direk_yz", (x, yy, h + 0.62), 0.5, syz, kalin=0.2)
            kure((x, yy + 0.32, h * 0.8), 0.13, mat_emis("lamba%d%d" % (s, j), lin(hex3("#fff6c0")), 4.0), sub=2)
            if j < len(ys) - 1:
                ym = (yy + ys[j + 1]) / 2; L = ys[j + 1] - yy - 0.7
                yuvarlak_kutu("pano", (x, ym, 0.62), (0.22, L, 1.0), pano, egim=0.06, seg=2)
                for zz in (0.14, 1.1):
                    boru((x - s * 0.13, ym - L / 2, zz), (x - s * 0.13, ym + L / 2, zz), 0.03, pano_k)
                for q in (-0.25, 0.25):
                    yd = yildiz("pano_yz", (x - s * 0.13, ym + q * L, 0.62), 0.24, pano_yz, kalin=0.05)
                    yd.rotation_euler = (math.pi / 2, 0, -s * math.pi / 2)
        taban = mat_parlak("taban", "#1a2aa8", emis=0.5)
        yuvarlak_kutu("taban", (x + s * 0.6, (ys[0] + ys[-1]) / 2, -0.9), (2.0, ys[-1] - ys[0] + 0.6, 2.0), taban, egim=0.1, seg=2)
        boru((x - s * 0.4, ys[0], 0.08), (x - s * 0.4, ys[-1], 0.08), 0.06, bc)
        boru((x, ys[0], 1.55), (x, ys[-1], 1.55), 0.1, bp)
        boru((x, ys[0], 1.25), (x, ys[-1], 1.25), 0.08, bc)


def kapi():
    Y, X, W_, H_, Z, K = KAP["y"], KAP["x"], KAP["w"], KAP["h"], KAP["z"], KAP["kalin"]
    cer = mat_parlak("kapi_cer", MAVI, emis=0.6, purluk=0.12)
    trim = mat_emis("kapi_trim", lin(hex3(PEMBE)), 3.4)
    trim_c = mat_emis("kapi_trim_c", lin(hex3(CAMG)), 3.0)
    lamba = mat_parlak("kapi_lamba", SARI, emis=2.2, purluk=0.08)
    tac = mat_parlak("kapi_tac", "#3a52ff", emis=0.7)
    xk = W_ / 2 + K / 2
    for s in (-1, 1):
        yuvarlak_kutu("kule", (X + s * xk, Y, Z + (H_ + K) / 2), (K * 1.6, K * 1.4, H_ + K), cer, egim=0.14, seg=3)
        boru((X + s * (xk - K * 0.55), Y - K * 0.75, Z + 0.1), (X + s * (xk - K * 0.55), Y - K * 0.75, Z + H_), 0.05, trim)
        kure((X + s * xk, Y, Z + H_ + K + 0.12), 0.42, lamba, sub=3)
        yuvarlak_kutu("lamba_alt", (X + s * xk, Y, Z + H_ + K - 0.02), (0.9, 0.9, 0.16), trim, egim=0.05, seg=2)
    yuvarlak_kutu("kiris", (X, Y, Z + H_ + K / 2), (W_ + K * 1.6, K * 1.4, K), cer, egim=0.14, seg=3)
    boru((X - W_ / 2, Y - K * 0.75, Z + H_ + 0.05), (X + W_ / 2, Y - K * 0.75, Z + H_ + 0.05), 0.05, trim)
    boru((X - W_ / 2, Y - K * 0.75, Z + 0.05), (X + W_ / 2, Y - K * 0.75, Z + 0.05), 0.05, trim_c)
    # tepe taci: yuvarlak pano + uc yildiz
    yuvarlak_kutu("tac", (X, Y, Z + H_ + K + 0.38), (2.4, 0.5, 0.62), tac, egim=0.2, seg=4)
    boru((X - 1.1, Y - 0.27, Z + H_ + K + 0.12), (X + 1.1, Y - 0.27, Z + H_ + K + 0.12), 0.04, trim_c)
    for i, (dx, c) in enumerate(((-0.7, "#ff5ad8"), (0.0, "#ff5ad8"), (0.7, "#4ae8ff"))):
        yildiz("tac_yz", (X + dx, Y - 0.27, Z + H_ + K + 0.4), 0.24, mat_emis("tac_yz%d" % i, lin(hex3(c)), 3.0), kalin=0.06)
    # ekran zemini: kapi acikligi saydam kalir (ekran / duvar karti motorda); arkada lacivert pano yok


def serit_katmani():
    sc = bos_sahne(w=1920, h=1080, saydam=True, ornek=min(ORNEK, 48))
    sc.cycles.transparent_max_bounces = 16
    kam = kamera(sc)
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (*lin(hex3("#6a4adf")), 1)   # mor gok yansir
    sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.9
    katlar(); korkuluk(); kapi()
    isik("AREA", (0, -3, 7), 900, lin(hex3("#f0e8ff")), 10, yon=(0, 6, 0))
    isik("AREA", (0, KAP["y"] + 3, 4), 400, lin(hex3("#ff7ae8")), 8, yon=(0, 4, 0))
    Y, X, W_, H_, Z = KAP["y"], KAP["x"], KAP["w"], KAP["h"], KAP["z"]
    bpy.context.view_layer.update()
    px = [world_to_camera_view(sc, kam, Vector(p)) for p in ((X - W_ / 2, Y, Z), (X + W_ / 2, Y, Z), (X - W_ / 2, Y, Z + H_), (X + W_ / 2, Y, Z + H_))]
    xs = [p.x * 1920 for p in px]; ys = [(1 - p.y) * 1080 for p in px]
    YERLESIM[ON_EK + "aciklik_p1"] = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
    YERLESIM[ON_EK + "yol"] = {"y_kapi": Y, "x_kapi": X, "kam": KAM, "serit_w": 1920}
    log("aciklik", YERLESIM[ON_EK + "aciklik_p1"])
    if KAPAK:
        sc.view_settings.exposure = POZLAMA
    parlat(sc, esik=1.3, boy=7, mix=0.1, saydam=True)
    yaz(sc, ON_EK + "serit.png")


if YALNIZ in ("hepsi", "poz"):
    poz_maskeleri()
if YALNIZ in ("hepsi", "sahne", "kapak"):
    gok_katmani(); serit_katmani()
json.dump(YERLESIM, open(os.path.join(CIKTI, "yerlesim.json"), "w"), indent=1)
log("bitti (yildizsahne)", YERLESIM.get(ON_EK + "aciklik_p1"))
