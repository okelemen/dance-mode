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
nz.inputs["Scale"].default_value = 26
nz.inputs["Detail"].default_value = 8
baglan(nt, tk.outputs["Object"], nz.inputs["Vector"])
vor = nt.nodes.new("ShaderNodeTexVoronoi")
vor.inputs["Scale"].default_value = 38
baglan(nt, tk.outputs["Object"], vor.inputs["Vector"])
kabuk_rmp = nt.nodes.new("ShaderNodeValToRGB")
kabuk_rmp.color_ramp.elements[0].color = hex_renk("#18220d")
kabuk_rmp.color_ramp.elements[1].color = hex_renk("#3f5520")
baglan(nt, nz.outputs["Fac"], kabuk_rmp.inputs["Fac"])
yukseklik = matematik(nt, "ADD", nz.outputs["Fac"], vor.outputs["Distance"])
bmp = nt.nodes.new("ShaderNodeBump")
bmp.inputs["Strength"].default_value = 0.55
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
    ince = matematik(nt, "LESS_THAN", uzak, None, deger_b=0.07)
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
kar.inputs[7].default_value = hex_renk("#a9c95a")
baglan(nt, kar.outputs[2], bsdf.inputs["Base Color"])
baglan(nt, bmp.outputs["Normal"], bsdf.inputs["Normal"])
bsdf.inputs["Roughness"].default_value = 0.42
meyve.data.materials.append(m)

# ---------------------------------------------------------------- bicak
def bicak_kur():
    # yerel: agiz kenari +X boyunca y=0, sirt y~0.42, uc x=2.0; kalinlik z
    pr = []
    N = 24
    for i in range(N + 1):
        x = 2.0 * i / N
        pr.append((x, 0.0))
    for i in range(N, -1, -1):
        x = 2.0 * i / N
        sirt = 0.42 if x < 1.3 else 0.42 - (x - 1.3) / 0.7 * 0.40
        # agiz ucta yukari kivrilir
        pr.append((x, sirt))
    alt = []
    for i in range(N + 1):
        x = 2.0 * i / N
        kivrim = 0.0 if x < 1.4 else ((x - 1.4) / 0.6) ** 2 * 0.06
        alt.append((x, kivrim))
    ust = [(x, (0.42 if x < 1.3 else 0.42 - (x - 1.3) / 0.7 * 0.36)) for x, _ in alt]
    kal = 0.012
    vs, fs = [], []
    n = len(alt)
    for (x, y) in alt:
        vs.append((x, y, 0.0))          # keskin agiz (ince)
    for (x, y) in ust:
        vs.append((x, y, kal))
    for (x, y) in ust:
        vs.append((x, y, -kal))
    for i in range(n - 1):
        fs.append((i, i + 1, n + i + 1, n + i))
        fs.append((i, 2 * n + i, 2 * n + i + 1, i + 1))
        fs.append((n + i, n + i + 1, 2 * n + i + 1, 2 * n + i))
    me = bpy.data.meshes.new("bicak")
    me.from_pydata(vs, [], fs)
    me.update()
    agiz = bpy.data.objects.new("bicak", me)
    sc.collection.objects.link(agiz)
    mb, ntb, bb = malzeme("celik")
    bb.inputs["Base Color"].default_value = hex_renk("#dfe2e6")
    bb.inputs["Metallic"].default_value = 0.85
    bb.inputs["Roughness"].default_value = 0.32
    me.materials.append(mb)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.55, 0.22, 0))
    sap = bpy.context.object
    sap.scale = (1.1, 0.26, 0.09)
    mh, nth, bh = malzeme("sap")
    bh.inputs["Base Color"].default_value = hex_renk("#1c1712")
    bh.inputs["Roughness"].default_value = 0.5
    sap.data.materials.append(mh)
    sap.parent = agiz
    agiz.scale = (1.2, 1.45, 1.0)  # agiz 2.4 boy, sirt ~0.6
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
DUSUS_ORNEK = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.75, 0.95]  # sn, parca dusus yorunge ornekleri
G = 11.0  # sahne birimi/sn^2 (agir cekim yer cekimi)
GORSEL_TAVANLAR = [40, 50, 60, 70, 80]  # tur basina eksen basi gorsel parca siniri (her tur kuculur)


def profil_r(x):
    xn = np.clip(x / A, -1, 1)
    return R * np.sqrt(np.maximum(0, 1 - xn * xn)) * (M["boyun"] + (1 - M["boyun"]) * (xn + 1) / 2) / FMAX


def kup_nesnesi(tur, no):
    """Parca = kesim hucresi ile avokado govdesinin kesisimi: ic parcalar kesim hucresi (kesim
    duzlemleriyle sinirli), dis parcalarin kabuk tarafi govde egrisine oturur. Her parca ayri duser."""
    tavan = GORSEL_TAVANLAR[min(no, len(GORSEL_TAVANLAR) - 1)]
    cx, cy, cz = tur["cx"], tur["cy"], tur["cz"]
    gx, gy, gz = (min(c + 1, tavan) for c in (cx, cy, cz))
    xs = -A + (np.arange(gx) + 0.5) * (2 * A / gx)
    ys = -R + (np.arange(gy) + 0.5) * (2 * R / gy)
    zs = -R + (np.arange(gz) + 0.5) * (2 * R / gz)
    X, Y, Z = np.meshgrid(xs, ys, zs, indexing="ij")
    rr = profil_r(X)
    ic = (np.abs(X / A) <= 1) & (Y * Y + Z * Z <= rr * rr)
    merk = np.stack([X[ic], Y[ic], Z[ic]], 1)
    k = len(merk)
    rng = np.random.default_rng(7 + no)
    hx, hy, hz = A / gx, R / gy, R / gz
    bosluk = 0.985  # kesim yuzeyleri arasinda ince bicak boslugu
    ofs = np.array([[sx * hx, sy * hy, sz * hz] for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]) * bosluk
    v = merk[:, None, :] + ofs[None, :, :]  # (k,8,3)
    # govde disina tasan koseler kabuk yuzeyine cekilir (dogal kesim parcasi)
    vx = np.clip(v[..., 0], -A * 0.995, A * 0.995)
    vr = profil_r(vx)
    rad = np.sqrt(v[..., 1] ** 2 + v[..., 2] ** 2)
    tasma = rad > vr
    olc = np.where(tasma, vr / np.maximum(rad, 1e-9), 1.0)
    v[..., 0] = vx
    v[..., 1] *= olc
    v[..., 2] *= olc
    disari = tasma | (np.abs(merk[:, None, 0] + ofs[None, :, 0]) > A * 0.995)
    # renkler
    ck = M["cekirdek"]
    cek_r = ck["r"] * R
    cek_m = np.array([ck["x"] * A, 0, 0])
    cek_ic = np.array(hex_renk("#6b3a1c")[:3])
    et_cek = np.array(hex_renk("#c6d96a")[:3])
    et_dis = np.array(hex_renk("#5e9a2a")[:3])
    kabuk = np.array(hex_renk("#22300f")[:3])
    cd = np.linalg.norm(merk - cek_m, axis=1)
    u = np.clip((cd - cek_r) / np.maximum(R * 0.62 - cek_r, 1e-6), 0, 1)[:, None]
    taban = et_cek * (1 - u) + et_dis * u
    taban[cd <= cek_r] = cek_ic
    taban *= rng.uniform(0.92, 1.06, (k, 1))
    yuz = np.array([[0, 1, 3, 2], [4, 6, 7, 5], [0, 4, 5, 1], [2, 3, 7, 6], [0, 2, 6, 4], [1, 5, 7, 3]])
    # yuz kabuk mu: 4 kosesinden en az 3'u yuzeye cekildiyse
    kabuk_yuz = disari[:, yuz].sum(axis=2) >= 3  # (k,6)
    renk = np.where(kabuk_yuz[..., None], kabuk[None, None, :] * rng.uniform(0.85, 1.15, (k, 1, 1)),
                    taban[:, None, :])  # (k,6,3)

    # ---- dusus: her parca ayri duser, tahtada yigilir, duserken doner
    p0 = merk.copy()
    p0[:, 2] += MERKEZ_Z
    zb = TAHTA_UST
    h = 2 * hz * 0.9
    yon = merk[:, :2] / np.maximum(np.linalg.norm(merk[:, :2], axis=1, keepdims=True), 1e-6)
    yuks = (p0[:, 2] - zb) / (2 * R)
    yay = (0.25 + 0.9 * yuks) * R * rng.uniform(0.5, 1.3, k)
    hedef_xy = merk[:, :2] + yon * yay[:, None] + rng.normal(0, 0.03, (k, 2))
    bx = np.floor(hedef_xy[:, 0] / (2 * hx)).astype(np.int64)
    by = np.floor(hedef_xy[:, 1] / (2 * hy)).astype(np.int64)
    hedef_xy[:, 0] = (bx + 0.5) * 2 * hx
    hedef_xy[:, 1] = (by + 0.5) * 2 * hy
    anah = (bx - bx.min()) * 1_000_003 + (by - by.min())
    sira = np.lexsort((p0[:, 2], anah))
    rank = np.zeros(k, np.int64)
    a_s = anah[sira]
    yeni = np.r_[True, a_s[1:] != a_s[:-1]]
    grup_bas = np.maximum.accumulate(np.where(yeni, np.arange(k), 0))
    rank[sira] = np.arange(k) - grup_bas
    zf = np.minimum(zb + h / 2 + rank * h, p0[:, 2])
    gecik = rng.uniform(0, 0.12, k) + (1 - yuks) * 0.04
    donus = rng.normal(0, 1.0, k) * 1.4  # z ekseni etrafinda son donus (radyan)
    yerel = v - merk[:, None, :]  # parcanin kendi merkezine gore koseler

    def konum(s):
        tau = np.maximum(s - gecik, 0)
        z = np.maximum(zf, p0[:, 2] - 0.5 * G * tau * tau)
        ilerle = np.where(p0[:, 2] - zf > 1e-6, (p0[:, 2] - z) / np.maximum(p0[:, 2] - zf, 1e-6), 1.0)
        xy = p0[:, :2] + (hedef_xy - p0[:, :2]) * ilerle[:, None]
        aci = donus * ilerle
        c, sn = np.cos(aci)[:, None], np.sin(aci)[:, None]
        lx = yerel[..., 0] * c - yerel[..., 1] * sn
        ly = yerel[..., 0] * sn + yerel[..., 1] * c
        out = np.empty_like(yerel)
        out[..., 0] = lx + xy[:, 0:1]
        out[..., 1] = ly + xy[:, 1:2]
        out[..., 2] = yerel[..., 2] + z[:, None]
        return out.reshape(-1, 3)

    v0 = v.copy()
    v0[..., 2] += MERKEZ_Z
    v0 = v0.reshape(-1, 3)
    f_all = (yuz[None, :, :] + (np.arange(k) * 8)[:, None, None]).reshape(-1, 4)
    me = bpy.data.meshes.new(f"kup_{no}")
    me.vertices.add(len(v0))
    me.vertices.foreach_set("co", v0.ravel().astype(np.float32))
    me.loops.add(f_all.size)
    me.loops.foreach_set("vertex_index", f_all.ravel().astype(np.int32))
    me.polygons.add(len(f_all))
    me.polygons.foreach_set("loop_start", (np.arange(len(f_all)) * 4).astype(np.int32))
    me.polygons.foreach_set("loop_total", np.full(len(f_all), 4, np.int32))
    me.update(calc_edges=True)
    ca = me.color_attributes.new("renk", "FLOAT_COLOR", "CORNER")
    rv = np.repeat(renk.reshape(-1, 3), 4, axis=0)
    ca.data.foreach_set("color", np.hstack([rv, np.ones((len(rv), 1))]).ravel().astype(np.float32))
    ob = bpy.data.objects.new(f"kup_{no}", me)
    sc.collection.objects.link(ob)
    try:
        ob.cycles.use_motion_blur = False
    except Exception:
        pass
    mk, ntk, bk = malzeme(f"kup_m_{no}")
    at = ntk.nodes.new("ShaderNodeAttribute")
    at.attribute_name = "renk"
    baglan(ntk, at.outputs["Color"], bk.inputs["Base Color"])
    bk.inputs["Roughness"].default_value = 0.5
    me.materials.append(mk)
    ob.shape_key_add(name="temel")
    for i, s in enumerate(DUSUS_ORNEK[1:], 1):
        sk = ob.shape_key_add(name=f"d{i}")
        sk.data.foreach_set("co", konum(s).ravel().astype(np.float32))
    print(f"tur {no}: {k} gorsel parca ({gx}x{gy}x{gz})", flush=True)
    return ob


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
    meyve.keyframe_insert("hide_render", frame=kare(ks + 0.05))
    bicak.location = DISARI
    bicak.keyframe_insert("location", frame=kare(kb - 0.3))
    # cizgi degerleri sifirla
    for eks, c in (("x", tur["cx"]), ("y", tur["cy"]), ("z", tur["cz"])):
        deger_anahtar(f"n_{eks}", bas, c + 1.0)
        deger_anahtar(f"d_{eks}", bas, 0.0)
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
    bicak.location = DISARI
    bicak.keyframe_insert("location", frame=kare(ks + 0.12))
    # kup yigini
    kup = kup_nesnesi(tur, no)
    kup.hide_render = True
    kup.keyframe_insert("hide_render", frame=0)
    kup.hide_render = False
    kup.keyframe_insert("hide_render", frame=kare(ks + 0.05))
    kup.hide_render = True
    kup.keyframe_insert("hide_render", frame=kare(son))
    kb_ = kup.data.shape_keys.key_blocks
    t0 = ks + 0.05
    nk = len(DUSUS_ORNEK)
    for i in range(1, nk):
        for j, s_ in enumerate(DUSUS_ORNEK):
            kb_[f"d{i}"].value = 1.0 if j == i else 0.0
            kb_[f"d{i}"].keyframe_insert("value", frame=kare(t0 + s_))
    sabit_interp(kup)
    for fc in egriler(kup.data.shape_keys.animation_data.action):
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"

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
cam.lens = 50
cam.sensor_fit = "HORIZONTAL"
cam.sensor_width = 36
k = bpy.data.objects.new("kamera", cam)
k.location = (2.0, -3.77, 2.57)
sc.collection.objects.link(k)
hedef = bpy.data.objects.new("hedef", None)
hedef.location = (0.0, 0.0, 0.62)
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
    liste = list(range(int(arg("--bas", "1")), int(arg("--son", str(PLAN["kare"]))) + 1))
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
