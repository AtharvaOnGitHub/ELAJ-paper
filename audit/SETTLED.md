# What is settled, and what is still running

Kept by hand. `NUMBERS.md` is generated and says where each figure comes
from; this says which figures are **final** and which are waiting on a job.
A finding in the first table can be written into the paper today.

Last updated 4 November 2026.

---

## Settled. No run will change these.

Every number below is measured on the full labelled pool of the held-out
split, or on the whole corpus, and re-derives through `NUMBERS.md`.

| # | finding | the numbers | why it is final |
|---|---|---|---|
| **A1** | **ELAJ strictly dominates all nine other methods on both axes at once.** No method reaches its menstrual-phase agreement and none reaches its donor-blindness | phase **0.7346**, the maximum of ten; donor recovery **0.5188**, the minimum of ten. 9 of 9 beaten on both simultaneously | both axes use every labelled cell with a cross-donor neighbour. No subsample anywhere |
| **A6** | **A method's disease score is largely a readout of donor memorisation.** ELAJ's is the lowest because its donor recovery is the lowest | Spearman across ten methods, donor recovery vs disease **ρ +0.721, p 0.019**; vs phase **ρ +0.176, p 0.627**; vs cell family ρ +0.409, p 0.241 | derived from two settled columns. The phase row is the control that makes A1 safe |
| **A4** | **Width anti-correlates with cycle recovery.** | width vs phase **ρ −0.650, p 0.042**. PCA at 16 dimensions beats scFoundation (3,072), SCimilarity (128), Harmony (50), scGPT (512) and Geneformer (256) | widths are facts; phase is settled |
| **A5** | **Cell family does not discriminate between methods.** Third place on it is not a loss | spread **0.0873** across ten methods, every one above 0.98 except Geneformer at 0.9023. Compare phase 0.2974 and donor 0.2704 | settled columns |
| **D1** | The phase head supplies a third of the cross-donor phase signal; the architecture carries the rest | 0.7346 → 0.4812, a ratio of excesses: **65.5% architecture, 34.5% head** | one scoring pass, ELAJ only, full pool |
| **D2** | Without the phase head the model pays the held-out split for the training split from epoch 1 | `-phase head`: `val_nb` best at **epoch 0** (0.4083) rising to 0.4256 while `train_nb` falls 0.4140 → 0.3772. BASE turns at epoch 4 (0.4024) | training logs |
| **D3** | ECS travels the frontier rather than expanding it | family +0.0017, phase +0.0051, disease +0.0274 against donor +0.0332, mixing +0.0786 | within-ELAJ deltas, identical protocol both sides |
| **D4** | Pooled order statistics are a phase mechanism | phase −0.0962, family −0.0022 | as D3 |
| **D5** | The sentinel is load-bearing for study mixing | mixing 0.6043 → 0.6260 | as D3 |
| **D6** | Random gene grouping costs disease most | disease 0.3364 → 0.2698 (−19.8%), family 0.9820 → 0.9606 | as D3 |
| **C2** | Cycle separation is concentrated in stromal and epithelial cells | proliferative→secretory, in units of each family's own scatter: 1.07 / 0.98 / 0.39 / 0.34, and 1.07 / 0.99 / 0.54 / 0.29 in the second arm | whole corpus. Carried by Figure 5, no magnitude in prose |
| **C3** | The cycle is continuous and closes | 466,176 cells (29.6%), one cohort, 60 donors, one day each, days 5–30, 22 of 26 present | metadata |
| **C4/C5** | Disease separation appears in marecko's immune compartment and does not reproduce in duempelmann | figure only, no magnitudes | whole corpus |
| **C6** | Surgical staging is not recoverable on held-out donors | stage 0.1313 at p 0.3035 over 16 held-out donors; **0.332 at p 0.005** over 58 whole-corpus donors; grade −0.0414 at p 0.4975, and negative in all six ablated arms | full labelled pool |
| **E1** | Whole-corpus agreement on a donor-constant label is a donor readout | donor agreement 0.327 against chance 0.0060, **54× enriched**, 269 donors, all 1,577,728 cells | whole corpus |
| **E3** | The standard scIB batch metrics are degenerate here | `ilisi_knn` exactly 0.0000 and `pcr_batch` exactly 1.0000 for ELAJ, PCA, scVI and scANVI alike | one run, four methods |
| — | The corpus is one corpus | 416,256 held-out cells, with 176,803 / 224,211 / 108,288 labelled for cell family / menstrual phase / cell cycle phase, identical in the reported arm, all four `fm_*` runs and `wide_transductive` | asserted from the runs' own logs by `verify_numbers.py` |

---

## Running or pending

| what | why it is not settled | what it costs |
|---|---|---|
| **study mixing on the full held-out split** | `study_mixing_max_cells` was 20,000, which on eleven studies is 1,818 each and **19,998 of 416,256**. Fixed 4 November; the default is now every cell | ELAJ's two local arms: minutes on this machine, running. PCA, Harmony, Scanorama: one CPU job. The four foundation models: their dumped latents were deleted, so re-measuring them needs re-embedding |
| **A2, Harmony as the demonstration** | the claim is Harmony halving study separation while losing cycle signal relative to PCA, so it rests on the mixing column | the same CPU job |
| **the frontier's mixing axis in [1]** | the six ELAJ arms were all scored under the old cap | internally consistent, same protocol and same cells across all six, so it is a within-ELAJ comparison. Re-measuring all six needs four ELAJ embeddings we do not hold locally |
| **A7's study-mean reference, 0.4315** | in no file any script reads. It is a computed baseline, not a logged metric | re-derive from the code that produced it |

---

## Which claims need the mixing column at all

**A1, A4, A5, A6 and every D and C finding do not.** They are phase, donor
recovery, cell family, disease, reconstruction and whole-corpus geometry.

Mixing carries exactly two things: **A2**, and the frontier's second axis in
`[1]`. So the pending work is bounded, and the paper's headline does not wait
on it.
