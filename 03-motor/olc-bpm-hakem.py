"""HAKEM BPM: vurus izleme + dogrusal oturtma.

Tarak (comb), otokorelasyon ve ince tarama ayni parcada farkli sayilar
verebiliyor (Golden Groove: 135,250 / 134,734 / 134,217). Bu betik KARPUZ
bolumunde hakem sayilan yontemi uygular:

1. Onset zarfi -> tepe noktalari (gercek vuruslar).
2. Aday BPM araliginda en iyi izgara fazi bulunur.
3. Her vurus en yakin izgara indeksine atanir; SADECE guclu ve tekil
   eslesmeler tutulur.
4. zaman = a + b * indeks dogrusu EN KUCUK KARELER ile oturtulur -> BPM = 60/b.
   Dogrusal oturtma tum parcayi kullandigi icin pencere gurultusunden
   etkilenmiyor; egim de tempo kaymasini dogrudan gosteriyor.
5. Kendi kendini dogrulama: bulunan BPM'de parcanin kac TAM olcu oldugu
   yazilir - tam sayiya cok yakinsa BPM dogru demektir.

   python olc-bpm-hakem.py <ses> [merkez_bpm]
"""
import subprocess, sys
import numpy as np

SR = 22050
HOP = 256
yol = sys.argv[1]
merkez = float(sys.argv[2]) if len(sys.argv) > 2 else 135.0

p = subprocess.run(['ffmpeg', '-v', 'error', '-i', yol, '-f', 'f32le',
                    '-ac', '1', '-ar', str(SR), '-'], stdout=subprocess.PIPE, check=True)
x = np.frombuffer(p.stdout, dtype=np.float32).astype(np.float64)
sure = len(x) / SR

# --- onset zarfi: spektral akis
N = 1024
pen = np.hanning(N)
kare = np.lib.stride_tricks.sliding_window_view(x, N)[::HOP]
S = np.abs(np.fft.rfft(kare * pen, axis=1))
akis = np.maximum(0, np.diff(S, axis=0)).sum(axis=1)
akis = akis / (akis.max() + 1e-9)
t_akis = (np.arange(len(akis)) + 1) * HOP / SR

# --- tepe noktalari
esik = np.percentile(akis, 70)
tepe = []
for i in range(1, len(akis) - 1):
    if akis[i] > esik and akis[i] >= akis[i-1] and akis[i] > akis[i+1]:
        tepe.append(i)
tepe = np.array(tepe)
tt = t_akis[tepe]
guc = akis[tepe]
print('dosya      :', yol.replace('\\', '/').split('/')[-1])
print('sure       : %.3f sn' % sure)
print('vurus adayi: %d' % len(tt))

# --- en iyi izgara: BPM ve faz taramasi
en_iyi = None
for bpm in np.arange(merkez - 4, merkez + 4, 0.01):
    per = 60.0 / bpm
    faz = (tt / per) % 1.0
    # dairesel ortalama: tutarli faz varsa uzunluk buyuk olur
    v = np.exp(2j * np.pi * faz)
    R = np.abs((v * guc).sum()) / guc.sum()
    if en_iyi is None or R > en_iyi[1]:
        en_iyi = (bpm, R, np.angle((v * guc).sum()) / (2 * np.pi) % 1.0)
bpm0, R, faz0 = en_iyi
print('kaba izgara: %.3f BPM (faz tutarliligi %.3f)' % (bpm0, R))

# --- indeks atama + dogrusal oturtma
per = 60.0 / bpm0
t0 = faz0 * per
idx = np.round((tt - t0) / per).astype(int)
# ayni indekse dusen birden fazla tepe -> en gucluyu tut
tut = {}
for k, i in enumerate(idx):
    if i not in tut or guc[k] > guc[tut[i]]:
        tut[i] = k
sec = np.array(sorted(tut.values()))
i_sec, t_sec, g_sec = idx[sec], tt[sec], guc[sec]
# izgaraya cok uzak olanlari at (yarim vurustan fazla sapma)
sapma = np.abs(t_sec - (t0 + i_sec * per))
iyi = sapma < per * 0.25
i_sec, t_sec = i_sec[iyi], t_sec[iyi]
A = np.vstack([np.ones_like(i_sec), i_sec]).T
(a, b), kalan, *_ = np.linalg.lstsq(A, t_sec, rcond=None)
bpm = 60.0 / b
hata = t_sec - (a + b * i_sec)
print('eslesen    : %d vurus' % len(i_sec))
print('HAKEM BPM  : %.4f' % bpm)
print('ilk vurus  : %.4f sn' % a)
print('faz hatasi : ort %.1f ms | std %.1f ms | en kotu %.1f ms'
      % (hata.mean() * 1000, hata.std() * 1000, np.abs(hata).max() * 1000))
# egim kaymasi: ilk/son yari ayri oturtma
yari = len(i_sec) // 2
for ad, dilim in [('ilk yari', slice(0, yari)), ('son yari', slice(yari, None))]:
    ii, tt2 = i_sec[dilim], t_sec[dilim]
    AA = np.vstack([np.ones_like(ii), ii]).T
    (aa, bb), *_ = np.linalg.lstsq(AA, tt2, rcond=None)
    print('  %s: %.4f BPM' % (ad, 60.0 / bb))
olcu = (sure - a) / (b * 4)
print('parca %.3f olcu (tam sayiya uzaklik %.3f)' % (olcu, abs(olcu - round(olcu))))
