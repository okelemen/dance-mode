"""HUMAN TETRIS 39 deniz kaplumbagasi yavrusu hakem maskot ornek sayfasi (TALIMATLAR §4: on/yan, 3-4 poz, 3 duygu)
-> POZ-DUVARI/taslak/HUMAN-TETRIS-39-MASKOT-ORNEK.jpg

38 dersi (kullanici 25 Kas: 3B govde reddedildi, "kafasi gibi bir cizim yapip ... hareketlendirsen"): TAMAMI 2B cizgi film, bastan.
Hareket: karakter.py --eklem 1 --govde-gizli 1 eklem verisi (gercek mocap/poz acilari, Masaustu md. 18); 38'in eklem kosusu
(varlik-38-maskot2b-on / -yan, ayni Mixamo iskeleti) ornek sayfasi icin yeniden kullanilir; video icin 39 pozlariyla yeni kosu alinir.
Tasarim (kendi tasarimimiz; bilinen kaplumbaga karakterlerine benzemez: maske/bandana/silah yok, insan gibi kas yok):
- tombul yavru govde, arkada yuvarlak yesil kabuk (on gorunuste kenari govdenin iki yanindan tasar), onde sari-krem karin plakasi (bolmeli)
- uzuvlar kisa tombul acik yesil; eller genis yuzgec (palet), ayaklar kucuk yuvarlak
- bas: buyuk yuvarlak acik yesil, iri parlak goz, pembe yanak, tepede uc kucuk koyu yesil benek
- hakem isareti: boynunda mercan-turuncu fular + altin duduk
Renk: ana yesil (mavi/pembe ana renk degil, §4).
"""
import json, math, os, sys
from PIL import Image, ImageDraw, ImageFont

BURA = os.path.dirname(os.path.abspath(__file__))
ON = os.path.join(BURA, sys.argv[1] if len(sys.argv) > 1 else "varlik-38-maskot2b-on/tetris-varlik")
YAN = os.path.join(BURA, sys.argv[2] if len(sys.argv) > 2 else "varlik-38-maskot2b-yan/tetris-varlik")
OLCEK = float(sys.argv[3]) if len(sys.argv) > 3 else 2.5
DY = float(sys.argv[4]) if len(sys.argv) > 4 else -8.0
S2 = 4
KN = "#0a2a14"                                                 # koyu yesil kontur
DERI, DERI_K = "#6ee07a", "#3ab850"                            # acik yesil deri / golge tarafi
KABUK, KABUK_K, KABUK_D = "#159a4a", "#0c6a32", "#2cc06a"      # kabuk / koyu desen / acik desen
KARIN, KARIN_C = "#ffd860", "#e8a830"                          # karin plakasi / bolme cizgisi
FULAR, FULAR_K, DUDUK = "#ff6a2a", "#d8461a", "#ffc21a"


def bas(dr, cx, cy, u, duygu, yan=False):
    S = lambda v: v * u * S2
    X = lambda v: (cx + v * u) * S2
    Y = lambda v: (cy + v * u) * S2
    def el(x, y, rx, ry, **k): dr.ellipse((X(x) - S(rx), Y(y) - S(ry), X(x) + S(rx), Y(y) + S(ry)), **k)
    w = int(S(1.6))
    if yan:
        el(2, 0, 21, 19, fill=DERI, outline=KN, width=w)
        el(14, 6, 9, 6.5, fill=DERI_K)                               # one uzanan agiz-burun
        for (bx, by) in ((-6, -15), (2, -17)):
            el(bx, by, 2.4, 1.8, fill=KABUK_K)
        el(8, -3, 6, 7, fill="#ffffff", outline=KN, width=int(S(1.2))); el(9.5, -2.4, 3.8, 4.6, fill=KN); el(8.2, -4.8, 1.3, 1.3, fill="#ffffff")
        el(10, 6, 3.0, 1.9, fill="#ff7a8a")
        dr.arc((X(13), Y(6), X(21), Y(12)), 10, 150, fill=KN, width=int(S(1.4)))
        return
    el(0, 0, 23, 21, fill=DERI, outline=KN, width=w)                 # yuvarlak acik yesil bas
    for (bx, by, r) in ((0, -15, 2.8), (-7, -13, 2.0), (7, -13, 2.0)):   # tepede uc benek
        el(bx, by, r, r * 0.75, fill=KABUK_K)
    for sx in (-1, 1):
        if duygu == "sevinc":
            dr.arc((X(sx * 9) - S(5.5), Y(-2) - S(5.5), X(sx * 9) + S(5.5), Y(-2) + S(5.5)), 200, 340, fill=KN, width=int(S(2.6)))
        elif duygu == "sasirma":
            el(sx * 9, -3, 6.5, 7.5, fill="#ffffff", outline=KN, width=int(S(1.4))); el(sx * 9, -3, 2.6, 2.8, fill=KN)
        else:
            el(sx * 9, -2, 6, 7, fill="#ffffff", outline=KN, width=int(S(1.4)))
            el(sx * 9 + 0.7, -1.4, 4.0, 4.8, fill=KN); el(sx * 9 - 0.8, -3.6, 1.5, 1.5, fill="#ffffff")
        el(sx * 15, 7, 3.6, 2.2, fill="#ff7a8a")
    el(-2, 6, 0.9, 0.7, fill=KN); el(2, 6, 0.9, 0.7, fill=KN)         # kucuk burun delikleri
    if duygu == "sasirma":
        el(0, 13, 3.2, 2.8, fill="#7a1020", outline=KN, width=int(S(1.0)))
    elif duygu == "sevinc":
        dr.chord((X(-7), Y(6), X(7), Y(17)), 0, 180, fill="#7a1020", outline=KN, width=int(S(1.2)))
    else:
        dr.arc((X(-6), Y(7), X(6), Y(15)), 20, 160, fill=KN, width=int(S(1.5)))


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
    ru, rl = boy * 0.1, boy * 0.088                                  # tombul bacak (ornek 1: ince, insan gibi okundu)
    ra, rf_ = boy * 0.078, boy * 0.07
    taraf = ("Left", "Right")
    if yan:
        taraf = tuple(sorted(taraf, key=lambda t: g(t + "UpLeg")[0]))
    def bacak(t, renk):
        uzuv([(g(t + "UpLeg"), g(t + "Leg"), ru, rl * 1.05, None), (g(t + "Leg"), g(t + "Foot"), rl * 1.05, rl, None)], renk)
        f, fu = g(t + "Foot"), g(t + "Foot_uc")                       # yuvarlak ayak
        elips(((f[0] + fu[0]) / 2, (f[1] + fu[1]) / 2), boy * 0.095, boy * 0.06, math.atan2(fu[1] - f[1], fu[0] - f[0]), renk)
    def kol(t, renk):
        uzuv([(g(t + "Arm"), g(t + "ForeArm"), ra, rf_ * 1.05, None), (g(t + "ForeArm"), g(t + "Hand"), rf_ * 1.05, rf_, None)], renk)
        h, hu = g(t + "Hand"), g(t + "Hand_uc")                       # genis yuzgec el (palet)
        aci = math.atan2(hu[1] - h[1], hu[0] - h[0])
        elips((h[0] + (hu[0] - h[0]) * 0.9, h[1] + (hu[1] - h[1]) * 0.9), boy * 0.12, boy * 0.065, aci, renk)
    hx, hy = g("Hips"); nx_, ny_ = g("Neck"); bx = g("Head")[0]
    aci = math.atan2(ny_ - hy, nx_ - hx) + math.pi / 2
    L = math.hypot(nx_ - hx, ny_ - hy)
    mx, my = hx * 0.72 + nx_ * 0.28, hy * 0.72 + ny_ * 0.28                # govde asagi: kabuk kalcayi ve uyluk basini ortsun
    yon = math.copysign(1, bx - hx) if yan else 0
    # kabuk: on gorunuste govdenin arkasinda, iki yandan tasan yuvarlak; yan gorunuste sirtta kubbe
    kab = (mx - yon * boy * 0.08, my - boy * 0.01)
    kgen = boy * (0.26 if yan else 0.31)
    elips(kab, kgen, L * 0.92, aci, KABUK)
    for i in range(6):                                                # kabuk kenari acik benekler (kabuk okunur)
        t = math.pi * 2 * i / 6 + 0.5
        px, py = kab[0] + math.cos(t) * kgen * 0.8, kab[1] + math.sin(t) * L * 0.74
        elips((px, py), boy * 0.03, boy * 0.024, t, KABUK_D, kontur=False)
    bacak(taraf[0], DERI_K); kol(taraf[0], DERI_K)
    if not yan:                                                       # karin plakasi: sari, iki dikey + uc yatay bolme
        elips((mx, my + L * 0.04), boy * 0.2, L * 0.74, aci, KARIN)
        for k in (-1, 1):
            kapsul((mx + k * boy * 0.065, my - L * 0.5), (mx + k * boy * 0.065, my + L * 0.58), boy * 0.006, boy * 0.006, KARIN_C, kontur=False)
        for j in (-0.3, 0.06, 0.42):
            kapsul((mx - boy * 0.16, my + L * j), (mx + boy * 0.16, my + L * j), boy * 0.006, boy * 0.006, KARIN_C, kontur=False)
    else:                                                             # yan: ince sari karin seridi onde
        elips((mx + yon * boy * 0.14, my + L * 0.04), boy * 0.08, L * 0.72, aci, KARIN)
        for j in range(5):                                            # kabuk desen petekleri
            elips((kab[0] - yon * boy * 0.03, kab[1] - L * 0.6 + j * L * 0.3), boy * 0.09, boy * 0.065, 0, KABUK_K, kontur=False)
    bacak(taraf[1], DERI); kol(taraf[1], DERI)
    # hakem fulari: boyunda bant + one sarkan ucgen; yaninda altin duduk (ornek 1: cubuk gibi okundu)
    elips((nx_, ny_ + boy * 0.005), boy * (0.1 if yan else 0.13), boy * 0.036, aci, FULAR)
    ox = nx_ + (yon * boy * 0.05 if yan else 0)
    u3 = [(ox - boy * 0.08, ny_ + boy * 0.02), (ox + boy * 0.08, ny_ + boy * 0.02), (ox, ny_ + boy * 0.13)]
    k3 = [(x * S2, y * S2) for x, y in u3]
    dr.polygon(k3, fill=KN); m3 = (sum(p[0] for p in k3) / 3, sum(p[1] for p in k3) / 3)
    dr.polygon([(m3[0] + (p[0] - m3[0]) * 0.78, m3[1] + (p[1] - m3[1]) * 0.78) for p in k3], fill=FULAR)
    dx = -1 if not yan else -yon
    elips((ox + dx * boy * 0.1, ny_ + boy * 0.07), boy * 0.028, boy * 0.022, 0, DUDUK)


def kare(klasor, ad, j, duygu, yan=False):
    Yr = json.load(open(os.path.join(klasor, "yerlesim.json"), encoding="utf-8"))["karakter"]["maskot"]
    W = Image.open(os.path.join(klasor, "karakter", "maskot", "%s-%02d.png" % (ad, j))).width
    UST = 40
    big = Image.new("RGBA", (W * S2, (W + UST) * S2), (0, 0, 0, 0)); dr = ImageDraw.Draw(big)
    E = {k: [v[0], v[1] + UST] for k, v in Yr["poz"][ad]["eklem"][j].items()}
    govde_ciz(dr, E, Yr["boy_px"], yan)
    kx, ky, ks = Yr["poz"][ad]["kafa"][j]; ky += UST
    u = ks / 30 * OLCEK
    bas(dr, kx, ky - ks * 0.25 + DY * u, u, duygu, yan)
    big = big.resize((W, W + UST), Image.LANCZOS)
    bg = Image.new("RGBA", (W, W + UST), (20, 170, 200, 255)); bg.alpha_composite(big)    # turkuaz su zemini (sahne rengi)
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
    cikti = r"C:\Users\eleme\OneDrive\Masaüstü\POZ-DUVARI\taslak\HUMAN-TETRIS-39-MASKOT-ORNEK.jpg"
    sayfa.save(cikti, quality=90)
    print("->", cikti, sayfa.size)
