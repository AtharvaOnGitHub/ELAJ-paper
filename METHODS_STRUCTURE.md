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

**SETTLED 30 October 2026.** NMI's Content Types page gives the Article's
main-text limit as "up to 3,500 words, **excluding abstract, Methods,**
references and figure legends". So Methods is outside the word count
altogether: there is no NMI cap on it, and Nature's 3,000 is advisory for a
section NMI does not count. The allocation below stands as a discipline
rather than a limit.

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

**Notes live in `METHODS_NOTES.md`, not in the manuscript.** A subsection's
`\note{}` block stays inline while it is unwritten, where it serves as the
brief; once seeded, the note moves to that file in the same commit. So the
`.tex` reads as prose and the scaffolding is still one file away.

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

Empty by ruling — see **Retired**. Per-study normalisation, batch
construction and the seed/variability disclosure all fold into Optimisation,
which now sits after the evaluation run rather than before it, because it is
procedure rather than measurement.

| # | heading | ch | status | what it does |
|---|---|---|---|---|
| 18 | **Optimisation** | 12 | **not written** — **CONTENTS OPEN** | AdamW, 1e-3, batch 256, bf16, cosine over a 20-epoch horizon chosen for shape not length, early stopping at patience 5. Catch-all: must also absorb per-study normalisation, per-study batch construction, the gene-masking policy, and seed 24 / single runs / the 4% band. |

## Evaluation

| # | heading | ch | status | what it does |
|---|---|---|---|---|
| 15 | **Cross-donor agreement** | 21 | **not written** | Why plain kNN recovery fails, then the definition: same-donor neighbours discarded, k=100. Absorbs the permutation null, p-floor argument intact. |
| 16 | **Donor and study recovery** | 24 | **not written** | How much non-biological signal remains in the latent; lower is better, because removing it is what the model is for. The frontier's second axis. |
| 17 | **Whole-corpus embedding** | 22 | **not written** | Why the split stops mattering once the model is fixed; all 1,577,728 cells embedded; phase the exception. Absorbs the cell-type region procedure. |

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

---

# What is left to write, and the argument each passage has to make

Rounded up 7 November 2026, after Results and the Discussion closed. Every
fact below was re-derived from the configs, the run records and the
benchmark files rather than taken from the notes, and three of them
contradict what the notes said.

Methods sits outside NMI's 3,500-word count, so length here is a discipline
and not a limit.

---

## 1. Donor and study recovery — 0 words

**The one argument that has to land:** these are the axes a good model
should *fail* at. Without that sentence a reader meets a column of low
numbers and reads it as poor performance.

- **Donor recovery** is $k$NN agreement on `patient_id` at $k=30$ over all
  416,256 held-out cells. No label is needed, since every cell has a donor,
  which is why this axis covers the whole split while the biology axes do
  not.
- **Study separation** is $k$NN study purity, rescaled so that 0 is
  perfectly mixed and 1 fully separated. The rescaling has to be given
  rather than implied: the reported 0.7613 is
  $(0.805-0.182)/(1-0.182)$, where 0.805 is raw purity and 0.182 is the
  purity eleven studies of these sizes would give by chance.
- **Why $k$NN purity and not the scIB batch metrics.** One line, pointing
  at the Discussion: iLISI is exactly 0.0000 and cLISI exactly 1.0000 for
  all ten representations, so the standard instrument cannot rank anything
  here.
- **Both are measured on the held-out split**, because unlike the metadata
  axes these measure the fit itself.
- **Harmony and Scanorama are transductive** and that is declared here, not
  left in the table's footnote alone.

## 2. Whole-corpus embedding — 11 words, and it should absorb the "whole-corpus rule"

**PROPOSAL, and the one structural question in this round.** `PRIORITY.md`
lists *Whole-corpus embedding* and *the whole-corpus rule* as two
subsections. They are the same argument: a label the model never received
cannot leak, therefore the split stops mattering for it. **I would write one
subsection, not two.** Two headings saying the same thing is worse than one
that says it properly.

What the single passage carries:

- The licence. Once the checkpoint is fixed nothing is being selected, and
  the cross-donor estimator already discards same-donor neighbours, so for
  a label the model never received a held-out split protects against
  nothing.
- The table of where each variable is measured: phase, study, platform and
  tissue held out because they reached the model; disease, stage, grade,
  severity, cell family, cycle day and progesterone on all 1,577,728 cells
  because they did not. Donor recovery is the odd one out, held out despite
  never being an input, because it measures the fit itself.
- **The region procedure**, which exists nowhere else in the paper: every
  cell takes the cell family of its 25 nearest *labelled* neighbours,
  searched in the sixteen dimensions and not in the UMAP. The reason is
  worth one clause, because it is a real choice: a bounding box drawn on a
  UMAP assumes each family occupies one convex patch, and immune cells do
  not.
- This subsection is what licenses `[2]`, `[4]` and every whole-corpus
  panel, so it has to come before them in the reader's mind even though
  Methods comes after.

## 3. Optimisation — 0 words

**Three corrections to the note that sits there now.**

- The note says lr $10^{-3}$. `training/base.yaml` says `3.0e-4`. The
  **arm config overrides it to 0.001**, and `run_config.json` for the
  reported arm confirms `lr = 0.001`, so the note is right and the base
  config is not the operative value. Quote the run record, not the base.
- The note says "early stopping at patience 5". Correct for the arms;
  `base.yaml` says 10 with a 25-epoch warmup, which the arms override to
  **patience 5, warmup 2**.
- `max_epochs: 50` in the base, **20 in every arm**.

What the passage says:

- AdamW, lr $10^{-3}$, weight decay $10^{-4}$, batch 256, bf16, gradient
  clipping at 1.0, KL weight ramped from 0 to 1 over the first 20% of steps.
- **The horizon is a shape, not a length**, and this is the only part that
  needs an argument. Cosine annealing takes $T_{max}$ from `max_epochs`, so
  the horizon sets how long the learning rate stays useful rather than when
  the run ends. At $T_{max}$ 12 the eleventh and twelfth epochs run at 6.7%
  and 1.7% of base rate; at $T_{max}$ 20 the same two run at 50.0% and
  42.2%. An arm still descending late is capped by the shape rather than by
  its own configuration.
- **What ends a run is early stopping on held-out reconstruction**, patience
  5 after a two-epoch warmup. No arm in this project has ever reached
  `max_epochs`.
- **A registered check that passed, and it is worth its sentence.** The
  configs state it in advance: if an arm's best epoch is its last, early
  stopping never fired and the arm did not converge. Verified for all six
  arms on 7 November, and none of them has its best epoch last (4 of 9,
  0 of 7, 4 of 9, 4 of 9, 5 of 10, 12 of 17). Every arm converged.
- **The selection sentence** `OUTSTANDING.md` requires: the reported
  checkpoint is `argmin val_nb` on the validation donors, and every metric
  reported in this paper is label-based and played no part in selecting it.
- bf16 and why, in one clause: FlashAttention has no fp32 kernel, and one
  forward-and-backward at the real training shapes measures 449.97 ms in
  fp32 against 174.87 ms in bf16. The Power Spherical sampler and the
  negative-binomial loss force fp32 back regardless.
- **A batch is one study by construction.** Two sentences, and they are
  load-bearing elsewhere: it is why ECS pairs are always within-study, and
  it is what the adversary sees.
- Seed 24, single runs, seed variability measured at 4%.

## 4. The severity merge — new, no heading yet

**The argument: this is sourced, not assumed.** That is the whole point of
the subsection and it should be its first sentence.

- Two cohorts record severity in different vocabularies: `marecko_2024` as
  rASRM I--IV, `duempelmann_2026` as mild against severe.
- duempelmann's own paper defines mild as rASRM I--II and severe as
  III--IV. The merge onto control / mild / severe therefore follows the
  published definitions rather than our judgement. **Cite both papers for
  their methods.**
- Coverage: 34 held-out donors and 118 across the whole corpus; dropping
  controls leaves 18 and 57.
- **Why the union variable is unused.** `severity (study vocabularies)`
  exists in the scored tables and appears nowhere in the paper, because its
  levels are study-prefixed (`stage_0`, `grade_mild`). A variable readable
  off study identity cannot carry a severity claim, and saying so pre-empts
  a reviewer who finds the column.

## 5. Cross-donor agreement — 812 words, written, never reviewed

The subsection carries a coral block listing six loopholes and one wrong
claim. Each needs a destination.

| | disposition |
|---|---|
| **The wrong claim** — "the number of distinct permutations is set by how many donors carry the label" | **Cut.** At 16 to 60 donors the number of assignments is astronomical and is not what binds. The binding constraint is the width of the null, which is loophole 1, and it is the stronger argument. |
| **1. `excess` is not comparable across labels.** The null's own 95th percentile tracks donor count: 0.06 at 34 donors, 0.18 at 36, 0.12 at 18, **0.42 at 16** | **Stays in Methods.** This is a property of the estimator, not a limitation of the study, and without it a reader puts 0.1313 and 0.7346 on one scale. |
| **2. $p$ is one-sided** | **One line in Methods.** It is why grade's $-$0.0414 is reported as "not positive" and never as "negative". |
| **3. The permutation is too permissive for a label spanning studies** | **Already written into the Discussion** as the unstratified null bounded by 0.7613. Methods points forward in half a sentence; it does not argue it twice. |
| **4. Unstratified by donor size** | **One clause**, with the remedy named. |
| **5. $k=100$ is a free choice with no sensitivity analysis** | **State it plainly.** The honest form is that $k=100$ is fixed and coverage is reported beside every scalar, not that the choice was validated. |
| **6. $p$ floors at $1/201$** | **Already in `[3]`.** Methods states the floor once where the estimator is defined. |

Two more jobs in this subsection:

- **Rewrite to the $t=1$ convention**, which was settled and never applied
  here: agreement is reported for every labelled cell with at least one
  cross-donor neighbour, 88.2% of them, with coverage beside the scalar.
  The prose still describes the single-scalar version.
- **E1 lands here**, by AW's ruling: whole-corpus agreement on a
  donor-constant label is a readout of donor memorisation, $\rho$ +0.943
  for disease against +0.371 for cell family, the only label that varies
  within a donor. It is the justification for the estimator and it belongs
  beside it.

## 6. Study selection — carries a TODO

- The TODO is a **PRISMA figure**, which is a display-item decision rather
  than prose. Six items are the budget and five are spoken for, so this is
  a real choice and not a formality.
- **A live inconsistency, and it is in the manuscript now.** Line 46 says
  "254 donors". Lines 597 and 673 say "269 donors". Both are true of
  different things, and the paper calls both "donors": there are **269
  donor identifiers and 254 people**, because one study pair deposits
  fifteen of them twice. The estimator operates on identifiers; the corpus
  description should say people. This needs one consistent form of words
  and a sentence explaining the gap, and it is the same fifteen people the
  Discussion's first limitation is about.

---

## Suggested order of work

1. **Optimisation** and **Donor and study recovery** first. Both are
   self-contained, both are pure description, and neither blocks on a
   decision.
2. **Whole-corpus embedding**, once the merge-or-split question above is
   answered.
3. **The severity merge**, which needs the two citations added to
   `references.bib`.
4. **Cross-donor agreement** last. It is a rewrite rather than a seed, it
   is the longest, and it is the one a methods reviewer will read hardest.
5. **Study selection**'s donor-count fix can go in with any of the above.
