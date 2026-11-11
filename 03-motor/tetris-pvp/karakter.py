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

# poz adi -> aci tanimi (maskenin klasorune gore dogru pozlar dosyasi)
ad_klasor = {os.path.basename(k)[:-4]: k.split("/")[0] for k in KAYNAK}
if OYUNCU == "maskot":
    ADLAR = [a for d in DUVAR for a in (d["p1"], d["p2"])]
else:
    ADLAR = [d[OYUNCU] for d in DUVAR]
TANIM = {}
_onbellek = {}
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


sc = bos_sahne(w=PX, h=PX, saydam=True, ornek=min(ORNEK, 16))
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


def ekip_yerlestir():
    for ob, ad, yerel in EKIP:
        Mb = arm.matrix_world @ kemik(arm, ad).matrix
        loc, rot, _ = Mb.decompose()
        ob.matrix_world = Matrix.LocRotScale(loc, rot, Vector((1, 1, 1))) @ yerel


# ---------------------------------------------------------------- kamera + isik (sabit olcek: butun pozlar ayni boyda)
CERCEVE = BOY * 1.42
bpy.ops.object.camera_add(location=(0, -12, alt0.z - BOY * 0.04 + CERCEVE / 2), rotation=(math.radians(90), 0, 0))
kam = bpy.context.active_object; sc.camera = kam; kam.data.type = "ORTHO"; kam.data.ortho_scale = CERCEVE
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


def uygula(P, q):
    """ayakta (DUR) -> P arasinda q (0..1) ile kemik yonleri; yon 'sag' pozlarda govde donusu de aradegerlenir"""
    for b in pb:
        b.matrix_basis = Matrix.Identity(4)
    arm.location = (0, 0, 0)
    sag = P.get("yon") == "sag"
    arm.rotation_euler.z = TABAN_ROT + (math.radians(90) * q if sag else 0)
    bpy.context.view_layer.update()
    ileri = (Vector((0, -1, 0)).lerp(Vector((1, 0, 0)), q)).normalized() if sag else Vector((0, -1, 0))
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
    ekip_yerlestir()
    bpy.context.view_layer.update()


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
