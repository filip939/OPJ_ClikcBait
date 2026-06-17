# 9. Zadaci u obradi prirodnih jezika

**Tema:** Pregled NLP zadataka kroz hijerarhiju jezičkih nivoa — od obrade signala i tokenizacije, preko jezičkih modela, morfologije i sintakse, do semantike, klasifikacije, sentimenta, NER-a, dohvatanja informacija, čet-botova, mašinskog prevođenja i sumarizacije.

---

## Hijerarhija NLP zadataka
Proučavanje jezika deli se na šest podoblasti:
1. **Fonetika/fonologija** — lingvistički zvuci.
2. **Morfologija** — oblici reči.
3. **Sintaksa** — strukturni odnosi između reči.
4. **Semantika** — značenje reči (leksička) i sekvenci reči (kompoziciona).
5. **Pragmatika** — način na koji se jezik koristi u komunikaciji.
6. **Diskurs** — jedinice šire od pojedinačnog iskaza.

---

## Prepoznavanje govora
- Zadatak: pretvoriti audio signal sa govorom u tekst.
- Na raskršću NLP-a (tekst) i obrade signala.
- Rešava se **modelima sekvenci**: HMM, **CRF (Conditional Random Fields)**, neuralne mreže.

## Segmentacija teksta na rečenice
- Obično prvi korak pipeline-a. Pre toga — filtriranje (uklanjanje XML/HTML tagova, boilerplate-a).
- Heuristički (regularni izrazi) → tačnost ~95%; najbolji rezultati nadgledanim ML-om nad velikim korpusom (~99%).
- Interpunkcija često označava kraj rečenice, ali se javlja i drugde: redni brojevi, decimalni brojevi, skraćenice (dr., npr.), inicijali, URL/IP adrese, emotikoni, brendiranje (npr. „hashSIGN"). Dodatno: izuzeci se ponekad jave i kad je zaista kraj rečenice.

## Tokenizacija
- Podela teksta na **tokene** (reči, brojevi, URL-ovi…). Interpunkcija = posebni tokeni (nekad se odbacuju), ali je ponekad integralni deo tokena (O'Nil, Pol Sartr, T-Mobile…).
- Heuristike (regex, ručna pravila) ili ML nad velikim korpusom.
- **Najjednostavnija:** po blanko znakovima (whitespace tokenization) — neprimenjivo na jezike bez razmaka (kineski, japanski, tajlandski).
- Teža kad tekst nije „čist" (npr. OCR izlaz).
- Segmentacija na rečenice i tokene = **preduslov skoro svih drugih obrada**; greške se **propagiraju** na složenije zadatke.

---

## Jezički modeli
- Služe za **probabilističko modelovanje jezika**: kolika je verovatnoća da se rečenica javi u jeziku?
- Rečenica = sekvenca tokena; verovatnoća se računa lančanim pravilom, na osnovu frekvencija sekvenci tokena u velikom korpusu.
- Posebni tokeni za početak/kraj rečenice (`<s>`, `</s>`).
- Problem **proređenosti** — duge sekvence se javljaju retko.
- **Markovljeva pretpostavka:** verovatnoća tokena zavisi samo od prethodnih n tokena.
  - **Unigramski** — svaki token zasebno (relativna frekvencija); ignoriše sekvencijalne zavisnosti.
  - **Bigramski** — zavisnost od prethodnog tokena; realnija aproksimacija.
  - **Tri-/n-gramski** — sekvence od n uzastopnih tokena.
- **Problem n-gramskih modela:** neviđene sekvence → verovatnoća 0. Rešenje: **poravnanje (smoothing)** — dodeljuje malu nenultu verovatnoću:
  - Laplasovo (brojanje počinje od 1), **Good-Turing**, **Kneser-Ney**. Takođe: interpolacija, backoff.
- **Perpleksnost (perplexity)** — **intrinzička** mera kvaliteta (inverzna verovatnoća test podataka, normalizovana brojem reči). **Niža perpleksnost = bolji model.** Nije zamena za **ekstrinzičku** evaluaciju (performanse na konkretnom NLP zadatku).
- **Primene:** korekcija pravopisa („debeo put" vs „debeo prut"), redijakritizacija („poste" vs „pošte"). Ne mogu uvek dati tačan odgovor (npr. „najlepše zelje/želje").

### Neuralni jezički modeli
- Pored klasičnih n-gramskih: **RNN/LSTM** arhitekture, danas **Transformer**.
- Umesto klasične tokenizacije — **mikro-tokenizacija**: **BPE (Byte Pair Encoding)**, **WordPiece**.
- Predstavnici: **GPT** porodica (GPT-2, GPT-3, ChatGPT, GPT-4). Najpoznatija biblioteka: **Hugging Face Transformers**.
- **Masked Language Models (MLM)** — predviđanje bilo koje izostavljene reči (ne samo sledeće); koristi se pri obučavanju **BERT**-a. Lako se konstruiše ogroman broj primera iz neanotiranih korpusa → **samonadgledano učenje**.
- Dovoljno veliki modeli (milijarde parametara, ogromni korpusi) stiču **robusno opšte znanje o jeziku**.
- **Prethodno obučeni (pretrained) modeli** → **fino podešavanje (fine-tuning)** za konkretne zadatke uz malo anotiranih primera = **transferno učenje** (danas dominantna paradigma). Najveći modeli pokazuju i **zero-shot** sposobnosti.

---

## Morfološka normalizacija
- U morfološki bogatim jezicima (srpski) ista reč ima mnogo oblika (padeži, rodovi, brojevi, lica). Računari ne razlikuju oblike iste reči od različitih reči.
- **Problem:** povećanje proređenosti (svaki oblik = posebna reč) — naročito kod malih skupova.
- **Rešenje:** svođenje oblika na zajedničku osnovu — morfološka normalizacija.

### Vrste morfoloških promena
- **Flektivna morfologija** — različiti oblici iste reči (npr. padeži: škola, škole, školu…).
- **Derivaciona morfologija** — izvođenje novih reči: sufiksacija (škola → školski, školarac…), prefiksacija (prijatelj → neprijatelj), slaganje/kompozicija (severoistok, ribolov), kombinovano.
- Pri promenama dolazi i do **glasovnih promena** (nepostojano „a", palatalizacija, sibilarizacija…).

### Dva pristupa
- **Stemovanje** — odsecanje krajeva reči → **stem**; alati = **stemeri** (npr. **Porterov** za engleski).
  - Blisko traženju korena, ali **bez lingvističkog znanja**; ne poznaju koncept sufiksa (npr. „-ski" jeste sufiks u „dramski", nije u „Vronski"). Ne uzimaju kontekst (svaka reč zasebno). Implementacija: liste pravila / regex; brzi alati. Moguće greške zbog **prejakog/preslabog** stemovanja.
- **Lematizacija** — zamena oblika reči **lemom** (osnovni rečnički oblik: nominativ jednine za imenice, infinitiv za glagole…); alati = **lematizatori**.
  - Složenije od stemovanja; ML modeli + morfološki rečnici. **Zahteva kontekst** (npr. „sedam" = broj ili glagol „sedati"). Sporiji od stemera.

## Obeležavanje vrste reči (POS tagging)
- Označavanje glavne kategorije reči (glagol, imenica, pridev…). Skup oznaka = **tagset** (ne mora odgovarati lingvističkim kategorijama).
  - Engleski: **Penn Treebank POS Tagset**. Srpski: **MULTEXT-East**.
- Obično se sprovodi pre lematizacije (vrsta reči pomaže odrediti lemu). Implementacija: **modeli sekvenci**.

## Obeležavanje morfosintaktičkih osobina reči
- Srodno POS-u, ali detaljnije: podvrsta + osobine (padež, rod, broj, lice…). Skup opisa = **morfosintaktički deskriptor (MSD)**.
- Zavisi od jezika i tagseta; važan za morfosintaktički bogate jezike. Srpski: **MULTEXT-East**. Slične tehnike kao POS.

## Parsiranje
- Analiza gramatičke strukture rečenice i raščlanjivanje na sintaksne delove uz označavanje odnosa. Parseri označavaju subjekat, objekat, glagol, atribute… koristeći gramatički formalizam.
- Dva tipa:
  - **Konstituentsko** — zasnovano na konstituentskim gramatikama; kreira **sintaksno stablo** (reči = listovi). Oznake (engl.): N (imenica), V (glagol), D (član), NP (imenička sintagma), VP (glagolska sintagma), S (rečenica).
  - **Dependencijalno** — zasnovano na dependencijalnim gramatikama; stablo sintaksnih zavisnosti između parova reči (svaka zavisnost: upravna + zavisna reč; glagol = sintaktički centar klauze). **Danas dominantno.**
- Projekat **Universal Dependencies** — isti skup osnovnih oznaka za parsiranje svih jezika.

---

## Leksička semantika
- Za zadatke višeg nivoa potrebno je značenje reči. Dobija se:
  - **Eksplicitno** — preko **baza znanja**.
  - **Implicitno** — preko praćenja upotrebe u korpusima = **distribuciona semantika**.

### WordNet
- Najpoznatija baza znanja o značenjima reči (definicije, primeri). Reči sličnog značenja grupisane u **synsets** (skupove sinonima); između njih hijerarhijski odnosi (**hipernim/hiponim**) i druge relacije → veliki **graf** reči. Semantička bliskost = udaljenost u grafu.

### Distribuciona semantika
> *„You shall know a word by the company it keeps."* — J. R. Firth.
- **Distribuciona hipoteza:** reči sličnog značenja javljaju se u sličnim kontekstima (slična distribucija). Značenje se izvodi iz konteksta upotrebe; potreban veliki neanotiran korpus.
- Primer: iz dovoljno primera nepoznate reči „bardiwac" zaključuje se da je u pitanju sorta vina.
- **Matrica zajedničkog javljanja (co-occurrence matrix):** redovi = posmatrane reči, kolone = kontekstne reči (nekoliko reči sa obe strane). Kontekst može biti i ceo dokument (**LSA — Latent Semantic Analysis**). Zbog veličine — redukcija dimenzionalnosti.

### Vektori značenja reči (word embeddings)
- Niskodimenzionalni vektori fiksne dužine koji reprezentuju semantiku reči; slične reči → slični vektori (bliski u semantičkom prostoru). Udaljenost: **kosinusna sličnost**.
- Dimenzije ose obično nemaju jasno značenje, ali položaji omogućavaju **rezonovanje analogijama** (npr. kralj − muškarac + žena ≈ kraljica).
- Algoritmi:
  - **GloVe** (Global Vectors) — zasnovan na brojanju (matrica zajedničkog pojavljivanja).
  - **word2vec** — neuralni **prediktivni** model: **CBOW** (iz konteksta predviđa reč) i **Skip-gram** (iz reči predviđa kontekst). Pokazano da word2vec i GloVe suštinski rešavaju isti problem.
  - **fastText** — unapređenje skip-grama; reči = skupovi znakovnih n-grama → bolje na morfologiji, blago lošije na semantici.
- **Statički** vektori (klasični) — isti za sve upotrebe reči (npr. „sto" obuhvata i nameštaj i broj). **Kontekstno osetljivi (contextual embeddings)** — različiti vektori za istu reč zavisno od konteksta, dinamički se računaju (BERT, GPT…).

---

## Klasifikacija tekstova
- Zadatak: svrstati tekst u jednu od predefinisanih kategorija (po temama, autorstvu, detekcija spama; sentiment je čest specijalan slučaj).
- Modeli: naivni Bajes, logistička regresija, SVM. Potrebna ručna anotacija trening podataka.
- **Bag-of-words (BOW)** — tekst kao neuređen skup reči (ignoriše redosled); svaka reč = odlika. Dobar za duže tekstove; mogu se koristiti i sekvence reči (n-grami) i odlike iz vektora značenja.
- Pretprocesiranje: tokenizacija, (opciono) morfološka normalizacija, (opciono) uklanjanje **stop reči** (vrlo česte funkcionalne reči — predlozi, veznici, uzvici, rečce — koje ne nose semantiku; moguće i domenske stop reči).

---

## Analiza sentimenta
- Zadatak: odrediti sentiment u tekstu. Najčešće klasifikacija (pozitivno/negativno/neutralno) ili numerička skala (npr. 1–5).
- Nivoi granularnosti: **dokument**, **rečenica/paragraf**, **aspekt**.

### Aspektna analiza sentimenta
- **Aspekt** = element prema kome se izražava sentiment (ličnost, pojava, događaj, tema, svojstvo…). Primer: „Hrana je bila odlična, ali je usluga spora."
- Osnovni elementi: **aspektni izraz** (reč prema kojoj se sentiment izražava), **izraz ispoljavanja sentimenta** (opinion term), **aspektna kategorija** (npr. „hrana" pokriva više termina), **polarnost** (pozitivna/negativna/neutralna).
  - Primer: „Roštilj im je izvrstan" → aspektni izraz: roštilj; kategorija: hrana; opinion term: izvrstan; polarnost: pozitivna.

### Konceptualni izazovi
- Šta tačno spada u neutralnu klasu (objektivni tekstovi i/ili mešavina)? Kako obeležiti dvosmislene tekstove? Kako pouzdano prepoznati **sarkazam** (često preko tona)? Granularnije posmatranje olakšava konzistentnu anotaciju.

### Pristupi i osobine
- Dominantno: nadgledano ML. Dopunski: **sentiment leksikoni** (rečnici reči sa polarnošću i jačinom; npr. **SentiWordNet** iz WordNeta).
- **Domenski osetljiv** problem: ista reč/izraz ima različitu konotaciju u različitim domenima (npr. „pročitajte knjigu" — pozitivno u recenziji knjige, negativno u recenziji filma po knjizi).
- Komercijalno izuzetno atraktivno. Srodni složeniji problemi: klasifikacija po **subjektivnosti**, **prepoznavanje emocija** (ljutnja, radost, žalost…), **detekcija stavova** (slaganje/neslaganje), **detekcija sarkazma**.

---

## Prepoznavanje imenovanih entiteta (NER)
- Prepoznavanje imena entiteta i označavanje tipa. Glavne kategorije: **PER** (osobe), **LOC** (lokacije), **ORG** (organizacije); moguće dodatne (vremenski izrazi, prisvojni oblici…).
- Komplikovanije od detekcije vlastitih imenica (npr. „Trg republike" jeste entitet iako su sastavne imenice zajedničke).
- **BIO sistem anotiranja tokena:** **B** (begins — početak entiteta), **I** (inside — pripada započetom entitetu), **O** (outside — ne pripada nijednom). Tretira se kao klasifikacija token-po-token ili kao označavanje sekvence.
- Odlike: sadržaj tokena, lema, vrsta reči, MSD, kapitalizacija…

---

## Dohvatanje informacija (Information Retrieval)
- Zadatak: pronaći izvore informacija (dokumente, najčešće tekst) koji zadovoljavaju potrebu korisnika, obično iz velike kolekcije.
- Korisnik formuliše **upit**; sistem poredi upit sa indeksom dokumenata i vraća relevantne. Cilj: vratiti **sve** relevantne i **nijedan** irelevantan.
- **Model vektorskog prostora:** dokumenti i upiti kao BOW vektori; sličnost (euklidska, **kosinusna**, Menhetn). Indeksiranje koja reč je u kom dokumentu; moguće filtriranje (stop reči) i ponderisanje reči.
- **Ponderisanje:**
  - **TF (Term Frequency)** — relevantnost raste sa frekvencijom reči iz upita, ali **logaritamski** (ne linearno): `tf = 1 + log(count)` (0 ako count=0).
  - **IDF (Inverse Document Frequency)** — reči u svim dokumentima manje su važne od retkih; retkim rečima veća težina: `idf = log(N / n)`, gde je N ukupan broj dokumenata, n broj dokumenata sa rečju.
  - **TF-IDF** = tf · idf — težina raste sa učestalošću i retkošću. Često i u drugim NLP problemima (klasifikacija).
- **Metrika MRR (Mean Reciprocal Rank):** `MRR = (1/Q) Σ 1/rankᵢ`, gde je rankᵢ rang prvog tačnog odgovora za upit i. Relevantnost binarna; ignoriše sve relevantne odgovore osim prvog.

---

## Čet-botovi
- **Čet-bot** = dijaloški sistem; ogroman raspon složenosti.
  - Najjednostavniji: prepoznavanje ključnih reči.
  - Najsavremeniji: konverzacioni LLM-ovi (ChatGPT, Google Bard) + **reinforcement learning** za kvalitet.
- Tipični podzadaci:
  - **Prepoznavanje namere (intent recognition)** — kategorizacija cilja poruke.
  - **Prepoznavanje imenovanih entiteta**.
  - **Upravljanje dijalogom** — često kretanje kroz predefinisana stanja u konverzacionom grafu (praćenje prethodnih interakcija).
  - **Odgovaranje na pitanja (question answering)** — složeniji oblik dohvatanja informacija.
  - **Generisanje odgovora** — zasnovano na pravilima/šablonima ili na naprednim tehnikama **generisanja prirodnog jezika (NLG)**.

---

## Određivanje semantičke sličnosti tekstova
- Zadatak: za dva teksta odrediti stepen semantičke sličnosti na skali (npr. 0–5).
- Cilj: prepoznati blizak smisao iako se leksika/sintaksa razlikuju („Ubrzo će doći do poskupljenja struje" ≈ „Cena električne energije će uskoro porasti").
- Netrivijalno, naročito za kratke tekstove. Većina pristupa: vektorska reprezentacija svakog teksta + poređenje vektora. Važno za pretragu/IR, sumarizaciju, QA.

---

## Mašinsko prevođenje
- Zadatak: prevesti iskaz uz očuvanje semantike i prirodnosti.
- **Problemi:** kompleksnost/višesmislenost jezika (npr. razrešavanje „it" zavisi od konteksta); razlike u gramatici i **redosledu reči** (engleski SVO, japanski SOV, srpski u principu slobodan, najčešće SVO).
- Pristupi:
  - **Statističko (SMT)** — paralelni korpusi kao primeri prevoda (rani: engleski–francuski iz kanadskog parlamenta; transkripti evropskog parlamenta).
  - **Phrase-based** (state-of-the-art do skoro) — prevode se grupe reči (izrazi), ne pojedinačne reči.
  - **Neuralno (NMT)** (state-of-the-art danas) — **sequence-to-sequence** modeli: tekst se enkoduje u vektor, pa dekodira u izlazni jezik; dužine ulaza/izlaza mogu se razlikovati.

---

## Sumarizacija teksta
- Zadatak: proizvesti skraćenu verziju teksta sa bitnim informacijama (primeri: novinski naslovi, apstrakti, opisi knjiga). Može biti nad jednim ili više dokumenata.
- Po tipu:
  - **Ekstraktivna** — sadrži neizmenjene delove polaznog teksta.
  - **Apstraktivna** — generiše bar delimično nov sadržaj (obuhvata **NLG — Natural Language Generation**).
  - **Generička** (ceo sadržaj) vs **upitno-orijentisana** (delovi relevantni za upit).
- Osnovni algoritam ekstraktivne sumarizacije: odrediti relevantnost svake rečenice (nadgledano/nenadgledano), odabrati najrelevantnije i eliminisati redundantnosti, odrediti redosled.

---

## Ostali NLP zadaci
Razrešavanje koreference/anafora, simplifikacija teksta, ekstrakcija odnosa između entiteta, ekstrakcija ključnih reči, modelovanje tema…
- Često se formulišu novi zadaci ili varijante starih (npr. NER u biomedicini). Popularizuju se kroz **deljene zadatke (shared tasks)** — javna međunarodna takmičenja timova; istraživačkoj zajednici se daje pristup anotiranim podacima.
