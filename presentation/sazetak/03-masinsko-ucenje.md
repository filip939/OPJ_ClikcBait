# 3. Mašinsko učenje

**Tema:** Uvod u mašinsko učenje, tipovi učenja (nadgledano, nenadgledano, samonadgledano, polunadgledano, učenje sa podrškom), odlike, tipovi problema (regresija, klasifikacija, strukturna predikcija) i grupisanje.

---

## Šta je mašinsko učenje
- Arthur Samuel: *„Field of study that gives computers the ability to learn without being explicitly programmed."*
- Kombinacija primenjene statistike, veštačke inteligencije, matematičke optimizacije, računarskih nauka.

### Čemu mašinsko učenje?
- Problemi koje je teško ručno definisati (klasično programiranje nije moguće).
- Izvlačenje korisnih informacija iz velikih količina sirovih podataka ili predviđanje trendova (**data mining, predictive analytics**) — ručna analiza nemoguća ili presporo.
- Kompleksni sistemi koji se dinamički prilagođavaju okruženju.

**Primeri primena:** NLP, detekcija spama, analiza sentimenta, mašinsko prevođenje, računarski vid (OCR, prepoznavanje lica/pokreta), robotika, dijagnoza u medicini (CAD), igranje igara (Go — DeepMind AlphaGo).

---

## Tipovi mašinskog učenja
- **Nadgledano** (supervised)
- **Nenadgledano** (unsupervised)
- **Samonadgledano** (self-supervised)
- **Polunadgledano** (semi-supervised)
- **Učenje sa podrškom** (reinforcement learning)

---

## Nadgledano učenje
- Najčešće primenjivan tip.
- Svakom ulaznom podatku **x** pridružena je željena izlazna vrednost **y** koju model treba da predvidi.
- Cilj: na osnovu parova (x, y) pronaći optimalnu funkciju koja mapira ulaz → izlaz.
- Realna funkcija preslikavanja je nepoznata; funkcija koja se optimizuje zove se **hipoteza** h(x).
- Model određuje **opšti oblik** funkcije (npr. linearna funkcija = prostor mogućih hipoteza); konkretne vrednosti podataka pri obučavanju određuju **najbolju hipotezu** u tom prostoru.

### Odlike (atributi / features)
- U klasičnom ML-u treba **ručno specificirati** faktore u ulaznim podacima koji utiču na izlaz — to su **odlike/atributi**.
- Svaki podatak se tretira kao vektor odlika: **x = (x₁, x₂, …, xₙ)**.
- U **dubokom učenju** model sam pronalazi relevantne odlike — ali treba naći odgovarajuću strukturu modela za svaki problem.

### Generalizacija
- Cilj: model daje dobre rezultate ne samo na trening podacima već i na **novim, neviđenim** podacima — to je **sposobnost generalizacije**.

### Tipovi izlazne vrednosti y
- **Kontinualna** → problem **regresije**.
- **Diskretna/kategorička** → problem **klasifikacije**.
  - Dve klase → **binarna klasifikacija**.
  - Više klasa → **višeklasna klasifikacija**.
- **Strukturirana** → problem **strukturne predikcije**.

> Veliki broj NLP zadataka svodi se na neki vid klasifikacije ili strukturne predikcije.

---

## Strukturna predikcija
- **Strukturirani podatak** se sastoji iz više delova; bitan je ne samo sadržaj delova nego i **odnos između njih**.
- Primeri strukturiranih podataka: sekvence, stabla, slike, tekstualni dokumenti.
- Primer zadatka: **mašinsko prevođenje**.

---

## Nenadgledano učenje
- Dati su samo ulazni podaci **x**, bez željene izlazne vrednosti.
- Cilj: pronaći neku pravilnost u podacima.
- Tipični zadaci:
  - **Grupisanje (clustering)** — podaci se svrstavaju u grupe koje maksimizuju kriterijum sličnosti / minimizuju kriterijum različitosti.
  - **Smanjenje dimenzionalnosti** — pronalaženje manjeg skupa promenljivih koje zadržavaju glavne obrasce i varijacije.

### Klasifikacija vs grupisanje
| | Klasifikacija | Grupisanje |
|---|---|---|
| Broj klasa | poznat unapred | nije poznat unapred |
| Oznake | postoje (označena pripadnost) | ne postoje |
| Uloga modela | klasifikovanje novih podataka | razumevanje/istraživanje postojećih |
| Tip učenja | nadgledano | nenadgledano |

---

## Samonadgledano učenje
- Smatra se tipom nenadgledanog (ili prelazom ka nadgledanom).
- Dati su samo ulazni podaci **x**; **željena izlazna vrednost se izvodi iz samih ulaznih podataka** (često iz njihove strukture).
- Primer: **jezički modeli** — cilj je predvideti sledeću/izostavljenu reč u sekvenci. Tačne izlazne vrednosti se „veštački" generišu iz velikih korpusa neobeleženih tekstova.
- Dosta zastupljeno u savremenom NLP-u, naročito u **distribucionoj semantici** (generisanje vektora značenja reči — *word embeddings*; kontekstno osetljivi vektori — *contextual embeddings*).

## Polunadgledano učenje
- Kombinacija nadgledanog i nenadgledanog: za manji deo podataka postoje oznake, za veći deo ne.
- Cilj: iskoristiti neobeležene podatke za bolje obučavanje. Veoma korisno u praksi jer je teško dobiti dovoljno obeleženih podataka.

## Učenje sa podrškom (reinforcement learning)
- Obučavanje softverskih agenata koji deluju u prostoru akcija.
- Učenje na osnovu akcija agenta i **signala podrške** (pozitivan/negativan, stiže tek na kraju skupa akcija).
- Algoritam koristi signal da utvrdi koja akcija/skup akcija je doveo do ishoda i koriguje ponašanje agenta.
- Pogodno kad je „nagrada" dugoročna, a ne kratkoročna.
- Primene: NLP (čet-botovi), robotika, igre (šah, Go — AlphaGo, video-igre). Za ovakve probleme klasično nadgledano učenje je nepogodno.

---

## Mašinsko učenje u ovom kursu
- Akcenat na tehnikama **nadgledanog učenja**, pre svega **algoritmima klasifikacije** (najširi spektar upotrebe).
- Većina današnjih NLP sistema koristi neki oblik nadgledanog učenja.
- Klasifikacija je jedan od najlakših problema za razumevanje → dobro polazište za složenije (strukturna predikcija).
- Razmatraju se i osnove **samonadgledanog učenja** — važna paradigma u osnovi mnogih state-of-the-art NLP sistema.
