# Discussion — what it has to carry

Rewritten 6 November 2026 on AW's detailed review. The first version framed
this as "handoffs", finishing sentences Results left open. **That was wrong
and he corrected it:**

> "Discussion is not about incomplete sentences from Results finding a
> home. It is about going beyond the numbers and saying something about the
> model, data, field, architecture, SOTA, etc. Handoffs is something like
> 'we spoke about the model but didn't comment on the field. Now we speak
> about the field'."

Organised by **what we say about the field**. ~1,000 words is the
guideline; AW has ruled going over acceptable for a submission draft, so
the plan below runs to roughly 1,350.

**Register, from the same review:** adjectives are free here in a way they
are not in Results. "Lower is better" has already been established for the
cost axes, so the goodness of a number can be carried by a word rather than
re-argued. Where Results showed numbers and let the reader conclude, the
Discussion concludes.

---

## The paragraphs

### 1. What this establishes (~170)

The full claim, **stated elaborately rather than summarised.** AW: we did
state it in Results, and it is worth stating again at length here.

Pooled single-cell data from eleven studies read as sixteen numbers that
are blind to the donor and still hold the menstrual cycle, on a corpus
where phase is constant within a donor and therefore geometrically
indistinguishable from a batch effect.

The careful version of the cycle claim, which Results supports and the
looser one does not: the head supplies 34.5% of the phase margin, so "the
cycle was recovered" overstates it. **"The cell-type structure of the cycle
was recovered" is the claim that holds** — the phase head is one linear map
over all sixteen dimensions and was never given cell family, and Figure 3
shows the cycle sharp in stromal cells, present in epithelial, close to
absent in endothelial and immune.

### 2. Pooling, and the framework this is (~190)

The single-biopsy confound is not an endometriosis problem. Any design
where each donor contributes one timepoint makes the biology collinear with
the sample, and the field's answer is a correction strength reported as one
scalar. It is two axes, and the two knobs move along and across the front
independently (`[1]`).

AW's framing, and the contribution at its proper altitude: **a framework
for building disease atlases where data is scarce and batch structure is
severe.** Both conditions hold wherever diagnosis requires surgery.

**Model selection gets one line here, not a passage.** AW: "a comment on
this as we speak about pooling would be sufficient." The line: the arm with
the best held-out reconstruction in this project is the one that holds the
least biology, so reconstruction is not a selection criterion for a
representation.

### 3. Scale (~120)

1.88M parameters at sixteen dimensions against pretrained models at 256 to
3,072. Width is not what produces the result: PCA at sixteen beats scGPT at
512 on cross-donor phase (0.6457 against 0.4869), and across the ten
methods width is *negatively* associated with phase agreement
($\rho = -0.6503$, $p = 0.0418$).

AW: "We have changed disease atlas efficiency drastically. That is a
disruptive result." Framed as efficiency rather than as a win over
foundation models, because A5 says we do not win on cell type.

### 4. How the field measures batch correction (~230)

Three things, all re-derived from the benchmark files on 6 November rather
than taken from the notes.

**(a) The standard scorecard does not discriminate here, in both halves.**
`ilisi_knn` is **exactly 0.0000 for all ten representations** and
`clisi_knn` **exactly 1.0000 for all ten**; `kbet` spans 0.0000 to 0.0400.
One of those is the batch half and one is the bio half.
*Correction to `RESULTS_STRUCTURE.md`'s E3, which says `pcr_batch` is
exactly 1.0000 for PCA, scVI, scANVI and ELAJ. It is 0.5249, 0.9268, 0.9386
and 0.8603. That sentence must not be reused.*

**(b) The third axis AW asked for, and it completes (a).** Cross-donor
agreement on cell family, the field's usual biology axis, puts **nine of
the ten methods within 0.0076 of each other** (0.9820 to 0.9896), with only
Geneformer outside at 0.9023. The bio half is saturated as well as
degenerate: a benchmark that ranks representations on cell-type
conservation cannot rank anything on a corpus of this shape.

**(c) A disease score is partly a memorisation score.** Across the ten
methods, agreement on disease status tracks donor recovery at $\rho$ +0.721
($p$ 0.019) while phase does not (+0.176). Disease is constant within a
donor, so a model that memorises donors gets disease for free, and the
same-donor floor is the mechanism: a quarter to three-fifths of a cell's
hundred neighbours come from its own donor, twenty to fifty times chance,
and 44% to 71% of plain agreement is that free part. **This is where E1 and
E2 get their comment in relation to the results** instead of sitting
silently in Methods.

**B2 and B3 are skipped by default.** AW: the defeated discriminator is a
claim arising from our own mistake and is well known from GANs. One line at
most, and only if the paragraph has room it does not currently have.

### 5. Endometriosis is in the endometrium (~180)

The paper's clinical point. A person's own uterine lining carries signal
about whether they have disease growing elsewhere: cross-donor agreement on
disease status is 0.3364 with no permutation reaching it ($p$ 0.005), on
cells that are all eutopic endometrium.

**One line, not a paragraph, on why our lowest number is the trustworthy
one.** AW: the goodness of these numbers is already established and
adjectives are free here. So: ELAJ gives the lowest disease score of the
ten and is also the representation from which donors are hardest to
recover, which by (c) makes it the least contaminated score in the table.
One sentence, no re-derivation.

Then the direction: diagnosis today takes 11.1 years and requires
laparoscopy, and this says the answer is present in tissue that can be
sampled **without surgery** (see the wording note below).

C4 and C5 are parked on AW's ruling: write the rest, then judge whether
they feel missing.

### 6. Staging should be reimagined (~240)

The longest paragraph and the one that justifies the venue. AW: talk freely
here about what staging has meant in endometriosis.

What it has meant: rASRM scores a surgeon's view of lesion size, depth and
adhesion at one operation. It was built to predict fertility outcomes, it
is what every cohort records, and it is the number a patient is given.
Lesion burden has never tracked symptom severity, and patients have said so
for decades.

What we measured: disease status is recoverable (0.3364, $p$ 0.005), merged
severity clears its null across 118 donors (0.1286, $p$ 0.025), and mild
against severe **among patients only** does not (0.0744, $p$ 0.129 at 57
donors). No other method does better: across all ten, merged severity ran
0.0759 to 0.1860 and not one cleared its own null; across all six of our
own configurations it cleared in none ($p$ 0.149 to 0.468).

**E4 gets its comment here**, because a negative cannot be read without it:
the permutation p has a floor set by donor count, so the claim is **not
recoverable from this corpus at this donor count**, never "not biologically
real". What follows is the case for a staging grounded in biology rather
than in what a surgeon can see, and for treating the millimetre-lesion
patient's account as data rather than noise.

### 7. Limitations (~170)

Plainly, not defensively, and **only the ones that bite.** AW: mostly
agreed, some can be skipped.

Kept:

- **F1**, width is not matched — but (b) and 3 above already bound how much
  that can matter, so it is one clause rather than a confession.
- **F2**, cycle-day continuity rests on one cohort of 60 donors.
- **F5**, li\_2025 is a follicular-fluid aspirate labelled as endometrium:
  45,312 cells, 2.87% of the corpus, 6 of 269 donors, and its
  eutopic/control marks follicular fluid from an ovarian endometriosis
  patient against a male-factor infertility control. It contributes no
  cell-family and no phase labels, so the cycle and cell-type results are
  untouched. **AW's point from the review:** this is the exception to
  "every cell in the disease test came from a biopsy", and it is too small
  to carry a diagnostic claim either way.
- **The corpus holds only a subset of the metadata that matters.** AW's
  note, and it replaces the annotation-gap sentence rather than joining it.
  No cohort records all of cycle day, progesterone, stage, grade and
  treatment.
- **The permutation null is unstratified.** Reassigning the donor-to-label
  map across all eleven studies breaks the label-study association, so the
  pooled null never sees whatever study structure remains in the latent.
  Bounded by our own study-mixing figure, 0.7613. A within-study
  permutation is the correct fix and is not built.

Skipped, with reasons:

- **F3** is C5, which is parked.
- ~~**F4**~~ **REINSTATED, 6 November, and it is now the FIRST limitation.**
  I dropped it as "a Methods fact about the split that does not change a
  claim" and AW caught it: it changes two claims. The overlapping pair
  carries a menstrual phase and a disease status on every cell, so the leak
  sits inside the two headline held-out measurements. The estimator
  discards a neighbour by donor identifier, and these fifteen people hold
  two, so a same-person neighbour is counted as cross-donor. Phase, disease
  and severity are donor-constant, so it inflates them.
  *Wording corrected in Methods too:* "share a donor with training" is not
  what the audit measured. One of the seven split samples has both sides
  held out (2,945 and 997 cells), so 3,942 of the 17,873 share a person
  with the held-out set rather than with training, which is the more direct
  problem for a cross-donor estimator, not a lesser one.
- **F6** (single runs, 4% seed variability) — kept only if the paragraph
  has room; it is real but it is the smallest of the six.
- **The annotation gap** (392,629 unannotated cells). AW: "doesn't need to
  be said". Results already leaves it at the right place — unannotated, and
  their position in the UMAP may be indicative.

### 8. What this makes possible (~130)

Concrete. No reflexive gesture at clinical translation.

---

## Settled in this review

| item | decision |
|---|---|
| "non-invasive" | **"without surgery"**, or "does not require laparoscopy". Every cell in the disease test is an endometrial biopsy, and in clinical usage non-invasive means blood, urine, saliva or imaging. li\_2025's follicular fluid is the one exception and is too small to support a test either way |
| our lowest disease score | one line, leaning on adjectives and on (c), not a re-derivation |
| C4, C5 | **parked.** Write the rest, then decide whether they feel missing. Their only statistic is the `over_scatter` ratio AW ruled unsound on 2 November, and immune moves from rank 1 to rank 4 in duempelmann when the KL weight changes, so they cannot be written as they stand |
| E3 | Discussion, paragraph 4(a). My Methods proposal is withdrawn — it is a finding about the field's instrument, not a justification for our estimator |
| E1, E2 | stay in Methods, and get their comment in 4(c) |
| E4 | stays in Methods, and gets its comment in 6, where the negative cannot be read without it |
| A7 | out of the paper. The reference value is not re-derivable and the log says +6.7%, not the 6.5% in `RESULTS_STRUCTURE.md`. **Optional later:** one line on average reconstruction loss in `[1]`, which AW says he would not miss |
| B2, B3 | skipped by default; one line at most |
| model selection | one line inside paragraph 2 |
| budget | over is fine for the submission draft |

---

## The plan

1. Seed paragraphs 1--4 in one pass. They are the model-and-field half and
   they share a register.
2. AW edits.
3. Seed 5--8. They are the disease-and-limits half, and 6 is the one that
   needs the most care.
4. AW edits.
5. Judge C4 and C5 against the finished section.
6. Re-audit. Both auditors read `02-results.tex` only, so **every number
   this section quotes has to be added to their scope** or the Discussion
   ships unchecked. That is a change to `TEX` in both scripts, not a new
   derivation, since the numbers are the ones Results already sources.
