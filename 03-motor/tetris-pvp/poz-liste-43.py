"""HUMAN TETRIS 43 (poz-liste-41.py kopyasi; 1P SOLO dinozor vadisi, 24 poz; SPEED yerine MIRROR ROUND (tur 3, 39 olcutu):
R1 sonrasi 18 pozdan sol-sag farki en buyuk 6si, kontakta aynalanmis.
HUMAN TETRIS 41 (poz-liste-40.py kopyasi; 1P SOLO col vahasi, 24 poz; BLIND yerine SPEED ROUND (tur 3, 36 olcutu):
R1 sonrasi 18 pozdan en hizli girilen 6si (iki ayak yerde, ayakta, dar) - son 4 duvar hizlanir.
HUMAN TETRIS 40 (poz-liste-39.py kopyasi; 1P SOLO donmus gol, 24 poz; MIRROR yerine BLIND ROUND (tur 3, 33/37 olcutu):
R1 sonrasi 18 pozdan en hizli girilen 6si (iki ayak yerde, ayakta, dar) - siluet son 1,5 sn belirir.
HUMAN TETRIS 39 (poz-liste-38.py kopyasi; 1P SOLO mercan resifi, 24 poz; FREEZE yerine MIRROR ROUND (tur 3, 30/34 olcutu):
R1 sonrasi 18 pozdan sol-sag farki en buyuk 6si, kontakta aynalanmis.
HUMAN TETRIS 38 (poz-liste-36.py kopyasi; 1P SOLO Christmas, 24 poz; SPEED yerine FREEZE ROUND (tur 3, 31 olcutu):
R1 sonrasi 18 pozdan denge puani en yuksek 6si - duvar gectikten sonra 3 sn kipirdamadan tutulur.
HUMAN TETRIS 36 (poz-liste-34.py kopyasi; 1P SOLO, 24 poz = 4 tur x 6 duvar x 1; MIRROR yerine SPEED ROUND (tur 3, 32 gibi):
R1 sonrasi 18 pozdan en kolay/hizli girilen 6si (iki ayak yerde, ayakta, dar); son 4 duvar hizlanir. Ortak formasyon yok.
HUMAN TETRIS 34 (poz-liste-32.py kopyasi; 3P CO-OP, 72 poz = 4 tur x 6 duvar x 3; SPEED yerine MIRROR ROUND (tur 3, 30 gibi):
R1 sonrasi 54 pozdan sol-sag farki en buyuk 18i, kontakta aynalanmis. CO-OP ortak formasyon: her duvarda en simetrik poz ortada (P2).
HUMAN TETRIS 32 (poz-liste-31.py kopyasi; 3 oyuncu, 72 poz = 4 tur x 6 duvar x 3; FREEZE yerine SPEED ROUND (tur 3, 29 gibi):
ortadaki 36 pozdan en kolay/hizli girilen 18i (iki ayak yerde, ayakta, dar) SPEED turunda; son 4 duvar hizlanir).
HUMAN TETRIS 31 (poz-liste-30.py kopyasi; MIRROR yerine FREEZE ROUND (tur 3): ortadaki 24 pozdan dengede en kolay tutulan 12'si
(genis taban = iki ayak yerde ve acik, dusuk agirlik merkezi) - duvar gectikten sonra 3 sn kipirdamadan tutulur; kontakta aynalama yok).
HUMAN TETRIS 30 (poz-liste-29.py kopyasi; SPEED yerine MIRROR ROUND (26 gibi): ortadaki 24 pozdan en asimetrik 12si, kontakta aynalanmis).
HUMAN TETRIS 29 (poz-liste-26.py kopyasi; MIRROR yerine SPEED ROUND: son 4 duvar hizlanir -> ortadaki 24 pozdan en kolay/hizli girilen 12si
SPEED turunda, kalan 12 ROUND 2'de). Asagisi 26'nin aciklamasi.
HUMAN TETRIS 26 (poz-liste-25.py kopyasi; FREEZE yerine MIRROR ROUND: ortadaki 24 pozdan en asimetrik 12si, kontakta aynalanmis gosterilir).
HUMAN TETRIS 25: aday-olcu-25.json'dan 48 poz (farthest-point), zorluk siralamasi -> 4 tur x 6 duvar (poz-liste-24.py kopyasi).
Tur sirasi (TALIMATLAR §4 ozel turlar, 25'te FREEZE): ROUND 1 en kolay 12, FREEZE ROUND ikinci kolay 12 (duvar gectikten sonra 3 sn tutulur ->
dengede tutulabilen ayakta pozlar), ROUND 2 sonraki 12, FINAL en zor 12; son duvar BOSS WALL. Kontak: POZ-DUVARI/taslak/HUMAN-TETRIS-29-POZ-KONTAK.jpg"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.argv = ["x"]
BURA = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(BURA, "poz-sec-43.py"), encoding="utf-8").read().split("dosyalar = ")[0])   # maske(), iou(), boy(), yakin
d = json.load(open(os.path.join(BURA, "aday-olcu-43.json"), encoding="utf-8"))
YASAK2 = ("hero-seat-lean-back", "kneeling-arm-swing-back", "ghoul-kneel-diagonal-reach", "half-kneel-v", "mermaid-pigeon", "kneeling-arm-sweep",   # 29 kontak 1: dusuyor / diz coken havada okunuyor / SPEED turunda yerde
          "kneeling-camel", "haunted", "front-leg-reach", "kick-back-reach", "tombstone", "bat-heel", "cat-back", "inchworm", "camel", "standing-split", "down-dog", "kneel-one-leg", "low-lunge-twist", "tabletop-reach", "dead-bug", "lizard", "mummy",
          "lying-reach-up", "v-sit", "pistol-squat",
          "wide-leg-twist", "glute-bridge", "skeleton-superman",
          "pyramid-fold", "stork-fold", "tabletop-knee", "childs-pose", "locust", "coffin-cobra", "kneeling-lean", "vampire-skater", "child-arms", "fish-pose", "lying-",   # 26 kontak 1-3: bas asagi / yere yapisik / dusuyor okunan
          "clasp-fold", "wide-leg-fold", "happy-baby", "supine", "seated-knees-up", "crab-kick", "forearm-plank", "coffin-tabletop", "heron-seat", "toe-touch-twist", "legs-up", "humble-pigeon", "floor-swimmer", "cross-leg-fold", "scissor-legs")   # 25 kontak 1-3: bas asagi / sirt ustu / yere yapisik / kolay turda oturan   # 24 kontak 1-2: bas asagi / havada / yere yapisik okunan   # havada / ziplama / dusuyor okunan (kontak 1)
YASAK2 = YASAK2 + ("nebula-lunge-arms-back-wings",)
YASAK2 = YASAK2 + ("coffin-point", "sakura-lunge-p", "truss-head-hip", "strobe-diag-fl")   # 33 kontak 1: havada / sicrama okunan   # 32 kontak 1: havada sicrama okunuyor
YASAK2 = YASAK2 + ("duel-warrior-t", "galaxy-v-wave", "nebula-dancer", "disco-lunge-ba", "cosmic-low-lun", "nebula-warrior", "bird-dog", "sakura-gate")   # + kontak 2: yerde / devrilen   # 31 kontak 1: havada / dusuyor / devriliyor okunan
YASAK2 = YASAK2 + ("duel-warrior-arms-spread",)   # 41 kontak 1: havada sicrama okunuyor
YASAK2 = YASAK2 + ("solar-low-head-tree",)   # 42 kontak 1: govde egik + diz havada, sicrama okunuyor
ad = [k for k in d if not any(w in k for w in YASAK2)]
# 30 kontak 1-2: genis aday havuzunda farthest-point oturan / diz coken / yatan / geriye devrilen pozlari secti (havada / dusuyor okunuyor)
# -> yalniz ayakta, yere iki ya da bir ayakla basan pozlar (TALIMATLAR §4 Pozlar: guvenli, yere basan); boy >= 0,62
YER = ("seated", "-sit", "sit-", "kneel", "plank", "child", "boat", "bridge", "recline", "crouch", "puppy", "straddle", "lying", "floor", "pike", "hands-ankles", "squat", "sprinter", "pigeon", "cross-leg", "lantern-cross", "bear", "crawl", "tabletop", "cobra", "cat-", "spell-cross", "lotus", "wide-se", "cosmic-gate", "skater", "deep-lung", "-seat")
ad = [k for k in ad if not any(w in k for w in YER) and d[k]["boy"] >= 0.62]
# 24: karakterler ve maskot pozu acilardan kurar (karakter.py) -> aci tanimi olmayan maske (or. varlik/poz/triangle) elenir
import glob as _g
_POZ = {"varlik": "pozlar.json", "varlik-03": "pozlar-03.json", "varlik-04": "pozlar-04.json", "varlik-05": "pozlar-05.json",
        "varlik-05-aday": "pozlar-05-aday.json", "varlik-06-aday": "pozlar-06-aday.json", "varlik-08-aday": "pozlar-08-aday.json",
        "varlik-09-aday": "pozlar-09-aday.json", "varlik-10-aday": "pozlar-10-aday.json", "varlik-12-aday": "pozlar-12-aday.json",
        "varlik-14-aday": "pozlar-14-aday.json", "varlik-16-aday-2": "pozlar-16-aday.json", "varlik-17-aday": "pozlar-17-aday.json"}
_TAN = {f: json.load(open(os.path.join(BURA, f), encoding="utf-8"))["pozlar"] for f in set(_POZ.values())}
ad = [k for k in ad if os.path.basename(k)[:-4] in _TAN[_POZ[k.split("/")[0]]]]
M = {k: maske(os.path.join(BURA, k)) for k in ad}
# farthest-point: ilk = en ayakta; sonra mevcut secilenlere en uzak (en dusuk max-IoU)
sec = [min(ad, key=lambda k: d[k]["gen"])]
mx = {k: iou(M[k], M[sec[0]]) for k in ad}
# 24 kontak 1: FINAL turu 12 yatay (plank / yatma) pozla doldu, telefonda okunmuyor -> yatik poz (boy/gen < 0,85) en cok 8
YATIK = lambda k: d[k]["boy"] / d[k]["gen"] < 0.85     # maske cerceveye sigdirildigi icin boy tek basina yaniltir -> en-boy orani
while len(sec) < 24:
    n_yat = sum(YATIK(q) for q in sec)
    k = min((k for k in ad if k not in sec and not (YATIK(k) and n_yat >= 4)), key=lambda k: mx[k]); sec.append(k)
    for q in ad: mx[q] = max(mx[q], iou(M[q], M[k]))
zor = lambda k: (1 - d[k]["boy"]) * 3 + d[k]["gen"] * 0.8 + (0.3 if any(w in k for w in ("kneel", "lunge", "split", "bridge", "plank", "squat", "twist")) else 0)
sec.sort(key=zor)
print("ic max IoU", round(max(iou(M[a], M[b]) for i, a in enumerate(sec) for b in sec[i + 1:]), 3))
duvar = []
# 31: FREEZE ROUND (tur 3) - ortadaki 24 pozdan denge puani en yuksek 12'si: tabandaki temas genisligi (iki ayak acik) + alcak agirlik merkezi
def denge(k):
    m = M[k]; ys, xs = np.nonzero(m); alt = m[ys.max() - 3:ys.max() + 1].any(0)
    tx = np.nonzero(alt)[0]; taban = (tx.max() - tx.min()) / m.shape[1] if len(tx) else 0
    ayak = int((np.diff(np.concatenate([[0], alt.astype(int), [0]])) == 1).sum())    # tabandaki ayri temas sayisi
    agm = (ys.mean() - ys.min()) / max(1, ys.max() - ys.min())                       # 1 = agirlik altta
    return taban + 0.3 * agm + (0.2 if ayak >= 2 else 0)
def iki_ayak(k):
    m = M[k]; ys, xs = np.nonzero(m); alt = m[ys.max() - 3:ys.max() + 1].any(0)
    return int((np.diff(np.concatenate([[0], alt.astype(int), [0]])) == 1).sum()) >= 2
# 36: SPEED ROUND (tur 3) - R1 sonrasi 18 pozdan en kolay/hizli girilen 6si (32 olcutu)
# 38: FREEZE ROUND (tur 3) - R1 sonrasi 18 pozdan denge puani en yuksek 6si (31 olcutu), iki ayak yerde sart
# 39: MIRROR ROUND (tur 3) - R1 sonrasi 18 pozdan sol-sag farki en buyuk 6si (30/34 olcutu)
asim = lambda k: 1 - (M[k] & M[k][:, ::-1]).sum() / max(1, (M[k] | M[k][:, ::-1]).sum())
# 41: SPEED ROUND (tur 3) - R1 sonrasi 18 pozdan en hizli girilen 6si (36 olcutu)
hiz = lambda k: d[k]["boy"] * 2 - d[k]["gen"] + (0.3 if iki_ayak(k) else 0)
# 43: MIRROR ROUND (tur 3) - R1 sonrasi 18 pozdan sol-sag farki en buyuk 6si (39 olcutu)
spd = sorted(sorted(sec[6:], key=asim)[-6:], key=zor)
kalan = [k for k in sec[6:] if k not in spd]
GRUP = {1: sec[:6], 2: kalan[:6], 3: spd, 4: kalan[6:]}
assert len(GRUP[4]) == 6, len(GRUP[4])
print("MIRROR asimetri en dusuk", round(min(asim(k) for k in spd), 3), "R2 en yuksek", round(max(asim(k) for k in GRUP[2]), 3), "FINAL en yuksek", round(max(asim(k) for k in GRUP[4]), 3))
print("iki ayak", {t: sum(iki_ayak(k) for k in GRUP[t]) for t in GRUP})
for t in range(1, 5):
    for w in range(6):
        duvar.append({"tur": t, "p1": os.path.basename(GRUP[t][w])[:-4]})
json.dump(sec, open(os.path.join(BURA, "poz-sec-43-sira.json"), "w"), indent=1)
json.dump(duvar, open(os.path.join(BURA, "duvar-listesi-43.json"), "w", encoding="utf-8"), indent=1)
# kontak (6 x 4, buyuk)
c, r, hh, ww = 6, 4, 300, 230
S = Image.new("RGB", (c * ww, r * (hh + 30)), "white"); dr = ImageDraw.Draw(S)
SIRA = [k for t in range(1, 5) for k in GRUP[t]]
TUR_AD = {1: "R1", 2: "R2", 3: "MIRROR", 4: "FINAL"}
F = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 18)
for i, k in enumerate(SIRA):
    im = Image.open(os.path.join(BURA, k)).convert("RGBA"); bg = Image.new("RGBA", im.size, "white"); bg.alpha_composite(im)
    im = bg.convert("RGB")
    if i // 6 == 2: im = im.transpose(Image.FLIP_LEFT_RIGHT)      # MIRROR: oyuncunun gorecegi ters siluet
    b = Image.fromarray(255 - np.array(im.convert("L"))).getbbox()
    if b: im = im.crop(b)
    im.thumbnail((ww - 16, hh)); x, y = (i % c) * ww, (i // c) * (hh + 30)
    S.paste(im, (x + (ww - im.width) // 2, y + 30 + hh - im.height))
    dr.text((x + 4, y + 4), "%d %s W%d%s" % (i + 1, TUR_AD[i // 6 + 1], i % 6 + 1, " BOSS" if i == 23 else ""), fill="red", font=F)
S.save("C:/Users/eleme/OneDrive/Masaüstü/POZ-DUVARI/taslak/HUMAN-TETRIS-43-POZ-KONTAK.jpg", quality=90)
for i, k in enumerate(SIRA): print(i + 1, TUR_AD[i // 6 + 1], k, "boy %.2f gen %.2f yakin %.2f" % (d[k]["boy"], d[k]["gen"], d[k]["yakin_iou"]))
