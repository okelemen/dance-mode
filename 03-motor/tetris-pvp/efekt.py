"""TETRIS MODE PVP - ses efektleri (sentez, indirme/telif yok). Zamanlar bolum JSON'undan (sahne4.html ile ayni kaynak).

    python efekt.py <bolum.json> <cikti.wav> [--muzik muzik.wav [--muzik-kazanc 0.5]]

Kullanici (17 Eki 2026): "ses efekti kesinlikle olacak". Sentez fonksiyonlari poz-duvari/efekt.py'den.
Olaylar: VS carpismasi, tur fanfari, 3-2-1-GO bipleri, oyuncu karti pop, duvar sayimi, yaklasan vuus,
en yakinda vurus + gecis vuusu, ovgu piriltisi, kapanis fanfari, SUBSCRIBE tik.
"""
import json, os, sys
import numpy as np
import soundfile as sf

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "poz-duvari"))
from efekt import SR, vuus, ding, bip, vurus, piril, zap, tik, fanfar, yerlestir  # noqa: E402


def duduk(sure=0.55):
    """25 (spor salonu): hakem duduk sesi - 2,9 kHz tasiyici, bilyeli titresim (~32 Hz genlik + frekans), hafif nefes gurultusu"""
    t = np.arange(int(sure * SR)) / SR
    tit = 0.5 + 0.5 * np.sin(2 * np.pi * 32 * t)
    f = 2900 + 120 * np.sin(2 * np.pi * 32 * t)
    faz = 2 * np.pi * np.cumsum(f) / SR
    x = (np.sin(faz) + 0.3 * np.sin(2 * faz)) * (0.55 + 0.45 * tit) + 0.08 * np.random.default_rng(7).standard_normal(len(t))
    zarf = np.minimum(1, t / 0.02) * np.minimum(1, (sure - t) / 0.08)
    return (x * zarf * 0.35).astype(np.float64)


def buz(sure=0.9):
    """25 FREEZE: buz cinlamasi - yuksek, inharmonik kristal kismi tonlar, uzun sonum"""
    t = np.arange(int(sure * SR)) / SR
    x = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * d) for f, a, d in ((2093, 0.5, 4), (3136, 0.35, 5), (4699, 0.25, 7), (6272, 0.15, 9)))
    return (x * np.minimum(1, t / 0.003) * 0.5).astype(np.float64)



def kum(sure=0.7):
    """26 (plaj): kuma dusus - boguk gumleme (90->45 Hz) + alcak geciren kum hisirtisi, hizli sonum"""
    t = np.arange(int(sure * SR)) / SR
    f = 90 * np.exp(-t * 3) + 45
    gum = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
    g = np.random.default_rng(11).standard_normal(len(t))
    k = np.exp(-np.arange(int(0.004 * SR)) / (0.0012 * SR)); g = np.convolve(g, k / k.sum(), "same")      # alcak geciren
    his = g * np.exp(-t * 6) * np.minimum(1, t / 0.01)
    return ((gum * 0.9 + his * 1.6) * 0.5).astype(np.float64)


def ayna(sure=0.8):
    """26 MIRROR: ayna isiltisi - yukari kayan iki ton (glissando) + parilti, siluet ters dondugunu duyurur"""
    t = np.arange(int(sure * SR)) / SR
    f = 880 * 2 ** (t / sure * 1.0)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.6 * np.sin(2 * np.pi * np.cumsum(f * 1.5) / SR)
    return (x * np.minimum(1, t / 0.02) * np.exp(-t * 2.5) * 0.3).astype(np.float64)


def kar(sure=0.8):
    """27 (karli zirve): kara gomulme - yumusak gumleme (80->40 Hz) + parlak toz kar hisirtisi (bant gecirgen, 2-6 kHz), kisa sonum"""
    t = np.arange(int(sure * SR)) / SR
    f = 80 * np.exp(-t * 4) + 40
    gum = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 10)
    g = np.random.default_rng(13).standard_normal(len(t))
    k1 = np.exp(-np.arange(int(0.002 * SR)) / (0.0004 * SR)); g1 = np.convolve(g, k1 / k1.sum(), "same")
    k2 = np.exp(-np.arange(int(0.006 * SR)) / (0.0015 * SR)); g2 = np.convolve(g, k2 / k2.sum(), "same")
    his = (g1 - g2) * np.exp(-t * 5) * np.minimum(1, t / 0.008)
    return ((gum * 0.85 + his * 2.2) * 0.5).astype(np.float64)


def ruzgar(sure=2.0):
    """27 BLIND: tipi ruzgari - alcak geciren gurultu, yavas yukselip alcalan uguldama (iki yavas LFO)"""
    t = np.arange(int(sure * SR)) / SR
    g = np.random.default_rng(17).standard_normal(len(t))
    k = np.exp(-np.arange(int(0.01 * SR)) / (0.003 * SR)); g = np.convolve(g, k / k.sum(), "same")
    lfo = 0.6 + 0.4 * np.sin(2 * np.pi * 0.7 * t) * np.sin(2 * np.pi * 0.23 * t + 1)
    zarf = np.minimum(1, t / 0.4) * np.minimum(1, (sure - t) / 0.5)
    return (g * lfo * zarf * 1.4).astype(np.float64)


def main():
    bolum, cikti = sys.argv[1:3]
    B = json.load(open(bolum, encoding="utf-8"))
    Z0 = B.get("zaman")                          # 24. video (motor 21): duvar basina dongu d["z"] (SPEED ROUND / BOSS WALL)
    sure = B["toplam_olcu"] * 60 / B["bpm"] * 4
    ef = np.zeros(int(sure * SR) + SR)
    for k in B["kartlar"]:
        t = k["t"]
        if k["tip"] in ("vs", "giris", "acilis"):          # 5. video: giris karti (3 PLAYERS) VS ile ayni carpisma
            yerlestir(ef, vuus(0.7, True, 0.9), t)
            yerlestir(ef, vurus(), t + 0.45, 1.0)
            yerlestir(ef, zap(0.4), t + 0.5, 0.7)
        elif k["tip"] == "tur":
            yerlestir(ef, vuus(0.5, True, 0.6), t)
            yerlestir(ef, fanfar(), t + 0.15, 0.9)
        elif k["tip"] == "basla":
            ad = k["sure"] / 4                                      # sahne4.html ile ayni adim
            for i in range(3):
                yerlestir(ef, bip(660, 0.18), t + i * ad + 0.02, 0.9)
            yerlestir(ef, bip(1320, 0.4), t + 3 * ad + 0.02, 1.0)
            yerlestir(ef, vurus(), t + 3 * ad + 0.02, 0.8)
        elif k["tip"] in ("sonuc", "rutbe"):    # 24: sonuc (kazanan) + rutbe kartlari
            yerlestir(ef, fanfar(1.2 if k["tip"] == "sonuc" else 1.0), t + 0.05, 1.0)
            yerlestir(ef, piril(0.8), t + 0.3, 0.8)
        elif k["tip"] == "wrap":
            yerlestir(ef, fanfar(1.2), t + 0.05, 1.0)
            yerlestir(ef, piril(0.8), t + 0.3, 0.8)
        elif k["tip"] == "abone":
            yerlestir(ef, ding(990, 0.25), t + 0.1, 0.6)
            yerlestir(ef, tik(), t + 1.2, 0.9)
            yerlestir(ef, ding(1760, 0.5), t + 1.25, 0.45)
    for d in B["duvarlar"]:
        t0 = d["t0"]
        Z = d.get("z") or Z0
        a = t0 + Z["kart"]; b = a + Z["say"]; c = b + Z["buyu"]; T = Z.get("tut", 0)   # 25: FREEZE tut evresi
        yerlestir(ef, ding(990, 0.2), t0 + 0.05, 0.5)                    # oyuncu kartlari pop
        if B.get("tema", {}).get("tekOyuncu"):                           # 10. video (REF-061): "!" uyarisinda alarm, sahne7 nabziyla ayni 3 vurus
            u0, ud = t0 + Z["kart"] * 0.5, Z["kart"] * 0.5
            for i in range(3):
                yerlestir(ef, bip(988, 0.12), u0 + ud * (1 + 4 * i) / 12 - 0.06, 0.8)
                yerlestir(ef, bip(740, 0.12), u0 + ud * (1 + 4 * i) / 12 + 0.08, 0.8)
        yerlestir(ef, ding(), a + 0.02, 0.6)                             # poz belirdi
        if d.get("ayna"):                                                # 26 MIRROR: siluet ters doner
            yerlestir(ef, ayna(), a + 0.02, 0.8)
        if d.get("blind"):                                               # 27 BLIND: tipi (siluet gizli), son 1,5 sn'de belirir -> buz cinlamasi
            yerlestir(ef, ruzgar(max(0.8, b - 1.5 - a + 0.3)), a, 0.55)
            yerlestir(ef, buz(), b - 1.5, 0.75)
        for i in range(3):
            yerlestir(ef, bip([660, 784, 988][i]), a + i * Z["say"] / 3 + 0.02, 0.9)    # 3-2-1 yukselen (sahne ile ayni adim)
        yerlestir(ef, vuus(Z["buyu"] * 0.6, True, 0.55), c - Z["buyu"] * 0.6)   # duvar yaklasiyor
        yerlestir(ef, vurus(), c - 0.05, 1.0)                            # en yakinda
        yerlestir(ef, vuus(0.6, False, 0.9), c)                          # icinden gecti
        out = [o for o in ("p1", "p2") if d.get("out", {}).get(o)]
        if out:                                                          # 24: OUT - karakter suya duser (sicrama) + alcak uyari
            yerlestir(ef, vuus(0.5, False, 1.0), c - Z["buyu"] * 0.25)
            yerlestir(ef, zap(0.35), c - Z["buyu"] * 0.2, 0.6)
            if "--kar" in sys.argv:                                       # 27: kar yiginina gomulur -> gumleme + toz kar + hakem duduk
                yerlestir(ef, kar(), c - 0.03, 1.0)
                yerlestir(ef, duduk(), c + 0.3, 0.7)
            elif "--kum" in sys.argv:                                       # 26: kuma yuvarlanir -> gumleme + kum + cankurtaran duduk
                yerlestir(ef, kum(), c - 0.03, 1.0)
                yerlestir(ef, duduk(), c + 0.3, 0.8)
            elif "--duduk" in sys.argv:                                   # 25: mindere duser -> hakem duduk
                yerlestir(ef, duduk(), c + 0.15, 0.9)
            else:
                yerlestir(ef, bip(330, 0.3), c + 0.25, 0.8)
        else:
            yerlestir(ef, piril(), c + T + Z["gec"] * 0.35, 0.6)         # ovgu (FREEZE'de tut sonrasi)
        if T:                                                             # 25 FREEZE: buz cinlamasi + her vuruste tik + sonda zil
            yerlestir(ef, buz(), c + 0.05, 0.8)
            v = 60 / B["bpm"]
            for i in range(1, int(round(T / v))):
                yerlestir(ef, tik(), c + i * v, 0.5)
            yerlestir(ef, ding(1568, 0.4), c + T - 0.05, 0.7)
    # SUBSCRIBE hatirlatmasi (her ~15 sn, sahne4.html aboneCiz ile ayni zaman): giriste pop, 1,3 sn'de tik + zil
    for ta in B.get("abone", []):
        yerlestir(ef, ding(990, 0.2), ta + 0.05, 0.55)
        yerlestir(ef, tik(), ta + 1.3, 0.9)
        yerlestir(ef, ding(1760, 0.5), ta + 1.35, 0.5)
        yerlestir(ef, piril(0.5), ta + 1.4, 0.35)
        if B.get("tema", {}).get("yildiz") or B.get("tema", {}).get("karakter"):   # 18. video: LIKE / COMMENT / SHARE dokunuslari (sahne15 begenSatiri, Masaustu md. 27)
            for i in range(3):
                yerlestir(ef, ding([1175, 1319, 1568][i], 0.15), ta + 1.75 + i * 0.32, 0.4)
    ef = ef[: int(sure * SR)]
    ef = ef / (np.max(np.abs(ef)) + 1e-9)
    eg = float(sys.argv[sys.argv.index("--efekt-kazanc") + 1]) if "--efekt-kazanc" in sys.argv else 0.5
    karisim = ef * eg
    if "--muzik" in sys.argv:
        # Kullanici (18 Eki 2026): "efekt duyulsun ... muzigin sesini kisip artiracagin yerleri sen ayarla".
        # Efekt zarfi muzigi kisar (sidechain ducking): hizli atak 15 ms, yavas birakma 350 ms; efekt yokken muzik tam.
        m, msr = sf.read(sys.argv[sys.argv.index("--muzik") + 1], dtype="float32", always_2d=True)
        assert msr == SR, f"muzik {msr} Hz, {SR} bekleniyor"
        m = np.pad(m, ((0, max(0, len(ef) - len(m))), (0, 0)))[: len(ef)]
        mg = float(sys.argv[sys.argv.index("--muzik-kazanc") + 1]) if "--muzik-kazanc" in sys.argv else 0.5
        kis = float(sys.argv[sys.argv.index("--kisma") + 1]) if "--kisma" in sys.argv else 0.55
        pen = int(0.03 * SR)
        env = np.convolve(np.abs(ef), np.ones(pen) / pen, mode="same")
        env = env / (np.percentile(env[env > 1e-4], 95) + 1e-9) if np.any(env > 1e-4) else env
        hedef = 1 - kis * np.clip(env * 2.5, 0, 1)
        # zarf takibi: bloklar halinde (her ornekte python dongusu yavas) 5 ms adim
        adim = int(0.005 * SR); g = np.ones(len(hedef)); son = 1.0
        a_at, a_bir = np.exp(-adim / (0.015 * SR)), np.exp(-adim / (0.35 * SR))
        for i in range(0, len(hedef), adim):
            h = hedef[i:i + adim].min()
            kk = a_at if h < son else a_bir
            son = kk * son + (1 - kk) * h
            g[i:i + adim] = son
        mb = m * (mg * g)[:, None]
        karisim = karisim[:, None] + mb
        if "--olcum" in sys.argv:
            rms = lambda v: 20 * np.log10(np.sqrt(np.mean(np.square(v))) + 1e-9)
            var = env > 0.2
            print(f"OLCUM efekt (calarken) {rms(ef[var] * eg):.1f} dBFS | muzik (efekt calarken) {rms(mb.mean(1)[var]):.1f} dBFS"
                  f" | muzik (efekt yokken) {rms(mb.mean(1)[~var]):.1f} dBFS | efekt/muzik farki {rms(ef[var] * eg) - rms(mb.mean(1)[var]):.1f} dB"
                  f" | efekt orani %{100 * var.mean():.0f}")
    karisim = karisim / (np.max(np.abs(karisim)) + 1e-9) * 0.89
    sf.write(cikti, karisim.astype(np.float32), SR, subtype="PCM_16")
    print(f"-> {cikti}  {sure:.1f} sn  {len(B['duvarlar'])} duvar, {len(B['kartlar'])} kart")


if __name__ == "__main__":
    main()
