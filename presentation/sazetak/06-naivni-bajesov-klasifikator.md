# 6. Naivni Bajesov klasifikator

**Tema:** Bajesova teorema u klasifikaciji, naivna pretpostavka o nezavisnosti odlika, MAP odlučivanje, multinomijalni i multivarijacioni Bernulijev model, Laplasovo poravnanje, generativni modeli.

> Napomena: formule su rekonstruisane iz standardne notacije.

---

## Bajesova teorema
Thomas Bayes — engleski statističar i filozof, autor teoreme o verovatnoći:
```
P(c | x) = P(x | c) · P(c) / P(x)
```
gde je **c** klasa, **x** podatak:
- **P(c)** — prethodna/apriorna verovatnoća klase (prior).
- **P(c|x)** — aposteriorna verovatnoća klase (posterior).
- **P(x, c)** — zajednička verovatnoća klase i podatka (joint).
- **P(x|c)** — funkcija izvesnosti (likelihood).

### MAP odlučivanje
- **Klasifikaciona odluka:** podatak svrstati u klasu sa **najvećom aposteriornom verovatnoćom** — *Maximum A Posteriori (MAP)*.
- Pošto je P(x) isto za sve klase, pri odluci se može zanemariti:
```
ĉ = argmaxₖ P(x | cₖ) · P(cₖ)
```

### Šta treba izračunati
- **P(c)** — zastupljenost klase u skupu za obučavanje.
- Podatak se predstavlja preko odlika x = (x₁, …, xₙ); koristeći pravilo ulančavanja uslovnih verovatnoća, P(x₁,…,xₙ|c) se rastavlja, ali je u opštem slučaju **nemoguće pouzdano proceniti** (previše kombinacija).

---

## Naivna pretpostavka o nezavisnosti odlika
- **Pretpostavka:** odlike su **statistički nezavisne** jedna od druge (poznavanje vrednosti jedne ne govori ništa o drugoj). Tada:
```
P(x₁,…,xₙ | c) = Π_{i} P(xᵢ | c)
```
- Uslovna verovatnoća svake odlike zavisi samo od klase. Raspodela P(xᵢ|c) može biti multinomijalna, Bernulijeva, Gausova…

> *„Essentially all models are wrong, but some are useful."* — George Box.
> Pretpostavka je praktično uvek pogrešna, ali znatno olakšava modelovanje i u praksi NB modeli često daju dobre rezultate — za tačnu klasifikaciju nije nužno znati tačne verovatnoće, već njihov **međusobni redosled**.

### Formula za pripadnost klasi
```
ĉ = argmaxₖ  P(cₖ) · Π_{i} P(xᵢ | cₖ)
```
- Broj odlika je često velik, a verovatnoće su u (0,1) → opasnost od **floating-point underflow**. Zato se umesto množenja sabiraju **logaritmi**:
```
ĉ = argmaxₖ  [ log P(cₖ) + Σ_{i} log P(xᵢ | cₖ) ]
```

---

## Raspodele uslovnih verovatnoća odlika
- **Multinomijalna** — odlike koje predstavljaju **broj javljanja** nečega.
- **Bernulijeva** — odlike sa **binarnim** (indikatorskim) vrednostima.
- **Gausova** — odlike sa **kontinualnim** numeričkim vrednostima.

---

## Multinomijalni naivni Bajesov klasifikator
- Pogodan kad vrednosti odlika predstavljaju broj javljanja.
- Verovatnoća P(xᵢ|c) = odnos zbirne vrednosti odlike u podacima klase i zbira svih odlika u podacima te klase. Ovo je **metod najveće izvesnosti (Maximum Likelihood Estimation, MLE)**.

### Problem nultih verovatnoća
- Ako se odlika **nikad ne javlja** u podacima neke klase → P(xᵢ|c) = 0 → ceo proizvod = 0 (model odbacuje klasu na osnovu jedne odlike). Problematično jer odsustvo može biti slučajno, naročito uz **proređenost podataka** (puno odlika, mali skup) — to je oblik overfitting-a.

### Laplasovo poravnanje (smoothing)
- **Laplasovo (aditivno) poravnanje:** brojanje ne počinje od 0 nego od neke predefinisane vrednosti (obično 1):
```
P(xᵢ | c) = (count(xᵢ, c) + 1) / (Σ count(x, c) + |V|)
```
- Deo verovatnoće javljanja viđenih odlika preraspodeljuje se na odlike koje u klasi još nisu opažene. Smatra se oblikom **regularizacije**.

### Poziciona nezavisnost odlika
- Multinomijalni NB **implicitno pretpostavlja** da nema zavisnosti između verovatnoće odlike i njene **pozicije** (npr. raspored reči u tekstu se ignoriše).
- U modelovanju teksta to je pristup **„vreće reči" (bag-of-words)** — pojedinačne reči su odlike. Drastično smanjuje broj parametara.
- Ponekad se odlike **binarizuju** (računaju se samo prisustvo/odsustvo, ne broj). U računanju P(x|c) učestvuju samo odlike koje se **javljaju** (nenulta vrednost) u podatku.

---

## Multivarijacioni Bernulijev naivni Bajesov klasifikator
- Odlike su **binarnog (indikatorskog)** tipa.
- P(xᵢ|c) = **procenat podataka klase** u kojima je odlika prisutna.
- U računanje učestvuju **sve** odlike modela, uključujući i one koje se ne javljaju (nulta vrednost).
- Poziciona nezavisnost **nije neophodna** — model po definiciji uzima u obzir samo prisustvo/odsustvo.
- Laplasovo poravnanje: dodaje se po jedan za svaki mogući ishod (kod binarne odlike to je 2 u imeniocu).

### Multinomijalni vs Bernulijev model (klasifikacija teksta)
| | Multinomijalni | Bernulijev |
|---|---|---|
| Vrednost odlike | broji javljanja (može se binarizovati) | binarno (prisustvo) |
| P(xᵢ\|c) | odnos zbirnih vrednosti | procenat dokumenata sa odlikom |
| U P(x\|c) učestvuju | samo prisutne odlike | sve odlike modela |
| Poziciona nezavisnost | potrebna | nepotrebna |
- **Binarizovan multinomijalni model NIJE isto što i Bernulijev.**

#### Primer (klasifikacija teksta C/J)
Klasičan primer (Manning IR): trening dokumenti o klasama C (Kina) i J (Japan), test „Chinese Chinese Chinese Tokyo Japan" — pokazuje računanje verovatnoća za oba modela.

---

## Generativni modeli
- Modeluju **zajedničku verovatnoću** P(x, c) → modeluju proces generisanja podataka.
- **Naivni Bajes je generativni model** — aposteriorna verovatnoća se dobija iz zajedničke preko Bajesove teoreme.
- Drugi generativni modeli: **skriveni Markovljevi lanci (HMM)**, **Bajesovske mreže**, **latentna Dirišleova alokacija (LDA)**.

---

## Prednosti i mane

**Prednosti:**
- Jednostavnost; **brzina** učenja i klasifikacije (dovoljan jedan prolaz kroz podatke).
- Nije osetljiv na irelevantne odlike; dobro radi kad ima više podjednako važnih odlika.
- Interpretabilnost (veća težina = važnija odlika).
- Direktno primenjiv na višeklasnu klasifikaciju; model se lako ažurira novim podacima.

**Mane:**
- Netačna pretpostavka o nezavisnosti odlika → kod korelisanih odlika **duplo brojanje** (iskrivljene procene važnosti).
- Vrednosti aposteriornih verovatnoća često **iskrivljene** u korist najverovatnije klase.

## Upotreba
- Često kao **baseline** (jednostavan, brz).
- Često bolji od složenijih modela kad je **malo trening podataka**; kompetitivan i kad ima puno podataka (zbog brzine).
- Raširen u klasifikaciji teksta; **multinomijalna varijanta sa binarizovanim odlikama** obično najbolja.
- Primene: detekcija spama, analiza sentimenta, klasifikacija po temama, analiza autorstva.
