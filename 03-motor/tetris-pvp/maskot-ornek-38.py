"""HUMAN TETRIS 38 ren geyigi yavrusu hakem maskot ornek sayfasi (TALIMATLAR §4: on/yan, 3-4 poz, 3 duygu) -> POZ-DUVARI/taslak/HUMAN-TETRIS-38-MASKOT-ORNEK.jpg

Govde kareleri Blender/Actions (karakter.py --rengeyik 1; on: --don 0, yan: --don 90; duvar-ornek-33.json). maskot-ornek-37.py kopyasi;
kafa 2B (motor birebir cizer): yuvarlak sicak kahve bas, krem-karamel burun-agiz bolgesi, kucuk KOYU KAHVE burun (parlak kirmizi burun yok -
bilinen ren geyigi karakterine benzemez), iri parlak goz, yana acik kulaklar (pembe ic), iki dalli tombul ten rengi boynuz, alinda krem lekeler,
boynuzda kucuk kirmizi kurdele (Christmas).
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

BURA = os.path.dirname(os.path.abspath(__file__))
ON = os.path.join(BURA, sys.argv[1] if len(sys.argv) > 1 else "varlik-38-maskot-on/tetris-varlik")
YAN = os.path.join(BURA, sys.argv[2] if len(sys.argv) > 2 else "varlik-38-maskot-yan/tetris-varlik")
OLCEK = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
DY = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
S2 = 4
KN = "#2a1004"
KURK, AGIZ, BOYNUZ, BURUN, KULAK_IC, LEKE = "#b8621e", "#ffc880", "#e8b060", "#4a1e08", "#ff8aa8", "#ffe0a8"


def bas(dr, cx, cy, u, duygu, yan=False):
    S = lambda v: v * u * S2
    X = lambda v: (cx + v * u) * S2
    Y = lambda v: (cy + v * u) * S2
    def el(x, y, rx, ry, **k): dr.ellipse((X(x) - S(rx), Y(y) - S(ry), X(x) + S(rx), Y(y) + S(ry)), **k)
    w = int(S(1.6))
    def boynuz(sx, kay=0.0):
        """iki dalli tombul boynuz: ana dal yukari-disa, bir yan dal; yuvarlak uclar"""
        bw = int(S(5.2))
        p0, p1, p2 = (X(sx * 9 + kay), Y(-15)), (X(sx * 15 + kay), Y(-29)), (X(sx * 13 + kay), Y(-38))
        q1 = (X(sx * 22 + kay), Y(-31))
        for a, b in ((p0, p1), (p1, p2), (p1, q1)):
            dr.line([a, b], fill=KN, width=bw + int(S(2.4)))
        for a, b in ((p0, p1), (p1, p2), (p1, q1)):
            dr.line([a, b], fill=BOYNUZ, width=bw)
        for c in (p2, q1):
            dr.ellipse((c[0] - S(2.9), c[1] - S(2.9), c[0] + S(2.9), c[1] + S(2.9)), fill=BOYNUZ, outline=KN, width=int(S(1.1)))
        if sx < 0:                                                    # sol boynuzda kirmizi kurdele
            kx, ky = X(sx * 12 + kay), Y(-23)
            for d in (-1, 1):
                dr.ellipse((kx + d * S(4) - S(3.4), ky - S(2.2), kx + d * S(4) + S(3.4), ky + S(2.2)), fill="#e8102c", outline=KN, width=int(S(0.9)))
            dr.ellipse((kx - S(1.6), ky - S(1.6), kx + S(1.6), ky + S(1.6)), fill="#ffc21a", outline=KN, width=int(S(0.8)))
    if yan:
        boynuz(-1, 2); boynuz(1, -4)
        dr.polygon([(X(-14), Y(-6)), (X(-30), Y(-12)), (X(-26), Y(-3))], fill=KURK, outline=KN, width=w)   # kulak arkaya
        el(0, 0, 20, 19, fill=KURK, outline=KN, width=w)
        el(15, 7, 12, 9, fill=AGIZ, outline=KN, width=int(S(1.2)))     # one uzanan burun-agiz
        el(25, 4, 3.6, 3.0, fill=BURUN)
        el(6, -4, 5.5, 6.5, fill="#ffffff", outline=KN, width=int(S(1.2))); el(7.5, -3.5, 3.6, 4.4, fill=KN); el(6.4, -5.6, 1.2, 1.2, fill="#ffffff")
        el(8, 6, 3.0, 1.9, fill="#ff7a8a")
        return
    boynuz(-1); boynuz(1)
    for sx in (-1, 1):                                                # yana acik kulaklar (pembe ic)
        dr.polygon([(X(sx * 15), Y(-10)), (X(sx * 32), Y(-15)), (X(sx * 27), Y(-4))], fill=KURK, outline=KN, width=w)
        dr.polygon([(X(sx * 18), Y(-9)), (X(sx * 29), Y(-13)), (X(sx * 26), Y(-6))], fill=KULAK_IC)
    el(0, 0, 22, 20, fill=KURK, outline=KN, width=w)                  # kahve bas
    el(0, -11, 4, 3, fill=LEKE); el(-6, -14, 2, 1.6, fill=LEKE); el(6, -14, 2, 1.6, fill=LEKE)   # alin lekeleri
    el(0, 9, 13, 9, fill=AGIZ, outline=KN, width=int(S(1.2)))        # krem-karamel burun-agiz
    el(0, 4.5, 4.6, 3.4, fill=BURUN); el(-1.4, 3.6, 1.3, 0.9, fill="#a86a4a")   # kucuk koyu kahve burun + parlama
    for sx in (-1, 1):
        if duygu == "sevinc":
            dr.arc((X(sx * 9) - S(5.5), Y(-3) - S(5.5), X(sx * 9) + S(5.5), Y(-3) + S(5.5)), 200, 340, fill=KN, width=int(S(2.6)))
        elif duygu == "sasirma":
            el(sx * 9, -4, 6.5, 7.5, fill="#ffffff", outline=KN, width=int(S(1.4))); el(sx * 9, -4, 2.6, 2.8, fill=KN)
        else:
            el(sx * 9, -3, 6, 7, fill="#ffffff", outline=KN, width=int(S(1.4)))
            el(sx * 9 + 0.7, -2.4, 4.0, 4.8, fill=KN); el(sx * 9 - 0.8, -4.6, 1.5, 1.5, fill="#ffffff")
        el(sx * 15, 5, 3.4, 2.1, fill="#ff7a8a")
    if duygu == "sasirma":
        el(0, 13.5, 3.0, 2.6, fill="#7a1020", outline=KN, width=int(S(1.0)))
    else:
        dr.arc((X(-5), Y(8), X(5), Y(15)), 20, 160, fill=KN, width=int(S(1.4)))


def kare(klasor, ad, j, duygu, yan=False):
    Yr = json.load(open(os.path.join(klasor, "yerlesim.json"), encoding="utf-8"))["karakter"]["maskot"]
    im = Image.open(os.path.join(klasor, "karakter", "maskot", "%s-%02d.png" % (ad, j))).convert("RGBA")
    W = im.width
    big = Image.new("RGBA", (W * S2, W * S2), (0, 0, 0, 0))
    kx, ky, ks = Yr["poz"][ad]["kafa"][j]
    u = ks / 30 * OLCEK
    bas(ImageDraw.Draw(big), kx, ky - ks * 0.25 + DY * u, u, duygu, yan)
    big = big.resize((W, W), Image.LANCZOS)
    bg = Image.new("RGBA", (W, W), (120, 70, 200, 255)); bg.alpha_composite(im); bg.alpha_composite(big)   # alacakaranlik moru
    return bg.convert("RGB")


if __name__ == "__main__":
    P = ["raven-down-reach-curtsy", "cosmic-heel-raise-arms-forward-high", "rise-wave-reach-wide", "sakura-shrug-palms-up"]
    hucre = [("ÖN — mutlu", ON, P[1], 0, "mutlu", False), ("YAN — gövde + boynuz", YAN, P[1], 0, "mutlu", True),
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
    cikti = r"C:\Users\eleme\OneDrive\Masaüstü\POZ-DUVARI\taslak\HUMAN-TETRIS-38-MASKOT-ORNEK.jpg"
    sayfa.save(cikti, quality=90)
    print("->", cikti, sayfa.size)
