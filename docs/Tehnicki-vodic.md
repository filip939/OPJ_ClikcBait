# Tehnička strana — hiperparametri i protokol evaluacije

> Cilj: razumeti **šta** svaki hiperparametar radi, **kako** radi 10-fold CV i nested CV, i **zašto** je sve postavljeno baš tako. Praktično za odbranu.

---

## 1. Hiperparametri vs parametri (osnova)

* **Parametri** — ono što model **sam nauči** tokom treninga (težine u logističkoj regresiji, verovatnoće reči u NB, milioni težina u BERT-u). Ne diramo ih ručno.
* **Hiperparametri** — podešavanja koja **mi zadajemo pre treninga** i koja određuju *kako* će se učenje odvijati (koliko jaka regularizacija, koliko epoha, koliki learning rate). Model ih ne uči sam — biramo ih mi (kod nas: GridSearch unutar nested CV za baseline; ručno fiksirane vrednosti za transformere).

Ključna ideja iza svakog hiperparametra: **kontrola kompromisa underfitting ↔ overfitting** (bias–variance). Premalo kapaciteta → model ne uhvati pravilnost. Previše → model „pamti" šum iz treninga i ne generalizuje.

---

## 2. Baseline hiperparametri

### 2.1 `C` — jačina regularizacije (Logistička regresija)

LogReg uči težinu za svaku reč/odliku. Bez ograničenja, težine mogu da „odlete" u velike vrednosti da bi savršeno ispratile trening skup → **overfitting**. Regularizacija kažnjava velike težine.

* `C` je **inverzna** jačina regularizacije: `C = 1/λ`.
* **Malo C** (npr. 0.01) → **jaka** regularizacija → težine guranje ka nuli → jednostavniji, „glađi" model → manje overfittinga, ali rizik od underfittinga.
* **Veliko C** (npr. 100) → **slaba** regularizacija → model slobodno prati trening → rizik od overfittinga.

GridSearch isproba mrežu vrednosti (npr. `0.01, 0.1, 1, 10, 100`) i bira onu koja daje najbolji rezultat na **unutrašnjoj** validaciji.

### 2.2 `alpha` — Laplasovo (additive) poravnanje (Naivni Bajes)

NB računa verovatnoću svake reči po klasi. Problem: ako se neka reč **nikad** ne pojavi u klikbejt primerima trening skupa, njena verovatnoća za tu klasu je **0**, a pošto NB množi verovatnoće, **jedna nula uništi ceo proizvod** (cela rečenica dobije verovatnoću 0).

* `alpha` dodaje mali „lažni broj javljanja" svakoj reči (smoothing): `P(reč|klasa) = (broj + alpha) / (ukupno + alpha·|vokabular|)`.
* **alpha = 1.0** → klasično Laplasovo poravnanje.
* **Malo alpha** (→0) → model veruje tačno onome što vidi u treningu (rizik od nula i overfittinga na retke reči).
* **Veliko alpha** → jako „izglađivanje" → verovatnoće se približavaju uniformnoj → model postaje tup (underfitting).
* Funkcioniše kao **oblik regularizacije** za NB.

### 2.3 Reprezentacija teksta (nisu hiperparametri u užem smislu, ali se biraju)

Ovo su odluke o tome **kako naslov pretvaramo u brojeve** — poredimo ih kao faktore:

* **Normalizacija reči** — `none` / `stem` / `lemma`. Svodi morfološke oblike („kapitenu", „kapitena", „kapiten") na zajedničku osnovu → smanjuje **proređenost** (manje različitih odlika), važno na malom skupu.
* **Ponderisanje** — `bow` (brojanje) / `tf` / `idf` / `tfidf`. Određuje koliko „težine" nosi svaka reč. **IDF** smanjuje uticaj čestih reči, povećava uticaj retkih i distinktivnih.
* **N-gram** — `1-1` (samo reči) ili `1-2` (reči + parovi). Bigrami hvataju fraze kao „nećete verovati", ali na kratkim naslovima donose malo.

---

## 3. Transformer hiperparametri (BERTić / mBERT)

Ovde **ne** koristimo GridSearch — vrednosti su fiksirane na osnovu prakse za fine-tuning, jer je svaki trening skup.

### 3.1 `learning_rate = 2e-5` — veličina koraka učenja

Koliko jako model pomera težine pri svakom koraku.

* BERT je **već pretreniran** i „zna srpski". Ne želimo da ga pokvarimo.
* **Veliki LR** (npr. 1e-3) bi „prejako" pomerio težine i **uništio** pretrenirano znanje (catastrophic forgetting).
* **Mali LR (2e-5)** → blago doteruje postojeće znanje ka našem zadatku.
* Standardna vrednost za BERT fine-tuning je upravo red veličine `2e-5` do `5e-5`.

### 3.2 `num_epochs ∈ {2, 3, 4}` — koliko puta model prođe kroz ceo skup

Jedna epoha = model je video svaki od 2200 naslova tačno jednom.

* **Premalo epoha (2)** → **nedotreniran** (underfitting): nije stigao da nauči → niži F1.
* **Previše epoha** → **overfitting**: počinje da pamti konkretne naslove umesto obrazaca.
* Kod nas **3–4 epohe** optimalno. Tretiramo ih kao **zasebne fine-tuning-ge** (vidi 3.5), ne kao checkpoint-e jednog treninga.

### 3.3 `batch_size = 64` — koliko primera obradi pre jednog ažuriranja težina

* Model ne ažurira težine posle svakog naslova, nego posle grupe (batch) od 64.
* Veći batch → stabilniji (uprosečeni) gradijent, ali traži više VRAM-a.
* 64 je kompromis koji staje na T4 GPU (\~16 GB) sa kratkim naslovima.

### 3.4 `max_len = 64 tokena` — maksimalna dužina ulaza

* Svaki naslov se seče/dopunjava na 64 tokena (subword jedinice).
* Naši naslovi su **kratki**, pa 64 je više nego dovoljno → nema gubitka informacije, a računica je brza i jeftina po memoriji.

### 3.5 LR raspored (scheduler) — i zašto su epohe „zasebni treninzi"

Learning rate **nije konstantan** tokom treninga — spušta se po rasporedu (linearni decay): kreće od 2e-5 i pada ka 0 do **kraja zadatog broja epoha**.

* Zato trening podešen za **4 epohe** u 2. epohi **još nije spustio LR** → to **nije** isto stanje kao trening koji se zaustavlja na 2 epohe.
* ❗ Zbog ovoga je „brza" verzija (jedan trening do max epoha + evaluacija posle svake) davala **lažan, obrnut trend** („2 epohe najbolje"). Rešenje: za svaku vrednost epoha pokrećemo **poseban fine-tuning sa sopstvenim LR rasporedom**.

### 3.6 Ostalo

* **fp16** (half precision) — računanje u 16-bitnim brojevima na GPU → 2× brže, manje memorije, zanemarljiv gubitak tačnosti.
* **Cross-entropy loss** — funkcija greške za klasifikaciju; kažnjava model srazmerno tome koliko je „samouvereno pogrešio".
* **Klasifikacioni sloj na `[CLS]`** — mali linearni sloj (768 → 2) dodat na vrh; uzima sažeti vektor celog naslova i daje 2 broja (klikbejt / regularan).

---

## 4. Dekoder (Claude) — „hiperparametri" prompta

Nema treninga, pa nema klasičnih hiperparametara. Ono što variramo su **uslovi prompta**:

* **Jezik prompta** — SR vs EN (jezik *instrukcije*, ne naslova; naslovi su uvek srpski).
* **Broj primera** — zero-shot (0 primera) vs few-shot (par primera u promptu).
* **Definicija** — sa definicijom klikbejta u promptu ili bez.
* **Temperatura** se drži niska/0 da odgovor bude determinističan (`1` ili `0`), bez „kreativnosti".

---

## 5. Kako radi 10-fold stratifikovana CV (korak po korak)

Problem koji rešava: ako bismo merili na jednoj 70/30 podeli, rezultat zavisi od **sreće u podeli**. CV koristi sve podatke i daje **stabilniju** procenu.

### Postupak

1. Ceo skup (2200 naslova) podelimo na **10 jednakih delova (fold-ova)**, po \~220.
2. **Stratifikovano** = u svakom fold-u zadržavamo isti balans klasa (50/50 klikbejt/regularno), kao u celom skupu.
3. Radimo **10 prolaza**. U prolazu *i*:
   * **9 fold-ova = trening** (\~1980 naslova) — model uči na njima,
   * **1 fold = test** (\~220 naslova) — model evaluiramo na njemu (model ga **nije video**).
   * Svaki fold tačno **jednom** bude test.
4. Dobijemo **10 rezultata** (F1, accuracy, AUC po prolazu) → **uprosečimo ih**. Prosek je finalna ocena; raspon pokazuje stabilnost.

```
Fold:   [1][2][3][4][5][6][7][8][9][10]
Prolaz 1: TEST  + ostalih 9 trening
Prolaz 2:    TEST + ostalih 9 trening
...
Prolaz 10:                        TEST + ostalih 9 trening
            → 10 ocena → prosek = finalni rezultat
```

### Zašto baš ovako (a ne fiksni split)

* **Koristi sve podatke** i za trening i za test (svaki naslov bar jednom test).
* **Mali skup (2200)** → jedna podela bi bila bučna; prosek 10 podela je pouzdaniji.
* Postavka **eksplicitno** propisuje 10-fold stratifikovanu CV → poređenje između modela je pošteno (svi mereni istim protokolom).

---

## 6. Sprečavanje curenja informacija (data leakage) u CV-u

Curenje = kad model na bilo koji način „vidi" test podatke tokom učenja → rezultat izgleda bolje nego što jeste.

* **Vektorizator (vokabular + IDF) se uči UNUTAR svakog fold-a**, samo na 9 trening fold-ova. IDF zavisi od skupa dokumenata — da smo ga računali nad svih 2200, test fold bi „procurio" u težine. Zato: fit na trening delu, transform na test delu.
* **Stem/lemma su deterministički po reči** (ista reč → uvek isti rezultat, nezavisno od ostatka skupa), pa se smeju uraditi **jednom** nad celim skupom — to **nije** curenje.

---

## 7. Nested (ugnežđena) CV — kad biramo i hiperparametre

Problem: ako iste podatke koristimo i da **biramo** hiperparametre (C, alpha) i da **ocenjujemo** model, izbor hiperparametara „vidi" test → optimistična, lažna ocena. Nested CV razdvaja te dve uloge u **dve petlje**.

```
SPOLJNA petlja (10-fold) — služi ČISTO za evaluaciju
│
├─ za svaki spoljni prolaz:
│    trening deo (9 fold-ova)  →  test deo (1 fold)
│                                  ↑ ocena se meri ovde
│    │
│    └─ UNUTRAŠNJA petlja (5-fold GridSearchCV) — služi za IZBOR hiperparametara
│         radi se SAMO nad spoljnim trening delom:
│         isproba sve kombinacije (npr. C, alpha) i bira najbolju
│         → tom najboljom konfiguracijom model se trenira na celom
│           spoljnom trening delu i meri na spoljnom test fold-u
```

* **Spoljna petlja (10-fold)** → daje finalnu, poštenu ocenu.
* **Unutrašnja petlja (5-fold GridSearch)** → bira hiperparametre, **bez ikakvog kontakta** sa spoljnim test fold-om.
* Rezultat: izbor hiperparametara **nikad ne vidi** podatke na kojima se model ocenjuje → nema optimističke pristrasnosti.

Napomena: nested CV koristimo za **baseline** (gde GridSearch bira C/alpha). Za **transformere** hiperparametri su fiksirani, pa je dovoljna obična 10-fold CV.

---

## 8. Brza tabela — šta koji hiperparametar radi


| Hiperparametar  | Model  | Šta kontroliše                  | Malo →                         | Veliko →                     |
| --------------- | ------ | --------------------------------- | ------------------------------- | ----------------------------- |
| `C`             | LogReg | jačina regularizacije (inverzno) | jača reg., jednostavniji model | slabija reg., rizik overfit   |
| `alpha`         | NB     | smoothing retkih reči            | veruje treningu, rizik nula     | tup model, underfit           |
| `learning_rate` | BERT   | veličina koraka učenja          | sporo, sigurno                  | brzo, rizik da pokvari znanje |
| `num_epochs`    | BERT   | broj prolaza kroz skup            | underfit (2)                    | overfit (mnogo)               |
| `batch_size`    | BERT   | primera po ažuriranju            | bučniji gradijent, manje VRAM  | stabilniji, više VRAM        |
| `max_len`       | BERT   | dužina ulaza u tokenima          | rizik sečenja teksta           | sporije, više memorije       |

---

## 9. Skraćeni odgovori za odbranu

* **Šta radi C?** → reguliše koliko model sme da prati trening; malo C = jača regularizacija = jednostavniji model.
* **Šta radi alpha?** → sprečava verovatnoću 0 za neviđene reči; smoothing / regularizacija za NB.
* **Zašto LR 2e-5?** → mali korak da fine-tuning ne uništi pretrenirano znanje.
* **Zašto 3–4 epohe?** → 2 = nedotreniran; previše = overfitting; 3–4 optimum.
* **Kako radi 10-fold CV?** → 10 delova, svaki jednom test a 9 puta trening, rezultati se uproseče; stabilnija ocena na malom skupu.
* **Zašto stratifikovano?** → da svaki fold ima isti balans klasa (50/50) kao ceo skup.
* **Kako sprečavate curenje?** → IDF/vektorizator se uče unutar fold-a; izbor hiperparametara u unutrašnjoj petlji nested CV-a koja ne vidi spoljni test.
* **Zašto nested CV?** → da izbor hiperparametara ne „vidi" podatke za evaluaciju i ne napravi lažno dobru ocenu.
