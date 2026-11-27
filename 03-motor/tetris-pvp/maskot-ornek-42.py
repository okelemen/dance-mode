"""HUMAN TETRIS 42 papagan yavrusu hakem maskot ornek sayfasi (TALIMATLAR §4: on/yan, 3-4 poz, 3 duygu)
-> POZ-DUVARI/taslak/HUMAN-TETRIS-42-MASKOT-ORNEK.jpg  (maskot-ornek-41.py kopyasi; cizici/kare/sayfa ayni, bas + govde papagan)

38-41 yontemi: TAMAMI 2B cizgi film; hareket karakter.py --eklem 1 eklem verisi (gercek mocap/poz acilari, Masaustu md. 18);
38'in eklem kosusu ornek sayfasi icin yeniden kullanilir; video icin 42 pozlariyla yeni kosu alinir.
Tasarim (kendi tasarimimiz; bilinen papagan karakterlerine benzemez):
- papaganin imzasi: kalin kivrik kanca gaga (ust sari-turuncu, alt koyu), basta uc tuylu turuncu-kirmizi tepelik, goz cevresinde beyaz halka
- canli yesil tuy + sari gogus + kanat uclarinda sari tuy; uzun sivri kuyruk tuyleri (yesil, ucu sari). Mavi/pembe ana renk YOK (oyuncu renkleri)
- tombul damla govde, kisa tombul bacak + turuncu pence, kol ucunda yelpaze kanat
- hakem isareti: kendi tasarimimiz uc koseli korsan sapkasi (kahve, altin serit, kurukafa YOK, altin rozet) + altin duduk
"""
import json, math, os, sys
from PIL import Image, ImageDraw, ImageFont

BURA = os.path.dirname(os.path.abspath(__file__))
ON = os.path.join(BURA, sys.argv[1] if len(sys.argv) > 1 else "varlik-38-maskot2b-on/tetris-varlik")
YAN = os.path.join(BURA, sys.argv[2] if len(sys.argv) > 2 else "varlik-38-maskot2b-yan/tetris-varlik")
OLCEK = float(sys.argv[3]) if len(sys.argv) > 3 else 2.5
DY = float(sys.argv[4]) if len(sys.argv) > 4 else -8.0
S2 = 4
KN = "#1e2a10"                                                 # koyu yesil-kahve kontur
POST, POST_K = "#3fd14a", "#22a83a"                            # canli yesil tuy / koyu yesil golge
KARIN = "#ffe04a"                                              # sari gogus
TEPE, TEPE_K = "#ff6a1a", "#e8361a"                            # turuncu-kirmizi tepelik
GAGA_U, GAGA_A = "#ffb21a", "#4a2a10"                          # ust gaga sari-turuncu / alt gaga koyu
KANAT_U = "#ffcc1a"                                            # kanat/kuyruk ucu sari
SAPKA, SAPKA_S = "#6a3a1a", "#ffd23a"                          # korsan sapkasi kahve / altin serit
DUDUK = "#ffc21a"


def bas(dr, cx, cy, u, duygu, yan=False):
    S = lambda v: v * u * S2
    X = lambda v: (cx + v * u) * S2
    Y = lambda v: (cy + v * u) * S2
    def el(x, y, rx, ry, **k): dr.ellipse((X(x) - S(rx), Y(y) - S(ry), X(x) + S(rx), Y(y) + S(ry)), **k)
    w = int(S(1.6))
    yx = 1 if yan else 0
    for i, (dx, uy, uyx) in enumerate(((-9, -44, -17), (0, -50, -2), (9, -43, 13))):   # tepelik: uc sivri tuy
        bx = dx - yx * 6
        dr.polygon([(X(bx - 5), Y(-16)), (X(uyx - yx * 10), Y(uy)), (X(bx + 5), Y(-16))], fill=TEPE if i != 1 else TEPE_K, outline=KN, width=int(S(1.2)))
    el(0, 0, 22, 20, fill=POST, outline=KN, width=w)                    # yuvarlak bas
    # korsan sapkasi (uc koseli, kurukafasiz): iki kamburlu tepe, kenarlar yukari kivrik, basin ustune oturur
    dr.polygon([(X(-28), Y(-9)), (X(-23), Y(-25)), (X(-11), Y(-33)), (X(0), Y(-28)), (X(11), Y(-33)), (X(23), Y(-25)), (X(28), Y(-9)),
                (X(14), Y(-15)), (X(0), Y(-12)), (X(-14), Y(-15))], fill=SAPKA, outline=KN, width=int(S(1.4)))
    dr.line((X(-26), Y(-11), X(-14), Y(-17), X(0), Y(-14.5), X(14), Y(-17), X(26), Y(-11)), fill=SAPKA_S, width=int(S(2.0)))
    el(0, -22, 3.6, 3.6, fill=SAPKA_S, outline=KN, width=int(S(0.9)))          # altin rozet
    if yan:
        el(4, -2, 6.5, 6.5, fill="#ffffff", outline=KN, width=int(S(1.0)))
        el(5, -2.2, 4.0, 4.6, fill="#101018"); el(3.6, -4.2, 1.4, 1.4, fill="#ffffff")
        dr.chord((X(10), Y(-6), X(34), Y(18)), 270, 90, fill=GAGA_U, outline=KN, width=int(S(1.2)))   # kanca gaga
        dr.polygon([(X(21), Y(15)), (X(29), Y(11)), (X(25), Y(21))], fill=GAGA_U, outline=KN)
        dr.chord((X(12), Y(4), X(24), Y(16)), 0, 180, fill=GAGA_A, outline=KN, width=int(S(1.0)))
        el(2, 9, 3.0, 1.9, fill="#ff8a6a")
        return
    for sx in (-1, 1):
        el(sx * 9, -4, 8.2, 8.6, fill="#ffffff", outline=KN, width=int(S(1.0)))   # beyaz goz halkasi
        if duygu == "sevinc":
            dr.arc((X(sx * 9) - S(5.2), Y(-4) - S(5.2), X(sx * 9) + S(5.2), Y(-4) + S(5.2)), 200, 340, fill=KN, width=int(S(2.6)))
        elif duygu == "sasirma":
            el(sx * 9, -4, 2.4, 2.6, fill="#101018")
        else:
            el(sx * 9 + 0.6, -3.6, 4.6, 5.4, fill="#101018"); el(sx * 9 - 0.9, -6.0, 1.7, 1.7, fill="#ffffff")
        el(sx * 16, 6, 3.4, 2.1, fill="#ff7a6a")
    if duygu in ("sasirma", "sevinc"):
        dr.chord((X(-6), Y(9), X(6), Y(23)), 0, 180, fill=GAGA_A, outline=KN, width=int(S(1.1)))   # acik agiz (alt gaga)
    dr.polygon([(X(-8), Y(4)), (X(0), Y(1)), (X(8), Y(4)), (X(6), Y(12)), (X(0), Y(19)), (X(-6), Y(12))], fill=GAGA_U, outline=KN, width=int(S(1.3)))
    dr.line((X(0), Y(5), X(0), Y(15)), fill="#d88a10", width=int(S(0.9)))


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
                elips((m[0] + math.cos(aci + k * 0.35) * rx * 0.55, m[1] + math.sin(aci + k * 0.35) * rx * 0.55), rx * 0.32, ry * 0.32, aci + k * 0.35, KANAT_U)
    def bacak(t, renk):
        uzuv([(g(t + "UpLeg"), g(t + "Leg"), ru, rl * 1.05, None), (g(t + "Leg"), g(t + "Foot"), rl * 0.6, rl * 0.5, GAGA_U)], renk)
        f, fu = g(t + "Foot"), g(t + "Foot_uc")                       # turuncu pence
        yelpaze(((f[0] + fu[0]) / 2, (f[1] + fu[1]) / 2), math.atan2(fu[1] - f[1], fu[0] - f[0]), boy * 0.11, boy * 0.06, GAGA_U)
    def kol(t, renk):
        uzuv([(g(t + "Arm"), g(t + "ForeArm"), ra, rf_ * 1.05, None), (g(t + "ForeArm"), g(t + "Hand"), rf_ * 1.05, rf_, None)], renk)
        a_, h_ = g(t + "Arm"), g(t + "Hand")                         # kanat: kol boyunca disa sarkan uzun tuyler (koyu yesil, ucu sari)
        dx_, dy_ = h_[0] - a_[0], h_[1] - a_[1]; L_ = math.hypot(dx_, dy_) or 1
        nx_k, ny_k = -dy_ / L_, dx_ / L_
        hx0 = g("Hips")[0]; mx0 = (a_[0] + h_[0]) / 2 - hx0
        if nx_k * mx0 + ny_k * 0.3 * abs(mx0 or 1) < 0: nx_k, ny_k = -nx_k, -ny_k   # tuyler govdeden DISA sarkar (ornek 2: ice dusup halka gibi okundu)
        fa = math.atan2(ny_k, nx_k)
        for q in (0.3, 0.5, 0.7, 0.9):
            px, py = a_[0] + dx_ * q, a_[1] + dy_ * q
            fm = (px + nx_k * boy * 0.1, py + ny_k * boy * 0.1)
            elips(fm, boy * 0.11, boy * 0.04, fa, POST_K)
            elips((fm[0] + nx_k * boy * 0.085, fm[1] + ny_k * boy * 0.085), boy * 0.04, boy * 0.03, fa, KANAT_U, kontur=False)
        uzuv([(g(t + "Arm"), g(t + "ForeArm"), ra, rf_ * 1.05, None), (g(t + "ForeArm"), g(t + "Hand"), rf_ * 1.05, rf_, None)], renk)
        h, hu = g(t + "Hand"), g(t + "Hand_uc")                       # kanat ucu: yesil yelpaze + sari tuy uclari
        aci = math.atan2(hu[1] - h[1], hu[0] - h[0])
        yelpaze((h[0] + (hu[0] - h[0]) * 0.9, h[1] + (hu[1] - h[1]) * 0.9), aci, boy * 0.13, boy * 0.07, renk, uc=True)
    hx, hy = g("Hips"); nx_, ny_ = g("Neck"); bx = g("Head")[0]
    aci = math.atan2(ny_ - hy, nx_ - hx) + math.pi / 2
    L = math.hypot(nx_ - hx, ny_ - hy)
    mx, my = hx * 0.72 + nx_ * 0.28, hy * 0.72 + ny_ * 0.28
    yon = math.copysign(1, bx - hx) if yan else 0
    # uzun sivri kuyruk tuyleri: kalcadan asagi uc tuy (yesil, ucu sari), govdenin arkasinda
    for k, uz in ((-0.35, 0.34), (0.0, 0.42), (0.35, 0.34)):
        ka = math.pi / 2 + k * 0.5 + (yon * 0.6 if yan else 0)
        km = (hx + math.cos(ka) * boy * uz * 0.55, hy + math.sin(ka) * boy * uz * 0.55)
        elips(km, boy * uz * 0.5, boy * 0.045, ka, POST_K)
        elips((km[0] + math.cos(ka) * boy * uz * 0.38, km[1] + math.sin(ka) * boy * uz * 0.38), boy * 0.07, boy * 0.03, ka, KANAT_U, kontur=False)
    bacak(taraf[0], POST_K); bacak(taraf[1], POST_K); kol(taraf[0], POST_K)
    # tombul damla govde: kalcada genis, boyuna dogru daralan (iki elips; ust elips konturu alttakinin icinde kalir)
    elips((mx, my - L * 0.38), boy * (0.19 if yan else 0.22), L * 0.5, aci, POST)
    elips((mx - yon * boy * 0.03, my + L * 0.3), boy * (0.24 if yan else 0.27), L * 0.95, aci, POST)   # tombul damla govde (foktan ince: bacaklar gorunur)
    elips((mx, my - L * 0.38), boy * (0.19 if yan else 0.22) - KON / S2, L * 0.5 - KON / S2, aci, POST, kontur=False)
    if not yan:
        elips((mx, my + L * 0.35), boy * 0.16, L * 0.75, aci, KARIN)
    else:
        elips((mx + yon * boy * 0.13, my + L * 0.32), boy * 0.08, L * 0.72, aci, KARIN)
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
    bg = Image.new("RGBA", (W, W + UST + ALT), (222, 160, 96, 255)); bg.alpha_composite(big)    # ahsap guverte zemin (sahne rengi)
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
    cikti = r"C:\Users\eleme\OneDrive\Masaüstü\POZ-DUVARI\taslak\HUMAN-TETRIS-42-MASKOT-ORNEK.jpg"
    sayfa.save(cikti, quality=90)
    print("->", cikti, sayfa.size)
