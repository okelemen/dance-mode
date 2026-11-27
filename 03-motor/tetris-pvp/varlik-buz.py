"""HUMAN TETRIS 40. video (REF-092 yapi, 1P SOLO) - GUNDUZ DONMUS GOL BUZ PATENI, CILALI 3D OYUN GORUNUMU, TEK serit.
varlik.py calistirir (--mod buz). Iskelet varlik-mercan.py (39, tek serit) - katmanlar, kamera, yerlesim anahtarlari ayni
(tek serit motoru 33/35/36'nin bekledigi aciklik_p1 / ampul_p1 / dag / yol).

Mekan kullanici karari (27 Kas 2026): gunduz, parlak kis gunesi, donmus gol. Pist puruzsuz mavi-beyaz buz + paten izleri + parlak
yon oklari; iki yanda karli susllu Noel agaclari, kar yiginlari, ahsap kulubeler, fener direkleri, ampul dizileri; arkada karli
tepeler + acik mavi gok; gokte suzulen kar taneleri ve parilti. Kapi: buz kristali kemer + cam dali celengi + ampul dizisi + tabela.
Pist korkulugu: seker kamisi direkler (REF-092'nin seker kamisi kopru korkulugundan yapi olarak).
OUT ani: duvar karakteri pistin yanindaki KAR YIGININA iter, karakter kara gomulur (kar pufu motorda).
Telif (md. 16): genel kis/Noel ogeleri; marka, bilinen film karakteri yok.
prompts.chat (md. 23): "Vintage Snow Globe of a Tiny Winter Village" -> buzlu camlar, sicak pencere isigi, ampul dizisi, kar tanesi
(gece ve makro foto gorunumu alinmaz).
§4 CILALI 3D OYUN GORUNUMU: doygun renk, tombul hatlar, parlak kaplama (coat), gercek isik-golge (Cycles); foto dokusu yok.
§8 SOLUK YASAK: buz beyaz-gri degil doygun buz mavisi; kar mavi-lila golgeli (gri degil); agaclar zumrut, susler tam doygun.
Ekran dolu (Masaustu md. 7): gok bolgesi kar taneleri + parilti + karli tepeler + ust ampul celengi; zemin ufka kadar orman ve kar.
"""

import random
YERLESIM.clear()
KAPAK = YALNIZ == "kapak"
POZLAMA = float(arg("--pozlama", arg("--kapak-pozlama", "0")))
GUNES = float(arg("--gunes", "3.0"))
ON_EK = "kapak-" if KAPAK else ""
KAP = {"y": 8.6, "w": 7.4, "h": 3.7, "kalin": 0.55}       # tek serit motoru ile ayni olcu
KAM = {"z": 2.3, "egim": 5.0, "lens": 18.0, "sensor": 24.0}
if KAPAK:
    KAM.update({"z": float(arg("--kapak-z", "2.0")), "egim": float(arg("--kapak-egim", "3.0")), "lens": float(arg("--kapak-lens", "16.0"))})
PIST = 3.9
GECIS = 11.5
GOK_UFUK, GOK_ORTA, GOK_UST = "#7ad8ff", "#2a9aff", "#1a5aff"      # acik mavi -> doygun mavi (beyaz-gri degil)
SIS = "#8acfff"                                            # mist: uzak orman acik mavi kis havasina karisir
KAR, KAR_G = "#f4f8ff", "#a8c0ff"                          # kar: beyaz + mavi-lila golge tonu
BUZ, BUZ_A = "#3aa8ff", "#7ad0ff"                          # buz: doygun buz mavisi + acik catlak/parlama tonu
CAM = ("#0a9a4a", "#0a8a5a", "#14a83a")                    # zumrut cam yesilleri
SUS = ("#ff1a3a", "#ffc81a", "#1a6aff", "#ff3ac8", "#9a3aff", "#ff7a1a")   # Noel topu renkleri
AMPUL = ("#ff2a3a", "#ffd21a", "#2ad86a", "#3aa8ff", "#ff6ad0")


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
    bg_i = nt.nodes.new("ShaderNodeBackground"); bg_i.inputs[1].default_value = 0.6
    bg_i.inputs[0].default_value = (*lin(hex3("#5a9aff")), 1)        # gok ortam isigi: mavi (kar golgesi gri degil mavi-lila)
    mx = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(lp.outputs["Is Camera Ray"], mx.inputs[0])
    nt.links.new(bg_i.outputs[0], mx.inputs[1]); nt.links.new(bg_k.outputs[0], mx.inputs[2])
    o = nt.nodes.new("ShaderNodeOutputWorld"); nt.links.new(mx.outputs[0], o.inputs[0])
    sc.view_layers[0].use_pass_mist = True
    sc.world.mist_settings.start = 60.0; sc.world.mist_settings.depth = 420.0; sc.world.mist_settings.falloff = "QUADRATIC"
    sc.use_nodes = True; sc.render.use_compositing = True; ct = sc.node_tree; ct.nodes.clear()
    rl = ct.nodes.new("CompositorNodeRLayers"); co = ct.nodes.new("CompositorNodeComposite")
    mk = ct.nodes.new("CompositorNodeMath"); mk.operation = "MULTIPLY"; mk.inputs[1].default_value = 0.55
    ct.links.new(rl.outputs["Mist"], mk.inputs[0])
    mm = ct.nodes.new("CompositorNodeMixRGB"); mm.blend_type = "MIX"
    ct.links.new(mk.outputs[0], mm.inputs[0]); ct.links.new(rl.outputs["Image"], mm.inputs[1])
    mm.inputs[2].default_value = (*lin(hex3(SIS)), 1)
    gl = ct.nodes.new("CompositorNodeGlare"); gl.glare_type = "FOG_GLOW"; gl.quality = "HIGH"; gl.threshold = 1.2; gl.size = 6; gl.mix = -0.5
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
    if KAPAK and arg("--kapak-dof", "0") != "0":            # mobil kapak (md. 30): kapi net, arka orman yumusak bulanik
        kam.data.dof.use_dof = True; kam.data.dof.focus_distance = KAP["y"]; kam.data.dof.aperture_fstop = float(arg("--kapak-dof", "1.2"))
    return kam


def isiklar():
    # alcak sicak kis gunesi (onden-yandan) -> karda uzun mavi golge, buzda parlama; mavi gok dolgu
    bpy.ops.object.light_add(type="SUN", location=(0, 0, 30))
    g = bpy.context.active_object; g.data.energy = GUNES; g.data.angle = math.radians(3.0)
    g.data.color = lin(hex3("#ffe8c8"))
    g.rotation_euler = Vector((0.35, 0.55, -0.7)).to_track_quat("-Z", "Y").to_euler()
    bpy.ops.object.light_add(type="SUN", location=(0, 0, 30))
    f = bpy.context.active_object; f.data.energy = 0.9; f.data.angle = math.radians(12.0)
    f.data.color = lin(hex3("#9ac8ff"))
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
        _SM[key] = mat_emis("isik" + renk, lin(hex3(renk)), guc)
    return _SM[key]


def mat_kar(ad="kar"):
    """kar: beyaz + mavi-lila tonlu noise (gri degil), yumusak kabartma, hafif ic sacilim"""
    if ad in _SM:
        return _SM[ad]
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    ns = nt.nodes.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value = 0.9; ns.inputs["Detail"].default_value = 3
    nt.links.new(geo.outputs["Position"], ns.inputs["Vector"])
    rp = nt.nodes.new("ShaderNodeValToRGB"); el = rp.color_ramp.elements
    el[0].position = 0.35; el[0].color = (*lin(hex3("#b8d0ff")), 1); el[1].position = 0.7; el[1].color = (*lin(hex3(KAR)), 1)
    nt.links.new(ns.outputs["Fac"], rp.inputs[0]); nt.links.new(rp.outputs[0], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.7
    b.inputs["Subsurface Weight"].default_value = 0.25; b.inputs["Subsurface Radius"].default_value = (0.3, 0.5, 1.0)
    n2 = nt.nodes.new("ShaderNodeTexNoise"); n2.inputs["Scale"].default_value = 18.0; n2.inputs["Detail"].default_value = 4
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.25
    nt.links.new(n2.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    _SM[ad] = m
    return m


def mat_buz(ad="buz", acik=False):
    """donmus gol buzu: doygun buz mavisi + acik voronoi catlak cizgileri + ayna gibi kaplama"""
    if ad in _SM:
        return _SM[ad]
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    vr = nt.nodes.new("ShaderNodeTexVoronoi"); vr.feature = "DISTANCE_TO_EDGE"; vr.inputs["Scale"].default_value = 0.35
    nt.links.new(geo.outputs["Position"], vr.inputs["Vector"])
    ns = nt.nodes.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value = 0.25; ns.inputs["Detail"].default_value = 3
    nt.links.new(geo.outputs["Position"], ns.inputs["Vector"])
    rp = nt.nodes.new("ShaderNodeValToRGB"); el = rp.color_ramp.elements          # derin buz tonlari (noise)
    el[0].position = 0.3; el[0].color = (*lin(hex3("#0a5aff" if not acik else "#0a78ff")), 1)   # sahne 1: pist beyaza patliyordu (S<0,35 %18)
    el[1].position = 0.75; el[1].color = (*lin(hex3("#1a8aff" if not acik else "#2aa0ff")), 1)
    nt.links.new(ns.outputs["Fac"], rp.inputs[0])
    cz = nt.nodes.new("ShaderNodeValToRGB"); ce = cz.color_ramp.elements           # catlak: kenara yakin ince acik cizgi
    ce[0].position = 0.0; ce[0].color = (1, 1, 1, 1); ce[1].position = 0.035; ce[1].color = (0, 0, 0, 1)
    nt.links.new(vr.outputs["Distance"], cz.inputs[0])
    mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"
    nt.links.new(cz.outputs[0], mx.inputs["Factor"]); nt.links.new(rp.outputs[0], mx.inputs[6])
    mx.inputs[7].default_value = (*lin(hex3(BUZ_A)), 1)
    nt.links.new(mx.outputs[2], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.3                # sahne 1: ayna buz beyaz gok/kari yansitip soldu
    b.inputs["Coat Weight"].default_value = 0.25; b.inputs["Coat Roughness"].default_value = 0.08
    _SM[ad] = m
    return m


def mat_kristal(renk="#6ac8ff"):
    """buz kristali (kapi): yari saydam mavi cam, hafif isik (cilali oyun gorunumu, gri degil)"""
    key = ("kr", renk)
    if key in _SM:
        return _SM[key]
    m = mat_pbr("kristal" + renk, renk, 0.05, kaplama=0.8)
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Transmission Weight"].default_value = 0.55; b.inputs["IOR"].default_value = 1.31
    b.inputs["Emission Color"].default_value = (*lin(hex3(renk)), 1); b.inputs["Emission Strength"].default_value = 0.35
    _SM[key] = m
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


# ------------------------------------------------------------------ ogeler
def noel_agaci(x, y, H, rnd, sus=True, yildiz=True):
    """tombul Noel agaci: 3-4 ust uste koni (zumrut) + her katta kar sapkasi + renkli toplar + tepede altin yildiz"""
    yesil = mat_m(rnd.choice(CAM), 0.5, 0.25)
    silindir((x, y, 0), 0.09 * H, 0.16 * H, mat_m("#7a3a1a", 0.6, 0.1), v=12)
    kat = rnd.choice((3, 4)); z = 0.12 * H
    for i in range(kat):
        r = 0.38 * H * (1 - i / (kat + 0.6)); h = 0.42 * H * (1 - i * 0.12)
        silindir((x, y, z), r, h, yesil, v=24, r2=r * 0.18)
        k = silindir((x, y, z + h * 0.62), r * 0.5, h * 0.12, mat_kar(), v=24, r2=r * 0.28)   # kat ustune kar sapkasi
        if sus:
            for j in range(5 + 2 * (kat - i)):
                a = rnd.uniform(0, 6.28); zz = z + h * rnd.uniform(0.1, 0.45); rr = r * (1 - (zz - z) / h * 0.82) * 0.98
                kure((x + math.cos(a) * rr, y + math.sin(a) * rr, zz), 0.035 * H, mat_m(rnd.choice(SUS), 0.18, 0.9, metal=0.3), sub=1)
        z += h * 0.6
    if yildiz:
        kure((x, y, z + 0.08 * H), 0.04 * H, mat_m("#ffb800", 0.2, 0.8, metal=0.7), sub=2)   # sahne 1: isikli yildiz sari leke okundu


def kar_yigini(x, y, r, rnd, ezik=0.55):
    """tombul kar yigini: 3-5 basik kure kumesi"""
    for _ in range(rnd.randint(3, 5)):
        dx, dy = rnd.uniform(-0.5, 0.5) * r, rnd.uniform(-0.3, 0.3) * r
        rr = r * rnd.uniform(0.6, 1.0)
        k = kure((x + dx, y + dy, rr * 0.2), rr, mat_kar(), sub=3); k.scale = (1.2, 1.0, ezik)


def kulube(x, y, s, rnd, yon=1):
    """ahsap kulube: kirmizi/kahve govde + karli ucgen cati + sicak pencere isigi + kapida celenk"""
    govde = mat_m(rnd.choice(("#c81a1a", "#a8441a", "#d8302a")), 0.55, 0.15)
    kutu("kulube", (x, y, 0.55 * s), (1.8 * s, 1.5 * s, 1.1 * s), govde, egim=0.04 * s)
    for sg in (-1, 1):                                                    # cati: iki egik kar plakasi
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x + sg * 0.5 * s, y, 1.38 * s))
        c = bpy.context.active_object; c.scale = (1.15 * s, 1.75 * s, 0.14 * s); c.rotation_euler = (0, -sg * 0.62, 0)
        c.data.materials.append(mat_kar())
    for wx in (-0.45, 0.45):                                              # sicak pencere
        kutu("pencere", (x + wx * s, y - 0.76 * s, 0.62 * s), (0.36 * s, 0.04, 0.36 * s), mat_isik("#ffb84a", 3.5), egim=0)
    k = kure((x, y - 0.8 * s, 0.75 * s), 0.18 * s, mat_m("#0a9a4a", 0.5, 0.2), sub=2); k.scale = (1, 0.4, 1)   # kapi celengi
    kure((x, y - 0.86 * s, 0.62 * s), 0.06 * s, mat_m("#ff1a3a", 0.2, 0.8), sub=1)


def fener(x, y, H):
    """fener diregi: koyu yesil metal direk + ustte sicak isikli fener + kar kapagi"""
    silindir((x, y, 0), 0.07, H, mat_m("#0a3a2a", 0.3, 0.5, metal=0.6), v=12)
    kutu("fener", (x, y, H + 0.2), (0.3, 0.3, 0.4), mat_isik("#ffc860", 5.0), egim=0.04)
    silindir((x, y, H + 0.4), 0.24, 0.12, mat_kar(), v=16, r2=0.06)


def ampul_dizisi(a, b, n, sark=0.4, guc=6.0):
    """iki nokta arasinda sarkan renkli ampul dizisi (ince kablo + kureler)"""
    a, b = Vector(a), Vector(b)
    nok = []
    for i in range(n + 1):
        t = i / n; p = a.lerp(b, t); p.z -= sark * 4 * t * (1 - t); nok.append(p)
    km = mat_m("#0a2a1a", 0.5, 0.0)
    for i in range(n):
        egik_boru(nok[i], nok[i + 1], 0.012, km, v=6)
        kure(nok[i + 1] - Vector((0, 0, 0.06)), 0.07, mat_isik(AMPUL[i % len(AMPUL)], guc), sub=1)


def kar_tanesi(x, y, z, s, mat, a0=0.0):
    """alti kollu kar tanesi: 6 ince kol + kol uclarinda kucuk catal"""
    for i in range(6):
        a = a0 + i * 1.0472
        u = Vector((x + math.cos(a) * s, y, z + math.sin(a) * s))
        egik_boru((x, y, z), u, 0.06 * s, mat, v=6)
        for d in (-0.6, 0.6):
            v = u - Vector((math.cos(a) * s * 0.35, 0, math.sin(a) * s * 0.35))
            egik_boru(v, v + Vector((math.cos(a + d) * s * 0.28, 0, math.sin(a + d) * s * 0.28)), 0.04 * s, mat, v=6)
    kure((x, y, z), 0.1 * s, mat, sub=1)


def seker_kamisi(x, y, H, cizgi=8):
    """seker kamisi direk: kirmizi-beyaz serit halkalar + ustte kivrik kanca (REF-092 korkuluk yapisi)"""
    kir, bey = mat_m("#ff1a2a", 0.25, 0.8), mat_m("#fff4f4", 0.25, 0.8)
    dh = H / cizgi
    for i in range(cizgi):
        silindir((x, y, i * dh), 0.07, dh, kir if i % 2 == 0 else bey, v=14)
    for i in range(6):                                                    # kanca: yarim halka
        a0, a1 = i * math.pi / 6, (i + 1) * math.pi / 6
        p0 = Vector((x + 0.16 - math.cos(a0) * 0.16, y, H + math.sin(a0) * 0.16))
        p1 = Vector((x + 0.16 - math.cos(a1) * 0.16, y, H + math.sin(a1) * 0.16))
        egik_boru(p0, p1, 0.07, kir if i % 2 == 0 else bey, v=12)


def tepe(x, y, r, h):
    """karli tepe (uzak): basik dev kure, kar malzemesi"""
    k = kure((x, y, -h * 0.35), r, mat_kar("tepe_kar"), sub=3); k.scale = (1.0, 0.6, h / r)


# ------------------------------------------------------------------ MEKAN (her iki katmanda; serit sahnesinde uzak kisim holdout)
def mekan(serit_modu, rnd):
    _SM.clear()                                         # ikinci katmanda bos_sahne eski malzemeleri siliyor (36 dersi)
    gb = mat_buz("gol_buz")
    me = bpy.data.meshes.new("yakin_zemin")
    me.from_pydata([(-60, -4, -0.02), (60, -4, -0.02), (60, GECIS, -0.02), (-60, GECIS, -0.02)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("yakin_zemin", me); bpy.context.collection.objects.link(o); o.data.materials.append(gb)
    # yakin kenar: gol kiyisinda kar setleri + Noel agaclari + kulubeler + fenerler (koridor bos; OUT kar yiginlarinin yeri acik)
    for s in (-1, 1):
        for (x, y, k) in ((10.5, 2.0, 4.2), (14.5, 7.5, 5.4), (9.0, 10.2, 3.6), (19.5, 3.5, 6.2), (12.2, 4.4, 3.0), (17.0, 10.8, 5.0)):
            noel_agaci(s * x, y, k, rnd)
        for (x, y, k) in ((8.0, 0.2, 1.1), (11.5, 9.0, 1.3), (16.5, 0.8, 1.6), (7.6, 6.8, 0.9)):
            kar_yigini(s * x, y, k, rnd)
        kulube(s * 15.5, 4.6, 1.5, rnd)
        for y in (-1.0, 3.4, 7.6):
            fener(s * (PIST + 1.5), y, 2.0)
        kar_yigini(s * (PIST + 2.6), 1.6, 0.6, rnd, ezik=0.4)
        kar_yigini(s * (PIST + 2.4), 9.6, 0.7, rnd, ezik=0.4)
    for y in (-1.0, 3.4, 7.6):                            # fenerler arasinda sarkan ampul dizileri (her iki yan)
        for s in (-1, 1):
            if y < 7:
                ampul_dizisi((s * (PIST + 1.5), y, 2.15), (s * (PIST + 1.5), y + 4.4, 2.15), 8, sark=0.25)
    for o in bpy.data.objects:
        if o.type == "MESH":
            o["yakin"] = 1
    # uzak: gol buzu kapinin arkasinda devam eder, kiyida kar + orman + tepeler
    me = bpy.data.meshes.new("gol_uzak")
    me.from_pydata([(-26, GECIS, -0.02), (26, GECIS, -0.02), (60, 140, -0.02), (-60, 140, -0.02)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("gol_uzak", me); bpy.context.collection.objects.link(o); o.data.materials.append(mat_buz("gol_buz_u", acik=True))
    me = bpy.data.meshes.new("kiyi_kar")
    me.from_pydata([(-420, GECIS, -0.05), (420, GECIS, -0.05), (420, 520, -0.05), (-420, 520, -0.05)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("kiyi_kar", me); bpy.context.collection.objects.link(o); o.data.materials.append(mat_kar())
    for s in (-1, 1):                                      # golun iki kiyisi: sik orman seridi (kapi arkasi ve orta koridor acik)
        y = GECIS + 2
        while y < 160:
            sc = 1.0 + y / 40
            x = s * rnd.uniform(11, 16) * (1 + y / 70)
            noel_agaci(x, y, 4.5 * sc * rnd.uniform(0.8, 1.25), rnd, sus=y < 60)
            noel_agaci(x + s * 4.2 * sc, y + 2 * sc, 5.5 * sc * rnd.uniform(0.8, 1.2), rnd, sus=False, yildiz=y < 60)
            if rnd.random() < 0.5:
                kar_yigini(x - s * 2.6 * sc, y + 1 * sc, 1.2 * sc, rnd)
            if rnd.random() < 0.18 and y < 90:
                kulube(x + s * 8 * sc, y + 3 * sc, 1.6 * sc, rnd)
            y += 4.5 * sc
    for _ in range(150):                                   # golun arkasinda uzak orman (ufuk dolu)
        x = rnd.uniform(-300, 300); y = rnd.uniform(150, 330)
        noel_agaci(x, y, rnd.uniform(10, 22), rnd, sus=False, yildiz=False)
    for (x, y, r, h) in ((-160, 430, 150, 70), (40, 470, 190, 95), (230, 420, 140, 60), (-330, 470, 170, 85), (380, 480, 160, 75)):
        tepe(x, y, r, h)                                   # karli tepeler (gokun alt yarisini doldurur)
    # gok: suzulen kar taneleri + parilti (ekran dolu), ust ampul celengi
    tm = mat_isik("#ffffff", 1.6); pm = mat_isik("#e0f4ff", 3.0)
    for _ in range(46):
        x = rnd.uniform(-34, 34); y = rnd.uniform(18, 46); z = rnd.uniform(4, 20)
        if abs(x) < 6 and z < 8:
            continue
        kar_tanesi(x, y, z, rnd.uniform(0.25, 0.6) * (1 + y / 40), tm, rnd.uniform(0, 1))
    for _ in range(380):
        x = rnd.uniform(-30, 30); y = rnd.uniform(4, 60); z = rnd.uniform(0.8, 18)
        if abs(x) < 5 and y < 14:
            continue
        kure((x, y, z), rnd.uniform(0.03, 0.08) * (1 + y / 30), pm, sub=1)
    if serit_modu:
        for o in bpy.data.objects:
            if o.type == "MESH" and not o.get("yakin"):
                o.is_holdout = True


# ------------------------------------------------------------------ SERIT: buz pist + paten izleri + seker kamisi korkuluk + oklar + OUT kar yiginlari
def serit_esyalari(rnd):
    kutu("pist", (0, (KAP["y"] + 0.4 - 4) / 2, 0.0), (PIST * 2, KAP["y"] + 4.4, 0.16), mat_buz("pist_buz", acik=True), egim=0.04, seg=2)
    iz = mat_m("#e8f8ff", 0.15, 0.6)
    for k in range(4):                                    # paten izleri: hafif kivrimli ince acik cizgiler (sahne 1: 7 iz sagda demet oldu)
        x0 = (-2.6, -0.9, 0.9, 2.6)[k] + rnd.uniform(-0.3, 0.3); a = rnd.uniform(0.3, 0.6); f = rnd.uniform(0.3, 0.5); ph = rnd.uniform(0, 6)
        y = -3.0
        while y < KAP["y"] - 0.6:
            x1 = x0 + a * math.sin(f * y + ph); x2 = x0 + a * math.sin(f * (y + 0.5) + ph)
            if abs(x1) < PIST - 0.3 and abs(x2) < PIST - 0.3:
                egik_boru((x1, y, 0.165), (x2, y + 0.5, 0.165), 0.012, iz, v=6)
            y += 0.5
    for s in (-1, 1):                                     # pist kenari: alcak kar seti
        kutu("kar_set", (s * (PIST + 0.2), (KAP["y"] - 3.4) / 2, 0.12), (0.5, KAP["y"] + 2.6, 0.26), mat_kar(), egim=0.12, seg=3)
    for s in (-1, 1):                                     # korkuluk: seker kamisi direkler + ustte ampul
        y = -3.0; i = 0
        while y < KAP["y"] - 0.4:
            seker_kamisi(s * (PIST + 0.5), y, 0.75)
            kure((s * (PIST + 0.5), y, 1.02), 0.1, mat_isik(AMPUL[i % len(AMPUL)], 5.0), sub=1)
            y += 1.3; i += 1
        kutu("celenk", (s * (PIST + 0.5), (KAP["y"] - 3.4) / 2, 0.55), (0.1, KAP["y"] + 2.6, 0.12), mat_m("#0a9a4a", 0.5, 0.2), egim=0)
    for j, x in enumerate((-1.7, 1.7)):                   # yon oklari: kirmizi ve yesil (beyaz-mavi buzda okunur)
        ok = mat_m("#ff1a3a" if j == 0 else "#0ab84a", 0.25, 0.8)
        for y in (4.6, 6.2):
            nok = [(x - 0.6, y - 0.4), (x, y), (x + 0.6, y - 0.4), (x + 0.6, y - 0.68), (x, y - 0.28), (x - 0.6, y - 0.68)]
            me = bpy.data.meshes.new("ok"); me.from_pydata([(a, b, 0.17) for a, b in nok], [], [list(range(6))]); me.update()
            o = bpy.data.objects.new("ok", me); bpy.context.collection.objects.link(o); o.data.materials.append(ok)
            o.modifiers.new("k", "SOLIDIFY").thickness = 0.02
    for s in (-1, 1):                                     # OUT ani: iki dis tarafta buyuk yumusak kar yigini
        kar_yigini(s * 5.6, 5.0, 1.5, random.Random(40 + s), ezik=0.7)


def kapi():
    """buz kristali kemer: iki ust uste buz blogu kule + tepede kristal sivri uclar, buz kiris + cam dali celengi (kirmizi kurdele)
    + ampul dizisi (motor ampul_p1 hatti) + LED tabela; kiris altinda buz sarkitlari"""
    Y, W_, H_, K = KAP["y"], KAP["w"], KAP["h"], KAP["kalin"]
    xk = W_ / 2 + K / 2
    rnd = random.Random(401)
    for s in (-1, 1):
        n = 5; dh = (H_ + K + 0.2) / n
        for i in range(n):                                # buz bloklari (hafif kaydirmali)
            yuvarlak_kutu("buz_blok", (s * xk + rnd.uniform(-0.05, 0.05), Y, i * dh + dh / 2), (K * 1.25, K * 1.25, dh * 0.94),
                          mat_kristal(("#6ac8ff", "#4ab0ff", "#8ad8ff")[i % 3]), egim=0.08, seg=3)
        for j in range(4):                                # kule tepesinde kristal sivri uclar
            a = j * 1.57 + 0.4
            egik_boru((s * xk + math.cos(a) * 0.12, Y + math.sin(a) * 0.12, H_ + K + 0.2),
                      (s * xk + math.cos(a) * 0.32, Y + math.sin(a) * 0.2, H_ + K + 0.2 + rnd.uniform(0.6, 1.0)), 0.13, mat_kristal("#9ae0ff"), r2=0.01, v=6)
    yuvarlak_kutu("kiris", (0, Y, H_ + K / 2), (W_ + 2 * K, K + 0.1, K), mat_kristal("#5ab8ff"), egim=0.18, seg=4)
    for i in range(22):                                   # kiris altinda buz sarkitlari
        x = -W_ / 2 + 0.2 + i * (W_ - 0.4) / 21
        L = rnd.uniform(0.18, 0.42)
        egik_boru((x, Y - 0.1, H_ + 0.02), (x, Y - 0.1, H_ + 0.02 - L), 0.05, mat_kristal("#bfeaff"), r2=0.005, v=6)
    cm = mat_m("#0a8a3a", 0.55, 0.2)
    for i in range(26):                                   # cam dali celengi: kiris onunde tombul yesil topuzlar
        x = -W_ / 2 - K + i * (W_ + 2 * K) / 25
        k = kure((x, Y - 0.34, H_ + K * 0.78 + rnd.uniform(-0.05, 0.05)), 0.24, cm, sub=2); k.scale = (1.2, 0.7, 0.8)
        if i % 3 == 0:
            kure((x, Y - 0.5, H_ + K * 0.78), 0.09, mat_m(SUS[i % len(SUS)], 0.18, 0.9, metal=0.3), sub=1)
    for x in (-W_ / 2 - K * 0.2, W_ / 2 + K * 0.2):       # kosede kirmizi kurdele
        for d in (-1, 1):
            k = kure((x + d * 0.22, Y - 0.5, H_ + K * 0.82), 0.18, mat_m("#ff1a2a", 0.3, 0.7), sub=2); k.scale = (1.3, 0.4, 0.8)
        kure((x, Y - 0.52, H_ + K * 0.82), 0.1, mat_m("#ff1a2a", 0.3, 0.7), sub=2)
    for i in range(16):                                   # ampul dizisi (motor ampul_p1 ile ayni hat)
        x = -W_ / 2 - K + i * (W_ + 2 * K) / 15
        kure((x, Y - 0.55, H_ + K * 0.4 + (i % 2) * 0.2), 0.09, mat_isik(AMPUL[i % len(AMPUL)], 6.0), sub=1)
    kar_tanesi(0, Y - 0.62, H_ + K * 0.55, 0.32, mat_isik("#e8f8ff", 3.0))          # kiris ortasinda kar tanesi
    yuvarlak_kutu("tabela", (0, Y, H_ + K + 0.75), (W_ * 0.6, 0.2, 0.7), mat_pbr("tabela", "#15171a", 0.35, metal=0.4), egim=0.05, seg=3)
    me = bpy.data.meshes.new("led_yuz"); a, b = W_ * 0.28, 0.28; z0 = H_ + K + 0.75
    me.from_pydata([(-a, Y - 0.11, z0 - b), (a, Y - 0.11, z0 - b), (a, Y - 0.11, z0 + b), (-a, Y - 0.11, z0 + b)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("led_yuz", me); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat_emis("led_yuz", lin(hex3("#0a2a5a")), 1.2))
    kutu("tabela_kar", (0, Y, H_ + K + 1.12), (W_ * 0.62, 0.26, 0.1), mat_kar(), egim=0.05, seg=2)    # tabela ustunde kar


def serit_katmani():
    sc = koy_sahnesi(1920, 1080, True)
    kam = kamera(sc)
    rnd = random.Random(40)
    isiklar()
    mekan(True, random.Random(40))
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
    mekan(False, random.Random(40))
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
log("bitti (buz)", YERLESIM.get(ON_EK + "aciklik_p1"))
