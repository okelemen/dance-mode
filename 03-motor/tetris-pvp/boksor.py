"""TETRIS MODE 6. video (REF-057) acilis boksorleri - varlik.py --mod boksor ile calisir (yardimcilar oradan gelir).

    blender -b --factory-startup -noaudio -P 03-motor/tetris-pvp/varlik.py -- --cikti cikti --mod boksor --ornek 32

Kullanici 20 Eki 2026: "Acilista box yapan mavi ve pembe siluetler ... farkli sekilde bir oyuncu koyabilirsin ... efektli
bir sekilde gelsin" + "2 karakterli ... karsilikli duracak". Glow'un robot karakterinin kopyasi DEGIL: Mixamo govdesi
(siluet-govde.fbx) gercek boks klipleriyle (yana-boxing-orta = gard + ayak oyunu, yumruk-jab = jab) oynar; malzeme
oyuncu renginde parlak jole + kenar isiltisi, oyuncu renginde boks kaski + eldiven (beyaz mansetli). Karakter 3/4 acida ekran SAGINA bakar;
P2 sahne4.html'de yatay aynalanir (karsilikli durus).
Cikti: boksor/<oyuncu>-gard-NN.png (16 kare dongu), boksor/<oyuncu>-jab-NN.png (12 kare), 720x900 saydam.
"""

BOKS_RENK = {"p1": arg("--renk1", "#2E9BFF"), "p2": arg("--renk2", "#FF3EA5")}
KLIP = {"gard": ("02-hareketler/yana-boxing-orta.fbx", 16), "jab": ("02-hareketler/yumruk-jab.fbx", 12)}
os.makedirs(os.path.join(CIKTI, "boksor"), exist_ok=True)


def mat_neon_govde(ad, renk):
    """parlak jole govde + kenarda (fresnel) oyuncu renginde guclu isilti"""
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*acik(renk, 0.78), 1)      # govde acik parlak, ekipman renkli (deneme 2)
    b.inputs["Roughness"].default_value = 0.15
    b.inputs["Coat Weight"].default_value = 1.0
    b.inputs["Coat Roughness"].default_value = 0.02
    lw = nt.nodes.new("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.35
    mu = nt.nodes.new("ShaderNodeMath"); mu.operation = "MULTIPLY"; mu.inputs[1].default_value = 2.6
    nt.links.new(lw.outputs["Facing"], mu.inputs[0])
    b.inputs["Emission Color"].default_value = (*acik(renk, 0.15), 1)
    nt.links.new(mu.outputs[0], b.inputs["Emission Strength"])
    return m


def klip_aksiyonu(yol):
    once = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=os.path.join(KOK, yol), automatic_bone_orientation=False)
    yeni = [o for o in bpy.data.objects if o not in once]
    a = [o for o in yeni if o.type == "ARMATURE"][0]
    akt = a.animation_data.action
    akt.use_fake_user = True
    for o in yeni:
        bpy.data.objects.remove(o, do_unlink=True)
    return akt


def boksor(oyuncu):
    R = lin(hex3(BOKS_RENK[oyuncu]))
    sc = bos_sahne(w=720, h=900, saydam=True, ornek=min(ORNEK, 48))
    sc.render.film_transparent = True
    once = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=os.path.join(KOK, "02-hareketler/siluet-govde.fbx"), automatic_bone_orientation=False)
    yeni = [o for o in bpy.data.objects if o not in once]
    arm = [o for o in yeni if o.type == "ARMATURE"][0]
    mesler = [o for o in yeni if o.type == "MESH"]
    gm = mat_neon_govde("govde_" + oyuncu, R)
    for m in mesler:
        m.data.materials.clear(); m.data.materials.append(gm)
        for poly in m.data.polygons:
            poly.material_index = 0
    alt, ust = dunya_kutusu(mesler)
    boy = ust.z - alt.z
    log("boksor govde boy", round(boy, 3))
    # yuzu: once kameraya, sonra 3/4 aciyla ekran sagina
    L = arm.matrix_world @ kemik(arm, "LeftArm").head; Rr = arm.matrix_world @ kemik(arm, "RightArm").head
    v = L - Rr; v.z = 0
    arm.rotation_euler.z -= math.atan2(v.y, v.x)
    arm.rotation_euler.z += math.radians(62)
    bpy.context.view_layer.update()
    # ---- BOKS EKIPMANI (kullanici 20 Eki 2026: "kafasinda normal boksorlerin ne takiyorsa ... ellerinde eldivenleri")
    # kullanici 20 Eki 2026 (2): "elinde eldiveni, dizinde dizlikleri, kafasinda normal sembolik kafasini saran bir kask.
    # Mavi ve pembe renkli" -> kask basi tamamen sarar (yalniz yuz penceresi acik, yanak ve cene korumali), dizlik iki dizde.
    # eldiven: tombul yumruk + bilekte beyaz mansetli gercek boks eldiveni. Govde acik/beyaz parlak, ekipman oyuncu renginde.
    import bmesh
    ekip = mat_jole("ekipman_" + oyuncu, R, emis=0.35, purluk=0.06)
    beyaz = mat_jole("kenar_" + oyuncu, (0.92, 0.94, 1.0), emis=0.15, purluk=0.08)
    EKIP = []                                            # (obje, kemik adi, yerel matris)

    def kemik_boy(ad):
        b = kemik(arm, ad)
        return ((arm.matrix_world @ b.tail) - (arm.matrix_world @ b.head)).length

    def kemik_rot(ad):
        return (arm.matrix_world @ kemik(arm, ad).matrix).decompose()[1]

    # yuzun baktigi yon (karakter 62 derece ekran sagina donuk): kask yuz acikligi bu yone kesilir
    ileri = Vector((math.sin(math.radians(62)), -math.cos(math.radians(62)), 0))
    f_yerel = (kemik_rot("Head").to_matrix().inverted() @ ileri).normalized()
    Lh = kemik_boy("Head")
    rk = max(0.6 * Lh, 0.066 * boy)
    log("boksor kafa kemigi", round(Lh, 3), "kask r", round(rk, 3), "yuz yerel", tuple(round(x, 2) for x in f_yerel))
    me = bpy.data.meshes.new("kask_" + oyuncu); bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=40, v_segments=24, radius=rk)
    bmesh.ops.scale(bm, vec=(1.0, 1.1, 1.0), verts=bm.verts)
    sil = [v for v in bm.verts if (v.co.normalized().dot(f_yerel) > 0.66 and -0.45 * rk < v.co.y < 0.45 * rk) or v.co.y < -0.80 * rk]
    bmesh.ops.delete(bm, geom=sil, context="VERTS")
    bm.to_mesh(me); bm.free()
    kask = bpy.data.objects.new("kask_" + oyuncu, me); bpy.context.collection.objects.link(kask)
    kask.data.materials.append(ekip)
    so = kask.modifiers.new("dolgu", "SOLIDIFY"); so.thickness = 0.22 * rk; so.offset = 1.0
    so.use_rim = True; so.material_offset_rim = 1
    kask.data.materials.append(beyaz)                     # dolgu kenari (yuz acikligi ve alt kenar) beyaz
    sb = kask.modifiers.new("yumusak", "SUBSURF"); sb.levels = 1; sb.render_levels = 2
    for p_ in kask.data.polygons:
        p_.use_smooth = True
    EKIP.append((kask, "Head", Matrix.Translation((0, 0.42 * Lh, 0))))
    # yuz: kask penceresinde Mixamo yuzunun sac/goz ayrintisi dagnik gorunuyordu (deneme 2) -> REF-057 gibi puruzsuz beyaz yuz
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.93 * rk, segments=40, ring_count=24)
    yz = bpy.context.active_object; yz.data.materials.append(mat_jole("yuz_" + oyuncu, (0.96, 0.97, 1.0), emis=0.25, purluk=0.12))
    bpy.ops.object.shade_smooth(); yz.data.transform(Matrix.Diagonal((1.0, 1.08, 1.0, 1.0)))
    EKIP.append((yz, "Head", Matrix.Translation((0, 0.42 * Lh, 0))))
    # eldivenler
    rg = 0.062 * boy
    for taraf in ("Left", "Right"):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=rg, segments=40, ring_count=20)
        g_ = bpy.context.active_object; g_.data.materials.append(ekip); bpy.ops.object.shade_smooth()
        g_.data.transform(Matrix.Diagonal((1.0, 1.3, 1.05, 1.0)))       # yumruk: el boyunca uzun, tombul
        EKIP.append((g_, taraf + "Hand", Matrix.Translation((0, 0.85 * rg, 0))))
        bpy.ops.mesh.primitive_cylinder_add(radius=0.78 * rg, depth=1.0 * rg, vertices=40)
        m_ = bpy.context.active_object; m_.data.materials.append(beyaz); bpy.ops.object.shade_smooth()
        m_.data.transform(Matrix.Rotation(math.radians(90), 4, "X"))      # silindir ekseni kemik ekseni (Y)
        bv = m_.modifiers.new("egim", "BEVEL"); bv.width = 0.12 * rg; bv.segments = 4
        EKIP.append((m_, taraf + "Hand", Matrix.Translation((0, -0.25 * rg, 0))))
        bpy.ops.mesh.primitive_torus_add(major_radius=0.80 * rg, minor_radius=0.09 * rg)
        s_ = bpy.context.active_object; s_.data.materials.append(ekip); bpy.ops.object.shade_smooth()
        s_.data.transform(Matrix.Rotation(math.radians(90), 4, "X"))
        EKIP.append((s_, taraf + "Hand", Matrix.Translation((0, -0.05 * rg, 0))))   # manset ustunde renkli serit

    # dizlikler: dizi saran tombul ped (kaval kemiginin basinda), onde yuvarlak kapak, ust/alt beyaz bant
    rd = 0.048 * boy
    for taraf in ("Left", "Right"):
        fd = (kemik_rot(taraf + "Leg").to_matrix().inverted() @ ileri).normalized()
        bpy.ops.mesh.primitive_cylinder_add(radius=rd, depth=1.5 * rd, vertices=40)
        d_ = bpy.context.active_object; d_.data.materials.append(ekip); bpy.ops.object.shade_smooth()
        d_.data.transform(Matrix.Rotation(math.radians(90), 4, "X"))
        bv = d_.modifiers.new("egim", "BEVEL"); bv.width = 0.35 * rd; bv.segments = 6
        EKIP.append((d_, taraf + "Leg", Matrix.Translation((0, 0.12 * rd, 0))))
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.62 * rd, segments=32, ring_count=16)
        c_ = bpy.context.active_object; c_.data.materials.append(ekip); bpy.ops.object.shade_smooth()
        c_.data.transform(Matrix.Diagonal((1.0, 1.15, 0.6, 1.0)))
        EKIP.append((c_, taraf + "Leg", Matrix.Translation(fd * (0.85 * rd) + Vector((0, 0.1 * rd, 0)))))
        for yy in (-0.62, 0.86):
            bpy.ops.mesh.primitive_torus_add(major_radius=1.0 * rd, minor_radius=0.12 * rd)
            b_ = bpy.context.active_object; b_.data.materials.append(beyaz); bpy.ops.object.shade_smooth()
            b_.data.transform(Matrix.Rotation(math.radians(90), 4, "X"))
            EKIP.append((b_, taraf + "Leg", Matrix.Translation((0, yy * rd, 0))))

    def eldiven_yerlestir():
        for ob, ad, yerel in EKIP:
            Mb = arm.matrix_world @ kemik(arm, ad).matrix
            loc, rot, _ = Mb.decompose()
            ob.matrix_world = Matrix.LocRotScale(loc, rot, Vector((1, 1, 1))) @ yerel
    # kamera + isik: on dolgu, iki yandan oyuncu renginde kenar isigi, arkadan beyaz kontur
    # deneme 1: figur kadrajin %40'iydi -> dikey FOV'a gore mesafe (lens 50, sensor 36 dikey): boy*1.12 sigar
    bpy.ops.object.camera_add(location=(0.08 * boy, -1.75 * boy, alt.z + boy * 0.52), rotation=(math.radians(90), 0, 0))
    kam = bpy.context.active_object; sc.camera = kam; kam.data.lens = 50
    m_ = (boy / 1.8) ** 2                                    # govde 1,8 m degil (3,76 birim): isik enerjisi mesafeyle olceklenir
    isik("AREA", (-1.3 * boy, -1.8 * boy, alt.z + boy * 1.3), 380 * m_, (1, 1, 1), boy=1.2 * boy, yon=(0, 0, alt.z + boy * 0.6))
    isik("AREA", (1.6 * boy, 0.8 * boy, alt.z + boy * 0.9), 650 * m_, acik(R, 0.2), boy=0.8 * boy, yon=(0, 0, alt.z + boy * 0.6))
    isik("AREA", (-1.6 * boy, 1.0 * boy, alt.z + boy * 0.9), 500 * m_, acik(R, 0.4), boy=0.8 * boy, yon=(0, 0, alt.z + boy * 0.6))
    isik("AREA", (0, 1.8 * boy, alt.z + boy * 1.6), 420 * m_, (1, 1, 1), boy=1.0 * boy, yon=(0, 0, alt.z + boy * 0.6))
    for tur, (yol, n) in KLIP.items():
        akt = klip_aksiyonu(yol)
        # klip ve govdenin kemik oneki farkli olabilir (mixamorig: / mixamorig1:) -> yollari govdenin adlarina cevir
        adlar = {b.name.split(":")[-1]: b.name for b in arm.pose.bones}
        degisen = 0
        for fc in akt.fcurves:
            if fc.data_path.startswith('pose.bones["'):
                eski_ad = fc.data_path.split('"')[1]
                yeni_ad = adlar.get(eski_ad.split(":")[-1])
                if yeni_ad and yeni_ad != eski_ad:
                    fc.data_path = fc.data_path.replace('"%s"' % eski_ad, '"%s"' % yeni_ad); degisen += 1
        arm.animation_data_create(); arm.animation_data.action = akt
        log("boksor klip", tur, "fcurve", len(akt.fcurves), "ad cevrilen", degisen, "aralik", tuple(akt.frame_range))
        f0, f1 = akt.frame_range
        x0 = None
        for i in range(n):
            f = f0 + (f1 - f0) * i / n                       # dongu: son kare = ilk kare oldugu icin n'e bolunur
            sc.frame_set(int(f), subframe=f - int(f))
            # ayak oyunu kok hareketini kaydiriyor: yatayda gogus hizasini sabitle (kare kayma yapmasin)
            g = arm.matrix_world @ kemik(arm, "Spine2").head
            if x0 is None:
                x0 = (g.x, g.y)
            arm.location.x -= g.x - x0[0]; arm.location.y -= g.y - x0[1]
            bpy.context.view_layer.update()
            eldiven_yerlestir()
            bpy.context.view_layer.update()
            yaz(sc, "boksor/%s-%s-%02d.png" % (oyuncu, tur, i))
        YERLESIM.setdefault("boksor", {})["%s-%s" % (oyuncu, tur)] = n


for _o in ("p1", "p2"):
    boksor(_o)
json.dump(YERLESIM, open(os.path.join(CIKTI, "yerlesim.json"), "w"), indent=1)
log("bitti", YERLESIM)
