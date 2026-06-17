# Radni izveštaj projekta — Detekcija klikbejta (OPJ 2025/2026)

> Interni dnevnik rada: šta smo radili, kako, **i zašto** — da imamo uvid pri pisanju
> finalnog rada (Faza dokumentacije) i da na odbrani umemo da odgovorimo na pitanja.
> Pregled zahteva: `docs/Projekat-zahtevi.md`. Prepiska sa profesorom: `docs/Prof conversation.rtf`.

**Grupa:** Filip Nikolić (25/3234), Danilo Nikolić (25/3235) — par (dogovoreno sa profesorom).
**Zadatak:** Detekcija klikbejt naslova (binarna klasifikacija) — srpski jezik.
**Domen:** sportski naslovi sa domaćih portala. **Izvor:** isključivo **SportKlub**.

---

## 0. Šta je profesor tražio (sažetak prepiske)

Ključne sugestije koje smo usvojili:
1. **Precizirati definiciju klikbejta** — ne svesti na površne signale (uzvičnik, „Nećete verovati"); obuhvatiti i suptilne manipulacije.
2. **Jedan tematski domen** → izabrali sportske vesti.
3. **Duplirati podatke** → ~1000–1200 po klasi (mi: 1100/1100).
4. **SVM → Naivni Bajes** kao baseline (uz logističku regresiju).
5. **Umesto izbacivanja stop-reči → razmotriti TF/IDF/TF-IDF ponderisanje.**
6. **Samo jedan dekoderski model** je dovoljan.

---

## 1. Faza 1 — Prikupljanje podataka ✅

- **Izvor:** SportKlub (jedan izvor, latinica). Drugi izvori (npr. Mozzart) razmatrani pa **odbačeni** — radimo čisto sa jednim izvorom radi konzistentnosti.
- **Obim:** prikupljeno **2994 jedinstvenih naslova** (posle uklanjanja duplikata).
- **Metapodaci:** za svaki naslov sačuvan URL/identifikator i rubrika (`data/metadata.csv`).
- **Format:** UTF-8, latinica; rad. kopija u `data/interim/headlines.csv`.

**Zašto jedan izvor:** kontrolisan stil i konzistentna definicija klikbejta; izbegavamo da model uči razliku između portala umesto razlike klikbejt/regularno.

---

## 2. Faza 2 — Anotacija ✅

### Metodologija (5 koraka po postavci)
1. **Oznake:** binarno — `1` = klikbejt, `0` = regularan.
2. **Uputstva za anotaciju:** definicija + problematični slučajevi. Klikbejt obuhvata: uskraćivanje ključne informacije (kognitivni jaz), preuveličavanje važnosti, veštački emotivni naboj, senzacionalističke fraze. (Dokumentovano u `annotation/guidelines.md`.)
3. **Kalibracija:** **220 naslova** (po 110 od svakog) anotirana **nezavisno** od oba člana.
4. **Glavna anotacija:** ravnomerno podeljeno — Filip 1497, Danilo 1497.
5. **Analiza saglasnosti + statistika.**

### Međuanotatorska saglasnost (IAA)
- **Cohen's kappa = 0.640** („dobro/good"), procentualno slaganje **82.7 %** (182/220).
- Cilj iz plana **κ ≥ 0.6 → ispunjen.**
- Neslaganja (38/220) dosledna i jednosmerna (Filip nešto šire tumači klikbejt) → tipično za **semantičku** (a ne površinsku) granicu.
- Izveštaj: `results/faza2_iaa_izvestaj.md`, sirovo: `results/faza2_iaa.txt`.

### Finalni skup
- 38 spornih naslova rešeno **adjudikacijom** (usaglašena labela).
- **`data/annotated/dataset.tsv` = 2200 naslova, balans 1100/1100** (po klasi), 0 duplikata, 0 praznih labela.
- Statistika: `results/faza2_statistika.txt`.

**Q&A za odbranu:**
- *Zašto 2200 a ne svih 2994?* — Profesor je tražio balansiran skup ~1100/1100; iz 2994 (49.3 %/50.7 %) izvučen balansiran podskup. Višak (~800) ostaje kao rezerva.
- *Zašto je κ=0.64 dovoljno?* — Iznad praga 0.6; neslaganja su na suptilnim graničnim slučajevima, ne na očiglednim — što potvrđuje da zadatak nije trivijalan (površinski).

---

## 3. Faza 3 — Obučavanje i evaluacija modela

**Protokol (po postavci, NEMA fiksnog train/test split-a):**
- Baseline + enkoderski: **10-slojna stratifikovana unakrsna validacija (CV)**; baseline dodatno **ugnežđena (nested) CV** za hiperparametre.
- Dekoderski: **ceo skup** za evaluaciju.
- **Metrike (identične za sve modele radi poređenja):** accuracy, preciznost/odziv/F1 za **klikbejt klasu**, macro-F1, ROC-AUC.
- Skup: balansiranih **2200** (1100/1100). Seed=42.

**Q&A:** *Zašto nema train/test split-a?* — Postavka eksplicitno propisuje 10-fold stratifikovanu CV (i nested CV za hiperparametre); CV sama deli podatke fold-po-fold, nested petlja bira hiperparametre bez curenja.

### 3a — Baseline (lokalno, CPU) ✅
- Modeli: **Logistička regresija + Naivni Bajes** (Multinomijalni i Bernoulli).
- Pun grid (72 konfiguracije): `normalize {none, stem, lemma} × šema {bow, tf, idf, tfidf} × n-gram {1-1, 1-2} × model`.
- **Pretprocesiranje:** lowercase, uklanjanje interpunkcije, ćirilica→latinica; stemovanje (heuristički) ili lematizacija (classla).
- **Bez curenja:** stem/lemma jednom nad celim skupom; **vektorizator (vokabular + IDF) se uči UNUTAR svakog fold-a**.

**Najbolji baseline: Naivni Bajes (MNB) + stemovanje + TF-IDF + bigrami → F1(klikbejt) = 0.646, ROC-AUC = 0.676.**

Efekti faktora (prosečan F1):
| Faktor | Nalaz |
|---|---|
| Model | MNB **0.626** > LogReg 0.611 = BNB 0.611 |
| Normalizacija | lemma 0.623 ≈ stem 0.622 ≫ none 0.603 |
| **Ponderisanje** | TF 0.620 ≈ TF-IDF 0.618 ≈ BoW 0.615 > IDF 0.610 |
| N-gram | 1-2 ≈ 1-1 (zanemarljivo) |

Izveštaj: `results/faza3a_baseline_izvestaj.md`, sirovo: `results/baseline_results.csv`.

**Q&A:**
- *Ponderisanje (profesorova sugestija)?* — Izmereno eksplicitno: TF/IDF/TF-IDF. Na kratkim naslovima razlika je mala (svaka reč retka, IDF ima malo prostora). TF-IDF jeste u vrhu, ali ne dominira nad pukim brojanjem — **iskren nalaz**.
- *Zašto NB najbolji?* — Kratki tekstovi, retke reči; NB dobro radi sa visoko-dimenzionalnim retkim odlikama.
- *Stem vs lemma?* — Praktično izjednačeni; jeftini heuristički stemmer dostiže classla lematizaciju.

### 3b — Enkoderski modeli (Colab, T4 GPU) ✅
- **BERTić** (`classla/bcms-bertic`, monolingvalni BCMS) + **mBERT** (`bert-base-multilingual-cased`, multilingvalni).
- Fine-tuning, **10-fold stratifikovana CV**, varijante **epoha {2, 3, 4}**, batch 64, max_len 64, lr 2e-5.
- HuggingFace Transformers (Trainer). Pokrenuto na besplatnom Colab T4.

**Rezultati (mean preko 10 foldova):**
| Model | Epohe | F1(klikbejt) | Acc | ROC-AUC |
|---|---|---|---|---|
| **BERTić** | **2** | 0.695 | **0.713** | **0.795** |
| BERTić | 3 / 4 | 0.687 / 0.677 | … | 0.795 |
| **mBERT** | **2** | **0.707** | 0.690 | 0.757 |
| mBERT | 3 / 4 | 0.676 / 0.666 | … | 0.759 |

Izveštaj: `results/faza3b_encoder_izvestaj.md`, sirovo: `results/encoder_{bertic,mbert}_results.csv`.

**Q&A:**
- *Koliko epoha?* — **2 epohe najbolje** za oba; sa 3/4 F1 i odziv opadaju (overfitting na malom skupu). → kratak fine-tuning optimalan.
- *Mono vs multi?* — mBERT ima viši F1 (0.707), ali **BERTić ukupno jači i stabilniji** (viši AUC 0.795, accuracy, preciznost); monolingvalni model uravnoteženiji za srpski.
- *Odnos prema baseline-u?* — Oba transformera **ubedljivo nadmašuju baseline** (AUC +0.12 kod BERTića), što je glavna teza: bag-of-words ne hvata suptilni klikbejt, kontekstualni enkoderi ga hvataju.

### 3c — Dekoderski model (Anthropic Claude API) 🔄 U TOKU
- Model: **Claude (`claude-haiku-4-5`)** — bez fine-tuninga (zatvoren model) → samo evaluacija na **celom skupu**.
- Poređenje **jezika upita: srpski (SR) vs engleski (EN) prompt**, oba sa definicijom klikbejta, zero-shot.
- **Bitno:** SR/EN se odnosi na **jezik uputstva modelu**, NE na naslove — naslovi su u oba slučaja srpski. Merimo da li jezik prompta utiče na klasifikaciju srpskih naslova.
- Keš odgovora: `results/decoder_cache/` (prekid/nastavak). Kod: `src/decoder/claude_eval.py`, prompti: `src/decoder/prompts.py`.

**Rezultati:** _(popuniti kad run završi — `results/decoder_results.csv`)_
| Varijanta | F1(klikbejt) | Acc |
|---|---|---|
| SR prompt (sr_zero_def) | … | … |
| EN prompt (en_zero_def) | … | … |

**Q&A:**
- *Zašto Claude, a ne ChatGPT/Gemini?* — Profesor je dozvolio „ChatGPT, Gemini **i drugi**". Besplatni **Gemini tier nije dostupan** za naš nalog/region (greška `limit: 0`). ChatGPT bi se plaćao; iskoristili smo **Claude** (plaćeni, ali jeftin za ovaj zadatak ~$1) kao validan dekoderski model.
- *Zašto samo 2 varijante (a ne 6)?* — Profesor traži jedan dekoderski model + poređenje SR/EN prompta — to je pokriveno. Ostale 4 varijante (few-shot, bez definicije) su opciono obogaćenje; kod ih podržava (`--variants`).

---

## 4. Sinteza Faze 3 ⏳ (sledeći korak)
Jedna uporedna tabela: najbolji baseline vs BERTić vs mBERT vs Claude (SR/EN) + diskusija (šta radi najbolje i zašto, ograničenja, dalji rad). Ulaz za finalnu dokumentaciju.

**Očekivani redosled (preliminarno):** transformeri > baseline; dekoder (zero-shot) obično između — biće potvrđeno brojkama.

---

## 5. Reproduktivnost (komande)

```bash
# 3a baseline (lokalno)
.venv/bin/python src/baseline/run_baseline.py --full --normalize none stem lemma
#   → results/baseline_results.csv

# 3b enkoderski (Google Colab T4) — jedan fajl
#   notebook: src/transformers/faza3b_colab.ipynb  ILI:
#   !wget .../src/transformers/colab_train.py && python colab_train.py --batch-size 64
#   → results/encoder_{bertic,mbert}_results.csv

# 3c dekoderski (Anthropic Claude)
export ANTHROPIC_API_KEY=sk-ant-...
.venv/bin/python src/decoder/claude_eval.py --model claude-haiku-4-5 \
    --variants sr_zero_def en_zero_def
#   → results/decoder_results.csv  (keš u results/decoder_cache/)
```

**Repo:** GitHub `filip939/OPJ_ClikcBait`. `.venv/` i tajne (`.env`) su u `.gitignore`.

---

## 6. Tehničke odluke vredne pamćenja (za odbranu)

- **Sudar imena:** folder `src/transformers` se zvao isto kao HF biblioteka → `finetune.py` ima self-healing import (sređuje `sys.path`).
- **Trainer API:** novi `transformers` traži `processing_class=` umesto `tokenizer=` → rešeno detekcijom verzije.
- **Optimizacija 3b:** treniramo jednom do max epoha i evaluiramo posle svake (eval_strategy="epoch") umesto zasebnog treninga po epohi → ~2× brže, iste brojke.
- **Rate-limit (Claude):** nov nalog 5 RPM (presporo) → posle uplate kredita 1000 RPM; throttle `--rpm` u skripti.

---

## 7. Trenutni status (na dan pisanja)
- Faza 1 ✅ · Faza 2 ✅ · Faza 3a ✅ · Faza 3b ✅ · **Faza 3c 🔄 (Claude run u toku)** · Sinteza ⏳ · Faza 4 (dokumentacija) — sledi.
