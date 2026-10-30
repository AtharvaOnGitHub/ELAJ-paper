# Results — the findings, inventoried and categorised

**Edit this file. Nothing gets written as prose until you have.**

Every number is read from `Outputs/Benchmarks/*/benchmark.csv`,
`Outputs/validate/`, or `axw1008/docs/paper/ABLATIONS.md`. Nothing from
memory.

---

## How NMI structures a Results section

**The structure rule, and I am confident of it** — two independent sources
agree, both summarising nature.com:

> Articles should be divided as follows: **Introduction (without heading),
> Results, Discussion, and Methods. Results and Methods should be divided by
> topical subheadings; the Discussion does not contain subheadings.**

So: our Results carries topical subheadings and our Discussion must not. The
current Discussion plan is four unheaded paragraphs, which already complies.

**The numbers, and these need your eyes rather than mine.** nature.com's
content-types page sits behind an authentication redirect from this machine,
so I could not read it directly. What a search of it reports for **Articles**:

| | reported for NMI Articles | what we have been working from |
|---|---|---|
| main text | **3,500 words**, excluding abstract, Methods, references, figure legends | 4,300 (Nature generic, 8pp at 5-6 items) |
| abstract | **150 words, UNREFERENCED** | 200 words, fully referenced (Nature generic) |
| display items | **6** | 8 |
| references | ~50 | 50 |

**⚠️ If that abstract line is right, I corrected you in the wrong
direction.** Your original header said "NMI allows up to 200 words, no
citations" and I overwrote it with "fully referenced" on the strength of
Nature's generic formatting guide, which says exactly that for Nature
Articles. NMI's own Article spec appears to say 150 and unreferenced. The
local PDFs do not settle it — they are the AIP, initial-submission,
preparing-material and production pages, and none of them carries the Article
word and figure spec. **Please check the content-types page while logged in**;
if it says 150 unreferenced, your instinct was right and the abstract note
needs reverting.

Two knock-on effects if the numbers hold: the figure list allocates **eight**
display items against a cap of **six**, and the main-text budget is 3,500
*excluding* the abstract, which is roomier for Results than my earlier
arithmetic allowed.

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

## Where each finding now sits — AW's rulings, 30 October 2026

### The victory march (A1-A4, B1, C1-C5)

AW: A1-A4 "should be the victory march of this paper. That puts us in SOTA
category straight away." B1 and C1-C5 likewise. These are the subsections
that justify the venue, and they run in sequence rather than being
interleaved with what we found out about the model.

**E3 moves into A**, on AW's ruling that it is a result rather than hedging:
the standard scIB batch metrics are degenerate on this corpus --
`ilisi_knn` exactly 0.0000 and `pcr_batch` exactly 1.0000 for PCA, scVI,
scANVI and ELAJ alike, `kbet` 0.000 to 0.025 for all. It belongs beside A2
because it is why study mixing is measured the way it is.

### A5 is not a loss. RESOLVED, and verified from the data

AW: "ELAJ is comparable on cell-type. I believe SCimilarity was
semi/supervised on it. We do not 'lose' cell type." Confirmed from the
`supervised_on` column of the benchmark table:

| method | supervised on | width | cross-donor family |
|---|---|---:|---:|
| SCimilarity | **cell family** | 128 | 0.9896 |
| PCA | --- | 16 | 0.9868 |
| **ELAJ** | --- | 16 | **0.9841** |
| scANVI | **cell family** | 16 | 0.9835 |
| scVI | --- | 16 | 0.9828 |

Both methods that beat us by more than 0.003 **were given the label being
scored**. Write it as comparable, with the supervision declared per method,
which the Methods already promises.

⚠️ **A correctness problem in our own table, and it cuts against us if
unfixed.** ELAJ's `supervised_on` is **empty** in every benchmark row, but
ELAJ *is* supervised on menstrual phase. A reader of that table would
conclude ELAJ saw no labels at all, which overstates A1 -- the headline
result. This is `OUTSTANDING`'s "supervised_on for ELAJ rows" and it must be
fixed before the table is published.

### A6 is an open question for the field, not our failure

AW: disease being weak for everyone "is a curious result to be mentioned
against the fact that we seem to have the best biology and least donor
identity. It is more an open question for the field rather than a failure on
our part." So: stated inside the benchmark subsection, framed as the field's
open problem. Three baselines reach a higher best-cohort figure than ours
(scFoundation 0.4486, scANVI 0.4221, scVI 0.4190 against our 0.3787) and
none of them is good.

### A7 gets one or two lines

AW: "Reconstruction was an objective of training. Reconstruction does not
define what our latent space is capable of." So the 6.5% over a study-mean
baseline is stated and not argued, and the no-per-gene-intercept point from
Methods is what a reader needs if they press.

### B2 and B3 leave the frontier subsection

AW: "B2 and B3 are results closer to ablation. We found something about the
model rather than the model found something about the data. I'd separate them
from B1." So B1 stays in the victory march and B2-B3 join D.

### D is the section an ML reader actually wants

AW: "These are the results that a true ML researcher would actually want to
read properly. The fact that we have them and we want to publish them is
itself a huge thing for a paper like ours to do. Most other papers don't do
this."

So D1-D6 plus B2-B3 form one subsection, and the fact that the predictions
were **registered in each config before the runs started** is worth its
sentence -- 6 of 11 banded predictions landed, and the misses are reported.

### D7 becomes C6, and splits across two sections

AW: "I would point D7 to discussion. This is the disruptive finding that
confirms what the patients go through: disease staging is not biologically
supported as far as we can tell and we should switch to a more biological
staging of this disease. We would need to write the numbers in results
though. Maybe this is a C6 instead of D7?"

Yes, C6. It is a discovery about the labels rather than an ablation result,
and it sits with C4 and C5 as the third disease finding.

| | |
|---|---|
| **Results (C6)** | the numbers only. Stage and grade carry nothing in any configuration: p 0.12 to 0.63, grade negative everywhere, across every arm in the A1 wave and both frontier arms. Stage reaches 58 donors and grade 60, so the p-floor is stated here too or the negative cannot be read |
| **Discussion** | the interpretation. Surgical staging is not recoverable from transcriptional state, which is consistent with what patients report -- stage does not predict symptom severity -- and argues for a staging that is biologically grounded rather than anatomical |

**This is the paper's most disruptive claim and it needs its evidence
airtight.** Two cautions before it is written: the p-floor means we are
reporting an absence we cannot distinguish from undetectability at 58-60
donors, and `EndometriosisGrade` reaching only 60 donors is thin. The
Discussion wording must say "not recoverable from this corpus at this donor
count", not "not biologically real".

### E leaves Results, except E3

AW: "These are either discussions or hedging. I would not have these in
results unless we are presenting numbers."

| | goes to |
|---|---|
| E1, the donor-memorisation readout at rho +0.943 | **Methods**, inside *Cross-donor agreement*, where it is the justification for the estimator. I had argued for Results and AW overruled it |
| E2, the same-donor floor | **Methods**, already written into *Cross-donor agreement* |
| E3, scIB degeneracy | **Results, category A** |
| E4, the p-floor | **Methods**, already written -- but it is also quoted in C6, because a negative result cannot be read without it |

### F stays out of Results

All six are Discussion limitations, which is where the Discussion plan
already puts them.

---

## Open questions

1. **Six display items or eight.** If NMI caps Articles at six, two of the
   eight planned figures merge or go. The victory march needs the frontier
   plot, the against-the-field panels, the cell-type crops and the cycle
   crop; that is four, leaving two for the ablations, the disease finding and
   the confound schematic.
2. **How much of the victory march can 3,500 words carry** alongside D,
   which AW wants read properly? D1-D6 plus B2-B3 is eight findings.
3. **Does the confound schematic (Figure 1) survive** at six display items?
   It is the one figure a reader needs before any other, and it shows no
   data.
