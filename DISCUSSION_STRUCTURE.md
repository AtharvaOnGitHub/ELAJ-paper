# Discussion — what it has to carry

Written 6 November 2026, after Results closed. Three inventories and a
plan. The inventories exist so nothing is lost, NOT so the Discussion
becomes the place everything is dumped.

NMI: ~1,000 words, **no subheadings**, limitations in the open rather than
in a defensive final paragraph.

---

## 1. The handoffs — where Results deliberately stopped short

Each of these is a finding whose numbers are already on the page. The
Discussion does not restate them; it finishes the sentence.

| from | Results states | stops short of |
|---|---|---|
| `[1]` | the nine readings across both knobs | that one knob *traverses* the front and the other *moves* it, and that moving it stops working past the middle weight. That is the claim that makes this a frontier rather than a tuning parameter |
| `[2]` | 392,629 cells from five sites carry no cell-type label in any of five annotation columns | that the public record cannot say what those cells are, which is a finding about the field's data and not about our model |
| `[3]` | 65.5% architecture, 34.5% head | that "the cycle was recovered" is therefore the wrong claim. **"The cell-type structure of the cycle was recovered" is the right one**, and Figure 3's legend already shows the split the supervision could not have produced |
| `[4]` | disease recoverable, merged severity recoverable at 118 donors, mild-against-severe not at 57 | the staging argument in full |
| `[5]` | disease agreement tracks donor recovery at $\rho$ +0.721 while phase does not (+0.176) | that an axis whose dominant property is donor memorisation is not a performance axis, so the field's disease-classification scores need reading differently |
| `[6]` | the shuffled grouping has the project's best reconstruction and worst biology | that reconstruction loss is not a model-selection criterion for a representation |

---

## 2. The round-up — findings with no spotlight anywhere

Checked against `RESULTS_STRUCTURE.md` claim by claim, and against the
current Results and legends rather than against what the notes claim.
**A verdict is proposed for each. Several should stay out.**

| # | finding | where it is now | proposed |
|---|---|---|---|
| **C4** | disease signal concentrates in the immune compartment (0.77 / 0.83 inside marecko's immune cells against 0.22 corpus-wide) | **nowhere.** Figure 4's note says "CARRIES C4 and C5" and its caption does not mention either. The note is stale | see the open question below |
| **C5** | and it does not replicate across cohorts (0.19--0.29, ordering flips between arms) | **nowhere**, same stale note | the Introduction promises exactly this question. See below |
| **B2** | a defeated discriminator is not evidence that a latent is study-free (+0.883 adversary loss against donor kNN, +0.890 against study kNN) | cut from Methods by AW on 6 Nov, cut from `[6]` this session | **one sentence in the Discussion.** It is the most transferable negative result the project holds and it is a comment about the field, which is what this section is for. The objection stands: it diagnoses the 64-unit discriminator retired at `58cc532`, and no reported arm uses it |
| **B3** | discriminator capacity, not batch composition, was the cause | with B2 | fold into B2's sentence or drop with it |
| **E3** | the scIB batch metrics are degenerate here: `ilisi_knn` exactly 0.0000 and `pcr_batch` exactly 1.0000 for PCA, scVI, scANVI and ELAJ alike, `kbet` 0.000--0.025 for all | **no home since 2 November.** The longest-open question in the project | **Methods, not Discussion.** It is the justification for measuring study by kNN purity, and it belongs beside the estimator it justifies. A scIB-literate reviewer will ask, and Methods is where they will look |
| **A7** | reconstruction beats a study-mean baseline by 6.5% | **nowhere**, and the reference value is not re-derivable. The training log says 0.4024 against **0.4315, +6.7%**, so the 6.5% in `RESULTS_STRUCTURE.md` is wrong as well as unsourced | **leave out.** It is a weak number, it would have to be derived before it could be printed, and `[6]`'s point about reconstruction cuts against quoting it approvingly |
| **E1** | whole-corpus agreement on a donor-constant label is a donor-memorisation readout, $\rho$ +0.943 | Methods, by AW's ruling | stays in Methods |
| **E2, E4** | the same-donor floor; the p-floor set by donor count | Methods, written | stay |
| **F1--F6** | the six limits | planned for here | yes, and plainly |

---

## 3. The field comments — our place in it

This is what the section is actually for, and the paragraph plan below is
built around these rather than around a tour of the results.

**On endometriosis.** Diagnosis requires surgery and takes 11.1 years. The
scale that surgery produces describes lesions, and we cannot read it off the
cells. A person's endometrium says whether they have the disease and not how
severe a surgeon judged it to be. That is the paper's most disruptive claim
and the one a patient would recognise.

**On pooling.** Every donor here was biopsied once, so phase is constant
within a donor and sits in the same geometric form as a batch effect. That
is not an endometriosis problem. It is true of every single-biopsy design,
and naming the others is what stops this reading as endometriosis-specific
tooling.

**On how the field measures batch correction.** Three separate things we
can say, and probably only room for one: the standard scIB metrics do not
discriminate on this corpus; a defeated adversary is not evidence of an
invariant latent; and a disease score that tracks donor recovery is
measuring memorisation.

**On how the field selects models.** The arm with the best held-out
reconstruction in this project is the arm that holds the least biology, and
it got there by reading provenance instead of cells. Single-cell models are
routinely selected on reconstruction or ELBO.

**On scale.** A 1.88M-parameter model at sixteen dimensions against
pretrained models at 256 to 3,072. Width is not what produces the result,
and PCA at sixteen beating scGPT at 512 on both biology axes is the cleanest
way to say so without claiming more than we measured.

---

## 4. Proposed paragraphs, ~1,000 words, no subheadings

1. **What the work establishes, at altitude.** ~160 words. Not a summary.
   Pooled single-cell data can be read in sixteen numbers that are blind to
   the donor and still hold the cycle, and the cycle's *cell-type structure*
   is the part supervision cannot account for.
2. **Why the frontier is the contribution.** ~170. The two knobs do
   different things; correction strength is reported as a scalar in this
   field and it is two axes. Name the other single-biopsy settings.
3. **Staging.** ~200, the longest, and the mic drop. Must read "not
   recoverable from this corpus at this donor count", never "not
   biologically real".
4. **What this says to people who build these models.** ~170. Reconstruction
   is not a selection criterion; the phase head regularises; and whichever
   measurement comment from §3 survives the budget.
5. **Limitations.** ~180. F1--F6, li\_2025 as follicular fluid, the
   annotation gap, and the pooled-null concern bounded by our own 0.7613.
6. **What it makes possible.** ~120. Concrete. No reflexive gesture at
   clinical translation.

---

## 5. The budget, stated rather than discovered later

Abstract 151 + Introduction 482 + Results 2,618 = **3,251 of 3,500**.
That leaves **249 words** for a section that wants 1,000.

Roughly 750 words have to come from somewhere, and that is AW's call. The
candidates, largest first:

- **`[1]`'s two knob paragraphs, ~330 words**, carrying all nine readings at
  full precision. Compressed to the shape of the finding plus the three
  readings that carry it, ~150 words come back. This is the passage AW asked
  to be made number-heavy, so it is his to cut and not mine.
- **`[4]`, ~430 words.** The ten-method corroboration paragraph restates in
  prose what Figure 4h shows.
- **`[6]`, ~730 words.** The two long paragraphs are the two that carry the
  trajectory argument, which is the part no other paper in this field writes.
- **The Introduction's ¶4, ~120 words** of literature review that the
  Discussion will partly repeat.

Doing nothing is also an option: NMI's limit is a guideline and editors
routinely accept overruns on a paper they want. But it should be a decision.

---

## 6. Open questions for AW

1. **C4 and C5 are not in the paper at all.** The immune concentration and
   its non-replication were assigned to Figure 4's panels and the caption
   never made either claim. The Introduction promises "whether a signature
   found in one cohort holds in another", which is C5 exactly. Three ways
   to go: (a) add both to Figure 4's caption, which costs no main-text
   words; (b) one Discussion sentence on the non-replication as a finding
   about cohort-level reproducibility; (c) leave out, and drop the promise
   from the Introduction instead. **(a) is cheapest and (b) is the one that
   answers the Introduction.**
2. **Does B2 get its sentence?** It is the best field comment available and
   it describes a discriminator we no longer run.
3. **E3 to Methods, or does it stay homeless?** It has been open since
   2 November and Methods is the right home.
