"""HUMAN TETRIS 34 jole kup hakem maskot ornek sayfasi (TALIMATLAR §4: on/yan, 3-4 poz, 3 duygu) -> POZ-DUVARI/taslak/HUMAN-TETRIS-34-MASKOT-ORNEK.jpg

Govde kareleri Blender/Actions (karakter.py --jole 1; on: varlik-34-maskot-on, yan: --don 90 varlik-34-maskot-yan).
Yuz motor 31 maskotCiz (yuzSadece) ile ayni olculerde PIL'de cizilir: merkez kafa noktasi (ky - ks*0.25) + TEMA.yuzDy, birim ks*1.6/62.
Tasarim kendimiz: turuncu-mango jole kup govde, iri oval gozler, kizarik yanak, acik agiz gulumseme, boyunda kirmizi hakem duduğu.
Bilinen kup/jole karakterlerine benzemez (yuz kupun ust yarisinda, govde tek parca kup, uzuvlar tombul turuncu).
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

BURA = os.path.dirname(os.path.abspath(__file__))
ON = os.path.join(BURA, sys.argv[1] if len(sys.argv) > 1 else "varlik-34-maskot-on")
YAN = os.path.join(BURA, sys.argv[2] if len(sys.argv) > 2 else "varlik-34-maskot-yan")
YUZ_DY = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
YUZ_OL = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
S2 = 4
KN = "#2a0a00"


def yuz(dr, cx, cy, s, duygu):
    S = lambda v: v * s * S2
    X = lambda v: (cx + v * s) * S2
    Y = lambda v: (cy + v * s) * S2
    def el(x, y, rx, ry, **k): dr.ellipse((X(x) - S(rx), Y(y) - S(ry), X(x) + S(rx), Y(y) + S(ry)), **k)
    for sx in (-1, 1):
        if duygu == "sevinc":
            dr.arc((X(sx * 24) - S(12), Y(-6) - S(12), X(sx * 24) + S(12), Y(-6) + S(12)), 205, 335, fill=KN, width=int(S(7)))
        elif duygu == "sasirma":
            el(sx * 24, -8, 17, 17, fill="#ffffff", outline=KN, width=int(S(4)))
            el(sx * 24, -6, 6, 6, fill=KN)
        else:
            el(sx * 24, -8, 15, 18, fill="#ffffff", outline=KN, width=int(S(4)))
            el(sx * 24 + 2, -5, 9, 9, fill=KN)
            el(sx * 24 - 1, -10, 3.5, 3.5, fill="#ffffff")
        el(sx * 46, 18, 12, 7, fill="#ff6a7a")
    if duygu == "sasirma":
        el(0, 30, 9, 12, fill="#7a1020", outline=KN, width=int(S(5)))
    else:
        dr.chord((X(-20), Y(8), X(20), Y(46)), 0, 180, fill="#7a1020", outline=KN, width=int(S(5)))
    dr.line([(X(36), Y(64)), (X(0), Y(72)), (X(-36), Y(56))], fill="#ffd21e", width=int(S(2.5)))
    dr.rounded_rectangle((X(34), Y(58), X(60), Y(71)), radius=S(6), fill="#e8102c", outline="#3a0a10", width=int(S(3)))


def kare(klasor, ad, j, duygu):
    Y = json.load(open(os.path.join(klasor, "yerlesim.json"), encoding="utf-8"))["karakter"]["maskot"]
    im = Image.open(os.path.join(klasor, "karakter", "maskot", "%s-%02d.png" % (ad, j))).convert("RGBA")
    W = im.width
    big = Image.new("RGBA", (W * S2, W * S2), (0, 0, 0, 0))
    kx, ky, ks = Y["poz"][ad]["kafa"][j]
    yuz(ImageDraw.Draw(big), kx, ky - ks * 0.25 + YUZ_DY * ks * 1.6 / 62, ks * 1.6 / 62 * YUZ_OL, duygu)
    big = big.resize((W, W), Image.LANCZOS)
    bg = Image.new("RGBA", (W, W), (40, 190, 70, 255)); bg.alpha_composite(im); bg.alpha_composite(big)   # blok sehri yesil zemini
    return bg.convert("RGB")


if __name__ == "__main__":
    pozlar = ["tiptoe-prayer", "horse-w", "magenta-halo-v-wide", "duel-lunge-diagonal-bolt"]
    hucre = [("ÖN — mutlu", ON, pozlar[1], 0, "mutlu"), ("YAN — gövde hacmi", YAN, pozlar[1], 0, "mutlu"),
             ("PERFECT! — sevinç", ON, pozlar[2], 6, "sevinc"), ("OUT! — şaşkın", ON, pozlar[0], 6, "sasirma"),
             ("POZ: horse-w", ON, pozlar[1], 6, "mutlu"), ("POZ: duel-lunge-diagonal-bolt", ON, pozlar[3], 6, "mutlu")]
    ims = [kare(k, a, j, d) for _, k, a, j, d in hucre]
    w = ims[0].width
    sayfa = Image.new("RGB", (3 * w, 2 * (w + 40)), "white")
    dr = ImageDraw.Draw(sayfa)
    f = ImageFont.truetype("arial.ttf", 22)
    for i, (im, h) in enumerate(zip(ims, hucre)):
        x, y = (i % 3) * w, (i // 3) * (w + 40)
        sayfa.paste(im, (x, y + 40)); dr.text((x + 10, y + 8), h[0], fill="black", font=f)
    cikti = r"C:\Users\eleme\OneDrive\Masaüstü\POZ-DUVARI\taslak\HUMAN-TETRIS-34-MASKOT-ORNEK.jpg"
    sayfa.save(cikti, quality=90)
    print("->", cikti, sayfa.size)
