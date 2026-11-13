"""CubeCut marka gorselleri (Blender, yalniz Actions'ta render): avokado kuplerinden harfler.
blender -b --factory-startup -noaudio -P marka3b.py -- --tur banner|profil --cikti cikti --ornek 48
"""
import ast
import json
import math
import os
import sys

import bpy
import numpy as np

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def arg(ad, vars=None):
    return argv[argv.index(ad) + 1] if ad in argv else vars


TUR = arg("--tur", "banner")
CIKTI = os.path.abspath(arg("--cikti", "cikti"))
ORNEK = int(arg("--ornek", "48"))
FPS = 30

# sahne.py'den yardimci fonksiyonlari al (tek kaynak): hex_renk, malzeme, baglan, matematik, bicak_kur
_kaynak = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sahne.py"), encoding="utf-8").read()
_agac = ast.parse(_kaynak)
_kod = [n for n in _agac.body if isinstance(n, ast.FunctionDef) and n.name in
        ("hex_renk", "malzeme", "baglan", "matematik", "bicak_kur")]
for ob in list(bpy.data.objects):
    bpy.data.objects.remove(ob, do_unlink=True)
sc = bpy.context.scene
exec(compile(ast.Module(body=_kod, type_ignores=[]), "sahne_yardimci", "exec"), globals())

sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = ORNEK
sc.cycles.use_denoising = True
if TUR == "banner":
    sc.render.resolution_x, sc.render.resolution_y = 2560, 1440
else:
    sc.render.resolution_x, sc.render.resolution_y = 800, 800
sc.render.resolution_percentage = 100
sc.render.image_settings.file_format = "PNG"
try:
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Punchy"
except Exception:
    pass
dunya = bpy.data.worlds.new("dunya")
sc.world = dunya
dunya.use_nodes = True
dunya.node_tree.nodes["Background"].inputs[0].default_value = hex_renk("#e8dcc4")
dunya.node_tree.nodes["Background"].inputs[1].default_value = 0.7
TAHTA_UST = 0.14

# --- canli mekan: parlak mermer + doygun nane-adacayi fayans
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0))
m, nt, bsdf = malzeme("mermer")
bsdf.inputs["Base Color"].default_value = hex_renk("#f2efe8")
bsdf.inputs["Roughness"].default_value = 0.18
bpy.context.object.data.materials.append(m)
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 2.2, 5), rotation=(math.radians(90), 0, 0))
m, nt, bsdf = malzeme("fayans")
tk = nt.nodes.new("ShaderNodeTexCoord")
br = nt.nodes.new("ShaderNodeTexBrick")
br.inputs["Scale"].default_value = 1.6
br.inputs["Mortar Size"].default_value = 0.014
br.inputs["Brick Width"].default_value = 0.5
br.inputs["Row Height"].default_value = 0.25
br.inputs["Color1"].default_value = hex_renk("#6fb37a")
br.inputs["Color2"].default_value = hex_renk("#82c48b")
br.inputs["Mortar"].default_value = hex_renk("#f6f1e2")
br.offset = 0.5
baglan(nt, tk.outputs["Object"], br.inputs["Vector"])
baglan(nt, br.outputs["Color"], bsdf.inputs["Base Color"])
bsdf.inputs["Roughness"].default_value = 0.22
bpy.context.object.data.materials.append(m)

# --- tahta
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.1, TAHTA_UST / 2))
tahta = bpy.context.object
tahta.scale = (4.4, 1.6, TAHTA_UST)
bpy.ops.object.transform_apply(scale=True)
tahta.modifiers.new("pah", "BEVEL").width = 0.04
m, nt, bsdf = malzeme("ahsap")
tk = nt.nodes.new("ShaderNodeTexCoord")
dl = nt.nodes.new("ShaderNodeTexWave")
dl.bands_direction = "X"
dl.inputs["Scale"].default_value = 3.0
dl.inputs["Distortion"].default_value = 10
baglan(nt, tk.outputs["Object"], dl.inputs["Vector"])
rm = nt.nodes.new("ShaderNodeValToRGB")
rm.color_ramp.elements[0].color = hex_renk("#c98a4b")
rm.color_ramp.elements[1].color = hex_renk("#e8b276")
baglan(nt, dl.outputs["Fac"], rm.inputs["Fac"])
baglan(nt, rm.outputs["Color"], bsdf.inputs["Base Color"])
bsdf.inputs["Roughness"].default_value = 0.45
tahta.data.materials.append(m)

rng = np.random.default_rng(3)


def kup_mesh(ad, merk, boy, renk, donus=None):
    k = len(merk)
    h = boy * 0.47
    ofs = np.array([[sx * h, sy * h, sz * h] for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)])
    if donus is not None:
        out = []
        for i in range(k):
            ax, ay, az = donus[i]
            cx, sx_ = math.cos(ax), math.sin(ax)
            cy, sy_ = math.cos(ay), math.sin(ay)
            cz, sz_ = math.cos(az), math.sin(az)
            Rm = np.array([[cz, -sz_, 0], [sz_, cz, 0], [0, 0, 1]]) @ np.array([[cy, 0, sy_], [0, 1, 0], [-sy_, 0, cy]]) @ np.array([[1, 0, 0], [0, cx, -sx_], [0, sx_, cx]])
            out.append(ofs @ Rm.T)
        o = np.stack(out)
    else:
        o = np.repeat(ofs[None], k, 0)
    v = (merk[:, None, :] + o).reshape(-1, 3)
    yuz = np.array([[0, 1, 3, 2], [4, 6, 7, 5], [0, 4, 5, 1], [2, 3, 7, 6], [0, 2, 6, 4], [1, 5, 7, 3]])
    f = (yuz[None] + (np.arange(k) * 8)[:, None, None]).reshape(-1, 4)
    me = bpy.data.meshes.new(ad)
    me.from_pydata(v.tolist(), [], f.tolist())
    me.update()
    ca = me.color_attributes.new("renk", "FLOAT_COLOR", "POINT")
    ca.data.foreach_set("color", np.hstack([np.repeat(renk, 8, 0), np.ones((k * 8, 1))]).ravel().astype(np.float32))
    ob = bpy.data.objects.new(ad, me)
    sc.collection.objects.link(ob)
    mk, ntk, bk = malzeme(ad + "_m")
    at = ntk.nodes.new("ShaderNodeAttribute")
    at.attribute_name = "renk"
    baglan(ntk, at.outputs["Color"], bk.inputs["Base Color"])
    bk.inputs["Roughness"].default_value = 0.35
    me.materials.append(mk)
    return ob


KABUK = np.array(hex_renk("#2f6a1e")[:3])
ET = np.array(hex_renk("#f5eaa0")[:3])
ET2 = np.array(hex_renk("#bfe06a")[:3])
CEK = np.array(hex_renk("#8a4a22")[:3])


def harf_kupleri(dosya, genislik, z0, derinlik=3, kopuk=None, kay=0.0):
    d = json.load(open(dosya))
    s = genislik / d["en"]
    merk, renk, don = [], [], []
    for x, y, kenar in d["kupler"]:
        for dz in range(derinlik):
            px = (x - d["en"] / 2 + 0.5) * s + kay
            pz = z0 + (y + 0.5) * s
            py = -0.1 + (dz - (derinlik - 1) / 2) * s
            on = dz == 0
            if kenar or dz == derinlik - 1:
                c = KABUK * rng.uniform(0.85, 1.15)
            else:
                c = (ET if rng.random() < 0.7 else ET2) * rng.uniform(0.92, 1.05)
            if not kenar and on and rng.random() < 0.03:
                c = CEK
            r_ = None
            if kopuk is not None and px > kopuk[0] and pz > kopuk[1]:  # bicak bu kosede: kupler dagilir
                if rng.random() < 0.55:  # kosenin bir kismi yerinde kalir (harf okunur)
                    merk.append((px, py, pz)); renk.append(c); don.append((0.0, 0.0, 0.0))
                    continue
                px += rng.uniform(0.05, 0.6)
                pz = max(TAHTA_UST + s / 2, pz - rng.uniform(0.0, pz - TAHTA_UST) * rng.uniform(0.6, 1.0))
                py += rng.uniform(-0.4, 0.3)
                r_ = rng.uniform(-1.2, 1.2, 3)
            merk.append((px, py, pz))
            renk.append(c)
            don.append(r_ if r_ is not None else (0.0, 0.0, 0.0))
    return np.array(merk), np.array(renk), np.array(don), s


if TUR == "banner":
    merk, renk, don, s = harf_kupleri("harf-cubecut.json", 3.3, TAHTA_UST, kopuk=(1.2, TAHTA_UST + 0.47), kay=-0.35)
    kup_mesh("harfler", merk, s, renk, don)
    # sagda kucuk avokado kup yigini, solda butun avokado
    n = 260
    yk = np.column_stack([rng.normal(1.75, 0.15, n), rng.normal(-0.25, 0.13, n), np.zeros(n)])
    yk[:, 2] = TAHTA_UST + 0.05 + np.maximum(0, 0.3 - np.hypot(yk[:, 0] - 1.75, yk[:, 1] + 0.25)) * rng.uniform(0.3, 1.0, n)
    rk = np.array([KABUK if rng.random() < 0.3 else (ET if rng.random() < 0.7 else ET2) for _ in range(n)])
    kup_mesh("yigin", yk, 0.09, rk, rng.uniform(-1.5, 1.5, (n, 3)))
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=48, radius=1.0, location=(-2.45, -0.15, TAHTA_UST + 0.36))
    av = bpy.context.object
    for v in av.data.vertices:
        x, y, z = v.co
        f = 0.6 + 0.4 * (x + 1) / 2
        v.co = (x * 0.55, y * 0.38 * f, z * 0.38 * f)
    av.rotation_euler = (0, 0, math.radians(-25))
    bpy.ops.object.shade_smooth()
    m, nt, bsdf = malzeme("kabuk")
    bsdf.inputs["Base Color"].default_value = hex_renk("#2f5a1c")
    bsdf.inputs["Roughness"].default_value = 0.25
    av.data.materials.append(m)
    # bicak: son harfi kesiyor (capraz, sag ustten)
    bicak = bicak_kur()
    bicak.scale = (0.5, 0.5, 0.5)
    bicak.rotation_euler = (math.radians(90), math.radians(-32), math.radians(180))
    bicak.location = (2.05, -0.1, TAHTA_UST + 0.98)
    kam_loc, hedef_loc, lens = (0.0, -9.6, 1.55), (0.0, -0.1, 0.62), 50
else:
    merk, renk, don, s = harf_kupleri("harf-c.json", 1.25, TAHTA_UST, derinlik=4, kopuk=(0.3, TAHTA_UST + 0.95))
    kup_mesh("harfler", merk, s, renk, don)
    kam_loc, hedef_loc, lens = (0.12, -2.75, 0.95), (0.12, -0.1, 0.8), 50

# isik: sicak gunes + dolgu (canli)
g = bpy.data.objects.new("gunes", bpy.data.lights.new("gunes", "SUN"))
g.data.energy = 4.0
g.data.color = (1.0, 0.95, 0.85)
g.data.angle = math.radians(8)
g.rotation_euler = (math.radians(48), math.radians(-30), math.radians(-28))
sc.collection.objects.link(g)
a = bpy.data.objects.new("dolgu", bpy.data.lights.new("dolgu", "AREA"))
a.data.energy = 500
a.data.size = 6
a.location = (-2.0, -5.0, 4.0)
a.rotation_euler = (math.radians(55), 0, math.radians(-20))
sc.collection.objects.link(a)
cam = bpy.data.cameras.new("kam")
cam.lens = lens
k = bpy.data.objects.new("kam", cam)
k.location = kam_loc
sc.collection.objects.link(k)
h = bpy.data.objects.new("hedef", None)
h.location = hedef_loc
sc.collection.objects.link(h)
c_ = k.constraints.new("TRACK_TO")
c_.target = h
c_.track_axis = "TRACK_NEGATIVE_Z"
c_.up_axis = "UP_Y"
sc.camera = k
cam.dof.use_dof = True
cam.dof.focus_object = h
cam.dof.aperture_fstop = 5.6
os.makedirs(CIKTI, exist_ok=True)
sc.render.filepath = os.path.join(CIKTI, f"{TUR}.png")
if arg("--render", "1") == "1":
    bpy.ops.render.render(write_still=True)
print("MARKA", TUR, "tamam", flush=True)
