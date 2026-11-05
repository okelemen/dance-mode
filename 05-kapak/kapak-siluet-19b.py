"""HUMAN TETRIS 19 kapak silueti - OLCULU insan silueti (bird-dog), kendi cizimimiz (5 Kas 2026).

Kullanici: "vucut hatlari insan gibi degil", "hala cok kaba", X Bot "uzayli gibi". kapak-siluet-19.py tahmini profillerdi;
bu surum REF-070 siluetinin KALINLIKLARINI ve eksen hatlarini olcer (1 birim = 254 px, 26 kesit; kapak 9 olcum tablosu
VIDEO-GECMISI'nde) ve kendi zincirimizi o olculere oturtur. Cizgi kopya degil: yuvarlak dolgu zinciri + yumusatma.

    python kapak-siluet-19b.py --klasor ../03-motor/tetris-pvp/varlik-19-olcu
"""
import argparse, json, math, os
from PIL import Image, ImageDraw, ImageFilter

p = argparse.ArgumentParser(); p.add_argument("--klasor", required=True); a = p.parse_args()
os.makedirs(os.path.join(a.klasor, "poz"), exist_ok=True)
S = 600

# (x, y, cap) - olculen eksen + kalinlik
ZINCIR = {
    "geri_bacak": [(-1.66, 0.43, 0.03), (-1.50, 0.43, 0.09), (-1.30, 0.41, 0.10), (-1.12, 0.36, 0.13), (-0.91, 0.26, 0.15),
                   (-0.75, 0.20, 0.175), (-0.59, 0.12, 0.20), (-0.43, 0.03, 0.20), (-0.28, -0.02, 0.25), (-0.12, -0.07, 0.29)],
    # taslak 1: karin-kalca birlesimi incelmisti -> olculen 0,45 (x 0,04-0,20, merkez -0,14)
    "govde": [(-0.12, -0.07, 0.30), (0.02, -0.08, 0.32), (0.14, -0.13, 0.44), (0.26, -0.14, 0.44), (0.40, -0.12, 0.34), (0.51, -0.10, 0.33),
              (0.67, -0.03, 0.37), (0.83, 0.05, 0.37), (0.95, 0.10, 0.30)],
    "diz_uyluk": [(0.12, -0.12, 0.30), (0.12, -0.37, 0.29), (0.12, -0.61, 0.25), (0.10, -0.79, 0.22)],
    "baldir": [(0.08, -0.84, 0.14), (-0.20, -0.85, 0.13), (-0.43, -0.86, 0.115), (-0.67, -0.87, 0.10), (-0.80, -0.88, 0.07), (-0.95, -0.87, 0.03)],
    "destek_kol": [(0.90, 0.02, 0.16), (0.90, -0.30, 0.13), (0.91, -0.53, 0.106), (0.91, -0.77, 0.08), (0.92, -0.86, 0.08)],
    "el": [(0.92, -0.88, 0.07), (1.04, -0.89, 0.05), (1.10, -0.895, 0.025)],
    "ileri_kol": [(0.95, 0.12, 0.16), (1.30, 0.106, 0.118), (1.46, 0.116, 0.098), (1.61, 0.128, 0.083), (1.77, 0.136, 0.075),
                  (1.93, 0.156, 0.043), (1.98, 0.16, 0.02)],
    "boyun": [(0.94, 0.12, 0.20), (1.00, 0.26, 0.12)],
}
KAFA = ((1.10, 0.50), 0.205)

W, H = int(4.2 * S), int(2.0 * S); ox, oy = 1.85 * S, 0.85 * S
don = lambda q: (ox + q[0] * S, oy - q[1] * S)
m = Image.new("L", (W, H), 0); d = ImageDraw.Draw(m)
for z in ZINCIR.values():
    for (x0, y0, c0), (x1, y1, c1) in zip(z, z[1:]):
        n = max(10, int(math.hypot(x1 - x0, y1 - y0) * 150))
        for i in range(n + 1):   # +0,02 pay: yumusatma ince uclari kemiriyor
            t = i / n; x, y = don((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t)); r = (c0 + (c1 - c0) * t + 0.02) / 2 * S
            d.ellipse((x - r, y - r, x + r, y + r), fill=255)
m = m.filter(ImageFilter.GaussianBlur(0.03 * S)).point(lambda v: 255 if v > 128 else 0)   # gecisler yumusak
(kx, ky), kr = KAFA; kx, ky = don((kx, ky)); kr *= S; g = 0.03 * S
d = ImageDraw.Draw(m)
d.ellipse((kx - kr - g, ky - kr - g, kx + kr + g, ky + kr + g), fill=0)
d.ellipse((kx - kr, ky - kr, kx + kr, ky + kr), fill=255)
m = m.filter(ImageFilter.GaussianBlur(1.5))
b = m.getbbox(); m = m.crop(b); m = m.resize((m.width // 3, m.height // 3), Image.LANCZOS)
im = Image.new("RGBA", m.size, (0, 0, 0, 0)); im.putalpha(m)
im.save(os.path.join(a.klasor, "poz", "olcu-bird-dog.png"))
json.dump({"poz": {"olcu-bird-dog": {"kafa_px": [round((kx - b[0]) / 3, 1), round((ky - b[1]) / 3, 1), round(kr / 3, 1)]}}},
          open(os.path.join(a.klasor, "yerlesim.json"), "w", encoding="utf-8"), indent=1)
print(im.size)
