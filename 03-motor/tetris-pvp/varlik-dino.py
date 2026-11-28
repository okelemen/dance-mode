"""HUMAN TETRIS 43. video (REF-095 yapi, 1P SOLO) - GUNDUZ DINOZOR VADISI, CILALI 3D OYUN GORUNUMU, TEK serit.
varlik.py calistirir (--mod dino). Iskelet varlik-col.py (41, tek serit) - katmanlar, kamera, yerlesim anahtarlari ayni
(tek serit motoru 33/35/36/37/38'in bekledigi aciklik_p1 / ampul_p1 / dag / yol).

Mekan kullanici karari (28 Kas 2026, A): gunduz, parlak gunes. Pist sikistirilmis kiremit-kahve toprak + dev uc parmakli ayak izleri
+ parlak yon oklari; iki yanda sikas agaclari, dev egreltiotlari, renkli benekli dev yumurta yuvalari, kemik cit, cicekli calilar, mesaleler;
arkada yesil tepeler, uzakta tepesinden beyaz duman tuten volkan (lav kanallari), kayalik + selale, yosunlu kayalar, doygun mavi gok;
gokte pterodaktiller + bulut + suzulen polen. Kapi: yosunlu tas kemer + fosil boynuz + kaburga kemeri + sarkan sarmasik + isik dizisi + tabela.
OUT ani: duvar karakteri pistin yanindaki CAMUR BIRIKINTISINE iter, karakter kayar (camur sicramasi motorda).
Telif (md. 16): genel tarih oncesi ogeler; bilinen dinozor filmlerinin logosu/kapisi/karakteri yok.
prompts.chat (md. 23): "dinosaur valley" / "baby t-rex mascot" 0 sonuc -> kendi plan.
§4 CILALI 3D OYUN GORUNUMU: doygun renk, tombul hatlar, parlak kaplama (coat), gercek isik-golge (Cycles); foto dokusu yok.
§8 SOLUK YASAK: cim gri-yesil degil canli yesil, toprak kiremit-turuncu, yumurta/cicek tam doygun, gok derin mavi.
Ekran dolu (Masaustu md. 7): gok bolgesi pterodaktil + polen + tombul bulut + volkan dumani; zemin ufka kadar yesil tepeler.
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
KUM, KUM_A, KUM_G = "#e8803a", "#f2a050", "#b8541a"        # pist toprak: kiremit-turuncu + acik + koyu iz (mat_kum adiyla)
if KAPAK and arg("--kapak-doygun", "0") != "0":
    KUM, KUM_A, KUM_G = "#e8601a", "#ff8a2a", "#a8400a"
CIM, CIM_A, CIM_G = "#3ac82a", "#6ad83a", "#1a9a2a"        # canli yesil cim (gri-yesil degil)
TAS, TAS_A = "#c8783a", "#e0a060"                          # sicak tas
YAPRAK = ("#18b83a", "#0aa04a", "#3ac81a", "#6ad81a")      # egrelti / sikas yesilleri
YUMURTA = ("#ffd81a", "#2ad8c8", "#ff6a9a", "#9a5aff", "#ff8a1a")
CICEK = ("#ff1a6a", "#ff7a0a", "#ffd81a", "#9a2aff", "#ff2ab8")
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


def mat_cim(ad="cim", acik=False):
    """canli yesil cim: noise ile koyu <-> acik yesil + hafif kabartma (gri-yesil degil)"""
    if ad in _SM:
        return _SM[ad]
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    ns = nt.nodes.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value = 0.5; ns.inputs["Detail"].default_value = 4
    nt.links.new(geo.outputs["Position"], ns.inputs["Vector"])
    rp = nt.nodes.new("ShaderNodeValToRGB"); el = rp.color_ramp.elements
    el[0].position = 0.3; el[0].color = (*lin(hex3(CIM_G if not acik else CIM)), 1)
    el[1].position = 0.72; el[1].color = (*lin(hex3(CIM_A if acik else CIM)), 1)
    nt.links.new(ns.outputs["Fac"], rp.inputs[0]); nt.links.new(rp.outputs[0], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.6
    b.inputs["Coat Weight"].default_value = 0.1; b.inputs["Coat Roughness"].default_value = 0.25
    n2 = nt.nodes.new("ShaderNodeTexNoise"); n2.inputs["Scale"].default_value = 6.0
    nt.links.new(geo.outputs["Position"], n2.inputs["Vector"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.12
    nt.links.new(n2.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    _SM[ad] = m
    return m


# ------------------------------------------------------------------ ogeler
def egrelti(x, y, H, rnd):
    """dev egreltiotu: yerden yelpaze gibi acilan 7-9 uzun basik yaprak (tombul, parlak yesil)"""
    for j in range(rnd.randint(7, 9)):
        a = j * 6.283 / 8 + rnd.uniform(-0.3, 0.3)
        d = Vector((math.cos(a), math.sin(a), 0))
        k = kure(Vector((x, y, 0)) + d * 0.45 * H + Vector((0, 0, 0.42 * H)), 0.55 * H, mat_m(rnd.choice(YAPRAK), 0.45, 0.3), sub=2)
        k.scale = (1.0, 0.16, 0.06); k.rotation_euler = (0, -0.75, a)


def sikas(x, y, H, rnd):
    """sikas agaci (tarih oncesi palmiye): kalin pullu govde + tepede 10 uzun sarkik yaprak"""
    kah = (mat_m("#8a4a1a", 0.6, 0.1), mat_m("#b0602a", 0.6, 0.1))
    egr = rnd.uniform(-0.2, 0.2) * H; n = 6; p = Vector((x, y, 0))
    for i in range(n):
        t = (i + 1) / n
        q = Vector((x + egr * t * t, y, H * t))
        egik_boru(p, q, 0.16 * H * (1.05 - 0.3 * t), kah[i % 2], r2=0.14 * H * (1.0 - 0.3 * t), v=10)
        p = q
    yaprak = mat_m(rnd.choice(YAPRAK), 0.45, 0.3)
    for j in range(10):
        a = j * 0.628 + rnd.uniform(-0.12, 0.12)
        d = Vector((math.cos(a), math.sin(a), 0))
        k = kure(p + d * 0.5 * H + Vector((0, 0, -0.08 * H)), 0.55 * H, yaprak, sub=2)
        k.scale = (1.0, 0.15, 0.06); k.rotation_euler = (0, 0.45, a)


def yumurta_yuvasi(x, y, s, rnd):
    """dev dinozor yuvasi: kahve dal halkasi (basik kure halka) + 3 benekli doygun renkli yumurta"""
    dal = mat_m("#9a5a1a", 0.65, 0.05)
    for i in range(14):
        a = i * 6.283 / 14
        k = kure((x + math.cos(a) * 0.9 * s, y + math.sin(a) * 0.9 * s, 0.18 * s), 0.32 * s, dal, sub=1); k.scale = (1.2, 0.7, 0.6)
    for j in range(3):
        a = j * 2.1 + rnd.uniform(-0.2, 0.2)
        ex, ey = x + math.cos(a) * 0.35 * s, y + math.sin(a) * 0.35 * s
        renk = rnd.choice(YUMURTA)
        e = kure((ex, ey, 0.55 * s), 0.38 * s, mat_m(renk, 0.25, 0.7, ss=0.15), sub=3); e.scale = (1.0, 1.0, 1.32)
        for _ in range(5):                                    # benekler
            b = rnd.uniform(0, 6.283); h = rnd.uniform(0.35, 0.85)
            kure((ex + math.cos(b) * 0.37 * s, ey + math.sin(b) * 0.37 * s, h * s), 0.06 * s, mat_m("#ffffff", 0.3, 0.6), sub=1)


def kemik(a, b, r, mat=None):
    """fosil kemik: krem govde + iki ucta cift topuz"""
    mat = mat or mat_m("#fff0d0", 0.4, 0.5)
    a, b = Vector(a), Vector(b); d = (b - a).normalized(); yan = d.cross(Vector((0, 0, 1)))
    if yan.length < 1e-3:
        yan = Vector((1, 0, 0))
    yan.normalize()
    egik_boru(a, b, r, mat, v=12)
    for u in (a, b):
        for k in (-1, 1):
            kure(u + yan * r * 0.9 * k, r * 1.45, mat, sub=2)


def kemik_cit(x, y0, y1, H):
    """kemik cit: dikey kemik direkler + yatay kemik kiris"""
    n = max(2, int(abs(y1 - y0) / 1.6))
    for i in range(n + 1):
        y = y0 + (y1 - y0) * i / n
        kemik((x, y, 0.1), (x, y, H), 0.07)
    kemik((x, y0, H * 0.75), (x, y1, H * 0.75), 0.06)


def cicek_cali(x, y, H, rnd):
    """cicekli cali: tombul yesil kure kumesi + ustte doygun renkli buyuk cicekler"""
    for _ in range(3):
        kure((x + rnd.uniform(-0.3, 0.3) * H, y + rnd.uniform(-0.2, 0.2) * H, 0.35 * H), 0.42 * H, mat_m(rnd.choice(YAPRAK), 0.5, 0.25), sub=2)
    for _ in range(4):
        cx, cy, cz = x + rnd.uniform(-0.45, 0.45) * H, y - 0.25 * H, rnd.uniform(0.45, 0.8) * H
        renk = rnd.choice(CICEK)
        for j in range(5):
            a = j * 1.2566
            k = kure((cx + math.cos(a) * 0.1 * H, cy, cz + math.sin(a) * 0.1 * H), 0.08 * H, mat_m(renk, 0.3, 0.5), sub=1); k.scale = (1, 0.4, 1)
        kure((cx, cy - 0.03 * H, cz), 0.05 * H, mat_m("#ffd81a", 0.3, 0.5), sub=1)


def yesil_tepe(x, y, r, h, ad="tepe_cim"):
    """yumusak yesil tepe: basik dev kure, cim malzemesi"""
    k = kure((x, y, -h * 0.35), r, mat_cim(ad, acik=True), sub=3); k.scale = (1.0, 0.55, h / r)
    return k


def kaya(x, y, s, rnd):
    """yosunlu kaya kumesi: ust uste 2-3 yuvarlak sicak tas blok + tepede yosun"""
    z = 0.0
    for i in range(rnd.randint(2, 3)):
        w = s * rnd.uniform(0.8, 1.2) * (1 - i * 0.2); hh = s * rnd.uniform(0.5, 0.8)
        yuvarlak_kutu("kaya", (x + rnd.uniform(-0.2, 0.2) * s, y, z + hh / 2), (w, w * 0.8, hh), mat_m(rnd.choice((TAS, TAS_A, "#a8582a")), 0.6, 0.15), egim=0.25 * s, seg=3)
        z += hh * 0.92
    k = kure((x, y, z), s * 0.45, mat_m("#3ac81a", 0.6, 0.1), sub=2); k.scale = (1.2, 1.0, 0.35)


def mesale(x, y, H):
    """mesale: ahsap direk + ustte sicak alev (emisyon damla)"""
    silindir((x, y, 0), 0.07, H, mat_m("#6a3a0a", 0.5, 0.2), v=12)
    silindir((x, y, H), 0.14, 0.18, mat_m("#3a1a0a", 0.5, 0.2), v=12, r2=0.2)
    k = kure((x, y, H + 0.32), 0.17, mat_isik("#ff8a1a", 6.0), sub=2); k.scale = (1, 1, 1.5)
    kure((x, y, H + 0.3), 0.09, mat_isik("#ffe04a", 8.0), sub=1)


def volkan(x, y, R, H):
    """uzakta volkan: kiremit-kahve koni + tepede parlak lav agzi + lav kanallari + beyaz tombul duman"""
    silindir((x, y, -2), R, H, mat_m("#c8400a", 0.55, 0.2), v=48, r2=R * 0.22)
    silindir((x, y, H - 2.2), R * 0.24, 0.5, mat_isik("#ff5a0a", 5.0), v=32, r2=R * 0.2)
    for j in range(4):                                     # lav kanallari
        a = math.radians(-90 + (j - 1.5) * 22)
        p = Vector((x + math.cos(a) * R * 0.2, y + math.sin(a) * R * 0.2, H - 2.4))
        q = Vector((x + math.cos(a) * R * 0.55, y + math.sin(a) * R * 0.55, H * 0.45))
        egik_boru(p, q, R * 0.03, mat_isik("#ff7a1a", 3.5), r2=R * 0.015, v=8)
    rnd = random.Random(431)
    dm = mat_m("#ffffff", 0.85, 0.0)
    for i in range(9):                                     # yukari genisleyen tombul duman
        k = kure((x + rnd.uniform(-0.15, 0.25) * R * (1 + i * 0.15), y, H + R * (0.12 + i * 0.13)), R * (0.12 + i * 0.03), dm, sub=2)
        k.scale = (1.0, 0.7, 0.8)


def selale(x, y, H, W):
    """uzak kayalik + selale: sicak tas duvar, onunde parlak acik mavi su seridi + altta havuz"""
    yuvarlak_kutu("ucurum", (x, y + 4, H / 2), (W * 2.2, 8, H), mat_m(TAS, 0.6, 0.15), egim=2.0, seg=3)
    kure((x, y + 4, H), W * 1.3, mat_cim("ucurum_cim", acik=True), sub=2).scale = (1.4, 1.2, 0.25)
    kutu("selale", (x, y - 0.2, H / 2), (W, 0.3, H), mat_su(), egim=0)
    k = kure((x, y - 1.5, -0.3), W * 1.2, mat_su(), sub=3); k.scale = (1.4, 0.7, 0.08)


def pterodaktil(x, y, z, s, rnd):
    """gokte suzulen pterodaktil: turuncu govde + iki ucgen kanat + ibik"""
    renk = rnd.choice(("#ff6a1a", "#e8381a", "#9a3aff", "#1a8aff"))
    gm = mat_m(renk, 0.4, 0.4)
    g = kure((x, y, z), 0.25 * s, gm, sub=2); g.scale = (1.6, 0.6, 0.6)
    ucgen((x - 0.2 * s, y, z), (x - 1.6 * s, y + 0.2 * s, z + 0.35 * s), (x + 0.15 * s, y, z + 0.05 * s), gm)
    ucgen((x + 0.2 * s, y, z), (x + 1.6 * s, y + 0.2 * s, z + 0.35 * s), (x - 0.15 * s, y, z + 0.05 * s), gm)
    egik_boru((x + 0.38 * s, y, z + 0.05 * s), (x + 0.75 * s, y, z - 0.02 * s), 0.07 * s, gm, r2=0.01 * s, v=6)
    egik_boru((x + 0.32 * s, y, z + 0.12 * s), (x + 0.1 * s, y, z + 0.4 * s), 0.05 * s, mat_m("#ffd81a", 0.3, 0.5), r2=0.01 * s, v=6)


def bulut(x, y, z, s, rnd):
    """tombul beyaz bulut: 4-6 kure kumesi (ekran dolu, gok ust bolgesi)"""
    bm = mat_m("#ffffff", 0.8, 0.0)
    for _ in range(rnd.randint(4, 6)):
        k = kure((x + rnd.uniform(-1.4, 1.4) * s, y, z + rnd.uniform(-0.2, 0.4) * s), s * rnd.uniform(0.6, 1.0), bm, sub=2)
        k.scale = (1.0, 0.6, 0.7)


def sarmasik(a, b, n, sark=0.35):
    """iki nokta arasinda sarkan sarmasik: yesil ip + yapraklar + aralarda renkli cicek"""
    a, b = Vector(a), Vector(b); nok = []
    for i in range(n + 1):
        t = i / n; p = a.lerp(b, t); p.z -= sark * 4 * t * (1 - t); nok.append(p)
    km = mat_m("#1a8a2a", 0.5, 0.1)
    for i in range(n):
        egik_boru(nok[i], nok[i + 1], 0.025, km, v=6)
        m = (nok[i] + nok[i + 1]) / 2
        k = kure(m + Vector((0, -0.03, -0.08)), 0.14, mat_m(YAPRAK[i % len(YAPRAK)], 0.4, 0.3), sub=1); k.scale = (1, 0.3, 0.6)
        if i % 2 == 0:
            kure(m + Vector((0, -0.06, -0.18)), 0.07, mat_m(CICEK[i % len(CICEK)], 0.3, 0.5), sub=1)


# ------------------------------------------------------------------ MEKAN (her iki katmanda; serit sahnesinde uzak kisim holdout)
def mekan(serit_modu, rnd):
    _SM.clear()                                         # ikinci katmanda bos_sahne eski malzemeleri siliyor (36 dersi)
    me = bpy.data.meshes.new("yakin_zemin")
    me.from_pydata([(-60, -4, -0.02), (60, -4, -0.02), (60, GECIS, -0.02), (-60, GECIS, -0.02)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("yakin_zemin", me); bpy.context.collection.objects.link(o); o.data.materials.append(mat_cim("zemin_cim"))
    # yakin kenar: sikas + egrelti + yumurta yuvasi + kemik cit + cicekli cali + mesaleler (koridor bos; OUT camur yeri acik)
    for s in (-1, 1):
        for (x, y, k) in ((10.5, 2.0, 4.6), (14.5, 7.5, 5.8), (9.2, 10.2, 4.0), (19.5, 3.5, 6.4), (17.0, 10.8, 5.2)):
            sikas(s * x, y, k, rnd)
        for (x, y, k) in ((8.0, 0.2, 1.6), (12.2, 5.6, 2.2), (7.6, 7.2, 1.4), (16.0, 1.0, 2.0), (11.0, 10.6, 1.8)):
            egrelti(s * x, y, k, rnd)
        yumurta_yuvasi(s * 12.6, 3.6, 1.3, rnd)
        cicek_cali(s * 8.6, 3.8, 1.2, rnd); cicek_cali(s * 15.6, 8.6, 1.6, rnd)
        kemik_cit(s * (PIST + 2.6), -2.0, 8.0, 1.2)
        for y in (-1.0, 3.4, 7.6):
            mesale(s * (PIST + 1.5), y, 2.0)
    for y in (-1.0, 3.4):                                  # mesaleler arasinda sarkan sarmasik (her iki yan)
        for s in (-1, 1):
            sarmasik((s * (PIST + 1.5), y, 2.15), (s * (PIST + 1.5), y + 4.4, 2.15), 8, sark=0.25)
    for o in bpy.data.objects:
        if o.type == "MESH":
            o["yakin"] = 1
    # uzak: cim ufka kadar, iki yanda sikas/egrelti seridi, yesil tepeler, kayalar, volkan, selale
    me = bpy.data.meshes.new("cim_uzak")
    me.from_pydata([(-420, GECIS, -0.05), (420, GECIS, -0.05), (420, 520, -0.05), (-420, 520, -0.05)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("cim_uzak", me); bpy.context.collection.objects.link(o); o.data.materials.append(mat_cim("cim_uzak", acik=True))
    for s in (-1, 1):                                      # iki yan: tarih oncesi orman seridi (kapi arkasi ve orta koridor acik)
        y = GECIS + 2
        while y < 150:
            sc = 1.0 + y / 40
            x = s * rnd.uniform(11, 16) * (1 + y / 70)
            sikas(x, y, 5.0 * sc * rnd.uniform(0.8, 1.25), rnd)
            if rnd.random() < 0.5:
                egrelti(x + s * 3 * sc, y + 1 * sc, 2.0 * sc, rnd)
            if rnd.random() < 0.35:
                yesil_tepe(x + s * 5 * sc, y + 2 * sc, 3.2 * sc, 1.6 * sc)
            if rnd.random() < 0.15 and y < 90:
                yumurta_yuvasi(x + s * 7 * sc, y + 3 * sc, 1.2 * sc, rnd)
            y += 4.5 * sc
    for _ in range(60):                                    # orta mesafe yesil tepeler (ufuk dolu)
        x = rnd.uniform(-300, 300); y = rnd.uniform(140, 320)
        if abs(x) < 18 + y * 0.05:
            continue
        yesil_tepe(x, y, rnd.uniform(14, 30), rnd.uniform(5, 12))
    for _ in range(14):
        kaya(rnd.uniform(-260, 260), rnd.uniform(200, 360), rnd.uniform(8, 16), rnd)
    volkan(-150, 330, 85, 115)                             # sol uzakta tuten volkan; sahne 1: (-120, 420) tabelanin arkasinda kaldi + sisle pembe -> sola ve yakina
    selale(150, 330, 70, 9)                                # sag uzakta kayalik + selale
    for (x, y, r, h) in ((40, 470, 200, 90), (240, 420, 150, 62), (-340, 470, 170, 80), (390, 480, 170, 72)):
        yesil_tepe(x, y, r, h, ad="dev_tepe")              # dev yesil tepeler (gokun alt yarisini doldurur)
    # gok: pterodaktiller + tombul bulutlar + suzulen polen (ekran dolu)
    for _ in range(18):
        x = rnd.uniform(-34, 34); y = rnd.uniform(18, 46); z = rnd.uniform(6, 20)
        if abs(x) < 6 and z < 9:
            continue
        pterodaktil(x, y, z, rnd.uniform(0.5, 0.9) * (1 + y / 40), rnd)
    for _ in range(10):
        bulut(rnd.uniform(-60, 60), rnd.uniform(60, 110), rnd.uniform(22, 40), rnd.uniform(2.5, 4.5), rnd)
    pm = mat_isik("#d8ff4a", 2.2)                       # suzulen polen: sari-yesil, seyrek
    for _ in range(140):
        x = rnd.uniform(-30, 30); y = rnd.uniform(4, 60); z = rnd.uniform(0.8, 18)
        if abs(x) < 5 and y < 14:
            continue
        kure((x, y, z), rnd.uniform(0.03, 0.07) * (1 + y / 30), pm, sub=1)
    if serit_modu:
        for o in bpy.data.objects:
            if o.type == "MESH" and not o.get("yakin"):
                o.is_holdout = True


# ------------------------------------------------------------------ SERIT: toprak pist + dev ayak izleri + kemik korkuluk + oklar + OUT camur birikintisi
def ayak_izi(x, y, s, a):
    """uc parmakli dev dinozor ayak izi: koyu toprak oval topuk + uc parmak (zemine gomulu)"""
    km = mat_m(KUM_G, 0.7, 0.05)
    k = kure((x, y, 0.08), 0.32 * s, km, sub=2); k.scale = (1.0, 1.1, 0.12)
    for j in (-1, 0, 1):
        b = a + j * 0.45
        k = kure((x + math.sin(b) * 0.55 * s, y + math.cos(b) * 0.55 * s, 0.085), 0.2 * s, km, sub=1)
        k.scale = (0.55, 1.4, 0.1); k.rotation_euler = (0, 0, -b)


def camur(x, y, r):
    """OUT ani: parlak koyu kahve camur birikintisi + kenarinda toprak kabarti"""
    k = kure((x, y, 0.0), r, mat_m("#6a2a0a", 0.08, 0.9), sub=3); k.scale = (1.0, 1.3, 0.1)
    for j in range(10):
        a = j * 0.628
        kure((x + math.cos(a) * r, y + math.sin(a) * r * 1.3, 0.05), r * 0.22, mat_m("#9a4a1a", 0.6, 0.1), sub=1).scale = (1, 1, 0.5)


def serit_esyalari(rnd):
    kutu("pist", (0, (KAP["y"] + 0.4 - 4) / 2, 0.0), (PIST * 2, KAP["y"] + 4.4, 0.16), mat_kum("pist_toprak", acik=True, dalga=False), egim=0.04, seg=2)
    for (x, y, a) in ((-0.55, 1.6, 0.08), (0.55, 3.1, -0.08)):    # sahne 1: kadraj altinda kesilen / oka binen izler tavsan izi gibi okundu -> ortada iki adimlik iz, parmaklar kapiya
        ayak_izi(x, y, 0.85, a)
    for s in (-1, 1):                                     # pist kenari: alcak yosunlu tas bordur
        kutu("bordur", (s * (PIST + 0.2), (KAP["y"] - 3.4) / 2, 0.12), (0.45, KAP["y"] + 2.6, 0.26), mat_m(TAS, 0.55, 0.25), egim=0.08, seg=3)
        kutu("yosun", (s * (PIST + 0.2), (KAP["y"] - 3.4) / 2, 0.27), (0.42, KAP["y"] + 2.5, 0.06), mat_m("#3ac81a", 0.6, 0.1), egim=0.02, seg=2)
    for s in (-1, 1):                                     # korkuluk: kemik direkler + ustte isik + sarmasik ip
        y = -3.0; i = 0
        while y < KAP["y"] - 0.4:
            kemik((s * (PIST + 0.5), y, 0.25), (s * (PIST + 0.5), y, 0.8), 0.06)
            kure((s * (PIST + 0.5), y, 1.0), 0.1, mat_isik(AMPUL[i % len(AMPUL)], 5.0), sub=1)
            y += 1.3; i += 1
        kutu("ip", (s * (PIST + 0.5), (KAP["y"] - 3.4) / 2, 0.72), (0.05, KAP["y"] + 2.6, 0.05), mat_m("#1a8a2a", 0.6, 0.0), egim=0)
    for j, x in enumerate((-1.7, 1.7)):                   # yon oklari: sari ve camgobegi (kahve toprakta okunur)
        ok = mat_m("#ffd80a" if j == 0 else "#0ad8e8", 0.25, 0.8)
        for y in (4.6, 6.2):
            nok = [(x - 0.6, y - 0.4), (x, y), (x + 0.6, y - 0.4), (x + 0.6, y - 0.68), (x, y - 0.28), (x - 0.6, y - 0.68)]
            me = bpy.data.meshes.new("ok"); me.from_pydata([(a, b, 0.17) for a, b in nok], [], [list(range(6))]); me.update()
            o = bpy.data.objects.new("ok", me); bpy.context.collection.objects.link(o); o.data.materials.append(ok)
            o.modifiers.new("k", "SOLIDIFY").thickness = 0.02
    for s in (-1, 1) if not KDOY else ():                 # OUT ani: iki dis tarafta camur birikintisi (karakter kayar)
        camur(s * 5.8, 5.0, 1.5)


def kapi():
    """yosunlu tas kemer: iki tas blok kule + tepede dev fosil kafatasi boynuzu, kirisin ustunden kemer gibi fosil kaburgalar
    + kiris altinda sarkan sarmasik + mesale/ampul dizisi (motor ampul_p1 hatti) + LED tabela"""
    Y, W_, H_, K = KAP["y"], KAP["w"], KAP["h"], KAP["kalin"]
    xk = W_ / 2 + K / 2
    rnd = random.Random(431)
    for s in (-1, 1):
        n = 5; dh = (H_ + K + 0.2) / n
        for i in range(n):                                # tas bloklar (hafif kaydirmali) + yosun kapaklari
            yuvarlak_kutu("tas_blok", (s * xk + rnd.uniform(-0.05, 0.05), Y, i * dh + dh / 2), (K * 1.3, K * 1.3, dh * 0.94),
                          mat_m((TAS, TAS_A, "#a8582a")[i % 3], 0.55, 0.3), egim=0.07, seg=3)
            if i % 2 == 1:
                k = kure((s * xk, Y - K * 0.55, i * dh + dh * 0.9), K * 0.45, mat_m("#3ac81a", 0.6, 0.1), sub=2); k.scale = (1.3, 0.4, 0.45)
        k = kure((s * xk, Y, H_ + K + 0.25), K * 0.7, mat_m("#fff0d0", 0.4, 0.5), sub=3); k.scale = (1, 1, 0.9)   # fosil topuz
        egik_boru((s * xk, Y, H_ + K + 0.6), (s * xk * 1.15, Y, H_ + K + 1.4), 0.14, mat_m("#fff0d0", 0.35, 0.6), r2=0.02, v=12)   # boynuz
    yuvarlak_kutu("kiris", (0, Y, H_ + K / 2), (W_ + 2 * K, K + 0.1, K), mat_m(TAS, 0.55, 0.3), egim=0.12, seg=4)
    for i in range(5):                                    # kirisin ustunden kemerlenen fosil kaburgalar
        x = -W_ / 2 + 0.6 + i * (W_ - 1.2) / 4
        p = Vector((x, Y + 0.15, H_ + K))
        for j in range(4):
            q = p + Vector((0.0, 0.05, 0.32 - j * 0.04)) + Vector((0.12 * (1 if x > 0 else -1) * j * 0.3, 0, 0))
            egik_boru(p, q, 0.06 - j * 0.008, mat_m("#fff0d0", 0.4, 0.5), v=8); p = q
    for i in range(9):                                    # kiris altinda sarkan sarmasik + cicek
        x = -W_ / 2 + 0.4 + i * (W_ - 0.8) / 8
        L = rnd.uniform(0.35, 0.7)
        egik_boru((x, Y - 0.12, H_ + 0.02), (x + rnd.uniform(-0.05, 0.05), Y - 0.12, H_ + 0.02 - L), 0.03, mat_m("#1a8a2a", 0.5, 0.1), v=6)
        k = kure((x, Y - 0.15, H_ + 0.02 - L * 0.5), 0.12, mat_m(YAPRAK[i % len(YAPRAK)], 0.4, 0.3), sub=1); k.scale = (1, 0.3, 0.7)
        kure((x, Y - 0.17, H_ + 0.02 - L), 0.08, mat_m(CICEK[i % len(CICEK)], 0.3, 0.5), sub=1)
    for i in range(16):                                   # isik dizisi (motor ampul_p1 ile ayni hat)
        x = -W_ / 2 - K + i * (W_ + 2 * K) / 15
        kure((x, Y - 0.55, H_ + K * 0.4 + (i % 2) * 0.2), 0.09, mat_isik(AMPUL[i % len(AMPUL)], 6.0), sub=1)
    yuvarlak_kutu("tabela", (0, Y, H_ + K + 0.75), (W_ * 0.6, 0.2, 0.7), mat_pbr("tabela", "#2a160a", 0.35, metal=0.3), egim=0.05, seg=3)
    me = bpy.data.meshes.new("led_yuz"); a, b = W_ * 0.28, 0.28; z0 = H_ + K + 0.75
    me.from_pydata([(-a, Y - 0.11, z0 - b), (a, Y - 0.11, z0 - b), (a, Y - 0.11, z0 + b), (-a, Y - 0.11, z0 + b)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("led_yuz", me); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat_emis("led_yuz", lin(hex3("#3a1a0a")), 1.2))
    kutu("tabela_ust", (0, Y, H_ + K + 1.12), (W_ * 0.62, 0.26, 0.1), mat_m("#3ac81a", 0.4, 0.4), egim=0.05, seg=2)


def serit_katmani():
    sc = koy_sahnesi(1920, 1080, True)
    kam = kamera(sc)
    rnd = random.Random(43)
    isiklar()
    mekan(True, random.Random(43))
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
    mk = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-5.8, 5.0, 0.2), (5.8, 5.0, 0.2), (0, GECIS, 0))]
    YERLESIM["dag"] = {"yigin_sol_x": round(mk[0].x * 1920, 1), "yigin_sag_x": round(mk[1].x * 1920, 1),
                       "yigin_y": round((1 - mk[0].y) * 1080, 1), "gecis_y": round((1 - mk[2].y) * 1080, 1)}
    YERLESIM["yol"] = {"y_kapi": Y, "genislik": PIST * 2, "kam": KAM, "serit_w": 1920}
    log("aciklik", YERLESIM[ON_EK + "aciklik_p1"], YERLESIM["dag"])
    yaz(sc, ON_EK + "serit.png")


def gok_katmani(ad):
    sc = koy_sahnesi(1920, 1080, False)
    kamera(sc)
    isiklar()
    mekan(False, random.Random(43))
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
log("bitti (dino)", YERLESIM.get(ON_EK + "aciklik_p1"))
