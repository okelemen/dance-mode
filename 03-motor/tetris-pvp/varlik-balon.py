"""HUMAN TETRIS 35. video (REF-087 yapi, CO-OP 2 oyuncu) - GUNDUZ SICAK HAVA BALONU FESTIVALI, CILALI 3D OYUN GORUNUMU, TEK serit.
varlik.py calistirir (--mod balon). Iskelet varlik-mutfak.py (28, tek serit CO-OP) - katmanlar, kamera, yerlesim anahtarlari ayni.

Mekan kullanici karari (20 Kas 2026, A): bulutlarin ustunde festival pisti, cevrede farkli boy ve desende sicak hava balonlari,
bayrak dizileri, konfeti. OUT ani: karakter pistin yanindaki yumusak bulut yiginina duser (yerlesim "dag" anahtari motor 24'ten).
20. videonun "balonpist"i (gece neon, sisme yastik kapi) ile ilgisi yok: bu gunduz, sepetli sicak hava balonu.
Telif (md. 16): genel balon festivali; logo / yazi / marka baskisi yok, balon desenleri dilimli serit (kendi renklerimiz).
§4 CILALI 3D OYUN GORUNUMU: doygun renk, tombul hatlar, parlak kumas (coat), gercek isik-golge (Cycles); foto dokusu yok,
isiksiz duz renk yok (ampul / LED tabela haric). §8 SOLUK YASAK: buyuk beyaz yuzey yok -> bulut denizi pembe-seftali (pamuk seker),
golgeleri lila; gok koyu doygun mavi tepe; pist sicak turuncu tahta.
Ekran dolu (Masaustu md. 7): gokte yakin-orta-uzak katmanda balonlar, bayrak dizileri, konfeti; bulut denizi ufka kadar.

Katmanlar 28 gibi: gok.png 1920x1080 = uzak bulut denizi + balonlar + gok, serit.png 1920x1080 saydam = yakin bulut + pist + kapi +
OUT bulut yiginlari. Isik iki katmanda ayni olsun diye butun mekan serit sahnesinde de kurulur, uzak kisim holdout.
yerlesim.json: aciklik_p1 (tek kapi), ampul_p1, dag (OUT bulut yiginlari: sol/sag x, y, gecis y), yol.
"""

import random
YERLESIM.clear()
KAPAK = YALNIZ == "kapak"
POZLAMA = float(arg("--pozlama", arg("--kapak-pozlama", "0")))
GUNES = float(arg("--gunes", "4.2"))
ON_EK = "kapak-" if KAPAK else ""
KAP = {"y": 8.6, "w": 7.4, "h": 3.7, "kalin": 0.55}       # CO-OP: iki kisilik genis kapi (27/28 ile ayni)
KAM = {"z": 2.3, "egim": 5.0, "lens": 18.0, "sensor": 24.0}
if KAPAK:
    KAM.update({"z": float(arg("--kapak-z", "2.0")), "egim": float(arg("--kapak-egim", "3.0")), "lens": float(arg("--kapak-lens", "16.0"))})
PIST = 3.9
GECIS = 11.5
CANLI = ("#ff2a3a", "#ffc21a", "#1e8cff", "#20c850", "#ff3aa8", "#ff7a10", "#8a3aff", "#10c8d0")
MAVI, PEMBE = "#1e8cff", "#ff3aa8"
BULUT_UST, BULUT_GOLGE = "#ffc6dc", "#c49cff"


# ------------------------------------------------------------------ sahne / isik
def balon_sahnesi(w, h, saydam):
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
    el[0].position = 0.0; el[0].color = (*lin(hex3("#3ad6ff")), 1)
    el[1].position = 0.42; el[1].color = (*lin(hex3("#0038e0")), 1)     # 30/31/34 dersi: koyu doygun tepe
    e2 = el.new(0.13); e2.color = (*lin(hex3("#0a8cff")), 1)
    nt.links.new(sp.outputs["Z"], rp.inputs[0])
    lp = nt.nodes.new("ShaderNodeLightPath")
    bg_k = nt.nodes.new("ShaderNodeBackground"); bg_k.inputs[1].default_value = 1.0
    bg_i = nt.nodes.new("ShaderNodeBackground"); bg_i.inputs[1].default_value = 0.35
    bg_i.inputs[0].default_value = (*lin(hex3("#bfe0ff")), 1)
    nt.links.new(rp.outputs[0], bg_k.inputs[0])
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


def kamera(sc):
    rx = math.radians(90 - KAM["egim"])
    bpy.ops.object.camera_add(location=(0, 0, KAM["z"]), rotation=(rx, 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.sensor_fit = "VERTICAL"; kam.data.sensor_height = KAM["sensor"]; kam.data.lens = KAM["lens"]
    kam.data.clip_end = 2500
    return kam


def isiklar():
    # ogleden sonra gunesi: arkadan-yandan, balonlarda parlak kenar + bulutlarda uzun lila golge
    bpy.ops.object.light_add(type="SUN", location=(0, 0, 30))
    g = bpy.context.active_object; g.data.energy = GUNES; g.data.angle = math.radians(2.0)
    g.data.color = lin(hex3("#fff0d6"))
    g.rotation_euler = Vector((-0.45, 0.55, -0.70)).to_track_quat("-Z", "Y").to_euler()


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


def mat_bulut(ad="bulut"):
    """pamuk seker bulut: ust yuz seftali-pembe, asagi bakan yuz lila (yon renk karisimi), yumusak ic sacilma; beyaz buyuk alan yok (§8)"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    ge = nt.nodes.new("ShaderNodeNewGeometry"); sp = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(ge.outputs["Normal"], sp.inputs[0])
    rp = nt.nodes.new("ShaderNodeValToRGB"); el = rp.color_ramp.elements
    el[0].position = 0.15; el[0].color = (*lin(hex3(BULUT_GOLGE)), 1)
    el[1].position = 0.75; el[1].color = (*lin(hex3(BULUT_UST)), 1)
    mp = nt.nodes.new("ShaderNodeMapRange"); mp.inputs["From Min"].default_value = -1.0; mp.inputs["From Max"].default_value = 1.0
    nt.links.new(sp.outputs["Z"], mp.inputs["Value"]); nt.links.new(mp.outputs["Result"], rp.inputs[0])
    nt.links.new(rp.outputs[0], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.9
    b.inputs["Subsurface Weight"].default_value = 0.25; b.inputs["Subsurface Radius"].default_value = (1.0, 0.6, 0.8)
    return m


def mat_tahta(ad="tahta", r1="#ff9a1e", r2="#f07a0a", olcek=0.6):
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    wv = nt.nodes.new("ShaderNodeTexWave"); wv.wave_type = "BANDS"; wv.bands_direction = "X"
    wv.inputs["Scale"].default_value = olcek; wv.inputs["Distortion"].default_value = 4.0; wv.inputs["Detail"].default_value = 3
    nt.links.new(geo.outputs["Position"], wv.inputs["Vector"])
    rp = nt.nodes.new("ShaderNodeValToRGB"); el = rp.color_ramp.elements
    el[0].position = 0.2; el[0].color = (*lin(hex3(r1)), 1)
    el[1].position = 0.85; el[1].color = (*lin(hex3(r2)), 1)
    nt.links.new(wv.outputs["Fac"], rp.inputs[0]); nt.links.new(rp.outputs[0], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.35
    b.inputs["Coat Weight"].default_value = 0.35; b.inputs["Coat Roughness"].default_value = 0.1
    return m


def mat_hasir(ad="hasir"):
    """sepet orgusu: sicak hasir, brick dokusuyla orgu kabartmasi"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    br = nt.nodes.new("ShaderNodeTexBrick"); br.inputs["Scale"].default_value = 6.0; br.inputs["Mortar Size"].default_value = 0.04
    br.inputs["Color1"].default_value = (*lin(hex3("#e8a030")), 1); br.inputs["Color2"].default_value = (*lin(hex3("#c8781a")), 1)
    br.inputs["Mortar"].default_value = (*lin(hex3("#8a4a10")), 1)
    nt.links.new(geo.outputs["Position"], br.inputs["Vector"]); nt.links.new(br.outputs["Color"], b.inputs["Base Color"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.5; bp.invert = True
    nt.links.new(br.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = 0.55; b.inputs["Coat Weight"].default_value = 0.15
    return m


def mat_balon(ad, r1, r2, dilim=12, r3=None):
    """balon kumasi: nesne uzayinda dikey dilimler (gore) iki renk sirayla; r3 verilirse ekvator bandi; parlak naylon (coat)"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord"); sp = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Object"], sp.inputs[0])
    at = nt.nodes.new("ShaderNodeMath"); at.operation = "ARCTAN2"
    nt.links.new(sp.outputs["Y"], at.inputs[0]); nt.links.new(sp.outputs["X"], at.inputs[1])
    ml = nt.nodes.new("ShaderNodeMath"); ml.operation = "MULTIPLY"; ml.inputs[1].default_value = dilim / (2 * math.pi)
    nt.links.new(at.outputs[0], ml.inputs[0])
    fr = nt.nodes.new("ShaderNodeMath"); fr.operation = "FRACT"; nt.links.new(ml.outputs[0], fr.inputs[0])
    gt = nt.nodes.new("ShaderNodeMath"); gt.operation = "GREATER_THAN"; gt.inputs[1].default_value = 0.5
    nt.links.new(fr.outputs[0], gt.inputs[0])
    mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"; nt.links.new(gt.outputs[0], mx.inputs["Factor"])
    mx.inputs[6].default_value = (*lin(hex3(r1)), 1); mx.inputs[7].default_value = (*lin(hex3(r2)), 1)
    son = mx.outputs[2]
    if r3:
        ab = nt.nodes.new("ShaderNodeMath"); ab.operation = "ABSOLUTE"; nt.links.new(sp.outputs["Z"], ab.inputs[0])
        lt = nt.nodes.new("ShaderNodeMath"); lt.operation = "LESS_THAN"; lt.inputs[1].default_value = 0.16
        nt.links.new(ab.outputs[0], lt.inputs[0])
        m2 = nt.nodes.new("ShaderNodeMix"); m2.data_type = "RGBA"; nt.links.new(lt.outputs[0], m2.inputs["Factor"])
        nt.links.new(son, m2.inputs[6]); m2.inputs[7].default_value = (*lin(hex3(r3)), 1); son = m2.outputs[2]
    nt.links.new(son, b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.32
    b.inputs["Coat Weight"].default_value = 0.6; b.inputs["Coat Roughness"].default_value = 0.08
    return m


def kutu(ad, merkez, boyut, mat, egim=0.03, seg=3):
    if egim > 0:
        return yuvarlak_kutu(ad, merkez, boyut, mat, egim=egim, seg=seg)
    bpy.ops.mesh.primitive_cube_add(size=1, location=merkez)
    o = bpy.context.active_object; o.name = ad; o.scale = boyut
    bpy.ops.object.transform_apply(scale=True)
    o.data.materials.append(mat)
    return o


def duz(ad, x0, x1, y0, y1, z, mat):
    me = bpy.data.meshes.new(ad)
    me.from_pydata([(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new(ad, me); bpy.context.collection.objects.link(o); o.data.materials.append(mat)
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


# ------------------------------------------------------------------ ogeler
_BMAT = {}


def balon(merkez, R, rnd, renk=None):
    """sicak hava balonu: dilimli zarf (kure 1:1:1,18 + alt koni etek), hasir sepet, 4 halat"""
    x, y, z = merkez
    if renk is None:
        i = rnd.randrange(len(CANLI)); j = (i + rnd.choice((2, 3, 4))) % len(CANLI)
        r3 = CANLI[(j + 2) % len(CANLI)] if rnd.random() < 0.5 else None
        renk = (CANLI[i], CANLI[j], r3)
    key = renk
    if key not in _BMAT:
        _BMAT[key] = mat_balon("balon" + str(len(_BMAT)), renk[0], renk[1], dilim=rnd.choice((10, 12, 14)), r3=renk[2])
    zm = _BMAT[key]
    bpy.ops.mesh.primitive_uv_sphere_add(radius=R, location=(x, y, z), segments=40, ring_count=20)
    o = bpy.context.active_object; o.scale = (1.0, 1.0, 1.18); o.data.materials.append(zm); bpy.ops.object.shade_smooth()
    o.rotation_euler = (0, 0, rnd.uniform(0, math.pi))
    bpy.ops.mesh.primitive_cone_add(radius1=0.62 * R, radius2=0.22 * R, depth=0.75 * R, location=(x, y, z - 1.12 * R), vertices=40)
    e = bpy.context.active_object; e.rotation_euler = (math.pi, 0, 0); e.data.materials.append(zm); bpy.ops.object.shade_smooth()
    zs = z - 1.62 * R
    sep = kutu("sepet", (x, y, zs - 0.13 * R), (0.32 * R, 0.32 * R, 0.24 * R), mat_hasir(), egim=0.03 * R, seg=2)
    hl = mat_pbr("halat", "#7a4a1a", 0.7)
    for dx in (-1, 1):
        for dy in (-1, 1):
            boru((x + dx * 0.14 * R, y + dy * 0.14 * R, zs - 0.02 * R), (x + dx * 0.24 * R, y + dy * 0.24 * R, z - 1.48 * R), max(0.012, 0.012 * R), hl)
    return o


def bulut(merkez, olcek, rnd, mat):
    x, y, z = merkez
    for k in range(9):
        r = olcek * rnd.uniform(0.45, 0.85)
        dx = rnd.uniform(-1.5, 1.5) * olcek; dz = rnd.uniform(-0.2, 0.55) * olcek * (1 - abs(dx) / (2 * olcek))
        b = kure((x + dx, y + rnd.uniform(-0.4, 0.4) * olcek, z + dz), r, mat, sub=3); b.scale = (1.15, 0.8, 0.9)
    kure((x, y, z - 0.25 * olcek), olcek * 0.75, mat).scale = (2.4, 0.8, 0.45)


def bulut_denizi(rnd, mat, y0, y1, x_gen, adim, z=-0.6):
    """ufka kadar kabarik bulut tepecikleri (zemin): seyrek kure tarlasi, uzakta buyur (perspektif zaten sikistirir)"""
    y = y0
    while y < y1:
        s = 1.0 + (y - y0) / 25.0
        x = -x_gen + rnd.uniform(0, adim * s)
        while x < x_gen:
            r = rnd.uniform(1.4, 2.4) * s
            b = kure((x, y + rnd.uniform(-0.5, 0.5) * s, z + rnd.uniform(-0.3, 0.4) * r), r, mat, sub=2); b.scale = (1.3, 1.0, 0.55)
            x += adim * s * rnd.uniform(0.75, 1.15)
        y += adim * 0.8 * s


def bayrak_dizisi(a, b, sarkma, rnd, n=None):
    """iki nokta arasinda sarkan ip + ucgen bayraklar (renkli, kumas)"""
    ip = mat_pbr("ip", "#fff2d0", 0.6)
    L = (Vector(b) - Vector(a)).length
    n = n or max(6, int(L / 0.7))
    pts = []
    for i in range(n + 1):
        t = i / n
        p = Vector(a).lerp(Vector(b), t); p.z -= sarkma * 4 * t * (1 - t); pts.append(p)
    for i in range(n):
        boru(tuple(pts[i]), tuple(pts[i + 1]), 0.02, ip)
    for i in range(n):
        p, q = pts[i], pts[i + 1]
        m = (p + q) / 2; w = (q - p).length * 0.42
        d = (q - p).normalized()
        v1, v2 = m - d * w, m + d * w
        v3 = m + Vector((0, 0, -w * 1.5))
        me = bpy.data.meshes.new("bayrak"); me.from_pydata([tuple(v1), tuple(v2), tuple(v3)], [], [[0, 1, 2]]); me.update()
        o = bpy.data.objects.new("bayrak", me); bpy.context.collection.objects.link(o)
        o.data.materials.append(mat_pbr("bayrak" + str(i % 8), CANLI[(i * 3) % 8], 0.45, kaplama=0.3))
        o.modifiers.new("k", "SOLIDIFY").thickness = 0.01


def direk(x, y, h, renk):
    """festival diregi: cizgili (iki renk halka) + tepede kucuk top"""
    m1, m2 = mat_pbr("dir1" + renk, renk, 0.3, kaplama=0.6), mat_pbr("dir2", "#fff2d0", 0.3, kaplama=0.6)
    n = int(h / 0.5)
    for i in range(n):
        silindir((x, y, i * 0.5), 0.14, 0.5, m1 if i % 2 == 0 else m2, v=20)
    kure((x, y, h + 0.15), 0.26, mat_pbr("dir_top", "#ffc21a", 0.2, kaplama=0.8))


def konfeti(rnd, n, x_gen, y0, y1, z0, z1, kac=0.0):
    for _ in range(n):
        x = rnd.uniform(-x_gen, x_gen); y = rnd.uniform(y0, y1); z = rnd.uniform(z0, z1)
        if abs(x) < kac and y < y0 + 15:
            continue
        o = kutu("konfeti", (x, y, z), (0.35, 0.05, 0.22), mat_pbr("konf" + str(_ % 8), CANLI[_ % 8], 0.3, kaplama=0.7), egim=0.0)
        o.rotation_euler = (rnd.uniform(0, 3.1), rnd.uniform(0, 3.1), rnd.uniform(0, 3.1))


# ------------------------------------------------------------------ MEKAN (her iki katmanda; serit sahnesinde uzak kisim holdout)
def mekan(serit_modu, rnd):
    bm = mat_bulut()
    bulut_denizi(rnd, bm, -4, GECIS, 60, 3.2, z=-0.7)                 # yakin bulut zemini (pistin iki yani)
    for o in bpy.data.objects:
        if o.type == "MESH":
            o["yakin"] = 1
    bulut_denizi(rnd, bm, GECIS, 260, 420, 5.0, z=-1.2)               # uzak bulut denizi ufka kadar
    for (x, y, z, s) in ((-60, 160, 26, 9), (70, 190, 34, 11), (-140, 230, 18, 12), (150, 240, 22, 13), (0, 320, 44, 15), (-30, 120, 52, 7)):
        bulut((x, y, z), s, rnd, bm)                                  # gokte suzulen kabarik bulutlar
    # balonlar: yakin (kenarlarda buyuk), orta, uzak; kapinin ustu ve tam orta koridor bos kalir
    for (x, y, z, R) in ((-15, 22, 9.5, 3.2), (17, 26, 12.5, 3.6), (-30, 40, 20, 4.4), (32, 46, 7.5, 4.0), (-9, 55, 26, 3.4),
                         (11, 62, 31, 3.0), (-46, 70, 12, 5.0), (52, 80, 24, 5.2), (-24, 95, 40, 4.6), (28, 105, 44, 4.2),
                         (-72, 120, 30, 6.0), (78, 130, 14, 6.4), (0, 150, 58, 5.0), (-55, 170, 56, 6.0), (60, 175, 60, 6.2),
                         (-100, 200, 22, 7.0), (110, 215, 40, 7.4), (-20, 240, 80, 6.0), (35, 260, 96, 6.6), (-80, 280, 100, 7.0)):
        balon((x, y, z), R, rnd)
    for _ in range(26):                                               # uzak kucuk balonlar (gok dolu)
        x = rnd.uniform(-260, 260); y = rnd.uniform(280, 520); z = rnd.uniform(20, 170)
        balon((x, y, z), rnd.uniform(5, 9), rnd)
    konfeti(rnd, 70, 40, 14, 60, 6, 34, kac=8)
    if serit_modu:
        for o in bpy.data.objects:
            if o.type == "MESH" and not o.get("yakin"):
                o.is_holdout = True


# ------------------------------------------------------------------ SERIT: tahta festival pisti + balon babali sinir + oklar + OUT bulut yiginlari
def serit_esyalari(rnd):
    kutu("pist", (0, (KAP["y"] + 0.4 - 4) / 2, 0.0), (PIST * 2, KAP["y"] + 4.4, 0.16), mat_tahta("pist"), egim=0.04, seg=2)
    kenar = mat_pbr("pist_kenar", "#e8102c", 0.3, kaplama=0.6)
    for s in (-1, 1):
        kutu("pist_kenar", (s * (PIST + 0.06), (KAP["y"] + 0.4 - 4) / 2, 0.02), (0.18, KAP["y"] + 4.4, 0.24), kenar, egim=0.05, seg=2)
    bay = {-1: MAVI, 1: PEMBE}
    for s in (-1, 1):                                            # pist kenarinda kucuk balon babalar: solda mavi, sagda pembe (P1/P2 tarafi)
        y = -3.0; i = 0
        while y < KAP["y"] - 0.4:
            renk = bay[s] if i % 2 == 0 else "#ffc21a"
            silindir((s * (PIST + 0.45), y, 0.0), 0.08, 0.7, mat_pbr("baba_dir", "#fff2d0", 0.4), v=12)
            b = kure((s * (PIST + 0.45), y, 0.98), 0.3, mat_pbr("baba" + renk, renk, 0.15, kaplama=0.9)); b.scale = (1, 1, 1.15)
            y += 1.3; i += 1
    ok = mat_pbr("ok", "#ffc21a", 0.3, kaplama=0.7)
    for x in (-1.7, 1.7):
        for y in (4.6, 6.2):
            nok = [(x - 0.6, y - 0.4), (x, y), (x + 0.6, y - 0.4), (x + 0.6, y - 0.68), (x, y - 0.28), (x - 0.6, y - 0.68)]
            me = bpy.data.meshes.new("ok"); me.from_pydata([(a, b, 0.17) for a, b in nok], [], [list(range(6))]); me.update()
            o = bpy.data.objects.new("ok", me); bpy.context.collection.objects.link(o); o.data.materials.append(ok)
            o.modifiers.new("k", "SOLIDIFY").thickness = 0.02
    bm = mat_bulut("out_bulut")
    for s in (-1, 1):                                            # OUT ani: iki dis tarafta yumusak bulut yigini
        bulut((s * 5.6, 5.0, 0.6), 1.25, random.Random(35 + s), bm)
    for s in (-1, 1):                                            # yakin plan: kenarda festival diregi + kucuk balon (dolu)
        direk(s * 7.6, 2.2, 3.4, MAVI if s < 0 else PEMBE)


def kapi():
    """sepet kuleli kemer: iki yanda ust uste hasir sepetler, kiris cizgili kumas, tepede iki kucuk balon; LED tabela; ampul dizisi; bayraklar"""
    Y, W_, H_, K = KAP["y"], KAP["w"], KAP["h"], KAP["kalin"]
    xk = W_ / 2 + K / 2
    hs = mat_hasir("kapi_hasir")
    rk = ("#e8102c", "#ffc21a")
    for s in (-1, 1):
        for i in range(5):
            kutu("kule_sepet", (s * xk, Y, i * 0.85 + 0.42), (K + 0.2, K + 0.2, 0.78), hs, egim=0.08, seg=3)
            kutu("kule_serit", (s * xk, Y, i * 0.85 + 0.80), (K + 0.24, K + 0.24, 0.08), mat_pbr("ks" + str(i), rk[i % 2], 0.3, kaplama=0.6), egim=0.03, seg=2)
        balon((s * xk, Y, H_ + K + 2.05), 0.62, random.Random(9 + s), renk=(MAVI if s < 0 else PEMBE, "#ffc21a", None))
    kp = mat_balon("kiris_kumas", "#e8102c", "#fff2d0", dilim=24)
    yuvarlak_kutu("kiris", (0, Y, H_ + K / 2), (W_ + 2 * K, K + 0.1, K), mat_pbr("kiris_ic", "#e8102c", 0.35, kaplama=0.5), egim=0.18, seg=5)
    for i in range(12):                                          # kiris uzerinde kirmizi-krem cizgi seritler
        x = -W_ / 2 - K + (i + 0.5) * (W_ + 2 * K) / 12
        if i % 2:
            yuvarlak_kutu("kiris_c", (x, Y, H_ + K / 2), ((W_ + 2 * K) / 12 * 0.98, K + 0.14, K + 0.04), mat_pbr("krem", "#fff2d0", 0.35, kaplama=0.5), egim=0.12, seg=3)
    bayrak_dizisi((-xk, Y - 0.45, H_ - 0.05), (xk, Y - 0.45, H_ - 0.05), 0.35, random.Random(35))
    yuvarlak_kutu("tabela", (0, Y, H_ + K + 0.75), (W_ * 0.6, 0.2, 0.7), mat_pbr("tabela", "#15171a", 0.35, metal=0.4), egim=0.05, seg=3)
    me = bpy.data.meshes.new("led_yuz"); a, b = W_ * 0.28, 0.28; z0 = H_ + K + 0.75
    me.from_pydata([(-a, Y - 0.11, z0 - b), (a, Y - 0.11, z0 - b), (a, Y - 0.11, z0 + b), (-a, Y - 0.11, z0 + b)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("led_yuz", me); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat_emis("led_yuz", lin(hex3("#0a3a6a")), 1.2))
    for s in (-1, 1):
        boru((s * W_ * 0.22, Y, H_ + K + 0.2), (s * W_ * 0.22, Y, H_ + K + 0.42), 0.02, mat_pbr("tel", "#cfd3d8", 0.3, metal=1.0))
    for s in (-1, 1):                                            # kapidan dis direklere bayrak dizisi (yakin plan dolu)
        bayrak_dizisi((s * (xk + 0.3), Y - 0.2, H_ + K), (s * 7.6, 2.2, 3.5), 0.5, random.Random(36 + s))


def serit_katmani():
    sc = balon_sahnesi(1920, 1080, True)
    kam = kamera(sc)
    rnd = random.Random(35)
    isiklar()
    mekan(True, random.Random(35))
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
    sc = balon_sahnesi(1920, 1080, False)
    kamera(sc)
    isiklar()
    mekan(False, random.Random(35))
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
log("bitti (balon)", YERLESIM.get(ON_EK + "aciklik_p1"))
