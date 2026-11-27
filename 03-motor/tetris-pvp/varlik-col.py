"""HUMAN TETRIS 41. video (REF-093 yapi, 1P SOLO) - GUNDUZ COL VAHASI, CILALI 3D OYUN GORUNUMU, TEK serit.
varlik.py calistirir (--mod col). Iskelet varlik-buz.py (40, tek serit) - katmanlar, kamera, yerlesim anahtarlari ayni
(tek serit motoru 33/35/36/37'nin bekledigi aciklik_p1 / ampul_p1 / dag / yol).

Mekan kullanici karari (27 Kas 2026, A): gunduz, parlak gunes. Pist sikistirilmis altin kum + ruzgar dalgaciklari + parlak yon oklari;
iki yanda palmiyeler, turkuaz vaha golu, renkli cizgili cadirlar, comlekler, sandiklar, kaktusler; arkada dalga dalga kum tepeleri,
uzakta kumtasi kayalar, doygun mavi gok; gokte ucurtmalar + kum pariltisi. Kapi: kumtasi kemer + renkli kilim sarkitlari + fener dizisi + tabela.
OUT ani: duvar karakteri pistin yanindaki KUM TEPESINE iter, karakter asagi yuvarlanir (kum pufu motorda).
Telif (md. 16): genel col/vaha ogeleri; bilinen film (lamba, sihirli hali, karakter) yok.
prompts.chat (md. 23): "desert oasis" / "fennec fox" 0 sonuc -> kendi plan.
§4 CILALI 3D OYUN GORUNUMU: doygun renk, tombul hatlar, parlak kaplama (coat), gercek isik-golge (Cycles); foto dokusu yok.
§8 SOLUK YASAK: kum bej degil altin-turuncu (HT26 plaj dersi #ffcf5c/#ffbd45), gok derin mavi, cadir/kilim tam doygun.
Ekran dolu (Masaustu md. 7): gok bolgesi ucurtma + kum pariltisi + tombul bulut + ufukta kayalar; zemin ufka kadar kum tepeleri.
"""

import random
YERLESIM.clear()
KAPAK = YALNIZ == "kapak"
POZLAMA = float(arg("--pozlama", arg("--kapak-pozlama", "0")))
GUNES = float(arg("--gunes", "3.4"))
ON_EK = "kapak-" if KAPAK else ""
KAP = {"y": 8.6, "w": 7.4, "h": 3.7, "kalin": 0.55}       # tek serit motoru ile ayni olcu
KAM = {"z": 2.3, "egim": 5.0, "lens": 18.0, "sensor": 24.0}
if KAPAK:
    KAM.update({"z": float(arg("--kapak-z", "2.0")), "egim": float(arg("--kapak-egim", "3.0")), "lens": float(arg("--kapak-lens", "16.0"))})
PIST = 3.9
GECIS = 11.5
GOK_UFUK, GOK_ORTA, GOK_UST = "#5ad0ff", "#1a9aff", "#0a52f0"      # acik camgobegi ufuk -> derin mavi (beyaz-gri degil)
SIS = "#6ac4ff"                                            # mist: uzak tepeler acik gok mavisine karisir (sahne 1: sicak altin sis gok mavisiyle karisip leylak yapti)
KDOY = KAPAK and arg("--kapak-doygun", "0") != "0"
KGB = KAPAK and arg("--kapak-doygun", "0") == "2"        # HT41 kapak: GUN BATIMI (REF-093 gece mor neon tunel 0,685 / 0,567 / 0,520;
if KDOY:                                                  # gunduz col 0,62 / 0,83 -> doygun turuncu-pembe-mor gok, parlaklik duser, doygunluk artar)
    GOK_UFUK, GOK_ORTA, GOK_UST = "#2a9aff", "#0a62ff", "#0a2ad8"
    SIS = "#2a8aff"
if KGB:
    GOK_UFUK, GOK_ORTA, GOK_UST = "#ff7a0a", "#ff1a6a", "#5a0aa8"
    SIS = "#ff4a5a"
KGC = KAPAK and arg("--kapak-doygun", "0") == "3"        # HT41 kapak tur 2: GECE NEON VAHA (REF-093 mor neon tunel havasi; HT39 gece resif emsali)
if KGC:
    GOK_UFUK, GOK_ORTA, GOK_UST = "#8a1ad8", "#3a0aa8", "#0a0440"
    SIS = "#5a0ac8"
ISIK_K = 2.0 if KGC else 1.0                              # gece: fener / ampul / bayrak isiklari daha guclu
KUM, KUM_A, KUM_G = "#ffbd45", "#ffcf5c", "#f08a1a"        # altin kum + acik tepe tonu + turuncu golge (bej degil)
if KAPAK and arg("--kapak-doygun", "0") != "0":            # HT41 kapak tur 1: kum 0,58 doygunlukta kaldi -> kapakta doygun turuncu kum
    KUM, KUM_A, KUM_G = "#ff9a10", "#ffb020", "#e0580a"
TAS, TAS_A = "#e0742a", "#f2a04a"                          # kumtasi: kiremit turuncu + acik
PALM = ("#18b83a", "#0aa04a", "#3ac81a")                   # palmiye yapragi yesilleri
CADIR = ("#ff1a4a", "#0ac8c8", "#9a2aff", "#ff7a0a", "#1a6aff", "#ff2ab8")   # cadir/kilim/bayrak renkleri
AMPUL = ("#ffb81a", "#ff6a1a", "#ffd84a", "#ff3a6a", "#2ae0d0")


# ------------------------------------------------------------------ sahne / isik
def koy_sahnesi(w, h, saydam):
    sc = bos_sahne(w=w, h=h, saydam=saydam, ornek=ORNEK, doygun=True)
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.exposure = POZLAMA
    sc.cycles.max_bounces = 6; sc.cycles.diffuse_bounces = 3; sc.cycles.glossy_bounces = 3
    sc.cycles.transmission_bounces = 4; sc.cycles.transparent_max_bounces = 8
    sc.cycles.use_light_tree = True
    nt = sc.world.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord"); sp = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Generated"], sp.inputs[0])
    rp = nt.nodes.new("ShaderNodeValToRGB"); el = rp.color_ramp.elements
    el[0].position = 0.0; el[0].color = (*lin(hex3(GOK_UFUK)), 1)
    el[1].position = 0.45; el[1].color = (*lin(hex3(GOK_UST)), 1)
    e2 = el.new(0.14); e2.color = (*lin(hex3(GOK_ORTA)), 1)
    nt.links.new(sp.outputs["Z"], rp.inputs[0])
    lp = nt.nodes.new("ShaderNodeLightPath")
    bg_k = nt.nodes.new("ShaderNodeBackground"); bg_k.inputs[1].default_value = 1.0
    nt.links.new(rp.outputs[0], bg_k.inputs[0])
    bg_i = nt.nodes.new("ShaderNodeBackground"); bg_i.inputs[1].default_value = 0.55
    bg_i.inputs[0].default_value = (*lin(hex3("#7a2aff" if KGC else "#b04aff" if KGB else "#6aa8ff")), 1)
    if KGC:
        bg_i.inputs[1].default_value = 0.9        # gok ortam isigi: mavi dolgu (kum golgesi kahve degil)
    mx = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(lp.outputs["Is Camera Ray"], mx.inputs[0])
    nt.links.new(bg_i.outputs[0], mx.inputs[1]); nt.links.new(bg_k.outputs[0], mx.inputs[2])
    o = nt.nodes.new("ShaderNodeOutputWorld"); nt.links.new(mx.outputs[0], o.inputs[0])
    sc.view_layers[0].use_pass_mist = True
    sc.world.mist_settings.start = 60.0; sc.world.mist_settings.depth = 420.0; sc.world.mist_settings.falloff = "QUADRATIC"
    sc.use_nodes = True; sc.render.use_compositing = True; ct = sc.node_tree; ct.nodes.clear()
    rl = ct.nodes.new("CompositorNodeRLayers"); co = ct.nodes.new("CompositorNodeComposite")
    mk = ct.nodes.new("CompositorNodeMath"); mk.operation = "MULTIPLY"; mk.inputs[1].default_value = 0.3 if KDOY else 0.35
    ct.links.new(rl.outputs["Mist"], mk.inputs[0])
    mm = ct.nodes.new("CompositorNodeMixRGB"); mm.blend_type = "MIX"
    ct.links.new(mk.outputs[0], mm.inputs[0]); ct.links.new(rl.outputs["Image"], mm.inputs[1])
    mm.inputs[2].default_value = (*lin(hex3(SIS)), 1)
    gl = ct.nodes.new("CompositorNodeGlare"); gl.glare_type = "FOG_GLOW"; gl.quality = "HIGH"; gl.threshold = 1.2; gl.size = 6; gl.mix = -1.0 if KDOY else -0.6   # HT38 dersi: fog glow renkliligi dusurur
    ct.links.new(mm.outputs[0], gl.inputs[0]); ct.links.new(gl.outputs[0], co.inputs[0])
    if saydam:
        ct.links.new(rl.outputs["Alpha"], co.inputs[1])
    return sc


def kamera(sc):
    rx = math.radians(90 - KAM["egim"])
    bpy.ops.object.camera_add(location=(0, 0, KAM["z"]), rotation=(rx, 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.sensor_fit = "VERTICAL"; kam.data.sensor_height = KAM["sensor"]; kam.data.lens = KAM["lens"]
    kam.data.clip_end = 2500
    if KAPAK and arg("--kapak-dof", "0") != "0":            # mobil kapak (md. 30): kapi net, arka plan yumusak bulanik
        kam.data.dof.use_dof = True; kam.data.dof.focus_distance = KAP["y"]; kam.data.dof.aperture_fstop = float(arg("--kapak-dof", "1.2"))
    return kam


def isiklar():
    # yuksek sicak col gunesi (onden-yandan) -> kumda kisa sicak golge, kaplamada parlama; mavi gok dolgu
    bpy.ops.object.light_add(type="SUN", location=(0, 0, 30))
    g = bpy.context.active_object; g.data.energy = GUNES * (0.8 if KGB else 0.55 if KGC else 1.0); g.data.angle = math.radians(2.5)
    g.data.color = lin(hex3("#ff9a4a" if KGB else "#ff4ad0" if KGC else "#fff0d0"))
    g.rotation_euler = Vector((0.4, 0.45, -0.85) if not KGB else (0.15, 0.95, -0.28)).to_track_quat("-Z", "Y").to_euler()   # gun batimi: alcak, karsidan
    bpy.ops.object.light_add(type="SUN", location=(0, 0, 30))
    f = bpy.context.active_object; f.data.energy = 0.8; f.data.angle = math.radians(12.0)
    f.data.color = lin(hex3("#c06aff" if KGB else "#3ad8ff" if KGC else "#9ac0ff"))
    if KGC:
        f.data.energy = 1.6
    f.rotation_euler = Vector((-0.4, -0.7, -0.55)).to_track_quat("-Z", "Y").to_euler()


# ------------------------------------------------------------------ malzemeler
_SM = {}


def mat_pbr(ad, renk, purluk, metal=0.0, kaplama=0.0, ss=0.0):
    m = bpy.data.materials.new(ad); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*lin(hex3(renk)), 1)
    b.inputs["Roughness"].default_value = purluk; b.inputs["Metallic"].default_value = metal
    b.inputs["Coat Weight"].default_value = kaplama; b.inputs["Coat Roughness"].default_value = 0.06
    if ss > 0:
        b.inputs["Subsurface Weight"].default_value = ss; b.inputs["Subsurface Radius"].default_value = (0.4, 0.6, 1.0)
    return m


def mat_m(renk, purluk=0.35, kaplama=0.5, ss=0.0, metal=0.0):
    key = ("m", renk, purluk, kaplama, ss, metal)
    if key not in _SM:
        _SM[key] = mat_pbr("m" + renk, renk, purluk, metal=metal, kaplama=kaplama, ss=ss)
    return _SM[key]


def mat_isik(renk, guc=4.0):
    key = ("i", renk, guc)
    if key not in _SM:
        _SM[key] = mat_emis("isik" + renk, lin(hex3(renk)), guc * ISIK_K)
    return _SM[key]


def mat_kum(ad="kum", acik=False, dalga=True):
    """altin kum: noise ile altin <-> turuncu ton + ruzgar dalgacigi (wave) kabartmasi; bej/gri degil"""
    if ad in _SM:
        return _SM[ad]
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    ns = nt.nodes.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value = 0.35; ns.inputs["Detail"].default_value = 3
    nt.links.new(geo.outputs["Position"], ns.inputs["Vector"])
    rp = nt.nodes.new("ShaderNodeValToRGB"); el = rp.color_ramp.elements
    el[0].position = 0.3; el[0].color = (*lin(hex3(KUM_G if not acik else KUM)), 1)
    el[1].position = 0.72; el[1].color = (*lin(hex3(KUM_A if acik else KUM)), 1)
    nt.links.new(ns.outputs["Fac"], rp.inputs[0]); nt.links.new(rp.outputs[0], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.55
    b.inputs["Coat Weight"].default_value = 0.12; b.inputs["Coat Roughness"].default_value = 0.2
    if dalga:
        wv = nt.nodes.new("ShaderNodeTexWave"); wv.wave_type = "BANDS"; wv.bands_direction = "Y"
        wv.inputs["Scale"].default_value = 0.9; wv.inputs["Distortion"].default_value = 4.0; wv.inputs["Detail"].default_value = 2
        nt.links.new(geo.outputs["Position"], wv.inputs["Vector"])
        bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.1   # sahne 1: 0,35 oluklu sac gibi okundu
        nt.links.new(wv.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    _SM[ad] = m
    return m


def mat_su():
    """vaha golu: doygun turkuaz, parlak kaplama, hafif ic isik (gri yansima degil)"""
    if "su" in _SM:
        return _SM["su"]
    m = mat_pbr("vaha_su", "#0ac8d0", 0.05, kaplama=0.9)
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Emission Color"].default_value = (*lin(hex3("#0ad8d8")), 1); b.inputs["Emission Strength"].default_value = 0.25
    _SM["su"] = m
    return m


def kutu(ad, merkez, boyut, mat, egim=0.03, seg=3):
    if egim > 0:
        return yuvarlak_kutu(ad, merkez, boyut, mat, egim=egim, seg=seg)
    bpy.ops.mesh.primitive_cube_add(size=1, location=merkez)
    o = bpy.context.active_object; o.name = ad; o.scale = boyut
    bpy.ops.object.transform_apply(scale=True)
    o.data.materials.append(mat)
    return o


def silindir(konum, r, h, mat, v=40, r2=None, bevel=0.0):
    x, y, z = konum
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, location=(x, y, z + h / 2), vertices=v)
    else:
        bpy.ops.mesh.primitive_cone_add(radius1=r, radius2=r2, depth=h, location=(x, y, z + h / 2), vertices=v)
    o = bpy.context.active_object; o.data.materials.append(mat)
    if bevel > 0:
        bv = o.modifiers.new("egim", "BEVEL"); bv.width = bevel; bv.segments = 4; bv.limit_method = "ANGLE"
    bpy.ops.object.shade_smooth()
    return o


def egik_boru(a, b, r, mat, r2=None, v=14):
    a, b = Vector(a), Vector(b); d = b - a
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d.length, location=(a + b) / 2, vertices=v)
    else:
        bpy.ops.mesh.primitive_cone_add(radius1=r, radius2=r2, depth=d.length, location=(a + b) / 2, vertices=v)
    o = bpy.context.active_object; o.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
    o.data.materials.append(mat); bpy.ops.object.shade_smooth()
    return o


def ucgen(p0, p1, p2, mat):
    me = bpy.data.meshes.new("ucgen"); me.from_pydata([tuple(p0), tuple(p1), tuple(p2)], [], [[0, 1, 2]]); me.update()
    o = bpy.data.objects.new("ucgen", me); bpy.context.collection.objects.link(o); o.data.materials.append(mat)
    o.modifiers.new("k", "SOLIDIFY").thickness = 0.015
    return o


# ------------------------------------------------------------------ ogeler
def palmiye(x, y, H, rnd, hindistan=True):
    """tombul palmiye: hafif kavisli halka halka govde + tepede 8 sarkik yaprak (basik uzun kure) + hindistancevizi"""
    kah = (mat_m("#a85a1a", 0.6, 0.1), mat_m("#c8782a", 0.6, 0.1))
    egr = rnd.uniform(-0.25, 0.25) * H; n = 7; p = Vector((x, y, 0))
    for i in range(n):
        t = (i + 1) / n
        q = Vector((x + egr * t * t, y, H * t))
        egik_boru(p, q, 0.11 * H * (1.05 - 0.35 * t), kah[i % 2], r2=0.1 * H * (1.0 - 0.35 * t), v=12)
        p = q
    yaprak = mat_m(rnd.choice(PALM), 0.45, 0.3)
    for j in range(8):
        a = j * 0.785 + rnd.uniform(-0.15, 0.15)
        d = Vector((math.cos(a), math.sin(a), 0))
        k = kure(p + d * 0.42 * H + Vector((0, 0, -0.05 * H)), 0.46 * H, yaprak, sub=2)
        k.scale = (1.0, 0.22, 0.07); k.rotation_euler = (0, 0.35, a)
    if hindistan:
        for j in range(3):
            a = j * 2.1
            kure(p + Vector((math.cos(a) * 0.1 * H, math.sin(a) * 0.1 * H, -0.08 * H)), 0.06 * H, mat_m("#6a3a1a", 0.5, 0.3), sub=1)


def kaktus(x, y, H, rnd):
    """tombul kaktus: yesil govde + iki kol + tepede pembe cicek"""
    km = mat_m("#1aa84a", 0.45, 0.35)
    silindir((x, y, 0), 0.16 * H, H, km, v=16); kure((x, y, H), 0.16 * H, km, sub=2)
    for s in (-1, 1):
        zb = H * rnd.uniform(0.35, 0.55); L = 0.28 * H
        egik_boru((x, y, zb), (x + s * L, y, zb), 0.1 * H, km, v=12)
        silindir((x + s * L, y, zb), 0.1 * H, 0.3 * H, km, v=12); kure((x + s * L, y, zb + 0.3 * H), 0.1 * H, km, sub=2)
    kure((x, y, H + 0.15 * H), 0.07 * H, mat_m("#ff2a9a", 0.3, 0.6), sub=1)


def cadir(x, y, s, rnd):
    """renkli cizgili cadir: 8 dilimli koni (iki renk sirayla) + tepede bayrak"""
    r1, r2 = rnd.sample(CADIR, 2)
    for i in range(8):
        a0, a1 = i * 0.785, (i + 1) * 0.785
        p0 = Vector((x + math.cos(a0) * 1.2 * s, y + math.sin(a0) * 1.2 * s, 0))
        p1 = Vector((x + math.cos(a1) * 1.2 * s, y + math.sin(a1) * 1.2 * s, 0))
        ucgen(p0, p1, Vector((x, y, 1.9 * s)), mat_m(r1 if i % 2 == 0 else r2, 0.5, 0.2))
    egik_boru((x, y, 1.85 * s), (x, y, 2.4 * s), 0.025 * s, mat_m("#ffc81a", 0.3, 0.5, metal=0.5), v=8)
    ucgen((x, y, 2.4 * s), (x, y, 2.15 * s), (x + 0.4 * s, y, 2.28 * s), mat_m(rnd.choice(CADIR), 0.4, 0.3))


def comlek(x, y, s, rnd):
    """toprak comlek: tombul govde + boyun + turkuaz serit"""
    k = kure((x, y, 0.32 * s), 0.34 * s, mat_m("#d8602a", 0.5, 0.35), sub=2); k.scale = (1, 1, 0.95)
    silindir((x, y, 0.58 * s), 0.14 * s, 0.18 * s, mat_m("#d8602a", 0.5, 0.35), v=16, r2=0.18 * s)
    silindir((x, y, 0.3 * s), 0.345 * s, 0.06 * s, mat_m("#0ac8c8", 0.3, 0.6), v=24)


def sandik(x, y, s, rnd):
    """ahsap sandik: kahve govde + altin kosebent"""
    kutu("sandik", (x, y, 0.3 * s), (0.8 * s, 0.55 * s, 0.6 * s), mat_m("#9a4a1a", 0.55, 0.2), egim=0.04 * s)
    for dx in (-0.36, 0.36):
        kutu("serit", (x + dx * s, y, 0.3 * s), (0.08 * s, 0.57 * s, 0.62 * s), mat_m("#ffb81a", 0.25, 0.6, metal=0.6), egim=0.01 * s)


def kum_tepesi(x, y, r, h, ad="tepe_kum"):
    """yumusak kum tepesi: basik dev kure, kum malzemesi"""
    k = kure((x, y, -h * 0.35), r, mat_kum(ad, acik=True), sub=3); k.scale = (1.0, 0.55, h / r)
    return k


def kaya(x, y, s, rnd):
    """kumtasi kaya kumesi: ust uste 2-3 yuvarlak blok (kiremit turuncu)"""
    z = 0.0
    for i in range(rnd.randint(2, 3)):
        w = s * rnd.uniform(0.8, 1.2) * (1 - i * 0.2); hh = s * rnd.uniform(0.5, 0.8)
        yuvarlak_kutu("kaya", (x + rnd.uniform(-0.2, 0.2) * s, y, z + hh / 2), (w, w * 0.8, hh), mat_m(rnd.choice((TAS, TAS_A, "#d0602a")), 0.6, 0.15), egim=0.25 * s, seg=3)
        z += hh * 0.92


def fener(x, y, H):
    """fener diregi: koyu ahsap direk + ustte pirinc kafes icinde sicak isik"""
    silindir((x, y, 0), 0.07, H, mat_m("#5a2a0a", 0.5, 0.2), v=12)
    kutu("fener", (x, y, H + 0.2), (0.28, 0.28, 0.38), mat_isik("#ffb84a", 5.0), egim=0.04)
    silindir((x, y, H + 0.39), 0.2, 0.18, mat_m("#ffb81a", 0.25, 0.6, metal=0.7), v=12, r2=0.03)


def bayrak_dizisi(a, b, n, sark=0.35):
    """iki nokta arasinda sarkan renkli ucgen bayrak dizisi (kilim/senlik)"""
    a, b = Vector(a), Vector(b); nok = []
    for i in range(n + 1):
        t = i / n; p = a.lerp(b, t); p.z -= sark * 4 * t * (1 - t); nok.append(p)
    km = mat_m("#3a1a0a", 0.5, 0.0)
    for i in range(n):
        egik_boru(nok[i], nok[i + 1], 0.012, km, v=6)
        m = (nok[i] + nok[i + 1]) / 2
        ucgen(nok[i] + Vector((0, -0.02, 0)), nok[i + 1] + Vector((0, -0.02, 0)), m + Vector((0, -0.02, -0.32)), mat_m(CADIR[i % len(CADIR)], 0.4, 0.4))


def ucurtma(x, y, z, s, rnd):
    """gokte ucurtma: iki renkli eskenar dortgen + kuyruk fiyonklari"""
    r1, r2 = rnd.sample(CADIR, 2)
    u, d, l_, r_ = Vector((x, y, z + s)), Vector((x, y, z - 1.4 * s)), Vector((x - 0.7 * s, y, z)), Vector((x + 0.7 * s, y, z))
    c = Vector((x, y, z))
    ucgen(u, l_, c, mat_m(r1, 0.4, 0.4)); ucgen(u, c, r_, mat_m(r2, 0.4, 0.4))
    ucgen(l_, d, c, mat_m(r2, 0.4, 0.4)); ucgen(c, d, r_, mat_m(r1, 0.4, 0.4))
    p = d
    for i in range(4):
        q = p + Vector((0.25 * s * math.sin(i * 1.3), 0, -0.45 * s))
        egik_boru(p, q, 0.015 * s, mat_m("#ffffff", 0.5, 0.0), v=5)
        kure(q, 0.09 * s, mat_m(CADIR[(i + 2) % len(CADIR)], 0.4, 0.4), sub=1)
        p = q


def bulut(x, y, z, s, rnd):
    """tombul beyaz bulut: 4-6 kure kumesi (ekran dolu, gok ust bolgesi)"""
    bm = mat_m("#ffffff", 0.8, 0.0)
    for _ in range(rnd.randint(4, 6)):
        k = kure((x + rnd.uniform(-1.4, 1.4) * s, y, z + rnd.uniform(-0.2, 0.4) * s), s * rnd.uniform(0.6, 1.0), bm, sub=2)
        k.scale = (1.0, 0.6, 0.7)


# ------------------------------------------------------------------ MEKAN (her iki katmanda; serit sahnesinde uzak kisim holdout)
def mekan(serit_modu, rnd):
    _SM.clear()                                         # ikinci katmanda bos_sahne eski malzemeleri siliyor (36 dersi)
    me = bpy.data.meshes.new("yakin_zemin")
    me.from_pydata([(-60, -4, -0.02), (60, -4, -0.02), (60, GECIS, -0.02), (-60, GECIS, -0.02)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("yakin_zemin", me); bpy.context.collection.objects.link(o); o.data.materials.append(mat_kum("zemin_kum"))
    # yakin kenar: palmiye + cadir + comlek/sandik + kaktus + fenerler (koridor bos; OUT kum tepelerinin yeri acik)
    for s in (-1, 1):
        for (x, y, k) in ((10.5, 2.0, 4.6), (14.5, 7.5, 5.8), (9.2, 10.2, 4.0), (19.5, 3.5, 6.4), (17.0, 10.8, 5.2)):
            palmiye(s * x, y, k, rnd)
        cadir(s * 13.0, 4.4, 1.5, rnd)
        for (x, y, k) in ((8.2, 0.4, 1.0), (11.4, 8.8, 1.2), (7.8, 6.6, 0.9)):
            comlek(s * x, y, k, rnd) if rnd.random() < 0.6 else sandik(s * x, y, k, rnd)
        kaktus(s * 16.5, 0.6, 2.2, rnd); kaktus(s * 7.4, 9.6, 1.6, rnd)
        for y in (-1.0, 3.4, 7.6):
            fener(s * (PIST + 1.5), y, 2.0)
    # vaha golu (yakin sol, uzak sag): turkuaz su + kiyida palmiye
    for (gx, gy, gr) in ((-15.0, 9.0, 3.2), (17.0, 15.0, 4.0)):
        k = kure((gx, gy, -0.25), gr, mat_su(), sub=3); k.scale = (1.4, 0.8, 0.08)
    for y in (-1.0, 3.4):                                  # fenerler arasinda sarkan bayrak dizileri (her iki yan)
        for s in (-1, 1):
            bayrak_dizisi((s * (PIST + 1.5), y, 2.15), (s * (PIST + 1.5), y + 4.4, 2.15), 8, sark=0.25)
    for o in bpy.data.objects:
        if o.type == "MESH":
            o["yakin"] = 1
    # uzak: kum ufka kadar, iki yanda palmiye/cadir seridi, dalga dalga kum tepeleri, kumtasi kayalar
    me = bpy.data.meshes.new("kum_uzak")
    me.from_pydata([(-420, GECIS, -0.05), (420, GECIS, -0.05), (420, 520, -0.05), (-420, 520, -0.05)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("kum_uzak", me); bpy.context.collection.objects.link(o); o.data.materials.append(mat_kum("kum_uzak", acik=True, dalga=False))
    for s in (-1, 1):                                      # iki yan: vaha seridi (kapi arkasi ve orta koridor acik)
        y = GECIS + 2
        while y < 150:
            sc = 1.0 + y / 40
            x = s * rnd.uniform(11, 16) * (1 + y / 70)
            palmiye(x, y, 5.0 * sc * rnd.uniform(0.8, 1.25), rnd, hindistan=y < 60)
            if rnd.random() < 0.45:
                kum_tepesi(x + s * 5 * sc, y + 2 * sc, 3.2 * sc, 1.6 * sc)
            if rnd.random() < 0.2 and y < 90:
                cadir(x + s * 7 * sc, y + 3 * sc, 1.5 * sc, rnd)
            if rnd.random() < 0.25:
                kaktus(x - s * 2.4 * sc, y + 1 * sc, 1.8 * sc, rnd)
            y += 4.5 * sc
    for _ in range(60):                                    # orta mesafe kum tepeleri (ufuk dolu)
        x = rnd.uniform(-300, 300); y = rnd.uniform(140, 320)
        if abs(x) < 18 + y * 0.05:
            continue
        kum_tepesi(x, y, rnd.uniform(14, 30), rnd.uniform(5, 12))
    for _ in range(14):
        kaya(rnd.uniform(-260, 260), rnd.uniform(200, 360), rnd.uniform(8, 16), rnd)
    for (x, y, r, h) in ((-170, 430, 160, 70), (40, 470, 200, 90), (240, 420, 150, 62), (-340, 470, 170, 80), (390, 480, 170, 72)):
        kum_tepesi(x, y, r, h, ad="dev_tepe")              # dev kum tepeleri (gokun alt yarisini doldurur)
    # gok: ucurtmalar + tombul bulutlar + kum pariltisi (ekran dolu)
    for _ in range(26):
        x = rnd.uniform(-34, 34); y = rnd.uniform(18, 46); z = rnd.uniform(5, 20)
        if abs(x) < 6 and z < 8:
            continue
        ucurtma(x, y, z, rnd.uniform(0.35, 0.7) * (1 + y / 40), rnd)
    for _ in range(9):
        bulut(rnd.uniform(-60, 60), rnd.uniform(60, 110), rnd.uniform(22, 40), rnd.uniform(2.5, 4.5), rnd)
    pm = mat_isik("#ffc23a", 2.5)                       # sahne 1: acik parilti kar gibi okundu -> sicak altin, seyrek
    for _ in range(140):
        x = rnd.uniform(-30, 30); y = rnd.uniform(4, 60); z = rnd.uniform(0.8, 18)
        if abs(x) < 5 and y < 14:
            continue
        kure((x, y, z), rnd.uniform(0.03, 0.07) * (1 + y / 30), pm, sub=1)
    if serit_modu:
        for o in bpy.data.objects:
            if o.type == "MESH" and not o.get("yakin"):
                o.is_holdout = True


# ------------------------------------------------------------------ SERIT: kum pist + ruzgar dalgaciklari + ahsap korkuluk + oklar + OUT kum tepeleri
def serit_esyalari(rnd):
    kutu("pist", (0, (KAP["y"] + 0.4 - 4) / 2, 0.0), (PIST * 2, KAP["y"] + 4.4, 0.16), mat_kum("pist_kum", acik=True), egim=0.04, seg=2)
    iz = mat_m("#e8781a", 0.5, 0.2)
    for k in range(4):                                    # ruzgar dalgaciklari: yatay hafif kivrimli turuncu cizgiler
        y0 = (-1.6, 0.6, 2.8, 5.0)[k] + rnd.uniform(-0.2, 0.2); a = rnd.uniform(0.08, 0.15); f = rnd.uniform(0.8, 1.2); ph = rnd.uniform(0, 6)
        x = -PIST + 0.3
        while x < PIST - 0.8:
            egik_boru((x, y0 + a * math.sin(f * x + ph), 0.165), (x + 0.5, y0 + a * math.sin(f * (x + 0.5) + ph), 0.165), 0.014, iz, v=6)
            x += 0.5
    for s in (-1, 1):                                     # pist kenari: alcak kumtasi bordur
        kutu("bordur", (s * (PIST + 0.2), (KAP["y"] - 3.4) / 2, 0.12), (0.45, KAP["y"] + 2.6, 0.26), mat_m(TAS, 0.55, 0.25), egim=0.08, seg=3)
    for s in (-1, 1):                                     # korkuluk: ahsap direkler + ustte isik + ip
        y = -3.0; i = 0
        while y < KAP["y"] - 0.4:
            silindir((s * (PIST + 0.5), y, 0.2), 0.07, 0.65, mat_m("#8a3a0a", 0.5, 0.3), v=12)
            kure((s * (PIST + 0.5), y, 0.95), 0.1, mat_isik(AMPUL[i % len(AMPUL)], 5.0), sub=1)
            y += 1.3; i += 1
        kutu("ip", (s * (PIST + 0.5), (KAP["y"] - 3.4) / 2, 0.7), (0.05, KAP["y"] + 2.6, 0.05), mat_m("#f0d8a0", 0.6, 0.0), egim=0)
    for j, x in enumerate((-1.7, 1.7)):                   # yon oklari: turkuaz ve pembe (altin kumda okunur)
        ok = mat_m("#0ac8d8" if j == 0 else "#ff2a8a", 0.25, 0.8)
        for y in (4.6, 6.2):
            nok = [(x - 0.6, y - 0.4), (x, y), (x + 0.6, y - 0.4), (x + 0.6, y - 0.68), (x, y - 0.28), (x - 0.6, y - 0.68)]
            me = bpy.data.meshes.new("ok"); me.from_pydata([(a, b, 0.17) for a, b in nok], [], [list(range(6))]); me.update()
            o = bpy.data.objects.new("ok", me); bpy.context.collection.objects.link(o); o.data.materials.append(ok)
            o.modifiers.new("k", "SOLIDIFY").thickness = 0.02
    for s in (-1, 1) if not KDOY else ():                 # OUT ani: iki dis tarafta yuksek kum tepesi (karakter asagi yuvarlanir)
        kum_tepesi(s * 5.8, 5.0, 1.8, 1.3, ad="out_kum")


def kapi():
    """kumtasi kemer: iki kumtasi blok kule + tepede kubbe ve altin tepelik, kiris onunde turkuaz mozaik serit
    + kiris altinda renkli kilim sarkitlari + fener dizisi (motor ampul_p1 hatti) + LED tabela"""
    Y, W_, H_, K = KAP["y"], KAP["w"], KAP["h"], KAP["kalin"]
    xk = W_ / 2 + K / 2
    rnd = random.Random(411)
    for s in (-1, 1):
        n = 5; dh = (H_ + K + 0.2) / n
        for i in range(n):                                # kumtasi bloklari (hafif kaydirmali)
            yuvarlak_kutu("tas_blok", (s * xk + rnd.uniform(-0.05, 0.05), Y, i * dh + dh / 2), (K * 1.3, K * 1.3, dh * 0.94),
                          mat_m((TAS, TAS_A, "#d8662a")[i % 3], 0.55, 0.3), egim=0.07, seg=3)
        k = kure((s * xk, Y, H_ + K + 0.25), K * 0.75, mat_m("#0ab8c0", 0.25, 0.7), sub=3); k.scale = (1, 1, 1.15)   # turkuaz kubbe
        egik_boru((s * xk, Y, H_ + K + 0.95), (s * xk, Y, H_ + K + 1.35), 0.06, mat_m("#ffc81a", 0.2, 0.8, metal=0.8), r2=0.01, v=8)
        kure((s * xk, Y, H_ + K + 1.0), 0.09, mat_m("#ffc81a", 0.2, 0.8, metal=0.8), sub=1)
    yuvarlak_kutu("kiris", (0, Y, H_ + K / 2), (W_ + 2 * K, K + 0.1, K), mat_m(TAS, 0.55, 0.3), egim=0.12, seg=4)
    for i in range(18):                                   # kiris onunde turkuaz/altin mozaik kareler
        x = -W_ / 2 - K + 0.3 + i * (W_ + 2 * K - 0.6) / 17
        kutu("mozaik", (x, Y - K / 2 - 0.07, H_ + K * 0.72), (0.22, 0.04, 0.22), mat_m(("#0ac8c8", "#ffc81a", "#1a6aff")[i % 3], 0.2, 0.8), egim=0.02)
    for i in range(9):                                    # kiris altinda kilim sarkitlari (dikey cizgili renkli seritler)
        x = -W_ / 2 + 0.4 + i * (W_ - 0.8) / 8
        L = rnd.uniform(0.35, 0.6)
        kutu("kilim", (x, Y - 0.12, H_ + 0.02 - L / 2), (0.32, 0.03, L), mat_m(CADIR[i % len(CADIR)], 0.5, 0.3), egim=0)
        kutu("kilim_s", (x, Y - 0.14, H_ + 0.02 - L / 2), (0.08, 0.03, L), mat_m("#ffd84a", 0.4, 0.4), egim=0)
    for i in range(16):                                   # fener dizisi (motor ampul_p1 ile ayni hat)
        x = -W_ / 2 - K + i * (W_ + 2 * K) / 15
        kure((x, Y - 0.55, H_ + K * 0.4 + (i % 2) * 0.2), 0.09, mat_isik(AMPUL[i % len(AMPUL)], 6.0), sub=1)
    yuvarlak_kutu("tabela", (0, Y, H_ + K + 0.75), (W_ * 0.6, 0.2, 0.7), mat_pbr("tabela", "#2a160a", 0.35, metal=0.3), egim=0.05, seg=3)
    me = bpy.data.meshes.new("led_yuz"); a, b = W_ * 0.28, 0.28; z0 = H_ + K + 0.75
    me.from_pydata([(-a, Y - 0.11, z0 - b), (a, Y - 0.11, z0 - b), (a, Y - 0.11, z0 + b), (-a, Y - 0.11, z0 + b)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("led_yuz", me); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat_emis("led_yuz", lin(hex3("#3a1a0a")), 1.2))
    kutu("tabela_ust", (0, Y, H_ + K + 1.12), (W_ * 0.62, 0.26, 0.1), mat_m("#ffc81a", 0.25, 0.7, metal=0.6), egim=0.05, seg=2)


def serit_katmani():
    sc = koy_sahnesi(1920, 1080, True)
    kam = kamera(sc)
    rnd = random.Random(41)
    isiklar()
    mekan(True, random.Random(41))
    serit_esyalari(rnd)
    kapi()
    Y, W_, H_ = KAP["y"], KAP["w"], KAP["h"]
    ic = W_ / 2
    bpy.context.view_layer.update()
    px = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-ic, Y, 0), (ic, Y, 0), (-ic, Y, H_), (ic, Y, H_))]
    xs = [p.x * 1920 for p in px]; ys = [(1 - p.y) * 1080 for p in px]
    YERLESIM[ON_EK + "aciklik_p1"] = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
    YERLESIM[ON_EK + "ampul_p1"] = []
    for i in range(23):
        q = world_to_camera_view(sc, kam, Vector((-ic + i * 2 * ic / 22, Y - 0.42, H_ + 0.05)))
        YERLESIM[ON_EK + "ampul_p1"].append([round(q.x * 1920, 1), round((1 - q.y) * 1080, 1)])
    mk = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-5.8, 5.0, 1.0), (5.8, 5.0, 1.0), (0, GECIS, 0))]
    YERLESIM["dag"] = {"yigin_sol_x": round(mk[0].x * 1920, 1), "yigin_sag_x": round(mk[1].x * 1920, 1),
                       "yigin_y": round((1 - mk[0].y) * 1080, 1), "gecis_y": round((1 - mk[2].y) * 1080, 1)}
    YERLESIM["yol"] = {"y_kapi": Y, "genislik": PIST * 2, "kam": KAM, "serit_w": 1920}
    log("aciklik", YERLESIM[ON_EK + "aciklik_p1"], YERLESIM["dag"])
    yaz(sc, ON_EK + "serit.png")


def gok_katmani(ad):
    sc = koy_sahnesi(1920, 1080, False)
    kamera(sc)
    isiklar()
    mekan(False, random.Random(41))
    yaz(sc, ad)


if KAPAK:
    gok_katmani("kapak-gok.png")
    serit_katmani()
if YALNIZ in ("hepsi", "poz"):
    poz_maskeleri()
if YALNIZ in ("hepsi", "sahne"):
    gok_katmani("gok.png")
    serit_katmani()
json.dump(YERLESIM, open(os.path.join(CIKTI, "yerlesim.json"), "w"), indent=1)
log("bitti (col)", YERLESIM.get(ON_EK + "aciklik_p1"))
