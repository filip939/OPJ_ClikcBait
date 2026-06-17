# 1. Uvodno predavanje

**Tema:** Organizacija predmeta, uvod u NLP, istorija, klasifikacija teksta i analiza sentimenta, savremeni pristupi i istraživački projekti.

---

## Organizacija predmeta

- **Predavanja/vežbe:** Boško Nikolić (nbosko@etf.bg.ac.rs), Vuk Batanović (vuk.batanovic@etf.bg.ac.rs).
- Predmet je **kombinacija teorije i praktičnog rada** — puno eksperimenata i rada sa podacima.
- Rad na računarima, obrada praktičnih skupova podataka — **korpus srpskog jezika**.
- **Projekat:** grupe od 4–5 članova, konkretan zadatak definisan rano, izrada tokom celog semestra.

### Program predmeta
Mašinsko učenje u NLP-u; generativni i diskriminativni modeli; modeli sekvenci; morfološki, sintaksni i semantički problemi; jezički modeli; stemovanje i lematizacija, parsiranje; klasifikacija tekstova (tematika, sentiment); semantička sličnost; prepoznavanje imenovanih entiteta; pregled novih tehnologija.

---

## Šta je NLP

**NLP (Natural Language Processing)** proučava metode za računarsku obradu i interpretaciju tekstualnih podataka napisanih na prirodnim jezicima (jezici koje ljudi koriste u komunikaciji).
- Struktura i semantika jezika **nisu direktno mašinski čitljivi**.
- Velika kompleksnost, nejasnoća i višesmislenost u izražavanju.
  - Primer parafraze: „Uskoro sledi poskupljenje struje." ≈ „Cena električne energije će ubrzo porasti."

### Osnovni NLP pipeline
`Tekst → Tokenizacija → Obrada → Model → Rezultat`
- **Tekst** — sirovi ulaz (rečenice, dokumenti, upiti).
- **Tokenizacija** — razbijanje na manje jedinice (reči, fraze, tokeni).
- **Obrada** — čišćenje i priprema (uklanjanje stop reči, lematizacija, normalizacija).
- **Model** — primena (klasifikacija, prevođenje, analiza sentimenta).
- **Rezultat** — predikcija, oznaka, generisani tekst, uvid.

Primeri zadataka: tokenizacija (`Ne volim ovu knjigu` → `[Ne, volim, ovu, knjigu]`), NER (`Beograd → Lokacija`, `Srbija → Država`), analiza sentimenta (čak i uz negaciju: „Ne mogu da verujem koliko je ovo dobro" → pozitivno).

### Rast oblasti
Broj radova naglo raste: <500 (1985), ~2000 (2000), ~9800 (Scopus, 2016), procena 25.000–30.000 (2025). Ključne prekretnice: deep learning era (~2015), Transformer revolucija (2019), BERT/GPT (2020), eksplozija LLM-ova (2021+).

### Evolucija NLP metoda
- **Rule-based:** kontrola, ali teško održavanje.
- **Mašinsko učenje:** fleksibilnost, ali potreba za podacima.
- **Duboko učenje:** najbolji rezultati, ali kompleksnost.

---

## Razumevanje jezika i istorija

- Ideja o razumevanju jezika stara koliko i razmišljanje o računarima/robotima (npr. naučna fantastika — *Metropolis*, 1926).
- Računari traže preciznost i specifično znanje (API, XML, meniji) — prirodni jezici nisu takvi.
- **Mašinsko prevođenje** je počelo 1950-ih (Hladni rat, SAD/SSSR): velika očekivanja, mala procesna snaga, nerazumevanje funkcionisanja jezika.
  - Rani sistemi: traženje i zamena reči po rečniku → loši rezultati.
  - **ALPAC izveštaj (1966)** preporučio prekid rada na mašinskom prevođenju → naglasak na osnovnim naukama.
- 1990-te: oporavak u SAD, jači sistemi, ogromne količine podataka (milijarde reči), razvoj računarske lingvistike, manja očekivanja (npr. „dovoljan" prevod za web, ne savršen).
- Sintaksno i semantičko bazirano statističko prevođenje; korišćenje paralelnih tekstova (npr. UN dokumenti).

### Teškoće
- Obrada jezika je **inverzni problem** — od površinskih elemenata treba rekonstruisati osnovu (značenje).
- Jezici su veoma dvosmisleni; razumevanje zavisi od konteksta (rečenice, diskursa, realnog sveta).
- Zato se koriste **faktori verovatnoće i rezonovanje** za simulaciju ljudskog razumevanja.
- Prepoznavanje govora bliže elektrotehnici (obrada signala), takođe metode verovatnoće (AT&T, Bell, IBM).

---

## Obrada teksta i mašinsko učenje

- Pre obrade potrebna je **normalizacija** teksta: ekvivalentne klase, velika/mala slova, stemovanje, lematizacija (da se sva pojavljivanja iste reči svedu na isti oblik).
- Svi ML algoritmi imaju dve faze:
  1. **Učenje** — na osnovu poznatih odgovora algoritam uči da klasifikuje.
  2. **Predviđanje** — za nov, nepoznat tekst predviđa klasu.
- **Nadgledano učenje** — postoje anotirani trening podaci.
- **Nenadgledano učenje** — nema tačnih odgovora; traži se struktura u podacima.

### Klasifikacija teksta
Jedan od osnovnih problema. Primene: spam filteri, prepoznavanje autora/pola/godišta, prepoznavanje teme, analiza sentimenta, pretraživači.

---

## Analiza sentimenta

- Specijalan slučaj klasifikacije teksta (npr. pozitivna/negativna konotacija, ili više nivoa 1–5 zvezdica).
- Primene: kvalitet proizvoda (Google Product Search, Bing Shopping), raspoloženje sa Twittera/Facebooka, rezultati izbora, položaj proizvoda na tržištu.
- Srodni pojmovi: ekstrakcija mišljenja (opinion mining), analiza subjektivnosti.
- Prvi rad 1979; nagla ekspanzija od 2001 (napredak ML metoda, dostupnost podataka, komercijalni i istraživački potencijal).

### Teškoće analize sentimenta
- Sentiment se ne može uvek utvrditi po ključnoj reči; reči mogu biti neutralne van konteksta.
- **Zavisnost od konteksta i domena:** „Pročitajte knjigu" je pozitivno u recenziji knjige, negativno u recenziji filma.
- **Obrada negacije:** model „vreće reči" (bag-of-words) posmatra reči nezavisno → „Volim ovu knjigu" i „Ne volim ovu knjigu" izgledaju bliske. Negacija ne postoji u klasičnom pribavljanju informacija. „Ne mogu da verujem kako je ovo dobro" — pozitivno uprkos negaciji.
- **Ironija i sarkazam:** teško mašinski detektovati; reči mogu signalizirati suprotnu polarnost. Primer: „Film izbegava sve klišee..." — „izbegava" je neočekivani reverzer sentimenta.

---

## Konceptualni pristupi (rezime)

- **Rule-based NLP:** ručno sastavljena pravila — tačno ali krhko; ogroman ekspertski napor, jezik se menja → stalno ažuriranje.
- **Statistical NLP:** ML na parovima (ulaz, tačan izlaz), bez eksplicitnog objašnjavanja veza; isti algoritmi za različite probleme; podstaknut razvojem hardvera i Web 2.0.
- **Deep learning:** najbolji rezultati, ali zahteva ogromne količine podataka (teško za manje jezike); pomak ka **višejezičnim modelima**.

### Kako funkcioniše ChatGPT / Transformeri
- Transformer arhitektura predviđa sledeću reč koristeći kontekst.
- **Attention mehanizam**, paralelna obrada, bolje razumevanje konteksta.
- Transformeri = generativni modeli dubokog učenja sa višestrukim slojevima pažnje; umesto RNN-ova obrađuju sve ulazne reči istovremeno → uče složene odnose. Primene: prevođenje, generisanje, klasifikacija, QA, obrada slike. **BERT** (Bidirectional Encoder Representations from Transformers).

### Semantički problemi u NLP-u
Analiza sentimenta/emocija, semantička sličnost, detekcija parafraza, QA, dohvatanje informacija, sažeci, uprošćavanje, mašinsko prevođenje, zaključivanje na prirodnom jeziku.

---

## NLP u realnim sistemima — izazovi
- **Performanse i latencija** (LLM-ovi su veliki/spori → batching, caching, distillation).
- **Skalabilnost** (cloud, distribuirani sistemi).
- **Kvalitet podataka** (šum, ćirilica/latinica, sleng; nedostatak anotiranih podataka za manje jezike).
- **Bias i etika** (pristrasnosti iz podataka).
- **Robusnost** (typo, ironija, edge-case).
- **Integracija** (API dizajn, mikroservisi, monitoring, verzionisanje modela).
- Zaključak: *NLP nije samo model, već kompletan softverski sistem.*

---

## Istraživački projekti (ICEF / ETF)
- **COMtext.SR** — resursi i alati za automatsku obradu srpskog (ekavica i ijekavica), javna licenca; fokus na do sada nepokrivenim domenima (pravno-administrativni, finansijski, medicinski). Od 2023: morfosintaktičko opisivanje i lematizacija; 2024: NER u pravno-administrativnim tekstovima. [github.com/ICEF-NLP/COMtext.SR](https://github.com/ICEF-NLP/COMtext.SR)
- **STOP** — detekcija govora mržnje na srpskom (PROMIS, Fond za nauku); anotirani skupovi, ML/AI za kratke tekstove.
- **AVANTES** — sličnost tekstova; cross-level semantička sličnost (srpski/engleski), semantička pretraga koda.
- **Automatizacija RIA procedure (UNDP)** — pronalaženje delova pravnih dokumenata vezanih za UN ciljeve održivog razvoja; semantička pretraga (nestandardan format, ćirilica/latinica, morfologija).
