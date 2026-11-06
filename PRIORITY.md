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
| Discussion | **~1** | notes only, nothing written |
| Methods | 4,714 | **five subsections empty** |
| Legends | 733 | Figures 2, 3, 4 written; 1 and 5 not |

Main text 2,411 of 3,500. Build: 24 pages, zero overfull, both auditors green.

## Compute

Nothing is running and nothing is blocked on compute. Every number the paper
needs is on disk and sourced through the manifest.

---

- [ ] **Results `[6]`** — what the latent needs. The last subsection. D1, D2,
      D4, D6 settled; D3 and D5's mixing figures are now full-split
      (0.7613 base, 0.8340 without ECS, 0.7818 without the sentinel). B2 and
      B3 need their arms named. All eleven arms are in `Outputs/Benchmarks/full/`.

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

- [ ] **Methods — *Donor and study recovery*.** 0 words.
- [ ] **Methods — *Optimisation*.** 0 words.
- [ ] **Methods — *Use of large language models*.** 0 words, NMI requires it.
- [ ] **Methods — *Whole-corpus embedding*.** 11 words.
- [ ] **Methods — *the severity merge*.** New. rASRM I–II and III–IV from
      duempelmann\_2026, rASRM I–IV from marecko\_2024, both published, so the
      merge is sourced and not assumed. Say why
      `severity (study vocabularies)` is unused: study-prefixed levels.
- [ ] **Methods — *the whole-corpus rule*.** One paragraph: a label the model
      never received cannot leak and the estimator already discards same-donor
      neighbours, so severity, stage, grade and disease are measured on all
      1,577,728 cells while phase, study and donor recovery are held out.
- [ ] **Methods — *Cross-donor agreement*.** 812 words, unreviewed. Needs the
      estimator rewrite and one claim cut: the binding constraint at 16 to 60
      donors is the width of the null, not the number of permutations.
- [ ] **Methods — *Study selection*.** Carries a TODO. Also where the fifteen
      dual-identifier donors go: 269 identifiers, **254 people**.

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

- [ ] **Discussion.** No subheadings, ~1,000 words, currently nothing but
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

- [ ] **Backmatter.** Author contributions, competing interests,
      acknowledgements, in Nature's order.
      *Blocked by:* the Zenodo DOI.

- [ ] **Cite duempelmann\_2026 and marecko\_2024 for their methods sections.**

- [ ] **Verify the remaining six references.** `gbd2019asthma`,
      `idf2021diabetes`, `nhs2024noncoding`, `rands2014constrained`,
      `ballard2006delay`, `li2025factors`. All cited zero times.
