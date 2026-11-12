# Experiment tracker

What needs doing, checking, measuring or testing. Opened 11 November 2026 for
the claims axis; it is the place for any experiment, not just those.

**Status**: `todo` · `running` · `done` · `blocked` · `dropped`
**Scripts live in `axw1008/src/scripts/`**, not here: they are model code and
ship with the published repo. Results land in `axw1008/docs/paper/`.
**Nothing here needs a GPU or a retrain.** Every arm's latents are on disk.

| X | what | for | status | cost |
|---|---|---|---|---|
| X1 | kNN label transfer, **four families only** | prerequisite for X7–X9, X14 | **DONE** | CPU, 3 h |
| X2 | Fetch `vocabulary_v1.json` from HPC | prerequisite for X10–X13 | todo | minutes |
| X3 | Cycle agreement split by disease status | H1, H2 | **done, null** | CPU, small |
| X3b | Cycle vs immune composition by disease | H1 | **done, null** | CPU, small |
| X4 | Severity dose-response write-up | D2, H4 | todo, **numbers exist** | writing |
| X5 | Disease displacement by family, read against HECA | M1 | todo, **numbers exist** | writing |
| X6 | Perivascular and mural cells across three studies | D3, T1, T2, S2, M1 | **future work**, AW 12 Nov: finer cell types are out of this paper | — |
| X7 | Progenitor-like epithelium in lesions | G1, T3, H2 | **dropped**: needs finer labels or expression | — |
| X8 | Composition, case vs control | D1, D3 | **done, supports D3** | CPU, small |
| X9 | Composition, lesion vs eutopic | S2 | **done, one hit, confounded** | CPU, small |
| X10 | Metabolic pathway activity, case vs control | S3 vs D1 | blocked on X2 | CPU, medium |
| X11 | Pathway activity, lesion vs eutopic | S1, S4, F2, L1 | blocked on X2 | CPU, medium |
| X12 | Genes distinguishing control from case | D5 inverse, H3 | step A done; **step B queued on HPC** | medium |
| X13 | Reproducible marker signatures across studies | M2 | todo | large |
| X14 | Tissue effect within a transferred label | F1 | **dropped**: circular, tissue is a decoder input |
| X15 | Group embedding analysis | Supplementary | todo, unscoped | unknown |

---

## X1 — kNN label transfer in the latent

**Why.** Only four of eleven keys brought cell annotations, and two carry
almost all of them: Dümpelmann and Marečková supply 640,606 labelled cells
from 118 donors. Six keys brought nothing (Fonseca, Huang, Tan, Shih, Chen,
Sarsenova), which is 782,016 cells and 115 donors with no cell identity.
Almost every composition claim in the literature is therefore a claim about
cell types we have no labels for **in the study that made the claim**.

**Method.** kNN in the 16-dimensional latent from the 118 annotated donors to
the remaining 136. The cross-donor machinery already builds the neighbour
graph, so this is a new readout rather than new infrastructure.

**Decisions needed before it runs.**
- Which vocabulary to transfer. The four-level `cell family` is safe and
  coarse; Marečková's 45 `celltype` values and Dümpelmann's 63
  `AnnotationRefined` are finer but the two do not share a vocabulary.
  **Perivascular and mural cells do not exist as a `cell family` level**, so
  X6 needs the finer one.
- Whether to exclude same-study neighbours. Not excluding risks transferring
  within-study structure; excluding makes the transfer harder and more
  honest.
- What confidence threshold leaves a cell unlabelled.

**Validation, run 12 November on the Mac from `Outputs/cells/p1_dab168_kl1/`.**
k=25, 60,000 cells sampled per study, four-level `cell family`.

| direction | accuracy | balanced | majority baseline |
|---|---:|---:|---:|
| train Marečková → predict Dümpelmann | 0.987 | 0.962 | 0.883 |
| train Dümpelmann → predict Marečková | 0.987 | 0.969 | 0.527 |
| within Dümpelmann, 20 of 60 donors held out | 0.995 | 0.970 | 0.882 |
| within Marečková, 19 of 58 donors held out | 0.997 | 0.996 | 0.640 |

**Crossing the study barrier costs almost nothing at four levels.** The
control that matters is the second row: Dümpelmann is 88% stromal and
Marečková 53%, so a transfer that merely inherited the source prior would
collapse. Balanced accuracy 0.969 against a 0.527 baseline says it does not.
Worst cell in either confusion matrix is immune into Marečková at 0.887.

**Out-of-tissue validation on `li_2025`, the only one available.** Li brought
its own `celltype` column for 45,312 follicular-fluid cells. Trained on
Dümpelmann and Marečková endometrium, predicting Li:

| Li's own label | n | called immune | called stromal |
|---|---:|---:|---:|
| Neutrophils, Macro/Mono, T/NKT, DC, B | 30,207 | **0.997** | 0.003 |
| Li's own "Stromal" | 49 | 0.020 | 0.939 |
| **Granulosa 1–3** | 15,056 | 0.010 | **0.989** |

**Immune transfers across tissue at 0.997.** That is the encouraging half.

⚠ **The granulosa row is the warning and it is the important result.**
Granulosa cells have no counterpart in an endometrial vocabulary, and 98.9%
of them were confidently called stromal. A cell type the reference does not
contain is not flagged, it is absorbed.

**Rejection rules do not fix it.** Median kNN vote is 1.00 for granulosa,
for Li's immune cells and for held-out Marečková alike, so confidence is
useless. Distance is worse than useless: granulosa sits *closer* to the
reference (mean distance to the 25th neighbour 1.773) than Li's correctly
called immune cells do (2.134).

| distance cut | granulosa rejected | Li immune lost | Marečková lost |
|---|---:|---:|---:|
| 1.5 | 79.0% | 99.3% | 34.2% |
| 2.0 | 22.8% | 64.1% | 9.1% |
| 3.0 | 0.3% | 0.8% | 0.4% |

Every threshold discards more correct labels than wrong ones. **The transfer
cannot tell us when it is wrong.**

**Scoping that follows from this.** Assigning families to cells whose types
exist in the endometrial reference is sound. **Composition in tissue with
novel cell types is not**, because unknowns silently inflate whichever
family absorbs them. That lands on exactly the lesion claims: ovary,
peritoneum and myometrium are where the unlabelled ectopic donors are.

**X1 COMPLETED 12 November.** 937,122 cells labelled. Written to
`Outputs/cells/p1_dab168_kl1/cell_family_transferred.csv.gz`.

| | |
|---|---|
| stromal / immune / epithelial / endothelial | 474,116 / 277,730 / 115,889 / 69,387 |
| vote unanimous across all 25 neighbours | 94.3% |
| vote below 0.6 | 0.45% |
| neighbourhoods drawing on more than one donor | 98.8% |
| neighbourhoods drawing on more than one study | 28.8% |

⚠ **`garcia_alonso_2021_b` comes out 99.9% epithelial.** Worth checking what
that deposit actually is before any composition claim uses it.

⚠ **Li's 66.8% immune / 33.1% stromal is the known granulosa failure**, exactly
as the validation predicted. Shih at 78.2% immune is plausible: menstrual
effluent is blood-rich.

## X12 step A at 207 donors: the signal WEAKENS

Transferred labels, every study, `--transferred`:

| family | donors | AUC | null | p | (118-donor, real labels) |
|---|---:|---:|---:|---:|---|
| all mixed | 202 | 0.518 | 0.471 | 0.268 | 0.605, p 0.155 |
| stromal | 175 | 0.492 | 0.480 | 0.445 | 0.592, p 0.175 |
| epithelial | 176 | 0.470 | 0.478 | 0.535 | 0.466, p 0.590 |
| **immune** | 162 | **0.596** | 0.482 | **0.073** | **0.708, p 0.015** |
| endothelial | 134 | 0.595 | 0.478 | 0.103 | 0.682, p 0.050 |

**Immune stays the strongest family at both scales and stays the same sign,
but it does not strengthen with scale, which is what we would want.**

Two explanations and I cannot separate them: transferred labels add noise, or
the nine extra studies are genuinely heterogeneous. Tissue labels do not
explain it -- nearly every donor is labelled endometrium, including Li's
follicular fluid and Shih's menstrual effluent, which are different tissues
wearing the same label.

**What to report**: the 118-donor figure with real labels is the cleaner
measurement and the 207-donor figure is the honest limitation. Neither should
be quoted alone.

## X2 — Fetch the gene-group vocabulary

44 Reactome/GO groups, named, in
`/rds/projects/a/acharjea-multi-omics/Atharva/data/processed/vocabulary_v1.json`.
Not on this machine. Blocks every pathway-level claim and X15.

**Open question that only the file answers**: do the 44 groups reach the
granularity Sarsenova's claims need? AMPK signalling, HIF-1 signalling,
glutathione metabolism, oxidative phosphorylation and glycolysis are five
distinct pathways. If the cut merged them into one metabolic group, S1, S3
and S11 collapse into a coarser claim and the ledger changes.

## X3 — Cycle agreement split by disease status

**Why.** H1 says the disease flattens the cycle rather than shifting a
quantity. Cross-donor cycle agreement is the number the paper already leads
with, so this tests someone else's biology with our own instrument.

**Method.** Cross-donor menstrual-phase agreement computed separately over
control donors and over eutopic donors, with a permutation null for the
difference.

`axw1008/src/scripts/cycle_by_disease.py`

**The held-out restriction was dropped, and AW was right to push on it.** The
rule says phase is a supervised input so measure it held out. Measured:

| | cycle agreement (excess) | donors |
|---|---:|---:|
| held-out donors | 0.6545 | 32 |
| train donors, matched to the same count | 0.6422 | 32 |

Train is not inflated, it is fractionally lower. The phase head is one linear
map from latent position to phase, so it cannot store which donor had which
phase, and the estimator already discards same-donor neighbours. Held out
cost two thirds of the donors for nothing.

**Result, held-out donors (16 per arm):** control excess 0.830, eutopic
0.665, difference **+0.164** in Huang's direction. Permuting which donors are
control, 2000 times, gives a null of 95% [-0.485, +0.475]. **p = 0.72.**
The direction matches and the number means nothing. All-donor run pending.

⚠ **Phase labels come from three keys of eleven**, so both arms are
Dümpelmann and Marečková. Not a general corpus result.

## X3b — cycle against composition, by disease

`axw1008/src/scripts/cycle_composition_by_disease.py`

**Why it is better than X3.** Huang's claim is about cell proportions, not
latent geometry. Cell family, phase and disease all arrived with the data, so
this tests the claim as made, at 101 donors against Huang's 13, and nobody
can attribute it to ELAJ being good or bad. **It uses no model output.**

**REBUILT 12 November on AW's ruling.** The first version standardised within
study and compared the two arms separately, then I read the single-study row
as the trustworthy one. That is the move the project has ruled against: our
power is the pooling, and splitting by study destroys it. AW: *"our power
comes from the scale... I would take the pooled numbers over single study."*

The fix was to pool properly rather than to drop a study. Study goes **in**
the model as a covariate:

    logit(fraction) ~ study + phase + disease + phase:disease

The interaction is Huang's claim as arithmetic. The null permutes disease
across donors within study, keeping each donor's phase and composition
together. 5,000 permutations, 101 donors.

**Result: no interaction. F = 0.263, p = 0.76.** The null's 95th percentile
is 3.06, so the observed value is not close. Huang's claim does not hold at
this scale.

**The main effects are the more interesting half, and they test Dümpelmann
D3 rather than Huang.** Same model, testing disease after study and phase:

| family | control | disease | p, uncorrected |
|---|---:|---:|---:|
| immune | 0.0717 | 0.0272 | 0.063 |
| endothelial | 0.0550 | 0.0289 | 0.049 |
| stromal | 0.6628 | 0.8148 | 0.75 |
| epithelial | 0.2105 | 0.1291 | 0.91 |

⚠ **Four families tested, so neither small p survives correction.** Bonferroni
needs 0.0125. Writing either as a finding would be the thing failure mode 7b
warns about.

**What it does support is D3.** Dümpelmann claims that, stratified by phase,
cell composition barely differs between case and control, with one 1.6-fold
exception in secretory mural cells. At 101 donors we find the same: stromal
and epithelial are flatly null, and the two compartments with any signal at
all do not clear four-way correction. **A 60-donor claim reproduced at 101.**
Mural cells are not one of our four families, so the exception itself is out
of reach and stays future work.

## X4 — Severity dose-response

**Numbers exist.** Merged severity 0.1286, p=0.025 at 118 donors; mild
against severe among patients only 0.0744, p=0.129 at 57. The work is
writing them against Dümpelmann's fivefold DEG gradient, and deciding
whether the whole-corpus surgical-stage number (+0.3320, p=0.005 at 58
donors) comes in with them. That number is currently uncarried and is also
the open question on the pinned dissociation panel.

## X5 — Disease displacement by family, against HECA

**Numbers exist**, in `Outputs/analysis/*/disease_within_family.csv`. Immune
family leads in Marečková at 0.7732 and 0.8321, highest of four families in
both arms; it does not replicate in Dümpelmann and the leading family there
is not even stable across arms.

This is currently filed as audit item C5, a non-replication. Read against
M1, HECA's GWAS-derived prediction of macrophages and decidualised stromal
cells, it becomes a statement about where the signal lives. **The work is
deciding which reading the paper takes**, not computing anything.

## X6 — Perivascular and mural cells

**Why.** Three studies, three designs, three tissues, one cell type, and
none of them could test another. Dümpelmann: the only case-control
composition change is a 1.6× rise in secretory mural cells. Tan: a
perivascular population specific to peritoneal lesions. Sarsenova:
perivascular cells carry the largest metabolic reprogramming.

**Method.** After X1, abundance and latent separation of perivascular and
mural cells across 108 control, 99 eutopic and 58 ectopic donor records.

**Needs the fine vocabulary**, since perivascular is not a `cell family`.

## X7 — Progenitor-like epithelium in lesions

**Why.** García-Alonso claims lesions are less differentiated and enriched
for SOX9+ LGR5+, **inferred from bulk deconvolution with no lesion single
cells**. Tan reports a progenitor-like epithelial subpopulation in 14
people. We hold 58 ectopic donors with single cells, so this is a first
direct test rather than a replication.

**Method.** After X1, epithelial sub-state composition in ectopic against
eutopic tissue. A gene-level check on SOX9, LGR5, WNT7A, KRT17 against PAEP,
SCGB2A2, PIFO, TP73 would make it concrete and needs no transfer at all.

## X8 / X9 — Composition

X8 is case against control (D1, D3); X9 is lesion against eutopic (S2).
Both are per-donor composition over transferred labels with a test across
donors. Informative as a pair: D3 says composition barely moves between
disease states, S2 says it moves between tissues.

## X10 — Metabolic pathway activity, case vs control

**The sharpest disagreement in the ledger.** Dümpelmann found 427 DEGs
between case and control eutopic endometrium in the proliferative phase.
Sarsenova found "virtually no difference" in metabolic pathway activity on
the same contrast, at N=3 vs N=3, on an external dataset.

Both restricted to the proliferative phase, so it is a clean comparison. We
have 108 control and 99 eutopic donor records.

**Scope it to metabolism**, since that is what S3 actually claims. A general
expression difference would not settle it.

## X11 — Pathway activity, lesion vs eutopic

S1 (metabolism in perivascular, stromal, endothelial), S4 (steroid
signalling), F2 (complement and inflammation in endometriomas), L1 (iron and
senescence). All the same machinery on different groups; what is available
depends on X2.

## X12 — Genes distinguishing control from case

**AW's proposal**, and the inverse of D5. A gene set derived from 254 donors
is ours rather than a replication of someone else's eleven.

**The decision to take first.** ELAJ emits 44 gene *groups*, not per-gene
importances. Two routes:

| route | gives | cost |
|---|---|---|
| decoder attribution | genes the model uses, through our own machinery | larger, novel, defensible as a model result |
| differential expression over the corpus | genes that differ, independent of the model | standard, cheap, says nothing about ELAJ |

They answer different questions. The second is not really a result about our
model; the first is, and it is more work.

## X12 step A — where in the latent the disease signal lives

`axw1008/src/scripts/disease_direction.py` and `disease_direction_by_family.py`

**The premise failed and then AW fixed it.** Step A was meant to find the one
direction in the 16-dimensional latent separating control donors from cases,
so step B could push it through the decoder for per-gene weights. Globally
there is no such direction: held-out donor AUC **0.536** against a
shuffled-label null of 0.482, with 28% of shuffles beating it. 207 donor
records, study centred out, donors not cells.

That does not contradict our 0.3364 cross-donor disease number, which is a
**local** measure: a cell's neighbours from other donors can share its label
without any global axis existing.

AW, 12 November: *"We already know that the latent splits by cell-family. We
should check for disease signal within cell family inside the latent."*

**Inside a family the direction appears, and it is immune.** Real labels, so
duempelmann_2026 and marecko_2024 only, 400 donor-level splits:

| family | donors | held-out AUC | null | p |
|---|---:|---:|---:|---:|
| all mixed | 114 | 0.605 | 0.503 | 0.155 |
| stromal | 101 | 0.592 | 0.499 | 0.175 |
| epithelial | 98 | 0.466 | 0.490 | 0.590 |
| **immune** | 94 | **0.708** | 0.481 | **0.015** |
| endothelial | 85 | 0.682 | 0.486 | 0.050 |

**Mixing families destroys the signal.** Pooled across all four it is 0.605
and does not clear its null; inside immune it is 0.708 and does.

⚠ **Four families tested.** Bonferroni puts immune at about 0.06 and
endothelial at 0.20. Immune is the only one worth calling real, and it is
borderline rather than emphatic.

⚠ **Two studies, 118 donors.** The transferred-label run extends this to 207
donor records and is the test that matters. Blocked on X1.

**It converges with four independent claims.** HECA names macrophages from
GWAS (M1). Our own displacement numbers put immune highest in Marecko (X5).
X3b's main effect has immune proportion lower in disease. Dümpelmann's
ligand-receptor changes are macrophage-centred (D1). And endothelial being
second is the vascular thread: Dümpelmann's only composition change is mural
cells, Tan's lesion-specific population is perivascular, Sarsenova's largest
metabolic change is perivascular.

**Step B is unblocked in principle** -- there is a direction to push through
the decoder -- but it should be the immune one, computed on all 207 donors,
not the global one.

## X8 and X9 — composition, on all eleven studies

`axw1008/src/scripts/composition_by_disease.py`, transferred labels, 5,000
permutations, study as a covariate.

**X8, control against eutopic endometrium. Nothing moves.** 194 donors.

| family | control | eutopic | p |
|---|---:|---:|---:|
| immune | 0.1006 | 0.2302 | 0.619 |
| stromal | 0.5226 | 0.5836 | 0.736 |
| epithelial | 0.3308 | 0.1469 | 0.902 |
| endothelial | 0.0460 | 0.0393 | 0.236 |

**This is D3 confirmed at 194 donors across eleven studies.** Dümpelmann
claimed composition barely differs between case and control once phase is
accounted for; at more than three times their donor count, nothing clears.
A clean positive for a published claim, and it is the result that says you
cannot find endometriosis by counting cell types.

**X9, eutopic against ectopic. One large hit, and it is confounded.** 151
donors.

| family | eutopic | ectopic | p |
|---|---:|---:|---:|
| epithelial | 0.1469 | **0.0222** | **<0.0001** |
| immune | 0.2302 | 0.4015 | 0.119 |
| endothelial | 0.0393 | 0.0805 | 0.700 |
| stromal | 0.5836 | 0.4958 | 0.818 |

Epithelium is **6.6 times lower** in lesions. The direction agrees with
Sarsenova S2, which has stromal larger in eutopic tissue and the other
compartments larger in lesions.

⚠ **Sarsenova names the confound herself**: "we observed a small population of
epithelial cells in both EuE and EcE, most likely due to the cell loss during
the tissue dissociation procedure." Lesion tissue is fibrous and epithelium is
fragile, so a lower epithelial fraction may be protocol rather than biology,
and nothing in the corpus separates the two. **Report it as a limitation of
the data.**

⚠ The mesothelial absorption error runs the other way -- it would push
epithelial *up* in lesions -- so it does not explain this and the finding is
conservative with respect to that particular error.

**X7 and X14 dropped.** X7 needs epithelial subtypes finer than our four
families, or measured expression, and has neither. X14 asks whether tissue
separates cells within a family, but tissue is a decoder covariate, so a
positive result would partly be the model returning what it was given. Both
go to future work rather than being forced.

## X13 — Reproducible marker signatures

**Why.** HECA's M2 complaint is that prior atlases lacked *reproducible*
marker signatures. Reproducibility across studies is exactly what no single
cohort can measure and our corpus can.

**Largest and most novel item in the tracker, and unscoped.** Needs a
decision on what a signature is here, and on how reproducibility is scored
across eleven studies with no shared vocabulary.

⚠ The cycle-coverage half of HECA's complaint lands on us: phase labels come
from three keys of eleven. If we quote M2 we are quoting a criticism that
applies to our own corpus. Deliberately, not by accident.

## X14 — Tissue effect within a transferred label

**Why.** F1 says the same cell type differs transcriptionally by tissue
site. That is the citation already standing behind conditioning the decoder
on tissue.

⚠ **Circularity is the whole difficulty.** Tissue is a decoder covariate, so
finding that tissue separates things in our representation is close to
finding what we built in. The test has to ask whether tissue differences
survive *within* a transferred cell label after study is accounted for, and
the framing matters more than the number.

## X15 — Group embedding analysis

AW's own addition, for Supplementary. Unscoped. Blocked on X2 at minimum.
