"""HUMAN TETRIS 9. video (REF-060, 1v1) - UZAY sahne varliklari (Blender, GitHub Actions).

varlik.py tarafindan calistirilir (yardimcilar oradan gelir):
    blender -b --factory-startup -noaudio -P 03-motor/tetris-pvp/varlik.py -- --mod uzay --renk1 FF3EA5 --renk2 2E9BFF \
        --cikti cikti [--ornek 64] [--yalniz sahne] [--pozlar 03-motor/tetris-pvp/pozlar-09.json]

REF-060'da ne varsa (CLAUDE.md md. 22): kara uzay + yildiz tozu, ortada dev YANARDONER gezegen kuresi (gokkusagi girdapli,
isiltili), cevresinde galaksi sarmali halkasi, renkli isik noktalari · her oyuncunun seridi = PELUS (tuylu) zemin + isikli
beyaz pelus chevron'lar + pelus korkuluk + BLOK/CIVATA desenli KAFES (truss) kapi · duvar paneli = duz isin patlamasi +
yildiz deseni (pastel oyuncu rengi). P1 pembe solda, P2 mavi sagda, mor ortak vurgu (kullanici, 24 Eki 2026).
Pelus yardimcilari (mat_tuy, tuylu, yildiz_mesh) varlik-disko.py'den alinir.

Ciktilar (sahne4.html 2B'de birlestirir, kamera sabit):
  gok.png            1920x1080  uzay + gezegen + galaksi halkasi + isik noktalari (opak)
  serit-p1/p2.png    960x1080   pelus zemin, chevron, korkuluk, kafes kapi (gokte saydam)
  panel-p1/p2.png    1100x904   yildizli isin patlamasi
  poz/<ad>.png       --yalniz hepsi|poz ise (varlik.py poz_maskeleri)
  yerlesim.json      aciklik_p1/p2, ampul_p1/p2 (kapi cercevesindeki parilti noktalari - motor yakip sondurur)
"""

_disko = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "varlik-disko.py"), encoding="utf-8").read()
exec(compile(_disko.split("# ------------------------------------------------------------------ GOK:")[0], "varlik-disko.py", "exec"))
MOR = "#9b5cff"


def mat_desen(ad, kur):
    """emisyon malzemesi; kur(nt, tc) -> renk cikisi"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord")
    em = nt.nodes.new("ShaderNodeEmission"); nt.links.new(kur(nt, tc), em.inputs[0])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], o.inputs[0])
    return m, nt, em


def rampa(nt, girdi, duraklar):
    rp = nt.nodes.new("ShaderNodeValToRGB"); cr = rp.color_ramp
    cr.elements[0].position = duraklar[0][0]; cr.elements[0].color = (*lin(hex3(duraklar[0][1])), 1)
    cr.elements[1].position = duraklar[-1][0]; cr.elements[1].color = (*lin(hex3(duraklar[-1][1])), 1)
    for p, c in duraklar[1:-1]:
        e = cr.elements.new(p); e.color = (*lin(hex3(c)), 1)
    nt.links.new(girdi, rp.inputs[0])
    return rp.outputs[0]


# ------------------------------------------------------------------ GOK: uzay + yanardoner gezegen + galaksi halkasi
def gezegen(merkez, R):
    """REF-060 gezegeni: gokkusagi girdaplari (camgobegi / pembe / mor / altin) + ince isilti benekleri"""
    def kur(nt, tc):
        dl = nt.nodes.new("ShaderNodeTexWave"); dl.wave_type = "BANDS"; dl.bands_direction = "DIAGONAL"
        dl.inputs["Scale"].default_value = 1.6; dl.inputs["Distortion"].default_value = 9.0
        dl.inputs["Detail"].default_value = 4.0; dl.inputs["Detail Scale"].default_value = 1.5
        nt.links.new(tc.outputs["Object"], dl.inputs["Vector"])
        renk = rampa(nt, dl.outputs["Fac"], [(0.0, "#0a2a6a"), (0.18, "#25e6ff"), (0.36, "#ff4fc3"), (0.52, "#8a4dff"),
                                                (0.68, "#ffd25a"), (0.84, "#3fffd2"), (1.0, "#1a3fb0")])
        vr = nt.nodes.new("ShaderNodeTexVoronoi"); vr.inputs["Scale"].default_value = 140.0
        nt.links.new(tc.outputs["Object"], vr.inputs["Vector"])
        bn = nt.nodes.new("ShaderNodeMath"); bn.operation = "LESS_THAN"; bn.inputs[1].default_value = 0.07
        nt.links.new(vr.outputs["Distance"], bn.inputs[0])
        mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"; mx.blend_type = "ADD"
        nt.links.new(bn.outputs[0], mx.inputs[0]); nt.links.new(renk, mx.inputs[6])
        mx.inputs[7].default_value = (1.2, 1.2, 1.3, 1)
        return mx.outputs[2]
    m, nt, em = mat_desen("gezegen", kur); em.inputs[1].default_value = 2.1
    bpy.ops.mesh.primitive_uv_sphere_add(radius=R, location=merkez, segments=96, ring_count=48)
    g = bpy.context.active_object; g.data.materials.append(m); bpy.ops.object.shade_smooth()
    g.rotation_euler = (0.4, 0.2, 0.7)
    # kenarda ince isilti halesi (REF-060 gezegeninin kenari parlak)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=R * 1.035, location=merkez, segments=64, ring_count=32)
    h = bpy.context.active_object; bpy.ops.object.shade_smooth()
    hm = bpy.data.materials.new("hale"); hm.use_nodes = True; hn = hm.node_tree; hn.nodes.clear()
    lw = hn.nodes.new("ShaderNodeLayerWeight"); lw.inputs[0].default_value = 0.25
    e2 = hn.nodes.new("ShaderNodeEmission"); e2.inputs[0].default_value = (*lin(hex3("#9fe8ff")), 1); e2.inputs[1].default_value = 3.0
    tr = hn.nodes.new("ShaderNodeBsdfTransparent"); mx2 = hn.nodes.new("ShaderNodeMixShader")
    hn.links.new(lw.outputs["Facing"], mx2.inputs[0]); hn.links.new(tr.outputs[0], mx2.inputs[1]); hn.links.new(e2.outputs[0], mx2.inputs[2])
    o2 = hn.nodes.new("ShaderNodeOutputMaterial"); hn.links.new(mx2.outputs[0], o2.inputs[0])
    hm.blend_method = "BLEND"; h.data.materials.append(hm)


def galaksi_halkasi(merkez, R):
    """gezegenin arkasinda egik galaksi sarmali: log-sarmal kollar x gurultu, kenara dogru sonen, saydam disk"""
    m = bpy.data.materials.new("galaksi"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sp = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Object"], sp.inputs[0])
    at = nt.nodes.new("ShaderNodeMath"); at.operation = "ARCTAN2"
    nt.links.new(sp.outputs["Y"], at.inputs[0]); nt.links.new(sp.outputs["X"], at.inputs[1])
    uz = nt.nodes.new("ShaderNodeVectorMath"); uz.operation = "LENGTH"; nt.links.new(tc.outputs["Object"], uz.inputs[0])
    lg = nt.nodes.new("ShaderNodeMath"); lg.operation = "LOGARITHM"; lg.inputs[1].default_value = 2.718
    nt.links.new(uz.outputs["Value"], lg.inputs[0])
    m1 = nt.nodes.new("ShaderNodeMath"); m1.operation = "MULTIPLY"; m1.inputs[1].default_value = 2.0   # iki kol
    nt.links.new(at.outputs[0], m1.inputs[0])
    m2 = nt.nodes.new("ShaderNodeMath"); m2.operation = "MULTIPLY"; m2.inputs[1].default_value = -6.0
    nt.links.new(lg.outputs[0], m2.inputs[0])
    t1 = nt.nodes.new("ShaderNodeMath"); t1.operation = "ADD"; nt.links.new(m1.outputs[0], t1.inputs[0]); nt.links.new(m2.outputs[0], t1.inputs[1])
    sn = nt.nodes.new("ShaderNodeMath"); sn.operation = "SINE"; nt.links.new(t1.outputs[0], sn.inputs[0])
    kol = nt.nodes.new("ShaderNodeMapRange"); kol.inputs["From Min"].default_value = 0.2; kol.inputs["To Min"].default_value = 0.0
    nt.links.new(sn.outputs[0], kol.inputs["Value"])
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 9.0; nz.inputs["Detail"].default_value = 6
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    vr = nt.nodes.new("ShaderNodeTexVoronoi"); vr.inputs["Scale"].default_value = 60.0
    nt.links.new(tc.outputs["Object"], vr.inputs["Vector"])
    yl = nt.nodes.new("ShaderNodeMath"); yl.operation = "LESS_THAN"; yl.inputs[1].default_value = 0.09
    nt.links.new(vr.outputs["Distance"], yl.inputs[0])
    # yogunluk = kol * gurultu + yildiz benekleri; kenar sonumu
    k1 = nt.nodes.new("ShaderNodeMath"); k1.operation = "MULTIPLY"; nt.links.new(kol.outputs[0], k1.inputs[0]); nt.links.new(nz.outputs["Fac"], k1.inputs[1])
    k2 = nt.nodes.new("ShaderNodeMath"); k2.operation = "ADD"; nt.links.new(k1.outputs[0], k2.inputs[0]); nt.links.new(yl.outputs[0], k2.inputs[1])
    ks = nt.nodes.new("ShaderNodeMapRange"); ks.inputs["From Min"].default_value = R * 0.95; ks.inputs["From Max"].default_value = R * 0.35
    nt.links.new(uz.outputs["Value"], ks.inputs["Value"])
    ic = nt.nodes.new("ShaderNodeMapRange"); ic.inputs["From Min"].default_value = R * 0.18; ic.inputs["From Max"].default_value = R * 0.3
    nt.links.new(uz.outputs["Value"], ic.inputs["Value"])
    s1 = nt.nodes.new("ShaderNodeMath"); s1.operation = "MULTIPLY"; nt.links.new(k2.outputs[0], s1.inputs[0]); nt.links.new(ks.outputs[0], s1.inputs[1])
    s2 = nt.nodes.new("ShaderNodeMath"); s2.operation = "MULTIPLY"; nt.links.new(s1.outputs[0], s2.inputs[0]); nt.links.new(ic.outputs[0], s2.inputs[1])
    s2.use_clamp = True
    renk = rampa(nt, nz.outputs["Fac"], [(0.3, "#4fd8ff"), (0.5, "#c06bff"), (0.7, "#ff6ad0")])
    e = nt.nodes.new("ShaderNodeEmission"); e.inputs[1].default_value = 4.0; nt.links.new(renk, e.inputs[0])
    tr = nt.nodes.new("ShaderNodeBsdfTransparent"); mx = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(s2.outputs[0], mx.inputs[0]); nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(e.outputs[0], mx.inputs[2])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(mx.outputs[0], o.inputs[0])
    m.blend_method = "BLEND"
    bpy.ops.mesh.primitive_plane_add(size=2 * R, location=merkez)
    d = bpy.context.active_object; d.data.materials.append(m)
    d.rotation_euler = (math.radians(74), math.radians(-12), 0)      # REF-060: egik, gezegeni yatay saran halka


def gok_uzay():
    sc = bos_sahne(w=1920, h=1080, ornek=min(ORNEK, 48))
    rnd = random.Random(60)
    # arka plan: kara uzay, hafif mor-lacivert bulutsu
    def kur(nt, tc):
        nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 2.2; nz.inputs["Detail"].default_value = 8
        nt.links.new(tc.outputs["Generated"], nz.inputs["Vector"])
        return rampa(nt, nz.outputs["Fac"], [(0.35, "#020108"), (0.55, "#0b0626"), (0.72, "#24104e")])
    m, nt, em = mat_desen("uzay", kur)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 80, 9), rotation=(math.pi / 2, 0, 0))
    p = bpy.context.active_object; p.scale = (190, 110, 1); p.data.materials.append(m)
    renkler = [RENK["p1"], RENK["p2"], MOR, "#ffffff", "#5ff2ff", "#ffd25a", "#7dffb4"]
    # yildiz tozu: kucuk beyaz/renkli noktalar tum gokte
    yb = mat_emis("yildiz_b", (1, 1, 1), 9.0)
    for i in range(420):
        x, y, z = rnd.uniform(-52, 52), rnd.uniform(46, 70), rnd.uniform(-6, 34)
        kure((x, y, z), rnd.choice([0.05, 0.07, 0.09, 0.13]), yb if rnd.random() < 0.7 else
             mat_emis("yr%d" % i, lin(hex3(rnd.choice(renkler))), 8.0), sub=1)
    # galaksi halkasi + gezegen: ekranin ortasi, kapilarin ustunden ve arasindan gorunur (REF-060)
    galaksi_halkasi((0, 38, 12.5), 30)
    gezegen((0, 34, 12.2), 6.6)
    # renkli isik noktalari (REF-060: gezegen cevresinde pembe/mavi/yesil benekler)
    for i in range(110):
        ac = rnd.uniform(0, 6.283); r = rnd.uniform(9, 40)
        kure((math.cos(ac) * r, rnd.uniform(24, 44), 12 + math.sin(ac) * r * 0.55), rnd.uniform(0.12, 0.42),
             mat_emis("benek%d" % i, lin(hex3(rnd.choice(renkler))), rnd.uniform(3, 8)), sub=2)
    bpy.ops.object.camera_add(location=(0, -6, 9), rotation=(math.radians(90), 0, 0))
    kam = bpy.context.active_object; kam.data.lens = 26; sc.camera = kam
    sc.use_nodes = True
    nt2 = sc.node_tree; nt2.nodes.clear()
    rl = nt2.nodes.new("CompositorNodeRLayers")
    gl = nt2.nodes.new("CompositorNodeGlare"); gl.glare_type = "FOG_GLOW"; gl.threshold = 0.8; gl.size = 8; gl.mix = 0.0
    ou = nt2.nodes.new("CompositorNodeComposite")
    nt2.links.new(rl.outputs[0], gl.inputs[0]); nt2.links.new(gl.outputs[0], ou.inputs[0])
    if KAPAK:
        sc.view_settings.exposure = POZ_KAPAK
    yaz(sc, ON + "gok.png")


# ------------------------------------------------------------------ SERIT: pelus zemin + chevron + kafes kapi
def mat_plastik(ad, renk, isilti=0.25):
    m = bpy.data.materials.new(ad); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*renk, 1); b.inputs["Roughness"].default_value = 0.32
    b.inputs["Coat Weight"].default_value = 0.4; b.inputs["Coat Roughness"].default_value = 0.15
    b.inputs["Emission Color"].default_value = (*renk, 1); b.inputs["Emission Strength"].default_value = isilti
    return m


def kafes_kiris(a, b, kal, mat, civata, dikey):
    """REF-060 truss: iki paralel ana cubuk + basamaklar + capraz gergiler + ana cubuklarda civata/blok cikintilari"""
    a, b = Vector(a), Vector(b); L = (b - a).length
    yan = Vector((kal / 2, 0, 0)) if dikey else Vector((0, 0, kal / 2))
    u = (b - a).normalized()
    for s in (-1, 1):
        o = a + yan * s; e = b + yan * s
        merk = (o + e) / 2
        boyut = (0.16, 0.2, L + 0.16) if dikey else (L + 0.16, 0.2, 0.16)
        yuvarlak_kutu("ana", merk, boyut, mat, egim=0.03, seg=2)
        n = max(2, int(L / 0.38))
        for j in range(n + 1):
            q = o + u * (L * j / n) + Vector((0, -0.11, 0))
            bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=0.05, location=q, rotation=(math.pi / 2, 0, 0), vertices=12)
            bpy.context.active_object.data.materials.append(civata)
    n = max(2, int(L / (kal * 1.05)))
    for j in range(n + 1):
        p = a + u * (L * j / n)
        boru(p - yan, p + yan, 0.045, mat)
        if j < n:
            p2 = a + u * (L * (j + 1) / n)
            boru(p - yan, p2 + yan, 0.035, mat)
            boru(p + yan, p2 - yan, 0.035, mat)


def serit_uzay(oyuncu):
    sc = bos_sahne(w=960, h=1080, saydam=True)
    R = lin(hex3(RENK[oyuncu]))
    tuy = mat_tuy("tuy", R, acik_m=0.45)
    neon = mat_emis("neon", acik(R, 0.45), 10.0)
    Y = KAPI["y"]; W, H = KAPI["w"], KAPI["h"]
    KK = 0.9
    # pelus zemin: REF-060'da yol oyuncu renginde tuylu; kisa sik tuy
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, (Y + 3) / 2 - 0.5, 0))
    z = bpy.context.active_object; z.scale = (11.0, Y + 4, 1); bpy.ops.object.transform_apply(scale=True)
    tuylu(z, mat_tuy("tuy_zemin", acik(R, 0.08), acik_m=0.4), yogun=170, boy=0.06)
    # beyaz pelus chevron'lar, altinda oyuncu rengi neon (REF-060: beyaz, kenari parlayan V'ler)
    tuy_chev = mat_tuy("tuy_chev", acik(R, 0.75), acik_m=0.9)
    CHEV = []
    for yy in (2.6, 4.4, 6.2):
        for s in (-1, 1):
            o = yuvarlak_kutu("chev", (s * 0.95, yy + 0.5, 0.15), (2.3, 0.42, 0.26), tuy_chev, egim=0.12)
            o.rotation_euler = (0, 0, -s * math.radians(26))
            bpy.context.view_layer.update(); bpy.ops.object.select_all(action="DESELECT")
            o.select_set(True); bpy.context.view_layer.objects.active = o
            bpy.ops.object.transform_apply(rotation=True)
            tuylu(o, tuy_chev, yogun=2400, boy=0.07)
            CHEV.append(Vector((s * 0.95, yy + 0.5, 0.15)))
        boru((-1.95, yy + 0.98, 0.03), (0, yy - 0.08, 0.03), 0.04, neon)
        boru((0, yy - 0.08, 0.03), (1.95, yy + 0.98, 0.03), 0.04, neon)
    # pelus korkuluk
    for s in (-1, 1):
        ys = [0.9 + i * 1.35 for i in range(int((Y - 1.4) / 1.35) + 1)]
        for yy in ys:
            o = yuvarlak_kutu("baba", (s * 2.45, yy, 0.42), (0.42, 0.42, 0.84), tuy, egim=0.16)
            tuylu(o, tuy, yogun=2400, boy=0.08)
        o = yuvarlak_kutu("tirabzan", (s * 2.45, (ys[0] + ys[-1]) / 2, 0.66), (0.22, ys[-1] - ys[0], 0.2), tuy, egim=0.09)
        tuylu(o, tuy, yogun=2400, boy=0.07)
    # KAFES KAPI (REF-060): iki yan kule + ust kiris, pastel oyuncu renginde parlak plastik, civata cikintilari
    kafes = mat_plastik("kafes", acik(R, 0.3), 0.3)
    civata = mat_plastik("civata", acik(R, 0.55), 0.4)
    xk = W / 2 - KK / 2
    for s in (-1, 1):
        kafes_kiris((s * xk, Y, 0.0), (s * xk, Y, H + KK / 2), KK, kafes, civata, dikey=True)
    kafes_kiris((-xk, Y, H + KK / 2), (xk, Y, H + KK / 2), KK, kafes, civata, dikey=False)
    # arka katman (derinlik): ayni kafes 0,6 m geride, biraz koyu
    kafes2 = mat_plastik("kafes2", R, 0.15)
    for s in (-1, 1):
        kafes_kiris((s * xk, Y + 0.6, 0.0), (s * xk, Y + 0.6, H + KK / 2), KK, kafes2, kafes2, dikey=True)
    kafes_kiris((-xk, Y + 0.6, H + KK / 2), (xk, Y + 0.6, H + KK / 2), KK, kafes2, kafes2, dikey=False)
    ic = W / 2 - KK
    for a, b in (((-ic + 0.06, Y - 0.2, 0.04), (-ic + 0.06, Y - 0.2, H - 0.06)), ((ic - 0.06, Y - 0.2, 0.04), (ic - 0.06, Y - 0.2, H - 0.06)),
                 ((-ic + 0.06, Y - 0.2, H - 0.06), (ic - 0.06, Y - 0.2, H - 0.06))):
        boru(a, b, 0.05, neon)
    par = mat_emis("parilti", (1, 1, 1), 6.0)
    AMPUL = []
    rnd = random.Random(41 if oyuncu == "p1" else 43)
    for s in (-1, 1):
        for j in range(5):
            AMPUL.append(Vector((s * xk + rnd.uniform(-0.25, 0.25), Y - 0.3, 0.5 + j * (H - 0.6) / 4)))
    for i in range(7):
        AMPUL.append(Vector((-ic + 0.4 + i * (2 * ic - 0.8) / 6, Y - 0.3, H + KK / 2 + rnd.uniform(-0.2, 0.2))))
    for q in AMPUL:
        yildiz_mesh(q, 0.1, par, kal=0.02, uc=4)
    isik("AREA", (0, -1.5, 6.5), 420, (1, 1, 1), 6, yon=(0, Y * 0.6, 0))
    isik("AREA", (-4, 3, 3), 300, acik(R, 0.2), 3, yon=(0, Y, 2))
    isik("AREA", (4, 3, 3), 260, lin(hex3(MOR)), 3, yon=(0, Y, 2))
    isik("AREA", (0, Y - 2.5, 5.5), 380, acik(R, 0.3), 4, yon=(0, Y, 2))
    rx = math.radians(90 - KAM["egim"])
    bpy.ops.object.camera_add(location=(0, -1.6 if KAPAK else 0, KAM["z"] + (0.35 if KAPAK else 0)), rotation=(rx, 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.sensor_fit = "VERTICAL"; kam.data.sensor_height = KAM["sensor"]; kam.data.lens = KAM["lens"]
    noktalar = [Vector((-ic, Y, 0)), Vector((ic, Y, 0)), Vector((-ic, Y, H)), Vector((ic, Y, H))]
    bpy.context.view_layer.update()
    px = [world_to_camera_view(sc, kam, p) for p in noktalar]
    xs = [p.x * 960 for p in px]; ys = [(1 - p.y) * 1080 for p in px]
    YERLESIM[ON + "aciklik_" + oyuncu] = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
    YERLESIM[ON + "ampul_" + oyuncu] = [[round(p.x * 960, 1), round((1 - p.y) * 1080, 1)] for p in (world_to_camera_view(sc, kam, q) for q in AMPUL)]
    log("aciklik", oyuncu, YERLESIM[ON + "aciklik_" + oyuncu])
    log("chevron px", [[round(q.x * 960), round((1 - q.y) * 1080)] for q in (world_to_camera_view(sc, kam, c) for c in CHEV)])
    if KAPAK:
        sc.view_settings.exposure = POZ_KAPAK
    yaz(sc, ON + "serit-%s.png" % oyuncu)


# ------------------------------------------------------------------ PANEL: yildizli isin patlamasi
PW, PH = 5.0, 4.1


def panel_uzay(oyuncu):
    """REF-060: merkezden duz acilan isin dilimleri (pastel oyuncu rengi / beyazimsi), dilimlerde konturlu yildizlar, parilti"""
    sc = bos_sahne(w=1100, h=904, saydam=True)
    R = lin(hex3(RENK[oyuncu]))
    m = bpy.data.materials.new("isin"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sp = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Object"], sp.inputs[0])
    at = nt.nodes.new("ShaderNodeMath"); at.operation = "ARCTAN2"
    nt.links.new(sp.outputs["Z"], at.inputs[0]); nt.links.new(sp.outputs["X"], at.inputs[1])
    m1 = nt.nodes.new("ShaderNodeMath"); m1.operation = "MULTIPLY"; m1.inputs[1].default_value = 11.0      # 22 isin dilimi
    nt.links.new(at.outputs[0], m1.inputs[0])
    sn = nt.nodes.new("ShaderNodeMath"); sn.operation = "SINE"; nt.links.new(m1.outputs[0], sn.inputs[0])
    rp = nt.nodes.new("ShaderNodeValToRGB"); cr = rp.color_ramp; cr.interpolation = "CONSTANT"
    cr.elements[0].position = 0.0; cr.elements[0].color = (*acik(R, 0.42), 1)
    cr.elements[1].position = 0.5; cr.elements[1].color = (*acik(R, 0.85), 1)
    nt.links.new(sn.outputs[0], rp.inputs[0])
    # pelus doku: ince gurultuyle tel tel ton (REF-060 paneli tuylu gorunur)
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 90.0; nz.inputs["Detail"].default_value = 3
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    nr = nt.nodes.new("ShaderNodeMapRange"); nr.inputs["To Min"].default_value = 0.86; nr.inputs["To Max"].default_value = 1.06
    nt.links.new(nz.outputs["Fac"], nr.inputs["Value"])
    mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"; mx.blend_type = "MULTIPLY"; mx.inputs[0].default_value = 1.0
    nt.links.new(rp.outputs[0], mx.inputs[6]); nt.links.new(nr.outputs[0], mx.inputs[7])
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs[1].default_value = 1.0; nt.links.new(mx.outputs[2], em.inputs[0])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], o.inputs[0])
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    p = bpy.context.active_object; p.scale = (PW, 0.25, PH); bpy.ops.object.transform_apply(scale=True)
    bv = p.modifiers.new("egim", "BEVEL"); bv.width = 0.22; bv.segments = 8; bv.limit_method = "NONE"
    bpy.ops.object.shade_smooth(); p.data.materials.append(m)
    rnd = random.Random(6 if oyuncu == "p1" else 8)
    kontur = mat_emis("kontur", (1, 1, 1), 2.0)
    dolgu = mat_emis("dolgu", acik(R, 0.6), 1.1)
    for i in range(16):
        x, zz = rnd.uniform(-PW / 2 + 0.35, PW / 2 - 0.35), rnd.uniform(-PH / 2 + 0.35, PH / 2 - 0.35)
        r = rnd.choice([0.16, 0.22, 0.3])
        a = rnd.uniform(0, 1.2)
        yo = yildiz_mesh((x, -0.14, zz), r, kontur, kal=0.02); yo.rotation_euler[1] = a
        yi = yildiz_mesh((x, -0.16, zz), r * 0.8, dolgu, kal=0.02); yi.rotation_euler[1] = a
    par = mat_emis("parilti", (1, 1, 1), 10.0)
    for i in range(55):
        kure((rnd.uniform(-PW / 2 + 0.2, PW / 2 - 0.2), -0.17, rnd.uniform(-PH / 2 + 0.2, PH / 2 - 0.2)), rnd.choice([0.015, 0.025, 0.035]), par, sub=1)
    bpy.ops.object.camera_add(location=(0, -10, 0), rotation=(math.radians(90), 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.type = "ORTHO"; kam.data.ortho_scale = PW + 0.08
    if KAPAK:
        sc.view_settings.exposure = POZ_KAPAK
    yaz(sc, ON + "panel-%s.png" % oyuncu)


# ------------------------------------------------------------------ ana akis (uzay)
if YALNIZ in ("hepsi", "poz"):
    poz_maskeleri()
if YALNIZ in ("hepsi", "sahne", "gok", "kapak"):
    gok_uzay()
if YALNIZ in ("hepsi", "sahne", "serit", "kapak"):
    for o_ in ("p1", "p2"):
        serit_uzay(o_)
if YALNIZ in ("hepsi", "sahne", "panel", "kapak"):
    for o_ in ("p1", "p2"):
        panel_uzay(o_)
json.dump(YERLESIM, open(os.path.join(CIKTI, "yerlesim.json"), "w"), indent=1)
log("bitti (uzay)", {k: v for k, v in YERLESIM.items() if k.startswith("aciklik")})
