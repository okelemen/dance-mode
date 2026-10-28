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


def main():
    bolum, cikti = sys.argv[1:3]
    B = json.load(open(bolum, encoding="utf-8"))
    Z = B["zaman"]
    sure = B["toplam_olcu"] * 60 / B["bpm"] * 4
    ef = np.zeros(int(sure * SR) + SR)
    for k in B["kartlar"]:
        t = k["t"]
        if k["tip"] in ("vs", "giris"):          # 5. video: giris karti (3 PLAYERS) VS ile ayni carpisma
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
        elif k["tip"] == "wrap":
            yerlestir(ef, fanfar(1.2), t + 0.05, 1.0)
            yerlestir(ef, piril(0.8), t + 0.3, 0.8)
        elif k["tip"] == "abone":
            yerlestir(ef, ding(990, 0.25), t + 0.1, 0.6)
            yerlestir(ef, tik(), t + 1.2, 0.9)
            yerlestir(ef, ding(1760, 0.5), t + 1.25, 0.45)
    for d in B["duvarlar"]:
        t0 = d["t0"]
        a = t0 + Z["kart"]; b = a + Z["say"]; c = b + Z["buyu"]
        yerlestir(ef, ding(990, 0.2), t0 + 0.05, 0.5)                    # oyuncu kartlari pop
        if B.get("tema", {}).get("tekOyuncu"):                           # 10. video (REF-061): "!" uyarisinda alarm, sahne7 nabziyla ayni 3 vurus
            u0, ud = t0 + Z["kart"] * 0.5, Z["kart"] * 0.5
            for i in range(3):
                yerlestir(ef, bip(988, 0.12), u0 + ud * (1 + 4 * i) / 12 - 0.06, 0.8)
                yerlestir(ef, bip(740, 0.12), u0 + ud * (1 + 4 * i) / 12 + 0.08, 0.8)
        yerlestir(ef, ding(), a + 0.02, 0.6)                             # poz belirdi
        for i in range(3):
            yerlestir(ef, bip([660, 784, 988][i]), a + i * Z["say"] / 3 + 0.02, 0.9)    # 3-2-1 yukselen (sahne ile ayni adim)
        yerlestir(ef, vuus(Z["buyu"] * 0.6, True, 0.55), c - Z["buyu"] * 0.6)   # duvar yaklasiyor
        yerlestir(ef, vurus(), c - 0.05, 1.0)                            # en yakinda
        yerlestir(ef, vuus(0.6, False, 0.9), c)                          # icinden gecti
        yerlestir(ef, piril(), c + Z["gec"] * 0.35, 0.6)                 # ovgu
    # SUBSCRIBE hatirlatmasi (her ~15 sn, sahne4.html aboneCiz ile ayni zaman): giriste pop, 1,3 sn'de tik + zil
    for ta in B.get("abone", []):
        yerlestir(ef, ding(990, 0.2), ta + 0.05, 0.55)
        yerlestir(ef, tik(), ta + 1.3, 0.9)
        yerlestir(ef, ding(1760, 0.5), ta + 1.35, 0.5)
        yerlestir(ef, piril(0.5), ta + 1.4, 0.35)
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
