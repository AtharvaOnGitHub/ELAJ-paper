# Results — the findings, inventoried before anything is ordered

**Edit this file. Nothing gets written as prose until you have.**

Every number below is read from `Outputs/Benchmarks/*/benchmark.csv`,
`Outputs/validate/`, or `axw1008/docs/paper/ABLATIONS.md`. Nothing is from
memory. Where a figure is provisional or not comparable across runs, it says
so.

**No ordering here, by design.** This is the list and the categories; scoring
and sequence come next.

---

## A. ELAJ against the field — cross-donor, held-out

All at the reported arm unless stated. Chance is given where it exists.

| # | finding | numbers | status |
|---|---|---|---|
| A1 | **ELAJ holds more cycle signal than anything else tested.** | phase 0.7346 at 16 dims; 0.7514 at 24. Next best scVI 0.7053, scANVI 0.6971, PCA 0.6906. Chance 0.370 | solid |
| A2 | **ELAJ removes study signal far better than anything else.** | study mixing 0.4712 against next-best scGPT 0.6284, scANVI 0.6964, scVI 0.7161, PCA 0.7804, scFoundation 0.8076. Lower is better | solid |
| A3 | **ELAJ is the least donor-identifiable representation tested, by a wide margin.** | donor recovery 0.2406 against Geneformer 0.5421, scGPT 0.5630, PCA 0.5654, scVI 0.6734, scanorama 0.8223. Lower is better | solid |
| A4 | **Foundation models are near chance on cycle phase despite 16 to 192 times the width.** | scGPT 0.4869 at 512 dims, Geneformer 0.4372 at 256, scFoundation 0.6449 at 3,072 — against PCA's 0.6906 at 16. Chance 0.370 | solid |
| A5 | **ELAJ does NOT win on cell type, and loses to PCA at equal width.** | family 0.9841 against SCimilarity 0.9896 (128 dims) and PCA 0.9868 (16 dims). Third of twelve | solid, and it must be declared |
| A6 | **Disease is weak for every method, ours included.** | ELAJ cross-donor disease max 0.3787 and negative in some cohorts (-0.1076); scFoundation 0.4486, scANVI 0.4221, scVI 0.4190 all above our best | solid |
| A7 | **Reconstruction beats a study-mean baseline by 6.5%.** | `val_nb` 0.4024 against 0.4315. Training moves it by 0.005 to 0.047 nats depending on arm | solid, and uncomfortable |

**The shape of A1 + A2 + A3 together is the paper's central benchmark
claim**: ELAJ is simultaneously the best at discarding donor and study and
the best at keeping the cycle, which is precisely the trade the Introduction
says cannot be had by tuning a correction strength.

---

## B. The frontier — what the method gives that a fixed model cannot

| # | finding | numbers | status |
|---|---|---|---|
| B1 | **The trade-off is controllable, and the two knobs do different things.** `lambda_dab` moves the frontier, `w_kl_gauss` travels along it. | the pre-registered 2-knob factorial; `lambda_dab` 7/168/336 at two latent prices | solid |
| B2 | **A defeated discriminator is not evidence that a latent is study-free.** The encoder hides study from a weak classifier rather than discarding it. | adversary loss correlated **+0.883** with donor kNN at m3, and **+0.890** with study kNN at m2_cls40. Both should be negative if the term worked | graded **B** in LEVERS.md |
| B3 | **Discriminator capacity, not batch composition, was the cause.** | one 64-unit ReLU layer through m4 to three 256-unit LeakyReLU layers at `58cc532`; scGPT's own DAB trains on single-study batches too, verified from their source | solid |

B2 is the most transferable negative result the project holds. "Our adversary
converged to chance, therefore batch effect is removed" appears as evidence
in published single-cell work, and this is a measurement that the inference
is unsound.

---

## C. What the latent holds — whole corpus, 1,577,728 cells

Discovery, not competition. No baseline column, by the rule in
`OUTSTANDING.md`.

| # | finding | numbers | status |
|---|---|---|---|
| C1 | **Cells group by what they are, not where they came from.** Stromal cells from five tissues land together; most cells in each region carried no cell-type label at all | cross-donor family 0.9841; the UMAP crops | solid; claim stays at the level the approximation supports |
| C2 | **Cycle displacement splits by cell type, and the supervision cannot have produced the split.** The phase head is one linear map over the whole latent and was never given cell type. | displacement in units of each type's own width: stromal 1.07, epithelial 0.98, endothelial 0.39, immune 0.34. **Identical across both frontier arms** | solid, and this is the headline |
| C3 | **The cycle is continuous and closes.** | day 8 through 15-20 to 25-30 with the ends meeting, read off a cyclic colour map rather than inferred | solid; **day values come from one cohort**, stated in the same breath |
| C4 | **Disease signal concentrates in the immune compartment.** | 0.77 / 0.83 inside marecko's immune cells against 0.22 corpus-wide; rank 1 of 4 in both arms | solid |
| C5 | **And it does not replicate across cohorts.** | duempelmann's families at 0.19-0.29 with the ordering flipping between arms | solid — reported as a result, not a caveat |

C2 is the strongest thing in the paper. C4 and C5 belong in the same
subsection: a finding and its non-replication, stated together.

---

## D. What the latent needs — the A1 ablations

Five single-key changes against `p1_dab168_kl1`. Benchmark numbers,
cross-donor, held-out.

| # | finding | numbers | status |
|---|---|---|---|
| D1 | **The phase head supplies about 69.5% of the phase margin over chance; the architecture supplies the other 30.5%.** Neither "phase emerges" nor "phase is supervised" — a measurement of how the two divide | phase 0.7346 to 0.4812 on removal, chance 0.370 | solid |
| D2 | **The phase head is also a regulariser.** Without it the model fits the training split at the expense of held-out cells from epoch 1 | `train_nb` 0.4140 to 0.3772 while `val_nb` 0.4083 to 0.4256 | solid |
| D3 | **ECS traverses the frontier rather than expanding it.** Removing it improves every biology axis and worsens every cost axis — the same kind of knob as `w_kl_gauss`, not an independent gain | family +0.0017, phase +0.0051, disease +0.0274; donor 0.5188 to 0.5520, mixing 0.6043 to 0.6829 | solid |
| D4 | **Pooled order statistics are a phase mechanism, not a general one.** | phase -0.096, family -0.002 on removal | solid |
| D5 | **The sentinel is load-bearing for study mixing.** Sentinel positions are excluded from the reconstruction loss and zeros are not, so the panel has no route into the latent | mixing 0.6043 to 0.6260 on removal | solid; **my 26 Oct correction of the original prediction was itself wrong and is withdrawn** |
| D6 | **Random gene grouping costs disease most, in the arm with the best reconstruction in the project.** | disease 0.3364 to 0.2698, -20%; family 0.9820 to 0.9606 | solid |
| D7 | **Stage and grade carry nothing in any configuration.** | p 0.12 to 0.63; grade negative everywhere. A property of the labels, not of the model | solid — belongs in the paper as a limitation |

**6 of 11 banded predictions landed.** The predictions were registered in
each config before the runs started, which is worth one sentence.

---

## E. Findings about measurement itself

NMI's readership is methodological. These transfer beyond this dataset and I
would argue they are undersold if they sit in Methods only.

| # | finding | numbers | status |
|---|---|---|---|
| E1 | **Whole-corpus neighbour agreement on a donor-constant label is a readout of donor memorisation.** Across six arms it ranks almost identically with donor recovery; the cross-donor estimator breaks that. `random groups` is best of six on plain disease and **worst of six** cross-donor | Spearman rho +0.943 for disease, +0.829 for phase, against +0.371 for cell family, the only label that varies within a donor. Estimator cuts disease to +0.429 | solid |
| E2 | **The same-donor floor is large and the model can raise it.** | 25% to 61% of a cell's hundred neighbours are same-donor; chance is 0.6% to 3.1%, so 20 to 50 times enriched; 44% to 71% of plain agreement is the free part | solid |
| E3 | **The standard scIB batch metrics are degenerate on this corpus.** | `ilisi_knn` exactly 0.0000 and `pcr_batch` exactly 1.0000 for PCA, scVI, scANVI and ELAJ alike; `kbet` 0.000 to 0.025 for all | solid |
| E4 | **Permutation p has a floor set by donor count, so "not significant" can mean undetectable.** | smallest attainable p is 1/201; stage reaches 58 donors and grade 60, against 269 for disease status | solid |

---

## F. Limits that are findings, not apologies

| # | | numbers |
|---|---|---|
| F1 | 16 dimensions against baselines at 128 to 3,072, so the comparison is not width-matched. **But PCA at 16 beats scGPT at 512 on both biology axes**, so width is not what drives it | A1, A4, A5 |
| F2 | The cycle-day continuity rests on one cohort | C3 |
| F3 | The immune disease result does not replicate | C5 |
| F4 | 17,873 held-out cells, 4.3%, share a donor with training through the one overlapping study pair | Methods |
| F5 | One study is a follicular-fluid aspirate labelled as endometrium | 45,312 cells, 2.87%, 6 of 269 donors |
| F6 | Reported arms are single runs; seed variability measured at 4% | |

---

## Open questions before we order

1. **Does category E go in Results or stay in Methods?** E1 and E2 are
   measurements, which argues Results. Against: they are measurements about
   our own estimator rather than about the biology or the model, and a
   reader may read a section defending the metric as defensive. My view is
   that E1 earns Results on its own — `random groups` inverting from best to
   worst is a striking result in its own right — and E2-E4 belong in Methods.
2. **A5 and A7 are negative and both are real.** We lose to PCA at equal
   width on cell type, and reconstruction beats a study-mean baseline by only
   6.5%. Both need a home. Declared inside the benchmark subsection, or
   gathered in a limitations passage?
3. **How many of D1-D7 survive?** Seven ablation findings is more than
   ~1,800 words of Results can carry alongside everything else. D1 and D3
   look essential, D7 is a limitation rather than an ablation result, and
   D2's regulariser finding is the most surprising.
4. **Is A6 reportable at all?** Disease is weak for everyone and three
   baselines beat our best cohort-level figure. Stating it is honest;
   omitting it would be noticed, since the benchmark table carries disease.
