"""HUMAN TETRIS 39. video (REF-091 yapi, 1P SOLO) - GUNDUZ MERCAN RESIFI, CILALI 3D OYUN GORUNUMU, TEK serit.
varlik.py calistirir (--mod mercan). Iskelet varlik-kurabiye.py (38, tek serit) - katmanlar, kamera, yerlesim anahtarlari ayni
(tek serit motoru 33/35'in bekledigi aciklik_p1 / ampul_p1 / dag / yol).

Mekan kullanici karari (26 Kas 2026, A): gunduz, sig turkuaz su, iki yanda renkli mercan kumeleri (sert mercan, deniz yelpazesi,
tup sunger, beyin mercani), balik suruleri, yukselen kabarciklar, yukaridan gunes huzmeleri + su yuzeyi dalgasi; pist acik kum yol +
deniz kabugu kenari + parlak yon oklari; kapi mercan kemer + deniz yildizlari + inci ampul dizisi + tabela.
OUT ani: duvar karakteri pistin yanindaki DENIZ ANEMONUNA iter, karakter anemonda seker (kabarcik pufu motorda).
Telif (md. 16): genel resif ogeleri; bilinen animasyon karakterlerine benzeyen balik (turuncu-beyaz serit palyaco) YOK.
prompts.chat (md. 23): "Underwater Kelp Forest" -> egik gunes huzmesi, balik surusu, turkuaz su (foto-gercekcilik alinmaz).
§4 CILALI 3D OYUN GORUNUMU: doygun renk, tombul hatlar, parlak kaplama (coat), gercek isik-golge (Cycles); foto dokusu yok.
§8 SOLUK YASAK: su beyaz-gri degil doygun turkuaz/camgobegi; kum soluk bej degil sicak altin; mercanlar tam doygun.
Ekran dolu (Masaustu md. 7): ust bolge su yuzeyi dalgasi + gunes huzmeleri + balik suruleri + kabarcik; zemin ufka kadar mercan.
Su derinligi: mist gecisiyle uzak nesneler turkuaz suya karisir (hacim isigi yok -> render suresi kurabiye kadar).
"""

import random
YERLESIM.clear()
KAPAK = YALNIZ == "kapak"
POZLAMA = float(arg("--pozlama", arg("--kapak-pozlama", "0")))
GUNES = float(arg("--gunes", "2.6"))
ON_EK = "kapak-" if KAPAK else ""
KDOY = KAPAK and arg("--kapak-doygun", "0") != "0"        # HT38 dersi: kapakta fog glow + beyazimsi sis renkliligi dusuruyor
KAP = {"y": 8.6, "w": 7.4, "h": 3.7, "kalin": 0.55}       # tek serit motoru ile ayni olcu
KAM = {"z": 2.3, "egim": 5.0, "lens": 18.0, "sensor": 24.0}
if KAPAK:
    KAM.update({"z": float(arg("--kapak-z", "2.0")), "egim": float(arg("--kapak-egim", "3.0")), "lens": float(arg("--kapak-lens", "16.0"))})
PIST = 3.9
GECIS = 11.5
KUM, KUM_K = "#ffbc3a", "#f08a1a"                         # sicak altin kum (soluk bej degil)
KDOY2 = KAPAK and arg("--kapak-doygun", "0") in ("2", "3", "4", "5")
KDOY5 = KAPAK and arg("--kapak-doygun", "0") == "5"      # kapak 6: gece neon resif (REF-091 lacivert zemin + neon; 26 Kas kullanici secimi)
KDOY4 = KAPAK and arg("--kapak-doygun", "0") in ("4", "5")      # kapak 5: derin su + parlayan mercan (REF-091 koyu zemin + neon)
KDOY3 = KAPAK and arg("--kapak-doygun", "0") in ("3", "4", "5")      # kapak 3: beyaz parlama / inci / kabarcik / huzme doygunlugu dusuruyor
if KDOY:                                                  # kapak 1: acik sari kum kadrajin yarisi -> doygunluk 0,54 (REF 0,72)
    KUM, KUM_K = ("#ff5a00", "#c82a00") if KDOY2 else ("#ff8a00", "#e04a00")
    if KDOY2:
        GUNES = GUNES * (0.3 if KDOY5 else 0.5 if KDOY4 else 0.75)                                # kapak 2: parlak yuzeyler beyaza patliyordu (S dusuk)
SU_UFUK, SU_ORTA, SU_UST = ("#1a3aff", "#2a0ae0", "#4a00b0") if KDOY5 else ("#0a6aff", "#1a2ae0", "#3a0aa0") if KDOY4 else ("#00a8ff", "#0060ff", "#3a1ae0") if KDOY2 else ("#00d8e0", "#00a8f0", "#0a5ae8")  # ufuk camgobegi -> mavi -> derin
SU_SIS = "#08c0dc"                                        # mist rengi (uzak nesneler bu suya karisir)
MERCAN = ("#ff2a7a", "#ff6a10", "#9a3aff", "#ffd21a", "#ff3ac8", "#20d070", "#ff4a3a", "#3a8cff")
BALIK = ("#ffd21a", "#1e8cff", "#ff3a9a", "#8a3aff", "#20e0a0", "#ff6a10")
INCI = ("#ff3ac8", "#ffd21a", "#3ad8ff", "#ff8a1a", "#9a5aff") if KDOY3 else ("#fff4e8", "#ffe0f0", "#e8f0ff", "#fff0c8", "#f0e0ff")


# ------------------------------------------------------------------ sahne / isik
def koy_sahnesi(w, h, saydam):
    sc = bos_sahne(w=w, h=h, saydam=saydam, ornek=ORNEK, doygun=True)
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.exposure = POZLAMA
    sc.cycles.max_bounces = 6; sc.cycles.diffuse_bounces = 3; sc.cycles.glossy_bounces = 3
    sc.cycles.transmission_bounces = 2; sc.cycles.transparent_max_bounces = 8
    sc.cycles.use_light_tree = True
    nt = sc.world.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord"); sp = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Generated"], sp.inputs[0])
    rp = nt.nodes.new("ShaderNodeValToRGB"); el = rp.color_ramp.elements
    el[0].position = 0.0; el[0].color = (*lin(hex3(SU_UFUK)), 1)
    el[1].position = 0.5; el[1].color = (*lin(hex3(SU_UST)), 1)
    e2 = el.new(0.16); e2.color = (*lin(hex3(SU_ORTA)), 1)
    nt.links.new(sp.outputs["Z"], rp.inputs[0])
    # su yuzeyi (ust bant): dalgali parlak cizgiler -> gokte bos alan yok
    wv = nt.nodes.new("ShaderNodeTexWave"); wv.wave_type = "BANDS"; wv.bands_direction = "X"; wv.inputs["Scale"].default_value = 7.0
    wv.inputs["Distortion"].default_value = 6.0; wv.inputs["Detail"].default_value = 2.0; wv.inputs["Detail Scale"].default_value = 1.0   # sahne 1: mermer gibi kalabalik okundu
    nt.links.new(tc.outputs["Generated"], wv.inputs["Vector"])
    bt = nt.nodes.new("ShaderNodeValToRGB"); be = bt.color_ramp.elements
    be[0].position = 0.8; be[0].color = (0, 0, 0, 1); be[1].position = 0.97; be[1].color = (1, 1, 1, 1)   # yalniz ince parlak cizgiler
    nt.links.new(wv.outputs["Fac"], bt.inputs[0])
    zb = nt.nodes.new("ShaderNodeValToRGB"); ze = zb.color_ramp.elements
    ze[0].position = 0.3; ze[0].color = (0, 0, 0, 1); ze[1].position = 0.6; ze[1].color = (0.6, 0.6, 0.6, 1)   # su yuzeyi yalniz ust bantta
    nt.links.new(sp.outputs["Z"], zb.inputs[0])
    ml = nt.nodes.new("ShaderNodeMath"); ml.operation = "MULTIPLY"
    nt.links.new(bt.outputs[0], ml.inputs[0]); nt.links.new(zb.outputs[0], ml.inputs[1])
    am = nt.nodes.new("ShaderNodeMix"); am.data_type = "RGBA"; am.blend_type = "ADD"
    nt.links.new(ml.outputs[0], am.inputs["Factor"]); nt.links.new(rp.outputs[0], am.inputs[6])
    am.inputs[7].default_value = (*lin(hex3("#ff3ae8" if KDOY5 else "#40e8ff" if KDOY else "#a0fff8")), 1)
    lp = nt.nodes.new("ShaderNodeLightPath")
    bg_k = nt.nodes.new("ShaderNodeBackground"); bg_k.inputs[1].default_value = 1.0
    nt.links.new(am.outputs[2], bg_k.inputs[0])
    bg_i = nt.nodes.new("ShaderNodeBackground"); bg_i.inputs[1].default_value = 0.55
    bg_i.inputs[0].default_value = (*lin(hex3("#5a1aff" if KDOY5 else "#2a3aff" if KDOY4 else "#1a6aff" if KDOY2 else "#30c8ff")), 1)     # su ortam isigi: camgobegi (gri golge yok)
    mx = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(lp.outputs["Is Camera Ray"], mx.inputs[0])
    nt.links.new(bg_i.outputs[0], mx.inputs[1]); nt.links.new(bg_k.outputs[0], mx.inputs[2])
    o = nt.nodes.new("ShaderNodeOutputWorld"); nt.links.new(mx.outputs[0], o.inputs[0])
    # su derinligi: mist gecisi (40 m'den sonra baslar) -> uzak resif turkuaz suya karisir
    sc.view_layers[0].use_pass_mist = True
    sc.world.mist_settings.start = 40.0; sc.world.mist_settings.depth = 360.0; sc.world.mist_settings.falloff = "QUADRATIC"
    sc.use_nodes = True; sc.render.use_compositing = True; ct = sc.node_tree; ct.nodes.clear()
    rl = ct.nodes.new("CompositorNodeRLayers"); co = ct.nodes.new("CompositorNodeComposite")
    mk = ct.nodes.new("CompositorNodeMath"); mk.operation = "MULTIPLY"; mk.inputs[1].default_value = 0.3 if KDOY else 0.7
    ct.links.new(rl.outputs["Mist"], mk.inputs[0])
    mm = ct.nodes.new("CompositorNodeMixRGB"); mm.blend_type = "MIX"
    ct.links.new(mk.outputs[0], mm.inputs[0]); ct.links.new(rl.outputs["Image"], mm.inputs[1])
    mm.inputs[2].default_value = (*lin(hex3("#2a1ae8" if KDOY5 else "#0090e0" if KDOY else SU_SIS)), 1)
    gl = ct.nodes.new("CompositorNodeGlare"); gl.glare_type = "FOG_GLOW"; gl.quality = "HIGH"; gl.threshold = 1.0; gl.size = 7; gl.mix = -0.4
    if KDOY:
        ct.links.new(mm.outputs[0], co.inputs[0])
    else:
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
    if KAPAK and arg("--kapak-dof", "0") != "0":            # mobil kapak (md. 30): kapi net, arka resif yumusak bulanik
        kam.data.dof.use_dof = True; kam.data.dof.focus_distance = KAP["y"]; kam.data.dof.aperture_fstop = float(arg("--kapak-dof", "1.2"))
    return kam


def isiklar():
    # yukaridan sicak gunes (su yuzeyinden suzulen, hafif onden) + camgobegi yan dolgu -> mercan golgeli, gri degil
    bpy.ops.object.light_add(type="SUN", location=(0, 0, 30))
    g = bpy.context.active_object; g.data.energy = GUNES; g.data.angle = math.radians(4.0)
    g.data.color = lin(hex3("#b07aff" if KDOY5 else "#fff4d8"))
    g.rotation_euler = Vector((0.2, 0.45, -0.85)).to_track_quat("-Z", "Y").to_euler()
    bpy.ops.object.light_add(type="SUN", location=(0, 0, 30))
    f = bpy.context.active_object; f.data.energy = 1.1; f.data.angle = math.radians(10.0)
    f.data.color = lin(hex3("#60e0ff"))
    f.rotation_euler = Vector((-0.3, -0.8, -0.5)).to_track_quat("-Z", "Y").to_euler()


# ------------------------------------------------------------------ malzemeler
_SM = {}


def mat_pbr(ad, renk, purluk, metal=0.0, kaplama=0.0, bump=None, ss=0.0):
    m = bpy.data.materials.new(ad); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    if KDOY3:
        kaplama *= 0.2; purluk = max(purluk, 0.55)
    b.inputs["Base Color"].default_value = (*lin(hex3(renk)), 1)
    b.inputs["Roughness"].default_value = purluk; b.inputs["Metallic"].default_value = metal
    b.inputs["Coat Weight"].default_value = kaplama; b.inputs["Coat Roughness"].default_value = 0.06
    if ss > 0:
        b.inputs["Subsurface Weight"].default_value = ss; b.inputs["Subsurface Radius"].default_value = (1.0, 0.5, 0.3)
    if bump:
        nt = m.node_tree
        ns = nt.nodes.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value = bump[0]; ns.inputs["Detail"].default_value = 6
        bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = bump[1]; bp.inputs["Distance"].default_value = 0.02
        nt.links.new(ns.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    return m


def mat_m(renk, purluk=0.35, kaplama=0.5, ss=0.0):
    key = ("m", renk, purluk, kaplama, ss)
    if key not in _SM:
        _SM[key] = mat_pbr("m" + renk, renk, purluk, kaplama=kaplama, ss=ss)
    return _SM[key]


def mat_mercan(renk):
    """mercan: doygun renk + gozenekli kabartma (voronoi) + hafif kaplama"""
    key = ("mc", renk)
    if key in _SM:
        return _SM[key]
    m = mat_pbr("mercan" + renk, renk, 0.45, kaplama=0.35, ss=0.15)
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    vr = nt.nodes.new("ShaderNodeTexVoronoi"); vr.inputs["Scale"].default_value = 14.0
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.5
    nt.links.new(vr.outputs["Distance"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    if KDOY4:
        b.inputs["Emission Color"].default_value = (*lin(hex3(renk)), 1); b.inputs["Emission Strength"].default_value = 1.6 if KDOY5 else 0.6
    _SM[key] = m
    return m


def mat_isik(renk, guc=4.0):
    key = ("i", renk, guc)
    if key not in _SM:
        _SM[key] = mat_emis("isik" + renk, lin(hex3(renk)), guc)
    return _SM[key]


def mat_kum(ad="kum", acik_ton=False):
    """kum: iki altin ton noise + dalgacik kabartmasi (su altindaki kum sirtlari)"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    ns = nt.nodes.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value = 0.8; ns.inputs["Detail"].default_value = 4
    nt.links.new(geo.outputs["Position"], ns.inputs["Vector"])
    rp = nt.nodes.new("ShaderNodeValToRGB"); el = rp.color_ramp.elements
    el[0].position = 0.3; el[0].color = (*lin(hex3((("#ff6a00" if KDOY2 else "#ff9a00") if KDOY else "#ffcc4a") if acik_ton else KUM_K)), 1)
    el[1].position = 0.75; el[1].color = (*lin(hex3((("#ff9a00" if KDOY2 else "#ffc020") if KDOY else "#ffe07a") if acik_ton else KUM)), 1)
    nt.links.new(ns.outputs["Fac"], rp.inputs[0]); nt.links.new(rp.outputs[0], b.inputs["Base Color"])
    wv = nt.nodes.new("ShaderNodeTexWave"); wv.wave_type = "BANDS"; wv.bands_direction = "Y"; wv.inputs["Scale"].default_value = 1.2
    wv.inputs["Distortion"].default_value = 4.0
    nt.links.new(geo.outputs["Position"], wv.inputs["Vector"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.3
    nt.links.new(wv.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = 0.6
    b.inputs["Coat Weight"].default_value = 0.0   # sahne 1: pistte beyaz parlama lekesi; b.inputs["Coat Roughness"].default_value = 0.1
    return m


def mat_huzme(ad="huzme"):
    """gunes huzmesi: yari saydam isik seridi (ustte parlak, altta sonuk)"""
    if ad in _SM:
        return _SM[ad]
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord"); sp = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["UV"], sp.inputs[0])
    rp = nt.nodes.new("ShaderNodeValToRGB"); el = rp.color_ramp.elements
    el[0].position = 0.0; el[0].color = (0, 0, 0, 1); el[1].position = 1.0; el[1].color = (1, 1, 1, 1)
    nt.links.new(sp.outputs["Y"], rp.inputs[0])
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs[0].default_value = (*lin(hex3("#e0fff8")), 1); em.inputs[1].default_value = 2.2
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mx = nt.nodes.new("ShaderNodeMixShader")
    mt = nt.nodes.new("ShaderNodeMath"); mt.operation = "MULTIPLY"; mt.inputs[1].default_value = 0.45   # sahne 1: huzme gorunmuyordu
    nt.links.new(rp.outputs[0], mt.inputs[0]); nt.links.new(mt.outputs[0], mx.inputs[0])
    nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(mx.outputs[0], o.inputs[0])
    _SM[ad] = m
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


def egik_boru(a, b, r, mat, r2=None):
    """a'dan b'ye egik silindir/koni (mercan dali, yosun)"""
    a, b = Vector(a), Vector(b); d = b - a
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d.length, location=(a + b) / 2, vertices=14)
    else:
        bpy.ops.mesh.primitive_cone_add(radius1=r, radius2=r2, depth=d.length, location=(a + b) / 2, vertices=14)
    o = bpy.context.active_object; o.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
    o.data.materials.append(mat); bpy.ops.object.shade_smooth()
    return o


# ------------------------------------------------------------------ ogeler
def dal_mercan(x, y, s, rnd, renk=None):
    """dallanan sert mercan: govdeden 5-8 egik dal, uclarda tombul topuz"""
    m = mat_mercan(renk or rnd.choice(MERCAN))
    taban = Vector((x, y, 0))
    for _ in range(rnd.randint(5, 8)):
        a = rnd.uniform(0, 6.28); e = rnd.uniform(0.45, 1.25); L = s * rnd.uniform(0.7, 1.3)
        uc = taban + Vector((math.cos(a) * math.cos(e) * L, math.sin(a) * math.cos(e) * L * 0.6, math.sin(e) * L))
        egik_boru(taban, uc, 0.09 * s, m, r2=0.06 * s)
        kure(uc, 0.12 * s, m, sub=2)
        if rnd.random() < 0.6:                            # ikinci kat dal
            u2 = uc + Vector((rnd.uniform(-0.3, 0.3) * L, 0, 0.35 * L))
            egik_boru(uc, u2, 0.06 * s, m, r2=0.04 * s); kure(u2, 0.09 * s, m, sub=2)


def beyin_mercan(x, y, s, rnd):
    """beyin mercani: basik tombul kure, kivrimli dalga kabartmasi"""
    renk = rnd.choice(("#ffd21a", "#20d070", "#ff6a10", "#ff3ac8", "#9a3aff"))
    key = ("bm", renk)
    if key not in _SM:
        m = mat_pbr("beyin" + renk, renk, 0.4, kaplama=0.4, ss=0.1); nt = m.node_tree; b = nt.nodes["Principled BSDF"]
        wv = nt.nodes.new("ShaderNodeTexWave"); wv.inputs["Scale"].default_value = 6.0; wv.inputs["Distortion"].default_value = 12.0
        bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.8
        nt.links.new(wv.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
        _SM[key] = m
    k = kure((x, y, s * 0.25), s * 0.7, _SM[key]); k.scale = (1.1, 1.0, 0.7)


def yelpaze(x, y, s, rnd):
    """deniz yelpazesi: ince dik disk (kameraya donuk), kenarda koyu cerceve"""
    renk = rnd.choice(("#9a3aff", "#ff2a7a", "#ffd21a", "#ff4a3a"))
    bpy.ops.mesh.primitive_cylinder_add(radius=s, depth=0.06 * s, location=(x, y, s * 0.95), rotation=(math.radians(90), 0, rnd.uniform(-0.4, 0.4)), vertices=32)
    o = bpy.context.active_object; o.scale = (1.0, 1.2, 1.0); o.data.materials.append(mat_mercan(renk)); bpy.ops.object.shade_smooth()
    silindir((x, y, 0), 0.06 * s, s * 0.3, mat_mercan(renk), v=10)


def tup_sunger(x, y, s, rnd):
    """tup sunger: 3-5 kalin dik boru, ucu acik koyu agiz"""
    renk = rnd.choice(("#ff6a10", "#9a3aff", "#ff2a7a", "#3a8cff", "#ffd21a"))
    for i in range(rnd.randint(3, 5)):
        dx, dy = rnd.uniform(-0.4, 0.4) * s, rnd.uniform(-0.3, 0.3) * s
        h = s * rnd.uniform(0.9, 1.8)
        silindir((x + dx, y + dy, 0), 0.22 * s, h, mat_mercan(renk), v=20)
        silindir((x + dx, y + dy, h - 0.02), 0.15 * s, 0.03, mat_m("#3a0a2a", 0.6, 0.0), v=20)


def yosun(x, y, H, rnd):
    """deniz yosunu: 3-4 ince yesil serit, hafif egik"""
    m = mat_m(rnd.choice(("#20c850", "#10b870", "#60d020")), 0.4, 0.3)
    for _ in range(rnd.randint(3, 4)):
        dx = rnd.uniform(-0.25, 0.25)
        egik_boru((x + dx, y, 0), (x + dx + rnd.uniform(-0.5, 0.5), y, H * rnd.uniform(0.7, 1.1)), 0.06, m, r2=0.02)


def deniz_yildizi(x, y, z, s, renk, ry=0.0):
    """bes kollu deniz yildizi: ortada tombul gobek, 5 sivri kol"""
    m = mat_m(renk, 0.35, 0.6, 0.15)
    for i in range(5):
        a = i * 1.2566 + ry
        egik_boru((x, y, z), (x + math.cos(a) * s, y, z + math.sin(a) * s), 0.16 * s, m, r2=0.05 * s)
    kure((x, y, z), 0.22 * s, m, sub=2)


def kabuk(x, y, z, s, rnd):
    """deniz kabugu (tarak): basik yarim kure, isinsal kabartma"""
    m = mat_m(rnd.choice(("#ffb0c8", "#ffd28a", "#ff8a6a", "#fff0e0")), 0.3, 0.7)
    k = kure((x, y, z), s, m, sub=2); k.scale = (1.0, 0.8, 0.45)


def balik(x, y, z, s, renk, yon=1):
    """tombul oyuncak balik: govde elipsoid + kuyruk konisi + iri goz; renk bloklu, cizgisiz (telif: palyaco deseni yok)"""
    m = mat_m(renk, 0.3, 0.7)
    g = kure((x, y, z), s, m, sub=2); g.scale = (1.4, 0.6, 1.0)
    egik_boru((x - yon * s * 1.2, y, z), (x - yon * s * 2.0, y, z), s * 0.05, m, r2=s * 0.6)
    kure((x + yon * s * 0.8, y - s * 0.4, z + s * 0.25), s * 0.22, mat_m("#ffffff", 0.2, 0.8), sub=1)
    kure((x + yon * s * 0.86, y - s * 0.52, z + s * 0.25), s * 0.11, mat_m("#101018", 0.2, 0.8), sub=1)


def balik_surusu(rnd, n, merkez, yaricap, s, renk):
    cx, cy, cz = merkez; yon = rnd.choice((-1, 1))
    for _ in range(n):
        balik(cx + rnd.uniform(-1, 1) * yaricap, cy + rnd.uniform(-0.5, 0.5) * yaricap, cz + rnd.uniform(-0.4, 0.4) * yaricap,
              s * rnd.uniform(0.8, 1.2), renk, yon)


def kabarcik(rnd, n, x_gen, y0, y1, z0, z1, kac=0.0):
    km = mat_emis("kabarcik", lin(hex3("#3ae8ff" if KDOY3 else "#e8fffc")), 1.3)
    for _ in range(n):
        x = rnd.uniform(-x_gen, x_gen); y = rnd.uniform(y0, y1); z = rnd.uniform(z0, z1)
        if abs(x) < kac and y < y0 + 12:
            continue
        kure((x, y, z), rnd.uniform(0.04, 0.11) * (1 + (y - y0) / 30), km, sub=1)


def huzme(x, y, gen, uz, egim):
    """gunes huzmesi: ustten asagi uzanan yari saydam serit, hafif egik"""
    bpy.ops.mesh.primitive_plane_add(size=1, location=(x, y, 0))
    p = bpy.context.active_object; p.scale = (gen, uz, 1)
    bpy.ops.object.transform_apply(scale=True)
    p.rotation_euler = (math.radians(90), egim, 0)
    p.location.z = uz / 2 - 2
    p.data.materials.append(mat_huzme()); p.visible_shadow = False
    return p


def zemin(rnd, y0, y1, x_gen, kac=0.0):
    """kum zemin + uzaga dogru mercan tepecikleri ve kaya (ufka kadar dolu)"""
    km = mat_kum()
    me = bpy.data.meshes.new("zemin")
    me.from_pydata([(-x_gen, y0, 0), (x_gen, y0, 0), (x_gen, y1, 0), (-x_gen, y1, 0)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("zemin", me); bpy.context.collection.objects.link(o); o.data.materials.append(km)
    y = y0 + 6
    while y < y1:
        s = 1.0 + (y - y0) / 30.0
        x = -x_gen + rnd.uniform(0, 8 * s)
        while x < x_gen:
            r = rnd.uniform(2.2, 4.2) * s
            if abs(x) - r < kac:
                x += 8 * s; continue
            t = kure((x, y, -r * 0.55), r, mat_mercan(rnd.choice(MERCAN)), sub=2); t.scale = (1.5, 1.0, 0.65)
            x += 8 * s * rnd.uniform(0.8, 1.3)
        y += 9 * s
    return km


def anemon(x, y, r, rnd):
    """OUT: deniz anemonu - tombul taban + 30 yumusak dokunac (uclari top), mor-pembe; karakter buna duser, seker"""
    taban = mat_m("#c81a8a", 0.35, 0.5, 0.2)
    t = silindir((x, y, 0), r * 0.55, r * 0.35, taban, v=28, r2=r * 0.45); t.scale = (1, 1, 1)
    dk = mat_m("#ff5ad0", 0.3, 0.6, 0.3); uc = mat_m("#ffe0f8", 0.25, 0.7, 0.2)
    for i in range(30):
        a = rnd.uniform(0, 6.28); rr = rnd.uniform(0.05, 0.45) * r
        b = Vector((x + math.cos(a) * rr, y + math.sin(a) * rr, r * 0.33))
        e = b + Vector((math.cos(a) * r * 0.35, math.sin(a) * r * 0.2, r * rnd.uniform(0.55, 0.9)))
        egik_boru(b, e, 0.07 * r, dk, r2=0.05 * r)
        kure(e, 0.08 * r, uc, sub=1)


def inci_fener(x, y, H, rnd):
    """yol feneri yerine: mercan direk + ustte acik istiridye kabugu icinde parlayan inci"""
    silindir((x, y, 0), 0.08, H, mat_mercan("#ff6a10"), v=12)
    k = kure((x, y, H + 0.05), 0.32, mat_m("#ffb0c8", 0.3, 0.7)); k.scale = (1.2, 1.0, 0.35)
    kure((x, y, H + 0.2), 0.14, mat_isik("#fff6e8", 6.0), sub=2)


# ------------------------------------------------------------------ MEKAN (her iki katmanda; serit sahnesinde uzak kisim holdout)
def mekan(serit_modu, rnd):
    _SM.clear()                                         # ikinci katmanda bos_sahne eski malzemeleri siliyor (36 dersi)
    km = mat_kum("yakin_kum")
    me = bpy.data.meshes.new("yakin_zemin")
    me.from_pydata([(-60, -4, -0.02), (60, -4, -0.02), (60, GECIS, -0.02), (-60, GECIS, -0.02)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("yakin_zemin", me); bpy.context.collection.objects.link(o); o.data.materials.append(km)
    # yakin kenar: pistin iki yaninda mercan kumeleri + sunger + yosun + kabuk + inci fenerler (koridor bos; OUT anemonlarinin yeri acik)
    for s in (-1, 1):
        for (x, y, k) in ((9.5, 1.5, 1.6), (13, 6, 2.2), (8.8, 10, 1.4), (18, 9, 2.8), (11.5, 3.2, 1.2)):
            dal_mercan(s * x, y, k, rnd)
        for (x, y, k) in ((7.8, 2.6, 0.9), (12, 8.2, 1.2), (16, 3, 1.4)):
            beyin_mercan(s * x, y, k, rnd)
        for (x, y, k) in ((10.5, 7.4, 1.3), (15, 1.0, 1.6)):
            yelpaze(s * x, y, k, rnd)
        for (x, y, k) in ((8.4, 6.6, 0.8), (14, 5, 1.0)):
            tup_sunger(s * x, y, k, rnd)
        for (x, y) in ((7.4, 0.4), (9.8, 4.8), (13.5, 10.5)):
            yosun(s * x, y, rnd.uniform(1.4, 2.4), rnd)
        for (x, y) in ((6.8, 1.2), (7.2, 3.8), (6.6, 7.8)):
            kabuk(s * x, y, 0.05, 0.28, rnd)
        for y in (-1.0, 3.4, 7.6):
            inci_fener(s * (PIST + 1.4), y, 1.8, rnd)
    for o in bpy.data.objects:
        if o.type == "MESH":
            o["yakin"] = 1
    zemin(rnd, GECIS, 420, 420, kac=PIST + 2)
    # resif koridoru: iki yanda sik mercan bahcesi, kapinin arkasi ve orta koridor acik
    for s in (-1, 1):
        y = GECIS + 3
        while y < 150:
            sc = 1.4 + y / 35
            x = s * rnd.uniform(9, 14) * (1 + y / 60)
            dal_mercan(x, y, 1.6 * sc, rnd)
            beyin_mercan(x + s * 3.0 * sc, y + 1.5 * sc, 1.2 * sc, rnd)
            if rnd.random() < 0.6:
                yelpaze(x + s * 6 * sc, y + 3 * sc, 1.6 * sc, rnd)
            else:
                tup_sunger(x + s * 6 * sc, y + 3 * sc, 1.3 * sc, rnd)
            if rnd.random() < 0.5:
                yosun(x - s * 2.2 * sc, y + 1 * sc, 2.4 * sc, rnd)
            y += 5.0 * sc
    for _ in range(70):                                 # orta-uzak resif (ufuk dolu)
        x = rnd.choice((-1, 1)) * rnd.uniform(25, 260); y = rnd.uniform(60, 420)
        r = rnd.random()
        if r < 0.45:
            dal_mercan(x, y, rnd.uniform(4, 10), rnd)
        elif r < 0.75:
            beyin_mercan(x, y, rnd.uniform(4, 9), rnd)
        else:
            yelpaze(x, y, rnd.uniform(4, 9), rnd)
    for i in range(30):                                 # kapiya dogru iki yanda dizili kucuk mercan direkler
        s = -1 if i % 2 == 0 else 1; y = GECIS + 2 + (i // 2) * 4.5
        dal_mercan(s * (PIST + 2.2 + y * 0.02), y, 0.9 + y * 0.02, rnd, renk=MERCAN[(i // 2) % len(MERCAN)])
    # su ici: gunes huzmeleri, balik suruleri, kabarciklar
    for i in range(9):                                  # sahne 1: 40-140 m'de mist icinde kayboldu -> yakin (22-45 m), genis
        x = -48 + i * 12 + rnd.uniform(-3, 3)
        if abs(x) < 7 or KDOY3:
            continue
        huzme(x, rnd.uniform(22, 45), rnd.uniform(3, 6), 50, rnd.uniform(-0.35, -0.15))
    for (m, r, s, renk) in (((-18, 30, 8), 4, 0.7, BALIK[0]), ((20, 34, 9), 4.5, 0.75, BALIK[1]), ((-34, 60, 14), 7, 1.1, BALIK[2]),   # sahne 1: suruler cok kucuktu
                            ((38, 70, 16), 7, 1.2, BALIK[3]), ((-10, 110, 24), 10, 1.6, BALIK[4]), ((55, 140, 28), 12, 1.9, BALIK[5])):
        balik_surusu(rnd, 12, m, r, s, renk)
    for (x, y, z, renk) in ((-9, 16, 5.5, BALIK[1]), (10, 20, 6.5, BALIK[0]), (-14, 26, 8, BALIK[3])):   # yakin tek baliklar (gokte bos alan yok)
        balik(x, y, z, 0.5, renk, 1 if x < 0 else -1)
    kabarcik(rnd, 420, 30, 2, 60, 0.5, 18, kac=5)
    if serit_modu:
        for o in bpy.data.objects:
            if o.type == "MESH" and not o.get("yakin"):
                o.is_holdout = True


# ------------------------------------------------------------------ SERIT: kum pist + kabuk kenar + inci korkuluk + oklar + OUT anemonlari
def serit_esyalari(rnd):
    kutu("pist", (0, (KAP["y"] + 0.4 - 4) / 2, 0.0), (PIST * 2, KAP["y"] + 4.4, 0.16), mat_kum("pist", acik_ton=True), egim=0.04, seg=2)
    for s in (-1, 1):                                   # pist kenari: pembe-turuncu deniz kabugu dizisi
        y = -3.0; i = 0
        while y < KAP["y"] - 0.2:
            k = kure((s * (PIST + 0.08), y, 0.12), 0.26, mat_m(("#ff8ab0", "#ffb06a", "#ff6a9a")[i % 3], 0.3, 0.7)); k.scale = (0.8, 1.0, 0.5)
            y += 0.5; i += 1
    for s in (-1, 1):                                   # korkuluk: alcak mercan direkler + ustte inci isik + aradaki yosun halat
        y = -3.0; i = 0
        while y < KAP["y"] - 0.4:
            silindir((s * (PIST + 0.5), y, 0.0), 0.07, 0.7, mat_mercan(MERCAN[i % 4]), v=14)
            kure((s * (PIST + 0.5), y, 0.78), 0.12, mat_isik(INCI[i % 5], 5.0))
            y += 1.3; i += 1
        kutu("halat", (s * (PIST + 0.5), (KAP["y"] - 3.4) / 2, 0.55), (0.06, KAP["y"] + 2.6, 0.1), mat_m("#10b870", 0.35, 0.5), egim=0)
    for j, x in enumerate((-1.7, 1.7)):                 # yon oklari: mercan pembesi ve sari
        ok = mat_m("#ff2a7a" if j == 0 else "#7a2aff", 0.25, 0.8)   # sahne 1: sari ok sari kumda kayboldu -> mor
        for y in (4.6, 6.2):
            nok = [(x - 0.6, y - 0.4), (x, y), (x + 0.6, y - 0.4), (x + 0.6, y - 0.68), (x, y - 0.28), (x - 0.6, y - 0.68)]
            me = bpy.data.meshes.new("ok"); me.from_pydata([(a, b, 0.17) for a, b in nok], [], [list(range(6))]); me.update()
            o = bpy.data.objects.new("ok", me); bpy.context.collection.objects.link(o); o.data.materials.append(ok)
            o.modifiers.new("k", "SOLIDIFY").thickness = 0.02
    for s in (-1, 1):                                   # OUT ani: iki dis tarafta deniz anemonu
        anemon(s * 5.6, 5.0, 1.5, random.Random(39 + s))


def kapi():
    """mercan kemer: iki kalin dallanan mercan kule, ustte mercan kiris + deniz yildizlari + inci ampul dizisi; LED tabela"""
    Y, W_, H_, K = KAP["y"], KAP["w"], KAP["h"], KAP["kalin"]
    xk = W_ / 2 + K / 2
    rnd = random.Random(391)
    for s, renk in ((-1, "#ff2a7a"), (1, "#9a3aff")):
        m = mat_mercan(renk)
        silindir((s * xk, Y, 0), K * 0.55, H_ + K + 0.2, m, v=32)
        for i in range(9):                              # kule yuzeyinde mercan topuzlari
            z = 0.3 + i * (H_ + K) / 9
            kure((s * xk + rnd.uniform(-0.2, 0.2), Y - K * 0.45, z), K * rnd.uniform(0.22, 0.32), m, sub=2)
        kure((s * xk, Y, H_ + K + 0.35), K * 0.6, mat_isik("#fff6e8", 6.0))
    yuvarlak_kutu("kiris", (0, Y, H_ + K / 2), (W_ + 2 * K, K + 0.1, K), mat_mercan("#ff6a10"), egim=0.2, seg=5)
    for i in range(24):                                 # kiris onunde renkli mercan topuzlari
        x = -W_ / 2 - K + i * (W_ + 2 * K) / 23
        k = kure((x, Y - 0.3, H_ + K * 0.5 + rnd.uniform(-0.15, 0.15)), 0.26, mat_mercan(MERCAN[i % len(MERCAN)]), sub=2); k.scale = (1.1, 0.7, 0.9)
    for i in range(16):                                 # inci ampul dizisi (motor ampul_p1 ile ayni hat)
        x = -W_ / 2 - K + i * (W_ + 2 * K) / 15
        kure((x, Y - 0.55, H_ + K * 0.4 + (i % 2) * 0.2), 0.09, mat_isik(INCI[i % 5], 6.0), sub=1)
    for x, renk in ((-W_ / 2, "#ffd21a"), (0, "#ff4a3a"), (W_ / 2, "#ff8a1a")):   # deniz yildizlari
        deniz_yildizi(x, Y - 0.62, H_ + K * 0.55, 0.34, renk, ry=0.3)
    yuvarlak_kutu("tabela", (0, Y, H_ + K + 0.75), (W_ * 0.6, 0.2, 0.7), mat_pbr("tabela", "#15171a", 0.35, metal=0.4), egim=0.05, seg=3)
    me = bpy.data.meshes.new("led_yuz"); a, b = W_ * 0.28, 0.28; z0 = H_ + K + 0.75
    me.from_pydata([(-a, Y - 0.11, z0 - b), (a, Y - 0.11, z0 - b), (a, Y - 0.11, z0 + b), (-a, Y - 0.11, z0 + b)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("led_yuz", me); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat_emis("led_yuz", lin(hex3("#0a3a5a")), 1.2))
    for x in (-W_ * 0.32, W_ * 0.32):                   # tabela kenarinda kabuk
        k = kure((x, Y - 0.12, H_ + K + 1.15), 0.3, mat_m("#ffb0c8", 0.3, 0.7)); k.scale = (1.2, 0.5, 0.9)


def serit_katmani():
    sc = koy_sahnesi(1920, 1080, True)
    kam = kamera(sc)
    rnd = random.Random(39)
    isiklar()
    mekan(True, random.Random(39))
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
    mk = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-5.6, 5.0, 1.0), (5.6, 5.0, 1.0), (0, GECIS, 0))]
    YERLESIM["dag"] = {"yigin_sol_x": round(mk[0].x * 1920, 1), "yigin_sag_x": round(mk[1].x * 1920, 1),
                       "yigin_y": round((1 - mk[0].y) * 1080, 1), "gecis_y": round((1 - mk[2].y) * 1080, 1)}
    YERLESIM["yol"] = {"y_kapi": Y, "genislik": PIST * 2, "kam": KAM, "serit_w": 1920}
    log("aciklik", YERLESIM[ON_EK + "aciklik_p1"], YERLESIM["dag"])
    yaz(sc, ON_EK + "serit.png")


def gok_katmani(ad):
    sc = koy_sahnesi(1920, 1080, False)
    kamera(sc)
    isiklar()
    mekan(False, random.Random(39))
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
log("bitti (mercan)", YERLESIM.get(ON_EK + "aciklik_p1"))
