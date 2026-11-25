"""HUMAN TETRIS 38. video (REF-090 yapi, 1P SOLO Christmas) - ALACAKARANLIKTA KURABIYE KOYU KOPRUSU, CILALI 3D OYUN GORUNUMU, TEK serit.
varlik.py calistirir (--mod kurabiye). Iskelet varlik-mantar.py (36, tek serit) - katmanlar, kamera, yerlesim anahtarlari ayni
(tek serit motoru 33'un bekledigi aciklik_p1 / ampul_p1 / dag / yol).

Mekan kullanici karari (24 Kas 2026, A): alacakaranlik, zencefilli kurabiye evleri (krema sacak, seker pencere, isikli), seker kamisi
korkuluk + kurdele + fener, isikli susli camlar, aurora + dolunay + yildiz, kar yagisi. OUT ani: karakter pistin yanindaki krema kapli
kar yiginina gomulur (kar pufu + seker serpintisi). REF-090 temasi; mekan kurgusu bizim (32 Noel atolyesi tekrar edilmez).
Telif (md. 16): genel Christmas ogeleri; marka/karakter yok.
§4 CILALI 3D OYUN GORUNUMU: doygun renk, tombul hatlar, parlak kaplama (coat), gercek isik-golge (Cycles); foto dokusu yok.
§8 SOLUK YASAK: kar beyaz degil, alacakaranlik leylak-mavisi; buyuk alanlar doygun (kurabiye kahve-turuncu, cam yesili, gok mor-lacivert).
Ekran dolu (Masaustu md. 7): gokte aurora seritleri, dolunay, yildiz, kar taneleri; zemin ufka kadar ev + cam + tepe isiklari.
"""

import random
YERLESIM.clear()
KAPAK = YALNIZ == "kapak"
POZLAMA = float(arg("--pozlama", arg("--kapak-pozlama", "0")))
AY_GUC = float(arg("--ay", "1.6"))
ON_EK = "kapak-" if KAPAK else ""
KAP = {"y": 8.6, "w": 7.4, "h": 3.7, "kalin": 0.55}       # tek serit motoru (27/28/35/36) ile ayni olcu
KAM = {"z": 2.3, "egim": 5.0, "lens": 18.0, "sensor": 24.0}
if KAPAK:
    KAM.update({"z": float(arg("--kapak-z", "2.0")), "egim": float(arg("--kapak-egim", "3.0")), "lens": float(arg("--kapak-lens", "16.0"))})
PIST = 3.9
GECIS = 11.5
KURABIYE, KURABIYE_K = "#c8661e", "#8a3a10"               # zencefilli kurabiye
KREMA = "#ffd0e8"                                         # krema (kucuk alanlar; buyuk alan degil)
KAR, KAR_K = "#8a96ff", "#6a4aff"                         # alacakaranlik kari: doygun leylak-mavi (sahne 1: #c4ccff soluk, doygunluk 0,47)
CAM, CAM_K = "#14b83a", "#0a7a28"
SEKER = ("#ff2a4a", "#20c850", "#ffc21a", "#1e8cff", "#ff3aa8", "#8a3aff", "#ff7a10", "#10c8d0")
ISIK = ("#ff3030", "#30ff50", "#ffd21a", "#3a8cff", "#ff40c0")
GOK_ALT, GOK_ORTA, GOK_UST = "#ff3a9a", "#7a1ae8", "#1a0a8a"   # ufuk pembe -> mor -> derin lacivert
AURORA = ("#20ffa0", "#20e0ff", "#ff50d0")


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
    el[0].position = 0.0; el[0].color = (*lin(hex3(GOK_ALT)), 1)
    el[1].position = 0.45; el[1].color = (*lin(hex3(GOK_UST)), 1)
    e2 = el.new(0.12); e2.color = (*lin(hex3(GOK_ORTA)), 1)
    nt.links.new(sp.outputs["Z"], rp.inputs[0])
    lp = nt.nodes.new("ShaderNodeLightPath")
    bg_k = nt.nodes.new("ShaderNodeBackground"); bg_k.inputs[1].default_value = 1.0
    bg_i = nt.nodes.new("ShaderNodeBackground"); bg_i.inputs[1].default_value = 0.5
    bg_i.inputs[0].default_value = (*lin(hex3("#a080ff")), 1)      # alacakaranlik ortam isigi: mor-mavi (gri golge yok)
    # aurora (sahne 1: perde duzlemleri dikdortgen blok okundu): gok rengine yumusak dalgali seritler; yalniz ufkun ustu (Z 0,06-0,4)
    gz = nt.nodes.new("ShaderNodeTexCoord")
    wv = nt.nodes.new("ShaderNodeTexWave"); wv.wave_type = "BANDS"; wv.bands_direction = "X"; wv.inputs["Scale"].default_value = 1.6
    wv.inputs["Distortion"].default_value = 9.0; wv.inputs["Detail"].default_value = 3.0; wv.inputs["Detail Scale"].default_value = 1.5
    nt.links.new(gz.outputs["Generated"], wv.inputs["Vector"])
    bt = nt.nodes.new("ShaderNodeValToRGB"); be = bt.color_ramp.elements                      # serit maskesi: ince parlak cizgiler
    be[0].position = 0.55; be[0].color = (0, 0, 0, 1); be[1].position = 0.9; be[1].color = (1, 1, 1, 1)
    nt.links.new(wv.outputs["Fac"], bt.inputs[0])
    zb = nt.nodes.new("ShaderNodeValToRGB"); ze = zb.color_ramp.elements                      # yukseklik bandi
    ze[0].position = 0.05; ze[0].color = (0, 0, 0, 1); ze[1].position = 0.42; ze[1].color = (0, 0, 0, 1)
    z1 = ze.new(0.13); z1.color = (1, 1, 1, 1); z2 = ze.new(0.26); z2.color = (0.7, 0.7, 0.7, 1)
    nt.links.new(sp.outputs["Z"], zb.inputs[0])
    ml = nt.nodes.new("ShaderNodeMath"); ml.operation = "MULTIPLY"
    nt.links.new(bt.outputs[0], ml.inputs[0]); nt.links.new(zb.outputs[0], ml.inputs[1])
    ar = nt.nodes.new("ShaderNodeValToRGB"); ae = ar.color_ramp.elements                      # renk: x boyunca yesil -> camgobegi -> pembe
    ae[0].position = 0.3; ae[0].color = (*lin(hex3(AURORA[0])), 1); ae[1].position = 0.7; ae[1].color = (*lin(hex3(AURORA[2])), 1)
    a3 = ae.new(0.5); a3.color = (*lin(hex3(AURORA[1])), 1)
    nt.links.new(sp.outputs["X"], ar.inputs[0])
    am = nt.nodes.new("ShaderNodeMix"); am.data_type = "RGBA"; am.blend_type = "ADD"
    nt.links.new(ml.outputs[0], am.inputs["Factor"]); nt.links.new(rp.outputs[0], am.inputs[6]); nt.links.new(ar.outputs[0], am.inputs[7])
    nt.links.new(am.outputs[2], bg_k.inputs[0])
    mx = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(lp.outputs["Is Camera Ray"], mx.inputs[0])
    nt.links.new(bg_i.outputs[0], mx.inputs[1]); nt.links.new(bg_k.outputs[0], mx.inputs[2])
    o = nt.nodes.new("ShaderNodeOutputWorld"); nt.links.new(mx.outputs[0], o.inputs[0])
    sc.use_nodes = True; sc.render.use_compositing = True; ct = sc.node_tree; ct.nodes.clear()
    rl = ct.nodes.new("CompositorNodeRLayers"); gl = ct.nodes.new("CompositorNodeGlare"); co = ct.nodes.new("CompositorNodeComposite")
    gl.glare_type = "FOG_GLOW"; gl.quality = "HIGH"; gl.threshold = 1.0; gl.size = 7; gl.mix = -0.3   # isik dizileri hafif parlar
    ct.links.new(rl.outputs["Image"], gl.inputs[0]); ct.links.new(gl.outputs[0], co.inputs[0])
    if saydam:
        ct.links.new(rl.outputs["Alpha"], co.inputs[1])
    return sc


def kamera(sc):
    rx = math.radians(90 - KAM["egim"])
    bpy.ops.object.camera_add(location=(0, 0, KAM["z"]), rotation=(rx, 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.sensor_fit = "VERTICAL"; kam.data.sensor_height = KAM["sensor"]; kam.data.lens = KAM["lens"]
    kam.data.clip_end = 2500
    if KAPAK and arg("--kapak-dof", "0") != "0":            # mobil kapak (md. 30): kapi/pano net, arka koy yumusak bulanik -> sade arka plan
        kam.data.dof.use_dof = True; kam.data.dof.focus_distance = KAP["y"]; kam.data.dof.aperture_fstop = float(arg("--kapak-dof", "1.2"))
    return kam


def isiklar():
    # ay isigi (soguk, arkadan) + on dolgu (sicak pembe, alacakaranlik ufku) -> kurabiye ve kar golgeli, gri degil
    bpy.ops.object.light_add(type="SUN", location=(0, 0, 30))
    g = bpy.context.active_object; g.data.energy = AY_GUC; g.data.angle = math.radians(3.0)
    g.data.color = lin(hex3("#c8d0ff"))
    g.rotation_euler = Vector((0.25, 0.7, -0.6)).to_track_quat("-Z", "Y").to_euler()
    bpy.ops.object.light_add(type="SUN", location=(0, 0, 30))
    f = bpy.context.active_object; f.data.energy = 1.4; f.data.angle = math.radians(8.0)
    f.data.color = lin(hex3("#ffb0a0"))
    f.rotation_euler = Vector((-0.2, -0.8, -0.55)).to_track_quat("-Z", "Y").to_euler()


# ------------------------------------------------------------------ malzemeler
def mat_pbr(ad, renk, purluk, metal=0.0, kaplama=0.0, bump=None, ss=0.0):
    m = bpy.data.materials.new(ad); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
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


def mat_kar(ad="kar"):
    """alacakaranlik kari: iki leylak-mavi noise karisimi + yumusak kabartma + parilti (sheen)"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    ns = nt.nodes.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value = 0.9; ns.inputs["Detail"].default_value = 4
    nt.links.new(geo.outputs["Position"], ns.inputs["Vector"])
    rp = nt.nodes.new("ShaderNodeValToRGB"); el = rp.color_ramp.elements
    el[0].position = 0.3; el[0].color = (*lin(hex3(KAR_K)), 1)
    el[1].position = 0.75; el[1].color = (*lin(hex3(KAR)), 1)
    nt.links.new(ns.outputs["Fac"], rp.inputs[0]); nt.links.new(rp.outputs[0], b.inputs["Base Color"])
    n2 = nt.nodes.new("ShaderNodeTexNoise"); n2.inputs["Scale"].default_value = 9.0; n2.inputs["Detail"].default_value = 6
    nt.links.new(geo.outputs["Position"], n2.inputs["Vector"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.35
    nt.links.new(n2.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = 0.55
    b.inputs["Sheen Weight"].default_value = 0.15; b.inputs["Sheen Tint"].default_value = (*lin(hex3("#b08aff")), 1)
    b.inputs["Subsurface Weight"].default_value = 0.2; b.inputs["Subsurface Radius"].default_value = (0.6, 0.7, 1.0)
    return m


def mat_kurabiye_tas(ad="pist"):
    """pist: kare kurabiye karolari (voronoi), kahve-turuncu ton farki + aralarda krema derz"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    vr = nt.nodes.new("ShaderNodeTexVoronoi"); vr.feature = "DISTANCE_TO_EDGE"; vr.inputs["Scale"].default_value = 1.4
    vr.distance = "CHEBYCHEV"
    nt.links.new(geo.outputs["Position"], vr.inputs["Vector"])
    v2 = nt.nodes.new("ShaderNodeTexVoronoi"); v2.inputs["Scale"].default_value = 1.4; v2.distance = "CHEBYCHEV"
    nt.links.new(geo.outputs["Position"], v2.inputs["Vector"])
    rt = nt.nodes.new("ShaderNodeValToRGB"); el = rt.color_ramp.elements
    el[0].position = 0.0; el[0].color = (*lin(hex3("#d8761e")), 1); el[1].position = 1.0; el[1].color = (*lin(hex3("#a8501a")), 1)
    nt.links.new(v2.outputs["Color"], rt.inputs[0])
    dz = nt.nodes.new("ShaderNodeMath"); dz.operation = "LESS_THAN"; dz.inputs[1].default_value = 0.03
    nt.links.new(vr.outputs["Distance"], dz.inputs[0])
    mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"; nt.links.new(dz.outputs[0], mx.inputs["Factor"])
    nt.links.new(rt.outputs[0], mx.inputs[6]); mx.inputs[7].default_value = (*lin(hex3("#ff7ab8")), 1)
    nt.links.new(mx.outputs[2], b.inputs["Base Color"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.6
    nt.links.new(vr.outputs["Distance"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = 0.45; b.inputs["Coat Weight"].default_value = 0.35; b.inputs["Coat Roughness"].default_value = 0.12
    return m


_SM = {}


def mat_cizgili(ad="seker_kamisi", renk="#ff1a3a"):
    """seker kamisi: kirmizi-krema capraz serit (wave BANDS, nesne uzayi), parlak kaplama"""
    if ad in _SM:
        return _SM[ad]
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    wv = nt.nodes.new("ShaderNodeTexWave"); wv.wave_type = "BANDS"; wv.bands_direction = "DIAGONAL"
    wv.inputs["Scale"].default_value = 2.2; wv.inputs["Distortion"].default_value = 0.0
    nt.links.new(tc.outputs["Object"], wv.inputs["Vector"])
    rp = nt.nodes.new("ShaderNodeValToRGB"); rp.color_ramp.interpolation = "CONSTANT"; el = rp.color_ramp.elements
    el[0].position = 0.0; el[0].color = (*lin(hex3(renk)), 1); el[1].position = 0.5; el[1].color = (*lin(hex3("#fff0f0")), 1)
    nt.links.new(wv.outputs["Fac"], rp.inputs[0]); nt.links.new(rp.outputs[0], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.2; b.inputs["Coat Weight"].default_value = 0.8; b.inputs["Coat Roughness"].default_value = 0.05
    _SM[ad] = m
    return m


def mat_m(renk, purluk=0.35, kaplama=0.5, ss=0.0):
    key = ("m", renk, purluk, kaplama, ss)
    if key not in _SM:
        _SM[key] = mat_pbr("m" + renk, renk, purluk, kaplama=kaplama, ss=ss)
    return _SM[key]


def mat_isik(renk, guc=4.0):
    key = ("i", renk, guc)
    if key not in _SM:
        _SM[key] = mat_emis("isik" + renk, lin(hex3(renk)), guc)
    return _SM[key]


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


def prizma(ad, x, y, z, gen, der, yuk, mat):
    """cati: ucgen prizma (sirt x ekseninde degil, cephe kameraya bakar -> sirt y ekseninde)"""
    a, d = gen / 2, der / 2
    v = [(-a, -d, 0), (a, -d, 0), (0, -d, yuk), (-a, d, 0), (a, d, 0), (0, d, yuk)]
    f = [(0, 1, 2), (3, 5, 4), (0, 3, 4, 1), (1, 4, 5, 2), (0, 2, 5, 3)]
    me = bpy.data.meshes.new(ad); me.from_pydata([(x + p[0], y + p[1], z + p[2]) for p in v], [], f); me.update()
    o = bpy.data.objects.new(ad, me); bpy.context.collection.objects.link(o); o.data.materials.append(mat)
    bv = o.modifiers.new("e", "BEVEL"); bv.width = min(gen, yuk) * 0.06; bv.segments = 3
    return o


# ------------------------------------------------------------------ ogeler
def kurabiye_ev(x, y, s, rnd, yon=1):
    """zencefilli ev: kurabiye govde, krema sacakli cati, seker cati boncuklari, isikli pencere + kapi, bacada kar"""
    w, d, h = 2.6 * s, 2.2 * s, 2.0 * s
    kutu("ev", (x, y, h / 2), (w, d, h), mat_m(KURABIYE, 0.45, 0.35, 0.1), egim=0.12 * s, seg=3)
    cati_renk = rnd.choice(("#ff2a4a", "#20c850", "#ff3aa8", "#1e8cff", KURABIYE_K))
    prizma("cati", x, y, h, w * 1.18, d * 1.15, h * 0.75, mat_m(cati_renk, 0.3, 0.6))
    kr = mat_m(KREMA, 0.3, 0.5, 0.2)
    for i in range(9):                                   # sacak kremasi: iki egik kenar boyunca damla kureler
        t = i / 8
        for sx in (-1, 1):
            kure((x + sx * (w * 0.59) * (1 - t), y - d * 0.58, h + h * 0.75 * t), 0.13 * s, kr)
    for i in range(5):                                   # cati sirti seker boncuklari
        kure((x, y - d * 0.5 + i * d * 0.25, h + h * 0.78), 0.14 * s, mat_m(rnd.choice(SEKER), 0.25, 0.8))
    pc = rnd.choice(("#ffc21a", "#ff9a2a", "#ffe04a"))
    for sx in (-1, 1):                                   # pencereler (sicak isik) + krema cerceve
        px, pz = x + sx * w * 0.27, h * 0.58
        kutu("pen", (px, y - d / 2 - 0.02, pz), (0.55 * s, 0.05, 0.55 * s), mat_isik(pc, 5.0), egim=0)
        kutu("pcer", (px, y - d / 2 - 0.05, pz), (0.66 * s, 0.03, 0.08 * s), kr, egim=0)
        kutu("pcer", (px, y - d / 2 - 0.05, pz), (0.08 * s, 0.03, 0.66 * s), kr, egim=0)
    kutu("kapi", (x, y - d / 2 - 0.03, 0.45 * s), (0.6 * s, 0.06, 0.9 * s), mat_m(rnd.choice(SEKER), 0.3, 0.6), egim=0.05 * s)
    if rnd.random() < 0.6:                               # baca + kar
        kutu("baca", (x + w * 0.25, y + d * 0.1, h + h * 0.55), (0.35 * s, 0.35 * s, 0.7 * s), mat_m(KURABIYE_K, 0.5, 0.2), egim=0.05 * s)
        k = kure((x + w * 0.25, y + d * 0.1, h + h * 0.55 + 0.38 * s), 0.25 * s, mat_m(KAR, 0.5, 0.1, 0.2)); k.scale = (1.2, 1.2, 0.5)
    for i in range(7):                                   # catı kenari isik dizisi
        t = i / 6
        kure((x - w * 0.55 + t * w * 1.1, y - d * 0.6, h + 0.05), 0.07 * s, mat_isik(ISIK[i % 5], 6.0))


def cam_agaci(x, y, z, H, rnd, isikli=True):
    """susli cam: uc kat koni (doygun yesil, parlak) + renkli isik toplari + tepede altin yildiz"""
    gm = mat_m(CAM, 0.4, 0.3)
    silindir((x, y, z), H * 0.06, H * 0.15, mat_m(KURABIYE_K, 0.6, 0.1), v=12)
    for k, (r, h0, hh) in enumerate(((0.42, 0.12, 0.45), (0.33, 0.38, 0.4), (0.23, 0.62, 0.38))):
        silindir((x, y, z + H * h0), H * r, H * hh, gm, v=24, r2=H * 0.02)
        ks = kure((x, y, z + H * h0 + 0.02 * H), H * r * 0.98, mat_m(KAR, 0.5, 0.1, 0.2), sub=2); ks.scale = (1, 1, 0.12)
    if isikli:
        for i in range(int(10 + H * 1.5)):
            t = rnd.uniform(0.15, 0.95); a = rnd.uniform(0, 6.28)
            r = H * (0.42 - 0.38 * t) * 0.95
            kure((x + math.cos(a) * r, y + math.sin(a) * r, z + H * t), max(0.05, H * 0.025), mat_isik(rnd.choice(ISIK), 6.0), sub=1)
    y_m = mat_isik("#ffd21a", 8.0)
    kure((x, y, z + H * 1.02), H * 0.06, y_m, sub=2)


def seker_kamisi(x, y, z, H, r, renk="#ff1a3a"):
    """seker kamisi direk: cizgili silindir + ustte yarim halka kanca"""
    silindir((x, y, z), r, H, mat_cizgili("sk" + renk, renk), v=20)
    bpy.ops.mesh.primitive_torus_add(major_radius=r * 2.2, minor_radius=r, location=(x + r * 2.2, y, z + H), rotation=(math.radians(90), 0, 0),
                                     major_segments=24, minor_segments=12)
    t = bpy.context.active_object; t.data.materials.append(mat_cizgili("sk" + renk, renk)); bpy.ops.object.shade_smooth()
    bm_cut = t.modifiers.new("yarim", "BOOLEAN")                     # alt yarimi kes (kanca)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x + r * 2.2, y, z + H - r * 2.0))
    c = bpy.context.active_object; c.scale = (r * 8, r * 4, r * 4); c.hide_render = True; c.hide_viewport = True
    bm_cut.object = c; bm_cut.operation = "DIFFERENCE"


def hediye(x, y, z, s, rnd):
    """hediye kutusu: parlak kutu + capraz kurdele + fiyonk"""
    renk = rnd.choice(SEKER); kur = rnd.choice(("#ffd21a", "#fff0f4", "#20c850", "#ff2a4a"))
    kutu("hediye", (x, y, z + s / 2), (s, s, s), mat_m(renk, 0.25, 0.7), egim=0.04 * s)
    km = mat_m(kur, 0.2, 0.8)
    kutu("kur1", (x, y, z + s / 2), (s * 1.02, s * 0.16, s * 1.02), km, egim=0)
    kutu("kur2", (x, y, z + s / 2), (s * 0.16, s * 1.02, s * 1.02), km, egim=0)
    for d in (-1, 1):
        f = kure((x + d * s * 0.16, y, z + s * 1.08), s * 0.17, km); f.scale = (1.3, 0.6, 0.9)


def kar_tanesi(rnd, n, x_gen, y0, y1, z0, z1, kac=0.0):
    km = mat_emis("kar_tane", lin(hex3("#f0e8ff")), 1.4)
    for _ in range(n):
        x = rnd.uniform(-x_gen, x_gen); y = rnd.uniform(y0, y1); z = rnd.uniform(z0, z1)
        if abs(x) < kac and y < y0 + 12:
            continue
        kure((x, y, z), rnd.uniform(0.04, 0.09) * (1 + (y - y0) / 30), km, sub=1)


def yildizlar(rnd, n):
    sm = mat_emis("yildiz", lin(hex3("#fff6d0")), 6.0)
    for _ in range(n):
        a = rnd.uniform(-1.2, 1.2); e = rnd.uniform(0.22, 0.75); R = 900
        kure((R * math.sin(a) * math.cos(e), R * math.cos(a) * math.cos(e), R * math.sin(e)), rnd.uniform(1.0, 2.4), sm, sub=1)


def aurora(x, y, z, uz, yuk, renk, egri):
    """kuzey isigi: yari saydam isik perdesi (dikey degrade: altta parlak, ustte sonuk), hafif dalgali"""
    m = bpy.data.materials.new("aurora" + renk); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord"); sp = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["UV"], sp.inputs[0])
    rp = nt.nodes.new("ShaderNodeValToRGB"); el = rp.color_ramp.elements
    el[0].position = 0.0; el[0].color = (1, 1, 1, 1); el[1].position = 1.0; el[1].color = (0, 0, 0, 1)
    nt.links.new(sp.outputs["Y"], rp.inputs[0])
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs[0].default_value = (*lin(hex3(renk)), 1); em.inputs[1].default_value = 3.0
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mx = nt.nodes.new("ShaderNodeMixShader")
    mt = nt.nodes.new("ShaderNodeMath"); mt.operation = "MULTIPLY"; mt.inputs[1].default_value = 0.55
    nt.links.new(rp.outputs[0], mt.inputs[0]); nt.links.new(mt.outputs[0], mx.inputs[0])
    nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(mx.outputs[0], o.inputs[0])
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=40, y_subdivisions=2, size=1, location=(x, y, z + yuk / 2))
    p = bpy.context.active_object; p.scale = (uz, yuk, 1); p.rotation_euler = (math.radians(90), 0, 0)
    bpy.ops.object.transform_apply(rotation=True, scale=True)
    for v in p.data.vertices:                                  # perde dalgasi (y ekseninde ileri-geri)
        v.co.y += math.sin(v.co.x / uz * 6.28 * egri) * uz * 0.08
    p.data.materials.append(m); p.visible_shadow = False


def zemin(rnd, y0, y1, x_gen, z=0.0, kac=0.0):
    """kar zemin: genis duzlem + uzaga dogru kar tepecikleri (ufka kadar dolu)"""
    km = mat_kar()
    me = bpy.data.meshes.new("zemin")
    me.from_pydata([(-x_gen, y0, z), (x_gen, y0, z), (x_gen, y1, z), (-x_gen, y1, z)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("zemin", me); bpy.context.collection.objects.link(o); o.data.materials.append(km)
    y = y0 + 6
    while y < y1:
        s = 1.0 + (y - y0) / 30.0
        x = -x_gen + rnd.uniform(0, 8 * s)
        while x < x_gen:
            r = rnd.uniform(2.5, 4.5) * s
            if abs(x) - r < kac:
                x += 8 * s; continue
            t = kure((x, y, z - r * 0.6), r, km, sub=2); t.scale = (1.6, 1.0, 0.6)
            x += 8 * s * rnd.uniform(0.8, 1.3)
        y += 9 * s
    return km


def kar_yigini(x, y, r, rnd):
    """OUT: krema kapli kar yigini - tombul kar kureleri + ustte pembe krema damlasi + seker serpintisi"""
    km = mat_m(KAR, 0.5, 0.15, 0.25)
    for i in range(6):
        a = i * 1.05
        k = kure((x + math.cos(a) * r * 0.45, y + math.sin(a) * r * 0.35, r * 0.25), r * rnd.uniform(0.45, 0.6), km); k.scale = (1, 1, 0.65)
    t = kure((x, y, r * 0.45), r * 0.62, km); t.scale = (1, 1, 0.7)
    kr = kure((x, y, r * 0.78), r * 0.42, mat_m("#ffb0d8", 0.25, 0.7, 0.2)); kr.scale = (1, 1, 0.4)
    for i in range(22):
        a = rnd.uniform(0, 6.28); rr = rnd.uniform(0, r * 0.5)
        s = kure((x + math.cos(a) * rr, y + math.sin(a) * rr, r * 0.8 + rnd.uniform(-0.05, 0.08)), 0.05, mat_m(SEKER[i % 8], 0.2, 0.8), sub=1)
        s.scale = (2.2, 0.8, 0.8); s.rotation_euler = (0, 0, a)


def fener(x, y, H):
    """sokak feneri: koyu yesil direk + sicak isikli kafa + kurdele"""
    silindir((x, y, 0), 0.08, H, mat_m("#0a5a28", 0.35, 0.5), v=12)
    kutu("fener", (x, y, H + 0.2), (0.34, 0.34, 0.4), mat_isik("#ffc860", 6.0), egim=0.04)
    kutu("fcati", (x, y, H + 0.45), (0.44, 0.44, 0.1), mat_m("#0a5a28", 0.35, 0.5), egim=0.03)
    f = kure((x, y - 0.1, H - 0.15), 0.12, mat_m("#ff1a3a", 0.25, 0.8)); f.scale = (1.6, 0.6, 0.9)


# ------------------------------------------------------------------ MEKAN (her iki katmanda; serit sahnesinde uzak kisim holdout)
def mekan(serit_modu, rnd):
    _SM.clear()                                         # ikinci katmanda bos_sahne eski malzemeleri siliyor (36 dersi)
    km = mat_kar("yakin_kar")
    me = bpy.data.meshes.new("yakin_zemin")
    me.from_pydata([(-60, -4, -0.02), (60, -4, -0.02), (60, GECIS, -0.02), (-60, GECIS, -0.02)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("yakin_zemin", me); bpy.context.collection.objects.link(o); o.data.materials.append(km)
    # yakin kenar: pistin iki yaninda kucuk camlar + hediye kutulari + fenerler (koridor bos; OUT yiginlarinin yeri acik)
    for s in (-1, 1):
        for (x, y, H) in ((9.5, 1.5, 2.6), (13, 6, 3.4), (8.6, 10, 2.2), (18, 9, 4.2)):
            cam_agaci(s * x, y, 0, H, rnd)
        for (x, y, k) in ((7.6, 2.8, 0.7), (8.2, 3.6, 0.5), (11, 3.0, 0.9), (10.4, 7.6, 0.6), (15, 2, 1.1)):
            hediye(s * x, y, 0, k, rnd)
        for y in (-1.0, 3.4, 7.6):
            fener(s * (PIST + 1.4), y, 2.0)
    for o in bpy.data.objects:
        if o.type == "MESH":
            o["yakin"] = 1
    zemin(rnd, GECIS, 420, 420, kac=PIST + 2)
    # kurabiye koyu: koridorun iki yaninda sira sira evler, araya camlar; kapinin arkasi ve orta koridor acik
    for s in (-1, 1):
        y = GECIS + 3
        while y < 150:
            sc = 1.6 + y / 35
            x = s * rnd.uniform(9, 14) * (1 + y / 60)
            kurabiye_ev(x, y, sc, rnd)
            cam_agaci(x + s * 3.2 * sc, y + 2 * sc, 0, 2.6 * sc, rnd)
            if rnd.random() < 0.7:
                kurabiye_ev(x + s * 6.5 * sc, y + 4 * sc, sc * 1.1, rnd)
            y += 5.5 * sc
    for _ in range(60):                                 # orta-uzak cam ormani + evler (ufuk dolu)
        x = rnd.choice((-1, 1)) * rnd.uniform(25, 260); y = rnd.uniform(60, 420)
        if rnd.random() < 0.55:
            cam_agaci(x, y, 0, rnd.uniform(8, 22), rnd)
        else:
            kurabiye_ev(x, y, rnd.uniform(4, 8), rnd)
    for i in range(40):                                 # koprunun ilerisinde iki yanda seker kamisi direkler (kapiya dogru siralanir)
        s = -1 if i % 2 == 0 else 1; y = GECIS + 2 + (i // 2) * 4.5
        seker_kamisi(s * (PIST + 2.0 + y * 0.02), y, 0, 2.4 + y * 0.03, 0.14 + y * 0.002, "#ff1a3a" if (i // 2) % 2 == 0 else "#20b850")
    # gok: dolunay, aurora perdeleri, yildizlar; kar tanesi havada
    kure((-150, 700, 230), 40, mat_emis("ay", lin(hex3("#fff0c0")), 4.0))
    yildizlar(rnd, 260)
    kar_tanesi(rnd, 420, 30, 2, 60, 0.5, 18, kac=5)
    if serit_modu:
        for o in bpy.data.objects:
            if o.type == "MESH" and not o.get("yakin"):
                o.is_holdout = True


# ------------------------------------------------------------------ SERIT: kurabiye pist + seker kamisi korkuluk isiklari + oklar + OUT kar yiginlari
def serit_esyalari(rnd):
    kutu("pist", (0, (KAP["y"] + 0.4 - 4) / 2, 0.0), (PIST * 2, KAP["y"] + 4.4, 0.16), mat_kurabiye_tas("pist"), egim=0.04, seg=2)
    for s in (-1, 1):                                   # pist kenari: krema kaplamali kurabiye kenar
        kutu("pist_kenar", (s * (PIST + 0.08), (KAP["y"] + 0.4 - 4) / 2, 0.04), (0.26, KAP["y"] + 4.4, 0.3), mat_m(KREMA, 0.3, 0.6, 0.2), egim=0.1, seg=3)
    for s in (-1, 1):                                   # korkuluk: alcak seker kamisi direkler + aradaki kirmizi kurdele + isik toplari
        y = -3.0; i = 0
        while y < KAP["y"] - 0.4:
            silindir((s * (PIST + 0.5), y, 0.0), 0.07, 0.7, mat_cizgili(), v=14)
            kure((s * (PIST + 0.5), y, 0.78), 0.12, mat_isik(ISIK[i % 5], 5.0))
            y += 1.3; i += 1
        kutu("kurdele", (s * (PIST + 0.5), (KAP["y"] - 3.4) / 2, 0.55), (0.06, KAP["y"] + 2.6, 0.12), mat_m("#ff1a3a", 0.25, 0.7), egim=0)
    for j, x in enumerate((-1.7, 1.7)):                 # yon oklari: kirmizi ve yesil seker
        ok = mat_m("#ff2a4a" if j == 0 else "#20c850", 0.25, 0.8)
        for y in (4.6, 6.2):
            nok = [(x - 0.6, y - 0.4), (x, y), (x + 0.6, y - 0.4), (x + 0.6, y - 0.68), (x, y - 0.28), (x - 0.6, y - 0.68)]
            me = bpy.data.meshes.new("ok"); me.from_pydata([(a, b, 0.17) for a, b in nok], [], [list(range(6))]); me.update()
            o = bpy.data.objects.new("ok", me); bpy.context.collection.objects.link(o); o.data.materials.append(ok)
            o.modifiers.new("k", "SOLIDIFY").thickness = 0.02
    for s in (-1, 1):                                   # OUT ani: iki dis tarafta krema kapli kar yigini
        kar_yigini(s * 5.6, 5.0, 1.5, random.Random(38 + s))


def kapi():
    """seker kamisi kemer: iki kalin cizgili kule, ustte cam dali celenk kiris + kirmizi fiyonklar + isik dizisi; LED tabela"""
    Y, W_, H_, K = KAP["y"], KAP["w"], KAP["h"], KAP["kalin"]
    xk = W_ / 2 + K / 2
    for s in (-1, 1):
        silindir((s * xk, Y, 0), K * 0.55, H_ + K + 0.3, mat_cizgili(), v=32)
        kure((s * xk, Y, H_ + K + 0.45), K * 0.6, mat_isik("#ffd21a", 6.0))
    yuvarlak_kutu("kiris", (0, Y, H_ + K / 2), (W_ + 2 * K, K + 0.1, K), mat_m(CAM_K, 0.5, 0.2), egim=0.2, seg=5)
    gm = mat_m(CAM, 0.45, 0.25)
    rnd = random.Random(381)
    for i in range(40):                                 # celenk: kiris onunde cam dali kumeleri
        x = -W_ / 2 - K + i * (W_ + 2 * K) / 39
        k = kure((x, Y - 0.32, H_ + K * 0.5 + rnd.uniform(-0.15, 0.15)), 0.3, gm, sub=2); k.scale = (1.1, 0.7, 0.9)
    for i in range(16):
        x = -W_ / 2 - K + i * (W_ + 2 * K) / 15
        kure((x, Y - 0.55, H_ + K * 0.4 + (i % 2) * 0.2), 0.09, mat_isik(ISIK[i % 5], 6.0), sub=1)
    for x in (-W_ / 2, 0, W_ / 2):                      # fiyonklar
        for d in (-1, 1):
            f = kure((x + d * 0.22, Y - 0.6, H_ + K * 0.55), 0.22, mat_m("#ff1a3a", 0.25, 0.8)); f.scale = (1.4, 0.5, 0.9)
        kure((x, Y - 0.62, H_ + K * 0.55), 0.1, mat_m("#ffd21a", 0.2, 0.8))
    yuvarlak_kutu("tabela", (0, Y, H_ + K + 0.75), (W_ * 0.6, 0.2, 0.7), mat_pbr("tabela", "#15171a", 0.35, metal=0.4), egim=0.05, seg=3)
    me = bpy.data.meshes.new("led_yuz"); a, b = W_ * 0.28, 0.28; z0 = H_ + K + 0.75
    me.from_pydata([(-a, Y - 0.11, z0 - b), (a, Y - 0.11, z0 - b), (a, Y - 0.11, z0 + b), (-a, Y - 0.11, z0 + b)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("led_yuz", me); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat_emis("led_yuz", lin(hex3("#5a0a1a")), 1.2))
    k = kure((0, Y, H_ + K + 1.15), 0.5, mat_m(KAR, 0.5, 0.1, 0.2)); k.scale = (W_ * 0.6, 0.6, 0.35)   # tabela ustunde kar


def serit_katmani():
    sc = koy_sahnesi(1920, 1080, True)
    kam = kamera(sc)
    rnd = random.Random(38)
    isiklar()
    mekan(True, random.Random(38))
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
    mekan(False, random.Random(38))
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
log("bitti (kurabiye)", YERLESIM.get(ON_EK + "aciklik_p1"))
