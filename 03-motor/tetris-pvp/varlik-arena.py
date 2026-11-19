"""HUMAN TETRIS 33. video (REF-085 yapi, 1v1) - GUNDUZ ANTIK KUM ARENASI, CILALI 3D OYUN GORUNUMU. varlik.py calistirir (--mod arena).

Mekan kullanici karari (19 Kas 2026): antik kum arenasi; OUT ani: karakter kum yiginina yuvarlanir (dis tarafta kum yigini).
Onceki mekanlardan farki: tas tribunler + renkli tenteler + kalabalik, kemerli arena duvari, sutunlar + sarkan flamalar,
yolun ucunda zafer kemeri; gokte flama zincirleri, guvercin suruleri, ucusan renkli kagit (30 balon, 31 ucurtma tekrar edilmez).
§4 CILALI 3D OYUN GORUNUMU: canli doygun renk, tombul hatlar, cilali yuzey, gercek isik-golge-parlama (Cycles); foto dokusu yok,
isiksiz duz renk yuzey yok (mesale/ampul/LED haric). §8 SOLUK YASAK: kum bej DEGIL doygun turuncu-altin, tas sicak terrakota,
buyuk beyaz yuzey yok; tentelerde/flamalarda doygun SICAK + mavi/mor dengeler.
Telif (md. 16): genel antik arena kalibi; film/oyun setleri, arma, yazi, logo, marka yok.

Katmanlar buzul (31) ile ayni (motor 28/30 uyumu): gok.png = arena + gok, serit-p1/p2.png = oyuncunun yakin tas yolu + serit
esyalari + kapi. Isik iki katmanda ayni olsun diye butun sahne serit katmaninda da kurulur, uzak kisim holdout.

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
KEMER_Y = 58.0          # yolun ucunda zafer kemeri
ARENA_R = 70.0          # arena duvarinin (elips) yaricapi - y ekseninde
SERIT = {
    "p1": {"ana": "#1e8cff", "koyu": "#0a3fa8", "acik": "#8cc8ff"},
    "p2": {"ana": "#ff3aa8", "koyu": "#a8105e", "acik": "#ffa6d6"},
}
SICAK = ("#ff1e3c", "#ffd21e", "#ff7a14", "#a040ff", "#ff3ab4", "#2fd04a", "#1e8cff")
KUM = "#ff9a14"
TAS = ("#e8641e", "#f0842a", "#d84a1a", "#ffa63a")


# ------------------------------------------------------------------ sahne / isik
def arena_sahnesi(w, h, saydam):
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


def mat_kum(ad, renk1, renk2, olcek=0.35):
    """doygun turuncu-altin kum: iki ton gurultu + ince dalga (ruzgar izi) bump; mat"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    ns = nt.nodes.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value = olcek; ns.inputs["Detail"].default_value = 3
    nt.links.new(geo.outputs["Position"], ns.inputs["Vector"])
    rp = nt.nodes.new("ShaderNodeValToRGB")
    rp.color_ramp.elements[0].color = (*lin(hex3(renk1)), 1); rp.color_ramp.elements[1].color = (*lin(hex3(renk2)), 1)
    nt.links.new(ns.outputs["Fac"], rp.inputs[0]); nt.links.new(rp.outputs[0], b.inputs["Base Color"])
    wv = nt.nodes.new("ShaderNodeTexWave"); wv.inputs["Scale"].default_value = 1.2; wv.inputs["Distortion"].default_value = 4.0
    nt.links.new(geo.outputs["Position"], wv.inputs["Vector"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.25; bp.inputs["Distance"].default_value = 0.04
    nt.links.new(wv.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = 0.85; b.inputs["Specular IOR Level"].default_value = 0.08
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


def kum_mat():
    return M("kum", lambda: mat_kum("kum", "#ff7000" if KAPAK else "#ff8a0a", "#ff9800" if KAPAK else "#ffb01e"))   # 33 kapak olcum: doygunluk 0,652 < 0,677 -> kapakta daha doygun kum


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


def tribun(rnd):
    """arenayi saran (yolun iki yaninda ve arkada) basamakli tas tribun: her basamakta renkli seyirci kafalari + govde,
    ustte renkli tenteler (direk + egik kumas); elips yay, ondeki acik kisim kamerada"""
    adim = 7
    # 33 sahne 2: dondurulmus kutu basamaklar ortada cizilmedi (seyirci gokte asili kaldi) -> her basamak tek parca eliptik
    # halka mesh'i: on yuz (z0 -> z) + ust yuz (r -> r + 3.2); acilar -12..192 derece, y < 6 olan uclar kesilir
    E = lambda a, rr, zz: (math.cos(a) * rr * 1.35, math.sin(a) * rr, zz)
    for k in range(adim):
        r = ARENA_R + 6 + k * 3.2
        z = 3.2 + k * 2.2
        acilar = [math.radians(-12 + i * (204 / 120)) for i in range(121)]
        acilar = [a for a in acilar if math.sin(a) * r >= 6]
        v, f = [], []
        for a in acilar:
            v += [E(a, r, 0.0), E(a, r, z), E(a, r + 3.2, z)]
        for i in range(len(acilar) - 1):
            p, q = 3 * i, 3 * (i + 1)
            f.append([p, q, q + 1, p + 1]); f.append([p + 1, q + 1, q + 2, p + 2])
        me = bpy.data.meshes.new("basamak"); me.from_pydata(v, [], f); me.update()
        o = bpy.data.objects.new("basamak", me); bpy.context.collection.objects.link(o)
        o.data.materials.append(tas(TAS[k % len(TAS)]))
        o.modifiers.new("k", "SOLIDIFY").thickness = 0.3
        for i in range(40):
            a0 = math.radians(-12 + i * (204 / 40)); a1 = math.radians(-12 + (i + 1) * (204 / 40))
            am = (a0 + a1) / 2
            if math.sin(am) * r < 6:
                continue
            for j in range(2):                             # seyirci: renkli govde + ten rengi kafa
                if rnd.random() < 0.18:                        # gercek kalabalik: arada bos koltuk
                    continue
                # 33 sahne 1: satirlar ayni acida dizilince uzaktan dikey boncuk dizisi okundu -> satir basina kaydir + titret
                aj = a0 + (a1 - a0) * ((j + 0.5 + 0.5 * (k % 2)) / 2 + rnd.uniform(-0.12, 0.12))
                sx, sy = math.cos(aj) * (r + 1.4) * 1.35, math.sin(aj) * (r + 1.4)          # basamagin ustunde oturur
                g = kure((sx, sy, z + 0.7), 0.55, P(rnd.choice(SICAK), 0.4, 0.4), sub=1); g.scale = (1.0, 0.8, 1.3)
                kure((sx, sy, z + 1.7), 0.38, P(rnd.choice(("#ffcf9a", "#d8925a", "#a8643a", "#ffd8b0")), 0.5, 0.2), sub=1)
    # tenteler: tribun tepesinde direkler + egik renkli kumas seritleri (cizgili)
    r = ARENA_R + 6 + adim * 3.2 + 1
    for i in range(26):
        a = math.radians(-8 + i * (196 / 25))
        x, y = math.cos(a) * r * 1.35, math.sin(a) * r
        if y < 8:
            continue
        z = 3.2 + adim * 2.2
        boru((x, y, z), (x, y, z + 9), 0.35, P("#ffd21e", 0.3, 0.7))
        flama(x, y - 0.6, z + 9, 5.0, 2.4, SICAK[i % len(SICAK)])
        if i % 2 == 0:
            t_ = yuvarlak_kutu("tente", (x * 0.97, y * 0.97, z + 7.5), (10, 5, 0.25), P(SICAK[(i // 2) % len(SICAK)], 0.5, 0.2), egim=0.1, seg=1)
            t_.rotation_euler = (math.radians(-18), 0, a + math.pi / 2)


def arena_duvari(rnd):
    """kum alanini cevreleyen alcak kemerli duvar (podyum): terrakota bloklar, aralarda kemerler ve sarkan flamalar"""
    for i in range(48):
        a = math.radians(-14 + i * (208 / 47))
        x, y = math.cos(a) * ARENA_R * 1.35, math.sin(a) * ARENA_R
        if y < 4:
            continue
        o = yuvarlak_kutu("duvar", (x, y, 2.4), (6.6, 2.2, 4.8), tas(TAS[i % len(TAS)]), egim=0.3, seg=2)
        o.rotation_euler = (0, 0, a + math.pi / 2)
        yuvarlak_kutu("duvar_ust", (x, y, 5.0), (6.9, 2.6, 0.5), tas("#ffa63a"), egim=0.15, seg=1).rotation_euler = (0, 0, a + math.pi / 2)
        # kemerli nis: koyu doygun mor-mavi boslugun onunde (beyaz/siyah yok)
        n_ = yuvarlak_kutu("nis", (x - math.cos(a) * 1.15, y - math.sin(a) * 1.15, 2.0), (2.4, 0.2, 3.0), P("#3a1aa8", 0.6, 0.0), egim=0.6, seg=3)
        n_.rotation_euler = (0, 0, a + math.pi / 2)
        if i % 2 == 0:
            flama(x - math.cos(a) * 1.3, y - math.sin(a) * 1.3, 4.6, 3.2, 1.4, SICAK[(i // 2) % len(SICAK)])


def kalkan(xy_z, r, renk, yon=0.0):
    """yuvarlak kalkan: renkli disk + altin kenar halkasi + ortada altin kubbe (silah yok)"""
    x, y, z = xy_z
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=r * 0.18, location=(x, y, z), rotation=(math.pi / 2, 0, yon), vertices=32)
    o = bpy.context.active_object; o.data.materials.append(P(renk, 0.3, 0.8)); bpy.ops.object.shade_smooth()
    bpy.ops.mesh.primitive_torus_add(major_radius=r, minor_radius=r * 0.1, location=(x, y, z), rotation=(math.pi / 2, 0, yon))
    t_ = bpy.context.active_object; t_.data.materials.append(P("#ffd21e", 0.25, 0.8)); bpy.ops.object.shade_smooth()
    kure((x - math.sin(yon) * r * 0.1, y - math.cos(yon) * r * 0.1, z), r * 0.28, P("#ffd21e", 0.25, 0.8), sub=2)


def amfora(xy, boy, renk, z0=0.0):
    """tombul amfora: govde kure + boyun + iki kulp; doygun renkli cilali seramik, ortada altin bant"""
    x, y = xy
    g = kure((x, y, z0 + boy * 0.45), boy * 0.4, P(renk, 0.25, 0.8), sub=3); g.scale = (1.0, 1.0, 1.25)
    bpy.ops.mesh.primitive_cylinder_add(radius=boy * 0.13, depth=boy * 0.3, location=(x, y, z0 + boy * 0.98), vertices=20)
    bpy.context.active_object.data.materials.append(P(renk, 0.25, 0.8)); bpy.ops.object.shade_smooth()
    bpy.ops.mesh.primitive_torus_add(major_radius=boy * 0.4, minor_radius=boy * 0.04, location=(x, y, z0 + boy * 0.5))
    bpy.context.active_object.data.materials.append(P("#ffd21e", 0.25, 0.8)); bpy.ops.object.shade_smooth()
    for s in (-1, 1):
        bpy.ops.mesh.primitive_torus_add(major_radius=boy * 0.13, minor_radius=boy * 0.03, location=(x + s * boy * 0.2, y, z0 + boy * 0.88),
                                         rotation=(math.pi / 2, 0, 0))
        bpy.context.active_object.data.materials.append(P(renk, 0.25, 0.8)); bpy.ops.object.shade_smooth()


def mesale(xy, boy=1.6):
    """ayakli mesale: altin direk + kase + alev (kendi isigi, emission serbest)"""
    x, y = xy
    boru((x, y, 0), (x, y, boy), 0.06, P("#c88a1a", 0.3, 0.6))
    k = kure((x, y, boy), 0.2, P("#c88a1a", 0.3, 0.6), sub=2); k.scale = (1.3, 1.3, 0.6)
    a = kure((x, y, boy + 0.25), 0.18, M("alev", lambda: mat_emis("alev", lin(hex3("#ffb21a")), 8.0)), sub=2); a.scale = (1.0, 1.0, 1.8)


def zafer_kemeri(rnd):
    """yolun ucunda buyuk zafer kemeri: uc acikli, sutunlu, ustte renkli flamalar + altin dev kalkanlar"""
    y = KEMER_Y
    kemer(0, y, 9.0, 12.0, "#f0842a", kalin=3.0)
    for s in (-1, 1):
        kemer(s * 12.5, y + 0.5, 5.0, 8.0, "#e8641e", kalin=2.4)
        for dx in (6.8, 18.5):
            sutun((s * dx, y - 2.2), 13.0, "#ffa63a", r=0.9)
        flama(s * 6.8, y - 3.4, 13.5, 6.0, 2.2, SICAK[(s + 1) // 2])
        flama(s * 18.5, y - 3.4, 13.5, 6.0, 2.2, SICAK[2 + (s + 1) // 2])
        kalkan((s * 12.5, y - 1.4, 13.8), 2.0, ("#1e8cff", "#ff3aa8")[(s + 1) // 2])
    yuvarlak_kutu("kemer_ust", (0, y, 19.5), (40, 3.6, 3.0), tas("#ffa63a"), egim=0.3, seg=2)
    yuvarlak_kutu("kemer_ust2", (0, y, 21.6), (30, 3.0, 1.4), tas("#e8641e"), egim=0.2, seg=2)
    for k in range(7):                                     # catida flama direkleri
        x = -15 + k * 5
        boru((x, y, 22.3), (x, y, 28.5), 0.18, P("#ffd21e", 0.3, 0.7))
        fl = yuvarlak_kutu("bayrak", (x + 1.4, y, 27.6), (2.8, 0.06, 1.6), P(SICAK[k % len(SICAK)], 0.45, 0.3), egim=0.05, seg=1)


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


def flama_zinciri(p0, p1, sark, n, rnd):
    """iki nokta arasinda sarkan ip + ucgen renkli bayraklar (sarkma parabol)"""
    p0, p1 = Vector(p0), Vector(p1)
    onceki = p0
    for i in range(1, n + 1):
        t = i / n
        q = p0.lerp(p1, t); q.z -= sark * 4 * t * (1 - t)
        boru(tuple(onceki), tuple(q), 0.03, M("ip", lambda: mat_pbr("ip", "#ffd21e", 0.5)))
        m = onceki.lerp(q, 0.5); yon = (q - onceki).normalized()
        a, b = m - yon * 0.45, m + yon * 0.45
        uc = m + Vector((0, 0, -1.1))
        me = bpy.data.meshes.new("ucgen"); me.from_pydata([tuple(a), tuple(b), tuple(uc)], [], [[0, 1, 2]]); me.update()
        o = bpy.data.objects.new("ucgen", me); bpy.context.collection.objects.link(o)
        o.data.materials.append(P(SICAK[(i + rnd.randint(0, 6)) % len(SICAK)], 0.45, 0.3)); o.modifiers.new("k", "SOLIDIFY").thickness = 0.03
        onceki = q


def gok_ogeleri(rnd):
    """ekran dolu kurali (md. 7): flama zincirleri tribunden tribune, guvercin suruleri, ucusan renkli kagit (konfeti),
    uzakta birkac kucuk bulut. 30 balon / 31 ucurtma tekrar edilmez."""
    for (x, y, z, o) in ((-170, 300, 80, 14), (160, 290, 74, 13), (-260, 360, 120, 18), (250, 360, 116, 18)):
        bulut((x, y, z), o, rnd)
    for (x0, x1, y, z, s) in ((-60, 60, 70, 34, 6), (-80, 80, 90, 44, 8), (-40, 40, 40, 22, 4), (-100, -20, 110, 50, 6), (20, 100, 110, 50, 6),
                              (-30, 30, 28, 17, 3)):
        flama_zinciri((x0, y, z), (x1, y, z), s, int((x1 - x0) / 2.2), rnd)
    for k in range(22):
        kus((rnd.uniform(-30, 30), rnd.uniform(30, 70), rnd.uniform(10, 26)), rnd.uniform(0.6, 0.9),
            rnd.choice(("#ffffff", "#ffe8b0", "#c8e0ff")), rnd)
    for k in range(70):                                    # ucusan renkli kagit (konfeti), cilali
        p = kure((rnd.uniform(-14, 14), rnd.uniform(12, 34), rnd.uniform(1.5, 10.0)), rnd.uniform(0.07, 0.13),
                 P(rnd.choice(SICAK), 0.3, 0.8), sub=1)
        p.scale = (1.6, 0.3, 1.0); p.rotation_euler = (rnd.uniform(0, 3), rnd.uniform(0, 3), rnd.uniform(0, 3))


# ------------------------------------------------------------------ ARENA (iki katmanda; serit sahnesinde uzak kisim holdout)
def arena(serit_modu, rnd):
    _MAT.clear()
    kum = kum_mat()
    duz("zemin_yakin", -120, 120, -4, GECIS, 0, kum)
    duz("zemin_uzak", -200, 200, GECIS, 400, 0, kum)
    yol = mat_tas_doseme("tas_yol", "#e8641e", "#f0842a", ara="#6a2008")
    duz("tas_yol_uzak", -2.6, 2.6, GECIS, KEMER_Y - 2, 0.006, yol)
    for s in (-1, 1):                                      # uzak yol boyunca sutun sirasi + flamalar + mesaleler
        y = GECIS + 3
        k = 0
        while y < KEMER_Y - 6:
            zt = sutun((s * 4.2, y), 3.2, TAS[k % len(TAS)], r=0.35)
            flama(s * 4.2, y - 0.45, zt - 0.1, 1.6, 0.7, SICAK[(k + (s > 0) * 3) % len(SICAK)])
            mesale((s * 3.3, y + 2.5), 1.3)
            y += 5.0; k += 1
    # kum alaninda: kalkan yiginlari, amforalar, renkli davullar, kum tepecikleri
    for k in range(18):
        x = rnd.choice((-1, 1)) * rnd.uniform(7, 60); y = rnd.uniform(GECIS + 2, ARENA_R * 0.8)
        amfora((x, y), rnd.uniform(1.0, 1.6), rnd.choice(SICAK))
    for k in range(14):
        x = rnd.choice((-1, 1)) * rnd.uniform(7, 60); y = rnd.uniform(GECIS + 2, ARENA_R * 0.8)
        kalkan((x, y, 1.0), rnd.uniform(0.8, 1.2), rnd.choice(SICAK), yon=rnd.uniform(-0.6, 0.6))
    for k in range(30):
        x = rnd.choice((-1, 1)) * rnd.uniform(6, 90); y = rnd.uniform(GECIS + 1, ARENA_R * 0.9)
        t_ = kure((x, y, -0.4), rnd.uniform(1.0, 2.6), kum, sub=2); t_.scale = (1.8, 1.0, 0.4)
    arena_duvari(rnd)
    tribun(rnd)
    zafer_kemeri(rnd)
    gok_ogeleri(rnd)
    if serit_modu:
        for o in bpy.data.objects:
            if o.type == "MESH" and o.name.split(".")[0] not in ("zemin_yakin",):
                o.is_holdout = True


# ------------------------------------------------------------------ SERIT: oyuncu tas yolu + kalkan siniri + OUT kum yigini + kapi
def serit_esyalari(oyuncu, R, rnd):
    s_dis = -1 if oyuncu == "p1" else 1
    # 31 dersi: tek tonlu sahnede renklilik tutmadi -> serit tas yolu oyuncu renginde (P1 mavi, P2 pembe tas)
    if oyuncu == "p1":
        yol = mat_tas_doseme("serit_yol", "#0a5cff", "#1a7cff", ara="#042a7a")
    else:
        yol = mat_tas_doseme("serit_yol", "#ff0a8c", "#ff14a0", ara="#6a0640")
    duz("serit_yol", -1.6, 1.6, -4, GECIS, 0.006, yol)
    bm = M("sinir" + R["ana"], lambda: mat_pbr("sinir" + R["ana"], R["ana"], 0.25, kaplama=0.8))
    for x in (-1.75, 1.75):                                # serit siniri: oyuncu renginde cilali tas bloklar
        y = -3.6
        while y < KAP["y"] - 0.8:
            yuvarlak_kutu("sinir", (x, y, 0.16), (0.34, 0.62, 0.32), bm, egim=0.08, seg=2)
            y += 0.75
    for y in (1.0, 3.6, 6.2):                              # dis sinirda oyuncu renginde kalkanlar
        kalkan((s_dis * 1.95, y, 0.55), 0.38, R["ana"], yon=s_dis * 1.2)
    boya = mat_pbr("ok_" + oyuncu, "#ffd21e", 0.35, kaplama=0.6)
    for y in (4.9, 6.4):                                   # yolda boyali yon oklari (seri sabiti; oyuncu renginde yolda sari)
        nok = [(-0.75, y - 0.45), (0, y), (0.75, y - 0.45), (0.75, y - 0.75), (0, y - 0.3), (-0.75, y - 0.75)]
        me = bpy.data.meshes.new("ok"); me.from_pydata([(a, b, 0.014) for a, b in nok], [], [list(range(6))]); me.update()
        o = bpy.data.objects.new("ok", me); bpy.context.collection.objects.link(o); o.data.materials.append(boya)
        o.modifiers.new("k", "SOLIDIFY").thickness = 0.02
    # OUT ani: dis tarafta kum yigini (tombul tepe + etrafinda kum topaklari; karakter buraya yuvarlanir)
    cx, cy = s_dis * 2.95, 5.2
    kum = kum_mat()
    y_ = kure((cx, cy, -0.35), 1.0, kum, sub=3); y_.scale = (1.3, 1.9, 0.95)
    for k in range(9):
        a = rnd.uniform(0, 6.28)
        t_ = kure((cx + 1.4 * math.cos(a), cy + 2.0 * math.sin(a), -0.05), rnd.uniform(0.2, 0.4), kum, sub=2); t_.scale = (1.4, 1.2, 0.5)
    # dis tarafta yakin esyalar: amforalar, kalkan yigini, renkli davul, mesale, kum tepecikleri
    for k in range(4):
        amfora((s_dis * rnd.uniform(4.6, 8.5), rnd.uniform(1.0, 10.0)), rnd.uniform(0.8, 1.2), rnd.choice(SICAK))
    for k in range(3):
        kalkan((s_dis * (5.0 + 0.4 * k), 8.6 + 0.3 * k, 0.6 + 0.05 * k), 0.6, SICAK[(k + (oyuncu == "p2") * 3) % len(SICAK)], yon=s_dis * 0.5)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=0.7, location=(s_dis * 4.2, 2.6, 0.35), vertices=24)
    d_ = bpy.context.active_object; d_.data.materials.append(P("#ff1e3c" if oyuncu == "p1" else "#2fd04a", 0.3, 0.7)); bpy.ops.object.shade_smooth()
    bpy.ops.mesh.primitive_torus_add(major_radius=0.5, minor_radius=0.05, location=(s_dis * 4.2, 2.6, 0.7))
    bpy.context.active_object.data.materials.append(P("#ffd21e", 0.25, 0.8))
    for k in range(8):
        t2 = kure((s_dis * rnd.uniform(6, 20), rnd.uniform(-3, GECIS), -0.3), rnd.uniform(0.7, 1.4), kum, sub=2)
        t2.scale = (1.6, 1.0, 0.45)
    for yy in (2.5, 7.4):                                  # ic tarafta (hakem yeri) kucuk mesaleler
        mesale((-s_dis * 2.45, yy), 1.2)


def kapi(R):
    """tas sutunlu kapi: iki tombul sutun (terrakota + altin baslik), oyuncu renginde bant + flama, ustte kiris + ucgen alinlik,
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
    yuvarlak_kutu("kiris", (0, Y, H_ + K / 2), (W_ + 2 * K + 0.3, K, K), tas("#ffa63a"), egim=0.1, seg=3)
    yuvarlak_kutu("kiris_bant", (0, Y - K / 2 - 0.02, H_ + K / 2), (W_ + 2 * K, 0.06, 0.18), boya, egim=0.02, seg=1)
    me = bpy.data.meshes.new("alinlik"); a = W_ / 2 + K; z0 = H_ + K
    me.from_pydata([(-a, Y - K / 2, z0), (a, Y - K / 2, z0), (0, Y - K / 2, z0 + 0.6)], [], [[0, 1, 2]]); me.update()
    o = bpy.data.objects.new("alinlik", me); bpy.context.collection.objects.link(o); o.data.materials.append(tas("#e8641e"))
    o.modifiers.new("k", "SOLIDIFY").thickness = -K
    ampul = M("ampul", lambda: mat_emis("ampul", lin(hex3("#ffe08a")), 5.0))
    for i in range(9):
        xx = -W_ / 2 + W_ * i / 8
        kure((xx, Y - K / 2 - 0.12, H_ - 0.35 - 0.12 * math.sin(math.pi * i / 8)), 0.07, ampul, sub=2)
    # 33 sahne 1: alinlik tabelayi ortuyordu -> tabela alinligin tepesinin ustune
    yuvarlak_kutu("tabela", (0, Y - 0.3, H_ + K + 1.15), (W_ * 0.85, 0.2, 0.7), mat_pbr("tabela", "#15171a", 0.35, metal=0.4), egim=0.05, seg=3)
    me = bpy.data.meshes.new("led_yuz"); a, b = W_ * 0.4, 0.28; z0 = H_ + K + 1.15
    me.from_pydata([(-a, Y - 0.41, z0 - b), (a, Y - 0.41, z0 - b), (a, Y - 0.41, z0 + b), (-a, Y - 0.41, z0 + b)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("led_yuz", me); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat_emis("led_yuz", lin(hex3(R["koyu"])), 1.2))
    for s in (-1, 1):                                      # sutun diplerinde amfora cifti
        amfora((s * (xk + 0.75), Y - 0.5), 0.8, SICAK[(s + 1) // 2 + 2])


def mat_parlama_kis():
    """buyuk yuzeylerde (kum, yol, tas) beyaz yansima doygunlugu yiyor -> specular/coat dusuk (30/31 dersi)"""
    for m in bpy.data.materials:
        if not m.use_nodes or "Principled BSDF" not in m.node_tree.nodes:
            continue
        ad = m.name.split(".")[0]
        if ad.startswith(("kum", "tas_yol", "serit_yol", "tas#")):
            b = m.node_tree.nodes["Principled BSDF"]
            b.inputs["Specular IOR Level"].default_value = 0.06
            b.inputs["Coat Weight"].default_value = 0.0
            if ad.startswith(("tas_yol", "serit_yol")):
                b.inputs["Roughness"].default_value = 0.5


def serit_katmani(oyuncu):
    R = SERIT[oyuncu]
    sc = arena_sahnesi(960, 1080, True)
    kam = kamera(sc)
    rnd = random.Random(33 + (oyuncu == "p2"))
    isiklar()
    arena(True, random.Random(33))
    serit_esyalari(oyuncu, R, rnd)
    kapi(R)
    Y, W_, H_ = KAP["y"], KAP["w"], KAP["h"]
    ic = W_ / 2
    bpy.context.view_layer.update()
    px = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-ic, Y, 0), (ic, Y, 0), (-ic, Y, H_), (ic, Y, H_))]
    xs = [p.x * 960 for p in px]; ys = [(1 - p.y) * 1080 for p in px]
    YERLESIM["aciklik_" + oyuncu] = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
    # OUT ani: kum yigininin ekrandaki yeri; motor anahtar duzeni korunur (minder = kum yigini)
    mk = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-2.95, 5.2, 0.4), (2.95, 5.2, 0.4), (0, GECIS, 0))]
    d = {"minder_sol_x": round(mk[0].x * 960, 1), "minder_sag_x": round(mk[1].x * 960, 1),
         "minder_y": round((1 - mk[0].y) * 1080, 1), "gecis_y": round((1 - mk[2].y) * 1080, 1)}
    for on in ("salon_", "plaj_", "orman_", "lale_", "buzul_", "arena_"):
        YERLESIM[on + oyuncu] = d
    YERLESIM["yol"] = {"y_kapi": Y, "genislik": YOL_YARI * 2, "kam": KAM, "serit_w": 960}
    log("aciklik", oyuncu, YERLESIM["aciklik_" + oyuncu], d)
    mat_parlama_kis()
    yaz(sc, ON_EK + "serit-%s.png" % oyuncu)


def gok_katmani(ad):
    sc = arena_sahnesi(1920, 1080, False)
    kamera(sc)
    isiklar()
    arena(False, random.Random(33))
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
log("bitti (arena)", YERLESIM.get("aciklik_p1"), YERLESIM.get("aciklik_p2"))
