"""HUMAN TETRIS 41 bolum JSON'u (REF-093 yapi, 1P SOLO, gunduz col vahasi) - bolum-kur-40.py'den; ozel tur SPEED
(37 BLIND, 38 FREEZE, 39 MIRROR, 40 BLIND -> 41 SPEED; en son 36). Giris KANCA + ruzgar kum tepesini kaydirir, altindan yazi (motor 38).

    python bolum-kur-41.py   ->  bolumler/tetris-mode-41.json

SURE 3:15-3:20 (TALIMATLAR §3) -> 109 olcu = 3:18,2 (132 BPM; Mirrorball Showdown, HT28 sabit surum, dizili 12-30,66-93,32-61,12-30,77-94):
  acilis 2 olcu (kanca + kum tepesi acilisi; ilk duvar <= 5 sn; mobil paket md. 1)
  normal duvar 16 vurus = 7,27 sn: kart 2 / say 9 / buyu 3 / gec 2
  SPEED turu: ilk 2 duvar normal, son 4 duvar 12 vurus (kart 2 / say 6 / buyu 2 / gec 2) + FASTER! (36 olcutu, d.hiz)
  tur kartlari (ROUND 2, SPEED ROUND, FINAL ROUND, BOSS WALL) 1'er olcu
  BOSS WALL 28 vurus: kart 2 / say 12 / buyu 6 / gec 8 (109 olcuye tamamlamak icin 40'tan 1 olcu uzun)
  sonuc 3 + RUTBE 2 + abone 3 olcu
SOLO: tek sporcu (BLUE). Gec kalirsa duvar onu kum tepesine iter, asagi yuvarlanir (OUT), o duvar sayilmaz. Sayac WALLS CLEARED n/24.
OUT: 3 (R1), 17 (SPEED, hizlanan duvar), 22 (FINAL) -> 21/24 = SILVER. BOSS WALL gecilir (son duvar zafer).
"""
import json, os

BURA = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.abspath(os.path.join(BURA, "..", ".."))
BPM = 132.0
V = 60 / BPM; O = 4 * V
DUVAR = json.load(open(os.path.join(BURA, "duvar-listesi-41.json"), encoding="utf-8"))
assert len(DUVAR) == 24 and all("p1" in d and "p2" not in d for d in DUVAR)

Z_NORMAL = {"kart": 2, "say": 9, "buyu": 3, "gec": 2}
Z_SPEED = {"kart": 2, "say": 6, "buyu": 2, "gec": 2}
Z_BOSS = {"kart": 2, "say": 12, "buyu": 6, "gec": 8}
OUT = {3, 17, 22}
OVGU = ["PERFECT!", "NICE!", "GREAT!", "AMAZING!", "SUPER!", "WOW!"]

kartlar, duvarlar = [], []
def kart(vur, sure_olcu, **k):
    kartlar.append(dict(t=round(vur * V, 4), sure=round(sure_olcu * O, 4), **k))

kart(0, 2, tip="acilis", soru=True)
vur = 8
temiz = 0
plan = [(1, None, 6), (2, ("02", "ROUND 2"), 6), (3, ("03", "SPEED ROUND", "FASTER AND FASTER!"), 6),
        (4, ("04", "FINAL ROUND"), 5), (5, ("!", "BOSS WALL", "GO FOR THE GOLDEN DUNE!"), 1)]
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
kart(vur, 3, tip="sonuc", skor=temiz, toplam=len(duvarlar), rutbe=rutbe); vur += 12
kart(vur, 2, tip="rutbe"); vur += 8
kart(vur, 3, tip="abone"); vur += 12
TOPLAM = vur // 4
assert TOPLAM == 109, TOPLAM                                   # muzik izgarasi 109 olcu
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
bolum = {"seri": "HUMAN TETRIS", "bolum": "human-tetris-41", "bpm": BPM, "toplam_olcu": TOPLAM, "toplam_duvar": len(duvarlar),
         "kartlar": kartlar, "duvarlar": duvarlar, "abone": abone, "abone_sure": 3.2,
         "muzik": "Mirrorball Showdown (Suno; hazir liste - kullanici 27 Kas) -> HT28 sabit surum mirror-132.wav -> DANCE-MODE/01-muzik/human-tetris-41/mirror-41-dizili.wav (132 BPM, 109 olcu, ilk 0,302)",
         "_not": "Uretici: 03-motor/tetris-pvp/bolum-kur-41.py. Motor 03-motor/sahne38.html (1P SOLO, SPEED, 2B fennek Fino, kanca + kum tepesi acilisi). REF-093 yapi, mekan col vahasi (kullanici 27 Kas 2026).",
         "tema": {"varlik": "/03-motor/tetris-pvp/varlik-41s2/tetris-varlik/", "karakter": "/03-motor/tetris-pvp/varlik-41-karakter/",
                  "maskeVarlik": "/03-motor/tetris-pvp/varlik-41s1/", "maskeKlasor": "poz/",
                  "turAd": {"1": "ROUND 1", "2": "ROUND 2", "3": "SPEED ROUND", "4": "FINAL ROUND"},
                  "aboneAlt": "NEW CHALLENGE EVERY DAY", "acilis": "kanca",
                  "renk": ["#1a8aff", "#ff2a7a"], "acik": ["#d0e8ff", "#ffd6e6"], "koyu": ["#0a4aa8", "#a8104a"], "ad": ["BLUE", "PINK"]}}
yol = os.path.join(KOK, "bolumler", "tetris-mode-41.json")
json.dump(bolum, open(yol, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("->", yol, "olcu", TOPLAM, "sure %.2f sn" % SURE, "duvar", len(duvarlar), "abone", len(abone), "ilk duvar %.2f" % duvarlar[0]["t0"],
      "temiz", temiz, rutbe)
