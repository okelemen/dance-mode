"""TETRIS MODE 6. video (REF-057) acilis boksorleri - varlik.py --mod boksor ile calisir (yardimcilar oradan gelir).

    blender -b --factory-startup -noaudio -P 03-motor/tetris-pvp/varlik.py -- --cikti cikti --mod boksor --ornek 32

Kullanici 20 Eki 2026: "Acilista box yapan mavi ve pembe siluetler ... farkli sekilde bir oyuncu koyabilirsin ... efektli
bir sekilde gelsin" + "2 karakterli ... karsilikli duracak". Glow'un robot karakterinin kopyasi DEGIL: Mixamo govdesi
(siluet-govde.fbx) gercek boks klipleriyle (yana-boxing-orta = gard + ayak oyunu, yumruk-jab = jab) oynar; malzeme
oyuncu renginde parlak jole + kenar isiltisi, beyaz-renkli eldivenler. Karakter 3/4 acida ekran SAGINA bakar;
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
    b.inputs["Base Color"].default_value = (*koyu(renk, 0.25), 1)
    b.inputs["Roughness"].default_value = 0.15
    b.inputs["Coat Weight"].default_value = 1.0
    b.inputs["Coat Roughness"].default_value = 0.02
    lw = nt.nodes.new("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.35
    mu = nt.nodes.new("ShaderNodeMath"); mu.operation = "MULTIPLY"; mu.inputs[1].default_value = 6.0
    nt.links.new(lw.outputs["Facing"], mu.inputs[0])
    b.inputs["Emission Color"].default_value = (*acik(renk, 0.35), 1)
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
    # eldivenler: el kemigine bagli tombul kure (ust yarisi beyaz parlak, govde rengi bilek bandi)
    eld = mat_jole("eldiven_" + oyuncu, acik(R, 0.55), emis=0.25, purluk=0.08)
    bant = mat_jole("bant_" + oyuncu, R, emis=0.6, purluk=0.1)
    for taraf in ("Left", "Right"):
        kb = kemik(arm, taraf + "Hand")
        for r_, mat, ofs in ((0.062 * boy, eld, 0.55), (0.040 * boy, bant, 0.0)):
            bpy.ops.mesh.primitive_uv_sphere_add(radius=r_, segments=32, ring_count=16)
            k = bpy.context.active_object; k.data.materials.append(mat); bpy.ops.object.shade_smooth()
            k.parent = arm; k.parent_type = "BONE"; k.parent_bone = kb.name
            k.location = (0, kb.length * ofs, 0)          # kemik ekseni boyunca (bone uzayi Y)
    # kafa bandi: oyuncu renginde parlak halka
    kk = kemik(arm, "Head")
    bpy.ops.mesh.primitive_torus_add(major_radius=0.062 * boy, minor_radius=0.010 * boy)
    t = bpy.context.active_object; t.data.materials.append(mat_emis("kafabandi_" + oyuncu, acik(R, 0.2), 6.0))
    t.parent = arm; t.parent_type = "BONE"; t.parent_bone = kk.name; t.location = (0, kk.length * 0.35, 0)
    # yuzu: once kameraya, sonra 3/4 aciyla ekran sagina
    L = arm.matrix_world @ kemik(arm, "LeftArm").head; Rr = arm.matrix_world @ kemik(arm, "RightArm").head
    v = L - Rr; v.z = 0
    arm.rotation_euler.z -= math.atan2(v.y, v.x)
    arm.rotation_euler.z += math.radians(62)
    bpy.context.view_layer.update()
    # kamera + isik: on dolgu, iki yandan oyuncu renginde kenar isigi, arkadan beyaz kontur
    bpy.ops.object.camera_add(location=(0, -5.2 * boy / 1.8, alt.z + boy * 0.55), rotation=(math.radians(88), 0, 0))
    kam = bpy.context.active_object; sc.camera = kam; kam.data.lens = 50
    isik("AREA", (-2.5, -3.5, alt.z + boy * 1.3), 380, (1, 1, 1), boy=2.5, yon=(0, 0, alt.z + boy * 0.6))
    isik("AREA", (3.0, 1.5, alt.z + boy * 0.9), 650, acik(R, 0.2), boy=1.5, yon=(0, 0, alt.z + boy * 0.6))
    isik("AREA", (-3.0, 2.0, alt.z + boy * 0.9), 500, acik(R, 0.4), boy=1.5, yon=(0, 0, alt.z + boy * 0.6))
    isik("AREA", (0, 3.5, alt.z + boy * 1.6), 420, (1, 1, 1), boy=2.0, yon=(0, 0, alt.z + boy * 0.6))
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
            yaz(sc, "boksor/%s-%s-%02d.png" % (oyuncu, tur, i))
        YERLESIM.setdefault("boksor", {})["%s-%s" % (oyuncu, tur)] = n


for _o in ("p1", "p2"):
    boksor(_o)
json.dump(YERLESIM, open(os.path.join(CIKTI, "yerlesim.json"), "w"), indent=1)
log("bitti", YERLESIM)
