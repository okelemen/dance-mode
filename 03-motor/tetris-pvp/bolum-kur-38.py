"""HUMAN TETRIS 38 bolum JSON'u (REF-090 yapi, 1P SOLO Christmas, alacakaranlik kurabiye koyu koprusu) - bolum-kur-36.py'den; ozel tur FREEZE
(34 MIRROR, 35 FREEZE, 36 SPEED, 37 BLIND -> 38 FREEZE; art arda ayni tur yok). Giris KANCA + dev hediye kutusu (motor 35).

    python bolum-kur-38.py   ->  bolumler/tetris-mode-38.json

SURE 3:15-3:20 (TALIMATLAR §3) -> 108 olcu = 3:19,4 (130 BPM; Golden Bridge Duel orijinal, HT14 sabit surum, dizili):
  acilis 2 olcu (kanca + hediye kutusu acilisi; ilk duvar 3,69 sn; mobil paket md. 1)
  normal duvar 15 vurus = 6,9 sn: kart 2 / say 8 / buyu 3 / gec 2
  FREEZE turu (6 duvar) 18 vurus: kart 2 / say 7 / buyu 2 / tut 7 (3,2 sn; FREEZE! + HOLD IT!) / gec 0
  tur kartlari (ROUND 2, FREEZE ROUND, FINAL ROUND, BOSS WALL) 1'er olcu
  BOSS WALL 21 vurus: kart 2 / say 10 / buyu 4 / gec 5
  sonuc 2 + RUTBE 2 + abone 2 olcu
SOLO: tek sporcu (RED). Gec kalirsa duvar onu krema kapli kar yiginina gomer (OUT), o duvar sayilmaz. Sayac WALLS CLEARED n/24.
OUT: 5 (R1), 14 (FREEZE, ikinci donma duvari), 21 (FINAL) -> 21/24 = SILVER. BOSS WALL gecilir (son duvar zafer).
"""
import json, os

BURA = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.abspath(os.path.join(BURA, "..", ".."))
BPM = 130.0
V = 60 / BPM; O = 4 * V
DUVAR = json.load(open(os.path.join(BURA, "duvar-listesi-38.json"), encoding="utf-8"))
assert len(DUVAR) == 24 and all("p1" in d and "p2" not in d for d in DUVAR)

Z_NORMAL = {"kart": 2, "say": 8, "buyu": 3, "gec": 2}
Z_FREEZE = {"kart": 2, "say": 7, "buyu": 2, "tut": 7, "gec": 0}   # tut 7 vurus = 3,2 sn
Z_BOSS = {"kart": 2, "say": 10, "buyu": 4, "gec": 5}
OUT = {5, 14, 21}
OVGU = ["PERFECT!", "NICE!", "GREAT!", "AMAZING!", "SUPER!", "WOW!"]

kartlar, duvarlar = [], []
def kart(vur, sure_olcu, **k):
    kartlar.append(dict(t=round(vur * V, 4), sure=round(sure_olcu * O, 4), **k))

kart(0, 2, tip="acilis", soru=True)
vur = 8
temiz = 0
plan = [(1, None, 6), (2, ("02", "ROUND 2"), 6), (3, ("03", "FREEZE ROUND", "FREEZE LIKE A SNOWMAN!"), 6),
        (4, ("04", "FINAL ROUND"), 5), (5, ("!", "BOSS WALL", "GO FOR THE GOLD STAR!"), 1)]
no = 0
for tur, tk, n in plan:
    if tk:
        kart(vur, 1, tip="tur", tur=min(tur, 4), metin=tk[0], alt=tk[1], ek=tk[2] if len(tk) > 2 else None, boss=tur == 5)
        vur += 4
    for j in range(n):
        d = DUVAR[no]; no += 1
        assert d["tur"] == min(tur, 4), (no, d["tur"])
        frz = tur == 3
        Z = Z_BOSS if tur == 5 else Z_FREEZE if frz else Z_NORMAL
        out = {"p1": no in OUT}
        if not out["p1"]:
            temiz += 1
        z = {k: round(v * V, 4) for k, v in Z.items()}; z["sure"] = round(sum(Z.values()) * V, 4)
        duvarlar.append({"no": no, "tur": min(tur, 4), "t0": round(vur * V, 4), "z": z, "grup": d["p1"], "p1": d["p1"],
                         "out": out, "skor": temiz, "ovgu": OVGU[(no - 1) % len(OVGU)], "boss": tur == 5, "freeze": frz,
                         "nasil": no <= 2})
        vur += sum(Z.values())
assert temiz == 21, temiz
assert not duvarlar[-1]["out"]["p1"]                         # BOSS gecilir
rutbe = "GOLD" if temiz == 24 else "SILVER" if temiz >= 18 else "BRONZE"
assert vur % 4 == 0, vur
kart(vur, 2, tip="sonuc", skor=temiz, toplam=len(duvarlar), rutbe=rutbe); vur += 8
kart(vur, 2, tip="rutbe"); vur += 8
kart(vur, 2, tip="abone"); vur += 8
TOPLAM = vur // 4
assert TOPLAM == 108, TOPLAM                                   # muzik izgarasi 108 olcu
assert 195 <= TOPLAM * O <= 200, TOPLAM * O                  # 3:15-3:20 kurali
assert duvarlar[0]["t0"] <= 5.0, duvarlar[0]["t0"]          # mobil paket md. 1

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
bolum = {"seri": "HUMAN TETRIS", "bolum": "human-tetris-38", "bpm": BPM, "toplam_olcu": TOPLAM, "toplam_duvar": len(duvarlar),
         "kartlar": kartlar, "duvarlar": duvarlar, "abone": abone, "abone_sure": 3.2,
         "muzik": "Golden Bridge Duel (Suno, HUMAN TETRIS 14; orijinal, zilsiz - kullanici 24 Kas) -> HT14 sabit surum golden-bridge-130.wav -> DANCE-MODE/01-muzik/human-tetris-38/golden-38-dizili.wav (130 BPM, 108 olcu, ilk 0,456)",
         "_not": "Uretici: 03-motor/tetris-pvp/bolum-kur-38.py. Motor 03-motor/sahne35.html (1P SOLO Christmas, FREEZE, 2B ren geyigi Pip, kanca + hediye kutusu). REF-090 yapi, mekan kurabiye koyu (kullanici 24 Kas 2026).",
         "tema": {"varlik": "/03-motor/tetris-pvp/varlik-38s2-m2/tetris-varlik/", "karakter": "/03-motor/tetris-pvp/varlik-38-karakter/",
                  "maskeVarlik": "/03-motor/tetris-pvp/varlik-38s1/", "maskeKlasor": "poz/",
                  "turAd": {"1": "ROUND 1", "2": "ROUND 2", "3": "FREEZE ROUND", "4": "FINAL ROUND"},
                  "aboneAlt": "NEW CHALLENGE EVERY DAY", "acilis": "kanca",
                  "renk": ["#ff2a3a", "#20c850"], "acik": ["#ffd6da", "#d6ffe0"], "koyu": ["#b00818", "#0a7a28"], "ad": ["RED", "GREEN"]}}
yol = os.path.join(KOK, "bolumler", "tetris-mode-38.json")
json.dump(bolum, open(yol, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("->", yol, "olcu", TOPLAM, "sure %.2f sn" % SURE, "duvar", len(duvarlar), "abone", len(abone), "ilk duvar %.2f" % duvarlar[0]["t0"],
      "temiz", temiz, rutbe)
