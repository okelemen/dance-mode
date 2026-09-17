# Suno brief — 130 BPM hareketli (bölüm 09 · BAL / petek)

> Yazıldı: 17 Eylül 2026. Kullanıcı isteği: **130 BPM, hareketli.**
> Kural: her bölüm kendi müziğiyle çıkar (`docs/KURALLAR.md` md. 3a).
> Prompt **Style** alanına yapıştırılacak, şarkı sözü yok.

---

## Neden 130 bu bölüme uyuyor

HAR-004 kliplerinin pencereleri 130 BPM'de (ölçü 1,84615 sn) hızlanmadan oturuyor:

| Cue | Klip | Pencere (130 BPM) | Hız |
|---|---:|---:|---:|
| zıpla (alçak buz) | 2,40 sn | 1,5 ölçü = 2,77 sn | 0,87× |
| eğil (saçak) | 1,53 sn | 1 ölçü = 1,85 sn | 0,83× |
| it (buz paneli) | 1,60 sn | 1 ölçü = 1,85 sn | 0,87× |
| yan adım (levha) | 0,77 sn | 0,5 ölçü = 0,92 sn | 0,83× |

Hiçbiri 1,0×'ın üstüne çıkmıyor; yani hareketler hızlandırılmıyor, hafif
ağırlaşıyor — spor izleyicisi için doğru yön.

**Bölüm uzunluğu:** 330 ölçü = **609,2 sn = 10:09,2** (kural 9,5–10,5 dk ✔).

---

## STYLE ALANINA YAPIŞTIR

```
instrumental dance, 130 BPM, energetic and uplifting, four-on-the-floor kick,
punchy snare and crisp hats, deep sub bass, driving plucked bassline,
bright major-key synth arpeggio, warm golden analog pads, glassy bell accents,
danceable workout groove, steady constant tempo, loud punchy mix,
no vocals, no tempo changes, no ambient intro, no breakdown, minimal fills
```

### Terimlerin gerekçesi

| Terim | Neden |
|---|---|
| `energetic and uplifting`, `danceable workout groove` | Kullanıcı isteği: hareketli. İzleyici spor yapıyor; müziğin işi nabzı yukarıda tutmak |
| `four-on-the-floor kick`, `punchy snare and crisp hats` | Ölçülen kick kilidi hedefi ≥0,55; koreografi vuruşa kilitli |
| `deep sub bass`, `driving plucked bassline` | Bas payı hedefi ≥%18; telefon hoparlöründe gövdeyi bas taşıyor |
| `bright major-key synth arpeggio` | Önceki bölümler koyu/karanlık tekno idi. Bu mekân altın-krem, parlak ve sıcak; müzik de aynı dünyayı anlatmalı |
| `warm golden analog pads`, `glassy bell accents` | Mekânın iki malzemesi: sıcak bal (pad) ve mavi buz engeli (cam/çan tınısı) |
| `loud punchy mix` | Crest hedefi ≤14,5 dB — rakip ölçümündeki ağır limitleme |

### Negatifler — hepsi kritik

| Negatif | Olmazsa ne olur |
|---|---|
| `no tempo changes` | Izgara kayar, bütün koreografi tutmaz. Kurtarıcısı yok |
| `no ambient intro` | Giriş ölçüleri boş kalır, bölüm sessiz başlar |
| `no breakdown` | Ortada davul kesilirse gövde tekrarında dikiş duyulur |
| `minimal fills` | Ölçü sınırındaki kesimlerde tık çıkar |
| `no vocals` | Dikkati koreografiden alır; söz telifi ayrı dert |

---

## Ayarlar

- [ ] **Ücretli plan** (ücretsiz katman ticari kullanım hakkı vermiyor)
- [ ] **Instrumental modu AÇIK**
- [ ] **WAV indir** (zaman esnetme yapılacak, kayıpsız kaynak lazım)
- [ ] **2–4 dakika yeter.** `03-motor/muzik-uzat.py` parçayı 330 ölçüye çıkarıyor:
      giriş bir kez, gövde tekrar, çıkış bir kez; bütün kesimler tam ölçü sınırında
- [ ] İlk turda **tek test parçası**. Ben ölçerim, gerekirse prompt kalibre edilir;
      kalibrasyonsuz seri üretim kredi yakar

## Parça geldiğinde ben ne yapacağım

1. Gerçek BPM ölçümü (`03-motor/olc-tempo-kayma.py`) — Suno tam 130,000 vermez
2. `atempo` ile tam 130,000'e oturtma + ilk vuruşu t=0'a kırpma
3. 330 ölçüye uzatma (`muzik-uzat.py`), ölçüm notunu `01-muzik/*-OLCUM.md`'ye yazma
4. Kabul testi: BPM 130,000 ±0,01 · kick kilidi ≥0,55 · crest ≤14,5 dB · bas payı ≥%18
5. `bolum-09-bal.json` → `bpm: 130`, `toplam_olcu: 330`, `muzik:` yeni dosya
6. Tam render (GitHub Actions, 16 paralel parça) + yerel montaj + kare kontrolü
