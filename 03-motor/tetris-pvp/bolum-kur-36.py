"""HUMAN TETRIS 36 bolum JSON'u (REF-088 yapi, 1P SOLO, gunduz dev mantar ormani) - bolum-kur-35.py'den; ozel tur SPEED
(32 SPEED, 33 BLIND, 34 MIRROR, 35 FREEZE -> 36 SPEED; art arda ayni tur yok). Giris KANCA (motor TEMA.acilis='kanca').

    python bolum-kur-36.py   ->  bolumler/tetris-mode-36.json

SURE 3:15-3:20 (TALIMATLAR §3) -> 105 olcu = 3:16,1 (128,5 BPM; Linked Through The Ice Grid, HT15 sabit surum, dizili):
  acilis 2 olcu (kanca 2 sn + mantar acilisi; ilk duvar 3,74 sn; mobil paket md. 1)
  normal duvar 16 vurus = 7,5 sn: kart 2 / say 8 / buyu 3 / gec 3
  SPEED turu: ilk 2 duvar normal, son 4 duvar 12 vurus (kart 2 / say 6 / buyu 2 / gec 2) + FASTER!
  tur kartlari (ROUND 2, SPEED ROUND, FINAL ROUND, BOSS WALL) 1'er olcu
  BOSS WALL 20 vurus: kart 2 / say 10 / buyu 4 / gec 4
  sonuc 2 + RUTBE 2 + abone 2 olcu
SOLO: tek duvar, tek sporcu (BLUE). Gec kalirsa duvar onu dev mantar sapkasina iter (OUT), o duvar sayilmaz. Sayac WALLS CLEARED n/24.
OUT: 4 (R1), 16 (SPEED, hizlanan ilk duvar), 22 (FINAL) -> 21/24 = SILVER. BOSS WALL gecilir (son duvar zafer).
"""
import json, os

BURA = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.abspath(os.path.join(BURA, "..", ".."))
BPM = 128.5
V = 60 / BPM; O = 4 * V
DUVAR = json.load(open(os.path.join(BURA, "duvar-listesi-36.json"), encoding="utf-8"))
assert len(DUVAR) == 24 and all("p1" in d and "p2" not in d for d in DUVAR)

Z_NORMAL = {"kart": 2, "say": 8, "buyu": 3, "gec": 3}
Z_SPEED = {"kart": 2, "say": 6, "buyu": 2, "gec": 2}
Z_BOSS = {"kart": 2, "say": 10, "buyu": 4, "gec": 4}
OUT = {4, 16, 22}
OVGU = ["PERFECT!", "NICE!", "GREAT!", "AMAZING!", "SUPER!", "WOW!"]

kartlar, duvarlar = [], []
def kart(vur, sure_olcu, **k):
    kartlar.append(dict(t=round(vur * V, 4), sure=round(sure_olcu * O, 4), **k))

kart(0, 2, tip="acilis", soru=True)
vur = 8
temiz = 0
plan = [(1, None, 6), (2, ("02", "ROUND 2"), 6), (3, ("03", "SPEED ROUND", "FASTER AND FASTER!"), 6),
        (4, ("04", "FINAL ROUND"), 5), (5, ("!", "BOSS WALL", "GO FOR GOLD!"), 1)]
no = 0
for tur, tk, n in plan:
    if tk:
        kart(vur, 1, tip="tur", tur=min(tur, 4), metin=tk[0], alt=tk[1], ek=tk[2] if len(tk) > 2 else None, boss=tur == 5)
        vur += 4
    for j in range(n):
        d = DUVAR[no]; no += 1
        assert d["tur"] == min(tur, 4), (no, d["tur"])
        hiz = tur == 3 and j >= 2
        Z = Z_BOSS if tur == 5 else Z_SPEED if hiz else Z_NORMAL
        out = {"p1": no in OUT}
        if not out["p1"]:
            temiz += 1
        z = {k: round(v * V, 4) for k, v in Z.items()}; z["sure"] = round(sum(Z.values()) * V, 4)
        duvarlar.append({"no": no, "tur": min(tur, 4), "t0": round(vur * V, 4), "z": z, "grup": d["p1"], "p1": d["p1"],
                         "out": out, "skor": temiz, "ovgu": OVGU[(no - 1) % len(OVGU)], "boss": tur == 5, "hiz": hiz,
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
assert TOPLAM == 105, TOPLAM                                   # muzik izgarasi 105 olcu
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
bolum = {"seri": "HUMAN TETRIS", "bolum": "human-tetris-36", "bpm": BPM, "toplam_olcu": TOPLAM, "toplam_duvar": len(duvarlar),
         "kartlar": kartlar, "duvarlar": duvarlar, "abone": abone, "abone_sure": 3.2,
         "muzik": "Linked Through The Ice Grid (Suno, HUMAN TETRIS 15) -> HT15 sabit surum ice-grid-1285.wav -> DANCE-MODE/01-muzik/human-tetris-36/ice-36-dizili.wav (128,5 BPM, 105 olcu, ilk 1,469)",
         "_not": "Uretici: 03-motor/tetris-pvp/bolum-kur-36.py. Motor 03-motor/sahne33.html (1P SOLO, SPEED, baykus Olli, kanca girisi). REF-088 yapi, mekan bizden (kullanici 20 Kas 2026).",
         "tema": {"varlik": "/03-motor/tetris-pvp/varlik-36s1/", "karakter": "/03-motor/tetris-pvp/varlik-36-karakter/",
                  "maskeVarlik": "/03-motor/tetris-pvp/varlik-36s1/", "maskeKlasor": "poz/",
                  "turAd": {"1": "ROUND 1", "2": "ROUND 2", "3": "SPEED ROUND", "4": "FINAL ROUND"},
                  "aboneAlt": "NEW CHALLENGE EVERY DAY", "acilis": "kanca"}}
yol = os.path.join(KOK, "bolumler", "tetris-mode-36.json")
json.dump(bolum, open(yol, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("->", yol, "olcu", TOPLAM, "sure %.2f sn" % SURE, "duvar", len(duvarlar), "abone", len(abone), "ilk duvar %.2f" % duvarlar[0]["t0"],
      "temiz", temiz, rutbe)
