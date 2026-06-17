# 5. Logistička regresija

**Tema:** Logistička regresija kao probabilistički diskriminativni klasifikator, sigmoidna funkcija, hiperravan razdvajanja, gubitak unakrsne entropije, regularizacija, višeklasna klasifikacija (one-vs-all, one-vs-one, multinomijalna/softmax), diskriminativni vs generativni modeli.

> Napomena: formule su rekonstruisane iz standardne notacije.

---

## Zašto ne (samo) linearna regresija za klasifikaciju?
- Za binarnu klasifikaciju (izlaz 0 ili 1) mogla bi se koristiti linearna regresija sa pragom: predviđa se klasa 1 ako h(x) ≥ 0.5, inače klasa 0.
- **Problemi:** outlieri dramatično remete kvalitet; h(x) može biti znatno veće od 1 ili manje od 0.

---

## Logistička regresija — osnovno
- Jedan od **najpopularnijih algoritama klasifikacije**; osnovna verzija = **binarna klasifikacija** (klase 0 i 1).
- Predstavio statističar **David Cox (1958)**. Široko rasprostranjena u ekonomskim, sociološkim, medicinskim analizama; sastavni element mnogih neuronskih mreža.
- **Probabilistički klasifikator** — izlaz je verovatnoća P(y=1|x), ne samo odluka.
- Pošto direktno modeluje P(y|x), spada u **diskriminativne modele**.
- Za razliku od naivnog Bajesa, **ne pretpostavlja statističku nezavisnost odlika**.

### Sigmoidna (logistička) funkcija
```
g(z) = 1 / (1 + e^(−z))
```
- Sabija interval (−∞, +∞) na opseg (0, 1) → izlaz se interpretira kao verovatnoća.
- Hipoteza: **h(x) = g(wᵀx) = 1 / (1 + e^(−wᵀx))** (uz fiktivnu odliku x₀ = 1; wᵀx je skalarni proizvod vektora težina i odlika).
- P(y=1|x) = h(x); P(y=0|x) = 1 − h(x).
- Nov podatak se klasifikuje u verovatniju klasu: klasa 1 za h(x) ≥ 0.5, klasa 0 za h(x) < 0.5.

### Hiperravan razdvajanja
- Granica razdvajanja je na h(x) = 0.5, tj. **wᵀx = 0** — to definiše **hiperravan razdvajanja** (separating hyperplane).
- Za jednu ulaznu promenljivu hiperravan je prava; u prostoru dimenzije n hiperravan je potprostor dimenzije n−1.
- Tačke s jedne strane → jedna klasa, s druge → druga. Što je tačka dalja od hiperravni, to je veća verovatnoća pripadnosti klasi te strane. Tačke na hiperravni se konvencijom dodeljuju jednoj klasi.

---

## Funkcija greške i gubitak
- Potrebna je **konveksna** funkcija greške → funkcija gubitka mora biti konveksna.
- **Kvadrat odstupanja (MSE) NIJE pogodan** za logističku regresiju — zbog sigmoidne funkcije takav gubitak je **nekonveksan**.
- Tražene osobine gubitka:
  - kad je y=1: greška velika kad je h(x) blizu 0, mala kad je blizu 1;
  - kad je y=0: greška velika kad je h(x) blizu 1, mala kad je blizu 0.
- Funkcija koja to ispunjava (**log gubitak**):
```
loss(h(x), y) = −[ y·log h(x) + (1−y)·log(1 − h(x)) ]
```
- Ovo je **logistički/log gubitak**, tj. **gubitak unakrsne entropije** (cross-entropy loss). Unakrsna entropija meri razliku između dve raspodele (stvarne i predviđene).

### Funkcija greške i gradijentni spust
```
J(w) = (1/m) · Σ loss(h(x⁽ⁱ⁾), y⁽ⁱ⁾)
```
- Cilj obučavanja: minimum J(w) gradijentnim spustom.
- Zanimljivo: **parcijalni izvod ima isti oblik kao u linearnoj regresiji**:
```
wⱼ := wⱼ − α · (1/m) Σ (h(x⁽ⁱ⁾) − y⁽ⁱ⁾) · xⱼ⁽ⁱ⁾
```
- Postoje grupna i stohastička varijanta (identično kao kod linearne regresije, uz simultano ažuriranje).
- Za ubrzanje se često koriste **naprednije metode optimizacije**: konjugovani spust, kvazi-Njutnove metode (**BFGS**, **L-BFGS**). Prednost: same biraju brzinu učenja. Mana: kompleksnost → koriste se gotove biblioteke.

---

## Preterana prilagođenost i regularizacija
- Kao i u regresiji, overfitting → neke težine postaju jako velike.
- **Primer:** klasifikacija dokumenata sport/informatika, bag-of-words. Reč „fudbal" se u trening skupu javlja samo u sport-dokumentima → algoritam dodeli veliku težinu → svaki dokument sa „fudbal" automatski ide u sport (ostale odlike se ignorišu). Nepoželjno (npr. informatički tekst o fudbalskom simulatoru). Uzrok — **proređenost podataka**.
- Rešenje: **regularizacija** (L1 ili L2) ograničava magnitude težina; težinski parametar w₀ obično ne podleže regularizaciji.

---

## Višeklasna klasifikacija
Logistička regresija na više klasa — dva pristupa:

### Kombinovanje binarnih klasifikatora
- **One-vs-all (one-vs-rest):** za K klasa konstruiše se **K** binarnih klasifikatora (svaki: „svoja klasa" vs „sve ostale zajedno"). Nov podatak ide u klasu čiji klasifikator daje najveću verovatnoću. Problem: **neuravnoteženost** (primera „ostalih" mnogo više).
- **One-vs-one:** za K klasa konstruiše se **K(K−1)/2** klasifikatora (po jedan za svaki par); glasanje. Više klasifikatora, ali svaki ima manji trening skup → vreme rada može biti kraće.
- Ovi pristupi primenjivi su i na druge binarne klasifikatore (npr. SVM).

### Multinomijalna (softmax) logistička regresija
- „Prirodno" proširenje na više klasa; verovatnoća pripadnosti se dobija **softmax** funkcijom:
```
P(y=k | x) = e^(wₖᵀx) / Σ_{j=1}^{K} e^(wⱼᵀx)
```
- Imenilac normalizuje raspodelu da suma svih verovatnoća bude 1.
- Hipoteza = K-dimenzionalni vektor verovatnoća pripadnosti svakoj klasi.
- Model je **preterano parametrizovan** (over-parameterized) — postoji slobodan izbor jednog vektora težina (zbir verovatnoća = 1). Iz toga se izvodi dokaz da je **binarna logistička regresija specijalan slučaj multinomijalne**.
- Funkcija gubitka — analogno binarnoj (kategorička unakrsna entropija). Funkcija greške koristi **indikatorsku (Kronekerovu delta) funkciju**. Regularizacija primenjiva.
- Multinomijalna logistička regresija je **log-linearni model** (logaritam hipoteze sadrži linearnu kombinaciju parametara) i poznata je i kao **model maksimalne entropije** (Maximum Entropy / MaxEnt):
  - Entropija raspodele: H = −Σ p·log p.
  - Intuicija: model treba da poštuje sva data ograničenja, a inače sledi **princip Okamove oštrice** — što manje dodatnih pretpostavki. Model s maksimalnom entropijom (bez ograničenja) svim klasama daje jednaku verovatnoću; pokazuje se da je MaxEnt model upravo multinomijalna logistička regresija čiji težinski faktori maksimizuju uslovne verovatnoće nad trening podacima.

### Multinomijalni pristup vs kombinacija binarnih
- Binarni klasifikatori ne modeluju celu složenost kad je K > 2 (ignorišu interakcije među klasama pri optimizaciji); osetljiviji na outliere.
- Multinomijalni pristup daje **globalni probabilistički izlaz** — pogodno kad podatak može pripadati **samo jednoj** klasi.
- Ako podatak može pripadati **više klasa u različitoj meri** → primerenija kombinacija binarnih klasifikatora.

---

## Diskriminativni vs generativni modeli
- **Diskriminativni modeli** direktno modeluju P(y|x); fokus na razlikovanju klasa (modelovanje granice), ne na P(x|y) niti procesu generisanja parova (x, y). Model ne uči ono što nije potrebno za zadatak.
  - Primeri: **logistička regresija, SVM (Support Vector Machines), uslovna nasumična polja (Conditional Random Fields)**.
- **Generativni modeli** modeluju zajedničku verovatnoću (proces generisanja podataka).

### Poređenje
| | Diskriminativni | Generativni |
|---|---|---|
| Granica razdvajanja | eksplicitno | implicitno |
| Srednje/veliki podaci | obično bolje | — |
| Mali podaci | — | obično bolje |
| Neobeleženi podaci | teže koriste | lakše koriste |

**Primer (određivanje jezika govornika):**
- Generativni: naučiti svaki jezik, pa odabrati najsličniji.
- Diskriminativni: naučiti samo **razlike** između jezika (bez učenja samih jezika) → mnogo lakši pristup.

---

## Prednosti i mane logističke regresije
**Prednosti:** ne pretpostavlja nezavisnost odlika; dobre performanse uz dovoljno podataka; probabilistički izlaz; lako primenjiva na višeklasnu klasifikaciju.
**Mane:** lako overfituje kad je malo podataka (neophodna regularizacija); efekti interakcija odlika moraju se **eksplicitno modelovati**.
