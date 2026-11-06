# Results notes

Moved out of `sections/02-results.tex` on 4 November 2026. A note of a
thousand words renders into the PDF and buries the prose it is about;
AW's rule is that the manuscript carries one-line notes and the detail
lives here. The tex keeps a single line per subsection pointing at the
heading below it.

## [1] The ELAJ frontier

CARRIES B1. FIGURE 1b, 1c. 213 words.

RESEEDED 2 November 2026 on AW's ruling, and he was right. Springer
Nature's own authoring guidance: "In the Results section, simply state what
you found, but do not interpret the results or discuss their implications."
The first draft opened with an argument about what the two terms do to each
other and closed on why this arm was chosen. Both are Discussion.

MOVED TO THE DISCUSSION, where they are findings worth keeping: that the
adversary buys donor-blindness at no cost in phase up to the middle weight
and nothing beyond it, so the frontier moves and then stops; and that the
information cost slides a model along the trade-off rather than moving it.
The numbers above support both and the Discussion can say so.

FULL PER-ARM FIGURES, from each arm's own `benchmark.csv`
(donor  / mixing  / phase  / family ):

`dab7_kl1` 0.5837 / 0.7183 / 0.7337 / 0.9829
`dab168_kl1` 0.5188 / 0.6043 / 0.7346 / 0.9820

`dab336_kl1` 0.5277 / 0.6530 / 0.7146 / 0.9779
`dab7_kl30` 0.5389 / 0.7381 / 0.6791 / 0.9841

`dab168_kl30` 0.3975 / 0.5129 / 0.6033 / 0.9565
`dab336_kl30` 0.4154 / 0.5474 / 0.5922 / 0.9553

NOT WRITTEN: the knob names, which are Methods' vocabulary; Fig.~1's
legend carries each arm's two values.

OPEN: "registered in its configuration file before
training" is checkable only if the repository is public. Code availability
has to be real before this sentence is.



**[2] WAS MERGED IN HERE, 2 November 2026**, on AW's ruling. Its
prose is deleted rather than kept, because every number in it is waiting on
the unified scoring run. What it has to carry is below.

ALSO CARRIES A1, A2, A3, A4, A5, A6, E3. SECOND FIGURE: Fig.~3.

WHAT THE SUBSECTION STATES, once the numbers land: ELAJ against nine
methods on the same held-out donors --- a sixteen-component principal
component decomposition, scVI, scANVI, Harmony, Scanorama, and four
pretrained foundation models. Inductive methods fitted on training donors
and applied to held-out ones; the rest reported as transductive. Supervision
declared per method, and ELAJ's is menstrual phase.

REGISTER, settled: flat. The deleted draft opened "a representation that
forgets donors is easy to build and worthless", asserted "width is not what
produces this", and called the disease figure a result about the disease.
All three are Discussion. A4 is stated as a fact --- the foundation models'
dimensions and their phase figures side by side, reader draws the inference.
A5 gives all four figures so the ordering is visible without a word like
"matched" doing the work, with the supervision column beside it.



EVERY FIGURE BELOW IS SUSPENDED pending the unified
run. `audit/NUMBERS.md` traced each one on 2 November:

0.4712 (study mixing) is the **train split**
(`p1_dab168_kl1_train`). Held out it is 0.6043, against scGPT's
0.6284, so "far better than anything else" does not survive as written.

0.7053 and 0.6971 (scVI, scANVI phase) are the
`fm_*` runs' figures; this arm's own file gives 0.7017 and 0.6943.
Both are valid, from different runs, and may not be quoted together.

0.9841 (cell family) is `p1_dab7_kl30`'s. This arm
is **0.9820**.

0.9868 is `scvi / knn-agreement / cell family` ---
a different method on a different test. PCA's cross-donor family in this
arm is 0.9865.

0.3787 and 0.4486 are **per-cohort** figures
(`disease-xdonor / marecko_2024`), not pooled, and ours is the train
split. Pooled, this arm is 0.3364 against scFoundation's 0.4024. The A6
claim holds either way; the numbers change.

Harmony and Scanorama have no valid source at all. Their
only rows are `r8_all`, which scores ELAJ at phase 0.1161 and PCA
at 0.2856 on a third of the cells.



E3 STILL HAS NO HOME. The scIB batch metrics are
degenerate here --- `ilisi_knn` exactly 0.0000 and
`pcr_batch` exactly 1.0000 for PCA, scVI, scANVI and ELAJ alike,
`kbet` 0.000--0.025 for all --- which is why study is measured by kNN
purity. In a flat register it fits as one more measurement sentence here, or
it goes to Methods. A scIB-literate reviewer will ask.



COVERAGE. From this point on, cross-donor agreement
is reported at t=1 --- every labelled cell with at least one cross-donor
neighbour, 88.2% of them --- with the coverage figure beside the scalar and
the threshold curve as the robustness object. t=1 is the maximum-coverage
choice and the one that does not preferentially keep well-mixed cells.
Methods' **Cross-donor agreement** still describes the single-scalar
version and has to be rewritten.

---

## [2] Reading 1.58 million cells as sixteen numbers

CARRIES C1. FIGURE 1e--g.

THE PIVOT OF THE PAPER, and the licence for everything after it. Once the
model is fixed nothing is being selected, and the metadata read below was
never an input, so there is nothing a held-out split protects against for
these labels and all 1,577,728 cells can be embedded and read together.
Menstrual phase is the exception, governed by the head.

STATE PLAINLY what was and was not given to the model. Every claim in
[4] and [5] depends on that line.

C1: cells group by what they are rather than where they came from.
Stromal cells from five tissues land together; most cells in each region
carried no cell-type label at all, so a per-family plot could not have
shown this. Claim stays at the level the approximation supports --- the
model groups largely by cell type and each region roughly represents one.
No purity percentages.

→ hands on: what does the geometry do with time?

---

## [3] The menstrual cycle through ELAJ

CARRIES C3, and C2 NOW ONLY THROUGH FIGURE 5. THE HEADLINE.

**PARAGRAPH 3 CUT 2 November 2026 on AW's ruling, and he is right on
the statistics.** The cut paragraph reported
`over_scatter`: centroid distance over the mean of the two groups'
root-mean-square radii. That denominator describes a cloud only if the cloud
is roughly a filled isotropic ball. If a group's cells sit on a shell, a ring
or an elongated ridge, its centroid falls in a low-density region and the
r.m.s.\ radius is not a width of anything. Three further ways the ratio
misleads, none of them visible in the number: a bimodal family inflates the
denominator and deflates the ratio; the metric is Euclidean on the raw latent,
whose dimensions do not carry equal variance; and separation along a direction
of small scatter scores the same as separation along a direction of large
scatter. AW: "the numbers are a weak representation of the information".

WHERE C2 LIVES NOW: Figure 5, as per-cell-type panels rather than a bar of
ratios. The ratio panel inherits every objection above, so it is replaced
there too. See that figure's note.

C2 GETS NO NUMBER. AW's ruling, 2 November: "I don't want to add more
calculations anymore. We've done enough. We'll add more only if the reviewer
says we need to or if it's wrong." The robust statistic would have been
cross-donor phase agreement within each cell family, which is not computed
and will not be unless a reviewer asks. Figure 5's panels carry the finding.

FIGURE NUMBERS CORRECTED HERE: the cycle is Figure 5 in
`06-display-items.tex`, not Figure 2, which is the frontier. [1] still
points at "Fig.~1b, c" for the frontier and should point at Figure 2; left
alone because [1] is suspended pending the unified run.

PARAGRAPH 6, donor locality, CUT. It duplicated Methods, where
**Cross-donor agreement** already states "between a quarter and
three-fifths belong to the same donor depending on the label, 37% for
menstrual phase" and "twenty to fifty times over-represented". In Results
it spent 40 words restating the justification for an estimator the reader had
just been sent to Methods for. The figures still must not colour by donor as
if spread were a result; the 54-fold enrichment is in
`audit/NUMBERS.md`.

"ANY SINGLE DIMENSION" CORRECTED TO "THE SINGLE BEST-MATCHED OF THE
SIXTEEN", on AW's approval. The statistic is the maximum |r| over the
sixteen dimensions, so "any" read as "all of them". It is also why the
four controls sit at 0.14--0.34 rather than near zero.

ORDER, after AW's ruling that importance should drive it: setup, then the
closed cycle, then the magnitude, then the bound on the magnitude, then the
external corroboration. The closed trajectory was fifth and is now second ---
it is the finding nothing else in the literature shows on this tissue,
whereas the agreement scalar properly belongs to the field comparison and
appears here as magnitude. Paragraph 3 bounds paragraph 2 so it must follow
it. Nothing was rewritten to reorder; the paragraphs moved whole.

NOTE ON THE PREMISE: no NMI or Nature guideline in
`Nature_websites/` says anything about ordering Results by
importance --- all seven were searched. Eye2Gene, one of the five NMI
Articles sampled for register, runs workflow order with its headline in the
second subsection. So the ordering is ours to choose.

290 words at the first seed, 232 after the centroid cut and the donor cut.

SEEDED 2 November 2026, every figure re-derived through
`audit/NUMBERS.md`. Flat register: no sentence here says what any of
it means. Four readings belong in the Discussion and are listed below.

**TWO CORRECTIONS TO THIS NOTE'S EARLIER CONTENT.**

(1) The displacements are **not** "identical across both frontier
arms". Stromal and epithelial are (1.0677 vs 1.0685; 0.9824 vs 0.9899), but
endothelial moves 0.3918  0.5429 and immune 0.3409  0.2861. What
replicates is the **ordering** and the gap between the two pairs, which is
what the claim needs; the prose now says exactly that and no more.

(2) The donor enrichment is **54**, not 14: agreement
0.327 against chance 0.0060 over 269 donors and all 1,577,728 cells at
k=100 (`Outputs/validate/p1_dab168_kl1_full/`). The 14 in
the figure notes is a 60-donor single-cohort subsample and must not be quoted
as a corpus figure.

FOR THE DISCUSSION, not here: that one linear map over the whole latent,
never given cell type, cannot have manufactured a four-way split by cell
type; that with 34.5% of the chance-corrected phase signal being the
head's, "the cycle was recovered" is a weaker claim than "the cell-type
structure of the cycle was recovered"; that stromal and epithelial cells are the two compartments
that remodel across the cycle and the two that move; and that the progesterone
and pseudotime correlations are external corroboration of the axis.

THE CONTROLS ARE IN THE SAME SENTENCE DELIBERATELY.
0.47 is a best-of-sixteen statistic and the negative controls reach 0.34 under
the identical procedure, so the margin is real and small. Quoting 0.47 alone
would be the kind of number a reviewer reproduces and then distrusts.

NO CLAIM ABOUT THE CIRCULAR BRANCH. Every
`circular-linear` row in `validation.csv` is `nan`, so
the closure in Fig.~2 is read off a cyclic colour map on the Gaussian latent
and is qualitative. If the circular branch is to carry any weight, that
measurement has to be made first.

DAY VALUES ARE ONE COHORT, 60 DONORS, ONE DAY EACH.
Stated in the prose rather than footnoted. Days 20, 24, 25 and 28 are absent
entirely.



**REGISTER CHANGED 2 November 2026, checked against five NMI
Articles with full text** (PlantRNA-FM 2024; deep latent variable path
modelling 2025; GEMS 2025; COMET 2025; Eye2Gene 2025).

WHAT THE CHECK FOUND. NMI Results prose is number-dense: 3.2 to 22 numeric
values per 100 words. AW's reading --- numbers in the figures, adjectives in
the prose --- is not the NMI norm, and my first seed at 8--9 per 100 words
was already mid-range. But his complaint about density was right and the
cause was different: my numbers were **unattached**. "was 1.07 for
stromal cells, 0.98 for epithelial" is four bare values with no verb of
finding, so the reader has to redo the comparison.

THE PATTERN THE READABLE PAPERS USE, and the one adopted here: the claim is
in words, the number sits in a parenthesis or a subordinate clause, and a
figure panel is named. COMET, the lowest-density of the five: "was strong,
indicating that COMET can make highly accurate predictions in small cohorts
with high-dimensional data (r = 0.868, 95% CI [0.825, 0.900],
P = 3.9  10^-53, r.m.s.e. = 16.0) (Fig.~2c)". Eye2Gene:
"attained an overall top-five accuracy (81.7--86.0%)".

I ALSO OVER-FLATTENED. All five interpret inside Results --- GEMS:
"enabling accurate prediction of test data point labels through simple
memorization"; COMET: "which may contribute to its superior performance".
Springer's "do not interpret" is the generic guide and NMI's own Articles
do not read that way. The line kept here: **the immediate reading of a
number stays in Results; the argument about what it means for the field goes
to the Discussion.** Four such arguments per subsection are still parked in
these notes.

DENSITY NOW: [3] 8.3 per 100 words, a figure reference every 124 words;
[4] 12.9 and every 98. NMI's own range is 3.2--22 at one reference per
150--200 words, so both sit inside it.

HEADINGS CONFIRMED, not changed: every heading in all five papers is a
claim rather than an activity --- "Eye2Gene generalizes across IRD
clinics", "COMET accurately predicted days to the onset of labour",
"PlantRNA-FM reveals superior performance". The placeholders here are
already in that form.

→ hands on: time is in there. What about the disease?

---

## [4] Disease signal, and where it is not

CARRIES C4 and C5 THROUGH FIGURE 4 ONLY, and C6 in prose. FIGURE 4.
235 words.

PER-STUDY SIGNIFICANCE NUMBERS REMOVED, on AW's standing ruling of 2
November: "there is no reason to look at per study numbers for any metadata
in the latent space because we already assumed that the latent mixes studies
properly. So per-study numbers are a way of shooting yourself in your own
leg." He is right, and the sharpest version of why is a number we already
have: restricting the test to one cohort cuts the donor count from 269 to
sixteen, eighteen and two, and at sixteen donors the permutation null itself
reaches 0.42. The per-cohort figures (p=0.3433, 0.0697, 1.000) were
therefore undetectability, not absence, and printing them would have handed a
reviewer "no cohort is significant" as if it refuted our own pooled 0.3364.
They are recorded in `axw1008/docs/paper/CROSS_DONOR_ESTIMATOR.md`
and nowhere in the paper.

**C4 AND C5 ARE NOT THE SAME THING AND STAY.** Re-running a
significance test on a subset destroys power. Asking whether a **pattern**
reproduces in an independent cohort is external validation, which is why
paragraph 3 survives the ruling: it reports replication, not stratified
inference, and it carries no p and no magnitude.

THE UNDERLYING CONCERN IS NOT ANSWERED BY DROPPING
THOSE NUMBERS, and belongs in the Discussion. Permuting the donor-to-label
map across all eleven studies breaks the label--study association, so the
pooled null never sees whatever study structure remains in the latent. The
bound on how much that can matter is our own study-mixing figure, 0.6043:
if study were fully removed the concern would be void, and it is not fully
removed. The correct fix is a permutation stratified within study, which
keeps all 269 donors and the label--study link together. Not being built,
per AW's ruling of 2 November that no further calculation is done unless a
reviewer asks. So: stated as a limitation, bounded by 0.6043.

**THE `over_scatter** RATIOS ARE GONE FROM HERE TOO`, with
the [3] paragraph they matched: a centroid distance over a root-mean-square
radius is sound only if the cloud is a filled isotropic ball. C4 and C5 are
now read off Fig.~4b and 4c with no magnitudes. No robust replacement exists,
because the cross-donor estimator breaks down by study and not by cell
family, and a per-compartment figure is therefore not computable without the
per-study split AW has just ruled out.

ORDER: the weak-but-real signal first, because the negative cannot be read
without it; stage and grade second, as the most disruptive finding here; the
compartment result third, because it carries no numbers.

STAGE IS SIGNIFICANT ON THE WHOLE CORPUS AND NOT ON
HELD-OUT DONORS, and both are in the prose. 0.332 at p=0.005 against
0.1313 at p=0.3035. That contrast is train against held out, not study
against study, so the ruling above does not touch it. Any wording that says
stage carries nothing **anywhere** contradicts `validation.csv`.
The Discussion reading, per AW: not recoverable from this corpus at this
donor count, never "not biologically real". The whole-corpus figure is the
memorisation pattern E1 documents for donor-constant labels.

HELD-OUT DONOR COUNTS ARE SIXTEEN AND EIGHTEEN, not 58 and 60. The larger
pair are the whole-corpus counts and belong to 0.332 and 0.0263. An earlier
seed attached the corpus counts to the held-out numbers.

→ hands on: which parts of the model are load-bearing?

---

## [5] What the latent needs in order to work

CARRIES D1--D6, B2, B3. FIGURE 5.

AW: "these are the results that a true ML researcher would actually want
to read properly. The fact that we have them and we want to publish them is
itself a huge thing for a paper like ours to do." So this subsection is
written for that reader and is not compressed to make room elsewhere.

FIVE SINGLE-KEY ABLATIONS against one base, predictions registered in each
config before the runs started, 6 of 11 bands landed, misses reported.

D1 FIRST AND MOST PROMINENTLY, because every reported arm is
semi-supervised and a reviewer will ask whether the cycle result is the
supervision played back: removing the phase head drops cross-donor phase
0.7346 to 0.4812. Both values are already chance-corrected, so the ratio
is the split: the architecture supplies about 65.5% of the signal, the head
34.5%. CORRECTED 5 November; the earlier 69.5% head figure subtracted
chance a second time.

D2, THE SURPRISE: the same head is a regulariser. Without it
`train_nb` falls 0.4140 to 0.3772 while `val_nb` rises
0.4083 to 0.4256, diverging from epoch 1.

D3: ECS traverses the frontier rather than expanding it --- removing it
improves every biology axis and worsens every cost axis, which makes it the
same kind of knob as `w_kl_gauss` rather than an independent gain.
Best shown by plotting it ON Figure 1b's frontier.

D4 statistics are a phase mechanism (phase -0.096, family -0.002).
D5 the sentinel is load-bearing for study mixing (0.6043 to 0.6260).
D6 random grouping costs disease most, -20%, in the arm with the best
reconstruction in the project.

B2 HERE RATHER THAN WITH THE FRONTIER, per AW --- it is something we found
out about the model, not something the model found out about the data: a
discriminator driven to chance is not evidence that the latent is
study-free. Adversary loss correlated +0.883 with donor kNN at m3 and
+0.890 with study kNN at m2_cls40; both should be negative if the term
worked. B3: discriminator capacity was the cause, not batch composition.

**Adversarial study removal head** in Methods points forward to this.
If B2 is cut, that pointer goes with it.

---

## [5] What the latent needs in order to work

FIVE subsections now, not six: [2] "against the field" was merged
into [1] on 2 November. ~2,000 words, 24 findings carried by six figures.
Overlap between [3], [4] and [5] is expected to move once prose exists.

This block was `textcolor\elajmuted\` and rendered into the PDF as
though it were prose, which also put "2,000" and "24" in front of
`verify_numbers.py` as unsourced figures. Scaffolding belongs in a
note.

AW to retitle the five headings; NMI wants the finding, not the activity.

---



---

## Closed subsections: the notes their tex no longer carries

Moved out of `02-results.tex` on 6 November, when each was closed. The
rule is that a finished subsection carries no note in the manuscript.

### [2]

THE LICENCE FOR EVERY WHOLE-CORPUS NUMBER THAT FOLLOWS, which is why it
states what the model was given before it states any result. AW's rule, 6
November: a label the model never received cannot leak, so held-out protects
against nothing for it.

- C1'S CROSS-TISSUE CLAIM IS WITHDRAWN. `RESULTS_STRUCTURE.md` had "stromal
cells from five tissues land together"; all five annotation columns in the
corpus are endometrium-only, so there are no labelled stromal cells outside
it. The coverage fact replaces it and is a finding of the same kind as
`[4]`'s: the public record cannot answer the question.

- REGISTER, calibrated against scGPT (Nat Methods 2024), whose main text
quotes AvgBIO 0.821 from its two-batch dataset while its eighteen-batch result
is 0.504 in Supplementary Table 3, and which calls the whole "state-of-the-art
performance on batch correction". Biology stated plainly here; study
separation reported honestly in `[1]`.

- NO PURITY PERCENTAGES, per the standing ruling. CARRIES C1. FIGURE 4a, 4c.

### [4]

AW'S ARGUMENT CHAIN, 6 November, and the prose is his. Four bracketed
tasks filled: ELAJ's held-out figure, the arm check, the baseline numbers,
and the called-out models.

- ARM CHECK: 0.1286 is `wholecorpus_p1_dab168_kl1` and 0.1114 is
`_kl30`, so B hi and B lo were the right way round as written.

- GRADE NOT CLEARING AT 60 DONORS IS NOT REPORTED. Severity is the variable
the claim is made on, and one of its two source vocabularies falling short of
power is a limit of that test rather than evidence against the claim.
Hedging on it would weaken something true.

- TWO NUMBERS WERE DROPPED, not for being wrong but for being unquotable.
scVI's merged severity is +0.0789 and its grade is -0.0789, so the audit
cannot tell which a reader is being shown; scANVI at 0.0759 makes the same
point unambiguously.

- CARRIES the staging result. FIGURE 4h, 4i. Detail in RESULTS_NOTES.md.

### [5]

CARRIES A6 and the disease row of the field table. FIGURE 4g. Per-study
disease rows exist and stay out, on AW's ruling of 2 November: inside one
cohort the test has 16, 18 and 2 donors and the benchmark marks them FEW
GROUPS, excess is unreadable. Detail in RESULTS_NOTES.md.
