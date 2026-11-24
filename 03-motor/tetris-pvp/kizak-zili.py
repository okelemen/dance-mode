"""Kizak zili (sleigh bells) katmani: muzigin vurus izgarasina kilitli sentez, dizili muzikle karistirir.

    python kizak-zili.py <dizili.wav> <cikti.wav> --bpm 130 --ilk 0 [--db -12] [--zil-wav zil.wav]

Christmas videolari icin (HT38, 24 Kas 2026). Disaridan ses indirilmez (TALIMATLAR §4 Ses).
Her 16'lik bir "sallama": 5-8 kucuk zil boncugu, her biri inharmonik metal kismilerin toplami, 1-14 ms dagilmis,
hizli sonumlu; uzerine 4-12 kHz gurultu tisi. Vurgu: 2 ve 4'te tam, diger dortlukler orta, ara 16'liklar hafif.
--ilk = dizili dosyada ilk olcu cizgisi (muzik-diz-izgara.py ciktisi olcu cizgisinden baslar -> 0).
"""
import sys
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

m_yol, cikti = sys.argv[1:3]
arg = lambda ad, v=None: sys.argv[sys.argv.index(ad) + 1] if ad in sys.argv else v
BPM, ILK, DB = float(arg("--bpm")), float(arg("--ilk", 0)), float(arg("--db", -12))
x, sr = sf.read(m_yol, dtype="float32", always_2d=True)
n = len(x)
rng = np.random.default_rng(38)


ZILLER = [(f0, [1.0, 2.32, 3.87, 5.6]) for f0 in (2350, 2780, 3120, 3510, 3960, 4400)]  # sabit zil takimi, inharmonik


def boncuk(sure=0.35):
    t = np.arange(int(sure * sr)) / sr
    s = np.zeros_like(t)
    f0, oranlar = ZILLER[rng.integers(len(ZILLER))]
    for k, o in enumerate(oranlar):
        tau = rng.uniform(0.06, 0.14) / (1 + 0.6 * k)  # zil calar: uzun cinlama
        s += np.sin(2 * np.pi * f0 * o * t + rng.uniform(0, 6.28)) * np.exp(-t / tau) / (1 + k)
    return s


def sallama(guc):
    L = int(0.4 * sr)
    s = np.zeros(L)
    for _ in range(rng.integers(5, 9)):
        b = boncuk()
        d = int(rng.uniform(0.001, 0.014) * sr)
        s[d:d + len(b)] += b[:L - d] * rng.uniform(0.5, 1)
    tis = sosfilt(butter(4, [4000, 12000], "bandpass", fs=sr, output="sos"), rng.standard_normal(L))
    s += tis * np.exp(-np.arange(L) / sr / 0.015) * 0.25
    return s / (np.abs(s).max() + 1e-9) * guc


zil = np.zeros(n)
on6 = 60 / BPM / 4
i = 0
while True:
    t0 = ILK + i * on6
    if t0 >= n / sr - 0.15:
        break
    poz = i % 16
    guc = 1.0 if poz in (4, 12) else 0.7 if poz % 4 == 0 else 0.45
    guc *= rng.uniform(0.85, 1.0)
    jit = rng.normal(0, 0.003)  # insan eli gibi hafif kayma
    s = sallama(guc)
    a = max(0, int((t0 + jit) * sr))
    e = min(n, a + len(s))
    zil[a:e] += s[:e - a]
    i += 1

zil = sosfilt(butter(2, 2200, "highpass", fs=sr, output="sos"), zil)
# hedef: zil RMS = muzik RMS + DB
mr = np.sqrt((x ** 2).mean()); zr = np.sqrt((zil ** 2).mean())
zil *= mr / zr * 10 ** (DB / 20)
f = int(0.6 * sr); zil[-f:] *= np.linspace(1, 0, f)
st = np.stack([zil * 0.9, zil * 1.0], 1)  # hafif saga
if arg("--zil-wav"):
    sf.write(arg("--zil-wav"), st.astype("float32"), sr)
out = x + st
pk = np.abs(out).max()
if pk > 0.98:
    out *= 0.98 / pk
sf.write(cikti, out.astype("float32"), sr)
print(f"-> {cikti}  {n / sr:.2f} sn, 16'lik {i}, zil {DB:+.0f} dB (RMS, muzige gore), tepe {20 * np.log10(np.abs(out).max()):.1f} dBFS")
