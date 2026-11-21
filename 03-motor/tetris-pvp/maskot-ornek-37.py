"""HUMAN TETRIS 37 kartal yavrusu hakem maskot ornek sayfasi (TALIMATLAR §4: on/yan, 3-4 poz, 3 duygu) -> POZ-DUVARI/taslak/HUMAN-TETRIS-37-MASKOT-ORNEK.jpg

Govde kareleri Blender/Actions (karakter.py --kartal 1; on: --don 0, yan: --don 90; duvar-ornek-33.json). maskot-ornek-36.py kopyasi;
kafa 2B (motor birebir cizer): krem tuylu bas + kestane yanlar, tepede uc dik tuy, kalin kas, iri amber goz, kivrik sari gaga.
Kendi tasarimimiz: bilinen kartal karakterlerine / marka amblemlerine benzemez (pilot atkisi gokyuzu hakemi).
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

BURA = os.path.dirname(os.path.abspath(__file__))
ON = os.path.join(BURA, sys.argv[1] if len(sys.argv) > 1 else "varlik-37-maskot-on/tetris-varlik")
YAN = os.path.join(BURA, sys.argv[2] if len(sys.argv) > 2 else "varlik-37-maskot-yan/tetris-varlik")
OLCEK = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
DY = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
S2 = 4
KN = "#3a1606"
KARAMEL, DISK, AMBER, GAGA, YAPRAK = "#a8501a", "#fff0c8", "#ffb01a", "#ffc21a", "#e8102c"
TUY, KAS = "#6a3010", "#5a2408"


def bas(dr, cx, cy, u, duygu, yan=False):
    """kartal yavrusu basi (ornek 2): kestane tuylu yuvarlak bas, onde krem yuz maskesi (iki goz ustunde yukari kivrik),
    arkaya yatik kestane tepe tuyleri, kalin koyu kas, iri amber goz, IRI kivrik sari gaga (ucu asagi kanca). Ornek 1 krem oval
    bas baykus gibi okundu, yan gorunumde kahve/krem sert dikey bolunme vardi."""
    S = lambda v: v * u * S2
    X = lambda v: (cx + v * u) * S2
    Y = lambda v: (cy + v * u) * S2
    def el(x, y, rx, ry, **k): dr.ellipse((X(x) - S(rx), Y(y) - S(ry), X(x) + S(rx), Y(y) + S(ry)), **k)
    w = int(S(1.6))
    if yan:
        for dx, h in ((-14, 24), (-9, 29), (-3, 31)):                    # tepe tuyu arkaya yatik
            dr.polygon([(X(dx + 2), Y(-15)), (X(dx - 9), Y(-h)), (X(dx + 9), Y(-17))], fill=KARAMEL, outline=KN, width=w)
        el(0, 0, 22, 20, fill=KARAMEL, outline=KN, width=w)
        el(9, 3, 13, 13, fill=DISK)                                    # yan yuz maskesi (yumusak gecis, sert cizgi yok)
        el(11, -3, 6.5, 7, fill="#ffffff", outline=KN, width=int(S(1.2))); el(12.5, -3, 4, 4.5, fill=AMBER); el(13.5, -3, 2.4, 2.6, fill=KN)
        dr.line([(X(4), Y(-11)), (X(18), Y(-12))], fill=KAS, width=int(S(3.4)))
        dr.polygon([(X(16), Y(-3)), (X(31), Y(0)), (X(33), Y(8)), (X(28), Y(13)), (X(27), Y(7)), (X(16), Y(8))], fill=GAGA, outline=KN, width=int(S(1.1)))
        el(8, 11, 3.2, 2, fill="#ff7a8a")
        return
    for dx, h, eg in ((-9, 27, -10), (0, 33, -3), (9, 27, 6)):          # tepe tuyleri (kestane, hafif saga savrulmus)
        dr.polygon([(X(dx - 5), Y(-16)), (X(dx + eg), Y(-h)), (X(dx + 5), Y(-17))], fill=KARAMEL, outline=KN, width=w)
    el(0, 0, 24, 21, fill=KARAMEL, outline=KN, width=w)                # kestane bas
    dr.polygon([(X(-19), Y(-6)), (X(-10), Y(-12)), (X(0), Y(-8)), (X(10), Y(-12)), (X(19), Y(-6)), (X(17), Y(10)),
                (X(8), Y(18)), (X(-8), Y(18)), (X(-17), Y(10))], fill=DISK)                         # krem yuz maskesi
    for sx in (-1, 1):
        if duygu == "sevinc":
            dr.arc((X(sx * 9) - S(6), Y(0) - S(6), X(sx * 9) + S(6), Y(0) + S(6)), 200, 340, fill=KN, width=int(S(2.6)))
        elif duygu == "sasirma":
            el(sx * 9, -1, 7.5, 8, fill="#ffffff", outline=KN, width=int(S(1.4))); el(sx * 9, -1, 4, 4.2, fill=AMBER); el(sx * 9, -1, 2.1, 2.1, fill=KN)
            dr.line([(X(sx * 4), Y(-13)), (X(sx * 15), Y(-16))], fill=KAS, width=int(S(3.0)))
        else:
            el(sx * 9, 0, 7, 7.5, fill="#ffffff", outline=KN, width=int(S(1.4)))
            el(sx * 9 + 0.8, 0.6, 4.7, 4.9, fill=AMBER); el(sx * 9 + 1.1, 0.9, 2.8, 3.0, fill=KN)
            el(sx * 9 - 1, -2.2, 1.4, 1.4, fill="#ffffff")
            dr.line([(X(sx * 3), Y(-9)), (X(sx * 16), Y(-12))], fill=KAS, width=int(S(3.4)))
        el(sx * 15, 11, 3.6, 2.2, fill="#ff7a8a")
    if duygu == "sasirma":
        dr.polygon([(X(-6.5), Y(5)), (X(6.5), Y(5)), (X(4), Y(11)), (X(0), Y(13)), (X(-4), Y(11))], fill=GAGA, outline=KN, width=int(S(1.1)))
        el(0, 17, 3.4, 2.8, fill="#7a1020", outline=KN, width=int(S(1.0)))
    else:                                                               # iri kivrik gaga: genis taban, ucu asagi kanca
        dr.polygon([(X(-7), Y(4)), (X(7), Y(4)), (X(5), Y(11)), (X(1.5), Y(19)), (X(-1), Y(16)), (X(-4.5), Y(11))], fill=GAGA, outline=KN, width=int(S(1.1)))
        dr.line([(X(-5), Y(8.5)), (X(5), Y(8.5))], fill="#e8901a", width=int(S(0.9)))


def kare(klasor, ad, j, duygu, yan=False):
    Yr = json.load(open(os.path.join(klasor, "yerlesim.json"), encoding="utf-8"))["karakter"]["maskot"]
    im = Image.open(os.path.join(klasor, "karakter", "maskot", "%s-%02d.png" % (ad, j))).convert("RGBA")
    W = im.width
    big = Image.new("RGBA", (W * S2, W * S2), (0, 0, 0, 0))
    kx, ky, ks = Yr["poz"][ad]["kafa"][j]
    u = ks / 30 * OLCEK
    bas(ImageDraw.Draw(big), kx, ky - ks * 0.25 + DY * u, u, duygu, yan)
    big = big.resize((W, W), Image.LANCZOS)
    bg = Image.new("RGBA", (W, W), (90, 190, 255, 255)); bg.alpha_composite(im); bg.alpha_composite(big)   # gok mavisi
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
    cikti = r"C:\Users\eleme\OneDrive\Masaüstü\POZ-DUVARI\taslak\HUMAN-TETRIS-37-MASKOT-ORNEK.jpg"
    sayfa.save(cikti, quality=90)
    print("->", cikti, sayfa.size)
