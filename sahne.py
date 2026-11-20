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
from plan import ananas_goz, ananas_sap, ananas_tac, biber_canak, biber_profil, domates_canak, icinde, meyve_profil, nar_tac, profil_yaricap, muz_egri, salatalik_egri

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
ANANAS = PLAN["meyve"] == "pineapple"
APPLE = PLAN["meyve"] == "apple"
ORANGE = PLAN["meyve"] == "orange"
BANANA = PLAN["meyve"] == "banana"
PEACH = PLAN["meyve"] == "peach"
NAR = PLAN["meyve"] == "pomegranate"
TOMATO = PLAN["meyve"] == "tomato"
CUCUMBER = PLAN["meyve"] == "cucumber"
PEPPER = PLAN["meyve"] == "red-bell-pepper"
B = M.get("B", R)
XMIN, XMAX = M.get("xmin", -A), M.get("xmax", A)
TAHTA_UST = 0.14
MERKEZ_Z = TAHTA_UST + R - 0.03 + (0.12 if BANANA else (0.04 if CUCUMBER else 0.0))
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
bpy.ops.mesh.primitive_uv_sphere_add(segments=128 if ANANAS else 96,
                                    ring_count=96 if ANANAS else 64,
                                    radius=1.0, location=(0, 0, MERKEZ_Z))
meyve = bpy.context.object
meyve.name = "meyve"
# Kure -> plan.py ile birebir ayni profil; cilekte dikey eksen Z.
goz_degerleri = []
for v in meyve.data.vertices:
    x, y, z = v.co
    eks = z if CILEK else x
    sphere_r = math.sqrt(max(0.0, 1.0 - eks * eks))
    radial = float(meyve_profil(np.array([eks]), M)[0]) / max(sphere_r, 1e-6) / FMAX
    if PEPPER:
        zz=z*R
        angle=math.atan2(y,x)
        lob=1.0-.14*math.cos(4*angle)
        ring=float(biber_profil(zz,M))*lob/max(math.sqrt(max(0.0,1.0-z*z)),1e-6)
        v.co=(x*A*ring,y*B*ring,zz)
    elif CILEK:
        v.co = (x * A * radial, y * B * radial, z * R)
    elif ANANAS:
        eye = float(ananas_goz(np.array([x * A]), np.array([math.atan2(z, y)]), M)[0])
        rr = R * float(meyve_profil(np.array([x]), M)[0]) / FMAX + 0.035 * eye
        scale = rr / max(sphere_r, 1e-6)
        v.co = (x * A, y * scale, z * scale)
        goz_degerleri.append(eye)
    else:
        xx, yy, zz = x * A, y * R * radial, z * R * radial
        if APPLE:
            # Iki gercek cukur; ustte bes yumusak omuz lobu.
            dip = 0.105 * math.exp(-(xx*xx + yy*yy) / 0.032)
            lob = 0.025 * math.cos(5 * math.atan2(yy, xx)) * max(0.0, (zz / R))**6
            zz -= math.copysign(dip, zz) if abs(zz) > 0.45 else 0.0
            zz += lob
            omuz = 1.0 + 0.08 * math.tanh(zz / (0.20*R))
            xx *= omuz; yy *= omuz
        elif ORANGE:
            zz *= 0.96
        elif BANANA:
            theta = math.atan2(zz, yy)
            rib = 1.0 + 0.11 * math.cos(5.0 * theta)
            yy *= rib; zz = zz * rib + float(muz_egri(xx, M))
        elif CUCUMBER:
            theta = math.atan2(zz, yy)
            ridge = 1.0 + .025 * math.cos(9*theta + .8*xx)
            yy *= ridge; zz = zz*ridge + float(salatalik_egri(xx, M))
        elif PEACH:
            theta = math.atan2(zz, yy)
            groove = 1.0 - 0.045 * math.exp(-(xx/.09)**2) * (yy < 0)
            wobble = 1.0 + 0.035 * math.sin(3*theta + 0.5)
            yy *= groove*wobble; zz *= groove*wobble
            if zz > 0.5:
                zz -= 0.07 * math.exp(-(xx*xx + yy*yy)/0.035)
        elif NAR or TOMATO:
            angle=math.atan2(zz,yy)
            lob=1.0+(0.025 if NAR else 0.035)*math.cos(5*angle)
            yy*=lob; zz*=lob
            if zz>0.53:
                zz-=0.04*math.exp(-(xx*xx+yy*yy)/0.045)
        v.co = (xx, yy, zz)
if ANANAS:
    goz_at = meyve.data.attributes.new("ananas_goz", "FLOAT", "POINT")
    goz_at.data.foreach_set("value", np.asarray(goz_degerleri, dtype=np.float32))
bpy.ops.object.shade_smooth()

m, nt, bsdf = malzeme("ananas_kabarik_baklava_goz" if ANANAS else ("elma_alacali_kabuk" if APPLE else ("portakal_gozenekli_kabuk" if ORANGE else ("salatalik_purtuklu_kabuk" if CUCUMBER else ("kirmizi_biber_parlak_loblu_kabuk" if PEPPER else ("kivi_kisa_tuylu_kabuk" if KIVI else ("karpuz_seritli_kabuk" if KARPUZ else ("cilek_yuzey" if CILEK else "avokado_kabuk"))))))))
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
if ANANAS:
    goz_attr = nt.nodes.new("ShaderNodeAttribute")
    goz_attr.attribute_name = "ananas_goz"
    goz_ramp = nt.nodes.new("ShaderNodeValToRGB")
    goz_ramp.color_ramp.elements[0].color = hex_renk("#4c4727")
    goz_ramp.color_ramp.elements[1].color = hex_renk("#dfb653")
    for pos, renk_ in ((0.15, "#6f7838"), (0.42, "#a18b35"), (0.75, "#c69c39")):
        el = goz_ramp.color_ramp.elements.new(pos); el.color = hex_renk(renk_)
    baglan(nt, goz_attr.outputs["Fac"], goz_ramp.inputs["Fac"])
    kabuk_rengi = goz_ramp.outputs["Color"]
else:
    kabuk_rengi = karpuz_serit(nt, tk.outputs["Object"]) if KARPUZ else kabuk_rmp.outputs["Color"]
    if APPLE:
        # Kirmizi allik, sari/yesil omuzlar ve dogal benekler.
        alaca = nt.nodes.new("ShaderNodeTexNoise")
        alaca.inputs["Scale"].default_value = 6.0
        alaca.inputs["Detail"].default_value = 3.0
        baglan(nt, tk.outputs["Object"], alaca.inputs["Vector"])
        arm = nt.nodes.new("ShaderNodeValToRGB")
        arm.color_ramp.elements[0].color = hex_renk("#77151a")
        arm.color_ramp.elements[1].color = hex_renk("#a8251f")
        for pos, col in ((0.30,"#9c1a20"),(0.58,"#b2261e"),(0.79,"#b83b20"),(0.91,"#a69940")):
            e = arm.color_ramp.elements.new(pos); e.color = hex_renk(col)
        baglan(nt, alaca.outputs["Fac"], arm.inputs["Fac"])
        benek_m = matematik(nt,"LESS_THAN",vor.outputs["Distance"],None,deger_b=.055)
        benek_c = nt.nodes.new("ShaderNodeMix"); benek_c.data_type="RGBA"
        baglan(nt,benek_m,benek_c.inputs["Factor"])
        baglan(nt,arm.outputs["Color"],benek_c.inputs[6])
        benek_c.inputs[7].default_value=hex_renk("#d8b988")
        kabuk_rengi = benek_c.outputs[2]
        bmp.inputs["Strength"].default_value = 0.10
        bmp.inputs["Distance"].default_value = 0.004
    elif ORANGE:
        por = nt.nodes.new("ShaderNodeTexVoronoi")
        por.inputs["Scale"].default_value = 72.0
        baglan(nt, tk.outputs["Object"], por.inputs["Vector"])
        por_r = nt.nodes.new("ShaderNodeValToRGB")
        por_r.color_ramp.elements[0].color = hex_renk("#a83d0b")
        por_r.color_ramp.elements[1].color = hex_renk("#f98a16")
        e = por_r.color_ramp.elements.new(0.24); e.color = hex_renk("#d65d0b")
        baglan(nt, por.outputs["Distance"], por_r.inputs["Fac"])
        kabuk_rengi = por_r.outputs["Color"]
        baglan(nt, por.outputs["Distance"], bmp.inputs["Height"])
        bmp.inputs["Strength"].default_value = 0.38
        bmp.inputs["Distance"].default_value = 0.013
    elif BANANA:
        bruise = nt.nodes.new("ShaderNodeTexNoise")
        bruise.inputs["Scale"].default_value = 8.0
        bruise.inputs["Detail"].default_value = 3.0
        baglan(nt, tk.outputs["Object"], bruise.inputs["Vector"])
        br = nt.nodes.new("ShaderNodeValToRGB")
        br.color_ramp.elements[0].color = hex_renk("#aa7d1d")
        br.color_ramp.elements[1].color = hex_renk("#eebd20")
        e = br.color_ramp.elements.new(.48); e.color = hex_renk("#dbad1d")
        baglan(nt, bruise.outputs["Fac"], br.inputs["Fac"])
        spots = matematik(nt,"LESS_THAN",vor.outputs["Distance"],None,deger_b=.095)
        sm = nt.nodes.new("ShaderNodeMix"); sm.data_type="RGBA"
        baglan(nt, spots, sm.inputs["Factor"])
        baglan(nt, br.outputs["Color"], sm.inputs[6])
        sm.inputs[7].default_value = hex_renk("#855c2c")
        kabuk_rengi = sm.outputs[2]
        bmp.inputs["Strength"].default_value = 0.12
        bmp.inputs["Distance"].default_value = .004
    elif CUCUMBER:
        gr=nt.nodes.new("ShaderNodeValToRGB")
        gr.color_ramp.elements[0].color=hex_renk("#214a20")
        gr.color_ramp.elements[1].color=hex_renk("#5b8e37")
        e=gr.color_ramp.elements.new(.55);e.color=hex_renk("#376c2c")
        baglan(nt,nz.outputs["Fac"],gr.inputs["Fac"])
        kabuk_rengi=gr.outputs["Color"]
        pore=nt.nodes.new("ShaderNodeTexVoronoi")
        pore.inputs["Scale"].default_value=85.0
        baglan(nt,tk.outputs["Object"],pore.inputs["Vector"])
        baglan(nt,pore.outputs["Distance"],bmp.inputs["Height"])
        bmp.inputs["Strength"].default_value=.28
        bmp.inputs["Distance"].default_value=.009
    elif PEACH:
        blush = nt.nodes.new("ShaderNodeTexNoise")
        blush.inputs["Scale"].default_value = 4.0
        blush.inputs["Detail"].default_value = 3.0
        baglan(nt, tk.outputs["Object"], blush.inputs["Vector"])
        xyz = nt.nodes.new("ShaderNodeSeparateXYZ")
        baglan(nt, tk.outputs["Object"], xyz.inputs[0])
        xblush = matematik(nt,"ADD",
            matematik(nt,"MULTIPLY",xyz.outputs[0],None,deger_b=.46/A),
            matematik(nt,"MULTIPLY",blush.outputs["Fac"],None,deger_b=.28))
        xblush = matematik(nt,"ADD",xblush,None,deger_b=.25)
        pr = nt.nodes.new("ShaderNodeValToRGB")
        pr.color_ramp.elements[0].color = hex_renk("#e9ac4d")
        pr.color_ramp.elements[1].color = hex_renk("#b72d35")
        e=pr.color_ramp.elements.new(.50); e.color=hex_renk("#e86543")
        baglan(nt, xblush, pr.inputs["Fac"])
        kabuk_rengi = pr.outputs["Color"]
        pos = nt.nodes.new("ShaderNodeSeparateXYZ")
        baglan(nt, tk.outputs["Object"], pos.inputs[0])
        seam = matematik(nt,"LESS_THAN",matematik(nt,"ABSOLUTE",pos.outputs[0]),None,deger_b=.012)
        front = matematik(nt,"LESS_THAN",pos.outputs[1],None,deger_b=-.12)
        seam = matematik(nt,"MULTIPLY",seam,front)
        ss=nt.nodes.new("ShaderNodeMix");ss.data_type="RGBA"
        baglan(nt,seam,ss.inputs["Factor"])
        baglan(nt,kabuk_rengi,ss.inputs[6])
        ss.inputs[7].default_value=hex_renk("#bd6047")
        kabuk_rengi=ss.outputs[2]
        fuzz = nt.nodes.new("ShaderNodeTexNoise")
        fuzz.inputs["Scale"].default_value = 170.0
        baglan(nt, tk.outputs["Object"], fuzz.inputs["Vector"])
        baglan(nt, fuzz.outputs["Fac"], bmp.inputs["Height"])
        bmp.inputs["Strength"].default_value = .38
        bmp.inputs["Distance"].default_value = .007
    elif NAR:
        nr=nt.nodes.new("ShaderNodeValToRGB")
        nr.color_ramp.elements[0].color=hex_renk("#5c101b")
        nr.color_ramp.elements[1].color=hex_renk("#ac2730")
        e=nr.color_ramp.elements.new(.52);e.color=hex_renk("#84202a")
        baglan(nt,nz.outputs["Fac"],nr.inputs["Fac"])
        kabuk_rengi=nr.outputs["Color"]
        bmp.inputs["Strength"].default_value=.15
        bmp.inputs["Distance"].default_value=.01
    elif TOMATO:
        tr=nt.nodes.new("ShaderNodeValToRGB")
        tr.color_ramp.elements[0].color=hex_renk("#a6191b")
        tr.color_ramp.elements[1].color=hex_renk("#e43623")
        e=tr.color_ramp.elements.new(.55);e.color=hex_renk("#c8231b")
        baglan(nt,nz.outputs["Fac"],tr.inputs["Fac"])
        kabuk_rengi=tr.outputs["Color"]
        bmp.inputs["Strength"].default_value=.06
        bmp.inputs["Distance"].default_value=.003
    elif PEPPER:
        red=nt.nodes.new("ShaderNodeValToRGB")
        red.color_ramp.elements[0].color=hex_renk("#8d171a")
        red.color_ramp.elements[1].color=hex_renk("#e3321c")
        e=red.color_ramp.elements.new(.52);e.color=hex_renk("#c6221b")
        baglan(nt,nz.outputs["Fac"],red.inputs["Fac"])
        kabuk_rengi=red.outputs["Color"]
        bmp.inputs["Strength"].default_value=.05
        bmp.inputs["Distance"].default_value=.003

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
bsdf.inputs["Roughness"].default_value = (0.91 if PEACH else (0.27 if PEPPER else (0.62 if CUCUMBER else (0.57 if ANANAS else
    (0.88 if KIVI else (0.54 if NAR else (0.30 if TOMATO else
    (0.46 if ORANGE else (0.35 if APPLE else (0.42 if CILEK else
    (0.34 if KARPUZ else 0.26)))))))))))
kes_x = nt.nodes.new("ShaderNodeValue"); kes_x.name = "kes_x"; kes_x.outputs[0].default_value = -10.0
kirp = matematik(nt, "LESS_THAN", ayir.outputs[0], kes_x.outputs[0])
seffaf = nt.nodes.new("ShaderNodeBsdfTransparent")
karis_s = nt.nodes.new("ShaderNodeMixShader")
baglan(nt, kirp, karis_s.inputs[0])
baglan(nt, bsdf.outputs[0], karis_s.inputs[1])
baglan(nt, seffaf.outputs[0], karis_s.inputs[2])
baglan(nt, karis_s.outputs[0], nt.nodes["Material Output"].inputs["Surface"])
meyve.data.materials.append(m)

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

ANANAS_EK_OB = []
ANANAS_EK_NT = []
if ANANAS:
    def ananas_ek_malzeme(ad, renk):
        mat, tree, b = malzeme(ad)
        b.inputs["Base Color"].default_value = hex_renk(renk)
        b.inputs["Roughness"].default_value = 0.61
        tc = tree.nodes.new("ShaderNodeTexCoord")
        if "yaprak" in ad:
            damar = tree.nodes.new("ShaderNodeTexNoise")
            damar.inputs["Scale"].default_value = 26.0
            damar.inputs["Detail"].default_value = 2.0
            baglan(tree, tc.outputs["Object"], damar.inputs["Vector"])
            yesil = tree.nodes.new("ShaderNodeValToRGB")
            yesil.color_ramp.elements[0].color = hex_renk("#214b28")
            yesil.color_ramp.elements[1].color = hex_renk("#65a54d")
            baglan(tree, damar.outputs["Fac"], yesil.inputs["Fac"])
            baglan(tree, yesil.outputs["Color"], b.inputs["Base Color"])
        xyz = tree.nodes.new("ShaderNodeSeparateXYZ")
        baglan(tree, tc.outputs["Object"], xyz.inputs[0])
        kes = tree.nodes.new("ShaderNodeValue")
        kes.name = "kes_x"; kes.outputs[0].default_value = -10.0
        sil = matematik(tree, "LESS_THAN", xyz.outputs[0], kes.outputs[0])
        mix = tree.nodes.new("ShaderNodeMixShader")
        trn = tree.nodes.new("ShaderNodeBsdfTransparent")
        baglan(tree, sil, mix.inputs[0])
        baglan(tree, b.outputs[0], mix.inputs[1])
        baglan(tree, trn.outputs[0], mix.inputs[2])
        baglan(tree, mix.outputs[0], tree.nodes["Material Output"].inputs["Surface"])
        ANANAS_EK_NT.append(tree)
        return mat

    yesiller = [ananas_ek_malzeme("ananas_yaprak_koyu", "#28572c"),
                ananas_ek_malzeme("ananas_yaprak_acik", "#4d923d"),
                ananas_ek_malzeme("ananas_tac_dibi", "#315f2e")]
    vs, fs, mi = [], [], []
    base = 0.78 * A
    for i in range(16):
        aci = 2 * math.pi * i / 16
        uzunluk = min(0.81, 0.77 + 0.035 * math.sin(i * 2.3) + 0.020 * math.cos(i * 3.7))
        once = None
        for t in (0.0, 0.22, 0.48, 0.72, 0.90):
            merkez = R * (0.19 + 0.53 * t)
            yarim = R * (0.26 * (1 - t) + 0.15)
            da = (0.44 * (1 - t) + 0.09) * (2 * math.pi / 16)
            j = len(vs)
            for rr, aa in ((merkez - yarim, aci - da), (merkez + yarim, aci - da),
                           (merkez + yarim, aci + da), (merkez - yarim, aci + da)):
                vs.append((base + uzunluk * t, rr * math.cos(aa), rr * math.sin(aa)))
            if once is not None:
                for q in range(4):
                    fs.append((once + q, once + (q + 1) % 4, j + (q + 1) % 4, j + q))
                    mi.append(i % 2)
            else:
                fs.append((j + 3, j + 2, j + 1, j)); mi.append(i % 2)
            once = j
        tip = len(vs)
        merkez = R * 0.72
        vs.append((base + uzunluk, merkez * math.cos(aci), merkez * math.sin(aci)))
        for q in range(4):
            fs.append((once + q, once + (q + 1) % 4, tip)); mi.append(i % 2)
    # Orta dip, yapraklarla ayni kesim hacminin icindedir.
    j = len(vs)
    for xx, rr in ((base, 0.19 * R), (A + 0.18, 0.07 * R)):
        for i in range(16):
            aa = 2 * math.pi * i / 16
            vs.append((xx, rr * math.cos(aa), rr * math.sin(aa)))
    for i in range(16):
        fs.append((j + i, j + (i + 1) % 16, j + 16 + (i + 1) % 16, j + 16 + i)); mi.append(2)
    fs.extend((tuple(j + i for i in range(15, -1, -1)),
               tuple(j + 16 + i for i in range(16))))
    mi.extend((2, 2))
    tac_mesh = bpy.data.meshes.new("ananas_on_alti_yaprak_tac")
    tac_mesh.from_pydata(vs, [], fs)
    tac_mesh.update()
    for p_, index in zip(tac_mesh.polygons, mi):
        p_.material_index = index
    tac_ob = bpy.data.objects.new("ananas_tac_kesilip_kuplenir", tac_mesh)
    sc.collection.objects.link(tac_ob)
    tac_ob.parent = meyve
    for mat in yesiller:
        tac_mesh.materials.append(mat)
    ANANAS_EK_OB.append(tac_ob)

    sap_mat = ananas_ek_malzeme("ananas_sol_sap_tabani", "#776643")
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.07, depth=0.13)
    sap_ob = bpy.context.object
    sap_ob.name = "ananas_sap_kesilip_kuplenir"
    sap_ob.location = (XMIN + 0.065, 0, 0)
    sap_ob.rotation_euler = (0, math.pi / 2, 0)
    bpy.ops.object.transform_apply(location=True, rotation=True)
    sap_ob.parent = meyve
    sap_ob.data.materials.append(sap_mat)
    ANANAS_EK_OB.append(sap_ob)

if APPLE or ORANGE or BANANA or NAR or TOMATO or CUCUMBER or PEPPER:
    def bagli_malzeme(ad, renk):
        mat, tree, b = malzeme(ad)
        b.inputs["Base Color"].default_value = hex_renk(renk)
        b.inputs["Roughness"].default_value = 0.69
        tc = tree.nodes.new("ShaderNodeTexCoord")
        xyz = tree.nodes.new("ShaderNodeSeparateXYZ")
        baglan(tree, tc.outputs["Object"], xyz.inputs[0])
        kes = tree.nodes.new("ShaderNodeValue"); kes.name = "kes_x"
        kes.outputs[0].default_value = -10.0
        sil = matematik(tree, "LESS_THAN", xyz.outputs[0], kes.outputs[0])
        mix = tree.nodes.new("ShaderNodeMixShader")
        trn = tree.nodes.new("ShaderNodeBsdfTransparent")
        baglan(tree, sil, mix.inputs[0]); baglan(tree, b.outputs[0], mix.inputs[1])
        baglan(tree, trn.outputs[0], mix.inputs[2])
        baglan(tree, mix.outputs[0], tree.nodes["Material Output"].inputs["Surface"])
        ANANAS_EK_NT.append(tree)
        return mat
    if APPLE:
        # Sap cukurundan cikan kisa, gercek odunsu sap.
        sm = bagli_malzeme("elma_odunsu_sap", "#624027")
        bpy.ops.mesh.primitive_cylinder_add(vertices=14, radius=0.050, depth=0.22)
        ob = bpy.context.object; ob.name = "elma_sapi_kesilir"
        ob.location = (0, 0, 0.65)
        bpy.ops.object.transform_apply(location=True, rotation=True)
        ob.parent = meyve; ob.data.materials.append(sm)
        ANANAS_EK_OB.append(ob)
        lm = bagli_malzeme("elma_yaprak", "#3c792d")
        vs = [(0.02,-0.10,0.66),(0.11,-0.43,0.75),(0.48,-0.45,0.74),(0.25,-0.34,0.67)]
        mesh = bpy.data.meshes.new("elma_yaprak_mesh"); mesh.from_pydata(vs,[],[(0,1,2,3)]); mesh.update()
        ob = bpy.data.objects.new("elma_yaprak_kesilir",mesh); sc.collection.objects.link(ob)
        ob.parent = meyve; ob.data.materials.append(lm); ANANAS_EK_OB.append(ob)
    elif ORANGE:
        # Bes uc yaprakli kucuk ust kaliks; govde kabugu gibi degil, yesil.
        cm = bagli_malzeme("portakal_yesil_kaliks", "#396a2e")
        vs=[(0,0,0.755)]; fs=[]
        for i in range(5):
            a=2*math.pi*i/5
            mid=len(vs)
            vs.extend([(0.08*math.cos(a-.35),0.08*math.sin(a-.35),0.752),
                       (0.21*math.cos(a),0.21*math.sin(a),0.715),
                       (0.08*math.cos(a+.35),0.08*math.sin(a+.35),0.752)])
            fs.append((0,mid,mid+1,mid+2))
        mesh=bpy.data.meshes.new("portakal_kaliks_mesh"); mesh.from_pydata(vs,[],fs); mesh.update()
        ob=bpy.data.objects.new("portakal_kaliks_kesilir",mesh); sc.collection.objects.link(ob)
        ob.parent=meyve; ob.data.materials.append(cm); ANANAS_EK_OB.append(ob)
    elif BANANA:
        for name, col, lo, hi, radius in (
            ("muz_sap", "#78613a", A-0.04, XMAX, .070),
            ("muz_cicek_ucu", "#4b3a2c", XMIN, -A+0.05, .047),
        ):
            mat = bagli_malzeme(name, col)
            bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=radius, depth=hi-lo)
            ob=bpy.context.object; ob.name=name+"_kesilir"
            ob.rotation_euler[1]=math.pi/2
            ob.location=((lo+hi)/2, 0, float(muz_egri((lo+hi)/2,M)))
            bpy.ops.object.transform_apply(location=True, rotation=True)
            ob.parent=meyve; ob.data.materials.append(mat); ANANAS_EK_OB.append(ob)
    elif CUCUMBER:
        mat=bagli_malzeme("salatalik_koyu_sap_ucu", "#43652a")
        bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=.052,depth=XMAX-A+.025)
        ob=bpy.context.object;ob.name="salatalik_sapi_kesilir"
        ob.rotation_euler[1]=math.pi/2
        mid=(A+XMAX-.025)/2
        ob.location=(mid,0,float(salatalik_egri(mid,M)))
        bpy.ops.object.transform_apply(location=True,rotation=True)
        ob.parent=meyve;ob.data.materials.append(mat);ANANAS_EK_OB.append(ob)
    elif NAR:
        cm = bagli_malzeme("nar_acik_besli_tac", "#9b4532")
        vs=[];fs=[]
        for i in range(5):
            angle=2*math.pi*i/5
            left=angle-math.pi/5;right=angle+math.pi/5
            j=len(vs)
            vs.extend([(.09*math.cos(left),.09*math.sin(left),.69),
                       (.20*math.cos(left),.20*math.sin(left),.72),
                       (.17*math.cos(angle),.17*math.sin(angle),.96),
                       (.20*math.cos(right),.20*math.sin(right),.72),
                       (.09*math.cos(right),.09*math.sin(right),.69)])
            fs.extend([(j,j+1,j+2),(j,j+2,j+4),(j+2,j+3,j+4)])
        mesh=bpy.data.meshes.new("nar_tac_mesh");mesh.from_pydata(vs,[],fs);mesh.update()
        ob=bpy.data.objects.new("nar_taci_kesilir",mesh);sc.collection.objects.link(ob)
        ob.parent=meyve;ob.data.materials.append(cm);ANANAS_EK_OB.append(ob)
    elif TOMATO:
        gm=bagli_malzeme("domates_yesil_canak", "#357a2f")
        vs=[(0,0,.735)];fs=[]
        for i in range(5):
            a=2*math.pi*i/5;j=len(vs)
            vs.extend([(.08*math.cos(a-.32),.08*math.sin(a-.32),.725),
                       (.30*math.cos(a),.30*math.sin(a),.697),
                       (.08*math.cos(a+.32),.08*math.sin(a+.32),.725)])
            fs.append((0,j,j+1,j+2))
        mesh=bpy.data.meshes.new("domates_canak_mesh");mesh.from_pydata(vs,[],fs);mesh.update()
        ob=bpy.data.objects.new("domates_canagi_kesilir",mesh);sc.collection.objects.link(ob)
        ob.parent=meyve;ob.data.materials.append(gm);ANANAS_EK_OB.append(ob)
        sm=bagli_malzeme("domates_sap", "#426633")
        bpy.ops.mesh.primitive_cylinder_add(vertices=14,radius=.043,depth=.14)
        ob=bpy.context.object;ob.name="domates_sapi_kesilir"
        ob.location=(0,0,.80)
        bpy.ops.object.transform_apply(location=True,rotation=True)
        ob.parent=meyve;ob.data.materials.append(sm);ANANAS_EK_OB.append(ob)
    elif PEPPER:
        green=bagli_malzeme("biber_yesil_besli_canak", "#2f7032")
        vs=[(0,0,.715)];fs=[]
        for i in range(5):
            a=2*math.pi*i/5;j=len(vs)
            vs.extend([(.10*math.cos(a-.33),.10*math.sin(a-.33),.705),
                       (.42*math.cos(a),.42*math.sin(a),.56),
                       (.10*math.cos(a+.33),.10*math.sin(a+.33),.705)])
            fs.append((0,j,j+1,j+2))
        mesh=bpy.data.meshes.new("biber_canak_mesh");mesh.from_pydata(vs,[],fs);mesh.update()
        ob=bpy.data.objects.new("biber_canagi_kesilir",mesh);sc.collection.objects.link(ob)
        ob.parent=meyve;ob.data.materials.append(green);ANANAS_EK_OB.append(ob)
        stem=bagli_malzeme("biber_kalin_sap", "#3b6d2d")
        bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=.053,depth=.24)
        ob=bpy.context.object;ob.name="biber_sapi_kesilir"
        ob.location=(0,0,.80)
        bpy.ops.object.transform_apply(location=True,rotation=True)
        ob.parent=meyve;ob.data.materials.append(stem);ANANAS_EK_OB.append(ob)

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
    xs = XMIN + (np.arange(gx) + 0.5) * ((XMAX - XMIN) / gx)
    ys = -B + (np.arange(gy) + 0.5) * (2 * B / gy)
    zmin, zmax = M.get("zmin", -R), M.get("zmax", R)
    zs = zmin + (np.arange(gz) + 0.5) * ((zmax-zmin) / gz)
    X, Y, Z = np.meshgrid(xs, ys, zs, indexing="ij")
    ic = icinde(X, Y, Z, M)
    idx = np.argwhere(ic)
    merk = np.stack([X[ic], Y[ic], Z[ic]], 1)
    k = len(merk)
    rng = np.random.default_rng(7 + no)
    hx, hy, hz = (XMAX - XMIN) / (2 * gx), B / gy, (zmax-zmin) / (2*gz)
    # Et/cekirdek rengi ve gercek dis kabuk maskesi ayni kaynak hucre konumundan gelir.
    if PEPPER:
        theta=np.arctan2(merk[:,1]/B,merk[:,0]/A)
        lob=1.0-.14*np.cos(4*theta)
        rr=np.maximum(.001,biber_profil(merk[:,2],M)*lob)
        d=np.sqrt((merk[:,0]/A)**2+(merk[:,1]/B)**2)/rr
    elif CILEK:
        pz = np.maximum(profil_r(merk[:, 2]), 1e-6)
        en = np.sqrt((merk[:, 0] / A) ** 2 + (merk[:, 1] / B) ** 2) / pz
        d = np.maximum(en, np.abs(merk[:, 2] / R))
    else:
        z_rad = (merk[:, 2] - muz_egri(merk[:, 0], M) if BANANA else
                 (merk[:, 2] - salatalik_egri(merk[:, 0], M) if CUCUMBER else merk[:, 2]))
        d = np.sqrt(merk[:, 1] ** 2 + z_rad ** 2) / np.maximum(profil_r(merk[:, 0]), 1e-6)
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
        if PEPPER:
            dis &= (u[:,0]>=.88) | (np.abs(merk[:,2])>=.74*R)
        maske += dis * (2 ** bit)
    if KIVI:
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
    elif ANANAS:
        # Kaynak konumu plan.py'deki hacimle ayni. Tac ve sap govde etine boyanmaz.
        renk = np.column_stack([np.interp(u[:, 0], [0, .28, .82, .95, 1],
            [hex_renk(h)[c] for h in ("#f8e9a2", "#f3dfa0", "#eec95f", "#aa8140", "#594925")])
            for c in range(3)])
        aci = np.arctan2(merk[:, 2], merk[:, 1])
        lif = (np.cos(38 * aci + 5 * merk[:, 0]) > .89) & (u[:, 0] > .28) & (u[:, 0] < .89)
        renk[lif] = .72 * renk[lif] + .28 * np.array(hex_renk("#fff2b8")[:3])
        govde = (np.abs(merk[:, 0]) <= A) & (merk[:, 1] ** 2 + merk[:, 2] ** 2 <=
            (profil_r(merk[:, 0]) + .035 * ananas_goz(merk[:, 0], aci, M)) ** 2)
        tac = ananas_tac(merk[:, 0], merk[:, 1], merk[:, 2], M) & ~govde
        sap = ananas_sap(merk[:, 0], merk[:, 1], merk[:, 2], M) & ~govde
        renk[tac] = np.array(hex_renk("#3e7937")[:3])
        renk[sap] = np.array(hex_renk("#776643")[:3])
        goz = ananas_goz(merk[:, 0], aci, M)
    elif BANANA:
        renk = np.tile(np.array(hex_renk("#f8efd5")[:3]), (k,1))
        renk[u[:,0] > .83] = np.array(hex_renk("#f5e6ad")[:3])
        renk[u[:,0] > .94] = np.array(hex_renk("#e7c137")[:3])
        zloc = merk[:,2] - muz_egri(merk[:,0],M)
        a = np.arctan2(zloc,merk[:,1])
        fleck = (u[:,0] < .15) & (np.cos(18*a + 9*merk[:,0]) > .93)
        renk[fleck] = np.array(hex_renk("#846849")[:3])
        stem = merk[:,0] > A-.04
        tip = merk[:,0] < -A+.05
        renk[stem] = np.array(hex_renk("#78613a")[:3])
        renk[tip] = np.array(hex_renk("#4b3a2c")[:3])
        maske[stem|tip] = 0
    elif CUCUMBER:
        renk=np.tile(np.array(hex_renk("#d8e6b1")[:3]),(k,1))
        renk[u[:,0]<.42]=np.array(hex_renk("#e5edc4")[:3])
        renk[u[:,0]>.84]=np.array(hex_renk("#a9c77e")[:3])
        renk[u[:,0]>.94]=np.array(hex_renk("#356d2c")[:3])
        angle=np.arctan2(z_rad,merk[:,1])
        seeds=(u[:,0]>.18)&(u[:,0]<.40)&(np.cos(11*angle+15*merk[:,0])>.95)
        renk[seeds]=np.array(hex_renk("#f8f2cd")[:3])
        stem=merk[:,0]>A-.025
        renk[stem]=np.array(hex_renk("#43652a")[:3]);maske[stem]=0
    elif PEACH:
        renk = np.tile(np.array(hex_renk("#f6ba63")[:3]), (k,1))
        renk[u[:,0] > .92] = np.array(hex_renk("#d95c4d")[:3])
        core = (merk[:,0]/(.40*A))**2 + (merk[:,1]/(.38*R))**2 + (merk[:,2]/(.44*R))**2
        pit = core < (1.0 + .14*np.sin(17*merk[:,0]+12*merk[:,2]))
        renk[pit] = np.array(hex_renk("#84502e")[:3])
        renk[pit & (core > .8)] = np.array(hex_renk("#a76b3b")[:3])
    elif NAR:
        renk=np.tile(np.array(hex_renk("#b52232")[:3]),(k,1))
        aci=np.arctan2(merk[:,2],merk[:,1])
        membrane=(np.cos(5*aci)>.94)&(u[:,0]<.78)
        pith=(u[:,0]>.77)&(u[:,0]<.90)
        renk[membrane|pith]=np.array(hex_renk("#f2e9d6")[:3])
        renk[u[:,0]>.90]=np.array(hex_renk("#8c1c27")[:3])
        beads=(u[:,0]<.78)&~membrane
        shade=(.85+.15*np.sin(38*merk[:,0]+47*merk[:,1]+52*merk[:,2]))[:,None]
        renk[beads]*=shade[beads]
        crown=nar_tac(merk[:,0],merk[:,1],merk[:,2],M)
        renk[crown]=np.array(hex_renk("#9b4532")[:3]);maske[crown]=0
    elif TOMATO:
        renk=np.tile(np.array(hex_renk("#cf3024")[:3]),(k,1))
        aci=np.arctan2(merk[:,2],merk[:,1])
        gel=(u[:,0]<.72)&(np.cos(5*aci)<.80)
        septa=(u[:,0]<.72)&~gel
        renk[gel]=np.array(hex_renk("#e9492b")[:3])
        renk[septa]=np.array(hex_renk("#ef9870")[:3])
        seed=gel&(u[:,0]>.24)&(u[:,0]<.62)&(np.cos(37*aci+23*merk[:,0])>.91)
        renk[seed]=np.array(hex_renk("#f8df9c")[:3])
        renk[u[:,0]>.92]=np.array(hex_renk("#c7231d")[:3])
        calyx=domates_canak(merk[:,0],merk[:,1],merk[:,2],M)
        renk[calyx]=np.array(hex_renk("#357a2f")[:3]);maske[calyx]=0
    elif PEPPER:
        renk=np.tile(np.array(hex_renk("#dc5130")[:3]),(k,1))
        renk[u[:,0]>.94]=np.array(hex_renk("#c3221a")[:3])
        renk[(u[:,0]>.72)&(u[:,0]<.90)]=np.array(hex_renk("#f2aa74")[:3])
        cream=(u[:,0]<.50)&(merk[:,2]>-.25)&(merk[:,2]<.65)
        renk[cream]=np.array(hex_renk("#f5dfac")[:3])
        seed=cream&(np.cos(29*merk[:,0]+37*merk[:,1]+41*merk[:,2])>.86)
        renk[seed]=np.array(hex_renk("#fff2cc")[:3])
        green=biber_canak(merk[:,0],merk[:,1],merk[:,2],M)
        renk[green]=np.array(hex_renk("#3b6d2d")[:3]);maske[green]=0
    elif APPLE:
        # Krem-beyaz et; yalniz merkezde bes odacikli cekirdek evi.
        renk = np.tile(np.array(hex_renk("#f5efdc")[:3]), (k, 1))
        renk[u[:, 0] > .91] = np.array(hex_renk("#c93225")[:3])
        aci = np.arctan2(merk[:, 2], merk[:, 1])
        merkez = (np.abs(merk[:, 0]) < .43*A) & (u[:, 0] < .37)
        odacik = merkez & (np.cos(5*aci) > .28) & (u[:, 0] > .15)
        tohum = odacik & (np.cos(5*aci) > .82) & (u[:, 0] > .22)
        renk[odacik] = np.array(hex_renk("#e1d5b6")[:3])
        renk[tohum] = np.array(hex_renk("#51321e")[:3])
        omuz=1.0+0.08*np.tanh(merk[:,2]/(.20*R))
        xn_app=merk[:,0]/(A*omuz)
        r_app=R*np.maximum(0,1-xn_app*xn_app)**.46
        govde = (np.abs(xn_app)<=1) & ((merk[:,1]/omuz)**2 +
            (np.abs(merk[:,2])+.105*np.exp(-(merk[:,0]**2+merk[:,1]**2)/.032))**2 <= r_app*r_app)
        sap = ~govde & (merk[:, 0]**2 + merk[:, 1]**2 <= .050**2) & (merk[:, 2] >= .56)
        yaprak = ~govde & ~sap & (((merk[:, 0]-.23)/.25)**2 +
            ((merk[:, 1]+.36)/.14)**2 + ((merk[:, 2]-.715)/.055)**2 <= 1)
        renk[sap] = np.array(hex_renk("#624027")[:3])
        renk[yaprak] = np.array(hex_renk("#3c792d")[:3])
        maske[sap | yaprak] = 0
    elif ORANGE:
        # Beyaz albedo, on dilimli zarlar ve merkezde acik oz.
        renk = np.tile(np.array(hex_renk("#f77b16")[:3]), (k, 1))
        renk[u[:, 0] > .80] = np.array(hex_renk("#f1ebd5")[:3])
        renk[u[:, 0] > .94] = np.array(hex_renk("#e87916")[:3])
        aci = np.arctan2(merk[:, 2], merk[:, 1])
        zar = (np.cos(10*aci) > .985) & (u[:, 0] < .80)
        renk[zar] = np.array(hex_renk("#fff0cd")[:3])
        renk[u[:, 0] < .10] = np.array(hex_renk("#ffefd1")[:3])
        kaliks = (merk[:, 0]**2 + merk[:, 1]**2 <= .21**2) & (merk[:, 2] >= .70)
        renk[kaliks] = np.array(hex_renk("#396a2e")[:3])
        maske[kaliks] = 0
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
    sag = XMIN + (idx[:, 0] + 1) * ((XMAX - XMIN) / gx)
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
    if ANANAS:
        for ad_, veri in (("ananas_tac", tac.astype(float)), ("ananas_sap", sap.astype(float)), ("ananas_goz", goz)):
            at_ = me.attributes.new(ad_, "FLOAT", "POINT")
            at_.data.foreach_set("value", np.asarray(veri, dtype=np.float32))
    at_ = me.attributes.new("renk", "FLOAT_COLOR", "POINT")
    at_.data.foreach_set("color", np.hstack([renk, np.ones((k, 1))]).ravel().astype(np.float32))
    if KARPUZ or KIVI or ANANAS or APPLE or ORANGE or BANANA or PEACH or NAR or TOMATO or CUCUMBER:
        at_ = me.attributes.new("kaynak", "FLOAT_VECTOR", "POINT")
        at_.data.foreach_set("vector", merk.ravel().astype(np.float32))
    if NAR or TOMATO:
        at_ = me.attributes.new("ek_mask", "FLOAT", "POINT")
        at_.data.foreach_set("value", (crown if NAR else calyx).astype(np.float32))
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
    karis.inputs[7].default_value = hex_renk("#b71f29" if CILEK else ("#c93225" if APPLE else ("#e87916" if ORANGE else ("#e7c137" if BANANA else ("#356d2c" if CUCUMBER else ("#c3221a" if PEPPER else ("#d95c4d" if PEACH else ("#8c1c27" if NAR else ("#c7231d" if TOMATO else "#21361a")))))))))
    if CILEK:
        # Sadece maskelenmis dis yuz; kesik et yuzunde aken bulunmaz.
        geometri = ntk.nodes.new("ShaderNodeNewGeometry")
        cilek_aken(ntk, geometri.outputs["Position"], karis.outputs[2], bk, dis_maske=bitv)
    elif ANANAS:
        a_goz = ntk.nodes.new("ShaderNodeAttribute"); a_goz.attribute_type = "INSTANCER"; a_goz.attribute_name = "ananas_goz"
        a_tac = ntk.nodes.new("ShaderNodeAttribute"); a_tac.attribute_type = "INSTANCER"; a_tac.attribute_name = "ananas_tac"
        a_sap = ntk.nodes.new("ShaderNodeAttribute"); a_sap.attribute_type = "INSTANCER"; a_sap.attribute_name = "ananas_sap"
        goz_r = ntk.nodes.new("ShaderNodeValToRGB")
        goz_r.color_ramp.elements[0].color = hex_renk("#51452c")
        goz_r.color_ramp.elements[1].color = hex_renk("#e2b449")
        for pos, col in ((.25, "#708044"), (.55, "#a98238"), (.82, "#c9973b")):
            el = goz_r.color_ramp.elements.new(pos); el.color = hex_renk(col)
        baglan(ntk, a_goz.outputs["Fac"], goz_r.inputs["Fac"])
        kab = ntk.nodes.new("ShaderNodeMix"); kab.data_type = "RGBA"
        baglan(ntk, bitv, kab.inputs["Factor"])
        baglan(ntk, a_r.outputs["Color"], kab.inputs[6])
        baglan(ntk, goz_r.outputs["Color"], kab.inputs[7])
        yap = ntk.nodes.new("ShaderNodeMix"); yap.data_type = "RGBA"
        baglan(ntk, a_tac.outputs["Fac"], yap.inputs["Factor"])
        baglan(ntk, kab.outputs[2], yap.inputs[6])
        yap_doku = ntk.nodes.new("ShaderNodeTexNoise")
        yap_doku.inputs["Scale"].default_value = 24.0
        yap_doku.inputs["Detail"].default_value = 2.0
        baglan(ntk, tkk.outputs["Generated"], yap_doku.inputs["Vector"])
        yap_renk = ntk.nodes.new("ShaderNodeValToRGB")
        yap_renk.color_ramp.elements[0].color = hex_renk("#28572c")
        yap_renk.color_ramp.elements[1].color = hex_renk("#5e9b45")
        baglan(ntk, yap_doku.outputs["Fac"], yap_renk.inputs["Fac"])
        baglan(ntk, yap_renk.outputs["Color"], yap.inputs[7])
        sap_mix = ntk.nodes.new("ShaderNodeMix"); sap_mix.data_type = "RGBA"
        baglan(ntk, a_sap.outputs["Fac"], sap_mix.inputs["Factor"])
        baglan(ntk, yap.outputs[2], sap_mix.inputs[6])
        baglan(ntk, a_r.outputs["Color"], sap_mix.inputs[7])
        baglan(ntk, sap_mix.outputs[2], bk.inputs["Base Color"])
    elif APPLE or ORANGE or PEACH or NAR or TOMATO or CUCUMBER:
        # Iri ilk tur kuplerinin kesik yuzlerinde gercek kaynak konumundaki
        # cekirdek evi veya portakal dilim zari gorunsun; her kupe ayni etiket basma.
        kaynak = ntk.nodes.new("ShaderNodeAttribute")
        kaynak.attribute_type="INSTANCER"; kaynak.attribute_name="kaynak"
        uv=ntk.nodes.new("ShaderNodeSeparateXYZ")
        baglan(ntk,tkk.outputs["Generated"],uv.inputs[0])
        src=ntk.nodes.new("ShaderNodeSeparateXYZ")
        baglan(ntk,kaynak.outputs["Vector"],src.inputs[0])
        def pos_eks(i,half):
            d=matematik(ntk,"MULTIPLY",matematik(ntk,"SUBTRACT",uv.outputs[i],None,deger_b=.5),
                       None,deger_b=2*half*.94)
            return matematik(ntk,"ADD",src.outputs[i],d)
        ox,oy,oz=pos_eks(0,hx),pos_eks(1,hy),pos_eks(2,hz)
        rad_=matematik(ntk,"SQRT",matematik(ntk,"ADD",matematik(ntk,"MULTIPLY",oy,oy),
                       matematik(ntk,"MULTIPLY",oz,oz)))
        u_src=matematik(ntk,"DIVIDE",rad_,None,deger_b=R)
        angle=matematik(ntk,"ARCTAN2",oz,oy)
        if NAR:
            bead=ntk.nodes.new("ShaderNodeTexVoronoi")
            bead.inputs["Scale"].default_value=34.0
            comb=ntk.nodes.new("ShaderNodeCombineXYZ")
            for axis,value in zip(("X","Y","Z"),(ox,oy,oz)):
                baglan(ntk,value,comb.inputs[axis])
            baglan(ntk,comb.outputs[0],bead.inputs["Vector"])
            ar=ntk.nodes.new("ShaderNodeValToRGB")
            ar.color_ramp.elements[0].color=hex_renk("#e24758")
            ar.color_ramp.elements[1].color=hex_renk("#7a1025")
            baglan(ntk,bead.outputs["Distance"],ar.inputs["Fac"])
            membr=matematik(ntk,"GREATER_THAN",
                matematik(ntk,"COSINE",matematik(ntk,"MULTIPLY",angle,None,deger_b=5.0)),
                None,deger_b=.93)
            pith=matematik(ntk,"MULTIPLY",
                matematik(ntk,"GREATER_THAN",u_src,None,deger_b=.77),
                matematik(ntk,"LESS_THAN",u_src,None,deger_b=.90))
            white=matematik(ntk,"MAXIMUM",membr,pith)
            wm=ntk.nodes.new("ShaderNodeMix");wm.data_type="RGBA"
            baglan(ntk,white,wm.inputs["Factor"])
            baglan(ntk,ar.outputs["Color"],wm.inputs[6])
            wm.inputs[7].default_value=hex_renk("#f2e9d6")
            skin=ntk.nodes.new("ShaderNodeMix");skin.data_type="RGBA"
            baglan(ntk,bitv,skin.inputs["Factor"])
            baglan(ntk,wm.outputs[2],skin.inputs[6])
            skin.inputs[7].default_value=hex_renk("#8c1c27")
            result=skin.outputs[2]
        elif TOMATO:
            chambers=matematik(ntk,"COSINE",matematik(ntk,"MULTIPLY",angle,None,deger_b=5.0))
            gel=matematik(ntk,"MULTIPLY",
                matematik(ntk,"LESS_THAN",u_src,None,deger_b=.72),
                matematik(ntk,"LESS_THAN",chambers,None,deger_b=.80))
            gm=ntk.nodes.new("ShaderNodeMix");gm.data_type="RGBA"
            baglan(ntk,gel,gm.inputs["Factor"])
            baglan(ntk,karis.outputs[2],gm.inputs[6])
            gm.inputs[7].default_value=hex_renk("#e9472e")
            seedwave=matematik(ntk,"COSINE",matematik(ntk,"ADD",
                matematik(ntk,"MULTIPLY",angle,None,deger_b=37.0),
                matematik(ntk,"MULTIPLY",ox,None,deger_b=23.0)))
            seed=matematik(ntk,"MULTIPLY",gel,
                matematik(ntk,"MULTIPLY",
                    matematik(ntk,"GREATER_THAN",u_src,None,deger_b=.24),
                    matematik(ntk,"MULTIPLY",
                        matematik(ntk,"LESS_THAN",u_src,None,deger_b=.62),
                        matematik(ntk,"GREATER_THAN",seedwave,None,deger_b=.91))))
            sm=ntk.nodes.new("ShaderNodeMix");sm.data_type="RGBA"
            baglan(ntk,seed,sm.inputs["Factor"])
            baglan(ntk,gm.outputs[2],sm.inputs[6])
            sm.inputs[7].default_value=hex_renk("#f8df9c")
            result=sm.outputs[2]
        elif PEACH:
            xp=matematik(ntk,"DIVIDE",ox,None,deger_b=.40*A)
            yp=matematik(ntk,"DIVIDE",oy,None,deger_b=.38*R)
            zp=matematik(ntk,"DIVIDE",oz,None,deger_b=.44*R)
            core=matematik(ntk,"ADD",matematik(ntk,"MULTIPLY",xp,xp),
                matematik(ntk,"ADD",matematik(ntk,"MULTIPLY",yp,yp),
                    matematik(ntk,"MULTIPLY",zp,zp)))
            rough=matematik(ntk,"SINE",matematik(ntk,"ADD",
                matematik(ntk,"MULTIPLY",ox,None,deger_b=17.0),
                matematik(ntk,"MULTIPLY",oz,None,deger_b=12.0)))
            threshold=matematik(ntk,"ADD",None,
                matematik(ntk,"MULTIPLY",rough,None,deger_b=.14),deger_a=1.0)
            pit=matematik(ntk,"LESS_THAN",core,threshold)
            pm=ntk.nodes.new("ShaderNodeMix");pm.data_type="RGBA"
            baglan(ntk,pit,pm.inputs["Factor"])
            baglan(ntk,karis.outputs[2],pm.inputs[6])
            pm.inputs[7].default_value=hex_renk("#80502d")
            baglan(ntk,pm.outputs[2],bk.inputs["Base Color"])
        elif APPLE:
            star=matematik(ntk,"COSINE",matematik(ntk,"MULTIPLY",angle,None,deger_b=5.0))
            inside=matematik(ntk,"MULTIPLY",matematik(ntk,"LESS_THAN",u_src,None,deger_b=.38),
                matematik(ntk,"LESS_THAN",matematik(ntk,"ABSOLUTE",ox),None,deger_b=.43*A))
            chamber=matematik(ntk,"MULTIPLY",inside,
                matematik(ntk,"MULTIPLY",matematik(ntk,"GREATER_THAN",star,None,deger_b=.28),
                    matematik(ntk,"GREATER_THAN",u_src,None,deger_b=.15)))
            seed=matematik(ntk,"MULTIPLY",chamber,
                matematik(ntk,"MULTIPLY",matematik(ntk,"GREATER_THAN",star,None,deger_b=.82),
                    matematik(ntk,"GREATER_THAN",u_src,None,deger_b=.22)))
            m1=ntk.nodes.new("ShaderNodeMix");m1.data_type="RGBA"
            baglan(ntk,chamber,m1.inputs["Factor"]);baglan(ntk,karis.outputs[2],m1.inputs[6])
            m1.inputs[7].default_value=hex_renk("#ddcfb0")
            m2=ntk.nodes.new("ShaderNodeMix");m2.data_type="RGBA"
            baglan(ntk,seed,m2.inputs["Factor"]);baglan(ntk,m1.outputs[2],m2.inputs[6])
            m2.inputs[7].default_value=hex_renk("#55351e")
            baglan(ntk,m2.outputs[2],bk.inputs["Base Color"])
        elif ORANGE:
            membrane=matematik(ntk,"MULTIPLY",matematik(ntk,"GREATER_THAN",
                matematik(ntk,"COSINE",matematik(ntk,"MULTIPLY",angle,None,deger_b=10.0)),
                None,deger_b=.98),matematik(ntk,"LESS_THAN",u_src,None,deger_b=.80))
            albedo=matematik(ntk,"MULTIPLY",matematik(ntk,"GREATER_THAN",u_src,None,deger_b=.80),
                matematik(ntk,"LESS_THAN",u_src,None,deger_b=.94))
            white=matematik(ntk,"MAXIMUM",membrane,albedo)
            m1=ntk.nodes.new("ShaderNodeMix");m1.data_type="RGBA"
            baglan(ntk,white,m1.inputs["Factor"]);baglan(ntk,karis.outputs[2],m1.inputs[6])
            m1.inputs[7].default_value=hex_renk("#fff0d0")
            baglan(ntk,m1.outputs[2],bk.inputs["Base Color"])
        elif CUCUMBER:
            seedwave=matematik(ntk,"COSINE",matematik(ntk,"ADD",
                matematik(ntk,"MULTIPLY",angle,None,deger_b=11.0),
                matematik(ntk,"MULTIPLY",ox,None,deger_b=15.0)))
            seed=matematik(ntk,"MULTIPLY",
                matematik(ntk,"GREATER_THAN",seedwave,None,deger_b=.95),
                matematik(ntk,"MULTIPLY",
                    matematik(ntk,"GREATER_THAN",u_src,None,deger_b=.18),
                    matematik(ntk,"MULTIPLY",
                        matematik(ntk,"LESS_THAN",u_src,None,deger_b=.40),
                        matematik(ntk,"SUBTRACT",None,bitv,deger_a=1.0))))
            sm=ntk.nodes.new("ShaderNodeMix");sm.data_type="RGBA"
            baglan(ntk,seed,sm.inputs["Factor"])
            baglan(ntk,karis.outputs[2],sm.inputs[6])
            sm.inputs[7].default_value=hex_renk("#f8f2cd")
            baglan(ntk,sm.outputs[2],bk.inputs["Base Color"])
        if NAR or TOMATO:
            ek=ntk.nodes.new("ShaderNodeAttribute")
            ek.attribute_type="INSTANCER";ek.attribute_name="ek_mask"
            em=ntk.nodes.new("ShaderNodeMix");em.data_type="RGBA"
            baglan(ntk,ek.outputs["Fac"],em.inputs["Factor"])
            baglan(ntk,result,em.inputs[6])
            baglan(ntk,a_r.outputs["Color"],em.inputs[7])
            baglan(ntk,em.outputs[2],bk.inputs["Base Color"])
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
    t_k.inputs[7].default_value = hex_renk("#60452f" if KIVI else ("#143c27" if KARPUZ else ("#b71f29" if CILEK else ("#c93225" if APPLE else ("#e87916" if ORANGE else ("#356d2c" if CUCUMBER else ("#c3221a" if PEPPER else "#21361a")))))))
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
    if (ANANAS or APPLE or ORANGE or BANANA or NAR or TOMATO or CUCUMBER or PEPPER) and ad == "kes_x":
        for tree in ANANAS_EK_NT:
            node = tree.nodes["kes_x"]
            node.outputs[0].default_value = deger
            node.outputs[0].keyframe_insert("default_value", frame=kare(t))


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
    for parca in ANANAS_EK_OB:
        parca.hide_render = False
        parca.keyframe_insert("hide_render", frame=kare(bas))
    for t_, dz_, sxy, sz in DUSUS_ANAHTAR:
        meyve.scale = (sxy, sxy, sz)
        meyve.location = (0, 0, MERKEZ_Z + dz_ - R * (1 - sz))  # ezilmede alt yuzey tahtada kalir
        meyve.keyframe_insert("scale", frame=kare(bas + t_))
        meyve.keyframe_insert("location", frame=kare(bas + t_))
    meyve.keyframe_insert("scale", frame=kare(ks))  # tur boyunca sabit
    meyve.keyframe_insert("location", frame=kare(ks))
    meyve.hide_render = True
    meyve.keyframe_insert("hide_render", frame=kare(ks + 0.02))
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
    for parca in ANANAS_EK_OB:
        parca.hide_render = True
        parca.keyframe_insert("hide_render", frame=kare(ks + 0.02))
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
            # Son dilim kalan tac ucunu da tasir; ayni anda butun kaynak
            # geometri kesilirken o dilimin yesil kupleri yigina katilir.
            bitis_x = XMAX + 0.01 if (ANANAS or BANANA or CUCUMBER) and i == len(vl) - 1 else konum
            deger_anahtar("kes_x", t, bitis_x)
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
if kivi_tuy_nt is not None:
    sabit_interp(kivi_tuy_nt)
for tree in ANANAS_EK_NT:
    sabit_interp(tree)
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
if KARPUZ or KIVI:
    kesit_koordinat = ntk_.nodes.new("ShaderNodeTexCoord")
    baglan(ntk_, kesit_koordinat.outputs["Object"], ay_.inputs[0])
else:
    baglan(ntk_, gp.outputs["Position"], ay_.inputs[0])
v_r = ntk_.nodes.new("ShaderNodeValue"); v_r.name = "kesit_r"; v_r.outputs[0].default_value = 1.0
v_x = ntk_.nodes.new("ShaderNodeValue"); v_x.name = "kesit_x"; v_x.outputs[0].default_value = 0.0
dy = matematik(ntk_, "MULTIPLY", ay_.outputs[1], v_r.outputs[0]) if (KARPUZ or KIVI) else ay_.outputs[1]
dz = (matematik(ntk_, "MULTIPLY", ay_.outputs[2], v_r.outputs[0]) if (KARPUZ or KIVI) else
      matematik(ntk_, "SUBTRACT", ay_.outputs[2], None, deger_b=MERKEZ_Z))
if BANANA or CUCUMBER:
    xu = matematik(ntk_, "DIVIDE", v_x.outputs[0], None, deger_b=A)
    curve = matematik(ntk_, "SUBTRACT",
        matematik(ntk_, "MULTIPLY", xu, xu, deger_b=.30 if BANANA else .085),
        None, deger_b=.12 if BANANA else .035)
    dz = matematik(ntk_, "SUBTRACT", dz, curve)
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
elif PEPPER:
    zn=matematik(ntk_,"DIVIDE",dz,None,deger_b=R)
    s=matematik(ntk_,"MULTIPLY",matematik(ntk_,"ADD",zn,None,deger_b=1.0),None,deger_b=.5)
    decay=matematik(ntk_,"ADD",None,
        matematik(ntk_,"MULTIPLY",s,None,deger_b=-.12),deger_a=.92)
    bulge=matematik(ntk_,"MULTIPLY",
        matematik(ntk_,"SINE",matematik(ntk_,"MULTIPLY",s,None,deger_b=math.pi)),None,deger_b=.15)
    s4=matematik(ntk_,"POWER",s,None,deger_b=4.0)
    base=matematik(ntk_,"SUBTRACT",matematik(ntk_,"ADD",decay,bulge),
        matematik(ntk_,"MULTIPLY",s4,None,deger_b=.15))
    taper=matematik(ntk_,"POWER",matematik(ntk_,"MAXIMUM",
        matematik(ntk_,"SUBTRACT",None,
            matematik(ntk_,"POWER",matematik(ntk_,"ABSOLUTE",zn),None,deger_b=8.0),deger_a=1.0),
        None,deger_b=0.0),None,deger_b=.23)
    body=matematik(ntk_,"MULTIPLY",base,taper)
    xx=matematik(ntk_,"DIVIDE",v_x.outputs[0],None,deger_b=A)
    yy=matematik(ntk_,"DIVIDE",dy,None,deger_b=B)
    theta=matematik(ntk_,"ARCTAN2",yy,xx)
    lob=matematik(ntk_,"ADD",None,
        matematik(ntk_,"MULTIPLY",
            matematik(ntk_,"COSINE",matematik(ntk_,"MULTIPLY",theta,None,deger_b=4.0)),
            None,deger_b=-.14),deger_a=1.0)
    shape=matematik(ntk_,"MAXIMUM",matematik(ntk_,"MULTIPLY",body,lob),None,deger_b=.001)
    radial_xy=matematik(ntk_,"SQRT",matematik(ntk_,"ADD",
        matematik(ntk_,"MULTIPLY",xx,xx),matematik(ntk_,"MULTIPLY",yy,yy)))
    u_=matematik(ntk_,"DIVIDE",radial_xy,shape)
else:
    u_ = matematik(ntk_, "DIVIDE", rad, v_r.outputs[0])
et_r = ntk_.nodes.new("ShaderNodeValToRGB")
if KARPUZ:
    et_r.color_ramp.elements[0].color = hex_renk("#e84244")
    et_r.color_ramp.elements[1].position = 1.0
    et_r.color_ramp.elements[1].color = hex_renk("#143c27")
    for pos, renk_ in ((0.72, "#d92730"), (0.78, "#ee7773"), (0.81, "#f8efdc"),
                       (0.90, "#ebedd5"), (0.965, "#a2c891"), (0.985, "#1d4a2d")):
        el = et_r.color_ramp.elements.new(pos); el.color = hex_renk(renk_)
elif ANANAS:
    et_r.color_ramp.elements[0].color = hex_renk("#f8e9a2")
    et_r.color_ramp.elements[1].position = 1.0
    et_r.color_ramp.elements[1].color = hex_renk("#594925")
    for pos, col in ((.28, "#f3dfa0"), (.82, "#eec95f"), (.95, "#aa8140")):
        el = et_r.color_ramp.elements.new(pos); el.color = hex_renk(col)
elif APPLE:
    et_r.color_ramp.elements[0].color = hex_renk("#f5efdc")
    et_r.color_ramp.elements[1].color = hex_renk("#c93225")
    for pos,col in ((.87,"#f1ead5"),(.94,"#e5b78a"),(.98,"#bf3326")):
        e=et_r.color_ramp.elements.new(pos); e.color=hex_renk(col)
elif ORANGE:
    et_r.color_ramp.elements[0].color = hex_renk("#fff0d4")
    et_r.color_ramp.elements[1].color = hex_renk("#dd6812")
    for pos,col in ((.11,"#fa8b23"),(.78,"#f77b16"),(.83,"#f7efdb"),(.94,"#f4e8ce"),(.96,"#e97816")):
        e=et_r.color_ramp.elements.new(pos); e.color=hex_renk(col)
elif BANANA:
    et_r.color_ramp.elements[0].color = hex_renk("#f8efd5")
    et_r.color_ramp.elements[1].color = hex_renk("#ddb431")
    for pos,col in ((.82,"#f8efd5"),(.86,"#f5e6ad"),(.94,"#f5e6ad"),(.955,"#e8c43a")):
        e=et_r.color_ramp.elements.new(pos); e.color=hex_renk(col)
elif CUCUMBER:
    et_r.color_ramp.elements[0].color=hex_renk("#e5edc4")
    et_r.color_ramp.elements[1].color=hex_renk("#295e29")
    for pos,col in ((.42,"#e5edc4"),(.84,"#d1e1a8"),(.94,"#a9c77e"),(.955,"#356d2c")):
        e=et_r.color_ramp.elements.new(pos);e.color=hex_renk(col)
elif PEPPER:
    et_r.color_ramp.elements[0].color=hex_renk("#f2dfaa")
    et_r.color_ramp.elements[1].color=hex_renk("#b51d1b")
    for pos,col in ((.68,"#8d231e"),(.73,"#ed8b53"),(.90,"#dc5130"),(.96,"#c3221a")):
        e=et_r.color_ramp.elements.new(pos);e.color=hex_renk(col)
elif PEACH:
    et_r.color_ramp.elements[0].color = hex_renk("#f8ba64")
    et_r.color_ramp.elements[1].color = hex_renk("#cf514d")
    for pos,col in ((.39,"#efa561"),(.84,"#f4bd68"),(.96,"#e47c55")):
        e=et_r.color_ramp.elements.new(pos); e.color=hex_renk(col)
elif NAR:
    et_r.color_ramp.elements[0].color=hex_renk("#d23347")
    et_r.color_ramp.elements[1].color=hex_renk("#781421")
    for pos,col in ((.78,"#cc2639"),(.80,"#f2e9d6"),(.90,"#eee1cc"),(.91,"#9d2730")):
        e=et_r.color_ramp.elements.new(pos);e.color=hex_renk(col)
elif TOMATO:
    et_r.color_ramp.elements[0].color=hex_renk("#e94a30")
    et_r.color_ramp.elements[1].color=hex_renk("#b81e1c")
    for pos,col in ((.7,"#e44b2e"),(.76,"#cf3726"),(.94,"#d1261d")):
        e=et_r.color_ramp.elements.new(pos);e.color=hex_renk(col)
else:
    et_r.color_ramp.elements[0].color = hex_renk("#fff1e5" if CILEK else "#f1e9b8")
    et_r.color_ramp.elements[1].position = 0.97
    et_r.color_ramp.elements[1].color = hex_renk("#a81722" if CILEK else "#a8cc5c")
    e_m = et_r.color_ramp.elements.new(0.42 if CILEK else 0.6); e_m.color = hex_renk("#f7a7ab" if CILEK else "#e3e08e")
if CILEK:
    e_r = et_r.color_ramp.elements.new(0.82); e_r.color = hex_renk("#d52b36")
elif not KARPUZ and not ANANAS and not APPLE and not ORANGE and not BANANA and not PEACH and not NAR and not TOMATO and not CUCUMBER:
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
elif ANANAS:
    # Uzunlamasina lifler kesitte radyal acik izler olarak gorunur.
    aci_ = matematik(ntk_, "ARCTAN2", dz, dy)
    dalga_ = matematik(ntk_, "COSINE", matematik(ntk_, "ADD",
        matematik(ntk_, "MULTIPLY", aci_, None, deger_b=38.0),
        matematik(ntk_, "MULTIPLY", v_x.outputs[0], None, deger_b=5.0)))
    lif_ = matematik(ntk_, "MULTIPLY", matematik(ntk_, "GREATER_THAN", dalga_, None, deger_b=.89),
        matematik(ntk_, "MULTIPLY", matematik(ntk_, "GREATER_THAN", u_, None, deger_b=.28),
            matematik(ntk_, "LESS_THAN", u_, None, deger_b=.89)))
    lif_mix = ntk_.nodes.new("ShaderNodeMix"); lif_mix.data_type = "RGBA"
    baglan(ntk_, lif_, lif_mix.inputs["Factor"])
    baglan(ntk_, et_r.outputs["Color"], lif_mix.inputs[6])
    lif_mix.inputs[7].default_value = hex_renk("#fff2b8")
    baglan(ntk_, lif_mix.outputs[2], bk_.inputs["Base Color"])
elif APPLE:
    angle = matematik(ntk_, "ARCTAN2", dz, dy)
    star = matematik(ntk_, "COSINE", matematik(ntk_, "MULTIPLY", angle, None, deger_b=5.0))
    core = matematik(ntk_, "MULTIPLY", matematik(ntk_, "LESS_THAN", u_, None, deger_b=.38),
        matematik(ntk_, "LESS_THAN", matematik(ntk_, "ABSOLUTE", v_x.outputs[0]), None, deger_b=.43*A))
    chamber = matematik(ntk_, "MULTIPLY", core,
        matematik(ntk_, "MULTIPLY", matematik(ntk_, "GREATER_THAN", star, None, deger_b=.28),
            matematik(ntk_, "GREATER_THAN", u_, None, deger_b=.15)))
    seed = matematik(ntk_, "MULTIPLY", chamber,
        matematik(ntk_, "MULTIPLY", matematik(ntk_, "GREATER_THAN", star, None, deger_b=.82),
            matematik(ntk_, "GREATER_THAN", u_, None, deger_b=.22)))
    cm=ntk_.nodes.new("ShaderNodeMix"); cm.data_type="RGBA"
    baglan(ntk_,chamber,cm.inputs["Factor"]); baglan(ntk_,et_r.outputs["Color"],cm.inputs[6])
    cm.inputs[7].default_value=hex_renk("#ddcfb0")
    sm=ntk_.nodes.new("ShaderNodeMix"); sm.data_type="RGBA"
    baglan(ntk_,seed,sm.inputs["Factor"]); baglan(ntk_,cm.outputs[2],sm.inputs[6])
    sm.inputs[7].default_value=hex_renk("#55351e")
    baglan(ntk_,sm.outputs[2],bk_.inputs["Base Color"])
elif ORANGE:
    angle=matematik(ntk_,"ARCTAN2",dz,dy)
    ten=matematik(ntk_,"COSINE",matematik(ntk_,"MULTIPLY",angle,None,deger_b=10.0))
    membr=matematik(ntk_,"MULTIPLY",matematik(ntk_,"GREATER_THAN",ten,None,deger_b=.98),
        matematik(ntk_,"LESS_THAN",u_,None,deger_b=.80))
    seg=ntk_.nodes.new("ShaderNodeMix"); seg.data_type="RGBA"
    baglan(ntk_,membr,seg.inputs["Factor"]); baglan(ntk_,et_r.outputs["Color"],seg.inputs[6])
    seg.inputs[7].default_value=hex_renk("#fff2d6")
    baglan(ntk_,seg.outputs[2],bk_.inputs["Base Color"])
elif BANANA:
    seed_pattern = matematik(ntk_, "COSINE", matematik(ntk_, "MULTIPLY",
        matematik(ntk_, "ARCTAN2", dz, dy), None, deger_b=18.0))
    seed = matematik(ntk_, "MULTIPLY",
        matematik(ntk_, "LESS_THAN", u_, None, deger_b=.14),
        matematik(ntk_, "GREATER_THAN", seed_pattern, None, deger_b=.93))
    sm=ntk_.nodes.new("ShaderNodeMix"); sm.data_type="RGBA"
    baglan(ntk_,seed,sm.inputs["Factor"])
    baglan(ntk_,et_r.outputs["Color"],sm.inputs[6])
    sm.inputs[7].default_value=hex_renk("#846849")
    baglan(ntk_,sm.outputs[2],bk_.inputs["Base Color"])
elif CUCUMBER:
    angle=matematik(ntk_,"ARCTAN2",dz,dy)
    wave=matematik(ntk_,"COSINE",matematik(ntk_,"ADD",
        matematik(ntk_,"MULTIPLY",angle,None,deger_b=11.0),
        matematik(ntk_,"MULTIPLY",v_x.outputs[0],None,deger_b=15.0)))
    seed=matematik(ntk_,"MULTIPLY",
        matematik(ntk_,"GREATER_THAN",wave,None,deger_b=.95),
        matematik(ntk_,"MULTIPLY",
            matematik(ntk_,"GREATER_THAN",u_,None,deger_b=.18),
            matematik(ntk_,"LESS_THAN",u_,None,deger_b=.40)))
    sm=ntk_.nodes.new("ShaderNodeMix");sm.data_type="RGBA"
    baglan(ntk_,seed,sm.inputs["Factor"])
    baglan(ntk_,et_r.outputs["Color"],sm.inputs[6])
    sm.inputs[7].default_value=hex_renk("#f8f2cd")
    baglan(ntk_,sm.outputs[2],bk_.inputs["Base Color"])
elif PEPPER:
    baglan(ntk_,et_r.outputs["Color"],bk_.inputs["Base Color"])
elif PEACH:
    # Merkezde tek, pütürlü taş çekirdeğin YZ kesişimi.
    xfac=matematik(ntk_,"DIVIDE",v_x.outputs[0],None,deger_b=.40*A)
    ry=matematik(ntk_,"DIVIDE",dy,None,deger_b=.38*R)
    rz=matematik(ntk_,"DIVIDE",dz,None,deger_b=.44*R)
    pit2=matematik(ntk_,"ADD",matematik(ntk_,"MULTIPLY",xfac,xfac),
        matematik(ntk_,"ADD",matematik(ntk_,"MULTIPLY",ry,ry),matematik(ntk_,"MULTIPLY",rz,rz)))
    pit=matematik(ntk_,"LESS_THAN",pit2,None,deger_b=1.0)
    pm=ntk_.nodes.new("ShaderNodeMix");pm.data_type="RGBA"
    baglan(ntk_,pit,pm.inputs["Factor"])
    baglan(ntk_,et_r.outputs["Color"],pm.inputs[6])
    pm.inputs[7].default_value=hex_renk("#895330")
    baglan(ntk_,pm.outputs[2],bk_.inputs["Base Color"])
elif NAR:
    ang=matematik(ntk_,"ARCTAN2",dz,dy)
    membrane=matematik(ntk_,"MULTIPLY",
        matematik(ntk_,"GREATER_THAN",
            matematik(ntk_,"COSINE",matematik(ntk_,"MULTIPLY",ang,None,deger_b=5.0)),
            None,deger_b=.94),
        matematik(ntk_,"LESS_THAN",u_,None,deger_b=.78))
    wm=ntk_.nodes.new("ShaderNodeMix");wm.data_type="RGBA"
    baglan(ntk_,membrane,wm.inputs["Factor"])
    baglan(ntk_,et_r.outputs["Color"],wm.inputs[6])
    wm.inputs[7].default_value=hex_renk("#f2e9d6")
    baglan(ntk_,wm.outputs[2],bk_.inputs["Base Color"])
elif TOMATO:
    ang=matematik(ntk_,"ARCTAN2",dz,dy)
    wave=matematik(ntk_,"COSINE",matematik(ntk_,"ADD",
        matematik(ntk_,"MULTIPLY",ang,None,deger_b=37.0),
        matematik(ntk_,"MULTIPLY",v_x.outputs[0],None,deger_b=23.0)))
    seed=matematik(ntk_,"MULTIPLY",
        matematik(ntk_,"GREATER_THAN",wave,None,deger_b=.91),
        matematik(ntk_,"MULTIPLY",
            matematik(ntk_,"GREATER_THAN",u_,None,deger_b=.24),
            matematik(ntk_,"LESS_THAN",u_,None,deger_b=.62)))
    sm=ntk_.nodes.new("ShaderNodeMix");sm.data_type="RGBA"
    baglan(ntk_,seed,sm.inputs["Factor"])
    baglan(ntk_,et_r.outputs["Color"],sm.inputs[6])
    sm.inputs[7].default_value=hex_renk("#f7de9e")
    baglan(ntk_,sm.outputs[2],bk_.inputs["Base Color"])
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
if PEPPER:
    outside_z=matematik(ntk_,"GREATER_THAN",matematik(ntk_,"ABSOLUTE",dz),None,deger_b=R)
    cavity=matematik(ntk_,"MULTIPLY",
        matematik(ntk_,"LESS_THAN",u_,None,deger_b=.72),
        matematik(ntk_,"MULTIPLY",
            matematik(ntk_,"GREATER_THAN",dz,None,deger_b=-.62*R),
            matematik(ntk_,"LESS_THAN",dz,None,deger_b=.85*R)))
    pith=matematik(ntk_,"MULTIPLY",
        matematik(ntk_,"LESS_THAN",u_,None,deger_b=.18),
        matematik(ntk_,"GREATER_THAN",dz,None,deger_b=-.22))
    cavity=matematik(ntk_,"MULTIPLY",cavity,matematik(ntk_,"SUBTRACT",None,pith,deger_a=1.0))
    _dis=matematik(ntk_,"MAXIMUM",_dis,matematik(ntk_,"MAXIMUM",outside_z,cavity))
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
    kesit.keyframe_insert("hide_render", frame=kare(xk[-1][0] + 0.02))
    for t, konum in xk:
        if (ANANAS or BANANA or CUCUMBER) and konum >= A:
            kesit.hide_render = True
            kesit.keyframe_insert("hide_render", frame=kare(t))
        r_ = 1.0 if (CILEK or PEPPER) else float(profil_r(np.array([konum]))[0]) * 0.995
        # Yalniz kalan govdenin yeni kesim duzlemine bagli; hicbir nesnede
        # kameraya/yone dogru ayrik bir on yuz konumlandirilmaz.
        kesit.location = (konum + 0.002, 0, MERKEZ_Z + (float(muz_egri(konum,M)) if BANANA else (float(salatalik_egri(konum,M)) if CUCUMBER else 0.0)))
        kesit.scale = (1, r_, r_)
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
