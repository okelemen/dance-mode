"""HUMAN TETRIS 25. video (REFERANSSIZ, 1v1) - GUNDUZ OKUL SPOR SALONU, CILALI 3D OYUN GORUNUMU. varlik.py calistirir (--mod salon).

STIL (kullanici 11 Kas 2026, onizleme 1 sonrasi): foto-gercekci salon REDDEDILDI ("gercek hayattan alinan bir kesit ... olmaz") ->
"cilali 3D oyun gorunumu": canli doygun renkler, yuvarlak tombul hatlar (her kutu pahli), parlak oyuncak plastik / cilali yuzey,
ama gercek isik-golge-parlama (Cycles) + isik hare (glare). Foto dokusu yok (ambientCG dokulari kullanilmaz), desenler prosedurel ve sade.

POZ-DUVARI TALIMATLAR §2b 2. mekan + §4 GERCEKCI GORUNUM (kullanici 11 Kas 2026: "cocuklarin pastel boyayla resim cizmis gibi
seyler yapma ... biraz daha gercekci olmaya bak"). 24'un (varlik-havuz.py) farki: isiksiz emission yuzey yok; PBR malzeme
(CC0 ambientCG dokulari doku/), gercek isik (pencereden gunes + tavan lambalari, golge, yansima, dolayli isik), AgX.
Oyuncu rengi yalniz aksanlarda: serit bandi, yan minderler, kapi yastiklari. Kendi isigi olan nesneler (lamba, skor tabelasi) emission.

Katmanlar 24 ile ayni (motor uyumu): gok.png = salonun uzak kismi (ortada kamera, perspektif), serit-p1/p2.png = oyuncunun
yakin zemini + minder + kapi. Isik iki katmanda ayni olsun diye butun salon serit sahnesinde de kurulur, uzak kismi holdout
(saydam ama golge/yansima verir). Gecis cizgisi y = GECIS (beyaz saha cizgisinin ortasi).
OUT ani (mobil paket md. 2) motorda: karakter yandaki mindere duser, duduk.
Telif: genel spor salonu ogeleri; yazi, logo, okul/takim adi yok.

Ciktilar: gok.png, serit-p1/p2.png, panel-p1/p2.png, yerlesim.json; kapak modu (--yalniz kapak): kapak-gok.png, kapak-serit-p1/p2.png
"""

import random
YERLESIM.clear()
KAPAK = YALNIZ == "kapak"
POZLAMA = float(arg("--pozlama", arg("--kapak-pozlama", "0")))
ON_EK = "kapak-" if KAPAK else ""
DOKU = os.path.join(KOK, "03-motor", "tetris-pvp", "doku")
KAP = {"y": 8.0, "w": 3.4, "h": 3.7, "kalin": 0.30}
KAM = {"z": 2.3, "egim": 5.0, "lens": 18.0, "sensor": 24.0}
if KAPAK:
    KAM.update({"z": float(arg("--kapak-z", "2.0")), "egim": float(arg("--kapak-egim", "3.0")), "lens": float(arg("--kapak-lens", "16.0"))})
YOL_YARI = 2.6
GECIS = 11.0            # serit zemini burada biter, otesi gok.png
ARKA_Y = 20.0           # arka duvar
YAN_X = 16.0            # yan duvarlar
TAVAN = 9.0
SERIT = {
    "p1": {"ana": "#1e8cff", "koyu": "#0a3fa8", "minder": "#1a78f0"},
    "p2": {"ana": "#ff3aa8", "koyu": "#a8105e", "minder": "#ff2a98"},
}
OKUL = {"lacivert": "#3a2fc8", "sari": "#ffcc1e", "kirmizi": "#ff3b4e"}      # oyun paleti: canli mor-lacivert, sari, kirmizi


# ------------------------------------------------------------------ sahne / isik
def salon_sahnesi(w, h, saydam):
    sc = bos_sahne(w=w, h=h, saydam=saydam, ornek=ORNEK, doygun=False)
    # onizleme 2 (oyun gorunumu): AgX doygun renkleri pastele cekti (tribun, minderler soluk) -> Standard (seri notu: varlik.py deneme 1)
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.exposure = POZLAMA
    sc.cycles.max_bounces = 6; sc.cycles.diffuse_bounces = 3; sc.cycles.glossy_bounces = 3
    sc.cycles.transmission_bounces = 2; sc.cycles.transparent_max_bounces = 8
    sc.cycles.use_light_tree = True
    # dunya: pencereden gorunen gunduz gogu (Nishita) - salonun icine yalniz pencerelerden girer
    nt = sc.world.node_tree; nt.nodes.clear()
    gk = nt.nodes.new("ShaderNodeTexSky"); gk.sky_type = "NISHITA"
    gk.sun_elevation = math.radians(38); gk.sun_rotation = math.radians(-60); gk.air_density = 1.0; gk.dust_density = 0.6
    bg = nt.nodes.new("ShaderNodeBackground"); bg.inputs[1].default_value = 0.35
    o = nt.nodes.new("ShaderNodeOutputWorld")
    nt.links.new(gk.outputs[0], bg.inputs[0]); nt.links.new(bg.outputs[0], o.inputs[0])
    # oyun gorunumu: lamba ve parlama noktalarinda yumusak hare
    sc.use_nodes = True; sc.render.use_compositing = True; ct = sc.node_tree; ct.nodes.clear()
    rl = ct.nodes.new("CompositorNodeRLayers"); gl = ct.nodes.new("CompositorNodeGlare"); co = ct.nodes.new("CompositorNodeComposite")
    gl.glare_type = "FOG_GLOW"; gl.quality = "HIGH"; gl.threshold = 1.2; gl.size = 7; gl.mix = 0.0
    ct.links.new(rl.outputs["Image"], gl.inputs[0]); ct.links.new(gl.outputs[0], co.inputs[0])
    if saydam:
        ct.links.new(rl.outputs["Alpha"], co.inputs[1])
    return sc


def kamera(sc, x=0.0):
    rx = math.radians(90 - KAM["egim"])
    bpy.ops.object.camera_add(location=(x, 0, KAM["z"]), rotation=(rx, 0, 0))
    kam = bpy.context.active_object; sc.camera = kam
    kam.data.sensor_fit = "VERTICAL"; kam.data.sensor_height = KAM["sensor"]; kam.data.lens = KAM["lens"]
    kam.data.clip_end = 200
    return kam


def isiklar():
    # gunes: sag yan duvarin pencerelerinden iceri, zemine pencere lekeleri dusurur
    bpy.ops.object.light_add(type="SUN", location=(0, 0, 20))
    g = bpy.context.active_object; g.data.energy = 4.2; g.data.angle = math.radians(0.8)
    g.data.color = lin(hex3("#fff1dc"))
    g.rotation_euler = Vector((-0.78, -0.30, -0.55)).to_track_quat("-Z", "Y").to_euler()
    # tavan lambalari (high-bay): gorunur disk emission, isigi alan lambasi verir
    govde = mat_pbr("lamba_g", "#3a3d42", 0.4, metal=1.0)
    disk = mat_emis("lamba_d", lin(hex3("#fff4e2")), 18.0)
    for x in (-10.5, -3.5, 3.5, 10.5):
        for y in (2.0, 7.0, 12.0, 17.0):
            boru((x, y, TAVAN - 0.05), (x, y, TAVAN - 1.0), 0.02, govde)
            c = boru((x, y, TAVAN - 1.0), (x, y, TAVAN - 1.32), 0.28, govde)
            bpy.ops.mesh.primitive_circle_add(vertices=32, radius=0.25, fill_type="NGON", location=(x, y, TAVAN - 1.33))
            bpy.context.active_object.data.materials.append(disk)
            L = isik("AREA", (x, y, TAVAN - 1.4), 520, lin(hex3("#fff0dc")), boy=0.6, yon=(x, y, 0))


# ------------------------------------------------------------------ malzemeler
def mat_pbr(ad, renk, purluk, metal=0.0, kaplama=0.0, bump=None):
    m = bpy.data.materials.new(ad); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*lin(hex3(renk)), 1)
    b.inputs["Roughness"].default_value = purluk; b.inputs["Metallic"].default_value = metal
    b.inputs["Coat Weight"].default_value = kaplama; b.inputs["Coat Roughness"].default_value = 0.08
    if bump:                                                     # (olcek, guc): ince gozenek / vinil dokusu
        nt = m.node_tree
        ns = nt.nodes.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value = bump[0]; ns.inputs["Detail"].default_value = 8
        bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = bump[1]; bp.inputs["Distance"].default_value = 0.02
        nt.links.new(ns.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    return m


def mat_doku(ad, kod, olcek, duzlem="XY", ton=None, purluk_kat=1.0, kaplama=0.0, normal=1.0, ofset=(0.0, 0.0), parlak=1.0):
    """ambientCG dokusu, dunya koordinatindan duzlemsel izdusum (parcalar arasinda desen kesintisiz).
    ton=(koyu, acik): renk haritasinin parlakligi bu iki boya rengi arasina eslenir (gri blok -> boyali blok)."""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry"); sp = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(geo.outputs["Position"], sp.inputs[0])
    cb = nt.nodes.new("ShaderNodeCombineXYZ")
    nt.links.new(sp.outputs[duzlem[0]], cb.inputs[0]); nt.links.new(sp.outputs[duzlem[1]], cb.inputs[1])
    mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (1 / olcek, 1 / olcek, 1)
    mp.inputs["Location"].default_value = (ofset[0], ofset[1], 0)
    nt.links.new(cb.outputs[0], mp.inputs[0])

    def harita(tur, renkli):
        t = nt.nodes.new("ShaderNodeTexImage")
        t.image = bpy.data.images.load(os.path.join(DOKU, kod, "%s_1K-JPG_%s.jpg" % (kod, tur)), check_existing=True)
        if not renkli:
            t.image.colorspace_settings.name = "Non-Color"
        nt.links.new(mp.outputs[0], t.inputs[0])
        return t
    c = harita("Color", True)
    if ton:
        bw = nt.nodes.new("ShaderNodeRGBToBW"); nt.links.new(c.outputs[0], bw.inputs[0])
        rp = nt.nodes.new("ShaderNodeValToRGB"); nt.links.new(bw.outputs[0], rp.inputs[0])
        rp.color_ramp.elements[0].position = 0.12; rp.color_ramp.elements[1].position = 0.55
        rp.color_ramp.elements[0].color = (*lin(hex3(ton[0])), 1); rp.color_ramp.elements[1].color = (*lin(hex3(ton[1])), 1)
        nt.links.new(rp.outputs[0], b.inputs["Base Color"])
    elif parlak != 1.0:
        hv = nt.nodes.new("ShaderNodeHueSaturation"); hv.inputs["Value"].default_value = parlak
        nt.links.new(c.outputs[0], hv.inputs["Color"]); nt.links.new(hv.outputs[0], b.inputs["Base Color"])
    else:
        nt.links.new(c.outputs[0], b.inputs["Base Color"])
    r = harita("Roughness", False)
    mt = nt.nodes.new("ShaderNodeMath"); mt.operation = "MULTIPLY"; mt.inputs[1].default_value = purluk_kat
    nt.links.new(r.outputs[0], mt.inputs[0]); nt.links.new(mt.outputs[0], b.inputs["Roughness"])
    n = harita("NormalGL", False)
    nm = nt.nodes.new("ShaderNodeNormalMap"); nm.inputs["Strength"].default_value = normal
    nt.links.new(n.outputs[0], nm.inputs["Color"]); nt.links.new(nm.outputs[0], b.inputs["Normal"])
    b.inputs["Coat Weight"].default_value = kaplama; b.inputs["Coat Roughness"].default_value = 0.06
    return m


def mat_tahta(ad, renk1, renk2, harc, olcek=(1.6, 0.11), duzlem="XY", kaplama=0.7, purluk=0.22):
    """oyun parkesi / tahta: prosedurel uzun tahta seritleri, iki ton + ince koyu derz, cilali ust kaplama (foto dokusu yok)"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry"); sp = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(geo.outputs["Position"], sp.inputs[0])
    cb = nt.nodes.new("ShaderNodeCombineXYZ")
    # tahta boyu ikinci eksen boyunca: bricks X'te uzun -> (v, u) verilir
    nt.links.new(sp.outputs[duzlem[1]], cb.inputs[0]); nt.links.new(sp.outputs[duzlem[0]], cb.inputs[1])
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.inputs["Color1"].default_value = (*lin(hex3(renk1)), 1); br.inputs["Color2"].default_value = (*lin(hex3(renk2)), 1)
    br.inputs["Mortar"].default_value = (*lin(hex3(harc)), 1); br.inputs["Scale"].default_value = 1.0
    br.inputs["Mortar Size"].default_value = 0.006; br.inputs["Brick Width"].default_value = olcek[0]; br.inputs["Row Height"].default_value = olcek[1]
    br.offset = 0.37; br.squash = 1.0
    nt.links.new(cb.outputs[0], br.inputs["Vector"]); nt.links.new(br.outputs["Color"], b.inputs["Base Color"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.25; bp.invert = True
    nt.links.new(br.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = purluk; b.inputs["Coat Weight"].default_value = kaplama; b.inputs["Coat Roughness"].default_value = 0.04
    return m


def mat_blok(ad, renk1, renk2, harc, duzlem):
    """oyun duvari: iri yuvarlak hatli boyali bloklar, iki canli ton, beyaz derz"""
    # onizleme 2: bloklar dikey diziliyordu (mat_tahta eksenleri cevirir) -> duzlem ters verilir, bloklar yatay
    m = mat_tahta(ad, renk1, renk2, harc, olcek=(0.8, 0.4), duzlem=duzlem[::-1], kaplama=0.25, purluk=0.4)
    br = [n for n in m.node_tree.nodes if n.type == "TEX_BRICK"][0]
    br.inputs["Mortar Size"].default_value = 0.035; br.inputs["Mortar Smooth"].default_value = 0.6; br.offset = 0.5
    m.node_tree.nodes["Bump"].inputs["Strength"].default_value = 0.5
    return m


def kutu(ad, merkez, boyut, mat, egim=0.025, seg=3):
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


# ------------------------------------------------------------------ SALON (her iki katmanda; serit sahnesinde uzak kisim holdout)
def salon(serit_modu, rnd):
    uzak = []                                                   # serit sahnesinde holdout olacaklar
    parke = mat_tahta("parke", "#f0a24a", "#e48a34", "#9a4e1c")
    boya_beyaz = mat_pbr("cizgi_b", "#f4f1ea", 0.35, kaplama=0.4)
    boya_lac = mat_pbr("cizgi_l", OKUL["lacivert"], 0.4, kaplama=0.4)
    # zemin: yakin (serit katmaninda gorunur) + uzak
    duz("zemin_yakin", -YAN_X, YAN_X, -4, GECIS, 0, parke)
    uzak.append(duz("zemin_uzak", -YAN_X, YAN_X, GECIS, ARKA_Y, 0, parke))
    # saha cizgileri: gecis cizgisi (iki katmanin birlestigi yer) + dip cizgi + boyali anahtar alani
    uzak.append(duz("gecis_u", -YAN_X + 0.6, YAN_X - 0.6, GECIS, GECIS + 0.07, 0.002, boya_beyaz))
    duz("gecis_y", -YAN_X + 0.6, YAN_X - 0.6, GECIS - 0.07, GECIS, 0.002, boya_beyaz)
    uzak.append(duz("dip", -YAN_X + 0.6, YAN_X - 0.6, ARKA_Y - 1.6, ARKA_Y - 1.52, 0.002, boya_beyaz))
    uzak.append(duz("anahtar", -2.45, 2.45, ARKA_Y - 1.52 - 5.8, ARKA_Y - 1.52, 0.0015, boya_lac))
    for x in (-2.45, 2.45):
        uzak.append(duz("anahtar_k", x - 0.04, x + 0.04, ARKA_Y - 7.32, ARKA_Y - 1.52, 0.002, boya_beyaz))
    uzak.append(duz("anahtar_u", -2.49, 2.49, ARKA_Y - 7.36, ARKA_Y - 7.28, 0.002, boya_beyaz))
    uzak += arka_duvar(rnd) + yan_duvarlar(rnd) + tavan(rnd) + tribun(rnd)
    if serit_modu:                                              # yakin zemin disinda salonun her parcasi (lambalar dahil) holdout
        for o in bpy.data.objects:
            if o.type == "MESH" and o.name.split(".")[0] not in ("zemin_yakin", "gecis_y"):
                o.is_holdout = True
    return uzak


def blok_duvar_mat(ad, duzlem):
    return mat_blok(ad, "#36b4f2", "#28a2e6", "#eaf8ff", duzlem)


def duvar_pencereli(ad, eksen, sabit, a0, a1, pencereler, z_alt, z_ust, mat, cerceve):
    """dikey duvar: pencere araliklarinda bosluk birakir (gunes iceri girer). eksen 'x' -> duvar XZ duzleminde (y=sabit)."""
    ob = []
    def parca(u0, u1, z0, z1):
        if u1 - u0 < 0.01 or z1 - z0 < 0.01:
            return
        if eksen == "x":
            ob.append(kutu(ad, ((u0 + u1) / 2, sabit, (z0 + z1) / 2), (u1 - u0, 0.3, z1 - z0), mat))
        else:
            ob.append(kutu(ad, (sabit, (u0 + u1) / 2, (z0 + z1) / 2), (0.3, u1 - u0, z1 - z0), mat))
    parca(a0, a1, 0, z_alt); parca(a0, a1, z_ust, TAVAN + 0.2)
    u = a0
    for (p0, p1) in pencereler:
        parca(u, p0, z_alt, z_ust); u = p1
        # pencere kayitlari (metal) - 3 dikey + 1 yatay
        for q in (0.0, 1 / 3, 2 / 3, 1.0):
            uu = p0 + (p1 - p0) * q
            if eksen == "x":
                ob.append(kutu("kayit", (uu, sabit, (z_alt + z_ust) / 2), (0.06, 0.12, z_ust - z_alt), cerceve))
            else:
                ob.append(kutu("kayit", (sabit, uu, (z_alt + z_ust) / 2), (0.12, 0.06, z_ust - z_alt), cerceve))
        if eksen == "x":
            ob.append(kutu("kayit_y", ((p0 + p1) / 2, sabit, (z_alt + z_ust) / 2), (p1 - p0, 0.12, 0.06), cerceve))
        else:
            ob.append(kutu("kayit_y", (sabit, (p0 + p1) / 2, (z_alt + z_ust) / 2), (0.12, p1 - p0, 0.06), cerceve))
    parca(u, a1, z_alt, z_ust)
    return ob


def duvar_minderleri(eksen, sabit, a0, a1, renk):
    """duvar dibi koruma minderleri (vinil, 2,1 m), panel araliklari gercek bosluk"""
    mat = mat_pbr("duvar_minder", renk, 0.55, kaplama=0.15, bump=(180, 0.08))
    ob = []; u = a0
    while u < a1 - 0.2:
        u1 = min(a1, u + 1.2)
        if eksen == "x":
            ob.append(kutu("dm", ((u + u1) / 2 - 0.01, sabit - 0.2, 1.1), (u1 - u - 0.03, 0.09, 1.9), mat, egim=0.03, seg=3))
        else:
            ob.append(kutu("dm", (sabit + (0.2 if sabit < 0 else -0.2), (u + u1) / 2, 1.1), (0.09, u1 - u - 0.03, 1.9), mat, egim=0.03, seg=3))
        u = u1
    return ob


def arka_duvar(rnd):
    mat = blok_duvar_mat("blok_arka", "XZ"); cer = mat_pbr("pencere_c", "#5b6068", 0.35, metal=1.0)
    pen = [(-13.5, -10.5), (-8.5, -5.5), (5.5, 8.5), (10.5, 13.5)]
    ob = duvar_pencereli("arka", "x", ARKA_Y + 0.15, -YAN_X, YAN_X, pen, 6.2, 8.4, mat, cer)
    # alt bant boyasi (okul lacivert) - blok duvarin 2,1-2,6 m arasi
    ob.append(kutu("bant", (0, ARKA_Y - 0.01, 2.35), (2 * YAN_X, 0.02, 0.5), mat_pbr("bant", OKUL["lacivert"], 0.45)))
    # skor tabelasi (yazisiz: sonuk LED noktalari) + duvar saati
    ob.append(kutu("tabela", (0, ARKA_Y - 0.2, 6.9), (3.6, 0.3, 1.5), mat_pbr("tabela_k", "#121417", 0.4, metal=0.3), egim=0.04, seg=2))
    led = mat_emis("led", lin(hex3("#ff3a1e")), 2.2); led_s = mat_emis("led_s", lin(hex3("#3a0a06")), 1.0)
    for i in range(26):
        for j in range(7):
            yanik = (i in (3, 4, 5, 20, 21, 22) and j in (1, 2, 3, 4, 5))
            kure((-1.6 + i * 0.128, ARKA_Y - 0.37, 6.45 + j * 0.13), 0.035, led if yanik else led_s, sub=1)
    saat = mat_pbr("saat", "#f7f5ef", 0.3); saat_c = mat_pbr("saat_c", "#202226", 0.3, metal=0.6)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.42, depth=0.08, location=(-6.2, ARKA_Y - 0.06, 5.2), rotation=(math.radians(90), 0, 0))
    o = bpy.context.active_object; o.data.materials.append(saat_c); ob.append(o)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.37, depth=0.09, location=(-6.2, ARKA_Y - 0.07, 5.2), rotation=(math.radians(90), 0, 0))
    o = bpy.context.active_object; o.data.materials.append(saat); ob.append(o)
    for (u, l) in ((math.radians(60), 0.18), (math.radians(-30), 0.28)):
        ob.append(boru((-6.2, ARKA_Y - 0.13, 5.2), (-6.2 + l * math.sin(u), ARKA_Y - 0.13, 5.2 + l * math.cos(u)), 0.012, saat_c))
    # sampiyonluk flamalari (yazisiz kece, yildiz amblem)
    for k, x in enumerate((-12.0, -9.6, -4.2, 4.2, 9.6, 12.0)):
        renk = (OKUL["lacivert"], OKUL["kirmizi"], OKUL["lacivert"], OKUL["kirmizi"], OKUL["lacivert"], OKUL["kirmizi"])[k]
        kece = mat_pbr("kece%d" % k, renk, 0.85, bump=(60, 0.15))
        me = bpy.data.meshes.new("flama")
        me.from_pydata([(x - 0.7, ARKA_Y - 0.12, 5.6), (x + 0.7, ARKA_Y - 0.12, 5.6), (x + 0.7, ARKA_Y - 0.12, 4.1), (x, ARKA_Y - 0.12, 3.6),
                        (x - 0.7, ARKA_Y - 0.12, 4.1)], [], [[0, 1, 2, 3, 4]]); me.update()
        o = bpy.data.objects.new("flama", me); bpy.context.collection.objects.link(o); o.data.materials.append(kece); ob.append(o)
        y_ = mat_pbr("yildiz", OKUL["sari"], 0.7)
        nok = []
        for i in range(10):
            r = 0.32 if i % 2 == 0 else 0.13; a = math.pi / 2 + i * math.pi / 5
            nok.append((x + r * math.cos(a), ARKA_Y - 0.14, 4.75 + r * math.sin(a)))
        me = bpy.data.meshes.new("yildiz"); me.from_pydata(nok, [], [list(range(10))]); me.update()
        o = bpy.data.objects.new("yildiz", me); bpy.context.collection.objects.link(o); o.data.materials.append(y_); ob.append(o)
        ob.append(boru((x - 0.75, ARKA_Y - 0.1, 5.62), (x + 0.75, ARKA_Y - 0.1, 5.62), 0.02, cer))
    return ob


def yan_duvarlar(rnd):
    ob = []
    cer = mat_pbr("pencere_c2", "#5b6068", 0.35, metal=1.0)
    pen = [(y, y + 2.6) for y in (-1.0, 3.0, 7.0, 11.0, 15.0)]
    ahsap = mat_pbr("isvec", "#f2b04a", 0.3, kaplama=0.6)
    ip = mat_pbr("ip", "#c9b48a", 0.9, bump=(90, 0.4))
    for s in (-1, 1):
        x = s * (YAN_X + 0.15)
        ob += duvar_pencereli("yan", "y", x, -4, ARKA_Y + 0.3, pen, 5.6, 8.2, blok_duvar_mat("blok_yan%d" % s, "YZ"), cer)
        ob.append(kutu("bant", (s * (YAN_X - 0.01), ARKA_Y / 2 - 2, 2.35), (0.02, ARKA_Y + 4, 0.5), mat_pbr("bant2", OKUL["lacivert"], 0.45)))
        ob += duvar_minderleri("y", s * YAN_X, -4, 4.0, OKUL["lacivert"])
        # isvec merdiveni (duvar barlari): 4 bolum, ahsap dikme + yuvarlak basamak
        for b in range(4):
            y0 = 5.0 + b * 1.1
            for d in (y0, y0 + 0.95):
                ob.append(kutu("bar_d", (s * (YAN_X - 0.12), d, 1.35), (0.1, 0.08, 2.7), ahsap))
            for k in range(16):
                ob.append(boru((s * (YAN_X - 0.14), y0, 0.18 + k * 0.16), (s * (YAN_X - 0.14), y0 + 0.95, 0.18 + k * 0.16), 0.018, ahsap))
        ob += duvar_minderleri("y", s * YAN_X, 9.6, ARKA_Y, OKUL["lacivert"])
        # potalar (yan duvara katlanir cam pano): yan saha potalari
        ob += pota(s, 15.5)
        # tirmanma halatlari (tavandan)
        for k in range(3):
            y = 10.0 + k * 0.9
            ob.append(boru((s * 12.5, y, TAVAN), (s * 12.5, y, 0.5), 0.022, ip))
            kure((s * 12.5, y, 0.5), 0.05, ip)
    return ob


def pota(s, y):
    ob = []
    cel = mat_pbr("pota_c", "#2d3036", 0.4, metal=1.0)
    cam = bpy.data.materials.new("pano_cam"); cam.use_nodes = True; bb = cam.node_tree.nodes["Principled BSDF"]
    bb.inputs["Roughness"].default_value = 0.05; bb.inputs["Transmission Weight"].default_value = 0.9
    bb.inputs["Base Color"].default_value = (0.9, 0.95, 0.97, 1); bb.inputs["IOR"].default_value = 1.5
    x_pano = s * (YAN_X - 1.6)
    # duvara kollu tasiyici
    for z in (3.2, 4.2):
        ob.append(boru((s * (YAN_X - 0.1), y - 0.5, z), (x_pano + s * 0.05, y - 0.5, z), 0.05, cel))
        ob.append(boru((s * (YAN_X - 0.1), y + 0.5, z), (x_pano + s * 0.05, y + 0.5, z), 0.05, cel))
    ob.append(kutu("pano", (x_pano, y, 3.55), (0.03, 1.8, 1.05), cam))
    beyaz = mat_pbr("pano_cizgi", "#ffffff", 0.3)
    for (yy, zz, dy, dz) in ((y, 3.1, 0.6, 0.05), (y - 0.3, 3.32, 0.05, 0.45), (y + 0.3, 3.32, 0.05, 0.45), (y, 3.54, 0.6, 0.05)):
        ob.append(kutu("pano_k", (x_pano - s * 0.02, yy, zz), (0.01, dy, dz), beyaz))
    turuncu = mat_pbr("cember", "#e2571c", 0.35, metal=0.6)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.23, minor_radius=0.012, location=(x_pano - s * 0.3, y, 3.05))
    o = bpy.context.active_object; o.data.materials.append(turuncu); ob.append(o)
    ag = mat_pbr("file", "#f2f2f2", 0.8)
    for i in range(12):
        a = i * math.pi / 6
        ob.append(boru((x_pano - s * 0.3 + 0.23 * math.cos(a), y + 0.23 * math.sin(a), 3.05),
                       (x_pano - s * 0.3 + 0.13 * math.cos(a + 0.5), y + 0.13 * math.sin(a + 0.5), 2.62), 0.005, ag))
    return ob


def tavan(rnd):
    ob = []
    sac = mat_pbr("tavan_sac", "#f2f6fb", 0.5)
    ob.append(kutu("tavan", (0, ARKA_Y / 2 - 2, TAVAN + 0.1), (2 * YAN_X + 1, ARKA_Y + 6, 0.2), sac))
    celik = mat_pbr("makas", "#ffcc1e", 0.3, kaplama=0.5)
    for y in (0.0, 4.5, 9.0, 13.5, 18.0):                    # celik makaslar (alt + ust kusak + diyagonal)
        ob.append(boru((-YAN_X, y, TAVAN - 0.15), (YAN_X, y, TAVAN - 0.15), 0.07, celik))
        ob.append(boru((-YAN_X, y, TAVAN - 1.0), (YAN_X, y, TAVAN - 1.0), 0.06, celik))
        x = -YAN_X; i = 0
        while x < YAN_X - 0.01:
            z0, z1 = (TAVAN - 1.0, TAVAN - 0.15) if i % 2 == 0 else (TAVAN - 0.15, TAVAN - 1.0)
            ob.append(boru((x, y, z0), (x + 1.6, y, z1), 0.03, celik)); x += 1.6; i += 1
    # (sarili bolme perdesi kaldirildi - onizleme 1: ust kadrajda agir siyah bant)
    ob += flama_dizileri(rnd) + balonlar(rnd)
    return ob


def flama_dizileri(rnd):
    """tavandan sarkan ucgen flama dizileri (oyun / senlik havasi, ekran dolu kurali md. 7)"""
    ob = []
    renk = [mat_pbr("fl%d" % i, c, 0.35, kaplama=0.3) for i, c in enumerate(("#ff3b4e", "#ffcc1e", "#1e9cff", "#2fd06a", "#ff4fc0", "#ff8a1e"))]
    ip = mat_pbr("fl_ip", "#ffffff", 0.5)
    for (y, z, sark) in ((3.0, TAVAN - 1.4, 0.9), (8.5, TAVAN - 1.3, 1.0), (14.0, TAVAN - 1.2, 0.9)):
        n = 26; onc = None
        for i in range(n + 1):
            q = i / n; x = -YAN_X + 2 * YAN_X * q; zz = z - sark * 4 * q * (1 - q)
            if onc:
                ob.append(boru((onc[0], y, onc[1]), (x, y, zz), 0.012, ip))
                mx_, mz = (onc[0] + x) / 2, (onc[1] + zz) / 2
                me = bpy.data.meshes.new("flama_u")
                me.from_pydata([(mx_ - 0.42, y, mz), (mx_ + 0.42, y, mz), (mx_, y, mz - 0.7)], [], [[0, 1, 2]]); me.update()
                o = bpy.data.objects.new("flama_u", me); bpy.context.collection.objects.link(o); o.data.materials.append(renk[i % len(renk)])
                sl = o.modifiers.new("kal", "SOLIDIFY"); sl.thickness = 0.02
                ob.append(o)
            onc = (x, zz)
    return ob


def balonlar(rnd):
    """tribun koselerinde ve tavanda parlak balon kumeleri (oyuncak plastik)"""
    ob = []
    renk = [mat_pbr("bl%d" % i, c, 0.12, kaplama=1.0) for i, c in enumerate(("#ff3b4e", "#ffcc1e", "#1e9cff", "#2fd06a", "#ff4fc0", "#8a5aff"))]
    ip = mat_pbr("bl_ip", "#ffffff", 0.5)
    for (cx_, cy_, cz_) in ((-12.5, ARKA_Y - 5.2, 3.2), (12.5, ARKA_Y - 5.2, 3.2), (-6.0, 12.0, 6.6), (6.5, 13.0, 6.9), (0.0, 16.5, 7.4)):
        for k in range(7):
            p_ = (cx_ + rnd.uniform(-0.5, 0.5), cy_ + rnd.uniform(-0.4, 0.4), cz_ + rnd.uniform(-0.3, 0.6))
            b_ = kure(p_, rnd.uniform(0.32, 0.42), rnd.choice(renk), sub=3); b_.scale = (1, 1, 1.15); ob.append(b_)
            ob.append(boru((p_[0], p_[1], p_[2] - 0.45), (cx_, cy_, cz_ - 2.6 if cz_ < 5 else cz_ - 1.2), 0.006, ip))
    return ob


def tribun(rnd):
    """arka duvar onunde teleskopik ahsap tribun (8 kademe), mavi plastik sirt, korkuluk; seyirci yok (gercekci, cizgi film insan yok)"""
    ob = []
    tahta = mat_pbr("tribun_t", "#f6f2ea", 0.3, kaplama=0.4)
    yuz = mat_pbr("tribun_y", "#3a3f48", 0.5)
    gokkusagi = [mat_pbr("sirt%d" % i, c, 0.25, kaplama=0.7) for i, c in enumerate(("#ff3b4e", "#ff8a1e", "#ffd21e", "#2fd06a", "#1e9cff", "#8a5aff", "#ff4fc0", "#20d6d0"))]
    kork = mat_pbr("korkuluk", "#b8bcc2", 0.3, metal=1.0)
    x0, x1 = -11.0, 11.0
    for r in range(8):
        y = ARKA_Y - 4.4 + r * 0.55; z = 0.42 * (r + 1)
        ob.append(kutu("basamak", (0, y, z - 0.03), (x1 - x0, 0.55, 0.06), tahta))
        ob.append(kutu("yukselti", (0, y - 0.27, z - 0.22), (x1 - x0, 0.03, 0.4), yuz))
        x = x0 + 0.25
        while x < x1 - 0.2:                                   # koltuk sirtlari (aralikli)
            if rnd.random() < 0.93:
                ob.append(kutu("sirt", (x, y + 0.18, z + 0.2), (0.42, 0.06, 0.34), gokkusagi[r], egim=0.05, seg=3))
            x += 0.5
    for s in (-1, 1):
        ob.append(boru((s * 11.1, ARKA_Y - 4.6, 1.0), (s * 11.1, ARKA_Y - 0.6, 4.4), 0.03, kork))
        for k in range(5):
            yy = ARKA_Y - 4.6 + k * 1.0
            ob.append(boru((s * 11.1, yy, 0.42 * (k * 1.8 + 1)), (s * 11.1, yy, 0.42 * (k * 1.8 + 1) + 0.95), 0.025, kork))
    ob.append(kutu("tribun_on", (0, ARKA_Y - 4.7, 0.21), (x1 - x0, 0.04, 0.42), yuz))
    return ob


# ------------------------------------------------------------------ SERIT: oyuncu zemini + yan minderler + kapi + yan esyalar
def serit_esyalari(oyuncu, R, rnd):
    s_dis = -1 if oyuncu == "p1" else 1                          # dis taraf (ekran kenari)
    bant = mat_pbr("bant_" + oyuncu, R["ana"], 0.35, kaplama=0.2)
    for x in (-1.6, 1.6):                                        # serit bandi (oyuncu renginde yapiskan bant)
        duz("bant", x - 0.04, x + 0.04, -4, KAP["y"] - 0.2, 0.003, bant)
    boya = mat_pbr("ok_" + oyuncu, R["ana"], 0.4, kaplama=0.45)
    for y in (4.9, 6.4):                                          # yerde boyali yon oklari (seri sabiti)
        nok = [(-0.75, y - 0.45), (0, y), (0.75, y - 0.45), (0.75, y - 0.75), (0, y - 0.3), (-0.75, y - 0.75)]
        me = bpy.data.meshes.new("ok"); me.from_pydata([(a, b, 0.002) for a, b in nok], [], [list(range(6))]); me.update()
        o = bpy.data.objects.new("ok", me); bpy.context.collection.objects.link(o); o.data.materials.append(boya)
    # iki yanda katlanir jimnastik minderi (OUT ani: karakter buraya duser), 4 panel, dikis olugu
    # onizleme 1: ic minderler ekran ortasinda mavi | pembe sert cizgiyle birlesiyordu -> ic taraf iki seritte ayni lacivert hakem minderi
    vinil = mat_pbr("minder_" + oyuncu, R["minder"], 0.3, kaplama=0.6)
    hakem = mat_pbr("minder_hakem", OKUL["lacivert"], 0.3, kaplama=0.6)
    for s in (-1, 1):
        for k in range(4):
            y0 = 3.2 + k * 1.2
            kutu("minder", (s * 2.55, y0 + 0.6, 0.05), (1.5, 1.17, 0.1), vinil if s == s_dis else hakem, egim=0.035, seg=3)
    # dis tarafta salon esyalari
    if oyuncu == "p1":
        top_arabasi((s_dis * 5.2, 6.0), rnd)
        for (x, y) in ((-3.9, 9.0), (-4.6, 9.6)):
            koni((x, y))
    else:
        bank((s_dis * 4.9, 6.6))
        for (x, y) in ((4.0, 9.2), (4.7, 9.7)):
            koni((x, y))
        rulo_minder((s_dis * 5.4, 9.8))


def basketbol(konum, r=0.12):
    deri = mat_pbr("basket", "#c4561e", 0.62, bump=(900, 0.25))
    dikis = mat_pbr("dikis", "#1a1a1a", 0.6)
    kure(konum, r, deri, sub=3)
    for rot in ((0, 0, 0), (math.radians(90), 0, 0), (0, math.radians(90), 0)):
        bpy.ops.mesh.primitive_torus_add(major_radius=r * 1.002, minor_radius=r * 0.035, location=konum, rotation=rot)
        bpy.context.active_object.data.materials.append(dikis)


def top_arabasi(xy, rnd):
    x, y = xy
    cel = mat_pbr("araba", "#2c2f34", 0.35, metal=1.0)
    for dx in (-0.5, 0.5):
        for dy in (-0.3, 0.3):
            boru((x + dx, y + dy, 0.08), (x + dx, y + dy, 1.0), 0.015, cel)
            kure((x + dx, y + dy, 0.05), 0.05, mat_pbr("teker", "#111111", 0.6))
    for z in (0.35, 1.0):
        for dy in (-0.3, 0.3):
            boru((x - 0.5, y + dy, z), (x + 0.5, y + dy, z), 0.012, cel)
        for dx in (-0.5, 0.5):
            boru((x + dx, y - 0.3, z), (x + dx, y + 0.3, z), 0.012, cel)
    for i in range(4):
        for j in range(2):
            basketbol((x - 0.36 + i * 0.24, y - 0.13 + j * 0.26, 0.48 + rnd.uniform(0, 0.02)))
    for i in range(3):
        basketbol((x - 0.24 + i * 0.24, y + rnd.uniform(-0.05, 0.05), 0.69))
    basketbol((x + 0.85, y - 0.5, 0.12))                        # yere dusmus top


def koni(xy):
    x, y = xy
    tur = mat_pbr("koni", "#f05a14", 0.45, kaplama=0.2); bey = mat_pbr("koni_b", "#f2f2f2", 0.4)
    bpy.ops.mesh.primitive_cone_add(radius1=0.13, radius2=0.02, depth=0.45, location=(x, y, 0.245))
    bpy.context.active_object.data.materials.append(tur); bpy.ops.object.shade_smooth()
    bpy.ops.mesh.primitive_cylinder_add(radius=0.085, depth=0.06, location=(x, y, 0.27)); bpy.context.active_object.data.materials.append(bey)
    kutu("koni_t", (x, y, 0.012), (0.34, 0.34, 0.024), tur)


def bank(xy):
    x, y = xy
    tahta = mat_tahta("bank", "#f0a24a", "#e48a34", "#9a4e1c", olcek=(0.6, 0.08))
    ayak = mat_pbr("bank_a", "#2c2f34", 0.35, metal=1.0)
    kutu("bank_ust", (x, y, 0.45), (0.32, 2.6, 0.05), tahta, egim=0.01, seg=2)
    for dy in (-1.1, 1.1):
        kutu("bank_ayak", (x, y + dy, 0.22), (0.3, 0.04, 0.44), ayak)
    spor_cantasi((x - 0.05, y - 0.5, 0.6))
    sise((x + 0.08, y + 0.6, 0.47))


def spor_cantasi(konum):
    k = kure(konum, 0.2, mat_pbr("canta", "#2a2d33", 0.7, bump=(300, 0.1)), sub=3); k.scale = (1.0, 2.2, 0.75)


def sise(konum):
    x, y, z = konum
    bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=0.22, location=(x, y, z + 0.11))
    bpy.context.active_object.data.materials.append(mat_pbr("sise", "#2f9e5a", 0.25, kaplama=0.5)); bpy.ops.object.shade_smooth()


def rulo_minder(xy):
    x, y = xy
    for k, renk in enumerate(("#1f63c4", "#d02a86", "#e8b21e")):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.26, depth=1.2, location=(x, y + k * 0.0, 0.26 + k * 0.5), rotation=(0, math.radians(90), 0))
        o = bpy.context.active_object; o.data.materials.append(mat_pbr("rulo%d" % k, renk, 0.5, bump=(220, 0.06)))
        bv = o.modifiers.new("e", "BEVEL"); bv.width = 0.05; bv.segments = 3; bpy.ops.object.shade_smooth()


def kapi(R):
    """celik cerceve + oyuncu renginde kalin vinil koruma yastiklari; ustte sonuk LED tabela (motor PLAYER n yazar)"""
    Y, W_, H_, K = KAP["y"], KAP["w"], KAP["h"], KAP["kalin"]
    yastik = mat_pbr("kapi_y", R["ana"], 0.3, kaplama=0.7)
    cel = mat_pbr("kapi_c", "#cfd3d8", 0.3, metal=1.0)
    xk = W_ / 2 + K / 2
    for s in (-1, 1):
        yuvarlak_kutu("direk", (s * xk, Y, (H_ + K) / 2), (K, K, H_ + K), yastik, egim=0.05, seg=3)
        kutu("taban", (s * xk, Y, 0.02), (K + 0.3, K + 0.4, 0.04), cel)
    yuvarlak_kutu("kiris", (0, Y, H_ + K / 2), (W_ + 2 * K, K, K), yastik, egim=0.05, seg=3)
    for z in (0.9, 2.0, 3.1):                                  # yastik kayislari
        for s in (-1, 1):
            kutu("kayis", (s * xk, Y - K / 2 - 0.005, z), (K + 0.01, 0.012, 0.06), mat_pbr("kayis", "#1a1c20", 0.6))
    # ustte tabela: siyah kasa + sonuk LED yuzey (motor yazar)
    yuvarlak_kutu("tabela", (0, Y, H_ + K + 0.5), (W_ * 0.85, 0.2, 0.7), mat_pbr("tabela", "#15171a", 0.35, metal=0.4), egim=0.03, seg=2)
    duz_dik = bpy.data.meshes.new("led_yuz")
    a, b = W_ * 0.4, 0.28; z0 = H_ + K + 0.5
    duz_dik.from_pydata([(-a, Y - 0.11, z0 - b), (a, Y - 0.11, z0 - b), (a, Y - 0.11, z0 + b), (-a, Y - 0.11, z0 + b)], [], [[0, 1, 2, 3]]); duz_dik.update()
    o = bpy.data.objects.new("led_yuz", duz_dik); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat_emis("led_yuz", lin(hex3(R["koyu"])), 1.2))
    for s in (-1, 1):
        boru((s * W_ * 0.3, Y, H_ + K), (s * W_ * 0.3, Y, H_ + K + 0.15), 0.02, cel)


def serit_katmani(oyuncu):
    R = SERIT[oyuncu]
    sc = salon_sahnesi(960, 1080, True)
    kam = kamera(sc)
    rnd = random.Random(25 + (oyuncu == "p2"))
    isiklar()
    salon(True, random.Random(25))
    serit_esyalari(oyuncu, R, rnd)
    kapi(R)
    Y, W_, H_ = KAP["y"], KAP["w"], KAP["h"]
    ic = W_ / 2
    bpy.context.view_layer.update()
    px = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-ic, Y, 0), (ic, Y, 0), (-ic, Y, H_), (ic, Y, H_))]
    xs = [p.x * 960 for p in px]; ys = [(1 - p.y) * 1080 for p in px]
    YERLESIM["aciklik_" + oyuncu] = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
    # OUT ani: minderlerin ekrandaki yeri (y=5,0); oyuncu dis taraftaki kendi renkli minderine duser
    mk = [world_to_camera_view(sc, kam, Vector(p)) for p in ((-2.55, 5.0, 0.1), (2.55, 5.0, 0.1), (0, GECIS, 0))]
    YERLESIM["salon_" + oyuncu] = {"minder_sol_x": round(mk[0].x * 960, 1), "minder_sag_x": round(mk[1].x * 960, 1),
                                  "minder_y": round((1 - mk[0].y) * 1080, 1), "gecis_y": round((1 - mk[2].y) * 1080, 1)}
    YERLESIM["yol"] = {"y_kapi": Y, "genislik": YOL_YARI * 2, "kam": KAM, "serit_w": 960}
    log("aciklik", oyuncu, YERLESIM["aciklik_" + oyuncu], YERLESIM["salon_" + oyuncu])
    yaz(sc, ON_EK + "serit-%s.png" % oyuncu)


def gok_katmani(ad):
    sc = salon_sahnesi(1920, 1080, False)
    kamera(sc)
    isiklar()
    salon(False, random.Random(25))
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
log("bitti (salon)", YERLESIM.get("aciklik_p1"), YERLESIM.get("aciklik_p2"))
