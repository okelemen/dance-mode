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
TAHTA_UST = 0.14
MERKEZ_Z = TAHTA_UST + R - 0.03
GORSEL_TAVAN = 120  # gorsel kup izgarasi eksen basina en fazla (sayi plandaki gercek degerdir)


def hex_renk(h, a=1.0):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((x / 12.92) if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4) for x in c) + (a,)


def kare(t):
    return t * FPS + 1.0


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
dunya.node_tree.nodes["Background"].inputs[0].default_value = hex_renk("#9a9a9a")
dunya.node_tree.nodes["Background"].inputs[1].default_value = 0.6


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


# ---------------------------------------------------------------- zemin (koyu fayans)
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0))
zemin = bpy.context.object
m, nt, bsdf = malzeme("fayans")
tk = nt.nodes.new("ShaderNodeTexCoord")
br = nt.nodes.new("ShaderNodeTexBrick")
br.inputs["Scale"].default_value = 0.55
br.inputs["Mortar Size"].default_value = 0.012
br.inputs["Color1"].default_value = hex_renk("#3b3b3d")
br.inputs["Color2"].default_value = hex_renk("#2d2d2f")
br.inputs["Mortar"].default_value = hex_renk("#151515")
br.offset = 0.0
baglan(nt, tk.outputs["Object"], br.inputs["Vector"])
baglan(nt, br.outputs["Color"], bsdf.inputs["Base Color"])
bsdf.inputs["Roughness"].default_value = 0.35
zemin.data.materials.append(m)

# ---------------------------------------------------------------- duvar (acik gri siva)
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 4.2, 5), rotation=(math.radians(90), 0, 0))
duvar = bpy.context.object
m, nt, bsdf = malzeme("duvar")
nz = nt.nodes.new("ShaderNodeTexNoise")
nz.inputs["Scale"].default_value = 18
rmp = nt.nodes.new("ShaderNodeValToRGB")
rmp.color_ramp.elements[0].color = hex_renk("#a9a9a9")
rmp.color_ramp.elements[1].color = hex_renk("#c4c4c4")
baglan(nt, nz.outputs["Fac"], rmp.inputs["Fac"])
baglan(nt, rmp.outputs["Color"], bsdf.inputs["Base Color"])
bmp = nt.nodes.new("ShaderNodeBump")
bmp.inputs["Strength"].default_value = 0.15
baglan(nt, nz.outputs["Fac"], bmp.inputs["Height"])
baglan(nt, bmp.outputs["Normal"], bsdf.inputs["Normal"])
bsdf.inputs["Roughness"].default_value = 0.9
duvar.data.materials.append(m)

# ---------------------------------------------------------------- kesme tahtasi
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.1, TAHTA_UST / 2))
tahta = bpy.context.object
tahta.scale = (4.8, 3.2, TAHTA_UST)
bpy.ops.object.transform_apply(scale=True)
bv = tahta.modifiers.new("pah", "BEVEL")
bv.width = 0.025
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

# ---------------------------------------------------------------- avokado govdesi
bpy.ops.mesh.primitive_uv_sphere_add(segments=96, ring_count=64, radius=1.0, location=(0, 0, MERKEZ_Z))
meyve = bpy.context.object
meyve.name = "meyve"
# kure -> x boyunca donel profil (plan.py ile ayni formul)
for v in meyve.data.vertices:
    x, y, z = v.co
    xn = max(-1.0, min(1.0, x))
    s = (xn + 1) / 2
    f = (M["boyun"] + (1 - M["boyun"]) * s)
    v.co = (x * A, y * R * f / FMAX, z * R * f / FMAX)
bpy.ops.object.shade_smooth()

m, nt, bsdf = malzeme("avokado_kabuk")
tk = nt.nodes.new("ShaderNodeTexCoord")
nz = nt.nodes.new("ShaderNodeTexNoise")
nz.inputs["Scale"].default_value = 5
nz.inputs["Detail"].default_value = 4
baglan(nt, tk.outputs["Object"], nz.inputs["Vector"])
vor = nt.nodes.new("ShaderNodeTexVoronoi")
vor.inputs["Scale"].default_value = 38
baglan(nt, tk.outputs["Object"], vor.inputs["Vector"])
kabuk_rmp = nt.nodes.new("ShaderNodeValToRGB")
kabuk_rmp.color_ramp.elements[0].color = hex_renk("#1d3014")
kabuk_rmp.color_ramp.elements[1].color = hex_renk("#4a6b2c")
baglan(nt, nz.outputs["Fac"], kabuk_rmp.inputs["Fac"])
yukseklik = matematik(nt, "ADD", nz.outputs["Fac"], vor.outputs["Distance"])
bmp = nt.nodes.new("ShaderNodeBump")
bmp.inputs["Strength"].default_value = 0.12
bmp.inputs["Distance"].default_value = 0.02
baglan(nt, yukseklik, bmp.inputs["Height"])

# kesim cizgileri: her eksen icin n=c+1 ve yapilan kesim sayisi d (anahtar kareli Value dugumleri)
ayir = nt.nodes.new("ShaderNodeSeparateXYZ")
baglan(nt, tk.outputs["Object"], ayir.inputs[0])
DEGER = {}
cizgi_top = None
for eks, idx, yar in (("x", 0, A), ("y", 1, R), ("z", 2, R)):
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
baglan(nt, kabuk_rmp.outputs["Color"], kar.inputs[6])
kar.inputs[7].default_value = hex_renk("#c3df86")
baglan(nt, kar.outputs[2], bsdf.inputs["Base Color"])
baglan(nt, bmp.outputs["Normal"], bsdf.inputs["Normal"])
bsdf.inputs["Roughness"].default_value = 0.26
kes_x = nt.nodes.new("ShaderNodeValue"); kes_x.name = "kes_x"; kes_x.outputs[0].default_value = -10.0
kirp = matematik(nt, "LESS_THAN", ayir.outputs[0], kes_x.outputs[0])
seffaf = nt.nodes.new("ShaderNodeBsdfTransparent")
karis_s = nt.nodes.new("ShaderNodeMixShader")
baglan(nt, kirp, karis_s.inputs[0])
baglan(nt, bsdf.outputs[0], karis_s.inputs[1])
baglan(nt, seffaf.outputs[0], karis_s.inputs[2])
baglan(nt, karis_s.outputs[0], nt.nodes["Material Output"].inputs["Surface"])
meyve.data.materials.append(m)

# ---------------------------------------------------------------- bicak
def bicak_kur():
    """Gercekci buyuk sef bicagi (kullanici 13 Kas): yerel +X boyunca agiz (y=0 kesici kenar), sirt y~0.62,
    uc x=2.9; kesitte kama (kenarda ince, sirtta 0.036). Celik topuk + perçinli koyu ahsap sap (-X)."""
    L_ = 2.9      # agiz boyu
    H_ = 0.62     # topuk yuksekligi
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
    topuk.scale = (0.12, H_ * 0.92, 0.07)
    bv_ = topuk.modifiers.new("pah", "BEVEL"); bv_.width = 0.015; bv_.segments = 2
    topuk.data.materials.append(mb)
    topuk.parent = agiz
    # sap: koyu ahsap, hafif oval, 3 perçin
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.78, H_ * 0.52, 0))
    sap = bpy.context.object
    sap.scale = (1.3, 0.30, 0.11)
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
    for px in (-0.35, -0.75, -1.15):
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.035, depth=0.125, location=(px, H_ * 0.52, 0),
                                            rotation=(0, 0, 0))
        pc = bpy.context.object
        pc.data.materials.append(mb)
        pc.parent = agiz
    return agiz


bicak = bicak_kur()

# eksene gore bicak yonleri (Euler XYZ, radyan)
YON = {
    "x": (math.radians(90), 0.0, math.radians(-90)),   # agiz derinlik boyunca, duzlem YZ, sap arkada
    "y": (math.radians(90), 0.0, math.radians(180)),   # agiz x boyunca, duzlem XZ, kameraya yuzu donuk
    "z": (0.0, 0.0, math.radians(-90)),                # yatay dilim, agiz -x'e bakar
}
DISARI = (7.5, -1.0, 4.5)  # kadraj disi (sag ust)


def bicak_konum(eks, konum, asagi, yuk):
    """eks kesim duzlemi, konum duzlem koordinati, asagi=True agiz tahtada; yuk=0..1 kalkis yuksekligi."""
    if eks == "x":
        return (konum, 1.05, TAHTA_UST + 0.004 if asagi else MERKEZ_Z + R + 0.15 + 0.9 * yuk)
    if eks == "y":
        return (1.25, konum, TAHTA_UST + 0.004 if asagi else MERKEZ_Z + R + 0.15 + 0.9 * yuk)
    # z: yatay dilim; asagi = ice girmis (uc meyveden gecti), yukari = sagda disarida
    return ((-A - 0.3) if asagi else (A + 0.5 + 0.8 * yuk), 1.0, MERKEZ_Z + konum)


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
    xn = np.clip(x / A, -1, 1)
    return R * np.sqrt(np.maximum(0, 1 - xn * xn)) * (M["boyun"] + (1 - M["boyun"]) * (xn + 1) / 2) / FMAX


def kup_nesnesi(tur, no):
    """REF-080: kesim hucresi kupleri; dis yuz kabuk, ic et/cekirdek. x supurmesi soldan saga ilerledikce
    her dilimin kupleri yerine coker (GN: Scene Time ile kup basina birakilma ani). Son yigin: alt yari
    tumsek, ust yari icine coker -> ustte kesit (krem et + kahve cekirdek)."""
    tavan = GORSEL_TAVANLAR[min(no, len(GORSEL_TAVANLAR) - 1)]
    cx, cy, cz = tur["cx"], tur["cy"], tur["cz"]
    gx, gy, gz = (min(c + 1, tavan) for c in (cx, cy, cz))
    xs = -A + (np.arange(gx) + 0.5) * (2 * A / gx)
    ys = -R + (np.arange(gy) + 0.5) * (2 * R / gy)
    zs = -R + (np.arange(gz) + 0.5) * (2 * R / gz)
    X, Y, Z = np.meshgrid(xs, ys, zs, indexing="ij")
    rr = profil_r(X)
    ic = (np.abs(X / A) <= 1) & (Y * Y + Z * Z <= rr * rr)
    idx = np.argwhere(ic)
    merk = np.stack([X[ic], Y[ic], Z[ic]], 1)
    k = len(merk)
    rng = np.random.default_rng(7 + no)
    hx, hy, hz = A / gx, R / gy, R / gz
    # dis yuz maskesi: bit 0:+X 1:-X 2:+Y 3:-Y 4:+Z 5:-Z (komsu hucre disarida ise kabuk)
    p = np.pad(ic, 1)
    maske = np.zeros(k)
    for bit, (dx, dy, dz) in enumerate([(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]):
        dis = ~p[idx[:, 0] + 1 + dx, idx[:, 1] + 1 + dy, idx[:, 2] + 1 + dz]
        maske += dis * (2 ** bit)
    # et/cekirdek rengi (REF-080: ic krem, kabuga yakin acik yesil, cekirdek kahve + koyu kenar)
    ck = M["cekirdek"]
    cek_r = ck["r"] * R
    cd = np.linalg.norm(merk - np.array([ck["x"] * A, 0, 0]), axis=1)
    d = np.sqrt(merk[:, 1] ** 2 + merk[:, 2] ** 2) / np.maximum(profil_r(merk[:, 0]), 1e-6)
    krem = np.array(hex_renk("#f1e9b8")[:3])
    sari = np.array(hex_renk("#e3e08e")[:3])
    yesil = np.array(hex_renk("#a8cc5c")[:3])
    u = np.clip(d, 0, 1)[:, None]
    renk = np.where(u < 0.6, krem * (1 - u / 0.6) + sari * (u / 0.6), sari * (1 - (u - 0.6) / 0.4) + yesil * ((u - 0.6) / 0.4))
    renk[cd <= cek_r] = np.array(hex_renk("#b98a52")[:3])
    renk[(cd <= cek_r) & (cd > cek_r * 0.86)] = np.array(hex_renk("#4a2412")[:3])
    renk *= rng.uniform(0.93, 1.05, (k, 1))

    # birakilma ani: x kesimi hucrenin sag kenarini gectiginde (soldan saga)
    xk = [(t, konum) for t, eks, konum, j in tur["kesimler"] if eks == "x"]
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
    x0, y0 = -2.3, -1.55
    nxm, nym = int(4.6 / hucre) + 1, int(2.9 / hucre) + 1
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
    B = max(1, int(np.sqrt(k) / 2))
    def _sira(xv, yv, zv):
        o = np.argsort(xv, kind="stable")
        serit = np.empty(len(xv), np.int64)
        serit[o] = (np.arange(len(xv)) * B) // len(xv)
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
    karis.inputs[7].default_value = hex_renk("#21361a")
    baglan(ntk, karis.outputs[2], bk.inputs["Base Color"])
    bk.inputs["Roughness"].default_value = 0.5

    mt, ntt, bt = malzeme(f"tanecik_m_{no}")
    t_r = ntt.nodes.new("ShaderNodeAttribute"); t_r.attribute_type = "GEOMETRY"; t_r.attribute_name = "renk"
    t_m = ntt.nodes.new("ShaderNodeAttribute"); t_m.attribute_type = "GEOMETRY"; t_m.attribute_name = "maske"
    t_k = ntt.nodes.new("ShaderNodeMix"); t_k.data_type = "RGBA"
    baglan(ntt, matematik(ntt, "GREATER_THAN", t_m.outputs["Fac"], None, deger_b=0.5), t_k.inputs["Factor"])
    baglan(ntt, t_r.outputs["Color"], t_k.inputs[6])
    t_k.inputs[7].default_value = hex_renk("#21361a")
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
    meyve.scale = (0.001, 0.001, 0.001)
    meyve.keyframe_insert("scale", frame=kare(bas))
    meyve.scale = (1.05, 1.05, 1.05)
    meyve.keyframe_insert("scale", frame=kare(bas + 0.22))
    meyve.scale = (1, 1, 1)
    meyve.keyframe_insert("scale", frame=kare(bas + 0.36))
    meyve.keyframe_insert("scale", frame=kare(ks))  # tur boyunca 1.0 sabit
    meyve.hide_render = True
    meyve.keyframe_insert("hide_render", frame=kare(ks + 0.02))
    bicak.location = DISARI
    bicak.keyframe_insert("location", frame=kare(kb - 0.3))
    # cizgi degerleri sifirla
    for eks, c in (("x", tur["cx"]), ("y", tur["cy"]), ("z", tur["cz"])):
        deger_anahtar(f"n_{eks}", bas, c + 1.0)
        deger_anahtar(f"d_{eks}", bas, 0.0)
    deger_anahtar("kes_x", bas, -10.0)
    # kesimler
    sayac = {"x": 0, "y": 0, "z": 0}
    ks_list = tur["kesimler"]
    onceki_eks = None
    for i, (t, eks, konum, j) in enumerate(ks_list):
        sonraki = ks_list[i + 1][0] if i + 1 < len(ks_list) else t + 0.4
        onceki = ks_list[i - 1][0] if i > 0 else kb - 0.25
        ara_on = max(0.01, t - onceki)
        ara_son = max(0.01, sonraki - t)
        yuk_on = min(1.0, ara_on * 3)
        if eks != onceki_eks:
            # yon degisimi: bicak yukarida, bir onceki anda yon degisir
            bicak.rotation_euler = YON[eks]
            bicak.keyframe_insert("rotation_euler", frame=kare(t - ara_on * 0.6))
            onceki_eks = eks
        bicak.location = bicak_konum(eks, konum, False, yuk_on)
        bicak.keyframe_insert("location", frame=kare(t - min(ara_on * 0.55, 0.18)))
        bicak.location = bicak_konum(eks, konum, True, 0)
        bicak.keyframe_insert("location", frame=kare(t))
        sayac[eks] += 1
        deger_anahtar(f"d_{eks}", t, float(sayac[eks]))
        if eks == "x":
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
ad = meyve.animation_data.action
for fc in egriler(ad):
    for kp in fc.keyframe_points:
        kp.interpolation = "CONSTANT" if fc.data_path == "hide_render" else "BEZIER"

# ---------------------------------------------------------------- kesit yuzu (kalan meyve)
# disk elle kurulur (YZ duzleminde, yaricap tam 1): surumden bagimsiz olcu
_n = 96
_vs = [(0.0, math.cos(2 * math.pi * i / _n), math.sin(2 * math.pi * i / _n)) for i in range(_n)]
_me = bpy.data.meshes.new("kesit")
_me.from_pydata(_vs, [], [list(range(_n))[::-1]])
_me.update()
kesit = bpy.data.objects.new("kesit", _me)
sc.collection.objects.link(kesit)
kesit.location = (0, 0, MERKEZ_Z)
mk_, ntk_, bk_ = malzeme("kesit_m")
gp = ntk_.nodes.new("ShaderNodeNewGeometry")
ay_ = ntk_.nodes.new("ShaderNodeSeparateXYZ")
baglan(ntk_, gp.outputs["Position"], ay_.inputs[0])
v_r = ntk_.nodes.new("ShaderNodeValue"); v_r.name = "kesit_r"; v_r.outputs[0].default_value = 1.0
v_x = ntk_.nodes.new("ShaderNodeValue"); v_x.name = "kesit_x"; v_x.outputs[0].default_value = 0.0
dy = ay_.outputs[1]
dz = matematik(ntk_, "SUBTRACT", ay_.outputs[2], None, deger_b=MERKEZ_Z)
rad = matematik(ntk_, "SQRT", matematik(ntk_, "ADD", matematik(ntk_, "MULTIPLY", dy, dy), matematik(ntk_, "MULTIPLY", dz, dz)))
u_ = matematik(ntk_, "DIVIDE", rad, v_r.outputs[0])
et_r = ntk_.nodes.new("ShaderNodeValToRGB")
et_r.color_ramp.elements[0].color = hex_renk("#f1e9b8")
et_r.color_ramp.elements[1].position = 0.97
et_r.color_ramp.elements[1].color = hex_renk("#a8cc5c")
e_m = et_r.color_ramp.elements.new(0.6); e_m.color = hex_renk("#e3e08e")
e_k = et_r.color_ramp.elements.new(0.985); e_k.color = hex_renk("#21361a")
baglan(ntk_, u_, et_r.inputs["Fac"])
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
    xk = [(t, konum) for t, eks, konum, j in tur["kesimler"] if eks == "x"]
    kesit.hide_render = False
    kesit.keyframe_insert("hide_render", frame=kare(xk[0][0]))
    kesit.hide_render = True
    kesit.keyframe_insert("hide_render", frame=kare(xk[-1][0] + 0.02))
    for t, konum in xk:
        r_ = float(profil_r(np.array([konum]))[0]) * 0.995
        kesit.location = (konum + 0.002, 0, MERKEZ_Z)
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
gunes.energy = 3.2
gunes.angle = math.radians(6)
g = bpy.data.objects.new("gunes", gunes)
g.rotation_euler = (math.radians(50), math.radians(-28), math.radians(-35))
sc.collection.objects.link(g)
alan = bpy.data.lights.new("dolgu", "AREA")
alan.energy = 450
alan.size = 5
a = bpy.data.objects.new("dolgu", alan)
a.location = (-2.5, -4.0, 5.0)
a.rotation_euler = (math.radians(45), 0, math.radians(-30))
sc.collection.objects.link(a)

cam = bpy.data.cameras.new("kamera")
cam.lens = 58
cam.sensor_fit = "HORIZONTAL"
cam.sensor_width = 36
k = bpy.data.objects.new("kamera", cam)
k.location = (-1.2, -4.15, 2.35)  # on-soldan: kalan meyvenin kesit yuzu gorunur (REF-080)
sc.collection.objects.link(k)
hedef = bpy.data.objects.new("hedef", None)
hedef.location = (0.05, 0.0, 0.66)
sc.collection.objects.link(hedef)
tr = k.constraints.new("TRACK_TO")
tr.target = hedef
tr.track_axis = "TRACK_NEGATIVE_Z"
tr.up_axis = "UP_Y"
sc.camera = k

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
