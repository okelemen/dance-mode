"""HUMAN TETRIS 28 bolum JSON'u (referanssiz, CO-OP 2 oyuncu, cilali 3D dev mutfak tezgahi) - bolum-kur-27.py'den; ozel tur FREEZE
(24 SPEED, 25 FREEZE, 26 MIRROR, 27 BLIND -> 28 FREEZE; art arda ayni tur yok).

    python bolum-kur-28.py   ->  bolumler/tetris-mode-28.json

SURE 3:15-3:20 (TALIMATLAR §3) -> 109 olcu = 3:18,2 (132 BPM, vurus 0,455 sn, olcu 1,818 sn):
  acilis 2 olcu (ilk duvar 3,64 sn; mobil paket md. 1)
  normal duvar 15 vurus = 6,82 sn: kart 2 / say 8 / buyu 3 / gec 2
  FREEZE duvari 18 vurus = 8,18 sn: kart 2 / say 7 / buyu 3 / tut 6 (2,73 sn; HOLD IT! 3-2-1) / gec 0 (tut biter, sonraki duvar)
  tur kartlari (ROUND 2, FREEZE ROUND, FINAL ROUND, BOSS WALL) 1'er olcu
  BOSS WALL 25 vurus: kart 2 / say 12 / buyu 5 / gec 6
  sonuc 2 + RUTBE 2 + abone 2 olcu
CO-OP: tek duvar, iki oyuncu ayni ikili pozu birlikte yapar. Biri gec kalirsa duvar ikisini dev jole kaselerine iter (OUT),
o duvar sayilmaz. Sayac WALLS CLEARED n/24. OUT: 6 (PINK gec), 14 (FREEZE, BLUE gec), 20 (FINAL, PINK gec) -> 21/24 = SILVER.
BOSS WALL gecilir (son duvar zafer).
"""
import json, os

BURA = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.abspath(os.path.join(BURA, "..", ".."))
BPM = 132.0
V = 60 / BPM; O = 4 * V
DUVAR = json.load(open(os.path.join(BURA, "duvar-listesi-28.json"), encoding="utf-8"))
assert len(DUVAR) == 24

Z_NORMAL = {"kart": 2, "say": 8, "buyu": 3, "gec": 2}       # 3:15-3:20 kurali (14 Kas 2026)
Z_FREEZE = {"kart": 2, "say": 7, "buyu": 3, "tut": 6, "gec": 0}   # 28: tut 2,73 sn
Z_BOSS = {"kart": 2, "say": 12, "buyu": 5, "gec": 6}
OUT = {6: "p2", 14: "p1", 20: "p2"}
OVGU = ["PERFECT!", "NICE!", "GREAT!", "AMAZING!", "SUPER!", "WOW!"]

kartlar, duvarlar = [], []
def kart(vur, sure_olcu, **k):                                  # konum vurus cinsinden (duvarlar olcu ortasinda bitebilir)
    kartlar.append(dict(t=round(vur * V, 4), sure=round(sure_olcu * O, 4), **k))

kart(0, 2, tip="acilis", soru=True)
vur = 8
temiz = 0
plan = [(1, None, 6, Z_NORMAL), (2, ("02", "ROUND 2"), 6, Z_NORMAL), (3, ("03", "FREEZE ROUND", "HOLD YOUR POSE!"), 6, Z_FREEZE),
        (4, ("04", "FINAL ROUND"), 5, Z_NORMAL), (5, ("!", "BOSS WALL", "CLEAR IT TOGETHER"), 1, Z_BOSS)]
no = 0
for tur, tk, n, Z in plan:
    if tk:
        kart(vur, 1, tip="tur", tur=min(tur, 4), metin=tk[0], alt=tk[1], ek=tk[2] if len(tk) > 2 else None, boss=tur == 5)
        vur += 4
    for _ in range(n):
        d = DUVAR[no]; no += 1
        assert d["tur"] == {1: "ROUND 1", 2: "ROUND 2", 3: "FREEZE ROUND", 4: "FINAL ROUND", 5: "FINAL ROUND"}[tur], (no, d["tur"])
        out = {o: OUT.get(no) == o for o in ("p1", "p2")}
        if not any(out.values()):
            temiz += 1
        z = {k: round(v * V, 4) for k, v in Z.items()}; z["sure"] = round(sum(Z.values()) * V, 4)
        duvarlar.append({"no": no, "tur": min(tur, 4), "t0": round(vur * V, 4), "z": z, "grup": d["grup"], "video": d["video"],
                         "out": out, "skor": temiz, "ovgu": OVGU[(no - 1) % len(OVGU)], "boss": tur == 5, "freeze": tur == 3,
                         "nasil": no <= 2})
        vur += sum(Z.values())
assert temiz == 21, temiz
rutbe = "GOLD" if temiz == 24 else "SILVER" if temiz >= 18 else "BRONZE"
assert vur % 4 == 0, vur                                     # kapanis kartlari olcu basinda
kart(vur, 2, tip="sonuc", skor=temiz, toplam=len(duvarlar), rutbe=rutbe); vur += 8
kart(vur, 2, tip="rutbe"); vur += 8
kart(vur, 2, tip="abone"); vur += 8
TOPLAM = vur // 4
assert TOPLAM == 109, TOPLAM
assert 195 <= TOPLAM * O <= 200, TOPLAM * O                  # 3:15-3:20 kurali
assert duvarlar[0]["t0"] <= 5.0, duvarlar[0]["t0"]          # mobil paket md. 1

# SUBSCRIBE her ~15 sn (TALIMATLAR §4), tam ekran kartlarda yok, gec panelinde yok; 3,2 sn
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
bolum = {"seri": "HUMAN TETRIS", "bolum": "human-tetris-28", "bpm": BPM, "toplam_olcu": TOPLAM, "toplam_duvar": len(duvarlar),
         "kartlar": kartlar, "duvarlar": duvarlar, "abone": abone, "abone_sure": 3.2,
         "muzik": "Mirrorball Showdown.wav (Suno, kullanici, 24 Eki 2026; HUMAN TETRIS 8de de) -> 01-muzik/human-tetris-28/mirror-132.wav (130->133 kayiyordu, 132 BPM sabit, sapma 0,34)",
         "_not": "Uretici: 03-motor/tetris-pvp/bolum-kur-28.py. Motor 03-motor/sahne25.html (CO-OP, FREEZE). Referanssiz (kullanici 15 Kas 2026).",
         "tema": {"varlik": "/03-motor/tetris-pvp/varlik-28s3/tetris-varlik/", "karakter": "/03-motor/tetris-pvp/varlik-28-karakter/",
                  "maskeVarlik": "/03-motor/tetris-pvp/varlik-28-grup/", "maskeKlasor": "",
                  "turAd": {"1": "ROUND 1", "2": "ROUND 2", "3": "FREEZE ROUND", "4": "FINAL ROUND"},
                  "aboneAlt": "NEW BATTLE EVERY DAY"}}
yol = os.path.join(KOK, "bolumler", "tetris-mode-28.json")
json.dump(bolum, open(yol, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("->", yol, "olcu", TOPLAM, "sure %.1f sn" % SURE, "duvar", len(duvarlar), "abone", len(abone), "ilk duvar %.2f" % duvarlar[0]["t0"],
      "temiz", temiz, rutbe)
