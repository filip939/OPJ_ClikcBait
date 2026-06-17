# 2. Uvod u obradu prirodnih jezika

**Tema:** Definicija NLP-a, zašto je obrada jezika teška (kompleksnost, dvosmislenost), istorijat oblasti, konceptualni pristupi i metodologija razvoja statističkih rešenja (prikupljanje, anotacija, evaluacija).

---

## Šta je NLP
- **NLP (Natural Language Processing)** — oblast na raskršću računarskih nauka, veštačke inteligencije, mašinskog učenja, inženjerstva, lingvistike i kognitivne psihologije.
- Alternativni naziv: **računarska lingvistika** (computational linguistics).
- **Prirodni jezici** — jezici koje ljudi prirodno koriste za komunikaciju (engleski, srpski, japanski…), za razliku od veštačkih jezika (Morzeovi znaci, programski jezici).

## Čemu računarska obrada prirodnih jezika?
- Podaci na prirodnim jezicima (tekst) prisutni su svuda i ima ih sve više (knjige, časopisi, novine, email, društvene mreže).
- Najveći deo ljudskog znanja dostupan je **samo u nestrukturiranom tekstualnom obliku** (nasuprot strukturiranim izvorima poput relacionih baza).
- Tekstualni podaci imaju internu strukturu (lingvistička: sintaktička i diskursna; struktura formatiranja: pasusi, sekcije, poglavlja), ali se ona ne prevodi lako u mašinski čitljiv oblik.

## Zašto je obrada jezika teška?
- Velika kompleksnost, česte nejasnoće i dvosmislenosti/višesmislenosti.
- Razumevanje često zavisi od šireg **znanja o svetu** (world knowledge).
- Potpuno razumevanje jezika je **AI-potpun problem** — zahteva da računari dostignu ljudski nivo inteligencije; ne može se rešiti nekim uskim, jednostavnim algoritmom.

---

## Kompleksnost jezika
Aspekti kompleksnosti:
- **Morfološka** — više različitih oblika jedne iste reči.
- **Sintaktička** — više validnih sintaktičkih struktura za isti iskaz.
- **Semantička** — više značenja za jednu istu reč/iskaz.
- **Frazeologizmi i idiomi** — ustaljene jedinice čije se značenje ne može izvesti iz sastavnih reči: „carski rez", „kupiti mačku u džaku", „izvoditi besne gliste", „novinarska patka", „obrati zelen bostan", „slepi putnik".
  - Za razumevanje idioma često je neophodan **kulturološki kontekst** („lupati kao Maksim po diviziji", „razbiti kao bugarsku skupštinu", „Ahilova peta"; kineski „pritajeni tigar, skriveni zmaj"). Intuitivno za vlastitu kulturu, izuzetno teško za stranu (npr. *Star Trek TNG* epizoda „Darmok").

---

## Nejasnoće u izražavanju
- Nejasnoće su ponekad slučajne, ali vrlo često **namerne** (politika, reklame).
- Reklamni „verbalni mamci": „Traje X duže nego što ste očekivali (Fairy)", „Muzika nikada nije bolje zvučala (zvučnici)", „Vozite dalje, živite bolje (Renault)".
- Političke fraze: „nastavak strukturnih reformi", „treba ostaviti prošlost iza sebe", „neophodan je pragmatičan pristup" — kombinovanjem se dobijaju celi iskazi za koje je nejasno da li išta znače.

## Dvosmislenost i višesmislenost — tipovi
1. **Kategorijska** — isti oblik reči može biti više vrsta reči. „Gore, gore, gore, gore" (imenica/glagol/prilog/pridev). „Ona je bila mlada / nevesta / imala malo godina".
2. **Leksička**
   - **Polisemija** — više srodnih značenja (uočavanje sličnosti): „crkva" (građevina/institucija), „glava" (deo tela/strana novčića/deo knjige/rukovodilac), „miš" (životinja/uređaj).
   - **Homonimija** — više nepovezanih značenja: „sto" (nameštaj/broj), „pop" (sveštenik/muzički žanr), „zavijati" (umotavati/urlati).
3. **Sintaktička** — sekvenca reči ima više strukturnih tumačenja, često iz vezivanja predloško-padežnih konstrukcija: „Dve devojčice ujele meduze", „Veliki broj studenata ugrožava nastavu" (primeri R. Bugarski).
4. **Referencijalna** — više mogućih entiteta na koje se iskaz odnosi, često zbog elipse (izostavljanja reči): „Petar je javio Marku da je kupio auto / dobio posao" — ko?
5. **Pragmatička** — više mogućih ciljeva iskaza iako je osnovno značenje jasno; često nerešiva čak ni iz šireg konteksta: „Znate li koliko je sati?" (upit ili prekor), „Na putu sam" (napomena ili uveravanje).

- Većina iskaza sadrži bar neki oblik dvosmislenosti; ljudi je najčešće i ne primećuju, razrešavaju je kontekstom, znanjem o svetu i zdravorazumskim pretpostavkama. Svojstvo se koristi u šalama i vicevima.

---

## Istorijat obrade prirodnih jezika
- **1950 — Tjuringov test:** test inteligencije zasnovan na pisanoj komunikaciji u realnom vremenu; cilj — mašina prevari sudiju. Lebnerova nagrada (od 1991). Kasnije osporeno: **Kineska soba** (Džon Serl).
- **1957 — Noam Čomski, *Sintaksičke strukture*:** generativna gramatika (skup pravila za generisanje beskonačno mnogo ispravnih rečenica). Podela na **simboličku** i **stohastičku** paradigmu.
  - **Simbolička:** formalna teorija jezika, generativna sintaksa, algoritmi za parsiranje, rezonovanje/logika; prvi sistemi na ključnim rečima i heuristikama.
- **1966 — ELIZA (Vajzenbaum):** prvi NLP sistem za ograničenu konverzaciju; detekcija jezičkih obrazaca po ključnim rečima; imitirao psihoterapeuta.
- **Stohastička paradigma:** Bajesovske metode (autorstvo Federalističkih spisa); **Brown Corpus** (milion reči, različiti žanrovi); veliki uticaj na prepoznavanje govora (noisy channel, **skriveni Markovljevi lanci / HMM**).
- **1954 — Georgetown–IBM eksperiment:** demonstracija prevođenja ruski→engleski; preterana obećanja → **ALPAC** negativno mišljenje → pad finansiranja i usporen razvoj cele oblasti NLP-a.
- **1970-te:** modeli zasnovani na konačnim automatima i ručno pisanim pravilima (fonologija, morfologija, sintaksa); **SHRDLU (Vinograd)** — razumevanje jezika u svetu blokova.
- **Kasne 1970-e i 1980-e:** probabilistički modeli i modeli zasnovani na podacima → **„statistička revolucija"** (od 1990-ih): ogromne količine teksta sa interneta, jači računari, komercijalne primene; ML modeli i metodologija evaluacije postaju standard; razvoj rešenja i za jezike osim engleskog.
- **Danas:** prvi radovi o sentimentu (~2002), Apple Siri (2011), IBM Watson (Jeopardy), neuralne mreže u NLP-u (word2vec 2013, WaveNet, Google NMT, BERT 2018), pomak ka **multilingvalnim, kroslingvalnim i multimodalnim** rešenjima.

---

## Konceptualni pristupi obradi
- **Rule-based NLP** — simboličko procesiranje, konačni automati, logičko rezonovanje. Prilično tačno, ali **veoma krhko**: loše performanse van pokrivenih slučajeva; izrada baza znanja je naporna i traži ekspertsko znanje; jezik se menja → stalno ručno ažuriranje.
- **Statistical NLP** — daleko robusnije i fleksibilnije, ali zahteva (obično anotirane) podatke za uočavanje obrazaca; nadgledano mašinsko učenje, teorija verovatnoće.

> *„Every time I fire a linguist the performance of our speech recognition system goes up."* — Frederik Jelinek.
> Ispravan lingvistički tretman ne mora voditi praktičnom poboljšanju; s druge strane, odsustvo lingvističkog znanja ograničava obradu na rudimentarne inženjerske zadatke.

---

## Metodologija razvoja statističkih rešenja
Faze (iz doktorata V. Batanovića): **Prikupljanje tekstualnog sadržaja → Ekstrakcija i filtriranje → Anotacija podataka → Formulisanje, obučavanje i evaluacija modela.**

### Prikupljanje tekstualnog sadržaja
- Problem pronalaženja adekvatnih izvora. Mogu se iskoristiti postojeći skupovi/digitalizovane kolekcije (češće za velike svetske jezike) ili internet.
- Podaci za obuku treba da budu **iste prirode** kao oni na kojima će se model primenjivati.
- Alati za parsiranje HTML/JS: JSoup, BeautifulSoup, Scrapy, HTMLUnit.
- Za manje jezike (srpski) teško je naći dovoljno podataka; prikupljeni tekstovi se filtriraju.

### Anotacija podataka
- Obeležavanje podataka sistemom označavanja vezanim za problem.
- Neki zadaci (sentiment) ne traže domenske eksperte; drugi (parsiranje) traže ekspertsko lingvističko znanje.
- **Kvalitet anotacije je presudan**: detaljna i jasna uputstva + kvalitetni anotatori.
- **Slaganje anotatora = gornja granica performansi sistema.** Ako se ljudi ne slažu u X% slučajeva, ne treba očekivati bolji sistem.
- Metrike saglasnosti:
  - Procentualna saglasnost (ne uzima u obzir slučajnu saglasnost).
  - **Koenov κ (kappa), Skotov π** — kategoričke oznake, dva anotatora, uzimaju u obzir slučajnu saglasnost.
  - **Flajsov κ** — proširenje Skotovog π na više anotatora.
  - **Pirsonov / Spirmanov** koeficijent korelacije — realne numeričke oznake (vrednosti / rangovi).
  - **Kripendorfov α** — opšta i preporučena metrika nesaglasnosti; proizvoljan broj anotatora, razni tipovi oznaka (binarne, kategorijske, ordinalne, intervalske).

#### Koraci faze anotacije
1. **Odabir oznaka** (sa definicijama/interpretacijama; standardizovane ako postoje, ili razvoj novog sistema).
2. **Formulisanje uputstava** (detaljnija → veća konzistentnost, ali sporiji proces).
3. **Obučavanje anotatora i kalibracija** (anotacija probnog podskupa, razrešavanje nedoumica, dorada uputstava).
4. **Sprovođenje anotacije** (individualno; jednostruka vs višestruka; kod višestruke — *curation*, razrešavanje neslaganja).
5. **Analiza sprovedene anotacije** (konzistentnost, statistička analiza).
- Koraci se često preklapaju i ciklično povezuju. Anotacija se ponekad može **preskočiti/automatizovati** (npr. broj zvezdica kao oznaka sentimenta) — ali to ograničava fleksibilnost oznaka i može uneti šum.

### Formulisanje, obučavanje i evaluacija modela
- Statistički modeli zasnovani na **nadgledanom mašinskom učenju**; ulaz = anotirani podaci.
- Razmatraju se različite varijante modela i tehnike pretprocesiranja; tačan oblik zavisi od problema i konceptualnog pristupa.
