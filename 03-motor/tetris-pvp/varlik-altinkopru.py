"""HUMAN TETRIS 14. video (REF-065 HumanWarmUp, 1v1) - ALTIN KOPRU sahne varliklari, IKI serit. varlik.py calistirir (--mod altinkopru).

REF-065'te ne varsa (md. 22): iki yari ayri kamerali; ortadaki V korkuluk iki yarinin birlesiminden dogar. Bakir-altin plaka zemin,
parlak sari chevron basamaklar, altin korkuluk + kenarda LED sira, gumus kafes kapi, kapi arkasinda ic ice neon ucgen, dev capraz isinlar.
Olculer referans karesinden (t=45 sn, 1080p'ye cevrildi): ufuk y~570, kapi tabani y~735, tepesi y~330, kapi genisligi ~445 px.
"Coming Soon", "!", duvarlar, VS cubugu ve gokun renk gecisi motorda.

Ciktilar:
  gok.png            1920x1080  mor-mavi gok (opak)
  gok2.png           1920x1080  ayni gok, kirmizi (REF-065 acilis gogu); motor gecis yapar
  serit-p1/p2.png    960x1080   zemin, chevron, korkuluk, kafes kapi (gokte saydam)
  panel-p1/p2.png    1100x904   duz renk duvar; renk motorda duvar basina degisir
"""

import random
YERLESIM.clear()
KAP = {"y": 8.6, "w": 4.72, "h": 3.95, "kule": 0.42}
KAM = {"z": 1.75, "egim": -2.1, "lens": 18.0, "sensor": 24.0}
YOL_YARI = 2.36
KORK_Z = 1.42
KAPAK = YALNIZ == "kapak"
POZLAMA = float(arg("--kapak-pozlama", "0"))
ON_EK = "kapak-" if KAPAK else ""
if KAPAK:   # REF-065 kapagi (1280x720): kapi 260x235 px, tepesi y~205, tabani y~440
    KAM["lens"] = 15.7; KAM["egim"] = 1.9


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


def sekil(ad, noktalar, mat, z=0.0):
    me = bpy.data.meshes.new(ad)
    me.from_pydata([(a, b, z) for a, b in noktalar], [], [list(range(len(noktalar)))]); me.update()
    o = bpy.data.objects.new(ad, me); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat)
    return o


def mat_kat(ad, renk, guc):
    """eklemeli (additive) isik: duz bant yerine sisli hale, altindaki rengi ortmez"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs[0].default_value = (*renk, 1); em.inputs[1].default_value = guc
    tr = nt.nodes.new("ShaderNodeBsdfTransparent"); ad_ = nt.nodes.new("ShaderNodeAddShader")
    nt.links.new(em.outputs[0], ad_.inputs[0]); nt.links.new(tr.outputs[0], ad_.inputs[1])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(ad_.outputs[0], o.inputs[0])
    return m


def parlat(sc, esik=1.0, boy=8):
    """REF-065 neonu hale ile yanar: duz cizgi ilk denemede cansiz kaldi -> Blender compositor fog glow"""
    sc.use_nodes = True; sc.render.use_compositing = True; nt = sc.node_tree; nt.nodes.clear()
    rl = nt.nodes.new("CompositorNodeRLayers"); g = nt.nodes.new("CompositorNodeGlare"); o = nt.nodes.new("CompositorNodeComposite")
    g.glare_type = "FOG_GLOW"; g.quality = "HIGH"; g.threshold = esik; g.size = boy; g.mix = 0.15
    nt.links.new(rl.outputs["Image"], g.inputs[0]); nt.links.new(g.outputs[0], o.inputs[0]); nt.links.new(rl.outputs["Alpha"], o.inputs[1])


# ------------------------------------------------------------------ GOK: ortografik duz resim; x -960..960, z 0..1080
def gok_cizgi(a, b, r, m):
    boru((a[0], 0, a[1]), (b[0], 0, b[1]), r, m)


def ucgen(cx_, taban, tepe, yari, r, m):
    gok_cizgi((cx_ - yari, taban), (cx_, tepe), r, m)
    gok_cizgi((cx_, tepe), (cx_ + yari, taban), r, m)
    gok_cizgi((cx_ + yari, taban), (cx_ - yari, taban), r, m)


def gok_katmani(ad, zemin_alt, zemin_ust, isin):
    """isin = (kenar, ic1, ic2, kesik): ayni kompozisyon, iki renk ailesi"""
    sc = bos_sahne(w=1920, h=1080, ornek=min(ORNEK, 24))
    bpy.ops.object.camera_add(location=(0, -600, 540), rotation=(math.radians(90), 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.type = "ORTHO"; kam.data.ortho_scale = 1920; kam.data.clip_end = 3000
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)
    nt = sc.world.node_tree
    zem = bpy.data.materials.new("zemin"); zem.use_nodes = True; n2 = zem.node_tree; n2.nodes.clear()
    tc = n2.nodes.new("ShaderNodeTexCoord"); sp = n2.nodes.new("ShaderNodeSeparateXYZ"); rp = n2.nodes.new("ShaderNodeValToRGB")
    n2.links.new(tc.outputs["Object"], sp.inputs[0])
    nz = n2.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 0.006; nz.inputs["Detail"].default_value = 6
    n2.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    nm = n2.nodes.new("ShaderNodeMapRange"); nm.inputs["From Min"].default_value = 0.3; nm.inputs["From Max"].default_value = 0.7; nm.inputs["To Min"].default_value = 0.35; nm.inputs["To Max"].default_value = 1.9
    n2.links.new(nz.outputs["Fac"], nm.inputs["Value"])
    mr = n2.nodes.new("ShaderNodeMapRange"); mr.inputs["From Min"].default_value = -540; mr.inputs["From Max"].default_value = 540
    n2.links.new(sp.outputs["Z"], mr.inputs["Value"]); n2.links.new(mr.outputs[0], rp.inputs[0])
    cr = rp.color_ramp
    cr.elements[0].position = 0.28; cr.elements[0].color = (*lin(hex3(zemin_alt)), 1)
    cr.elements[1].position = 0.95; cr.elements[1].color = (*lin(hex3(zemin_ust)), 1)
    em = n2.nodes.new("ShaderNodeEmission"); n2.links.new(rp.outputs[0], em.inputs[0]); n2.links.new(nm.outputs[0], em.inputs[1])
    o = n2.nodes.new("ShaderNodeOutputMaterial"); n2.links.new(em.outputs[0], o.inputs[0])
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 400, 540), rotation=(math.radians(90), 0, 0))
    p = bpy.context.active_object; p.scale = (2000, 1100, 1); bpy.ops.object.transform_apply(scale=True)
    p.data.materials.append(zem)
    kenar, ic1, ic2, kesik = [mat_emis("n%d" % i, lin(hex3(c)), g) for i, (c, g) in enumerate(zip(isin, (5.5, 5.0, 5.0, 4.0)))]
    beyaz = mat_emis("beyaz", lin(hex3("#fff4ff")), 7.0)
    sc.cycles.transparent_max_bounces = 64
    sisler = [mat_kat("sis%d" % i, lin(hex3(isin[0])), g) for i, g in enumerate((0.05, 0.08, 0.12, 0.2))]
    rnd = random.Random(65)
    for cx_ in (-480, 480):                                # her oyuncunun arkasinda ic ice neon ucgen ve dev kollar
        for s in (-1, 1):
            gok_cizgi((cx_ + s * 480, 420), (cx_ + s * 40, 1110), 9.0, kenar)
            for r_, m_ in zip((48, 32, 21, 13), sisler):   # kolun cevresinde kademeli sis
                gok_cizgi((cx_ + s * 480, 420), (cx_ + s * 40, 1110), r_, m_)
            gok_cizgi((cx_ + s * 330, 470), (cx_ + s * 20, 1040), 4.0, beyaz)
            for j in range(7):                             # kesik cizgili ikinci kol
                q0 = 0.08 + j * 0.13; q1 = q0 + 0.07
                gok_cizgi((cx_ + s * lerp_(250, 40, q0), lerp_(470, 1060, q0)), (cx_ + s * lerp_(250, 40, q1), lerp_(470, 1060, q1)), 5.0, kesik)
        ucgen(cx_, 395, 800, 225, 4.2, ic1)
        ucgen(cx_, 400, 720, 160, 3.8, ic2)
        ucgen(cx_, 405, 650, 105, 3.4, ic1)
        for j in range(6):                                 # ucgenin altinda su gibi parlayan yansima bantlari
            z = 340 + j * 14; g_ = 150 + j * 28
            boru((cx_ - g_, 0, z), (cx_ + g_, 0, z), 10.0 - j, sisler[j % 4])
        for j in range(9):                                 # ufukta yansiyan neon bantlar (referansta ucgenin parlak yansimasi)
            x = cx_ - 240 + j * 60
            boru((x, 0, 395 - j % 3 * 14), (x + 34, 0, 395 - j % 3 * 14), 2.6, beyaz if j % 2 else ic2)
    for z, r_, m_ in ((405, 70, sisler[0]), (400, 46, sisler[0]), (395, 26, sisler[1])):   # ufuk boyunca sis bandi
        boru((-980, 120, z), (980, 120, z), r_, m_)
    for _ in range(90):                                    # isik tozu
        x, z = rnd.uniform(-960, 960), rnd.uniform(420, 1080)
        kure((x, 0, z), rnd.choice((1.2, 1.8, 2.6, 4.0)), beyaz, sub=1)
    if KAPAK:
        palmiye()
        sc.view_settings.exposure = POZLAMA
    parlat(sc, esik=1.0, boy=9)
    yaz(sc, ad)


def palmiye():
    """REF-065 kapagi: kenarlarda koyu palmiye siluetleri (videoda yok)"""
    koyu = mat_emis("palm", lin(hex3("#1c0610")), 1.0)
    for x, boy in ((-880, 760), (-720, 660), (880, 760), (720, 660)):
        gok_cizgi((x, 380), (x + 18, boy), 7.0, koyu)
        for i in range(9):
            t = i / 9 * 2 * math.pi; ux, uz = math.cos(t), abs(math.sin(t)) * 0.45
            onc = (x + 18, boy)
            for j in range(1, 7):                          # sarkan yaprak
                q = j / 6
                son = (x + 18 + ux * 130 * q, boy + uz * 110 * q - 95 * q * q)
                gok_cizgi(onc, son, 7.5 - j, koyu)
                onc = son


def lerp_(a, b, q):
    return a + (b - a) * q


# ------------------------------------------------------------------ SERIT: tek yari; ayni goruntu iki oyuncuda da kullanilir
def zemin():
    bakir = bpy.data.materials.new("bakir"); bakir.use_nodes = True; n_ = bakir.node_tree; n_.nodes.clear()
    tc_ = n_.nodes.new("ShaderNodeTexCoord"); sp_ = n_.nodes.new("ShaderNodeSeparateXYZ"); n_.links.new(tc_.outputs["Object"], sp_.inputs[0])
    mr_ = n_.nodes.new("ShaderNodeMapRange"); mr_.inputs["From Min"].default_value = 1.0; mr_.inputs["From Max"].default_value = 8.6
    n_.links.new(sp_.outputs["Y"], mr_.inputs["Value"])
    rp_ = n_.nodes.new("ShaderNodeValToRGB"); cr_ = rp_.color_ramp; n_.links.new(mr_.outputs[0], rp_.inputs[0])
    cr_.elements[0].position = 0.0; cr_.elements[0].color = (*lin(hex3("#e08a34")), 1)
    cr_.elements[1].position = 1.0; cr_.elements[1].color = (*lin(hex3("#5a2c0c")), 1)
    em_ = n_.nodes.new("ShaderNodeEmission"); n_.links.new(rp_.outputs[0], em_.inputs[0])
    o_ = n_.nodes.new("ShaderNodeOutputMaterial"); n_.links.new(em_.outputs[0], o_.inputs[0])
    sekil("zemin", [(-YOL_YARI, 4.0), (YOL_YARI, 4.0), (YOL_YARI, KAP["y"]), (-YOL_YARI, KAP["y"])], bakir)
    sekil("zemin2", [(-3.2, -0.5), (3.2, -0.5), (3.2, 4.0), (-3.2, 4.0)], bakir, z=-0.002)
    derz = mat_emis("derz", lin(hex3("#6e3a10")), 1.0)
    for x, y0, y1 in ((-1.55, 4.3, 8.6), (1.55, 4.3, 8.6), (-1.05, 1.0, 4.3), (1.05, 1.0, 4.3)):
        boru((x, y0, 0.006), (x * (0.8 if y1 < 5 else 1), y1, 0.006), 0.012, derz)
    for yy in (2.2, 3.6, 5.2, 6.8):
        boru((-YOL_YARI, yy, 0.006), (YOL_YARI, yy, 0.006), 0.01, derz)
    ic = mat_emis("chev_ic", lin(hex3("#ffb040")), 2.2)
    kenar = mat_emis("chev_k", lin(hex3("#ffe08a")), 5.0)
    hale = [mat_kat("hale%d" % i, lin(hex3("#ff8a1c")), g) for i, g in enumerate((0.05, 0.1))]
    for yy, hw, d, kal in ((1.75, 1.0, 0.72, 0.3), (3.05, 0.86, 0.72, 0.28), (4.2, 0.84, 0.68, 0.26), (5.5, 0.84, 0.62, 0.24), (6.5, 0.84, 0.56, 0.22), (7.3, 0.84, 0.5, 0.2), (8.05, 0.84, 0.3, 0.16)):
        kose = [(-hw, yy + d), (0, yy), (hw, yy + d), (hw, yy + d + kal), (0, yy + kal), (-hw, yy + d + kal)]
        sekil("chev", kose, ic, z=0.01)
        for g_, m_ in ((0.16, hale[0]), (0.09, hale[1])):   # zemine dusen turuncu hale
            for i in range(5):
                boru((*kose[[0, 1, 2, 3, 4][i]], 0.004), (*kose[[1, 2, 3, 4, 5][i]], 0.004), g_, m_)
        for i in range(6):
            boru((*kose[i], 0.015), (*kose[(i + 1) % 6], 0.015), 0.018, kenar)


def korkuluk():
    altin = mat_emis("kork", lin(hex3("#d8842c")), 1.3)
    neon = mat_emis("kork_n", lin(hex3("#ffb04a")), 5.0)
    led = mat_emis("led", lin(hex3("#ffd070")), 7.0)
    serit_m = mat_emis("kork_s", lin(hex3("#ff8a24")), 1.5)
    for s in (-1, 1):
        x = s * YOL_YARI
        y0, y1 = 3.2, KAP["y"]
        for j in range(6):
            yy = y0 + j * (y1 - y0) / 5
            yuvarlak_kutu("dikme", (x, yy, KORK_Z / 2), (0.07, 0.07, KORK_Z), altin, egim=0.02, seg=2)
        boru((x, y0, KORK_Z), (x, y1, KORK_Z), 0.05, neon)
        for z in (KORK_Z * 0.74, KORK_Z * 0.5, KORK_Z * 0.28):
            boru((x, y0, z), (x, y1, z), 0.024, altin)
        for z, dx in ((0.03, 0.0), (0.16, 0.05), (0.3, 0.1)):   # REF-065: korkuluk dibinde kademeli isikli raf
            boru((x + s * dx, y0, z), (x + s * dx, y1, z), 0.035, serit_m)
        for j in range(int((y1 - y0) / 0.32)):             # korkuluk dibinde LED sira
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.04, location=(x - s * 0.1, y0 + j * 0.32, 0.05), segments=10, ring_count=6)
            bpy.context.active_object.data.materials.append(led)


def kapi():
    Y, W_, H_, KK = KAP["y"], KAP["w"], KAP["h"], KAP["kule"]
    ana = mat_metal("kapi_ana", lin(hex3("#c4c6d0")), 0.28, metal=0.7)
    ince = mat_metal("kapi_ince", lin(hex3("#9498a6")), 0.35, metal=0.7)
    xk = W_ / 2 - KK / 2
    for s in (-1, 1):
        kafes_kule(s * xk, Y, 0.0, H_ + KK, KK, ana, ince)
    kafes_kiris(-xk, xk, Y, H_ + KK / 2, KK, ana, ince)


def serit_katmani(oyuncu):
    sc = bos_sahne(w=960, h=1080, saydam=True, ornek=min(ORNEK, 64))
    sc.cycles.transparent_max_bounces = 32
    kam = kamera(sc)
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (*lin(hex3("#e8dcff")), 1)
    sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.3
    zemin(); korkuluk(); kapi()
    Y, W_, H_, KK = KAP["y"], KAP["w"], KAP["h"], KAP["kule"]
    isik("AREA", (0, 3, 6), 260, lin(hex3("#ffe0b0")), 8, yon=(0, 6, 0))
    isik("AREA", (0, Y - 3, 6), 900, lin(hex3("#ffffff")), 5, yon=(0, Y, 2))
    ic = W_ / 2 - KK
    bpy.context.view_layer.update()
    px = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-ic, Y, 0), (ic, Y, 0), (-ic, Y, H_), (ic, Y, H_))]
    xs = [p.x * 960 for p in px]; ys = [(1 - p.y) * 1080 for p in px]
    YERLESIM["aciklik_" + oyuncu] = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
    YERLESIM["ampul_" + oyuncu] = []
    for i in range(15):                                    # ust kiris altinda ampul dizisi; motor yakip sondurur
        q = world_to_camera_view(sc, kam, Vector((-ic + i * 2 * ic / 14, Y - 0.3, H_ - 0.02)))
        YERLESIM["ampul_" + oyuncu].append([round(q.x * 960, 1), round((1 - q.y) * 1080, 1)])
    YERLESIM["yol"] = {"y_kapi": Y, "genislik": YOL_YARI * 2, "kam": KAM, "serit_w": 960}
    log("aciklik", oyuncu, YERLESIM["aciklik_" + oyuncu])
    if KAPAK:
        sc.view_settings.exposure = POZLAMA
    parlat(sc, esik=1.0, boy=8)
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
    gok_katmani("kapak-gok.png", "#7a1430", "#2a0612", ("#ffc040", "#ff40a0", "#ffe060", "#ffd060"))
    serit_katmani("p1")
if YALNIZ in ("hepsi", "poz"):
    poz_maskeleri()
if YALNIZ in ("hepsi", "sahne"):
    gok_katmani("gok.png", "#7a3ad8", "#1c0e6a", ("#c040ff", "#ff40c8", "#30d8ff", "#50e8ff"))
    gok_katmani("gok2.png", "#d8285a", "#5a0a2a", ("#ffc040", "#ff40a0", "#ffe060", "#ffd060"))
    for o_ in ("p1", "p2"):
        serit_katmani(o_)
        panel(o_)
json.dump(YERLESIM, open(os.path.join(CIKTI, "yerlesim.json"), "w"), indent=1)
log("bitti (altinkopru)", YERLESIM.get("aciklik_p1"))
