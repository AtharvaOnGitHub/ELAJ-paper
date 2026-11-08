# Priority list

**The goal: ELAJ at an NMI reviewer's desk, in the strongest honest shape.**

One list, in the order to work it. A line with no *blocked by* can be done
right now. Rebuilt 6 November, after Results `[1]`, `[2]`, `[4]`, `[5]` and
Figure 2 landed.

## Where the paper stands

| section | prose words | state |
|---|---:|---|
| Abstract | 151 | drafted, **pinned** on the referenced-or-not question |
| Introduction | 476 | ¶4–6 unfinished |
| Results `[1]` the frontier | ~380 | **done** |
| Results `[2]` sixteen numbers | ~190 | **done** |
| Results `[3]` the cycle | ~326 | with AW |
| Results `[4]` stage and grade | ~430 | **done** |
| Results `[5]` the disease axis | ~160 | **done** |
| Results `[6]` what the latent needs | **0** | the last one |
| Discussion | 1,285 | **done**, 8 paragraphs |
| Methods | 4,714 | **five subsections empty** |
| Legends | 733 | Figures 2, 3, 4 written; 1 and 5 not |

Main text 2,411 of 3,500. Build: 24 pages, zero overfull, both auditors green.

## To be discussed in person, not over comments

AW, 8 November 2026. Two of the supervisor's untracked edits are losses
rather than corrections, and AW will raise them face to face rather than
argue them in a Word thread. Both are SYNCED INTO THE TEX AS HE MADE THEM;
these are notes on what to put back if the conversation goes that way.

- [ ] **The opening line of the Introduction, cut.** "Pain is a recurring
      date on a calendar for 190 million people worldwide
      (`who2025endometriosis`)." It was the hook the whole Introduction was
      built on, and it is the sentence the abstract's own opening answers
      to. Its citation is now unused.
- [ ] **The human-health paragraph, cut.** "A subtle but deliberate choice
      in this study is to treat this disease as a human health problem
      rather than a gendered disease. At a scale of hundreds of millions of
      patients, we believe this to be necessary to bring attention to this
      problem." It is a stated position rather than a stylistic choice, and
      it is the one place the paper explains a convention it follows
      throughout.

## Compute

Nothing is running and nothing is blocked on compute. Every number the paper
needs is on disk and sourced through the manifest.

---

- [ ] **Results `[6]`** — what the latent needs. The last subsection. D1, D2,
      D4, D6 settled; D3 and D5's mixing figures are now full-split
      (0.7613 base, 0.8340 without ECS, 0.7818 without the sentinel). B2 and
      B3 need their arms named. All eleven arms are in `Outputs/Benchmarks/full/`.

- [ ] **Supplementary Figure 1, the ablation UMAPs.** Scheduled late, on AW's
      ruling of 6 November, but `[6]` points at it twice. One horizontal
      figure: study-mixing UMAPs for ELAJ$_{B\,hi}$ and all five ablation
      arms, coloured by study, one panel each. Sources are already on disk,
      each arm's own selected checkpoint:
      `Outputs/{p_series/p1_dab168_kl1,a_series/a1_*}/figures/best/latent_umap_epoch*.png`
      is the rendered five-panel version; the figure wants only the *by
      study* panel from each, redrawn from the latents rather than cropped.
      What it has to show, and what the benchmark already says: study
      territory grows in the order base 0.7613 < -sentinel 0.7818 <
      -ECS 0.8340, and both ablations develop large single-study regions
      that the reported arm does not have.

- [ ] **Figure 5, the ablations.** AW's proposal, 6 November: replace the
      five-panel figure with **one long table** carrying cell family,
      menstrual phase, donor recovery, study separation and the rest, for
      every p-series and a-series arm, base row marked. NMI counts tables as
      display items, so this keeps us at five of six.
      *Blocked by:* `[6]`, which decides what the table has to carry.

- [ ] **Figure 1** — ELAJ as a model and the main findings. Architecture as
      one wide butterfly panel, **two frontier scatters with every method and
      the Pareto front drawn** (AW, 6 November: Figure 1 keeps the frontier,
      Figure 2 keeps the movement), three UMAPs along the bottom. Known
      defects: whitespace, clipped boxes, the spider label, and a chance line
      drawn at 0.370 which is the double-counting error.

- [ ] **Legends for Figures 1 and 5.**
      *Blocked by:* those two figures.

- [x] **Methods — *Donor and study recovery*.** CUT 7 Nov, AW: one-liners
      already stated elsewhere. The study rescaling it would have defined
      now lives in Table 1's caption.
- [x] **Methods — *Optimisation*.** Written 7 Nov, 335 words.
- [x] **Methods — *Use of large language models*.** Written 6 November from
      the thesis's own Appendix A, compressed to ~160 words.
- [x] **Methods — *Whole-corpus embedding*.** CUT 7 Nov, AW: a CVAE has a
      latent space and we read it; the procedure is in the code.
- [x] **Methods — *the severity merge*.** CUT 7 Nov, AW: `[4]` already
      states the rASRM I--II / III--IV definition. Only the citation to
      duempelmann\_2026 on that sentence is outstanding.
- [x] **Methods — *the whole-corpus rule*.** CUT with the subsection above.
- [x] **Methods — *Cross-donor agreement*.** Rewritten 7 Nov. The six
      loopholes resolved, the wrong claim cut, E1 in and then out on AW's
      edit, and t=1 found not to exist in the code.
- [x] **Methods — *Study selection*.** PRISMA settled 7 Nov as Figure 1
      panel (d). 254 is the donor count everywhere; 269 appears once, where
      the deduplication is explained.

- [ ] **Extend both auditors to Methods.** Results' numbers are covered;
      Methods' are not. Mostly accessions and configuration.

- [ ] **Paper title.**

- [ ] **Resolve the abstract reference question.** Read
      `Nature_websites/NMI_Content_Types.pdf`. The file header quotes it as
      "up to 150 words, unreferenced"; AW believes otherwise. The draft is
      written either way.

- [ ] **Verify `hoffmann2001girl` and `chen2008gender`.** Cited zero times.
      *Unblocks:* Introduction ¶4–6.

- [ ] **Introduction ¶4–6.** 476 words, unfinished.
      *Blocked by:* the two references above.

- [ ] **Reporting Summary.** Adobe Reader form.
- [ ] **Cover letter.** The IDAI answers carry the framing.

- [x] **Discussion.** Written 6 November, 1,285 words, no subheadings.
      SUPERSEDED, kept for the record: No subheadings, ~1,000 words, currently nothing but
      notes. Carries the arguments moved out of Results, C6, F1–F6, the cut
      Introduction material, and the staging argument in full: the scale
      describes lesions, lesion burden has never predicted symptoms, patients
      have said so for decades, and the dissociation in `[4]` is evidence the
      field should act on.
      *Blocked by:* `[6]`.

- [ ] **Abstract, final.** 150 words.
      *Blocked by:* everything above.

- [ ] **Extended Data and Supplementary.** 10 items, none built.

- [ ] **Foundation models on the whole corpus.** AW wants it; not a blocker.
      `embed_pretrained.sh` hardcodes its arguments and forwards nothing, so
      `--splits train val test` and a separate `OUT` cannot be passed and the
      existing val+test latents must not be overwritten. Then four GPU jobs at
      roughly 24 h each.

- [ ] **Code availability.** No public repo, licence, tag or DOI. Methods
      claims predictions were registered before training, which is only
      checkable if the repo is public.
      *Blocked by:* external, a licence choice and a Zenodo deposit.

- [~] **Backmatter.** Competing interests written. Acknowledgements and
      author contributions seeded with coral placeholders: BlueBEAR
      publishes a form of words it asks to be used verbatim, and the author
      list is not final.

- [ ] **Cite duempelmann\_2026 and marecko\_2024 for their methods sections.**

- [ ] **Verify the remaining six references.** `gbd2019asthma`,
      `idf2021diabetes`, `nhs2024noncoding`, `rands2014constrained`,
      `ballard2006delay`, `li2025factors`. All cited zero times.
