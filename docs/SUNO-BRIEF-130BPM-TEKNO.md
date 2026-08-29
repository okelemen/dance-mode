# Suno brief — 130 BPM tekno

> Yazıldı: 29 Ağustos 2026. İstendiğinde verilmek üzere hazır.
> Her terim ölçüme dayanıyor: `docs/OLCUM-STAY-ON-BEAT-11.md` ve
> `docs/RAKIP-ANALIZI-6-KANAL.md`.

---

## Neden bu ses — hedef "önerilenler" listesi

Kanal rakiplerin yanında önerilecek. YouTube birini bize getirdiğinde, gelen kişi
STAY ON BEAT veya BEAT MOTION izlemiş olacak. Kulağı o sese ayarlı geliyor.
Farklı bir şey duyarsa "bu o değil" der ve çıkar.

Bu yüzden brief keyfi değil, **ölçülen rakip profilini hedefliyor**:

| Ölçüm | Dance Mode | Stay on Beat | Beat Motion | **Hedefimiz** |
|---|---:|---:|---:|---:|
| BPM | 142 | **130** | 135 | **130** |
| Kick kilidi (four-on-the-floor) | 0,73 | 0,61 | 0,50 | **0,60-0,75** |
| Crest (dB) — düşük = daha gür | 12,6 | 13,3 | 16,0 | **12,5-14** |
| Bas payı (<150 Hz) | %25,9 | %18,1 | %28,4 | **%20-28** |
| Spektral merkez | 2325 Hz | 2767 Hz | 2052 Hz | **2300-2800 Hz** |

Üç kanalın da müziği Content ID'ye takılmıyor — hiçbiri telifli parça
kullanmıyor. Suno tercihi sahanın standardı.

---

## Ana prompt

```
instrumental techno, 130 BPM, hard four-on-the-floor kick, deep sub bass,
driving analog bassline, hypnotic arpeggiated synth, dark neon atmosphere,
punchy compressed mix, loud and dense, steady groove, consistent tempo
throughout, no vocals, no tempo changes, no ambient intro, no breakdown,
minimal fills
```

### Terimlerin gerekçesi

| Terim | Neden |
|---|---|
| `hard four-on-the-floor kick` | Ölçülen kick kilidi 0,50-0,73. Davul ızgaraya sıkı oturmazsa "dans müziği" değil "fon müziği" olur. |
| `deep sub bass` | Bas payı hedefi %20-28. Bizim ilk parçamızın bası inceydi. |
| `punchy compressed mix`, `loud and dense` | Crest 12,6-13,3 dB = ağır limitlenmiş. Telefon hoparlöründe duyulan şey bu. |
| `hypnotic arpeggiated synth` | Spektral merkez 2300-2800 Hz — üst orta bölgeyi dolduran şey arpej. |
| `dark neon atmosphere` | Görsel dille (tema b) aynı dünyayı anlatıyor. |

### Negatifler — üçü de kritik

| Negatif | Olmazsa ne olur |
|---|---|
| `no tempo changes` | Izgara kayar, koreografi tutmaz. Tek kurtarıcı yok. |
| `no ambient intro` | `muzik-bolum.py` ilk 16 ölçüyü giriş sayıyor; orası boşsa bölüm sessiz başlar. |
| `no breakdown` | Ortada davul kesilirse gövde döngüsü bozulur, tekrar dikişi duyulur. |
| `minimal fills` | Aşırı fill ölçü sınırındaki kesimlerde tık yaratır. |
| `no vocals` | Dikkat dağıtır, ayrıca söz telifi ayrı dert. |

---

## Ortam varyantları

Dört ortamımız var. **Sadece ilk satır değişir**, gerisi aynı kalır — böylece
tempo ve karakter sabit, renk değişiyor.

**NEON CITY** (varsayılan)
```
instrumental techno, 130 BPM, hard four-on-the-floor kick, deep sub bass, ...
```

**DEEP SPACE**
```
instrumental deep space techno, wide reverb pads, 130 BPM, hard four-on-the-floor kick, ...
```

**CIRCUIT**
```
instrumental acid techno, squelchy 303 bassline, 130 BPM, hard four-on-the-floor kick, ...
```

**ULTRA**
```
instrumental peak-time driving techno, relentless energy, 130 BPM, hard four-on-the-floor kick, ...
```

---

## Ayarlar

- [ ] **Ücretli plan.** Ücretsiz katman ticari kullanım hakkı vermez; free ile
      üretilip yayınlanırsa bütün proje boşa gider.
- [ ] **Instrumental modu AÇIK**
- [ ] **WAV indir, MP3 değil** — zaman esnetme yapılacak, kayıpsız kaynak lazım
- [ ] Uzun tek parça peşinde koşma. **2-4 dakikalık parça yeter**;
      `03-motor/muzik-bolum.py` onu bölüm uzunluğuna çıkarıyor
      (giriş bir kez, gövde tekrar, çıkış bir kez, kesimler tam ölçü sınırında)

### İlk iş: tam bölüm üretme yok

Önce **tek bir 2 dakikalık test parçası**. Ben ölçerim, prompt ona göre
kalibre edilir. Kalibrasyon olmadan tam bölüm üretmek kredi yakar.

---

## Parça geldiğinde ben ne yapacağım

1. **Gerçek BPM ölçümü** — Suno tam 130,000 vermez, yaklaşık verir
2. **Tempo düzeltme** — `atempo` ile mikroskobik esnetme (tipik %0,2, kulakla
   duyulmaz), tam 130,000'e oturtulur
3. **İlk vuruş t=0'a kırpılır**
4. **Kabul testi** — şu dördü ölçülür ve hedef aralıkta mı diye bakılır:

| Ölçüm | Kabul aralığı |
|---|---|
| BPM | 130,000 ± 0,01 (düzeltme sonrası) |
| Kick kilidi | ≥ 0,55 |
| Crest | ≤ 14,5 dB |
| Bas payı (<150 Hz) | ≥ %18 |

Tutmuyorsa prompt düzeltilir, parça yeniden üretilir. Ölçüm scripti hazır.

---

## Bir uyarı: 130 BPM tam kare vermiyor

Plan 120 BPM'i "kilitli" ilan etmişti çünkü 30 fps'te tam **15 kare/vuruş**
veriyor. 130'da bu sayı **13,846** — tam sayı değil.

**Pratikte sorun değil.** Motor her şeyi mutlak zamandan hesaplıyor
(`t = kare_no / 30`), cue zamanları saniye cinsinden türetiliyor. Yani **birikimli
kayma yok**; tek etki, bir vuruşun kare sınırına en fazla yarım kare (16,7 ms)
uzağa düşmesi. Bu görülmez.

Tam sayı isteniyorsa en yakın seçenekler 128,571 (14 kare) ve 138,462 (13 kare).
Ama rakip 130'da ve "önerilenler" hedefi tempo eşleşmesini önemli kılıyor.
**Önerim 130'da kalmak.**

Değişecek yerler: `03-motor/muzik-bolum.py` içinde `OLCU_SN = 2.0` → `1.846`,
`ATEMPO` ve `KAYNAK_OLCU` yeni parçaya göre; `spec/sabitler.json` içinde ölçü ve
vuruş süreleri. Koreografi ölçü cinsinden yazıldığı için **aynen taşınır**.
