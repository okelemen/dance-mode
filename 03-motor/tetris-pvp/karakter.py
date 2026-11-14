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
"""
import bmesh

OYUNCU = arg("--oyuncu", "p1")                    # p1 | p2 | maskot
K = int(arg("--kare", "7"))
PX = int(arg("--px", "420"))
DUVAR = json.load(open(os.path.join(KOK, arg("--duvar", "03-motor/tetris-pvp/duvar-listesi-24.json")), encoding="utf-8"))
KAYNAK = json.load(open(os.path.join(KOK, arg("--kaynak", "03-motor/tetris-pvp/aday-olcu-24.json")), encoding="utf-8"))
POZ_DOSYA = {"varlik": "pozlar.json", "varlik-03": "pozlar-03.json", "varlik-04": "pozlar-04.json", "varlik-05": "pozlar-05.json"}
RENK_K = {"p1": "#2E9BFF", "p2": "#FF3EA5", "maskot": "#ff9ad8"}
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
        ADLAR = [a for d in DUVAR for a in (d["p1"], d["p2"])]
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
bpy.context.view_layer.update()
TABAN_ROT = arm.rotation_euler.z
alt0, ust0 = dunya_kutusu(mesler)
BOY = ust0.z - alt0.z
log("govde boy", round(BOY, 3))

# ---------------------------------------------------------------- ekipman (yalniz yarisan karakterler; VS kartindaki boksorlerin dili)
EKIP = []
if OYUNCU != "maskot":
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
