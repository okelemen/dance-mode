"""2 kisilik CO-OP poz kontak sayfasi (7. video, REF-058) - Actions'tan inen grup/<ad>.png maskelerini tek sayfada,
REF-058 duvar paneli gibi renk gecisli zeminde (camgobegi->mavi, sari->yesil) dizer (yerel montaj, render degil).

    python ikili-kontak.py --varlik varlik-07-poz --duvar duvar-listesi-07.json --gruplar gruplar-07.json --cikti <jpg>
"""
import argparse, json, os
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
for a in ("--varlik", "--duvar", "--gruplar", "--cikti"):
    ap.add_argument(a, required=True)
ap.add_argument("--etiket", default="", help="grup basliklari virgulle (11. video: tur yok, poz ailesi)")
A = ap.parse_args()
duvar = json.load(open(A.duvar, encoding="utf-8"))
gruplar = json.load(open(A.gruplar, encoding="utf-8"))["gruplar"]
yer = json.load(open(os.path.join(A.varlik, "yerlesim.json"), encoding="utf-8")).get("grup", {})
ZEMIN = [((40, 240, 220), (40, 120, 255)), ((250, 240, 60), (120, 240, 60))]
TUR = {1: "ROUND 1", 2: "ROUND 2", 3: "ROUND 3"}
if A.etiket:
    TUR = dict(zip((1, 2, 3), A.etiket.split(",")))
try:
    F = ImageFont.truetype("arialbd.ttf", 20); FB = ImageFont.truetype("arialbd.ttf", 30)
except OSError:
    F = FB = ImageFont.load_default()

PW, PH, BOS, SUT = 400, 225, 10, 4
sat = sum((sum(d["tur"] == t for d in duvar) + SUT - 1) // SUT for t in TUR)
W = SUT * (PW + BOS) + BOS
im = Image.new("RGB", (W, 3 * 50 + sat * (PH + 34 + BOS)), (30, 6, 34)); dr = ImageDraw.Draw(im)
y = 10
for t in TUR:
    liste = [(i + 1, d) for i, d in enumerate(duvar) if d["tur"] == t]
    dr.text((BOS, y), TUR[t], font=FB, fill=(255, 120, 220)); y += 40
    for j, (no, d) in enumerate(liste):
        x = BOS + (j % SUT) * (PW + BOS); y0 = y + (j // SUT) * (PH + 34 + BOS)
        c1, c2 = ZEMIN[no % 2]
        g = Image.linear_gradient("L").rotate(-60, expand=True).resize((PW, PH))
        p = Image.composite(Image.new("RGB", (PW, PH), c2), Image.new("RGB", (PW, PH), c1), g)
        m = Image.open(os.path.join(A.varlik, "grup", d["grup"] + ".png")).convert("RGBA").resize((PW, PH), Image.LANCZOS)
        p.paste((12, 4, 20), (0, 0), m.split()[3])
        im.paste(p, (x, y0))
        dz = max([abs(q["dz"]) for q in yer.get(d["grup"], {}).get("temas", []) if q["tip"] != "yan"] or [0])
        renk = (255, 110, 110) if dz > 0.25 else (240, 230, 255)
        dr.text((x + 4, y0 + PH + 6), f"{no}. {gruplar[d['grup']]['ad']}" + (f"  (dz {dz:.2f})" if dz > 0.25 else ""),
                font=F, fill=renk)
    y += ((len(liste) + SUT - 1) // SUT) * (PH + 34 + BOS)
im.save(A.cikti, quality=88)
print(A.cikti, im.size)
