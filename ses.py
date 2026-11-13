"""KESIM SAYACI - ses: her kesime bir tahta/bicak tiki (plan JSON'undaki zamanlar).

python ses.py --plan plan-avokado.json --cikti ses/avokado.wav [--tik-ornek ses/tik_ornek.wav]
Kaynak tik: earshot bankasi fit/hit/bamboo_tok (CC0 kayittan, michorvath, freesound 386888).
Tik govdesi: alcak gecirgenle yumusatilir + kisa tahta 'tok' rezonansi eklenir.
"""
import argparse
import glob
import json
import wave

import numpy as np

SR = 48000


def oku(yol):
    with wave.open(yol) as w:
        n, ch, sw = w.getnframes(), w.getnchannels(), w.getsampwidth()
        ham = w.readframes(n)
    if sw == 3:
        b = np.frombuffer(ham, np.uint8).reshape(-1, 3)
        x = (b[:, 0].astype(np.int32) | (b[:, 1].astype(np.int32) << 8) | (b[:, 2].astype(np.int32) << 16))
        x = np.where(x >= 2 ** 23, x - 2 ** 24, x) / 2 ** 23
    else:
        x = np.frombuffer(ham, np.int16) / 32768.0
    return x.reshape(-1, ch).mean(1)


def yaz(yol, x):
    x = np.clip(x, -1, 1)
    st = np.stack([x, x], 1) if x.ndim == 1 else x
    with wave.open(yol, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())


def alcak(x, fc):
    # tek kutuplu iki kez (12 dB/okt)
    a = np.exp(-2 * np.pi * fc / SR)
    for _ in range(2):
        y = np.zeros_like(x); p = 0.0
        for i, v in enumerate(x):
            p = (1 - a) * v + a * p; y[i] = p
        x = y
    return x


def tik_yap(kaynak, rng):
    x = kaynak.copy()
    yum = alcak(x, rng.uniform(2200, 3200))
    t = np.arange(len(x)) / SR
    f0 = rng.uniform(170, 230)
    tok = np.sin(2 * np.pi * f0 * t) * np.exp(-t / 0.018) * 0.55
    tik = 0.75 * yum / (np.abs(yum).max() + 1e-9) + 0.25 * x / (np.abs(x).max() + 1e-9) + tok
    return tik / np.abs(tik).max()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True)
    ap.add_argument("--cikti", required=True)
    ap.add_argument("--tik-ornek")
    a = ap.parse_args()
    P = json.load(open(a.plan, encoding="utf-8"))
    rng = np.random.default_rng(11)
    kaynaklar = [oku(f) for f in sorted(glob.glob("ses/tik_[0-9].wav"))]
    tikler = [tik_yap(kaynaklar[i % len(kaynaklar)], rng) for i in range(8)]
    if a.tik_ornek:
        yaz(a.tik_ornek, np.concatenate([np.concatenate([t, np.zeros(SR // 3)]) for t in tikler]) * 0.7)
    N = int(P["sure"] * SR)
    sol, sag = np.zeros(N + SR), np.zeros(N + SR)
    for tur in P["turlar"]:
        for t, eks, konum, j in tur["kesimler"]:
            i = int(round(t * SR))
            tk = tikler[rng.integers(len(tikler))]
            g = rng.uniform(0.75, 1.0) * (0.9 if eks == "x" else 0.82)
            pan = rng.uniform(-0.15, 0.15)
            sol[i:i + len(tk)] += tk * g * (1 - pan)
            sag[i:i + len(tk)] += tk * g * (1 + pan)
    st = np.stack([sol[:N], sag[:N]], 1)
    st *= 10 ** (-1.5 / 20) / np.abs(st).max()  # tepe -1,5 dBFS (kodlama sonrasi < -1 dBTP payi)
    yaz(a.cikti, st)
    print("ses yazildi", a.cikti, len(st) / SR, "sn")
