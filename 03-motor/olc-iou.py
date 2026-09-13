"""Siluet maskesi CAKISMASINI olcer (IoU). Goz karari yerine sayi.

   python olc-iou.py ../04-ciktilar/faz-A [esik]
   python olc-iou.py ../04-ciktilar/faz-A --set duck,dodge-right,arm-stretch,twist-dance

Kural (REFERANSLAR/hareket-defteri.md): bir bolumun dort hareketi dort AYRI
sekil ailesinden gelmeli. Iki hareket esigin (0,50) ustunde cakisiyorsa ayni
sette ikisi birden olmaz - HUD boyutundaki siluet kutusunda ayirt edilmiyorlar.

YONTEM - TEPE FAZI (13 Eyl 2026'da dogrulanarak secildi)
1. Kare 120x160'a normalize edilir. Siluet KONTUR olarak ciziliyor (ici bos);
   kontur uzerinden IoU olcmek degeri yapay olarak dusuruyor (butun ciftler
   0,1-0,2 cikiyordu), bu yuzden maske kapatilip DOLDURULUYOR.
2. Her klibin TEPE FAZI bulunur: notr duruma (faz 0) en uzak olan faz.
   Karsilastirma tepe-tepe yapilir.

NEDEN tum faz ciftlerinde maksimum DEGIL: butun klipler "notr basla - notr bit"
kuralina uyuyor, yani her klibin basi ve sonu ayni duruş. Faz ciftleri uzerinden
maksimum almak her çiftte o notr ani buluyor ve HER SEY cakisik cikiyor.
Olculdu: o yontemle bilinen kotu cift (duck x arms_up) 0,698, kabul edilmis cift
(duck x dodge, HAR-001'de birlikte) 0,719 - yani siralama TERS donuyordu.
Tepe fazi yonteminde duck x arms_up 0,698 ile en tepede, duck x dodge 0,474 ile
esigin altinda: bilinen iki gercegi de dogru veren tek yontem bu.

DOGRULAMA: python olc-iou.py ../04-ciktilar/faz-kontrol-iou
  duck x arms-up en yuksek cift olmali ve esigi asmali.
"""
import sys, os, glob, itertools
import numpy as np
from PIL import Image
from scipy import ndimage

dizin = sys.argv[1] if len(sys.argv) > 1 else '../04-ciktilar/faz-A'
ESIK = 0.50
SET = None
if '--set' in sys.argv:
    SET = sys.argv[sys.argv.index('--set') + 1].split(',')
for a in sys.argv[2:]:
    try:
        ESIK = float(a)
    except ValueError:
        pass


def maske_al(yol):
    im = Image.open(yol).convert('RGBA').resize((120, 160), Image.BILINEAR)
    a = np.asarray(im).astype(np.float32) / 255
    k = (a[:, :, 3] > 0.35) & (a[:, :, :3].max(2) > 0.20)
    if k.sum() < 50:
        k = a[:, :, :3].max(2) > 0.35
    k = ndimage.binary_closing(k, structure=np.ones((3, 3)), iterations=2)
    return ndimage.binary_fill_holes(k)


def iou(m1, m2):
    b = (m1 | m2).sum()
    return (m1 & m2).sum() / b if b else 0.0


klipler = {}
for f in sorted(glob.glob(os.path.join(dizin, '*.png'))):
    ad, kuyruk = os.path.basename(f).rsplit('-faz', 1)
    klipler.setdefault(ad, {})[int(kuyruk[:3])] = maske_al(f)

tepeler = {}
for ad, fz in klipler.items():
    notr = fz[min(fz)]
    tepeler[ad] = max(fz, key=lambda f: 1.0 - iou(fz[f], notr))

adlar = sorted(SET) if SET else sorted(klipler)
eksik = [a for a in adlar if a not in klipler]
if eksik:
    print('UYARI: bu kliplerin karesi yok:', ', '.join(eksik))
    adlar = [a for a in adlar if a in klipler]

print('dizin:', dizin, ' esik:', ESIK)
for ad in adlar:
    print('  %-14s tepe faz %.2f, doluluk %%%.1f'
          % (ad, tepeler[ad] / 100, klipler[ad][tepeler[ad]].mean() * 100))

print('\nIKILI CAKISMA (tepe fazlarinda IoU)')
ihlal = []
for a1, a2 in itertools.combinations(adlar, 2):
    v = iou(klipler[a1][tepeler[a1]], klipler[a2][tepeler[a2]])
    if v >= ESIK:
        ihlal.append((a1, a2, v))
    print('  %-14s x %-14s  %.3f  %s'
          % (a1, a2, v, 'IHLAL' if v >= ESIK else 'TAMAM'))

print('\nSONUC:', 'SET GECERLI' if not ihlal
      else 'SET GECERSIZ - %d cift esigin ustunde' % len(ihlal))
for a1, a2, v in ihlal:
    print('  ELE:', a1, '/', a2, '%.3f' % v)
