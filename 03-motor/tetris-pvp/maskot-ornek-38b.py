"""HUMAN TETRIS 38 ren geyigi - TAMAMI 2B (kullanici 25 Kas: "kafasi geyik ama alti ... tahtadan bir sey duruyor ... kafasi gibi bir cizim
yapip geyik hareketlendirsen"). 3B govde (karakter.py --rengeyik) reddedildi; govde de kafayla ayni cizgi-film dilinde 2B cizilir.

Hareket: Blender/Actions karakter.py --eklem 1 --govde-gizli 1 -> her karede eklemlerin ekran yeri (gercek mocap/poz aciları, Masaustu md. 18).
Cizim (motor birebir aynisini JS'de cizer): kalin koyu kontur + duz dolgu; arka bacak -> arka kol -> govde (damla) + krem karin ->
on bacak -> on kol -> atki + altin can -> bas (maskot-ornek-38.bas). Uzuvlar tombul kapsul, uclarda koyu toynak; kuyruk krem ponpon.
"""
import json, math, os, sys
from PIL import Image, ImageDraw, ImageFont

BURA = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BURA)
import importlib.util
_sp = importlib.util.spec_from_file_location("mo38", os.path.join(BURA, "maskot-ornek-38.py")); MO = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(MO)

ON = os.path.join(BURA, sys.argv[1] if len(sys.argv) > 1 else "varlik-38-maskot2b-on/tetris-varlik")
YAN = os.path.join(BURA, sys.argv[2] if len(sys.argv) > 2 else "varlik-38-maskot2b-yan/tetris-varlik")
OLCEK = float(sys.argv[3]) if len(sys.argv) > 3 else 2.6
DY = float(sys.argv[4]) if len(sys.argv) > 4 else -9.0
S2 = 4
KN = MO.KN
KURK, KURK_K, KARIN, TOYNAK, KUYRUK = "#b8621e", "#9a4e14", "#ffc880", "#3a1a0a", "#ffe0a8"
ATKI, ATKI_K, CAN = "#e8102c", "#b00820", "#ffc21a"


def cizici(dr, boy):
    """boy = govde boyu (px); kontur ve kalinliklar buna oranli"""
    KON = max(2, boy * 0.018) * S2
    P = lambda p: (p[0] * S2, p[1] * S2)

    def uzuv(segs, renk):
        """tek parca uzuv: [(a, b, ra, rb, renk_ozel)] -> once hepsinin konturu, sonra dolgular (eklemde kontur cizgisi yok)"""
        for a_, b_, r1, r2, _ in segs:
            kapsul(a_, b_, r1 + KON / S2, r2 + KON / S2, KN, kontur=False)
        for a_, b_, r1, r2, c in segs:
            kapsul(a_, b_, r1, r2, c or renk, kontur=False)

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

    def elips(m, rx, ry, aci, renk, kontur=True, n=48):
        cx, cy = P(m)
        for gec, (ex, c) in enumerate(((KON, KN), (0, renk))):
            if gec == 0 and not kontur:
                continue
            pts = []
            for i in range(n):
                t = 2 * math.pi * i / n
                x, y = (rx * S2 + ex) * math.cos(t), (ry * S2 + ex) * math.sin(t)
                pts.append((cx + x * math.cos(aci) - y * math.sin(aci), cy + x * math.sin(aci) + y * math.cos(aci)))
            dr.polygon(pts, fill=c)
    return kapsul, elips, uzuv


def govde_ciz(dr, E, boy, yan=False):
    kapsul, elips, uzuv = cizici(dr, boy)
    g = lambda k: E[k]
    ru, rl, rt = boy * 0.062, boy * 0.042, boy * 0.048         # ince geyik bacagi: uyluk tombul, baldir ince, kucuk toynak
    ra, rf_ = boy * 0.05, boy * 0.04
    taraf = ("Left", "Right")
    if yan:
        taraf = tuple(sorted(taraf, key=lambda t: g(t + "UpLeg")[0]))
    def bacak(t, renk):
        uzuv([(g(t + "UpLeg"), g(t + "Leg"), ru, rl * 1.1, None), (g(t + "Leg"), g(t + "Foot"), rl * 1.1, rl, None),
              (g(t + "Foot"), g(t + "Foot_uc"), rt, rt * 0.8, TOYNAK)], renk)
    def kol(t, renk):
        uzuv([(g(t + "Arm"), g(t + "ForeArm"), ra, rf_ * 1.05, None), (g(t + "ForeArm"), g(t + "Hand"), rf_ * 1.05, rf_, None),
              (g(t + "Hand"), g(t + "Hand_uc"), rf_ * 1.0, rf_ * 0.8, TOYNAK)], renk)
    bacak(taraf[0], KURK_K); kol(taraf[0], KURK_K)
    hx, hy = g("Hips"); bx = g("Head")[0]
    if yan:
        elips((hx - math.copysign(boy * 0.14, bx - hx), hy - boy * 0.03), boy * 0.06, boy * 0.05, 0, KUYRUK)
    nx_, ny_ = g("Neck")
    aci = math.atan2(ny_ - hy, nx_ - hx) + math.pi / 2
    L = math.hypot(nx_ - hx, ny_ - hy)
    mx, my = hx * 0.6 + nx_ * 0.4, hy * 0.6 + ny_ * 0.4                  # armut govde: agirlik altta
    genis = boy * (0.14 if yan else 0.17)
    elips((mx, my), genis, L * 0.62, aci, KURK)
    kay = math.copysign(boy * 0.045, bx - hx) if yan else 0
    elips((mx + kay, my + L * 0.06), genis * (0.55 if yan else 0.64), L * 0.44, aci, KARIN, kontur=False)
    for i in range(3):                                                    # gogus tuyu: karnin ustunde uc krem tutam
        tx = nx_ + kay * 0.8 + (i - 1) * boy * 0.035; ty = ny_ + boy * 0.07
        dr.polygon([(tx * S2 - boy * 0.03 * S2, ty * S2), (tx * S2, (ty + boy * 0.06) * S2), (tx * S2 + boy * 0.03 * S2, ty * S2)], fill=KARIN)
    bacak(taraf[1], KURK); kol(taraf[1], KURK)
    elips((nx_, ny_ + boy * 0.005), boy * (0.11 if yan else 0.14), boy * 0.04, aci, ATKI)     # atki
    uc = 1 if (not yan or bx > hx) else -1
    kapsul((nx_ - uc * boy * 0.07, ny_ + boy * 0.02), (nx_ - uc * boy * 0.09, ny_ + boy * 0.1), boy * 0.03, boy * 0.026, ATKI_K)
    elips((nx_ + kay * 0.6, ny_ + boy * 0.05), boy * 0.03, boy * 0.03, 0, CAN)


def kare(klasor, ad, j, duygu, yan=False):
    Yr = json.load(open(os.path.join(klasor, "yerlesim.json"), encoding="utf-8"))["karakter"]["maskot"]
    W = Image.open(os.path.join(klasor, "karakter", "maskot", "%s-%02d.png" % (ad, j))).width
    UST = 70                                                              # boynuzlar kareden tasmasin (ornek sayfasi payi)
    big = Image.new("RGBA", (W * S2, (W + UST) * S2), (0, 0, 0, 0)); dr = ImageDraw.Draw(big)
    E = {k: [v[0], v[1] + UST] for k, v in Yr["poz"][ad]["eklem"][j].items()}
    govde_ciz(dr, E, Yr["boy_px"], yan)
    kx, ky, ks = Yr["poz"][ad]["kafa"][j]; ky += UST
    u = ks / 30 * OLCEK
    MO.bas(dr, kx, ky - ks * 0.25 + DY * u, u, duygu, yan)
    big = big.resize((W, W + UST), Image.LANCZOS)
    bg = Image.new("RGBA", (W, W + UST), (120, 70, 200, 255)); bg.alpha_composite(big)
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
    cikti = r"C:\Users\eleme\OneDrive\Masaüstü\POZ-DUVARI\taslak\HUMAN-TETRIS-38-MASKOT-ORNEK-2.jpg"
    sayfa.save(cikti, quality=90)
    print("->", cikti, sayfa.size)
