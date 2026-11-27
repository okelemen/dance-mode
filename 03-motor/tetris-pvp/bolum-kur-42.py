"""HUMAN TETRIS 42 bolum JSON'u (REF-094 yapi, 1v1, cilali 3D korsan gemisi guvertesi) - bolum-kur-37.py'den; ozel tur FREEZE
(38 FREEZE, 39 MIRROR, 40 BLIND, 41 SPEED -> 42 FREEZE; art arda ayni tur yok). FREEZE zamanlamasi bolum-kur-31/38 (Z.tut).
Giris KANCA + yelken acilisi (motor 39). SUBSCRIBE WALL yok (37'ye ozeldi). Rutbe karti yok (PvP: kazanan hazine sandigini acar).
SURE 3:15-3:20 (TALIMATLAR §3) -> 107 olcu = 3:19,07 (129 BPM, vurus 0,4651 sn, olcu 1,8605 sn; Two Through The Light Tunnel, ilk 0,5233):
  acilis (kanca + geri sarma + yelken + WHO WILL WIN THE TREASURE?) 2 olcu (ilk duvar 3,72 sn; mobil paket md. 1)
  normal duvar 14 vurus = 6,51 sn: kart 2 / say 7 / buyu 3 / gec 2 (40 olcutu)
  FREEZE duvari 18 vurus: kart 2 / say 7 / buyu 2 / tut 7 (3,26 sn; aciklamadaki "3 more seconds") / gec 0
  tur kartlari (ROUND 2, FREEZE ROUND, FINAL ROUND, BOSS WALL) 1'er olcu
  BOSS WALL 30 vurus: kart 2 / say 12 / buyu 6 / gec 10
  sonuc (kazanan + hazine sandigi) 4 + abone 3 olcu
Skor: BOSS'a kadar 20-20; BOSS WALL'da BLUE OUT -> PINK 21-20 (37'de BLUE kazanmisti). OUT P1 4/11/16(FREEZE)/24, P2 7/14(FREEZE)/20.
"""
import json, os

BURA = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.abspath(os.path.join(BURA, "..", ".."))
BPM = 129.0
V = 60 / BPM; O = 4 * V
DUVAR = json.load(open(os.path.join(BURA, "duvar-listesi-42.json"), encoding="utf-8"))
assert len(DUVAR) == 24

Z_NORMAL = {"kart": 2, "say": 7, "buyu": 3, "gec": 2}
Z_FREEZE = {"kart": 2, "say": 7, "buyu": 2, "tut": 7, "gec": 0}
Z_BOSS = {"kart": 2, "say": 12, "buyu": 6, "gec": 10}
OUT = {"p1": {4, 11, 16, 24}, "p2": {7, 14, 20}}         # PINK 21 - 20 BLUE (23. duvardan sonra 20-20; 14 ve 16 FREEZE turunda)
OVGU = ["PERFECT!", "NICE!", "GREAT!", "AMAZING!", "SUPER!", "WOW!"]

kartlar, duvarlar = [], []
def kart(vur, sure_olcu, **k):
    kartlar.append(dict(t=round(vur * V, 4), sure=round(sure_olcu * O, 4), **k))
def zz(Z):
    z = {k: round(v * V, 4) for k, v in Z.items()}; z["sure"] = round(sum(Z.values()) * V, 4); return z

kart(0, 2, tip="acilis", soru=True)
vur = 8
skor = {"p1": 0, "p2": 0}
plan = [(1, None, 6, Z_NORMAL), (2, ("02", "ROUND 2"), 6, Z_NORMAL), (3, ("03", "FREEZE ROUND", "HOLD STILL, SAILOR!"), 6, Z_FREEZE),
        (4, ("04", "FINAL ROUND"), 5, Z_NORMAL), (5, ("!", "BOSS WALL", "WINNER TAKES THE TREASURE"), 1, Z_BOSS)]
no = 0
for tur, tk, n, Z in plan:
    if tk:
        kart(vur, 1, tip="tur", tur=min(tur, 4), metin=tk[0], alt=tk[1], ek=tk[2] if len(tk) > 2 else None, boss=tur == 5)
        vur += 4
    for j in range(n):
        d = DUVAR[no]; no += 1
        out = {o: no in OUT[o] for o in ("p1", "p2")}
        for o in ("p1", "p2"):
            if not out[o]:
                skor[o] += 1
        duvarlar.append({"no": no, "tur": min(tur, 4), "t0": round(vur * V, 4), "z": zz(Z), "p1": d["p1"], "p2": d["p2"],
                         "out": out, "skor": dict(skor), "ovgu": OVGU[(no - 1) % len(OVGU)], "boss": tur == 5, "freeze": tur == 3,
                         "nasil": no <= 2})
        vur += sum(Z.values())
kazanan = "p1" if skor["p1"] > skor["p2"] else "p2"
assert skor == {"p1": 20, "p2": 21}, skor
assert duvarlar[-2]["skor"] == {"p1": 20, "p2": 20}, duvarlar[-2]["skor"]       # son tura kadar basa bas (mobil paket md. 2)
assert len(duvarlar) == 24
assert vur % 4 == 0, vur
kart(vur, 4, tip="sonuc", kazanan=kazanan, skor=skor, hazine=True); vur += 16
kart(vur, 3, tip="abone"); vur += 12
TOPLAM = vur // 4
assert TOPLAM == 107, TOPLAM
assert 195 <= TOPLAM * O <= 200, TOPLAM * O                  # 3:15-3:20 kurali
assert duvarlar[0]["t0"] <= 5.0, duvarlar[0]["t0"]          # mobil paket md. 1

# SUBSCRIBE her ~15 sn (TALIMATLAR §4), tam ekran kartlarda yok, gec/tut panelinde yok; 3,2 sn
SURE = TOPLAM * O
bos = lambda t: not any(k["t"] - 0.2 <= t <= k["t"] + k["sure"] + 0.2 or k["t"] <= t + 3.2 <= k["t"] + k["sure"] for k in kartlar) and \
    not any(d["t0"] + d["z"]["kart"] + d["z"]["say"] + d["z"]["buyu"] - 0.1 <= t + s <= d["t0"] + d["z"]["sure"] for d in duvarlar for s in (0, 3.2))
abone, t = [], 8.0
while t < SURE - 30:
    q = t
    while not bos(q) and q < t + 6:
        q += 0.1
    if bos(q):
        abone.append(round(q, 2)); t = q + 15
    else:
        t += 1
bolum = {"seri": "HUMAN TETRIS", "bolum": "human-tetris-42", "bpm": BPM, "toplam_olcu": TOPLAM, "toplam_duvar": 24,
         "kartlar": kartlar, "duvarlar": duvarlar, "abone": abone, "abone_sure": 3.2,
         "muzik": "Two Through The Light Tunnel (Suno; hazir liste - kullanici 28 Kas) -> HT13 sabit surum light-tunnel-129.wav -> DANCE-MODE/01-muzik/human-tetris-42/light-42-dizili.wav (129 BPM, 107 olcu, ilk 0,5233)",
         "_not": "Uretici: 03-motor/tetris-pvp/bolum-kur-42.py. Motor 03-motor/sahne39.html (korsan gemisi guvertesi, FREEZE, 2B papagan Pako hakem, kanca + yelken acilisi). Referans REF-094 (yapi), mekan bizden (kullanici 28 Kas 2026).",
         "tema": {"acilis": "kanca", "varlik": "/03-motor/tetris-pvp/varlik-42s1/tetris-varlik/", "karakter": "/03-motor/tetris-pvp/varlik-42-karakter/",
                  "maskeVarlik": "/03-motor/tetris-pvp/varlik-42s1/", "maskeKlasor": "poz/",
                  "turAd": {"1": "ROUND 1", "2": "ROUND 2", "3": "FREEZE ROUND", "4": "FINAL ROUND"},
                  "aboneAlt": "NEW BATTLE EVERY DAY"}}
yol = os.path.join(KOK, "bolumler", "tetris-mode-42.json")
json.dump(bolum, open(yol, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("->", yol, "olcu", TOPLAM, "sure %.2f sn" % SURE, "duvar", len(duvarlar), "abone", len(abone), abone[:4], "ilk duvar %.2f" % duvarlar[0]["t0"], "skor", skor)
