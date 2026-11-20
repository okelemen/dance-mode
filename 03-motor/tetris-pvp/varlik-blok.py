"""HUMAN TETRIS 34. video (REF-086 yapi, 3P CO-OP) - GUNDUZ OYUNCAK BLOK SEHRI, CILALI 3D OYUN GORUNUMU.
varlik.py calistirir (--mod blok).

Mekan kullanici karari (20 Kas 2026, B): oyuncak blok sehri, gunduz; OUT ani: karakter kapinin yanindaki blok yiginina duser
(bloklar sacilir). Icerik: tombul renkli yapi bloklarindan evler, kuleler (koni cati), blok agaclar, yolun ustunden gecen blok
kopru-kemer, uzakta blok silueti sehir; gokte blok bulutlar, ucusan renkli kupler, kuslar (30 balon, 31 ucurtma tekrar edilmez).
Telif (md. 16): bloklar DUZ / yuvarlatilmis yuzlu, ustte yuvarlak cikinti (stud) YOK, logo/minifigur/yazi yok - tanınır marka
tuglasi birebir alinmaz. §4 CILALI 3D OYUN GORUNUMU: doygun renk, tombul hatlar, parlak oyuncak plastik (coat), gercek isik-golge
(Cycles); foto dokusu yok, isiksiz duz renk yok (ampul / LED tabela / pencere haric). §8 SOLUK YASAK: buyuk beyaz yuzey yok
(bulutlar acik mavi-beyaz, kucuk), zemin doygun yesil, gok koyu doygun mavi tepe.
Pist: uc serit (P1 mavi sol / P2 pembe orta / P3 yesil sag; atolye 32 duzeni 3 x 640): oyuncu renginde iki tonlu blok dosemeli
yol, kenarda sari blok bordur, sari yon oklari. Kapi: oyuncu renginde ust uste bloklardan direkler + kiris, tepede renkli kup,
ampul dizisi, LED tabela.

Katmanlar atolye (32) ile ayni: gok.png = butun sehir (1920), serit-p1..p3.png = oyuncunun yakin yolu + kapi + blok yigini;
isik ayni olsun diye butun sehir serit katmaninda da kurulur, holdout.
Ciktilar: gok.png, serit-p1..p3.png (640x1080), panel-p1..p3.png, yerlesim.json;
kapak modu (--yalniz kapak): kapak-gok.png, kapak-serit-p1..p3.png
"""

import random
YERLESIM.clear()
KAPAK = YALNIZ == "kapak"
POZLAMA = float(arg("--pozlama", arg("--kapak-pozlama", "0")))
GUNES = float(arg("--gunes", "4.6"))
ON_EK = "kapak-" if KAPAK else ""
SERIT_W = 640
KAP = {"y": 8.0, "w": 2.7, "h": 3.5, "kalin": 0.5}
KAM = {"z": 2.2, "egim": 5.0, "lens": 18.0, "sensor": 24.0}
if KAPAK:
    KAM.update({"z": float(arg("--kapak-z", "2.0")), "egim": float(arg("--kapak-egim", "4.0")), "lens": float(arg("--kapak-lens", "15.0"))})
GECIS = 11.0            # serit yolu burada biter, otesi gok.png
SEHIR_Y = 90.0
SERIT = {
    "p1": {"ana": "#1e7cff", "koyu": "#0a3fa8", "acik": "#8cc8ff", "iki": "#00b4ff"},
    "p2": {"ana": "#ff2aa0", "koyu": "#a8105e", "acik": "#ffa6d6", "iki": "#c020ff"},
    "p3": {"ana": "#18c840", "koyu": "#0a6a22", "acik": "#9cf0a8", "iki": "#00d890"},
}
BLOK = ("#e8102c", "#ffc21a", "#1e7cff", "#18c840", "#ff6a10", "#8a2ae8", "#ff2aa0", "#00b8d8")


# ------------------------------------------------------------------ sahne / isik (arena 33 gok semasi)
def blok_sahnesi(w, h, saydam):
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
    el[0].position = 0.0; el[0].color = (*lin(hex3("#20c0ff")), 1)
    el[1].position = 0.40; el[1].color = (*lin(hex3("#0030d0")), 1)   # 30/31 dersi: koyu doygun tepe
    e2 = el.new(0.12); e2.color = (*lin(hex3("#0a80ff")), 1)
    nt.links.new(sp.outputs["Z"], rp.inputs[0])
    lp = nt.nodes.new("ShaderNodeLightPath")
    bg_k = nt.nodes.new("ShaderNodeBackground"); bg_k.inputs[1].default_value = 1.0
    bg_i = nt.nodes.new("ShaderNodeBackground"); bg_i.inputs[1].default_value = 0.25
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


def mat_doseme(ad, renk1, renk2, ara, olcek=1.0, satir=0.5, gen=1.0):
    """blok doseme: tugla dokusuyla kare plakalar, iki ton + koyu derz + kabarik kenar bump; yari mat plastik"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.inputs["Scale"].default_value = olcek; br.inputs["Mortar Size"].default_value = 0.03
    br.inputs["Brick Width"].default_value = gen; br.inputs["Row Height"].default_value = satir
    br.inputs["Color1"].default_value = (*lin(hex3(renk1)), 1); br.inputs["Color2"].default_value = (*lin(hex3(renk2)), 1)
    br.inputs["Mortar"].default_value = (*lin(hex3(ara)), 1)
    br.offset = 0.0; br.squash = 1.0
    nt.links.new(geo.outputs["Position"], br.inputs["Vector"])
    nt.links.new(br.outputs["Color"], b.inputs["Base Color"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.5; bp.inputs["Distance"].default_value = 0.03
    nt.links.new(br.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = 0.4; b.inputs["Coat Weight"].default_value = 0.2; b.inputs["Coat Roughness"].default_value = 0.1
    b.inputs["Specular IOR Level"].default_value = 0.15
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


def P(renk, purluk=0.3, kaplama=0.7, metal=0.0):
    """tekrar kullanilan cilali oyuncak plastik"""
    return M("p%s_%s_%s" % (renk, purluk, metal), lambda: mat_pbr("p" + renk, renk, purluk, metal=metal, kaplama=kaplama))


# ------------------------------------------------------------------ blok ogeleri (stud YOK)
def blok(konum, boyut, renk, egim=None):
    """tek tombul oyuncak blok: yuvarlatilmis kenarli kutu, cilali plastik; konum = taban merkezi"""
    x, y, z = konum; bx, by, bz = boyut
    return yuvarlak_kutu("blok", (x, y, z + bz / 2), boyut, P(renk, 0.28, 0.6), egim=egim or min(bx, by, bz) * 0.14, seg=3)


def pencere_izgara(x, y_on, z0, gen, yuk, rnd, yon=-1, eksen="y"):
    """bina onunde koyu cam pencere kareleri (bazilari sicak yanar), cerceve beyaz degil sari"""
    cam = M("cam", lambda: mat_pbr("cam", "#0a2a8a", 0.12, kaplama=0.9))
    yanan = M("yanan", lambda: mat_emis("yanan", lin(hex3("#ffd23a")), 2.5))
    nx = max(1, int(gen / 1.1)); nz = max(1, int(yuk / 1.3))
    for i in range(nx):
        for k in range(nz):
            px = x - gen / 2 + (i + 0.5) * gen / nx; pz = z0 + 0.7 + k * 1.3
            if pz > z0 + yuk - 0.5:
                continue
            m = yanan if rnd.random() < 0.15 else cam
            if eksen == "y":
                yuvarlak_kutu("pencere", (px, y_on + yon * 0.04, pz), (0.55, 0.08, 0.7), m, egim=0.05, seg=2)
            else:
                yuvarlak_kutu("pencere", (y_on + yon * 0.04, px, pz), (0.08, 0.55, 0.7), m, egim=0.05, seg=2)


def ev(taban, gen, der, kat, rnd):
    """ust uste bloklardan ev: her kat ayri renk blok, pencereler, ustte koni/piramit cati"""
    x, y, z = taban
    h = 0.0
    renkler = rnd.sample(BLOK, len(BLOK))
    for k in range(kat):
        kh = rnd.uniform(1.6, 2.2)
        blok((x, y, z + h), (gen, der, kh), renkler[k % len(renkler)])
        h += kh
    pencere_izgara(x, y - der / 2, z, gen * 0.85, h, rnd)
    cati = rnd.choice(("koni", "piramit", "kup"))
    cr = rnd.choice(BLOK)
    if cati == "koni":
        bpy.ops.mesh.primitive_cone_add(radius1=max(gen, der) * 0.62, radius2=0, depth=gen * 0.8, location=(x, y, z + h + gen * 0.4), vertices=32)
        bpy.context.active_object.data.materials.append(P(cr, 0.28, 0.6)); bpy.ops.object.shade_smooth()
    elif cati == "piramit":
        bpy.ops.mesh.primitive_cone_add(radius1=max(gen, der) * 0.75, radius2=0, depth=gen * 0.7, location=(x, y, z + h + gen * 0.35), vertices=4, rotation=(0, 0, math.pi / 4))
        o = bpy.context.active_object; o.data.materials.append(P(cr, 0.28, 0.6))
        bv = o.modifiers.new("b", "BEVEL"); bv.width = 0.08; bv.segments = 2
    else:
        blok((x, y, z + h), (gen * 0.5, der * 0.5, gen * 0.5), cr)
    return h


def kule(taban, r, kat, rnd):
    """silindir bloklardan yuvarlak kule + sivri koni cati + tepede kup"""
    x, y, z = taban
    h = 0.0
    for k in range(kat):
        kh = rnd.uniform(1.4, 2.0)
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=kh, location=(x, y, z + h + kh / 2), vertices=36)
        o = bpy.context.active_object; o.data.materials.append(P(BLOK[(k + int(x * 3)) % len(BLOK)], 0.28, 0.6)); bpy.ops.object.shade_smooth()
        bv = o.modifiers.new("b", "BEVEL"); bv.width = 0.12; bv.segments = 3; bv.limit_method = "ANGLE"
        h += kh
    bpy.ops.mesh.primitive_cone_add(radius1=r * 1.25, radius2=0, depth=r * 2.4, location=(x, y, z + h + r * 1.2), vertices=36)
    bpy.context.active_object.data.materials.append(P(rnd.choice(("#e8102c", "#8a2ae8", "#ff6a10")), 0.28, 0.6)); bpy.ops.object.shade_smooth()
    blok((x, y, z + h + r * 2.3), (0.35, 0.35, 0.35), "#ffc21a")
    return h


def agac(taban, olcek, rnd):
    """blok agac: kahve kutu govde + ust uste yesil kupler"""
    x, y, z = taban
    blok((x, y, z), (0.45 * olcek, 0.45 * olcek, 1.1 * olcek), "#a0480e")
    yes = rnd.choice(("#18b030", "#2fd04a", "#0a9a30", "#7ad010"))
    blok((x, y, z + 1.0 * olcek), (1.6 * olcek, 1.6 * olcek, 1.0 * olcek), yes)
    blok((x, y, z + 1.9 * olcek), (1.1 * olcek, 1.1 * olcek, 0.85 * olcek), yes)
    blok((x, y, z + 2.65 * olcek), (0.6 * olcek, 0.6 * olcek, 0.6 * olcek), yes)


def blok_yigini(merkez, gen, yuk, rnd, kat=4):
    """piramit gibi ust uste dagilmis oyuncak bloklar (OUT yigini ve dolgu)"""
    x0, y0 = merkez
    z = 0.0
    for k in range(kat):
        w = gen * (1 - 0.2 * k)
        n = max(1, int(w / (yuk * 0.9)))
        for i in range(n):
            b = rnd.uniform(0.8, 1.0) * w / n
            blok((x0 - w / 2 + (i + 0.5) * w / n + rnd.uniform(-0.1, 0.1) * b, y0 + rnd.uniform(-0.3, 0.3) * yuk, z),
                 (b * 0.92, b * rnd.uniform(0.75, 1.0), yuk * rnd.uniform(0.75, 1.0)), rnd.choice(BLOK))
        z += yuk * 0.85
        if w < yuk:
            break


def bulut(merkez, olcek, rnd):
    """kuplerden bulut (acik mavi-beyaz, kucuk; buyuk beyaz yuzey olmasin - soluk yasak)"""
    x, y, z = merkez
    for k in range(rnd.randint(5, 8)):
        s = olcek * rnd.uniform(0.7, 1.3)
        yuvarlak_kutu("bulut", (x + rnd.uniform(-1.6, 1.6) * olcek, y + rnd.uniform(-0.4, 0.4) * olcek, z + rnd.uniform(-0.4, 0.6) * olcek),
                      (s, s, s * 0.8), M("bulut", lambda: mat_pbr("bulut", "#e8f4ff", 0.5, kaplama=0.3)), egim=s * 0.25, seg=3)


def kus(merkez, olcek, renk):
    x, y, z = merkez
    for s in (-1, 1):
        k = kure((x + s * 0.35 * olcek, y, z + 0.08 * olcek), 0.3 * olcek, P(renk, 0.4, 0.3), sub=2); k.scale = (1.4, 0.25, 0.35)
        k.rotation_euler = (0, s * 0.35, 0)
    kure((x, y, z), 0.18 * olcek, P(renk, 0.4, 0.3), sub=2)


# ------------------------------------------------------------------ SEHIR (iki katmanda; serit sahnesinde holdout)
def sehir(serit_modu, rnd):
    _MAT.clear()
    zemin = mat_doseme("zemin", "#18b830", "#22c83a", "#0a6a1c", olcek=0.5, satir=0.5, gen=1.0)
    duz("zemin_yakin", -60, 60, -4, GECIS, 0, zemin)
    duz("zemin_uzak", -400, 400, GECIS, 600, 0, zemin)
    # orta cadde (uzak yol): sari-turuncu blok doseme, kameradan ufka
    cad = mat_doseme("cadde", "#ffb21a", "#ff9a10", "#a04a04", olcek=0.6, satir=0.5, gen=1.0)
    duz("cadde", -6.0, 6.0, GECIS, SEHIR_Y, 0.01, cad)
    # caddenin iki yaninda evler / kuleler / agaclar (yakindan uzaga sik; bos koridor yok)
    for s in (-1, 1):
        y = 13.0
        while y < SEHIR_Y:
            x = s * rnd.uniform(9.0, 11.0)
            if rnd.random() < 0.28:
                kule((x, y, 0), rnd.uniform(1.4, 2.0), rnd.randint(3, 6), rnd); y += rnd.uniform(4.5, 6.0)
            else:
                g = rnd.uniform(3.5, 5.0)
                ev((x, y, 0), g, rnd.uniform(3.0, 4.0), rnd.randint(2, 5), rnd); y += g + rnd.uniform(1.0, 2.0)
        # ikinci sira (daha yuksek, arkada)
        y = 16.0
        while y < SEHIR_Y + 20:
            x = s * rnd.uniform(17.0, 24.0)
            if rnd.random() < 0.35:
                kule((x, y, 0), rnd.uniform(2.0, 2.8), rnd.randint(5, 9), rnd); y += rnd.uniform(6, 9)
            else:
                g = rnd.uniform(5.0, 7.0)
                ev((x, y, 0), g, rnd.uniform(4.0, 5.5), rnd.randint(4, 8), rnd); y += g + rnd.uniform(1.0, 3.0)
        # yakin kenarda agaclar + ucuncu sira dolgu
        y = 12.0
        while y < SEHIR_Y:
            agac((s * rnd.uniform(6.6, 7.6), y, 0), rnd.uniform(0.9, 1.3), rnd); y += rnd.uniform(3.0, 4.5)
        for k in range(26):
            agac((s * rnd.uniform(27, 45), rnd.uniform(14, 110), 0), rnd.uniform(1.4, 2.4), rnd)
    # uzak skyline: caddenin sonunda dev blok binalar duvari (ufuk dolu)
    x = -80.0
    while x < 80:
        g = rnd.uniform(6, 11)
        if abs(x) < 7:
            x += g; continue
        ev((x, SEHIR_Y + rnd.uniform(5, 25), 0), g, rnd.uniform(5, 8), rnd.randint(5, 12), rnd)
        x += g + rnd.uniform(0.5, 2.5)
    kule((0, SEHIR_Y + 30, 0), 4.0, 10, rnd)
    # caddenin ustunden gecen iki blok kopru-kemer
    for yk in (30.0, 58.0):
        for s in (-1, 1):
            h = 0
            for k in range(5):
                blok((s * 7.0, yk, h), (1.6, 1.6, 1.4), BLOK[(k + int(yk)) % len(BLOK)]); h += 1.4
        for i in range(10):
            blok((-7.0 + 14.0 * i / 9, yk, 7.0), (1.6, 1.8, 1.0), BLOK[i % len(BLOK)])
    # gok: kup bulutlar, ucusan renkli kupler, kuslar (ekran dolu kurali)
    for k in range(22):
        bulut((rnd.uniform(-70, 70), rnd.uniform(70, 220), rnd.uniform(22, 70)), rnd.uniform(2.5, 5.0), rnd)
    for k in range(70):
        yuvarlak_kutu("ucan_kup", (rnd.uniform(-30, 30), rnd.uniform(25, 120), rnd.uniform(9, 45)), (rnd.uniform(0.6, 1.6),) * 3,
                      P(rnd.choice(BLOK), 0.28, 0.6), egim=0.15, seg=2).rotation_euler = (rnd.uniform(0, 3), rnd.uniform(0, 3), rnd.uniform(0, 3))
    for k in range(30):
        kus((rnd.uniform(-25, 25), rnd.uniform(25, 80), rnd.uniform(10, 30)), rnd.uniform(0.6, 1.0), rnd.choice(("#ff6a10", "#e8102c", "#ffc21a")))
    if serit_modu:
        for o in bpy.data.objects:
            if o.type == "MESH" and o.name.split(".")[0] not in ("zemin_yakin",):
                o.is_holdout = True


# ------------------------------------------------------------------ SERIT: blok dosemeli yol + kapi + OUT blok yigini
def serit_esyalari(oyuncu, R, rnd):
    yol = M("yol" + oyuncu, lambda: mat_doseme("yol" + oyuncu, R["ana"], R["iki"], R["koyu"], olcek=1.2, satir=0.5, gen=1.0))
    duz("yol", -1.15, 1.15, -4, GECIS, 0.02, yol)
    for s in (-1, 1):                                                      # sari blok bordur
        y = -3.6
        while y < KAP["y"] - 0.3:
            blok((s * 1.32, y, 0), (0.32, 0.62, 0.3), "#ffc21a" if int(y * 2) % 2 == 0 else "#ff6a10")
            y += 0.7
    boya = P("#ffd21e", 0.3, 0.6)
    for y in (4.9, 6.4):                                                   # yolda sari yon oklari (seri sabiti)
        nok = [(-0.65, y - 0.4), (0, y), (0.65, y - 0.4), (0.65, y - 0.68), (0, y - 0.28), (-0.65, y - 0.68)]
        me = bpy.data.meshes.new("ok"); me.from_pydata([(a, b, 0.035) for a, b in nok], [], [list(range(6))]); me.update()
        o = bpy.data.objects.new("ok", me); bpy.context.collection.objects.link(o); o.data.materials.append(boya)
        o.modifiers.new("k", "SOLIDIFY").thickness = 0.02
    # OUT ani: kapinin iki yaninda blok yigini (karakter buraya duser, bloklar sacilir)
    for s in (-1, 1):
        blok_yigini((s * 2.45, KAP["y"] + 0.4), 1.6, 0.7, random.Random({"p1": 5, "p2": 6, "p3": 7}[oyuncu] * 10 + s), kat=4)
    for s in (-1, 1):                                                      # yol onunde sacilmis birkac kup
        blok((s * 1.95, 2.4 + rnd.uniform(-0.3, 0.3), 0), (0.45, 0.45, 0.45), rnd.choice(BLOK))
        blok((s * 1.9, 4.0, 0), (0.35, 0.35, 0.35), rnd.choice(BLOK))


def kapi(R):
    """blok kapi: iki yanda oyuncu renginde ust uste dort blok, ustte uzun blok kiris, tepede renkli kup ucu,
    kirisin altinda ampul dizisi, ustte sonuk LED tabela (motor PLAYER n yazar)"""
    Y, W_, H_, K = KAP["y"], KAP["w"], KAP["h"], KAP["kalin"]
    xk = W_ / 2 + K / 2
    for s in (-1, 1):
        z = 0.0
        for i in range(4):
            h = (H_ + K) / 4
            blok((s * xk, Y, z), (K + 0.08 * (i % 2), K + 0.08 * (i % 2), h - 0.03), R["ana"] if i % 2 == 0 else R["iki"])
            z += h
    blok((0, Y, H_), (W_ + 2 * K + 0.2, K, K), R["ana"])
    for i, c in enumerate(("#ffc21a", "#e8102c", "#ffc21a")):
        blok(((i - 1) * 0.6, Y, H_ + K), (0.45, 0.45, 0.45), c)
    ampul = [M("amp" + c, lambda c_=c: mat_emis("amp" + c_, lin(hex3(c_)), 6.0)) for c in ("#ffd21e", "#ff2a5a", "#2a8aff", "#30e060")]
    for i in range(9):
        xx = -W_ / 2 + W_ * i / 8
        kure((xx, Y - K / 2 - 0.1, H_ - 0.3 - 0.12 * math.sin(math.pi * i / 8)), 0.07, ampul[i % 4], sub=2)
    yuvarlak_kutu("tabela", (0, Y - 0.3, H_ + K + 1.15), (W_ * 0.85, 0.2, 0.62), mat_pbr("tabela", "#15171a", 0.35, metal=0.4), egim=0.05, seg=3)
    me = bpy.data.meshes.new("led_yuz"); a, b = W_ * 0.4, 0.24; z0 = H_ + K + 1.15
    me.from_pydata([(-a, Y - 0.41, z0 - b), (a, Y - 0.41, z0 - b), (a, Y - 0.41, z0 + b), (-a, Y - 0.41, z0 + b)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("led_yuz", me); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat_emis("led_yuz", lin(hex3(R["koyu"])), 1.2))


def mat_parlama_kis():
    """buyuk yuzeylerde beyaz yansima doygunlugu yiyor (30/31 dersi) -> zemin/yol specular dusuk"""
    for m in bpy.data.materials:
        if not m.use_nodes or "Principled BSDF" not in m.node_tree.nodes:
            continue
        ad = m.name.split(".")[0]
        if ad.startswith(("zemin", "cadde", "yol", "bulut")):
            b = m.node_tree.nodes["Principled BSDF"]
            b.inputs["Specular IOR Level"].default_value = 0.08
            b.inputs["Coat Weight"].default_value = 0.0


def serit_katmani(oyuncu):
    R = SERIT[oyuncu]
    sc = blok_sahnesi(SERIT_W, 1080, True)
    kam = kamera(sc)
    rnd = random.Random({"p1": 31, "p2": 32, "p3": 33}[oyuncu])
    isiklar()
    sehir(True, random.Random(34))
    serit_esyalari(oyuncu, R, rnd)
    kapi(R)
    Y, W_, H_ = KAP["y"], KAP["w"], KAP["h"]
    ic = W_ / 2
    bpy.context.view_layer.update()
    px = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-ic, Y, 0), (ic, Y, 0), (-ic, Y, H_), (ic, Y, H_))]
    xs = [p.x * SERIT_W for p in px]; ys = [(1 - p.y) * 1080 for p in px]
    YERLESIM["aciklik_" + oyuncu] = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
    mk = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-2.45, Y + 0.4, 0.8), (2.45, Y + 0.4, 0.8), (0, GECIS, 0))]
    d = {"minder_sol_x": round(mk[0].x * SERIT_W, 1), "minder_sag_x": round(mk[1].x * SERIT_W, 1),
         "minder_y": round((1 - mk[0].y) * 1080, 1), "gecis_y": round((1 - mk[2].y) * 1080, 1)}
    YERLESIM[ON_EK + "blok_" + oyuncu] = d
    YERLESIM[ON_EK + "yol"] = {"y_kapi": Y, "kam": KAM, "serit_w": SERIT_W}
    log("aciklik", oyuncu, YERLESIM["aciklik_" + oyuncu], d)
    mat_parlama_kis()
    yaz(sc, ON_EK + "serit-%s.png" % oyuncu)


def gok_katmani(ad):
    sc = blok_sahnesi(1920, 1080, False)
    kamera(sc)
    isiklar()
    sehir(False, random.Random(34))
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
    for o_ in ("p1", "p2", "p3"):
        serit_katmani(o_)
if YALNIZ in ("hepsi", "poz"):
    poz_maskeleri()
if YALNIZ in ("hepsi", "sahne"):
    gok_katmani("gok.png")
    for o_ in ("p1", "p2", "p3"):
        serit_katmani(o_)
        panel(o_)
json.dump(YERLESIM, open(os.path.join(CIKTI, "yerlesim.json"), "w"), indent=1)
log("bitti (blok)", YERLESIM.get("aciklik_p1"), YERLESIM.get("aciklik_p2"), YERLESIM.get("aciklik_p3"))
