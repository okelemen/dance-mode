"""Muzigin temposu SABIT mi, yoksa KAYIYOR mu - bagimsiz ikinci yontem.

   python olc-tempo-kayma.py ../01-muzik/neon-party-pulse.mp3

analiz-bpm.py dilim dilim BPM veriyor; dilimler arasi fark hem gercek kaymadan
hem olcum penceresinden gelebilir. Bu betik farkli bir yol izliyor:

1. Onset (vurus baslangici) zarfi cikarilir.
2. Genis bir BPM araliginda TARAK (comb) puani hesaplanir -> en iyi sabit BPM.
3. O sabit izgaranin FAZ HATASI parca boyunca olculur: her vurusun en yakin
   onset'e uzakligi. Tempo gercekten sabitse hata parca boyunca 0 civarinda
   salinir; KAYIYORSA hata duzenli olarak buyur (isaretli birikme).
4. Ayrica parcanin ilk ve son 30 saniyesi AYRI AYRI taranir.

Ciktidaki "birikimli faz hatasi" milisaniye cinsindendir. 130 BPM'de bir vurus
461 ms; hata bunun yarisina yaklastiysa cue'lar gozle gorulur kayar.
"""
import subprocess, sys
import numpy as np

SR = 22050
yol = sys.argv[1]
p = subprocess.run(['ffmpeg', '-v', 'error', '-i', yol, '-f', 'f32le',
                    '-ac', '1', '-ar', str(SR), '-'],
                   stdout=subprocess.PIPE, check=True)
x = np.frombuffer(p.stdout, dtype=np.float32).astype(np.float64)
sure = len(x) / SR
print('dosya:', yol.split('/')[-1])
print('sure : %.3f sn' % sure)

# --- onset zarfi: kisa pencere enerjisinin POZITIF farki (spectral flux yerine
#     enerji akisi - kick agirlikli tekno icin yeterli ve hizli)
N = 256
kare = len(x) // N
env = np.abs(x[:kare * N].reshape(kare, N)).mean(axis=1)
akis = np.diff(env, prepend=env[0])
akis[akis < 0] = 0
akis = akis / (akis.max() + 1e-9)
FPS = SR / N


def tarak(sinyal, bpm_min=100, bpm_max=170, adim=0.05):
    """Verilen zarf icin en iyi sabit BPM'i tarak puaniyla bulur."""
    en_iyi, en_puan = None, -1
    for bpm in np.arange(bpm_min, bpm_max, adim):
        periyot = 60.0 / bpm * FPS
        if periyot < 4:
            continue
        idx = np.arange(0, len(sinyal), periyot)
        idx = np.round(idx).astype(int)
        idx = idx[idx < len(sinyal)]
        puan = sinyal[idx].mean()
        if puan > en_puan:
            en_puan, en_iyi = puan, bpm
    return en_iyi, en_puan


bpm, _ = tarak(akis)
print('\nTARAK YONTEMI (tum parca): %.3f BPM' % bpm)

# ilk / son 30 saniye ayri
n30 = int(30 * FPS)
b_ilk, _ = tarak(akis[:n30])
b_son, _ = tarak(akis[-n30:])
print('  ilk 30 sn: %.3f BPM   son 30 sn: %.3f BPM   fark: %+.3f'
      % (b_ilk, b_son, b_son - b_ilk))

# --- sabit izgaranin faz hatasi
periyot = 60.0 / bpm
# ilk vurus: ilk 4 saniyedeki en guclu onset
ilk = int(np.argmax(akis[:int(4 * FPS)])) / FPS
vurus = np.arange(ilk, sure, periyot)
onset_idx = np.where(akis > np.percentile(akis, 92))[0] / FPS
hatalar = []
for v in vurus:
    if len(onset_idx) == 0:
        break
    d = onset_idx - v
    j = int(np.argmin(np.abs(d)))
    if abs(d[j]) < periyot / 2:
        hatalar.append(d[j])
hatalar = np.array(hatalar)
print('\nSABIT IZGARA FAZ HATASI (%d vurus eslesti)' % len(hatalar))
if len(hatalar) > 20:
    ceyrek = len(hatalar) // 4
    for i in range(4):
        dilim = hatalar[i * ceyrek:(i + 1) * ceyrek]
        print('  %d. ceyrek ortalama hata: %+7.1f ms' % (i + 1, dilim.mean() * 1000))
    egim = np.polyfit(np.arange(len(hatalar)), hatalar, 1)[0] * 1000
    print('  vurus basina birikme    : %+.2f ms/vurus' % egim)
    print('  parca sonunda toplam    : %+.0f ms' % (egim * len(hatalar)))
    print('  bir vurus               : %.0f ms' % (periyot * 1000))
    if abs(egim * len(hatalar)) > periyot * 1000 * 0.25:
        print('\n  SONUC: TEMPO KAYIYOR - sabit izgara tutmaz.')
    else:
        print('\n  SONUC: TEMPO SABIT - sabit izgara tutar.')
