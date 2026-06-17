# Faza 3b — Enkoderski modeli (izveštaj)

> Fine-tuning **BERTić** (`classla/bcms-bertic`, monolingvalni) i **mBERT**
> (`bert-base-multilingual-cased`, multilingvalni) na balansiranom skupu **2200**
> naslova (1100/1100). Protokol: **10-slojna stratifikovana CV**, varijante po
> **broju epoha (2/3/4)** kao **ZASEBNI fine-tuning-zi** (svaki sa sopstvenim LR
> rasporedom — po zahtevu „različite varijante po dužini fine-tuninga"), batch 64,
> max_len 64, lr 2e-5. Pokrenuto na Google Colab (T4 GPU).
> Reprodukcija: `python src/transformers/finetune.py --model {bertic,mbert} --epochs 2 3 4 --batch-size 64`
> Sirovo: `results/encoder_bertic_results.csv`, `results/encoder_mbert_results.csv`.

## Rezultati (mean ± std preko 10 foldova)

### BERTić
| Epohe | F1(klikbejt) | Accuracy | Preciznost | Odziv | Macro-F1 | ROC-AUC |
|---|---|---|---|---|---|---|
| 2 | 0.681 | 0.680 | 0.678 | 0.688 | 0.678 | 0.760 |
| **3** | **0.703** | 0.704 | 0.707 | 0.703 | 0.703 | 0.785 |
| **4** | 0.703 | 0.702 | 0.703 | 0.704 | 0.702 | **0.788** |

### mBERT
| Epohe | F1(klikbejt) | Accuracy | Preciznost | Odziv | Macro-F1 | ROC-AUC |
|---|---|---|---|---|---|---|
| 2 | 0.651 | 0.664 | 0.678 | 0.629 | 0.663 | 0.736 |
| **3** | **0.690** | 0.687 | 0.685 | 0.699 | 0.686 | 0.753 |
| 4 | 0.682 | 0.691 | 0.703 | 0.664 | 0.690 | 0.755 |

## Diskusija

- **Broj epoha:** za oba modela **3–4 epohe daju najbolji rezultat**; sa samo 2 epohe
  model je **nedotreniran** (najniži F1/AUC). BERTić se izjednači na 3 i 4 (F1 0.703;
  AUC blago raste do 0.788), mBERT je najbolji na 3 epohe (F1 0.690). Zaključak:
  potrebno je bar 3 epohe fine-tuninga.
- **Mono vs multi:** **BERTić nadmašuje mBERT na svim metrikama** u najboljoj tački
  (F1 0.703 vs 0.690, AUC 0.788 vs 0.753, accuracy 0.704 vs 0.687). Monolingvalni
  BCMS model je očekivano bolji za srpski.
- **Metodološka napomena:** ranija „brza" varijanta (jedan trening do max epoha +
  evaluacija posle svake) davala je obrnut trend (2 epohe „najbolje") — to je bio
  artefakt LR-rasporeda (checkpoint epohe 2 u 4-epoha run-u ima nedovršen LR
  pad). Ispravan, zaseban fine-tuning po epohi pokazuje da je 2 epohe nedovoljno.

## Poređenje sa baseline-om (Faza 3a)

| Model | F1(klikbejt) | ROC-AUC |
|---|---|---|
| Baseline (MNB + stem + TF-IDF) | 0.646 | 0.676 |
| **BERTić (3–4 epohe)** | **0.703** | **0.788** |
| mBERT (3 epohe) | 0.690 | 0.753 |

Oba enkodera nadmašuju najbolji baseline, posebno po ROC-AUC (BERTić +0.11).
Potvrđuje glavnu tezu: linearni/bag-of-words modeli teško hvataju suptilni klikbejt,
dok kontekstualni enkoderi znатно bolje razdvajaju klase.
