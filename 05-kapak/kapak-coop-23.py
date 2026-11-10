"""HUMAN TETRIS 23 kapagi (REF-078 HumanWarmUp, CO-OP 2 oyuncu, altigen neon tunel) - 1280x720.

    python kapak-coop-23.py --siluet D163069 D222008 --arka varlik-23-kapak-p0 --cikti A.jpg

REF-078 kapagi (olculdu 10 Kas 2026: doygunluk 0,727, parlaklik 0,544, renklilik 0,535, siyah 0,126, beyaz 0,059;
birlesik cift siluet yukseklik %81,4, genislik %64,0, alan %11,4 - koyu bilesen olcumu): ustte tum genislikte gokkusagi baloncuk HUMAN TETRIS;
sol ustte sari "2 Player", sagda sari numara; sol altta kirmizi rozet; arkada neon kopru + kafes kapida SARI DUVAR (uzerinde ayni cift pozu,
mor cizgili); onde birbirine degen iki simsiyah siluet + kalin beyaz kontur (uzun ayakta esneme + alcak egilme). VS YOK (CO-OP).
Arka plan Blender kapak modu (varlik-altigentunel.py). Siluetler onceki videolarin CC0 cizimleri (Y = OC-yoga-siluet, D = OC-dans-siluet/buyuk).
Alinmaz: "#89" (bizim numara 23), "NEW VERSION" yerine icerigi dogru rozet (md. 21 madde 7).
Cizim sirasi: arka plan -> sari duvardaki kucuk cift -> etiketler / rozet -> siluetler -> baslik.
"""
import argparse, json, math, os
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageEnhance
from scipy import ndimage

KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TP = os.path.join(KOK, "03-motor", "tetris-pvp")
REF = r"C:\Users\eleme\OneDrive\Masaüstü\REFERANSLAR"
KAYNAK = {"Y": ("OC-yoga-siluet", "%s-2000.png"), "D": ("OC-dans-siluet/buyuk", "%s.png"), "K": ("OC-dans-siluet", "%s-2000.png")}
p = argparse.ArgumentParser()
p.add_argument("--siluet", nargs=2, required=True, help="kaynak harfi + Openclipart id: sol sag, or. D163069")
p.add_argument("--ayna", nargs=2, type=int, default=[0, 0])
p.add_argument("--boy", nargs=2, type=float, default=[0.82, 0.50], help="siluet yuksekligi (kadraj orani)")
p.add_argument("--x", nargs=2, type=float, default=[0.42, 0.66], help="siluet merkezi (kadraj orani)")
p.add_argument("--arka", default="varlik-23-kapak-p0")
p.add_argument("--bas-y", type=float, default=72)
p.add_argument("--kontur", type=int, default=17)
p.add_argument("--renk", type=float, default=1.0); p.add_argument("--parlak", type=float, default=1.0)
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
im.alpha_composite(Image.open(os.path.join(V, "kapak-serit.png")).convert("RGBA").resize((W, H), Image.LANCZOS))
if a.renk != 1.0:
    im = ImageEnhance.Color(im).enhance(a.renk)
if a.parlak != 1.0:
    im = ImageEnhance.Brightness(im).enhance(a.parlak)
YER = json.load(open(os.path.join(V, "yerlesim.json"), encoding="utf-8")); OL = W / 1920


def siluet_maske(kid, ayna):
    """CC0 PNG (LA) -> alfa maske; 2x LANCZOS (kenar puruzsuz), kirpilmis"""
    kl, ad = KAYNAK[kid[0]]
    al = Image.open(os.path.join(REF, kl, ad % kid[1:])).convert("RGBA").getchannel("A")
    al = al.resize((al.width * 2, al.height * 2), Image.LANCZOS).point(lambda v: 255 if v > 110 else 0).filter(ImageFilter.GaussianBlur(1.0))
    if ayna:
        al = al.transpose(Image.FLIP_LEFT_RIGHT)
    return al.crop(al.getbbox())


def cift(yuk_px, boylar, xler, taban):
    """iki silueti ortak tabana oturtur -> (L maske, kutular); yuk_px = kadraj yuksekligi olcegi"""
    m = Image.new("L", (W, H), 0); kutu = []
    for i in (0, 1):
        ma = siluet_maske(a.siluet[i], a.ayna[i])
        sb = int(yuk_px * boylar[i]); sw = int(sb * ma.width / ma.height)
        sa = ma.resize((sw, sb), Image.LANCZOS)
        sx = int(xler[i] - sw / 2); sy = int(taban - sb)
        m.paste(255, (sx, sy), sa); kutu.append((sx, sy, sw, sb))
    return m, kutu


# sari duvardaki kucuk cift (REF-078: ayni poz, mor cizgili) - kapi acikliginin icinde
x0, y0, x1, y1 = [v * OL for v in YER["kapak-aciklik_p1"]]
dw, dh = x1 - x0, y1 - y0
ok_ = dh * 0.86 / (H * a.boy[0])
kucuk, _ = cift(H * ok_, a.boy, [x0 + dw / 2 + (a.x[i] - sum(a.x) / 2) * W * ok_ for i in (0, 1)], y1 - dh * 0.04)
cizgi = np.zeros((H, W, 4), np.uint8)
xx = np.arange(W)[None, :].repeat(H, 0)
cizgi[..., :3] = np.where(((xx // 4) % 2 == 0)[..., None], np.array([74, 20, 110], np.uint8), np.array([150, 40, 170], np.uint8)); cizgi[..., 3] = 255
im.paste(Image.fromarray(cizgi), (0, 0), kucuk)

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


def baloncuk(metin, cx, cy, boy, renkler, kontur="#4a1f86", hedef=None, aci=0, ad=None):
    """baloncuk yazi: yatay cok renkli degrade, kalin mor dis kontur, ustte cam yansimasi, beyaz ince ic hat"""
    S = 2; fS = font(boy * S)
    bx = fS.getbbox(metin); tw, th = bx[2] - bx[0], bx[3] - bx[1]
    pad = int(boy * S * 0.3); w, h = tw + 2 * pad, th + 2 * pad
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).text((pad - bx[0], pad - bx[1]), metin, font=fS, fill=255)
    dis = Image.new("L", (w, h), 0); ImageDraw.Draw(dis).text((pad - bx[0], pad - bx[1]), metin, font=fS, fill=255, stroke_width=int(boy * S * 0.085), stroke_fill=255)
    ic = Image.new("L", (w, h), 0); ImageDraw.Draw(ic).text((pad - bx[0], pad - bx[1]), metin, font=fS, fill=255, stroke_width=int(boy * S * 0.02), stroke_fill=255)
    # md. 28 (6 Kas 2026): mor kontur koyu gokte / siyah siluette kayboluyordu -> disina beyaz ikinci kontur (REF-072 basligi gibi)
    dis2 = Image.new("L", (w, h), 0); ImageDraw.Draw(dis2).text((pad - bx[0], pad - bx[1]), metin, font=fS, fill=255, stroke_width=int(boy * S * 0.125), stroke_fill=255)
    rgb = gradyan(w, h, renkler)
    yy = np.linspace(0, 1, h)[:, None]
    rgb = rgb * (0.92 + 0.22 * (1 - yy))[..., None].clip(0, 1.15)
    dol = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).convert("RGBA")
    K = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    K.paste(Image.new("RGBA", (w, h), (30, 6, 70, 150)), (int(boy * S * 0.03), int(boy * S * 0.06)), dis2)
    K.paste(Image.new("RGBA", (w, h), "#ffffff"), (0, 0), dis2)
    K.paste(Image.new("RGBA", (w, h), kontur), (0, 0), dis)
    K.paste(Image.new("RGBA", (w, h), "#ffffff"), (0, 0), ic)
    K.paste(dol, (0, 0), m)
    yans = Image.new("L", (w, h), 0); ImageDraw.Draw(yans).rectangle((0, pad + int(th * 0.06), w, pad + int(th * 0.36)), fill=110)
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


def parilti(cx, cy, r, n, rnd):
    d = ImageDraw.Draw(im)
    for _ in range(n):
        x, y = cx + rnd.uniform(-r, r), cy + rnd.uniform(-r, r); q = rnd.uniform(4, 9)
        renk = rnd.choice(("#ffffff", "#fff2a0", "#ffb8ec", "#a8f0ff"))
        d.polygon([(x, y - q * 1.8), (x + q * 0.35, y), (x, y + q * 1.8), (x - q * 0.35, y)], fill=renk)
        d.polygon([(x - q * 1.8, y), (x, y + q * 0.35), (x + q * 1.8, y), (x, y - q * 0.35)], fill=renk)

def rozet(cx, cy):
    """REF-078 sol alt: kirmizi kalkan rozet, altin kenar, iki satir yazi (icerik dogru: yeni gorevler)"""
    w, h = 250, 215; S = 2
    K = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(K)
    pts = [(0.06, 0.04), (0.94, 0.04), (0.94, 0.62), (0.5, 0.97), (0.06, 0.62)]
    d.polygon([(x * w * S, y * h * S) for x, y in pts], fill="#ffc21a")
    pts2 = [(0.1, 0.09), (0.9, 0.09), (0.9, 0.6), (0.5, 0.91), (0.1, 0.6)]
    d.polygon([(x * w * S, y * h * S) for x, y in pts2], fill="#a80a1c")
    K = K.resize((w, h), Image.LANCZOS)
    im.alpha_composite(K, (int(cx - w / 2), int(cy - h / 2)))
    global ARKA
    ARKA = im.copy()
    baloncuk("NEW", cx, cy - 52, 62, ["#fff6a0", "#ffe23a", "#ffd21a"], kontur="#5a0a10", ad="NEW")
    baloncuk("MISSIONS", cx, cy + 20, 38, ["#ffffff", "#ffffff"], kontur="#5a0a10", ad="MISSIONS")


ARKA = im.copy()
SARI = ["#fff6a0", "#ffd21a", "#ffa21a"]
baloncuk("2 Player", 262, 190, 78, SARI, kontur="#3a1478", ad="2 Player")
baloncuk("#23", 1150, 190, 84, SARI, kontur="#3a1478", ad="#23")
rozet(175, 540)

# on plan: birbirine degen iki siluet, ortak taban (alt kenar)
buyuk, KUTU = cift(H, a.boy, [W * v for v in a.x], H - 8)
kont = buyuk.filter(ImageFilter.MaxFilter(a.kontur))
im.paste((255, 255, 255, 255), (0, 0), kont)
im.paste((0, 0, 0, 255), (0, 0), buyuk)
SIL_M = np.asarray(kont) > 127
ARKA = im.copy()
ONCE2 = np.asarray(im.convert("RGB")).copy()
# baslik en onde, tum genislikte gokkusagi (REF-078 harf renkleri: pembe, sari, mavi, yesil, mor ...)
baloncuk("HUMAN", 345, a.bas_y, 150, ["#ff2aa8", "#ff8a1a", "#ffe01a", "#3ae05a", "#2ac0ff"], hedef=560)
baloncuk("TETRIS", 950, a.bas_y, 150, ["#ff2aa8", "#ffd21a", "#2ac0ff", "#a04aff", "#3ae05a", "#2ac0ff"], hedef=560)
BAS_M = np.abs(np.asarray(im.convert("RGB")).astype(int) - ONCE2.astype(int)).sum(2) > 30
print("baslik-siluet cakisma piksel:", int((BAS_M & SIL_M).sum()))
im.convert("RGB").save(a.cikti, quality=95)
print("->", a.cikti)
sm = np.asarray(buyuk) > 127
lab, n = ndimage.label(sm); ys, xs = np.where(sm)
print("cift siluet: yukseklik %%%.1f  genislik %%%.1f  alan %%%.1f  bilesen %d (1 = degiyor)" % ((ys.max() - ys.min()) / H * 100, (xs.max() - xs.min()) / W * 100, sm.sum() / (W * H) * 100, n))
for ad, r1, r2, r3 in KONTRAST:
    ok = r2 >= 4.5 or (r1 >= 4.5 and r3 >= 3)
    print("kontrast %-9s dolgu/zemin %4.1f  dolgu/kontur %4.1f  kontur/zemin %4.1f  %s" % (ad, r2, r1, r3, "GECER" if ok else "KALIR"))
print("kontrast: %d/%d yazi gecer" % (sum(1 for _, r1, r2, r3 in KONTRAST if r2 >= 4.5 or (r1 >= 4.5 and r3 >= 3)), len(KONTRAST)))
