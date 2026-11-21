"""HUMAN TETRIS 37. video (REF-089 yapi, 1v1) - GUNDUZ UCAN GOKYUZU ADALARI, CILALI 3D OYUN GORUNUMU. varlik.py calistirir (--mod gokada).
Iskelet varlik-arena.py (33, 1v1 iki serit): katmanlar, kamera, kapi olcusu, yerlesim anahtarlari ayni (motor 30 uyumu).

Mekan kullanici karari (21 Kas 2026, A): ucan adalar, adalardan dokulen selaleler, altta ve uzakta bulut denizi, kus suruleri,
gokkusagi, tombul kumulusler. OUT ani: karakter pistin dis yanindaki tombul BULUT YATAGINA duser, seker.
Onceki mekanlardan farki: 35 balon festivalinde bulut ustu pist + balonlar vardi -> burada balon yok; yesil ucan adalar,
kaya govdeler, selaleler, tas kopru, gok kapisi (kemer) belirleyici. 31 ucurtma / 30 balon / 33 flama zinciri tekrar edilmez.
§4 CILALI 3D OYUN GORUNUMU: doygun renk, tombul hatlar, cilali yuzey, gercek isik-golge (Cycles); foto dokusu yok.
§8 SOLUK YASAK: bulut beyaz DEGIL doygun gok mavisi + pembe vurgu, cimen doygun yesil, kaya sicak turuncu/mor, gok koyu doygun tepe.
Telif (md. 16): genel ucan ada kalibi; bilinen film/oyun adalarinin tasarimi birebir alinmaz; yazi, logo, marka yok.

Ciktilar: gok.png, serit-p1/p2.png, panel-p1/p2.png, yerlesim.json; kapak modu (--yalniz kapak): kapak-gok.png, kapak-serit-p1/p2.png
"""
import random
YERLESIM.clear()
KAPAK = YALNIZ == "kapak"
POZLAMA = float(arg("--pozlama", arg("--kapak-pozlama", "0")))
GUNES = float(arg("--gunes", "4.8"))
ON_EK = "kapak-" if KAPAK else ""
KAP = {"y": 8.0, "w": 3.4, "h": 3.7, "kalin": 0.55}
KAM = {"z": 2.3, "egim": 5.0, "lens": 18.0, "sensor": 24.0}
if KAPAK:
    KAM.update({"z": float(arg("--kapak-z", "2.0")), "egim": float(arg("--kapak-egim", "3.0")), "lens": float(arg("--kapak-lens", "16.0"))})
YOL_YARI = 2.6
GECIS = 11.0            # serit tas yolu burada biter, otesi gok.png
BULUT_Z = -26.0         # bulut denizi yuksekligi (yakin ada kenarinin altinda)
KEMER_Y = 58.0          # yolun ucunda gok kapisi
SERIT = {
    "p1": {"ana": "#1e8cff", "koyu": "#0a3fa8", "acik": "#8cc8ff"},
    "p2": {"ana": "#ff3aa8", "koyu": "#a8105e", "acik": "#ffa6d6"},
}
SICAK = ("#ff1e3c", "#ffd21e", "#ff7a14", "#a040ff", "#ff3ab4", "#2fd04a", "#1e8cff")
CIMEN = ("#18c82a", "#4ae83a")
TAC = ("#20c850", "#14a83a", "#ff6ab8", "#7ae83a", "#ffb21e")
KAYA = ("#ff7a2a", "#e85a1a", "#a040ff", "#ff9a3a")
SU = "#18b8ff"
BULUT = "#78d4ff"
BULUT_P = "#ffa0dc"
TAS_YOL = ("#e8641e", "#f0842a")
TAS = ("#e8641e", "#f0842a", "#d84a1a", "#ffa63a")


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
    el[0].position = 0.0; el[0].color = (*lin(hex3("#18b8ff")), 1)
    el[1].position = 0.40; el[1].color = (*lin(hex3("#0030d0")), 1)   # 30/31 dersi: koyu doygun tepe
    e2 = el.new(0.12); e2.color = (*lin(hex3("#0a7cff")), 1)
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
    gl.glare_type = "FOG_GLOW"; gl.quality = "HIGH"; gl.threshold = 1.3; gl.size = 7; gl.mix = 0.0
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
    g.data.color = lin(hex3("#fff3dc"))
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



def mat_tas_doseme(ad, renk1, renk2, ara="#6a2008", olcek=1.0, satir=0.5):
    """tas dosemeli yol: tugla dokusuyla kare taslar, her tas kendi tonunda + koyu derz + hafif kabarik bump; yari mat"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.inputs["Scale"].default_value = olcek; br.inputs["Mortar Size"].default_value = 0.022
    br.inputs["Brick Width"].default_value = 1.0; br.inputs["Row Height"].default_value = satir
    br.inputs["Color1"].default_value = (*lin(hex3(renk1)), 1); br.inputs["Color2"].default_value = (*lin(hex3(renk2)), 1)
    br.inputs["Mortar"].default_value = (*lin(hex3(ara)), 1)
    br.offset = 0.5; br.squash = 1.0
    nt.links.new(geo.outputs["Position"], br.inputs["Vector"])
    nt.links.new(br.outputs["Color"], b.inputs["Base Color"])
    ns = nt.nodes.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value = 4.0; ns.inputs["Detail"].default_value = 4
    nt.links.new(geo.outputs["Position"], ns.inputs["Vector"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.15; bp.inputs["Distance"].default_value = 0.02
    nt.links.new(ns.outputs["Fac"], bp.inputs["Height"])
    bp2 = nt.nodes.new("ShaderNodeBump"); bp2.inputs["Strength"].default_value = 0.6; bp2.inputs["Distance"].default_value = 0.03
    nt.links.new(br.outputs["Fac"], bp2.inputs["Height"]); nt.links.new(bp.outputs["Normal"], bp2.inputs["Normal"])
    nt.links.new(bp2.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = 0.45; b.inputs["Coat Weight"].default_value = 0.2; b.inputs["Coat Roughness"].default_value = 0.1
    return m




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


def P(renk, purluk=0.3, kaplama=0.6):
    return M("c" + renk + str(purluk), lambda: mat_pbr("c" + renk, renk, purluk, kaplama=kaplama))


def tas(renk):
    return M("tas" + renk, lambda: mat_pbr("tas" + renk, renk, 0.55, kaplama=0.15, bump=(3, 0.25)))



# ------------------------------------------------------------------ yapi parcalari
def sutun(xy, boy, renk, r=0.5, z0=0.0):
    """tombul sutun: taban + yivli govde (silindir) + baslik; terrakota/altin"""
    x, y = xy
    m = tas(renk); bas = P("#ffd21e", 0.3, 0.6)
    yuvarlak_kutu("sutun_taban", (x, y, z0 + r * 0.3), (r * 2.6, r * 2.6, r * 0.6), m, egim=r * 0.15, seg=2)
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=boy, location=(x, y, z0 + r * 0.6 + boy / 2), vertices=24)
    o = bpy.context.active_object; o.data.materials.append(m); bpy.ops.object.shade_smooth()
    yuvarlak_kutu("sutun_bas", (x, y, z0 + r * 0.6 + boy + r * 0.3), (r * 2.8, r * 2.8, r * 0.6), bas, egim=r * 0.15, seg=2)
    return z0 + r * 1.2 + boy


def flama(x, y, z, boy, gen, renk, kenar="#ffd21e"):
    """sutundan/duvardan sarkan dikey flama: renkli kumas + altin kenar + uc kisminda V kesik"""
    nok = [(x - gen / 2, y, z), (x + gen / 2, y, z), (x + gen / 2, y, z - boy), (x, y, z - boy * 0.82), (x - gen / 2, y, z - boy)]
    me = bpy.data.meshes.new("flama"); me.from_pydata(nok, [], [list(range(5))]); me.update()
    o = bpy.data.objects.new("flama", me); bpy.context.collection.objects.link(o); o.data.materials.append(P(renk, 0.45, 0.3))
    o.modifiers.new("k", "SOLIDIFY").thickness = 0.04
    yuvarlak_kutu("flama_cubuk", (x, y - 0.03, z), (gen * 1.15, 0.08, 0.08), P(kenar, 0.3, 0.7), egim=0.03, seg=1)
    kure((x, y - 0.06, z - boy * 0.45), gen * 0.16, P(kenar, 0.3, 0.7), sub=2)


def kemer(cx, y, gen, boy, renk, kalin=1.2):
    """yuvarlak kemer: iki ayak + yarim halka (torus yarisi) + kilit tasi"""
    m = tas(renk)
    for s in (-1, 1):
        yuvarlak_kutu("kemer_ayak", (cx + s * (gen / 2 + kalin / 2), y, boy / 2), (kalin, kalin, boy), m, egim=0.15, seg=2)
    bpy.ops.mesh.primitive_torus_add(major_radius=gen / 2 + kalin / 2, minor_radius=kalin / 2, location=(cx, y, boy),
                                     rotation=(math.pi / 2, 0, 0), major_segments=40, minor_segments=12)
    t_ = bpy.context.active_object; t_.data.materials.append(m); bpy.ops.object.shade_smooth()
    bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="DESELECT"); bpy.ops.object.mode_set(mode="OBJECT")
    for v in t_.data.vertices:
        v.select = v.co.y < -0.01                      # (yerel y = dunya -z, donusten once) alt yari silinir
    bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.delete(type="VERT"); bpy.ops.object.mode_set(mode="OBJECT")
    yuvarlak_kutu("kilit", (cx, y - kalin * 0.1, boy + gen / 2 + kalin * 0.6), (kalin * 0.8, kalin * 1.1, kalin * 1.1), P("#ffd21e", 0.3, 0.7), egim=0.1, seg=2)



def kus(konum, olcek, renk, rnd):
    """guvercin: tombul govde + acik kanatlar + turuncu gaga"""
    x, y, z = konum
    g = kure((x, y, z), 0.4 * olcek, M("kus" + renk, lambda: mat_pbr("kus" + renk, renk, 0.35, kaplama=0.6)), sub=2); g.scale = (0.85, 1.5, 0.8)
    kure((x, y - 0.65 * olcek, z + 0.08 * olcek), 0.1 * olcek, P("#ff8a10", 0.3, 0.7), sub=2)
    k = rnd.uniform(0.3, 0.9)
    for s in (-1, 1):
        me = bpy.data.meshes.new("kanat")
        me.from_pydata([(x, y - 0.25 * olcek, z), (x + s * 1.6 * olcek, y, z + k * olcek), (x, y + 0.45 * olcek, z)], [], [[0, 1, 2]]); me.update()
        o = bpy.data.objects.new("kanat", me); bpy.context.collection.objects.link(o)
        o.data.materials.append(M("kanat" + renk, lambda: mat_pbr("kanat" + renk, renk, 0.35, kaplama=0.5))); o.modifiers.new("k", "SOLIDIFY").thickness = 0.05 * olcek


def bulut(merkez, olcek, rnd):
    beyaz = M("bulut", lambda: mat_pbr("bulut", "#7ad0ff", 0.85))
    x, y, z = merkez
    for k in range(7):
        r = olcek * rnd.uniform(0.45, 0.85)
        dx = rnd.uniform(-1.5, 1.5) * olcek; dz = rnd.uniform(-0.2, 0.55) * olcek * (1 - abs(dx) / (2 * olcek))
        b = kure((x + dx, y + rnd.uniform(-0.4, 0.4) * olcek, z + dz), r, beyaz, sub=3); b.scale = (1.15, 0.8, 0.9)



def mat_cimen(ad, renk1, renk2, olcek=0.6):
    """doygun cimen: iki ton gurultu + ince cimen bump; yari mat (beyaz parlama yok)"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    ns = nt.nodes.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value = olcek; ns.inputs["Detail"].default_value = 4
    nt.links.new(geo.outputs["Position"], ns.inputs["Vector"])
    rp = nt.nodes.new("ShaderNodeValToRGB")
    rp.color_ramp.elements[0].color = (*lin(hex3(renk1)), 1); rp.color_ramp.elements[1].color = (*lin(hex3(renk2)), 1)
    nt.links.new(ns.outputs["Fac"], rp.inputs[0]); nt.links.new(rp.outputs[0], b.inputs["Base Color"])
    n2 = nt.nodes.new("ShaderNodeTexNoise"); n2.inputs["Scale"].default_value = 40.0; n2.inputs["Detail"].default_value = 2
    nt.links.new(geo.outputs["Position"], n2.inputs["Vector"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.35; bp.inputs["Distance"].default_value = 0.02
    nt.links.new(n2.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = 0.7; b.inputs["Specular IOR Level"].default_value = 0.1
    return m


def cimen_mat():
    return M("cimen", lambda: mat_cimen("cimen", CIMEN[0], CIMEN[1]))


def kaya_mat(renk):
    return M("kaya" + renk, lambda: mat_pbr("kaya" + renk, renk, 0.55, kaplama=0.15, bump=(1.5, 0.45)))


def su_mat():
    """selale suyu: doygun camgobegi-mavi, cilali, akis cizgisi bump (emission degil; kendi isigi yok)"""
    def f():
        m = bpy.data.materials.new("su"); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
        b.inputs["Roughness"].default_value = 0.12; b.inputs["Coat Weight"].default_value = 0.8
        geo = nt.nodes.new("ShaderNodeNewGeometry"); wv = nt.nodes.new("ShaderNodeTexWave")
        wv.wave_type = "BANDS"; wv.bands_direction = "X"; wv.inputs["Scale"].default_value = 1.4; wv.inputs["Distortion"].default_value = 3.0
        wv.inputs["Detail"].default_value = 4
        nt.links.new(geo.outputs["Position"], wv.inputs["Vector"])
        # sahne 1: duz mavi serit direk gibi okundu -> dikey akis cizgileri RENKTE (koyu mavi / acik camgobegi)
        rp = nt.nodes.new("ShaderNodeValToRGB"); rp.color_ramp.elements[0].color = (*lin(hex3(SU)), 1)
        rp.color_ramp.elements[1].color = (*lin(hex3("#8af0ff")), 1); rp.color_ramp.elements[1].position = 0.85
        nt.links.new(wv.outputs["Fac"], rp.inputs[0]); nt.links.new(rp.outputs[0], b.inputs["Base Color"])
        bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.5
        nt.links.new(wv.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
        return m
    return M("su", f)


def bulut_mat():
    return M("bulutm", lambda: mat_pbr("bulutm", BULUT, 0.85))


def bulut_pembe():
    return M("bulutp", lambda: mat_pbr("bulutp", BULUT_P, 0.85))


def agac(xy, boy, z0, rnd):
    """tombul agac: kahve govde + 3-4 kure tac (doygun yesil / pembe ciceklenmis)"""
    x, y = xy
    boru((x, y, z0), (x, y, z0 + boy * 0.55), boy * 0.07, P("#a8501a", 0.6, 0.1))
    renk = rnd.choice(TAC)
    for k in range(rnd.randint(3, 4)):
        kure((x + rnd.uniform(-0.25, 0.25) * boy, y + rnd.uniform(-0.2, 0.2) * boy, z0 + boy * rnd.uniform(0.6, 0.85)),
             boy * rnd.uniform(0.22, 0.32), P(renk, 0.45, 0.35), sub=2)


def cicek(xy, z0, renk, r=0.12):
    x, y = xy
    kure((x, y, z0 + r * 0.6), r, P(renk, 0.3, 0.6), sub=1)


def selale(x, y, z_ust, boy, gen):
    """adanin kenarindan dokulen su seridi (asagi genisler) + altinda su sisi bulutu"""
    me = bpy.data.meshes.new("selale")
    v, f = [], []
    n = 8
    for i in range(n + 1):
        t = i / n
        zz = z_ust - boy * t
        v += [(x - gen / 2 * (1 + 0.4 * t), y - 0.2 * t, zz), (x + gen / 2 * (1 + 0.4 * t), y - 0.2 * t, zz)]
    for i in range(n):
        f.append([2 * i, 2 * i + 1, 2 * i + 3, 2 * i + 2])
    me.from_pydata(v, [], f); me.update()
    o = bpy.data.objects.new("selale", me); bpy.context.collection.objects.link(o); o.data.materials.append(su_mat())
    o.modifiers.new("k", "SOLIDIFY").thickness = 0.15
    for k in range(4):
        kure((x + (k - 1.5) * gen * 0.4, y, z_ust - boy), gen * 0.45, bulut_mat(), sub=2).scale = (1.2, 0.9, 0.7)
    for k in range(3):                                     # sahne 1: ustte kopuk yok, direk gibiydi -> agizda su kabarcigi kumesi
        kure((x + (k - 1) * gen * 0.35, y - 0.1, z_ust + 0.05), gen * 0.28, M("kopuk", lambda: mat_pbr("kopuk", "#a8f4ff", 0.3, kaplama=0.6)), sub=2).scale = (1.2, 0.8, 0.6)


def ada(merkez, r, rnd, agac_n=4, su=True, kaya=None):
    """ucan ada: asagi bakan tombul kaya konisi (katman halkalari) + ustte cimen kapak + agaclar, cicekler + kenardan selale"""
    x, y, z = merkez
    kaya = kaya or rnd.choice(KAYA)
    bpy.ops.mesh.primitive_cone_add(radius1=r, radius2=0.05 * r, depth=r * 1.5, location=(x, y, z - r * 0.75), rotation=(math.pi, 0, 0), vertices=28)
    o = bpy.context.active_object; o.data.materials.append(kaya_mat(kaya)); bpy.ops.object.shade_smooth()
    for k in range(3):                                     # kaya katman halkalari (tombul, farkli ton)
        kk = kure((x, y, z - r * (0.25 + 0.3 * k)), r * (0.85 - 0.25 * k), kaya_mat(KAYA[(KAYA.index(kaya) + k + 1) % len(KAYA)]), sub=2)
        kk.scale = (1.0, 1.0, 0.35)
    bpy.ops.mesh.primitive_cylinder_add(radius=r * 1.04, depth=r * 0.18, location=(x, y, z), vertices=32)
    c = bpy.context.active_object; c.data.materials.append(cimen_mat()); bpy.ops.object.shade_smooth()
    for k in range(agac_n):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(0, 0.7) * r
        agac((x + d * math.cos(a), y + d * math.sin(a)), rnd.uniform(0.35, 0.6) * r, z + r * 0.09, rnd)
    for k in range(int(6 + r)):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(0, 0.95) * r
        cicek((x + d * math.cos(a), y + d * math.sin(a)), z + r * 0.09, rnd.choice(SICAK), r=0.06 * r)
    if su:
        a = rnd.choice((-0.6, 0.6, -1.2, 1.2)) - math.pi / 2       # kameraya bakan kenar
        selale(x + r * math.cos(a), y + r * math.sin(a), z + r * 0.05, r * rnd.uniform(1.6, 2.6), r * 0.34)   # sahne 1: ince serit direk gibi -> genis


def gokkusagi(cx, y, R0, z0):
    """gokte genis gokkusagi: 6 renkli yay seridi (yarim halka mesh), mat; emission degil"""
    for i, renk in enumerate(("#ff2a3a", "#ff8a10", "#ffd21e", "#2fd04a", "#1e8cff", "#a040ff")):
        r0 = R0 - i * R0 * 0.045; r1 = r0 - R0 * 0.045
        v, f = [], []
        n = 60
        for k in range(n + 1):
            a = math.pi * k / n
            v += [(cx + math.cos(a) * r0, y, z0 + math.sin(a) * r0), (cx + math.cos(a) * r1, y, z0 + math.sin(a) * r1)]
        for k in range(n):
            f.append([2 * k, 2 * k + 2, 2 * k + 3, 2 * k + 1])
        me = bpy.data.meshes.new("gk"); me.from_pydata(v, [], f); me.update()
        o = bpy.data.objects.new("gk", me); bpy.context.collection.objects.link(o); o.data.materials.append(P(renk, 0.5, 0.0))


def fener(xy, z0=0.0, boy=1.4):
    """ayakli fener: altin direk + sicak isikli kure (kendi isigi, emission serbest)"""
    x, y = xy
    boru((x, y, z0), (x, y, z0 + boy), 0.05, P("#c88a1a", 0.3, 0.6))
    kure((x, y, z0 + boy + 0.12), 0.16, M("fener", lambda: mat_emis("fener", lin(hex3("#ffd88a")), 6.0)), sub=2)


def kopru(y0, y1, gen=5.2):
    """uzak tas kopru: tas doseme + iki yanda tas babalar + ahsap tirabzan + fenerler; altinda sarkan kaya"""
    yol = mat_tas_doseme("tas_yol", TAS_YOL[0], TAS_YOL[1], ara="#5a2a0a")
    duz("tas_yol_uzak", -gen / 2, gen / 2, y0, y1, 0.006, yol)
    yuvarlak_kutu("kopru_govde", (0, (y0 + y1) / 2, -0.7), (gen + 0.4, y1 - y0, 1.4), kaya_mat(KAYA[0]), egim=0.2, seg=2)
    y = y0 + 1.0
    k = 0
    while y < y1 - 1:
        for s in (-1, 1):
            yuvarlak_kutu("baba", (s * (gen / 2 + 0.1), y, 0.45), (0.45, 0.45, 0.9), tas(TAS[k % len(TAS)]), egim=0.12, seg=2)
            if k % 2 == 0:
                fener((s * (gen / 2 + 0.1), y), 0.9, 1.0)
        y += 3.0; k += 1
    for s in (-1, 1):
        yuvarlak_kutu("tirabzan", (s * (gen / 2 + 0.1), (y0 + y1) / 2, 0.95), (0.18, y1 - y0, 0.18), P("#c8641a", 0.5, 0.2), egim=0.05, seg=1)
    for yy in range(int(y0) + 6, int(y1), 12):
        k_ = kure((0, yy, -2.0), 2.2, kaya_mat(KAYA[1]), sub=2); k_.scale = (1.4, 1.0, 1.1)


def bulut_denizi(rnd):
    """adalarin altinda ufka kadar bulut denizi: taban + dev yassi kure kumeleri (doygun gok mavisi + pembe vurgu, beyaz yok)"""
    duz("bulut_tabani", -900, 900, GECIS - 6, 1400, BULUT_Z, bulut_mat())
    for k in range(220):
        x = rnd.uniform(-420, 420); y = rnd.uniform(GECIS + 4, 900)
        r = rnd.uniform(6, 22) * (1 + y / 500)
        b = kure((x, y, BULUT_Z + r * 0.15), r, bulut_mat() if rnd.random() < 0.7 else bulut_pembe(), sub=2); b.scale = (1.5, 1.0, 0.45)


def gok_ogeleri(rnd):
    """ekran dolu kurali (md. 7): uzakta gokkusagi, her seviyede ucan adalar (yakin-orta-uzak, gokte asili), kus suruleri,
    kucuk ucan kaya parcalari, tombul kumulusler. 30 balon / 31 ucurtma / 35 balon tekrar edilmez."""
    gokkusagi(-40, 700, 330, BULUT_Z)
    for (x, y, z, o) in ((-260, 520, 150, 34), (240, 500, 140, 32), (-90, 640, 210, 30), (120, 660, 230, 28), (-380, 420, 60, 30), (380, 430, 70, 30)):
        bulut((x, y, z), o, rnd)
    for (x, y, z, r) in ((-24, 40, 6, 7), (26, 46, 9, 8), (-46, 70, 16, 10), (48, 76, 20, 11), (-16, 95, 30, 7), (18, 100, 34, 6),
                         (-80, 120, 10, 15), (82, 130, 14, 15), (-34, 150, 44, 9), (40, 160, 50, 10), (-120, 220, 30, 22), (130, 230, 36, 22),
                         (0, 210, 62, 12), (-60, 260, 80, 14), (70, 270, 86, 14), (-160, 320, 60, 26), (170, 330, 70, 26),
                         (-12, 24, 14, 3.2), (14, 28, 17, 3.0), (-30, 30, 22, 3.6), (32, 34, 24, 3.8)):
        ada((x, y, z), r, rnd, agac_n=int(2 + r / 3))
    for k in range(26):
        kus((rnd.uniform(-40, 40), rnd.uniform(30, 90), rnd.uniform(8, 30)), rnd.uniform(0.6, 1.0), rnd.choice(("#ffffff", "#ffe08a", "#ffb8d8")), rnd)
    for k in range(60):                                    # kucuk ucan kaya parcalari
        p = kure((rnd.uniform(-22, 22), rnd.uniform(14, 40), rnd.uniform(2.5, 14.0)), rnd.uniform(0.12, 0.3), kaya_mat(rnd.choice(KAYA)), sub=1)
        p.scale = (1.3, 1.0, 0.8)
    for k in range(50):                                    # ucusan cicek yapraklari (cilali)
        p = kure((rnd.uniform(-16, 16), rnd.uniform(10, 30), rnd.uniform(1.5, 9.0)), rnd.uniform(0.07, 0.12),
                 P(rnd.choice(("#ff3aa8", "#ffd21e", "#2fd04a")), 0.3, 0.8), sub=1)
        p.scale = (1.6, 0.3, 1.0); p.rotation_euler = (rnd.uniform(0, 3), rnd.uniform(0, 3), rnd.uniform(0, 3))


def gok_kapisi(rnd):
    """yolun ucunda buyuk ucan adada gok kapisi: tas kemer + cicek sarmasigi + iki yanda selale; kemerin ustunde altin kure"""
    y = KEMER_Y
    ada((0, y + 4, 0.0), 16, rnd, agac_n=6, su=False, kaya=KAYA[2])
    kemer(0, y, 8.0, 10.0, "#f0842a", kalin=2.6)
    for s in (-1, 1):
        sutun((s * 7.5, y - 1.0), 9.0, "#ffa63a", r=0.8)
        flama(s * 7.5, y - 1.9, 9.6, 4.6, 1.8, ("#1e8cff", "#ff3aa8")[(s + 1) // 2])
        selale(s * 15.5, y - 6, 0.0, 26, 3.4)
    kure((0, y, 17.2), 1.5, P("#ffd21e", 0.2, 0.9), sub=3)
    for k in range(26):
        a = math.pi * k / 25
        cicek((math.cos(a) * 5.4, y - 1.4), 10.0 + math.sin(a) * 5.4 - 0.12, SICAK[k % len(SICAK)], r=0.32)


# ------------------------------------------------------------------ GOK ADALARI (iki katmanda; serit sahnesinde uzak kisim holdout)
def adalar(serit_modu, rnd):
    _MAT.clear()
    duz("zemin_yakin", -34, 34, -4, GECIS, 0, cimen_mat())    # yakin ada ustu (iki seridin cimen tabani)
    yuvarlak_kutu("yakin_ada_kaya", (0, GECIS / 2, -2.4), (68, GECIS + 4, 4.6), kaya_mat(KAYA[0]), egim=1.2, seg=3)
    for s in (-1, 1):                                       # yakin adanin kenarlarindan selaleler (kadrajin iki yaninda)
        selale(s * 33.5, 2.0, 0.0, 30, 4.0)
        selale(s * 30.0, GECIS - 0.5, 0.0, 34, 3.2)
    bulut_denizi(rnd)
    kopru(GECIS, KEMER_Y - 6)
    gok_kapisi(rnd)
    gok_ogeleri(rnd)
    for k in range(40):                                     # yakin ada ustunde cicekli calilar (yol disinda)
        x = rnd.choice((-1, 1)) * rnd.uniform(6.5, 30); y = rnd.uniform(-2, GECIS - 1)
        c_ = kure((x, y, 0.1), rnd.uniform(0.4, 0.9), P(rnd.choice(TAC), 0.45, 0.35), sub=2); c_.scale = (1.3, 1.0, 0.7)
        for j in range(3):
            cicek((x + rnd.uniform(-0.6, 0.6), y + rnd.uniform(-0.5, 0.5)), 0.35, rnd.choice(SICAK), r=0.14)
    for k in range(6):
        agac((rnd.choice((-1, 1)) * rnd.uniform(12, 30), rnd.uniform(4, GECIS)), rnd.uniform(3.0, 5.0), 0.0, rnd)
    if serit_modu:
        for o in bpy.data.objects:
            if o.type == "MESH" and o.name.split(".")[0] not in ("zemin_yakin",):
                o.is_holdout = True


# ------------------------------------------------------------------ SERIT: oyuncu tas yolu + kristal sinir + OUT bulut yatagi + kapi
def serit_esyalari(oyuncu, R, rnd):
    s_dis = -1 if oyuncu == "p1" else 1
    if oyuncu == "p1":
        yol = mat_tas_doseme("serit_yol", "#0a5cff", "#1a7cff", ara="#042a7a")
    else:
        yol = mat_tas_doseme("serit_yol", "#ff0a8c", "#ff14a0", ara="#6a0640")
    duz("serit_yol", -1.6, 1.6, -4, GECIS, 0.006, yol)
    bm = M("sinir" + R["ana"], lambda: mat_pbr("sinir" + R["ana"], R["ana"], 0.15, kaplama=0.9))
    for x in (-1.75, 1.75):                                # serit siniri: oyuncu renginde cilali kristal tas bloklar
        y = -3.6
        while y < KAP["y"] - 0.8:
            yuvarlak_kutu("sinir", (x, y, 0.16), (0.34, 0.62, 0.32), bm, egim=0.08, seg=2)
            y += 0.75
    boya = mat_pbr("ok_" + oyuncu, "#ffd21e", 0.35, kaplama=0.6)
    for y in (4.9, 6.4):                                   # yolda boyali yon oklari (seri sabiti)
        nok = [(-0.75, y - 0.45), (0, y), (0.75, y - 0.45), (0.75, y - 0.75), (0, y - 0.3), (-0.75, y - 0.75)]
        me = bpy.data.meshes.new("ok"); me.from_pydata([(a, b, 0.014) for a, b in nok], [], [list(range(6))]); me.update()
        o = bpy.data.objects.new("ok", me); bpy.context.collection.objects.link(o); o.data.materials.append(boya)
        o.modifiers.new("k", "SOLIDIFY").thickness = 0.02
    # OUT ani: dis tarafta tombul BULUT YATAGI (karakter buraya duser, seker)
    cx, cy = s_dis * 2.95, 5.2
    y_ = kure((cx, cy, 0.25), 1.0, bulut_mat(), sub=3); y_.scale = (1.3, 1.9, 0.6)
    for k in range(10):
        a = rnd.uniform(0, 6.28)
        t_ = kure((cx + 1.3 * math.cos(a), cy + 1.9 * math.sin(a), 0.3), rnd.uniform(0.35, 0.6),
                  bulut_mat() if k % 3 else bulut_pembe(), sub=2); t_.scale = (1.2, 1.1, 0.75)
    for k in range(5):                                     # dis tarafta cicekli calilar
        x = s_dis * rnd.uniform(4.8, 9.0); y = rnd.uniform(0.5, 10.0)
        c_ = kure((x, y, 0.1), rnd.uniform(0.4, 0.7), P(rnd.choice(TAC), 0.45, 0.35), sub=2); c_.scale = (1.3, 1.0, 0.7)
        for j in range(3):
            cicek((x + rnd.uniform(-0.5, 0.5), y + rnd.uniform(-0.4, 0.4)), 0.3, rnd.choice(SICAK), r=0.12)
    agac((s_dis * 6.5, 9.5), 2.6, 0.0, rnd)
    for yy in (2.5, 7.4):                                  # ic tarafta (hakem yeri) kucuk fenerler
        fener((-s_dis * 2.45, yy), 0.0, 1.1)


def kapi(R):
    """cicekli tas kapi: iki tombul sutun + sarili cicekler, oyuncu renginde bant + flama, ustte kiris + cimen sacak,
    ampul dizisi, ustte sonuk LED tabela (motor PLAYER n yazar)"""
    Y, W_, H_, K = KAP["y"], KAP["w"], KAP["h"], KAP["kalin"]
    boya = mat_pbr("kapi_boya", R["ana"], 0.25, kaplama=0.9)
    xk = W_ / 2 + K / 2
    for s in (-1, 1):
        sutun((s * xk, Y), H_ - K * 0.6, "#f0842a", r=K / 2)
        for z in (1.1, 2.3):
            bpy.ops.mesh.primitive_torus_add(major_radius=K / 2 + 0.02, minor_radius=0.07, location=(s * xk, Y, z))
            bpy.context.active_object.data.materials.append(boya); bpy.ops.object.shade_smooth()
        flama(s * (xk + 0.05), Y - K / 2 - 0.08, H_ - 0.1, 1.5, 0.45, R["ana"])
        for k in range(7):
            cicek((s * (xk + 0.28 * math.cos(k)), Y - 0.28), 0.3 + k * 0.45, SICAK[k % len(SICAK)], r=0.1)
    yuvarlak_kutu("kiris", (0, Y, H_ + K / 2), (W_ + 2 * K + 0.3, K, K), tas("#ffa63a"), egim=0.1, seg=3)
    yuvarlak_kutu("kiris_bant", (0, Y - K / 2 - 0.02, H_ + K / 2), (W_ + 2 * K, 0.06, 0.18), boya, egim=0.02, seg=1)
    for k in range(9):
        kure((-W_ / 2 - K + (W_ + 2 * K) * k / 8, Y - 0.1, H_ + K + 0.05), 0.22, P(TAC[k % len(TAC)], 0.45, 0.35), sub=1).scale = (1.3, 1.0, 0.6)
    ampul = M("ampul", lambda: mat_emis("ampul", lin(hex3("#ffe08a")), 5.0))
    for i in range(9):
        xx = -W_ / 2 + W_ * i / 8
        kure((xx, Y - K / 2 - 0.12, H_ - 0.35 - 0.12 * math.sin(math.pi * i / 8)), 0.07, ampul, sub=2)
    yuvarlak_kutu("tabela", (0, Y - 0.3, H_ + K + 1.15), (W_ * 0.85, 0.2, 0.7), mat_pbr("tabela", "#15171a", 0.35, metal=0.4), egim=0.05, seg=3)
    me = bpy.data.meshes.new("led_yuz"); a, b = W_ * 0.4, 0.28; z0 = H_ + K + 1.15
    me.from_pydata([(-a, Y - 0.41, z0 - b), (a, Y - 0.41, z0 - b), (a, Y - 0.41, z0 + b), (-a, Y - 0.41, z0 + b)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("led_yuz", me); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat_emis("led_yuz", lin(hex3(R["koyu"])), 1.2))
    for s in (-1, 1):
        c_ = kure((s * (xk + 0.75), Y - 0.5, 0.2), 0.45, P(TAC[(s + 1) // 2], 0.45, 0.35), sub=2); c_.scale = (1.3, 1.0, 0.8)


def mat_parlama_kis():
    """buyuk yuzeylerde (cimen, yol, bulut, kaya) beyaz yansima doygunlugu yiyor -> specular/coat dusuk (30/31 dersi)"""
    for m in bpy.data.materials:
        if not m.use_nodes or "Principled BSDF" not in m.node_tree.nodes:
            continue
        ad = m.name.split(".")[0]
        if ad.startswith(("cimen", "tas_yol", "serit_yol", "tas#", "bulut", "kaya")):
            b = m.node_tree.nodes["Principled BSDF"]
            b.inputs["Specular IOR Level"].default_value = 0.06
            b.inputs["Coat Weight"].default_value = 0.0
            if ad.startswith(("tas_yol", "serit_yol")):
                b.inputs["Roughness"].default_value = 0.5


def serit_katmani(oyuncu):
    R = SERIT[oyuncu]
    sc = gok_sahnesi(960, 1080, True)
    kam = kamera(sc)
    rnd = random.Random(37 + (oyuncu == "p2"))
    isiklar()
    adalar(True, random.Random(37))
    serit_esyalari(oyuncu, R, rnd)
    kapi(R)
    Y, W_, H_ = KAP["y"], KAP["w"], KAP["h"]
    ic = W_ / 2
    bpy.context.view_layer.update()
    px = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-ic, Y, 0), (ic, Y, 0), (-ic, Y, H_), (ic, Y, H_))]
    xs = [p.x * 960 for p in px]; ys = [(1 - p.y) * 1080 for p in px]
    YERLESIM["aciklik_" + oyuncu] = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
    # OUT ani: bulut yataginin ekrandaki yeri; motor anahtar duzeni korunur (minder = bulut yatagi)
    mk = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-2.95, 5.2, 0.4), (2.95, 5.2, 0.4), (0, GECIS, 0))]
    d = {"minder_sol_x": round(mk[0].x * 960, 1), "minder_sag_x": round(mk[1].x * 960, 1),
         "minder_y": round((1 - mk[0].y) * 1080, 1), "gecis_y": round((1 - mk[2].y) * 1080, 1)}
    for on in ("salon_", "plaj_", "orman_", "lale_", "buzul_", "arena_", "gokada_"):
        YERLESIM[on + oyuncu] = d
    YERLESIM["yol"] = {"y_kapi": Y, "genislik": YOL_YARI * 2, "kam": KAM, "serit_w": 960}
    log("aciklik", oyuncu, YERLESIM["aciklik_" + oyuncu], d)
    mat_parlama_kis()
    yaz(sc, ON_EK + "serit-%s.png" % oyuncu)


def gok_katmani(ad):
    sc = gok_sahnesi(1920, 1080, False)
    kamera(sc)
    isiklar()
    adalar(False, random.Random(37))
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
log("bitti (gokada)", YERLESIM.get("aciklik_p1"), YERLESIM.get("aciklik_p2"))

