"""HUMAN TETRIS 24. video (REFERANSSIZ, 1v1) - GUNDUZ HAVUZLU YARISMA STUDYOSU sahne varliklari. varlik.py calistirir (--mod havuz).

Kullanici 11 Kas 2026: "Bugun referans kanal yok ... yeni mekan, yeni talimatlara gore" -> POZ-DUVARI TALIMATLAR §2b 1. mekan:
gunduz, aydinlik acik hava yarisma stadyumu; mavi gok + beyaz bulutlar, renkli tribun + seyirci, isik kuleleri, bayrak dizisi, sisme toplar.
Her oyuncunun seridi: havuzun ustunde beyaz-renkli yastikli platform (yolda renkli ok), iki yanda su; sonda ampul dizili yarisma kapisi.
OUT ani (mobil paket md. 2) motorda: karakter platformdan suya duser, su sicrar. Telif: bilinen TV sovlarinin seti / logosu / duvari alinmaz.
Taban: varlik-lunapark.py (iki seritli yapi, ayni cikti dosyalari, ayni yerlesim anahtarlari).

Ciktilar: gok.png, serit-p1/p2.png, panel-p1/p2.png, yerlesim.json; kapak modu (--yalniz kapak): kapak-gok.png, kapak-serit-p1/p2.png
"""

import random
YERLESIM.clear()
KAPAK = YALNIZ == "kapak"
POZLAMA = float(arg("--kapak-pozlama", "0"))
ON_EK = "kapak-" if KAPAK else ""
KAP = {"y": 8.0, "w": 3.4, "h": 3.7, "kalin": 0.42}
KAM = {"z": 2.3, "egim": 5.0, "lens": 18.0, "sensor": 24.0}
if KAPAK:
    KAM.update({"z": float(arg("--kapak-z", "2.0")), "egim": float(arg("--kapak-egim", "3.0")), "lens": float(arg("--kapak-lens", "16.0"))})
YOL_YARI = 2.6          # yerlesim uyumu (motor serit genisligi); platform bundan dar
PLAT = 1.75             # platform yari genisligi
SU_Z = -0.55            # su yuzeyi platform ustunden bu kadar asagida
SERIT = {
    "p1": {"ana": "#1aa8ff", "acik": "#bfeaff", "koyu": "#0a50d0"},
    "p2": {"ana": "#ff3fb4", "acik": "#ffd0ee", "koyu": "#b0107c"},
}


def kamera(sc):
    rx = math.radians(90 - KAM["egim"])
    bpy.ops.object.camera_add(location=(0, 0, KAM["z"]), rotation=(rx, 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.sensor_fit = "VERTICAL"; kam.data.sensor_height = KAM["sensor"]; kam.data.lens = KAM["lens"]
    kam.data.clip_end = 900
    return kam


def parlat(sc, esik=1.0, boy=7, mix=0.12, saydam=True):
    sc.use_nodes = True; sc.render.use_compositing = True; nt = sc.node_tree; nt.nodes.clear()
    rl = nt.nodes.new("CompositorNodeRLayers"); g = nt.nodes.new("CompositorNodeGlare"); o = nt.nodes.new("CompositorNodeComposite")
    g.glare_type = "FOG_GLOW"; g.quality = "HIGH"; g.threshold = esik; g.size = boy; g.mix = mix
    nt.links.new(rl.outputs["Image"], g.inputs[0]); nt.links.new(g.outputs[0], o.inputs[0])
    if saydam:
        nt.links.new(rl.outputs["Alpha"], o.inputs[1])


def E(ad, renk, guc=1.0):
    return mat_emis(ad, lin(hex3(renk)), guc)


def mat_dikey(ad, alt, ust, z0, z1, guc=1.0, eksen="Z"):
    """emisyon, bir eksende iki ton gecis"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord"); sp = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Object"], sp.inputs[0])
    mr = nt.nodes.new("ShaderNodeMapRange"); mr.inputs["From Min"].default_value = z0; mr.inputs["From Max"].default_value = z1
    nt.links.new(sp.outputs[eksen], mr.inputs["Value"])
    rp = nt.nodes.new("ShaderNodeValToRGB"); nt.links.new(mr.outputs[0], rp.inputs[0])
    rp.color_ramp.elements[0].color = (*lin(hex3(alt)), 1); rp.color_ramp.elements[1].color = (*lin(hex3(ust)), 1)
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs[1].default_value = guc; nt.links.new(rp.outputs[0], em.inputs[0])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], o.inputs[0])
    return m


def mat_su(ad, yakin, uzak, y0, y1, olcek=1.6):
    """havuz suyu: yakindan uzaga turkuaz -> derin mavi + parlak kostik aglari (voronoi kenar mesafesi)"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord"); sp = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Object"], sp.inputs[0])
    mr = nt.nodes.new("ShaderNodeMapRange"); mr.inputs["From Min"].default_value = y0; mr.inputs["From Max"].default_value = y1
    nt.links.new(sp.outputs["Y"], mr.inputs["Value"])
    rp = nt.nodes.new("ShaderNodeValToRGB"); nt.links.new(mr.outputs[0], rp.inputs[0])
    rp.color_ramp.elements[0].color = (*lin(hex3(yakin)), 1); rp.color_ramp.elements[1].color = (*lin(hex3(uzak)), 1)
    vo = nt.nodes.new("ShaderNodeTexVoronoi"); vo.feature = "DISTANCE_TO_EDGE"; vo.inputs["Scale"].default_value = olcek
    ns = nt.nodes.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value = 2.0
    bz = nt.nodes.new("ShaderNodeVectorMath"); bz.operation = "ADD"
    nt.links.new(tc.outputs["Object"], bz.inputs[0]); nt.links.new(ns.outputs["Color"], bz.inputs[1])
    nt.links.new(bz.outputs[0], vo.inputs["Vector"])
    kr = nt.nodes.new("ShaderNodeMapRange"); kr.inputs["From Min"].default_value = 0.0; kr.inputs["From Max"].default_value = 0.06
    kr.inputs["To Min"].default_value = 0.85; kr.inputs["To Max"].default_value = 0.0
    nt.links.new(vo.outputs["Distance"], kr.inputs["Value"])
    mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"; mx.inputs[7].default_value = (*lin(hex3("#e8fbff")), 1)
    nt.links.new(kr.outputs[0], mx.inputs[0]); nt.links.new(rp.outputs[0], mx.inputs[6])
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs[1].default_value = 1.0; nt.links.new(mx.outputs[2], em.inputs[0])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], o.inputs[0])
    return m


def _sekil(ad, noktalar, mat, z=0.0):
    me = bpy.data.meshes.new(ad)
    me.from_pydata([(a, b, z) for a, b in noktalar], [], [list(range(len(noktalar)))]); me.update()
    o = bpy.data.objects.new(ad, me); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat)
    return o


def dik_sekil(ad, noktalar, mat, y):
    """XZ duzleminde (kameraya donuk) cokgen"""
    me = bpy.data.meshes.new(ad)
    me.from_pydata([(a, y, b) for a, b in noktalar], [], [list(range(len(noktalar)))]); me.update()
    o = bpy.data.objects.new(ad, me); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat)
    return o


# ------------------------------------------------------------------ GOK: ortografik; x -960..960, z 0..1080
def mat_gok():
    """gunduz gogu: tepede doygun mavi, ufka dogru acik camgobegi"""
    return mat_dikey("gok", "#bdeeff", "#2a94ff", 300, 1080, 1.0, eksen="Z")


def bulut(cx, cz, rr, rnd, mats, y=420):
    for _ in range(9):
        k = kure((cx + rnd.uniform(-rr * 1.4, rr * 1.4), y + rnd.uniform(-20, 20), cz + rnd.uniform(-rr * 0.25, rr * 0.45)),
                 rnd.uniform(rr * 0.45, rr * 0.85), rnd.choice(mats), sub=3)
        k.scale = (1.25, 0.4, 0.85)


def isik_kulesi(x, z0, z1, y, rnd):
    """kafes isik kulesi + ustte 3x4 spot paneli (beyaz ampuller) + asagi dogru yumusak isik huzmesi"""
    gri = E("kule", "#dfe6f2", 1.0); koyu_ = E("kule_k", "#6a7a96", 1.0)
    for dx in (-22, 22):
        boru((x + dx, y, z0), (x + dx, y, z1), 5, gri)
    z = z0
    while z < z1 - 30:
        boru((x - 22, y, z), (x + 22, y, z + 40), 2.5, koyu_); boru((x + 22, y, z), (x - 22, y, z + 40), 2.5, koyu_); z += 40
    yuvarlak_kutu("spot_panel", (x, y - 6, z1 + 40), (150, 12, 100), E("spot_k", "#2a3550", 1.0), egim=4, seg=2)
    amp = E("ampul", "#fffbe8", 4.0)
    for i in range(4):
        for j in range(3):
            kure((x - 54 + i * 36, y - 16, z1 + 10 + j * 30), 12, amp, sub=2)
    huz = mat_kristal_huzme()
    me = bpy.data.meshes.new("huzme")
    me.from_pydata([(x - 70, y - 20, z1), (x + 70, y - 20, z1), (x * 0.35 + 260, y - 20, 300), (x * 0.35 - 260, y - 20, 300)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("huzme", me); bpy.context.collection.objects.link(o); o.data.materials.append(huz)


def mat_kristal_huzme():
    m = bpy.data.materials.new("huzme"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs[0].default_value = (*lin(hex3("#fffbe0")), 1); em.inputs[1].default_value = 1.0
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mx = nt.nodes.new("ShaderNodeMixShader"); mx.inputs[0].default_value = 0.16
    nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(mx.outputs[0], o.inputs[0])
    return m


def tribun(rnd):
    """kademeli renkli tribun + seyirci (renkli govde + ten kafa), aralarda pankart bezleri"""
    kat_renk = ("#ffffff", "#e8f2ff")
    seyirci = [E("sy%d" % i, c, 1.0) for i, c in enumerate(("#ff4a6a", "#ffd23a", "#2ac86a", "#1aa8ff", "#ff8a1a", "#a65aff", "#ff4fc8", "#ffffff"))]
    ten = [E("ten%d" % i, c, 1.0) for i, c in enumerate(("#f6c9a0", "#d89a6a", "#8a5a3a", "#ffe0c0"))]
    for r in range(7):                                    # alttan uste 7 kademe
        z = 300 + r * 46
        yuvarlak_kutu("kat", (0, 380 + r * 10, z - 14), (1980, 30, 26), E("kat%d" % r, kat_renk[r % 2], 1.0), egim=3, seg=1)
        x = -960 + rnd.uniform(0, 20)
        while x < 960:
            if rnd.random() < 0.9:
                g = kure((x, 370 + r * 10, z + 6), rnd.uniform(11, 14), rnd.choice(seyirci), sub=1); g.scale = (1.0, 0.7, 1.15)
                kure((x, 366 + r * 10, z + 26), rnd.uniform(7, 8.5), rnd.choice(ten), sub=1)
                if rnd.random() < 0.18:                   # kol kaldiran seyirci
                    boru((x + 8, 366 + r * 10, z + 14), (x + 14, 366 + r * 10, z + 40), 2.6, rnd.choice(ten))
            x += rnd.uniform(24, 32)
    # tribun ustunde pankart bezleri (yazisiz, renkli seritler)
    for i, (x, c) in enumerate(((-760, "#1aa8ff"), (-380, "#ff3fb4"), (380, "#1aa8ff"), (760, "#ff3fb4"))):
        yuvarlak_kutu("pankart", (x, 352, 640), (240, 6, 46), E("pk%d" % i, c, 1.1), egim=4, seg=1)
        yuvarlak_kutu("pankart_b", (x, 349, 640), (200, 4, 12), E("pkb%d" % i, "#ffffff", 1.2), egim=2, seg=1)


def bayrak_dizisi(x0, x1, z, sark, y, rnd):
    renk = [E("by%d" % i, c, 1.1) for i, c in enumerate(("#ff4a6a", "#ffd23a", "#1aa8ff", "#2ac86a", "#ff4fc8", "#ff8a1a"))]
    ip = E("ip", "#ffffff", 1.0)
    n = 22; onc = None
    for i in range(n + 1):
        q = i / n; x = x0 + (x1 - x0) * q; zz = z - sark * 4 * q * (1 - q)
        if onc:
            boru((onc[0], y, onc[1]), (x, y, zz), 1.6, ip)
            mx_, mz = (onc[0] + x) / 2, (onc[1] + zz) / 2
            dik_sekil("bayrak", [(mx_ - 18, mz), (mx_ + 18, mz), (mx_, mz - 40)], renk[i % len(renk)], y - 2)
        onc = (x, zz)


def sisme_top(x, z, r, y):
    """plaj topu: beyaz + renkli dilimler (iki renk yerine alti dilim: kure + dilim halkalari)"""
    kure((x, y, z), r, E("top_b", "#ffffff", 1.0), sub=3)
    for i, c in enumerate(("#ff4a6a", "#ffd23a", "#1aa8ff")):
        bpy.ops.mesh.primitive_torus_add(major_radius=r * 0.99, minor_radius=r * 0.17, location=(x, y, z),
                                         rotation=(math.radians(90), 0, math.radians(i * 60)))
        bpy.context.active_object.data.materials.append(E("top_%d" % i, c, 1.0))


def dev_ekran(y):
    """tribunun ustunde ortada skor ekrani cercevesi (ici renkli dalga deseni, yazisiz) - motor ustune HUD cizer"""
    yuvarlak_kutu("ekran_c", (0, y, 820), (560, 20, 230), E("ekran_c", "#2a3550", 1.0), egim=10, seg=2)
    yuvarlak_kutu("ekran", (0, y - 12, 820), (520, 4, 196), mat_dikey("ekran_i", "#1aa8ff", "#ff3fb4", -260, 260, 1.4, eksen="X"), egim=4, seg=1)
    boru((-200, y, 700), (-200, y, 520), 8, E("ekran_d", "#dfe6f2", 1.0)); boru((200, y, 700), (200, y, 520), 8, E("ekran_d2", "#dfe6f2", 1.0))


def gok_katmani(ad):
    sc = bos_sahne(w=1920, h=1080, ornek=min(ORNEK, 16))
    bpy.ops.object.camera_add(location=(0, -900, 540), rotation=(math.radians(90), 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.type = "ORTHO"; kam.data.ortho_scale = 1920; kam.data.clip_end = 3000
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 600, 540), rotation=(math.radians(90), 0, 0))
    p = bpy.context.active_object; p.scale = (2000, 1100, 1); bpy.ops.object.transform_apply(scale=True)
    p.data.materials.append(mat_gok())
    rnd = random.Random(24)
    # gunes (sag ust) + hale
    kure((720, 560, 960), 70, E("gunes", "#fff6c8", 3.0), sub=3)
    hl = kure((720, 570, 960), 190, E("hale", "#fff2b0", 0.35), sub=3); hl.scale = (1, 0.1, 1)
    bm = [E("bulut%d" % i, c, g) for i, (c, g) in enumerate((("#ffffff", 1.05), ("#f2f8ff", 1.0), ("#e4f0ff", 0.95)))]
    for (cx_, cz_, rr) in ((-760, 960, 70), (-330, 1010, 55), (120, 950, 60), (480, 1020, 50), (-620, 820, 45), (880, 820, 55)):
        bulut(cx_, cz_, rr, rnd, bm)
    tribun(rnd)
    dev_ekran(330)
    for x in (-880, 880):
        isik_kulesi(x, 300, 860, 300, rnd)
    bayrak_dizisi(-960, -260, 760, 70, 280, rnd); bayrak_dizisi(260, 960, 760, 70, 280, rnd)
    bayrak_dizisi(-960, 960, 1060, 120, 290, rnd)
    for (x, z, r) in ((-560, 900, 34), (330, 880, 28), (-120, 790, 22), (620, 720, 26)):
        sisme_top(x, z, r, 260)
    konf = [E("kf%d" % i, c, 1.3) for i, c in enumerate(("#ff4a6a", "#ffd23a", "#1aa8ff", "#2ac86a", "#ff4fc8"))]
    for _ in range(140):                                  # konfeti: gok bos kalmaz (md. 7)
        x, z = rnd.uniform(-950, 950), rnd.uniform(680, 1070)
        yuvarlak_kutu("kf", (x, 250, z), (rnd.uniform(6, 11), 1, rnd.uniform(3, 6)), rnd.choice(konf), egim=0.5, seg=1).rotation_euler.y = rnd.uniform(0, 3.1)
    if KAPAK:
        sc.view_settings.exposure = POZLAMA
    parlat(sc, esik=1.6, boy=8, mix=0.08, saydam=False)
    yaz(sc, ad)


# ------------------------------------------------------------------ SERIT: havuz + platform + yarisma kapisi
def havuz(R):
    su = mat_su("su", "#3ae0f0", "#0a6ad8", -0.6, KAP["y"] + 6, 1.4)
    _sekil("su", [(-14, -1.0), (14, -1.0), (14, KAP["y"] + 12), (-14, KAP["y"] + 12)], su, z=SU_Z)
    # can simidi + sisme ordek (genel nesne) iki yanda suda
    for (x, y) in ((-3.3, 2.4), (3.4, 4.6), (-3.6, 6.8)):
        bpy.ops.mesh.primitive_torus_add(major_radius=0.42, minor_radius=0.13, location=(x, y, SU_Z + 0.05))
        o = bpy.context.active_object; o.data.materials.append(E("simit", "#ff3a4a", 1.0))
        for i in range(4):
            a = i * math.pi / 2 + 0.4
            kk = kure((x + 0.42 * math.cos(a), y + 0.42 * math.sin(a), SU_Z + 0.08), 0.15, E("simit_b", "#ffffff", 1.1), sub=2); kk.scale = (1, 1, 0.8)
    for (x, y) in ((3.2, 1.6), (-3.0, 4.3)):
        g = kure((x, y, SU_Z + 0.2), 0.28, E("ordek", "#ffd23a", 1.1), sub=2); g.scale = (1.25, 1, 0.8)
        kure((x + 0.18, y, SU_Z + 0.48), 0.17, E("ordek2", "#ffd23a", 1.1), sub=2)
        g = kure((x + 0.36, y, SU_Z + 0.46), 0.07, E("gaga", "#ff8a1a", 1.1), sub=1); g.scale = (1.6, 1, 0.6)


def platform(R):
    """yastikli yarisma platformu: beyaz ust, kenarlarda oyuncu renginde yuvarlak yastiklar, ustte renkli ok; ayaklar suya iner"""
    ust = mat_dikey("plat", "#ffffff", R["acik"], -0.6, KAP["y"], 1.0, eksen="Y")
    yuvarlak_kutu("plat", (0, (KAP["y"] - 0.6) / 2 - 0.3, -0.16), (PLAT * 2, KAP["y"] + 0.6, 0.32), ust, egim=0.06, seg=2)
    yastik = (E("yastik_a", R["ana"], 1.0), E("yastik_b", "#ffffff", 1.05))
    for s in (-1, 1):
        y = -0.6; i = 0
        while y < KAP["y"]:
            boru((s * PLAT, y, 0.0), (s * PLAT, min(KAP["y"], y + 0.9), 0.0), 0.16, yastik[i % 2]); y += 0.9; i += 1
        for yy in (0.6, 3.0, 5.4, 7.6):                    # ayaklar
            boru((s * (PLAT - 0.3), yy, -0.3), (s * (PLAT - 0.3), yy, SU_Z - 0.4), 0.09, E("ayak", "#c8d4e6", 1.0))
    ok = E("ok", R["ana"], 1.15); ok_k = E("ok_k", R["koyu"], 1.0)
    for y in (0.9, 2.8, 4.6, 6.2):                          # yerde yon oklari (seri sabiti)
        nok = [(-0.9, y - 0.5), (0, y), (0.9, y - 0.5), (0.9, y - 0.85), (0, y - 0.35), (-0.9, y - 0.85)]
        _sekil("ok_k", [(a, b - 0.06) for a, b in nok], ok_k, z=0.003)
        _sekil("ok", nok, ok, z=0.006)


def kapi(R):
    """yarisma kapisi: kalin renkli cerceve, cevresinde ampul dizisi, ustte bos tabela (motor PLAYER n yazar), iki yanda sisme sutun"""
    Y, W_, H_, K = KAP["y"], KAP["w"], KAP["h"], KAP["kalin"]
    cer = mat_dikey("cerceve", R["koyu"], R["ana"], 0.0, H_ + 1.0, 1.15)
    xk = W_ / 2 + K / 2
    for s in (-1, 1):
        yuvarlak_kutu("direk", (s * xk, Y, (H_ + K) / 2), (K, K, H_ + K), cer, egim=0.08, seg=3)
    yuvarlak_kutu("kiris", (0, Y, H_ + K / 2), (W_ + 2 * K, K, K), cer, egim=0.08, seg=3)
    amp = E("ampul", "#fff6d0", 3.2)
    n = 9
    for s in (-1, 1):
        for i in range(n):
            kure((s * xk, Y - K / 2 - 0.02, 0.25 + i * (H_ - 0.1) / (n - 1)), 0.075, amp, sub=1)
    for i in range(11):
        kure((-xk + i * (2 * xk) / 10, Y - K / 2 - 0.02, H_ + K / 2), 0.075, amp, sub=1)
    # tabela (yildizli, yazisiz)
    yuvarlak_kutu("tabela", (0, Y - 0.05, H_ + K + 0.55), (W_ * 0.9, 0.12, 0.8), E("tabela", "#ffffff", 1.05), egim=0.12, seg=3)
    yuvarlak_kutu("tabela_c", (0, Y + 0.02, H_ + K + 0.55), (W_ * 0.9 + 0.2, 0.08, 1.0), E("tabela_c", R["ana"], 1.1), egim=0.14, seg=3)
    for s in (-1, 1):                                       # sisme sutunlar (renkli halkali)
        x = s * (xk + K / 2 + 0.55)
        for j in range(6):
            k = kure((x, Y, 0.35 + j * 0.62), 0.42, E("sisme%d" % (j % 2), (R["ana"], "#ffd23a")[j % 2], 1.05), sub=2); k.scale = (1, 1, 0.8)
        kure((x, Y, 0.35 + 6 * 0.62), 0.32, E("sisme_t", "#ffffff", 1.1), sub=2)
    # kapi arkasi: kart acikligi koyu degil, acik pastel perde (motor karti uzerine cizer)
    dik_sekil("perde", [(-W_ / 2, 0), (W_ / 2, 0), (W_ / 2, H_), (-W_ / 2, H_)], E("perde", R["acik"], 1.0), Y + 0.1)


def serit_katmani(oyuncu):
    R = SERIT[oyuncu]
    sc = bos_sahne(w=960, h=1080, saydam=True, ornek=min(ORNEK, 24))
    sc.cycles.transparent_max_bounces = 24
    kam = kamera(sc)
    havuz(R); platform(R); kapi(R)
    Y, W_, H_ = KAP["y"], KAP["w"], KAP["h"]
    ic = W_ / 2
    bpy.context.view_layer.update()
    px = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-ic, Y, 0), (ic, Y, 0), (-ic, Y, H_), (ic, Y, H_))]
    xs = [p.x * 960 for p in px]; ys = [(1 - p.y) * 1080 for p in px]
    YERLESIM["aciklik_" + oyuncu] = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
    # OUT ani icin: platform kenari ve su yuzeyinin ekrandaki yeri (yakin plan y=1.5'te)
    pk = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-PLAT, 1.5, 0), (PLAT, 1.5, 0), (0, 1.5, SU_Z), (0, Y - 0.6, 0))]
    YERLESIM["havuz_" + oyuncu] = {"plat_sol_x": round(pk[0].x * 960, 1), "plat_sag_x": round(pk[1].x * 960, 1),
                                  "plat_y": round((1 - pk[0].y) * 1080, 1), "su_y": round((1 - pk[2].y) * 1080, 1),
                                  "kapi_onu_y": round((1 - pk[3].y) * 1080, 1)}
    YERLESIM["yol"] = {"y_kapi": Y, "genislik": YOL_YARI * 2, "kam": KAM, "serit_w": 960}
    log("aciklik", oyuncu, YERLESIM["aciklik_" + oyuncu], YERLESIM["havuz_" + oyuncu])
    if KAPAK:
        sc.view_settings.exposure = POZLAMA
    parlat(sc, esik=1.8, boy=6, mix=0.08)
    yaz(sc, ON_EK + "serit-%s.png" % oyuncu)


def panel(oyuncu):
    sc = bos_sahne(w=1100, h=904, saydam=True, ornek=4)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0), rotation=(math.radians(90), 0, 0))
    p = bpy.context.active_object; p.scale = (6, 6, 1); bpy.ops.object.transform_apply(scale=True)
    p.data.materials.append(mat_emis("p", (1, 1, 1), 1.0))
    bpy.ops.object.camera_add(location=(0, -10, 0), rotation=(math.radians(90), 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.type = "ORTHO"; kam.data.ortho_scale = 5
    yaz(sc, "panel-%s.png" % oyuncu)


if KAPAK:
    gok_katmani("kapak-gok.png")
    for o_ in ("p1", "p2"):
        serit_katmani(o_)
if YALNIZ in ("hepsi", "poz"):
    poz_maskeleri()
if YALNIZ in ("hepsi", "sahne"):
    gok_katmani("gok.png")
    for o_ in ("p1", "p2"):
        serit_katmani(o_)
        panel(o_)
json.dump(YERLESIM, open(os.path.join(CIKTI, "yerlesim.json"), "w"), indent=1)
log("bitti (havuz)", YERLESIM.get("aciklik_p1"), YERLESIM.get("aciklik_p2"))
