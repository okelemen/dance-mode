"""Yeni poz maskelerini eski videolarin maskeleriyle karsilastirir (sekil tekrari kontrolu, goz karari yerine olcu).

    python olc-poz-iou.py --yeni varlik-04/poz --eski varlik/poz varlik-03/poz [--esik 0.80]

Her maske: alfa > 0 -> kutuya kirpilir, kareye ortalanir, 128x128. IoU hem duz hem aynali (P1/P2 aynasi ayni poz sayilir).
Cikti: her yeni poz icin en benzer eski poz + IoU; esigi gecenler 'TEKRAR' diye isaretlenir. Ayrica yeni pozlarin kendi
aralarindaki en yuksek IoU (videoda ayni sekil iki kez).
"""
import argparse, glob, os
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--yeni", required=True)
ap.add_argument("--eski", nargs="+", required=True)
ap.add_argument("--esik", type=float, default=0.80)
A = ap.parse_args()
N = 128


def maske(yol):
    a = np.array(Image.open(yol).convert("RGBA"))[:, :, 3] > 40
    ys, xs = np.nonzero(a)
    a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h, w = a.shape; s = max(h, w)
    kare = np.zeros((s, s), bool); kare[s - h:, (s - w) // 2:(s - w) // 2 + w] = a      # zemine oturt, yatay ortala
    return np.array(Image.fromarray(kare.astype(np.uint8) * 255).resize((N, N), Image.BILINEAR)) > 127


def iou(a, b):
    return max((a & b).sum() / max(1, (a | b).sum()), (a & b[:, ::-1]).sum() / max(1, (a | b[:, ::-1]).sum()))


oku = lambda d: {os.path.splitext(os.path.basename(f))[0]: maske(f) for f in sorted(glob.glob(os.path.join(d, "*.png")))}
yeni = oku(A.yeni)
eski = {}
for d in A.eski:
    eski.update({f"{os.path.basename(os.path.dirname(d.rstrip('/')))}/{k}": v for k, v in oku(d).items()})
assert yeni and eski, (len(yeni), len(eski))
print(f"yeni {len(yeni)} maske, eski {len(eski)} maske, esik {A.esik}")
tekrar = 0
for ad, m in yeni.items():
    en, deg = max(((k, iou(m, v)) for k, v in eski.items()), key=lambda x: x[1])
    ic, ideg = max(((k, iou(m, v)) for k, v in yeni.items() if k != ad), key=lambda x: x[1])
    bayrak = " TEKRAR" if deg >= A.esik else ""
    bayrak += " IC-TEKRAR" if ideg >= A.esik else ""
    tekrar += bool(bayrak)
    print(f"{ad:40s} eski {deg:.2f} {en:40s} | ic {ideg:.2f} {ic}{bayrak}")
print(f"isaretli: {tekrar}")
