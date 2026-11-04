# Figures — panel by panel

**Edit this file. A panel does not get drawn until its row is agreed.**

Six main display items, which is NMI's cap for an Article. Extended Data is
capped at ten separately and Supplementary Information is uncapped.

Every number in the "supports" column is traceable through
`audit/NUMBERS.md`. Nothing in this file is typed from memory.

---

## Why panels, and why legends are written long

NMI, *Content Types*: main text is up to **3,500 words, excluding abstract,
Methods, references and figure legends**. Nature's formatting guide: legends
"should be fewer than **300 words each**", and a multi-panel composite
"usually needs to take about half a page".

So six figures carry up to **1,800 words of legend that cost nothing against
the 3,500**. A finding that lives in a panel and its legend costs zero
main-text words; the same finding enumerated in prose costs around 125. With
roughly twenty findings and ~2,000 words of Results, the figures are not
illustrations of the prose. They carry findings the prose points at.

Consequence: every main figure is a composite, panels are used generously,
and legends are written to the 300-word limit rather than kept brief.

**Each figure must be regenerable by one command from a committed script.**

**Every cross-donor value in this file is an excess over chance**, computed
as `(agreement − chance) / (1 − chance)` in
`endo_model/evaluation/sufficient_stats.py`. Zero is chance, one is perfect,
and a negative value is possible. **Never subtract a chance rate from one of
them.** The comparator a panel should draw is the permutation null's 95th
percentile, carried per row in the benchmark's own `note` column.

---

## Status vocabulary

| | |
|---|---|
| **exists** | the asset is on disk and is publication-shaped |
| **asset** | the data is drawn but the panel needs compositing or restyling |
| **build** | the data exists, the panel does not |
| **blocked** | waiting on the unified scoring run |
| **draw** | no data, a schematic to be drawn by hand |

---

## The mapping, and why it is a mapping

Six figures, twenty-odd findings, ~2,000 words of Results. A finding that
lives in a panel and its legend costs **zero** main-text words; enumerated in
prose it costs about 125. So the figures are not illustrations of the prose.
They are where the findings that prose cannot hold are gathered.

**What a figure is for here.** Each one clumps the evidence for something the
Results cannot say succinctly, usually because the claim is about *structure*
across many methods or arms rather than about one number. A reader should be
able to reach the conclusion from the panel. They should not be told it
inside the panel.

**What that forbids.** No callouts, no arrows pointing at the good news, no
annotation naming our own arm as the hero, no title that states the result.
The legend defines the axes and the symbols. The data does the rest, and it
stays open to a reader who disagrees with us.

| figure | the thing prose cannot say | findings |
|---|---|---|
| **1** | that a donor-constant trait and a batch effect are the same geometric object | Introduction ¶3 |
| **2** | that two knobs move a model along a trade-off, and in different directions | B1 |
| **3** | that across ten methods the axes trade against each other, and one point sits in the corner | A1, A2, A4, A5, A6, E3 |
| **4** | where disease signal sits and where it fails to reappear | C1 part, C4, C5, C6 |
| **5** | that the cycle closes, and that it separates two cell families and not the other two | C2, C3, C1 part |
| **6** | what each component is load-bearing for, across five single-key changes | D1–D6, B2, B3 |

**Prose today points at:** `[1]`→1b, `[3]`→5a, `[4]`→4b, 4c, 4d. `[2]` and
`[5]` are unwritten. `[1]`'s reference is stale: the frontier is Figure 2.

---

## What changed in the findings, and what the figures now have to carry

Settled on 4 November, from the completed field table. These supersede the
earlier per-axis claims and they change what Figures 3 and 6 must show.

| was | is now | consequence for the figure |
|---|---|---|
| A1 "best at phase" | **ELAJ is the only method that is simultaneously highest on phase and lowest on donor recovery.** No method reaches either | a **scatter** of phase against donor, ten methods. The reader sees the corner. Bars cannot show a joint claim |
| A2 "we remove study signal best" | **Harmony removes it best, and pays in cycle signal** — 0.4168 against PCA's 0.8435 while phase falls 0.6457 → 0.6186 | mixing against phase, same scatter treatment. Harmony's position *is* the argument |
| A6 "disease is weak for everyone" | **disease score tracks donor memorisation**, ρ +0.721, p 0.019 across ten methods; phase does not, ρ +0.176 | disease against donor recovery, ten points. The trend is the finding |
| A4 "foundation models are near chance" | **width anti-correlates with phase**, ρ −0.650, p 0.042 | phase against width, log x |
| A5 "we lose cell type" | **the axis is saturated**: spread 0.0873, nine of ten above 0.98 | shown by the shared y-range, not argued |
| B2 "+0.883 at one arm" | **positive in 25 of 28 arms, median +0.615** | a distribution, not two numbers |
| C2 ratios in prose | **figure only**, no magnitudes anywhere | per-cell-family panels |
| C4/C5 ratios in prose | **figure only** | crops side by side |

---

## Figure 1 — The confound, and where the model pulls it apart

Schematic. No data anywhere in it. The one figure a reader must understand
before any other, and the one most at risk now the cap is six: it shows
nothing measured, which is the easiest kind for an editor to cut. It stays
because the Introduction's central argument is geometric and a sentence
cannot carry it.

| panel | type of vis | purpose | matching prose | supports / numbers |
|---|---|---|---|---|
| a | schematic, cells grouped under one donor | one biopsy per donor, so every cell of a donor shares one cycle phase | Introduction ¶3 | none. 254 people, 11 studies, one biopsy each is the only quantity |
| b | schematic, two offsets drawn side by side | the per-donor phase offset and a batch effect are the same geometric object | Introduction ¶3 | none |
| c | schematic, model block diagram | where the two are separated: adversary on the latent, phase head on the latent, decoder given study directly | Introduction ¶3, Methods *Decoder conditioning* | none |

**Status: draw.** `figures/scripts/figure1.py` exists and produces a first
version. Open items carried from the 2 November session: whitespace between
rows 1 and 2; panel d undecided; the `similarity` and `reconstruction` boxes
clip; the spider's `cell type` label is wrong.

---

## Figure 2 — The frontier

| panel | type of vis | purpose | matching prose | supports / numbers |
|---|---|---|---|---|
| a | scatter, Pareto front drawn | cross-donor phase against donor recovery over the six arms | Results [1] | the six arms: donor 0.3975–0.5837, phase 0.5922–0.7346 |
| b | scatter, same arms | the same against study mixing | Results [1] | mixing 0.5129–0.7381 |
| c | two small panels, one per knob | `lambda_dab` moves the frontier, `w_kl_gauss` travels along it | Results [1] | reported arm 0.5188 / 0.6043 / 0.7346 / 0.9820 |

**Carries:** B1.

**The legend solves the arms-table problem.** No hyperparameter table appears
anywhere in this paper. The frontier points still need their coordinates, so
each arm's two knob values go in the legend, where they cost no main-text
words and sit beside the point they describe.

**Status: asset.** `Outputs/figures/frontier/` has five panels for both arms
(`frontier_headline`, `frontier_donor_knn`, `frontier_study_mixing`,
`frontier_val_nb`, `frontier_neighbours_kept`), plus
`Outputs/figures/ELAJ_frontier.xlsx` for choosing which points appear.
Needs selecting down to three panels and restyling to one visual family.

---

## Figure 3 — ELAJ against the field

The victory march in one item. Every panel oriented higher-is-better or
marked otherwise.

| panel | type of vis | purpose | matching prose | supports / numbers |
|---|---|---|---|---|
| a | grouped bars, width annotated per bar | cross-donor menstrual phase across every method | Results [1], merged | **blocked** |
| b | grouped bars, supervised methods hatched | cross-donor cell family, with SCimilarity and scANVI marked as supervised on the label being scored | Results [1] | **blocked**. Pre-run: ELAJ 0.9820, SCimilarity 0.9896, PCA 0.9865 |
| c | grouped bars, lower-better marked | donor recovery | Results [1] | **blocked** |
| d | grouped bars, lower-better marked | study mixing | Results [1] | **blocked** |
| e | grouped bars or a flat strip | the scIB batch metrics are degenerate here, which is why c and d are measured our way | Results [1], or Methods | `ilisi_knn` exactly 0.0000 and `pcr_batch` exactly 1.0000 for PCA, scVI, scANVI and ELAJ alike; `kbet` 0.000–0.025 for all |
| f | grouped bars | disease, every method, nobody good | Results [1] | **blocked**. Pre-run: ELAJ 0.3364, scFoundation 0.4024 |

**Carries:** A1, A2, A3, A4, A5, A6, E3. Seven findings with no prose
enumeration: Results states the claim and points here.

**Blocked on the unified scoring run.** Harmony and Scanorama currently have
no valid source at all; their only rows are `r8_all`, which scores ELAJ at
phase 0.1161 and PCA at 0.2856 on a third of the cells. Every other baseline
figure comes from a run with a different gene policy, and the two cannot be
quoted in one chart.

**Status: asset for a, c, d; build for b, e, f; all blocked.**
`Outputs/figures/bars/` holds `bars_field`, `bars_p1`, `bars_best`,
`bars_ceiling`, each with and without clustering. The caption carries the
width limitation and the per-method supervision.

---

## Figure 4 — Disease, and where it is not

| panel | type of vis | purpose | matching prose | supports / numbers |
|---|---|---|---|---|
| a | whole-corpus UMAP, cell-type regions outlined | the entry point every crop below refers back to | Results [2] | cross-donor cell family 0.9807 whole corpus, 0.9820 held out |
| b | UMAP crop, coloured case against control, marecko | disease separation concentrates in the immune compartment | Results [4] ¶3 | **no number**. The `over_scatter` ratios were cut with the [3] paragraph; the panel carries the claim |
| c | the same crop for duempelmann, beside b | the non-replication, in magnitude and in which family leads | Results [4] ¶3 | **no number**, same reason as b. The leading family differs between arms and the panel must show both |
| d | dot or bar per arm, **null95 band drawn behind each point**, donor count on the axis | stage and grade against their own permutation nulls, so a reader sees why 0.1313 is not significant | Results [4] ¶2 | stage 0.1313 against null95 0.42, p 0.3035 held out; 0.332 at p 0.005 whole corpus; grade −0.0414 against null95 0.12, p 0.4975; 58 and 60 donors against 269 |

**Carries:** C1 in part, C4, C5, C6.

**Deliberately one item.** Splitting b from c would let a reader take the
positive without the negative. And d belongs here rather than with the
ablations: it is a finding about the labels, not about the model.

**Panel d must not overstate.** Whole-corpus stage is significant and
held-out stage is not. Both go on the panel or the figure contradicts the
prose.

**Status: asset for a and b (`Outputs/analysis/umaps/p1_dab168_kl1/01_cell_family.png`,
`03_disease.png`); build for c and d.** The arm must be named in the caption.

---

## Figure 5 — The menstrual cycle through ELAJ

The headline figure. Panel letters follow the Results paragraph order.

| panel | type of vis | purpose | matching prose | supports / numbers |
|---|---|---|---|---|
| a | UMAP crop on a cyclic colour map | the cycle is continuous and closes | Results [3] ¶2 | 466,176 cells, one cohort, 60 donors, 22 days between day 5 and 30 |
| b | small multiples, one UMAP per cell family, coloured by phase | phase does not separate every cell type equally. Read off the picture, not off a ratio | **none — figure only** | no number. C2 is carried visually and the claim is the ordering, not a magnitude |
| c | the same small multiples, second frontier arm | the ordering reproduces at a different information cost | **none — figure only** | no number |
| d | UMAP crop coloured by tissue | stromal cells from five tissues land together; epithelium is almost purely endometrial | Results [2] | cross-donor cell family 0.9807 whole corpus |

**Carries:** C3 and C1's other half in a and d; **C2 in b and c and only
there.**

**The argument the legend must make:** the phase head is one linear map over
the whole latent and was never given cell type, so it cannot have produced
the split in b. The honest limit sits in the same legend, not a footnote:
the day values come from one cohort of 60 donors contributing one day each.

**Panel b was a bar of `over_scatter` ratios and is not any more.** AW cut
the matching Results paragraph on 2 November because that statistic divides a
centroid distance by a root-mean-square radius, which describes a cloud only
if the cloud is a filled isotropic ball. The panel inherited the assumption
whole. No number replaces it: no further calculation is done unless a
reviewer asks.

**Never colour a panel here by donor.** Donor identity is 54-fold enriched
among a cell's hundred nearest neighbours (0.327 against 0.0060). A
donor-coloured panel argues for the estimator, not for the result.

**Open: four cell families or three.** Endothelial was dropped from the
animation on an earlier ruling.

**Status: asset for a (`08_cycleday.png`) and d (`02_tissue.png`); build for
b and c** by compositing frames from
`figures/scripts/movie_cycle_by_celltype.py`.

---

## Figure 6 — What the latent needs

The figure an ML reader comes for, and the one most papers in this area do
not publish.

| panel | type of vis | purpose | matching prose | supports / numbers |
|---|---|---|---|---|
| a | grouped bars, five axes, base marked | the five single-key ablations against the base | Results [5] | family 0.9606–0.9837, phase 0.4812–0.7397, disease 0.2698–0.3638, donor 0.3754–0.5520, mixing 0.5305–0.6829 |
| b | stacked bar or annotated axis | the phase margin splits into supervision and architecture | Results [5] | 0.7346 → 0.4812, both already chance-corrected: **65.5% architecture, 34.5% head**. Do not subtract 0.370 |
| c | two lines per arm, train against val by epoch | without the phase head the model pays the held-out split for the training split from epoch 1 | Results [5] | `-phase head`: `val_nb` best at epoch 0 (0.4083) rising to 0.4256 while `train_nb` falls 0.4140 → 0.3772. BASE turns at epoch 4 (0.4024) |
| d | the ablation points drawn ON Figure 2's frontier | ECS travels along the frontier rather than expanding it | Results [5] | family +0.0017, phase +0.0051, disease +0.0274 against donor +0.0332, mixing +0.0786 |
| e | scatter, one point per arm, correlation annotated | a defeated discriminator is not evidence that a latent is study-free | Results [5] | adversary loss against donor kNN +0.883 at m3; against study kNN +0.890 at m2_cls40 |

**Carries:** D1, D2, D3, D4, D5, D6, B2, B3.

**The legend carries the registration.** Predictions were written into each
configuration file before the runs started, 6 of 11 banded predictions
landed, and the misses are reported. That is the sentence that makes this
figure unusual, and it is only honest if the repository is public.

**Panel c must be read down one arm, not across two.** 0.4083 is the
`-phase head` arm's best `val_nb`; BASE's is 0.4024.

**Status: build, all five panels.** Every arm is scored and every number
above re-derives through `audit/NUMBERS.md`. Nothing here is blocked.

---

## What is not a main figure

| | where it goes | why |
|---|---|---|
| the whole-corpus vs cross-donor inversion, ρ +0.943 | Extended Data 1 | E1 was ruled into Methods as the justification for the estimator |
| the same-donor floor per label | Extended Data 2 | E2, already written into Methods *Cross-donor agreement* |
| remaining crop panels: phase, stage, grade, platform, progesterone | Extended Data 3 | `04_phase`, `05_stage`, `06_grade`, `07_platform`, `09_progesterone` all exist |
| the donor-overlap audit, 17,873 cells, 4.3%, one study pair | Extended Data 4 | F4 |
| baseline fitting, inductive against transductive, with `supervised_on` | Extended Data 5 | the protocol a reviewer will want and the prose should not spend words on |
| per-arm comparison tables across the full factorial | Extended Data 6 | |
| sufficient-statistics tables at every coarsening | Extended Data 7 | |
| the cycle animations | Supplementary | they are the clearest evidence for C3 and are not a static panel |

---

## Open questions

1. **Figure 1 shows no data and is the first thing an editor cuts.** If it
   goes, the Introduction's geometric argument has to survive in prose alone.
2. **Figure 3 is entirely blocked** and is also the figure that justifies the
   venue. Nothing about its layout can be settled until the unified run
   returns.
3. **Figure 5 panel b: four families or three.**
4. **Figure 6 panel e draws on arms outside the p-series** (m3, m2_cls40). It
   is the only main panel that does, which needs either a note or a different
   pair of arms.
