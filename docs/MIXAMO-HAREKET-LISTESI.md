# Mixamo hareket listesi

**mixamo.com** — Adobe hesabıyla ücretsiz giriş. Hiçbir Adobe programı kurulmaz,
site üzerinden `.fbx` indirilir.

> **DURUM: 21 klibin hepsi indirildi (23 Ağustos 2026).** `02-hareketler/` içindeler.
> Bu belge artık bir alışveriş listesi değil, **kütüphane kaydı** — hangi klibin
> Mixamo'da hangi ada karşılık geldiğini ve kaç kare olduğunu tutuyor.
>
> Kliplerin indirilmesi Adobe girişi gerektiriyor. Chrome'da "Claude in Chrome"
> eklentisi Profile 9'a kurulu ve bağlı; giriş açıkken Claude indirebiliyor.
> Yeni klip gerekirse aynı yoldan eklenir.

---

## KANONİK NÖTR DURUŞ: "Fitness Idle"

Mixamo'nun fitness ailesi tek bir ortak duruş etrafında kurulmuş ve klipler açıkça
`From Fitness Idle` / `To Fitness Idle` diye etiketlenmiş.

**Bizim nötr duruşumuz bu.** Kendi tanımımızı uydurmaya gerek yok — hazır ve tutarlı.

Bu yüzden mümkün olan her yerde **fitness ailesinden** klip seçiyoruz. Aile dışından
alınanlar (side step, dodge) yerinde yapılan ve başladığı duruşa dönen kliplerden
seçildi; motorda kısa geçiş harmanıyla oturtulacak.

**Seçerken:** Mixamo önizlemesinde klibi loop'ta izle. Başlangıç ve bitiş pozu
birbirine oturmuyorsa o klibi alma. Bu tek kural kütüphanenin kalitesini belirler.

---

## İndirme ayarları

| Ayar | Değer |
|---|---|
| Format | FBX Binary (.fbx) |
| Skin | **Without Skin** |
| Frames per Second | 30 |
| Keyframe Reduction | none |

> Karakter fark etmez — ekranda düz siyah siluet olarak render edilecek,
> sadece iskelet lazım.

---

## İNDİRME LİSTESİ — 11 klip

Mixamo'da **arama kutusuna "Ara" sütunundaki metni yaz**, sonra "Açıklama" sütunundaki
alt yazıya sahip olanı seç (aynı isimde birden fazla klip var, ayırt edici olan açıklama).

| # | Kaydet | Ara | Açıklama (ayırt edici) | Cue |
|---|---|---|---|---|
| 1 | `idle.fbx` | `fitness` | **Male Fitness Idle** | `rest` — KANONİK NÖTR |
| 2 | `idle-breathing.fbx` | `fitness` | **Male Fitness Idle With Breathing** | `rest` alternatif |
| 3 | `step-left.fbx` | `side step` | **Short Left Boxing Side Step** | `step_L` |
| 4 | `step-right.fbx` | `side step` | **Short Right Boxing Side Step** | `step_R` |
| 5 | `jump.fbx` | `jump` | **Jumping In Place** | `jump` |
| 6 | `jump-standing.fbx` | `jump` | **Jumping And Landing In Place** | `jump` alternatif |
| 7 | `duck.fbx` | `fitness` | **Air Squat Workout** | `duck` |
| 8 | `dodge-right.fbx` | `dodge` | **Dodging To The Right In Place** | `dodge_R` |
| 9 | `arms-up.fbx` | `fitness` | **Overhead Squat Workout** | `arms_up` |
| 10 | `jacks.fbx` | `jump` | **Standard Jumping Jacks** | mola / dolgu |
| 11 | `punch.fbx` | `punch` | **Hook With The Lead Hand** | `punch` |

### Neden 12 değil 11

**`dodge_L` indirilmiyor.** Motor `dodge-right.fbx` klibini aynalayarak üretecek.
Aynalama zaten koreografi varyasyonu için motorda var (her 8 ölçülük cümlede
sol/sağ takası), bedavaya geliyor.

`spin` de listede yok — ileri cue tiplerinden biri, ilk bölümde kullanılmıyor.
Gerektiğinde eklenir.

### Alternatifler (ana seçim tutmazsa)

| Cue | Yedek |
|---|---|
| `duck` | `Ducking For Cover From Standing Idle` |
| `arms_up` | `Cheering — Male Cheering With Two Fists Pump` |
| `arms_up` | `Fist Pump — Less Enthusiastic Fist Pump` |
| dolgu | `Hip Hop Dancing — Hip Hop Dancing Bboy Variation One` |
| dolgu | `Kettlebell Swing — Russian Kettlebell Swing` (ritmik, tempoya oturur) |

### Bonus: fitness ailesinin geçiş klipleri

Aile içinde `Start Jumping Jacks From Fitness Idle`, `Stop Jumping Jacks To Fitness Idle`
gibi **açık geçiş klipleri** var. İlk turda gerekmiyor, ama ileride hareketler arası
geçişi yumuşatmak istersek hazır kaynak. Aklında olsun.

---

## Retime — neden gerekli

Mixamo klipleri rastgele sürelerde gelir. Bizim ızgaramızda
**1 ölçü = tam 2,000 saniye = 60 kare.**

Retime'ı Claude yapacak, sen sadece indir. Ama seçerken orijinal süre hedefe
**yakın** olsun:

| Hedef | İdeal orijinal süre |
|---|---|
| 1 ölçü (2,0 sn) | 1,5 - 2,8 sn |
| 2 ölçü (4,0 sn) | 3,2 - 5,0 sn |

5 saniyelik klibi 2 saniyeye sıkıştırmak hareketi komik hızlandırır.

## Ayak basışı hizası

Retime'da en kritik nokta: **ayak basışı 1. vuruşa oturmalı.** Klip 2 saniyeye
esnetilse bile içindeki temas anı yanlış yerdeyse siluet müzikle uyumsuz görünür.

Claude bunu klip klip ayarlayacak. İndirirken belirgin ve net ayak basışı olan
klipleri tercih et — bulanık, akışkan hareketlerde hizalanacak referans nokta olmaz.

---

## İNDİRİLDİ — 23 Ağustos 2026

11 klibin hepsi `02-hareketler/` içinde. Mixamo'da ölçülen ham kare sayıları:

| Dosya | Kare | Süre | Hedef | Esnetme |
|---|---|---|---|---|
| `idle.fbx` | 76 | 2,53 sn | 1 ölçü (2,0) | 0,79x |
| `idle-breathing.fbx` | 100 | 3,33 sn | 2 ölçü (4,0) | 1,20x |
| `step-right.fbx` | 27 | 0,90 sn | **yarım ölçü (1,0)** | 1,11x |
| `step-left.fbx` | 25 | 0,83 sn | **yarım ölçü (1,0)** | 1,20x |
| `jump.fbx` | 66 | 2,20 sn | 1 ölçü (2,0) | 0,91x |
| `jump-standing.fbx` | 72 | 2,40 sn | 1 ölçü (2,0) | 0,83x |
| `jacks.fbx` | 33 | 1,10 sn | **yarım ölçü (1,0)** | 0,91x |
| `duck.fbx` | 57 | 1,90 sn | 1 ölçü (2,0) | 1,05x |
| `dodge-right.fbx` | 44 | 1,47 sn | 1 ölçü (2,0) | 1,36x |
| `arms-up.fbx` | 57 | 1,90 sn | 1 ölçü (2,0) | 1,05x |
| `punch.fbx` | ölçülmedi | — | 1 ölçü (2,0) | — |

Esnetmelerin hepsi kabul edilebilir aralıkta. En agresif olan `dodge-right`
(1,36x yavaşlatma) — göze batarsa daha uzun bir dodge klibiyle değiştirilir.

### TASARIM DEĞİŞİKLİĞİ: adımlar yarım ölçü

Ölçüm bir şeyi ortaya çıkardı: yan adımlar **0,85 saniye**. Bunları 2,0 saniyeye
çekmek 2,4x yavaşlatma demek — hareket sünger gibi görünürdü.

Doğrusu şu: **adım hareketleri doğal olarak yarım ölçü (2 vuruş) sürer.**
0,85 → 1,0 sn neredeyse esnetmesiz oturuyor.

Bu zaten koreografiyle de tutarlı: adımlar 1. ve 3. vuruşta geliyor, yani her adım
kendinden sonraki vuruşa kadar olan alanı dolduruyor.

| Süre | Hareketler |
|---|---|
| **Yarım ölçü (1,0 sn)** | `step_L`, `step_R`, `jacks` |
| **Tam ölçü (2,0 sn)** | `idle`, `jump`, `duck`, `dodge`, `arms_up`, `punch` |
| **İki ölçü (4,0 sn)** | `idle-breathing` |

---

# FAZ 2 — takip hareketleri (İNDİRİLDİ)

> **Karar (23 Ağu 2026):** Klipler indirildi ve saklanıyor, ama **kullanımı bekliyor.**
> Motor ve prototip önce Faz 1 (tepki hareketleri) üstüne kurulacak.
> Takip hareketleri o çalıştıktan sonra devreye girecek.

### İndirilenler ve ölçülen uzunluklar

| Dosya | Mixamo klibi | Kare | Süre |
|---|---|---|---|
| `neck-roll.fbx` | Stretching Neck Rolling Side To Side | 97 | 3,23 sn |
| `arm-stretch.fbx` | Stretching Arms By Pushing The Elbows | 267 | 8,90 sn |
| `running-man.fbx` | Dancing The Running Man | 326 | 10,87 sn |
| `raise-roof.fbx` | Hip Hop 'Raise The Roof' | ölçülmedi | — |
| `side-to-side.fbx` | Hip Hop Dancing Side To Side | ölçülmedi | — |
| `shimmy.fbx` | Hip Hop Dancing Shimmy | 360 | 12,00 sn |
| `arm-wave.fbx` | Hip Hop 'Arm Wave' | 157 | 5,23 sn |
| `kick-step.fbx` | Hip Hop 'Kick Step' | ölçülmedi | — |
| `twist-dance.fbx` | Doing The Twist Dance | ölçülmedi | — |
| `charleston.fbx` | Dance Swing Charleston | ölçülmedi | — |

### ÖNEMLİ: takip hareketleri farklı işlenir

Tepki klipleri kısa (0,8-2,5 sn), tek bir hareket. Takip klipleri **uzun döngüler**
(5-12 sn), içinde birden fazla tekrar var.

Bu yüzden retime mantığı farklı:

| | Tepki | Takip |
|---|---|---|
| Uzunluk | Yarım / tam ölçü | Çok ölçülü |
| İşlem | Tek ölçüye esnet | **Ölçü sınırında kırp, döngüye al** |
| Hedef | Vuruşa tam otur | Tempoya otur, sonsuz dönebilsin |

Yani takip klibinde tek bir dans döngüsünün kaç saniye sürdüğünü bulup, onu
en yakın ölçü sayısına esnetip kırpmak gerekiyor. Klip 12 saniyeyse ve içinde
6 tekrar varsa, bir tekrar 2 saniye — yani tam 1 ölçü, harika. Bu analiz
klip klip yapılacak.

### Havuzda ayrıca var (indirilmedi)

`Hip Hop Dancing Rib Pops` · `Body Wave` · `Slide Step` · `Cabbage Patch` ·
`Maraschino Step` · `Salsa Dancing Side To Side` · `Boogaloo`

Katalogda toplam 98 dans klibi var. Tıkanma riski yok.


### Neden gerekli

Kanalın vaadi "Full Body" ve açıklaması "steps, jumps, dodges, **and full body**"
diyor. Sadece ayak işi bu vaadi karşılamaz. İzleyicinin evde kolayca yapabileceği
her hareket havuza girmeli.

### Kısıtlar — her yeni klip bunları geçmek zorunda

| Kural | Neden |
|---|---|
| **Yerinde** olacak, ilerlemeyecek | Siluet karede ortada sabit durmalı |
| **Ayakta** olacak | İzleyici ekrana bakarak duruyor. Şınav, mekik, plank elenir — Mixamo fitness ailesinin yarısı bu yüzden kullanılamaz |
| **Aletsiz** olacak | Kettlebell, barbell, halter siluet olarak anlamsız görünür (havada görünmez nesne) |
| **Yeni başlayan** yapabilecek | Burpee, pistol squat kitle kaybettirir |


## Sonra ne olacak

Faz 1 klipleri indi. Sıradaki adımda Claude:

1. Her klibi tam ölçü uzunluğuna retime eder
2. Ayak basışını 1. vuruşa hizalar
3. Nötr giriş/çıkış pozunu Fitness Idle'a göre doğrular, tutmayanları işaretler
4. `dodge_L`'i aynalayarak üretir
5. Hepsini tek bir `.glb` kütüphanesine paketler (Three.js doğrudan okusun)

Bundan sonra hareket tarafı biter ve bir daha dönülmez.
