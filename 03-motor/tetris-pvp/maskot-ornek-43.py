"""HUMAN TETRIS 43 T-rex yavrusu hakem maskot ornek sayfasi (TALIMATLAR §4: on/yan, 3-4 poz, 3 duygu)
-> POZ-DUVARI/taslak/HUMAN-TETRIS-43-MASKOT-ORNEK.jpg  (maskot-ornek-42.py kopyasi; cizici/kare/sayfa ayni, bas + govde T-rex)

38-42 yontemi: TAMAMI 2B cizgi film; hareket karakter.py --eklem 1 eklem verisi (gercek mocap/poz acilari, Masaustu md. 18);
38'in eklem kosusu ornek sayfasi icin yeniden kullanilir; video icin 43 pozlariyla yeni kosu alinir.
Tasarim (kendi tasarimimiz; bilinen dinozor karakterlerine / film dinozorlarina benzemez):
- yumurtadan yeni cikmis: basinda beyaz zikzak kenarli YUMURTA KABUGU sapka (sari benekli)
- iri yuvarlak bas, genis burun + iki burun deligi, iri goz, kizarik yanak; acik agizda minik beyaz disler
- canli turuncu govde + sari karin plakalari (yatay seritler), sirtta yesil sivri pullar (yan gorunum)
- kalcadan cikan kalin, sivrilen kuyruk; kalin bacak + uc beyaz tirnakli ayak; ince kol + uc tirnak
  (kollar pozu gostersin diye iskelet boyunda; "minik kol" etkisi ince kalinlikla verilir)
- yesil cimde okunur: turuncu ana renk; mavi/pembe ana renk YOK (oyuncu PURPLE ile de karismaz)
- hakem isareti: altin duduk
"""
import json, math, os, sys
from PIL import Image, ImageDraw, ImageFont

BURA = os.path.dirname(os.path.abspath(__file__))
ON = os.path.join(BURA, sys.argv[1] if len(sys.argv) > 1 else "varlik-38-maskot2b-on/tetris-varlik")
YAN = os.path.join(BURA, sys.argv[2] if len(sys.argv) > 2 else "varlik-38-maskot2b-yan/tetris-varlik")
OLCEK = float(sys.argv[3]) if len(sys.argv) > 3 else 2.5
DY = float(sys.argv[4]) if len(sys.argv) > 4 else -8.0
S2 = 4
KN = "#2a1608"                                                 # koyu kahve kontur
POST, POST_K = "#ff8a2a", "#e8601a"                            # canli turuncu deri / koyu turuncu golge
KARIN, KARIN_S = "#ffe04a", "#f0b81a"                          # sari karin / karin plakasi cizgisi
PUL = "#2ab83a"                                                # sirt pullari yesil
KABUK, KABUK_B = "#fffaf0", "#ffd84a"                          # yumurta kabugu beyaz / sari benek
TIRNAK = "#fff6e0"
DUDUK = "#ffc21a"


def bas(dr, cx, cy, u, duygu, yan=False):
    S = lambda v: v * u * S2
    X = lambda v: (cx + v * u) * S2
    Y = lambda v: (cy + v * u) * S2
    def el(x, y, rx, ry, **k): dr.ellipse((X(x) - S(rx), Y(y) - S(ry), X(x) + S(rx), Y(y) + S(ry)), **k)
    w = int(S(1.6))
    if yan:
        el(-2, 0, 21, 19, fill=POST, outline=KN, width=w)                # kafa arkasi
        dr.rounded_rectangle((X(-2), Y(-6), X(30), Y(14)), radius=S(9), fill=POST, outline=KN, width=w)   # uzun burun
        el(-2, 0, 19.5, 17.5, fill=POST)                                  # birlesme yerini ort
        el(25, -2, 1.6, 1.2, fill=KN)                                     # burun deligi
        el(4, -5, 6.5, 6.8, fill="#ffffff", outline=KN, width=int(S(1.0)))
        el(5.5, -4.8, 4.0, 4.8, fill="#101018"); el(4.2, -6.8, 1.4, 1.4, fill="#ffffff")
        dr.line((X(6), Y(9), X(28), Y(8)), fill=KN, width=int(S(1.2)))   # agiz cizgisi
        for tx in (12, 17, 22):
            dr.polygon([(X(tx - 1.4), Y(8.6)), (X(tx), Y(11)), (X(tx + 1.4), Y(8.5))], fill="#ffffff", outline=KN)
        el(2, 7, 3.0, 1.9, fill="#ff6a4a")
        ox = -3
    else:
        el(0, 0, 24, 21, fill=POST, outline=KN, width=w)                 # iri yuvarlak bas
        dr.rounded_rectangle((X(-15), Y(2), X(15), Y(19)), radius=S(8), fill=POST, outline=KN, width=w)   # genis burun
        el(0, 2, 22.5, 18.5, fill=POST)
        for sx in (-1, 1):
            el(sx * 5, 8, 1.6, 1.2, fill=KN)                              # burun delikleri
            el(sx * 9.5, -6, 7.6, 8.0, fill="#ffffff", outline=KN, width=int(S(1.0)))
            if duygu == "sevinc":
                dr.arc((X(sx * 9.5) - S(5), Y(-6) - S(5), X(sx * 9.5) + S(5), Y(-6) + S(5)), 200, 340, fill=KN, width=int(S(2.6)))
            elif duygu == "sasirma":
                el(sx * 9.5, -6, 2.4, 2.6, fill="#101018")
            else:
                el(sx * 9.5 + 0.6, -5.6, 4.4, 5.2, fill="#101018"); el(sx * 9.5 - 0.9, -8.0, 1.6, 1.6, fill="#ffffff")
            el(sx * 18, 6, 3.4, 2.1, fill="#ff5a3a")
        if duygu in ("sasirma", "sevinc"):
            dr.chord((X(-9), Y(9), X(9), Y(24)), 0, 180, fill="#a8201a", outline=KN, width=int(S(1.1)))   # acik agiz
            for tx in (-6, -2, 2, 6):
                dr.polygon([(X(tx - 1.4), Y(16.2)), (X(tx), Y(19)), (X(tx + 1.4), Y(16.2))], fill="#ffffff", outline=KN)
        else:
            dr.arc((X(-9), Y(6), X(9), Y(18)), 20, 160, fill=KN, width=int(S(1.4)))   # gulumseme
        ox = 0
    # yumurta kabugu sapka: ustte kubbe, altta zikzak kirik kenar, sari benekler
    nok = [(X(ox - 22), Y(-16))]
    for i in range(9):
        nok.append((X(ox - 22 + (i + 0.5) * 44 / 9), Y(-16 + (3 if i % 2 == 0 else -1))))
    nok.append((X(ox + 22), Y(-16)))
    ust = [(X(ox + 22 * math.cos(t)), Y(-16 - 18 * math.sin(t))) for t in [k * math.pi / 16 for k in range(17)]]
    dr.polygon(nok + ust, fill=KABUK, outline=KN, width=int(S(1.4)))
    for (bx, by, br) in ((-10, -24, 3.2), (6, -29, 2.6), (13, -20, 2.2), (-2, -20, 1.8)):
        el(ox + bx, by, br, br * 0.85, fill=KABUK_B)


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
    def yelpaze(m, aci, rx, ry, renk, uc=False):                      # kanat ucu tuy yelpazesi / pence
        elips(m, rx * 0.6, ry * 0.85, aci, renk)
        if uc:
            for k in (-1, 0, 1):
                elips((m[0] + math.cos(aci + k * 0.35) * rx * 0.55, m[1] + math.sin(aci + k * 0.35) * rx * 0.55), rx * 0.32, ry * 0.32, aci + k * 0.35, KARIN)
    def bacak(t, renk):
        uzuv([(g(t + "UpLeg"), g(t + "Leg"), ru, rl * 1.05, None), (g(t + "Leg"), g(t + "Foot"), rl * 0.75, rl * 0.65, None)], renk)
        f, fu = g(t + "Foot"), g(t + "Foot_uc")                       # turuncu pence
        fa = math.atan2(fu[1] - f[1], fu[0] - f[0])
        elips(((f[0] + fu[0]) / 2, (f[1] + fu[1]) / 2), boy * 0.1, boy * 0.06, fa, renk)
        for k in (-1, 0, 1):
            elips((fu[0] + math.cos(fa + k * 0.4) * boy * 0.03, fu[1] + math.sin(fa + k * 0.4) * boy * 0.03), boy * 0.028, boy * 0.016, fa + k * 0.4, TIRNAK)
    def kol(t, renk):
        uzuv([(g(t + "Arm"), g(t + "ForeArm"), ra * 0.75, rf_ * 0.7, None), (g(t + "ForeArm"), g(t + "Hand"), rf_ * 0.7, rf_ * 0.6, None)], renk)
        h, hu = g(t + "Hand"), g(t + "Hand_uc")                       # uc beyaz tirnak
        aci = math.atan2(hu[1] - h[1], hu[0] - h[0])
        for k in (-1, 0, 1):
            m = (h[0] + math.cos(aci + k * 0.45) * boy * 0.05, h[1] + math.sin(aci + k * 0.45) * boy * 0.05)
            elips(m, boy * 0.03, boy * 0.016, aci + k * 0.45, TIRNAK)
    hx, hy = g("Hips"); nx_, ny_ = g("Neck"); bx = g("Head")[0]
    aci = math.atan2(ny_ - hy, nx_ - hx) + math.pi / 2
    L = math.hypot(nx_ - hx, ny_ - hy)
    mx, my = hx * 0.72 + nx_ * 0.28, hy * 0.72 + ny_ * 0.28
    yon = 1 if yan else 0                     # 43: yan kafa hep saga bakar (burun saga) -> karin onde/sagda, pul + kuyruk arkada/solda
    # kalin, sivrilen T-rex kuyrugu: kalcadan asagi-yana (yan gorunumde arkaya), govdenin arkasinda
    ka = math.pi / 2 + (yon * 1.1 if yan else 0.55)
    for q, rr in ((0.18, 0.15), (0.36, 0.11), (0.52, 0.075), (0.64, 0.045)):
        elips((hx + math.cos(ka) * boy * q, hy + math.sin(ka) * boy * q), boy * rr * 1.25, boy * rr, ka, POST_K)
    bacak(taraf[0], POST_K); bacak(taraf[1], POST_K); kol(taraf[0], POST_K)
    # tombul damla govde: kalcada genis, boyuna dogru daralan (iki elips; ust elips konturu alttakinin icinde kalir)
    elips((mx, my - L * 0.38), boy * (0.19 if yan else 0.22), L * 0.5, aci, POST)
    elips((mx - yon * boy * 0.03, my + L * 0.3), boy * (0.24 if yan else 0.27), L * 0.95, aci, POST)   # tombul damla govde (foktan ince: bacaklar gorunur)
    elips((mx, my - L * 0.38), boy * (0.19 if yan else 0.22) - KON / S2, L * 0.5 - KON / S2, aci, POST, kontur=False)
    if not yan:
        elips((mx, my + L * 0.35), boy * 0.16, L * 0.75, aci, KARIN)
        dx_, dy_ = math.cos(aci), math.sin(aci)                          # govde enine yon
        ux_, uy_ = -dy_, dx_                                             # govde boyuna yon
        for q in (0.0, 0.3, 0.6, 0.9):                                   # yatay karin plakasi cizgileri
            cxq, cyq = mx + ux_ * L * q * -1 + 0 * dx_, my + uy_ * L * q * -1
            cxq, cyq = mx - ux_ * L * (q - 0.35) * -1, my - uy_ * L * (q - 0.35) * -1
            kapsul((cxq - dx_ * boy * 0.11, cyq - dy_ * boy * 0.11), (cxq + dx_ * boy * 0.11, cyq + dy_ * boy * 0.11), boy * 0.006, boy * 0.006, KARIN_S, kontur=False)
    else:
        elips((mx + yon * boy * 0.13, my + L * 0.32), boy * 0.08, L * 0.72, aci, KARIN)
        for q in (-0.5, -0.15, 0.2, 0.55):                               # sirtta yesil sivri pullar
            px, py = mx - yon * boy * 0.25, my + L * q
            dr.polygon([((px) * S2, (py - boy * 0.05) * S2), ((px - yon * boy * 0.09) * S2, py * S2), ((px) * S2, (py + boy * 0.05) * S2)], fill=PUL, outline=KN)
    kol(taraf[1], POST)
    dx = -1 if not yan else -yon
    elips((nx_ + dx * boy * 0.1, ny_ + boy * 0.08), boy * 0.028, boy * 0.022, 0, DUDUK)


def kare(klasor, ad, j, duygu, yan=False):
    Yr = json.load(open(os.path.join(klasor, "yerlesim.json"), encoding="utf-8"))["karakter"]["maskot"]
    W = Image.open(os.path.join(klasor, "karakter", "maskot", "%s-%02d.png" % (ad, j))).width
    UST = 110                                                         # dev kulaklar icin ust pay
    ALT = 50
    big = Image.new("RGBA", (W * S2, (W + UST + ALT) * S2), (0, 0, 0, 0)); dr = ImageDraw.Draw(big)
    E = {k: [v[0], v[1] + UST] for k, v in Yr["poz"][ad]["eklem"][j].items()}
    govde_ciz(dr, E, Yr["boy_px"], yan)
    kx, ky, ks = Yr["poz"][ad]["kafa"][j]; ky += UST
    u = ks / 30 * OLCEK
    bas(dr, kx, ky - ks * 0.25 + DY * u, u, duygu, yan)
    big = big.resize((W, W + UST + ALT), Image.LANCZOS)
    bg = Image.new("RGBA", (W, W + UST + ALT), (58, 200, 42, 255)); bg.alpha_composite(big)    # canli yesil cim zemin (sahne rengi)
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
    cikti = r"C:\Users\eleme\OneDrive\Masaüstü\POZ-DUVARI\taslak\HUMAN-TETRIS-43-MASKOT-ORNEK.jpg"
    sayfa.save(cikti, quality=90)
    print("->", cikti, sayfa.size)
