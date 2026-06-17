# 7. Metoda potpornih vektora (SVM)

**Tema:** SVM kao linearni diskriminativni klasifikator sa maksimalnom marginom, potporni vektori, optimizacioni problem i dualna formulacija, meka margina i hinge loss, regularizacija (hiperparametar C), kernel trik, višeklasna klasifikacija.

> Napomena: formule su rekonstruisane iz standardne notacije.

---

## Osnovno
- **Metoda potpornih vektora (Support Vector Machines, SVM)** — **binarni** klasifikator (klase −1 i +1).
- Osnovna verzija = **linearni** klasifikator.
- **Neprobabilistički** — izlaz je samo klasifikaciona odluka (ne verovatnoća).
- Direktno modeluje granicu između klasa → **diskriminativni model**.

### Istorijat
- Osnovnu varijantu predstavili **Vladimir Vapnik i Aleksej Červonenkis (1963)**.
- **1992** — grupa autora (uključujući Vapnika) predlaže proširenje na nelinearne slučajeve preko **kernel trika**.
- **Cortes i Vapnik (1993/1995)** — varijanta sa **mekom marginom** (soft margin).

---

## Izbor hiperravni razdvajanja
- Ako su podaci **linearno separabilni**, postoji **beskonačno mnogo** hiperravni koje ih razdvajaju → po kom kriterijumu odabrati?
  - Logistička regresija: kriterijum = maksimalna entropija modela.
  - **SVM: kriterijum = maksimalna margina između klasa.**

## Maksimalna margina i potporni vektori
- Zamislimo dve paralelne hiperravni koje razdvajaju klase tako da između njih nema nijednog podatka. Oblast između njih = **margina**.
- Cilj obučavanja: pronaći **maksimalnu marginu**.
- Podaci na koje te zamišljene hiperravni naležu su **potporni vektori (support vectors)** — oni „podupiru" hiperravni. (Naziv „vektor": svaki podatak se posmatra kao tačka/vektor u n-dimenzionalnom prostoru.)
- **Intuicija:** hiperravan kroz sredinu praznine ima više smisla od one blizu podataka; biranjem hiperravni najdalje od podataka **minimizuje se greška generalizacije** (uz pretpostavku da su novi podaci iz iste raspodele).
- Razlika u odnosu na logističku regresiju:
  - Logistička: minimizuje **empirijsku grešku** na svim raspoloživim podacima (zavisi od položaja svih podataka).
  - SVM: hiperravan je određena **malim brojem najbližih podataka** (potpornih vektora); položaj udaljenijih podataka **nije bitan**.

---

## Hipoteza i jednačina hiperravni
- Hipoteza: **h(x) = wᵀx + b**, gde je **b** slobodni član (bias term), **w** vektor normale na hiperravan.
- Jednačina hiperravni razdvajanja: **wᵀx + b = 0**.

### Skaliranje jednačine
- Jednačina se može pomnožiti/podeliti pozitivnim brojem bez promene položaja hiperravni → usvaja se **kanonska** vrednost tako da za potporne vektore važi |wᵀx + b| = 1:
  - potporni vektori klase +1: wᵀx + b = +1
  - potporni vektori klase −1: wᵀx + b = −1

### Širina margine
- Udaljenost tačke od hiperravni = |wᵀx + b| / ‖w‖.
- Udaljenost potpornih vektora = 1/‖w‖; pošto su sa obe strane, **širina margine = 2/‖w‖** → treba je **maksimizovati**.

---

## Cilj obučavanja (tvrda margina)
- Maksimizovati 2/‖w‖ ⇔ minimizovati ‖w‖ ⇔ (radi lakše optimizacije) minimizovati **½‖w‖²** (minimizacija kvadrata norme minimizuje i samu normu).
- Uslov da nijedan podatak ne upadne u marginu: **yᵢ·(wᵀxᵢ + b) ≥ 1** za sve i.
- Optimizacioni problem:
```
min  ½‖w‖²
s.o. yᵢ·(wᵀxᵢ + b) ≥ 1,  i = 1,…,m
```
- Ovo je **konveksna optimizacija sa ograničenjima** = **kvadratno programiranje**.
- Rešava se **Lagranžovim multiplikatorima** uz **Karush-Kuhn-Tucker (KKT)** uslove → kreira se **dualna reprezentacija** (po jedan Lagranžov multiplikator αᵢ za svaku nejednakost).

### Dualna formulacija
- W se izražava kao kombinacija podataka: w = Σ αᵢ yᵢ xᵢ.
- Optimalne vrednosti αᵢ su **nula za sve tačke osim potpornih vektora** (kojih je obično mnogo manje od ukupnog broja). Hipoteza i hiperravan zavise **samo od potpornih vektora**.
- Vrednost hipoteze za nov podatak zavisi od proizvoda **xᵢᵀx** — tj. od **sličnosti** potpornih vektora sa novim podatkom. Klasifikacija = provera sa koje strane hiperravni je podatak.

---

## Meka margina (soft margin)
- Insistiranje na linearnoj separabilnosti (čak i kad je moguća) može voditi overfitting-u; problem kod **outliera** (mala margina → slaba generalizacija).
- Bolje: u ograničenoj meri **dozvoliti** ulazak podataka u marginu ili prelazak na pogrešnu stranu → **meka margina**.
- Uvode se **slack promenljive ξᵢ** (prekoračenja):
```
min  ½‖w‖² + C · Σ ξᵢ
s.o. yᵢ·(wᵀxᵢ + b) ≥ 1 − ξᵢ,  ξᵢ ≥ 0
```
- Interpretacija ξᵢ:
  - **ξᵢ = 0** → podatak pravilno klasifikovan i izvan margine;
  - **0 < ξᵢ ≤ 1** → pravilno klasifikovan, ali unutar margine;
  - **ξᵢ > 1** → pogrešno klasifikovan (sa suprotne strane hiperravni).

### Hinge loss (gubitak u obliku šarke)
- Funkcija gubitka SVM-a sa mekom marginom = **hinge loss**:
```
loss(x, y) = max(0, 1 − y·(wᵀx + b))
```
- Postoji i **kvadratni hinge** (L2 oblik): max(0, 1 − y·h(x))².
- Logistički gubitak se može reformulisati za oznake y∈{−1,+1} i (uz skaliranje) prolazi kroz tačku (0, log2); poređenje oblika gubitaka (hinge plava, logistički crveni, kvadratni zeleni — Bishop) pokazuje sličnosti.

### Funkcija greške sa mekom marginom
- Dva (ponekad suprotstavljena) cilja: **maksimizacija margine** i **minimizacija greške klasifikacije** (hinge loss).
```
J(w) = ½‖w‖² + C · Σ max(0, 1 − yᵢ·(wᵀxᵢ + b))
```
- **C** — hiperparametar koji određuje balans dva cilja. Cilj obučavanja = minimizacija J(w).
- **L1 oblik hinge gubitka:** rešenje stabilnije (male promene podataka manje utiču), ali manja otpornost na outliere.
- **L2 oblik (kvadratni hinge):** rešenje manje stabilno, ali veća otpornost na outliere.

---

## Regularizacija i hiperparametar C
- Veća margina = bolja generalizacija; minimizacija ‖w‖ je **regularizacija**.
- Može se koristiti L1 ili L2 regularizacija (sve ranije razlike L1/L2 važe i ovde).
- **Hiperparametar C:**
  - **Veliko C** → fokus na smanjivanje greške klasifikacije po cenu manje margine → **manja regularizacija**.
  - **Malo C** → fokus na povećanje margine → **veća regularizacija**, po cenu veće greške.
  - C je **inverzan** hiperparametru λ koji određuje jačinu regularizacije u linearnoj/logističkoj regresiji.

---

## Optimizacija: primalni vs dualni domen
- Funkcija greške se može minimizovati i u **primalnom domenu** (bez Lagranžovih multiplikatora) — naprednije tehnike numeričke optimizacije (npr. subgradijentni spust); često se traži **aproksimacija** rešenja.
- Dualni pristup može biti spor kad je skup za obučavanje jako velik (mnogo potpornih vektora).
- Kad je **broj odlika znatno veći od broja podataka**, preporučljiv je dualni domen.

> **Kernel trik** (pomenut u istorijatu): zamenom skalarnog proizvoda kernel funkcijom SVM rešava i **nelinearne** probleme, implicitno preslikavajući podatke u prostor više dimenzije.

---

## Višeklasna klasifikacija
- Kombinovanje više nezavisnih binarnih klasifikacija:
  - **one-vs-all (one-vs-rest)** — podatak ide u klasu čiji klasifikator ga svrstava sa **najvećom udaljenošću** od hiperravni (umesto najveće verovatnoće kao kod logističke regresije);
  - **one-vs-one**.
- Postoje i pristupi koji istovremeno modeluju više klasa — npr. **Crammer & Singer** algoritam.

---

## Prednosti i mane

**Prednosti:**
- Veoma dobre performanse na širokom spektru problema.
- Metoda **sama odabira** koji podaci su potporni vektori i koliko ih ima.
- Manja sklonost overfitting-u od mnogih drugih metoda.

**Mane:**
- Može biti primetno **sporiji** od drugih metoda (zavisno od broja odlika i količine podataka).
- Izlaz **nije probabilistički** (moguća procena preko udaljenosti od hiperravni).
- Varijanta sa **tvrdom marginom** je osetljiva na outliere.
