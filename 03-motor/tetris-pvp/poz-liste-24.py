"""HUMAN TETRIS 24: aday-olcu-24.json'dan 48 poz (farthest-point), zorluk siralamasi -> 4 tur x 6 duvar.
Tur sirasi (TALIMATLAR §4 ozel turlar): ROUND 1 en kolay 12, SPEED ROUND ikinci kolay 12 (hizli duvarda ayakta pozlar), ROUND 2 sonraki 12,
FINAL en zor 12; son duvar BOSS WALL. Kontak: POZ-DUVARI/taslak/HUMAN-TETRIS-24-POZ-KONTAK.jpg"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.argv = ["x"]
BURA = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(BURA, "poz-sec-24.py"), encoding="utf-8").read().split("dosyalar = ")[0])   # maske(), iou(), boy(), yakin
d = json.load(open(os.path.join(BURA, "aday-olcu-24.json"), encoding="utf-8"))
YASAK2 = ("kneeling-camel", "haunted", "front-leg-reach", "kick-back-reach", "tombstone", "bat-heel", "cat-back", "inchworm", "camel", "standing-split", "down-dog", "kneel-one-leg", "low-lunge-twist", "tabletop-reach", "dead-bug", "lizard", "mummy",
          "lying-reach-up", "v-sit", "pistol-squat",
          "wide-leg-twist", "glute-bridge", "skeleton-superman")   # 24 kontak 1-2: bas asagi / havada / yere yapisik okunan   # havada / ziplama / dusuyor okunan (kontak 1)
ad = [k for k in d if not any(w in k for w in YASAK2)]
M = {k: maske(os.path.join(BURA, k)) for k in ad}
# farthest-point: ilk = en ayakta; sonra mevcut secilenlere en uzak (en dusuk max-IoU)
sec = [min(ad, key=lambda k: d[k]["gen"])]
mx = {k: iou(M[k], M[sec[0]]) for k in ad}
# 24 kontak 1: FINAL turu 12 yatay (plank / yatma) pozla doldu, telefonda okunmuyor -> yatik poz (boy/gen < 0,85) en cok 8
YATIK = lambda k: d[k]["boy"] / d[k]["gen"] < 0.85     # maske cerceveye sigdirildigi icin boy tek basina yaniltir -> en-boy orani
while len(sec) < 48:
    n_yat = sum(YATIK(q) for q in sec)
    k = min((k for k in ad if k not in sec and not (YATIK(k) and n_yat >= 8)), key=lambda k: mx[k]); sec.append(k)
    for q in ad: mx[q] = max(mx[q], iou(M[q], M[k]))
zor = lambda k: (1 - d[k]["boy"]) * 3 + d[k]["gen"] * 0.8 + (0.3 if any(w in k for w in ("kneel", "lunge", "split", "bridge", "plank", "squat", "twist")) else 0)
sec.sort(key=zor)
print("ic max IoU", round(max(iou(M[a], M[b]) for i, a in enumerate(sec) for b in sec[i + 1:]), 3))
duvar = []
DILIM = {1: 0, 2: 2, 3: 1, 4: 3}            # tur -> zorluk dilimi (3 = SPEED ROUND: ikinci en kolay dilim)
for t in range(1, 5):
    grp = sec[DILIM[t] * 12:(DILIM[t] + 1) * 12]
    for w in range(6):
        duvar.append({"tur": t, "p1": os.path.basename(grp[w * 2])[:-4], "p2": os.path.basename(grp[w * 2 + 1])[:-4]})
json.dump(sec, open(os.path.join(BURA, "poz-sec-24-sira.json"), "w"), indent=1)
json.dump(duvar, open(os.path.join(BURA, "duvar-listesi-24.json"), "w", encoding="utf-8"), indent=1)
# kontak
c, r, hh, ww = 12, 4, 190, 150
S = Image.new("RGB", (c * ww, r * (hh + 22)), "white"); dr = ImageDraw.Draw(S)
SIRA = [k for t in range(1, 5) for k in sec[DILIM[t] * 12:(DILIM[t] + 1) * 12]]
TUR_AD = {1: "R1", 2: "R2", 3: "SPEED", 4: "FINAL"}
for i, k in enumerate(SIRA):
    im = Image.open(os.path.join(BURA, k)).convert("RGBA"); bg = Image.new("RGBA", im.size, "white"); bg.alpha_composite(im)
    im = bg.convert("RGB"); b = Image.fromarray(255 - np.array(im.convert("L"))).getbbox()
    if b: im = im.crop(b)
    im.thumbnail((ww - 10, hh)); x, y = (i % c) * ww, (i // c) * (hh + 22)
    S.paste(im, (x + (ww - im.width) // 2, y + 22 + hh - im.height))
    dr.text((x + 3, y + 3), "%s W%d %s %s" % (TUR_AD[i // 12 + 1], i % 12 // 2 + 1, "P1" if i % 2 == 0 else "P2", os.path.basename(k)[:-4][:14]), fill="red")
S.save(r"C:\Users\eleme\OneDrive\Masaüstü\POZ-DUVARI\taslak\HUMAN-TETRIS-24-POZ-KONTAK.jpg", quality=90)
