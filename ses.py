"""KESIM SAYACI - ses: her kesimde once avokadoyu kesme hisirtisi, sonra bicagin tahtaya vurusu.

python ses.py --plan plan-avokado.json --cikti ses/avokado.wav
Kaynak: Mixkit #136 "Cutting hard vegetables with knife" (Mixkit Sound Effects Free License,
https://mixkit.co/free-sound-effects/knife/). Kayittan kesme parcalari ve tahta vuruslari ayri kesildi
(earshot timeline ile bulunan anlar). Yatay (z) kesimde tahtaya vurus yok, yalniz kesme sesi.
"""
import argparse
import json
import subprocess

import numpy as np

SR = 48000
KAYNAK = "ses/mixkit-136.wav"
VURUS = [2.25, 4.66, 5.64, 6.96, 7.96, 9.56]                       # tahtaya vurus baslangiclari (sn)
KESME = [(0.12, 0.80), (3.28, 3.80), (6.42, 6.92), (7.62, 7.92), (8.90, 9.50)]  # kesme hisirtisi
TAHTA_UST = 0.14


def yukle(yol):
    ham = subprocess.run(["ffmpeg", "-v", "error", "-i", yol, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(ham, np.float32).astype(np.float64)


def yaz(yol, st):
    st = np.clip(st, -1, 1)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", yol],
                   input=st.astype(np.float32).tobytes(), check=True)


def parca(x, a, b):
    p = x[int(a * SR):int(b * SR)].copy()
    return p / (np.abs(p).max() + 1e-9)


def sar(p, giris=0.004, cikis=0.012):
    n = len(p)
    gi, ci = min(int(giris * SR), n // 2), min(int(cikis * SR), n // 2)
    if gi:
        p[:gi] *= np.linspace(0, 1, gi)
    if ci:
        p[-ci:] *= np.linspace(1, 0, ci)
    return p


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True)
    ap.add_argument("--cikti", required=True)
    a = ap.parse_args()
    P = json.load(open(a.plan, encoding="utf-8"))
    R = P["sekil"]["R"]
    MERKEZ_Z = TAHTA_UST + R - 0.03
    x = yukle(KAYNAK)
    rng = np.random.default_rng(5)
    N = int(P["sure"] * SR)
    sol, sag = np.zeros(N + SR), np.zeros(N + SR)

    def ekle(sinyal, t, g, pan):
        i = int(round(t * SR))
        if i < 0:
            sinyal = sinyal[-i:]
            i = 0
        n = min(len(sinyal), len(sol) - i)
        sol[i:i + n] += sinyal[:n] * g * (1 - pan)
        sag[i:i + n] += sinyal[:n] * g * (1 + pan)

    # her gorunur bicak vurusu = kayittaki TAM bir dograma ani (kesme + tahtaya inis birlikte, dogal zarf);
    # kisa kesme kirpintilari yok (cizirti yapiyordu). Yatay (z) vurus tahtaya inmez: yalniz kesme kismi.
    # earshot rank ("knife chopping through a vegetable onto a wooden cutting board"): en iyi 3 dograma
    tam = [sar(parca(x, h - 0.12, h + 0.22), 0.01, 0.06) for h in (4.66, 6.96, 9.56)]
    for tur in P["turlar"]:
        for t, eks, konum, adet in tur["vuruslar"]:
            pan = rng.uniform(-0.1, 0.1)
            g = rng.uniform(0.85, 1.0) * (1.0 if adet == 1 else 1.05)
            ekle(tam[rng.integers(len(tam))], t - 0.12, g * (0.8 if eks == "z" else 1.0), pan)
    # yeni meyve tahtaya duser (sahne.py DUSUS_ANAHTAR: temas 0.30 sn, sekme inisi 0.53 sn): tok + yumusak pof
    tok = yukle("ses/dusus_tok.wav")
    pof = yukle("ses/dusus_pof.wav")
    for tur in P["turlar"]:
        ekle(tok, tur["bas"] + 0.30, 1.0, 0.0)
        ekle(pof, tur["bas"] + 0.30, 0.8, 0.0)
        ekle(tok, tur["bas"] + 0.53, 0.35, 0.0)
    st = np.stack([sol[:N], sag[:N]], 1)
    st *= 10 ** (-1.5 / 20) / np.abs(st).max()
    yaz(a.cikti, st)
    print("ses yazildi", a.cikti, N / SR, "sn")
