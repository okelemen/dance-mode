"""3 kisilik grup poz kontak sayfasi (5. video, REF-056) - Actions'tan inen grup maskelerini tur tur, renk gecisli
panellerde dizer (yerel montaj, render degil).

    python grup-kontak.py --varlik varlik-05 --duvar duvar-listesi-05.json --gruplar gruplar-05.json --cikti <klasor> --ad TETRIS-MODE-05-POZLAR
"""
import argparse, json, os
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
for a in ("--varlik", "--duvar", "--gruplar", "--cikti", "--ad"):
    ap.add_argument(a, required=True)
A = ap.parse_args()
duvar = json.load(open(A.duvar, encoding="utf-8"))
gruplar = json.load(open(A.gruplar, encoding="utf-8"))["gruplar"]
yer = json.load(open(os.path.join(A.varlik, "yerlesim.json"), encoding="utf-8")).get("grup", {})
PANELLER = ["kabak", "zehir", "gece"]
pan = {}
for p in PANELLER:
    f = os.path.join(A.varlik, f"panel-{p}.png")
    pan[p] = Image.open(f).convert("RGB") if os.path.exists(f) else None
YEDEK = {"kabak": ((255, 176, 42), (200, 16, 46)), "zehir": ((125, 255, 74), (244, 236, 210)), "gece": ((122, 43, 214), (255, 233, 176))}
try:
    F = ImageFont.truetype("arialbd.ttf", 22); FB = ImageFont.truetype("arialbd.ttf", 34)
except OSError:
    F = FB = ImageFont.load_default()

PW, PH, BOS, SUT = 480, 270, 14, 3
os.makedirs(A.cikti, exist_ok=True)
for tur in sorted({d["tur"] for d in duvar}):
    liste = [(i + 1, d) for i, d in enumerate(duvar) if d["tur"] == tur]
    sat = (len(liste) + SUT - 1) // SUT
    W = SUT * (PW + BOS) + BOS
    H = 60 + sat * (PH + 40 + BOS)
    im = Image.new("RGB", (W, H), (14, 6, 28)); dr = ImageDraw.Draw(im)
    dr.text((BOS, 12), f"ROUND {tur}", font=FB, fill=(255, 220, 160))
    for j, (no, d) in enumerate(liste):
        x = BOS + (j % SUT) * (PW + BOS); y0 = 60 + (j // SUT) * (PH + 40 + BOS)
        tip = PANELLER[(no - 1) % 3]
        if pan[tip] is not None:
            p = pan[tip].resize((PW, PH), Image.LANCZOS)
        else:
            c1, c2 = YEDEK[tip]; p = Image.linear_gradient("L").resize((PW, PH)).rotate(45)
            p = Image.composite(Image.new("RGB", (PW, PH), c2), Image.new("RGB", (PW, PH), c1), p)
        m = Image.open(os.path.join(A.varlik, "grup", d["grup"] + ".png")).convert("RGBA").resize((PW, PH), Image.LANCZOS)
        p.paste((10, 4, 22), (0, 0), m.split()[3])
        im.paste(p, (x, y0))
        dz = max([abs(t["dz"]) for t in yer.get(d["grup"], {}).get("temas", [])] or [0])
        renk = (255, 120, 120) if dz > 0.25 else (235, 225, 255)
        dr.text((x + 4, y0 + PH + 6), f"{no}. {gruplar[d['grup']]['ad']}" + (f"  (dz {dz:.2f})" if dz > 0.25 else ""), font=F, fill=renk)
    yol = os.path.join(A.cikti, f"{A.ad}-TUR{tur}.jpg")
    im.save(yol, quality=88); print(yol, im.size)
