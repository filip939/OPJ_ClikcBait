# Sve što treba da znaš o projektu — Detekcija klikbejta (OPJ 2025/2026)

> Jedinstveni vodič „od nule": **šta smo radili, kako radi, i zašto baš tako.**
> Namenjeno pripremi za odbranu i razumevanju celog rešenja bez prelistavanja
> deset fajlova. Detalji po fazama: `docs/Radni-izvestaj.md`. Zahtevi:
> `docs/Projekat-zahtevi.md`. Teorija (predavanja): `presentation/sazetak/`.

---

## 0. Suština u jednom pasusu

Pravimo sistem koji za **srpski sportski novinski naslov** odlučuje da li je
**klikbejt (1)** ili **regularan (0)** — to je **binarna klasifikacija teksta**.
Sami smo prikupili naslove (Faza 1), ručno ih obeležili (Faza 2), i nad njima

obučili/evaluirali tri vrste modela (Faza 3): jednostavne **baseline** modele,
**enkoderske transformere** (BERTić, mBERT) koje fino podešavamo, i jedan
**dekoderski LLM** (Claude) koji samo ispitujemo bez treninga. Sve modele merimo
**istim metrikama** i **istim protokolom (10-fold CV)** da bismo ih pošteno
poredili. Glavni nalaz: svi modeli su bolji od baseline-a, a kontekstualni modeli
(BERTić ~0.70 F1, Claude ~0.71 F1) ubedljivo nadmašuju „vreću reči" (~0.65 F1) —
jer klikbejt je **semantička/pragmatska** pojava koju brojanje reči ne hvata.

**Grupa:** Filip Nikolić (25/3234), Danilo Nikolić (25/3235) — par.
**Zadatak/domen:** detekcija klikbejta / sportski naslovi. **Izvor:** SportKlub.

---

## 1. Šta je „klikbejt" i zašto je to NLP zadatak

**Klikbejt** je naslov koji **namerno manipuliše čitaoca da klikne**, a ne da ga
pošteno informiše. Naša definicija (iz `annotation/guidelines.md`) obuhvata:
- **uskraćivanje ključne informacije** → „kognitivni jaz" / curiosity gap
  („Nećete verovati šta je uradio kapiten!");
- **preuveličavanje važnosti** događaja;
- **veštački emocionalni naboj**;
- **senzacionalističke fraze** („a onda se desilo ovo", velika slova, uzvičnici).

**Regularan** naslov jasno i informativno prenosi suštinu vesti
(„Partizan pobedio Zvezdu 2:1 u derbiju").

Bitno: profesor je tražio da **NE** svedemo klikbejt na površne signale
(uzvičnik, velika slova). Cilj je da uhvatimo i **suptilne** manipulacije, što
zadatak čini **semantičkim/pragmatskim**, a ne pukim traženjem ključnih reči.
Zato baseline (vreća reči) ima granicu koliko može, a kontekstualni modeli
profitiraju.

**Gde u NLP-u ovo stoji** (predavanje 9): ovo je **klasifikacija teksta** —
svrstavanje teksta u jednu od predefinisanih kategorija. Srodno je detekciji
spama i analizi sentimenta. Standardni modeli: naivni Bajes, logistička
regresija, SVM; danas i transformeri.

---

## 2. Faza 1 — Prikupljanje podataka

**Šta smo uradili:** skrejpovali naslove sa **SportKlub** portala (jedan izvor,
latinica), uklonili duplikate → **2994 jedinstvena naslova**. Za svaki čuvamo
URL/identifikator i rubriku (`data/metadata.csv`). Format: UTF-8.

**Zašto jedan izvor (a ne više):** kontrolisan, konzistentan stil. Da smo mešali
portale, model bi mogao da uči **razliku između portala** umesto razlike
klikbejt/regularno. Drugi izvori (npr. Mozzart) razmatrani pa **odbačeni**.

**Zašto baš sport:** profesor je tražio jedan tematski domen; sportske vesti
imaju puno naslova i jasan stilski opseg (od suvoparnih rezultata do
senzacionalizma).

Kod: `src/scraping/`.

---

## 3. Faza 2 — Anotacija (ručno obeležavanje)

Model uči iz primera koje **mi** označimo, pa kvalitet anotacije direktno
određuje gornju granicu kvaliteta modela. Pratili smo **standardnu metodologiju
u 5 koraka** (iz postavke):

1. **Oznake:** binarno — `1` = klikbejt, `0` = regularan.
2. **Uputstva za anotaciju** (`annotation/guidelines.md`): definicija + kako
   rešavati problematične/granične slučajeve.
3. **Kalibracija:** **220 naslova** (po 110) oba člana anotirala **nezavisno,
   bez konsultacija** → da proverimo da li uputstva „drže vodu".
4. **Glavna anotacija:** ravnomerno podeljeno (Filip 1497, Danilo 1497) —
   jednostruka anotacija po naslovu.
5. **Analiza saglasnosti + statistika.**

### Međuanotatorska saglasnost (IAA) — i zašto je važna

Ako se dva čoveka ne slažu oko toga šta je klikbejt, ni model ne može da nauči
doslednu granicu. Zato merimo **slaganje** na kalibracionom skupu:

- **Procentualno slaganje: 82.7 %** (182/220).
- **Cohen's kappa κ = 0.640** („good"). Kappa je strože od procenta jer
  **koriguje za slučajno slaganje** — koliko bismo se složili i da nasumično
  pogađamo. κ ≥ 0.6 je bio cilj → **ispunjen**.
- Neslaganja (38/220) su **dosledna i jednosmerna** (Filip nešto šire tumači
  klikbejt) i na **suptilnim graničnim** slučajevima — to potvrđuje da je granica
  **semantička**, a ne trivijalna/površinska.

38 spornih rešeno **adjudikacijom** (zajednički usaglašena labela).

### Finalni skup

**`data/annotated/dataset.tsv` = 2200 naslova, balans 1100/1100**, 0 duplikata.
Iz 2994 (koji su bili ~49/51 %) izvukli smo **balansiran** podskup 1100/1100
(profesor je tražio ~1100 po klasi). Balans je bitan jer **accuracy ima smisla
samo kad su klase izbalansirane** (predavanje 8). Višak (~800) ostaje kao rezerva.

Kod: `src/annotation/` (iaa.py, build_dataset.py, stats.py, reconcile_iaa.py).

---

## 4. Teorijski temelji obučavanja i evaluacije (predavanje 8)

Ovo su pojmovi koje moraš znati da objasniš **zašto** smo evaluaciju radili kako
smo radili.

- **Obučavanje** = optimizacija modela nad parovima (x = naslov, y = labela), da
  nađe funkciju x→y. **Parametri** su ono što algoritam sam podešava;
  **hiperparametri** su podešavanja koja zadajemo ručno pre treninga (npr. jačina
  regularizacije C, alpha kod NB, broj epoha kod BERT-a).
- **Underfitting** (model prejednostavan, ne uči pravilnosti) vs **overfitting**
  (model presložen, „pamti" šum umesto da generalizuje). Cilj je balans =
  **bias–variance kompromis**.
- **Zašto se ne sme evaluirati na trening podacima:** model je već prilagođen
  njima → izgledao bi bolje nego što jeste. Treba **nedirnut skup**.
- **Stratifikacija:** pri deljenju podataka zadržavamo istu raspodelu klasa u
  svakom delu (kod nas 50/50).
- **k-fold unakrsna validacija (CV):** podelimo skup na k slojeva; u k prolaza
  svaki put model **uči na k−1 sloja, testira na 1**, pa **uprosečimo**. Daje
  **pouzdaniju** procenu od jedne podele i koristi sve podatke.
- **Ugnežđena (nested) CV:** kad treba i da **biramo hiperparametre** i da
  **pošteno evaluiramo**, ne smemo iste podatke koristiti za oboje (curilo bi).
  Zato: **spoljna** petlja evaluira, a unutar svakog spoljnog trening dela
  **unutrašnja** petlja bira hiperparametre (GridSearch). Tako izbor
  hiperparametara „ne vidi" spoljni test fold.

### Metrike koje koristimo (iste za sve modele)

- **Matrica zabune:** TP, TN, FP, FN. Pozitivna klasa = **klikbejt**.
- **Accuracy** = (TP+TN)/ukupno — pouzdana jer nam je skup balansiran.
- **Preciznost** = TP/(TP+FP): od onih koje je nazvao klikbejtom, koliko ih je
  zaista klikbejt.
- **Odziv (recall)** = TP/(TP+FN): od svih pravih klikbejtova, koliko ih je uhvatio.
- **F1** = harmonijska sredina preciznosti i odziva — glavna metrika (balansira
  oba). Računamo je **za klikbejt klasu** (F1_kb) i kao **macro-F1**.
- **ROC-AUC:** koliko dobro model **rangira** klikbejt iznad regularnog kroz sve
  pragove; meri kvalitet **verovatnoća**, ne samo tvrde odluke (1/0).

**Zašto ove metrike:** klikbejt je „pozitivna" klasa koju želimo da uhvatimo;
F1 hvata kompromis preciznost/odziv, a AUC pokazuje kalibraciju verovatnoća.

### Zašto NEMA fiksnog train/test split-a

Postavka **eksplicitno** propisuje 10-fold stratifikovanu CV (i nested CV za
hiperparametre) za baseline i enkodere, a **ceo skup** za dekoder. CV sama deli
podatke fold-po-fold; to je metodološki ispravnije od jedne 70/30 podele kod
malog skupa (2200).

---

## 5. Faza 3a — Baseline modeli (klasično ML, lokalno na CPU)

**Ideja:** najjednostavniji mogući modeli kao **donja referenca**. Bez baseline-a
nema smisla reći da je transformer „dobar" — moramo znati u odnosu na šta
(predavanje 8: baseline = npr. uvek većinska klasa; mi koristimo prave, ali
jednostavne klasifikatore).

### Kako baseline pretvara naslov u brojeve (feature-i)

Računar ne razume reči — treba mu vektor brojeva. Koristimo **bag-of-words**:
tekst = neuređen skup reči, svaka reč (ili bigram) = jedna odlika. Pipeline:

1. **Pretprocesiranje** (`src/preprocessing/serbian.py`):
   - NFC normalizacija, **ćirilica → latinica**, **lowercase**, uklanjanje
     interpunkcije;
   - **normalizacija reči** u tri varijante koje poredimo:
     - `none` (bez),
     - `stem` — naš **heuristički stemmer** (odseca česte srpske nastavke,
       greedy najduži-prvo, ne kraći od 3 slova; bez ikakvih zavisnosti),
     - `lemma` — prava lematizacija preko **classla** (svodi reč na rečnički
       oblik, koristi POS).
   - **Zašto normalizacija:** srpski je morfološki bogat — ista reč ima mnogo
     oblika (padeži, rod, broj). Bez svođenja na osnovu raste **proređenost**
     (svaki oblik = posebna odlika), što je problem kod malih skupova.
2. **Vektorizacija / ponderisanje** (`run_baseline.py: make_vectorizer`) — četiri
   šeme koje poredimo (profesor je tražio TF/IDF/TF-IDF, ne izbacivanje stop-reči):
   - `bow` — puko **brojanje** reči (CountVectorizer);
   - `tf` — **term frequency**, l2-normalizovano;
   - `idf` — prisustvo × **inverzna dokument-frekvencija** (retke reči = veća
     težina);
   - `tfidf` — **TF·IDF** (sublinear_tf) — težina raste i sa učestalošću u naslovu
     i sa retkošću u korpusu.
   - n-gram: `1-1` (samo reči) ili `1-2` (reči + parovi reči).

### Modeli

- **Logistička regresija (LogReg):** linearni **diskriminativni** model; uči
  težine po odlikama i kroz sigmoidu daje verovatnoću klase. Hiperparametar
  **C** = jačina regularizacije (manje C = jača regularizacija = jednostavniji
  model).
- **Naivni Bajes (NB):** **generativni** model na Bajesovoj teoremi sa „naivnom"
  pretpostavkom da su odlike (reči) **nezavisne** uz datu klasu. Pretpostavka je
  formalno netačna, ali u praksi radi dobro za tekst. Dve varijante:
  - **Multinomijalni (MNB)** — odlike su **broj javljanja** reči;
  - **Bernoulli (BNB)** — odlike su **prisustvo/odsustvo** reči.
  - Hiperparametar **alpha** = **Laplasovo poravnanje** (sprečava da nikad-viđena
    reč daje verovatnoću 0; oblik regularizacije).

### Protokol bez curenja informacija

- **Spoljna 10-fold stratifikovana CV** za evaluaciju + **unutrašnja 5-fold
  GridSearchCV** za izbor hiperparametara (C, alpha) → **nested CV**.
- Stem/lemma su **deterministički po tokenu**, pa ih radimo **jednom** nad celim
  skupom (nije curenje). Ali **vektorizator (vokabular + IDF) se uči UNUTAR
  svakog fold-a** — IDF zavisi od skupa, pa bi učenje nad svim podacima bilo
  curenje.

### Rezultat

**Najbolji baseline: MNB + stem + TF-IDF + bigrami → F1(klikbejt) = 0.646,
ROC-AUC = 0.676.** Efekti faktora (prosečan F1):

| Faktor | Nalaz |
|---|---|
| Model | MNB **0.626** > LogReg 0.611 = BNB 0.611 |
| Normalizacija | lemma 0.623 ≈ stem 0.622 ≫ none 0.603 |
| Ponderisanje | TF 0.620 ≈ TF-IDF 0.618 ≈ BoW 0.615 > IDF 0.610 |
| N-gram | 1-2 ≈ 1-1 (zanemarljivo) |

**Zašto je NB najbolji:** kratki tekstovi, retke reči, visoka dimenzionalnost —
NB se tu dobro ponaša i jak je kad ima malo podataka. **Zašto TF-IDF ne dominira:**
naslovi su kratki, svaka reč se javlja retko → IDF ima malo prostora da napravi
razliku. To je **iskren nalaz** (profesor je tražio da izmerimo efekat
ponderisanja, ne da „nateramo" TF-IDF da bude najbolji).

Kod: `src/baseline/`. Rezultat: `results/baseline_results.csv`,
`results/faza3a_baseline_izvestaj.md`.

---

## 6. Faza 3b — Enkoderski transformeri (BERTić + mBERT) — „naša neuralna mreža"

Ovo je deo koji najčešće traži dodatno objašnjenje. Ide odozgo (intuicija) ka
dole (detalji).

### 6.1 Zašto uopšte transformer, a ne baseline

Baseline gleda reči **izolovano** (vreća reči). Ali klikbejt zavisi od
**konteksta i redosleda**: „Nećete verovati šta se desilo" je klikbejt zbog
**konstrukcije**, ne zbog pojedinačnih reči. Transformer čita ceo naslov i pravi
**kontekstualnu** reprezentaciju — značenje svake reči zavisi od ostalih. To je
glavna teza projekta i razlog zašto transformeri pobeđuju baseline.

### 6.2 Šta je BERT (enkoderski transformer), pojmovno

- **BERT** = Bidirectional Encoder Representations from Transformers. To je
  neuralna mreža koja je **prethodno obučena (pretraining)** na ogromnom
  neanotiranom tekstu zadatkom **Masked Language Model (MLM)**: sakrije se deo
  reči i mreža uči da ih pogodi iz **konteksta sa obe strane** (otud
  „bidirectional"). Tako mreža stekne **opšte znanje o jeziku** bez ručne
  anotacije (= samonadgledano učenje).
- **Tokenizacija (WordPiece):** ulazni tekst se ne deli na cele reči nego na
  **podreči** (subword) — retke/nepoznate reči se rastave na delove. Dodaju se
  posebni tokeni: **`[CLS]`** na početku i **`[SEP]`** na kraju.
- **Embeddings:** svaki token → vektor; dodaje se **pozicioni** vektor (da mreža
  zna redosled).
- **Self-attention (srce transformera):** svaki token „gleda" sve ostale tokene i
  računa koliko je koji relevantan za njega → tako se gradi **kontekst**.
  Naslagano u više slojeva (12 kod ovih modela), svaki sa više „glava" pažnje.
- **Izlaz:** vektor `[CLS]` tokena sažima ceo naslov → koristi se za
  klasifikaciju.

### 6.3 Fine-tuning = transferno učenje (kako mi pravimo klasifikator)

Ne treniramo BERT od nule (to traži milijarde reči i ogroman GPU). Umesto toga:

1. Uzmemo **pretrenirani** model (sve njegovo jezičko znanje već postoji).
2. Na vrh `[CLS]` izlaza dodamo **mali klasifikacioni sloj** (2 izlaza:
   klikbejt / regularan) — `AutoModelForSequenceClassification(num_labels=2)`.
3. **Fino podešavamo (fine-tuning):** treniramo na **našim 2200 naslova** sa
   labelama; gradijenti idu kroz ceo model i **blago pomeraju** sve težine ka
   našem zadatku. Pošto model već „zna srpski", dovoljno je malo primera i
   malo epoha. Ovo je **dominantna paradigma** u modernom NLP-u (predavanje 9).

Konkretno (`src/transformers/finetune.py`):
- **learning rate = 2e-5** (mali — da ne „pokvarimo" pretrenirano znanje),
- **batch = 64**, **max_len = 64 tokena** (naslovi su kratki),
- optimizacija unakrsne entropije, fp16 na GPU.

### 6.4 Dva modela — i zašto baš ta dva

Postavka traži **bar jedan monolingvalni i jedan multilingvalni** enkoder:
- **BERTić** (`classla/bcms-bertic`) — **monolingvalni** za BCMS (bos/hrv/srp/cnr).
  Treniran baš na našem jeziku.
- **mBERT** (`bert-base-multilingual-cased`) — **multilingvalni** (104 jezika
  odjednom).

Poređenje pokazuje da li je vredno imati **namenski srpski** model vs „univerzalni".

### 6.5 Protokol — i jedna metodološka finesa

- **10-fold stratifikovana CV** (kao baseline, radi poređenja).
- **Varijante po broju epoha {2, 3, 4}** kao **ZASEBNI fine-tuning-zi** — svaki sa
  svojim **LR-rasporedom** (learning rate se tokom treninga spušta po rasporedu
  koji zavisi od ukupnog broja epoha). To je metodološki ispravno, ali skuplje
  (10×(2+3+4) treninga).
  - ⚠️ **Zašto ovo naglašavamo:** prva, „brza" verzija je radila jedan trening do
    max epoha i samo evaluirala posle svake epohe. To je davalo **obrnut, pogrešan
    trend** („2 epohe najbolje") jer su 2 i 3 bili samo checkpoint-i treninga
    podešenog za 4 epohe (LR još nije bio spušten). Zato smo prešli na zasebne
    fine-tuning-ge. Stara varijanta je ostala samo kao `--fast-epochs` za probu.

Pokrenuto na **Google Colab T4 GPU** (besplatno; ~40–60 min za oba modela), jer
fine-tuning traži GPU sa ≥8 GB VRAM. Jedan fajl: `src/transformers/colab_train.py`.

### 6.6 Rezultati

| Model | Epohe | F1(kb) | Acc | ROC-AUC |
|---|---|---|---|---|
| BERTić | 2 | 0.681 | 0.680 | 0.760 |
| **BERTić** | **3** | **0.703** | 0.704 | 0.785 |
| BERTić | 4 | 0.703 | 0.702 | **0.788** |
| mBERT | 2 | 0.651 | 0.664 | 0.736 |
| **mBERT** | **3** | **0.690** | 0.687 | 0.753 |
| mBERT | 4 | 0.682 | 0.691 | 0.755 |

**Nalazi:** (1) **3–4 epohe** najbolje; sa 2 epohe model je **nedotreniran**.
(2) **BERTić > mBERT** na svim metrikama — monolingvalni model za srpski je
očekivano bolji. (3) Oba **ubedljivo nadmašuju baseline** (AUC +0.11 kod BERTića) —
potvrda glavne teze: vreća reči ne hvata suptilni klikbejt, kontekstualni enkoder
ga hvata.

Kod: `src/transformers/finetune.py`. Rezultat:
`results/encoder_{bertic,mbert}_results.csv`, `results/faza3b_encoder_izvestaj.md`.

---

## 7. Faza 3c — Dekoderski LLM (Claude) — samo evaluacija

### 7.1 Zašto „samo evaluacija"

**Dekoderski/generativni** modeli (ChatGPT, Gemini, Claude) su ogromni i
zatvoreni → **ne možemo ih fine-tune-ovati**. Zato ih, po postavci, **samo
evaluiramo** — i to na **celom skupu (2200)**, jer nema treninga pa nema potrebe
za CV-om.

### 7.2 Kako radi (prompting / zero-shot)

Modelu damo **uputstvo (prompt)** sa definicijom klikbejta i tražimo da odgovori
**samo `1` ili `0`** za dati naslov. Bez ijednog primera u promptu = **zero-shot**
(model rešava zadatak „iz prve", oslanjajući se na opšte znanje stečeno u
pretreningu). Kod podržava i few-shot (primeri u promptu) i bez-definicije, ali
to su opciona obogaćenja.

### 7.3 Glavni eksperiment — jezik prompta (SR vs EN)

Postavka traži poređenje **jezika upita**. Merimo **srpski vs engleski prompt**.
- ‼️ **Bitno za odbranu:** SR/EN se odnosi na **jezik uputstva modelu**, NE na
  naslove — **naslovi su u oba slučaja srpski**. Pitanje je: da li jezik
  instrukcije menja kako model klasifikuje srpske naslove.

| Varijanta | F1(kb) | Acc | Preciznost | Odziv |
|---|---|---|---|---|
| SR prompt (sr_zero_def) | 0.710 | **0.695** | 0.676 | 0.748 |
| EN prompt (en_zero_def) | **0.715** | 0.691 | 0.664 | 0.775 |

**Nalaz:** SR ≈ EN (gotovo isto). Jezik prompta **ne menja bitno** rezultat;
EN ima nešto viši odziv, SR višu preciznost/accuracy.

### 7.4 Zašto Claude (a ne ChatGPT/Gemini)

Profesor je dozvolio „ChatGPT, Gemini **i drugi**". Besplatni **Gemini tier nije
bio dostupan** za naš nalog/region (greška `limit: 0`); ChatGPT bi se plaćao.
Iskoristili smo **Claude** (`claude-haiku-4-5`) — plaćeni ali jeftin (~$1 za ceo
skup), validan dekoderski model. Odgovori keširani (`results/decoder_cache/`) radi
prekida/nastavka; 0 neparsiranih.

Kod: `src/decoder/claude_eval.py`, prompti: `src/decoder/prompts.py`. Rezultat:
`results/faza3c_decoder_izvestaj.md`.

---

## 8. Sinteza — uporedni pregled svih modela

| Model | Tip | F1(kb) | Acc | ROC-AUC |
|---|---|---|---|---|
| MNB + stem + TF-IDF | baseline | 0.646 | 0.622 | 0.676 |
| mBERT (3 ep) | enkoder multi | 0.690 | 0.687 | 0.753 |
| **BERTić (3–4 ep)** | enkoder mono | 0.703 | **0.704** | **0.788** |
| Claude SR (zero-shot) | dekoder | 0.710 | 0.695 | — |
| **Claude EN (zero-shot)** | dekoder | **0.715** | 0.691 | — |

**Zaključci:**
1. **Svi modeli > baseline** — kontekst pobeđuje vreću reči.
2. **Dekoder bez ikakvog treninga** ima najviši F1 (~0.715), tek blago iznad
   BERTića (0.703) — impresivno za zero-shot.
3. Ali **BERTić** je najbolji po **accuracy** i jedini sa **kalibrisanim
   verovatnoćama (AUC 0.788)**; mali je, besplatan, radi lokalno.
4. **Mono > multi**, **3–4 epohe** optimalno, **SR ≈ EN** prompt.

**Preporuka:** za produkciju → **BERTić** (mali, lokalan, dobar AUC); kad nema
podataka za trening → **Claude zero-shot**.

---

## 9. Najverovatnija pitanja na odbrani (i kratki odgovori)

**Definicija/anotacija**
- *Šta je klikbejt kod vas?* → manipulacija ka kliku kroz 4 mehanizma (kognitivni
  jaz, preuveličavanje, emocije, senzacionalizam); ne svodimo na površne signale.
- *Zašto je κ=0.64 dovoljno?* → iznad praga 0.6; neslaganja su na **suptilnim
  graničnim** slučajevima → potvrda da zadatak nije trivijalan.
- *Zašto 2200 a ne svih 2994?* → profesor je tražio balansiran skup ~1100/1100;
  balans je preduslov da accuracy bude smislena.

**Protokol/evaluacija**
- *Zašto nema train/test split-a?* → postavka propisuje **10-fold stratifikovanu
  CV** (+ nested CV za hiperparametre); CV deli podatke fold-po-fold bez curenja.
- *Kako sprečavate curenje?* → vektorizator/IDF se uče **unutar** svakog fold-a;
  hiperparametri biraju se u **unutrašnjoj** petlji nested CV.
- *Zašto baš F1 i AUC?* → klikbejt je pozitivna klasa; F1 balansira
  preciznost/odziv, AUC meri kvalitet rangiranja/verovatnoća.

**Baseline**
- *Zašto je NB najbolji baseline?* → kratki tekstovi, retke i visoko-dimenzionalne
  odlike; NB tu dobro radi i jak je sa malo podataka.
- *Efekat TF/IDF/TF-IDF?* → izmeren eksplicitno; na kratkim naslovima razlika mala
  (IDF ima malo prostora). TF-IDF jeste u vrhu, ali ne dominira — iskren nalaz.
- *Stem vs lemma?* → praktično izjednačeni; jeftin heuristički stemmer dostiže
  classla lematizaciju.

**Transformeri**
- *Kako radi BERT/fine-tuning?* → pretreniran MLM-om na ogromnom tekstu
  (samonadgledano), pa fino podešavamo na našim 2200 sa malim LR-om i
  klasifikacionim slojem na `[CLS]`. Transferno učenje.
- *Koliko epoha i zašto?* → 3–4; sa 2 nedotreniran. Varijante = zasebni
  fine-tuning-zi (svaki svoj LR-raspored).
- *Mono vs multi?* → BERTić (mono, BCMS) > mBERT na svim metrikama — namenski
  srpski model očekivano bolji.
- *Zašto je prvi run delovao sumnjivo?* → „brza" aproksimacija (jedan trening +
  eval po epohi) davala je obrnut trend zbog LR-rasporeda; zamenjeno zasebnim
  treninzima.

**Dekoder**
- *Zašto samo evaluacija?* → zatvoren/ogroman model, fine-tuning nemoguć.
- *SR vs EN — šta poredite?* → jezik **prompta**, ne naslova; naslovi su uvek
  srpski. Nalaz: SR ≈ EN.
- *Zašto Claude?* → „i drugi" dozvoljeni; Gemini besplatni tier nedostupan,
  ChatGPT se plaća; Claude jeftin (~$1) i validan.

**Sinteza**
- *Koji je model najbolji?* → zavisi od kriterijuma: F1 → Claude EN; accuracy+AUC
  i praktičnost → BERTić. Svi > baseline.

---

## 10. Mapa projekta (gde je šta)

```
data/annotated/dataset.tsv        finalni skup (2200, 1100/1100)
annotation/guidelines.md          uputstva za anotaciju (definicija klikbejta)
src/preprocessing/serbian.py      ćir→lat, lowercase, stem, classla lemma
src/baseline/run_baseline.py      LogReg + NB, nested CV, TF/IDF/TF-IDF
src/transformers/finetune.py      BERTić + mBERT fine-tuning, 10-fold CV, epohe
src/transformers/colab_train.py   pokretač za Google Colab (jedan fajl)
src/decoder/claude_eval.py        Claude evaluacija (ceo skup)
src/decoder/prompts.py            SR/EN × zero/few × def/nodef prompt varijante
results/                          svi CSV-ovi + izveštaji po fazama + sinteza
report/izvestaj.tex               finalni rad (Faza dokumentacije)
docs/Radni-izvestaj.md            detaljan dnevnik rada (dopuna ovom vodiču)
docs/Projekat-zahtevi.md          razrađeni zahtevi iz postavke
presentation/sazetak/             sažeci svih predavanja (teorija)
```

### Reprodukcija (komande)

```bash
# 3a baseline (lokalno)
.venv/bin/python src/baseline/run_baseline.py --full --normalize none stem lemma

# 3b enkoderski (Google Colab T4)
#   !python colab_train.py            (klonira repo, instalira, trenira oba modela)

# 3c dekoderski (Claude)
export ANTHROPIC_API_KEY=sk-ant-...
.venv/bin/python src/decoder/claude_eval.py --model claude-haiku-4-5 \
    --variants sr_zero_def en_zero_def
```
