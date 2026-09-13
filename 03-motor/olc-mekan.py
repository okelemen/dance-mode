"""Mekan karesini KURALLARLA olcer. Gozle onay yok.
   python olc-mekan.py ../04-ciktilar/taban-v2-4600.png
Kurallar: 07-mekan/MEKAN-KARARI.md "Dogrulama olcutu"
 - ufuk cizgisi %42-50
 - siyah piksel (V<0,04) %0
 - S>0,5 doygun pikselin COGU cue/nota/siluet katmaninda olmali, mekanda degil
NOT: doygunluk yalnizca GORUNUR pikselde (V>0,15) olculur. Koyu pikselde S
matematiksel olarak siser - V=0,05'te S=0,87 cikiyor ve hicbir sey ifade etmiyor.
Bu tuzaga 12 Eyl 2026'da bir kez dusuldu, o yuzden yazili."""
import sys
import numpy as np
from PIL import Image
f = sys.argv[1]
im = np.asarray(Image.open(f).convert('RGB')).astype(np.float32) / 255
H, W, _ = im.shape
mx = im.max(2); mn = im.min(2)
V = mx; S = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
gor = V > 0.15                                   # gorunur piksel maskesi
# HUD DISLANIR: siyah piksel kurali MEKAN icin yazilmis ("deniz siyaha
# dusuyordu"). Siluet paneli zaten tam siyah bir kutu ve karenin %10'unu
# kapliyor; onu sayinca kural hicbir zaman tutmaz. 12 Eyl 2026 olcumu:
# toplam siyah %11,6 iken panel disi yalnizca %0,9 idi.
hud = np.zeros(V.shape, bool)
hud[int(H*0.24):int(H*0.87), int(W*0.02):int(W*0.25)] = True   # siluet paneli
hud[0:int(H*0.40), int(W*0.72):W] = True                        # COMBO + etiket
hud[int(H*0.70):H, int(W*0.82):W] = True                        # sure halkasi
siyah = (V < 0.04)[~hud].mean() * 100
# ufuk: orta kolonlarda satir ortalamasinin en buyuk ziplamasi. HUD ve
# kenar panelleri dislaniyor, alt %20 (vurus cizgisi/yol) taranmiyor.
orta = im[:, int(W*0.35):int(W*0.65)].mean(axis=(1, 2))
# --ust: taramanin BASLADIGI satir orani. Mekan yukaridan kuruluyorsa (KARPUZ,
# MEK-002) gokteki kutleler kendi kenarlarini yapiyor ve argmax onlari ufuk
# saniyor - olcum %22 diyordu, gercek ufuk %44'tu. Varsayilan 0: eski cagrilar
# aynen calisir.
UST = 0.0
if '--ust' in sys.argv:
    UST = float(sys.argv[sys.argv.index('--ust') + 1])
u0 = int(H * UST)
ufuk = int(np.argmax(np.abs(np.diff(orta))[u0:int(H*0.8)])) + 1 + u0
# mekan bandi = kadrajin ust yarisi, oyun alani disi orta serit
mekan = (slice(0, int(H*0.44)), slice(int(W*0.30), int(W*0.70)))
Sm = S[mekan][gor[mekan] & ~hud[mekan]]
print(f)
print('  ufuk                %%%.0f   %s (kural %%42-50)' % (ufuk/H*100, 'TAMAM' if 42 <= ufuk/H*100 <= 50 else 'IHLAL'))
print('  siyah piksel (HUD disi) %.1f%%  %s (kural %%0)' % (siyah, 'TAMAM' if siyah < 0.5 else 'IHLAL'))
print('  V medyan (tum kare) %.3f' % np.median(V))
print('  gorunur piksel      %.1f%%' % (gor.mean()*100))
print('  MEKAN S medyan      %.3f  %s (kural <0,25 - doygunluk mekanda olmaz)'
      % (np.median(Sm) if Sm.size else 0, 'TAMAM' if Sm.size and np.median(Sm) < 0.25 else 'IHLAL'))
print('  MEKAN S>0,5         %.1f%% (gorunur, HUD disi)' % ((S[gor & ~hud] > 0.5).mean()*100))
print('  ust yari V %.3f | alt yari V %.3f' % (V[:int(H*0.44)].mean(), V[int(H*0.44):].mean()))
