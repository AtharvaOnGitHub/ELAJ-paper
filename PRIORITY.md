# Priority list

**The goal: ELAJ at an NMI reviewer's desk, in the strongest honest shape.**

One list, in the order to work it. Tick as they land. A line with no
*blocked by* can be done right now.

---

- [ ] **Confirm the HPC round exited 0**, and run the `sev_ind_*` chain if the
      dependency did not fire. 4 × `mix_*`, 1 × `elaj_bench`, 7 × `sev_*`,
      4 × `elaj_dump`.
      *Gives:* full-split mixing and severity for all ten methods, and the
      ablation latents.

- [ ] **Settle the figure numbering.** `figures/pinned/` carries 1 ELAJ as a
      model · 2 the frontier · 3 both latents by cell family and cycle phase ·
      4 nine UMAPs · 5 ablations. `sections/06-display-items.tex` still carries
      1 the confound · 2 the frontier · 3 against the field · 4 disease ·
      5 the cycle · 6 what the latent needs. Results `[5]` cites `Fig.~4a`,
      `4d`, `4g`, correct under the pinned scheme only.
      *Unblocks:* all six legends, every `Fig.~N` reference, Extended Data.

- [ ] **Approve the local mixing and cross-donor scorer.** `--dump-cells`
      writes `latent.npy` plus `metadata.csv.gz` and no manifest, so
      `--external-latent` cannot read the ELAJ or ablation dumps. One file,
      roughly 80 lines, calling the project's own `study_mixing.measure` and
      `cross_group_agreement`, brute-force neighbours.
      *Unblocks:* nine rows of the field table, D3 and D5's mixing numbers.

- [ ] **Methods — *Donor and study recovery*.** 0 words.
- [ ] **Methods — *Optimisation*.** 0 words.
- [ ] **Methods — *Use of large language models*.** 0 words, NMI requires it.
- [ ] **Methods — *Whole-corpus embedding*.** 11 words.
- [ ] **Methods — *the severity merge*.** rASRM I–II and III–IV from
      duempelmann\_2026, rASRM I–IV from marecko\_2024, both published, so the
      merge is sourced and not assumed. Include why
      `severity (study vocabularies)` is not used: its levels are
      study-prefixed and readable off study identity.
- [ ] **Methods — *Cross-donor agreement*.** 837 words, unreviewed. Needs the
      estimator rewrite and one claim cut: the binding constraint at 16 to 60
      donors is the width of the null, not the number of distinct permutations.
- [ ] **Methods — *Study selection*.** Written, carries a TODO.

- [ ] **Results `[2]`** — 1.58M cells as sixteen numbers. Fully settled.

- [ ] **Paper title.**

- [ ] **Verify `hoffmann2001girl` and `chen2008gender`.** The pain-bias
      citations. Cited zero times today, so nothing rests on them yet.
      *Unblocks:* Introduction ¶4–6.

- [ ] **Introduction ¶4–6.** Unfinished at 581 words. Where the
      research-neglect material goes.
      *Blocked by:* the two references above.

- [ ] **Reporting Summary.** Adobe Reader form, published with every accepted
      manuscript.

- [ ] **Cover letter.** NMI asks for one on the work's importance. The IDAI
      answers carry the framing.

- [ ] **Results `[6]`** — what the latent needs. D1, D2, D4, D6 settled. B2
      and B3 need their arms named.
      *Blocked by:* the local scorer, for D3 and D5's mixing numbers only.

- [ ] **Figures 1 to 4, known defects.** Fig 1: whitespace, clipped boxes,
      spider label, the 0.370 chance line, two separate Pareto fronts. Fig 2:
      labels collide in panels c and d. Figs 3 and 4: transparency at 600 dpi.
      *Blocked by:* the figure numbering.

- [ ] **Results `[4]`** — surgical stage and grade. Story settled: not one of
      the ten methods clears its own permutation null on stage, lowest *p*
      0.149, and that includes the heaviest donor memorisers.
      *Blocked by:* the severity jobs.

- [ ] **Rewrite A1–A6 in `RESULTS_STRUCTURE.md`** on the completed field table.
      *Blocked by:* the HPC round, the local scorer.

- [ ] **Results `[1]`** — the frontier and the field.
      *Blocked by:* A1–A6, the HPC round, the local scorer.

- [ ] **Figure 2 rebuilt** on full-split numbers. Study column is still
      old-cap.
      *Blocked by:* the figure numbering, the HPC round.

- [ ] **All six legends.** 1,173 words written against the older scheme.
      *Blocked by:* the figure numbering.

- [ ] **Discussion.** No subheadings, roughly 1,000 words, currently 397.
      Carries the arguments moved out of Results, C6's interpretation, F1–F6,
      and the cut Introduction material.
      *Blocked by:* Results `[1]`, `[4]`, `[6]`.

- [ ] **Figure 5, the ablations.** Deferred by AW until after the Discussion;
      likely Extended Data.
      *Blocked by:* the Discussion, the figure numbering, the local scorer.

- [ ] **Abstract.** 150 words, unreferenced. Currently 183.
      *Blocked by:* everything above.

- [ ] **Extended Data and Supplementary.** 10 items and an uncapped appendix,
      planned, none built.
      *Blocked by:* the figure numbering.

- [ ] **Code availability.** No public repo, no licence, no tag, no DOI.
      Methods claims predictions were registered before training, which is
      only checkable if the repo is public.
      *Blocked by:* external, a licence choice and a Zenodo deposit.

- [ ] **Backmatter.** Author contributions, competing interests,
      acknowledgements, in Nature's order. 79 words.
      *Blocked by:* the Zenodo DOI.

- [ ] **Cite duempelmann\_2026 and marecko\_2024 for their methods sections**,
      not only as corpus rows, since the severity merge rests on them.

- [ ] **Verify the remaining six references.** `gbd2019asthma`,
      `idf2021diabetes`, `nhs2024noncoding`, `rands2014constrained`,
      `ballard2006delay`, `li2025factors`. All cited zero times. The bib's
      "ALL UNVERIFIED" block header is stale; four entries inside it are
      marked verified individually.

---

## Word counts, last build

| | words | |
|---|---:|---|
| Abstract | 183 | cap 150 |
| Introduction | 581 | |
| Results | 996 | |
| Discussion | 397 | target ~1,000 |
| **main text** | **2,157** | cap 3,500 |
| Methods | 5,718 | own budget |
| Legends | 1,173 | own budget |

20 pages, zero overfull, `audit_numbers.py` and `verify_numbers.py` both
passing.
