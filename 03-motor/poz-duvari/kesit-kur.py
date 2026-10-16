"""POZ DUVARI - bolum JSON'u uretir: kartlar, duvarlar, koc cumleleri (tek kaynak).

Sahne (sahne3.html) gorseli, koc-sesi.py sesi ayni JSON'dan kurar; boylece
konusma ile goruntu ayni zaman cizelgesine bagli kalir.

    python poz-duvari/kesit-kur.py <cikti.json> [--kesit]

--kesit: kullanicinin istedigi kisa, muziksiz kesit (16 Eki 2026):
         giris + TUR 1'den 6 duvar + TUR 2'den 2 duvar (kesit 2: ~70 sn).
"""
import json, math, sys

BPM = 120                       # muzik yok; olcu = 2 sn, render.js izgarasi
OLCU = 60 / BPM * 4
DUVAR = 7.0                     # bir duvarin toplam suresi (sn) - kesit 2: "tempoyu hizlandir"
# Kesit 2 (16 Eki 2026): tempo ~7 sn/duvar. Koc: poz adi (0,35) + kisa ipucu (1,25),
# ipucu penceresi say[0]-1,25 = 1,55 sn. Sayim 0,8 sn arayla.
ZAMAN = {"yaklas": 5.2, "goster": 0.3, "tut": 1.2, "gec": 0.4, "say": [2.8, 3.6, 4.4]}

TURLAR = [
    {"no": 1, "ad": "EASY", "renk": "#22d3ee"},
    {"no": 2, "ad": "MEDIUM", "renk": "#facc15"},
    {"no": 3, "ad": "HARD", "renk": "#fb923c"},
    {"no": 4, "ad": "FINAL", "renk": "#e879f9"},
]
TUR_KOC = {1: "Round one! Easy!", 2: "Round two! Medium!", 3: "Round three! Hard!", 4: "Final round!"}
OVGU = ["NICE!", "GREAT!", "PERFECT!", "AWESOME!", "SUPER!"]
OVGU_KOC = ["Nice!", "Great!", "Perfect!", "Awesome!", "Super!"]

# koc: poz adi + kisa ipucu (pencere 1,55 sn)
KOC = {
    1: ("Star!", None),
    2: ("High five!", "Touch hands up high!"),
    3: ("Rocket!", "Hands up high!"),
    4: ("Mirror!", "Outside arm out!"),
    5: ("Big arch!", "Inside hands up!"),
    6: ("Robot!", "One up, two down!"),
    13: ("Low and high!", "One low, two tall!"),
    14: ("Lunge twins!", "Lunge, arms up!"),
}


def kur(dizi):
    """dizi: [(tur, [(duvar_no, poz_no), ...]), ...]"""
    kartlar, duvarlar, koc = [], [], []
    t = 0.0
    kartlar += [
        {"t": 0.0, "sure": 2.5, "tip": "buyuk", "metin": "WELCOME", "alt": "POSE WALL", "renk": "#fb923c"},
        {"t": 2.5, "sure": 4.0, "tip": "nasil"},
        {"t": 6.5, "sure": 1.5, "tip": "buyuk", "metin": "READY?", "renk": "#4ade80"},
    ]
    koc += [
        {"t": 0.3, "metin": "Welcome to Pose Wall!"},
        {"t": 2.6, "metin": "Player one, pink wall. Player two, blue wall."},
        {"t": 5.2, "metin": "Match your pose!"},
        {"t": 6.6, "metin": "Ready?"},
    ]
    t = 8.0
    sayac = 0
    for tur, liste in dizi:
        kartlar.append({"t": t, "sure": 2.5, "tip": "tur", "tur": tur, "metin": f"ROUND {tur}"})
        koc.append({"t": t + 0.3, "metin": TUR_KOC[tur]})
        t += 2.5
        for no, poz in liste:
            ad, ipucu = KOC[poz]
            o = sayac % len(OVGU)
            duvarlar.append({"no": no, "poz": poz, "tur": tur, "t0": round(t, 3), "sure": DUVAR, "ovgu": OVGU[o]})
            koc.append({"t": round(t + 0.35, 3), "metin": ad})
            if ipucu:
                koc.append({"t": round(t + 1.25, 3), "metin": ipucu})
            for i, s in enumerate(ZAMAN["say"]):
                koc.append({"t": round(t + s + 0.05, 3), "metin": ["Three!", "Two!", "One!"][i], "kisa": True})
            koc.append({"t": round(t + ZAMAN["yaklas"] + 0.05, 3), "metin": "Hold it!", "kisa": True})
            koc.append({"t": round(t + ZAMAN["yaklas"] + ZAMAN["tut"] + 0.1, 3), "metin": OVGU_KOC[o], "kisa": True})
            t += DUVAR
            sayac += 1
    t += 0.5
    olcu = math.ceil(t / OLCU)
    return {
        "seri": "POSE WALL", "bolum": "pose-wall-01", "bpm": BPM, "toplam_olcu": olcu,
        "toplam_duvar": 38, "zaman": ZAMAN, "turlar": TURLAR,
        "kartlar": kartlar, "duvarlar": duvarlar, "koc": koc,
        "_not": "POZ DUVARI kesit (muziksiz). Uretici: 03-motor/poz-duvari/kesit-kur.py",
    }


if __name__ == "__main__":
    cikti = sys.argv[1]
    if "--kesit" in sys.argv:
        dizi = [(1, [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)]), (2, [(13, 13), (14, 14)])]
    else:
        raise SystemExit("tam bolum dizisi henuz yok - once kesit onayi")
    b = kur(dizi)
    with open(cikti, "w", encoding="utf-8") as f:
        json.dump(b, f, ensure_ascii=False, indent=1)
    print(f"{cikti}: {len(b['duvarlar'])} duvar, {len(b['koc'])} koc cumlesi, "
          f"{b['toplam_olcu']} olcu = {b['toplam_olcu'] * OLCU:.1f} sn")
