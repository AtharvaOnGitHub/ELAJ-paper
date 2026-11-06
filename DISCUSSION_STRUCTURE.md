# Discussion — what it has to carry

Rewritten 6 November 2026 on AW's comments. The first version framed this
as "handoffs", finishing sentences Results left open. **That was wrong and
he corrected it:**

> "Discussion is not about incomplete sentences from Results finding a
> home. It is about going beyond the numbers and saying something about the
> model, data, field, architecture, SOTA, etc. Handoffs is something like
> 'we spoke about the model but didn't comment on the field. Now we speak
> about the field'."

So this file is organised by **what we say about the field**, not by what
Results left over. ~1,000 words is the guideline; AW has ruled that going
over is acceptable for a submission draft.

---

## The paragraphs

### 1. What this establishes (~180)

The full claim, stated elaborately rather than summarised. Pooled
single-cell data from eleven studies can be read as sixteen numbers that
are blind to the donor and still hold the menstrual cycle, on a corpus
where phase is constant within a donor and therefore geometrically
indistinguishable from a batch effect.

The careful version of the cycle claim, which Results supports and the
looser version does not: the head supplies 34.5% of the phase margin, so
"the cycle was recovered" overstates it. **"The cell-type structure of the
cycle was recovered" is the claim that holds**, because the phase head is
one linear map over all sixteen dimensions and was never given cell family,
and Figure 3 shows the cycle sharp in stromal cells, present in epithelial
and close to absent in endothelial and immune.

### 2. Pooling, and the framework this is (~210)

The single-biopsy confound is not an endometriosis problem. Any design
where each donor contributes one timepoint makes the biology collinear with
the sample, and the field's response is a correction strength reported as
one scalar. It is two axes, and the two knobs here move along and across
the front independently (`[1]`).

AW's framing, and the contribution at its proper altitude: **a framework
for building disease atlases where data is scarce and batch structure is
severe.** Both conditions hold wherever tissue requires surgery.

Model selection folds in here rather than taking its own paragraph: the arm
with the best held-out reconstruction in this project is the arm that holds
the least biology, and it got there by reading provenance instead of cells.
Single-cell models are routinely selected on reconstruction or ELBO.

### 3. Scale (~130)

1.88M parameters at sixteen dimensions against pretrained models at 256 to
3,072. Width is not what produces the result: PCA at sixteen beats scGPT at
512 on cross-donor phase (0.6457 against 0.4869), and across the ten methods
width is *negatively* associated with phase agreement
($\rho = -0.6503$, $p = 0.0418$).

AW: "We have changed disease atlas efficiency drastically. That is a
disruptive result." Stated as efficiency, not as a win over foundation
models, because A5 says we do not win on cell type.

### 4. How the field measures batch correction (~230)

Three things, all re-derived from the benchmark files on 6 November rather
than taken from the notes.

**(a) The standard scorecard does not discriminate here, in both halves.**
`ilisi_knn` is **exactly 0.0000 for all ten representations** and
`clisi_knn` **exactly 1.0000 for all ten**; `kbet` spans 0.0000 to 0.0400.
One of those is the batch half and one is the bio half.
*Correction to `RESULTS_STRUCTURE.md`'s E3: it says `pcr_batch` is exactly
1.0000 for PCA, scVI, scANVI and ELAJ. It is not — 0.5249, 0.9268, 0.9386
and 0.8603. That sentence must not be reused.*

**(b) The third axis AW asked for, and it completes (a).** Cross-donor
agreement on cell family, the field's usual biology axis, puts **nine of
the ten methods within 0.0076 of each other** (0.9820 to 0.9896), with only
Geneformer outside at 0.9023. So the bio half is saturated as well as
degenerate: a benchmark that ranks methods on cell-type conservation cannot
rank anything on a corpus like this.

**(c) A disease score is partly a memorisation score.** Across the ten
methods, agreement on disease status tracks donor recovery at $\rho$ +0.721
($p$ 0.019) while phase does not (+0.176). Disease is constant within a
donor, so a model that memorises donors gets disease for free, and Methods'
same-donor floor is the mechanism: a quarter to three-fifths of a cell's
hundred neighbours come from its own donor, twenty to fifty times chance,
and 44% to 71% of plain agreement is that free part. **This is where E1,
E2 and E4 get their comment in relation to the results**, rather than
sitting silently in Methods.

B2 and B3, if they appear at all, are one line here. AW: the defeated
discriminator is a claim arising from our own mistake and is well known
from GANs.

### 5. Endometriosis is in the endometrium (~200)

The paper's clinical point, and AW's: a person's own uterine lining carries
signal about whether they have disease growing elsewhere. Cross-donor
agreement on disease status is 0.3364 with no permutation reaching it
($p$ 0.005), on cells that are all eutopic endometrium.

**The argument this paragraph has to make explicitly**, or a reviewer will
make the opposite one: 0.3364 is the *lowest* of the ten methods. That is
a strength, not a weakness, and (c) above is why — the higher scores belong
to the methods from which donors are most easily recovered. ELAJ is the
least donor-identifiable representation tested, so its disease signal is
the least contaminated one in the table.

Then the direction: diagnosis today takes 11.1 years and requires
laparoscopy. See the argument below on what we are allowed to call the
alternative.

C4 and C5 would sit here. See the open question.

### 6. Staging should be reimagined (~240)

The longest paragraph and the one that justifies the venue.

What staging has meant in endometriosis: rASRM scores a surgeon's view of
lesion size, depth and adhesion at one operation. It was built to predict
fertility outcomes, it is what every cohort records, and it is the number a
patient is given. Lesion burden has never tracked symptom severity, and
patients have said so for decades.

What we measured: disease status is recoverable (0.3364, $p$ 0.005), merged
severity clears its null across 118 donors (0.1286, $p$ 0.025), and
mild against severe **among patients only** does not (0.0744, $p$ 0.129 at
57 donors). No other method does better: across all ten, merged severity
ran 0.0759 to 0.1860 and not one cleared its own null. Across all six of
our own configurations it cleared in none ($p$ 0.149 to 0.468).

The claim, worded exactly: **not recoverable from this corpus at this donor
count**, never "not biologically real". What follows is a case for a
staging grounded in biology rather than in what a surgeon can see, and for
treating the millimetre-lesion patient's account as data rather than as
noise.

### 7. Limitations (~180)

Plainly, not defensively, and only the ones that bite.

F1 width is not matched (and (b)/(3) above already bound how much that
matters). F2 cycle-day continuity rests on one cohort of 60 donors. F4
17,873 held-out cells, 4.3%, share a donor with training through the one
overlapping study pair. F5 li\_2025 is a follicular-fluid aspirate labelled
as endometrium: 45,312 cells, 2.87%, 6 of 269 donors, contributing no
cell-family and no phase labels. F6 reported arms are single runs with seed
variability measured at 4%.

Two more that are not in F1--F6 and should be:

- **The corpus carries a subset of the metadata that matters.** AW's note.
  No cohort records all of cycle day, progesterone, stage, grade and
  treatment, and cell-type labels exist for endometrium only, so 392,629
  cells from five other sites carry none.
- **The permutation null is unstratified.** Reassigning the donor-to-label
  map across all eleven studies breaks the label-study association, so the
  pooled null never sees whatever study structure remains in the latent.
  The bound on how much that can matter is our own study-mixing figure,
  0.7613. A within-study permutation is the correct fix and is not built.

F3 is dropped, because it is C5 and C5 is in question below.

### 8. What this makes possible (~120)

Concrete. No reflexive gesture at clinical translation.

---

## Three arguments back

### A. "Non-invasive" is the wrong word and a reviewer will catch it

AW's framing: "the endometriosis patient's endometrium has signal about the
disease. We suggest that to be a possible direction for non-invasive
testing."

The finding is right and it is the best clinical sentence in the paper. The
word is the problem. Every cell in this test came from an **endometrial
biopsy**. A pipelle biopsy is an outpatient procedure under no general
anaesthetic and is worlds away from diagnostic laparoscopy, but in clinical
usage "non-invasive" means blood, urine, saliva or imaging. A clinician
reviewer reads "non-invasive" and finds a biopsy, and the whole paragraph
loses credit for a word we did not need.

**Proposed: "without surgery", or "a route to diagnosis that does not
require laparoscopy".** This keeps the entire force of the claim — 11.1
years because confirmation needs an operating theatre, and our result says
the answer is present in tissue obtainable in a clinic — and costs nothing.

### B. C4 and C5 cannot be written as they stand

AW asked for both in Figure 4's legend and in the Discussion. Two problems,
found by reading the source files rather than the notes.

**Their only statistic was withdrawn.** C4 and C5 live in
`Outputs/analysis/*/disease_within_family.csv` and the quantity is
`over_scatter`, a centroid distance over a mean root-mean-square radius.
AW ruled that unsound on 2 November — it describes a cloud only if the
cloud is a filled isotropic ball — and it was cut from `[3]` and `[4]` for
exactly that reason. There is no sound replacement in any file.

**And the claim does not survive its own arm check.** Ranked by
`over_scatter`:

| arm | marecko\_2024 | duempelmann\_2026 |
|---|---|---|
| B hi | **immune** .773 > epi .609 > endo .576 > stromal .428 | **immune** .289 > endo .233 > epi .211 > stromal .206 |
| B lo | **immune** .832 > stromal .570 > endo .507 > epi .506 | endo .266 > epi .252 > stromal .216 > **immune .191** |

Immune is first in three of the four cells and **last** in the fourth.
Changing one weight moves it from rank 1 to rank 4 in the second cohort.
`RESULTS_STRUCTURE.md` has C4 as "rank 1 of 4 in both arms", which is true
of marecko and false of duempelmann.

Three ways forward:

1. **Drop C4 and C5, and drop the Introduction's promise with them.** The
   Introduction currently asks "whether a signature found in one cohort
   holds in another" and the paper would then not answer it. Cheapest,
   and it removes a question we raised ourselves.
2. **Compute the sound statistic.** Cross-donor disease agreement
   restricted to each cell family, which is the estimator we already
   trust, with its own permutation null. The notes name this as the robust
   replacement that was never built. It answers the Introduction properly
   and it is the only honest route to the claim. It breaks the standing
   "no further calculation" rule, but the exception AW wrote into that rule
   is "unless something is wrong", and an unsound statistic behind a
   printed claim is wrong. **This is my recommendation.**
3. Write them qualitatively off a figure. Not available: Figure 4 has no
   panel showing disease within cell family, so there is nothing to read
   them off.

### C. E3 goes to the Discussion, and I withdraw the Methods argument

I proposed Methods. AW: "I think it is a finding of the paper so it
shouldn't be in Methods." He is right, and the re-derived numbers make it
a stronger finding than the note claimed — two metrics perfectly
degenerate across all ten representations, one from each half of the
scorecard. That is a result about the field's measuring instrument on
corpora of this shape, not a justification for our estimator. It is
paragraph 4(a).

---

## Open question

**C4 and C5: option 1, 2 or 3 above.** Nothing else is pending; every other
comment on the previous version is settled and built into the paragraphs.
