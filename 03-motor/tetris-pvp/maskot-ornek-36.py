"""HUMAN TETRIS 36 baykus yavrusu hakem maskot ornek sayfasi (TALIMATLAR §4: on/yan, 3-4 poz, 3 duygu) -> POZ-DUVARI/taslak/HUMAN-TETRIS-36-MASKOT-ORNEK.jpg

Govde kareleri Blender/Actions (karakter.py --baykus 1; on: --don 0, yan: --don 90; ornek duvar listesi duvar-ornek-33.json).
Kafa 2B (motor bunu birebir cizer): genis yuvarlak karamel bas, iki yana-yukari kalkik kulak tuyu, iki daireden olusan krem
yuz diski, kocaman parlak gozler (amber halka), kucuk turuncu asagi gaga, kizarik yanak, iki kulak arasinda kucuk yesil yaprak.
Kendi tasarimimiz: bilinen baykus karakterlerine benzemez (gozluk/kep/kitap yok; yaprak + yesil atki orman hakemi).
Merkez: yerlesim.json karakter.maskot.poz[ad].kafa[j] = (kx, ky, ks); birim u = ks / 30.
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

BURA = os.path.dirname(os.path.abspath(__file__))
ON = os.path.join(BURA, sys.argv[1] if len(sys.argv) > 1 else "varlik-36-maskot-on/tetris-varlik")
YAN = os.path.join(BURA, sys.argv[2] if len(sys.argv) > 2 else "varlik-36-maskot-yan/tetris-varlik")
OLCEK = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
DY = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
S2 = 4
KN = "#3a1606"
KARAMEL, DISK, AMBER, GAGA, YAPRAK = "#c8782a", "#ffe2a8", "#ffb01a", "#ff8a10", "#20c850"


def bas(dr, cx, cy, u, duygu, yan=False):
    S = lambda v: v * u * S2
    X = lambda v: (cx + v * u) * S2
    Y = lambda v: (cy + v * u) * S2
    def el(x, y, rx, ry, **k): dr.ellipse((X(x) - S(rx), Y(y) - S(ry), X(x) + S(rx), Y(y) + S(ry)), **k)
    w = int(S(1.6))
    if yan:
        dr.polygon([(X(4), Y(-16)), (X(10), Y(-32)), (X(14), Y(-15))], fill=KARAMEL, outline=KN, width=w)   # kulak tuyu
        el(0, 0, 22, 20, fill=KARAMEL, outline=KN, width=w)
        el(10, 0, 12, 13, fill=DISK)
        el(12, -2, 6.5, 7, fill="#ffffff", outline=KN, width=int(S(1.2))); el(13.5, -2, 4, 4.5, fill=AMBER); el(14.5, -2, 2.4, 2.6, fill=KN)
        dr.polygon([(X(19), Y(3)), (X(26), Y(6)), (X(19), Y(10))], fill=GAGA, outline=KN, width=int(S(1.0)))
        el(9, 9, 3.2, 2, fill="#ff7a8a")
        dr.polygon([(X(-2), Y(-19)), (X(3), Y(-30)), (X(7), Y(-19))], fill=YAPRAK, outline=KN, width=int(S(1.0)))
        return
    for sx in (-1, 1):                                           # kulak tuyleri (yana-yukari)
        dr.polygon([(X(sx * 8), Y(-15)), (X(sx * 22), Y(-33)), (X(sx * 19), Y(-11))], fill=KARAMEL, outline=KN, width=w)
        dr.polygon([(X(sx * 11), Y(-16)), (X(sx * 19), Y(-27)), (X(sx * 17), Y(-14))], fill="#8a4a1a")
    el(0, 0, 24, 21, fill=KARAMEL, outline=KN, width=w)          # bas
    dr.polygon([(X(-3), Y(-19)), (X(0), Y(-31)), (X(4), Y(-19))], fill=YAPRAK, outline=KN, width=int(S(1.0)))   # yaprak
    dr.line([(X(0.5), Y(-19)), (X(0.3), Y(-28))], fill="#108a2a", width=int(S(0.6)))
    for sx in (-1, 1):
        el(sx * 9.5, 1, 11, 12, fill=DISK)                       # yuz diski (iki daire)
    for sx in (-1, 1):
        if duygu == "sevinc":
            dr.arc((X(sx * 9.5) - S(6), Y(1) - S(6), X(sx * 9.5) + S(6), Y(1) + S(6)), 200, 340, fill=KN, width=int(S(2.6)))
        elif duygu == "sasirma":
            el(sx * 9.5, 0, 8, 8.5, fill="#ffffff", outline=KN, width=int(S(1.4))); el(sx * 9.5, 0, 4.2, 4.4, fill=AMBER); el(sx * 9.5, 0, 2.2, 2.2, fill=KN)
        else:
            el(sx * 9.5, 0, 7.5, 8, fill="#ffffff", outline=KN, width=int(S(1.4)))
            el(sx * 9.5 + 0.8, 0.5, 5, 5.2, fill=AMBER); el(sx * 9.5 + 1.2, 0.8, 3, 3.2, fill=KN)
            el(sx * 9.5 - 1, -2.4, 1.4, 1.4, fill="#ffffff")
        el(sx * 17, 11, 3.6, 2.2, fill="#ff7a8a")
    if duygu == "sasirma":
        dr.polygon([(X(-3.5), Y(8)), (X(3.5), Y(8)), (X(0), Y(13))], fill=GAGA, outline=KN, width=int(S(1.0)))
        el(0, 15.5, 2.6, 2.4, fill="#7a1020", outline=KN, width=int(S(1.0)))
    else:
        dr.polygon([(X(-3.5), Y(8)), (X(3.5), Y(8)), (X(0), Y(15))], fill=GAGA, outline=KN, width=int(S(1.0)))


def kare(klasor, ad, j, duygu, yan=False):
    Yr = json.load(open(os.path.join(klasor, "yerlesim.json"), encoding="utf-8"))["karakter"]["maskot"]
    im = Image.open(os.path.join(klasor, "karakter", "maskot", "%s-%02d.png" % (ad, j))).convert("RGBA")
    W = im.width
    big = Image.new("RGBA", (W * S2, W * S2), (0, 0, 0, 0))
    kx, ky, ks = Yr["poz"][ad]["kafa"][j]
    u = ks / 30 * OLCEK
    bas(ImageDraw.Draw(big), kx, ky - ks * 0.25 + DY * u, u, duygu, yan)
    big = big.resize((W, W), Image.LANCZOS)
    bg = Image.new("RGBA", (W, W), (120, 210, 150, 255)); bg.alpha_composite(im); bg.alpha_composite(big)   # orman yesili
    return bg.convert("RGB")


if __name__ == "__main__":
    P = ["raven-down-reach-curtsy", "cosmic-heel-raise-arms-forward-high", "rise-wave-reach-wide", "sakura-shrug-palms-up"]
    hucre = [("ÖN — mutlu", ON, P[1], 0, "mutlu", False), ("YAN — gövde + kanat", YAN, P[1], 0, "mutlu", True),
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
    cikti = r"C:\Users\eleme\OneDrive\Masaüstü\POZ-DUVARI\taslak\HUMAN-TETRIS-36-MASKOT-ORNEK.jpg"
    sayfa.save(cikti, quality=90)
    print("->", cikti, sayfa.size)
