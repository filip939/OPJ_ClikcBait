# Obrada prirodnih jezika — Projekat 2025/2026

> Razrađen pregled zahteva iz `Projekat 2025-2026.pdf`. Cilj: jasno znati **šta se tačno traži** u svakoj fazi.

---

## 🎯 Tema projekta

Izrada rešenja za **odabrani NLP zadatak nad tekstovima na srpskom jeziku**.

- **Slobodan izbor zadatka** u obradi prirodnih jezika.
- Može biti čest/popularan zadatak sa nivoa:
  - **morfologije**
  - **(morfo)sintakse**
  - **semantike**
  - …obrađen na predavanjima, ili noviji zadatak (npr. iz **SemEval** konferencija).
- Projekat se radi **grupno**.
- Implementacija u **bilo kom programskom jeziku / paketu** po izboru.
- Više grupa može raditi isti zadatak, ali sa **fokusom na različite tematske domene** (novinski, pravni, književni, itd.).

### Suština projekta (kompletan tok)
1. Prikupiti odgovarajući skup polaznih tekstova na srpskom iz odabranog domena.
2. **Ručno anotirati** prikupljene podatke na način primeren zadatku.
3. Iskoristiti taj skup za **obučavanje i evaluaciju nekoliko različitih statističkih modela**.

### ⚠️ Specijalan slučaj — zadatak već rađen za srpski
Ako zadatak **već ima rešenja na srpskom**, fokus MORA biti na **novom tematskom domenu**:
- Dozvoljeno je pratiti ranije standardizovan sistem prikupljanja/anotacije.
- Ali u fazi modela treba **dodatno razmotriti efekte promene domena**:
  - modele obučene na starom domenu evaluirati na novom domenu **i obrnuto**;
  - evaluacija mora sadržati **analizu povezanosti domena** i efekata te povezanosti na modele.
- 📉 Posledica na bodovanje: max bodovi za preuzetu fazu (prikupljanje/anotacija) se **umanjuju**, a za fazu modela se **uvećavaju**.

### ‼️ Pravilo o radu grupe
**Svi članovi učestvuju u SVIM fazama.** Nije dozvoljena podela posla po fazama (npr. jedan radi prikupljanje, drugi anotaciju).

---

## 📦 Faza 1 — Prikupljanje podataka (25 poena)

Formiranje **dovoljno velikog** skupa tekstova za odabrani domen, takvog da posle anotacije može da se koristi za obučavanje i evaluaciju.

### Zahtevi
- Pri izboru domena prvo proveriti **da li postoji dovoljno tekstova na srpskom** za taj problem.
- Izvor: **bilo koji javno dostupan veb sajt** sa sadržajem na srpskom.
- **Minimalan broj tekstova**: određuje se **zasebno za svaku grupu** u dogovoru sa predavačem (zavisi od zadatka i veličine grupe), nakon što grupa ispita dostupnost podataka.
- Dozvoljen poneki **termin na engleskom** unutar srpskog teksta (češće u tehničkim domenima).
- Finalni skup **pročistiti od duplikata** (isti tekst više puta).

### Format / tehnički zahtevi
- Tekstovi sačuvani kao **UTF-8 enkodovani TXT fajlovi**.
- Format pogodan za konkretan zadatak.
- U **metapodacima** za svaki tekst zabeležiti **URL ili jedinstveni identifikator izvora**.

### ✅ Checklist Faze 1
- [ ] Odabran tematski domen sa dovoljno dostupnih tekstova
- [ ] Dogovoren minimalan broj tekstova sa predavačem
- [ ] Prikupljeni tekstovi sa veb izvora
- [ ] Uklonjeni duplikati
- [ ] Sačuvano kao UTF-8 TXT
- [ ] Zabeleženi metapodaci (URL / ID izvora) za svaki tekst

---

## 🏷️ Faza 2 — Anotacija podataka (25 poena)

Ručno obeležiti svaki tekst prema NLP zadatku, koristeći **adekvatnu šemu oznaka/ocena**.

- Pri izboru/formiranju šeme: dozvoljeno konsultovanje **naučnih radova**, ali se očekuje i **uvid u konkretne podatke** (radi potpunosti).
- Alat za anotaciju: dozvoljen (postojeći ili sopstveni), ali **nije obavezan**.

### Standardna metodologija anotacije (5 koraka)
1. **Odabir oznaka** — definisanje skupa oznaka/ocena.
2. **Formulisanje uputstava za anotaciju**:
   - jasne definicije svake oznake;
   - usaglašene instrukcije za **problematične situacije**.
3. **Kalibracija**:
   - mali podskup (**~10% ukupnog broja**) anotiraju **SVI članovi paralelno**, zasebno i **bez konsultacija**;
   - ako se uoče nedostaci u oznakama/uputstvima → **vratiti se na prethodni korak**.
4. **Sprovođenje anotacije**:
   - podatke **ravnomerno rasporediti** — svako anotira ~istu količinu;
   - glavni set: **jednostruka** anotacija (očekivano), ali višestruko paralelno označavanje **nije zabranjeno** ako podiže konzistentnost.
5. **Analiza anotacije**:
   - **saglasnost anotatora** na osnovu kalibracionog skupa:
     - stepen saglasnosti **između svaka dva člana**,
     - **grupni prosek** binarnih stepena saglasnosti;
   - **statistička analiza** oznaka u finalnim podacima.

### Format / čuvanje
- Anotirani podaci: **UTF-8 TXT**, u standardnom formatu za zadatak.
- **Kalibracioni skup čuvati zasebno** — sa onoliko anotacija koliko ima članova grupe; sve anotacije u **istom formatu zapisa**.

### ✅ Checklist Faze 2
- [ ] Definisana šema oznaka (uz uvid u radove i podatke)
- [ ] Napisana uputstva za anotaciju (definicije + problematični slučajevi)
- [ ] Kalibracija na ~10% — svi članovi nezavisno
- [ ] Izmereni inter-annotator agreement (parovi + grupni prosek)
- [ ] Po potrebi revidirane oznake/uputstva i ponovljena kalibracija
- [ ] Ravnomerno raspoređena i sprovedena glavna anotacija
- [ ] Statistička analiza finalnih oznaka
- [ ] Glavni set i kalibracioni set sačuvani zasebno (UTF-8 TXT, isti format)

---

## 🤖 Faza 3 — Obučavanje i evaluacija statističkih modela (40 poena)

Razmotriti **dva tipa modela**.

### Tip 1 — Osnovni (baseline) modeli — *20 poena*
- Jednostavni / linearni modeli kao baseline.
- Primeri:
  - **klasifikacija teksta** → linearni klasifikatori sa ručno definisanim odlikama (**logistička regresija**, **SVM**);
  - **sekvencijalni zadaci** (npr. **NER**) → iste metode uz zasebne predikcije po tokenu.
- Obučavanje/evaluacija moguća lokalno na **CPU**.
- Izbor konkretnih modela → **u konsultaciji sa predavačem**.
- Razmotriti efekte **pretprocesiranja** (zavisno od zadatka):
  - **lowercasing**, **TF**, **IDF**, **TFIDF** ponderisanje, itd.

### Tip 2 — Veliki jezički modeli (Transformer) — *20 poena*
Razmatra se **jedan ili oba** podtipa (zavisno od veličine grupe i kompleksnosti):

#### a) Enkoderski LLM (fine-tuning)
- **Monolingvalni**: npr. **BERTić**.
- **Multilingvalni**: npr. **multilingual BERT**, **XLM**, …
- ⚠️ Potrebno **bar jedan mono- i jedan multilingvalni** model.
- Preporučene biblioteke: **Huggingface Transformers** ili **Simple Transformers**.
- Modele **fino podesiti (fine-tuning)** za zadatak, pa evaluirati.
- Zahtevaju **GPU** sa dovoljno VRAM-a (najčešće **≥ 8 GB**).
- Preporuka: **Google Colab** ili **studentski krediti na MS Azure**.

#### b) Dekoderski / generativni LLM (samo evaluacija)
- Predstavnici: **ChatGPT**, **Gemini** (dozvoljeni i drugi).
- Veličina + zatvorenost → **fine-tuning nemoguć** → samo **evaluacija**.
- Razmotriti:
  - efekte različitih **formata upita (prompt engineering)**;
  - efekte **jezika upita** (engleski / srpski).

> Konkretan izbor svih modela zavisi od zadatka i utvrđuje se **u konsultaciji sa predavačem prilikom prijave**.

### 📐 Protokol evaluacije (vrlo bitno)
| Model | Validacija | Hiperparametri / varijante |
|---|---|---|
| **Osnovni modeli** | **10-slojna stratifikovana unakrsna validacija** | optimizacija glavnih hiperparametara (npr. jačina regularizacije) preko **ugnežđene (nested) unakrsne validacije** |
| **Enkoderski LLM** | **10-slojna stratifikovana unakrsna validacija** | evaluacija **različitih varijanti po broju epoha** (dužina fine-tuninga) |
| **Dekoderski/generativni LLM** | — | **ceo skup podataka** koristi se za evaluaciju |

- Koristiti **odgovarajuću metriku** za merenje performansi (zavisno od zadatka).

### ✅ Checklist Faze 3
- [ ] Izabrani osnovni modeli (uz predavača)
- [ ] Razmotreni efekti pretprocesiranja (lowercasing/TF/IDF/TFIDF)
- [ ] Osnovni modeli: 10-fold stratifikovana CV + nested CV za hiperparametre
- [ ] Enkoderski: ≥1 mono (BERTić) + ≥1 multilingvalni (mBERT/XLM)
- [ ] Enkoderski: fine-tuning + 10-fold CV + varijante po broju epoha
- [ ] (Opciono/po dogovoru) Dekoderski: prompt engineering + EN/SR upiti, evaluacija na celom skupu
- [ ] Rezultati prikazani sa odgovarajućim metrikama

---

## 📝 Projektna dokumentacija (15 poena)

Detaljno opisati **svaku fazu**:

- **Faza 1**: proces prikupljanja, izvori, korišćeni kriterijumi, tehnička strana procesa.
- **Faza 2**: detaljan opis anotacije, **uputstva za anotaciju**, tehnička strana označavanja.
- **Deskriptivni statistički prikaz** prikupljenih i anotiranih podataka.
- **Faza 3**: **pregledan tabelarni prikaz rezultata** različitih (varijanti) modela i efekata podešavanja + **analiza i diskusija** rezultata.

> ❌ Dokumentacija **NE treba** da sadrži iskopirana detaljna objašnjenja tehnika/algoritama iz nastavnih materijala.

---

## 📋 Propozicije i prijava

### Veličina grupe
- **Optimalno: 4 studenta**; dozvoljeno **3 ili 5**.

### Prijava grupe
- Obavezna pre početka rada, **mejlom**: **vuk.batanovic@etf.bg.ac.rs**
- Prijava sadrži:
  - spisak članova grupe,
  - izbor **NLP zadatka** i **tematskog domena**,
  - spisak **izvora podataka**,
  - **procenu veličine** skupa podataka,
  - spisak **modela** koje grupa planira.
- Predavač dodeljuje zadatak/domen ako nije zauzet od ranije prijavljene grupe.

### Individualne prijave
- Mogu ako se grupa ne formira → predavač organizuje u grupe.
- Individualno prijavljeni **nemaju mogućnost izbora** zadatka/domena.

### ⏰ Rokovi
| Stavka | Rok |
|---|---|
| Individualne prijave | **01.07.2026.** |
| Prijava grupa | **01.08.2026.** |
| Slanje rešenja + dokumentacije | **do početka ispitnog roka** u kom se brani |

- Prijave posle rokova **se ne uzimaju u obzir**.
- Postavka projekta važi **do prolećnog semestra naredne školske godine**.
- Odbrane: u svim ispitnim rokovima za predmete letnjeg semestra.

---

## 🧮 Bodovanje (skala 0–100)

| Stavka | Poeni |
|---|---|
| Faza 1 — prikupljanje podataka | **25** |
| Faza 2 — anotacija podataka | **25** |
| Faza 3 — obučavanje i evaluacija | **40** (20 osnovni + 20 LLM) |
| Kvalitet i potpunost dokumentacije | **15** |
| **Ukupno** | **100** |

### ⚠️ Uslovi za prolaz
- Za **svaku od prve tri stavke** potrebno **bar 50% od max poena** te stavke.
- **Nije moguće odbraniti** projekat bez sprovođenja i opisivanja **sve tri faze**.
- Ako je metodologija prikupljanja/anotacije **direktno preuzeta** (već rađen domen za srpski): max za tu fazu **umanjen**, max za Fazu 3 **uvećan**.

---

## 🚀 Predloženi redosled koraka

1. Dogovor u grupi → izbor zadatka + domena + izvora + modela.
2. Provera dostupnosti podataka na internetu.
3. **Prijava grupe** mejlom (do 01.08.2026) → dobijanje zvaničnog zadatka/domena + dogovor o min. broju tekstova.
4. **Faza 1**: scraping/prikupljanje → čišćenje duplikata → UTF-8 TXT + metapodaci.
5. **Faza 2**: oznake → uputstva → kalibracija (10%, svi) → agreement → glavna anotacija → analiza.
6. **Faza 3**: baseline (10-fold + nested CV) → enkoderski LLM (fine-tuning, mono+multi, epohe) → (opciono) generativni LLM (prompt eng., EN/SR).
7. **Dokumentacija**: opis svih faza + statistika + tabele rezultata + diskusija.
8. Slanje rešenja + dokumentacije pre ispitnog roka → odbrana.
