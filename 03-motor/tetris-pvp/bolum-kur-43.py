"""HUMAN TETRIS 43 bolum JSON'u (REF-095 yapi, 1P SOLO, gunduz dinozor vadisi) - bolum-kur-39.py'den; ozel tur MIRROR
(39 MIRROR, 40 BLIND, 41 SPEED, 42 FREEZE -> 43 MIRROR; en son 39). Giris KANCA + volkan pufu, altin yumurta catlar, Baku cikar (motor 40).

    python bolum-kur-43.py   ->  bolumler/tetris-mode-43.json

SURE 3:15-3:20 (TALIMATLAR §3) -> 100 olcu = 3:16,7 (122 BPM; Twin Runway Bend Duel, HT21 sabit surum, dizili 8-14/16-22/24-30 bloklari):
  acilis 2 olcu (kanca + yumurta acilisi; ilk duvar <= 5 sn; mobil paket md. 1)
  normal duvar 14 vurus = 6,9 sn: kart 2 / say 8 / buyu 2 / gec 2 (122 BPM yavas -> dongu kisaltildi, 24 duvar korundu)
  MIRROR turu (6 duvar) 15 vurus: kart 2 / say 9 / buyu 2 / gec 2 (ters siluet icin bir vurus fazla say; d.ayna)
  tur kartlari (ROUND 2, MIRROR ROUND, FINAL ROUND, BOSS WALL) 1'er olcu
  BOSS WALL 24 vurus: kart 2 / say 10 / buyu 6 / gec 6
  sonuc 2 + RUTBE 2 + abone 2 olcu
SOLO: tek sporcu (PURPLE). Gec kalirsa duvar onu camur birikintisine iter, kayar (OUT), o duvar sayilmaz. Sayac WALLS CLEARED n/24.
OUT: 5 (R1), 14 (MIRROR), 21 (FINAL) -> 21/24 = SILVER. BOSS WALL gecilir (son duvar zafer). Rutbe adlari BRONZE / SILVER / GOLDEN EGG.
"""
import json, os

BURA = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.abspath(os.path.join(BURA, "..", ".."))
BPM = 122.0
V = 60 / BPM; O = 4 * V
DUVAR = json.load(open(os.path.join(BURA, "duvar-listesi-43.json"), encoding="utf-8"))
assert len(DUVAR) == 24 and all("p1" in d and "p2" not in d for d in DUVAR)

Z_NORMAL = {"kart": 2, "say": 8, "buyu": 2, "gec": 2}
Z_AYNA = {"kart": 2, "say": 9, "buyu": 2, "gec": 2}
Z_BOSS = {"kart": 2, "say": 10, "buyu": 6, "gec": 6}
OUT = {5, 14, 21}
OVGU = ["PERFECT!", "NICE!", "GREAT!", "AMAZING!", "SUPER!", "WOW!"]

kartlar, duvarlar = [], []
def kart(vur, sure_olcu, **k):
    kartlar.append(dict(t=round(vur * V, 4), sure=round(sure_olcu * O, 4), **k))

kart(0, 2, tip="acilis", soru=True)
vur = 8
temiz = 0
plan = [(1, None, 6), (2, ("02", "ROUND 2"), 6), (3, ("03", "MIRROR ROUND", "EVERYTHING IS FLIPPED!"), 6),
        (4, ("04", "FINAL ROUND"), 5), (5, ("!", "BOSS WALL", "GO FOR THE GOLDEN EGG!"), 1)]
no = 0
for tur, tk, n in plan:
    if tk:
        kart(vur, 1, tip="tur", tur=min(tur, 4), metin=tk[0], alt=tk[1], ek=tk[2] if len(tk) > 2 else None, boss=tur == 5)
        vur += 4
    for j in range(n):
        d = DUVAR[no]; no += 1
        assert d["tur"] == min(tur, 4), (no, d["tur"])
        ayna = tur == 3
        Z = Z_BOSS if tur == 5 else Z_AYNA if ayna else Z_NORMAL
        out = {"p1": no in OUT}
        if not out["p1"]:
            temiz += 1
        z = {k: round(v * V, 4) for k, v in Z.items()}; z["sure"] = round(sum(Z.values()) * V, 4)
        duvarlar.append({"no": no, "tur": min(tur, 4), "t0": round(vur * V, 4), "z": z, "grup": d["p1"], "p1": d["p1"],
                         "out": out, "skor": temiz, "ovgu": OVGU[(no - 1) % len(OVGU)], "boss": tur == 5, "ayna": ayna,
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
assert TOPLAM == 100, TOPLAM                                   # muzik izgarasi 100 olcu
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
bolum = {"seri": "HUMAN TETRIS", "bolum": "human-tetris-43", "bpm": BPM, "toplam_olcu": TOPLAM, "toplam_duvar": len(duvarlar),
         "kartlar": kartlar, "duvarlar": duvarlar, "abone": abone, "abone_sure": 3.2,
         "muzik": "Twin Runway Bend Duel (Suno, HT21; hazir liste - kullanici 28 Kas) -> HT21 sabit surum twin-122.wav -> DANCE-MODE/01-muzik/human-tetris-43/twin-43-dizili.wav (122 BPM, 100 olcu, ilk 0,0786)",
         "_not": "Uretici: 03-motor/tetris-pvp/bolum-kur-43.py. Motor 03-motor/sahne40.html (1P SOLO, MIRROR, 2B T-rex yavrusu Baku, kanca + yumurta acilisi). REF-095 yapi, mekan dinozor vadisi (kullanici 28 Kas 2026).",
         "tema": {"varlik": "/03-motor/tetris-pvp/varlik-43s2/tetris-varlik/", "karakter": "/03-motor/tetris-pvp/varlik-43-karakter/",
                  "maskeVarlik": "/03-motor/tetris-pvp/varlik-43s1/", "maskeKlasor": "poz/",
                  "turAd": {"1": "ROUND 1", "2": "ROUND 2", "3": "MIRROR ROUND", "4": "FINAL ROUND"},
                  "aboneAlt": "NEW CHALLENGE EVERY DAY", "acilis": "kanca",
                  "renk": ["#9a3aff", "#ff2a7a"], "acik": ["#ead8ff", "#ffd6e6"], "koyu": ["#5a10b8", "#a8104a"], "ad": ["PURPLE", "PINK"]}}
yol = os.path.join(KOK, "bolumler", "tetris-mode-43.json")
json.dump(bolum, open(yol, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("->", yol, "olcu", TOPLAM, "sure %.2f sn" % SURE, "duvar", len(duvarlar), "abone", len(abone), "ilk duvar %.2f" % duvarlar[0]["t0"],
      "temiz", temiz, rutbe)
