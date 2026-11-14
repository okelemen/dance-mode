"""HUMAN TETRIS 26 (poz-liste-25.py kopyasi; FREEZE yerine MIRROR ROUND: ortadaki 24 pozdan en asimetrik 12si, kontakta aynalanmis gosterilir).
HUMAN TETRIS 25: aday-olcu-25.json'dan 48 poz (farthest-point), zorluk siralamasi -> 4 tur x 6 duvar (poz-liste-24.py kopyasi).
Tur sirasi (TALIMATLAR §4 ozel turlar, 25'te FREEZE): ROUND 1 en kolay 12, FREEZE ROUND ikinci kolay 12 (duvar gectikten sonra 3 sn tutulur ->
dengede tutulabilen ayakta pozlar), ROUND 2 sonraki 12, FINAL en zor 12; son duvar BOSS WALL. Kontak: POZ-DUVARI/taslak/HUMAN-TETRIS-26-POZ-KONTAK.jpg"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.argv = ["x"]
BURA = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(BURA, "poz-sec-26.py"), encoding="utf-8").read().split("dosyalar = ")[0])   # maske(), iou(), boy(), yakin
d = json.load(open(os.path.join(BURA, "aday-olcu-26.json"), encoding="utf-8"))
YASAK2 = ("kneeling-camel", "haunted", "front-leg-reach", "kick-back-reach", "tombstone", "bat-heel", "cat-back", "inchworm", "camel", "standing-split", "down-dog", "kneel-one-leg", "low-lunge-twist", "tabletop-reach", "dead-bug", "lizard", "mummy",
          "lying-reach-up", "v-sit", "pistol-squat",
          "wide-leg-twist", "glute-bridge", "skeleton-superman",
          "pyramid-fold", "stork-fold", "tabletop-knee", "childs-pose", "locust", "coffin-cobra", "kneeling-lean", "vampire-skater", "child-arms", "fish-pose", "lying-",   # 26 kontak 1-3: bas asagi / yere yapisik / dusuyor okunan
          "clasp-fold", "wide-leg-fold", "happy-baby", "supine", "seated-knees-up", "crab-kick", "forearm-plank", "coffin-tabletop", "heron-seat", "toe-touch-twist", "legs-up", "humble-pigeon", "floor-swimmer", "cross-leg-fold", "scissor-legs")   # 25 kontak 1-3: bas asagi / sirt ustu / yere yapisik / kolay turda oturan   # 24 kontak 1-2: bas asagi / havada / yere yapisik okunan   # havada / ziplama / dusuyor okunan (kontak 1)
ad = [k for k in d if not any(w in k for w in YASAK2)]
# 24: karakterler ve maskot pozu acilardan kurar (karakter.py) -> aci tanimi olmayan maske (or. varlik/poz/triangle) elenir
import glob as _g
_POZ = {"varlik": "pozlar.json", "varlik-03": "pozlar-03.json", "varlik-04": "pozlar-04.json", "varlik-05": "pozlar-05.json"}
_TAN = {f: json.load(open(os.path.join(BURA, f), encoding="utf-8"))["pozlar"] for f in set(_POZ.values())}
ad = [k for k in ad if os.path.basename(k)[:-4] in _TAN[_POZ[k.split("/")[0]]]]
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
# 26: MIRROR ROUND (tur 3) — ortadaki 24 pozdan sol-sag farki en buyuk 12'si (ayna cevirince fark edilsin); R1 en kolay 12, FINAL en zor 12
asim = lambda k: 1 - (M[k] & M[k][:, ::-1]).sum() / max(1, (M[k] | M[k][:, ::-1]).sum())
orta = sec[12:36]; ayna_g = sorted(sorted(orta, key=asim)[-12:], key=zor)
GRUP = {1: sec[:12], 2: [k for k in orta if k not in ayna_g], 3: ayna_g, 4: sec[36:]}
print("MIRROR asimetri en dusuk", round(min(asim(k) for k in ayna_g), 3), "R2 en yuksek", round(max(asim(k) for k in GRUP[2]), 3))
for t in range(1, 5):
    grp = GRUP[t]
    for w in range(6):
        duvar.append({"tur": t, "p1": os.path.basename(grp[w * 2])[:-4], "p2": os.path.basename(grp[w * 2 + 1])[:-4]})
json.dump(sec, open(os.path.join(BURA, "poz-sec-26-sira.json"), "w"), indent=1)
json.dump(duvar, open(os.path.join(BURA, "duvar-listesi-26.json"), "w", encoding="utf-8"), indent=1)
# kontak
c, r, hh, ww = 12, 4, 190, 150
S = Image.new("RGB", (c * ww, r * (hh + 22)), "white"); dr = ImageDraw.Draw(S)
SIRA = [k for t in range(1, 5) for k in GRUP[t]]
TUR_AD = {1: "R1", 2: "R2", 3: "MIRROR", 4: "FINAL"}
for i, k in enumerate(SIRA):
    im = Image.open(os.path.join(BURA, k)).convert("RGBA"); bg = Image.new("RGBA", im.size, "white"); bg.alpha_composite(im)
    im = bg.convert("RGB")
    if i // 12 == 2: im = im.transpose(Image.FLIP_LEFT_RIGHT)      # MIRROR: oyuncunun gorecegi ters siluet
    b = Image.fromarray(255 - np.array(im.convert("L"))).getbbox()
    if b: im = im.crop(b)
    im.thumbnail((ww - 10, hh)); x, y = (i % c) * ww, (i // c) * (hh + 22)
    S.paste(im, (x + (ww - im.width) // 2, y + 22 + hh - im.height))
    dr.text((x + 3, y + 3), "%s W%d %s %s" % (TUR_AD[i // 12 + 1], i % 12 // 2 + 1, "P1" if i % 2 == 0 else "P2", os.path.basename(k)[:-4][:14]), fill="red")
S.save(r"C:\Users\eleme\OneDrive\Masaüstü\POZ-DUVARI\taslak\HUMAN-TETRIS-26-POZ-KONTAK.jpg", quality=90)
