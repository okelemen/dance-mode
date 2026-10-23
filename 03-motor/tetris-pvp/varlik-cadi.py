"""TETRIS MODE 5. video (REF-056, 3 oyuncu) - HALLOWEEN sahne varliklari + tek kisilik poz maskeleri, 3 serit yan yana.

varlik.py tarafindan calistirilir (yardimcilar oradan gelir):
    blender -b --factory-startup -noaudio -P 03-motor/tetris-pvp/varlik.py -- --mod cadi --cikti cikti \
        [--ornek 64] [--yalniz hepsi|poz|sahne] --pozlar 03-motor/tetris-pvp/pozlar-05.json

REF-056'nin yapisi (tek genis serit, ortada TEK kafes kapi, chevron basamakli parlak yol, babali korkuluk,
yol kenarinda isikli bulut kumeleri, ufkun ustunde dev sarmal) korunur; dunya HALLOWEEN olur (kullanici 19 Eki 2026,
yalniz bu video): galaksi -> dev dolunay + ruh/sis girdabi + yarasalar, kapi kafes + mezarlik demir susu + balkabagi
fenerleri, korkuluk babalari -> fenerli mezar taslari, bulut kumeleri -> yesil-mor yer sisi + balkabagi kumeleri,
ufukta perili tepe + carpik agaclar + sato silueti. Genel Halloween nesneleri; marka/film karakteri yok.

Ciktilar (sahne5.html 2B'de birlestirir, kamera sabit):
  gok.png            1920x1080  gok + ay + girdap + uzak tepeler (tam ekran)
  serit-p1..p3.png   640x1080   her oyuncunun seridi: zemin, yol, mezar tasi korkuluk, kapi, balkabaklari, sis (gokte saydam)
  panel-p1..p3.png   1100x904   oyuncu renginde renk gecisli duvar paneli
  poz/<ad>.png       900x740    tek kisilik duz siyah siluet maskesi (varlik.py poz_maskeleri, --pozlar pozlar-05.json)
  yerlesim.json      kapi acikliklari (aciklik_p1..p3, serit koordinati), ampuller
Kullanici 19 Eki 2026: "her karede tek siluet, 3 tane yan yana" -> ekran 3 serit (P1 | P2 | P3).
"""

YERLESIM.clear()
# Kullanici 19 Eki 2026: "her karede tek siluet, 3 tane yan yana" -> ekran uce bolunur, her oyuncunun kendi seridi/kapisi/paneli.
OYUNCU = {"p1": "#ff7a1a", "p2": "#7dff4a", "p3": "#a35cff"}          # balkabagi turuncu | zehir yesili | cadi moru
SERIT_W = 640

# kamera: varlik.py serit kamerasi ile ayni (z 2,6 m, 10,5 derece asagi), goruntu tam genislik 1920x1080
KAP = {"y": 12.0, "w": 4.6, "h": 3.1, "kule": 0.45, "kiris": 0.45}     # acıklık 6,4 x 4,3 ~ panel orani 16:9
YOL_W = 3.6


def kamera(sc):
    rx = math.radians(90 - KAM["egim"])
    bpy.ops.object.camera_add(location=(0, 0, KAM["z"]), rotation=(rx, 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.sensor_fit = "VERTICAL"; kam.data.sensor_height = KAM["sensor"]; kam.data.lens = KAM["lens"]
    kam.data.clip_end = 400
    return kam


def mat_sis(ad, renk, guc, alfa):
    """yari saydam isikli sis (hacim degil: Cycles CPU'da hizli)"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    e = nt.nodes.new("ShaderNodeEmission"); e.inputs[0].default_value = (*renk, 1); e.inputs[1].default_value = guc
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mx = nt.nodes.new("ShaderNodeMixShader"); mx.inputs[0].default_value = alfa
    nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(e.outputs[0], mx.inputs[2])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(mx.outputs[0], o.inputs[0])
    m.blend_method = "BLEND"
    return m


def mat_duz(ad, renk, purluk=0.6, emis=0.0, emis_renk=None):
    m = bpy.data.materials.new(ad); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*renk, 1); b.inputs["Roughness"].default_value = purluk
    if emis:
        b.inputs["Emission Color"].default_value = (*(emis_renk or renk), 1); b.inputs["Emission Strength"].default_value = emis
    return m


def duz_sekil(ad, noktalar, konum, mat, olcek=1.0, kal=0.0):
    """XZ duzleminde (kameraya donuk) duz cokgen: yarasa, sato, agac dali silueti"""
    me = bpy.data.meshes.new(ad)
    v = [(x * olcek, 0, z * olcek) for x, z in noktalar]
    me.from_pydata(v, [], [list(range(len(v)))]); me.update()
    o = bpy.data.objects.new(ad, me); bpy.context.collection.objects.link(o)
    o.location = konum; o.data.materials.append(mat)
    if kal:
        so = o.modifiers.new("kal", "SOLIDIFY"); so.thickness = kal
    return o


YARASA = [(0, 0.10), (0.12, 0.16), (0.2, 0.08), (0.34, 0.2), (0.62, 0.32), (0.56, 0.12), (0.44, 0.0), (0.32, -0.06),
          (0.18, -0.02), (0.08, -0.12), (0, -0.06), (-0.08, -0.12), (-0.18, -0.02), (-0.32, -0.06), (-0.44, 0.0), (-0.56, 0.12),
          (-0.62, 0.32), (-0.34, 0.2), (-0.2, 0.08), (-0.12, 0.16)]


# ------------------------------------------------------------------ GOK + uzak tepeler
def ay_ve_gok(rnd):
    # gok duzlemi: ufukta mor-yesil isilti -> tepede koyu gece, ustune bulutsu gurultu
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 140, 30), rotation=(math.pi / 2, 0, 0))
    p = bpy.context.active_object; p.scale = (420, 160, 1)
    m = bpy.data.materials.new("gok"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    rmp = nt.nodes.new("ShaderNodeValToRGB"); cr = rmp.color_ramp
    cr.elements[0].position = 0.30; cr.elements[0].color = (*lin(hex3("#3b1866")), 1)
    cr.elements[1].position = 0.80; cr.elements[1].color = (*lin(hex3("#05030f")), 1)
    e = cr.elements.new(0.45); e.color = (*lin(hex3("#1d0b40")), 1)
    nt.links.new(sep.outputs["Y"], rmp.inputs[0])
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 6.0; nz.inputs["Detail"].default_value = 6
    nz.inputs["Distortion"].default_value = 0.8; nt.links.new(tc.outputs["Generated"], nz.inputs["Vector"])
    nr = nt.nodes.new("ShaderNodeValToRGB"); c2 = nr.color_ramp
    c2.elements[0].position = 0.5; c2.elements[0].color = (0, 0, 0, 1)
    c2.elements[1].position = 0.85; c2.elements[1].color = (*lin(hex3("#6a2bd6")), 1)
    nt.links.new(nz.outputs["Fac"], nr.inputs[0])
    nz2 = nt.nodes.new("ShaderNodeTexNoise"); nz2.inputs["Scale"].default_value = 9.0; nz2.inputs["Detail"].default_value = 4
    nt.links.new(tc.outputs["Generated"], nz2.inputs["Vector"])
    nr2 = nt.nodes.new("ShaderNodeValToRGB"); c3 = nr2.color_ramp
    c3.elements[0].position = 0.58; c3.elements[0].color = (0, 0, 0, 1)
    c3.elements[1].position = 0.9; c3.elements[1].color = (*lin(hex3("#2fe08a")), 1)
    nt.links.new(nz2.outputs["Fac"], nr2.inputs[0])
    a1 = nt.nodes.new("ShaderNodeMix"); a1.data_type = "RGBA"; a1.blend_type = "ADD"; a1.inputs[0].default_value = 0.55
    nt.links.new(rmp.outputs[0], a1.inputs[6]); nt.links.new(nr.outputs[0], a1.inputs[7])
    a2 = nt.nodes.new("ShaderNodeMix"); a2.data_type = "RGBA"; a2.blend_type = "ADD"; a2.inputs[0].default_value = 0.22
    nt.links.new(a1.outputs[2], a2.inputs[6]); nt.links.new(nr2.outputs[0], a2.inputs[7])
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs[1].default_value = 1.0
    nt.links.new(a2.outputs[2], em.inputs[0])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], o.inputs[0])
    p.data.materials.append(m)
    # yildizlar
    ym = mat_emis("yildiz", (1, 1, 1), 8)
    for i in range(520):
        x, z = rnd.uniform(-190, 190), rnd.uniform(10, 150)
        kure((x, 130, z), rnd.uniform(0.12, 0.42), ym)
    # DOLUNAY (galaksinin yerine): krem yuzey, krater gurultusu, kenara dogru kararan hacim, turuncu hale
    AY = Vector((0, 110, 14)); R_ = 17.0
    bpy.ops.mesh.primitive_uv_sphere_add(radius=R_, location=AY, segments=96, ring_count=48)
    ay = bpy.context.active_object; bpy.ops.object.shade_smooth()
    m = bpy.data.materials.new("ay"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord")
    vz = nt.nodes.new("ShaderNodeTexVoronoi"); vz.inputs["Scale"].default_value = 5.0
    nt.links.new(tc.outputs["Generated"], vz.inputs["Vector"])
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 3.0; nz.inputs["Detail"].default_value = 8
    nt.links.new(tc.outputs["Generated"], nz.inputs["Vector"])
    mx = nt.nodes.new("ShaderNodeMath"); mx.operation = "MULTIPLY"
    nt.links.new(vz.outputs["Distance"], mx.inputs[0]); nt.links.new(nz.outputs["Fac"], mx.inputs[1])
    rp = nt.nodes.new("ShaderNodeValToRGB"); cr = rp.color_ramp
    cr.elements[0].position = 0.05; cr.elements[0].color = (*lin(hex3("#d9b98a")), 1)
    cr.elements[1].position = 0.45; cr.elements[1].color = (*lin(hex3("#fff4d6")), 1)
    nt.links.new(mx.outputs[0], rp.inputs[0])
    fr = nt.nodes.new("ShaderNodeLayerWeight"); fr.inputs["Blend"].default_value = 0.5
    kr = nt.nodes.new("ShaderNodeMath"); kr.operation = "SUBTRACT"; kr.inputs[0].default_value = 1.2
    nt.links.new(fr.outputs["Facing"], kr.inputs[1])
    gm = nt.nodes.new("ShaderNodeMath"); gm.operation = "MULTIPLY"; gm.inputs[1].default_value = 2.6
    nt.links.new(kr.outputs[0], gm.inputs[0])
    em = nt.nodes.new("ShaderNodeEmission"); nt.links.new(rp.outputs[0], em.inputs[0]); nt.links.new(gm.outputs[0], em.inputs[1])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], o.inputs[0])
    ay.data.materials.append(m)
    for (rr, c, g) in ((1.10, "#ffcf7a", 0.55), (1.32, "#ff8a3a", 0.22), (1.7, "#8a3bd6", 0.10)):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=R_ * rr, location=AY + Vector((0, 8 * rr, 0)), segments=64, ring_count=32)
        h_ = bpy.context.active_object; bpy.ops.object.shade_smooth()
        h_.data.materials.append(mat_sis("hale%.2f" % rr, lin(hex3(c)), g * 6, 0.35))
    # RUH / SIS GIRDABI: ayin cevresinde iki kollu sarmal (REF-056 galaksi sarmalinin yerine), yesil-mor-beyaz
    mats = [mat_emis("r%d" % i, lin(hex3(c)), e) for i, (c, e) in enumerate(
        (("#ffffff", 12), ("#7dff6a", 10), ("#b45cff", 11), ("#5ef0ff", 8), ("#ffb05a", 9)))]
    for kol in (0, math.pi):
        for i in range(900):
            u = rnd.random() ** 0.75
            r = R_ * 1.15 + u * 70
            a = kol + 2.3 * math.log(r / (R_ * 1.15) + 1) * 2.0 + rnd.gauss(0, 0.16)
            x = AY.x + r * math.cos(a) + rnd.gauss(0, 1.2)
            z = AY.z + 0.5 * r * math.sin(a) + rnd.gauss(0, 0.9)
            kure((x, AY.y - 14 + rnd.uniform(-2, 2), z), rnd.uniform(0.12, 0.5) * (1.25 - u * 0.6), rnd.choice(mats))
    # sarmalin ici: yari saydam sis kollari (parcaciklarin altinda yumusak bant)
    sis_m = [mat_sis("sk%d" % i, lin(hex3(c)), 1.1, 0.08) for i, c in enumerate(("#7dff6a", "#b45cff", "#5ef0ff"))]
    for kol in (0, math.pi):
        for i in range(70):
            u = i / 70
            r = R_ * 1.2 + u * 60
            a = kol + 2.3 * math.log(r / (R_ * 1.15) + 1) * 2.0
            kure((AY.x + r * math.cos(a), AY.y - 10, AY.z + 0.5 * r * math.sin(a)), 2.2 + 2.5 * u, sis_m[i % 3])
    # YARASA SURULERI: girdap kollari boyunca siyah yarasalar, aya yakin olanlar ayin onunde siluet
    siyah = mat_emis("yarasa", lin(hex3("#05020a")), 0.0)
    for i in range(110):
        u = rnd.random()
        r = R_ * 0.4 + u * 55
        a = rnd.choice((0, math.pi)) + 2.3 * math.log(max(r, R_ * 0.5) / (R_ * 1.15) + 1) * 2.0 + rnd.gauss(0, 0.3)
        x = AY.x + r * math.cos(a); z = AY.z + 0.5 * r * math.sin(a) + rnd.gauss(0, 1.5)
        s = rnd.uniform(1.6, 3.6) * (1.3 - u * 0.6)
        b = duz_sekil("yarasa", YARASA, (x, AY.y - 20, z), siyah, olcek=s)
        b.rotation_euler.y = rnd.uniform(-0.4, 0.4)
    return AY, R_


def uzak_tepeler(rnd):
    """ufukta perili tepe, carpik agaclar, sato silueti (koyu mor, pencereler turuncu)"""
    tepe = mat_duz("tepe", lin(hex3("#0d0618")), 0.9, emis=0.15, emis_renk=lin(hex3("#2a0f4a")))
    for (x, y, sx, sz) in ((-70, 85, 46, 13), (-20, 92, 40, 9), (35, 88, 44, 12), (85, 80, 40, 15), (0, 75, 60, 6)):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(x, y, -2), segments=48, ring_count=24)
        o = bpy.context.active_object; o.scale = (sx, 8, sz); o.data.materials.append(tepe); bpy.ops.object.shade_smooth()
    # sato (sol tepede): kuleler + sivri catilar + isikli pencereler
    cati = mat_duz("cati", lin(hex3("#07030d")), 0.8)
    pen = mat_emis("pencere", lin(hex3("#ffa63a")), 12)
    sx0, sy0, sz0 = -62, 80, 9.0
    for (dx, w, h) in ((0, 3.4, 12), (-6, 2.4, 8), (6, 2.6, 9.5), (-11, 1.8, 6), (11.5, 1.8, 7), (3, 6, 5)):
        yuvarlak_kutu("kule", (sx0 + dx, sy0, sz0 + h / 2), (w, w, h), tepe, egim=0.05, seg=2)
        bpy.ops.mesh.primitive_cone_add(radius1=w * 0.72, depth=w * 1.6, location=(sx0 + dx, sy0, sz0 + h + w * 0.8), vertices=12)
        bpy.context.active_object.data.materials.append(cati)
        for j in range(int(h / 2.5)):
            if rnd.random() < 0.65:
                yuvarlak_kutu("pen", (sx0 + dx + rnd.uniform(-w * 0.25, w * 0.25), sy0 - w / 2 - 0.05, sz0 + 1.6 + j * 2.4), (0.45, 0.1, 0.8), pen, egim=0.02, seg=1)
    # carpik agaclar: dallanan borular (siluet)
    agac = mat_duz("agac", lin(hex3("#05020a")), 0.9)
    for x in (-96, -40, -28, 22, 52, 70, 100):
        y = rnd.uniform(70, 86)
        def dal(a, b, r, n):
            boru(a, b, r, agac)
            if n == 0:
                return
            d = Vector(b) - Vector(a)
            for s in (-1, 1):
                yon = Matrix.Rotation(s * rnd.uniform(0.4, 0.9), 3, "Y") @ d
                dal(b, tuple(Vector(b) + yon * rnd.uniform(0.45, 0.7)), r * 0.62, n - 1)
        dal((x, y, 0), (x + rnd.uniform(-1.5, 1.5), y, rnd.uniform(6, 10)), 0.55, 4)


# ------------------------------------------------------------------ ZEMIN + YOL + KAPI (serit katmani)
def kabak(konum, r, kabuk, sap, yuz=None):
    x, y, z = konum
    for i in range(8):
        a = i / 8 * 2 * math.pi
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r * 0.62, location=(x + math.cos(a) * r * 0.42, y + math.sin(a) * r * 0.42, z + r * 0.72), segments=24, ring_count=12)
        o = bpy.context.active_object; o.scale = (1, 1, 0.92); o.data.materials.append(kabuk); bpy.ops.object.shade_smooth()
    boru((x, y, z + r * 1.2), (x + r * 0.08, y, z + r * 1.55), r * 0.1, sap)
    if yuz:
        on_ = y - r * 1.0
        for dx in (-0.32, 0.32):
            duz_sekil("goz", [(-0.15, -0.1), (0.15, -0.1), (0, 0.15)], (x + dx * r, on_, z + r * 0.92), yuz, olcek=r)
        duz_sekil("agiz", [(-0.48, 0.05), (-0.3, -0.05), (-0.18, 0.06), (0, -0.08), (0.18, 0.06), (0.3, -0.05), (0.48, 0.05),
                           (0.3, -0.25), (0, -0.32), (-0.3, -0.25)], (x, on_, z + r * 0.55), yuz, olcek=r)
        isik("POINT", (x, on_ - r * 0.4, z + r * 0.7), 40 * r * r, lin(hex3("#ff9a2a")))


def mezar(x, y, mat, fener):
    yuvarlak_kutu("mezar", (x, y, 0.5), (0.62, 0.22, 1.0), mat, egim=0.06)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.31, depth=0.22, location=(x, y, 1.0), rotation=(math.pi / 2, 0, 0), vertices=24)
    o = bpy.context.active_object; o.data.materials.append(mat); bpy.ops.object.shade_smooth()
    yuvarlak_kutu("hac", (x, y - 0.12, 0.62), (0.08, 0.03, 0.4), fener, egim=0.01, seg=1)
    yuvarlak_kutu("hac2", (x, y - 0.12, 0.7), (0.26, 0.03, 0.07), fener, egim=0.01, seg=1)
    kure((x, y, 1.42), 0.11, fener)


def zemin_ve_yol(rnd, oyuncu):
    Y = KAP["y"]
    # zemin: koyu mor, yesil sis lekeli (ekran bos kalmasin)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 60, -0.02))
    g = bpy.context.active_object; g.scale = (300, 140, 1)
    m = bpy.data.materials.new("zemin"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 40; nz.inputs["Detail"].default_value = 5
    nt.links.new(tc.outputs["Generated"], nz.inputs["Vector"])
    rp = nt.nodes.new("ShaderNodeValToRGB"); cr = rp.color_ramp
    cr.elements[0].position = 0.35; cr.elements[0].color = (*lin(hex3("#140826")), 1)
    cr.elements[1].position = 0.75; cr.elements[1].color = (*lin(hex3("#1f7a5a")), 1)
    e = cr.elements.new(0.55); e.color = (*lin(hex3("#3a1660")), 1)
    nt.links.new(nz.outputs["Fac"], rp.inputs[0])
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs[1].default_value = 0.55; nt.links.new(rp.outputs[0], em.inputs[0])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], o.inputs[0])
    g.data.materials.append(m)
    # yol: koyu mor doseme + REF-056'daki gibi isikli chevron basamaklar (bizde turuncu-mor)
    yol = mat_duz("yol", lin(hex3("#2a1048")), 0.75, emis=0.08)
    yuvarlak_kutu("yol", (0, (0.5 + Y + 3) / 2, -0.2), (YOL_W, Y + 3 - 0.5, 0.4), yol, egim=0.12)
    chev_a = mat_emis("chev_a", lin(hex3("#ff7a1a")), 5.0)
    chev_b = mat_emis("chev_b", lin(hex3("#b45cff")), 4.0)
    adim = 1.6
    for j, yy in enumerate([1.5 + i * adim for i in range(int((Y - 2) / adim))]):
        for s in (-1, 1):
            a = (0, yy + 0.55, 0.02); b = (s * (YOL_W / 2 - 0.35), yy, 0.02)
            boru(a, b, 0.07, chev_a if j % 2 == 0 else chev_b)
    # kenar seritleri
    neon_k = mat_emis("kenar", lin(hex3(OYUNCU[oyuncu])), 6.0)
    for s in (-1, 1):
        boru((s * (YOL_W / 2 - 0.1), 0.5, 0.02), (s * (YOL_W / 2 - 0.1), Y + 2.5, 0.02), 0.06, neon_k)
    # korkuluk: fenerli mezar taslari (REF-056'nin yuvarlak babalarinin yerine) + dovme demir parmaklik
    tas = mat_jole("tas", lin(hex3("#5a4a78")), emis=0.04, purluk=0.55)
    fener = mat_emis("mezar_fener", lin(hex3("#7dff6a")), 6.0)
    demir = mat_duz("demir", lin(hex3("#0b0612")), 0.4)
    for s in (-1, 1):
        ys = [1.4 + i * 1.6 for i in range(int((Y - 1.4) / 1.6) + 1)]
        for yy in ys:
            mezar(s * (YOL_W / 2 + 0.35), yy, tas, fener)
        for zz in (0.35, 0.95):
            boru((s * (YOL_W / 2 + 0.35), ys[0], zz), (s * (YOL_W / 2 + 0.35), ys[-1], zz), 0.04, demir)
        for k_ in range(int((ys[-1] - ys[0]) / 0.4)):
            yy = ys[0] + 0.2 + k_ * 0.4
            boru((s * (YOL_W / 2 + 0.35), yy, 0.0), (s * (YOL_W / 2 + 0.35), yy, 1.15), 0.025, demir)
            bpy.ops.mesh.primitive_cone_add(radius1=0.06, depth=0.18, location=(s * (YOL_W / 2 + 0.35), yy, 1.22), vertices=8)
            bpy.context.active_object.data.materials.append(demir)
    # yol kenarinda balkabagi kumeleri + yer sisi (REF-056'nin isikli bulut kumelerinin yerine)
    kabuk = mat_jole("kabuk", lin(hex3("#ff6a10")), emis=0.12, purluk=0.35)
    kabuk2 = mat_jole("kabuk2", lin(hex3("#e04a08")), emis=0.08, purluk=0.4)
    sap = mat_duz("sap", lin(hex3("#3a5a12")), 0.6)
    yuz = mat_emis("yuz", lin(hex3("#ffd23a")), 18)
    for s in (-1, 1):
        yy = 1.2
        while yy < Y + 30:
            r = rnd.uniform(0.3, 0.6) * (1 + yy / 30)
            x = s * (YOL_W / 2 + 0.9 + rnd.uniform(0, 1.6) + yy * 0.2)
            kabak((x, yy, 0), r, rnd.choice((kabuk, kabuk2)), sap, yuz if rnd.random() < 0.55 else None)
            if rnd.random() < 0.6:
                r2 = r * rnd.uniform(0.5, 0.75)
                kabak((x + s * r * 1.5, yy + rnd.uniform(-0.6, 0.6), 0), r2, rnd.choice((kabuk, kabuk2)), sap, None)
            yy += rnd.uniform(1.6, 3.2) * (1 + yy / 25)
    # mezarlik (yol disi, uzakta): egik mezar taslari
    for i in range(70):
        s = rnd.choice((-1, 1)); yy = rnd.uniform(6, 60)
        x = s * rnd.uniform(YOL_W / 2 + 3 + yy * 0.2, 14 + yy * 0.9)
        mezar(x, yy, tas, fener)
        bpy.context.active_object.rotation_euler.y = rnd.uniform(-0.2, 0.2)
    sis = [mat_sis("sis%d" % i, lin(hex3(c)), 0.6, 0.06) for i, c in enumerate(("#4dff9a", "#9a5cff", "#c7b8ff"))]
    for i in range(60):
        s = rnd.choice((-1, 1)); yy = rnd.uniform(KAP["y"] + 2, 70)
        x = s * rnd.uniform(YOL_W / 2 + 0.5, YOL_W / 2 + 4 + yy * 0.9)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(x, yy, 0.1), segments=24, ring_count=12)
        o = bpy.context.active_object; rr = rnd.uniform(0.8, 2.2) * (1 + yy / 40)
        o.scale = (rr * 1.8, rr, rr * 0.5); o.data.materials.append(rnd.choice(sis)); bpy.ops.object.shade_smooth()


def kapi_cadi(oyuncu, tabela_yazi=True):
    """REF-056 kafes kapisi (yapi ayni) + mezarlik demir susu, kule tepelerinde balkabagi fenerleri, HALLOWEEN tabelasi"""
    Y, W, H, KK, KR = KAP["y"], KAP["w"], KAP["h"], KAP["kule"], KAP["kiris"]
    R = lin(hex3(OYUNCU[oyuncu]))
    ana = mat_jole("kapi_ana", R, emis=0.25, purluk=0.15)
    ince = mat_jole("kapi_ince", acik(R, 0.35), emis=0.35, purluk=0.15)
    koyum = mat_jole("kapi_koyu", lin(hex3("#2a0f4a")), emis=0.02)
    demir = mat_duz("kapi_demir", lin(hex3("#0b0612")), 0.35)
    xk = W / 2 - KK / 2
    for s in (-1, 1):
        kafes_kule(s * xk, Y, 0.0, H + KR, KK, ana, ince)
        yuvarlak_kutu("taban", (s * xk, Y, 0.14), (KK + 0.35, KK + 0.35, 0.28), koyum, egim=0.06)
    kafes_kiris(-xk, xk, Y, H + KR / 2, KR, ana, ince)
    # demir sus: kirisin ustunde kivrimli halkalar + sivri uclar
    for i in range(7):
        x = -xk + 0.4 + i * (2 * xk - 0.8) / 6
        bpy.ops.mesh.primitive_torus_add(major_radius=0.22, minor_radius=0.035, location=(x, Y - KK / 2, H + KR + 0.28), rotation=(math.pi / 2, 0, 0))
        bpy.context.active_object.data.materials.append(demir)
        bpy.ops.mesh.primitive_cone_add(radius1=0.06, depth=0.35, location=(x, Y - KK / 2, H + KR + 0.62), vertices=8)
        bpy.context.active_object.data.materials.append(demir)
    # neon tup (acikligi cevreler) - turuncu
    ic = W / 2 - KK
    neon = mat_emis("neon", lin(hex3("#ff8a2a")), 9.0)
    for a, b in (((-ic + 0.12, Y - 0.3, 0.05), (-ic + 0.12, Y - 0.3, H - 0.12)), ((ic - 0.12, Y - 0.3, 0.05), (ic - 0.12, Y - 0.3, H - 0.12)),
                 ((-ic + 0.12, Y - 0.3, H - 0.12), (ic - 0.12, Y - 0.3, H - 0.12))):
        boru(a, b, 0.05, neon)
    # ampuller (sahne5.html yakip sondurur)
    amp = mat_emis("ampul", lin(hex3("#ffd08a")), 2.5)
    AMPUL = []
    for i in range(13):
        AMPUL.append(Vector((-ic + 0.2 + i * (2 * ic - 0.4) / 12, Y - KK / 2 - 0.05, H - 0.06)))
    for s_ in (-1, 1):
        for j in range(9):
            AMPUL.append(Vector((s_ * xk, Y - KK / 2 - 0.06, 0.35 + j * (H - 0.45) / 8)))
    for q in AMPUL:
        kure(q, 0.065, amp)
    # tabela
    yuvarlak_kutu("tabela", (0, Y - KK / 2 - 0.22, H + KR / 2), (2.2, 0.14, 0.5), koyum, egim=0.12, seg=6)
    yuvarlak_kutu("tabela_cerceve", (0, Y - KK / 2 - 0.16, H + KR / 2), (2.4, 0.12, 0.62), mat_jole("tc", acik(R, 0.2), emis=0.3), egim=0.16, seg=6)
    try:
        font = bpy.data.fonts.load(os.path.join(KOK, "05-kapak/fontlar/TitanOne.ttf"))
        bpy.ops.object.text_add(location=(0, Y - KK / 2 - 0.31, H + KR / 2 - 0.03), rotation=(math.pi / 2, 0, 0))
        tx = bpy.context.active_object
        if not tabela_yazi:          # kapak: kullanici "yazi yalniz TETRIS MODE + HALLOWEEN" -> tabelada yazi yok
            bpy.data.objects.remove(tx); raise RuntimeError("kapak: tabela yazisiz")
        tx.data.body = "PLAYER " + oyuncu[1]; tx.data.font = font; tx.data.size = 0.34; tx.data.extrude = 0.04; tx.data.bevel_depth = 0.012
        tx.data.align_x = "CENTER"; tx.data.align_y = "CENTER"
        tx.data.materials.append(mat_emis("tabela_yazi", lin(hex3("#ffe0a0")), 4.0))
    except Exception as e:
        log("tabela yazisi atlandi:", e)
    # kule tepelerinde yuzlu balkabagi fenerleri (REF'teki kose susunun yerine)
    kabuk = mat_jole("kk", lin(hex3("#ff6a10")), emis=0.2, purluk=0.35)
    sap = mat_duz("ks", lin(hex3("#3a5a12")), 0.6)
    yuz = mat_emis("ky", lin(hex3("#ffd23a")), 20)
    for s_ in (-1, 1):
        kabak((s_ * xk, Y - 0.1, H + KR + 0.04), 0.3, kabuk, sap, yuz)
    # kaide
    yuvarlak_kutu("kaide", (0, Y - 0.6, 0.07), (W + 0.5, 0.8, 0.18), koyum, egim=0.06)
    boru((-W / 2 - 0.15, Y - 1.02, 0.14), (W / 2 + 0.15, Y - 1.02, 0.14), 0.04, neon)
    return AMPUL


def sahne_cadi():
    rnd = random.Random(56)
    # --- 1) GOK (tam ekran 1920x1080, serit kamerasi ile ayni egim)
    sc = bos_sahne(w=1920, h=1080, ornek=min(ORNEK, 64))
    kamera(sc)
    sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.15
    ay_ve_gok(rnd)
    uzak_tepeler(rnd)
    sc.use_nodes = True
    nt2 = sc.node_tree; nt2.nodes.clear()
    rl = nt2.nodes.new("CompositorNodeRLayers")
    gl = nt2.nodes.new("CompositorNodeGlare"); gl.glare_type = "FOG_GLOW"; gl.threshold = 0.85; gl.size = 9; gl.mix = 0.2
    ou = nt2.nodes.new("CompositorNodeComposite")
    nt2.links.new(rl.outputs[0], gl.inputs[0]); nt2.links.new(gl.outputs[0], ou.inputs[0])
    yaz(sc, "gok.png")
    # --- 2) her oyuncunun SERIDI (640x1080, gokte saydam)
    for oyuncu in OYUNCU:
        rnd = random.Random({"p1": 21, "p2": 23, "p3": 29}[oyuncu])
        sc = bos_sahne(w=SERIT_W, h=1080, saydam=True, ornek=min(ORNEK, 64))
        kam = kamera(sc)
        sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.15
        zemin_ve_yol(rnd, oyuncu)
        AMPUL = kapi_cadi(oyuncu)
        R = lin(hex3(OYUNCU[oyuncu]))
        isik("AREA", (0, -1.5, 6.5), 420, lin(hex3("#d8c8ff")), 6, yon=(0, KAP["y"] * 0.6, 0))
        isik("AREA", (-3, 3, 3), 260, acik(R, 0.2), 3, yon=(0, KAP["y"], 2))
        isik("AREA", (3, 3, 3), 220, lin(hex3("#b48cff")), 3, yon=(0, KAP["y"], 2))
        isik("AREA", (0, KAP["y"] + 3, 5), 500, acik(R, 0.1), 5, yon=(0, KAP["y"], 1))
        Y, W_, H_, KK = KAP["y"], KAP["w"], KAP["h"], KAP["kule"]
        ic = W_ / 2 - KK
        bpy.context.view_layer.update()
        px = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-ic, Y, 0), (ic, Y, 0), (-ic, Y, H_), (ic, Y, H_))]
        xs = [p.x * SERIT_W for p in px]; ys = [(1 - p.y) * 1080 for p in px]
        YERLESIM["aciklik_" + oyuncu] = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
        YERLESIM["ampul_" + oyuncu] = [[round(p.x * SERIT_W, 1), round((1 - p.y) * 1080, 1)] for p in (world_to_camera_view(sc, kam, q) for q in AMPUL)]
        log("aciklik", oyuncu, YERLESIM["aciklik_" + oyuncu])
        yaz(sc, "serit-%s.png" % oyuncu)
    YERLESIM["yol"] = {"y_kapi": KAP["y"], "genislik": YOL_W, "kam": KAM, "serit_w": SERIT_W}


# ------------------------------------------------------------------ PANELLER (renk gecisli, ince taneli)
PANEL_RENK = {"p1": ("#ffc23a", "#d0122e"), "p2": ("#d6ff5a", "#139a52"), "p3": ("#e0b8ff", "#5a1ab0")}


def panel_cadi(tip):
    """oyuncu renginde renk gecisli panel (REF-056 duvari), 1100x904 (sahne4 ile ayni oran)"""
    sc = bos_sahne(w=1100, h=904, saydam=True, ornek=min(ORNEK, 32))
    A, B = (lin(hex3(c)) for c in PANEL_RENK[tip])
    PW, PH = 5.0, 4.1
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    p = bpy.context.active_object; p.scale = (PW, 0.2, PH); bpy.ops.object.transform_apply(scale=True)
    bv = p.modifiers.new("egim", "BEVEL"); bv.width = 0.12; bv.segments = 6; bv.limit_method = "NONE"
    bpy.ops.object.shade_smooth()
    m = bpy.data.materials.new("panel"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sp = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Generated"], sp.inputs[0])
    t = nt.nodes.new("ShaderNodeMath"); t.operation = "MULTIPLY_ADD"; t.inputs[1].default_value = 0.6
    nt.links.new(sp.outputs["X"], t.inputs[0]); nt.links.new(sp.outputs["Z"], t.inputs[2])
    t2 = nt.nodes.new("ShaderNodeMath"); t2.operation = "MULTIPLY"; t2.inputs[1].default_value = 0.625
    nt.links.new(t.outputs[0], t2.inputs[0])
    rp = nt.nodes.new("ShaderNodeValToRGB"); cr = rp.color_ramp
    cr.elements[0].position = 0.1; cr.elements[0].color = (*A, 1)
    cr.elements[1].position = 0.95; cr.elements[1].color = (*B, 1)
    nt.links.new(t2.outputs[0], rp.inputs[0])
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 400; nz.inputs["Detail"].default_value = 2
    nt.links.new(tc.outputs["Generated"], nz.inputs["Vector"])
    mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"; mx.blend_type = "OVERLAY"; mx.inputs[0].default_value = 0.18
    nt.links.new(rp.outputs[0], mx.inputs[6]); nt.links.new(nz.outputs["Fac"], mx.inputs[7])
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs[1].default_value = 1.0; nt.links.new(mx.outputs[2], em.inputs[0])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], o.inputs[0])
    p.data.materials.append(m)
    bpy.ops.object.camera_add(location=(0, -10, 0), rotation=(math.radians(90), 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.type = "ORTHO"; kam.data.ortho_scale = PW + 0.06
    yaz(sc, "panel-%s.png" % tip)


# ------------------------------------------------------------------ KAPAK: REF-056 kapak duzeni (kullanici 19 Eki 2026: "o ne yaptiysa aynisini yap
# ama siluetin hareketleri farkli olsun") -> tek kapi sagda + 3 kisilik TEK grup siluet (birbirine deger), kapida ayni grubun kucugu.
# 3 kisilik grup maskesi kodu (videoda iptal edilen) yalniz kapak icin burada.

# ------------------------------------------------------------------ 3 KISILIK GRUP MASKELERI
def ayna_poz(P):
    """ekran aynasi: sol/sag uzuvlar yer degistirir, acilar eksi olur, profil yonu doner"""
    Q = {"ad": P["ad"], "yon": {"on": "on", "sag": "sol", "sol": "sag"}[P.get("yon", "on")]}
    neg = lambda v: [x if x == "geri" else -x for x in v]
    Q["govde"] = -P.get("govde", 180); Q["bas"] = -P.get("bas", 0)
    for a, b in (("sagKol", "solKol"), ("sagBacak", "solBacak")):
        if a in P: Q[b] = neg(P[a])
        if b in P: Q[a] = neg(P[b])
    return Q


def figur_pozla(arm, mesler, P, taban_rot):
    for b in arm.pose.bones:
        b.matrix_basis = Matrix.Identity(4)
    yon = P.get("yon", "on")
    arm.rotation_euler.z = taban_rot + {"on": 0, "sag": math.radians(90), "sol": math.radians(-90)}[yon]
    arm.location = (0, 0, 0)
    bpy.context.view_layer.update()
    ileri = {"on": Vector((0, -1, 0)), "sag": Vector((1, 0, 0)), "sol": Vector((-1, 0, 0))}[yon]
    g = P.get("govde", 180); ba = P.get("bas", 0)
    for k_, aci in (("Spine", g), ("Spine1", g), ("Spine2", g), ("Neck", g + ba), ("Head", g + ba)):
        try:
            yonelt(arm, kemik(arm, k_), yon_vek(aci, ileri))
        except KeyError:
            pass
    for taraf, anah in (("Left", "sol"), ("Right", "sag")):
        kol = P.get(anah + "Kol", [-12 if anah == "sag" else 12] * 2)
        yonelt(arm, kemik(arm, taraf + "Arm"), yon_vek(kol[0], ileri))
        yonelt(arm, kemik(arm, taraf + "ForeArm"), yon_vek(kol[1], ileri))
        yonelt(arm, kemik(arm, taraf + "Hand"), yon_vek(kol[1], ileri))
        bac = P.get(anah + "Bacak", [-3 if anah == "sag" else 3, 0])
        yonelt(arm, kemik(arm, taraf + "UpLeg"), yon_vek(bac[0], ileri))
        yonelt(arm, kemik(arm, taraf + "Leg"), yon_vek(bac[1], ileri))
        baldir = yon_vek(bac[1], ileri)
        if baldir.dot(ileri) < -0.5 or bac[1] == "geri":
            ayak = (baldir * 0.7 + Vector((0, 0, -0.7))).normalized()
        else:
            ayak = (ileri * 0.9 + baldir * 0.35).normalized()
        yonelt(arm, kemik(arm, taraf + "Foot"), ayak)
    # zemine oturt (kaldirma/tasima yok: her figur kendi ayagi/dizi/eli ile yerde)
    alt, ust = dunya_kutusu(mesler)
    arm.location.z -= alt.z
    bpy.context.view_layer.update()


EKLEM = {"el": [("LeftHand", "kuyruk"), ("RightHand", "kuyruk")], "omuz": [("LeftArm", "bas"), ("RightArm", "bas")],
         "ayak": [("LeftToeBase", "bas"), ("RightToeBase", "bas")], "diz": [("LeftLeg", "bas"), ("RightLeg", "bas")],
         "kalca": [("LeftUpLeg", "bas"), ("RightUpLeg", "bas")], "bas": [("Head", "kuyruk")], "sirt": [("Spine2", "bas")]}


def eklemler(arm, tur):
    out = []
    for ad, uc in EKLEM[tur]:
        b = kemik(arm, ad)
        out.append(arm.matrix_world @ (b.tail if uc == "kuyruk" else b.head))
    return out


def hizala(solA, solM, sagA, sagM, temas):
    """sag figuru x'te kaydirir: temas = [sol figurun eklem turu, sag figurun eklem turu] ya da "yan" (silüetler deger)"""
    bpy.context.view_layer.update()
    if temas == "yan":
        a1, u1 = dunya_kutusu(solM); a2, u2 = dunya_kutusu(sagM)
        sagA.location.x += (u1.x - 0.22) - a2.x      # 0,22 m bindirme: silüetler gercekten deger
        bpy.context.view_layer.update()
        return {"tip": "yan", "dz": 0.0}
    p = max(eklemler(solA, temas[0]), key=lambda v: v.x)
    q = min(eklemler(sagA, temas[1]), key=lambda v: v.x)
    sagA.location.x += (p.x - 0.04) - q.x
    bpy.context.view_layer.update()
    return {"tip": "-".join(temas), "dz": round(q.z - p.z, 3)}


def grup_maskeleri(dosya="kapak-grup-%s.png", kisi_basi=True):
    """grup siluetleri: figur sayisi grup dosyasindan (5. video kapagi 3 kisi; 7. video CO-OP 2 kisi, --yalniz grup)"""
    GRUPLAR = json.load(open(os.path.join(KOK, arg("--gruplar", "03-motor/tetris-pvp/kapak-grup-05.json")), encoding="utf-8"))["gruplar"]
    NFIG = max(len(G["figurler"]) for G in GRUPLAR.values())
    os.makedirs(os.path.dirname(os.path.join(CIKTI, dosya % "x")), exist_ok=True)
    sc = bos_sahne(motor="CYCLES", w=1600, h=900, saydam=True, ornek=16)
    sc.frame_set(1); sc.cycles.use_denoising = False; sc.view_settings.view_transform = "Standard"
    siyah = mat_emis("siluet", (0, 0, 0), 0.0)
    FIG = []
    for i in range(NFIG):
        once = set(bpy.data.objects)
        bpy.ops.import_scene.fbx(filepath=os.path.join(KOK, "02-hareketler/siluet-govde.fbx"), automatic_bone_orientation=False)
        yeni = [o for o in bpy.data.objects if o not in once]
        arm = [o for o in yeni if o.type == "ARMATURE"][0]
        mesler = [o for o in yeni if o.type == "MESH"]
        for m in mesler:
            m.data.materials.clear(); m.data.materials.append(siyah)
            for poly in m.data.polygons:
                poly.material_index = 0
            m.animation_data_clear()
        arm.animation_data_clear()
        L = arm.matrix_world @ kemik(arm, "LeftArm").head; Rr = arm.matrix_world @ kemik(arm, "RightArm").head
        v = L - Rr; v.z = 0
        arm.rotation_euler.z -= math.atan2(v.y, v.x)
        bpy.context.view_layer.update()
        FIG.append((arm, mesler, arm.rotation_euler.z))
    bpy.ops.object.camera_add(location=(0, -14, 1), rotation=(math.radians(90), 0, 0))
    kam = bpy.context.active_object; sc.camera = kam; kam.data.type = "ORTHO"
    ASPECT = 1600 / 900
    for ad, G in GRUPLAR.items():
        FG = FIG[:len(G["figurler"])]
        for k_, f in enumerate(FIG):
            for m in f[1]:
                m.hide_render = k_ >= len(FG)
        for (arm, mesler, rot), P in zip(FG, G["figurler"]):
            figur_pozla(arm, mesler, P, rot)
        olcu = []
        for j in range(len(FG) - 1):
            olcu.append(hizala(FG[j][0], FG[j][1], FG[j + 1][0], FG[j + 1][1], G["temas"][j]))
            # kapak deneme 2 (kullanici "hic begenmedim"): REF-056 kumesi sikisik, kisiler ic ice -> ek bindirme (m)
            if G.get("bindirme"):
                for f in FG[j + 1:]:
                    f[0].location.x -= G["bindirme"]
                bpy.context.view_layer.update()
        tum = [m for f in FG for m in f[1]]
        alt, ust = dunya_kutusu(tum)
        gen, yuk = ust.x - alt.x, ust.z - alt.z
        olc = 2.3
        if yuk > olc * 0.88: olc = yuk / 0.88
        if gen > olc * ASPECT * 0.9: olc = gen / (ASPECT * 0.9)
        kam.data.ortho_scale = olc * ASPECT
        kam.location = ((alt.x + ust.x) / 2, -14, alt.z - olc * 0.05 + olc / 2)
        bpy.context.view_layer.update()
        YERLESIM.setdefault("grup", {})[ad] = {"cerceve_m": round(olc, 3), "gen_m": round(gen, 3), "yuk_m": round(yuk, 3), "temas": olcu}
        log("grup", ad, "gen", round(gen, 2), "yuk", round(yuk, 2), "temas", olcu)
        yaz(sc, dosya % ad)
        if not kisi_basi:
            continue
        # kisi basi ayri maske (ayni kamera): kapakta her kisinin kendi beyaz cizgisi (REF-056'da kisiler arasi ince beyaz hat)
        for j in range(len(FG)):
            for k_, f in enumerate(FG):
                for m in f[1]:
                    m.hide_render = (k_ != j)
            yaz(sc, "kapak-grup-%s-%d.png" % (ad, j))
        for f in FG:
            for m in f[1]:
                m.hide_render = False




def kapak_sahne():
    """1280x720: gok + tek serit (yol, mezar tasi korkuluk, kapi) - kamera sola kayik, kapi sagda (REF-056 kapagindaki gibi)"""
    rnd = random.Random(57)
    for katman in ("gok", "serit"):
        sc = bos_sahne(w=1280, h=720, saydam=(katman == "serit"), ornek=min(ORNEK, 64))
        kam = kamera(sc); kam.location.x = -4.3
        sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.15
        if katman == "gok":
            ay_ve_gok(rnd); uzak_tepeler(rnd)
            yaz(sc, "kapak-gok.png"); continue
        zemin_ve_yol(rnd, "p1")
        kapi_cadi("p1", tabela_yazi=False)
        R = lin(hex3(OYUNCU["p1"]))
        isik("AREA", (-4, -1.5, 6.5), 420, lin(hex3("#d8c8ff")), 6, yon=(0, KAP["y"] * 0.6, 0))
        isik("AREA", (-3, 3, 3), 260, acik(R, 0.2), 3, yon=(0, KAP["y"], 2))
        isik("AREA", (3, 3, 3), 220, lin(hex3("#b48cff")), 3, yon=(0, KAP["y"], 2))
        isik("AREA", (0, KAP["y"] + 3, 5), 500, acik(R, 0.1), 5, yon=(0, KAP["y"], 1))
        Y, W_, H_, KK = KAP["y"], KAP["w"], KAP["h"], KAP["kule"]
        ic = W_ / 2 - KK
        bpy.context.view_layer.update()
        px = [world_to_camera_view(sc, kam, Vector(q)) for q in ((-ic, Y, 0), (ic, Y, 0), (-ic, Y, H_), (ic, Y, H_))]
        xs = [q.x * 1280 for q in px]; ys = [(1 - q.y) * 720 for q in px]
        YERLESIM["kapak_aciklik"] = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
        log("kapak aciklik", YERLESIM["kapak_aciklik"])
        yaz(sc, "kapak-serit.png")


# ------------------------------------------------------------------ KAPAK OGELERI (kullanici 19 Eki: kapakta yazi yalniz TETRIS MODE + HALLOWEEN,
# referanstaki etiket/NEW! yerleri GORUNTU ile dolar) -> yuzu oyulmus 3B balkabagi fenerleri, saydam PNG
def kapak_ogeleri():
    for ad, dizilim in (("kapak-kabak.png", [(0, 0, 1.0, True)]),
                        ("kapak-kabak-kume.png", [(0, 0, 1.0, True), (-1.25, 0.5, 0.62, True), (1.15, 0.4, 0.55, False)])):
        sc = bos_sahne(w=900, h=700, saydam=True, ornek=min(ORNEK, 64))
        sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.3
        kabuk = mat_jole("kk", lin(hex3("#ff6a10")), emis=0.12, purluk=0.35)
        sap = mat_duz("ks", lin(hex3("#3a5a12")), 0.6)
        yuz = mat_emis("ky", lin(hex3("#ffd23a")), 24)
        for x, y, r, yz in dizilim:
            kabak((x, y, 0), r, kabuk, sap, yuz if yz else None)
        isik("AREA", (-2, -4, 3), 300, lin(hex3("#ffd8b0")), 4, yon=(0, 0, 0.6))
        isik("AREA", (3, -2, 1.5), 160, lin(hex3("#b48cff")), 3, yon=(0, 0, 0.6))
        bpy.ops.object.camera_add(location=(0, -9, 1.2), rotation=(math.radians(86), 0, 0))
        kam = bpy.context.active_object; sc.camera = kam; kam.data.lens = 50
        yaz(sc, ad)


# ------------------------------------------------------------------ ana akis (cadi)
# tek kisilik poz maskeleri: varlik.py poz_maskeleri() (--pozlar pozlar-05.json). 3 kisilik grup maskesi iptal (kullanici 19 Eki).
if YALNIZ in ("hepsi", "poz"):
    poz_maskeleri()
if YALNIZ in ("hepsi", "sahne"):
    sahne_cadi()
    for o_ in OYUNCU:
        panel_cadi(o_)
if YALNIZ == "kapak":
    kapak_ogeleri()
if YALNIZ == "kapak2":
    kapak_sahne()
    grup_maskeleri()
if YALNIZ == "grup":        # 7. video (REF-058, CO-OP): duvar basina 2 kisilik TEK siluet -> grup/<ad>.png
    grup_maskeleri("grup/%s.png", kisi_basi=False)
json.dump(YERLESIM, open(os.path.join(CIKTI, "yerlesim.json"), "w"), indent=1)
log("bitti (cadi)")
