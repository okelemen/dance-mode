"""HUMAN TETRIS 40 bolum JSON'u (REF-092 yapi, 1P SOLO, gunduz donmus gol buz pateni) - bolum-kur-39.py'den; ozel tur BLIND
(36 SPEED, 37 BLIND, 38 FREEZE, 39 MIRROR -> 40 BLIND; en son 37). Giris KANCA + paten bicagi buza yazi oyar (motor 37).

    python bolum-kur-40.py   ->  bolumler/tetris-mode-40.json

SURE 3:15-3:20 (TALIMATLAR §3) -> 103 olcu = 3:17,8 (125 BPM; Neon Tunnel Wake-Up, HT10 sabit surum, dizili 10-24,28-35,48-60 x3,64-68):
  acilis 2 olcu (kanca + paten oyma; ilk duvar <= 5 sn; mobil paket md. 1)
  normal duvar 14 vurus = 6,72 sn: kart 2 / say 7 / buyu 3 / gec 2
  BLIND turu (6 duvar) 17 vurus: kart 2 / say 9 (siluet son 1,5 sn'de, kar firtinasi) / buyu 4 / gec 2 (d.blind)
  tur kartlari (ROUND 2, BLIND ROUND, FINAL ROUND, BOSS WALL) 1'er olcu
  BOSS WALL 24 vurus: kart 2 / say 11 / buyu 5 / gec 6
  sonuc 2 + RUTBE 2 + abone 2 olcu
SOLO: tek sporcu (RED). Gec kalirsa duvar onu buzda kaydirip kar yiginina gomer (OUT), o duvar sayilmaz. Sayac WALLS CLEARED n/24.
OUT: 5 (R1), 16 (BLIND), 21 (FINAL) -> 21/24 = SILVER. BOSS WALL gecilir (son duvar zafer).
"""
import json, os

BURA = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.abspath(os.path.join(BURA, "..", ".."))
BPM = 125.0
V = 60 / BPM; O = 4 * V
DUVAR = json.load(open(os.path.join(BURA, "duvar-listesi-40.json"), encoding="utf-8"))
assert len(DUVAR) == 24 and all("p1" in d and "p2" not in d for d in DUVAR)

Z_NORMAL = {"kart": 2, "say": 7, "buyu": 3, "gec": 2}
Z_KOR = {"kart": 2, "say": 9, "buyu": 4, "gec": 2}
Z_BOSS = {"kart": 2, "say": 11, "buyu": 5, "gec": 6}
OUT = {5, 16, 21}
OVGU = ["PERFECT!", "NICE!", "GREAT!", "AMAZING!", "SUPER!", "WOW!"]

kartlar, duvarlar = [], []
def kart(vur, sure_olcu, **k):
    kartlar.append(dict(t=round(vur * V, 4), sure=round(sure_olcu * O, 4), **k))

kart(0, 2, tip="acilis", soru=True)
vur = 8
temiz = 0
plan = [(1, None, 6), (2, ("02", "ROUND 2"), 6), (3, ("03", "BLIND ROUND", "SNOWSTORM INCOMING!"), 6),
        (4, ("04", "FINAL ROUND"), 5), (5, ("!", "BOSS WALL", "GO FOR THE GOLDEN SKATE!"), 1)]
no = 0
for tur, tk, n in plan:
    if tk:
        kart(vur, 1, tip="tur", tur=min(tur, 4), metin=tk[0], alt=tk[1], ek=tk[2] if len(tk) > 2 else None, boss=tur == 5)
        vur += 4
    for j in range(n):
        d = DUVAR[no]; no += 1
        assert d["tur"] == min(tur, 4), (no, d["tur"])
        kor = tur == 3
        Z = Z_BOSS if tur == 5 else Z_KOR if kor else Z_NORMAL
        out = {"p1": no in OUT}
        if not out["p1"]:
            temiz += 1
        z = {k: round(v * V, 4) for k, v in Z.items()}; z["sure"] = round(sum(Z.values()) * V, 4)
        duvarlar.append({"no": no, "tur": min(tur, 4), "t0": round(vur * V, 4), "z": z, "grup": d["p1"], "p1": d["p1"],
                         "out": out, "skor": temiz, "ovgu": OVGU[(no - 1) % len(OVGU)], "boss": tur == 5, "blind": kor,
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
assert TOPLAM == 103, TOPLAM                                   # muzik izgarasi 103 olcu
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
bolum = {"seri": "HUMAN TETRIS", "bolum": "human-tetris-40", "bpm": BPM, "toplam_olcu": TOPLAM, "toplam_duvar": len(duvarlar),
         "kartlar": kartlar, "duvarlar": duvarlar, "abone": abone, "abone_sure": 3.2,
         "muzik": "Neon Tunnel Wake-Up (Suno; hazir liste - kullanici 27 Kas) -> HT10 sabit surum neon-125.wav -> DANCE-MODE/01-muzik/human-tetris-40/neon-40-dizili.wav (125 BPM, 103 olcu)",
         "_not": "Uretici: 03-motor/tetris-pvp/bolum-kur-40.py. Motor 03-motor/sahne37.html (1P SOLO, BLIND, 2B fok Lumi, kanca + paten oyma). REF-092 yapi, mekan donmus gol (kullanici 27 Kas 2026).",
         "tema": {"varlik": "/03-motor/tetris-pvp/varlik-40s2/tetris-varlik/", "karakter": "/03-motor/tetris-pvp/varlik-40-karakter/",
                  "maskeVarlik": "/03-motor/tetris-pvp/varlik-40s1/", "maskeKlasor": "poz/",
                  "turAd": {"1": "ROUND 1", "2": "ROUND 2", "3": "BLIND ROUND", "4": "FINAL ROUND"},
                  "aboneAlt": "NEW CHALLENGE EVERY DAY", "acilis": "kanca",
                  "renk": ["#ff1a2a", "#1a8aff"], "acik": ["#ffd0d4", "#d0e8ff"], "koyu": ["#a8000e", "#0a4aa8"], "ad": ["RED", "BLUE"]}}
yol = os.path.join(KOK, "bolumler", "tetris-mode-40.json")
json.dump(bolum, open(yol, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("->", yol, "olcu", TOPLAM, "sure %.2f sn" % SURE, "duvar", len(duvarlar), "abone", len(abone), "ilk duvar %.2f" % duvarlar[0]["t0"],
      "temiz", temiz, rutbe)
