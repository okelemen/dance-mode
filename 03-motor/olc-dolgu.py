"""Dolgunun BANT BANT boslugunu olcer - ufka dogru bosluk kaliyor mu?

   python olc-dolgu.py <kare.png> [--zemin et|koyu] [--ufuk 0.44]

Gerekce (13 Eyl 2026, kullanici): "Ufka dogru bosluklar goruyorum. Tabanda
belirgin bosluk kalmayacak." Tek bir genel oran bunu YAKALAMIYOR: yakin plandaki
buyuk nesneler ortalamayi asagi cekiyor ve ufka yakin bantta acik kalan zemin
gorunmuyor. Perspektifte ufka yakin bant ekranin kucuk bir kismi ama IZLEYICININ
BAKTIGI yer orasi.

Yontem: koridorun DISI, ufuk cizgisinin ALTI alinir ve UC BANDA bolunur
(ufka gore): UZAK / ORTA / YAKIN. Her bantta zemin renginin gorundugu piksel
orani ayri ayri verilir.

Zemin tespiti:
  --zemin et   : kirmizi ic (R baskin) - karpuz mekani
  --zemin koyu : dolgudan koyu yuzey   - genel
"""
import sys
import numpy as np
from PIL import Image

f = sys.argv[1]
ZEMIN = 'et'
UFUK = 0.44
if '--zemin' in sys.argv:
    ZEMIN = sys.argv[sys.argv.index('--zemin') + 1]
if '--ufuk' in sys.argv:
    UFUK = float(sys.argv[sys.argv.index('--ufuk') + 1])

im = np.asarray(Image.open(f).convert('RGB')).astype(np.float32)
H, W, _ = im.shape
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

if ZEMIN == 'et':
    zemin = (r > g + 35) & (r > b + 20)
else:
    V = im.max(2)
    zemin = V < 60

# HUD ve koridor disla
hud = np.zeros((H, W), bool)
hud[int(H * 0.24):int(H * 0.87), 0:int(W * 0.27)] = True     # siluet paneli
hud[0:int(H * 0.40), int(W * 0.72):W] = True                  # COMBO
hud[int(H * 0.70):H, int(W * 0.80):W] = True                  # sure halkasi

y0 = int(H * UFUK)
print(f)
print('  ufuk satiri: %d  (kare yuksekligi %d)' % (y0, H))
print('\n  BANT            bosluk (zemin gorunen)   kural')
kotu = []
for ad, a, b2 in [('UZAK (ufka yakin)', 0.00, 0.22),
                  ('ORTA', 0.22, 0.55),
                  ('YAKIN (kamera)', 0.55, 1.00)]:
    ya = y0 + int((H - y0) * a)
    yb = y0 + int((H - y0) * b2)
    m = np.zeros((H, W), bool)
    m[ya:yb, :] = True
    m &= ~hud
    # koridor: bandin ortasinda perspektife gore daralan serit
    for y in range(ya, yb):
        k = (y - y0) / max(1, H - y0)
        yari = int(W * (0.012 + 0.30 * k))
        m[y, W // 2 - yari:W // 2 + yari] = False
    if m.sum() < 500:
        continue
    oran = zemin[m].mean() * 100
    durum = 'TAMAM' if oran < 25 else 'IHLAL'
    if oran >= 25:
        kotu.append((ad, oran))
    print('  %-16s %6.1f%%                  <%%25  %s' % (ad, oran, durum))

print('\n  SONUC:', 'DOLGU YETERLI' if not kotu else 'BOSLUK VAR - ' +
      ', '.join('%s %%%.1f' % k for k in kotu))
