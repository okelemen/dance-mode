"""HUMAN TETRIS 22: aday-olcu-22.json'dan 40 poz (en cesitli = farthest-point), zorluk siralamasi -> 4 tur x 5 duvar. Kontak: POZ-DUVARI/taslak/HUMAN-TETRIS-22-POZ-KONTAK.jpg"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.argv = ["x"]
BURA = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(BURA, "poz-sec-22.py"), encoding="utf-8").read().split("dosyalar = ")[0])   # maske(), iou(), boy(), yakin
d = json.load(open(os.path.join(BURA, "aday-olcu-22.json"), encoding="utf-8"))
YASAK2 = ("kneeling-camel", "haunted", "front-leg-reach", "kick-back-reach", "tombstone", "bat-heel", "cat-back", "inchworm", "camel", "standing-split", "down-dog", "kneel-one-leg", "low-lunge-twist", "tabletop-reach", "dead-bug", "lizard", "mummy")   # havada / ziplama / dusuyor okunan (kontak 1)
ad = [k for k in d if not any(w in k for w in YASAK2)]
M = {k: maske(os.path.join(BURA, k)) for k in ad}
# farthest-point: ilk = en ayakta; sonra mevcut secilenlere en uzak (en dusuk max-IoU)
sec = [min(ad, key=lambda k: d[k]["gen"])]
mx = {k: iou(M[k], M[sec[0]]) for k in ad}
while len(sec) < 40:
    k = min((k for k in ad if k not in sec), key=lambda k: mx[k]); sec.append(k)
    for q in ad: mx[q] = max(mx[q], iou(M[q], M[k]))
zor = lambda k: (1 - d[k]["boy"]) * 3 + d[k]["gen"] * 0.8 + (0.3 if any(w in k for w in ("kneel", "lunge", "split", "bridge", "plank", "squat", "twist")) else 0)
sec.sort(key=zor)
print("ic max IoU", round(max(iou(M[a], M[b]) for i, a in enumerate(sec) for b in sec[i + 1:]), 3))
duvar = []
for t in range(4):
    grp = sec[t * 10:(t + 1) * 10]
    for w in range(5):
        duvar.append({"tur": t + 1, "p1": os.path.basename(grp[w * 2])[:-4], "p2": os.path.basename(grp[w * 2 + 1])[:-4]})
json.dump(sec, open(os.path.join(BURA, "poz-sec-22-sira.json"), "w"), indent=1)
json.dump(duvar, open(os.path.join(BURA, "duvar-listesi-22.json"), "w", encoding="utf-8"), indent=1)
# kontak
c, r, hh, ww = 8, 5, 190, 150
S = Image.new("RGB", (c * ww, r * (hh + 22)), "white"); dr = ImageDraw.Draw(S)
for i, k in enumerate(sec):
    im = Image.open(os.path.join(BURA, k)).convert("RGBA"); bg = Image.new("RGBA", im.size, "white"); bg.alpha_composite(im)
    im = bg.convert("RGB"); b = Image.fromarray(255 - np.array(im.convert("L"))).getbbox()
    if b: im = im.crop(b)
    im.thumbnail((ww - 10, hh)); x, y = (i % c) * ww, (i // c) * (hh + 22)
    S.paste(im, (x + (ww - im.width) // 2, y + 22 + hh - im.height))
    dr.text((x + 3, y + 3), "T%d W%d %s %s" % (i // 10 + 1, i % 10 // 2 + 1, "P1" if i % 2 == 0 else "P2", os.path.basename(k)[:-4][:16]), fill="red")
S.save(r"C:\Users\eleme\OneDrive\Masaüstü\POZ-DUVARI\taslak\HUMAN-TETRIS-22-POZ-KONTAK.jpg", quality=90)
