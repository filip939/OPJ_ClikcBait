# 4. Linearna regresija

**Tema:** Linearna regresija kao osnovni regresioni model, funkcija greške (MSE), obučavanje gradijentnim spustom (grupni/stohastički/mini-batch), skaliranje odlika, regularizacija (ridge/L2 i LASSO/L1).

> Napomena: formule u nastavku rekonstruisane su iz standardne notacije jer ih PDF nije izvezao čitljivo.

---

## Osnovni pojmovi
- **Regresija** = predviđanje kontinualnih numeričkih vrednosti. Prvi oblik linearne regresije predstavljen početkom 19. veka (metoda najmanjih kvadrata).
- Vrste:
  - **Prosta (jednostruka)** — jedna ulazna promenljiva (odlika).
  - **Višestruka** — više ulaznih promenljivih (x₁, x₂, …, xₙ).
  - **Univarijantna** — jedna izlazna promenljiva.
  - **Multivarijantna** — više izlaznih promenljivih.
- Pretpostavka: zavisnost izlaza ima oblik **linearne kombinacije odlika i njihovih težina**.
- Dve glavne upotrebe: (1) **predviđanje** izlaza za nove podatke; (2) **analiza stepena povezanosti** između izlaza i promenljivih.
- Široko korišćena u prirodnim i društvenim naukama.

---

## Jednostruka univarijantna linearna regresija
- Hipoteza: **h(x) = w₀ + w₁·x** (w₀, w₁ su težine = parametri modela; ponekad notacija θ₀, θ₁).
- **Obučavanje** = odabir optimalnih vrednosti parametara tako da h(x) bude blisko stvarnom y za sve parove (x, y).
- Potrebna je **funkcija cene/greške** koja meri koliko hipoteza odskače od stvarnih vrednosti.

### Funkcija gubitka i funkcija greške
- **Funkcija gubitka (loss)** — mera odstupanja hipoteze na **pojedinačnom** podatku.
- **Funkcija greške (cost/error)** — **prosek** funkcije gubitka po svim podacima u skupu.
- Obučavanje ⇒ odabir parametara koji minimizuju funkciju greške na skupu za obučavanje.

### Funkcija greške u linearnoj regresiji — MSE
Najčešće **srednja kvadratna greška** (Mean Squared Error):

```
J(w) = (1/2m) · Σ_{i=1}^{m} ( h(x⁽ⁱ⁾) − y⁽ⁱ⁾ )²
```
gde je **m** broj podataka u skupu.
- Minimum je moguće naći **analitički** (normalne jednačine, računanje inverznih matrica), ali to može biti preskupo kada je broj odlika veliki.

---

## Obučavanje — gradijentni spust
- U praksi se najčešće koristi **gradijentni spust** — iterativni metod traženja minimuma funkcije.
- **Gradijent** = vektor parcijalnih izvoda funkcije; pokazuje smer najbržeg rasta → parametri se menjaju u **smeru opadanja** (suprotno gradijentu).

### Pravilo ažuriranja
```
wⱼ := wⱼ − α · ∂J/∂wⱼ
```
- **α (learning rate, brzina učenja)** — pozitivan broj koji određuje veličinu koraka.
- Brzina učenja mora se **pažljivo odabrati**:
  - **Premala α** → učenje veoma sporo (mnogo koraka); moguće zaglavljivanje u lokalnim minimumima (zavisno od oblika funkcije).
  - **Prevelika α** → optimizacija može preskočiti minimum ili **divergirati**.
- **Sve težine treba ažurirati istovremeno (simultano)**; u suprotnom promena jednog parametra utiče na parcijalne izvode drugih → više se ne kreće u smeru gradijenta.

### Konvergencija
- Gradijentni spust može konvergirati i sa **fiksnom α**: kako se približava minimumu, vrednosti parcijalnih izvoda se smanjuju → koraci postaju manji.
- U minimumu je izvod jednak nuli → parametri se više ne menjaju.
- Obučavanje se ponekad obustavlja kad promena parametara u koraku padne ispod predefinisanog praga.
- Funkcija greške MSE je **kvadratna → konveksna** → ima jedan (globalni) minimum; uz dobro odabranu α spust uvek konvergira ka globalnom minimumu.
- Provera konvergencije: greška treba da se smanjuje u svakom koraku.

### Grupni vs stohastički vs mini-batch
- **Grupni gradijentni spust (batch)** — u svakom koraku koristi **sve** podatke iz skupa za obučavanje. Mora proći ceo skup za jedan korak → skupo za velike skupove.
- **Stohastički gradijentni spust (SGD)** — podaci se obrađuju **jedan po jedan**, parametri se ažuriraju nakon svakog podatka.
  - Često se brže približi minimumu od grupnog.
  - Veća varijansa (svaki gradijent je drugačiji) → može usporiti konvergenciju; zahteva da α vremenom opada.
  - Može nikad ne konvergirati sasvim, već oscilovati oko minimuma (obično dovoljno dobro).
  - Pogodan za **online obučavanje** (podaci pristižu sekvencijalno).
- **Mini-batch** — kompromis: obučavanje na manjim podskupovima podataka.

---

## Višestruka linearna regresija
- Hipoteza: **h(x) = w₀ + w₁x₁ + w₂x₂ + … + wₙxₙ** = wᵀx (uz fiktivnu odliku x₀ = 1).
- Funkcija greške i pravila ažuriranja su analogni jednostrukom slučaju, sa sumiranjem po svim odlikama. Postoje grupna i stohastička varijanta.

---

## Skaliranje vrednosti odlika
- Brzina učenja je **ista za sve težinske parametre**, pa mora biti birana prema odlici sa najvećom magnitudom (da se spreči divergencija). Posledica: mnogo koraka i „cik-cak" kretanje jer neki parametri konvergiraju brže od drugih.
- Gradijentni spust **brže konvergira** kada su sve odlike u sličnim opsezima (put do minimuma direktniji, manje cik-cak).
- Skaliranje: tipično svesti vrednosti u opseg npr. [−1, 1] ili tako da srednja vrednost bude 0. Nije nužno potpuno identičan opseg — manja odstupanja ne smetaju.

---

## Regularizacija
- **Regularizacija** = sprečavanje **preterane prilagođenosti (overfitting)** kažnjavanjem prevelikih magnituda parametara.
- Velike magnitude nastaju kad model prilagođava oblik funkcije **šumu i izuzecima** u podacima radi smanjenja greške.
- Šire: regularizacija = svaki postupak koji smanjuje **grešku generalizacije** (na novim podacima) bez povećanja greške na skupu za obučavanje.

**Primer (NLP):** predikcija kontinualne ocene sentimenta; model uzima reči i sekvence reči kao odlike. Preterano prilagođen model može „naučiti" da pozitivnost izvire iz neke retke sekvence reči koja se javlja samo u jednom trening primeru → toj odlici dodeli veliku težinu (memoriše umesto da generalizuje).

- Regularizacija čini funkciju izlaza „regularnijom" (pravilnijom) ubacivanjem **regularizacionog izraza** u funkciju greške:
```
J(w) = MSE(w) + λ · R(w)
```
- **λ** — hiperparametar koji određuje **jačinu** regularizacije; takođe smanjuje nelinearnost modela.
- λ se određuje eksperimentalno, **unakrsnom validacijom** (uz ugnežđenu unakrsnu validaciju ako se isti postupak koristi i za evaluaciju).
  - **Premalo λ** → nedovoljan efekat.
  - **Preveliko λ** → **underfitting**; gradijentni spust možda neće konvergirati.
- Pošto vrednosti zavise od skale odlika, **skaliranje** se obično radi pre regularizacije.
- Slobodni član (w₀/bias) se obično **izuzima** iz regularizacije.

### Tipovi regularizacije
- **L2 (Tihonovljeva) regularizacija:** R(w) = Σ wⱼ²  → **grebena (ridge) regresija**.
- **L1 regularizacija:** R(w) = Σ |wⱼ| → **LASSO** regresija.

### Grebena (ridge) regresija — L2
- Funkcija greške: MSE + λ·Σwⱼ²; parcijalni izvodi i pravilo ažuriranja se prilagođavaju (osim za w₀, koji ostaje kao u neregularizovanoj regresiji).
- Kod visoke korelacije odlika, funkcija cene neregularizovane regresije nema jedinstven minimum već **„greben" minimalnih vrednosti** → model nestabilan (male promene ulaza → velike promene parametara), otežana interpretacija. L2 zamenjuje greben jedinstvenim minimumom.

### LASSO regresija — L1
- LASSO = *Least Absolute Shrinkage and Selection Operator*.
- L1 regularizator **nije diferencijabilan** (zbog apsolutne vrednosti) → za ažuriranje se koriste naprednije metode: **subgradijentne metode, koordinatni spust, proksimalne metode**.
- Uz dovoljno veliko λ, L1 forsira neke težine **tačno na nulu** → **proređeni (sparse) modeli** (odlike s težinom 0 se efektivno ignorišu). Korisno za **istovremenu regularizaciju i selekciju odlika**, pogotovo kad ima ogroman broj odlika.

### L1 vs L2 — poređenje
| Svojstvo | L1 (LASSO) | L2 (ridge) |
|---|---|---|
| Selekcija odlika | da (parametri → 0) | ne (u principu) |
| Interpretabilnost | povećava | — |
| Stabilnost | manje stabilna | otpornija na male promene podataka |
| Brzina izračunavanja | može biti brža | — |
| Kada koristiti | mali broj odlika sa velikim uticajem | velik broj odlika sa uravnoteženim uticajem |

Izbor između L1 i L2 pravi se **unakrsnom validacijom** na konkretnom skupu.

---

## Prednosti i mane linearne regresije
**Prednosti:** jednostavnost; interpretabilnost (veća težina = veća važnost, ako su odlike skalirane — uz oprez kod međuzavisnih odlika); često dobra predikcija budućih podataka.
**Mane:** realne regresione funkcije su skoro uvek **nelinearne**; **osetljivost na outliere**.
