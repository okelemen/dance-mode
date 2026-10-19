"""TETRIS MODE 5. video - 135 pozu OLCUMLE secer (goz karari yerine): ilk liste (pozlar-05-ilk.json) + aday havuzu
(pozlar-05-aday.json) maskeleri, eski videolarin maskelerine ve secilenlere aynali IoU ile karsilastirilir.

    python poz-sec-05.py [--esik-eski 0.78] [--esik-ic 0.75]

Kural: eski maskeye IoU >= esik-eski ya da videoda secilmis bir poza IoU >= esik-ic olan poz alinmaz. Once ilk listedeki
(elle tasarlanmis) pozlar, sonra adaylar eski-benzerligi en dusukten baslayarak. Her turdan 45 -> pozlar-05.json,
duvar-listesi-05.json (duvar w: turun w, w+15, w+30. pozlari -> benzer aileler ayni duvarda yan yana gelmez), rapor iou-secim.txt.
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
for d in ("varlik/poz", "varlik-03/poz", "varlik-04/poz"):
    for f in glob.glob(os.path.join(BURA, d, "*.png")):
        eski[d + "/" + os.path.basename(f)] = maske(f)
assert len(eski) > 200, len(eski)

ilk = json.load(open(os.path.join(BURA, "pozlar-05-ilk.json"), encoding="utf-8"))["pozlar"]
ilk_tur = {}
for d in json.load(open(os.path.join(BURA, "duvar-listesi-05-ilk.json"), encoding="utf-8")):
    for o in ("p1", "p2", "p3"):
        ilk_tur[d[o]] = d["tur"]
aday = json.load(open(os.path.join(BURA, "pozlar-05-aday.json"), encoding="utf-8"))["pozlar"]
havuz = []   # (sira, ad, tanim, tur, maske_yolu)
for ad, p in ilk.items():
    havuz.append((0, ad, p, ilk_tur[ad], os.path.join(BURA, "varlik-05-tek/poz", ad + ".png")))
for ad, p in aday.items():
    havuz.append((1, ad, p, p["tur"], os.path.join(BURA, "varlik-05-aday/poz", ad + ".png")))
# kontak sayfasi 1 (19 Eki 2026): bu tabanlar siluette bas asagi / tam kopru gibi okunuyor -> guvenlik kurali (§2) geregi alinmaz
YASAK3 = ("Bridge", "Standing Split", "Half Moon", "Dead Bug", "Lying Knees", "Child", "Lying Floor", "Lying Diag Floor", "Lying Back Floor")


def uygun(p, tur):
    a = p["ad"]
    if tur != 3:
        return True
    if any(y in a for y in YASAK3):
        return False
    if " Child " in a + " " and any(y in a for y in (" Up", " Diag", " Wide", " Hug")):
        return False
    if (" Boat " in a + " " or " Lying " in a + " ") and "Floor" in a:      # yatarken/kayikta kol yere dogru: kol zeminden gecer
        return False
    return True


olcu = []
for sira, ad, p, tur, yol in havuz:
    if not os.path.exists(yol) or not uygun(p, tur):
        continue
    m = maske(yol)
    en, deg = max(((k, iou(m, v)) for k, v in eski.items()), key=lambda x: x[1])
    olcu.append((sira, deg, ad, p, tur, yol, m, en))
secilen = {1: [], 2: [], 3: []}
tum = []
rapor = []
for sira, deg, ad, p, tur, yol, m, en in sorted(olcu, key=lambda x: (x[0], x[1])):
    if len(secilen[tur]) >= 45:
        continue
    if deg >= A.esik_eski:
        continue
    ic = max([iou(m, q[1]) for q in tum] or [0])
    if ic >= A.esik_ic:
        continue
    secilen[tur].append((ad, p, yol)); tum.append((ad, m))
    rapor.append(f"T{tur} {ad:45s} eski {deg:.2f} ({en}) ic {ic:.2f} {'ILK' if sira == 0 else 'ADAY'}")
print({t: len(v) for t, v in secilen.items()})
assert all(len(v) == 45 for v in secilen.values()), "yeterli farkli poz yok - aday havuzunu buyut"

pozlar, duvarlar = {}, []
hedef = os.path.join(BURA, "varlik-05", "poz"); os.makedirs(hedef, exist_ok=True)
for f in glob.glob(os.path.join(hedef, "*.png")):
    os.remove(f)                                               # yalniz secilenler kalsin (motor buradan okur)
for tur in (1, 2, 3):
    L = secilen[tur]
    for ad, p, yol in L:
        q = {k: v for k, v in p.items() if k != "tur"}
        pozlar[ad] = q
        shutil.copy(yol, os.path.join(hedef, ad + ".png"))
    for w in range(15):
        duvarlar.append({"tur": tur, "p1": L[w][0], "p2": L[w + 15][0], "p3": L[w + 30][0]})
not_ = json.load(open(os.path.join(BURA, "pozlar.json"), encoding="utf-8"))["_not"].replace("(REF-053)", "5. video (REF-056, 3 oyuncu, Halloween; poz-sec-05.py olcumle secildi)")
json.dump({"_not": not_, "pozlar": pozlar}, open(os.path.join(BURA, "pozlar-05.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(duvarlar, open(os.path.join(BURA, "duvar-listesi-05.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(os.path.join(BURA, "varlik-05", "iou-secim.txt"), "w", encoding="utf-8").write(
    f"esik eski {A.esik_eski} / ic {A.esik_ic}, eski maske {len(eski)}\n" + "\n".join(rapor) + "\n")
print(f"{len(pozlar)} poz secildi; en yuksek eski IoU {max(float(r.split('eski ')[1][:4]) for r in rapor):.2f}")
