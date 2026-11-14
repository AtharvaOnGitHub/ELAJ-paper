# Priority list

**The goal: ELAJ at an NMI reviewer's desk, in the strongest honest shape.**
Rebuilt 11 November, once the paper's story settled. `REVIEW_FEEDBACK.md` is
the contract for the supervisor's register feedback; `CONTINUITY.md` carries
the story, the rulings and how the figures are built.

## The line everything now serves

> In this paper we build a single-cell disease atlas where inductive bias
> replaces pretraining scale, and use that to measure the trade-off between
> removing batch effects and keeping biology on a corpus limited by donors.

A **case study**, deliberately, licensed by `hrovatin2025atlases` saying no
one-size-fits-all atlas protocol exists. Not a framework and not a method
paper: both owe a second dataset we do not have and cannot get. See
CONTINUITY for the four rejected framings and why each died.

The **11 November group feedback** is in `REVIEW_FEEDBACK.md`, verbatim. It
does not reopen the story. It asks for the story to be made legible, and it
overturns three things recorded here as settled.

---

## The display items, settled 11 November

**Four, and the order is the argument's order.** AW overruled the
supervisor's "fig 4 becomes fig 2" with a structural reason: the model has
no credibility on the UMAPs until the frontier has been explained, and the
paper has to say why only one ELAJ arm is discussed before showing what that
arm can do.

| | what it is | change |
|---|---|---|
| Fig 1 | graphical abstract, architecture, frontier, cell-family latent | none |
| Fig 2 | **the frontier** | was Fig 2, stays, but **must stop looking like a benchmark** |
| Fig 3 | **the nine endometriosis UMAPs** | was Fig 4, renumbered |
| Table 1 | every arm | none |
| — | both latents by family and phase | **was Fig 3, goes to Supplementary** |

**Figure 2 is an open design question, not a settled one.** AW: *"it needs
to be a little more interesting and less cold and scientific looking. I
might consider supplementing the frontier plots with some other panels."*
Discuss before drawing.

---

## Tier 0. New analysis. **DONE, 13 November.** Writing can start.

`CLAIMS_LEDGER.md` holds the 30 published claims. `EXPERIMENTS.md` holds the
protocols as X1-X15. **`CLAIMS_SUMMARY.md` is the one to read**: every
experiment in plain language with the claim it tests and the verdict.

**What the paper can now say**, all of it measured:

- composition does not differ between control and eutopic endometrium, 194
  donors, eleven studies -- Dümpelmann's claim confirmed at 3x their donors
- immune cells carry a disease direction that holds on unseen donors, 118
  donors, AUC 0.708 against a 0.481 null, p 0.015
- that direction reads in genes as macrophage-led inflammation, and **four of
  its top fifteen replicate an external cohort's upregulated list at
  p = 4.0e-07**; IL1B is first in Dümpelmann's own classifier's importance list
- four genes in that list have no prior endometriosis report in the corpus,
  Open Targets or PubMed: SIGLEC7, ADAMDEC1, ALPK2, KCNH1
- neither severity readout recovers the surgical grade: an argument that
  rASRM staging is anatomy, not biology
- Huang's claim that disease flattens the cycle does not hold, two ways
- tissue structure is largely absent from the latent, which is the decoder
  conditioning working as designed

**Still open and NOT blocking**: X13 marker signatures, unscoped; X15 group
embeddings, unscoped. Both are Supplementary-level.

## Tier 0 as it was framed

- [ ] **The claims axis.** AW, approving it: *"We need to lay out all the
      major claims of each dataset and see if we can support or reject them
      in our architecture. That is a results axis we hadn't considered
      yet."* Not a citation exercise and not a literature table. It is a
      new axis of results, and it gates the Abstract, the Introduction, the
      Discussion's third section and part of Results.

      **Every dataset in the corpus is accounted for even where its claims
      go untested.** AW's condition.

      The order of work, AW's: **claims laid out by paper → pick what is
      most relevant → scripts and inferences.**

      **Step 1 is done.** 30 disease claims from the ten corpus papers are
      in `CLAIMS_LEDGER.md`, read from the PDFs. Protocols and status live
      in `EXPERIMENTS.md` as X1 to X15. **Step 2, picking what is most
      relevant, is with AW.**

      The standing rule "no per-study numbers for metadata in the latent"
      still binds. Testing a published claim against the pooled corpus runs
      the other way and is allowed; a reproduction needing a per-study
      latent breakdown is out.

      Nothing in this axis needs a GPU or a retrain. The two prerequisites
      are **X1 label transfer** and **X2 fetching `vocabulary_v1.json`**.
- [ ] **Group embeddings, for Supplementary.** AW's own addition. Needs
      work and possibly HPC time. Not scoped yet. Tracked as X15.

## Tier 1. The sections. **RESULTS IS DRAFTED, 13 November.**

**Five subsections, 1,650 words, both auditors green, zero overfull.**
Delivered to AW's supervisor as `changesets/ELAJ_results_2026-11-13.docx`,
a wholesale replacement with **nothing to re-insert by hand**: the section
is now maths-free, so italics, subscripts and superscripts all survive the
Word paste.

| subsection | words |
|---|---:|
| Batch effects and biology have a measurable trade-off | 227 |
| Biology is an emergent property of training | 364 |
| Endometriosis severity is not biologically rooted | 268 |
| Immune genes identify endometriosis | 394 |
| Ablation studies | 397 |

**How it was written is in `REGISTER.md` and it should not be re-derived.**
Eleven rules, each with the correction from AW that produced it, and the
working loop: AW sets the header, I produce a numbers sheet saying what each
value will and will not support, AW writes the opening or tells me to, I
write the rest, AW edits the tex and I fix only spelling, grammar and tense.

### What is next, in order

1. **The five figures.** `FIGURES_NEEDED.md` says what each must show, why
   prose cannot, and roughly what it might look like. Two are main-text
   candidates and take the paper to NMI's six-item cap exactly.
2. **The Abstract.** AW's ruling of 11 November: it goes before the
   Introduction, because the Introduction has to expand something and 150
   words is the cheapest place to find out whether the story holds. It now
   has to carry the claims axis, which did not exist when the order was set.
3. **The Introduction**, to the supervisor's spine: why scRNA, why
   endometriosis, why a disease atlas, what other studies showed, what
   foundation models can say, what we do.
4. **The Discussion.** Deferred until figures were settled; now unblocked.
   Three comparisons, plus limitations. **Four pieces of Results material
   were moved here and must not be lost**: the ρ = +0.721 donor-memorisation
   asymmetry, Huang's overturned cycle claim, scIB's saturation on this
   corpus, and Shih's four untestable claims.
5. **Supplementary.** Still nothing exists.

⚠ **NMI forbids Discussion subheadings and the supervisor asked for a
sectioned Discussion.** Unresolved.

## Tier 1 as originally framed. **Abstract first this time.**

AW, 11 November: *"I feel like this intro needs an abstract to work better.
So I'll place abstract first this time."* The Discussion is deferred
outright until the claims axis lands and Figure 2 is decided.

- [ ] **Abstract: full rewrite. FIRST.** Cannot be patched; it was written
      to a different story. Also still carries `[42]`, avoid the
      abbreviation, and runs 160 words against NMI's 150. It goes first
      because the Introduction has to expand something, and 150 words is
      the cheapest place to find out whether the story holds.
- [ ] **Introduction: full rewrite.** Stale against the new line, and it is
      also `[65]` and `[83]`, the supervisor's largest comments. The shape
      AW set: open on the atlas-building problem, then what each study in
      the corpus found individually, then the need for a disease atlas, and
      endometriosis as the motivated choice **after** the shape is stated,
      not before. `INTRODUCTION_STRUCTURE.md` is from the old framing and
      has to be rewritten before any prose, per that file's own contract.
      Budget it against Hrovatin's five stages.
      **The 11 November spine, from the supervisor, is now the paragraph
      map**: why scRNA, why endometriosis, why a disease atlas, what the
      other endometriosis studies have shown, what foundation models can say
      at single-disease level and why an atlas beats that, then what we do.
      Two consequences. The delay and misdiagnosis material stops being the
      opening hook and becomes the evidence under **why endometriosis**,
      which also settles where the supervisor's cut lands. And the
      foundation-model sentence grows from one line into a paragraph, with
      the warning attached: *"I'd be careful of overreaching here."*
      The message that must land is that **a disease atlas is a great thing
      to have for a disease**.

      **Three quotations the Introduction must carry.** The first is the
      strongest licence the project has found and it is endometriosis
      specific, which Hrovatin is not. All three are AW's call to place.

      1. HECA, Marečková 2024, *Nat. Genet.*: *"Conflicting evidence exists
         about whether and to what extent the endometrium itself (that is,
         the eutopic endometrium) differs between those with and without
         endometriosis. ... Larger sample sets are now needed to unpick
         whether and how the endometrium differs in those with and without
         endometriosis."* The field's own reference atlas asking for the
         thing our corpus is. ⚠ The full sentence uses "women"; quoting it
         verbatim is reporting the source, which is still the open question
         in `INTRODUCTION_STRUCTURE.md`.
      2. HECA again: *"Previous endometrial single-cell atlases profiled
         few donors and lacked consensus in defining cell types."* AW:
         quote and cite.
      3. Dümpelmann 2026: *"recent single-cell endometriosis studies
         including the eutopic endometrium faced limitations, such as small
         eutopic sample size, cell type exclusion, exogenous hormone
         treatment, or did not consider menstrual cycle phase changes."*
         AW: quote and cite. Every item is a design limitation pooling
         addresses.
- [ ] **Results: remould, do not rewrite.** The numbers stand. What changes
      is the framing and the subsection headers, which must name the
      **stage or the constraint**, not the dataset, or a reviewer reads the
      paper as an anecdote rather than a case study. Declarative headers in
      IBDex's style. Results now interprets, per the 9 November ruling: one
      precise line of reading per subsection, argument still in Discussion.
      **Two passages get real depth, per 11 November.** The frontier must be
      explained properly and must carry the dominance result: all nine
      competing representations are strictly worse than ELAJ$_{B\,hi}$ on
      **both** axes, nine of nine. The supervisor's reason for wanting it is
      explicit, *"SOTA status is important"* and it *"cements the paper's
      place in a journal like NMI"*. And the Figure 4 UMAPs get discussed in
      detail rather than pointed at. This sits against the 9 November rule
      to keep Results tight; depth here means more reading per number, not
      more words per number.
- [ ] **Discussion: DEFERRED, then remould, and it is now sectioned.** AW,
      11 November: *"Discussions can come later. It needs HPC work as well
      as figures placement decided. Without these things it is hard to
      structure the discussion section."* Eight paragraphs
      written to the old framing become subheaded sections comparing us to
      three things, in the supervisor's order: **foundation models** (an
      atlas gives more about one disease than a foundation model does),
      **baselines** (a better architecture earns the frontier), and
      **single datasets** (scale lets us confirm or contradict what small
      cohorts claimed). The scIB and donor-memorisation findings stay here
      as results about the field's instrument, NOT in Methods.
      **A fourth section is required: limitations and future work**, and it
      must answer the three questions the supervisor predicts a reader will
      ask. Does this become a good foundation model. Are foundation models
      bad. Would it work on any disease. **This is the one licensed
      exception to "do not pre-empt objections nobody has made"**, because
      he has made them.
- [ ] **Methods: tweaks only.** Add a *Comparison methods* cross-reference
      to the new framing, and check nothing contradicts the case-study
      shape. The `\flow{}` cuts and the KL-ramp correction are already in.

## Tier 2. Supplementary and Extended Data. Nothing exists.

- [ ] **The entire Supplementary Information section.** Not started, and
      **it was upgraded on 11 November from a gap to a destination**:
      *"There needs to be a lot of supplementary figures and data. Tables,
      figures of all kinds, etc. Reducing figures in the main prose is
      countered by figures in supplementary. All your crazy ideas can fit
      here."* IBDex ships 26 supplementary tables and 6 figures, which is
      the scale he is used to seeing and the reference he named. Everything
      cut from the main set lands here rather than being lost: the current
      Figure 3 if the three-figure decision goes through, the ablation
      UMAPs, the dissociation panel, the per-arm tables.
- [ ] **Supplementary Figure 1, the ablation UMAPs.** Study-mixing UMAPs for
      ELAJ$_{B\,hi}$ and the five ablation arms. Sources on disk at
      `Outputs/{p_series,a_series}/*/figures/best/`; redraw from the latents.
- [ ] **Extended Data.** One slot filled, PRISMA. Nine open; priority order
      in `06-display-items.tex`.
- [ ] **The pinned dissociation panel** needs a home: Figure 4 or Extended
      Data. Built, looks right, unplaced. `panel_dissociation.png`.
      **It surfaces a number the paper does not carry**: surgical stage on
      the whole corpus is $+$0.3320, $p=0.005$ at 58 donors, against the
      held-out 0.1313 at $p=0.303$. Either that goes into Results `[4]` or
      the row comes out of the panel.

## Tier 3. Display items

- [ ] **R4 ASSUMES A FIGURE AND ITS NATURE IS OPEN.** AW, 13 November:
      *"We may need to assume a figure that describes a couple of things.
      Feel free to make that assumption but record it."* R4's prose carries
      `(Fig.~X)` placeholders for two things that cannot be read from prose:
      **the per-family disease AUCs against their nulls**, where the point
      is that mixing the families destroys a signal immune cells carry
      alone; and **the ranked gene shifts**, where the point is the
      asymmetry, four externally replicating genes at one end and none at
      the other. Whether that is one figure or two, main text or
      Supplementary, is undecided. R3 also carries one `(Fig.~X)` for the
      severity composition.


- [ ] **Figure 1's legend is stale.** It describes five panels; there are
      now four, and **panel a has never been described at all**.
- [ ] **The renumbering.** `figure4.py` becomes Figure 3 and the old
      Figure 3 leaves the main set. Script names match paper numbers, so
      this renames files, captions, every `\ref`, and both auditors' pins.
- [ ] **Figure 2, the frontier, needs a redesign discussion before any
      drawing.** It must carry the cycle-against-study-separation scatter
      cut from Figure 1, it must carry the SOTA argument visually as well
      as in prose, and per AW it must stop reading as a cold benchmark.
      Possibly supplemented with panels that are not scatters.
- [ ] **Every panel referenced in prose.** Figures 2, 3 and 4 still have
      panels that no sentence points at.
- [x] Figure 1 panel c's x-label was clipped by the canvas edge. Bottom
      margin 4 to 8 mm; the figure is 213.5 mm tall and an assert now fails
      the render rather than leaving it for a reader to spot.
- [ ] Figure 1 is 213.5 mm tall. It fits, but it is close to a full page.

## Tier 3b. Citations, and this is a whole-paper pass

- [ ] **CITATIONS IN THE SUPERVISOR'S FILE ARE DEFERRED, AW's ruling
      14 November.** The 2026-11-14 Discussion changeset was pasted in with
      its citations rendered as author-year brackets and **he has made no
      citation changes yet, by choice**: *"We have citations in the right
      place in our local tex files. We will both add all references in the
      correct and edit the file to add citations in the correct place.
      You'll just have to give me pointed changes then."*
      So the citation work is **one later pass over his whole file**, not
      per-section, and when it happens the deliverable is **pointed
      find-and-replace changes naming each location and its number**, not
      another wholesale paste. Until then his file's Results section carries
      no citations at all, because pandoc dropped every `\citep` from the
      2026-11-13 batch, and the Discussion carries author-year brackets.
      `sections/*.tex` is the authority on where each citation belongs.
- [ ] **AW, 14 November: the paper is under-cited throughout.** His own
      observation and it matches what the register reading found. Five of the
      eight published Discussions read for `DISCUSSION_REGISTER.md` cite
      twelve or more references in that section alone; MIDAS cites 35 in 995
      words. Our Discussion now cites 18 after the rewrite, up from one, and
      **the Introduction, Results and Methods have not been reviewed this
      way.** Do this as one pass over the whole paper once the sections are
      drafted, not section by section.
- [ ] **The Discussion's paragraph 6 must reference the ablation Supplementary
      figures.** AW, 14 November. That paragraph asserts four ablation
      outcomes, and two of them, the single-study territories that appear
      without the elastic cell similarity head and the latent reorganising
      when the sentinel is replaced with zeros, **are claims about an
      embedding the reader cannot see**. Results carries the same two with
      `(Fig.~X)` placeholders, so the panels are already owed; the Discussion
      needs its own pointer to them. `FIGURES_NEEDED.md` F4 and F5 are those
      panels, and they were provisionally one four-panel Supplementary
      figure, which is now load-bearing for two sections rather than one.
- [ ] **`Supplementary Note~X` is now referenced from the Discussion.** The
      limitations paragraph redirects three corpus constraints there:
      overlapping donor identifiers across one study pair, the single cohort
      recording cycle day, and the unstratified permutation null. That note
      has to exist before submission, and the placeholder has to resolve.

## Tier 4. Mechanical, none of it blocking

- [ ] **Numbered references in the DOCX.** The `.tex` is already numbered;
      pandoc renders author-year. `make_draft.sh` is wired for
      `assets/nature.csl` and AW is fetching it.
- [ ] **Reference format** per NMI: sequential across main text, Methods,
      Data availability; article titles required; URLs parenthetical.
- [ ] **The bibliography has not been updated** in the supervisor's file.
      AW's call to do it at the end. Seven new entries so far.
- [ ] Extend both auditors to Methods.
- [ ] `vasilevsky2022mondo` and `czi2023cellxgene` are preprints; check for
      journal versions.
- [ ] Six references cited zero times.
- [ ] One unnamed skipped test in the suite of 1,945.

## The handover workflow, unchanged

1. change the `.tex`
2. build the Word file
3. hand AW a changeset of short **maths-free** find-and-replace fragments,
   built by `make_changeset.py`; he applies them in the guide's OneDrive copy

**Batch 2026-11-10 is with AW and not confirmed applied.** Figure 1 has
changed since, so the next batch must carry the new image and legend.

## The supervisor's comments still ours

`[97]` rephrase the pooled-corpus paragraph, `[42]` the abstract
abbreviation, `[82]` trials or studies, `[503]` and `[511]` in *Data
collection*. Most are absorbed by the Introduction and Abstract rewrites.

**His to clear**: `[132]`, `[467]`, `[507]`.

**To discuss in person**, both synced into the tex as he made them: the
"pain is a recurring date on a calendar" opening, and the human-health
paragraph. Exact words in CONTINUITY.

## Externals, AW owns all of these

Repository URL, licence, Zenodo DOI, funding and grant numbers, final author
list, Reporting Summary, cover letter, bioRxiv preprint.
