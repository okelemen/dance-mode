"""HUMAN TETRIS 20. video (REF-072, 3 oyuncu, 4 tur x 3 duvar = 12 duvar / 36 poz): hazir siluet adaylarini olcer (poz-sec-17.py'den).
Adaylar (md. 21 5c, 6 Kas 2026): Openclipart kamu mali 32 (REFERANSLAR/OC-dans-siluet/buyuk) + svgsilh CC0 8 (REFERANSLAR/SVGSILH-dans-siluet/png512);
giysisiz duz vucut hatti, kafa siluetin kendi kafasi. Eski pozlar: 3-17. videonun tek kisilik maskeleri + 19. videonun Openclipart siluetleri + kapak 20.
Cikti: aday-olcu-20.json (her adayin en yakin eski pozu ve IoU'su, aday ici en yakin), konsola tablo."""
import glob, json, os
import numpy as np
from PIL import Image

BURA = os.path.dirname(os.path.abspath(__file__))
REF = r"C:\Users\eleme\OneDrive\Masaüstü\REFERANSLAR"
N = 128
ESIK_ESKI, ESIK_IC = 0.78, 0.70


def maske(yol):
    im = np.array(Image.open(yol).convert("RGBA"))
    a = im[:, :, 3] > 40
    if a.mean() > 0.97:                       # opak arka planli PNG: koyu pikseller
        a = im[:, :, :3].mean(2) < 100
    ys, xs = np.nonzero(a)
    a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h, w = a.shape; s = max(h, w)
    kare = np.zeros((s, s), bool); kare[s - h:, (s - w) // 2:(s - w) // 2 + w] = a
    return np.array(Image.fromarray(kare.astype(np.uint8) * 255).resize((N, N), Image.BILINEAR)) > 127


def iou(a, b):
    return max((a & b).sum() / max(1, (a | b).sum()), (a & b[:, ::-1]).sum() / max(1, (a | b[:, ::-1]).sum()))


eski = {}
for d in ("varlik/poz", "varlik-03/poz", "varlik-04/poz", "varlik-05/poz", "varlik-06/poz", "varlik-08/poz", "varlik-09/poz", "varlik-10/poz",
          "varlik-12/poz", "varlik-14/poz", "varlik-16/poz", "varlik-17/poz"):
    for f in glob.glob(os.path.join(BURA, d, "*.png")):
        eski[d + "/" + os.path.basename(f)] = maske(f)
for f in glob.glob(os.path.join(REF, "OC-yoga-siluet", "*-2000.png")):          # 19. video duvar + kapak siluetleri
    eski["19-oc/" + os.path.basename(f)] = maske(f)
for k in ("273073", "277859", "230147", "272052", "309217", "268844"):           # 20. video kapak siluetleri (REF-073)
    eski["20-kapak/" + k] = maske(os.path.join(REF, "OC-dans-siluet", k + "-2000.png"))
n_dosya = sum(len(glob.glob(os.path.join(BURA, d, "*.png"))) for d in ("varlik/poz", "varlik-03/poz", "varlik-04/poz", "varlik-05/poz", "varlik-06/poz",
              "varlik-08/poz", "varlik-09/poz", "varlik-10/poz", "varlik-12/poz", "varlik-14/poz", "varlik-16/poz", "varlik-17/poz"))
assert n_dosya > 560 and len(eski) >= n_dosya + 18 + 6, (len(eski), n_dosya)   # bos sayim = kirik komut, "tekrar yok" degil

aday = {}
for f in sorted(glob.glob(os.path.join(REF, "OC-dans-siluet", "buyuk", "*.png"))):
    aday["oc-" + os.path.basename(f)[:-4]] = f
for k in ("1043462", "1055879", "1074932", "1132025", "1132027", "1226176", "1280880", "1824819"):
    aday["sv-" + k] = os.path.join(REF, "SVGSILH-dans-siluet", "png512", k + ".png")
assert len(aday) == 40, len(aday)
M = {k: maske(v) for k, v in aday.items()}
olcu = {}
for k, m in M.items():
    en, deg = max(((e, iou(m, v)) for e, v in eski.items()), key=lambda x: x[1])
    ic, ideg = max(((o, iou(m, M[o])) for o in M if o != k), key=lambda x: x[1])
    olcu[k] = {"eski": en, "eski_iou": round(float(deg), 3), "ic": ic, "ic_iou": round(float(ideg), 3)}
json.dump(olcu, open(os.path.join(BURA, "aday-olcu-20.json"), "w", encoding="utf-8"), indent=1)
print("eski maske", len(eski), "aday", len(M))
for k, v in sorted(olcu.items(), key=lambda x: -x[1]["eski_iou"]):
    print("%-12s eski %.2f %-32s ic %.2f %s%s" % (k, v["eski_iou"], v["eski"][-32:], v["ic_iou"], v["ic"],
          "  <-- ESKI" if v["eski_iou"] >= ESIK_ESKI else ("  <-- IC" if v["ic_iou"] >= ESIK_IC else "")))
