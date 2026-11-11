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

## Decisions AW owes before the next block of work

1. **Three figures and a table, or six display items?** The supervisor's
   number against the settled one. He also wants the frontier explained in
   far more depth and the Figure 4 UMAPs discussed in detail, which argues
   for more figure space, not less. The resolution the feedback itself
   offers: depth goes into the **prose and the supplementary**, and the main
   set shrinks. AW has already said grain of salt.
2. **If three: which three, and in what order?** The supervisor asked for
   current Fig 4 to become Fig 2. The set that falls out is Fig 1 unchanged,
   Fig 2 the nine endometriosis UMAPs, Fig 3 the frontier in depth, Table 1.
   That sends the current Fig 3, both latents by family and phase, to
   Supplementary, and it puts the atlas before the integration evidence.
   **Results has to reorder with it.**
3. **Is the reproduction analysis in scope?** *"Some work on reproducing
   individual dataset results on the full corpus is needed."* New analysis,
   needs HPC, and it overturns "no further calculation". See Tier 0.

---

## Tier 0. New analysis, because it gates three sections at once

- [ ] **Reproduce individual-study results on the pooled corpus.** The
      supervisor's words: *"this is partially results and discussions because
      we compare what they have shown and what we are able to show."* It
      feeds the Introduction's "what other studies have shown", a Results
      passage, and the Discussion's third comparison. **Nothing else in this
      list needs compute; this does.** Scope it with AW first: which claims,
      from which of the eleven studies, measurable how. The standing rule
      "no per-study numbers for metadata in the latent" still binds, so any
      reproduction needing a per-study latent breakdown is out.

## Tier 1. The sections, in the order they should be done

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
- [ ] **Abstract: full rewrite.** Cannot be patched; it was written to a
      different story. Also still carries `[42]`, avoid the abbreviation,
      and runs 160 words against NMI's 150.
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
- [ ] **Discussion: remould, and it is now sectioned.** Eight paragraphs
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

- [ ] **Figure 1's legend is stale.** It describes five panels; there are
      now four, and **panel a has never been described at all**.
- [ ] **The renumbering, once decision 2 lands.** Script names match paper
      numbers, so `figure4.py` becoming Figure 2 renames files, captions,
      every `\ref`, and both auditors' pins.
- [ ] **The frontier figure** must carry the frontier properly, including
      the cycle-against-study-separation scatter cut from Figure 1, and it
      now has to carry the SOTA argument visually as well as in prose.
- [ ] **Every panel referenced in prose.** Figures 2, 3 and 4 still have
      panels that no sentence points at.
- [x] Figure 1 panel c's x-label was clipped by the canvas edge. Bottom
      margin 4 to 8 mm; the figure is 213.5 mm tall and an assert now fails
      the render rather than leaving it for a reader to spot.
- [ ] Figure 1 is 213.5 mm tall. It fits, but it is close to a full page.

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
