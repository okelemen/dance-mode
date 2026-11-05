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
# kapak 1: uzuvlar ince (cop adam); kapak 2: kutuk gibi kalin; kapak 4 (kullanici: "siluette sorun var, daha estetik olabilir"):
# oranlar REF-070 kapagindan izgarayla OLCULDU (1 birim = kalca-omuz 254 px): kalca yerden 0,89; omuz (0,98, +0,18); kafa (1,10, 0,47) r 0,20;
# ileri kol yatay ucu (1,95, 0,16); destek kolu dikey (0,91, zemin); diz kalcanin altinda, baldir geride zeminde (-0,91);
# geri bacak hafif yukari (-1,38, 0,45), uyluk kalin dizden sonra incelir; govde arkada dolgun damla (cap 0,40 -> 0,30), uzuvlar uca incelir.
# uzuv: (bas, son, cap_bas, cap_son)
Z = -0.89
POZLAR = {
    "pikto-bird-dog": {
        "kalca": (-0.10, 0.0), "omuz": (0.98, 0.18), "govde": (0.42, 0.30), "kafa": ((1.10, 0.47), 0.20),
        "uzuv": [((0.98, 0.18), (1.95, 0.16), 0.14, 0.08),        # ileri uzanan kol
                 ((0.92, 0.10), (0.91, Z), 0.17, 0.14),           # destek kolu (yere)
                 ((0.0, -0.05), (0.0, Z + 0.04), 0.30, 0.22),      # diz cokulen bacak: uyluk
                 ((0.0, Z + 0.04), (-0.91, Z + 0.02), 0.20, 0.11), # baldir (yerde, geride)
                 ((-0.05, 0.05), (-0.71, 0.25), 0.34, 0.22), ((-0.71, 0.25), (-1.38, 0.45), 0.22, 0.07)],      # geri ve hafif yukari uzanan bacak
    },
    "pikto-bird-dog-high": {
        "kalca": (-0.10, 0.0), "omuz": (0.98, 0.22), "govde": (0.42, 0.30), "kafa": ((1.11, 0.52), 0.20),
        "uzuv": [((0.98, 0.22), (1.90, 0.42), 0.14, 0.08),
                 ((0.92, 0.14), (0.91, Z), 0.17, 0.14),
                 ((0.0, -0.05), (0.0, Z + 0.04), 0.30, 0.22),
                 ((0.0, Z + 0.04), (-0.91, Z + 0.02), 0.20, 0.11),
                 ((-0.05, 0.05), (-0.68, 0.38), 0.34, 0.22), ((-0.68, 0.38), (-1.3, 0.72), 0.22, 0.07)],
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
    W, H = int(3.6 * S), int(2.4 * S)
    ox, oy = 1.5 * S, 1.3 * S
    don = lambda q: (ox + q[0] * S, oy - q[1] * S)
    m = Image.new("L", (W, H), 0); d = ImageDraw.Draw(m)
    # govde: kalcadan omuza kalinlasan kapsul (kalca 0,24, omuz 0,21)
    hx, hy = don(P["kalca"]); sx, sy = don(P["omuz"])
    n = 40
    for i in range(n + 1):
        t = i / n; r = (P["govde"][0] * (1 - t) + P["govde"][1] * t) / 2 * S
        x, y = hx + (sx - hx) * t, hy + (sy - hy) * t
        d.ellipse((x - r, y - r, x + r, y + r), fill=255)
    for a_, b_, c0, c1 in P["uzuv"]:
        kapsul(d, a_, b_, c0, c1, don)
    # kapak 5: diz cokulen ayagin ucu ve destek eli zeminde kisa cikinti
    kapsul(d, (-0.91, Z + 0.02), (-1.02, Z + 0.10), 0.11, 0.07, don)
    kapsul(d, (0.91, Z + 0.02), (1.03, Z + 0.02), 0.13, 0.10, don)
    (kx, ky), kr = P["kafa"]; kx, ky = don((kx, ky)); kr *= S
    g = 0.035 * S   # kapak 3: kafa govdeye yapisik -> referanstaki gibi ince boslukla ayri (bosluk kapakta beyaz kontura doner)
    d.ellipse((kx - kr - g, ky - kr - g, kx + kr + g, ky + kr + g), fill=0)
    d.ellipse((kx - kr, ky - kr, kx + kr, ky + kr), fill=255)
    b = m.getbbox(); m = m.crop(b); m = m.resize((m.width // 2, m.height // 2), Image.LANCZOS)
    im = Image.new("RGBA", m.size, (0, 0, 0, 0)); im.putalpha(m)
    im.save(os.path.join(a.klasor, "poz", ad + ".png"))
    print(ad, im.size)
