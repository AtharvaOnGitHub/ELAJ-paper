# Methods notes

Scaffolding for the **completed** Methods subsections, lifted out of
`sections/04-methods.tex` on 30 October 2026 so the manuscript source reads
as prose. Subsections still unwritten keep their notes inline, where they
function as the brief; a note moves here when its subsection is seeded.

Each entry records what the subsection is for, what was cut from it and why,
what is verified against the code and what is not, and where it collides with
another subsection. **This file is Claude's to maintain** — it is updated in
the same commit as the subsection it describes, and it is the thing to read
before revising anything.

Order matches the manuscript.

---

## Open items, gathered

Everything below is also stated in its own section; collected here because
these are the ones that need a decision or a measurement rather than a read.

- **Cross-donor agreement** — the rho +0.943 demonstration is deliberately NOT in the subsection and is the strongest evidence we hold for it. Across the six A1 arms, whole-corpus agreement on a donor-constant label ranks almost identically with benchmark donor-kNN recovery: Spearman rho +0.943 for disease status, +0.829 for phase, while cell family — the only label varying WITHIN a donor — sits at +0.371 with a spread of 0.003 across every arm including randomised gene groups. The estimator cuts disease's correlation with donor recovery from +0.943 to +0.429, and `random groups` inverts outright: best of six on whole-corpus disease, worst of six cross-donor. That is a measurement, so it belongs in RESULTS beside the ablations — same ruling as the baseline protocol. Full tables in `axw1008/docs/paper/ABLATIONS.md`. **Still pending AW's review.**
- **Code availability** — TBD by AW's ruling, not blocking the draft. Three infrastructure prerequisites, none of them writing: no public repository for the code (`origin` is a university GitLab course project; `old-repo` a stale GitHub mirror), no licence file anywhere in the tree, and no tags or DOI so nothing identifies the commit that produced the reported arm.

### Closed 30 October 2026

- **Decoder conditioning** — why the reported arm runs `d_study` 16 *and* `lambda_dab` 168. CLOSED: AW's ruling that the rationale for a hyperparameter choice is a Results/Discussion matter, not a Methods one.
- **Reconstruction head** — the droplet-overdispersion claim needed a citation. CLOSED: the claim no longer exists. AW's edit of the likelihood paragraph removed the Poisson justification and left only the statement; `grep -n "Poisson\|droplet"` on the Methods returns nothing. The open item was stale when written.
- **Adversarial study removal head** — what the "October 2026 discriminator change" was. ANSWERED, and it stays only as a caveat that never fires. Commit `58cc532`, 5 October 2026: the discriminator was one 64-unit ReLU layer with dropout 0.1 in every arm from r1 to m4, and became scGPT's `AdversarialDiscriminator` shape — three 256-unit LeakyReLU layers with LayerNorm and no dropout. The same `lambda_dab` through a stronger network is a different pressure on the encoder, so the value does not carry across the change. Every reported arm post-dates it, so nothing in the paper needs the caveat. **Correction while checking this:** there are TWO correlation measurements and I had been conflating them — `+0.890` between adversary loss and **study** kNN at m2_cls40 (the commit), and `+0.883` between adversary loss and **donor** kNN at m3 (`LEVERS.md`). Different arms, different targets, both real.
- **Data availability** — li et al.'s accession. RESOLVED, and it was not a citation problem. The paper (*Advanced Science*, `10.1002/advs.202417528`) is titled "Iron Overload-Induced Senescence and Metabolic Reprogramming in Ovarian Endometriosis-Associated Infertility"; its section 2.3 is "Single-cell Atlas of Follicular Fluid from OEI Patients Decoded by scRNA-seq"; the words "endometrium" and "endometrial tissue" appear zero times and "granulosa" appears 75. The scRNA-seq we used is **pre-ovulatory follicular fluid**, deposited at CNGBdb **CNP0006183**; GSE276193 is the bulk RNA-seq we did not use. Our own metadata agrees independently — the cell types are Granulosa2 (10,270), Granulosa3 (3,445) and 24,155 neutrophils, and granulosa cells have no endometrial existence. AW's ruling is **option 1: keep the study, correct it in the paper, leave the trained model alone** — tissue is a decoder covariate, so relabelling the data would mean retraining, and a corrected CSV would desynchronise the config from the reported arm. Declared in Study selection and in the Discussion's limitations. Accession in the manuscript is now CNP0006183.

--- Spearman rho +0.943 for disease status, +0.829 for phase --- while cell family, the only label that varies WITHIN a donor, sits at +0.371 with a spread of 0.003 across every arm including randomised gene groups. The cross-donor estimator cuts disease's correlation with donor recovery from +0.943 to +0.429, and `random groups` inverts completely: best of six on whole-corpus disease, worst of six cross-donor. That is a measurement, so it belongs in RESULTS, beside the ablations --- same ruling as the baseline protocol. Full tables in axw1008/docs/paper/ABLATIONS.md. If a reviewer challenges the estimator, this is the answer.
- **Data availability** — TWO ACCESSIONS NOT SETTLED. (1) **li_2025:** GSE276193 is that study's *bulk* RNA-seq; its scRNA-seq is in CNGBdb under CNP0006183. We hold 45,803 single cells from it and the screening sheet records the tissue as follicular fluid and mouse ovary, neither endometrium. Verify the h5ad before writing anything --- if it is not endometrium this is a corpus problem, not a citation one. (2) **GSE213216:** accession right, citation wrong --- the PDF on file is Pei et al. 2023, a re-analysis that used it, not the original submission.
- **Code availability** — THREE PREREQUISITES, ALL INFRASTRUCTURE, NONE WRITING. (1) No public repository --- `origin` is a university GitLab course project a reviewer cannot open, `old-repo` a stale GitHub mirror. (2) No licence file: no LICENSE, LICENCE or COPYING in the tree, so the code is technically all-rights-reserved, which contradicts this statement. (3) No tags and no DOI --- `git tag` is empty, so nothing identifies the commit that produced the reported arm. A GitHub release at that commit through the Zenodo integration mints one if we want it; the statement does not need it.

---

## Study selection

DONE. Establishes the corpus as a complete published record for endometriosis rather than a convenience sample, and states what was and was not done to the data --- identifiers unified, ontologies applied, expression left alone.

## Gene vocabulary

DONE. Settles the feature axis: what the genes are called, then which of them the model reads --- chosen from pathway annotation without looking at expression, which is the defence against having picked genes that flatter the model.

## Gene tokens

DONE. What a gene looks like to the model: an identity embedding plus a count scaled along a direction that gene owns, kept separable so the next passage can replace one half and leave the other.

## Unmeasured genes and the sentinel

DONE. Three states rather than two, and why the third cannot be recovered from a cell at all without knowing which study it came from.

## Pathway gene grouping

DONE. The cost argument and the inductive-bias argument as one decision, because the partition arrived free with the vocabulary. Still open: 1.08M and 47.6M are formula estimates, not measured --- the log reports only the whole model at 1{,}883{,}986.

## Group encoders

DONE. What happens inside one pathway, and the hypothesis that order statistics recover part of what a single learned query averages away --- described precisely enough that ablation C-4 means something.

## Cell aggregation

DONE. The second narrowing, and what the stage is for: the groups were read independently, so something has to relate them. The lossy-readout objection is raised a second time here because the same remedy answers it, and because the measured loss is worse at this level than at the group one.

## Latent space

DONE. The bottleneck. Width is stated and its justification deferred to Results, which is the right place for it --- the frontier is a result, and Nature keeps results out of Methods. The circular branch is still not mentioned; the code supports it and no reported arm uses it. Two sentences if a thesis reader would notice the absence.

## Decoder conditioning

PURPOSE: what the latent is relieved of, and the one omission every
disease claim rests on.

DROPPED FROM THE PAPER ENTIRELY: the `+0.883` correlation between the
discriminator's loss and donor recovery. It is a measurement, so Methods is
the wrong place for it either way, and it diagnoses the undersized
discriminator retired in October 2026 rather than anything a reported arm
does. No forward pointer remains.

DROPPED IN THE EDIT, listed so the choice is visible rather than lost: the
encoder sees none of the covariates; the decoder needs a study id at
inference on a new study, though the encoder and latent do not; scVI as the
precedent and the citation that comes with it.

NOT WRITTEN, implementation rather than method: a decoder built to expect a
covariate and handed nothing raises rather than falling back to a narrower
context; the three covariate tables together hold 1{,}968 parameters.

OPEN: the reported arm runs `d_study` 16
*and* `lambda_dab` 168, which the commit history frames as two
opposite-end fixes for the same contradiction. Needs one sentence on why
both; the decision is not recorded anywhere I could find.

## Reconstruction head

PURPOSE: plan item 13 --- gene queries against a cell context, and
why not a per-gene output layer, argued in parameters --- plus item 14's
likelihood. Every passage now answers "what does the paper claim that
needs this".

CUT, and the reason is the same for all three: nothing the paper claims
depends on them.
(a) THE RANK ARGUMENT, two paragraphs on `{rank}(Q)` bounding
the profile space at 64 of 15{,}496. No arm tests it; a1_randgroups
permutes group membership, which is the partition and not the projection.
And it is a liability: `val_nb` 0.4024 against a study-mean
baseline of 0.4315 is a 6.5% improvement, so advertising a 64-dimensional
ceiling hands a reviewer a candidate explanation for our weakest number
that we cannot rule out. The per-group choice is kept, argued directly
instead.
(b) THE QUERY BIAS becoming a per-pathway offset under per-group
projections while a shared one leaves it inert. True and neat, but it
justifies nothing we report.
(c) PANEL-RELATIVE PROFILES --- normalising over the measured genes makes a
predicted profile relative to the study's panel, so one cell state through
two panels gives two sets of proportions. No claim in the paper compares
reconstructions across studies; the comparisons are all on latents.

TO SUPPLEMENTARY NOTE: the full forward pass with every shape, and what
each of the six learned objects uniquely holds. Drawn from
docs/walkthrough/15-flow-reconstruction.md.

DROPPED ON AW'S RULING, do not re-propose: the no-cell-index clause. My
case was weak and the rebuttal is right --- nobody asks whether a model
leaks to its decoder, and the evidence the bottleneck holds is already the
latent's own metrics (cell-family kNN 0.994 on sixteen dimensions is not
what an empty latent produces), so an architectural guarantee adds nothing
a reader needs. The code keeps the record: run 49817807 concatenated the
encoder's per-cell group summary into the query and both latent branches
collapsed to zero information.

COLLISIONS: the old no-cell-index clause was *Bottleneck integrity*'s
subject and is one clause here; sentinel exclusion from the loss is under
*Unmeasured genes and the sentinel*; the reliance measurement belongs
to *Bottleneck integrity* and only its architectural reason is given
here; masking depends on a subsection that does not exist (item 22b in
METHODS_STRUCTURE.md).

NOT WRITTEN, implementation: the per-group initialisation and its
`sqrt{44}`; the algebraic fold that avoids `{}918` MB of activations
per forward at batch 256; fp32 forcing under bfloat16 autocast; the three
index spaces a gene lives in; and two dead ends --- `b` is one constant
across genes that the normalisation cancels exactly, and
`{w}^ W_v` collapses to a single 112-number vector, so 7{,}232
parameters realise 112 degrees of freedom.

OPEN: the droplet-overdispersion claim needs a
citation, and the parameter figures are arithmetic from the code rather
than read from a log.

## Adversarial study removal head

PURPOSE: the term that makes `lambda_dab` a knob, so the one
head the paper's central result rests on.

AW REMOVED, as artefacts of our own earlier errors rather than method: that
a defeated discriminator is not evidence of an invariant latent, with the
`+0.883` correlation; and that single-study batches do not handicap a
row-wise discriminator. Both answer objections to designs we no longer run.
The `+0.883` figure now appears nowhere in the paper, and
*Decoder conditioning*'s forward pointer to it has been dropped
rather than redirected.

NOT WRITTEN, deliberately: the discriminator's parameter count, since it is
discarded after training and is not part of the released model; and the
LeakyReLU slope 0.01 and the circular inputs arriving as `(,)`
pairs, which matter only when `n_circular> 0` and no reported arm
has it.

OPEN: `lambda_dab` is not comparable across
the October 2026 discriminator change, so any number quoted from an arm
before it must say so.

## Elastic cell similarity head

PURPOSE: the anti-collapse pressure, and the one term whose sign has to
be stated or a reader will assume the opposite. The paper needs it because
the A1 ablation shows removing it improves every biology axis and worsens
every cost axis --- a frontier-traversing knob rather than an expanding one
--- and that result is unreadable without knowing which way the term pushes.

HEADING: withdrawn. The subsection now sits inside AW's framing of the
decoder as four heads, which makes "head" the consistent label even though
this term holds no parameters.

NOT WRITTEN: the cross-study buffer variant, built and never used by a
reported arm; and the self-pair handling, which differs from scGPT's by a
factor `(B-1)/B`, or 0.4% of the effective weight at batch 256.

## Menstrual-phase head

FOR THE DISCUSSION, cut from here as a significance claim and because it credits the wrong component --- phase is endometrial physiology, not endometriosis, and what tailors ELAJ to the disease is the corpus and the pathway vocabulary: *supervising cycle phase is what makes this a model of endometrium rather than a generic single-cell autoencoder*.

PURPOSE: the fourth head, argued as a design choice with a measured
benefit. Earlier drafts hedged in every paragraph as though supervision
needed excusing; the argument is that phase is real biology the rest of the
objective cannot reach, and that the adversarial head would remove it if
nothing asked for it.

THE REGULARISER CLAIM IS MEASURED: on a1_nophase, `train_nb` falls
0.4140 `->` 0.3772 over eight epochs while `val_nb` rises
0.4083 `->` 0.4256, diverging from epoch 1. Removing the head also
costs every biology axis, phase worst but cell family and disease too. The
numbers belong in *Ablations*; stated here only as "measured by
removing it".

VERIFIED: 512{,}101 of 1{,}161{,}472, from the benchmark log's
"Harmonised menstrual phase" line on the train split.
NOT verified: four of eleven studies, and the
91-of-184-donor figure registered in METHODS_STRUCTURE.md item 20, which
stays out until it is read off a log. Coverage differs by split --- val is
101{,}479 of 190{,}976, 53% against train's 44% --- so any figure quoted
must name its split.

NOT WRITTEN: weight 40 and label smoothing 0.05, which belong in the
objective's weight table; that the head reads `mu_gauss` alone
rather than the circular block, indistinguishable from "the Gaussian
means" while no reported arm has a circular branch; and that the head is
discarded after training.

COLLISION: the 34.5% figure for how much of the chance-corrected phase
signal the head supplies is a result and belongs in *Ablations*.

## Composite objective

PURPOSE: how the four heads combine, as one equation inside the
story. Two earlier drafts failed in opposite directions --- one discussed
the objective at length without ever writing it, the other became two
display blocks and a symbol table with no argument in them.

SIMPLIFIED FOR THE REPORTED ARM, all three verified absent from
p1_dab168_kl1: the circular branch's KL at `w_kl_circ` 2
(`n_circular` 0), the drain's KL charged at the Gaussian weight
(`d_drain` 0), and the contrastive term `w_cce`, which needs
two augmented views. `composite.py` carries all three, so if any
reported arm ever has one, this equation is wrong for it.

NOT WRITTEN: the per-term definitions, since each is the standard loss for
the head that owns it and those subsections give them; that
`{L}_{dab}` stays in the graph because an untrained
discriminator reports chance whatever the latent holds; and the
fourteen-fold volatility figure behind the selection sentence, which is a
measurement and belongs in *Checkpoint selection* if anywhere.

HISTORY, kept only because it makes older logs readable: before 28 September
2026 the per-cell terms were not divided by `G`, so each silently carried a
weight of `G_meas` --- `lambda_{dab} x w_{dab}
 x G` was about 70 at v1_pool, 140 through r4 to r8 and 1{,}400 at r2,
and `w_cce` 0.05 was an effective 700. Every reported arm post-dates
the fix, so the paper needs no comparability note.

MERGED IN, AW's call: *Latent information cost* was a separate
subsection and is now the one paragraph above. The KL is a standard VAE
term, so only the three things a reader cannot infer survived --- that it is
summed over dimensions and averaged over cells, the anneal that defines
`beta(t)`, and `w_{kl}` as knob two.

DROPPED IN THAT MERGE: the free-bits floor of 0.25 nats per dimension,
which the project believes inert on this corpus and which I never
re-measured on the reported arm --- it was a paragraph reporting that a
guard does nothing, and it goes to Code availability with the rest of the
configuration; and the measured case for dividing by `G`, which is that
undivided the Gaussian branch ran at an effective 469 and the circular one
at 1{,}875, against the 1--20 range where posterior collapse is a
documented risk, and that run 50132670 collapsed exactly so, circular
branch first. That evidence belongs in a rebuttal if a reviewer presses on
the division.

VERIFIED from `composite.py` and the reported arm's config:
`beta_max` 0.5, `warmup_fraction` 0.05,
`w_kl_gauss` 1.0, `free_bits` 0.25. The module
docstring still says the KL "ramps 0 to 1 over the first 20%", true when
both were hardcoded and now stale --- a code fix, not a paper one.

SOURCE: `composite.py` 300--407. Thesis §Objective is revised beyond
use --- four terms, none of these weights.

## Cross-donor agreement

PURPOSE: the paper's central measurement, and the reason the obvious one
fails. Opens on AW's two lines about the single biopsy, which are the right
entry point. Absorbs plan item 27, the permutation null, which has no
independent existence -- it defines what the agreement number is compared
against.

RE-SEEDED 30 October 2026, because AW asked what ties the claim together and
the honest answer was nothing. The old version asserted "a cell's nearest
neighbours are predominantly other cells from the same donor" and stopped.
The mechanism now runs as four steps: a single biopsy makes each label a
donor property; so asking about labels is asking about donors; so every
same-donor neighbour is an automatic match; so plain agreement rests on a
floor equal to the same-donor share -- and that floor is one the model can
raise by memorising donors.

MEASURED FOR THE RE-SEED, from `p1_dab168_kl1_full/donor_adjacency.csv`,
whose diagonal the code keeps for exactly this purpose. Decomposing the one
matrix two ways, k=100:

| label | plain | cross-donor | same-donor share | free share of the agreement |
|---|---:|---:|---:|---:|
| menstrual phase | 0.8418 | 0.7502 | 36.7% | 43.6% |
| disease_status | 0.6311 | 0.4769 | 29.5% | 46.7% |
| Endometriosis_stage | 0.8552 | 0.6287 | 61.0% | 71.3% |
| EndometriosisGrade | 0.5043 | 0.3358 | 25.4% | 50.3% |
| severity | 0.5896 | 0.3732 | 34.5% | 58.6% |

Against a donor-blind chance rate of `sum_d p_d^2`: disease 0.60%, phase
1.11%, severity 1.16%, stage 3.05%. So same-donor neighbours are
over-represented 49x, 33x, 30x and 20x respectively.

**"predominantly" WAS FALSE AND IS GONE.** 36.7% is not a majority, and a
reviewer could have caught it. The replacement claim is stronger anyway: not
that most neighbours are same-donor, but that they are twenty to fifty times
over-represented, and that each one is a free match.

TWO FACTUAL ERRORS OF MINE, FIXED IN THE SAME PASS. (1) "a 254-by-254 table"
-- the matrix is per label and is indexed by patient_id, so it is at most 269
rows, and in practice 269 for disease status, 142 for menstrual phase, 118
for severity, 60 for grade and 58 for stage. 254 is the count of true people,
which is not what the matrix is built on. Now written as "at most one row per
donor". (2) "tumour grade" -- it is endometriosis grade; there is no tumour
in this corpus.

VERIFIED against `evaluation/sufficient_stats.py`: `donor_adjacency` k=100
with self excluded; `np.fill_diagonal` to zero before scoring; chance as
`sum p_j^2` over donor shares; excess `(a-c)/(1-c)`, matching
`cross_group_agreement` so the two are comparable; 200 permutations at seed
24; `p` and `p_floor` exactly as written. Per-label neighbour agreement
elsewhere uses k=30 -- the k=100 here is the donor graph specifically.

NOT WRITTEN: that the donor matrix is also what makes the
sufficient-statistics release useful, which is Code availability's; and the
95th-percentile null excess the code also reports, which no result quotes.

ALSO BEWARE, cost me a wrong answer once: in pandas, `df.lt` is the
less-than method, so a column named `lt` is unreachable by attribute access
and comparisons against it silently compare a Series to a bound method.
## Data availability

PURPOSE: mandatory, and no longer than the atlas papers write it ---
no new data, then the accessions. An earlier draft explained the CellxGene
route, listed the two datasets we excluded, and promised not to redistribute
processed matrices; none of that is what this statement is for.

TWO ACCESSIONS NOT SETTLED.
(1) **li_2025:** GSE276193 is that study's *bulk* RNA-seq; its
scRNA-seq is in CNGBdb under CNP0006183. We hold 45,803 single cells from it
and the screening sheet records the tissue as follicular fluid and mouse
ovary, neither endometrium. Verify the h5ad before writing anything --- if
it is not endometrium this is a corpus problem, not a citation one.
(2) **GSE213216:** accession right, citation wrong --- the PDF on file
is Pei et al. 2023, a re-analysis that used it, not the original
submission.

ON RECORD, needs no sentence unless an editor asks: shih_2022's deposit
note says "available from the corresponding authors on request" for its
other materials while the single-cell data sit openly in GSE203191;
garcia-alonso's CellxGene collections are the open component, not the
controlled-access E-MTAB-10287. Both in DATA_PROVENANCE.md.

## Code availability

PURPOSE: mandatory, one sentence, which is what the field writes.
An earlier draft listed what the release contains and pinned four library
versions; the repository carries both.

THREE PREREQUISITES, ALL INFRASTRUCTURE, NONE WRITING.
(1) No public repository --- `origin` is a university GitLab course
project a reviewer cannot open, `old-repo` a stale GitHub mirror.
(2) No licence file: no LICENSE, LICENCE or COPYING in the tree, so the code
is technically all-rights-reserved, which contradicts this statement.
(3) No tags and no DOI --- `git tag` is empty, so nothing identifies
the commit that produced the reported arm. A GitHub release at that commit
through the Zenodo integration mints one if we want it; the statement does
not need it.

ABSORBS by AW's ruling: every hyperparameter, the retired compute
subsection, and *Latent geometry*'s sufficient-statistics rationale.
Versions, verified and not in prose: PyTorch 2.7.1, CUDA 12.6.0, Python
3.12, scikit-learn 1.9.0, pinned in `src/requirements.txt`.
