"""HUMAN TETRIS 16. video (REF-067, 1v1, 3 tur): 42 pozu olcumle secer (poz-sec-14.py'den). Cikti pozlar-16.json, duvar-listesi-16.json, varlik-16/poz/.
Kapakta onaylanan 4 poz (aday "kapak": true) zorunlu girer; yine de eski IoU raporlanir."""
import argparse, glob, json, os, shutil
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--esik-eski", type=float, default=0.78)
ap.add_argument("--esik-ic", type=float, default=0.55)   # kontak 2: 0,75 dort benzer yan hamle birakti

BURA = os.path.dirname(os.path.abspath(__file__))
N = 128
DUVAR_SAYI = {1: 7, 2: 7, 3: 7}   # REF-067: ROUND 1 EASY / 2 MEDIUM / 3 HARD   # duvar; poz iki kati
# siluette bas asagi / tam kopru gibi okunan tabanlar (5. video kontak dersi, TALIMATLAR §4 guvenlik)
YASAK = ("Standing Split", "Bridge", "Headstand", "Handstand")
# kontak 1 (28 Eki 2026): siluette havada / dusuyor / ziplama gibi okunanlar
# kontak 1 (30 Eki 2026): siluette havada / dusuyor / bas asagi okunanlar
# kontak 1 (1 Kas 2026): havada / siciyor gibi ya da eli yere degmeden asili okunanlar
# kontak 1 (3 Kas 2026): siluette havada / ziplar / duser gibi okunanlar
HARIC = {"sakura-chair-pose-arms-up", "sakura-lunge-reach-forward", "sakura-lunge-prayer-twist", "sakura-seated-knees-hug", "sakura-side-kneel-leg-out",
         "sakura-seated-one-knee-reach", "sakura-kneel-sit-heels-arms-forward", "sakura-gate-pose-low-hand", "sakura-kneel-lean-back-hands",
         "sakura-frog-squat-arms-up", "sakura-kneel-shrug-up",
         "sakura-gate-pose-over-reach", "sakura-dancer-pose-reach", "sakura-deep-squat-elbows-knees"}   # kontak 2
# grup 3 havuzundan yalniz el + ayak / diz yere acikca basanlar (yer-adaylari.jpg gozle secimi)
IZIN3 = set()
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
for d in ("varlik/poz", "varlik-03/poz", "varlik-04/poz", "varlik-05/poz", "varlik-06/poz", "varlik-08/poz", "varlik-09/poz", "varlik-10/poz", "varlik-12/poz", "varlik-14/poz"):
    for f in glob.glob(os.path.join(BURA, d, "*.png")):
        eski[d + "/" + os.path.basename(f)] = maske(f)
n_eski = sum(len(glob.glob(os.path.join(BURA, d, "*.png"))) for d in ("varlik/poz", "varlik-03/poz", "varlik-04/poz", "varlik-05/poz", "varlik-06/poz", "varlik-08/poz", "varlik-09/poz", "varlik-10/poz", "varlik-12/poz", "varlik-14/poz"))
assert len(eski) == n_eski and n_eski > 530, (len(eski), n_eski)

aday = json.load(open(os.path.join(BURA, "pozlar-16-aday.json"), encoding="utf-8"))["pozlar"]
olcu, eksik = [], []
for ad, p in aday.items():
    yol = os.path.join(BURA, "varlik-16-aday-2/tetris-varlik/poz", ad + ".png")
    if not os.path.exists(yol):
        eksik.append(ad); continue
    if any(y in p["ad"] for y in YASAK) or ad in HARIC or (not p.get("el") and not A_havuz()):
        continue
    if p["tur"] == 3 and not p.get("el") and ad not in IZIN3:
        continue
    m = maske(yol)
    en, deg = max(((k, iou(m, v)) for k, v in eski.items()), key=lambda x: x[1])
    olcu.append((-1 if p.get("kapak") else (0 if p.get("el") else 1), deg, ad, p, p["tur"], yol, m, en))
assert not eksik or len(eksik) < len(aday) // 2, f"maske eksik: {len(eksik)}"

secilen = {t: [] for t in DUVAR_SAYI}
tum, rapor = [], []
for sira, deg, ad, p, tur, yol, m, en in sorted(olcu, key=lambda x: (x[0], x[1])):
    if len(secilen[tur]) >= DUVAR_SAYI[tur] * 2 or (deg >= A.esik_eski and sira >= 0):
        continue
    ic = max([iou(m, q[1]) for q in tum] or [0])
    if ic >= A.esik_ic and sira >= 0:  # 30 Eki 2026: 25. duvar elle secildi (kollari ters, yere net basiyor)
        continue
    secilen[tur].append((ad, p, yol)); tum.append((ad, m))
    rapor.append(f"T{tur} {ad:50s} eski {deg:.2f} ({en}) ic {ic:.2f} {'KAPAK' if sira < 0 else 'EL' if sira == 0 else 'HAVUZ'}")
print({t: len(v) for t, v in secilen.items()}, "eksik maske:", len(eksik))
assert all(len(secilen[t]) == DUVAR_SAYI[t] * 2 for t in secilen), "yeterli farkli poz yok - aday havuzunu buyut"

pozlar, duvarlar = {}, []
hedef = os.path.join(BURA, "varlik-16", "poz"); os.makedirs(hedef, exist_ok=True)
for f in glob.glob(os.path.join(hedef, "*.png")):
    os.remove(f)
for tur in sorted(DUVAR_SAYI):
    L, n = secilen[tur], DUVAR_SAYI[tur]
    for ad, p, yol in L:
        pozlar[ad] = {k: v for k, v in p.items() if k not in ("tur", "el", "kapak")}
        shutil.copy(yol, os.path.join(hedef, ad + ".png"))
    for w in range(n):
        duvarlar.append({"tur": tur, "p1": L[2 * w][0], "p2": L[2 * w + 1][0]})
not_ = json.load(open(os.path.join(BURA, "pozlar.json"), encoding="utf-8"))["_not"].replace(
    "(REF-053)", "16. video (REF-067, 1v1, 3 tur; poz-sec-16.py olcumle secildi)")
json.dump({"_not": not_, "pozlar": pozlar}, open(os.path.join(BURA, "pozlar-16.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(duvarlar, open(os.path.join(BURA, "duvar-listesi-16.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(os.path.join(BURA, "varlik-16", "iou-secim.txt"), "w", encoding="utf-8").write(
    f"esik eski {A.esik_eski} / ic {A.esik_ic}, eski maske {len(eski)}\n" + "\n".join(rapor) + "\n")
print(f"{len(pozlar)} poz, {len(duvarlar)} duvar; en yuksek eski IoU {max(float(r.split('eski ')[1][:4]) for r in rapor):.2f}")
