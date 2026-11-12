# Experiment tracker

What needs doing, checking, measuring or testing. Opened 11 November 2026 for
the claims axis; it is the place for any experiment, not just those.

**Status**: `todo` · `running` · `done` · `blocked` · `dropped`
**Nothing here needs a GPU or a retrain.** Every arm's latents are on disk.

| X | what | for | status | cost |
|---|---|---|---|---|
| X1 | kNN label transfer in the latent | prerequisite for X6–X9, X14 | todo | CPU, hours |
| X2 | Fetch `vocabulary_v1.json` from HPC | prerequisite for X10–X13 | todo | minutes |
| X3 | Cycle agreement split by disease status | H1, H2 | todo | CPU, small |
| X4 | Severity dose-response write-up | D2, H4 | todo, **numbers exist** | writing |
| X5 | Disease displacement by family, read against HECA | M1 | todo, **numbers exist** | writing |
| X6 | Perivascular and mural cells across three studies | D3, T1, T2, S2, M1 | blocked on X1 | CPU, small |
| X7 | Progenitor-like epithelium in lesions | G1, T3, H2 | blocked on X1 | CPU, small |
| X8 | Composition, case vs control | D1, D3 | blocked on X1 | CPU, small |
| X9 | Composition, lesion vs eutopic | S2 | blocked on X1 | CPU, small |
| X10 | Metabolic pathway activity, case vs control | S3 vs D1 | blocked on X2 | CPU, medium |
| X11 | Pathway activity, lesion vs eutopic | S1, S4, F2, L1 | blocked on X2 | CPU, medium |
| X12 | Genes distinguishing control from case | D5 inverse, H3 | todo, **needs a decision** | medium–large |
| X13 | Reproducible marker signatures across studies | M2 | todo | large |
| X14 | Tissue effect within a transferred label | F1 | blocked on X1 | CPU, small |
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

⚠ **What this does not show.** Both studies are endometrium on droplet
capture and both are the best annotated in the corpus. The six unlabelled
studies include peritoneum, ovary, myometrium and follicular fluid, and
**there are no labels there to validate against**. That risk cannot be
measured away.

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

⚠ **Two cautions.** Phase is a supervised head, so the model was given this
label; the comparison is of agreement between disease groups, not of the
label's recoverability. And phase labels come from three keys of eleven, so
the control and eutopic sets will be dominated by Dümpelmann and
Marečková. Check the donor counts on both sides before reading anything
into the result.

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
