# Faza 3a — Baseline modeli (izveštaj)

> Logistička regresija + Naivni Bajes (MNB/BNB) na balansiranom skupu **2200**
> naslova (1100 klikbejt / 1100 regularan). Protokol: **nested 10-slojna
> stratifikovana CV** (spoljna 10-fold + unutrašnji GridSearchCV za hiperparametre).
> Reprodukcija: `.venv/bin/python src/baseline/run_baseline.py --full --normalize none stem lemma`
> Sirovi rezultati: `results/baseline_results.csv` (72 konfiguracije).

## Najbolja konfiguracija

| Model | Normalizacija | Šema | N-gram | F1(klikbejt) | Preciznost | Odziv | Macro-F1 | ROC-AUC |
|---|---|---|---|---|---|---|---|---|
| **Naivni Bajes (MNB)** | **stem** | **TF-IDF** | **1-2** | **0.646 ± 0.045** | 0.609 | 0.688 | — | 0.676 |

## Efekti faktora (prosečan F1_kb preko svih konfiguracija)

| Faktor | Vrednosti (prosek F1_kb) | Zaključak |
|---|---|---|
| **Model** | MNB **0.626** > LogReg 0.611 = BNB 0.611 | Naivni Bajes najbolji baseline |
| **Normalizacija** | lemma **0.623** ≈ stem **0.622** ≫ none 0.603 | morfološka normalizacija nosi ~2 poena; heuristički stemmer ≈ classla lematizacija |
| **Ponderisanje** | TF **0.620** ≈ TF-IDF 0.618 ≈ BoW 0.615 > IDF 0.610 | slab efekat (~1 poen); TF-IDF u vrhu ali ne dominira nad pukim brojanjem |
| **N-gram** | 1-2 **0.616** ≈ 1-1 0.615 | bigrami zanemarljivo pomažu |

## Diskusija

- **Ponderisanje (profesorova sugestija TF/IDF/TF-IDF umesto stop-reči):** izmereno
  eksplicitno. Na kratkim naslovima razlika između pukog brojanja (BoW) i TF-IDF je
  mala — svaka reč je retka, pa IDF ima malo prostora da diskriminuje. TF-IDF jeste
  najbolja pojedinačna šema, ali prednost je u granicama standardne devijacije.
- **Skroman apsolutni nivo (~0.65 F1, ~0.68 AUC)** je očekivan: definicija klikbejta
  cilja *suptilne* manipulacije (uskraćivanje ključne informacije, emotivni naboj),
  koje bag-of-words pristup teško hvata. Ovo je glavna motivacija za enkoderske
  modele (Faza 3b).
- **Napomena o BernoulliNB:** binarizuje ulaz, pa su mu rezultati identični preko
  različitih šema ponderisanja (TF/IDF/TF-IDF) — očekivano ponašanje.

## Reprodukcija

```bash
.venv/bin/python src/baseline/run_baseline.py --full --normalize none stem lemma
#   → results/baseline_results.csv  (sortirano po F1_kb, opadajuće)
```
