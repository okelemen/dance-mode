"""HUMAN TETRIS 19. video (REF-070 TetrisBounce, SOLO Easy Beginner) - NEON YILDIZ KOPRUSU varliklari, TEK serit. varlik.py calistirir (--mod yildizkopru).

REF-070'te ne varsa (md. 22): tepede koyu lacivert, ufka dogru mor-pembe gece gogu; arti seklinde piksel isiltilar (sari, beyaz, pembe, camgobegi),
basamakli piksel bulutlar (lila / pembe), kapinin solunda arkada basamak kenarli sari-turuncu piksel ay, ufukta pembe isilti ve basamakli tepeler;
iki yanda sari pencereli lacivert piksel sehir binalari, tepelerde pembe/camgobegi isikli antenler; kameradan kapiya uzanan koyu parlak mavi
kopru zemini (orta cizgi), zeminde neon cizimler: gulen pembe yildiz, camgobegi bulut, camgobegi pati, sari cift chevron, pembe/camgobegi uzun
cubuklar; iki yanda camgobegi parlak kup direkler (ic yuzlerinde gulen yuz / kedi / ay simgesi) + iki pembe neon boru korkuluk; ortada camgobegi
truss kapi, ust kirisinde simge karolari (bulut, yildiz, ayi, kalp, tavsan), yan kulelerde kucuk simgeler.
Alinmaz (telif): kapi ustundeki iki anime kiz, ilerleme cubugundaki anime kiz. Hologram kart, 3-2-1, sayac ve kendi maskotumuz motorda / kapak betiginde.

Ciktilar:
  gok.png     1920x1080  gece gogu + ay + bulutlar + tepeler + sehir (opak)
  serit.png   1920x1080  kopru zemini + neon cizimler + korkuluk + kapi (saydam)
  yerlesim.json  aciklik_p1 (kapinin ic acikligi, piksel) + kamera
Kapak (--yalniz kapak): ayni katmanlar "kapak-" on ekiyle.
"""

import random
import bmesh
YERLESIM.clear()
KAPAK = YALNIZ == "kapak"
POZLAMA = float(arg("--kapak-pozlama", "0"))
ON_EK = "kapak-" if KAPAK else ""
# REF-070 karesi (1280x720): kapi x %35-65, ust %34, alt %66; korkuluk ucu (ufuk) ~%57; zemin kameraya kadar, korkuluklar kadraj kenarindan tasar.
KAP = {"y": 5.8, "x": 0.0, "w": 4.8, "h": 3.1, "kule": 0.66, "kiris": 0.72}   # sahne 2: kapi x %39-61 ince -> buyuk, kalin truss   # sahne 1: y 12 kapi x %43-57 (ref %35-65) -> yaklastirildi
KORK_X = 3.6
KAM = {"x": 0.0, "y": -1.0, "z": 2.2, "egim": 6.0, "lens": 15.0, "sensor": 24.0, "kaydir": 0.0}
if KAPAK:   # REF-070 kapagi: kapi x %35-65 ust %26, alt %62; sag ve solda korkuluk on planda buyuk
    KAM.update({"x": 0.0, "y": 0.4, "z": 1.7, "egim": 2.0, "lens": 15.0})   # kapak 2: kapi ust %38 (ref %27)
_mat_emis = mat_emis


def mat_emis(ad, renk, guc):
    """18. video kapak dersi: kapakta neon cekirdekleri beyaza patlamasin -> isilti gucu %70"""
    return _mat_emis(ad, renk, guc * (0.7 if KAPAK else 1.0))


PEMBE, CAMG, SARI, MOR = "#ff3fd0", "#3fe8ff", "#ffd83a", "#b070ff"


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
    m = mat_jole(ad, lin(hex3(renk)), emis=emis, purluk=purluk)
    m.node_tree.nodes["Principled BSDF"].inputs["Emission Color"].default_value = (*lin(hex3(renk)), 1)
    return m


def cizgi(noktalar, r, mat, kapali=True):
    """neon cizim: noktalar boyunca yuvarlak kesitli egri (zemin simgeleri, kapi simgeleri)"""
    cu = bpy.data.curves.new("cizgi", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = r; cu.bevel_resolution = 3
    sp = cu.splines.new("POLY"); sp.points.add(len(noktalar) - 1)
    for i, p in enumerate(noktalar):
        sp.points[i].co = (*p, 1)
    sp.use_cyclic_u = kapali
    o = bpy.data.objects.new("cizgi", cu); bpy.context.collection.objects.link(o); o.data.materials.append(mat)
    return o


def yildiz_nok(cx, cy, r, ic=0.45, n=5, aci=0.0):
    return [(cx + math.cos(math.pi / 2 + aci + i * math.pi / n) * (r if i % 2 == 0 else r * ic),
             cy + math.sin(math.pi / 2 + aci + i * math.pi / n) * (r if i % 2 == 0 else r * ic)) for i in range(2 * n)]


def daire_nok(cx, cy, rx, ry=None, n=28, a0=0.0, a1=2 * math.pi):
    ry = rx if ry is None else ry
    return [(cx + math.cos(a0 + (a1 - a0) * i / n) * rx, cy + math.sin(a0 + (a1 - a0) * i / n) * ry) for i in range(n + 1)]


# ------------------------------------------------------------------ GOK: ortografik; x -960..960, z 0..1080
def piksel_disk(cx, cz, r, adim, mat, y):
    """basamak kenarli piksel daire (ay): yatay seritler"""
    z = -r
    while z < r:
        w = math.sqrt(max(0.0, r * r - (z + adim / 2) ** 2))
        w = round(w / adim) * adim
        if w > 0:
            yuvarlak_kutu("ay", (cx, y, cz + z + adim / 2), (2 * w, 1, adim), mat, egim=0.0, seg=1)
        z += adim


def piksel_bulut(cx, cz, w, rnd, mat, y, adim=18):
    """basamakli piksel bulut: ustu daralan uc-dort sira"""
    n = rnd.randint(3, 4)
    for i in range(n):
        ww = w * (1 - i * 0.24) + rnd.uniform(-1, 1) * adim
        ww = max(adim * 3, round(ww / adim) * adim)
        dx = round(rnd.uniform(-0.12, 0.12) * w / adim) * adim
        yuvarlak_kutu("bulut", (cx + dx, y, cz + i * adim), (ww, 1, adim), mat, egim=0.0, seg=1)


def gok_katmani():
    sc = bos_sahne(w=1920, h=1080, ornek=min(ORNEK, 16))
    bpy.ops.object.camera_add(location=(0, -900, 540), rotation=(math.radians(90), 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.type = "ORTHO"; kam.data.ortho_scale = 1920; kam.data.clip_end = 3000
    zem = bpy.data.materials.new("gok"); zem.use_nodes = True; nt = zem.node_tree; nt.nodes.clear()
    # sahne 2: Generated Y duz duzlemde sabit 0,5 cikiyordu (gok tek renk mor) -> dunya yuksekligi z 0..1080 -> 0..1
    gm = nt.nodes.new("ShaderNodeNewGeometry"); sp = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(gm.outputs["Position"], sp.inputs[0])
    mr = nt.nodes.new("ShaderNodeMapRange"); mr.inputs["From Min"].default_value = 0.0; mr.inputs["From Max"].default_value = 1080.0
    nt.links.new(sp.outputs["Z"], mr.inputs["Value"])
    rp = nt.nodes.new("ShaderNodeValToRGB"); cr = rp.color_ramp; nt.links.new(mr.outputs["Result"], rp.inputs[0])
    # sahne 1: gok her yerde pembe-mor kaldi (ref tepede koyu lacivert) -> lacivert yukari genisletildi
    cr.elements[0].position = 0.42; cr.elements[0].color = (*lin(hex3("#ff5ac8")), 1)       # ufukta pembe (REF-070 kapi arkasi isilti)
    cr.elements[1].position = 0.92; cr.elements[1].color = (*lin(hex3("#0a0848")), 1)       # tepede koyu lacivert
    e = cr.elements.new(0.52); e.color = (*lin(hex3("#7a2ad0")), 1)                         # ufuk ustu mor
    e = cr.elements.new(0.66); e.color = (*lin(hex3("#241a8a")), 1)                         # ortada lacivert
    em = nt.nodes.new("ShaderNodeEmission"); nt.links.new(rp.outputs[0], em.inputs[0])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], o.inputs[0])
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 600, 540), rotation=(math.radians(90), 0, 0))
    p = bpy.context.active_object; p.scale = (2000, 1100, 1); bpy.ops.object.transform_apply(scale=True)
    p.data.materials.append(zem)
    rnd = random.Random(70)
    renkler = [mat_emis("yz%d" % i, lin(hex3(c)), 3.2) for i, c in enumerate(("#ffffff", "#ffe56a", "#ff7ae0", "#7af0ff", "#ffe56a"))]
    # isiltilar: arti seklinde piksel yildizlar (buyuk sari, kucuk beyaz/pembe/camgobegi) + kare noktalar
    for _ in range(260):
        b = rnd.choice((3, 3, 4, 5))
        yuvarlak_kutu("yz", (rnd.uniform(-960, 960), 300, rnd.uniform(560, 1080)), (b, 1, b), rnd.choice(renkler), egim=0.0, seg=1)
    for _ in range(60):
        x, z = rnd.uniform(-960, 960), rnd.uniform(600, 1070); L = rnd.choice((18, 24, 30, 44)); t = max(4, L // 6); m = rnd.choice(renkler)
        yuvarlak_kutu("arti_y", (x, 280, z), (t, 1, L), m, egim=0.0, seg=1)
        yuvarlak_kutu("arti_x", (x, 280, z), (L, 1, t), m, egim=0.0, seg=1)
    # basamakli tepeler: ufukta pembe-mor iki sira (sehrin arkasi)
    tepe = [mat_emis("tepe%d" % i, lin(hex3(c)), g) for i, (c, g) in enumerate((("#c040e0", 0.9), ("#ff70d0", 1.0)))]
    for k, (z0, gen, m) in enumerate(((560, 150, tepe[0]), (520, 110, tepe[1]))):
        x = -980
        while x < 980:
            w = rnd.choice((36, 54, 72)); h = z0 + gen * (0.5 + 0.5 * math.sin(x / (210 + 60 * k) + k)) + rnd.uniform(-12, 12)
            yuvarlak_kutu("tepe", (x + w / 2, 200 - 20 * k, (h + 300) / 2), (w, 1, h - 300), m, egim=0.0, seg=1)
            x += w
    # piksel ay: kapinin solunda arkada, sari ust - turuncu alt
    piksel_disk(-420, 600, 170, 22, mat_emis("ay", lin(hex3("#ffd23a")), 3.0), 240)
    piksel_disk(-420, 560, 145, 22, mat_emis("ay_alt", lin(hex3("#ff9a2a")), 2.6), 230)
    # piksel bulutlar: lila / pembe, ust yarida
    bul = [mat_emis("bul%d" % i, lin(hex3(c)), g) for i, (c, g) in enumerate((("#8a5ae8", 1.2), ("#d070f0", 1.2), ("#ff7ad8", 1.1)))]
    for cx, cz, w in ((-560, 860, 220), (-760, 690, 160), (640, 800, 200), (860, 660, 140), (150, 930, 120), (-120, 760, 90)):
        piksel_bulut(cx, cz, w, rnd, rnd.choice(bul), 220)
    # piksel sehir: iki yanda, sari pencereli lacivert binalar + antenler (asagi kadar iner, kopru disi bos kalmasin)
    bina = [mat_emis("bina%d" % i, lin(hex3(c)), 0.55) for i, c in enumerate(("#1a1c6a", "#24207e", "#2a1a70"))]
    pen = [mat_emis("pen%d" % i, lin(hex3(c)), 2.6) for i, c in enumerate(("#ffd84a", "#ffb84a", "#7af0ff"))]
    anten = [mat_emis("anten%d" % i, lin(hex3(c)), 4.0) for i, c in enumerate((PEMBE, CAMG))]
    for s in (-1, 1):
        x = 330
        while x < 1000:
            w = rnd.choice((90, 110, 130, 160)); h = rnd.uniform(380, 560) if x < 700 else rnd.uniform(460, 680)   # sahne 1: binalar ufku kapatiyordu
            cx = s * (x + w / 2)
            yuvarlak_kutu("bina", (cx, 120, h / 2), (w, 1, h), rnd.choice(bina), egim=0.0, seg=1)
            for zz in range(60, int(h) - 40, 34):
                for xx in range(int(-w / 2) + 16, int(w / 2) - 12, 26):
                    if rnd.random() < 0.55:
                        yuvarlak_kutu("pen", (cx + xx + 6, 110, zz), (12, 1, 16), rnd.choice(pen), egim=0.0, seg=1)
            if rnd.random() < 0.45:
                yuvarlak_kutu("anten", (cx, 115, h + 40), (6, 1, 80), bina[0], egim=0.0, seg=1)
                kure((cx, 100, h + 86), 12, rnd.choice(anten), sub=2)
            x += w + rnd.uniform(-8, 10)
    if KAPAK:
        sc.view_settings.exposure = POZLAMA
    parlat(sc, esik=1.2, boy=8, mix=0.12)
    yaz(sc, ON_EK + "gok.png")


# ------------------------------------------------------------------ SERIT: kopru zemini + neon cizimler + korkuluk + kapi (perspektif, saydam)
def zemin():
    """sahne 1: zemin mat acik mor + simgeler dev kaliyordu -> koyu parlak mavi (sol mavi, sag morumsu yansima), simgeler kucuk, kapiya kadar dagilir"""
    for sx, renk in ((-1, "#121a9a"), (1, "#3a128a")):
        yuvarlak_kutu("zemin", (sx * (KORK_X + 0.2) / 2, KAP["y"] - 1, -0.15), (KORK_X + 0.2, KAP["y"] + 8, 0.3), mat_parlak("zemin%d" % sx, renk, emis=0.18, purluk=0.14), egim=0.0, seg=1)   # sahne 3: ayna zeminde kapi ayaklari etek gibi yansiyordu -> purluk 0,14
    kenar = mat_emis("zemin_kenar", lin(hex3(CAMG)), 3.0)
    for s_ in (-1, 1):
        boru((s_ * (KORK_X - 0.15), -3, 0.02), (s_ * (KORK_X - 0.15), KAP["y"] + 3, 0.02), 0.04, kenar)
    boru((0, -3, 0.005), (0, KAP["y"], 0.005), 0.02, mat_emis("orta", lin(hex3("#c8f8ff")), 1.4))
    pem = mat_emis("z_pem", lin(hex3(PEMBE)), 4.0); cam = mat_emis("z_cam", lin(hex3(CAMG)), 3.6); sar = mat_emis("z_sar", lin(hex3(SARI)), 3.6)
    z = 0.02
    # gulen pembe yildiz (on sol) + kucuk pembe yildiz (kapi onu sol), camgobegi pati (on sag), camgobegi bulut (kapi onu sag)
    for (cx, cy, r, m) in ((-1.1, 1.7, 0.42, pem), (-0.9, 4.2, 0.28, pem)):
        cizgi([(x, y, z) for x, y in yildiz_nok(cx, cy, r, ic=0.5)], 0.03, m)
        cizgi([(x, y, z) for x, y in daire_nok(cx, cy - r * 0.12, r * 0.22, n=12, a0=math.pi, a1=2 * math.pi)], 0.02, m, kapali=False)
    cizgi([(x, y, z) for x, y in daire_nok(1.15, 1.6, 0.3, 0.22)], 0.03, cam)
    for dx, dy in ((-0.34, 0.3), (-0.12, 0.42), (0.12, 0.42), (0.34, 0.3)):
        cizgi([(x, y, z) for x, y in daire_nok(1.15 + dx, 1.6 + dy, 0.09)], 0.025, cam)
    bulut = daire_nok(1.05, 4.2, 0.32, 0.2, n=10, a0=0, a1=math.pi) + daire_nok(0.6, 4.2, 0.24, 0.17, n=8, a0=0.2, a1=math.pi) + [(0.36, 4.17), (1.37, 4.17)]
    cizgi([(x, y, z) for x, y in bulut], 0.03, cam)
    # sari cift chevron (orta) + pembe/camgobegi cubuklar (V, kapiya bakar)
    for k in range(2):
        yy = 3.0 + k * 0.22
        cizgi([(-0.35, yy, z), (0, yy + 0.25, z), (0.35, yy, z)], 0.035, sar, kapali=False)
    for s_, m in ((-1, pem), (1, cam)):
        for (y0, L) in ((2.2, 1.4), (5.0, 1.0)):
            a = (s_ * 0.2, y0); b = (s_ * (0.2 + L), y0 - 0.3)
            cizgi([(a[0], a[1], z), (b[0], b[1], z), (b[0], b[1] - 0.22, z), (a[0], a[1] - 0.22, z)], 0.028, m)


def korkuluk():
    direk = mat_parlak("direk", "#4ae0ff", emis=0.9, purluk=0.1)
    yuz = mat_parlak("direk_yuz", "#c8f8ff", emis=1.0, purluk=0.1)
    simge = [mat_emis("simge%d" % i, lin(hex3(c)), 3.2) for i, c in enumerate((SARI, PEMBE, "#ff9a2a"))]
    bp = mat_emis("boru_p", lin(hex3(PEMBE)), 3.2)
    for s in (-1, 1):
        x = s * KORK_X
        ys = [-1.4, 0.6, 2.6, 4.6, 6.6, 8.6]   # sahne 1: kopru kapidan cok oteye uzaniyordu
        for j, yy in enumerate(ys):
            h = 1.2
            yuvarlak_kutu("direk", (x, yy, h / 2), (0.5, 0.5, h), direk, egim=0.06, seg=2)
            yuvarlak_kutu("direk_kapak", (x, yy, h + 0.05), (0.56, 0.56, 0.1), yuz, egim=0.03, seg=2)
            # ic yuzde simge: gulen yuz / kedi / ay (sirayla)
            fy = yy - 0.27; m = simge[j % 3]; zc = h * 0.5   # sahne 1: ic yuzdeki simge zeminde cizgi gibi okunuyordu -> kameraya bakan on yuz
            if j % 3 == 0:
                cizgi([(x + math.cos(t) * 0.2, fy, zc + math.sin(t) * 0.2) for t in [i / 20 * 2 * math.pi for i in range(21)]], 0.025, m)
                cizgi([(x + math.cos(t) * 0.11, fy, zc + math.sin(t) * 0.11) for t in [math.pi * (1.15 + i / 10 * 0.7) for i in range(11)]], 0.02, m, kapali=False)
            elif j % 3 == 1:
                cizgi([(x + math.cos(t) * 0.19, fy, zc + math.sin(t) * 0.17) for t in [i / 20 * 2 * math.pi for i in range(21)]], 0.025, m)
                for e in (-1, 1):
                    cizgi([(x + e * 0.17, fy, zc + 0.08), (x + e * 0.14, fy, zc + 0.3), (x + e * 0.04, fy, zc + 0.16)], 0.022, m, kapali=False)
            else:
                cizgi([(x + math.cos(t) * 0.2, fy, zc + math.sin(t) * 0.2) for t in [math.pi * (0.3 + i / 16 * 1.4) for i in range(17)]]
                      + [(x + math.cos(t) * 0.12 + 0.07, fy, zc + math.sin(t) * 0.14) for t in [math.pi * (1.7 - i / 16 * 1.4) for i in range(17)]], 0.022, m)
            if j < len(ys) - 1:
                for zz in (0.6, 1.0):
                    boru((x, yy + 0.26, zz), (x, ys[j + 1] - 0.26, zz), 0.07, bp)


def kapi():
    Y, X, W_, H_, KK, KR = KAP["y"], KAP["x"], KAP["w"], KAP["h"], KAP["kule"], KAP["kiris"]
    ana = mat_parlak("kapi_ana", "#5ae8ff", emis=1.0, purluk=0.1)
    ince = mat_emis("kapi_ince", lin(hex3("#ff7ae0")), 2.6)
    xk = W_ / 2 + KK / 2
    for s in (-1, 1):
        kafes_kule(X + s * xk, Y, 0.0, H_ + KR, KK, ana, ince)
    kafes_kiris(X - xk - KK / 2, X + xk + KK / 2, Y, H_ + KR / 2, KR, ana, ince)
    # ust kiris onunde simge karolari: bulut, yildiz, ayi, kalp, tavsan, yildiz, bulut (kendi cizimimiz)
    karo = mat_parlak("karo", "#2a2ab8", emis=0.6)
    renk = {"bulut": CAMG, "yildiz": SARI, "ayi": CAMG, "kalp": PEMBE, "tavsan": PEMBE}
    sira = ["bulut", "yildiz", "ayi", "kalp", "tavsan", "yildiz", "bulut"]
    n = len(sira); L = 2 * xk + KK
    yf = Y - KR / 2 - 0.04; zc = H_ + KR / 2
    for i, ad in enumerate(sira):
        cx = X - L / 2 + (i + 0.5) * L / n
        yuvarlak_kutu("karo", (cx, yf + 0.03, zc), (L / n * 0.86, 0.06, KR * 0.86), karo, egim=0.03, seg=2)
        m = mat_emis("ks_%d" % i, lin(hex3(renk[ad])), 3.4); r = KR * 0.3
        P = lambda pts: [(cx + px, yf - 0.01, zc + pz) for px, pz in pts]
        if ad == "yildiz":
            cizgi(P(yildiz_nok(0, 0, r, ic=0.48)), 0.022, m)
        elif ad == "kalp":
            cizgi(P([(math.sin(t) ** 3 * r, (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)) / 16 * r) for t in [i / 30 * 2 * math.pi for i in range(31)]]), 0.022, m)
        elif ad == "bulut":
            cizgi(P(daire_nok(0.05, -0.05, r, r * 0.6, n=10, a0=0, a1=math.pi) + daire_nok(-r * 0.55, -0.05, r * 0.5, r * 0.45, n=8, a0=0.3, a1=math.pi) + [(-r * 1.05, -0.08), (r * 1.05, -0.08)]), 0.02, m)
        else:   # ayi / tavsan: yuz + kulak
            cizgi(P(daire_nok(0, -0.04, r * 0.8)), 0.02, m)
            for e in (-1, 1):
                if ad == "ayi":
                    cizgi(P(daire_nok(e * r * 0.62, r * 0.62, r * 0.28)), 0.018, m)
                else:
                    cizgi(P(daire_nok(e * r * 0.32, r * 0.95, r * 0.15, r * 0.4)), 0.018, m)
    # yan kulelerde kucuk simgeler (yildiz / kalp / ayi) on yuzde
    for s in (-1, 1):
        for k, (zz, c) in enumerate(((0.8, PEMBE), (1.7, SARI), (2.6, CAMG))):
            cizgi([(X + s * xk + px, Y - KK / 2 - 0.05, zz + pz) for px, pz in yildiz_nok(0, 0, 0.17, ic=0.48)], 0.02, mat_emis("ky%d%d" % (s, k), lin(hex3(c)), 3.2))


def serit_katmani():
    sc = bos_sahne(w=1920, h=1080, saydam=True, ornek=min(ORNEK, 48))
    sc.cycles.transparent_max_bounces = 16
    kam = kamera(sc)
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (*lin(hex3("#4a3ae0")), 1)   # sahne 2: zemin pembe-lila parliyordu (ref koyu mavi) -> mavi-mor gok, kisik
    sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.55
    zemin(); korkuluk(); kapi()
    isik("AREA", (0, -2, 6), 500 if KAPAK else 800, lin(hex3("#c8a8ff" if KAPAK else "#f0e8ff")), 10, yon=(0, 6, 0))
    isik("AREA", (0, KAP["y"] + 3, 3), 160, lin(hex3("#ff7ae8")), 8, yon=(0, -4, 0))
    Y, X, W_, H_ = KAP["y"], KAP["x"], KAP["w"], KAP["h"]
    bpy.context.view_layer.update()
    px = [world_to_camera_view(sc, kam, Vector(p)) for p in ((X - W_ / 2, Y, 0), (X + W_ / 2, Y, 0), (X - W_ / 2, Y, H_), (X + W_ / 2, Y, H_))]
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
log("bitti (yildizkopru)", YERLESIM.get(ON_EK + "aciklik_p1"))
