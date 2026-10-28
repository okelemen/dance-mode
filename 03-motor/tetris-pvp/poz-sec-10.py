"""HUMAN TETRIS 10. video (REF-061 HumanWarmUp, 1 oyuncu) - 29 pozu OLCUMLE secer: aday maskeleri (varlik-10-aday/poz, Actions)
eski 8 videonun maskelerine ve secilenlere aynali IoU ile karsilastirilir.

    python poz-sec-10.py [--esik-eski 0.78] [--esik-ic 0.75] [--havuz]

Tur yok (REF-061 tek akis, 19 -> 29 duvar); siralama grubu 1 ayakta 10 / 2 hamle-tekme 10 / 3 yer 9. Duvar basina tek poz (p1).
Cikti pozlar-10.json, duvar-listesi-10.json, varlik-10/poz/, varlik-10/iou-secim.txt.
"""
import argparse, glob, json, os, shutil
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--esik-eski", type=float, default=0.78)
ap.add_argument("--esik-ic", type=float, default=0.55)   # kontak 2: 0,75 dort benzer yan hamle birakti

BURA = os.path.dirname(os.path.abspath(__file__))
N = 128
DUVAR_SAYI = {1: 10, 2: 10, 3: 9}
# siluette bas asagi / tam kopru gibi okunan tabanlar (5. video kontak dersi, TALIMATLAR §4 guvenlik)
YASAK = ("Standing Split", "Bridge", "Headstand", "Handstand")
# kontak 1 (28 Eki 2026): siluette havada / dusuyor / ziplama gibi okunanlar
HARIC = {"daily-seated-twist-arm-back", "daily-boat-arms-up", "daily-child-pose-arms-back", "daily-low-squat-hands-floor",
         "daily-side-plank-knee-down-arm-up", "daily-bear-crawl-hold", "daily-seated-butterfly-hands-feet",
         "daily-dancer-hold-arm-forward", "daily-deep-lunge-hands-floor", "daily-lunge-twist-arms-t", "daily-crescent-lunge-arms-v",
         "daily-standing-calf-stretch-hands-wall",
         # kontak 2: garip / ziplama okunan havuz pozlari
         "spark-drift-79", "light-drift-73", "fresh-drift-99",
         # kontak 3: ayni bacakli genis yan hamle tekrari (IoU kol farkini sayiyor) + dusuyor okunan
         "daily-low-side-lunge-arms-front", "daily-side-lunge-hands-prayer", "flow-drift-89"}
# grup 3 havuzundan yalniz el + ayak / diz yere acikca basanlar (yer-adaylari.jpg gozle secimi)
IZIN3 = {"flow-drift-78", "smooth-drift-88", "fresh-drift-99", "morning-drift-127", "morning-drift-135", "light-drift-73"}
ap.add_argument("--havuz", action="store_true", help="elle tasarlananlar yetmezse rastgele havuzu da kullan")
A = ap.parse_args()
A_havuz = lambda: A.havuz


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
for d in ("varlik/poz", "varlik-03/poz", "varlik-04/poz", "varlik-05/poz", "varlik-06/poz", "varlik-08/poz", "varlik-09/poz"):
    for f in glob.glob(os.path.join(BURA, d, "*.png")):
        eski[d + "/" + os.path.basename(f)] = maske(f)
n_eski = sum(len(glob.glob(os.path.join(BURA, d, "*.png"))) for d in ("varlik/poz", "varlik-03/poz", "varlik-04/poz", "varlik-05/poz", "varlik-06/poz", "varlik-08/poz", "varlik-09/poz"))
assert len(eski) == n_eski and n_eski > 530, (len(eski), n_eski)

aday = json.load(open(os.path.join(BURA, "pozlar-10-aday.json"), encoding="utf-8"))["pozlar"]
olcu, eksik = [], []
for ad, p in aday.items():
    yol = os.path.join(BURA, "varlik-10-aday/poz", ad + ".png")
    if not os.path.exists(yol):
        eksik.append(ad); continue
    if any(y in p["ad"] for y in YASAK) or ad in HARIC or (not p.get("el") and not A_havuz()):
        continue
    if p["tur"] == 3 and not p.get("el") and ad not in IZIN3:
        continue
    m = maske(yol)
    en, deg = max(((k, iou(m, v)) for k, v in eski.items()), key=lambda x: x[1])
    olcu.append((0 if p.get("el") else 1, deg, ad, p, p["tur"], yol, m, en))
assert not eksik or len(eksik) < len(aday) // 2, f"maske eksik: {len(eksik)}"

secilen = {t: [] for t in DUVAR_SAYI}
tum, rapor = [], []
for sira, deg, ad, p, tur, yol, m, en in sorted(olcu, key=lambda x: (x[0], x[1])):
    if len(secilen[tur]) >= DUVAR_SAYI[tur] or deg >= A.esik_eski:
        continue
    ic = max([iou(m, q[1]) for q in tum] or [0])
    if ic >= A.esik_ic:
        continue
    secilen[tur].append((ad, p, yol)); tum.append((ad, m))
    rapor.append(f"T{tur} {ad:50s} eski {deg:.2f} ({en}) ic {ic:.2f} {'EL' if sira == 0 else 'HAVUZ'}")
print({t: len(v) for t, v in secilen.items()}, "eksik maske:", len(eksik))
assert all(len(secilen[t]) == DUVAR_SAYI[t] for t in secilen), "yeterli farkli poz yok - aday havuzunu buyut"

pozlar, duvarlar = {}, []
hedef = os.path.join(BURA, "varlik-10", "poz"); os.makedirs(hedef, exist_ok=True)
for f in glob.glob(os.path.join(hedef, "*.png")):
    os.remove(f)
for tur in sorted(DUVAR_SAYI):
    L, n = secilen[tur], DUVAR_SAYI[tur]
    for ad, p, yol in L:
        pozlar[ad] = {k: v for k, v in p.items() if k not in ("tur", "el")}
        shutil.copy(yol, os.path.join(hedef, ad + ".png"))
    for w in range(n):
        duvarlar.append({"tur": tur, "p1": L[w][0]})
not_ = json.load(open(os.path.join(BURA, "pozlar.json"), encoding="utf-8"))["_not"].replace(
    "(REF-053)", "10. video (REF-061, 1 oyuncu, 5 dk; poz-sec-10.py olcumle secildi)")
json.dump({"_not": not_, "pozlar": pozlar}, open(os.path.join(BURA, "pozlar-10.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(duvarlar, open(os.path.join(BURA, "duvar-listesi-10.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(os.path.join(BURA, "varlik-10", "iou-secim.txt"), "w", encoding="utf-8").write(
    f"esik eski {A.esik_eski} / ic {A.esik_ic}, eski maske {len(eski)}\n" + "\n".join(rapor) + "\n")
print(f"{len(pozlar)} poz, {len(duvarlar)} duvar; en yuksek eski IoU {max(float(r.split('eski ')[1][:4]) for r in rapor):.2f}")
