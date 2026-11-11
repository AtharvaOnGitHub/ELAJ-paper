# The claims axis — step 1, claims laid out by paper

Opened 11 November 2026, on AW's ruling:

> "We need to lay out all the major claims of each dataset and see if we can
> support or reject them in our architecture. That is a results axis we
> hadn't considered yet."

**Every dataset is accounted for even where its claims go untested.** AW's
condition, and the reason this file lists studies that will contribute
nothing testable.

**This file is step 1 only.** Step 2 is picking what is most relevant, and
that is a decision taken with AW. Step 3 is scripts and inferences. Nothing
here proposes a test as chosen.

## Where each claim comes from

Most of the extraction already existed. `Thesis/literature-evidence.md` is
AW's own verified pass over the corpus papers, with ❝ marking quotations
checked against the PDF. Claims carried over from there are marked
**verified**. Anything I could not source from a verified extraction is
marked **unread** and must not be written into the paper until someone has
opened the paper. The rule from CONTINUITY applies: check the paper, not the
summary of the paper.

---

## What the corpus can actually carry

This table decides more than the claims do, and it was the surprise of the
exercise.

| study key | published as | cells | donors | tissue | disease status (donors) | labels it brought |
|---|---|---:|---:|---|---|---|
| `duempelmann_2026` | Dümpelmann 2026 | 466,176 | 60 | endometrium | 25 control, 35 eutopic | **cell type, phase, grade** |
| `fonseca_2023` | Fonseca 2023 | 386,560 | 48 | ovary, peritoneum, endometrium, rectum, bladder | 4 control, 35 ectopic, 9 eutopic | none |
| `marecko_2024` | Marečková 2024 | 174,848 | 58 | endometrium | 36 control, 22 eutopic | **cell type, lineage, phase, stage** |
| `lin_2023` | Huang 2023 | 140,032 | 13 | endometrium | 7 control, 6 eutopic | none |
| `tan_2022` | Tan 2022 | 114,944 | 31 | endometrium, ovary, peritoneum | 3 control, 19 ectopic, 9 eutopic | none |
| `garcia_alonso_2021_a` | García-Alonso 2021, whole | 100,096 | 15 | endometrium | 15 control | stage, phase |
| `shih_2022` | Shih 2022 | 74,496 | 11 | endometrium | 11 eutopic | none |
| `wang_2022` | Chen 2022 | 49,152 | 4 | myometrium | 4 adenomyosis | none |
| `li_2025` | Li 2025 | 45,312 | 6 | endometrium (**mislabelled**, see Methods) | 3 control, 3 eutopic | cell type |
| `ferrero_2024` | Sarsenova 2024 | 15,872 | 8 | endometrium, peritoneum | 4 ectopic, 4 eutopic | none |
| `garcia_alonso_2021_b` | García-Alonso 2021, epithelial | 10,240 | 15 | endometrium | 15 control | stage, phase |

### Three constraints fall out of it, and they shape everything downstream

**1. Only four of eleven keys brought any cell annotation, and two of those
carry the corpus.** Dümpelmann and Marečková supply 640,606 labelled cells
from 118 donors; `li_2025` adds 45,312 in a vocabulary of its own; the
García-Alonso pair brought cycle stage but no cell labels. **Six keys
brought nothing**: Fonseca, Huang, Tan, Shih, Chen and Sarsenova, which is
782,016 cells and 115 donors with no cell identity attached.

So almost every composition claim in the literature is a claim about cell
types we do not have labels for in the study that made it. **Testing them
means transferring labels through the latent first.** That is not a
workaround. It is the atlas doing the job an atlas exists to do, and it is
the most defensible framing of this whole axis.

**2. Shih's cohort arrives without its controls.** The paper compares 11
confirmed cases against 9 controls and 13 symptomatic undiagnosed subjects.
The corpus has **11 donors, all eutopic**. Its headline claim is a
case-versus-control contrast and the control arm is not here, so it cannot
be tested within its own study. Testing it against controls from other
studies is a cross-study contrast, which is a different and weaker thing.

**3. Phase and severity are even thinner than cell type.** Phase labels come
from three keys, severity from two. Any claim conditioned on cycle phase is
testable on Dümpelmann, Marečková and García-Alonso, and nowhere else,
unless the phase head's predictions are used as the label.

### Two prerequisites before any of this runs

- **The 44 gene-group names are not on this machine.** They live in
  `vocabulary_v1.json` on the HPC at
  `/rds/projects/a/acharjea-multi-omics/Atharva/data/processed/`. Every
  pathway-level claim needs them, and so does AW's group-embedding
  supplementary item. Small fetch, but it blocks both.
- **Label transfer does not exist yet.** Nothing in `Outputs/` moves
  annotations from the 118 labelled donors to the other 136. It is kNN in
  the sixteen-dimensional latent and the cross-donor machinery already
  computes the neighbour graph, so this is CPU work on latents we have, not
  a retrain.

**Nothing in this axis needs a GPU or a retraining run.** The latents for
every arm are already on disk. That is worth saying up front, because "HPC
work" here means CPU scoring jobs, not another eleven-hour training.

---

# The claims, by paper

## Dümpelmann 2026 — `duempelmann_2026`

The largest study in the corpus, the best annotated, and the closest prior
work to ours.

| # | claim | status | how it would be tested |
|---|---|---|---|
| D1 | The eutopic endometrium of cases differs from controls: increased inflammation, adhesion, proliferation, cell survival, angiogenesis | verified | **direct**. 25 control against 35 eutopic donors, its own labels, then repeated across the corpus's 85 control and 136 eutopic donors |
| D2 | Neural networks predict disease severity at median **AUC 0.83**, one model on **11 genes** | verified | **expression**. The 11-gene model is the sharpest test in the ledger: does their signature hold at 254 donors |
| D3 | The largest bulk studies at n>200, phase-stratified, found **no significant** case-control expression difference | verified | not ours to test. It is the argument for resolution over sample size and belongs in the Introduction |
| D4 | Prior single-cell work was limited by small eutopic samples, cell-type exclusion, hormone treatment, and ignoring cycle phase | verified quote | not a testable claim. It is the field's own statement of the gap |

**D2 is the one to look at hardest.** It is the closest prior result to ours
and the distinction has to be made explicitly or a reviewer asks why we did
not simply do that: supervised prediction of a label the model was given,
against unsupervised representation validated on a label the model never
saw. Testing their 11-gene signature across 254 donors answers the question
on their terms rather than ours.

## Marečková 2024 (HECA) — `marecko_2024`

The field's own reference atlas and the thing we are most directly compared
to.

| # | claim | status | how it would be tested |
|---|---|---|---|
| M1 | Previous atlases "profiled few donors and lacked consensus in defining cell types" | verified quote | not testable. It is the sentence that licenses the paper |
| M2 | Prior censuses "lacked even coverage of the menstrual cycle phases, consensus cell state annotation and reproducible marker gene signatures" | verified quote | **partly direct**. Cycle coverage across our corpus is measurable and is a fact about our own data |
| M3 | Small studies reported stromal and immune dysregulation "to various degrees" | verified quote | **transfer**. The disagreement across studies is the thing pooling addresses, and it is measurable once labels are transferred |
| M4 | HECA integrates 7 datasets, 313,527 cells, 63 donors | verified | the comparator for scale. 11 datasets, 1.58M cells, 254 donors |

**M2 is a trap worth naming now.** HECA names uneven cycle coverage as a
deficiency, and our corpus has it too: phase labels on three keys of eleven.
If we quote M2 we are quoting a criticism that lands on us. That is fine and
it is honest, but it has to be stated deliberately rather than discovered.

## Fonseca 2023 — `fonseca_2023`

The second largest study, the broadest tissue coverage, and no cell labels.

| # | claim | status | how it would be tested |
|---|---|---|---|
| F1 | "Cellular and molecular signatures of endometrial-type epithelium and stroma differed across tissue types" | verified quote | **transfer**. It is also the citation behind conditioning the decoder on tissue |
| F2 | Cellular restructuring and transcriptional reprogramming distinguish lesion from endometrium | verified | **transfer plus expression** |
| F3 | Composition across 370,000 cells: T cells 27%, epithelial 10%, myeloid 7.3%, endothelial 6.2%, smooth muscle 4.9%, B and plasma 2.2%, mast 0.4% | verified | **transfer**. A composition claim we can reproduce or contradict once labels move, on their own 48 donors |

**F1 is the one with a second job.** It is already cited in Methods as the
justification for tissue conditioning, so confirming it on the pooled corpus
closes a loop the paper has already opened.

## Tan 2022 — `tan_2022`

| # | claim | status | how it would be tested |
|---|---|---|---|
| T1 | Eutopic endometrium is heterogeneous **between individuals**, independently of hormone treatment | verified | **direct, and it is the most interesting claim in the ledger**. Between-individual heterogeneity is exactly what donor recovery measures. We have a number for this at 254 donors |
| T2 | Lesions differ from matched eutopic endometrium within the same person | verified | **transfer**. 19 ectopic and 9 eutopic donors, some matched |
| T3 | Diagnostic delay up to 7 years; diagnosis requires surgical biopsy | verified quote | Introduction material, not a test |

**T1 deserves attention out of proportion to its size.** Tan claims
between-individual heterogeneity in eutopic endometrium from 14 individuals.
Donor recovery is a direct measurement of exactly that quantity, and we
report it on 254. This is the cleanest case in the ledger of a small-cohort
claim that our corpus can put a number on.

## Sarsenova 2024 — `ferrero_2024`

The smallest endometriosis study and the most useful disagreement.

| # | claim | status | how it would be tested |
|---|---|---|---|
| S1 | Metabolic differences between ectopic and eutopic concentrate in perivascular, stromal and endothelial cells | verified | **transfer plus group embeddings** |
| S2 | Largest changes in AMPK signalling, HIF-1 signalling, glutathione metabolism, oxidative phosphorylation, glycolysis | verified | **gene groups**. These are pathway-level claims and the model's 44 Reactome/GO groups are pathway-level objects. Needs the vocabulary fetch first |
| S3 | Eutopic endometrium of cases against controls, **N=3 vs N=3**, gave few differentially expressed genes: no major metabolic difference | verified | **direct**, and it is the headline disagreement |

**S3 against D1 is the single best illustration in the project of why
pooling is needed**, and AW's extraction already says so: two studies,
opposite conclusions, and the difference is statistical power. Sarsenova
finds nothing at N=3 versus N=3 where Dümpelmann finds a great deal at 25
versus 35. We have 85 control and 136 eutopic donors. **Whichever way that
test comes out, it is a result**, which is a rare property.

**S2 is the claim that ties AW's group-embedding item to this axis.** If the
44 groups include metabolic pathways at this granularity, Sarsenova's
pathway claims are testable in the model's own representation rather than in
gene space. Cannot be confirmed until the vocabulary is on disk.

## Shih 2022 — `shih_2022`

| # | claim | status | how it would be tested |
|---|---|---|---|
| Sh1 | Proliferating uterine NK subcluster present in controls, almost absent in cases; total uNK reduced at **p < 10⁻¹⁶** | verified | **blocked within its own study.** Its controls are not in our corpus. Cross-study only |
| Sh2 | IGFBP1+ decidualised stromal cells abundant in controls relative to cases, **p < 10⁻¹⁶** | verified | same block, same options |
| Sh3 | Disease signal is recoverable from **menstrual effluent**, no surgery | verified | not a test. It is the clinical hook and belongs in the Introduction |
| Sh4 | Cohort is 91% Caucasian | verified | a limitation, and support for pooling across cohorts |

**Shih is the clearest case of "accounted for but not tested".** Two claims
with enormous p-values, and we hold only the case arm. Worth stating in the
ledger rather than quietly skipping, because the reason is a property of the
corpus and not of the claims.

## Huang 2023 — `lin_2023`

| # | claim | status | how it would be tested |
|---|---|---|---|
| H1 | Fewer state-2 secretory-phase epithelial cells in the endometriosis group | verified | **transfer plus phase**. Needs both a transferred epithelial label and a phase call, and this study brought neither. 7 control against 6 eutopic donors |
| H2 | Findings are specific to **minimal/mild disease**, rASRM stage I–II | verified | severity labels come from two other studies, so this is cross-study |
| H3 | The authors name small sample size and absent validation as limitations | verified quote | one of three such admissions in the corpus. A pattern, and it is Introduction material |

**H1 is the most demanding test in the ledger** and the one most likely to
be dropped at step 2. It needs two transferred labels at once in a study
that supplied neither, on thirteen donors.

## Chen 2022 — `wang_2022`

The adenomyosis study, four donors, myometrium, and the only paper in the
corpus that reaches pain.

| # | claim | status | how it would be tested |
|---|---|---|---|
| C1 | SFRP4+ IGFBP5-high NKT cells in the pain group | verified | **blocked**. Pain is not a covariate anywhere in the corpus |
| C2 | NEFM expression correlates with pain **duration**; IGFBP5 with pain **score** | verified | **blocked**, same reason |
| C3 | Adenomyosis is a contrasting related disease | verified | **direct**. 49,152 cells and 4 donors of adenomyosis is why the corpus has a fourth disease status |

**Chen is accounted for and contributes no testable claim.** Its sequencing
is n=2 per group, its tissue is the only myometrium in the corpus, and its
variable of interest is pain, which we never collected. C3 is the reason it
is in the corpus at all.

## Li 2025 — `li_2025`

| # | claim | status | how it would be tested |
|---|---|---|---|
| L1 | Ovarian endometriosis is associated with fewer antral follicles, fewer mature oocytes, fewer high-quality embryos, in a propensity-matched IVF cohort of 4,087 | verified | **out of scope**. A clinical outcome claim with no single-cell object in our corpus |
| L2 | Iron overload, senescence and metabolic reprogramming in pre-ovulatory follicular fluid | verified | **expression plus gene groups**, on 6 donors |
| L3 | The disease affects tissue that contains no lesions | verified | the reason for multi-site profiling, and it is already a Methods argument |

⚠ **Li is the study whose tissue label is wrong in the data.** Follicular
fluid recorded as endometrium, corrected in the paper only, because tissue is
a decoder covariate and relabelling means retraining. Any test touching
`li_2025` has to handle that explicitly or it is comparing follicular fluid
to endometrium while calling both endometrium.

## García-Alonso 2021 — `garcia_alonso_2021_a` and `_b`

Two CELLxGENE deposits from one Nature Genetics paper, the whole-tissue and
epithelial collections. A third, the organoid deposit, was excluded from the
corpus (`garcia_alonso_2021_c` in `exclude_studies`). All control tissue:
30 donor records for 15 people, which is the duplication behind 269 against
254.

| # | claim | status | how it would be tested |
|---|---|---|---|
| G1 | — | **unread** | — |

**This is the one gap in the ledger and it is mine to close.** There is no
verified extraction for García-Alonso anywhere in the thesis or the paper;
`literature-evidence.md` covers nine studies and this is not one of them, and
the PDF is not in `Atharva Papers`. Its claims concern healthy endometrial
dynamics across the cycle rather than endometriosis, which is probably why it
was never extracted: it entered the corpus as reference tissue, not as a
finding.

**I will not write its claims from memory.** It needs the paper on disk and
one extraction pass, the same as the other nine got.

It matters more than its cell count suggests, because it is 30 of our control
donor records and it carries cycle stage, which only two other studies do.

---

# What this leaves for step 2

**The claims sort into four kinds**, and the sorting is more useful than the
count:

| kind | claims | what it needs |
|---|---|---|
| **testable now, no new machinery** | T1, S3, D1, C3, M2 | existing latents and metadata |
| **testable after label transfer** | F1, F2, F3, M3, T2, S1, H1 | kNN transfer from 118 annotated donors |
| **testable at gene or pathway level** | D2, S2, L2 | the vocabulary fetch, then expression work |
| **accounted for, not testable** | Sh1, Sh2, C1, C2, L1, D3, D4, M1, Sh3, Sh4, H2, H3, L3, T3 | nothing. They are Introduction and Discussion material |

**The strongest four, on my reading, and this is a recommendation not a
decision:**

1. **S3 against D1.** Opposite published conclusions, resolved by donor
   count, and either outcome is a result.
2. **T1.** A between-individual heterogeneity claim from 14 people, against
   a donor-recovery number measured on 254. It needs no new machinery.
3. **D2.** The closest prior work, tested on its own terms.
4. **F3.** A composition claim with published percentages, reproducible on
   the same 48 donors once labels transfer.

**The one that would change the paper most is label transfer itself**, since
seven claims depend on it and it is the atlas performing its defining
function. If step 2 keeps any of those seven, transfer is the first script.
