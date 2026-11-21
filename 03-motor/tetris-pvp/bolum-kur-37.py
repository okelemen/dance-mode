"""HUMAN TETRIS 37 bolum JSON'u (REF-089 yapi, 1v1, cilali 3D ucan gokyuzu adalari) - bolum-kur-33.py'den; ozel tur BLIND
(33 BLIND, 34 MIRROR, 35 FREEZE, 36 SPEED -> 37 BLIND). Giris KANCA. Motor 34 (sahne34.html).
SURE 3:15-3:20 (TALIMATLAR §3) -> 113 olcu = 3:16,5 (138 BPM, vurus 0,4348 sn, olcu 1,7391 sn; Nebula Grid, ilk 0,042):
  acilis (kanca + geri sarma + bulut perdesi / ada + WHO WILL WIN?) 2 olcu (ilk duvar 3,48 sn; mobil paket md. 1)
  normal duvar 15 vurus = 6,52 sn: kart 2 / say 8 / buyu 3 / gec 2
  BLIND duvari 16 vurus: kart 2 / say 9 (siluet son 1,5 sn'de) / buyu 3 / gec 2
  SUBSCRIBE WALL (kullanici 21 Kas: ilk dakikada gorunur abone cagrisi, A) R1'in 4. duvarindan sonra, 21 vurus: kart 2 / say 8 /
    buyu 3 / gec 8 (tam ekran yarim ekran dugme + LIKE/COMMENT/SHARE); skora sayilmaz, OUT yok, 24 duvarin disinda
  tur kartlari (ROUND 2, BLIND ROUND, FINAL ROUND, BOSS WALL) 1'er olcu
  BOSS WALL 20 vurus: kart 2 / say 10 / buyu 4 / gec 4
  sonuc 3 + RUTBE 3 + abone 3 olcu
Skor: son duvara kadar 20-20; BOSS WALL'da PINK OUT -> BLUE 21-20 (33'te PINK kazanmisti).
"""
import json, os

BURA = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.abspath(os.path.join(BURA, "..", ".."))
BPM = 138.0
V = 60 / BPM; O = 4 * V
DUVAR = json.load(open(os.path.join(BURA, "duvar-listesi-37.json"), encoding="utf-8"))
assert len(DUVAR) == 24

Z_NORMAL = {"kart": 2, "say": 8, "buyu": 3, "gec": 2}
Z_BLIND = {"kart": 2, "say": 9, "buyu": 3, "gec": 2}
Z_ABONE = {"kart": 2, "say": 8, "buyu": 3, "gec": 8}
Z_BOSS = {"kart": 2, "say": 10, "buyu": 4, "gec": 4}
OUT = {"p1": {5, 12, 19}, "p2": {3, 10, 16, 24}}          # BLUE 21 - 20 PINK (23. duvardan sonra 20-20; 16 BLIND turunda)
OVGU = ["PERFECT!", "NICE!", "GREAT!", "AMAZING!", "SUPER!", "WOW!"]
ABONE_SONRA = 4                                           # SUBSCRIBE WALL bu duvardan sonra (R1)

kartlar, duvarlar = [], []
def kart(vur, sure_olcu, **k):
    kartlar.append(dict(t=round(vur * V, 4), sure=round(sure_olcu * O, 4), **k))
def zz(Z):
    z = {k: round(v * V, 4) for k, v in Z.items()}; z["sure"] = round(sum(Z.values()) * V, 4); return z

kart(0, 2, tip="acilis", soru=True)
vur = 8
skor = {"p1": 0, "p2": 0}
plan = [(1, None, 6, Z_NORMAL), (2, ("02", "ROUND 2"), 6, Z_NORMAL), (3, ("03", "BLIND ROUND", "CLOUD COVER!"), 6, Z_BLIND),
        (4, ("04", "FINAL ROUND"), 5, Z_NORMAL), (5, ("!", "BOSS WALL", "WINNER TAKES IT ALL"), 1, Z_BOSS)]
no = 0
abone_duvar = None
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
                         "out": out, "skor": dict(skor), "ovgu": OVGU[(no - 1) % len(OVGU)], "boss": tur == 5, "blind": tur == 3,
                         "nasil": no <= 2})
        vur += sum(Z.values())
        if no == ABONE_SONRA:                             # SUBSCRIBE WALL: iki serit ayni poz, OUT yok, skor degismez
            abone_duvar = {"no": no, "tur": 1, "t0": round(vur * V, 4), "z": zz(Z_ABONE), "p1": "wide-stance-punch-up", "p2": "wide-stance-punch-up",
                           "out": {"p1": False, "p2": False}, "skor": dict(skor), "aboneDuvar": True, "boss": False, "blind": False, "nasil": False}
            duvarlar.append(abone_duvar)
            vur += sum(Z_ABONE.values())
kazanan = "p1" if skor["p1"] > skor["p2"] else "p2"
assert skor == {"p1": 21, "p2": 20}, skor
assert sum(1 for d in duvarlar if not d.get("aboneDuvar")) == 24
assert vur % 4 == 0, vur
kart(vur, 3, tip="sonuc", kazanan=kazanan, skor=skor); vur += 12
kart(vur, 3, tip="rutbe"); vur += 12
kart(vur, 3, tip="abone"); vur += 12
TOPLAM = vur // 4
assert TOPLAM == 113, TOPLAM
assert 195 <= TOPLAM * O <= 200, TOPLAM * O                  # 3:15-3:20 kurali
assert duvarlar[0]["t0"] <= 5.0, duvarlar[0]["t0"]          # mobil paket md. 1
ab0 = abone_duvar["t0"]; ab1 = ab0 + abone_duvar["z"]["sure"]
assert 28 <= ab0 and ab1 <= 50, (ab0, ab1)                   # kullanici: ilk dakika, 0:30-0:50 plani

# SUBSCRIBE her ~15 sn (TALIMATLAR §4), tam ekran kartlarda yok, gec panelinde yok, SUBSCRIBE WALL boyunca yok; 3,2 sn
SURE = TOPLAM * O
bos = lambda t: not any(k["t"] - 0.2 <= t <= k["t"] + k["sure"] + 0.2 or k["t"] <= t + 3.2 <= k["t"] + k["sure"] for k in kartlar) and \
    not any(d["t0"] + d["z"]["kart"] + d["z"]["say"] + d["z"]["buyu"] - 0.1 <= t + s <= d["t0"] + d["z"]["sure"] for d in duvarlar for s in (0, 3.2)) and \
    not (ab0 - 3.5 <= t <= ab1 + 6)
abone, t = [], 8.0
while t < SURE - 30:
    q = t
    while not bos(q) and q < t + 6:
        q += 0.1
    if bos(q):
        abone.append(round(q, 2)); t = q + 15
    else:
        t += 1
bolum = {"seri": "HUMAN TETRIS", "bolum": "human-tetris-37", "bpm": BPM, "toplam_olcu": TOPLAM, "toplam_duvar": 24,
         "kartlar": kartlar, "duvarlar": duvarlar, "abone": abone, "abone_sure": 3.2,
         "muzik": "Nebula Grid (HT17'den beri ilk, kullanici 21 Kas) -> 01-muzik/human-tetris-37/nebula-37-dizili.wav (138 BPM sabit, 113 olcu)",
         "_not": "Uretici: 03-motor/tetris-pvp/bolum-kur-37.py. Motor 03-motor/sahne34.html (ucan gokyuzu adalari, BLIND, SUBSCRIBE WALL, Kiko hakem). Referans REF-089 (yapi), mekan bizden (kullanici 21 Kas 2026).",
         "tema": {"acilis": "kanca", "varlik": "/03-motor/tetris-pvp/varlik-37s1/", "karakter": "/03-motor/tetris-pvp/varlik-37-karakter/",
                  "maskeVarlik": "/03-motor/tetris-pvp/varlik-37s1/", "turAd": {"1": "ROUND 1", "2": "ROUND 2", "3": "BLIND ROUND", "4": "FINAL ROUND"},
                  "aboneAlt": "NEW BATTLE EVERY DAY"}}
yol = os.path.join(KOK, "bolumler", "tetris-mode-37.json")
json.dump(bolum, open(yol, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("->", yol, "olcu", TOPLAM, "sure %.2f sn" % SURE, "duvar", len(duvarlar), "abone", len(abone), abone[:4], "ilk duvar %.2f" % duvarlar[0]["t0"],
      "SUBSCRIBE WALL %.1f-%.1f" % (ab0, ab1), "skor", skor)
