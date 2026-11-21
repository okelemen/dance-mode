"""HUMAN TETRIS 24 - yarisan karakterler + hakem maskot poz kareleri. varlik.py calistirir (--mod karakter).

    blender -b --factory-startup -noaudio -P 03-motor/tetris-pvp/varlik.py -- --cikti cikti --mod karakter --oyuncu p1 \
        --duvar 03-motor/tetris-pvp/duvar-listesi-24.json --kaynak 03-motor/tetris-pvp/aday-olcu-24.json

Kullanici 11 Kas 2026 (POZ-DUVARI TALIMATLAR §4 mobil paket md. 2 + maskot): "ekranda yarisan karakterler" (P1 mavi / P2 pembe, VS kartindaki
boksorlerimiz: beyaz govde, kask, eldiven, dizlik oyuncu renginde) her duvarda pozu kendileri dener; "maskot gelen hareketi yapsin" -> hakem
maskot (pembe jole govde; yuzu motorda 2B cizilir, kafa kemiginin ekrandaki yeri yerlesim.json'a yazilir) pozu once gosterir.
Poz acilari: maskenin uretildigi pozlar*.json (duvardaki siyah siluetle ayni govde, ayni acilar -> karakter siluetle birebir).
Gecis: ayakta durustan poza K karede (kemik yonleri acilarla aradeger, ease); kare 0 = ayakta, kare K-1 = tam poz. Ayaklar her karede yere
oturtulur (en alt nokta = zemin), kalca yatayda sabit. Kamera ortografik, butun pozlarda ayni olcek (karakterler platformda ayni boyda).
Cikti: karakter/<oyuncu>/<poz>-NN.png (KxK kare, saydam), yerlesim.json: karakter.<oyuncu>.<poz> = {"kafa": [[x,y,r] her kare], "taban_y"}.

27 (CO-OP, --ikili 1, duvar listesi {"grup", "video"}): aci tanimi gruplar-<video>.json'dan (duvardaki ikili maskeyle ayni figurler).
  p1 = sol figur (A), p2 = sag figur (B). Es govde (gorunmez) de pozlanir; iki govde her karede varlik-cadi hizala() ile duvardaki
  gibi birbirine yaslanir (temas: eklem-eklem / yan / bosluk m). Kare genis (PXW x PXH), ayni kamera iki oyuncuda ortak ->
  motor iki karakteri ayni yere cizer, birlikte ikili pozu olusturur; OUT'ta her biri kendi tarafina savrulur.
  maskot: her grubun A ve B figurleri ayri poz (<grup>-A, <grup>-B), tekli kare (motor once A'yi sonra B'yi gosterir).
  yerlesim: karakter.<oyuncu> = {boy_px, zemin_px, w_px, h_px, poz: {grup: {"kalca": [[x,y] her kare]}}}.
  --kayakci 1: maskota bere (ponponlu) + atki (karli zirve hakemi).
  --asci 1: maskota asci sapkasi (beyaz, kabarik) + kirmizi fular (28, dev mutfak hakemi).
  --kasif 1: maskota kasif sapkasi (genis kenarli haki, yesil bant) + yesil fular (29, orman tapinagi hakemi).
  --ciftci 1: maskota hasir sapka (sari, kirmizi bant) + kirmizi fular (30, lale tarlasi hakemi).
  --penguen 1: maskot penguen yavrusu govdesi (lacivert sirt, beyaz gogus, turuncu ayak) + kirmizi atki (31). --don 90: yan gorunum.
  --panda 1: maskot panda yavrusu govdesi (32): siyah kol/bacak, beyaz tombul yumurta govde + kirmizi atki; kafa motorda 2B.
  --ejderha 1: maskot kucuk ejderha (33): yesil tombul uzuv + yumurta govde (sari karin), sirt dikeni, turuncu kanat, kuyruk; kafa motorda 2B.
  --jole 1: maskot jole kup (34): kalcadan basa tek buyuk turuncu jole kup govde + tombul uzuvlar; yuz motorda 2B.
  --sincap 1: maskot ucan sincap yavrusu (35, balon festivali): turuncu-kahve tombul uzuv + yumurta govde (krem karin), yan kanat zari,
              sirttan yukari kivrilan kabarik kuyruk + kirmizi atki; kafa, kulak ve pilot gozlugu motorda 2B.
  --baykus 1: maskot baykus yavrusu (36, mantar ormani): yuvarlak karamel tuy topu govde (krem gogus), kollara bagli kanatlar
              (pozu kanatlarla gosterir), kisa tuylu bacak + turuncu ayak, yesil atki; kafa, goz diski, kulak tuyleri motorda 2B.
  --p3 (32, 3 oyuncu): yesil sporcu.
  --sporcu 1: yarisan karakterler boksor degil sporcu (30'dan itibaren, kullanici 17 Kas): forma + koyu sort + ayakkabi oyuncu renginde, sac bandi, bileklik.
"""
import bmesh

OYUNCU = arg("--oyuncu", "p1")                    # p1 | p2 | maskot
K = int(arg("--kare", "7"))
PX = int(arg("--px", "420"))
DUVAR = json.load(open(os.path.join(KOK, arg("--duvar", "03-motor/tetris-pvp/duvar-listesi-24.json")), encoding="utf-8"))
KAYNAK = json.load(open(os.path.join(KOK, arg("--kaynak", "03-motor/tetris-pvp/aday-olcu-24.json")), encoding="utf-8"))
POZ_DOSYA = {"varlik": "pozlar.json", "varlik-03": "pozlar-03.json", "varlik-04": "pozlar-04.json", "varlik-05": "pozlar-05.json",
             # 30: aday havuzlari (daha once render edilip kullanilmamis pozlar)
             "varlik-05-aday": "pozlar-05-aday.json", "varlik-06-aday": "pozlar-06-aday.json", "varlik-08-aday": "pozlar-08-aday.json",
             "varlik-09-aday": "pozlar-09-aday.json", "varlik-10-aday": "pozlar-10-aday.json", "varlik-12-aday": "pozlar-12-aday.json",
             "varlik-14-aday": "pozlar-14-aday.json", "varlik-16-aday-2": "pozlar-16-aday.json", "varlik-17-aday": "pozlar-17-aday.json"}
RENK_K = {"p1": "#2E9BFF", "p2": "#FF3EA5", "p3": "#22C84A", "maskot": "#ff9ad8"}
# 25 (TALIMATLAR §4 cilali 3D oyun gorunumu): 24'teki guclu kenar isiltisi govdeyi bembeyaz/pastel yapiyordu -> ayarlanabilir
RIM = float(arg("--rim", "1.6")); EKIP_EMIS = float(arg("--ekip-emis", "0.35")); GOVDE_ACIK = float(arg("--govde-acik", "0.78"))

IKILI = arg("--ikili", "0") == "1"
TANIM = {}
_onbellek = {}
GRUP = {}
if IKILI:
    for d in DUVAR:
        f = "gruplar-%s.json" % d["video"]
        if f not in _onbellek:
            _onbellek[f] = json.load(open(os.path.join(KOK, "03-motor/tetris-pvp", f), encoding="utf-8"))["gruplar"]
        if d["grup"] not in _onbellek[f]:                     # 28: havuz maskesi videonun aday dosyasindan gelebilir (gruplar-18-aday.json)
            fa = f.replace(".json", "-aday.json")
            if fa not in _onbellek and os.path.exists(os.path.join(KOK, "03-motor/tetris-pvp", fa)):
                _onbellek[fa] = json.load(open(os.path.join(KOK, "03-motor/tetris-pvp", fa), encoding="utf-8"))["gruplar"]
            GRUP[d["grup"]] = _onbellek[fa][d["grup"]]
        else:
            GRUP[d["grup"]] = _onbellek[f][d["grup"]]
        assert len(GRUP[d["grup"]]["figurler"]) == 2, d["grup"]
    if OYUNCU == "maskot":
        for g_, G in GRUP.items():
            TANIM[g_ + "-A"] = G["figurler"][0]; TANIM[g_ + "-B"] = G["figurler"][1]
    else:
        TANIM = {g_: G["figurler"][0 if OYUNCU == "p1" else 1] for g_, G in GRUP.items()}
    ADLAR = list(TANIM)
else:
    # poz adi -> aci tanimi (maskenin klasorune gore dogru pozlar dosyasi)
    ad_klasor = {os.path.basename(k)[:-4]: k.split("/")[0] for k in KAYNAK}
    if OYUNCU == "maskot":
        ADLAR = [a for d in DUVAR for a in (d["p1"], d["p2"]) + ((d["p3"],) if "p3" in d else ())]
    else:
        ADLAR = [d[OYUNCU] for d in DUVAR]
    for a in ADLAR:
        f = POZ_DOSYA[ad_klasor[a]]
        if f not in _onbellek:
            _onbellek[f] = json.load(open(os.path.join(KOK, "03-motor/tetris-pvp", f), encoding="utf-8"))["pozlar"]
        TANIM[a] = _onbellek[f][a]
assert len(TANIM) == len(set(ADLAR)) and TANIM, (len(TANIM), len(ADLAR))
log("karakter", OYUNCU, "poz", len(TANIM), "kare", K)
os.makedirs(os.path.join(CIKTI, "karakter", OYUNCU), exist_ok=True)


def mat_govde(renk, acik_m):
    m = bpy.data.materials.new("govde"); m.use_nodes = True; nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*acik(renk, acik_m), 1)
    b.inputs["Roughness"].default_value = 0.18
    b.inputs["Coat Weight"].default_value = 1.0
    b.inputs["Coat Roughness"].default_value = 0.03
    lw = nt.nodes.new("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.35
    mu = nt.nodes.new("ShaderNodeMath"); mu.operation = "MULTIPLY"; mu.inputs[1].default_value = RIM
    nt.links.new(lw.outputs["Facing"], mu.inputs[0])
    b.inputs["Emission Color"].default_value = (*acik(renk, 0.2), 1)
    nt.links.new(mu.outputs[0], b.inputs["Emission Strength"])
    return m


PXW, PXH = (int(arg("--pxw", "1000")), int(arg("--pxh", "420"))) if (IKILI and OYUNCU != "maskot") else (PX, PX)
sc = bos_sahne(w=PXW, h=PXH, saydam=True, ornek=min(ORNEK, 16))
sc.cycles.use_denoising = True
sc.view_settings.view_transform = "Standard"
once = set(bpy.data.objects)
bpy.ops.import_scene.fbx(filepath=os.path.join(KOK, "02-hareketler/siluet-govde.fbx"), automatic_bone_orientation=False)
yeni = [o for o in bpy.data.objects if o not in once]
arm = [o for o in yeni if o.type == "ARMATURE"][0]
mesler = [o for o in yeni if o.type == "MESH"]
arm.animation_data_clear()
for o in mesler:
    o.animation_data_clear()
R = lin(hex3(RENK_K[OYUNCU]))
gm = mat_govde(R, GOVDE_ACIK if OYUNCU != "maskot" else 0.35)
for m in mesler:
    m.data.materials.clear(); m.data.materials.append(gm)
    for poly in m.data.polygons:
        poly.material_index = 0
# yuzu kameraya (poz_maskeleri ile ayni)
pb = arm.pose.bones
L = arm.matrix_world @ kemik(arm, "LeftArm").head; Rr = arm.matrix_world @ kemik(arm, "RightArm").head
v = L - Rr; v.z = 0
arm.rotation_euler.z -= math.atan2(v.y, v.x)
arm.rotation_euler.z += math.radians(float(arg("--don", "0")))   # 31: maskot ornek sayfasi yan gorunum (--don 90)
bpy.context.view_layer.update()
TABAN_ROT = arm.rotation_euler.z
alt0, ust0 = dunya_kutusu(mesler)
BOY = ust0.z - alt0.z
log("govde boy", round(BOY, 3))

# ---------------------------------------------------------------- ekipman (yalniz yarisan karakterler; VS kartindaki boksorlerin dili)
EKIP = []
SPORCU = arg("--sporcu", "0") == "1"
if OYUNCU != "maskot" and SPORCU:      # 30 (17 Kas 2026, kullanici: "box eldivenleri falan olmasin" -> sporcu): kask/eldiven/dizlik yok;
    # govde parcalari: dinlenme pozundaki yukseklik ("boy") + kol sinifi ("kol") nokta ozniteligi -> shader'da keskin cizgi
    # (1. deneme poligon boyamasi bel/diz cizgisini basamakli yapti). forma (oyuncu rengi, kisa kol) / koyu sort / ayakkabi / ten
    forma = mat_jole("forma", R, emis=EKIP_EMIS, purluk=0.10)
    beyazs = mat_jole("serit", (0.92, 0.94, 1.0), emis=0.15, purluk=0.08)
    zb = lambda ad: (arm.matrix_world @ kemik(arm, ad).head).z
    BEL, DIZ, BILEK, BOYUN = zb("Hips") + 0.035 * BOY, zb("LeftLeg") + 0.045 * BOY, zb("LeftFoot") + 0.012 * BOY, zb("Neck") - 0.005 * BOY
    log("sporcu cizgiler bel/diz/bilek/boyun", [round(x, 3) for x in (BEL, DIZ, BILEK, BOYUN)])
    def kol_sinif(ad):
        if "ForeArm" in ad or "Hand" in ad: return 2.0
        if "Arm" in ad or "Shoulder" in ad: return 1.0
        return 0.0
    for m in mesler:
        gs = {g.index: kol_sinif(g.name) for g in m.vertex_groups}
        ab = m.data.attributes.new("boy", "FLOAT", "POINT"); ak = m.data.attributes.new("kol", "FLOAT", "POINT")
        for v_ in m.data.vertices:
            ab.data[v_.index].value = (m.matrix_world @ v_.co).z
            en = max(v_.groups, key=lambda g: g.weight, default=None)
            ak.data[v_.index].value = gs.get(en.group, 0.0) if en else 0.0
    sm = mat_govde(R, GOVDE_ACIK); sm.name = "sporcu"; nt = sm.node_tree; bs = nt.nodes["Principled BSDF"]
    TEN = (*acik(R, GOVDE_ACIK), 1); FORMA = (*R, 1); SORT = (*(c * 0.2 for c in R), 1); AYAK = (*R, 1)
    nb = nt.nodes.new("ShaderNodeAttribute"); nb.attribute_name = "boy"
    nk = nt.nodes.new("ShaderNodeAttribute"); nk.attribute_name = "kol"
    rp = nt.nodes.new("ShaderNodeValToRGB"); cr = rp.color_ramp; cr.interpolation = "CONSTANT"
    span = BOY * 1.2; z0 = alt0.z - 0.1 * BOY; f = lambda z: (z - z0) / span
    mp = nt.nodes.new("ShaderNodeMapRange"); mp.inputs["From Min"].default_value = z0; mp.inputs["From Max"].default_value = z0 + span
    nt.links.new(nb.outputs["Fac"], mp.inputs["Value"]); nt.links.new(mp.outputs["Result"], rp.inputs["Fac"])
    cr.elements[0].position = 0.0; cr.elements[0].color = AYAK; cr.elements[1].position = f(BILEK); cr.elements[1].color = TEN
    for z, c in ((DIZ, SORT), (BEL, FORMA), (BOYUN, TEN)):
        e = cr.elements.new(f(z)); e.color = c
    def esik(deger):
        g = nt.nodes.new("ShaderNodeMath"); g.operation = "GREATER_THAN"; g.inputs[1].default_value = deger
        nt.links.new(nk.outputs["Fac"], g.inputs[0]); return g
    m1 = nt.nodes.new("ShaderNodeMix"); m1.data_type = "RGBA"; nt.links.new(esik(0.5).outputs[0], m1.inputs["Factor"])
    nt.links.new(rp.outputs["Color"], m1.inputs[6]); m1.inputs[7].default_value = FORMA
    m2 = nt.nodes.new("ShaderNodeMix"); m2.data_type = "RGBA"; nt.links.new(esik(1.5).outputs[0], m2.inputs["Factor"])
    nt.links.new(m1.outputs[2], m2.inputs[6]); m2.inputs[7].default_value = TEN
    nt.links.new(m2.outputs[2], bs.inputs["Base Color"])
    for m in mesler:
        m.data.materials.clear(); m.data.materials.append(sm)
    Lh = ((arm.matrix_world @ kemik(arm, "Head").tail) - (arm.matrix_world @ kemik(arm, "Head").head)).length
    rk = max(0.6 * Lh, 0.066 * BOY)
    bpy.ops.mesh.primitive_torus_add(major_radius=rk * 0.86, minor_radius=rk * 0.13, major_segments=48, minor_segments=12)   # sac bandi
    sb = bpy.context.active_object; bpy.ops.object.shade_smooth(); sb.data.materials.append(forma)
    sb.data.transform(Matrix.Rotation(math.radians(-90), 4, "X"))
    EKIP.append((sb, "Head", Matrix.Translation((0, 0.55 * Lh, 0))))
    for taraf in ("Left", "Right"):                                   # bileklik (beyaz)
        bpy.ops.mesh.primitive_torus_add(major_radius=0.017 * BOY, minor_radius=0.008 * BOY, major_segments=32, minor_segments=10)
        bl = bpy.context.active_object; bpy.ops.object.shade_smooth(); bl.data.materials.append(beyazs)
        bl.data.transform(Matrix.Rotation(math.radians(90), 4, "X"))
        EKIP.append((bl, taraf + "Hand", Matrix.Translation((0, -0.01 * BOY, 0))))
elif OYUNCU != "maskot":
    ekip = mat_jole("ekipman", R, emis=EKIP_EMIS, purluk=0.06)
    beyaz = mat_jole("kenar", (0.92, 0.94, 1.0), emis=0.15, purluk=0.08)

    def kemik_boy(ad):
        b = kemik(arm, ad); return ((arm.matrix_world @ b.tail) - (arm.matrix_world @ b.head)).length

    def kemik_rot(ad):
        return (arm.matrix_world @ kemik(arm, ad).matrix).decompose()[1]

    ileri = Vector((0, -1, 0))                              # kameraya donuk
    f_yerel = (kemik_rot("Head").to_matrix().inverted() @ ileri).normalized()
    Lh = kemik_boy("Head"); rk = max(0.6 * Lh, 0.066 * BOY)
    me = bpy.data.meshes.new("kask"); bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=40, v_segments=24, radius=rk)
    bmesh.ops.scale(bm, vec=(1.0, 1.1, 1.0), verts=bm.verts)
    sil = [v_ for v_ in bm.verts if (v_.co.normalized().dot(f_yerel) > 0.66 and -0.45 * rk < v_.co.y < 0.45 * rk) or v_.co.y < -0.80 * rk]
    bmesh.ops.delete(bm, geom=sil, context="VERTS"); bm.to_mesh(me); bm.free()
    kask = bpy.data.objects.new("kask", me); bpy.context.collection.objects.link(kask)
    kask.data.materials.append(ekip); kask.data.materials.append(beyaz)
    so = kask.modifiers.new("dolgu", "SOLIDIFY"); so.thickness = 0.22 * rk; so.offset = 1.0; so.use_rim = True; so.material_offset_rim = 1
    for p_ in kask.data.polygons:
        p_.use_smooth = True
    EKIP.append((kask, "Head", Matrix.Translation((0, 0.42 * Lh, 0))))
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.93 * rk, segments=32, ring_count=16)
    yz = bpy.context.active_object; yz.data.materials.append(mat_jole("yuz", (0.96, 0.97, 1.0), emis=0.25, purluk=0.12))
    bpy.ops.object.shade_smooth(); yz.data.transform(Matrix.Diagonal((1.0, 1.08, 1.0, 1.0)))
    EKIP.append((yz, "Head", Matrix.Translation((0, 0.42 * Lh, 0))))
    rg = 0.062 * BOY
    for taraf in ("Left", "Right"):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=rg, segments=32, ring_count=16)
        g_ = bpy.context.active_object; g_.data.materials.append(ekip); bpy.ops.object.shade_smooth()
        g_.data.transform(Matrix.Diagonal((1.0, 1.3, 1.05, 1.0)))
        EKIP.append((g_, taraf + "Hand", Matrix.Translation((0, 0.85 * rg, 0))))
        bpy.ops.mesh.primitive_cylinder_add(radius=0.78 * rg, depth=1.0 * rg, vertices=32)
        m_ = bpy.context.active_object; m_.data.materials.append(beyaz); bpy.ops.object.shade_smooth()
        m_.data.transform(Matrix.Rotation(math.radians(90), 4, "X"))
        EKIP.append((m_, taraf + "Hand", Matrix.Translation((0, -0.25 * rg, 0))))
    rd = 0.048 * BOY
    for taraf in ("Left", "Right"):
        bpy.ops.mesh.primitive_cylinder_add(radius=rd, depth=1.5 * rd, vertices=32)
        d_ = bpy.context.active_object; d_.data.materials.append(ekip); bpy.ops.object.shade_smooth()
        d_.data.transform(Matrix.Rotation(math.radians(90), 4, "X"))
        bv = d_.modifiers.new("egim", "BEVEL"); bv.width = 0.35 * rd; bv.segments = 4
        EKIP.append((d_, taraf + "Leg", Matrix.Translation((0, 0.12 * rd, 0))))

if OYUNCU == "maskot" and arg("--cankurtaran", "0") == "1":   # 26 (plaj): hakem maskot cankurtaran sortu (kirmizi, beyaz bel bandi); duduk motorda 2B
    sort = mat_jole("sort", lin(hex3("#ff2436")), emis=0.25, purluk=0.08)
    bant = mat_jole("bant", (0.95, 0.96, 1.0), emis=0.15, purluk=0.1)
    rh = 0.112 * BOY
    bpy.ops.mesh.primitive_cylinder_add(radius=rh, depth=0.75 * rh, vertices=40)
    h_ = bpy.context.active_object; h_.data.materials.append(sort); bpy.ops.object.shade_smooth()
    h_.data.transform(Matrix.Diagonal((1.0, 1.0, 0.8, 1.0)) @ Matrix.Rotation(math.radians(90), 4, "X"))
    bv = h_.modifiers.new("egim", "BEVEL"); bv.width = 0.2 * rh; bv.segments = 4
    EKIP.append((h_, "Hips", Matrix.Translation((0, 0.05 * rh, 0))))
    bpy.ops.mesh.primitive_cylinder_add(radius=1.03 * rh, depth=0.16 * rh, vertices=40)
    w_ = bpy.context.active_object; w_.data.materials.append(bant); bpy.ops.object.shade_smooth()
    w_.data.transform(Matrix.Diagonal((1.0, 1.0, 0.8, 1.0)) @ Matrix.Rotation(math.radians(90), 4, "X"))
    EKIP.append((w_, "Hips", Matrix.Translation((0, 0.42 * rh, 0))))
    rb = 0.07 * BOY
    for taraf in ("Left", "Right"):
        bpy.ops.mesh.primitive_cylinder_add(radius=rb, depth=1.5 * rb, vertices=32)
        u_ = bpy.context.active_object; u_.data.materials.append(sort); bpy.ops.object.shade_smooth()
        u_.data.transform(Matrix.Rotation(math.radians(90), 4, "X"))
        bv = u_.modifiers.new("egim", "BEVEL"); bv.width = 0.25 * rb; bv.segments = 3
        EKIP.append((u_, taraf + "UpLeg", Matrix.Translation((0, 0.75 * rb, 0))))


if OYUNCU == "maskot" and arg("--kayakci", "0") == "1":     # 27 (karli zirve): hakem maskot bere (ponponlu) + atki
    import bmesh as _bm
    bere = mat_jole("bere", lin(hex3("#1e8cff")), emis=0.2, purluk=0.1)
    beyazk = mat_jole("bere_b", (0.95, 0.96, 1.0), emis=0.15, purluk=0.1)
    atki = mat_jole("atki", lin(hex3("#ff2436")), emis=0.22, purluk=0.1)
    Lh = ((arm.matrix_world @ kemik(arm, "Head").tail) - (arm.matrix_world @ kemik(arm, "Head").head)).length
    rk = max(0.6 * Lh, 0.066 * BOY)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=rk * 1.04, segments=32, ring_count=16)
    b_ = bpy.context.active_object; bpy.ops.object.shade_smooth(); b_.data.materials.append(bere)
    bm_ = _bm.new(); bm_.from_mesh(b_.data)
    _bm.ops.delete(bm_, geom=[v_ for v_ in bm_.verts if v_.co.z < rk * 0.05], context="VERTS"); bm_.to_mesh(b_.data); bm_.free()
    b_.data.transform(Matrix.Rotation(math.radians(-90), 4, "X"))            # kubbe kemigin +Y (yukari) yonune
    EKIP.append((b_, "Head", Matrix.Translation((0, 0.55 * Lh, 0))))
    bpy.ops.mesh.primitive_torus_add(major_radius=rk * 1.0, minor_radius=rk * 0.17, major_segments=40, minor_segments=12)
    k_ = bpy.context.active_object; bpy.ops.object.shade_smooth(); k_.data.materials.append(beyazk)
    k_.data.transform(Matrix.Rotation(math.radians(-90), 4, "X"))
    EKIP.append((k_, "Head", Matrix.Translation((0, 0.58 * Lh, 0))))
    bpy.ops.mesh.primitive_uv_sphere_add(radius=rk * 0.34, segments=24, ring_count=12)
    p_ = bpy.context.active_object; bpy.ops.object.shade_smooth(); p_.data.materials.append(beyazk)
    EKIP.append((p_, "Head", Matrix.Translation((0, 0.55 * Lh + rk * 1.08, 0))))
    ra = 0.085 * BOY
    bpy.ops.mesh.primitive_torus_add(major_radius=ra, minor_radius=ra * 0.34, major_segments=40, minor_segments=12)
    a_ = bpy.context.active_object; bpy.ops.object.shade_smooth(); a_.data.materials.append(atki)
    a_.data.transform(Matrix.Rotation(math.radians(-90), 4, "X"))
    EKIP.append((a_, "Neck", Matrix.Translation((0, 0.02 * BOY, 0))))
    bpy.ops.mesh.primitive_cube_add(size=1)
    u_ = bpy.context.active_object; u_.data.materials.append(atki)
    u_.data.transform(Matrix.Diagonal((0.05 * BOY, 0.2 * BOY, 0.025 * BOY, 1.0)))
    bv = u_.modifiers.new("egim", "BEVEL"); bv.width = 0.008 * BOY; bv.segments = 3
    EKIP.append((u_, "Neck", Matrix.Translation((0.05 * BOY, -0.1 * BOY, 0.08 * BOY))))


if OYUNCU == "maskot" and arg("--asci", "0") == "1":        # 28 (dev mutfak): hakem maskot asci sapkasi (beyaz, kabarik tepe) + kirmizi fular
    sap = mat_jole("asci_sapka", (0.97, 0.97, 1.0), emis=0.12, purluk=0.25)
    fular = mat_jole("fular", lin(hex3("#ff2436")), emis=0.22, purluk=0.1)
    Lh = ((arm.matrix_world @ kemik(arm, "Head").tail) - (arm.matrix_world @ kemik(arm, "Head").head)).length
    rk = max(0.6 * Lh, 0.066 * BOY)
    bpy.ops.mesh.primitive_cylinder_add(radius=rk * 0.98, depth=rk * 0.75, vertices=40)      # serit (bant)
    c_ = bpy.context.active_object; bpy.ops.object.shade_smooth(); c_.data.materials.append(sap)
    c_.data.transform(Matrix.Rotation(math.radians(-90), 4, "X"))
    bv = c_.modifiers.new("egim", "BEVEL"); bv.width = 0.08 * rk; bv.segments = 3
    EKIP.append((c_, "Head", Matrix.Translation((0, 0.62 * Lh + rk * 0.25, 0))))
    for i in range(6):                                                                        # kabarik tepe: halka 5 top + ortada 1
        a_ = i * 2 * math.pi / 5
        rr = 0.0 if i == 5 else rk * 0.55
        bpy.ops.mesh.primitive_uv_sphere_add(radius=rk * (0.62 if i == 5 else 0.52), segments=24, ring_count=12)
        t_ = bpy.context.active_object; bpy.ops.object.shade_smooth(); t_.data.materials.append(sap)
        EKIP.append((t_, "Head", Matrix.Translation((math.cos(a_) * rr, 0.62 * Lh + rk * (0.95 if i < 5 else 1.15), math.sin(a_) * rr))))
    ra = 0.085 * BOY
    bpy.ops.mesh.primitive_torus_add(major_radius=ra, minor_radius=ra * 0.34, major_segments=40, minor_segments=12)
    f_ = bpy.context.active_object; bpy.ops.object.shade_smooth(); f_.data.materials.append(fular)
    f_.data.transform(Matrix.Rotation(math.radians(-90), 4, "X"))
    EKIP.append((f_, "Neck", Matrix.Translation((0, 0.02 * BOY, 0))))


if OYUNCU == "maskot" and arg("--kasif", "0") == "1":       # 29 (orman tapinagi): hakem maskot kasif sapkasi (genis kenarli, haki) + yesil bant + yesil fular
    sap = mat_jole("kasif_sapka", lin(hex3("#f0b44a")), emis=0.14, purluk=0.3)
    bant = mat_jole("kasif_bant", lin(hex3("#1fae3a")), emis=0.18, purluk=0.15)
    Lh = ((arm.matrix_world @ kemik(arm, "Head").tail) - (arm.matrix_world @ kemik(arm, "Head").head)).length
    rk = max(0.6 * Lh, 0.066 * BOY)
    bpy.ops.mesh.primitive_cylinder_add(radius=rk * 1.75, depth=rk * 0.12, vertices=48)      # genis kenar
    k_ = bpy.context.active_object; bpy.ops.object.shade_smooth(); k_.data.materials.append(sap)
    k_.data.transform(Matrix.Rotation(math.radians(-90), 4, "X"))
    bv = k_.modifiers.new("egim", "BEVEL"); bv.width = 0.05 * rk; bv.segments = 3
    EKIP.append((k_, "Head", Matrix.Translation((0, 0.62 * Lh + rk * 0.15, 0))))
    bpy.ops.mesh.primitive_uv_sphere_add(radius=rk * 1.0, segments=32, ring_count=16)        # kubbe tepe
    c_ = bpy.context.active_object; bpy.ops.object.shade_smooth(); c_.data.materials.append(sap)
    c_.data.transform(Matrix.Diagonal((1.0, 1.0, 0.75, 1.0)) @ Matrix.Rotation(math.radians(-90), 4, "X"))
    EKIP.append((c_, "Head", Matrix.Translation((0, 0.62 * Lh + rk * 0.35, 0))))
    bpy.ops.mesh.primitive_cylinder_add(radius=rk * 1.01, depth=rk * 0.22, vertices=48)      # yesil bant
    b_ = bpy.context.active_object; bpy.ops.object.shade_smooth(); b_.data.materials.append(bant)
    b_.data.transform(Matrix.Rotation(math.radians(-90), 4, "X"))
    EKIP.append((b_, "Head", Matrix.Translation((0, 0.62 * Lh + rk * 0.3, 0))))
    ra = 0.085 * BOY
    bpy.ops.mesh.primitive_torus_add(major_radius=ra, minor_radius=ra * 0.34, major_segments=40, minor_segments=12)
    f_ = bpy.context.active_object; bpy.ops.object.shade_smooth(); f_.data.materials.append(bant)
    f_.data.transform(Matrix.Rotation(math.radians(-90), 4, "X"))
    EKIP.append((f_, "Neck", Matrix.Translation((0, 0.02 * BOY, 0))))

if OYUNCU == "maskot" and arg("--ciftci", "0") == "1":      # 30 (lale tarlasi): hakem maskot hasir sapka (genis duz kenar, sari) + kirmizi bant + kirmizi fular
    sap = mat_jole("ciftci_sapka", lin(hex3("#ffd23a")), emis=0.14, purluk=0.35)
    bant = mat_jole("ciftci_bant", lin(hex3("#ff2a3a")), emis=0.18, purluk=0.15)
    Lh = ((arm.matrix_world @ kemik(arm, "Head").tail) - (arm.matrix_world @ kemik(arm, "Head").head)).length
    rk = max(0.6 * Lh, 0.066 * BOY)
    bpy.ops.mesh.primitive_cylinder_add(radius=rk * 1.95, depth=rk * 0.10, vertices=48)      # genis duz hasir kenar
    k_ = bpy.context.active_object; bpy.ops.object.shade_smooth(); k_.data.materials.append(sap)
    k_.data.transform(Matrix.Rotation(math.radians(-90), 4, "X"))
    bv = k_.modifiers.new("egim", "BEVEL"); bv.width = 0.05 * rk; bv.segments = 3
    EKIP.append((k_, "Head", Matrix.Translation((0, 0.62 * Lh + rk * 0.15, 0))))
    bpy.ops.mesh.primitive_cylinder_add(radius=rk * 0.95, depth=rk * 0.7, vertices=48)       # silindir tepe (hasir sapka)
    c_ = bpy.context.active_object; bpy.ops.object.shade_smooth(); c_.data.materials.append(sap)
    c_.data.transform(Matrix.Rotation(math.radians(-90), 4, "X"))
    bv = c_.modifiers.new("egim", "BEVEL"); bv.width = 0.12 * rk; bv.segments = 3
    EKIP.append((c_, "Head", Matrix.Translation((0, 0.62 * Lh + rk * 0.5, 0))))
    bpy.ops.mesh.primitive_cylinder_add(radius=rk * 0.97, depth=rk * 0.2, vertices=48)       # kirmizi bant
    b_ = bpy.context.active_object; bpy.ops.object.shade_smooth(); b_.data.materials.append(bant)
    b_.data.transform(Matrix.Rotation(math.radians(-90), 4, "X"))
    EKIP.append((b_, "Head", Matrix.Translation((0, 0.62 * Lh + rk * 0.3, 0))))
    ra = 0.085 * BOY
    bpy.ops.mesh.primitive_torus_add(major_radius=ra, minor_radius=ra * 0.34, major_segments=40, minor_segments=12)
    f_ = bpy.context.active_object; bpy.ops.object.shade_smooth(); f_.data.materials.append(bant)
    f_.data.transform(Matrix.Rotation(math.radians(-90), 4, "X"))
    EKIP.append((f_, "Neck", Matrix.Translation((0, 0.02 * BOY, 0))))

if OYUNCU == "maskot" and arg("--penguen", "0") == "1":     # 31 (kutup buzul kiyisi; TALIMATLAR §4 maskot sirasi): penguen yavrusu
    # govde uc renk, dinlenme pozunda nokta ozniteligi "pg" (0 lacivert-siyah sirt, 1 beyaz gogus/karin, 2 turuncu ayak) -> keskin sinir.
    # Kafa motorda 2B cizilir (siyah yuvarlak bas, beyaz yuz lekesi, buyuk gozler, turuncu gaga, kizarik yanak).
    zb = lambda ad: (arm.matrix_world @ kemik(arm, ad).head).z
    BILEK, BOYUN, KALCA = zb("LeftFoot") + 0.015 * BOY, zb("Neck"), zb("Hips")
    mx = (arm.matrix_world @ kemik(arm, "Hips").head)
    for m in mesler:
        a_ = m.data.attributes.new("pg", "FLOAT", "POINT")
        mw = m.matrix_world; nr = mw.to_3x3()
        on = None
        for v_ in m.data.vertices:
            w = mw @ v_.co; n = (nr @ v_.normal).normalized()
            if w.z < BILEK:
                val = 2.0
            elif False:                                           # ornek 1: yumurta gocdeyi ortunce kalcada beyaz bant kaliyordu -> govde beyazi yalniz yumurtada
                val = 1.0
            else:
                val = 0.0
            a_.data[v_.index].value = val
    pm = mat_govde(lin(hex3("#1c2a5a")), 0.0); pm.name = "penguen"; nt = pm.node_tree; bs = nt.nodes["Principled BSDF"]
    na = nt.nodes.new("ShaderNodeAttribute"); na.attribute_name = "pg"
    mp = nt.nodes.new("ShaderNodeMapRange"); mp.inputs["From Min"].default_value = 0; mp.inputs["From Max"].default_value = 2
    nt.links.new(na.outputs["Fac"], mp.inputs["Value"])
    rp = nt.nodes.new("ShaderNodeValToRGB"); cr = rp.color_ramp; cr.interpolation = "CONSTANT"
    cr.elements[0].position = 0.0; cr.elements[0].color = (*lin(hex3("#1c2a5a")), 1)
    cr.elements[1].position = 0.75; cr.elements[1].color = (*lin(hex3("#ff8a10")), 1)
    e = cr.elements.new(0.25); e.color = (*lin(hex3("#f4f8ff")), 1)
    nt.links.new(mp.outputs["Result"], rp.inputs["Fac"]); nt.links.new(rp.outputs["Color"], bs.inputs["Base Color"])
    bs.inputs["Emission Color"].default_value = (*lin(hex3("#3a5ab8")), 1)
    for m in mesler:
        m.data.materials.clear(); m.data.materials.append(pm)
    # 31 yan gorunum kontrolu: ince insan govdesi penguen okunmuyordu -> gogus kemigine bagli TOMBUL YUMURTA govde (lacivert sirt, beyaz karin).
    # Kemik uzayinda y = kemik boyu (yukari); karin yonu dinlenme pozunda dunya -y'den (kameraya) hesaplanir, shader nesne normaliyle boyar.
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=48, ring_count=24)
    yum = bpy.context.active_object; bpy.ops.object.shade_smooth()
    yum.data.transform(Matrix.Diagonal((0.155 * BOY, 0.21 * BOY, 0.14 * BOY, 1)))
    Mb0 = (arm.matrix_world @ kemik(arm, "Spine1").matrix).to_3x3()
    on_d = Matrix.Rotation(math.radians(float(arg("--don", "0"))), 3, "Z") @ Vector((0, -1, 0))
    on_l = (Mb0.inverted() @ on_d).normalized()
    ym = mat_govde(lin(hex3("#1c2a5a")), 0.0); ym.name = "pg_yumurta"; nt = ym.node_tree; bs = nt.nodes["Principled BSDF"]
    ge = nt.nodes.new("ShaderNodeNewGeometry"); vt = nt.nodes.new("ShaderNodeVectorTransform")
    vt.vector_type = "NORMAL"; vt.convert_from = "WORLD"; vt.convert_to = "OBJECT"
    nt.links.new(ge.outputs["Normal"], vt.inputs["Vector"])
    dp = nt.nodes.new("ShaderNodeVectorMath"); dp.operation = "DOT_PRODUCT"; dp.inputs[1].default_value = tuple(on_l)
    nt.links.new(vt.outputs["Vector"], dp.inputs[0])
    gt = nt.nodes.new("ShaderNodeMath"); gt.operation = "GREATER_THAN"; gt.inputs[1].default_value = 0.42
    nt.links.new(dp.outputs["Value"], gt.inputs[0])
    mx_ = nt.nodes.new("ShaderNodeMix"); mx_.data_type = "RGBA"; nt.links.new(gt.outputs[0], mx_.inputs["Factor"])
    mx_.inputs[6].default_value = (*lin(hex3("#1c2a5a")), 1); mx_.inputs[7].default_value = (*lin(hex3("#f4f8ff")), 1)
    nt.links.new(mx_.outputs[2], bs.inputs["Base Color"])
    yum.data.materials.append(ym)
    EKIP.append((yum, "Spine1", Matrix.Translation((0, 0.02 * BOY, 0))))
    log("penguen yumurta karin yonu (kemik uzayi)", [round(c, 2) for c in on_l])
    ra = 0.07 * BOY                                                   # kirmizi-beyaz seritli atki (kutup hakemi)
    bpy.ops.mesh.primitive_torus_add(major_radius=ra, minor_radius=ra * 0.36, major_segments=40, minor_segments=12)
    f_ = bpy.context.active_object; bpy.ops.object.shade_smooth(); f_.data.materials.append(mat_jole("pg_atki", lin(hex3("#ff2a3a")), emis=0.18, purluk=0.15))
    f_.data.transform(Matrix.Rotation(math.radians(-90), 4, "X"))
    EKIP.append((f_, "Neck", Matrix.Translation((0, 0.02 * BOY, 0))))

if OYUNCU == "maskot" and arg("--panda", "0") == "1":     # 32 (Noel oyuncak atolyesi; TALIMATLAR §4 maskot sirasi): PANDA yavrusu - penguen blogunun kopyasi, renkler panda
    # govde uc renk, dinlenme pozunda nokta ozniteligi "pg" (0 lacivert-siyah sirt, 1 beyaz gogus/karin, 2 turuncu ayak) -> keskin sinir.
    # Kafa motorda 2B cizilir (siyah yuvarlak bas, beyaz yuz lekesi, buyuk gozler, turuncu gaga, kizarik yanak).
    zb = lambda ad: (arm.matrix_world @ kemik(arm, ad).head).z
    BILEK, BOYUN, KALCA = zb("LeftFoot") + 0.015 * BOY, zb("Neck"), zb("Hips")
    mx = (arm.matrix_world @ kemik(arm, "Hips").head)
    for m in mesler:
        a_ = m.data.attributes.new("pg", "FLOAT", "POINT")
        mw = m.matrix_world; nr = mw.to_3x3()
        on = None
        for v_ in m.data.vertices:
            w = mw @ v_.co; n = (nr @ v_.normal).normalized()
            if w.z < BILEK:
                val = 2.0
            elif False:                                           # ornek 1: yumurta gocdeyi ortunce kalcada beyaz bant kaliyordu -> govde beyazi yalniz yumurtada
                val = 1.0
            else:
                val = 0.0
            a_.data[v_.index].value = val
    pm = mat_govde(lin(hex3("#16161e")), 0.0); pm.name = "panda"; nt = pm.node_tree; bs = nt.nodes["Principled BSDF"]
    # 32 video 1 (kullanici: "ustu maskot, alti iskelet ... alti facia"): ince parlak insan uzuvlari -> TOMBUL MAT panda uzuvlari
    bs.inputs["Roughness"].default_value = 0.6; bs.inputs["Coat Weight"].default_value = 0.0
    for m_ in mesler:
        m_.hide_render = True                                         # 32 video 1 duzeltme 2: sisirme yetmedi -> insan govdesi gizli
    # kemiklere bagli TOMBUL panda uzuvlari: kalin siyah kapsul kol/bacak + yuvarlak pati + oval ayak (mat)
    pmat = mat_pbr_k = bpy.data.materials.new("panda_uzuv"); pmat.use_nodes = True
    pb_ = pmat.node_tree.nodes["Principled BSDF"]; pb_.inputs["Base Color"].default_value = (*lin(hex3("#1a1a24")), 1)
    pb_.inputs["Roughness"].default_value = 0.55; pb_.inputs["Coat Weight"].default_value = 0.15
    def uzuv(ad, r):
        b_ = kemik(arm, ad); L = ((arm.matrix_world @ b_.tail) - (arm.matrix_world @ b_.head)).length
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=L, vertices=28); c_ = bpy.context.active_object; bpy.ops.object.shade_smooth()
        c_.data.transform(Matrix.Rotation(math.radians(-90), 4, "X") @ Matrix.Translation((0, 0, L / 2))); c_.data.materials.append(pmat)
        EKIP.append((c_, ad, Matrix.Identity(4)))
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=24, ring_count=12); k_ = bpy.context.active_object; bpy.ops.object.shade_smooth()
        k_.data.materials.append(pmat); EKIP.append((k_, ad, Matrix.Identity(4)))
        return L
    for tr in ("Left", "Right"):
        uzuv(tr + "Arm", 0.052 * BOY); uzuv(tr + "ForeArm", 0.048 * BOY); uzuv(tr + "UpLeg", 0.075 * BOY); uzuv(tr + "Leg", 0.066 * BOY)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.058 * BOY, segments=24, ring_count=12); h_ = bpy.context.active_object; bpy.ops.object.shade_smooth()
        h_.data.materials.append(pmat); EKIP.append((h_, tr + "Hand", Matrix.Translation((0, 0.02 * BOY, 0))))
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=24, ring_count=12); f_ = bpy.context.active_object; bpy.ops.object.shade_smooth()
        f_.data.transform(Matrix.Diagonal((0.065 * BOY, 0.11 * BOY, 0.05 * BOY, 1))); f_.data.materials.append(pmat)
        EKIP.append((f_, tr + "Foot", Matrix.Translation((0, 0.04 * BOY, 0))))
    na = nt.nodes.new("ShaderNodeAttribute"); na.attribute_name = "pg"
    mp = nt.nodes.new("ShaderNodeMapRange"); mp.inputs["From Min"].default_value = 0; mp.inputs["From Max"].default_value = 2
    nt.links.new(na.outputs["Fac"], mp.inputs["Value"])
    rp = nt.nodes.new("ShaderNodeValToRGB"); cr = rp.color_ramp; cr.interpolation = "CONSTANT"
    cr.elements[0].position = 0.0; cr.elements[0].color = (*lin(hex3("#16161e")), 1)
    cr.elements[1].position = 0.75; cr.elements[1].color = (*lin(hex3("#16161e")), 1)
    e = cr.elements.new(0.25); e.color = (*lin(hex3("#f4f8ff")), 1)
    nt.links.new(mp.outputs["Result"], rp.inputs["Fac"]); nt.links.new(rp.outputs["Color"], bs.inputs["Base Color"])
    bs.inputs["Emission Color"].default_value = (*lin(hex3("#3a3a5a")), 1)
    for m in mesler:
        m.data.materials.clear(); m.data.materials.append(pm)
    # 31 yan gorunum kontrolu: ince insan govdesi penguen okunmuyordu -> gogus kemigine bagli TOMBUL YUMURTA govde (lacivert sirt, beyaz karin).
    # Kemik uzayinda y = kemik boyu (yukari); karin yonu dinlenme pozunda dunya -y'den (kameraya) hesaplanir, shader nesne normaliyle boyar.
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=48, ring_count=24)
    yum = bpy.context.active_object; bpy.ops.object.shade_smooth()
    yum.data.transform(Matrix.Diagonal((0.155 * BOY, 0.21 * BOY, 0.14 * BOY, 1)))
    Mb0 = (arm.matrix_world @ kemik(arm, "Spine1").matrix).to_3x3()
    on_d = Matrix.Rotation(math.radians(float(arg("--don", "0"))), 3, "Z") @ Vector((0, -1, 0))
    on_l = (Mb0.inverted() @ on_d).normalized()
    ym = mat_govde(lin(hex3("#16161e")), 0.0); ym.name = "pd_yumurta"; nt = ym.node_tree; bs = nt.nodes["Principled BSDF"]
    ge = nt.nodes.new("ShaderNodeNewGeometry"); vt = nt.nodes.new("ShaderNodeVectorTransform")
    vt.vector_type = "NORMAL"; vt.convert_from = "WORLD"; vt.convert_to = "OBJECT"
    nt.links.new(ge.outputs["Normal"], vt.inputs["Vector"])
    dp = nt.nodes.new("ShaderNodeVectorMath"); dp.operation = "DOT_PRODUCT"; dp.inputs[1].default_value = tuple(on_l)
    nt.links.new(vt.outputs["Vector"], dp.inputs[0])
    gt = nt.nodes.new("ShaderNodeMath"); gt.operation = "GREATER_THAN"; gt.inputs[1].default_value = 0.42
    nt.links.new(dp.outputs["Value"], gt.inputs[0])
    mx_ = nt.nodes.new("ShaderNodeMix"); mx_.data_type = "RGBA"; nt.links.new(gt.outputs[0], mx_.inputs["Factor"])
    mx_.inputs[6].default_value = (*lin(hex3("#f6f6fa")), 1); mx_.inputs[7].default_value = (*lin(hex3("#f6f6fa")), 1)   # panda: govde bastan sona beyaz
    nt.links.new(mx_.outputs[2], bs.inputs["Base Color"])
    yum.data.materials.append(ym)
    EKIP.append((yum, "Spine1", Matrix.Translation((0, 0.02 * BOY, 0))))
    log("panda yumurta karin yonu (kemik uzayi)", [round(c, 2) for c in on_l])
    ra = 0.07 * BOY                                                   # kirmizi Noel atkisi (atolye hakemi)
    bpy.ops.mesh.primitive_torus_add(major_radius=ra, minor_radius=ra * 0.36, major_segments=40, minor_segments=12)
    f_ = bpy.context.active_object; bpy.ops.object.shade_smooth(); f_.data.materials.append(mat_jole("pd_atki", lin(hex3("#e8102c")), emis=0.18, purluk=0.15))
    f_.data.transform(Matrix.Rotation(math.radians(-90), 4, "X"))
    EKIP.append((f_, "Neck", Matrix.Translation((0, 0.02 * BOY, 0))))

if OYUNCU == "maskot" and arg("--ejderha", "0") == "1":   # 33 (antik kum arenasi; TALIMATLAR §4 maskot sirasi): KUCUK EJDERHA yavrusu
    # 32'nin dersi (kullanici: "ustu maskot, alti iskelet"): insan govdesi gizli; kemiklere bagli TOMBUL yesil uzuvlar + yumurta govde
    # (yesil sirt, sari-turuncu karin), sirtta turuncu yarasa kanatlari, kalcadan sarkan tombul kuyruk + ok ucu. Kafa motorda 2B.
    YESIL, KARIN, KANAT = "#22c43a", "#ffc21e", "#ff7a14"
    for m_ in mesler:
        m_.hide_render = True
    def mat_ej(ad, renk, purluk=0.4, kap=0.35):
        m_ = bpy.data.materials.new(ad); m_.use_nodes = True; b_ = m_.node_tree.nodes["Principled BSDF"]
        b_.inputs["Base Color"].default_value = (*lin(hex3(renk)), 1)
        b_.inputs["Roughness"].default_value = purluk; b_.inputs["Coat Weight"].default_value = kap; b_.inputs["Coat Roughness"].default_value = 0.08
        return m_
    emat, kmat, sm = mat_ej("ej_uzuv", YESIL, 0.6, 0.12), mat_ej("ej_kanat", KANAT, 0.55, 0.1), mat_ej("ej_sari", KARIN, 0.45, 0.25)   # ornek 1: beyaz parlama seritleri -> mat (32 panda dersi)
    def uzuv(ad, r):
        b_ = kemik(arm, ad); L = ((arm.matrix_world @ b_.tail) - (arm.matrix_world @ b_.head)).length
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=L, vertices=28); c_ = bpy.context.active_object; bpy.ops.object.shade_smooth()
        c_.data.transform(Matrix.Rotation(math.radians(-90), 4, "X") @ Matrix.Translation((0, 0, L / 2))); c_.data.materials.append(emat)
        EKIP.append((c_, ad, Matrix.Identity(4)))
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=24, ring_count=12); k_ = bpy.context.active_object; bpy.ops.object.shade_smooth()
        k_.data.materials.append(emat); EKIP.append((k_, ad, Matrix.Identity(4)))
        return L
    for tr in ("Left", "Right"):
        uzuv(tr + "Arm", 0.05 * BOY); uzuv(tr + "ForeArm", 0.046 * BOY); uzuv(tr + "UpLeg", 0.075 * BOY); uzuv(tr + "Leg", 0.066 * BOY)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.056 * BOY, segments=24, ring_count=12); h_ = bpy.context.active_object; bpy.ops.object.shade_smooth()
        h_.data.materials.append(emat); EKIP.append((h_, tr + "Hand", Matrix.Translation((0, 0.02 * BOY, 0))))
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=24, ring_count=12); f_ = bpy.context.active_object; bpy.ops.object.shade_smooth()
        f_.data.transform(Matrix.Diagonal((0.068 * BOY, 0.115 * BOY, 0.05 * BOY, 1))); f_.data.materials.append(emat)
        EKIP.append((f_, tr + "Foot", Matrix.Translation((0, 0.04 * BOY, 0))))
        for dx in (-1, 0, 1):                                         # ayakta uc kucuk sari tirnak
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.018 * BOY, segments=12, ring_count=6); t_ = bpy.context.active_object
            t_.data.materials.append(sm); EKIP.append((t_, tr + "Foot", Matrix.Translation((dx * 0.035 * BOY, 0.14 * BOY, 0.0))))
    # yumurta govde: karin (kameraya donuk taraf) sari-turuncu, sirt yesil; karin yonu nesne normaliyle (31/32 yontemi)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=48, ring_count=24)
    yum = bpy.context.active_object; bpy.ops.object.shade_smooth()
    yum.data.transform(Matrix.Diagonal((0.155 * BOY, 0.21 * BOY, 0.145 * BOY, 1)))
    Mb0 = (arm.matrix_world @ kemik(arm, "Spine1").matrix).to_3x3()
    on_d = Matrix.Rotation(math.radians(float(arg("--don", "0"))), 3, "Z") @ Vector((0, -1, 0))
    on_l = (Mb0.inverted() @ on_d).normalized()
    ym = mat_ej("ej_yumurta", YESIL, 0.55, 0.15); nt = ym.node_tree; bs = nt.nodes["Principled BSDF"]
    ge = nt.nodes.new("ShaderNodeNewGeometry"); vt = nt.nodes.new("ShaderNodeVectorTransform")
    vt.vector_type = "NORMAL"; vt.convert_from = "WORLD"; vt.convert_to = "OBJECT"
    nt.links.new(ge.outputs["Normal"], vt.inputs["Vector"])
    dp = nt.nodes.new("ShaderNodeVectorMath"); dp.operation = "DOT_PRODUCT"; dp.inputs[1].default_value = tuple(on_l)
    nt.links.new(vt.outputs["Vector"], dp.inputs[0])
    gt = nt.nodes.new("ShaderNodeMath"); gt.operation = "GREATER_THAN"; gt.inputs[1].default_value = 0.42
    nt.links.new(dp.outputs["Value"], gt.inputs[0])
    mx_ = nt.nodes.new("ShaderNodeMix"); mx_.data_type = "RGBA"; nt.links.new(gt.outputs[0], mx_.inputs["Factor"])
    mx_.inputs[6].default_value = (*lin(hex3(YESIL)), 1); mx_.inputs[7].default_value = (*lin(hex3(KARIN)), 1)
    nt.links.new(mx_.outputs[2], bs.inputs["Base Color"])
    yum.data.materials.append(ym)
    EKIP.append((yum, "Spine1", Matrix.Translation((0, 0.02 * BOY, 0))))
    arka = (-on_l).normalized(); yan = Vector((0, 1, 0)).cross(on_l).normalized()
    log("ejderha karin yonu (kemik uzayi)", [round(c, 2) for c in on_l], "yan", [round(c, 2) for c in yan])
    for yy in (0.16, 0.06, -0.04, -0.13):                             # sirt dikenleri: yumurtanin sirt cizgisinde 4 sari koni
        bpy.ops.mesh.primitive_cone_add(radius1=0.03 * BOY, radius2=0.0, depth=0.06 * BOY, vertices=12); c_ = bpy.context.active_object
        c_.data.materials.append(sm)
        q = arka.to_track_quat("Z", "Y").to_matrix().to_4x4()
        c_.data.transform(Matrix.Translation(arka * (0.14 * BOY) + Vector((0, yy * BOY, 0))) @ q @ Matrix.Translation((0, 0, 0.02 * BOY)))
        EKIP.append((c_, "Spine1", Matrix.Translation((0, 0.02 * BOY, 0))))
    for s_ in (-1, 1):                                                # kanatlar: sirttan iki yana acilan yarasa kanadi, Spine2'ye bagli
        r0 = arka * (0.11 * BOY) + Vector((0, 0.06 * BOY, 0))
        uc = r0 + yan * (s_ * 0.30 * BOY) + Vector((0, 0.16 * BOY, 0)) + arka * (0.06 * BOY)
        nok = [r0, uc]
        for t, d_ in ((0.78, 0.10), (0.5, 0.13), (0.22, 0.09)):
            nok.append(r0 + yan * (s_ * 0.30 * BOY * t) + Vector((0, (0.16 * t - d_) * BOY, 0)) + arka * (0.06 * BOY * t))
        me = bpy.data.meshes.new("kanat"); me.from_pydata([tuple(v) for v in nok], [], [[0, 1, 2, 3, 4]]); me.update()
        o_ = bpy.data.objects.new("kanat", me); bpy.context.collection.objects.link(o_); o_.data.materials.append(kmat)
        o_.modifiers.new("k", "SOLIDIFY").thickness = 0.012 * BOY
        EKIP.append((o_, "Spine2", Matrix.Identity(4)))
        bpy.ops.mesh.primitive_cylinder_add(radius=0.012 * BOY, depth=(uc - r0).length, vertices=12); kb = bpy.context.active_object
        kb.data.materials.append(emat)
        q = (uc - r0).to_track_quat("Z", "Y").to_matrix().to_4x4()
        kb.data.transform(Matrix.Translation((r0 + uc) / 2) @ q)
        EKIP.append((kb, "Spine2", Matrix.Identity(4)))
    for i in range(6):                                                # kuyruk: kalcadan arkaya-asagi kivrilan, incelen 6 kure + sari ok ucu
        t = i / 5
        c = arka * ((0.10 + 0.16 * t) * BOY) + Vector((0, (-0.02 - 0.10 * t + 0.06 * t * t) * BOY, 0)) + yan * (0.05 * t * t * BOY)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=(0.06 - 0.035 * t) * BOY, segments=20, ring_count=10); k_ = bpy.context.active_object
        bpy.ops.object.shade_smooth(); k_.data.materials.append(emat); k_.data.transform(Matrix.Translation(c))
        EKIP.append((k_, "Hips", Matrix.Identity(4)))
    bpy.ops.mesh.primitive_cone_add(radius1=0.05 * BOY, radius2=0.0, depth=0.07 * BOY, vertices=4); k_ = bpy.context.active_object
    k_.data.materials.append(sm)
    q = arka.to_track_quat("Z", "Y").to_matrix().to_4x4()
    k_.data.transform(Matrix.Translation(c + arka * (0.04 * BOY)) @ q @ Matrix.Diagonal((1.0, 0.3, 1.0, 1)))
    EKIP.append((k_, "Hips", Matrix.Identity(4)))
    ra = 0.07 * BOY                                                   # kirmizi hakem fulari
    bpy.ops.mesh.primitive_torus_add(major_radius=ra, minor_radius=ra * 0.36, major_segments=40, minor_segments=12)
    f_ = bpy.context.active_object; bpy.ops.object.shade_smooth(); f_.data.materials.append(mat_jole("ej_ful", lin(hex3("#e8102c")), emis=0.18, purluk=0.15))
    f_.data.transform(Matrix.Rotation(math.radians(-90), 4, "X"))
    EKIP.append((f_, "Neck", Matrix.Translation((0, 0.02 * BOY, 0))))

if OYUNCU == "maskot" and arg("--sincap", "0") == "1":   # 35 (balon festivali; kullanici 20 Kas secimi C): UCAN SINCAP yavrusu
    # 33 ejderha blogunun kopyasi: insan govdesi gizli; kemiklere bagli TOMBUL uzuvlar + yumurta govde. Kanat yerine govde yanlarinda
    # bilekten kalcaya inen ince kanat zari (ucan sincap), dikensiz; kuyruk sirttan YUKARI kivrilan buyuk kabarik kure dizisi.
    KAHVE, KARIN, ZAR, KUYRUK_UC = "#c8642a", "#ffe0b0", "#e08a4a", "#ffe0b0"
    for m_ in mesler:
        m_.hide_render = True
    def mat_sc(ad, renk, purluk=0.6, kap=0.12):
        m_ = bpy.data.materials.new(ad); m_.use_nodes = True; b_ = m_.node_tree.nodes["Principled BSDF"]
        b_.inputs["Base Color"].default_value = (*lin(hex3(renk)), 1)
        b_.inputs["Roughness"].default_value = purluk; b_.inputs["Coat Weight"].default_value = kap; b_.inputs["Coat Roughness"].default_value = 0.1
        return m_
    emat, zmat, km = mat_sc("sc_uzuv", KAHVE), mat_sc("sc_zar", ZAR, 0.65, 0.05), mat_sc("sc_krem", KARIN, 0.55, 0.15)
    def uzuv(ad, r):
        b_ = kemik(arm, ad); L = ((arm.matrix_world @ b_.tail) - (arm.matrix_world @ b_.head)).length
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=L, vertices=28); c_ = bpy.context.active_object; bpy.ops.object.shade_smooth()
        c_.data.transform(Matrix.Rotation(math.radians(-90), 4, "X") @ Matrix.Translation((0, 0, L / 2))); c_.data.materials.append(emat)
        EKIP.append((c_, ad, Matrix.Identity(4)))
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=24, ring_count=12); k_ = bpy.context.active_object; bpy.ops.object.shade_smooth()
        k_.data.materials.append(emat); EKIP.append((k_, ad, Matrix.Identity(4)))
        return L
    for tr in ("Left", "Right"):
        uzuv(tr + "Arm", 0.05 * BOY); uzuv(tr + "ForeArm", 0.046 * BOY); uzuv(tr + "UpLeg", 0.075 * BOY); uzuv(tr + "Leg", 0.066 * BOY)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.054 * BOY, segments=24, ring_count=12); h_ = bpy.context.active_object; bpy.ops.object.shade_smooth()
        h_.data.materials.append(km); EKIP.append((h_, tr + "Hand", Matrix.Translation((0, 0.02 * BOY, 0))))
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=24, ring_count=12); f_ = bpy.context.active_object; bpy.ops.object.shade_smooth()
        f_.data.transform(Matrix.Diagonal((0.064 * BOY, 0.11 * BOY, 0.05 * BOY, 1))); f_.data.materials.append(km)
        EKIP.append((f_, tr + "Foot", Matrix.Translation((0, 0.04 * BOY, 0))))
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=48, ring_count=24)
    yum = bpy.context.active_object; bpy.ops.object.shade_smooth()
    yum.data.transform(Matrix.Diagonal((0.15 * BOY, 0.21 * BOY, 0.14 * BOY, 1)))
    Mb0 = (arm.matrix_world @ kemik(arm, "Spine1").matrix).to_3x3()
    on_d = Matrix.Rotation(math.radians(float(arg("--don", "0"))), 3, "Z") @ Vector((0, -1, 0))
    on_l = (Mb0.inverted() @ on_d).normalized()
    ym = mat_sc("sc_yumurta", KAHVE, 0.6, 0.15); nt = ym.node_tree; bs = nt.nodes["Principled BSDF"]
    ge = nt.nodes.new("ShaderNodeNewGeometry"); vt = nt.nodes.new("ShaderNodeVectorTransform")
    vt.vector_type = "NORMAL"; vt.convert_from = "WORLD"; vt.convert_to = "OBJECT"
    nt.links.new(ge.outputs["Normal"], vt.inputs["Vector"])
    dp = nt.nodes.new("ShaderNodeVectorMath"); dp.operation = "DOT_PRODUCT"; dp.inputs[1].default_value = tuple(on_l)
    nt.links.new(vt.outputs["Vector"], dp.inputs[0])
    gt = nt.nodes.new("ShaderNodeMath"); gt.operation = "GREATER_THAN"; gt.inputs[1].default_value = 0.62   # ornek 1: karin onden butun govdeyi kapliyordu
    nt.links.new(dp.outputs["Value"], gt.inputs[0])
    mx_ = nt.nodes.new("ShaderNodeMix"); mx_.data_type = "RGBA"; nt.links.new(gt.outputs[0], mx_.inputs["Factor"])
    mx_.inputs[6].default_value = (*lin(hex3(KAHVE)), 1); mx_.inputs[7].default_value = (*lin(hex3(KARIN)), 1)
    nt.links.new(mx_.outputs[2], bs.inputs["Base Color"])
    yum.data.materials.append(ym)
    EKIP.append((yum, "Spine1", Matrix.Translation((0, 0.02 * BOY, 0))))
    arka = (-on_l).normalized(); yan = Vector((0, 1, 0)).cross(on_l).normalized()
    log("sincap karin yonu (kemik uzayi)", [round(c, 2) for c in on_l], "yan", [round(c, 2) for c in yan])
    # ornek 1 (20 Kas): kanat zari karton levha gibi okundu -> kaldirildi; kuyruk boğum boğum karides kabugu gibiydi ve onden gorunmuyordu
    # -> az sayida, buyuk, ic ice gecen kurelerle puruzsuz kabarik kuyruk; govdenin bir yaninda omuz ustune kadar cikar (onden gorunur).
    uc_m = mat_sc("sc_kuyruk_uc", "#f0a060")      # ornek 2: krem uc basin yaninda ikinci bas gibi okundu -> acik turuncu
    for i in range(36):                                   # ornek 2: 11 kure bogum bogum okundu -> 36 sik kure, puruzsuz
        t = i / 35
        c = (arka * ((0.10 + 0.10 * math.sin(t * math.pi)) * BOY) + Vector((0, (-0.10 + 0.50 * t) * BOY, 0))
             + yan * ((0.10 + 0.08 * math.sin(t * math.pi * 0.8)) * BOY))
        bpy.ops.mesh.primitive_uv_sphere_add(radius=(0.075 + 0.04 * math.sin(t * math.pi * 0.9)) * BOY, segments=24, ring_count=12)
        k_ = bpy.context.active_object; bpy.ops.object.shade_smooth(); k_.data.materials.append(uc_m if i >= 30 else emat); k_.data.transform(Matrix.Translation(c))
        EKIP.append((k_, "Hips", Matrix.Identity(4)))
    ra = 0.08 * BOY                                                   # kirmizi hakem atkisi
    bpy.ops.mesh.primitive_torus_add(major_radius=ra, minor_radius=ra * 0.36, major_segments=40, minor_segments=12)
    f_ = bpy.context.active_object; bpy.ops.object.shade_smooth(); f_.data.materials.append(mat_jole("sc_atki", lin(hex3("#e8102c")), emis=0.18, purluk=0.15))
    f_.data.transform(Matrix.Rotation(math.radians(-90), 4, "X"))
    EKIP.append((f_, "Neck", Matrix.Translation((0, 0.02 * BOY, 0))))
    bpy.ops.mesh.primitive_cube_add(size=1.0); u_ = bpy.context.active_object      # atkinin sarkan ucu (gogus onunde, sola)
    u_.data.transform(Matrix.Translation(on_l * (0.08 * BOY) + yan * (0.04 * BOY) + Vector((0, -0.08 * BOY, 0))) @ Matrix.Diagonal((0.05 * BOY, 0.12 * BOY, 0.02 * BOY, 1)))
    u_.modifiers.new("b", "BEVEL").width = 0.008 * BOY; u_.data.materials.append(mat_jole("sc_atki2", lin(hex3("#e8102c")), emis=0.18, purluk=0.15))
    EKIP.append((u_, "Spine2", Matrix.Identity(4)))
if OYUNCU == "maskot" and arg("--baykus", "0") == "1":   # 36 (dev mantar ormani; kullanici 20 Kas secimi C): BAYKUS yavrusu
    # 35 sincap blogunun kopyasi: insan govdesi gizli; kemiklere bagli tombul uzuvlar. Govde = kure gibi yuvarlak tuy topu (yumurtadan genis),
    # kollar KANAT: Arm/ForeArm/Hand uzerinde yassi tuy dilimleri (poz kanatla okunur). Kuyruk: kisa tuy yelpazesi.
    KARAMEL, GOGUS, KANAT, KANAT_UC, AYAK = "#c8782a", "#ffc870", "#8a4a1a", "#e8a040", "#ff8a10"
    for m_ in mesler:
        m_.hide_render = True
    def mat_by(ad, renk, purluk=0.62, kap=0.12):
        m_ = bpy.data.materials.new(ad); m_.use_nodes = True; b_ = m_.node_tree.nodes["Principled BSDF"]
        b_.inputs["Base Color"].default_value = (*lin(hex3(renk)), 1)
        b_.inputs["Roughness"].default_value = purluk; b_.inputs["Coat Weight"].default_value = kap; b_.inputs["Coat Roughness"].default_value = 0.1
        b_.inputs["Sheen Weight"].default_value = 0.5; b_.inputs["Sheen Tint"].default_value = (*lin(hex3("#ffe0a0")), 1)   # tuy yumusakligi
        return m_
    gm, km, ku, am = mat_by("by_govde", KARAMEL), mat_by("by_kanat", KANAT), mat_by("by_kanat_uc", KANAT_UC), mat_by("by_ayak", AYAK, 0.4, 0.4)
    def kanat(ad, uz, gen, mat):
        """kemik boyunca yassi tuy dilimi: elipsoid, kemik yonunde uzun, bir eksende ince (kanat kalinligi)"""
        b_ = kemik(arm, ad); L = ((arm.matrix_world @ b_.tail) - (arm.matrix_world @ b_.head)).length
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=28, ring_count=14); k_ = bpy.context.active_object; bpy.ops.object.shade_smooth()
        k_.data.transform(Matrix.Translation((0, L * 0.5, 0)) @ Matrix.Diagonal((gen * BOY, L * uz, 0.035 * BOY, 1)))
        k_.data.materials.append(mat); EKIP.append((k_, ad, Matrix.Identity(4)))
        return L
    def bacak(ad, r):
        b_ = kemik(arm, ad); L = ((arm.matrix_world @ b_.tail) - (arm.matrix_world @ b_.head)).length
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=L, vertices=28); c_ = bpy.context.active_object; bpy.ops.object.shade_smooth()
        c_.data.transform(Matrix.Rotation(math.radians(-90), 4, "X") @ Matrix.Translation((0, 0, L / 2))); c_.data.materials.append(gm)
        EKIP.append((c_, ad, Matrix.Identity(4)))
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=24, ring_count=12); k_ = bpy.context.active_object; bpy.ops.object.shade_smooth()
        k_.data.materials.append(gm); EKIP.append((k_, ad, Matrix.Identity(4)))
    for tr in ("Left", "Right"):
        kanat(tr + "Arm", 0.72, 0.11, km); kanat(tr + "ForeArm", 0.72, 0.10, km)   # ornek 1: ince cubuk gibi -> genis tuy
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=24, ring_count=12); h_ = bpy.context.active_object; bpy.ops.object.shade_smooth()
        h_.data.transform(Matrix.Translation((0, 0.05 * BOY, 0)) @ Matrix.Diagonal((0.08 * BOY, 0.12 * BOY, 0.035 * BOY, 1)))   # kanat ucu tuyleri
        h_.data.materials.append(ku); EKIP.append((h_, tr + "Hand", Matrix.Identity(4)))
        bacak(tr + "UpLeg", 0.08 * BOY); bacak(tr + "Leg", 0.06 * BOY)
        for dx in (-0.035, 0.0, 0.035):                                   # uc parmakli turuncu ayak
            bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=20, ring_count=10); f_ = bpy.context.active_object; bpy.ops.object.shade_smooth()
            f_.data.transform(Matrix.Translation((dx * BOY, 0.03 * BOY, 0.05 * BOY)) @ Matrix.Diagonal((0.02 * BOY, 0.025 * BOY, 0.04 * BOY, 1)))
            f_.data.materials.append(am); EKIP.append((f_, tr + "Foot", Matrix.Identity(4)))
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=48, ring_count=24)
    yum = bpy.context.active_object; bpy.ops.object.shade_smooth()
    yum.data.transform(Matrix.Diagonal((0.19 * BOY, 0.22 * BOY, 0.18 * BOY, 1)))        # tuy topu: yumurtadan genis, neredeyse kure
    Mb0 = (arm.matrix_world @ kemik(arm, "Spine1").matrix).to_3x3()
    on_d = Matrix.Rotation(math.radians(float(arg("--don", "0"))), 3, "Z") @ Vector((0, -1, 0))
    on_l = (Mb0.inverted() @ on_d).normalized()
    ym = mat_by("by_yumurta", KARAMEL); nt = ym.node_tree; bs = nt.nodes["Principled BSDF"]
    ge = nt.nodes.new("ShaderNodeNewGeometry"); vt = nt.nodes.new("ShaderNodeVectorTransform")
    vt.vector_type = "NORMAL"; vt.convert_from = "WORLD"; vt.convert_to = "OBJECT"
    nt.links.new(ge.outputs["Normal"], vt.inputs["Vector"])
    dp = nt.nodes.new("ShaderNodeVectorMath"); dp.operation = "DOT_PRODUCT"; dp.inputs[1].default_value = tuple(on_l)
    nt.links.new(vt.outputs["Vector"], dp.inputs[0])
    gt = nt.nodes.new("ShaderNodeMath"); gt.operation = "GREATER_THAN"; gt.inputs[1].default_value = 0.8   # ornek 1: krem gogus butun onu kapliyordu (soluk alan)
    nt.links.new(dp.outputs["Value"], gt.inputs[0])
    tc = nt.nodes.new("ShaderNodeTexCoord"); vr = nt.nodes.new("ShaderNodeTexVoronoi"); vr.inputs["Scale"].default_value = 9.0
    nt.links.new(tc.outputs["Object"], vr.inputs["Vector"])
    lt = nt.nodes.new("ShaderNodeMath"); lt.operation = "LESS_THAN"; lt.inputs[1].default_value = 0.1
    nt.links.new(vr.outputs["Distance"], lt.inputs[0])
    mg = nt.nodes.new("ShaderNodeMix"); mg.data_type = "RGBA"; nt.links.new(lt.outputs[0], mg.inputs["Factor"])
    mg.inputs[6].default_value = (*lin(hex3(GOGUS)), 1); mg.inputs[7].default_value = (*lin(hex3("#d89a50")), 1)   # gogus tuy benekleri
    mx_ = nt.nodes.new("ShaderNodeMix"); mx_.data_type = "RGBA"; nt.links.new(gt.outputs[0], mx_.inputs["Factor"])
    mx_.inputs[6].default_value = (*lin(hex3(KARAMEL)), 1); nt.links.new(mg.outputs[2], mx_.inputs[7])
    nt.links.new(mx_.outputs[2], bs.inputs["Base Color"])
    yum.data.materials.append(ym)
    EKIP.append((yum, "Spine1", Matrix.Translation((0, 0.02 * BOY, 0))))
    arka = (-on_l).normalized(); yan = Vector((0, 1, 0)).cross(on_l).normalized()
    log("baykus gogus yonu (kemik uzayi)", [round(c, 2) for c in on_l], "yan", [round(c, 2) for c in yan])
    for a_ in (-0.5, 0.0, 0.5):                                       # kisa kuyruk tuy yelpazesi (arkada, alt)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=20, ring_count=10); t_ = bpy.context.active_object; bpy.ops.object.shade_smooth()
        c = arka * (0.17 * BOY) + Vector((0, -0.16 * BOY, 0)) + yan * (a_ * 0.06 * BOY)
        t_.data.transform(Matrix.Translation(c) @ Matrix.Diagonal((0.035 * BOY, 0.08 * BOY, 0.02 * BOY, 1)))
        t_.data.materials.append(km); EKIP.append((t_, "Hips", Matrix.Identity(4)))
    ra = 0.13 * BOY                                                   # yesil hakem atkisi (orman); ornek 1: govde icinde kayboluyordu
    bpy.ops.mesh.primitive_torus_add(major_radius=ra, minor_radius=ra * 0.36, major_segments=40, minor_segments=12)
    f_ = bpy.context.active_object; bpy.ops.object.shade_smooth(); f_.data.materials.append(mat_jole("by_atki", lin(hex3("#18b83a")), emis=0.15, purluk=0.2))
    f_.data.transform(Matrix.Rotation(math.radians(-90), 4, "X"))
    EKIP.append((f_, "Neck", Matrix.Translation((0, -0.02 * BOY, 0))))
    bpy.ops.mesh.primitive_cube_add(size=1.0); u_ = bpy.context.active_object      # atkinin sarkan ucu
    u_.data.transform(Matrix.Translation(on_l * (0.19 * BOY) + yan * (0.06 * BOY) + Vector((0, 0.0, 0))) @ Matrix.Diagonal((0.06 * BOY, 0.14 * BOY, 0.025 * BOY, 1)))
    u_.modifiers.new("b", "BEVEL").width = 0.008 * BOY; u_.data.materials.append(mat_jole("by_atki2", lin(hex3("#18b83a")), emis=0.15, purluk=0.2))
    EKIP.append((u_, "Spine2", Matrix.Identity(4)))
if OYUNCU == "maskot" and arg("--jole", "0") == "1":     # 34 (oyuncak blok sehri; TALIMATLAR §4 maskot sirasi): JOLE KUP
    # 32/33 dersi: insan govdesi gizli; kemiklere bagli TOMBUL uzuvlar. Govde = kalcadan basa kadar tek buyuk yuvarlatilmis jole kup
    # (turuncu-mango, ic isilti, yari mat cilali - beyaz parlama seridi olmasin). Yuz motorda 2B (kupun ust yarisina cizilir).
    JOLE, JOLE_K = "#ff8a10", "#e85a00"
    for m_ in mesler:
        m_.hide_render = True
    def mat_jk(ad, renk, purluk=0.32, kap=0.45, emis=0.12):
        m_ = bpy.data.materials.new(ad); m_.use_nodes = True; b_ = m_.node_tree.nodes["Principled BSDF"]
        b_.inputs["Base Color"].default_value = (*lin(hex3(renk)), 1)
        b_.inputs["Roughness"].default_value = purluk; b_.inputs["Coat Weight"].default_value = kap; b_.inputs["Coat Roughness"].default_value = 0.1
        b_.inputs["Subsurface Weight"].default_value = 0.45; b_.inputs["Subsurface Radius"].default_value = (0.6, 0.35, 0.15)   # ornek 1: plastik okunuyordu -> daha jole
        b_.inputs["Emission Color"].default_value = (*lin(hex3("#ffb040")), 1); b_.inputs["Emission Strength"].default_value = emis
        b_.inputs["Specular IOR Level"].default_value = 0.3
        return m_
    jm, jk = mat_jk("jole_govde", JOLE), mat_jk("jole_uzuv", JOLE_K, 0.45, 0.2, 0.06)
    def uzuv(ad, r):
        b_ = kemik(arm, ad); L = ((arm.matrix_world @ b_.tail) - (arm.matrix_world @ b_.head)).length
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=L, vertices=28); c_ = bpy.context.active_object; bpy.ops.object.shade_smooth()
        c_.data.transform(Matrix.Rotation(math.radians(-90), 4, "X") @ Matrix.Translation((0, 0, L / 2))); c_.data.materials.append(jk)
        EKIP.append((c_, ad, Matrix.Identity(4)))
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=24, ring_count=12); k_ = bpy.context.active_object; bpy.ops.object.shade_smooth()
        k_.data.materials.append(jk); EKIP.append((k_, ad, Matrix.Identity(4)))
        return L
    for tr in ("Left", "Right"):
        uzuv(tr + "Arm", 0.05 * BOY); uzuv(tr + "ForeArm", 0.046 * BOY); uzuv(tr + "UpLeg", 0.075 * BOY); uzuv(tr + "Leg", 0.066 * BOY)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.058 * BOY, segments=24, ring_count=12); h_ = bpy.context.active_object; bpy.ops.object.shade_smooth()
        h_.data.materials.append(jm); EKIP.append((h_, tr + "Hand", Matrix.Translation((0, 0.02 * BOY, 0))))
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=24, ring_count=12); f_ = bpy.context.active_object; bpy.ops.object.shade_smooth()
        f_.data.transform(Matrix.Diagonal((0.07 * BOY, 0.11 * BOY, 0.05 * BOY, 1))); f_.data.materials.append(jm)
        EKIP.append((f_, tr + "Foot", Matrix.Translation((0, 0.04 * BOY, 0))))
    # KUP govde: Spine1'e bagli; kemik uzayinda +Y = omurga yukari. Kalca ustunden bas tepesine kadar (~0,52 BOY), genislik 0,40 BOY
    bpy.ops.mesh.primitive_cube_add(size=1.0); kp = bpy.context.active_object
    kp.data.transform(Matrix.Translation((0, 0.10 * BOY, 0)) @ Matrix.Diagonal((0.46 * BOY, 0.46 * BOY, 0.42 * BOY, 1)))   # ornek 1: uzun kutu okunuyordu -> kup oranlari
    bv = kp.modifiers.new("egim", "BEVEL"); bv.width = 0.09 * BOY; bv.segments = 6; bv.limit_method = "NONE"
    bpy.ops.object.shade_smooth(); kp.data.materials.append(jm)
    EKIP.append((kp, "Spine1", Matrix.Identity(4)))
    log("jole kup govde: 0.46 x 0.46 x 0.42 BOY, Spine1 +0.10 BOY")

def ekip_yerlestir():
    for ob, ad, yerel in EKIP:
        Mb = arm.matrix_world @ kemik(arm, ad).matrix
        loc, rot, _ = Mb.decompose()
        ob.matrix_world = Matrix.LocRotScale(loc, rot, Vector((1, 1, 1))) @ yerel


# ---------------------------------------------------------------- kamera + isik (sabit olcek: butun pozlar ayni boyda)
CERCEVE = BOY * 1.42
bpy.ops.object.camera_add(location=(0, -12, alt0.z - BOY * 0.04 + CERCEVE / 2), rotation=(math.radians(90), 0, 0))
kam = bpy.context.active_object; sc.camera = kam; kam.data.type = "ORTHO"; kam.data.ortho_scale = CERCEVE * max(1, PXW / PXH)
m_ = (BOY / 1.8) ** 2
isik("AREA", (-1.3 * BOY, -1.8 * BOY, alt0.z + BOY * 1.3), 380 * m_, (1, 1, 1), boy=1.2 * BOY, yon=(0, 0, alt0.z + BOY * 0.6))
isik("AREA", (1.6 * BOY, 0.8 * BOY, alt0.z + BOY * 0.9), 500 * m_, acik(R, 0.2), boy=0.8 * BOY, yon=(0, 0, alt0.z + BOY * 0.6))
isik("AREA", (-1.6 * BOY, 1.0 * BOY, alt0.z + BOY * 0.9), 420 * m_, acik(R, 0.4), boy=0.8 * BOY, yon=(0, 0, alt0.z + BOY * 0.6))
isik("AREA", (0, 1.8 * BOY, alt0.z + BOY * 1.6), 380 * m_, (1, 1, 1), boy=1.0 * BOY, yon=(0, 0, alt0.z + BOY * 0.6))
ZEMIN = alt0.z
KALCA0 = (arm.matrix_world @ kemik(arm, "Hips").head).x

DUR = {"govde": 180, "bas": 0, "solKol": [12, 12], "sagKol": [-12, -12], "solBacak": [3, 0], "sagBacak": [-3, 0]}


def ara(a, b, q):
    if a == "geri" or b == "geri":
        return b if q > 0.5 else a
    return a + (b - a) * q


def uygula(P, q, arm=arm, mesler=mesler, ekip=True):
    """ayakta (DUR) -> P arasinda q (0..1) ile kemik yonleri; yon 'sag' / 'sol' pozlarda govde donusu de aradegerlenir"""
    pb = arm.pose.bones
    for b in pb:
        b.matrix_basis = Matrix.Identity(4)
    arm.location = (0, 0, 0)
    sx = {"on": 0, "sag": 1, "sol": -1}.get(P.get("yon", "on"), 0)
    arm.rotation_euler.z = TABAN_ROT + math.radians(90) * q * sx
    bpy.context.view_layer.update()
    ileri = (Vector((0, -1, 0)).lerp(Vector((sx, 0, 0)), q)).normalized() if sx else Vector((0, -1, 0))
    g = ara(DUR["govde"], P.get("govde", 180), q); ba = ara(0, P.get("bas", 0), q)
    for k_, aci in (("Spine", g), ("Spine1", g), ("Spine2", g), ("Neck", g + ba), ("Head", g + ba)):
        try:
            yonelt(arm, kemik(arm, k_), yon_vek(aci, ileri))
        except KeyError:
            pass
    for taraf, anah in (("Left", "sol"), ("Right", "sag")):
        kol0 = DUR[anah + "Kol"]; kol = P.get(anah + "Kol", kol0)
        yonelt(arm, kemik(arm, taraf + "Arm"), yon_vek(ara(kol0[0], kol[0], q), ileri))
        yonelt(arm, kemik(arm, taraf + "ForeArm"), yon_vek(ara(kol0[1], kol[1], q), ileri))
        yonelt(arm, kemik(arm, taraf + "Hand"), yon_vek(ara(kol0[1], kol[1], q), ileri))
        bac0 = DUR[anah + "Bacak"]; bac = P.get(anah + "Bacak", bac0)
        b0, b1 = ara(bac0[0], bac[0], q), ara(bac0[1], bac[1], q)
        yonelt(arm, kemik(arm, taraf + "UpLeg"), yon_vek(b0, ileri))
        yonelt(arm, kemik(arm, taraf + "Leg"), yon_vek(b1, ileri))
        baldir = yon_vek(b1, ileri)
        if baldir.dot(ileri) < -0.5 or b1 == "geri":
            ayak = (baldir * 0.7 + Vector((0, 0, -0.7))).normalized()
        else:
            ayak = (ileri * 0.9 + baldir * 0.35).normalized()
        yonelt(arm, kemik(arm, taraf + "Foot"), ayak)
    # yere oturt + kalca yatayda sabit (kok hareketi yok: yalniz zemin temasi korunur)
    alt, _ = dunya_kutusu(mesler)
    kx = (arm.matrix_world @ kemik(arm, "Hips").head).x
    arm.location = (KALCA0 - kx, 0, ZEMIN - alt.z)
    bpy.context.view_layer.update()
    if ekip:
        ekip_yerlestir()
        bpy.context.view_layer.update()


EKLEM = {"el": [("LeftHand", "kuyruk"), ("RightHand", "kuyruk")], "omuz": [("LeftArm", "bas"), ("RightArm", "bas")],
         "ayak": [("LeftToeBase", "bas"), ("RightToeBase", "bas")], "diz": [("LeftLeg", "bas"), ("RightLeg", "bas")],
         "kalca": [("LeftUpLeg", "bas"), ("RightUpLeg", "bas")], "bas": [("Head", "kuyruk")], "sirt": [("Spine2", "bas")]}


def eklemler(A, tur):
    out = []
    for ad, uc in EKLEM[tur]:
        b = kemik(A, ad)
        out.append(A.matrix_world @ (b.tail if uc == "kuyruk" else b.head))
    return out


def hizala(solA, solM, sagA, sagM, temas):
    """varlik-cadi.py hizala() ile ayni (duvardaki ikili maske bu kuralla kuruldu): sag figuru x'te kaydirir"""
    bpy.context.view_layer.update()
    if isinstance(temas, (int, float)):
        a1, u1 = dunya_kutusu(solM); a2, u2 = dunya_kutusu(sagM)
        sagA.location.x += (u1.x + temas) - a2.x
    elif temas == "yan":
        a1, u1 = dunya_kutusu(solM); a2, u2 = dunya_kutusu(sagM)
        sagA.location.x += (u1.x - 0.22) - a2.x
    else:
        p = max(eklemler(solA, temas[0]), key=lambda v: v.x)
        q_ = min(eklemler(sagA, temas[1]), key=lambda v: v.x)
        sagA.location.x += (p.x - 0.04) - q_.x
    bpy.context.view_layer.update()


if IKILI and OYUNCU != "maskot":
    # es govde: gorunmez, yalniz temas hizasi icin pozlanir
    once = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=os.path.join(KOK, "02-hareketler/siluet-govde.fbx"), automatic_bone_orientation=False)
    yeni2 = [o for o in bpy.data.objects if o not in once]
    ES = [o for o in yeni2 if o.type == "ARMATURE"][0]; ESM = [o for o in yeni2 if o.type == "MESH"]
    ES.animation_data_clear()
    for o in ESM:
        o.animation_data_clear(); o.hide_render = True
    ES.rotation_euler.z = TABAN_ROT; bpy.context.view_layer.update()
    BEN_SOL = OYUNCU == "p1"

    def ikili_kur(g_, q):
        G = GRUP[g_]
        uygula(G["figurler"][1 if BEN_SOL else 0], q, arm=ES, mesler=ESM, ekip=False)
        uygula(G["figurler"][0 if BEN_SOL else 1], q, ekip=False)
        sol, solM, sag, sagM = (arm, mesler, ES, ESM) if BEN_SOL else (ES, ESM, arm, mesler)
        sag.location.x = sol.location.x + 1.2 * BOY; bpy.context.view_layer.update()
        hizala(sol, solM, sag, sagM, G["temas"][0])
        ekip_yerlestir(); bpy.context.view_layer.update()
        return dunya_kutusu(mesler + ESM)

    # on gecis: ortak olcek (butun ikililer ayni boyda) + her grubun yatay merkezi (son pozun ikili kutusu)
    MERKEZ = {}; GEN = 0.0
    for g_ in TANIM:
        for q in (0.0, 1.0):
            a_, u_ = ikili_kur(g_, q)
            GEN = max(GEN, u_.x - a_.x)
        MERKEZ[g_] = (a_.x + u_.x) / 2
    OS = max(CERCEVE * PXW / PXH, GEN * 1.08)
    kam.data.ortho_scale = OS
    CER_H = OS * PXH / PXW
    kam.location.z = ZEMIN - BOY * 0.04 + CER_H / 2
    log("ikili ortak genislik", round(GEN, 2), "ortho", round(OS, 2), "boy/kare", round(BOY / CER_H, 3))
    yer = YERLESIM.setdefault("karakter", {}).setdefault(OYUNCU, {"boy_px": round(BOY / CER_H * PXH, 1),
        "zemin_px": round((1 - (ZEMIN - (kam.location.z - CER_H / 2)) / CER_H) * PXH, 1), "w_px": PXW, "h_px": PXH, "poz": {}})
    for g_ in TANIM:
        kam.location.x = MERKEZ[g_]; bpy.context.view_layer.update()
        kal = []
        for i in range(K):
            q = i / (K - 1); q = q * q * (3 - 2 * q)
            ikili_kur(g_, q)
            kv = world_to_camera_view(sc, kam, arm.matrix_world @ kemik(arm, "Hips").head)
            kal.append([round(kv.x * PXW, 1), round((1 - kv.y) * PXH, 1)])
            yaz(sc, "karakter/%s/%s-%02d.png" % (OYUNCU, g_, i))
        yer["poz"][g_] = {"kalca": kal}
    json.dump(YERLESIM, open(os.path.join(CIKTI, "yerlesim.json"), "w"), indent=1)
    log("bitti (karakter ikili)", OYUNCU, len(TANIM))
    raise SystemExit(0)

kafa_gizli = OYUNCU == "maskot"
if kafa_gizli:   # maskotun yuzu motorda cizilir: Mixamo kafasi gizlenir, kafa kemiginin yeri her karede yazilir
    hb = kemik(arm, "Head")
yer = YERLESIM.setdefault("karakter", {}).setdefault(OYUNCU, {"boy_px": round(BOY / CERCEVE * PX, 1), "zemin_px": round((1 - (ZEMIN - (kam.location.z - CERCEVE / 2)) / CERCEVE) * PX, 1), "poz": {}})
for ad, P in TANIM.items():
    kafa = []
    for i in range(K):
        q = i / (K - 1); q = q * q * (3 - 2 * q)
        uygula(P, q)
        hb_ = kemik(arm, "Head")
        h0 = arm.matrix_world @ hb_.head; h1 = arm.matrix_world @ hb_.tail
        mrk = h0 + (h1 - h0) * 0.6
        kv = world_to_camera_view(sc, kam, mrk)
        kafa.append([round(kv.x * PX, 1), round((1 - kv.y) * PX, 1), round(((h1 - h0).length * 1.25) / CERCEVE * PX, 1)])
        if kafa_gizli:
            hb_.scale = (0.01, 0.01, 0.01); bpy.context.view_layer.update()
        yaz(sc, "karakter/%s/%s-%02d.png" % (OYUNCU, ad, i))
    yer["poz"][ad] = {"kafa": kafa}
json.dump(YERLESIM, open(os.path.join(CIKTI, "yerlesim.json"), "w"), indent=1)
log("bitti (karakter)", OYUNCU, len(TANIM))
