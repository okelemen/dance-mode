"""KESIM SAYACI - Blender sahnesi (yalniz GitHub Actions'ta render edilir).

blender -b --factory-startup -noaudio -P sahne.py -- --plan plan-avokado.json --cikti cikti \
    [--bas 1 --son 120 | --kareler 30,200,900] [--ornek 24]

Sahne tamamen koddan kurulur: ahsap tahta, koyu fayans, gri duvar, avokado, bicak.
Her sey anahtar karelerle (handler yok): bicak inisleri, kesim cizgileri (shader degerleri),
tur sonu kup yigini (her tur ayri nesne + 'cokme' sekil anahtari).
"""
import json
import math
import os
import sys

import bpy
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plan import icinde, mango_yaprak_icinde, meyve_profil, profil_yaricap

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def arg(ad, vars=None):
    if ad in argv:
        return argv[argv.index(ad) + 1]
    return vars


PLAN = json.load(open(arg("--plan"), encoding="utf-8"))
CIKTI = os.path.abspath(arg("--cikti", "cikti"))
ORNEK = int(arg("--ornek", "6"))
FPS = PLAN["fps"]
M = PLAN["sekil"]
FMAX = PLAN["fmax"]
A, R = M["A"], M["R"]
CILEK = PLAN["meyve"] == "strawberry"
KARPUZ = PLAN["meyve"] == "watermelon"
KIVI = PLAN["meyve"] == "kiwi"
MANGO = PLAN["meyve"] == "mango"
B = M.get("B", R)
TAHTA_UST = 0.14
MERKEZ_Z = TAHTA_UST + R - 0.03
GORSEL_TAVAN = 120  # gorsel kup izgarasi eksen basina en fazla (sayi plandaki gercek degerdir)


def hex_renk(h, a=1.0):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((x / 12.92) if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4) for x in c) + (a,)


def kare(t):
    f = t * FPS
    r = round(f)
    return (r if abs(f - r) < 1e-3 else f) + 1.0  # karede olan anlar tam kareye oturur


# ---------------------------------------------------------------- sahne temizligi
for ob in list(bpy.data.objects):
    bpy.data.objects.remove(ob, do_unlink=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = ORNEK
sc.cycles.use_denoising = True
try:
    sc.cycles.denoiser = "OPENIMAGEDENOISE"
except Exception:
    pass
sc.cycles.max_bounces = 2
sc.cycles.use_adaptive_sampling = True
sc.cycles.adaptive_threshold = 0.04
sc.render.use_persistent_data = True
sc.render.resolution_x = 1080
sc.render.resolution_y = 1920
sc.render.resolution_percentage = int(arg("--yuzde", "50"))  # kural: hep hizli mod
sc.render.fps = FPS
sc.frame_start = 1
sc.frame_end = PLAN["kare"]
sc.render.use_motion_blur = False
sc.render.motion_blur_shutter = 0.5
sc.render.image_settings.file_format = "PNG"
sc.render.image_settings.color_mode = "RGB"
try:
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Medium High Contrast"
except Exception:
    pass

dunya = bpy.data.worlds.new("dunya")
sc.world = dunya
dunya.use_nodes = True
dunya.node_tree.nodes["Background"].inputs[0].default_value = hex_renk("#303b35")
dunya.node_tree.nodes["Background"].inputs[1].default_value = 0.25


# ---------------------------------------------------------------- malzeme yardimcilari
def malzeme(ad):
    m = bpy.data.materials.new(ad)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    return m, nt, bsdf


def baglan(nt, a, b):
    nt.links.new(a, b)


def matematik(nt, islem, a=None, b=None, deger_a=0.0, deger_b=0.0):
    n = nt.nodes.new("ShaderNodeMath")
    n.operation = islem
    if a is not None:
        nt.links.new(a, n.inputs[0])
    else:
        n.inputs[0].default_value = deger_a
    if b is not None:
        nt.links.new(b, n.inputs[1])
    else:
        n.inputs[1].default_value = deger_b
    return n.outputs[0]


def mango_cekirdek_maske(nt, x, y, z):
    """Uzun X, dar Y ve orta Z eksenli gercek yassi cekirdek hacmi."""
    ck = M["cekirdek"]
    toplam = None
    for deger, merkez, yari in ((x, ck["x"] * A, ck["a"]),
                                (y, 0.0, ck["b"]), (z, 0.0, ck["r"])):
        q = matematik(nt, "DIVIDE", matematik(nt, "SUBTRACT", deger, None, deger_b=merkez),
                     None, deger_b=yari)
        q2 = matematik(nt, "MULTIPLY", q, q)
        toplam = q2 if toplam is None else matematik(nt, "ADD", toplam, q2)
    return matematik(nt, "LESS_THAN", toplam, None, deger_b=1.0), toplam


def mango_kabuk(nt, vector):
    """Yesil-sari zemin, kameraya bakan tarafta turuncu-kirmizi gun yanigi."""
    xyz = nt.nodes.new("ShaderNodeSeparateXYZ")
    baglan(nt, vector, xyz.inputs[0])
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 3.6
    noise.inputs["Detail"].default_value = 3.0
    baglan(nt, vector, noise.inputs["Vector"])
    taban = nt.nodes.new("ShaderNodeValToRGB")
    taban.color_ramp.elements[0].color = hex_renk("#587a36")
    taban.color_ramp.elements[1].color = hex_renk("#e9b83e")
    baglan(nt, noise.outputs["Fac"], taban.inputs["Fac"])
    on = matematik(nt, "MULTIPLY", matematik(nt, "SUBTRACT", None, xyz.outputs[1], deger_a=0.12),
                   None, deger_b=2.0)
    on = matematik(nt, "MINIMUM", matematik(nt, "MAXIMUM", on, None, deger_b=0.0), None, deger_b=1.0)
    allik = matematik(nt, "MULTIPLY", on,
                      matematik(nt, "GREATER_THAN", xyz.outputs[0], None, deger_b=-0.75 * A))
    kar = nt.nodes.new("ShaderNodeMix"); kar.data_type = "RGBA"
    baglan(nt, allik, kar.inputs["Factor"])
    baglan(nt, taban.outputs["Color"], kar.inputs[6])
    kar.inputs[7].default_value = hex_renk("#cf512d")
    return kar.outputs[2]


def karpuz_serit(nt, vector):
    """X boyunca surekli fakat hafif dalgalanan boyuna kabuk seritleri."""
    xyz = nt.nodes.new("ShaderNodeSeparateXYZ")
    baglan(nt, vector, xyz.inputs[0])
    x, y, z = xyz.outputs[0], xyz.outputs[1], xyz.outputs[2]
    aci = matematik(nt, "ARCTAN2", z, y)
    dalga1 = matematik(nt, "SINE", matematik(nt, "ADD",
        matematik(nt, "MULTIPLY", x, None, deger_b=6.0),
        matematik(nt, "MULTIPLY", aci, None, deger_b=2.0)))
    dalga2 = matematik(nt, "SINE", matematik(nt, "SUBTRACT",
        matematik(nt, "MULTIPLY", x, None, deger_b=13.0),
        matematik(nt, "MULTIPLY", aci, None, deger_b=3.0)))
    faz = matematik(nt, "ADD", matematik(nt, "MULTIPLY", aci, None, deger_b=9.0),
        matematik(nt, "ADD", matematik(nt, "MULTIPLY", dalga1, None, deger_b=0.35),
                            matematik(nt, "MULTIPLY", dalga2, None, deger_b=0.15)))
    serit = matematik(nt, "GREATER_THAN", matematik(nt, "SINE", faz), None, deger_b=0.05)
    renk = nt.nodes.new("ShaderNodeMix"); renk.data_type = "RGBA"
    baglan(nt, serit, renk.inputs["Factor"])
    renk.inputs[6].default_value = hex_renk("#143c27")
    renk.inputs[7].default_value = hex_renk("#6c9c49")
    return renk.outputs[2]


KARPUZ_CEKIRDEKLER = [
    (fx * A, fy * R, fz * R)
    for fx, yz in ((-0.60, ((-0.21, 0.17), (0.22, -0.18))),
                   (-0.20, ((0.14, 0.22), (-0.24, -0.11))),
                   (0.20, ((-0.17, -0.20), (0.22, 0.15))),
                   (0.60, ((0.18, -0.16), (-0.20, 0.20))))
    for fy, fz in yz
] if KARPUZ else []


def karpuz_cekirdek_maske(nt, x, y, z):
    """Ayni sonlu 3B cekirdek konumlari kesitte ve kup malzemesinde kullanilir."""
    maske = None
    for sx, sy, sz in KARPUZ_CEKIRDEKLER:
        dx = matematik(nt, "DIVIDE", matematik(nt, "SUBTRACT", x, None, deger_b=sx), None, deger_b=0.075)
        dy = matematik(nt, "DIVIDE", matematik(nt, "SUBTRACT", y, None, deger_b=sy), None, deger_b=0.065)
        dz = matematik(nt, "DIVIDE", matematik(nt, "SUBTRACT", z, None, deger_b=MERKEZ_Z + sz), None, deger_b=0.11)
        d2 = matematik(nt, "ADD", matematik(nt, "ADD", matematik(nt, "MULTIPLY", dx, dx),
                                                   matematik(nt, "MULTIPLY", dy, dy)), matematik(nt, "MULTIPLY", dz, dz))
        tek = matematik(nt, "LESS_THAN", d2, None, deger_b=1.0)
        maske = tek if maske is None else matematik(nt, "MAXIMUM", maske, tek)
    return maske


def kivi_ic_renk(nt, x, y, z, yaricap, tohum_kapisi=None):
    """Ayni radyal et/oz/kabuk ve acisal isin/tohum alani kesitte ve kupte."""
    rad = matematik(nt, "SQRT", matematik(nt, "ADD",
        matematik(nt, "MULTIPLY", y, y), matematik(nt, "MULTIPLY", z, z)))
    u = matematik(nt, "DIVIDE", rad, yaricap)
    et = nt.nodes.new("ShaderNodeValToRGB")
    et.color_ramp.elements[0].color = hex_renk("#f6f1d8")
    et.color_ramp.elements[1].position = 1.0
    et.color_ramp.elements[1].color = hex_renk("#5e422d")
    for pos, renk in ((0.25, "#f2eed1"), (0.31, "#c8e68d"),
                      (0.47, "#72c83e"), (0.76, "#48ab2f"),
                      (0.91, "#8fc75c"), (0.965, "#d5d8a1"),
                      (0.985, "#8a6747")):
        el = et.color_ramp.elements.new(pos); el.color = hex_renk(renk)
    baglan(nt, u, et.inputs["Fac"])
    aci = matematik(nt, "ARCTAN2", z, y)
    faz = matematik(nt, "ADD", matematik(nt, "MULTIPLY", aci, None, deger_b=40.0),
                    matematik(nt, "MULTIPLY", x, None, deger_b=2.0))
    dalga = matematik(nt, "COSINE", faz)
    isin = matematik(nt, "MULTIPLY", matematik(nt, "GREATER_THAN", dalga, None, deger_b=0.93),
        matematik(nt, "MULTIPLY", matematik(nt, "GREATER_THAN", u, None, deger_b=0.30),
                    matematik(nt, "LESS_THAN", u, None, deger_b=0.88)))
    isikli = nt.nodes.new("ShaderNodeMix"); isikli.data_type = "RGBA"
    baglan(nt, matematik(nt, "MULTIPLY", isin, None, deger_b=0.62), isikli.inputs["Factor"])
    baglan(nt, et.outputs["Color"], isikli.inputs[6])
    isikli.inputs[7].default_value = hex_renk("#e1ecab")
    tohum = matematik(nt, "MULTIPLY", matematik(nt, "GREATER_THAN", dalga, None, deger_b=0.45),
        matematik(nt, "MULTIPLY", matematik(nt, "GREATER_THAN", u, None, deger_b=0.38),
                    matematik(nt, "LESS_THAN", u, None, deger_b=0.53)))
    if tohum_kapisi is not None:
        tohum = matematik(nt, "MULTIPLY", tohum, tohum_kapisi)
    benek = nt.nodes.new("ShaderNodeMix"); benek.data_type = "RGBA"
    baglan(nt, tohum, benek.inputs["Factor"])
    baglan(nt, isikli.outputs[2], benek.inputs[6])
    benek.inputs[7].default_value = hex_renk("#10150d")
    return benek.outputs[2], u


def cilek_aken(nt, vector, ana_renk, bsdf, dis_maske=None, temel_normal=None):
    """Iri oval altin aken, koyu sig cukur ve ona eslik eden fiziksel bump."""
    esne = nt.nodes.new("ShaderNodeVectorMath")
    esne.operation = "MULTIPLY"
    esne.inputs[1].default_value = (0.72, 1.0, 1.18)
    baglan(nt, vector, esne.inputs[0])
    vor = nt.nodes.new("ShaderNodeTexVoronoi")
    vor.inputs["Scale"].default_value = 13.5
    baglan(nt, esne.outputs["Vector"], vor.inputs["Vector"])
    cukur = matematik(nt, "LESS_THAN", vor.outputs["Distance"], None, deger_b=0.27)
    aken = matematik(nt, "LESS_THAN", vor.outputs["Distance"], None, deger_b=0.17)
    if dis_maske is not None:
        cukur = matematik(nt, "MULTIPLY", cukur, dis_maske)
        aken = matematik(nt, "MULTIPLY", aken, dis_maske)
    oyuk_rengi = nt.nodes.new("ShaderNodeMix"); oyuk_rengi.data_type = "RGBA"
    baglan(nt, cukur, oyuk_rengi.inputs["Factor"])
    baglan(nt, ana_renk, oyuk_rengi.inputs[6])
    oyuk_rengi.inputs[7].default_value = hex_renk("#862b28")
    cekirdek_rengi = nt.nodes.new("ShaderNodeMix"); cekirdek_rengi.data_type = "RGBA"
    baglan(nt, aken, cekirdek_rengi.inputs["Factor"])
    baglan(nt, oyuk_rengi.outputs[2], cekirdek_rengi.inputs[6])
    cekirdek_rengi.inputs[7].default_value = hex_renk("#f4ce80")
    baglan(nt, cekirdek_rengi.outputs[2], bsdf.inputs["Base Color"])
    yukseklik = matematik(nt, "SUBTRACT",
                         matematik(nt, "MULTIPLY", aken, None, deger_b=0.28),
                         matematik(nt, "MULTIPLY", cukur, None, deger_b=0.23))
    pit_bump = nt.nodes.new("ShaderNodeBump")
    pit_bump.inputs["Strength"].default_value = 0.48
    pit_bump.inputs["Distance"].default_value = 0.025
    baglan(nt, yukseklik, pit_bump.inputs["Height"])
    if temel_normal is not None:
        baglan(nt, temel_normal, pit_bump.inputs["Normal"])
    baglan(nt, pit_bump.outputs["Normal"], bsdf.inputs["Normal"])


# ---------------------------------------------------------------- mekan: mermer tezgah
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0))
zemin = bpy.context.object
m, nt, bsdf = malzeme("mermer")
tk = nt.nodes.new("ShaderNodeTexCoord")
nzm = nt.nodes.new("ShaderNodeTexNoise")
nzm.inputs["Scale"].default_value = 0.9
nzm.inputs["Detail"].default_value = 6
nzm.inputs["Distortion"].default_value = 2.5
baglan(nt, tk.outputs["Object"], nzm.inputs["Vector"])
dm = nt.nodes.new("ShaderNodeTexWave")
dm.inputs["Scale"].default_value = 0.6
dm.inputs["Distortion"].default_value = 9.0
dm.inputs["Detail"].default_value = 6.0
baglan(nt, nzm.outputs["Color"], dm.inputs["Vector"])
dmr = nt.nodes.new("ShaderNodeValToRGB")
dmr.color_ramp.elements[0].position = 0.0
dmr.color_ramp.elements[0].color = hex_renk("#252c2a")
dmr.color_ramp.elements[1].position = 0.12
dmr.color_ramp.elements[1].color = hex_renk("#414743")
baglan(nt, dm.outputs["Fac"], dmr.inputs["Fac"])
baglan(nt, dmr.outputs["Color"], bsdf.inputs["Base Color"])
bsdf.inputs["Roughness"].default_value = 0.38
zemin.data.materials.append(m)

# ---------------------------------------------------------------- mekan: adacayi yesili metro fayans duvar
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 2.6, 5), rotation=(math.radians(90), 0, 0))
duvar = bpy.context.object
m, nt, bsdf = malzeme("fayans_duvar")
tk = nt.nodes.new("ShaderNodeTexCoord")
br = nt.nodes.new("ShaderNodeTexBrick")
br.inputs["Scale"].default_value = 1.6
br.inputs["Mortar Size"].default_value = 0.012
br.inputs["Brick Width"].default_value = 0.5
br.inputs["Row Height"].default_value = 0.25
br.inputs["Color1"].default_value = hex_renk("#263a34")
br.inputs["Color2"].default_value = hex_renk("#334940")
br.inputs["Mortar"].default_value = hex_renk("#172621")
br.offset = 0.5
baglan(nt, tk.outputs["Object"], br.inputs["Vector"])
baglan(nt, br.outputs["Color"], bsdf.inputs["Base Color"])
bmp = nt.nodes.new("ShaderNodeBump")
bmp.inputs["Strength"].default_value = 0.35
bmp.invert = True
baglan(nt, br.outputs["Fac"], bmp.inputs["Height"])
baglan(nt, bmp.outputs["Normal"], bsdf.inputs["Normal"])
bsdf.inputs["Roughness"].default_value = 0.48
duvar.data.materials.append(m)

# ---------------------------------------------------------------- kesme tahtasi
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.1, TAHTA_UST / 2))
tahta = bpy.context.object
tahta.scale = (3.7, 2.5, TAHTA_UST)
bpy.ops.object.transform_apply(scale=True)
bv = tahta.modifiers.new("pah", "BEVEL")
bv.width = 0.04
bv.segments = 3
m, nt, bsdf = malzeme("ahsap")
tk = nt.nodes.new("ShaderNodeTexCoord")
mp = nt.nodes.new("ShaderNodeMapping")
mp.inputs["Scale"].default_value = (0.35, 3.0, 1.0)
baglan(nt, tk.outputs["Object"], mp.inputs["Vector"])
dalga = nt.nodes.new("ShaderNodeTexWave")
dalga.wave_type = "BANDS"
dalga.bands_direction = "Y"
dalga.inputs["Scale"].default_value = 1.5
dalga.inputs["Distortion"].default_value = 11.0
dalga.inputs["Detail"].default_value = 3.0
baglan(nt, mp.outputs["Vector"], dalga.inputs["Vector"])
rmp = nt.nodes.new("ShaderNodeValToRGB")
rmp.color_ramp.elements[0].color = hex_renk("#b97e44")
rmp.color_ramp.elements[1].color = hex_renk("#deaa6c")
baglan(nt, dalga.outputs["Fac"], rmp.inputs["Fac"])
baglan(nt, rmp.outputs["Color"], bsdf.inputs["Base Color"])
bsdf.inputs["Roughness"].default_value = 0.55
tahta.data.materials.append(m)

# ---------------------------------------------------------------- nesne govdesi
bpy.ops.mesh.primitive_uv_sphere_add(segments=96, ring_count=64, radius=1.0, location=(0, 0, MERKEZ_Z))
meyve = bpy.context.object
meyve.name = "meyve"
# Kure -> plan.py ile birebir ayni profil; cilekte dikey eksen Z.
for v in meyve.data.vertices:
    x, y, z = v.co
    eks = z if CILEK else x
    sphere_r = math.sqrt(max(0.0, 1.0 - eks * eks))
    radial = float(meyve_profil(np.array([eks]), M)[0]) / max(sphere_r, 1e-6) / FMAX
    if CILEK:
        v.co = (x * A * radial, y * B * radial, z * R)
    elif MANGO:
        v.co = (x * A, y * B * radial,
                z * R * radial + 0.09 * math.sin(math.pi * x))
    else:
        v.co = (x * A, y * R * radial, z * R * radial)
bpy.ops.object.shade_smooth()

m, nt, bsdf = malzeme("mango_alacali_kabuk" if MANGO else ("kivi_kisa_tuylu_kabuk" if KIVI else ("karpuz_seritli_kabuk" if KARPUZ else ("cilek_yuzey" if CILEK else "avokado_kabuk"))))
tk = nt.nodes.new("ShaderNodeTexCoord")
nz = nt.nodes.new("ShaderNodeTexNoise")
nz.inputs["Scale"].default_value = 5
nz.inputs["Detail"].default_value = 4
baglan(nt, tk.outputs["Object"], nz.inputs["Vector"])
vor = nt.nodes.new("ShaderNodeTexVoronoi")
vor.inputs["Scale"].default_value = 38
baglan(nt, tk.outputs["Object"], vor.inputs["Vector"])
kabuk_rmp = nt.nodes.new("ShaderNodeValToRGB")
kabuk_rmp.color_ramp.elements[0].color = hex_renk("#56402d" if KIVI else ("#a81722" if CILEK else "#1d3014"))
kabuk_rmp.color_ramp.elements[1].color = hex_renk("#997852" if KIVI else ("#e53639" if CILEK else "#4a6b2c"))
baglan(nt, nz.outputs["Fac"], kabuk_rmp.inputs["Fac"])
yukseklik = matematik(nt, "ADD", nz.outputs["Fac"], vor.outputs["Distance"])
bmp = nt.nodes.new("ShaderNodeBump")
bmp.inputs["Strength"].default_value = 0.24 if KIVI else (0.08 if CILEK else 0.12)
bmp.inputs["Distance"].default_value = 0.008 if KIVI else (0.01 if CILEK else 0.02)
if KIVI:
    kisa_tuy = nt.nodes.new("ShaderNodeTexNoise")
    kisa_tuy.inputs["Scale"].default_value = 96
    kisa_tuy.inputs["Detail"].default_value = 2
    baglan(nt, tk.outputs["Object"], kisa_tuy.inputs["Vector"])
    yukseklik = matematik(nt, "ADD", yukseklik,
        matematik(nt, "MULTIPLY", kisa_tuy.outputs["Fac"], None, deger_b=0.65))
baglan(nt, yukseklik, bmp.inputs["Height"])
kabuk_rengi = (mango_kabuk(nt, tk.outputs["Object"]) if MANGO else
                karpuz_serit(nt, tk.outputs["Object"]) if KARPUZ else kabuk_rmp.outputs["Color"])
if MANGO:
    xyz_sap = nt.nodes.new("ShaderNodeSeparateXYZ")
    baglan(nt, tk.outputs["Object"], xyz_sap.inputs[0])
    sap_alan = matematik(nt, "MULTIPLY",
        matematik(nt, "LESS_THAN", xyz_sap.outputs[0], None, deger_b=-0.78 * A),
        matematik(nt, "MULTIPLY",
            matematik(nt, "LESS_THAN", matematik(nt, "ABSOLUTE", xyz_sap.outputs[1]), None, deger_b=0.13),
            matematik(nt, "GREATER_THAN", xyz_sap.outputs[2], None, deger_b=0.08)))
    sap_renk = nt.nodes.new("ShaderNodeMix"); sap_renk.data_type = "RGBA"
    baglan(nt, sap_alan, sap_renk.inputs["Factor"])
    baglan(nt, kabuk_rengi, sap_renk.inputs[6])
    sap_renk.inputs[7].default_value = hex_renk("#765739")
    kabuk_rengi = sap_renk.outputs[2]

# kesim cizgileri: her eksen icin n=c+1 ve yapilan kesim sayisi d (anahtar kareli Value dugumleri)
ayir = nt.nodes.new("ShaderNodeSeparateXYZ")
baglan(nt, tk.outputs["Object"], ayir.inputs[0])
DEGER = {}
cizgi_top = None
for eks, idx, yar in (("x", 0, A), ("y", 1, B), ("z", 2, R)):
    vn = nt.nodes.new("ShaderNodeValue"); vn.name = f"n_{eks}"; vn.outputs[0].default_value = 1.0
    vd = nt.nodes.new("ShaderNodeValue"); vd.name = f"d_{eks}"; vd.outputs[0].default_value = 0.0
    DEGER[eks] = (vn, vd)
    koord = ayir.outputs[idx]
    if eks == "z":
        koord = matematik(nt, "SUBTRACT", koord, None, deger_b=0.0)  # nesne uzayi, merkez 0
    u = matematik(nt, "DIVIDE", matematik(nt, "ADD", koord, None, deger_b=yar), None, deger_b=2 * yar)
    s = matematik(nt, "MULTIPLY", u, vn.outputs[0])
    en_yakin = matematik(nt, "ROUND", s)
    uzak = matematik(nt, "ABSOLUTE", matematik(nt, "SUBTRACT", s, en_yakin))
    ince = matematik(nt, "LESS_THAN", uzak, None, deger_b=-1.0)  # kullanici: kesim izi yok
    # gorunur: en_yakin >= n - d  ve en_yakin <= n - 1 ve d > 0
    alt = matematik(nt, "SUBTRACT", vn.outputs[0], vd.outputs[0])
    k1 = matematik(nt, "GREATER_THAN", en_yakin, matematik(nt, "SUBTRACT", alt, None, deger_b=0.5))
    k2 = matematik(nt, "LESS_THAN", en_yakin, matematik(nt, "SUBTRACT", vn.outputs[0], None, deger_b=0.5))
    k3 = matematik(nt, "GREATER_THAN", vd.outputs[0], None, deger_b=0.5)
    c = matematik(nt, "MULTIPLY", matematik(nt, "MULTIPLY", ince, k1), matematik(nt, "MULTIPLY", k2, k3))
    cizgi_top = c if cizgi_top is None else matematik(nt, "MAXIMUM", cizgi_top, c)

kar = nt.nodes.new("ShaderNodeMix")
kar.data_type = "RGBA"
baglan(nt, cizgi_top, kar.inputs["Factor"])
baglan(nt, kabuk_rengi, kar.inputs[6])
kar.inputs[7].default_value = hex_renk("#f5bcc1" if CILEK else "#c3df86")
if CILEK:
    cilek_aken(nt, tk.outputs["Object"], kar.outputs[2], bsdf,
               temel_normal=bmp.outputs["Normal"])
else:
    baglan(nt, kar.outputs[2], bsdf.inputs["Base Color"])
    baglan(nt, bmp.outputs["Normal"], bsdf.inputs["Normal"])
bsdf.inputs["Roughness"].default_value = 0.35 if MANGO else (0.88 if KIVI else (0.42 if CILEK else (0.34 if KARPUZ else 0.26)))
kes_x = nt.nodes.new("ShaderNodeValue"); kes_x.name = "kes_x"; kes_x.outputs[0].default_value = -10.0
kirp = matematik(nt, "LESS_THAN", ayir.outputs[0], kes_x.outputs[0])
seffaf = nt.nodes.new("ShaderNodeBsdfTransparent")
karis_s = nt.nodes.new("ShaderNodeMixShader")
baglan(nt, kirp, karis_s.inputs[0])
baglan(nt, bsdf.outputs[0], karis_s.inputs[1])
baglan(nt, seffaf.outputs[0], karis_s.inputs[2])
baglan(nt, karis_s.outputs[0], nt.nodes["Material Output"].inputs["Surface"])
meyve.data.materials.append(m)

mango_yaprak = None
mango_yaprak_nt = None
if MANGO:
    # Yaprak tek mesh olarak govdeye bagli; kes_x shader'i ayni vurusla kirpar.
    # Kesilen hacim asagidaki ana kup nokta kumesine de dahil edilir.
    verts, faces = [], []
    for i in range(13):
        t = i / 12
        xx = -A + 0.08 + 0.54 * t
        yy = -0.14
        zz = 0.54 - 0.06 * t
        gen = 0.16 * math.sin(math.pi * t) + 0.035
        verts.extend([(xx, yy - gen, zz - 0.055), (xx, yy + gen, zz - 0.055),
                      (xx, yy + gen, zz + 0.055), (xx, yy - gen, zz + 0.055)])
        if i:
            b = 4 * (i - 1); n = 4 * i
            faces.extend([(b+j, b+(j+1)%4, n+(j+1)%4, n+j) for j in range(4)])
    faces.extend([(3, 2, 1, 0), tuple(4*12+j for j in range(4))])
    leaf_mesh = bpy.data.meshes.new("mango_yaprak_mesh")
    leaf_mesh.from_pydata(verts, [], faces)
    leaf_mesh.update()
    mango_yaprak = bpy.data.objects.new("mango_kesilen_yaprak", leaf_mesh)
    sc.collection.objects.link(mango_yaprak)
    mango_yaprak.parent = meyve
    lm, mango_yaprak_nt, lb = malzeme("mango_yaprak_yesili")
    lb.inputs["Base Color"].default_value = hex_renk("#3f782e")
    lb.inputs["Roughness"].default_value = 0.72
    lxyz = mango_yaprak_nt.nodes.new("ShaderNodeSeparateXYZ")
    ltc = mango_yaprak_nt.nodes.new("ShaderNodeTexCoord")
    baglan(mango_yaprak_nt, ltc.outputs["Object"], lxyz.inputs[0])
    lkes = mango_yaprak_nt.nodes.new("ShaderNodeValue"); lkes.name = "kes_x"
    lkes.outputs[0].default_value = -10.0
    lclip = matematik(mango_yaprak_nt, "LESS_THAN", lxyz.outputs[0], lkes.outputs[0])
    ltrans = mango_yaprak_nt.nodes.new("ShaderNodeBsdfTransparent")
    lmix = mango_yaprak_nt.nodes.new("ShaderNodeMixShader")
    baglan(mango_yaprak_nt, lclip, lmix.inputs[0])
    baglan(mango_yaprak_nt, lb.outputs[0], lmix.inputs[1])
    baglan(mango_yaprak_nt, ltrans.outputs[0], lmix.inputs[2])
    baglan(mango_yaprak_nt, lmix.outputs[0], mango_yaprak_nt.nodes["Material Output"].inputs["Surface"])
    mango_yaprak.data.materials.append(lm)

kivi_tuy = None
kivi_tuy_nt = None
if KIVI:
    # Siluette gorunen gercek kisa tuyler; yuzeydeki ince bump ile birlikte.
    tuy_egri = bpy.data.curves.new("kivi_kisa_tuyler", "CURVE")
    tuy_egri.dimensions = "3D"
    tuy_egri.bevel_depth = 0.0019
    tuy_egri.bevel_resolution = 1
    rng_t = np.random.default_rng(2026)
    for _ in range(2100):
        xx = float(rng_t.uniform(-0.96 * A, 0.96 * A))
        rr = float(profil_yaricap(np.array([xx]), M, FMAX)[0])
        aci = float(rng_t.uniform(0, 2 * math.pi))
        yy, zz = math.cos(aci), math.sin(aci)
        boy = float(rng_t.uniform(0.015, 0.032))
        c = tuy_egri.splines.new("POLY")
        c.points.add(1)
        c.points[0].co = (xx, rr * yy, rr * zz, 1)
        c.points[1].co = (xx + float(rng_t.uniform(-0.007, 0.007)),
                          (rr + boy) * yy, (rr + boy) * zz, 1)
    kivi_tuy = bpy.data.objects.new("kivi_gercek_kisa_tuy", tuy_egri)
    sc.collection.objects.link(kivi_tuy)
    kivi_tuy.parent = meyve
    tuy_m, kivi_tuy_nt, tuy_bsdf = malzeme("kivi_tuy_m")
    tuy_bsdf.inputs["Base Color"].default_value = hex_renk("#b5966c")
    tuy_bsdf.inputs["Roughness"].default_value = 1.0
    tuy_tc = kivi_tuy_nt.nodes.new("ShaderNodeTexCoord")
    tuy_xyz = kivi_tuy_nt.nodes.new("ShaderNodeSeparateXYZ")
    baglan(kivi_tuy_nt, tuy_tc.outputs["Object"], tuy_xyz.inputs[0])
    tuy_kes = kivi_tuy_nt.nodes.new("ShaderNodeValue")
    tuy_kes.name = "kes_x"
    tuy_kes.outputs[0].default_value = -10.0
    tuy_sil = matematik(kivi_tuy_nt, "LESS_THAN", tuy_xyz.outputs[0], tuy_kes.outputs[0])
    tuy_saydam = kivi_tuy_nt.nodes.new("ShaderNodeBsdfTransparent")
    tuy_mix = kivi_tuy_nt.nodes.new("ShaderNodeMixShader")
    baglan(kivi_tuy_nt, tuy_sil, tuy_mix.inputs[0])
    baglan(kivi_tuy_nt, tuy_bsdf.outputs[0], tuy_mix.inputs[1])
    baglan(kivi_tuy_nt, tuy_saydam.outputs[0], tuy_mix.inputs[2])
    baglan(kivi_tuy_nt, tuy_mix.outputs[0], kivi_tuy_nt.nodes["Material Output"].inputs["Surface"])
    tuy_egri.materials.append(tuy_m)

# Cilegin yesil canak yapraklari ve kisa sapi, meyveyle birlikte duser.
canak = None
if CILEK:
    yaprak_m, _, yaprak_bsdf = malzeme("cilek_canak_yesili")
    yaprak_bsdf.inputs["Base Color"].default_value = hex_renk("#357c2b")
    yaprak_bsdf.inputs["Roughness"].default_value = 0.62
    def on_yuz(x, z):
        rr = float(profil_yaricap(np.array([z]), M, FMAX)[0])
        return -B * math.sqrt(max(0.0, rr * rr - (x / A) ** 2)) - 0.035

    vs, fs = [], []
    # Ustteki yedi sepal -Y on yuzune iner; karsidan gorulen tac x boyunca yayilir.
    for i in range(-3, 4):
        base_x = i * 0.035
        base_z = R * 0.87
        tip_x = i * 0.18
        tip_z = R * (0.45 + 0.035 * abs(i))
        mid_x = (base_x + tip_x) * 0.5
        mid_z = (base_z + tip_z) * 0.5
        j = len(vs)
        vs.extend([(base_x, on_yuz(base_x, base_z), base_z),
                   (mid_x - 0.075, on_yuz(mid_x - 0.075, mid_z), mid_z),
                   (tip_x, on_yuz(tip_x, tip_z), tip_z),
                   (mid_x + 0.075, on_yuz(mid_x + 0.075, mid_z), mid_z)])
        fs.append((j, j + 1, j + 2, j + 3))
    yaprak_mesh = bpy.data.meshes.new("cilek_canak_mesh")
    yaprak_mesh.from_pydata(vs, [], fs)
    yaprak_mesh.update()
    canak = bpy.data.objects.new("cilek_canak", yaprak_mesh)
    sc.collection.objects.link(canak)
    canak.parent = meyve
    canak.data.materials.append(yaprak_m)
    sap_m, _, sap_bsdf = malzeme("cilek_sap_yesili")
    sap_bsdf.inputs["Base Color"].default_value = hex_renk("#315b29")
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.052, depth=0.24)
    sap_cilek = bpy.context.object
    sap_cilek.name = "cilek_sap"
    sap_cilek.parent = meyve
    sap_cilek.location = (0, -0.22, R + 0.045)
    sap_cilek.data.materials.append(sap_m)

sap_izi = None
if KARPUZ or KIVI:
    iz_m, _, iz_bsdf = malzeme("kivi_sap_izi" if KIVI else "karpuz_ince_sap_izi")
    iz_bsdf.inputs["Base Color"].default_value = hex_renk("#5c432f" if KIVI else "#6b7350")
    iz_bsdf.inputs["Roughness"].default_value = 0.72
    bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=0.055 if KIVI else 0.075, depth=0.018)
    sap_izi = bpy.context.object
    sap_izi.name = "kivi_sap_izi" if KIVI else "karpuz_sap_izi"
    sap_izi.parent = meyve
    sap_izi.location = (A - 0.012, 0, 0)
    sap_izi.rotation_euler = (0, math.pi / 2, 0)
    sap_izi.data.materials.append(iz_m)

# ---------------------------------------------------------------- bicak
def bicak_kur():
    """Gercekci buyuk sef bicagi (kullanici 13 Kas): yerel +X boyunca agiz (y=0 kesici kenar), sirt y~0.62,
    uc x=2.9; kesitte kama (kenarda ince, sirtta 0.036). Celik topuk + perçinli koyu ahsap sap (-X)."""
    L_ = 3.4      # agiz boyu (buyuk sef bicagi)
    H_ = 0.78     # topuk yuksekligi
    N = 48
    xs = np.linspace(0, L_, N + 1)
    # kesici kenar: duz, son %35'te kavisle uca kalkar (belly)
    kenar = np.where(xs < L_ * 0.62, 0.0, ((xs - L_ * 0.62) / (L_ * 0.38)) ** 2.2 * H_ * 0.42)
    # sirt: duz, son %25'te uca iner
    sirt = np.where(xs < L_ * 0.72, H_, H_ - ((xs - L_ * 0.72) / (L_ * 0.28)) ** 1.4 * (H_ - H_ * 0.42 - 0.004))
    sirt = np.maximum(sirt, kenar + 0.004)
    kal_s = 0.018  # sirt yari kalinligi
    vs, fs = [], []
    # her istasyonda 4 nokta: kenar (0), egim baslangici (+/-), sirt (+/-)
    for x, ke, si in zip(xs, kenar, sirt):
        egim = ke + (si - ke) * 0.35
        vs += [(x, ke, 0.0), (x, egim, kal_s * 0.55), (x, si, kal_s), (x, si, -kal_s), (x, egim, -kal_s * 0.55)]
    n = 5
    for i in range(N):
        a, b = i * n, (i + 1) * n
        for j in range(n):
            j2 = (j + 1) % n
            fs.append((a + j, b + j, b + j2, a + j2))
    fs.append(tuple(range(n))[::-1])
    fs.append(tuple(range(N * n, N * n + n)))
    me = bpy.data.meshes.new("bicak")
    me.from_pydata(vs, [], fs)
    me.update()
    agiz = bpy.data.objects.new("bicak", me)
    sc.collection.objects.link(agiz)
    for p in me.polygons:
        p.use_smooth = False
    mb, ntb, bb = malzeme("celik")
    bb.inputs["Base Color"].default_value = hex_renk("#cfd3d8")
    bb.inputs["Metallic"].default_value = 0.9
    bb.inputs["Roughness"].default_value = 0.24
    # firca izi: x yonunde ince cizgili puruz
    tkb = ntb.nodes.new("ShaderNodeTexCoord")
    mpb = ntb.nodes.new("ShaderNodeMapping")
    mpb.inputs["Scale"].default_value = (2.0, 220.0, 1.0)
    ntb.links.new(tkb.outputs["Object"], mpb.inputs["Vector"])
    nzb = ntb.nodes.new("ShaderNodeTexNoise")
    nzb.inputs["Scale"].default_value = 3.0
    ntb.links.new(mpb.outputs["Vector"], nzb.inputs["Vector"])
    rb = ntb.nodes.new("ShaderNodeMapRange")
    rb.inputs["To Min"].default_value = 0.18
    rb.inputs["To Max"].default_value = 0.34
    ntb.links.new(nzb.outputs["Fac"], rb.inputs["Value"])
    ntb.links.new(rb.outputs["Result"], bb.inputs["Roughness"])
    me.materials.append(mb)
    # celik topuk (bolster)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.06, H_ * 0.5, 0))
    topuk = bpy.context.object
    topuk.name = "bicak_topuk"
    topuk.scale = (0.12, H_ * 0.92, 0.07)
    bv_ = topuk.modifiers.new("pah", "BEVEL"); bv_.width = 0.015; bv_.segments = 2
    topuk.data.materials.append(mb)
    topuk.parent = agiz
    # sap: koyu ahsap, hafif oval, 3 perçin
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.72, H_ * 0.5, 0))
    sap = bpy.context.object
    sap.name = "bicak_sap"
    sap.scale = (1.2, 0.27, 0.10)
    bv2 = sap.modifiers.new("pah", "BEVEL"); bv2.width = 0.045; bv2.segments = 4
    mh, nth, bh = malzeme("sap")
    nzh = nth.nodes.new("ShaderNodeTexWave")
    nzh.inputs["Scale"].default_value = 6.0
    nzh.inputs["Distortion"].default_value = 8.0
    rh = nth.nodes.new("ShaderNodeValToRGB")
    rh.color_ramp.elements[0].color = hex_renk("#2a1810")
    rh.color_ramp.elements[1].color = hex_renk("#5a3420")
    nth.links.new(nzh.outputs["Fac"], rh.inputs["Fac"])
    nth.links.new(rh.outputs["Color"], bh.inputs["Base Color"])
    bh.inputs["Roughness"].default_value = 0.45
    sap.data.materials.append(mh)
    sap.parent = agiz
    for px in (-0.33, -0.7, -1.07):
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.032, depth=0.115, location=(px, H_ * 0.5, 0),
                                            rotation=(0, 0, 0))
        pc = bpy.context.object
        pc.data.materials.append(mb)
        pc.parent = agiz
    return agiz


bicak = bicak_kur()

# eksene gore bicak yonleri (Euler XYZ, radyan)
YON = {
    "x": (math.radians(90), 0.0, math.radians(-105)),  # dikey dograma; 15 derece cevrik: agzin yuzu gorunur, sap sag-arkada
    "y": (math.radians(90), 0.0, math.radians(180)),   # agiz x boyunca, duzlem XZ, kameraya yuzu donuk
    "z": (0.0, 0.0, math.radians(180)),                # yatay dilim, agiz meyve boyunca -x'e bakar
}
DISARI = (7.5, -1.0, 4.5)  # kadraj disi (sag ust)


def bicak_konum(eks, konum, asagi, yuk):
    """eks kesim duzlemi, konum duzlem koordinati, asagi=True agiz tahtada; yuk=0..1 kalkis yuksekligi."""
    if eks == "x":
        # bicak 15 derece cevrik: meyvenin kameraya bakan on yuzunde (y=-B/2) agiz tam kesim duzleminde
        return (konum + (1.05 + B * 0.5) * math.tan(math.radians(15)), 1.05,
                TAHTA_UST + 0.004 if asagi else MERKEZ_Z + R + 0.15 + 0.2 * yuk)
    if eks == "y":
        return (1.25, konum, TAHTA_UST + 0.004 if asagi else MERKEZ_Z + R + 0.15 + 0.2 * yuk)
    # z: yatay dilim; sap ve topuk sagda meyvenin DISINDA kalir.
    # Bicak yerel +x yonunde, 180 derece donunce dunyada -x'e uzanir.
    # Kok noktasini sol uca goturmek sapi meyvenin icine sokuyordu.
    return ((A + 0.22) if asagi else (A + 3.6 + 0.2 * yuk), 0.0, MERKEZ_Z + konum)


def anahtar(ob, yol, t, deger, interp="LINEAR"):
    setattr(ob, yol, deger) if not isinstance(deger, tuple) else setattr(ob, yol, deger)
    ob.keyframe_insert(yol, frame=kare(t))


def egriler(action):
    """4.2 (action.fcurves) ve 4.4+/5.x (katmanli action) ile uyumlu."""
    try:
        return list(action.fcurves)
    except Exception:
        out = []
        for ly in action.layers:
            for st in ly.strips:
                for cb in st.channelbags:
                    out += list(cb.fcurves)
        return out


def sabit_interp(kimlik):
    ad = kimlik.animation_data
    if ad and ad.action:
        for fc in egriler(ad.action):
            for kp in fc.keyframe_points:
                kp.interpolation = "CONSTANT"


def dogrusal_interp(kimlik):
    ad = kimlik.animation_data
    if ad and ad.action:
        for fc in egriler(ad.action):
            for kp in fc.keyframe_points:
                kp.interpolation = "LINEAR"


# ---------------------------------------------------------------- kup yigini (tur sonu)
GORSEL_TAVANLAR = [200] * 6  # parca boyutu gercek kesim hucresi; 200/eksen ustu render cozunurlugunde piksel alti
TANECIK_ESIK = 60  # eksen basi hucre bunu gecerse kupler tanecik (nokta bulutu) olarak cizilir
DUSUS_SN = 0.5  # bir kupun yerine cokme suresi
SN_KAYMA = 1.0 / FPS  # GN Scene Time saniyesi = kare / fps; kare(t) = t*fps + 1


def profil_r(x):
    return profil_yaricap(x, M, FMAX)


def kup_nesnesi(tur, no):
    """REF-080: kesim hucresi kupleri; dis yuz kabuk, ic et/cekirdek. x supurmesi soldan saga ilerledikce
    her dilimin kupleri yerine coker (GN: Scene Time ile kup basina birakilma ani). Son yigin: alt yari
    tumsek, ust yari icine coker -> ustte kesit (krem et + kahve cekirdek)."""
    tavan = GORSEL_TAVANLAR[min(no, len(GORSEL_TAVANLAR) - 1)]
    cx, cy, cz = tur["cx"], tur["cy"], tur["cz"]
    gx, gy, gz = (min(c + 1, tavan) for c in (cx, cy, cz))
    xs = -A + (np.arange(gx) + 0.5) * (2 * A / gx)
    ys = -B + (np.arange(gy) + 0.5) * (2 * B / gy)
    zs = -R + (np.arange(gz) + 0.5) * (2 * R / gz)
    X, Y, Z = np.meshgrid(xs, ys, zs, indexing="ij")
    ic = icinde(X, Y, Z, M)
    idx = np.argwhere(ic)
    merk = np.stack([X[ic], Y[ic], Z[ic]], 1)
    k = len(merk)
    rng = np.random.default_rng(7 + no)
    hx, hy, hz = A / gx, B / gy, R / gz
    # Et/cekirdek rengi ve gercek dis kabuk maskesi ayni kaynak hucre konumundan gelir.
    if CILEK:
        pz = np.maximum(profil_r(merk[:, 2]), 1e-6)
        en = np.sqrt((merk[:, 0] / A) ** 2 + (merk[:, 1] / B) ** 2) / pz
        d = np.maximum(en, np.abs(merk[:, 2] / R))
    elif MANGO:
        kayma = 0.09 * np.sin(np.pi * merk[:, 0] / A)
        d = np.sqrt((merk[:, 1] / B) ** 2 + ((merk[:, 2] - kayma) / R) ** 2) / np.maximum(profil_r(merk[:, 0]) / R, 1e-6)
    else:
        d = np.sqrt(merk[:, 1] ** 2 + merk[:, 2] ** 2) / np.maximum(profil_r(merk[:, 0]), 1e-6)
    u = np.clip(d, 0, 1)[:, None]
    # bit 0:+X 1:-X 2:+Y 3:-Y 4:+Z 5:-Z.
    # Karpuzda kaba izgaranin eksik komsusu tek basina kabuk kaniti degildir:
    # hucre gercek dis halka yakininda veya fiziksel ucta olmalidir.
    p = np.pad(ic, 1)
    maske = np.zeros(k)
    for bit, (dx, dy, dz) in enumerate([(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]):
        dis = ~p[idx[:, 0] + 1 + dx, idx[:, 1] + 1 + dy, idx[:, 2] + 1 + dz]
        if KARPUZ:
            uc = (dx > 0) & (idx[:, 0] == gx - 1) | (dx < 0) & (idx[:, 0] == 0)
            dis &= (u[:, 0] >= 0.82) | uc
        maske += dis * (2 ** bit)
    if MANGO:
        ck = M["cekirdek"]
        ell = (((merk[:, 0] - ck["x"] * A) / ck["a"]) ** 2 +
               (merk[:, 1] / ck["b"]) ** 2 + ((merk[:, 2] - kayma) / ck["r"]) ** 2)
        renk = np.tile(np.array(hex_renk("#f5a729")[:3]), (k, 1))
        renk[(ell >= 1.0) & (ell < 1.35)] = np.array(hex_renk("#d98627")[:3])
        renk[ell < 1.0] = np.array(hex_renk("#ae7941")[:3])
        yaprak_hucre = mango_yaprak_icinde(merk[:, 0], merk[:, 1], merk[:, 2], M)
        renk[yaprak_hucre] = np.array(hex_renk("#3f782e")[:3])
        deri = np.tile(np.array(hex_renk("#dcae3c")[:3]), (k, 1))
        deri[merk[:, 1] > 0.13] = np.array(hex_renk("#72964a")[:3])
        deri[(merk[:, 1] < -0.08) & (merk[:, 0] > -0.75 * A)] = np.array(hex_renk("#cf512d")[:3])
        deri[yaprak_hucre] = np.array(hex_renk("#3f782e")[:3])
        # Dar ucta govdeye gomulu sap izi; ayri butun nesne degildir.
        sap_hucre = (merk[:, 0] < -0.79 * A) & (np.abs(merk[:, 1]) < 0.13) & (merk[:, 2] > 0.08)
        deri[sap_hucre & ~yaprak_hucre] = np.array(hex_renk("#765739")[:3])
    elif KIVI:
        durak = np.array([0.0, 0.25, 0.31, 0.47, 0.76, 0.91, 0.965, 0.985, 1.0])
        ton = np.array([hex_renk(h)[:3] for h in
            ("#f6f1d8", "#f2eed1", "#c8e68d", "#72c83e", "#48ab2f",
             "#8fc75c", "#d5d8a1", "#8a6747", "#5e422d")])
        renk = np.column_stack([np.interp(u[:, 0], durak, ton[:, c]) for c in range(3)])
        theta = np.arctan2(merk[:, 2], merk[:, 1])
        dalga = np.cos(40 * theta + 2 * merk[:, 0])
        isin = (dalga > 0.93) & (u[:, 0] > 0.30) & (u[:, 0] < 0.88)
        renk[isin] = 0.38 * renk[isin] + 0.62 * np.array(hex_renk("#e1ecab")[:3])
        tohum = (dalga > 0.45) & (u[:, 0] > 0.38) & (u[:, 0] < 0.53)
        renk[tohum] = np.array(hex_renk("#10150d")[:3])
    elif KARPUZ:
        # Ayni radyal duraklar asagidaki kesit shader'indaki rampayla eslesir.
        durak = np.array([0.0, 0.72, 0.78, 0.81, 0.90, 0.965, 0.985, 1.0])
        ton = np.array([hex_renk(h)[:3] for h in
            ("#e84244", "#d92730", "#ee7773", "#f8efdc", "#ebedd5", "#a2c891", "#1d4a2d", "#143c27")])
        # Iri hucrede merkezdeki rind ornegi tum kupu beyaza boyamasin;
        # hucrenin icerideki kirmizi et payini olcuyle hesaba kat.
        ic_renk_u = np.maximum(0.0, u[:, 0] - np.minimum(0.10, 0.5 * max(hy, hz) / R))
        renk = np.column_stack([np.interp(ic_renk_u, durak, ton[:, c]) for c in range(3)])
    elif CILEK:
        # Kesit rampasiyla ayni duraklar: beyaz oz, pembe et, kirmizi halka.
        oz = np.array(hex_renk("#fff1e5")[:3])
        pembe = np.array(hex_renk("#f7a7ab")[:3])
        kirmizi = np.array(hex_renk("#d52b36")[:3])
        koyu = np.array(hex_renk("#a81722")[:3])
        renk = np.where(u < 0.42, oz * (1 - u / 0.42) + pembe * (u / 0.42),
                        np.where(u < 0.82, pembe * (1 - (u - 0.42) / 0.40) + kirmizi * ((u - 0.42) / 0.40),
                                 kirmizi * (1 - (u - 0.82) / 0.18) + koyu * ((u - 0.82) / 0.18)))
    else:
        ck = M["cekirdek"]
        cek_r = ck["r"] * R
        cd = np.linalg.norm(merk - np.array([ck["x"] * A, 0, 0]), axis=1)
        krem = np.array(hex_renk("#f1e9b8")[:3])
        sari = np.array(hex_renk("#e3e08e")[:3])
        yesil = np.array(hex_renk("#a8cc5c")[:3])
        renk = np.where(u < 0.6, krem * (1 - u / 0.6) + sari * (u / 0.6), sari * (1 - (u - 0.6) / 0.4) + yesil * ((u - 0.6) / 0.4))
        renk[cd <= cek_r] = np.array(hex_renk("#b98a52")[:3])
        renk[(cd <= cek_r) & (cd > cek_r * 0.86)] = np.array(hex_renk("#4a2412")[:3])
    renk *= rng.uniform(0.96 if KARPUZ else 0.93, 1.04 if KARPUZ else 1.05, (k, 1))
    # birakilma ani: x kesimi hucrenin sag kenarini gectiginde (soldan saga)
    xk = [(k_[4], k_[2]) for k_ in tur["kesimler"] if k_[1] == "x"]
    T = np.array([t for t, _ in xk])
    P = np.array([c for _, c in xk])
    sag = -A + (idx[:, 0] + 1) * (2 * A / gx)
    j = np.searchsorted(P, sag - 1e-6)
    tr = np.where(j < len(T), T[np.minimum(j, len(T) - 1)], T[-1]) + 0.005 + rng.uniform(0, 0.05, k)
    # REF-080 dokulme: dilim kesilince kupler hizla duser, donerek akar, tahtada daha once dusenlerin ustune
    # yigilir (yigin = biriktirme + dogal egim; onceden hesaplanmis duzgun sekil yok)
    zc = MERKEZ_Z
    zb = TAHTA_UST
    p0 = merk.copy()
    p0[:, 2] += zc
    hucre = 2 * max(hx, hy) * 0.98
    h = 2 * hz * 0.92
    yuks = np.maximum(p0[:, 2] - zb, 0)
    # yatay savrulma: yukseklikle artar, sola (kesilmis tarafa) ve kesitten disari egilimli
    yon_y = np.sign(merk[:, 1] + 1e-9)
    dx = -np.abs(rng.normal(0.10, 0.10, k)) * yuks + rng.normal(0, 0.08, k) * yuks
    dy = yon_y * np.abs(rng.normal(0.06, 0.08, k)) * yuks + rng.normal(0, 0.06, k) * yuks
    hx_ = p0[:, 0] + dx
    hy_ = p0[:, 1] + dy
    # dogal yigin: kum yigini gibi devrilme (yukseklik alani, ~35 derece dogal egim) + duzene sokulmamis yerlesim
    x0, y0 = -1.75, -1.25
    nxm, nym = int(3.5 / hucre) + 1, int(2.3 / hucre) + 1
    ix = np.clip(((hx_ - x0) / hucre).astype(np.int64), 0, nxm - 1)
    iy = np.clip(((hy_ - y0) / hucre).astype(np.int64), 0, nym - 1)
    H = np.zeros((nxm, nym))
    np.add.at(H, (ix, iy), 1.0)
    lim = 0.7 * hucre / h  # komsu farki bu kadar kupu gecince devrilir (tan 35)
    for _ in range(600):
        degisti = False
        for ax_, sh in ((0, 1), (0, -1), (1, 1), (1, -1)):
            fark_ = H - np.roll(H, sh, axis=ax_)
            asim = np.maximum(fark_ - lim, 0) / 5.0
            if ax_ == 0:
                asim[0 if sh == -1 else -1, :] = 0
            else:
                asim[:, 0 if sh == -1 else -1] = 0
            if asim.max() > 1e-3:
                degisti = True
            H -= asim
            H += np.roll(asim, -sh, axis=ax_)
        if not degisti:
            break
    # yuvalara (cell, katman) yerlestirme: toplam k
    sayi = np.floor(H).astype(np.int64)
    eksik = k - int(sayi.sum())
    if eksik > 0:
        kesir = (H - np.floor(H)).ravel()
        ek = np.argsort(-kesir)[:eksik]
        sayi.ravel()[ek] += 1
    elif eksik < 0:
        dolu = np.argwhere(sayi.ravel() > 0).ravel()
        cik = rng.choice(dolu, -eksik, replace=True)
        np.subtract.at(sayi.ravel(), cik, 1)
        sayi = np.maximum(sayi, 0)
    ci, cj = np.nonzero(sayi)
    adet = sayi[ci, cj]
    slot_i = np.repeat(ci, adet)
    slot_j = np.repeat(cj, adet)
    slot_k = np.concatenate([np.arange(n_) for n_ in adet]) if len(adet) else np.zeros(0, np.int64)
    n_s = len(slot_i)
    if n_s < k:  # yuvarlama guvencesi
        slot_i = np.r_[slot_i, np.full(k - n_s, slot_i[-1])]
        slot_j = np.r_[slot_j, np.full(k - n_s, slot_j[-1])]
        slot_k = np.r_[slot_k, np.arange(k - n_s) + slot_k.max() + 1]
    slot_i, slot_j, slot_k = slot_i[:k], slot_j[:k], slot_k[:k]
    # esleme: kupler ve yuvalar x seridine, serit icinde y'ye, sonra yukseklige gore siralanir
    serit_adedi = max(1, int(np.sqrt(k) / 2))
    def _sira(xv, yv, zv):
        o = np.argsort(xv, kind="stable")
        serit = np.empty(len(xv), np.int64)
        serit[o] = (np.arange(len(xv)) * serit_adedi) // len(xv)
        return np.lexsort((zv, yv, serit))
    kup_sira = _sira(hx_, hy_, p0[:, 2])
    slot_sira = _sira(slot_i + rng.uniform(0, 1, k), slot_j + rng.uniform(0, 1, k), slot_k.astype(float))
    son = np.empty_like(p0)
    si, sj, sk = slot_i[slot_sira], slot_j[slot_sira], slot_k[slot_sira]
    son[kup_sira, 0] = x0 + (si + rng.uniform(0, 1, k)) * hucre
    son[kup_sira, 1] = y0 + (sj + rng.uniform(0, 1, k)) * hucre
    son[kup_sira, 2] = zb + h / 2 + sk * h * 0.92 + rng.uniform(-0.25, 0.25, k) * h
    # dusus suresi: yer cekimi (hizli), en az 0.12 sn
    G_ = 30.0
    dz = np.maximum(p0[:, 2] - son[:, 2], 0.0)
    sure = np.maximum(np.sqrt(2 * dz / G_), 0.12)
    # donus: dusus boyunca serbest dondurme, kupler egik iner
    rv = rng.normal(0, 1.0, (k, 3)) * np.array([1.6, 1.6, 2.2])
    me = bpy.data.meshes.new(f"kup_{no}")
    me.vertices.add(k)
    me.vertices.foreach_set("co", p0.ravel().astype(np.float32))
    me.update()
    for ad_, tip, veri in (("son", "FLOAT_VECTOR", son), ("rv", "FLOAT_VECTOR", rv)):
        at_ = me.attributes.new(ad_, tip, "POINT")
        at_.data.foreach_set("vector", veri.ravel().astype(np.float32))
    for ad_, veri in (("tr", tr + SN_KAYMA), ("maske", maske), ("sure", sure)):
        at_ = me.attributes.new(ad_, "FLOAT", "POINT")
        at_.data.foreach_set("value", veri.astype(np.float32))
    at_ = me.attributes.new("renk", "FLOAT_COLOR", "POINT")
    at_.data.foreach_set("color", np.hstack([renk, np.ones((k, 1))]).ravel().astype(np.float32))
    if MANGO:
        at_ = me.attributes.new("deri", "FLOAT_COLOR", "POINT")
        at_.data.foreach_set("color", np.hstack([deri, np.ones((k, 1))]).ravel().astype(np.float32))
    if KARPUZ or KIVI:
        at_ = me.attributes.new("kaynak", "FLOAT_VECTOR", "POINT")
        at_.data.foreach_set("vector", merk.ravel().astype(np.float32))
    ob = bpy.data.objects.new(f"kup_{no}", me)
    sc.collection.objects.link(ob)
    try:
        ob.cycles.use_motion_blur = False
    except Exception:
        pass

    # malzeme: yuz normali (nesne uzayi) + maske bitinden kabuk / et
    mk, ntk, bk = malzeme(f"kup_m_{no}")
    a_r = ntk.nodes.new("ShaderNodeAttribute"); a_r.attribute_type = "INSTANCER"; a_r.attribute_name = "renk"
    a_m = ntk.nodes.new("ShaderNodeAttribute"); a_m.attribute_type = "INSTANCER"; a_m.attribute_name = "maske"
    tkk = ntk.nodes.new("ShaderNodeTexCoord")
    ay = ntk.nodes.new("ShaderNodeSeparateXYZ")
    baglan(ntk, tkk.outputs["Normal"], ay.inputs[0])
    nx, ny, nz_ = ay.outputs[0], ay.outputs[1], ay.outputs[2]
    kk = matematik(ntk, "LESS_THAN", nx, None, deger_b=-0.5)
    kk = matematik(ntk, "ADD", kk, matematik(ntk, "MULTIPLY", matematik(ntk, "GREATER_THAN", ny, None, deger_b=0.5), None, deger_b=2))
    kk = matematik(ntk, "ADD", kk, matematik(ntk, "MULTIPLY", matematik(ntk, "LESS_THAN", ny, None, deger_b=-0.5), None, deger_b=3))
    kk = matematik(ntk, "ADD", kk, matematik(ntk, "MULTIPLY", matematik(ntk, "GREATER_THAN", nz_, None, deger_b=0.5), None, deger_b=4))
    kk = matematik(ntk, "ADD", kk, matematik(ntk, "MULTIPLY", matematik(ntk, "LESS_THAN", nz_, None, deger_b=-0.5), None, deger_b=5))
    iki = matematik(ntk, "POWER", None, kk, deger_a=2.0)
    bitv = matematik(ntk, "MODULO", matematik(ntk, "FLOOR", matematik(ntk, "DIVIDE", a_m.outputs["Fac"], iki)), None, deger_b=2.0)
    karis = ntk.nodes.new("ShaderNodeMix")
    karis.data_type = "RGBA"
    baglan(ntk, bitv, karis.inputs["Factor"])
    baglan(ntk, a_r.outputs["Color"], karis.inputs[6])
    karis.inputs[7].default_value = hex_renk("#b71f29" if CILEK else "#21361a")
    if MANGO:
        a_deri = ntk.nodes.new("ShaderNodeAttribute")
        a_deri.attribute_type = "INSTANCER"; a_deri.attribute_name = "deri"
        baglan(ntk, a_deri.outputs["Color"], karis.inputs[7])
    if CILEK:
        # Sadece maskelenmis dis yuz; kesik et yuzunde aken bulunmaz.
        geometri = ntk.nodes.new("ShaderNodeNewGeometry")
        cilek_aken(ntk, geometri.outputs["Position"], karis.outputs[2], bk, dis_maske=bitv)
    elif KARPUZ:
        # Generated kubun yerel 0..1 koordinati, kaynak merkez ve hucre boyutu
        # ile kesilmeden onceki tam 3B konuma geri cevrilir. Rind renkleri
        # boylece ilk turun iri kuplerinde bile tek renkli etiket olmaz.
        kaynak = ntk.nodes.new("ShaderNodeAttribute")
        kaynak.attribute_type = "INSTANCER"; kaynak.attribute_name = "kaynak"
        uv = ntk.nodes.new("ShaderNodeSeparateXYZ")
        baglan(ntk, tkk.outputs["Generated"], uv.inputs[0])
        src = ntk.nodes.new("ShaderNodeSeparateXYZ")
        baglan(ntk, kaynak.outputs["Vector"], src.inputs[0])
        def konum(eks, yarim):
            ofset = matematik(ntk, "MULTIPLY", matematik(ntk, "SUBTRACT", uv.outputs[eks], None, deger_b=0.5),
                             None, deger_b=2 * yarim * 0.94)
            return matematik(ntk, "ADD", src.outputs[eks], ofset)
        ox, oy, oz = konum(0, hx), konum(1, hy), konum(2, hz)
        rr_ = matematik(ntk, "MULTIPLY", matematik(ntk, "SQRT",
            matematik(ntk, "MAXIMUM", matematik(ntk, "SUBTRACT", None,
                matematik(ntk, "MULTIPLY", matematik(ntk, "DIVIDE", ox, None, deger_b=A),
                                          matematik(ntk, "DIVIDE", ox, None, deger_b=A)), deger_a=1.0),
                None, deger_b=1e-8)), None, deger_b=R)
        radyal = matematik(ntk, "SQRT", matematik(ntk, "ADD",
            matematik(ntk, "MULTIPLY", oy, oy), matematik(ntk, "MULTIPLY", oz, oz)))
        u_src = matematik(ntk, "DIVIDE", radyal, rr_)
        ramp = ntk.nodes.new("ShaderNodeValToRGB")
        ramp.color_ramp.elements[0].color = hex_renk("#e84244")
        ramp.color_ramp.elements[1].position = 1.0
        ramp.color_ramp.elements[1].color = hex_renk("#143c27")
        for pos, renk_ in ((0.72, "#d92730"), (0.78, "#ee7773"), (0.81, "#f8efdc"),
                           (0.90, "#ebedd5"), (0.965, "#a2c891"), (0.985, "#1d4a2d")):
            el = ramp.color_ramp.elements.new(pos); el.color = hex_renk(renk_)
        baglan(ntk, u_src, ramp.inputs["Fac"])
        kaynak_vec = ntk.nodes.new("ShaderNodeCombineXYZ")
        for i, val in enumerate((ox, oy, oz)):
            baglan(ntk, val, kaynak_vec.inputs[i])
        serit_renk = karpuz_serit(ntk, kaynak_vec.outputs[0])
        deri = matematik(ntk, "MULTIPLY", bitv,
            matematik(ntk, "GREATER_THAN", u_src, None, deger_b=0.985))
        rind = ntk.nodes.new("ShaderNodeMix"); rind.data_type = "RGBA"
        baglan(ntk, deri, rind.inputs["Factor"])
        baglan(ntk, ramp.outputs["Color"], rind.inputs[6])
        baglan(ntk, serit_renk, rind.inputs[7])
        # Ayni sekiz sonlu tohum hacmi; yalniz kirmizi et ve X kesim yuzleri.
        x_yuzu = matematik(ntk, "GREATER_THAN", matematik(ntk, "ABSOLUTE", nx), None, deger_b=0.5)
        et_tohum = matematik(ntk, "MULTIPLY", karpuz_cekirdek_maske(ntk, ox, oy,
            matematik(ntk, "ADD", oz, None, deger_b=MERKEZ_Z)),
            matematik(ntk, "MULTIPLY", x_yuzu,
                matematik(ntk, "LESS_THAN", u_src, None, deger_b=0.72)))
        cek = ntk.nodes.new("ShaderNodeMix"); cek.data_type = "RGBA"
        baglan(ntk, et_tohum, cek.inputs["Factor"])
        baglan(ntk, rind.outputs[2], cek.inputs[6])
        cek.inputs[7].default_value = hex_renk("#261b18")
        baglan(ntk, cek.outputs[2], bk.inputs["Base Color"])
    elif KIVI:
        kaynak = ntk.nodes.new("ShaderNodeAttribute")
        kaynak.attribute_type = "INSTANCER"; kaynak.attribute_name = "kaynak"
        uv = ntk.nodes.new("ShaderNodeSeparateXYZ")
        baglan(ntk, tkk.outputs["Generated"], uv.inputs[0])
        src = ntk.nodes.new("ShaderNodeSeparateXYZ")
        baglan(ntk, kaynak.outputs["Vector"], src.inputs[0])
        def konum_kivi(eks, yarim):
            ofset = matematik(ntk, "MULTIPLY", matematik(ntk, "SUBTRACT", uv.outputs[eks], None, deger_b=0.5),
                             None, deger_b=2 * yarim * 0.94)
            return matematik(ntk, "ADD", src.outputs[eks], ofset)
        ox, oy, oz = konum_kivi(0, hx), konum_kivi(1, hy), konum_kivi(2, hz)
        xn_ = matematik(ntk, "DIVIDE", ox, None, deger_b=A)
        taban = matematik(ntk, "MAXIMUM", matematik(ntk, "SUBTRACT", None,
            matematik(ntk, "MULTIPLY", xn_, xn_), deger_a=1.0), None, deger_b=1e-8)
        rr_ = matematik(ntk, "MULTIPLY", matematik(ntk, "POWER", taban, None, deger_b=0.38),
                       None, deger_b=R)
        x_yuzu = matematik(ntk, "GREATER_THAN", matematik(ntk, "ABSOLUTE", nx), None, deger_b=0.5)
        ic_renk, u_kivi = kivi_ic_renk(ntk, ox, oy, oz, rr_, x_yuzu)
        # Kahve ve mat tuy dokusu sadece dis kabuk yuzunde kalir.
        deri = matematik(ntk, "MULTIPLY", bitv,
            matematik(ntk, "GREATER_THAN", u_kivi, None, deger_b=0.975))
        rmp_k = ntk.nodes.new("ShaderNodeTexNoise")
        rmp_k.inputs["Scale"].default_value = 65
        vec_k = ntk.nodes.new("ShaderNodeCombineXYZ")
        for i, val in enumerate((ox, oy, oz)):
            baglan(ntk, val, vec_k.inputs[i])
        baglan(ntk, vec_k.outputs[0], rmp_k.inputs["Vector"])
        kabuk_k = ntk.nodes.new("ShaderNodeValToRGB")
        kabuk_k.color_ramp.elements[0].color = hex_renk("#57412e")
        kabuk_k.color_ramp.elements[1].color = hex_renk("#a1845a")
        baglan(ntk, rmp_k.outputs["Fac"], kabuk_k.inputs["Fac"])
        son_k = ntk.nodes.new("ShaderNodeMix"); son_k.data_type = "RGBA"
        baglan(ntk, deri, son_k.inputs["Factor"])
        baglan(ntk, ic_renk, son_k.inputs[6])
        baglan(ntk, kabuk_k.outputs["Color"], son_k.inputs[7])
        baglan(ntk, son_k.outputs[2], bk.inputs["Base Color"])
    else:
        baglan(ntk, karis.outputs[2], bk.inputs["Base Color"])
    bk.inputs["Roughness"].default_value = 0.72 if KIVI else 0.5

    mt, ntt, bt = malzeme(f"tanecik_m_{no}")
    t_r = ntt.nodes.new("ShaderNodeAttribute"); t_r.attribute_type = "GEOMETRY"; t_r.attribute_name = "renk"
    t_m = ntt.nodes.new("ShaderNodeAttribute"); t_m.attribute_type = "GEOMETRY"; t_m.attribute_name = "maske"
    t_k = ntt.nodes.new("ShaderNodeMix"); t_k.data_type = "RGBA"
    baglan(ntt, matematik(ntt, "GREATER_THAN", t_m.outputs["Fac"], None, deger_b=0.5), t_k.inputs["Factor"])
    baglan(ntt, t_r.outputs["Color"], t_k.inputs[6])
    t_k.inputs[7].default_value = hex_renk("#60452f" if KIVI else ("#143c27" if KARPUZ else ("#b71f29" if CILEK else "#21361a")))
    baglan(ntt, t_k.outputs[2], bt.inputs["Base Color"])
    bt.inputs["Roughness"].default_value = 0.55

    # geometri dugumleri: zaman -> konum, kup kopyalari
    ng = bpy.data.node_groups.new(f"kupGN_{no}", "GeometryNodeTree")
    ng.interface.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    N = ng.nodes
    L = ng.links
    gi = N.new("NodeGroupInput")
    go = N.new("NodeGroupOutput")

    def nattr(ad_, tip):
        n_ = N.new("GeometryNodeInputNamedAttribute")
        n_.data_type = tip
        n_.inputs["Name"].default_value = ad_
        return n_.outputs["Attribute"]

    def gm(islem, a_, b_=None, db=None):
        n_ = N.new("ShaderNodeMath")
        n_.operation = islem
        L.new(a_, n_.inputs[0])
        if b_ is not None:
            L.new(b_, n_.inputs[1])
        elif db is not None:
            n_.inputs[1].default_value = db
        return n_

    zaman = N.new("GeometryNodeInputSceneTime")
    e = gm("SUBTRACT", zaman.outputs["Seconds"], nattr("tr", "FLOAT"))
    e = gm("DIVIDE", e.outputs[0], nattr("sure", "FLOAT"))
    e.use_clamp = True
    e2 = gm("MULTIPLY", e.outputs[0], e.outputs[0])
    poz = N.new("GeometryNodeInputPosition")
    fark = N.new("ShaderNodeVectorMath"); fark.operation = "SUBTRACT"
    L.new(nattr("son", "FLOAT_VECTOR"), fark.inputs[0]); L.new(poz.outputs[0], fark.inputs[1])
    olc = N.new("ShaderNodeVectorMath"); olc.operation = "SCALE"
    L.new(fark.outputs[0], olc.inputs[0]); L.new(e2.outputs[0], olc.inputs["Scale"])
    topla = N.new("ShaderNodeVectorMath"); topla.operation = "ADD"
    L.new(poz.outputs[0], topla.inputs[0]); L.new(olc.outputs[0], topla.inputs[1])
    once = gm("LESS_THAN", zaman.outputs["Seconds"], nattr("tr", "FLOAT"))
    sil = N.new("GeometryNodeDeleteGeometry")
    sil.domain = "POINT"
    L.new(gi.outputs[0], sil.inputs["Geometry"])
    L.new(once.outputs[0], sil.inputs["Selection"])
    sp = N.new("GeometryNodeSetPosition")
    L.new(sil.outputs["Geometry"], sp.inputs["Geometry"])
    L.new(topla.outputs[0], sp.inputs["Position"])
    if gx <= TANECIK_ESIK:
        kup = N.new("GeometryNodeMeshCube")
        kup.inputs["Size"].default_value = (2 * hx * 0.94, 2 * hy * 0.94, 2 * hz * 0.94)
        sm = N.new("GeometryNodeSetMaterial")
        sm.inputs["Material"].default_value = mk
        L.new(kup.outputs["Mesh"], sm.inputs["Geometry"])
        iop = N.new("GeometryNodeInstanceOnPoints")
        L.new(sp.outputs["Geometry"], iop.inputs["Points"])
        L.new(sm.outputs["Geometry"], iop.inputs["Instance"])
        rot = N.new("ShaderNodeVectorMath"); rot.operation = "SCALE"
        L.new(nattr("rv", "FLOAT_VECTOR"), rot.inputs[0]); L.new(e.outputs[0], rot.inputs["Scale"])
        try:
            e2r = N.new("FunctionNodeEulerToRotation")
            L.new(rot.outputs[0], e2r.inputs[0])
            L.new(e2r.outputs[0], iop.inputs["Rotation"])
        except Exception:
            L.new(rot.outputs[0], iop.inputs["Rotation"])
        L.new(iop.outputs["Instances"], go.inputs[0])
    else:
        m2p = N.new("GeometryNodeMeshToPoints")
        m2p.inputs["Radius"].default_value = max(hx, hy, hz) * 0.95
        L.new(sp.outputs["Geometry"], m2p.inputs["Mesh"])
        sm = N.new("GeometryNodeSetMaterial")
        sm.inputs["Material"].default_value = mt
        L.new(m2p.outputs["Points"], sm.inputs["Geometry"])
        L.new(sm.outputs["Geometry"], go.inputs[0])
    md = ob.modifiers.new("kupler", "NODES")
    md.node_group = ng
    print(f"tur {no}: {k} gorsel kup ({gx}x{gy}x{gz}), supurme {T[0]:.2f}-{T[-1]:.2f} sn", flush=True)
    return ob, float(T[0])


# ---------------------------------------------------------------- animasyon
bicak.rotation_mode = "XYZ"
meyve_mat = meyve.data.materials[0]
nt_m = meyve_mat.node_tree


def deger_anahtar(ad, t, deger):
    n = nt_m.nodes[ad]
    n.outputs[0].default_value = deger
    n.outputs[0].keyframe_insert("default_value", frame=kare(t))
    if KIVI and ad == "kes_x":
        n_tuy = kivi_tuy_nt.nodes["kes_x"]
        n_tuy.outputs[0].default_value = deger
        n_tuy.outputs[0].keyframe_insert("default_value", frame=kare(t))
    if MANGO and ad == "kes_x":
        n_leaf = mango_yaprak_nt.nodes["kes_x"]
        n_leaf.outputs[0].default_value = deger
        n_leaf.outputs[0].keyframe_insert("default_value", frame=kare(t))


# yeni meyve dusus anahtarlari: (sn, yukseklik, xy olcek, z olcek) - dusus, ezilme, sekme, oturma
rng_b = np.random.default_rng(21)
DUSUS_ANAHTAR = [(0.0, 3.0, 0.94, 1.10), (0.30, 0.0, 1.12, 0.84), (0.42, 0.20, 0.97, 1.05),
                 (0.53, 0.0, 1.04, 0.95), (0.62, 0.0, 1.0, 1.0)]
# baslangic
bicak.location = DISARI
bicak.rotation_euler = YON["x"]
bicak.keyframe_insert("location", frame=0)
bicak.keyframe_insert("rotation_euler", frame=0)

for no, tur in enumerate(PLAN["turlar"]):
    bas, kb, ks, son = tur["bas"], tur["kes_bas"], tur["kes_son"], tur["son"]
    # meyve: belirir (olcek), sonda gizlenir
    meyve.hide_render = False
    meyve.keyframe_insert("hide_render", frame=kare(bas))
    if mango_yaprak is not None:
        mango_yaprak.hide_render = False
        mango_yaprak.keyframe_insert("hide_render", frame=kare(bas))
    if canak is not None:
        for parca in (canak, sap_cilek):
            parca.hide_render = False
            parca.keyframe_insert("hide_render", frame=kare(bas))
    if sap_izi is not None:
        sap_izi.hide_render = False
        sap_izi.keyframe_insert("hide_render", frame=kare(bas))
    if kivi_tuy is not None:
        kivi_tuy.hide_render = False
        kivi_tuy.keyframe_insert("hide_render", frame=kare(bas))
    for t_, dz_, sxy, sz in DUSUS_ANAHTAR:
        meyve.scale = (sxy, sxy, sz)
        meyve.location = (0, 0, MERKEZ_Z + dz_ - R * (1 - sz))  # ezilmede alt yuzey tahtada kalir
        meyve.keyframe_insert("scale", frame=kare(bas + t_))
        meyve.keyframe_insert("location", frame=kare(bas + t_))
    meyve.keyframe_insert("scale", frame=kare(ks))  # tur boyunca sabit
    meyve.keyframe_insert("location", frame=kare(ks))
    meyve.hide_render = True
    meyve.keyframe_insert("hide_render", frame=kare(ks + 0.02))
    if mango_yaprak is not None:
        mango_yaprak.hide_render = True
        mango_yaprak.keyframe_insert("hide_render", frame=kare(ks + 0.02))
    if canak is not None:
        for parca in (canak, sap_cilek):
            parca.hide_render = True
            parca.keyframe_insert("hide_render", frame=kare(ks + 0.02))
    if sap_izi is not None:
        sap_izi.hide_render = True
        sap_izi.keyframe_insert("hide_render", frame=kare(ks + 0.02))
    if kivi_tuy is not None:
        kivi_tuy.hide_render = True
        kivi_tuy.keyframe_insert("hide_render", frame=kare(ks + 0.02))
    bicak.location = DISARI
    bicak.keyframe_insert("location", frame=kare(kb - 0.3))
    # cizgi degerleri sifirla
    for eks, c in (("x", tur["cx"]), ("y", tur["cy"]), ("z", tur["cz"])):
        deger_anahtar(f"n_{eks}", bas, c + 1.0)
        deger_anahtar(f"d_{eks}", bas, 0.0)
    deger_anahtar("kes_x", bas, -10.0)
    # bicak: her gorunur vurus TAM: ustte -> tek hamlede tahtaya -> kisa durus -> ustte (ara durum yok)
    vl = tur["vuruslar"]
    onceki_eks = None
    # her vurus kesimin GERCEK yonunde (REF-080): z = sagdan yatay dilim, y = yukaridan boyuna, x = dilim dograma.
    # Kare tabanli: vurus karesinde agiz tahtada (z: meyvenin icinden gecmis), bir sonraki karede yukarida.
    for i, (t, eks, konum, adet) in enumerate(vl):
        f = round(t * FPS)
        f_once = round(vl[i - 1][0] * FPS) if i > 0 else round((kb - 0.3) * FPS)
        f_sonra = round(vl[i + 1][0] * FPS) if i + 1 < len(vl) else f + 12
        inis = 1  # ustten tahtaya tek karede: ara karede bicak meyvenin yarisinda gorunmez (net vurus)
        kalkis = 1
        tut = 1 if (f - f_once >= 6 and f_sonra - f >= 6) else 0
        if eks != onceki_eks:
            bicak.rotation_euler = YON[eks]
            bicak.keyframe_insert("rotation_euler", frame=f - inis + 1)
            onceki_eks = eks
        bicak.location = bicak_konum(eks, konum, False, 1.0)
        bicak.keyframe_insert("location", frame=f - inis + 1)
        bicak.location = bicak_konum(eks, konum, True, 0)
        bicak.keyframe_insert("location", frame=f + 1)
        if tut:
            bicak.keyframe_insert("location", frame=f + 2)
        bicak.location = bicak_konum(eks, konum, False, 1.0)
        bicak.keyframe_insert("location", frame=f + 1 + tut + kalkis)
        if eks == "x":  # kesim yuzu yalniz dilim kesiminde ilerler (iz asamasinda meyve butun)
            deger_anahtar("kes_x", t, konum)
    bicak.location = DISARI
    bicak.keyframe_insert("location", frame=kare(ks + 0.12))
    # kup yigini: supurme basinda gorunur (meyvenin icinde), dilim dilim coker
    kup, t_sup = kup_nesnesi(tur, no)
    kup.hide_render = True
    kup.keyframe_insert("hide_render", frame=0)
    kup.hide_render = False
    kup.keyframe_insert("hide_render", frame=kare(t_sup - 0.05))
    kup.hide_render = True
    kup.keyframe_insert("hide_render", frame=kare(son))
    sabit_interp(kup)

# interpolasyon: bicak konumu dogrusal, yon sabit; cizgi degerleri sabit; gorunurluk sabit
ad = bicak.animation_data.action
for fc in egriler(ad):
    for kp in fc.keyframe_points:
        kp.interpolation = "CONSTANT" if fc.data_path == "rotation_euler" else "LINEAR"
sabit_interp(nt_m)
if mango_yaprak_nt is not None:
    sabit_interp(mango_yaprak_nt)
    sabit_interp(mango_yaprak)
if kivi_tuy_nt is not None:
    sabit_interp(kivi_tuy_nt)
ad = meyve.animation_data.action
for fc in egriler(ad):
    for kp in fc.keyframe_points:
        kp.interpolation = "CONSTANT" if fc.data_path == "hide_render" else "BEZIER"

# ---------------------------------------------------------------- kesit yuzu (kalan meyve)
# Cilek kesiti YZ dikdortgeninde shader ile gercek profil sinirina kirpilir.
# Avokado eski dairesel kesitini korur.
_n = 96
_vs = ([(0.0, -B, -R), (0.0, B, -R), (0.0, B, R), (0.0, -B, R)] if CILEK else
       [(0.0, math.cos(2 * math.pi * i / _n), math.sin(2 * math.pi * i / _n)) for i in range(_n)])
_me = bpy.data.meshes.new("kesit")
_me.from_pydata(_vs, [], [list(range(len(_vs)))[::-1]])
_me.update()
kesit = bpy.data.objects.new("kesit", _me)
sc.collection.objects.link(kesit)
kesit.location = (0, 0, MERKEZ_Z)
# Kesit nesnenin GERCEK YZ kesim duzlemindedir. Kameraya cevrilen veya one
# tasinan gosterim diski, kup dokulurken havada duran sahte yuvarlak yuz olusturur.
kesit.rotation_euler = (0, 0, 0)
mk_, ntk_, bk_ = malzeme("kesit_m")
gp = ntk_.nodes.new("ShaderNodeNewGeometry")
ay_ = ntk_.nodes.new("ShaderNodeSeparateXYZ")
if KARPUZ or KIVI or MANGO:
    kesit_koordinat = ntk_.nodes.new("ShaderNodeTexCoord")
    baglan(ntk_, kesit_koordinat.outputs["Object"], ay_.inputs[0])
else:
    baglan(ntk_, gp.outputs["Position"], ay_.inputs[0])
v_r = ntk_.nodes.new("ShaderNodeValue"); v_r.name = "kesit_r"; v_r.outputs[0].default_value = 1.0
v_x = ntk_.nodes.new("ShaderNodeValue"); v_x.name = "kesit_x"; v_x.outputs[0].default_value = 0.0
dy = (matematik(ntk_, "MULTIPLY", ay_.outputs[1], v_r.outputs[0]) if (KARPUZ or KIVI) else
      matematik(ntk_, "MULTIPLY", ay_.outputs[1],
          matematik(ntk_, "MULTIPLY", v_r.outputs[0], None, deger_b=B / R)) if MANGO else ay_.outputs[1])
dz = (matematik(ntk_, "MULTIPLY", ay_.outputs[2], v_r.outputs[0]) if (KARPUZ or KIVI or MANGO) else
      matematik(ntk_, "SUBTRACT", ay_.outputs[2], None, deger_b=MERKEZ_Z))
rad = matematik(ntk_, "SQRT", matematik(ntk_, "ADD", matematik(ntk_, "MULTIPLY", dy, dy), matematik(ntk_, "MULTIPLY", dz, dz)))
if CILEK:
    # plan.py: p(z) = s^.62 * (1-s)^.25 / FMAX.
    s_ = matematik(ntk_, "MULTIPLY", dz, None, deger_b=0.5 / R)
    s_ = matematik(ntk_, "ADD", s_, None, deger_b=0.5)
    s_ = matematik(ntk_, "MINIMUM", matematik(ntk_, "MAXIMUM", s_, None, deger_b=0.0), None, deger_b=1.0)
    p_ = matematik(ntk_, "MULTIPLY",
                   matematik(ntk_, "POWER", s_, None, deger_b=0.62),
                   matematik(ntk_, "POWER", matematik(ntk_, "SUBTRACT", None, s_, deger_a=1.0), None, deger_b=0.25))
    p_ = matematik(ntk_, "DIVIDE", p_, None, deger_b=FMAX)
    nx_ = matematik(ntk_, "DIVIDE", v_x.outputs[0], None, deger_b=A)
    ny_ = matematik(ntk_, "DIVIDE", dy, None, deger_b=B)
    en_ = matematik(ntk_, "SQRT", matematik(ntk_, "ADD", matematik(ntk_, "MULTIPLY", nx_, nx_), matematik(ntk_, "MULTIPLY", ny_, ny_)))
    en_ = matematik(ntk_, "DIVIDE", en_, matematik(ntk_, "MAXIMUM", p_, None, deger_b=1e-6))
    u_ = matematik(ntk_, "MAXIMUM", en_, matematik(ntk_, "ABSOLUTE", matematik(ntk_, "DIVIDE", dz, None, deger_b=R)))
elif MANGO:
    p_rad = matematik(ntk_, "DIVIDE", v_r.outputs[0], None, deger_b=R)
    ny = matematik(ntk_, "DIVIDE", dy, None, deger_b=B)
    nz = matematik(ntk_, "DIVIDE", dz, None, deger_b=R)
    u_ = matematik(ntk_, "DIVIDE", matematik(ntk_, "SQRT", matematik(ntk_, "ADD",
        matematik(ntk_, "MULTIPLY", ny, ny), matematik(ntk_, "MULTIPLY", nz, nz))),
        matematik(ntk_, "MAXIMUM", p_rad, None, deger_b=1e-6))
else:
    u_ = matematik(ntk_, "DIVIDE", rad, v_r.outputs[0])
et_r = ntk_.nodes.new("ShaderNodeValToRGB")
if MANGO:
    et_r.color_ramp.elements[0].color = hex_renk("#f6ae33")
    et_r.color_ramp.elements[1].position = 1.0
    et_r.color_ramp.elements[1].color = hex_renk("#d88922")
    e_mango = et_r.color_ramp.elements.new(0.96); e_mango.color = hex_renk("#f6a32c")
elif KARPUZ:
    et_r.color_ramp.elements[0].color = hex_renk("#e84244")
    et_r.color_ramp.elements[1].position = 1.0
    et_r.color_ramp.elements[1].color = hex_renk("#143c27")
    for pos, renk_ in ((0.72, "#d92730"), (0.78, "#ee7773"), (0.81, "#f8efdc"),
                       (0.90, "#ebedd5"), (0.965, "#a2c891"), (0.985, "#1d4a2d")):
        el = et_r.color_ramp.elements.new(pos); el.color = hex_renk(renk_)
else:
    et_r.color_ramp.elements[0].color = hex_renk("#fff1e5" if CILEK else "#f1e9b8")
    et_r.color_ramp.elements[1].position = 0.97
    et_r.color_ramp.elements[1].color = hex_renk("#a81722" if CILEK else "#a8cc5c")
    e_m = et_r.color_ramp.elements.new(0.42 if CILEK else 0.6); e_m.color = hex_renk("#f7a7ab" if CILEK else "#e3e08e")
if MANGO:
    cek, ell = mango_cekirdek_maske(ntk_, v_x.outputs[0], dy, dz)
    lif = matematik(ntk_, "MULTIPLY", matematik(ntk_, "GREATER_THAN", ell, None, deger_b=1.0),
                    matematik(ntk_, "LESS_THAN", ell, None, deger_b=1.35))
    lif_mix = ntk_.nodes.new("ShaderNodeMix"); lif_mix.data_type = "RGBA"
    baglan(ntk_, lif, lif_mix.inputs["Factor"])
    baglan(ntk_, et_r.outputs["Color"], lif_mix.inputs[6])
    lif_mix.inputs[7].default_value = hex_renk("#d98627")
    cek_mix = ntk_.nodes.new("ShaderNodeMix"); cek_mix.data_type = "RGBA"
    baglan(ntk_, cek, cek_mix.inputs["Factor"])
    baglan(ntk_, lif_mix.outputs[2], cek_mix.inputs[6])
    cek_mix.inputs[7].default_value = hex_renk("#ae7941")
    baglan(ntk_, cek_mix.outputs[2], bk_.inputs["Base Color"])
elif CILEK:
    e_r = et_r.color_ramp.elements.new(0.82); e_r.color = hex_renk("#d52b36")
elif not KARPUZ:
    e_k = et_r.color_ramp.elements.new(0.985); e_k.color = hex_renk("#21361a")
baglan(ntk_, u_, et_r.inputs["Fac"])
if CILEK:
    baglan(ntk_, et_r.outputs["Color"], bk_.inputs["Base Color"])
elif KARPUZ:
    tohum_maske = karpuz_cekirdek_maske(ntk_, v_x.outputs[0], dy,
        matematik(ntk_, "ADD", dz, None, deger_b=MERKEZ_Z))
    # Koyu cekirdek yalniz kirmizi et araliginda.
    tohum_maske = matematik(ntk_, "MULTIPLY", tohum_maske,
        matematik(ntk_, "LESS_THAN", u_, None, deger_b=0.72))
    cek = ntk_.nodes.new("ShaderNodeMix"); cek.data_type = "RGBA"
    baglan(ntk_, tohum_maske, cek.inputs["Factor"])
    baglan(ntk_, et_r.outputs["Color"], cek.inputs[6])
    cek.inputs[7].default_value = hex_renk("#261b18")
    baglan(ntk_, cek.outputs[2], bk_.inputs["Base Color"])
elif KIVI:
    kivi_renk, _ = kivi_ic_renk(ntk_, v_x.outputs[0], dy, dz, v_r.outputs[0])
    baglan(ntk_, kivi_renk, bk_.inputs["Base Color"])
else:
    ck_ = M["cekirdek"]
    dxp = matematik(ntk_, "SUBTRACT", v_x.outputs[0], None, deger_b=ck_["x"] * A)
    cdist = matematik(ntk_, "SQRT", matematik(ntk_, "ADD", matematik(ntk_, "MULTIPLY", dxp, dxp),
                                             matematik(ntk_, "ADD", matematik(ntk_, "MULTIPLY", dy, dy), matematik(ntk_, "MULTIPLY", dz, dz))))
    cu = matematik(ntk_, "DIVIDE", cdist, None, deger_b=ck_["r"] * R)
    cek_r_ = ntk_.nodes.new("ShaderNodeValToRGB")
    cek_r_.color_ramp.interpolation = "CONSTANT"
    cek_r_.color_ramp.elements[0].color = hex_renk("#b98a52")
    cek_r_.color_ramp.elements[1].position = 1.0
    cek_r_.color_ramp.elements[1].color = hex_renk("#000000", 0.0)
    c_k = cek_r_.color_ramp.elements.new(0.86); c_k.color = hex_renk("#4a2412")
    baglan(ntk_, cu, cek_r_.inputs["Fac"])
    ic_mi = matematik(ntk_, "LESS_THAN", cu, None, deger_b=1.0)
    kk_ = ntk_.nodes.new("ShaderNodeMix"); kk_.data_type = "RGBA"
    baglan(ntk_, ic_mi, kk_.inputs["Factor"])
    baglan(ntk_, et_r.outputs["Color"], kk_.inputs[6])
    baglan(ntk_, cek_r_.outputs["Color"], kk_.inputs[7])
    baglan(ntk_, kk_.outputs[2], bk_.inputs["Base Color"])
bk_.inputs["Roughness"].default_value = 0.45
# guvence: meyve kesitinin disina tasan her nokta seffaf
_dis = matematik(ntk_, "GREATER_THAN", u_, None, deger_b=1.0)
_sf = ntk_.nodes.new("ShaderNodeBsdfTransparent")
_mx = ntk_.nodes.new("ShaderNodeMixShader")
baglan(ntk_, _dis, _mx.inputs[0])
baglan(ntk_, bk_.outputs[0], _mx.inputs[1])
baglan(ntk_, _sf.outputs[0], _mx.inputs[2])
baglan(ntk_, _mx.outputs[0], ntk_.nodes["Material Output"].inputs["Surface"])
kesit.data.materials.append(mk_)
nt_k = mk_.node_tree
kesit.hide_render = True
kesit.keyframe_insert("hide_render", frame=0)
for tur in PLAN["turlar"]:
    xk = [(v_[0], v_[2]) for v_ in tur["vuruslar"] if v_[1] == "x"]
    kesit.hide_render = False
    kesit.keyframe_insert("hide_render", frame=kare(xk[0][0]))
    kesit.hide_render = True
    kesit.keyframe_insert("hide_render", frame=kare(xk[-1][0] if MANGO else xk[-1][0] + 0.02))
    for t, konum in xk:
        r_ = 1.0 if CILEK else float(profil_r(np.array([konum]))[0]) * 0.995
        # Yalniz kalan govdenin yeni kesim duzlemine bagli; hicbir nesnede
        # kameraya/yone dogru ayrik bir on yuz konumlandirilmaz.
        z_kayma = 0.09 * math.sin(math.pi * konum / A) if MANGO else 0.0
        kesit.location = (konum + 0.002, 0, MERKEZ_Z + z_kayma)
        kesit.scale = (1, B * r_ / R, r_) if MANGO else (1, r_, r_)
        kesit.keyframe_insert("location", frame=kare(t))
        kesit.keyframe_insert("scale", frame=kare(t))
        for ad_, deger in (("kesit_r", r_), ("kesit_x", konum)):
            nt_k.nodes[ad_].outputs[0].default_value = deger
            nt_k.nodes[ad_].outputs[0].keyframe_insert("default_value", frame=kare(t))
sabit_interp(kesit)
sabit_interp(nt_k)

# ---------------------------------------------------------------- isik + kamera
gunes = bpy.data.lights.new("gunes", "SUN")
gunes.energy = 0.75
gunes.angle = math.radians(6)
g = bpy.data.objects.new("gunes", gunes)
g.rotation_euler = (math.radians(50), math.radians(-28), math.radians(-35))
sc.collection.objects.link(g)
alan = bpy.data.lights.new("dolgu", "AREA")
alan.energy = 700
alan.size = 3.0
alan.color = (1.0, 0.84, 0.67)
a = bpy.data.objects.new("dolgu", alan)
a.location = (-2.0, -4.5, 5.0)
a.rotation_euler = (math.radians(45), 0, math.radians(-22))
arka = bpy.data.lights.new("arka", "AREA")
arka.energy = 140
arka.size = 3
arka.color = (0.66, 0.82, 0.88)
ab = bpy.data.objects.new("arka", arka)
ab.location = (2.5, 1.8, 3.5)
ab.rotation_euler = (math.radians(-55), math.radians(30), 0)
sc.collection.objects.link(ab)
sc.collection.objects.link(a)

cam = bpy.data.cameras.new("kamera")
cam.lens = 58
cam.sensor_fit = "HORIZONTAL"
cam.sensor_width = 36
k = bpy.data.objects.new("kamera", cam)
k.location = (0.0, -6.7, 3.55)  # tam karsidan (kullanici 13 Kas)
sc.collection.objects.link(k)
hedef = bpy.data.objects.new("hedef", None)
hedef.location = (0.0, -0.1, 0.62)
cam.dof.use_dof = True
cam.dof.focus_object = hedef
cam.dof.aperture_fstop = 4.0
sc.collection.objects.link(hedef)
tr = k.constraints.new("TRACK_TO")
tr.target = hedef
tr.track_axis = "TRACK_NEGATIVE_Z"
tr.up_axis = "UP_Y"
sc.camera = k
# foto modu (marka gorselleri): --cozunurluk WxH, --kamera "kx,ky,kz,hx,hy,hz,lens"
if arg("--cozunurluk"):
    w_, h_ = (int(v) for v in arg("--cozunurluk").lower().split("x"))
    sc.render.resolution_x, sc.render.resolution_y = w_, h_
    sc.render.resolution_percentage = 100
    cam.sensor_fit = "AUTO"
if arg("--kamera"):
    kv = [float(v) for v in arg("--kamera").split(",")]
    k.location = kv[0:3]
    hedef.location = kv[3:6]
    cam.lens = kv[6]

# ---------------------------------------------------------------- render
os.makedirs(CIKTI, exist_ok=True)
kareler = arg("--kareler")
if kareler:
    liste = [int(x) for x in kareler.split(",") if x.strip()]
else:
    liste = list(range(int(arg("--bas", "1")), int(arg("--son", str(PLAN["kare"]))) + 1, int(arg("--adim", "1"))))
if arg("--kaydet"):
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(arg("--kaydet")))
if arg("--render", "1") == "1":
    for f in liste:
        sc.frame_set(f)
        sc.render.filepath = os.path.join(CIKTI, f"kare_{f:04d}.png")
        import time as _t
        _b = _t.time()
        bpy.ops.render.render(write_still=True)
        print(f"KARE {f} tamam {(_t.time() - _b):.1f} sn", flush=True)
