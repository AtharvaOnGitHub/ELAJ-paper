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
| X12 | Genes distinguishing control from case | D5 inverse, H3 | **done**, one half usable | medium |
| X13 | Reproducible marker signatures across studies | M2 | **done, counters M2** | CPU, 20 min |
| X14 | Tissue effect within a transferred label | F1 | **done**, weak but real | CPU, small |
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
0.665, difference **+0.164** in Huang's direction, null 95% [-0.485, +0.475],
**p = 0.72**. The direction matches and the number means nothing.

**Result, all 112 donors:** control 0.6825, eutopic 0.7474, difference
**-0.0650**, null 95% [-0.180, +0.195], **p = 0.505**.

**The sign flips and the null tightens threefold**, from +-0.48 to +-0.19. So
the held-out estimate was noise, this run had the power the first one lacked,
and the answer is that there is no difference. X3 and X3b now agree.

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
Sarsenova S2, which reports stromal larger in eutopic tissue and the other
compartments larger in lesions.

⚠ **The Sarsenova paper names the confound itself**: "we observed a small population of
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

## X8 reached to severity — a second leg for the rASRM argument

AW, 12 November: can X8 support the severity result? It can, and the two
measurements are independent of each other.

Composition against surgical severity, patients only, low = mild or rASRM
stage 1-2, high = severe or stage 3-4. 51 donors, study as a covariate:

| family | low | high | p |
|---|---:|---:|---:|
| immune | 0.0911 | 0.0314 | 0.209 |
| endothelial | 0.0285 | 0.0281 | 0.162 |
| stromal | 0.7024 | 0.7907 | 0.970 |
| epithelial | 0.1780 | 0.1498 | 0.913 |

**Nothing tracks severity.** Put beside the latent result -- merged severity
clears at 118 donors (0.1286, p = 0.025) while mild against severe among
patients does not (0.0744, p = 0.129 at 57) -- two independent readouts, one
from the representation and one from raw composition, both fail to recover
the surgeon's severity grade among patients at about 55 donors each.

**The argument this supports**: rASRM staging describes where lesions are and
how extensive they look, not what the tissue is doing. It is anatomy, not
biology.

⚠ **Both legs are nulls at ~55 donors**, so neither is decisive alone and the
pairing is the argument rather than either number.

**A hedge was here and AW cut it, correctly.** I had attached Dümpelmann's D2
-- severe disease giving fivefold more DEGs than mild -- as a counterpoint
the paper must carry. AW: *"We are stating a result from a component study
that we haven't even verified on our model. I don't think it applies.
Clawing."* He is right twice over. It is an untested claim, and a count of
differentially expressed genes is not the same quantity as whether a severity
ordering is recoverable, so it does not contradict our result in the first
place. D2 stays in the ledger as an untested claim, not as a caveat on ours.

## X14 — tissue inside one cell family

`axw1008/src/scripts/tissue_within_family.py`. 262 donors, units are
(donor, tissue) pairs, split by donor.

| family | units | AUC | null | p |
|---|---:|---:|---:|---:|
| stromal | 229 | 0.623 | 0.495 | 0.078 |
| endothelial | 175 | 0.618 | 0.494 | 0.095 |
| immune | 215 | 0.562 | 0.502 | 0.240 |
| epithelial | 194 | 0.522 | 0.494 | 0.401 |

**I had the logic backwards and AW corrected it.** I called this circular
because tissue is a decoder covariate. The covariate does the opposite:
conditioning the decoder on tissue removes the latent's *obligation* to
encode it, which is the stated purpose. So tissue structure surviving in the
latent is structure the model had every reason to discard, and a positive
result is evidence rather than an artefact. AW: *"tissue information being
less in the latent is a support to our claim rather than a detriment."*

**Read that way the result is good for the paper in both halves.** Most
tissue structure is gone, which is the covariate working as designed. What
remains sits in stromal and endothelial cells, weakly, at p = 0.08 and 0.10,
which is the Fonseca F1 direction.

⚠ Tissue is near-perfectly confounded with disease status: ovary and
peritoneum are almost all ectopic donors. So this is the latent-level
companion to X9 rather than an independent axis, and neither family clears
0.05.

## X12 step B — the immune disease direction, in genes

Ran on the HPC 12 November, `decode_dx_61604807`. 4,000 immune cells against
15,496 genes, direction from 94 donors. **Step-size check passed: rank
correlation 0.9973 between eps 0.5 and 1.0**, so the attribution is locally
stable and not an artefact of how far the latent was nudged.

**The case end is coherent and interpretable.** Top genes moving toward case:

    CCL3, CCL13     macrophage chemokines
    ITGAX (CD11c)   myeloid and dendritic
    SIGLEC7         NK and myeloid receptor
    TNFRSF17 (BCMA) plasma cells
    MMP3, MMP27, LRRC15   matrix remodelling

That is an inflammatory, myeloid-weighted immune profile, and it is the
direction Dümpelmann D1 describes from a completely different method:
macrophage-centred ligand-receptor changes, inflammation enriched.

**TNFRSF17 is worth noting and not over-reading.** It is a plasma-cell gene,
and Shih Sh4 claims B cells are enriched in cases -- a claim we cannot test,
because our copy of that cohort has no controls. One gene on a ranked list is
not a test of it, but the directions agree.

⚠ **The control end is contaminated and must not be read as biology.** It is
topped by epithelial identity genes: WNT7A, LGR5, SOX17, MSLN, TFF3, VTCN1.
Measured: the immune disease direction has cosine **+0.21** with the
immune-to-epithelial axis in the latent. That is modest -- the two family
axes themselves sit at +0.62 -- but epithelial identity genes have the
steepest decoder response of anything in the vocabulary, so a small component
along that axis is enough to put them on top. **Report the case end only.**

**HECA's genes, and I set the test up wrongly.** I checked four genes in
immune cells. Only ONE of them is a macrophage claim: HECA reports GREB1 up,
DKK1 down and IGF2 down in *decidualised stromal* cells, and IGF1 up in *both*
dStromal and uM2 macrophages.

| gene | HECA's compartment | agrees? |
|---|---|---|
| **IGF1** | **macrophage (uM2) and stromal** | **yes, up in case, percentile 0.040** |
| GREB1 | stromal only | shift 0.000, untestable here |
| DKK1 | stromal only | wrong compartment, do not score |
| IGF2 | stromal only | wrong compartment, do not score |

So the one HECA gene that is genuinely a macrophage claim agrees with our
immune direction. The other three were never ours to test in this compartment,
and re-testing them properly would need a stromal direction -- which step A
says does not generalise (AUC 0.592, p 0.175), so there is nothing to push
through. **That goes in limitations.**

Outputs: `axw1008/docs/paper/x12_gene_shifts.csv` on the HPC.

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

`axw1008/src/scripts/probe_stages.py`, run as `probe_stages.sh
p1_dab168_kl1 --runs-dir outputs/p_series --splits val test --only-groups
--no-references`. Job 61861150, 16 November 2026, 13:26:46 on one A100,
exit 0. Output `Outputs/probes/p1_groups/stages.csv`.

**Why.** AW's own addition. The model's one structural commitment is that a
cell is read as 44 pathway groups rather than as 15,496 independent genes.
D3 already shows that scrambling that grouping costs biology. X15 asks the
other half: what does each group carry on its own, and does the
sixteen-number latent hold more than the best of them?

**What was measured.** Each group hands forward 288 numbers, one learned
summary token plus eight pooled order statistics over 32 dimensions. Those
288 numbers were scored with the benchmark's own $k$NN estimator on the
benchmark's own held-out cells: cell family over 176,803 cells, 4 labels,
chance 0.673; menstrual phase over 224,211 cells, 7 labels, chance 0.370.
Every value below is excess over chance, as everywhere else in the paper.

**The integrity row is exact.** The same run scores the full
sixteen-dimensional latent through the same code path, and all six axes
match Table 1's ELAJ B_hi row to the last digit: cycle 0.7346, cross-donor
family 0.9820, donor recovery 0.5188, kNN family 0.9864, disease 0.3364,
study mixing 0.7613. The per-group numbers are therefore on the same cells
and the same estimator as the paper's headline table.

**Result 1. The latent beats every group, on both labels.**

| | cell family | menstrual phase |
|---|---:|---:|
| the 16-dimensional latent | **0.9864** | **0.8725** |
| best single group, 288 numbers | 0.9695 | 0.7341 |
| **groups beating the latent** | **0 of 44** | **0 of 44** |

Each group is eighteen times wider than the latent, so the comparison runs
against us and the latent wins anyway. Whatever the latent is, it is not a
copy of its best-informed group.

**Result 2. The groups are not interchangeable.**

| | min | median | max |
|---|---:|---:|---:|
| cell family | 0.3305 | 0.7748 | 0.9695 |
| menstrual phase | 0.3051 | 0.5690 | 0.7341 |

Best on both is `reactome_complement_cascade_plus_9_more`. Worst on both is
`reactome_sensory_perception`, which names a function the endometrium does
not perform, and reads accordingly. A probe that scored every group alike
would be measuring nothing; this one does not.

⚠ **The ordering is not label-specific.** Family and phase excess correlate
across the 44 groups at Spearman $+0.665$, $P < 0.0001$, and 16 of the 44
sit below both medians. So part of what this reads is how much
transcriptional signal a group carries at all, rather than anything
specific to either label. Any claim that a particular pathway carries the
cycle has to clear that correlation first.

### Going past the scalars, 17 November

AW: *"These are still in the realm of statistical interpretation of results.
We can go a few levels deeper than this."* He was right. What follows uses
the underlying objects rather than the 88 per-group numbers, and needs no
new compute: `D5_pathway_groups_and_genes.csv` (gene to group),
`x12_gene_shifts_orth.csv` (the decoder's per-gene response along the immune
disease direction, all 15,496) and the dumped latent.

**Result 3. The cycle is ONE axis in the latent; cell identity is THREE.**
Linear discriminant analysis on the sixteen dimensions, 150,000 cells:

| label | share of between-class separation per discriminant |
|---|---|
| menstrual phase | **0.601**, 0.196, 0.108, 0.069, 0.023, 0.004 |
| cell family | 0.434, 0.312, 0.254 |

Phase puts 60% of its separation on a single direction and 80% on two. Cell
family spreads evenly over three. **The model encodes the cycle as a
gradient and cell identity as territories**, which is what the UMAPs show
and what Results already says about families being contiguous regions, now
as a measured decomposition rather than a reading of a picture.

**This is why no group recovers the cycle alone.** A single axis assembled
as a weighted combination across 44 groups is not present in any one of
them; three balanced axes of cell identity are visible from almost any
pathway, which is why 17 of 44 groups reach 80% of the latent on family and
2 of 44 do on phase.

**Result 4. The disease direction rides on the identity machinery, not on
the cycle machinery.** For each group, take the root-mean-square response of
its genes along X12's immune disease direction, and correlate that with what
the group carries:

| | Spearman | permutation $P$ |
|---|---:|---:|
| group's **cell family** score vs its disease loading | **$+0.519$** | **0.0005** |
| group's **menstrual phase** score vs its disease loading | $+0.262$ | 0.090 |
| group's **gene count** vs its disease loading | $-0.232$ | 0.13 |

**And the partial correlations settle which of the two it is.** Holding
phase constant, family against disease loading is $+0.501$, $P = 0.0005$.
Holding family constant, phase against disease loading is $-0.118$,
$P = 0.44$: it vanishes. The null reshuffles gene-to-group assignment while
keeping every group's size, 2,000 times, and centres on zero with
sd 0.155, so the observed $+0.519$ is 3.3 standard deviations out.

**What that means.** The pathway groups that tell you what kind of cell you
are looking at are the same groups the disease signal is written in. The
groups that track where the tissue is in its cycle are not. Disease and
cycle are carried by different parts of the architecture, which is the
mechanism behind their behaving as separate axes everywhere else in the
paper: it is why the frontier trades the cycle against donor-blindness
while the disease readout follows donor memorisation instead (B3,
$\rho = +0.721$).

⚠ **One thing was tried and gives nothing; do not re-run it.** The direct
geometry, the angle between X12's disease direction and each label's leading
discriminant axis, sits inside the random-direction null on every label
(phase $|\cos| = 0.312$, 78th percentile; family 0.194, 55th; disease\_status
0.153, 44th). The comparator is also confounded, because the whole-corpus
`disease_status` discriminant is dominated by ectopic against eutopic, which
is tissue, and tissue is a decoder covariate. The gene-level route above is
the one that works.

⚠ **No counts baseline exists.** `--no-references` skipped the two per-group
PCA reference families, which are two thirds of the job's cost and what
fill `counts_raw`, `counts_log` and every `delta` column. X15 therefore says
what each group carries and says nothing about what the tokenisation costs
against raw counts. Running them is a separate decision.
