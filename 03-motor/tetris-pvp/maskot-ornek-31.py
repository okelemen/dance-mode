"""HUMAN TETRIS 31 penguen hakem maskot ornek sayfasi (TALIMATLAR §4: on/yan, 3-4 poz, 3 duygu) -> POZ-DUVARI/taslak/HUMAN-TETRIS-31-MASKOT-ORNEK.jpg

Govde kareleri Blender/Actions (karakter.py --penguen 1; on: varlik-31-maskot-on2, yan: --don 90 varlik-31-maskot-yan2).
2B kafa motor 28 maskotCiz ile ayni olculerde PIL'de cizilir (birim: maskot olcegi s, kafa yaricapi ~66). Yan gorunumde kafa da onden cizilir
(motor yalniz on gorunum kullanir; yan gorunum govde hacmini gostermek icin).
"""
import json, math, os
from PIL import Image, ImageDraw, ImageFont

BURA = os.path.dirname(os.path.abspath(__file__))
ON, YAN = os.path.join(BURA, "varlik-31-maskot-on2"), os.path.join(BURA, "varlik-31-maskot-yan2")
S2 = 4   # supersample


def kafa(dr, cx, cy, s, duygu):
    S = lambda v: v * s * S2
    X = lambda v: (cx + v * s) * S2
    Y = lambda v: (cy + v * s) * S2
    def el(x, y, rx, ry, **k): dr.ellipse((X(x) - S(rx), Y(y) - S(ry), X(x) + S(rx), Y(y) + S(ry)), **k)
    el(0, -2, 66, 60, fill="#1c2a5a", outline="#0a0f2a", width=int(S(5)))
    el(-18, -26, 30, 24, fill="#2e4a9a")
    # beyaz kalp yuz lekesi (iki ust daire + alt oval)
    for sx in (-1, 1):
        el(sx * 24, 2, 30, 34, fill="#f6faff")
    el(0, 22, 40, 30, fill="#f6faff")
    for sx in (-1, 1):
        if duygu == "sevinc":
            dr.arc((X(sx * 20) - S(11), Y(2) - S(11), X(sx * 20) + S(11), Y(2) + S(11)), 205, 335, fill="#141e48", width=int(S(6)))
        elif duygu == "sasirma":
            el(sx * 21, -4, 15, 15, fill="#ffffff", outline="#141e48", width=int(S(3)))
            el(sx * 21, -2, 6, 6, fill="#141e48")
        else:
            el(sx * 20, -2, 11, 14, fill="#141e48")
            el(sx * 20 - 4, -8, 5, 5, fill="#ffffff"); el(sx * 20 + 3, 3, 2.2, 2.2, fill="#ffffff")
        el(sx * 36, 20, 10, 6, fill="#ff8aa8")
    if duygu == "sasirma":
        dr.polygon([(X(-13), Y(12)), (X(13), Y(12)), (X(0), Y(20))], fill="#ff9a1a", outline="#7a3000")
        dr.polygon([(X(-10), Y(24)), (X(10), Y(24)), (X(0), Y(33))], fill="#ff7a10", outline="#7a3000")
    else:
        dr.polygon([(X(-12), Y(14)), (X(12), Y(14)), (X(0), Y(28))], fill="#ff9a1a", outline="#7a3000")
    el(-22, -40, 18, 8, fill="#5a78c8")
    dr.rounded_rectangle((X(-46), Y(46), X(46), Y(64)), radius=S(9), fill="#ff2a3a", outline="#0a0f2a", width=int(S(3)))
    for xx in (-30, -6, 18):
        dr.rectangle((X(xx), Y(47), X(xx + 9), Y(63)), fill="#ffffff")


def kare(klasor, ad, j, duygu, olcek=1.0):
    Y = json.load(open(os.path.join(klasor, "yerlesim.json"), encoding="utf-8"))["karakter"]["maskot"]
    im = Image.open(os.path.join(klasor, "karakter", "maskot", "%s-%02d.png" % (ad, j))).convert("RGBA")
    W = im.width
    big = Image.new("RGBA", (W * S2, W * S2), (0, 0, 0, 0))
    dr = ImageDraw.Draw(big)
    kx, ky, ks = Y["poz"][ad]["kafa"][j]
    kafa(dr, kx, ky - ks * 0.25, ks * 1.6 / 62, duygu)   # motor 28 ile ayni: yavru penguen buyuk kafa
    big = big.resize((W, W), Image.LANCZOS)
    bg = Image.new("RGBA", (W, W), (196, 236, 255, 255)); bg.alpha_composite(im); bg.alpha_composite(big)
    return bg.convert("RGB")


pozlar = ["spider-stork-up-down", "nebula-crescent-lean-left", "low-v-stance", "petal-t-v-wide"]
hucre = [("ÖN — mutlu", ON, pozlar[2], 0, "mutlu"), ("YAN — gövde hacmi", YAN, pozlar[2], 0, "mutlu"),
         ("PERFECT! — sevinç", ON, pozlar[0], 6, "sevinc"), ("OUT! — şaşkın", ON, pozlar[1], 6, "sasirma"),
         ("POZ: low-v-stance", ON, pozlar[2], 6, "mutlu"), ("POZ: petal-t-v-wide", ON, pozlar[3], 6, "mutlu")]
ims = [kare(k, a, j, d) for _, k, a, j, d in hucre]
w = ims[0].width
sayfa = Image.new("RGB", (3 * w, 2 * (w + 40)), "white")
dr = ImageDraw.Draw(sayfa)
f = ImageFont.truetype("arial.ttf", 22)
for i, (im, h) in enumerate(zip(ims, hucre)):
    x, y = (i % 3) * w, (i // 3) * (w + 40)
    sayfa.paste(im, (x, y + 40)); dr.text((x + 10, y + 8), h[0], fill="black", font=f)
cikti = r"C:\Users\eleme\OneDrive\Masaüstü\POZ-DUVARI\taslak\HUMAN-TETRIS-31-MASKOT-ORNEK.jpg"
sayfa.save(cikti, quality=90)
print("->", cikti, sayfa.size)
