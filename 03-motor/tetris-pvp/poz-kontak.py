"""Poz kontak sayfasi - Actions'tan inen siluet maskelerini tur tur, P1/P2 renkli panellerde dizer (yerel montaj, render degil).

    python poz-kontak.py --maske <poz klasoru> --duvar duvar-listesi-03.json --pozlar pozlar-03.json \
        --renk1 "#A64DFF" --renk2 "#F5FF3D" --cikti <klasor> --ad TETRIS-MODE-03-POZLAR
"""
import argparse, json, os
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
for a in ("--maske", "--duvar", "--pozlar", "--renk1", "--renk2", "--cikti", "--ad"):
    ap.add_argument(a, required=True)
ap.add_argument("--renk3")            # 5. video (REF-056): 3 oyuncu -> duvarda p3 de var
A = ap.parse_args()
duvar = json.load(open(A.duvar, encoding="utf-8"))
pozlar = json.load(open(A.pozlar, encoding="utf-8"))["pozlar"]
hx = lambda h: tuple(int(h.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
R1, R2 = hx(A.renk1), hx(A.renk2)
OYUNCU = (("p1", R1), ("p2", R2)) + ((("p3", hx(A.renk3)),) if A.renk3 else ())
NP = len(OYUNCU)
try:
    F = ImageFont.truetype("arialbd.ttf", 22); FB = ImageFont.truetype("arialbd.ttf", 34)
except OSError:
    F = FB = ImageFont.load_default()

PW, PH, BOS = 300, 247, 12          # panel (maske 900x740 oraninda)
SUT = 3                             # satirda 3 duvar (her duvar 2 panel)
os.makedirs(A.cikti, exist_ok=True)
for tur in sorted({d["tur"] for d in duvar}):
    liste = [(i + 1, d) for i, d in enumerate(duvar) if d["tur"] == tur]
    sat = (len(liste) + SUT - 1) // SUT
    W = SUT * (NP * PW + (NP + 1) * BOS) + BOS
    H = 60 + sat * (PH + 40 + BOS)
    im = Image.new("RGB", (W, H), (14, 16, 34)); dr = ImageDraw.Draw(im)
    dr.text((BOS, 12), f"ROUND {tur}", font=FB, fill=(255, 255, 255))
    for j, (no, d) in enumerate(liste):
        x0 = BOS + (j % SUT) * (NP * PW + (NP + 1) * BOS); y0 = 60 + (j // SUT) * (PH + 40 + BOS)
        for k, (anah, renk) in enumerate(OYUNCU):
            x = x0 + k * (PW + BOS)
            pan = Image.new("RGB", (PW, PH), renk)
            m = Image.open(os.path.join(A.maske, d[anah] + ".png")).convert("RGBA").resize((PW, PH), Image.LANCZOS)
            pan.paste((0, 0, 0), (0, 0), m.split()[3])
            im.paste(pan, (x, y0))
            dr.text((x + 4, y0 + PH + 6), f"{no}{'abc'[k]} {pozlar[d[anah]]['ad']}", font=F, fill=renk)
    yol = os.path.join(A.cikti, f"{A.ad}-TUR{tur}.jpg")
    im.save(yol, quality=88); print(yol, im.size)
