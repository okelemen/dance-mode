"""HUMAN TETRIS 33 kucuk ejderha hakem maskot ornek sayfasi (TALIMATLAR §4: on/yan, 3-4 poz, 3 duygu) -> POZ-DUVARI/taslak/HUMAN-TETRIS-33-MASKOT-ORNEK.jpg

Govde kareleri Blender/Actions (karakter.py --ejderha 1; on: varlik-33-maskot-on, yan: --don 90 varlik-33-maskot-yan).
2B kafa motor 30 maskotCiz ile ayni olculerde PIL'de cizilir (birim: maskot olcegi s, kafa yaricapi ~66; maskot-ornek-31.py duzeni).
Tasarim kendimiz: yesil tombul yuvarlak bas, sari-yesil burun, iki sari boynuz, turuncu kulak yuzgecleri, buyuk goz, kizarik yanak,
kirmizi hakem fulari altin seritli (arena). Bilinen ejderha karakterlerine benzemez (kanatli siyah/mor degil, sivri cene yok).
"""
import json, math, os
from PIL import Image, ImageDraw, ImageFont

BURA = os.path.dirname(os.path.abspath(__file__))
ON, YAN = os.path.join(BURA, "varlik-33-maskot-on"), os.path.join(BURA, "varlik-33-maskot-yan")
S2 = 4   # supersample
YESIL, KOYU, ACIK, SARI, TURUNCU = "#22c43a", "#0a5a1a", "#7ae86a", "#ffc21e", "#ff7a14"


def kafa(dr, cx, cy, s, duygu):
    S = lambda v: v * s * S2
    X = lambda v: (cx + v * s) * S2
    Y = lambda v: (cy + v * s) * S2
    def el(x, y, rx, ry, **k): dr.ellipse((X(x) - S(rx), Y(y) - S(ry), X(x) + S(rx), Y(y) + S(ry)), **k)
    def ucgen(p, **k): dr.polygon([(X(a), Y(b)) for a, b in p], **k)
    for sx in (-1, 1):                                                   # boynuzlar (sari, tombul) + kulak yuzgecleri (turuncu)
        ucgen([(sx * 22, -50), (sx * 40, -50), (sx * 38, -84)], fill=SARI, outline="#7a4a00", width=int(S(3)))
        ucgen([(sx * 58, -18), (sx * 64, 6), (sx * 92, -28)], fill=TURUNCU, outline="#7a3000", width=int(S(3)))
    el(0, -2, 66, 60, fill=YESIL, outline=KOYU, width=int(S(5)))
    el(-20, -28, 26, 18, fill=ACIK)                                      # parlama
    el(0, 26, 40, 26, fill="#c8f05a", outline=KOYU, width=int(S(2)))     # burun/agiz bolgesi
    for sx in (-1, 1):
        el(sx * 12, 18, 4, 3, fill=KOYU)                                 # burun delikleri
        if duygu == "sevinc":
            dr.arc((X(sx * 24) - S(12), Y(-6) - S(12), X(sx * 24) + S(12), Y(-6) + S(12)), 205, 335, fill="#0a2a10", width=int(S(6)))
        elif duygu == "sasirma":
            el(sx * 24, -8, 16, 16, fill="#ffffff", outline="#0a2a10", width=int(S(3)))
            el(sx * 24, -6, 6, 6, fill="#0a2a10")
        else:
            el(sx * 24, -8, 15, 17, fill="#ffffff", outline="#0a2a10", width=int(S(2)))
            el(sx * 24, -5, 9, 11, fill="#1a2a10")
            el(sx * 24 - 4, -11, 4, 4, fill="#ffffff")
        el(sx * 44, 12, 10, 6, fill="#ff8aa8")                           # yanak
    if duygu == "sasirma":
        el(0, 36, 9, 11, fill="#8a1020", outline="#0a2a10", width=int(S(2)))
    elif duygu == "sevinc":
        dr.chord((X(-18), Y(22), X(18), Y(48)), 0, 180, fill="#8a1020", outline="#0a2a10", width=int(S(2)))
        dr.rectangle((X(-6), Y(34), X(-1), Y(39)), fill="#ffffff"); dr.rectangle((X(1), Y(34), X(6), Y(39)), fill="#ffffff")
    else:
        dr.arc((X(-16), Y(20), X(16), Y(42)), 20, 160, fill="#0a2a10", width=int(S(4)))
        ucgen([(-7, 39), (-1, 39), (-4, 45)], fill="#ffffff")            # kucuk dis
    dr.rounded_rectangle((X(-46), Y(52), X(46), Y(70)), radius=S(9), fill="#e8102c", outline="#3a0008", width=int(S(3)))
    for xx in (-30, -6, 18):
        dr.rectangle((X(xx), Y(53), X(xx + 9), Y(69)), fill="#ffd21e")


def kare(klasor, ad, j, duygu):
    Y = json.load(open(os.path.join(klasor, "yerlesim.json"), encoding="utf-8"))["karakter"]["maskot"]
    im = Image.open(os.path.join(klasor, "karakter", "maskot", "%s-%02d.png" % (ad, j))).convert("RGBA")
    W = im.width
    big = Image.new("RGBA", (W * S2, W * S2), (0, 0, 0, 0))
    dr = ImageDraw.Draw(big)
    kx, ky, ks = Y["poz"][ad]["kafa"][j]
    kafa(dr, kx, ky - ks * 0.25, ks * 1.6 / 62, duygu)   # motor 28-29 ile ayni: yavru maskot buyuk kafa
    big = big.resize((W, W), Image.LANCZOS)
    bg = Image.new("RGBA", (W, W), (255, 214, 150, 255)); bg.alpha_composite(im); bg.alpha_composite(big)   # kum rengi zemin
    return bg.convert("RGB")


pozlar = ["raven-down-reach-curtsy", "cosmic-heel-raise-arms-forward-high", "rise-wave-reach-wide", "sakura-shrug-palms-up"]
hucre = [("ÖN — mutlu", ON, pozlar[2], 0, "mutlu"), ("YAN — gövde hacmi", YAN, pozlar[2], 0, "mutlu"),
         ("PERFECT! — sevinç", ON, pozlar[0], 6, "sevinc"), ("OUT! — şaşkın", ON, pozlar[1], 6, "sasirma"),
         ("POZ: rise-wave-reach-wide", ON, pozlar[2], 6, "mutlu"), ("POZ: sakura-shrug-palms-up", ON, pozlar[3], 6, "mutlu")]
ims = [kare(k, a, j, d) for _, k, a, j, d in hucre]
w = ims[0].width
sayfa = Image.new("RGB", (3 * w, 2 * (w + 40)), "white")
dr = ImageDraw.Draw(sayfa)
f = ImageFont.truetype("arial.ttf", 22)
for i, (im, h) in enumerate(zip(ims, hucre)):
    x, y = (i % 3) * w, (i // 3) * (w + 40)
    sayfa.paste(im, (x, y + 40)); dr.text((x + 10, y + 8), h[0], fill="black", font=f)
cikti = r"C:\Users\eleme\OneDrive\Masaüstü\POZ-DUVARI\taslak\HUMAN-TETRIS-33-MASKOT-ORNEK.jpg"
sayfa.save(cikti, quality=90)
print("->", cikti, sayfa.size)
