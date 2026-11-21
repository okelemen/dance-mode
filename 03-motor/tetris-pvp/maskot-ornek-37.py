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
    """kartal yavrusu basi: krem tuylu yuvarlak bas (kestane ense), tepede uc sivri tuy, kalin kas tuyu, iri parlak goz,
    kivrik sari gaga (ucu asagi), kizarik yanak; boyunda kirmizi atki zaten 3B govdede. Kendi tasarimimiz."""
    S = lambda v: v * u * S2
    X = lambda v: (cx + v * u) * S2
    Y = lambda v: (cy + v * u) * S2
    def el(x, y, rx, ry, **k): dr.ellipse((X(x) - S(rx), Y(y) - S(ry), X(x) + S(rx), Y(y) + S(ry)), **k)
    w = int(S(1.6))
    if yan:
        for dx, h in ((-6, 30), (0, 33), (6, 29)):                      # tepe tuyu (arkaya yatik)
            dr.polygon([(X(dx - 4), Y(-16)), (X(dx - 6), Y(-h)), (X(dx + 3), Y(-17))], fill=DISK, outline=KN, width=w)
        el(0, 0, 22, 20, fill=DISK, outline=KN, width=w)
        dr.chord((X(-22), Y(-20), X(22), Y(20)), 100, 260, fill=KARAMEL, outline=KN, width=w)   # kestane ense
        el(11, -3, 6.5, 7, fill="#ffffff", outline=KN, width=int(S(1.2))); el(12.5, -3, 4, 4.5, fill=AMBER); el(13.5, -3, 2.4, 2.6, fill=KN)
        dr.line([(X(5), Y(-12)), (X(17), Y(-10))], fill=KAS, width=int(S(3.0)))
        dr.polygon([(X(18), Y(-2)), (X(30), Y(2)), (X(28), Y(9)), (X(24), Y(6)), (X(18), Y(7))], fill=GAGA, outline=KN, width=int(S(1.0)))
        el(9, 10, 3.2, 2, fill="#ff7a8a")
        return
    for dx, h, eg in ((-6, 30, -4), (0, 34, 0), (6, 30, 4)):            # tepede uc sivri tuy (kedi kulagi degil: ortada, dik)
        dr.polygon([(X(dx - 4), Y(-17)), (X(dx + eg), Y(-h)), (X(dx + 4), Y(-17))], fill=DISK, outline=KN, width=w)
    el(0, 0, 24, 21, fill=DISK, outline=KN, width=w)                   # krem tuylu bas
    for sx in (-1, 1):                                                 # yanlarda kestane tuy (bas kenari, ense rengi)
        dr.chord((X(-24), Y(-21), X(24), Y(21)), (150 if sx < 0 else -30), (210 if sx < 0 else 30), fill=KARAMEL, outline=KN, width=w)
    for sx in (-1, 1):
        if duygu == "sevinc":
            dr.arc((X(sx * 9) - S(6), Y(0) - S(6), X(sx * 9) + S(6), Y(0) + S(6)), 200, 340, fill=KN, width=int(S(2.6)))
        elif duygu == "sasirma":
            el(sx * 9, -1, 7.5, 8, fill="#ffffff", outline=KN, width=int(S(1.4))); el(sx * 9, -1, 4, 4.2, fill=AMBER); el(sx * 9, -1, 2.1, 2.1, fill=KN)
            dr.line([(X(sx * 4), Y(-13)), (X(sx * 14), Y(-15))], fill=KAS, width=int(S(2.6)))       # kaslar yukari
        else:
            el(sx * 9, 0, 7, 7.5, fill="#ffffff", outline=KN, width=int(S(1.4)))
            el(sx * 9 + 0.8, 0.6, 4.7, 4.9, fill=AMBER); el(sx * 9 + 1.1, 0.9, 2.8, 3.0, fill=KN)
            el(sx * 9 - 1, -2.2, 1.4, 1.4, fill="#ffffff")
            dr.line([(X(sx * 3), Y(-9)), (X(sx * 15), Y(-11))], fill=KAS, width=int(S(3.0)))        # kararli kas tuyu (cesur, kizgin degil)
        el(sx * 16, 10, 3.6, 2.2, fill="#ff7a8a")
    if duygu == "sasirma":                                              # gaga acik
        dr.polygon([(X(-5), Y(5)), (X(5), Y(5)), (X(3), Y(10)), (X(0), Y(12)), (X(-3), Y(10))], fill=GAGA, outline=KN, width=int(S(1.0)))
        el(0, 15.5, 3.0, 2.6, fill="#7a1020", outline=KN, width=int(S(1.0)))
    else:                                                               # kivrik gaga: genis taban, ucu asagi kanca
        dr.polygon([(X(-5.5), Y(5)), (X(5.5), Y(5)), (X(3.5), Y(11)), (X(0), Y(16)), (X(-1.5), Y(13)), (X(-3.5), Y(11))], fill=GAGA, outline=KN, width=int(S(1.0)))
        dr.line([(X(-4), Y(8.5)), (X(4), Y(8.5))], fill="#e8901a", width=int(S(0.8)))


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
