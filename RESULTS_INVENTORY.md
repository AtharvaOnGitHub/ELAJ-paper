# Every result we have, by type

Built 13 November 2026 before the Results remould. Numbers are from
`audit/NUMBERS.md` (re-derived at build time) and `CLAIMS_SUMMARY.md`.
Nothing here is from memory.

**Significance** is how strong the result is on its own: effect size, donor
count, how hard it would be to argue with. **Importance** is how much this
paper needs it. They come apart often, and where they do is where the
editing decisions are.

**AW's ruling, 13 November:** where a result is proved more than one way,
all the proofs stay. Corroboration is not redundancy.

---

## Type A. Where ELAJ sits against the field

Ten representations, one scoring pass, same corpus.

| # | result | sig | imp | figure? |
|---|---|---:|---:|---|
| **A1** | **All nine competing representations are strictly worse than ELAJ on BOTH axes at once: higher donor recovery AND lower cycle agreement. Nine of nine.** Donor 0.5188 against 0.5421–0.7892; phase 0.7346 against 0.4372–0.7303 | **9** | **10** | **Yes.** The two-axis scatter with the Pareto front. One panel does what a paragraph cannot: show there is no point below-and-left of us |
| **A2** | **1,883,986 parameters beats scFoundation at 100M and scGPT at 512 dimensions.** ELAJ 16 dims, phase 0.7346; scFoundation 3072 dims, 0.6449; scGPT 512 dims, 0.4869; Geneformer 256 dims, 0.4372 | 8 | **10** | **Yes.** Parameter count against phase recovery, log x-axis. The gap is three orders of magnitude and a table hides that |
| **A3** | Representation width correlates **negatively** with cycle recovery across the ten methods: Spearman −0.650, p = 0.042 | 6 | 7 | Optional. Small inset on A2's panel; it is the same claim with a statistic attached |
| **A4** | **Cell family is saturated across the whole field**: 0.9023–0.9896, spread 0.0873, against a phase spread of 0.2974. Every method solves it | 8 | 7 | No. One sentence with the two spreads |
| **A5** | ELAJ is the only method in the ten supervised on menstrual phase; scANVI and SCimilarity are supervised on cell family | 7 | 6 | No. Belongs in the table's own column, which it has |

⚠ **A2 is the NMI credential.** AW: *"If parameter efficiency isn't part of
the main story then this paper loses its credential for being in Nature
Machine Intelligence."*

---

## Type B. The frontier, which is the paper's central measurement

| # | result | sig | imp | figure? |
|---|---|---:|---:|---|
| **B1** | **Two knobs move the model along a frontier rather than to a better point.** Six arms: donor 0.3975–0.5837, phase 0.5922–0.7346. Removing more of the donor costs cycle signal, monotonically | **9** | **10** | **Yes, and this is Figure 2's job.** The six arms joined, with both knobs visible. Prose cannot show a curve |
| **B2** | The adversary buys donor-blindness at no cost in cycle up to the middle weight and nothing beyond it: dab7 → dab168 drops donor 0.5837 → 0.5188 with phase flat at 0.7337 → 0.7346; dab336 gains nothing | 7 | 8 | **Yes.** Same panel; it is the shape of the curve, not a separate finding |
| **B3** | **Across the ten methods, donor recovery predicts the disease score (Spearman +0.721, p = 0.019) and does not predict cycle (+0.176, p = 0.627).** An axis whose dominant property is that it reads out donor memorisation is not a performance axis | 7 | **9** | **Yes.** Two small scatters side by side. This is why the disease row left Figure 2, and the asymmetry is the whole point |
| **B4** | **Donor identity is 54× enriched over chance** in the latent: 0.327 of a cell's hundred nearest neighbours share its donor, against a chance rate of 0.0060 over 269 donors | **9** | 8 | No. The number carries itself |
| **B5** | Two arms are reported by name, B$_{hi}$ keeping cycle and B$_{lo}$ removing study harder, and the choice between them is the trade-off made concrete | 8 | 9 | **Yes**, as two marked points on B1's curve |

---

## Type C. What the latent carries — the atlas read

All 1,577,728 cells, model fixed, nothing selected on these labels.

| # | result | sig | imp | figure? |
|---|---|---:|---:|---|
| **C1** | **Cell family 0.9807 and menstrual phase 0.6796 cross-donor, both p = 0.005**, on 630,689 and 723,599 cells | **9** | 8 | **Yes.** The cell-family UMAP, which is Figure 1d. Phase needs no picture |
| **C2** | **Cycle signal is not uniform across cell types**: stromal 1.0677, epithelial 0.9824, endothelial 0.3918, immune 0.3409. The phase head is one linear map that was never given cell type | 7 | 6 | **Yes.** Four small panels or one grouped bar. The ordering is the result and a list of four numbers reads flat |
| **C3** | **Disease status is recoverable: 0.3364, p = 0.005.** From endometrium inside the uterus, the model can tell whether that person has lesions elsewhere | 8 | **10** | No for the number. **Yes** for the UMAP that shows what it looks like |
| **C4** | Disease displacement is **largest in immune cells in Marečková**, 0.7732 and 0.8321 across two arms, highest of four families in both | 7 | 8 | **Yes**, and it now pairs with E2 rather than standing alone |
| **C5** | **It does not replicate in Dümpelmann**, where magnitude is a third and the leading family is not stable across arms | 6 | 7 | Same panel as C4. The non-replication has to be visible, not stated |
| **C6** | **Surgical stage splits between the two reads**: whole-corpus +0.3320 at p = 0.005 on 58 donors, held-out +0.1313 at p = 0.3035 on 16. Grade is **negative in all six arms**, −0.0723 to −0.0227 | 6 | 7 | **Yes.** The pinned dissociation panel, still unplaced |
| **C7** | **Merged severity clears its null**, and it is measured twice: 0.2655 at p = 0.005 (`validation.csv`, 631,090 cells) and 0.1286 at p = 0.025 (benchmark). **Mild against severe among patients only does not**: 0.0744, p = 0.129, 57 donors | 7 | 8 | No. But the dissociation needs stating in one line |
| **C8** | **Negative controls behave**: mitochondrial fraction 0.3396, total counts 0.2514, doublet score 0.1366, against serum progesterone 0.4725 and pseudotime 0.5801 | 8 | 6 | No. A table row, probably Extended Data |

⚠ **C7 carries two numbers for the same quantity from two files.** Both are
legitimate reads and AW's ruling keeps both, but the prose must say which
estimator each comes from or a reviewer will read it as an inconsistency.

---

## Type D. What the architecture needs — the ablations

| # | result | sig | imp | figure? |
|---|---|---:|---:|---|
| **D1** | **Removing the phase head costs cycle 0.7346 → 0.4812, but 65.5% of the chance-corrected signal survives.** The head accounts for 34.5%; the architecture carries the rest | 8 | **9** | **Yes.** This is the inductive-bias claim made numeric, and a bar chart of the six arms says it faster than prose |
| **D2** | **Without the head the model starts overfitting immediately**: `val_nb` is best at epoch 0 and worsens monotonically while `train_nb` keeps falling. BASE improves to epoch 4 | 8 | 7 | **Yes.** Two training curves. A number cannot show "from the first epoch onward" |
| **D3** | **Random gene groups cost disease 0.3364 → 0.2698 and family 0.9820 → 0.9606.** Pathway grouping is load-bearing, not decoration | 7 | **9** | **Yes**, same bar chart. This is the single clearest evidence that the inductive bias is doing work |
| **D4** | Removing ECS worsens study mixing by +0.0727 and donor recovery by +0.0332 | 6 | 6 | Same bar chart |
| **D5** | Removing the DNS sentinel costs almost nothing on biology but worsens mixing +0.0205 and disease +0.0251 | 5 | 5 | Same bar chart |
| **D6** | **The sixteen-dimensional latent beats all 44 pathway groups on both labels, 0 of 44 either way**, while every group is 288 numbers wide and therefore eighteen times the latent. Family 0.9864 against a best group of 0.9695; phase 0.8725 against 0.7341 | 8 | 8 | **Yes, in Supplementary.** 44 groups ranked with the latent drawn as a line through them. The point is that the line sits above every bar, and no table makes that visible at a glance |
| **D7** | **The 44 groups are nothing like equal**: cell family 0.3305 to 0.9695, median 0.7748; phase 0.3051 to 0.7341, median 0.5690. Best on both is the complement cascade, worst on both is sensory perception | 7 | 6 | Same figure as D6 |

⚠ **D6 is the positive half of D3 and the two belong together.** D3 scrambles
the grouping and shows biology falls; D6 keeps it and shows the combination
beats every part of itself. One says the structure is load-bearing, the other
says what the load is.

⚠ **D7's ordering is not label-specific.** Family and phase excess correlate
across the 44 at Spearman +0.665, P < 0.0001, with 16 of 44 below both
medians. Part of what it measures is how much signal a group carries at all.
State it once; it does not weaken D6, which is a comparison against the
latent rather than between groups.

---

## Type E. Published claims tested at scale — the new axis

| # | result | sig | imp | figure? |
|---|---|---:|---:|---|
| **E1** | **Composition does not differ between control and eutopic endometrium**, 194 donors, eleven studies, every family p > 0.23. Dümpelmann's claim confirmed at three times their donor count | 8 | **9** | Maybe. Four paired bars. Its real job is to set up E2, and a figure may not be needed for a null |
| **E2** | **Immune cells carry a disease direction that holds on donors it never saw**: AUC 0.708 against a 0.481 shuffled null, p = 0.015, 94 donors. Mixing the families destroys it (0.605, p = 0.155) | 7 | **10** | **Yes.** The per-family AUC bars with the null. The contrast between mixed and immune-only is the result |
| **E3** | **Decoding that direction gives macrophage-led inflammation**, and **four of the top fifteen genes replicate an external cohort's upregulated list at hypergeometric p = 4.0×10⁻⁷**: SERPINB2 72.9×, MMP27 40.9×, LRRC15 25.2×, INHBA 15.3×. **Zero control-side genes replicate.** IL1B is first in Dümpelmann's own classifier's importance ranking | **9** | **10** | **Yes, and it is the figure the paper does not yet have.** Ranked gene shifts with the replicating genes marked, plus the asymmetry between the two ends |
| **E4** | **Four genes have no prior endometriosis report** in the corpus, Open Targets (MONDO_0005133) or PubMed: SIGLEC7, ADAMDEC1, ALPK2, KCNH1 | 5 | 8 | Part of E3's panel, marked differently |
| **E5** | **Neither severity readout recovers the surgical grade.** Composition does not track it (51 donors, all p > 0.16) and nor does the latent (C7). Two independent measurements, one model-based and one not | 5 | 7 | No. Two sentences |
| **E6** | **Huang's claim that disease flattens the menstrual cycle does not hold**, measured two ways: cross-donor agreement at 112 donors (difference −0.065, p = 0.505) and composition-by-phase interaction at 101 donors (F = 0.263, p = 0.76) | 7 | 8 | No, unless the Discussion needs it. The claim is a null and the donor counts are the argument |
| **E7** | Epithelium is **6.6× rarer in lesions**, 14.7% against 2.2%, p < 0.0001 at 151 donors. **Confounded with dissociation loss**, which the source paper names itself | 4 | 4 | No. One sentence with the caveat attached |
| **E8** | **Tissue structure is largely absent from the latent**, which is the decoder conditioning working as designed. A weak residue sits in stromal (AUC 0.623, p = 0.078) and endothelial (0.618, p = 0.095) | 5 | 6 | No |
| **E9** | **Shih's four claims cannot be tested at all** — our copy of that cohort has 11 donors, all with disease, and all four claims are case-against-control. They are the largest effects claimed in any corpus paper, both at p < 10⁻¹⁶ | n/a | 7 | No. It is a limitation and it should be stated plainly |

---

## Type F. Findings about the field's instruments

These are results about how single-cell integration is measured, not about
endometriosis. They are the reason the paper is a case study rather than a
benchmark.

| # | result | sig | imp | figure? |
|---|---|---:|---:|---|
| **F1** | **The disease axis, as the field scores it, is partly a donor-memorisation readout** (B3's ρ = +0.721). A method that remembers donors scores better on disease | 7 | **9** | Shares B3's panel |
| **F2** | **scIB's biological half is saturated on this corpus** (A4). The metric cannot discriminate where the field uses it | 8 | 8 | No |
| **F3** | **Label transfer through the latent is accurate across studies** (0.987 raw, 0.962–0.969 balanced against majority baselines of 0.88 and 0.53) **and fails silently on cell types absent from the reference**: 98.9% of granulosa cells confidently called stromal, with no rejection rule able to catch it — confidence is 1.00 and distance is *closer* than correct calls | 8 | 6 | **Yes, in Supplementary.** The failure is the useful half and it needs the distance distributions to be believable |
| **F4** | **Both gene-disease databases have demonstrable false negatives.** LRRC15 is reported up 25× at p = 3.2×10⁻²⁴ and returns zero PubMed hits; MMP27 is up 41× and absent from Open Targets entirely. Both live only in supplementary tables | 7 | 5 | No. One sentence, and it shapes how the novelty claim is worded |

---

# What this says about the Results section

## The current five subsections do not match this

| current heading | carries | problem |
|---|---|---|
| The ELAJ frontier | A1, B1, B2 | **Does not name the result.** It names the object |
| Reading 1.58M cells as sixteen numbers | C1, B4 | Poetic, not declarative |
| The menstrual cycle through ELAJ | C2 | Names the variable, not the finding |
| Surgical stage and grade | C6, C7 | Names the variable, not the finding |
| What the disease axis measures | B3, F1 | **This one is already right** |
| What the latent needs in order to work | D1–D5 | Close, could be sharper |

**Nothing in the current structure has a home for Type E at all.**

## Where the weight actually sits

Six results score 10 on importance: **A1, A2, B1, C3, E2, E3**. Three of
those six are from the claims axis or depend on it.

**D6 joins A2 as evidence for the one-line story's first half.** A2 is the
external comparison, 1.88M parameters against 100M. D6 is the internal one:
the architecture's own structure beats every piece of itself. Both say that
inductive bias is doing the work that scale does elsewhere, and only one of
them was in this inventory before 16 November.

Three results score 9 on significance: **A1, B1, E3**, plus B4 and C1.

**E3 is the only result scoring 9+ on both and it has no figure and no
subsection.**

## The structural problem

The paper currently proves the model is good (A, B, D) and then shows what
the latent holds (C). The claims axis (E) is a different kind of result:
**it is the atlas being used rather than evaluated.** That is what the
supervisor asked for when he said a disease atlas is a great thing to have
for a disease, and it is the part a biologist reviewer will care about.

**My reading: Results needs a sixth subsection, and E3 needs a figure.**
That pushes on the four-display-item decision, which is why AW flagged a
possible detour.
