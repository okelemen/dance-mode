"""HUMAN TETRIS 31. video (REF-083 yapi, 1v1) - GUNDUZ KUTUP BUZUL KIYISI, CILALI 3D OYUN GORUNUMU. varlik.py calistirir (--mod buzul).

Mekan kullanici karari (17 Kas 2026): kutup buzul kiyisi; OUT ani: karakter buzlu suya kayar (dis tarafta acik su deligi).
27 (karli dag zirvesi: dag, cam, teleferik) ile ayni olmasin: dag/cam/teleferik YOK; turkuaz deniz, yuzen buz kutleleri,
buzul duvari, penguen kolonileri, renkli arastirma kulubeleri, kirmizi-beyaz deniz feneri, balina, renkli ucurtmalar.
§4 CILALI 3D OYUN GORUNUMU: canli doygun renk, tombul hatlar, cilali yuzey, gercek isik-golge-parlama (Cycles); foto dokusu yok,
isiksiz duz renk (emission) yuzey yok (ampul/LED/fener haric). Gok dolu (Masaustu md. 7): ucurtmalar, marti suruleri, kucuk bulutlar.
§8 SOLUK YASAK: REF-083 kapagi doygunluk 0,675 / renklilik 0,526 - buz beyaz DEGIL doygun camgobegi/turkuaz, kar mavi tonlu,
buyuk beyaz yuzey yok; sicak renkler (turuncu/kirmizi/sari kulube, fener, ucurtma, sandal, saman yerine renkli samandira) dengeler.

Katmanlar lale (30) ile ayni (motor 27 uyumu): gok.png = deniz + buzul + gok, serit-p1/p2.png = oyuncunun yakin buz yolu + serit
esyalari + kapi. Isik iki katmanda ayni olsun diye butun sahne serit katmaninda da kurulur, uzak kisim holdout.
Telif: genel kutup ogeleri; bilinen film/oyun penguenleri, yazi, logo, marka yok.

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
GECIS = 11.0            # serit buz yolu burada biter, otesi gok.png
FENER_Y = 54.0          # yolun ucunda buz kutlesi ustunde kirmizi-beyaz deniz feneri
KIYI_Y = 30.0           # buz rafinin bittigi kiyi; otesi deniz (yol iskele olarak devam eder)
SERIT = {
    "p1": {"ana": "#1e8cff", "koyu": "#0a3fa8", "acik": "#8cc8ff"},
    "p2": {"ana": "#ff3aa8", "koyu": "#a8105e", "acik": "#ffa6d6"},
}
SICAK = ("#ff1e3c", "#ffd21e", "#ff7a14", "#a040ff", "#ff3ab4", "#2fd04a")
BUZ = ("#08b8ff", "#0a8cff", "#00d0f0", "#1a6cff")


# ------------------------------------------------------------------ sahne / isik
def buzul_sahnesi(w, h, saydam):
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
    el[0].position = 0.0; el[0].color = (*lin(hex3("#10c4ff")), 1)
    el[1].position = 0.40; el[1].color = (*lin(hex3("#0030d0")), 1)   # 30'un dersi: koyu doygun tepe (parlaklik + soluk)
    e2 = el.new(0.12); e2.color = (*lin(hex3("#0a86ff")), 1)
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


def mat_buz_blok(ad, renk1, renk2, ara="#0a5aa8", olcek=1.0, satir=0.5):
    """buz bloklarindan yol: tugla dokusuyla kare bloklar, her blok kendi camgobegi tonunda + koyu mavi derz + catlak bump; cilali"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.inputs["Scale"].default_value = olcek; br.inputs["Mortar Size"].default_value = 0.018
    br.inputs["Brick Width"].default_value = 1.1; br.inputs["Row Height"].default_value = satir
    br.inputs["Color1"].default_value = (*lin(hex3(renk1)), 1); br.inputs["Color2"].default_value = (*lin(hex3(renk2)), 1)
    br.inputs["Mortar"].default_value = (*lin(hex3(ara)), 1)
    br.offset = 0.5; br.squash = 1.0
    nt.links.new(geo.outputs["Position"], br.inputs["Vector"])
    nt.links.new(br.outputs["Color"], b.inputs["Base Color"])
    vo = nt.nodes.new("ShaderNodeTexVoronoi"); vo.feature = "DISTANCE_TO_EDGE"; vo.inputs["Scale"].default_value = 3.0
    nt.links.new(geo.outputs["Position"], vo.inputs["Vector"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.2; bp.inputs["Distance"].default_value = 0.02
    nt.links.new(vo.outputs["Distance"], bp.inputs["Height"])
    bp2 = nt.nodes.new("ShaderNodeBump"); bp2.inputs["Strength"].default_value = 0.6; bp2.inputs["Distance"].default_value = 0.03
    nt.links.new(br.outputs["Fac"], bp2.inputs["Height"]); nt.links.new(bp.outputs["Normal"], bp2.inputs["Normal"])
    nt.links.new(bp2.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = 0.2; b.inputs["Coat Weight"].default_value = 0.5; b.inputs["Coat Roughness"].default_value = 0.05
    return m


def mat_su(ad, renk_yakin, renk_uzak, olcek=0.25):
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    ns = nt.nodes.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value = olcek; ns.inputs["Detail"].default_value = 2
    nt.links.new(geo.outputs["Position"], ns.inputs["Vector"])
    rp = nt.nodes.new("ShaderNodeValToRGB")
    rp.color_ramp.elements[0].color = (*lin(hex3(renk_yakin)), 1); rp.color_ramp.elements[1].color = (*lin(hex3(renk_uzak)), 1)
    nt.links.new(ns.outputs["Fac"], rp.inputs[0]); nt.links.new(rp.outputs[0], b.inputs["Base Color"])
    bn = nt.nodes.new("ShaderNodeTexNoise"); bn.inputs["Scale"].default_value = 2.5; bn.inputs["Detail"].default_value = 5
    nt.links.new(geo.outputs["Position"], bn.inputs["Vector"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.3; bp.inputs["Distance"].default_value = 0.05
    nt.links.new(bn.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = 0.12; b.inputs["Specular IOR Level"].default_value = 0.15
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


def buz_mat(renk):
    return M("buz" + renk, lambda: mat_pbr("buz" + renk, renk, 0.12, kaplama=0.7, bump=(2.5, 0.15)))


def buz_kutlesi(konum, boyut, renk, rnd, kar=True):
    """kose koseli (duz golgeli) buz kutlesi: ico kure + rastgele olcek; ustunde mavi tonlu kar sapkasi"""
    x, y, z = konum
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1.0, location=(x, y, z))
    o = bpy.context.active_object
    for v in o.data.vertices:
        v.co *= rnd.uniform(0.82, 1.12)
    o.scale = boyut
    o.data.materials.append(buz_mat(renk))
    if kar:
        k = kure((x, y, z + boyut[2] * 0.72), 1.0, M("kar", lambda: mat_pbr("kar", "#5ad0ff", 0.45, kaplama=0.2, bump=(6, 0.2))), sub=2)
        k.scale = (boyut[0] * 0.8, boyut[1] * 0.8, boyut[2] * 0.3)
    return o


# ------------------------------------------------------------------ penguen (sablon + bagli kopya)
_SABLON = {}


def penguen_sablon():
    """tombul penguen (kameraya donuk): siyah yumurta govde, beyaz gogus, siyah bas, beyaz goz lekeleri, sari yanak,
    turuncu gaga + ayaklar, iki kisa kanat; tek nesne, sahne disi"""
    if "p" in _SABLON:
        return _SABLON["p"]
    siyah = M("pg_siyah", lambda: mat_pbr("pg_siyah", "#141a2e", 0.3, kaplama=0.7))
    beyaz = M("pg_beyaz", lambda: mat_pbr("pg_beyaz", "#f4f8ff", 0.35, kaplama=0.5))
    turuncu = M("pg_tur", lambda: mat_pbr("pg_tur", "#ff8a10", 0.3, kaplama=0.7))
    sari = M("pg_sari", lambda: mat_pbr("pg_sari", "#ffd21e", 0.3, kaplama=0.6))
    parca = []
    g = kure((0, 0, 0.42), 0.3, siyah, sub=3); g.scale = (1.0, 0.9, 1.35); parca.append(g)
    gg = kure((0, -0.12, 0.38), 0.24, beyaz, sub=3); gg.scale = (0.95, 0.7, 1.3); parca.append(gg)
    parca.append(kure((0, 0, 0.92), 0.2, siyah, sub=3))
    for s in (-1, 1):
        parca.append(kure((s * 0.08, -0.15, 0.95), 0.06, beyaz, sub=2))
        parca.append(kure((s * 0.08, -0.2, 0.95), 0.028, siyah, sub=2))
        parca.append(kure((s * 0.14, -0.1, 0.88), 0.05, sari, sub=2))
        k = kure((s * 0.3, 0, 0.5), 0.1, siyah, sub=2); k.scale = (0.4, 0.6, 2.0); k.rotation_euler = (0, s * 0.35, 0); parca.append(k)
        a = kure((s * 0.1, -0.12, 0.03), 0.07, turuncu, sub=2); a.scale = (1.0, 1.6, 0.35); parca.append(a)
    gb = kure((0, -0.22, 0.88), 0.05, turuncu, sub=2); gb.scale = (1.0, 1.6, 0.6); parca.append(gb)
    bpy.ops.object.select_all(action="DESELECT")
    for p in parca:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parca[0]
    bpy.ops.object.join()
    o = bpy.context.active_object; o.name = "penguen_sablon"
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    bpy.context.collection.objects.unlink(o)
    _SABLON["p"] = o
    return o


def penguen(konum, olcek, rnd, don=0.0):
    s = penguen_sablon()
    o = s.copy(); o.data = s.data
    bpy.context.collection.objects.link(o)
    o.location = konum; o.scale = (olcek, olcek, olcek * rnd.uniform(0.92, 1.08))
    o.rotation_euler = (0, rnd.uniform(-0.06, 0.06), don + rnd.uniform(-0.5, 0.5))
    return o


# ------------------------------------------------------------------ KUTUP KIYISI (iki katmanda; serit sahnesinde uzak kisim holdout)
def kiyi(serit_modu, rnd):
    _MAT.clear(); _SABLON.clear()
    raf = mat_pbr("buz_raf", "#0a9cff", 0.25, kaplama=0.4, bump=(3, 0.2))          # buz rafi: doygun camgobegi-mavi (17 Kas kapak 1: acik camgobegi soluk + parlak cikti)
    duz("zemin_yakin", -80, 80, -4, GECIS, 0, raf)
    duz("zemin_uzak", -80, 80, GECIS, KIYI_Y, 0, raf)
    deniz = mat_su("deniz", "#00c8e8", "#0068e0", olcek=0.08)
    duz("deniz", -600, 600, KIYI_Y - 0.5, 900, -0.25, deniz)
    for s in (-1, 1):                                                       # raf disinda da deniz (yanlarda)
        duz("deniz_yan", s * 80, s * 600, -4, KIYI_Y, -0.25, deniz)
    for x in (-80, 80):
        yuvarlak_kutu("raf_kenar", (x, (KIYI_Y - 4) / 2, -0.15), (1.2, KIYI_Y + 4, 0.5), raf, egim=0.3, seg=2)
    yuvarlak_kutu("raf_kenar", (0, KIYI_Y, -0.15), (161, 1.2, 0.5), raf, egim=0.3, seg=2)
    yol = mat_buz_blok("buz_yol", "#0a7cff", "#12a4ff", ara="#04307a")
    duz("buz_yol_uzak", -2.6, 2.6, GECIS, KIYI_Y, 0.006, yol)
    iskele(rnd)
    # raf ustunde: kar tumsekleri (mavi tonlu), penguen kolonileri, renkli arastirma kulubeleri, samandira ve kizaklar
    for k in range(40):
        x = rnd.choice((-1, 1)) * rnd.uniform(5.5, 70); y = rnd.uniform(GECIS + 1, KIYI_Y - 2)
        t_ = kure((x, y, -0.3), rnd.uniform(0.8, 2.2), M("kar", lambda: mat_pbr("kar", "#5ad0ff", 0.45, kaplama=0.2, bump=(6, 0.2))), sub=2)
        t_.scale = (1.6, 1.0, 0.45)
    for (cx, cy, n) in ((-9, 16, 14), (11, 19, 16), (-22, 24, 18), (26, 14, 12), (-38, 18, 14), (40, 25, 16)):
        for k in range(n):
            penguen((cx + rnd.uniform(-3, 3), cy + rnd.uniform(-2.2, 2.2), 0), rnd.uniform(0.9, 1.25), rnd)
    for k, (x, y) in enumerate(((-15, 27), (18, 27.5), (-30, 21), (32, 20), (-52, 26), (55, 23))):
        kulube((x, y), rnd.uniform(1.6, 2.1), SICAK[k % 4])
    # denizde: buz kutleleri, penguenli buz parcalari, balina, renkli sandallar
    for k in range(26):
        x = rnd.choice((-1, 1)) * rnd.uniform(8, 160); y = rnd.uniform(KIYI_Y + 6, 240)
        r = rnd.uniform(2.5, 9.0)
        buz_kutlesi((x, y, r * 0.15), (r * rnd.uniform(1.0, 1.6), r * rnd.uniform(0.7, 1.1), r * rnd.uniform(0.5, 1.1)), rnd.choice(BUZ), rnd)
    for k in range(10):
        x = rnd.choice((-1, 1)) * rnd.uniform(6, 45); y = rnd.uniform(KIYI_Y + 4, 70)
        p_ = buz_kutlesi((x, y, -0.15), (rnd.uniform(2.0, 3.2), rnd.uniform(1.2, 2.0), 0.35), rnd.choice(BUZ), rnd, kar=False)
        for j in range(rnd.randint(2, 4)):
            penguen((x + rnd.uniform(-1.2, 1.2), y + rnd.uniform(-0.5, 0.5), 0.15), 1.0, rnd)
    balina((-34, 95, -0.2), 5.0)
    for k, (x, y) in enumerate(((-14, 46), (20, 52), (-48, 64), (52, 74))):
        sandal((x, y), 1.4, SICAK[(k + 1) % len(SICAK)])
    fener_kule((0, FENER_Y, 0), 16.0, rnd)
    buzul(rnd)
    gok_ogeleri(rnd)
    if serit_modu:
        for o in bpy.data.objects:
            if o.type == "MESH" and o.name.split(".")[0] not in ("zemin_yakin",):
                o.is_holdout = True


def iskele(rnd):
    """kiyidan fener kutlesine uzanan iskele: buz yolu devam eder, iki yanda oyuncu renginde halat babalari"""
    yol = M("iskele", lambda: mat_buz_blok("iskele", "#0a7cff", "#12a4ff", ara="#04307a"))
    yuvarlak_kutu("iskele", (0, (KIYI_Y + FENER_Y - 6) / 2, -0.05), (5.4, FENER_Y - 6 - KIYI_Y, 0.3), yol, egim=0.08, seg=2)
    for s, R in ((-1, SERIT["p1"]), (1, SERIT["p2"])):
        bm = M("baba" + R["ana"], lambda r_=R["ana"]: mat_pbr("baba" + r_, r_, 0.3, kaplama=0.7))
        y = KIYI_Y + 1
        while y < FENER_Y - 6:
            boru((s * 2.75, y, -0.2), (s * 2.75, y, 0.9), 0.12, bm)
            kure((s * 2.75, y, 0.95), 0.16, bm, sub=2)
            y += 3.0


def kulube(xy, boy, renk):
    """tombul arastirma kulubesi: renkli kutu govde, mavi tonlu kar catili, beyaz pencere cercevesi + sari yanan pencere, kapi"""
    x, y = xy
    gov = M("kul" + renk, lambda: mat_pbr("kul" + renk, renk, 0.35, kaplama=0.5))
    yuvarlak_kutu("kulube", (x, y, boy * 0.45), (boy * 1.6, boy * 1.1, boy * 0.9), gov, egim=boy * 0.08, seg=3)
    c = kure((x, y, boy * 0.9), boy * 0.95, M("kar", lambda: mat_pbr("kar", "#5ad0ff", 0.45, kaplama=0.2, bump=(6, 0.2))), sub=2)
    c.scale = (1.0, 0.7, 0.4)
    pen = M("pen_isik", lambda: mat_emis("pen_isik", lin(hex3("#ffd27a")), 3.0))
    for dx in (-0.4, 0.4):
        yuvarlak_kutu("pen", (x + dx * boy, y - boy * 0.56, boy * 0.5), (boy * 0.3, 0.05, boy * 0.28), pen, egim=0.02, seg=1)
    yuvarlak_kutu("kapi", (x, y - boy * 0.56, boy * 0.28), (boy * 0.28, 0.06, boy * 0.52), M("kul_kapi", lambda: mat_pbr("kul_kapi", "#1a3a8a", 0.4, kaplama=0.4)), egim=0.02, seg=1)
    boru((x + boy * 0.6, y, boy * 0.9), (x + boy * 0.6, y, boy * 2.0), 0.05, M("bayrak_d", lambda: mat_pbr("bayrak_d", "#e8eef8", 0.3, metal=0.5)))
    yuvarlak_kutu("bayrak", (x + boy * 0.85, y, boy * 1.8), (boy * 0.5, 0.04, boy * 0.3), M("bayrak" + renk, lambda: mat_pbr("bayrak" + renk, SICAK[(SICAK.index(renk) + 1) % len(SICAK)], 0.4, kaplama=0.4)), egim=0.02, seg=1)


def sandal(xy, olcek, renk):
    x, y = xy
    g = kure((x, y, -0.1), olcek, M("san" + renk, lambda: mat_pbr("san" + renk, renk, 0.3, kaplama=0.7)), sub=3)
    g.scale = (0.7, 1.8, 0.4)
    kure((x, y, 0.15), olcek * 0.62, M("san_ic", lambda: mat_pbr("san_ic", "#fff2d8", 0.4, kaplama=0.3)), sub=2).scale = (0.6, 1.6, 0.2)


def balina(konum, olcek):
    """yuzen balina sirti + kuyruk + puskurme (beyaz-mavi su tanecikleri)"""
    x, y, z = konum
    gm = M("balina", lambda: mat_pbr("balina", "#2050c8", 0.25, kaplama=0.8))
    s_ = kure((x, y, z), olcek, gm, sub=3); s_.scale = (0.8, 2.2, 0.45)
    for s in (-1, 1):
        k = kure((x + s * olcek * 0.5, y + olcek * 2.6, z + olcek * 0.9), olcek * 0.45, gm, sub=2); k.scale = (1.4, 0.25, 0.5)
        k.rotation_euler = (0, s * 0.4, 0)
    boru((x, y + olcek * 2.0, z), (x, y + olcek * 2.5, z + olcek * 0.8), olcek * 0.18, gm)
    su = M("puskur", lambda: mat_pbr("puskur", "#bff2ff", 0.2, kaplama=0.5))
    for k in range(9):
        a = k * 0.7
        kure((x + math.cos(a) * olcek * 0.3, y - olcek * 0.8, z + olcek * (1.0 + 0.25 * k)), olcek * 0.22, su, sub=2)


def fener_kule(taban, boy, rnd):
    """kirmizi-beyaz seritli tombul deniz feneri, buz kutlesi ustunde: konik govde, balkon korkulugu, cam fener odasi
    (kendi isigi - emission serbest), kirmizi kubbe"""
    x, y, z = taban
    buz_kutlesi((x, y, -0.5), (9.0, 7.0, 2.6), "#38d4ff", rnd)
    kirmizi = M("fen_kirmizi", lambda: mat_pbr("fen_kirmizi", "#ff1e3c", 0.3, kaplama=0.6))
    beyaz = M("fen_beyaz", lambda: mat_pbr("fen_beyaz", "#fff6ea", 0.35, kaplama=0.5))
    h = boy * 0.7; n = 5
    for i in range(n):
        z0 = 1.6 + h * i / n; r0 = boy * (0.17 - 0.05 * i / n); r1 = boy * (0.17 - 0.05 * (i + 1) / n)
        bpy.ops.mesh.primitive_cone_add(radius1=r0, radius2=r1, depth=h / n, location=(x, y, z0 + h / n / 2), vertices=32)
        o = bpy.context.active_object; o.data.materials.append(kirmizi if i % 2 == 0 else beyaz); bpy.ops.object.shade_smooth()
    zt = 1.6 + h
    bpy.ops.mesh.primitive_cylinder_add(radius=boy * 0.16, depth=boy * 0.04, location=(x, y, zt), vertices=32)
    bpy.context.active_object.data.materials.append(beyaz); bpy.ops.object.shade_smooth()
    oda = M("fen_isik", lambda: mat_emis("fen_isik", lin(hex3("#ffe88a")), 6.0))
    bpy.ops.mesh.primitive_cylinder_add(radius=boy * 0.09, depth=boy * 0.12, location=(x, y, zt + boy * 0.08), vertices=24)
    bpy.context.active_object.data.materials.append(oda)
    k = kure((x, y, zt + boy * 0.15), boy * 0.11, kirmizi, sub=3); k.scale = (1.0, 1.0, 0.7)
    for i in range(12):
        a = i * math.pi / 6
        boru((x + math.cos(a) * boy * 0.15, y + math.sin(a) * boy * 0.15, zt), (x + math.cos(a) * boy * 0.15, y + math.sin(a) * boy * 0.15, zt + boy * 0.04),
             boy * 0.006, M("fen_kor", lambda: mat_pbr("fen_kor", "#1a2a5a", 0.3, metal=0.6)))


def buzul(_rnd=None):
    """ufukta buzul duvari: kose koseli turkuaz-mavi kutleler (dikey yarikli), arkada mavi tonlu karli sirtlar (dag/cam yok)"""
    rnd = random.Random(31)
    for k in range(30):
        x = -330 + k * 23 + rnd.uniform(-6, 6)
        if abs(x) < 14:
            continue
        h = rnd.uniform(18, 34)
        buz_kutlesi((x, rnd.uniform(270, 300), h * 0.35), (rnd.uniform(14, 20), rnd.uniform(10, 16), h), rnd.choice(BUZ + ("#1a9cf0",)), rnd)
    for (x, y, r, h) in ((-200, 420, 90, 50), (-40, 460, 80, 40), (120, 430, 95, 56), (280, 460, 90, 44)):
        k_ = kure((x, y, 0), r, M("sirt", lambda: mat_pbr("sirt", "#3aa8ff", 0.5, kaplama=0.15, bump=(1.5, 0.4))), sub=3)
        k_.scale = (1.6, 0.7, h / r)


def kus(konum, olcek, renk, rnd):
    """marti: beyaz tombul govde + gri-mavi kanatlar + sari gaga"""
    x, y, z = konum
    g = kure((x, y, z), 0.4 * olcek, M("kus" + renk, lambda: mat_pbr("kus" + renk, renk, 0.35, kaplama=0.6)), sub=2); g.scale = (0.85, 1.5, 0.8)
    kure((x, y - 0.65 * olcek, z + 0.08 * olcek), 0.1 * olcek, M("gaga", lambda: mat_pbr("gaga", "#ffc41e", 0.3, kaplama=0.7)), sub=2)
    k = rnd.uniform(0.3, 0.9)
    for s in (-1, 1):
        me = bpy.data.meshes.new("kanat")
        me.from_pydata([(x, y - 0.25 * olcek, z), (x + s * 1.6 * olcek, y, z + k * olcek), (x, y + 0.45 * olcek, z)], [], [[0, 1, 2]]); me.update()
        o = bpy.data.objects.new("kanat", me); bpy.context.collection.objects.link(o)
        o.data.materials.append(M("kanat", lambda: mat_pbr("kanat", "#5a8ad8", 0.35, kaplama=0.5))); o.modifiers.new("k", "SOLIDIFY").thickness = 0.05 * olcek


def ucurtma(merkez, olcek, renk1, renk2, rnd):
    """renkli eskenar dortgen ucurtma (iki renk ucgen) + kuyrukta fiyonklar"""
    x, y, z = merkez
    a = rnd.uniform(-0.4, 0.4)
    u, d = Vector((math.sin(a), 0, math.cos(a))), Vector((math.cos(a), 0, -math.sin(a)))
    c = Vector((x, y, z))
    ust, alt, sol, sag = c + u * olcek * 1.2, c - u * olcek * 1.6, c - d * olcek, c + d * olcek
    for (nok, renk) in (((ust, sag, alt), renk1), ((ust, alt, sol), renk2)):
        me = bpy.data.meshes.new("ucurtma"); me.from_pydata([tuple(p) for p in nok], [], [[0, 1, 2]]); me.update()
        o = bpy.data.objects.new("ucurtma", me); bpy.context.collection.objects.link(o)
        o.data.materials.append(M("uc" + renk, lambda r_=renk: mat_pbr("uc" + r_, r_, 0.3, kaplama=0.7))); o.modifiers.new("k", "SOLIDIFY").thickness = 0.04 * olcek
    p = alt
    for k in range(6):
        q = p + Vector((rnd.uniform(-0.3, 0.3), 0, -0.6)) * olcek
        boru(tuple(p), tuple(q), 0.02 * olcek, M("ip", lambda: mat_pbr("ip", "#ffffff", 0.5)))
        f = kure(tuple(q), 0.14 * olcek, M("uc" + (renk1, renk2)[k % 2], lambda r_=(renk1, renk2)[k % 2]: mat_pbr("uc" + r_, r_, 0.3, kaplama=0.7)), sub=1)
        f.scale = (1.8, 0.3, 0.6)
        p = q


def bulut(merkez, olcek, rnd):
    beyaz = M("bulut", lambda: mat_pbr("bulut", "#e8f6ff", 0.85))
    x, y, z = merkez
    for k in range(7):
        r = olcek * rnd.uniform(0.45, 0.85)
        dx = rnd.uniform(-1.5, 1.5) * olcek; dz = rnd.uniform(-0.2, 0.55) * olcek * (1 - abs(dx) / (2 * olcek))
        b = kure((x + dx, y + rnd.uniform(-0.4, 0.4) * olcek, z + dz), r, beyaz, sub=3); b.scale = (1.15, 0.8, 0.9)


def gok_ogeleri(rnd):
    """ekran dolu kurali (md. 7): uzakta birkac kucuk bulut, ortada renkli ucurtmalar (30'un balonlari tekrar edilmez),
    marti suruleri, yakinda ucusan kar taneleri (mavi tonlu)"""
    for (x, y, z, o) in ((-170, 300, 80, 14), (160, 290, 74, 13), (-260, 360, 120, 18), (250, 360, 116, 18)):
        bulut((x, y, z), o, rnd)
    takim = (("#ff1e3c", "#ffd21e"), ("#ff7a14", "#a040ff"), ("#ffd21e", "#ff3ab4"), ("#2fd04a", "#ff7a14"), ("#ff3ab4", "#ffd21e"),
             ("#a040ff", "#2fd04a"), ("#ff1e3c", "#ff7a14"), ("#ffd21e", "#2fd04a"))
    for k, (x, y, z, r) in enumerate(((-30, 80, 24, 2.6), (28, 76, 28, 2.4), (-12, 110, 40, 3.2), (46, 120, 22, 3.0), (-58, 130, 44, 3.6),
                                      (10, 150, 54, 3.6), (76, 170, 56, 4.4), (-90, 180, 32, 4.4), (-20, 64, 15, 1.8), (16, 60, 19, 1.6),
                                      (-44, 100, 18, 2.4), (60, 96, 38, 2.8))):
        ucurtma((x, y, z), r, takim[k % len(takim)][0], takim[k % len(takim)][1], rnd)
    for k in range(16):
        kus((rnd.uniform(-24, 24), rnd.uniform(28, 60), rnd.uniform(9, 22)), rnd.uniform(0.6, 0.9), "#ffffff", rnd)
    for k in range(40):                                                    # ucusan kar taneleri (mavi tonlu, cilali)
        p = kure((rnd.uniform(-12, 12), rnd.uniform(12, 30), rnd.uniform(1.5, 8.0)), rnd.uniform(0.06, 0.11),
                 M("tane", lambda: mat_pbr("tane", "#a8e8ff", 0.2, kaplama=0.8)), sub=1)


# ------------------------------------------------------------------ SERIT: oyuncu buz yolu + renkli sinir + OUT su deligi + kapi
def serit_esyalari(oyuncu, R, rnd):
    s_dis = -1 if oyuncu == "p1" else 1
    yol = mat_buz_blok("serit_yol", "#0a7cff", "#12a4ff", ara="#04307a")
    duz("serit_yol", -1.6, 1.6, -4, GECIS, 0.006, yol)
    bm = M("sinir" + R["ana"], lambda: mat_pbr("sinir" + R["ana"], R["ana"], 0.25, kaplama=0.8))
    for x in (-1.75, 1.75):                                                # serit siniri: oyuncu renginde cilali buz bloklari
        y = -3.6
        while y < KAP["y"] - 0.8:
            yuvarlak_kutu("sinir", (x, y, 0.16), (0.34, 0.62, 0.32), bm, egim=0.08, seg=2)
            y += 0.75
    boya = mat_pbr("ok_" + oyuncu, R["ana"], 0.35, kaplama=0.6)
    for y in (4.9, 6.4):                                                   # buz yolda oyuncu renginde boyali yon oklari (seri sabiti)
        nok = [(-0.75, y - 0.45), (0, y), (0.75, y - 0.45), (0.75, y - 0.75), (0, y - 0.3), (-0.75, y - 0.75)]
        me = bpy.data.meshes.new("ok"); me.from_pydata([(a, b, 0.014) for a, b in nok], [], [list(range(6))]); me.update()
        o = bpy.data.objects.new("ok", me); bpy.context.collection.objects.link(o); o.data.materials.append(boya)
        o.modifiers.new("k", "SOLIDIFY").thickness = 0.02
    # OUT ani: dis tarafta acik su deligi (koyu turkuaz su + kenarinda kar halkasi + yuzen buz parcalari; karakter buraya kayar)
    cx, cy = s_dis * 2.95, 5.2
    su = M("delik", lambda: mat_su("delik", "#00a8e0", "#0038c0", olcek=1.5))
    bpy.ops.mesh.primitive_cylinder_add(radius=1.0, depth=0.05, location=(cx, cy, 0.01), vertices=40)
    d_ = bpy.context.active_object; d_.scale = (1.15, 1.8, 1.0); d_.data.materials.append(su)
    bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.16, location=(cx, cy, 0.04))
    t_ = bpy.context.active_object; t_.scale = (1.15, 1.8, 1.0)
    t_.data.materials.append(M("kar", lambda: mat_pbr("kar", "#5ad0ff", 0.45, kaplama=0.2, bump=(6, 0.2)))); bpy.ops.object.shade_smooth()
    for k in range(5):
        a = rnd.uniform(0, 6.28)
        buz_kutlesi((cx + 0.55 * math.cos(a), cy + 1.0 * math.sin(a), 0.02), (0.25, 0.2, 0.08), rnd.choice(BUZ), rnd, kar=False)
    # dis tarafta yakin buz rafi esyalari: penguen grubu, renkli samandira, kizak, kar tumsekleri
    for k in range(7):
        penguen((s_dis * rnd.uniform(5.0, 9.0), rnd.uniform(2.0, 10.0), 0), rnd.uniform(1.0, 1.3), rnd)
    for k, renk in enumerate(("#ff1e3c", "#ffd21e", "#ff7a14")):
        bpy.ops.mesh.primitive_torus_add(major_radius=0.4, minor_radius=0.14, location=(s_dis * (4.4 + 0.5 * k), 9.4 + 0.4 * k, 0.14))
        o = bpy.context.active_object; o.data.materials.append(M("sam" + renk, lambda r_=renk: mat_pbr("sam" + r_, r_, 0.3, kaplama=0.7)))
        bpy.ops.object.shade_smooth()
    kz = M("kizak", lambda: mat_pbr("kizak", "#ff7a14" if oyuncu == "p1" else "#2fd04a", 0.3, kaplama=0.6))
    yuvarlak_kutu("kizak", (s_dis * 4.2, 2.6, 0.32), (0.8, 1.6, 0.12), kz, egim=0.05, seg=2)
    for dx in (-0.3, 0.3):
        boru((s_dis * 4.2 + dx, 1.6, 0.25), (s_dis * 4.2 + dx, 3.4, 0.05), 0.04, M("fen_g", lambda: mat_pbr("fen_g", "#2a3a4a", 0.4, metal=0.6)))
    for k in range(8):
        t2 = kure((s_dis * rnd.uniform(6, 20), rnd.uniform(-3, GECIS), -0.25), rnd.uniform(0.7, 1.4),
                  M("kar", lambda: mat_pbr("kar", "#5ad0ff", 0.45, kaplama=0.2, bump=(6, 0.2))), sub=2)
        t2.scale = (1.6, 1.0, 0.45)
    for yy in (2.5, 7.4):                                                  # ic tarafta (hakem yeri) kucuk fener direkleri
        fener((-s_dis * 2.45, yy))


def fener(xy):
    x, y = xy
    boru((x, y, 0), (x, y, 1.2), 0.05, M("fen_g", lambda: mat_pbr("fen_g", "#2a3a4a", 0.4, metal=0.6)))
    yuvarlak_kutu("fen_k", (x, y, 1.36), (0.22, 0.22, 0.3), M("fen_c", lambda: mat_pbr("fen_c", "#2a3a4a", 0.4, metal=0.6)), egim=0.03, seg=1)
    kure((x, y, 1.36), 0.09, M("alev", lambda: mat_emis("alev", lin(hex3("#ffd27a")), 6.0)), sub=2)


def kapi(R):
    """buz bloklarindan kapi cercevesi: iki ust uste buz blok direk + kiris (camgobegi cilali), oyuncu renginde bantlar,
    kirisin ustunde kar sapkasi + sarkan buz sarkitlari, ampul dizisi, ustte sonuk LED tabela (motor PLAYER n yazar)"""
    Y, W_, H_, K = KAP["y"], KAP["w"], KAP["h"], KAP["kalin"]
    buz = mat_pbr("kapi_buz", "#08b4ff", 0.12, kaplama=0.8, bump=(4, 0.15))
    kar = mat_pbr("kapi_kar", "#5ad0ff", 0.4, kaplama=0.3, bump=(6, 0.2))
    boya = mat_pbr("kapi_boya", R["ana"], 0.25, kaplama=0.9)
    xk = W_ / 2 + K / 2
    for s in (-1, 1):
        for i, z in enumerate((0.0, 1.05, 2.1, 3.15)):
            hh = min(1.0, H_ + K - z)
            yuvarlak_kutu("direk", (s * xk, Y, z + hh / 2), (K + 0.08 * (i % 2), K + 0.08 * (i % 2), hh - 0.04), buz, egim=0.1, seg=3)
        for z in (1.03, 2.08):
            yuvarlak_kutu("bant", (s * xk, Y, z), (K + 0.1, K + 0.1, 0.14), boya, egim=0.05, seg=2)
        k_ = kure((s * xk, Y, 0.1), K * 0.9, kar, sub=2); k_.scale = (1.0, 1.0, 0.35)
    yuvarlak_kutu("kiris", (0, Y, H_ + K / 2), (W_ + 2 * K + 0.3, K, K), buz, egim=0.1, seg=3)
    yuvarlak_kutu("kiris_bant", (0, Y - K / 2 - 0.02, H_ + K / 2), (W_ + 2 * K, 0.06, 0.18), boya, egim=0.02, seg=1)
    kk = kure((0, Y, H_ + K + 0.05), 1.0, kar, sub=3); kk.scale = ((W_ + 2 * K + 0.5) / 2, K * 0.7, 0.28)
    rnd = random.Random(11 + (R["ana"] == SERIT["p2"]["ana"]))
    sark = M("sarkit", lambda: mat_pbr("sarkit", "#7ae8ff", 0.08, kaplama=0.9))
    for i in range(11):                                                    # kirisin onunden sarkan buz sarkitlari
        xx = -W_ / 2 - K / 2 + (W_ + K) * i / 10
        bpy.ops.mesh.primitive_cone_add(radius1=0.07, radius2=0.0, depth=rnd.uniform(0.25, 0.5), location=(xx, Y - K / 2 - 0.05, H_ - 0.12), rotation=(math.pi, 0, 0), vertices=10)
        bpy.context.active_object.data.materials.append(sark)
    ampul = M("ampul", lambda: mat_emis("ampul", lin(hex3("#ffe08a")), 5.0))
    for i in range(9):
        xx = -W_ / 2 + W_ * i / 8
        kure((xx, Y - K / 2 - 0.12, H_ - 0.35 - 0.12 * math.sin(math.pi * i / 8)), 0.07, ampul, sub=2)
    yuvarlak_kutu("tabela", (0, Y - 0.3, H_ + K + 0.55), (W_ * 0.85, 0.2, 0.7), mat_pbr("tabela", "#15171a", 0.35, metal=0.4), egim=0.05, seg=3)
    me = bpy.data.meshes.new("led_yuz"); a, b = W_ * 0.4, 0.28; z0 = H_ + K + 0.55
    me.from_pydata([(-a, Y - 0.41, z0 - b), (a, Y - 0.41, z0 - b), (a, Y - 0.41, z0 + b), (-a, Y - 0.41, z0 + b)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("led_yuz", me); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat_emis("led_yuz", lin(hex3(R["koyu"])), 1.2))
    for s in (-1, 1):                                                      # direk diplerinde penguen cifti
        for k in range(2):
            penguen((s * (xk + 0.7 + 0.5 * k), Y - 0.6 + rnd.uniform(-0.2, 0.2), 0), 0.9, rnd)


def mat_parlama_kis():
    """buyuk yuzeylerde (buz rafi, yol, kar, sirt) beyaz yansima doygunlugu yiyor -> specular/coat dusuk (30 dersi)"""
    for m in bpy.data.materials:
        if not m.use_nodes or "Principled BSDF" not in m.node_tree.nodes:
            continue
        if m.name.split(".")[0].startswith(("buz_raf", "buz_yol", "serit_yol", "iskele", "kar", "sirt")):
            b = m.node_tree.nodes["Principled BSDF"]
            b.inputs["Specular IOR Level"].default_value = 0.18
            b.inputs["Coat Weight"].default_value = min(0.1, b.inputs["Coat Weight"].default_value)


def serit_katmani(oyuncu):
    R = SERIT[oyuncu]
    sc = buzul_sahnesi(960, 1080, True)
    kam = kamera(sc)
    rnd = random.Random(31 + (oyuncu == "p2"))
    isiklar()
    kiyi(True, random.Random(31))
    serit_esyalari(oyuncu, R, rnd)
    kapi(R)
    Y, W_, H_ = KAP["y"], KAP["w"], KAP["h"]
    ic = W_ / 2
    bpy.context.view_layer.update()
    px = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-ic, Y, 0), (ic, Y, 0), (-ic, Y, H_), (ic, Y, H_))]
    xs = [p.x * 960 for p in px]; ys = [(1 - p.y) * 1080 for p in px]
    YERLESIM["aciklik_" + oyuncu] = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
    # OUT ani: su deliginin ekrandaki yeri; motor 22/23/26/27 anahtar duzeni korunur (minder = su deligi)
    mk = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-2.95, 5.2, 0.4), (2.95, 5.2, 0.4), (0, GECIS, 0))]
    d = {"minder_sol_x": round(mk[0].x * 960, 1), "minder_sag_x": round(mk[1].x * 960, 1),
         "minder_y": round((1 - mk[0].y) * 1080, 1), "gecis_y": round((1 - mk[2].y) * 1080, 1)}
    for on in ("salon_", "plaj_", "orman_", "lale_", "buzul_"):
        YERLESIM[on + oyuncu] = d
    YERLESIM["yol"] = {"y_kapi": Y, "genislik": YOL_YARI * 2, "kam": KAM, "serit_w": 960}
    log("aciklik", oyuncu, YERLESIM["aciklik_" + oyuncu], d)
    mat_parlama_kis()
    yaz(sc, ON_EK + "serit-%s.png" % oyuncu)


def gok_katmani(ad):
    sc = buzul_sahnesi(1920, 1080, False)
    kamera(sc)
    isiklar()
    kiyi(False, random.Random(31))
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
log("bitti (buzul)", YERLESIM.get("aciklik_p1"), YERLESIM.get("aciklik_p2"))
