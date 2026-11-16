# Introduction — paragraph map

**Rewritten 17 November 2026. The 30 October version is discarded**, on AW's
instruction: *"Forget the previous introduction structure."* That file
predated both the guide's pointers and the settled one-line story, and it
spent 390 of its 790 words on clinical background the guide did not ask for.

**Edit this file. Prose follows it, not the other way round.**

---

## The two things this section serves

### 1. The one-line story, at the centre of everything

> In this paper we build a single-cell disease atlas where inductive bias
> replaces pretraining scale, and use that to measure the trade-off between
> removing batch effects and keeping biology on a corpus limited by donors.

**The Introduction's job is to make each clause of that line land when the
reader reaches it.** Every clause needs a premise, and the premises are the
paragraphs:

| clause | the premise it needs |
|---|---|
| single-cell | why scRNA is the resolution the question needs |
| disease atlas | why an atlas, and why for one disease |
| *(endometriosis)* | why this disease is worth the apparatus |
| inductive bias replaces pretraining scale | why a pretrained foundation model is not the answer here |
| the trade-off between removing batch effects and keeping biology | **the confound.** Nothing in the paper means anything before the reader has it |
| a corpus limited by donors | donors, not cells, are the binding variable |

**It is a CASE STUDY, deliberately.** Every framing that centres a *method*
owes a reviewer a second dataset, and there is no second endometriosis
corpus because we used all of it. See `CONTINUITY.md`, *THE STORY OF THE
PAPER*, for the quadrilemma that produced this and the four framings it
killed.

### 2. The guide's pointers, which are the spine

From the 11 November group feedback, verbatim in `REVIEW_FEEDBACK.md`:

> - Intro needs to clear up the story a little more from the foundations:
>   why scRNA / why endometriosis / why disease atlas
> - Intro also needs to say: what other endometriosis studies have shown
>   ... what foundation models are capable of saying on a single disease
>   level and how having a disease atlas on a study beats foundation model
>   approach. (I'd be careful of overreaching here. However, the main
>   message of; **having a disease atlas is a great thing for a disease**,
>   should be very evident)

And from 9 November: *"The 'story' of the paper is unclear (reflects most
strongly in abstract and introduction)."*

**Two things he assigned elsewhere and that must therefore stay out.** The
three reader questions — does this make a great foundation model, are
foundation models useless, would this work on any disease — go to **future
work and limitations**, not here. And *"foundation models are useless"
cannot be written*; only that four of them give no advantage on this corpus.

---

## The register, read off IBDex

IBDex's Introduction is **six paragraphs, 600 words, 15 references**, and
its construction is worth copying exactly:

| ¶ | what it does | its closing line |
|---|---|---|
| 1 | the field's problem as a structural fact, not a complaint | *"Historical data accumulate without becoming a reference."* |
| 2 | why this disease makes that problem consequential | the endpoints *"do not establish whether deep remission restores non-IBD mucosal biology"* |
| 3 | what the field has already shown, then the ceiling | *"The challenge is no longer detecting signal, but measuring the same biology on a scale that persists across studies."* |
| 4 | the analogous problem solved elsewhere, which licenses the approach | *"Molecular atlases can therefore outlive their construction datasets."* |
| 5 | why that solution does not transfer, and the precise gap | the machinery exists; the reference frame does not |
| 6 | what we built, the questions we asked, the contribution stated flat | *"The contribution is not another embedding. It is a frozen patient-scale tissue atlas that converts historical bulk transcriptomes into a reusable molecular reference."* |

**Four rules taken from it:**

1. **Every paragraph ends on a short declarative that lands the point.** Not
   a transition, not a hedge.
2. **The contribution is stated by contrast**: *not X. It is Y.*
3. **One naming sentence**: *"We therefore developed IBDex as a frozen
   patient-scale tissue atlas."* Never "we propose a novel architecture".
4. **The questions are a tricolon that maps onto Results in order**:
   *"we asked whether ..., whether ..., and whether ..."*

Spelling stays British. Register is the NMI reader who knows what a VAE, a
batch effect and a $k$NN graph are.

---

## The six paragraphs

| # | what it does | words | the guide's ask it serves | cites |
|---|---|---:|---|---:|
| 1 | **Why endometriosis.** Common, and diagnosed years late. The biology that would shorten that delay moves on a cycle, so the cycle is not a nuisance variable in this disease, it is the axis the disease moves along. Close on the stakes. | 105 | why endometriosis | 3 |
| 2 | **Why scRNA, and what the studies have shown.** Single-cell has established real things: lesions are not simply displaced endometrium, the unaffected endometrium of an affected person is already altered, immune involvement recurs. Then the ceiling, which is arithmetic rather than anyone's failure: surgical diagnosis makes every cohort tens of donors, assembled one hospital at a time. **Close on the sharpest fact we own: independent cohorts keep landing on the same findings and not one can confirm another, because no two share donors or a cell vocabulary.** | 145 | why scRNA; what other studies have shown | 7 |
| 3 | **Why a disease atlas.** Pooling is the only route to the donor count the question needs, and atlases are how other fields did it. Then Hrovatin: the field's own review says **no one-size-fits-all protocol for atlas building exists**, so a worked context is what is missing. Close on AW's thesis line: **this corpus is not a sample of the field, it is the field.** | 130 | why disease atlas | 5 |
| 4 | **THE CONFOUND, and the gap in the field's own guidance.** Each donor is biopsied once, so menstrual phase is constant within a donor and a per-donor offset is geometrically the same object as a batch effect. Hrovatin's recommended fix is to coarsen the batch covariate to dataset; every example they give is dataset-level, a phenotype constant within a subject is not among them, and the fix has a cost nobody measures, because subject-level variation then simply survives. Close: **donor recovery is not a nuisance we removed, it is the cost axis we report.** | 145 | the trade-off clause of the one-liner | 3 |
| 5 | **Why not a foundation model.** What a pretrained model offers a single disease: one fixed representation, built across tissues and conditions, which cannot be moved. What a disease atlas offers instead: a representation built for this disease's confound, and cheap enough to retrain. **The connective a reader will not infer — a 1.88M-parameter model retrains eleven times, a 100M pretrained model gives one fixed point and no curve, so affordable retraining is what makes the trade-off measurable at all.** | 105 | foundation models at a single-disease level; why an atlas beats that | 5 |
| 6 | **What we built, and what the paper asks.** One naming sentence. The corpus in one line, 1,577,728 cells, 254 donors, eleven studies. Then the three questions as a tricolon mapping onto Results in order. Close with the contribution by contrast, IBDex's device. | 130 | the whole line | 1 |

**Total 760 words, about 24 citations.**

### The lever if the citation budget tightens

The main-text cap is 50 and the Introduction is where most go. The eleven
corpus studies can be cited **collectively** here and individually in
Methods, where references are uncapped.

---

## Decisions AW has to take

1. **"The published record is a record of the believed."** The survey cohort
   behind the delay figure was 85.6\% white and 64.5\% degree-educated, and
   every single-cell cohort in existence is drawn from patients who reached
   laparoscopy, which means having been believed first. It is AW's strongest
   sentence and it is a real selection-bias statement about our own corpus.
   **The draft carries it as one sentence closing ¶2.** It can instead go to
   the Discussion's limitations, or come out.
2. **The pain-bias material is cut, and that is a change.** The old plan gave
   180 words to the misdiagnosis statistics (`hoffmann2001girl`,
   `chen2008gender`). The guide asked for five foundations and none of them
   is this, and `hoffmann2001girl` and `chen2008gender` are not in
   `references.bib` at all. **Cutting it also sidesteps the collision with
   the standing rule**, since those studies' findings are comparisons
   between groups and reporting them needs the word the rule forbids. If AW
   wants the material back it costs ~150 words and two new bib entries, and
   question 1 of the old file comes back with it.
3. **How hard to push on foundation models in ¶5.** The guide said *"I'd be
   careful of overreaching here"* and also that the atlas-beats-foundation
   message *"should be very evident"*. The draft keeps ¶5 about what the two
   approaches can offer and leaves every number to Results.
4. **The Abstract now follows the Introduction.** AW, 17 November, reversing
   his own 11 November ruling. Nothing in this file depends on it.
