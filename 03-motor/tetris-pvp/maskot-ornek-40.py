"""HUMAN TETRIS 40 fok yavrusu hakem maskot ornek sayfasi (TALIMATLAR §4: on/yan, 3-4 poz, 3 duygu)
-> POZ-DUVARI/taslak/HUMAN-TETRIS-40-MASKOT-ORNEK.jpg

38-39 yontemi: TAMAMI 2B cizgi film; hareket karakter.py --eklem 1 eklem verisi (gercek mocap/poz acilari, Masaustu md. 18);
38'in eklem kosusu ornek sayfasi icin yeniden kullanilir; video icin 40 pozlariyla yeni kosu alinir.
Tasarim (kendi tasarimimiz; bilinen fok karakterlerine benzemez):
- tombul damla govde (uyluklari orter), beyaz fok yavrusu postu + mavi-lila golge, lacivert kontur (doygun mavi buzda en okunur;
  ornek 1 karamel+benek kedi/leopar gibi okundu)
- uzuvlar kisa tombul; eller genis on yuzgec, ayaklar arka yuzgec (yelpaze, ucta 3 bogum)
- bas: buyuk yuvarlak, iri parlak goz, ucgen burun, burun yastiklari + biyiklar, pembe yanak
- kis + hakem isareti: kirmizi orgu atki (yesil benek deseni, prompts.chat "Matryoshka Fox Family"), kirmizi ponponlu bere, altin duduk
"""
import json, math, os, sys
from PIL import Image, ImageDraw, ImageFont

BURA = os.path.dirname(os.path.abspath(__file__))
ON = os.path.join(BURA, sys.argv[1] if len(sys.argv) > 1 else "varlik-38-maskot2b-on/tetris-varlik")
YAN = os.path.join(BURA, sys.argv[2] if len(sys.argv) > 2 else "varlik-38-maskot2b-yan/tetris-varlik")
OLCEK = float(sys.argv[3]) if len(sys.argv) > 3 else 2.5
DY = float(sys.argv[4]) if len(sys.argv) > 4 else -8.0
S2 = 4
KN = "#1a2040"                                                 # koyu lacivert kontur
POST, POST_K, BENEK = "#f6f8ff", "#c4d0ec", "#d8e0f4"          # beyaz fok yavrusu postu / mavi-lila golge / hafif ton
KARIN = "#ffffff"                                              # parlak beyaz karin
YUZGEC = "#7a88b0"                                             # yuzgec bogum cizgisi
ATKI, ATKI_K, ATKI_D = "#e81a2a", "#a80a1a", "#18a848"         # kirmizi atki / koyu / yesil desen
BERE, PONPON, DUDUK = "#e81a2a", "#ffffff", "#ffc21a"


def bas(dr, cx, cy, u, duygu, yan=False):
    S = lambda v: v * u * S2
    X = lambda v: (cx + v * u) * S2
    Y = lambda v: (cy + v * u) * S2
    def el(x, y, rx, ry, **k): dr.ellipse((X(x) - S(rx), Y(y) - S(ry), X(x) + S(rx), Y(y) + S(ry)), **k)
    w = int(S(1.6))
    def bere(ox):
        dr.chord((X(ox - 17), Y(-34), X(ox + 17), Y(-6)), 180, 360, fill=BERE, outline=KN, width=int(S(1.3)))
        dr.rounded_rectangle((X(ox - 18), Y(-22), X(ox + 18), Y(-15)), radius=S(3), fill="#ffffff", outline=KN, width=int(S(1.1)))
        el(ox, -35, 5, 5, fill=PONPON, outline=KN, width=int(S(1.1)))
    if yan:
        el(2, 0, 20, 19, fill=POST, outline=KN, width=w)
        el(15, 6, 9, 7, fill=KARIN, outline=KN, width=int(S(1.1)))                # one uzanan burun
        el(22, 3, 3.2, 2.4, fill="#101018")
        for k in (-1, 1):
            dr.line((X(16), Y(8 + k), X(29), Y(7 + k * 4)), fill=KN, width=int(S(0.8)))
        el(7, -3, 5.5, 6.5, fill="#ffffff", outline=KN, width=int(S(1.2))); el(8.5, -2.4, 3.8, 4.6, fill=KN); el(7.2, -4.8, 1.3, 1.3, fill="#ffffff")
        el(6, 8, 3.0, 1.9, fill="#ff8a9a")
        bere(-1)
        return
    el(0, 0, 23, 21, fill=POST, outline=KN, width=w)                    # yuvarlak karamel bas
    for sx in (-1, 1):
        if duygu == "sevinc":
            dr.arc((X(sx * 9) - S(5.5), Y(-3) - S(5.5), X(sx * 9) + S(5.5), Y(-3) + S(5.5)), 200, 340, fill=KN, width=int(S(2.6)))
        elif duygu == "sasirma":
            el(sx * 9, -4, 6.5, 7.5, fill="#ffffff", outline=KN, width=int(S(1.4))); el(sx * 9, -4, 2.6, 2.8, fill=KN)
        else:
            el(sx * 9, -3, 6.2, 7.2, fill="#ffffff", outline=KN, width=int(S(1.4)))
            el(sx * 9 + 0.7, -2.4, 4.2, 5.0, fill=KN); el(sx * 9 - 0.8, -4.8, 1.6, 1.6, fill="#ffffff")
        el(sx * 16, 6, 3.6, 2.2, fill="#ff7a9a")
    el(-4.2, 9, 5.2, 4.2, fill=KARIN, outline=KN, width=int(S(1.0)))   # burun yastiklari
    el(4.2, 9, 5.2, 4.2, fill=KARIN, outline=KN, width=int(S(1.0)))
    for sx in (-1, 1):
        for k, dy in enumerate((-1.5, 1.0, 3.5)):
            el(sx * (3 + k * 1.6), 8.6 + dy * 0.5, 0.55, 0.55, fill=BENEK)
            dr.line((X(sx * 8), Y(8.5 + dy), X(sx * 20), Y(6 + dy * 2.2)), fill=KN, width=int(S(0.8)))   # biyiklar
    dr.polygon([(X(-3.2), Y(4.2)), (X(3.2), Y(4.2)), (X(0), Y(8.0))], fill="#101018")
    if duygu == "sasirma":
        el(0, 15, 3.0, 2.8, fill="#7a1020", outline=KN, width=int(S(1.0)))
    elif duygu == "sevinc":
        dr.chord((X(-6), Y(11), X(6), Y(19)), 0, 180, fill="#7a1020", outline=KN, width=int(S(1.2)))
    else:
        dr.arc((X(-4.5), Y(10), X(0.2), Y(15)), 0, 160, fill=KN, width=int(S(1.3)))
        dr.arc((X(-0.2), Y(10), X(4.5), Y(15)), 20, 180, fill=KN, width=int(S(1.3)))
    bere(0)


def cizici(dr, boy):
    KON = max(2, boy * 0.018) * S2
    P = lambda p: (p[0] * S2, p[1] * S2)

    def kapsul(a, b, ra, rb, renk, kontur=True):
        a, b = P(a), P(b); ra, rb = ra * S2, rb * S2
        dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        for gec, (r_a, r_b, c) in enumerate(((ra + KON, rb + KON, KN), (ra, rb, renk))):
            if gec == 0 and not kontur:
                continue
            poly = [(a[0] + nx * r_a, a[1] + ny * r_a), (b[0] + nx * r_b, b[1] + ny * r_b), (b[0] - nx * r_b, b[1] - ny * r_b), (a[0] - nx * r_a, a[1] - ny * r_a)]
            dr.polygon(poly, fill=c)
            dr.ellipse((a[0] - r_a, a[1] - r_a, a[0] + r_a, a[1] + r_a), fill=c)
            dr.ellipse((b[0] - r_b, b[1] - r_b, b[0] + r_b, b[1] + r_b), fill=c)

    def uzuv(segs, renk):
        for a_, b_, r1, r2, _ in segs:
            kapsul(a_, b_, max(0.5, r1) + KON / S2, max(0.5, r2) + KON / S2, KN, kontur=False)
        for a_, b_, r1, r2, c in segs:
            kapsul(a_, b_, max(0.5, r1), max(0.5, r2), c or renk, kontur=False)

    def elips(m, rx, ry, aci, renk, kontur=True, n=48):
        cx, cy = P(m)
        for gec, (ex, c) in enumerate(((KON, KN), (0, renk))):
            if gec == 0 and not kontur:
                continue
            pts = []
            for i in range(n):
                t = 2 * math.pi * i / n
                x, y = (max(0.5, rx) * S2 + ex) * math.cos(t), (max(0.5, ry) * S2 + ex) * math.sin(t)
                pts.append((cx + x * math.cos(aci) - y * math.sin(aci), cy + x * math.sin(aci) + y * math.cos(aci)))
            dr.polygon(pts, fill=c)
    return kapsul, elips, uzuv, KON


def govde_ciz(dr, E, boy, yan=False):
    kapsul, elips, uzuv, KON = cizici(dr, boy)
    g = lambda k: E[k]
    ru, rl = boy * 0.1, boy * 0.088                                  # tombul bacak (39 dersi: ince insan gibi okunur)
    ra, rf_ = boy * 0.08, boy * 0.072
    taraf = ("Left", "Right")
    if yan:
        taraf = tuple(sorted(taraf, key=lambda t: g(t + "UpLeg")[0]))
    def yelpaze(m, aci, rx, ry, renk):                                # yuzgec: elips + ucta 3 koyu bogum cizgisi
        elips(m, rx, ry, aci, renk)
        for k in (-0.5, 0, 0.5):
            a2 = aci + k * 0.5
            kapsul((m[0] + math.cos(a2) * rx * 0.25, m[1] + math.sin(a2) * rx * 0.25),
                   (m[0] + math.cos(a2) * rx * 0.85, m[1] + math.sin(a2) * rx * 0.85), boy * 0.006, boy * 0.006, YUZGEC, kontur=False)
    def bacak(t, renk):
        uzuv([(g(t + "UpLeg"), g(t + "Leg"), ru, rl * 1.05, None), (g(t + "Leg"), g(t + "Foot"), rl * 1.05, rl, None)], renk)
        f, fu = g(t + "Foot"), g(t + "Foot_uc")                       # arka yuzgec (yelpaze ayak)
        yelpaze(((f[0] + fu[0]) / 2, (f[1] + fu[1]) / 2), math.atan2(fu[1] - f[1], fu[0] - f[0]), boy * 0.12, boy * 0.07, renk)
    def kol(t, renk):
        uzuv([(g(t + "Arm"), g(t + "ForeArm"), ra, rf_ * 1.05, None), (g(t + "ForeArm"), g(t + "Hand"), rf_ * 1.05, rf_, None)], renk)
        h, hu = g(t + "Hand"), g(t + "Hand_uc")                       # genis on yuzgec
        aci = math.atan2(hu[1] - h[1], hu[0] - h[0])
        yelpaze((h[0] + (hu[0] - h[0]) * 0.9, h[1] + (hu[1] - h[1]) * 0.9), aci, boy * 0.12, boy * 0.068, renk)
    hx, hy = g("Hips"); nx_, ny_ = g("Neck"); bx = g("Head")[0]
    aci = math.atan2(ny_ - hy, nx_ - hx) + math.pi / 2
    L = math.hypot(nx_ - hx, ny_ - hy)
    mx, my = hx * 0.72 + nx_ * 0.28, hy * 0.72 + ny_ * 0.28
    yon = math.copysign(1, bx - hx) if yan else 0
    bacak(taraf[0], POST_K); bacak(taraf[1], POST_K); kol(taraf[0], POST_K)
    # tombul damla govde: kalcada genis, boyuna dogru daralan (iki elips; ust elips konturu alttakinin icinde kalir)
    elips((mx, my - L * 0.38), boy * (0.19 if yan else 0.22), L * 0.5, aci, POST)
    elips((mx - yon * boy * 0.03, my + L * 0.42), boy * (0.27 if yan else 0.31), L * 1.12, aci, POST)   # damla govde uyluklari ortsun (fok)
    elips((mx, my - L * 0.38), boy * (0.19 if yan else 0.22) - KON / S2, L * 0.5 - KON / S2, aci, POST, kontur=False)
    if not yan:
        elips((mx, my + L * 0.45), boy * 0.19, L * 0.9, aci, KARIN)
    else:
        elips((mx + yon * boy * 0.15, my + L * 0.42), boy * 0.09, L * 0.86, aci, KARIN)
    kol(taraf[1], POST)
    # orgu atki: boyunda kalin bant (yesil benekli) + one sarkan uc, sacakli; yaninda altin duduk
    elips((nx_, ny_ + boy * 0.01), boy * (0.12 if yan else 0.15), boy * 0.045, aci, ATKI)
    for k in range(-3, 4):
        elips((nx_ + k * boy * 0.035 * (0.7 if yan else 1), ny_ + boy * 0.01), boy * 0.009, boy * 0.009, 0, ATKI_D, kontur=False)
    ox = nx_ + (yon * boy * 0.06 if yan else boy * 0.06)
    kapsul((ox, ny_ + boy * 0.03), (ox + boy * 0.015, ny_ + boy * 0.2), boy * 0.035, boy * 0.032, ATKI)
    for j in (0.08, 0.14):
        kapsul((ox - boy * 0.025, ny_ + boy * j), (ox + boy * 0.045, ny_ + boy * j), boy * 0.008, boy * 0.008, ATKI_D, kontur=False)
    for k in (-1, 0, 1):                                              # sacak
        kapsul((ox + boy * 0.015 + k * boy * 0.02, ny_ + boy * 0.23), (ox + boy * 0.015 + k * boy * 0.024, ny_ + boy * 0.26), boy * 0.006, boy * 0.006, ATKI_K, kontur=False)
    dx = -1 if not yan else -yon
    elips((nx_ + dx * boy * 0.1, ny_ + boy * 0.08), boy * 0.028, boy * 0.022, 0, DUDUK)


def kare(klasor, ad, j, duygu, yan=False):
    Yr = json.load(open(os.path.join(klasor, "yerlesim.json"), encoding="utf-8"))["karakter"]["maskot"]
    W = Image.open(os.path.join(klasor, "karakter", "maskot", "%s-%02d.png" % (ad, j))).width
    UST = 60                                                          # bere + ponpon icin ust pay
    ALT = 50
    big = Image.new("RGBA", (W * S2, (W + UST + ALT) * S2), (0, 0, 0, 0)); dr = ImageDraw.Draw(big)
    E = {k: [v[0], v[1] + UST] for k, v in Yr["poz"][ad]["eklem"][j].items()}
    govde_ciz(dr, E, Yr["boy_px"], yan)
    kx, ky, ks = Yr["poz"][ad]["kafa"][j]; ky += UST
    u = ks / 30 * OLCEK
    bas(dr, kx, ky - ks * 0.25 + DY * u, u, duygu, yan)
    big = big.resize((W, W + UST + ALT), Image.LANCZOS)
    bg = Image.new("RGBA", (W, W + UST + ALT), (58, 168, 255, 255)); bg.alpha_composite(big)    # buz mavisi zemin (sahne rengi)
    return bg.convert("RGB")


if __name__ == "__main__":
    P = ["raven-down-reach-curtsy", "cosmic-heel-raise-arms-forward-high", "rise-wave-reach-wide", "sakura-shrug-palms-up"]
    hucre = [("ÖN — mutlu", ON, P[1], 0, "mutlu", False), ("YAN — gövde", YAN, P[1], 0, "mutlu", True),
             ("PERFECT! — sevinç", ON, P[2], 6, "sevinc", False), ("OUT! — şaşkın", ON, P[0], 6, "sasirma", False),
             ("POZ: " + P[3], ON, P[3], 6, "mutlu", False), ("YAN POZ: " + P[2], YAN, P[2], 6, "mutlu", True)]
    ims = [kare(k, a, j, d, y) for _, k, a, j, d, y in hucre]
    w, hh = ims[0].size
    sayfa = Image.new("RGB", (3 * w, 2 * (hh + 40)), "white")
    dr = ImageDraw.Draw(sayfa)
    f = ImageFont.truetype("arial.ttf", 22)
    for i, (im, h) in enumerate(zip(ims, hucre)):
        x, y = (i % 3) * w, (i // 3) * (hh + 40)
        sayfa.paste(im, (x, y + 40)); dr.text((x + 10, y + 8), h[0], fill="black", font=f)
    cikti = r"C:\Users\eleme\OneDrive\Masaüstü\POZ-DUVARI\taslak\HUMAN-TETRIS-40-MASKOT-ORNEK.jpg"
    sayfa.save(cikti, quality=90)
    print("->", cikti, sayfa.size)
