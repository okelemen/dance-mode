"""HUMAN TETRIS 20. video (REF-072 TetrisBounce, 3 oyuncu 1v1v1) - UC NEON PIST + SISME BALON KAPI varliklari. varlik.py calistirir (--mod balonpist).

REF-072'de ne varsa (md. 22): ekran uce bolunur, her oyuncunun kendi seridi (P1 pembe sol / P2 mavi orta / P3 sari sag);
her seritte sisme balon gibi yastik bloklardan kapi (her blokta beyaz yildiz / kalp), kapinin ic kenarlarinda beyaz X kafes,
kapidan kameraya inen chevron basamakli parlak yol (neon kenar), iki yanda balon babali korkuluk + parlak boru; arkada mor yildizli
gece gogu, iki yanda pembe kabarik bulutlar, sari yildizlar. Alinmaz (telif): anime kiz maskot, oyuncu kartlarindaki anime karakterler.
Duvar karti (pastel), siyah siluet, 3-2-1, ROUND, ilerleme cubugu, kendi maskotumuz motorda / kapak betiginde.

Ciktilar:
  gok.png            1920x1080  gok + yildizlar + pembe bulutlar (opak)
  serit-p1..p3.png   640x1080   her oyuncunun seridi (gokte saydam), kapi acikligi saydam
  yerlesim.json      aciklik_p1..p3 (serit koordinati), kamera
Kapak (--yalniz kapak): kapak-gok.png + kapak-serit-p1..p3.png (ayni boy; kapak betigi 1280x720'ye 3 x 427 olarak dizer);
REF-072 kapaginda kapilar daha yakin ve buyuk, kapi icinde koyu lacivert neon izgara ekran.
"""

import random
import bmesh
YERLESIM.clear()
KAPAK = YALNIZ == "kapak"
POZLAMA = float(arg("--kapak-pozlama", "0"))
ON_EK = "kapak-" if KAPAK else ""
SERIT_W = 640
OYUNCU = {"p1": "#ff4fc8", "p2": "#2fb4ff", "p3": "#ffc21a"}          # pembe | mavi | sari (REF-072)
ACIK = {"p1": "#ffb8ec", "p2": "#a8e4ff", "p3": "#fff0a0"}
# REF-072 karesi (seritte): kapi ust ~%11, kart alt ~%66, kapi dis genislik ~seridin %85'i; yol kapidan kameraya iner
KAP = {"y": 10.0, "w": 2.9, "h": 4.0, "z": 1.0, "blok": 0.8}      # sahne 1: aciklik seridin %68i (ref ~%45) -> daralt         # ic aciklik w x h (dikey kart), blok = yastik blok kalinligi
KAM = {"x": 0.0, "y": 0.0, "z": 3.0, "egim": 4.0, "lens": 21.5, "sensor": 24.0}
if KAPAK:   # REF-072 kapagi: kapi ust ~%28, alt ~%80, seridi dolduruyor
    KAM.update({"y": float(arg("--kapak-y", "2.2")), "z": float(arg("--kapak-z", "3.3")), "egim": float(arg("--kapak-egim", "2.0"))})
YOL_W = 1.55          # yol yari genislik
KORK_X = 2.15         # korkuluk cizgisi
BASAMAK = [(8.6, 9.9, 0.80), (7.2, 8.6, 0.60), (5.8, 7.2, 0.40), (4.4, 5.8, 0.20), (2.5, 4.4, 0.0)]   # (on y, arka y, ust z) kapidan kameraya


def kamera(sc):
    rx = math.radians(90 - KAM["egim"])
    bpy.ops.object.camera_add(location=(KAM["x"], KAM["y"], KAM["z"]), rotation=(rx, 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.sensor_fit = "VERTICAL"; kam.data.sensor_height = KAM["sensor"]; kam.data.lens = KAM["lens"]
    kam.data.clip_end = 900
    return kam


def parlat(sc, esik=1.0, boy=7, mix=0.12, saydam=False):
    sc.use_nodes = True; sc.render.use_compositing = True; nt = sc.node_tree; nt.nodes.clear()
    rl = nt.nodes.new("CompositorNodeRLayers"); g = nt.nodes.new("CompositorNodeGlare"); o = nt.nodes.new("CompositorNodeComposite")
    g.glare_type = "FOG_GLOW"; g.quality = "HIGH"; g.threshold = esik; g.size = boy; g.mix = mix
    nt.links.new(rl.outputs["Image"], g.inputs[0]); nt.links.new(g.outputs[0], o.inputs[0])
    if saydam:
        nt.links.new(rl.outputs["Alpha"], o.inputs[1])


def mat_parlak(ad, renk, emis=0.35, purluk=0.15):
    """REF-072 balon yuzeyi: doygun parlak plastik + kendi renginde isilti"""
    m = mat_jole(ad, lin(hex3(renk)), emis=emis, purluk=purluk)
    m.node_tree.nodes["Principled BSDF"].inputs["Emission Color"].default_value = (*lin(hex3(renk)), 1)
    return m


def prizma(ad, noktalar, z0, z1, mat, egim=0.0):
    """duz tabanli prizma (chevron basamak, yildiz, kalp)"""
    me = bpy.data.meshes.new(ad); bm = bmesh.new()
    alt = [bm.verts.new((x, y, z0)) for x, y in noktalar]
    yuz = bm.faces.new(alt)
    ex = bmesh.ops.extrude_face_region(bm, geom=[yuz])
    for v in [e for e in ex["geom"] if isinstance(e, bmesh.types.BMVert)]:
        v.co.z = z1
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(ad, me); bpy.context.collection.objects.link(o)
    if egim > 0:
        bv = o.modifiers.new("egim", "BEVEL"); bv.width = egim; bv.segments = 3; bv.limit_method = "NONE"
    o.data.materials.append(mat)
    return o


def yildiz_nok(r, ic=0.45):
    return [(math.cos(math.pi / 2 + i * math.pi / 5) * (r if i % 2 == 0 else r * ic),
             math.sin(math.pi / 2 + i * math.pi / 5) * (r if i % 2 == 0 else r * ic)) for i in range(10)]


def kalp_nok(r):
    pts = []
    for i in range(36):
        t = i / 36 * 2 * math.pi
        x = 16 * math.sin(t) ** 3; y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((x / 17 * r, y / 17 * r))
    return pts


def simge(ad, nok, konum, mat, kalin=0.05):
    """kameraya bakan yassi simge (blok onundeki yildiz / kalp)"""
    o = prizma(ad, nok, 0, kalin, mat, egim=kalin * 0.3)
    o.location = konum; o.rotation_euler = (math.pi / 2, 0, 0)
    return o


# ------------------------------------------------------------------ GOK: ortografik; x -960..960, z 0..1080
def gok_katmani():
    sc = bos_sahne(w=1920, h=1080, ornek=min(ORNEK, 16))
    bpy.ops.object.camera_add(location=(0, -900, 540), rotation=(math.radians(90), 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.type = "ORTHO"; kam.data.ortho_scale = 1920; kam.data.clip_end = 3000
    zem = bpy.data.materials.new("gok"); zem.use_nodes = True; nt = zem.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord"); sp = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Object"], sp.inputs[0])
    mp = nt.nodes.new("ShaderNodeMapRange"); mp.inputs["From Min"].default_value = -540; mp.inputs["From Max"].default_value = 540
    nt.links.new(sp.outputs["Y"], mp.inputs["Value"])     # duzlem yerelinde Y = dunya z (90 derece dondu); 19. videodaki Generated sabit 0,5 tuzagi yok
    rp = nt.nodes.new("ShaderNodeValToRGB"); cr = rp.color_ramp; nt.links.new(mp.outputs[0], rp.inputs[0])
    cr.elements[0].position = 0.15; cr.elements[0].color = (*lin(hex3("#c050e8")), 1)     # ufka dogru pembe-mor (sahne 1: tepe siyaha yakindi, ref parlak mor)
    cr.elements[1].position = 0.95; cr.elements[1].color = (*lin(hex3("#2a0e78")), 1)     # tepede koyu mor
    ara = cr.elements.new(0.55); ara.color = (*lin(hex3("#5a20b8")), 1)
    em = nt.nodes.new("ShaderNodeEmission"); nt.links.new(rp.outputs[0], em.inputs[0])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], o.inputs[0])
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 600, 540), rotation=(math.radians(90), 0, 0))
    p = bpy.context.active_object; p.scale = (2000, 1080, 1); bpy.ops.object.transform_apply(scale=True)
    p.data.materials.append(zem)
    rnd = random.Random(72)
    renkler = [mat_emis("yz%d" % i, lin(hex3(c)), 3.0) for i, c in enumerate(("#ffffff", "#ffd0f4", "#c8f4ff", "#fff2a0"))]
    for _ in range(520):                       # kucuk yildiz noktalari
        x, z = rnd.uniform(-960, 960), rnd.uniform(250, 1080)
        kure((x, 300, z), rnd.choice((1.6, 2.0, 2.6, 3.4)), rnd.choice(renkler), sub=1)
    for _ in range(40):                        # arti isiltilar
        x, z = rnd.uniform(-960, 960), rnd.uniform(300, 1070); L = rnd.uniform(12, 26); m = rnd.choice(renkler)
        yuvarlak_kutu("isilti_y", (x, 280, z), (2.6, 1, L), m, egim=0.0, seg=1)
        yuvarlak_kutu("isilti_x", (x, 280, z), (L, 1, 2.6), m, egim=0.0, seg=1)
    sari = mat_parlak("gok_sari", "#ffd23a", emis=2.2, purluk=0.1)
    for _ in range(22):                        # REF-072 dolgun sari yildizlar (bulutlarin ustunde, kapilarin arasinda)
        o = prizma("gyz", yildiz_nok(rnd.uniform(14, 30), 0.5), 0, 6, sari, egim=2.5)
        o.location = (rnd.uniform(-950, 950), 200, rnd.uniform(380, 1050)); o.rotation_euler = (math.pi / 2, 0, rnd.uniform(-0.4, 0.4))
    # pembe kabarik bulutlar: iki yanda yuksege tirmanan kume + ufukta yatay serit (kapilarin arkasi bos kalmasin)
    pem = [mat_emis("bulut%d" % i, lin(hex3(c)), g) for i, (c, g) in enumerate((("#ff6ad8", 1.15), ("#ff8ae4", 1.2), ("#d860ff", 1.05), ("#ffa8ec", 1.25)))]
    for i in range(40):
        x = -1000 + i * 52 + rnd.uniform(-20, 20)
        k = kure((x, rnd.uniform(100, 160), rnd.uniform(260, 430)), rnd.uniform(60, 120), rnd.choice(pem), sub=2); k.scale = (1.4, 0.3, 0.8)
    for xm in (-960, -320, 320, 960):           # sahne 1: bulutlar zayifti -> her serit sinirinda (kapilarin iki yani) yukselen pembe kume
        for i in range(12):
            x = xm + rnd.uniform(-170, 170); z = rnd.uniform(300, 640)
            k = kure((x, rnd.uniform(60, 120), z), rnd.uniform(60, 120), rnd.choice(pem), sub=2); k.scale = (1.4, 0.3, 0.8)
    if KAPAK:
        sc.view_settings.exposure = POZLAMA
    parlat(sc, esik=1.1, boy=8, mix=0.14)
    yaz(sc, ON_EK + "gok.png")


# ------------------------------------------------------------------ SERIT: yol + korkuluk + balon kapi (perspektif, saydam)
def yol(oy):
    R, A = OYUNCU[oy], ACIK[oy]
    # sahne 1: basamaklar beyaza patliyordu (ust ACIK renk, emis 0,9) -> ust serit renginde, kenar neonu acik ton (REF-072 doygun basamak)
    ust = mat_parlak("bas_ust_" + oy, R, emis=0.3, purluk=0.06)
    yan = mat_jole("bas_yan_" + oy, lin(koyu(hex3(R), 0.35)), emis=0.2, purluk=0.1)
    neon = mat_emis("bas_neon_" + oy, lin(acik(hex3(R), 0.35)), 3.2)
    beyaz = mat_emis("bas_beyaz_" + oy, lin(acik(hex3(R), 0.7)), 2.2)
    zem = mat_jole("zemin_" + oy, lin(koyu(hex3(R), 0.5)), emis=0.15, purluk=0.08)
    prizma("zemin", [(-KORK_X - 0.6, -2), (KORK_X + 0.6, -2), (KORK_X + 0.6, 12), (-KORK_X - 0.6, 12)], -0.9, -0.05, zem)
    for i, (y0, y1, z) in enumerate(BASAMAK):
        w = YOL_W; d = w * 0.32
        pts = [(-w, y0 + d), (0, y0), (w, y0 + d), (w, y1), (-w, y1)]
        alt = BASAMAK[i + 1][2] if i + 1 < len(BASAMAK) else -0.6
        prizma("bas%d_yan" % i, pts, alt - 0.02, z - 0.07, yan)
        prizma("bas%d" % i, pts, z - 0.07, z, ust)
        for a_, b_ in ((pts[0], pts[1]), (pts[1], pts[2])):          # on kenar: kalin neon + icte beyaz cizgi (REF-072 chevron)
            boru((a_[0], a_[1], z + 0.01), (b_[0], b_[1], z + 0.01), 0.07, neon)
            boru((a_[0] * 0.82, a_[1] + 0.3, z + 0.012), (b_[0] * 0.82, b_[1] + 0.3, z + 0.012), 0.035, beyaz)
            boru((a_[0] * 0.6, a_[1] + 0.55, z + 0.012), (b_[0] * 0.6, b_[1] + 0.55, z + 0.012), 0.03, neon)
        for s in (-1, 1):
            boru((s * w, y0 + d, z + 0.01), (s * w, y1, z + 0.01), 0.06, neon)


def korkuluk(oy, rnd):
    R = OYUNCU[oy]
    govde = mat_parlak("baba_" + oy, R, emis=0.25, purluk=0.08)       # sahne 1: babalar soluk / kucuktu
    tepe = mat_parlak("baba_tepe_" + oy, R, emis=0.3, purluk=0.08)
    boru_n = mat_emis("kork_neon_" + oy, lin(hex3(R)), 3.6)
    boru_b = mat_emis("kork_beyaz_" + oy, lin(acik(hex3(R), 0.7)), 3.0)
    isil = mat_emis("kork_isil_" + oy, lin((1, 1, 1)), 6.0)
    for s in (-1, 1):
        x = s * KORK_X
        for yy in [3.0 + j * 0.85 for j in range(9)]:
            zt = max(0.0, min(0.8, (yy - 2.5) / 9.9 * 0.85))           # basamaklarla birlikte yukselir
            k = kure((x, yy, zt + 0.4), 0.38, govde, sub=3); k.scale = (1, 1, 1.15)   # REF-072 balon babasi: govde + boyun + bas
            boru((x, yy, zt + 0.7), (x, yy, zt + 0.9), 0.15, govde)
            kure((x, yy, zt + 1.08), 0.26, tepe, sub=3)
            kure((x - s * 0.08, yy - 0.18, zt + 1.18), 0.06, isil, sub=1)  # parlak nokta
        boru((x - s * 0.05, 2.8, 0.55), (x - s * 0.05, 10.0, 1.32), 0.07, boru_n)
        boru((x - s * 0.05, 2.8, 0.2), (x - s * 0.05, 10.0, 0.98), 0.05, boru_b)
        for _ in range(12):                                             # yol kenarinda parilti
            kure((x - s * rnd.uniform(0.2, 0.6), rnd.uniform(3, 9.6), rnd.uniform(0.9, 1.8)), rnd.uniform(0.02, 0.04), isil, sub=1)


def kapi(oy, ekran=False):
    """REF-072 balon kapi: yastik bloklardan cerceve (her blokta yildiz / kalp), ic kenarlarda beyaz X kafes"""
    Y, W_, H_, Z, B = KAP["y"], KAP["w"], KAP["h"], KAP["z"], KAP["blok"]
    R = OYUNCU[oy]
    # sahne 1: acik ton bloklar beyaz, beyaz celik kafes -> REF-072'de bloklar da kafes de serit renginde balon (kafes daha acik ton)
    blok = mat_parlak("blok_" + oy, R, emis=0.22, purluk=0.07)
    blok2 = mat_jole("blok2_" + oy, lin(koyu(hex3(R), 0.12)), emis=0.2, purluk=0.07)
    simge_m = mat_emis("simge_" + oy, lin((1, 1, 1)), 2.2)
    kafes = mat_jole("kafes_" + oy, lin(acik(hex3(R), 0.35)), emis=0.35, purluk=0.07)
    kafes_ic = mat_emis("kafes_ic_" + oy, lin(acik(hex3(R), 0.5)), 2.0)
    KF = 0.62                                                           # kafes seridi genisligi (aciklik ile blok arasi)
    xi = W_ / 2 + KF                                                    # blok sutununun ic kenari
    n_dik = 6; hb = (H_ + KF * 2) / n_dik
    k = 0
    for s in (-1, 1):                                                   # yan sutunlar
        for j in range(n_dik):
            zc = Z - KF + hb * (j + 0.5)
            yuvarlak_kutu("blok", (s * (xi + B / 2), Y, zc), (B, B * 0.9, hb * 0.94), blok if (j + k) % 2 == 0 else blok2, egim=0.24, seg=5)
            nok = yildiz_nok(0.17) if (j + k) % 2 == 0 else kalp_nok(0.15)
            simge("simge", nok, (s * (xi + B / 2), Y - B * 0.47, zc), simge_m)
        k += 1
    n_ust = 7; wb = (xi + B) * 2 / n_ust
    for j in range(n_ust):                                              # ust sira (kalin balon bloklar)
        xc = -(xi + B) + wb * (j + 0.5)
        yuvarlak_kutu("blok_ust", (xc, Y, Z + H_ + KF + B * 0.5), (wb * 0.94, B * 0.9, B), blok if j % 2 == 0 else blok2, egim=0.26, seg=5)
        simge("simge", yildiz_nok(0.17) if j % 2 == 0 else kalp_nok(0.15), (xc, Y - B * 0.47, Z + H_ + KF + B * 0.5), simge_m)
    for j in range(n_ust):                                              # alt esik
        xc = -(xi + B) + wb * (j + 0.5)
        yuvarlak_kutu("blok_alt", (xc, Y, Z - KF - B * 0.22), (wb * 0.94, B * 0.9, B * 0.44), blok2, egim=0.14, seg=4)
    # ic kenar kafesi: iki dikme + X caprazlar (sol, sag, ust)
    for s in (-1, 1):
        for xx in (s * (W_ / 2 + 0.04), s * (xi - 0.04)):
            boru((xx, Y - 0.1, Z - KF), (xx, Y - 0.1, Z + H_ + KF), 0.1, kafes)
        n = 7; h = (H_ + 2 * KF) / n
        for j in range(n):
            z0 = Z - KF + j * h
            boru((s * (W_ / 2 + 0.04), Y - 0.1, z0), (s * (xi - 0.04), Y - 0.1, z0 + h), 0.07, kafes)
            boru((s * (xi - 0.04), Y - 0.1, z0), (s * (W_ / 2 + 0.04), Y - 0.1, z0 + h), 0.07, kafes)
        boru((s * (W_ / 2 + KF / 2), Y - 0.14, Z - KF), (s * (W_ / 2 + KF / 2), Y - 0.14, Z + H_ + KF), 0.012, kafes_ic)
    for zz in (Z + H_ + 0.04, Z + H_ + KF - 0.04):
        boru((-xi, Y - 0.1, zz), (xi, Y - 0.1, zz), 0.1, kafes)
    n = 9; w = 2 * xi / n
    for j in range(n):
        x0 = -xi + j * w
        boru((x0, Y - 0.1, Z + H_), (x0 + w, Y - 0.1, Z + H_ + KF), 0.07, kafes)
        boru((x0 + w, Y - 0.1, Z + H_), (x0, Y - 0.1, Z + H_ + KF), 0.07, kafes)
    if ekran:   # kapak: kapi icinde koyu lacivert ekran + oyuncu renginde neon izgara (REF-072 kapagi)
        bpy.ops.mesh.primitive_plane_add(size=1, location=(0, Y + 0.05, Z + H_ / 2), rotation=(math.pi / 2, 0, 0))
        e = bpy.context.active_object; e.scale = (W_, H_, 1); e.data.materials.append(mat_emis("ekran_z", lin(hex3("#160a40")), 1.0))
        iz = mat_emis("izgara_" + oy, lin(hex3(R)), 2.6)
        for j in range(1, 8):
            x = -W_ / 2 + W_ * j / 8
            boru((x, Y, Z), (x, Y, Z + H_), 0.012, iz)
        for j in range(1, 10):
            z = Z + H_ * j / 10
            boru((-W_ / 2, Y, z), (W_ / 2, Y, z), 0.012, iz)


def serit_katmani(oy):
    rnd = random.Random({"p1": 11, "p2": 13, "p3": 17}[oy])
    sc = bos_sahne(w=SERIT_W, h=1080, saydam=True, ornek=min(ORNEK, 48))
    sc.cycles.transparent_max_bounces = 16
    kam = kamera(sc)
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (*lin(hex3("#7a3ae0")), 1)   # mor gok yansir
    sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.8
    yol(oy); korkuluk(oy, rnd); kapi(oy, ekran=KAPAK)
    R = lin(hex3(OYUNCU[oy]))
    isik("AREA", (0, -2, 7), 300, lin(hex3("#f4e8ff")), 8, yon=(0, 7, 0))   # sahne 1: 700 beyaza patlatiyordu
    isik("AREA", (0, KAP["y"] - 3, 5), 350, acik(R, 0.3), 6, yon=(0, KAP["y"], 2))
    Y, W_, H_, Z = KAP["y"], KAP["w"], KAP["h"], KAP["z"]
    bpy.context.view_layer.update()
    px = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-W_ / 2, Y, Z), (W_ / 2, Y, Z), (-W_ / 2, Y, Z + H_), (W_ / 2, Y, Z + H_))]
    xs = [p.x * SERIT_W for p in px]; ys = [(1 - p.y) * 1080 for p in px]
    YERLESIM[ON_EK + "aciklik_" + oy] = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
    log("aciklik", oy, YERLESIM[ON_EK + "aciklik_" + oy])
    if KAPAK:
        sc.view_settings.exposure = POZLAMA
    parlat(sc, esik=1.3, boy=7, mix=0.1, saydam=True)
    yaz(sc, ON_EK + "serit-%s.png" % oy)


if YALNIZ in ("hepsi", "poz"):
    poz_maskeleri()
if YALNIZ in ("hepsi", "sahne", "kapak"):
    gok_katmani()
    for oy_ in OYUNCU:
        serit_katmani(oy_)
    YERLESIM[ON_EK + "yol"] = {"y_kapi": KAP["y"], "kam": KAM, "serit_w": SERIT_W}
json.dump(YERLESIM, open(os.path.join(CIKTI, "yerlesim.json"), "w"), indent=1)
log("bitti (balonpist)", {k: v for k, v in YERLESIM.items() if "aciklik" in k})
