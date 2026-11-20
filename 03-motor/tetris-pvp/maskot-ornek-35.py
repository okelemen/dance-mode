"""HUMAN TETRIS 35 ucan sincap hakem maskot ornek sayfasi (TALIMATLAR §4: on/yan, 3-4 poz, 3 duygu) -> POZ-DUVARI/taslak/HUMAN-TETRIS-35-MASKOT-ORNEK.jpg

Govde kareleri Blender/Actions (karakter.py --sincap 1; on: --don 0, yan: --don 90; ornek duvar listesi duvar-ornek-33.json).
Kafa 2B (motor bunu birebir cizer): turuncu yuvarlak bas + krem burun-agiz bolgesi, iki sivri kulak (pembe ic), alinda
kahve cerceveli turkuaz camli PILOT GOZLUGU + kayis, iri parlak gozler, kizarik yanak, koyu kahve burun, iki on disli gulumseme.
Kendi tasarimimiz: bilinen sincap karakterlerine benzemez (pilot gozlugu alinda, krem yuz maskesi, kirmizi atki govdede 3B).
Merkez: yerlesim.json karakter.maskot.poz[ad].kafa[j] = (kx, ky, ks); birim u = ks / 30.
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

BURA = os.path.dirname(os.path.abspath(__file__))
ON = os.path.join(BURA, sys.argv[1] if len(sys.argv) > 1 else "varlik-35-maskot-on3/tetris-varlik")
YAN = os.path.join(BURA, sys.argv[2] if len(sys.argv) > 2 else "varlik-35-maskot-yan3/tetris-varlik")
OLCEK = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
DY = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
S2 = 4
KN = "#3a1606"
TURUNCU, KREM, PEMBE_IC = "#d8702e", "#ffe6c0", "#ff9ab0"


def bas(dr, cx, cy, u, duygu, yan=False):
    S = lambda v: v * u * S2
    X = lambda v: (cx + v * u) * S2
    Y = lambda v: (cy + v * u) * S2
    def el(x, y, rx, ry, **k): dr.ellipse((X(x) - S(rx), Y(y) - S(ry), X(x) + S(rx), Y(y) + S(ry)), **k)
    for sx in ((1,) if yan else (-1, 1)):                    # kulaklar (sivri, pembe ic)
        bx = sx * 15 + (4 if yan else 0)
        dr.polygon([(X(bx - 8), Y(-14)), (X(bx + sx * 3), Y(-34)), (X(bx + 8), Y(-12))], fill=TURUNCU, outline=KN, width=int(S(1.6)))
        dr.polygon([(X(bx - 4), Y(-15)), (X(bx + sx * 2), Y(-28)), (X(bx + 4), Y(-14))], fill=PEMBE_IC)
    el(0, 0, 22, 20, fill=TURUNCU, outline=KN, width=int(S(1.6)))   # bas
    if yan:
        el(12, 6, 11, 10, fill=KREM)
        el(21, 3, 3, 2.4, fill=KN)
        el(8, -2, 5, 6, fill="#ffffff", outline=KN, width=int(S(1.2))); el(9.5, -1, 3, 3, fill=KN)
        dr.rectangle((X(-22), Y(-15), X(14), Y(-11)), fill="#5a2a10")               # kayis
        el(10, -14, 6, 5, fill="#22d0c8", outline="#5a2a10", width=int(S(2)))       # gozluk (yan)
        return
    el(0, 8, 15, 11, fill=KREM)                                  # krem yuz maskesi
    dr.rounded_rectangle((X(-22), Y(-17), X(22), Y(-12)), radius=S(2), fill="#5a2a10")   # gozluk kayisi
    for sx in (-1, 1):                                           # pilot gozlugu alinda
        el(sx * 8, -15, 6.5, 5.5, fill="#22d0c8", outline="#5a2a10", width=int(S(2.2)))
        el(sx * 8 - 2, -17, 1.8, 1.4, fill="#e8fffd")
    for sx in (-1, 1):
        if duygu == "sevinc":
            dr.arc((X(sx * 8) - S(5), Y(-1) - S(5), X(sx * 8) + S(5), Y(-1) + S(5)), 205, 335, fill=KN, width=int(S(2.4)))
        elif duygu == "sasirma":
            el(sx * 8, -2, 5.5, 5.5, fill="#ffffff", outline=KN, width=int(S(1.4))); el(sx * 8, -1, 2, 2, fill=KN)
        else:
            el(sx * 8, -2, 4.8, 5.8, fill="#ffffff", outline=KN, width=int(S(1.4)))
            el(sx * 8 + 0.8, -1, 3, 3, fill=KN); el(sx * 8 - 0.4, -2.8, 1.1, 1.1, fill="#ffffff")
        el(sx * 15, 7, 3.6, 2.2, fill="#ff7a8a")
    el(0, 5, 2.6, 2, fill=KN)                                    # burun
    if duygu == "sasirma":
        el(0, 12, 3, 4, fill="#7a1020", outline=KN, width=int(S(1.4)))
    else:
        dr.chord((X(-6), Y(6), X(6), Y(16)), 0, 180, fill="#7a1020", outline=KN, width=int(S(1.4)))
        dr.rectangle((X(-2), Y(11), X(2), Y(14)), fill="#ffffff", outline=KN, width=int(S(0.6)))   # iki on dis
        dr.line([(X(0), Y(11)), (X(0), Y(14))], fill=KN, width=int(S(0.6)))


def kare(klasor, ad, j, duygu, yan=False):
    Yr = json.load(open(os.path.join(klasor, "yerlesim.json"), encoding="utf-8"))["karakter"]["maskot"]
    im = Image.open(os.path.join(klasor, "karakter", "maskot", "%s-%02d.png" % (ad, j))).convert("RGBA")
    W = im.width
    big = Image.new("RGBA", (W * S2, W * S2), (0, 0, 0, 0))
    kx, ky, ks = Yr["poz"][ad]["kafa"][j]
    u = ks / 30 * OLCEK
    bas(ImageDraw.Draw(big), kx, ky - ks * 0.25 + DY * u, u, duygu, yan)
    big = big.resize((W, W), Image.LANCZOS)
    bg = Image.new("RGBA", (W, W), (90, 180, 255, 255)); bg.alpha_composite(im); bg.alpha_composite(big)   # festival gogu
    return bg.convert("RGB")


if __name__ == "__main__":
    P = ["raven-down-reach-curtsy", "cosmic-heel-raise-arms-forward-high", "rise-wave-reach-wide", "sakura-shrug-palms-up"]
    hucre = [("ÖN — mutlu", ON, P[1], 0, "mutlu", False), ("YAN — gövde + kuyruk", YAN, P[1], 0, "mutlu", True),
             ("PERFECT! — sevinç", ON, P[2], 5, "sevinc", False), ("OUT! — şaşkın", ON, P[0], 5, "sasirma", False),
             ("POZ: " + P[3], ON, P[3], 5, "mutlu", False), ("YAN POZ: " + P[2], YAN, P[2], 5, "mutlu", True)]
    ims = [kare(k, a, j, d, y) for _, k, a, j, d, y in hucre]
    w = ims[0].width
    sayfa = Image.new("RGB", (3 * w, 2 * (w + 40)), "white")
    dr = ImageDraw.Draw(sayfa)
    f = ImageFont.truetype("arial.ttf", 22)
    for i, (im, h) in enumerate(zip(ims, hucre)):
        x, y = (i % 3) * w, (i // 3) * (w + 40)
        sayfa.paste(im, (x, y + 40)); dr.text((x + 10, y + 8), h[0], fill="black", font=f)
    cikti = r"C:\Users\eleme\OneDrive\Masaüstü\POZ-DUVARI\taslak\HUMAN-TETRIS-35-MASKOT-ORNEK.jpg"
    sayfa.save(cikti, quality=90)
    print("->", cikti, sayfa.size)
