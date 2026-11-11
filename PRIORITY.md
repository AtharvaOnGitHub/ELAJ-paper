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

---

## Tier 1. The sections, in the order they should be done

- [ ] **Introduction: full rewrite.** Stale against the new line, and it is
      also `[65]` and `[83]`, the supervisor's largest comments. The shape
      AW set: open on the atlas-building problem, then what each study in
      the corpus found individually, then the need for a disease atlas, and
      endometriosis as the motivated choice **after** the shape is stated,
      not before. `INTRODUCTION_STRUCTURE.md` is from the old framing and
      has to be rewritten before any prose, per that file's own contract.
      Budget it against Hrovatin's five stages.
- [ ] **Abstract: full rewrite.** Cannot be patched; it was written to a
      different story. Also still carries `[42]`, avoid the abbreviation,
      and runs 160 words against NMI's 150.
- [ ] **Results: remould, do not rewrite.** The numbers stand. What changes
      is the framing and the subsection headers, which must name the
      **stage or the constraint**, not the dataset, or a reviewer reads the
      paper as an anecdote rather than a case study. Declarative headers in
      IBDex's style. Results now interprets, per the 9 November ruling: one
      precise line of reading per subsection, argument still in Discussion.
- [ ] **Discussion: remould.** Eight paragraphs written to the old framing.
      The scIB and donor-memorisation findings stay here as results about
      the field's instrument, NOT in Methods.
- [ ] **Methods: tweaks only.** Add a *Comparison methods* cross-reference
      to the new framing, and check nothing contradicts the case-study
      shape. The `\flow{}` cuts and the KL-ramp correction are already in.

## Tier 2. Supplementary and Extended Data. Nothing exists.

- [ ] **The entire Supplementary Information section.** Not started. The
      supervisor flagged it as completely missing and AW accepted that.
      IBDex ships 26 supplementary tables and 6 figures, which is the scale
      he is used to seeing.
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
- [ ] **Figure 2** must now carry the frontier properly, including the
      cycle-against-study-separation scatter cut from Figure 1.
- [ ] **Every panel referenced in prose.** Figures 2, 3 and 4 still have
      panels that no sentence points at.
- [ ] Figure 1 is 209.5 mm tall. It fits, but it is close to a full page.

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
