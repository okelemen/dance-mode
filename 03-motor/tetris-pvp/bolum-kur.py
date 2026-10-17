"""TETRIS MODE PVP - tam bolum JSON'u (sahne4.html + efekt.py tek kaynak).

    python bolum-kur.py <cikti.json> [--bpm 133.0827]

Yapi (18 Eki 2026): REF-053 dongusu (kart -> 3-2-1 -> duvar buyur -> gecer), 3 tur x 15 duvar = 45 duvar / 90 poz
(duvar-listesi.json, poz-listesi-kur.py). Her sure VURUS katidir -> muzige kilitli (Victory Rush, hakem 133,08 BPM).
Duvar 28 vurus = 7 olcu (~12,6 sn, REF-053 ~12 sn). Toplam 1320 vurus = 330 olcu = ~9:55 (TALIMATLAR §11: ~10 dk).
SUBSCRIBE her 15 sn (TALIMATLAR §16 kural), tam ekran kartlara denk gelirse kartin bitisine kayar.
"""
import json, math, os, sys

BPM = float(sys.argv[sys.argv.index("--bpm") + 1]) if "--bpm" in sys.argv else 133.0827
V = 60 / BPM
r = lambda x: round(x, 4)
Z = {"kart": r(4 * V), "say": r(6 * V), "buyu": r(12 * V), "gec": r(2 * V), "sure": r(28 * V)}
KART = 8 * V

DUVAR = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "duvar-listesi.json"), encoding="utf-8"))
OVGU = ["GREAT!", "EXCELLENT!", "PERFECT!", "AWESOME!", "AMAZING!", "NICE MOVE!"]
TUR_KART = {1: ("ROUND 1", None), 2: ("ROUND 2", "SKILL CHECK"), 3: ("ROUND 3", "TIME TO GO ALL OUT!")}

kartlar, duvarlar = [], []
t = 0.0
kartlar.append({"t": r(t), "sure": r(KART), "tip": "vs"}); t += KART
for tur in (1, 2, 3):
    m, alt = TUR_KART[tur]
    k = {"t": r(t), "sure": r(KART), "tip": "tur", "tur": tur, "metin": m}
    if alt: k["alt"] = alt
    kartlar.append(k); t += KART
    if tur == 1:
        kartlar.append({"t": r(t), "sure": r(KART), "tip": "basla"}); t += KART
    for d in [x for x in DUVAR if x["tur"] == tur]:
        n = len(duvarlar) + 1
        duvarlar.append({"no": n, "tur": tur, "t0": r(t), "p1": d["p1"], "p2": d["p2"], "ovgu": OVGU[(n - 1) % len(OVGU)]})
        t += Z["sure"]
kartlar.append({"t": r(t), "sure": r(KART), "tip": "wrap"}); t += KART
kartlar.append({"t": r(t), "sure": r(12 * V), "tip": "abone"}); t += 12 * V
toplam_olcu = round(t / (4 * V))
assert abs(toplam_olcu * 4 * V - t) < 0.01, (t, toplam_olcu)

TAM = {"vs", "tur", "wrap", "abone"}; AS = 3.2
def bos(x):
    return not any(k["tip"] in TAM and x < k["t"] + k["sure"] and x + AS > k["t"] for k in kartlar)
abone, x = [], 15.0
while x + AS < t:
    u = x
    while not bos(u) and u + AS < t:
        u += 0.5
    if bos(u) and u + AS < t and (not abone or u - abone[-1] >= 10):
        abone.append(r(u))
    x += 15.0

b = {"seri": "TETRIS MODE PVP", "bolum": "tetris-pvp-01", "bpm": BPM, "toplam_olcu": toplam_olcu,
     "toplam_duvar": len(duvarlar), "zaman": Z, "kartlar": kartlar, "duvarlar": duvarlar,
     "abone": abone, "abone_sure": AS, "muzik": "Victory Rush.wav (Suno, kullanici)",
     "_not": "Uretici: 03-motor/tetris-pvp/bolum-kur.py. Motor 03-motor/sahne4.html."}
json.dump(b, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{sys.argv[1]}: {len(duvarlar)} duvar, {len(abone)} SUBSCRIBE, {toplam_olcu} olcu = {t:.1f} sn ({int(t // 60)}:{t % 60:04.1f})")
