"""TETRIS MODE 6. video (REF-057, 2 oyuncu) - 44 pozu OLCUMLE secer: aday maskeleri (varlik-06-aday/poz, Actions) eski 5 videonun
maskelerine ve secilenlere aynali IoU ile karsilastirilir.

    python poz-sec-06.py [--esik-eski 0.78] [--esik-ic 0.75]

Tur basina duvar REF-057'den: 7 / 7 / 8 -> 14 / 14 / 16 poz. Once elle tasarlananlar (el=True), sonra havuz; her grupta
eski-benzerligi en dusukten baslayarak. Duvar w: p1 = turun w. pozu, p2 = w+n. pozu (benzer aileler ayni duvarda yan yana
gelmez). Cikti pozlar-06.json, duvar-listesi-06.json, varlik-06/poz/ (motor buradan okur), varlik-06/iou-secim.txt.
"""
import argparse, glob, json, os, shutil
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--esik-eski", type=float, default=0.78)
ap.add_argument("--esik-ic", type=float, default=0.75)
A = ap.parse_args()
BURA = os.path.dirname(os.path.abspath(__file__))
N = 128
DUVAR_SAYI = {1: 7, 2: 7, 3: 8}
# siluette bas asagi / tam kopru gibi okunan tabanlar (5. video kontak dersi, TALIMATLAR §2 guvenlik)
YASAK = ("Standing Split", "Bridge", "Headstand", "Handstand")


def maske(yol):
    a = np.array(Image.open(yol).convert("RGBA"))[:, :, 3] > 40
    ys, xs = np.nonzero(a)
    a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h, w = a.shape; s = max(h, w)
    kare = np.zeros((s, s), bool); kare[s - h:, (s - w) // 2:(s - w) // 2 + w] = a
    return np.array(Image.fromarray(kare.astype(np.uint8) * 255).resize((N, N), Image.BILINEAR)) > 127


def iou(a, b):
    return max((a & b).sum() / max(1, (a | b).sum()), (a & b[:, ::-1]).sum() / max(1, (a | b[:, ::-1]).sum()))


eski = {}
for d in ("varlik/poz", "varlik-03/poz", "varlik-04/poz", "varlik-05/poz"):
    for f in glob.glob(os.path.join(BURA, d, "*.png")):
        eski[d + "/" + os.path.basename(f)] = maske(f)
n_eski = sum(len(glob.glob(os.path.join(BURA, d, "*.png"))) for d in ("varlik/poz", "varlik-03/poz", "varlik-04/poz", "varlik-05/poz"))
assert len(eski) == n_eski and n_eski > 400, (len(eski), n_eski)

aday = json.load(open(os.path.join(BURA, "pozlar-06-aday.json"), encoding="utf-8"))["pozlar"]
olcu, eksik = [], []
for ad, p in aday.items():
    yol = os.path.join(BURA, "varlik-06-aday/poz", ad + ".png")
    if not os.path.exists(yol):
        eksik.append(ad); continue
    if any(y in p["ad"] for y in YASAK):
        continue
    m = maske(yol)
    en, deg = max(((k, iou(m, v)) for k, v in eski.items()), key=lambda x: x[1])
    olcu.append((0 if p.get("el") else 1, deg, ad, p, p["tur"], yol, m, en))
assert not eksik or len(eksik) < len(aday) // 2, f"maske eksik: {len(eksik)}"

secilen = {1: [], 2: [], 3: []}
tum, rapor = [], []
for sira, deg, ad, p, tur, yol, m, en in sorted(olcu, key=lambda x: (x[0], x[1])):
    if len(secilen[tur]) >= 2 * DUVAR_SAYI[tur] or deg >= A.esik_eski:
        continue
    ic = max([iou(m, q[1]) for q in tum] or [0])
    if ic >= A.esik_ic:
        continue
    secilen[tur].append((ad, p, yol)); tum.append((ad, m))
    rapor.append(f"T{tur} {ad:50s} eski {deg:.2f} ({en}) ic {ic:.2f} {'EL' if sira == 0 else 'HAVUZ'}")
print({t: len(v) for t, v in secilen.items()}, "eksik maske:", len(eksik))
assert all(len(secilen[t]) == 2 * DUVAR_SAYI[t] for t in secilen), "yeterli farkli poz yok - aday havuzunu buyut"

pozlar, duvarlar = {}, []
hedef = os.path.join(BURA, "varlik-06", "poz"); os.makedirs(hedef, exist_ok=True)
for f in glob.glob(os.path.join(hedef, "*.png")):
    os.remove(f)
for tur in (1, 2, 3):
    L, n = secilen[tur], DUVAR_SAYI[tur]
    for ad, p, yol in L:
        pozlar[ad] = {k: v for k, v in p.items() if k not in ("tur", "el")}
        shutil.copy(yol, os.path.join(hedef, ad + ".png"))
    for w in range(n):
        duvarlar.append({"tur": tur, "p1": L[w][0], "p2": L[w + n][0]})
not_ = json.load(open(os.path.join(BURA, "pozlar.json"), encoding="utf-8"))["_not"].replace(
    "(REF-053)", "6. video (REF-057, 2 oyuncu, 5 dk; poz-sec-06.py olcumle secildi)")
json.dump({"_not": not_, "pozlar": pozlar}, open(os.path.join(BURA, "pozlar-06.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(duvarlar, open(os.path.join(BURA, "duvar-listesi-06.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(os.path.join(BURA, "varlik-06", "iou-secim.txt"), "w", encoding="utf-8").write(
    f"esik eski {A.esik_eski} / ic {A.esik_ic}, eski maske {len(eski)}\n" + "\n".join(rapor) + "\n")
print(f"{len(pozlar)} poz, {len(duvarlar)} duvar; en yuksek eski IoU {max(float(r.split('eski ')[1][:4]) for r in rapor):.2f}")
