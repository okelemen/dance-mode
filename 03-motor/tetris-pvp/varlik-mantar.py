"""HUMAN TETRIS 36. video (REF-088 yapi, 1P SOLO) - GUNDUZ DEV MANTAR ORMANI, CILALI 3D OYUN GORUNUMU, TEK serit.
varlik.py calistirir (--mod mantar). Iskelet varlik-balon.py (35, tek serit) - katmanlar, kamera, yerlesim anahtarlari ayni
(tek serit motoru 32'nin bekledigi aciklik_p1 / ampul_p1 / dag / yol).

Mekan kullanici karari (20 Kas 2026, A): gunes huzmeli orman, farkli boy ve renkte dev mantarlar, yosun ve cicek ortusu,
ucusan polen/sporlar, kelebekler. OUT ani: karakter pistin yanindaki yumusak dev mantar sapkasina duser, seker, spor bulutu.
Telif (md. 16): genel masal ormani; taninir oyun mantari (beyaz benekli kirmizi karakter mantari, yuzlu mantar) yok ->
benekler krem-sari, kirmizi sapka az ve beneksiz; mantarlarda yuz/goz yok.
§4 CILALI 3D OYUN GORUNUMU: doygun renk, tombul hatlar, parlak sapka (coat), gercek isik-golge (Cycles); foto dokusu yok.
§8 SOLUK YASAK: buyuk beyaz yuzey yok -> mantar saplari sicak krem-seftali, yosun doygun yesil, gok koyu doygun mavi tepe.
Ekran dolu (Masaustu md. 7): gokte dev mantar sapkalari (yakin-orta-uzak), gunes huzmeleri, sporlar, kelebekler; zemin ufka kadar dolu.
"""

import random
YERLESIM.clear()
KAPAK = YALNIZ == "kapak"
POZLAMA = float(arg("--pozlama", arg("--kapak-pozlama", "0")))
GUNES = float(arg("--gunes", "4.0"))
ON_EK = "kapak-" if KAPAK else ""
KAP = {"y": 8.6, "w": 7.4, "h": 3.7, "kalin": 0.55}       # tek serit motoru (27/28/35) ile ayni olcu
KAM = {"z": 2.3, "egim": 5.0, "lens": 18.0, "sensor": 24.0}
if KAPAK:
    KAM.update({"z": float(arg("--kapak-z", "2.0")), "egim": float(arg("--kapak-egim", "3.0")), "lens": float(arg("--kapak-lens", "16.0"))})
PIST = 3.9
GECIS = 11.5
SAPKA = ("#ff2a3a", "#ff7a10", "#8a3aff", "#ffc21a", "#ff3aa8", "#10c8d0", "#1e8cff", "#20c850")
CANLI = ("#ff2a3a", "#ffc21a", "#1e8cff", "#20c850", "#ff3aa8", "#ff7a10", "#8a3aff", "#10c8d0")
SAP, BENEK = "#ffcf8a", "#fff08a"                         # sap sicak krem-seftali (beyaz degil), benek krem-sari
YOSUN, YOSUN_K = "#2ec83a", "#109a2a"
GOK_ALT, GOK_ORTA, GOK_UST = "#7ae8ff", "#18a8ff", "#0040e0"
TAS = ("#ff9a3a", "#e86a1a")
if KAPAK and arg("--kapak-doygun", "0") != "0":        # kapak olcumu 1 (21 Kas): doygunluk 0,655 / renklilik 0,573 < REF-088 0,742 / 0,582
    SAP, BENEK = "#ffa418", "#ffe41a"                   # -> buyuk alanlar Blender'da doygun (soluk krem sap en buyuk dusuk-S alan); 2B boyama yok (md. 21)
    YOSUN, YOSUN_K = "#10d81a", "#068a10"
    GOK_ALT, GOK_ORTA, GOK_UST = "#10c0ff", "#0080ff", "#0028d8"
    TAS = ("#ff7a08", "#e04800")


# ------------------------------------------------------------------ sahne / isik
def orman_sahnesi(w, h, saydam):
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
    el[0].position = 0.0; el[0].color = (*lin(hex3(GOK_ALT)), 1)
    el[1].position = 0.42; el[1].color = (*lin(hex3(GOK_UST)), 1)
    e2 = el.new(0.13); e2.color = (*lin(hex3(GOK_ORTA)), 1)
    nt.links.new(sp.outputs["Z"], rp.inputs[0])
    lp = nt.nodes.new("ShaderNodeLightPath")
    bg_k = nt.nodes.new("ShaderNodeBackground"); bg_k.inputs[1].default_value = 1.0
    bg_i = nt.nodes.new("ShaderNodeBackground"); bg_i.inputs[1].default_value = 0.35
    bg_i.inputs[0].default_value = (*lin(hex3("#c8f0b0")), 1)     # orman ortam isigi: hafif yesil (gri golge yok)
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
    # sabah gunesi: arkadan-ustten, sapkalarda parlak kenar + yosunda uzun golge
    bpy.ops.object.light_add(type="SUN", location=(0, 0, 30))
    g = bpy.context.active_object; g.data.energy = GUNES; g.data.angle = math.radians(2.0)
    g.data.color = lin(hex3("#fff2c8"))
    g.rotation_euler = Vector((-0.35, 0.65, -0.68)).to_track_quat("-Z", "Y").to_euler()


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


def mat_yosun(ad="yosun"):
    """yosun ortusu: iki yesil noise karisimi + kabartma; dusuk parlaklik ama doygun"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    ns = nt.nodes.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value = 1.2; ns.inputs["Detail"].default_value = 5
    nt.links.new(geo.outputs["Position"], ns.inputs["Vector"])
    rp = nt.nodes.new("ShaderNodeValToRGB"); el = rp.color_ramp.elements
    el[0].position = 0.35; el[0].color = (*lin(hex3(YOSUN_K)), 1)
    el[1].position = 0.7; el[1].color = (*lin(hex3(YOSUN)), 1)
    nt.links.new(ns.outputs["Fac"], rp.inputs[0]); nt.links.new(rp.outputs[0], b.inputs["Base Color"])
    n2 = nt.nodes.new("ShaderNodeTexNoise"); n2.inputs["Scale"].default_value = 18.0; n2.inputs["Detail"].default_value = 8
    nt.links.new(geo.outputs["Position"], n2.inputs["Vector"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.6
    nt.links.new(n2.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = 0.85
    b.inputs["Sheen Weight"].default_value = 0.4; b.inputs["Sheen Tint"].default_value = (*lin(hex3("#b8ff60")), 1)
    return m


def mat_tas(ad="tas"):
    """pist: yuvarlak tas doseme (voronoi), sicak turuncu taslar + aralarda yosun derzi"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    vr = nt.nodes.new("ShaderNodeTexVoronoi"); vr.feature = "DISTANCE_TO_EDGE"; vr.inputs["Scale"].default_value = 0.9
    nt.links.new(geo.outputs["Position"], vr.inputs["Vector"])
    v2 = nt.nodes.new("ShaderNodeTexVoronoi"); v2.inputs["Scale"].default_value = 0.9
    nt.links.new(geo.outputs["Position"], v2.inputs["Vector"])
    rt = nt.nodes.new("ShaderNodeValToRGB"); el = rt.color_ramp.elements                    # tas basina ton farki
    el[0].position = 0.0; el[0].color = (*lin(hex3(TAS[0])), 1); el[1].position = 1.0; el[1].color = (*lin(hex3(TAS[1])), 1)
    nt.links.new(v2.outputs["Color"], rt.inputs[0])
    dz = nt.nodes.new("ShaderNodeMath"); dz.operation = "LESS_THAN"; dz.inputs[1].default_value = 0.06
    nt.links.new(vr.outputs["Distance"], dz.inputs[0])
    mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"; nt.links.new(dz.outputs[0], mx.inputs["Factor"])
    nt.links.new(rt.outputs[0], mx.inputs[6]); mx.inputs[7].default_value = (*lin(hex3(YOSUN_K)), 1)
    nt.links.new(mx.outputs[2], b.inputs["Base Color"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.7
    nt.links.new(vr.outputs["Distance"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = 0.4; b.inputs["Coat Weight"].default_value = 0.3; b.inputs["Coat Roughness"].default_value = 0.12
    return m


_SMAT = {}


def mat_sapka(renk, benek):
    """mantar sapkasi: parlak doygun renk (coat) + istege bagli krem-sari benek (nesne uzayi voronoi)"""
    key = (renk, benek)
    if key in _SMAT:
        return _SMAT[key]
    m = bpy.data.materials.new("sapka" + str(len(_SMAT))); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    if benek:
        tc = nt.nodes.new("ShaderNodeTexCoord")
        vr = nt.nodes.new("ShaderNodeTexVoronoi"); vr.inputs["Scale"].default_value = 3.2; vr.inputs["Randomness"].default_value = 0.8
        nt.links.new(tc.outputs["Object"], vr.inputs["Vector"])
        lt = nt.nodes.new("ShaderNodeMath"); lt.operation = "LESS_THAN"; lt.inputs[1].default_value = 0.12
        nt.links.new(vr.outputs["Distance"], lt.inputs[0])
        mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"; nt.links.new(lt.outputs[0], mx.inputs["Factor"])
        mx.inputs[6].default_value = (*lin(hex3(renk)), 1); mx.inputs[7].default_value = (*lin(hex3(BENEK)), 1)
        nt.links.new(mx.outputs[2], b.inputs["Base Color"])
    else:
        b.inputs["Base Color"].default_value = (*lin(hex3(renk)), 1)
    b.inputs["Roughness"].default_value = 0.3
    b.inputs["Coat Weight"].default_value = 0.6; b.inputs["Coat Roughness"].default_value = 0.08
    b.inputs["Subsurface Weight"].default_value = 0.15; b.inputs["Subsurface Radius"].default_value = (1.0, 0.4, 0.3)
    _SMAT[key] = m
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


# ------------------------------------------------------------------ ogeler
_SAP = {}


def mantar(taban, R, H, rnd, renk=None, benek=None, egik=0.0):
    """mantar: hafif konik tombul sap + kubbe sapka (kure 1:1:0,55) + alt yuzde koyu lamel diski. R = sapka yaricapi, H = sap boyu"""
    x, y, z = taban
    if renk is None:
        renk = rnd.choice(SAPKA)
    if benek is None:
        benek = renk != "#ff2a3a" and rnd.random() < 0.55          # kirmizi sapka beneksiz (taninir oyun mantari yok)
    if "sap" not in _SAP:
        _SAP["sap"] = mat_pbr("sap", SAP, 0.45, kaplama=0.2, ss=0.2)
        _SAP["lamel"] = mat_pbr("lamel", "#c86a3a", 0.7)
    rs = R * rnd.uniform(0.22, 0.3)
    s = silindir((x, y, z), rs * 1.25, H, _SAP["sap"], v=32, r2=rs * 0.9)
    s.rotation_euler = (egik * 0.6, egik, 0)
    tx, ty, tz = x + math.sin(egik) * H, y - math.sin(egik * 0.6) * H, z + H * math.cos(egik)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=R, location=(tx, ty, tz), segments=48, ring_count=24)
    c = bpy.context.active_object; c.scale = (1.0, 1.0, rnd.uniform(0.5, 0.62)); c.rotation_euler = (egik * 0.6, egik, rnd.uniform(0, 3.1))
    c.data.materials.append(mat_sapka(renk, benek)); bpy.ops.object.shade_smooth()
    bpy.ops.mesh.primitive_cylinder_add(radius=R * 0.93, depth=0.02 * R, location=(tx, ty, tz - 0.04 * R), vertices=48)
    l = bpy.context.active_object; l.rotation_euler = (egik * 0.6, egik, 0); l.data.materials.append(_SAP["lamel"])
    return c


def mantar_kumesi(merkez, olcek, rnd, n=5):
    x, y, z = merkez
    for i in range(n):
        R = olcek * rnd.uniform(0.35, 1.0)
        mantar((x + rnd.uniform(-1.2, 1.2) * olcek, y + rnd.uniform(-0.8, 0.8) * olcek, z), R, R * rnd.uniform(0.9, 1.6), rnd,
               egik=rnd.uniform(-0.18, 0.18))


def cicek(x, y, z, r, renk):
    """kucuk cicek: 5 yaprak kure + sari gobek"""
    ym = mat_pbr("cy" + renk, renk, 0.35, kaplama=0.4)
    for k in range(5):
        a = k * 2 * math.pi / 5
        p = kure((x + math.cos(a) * r, y + math.sin(a) * r * 0.5, z), r * 0.6, ym); p.scale = (1, 1, 0.4)
    kure((x, y, z + r * 0.15), r * 0.45, mat_pbr("cgobek", "#ffc21a", 0.3, kaplama=0.5))


def kelebek(x, y, z, s, renk, rnd):
    km = mat_pbr("kel" + renk, renk, 0.3, kaplama=0.5)
    for d in (-1, 1):
        me = bpy.data.meshes.new("kanat")
        me.from_pydata([(0, 0, 0), (d * s, -0.2 * s, 0.6 * s), (d * 0.9 * s, 0, -0.5 * s)], [], [[0, 1, 2]]); me.update()
        o = bpy.data.objects.new("kanat", me); bpy.context.collection.objects.link(o); o.data.materials.append(km)
        o.location = (x, y, z); o.rotation_euler = (0.3, d * 0.5, rnd.uniform(0, 6.28))
        o.modifiers.new("k", "SOLIDIFY").thickness = 0.01


def sporlar(rnd, n, x_gen, y0, y1, z0, z1, kac=0.0):
    sm = mat_emis("spor", lin(hex3("#fff27a")), 3.0)
    for _ in range(n):
        x = rnd.uniform(-x_gen, x_gen); y = rnd.uniform(y0, y1); z = rnd.uniform(z0, z1)
        if abs(x) < kac and y < y0 + 15:
            continue
        kure((x, y, z), rnd.uniform(0.05, 0.12) * (1 + (y - y0) / 40), sm)


def huzme(x, y, z, uz, gen):
    """gunes huzmesi: ince, yari saydam sicak isik serit (yukaridan egik), gogu dolu gosterir"""
    m = bpy.data.materials.new("huzme"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs[0].default_value = (*lin(hex3("#fff6b0")), 1); em.inputs[1].default_value = 1.2
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mx = nt.nodes.new("ShaderNodeMixShader"); mx.inputs[0].default_value = 0.22
    nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(mx.outputs[0], o.inputs[0])
    bpy.ops.mesh.primitive_plane_add(size=1, location=(x, y, z))
    p = bpy.context.active_object; p.scale = (gen, uz, 1); p.rotation_euler = (math.radians(90), math.radians(-28), 0)
    p.data.materials.append(m); p.visible_shadow = False


def zemin(rnd, y0, y1, x_gen, z=0.0, kac=0.0):
    """yosun zemin: genis duzlem + uzaga dogru tepecikler (ufka kadar dolu)"""
    ym = mat_yosun()
    me = bpy.data.meshes.new("zemin")
    me.from_pydata([(-x_gen, y0, z), (x_gen, y0, z), (x_gen, y1, z), (-x_gen, y1, z)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("zemin", me); bpy.context.collection.objects.link(o); o.data.materials.append(ym)
    y = y0 + 6
    while y < y1:
        s = 1.0 + (y - y0) / 30.0
        x = -x_gen + rnd.uniform(0, 8 * s)
        while x < x_gen:
            r = rnd.uniform(2.5, 4.5) * s
            if abs(x) - r < kac:
                x += 8 * s; continue
            t = kure((x, y, z - r * 0.55), r, ym, sub=2); t.scale = (1.6, 1.0, 0.7)
            x += 8 * s * rnd.uniform(0.8, 1.3)
        y += 9 * s
    return ym


# ------------------------------------------------------------------ MEKAN (her iki katmanda; serit sahnesinde uzak kisim holdout)
def mekan(serit_modu, rnd):
    _SMAT.clear(); _SAP.clear()          # Actions 44714901512 dersi: ikinci katmanda bos_sahne eski malzemeleri siliyor
    ym = mat_yosun("yakin_yosun")
    me = bpy.data.meshes.new("yakin_zemin")
    me.from_pydata([(-60, -4, -0.02), (60, -4, -0.02), (60, GECIS, -0.02), (-60, GECIS, -0.02)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("yakin_zemin", me); bpy.context.collection.objects.link(o); o.data.materials.append(ym)
    # yakin kenar: pistin iki yaninda alcak mantar kumeleri + cicekler (koridor bos; OUT sapkasinin yerini kapatmaz)
    for s in (-1, 1):
        for (x, y, k) in ((9.0, 1.0, 1.1), (12.5, 4.5, 1.5), (8.4, 9.5, 1.0), (16, 8, 2.0), (20, 2, 2.4)):
            mantar_kumesi((s * x, y, 0), k, rnd, n=4)
        for i in range(26):
            cicek(s * rnd.uniform(PIST + 1.0, 22), rnd.uniform(-3, GECIS), 0.08, rnd.uniform(0.12, 0.22), CANLI[i % 8])
    for o in bpy.data.objects:
        if o.type == "MESH":
            o["yakin"] = 1
    zemin(rnd, GECIS, 420, 420, kac=PIST + 2)
    # dev mantarlar: orta-uzak, sapkalari gogu doldurur; kapinin ustu ve tam orta koridor acik kalir
    for (x, y, R, H) in ((-14, 22, 4.5, 9), (16, 26, 5.5, 12), (-26, 36, 7, 16), (28, 42, 6.5, 10), (-8, 50, 5, 22),
                         (10, 58, 6, 26), (-40, 60, 9, 13), (44, 70, 10, 20), (-22, 80, 8, 32), (26, 90, 9, 36),
                         (-62, 100, 12, 22), (66, 110, 13, 15), (0, 130, 10, 48), (-48, 140, 12, 44), (52, 150, 13, 50),
                         (-90, 170, 16, 18), (96, 185, 17, 30), (-20, 210, 14, 64), (34, 230, 15, 72), (-70, 250, 18, 76)):
        mantar((x, y, 0), R, H, rnd, egik=rnd.uniform(-0.12, 0.12))
    for _ in range(30):                                               # uzak kucuk mantar ormani (ufuk dolu)
        mantar((rnd.uniform(-300, 300), rnd.uniform(260, 480), 0), rnd.uniform(10, 22), rnd.uniform(15, 60), rnd)
    # sahne 1 (Actions 44873050910): gunes huzmeleri gokte beyaz cubuk gibi okundu -> kaldirildi; orta plan cayir bos kaliyordu
    # -> orta-uzak zemine mantar kumeleri + cicek tarlasi (koridor ve kapinin arkasi acik)
    for _ in range(46):
        x = rnd.choice((-1, 1)) * rnd.uniform(7, 90); y = rnd.uniform(GECIS + 2, 120)
        mantar_kumesi((x, y, 0), rnd.uniform(0.9, 2.6) * (1 + y / 60), rnd, n=rnd.randint(3, 5))
    for i in range(260):
        y = rnd.uniform(GECIS, 90); x = rnd.choice((-1, 1)) * rnd.uniform(PIST + 2.5, 70)
        cicek(x, y, 0.08, rnd.uniform(0.25, 0.5) * (1 + y / 40), CANLI[i % 8])
    sporlar(rnd, 160, 40, 6, 70, 1.0, 26, kac=6)
    for i in range(18):
        kelebek(rnd.uniform(-24, 24), rnd.uniform(6, 50), rnd.uniform(2.5, 14), rnd.uniform(0.35, 0.6), CANLI[i % 8], rnd)
    if serit_modu:
        for o in bpy.data.objects:
            if o.type == "MESH" and not o.get("yakin"):
                o.is_holdout = True


# ------------------------------------------------------------------ SERIT: tas pist + isikli mini mantar siniri + oklar + OUT sapkalari
def serit_esyalari(rnd):
    kutu("pist", (0, (KAP["y"] + 0.4 - 4) / 2, 0.0), (PIST * 2, KAP["y"] + 4.4, 0.16), mat_tas("pist"), egim=0.04, seg=2)
    kenar = mat_pbr("pist_kenar", "#8a4a1a", 0.5, kaplama=0.3, bump=(6, 0.4))       # kutuk kenar
    for s in (-1, 1):
        kutu("pist_kenar", (s * (PIST + 0.08), (KAP["y"] + 0.4 - 4) / 2, 0.04), (0.26, KAP["y"] + 4.4, 0.3), kenar, egim=0.1, seg=3)
    for s in (-1, 1):                                            # pist kenarinda isikli mini mantarlar (sicak sari-turuncu sapka)
        y = -3.0; i = 0
        while y < KAP["y"] - 0.4:
            renk = ("#ffc21a", "#ff7a10", "#ff3aa8")[i % 3]
            silindir((s * (PIST + 0.5), y, 0.0), 0.07, 0.42, _SAP.get("sap") or mat_pbr("sap", SAP, 0.45), v=12)
            c = kure((s * (PIST + 0.5), y, 0.46), 0.22, mat_emis("mini" + renk, lin(hex3(renk)), 1.6)); c.scale = (1, 1, 0.55)
            y += 1.3; i += 1
    ok = mat_pbr("ok", "#ffc21a", 0.3, kaplama=0.7)
    for x in (-1.7, 1.7):
        for y in (4.6, 6.2):
            nok = [(x - 0.6, y - 0.4), (x, y), (x + 0.6, y - 0.4), (x + 0.6, y - 0.68), (x, y - 0.28), (x - 0.6, y - 0.68)]
            me = bpy.data.meshes.new("ok"); me.from_pydata([(a, b, 0.17) for a, b in nok], [], [list(range(6))]); me.update()
            o = bpy.data.objects.new("ok", me); bpy.context.collection.objects.link(o); o.data.materials.append(ok)
            o.modifiers.new("k", "SOLIDIFY").thickness = 0.02
    for s in (-1, 1):                                            # OUT ani: iki dis tarafta yumusak, alcak, genis mantar sapkasi
        mantar((s * 5.6, 5.0, 0), 1.5, 0.55, random.Random(36 + s), renk="#ff3aa8" if s < 0 else "#ff7a10", benek=True)


def kapi():
    """mantar kemer: iki yanda kalin sap kule (ustte sapka), aradaki kiris raf mantari (kat kat yarim disk); LED tabela; sarmasik"""
    Y, W_, H_, K = KAP["y"], KAP["w"], KAP["h"], KAP["kalin"]
    xk = W_ / 2 + K / 2
    sm = mat_pbr("kapi_sap", SAP, 0.45, kaplama=0.25, ss=0.2)
    for s in (-1, 1):
        silindir((s * xk, Y, 0), K * 0.75, H_ + K + 0.4, sm, v=40, r2=K * 0.6)
        mantar((s * xk, Y, H_ + K + 0.3), 1.25, 0.05, random.Random(8 + s), renk="#8a3aff" if s < 0 else "#10c8d0", benek=True)
    raf = mat_pbr("raf", "#ff7a10", 0.35, kaplama=0.5, ss=0.15)
    yuvarlak_kutu("kiris", (0, Y, H_ + K / 2), (W_ + 2 * K, K + 0.1, K), mat_pbr("kiris_ic", "#c8641a", 0.5, kaplama=0.2, bump=(5, 0.3)), egim=0.2, seg=5)
    for i in range(7):                                           # kiris onunde raf mantari dilimleri
        x = -W_ / 2 + i * W_ / 6
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.55, location=(x, Y - 0.35, H_ + K * 0.3 + (i % 2) * 0.2), segments=32, ring_count=16)
        r = bpy.context.active_object; r.scale = (1.0, 0.7, 0.28); r.data.materials.append(raf); bpy.ops.object.shade_smooth()
    yuvarlak_kutu("tabela", (0, Y, H_ + K + 0.75), (W_ * 0.6, 0.2, 0.7), mat_pbr("tabela", "#15171a", 0.35, metal=0.4), egim=0.05, seg=3)
    me = bpy.data.meshes.new("led_yuz"); a, b = W_ * 0.28, 0.28; z0 = H_ + K + 0.75
    me.from_pydata([(-a, Y - 0.11, z0 - b), (a, Y - 0.11, z0 - b), (a, Y - 0.11, z0 + b), (-a, Y - 0.11, z0 + b)], [], [[0, 1, 2, 3]]); me.update()
    o = bpy.data.objects.new("led_yuz", me); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat_emis("led_yuz", lin(hex3("#0a3a6a")), 1.2))
    yp = mat_pbr("yaprak", "#20c850", 0.4, kaplama=0.3)
    for s in (-1, 1):                                            # saplara sarilan sarmasik yapraklari
        for i in range(10):
            a = i * 1.1; z = 0.3 + i * 0.4
            p = kure((s * xk + math.cos(a) * K * 0.8, Y + math.sin(a) * K * 0.8, z), 0.16, yp); p.scale = (1.4, 0.5, 0.8)


def serit_katmani():
    sc = orman_sahnesi(1920, 1080, True)
    kam = kamera(sc)
    rnd = random.Random(36)
    isiklar()
    mekan(True, random.Random(36))
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
    sc = orman_sahnesi(1920, 1080, False)
    kamera(sc)
    isiklar()
    mekan(False, random.Random(36))
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
log("bitti (mantar)", YERLESIM.get(ON_EK + "aciklik_p1"))
