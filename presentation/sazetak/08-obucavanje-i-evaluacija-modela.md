# 8. Obučavanje i evaluacija modela (u nadgledanom mašinskom učenju)

**Tema:** Obučavanje i pojam modela, overfitting/underfitting, bias-variance kompromis, skup za testiranje/validaciju, stratifikacija, hiperparametri i njihova optimizacija, (ugnežđena) unakrsna validacija, metrike za regresiju i (binarnu/višeklasnu) klasifikaciju, baseline.

---

## Obučavanje modela
- **Obučavanje** = optimizacija modela korišćenjem raspoloživih parova (x, y).
- Cilj: pronaći **optimalnu hipotezu** — najsličniju pravoj funkciji preslikavanja x→y. Šta tačno znači optimizacija zavisi od konkretnog algoritma.
- Skup nad kojim se model optimizuje = **skup za obučavanje (training set)**.
- **Parametri** modela = faktori koje **sam algoritam** optimizuje tokom obučavanja.

### Šta je „model"?
- **Šire:** algoritam ML-a (npr. linearna regresija).
- **Uže:** konkretna funkcija preslikavanja (konkretna hipoteza) dobijena primenom algoritma na konkretan skup podataka.

---

## Evaluacija i prilagođenost podacima
- Kako znati da li je model A bolji od B? Evaluirati ih na **istom** skupu i uporediti metrike.
- **Nad kojim skupom?** Ne sme samo nad skupom za obučavanje.

### Underfitting i overfitting
- **Nedovoljna prilagođenost (underfitting):** model nije iskoristio podatke; hipoteza je **isuviše jednostavna** u odnosu na stvarnu funkciju; ne prati realne pravilnosti.
- **Preterana prilagođenost (overfitting):** hipoteza je **isuviše kompleksna**; model uočava pravilnosti i tamo gde ih nema (šum, slučajnost) → memoriše umesto da generalizuje.

### Šum u podacima
- Šum = neželjene anomalije (nepreciznost merenja, greške unosa/anotacije, subjektivnost…).
- Posledica: signal koji model treba da nauči postaje „zamagljen"; model može početi da **uči šum** → overfitting.

---

## Bias-variance kompromis
- Pronalaženje balansa underfitting↔overfitting = **kompromis između sistematskog odstupanja (bias) i varijanse**.
- **Greške zbog biasa** — posledica ograničene fleksibilnosti modela; model ne uči pravilnosti. Takvi modeli su u proseku **konzistentni ali netačni**.
- **Greške zbog varijanse** — posledica preterane osetljivosti; model pronalazi pravilnosti i u sitnim varijacijama. Takvi modeli su u proseku **tačni ali nekonzistentni**.
- **Zašto kompromis?**
  - Algoritmi sa **malom varijansom** (jednostavni, rigidni) → skloniji biasu. Npr. linearni modeli (linearna i logistička regresija).
  - Algoritmi sa **malim biasom** (fleksibilni, složeni) → skloniji varijansi. Npr. složene arhitekture neuronskih mreža.

---

## Skup za testiranje
- Obučen model je već prilagođen trening podacima → evaluacija nad istim podacima favorizuje složenije modele (bolje pamte šum).
- Za objektivnu procenu generalizacije potreban je **nov, nedirnut skup — skup za testiranje (test set)**.
- Početni skup se nasumično deli na trening i test. Česta podela **~70% / 30%**.
- **Stratifikacija** — pri podeli obezbediti istu raspodelu podataka u oba skupa (npr. ista frekventnost klasa kod klasifikacije; približno ista raspodela izlaznih vrednosti kod regresije).
- Ako **nema** overfitting-a: performanse na testu su slične ili blago niže od onih na treningu. Ako **ima**: primetno lošije na testu.

---

## Kako izbeći under/overfitting

**Underfitting:** odabrati dovoljno fleksibilan algoritam; odabrati pogodne odlike; pružiti modelu dovoljan broj kvalitetnih odlika.

**Overfitting:** izbegavati nepotrebno složene algoritme; koristiti **regularizaciju**; povećati broj trening podataka; eliminisati suvišne odlike; ako je obučavanje iterativno — **zaustaviti ga (early stopping)** kad model počne da overfituje. Za to je potrebno pratiti performanse na još jednom skupu — **skup za validaciju**.

---

## Validacija modela
- **Greška** modela nad podacima = odstupanje izlaza modela od tačnih odgovora (različiti algoritmi koriste različite funkcije greške).
- Pri iterativnom obučavanju greška na treningu kontinualno opada, ali greška na **drugom skupu** opada samo do neke tačke, pa počinje da raste → signal **ulaska u zonu overfitting-a**.
- Skup za validaciju mora biti **odvojen** od trening i test skupa. Ako bi se test koristio za validaciju, postao bi deo optimizacije → evaluacija više ne bi bila objektivna (rezultati bolji od realnih).
- Nema čvrstog pravila za podelu (npr. 60/20/20). Bitna je **stratifikovana** podela. Skup za validaciju = **skup za razvoj (development set, dev set)**.

---

## Hiperparametri i njihova optimizacija
- **Hiperparametri** = faktori ponašanja modela koje algoritam učenja **ne može** sam da optimizuje; zadaju se **ručno pre obučavanja**.
- Optimizacija: istraživanje kombinacija vrednosti; najjednostavnije — **pretraga po mreži (grid search)** (sistematski sve kombinacije).
- Hiperparametri se moraju optimizovati pomoću **validacije** (usvaja se set koji daje najbolje rezultate na validacionom skupu) — da bi evaluacija ostala nepristrasna.
- Optimizacija hiperparametara = i **odabir modela (model selection)** — biranjem vrednosti bira se i vrsta modela iz šire familije.

---

## Unakrsna validacija (cross-validation)
- Mane validacije pomoću jednog odvojenog skupa: (1) smanjuje količinu podataka za učenje; (2) optimalni hiperparametri zavise od nasumične podele (veća varijansa, naročito kad je malo podataka).
- **k-fold unakrsna validacija:** početni skup (bez test skupa) deli se na **k slojeva (folds)**; validacija se sprovodi u k prolaza — u svakom prolazu model se validira na jednom sloju, a obučava na svim ostalim. Rezultat = **prosek** po slojevima.
- Najčešće **stratifikovana** unakrsna validacija sa 5 ili 10 slojeva.
  - **Više slojeva** → duže traje, manja varijansa rezultata.
  - **Manje slojeva** → manje podataka po prolazu, veća varijansa.
- Na kraju se model testira na posebnom test skupu.

### Unakrsna validacija za evaluaciju
- Isti postupak može se koristiti i za **evaluaciju** (svi podaci se koriste → pouzdanija procena).
- **Terminološka zabuna:** treba razlikovati validaciju (deo optimizacije) od unakrsne validacije (metode sprovođenja validacije i/ili evaluacije).

### Ugnežđena unakrsna validacija
- Kad treba i validacija i evaluacija: **validacija u ugnežđenoj (unutrašnjoj), evaluacija u spoljnoj** unakrsnoj validaciji.
- Svi trening slojevi spoljne UV tretiraju se kao jedan skup koji se deli na nove slojeve u unutrašnjoj UV. Broj slojeva može se razlikovati (često manji unutra zbog brzine).

---

## Metrike — regresija
(niže vrednosti su bolje)
- **RMSE** (Root Mean Squared Error) — koren srednje kvadratne greške; najraširenija.
- **MAE** (Mean Absolute Error) — srednja apsolutna greška.
- **RRSE** (Root Relative Squared Error) — koren relativne kvadratne greške (u odnosu na srednju vrednost izlaza).
- **RAE** (Relative Absolute Error) — relativna apsolutna greška.
- RMSE/MAE: u **istim jedinicama** kao izlazna promenljiva (korisno kad se zna prihvatljiva greška). RRSE/RAE: **relativne, bez jedinice** → pogodne za poređenje između domena.

---

## Metrike — binarna klasifikacija
- **Matrica zabune (Confusion Matrix):** raspodela podataka po stvarnoj i predviđenoj klasi. Jedna klasa = pozitivna, druga = negativna.
  - **TP** (True Positives), **TN** (True Negatives), **FP** (False Positives — negativni pogrešno u pozitivne), **FN** (False Negatives — pozitivni pogrešno u negativne).
- **Tačnost (accuracy)** = (TP+TN)/ukupno. Korisna samo kad su klase **izbalansirane**.
  - Kod neizbalansiranih klasa tačnost je obmanjujuća — „model" koji sve svrsta u većinsku klasu dobija visoku tačnost (loše jer su greške nad malobrojnom klasom obično najvažnije; npr. detekcija sarkazma).
- **Preciznost (precision)** = TP/(TP+FP); **Odziv (recall)** = TP/(TP+FN).
- **F-mera (F1)** = harmonijska sredina preciznosti i odziva:
```
F1 = 2 · (precision · recall) / (precision + recall)
```
  - Kao pozitivna klasa uzima se **malobrojnija**. F-mera, preciznost i odziv **ne uzimaju u obzir TN** (tačno klasifikovane negativne).
  - Lako je optimizovati preciznost na uštrb odziva i obrnuto.

---

## Metrike — višeklasna klasifikacija
- **Tačnost** primenjiva kad je skup izbalansiran po klasama.
- **Mikro-uprosečavanje** — uprosečavanje **po podacima** (sabiraju se TP/FP/FN preko svih klasa pa se računa metrika).
- **Makro-uprosečavanje** — uprosečavanje **binarnih vrednosti metrika po klasama** (svaka klasa ista težina) → pogodnije za **neizbalansirane** skupove.
  - Postoji i varijanta makro-F-mere koja možda nije jednaka harmonijskoj sredini preciznosti i odziva.
- **Težinsko (weighted) uprosečavanje** — metrike po klasama ponderisane zastupljenošću klase.

---

## Procena performansi i baseline
- Da bi se procenilo koliko je model dobar, mora se uporediti sa **osnovnim (baseline)** pristupom.
- **Baseline pristupi:**
  - Klasifikacija: odabir **najfrekventnije klase**; odabir **nasumične klase**.
  - Regresija: predviđanje **srednje vrednosti** izlaza iz trening skupa.
- Navođenje samo rezultata modela bez poređenja sa baseline-om **nema smisla** (npr. tačnost 95% deluje dobro, ali ako 95% podataka pripada jednoj klasi, baseline već daje 95%).
- Ispitivanje baseline-a pomaže i u proceni da li je odabrana **metrika adekvatna**.
