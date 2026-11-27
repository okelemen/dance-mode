"""HUMAN TETRIS 41 kapagi (REF-093 duzeni, 1P SOLO, col vahasi, cilali 3D oyun gorunumu) - 1280x720.

    python kapak-x1-41.py --poz broom-side-lunge-cactus --arka varlik-41-kapak-g0 --cikti A.jpg

kapak-x1-40'tan. REF-093 kapagi (27 Kas olcum: doygunluk 0,685 / parlaklik 0,567 / renklilik 0,520; siluet yukseklik %78,5, alan %11,7
TEK siluet): ustte gokkusagi harf harf baloncuk HUMAN TETRIS (her harf ayri renk), solda mavi hap icinde beyaz "x1 Player", sagda
beyaz-leylak "#88" (bizde #41), sol altta altin tirtikli NEW rozeti (kirmizi halka, kirmizi NEW, altin kurdeleler), ortada truss kapinin
icinde SARI pano + ayni pozun koyu hayaleti, onde TEK dev siyah siluet kalin beyaz konturlu, arkada mor neon tunel (bizde vahanin kendisi).
MOBIL KURAL (md. 30): siluet REF'ten buyuk (hedef yukseklik >= %80), kamera yakin, arka plan sade. Asagidaki 40 notu tarihce.
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
p.add_argument("--poz", required=True, help="varlik-41s1/poz solo maske (ad, .png yok)")
p.add_argument("--boy", type=float, default=0.86, help="on siluet yuksekligi (kadraj orani)")
p.add_argument("--maks-gen", type=float, default=0.62)
p.add_argument("--x", type=float, default=0.42)
p.add_argument("--arka", default="varlik-41-kapak-g0")
p.add_argument("--bas-boy", type=float, default=150)
p.add_argument("--bas-y", type=float, default=74); p.add_argument("--tasma", type=float, default=0.0)
p.add_argument("--kontur", type=int, default=13)
p.add_argument("--renk", type=float, default=1.0); p.add_argument("--parlak", type=float, default=1.0)
p.add_argument("--yansima", type=int, default=70, help="baloncuk cam yansimasi gucu (0-255)")
p.add_argument("--pano", nargs=4, type=float, default=[600, 160, 940, 390], help="truss icindeki yesil pano x0 y0 x1 y1")
p.add_argument("--rozet-xy", nargs=2, type=float, default=[140, 560])
p.add_argument("--yazi-xy", nargs=2, type=float, default=[985, 168], help="#41 merkezi")
p.add_argument("--gosterge-xy", nargs=2, type=float, default=[205, 160], help="x1 Player merkezi")
p.add_argument("--hayalet", type=float, default=0.75, help="portaldaki beyaz hayalet pozun ortme orani")
p.add_argument("--hayalet-x", type=float, default=0.5, help="hayaletin portal icindeki yatay yeri (0-1)")
p.add_argument("--pano-saydam", type=float, default=0.6, help="portal degradesinin ortme orani (1 = duz pano)")
p.add_argument("--pano-elle", type=int, default=1, help="1 = REF-093 gibi --pano dikdortgeninde kucuk truss pano (kapi acikligi kadraji kapliyordu)")
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
    al = Image.open(os.path.join(TP, "varlik-41s1", "poz", ad + ".png")).convert("RGBA").getchannel("A")
    al = al.resize((al.width * 2, al.height * 2), Image.LANCZOS).point(lambda v: 255 if v > 110 else 0).filter(ImageFilter.GaussianBlur(1.0))
    if ayna:
        al = al.transpose(Image.FLIP_LEFT_RIGHT)
    return al.crop(al.getbbox())


def gradyan(w, h, renkler, dikey=False):
    t = (np.linspace(0, 1, h)[:, None].repeat(w, 1) if dikey else np.linspace(0, 1, w)[None, :].repeat(h, 0))
    cs = [np.array([int(c[i:i + 2], 16) for i in (1, 3, 5)], np.float32) for c in renkler]
    pos = np.linspace(0, 1, len(cs)); rgb = np.zeros((h, w, 3), np.float32)
    for ch in range(3):
        rgb[..., ch] = np.interp(t, pos, [c[ch] for c in cs])
    return rgb


def pano_hayalet():
    """REF-090: kapinin acikliginda pembe-mor-camgobegi degrade pano + ayni pozun beyaz yari saydam hayaleti"""
    ol = W / Image.open(os.path.join(V, "kapak-gok.png")).width          # yerlesim render pikselinde (1920) -> kapak 1280
    x0, y0, x1, y1 = [int(v * ol) for v in YER["kapak-aciklik_p1"]]
    if a.pano_elle:                                                       # HT41: REF-093 truss pano (gri kafes cerceve + sari pano)
        x0, y0, x1, y1 = [int(v) for v in a.pano]
        dt = ImageDraw.Draw(im); t_ = 14
        for (qa, qb, qc, qd) in ((x0 - t_, y0 - t_, x1 + t_, y0), (x0 - t_, y1, x1 + t_, y1 + t_), (x0 - t_, y0, x0, y1), (x1, y0, x1 + t_, y1)):
            dt.rectangle((qa, qb, qc, qd), fill=(150, 156, 170, 255), outline=(40, 40, 60, 255), width=2)
        for xx in range(x0 - t_, x1 + t_, 18):
            dt.line((xx, y0 - t_, xx + 12, y0), fill=(70, 74, 90, 255), width=2)
        for yy in range(y0, y1, 18):
            dt.line((x0 - t_, yy, x0, yy + 12), fill=(70, 74, 90, 255), width=2); dt.line((x1, yy, x1 + t_, yy + 12), fill=(70, 74, 90, 255), width=2)
    w_, h_ = x1 - x0, y1 - y0
    g = Image.fromarray(np.clip(gradyan(w_, h_, ["#fff04a", "#ffd81a", "#ffc20a"], dikey=True), 0, 255).astype(np.uint8)).convert("RGBA")   # REF-093: sari pano
    g = Image.blend(im.crop((x0, y0, x1, y1)), g, a.pano_saydam)          # REF-090: portal saydam isik, arkadaki koy/isiklar gorunur
    im.alpha_composite(g, (x0, y0))
    ma = siluet_maske(a.poz); ph = int(h_ * 0.86); pw = int(ph * ma.width / ma.height)
    if pw > w_ * 0.86:
        pw = int(w_ * 0.86); ph = int(pw * ma.height / ma.width)
    hm = ma.resize((pw, ph), Image.LANCZOS).point(lambda v: int(v * a.hayalet))
    im.paste((14, 20, 60, 255), (int(x0 + w_ * a.hayalet_x - pw / 2), int(y1 - ph - h_ * 0.04)), hm)   # REF-093: sari panoda koyu lacivert poz


OLCU = []
pano_hayalet()
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


def baloncuk(metin, cx, cy, boy, renkler, kontur="#4a1f86", hedef=None, aci=0, ad=None, dikey=False, desen=None):
    """baloncuk yazi: yatay cok renkli degrade, kalin mor dis kontur, ustte cam yansimasi, beyaz ince ic hat.
    desen (REF-092): "serit" = seker kamisi beyaz capraz serit, "kar" = beyaz kar taneleri"""
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
    if desen:
        dm_ = Image.new("L", (w, h), 0); dd_ = ImageDraw.Draw(dm_); u = boy * S
        if desen == "serit":
            for k in range(-h, w + h, int(u * 0.36)):
                dd_.polygon([(k, h), (k + int(u * 0.15), h), (k + int(u * 0.15) + h, 0), (k + h, 0)], fill=235)
        else:
            rn = np.random.default_rng(7)
            for _ in range(4):
                qx, qy, q = rn.uniform(0.25, 0.75) * w, rn.uniform(0.3, 0.8) * h, u * rn.uniform(0.07, 0.11)
                for t_ in range(3):
                    an = t_ * math.pi / 3
                    dd_.line((qx - q * math.cos(an), qy - q * math.sin(an), qx + q * math.cos(an), qy + q * math.sin(an)), fill=245, width=max(3, int(u * 0.025)))
        K.paste(Image.new("RGBA", (w, h), "#ffffff"), (0, 0), ImageChops.multiply(dm_, m.filter(ImageFilter.MinFilter(int(u * 0.03) | 1))))
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
KIR, ALT, YES, BYZ, MAV = ["#ff3a4a", "#f0102a", "#b00010"], ["#ffe01a", "#ffc000", "#f08a00"], ["#3ae04a", "#10c030", "#088a20"], ["#ff5ab8", "#ff2a90", "#d0006a"], ["#3ad0ff", "#109aff", "#0a5adf"]   # 25 Kas: pastel/beyaz harf kapagi soldurdu (0,48) -> REF-090 gibi doygun seker renkleri
TUR, CAM, MOR = ["#ffb03a", "#ff8a0a", "#e05a00"], ["#5af0e0", "#10d0c8", "#0a9aa8"], ["#d88aff", "#a83aff", "#7a10e0"]
HARF = [("H", KIR), ("U", TUR), ("M", ALT), ("A", YES), ("N", CAM), (" ", None), ("T", MAV), ("E", MOR), ("T", BYZ), ("R", TUR), ("I", KIR), ("S", YES)]   # REF-093 gokkusagi harfleri
fB = font(int(a.bas_boy)); ara = int(a.bas_boy * 0.03)
gen = [fB.getlength(c) if c != " " else a.bas_boy * 0.28 for c, _ in HARF]
top = sum(gen) + ara * (len(HARF) - 1); olc = min(1.0, (W - 70) / top)
x = W / 2 - top * olc / 2
KAR_KAP = []
DESEN = {}                                            # REF-093: duz parlak harfler
for j_, ((c, renk), g) in enumerate(zip(HARF, gen)):
    if renk:
        baloncuk(c, x + g * olc / 2, a.bas_y, a.bas_boy * olc, renk, kontur="#10022a", ad="harf-" + c, dikey=True, desen=DESEN.get(j_))
        KAR_KAP.append((x + g * olc / 2, g * olc))
    x += (g + ara) * olc
BAS_M = np.abs(np.asarray(im.convert("RGB")).astype(int) - ONCE2.astype(int)).sum(2) > 30

ONCE3 = np.asarray(im.convert("RGB")).copy()
# REF-092: solda beyaz "1 Player" + pembe-mor neon alt cizgi, sagda kirmizi "Christmas Version" + altin isilti cizgisi; NEW rozeti yok
def neon_cizgi(x0, x1, y, renkler, kalin, egri=10):
    """hafif kavisli parlak alt cizgi: genis yumusak hare + ince parlak cekirdek"""
    w_, h_ = int(x1 - x0) + 40, kalin * 6 + egri * 2
    m = Image.new("L", (w_, h_), 0); d = ImageDraw.Draw(m)
    pts = [(20 + t * (w_ - 40), h_ / 2 + egri * math.sin(t * math.pi) - egri / 2) for t in np.linspace(0, 1, 40)]
    d.line(pts, fill=255, width=kalin, joint="curve")
    g = Image.fromarray(np.clip(gradyan(w_, h_, renkler), 0, 255).astype(np.uint8)).convert("RGBA")
    hare = g.copy(); hare.putalpha(m.filter(ImageFilter.MaxFilter(kalin | 1)).filter(ImageFilter.GaussianBlur(kalin * 1.2)))
    cek = g.copy(); cek.putalpha(m)
    ic = Image.new("RGBA", (w_, h_), "#ffffff"); ic.putalpha(m.filter(ImageFilter.MinFilter(3)).point(lambda v: int(v * 0.7)))
    for q in (hare, hare, cek, ic):
        im.alpha_composite(q, (int(x0 - 20), int(y - h_ / 2)))


gx, gy = a.gosterge_xy                                              # REF-093: mavi hap (acik mavi -> koyu mavi), beyaz kontur, icinde x1 Player
hap = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dh = ImageDraw.Draw(hap)
dh.rounded_rectangle((gx - 175, gy - 50, gx + 175, gy + 50), radius=50, fill=(255, 255, 255, 255))
hg = Image.fromarray(np.clip(gradyan(340, 90, ["#5ac8ff", "#1a7aff", "#0a3ad8"], dikey=True), 0, 255).astype(np.uint8)).convert("RGBA")
hm_ = Image.new("L", (340, 90), 0); ImageDraw.Draw(hm_).rounded_rectangle((0, 0, 339, 89), radius=45, fill=255)
hap.paste(hg, (int(gx - 170), int(gy - 45)), hm_)
gl = Image.new("RGBA", (W, H), (60, 160, 255, 0)); gl.putalpha(hap.getchannel("A").filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.8)))
im.alpha_composite(gl); im.alpha_composite(hap)
baloncuk("x1 Player", gx, gy - 2, 66, ["#ffffff", "#f4f8ff", "#e0ecff"], kontur="#0a1a5a", hedef=300, ad="x1 Player", dikey=True)
baloncuk("#41", a.yazi_xy[0], a.yazi_xy[1], 120, ["#ffffff", "#f0e8ff", "#c8b0ff"], kontur="#3a0a6a", hedef=240, ad="#41", dikey=True)   # REF-093: beyaz-leylak numara
rx, ry = a.rozet_xy; R_ = 92                                         # REF-093: altin tirtikli NEW rozeti + altin kurdeleler
rz = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dz = ImageDraw.Draw(rz)
for s_ in (-1, 1):
    dz.polygon([(rx + s_ * 18, ry + 40), (rx + s_ * 70, ry + 150), (rx + s_ * 46, ry + 136), (rx + s_ * 34, ry + 168), (rx - s_ * 10, ry + 60)],
               fill=(255, 196, 30, 255), outline=(140, 80, 0, 255))
dis = []
for k in range(48):
    rr = R_ if k % 2 == 0 else R_ * 0.9; t_ = k * math.pi / 24
    dis.append((rx + rr * math.cos(t_), ry + rr * math.sin(t_)))
dz.polygon(dis, fill=(255, 200, 30, 255), outline=(150, 90, 0, 255))
gz = Image.fromarray(np.clip(gradyan(int(R_ * 1.45), int(R_ * 1.45), ["#fff6c0", "#ffe070", "#ffc020"], dikey=True), 0, 255).astype(np.uint8)).convert("RGBA")
mk = Image.new("L", gz.size, 0); ImageDraw.Draw(mk).ellipse((0, 0, gz.width - 1, gz.height - 1), fill=255)
rz.paste(gz, (int(rx - gz.width / 2), int(ry - gz.height / 2)), mk)
dz.ellipse((rx - R_ * 0.66, ry - R_ * 0.66, rx + R_ * 0.66, ry + R_ * 0.66), outline=(220, 20, 40, 255), width=8)
im.alpha_composite(rz)
baloncuk("NEW", rx, ry + 2, 72, ["#ff5a5a", "#f01a2a", "#c0000e"], kontur="#ffffff", hedef=120, ad="NEW", dikey=True)   # REF-093: kirmizi NEW, beyaz kontur
ROZ_M = np.abs(np.asarray(im.convert("RGB")).astype(int) - ONCE3.astype(int)).sum(2) > 30
print("yazi/rozet-siluet cakisma piksel:", int((ROZ_M & SIL_M).sum()))

kes = int((VS_M & SIL_M).sum())
print("baslik-siluet cakisma piksel:", int((BAS_M & SIL_M).sum()))
print("VS-siluet cakisma piksel:", kes, "TEMIZ" if kes == 0 else "DEGIYOR")
im.convert("RGB").save(a.cikti, quality=95)
print("->", a.cikti)
print("siluet toplam alan %%%.1f (REF-093 %%11,7 tek siluet; yukseklik %%78,5)" % sum(o[2] for o in OLCU))
for kid, yuk, alan, sx, sy, sw, sb in OLCU:
    print("siluet %s: yukseklik %%%.1f  alan %%%.1f  kutu %d,%d %dx%d" % (kid, yuk, alan, sx, sy, sw, sb))
# gecer (md. 28): dolgu/zemin >= 4,5 ya da kalin kontur yaziyi tasir: dolgu/kontur >= 4,5 ve kontur/zemin >= 3
for ad, r1, r2, r3 in KONTRAST:
    ok = r2 >= 4.5 or (r1 >= 4.5 and r3 >= 3)
    print("kontrast %-8s dolgu/zemin %4.1f  dolgu/kontur %4.1f  kontur/zemin %4.1f  %s" % (ad, r2, r1, r3, "GECER" if ok else "KALIR"))
print("kontrast: %d/%d yazi gecer" % (sum(1 for _, r1, r2, r3 in KONTRAST if r2 >= 4.5 or (r1 >= 4.5 and r3 >= 3)), len(KONTRAST)))

# harmanlama: siluet bu videonun onayli solo duvar maskesi (kapak siluet IoU kontrolu burada uygulanmaz)
