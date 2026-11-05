"""HUMAN TETRIS 19 kapak silueti - PIKTOGRAM (5 Kas 2026, kullanici: "Siluet piktogram olsun").
REF-070 kapagindaki figur: ayri yuvarlak kafa, kalin duz govde, yuvarlak uclu kalin uzuvlar, giysi/parmak yok. Mixamo govdesi yerine bu cizilir.
Cikti: <klasor>/poz/<ad>.png (saydam, siyah), kapak-tek-19.py --poz-klasor <klasor> ile kullanilir.

    python kapak-piktogram-19.py --klasor ../03-motor/tetris-pvp/varlik-19-pikto
"""
import argparse, math, os
from PIL import Image, ImageDraw

p = argparse.ArgumentParser(); p.add_argument("--klasor", required=True); a = p.parse_args()
os.makedirs(os.path.join(a.klasor, "poz"), exist_ok=True)
S = 400   # birim -> piksel (cizim 4x, sonra kucultulur)

# bird-dog, yuz saga: kalca (0,0); y yukari. Zemin y=-0.95 (diz ve el ayni hizada, referanstaki gibi yere yakin).
# kapak 1: uzuvlar ince kaldi (cop adam); kapak 2: esit kalin uzuvlar kutuk gibi -> referanstaki gibi govdeden uca INCELEN uzuvlar
# uzuv: (bas, son, cap_bas, cap_son)
POZLAR = {
    "pikto-bird-dog": {
        "omuz": (1.0, 0.12), "kafa": ((1.50, 0.40), 0.25),
        "uzuv": [((1.0, 0.12), (2.0, 0.18), 0.26, 0.16),          # ileri uzanan kol
                 ((1.0, 0.12), (1.06, -0.92), 0.26, 0.19),        # destek kolu (yere)
                 ((0.0, 0.0), (-0.02, -0.84), 0.36, 0.24),        # diz cokulen bacak: uyluk
                 ((-0.02, -0.84), (-0.82, -0.92), 0.24, 0.16),    # baldir (yerde, geride)
                 ((0.0, 0.0), (-1.55, 0.32), 0.32, 0.16)],        # geri uzanan bacak
    },
    "pikto-bird-dog-high": {
        "omuz": (1.0, 0.16), "kafa": ((1.50, 0.46), 0.25),
        "uzuv": [((1.0, 0.16), (1.94, 0.46), 0.26, 0.16),
                 ((1.0, 0.16), (1.06, -0.92), 0.26, 0.19),
                 ((0.0, 0.0), (-0.02, -0.84), 0.36, 0.24),
                 ((-0.02, -0.84), (-0.82, -0.92), 0.24, 0.16),
                 ((0.0, 0.0), (-1.48, 0.58), 0.32, 0.16)],
    },
}


def kapsul(d, a_, b_, c0, c1, don):
    """bastan sona incelen uzuv: cap c0 -> c1 (birim), yuvarlak uclu"""
    (x0, y0), (x1, y1) = don(a_), don(b_)
    n = 60
    for i in range(n + 1):
        t = i / n; rr = (c0 * (1 - t) + c1 * t) / 2 * S
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=255)


for ad, P in POZLAR.items():
    W, H = int(4.4 * S), int(2.2 * S)
    ox, oy = 2.0 * S, 1.15 * S
    don = lambda q: (ox + q[0] * S, oy - q[1] * S)
    m = Image.new("L", (W, H), 0); d = ImageDraw.Draw(m)
    # govde: kalcadan omuza kalinlasan kapsul (kalca 0,24, omuz 0,21)
    hx, hy = don((0, 0)); sx, sy = don(P["omuz"])
    n = 40
    for i in range(n + 1):
        t = i / n; r = (0.30 * (1 - t) + 0.25 * t) * S
        x, y = hx + (sx - hx) * t, hy + (sy - hy) * t
        d.ellipse((x - r, y - r, x + r, y + r), fill=255)
    for a_, b_, c0, c1 in P["uzuv"]:
        kapsul(d, a_, b_, c0, c1, don)
    (kx, ky), kr = P["kafa"]; kx, ky = don((kx, ky)); kr *= S
    g = 0.06 * S   # kapak 3: kafa govdeye yapisik -> referanstaki gibi ince boslukla ayri (bosluk kapakta beyaz kontura doner)
    d.ellipse((kx - kr - g, ky - kr - g, kx + kr + g, ky + kr + g), fill=0)
    d.ellipse((kx - kr, ky - kr, kx + kr, ky + kr), fill=255)
    b = m.getbbox(); m = m.crop(b); m = m.resize((m.width // 2, m.height // 2), Image.LANCZOS)
    im = Image.new("RGBA", m.size, (0, 0, 0, 0)); im.putalpha(m)
    im.save(os.path.join(a.klasor, "poz", ad + ".png"))
    print(ad, im.size)
