"""POZ DUVARI - ses efektleri (sentez) + koc sesiyle karisim.

Efektler dalga biciminden SENTEZLENIR (indirme yok, telif yok). Zamanlar bolum
JSON'undan (kartlar, duvarlar, zaman) - koc sesi ve goruntuyle ayni kaynak.
Kullanici (16 Eki 2026): "ses efektleri ... her geciste" -> TALIMATLAR §11.

    python efekt.py <bolum.json> <koc-sesi.wav> <cikti.wav> [--efekt-iz efekt.wav] [--muzik muzik.wav [--muzik-kazanc 0.5]]

Karisim: efektler koc konusurken kisilir (zarf takibi, -9 dB'e kadar), tepe -1 dBFS.
Muzik geldiginde ayni karisima ucuncu katman olarak eklenir.
"""
import json, sys
import numpy as np
import soundfile as sf

SR = 48000
rng = np.random.default_rng(51)


def zarf(n, atak, bitis):
    e = np.ones(n)
    a = max(1, int(atak * SR)); e[:a] = np.linspace(0, 1, a)
    return e * np.exp(-np.linspace(0, bitis, n))


def sin(f, sure, faz=0.0):
    t = np.arange(int(sure * SR)) / SR
    return np.sin(2 * np.pi * f * t + faz)


def gurultu(sure):
    return rng.standard_normal(int(sure * SR))


def filtre_bant(x, f0, f1):
    """basit FFT bant geciren (f0, f1 dizi olabilir: zamanla kayan tek bant icin parca parca)"""
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < f0) | (f > f1)] = 0
    return np.fft.irfft(X, len(x))


def vuus(sure=0.6, yukari=True, guc=1.0):
    """gurultu supurmesi: bandi zamanla kayan, parca parca filtreli"""
    n = int(sure * SR); out = np.zeros(n); P = 12
    g = gurultu(sure)
    for i in range(P):
        a, b = i * n // P, (i + 1) * n // P
        p = i / (P - 1)
        fc = (300 + 3500 * p) if yukari else (3800 - 3300 * p)
        out[a:b] = filtre_bant(g[a:b], fc * 0.6, fc * 1.6)
    e = np.sin(np.linspace(0, np.pi, n)) ** 1.5
    return out * e * guc / (np.max(np.abs(out)) + 1e-9)


def ding(f=1320, sure=0.45):
    x = sin(f, sure) + 0.5 * sin(f * 2.01, sure) + 0.25 * sin(f * 3.02, sure)
    return x * zarf(len(x), 0.002, 9) * 0.6


def bip(f, sure=0.14):
    x = np.sign(sin(f, sure)) * 0.35 + sin(f, sure) * 0.65
    return x * zarf(len(x), 0.003, 5) * 0.5


def vurus(sure=0.45):
    n = int(sure * SR); t = np.arange(n) / SR
    kick = np.sin(2 * np.pi * (55 + 120 * np.exp(-t * 30)) * t) * np.exp(-t * 9)
    cak = filtre_bant(gurultu(sure), 1500, 7000) * np.exp(-t * 25) * 0.6
    akor = (sin(523.25, sure) + sin(659.25, sure) + sin(783.99, sure)) / 3 * np.exp(-t * 6) * 0.5
    x = kick + cak + akor
    return x / np.max(np.abs(x))


def piril(sure=0.55):
    n = int(sure * SR); out = np.zeros(n)
    for i in range(9):
        f = 2000 + 2600 * rng.random()
        s = int(rng.random() * n * 0.6)
        b = ding(f, 0.18) * 0.5
        out[s:s + len(b)] += b[: n - s]
    return out


def zap(sure=0.3):
    n = int(sure * SR); t = np.arange(n) / SR
    f = 1800 * np.exp(-t * 8) + 300
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 10)
    x += filtre_bant(gurultu(sure), 3000, 9000) * np.exp(-t * 30) * 0.4
    return x * 0.6


def tik(sure=0.06):
    n = int(sure * SR); t = np.arange(n) / SR
    return filtre_bant(gurultu(sure), 2000, 8000) * np.exp(-t * 120) * 1.2


def fanfar(sure=0.9):
    out = np.zeros(int(sure * SR))
    for i, f in enumerate([523.25, 659.25, 783.99, 1046.5]):
        b = (sin(f, 0.5) + 0.4 * sin(f * 2, 0.5)) * zarf(int(0.5 * SR), 0.01, 4)
        s = int(i * 0.09 * SR)
        out[s:s + len(b)] += b[: len(out) - s] * 0.45
    return out


def yerlestir(iz, ses, t, kazanc=1.0):
    a = int(t * SR)
    if a >= len(iz): return
    b = min(len(iz), a + len(ses))
    iz[a:b] += ses[: b - a] * kazanc


def main():
    bolum, koc_yol, cikti = sys.argv[1:4]
    B = json.load(open(bolum, encoding="utf-8"))
    Z = B["zaman"]
    sure = B["toplam_olcu"] * 60 / B["bpm"] * 4
    ef = np.zeros(int(sure * SR) + SR)
    for k in B["kartlar"]:
        if k["tip"] == "tur" or k.get("metin") in ("CHALLENGE", "COMPLETE"):
            yerlestir(ef, fanfar(), k["t"] + 0.05, 0.9)
        elif k.get("metin") == "WELCOME":
            yerlestir(ef, vuus(0.8, True, 0.8), k["t"]); yerlestir(ef, fanfar(), k["t"] + 0.4, 0.8)
        elif k.get("metin") == "READY?":
            yerlestir(ef, bip(880, 0.25), k["t"] + 0.05, 0.8)
        elif k["tip"] == "son":
            yerlestir(ef, fanfar(1.2), k["t"] + 0.05, 1.0); yerlestir(ef, piril(0.8), k["t"] + 0.3, 0.8)
    for d in B["duvarlar"]:
        t0 = d["t0"]
        yerlestir(ef, vuus(0.55, True, 0.45), t0)                          # duvar belirdi
        yerlestir(ef, ding(), t0 + Z["goster"], 0.8)                        # poz açıldı
        for i, s in enumerate(Z["say"]):
            yerlestir(ef, bip([660, 784, 988][i]), t0 + s, 0.9)             # 3-2-1 yükselen
        yerlestir(ef, vurus(), t0 + Z["yaklas"], 1.0)                       # MATCH!
        if d.get("temas"):
            yerlestir(ef, zap(), t0 + Z["yaklas"] + 0.05, 0.7)              # temas kıvılcımı
        yerlestir(ef, vuus(0.5, False, 0.9), t0 + Z["yaklas"] + Z["tut"] - 0.05)  # yanından geçti
        yerlestir(ef, piril(), t0 + Z["yaklas"] + Z["tut"] + 0.15, 0.55)    # övgü
    # abone hatirlatmasi: girişte pop, 1,15 sn'de tik (sahne3.html aboneCiz ile ayni zaman)
    for ta in B.get("abone", []):
        yerlestir(ef, ding(990, 0.2) * 0.6, ta + 0.05, 0.5)
        yerlestir(ef, tik(), ta + 1.15, 0.9)
        yerlestir(ef, ding(1760, 0.5), ta + 1.2, 0.45)
    ef = ef[: int(sure * SR)]

    koc, ksr = sf.read(koc_yol, dtype="float32")
    if koc.ndim > 1: koc = koc.mean(axis=1)
    if ksr != SR:   # dogrusal yeniden ornekleme (konusma icin yeterli)
        x = np.arange(len(koc)) / ksr
        koc = np.interp(np.arange(int(len(koc) * SR / ksr)) / SR, x, koc).astype(np.float32)
    koc = np.pad(koc, (0, max(0, len(ef) - len(koc))))[: len(ef)]
    # koc zarfi -> efekt kisma
    pen = int(0.08 * SR)
    env = np.convolve(np.abs(koc), np.ones(pen) / pen, mode="same")
    env = env / (np.max(env) + 1e-9)
    kis = 1 - 0.65 * np.clip(env * 3, 0, 1)
    karisim = koc * 1.0 + ef * 0.42 * kis
    if "--muzik" in sys.argv:
        # MUZIK katmani (17 Eki 2026, kullanici: "konusma duyulmasi gerekiyor, ona gore ses ayarini yap").
        # Koc konusurken muzik ~-10 dB kisilir: hizli atak (30 ms), yavas birakma (350 ms).
        m, msr = sf.read(sys.argv[sys.argv.index("--muzik") + 1], dtype="float32", always_2d=True)
        assert msr == SR, f"muzik {msr} Hz, {SR} bekleniyor"
        m = np.pad(m, ((0, max(0, len(ef) - len(m))), (0, 0)))[: len(ef)]
        hedef = 1 - 0.68 * np.clip(env * 3, 0, 1)            # 1 -> ~0,32 (-10 dB)
        g = np.empty_like(hedef); g[0] = 1.0
        a_at, a_bir = np.exp(-1 / (0.03 * SR)), np.exp(-1 / (0.35 * SR))
        for i in range(1, len(hedef)):
            k_ = a_at if hedef[i] < g[i - 1] else a_bir
            g[i] = k_ * g[i - 1] + (1 - k_) * hedef[i]
        mg = float(sys.argv[sys.argv.index("--muzik-kazanc") + 1]) if "--muzik-kazanc" in sys.argv else 0.5
        karisim = karisim[:, None] + m * (mg * g)[:, None]       # stereo
        if "--olcum" in sys.argv:                                 # konusma netligi olcumu (kullanici: "konusma duyulmasi gerekiyor")
            kon = env > 0.15                                      # koc konusuyor
            rms = lambda x: 20 * np.log10(np.sqrt(np.mean(np.square(x))) + 1e-9)
            mb = (m * (mg * g)[:, None]).mean(axis=1)
            print(f"OLCUM koc (konusurken) {rms(koc[kon]):.1f} dBFS | muzik (koc konusurken) {rms(mb[kon]):.1f} dBFS"
                  f" | muzik (sessizken) {rms(mb[~kon]):.1f} dBFS | efekt {rms((ef * 0.42 * kis)[ef != 0]):.1f} dBFS"
                  f" | konusma/muzik farki {rms(koc[kon]) - rms(mb[kon]):.1f} dB | konusma orani %{100 * kon.mean():.0f}")
    karisim = karisim / (np.max(np.abs(karisim)) + 1e-9) * 0.89
    sf.write(cikti, karisim.astype(np.float32), SR, subtype="PCM_16")
    if "--efekt-iz" in sys.argv:
        sf.write(sys.argv[sys.argv.index("--efekt-iz") + 1], (ef / (np.max(np.abs(ef)) + 1e-9) * 0.89).astype(np.float32), SR, subtype="PCM_16")
    print(f"-> {cikti}  {sure:.1f} sn  efekt olaylari: {len(B['duvarlar'])} duvar x ~8 + kartlar")


if __name__ == "__main__":
    main()
