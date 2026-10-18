"""Suno parcasindaki tempo kaymasini duzeltir: yerel tempoyu olcer, ffmpeg rubberband ile sabit hedef BPM'ye ceker
(perde korunur). Yerel ses hazirlama (Masaustu CLAUDE.md md. 9 serbest).

    python muzik-sabitle.py <giris.wav> <cikti.wav> [--hedef 142.0]

Neden (18 Eki 2026, Starlight Sprint): parca basta 140,9, sonda 143,3 BPM - tek BPM ile duvar dongusu vuruştan kayiyordu.
Yontem: 20 sn pencerelerde (2,5 sn adim) onset otokorelasyonu -> yerel BPM; 2. derece egri; her 0,5 sn'de rubberband tempo
komutu (hedef / yerel). Cikti yeniden olculur: pencerelerin hepsi hedefe +-0,15 BPM icinde olmali.
"""
import os, subprocess, sys, tempfile
import numpy as np
import librosa

giris, cikti = sys.argv[1:3]
HEDEF = float(sys.argv[sys.argv.index("--hedef") + 1]) if "--hedef" in sys.argv else 142.0
HOP = 64


def yerel_tempo(yol, merkez):
    y, sr = librosa.load(yol, sr=22050)
    oe = librosa.onset.onset_strength(y=y, sr=sr, hop_length=HOP); fps = sr / HOP
    W, A = int(20 * fps), int(2.5 * fps)
    ts, bs = [], []
    for a in range(0, len(oe) - W, A):
        o = oe[a:a + W] - oe[a:a + W].mean(); ac = np.correlate(o, o, "full")[len(o) - 1:]
        en = None
        for bpm in np.arange(merkez - 6, merkez + 6, 0.02):
            s = 0.0
            for kat in (1, 2, 4, 8):
                L = kat * 60 / bpm * fps; i = int(L)
                if i + 1 < len(ac):
                    q = L - i; s += ac[i] * (1 - q) + ac[i + 1] * q
            if en is None or s > en[0]:
                en = (s, bpm)
        ts.append((a + W / 2) / fps); bs.append(en[1])
    return np.array(ts), np.array(bs), len(y) / sr


ts, bs, sure = yerel_tempo(giris, HEDEF)
egri = np.polyfit(ts, bs, 2)
print("yerel BPM:", " ".join(f"{t:.0f}s={b:.2f}" for t, b in zip(ts[::4], bs[::4])))
with tempfile.TemporaryDirectory() as td:
    cmd = os.path.join(td, "tempo.txt")
    with open(cmd, "w") as f:
        for t in np.arange(0, sure, 0.5):
            f.write(f"{t:.2f} rubberband tempo {HEDEF / np.polyval(egri, t):.6f};\n")
    ilk = HEDEF / np.polyval(egri, 0)
    # komut dosyasi goreli adla (Windows yolundaki ':' filtre sozdiziminde kaciyordu)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.abspath(giris), "-af",
                    f"asendcmd=f=tempo.txt,rubberband=tempo={ilk:.6f}:transients=crisp:detector=percussive",
                    "-c:a", "pcm_s16le", os.path.abspath(cikti)], check=True, cwd=td)
ts2, bs2, _ = yerel_tempo(cikti, HEDEF)
sapma = np.abs(bs2 - HEDEF)
print("cikti BPM :", " ".join(f"{t:.0f}s={b:.2f}" for t, b in zip(ts2[::4], bs2[::4])))
print(f"en buyuk sapma {sapma.max():.2f} BPM ({'TAMAM' if sapma.max() <= 0.15 else 'KONTROL ET'})")
