"""HUMAN TETRIS 8. video (REF-059, 1v1 PvP) - DISKO sahne varliklari (Blender, GitHub Actions).

varlik.py tarafindan calistirilir (yardimcilar oradan gelir):
    blender -b --factory-startup -noaudio -P 03-motor/tetris-pvp/varlik.py -- --mod disko --renk1 FF3EA5 --renk2 2E9BFF \
        --cikti cikti [--ornek 64] [--yalniz sahne] [--pozlar 03-motor/tetris-pvp/pozlar-08.json]

REF-059'da ne varsa (CLAUDE.md md. 22): ortada dev disko topu (aynali karolar), arkada neon tunel isinlari + bokeh,
her oyuncunun seridi = isikli ayna-karo zemin + PELUS (tuylu) chevron'lar + pelus korkuluk babalari + kalin PELUS kapi
cercevesi (ic kenarda neon, kosede yildiz parilti). Duvar paneli tur 1-2 yildizli isin girdabi, tur 3-4 spot isikli sahne.
P1 pembe solda, P2 mavi sagda (kullanici, 24 Eki 2026).

Ciktilar (sahne4.html 2B'de birlestirir, kamera sabit):
  gok.png            1920x1080  tunel + disko topu + bokeh (opak)
  serit-p1/p2.png    960x1080   zemin, chevron, korkuluk, pelus kapi (gokte saydam)
  panel-p1/p2.png    1100x904   yildizli isin girdabi (tur 1-2)
  panel2-p1/p2.png   1100x904   spot isikli sahne (tur 3-4, tema.panelTur)
  poz/<ad>.png       --yalniz hepsi|poz ise (varlik.py poz_maskeleri)
  yerlesim.json      aciklik_p1/p2, ampul_p1/p2 (kapi cercevesindeki parilti noktalari - motor yakip sondurur)
"""

YERLESIM.clear()
# --yalniz kapak (24 Eki, kullanici: kapak "soluk", sonra 2B boyama "arka taraftaki estetik yapi kayboldu"): kapak arka plani
# Blender'da DOYGUN kurulur - pelus ve karo oyuncu renginin kendisi (pastel degil), kamera biraz geride (cerceve tum gorunur)
KAPAK = YALNIZ == "kapak"
ON = "kapak-" if KAPAK else ""
POZ_KAPAK = float(arg("--kapak-pozlama", "-0.9"))


def mat_tuy(ad, renk, acik_m=0.45):
    """pelus tuy: tel tel acik/koyu ton (Object koordinatli ince gurultu), yumusak sheen, hafif ic isilti"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 60.0; nz.inputs["Detail"].default_value = 2
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    rp = nt.nodes.new("ShaderNodeValToRGB"); cr = rp.color_ramp
    cr.elements[0].position = 0.3; cr.elements[0].color = (*koyu(renk, 0.15), 1)
    cr.elements[1].position = 0.7; cr.elements[1].color = (*acik(renk, acik_m), 1)
    nt.links.new(nz.outputs["Fac"], rp.inputs[0])
    nt.links.new(rp.outputs[0], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.6
    b.inputs["Sheen Weight"].default_value = 1.0
    b.inputs["Emission Color"].default_value = (*acik(renk, 0.3), 1); b.inputs["Emission Strength"].default_value = 0.15
    return m


def tuylu(o, mat, yogun=900, boy=0.11):
    """objeye pelus tuy (Geometry Nodes): yuzeye yogun ince koniler, normale gore + rastgele egik, rastgele boy.
    Deneme 1 (24 Eki): particle hair Actions'ta hic cizilmedi -> mesh koni (her motorda guvenilir)."""
    o.data.materials.clear(); o.data.materials.append(mat)
    ng = bpy.data.node_groups.new("tuy_" + o.name, "GeometryNodeTree")
    ng.interface.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    N = ng.nodes; L = ng.links
    gi = N.new("NodeGroupInput"); go = N.new("NodeGroupOutput")
    dp = N.new("GeometryNodeDistributePointsOnFaces"); dp.distribute_method = "RANDOM"
    dp.inputs["Density"].default_value = yogun
    L.new(gi.outputs[0], dp.inputs["Mesh"])
    kn = N.new("GeometryNodeMeshCone")
    kn.inputs["Vertices"].default_value = 4
    kn.inputs["Radius Top"].default_value = 0.0; kn.inputs["Radius Bottom"].default_value = boy * 0.11
    kn.inputs["Depth"].default_value = boy
    tr = N.new("GeometryNodeTransform"); tr.inputs["Translation"].default_value = (0, 0, boy * 0.35)
    L.new(kn.outputs["Mesh"], tr.inputs["Geometry"])
    io = N.new("GeometryNodeInstanceOnPoints")
    L.new(dp.outputs["Points"], io.inputs["Points"]); L.new(tr.outputs[0], io.inputs["Instance"])
    rr = N.new("FunctionNodeRandomValue"); rr.data_type = "FLOAT_VECTOR"
    rr.inputs["Min"].default_value = (-0.55, -0.55, -3.14); rr.inputs["Max"].default_value = (0.55, 0.55, 3.14)
    try:
        rot = N.new("FunctionNodeRotateRotation"); rot.rotation_space = "LOCAL"
        e2r = N.new("FunctionNodeEulerToRotation"); L.new(rr.outputs["Value"], e2r.inputs[0])
        L.new(dp.outputs["Rotation"], rot.inputs["Rotation"]); L.new(e2r.outputs[0], rot.inputs[1])
        L.new(rot.outputs[0], io.inputs["Rotation"])
    except Exception as e:
        log("tuy egimi atlandi", e); L.new(dp.outputs["Rotation"], io.inputs["Rotation"])
    rs = N.new("FunctionNodeRandomValue"); rs.data_type = "FLOAT"
    rs.inputs[2].default_value = 0.55; rs.inputs[3].default_value = 1.35
    L.new(rs.outputs[1], io.inputs["Scale"])
    rl = N.new("GeometryNodeRealizeInstances"); L.new(io.outputs[0], rl.inputs[0])
    sm = N.new("GeometryNodeSetMaterial"); sm.inputs["Material"].default_value = mat; L.new(rl.outputs[0], sm.inputs["Geometry"])
    jn = N.new("GeometryNodeJoinGeometry"); L.new(gi.outputs[0], jn.inputs[0]); L.new(sm.outputs[0], jn.inputs[0])
    L.new(jn.outputs[0], go.inputs[0])
    md = o.modifiers.new("tuy", "NODES"); md.node_group = ng
    return o


def yildiz_mesh(konum, r, mat, kal=0.06, uc=5, rot=(math.pi / 2, 0, 0)):
    bpy.ops.mesh.primitive_circle_add(vertices=uc * 2, radius=r, fill_type="NGON", location=konum, rotation=rot)
    yo = bpy.context.active_object
    for i, v in enumerate(yo.data.vertices):
        if i % 2:
            v.co *= 0.45
    so = yo.modifiers.new("kal", "SOLIDIFY"); so.thickness = kal; so.offset = 0
    yo.data.materials.append(mat)
    return yo


# ------------------------------------------------------------------ GOK: neon tunel + disko topu
def disko_topu(merkez, R):
    """aynali karolu top: her yuz rastgele ayna / pembe / mavi / beyaz parlak karo (duz golgeleme = faset)"""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=R, location=merkez, segments=56, ring_count=28)
    top = bpy.context.active_object
    mats = []
    for ad_, renk, guc in (("ayna", None, 0), ("karo_pembe", RENK["p1"], 1.8), ("karo_mavi", RENK["p2"], 1.8),
                           ("karo_beyaz", "#ffffff", 2.2), ("karo_mor", "#b06bff", 1.5)):
        m = bpy.data.materials.new(ad_); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
        b.inputs["Metallic"].default_value = 1.0; b.inputs["Roughness"].default_value = 0.08
        b.inputs["Base Color"].default_value = (0.75, 0.78, 0.9, 1)
        if renk:
            b.inputs["Emission Color"].default_value = (*lin(hex3(renk)), 1); b.inputs["Emission Strength"].default_value = guc
        top.data.materials.append(m); mats.append(m)
    rnd = random.Random(59)
    for p in top.data.polygons:
        p.material_index = rnd.choices(range(5), weights=(46, 16, 18, 8, 12))[0]
        p.use_smooth = False
    # karo araligi: inset ile ince koyu derz
    bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.inset(thickness=R * 0.006, depth=R * 0.004, use_individual=True)
    bpy.ops.object.mode_set(mode="OBJECT")
    return top


def gok_disko():
    sc = bos_sahne(w=1920, h=1080, ornek=min(ORNEK, 48))
    rnd = random.Random(59)
    # arka plan: koyu gece moru, merkezde hafif mor-mavi parlama
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 70, 9), rotation=(math.pi / 2, 0, 0))
    p = bpy.context.active_object; p.scale = (170, 100, 1)
    m = bpy.data.materials.new("gok"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Location"].default_value = (-0.5, -0.5, 0)
    nt.links.new(tc.outputs["Generated"], mp.inputs["Vector"])
    gr = nt.nodes.new("ShaderNodeTexGradient"); gr.gradient_type = "SPHERICAL"; nt.links.new(mp.outputs[0], gr.inputs["Vector"])
    rp = nt.nodes.new("ShaderNodeValToRGB"); cr = rp.color_ramp
    cr.elements[0].position = 0.0; cr.elements[0].color = (*lin(hex3("#05031a")), 1)
    cr.elements[1].position = 0.9; cr.elements[1].color = (*lin(hex3("#3a1a8a")), 1)
    e = cr.elements.new(0.6); e.color = (*lin(hex3("#140a4a")), 1)
    nt.links.new(gr.outputs["Fac"], rp.inputs[0])
    em = nt.nodes.new("ShaderNodeEmission"); nt.links.new(rp.outputs[0], em.inputs[0])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], o.inputs[0])
    p.data.materials.append(m)
    renkler = [RENK["p1"], RENK["p2"], "#b06bff", "#ffffff", "#ff7ad8", "#5fd0ff"]
    # neon tunel: merkeze dogru kuculen dikdortgen cerceveler (perspektif derinlik) - REF-059 arka plani
    for i in range(10):
        yy = 22 + i * 4.6
        w_, h_ = 30 + i * 4.0, 17 + i * 2.2
        c = lin(hex3(renkler[i % 3]))
        nm = mat_emis("tunel%d" % i, c, 7.0 - i * 0.45)
        for a, b in (((-w_, yy, 9 - h_), (w_, yy, 9 - h_)), ((-w_, yy, 9 + h_), (w_, yy, 9 + h_)),
                     ((-w_, yy, 9 - h_), (-w_, yy, 9 + h_)), ((w_, yy, 9 - h_), (w_, yy, 9 + h_))):
            boru(a, b, 0.07 + 0.01 * i, nm)
    # merkezden disari isinlar (hiz cizgileri): ince parlak cubuklar, tunel boyunca derinlige uzanir
    for i in range(70):
        ac = rnd.uniform(0, 6.283)
        r0, r1 = rnd.uniform(4, 10), rnd.uniform(18, 40)
        y0, y1 = rnd.uniform(50, 64), rnd.uniform(20, 34)
        a = (math.cos(ac) * r0, y0, 9 + math.sin(ac) * r0 * 0.62)
        b = (math.cos(ac) * r1, y1, 9 + math.sin(ac) * r1 * 0.62)
        boru(a, b, rnd.uniform(0.03, 0.09), mat_emis("isin%d" % i, lin(hex3(rnd.choice(renkler))), rnd.uniform(5, 12)))
    # bokeh kureleri (ust bolgede pembe/mavi buyuk yumusak daireler) + kucuk parilti
    for i in range(70):
        c = lin(hex3(rnd.choice(renkler)))
        x, y, z = rnd.uniform(-38, 38), rnd.uniform(18, 40), rnd.uniform(2, 26)
        kure((x, y, z), rnd.uniform(0.25, 0.9), mat_emis("bokeh%d" % i, c, rnd.uniform(2.5, 6)), sub=2)
    # disko topu: ekranin tam ortasi, kapilarin arasindan gorunur (REF-059)
    disko_topu((0, 30, 11.2), 4.4)
    isik("POINT", (0, 18, 20), 700, lin(hex3("#ffffff")))
    isik("POINT", (-8, 24, 8), 900, lin(hex3(RENK["p1"])))
    isik("POINT", (8, 24, 8), 900, lin(hex3(RENK["p2"])))
    # top cevresine yansiyan isik benekleri (duvarda gezen disko noktalari)
    for i in range(160):
        ac = rnd.uniform(0, 6.283); r = rnd.uniform(7, 34)
        kure((math.cos(ac) * r, rnd.uniform(40, 60), 11 + math.sin(ac) * r * 0.6), rnd.uniform(0.08, 0.22),
             mat_emis("benek%d" % i, lin(hex3(rnd.choice(renkler))), rnd.uniform(6, 14)), sub=1)
    bpy.ops.object.camera_add(location=(0, -6, 9), rotation=(math.radians(90), 0, 0))
    kam = bpy.context.active_object; kam.data.lens = 26; sc.camera = kam
    sc.use_nodes = True
    nt2 = sc.node_tree; nt2.nodes.clear()
    rl = nt2.nodes.new("CompositorNodeRLayers")
    gl = nt2.nodes.new("CompositorNodeGlare"); gl.glare_type = "FOG_GLOW"; gl.threshold = 0.7; gl.size = 9; gl.mix = 0.2
    gl2 = nt2.nodes.new("CompositorNodeGlare"); gl2.glare_type = "STREAKS"; gl2.threshold = 2.5; gl2.streaks = 4; gl2.mix = -0.6
    ou = nt2.nodes.new("CompositorNodeComposite")
    nt2.links.new(rl.outputs[0], gl.inputs[0]); nt2.links.new(gl.outputs[0], gl2.inputs[0]); nt2.links.new(gl2.outputs[0], ou.inputs[0])
    if KAPAK:
        sc.view_settings.exposure = POZ_KAPAK
    yaz(sc, ON + "gok.png")


# ------------------------------------------------------------------ SERIT: ayna-karo zemin + pelus kapi
def mat_karo(R):
    """isikli ayna-karo zemin: kare karolar, karo basina rastgele parlaklik (oyuncu rengi <-> acik), ince koyu derz, parlak yuzey"""
    m = bpy.data.materials.new("karo"); m.use_nodes = True; nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.offset = 0.0; br.squash = 1.0
    br.inputs["Scale"].default_value = 1.0; br.inputs["Mortar Size"].default_value = 0.025
    br.inputs["Brick Width"].default_value = 0.42; br.inputs["Row Height"].default_value = 0.42
    br.inputs["Bias"].default_value = 0.0
    br.inputs["Color1"].default_value = (*R, 1); br.inputs["Color2"].default_value = (*(koyu(R, 0.35) if KAPAK else acik(R, 0.65)), 1)
    br.inputs["Mortar"].default_value = (*koyu(R, 0.2), 1)
    nt.links.new(tc.outputs["Object"], br.inputs["Vector"])
    nt.links.new(br.outputs["Color"], b.inputs["Base Color"])
    nt.links.new(br.outputs["Color"], b.inputs["Emission Color"]); b.inputs["Emission Strength"].default_value = 0.75 if KAPAK else 0.9   # kapak deneme 1: 1,4 karoyu beyaza patlatti
    b.inputs["Roughness"].default_value = 0.22; b.inputs["Metallic"].default_value = 0.1      # deneme 2: neon yansimasi zeminde uzun cizgi
    b.inputs["Coat Weight"].default_value = 0.35; b.inputs["Coat Roughness"].default_value = 0.12
    return m


def serit_disko(oyuncu):
    sc = bos_sahne(w=960, h=1080, saydam=True)
    R = lin(hex3(RENK[oyuncu]))
    tuy = mat_tuy("tuy", koyu(R, 0.1) if KAPAK else R, acik_m=0.3 if KAPAK else 0.45)
    tuy_acik = mat_tuy("tuy_acik", acik(R, 0.25), acik_m=0.6)
    tuy_cerceve = mat_tuy("tuy_cerceve", R if KAPAK else acik(R, 0.18), acik_m=0.35 if KAPAK else 0.55)     # REF-059 cerceve: acik pembe/mavi, uclari beyazimsi
    neon = mat_emis("neon", acik(R, 0.15) if KAPAK else acik(R, 0.45), 5.0 if KAPAK else 10.0)   # kapak: beyaz degil renkli neon
    Y = KAPI["y"]
    W, H = KAPI["w"], KAPI["h"]
    KK = 0.85                                   # pelus cerceve kalinligi (REF-059: kalin tuylu kenar)
    # zemin: kapiya kadar ve biraz otesine, korkuluklarin disina tasar (REF-059'da karo zemin tum alt yariyi kaplar)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, (Y + 3) / 2 - 0.5, 0))
    z = bpy.context.active_object; z.scale = (11.0, Y + 4, 1); bpy.ops.object.transform_apply(scale=True)
    z.data.materials.append(mat_karo(R))
    # pelus chevron'lar: kameraya bakan V (ucu kameraya), yol boyunca. Deneme 2: 1,6 m'deki kadraj altinda kaldi (kamera
    # zemini ~3,2 m'den gorur), 4,3'teki zeminle ayni tonda kayboldu -> gorunur mesafede, daha buyuk, beyazimsi + altinda neon
    tuy_chev = mat_tuy("tuy_chev", acik(R, 0.55), acik_m=0.8)
    CHEV = []
    for yy in (3.7, 5.9):
        for s in (-1, 1):
            o = yuvarlak_kutu("chev", (s * 0.95, yy + 0.5, 0.17), (2.3, 0.5, 0.32), tuy_chev, egim=0.13)
            o.rotation_euler = (0, 0, -s * math.radians(26))
            bpy.context.view_layer.update(); bpy.ops.object.select_all(action="DESELECT")
            o.select_set(True); bpy.context.view_layer.objects.active = o
            bpy.ops.object.transform_apply(rotation=True)
            tuylu(o, tuy_chev, yogun=2600, boy=0.09)
            CHEV.append(Vector((s * 0.95, yy + 0.5, 0.17)))
        boru((-1.9, yy + 0.95, 0.03), (0, yy - 0.05, 0.03), 0.035, neon)
        boru((0, yy - 0.05, 0.03), (1.9, yy + 0.95, 0.03), 0.035, neon)
    # pelus korkuluk: iki yanda tuylu babalar + tuylu tirabzan
    for s in (-1, 1):
        ys = [0.9 + i * 1.35 for i in range(int((Y - 1.4) / 1.35) + 1)]
        for yy in ys:
            o = yuvarlak_kutu("baba", (s * 2.45, yy, 0.42), (0.42, 0.42, 0.84), tuy, egim=0.16)
            tuylu(o, tuy, yogun=2400, boy=0.08)
        o = yuvarlak_kutu("tirabzan", (s * 2.45, (ys[0] + ys[-1]) / 2, 0.66), (0.22, ys[-1] - ys[0], 0.2), tuy, egim=0.09)
        tuylu(o, tuy, yogun=2400, boy=0.07)
    # pelus kapi cercevesi: iki kalin yan + ust kiris, ic kenarda neon tup
    xk = W / 2 - KK / 2
    for s in (-1, 1):
        o = yuvarlak_kutu("yan", (s * xk, Y, (H + KK) / 2), (KK, 0.8, H + KK), tuy, egim=0.25, seg=5)
        tuylu(o, tuy_cerceve, yogun=2200, boy=0.14)
    o = yuvarlak_kutu("ust", (0, Y, H + KK / 2), (W, 0.8, KK), tuy, egim=0.25, seg=5)
    tuylu(o, tuy_cerceve, yogun=2200, boy=0.14)
    ic = W / 2 - KK
    for a, b in (((-ic + 0.06, Y - 0.42, 0.04), (-ic + 0.06, Y - 0.42, H - 0.06)), ((ic - 0.06, Y - 0.42, 0.04), (ic - 0.06, Y - 0.42, H - 0.06)),
                 ((-ic + 0.06, Y - 0.42, H - 0.06), (ic - 0.06, Y - 0.42, H - 0.06))):
        boru(a, b, 0.05, neon)
    # cercevede parilti noktalari (REF-059 cercevede 4 kollu beyaz parilti): kucuk yildizlar; motor yakip sondurur
    par = mat_emis("parilti", (1, 1, 1), 6.0)
    AMPUL = []
    rnd = random.Random(31 if oyuncu == "p1" else 37)
    for s in (-1, 1):
        for j in range(5):
            AMPUL.append(Vector((s * xk + rnd.uniform(-0.2, 0.2), Y - 0.55, 0.5 + j * (H - 0.6) / 4)))
    for i in range(7):
        AMPUL.append(Vector((-ic + 0.4 + i * (2 * ic - 0.8) / 6, Y - 0.55, H + KK / 2 + rnd.uniform(-0.15, 0.15))))
    for q in AMPUL:
        yildiz_mesh(q, 0.11, par, kal=0.02, uc=4)
    # isiklar: ustten genis beyaz, yanlardan oyuncu rengi + karsi renk dolgu (tuy sheen'i yakalasin)
    isik("AREA", (0, -1.5, 6.5), 420, (1, 1, 1), 6, yon=(0, Y * 0.6, 0))
    isik("AREA", (-4, 3, 3), 300, acik(R, 0.2), 3, yon=(0, Y, 2))
    isik("AREA", (4, 3, 3), 260, lin(hex3("#c9a6ff")), 3, yon=(0, Y, 2))
    isik("AREA", (0, Y + 3, 6), 500, acik(R, 0.1), 5, yon=(0, Y, 1))
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
    if KAPAK:      # kapak deneme 2 olcumu: serit V 0,998 (asiri pozlama -> renk beyaza kaciyor), S 0,60 / ref 0,66
        sc.view_settings.exposure = POZ_KAPAK
    yaz(sc, ON + "serit-%s.png" % oyuncu)


# ------------------------------------------------------------------ PANEL: yildizli isin girdabi / spot isikli sahne
PW, PH = 5.0, 4.1


def panel_kamera(sc):
    bpy.ops.object.camera_add(location=(0, -10, 0), rotation=(math.radians(90), 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.type = "ORTHO"; kam.data.ortho_scale = PW + 0.08


def panel_govde(mat):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    p = bpy.context.active_object; p.scale = (PW, 0.25, PH); bpy.ops.object.transform_apply(scale=True)
    bv = p.modifiers.new("egim", "BEVEL"); bv.width = 0.22; bv.segments = 8; bv.limit_method = "NONE"
    bpy.ops.object.shade_smooth()
    p.data.materials.append(mat)
    return p


def panel_girdap_disko(oyuncu):
    """REF-059 tur 1-2: merkezden donerek acilan isin dilimleri (oyuncu rengi / acik), dilimlerde yildizlar, beyaz parilti"""
    sc = bos_sahne(w=1100, h=904, saydam=True)
    R = lin(hex3(RENK[oyuncu]))
    m = bpy.data.materials.new("girdap"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sp = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Object"], sp.inputs[0])
    at = nt.nodes.new("ShaderNodeMath"); at.operation = "ARCTAN2"
    nt.links.new(sp.outputs["Z"], at.inputs[0]); nt.links.new(sp.outputs["X"], at.inputs[1])
    uz = nt.nodes.new("ShaderNodeVectorMath"); uz.operation = "LENGTH"; nt.links.new(tc.outputs["Object"], uz.inputs[0])
    m1 = nt.nodes.new("ShaderNodeMath"); m1.operation = "MULTIPLY"; m1.inputs[1].default_value = 9.0      # 18 isin dilimi
    nt.links.new(at.outputs[0], m1.inputs[0])
    m2 = nt.nodes.new("ShaderNodeMath"); m2.operation = "MULTIPLY"; m2.inputs[1].default_value = 1.1      # donus (sarmal)
    nt.links.new(uz.outputs["Value"], m2.inputs[0])
    t1 = nt.nodes.new("ShaderNodeMath"); t1.operation = "ADD"; nt.links.new(m1.outputs[0], t1.inputs[0]); nt.links.new(m2.outputs[0], t1.inputs[1])
    sn = nt.nodes.new("ShaderNodeMath"); sn.operation = "SINE"; nt.links.new(t1.outputs[0], sn.inputs[0])
    rp = nt.nodes.new("ShaderNodeValToRGB"); cr = rp.color_ramp; cr.interpolation = "EASE"
    cr.elements[0].position = 0.45; cr.elements[0].color = (*R, 1)
    cr.elements[1].position = 0.6; cr.elements[1].color = (*acik(R, 0.62), 1)
    nt.links.new(sn.outputs[0], rp.inputs[0])
    # merkez parlama + kenara dogru koyulasma
    mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (0.42, 1.0, 0.5)
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    gr = nt.nodes.new("ShaderNodeTexGradient"); gr.gradient_type = "SPHERICAL"; nt.links.new(mp.outputs[0], gr.inputs["Vector"])
    rp2 = nt.nodes.new("ShaderNodeValToRGB"); c2 = rp2.color_ramp
    c2.elements[0].position = 0.0; c2.elements[0].color = (*koyu(R, 0.55), 1)
    c2.elements[1].position = 0.85; c2.elements[1].color = (1, 1, 1, 1)
    nt.links.new(gr.outputs["Fac"], rp2.inputs[0])
    mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"; mx.blend_type = "MULTIPLY"; mx.inputs[0].default_value = 1.0
    nt.links.new(rp.outputs[0], mx.inputs[6]); nt.links.new(rp2.outputs[0], mx.inputs[7])
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs[1].default_value = 1.15; nt.links.new(mx.outputs[2], em.inputs[0])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], o.inputs[0])
    panel_govde(m)
    rnd = random.Random(5 if oyuncu == "p1" else 9)
    yil = mat_emis("yildiz", acik(R, 0.8), 1.6)
    for i in range(34):
        x, zz = rnd.uniform(-PW / 2 + 0.25, PW / 2 - 0.25), rnd.uniform(-PH / 2 + 0.25, PH / 2 - 0.25)
        yo = yildiz_mesh((x, -0.14, zz), rnd.choice([0.1, 0.14, 0.18, 0.24]), yil, kal=0.02)
        yo.rotation_euler[1] = rnd.uniform(0, 1.2)
    par = mat_emis("parilti", (1, 1, 1), 10.0)
    for i in range(70):
        kure((rnd.uniform(-PW / 2 + 0.2, PW / 2 - 0.2), -0.15, rnd.uniform(-PH / 2 + 0.2, PH / 2 - 0.2)), rnd.choice([0.015, 0.025, 0.035]), par, sub=1)
    panel_kamera(sc)
    yaz(sc, "panel-%s.png" % oyuncu)


def panel_sahne_disko(oyuncu):
    """REF-059 tur 3-4: ustten inen spot isik huzmeleri, altta isikli karo sahne zemini, havada parilti"""
    sc = bos_sahne(w=1100, h=904, saydam=True)
    R = lin(hex3(RENK[oyuncu]))
    m = bpy.data.materials.new("sahne"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord"); sp = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Generated"], sp.inputs[0])
    rp = nt.nodes.new("ShaderNodeValToRGB"); cr = rp.color_ramp
    cr.elements[0].position = 0.0; cr.elements[0].color = (*(R if KAPAK else acik(R, 0.2)), 1)
    cr.elements[1].position = 1.0; cr.elements[1].color = (*koyu(R, 0.35), 1)
    e = cr.elements.new(0.35); e.color = (*R, 1)
    nt.links.new(sp.outputs["Z"], rp.inputs[0])
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs[1].default_value = 1.0; nt.links.new(rp.outputs[0], em.inputs[0])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], o.inputs[0])
    panel_govde(m)
    # karo sahne zemini (alt %30): perspektif izgara cizgileri
    izg = mat_emis("izgara", acik(R, 0.7), 3.0)
    taban = -PH / 2 + 1.25
    boru((-PW / 2 + 0.1, -0.14, taban), (PW / 2 - 0.1, -0.14, taban), 0.025, izg)
    for i in range(-6, 7):
        boru((i * 0.18, -0.14, taban), (i * 0.75, -0.14, -PH / 2 + 0.1), 0.012, izg)
    for j in range(1, 5):
        zz = taban - (j / 4) ** 1.6 * 1.15
        boru((-PW / 2 + 0.1, -0.14, zz), (PW / 2 - 0.1, -0.14, zz), 0.012, izg)
    # spot huzmeleri: ustten acilan yari saydam beyaz kamalar
    rnd = random.Random(13 if oyuncu == "p1" else 17)
    for i in range(7):
        x0 = -PW / 2 + 0.4 + i * (PW - 0.8) / 6
        x1 = x0 + rnd.uniform(-0.9, 0.9)
        bpy.ops.mesh.primitive_plane_add(size=1, location=(0, -0.13, 0), rotation=(math.pi / 2, 0, 0))
        k_ = bpy.context.active_object
        v = k_.data.vertices
        ust, alt = PH / 2 - 0.05, taban - 0.2
        # duzlem kose sirasi: (-,-) (+,-) (-,+) (+,+) yerel; Rx(90) sonrasi yerel y -> dunya z
        coords = [(x1 - 0.55, alt), (x1 + 0.55, alt), (x0 - 0.06, ust), (x0 + 0.06, ust)]
        for vi, (xx, zz) in zip(v, coords):
            vi.co = Vector((xx, zz, 0))
        hm = bpy.data.materials.new("huzme%d" % i); hm.use_nodes = True; hn = hm.node_tree; hn.nodes.clear()
        tc2 = hn.nodes.new("ShaderNodeTexCoord"); sp2 = hn.nodes.new("ShaderNodeSeparateXYZ"); hn.links.new(tc2.outputs["Generated"], sp2.inputs[0])
        r2 = hn.nodes.new("ShaderNodeValToRGB"); c3 = r2.color_ramp
        c3.elements[0].position = 0.0; c3.elements[0].color = (0, 0, 0, 1)
        c3.elements[1].position = 1.0; c3.elements[1].color = (0.55, 0.55, 0.55, 1)
        hn.links.new(sp2.outputs["Y"], r2.inputs[0])
        e2 = hn.nodes.new("ShaderNodeEmission"); e2.inputs[0].default_value = (*(acik(R, 0.45) if KAPAK else (1, 1, 1)), 1); e2.inputs[1].default_value = 2.2
        tr = hn.nodes.new("ShaderNodeBsdfTransparent"); mx2 = hn.nodes.new("ShaderNodeMixShader")
        hn.links.new(r2.outputs[0], mx2.inputs[0]); hn.links.new(tr.outputs[0], mx2.inputs[1]); hn.links.new(e2.outputs[0], mx2.inputs[2])
        o2 = hn.nodes.new("ShaderNodeOutputMaterial"); hn.links.new(mx2.outputs[0], o2.inputs[0])
        hm.blend_method = "BLEND"
        k_.data.materials.append(hm)
    par = mat_emis("parilti", (1, 1, 1), 10.0)
    for i in range(90):
        kure((rnd.uniform(-PW / 2 + 0.2, PW / 2 - 0.2), -0.16, rnd.uniform(taban - 0.1, PH / 2 - 0.2)), rnd.choice([0.012, 0.02, 0.03, 0.045]), par, sub=1)
    panel_kamera(sc)
    if KAPAK:
        sc.view_settings.exposure = POZ_KAPAK
    yaz(sc, ON + "panel2-%s.png" % oyuncu)


# ------------------------------------------------------------------ ana akis (disko)
if YALNIZ in ("hepsi", "poz"):
    poz_maskeleri()
if YALNIZ in ("hepsi", "sahne", "gok"):
    gok_disko()
if YALNIZ in ("hepsi", "sahne", "serit", "kapak"):
    for o_ in ("p1", "p2"):
        serit_disko(o_)
if KAPAK:
    gok_disko()
if KAPAK:              # 24 Eki kural: kapak doygunlugu = referans -> kapi icindeki spot paneli de doygun
    for o_ in ("p1", "p2"):
        panel_sahne_disko(o_)
if YALNIZ in ("hepsi", "sahne", "panel"):
    for o_ in ("p1", "p2"):
        panel_girdap_disko(o_)
        panel_sahne_disko(o_)
json.dump(YERLESIM, open(os.path.join(CIKTI, "yerlesim.json"), "w"), indent=1)
log("bitti (disko)", {k: v for k, v in YERLESIM.items() if k.startswith("aciklik")})
