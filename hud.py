"""KESIM SAYACI - yazi katmani (CUTS / CUBES / sure / abone cagrisi).

python hud.py --plan plan-avokado.json --giris kareler --cikis hud [--font yol]
Kare adlari kare_NNNN.png (1 tabanli). Yazilar kalin koyu konturlu: zemin ne olursa olsun
dolgu <-> kontur kontrasti yuksek (md. 28).
"""
import argparse
import glob
import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument("--plan", required=True)
ap.add_argument("--giris", required=True)
ap.add_argument("--cikis", required=True)
ap.add_argument("--font", default="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
a = ap.parse_args()

P = json.load(open(a.plan, encoding="utf-8"))
FPS = P["fps"]
os.makedirs(a.cikis, exist_ok=True)


def font(px):
    return ImageFont.truetype(a.font, px)


F_SAYI, F_ETIKET, F_SURE, F_KUP, F_CTA, F_CTA2 = font(150), font(56), font(46), font(104), font(50), font(38)
BEYAZ, ALTIN, KONTUR = (244, 244, 244), (246, 197, 64), (22, 22, 22)


def yaz(d, xy, metin, f, dolgu, kontur=8, hiza="mm"):
    d.text(xy, metin, font=f, fill=dolgu, anchor=hiza, stroke_width=kontur, stroke_fill=KONTUR)


def kup_metni(n):
    if n >= 10000:
        return "≈ " + f"{int(round(n, -3)):,}"
    return f"{n:,}"


def hap(d, merkez, metin, f, zemin, yazi, pad=(34, 16)):
    x, y = merkez
    l, t, r, b = d.textbbox((0, 0), metin, font=f)
    w, h = r - l + 2 * pad[0], b - t + 2 * pad[1]
    d.rounded_rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], radius=h / 2, fill=zemin,
                        outline=(255, 255, 255), width=4)
    d.text((x, y), metin, font=f, fill=yazi, anchor="mm")
    return w


CTA = [(14.6, 18.0), (44.0, 47.4)]

for yol in sorted(glob.glob(os.path.join(a.giris, "kare_*.png"))):
    f = int(os.path.basename(yol)[5:9])
    t = (f - 1) / FPS
    im = Image.open(yol).convert("RGB")
    if im.size != (1080, 1920):
        im = im.resize((1080, 1920), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    tur = next((r for r in P["turlar"] if r["bas"] <= t < r["son"]), P["turlar"][-1])
    kesim = sum(1 for k in tur["kesimler"] if k[0] <= t + 1e-6)
    # CUBES: kupler ayrilmaya baslayinca hedefe sayarak cikar (1,1 sn, yavaslayarak)
    s_ = (t - tur["kes_son"] - 0.05) / 1.1
    if s_ <= 0:
        kup = 0
        son_mu = False
    else:
        s_ = min(1.0, s_)
        kup = int(round(tur["kup"] * (1 - (1 - s_) ** 3)))
        son_mu = s_ >= 1.0
    yaz(d, (540, 250), str(kesim), F_SAYI, BEYAZ, 9)
    yaz(d, (540, 372), "CUTS", F_ETIKET, ALTIN, 6)
    yaz(d, (540, 1545), kup_metni(kup) if son_mu else f"{kup:,}", F_KUP, BEYAZ, 8)
    yaz(d, (540, 1650), "CUBES", F_ETIKET, ALTIN, 6)
    for c0, c1 in CTA:
        if c0 <= t < c1:
            hap(d, (540, 1765), "SUBSCRIBE", F_CTA, (214, 32, 26), (255, 255, 255))
            ws = [d.textbbox((0, 0), m, font=F_CTA2)[2] + 60 for m in ("LIKE", "COMMENT", "SHARE")]
            top = sum(ws) + 2 * 22
            x = 540 - top / 2
            for m, w in zip(("LIKE", "COMMENT", "SHARE"), ws):
                hap(d, (x + w / 2, 1858), m, F_CTA2, (58, 84, 30), (255, 255, 255), pad=(30, 12))
                x += w + 22
    im.save(os.path.join(a.cikis, os.path.basename(yol)))
    print("HUD", f, flush=True)
