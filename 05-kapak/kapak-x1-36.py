"""HUMAN TETRIS 36 kapagi (REF-088 duzeni, 1P SOLO, gunduz dev mantar ormani, cilali 3D oyun gorunumu) - 1280x720.

    python kapak-x1-36.py --poz werewolf-low-lunge-hip-diag --arka varlik-36-kapak-m0 --cikti A.jpg

kapak-x2-35'ten (kontrast / cakisma olcumleri aynen) + kapak-x3-34'un Warm Up gostergesi. REF-088 kapagi (20 Kas olcum:
doygunluk 0,742 / parlaklik 0,685 / renklilik 0,582; siluet yukseklik %79,9, alan %5,9): ustte HER HARFI AYRI RENK gokkusagi
baloncuk HUMAN TETRIS, solda gokkusagi gosterge + "Warm Up", sol altta kirmizi NEW rozeti (kurdeleli), sagda beyaz baloncuk
oyuncu yazisi (REF "1 Player / 9 MINS" yerine yukleme notu 7: 1 PLAYER; uzun sure yazilmaz), ortada truss cerceve icinde YESIL
pano + ayni poz koyu, onde TEK dev siyah siluet beyaz kalin konturlu. VS yok. Siluet (kullanici 21 Kas): A = werewolf-low-lunge-hip-diag
(BOSS WALL pozu), B = vampire-lunge-bent-up-diag - bu videonun onayli solo duvar maskeleri (TALIMATLAR §8, 7 Kas harmanlama).
Cizim sirasi: arka plan -> truss + pano -> on siluet -> baslik -> gosterge -> sag yazi -> NEW rozeti.
"""
import argparse, json, math, os
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageEnhance

KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TP = os.path.join(KOK, "03-motor", "tetris-pvp")
REF = r"C:\Users\eleme\OneDrive\Masaüstü\REFERANSLAR"
KAYNAK = {"Y": ("OC-yoga-siluet", "%s-2000.png"), "D": ("OC-dans-siluet/buyuk", "%s.png"), "K": ("OC-dans-siluet", "%s-2000.png"),
          "S": ("SVGSILH-dans-siluet/png512", "%s.png")}   # svgsilh.com CC0 (6 Kas kaydi), 512 px
p = argparse.ArgumentParser()
p.add_argument("--poz", required=True, help="varlik-36s1/poz solo maske (ad, .png yok)")
p.add_argument("--boy", type=float, default=0.86, help="on siluet yuksekligi (kadraj orani)")
p.add_argument("--maks-gen", type=float, default=0.62)
p.add_argument("--x", type=float, default=0.42)
p.add_argument("--arka", default="varlik-36-kapak-m0")
p.add_argument("--bas-boy", type=float, default=150)
p.add_argument("--bas-y", type=float, default=74); p.add_argument("--tasma", type=float, default=0.0)
p.add_argument("--kontur", type=int, default=13)
p.add_argument("--renk", type=float, default=1.0); p.add_argument("--parlak", type=float, default=1.0)
p.add_argument("--yansima", type=int, default=70, help="baloncuk cam yansimasi gucu (0-255)")
p.add_argument("--pano", nargs=4, type=float, default=[600, 160, 940, 390], help="truss icindeki yesil pano x0 y0 x1 y1")
p.add_argument("--rozet-xy", nargs=2, type=float, default=[140, 560])
p.add_argument("--yazi-xy", nargs=2, type=float, default=[1125, 250])
p.add_argument("--gosterge-xy", nargs=2, type=float, default=[175, 300])
p.add_argument("--cikti", required=True)
a = p.parse_args()
W, H = 1280, 720
FONT = os.path.join(KOK, "05-kapak", "fontlar", "Fredoka.ttf")


def font(boy):
    f = ImageFont.truetype(FONT, boy)
    try:
        f.set_variation_by_name("Bold")
    except Exception:
        pass
    return f


def klasor(ad):
    v = os.path.join(TP, ad, "tetris-varlik")
    return v if os.path.isdir(v) else os.path.join(TP, ad)


V = klasor(a.arka)
im = Image.open(os.path.join(V, "kapak-gok.png")).convert("RGBA").resize((W, H), Image.LANCZOS)
im.alpha_composite(Image.open(os.path.join(V, "kapak-serit.png")).convert("RGBA").resize((W, H), Image.LANCZOS))   # tek serit (CO-OP)
if a.renk != 1.0:
    im = ImageEnhance.Color(im).enhance(a.renk)
if a.parlak != 1.0:
    im = ImageEnhance.Brightness(im).enhance(a.parlak)


SW = W
YER = json.load(open(os.path.join(V, "yerlesim.json"), encoding="utf-8")); OL = 1.0
TON = {"p1": (30, 124, 255), "p2": (255, 42, 160), "p3": (24, 200, 64)}


def kart(i, oy, ton):
    """kapi acikliginda buzlu akrilik pano: arkadaki salon bulaniklasir + beyaz sut tonu + oyuncu renginde hafif ton, ust kenarda isik yansimasi"""
    x0, y0, x1, y1 = [v * OL for v in YER["aciklik_" + oy]]
    X0, Y0 = int(i * SW + x0), int(y0); w, h = int(x1 - x0), int(y1 - y0)
    arka = im.crop((X0, Y0, X0 + w, Y0 + h)).filter(ImageFilter.GaussianBlur(9))
    k = Image.blend(arka, Image.new("RGBA", (w, h), ton + (255,)), 0.85)   # REF-084: doygun oyuncu renginde pano
    yy = np.linspace(0, 1, h)[:, None].repeat(w, 1)
    yan = Image.fromarray((np.clip(1 - yy / 0.35, 0, 1) * 55).astype(np.uint8))      # ust kenardan inen yumusak yansima
    k.paste(Image.new("RGBA", (w, h), (255, 255, 255, 255)), (0, 0), yan)
    im.alpha_composite(k, (X0, Y0))
    return X0, Y0, w, h


def siluet_maske(ad, ayna=0):
    """solo duvar maskesi (varlik-36s1/poz, RGBA) -> alfa maske; 2x LANCZOS, kirpilmis"""
    al = Image.open(os.path.join(TP, "varlik-36s1", "poz", ad + ".png")).convert("RGBA").getchannel("A")
    al = al.resize((al.width * 2, al.height * 2), Image.LANCZOS).point(lambda v: 255 if v > 110 else 0).filter(ImageFilter.GaussianBlur(1.0))
    if ayna:
        al = al.transpose(Image.FLIP_LEFT_RIGHT)
    return al.crop(al.getbbox())


def truss_pano(x0, y0, x1, y1):
    """REF-086: gri celik kafes (truss) cerceve + icinde duz sari pano, panoda uc siluet koyu mor"""
    t = 26; d = ImageDraw.Draw(im)
    gri, koyu = (255, 210, 80, 255), (200, 110, 10, 255)   # REF-088: altin-turuncu isikli truss (gri soluk olcer)   # gri soluk olcumu dusuruyordu -> neon mor celik
    for (a0, b0, a1, b1, yatay) in ((x0 - t, y0 - t, x1 + t, y0, 1), (x0 - t, y1, x1 + t, y1 + t, 1),
                                    (x0 - t, y0 - t, x0, im.height, 0), (x1, y0 - t, x1 + t, im.height, 0)):
        d.rectangle((a0, b0, a1, b1), fill=koyu)
        d.rectangle((a0 + 3, b0 + 3, a1 - 3, b1 - 3), outline=gri, width=4)
        n = int(((a1 - a0) if yatay else (b1 - b0)) / t)
        for k in range(n):
            if yatay:
                xa = a0 + k * t; d.line((xa, b0 + 3, xa + t, b1 - 3), fill=gri, width=3)
            else:
                ya = b0 + k * t; d.line((a0 + 3, ya, a1 - 3, ya + t), fill=gri, width=3)
    d.rectangle((x0, y0, x1, y1), fill=(40, 220, 30, 255))      # REF-088: yesil pano
    w_, h_ = x1 - x0, y1 - y0
    ma = siluet_maske(a.poz); ph = int(h_ * 0.84); pw = int(ph * ma.width / ma.height)      # REF-087: panoda ayni es poz, koyu
    if pw > w_ * 0.86:
        pw = int(w_ * 0.86); ph = int(pw * ma.height / ma.width)
    im.paste((20, 50, 20, 255), (int(x0 + w_ / 2 - pw / 2), int(y1 - ph - h_ * 0.06)), ma.resize((pw, ph), Image.LANCZOS))


OLCU = []
truss_pano(*[int(v) for v in a.pano])
for i in (0,):
    ma = siluet_maske(a.poz)
    sb = int(H * a.boy); sw = int(sb * ma.width / ma.height)
    if sw > W * a.maks_gen:
        sw = int(W * a.maks_gen); sb = int(sw * ma.height / ma.width)
    sa = ma.resize((sw, sb), Image.LANCZOS)
    cx = W * a.x
    sx = int(max(8, min(W - sw - 8, cx - sw / 2))); sy = H - sb - 10 + int(H * a.tasma)   # 5b: gerekirse alttan tasar
    kont = Image.new("L", (sw + 60, sb + 60), 0); kont.paste(sa, (30, 30))
    im.paste((255, 255, 255, 255), (sx - 30, sy - 30), kont.filter(ImageFilter.MaxFilter(a.kontur)))
    im.paste((0, 0, 0, 255), (sx, sy), sa)
    gor = (np.asarray(sa) > 127)[:max(0, H - sy)]                      # yalniz kadrajda gorunen kisim (alttan tasma sayilmaz)
    OLCU.append((a.poz, min(sb, H - sy) / H * 100, gor.sum() / (W * H) * 100, sx, sy, sw, sb))


def gradyan(w, h, renkler, dikey=False):
    t = (np.linspace(0, 1, h)[:, None].repeat(w, 1) if dikey else np.linspace(0, 1, w)[None, :].repeat(h, 0))
    cs = [np.array([int(c[i:i + 2], 16) for i in (1, 3, 5)], np.float32) for c in renkler]
    pos = np.linspace(0, 1, len(cs)); rgb = np.zeros((h, w, 3), np.float32)
    for ch in range(3):
        rgb[..., ch] = np.interp(t, pos, [c[ch] for c in cs])
    return rgb


KONTRAST = []


def goreli(rgb):
    c = np.asarray(rgb, np.float32) / 255
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def oran(l1, l2):
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def kontrast_olc(ad, dolgu_m, kontur_m, dis_m, x, y):
    """md. 28: dolgu <-> kontur (en kotu %5 dolgu pikseli) ve kontur <-> hemen dis zemin (yazisiz arka plan, en kotu %5)"""
    son = np.asarray(im.convert("RGB"), np.float32); zem = np.asarray(ARKA.convert("RGB"), np.float32)
    w, h = dolgu_m.size
    dm = np.zeros((H, W), bool); km = np.zeros((H, W), bool); bm = np.zeros((H, W), bool)
    def yerlestir(m, hedef):
        arr = np.asarray(m) > 128
        x0, y0 = max(0, x), max(0, y); x1, y1 = min(W, x + w), min(H, y + h)
        hedef[y0:y1, x0:x1] = arr[y0 - y:y1 - y, x0 - x:x1 - x]
    yerlestir(dolgu_m, dm); yerlestir(kontur_m, km); yerlestir(dis_m, bm)
    bm &= ~np.asarray(Image.fromarray(km.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(3))) > 0   # beyaz dis kontur halkasi
    # kontur = dis kontur halkasinin dis yarisi (dolguya yakin beyaz ic hat ve kenar yumusatmasi olcume girmez)
    km &= ~(np.asarray(Image.fromarray(dm.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(13))) > 0)
    halka = np.asarray(Image.fromarray((km | dm | bm).astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(9))) > 0
    halka &= ~(km | dm | bm)
    # r1 = dolgu <-> kalin kontur (ortanca), r2 = dolgu <-> hemen dis zemin (en kotu %5), r3 = kontur <-> zemin (en kotu %5) (md. 28)
    Ld = float(np.median(goreli(son[dm]))); Lk = float(np.median(goreli(son[km]))); Lz = goreli(zem[halka])
    hi = lambda a_, b_: (np.maximum(a_, b_) + 0.05) / (np.minimum(a_, b_) + 0.05)
    Lb = float(np.median(goreli(son[bm]))) if bm.any() else Lk
    # r3: her zemin pikselinde mor ya da beyaz konturdan en az biri ayrisiyor mu (iki katli kontur)
    r1 = float(hi(Ld, Lk)); r2 = float(np.percentile(hi(Ld, Lz), 5)); r3 = float(np.percentile(np.maximum(hi(Lk, Lz), hi(Lb, Lz)), 5))
    KONTRAST.append((ad, r1, r2, r3))


def baloncuk(metin, cx, cy, boy, renkler, kontur="#4a1f86", hedef=None, aci=0, ad=None, dikey=False):
    """baloncuk yazi: yatay cok renkli degrade, kalin mor dis kontur, ustte cam yansimasi, beyaz ince ic hat"""
    S = 2; fS = font(boy * S)
    bx = fS.getbbox(metin); tw, th = bx[2] - bx[0], bx[3] - bx[1]
    pad = int(boy * S * 0.3); w, h = tw + 2 * pad, th + 2 * pad
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).text((pad - bx[0], pad - bx[1]), metin, font=fS, fill=255)
    dis = Image.new("L", (w, h), 0); ImageDraw.Draw(dis).text((pad - bx[0], pad - bx[1]), metin, font=fS, fill=255, stroke_width=int(boy * S * 0.085), stroke_fill=255)
    ic = Image.new("L", (w, h), 0); ImageDraw.Draw(ic).text((pad - bx[0], pad - bx[1]), metin, font=fS, fill=255, stroke_width=int(boy * S * 0.02), stroke_fill=255)
    # md. 28 (6 Kas 2026): mor kontur koyu gokte / siyah siluette kayboluyordu -> disina beyaz ikinci kontur (REF-072 basligi gibi)
    dis2 = Image.new("L", (w, h), 0); ImageDraw.Draw(dis2).text((pad - bx[0], pad - bx[1]), metin, font=fS, fill=255, stroke_width=int(boy * S * 0.125), stroke_fill=255)
    rgb = gradyan(w, h, renkler, dikey=dikey)
    yy = np.linspace(0, 1, h)[:, None]
    rgb = rgb * (0.92 + 0.22 * (1 - yy))[..., None].clip(0, 1.15)
    dol = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).convert("RGBA")
    K = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    K.paste(Image.new("RGBA", (w, h), (30, 6, 70, 150)), (int(boy * S * 0.03), int(boy * S * 0.06)), dis2)
    K.paste(Image.new("RGBA", (w, h), "#ffffff"), (0, 0), dis2)
    K.paste(Image.new("RGBA", (w, h), kontur), (0, 0), dis)
    K.paste(Image.new("RGBA", (w, h), "#ffffff"), (0, 0), ic)
    K.paste(dol, (0, 0), m)
    yans = Image.new("L", (w, h), 0); ImageDraw.Draw(yans).rectangle((0, pad + int(th * 0.06), w, pad + int(th * 0.36)), fill=a.yansima)
    yans = ImageChops.multiply(yans, m.filter(ImageFilter.MinFilter(int(boy * S * 0.05) | 1))).filter(ImageFilter.GaussianBlur(boy * S * 0.012))
    K.paste(Image.new("RGBA", (w, h), "#ffffff"), (0, 0), yans)
    K = K.resize((w // S, h // S), Image.LANCZOS); mm = m.resize((w // S, h // S), Image.LANCZOS); dd = dis.resize((w // S, h // S), Image.LANCZOS); d2 = dis2.resize((w // S, h // S), Image.LANCZOS)
    if hedef and K.width > hedef:
        olc = hedef / K.width; yeni = (hedef, int(K.height * olc))
        K, mm, dd, d2 = (q.resize(yeni, Image.LANCZOS) for q in (K, mm, dd, d2))
    if aci:
        K, mm, dd, d2 = (q.rotate(aci, resample=Image.BICUBIC, expand=True) for q in (K, mm, dd, d2))
    x, y = int(cx - K.width / 2), int(cy - K.height / 2)
    im.alpha_composite(K, (x, y))
    kontrast_olc(ad or metin, mm.filter(ImageFilter.MinFilter(3)), dd, d2, x, y)
    return K.width


def simsek(cx, cy, boy, aci):
    """REF-072 VS arkasi: gokkusagi degrade simsek, beyaz kontur + isilti"""
    S = 3; w, h = int(boy * 0.62 * S), int(boy * S)
    pts = [(0.62, 0.0), (0.18, 0.52), (0.46, 0.52), (0.28, 1.0), (0.86, 0.38), (0.56, 0.38), (0.82, 0.0)]
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).polygon([(x * w, y * h) for x, y in pts], fill=255)
    dol = Image.fromarray(np.clip(gradyan(w, h, ["#ffe23a", "#ff7a3a", "#ff3ac8", "#8a5aff", "#3ad8ff"], dikey=True), 0, 255).astype(np.uint8)).convert("RGBA")
    K = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    K.paste(Image.new("RGBA", (w, h), "#ffffff"), (0, 0), m.filter(ImageFilter.MaxFilter(int(boy * S * 0.05) | 1)))
    K.paste(dol, (0, 0), m)
    K = K.resize((w // S, h // S), Image.LANCZOS).rotate(aci, resample=Image.BICUBIC, expand=True)
    g = Image.new("RGBA", K.size, "#ffd8ff"); g.putalpha(K.getchannel("A").filter(ImageFilter.GaussianBlur(boy * 0.08)))
    for q in (g, K):
        im.alpha_composite(q, (int(cx - K.width / 2), int(cy - K.height / 2)))


def parilti(cx, cy, r, n, rnd):
    d = ImageDraw.Draw(im)
    for _ in range(n):
        x, y = cx + rnd.uniform(-r, r), cy + rnd.uniform(-r, r); q = rnd.uniform(4, 9)
        renk = rnd.choice(("#ffffff", "#fff2a0", "#ffb8ec", "#a8f0ff"))
        d.polygon([(x, y - q * 1.8), (x + q * 0.35, y), (x, y + q * 1.8), (x - q * 0.35, y)], fill=renk)
        d.polygon([(x - q * 1.8, y), (x, y + q * 0.35), (x + q * 1.8, y), (x, y - q * 0.35)], fill=renk)


def vs(cx, cy, sol, sag):
    """REF-072: arkada simsek, onde iki ayri baloncuk harf (V sol oyuncunun, S sag oyuncunun renginde), cevrede parilti / yildiz"""
    rnd = np.random.default_rng(int(cx))
    global VS_M
    baloncuk("V", cx - 62, cy, 190, sol, kontur="#3a1478", ad="V")
    baloncuk("S", cx + 66, cy + 8, 190, sag, kontur="#3a1478", ad="S")
    simsek(cx + 2, cy + 18, 120, -8)     # REF-075: kucuk sari simsek V ile S arasinda, harflerin onunde
    VS_M = np.abs(np.asarray(im.convert("RGB")).astype(int) - ONCE.astype(int)).sum(2) > 30   # cakisma olcumu: yalniz harf + simsek
    parilti(cx, cy, 120, 10, rnd)


SIL_M = np.zeros((H, W), bool)
for kid, yuk, alan, sx, sy, sw, sb in OLCU:
    m_ = np.asarray(siluet_maske(kid).resize((sw, sb), Image.LANCZOS).filter(ImageFilter.MaxFilter(a.kontur))) > 127
    x1, y1 = min(W, sx + sw), min(H, sy + sb)
    SIL_M[sy:y1, sx:x1] |= m_[:y1 - sy, :x1 - sx]
ONCE = np.asarray(im.convert("RGB")).copy()
ARKA = im.copy()      # kontrast olcumu icin yazisiz zemin (siluetler dahil: yazinin arkasinda gorunen bu)
PEMBE = ["#ffb8ec", "#ff5ad0", "#ff2aa8"]; MAVI = ["#a8f0ff", "#3ac0ff", "#2a7aff"]; SARI = ["#fff4a0", "#ffd21a", "#ffa21a"]
VS_M = np.zeros((H, W), bool)       # REF-084: VS yok    # REF-075: tek VS = mavi V + pembe S, kapilarin arasinda

ONCE2 = np.asarray(im.convert("RGB")).copy()
# baslik en onde: REF-086 her harf ayri renk
HARF = [("H", ["#ff70c8", "#ff3aa8", "#e0107a"]), ("U", ["#ffb040", "#ff8a1a", "#e85a00"]), ("M", ["#ffee40", "#ffd400", "#f0a800"]),
        ("A", ["#80f050", "#3ad83a", "#10a020"]), ("N", ["#60eeff", "#18d8f0", "#0aa0d0"]), (" ", None),
        ("T", ["#60e0ff", "#28c8ff", "#1090e8"]), ("E", ["#90b8ff", "#6aa0ff", "#4a7aff"]), ("T", ["#c090ff", "#9a5aff", "#6a28e0"]),
        ("R", ["#f080f0", "#e04ae0", "#a020c0"]), ("I", ["#ff88c0", "#ff5aa8", "#ff3a8a"]), ("S", ["#ffc050", "#ffa21a", "#ff6a00"])]
fB = font(int(a.bas_boy)); ara = int(a.bas_boy * 0.03)
gen = [fB.getlength(c) if c != " " else a.bas_boy * 0.28 for c, _ in HARF]
top = sum(gen) + ara * (len(HARF) - 1); olc = min(1.0, (W - 70) / top)
x = W / 2 - top * olc / 2
for (c, renk), g in zip(HARF, gen):
    if renk:
        baloncuk(c, x + g * olc / 2, a.bas_y, a.bas_boy * olc, renk, kontur="#2e0f66", ad="harf-" + c, dikey=True)
    x += (g + ara) * olc
BAS_M = np.abs(np.asarray(im.convert("RGB")).astype(int) - ONCE2.astype(int)).sum(2) > 30

ONCE3 = np.asarray(im.convert("RGB")).copy()
# solda gosterge rozeti (REF-086 "Warm Up"): gokkusagi yarim daire + ibre, altinda baloncuk yazi
gx, gy = a.gosterge_xy; R = 92
gs = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dg = ImageDraw.Draw(gs)
dg.pieslice((gx - R - 12, gy - R - 42, gx + R + 12, gy + R - 18), 180, 360, fill=(46, 15, 102, 255))
dg.pieslice((gx - R - 6, gy - R - 36, gx + R + 6, gy + R - 24), 180, 360, fill=(255, 255, 255, 255))
for k, rr in enumerate(("#e8102c", "#ff7a10", "#ffd400", "#3ad83a", "#18c0ff")):
    dg.pieslice((gx - R, gy - R - 30, gx + R, gy + R - 30), 180 + 36 * k, 180 + 36 * (k + 1), fill=rr)
dg.pieslice((gx - R * 0.55, gy - R * 0.55 - 30, gx + R * 0.55, gy + R * 0.55 - 30), 180, 360, fill=(46, 15, 102, 255))
ang = math.radians(330)
dg.line((gx, gy - 30, gx + R * 0.85 * math.cos(ang), gy - 30 + R * 0.85 * math.sin(ang)), fill=(255, 255, 255, 255), width=9)
dg.ellipse((gx - 13, gy - 43, gx + 13, gy - 17), fill=(255, 255, 255, 255), outline=(46, 15, 102, 255), width=4)
im.alpha_composite(gs)
baloncuk("Warm Up", gx, gy + 18, 64, ["#fff27a", "#ffd21e", "#ff9a1a"], kontur="#2e0f66", hedef=270, ad="Warm Up")
# sagda kapak yazisi (REF-088 "1 Player / 9 MINS" yerine 1 PLAYER; sure yazilmaz)
baloncuk("1 PLAYER", a.yazi_xy[0], a.yazi_xy[1], 84, ["#ffffff", "#f4f0ff", "#ffffff"], kontur="#2e0f66", hedef=290, ad="1 PLAYER", dikey=True)
# sol altta kirmizi NEW rozeti (REF-088): tirtikli altin madalyon + iki kurdele + kirmizi halka icinde NEW
rx, ry = a.rozet_xy; R_ = 98
rz = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dz = ImageDraw.Draw(rz)
for s_ in (-1, 1):
    dz.polygon([(rx + s_ * 18, ry + 40), (rx + s_ * 70, ry + 150), (rx + s_ * 46, ry + 136), (rx + s_ * 34, ry + 168), (rx - s_ * 10, ry + 60)],
               fill=(220, 20, 40, 255), outline=(120, 0, 10, 255))
dis = []
for k in range(48):
    rr = R_ if k % 2 == 0 else R_ * 0.9; t_ = k * math.pi / 24
    dis.append((rx + rr * math.cos(t_), ry + rr * math.sin(t_)))
dz.polygon(dis, fill=(232, 24, 48, 255), outline=(130, 0, 12, 255))
gz = Image.fromarray(np.clip(gradyan(int(R_ * 1.5), int(R_ * 1.5), ["#ff7a7a", "#f02a3a", "#c00a1a"], dikey=True), 0, 255).astype(np.uint8)).convert("RGBA")
mk = Image.new("L", gz.size, 0); ImageDraw.Draw(mk).ellipse((0, 0, gz.width - 1, gz.height - 1), fill=255)
rz.paste(gz, (int(rx - gz.width / 2), int(ry - gz.height / 2)), mk)
dz.ellipse((rx - R_ * 0.62, ry - R_ * 0.62, rx + R_ * 0.62, ry + R_ * 0.62), outline=(255, 200, 40, 255), width=7)
im.alpha_composite(rz)
baloncuk("NEW", rx, ry + 2, 74, ["#ffffff", "#fff4f4", "#ffffff"], kontur="#4a0008", hedef=124, ad="NEW", dikey=True)   # md. 28: kirmizi dolgu altin zeminde 4,5 tutmuyor -> beyaz dolgu + koyu bordo kontur (olcum araci kucuk yazida kontur maskesi bulamiyor -> oran elle)
ROZ_M = np.abs(np.asarray(im.convert("RGB")).astype(int) - ONCE3.astype(int)).sum(2) > 30
print("rozet/yazi-siluet cakisma piksel:", int((ROZ_M & SIL_M).sum()))

kes = int((VS_M & SIL_M).sum())
print("baslik-siluet cakisma piksel:", int((BAS_M & SIL_M).sum()))
print("VS-siluet cakisma piksel:", kes, "TEMIZ" if kes == 0 else "DEGIYOR")
im.convert("RGB").save(a.cikti, quality=95)
print("->", a.cikti)
print("siluet toplam alan %%%.1f (REF-088 %%5,9; yukseklik %%79,9)" % sum(o[2] for o in OLCU))
for kid, yuk, alan, sx, sy, sw, sb in OLCU:
    print("siluet %s: yukseklik %%%.1f  alan %%%.1f  kutu %d,%d %dx%d" % (kid, yuk, alan, sx, sy, sw, sb))
# gecer (md. 28): dolgu/zemin >= 4,5 ya da kalin kontur yaziyi tasir: dolgu/kontur >= 4,5 ve kontur/zemin >= 3
for ad, r1, r2, r3 in KONTRAST:
    ok = r2 >= 4.5 or (r1 >= 4.5 and r3 >= 3)
    print("kontrast %-8s dolgu/zemin %4.1f  dolgu/kontur %4.1f  kontur/zemin %4.1f  %s" % (ad, r2, r1, r3, "GECER" if ok else "KALIR"))
print("kontrast: %d/%d yazi gecer" % (sum(1 for _, r1, r2, r3 in KONTRAST if r2 >= 4.5 or (r1 >= 4.5 and r3 >= 3)), len(KONTRAST)))

# harmanlama: siluet bu videonun onayli solo duvar maskesi (kapak siluet IoU kontrolu burada uygulanmaz)
