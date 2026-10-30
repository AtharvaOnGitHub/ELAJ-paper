# Methods — subsection list for review

**Edit this file. Nothing gets written as prose until you have.**

Columns: the heading as it would be set in bold; its character count against
Nature's 40-character limit; what the passage does; where the text comes
from; and a word allocation.

---

## What the guidelines actually say

Three documents, and they do not say the same thing. Recorded here so the
budget below is arguable rather than asserted.

| source | on Methods length | on headings |
|---|---|---|
| **NMI**, *Preparing your material* | **No number.** "written as concisely as possible but should contain all elements necessary to allow interpretation and replication" | — |
| **NMI**, *AIP and formatting* §6 | **No number.** | "subdivided by short, bold headings referring to methods used. We encourage the inclusion of specific subsections; for example Statistics" |
| **Nature**, *Formatting guide* | "**As a guideline, the Methods section does not typically exceed 3,000 words.**" | "short bold headings referring to methods used"; subheadings "may be up to 40 characters (including spaces)" |

So **3,000 is Nature's generic guideline and NMI states no cap of its own.**
Treated below as a target to argue against, not a wall. The allocation comes
to **3,400**, and the four candidates for the missing 400 are named at the
bottom rather than silently absorbed.

### Hard rules, not guidelines

- **Methods cannot contain figures or tables.** The objective's weight table
  moves to Extended Data.
- **Flat headings, not nested.** Nature Methods is a sequence of bold
  headings with no numbering and no sub-levels. The grouping below is for
  your reading only; it is not structure in the document.
- **Use of an LLM must be documented in Methods.** NMI states this
  explicitly. It is a required subsection, not an optional courtesy.
- **Data availability** and **Code availability** are separate mandatory
  statements after the Methods text.
- Methods references are uncapped and numbered continuing from the main
  text. The 50-reference guideline applies to the main text alone — so a
  claim that needs a citation is cheaper here than anywhere else.

---

---

# The 21 subsections

Live tracker. Word counts are read from `sections/04-methods.tex`, not typed.
Retired subsections and the reasoning are at the end under **Retired**.

## The corpus

| # | heading | ch | status | what it does |
|---|---|---|---|---|
| 1 | **Study selection** | 15 | **written**, 390 w | Eleven studies, 1,577,728 cells, 254 donors, six sites. Identifiers to one namespace, sites to UBERON, every cell traced to a donor. Absorbs donor-level splits (70/15/15, the fifteen dual-identifier donors, 17,873 held-out cells sharing a donor with training) and the single-biopsy confound. |
| 2 | **Gene vocabulary** | 15 | **written**, 175 w | 15,496 genes as the Reactome-or-GO annotated set. Annotation rather than variance, and the same partition supplies the groups. |

## Input representation

| # | heading | ch | status | what it does |
|---|---|---|---|---|
| 3 | **Gene tokens** | 11 | **written**, 298 w | Identity embedding plus a count scaled along a direction the gene owns. |
| 4 | **Unmeasured genes and the sentinel** | 33 | **written**, 199 w | Three states not two, and why the third cannot be recovered from a cell without knowing its study. Absorbs the DNS sentinel. |
| 5 | **Pathway gene grouping** | 23 | **written**, 461 w | 44 groups from the annotations; attention cost 240M to 5.72M pairs, no gene discarded. |

## Encoder

| # | heading | ch | status | what it does |
|---|---|---|---|---|
| 6 | **Group encoders** | 14 | **written**, 301 w | What happens inside one pathway, and the order-statistics hypothesis ablation C-4 tests. |
| 7 | **Cell aggregation** | 16 | **written**, 192 w | The second narrowing, and what relates groups read independently. |
| 8 | **Latent space** | 12 | **written**, 95 w | The bottleneck. Width stated, justification deferred to Results because the frontier is a result. |

## Decoder

| # | heading | ch | status | what it does |
|---|---|---|---|---|
| 9 | **Decoder conditioning** | 20 | **written**, 243 w | Study, platform, tissue so the latent need not store them. `d_disease` 0 — every disease result rests on it. |
| 10 | **Reconstruction head** | 19 | **written**, 436 w | Gene queries against a cell context; why not a per-gene output layer, argued in parameters; no per-gene baseline. Absorbs the count likelihood. |

## Training objective

| # | heading | ch | status | what it does |
|---|---|---|---|---|
| 11 | **Adversarial study removal head** | 29 | **written**, 204 w | Gradient reversal. `w_dab` and `lambda_dab` distinguished; the second traces the frontier. |
| 12 | **Elastic cell similarity head** | 28 | **written**, 185 w | The anti-collapse term and which way it pushes. Largest weight in the model at 50. Pairs stay within one study. |
| 13 | **Menstrual-phase head** | 20 | **written**, 244 w | The fourth head, as a design choice with a measured benefit. 512,101 of 1,161,472 cells. Cell type, disease, stage and grade have no head. |
| 14 | **Composite objective** | 19 | **written**, 260 w | The sum, one equation, weights relative to reconstruction. `lambda_dab`'s absence from it. Absorbs the latent information cost. |

## Training procedure

| # | heading | ch | status | what it does |
|---|---|---|---|---|
| 15 | **Optimisation** | 12 | **not written** — **CONTENTS OPEN** | AdamW, 1e-3, batch 256, bf16, cosine over a 20-epoch horizon chosen for shape not length, early stopping at patience 5. Catch-all: must also absorb per-study normalisation, per-study batch construction, the gene-masking policy, and seed 24 / single runs / the 4% band. |

## Evaluation

| # | heading | ch | status | what it does |
|---|---|---|---|---|
| 16 | **Cross-donor agreement** | 21 | **not written** | Why plain kNN recovery fails, then the definition: same-donor neighbours discarded, k=100. Absorbs the permutation null, p-floor argument intact. |
| 17 | **Donor and study recovery** | 24 | **not written** | How much non-biological signal remains in the latent; lower is better, because removing it is what the model is for. The frontier's second axis. |
| 18 | **Whole-corpus embedding** | 22 | **not written** | Why the split stops mattering once the model is fixed; all 1,577,728 cells embedded; phase the exception. Absorbs the cell-type region procedure. |

## Reporting

| # | heading | ch | status | what it does |
|---|---|---|---|---|
| 19 | **Use of large language models** | 31 | **not written** | **Required by NMI**, stated explicitly in their guidelines. |
| 20 | **Data availability** | 17 | **not written** | Mandatory. Accessions for all eleven studies; no new primary data. GSE213216's citation corrected. |
| 21 | **Code availability** | 17 | **not written** | Mandatory. Repository, licence, the tag that produced the reported arm. Absorbs all hyperparameter and compute detail, and the sufficient-statistics rationale. |

**Written: 14 of 21. 3810 words.**
Still in the file and needing removal: six retired headings carrying notes
only, plus the 860-word `[RESULTS] Ablations` block awaiting its move.

## Going to Supplementary

Named here so the Methods above can be read as complete rather than thin:

- **Supplementary Note 1** — effective gene space: the three equations,
  eliminating *d*, and the 49.8M-against-1.11M comparison. NMI permits
  "algorithm description" as a Note.
- **Supplementary Note 2** — the Power Spherical distribution, the
  direction-versus-angle parameterisation, and why no circular ablation
  exists. Thesis 04 §§Power Spherical, Predicting a direction.
- **Supplementary Note 3** — corpus construction in full: inclusion
  criteria, raw-count recovery, doublet removal, cells removed on purpose.
  Thesis 03 §§Choosing which studies to keep, Cleaning what was downloaded.
- **Supplementary Note 4** — bucketing; gene masking; the sizing arithmetic
  (Appendix C), the grouping construction (Appendix D), the tuning campaign
  (Appendix E).
- **Extended Data Table 1** — the objective's five weights.

## Dropped

- Thesis 04 §Why a new architecture → **Introduction**. Motivation.
- Thesis 04 §Conditional variational autoencoders → **Introduction**.
  CVAE background and the Geneformer/scGPT comparison are prior art; only
  "what ELAJ is" survives, as two sentences opening the Methods.
- Thesis 04 §Contrastive cell embedding → **one line** in #16 noting the
  code supports it and no reported arm enables it.
- Thesis 03 §What the corpus contains → **Extended Data figure**.

---

## Three decisions I need from you

1. **Is "ELAJ" allowed in the title?** Nature: titles "do not normally
   include numbers, acronyms, abbreviations or punctuation", ≤75 characters.
   A model-name paper fights that. Worth settling before the title is drafted.
2. **Flat or grouped?** I have proposed flat per the guide. The ten groups
   above are reading aids only. If you want them as real headings, that is a
   deviation worth making deliberately.
3. **Is the 3,400 worth defending?** NMI states no cap. We could submit at
   3,400 and let the editor cut, or trim to 3,100 now. My preference is to
   trim #13 and #31 and hold the rest.

---

---

# Retired

Every row below was in the plan and is no longer a Methods subsection. Kept
so the decision is visible and is not re-proposed.

| was | ruling | reason |
|---|---|---|
| **Bottleneck integrity** | cut | Expected of a CVAE. Nobody asks whether a model leaks to its decoder, and the latent's own metrics — cell-family kNN 0.994 on sixteen dimensions — already carry the evidence. Run 49817807 keeps the record in the code. |
| **Latent information cost** | merged into 14 | A standard VAE term. Only the anneal, the summed-over-dimensions form, and `w_kl_gauss` as knob two survived, as one paragraph. |
| **Count likelihood** | merged into 10 | Same subject as the reconstruction head. |
| **DNS sentinel** | merged into 4 | Same subject. |
| **Donor-level splits**, **The single-biopsy confound** | merged into 1 | Both are corpus facts and read better in sequence there. |
| **Per-study normalisation**, **Batch construction** | to 15 | AW's ruling: training-procedure material is statements belonging inside other passages, not headings. |
| **Seeds and variability** | to 15 | Seed 24, single runs, the measured 4% band. One sentence. |
| **Checkpoint selection** | cut | Already stated in 14 — selection and early stopping read reconstruction alone. The removed study-separation guard is our own history, not a method. |
| **Permutation null** | merged into 16 | No independent existence; it defines what the agreement number is compared against. The p-floor survives whole: 1/(1+permutations) is a function of donor count, so "not significant" at six donors means undetectable, not absent. |
| **Latent geometry** | cut | Discussion, not method. The quantity — centroid distances in units of the groups' own scatter — is one sentence in 17. The sufficient-statistics rationale goes to 21. |
| **Baselines**, **Foundation model protocol** | to Results | They write correctly at the point of use. Stated in advance they read as excuses. What must survive in Results: inductive vs transductive, and supervision declared per method. |
| **Factorial design** | to Results | Results already claims it — "the pre-registered factorial and the curve it traces". |
| **Ablations** | to Results | 860 words written and parked in `04-methods.tex`. Methods keeps one sentence: single-key changes against one base. |
| **Cell-type regions** | merged into 18 | 25 nearest labelled neighbours searched in sixteen dimensions, not the UMAP, because immune cells are not convex. |
| **Statistics** | cut | NMI only "encourages" it, and its content comes from the **Reporting Summary** — a separate mandatory document filed at submission and seen by editors and reviewers, which cutting the subsection does not touch. ML papers routinely report neither multiple-comparison correction nor interval estimates. The two exposures are real but belong on that form: we correct for nothing across family/phase/disease/stage/grade, and we report point estimates with no uncertainty, which is why the donor bootstrap is `OUTSTANDING`'s largest hole. |
| **Compute** | cut | Configuration detail. The parameter count 1,883,986 stays, stated once. |
| **Phase harmonisation** | not written | Proposed and rejected as data cleaning. The mapping lives in `label_harmonisation.py`: nine classes in cycle order, three source columns, `garcia_alonso`'s reversed adjective order, `duempelmann`'s secretory collapse to the middle sub-phase, and three values dropped rather than mapped (two hormone-treated, one pathological). |

## Decisions log — 28–29 October 2026

Taken in review, AW ruling in every case. Rows above carry the same calls
inline; this is the reasoning and the pattern.

### Cut, and the reason is the same for four of them

**Bottleneck integrity (15), the checkpoint guard (24), the baseline
protocol (30, 31), and the earlier framing of donor/study recovery (28) all
failed one test: they pre-empt objections nobody has made.** A paper that
explains why it is *not* guilty of something invites the reader to wonder.
Where real evidence exists it already lives elsewhere — the latent's own
metrics prove the bottleneck holds; Composite objective already states the
selection rule; the baseline protocol reads as fair when stated at the point
of use in Results and as an excuse when stated in advance.

Also cut: **Latent information cost (17)** merged into 16, **Permutation null
(27)** merged into 26, **Latent geometry (29)** as discussion rather than
method, **Compute (37)** as configuration detail, and **phase harmonisation**
— proposed and rejected as data cleaning.

### Hyperparameters

**No table anywhere.** Not Extended Data, not Supplementary. Only the four
objective weights and the two knob values appear, in Composite objective
prose, because the knobs are the frontier's coordinates and the frontier is
the result. Everything else to Code availability. The field standard — scGPT
included — is prose for the design and code for the settings; we were going
further than the venue asks.

No arms table either: label the frontier points with their two knob values
and the figure carries its own legend.

### Display items

NMI caps Extended Data at **ten**, not unlimited — `06-display-items.tex`
said unlimited and has been corrected with the quote inline. Supplementary
is the uncapped tier. Eight main-text slots are the real budget.

### Still open

**Optimisation (23) is a catch-all** — AW's own description: everything too
small for a subsection and too big to fold in. Its contents are unresolved,
and three things currently have nowhere else to go: domain-specific
normalisation (21), per-study batch construction (22, used three times in
written subsections and established nowhere), and the gene-masking policy
(`gene_mask_target` 12,500, which Reconstruction head's last sentence
forward-references into empty space). To be settled last, deliberately.

**Count after these calls: 23 headings**, from 28.
