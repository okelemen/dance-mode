"""HUMAN TETRIS 42. video (REF-094 yapi, 1v1) - GUNDUZ KORSAN GEMISI GUVERTESI, CILALI 3D OYUN GORUNUMU. varlik.py calistirir (--mod gemi).
Iskelet varlik-gokada.py (37, 1v1 iki serit): katmanlar, kamera, kapi olcusu, yerlesim anahtarlari ayni (motor 34 uyumu).

Mekan kullanici karari (28 Kas 2026, A): gunduz, acik deniz, parlak gunes. Iki pist cilali ahsap guverte tahtasindan (oyuncu renginde boyali),
uzerinde yon oklari; iki yanda halat korkuluk, toplar, ficilar, hazine sandiklari; direklerde siskin renkli yelkenler ve flamalar;
arkada turkuaz deniz, uzakta palmiyeli adacik ve baska bir yelkenli; gokte martilar ve bulutlar.
Kapi: iki ahsap direk + oyuncu renginde halat sargisi + seren + flama + fener dizisi + altin capa rozeti + tabela.
OUT ani: her seridin DIS tarafinda kupestede bosluk + disari uzanan tahta ("walk the plank"); duvar karakteri tahtadan DENIZE iter, su sicrar (motorda).
Telif (md. 16): genel korsan gemisi kalibi; bilinen film/oyun gemisi, kurukafa-kemik amblemi birebir, karakter yok. Bayrak kendi cizimimiz (kirmizi + altin capa).
prompts.chat (md. 23): yalniz "Black Sails in the Fog" (foto-gercekci, sisli) -> sis ve foto gercekcilik YOK; alinan fikir yalniz katman katman yelken (motor acilisi).
§4 CILALI 3D OYUN GORUNUMU: doygun renk, tombul hatlar, cilali yuzey, gercek isik-golge (Cycles); foto dokusu yok.
§8 SOLUK YASAK: yelkenler krem/beyaz DEGIL doygun kirmizi-sari serit, deniz doygun turkuaz, ahsap sicak bal-turuncu, gok derin mavi.

Ciktilar: gok.png, serit-p1/p2.png, panel-p1/p2.png, yerlesim.json; kapak modu (--yalniz kapak): kapak-gok.png, kapak-serit-p1/p2.png
"""
import random
YERLESIM.clear()
KAPAK = YALNIZ == "kapak"
POZLAMA = float(arg("--pozlama", arg("--kapak-pozlama", "0")))
GUNES = float(arg("--gunes", "4.6"))
ON_EK = "kapak-" if KAPAK else ""
KAP = {"y": 8.0, "w": 3.4, "h": 3.7, "kalin": 0.55}
KAM = {"z": 2.3, "egim": 5.0, "lens": 18.0, "sensor": 24.0}
if KAPAK:
    KAM.update({"z": float(arg("--kapak-z", "2.0")), "egim": float(arg("--kapak-egim", "3.0")), "lens": float(arg("--kapak-lens", "16.0"))})
YOL_YARI = 2.6
GECIS = 11.0            # serit guvertesi burada biter, otesi gok.png
DENIZ_Z = -1.7          # deniz yuzeyi (guverte z=0)
KUPESTE_X = 2.4         # seridin dis kenarindaki kupeste (lane koordinati)
TAHTA_Y = (3.7, 6.7)    # kupestedeki bosluk + disari uzanan tahta (OUT)
SERIT = {
    "p1": {"ana": "#1e8cff", "koyu": "#0a3fa8", "acik": "#8cc8ff"},
    "p2": {"ana": "#ff3aa8", "koyu": "#a8105e", "acik": "#ffa6d6"},
}
SICAK = ("#ff1e3c", "#ffd21e", "#ff7a14", "#a040ff", "#2fd04a")
AHSAP = ("#d8822a", "#e89a3a")          # bal-turuncu guverte tahtasi (bej/gri degil)
AHSAP_KOYU = "#8a3a0a"
GOVDE = "#d82a1a"                       # gemi govdesi doygun kirmizi + altin serit
ALTIN = "#ffc21a"
YELKEN = ("#ff2a3a", "#ffd21e")         # kirmizi-sari serit yelken (krem degil, §8)
DENIZ = ("#0a9ae0", "#14d0e0")
GOK = ("#18b8ff", "#0a7cff", "#0030d0")
BULUT = "#8ad8ff"
KAPAK_D = KAPAK and arg("--kapak-doygun", "0") != "0"
if KAPAK_D:                              # kapak olcumu icin derin doygun gok/deniz (2B boyama yok, md. 21)
    GOK = ("#0a90ff", "#0050f0", "#1a10b8")
    DENIZ = ("#0a7ad8", "#0ab8d8")
    BULUT = "#3aa8ff"
KD = arg("--kapak-doygun", "0") if KAPAK else "0"
if KD in ("2", "3", "4"):                # HT42 kapak tur 2 (REF-094 doygunluk 0,727 / renklilik 0,594): tahta + gok + deniz daha doygun
    AHSAP = ("#ff6a0a", "#ff8a14"); AHSAP_KOYU = "#a02a06"
    YELKEN = ("#ff1030", "#ffc800"); GOVDE = "#e0100e"
    DENIZ = ("#0050e0", "#00b8f0"); BULUT = "#2a80ff"
    GOK = ("#0a7aff", "#1a30e8", "#2a08a0")      # ufuk mavi -> tepe lacivert-mor (REF koyu tepe)
if KD == "4":                            # tur 3: gok tepesi koyu lacivert-mor (REF koyu zemin), bulut/beyaz marti yok, gunes biraz kisik
    GOK = ("#0a6aff", "#1020d0", "#18047a"); GUNES = float(arg("--gunes", "3.8"))
if KD == "3":                            # gun batimi: ufuk turuncu-pembe, tepe mor; alcak altin gunes (magenta isik yok - 41 dersi)
    GOK = ("#ff8a10", "#ff2a7a", "#4a0ab0")
    DENIZ = ("#1a40d0", "#7a30e0"); BULUT = "#ff7ab8"
    GUNES = float(arg("--gunes", "3.4"))


# ------------------------------------------------------------------ sahne / isik
def gok_sahnesi(w, h, saydam):
    sc = bos_sahne(w=w, h=h, saydam=saydam, ornek=ORNEK, doygun=True)
    sc.view_settings.view_transform = "Standard"           # 25 notu: AgX doygun renkleri pastele ceker
    sc.view_settings.exposure = POZLAMA
    sc.cycles.max_bounces = 6; sc.cycles.diffuse_bounces = 3; sc.cycles.glossy_bounces = 3
    sc.cycles.transmission_bounces = 2; sc.cycles.transparent_max_bounces = 8
    sc.cycles.use_light_tree = True
    nt = sc.world.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord"); sp = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Generated"], sp.inputs[0])
    rp = nt.nodes.new("ShaderNodeValToRGB"); el = rp.color_ramp.elements
    el[0].position = 0.0; el[0].color = (*lin(hex3(GOK[0])), 1)
    el[1].position = 0.40; el[1].color = (*lin(hex3(GOK[2])), 1)   # 30/31 dersi: koyu doygun tepe
    e2 = el.new(0.12); e2.color = (*lin(hex3(GOK[1])), 1)
    nt.links.new(sp.outputs["Z"], rp.inputs[0])
    lp = nt.nodes.new("ShaderNodeLightPath")
    bg_k = nt.nodes.new("ShaderNodeBackground"); bg_k.inputs[1].default_value = 1.0
    bg_i = nt.nodes.new("ShaderNodeBackground"); bg_i.inputs[1].default_value = 0.22
    nt.links.new(rp.outputs[0], bg_k.inputs[0]); nt.links.new(rp.outputs[0], bg_i.inputs[0])
    mx = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(lp.outputs["Is Camera Ray"], mx.inputs[0])
    nt.links.new(bg_i.outputs[0], mx.inputs[1]); nt.links.new(bg_k.outputs[0], mx.inputs[2])
    o = nt.nodes.new("ShaderNodeOutputWorld"); nt.links.new(mx.outputs[0], o.inputs[0])
    sc.use_nodes = True; sc.render.use_compositing = True; ct = sc.node_tree; ct.nodes.clear()
    rl = ct.nodes.new("CompositorNodeRLayers"); gl = ct.nodes.new("CompositorNodeGlare"); co = ct.nodes.new("CompositorNodeComposite")
    gl.glare_type = "FOG_GLOW"; gl.quality = "HIGH"; gl.threshold = 1.3; gl.size = 7; gl.mix = -1.0 if KD in ("2", "3") else 0.0   # kapakta parlama yok (38 dersi)
    ct.links.new(rl.outputs["Image"], gl.inputs[0]); ct.links.new(gl.outputs[0], co.inputs[0])
    if saydam:
        ct.links.new(rl.outputs["Alpha"], co.inputs[1])
    return sc


def kamera(sc, x=0.0):
    rx = math.radians(90 - KAM["egim"])
    bpy.ops.object.camera_add(location=(x, 0, KAM["z"]), rotation=(rx, 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.sensor_fit = "VERTICAL"; kam.data.sensor_height = KAM["sensor"]; kam.data.lens = KAM["lens"]
    kam.data.clip_end = 1500
    return kam


def isiklar():
    bpy.ops.object.light_add(type="SUN", location=(0, 0, 30))
    g = bpy.context.active_object; g.data.energy = GUNES; g.data.angle = math.radians(1.5)
    g.data.color = lin(hex3("#ffc860" if KD == "3" else "#fff3dc"))
    g.rotation_euler = Vector((-0.40, 0.55, -0.73)).to_track_quat("-Z", "Y").to_euler()


# ------------------------------------------------------------------ malzemeler
def mat_pbr(ad, renk, purluk, metal=0.0, kaplama=0.0, bump=None):
    m = bpy.data.materials.new(ad); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*lin(hex3(renk)), 1)
    b.inputs["Roughness"].default_value = purluk; b.inputs["Metallic"].default_value = metal
    b.inputs["Coat Weight"].default_value = kaplama; b.inputs["Coat Roughness"].default_value = 0.06
    if bump:
        nt = m.node_tree
        ns = nt.nodes.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value = bump[0]; ns.inputs["Detail"].default_value = 6
        bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = bump[1]; bp.inputs["Distance"].default_value = 0.02
        nt.links.new(ns.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    return m


def mat_tahta(ad, renk1, renk2, ara="#5a2a08", olcek=1.0, satir=0.18):
    """guverte tahtasi: tugla dokusuyla uzun ince tahtalar (her tahta kendi tonunda) + koyu derz + damar bump; yari mat cilali"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.inputs["Scale"].default_value = olcek; br.inputs["Mortar Size"].default_value = 0.012
    br.inputs["Brick Width"].default_value = 2.6; br.inputs["Row Height"].default_value = satir
    br.inputs["Color1"].default_value = (*lin(hex3(renk1)), 1); br.inputs["Color2"].default_value = (*lin(hex3(renk2)), 1)
    br.inputs["Mortar"].default_value = (*lin(hex3(ara)), 1)
    br.offset = 0.37; br.squash = 1.0
    nt.links.new(geo.outputs["Position"], br.inputs["Vector"])
    nt.links.new(br.outputs["Color"], b.inputs["Base Color"])
    wv = nt.nodes.new("ShaderNodeTexWave"); wv.wave_type = "BANDS"; wv.bands_direction = "X"
    wv.inputs["Scale"].default_value = 6.0; wv.inputs["Distortion"].default_value = 6.0; wv.inputs["Detail"].default_value = 3
    nt.links.new(geo.outputs["Position"], wv.inputs["Vector"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.12; bp.inputs["Distance"].default_value = 0.02
    nt.links.new(wv.outputs["Fac"], bp.inputs["Height"])
    bp2 = nt.nodes.new("ShaderNodeBump"); bp2.inputs["Strength"].default_value = 0.5; bp2.inputs["Distance"].default_value = 0.02
    nt.links.new(br.outputs["Fac"], bp2.inputs["Height"]); nt.links.new(bp.outputs["Normal"], bp2.inputs["Normal"])
    nt.links.new(bp2.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = 0.4; b.inputs["Coat Weight"].default_value = 0.3; b.inputs["Coat Roughness"].default_value = 0.12
    return m


def mat_deniz(ad="deniz"):
    """doygun turkuaz deniz: iki ton gurultu + dalga bump, cilali (gri yansima degil; emission yok)"""
    def f():
        m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
        geo = nt.nodes.new("ShaderNodeNewGeometry")
        ns = nt.nodes.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value = 0.08; ns.inputs["Detail"].default_value = 3
        nt.links.new(geo.outputs["Position"], ns.inputs["Vector"])
        rp = nt.nodes.new("ShaderNodeValToRGB")
        rp.color_ramp.elements[0].color = (*lin(hex3(DENIZ[0])), 1); rp.color_ramp.elements[1].color = (*lin(hex3(DENIZ[1])), 1)
        nt.links.new(ns.outputs["Fac"], rp.inputs[0]); nt.links.new(rp.outputs[0], b.inputs["Base Color"])
        wv = nt.nodes.new("ShaderNodeTexWave"); wv.wave_type = "BANDS"; wv.bands_direction = "Y"
        wv.inputs["Scale"].default_value = 0.35; wv.inputs["Distortion"].default_value = 8.0; wv.inputs["Detail"].default_value = 3
        nt.links.new(geo.outputs["Position"], wv.inputs["Vector"])
        bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.35; bp.inputs["Distance"].default_value = 0.05
        nt.links.new(wv.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
        b.inputs["Roughness"].default_value = 0.1; b.inputs["Coat Weight"].default_value = 0.5
        b.inputs["Specular IOR Level"].default_value = 0.25
        return m
    return M(ad, f)


def duz(ad, x0, x1, y0, y1, z, mat):
    me = bpy.data.meshes.new(ad)
    me.from_pydata([(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new(ad, me); bpy.context.collection.objects.link(o); o.data.materials.append(mat)
    return o


_MAT = {}


def M(ad, f):
    if ad not in _MAT:
        _MAT[ad] = f()
    return _MAT[ad]


def P(renk, purluk=0.3, kaplama=0.6, metal=0.0):
    return M("c" + renk + str(purluk) + str(metal), lambda: mat_pbr("c" + renk, renk, purluk, metal=metal, kaplama=kaplama))


def guverte_mat():
    return M("guverte", lambda: mat_tahta("guverte", AHSAP[0], AHSAP[1]))


def ahsap(renk=AHSAP_KOYU):
    return M("ahsap" + renk, lambda: mat_pbr("ahsap" + renk, renk, 0.5, kaplama=0.25, bump=(6, 0.2)))


def altin():
    return P(ALTIN, 0.22, 0.8, metal=0.75)


# ------------------------------------------------------------------ parcalar
def flama(x, y, z, boy, gen, renk, kenar="#ffd21e"):
    """direkten sarkan dikey flama: renkli kumas + altin kenar + uc kisminda V kesik"""
    nok = [(x - gen / 2, y, z), (x + gen / 2, y, z), (x + gen / 2, y, z - boy), (x, y, z - boy * 0.82), (x - gen / 2, y, z - boy)]
    me = bpy.data.meshes.new("flama"); me.from_pydata(nok, [], [list(range(5))]); me.update()
    o = bpy.data.objects.new("flama", me); bpy.context.collection.objects.link(o); o.data.materials.append(P(renk, 0.45, 0.3))
    o.modifiers.new("k", "SOLIDIFY").thickness = 0.04
    yuvarlak_kutu("flama_cubuk", (x, y - 0.03, z), (gen * 1.15, 0.08, 0.08), P(kenar, 0.3, 0.7), egim=0.03, seg=1)


def kus(konum, olcek, renk, rnd):
    """marti: tombul beyaz-sari govde + acik kanatlar + turuncu gaga"""
    x, y, z = konum
    g = kure((x, y, z), 0.4 * olcek, P(renk, 0.35, 0.6), sub=2); g.scale = (0.85, 1.5, 0.8)
    kure((x, y - 0.65 * olcek, z + 0.08 * olcek), 0.1 * olcek, P("#ff8a10", 0.3, 0.7), sub=2)
    k = rnd.uniform(0.3, 0.9)
    for s in (-1, 1):
        me = bpy.data.meshes.new("kanat")
        me.from_pydata([(x, y - 0.25 * olcek, z), (x + s * 1.6 * olcek, y, z + k * olcek), (x, y + 0.45 * olcek, z)], [], [[0, 1, 2]]); me.update()
        o = bpy.data.objects.new("kanat", me); bpy.context.collection.objects.link(o)
        o.data.materials.append(P(renk, 0.35, 0.5)); o.modifiers.new("k", "SOLIDIFY").thickness = 0.05 * olcek


def bulut(merkez, olcek, rnd):
    bm = M("bulut", lambda: mat_pbr("bulut", BULUT, 0.85))
    x, y, z = merkez
    for k in range(7):
        r = olcek * rnd.uniform(0.45, 0.85)
        dx = rnd.uniform(-1.5, 1.5) * olcek; dz = rnd.uniform(-0.2, 0.55) * olcek * (1 - abs(dx) / (2 * olcek))
        b = kure((x + dx, y + rnd.uniform(-0.4, 0.4) * olcek, z + dz), r, bm, sub=3); b.scale = (1.15, 0.8, 0.9)


def fener(xy, z0=0.0, boy=1.4):
    """ayakli gemi feneri: koyu ahsap direk + pirinc kafes icinde sicak isik (kendi isigi, emission serbest)"""
    x, y = xy
    boru((x, y, z0), (x, y, z0 + boy), 0.05, ahsap())
    kure((x, y, z0 + boy + 0.14), 0.15, M("fener", lambda: mat_emis("fener", lin(hex3("#ffd070")), 6.0)), sub=2)
    silindir_k((x, y, z0 + boy + 0.3), 0.12, 0.1, altin(), r2=0.02)


def silindir_k(konum, r, h, mat, v=24, r2=None):
    x, y, z = konum
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, location=(x, y, z + h / 2), vertices=v)
    else:
        bpy.ops.mesh.primitive_cone_add(radius1=r, radius2=r2, depth=h, location=(x, y, z + h / 2), vertices=v)
    o = bpy.context.active_object; o.data.materials.append(mat); bpy.ops.object.shade_smooth()
    return o


def fici(x, y, s, z0=0.0, yatik=False):
    """tombul fici: bal ahsap govde + iki altin cember"""
    if yatik:
        k = kure((x, y, z0 + 0.42 * s), 0.45 * s, ahsap("#c8682a"), sub=2); k.scale = (1.3, 0.95, 0.95)
        for dx in (-0.32, 0.32):
            bpy.ops.mesh.primitive_torus_add(major_radius=0.42 * s, minor_radius=0.04 * s, location=(x + dx * s, y, z0 + 0.42 * s), rotation=(0, math.pi / 2, 0))
            bpy.context.active_object.data.materials.append(altin()); bpy.ops.object.shade_smooth()
        return
    k = kure((x, y, z0 + 0.5 * s), 0.45 * s, ahsap("#c8682a"), sub=2); k.scale = (0.95, 0.95, 1.25)
    for dz in (0.22, 0.78):
        bpy.ops.mesh.primitive_torus_add(major_radius=0.43 * s, minor_radius=0.04 * s, location=(x, y, z0 + dz * s))
        bpy.context.active_object.data.materials.append(altin()); bpy.ops.object.shade_smooth()


def sandik(x, y, s, z0=0.0, acik=True):
    """hazine sandigi: kirmizi-kahve govde + kubbeli kapak + altin kosebent; acik olanda altin sikke yigini"""
    yuvarlak_kutu("sandik", (x, y, z0 + 0.3 * s), (0.9 * s, 0.6 * s, 0.6 * s), ahsap("#a8321a"), egim=0.05 * s, seg=2)
    for dx in (-0.38, 0.38):
        yuvarlak_kutu("kose", (x + dx * s, y, z0 + 0.3 * s), (0.09 * s, 0.62 * s, 0.62 * s), altin(), egim=0.02 * s, seg=1)
    if acik:
        for k in range(9):
            a = k * 0.7
            kure((x + math.cos(a) * 0.22 * s, y + math.sin(a) * 0.12 * s, z0 + 0.62 * s + (k % 3) * 0.06 * s), 0.12 * s, altin(), sub=1)
        kp = yuvarlak_kutu("kapak", (x, y + 0.32 * s, z0 + 0.85 * s), (0.9 * s, 0.12 * s, 0.5 * s), ahsap("#a8321a"), egim=0.04 * s, seg=2)
        kp.rotation_euler = (-0.35, 0, 0)
    else:
        k = kure((x, y, z0 + 0.6 * s), 0.45 * s, ahsap("#a8321a"), sub=2); k.scale = (1.0, 0.66, 0.4)


def top(x, y, s, yon=1, z0=0.0):
    """tombul bronz top: kirmizi kizak + iki tekerlek + altin namlu (siyah degil; doygun)"""
    yuvarlak_kutu("kizak", (x, y, z0 + 0.22 * s), (0.7 * s, 0.9 * s, 0.32 * s), P("#d82a1a", 0.45, 0.4), egim=0.06 * s, seg=2)
    for dx in (-0.36, 0.36):
        for dy in (-0.3, 0.3):
            bpy.ops.mesh.primitive_cylinder_add(radius=0.18 * s, depth=0.1 * s, location=(x + dx * s, y + dy * s, z0 + 0.18 * s), rotation=(0, math.pi / 2, 0))
            bpy.context.active_object.data.materials.append(ahsap()); bpy.ops.object.shade_smooth()
    boru((x, y - 0.1 * s, z0 + 0.5 * s), (x + yon * 1.1 * s, y + 0.1 * s, z0 + 0.62 * s), 0.2 * s, P("#e0a020", 0.25, 0.7, metal=0.8))
    kure((x + yon * 1.12 * s, y + 0.1 * s, z0 + 0.62 * s), 0.23 * s, P("#e0a020", 0.25, 0.7, metal=0.8), sub=2)


def halat_kangal(x, y, s, z0=0.0):
    for k in range(3):
        bpy.ops.mesh.primitive_torus_add(major_radius=(0.35 - k * 0.08) * s, minor_radius=0.06 * s, location=(x, y, z0 + 0.06 * s + k * 0.1 * s))
        bpy.context.active_object.data.materials.append(P("#e8b45a", 0.6, 0.1)); bpy.ops.object.shade_smooth()


def can_simidi(x, y, z, s, rot=(0, 0, 0)):
    """kirmizi-beyaz can simidi (OUT bolgesi isareti / denizde yuzen)"""
    bpy.ops.mesh.primitive_torus_add(major_radius=0.42 * s, minor_radius=0.13 * s, location=(x, y, z), rotation=rot)
    bpy.context.active_object.data.materials.append(P("#ff1e2a", 0.3, 0.7)); bpy.ops.object.shade_smooth()
    for k in range(4):
        a = k * math.pi / 2 + math.pi / 4
        o = kure((x + math.cos(a) * 0.42 * s, y + math.sin(a) * 0.42 * s, z), 0.15 * s, P("#ffe8c8", 0.3, 0.7), sub=2)
        o.scale = (1.3, 1.3, 1.0)


def yelken(cx, y, z0, gen, boy, siskin=1.2, n=6):
    """siskin serit yelken: n dikey serit (kirmizi/sari sirayla), her serit 6x8 izgara, kameraya dogru siskin (cilali kumas)"""
    for i in range(n):
        x0 = cx - gen / 2 + gen * i / n; x1 = cx - gen / 2 + gen * (i + 1) / n
        v, f = [], []
        nx, nz = 3, 8
        for kz in range(nz + 1):
            tz = kz / nz
            for kx in range(nx + 1):
                x = x0 + (x1 - x0) * kx / nx
                tx = (x - (cx - gen / 2)) / gen
                b = siskin * math.sin(math.pi * tx) * (0.35 + 0.65 * math.sin(math.pi * tz))
                v.append((x * (1 - 0.06 * tz), y - b, z0 + boy * tz))
        for kz in range(nz):
            for kx in range(nx):
                a = kz * (nx + 1) + kx
                f.append([a, a + 1, a + nx + 2, a + nx + 1])
        me = bpy.data.meshes.new("yelken"); me.from_pydata(v, [], f); me.update()
        for p in me.polygons:
            p.use_smooth = True
        o = bpy.data.objects.new("yelken", me); bpy.context.collection.objects.link(o)
        o.data.materials.append(P(YELKEN[i % 2], 0.55, 0.2)); o.modifiers.new("k", "SOLIDIFY").thickness = 0.06


def direk(x, y, boy, yelkenler, bayrak=True):
    """direk: kalin ahsap + serenler (altin uclu) + siskin serit yelkenler + gozcu sepeti + tepede kendi bayragimiz (kirmizi + altin capa)"""
    silindir_k((x, y, 0.0), 0.42, boy, ahsap("#9a4a1a"), v=20, r2=0.28)
    for (z0, gen, h) in yelkenler:
        boru((x - gen / 2 - 0.6, y - 0.4, z0 + h), (x + gen / 2 + 0.6, y - 0.4, z0 + h), 0.18, ahsap("#9a4a1a"))
        for s in (-1, 1):
            kure((x + s * (gen / 2 + 0.6), y - 0.4, z0 + h), 0.24, altin(), sub=2)
        yelken(x, y - 0.6, z0, gen, h)
    silindir_k((x, y, boy - 2.4), 1.3, 0.9, ahsap("#c8682a"), v=24)          # gozcu sepeti
    bpy.ops.mesh.primitive_torus_add(major_radius=1.3, minor_radius=0.12, location=(x, y, boy - 1.5))
    bpy.context.active_object.data.materials.append(altin()); bpy.ops.object.shade_smooth()
    if bayrak:
        boru((x, y, boy), (x, y, boy + 3.0), 0.08, ahsap())
        nok = [(x, y, boy + 2.9), (x + 3.4, y, boy + 2.6), (x + 3.0, y, boy + 1.9), (x + 3.4, y, boy + 1.2), (x, y, boy + 1.5)]
        me = bpy.data.meshes.new("bayrak"); me.from_pydata(nok, [], [list(range(5))]); me.update()
        o = bpy.data.objects.new("bayrak", me); bpy.context.collection.objects.link(o); o.data.materials.append(P("#ff1e2a", 0.45, 0.3))
        o.modifiers.new("k", "SOLIDIFY").thickness = 0.05
        kure((x + 1.5, y - 0.08, boy + 2.25), 0.32, altin(), sub=2)        # altin capa rozeti (kurukafa yok)
        boru((x + 1.5, y - 0.1, boy + 1.75), (x + 1.5, y - 0.1, boy + 2.1), 0.07, altin())


def palmiye(x, y, z0, H, rnd):
    egr = rnd.uniform(-0.3, 0.3) * H; p = Vector((x, y, z0))
    for i in range(6):
        t = (i + 1) / 6
        q = Vector((x + egr * t * t, y, z0 + H * t))
        boru(p, q, 0.08 * H * (1.05 - 0.35 * t), ahsap("#a85a1a"))
        p = q
    yap = P(rnd.choice(("#18b83a", "#0aa04a", "#3ac81a")), 0.45, 0.3)
    for j in range(7):
        a = j * 0.9 + rnd.uniform(-0.15, 0.15)
        d = Vector((math.cos(a), math.sin(a), 0))
        k = kure(p + d * 0.4 * H + Vector((0, 0, -0.05 * H)), 0.44 * H, yap, sub=2)
        k.scale = (1.0, 0.22, 0.07); k.rotation_euler = (0, 0.35, a)


def adacik(x, y, r, rnd):
    """ufukta palmiyeli adacik: altin kum + yesil tepe + palmiyeler"""
    k = kure((x, y, DENIZ_Z - r * 0.25), r, P("#ffc04a", 0.6, 0.1), sub=3); k.scale = (1.0, 0.6, 0.35)
    k = kure((x + r * 0.1, y + r * 0.1, DENIZ_Z), r * 0.55, P("#20b83a", 0.5, 0.2), sub=3); k.scale = (1.0, 0.7, 0.6)
    for j in range(rnd.randint(3, 5)):
        palmiye(x + rnd.uniform(-0.6, 0.6) * r, y + rnd.uniform(-0.2, 0.2) * r, DENIZ_Z + r * 0.12, r * rnd.uniform(0.45, 0.7), rnd)


def uzak_gemi(x, y, s, rnd):
    """uzakta baska bir yelkenli: kirmizi govde + altin serit + iki direk + serit yelkenler"""
    yuvarlak_kutu("uzak_govde", (x, y, DENIZ_Z + 0.8 * s), (2.2 * s, 7.0 * s, 1.8 * s), P(GOVDE, 0.45, 0.4), egim=0.6 * s, seg=3)
    yuvarlak_kutu("uzak_serit", (x - 1.11 * s, y, DENIZ_Z + 1.2 * s), (0.04, 6.6 * s, 0.25 * s), altin(), egim=0.02, seg=1)
    for dy in (-1.6, 1.8):
        silindir_k((x, y + dy * s, DENIZ_Z + 1.6 * s), 0.12 * s, 9 * s, ahsap("#9a4a1a"), v=12)
        yelken(x, y + dy * s - 0.2 * s, DENIZ_Z + 3.0 * s, 4.4 * s, 5.2 * s, siskin=0.6 * s, n=4)


def korkuluk(a, b, h=0.9, aralik=1.2, bant=None):
    """kupeste korkulugu: alcak ahsap duvar + babalar (altin baslik) + ustte kalin halat"""
    a, b = Vector(a), Vector(b); d = b - a; L = d.length
    n = max(1, int(L / aralik))
    for i in range(n + 1):
        p = a + d * (i / n)
        silindir_k((p.x, p.y, 0.0), 0.11, h, ahsap("#9a4a1a"), v=12)
        kure((p.x, p.y, h + 0.06), 0.14, altin(), sub=1)
        if bant:
            bpy.ops.mesh.primitive_torus_add(major_radius=0.12, minor_radius=0.04, location=(p.x, p.y, h * 0.6))
            bpy.context.active_object.data.materials.append(bant); bpy.ops.object.shade_smooth()
    boru((a.x, a.y, h), (b.x, b.y, h), 0.06, P("#e8b45a", 0.6, 0.1))
    boru((a.x, a.y, h * 0.45), (b.x, b.y, h * 0.45), 0.045, P("#e8b45a", 0.6, 0.1))


# ------------------------------------------------------------------ GEMI + DENIZ (gok katmani tamami; serit katmaninda uzak kisim holdout)
GUVERTE = [(-9.0, -4.0), (9.0, -4.0), (9.0, GECIS), (8.4, 34.0), (5.2, 56.0), (0.0, 66.0), (-5.2, 56.0), (-8.4, 34.0), (-9.0, GECIS)]


def gemi(serit_modu, rnd):
    _MAT.clear()
    duz("deniz", -1200, 1200, -60, 1500, DENIZ_Z, mat_deniz())
    # guverte (cok kenli plaka) + kirmizi govde (solidify kenari): yakin kisim yalniz gok katmaninda (serit katmani kendi guvertesini kurar)
    nok = GUVERTE if not serit_modu else [(9.0, GECIS)] + GUVERTE[3:-1] + [(-9.0, GECIS)]
    me = bpy.data.meshes.new("guverte_ust"); me.from_pydata([(x, y, 0.0) for x, y in nok], [], [list(range(len(nok)))]); me.update()
    o = bpy.data.objects.new("guverte_ust", me); bpy.context.collection.objects.link(o)
    o.data.materials.append(guverte_mat()); o.data.materials.append(P(GOVDE, 0.45, 0.4))
    sm = o.modifiers.new("govde", "SOLIDIFY"); sm.thickness = -DENIZ_Z + 0.6; sm.offset = -1.0; sm.material_offset_rim = 1; sm.material_offset = 0
    for i in range(len(nok)):                                     # altin serit (govde ust kenari) + kupeste korkulugu
        a, b = nok[i], nok[(i + 1) % len(nok)]
        if abs(a[1] - b[1]) < 0.01 and a[1] in (-4.0, GECIS):
            continue
        boru((a[0], a[1], -0.35), (b[0], b[1], -0.35), 0.12, altin())
        korkuluk((a[0] * 0.97, a[1], 0), (b[0] * 0.97, b[1], 0), h=1.0, aralik=1.6)
    # uzak guverte esyalari: toplar, ficilar, sandiklar, halat kangallari (iki yanda, orta koridor acik)
    for s in (-1, 1):
        for yy in (15.0, 22.0, 29.0):
            top(s * 7.2, yy, 1.1, yon=s)
        for (xx, yy) in ((5.6, 17.5), (6.2, 25.5), (5.0, 36.0)):
            fici(s * xx, yy, 1.1); fici(s * (xx - 0.9), yy + 0.5, 0.9)
        sandik(s * 4.6, 31.0, 1.2, acik=(s > 0))
        halat_kangal(s * 3.6, 20.0, 1.2)
        fener((s * 8.0, 40.0), 0.0, 2.2)
    # direkler: ana direk (orta) + on direk; yelkenler iki kapinin arasinda/ustunde gokyuzunu doldurur
    direk(0.0, 25.0, 30.0, ((6.0, 13.0, 7.5), (15.0, 10.5, 6.5), (23.0, 7.5, 4.5)))
    direk(0.0, 47.0, 24.0, ((5.0, 9.0, 6.0), (13.0, 7.0, 5.0)))
    for s in (-1, 1):                                              # halatlar (iskota) direk tepelerinden kupesteye
        for (my, mz, gy) in ((25.0, 28.0, 14.0), (25.0, 28.0, 32.0), (47.0, 22.0, 40.0), (47.0, 22.0, 52.0)):
            gx = s * (8.0 if gy < 45 else 5.6)
            boru((0.0, my, mz), (gx, gy, 1.0), 0.05, P("#e8b45a", 0.6, 0.1))
        for k in range(6):                                         # iskele merdiveni halatlari (enine)
            z = 3 + k * 3.6
            boru((s * 7.9 * (1 - z / 30), 14.0 + z * 0.39, z), (s * 0.4, 25.0, z), 0.03, P("#e8b45a", 0.6, 0.1))
    boru((0.0, 64.0, 1.0), (0.0, 78.0, 6.5), 0.3, ahsap("#9a4a1a"))          # cibuk (pruva)
    nok_f = [(0.0, 77.0, 6.2), (0.0, 50.0, 22.0), (0.0, 64.0, 1.6)]
    me = bpy.data.meshes.new("flok"); me.from_pydata(nok_f, [], [[0, 1, 2]]); me.update()
    o = bpy.data.objects.new("flok", me); bpy.context.collection.objects.link(o); o.data.materials.append(P(YELKEN[1], 0.55, 0.2))
    o.modifiers.new("k", "SOLIDIFY").thickness = 0.06
    for k in range(14):                                            # pruvadan direge renkli bayrak dizisi
        t = k / 13
        p = Vector((0.0, 78.0, 6.5)).lerp(Vector((0.0, 47.0, 24.0)), t)
        ucgen_b(p, SICAK[k % len(SICAK)])
    # deniz: uzakta palmiyeli adaciklar, baska yelkenli, yuzen ficilar/can simitleri, kopuk
    for (x, y, r) in ((-130, 260, 34), (150, 300, 40), (-320, 420, 60), (320, 460, 70), (-40, 520, 46), (60, 180, 16), (-70, 150, 12)):
        adacik(x, y, r, rnd)
    uzak_gemi(-95, 210, 3.2, rnd)
    uzak_gemi(120, 380, 5.0, rnd)
    for k in range(18):
        x = rnd.choice((-1, 1)) * rnd.uniform(12, 70); y = rnd.uniform(5, 140)
        if rnd.random() < 0.5:
            fici(x, y, 1.0, z0=DENIZ_Z - 0.3, yatik=True)
        else:
            can_simidi(x, y, DENIZ_Z + 0.05, 1.2)
    for k in range(70):                                            # dalga kopugu (acik camgobegi, beyaz degil)
        x = rnd.choice((-1, 1)) * rnd.uniform(10, 90); y = rnd.uniform(-5, 200)
        f_ = kure((x, y, DENIZ_Z), rnd.uniform(0.3, 0.9), M("kopuk", lambda: mat_pbr("kopuk", "#a8f0ff", 0.4, kaplama=0.4)), sub=1); f_.scale = (2.2, 0.8, 0.25)
    # gok: tombul bulutlar + marti suruleri
    for (x, y, z, o_) in () if KD == "4" else ((-260, 520, 140, 34), (240, 500, 130, 32), (-90, 640, 200, 30), (120, 660, 220, 28), (-380, 420, 60, 30), (380, 430, 70, 30),
                          (-60, 220, 70, 14), (80, 240, 80, 14)):
        bulut((x, y, z), o_, rnd)
    for k in range(0 if KD == "4" else 28):
        kus((rnd.uniform(-40, 40), rnd.uniform(26, 90), rnd.uniform(9, 32)), rnd.uniform(0.6, 1.0), rnd.choice(("#ffffff", "#ffe08a", "#fff0c0")), rnd)
    if serit_modu:
        for o in bpy.data.objects:
            if o.type == "MESH":
                o.is_holdout = True


def ucgen_b(p, renk):
    nok = [(p.x - 0.0, p.y - 0.3, p.z), (p.x, p.y + 0.3, p.z), (p.x, p.y, p.z - 0.7)]
    me = bpy.data.meshes.new("bayrakcik"); me.from_pydata(nok, [], [[0, 1, 2]]); me.update()
    o = bpy.data.objects.new("bayrakcik", me); bpy.context.collection.objects.link(o); o.data.materials.append(P(renk, 0.4, 0.4))
    o.modifiers.new("k", "SOLIDIFY").thickness = 0.04
    o.rotation_euler = (0, 0, math.pi / 2)


# ------------------------------------------------------------------ SERIT: yakin guverte + oyuncu renginde boyali tahta pist + kupeste + OUT tahtasi + deniz
def serit_esyalari(oyuncu, R, rnd):
    s_dis = -1 if oyuncu == "p1" else 1
    # yakin guverte (ic tarafa genis; dis tarafta kupestede biter) + dis tarafta deniz (serit katmaninda gorunur)
    x_dis, x_ic = s_dis * KUPESTE_X, -s_dis * 14.0
    duz("guverte_yakin", min(x_dis, x_ic), max(x_dis, x_ic), -4, GECIS, 0.0, guverte_mat())
    yuvarlak_kutu("govde_yan", (s_dis * (KUPESTE_X + 0.15), GECIS / 2 - 2, DENIZ_Z / 2 - 0.2), (0.3, GECIS + 4, -DENIZ_Z + 0.4), P(GOVDE, 0.45, 0.4), egim=0.08, seg=2)
    boru((s_dis * (KUPESTE_X + 0.32), -4, -0.3), (s_dis * (KUPESTE_X + 0.32), GECIS, -0.3), 0.1, altin())
    # sahne 1: deniz_yakin GECIS+40'a kadar uzaniyordu -> uzak kupeste direkleri / adacik (holdout) opak denizde delik acip gok.png'den
    # uyusmayan koyu benekli bloklar + yesil ada yansimasi gosterdi -> yakin deniz yalniz gecis cizgisine kadar; otesi gok.png
    duz("deniz_yakin", min(s_dis * (KUPESTE_X + 0.1), s_dis * 60), max(s_dis * (KUPESTE_X + 0.1), s_dis * 60), -6, GECIS, DENIZ_Z, mat_deniz())
    # oyuncu renginde boyali tahta pist (iki ton) + kenarda altin civili tahta bordur
    if oyuncu == "p1":
        yol = mat_tahta("serit_yol", "#0a5cff", "#1a7cff", ara="#042a7a", olcek=1.2, satir=0.2)
    else:
        yol = mat_tahta("serit_yol", "#ff0a8c", "#ff1aa0", ara="#6a0640", olcek=1.2, satir=0.2)
    duz("serit_yol", -1.6, 1.6, -4, GECIS, 0.006, yol)
    bm = M("sinir" + R["ana"], lambda: mat_pbr("sinir" + R["ana"], R["ana"], 0.15, kaplama=0.9))
    for x in (-1.75, 1.75):
        yuvarlak_kutu("bordur", (x, (KAP["y"] - 4.4) / 2, 0.08), (0.24, KAP["y"] + 3.6, 0.16), ahsap("#9a4a1a"), egim=0.05, seg=2)
        y = -3.4
        while y < KAP["y"] - 0.8:
            kure((x, y, 0.17), 0.07, altin(), sub=1)                # altin civiler
            y += 0.9
    boya = mat_pbr("ok_" + oyuncu, "#ffd21e", 0.35, kaplama=0.6)
    for y in (4.9, 6.4):                                           # yolda boyali yon oklari (seri sabiti)
        nok = [(-0.75, y - 0.45), (0, y), (0.75, y - 0.45), (0.75, y - 0.75), (0, y - 0.3), (-0.75, y - 0.75)]
        me = bpy.data.meshes.new("ok"); me.from_pydata([(a, b, 0.014) for a, b in nok], [], [list(range(6))]); me.update()
        o = bpy.data.objects.new("ok", me); bpy.context.collection.objects.link(o); o.data.materials.append(boya)
        o.modifiers.new("k", "SOLIDIFY").thickness = 0.02
    # kupeste: dis kenarda korkuluk (oyuncu renginde bant), OUT tahtasinin oldugu yerde BOSLUK
    bant = M("bant" + R["ana"], lambda: mat_pbr("bant" + R["ana"], R["ana"], 0.25, kaplama=0.9))
    korkuluk((x_dis, -4.0, 0), (x_dis, TAHTA_Y[0], 0), h=0.95, aralik=1.0, bant=bant)
    korkuluk((x_dis, TAHTA_Y[1], 0), (x_dis, GECIS, 0), h=0.95, aralik=1.0, bant=bant)
    # OUT: kupesteden disari uzanan tahta (walk the plank) + altinda denizde can simidi + kopuk halkasi
    cy = sum(TAHTA_Y) / 2
    yuvarlak_kutu("tahta", (s_dis * (KUPESTE_X + 0.9), cy, 0.06), (2.0, 0.9, 0.12), ahsap("#c8782a"), egim=0.03, seg=2)
    for dy in (-0.3, 0.3):
        kure((s_dis * (KUPESTE_X + 1.8), cy + dy, 0.13), 0.05, altin(), sub=1)
    can_simidi(s_dis * 3.4, cy + 1.6, DENIZ_Z + 0.06, 1.0)
    for k in range(10):
        a = rnd.uniform(0, 6.28)
        f_ = kure((s_dis * 2.95 + 0.9 * math.cos(a), cy + 1.2 * math.sin(a), DENIZ_Z + 0.02), rnd.uniform(0.15, 0.3),
                  M("kopuk", lambda: mat_pbr("kopuk", "#a8f0ff", 0.4, kaplama=0.4)), sub=1)
        f_.scale = (1.6, 1.0, 0.35)
    # ic taraf (hakem yeri): kucuk fenerler; ic yanda fici + halat kangali (hakemin onunu kapatmaz)
    for yy in (2.5, 7.4):
        fener((-s_dis * 2.45, yy), 0.0, 1.1)
    fici(-s_dis * 3.6, 9.6, 0.8); halat_kangal(-s_dis * 3.4, 1.0, 0.8)


def kapi(R):
    """ahsap gemi kapisi: iki tombul direk + oyuncu renginde halat sargisi + flama, ustte seren (kiris) + renkli bayrak sacagi,
    ampul dizisi, ortada altin capa rozeti, ustte sonuk LED tabela (motor PLAYER n yazar)"""
    Y, W_, H_, K = KAP["y"], KAP["w"], KAP["h"], KAP["kalin"]
    boya = mat_pbr("kapi_boya", R["ana"], 0.25, kaplama=0.9)
    xk = W_ / 2 + K / 2
    for s in (-1, 1):
        silindir_k((s * xk, Y, 0.0), K / 2 * 1.2, 0.3, ahsap("#7a3a0a"), v=24)
        silindir_k((s * xk, Y, 0.3), K / 2, H_ - 0.3, ahsap("#9a4a1a"), v=24)
        for z in (0.9, 1.25, 2.2, 2.55):
            bpy.ops.mesh.primitive_torus_add(major_radius=K / 2 + 0.02, minor_radius=0.06, location=(s * xk, Y, z))
            bpy.context.active_object.data.materials.append(boya); bpy.ops.object.shade_smooth()
        flama(s * (xk + 0.05), Y - K / 2 - 0.08, H_ - 0.1, 1.5, 0.45, R["ana"])
        kure((s * xk, Y, H_ + K + 0.15), 0.22, altin(), sub=2)
    yuvarlak_kutu("kiris", (0, Y, H_ + K / 2), (W_ + 2 * K + 0.3, K, K), ahsap("#9a4a1a"), egim=0.1, seg=3)
    yuvarlak_kutu("kiris_bant", (0, Y - K / 2 - 0.02, H_ + K / 2), (W_ + 2 * K, 0.06, 0.18), boya, egim=0.02, seg=1)
    for k in range(10):                                            # kirisin altinda renkli ucgen bayrak sacagi
        x = -W_ / 2 - K + 0.2 + k * (W_ + 2 * K - 0.4) / 9
        nok = [(x - 0.18, Y - K / 2 - 0.05, H_), (x + 0.18, Y - K / 2 - 0.05, H_), (x, Y - K / 2 - 0.05, H_ - 0.38)]
        me = bpy.data.meshes.new("sacak"); me.from_pydata(nok, [], [[0, 1, 2]]); me.update()
        o = bpy.data.objects.new("sacak", me); bpy.context.collection.objects.link(o); o.data.materials.append(P(SICAK[k % len(SICAK)], 0.4, 0.4))
        o.modifiers.new("k", "SOLIDIFY").thickness = 0.03
    kure((0, Y - K / 2 - 0.15, H_ + K / 2), 0.26, altin(), sub=2)    # altin capa rozeti
    boru((0, Y - K / 2 - 0.2, H_ + K / 2 - 0.45), (0, Y - K / 2 - 0.2, H_ + K / 2 - 0.1), 0.06, altin())
    ampul = M("ampul", lambda: mat_emis("ampul", lin(hex3("#ffe08a")), 5.0))
    for i in range(9):
        xx = -W_ / 2 + W_ * i / 8
        kure((xx, Y - K / 2 - 0.12, H_ - 0.5 - 0.12 * math.sin(math.pi * i / 8)), 0.07, ampul, sub=2)
    yuvarlak_kutu("tabela", (0, Y - 0.3, H_ + K + 1.15), (W_ * 0.85, 0.2, 0.7), mat_pbr("tabela", "#2a160a", 0.35, metal=0.3), egim=0.05, seg=3)
    me = bpy.data.meshes.new("led_yuz"); a, b = W_ * 0.4, 0.28; z0 = H_ + K + 1.15
    me.from_pydata([(-a, Y - 0.41, z0 - b), (a, Y - 0.41, z0 - b), (a, Y - 0.41, z0 + b), (-a, Y - 0.41, z0 + b)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("led_yuz", me); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat_emis("led_yuz", lin(hex3(R["koyu"])), 1.2))
    for s in (-1, 1):
        fici(s * (xk + 0.85), Y - 0.5, 0.7)


def mat_parlama_kis():
    """buyuk yuzeylerde (guverte, yol, deniz) beyaz yansima doygunlugu yiyor -> specular/coat dusuk (30/31 dersi)"""
    for m in bpy.data.materials:
        if not m.use_nodes or "Principled BSDF" not in m.node_tree.nodes:
            continue
        ad = m.name.split(".")[0]
        if ad.startswith(("guverte", "serit_yol", "bulut")):
            b = m.node_tree.nodes["Principled BSDF"]
            b.inputs["Specular IOR Level"].default_value = 0.08
            b.inputs["Coat Weight"].default_value = 0.05


def serit_katmani(oyuncu):
    R = SERIT[oyuncu]
    sc = gok_sahnesi(960, 1080, True)
    kam = kamera(sc)
    rnd = random.Random(42 + (oyuncu == "p2"))
    isiklar()
    gemi(True, random.Random(42))
    serit_esyalari(oyuncu, R, rnd)
    kapi(R)
    Y, W_, H_ = KAP["y"], KAP["w"], KAP["h"]
    ic = W_ / 2
    bpy.context.view_layer.update()
    px = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-ic, Y, 0), (ic, Y, 0), (-ic, Y, H_), (ic, Y, H_))]
    xs = [p.x * 960 for p in px]; ys = [(1 - p.y) * 1080 for p in px]
    YERLESIM["aciklik_" + oyuncu] = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
    # OUT ani: tahtanin ucu / denizin ekrandaki yeri; motor anahtar duzeni korunur (minder = tahta ucu + deniz)
    cy = sum(TAHTA_Y) / 2
    mk = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-2.95, cy, 0.1), (2.95, cy, 0.1), (0, GECIS, 0), (-2.95, cy, DENIZ_Z), (2.95, cy, DENIZ_Z))]
    d = {"minder_sol_x": round(mk[0].x * 960, 1), "minder_sag_x": round(mk[1].x * 960, 1),
         "minder_y": round((1 - mk[0].y) * 1080, 1), "gecis_y": round((1 - mk[2].y) * 1080, 1),
         "deniz_y": round((1 - mk[3].y) * 1080, 1)}
    for on in ("salon_", "plaj_", "orman_", "lale_", "buzul_", "arena_", "gokada_", "gemi_"):
        YERLESIM[on + oyuncu] = d
    YERLESIM["yol"] = {"y_kapi": Y, "genislik": YOL_YARI * 2, "kam": KAM, "serit_w": 960}
    log("aciklik", oyuncu, YERLESIM["aciklik_" + oyuncu], d)
    mat_parlama_kis()
    yaz(sc, ON_EK + "serit-%s.png" % oyuncu)


def gok_katmani(ad):
    sc = gok_sahnesi(1920, 1080, False)
    kamera(sc)
    isiklar()
    gemi(False, random.Random(42))
    mat_parlama_kis()
    yaz(sc, ad)


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
log("bitti (gemi)", YERLESIM.get("aciklik_p1"), YERLESIM.get("aciklik_p2"))
