"""KAYAN TEMPOYU SABITLER (17 Eyl 2026, Golden Groove icin yazildi).

Suno parcalari bazen hizlaniyor: Golden Groove 133,56 -> 135,52 BPM
(dakikada ~0,65). Tek oranli `atempo` bunu DUZELTMEZ - o sabit bir carpan
uygular, kaymayi oldugu gibi birakir. Motor sabit izgarayla calistigi icin
10 dakikada cue'lar gozle gorulur kayar.

Yontem:
1. Kick zarfinda 30 sn'lik pencerelerle yerel BPM olculur.
2. Olculen noktalara DOGRU oturtulur: BPM(t) = a + b*t.
3. Parca kisa dilimlere bolunur; her dilim `atempo = hedef / BPM(t)` ile
   esnetilir (tipik %0,3-1,5, kulakla duyulmaz).
4. Dilimler birlestirilir, sonuc yeniden olculur - duz cikmali.

   python muzik-tempo-duzelt.py <giris> <cikis.wav> [hedef_bpm]
"""
import subprocess, sys, os, tempfile
import numpy as np

SR = 22050
HOP = 256
DILIM = 2.0                      # saniye - kisa dilim = yumusak duzeltme


def kick_zarfi(yol):
    p = subprocess.run(['ffmpeg', '-v', 'error', '-i', yol, '-f', 'f32le',
                        '-ac', '1', '-ar', str(SR), '-'], stdout=subprocess.PIPE, check=True)
    x = np.frombuffer(p.stdout, dtype=np.float32).astype(np.float64)
    N = 1024
    S = np.abs(np.fft.rfft(np.lib.stride_tricks.sliding_window_view(x, N)[::HOP] * np.hanning(N), axis=1))
    k = np.maximum(0, np.diff(S[:, :10].sum(axis=1)))
    return k / (k.max() + 1e-9), (np.arange(len(k)) + 1) * HOP / SR, len(x) / SR


def yerel_bpm(kick, t, a, b, lo=131.0, hi=138.0, adim=0.01):
    m = (t >= a) & (t < b)
    tt, kk = t[m], kick[m]
    if kk.sum() < 1e-6:
        return None
    en = (0, 0)
    for B in np.arange(lo, hi, adim):
        per = 60.0 / B
        for f in np.arange(0, per, 0.004):
            d = np.abs(tt - (f + np.round((tt - f) / per) * per))
            s = (kk * np.exp(-(d / 0.022) ** 2)).sum()
            if s > en[0]:
                en = (s, B)
    return en[1]


def egri(yol):
    kick, t, sure = kick_zarfi(yol)
    nok = []
    for a in np.arange(0, sure - 20, 30):
        B = yerel_bpm(kick, t, a, min(a + 30, sure))
        if B:
            nok.append((a + 15, B))
    xs = np.array([p[0] for p in nok]); ys = np.array([p[1] for p in nok])
    b, a0 = np.polyfit(xs, ys, 1)
    return a0, b, nok, sure


def main():
    giris, cikis = sys.argv[1], sys.argv[2]
    hedef = float(sys.argv[3]) if len(sys.argv) > 3 else None
    a0, b, nok, sure = egri(giris)
    print('olculen yerel tempolar:')
    for x, y in nok:
        print('  %5.0f sn: %.2f BPM' % (x, y))
    print('dogru: BPM(t) = %.3f + %.5f*t   (parca boyu %.2f BPM kayma)' % (a0, b, b * sure))
    if hedef is None:
        hedef = round(a0 + b * sure / 2, 2)      # ortalama tempo
    print('hedef: %.3f BPM' % hedef)
    gecici = tempfile.mkdtemp()
    liste = os.path.join(gecici, 'liste.txt')
    parcalar = []
    n = int(np.ceil(sure / DILIM))
    for i in range(n):
        t0 = i * DILIM
        sn = min(DILIM, sure - t0)
        B = a0 + b * (t0 + sn / 2)
        oran = hedef / B                          # <1 ise yavaslatir
        out = os.path.join(gecici, 'p%04d.wav' % i)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '%.6f' % t0, '-t', '%.6f' % sn,
                        '-i', giris, '-filter:a', 'atempo=%.8f' % oran,
                        '-ac', '2', '-ar', '48000', '-c:a', 'pcm_s16le', out], check=True)
        parcalar.append(out)
    with open(liste, 'w', encoding='utf-8') as f:
        for p in parcalar:
            f.write("file '%s'\n" % p.replace('\\', '/'))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', liste,
                    '-ac', '2', '-ar', '48000', '-c:a', 'pcm_s16le', cikis], check=True)
    print('-> %s' % cikis)
    a1, b1, nok1, sure1 = egri(cikis)
    print('SONUC: BPM(t) = %.3f + %.5f*t  (kalan kayma %.2f BPM)' % (a1, b1, b1 * sure1))
    for x, y in nok1:
        print('  %5.0f sn: %.2f BPM' % (x, y))


if __name__ == '__main__':
    main()
