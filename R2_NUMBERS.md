# R2 — Biology is an emergent property of training

The title changed the subsection. "Emergent" means the model recovers
something it was never given, so the first job is to separate what it was
given from what it was not. Two numbers that looked like obvious candidates
do not survive that test, and they are listed first so they do not get used.

---

## What the model was given, and what it was not

| given | withheld |
|---|---|
| gene expression, grouped into 44 Reactome/GO pathway groups | **cell type and cell family** |
| study, tissue, platform (decoder covariates) | **disease status** (`d_disease = 0`) |
| **menstrual phase**, through one linear classification head | surgical stage, grade, severity |
| | cycle day, serum progesterone, epithelial pseudotime |

Everything in the right column is fair game for an emergence claim.
Menstrual phase is not, **unless** the ablation is quoted with it.

---

## TWO TRAPS. Do not build the subsection on these.

**Cell family 0.9807 is not distinctive.** PCA reaches 0.9866 and SCimilarity
0.9896, both above us. The band across the nine representations that recover
it at all is 0.0076. Every method emerges cell family, so emerging it proves
nothing about \elaj{}.

**Disease status 0.3364 is the LOWEST of the ten.** scanorama reaches 0.4290,
scFoundation 0.4024, Harmony 0.3846. We are last.

That is explainable rather than embarrassing: across the ten, donor recovery
predicts the disease score at $\rho = +0.721$, and we memorise donors least.
But the explanation belongs in R4 with the rest of the disease material.
**Quoting 0.3364 here as evidence of emergence invites a reader to check
Table 1 and find nine better numbers.**

---

## 1. Most of the cycle signal is not coming from the supervision

| arm | cross-donor cycle agreement |
|---|---:|
| \elaj$_{B\,hi}$ | 0.7346 |
| same model, **phase head removed and retrained** | 0.4812 |

**65.5% of the chance-corrected signal survives removing the head.** The
supervision accounts for 34.5%; the architecture accounts for the rest.

**Means:** the one label the model was given is mostly not the reason it has
that label's signal. This is the strongest single piece of evidence for the
subsection's title.

⚠ **Derived, and the derivation was wrong once.** Cross-donor values are
already chance-corrected, so the split is the ratio 0.4812 / 0.7346, not a
difference from a chance rate. An earlier version reported 30.5% surviving
by subtracting chance twice.

⚠ This is an ablation, and ablations were assigned to R6. See the structural
note at the foot.

## 2. The cycle's cell-type structure was never supplied

Displacement from proliferative to secretory, divided by each cell type's own
spread, so the four are comparable:

| stromal | epithelial | endothelial | immune |
|---:|---:|---:|---:|
| **1.0677** | **0.9824** | 0.3918 | 0.3409 |

**Means:** the cycle moves stroma and epithelium roughly three times further
than it moves endothelium and immune cells. **The phase head is a single
linear map over the whole latent and was never given cell type.** Nothing in
the objective could have produced this ordering; it is a consequence of where
the model placed cells.

**It is also biologically correct**, which is what makes it evidence rather
than an artefact: the endometrial cycle acts on the stromal and epithelial
compartments.

**Will not support:** a claim about immune cells being unaffected by the
cycle. 0.3409 is a displacement, not an absence, and R5 finds immune cells
carrying disease signal.

⚠ This was R3's material. With the new title it is R2's best content.

## 3. Labels the model never received are recoverable

Whole corpus, parameters frozen, each against its own permutation null.

| label | value | cells | donors | p |
|---|---:|---:|---:|---:|
| cell family | 0.9807 | 630,689 | 118 | 0.005 |
| menstrual phase | 0.6796 | 723,599 | 142 | 0.005 |
| severity (merged) | 0.2655 | 631,090 | 118 | 0.005 |
| surgical stage | 0.3320 | 164,474 | 58 | 0.005 |
| grade | 0.0263 | 465,391 | 60 | **0.408, fails** |

**Means:** three labels the model never saw clear their nulls. Grade does
not, and saying so is what makes the other three credible.

⚠ **Severity and stage belong to R4.** Listing them here duplicates R4's
subject. My view: name them in one clause as examples of withheld labels
being recoverable, and leave the interpretation to R4.

## 4. Technical variation is not the explanation

Best-of-sixteen linear criterion, so every value is the strongest correlation
available across the sixteen dimensions.

| withheld biology | | technical control | |
|---|---:|---|---:|
| epithelial pseudotime | **0.5801** | mitochondrial fraction | 0.3396 |
| serum progesterone | **0.4725** | total counts | 0.2514 |
| | | genes detected | 0.3366 |
| | | doublet score | 0.1366 |
| | | scrublet score | 0.1551 |

**Means:** the model was given neither column. Biology wins every pairing.

**Will not support:** "the latent contains no technical signal". 0.3396 for
mitochondrial fraction is not small, and the criterion takes the best of
sixteen dimensions, so these are upper bounds. Say that.

## 5. The emergence depends on the pathway grouping being real

Replacing the 44 Reactome/GO groups with random groups of the same sizes:

| | \elaj$_{B\,hi}$ | random groups | change |
|---|---:|---:|---:|
| cell family | 0.9820 | 0.9606 | **−0.0214** |
| menstrual phase | 0.7346 | 0.6780 | **−0.0566** |
| disease | 0.3364 | 0.2698 | **−0.0666** |

**Means:** scramble the biological structure of the input and the biology
comes out worse. This is the mechanism behind the title, and it is the one
ablation that is not a component-removal but a structure-removal.

⚠ Also R6's material.

---

# The structural problem the new title creates

**Three of the five blocks above were assigned to other subsections.** Block 1
and block 5 are ablations (R6), block 2 was R3, and block 3's severity and
stage are R4.

That is not a reason to avoid them. It is a sign the title has reorganised
the section. Two coherent options:

**Option A — R2 absorbs R3, and borrows two ablations.** R2 becomes the
emergence subsection: the cycle survives without its head, its cell-type
structure was never supplied, withheld labels are recoverable, technical
variation does not explain it, and scrambling the pathway groups breaks it.
R3 disappears. R6 keeps the component ablations (ECS, sentinel, statistics)
and loses D1 and D3 to here.

**Option B — R2 stays narrow**, carrying only blocks 3 and 4, and the
emergence claim is made by pointing forward to R3 and R6.

**I would take A.** The title is a claim, and the evidence for it is blocks 1,
2 and 5. Under B the subsection asserts emergence and then sends the reader
elsewhere for the proof, which is the thing the supervisor objected to about
leaving results to interpretation.

**What A costs:** R6 shrinks to ECS, the DNS sentinel and the statistics
path, which is thin but honest, and may fold into R2 as well.
