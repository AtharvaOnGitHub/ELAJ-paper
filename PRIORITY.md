# Priority list

**The goal: ELAJ at an NMI reviewer's desk, in the strongest honest shape.**

One list, in the order to work it. A line with no *blocked by* can be done
right now. Rebuilt 6 November.

## Where the paper stands

| section | state |
|---|---|
| Abstract | 149 words drafted, **pinned** on the referenced-or-not question |
| Introduction | 581 words, ¶4–6 unfinished |
| Results `[1]` | 165 words, written against superseded numbers |
| Results `[2]` | **0 words** |
| Results `[3]` | 326 words, with AW |
| Results `[4]` | 416 words, ten of ten, done bar the 118-donor update |
| Results `[5]` | 156 words, approved |
| Results `[6]` | **0 words** |
| Discussion | 397 words of a ~1,000 target |
| Methods | 5,718 words, **five subsections empty** |
| Legends | 1,173 words, written against the older figure scheme |

## Compute in flight

| | gives | eta |
|---|---|---|
| `mix_scfoundation` | the last point on Figure 2's mixing axis | running 15 h+ |
| Run 1, 2 whole-corpus embeds + scorings | `[4]` severity at **118 donors** instead of 34 | ~2 h |
| Run 2, 9 held-out embeds + scorings | `[1]`, `[6]`, Figure 2's mixing axis | ~5 h |

---

- [ ] **Settle the figure numbering.** `figures/pinned/` has 1 ELAJ as a model ·
      2 the frontier · 3 both latents · 4 nine UMAPs · 5 ablations.
      `06-display-items.tex` still has 1 the confound · 2 the frontier ·
      3 against the field · 4 disease · 5 the cycle · 6 what the latent needs.
      `[4]` and `[5]` already cite `Fig.~4a/4d/4g/4h/4i`, correct only under the
      pinned scheme.
      *Unblocks:* six legends, every `Fig.~N`, all figure fixes, Extended Data.
      **One decision, and it is the biggest single unlock on this list.**

- [ ] **Results `[2]`** — 1.58M cells as sixteen numbers. Fully settled, zero
      words written.

- [ ] **Methods — *Donor and study recovery*.** 0 words.
- [ ] **Methods — *Optimisation*.** 0 words.
- [ ] **Methods — *Use of large language models*.** 0 words, NMI requires it.
- [ ] **Methods — *Whole-corpus embedding*.** 11 words.
- [ ] **Methods — *the severity merge*.** New subsection. rASRM I–II and III–IV
      from duempelmann\_2026, rASRM I–IV from marecko\_2024, both published, so
      the merge is sourced and not assumed. Say why
      `severity (study vocabularies)` is not used: study-prefixed levels,
      readable off study identity.
- [ ] **Methods — *the whole-corpus rule*.** One paragraph: a label the model
      was never given cannot leak, and the estimator already discards
      same-donor neighbours, so severity, stage, grade and disease are measured
      on all 1,577,728 cells while phase, study and donor recovery are held out.
      This is the rule the figures already follow.
- [ ] **Methods — *Cross-donor agreement*.** 812 words, unreviewed. Needs the
      estimator rewrite and one claim cut: the binding constraint at 16 to 60
      donors is the width of the null, not the number of distinct permutations.
- [ ] **Methods — *Study selection*.** 355 words, carries a TODO. Also where
      the fifteen dual-identifier donors go: 269 identifiers, **254 people**.

- [ ] **Extend both auditors to Methods.** 85 numbers there are unaudited;
      Results' 50 are covered. Mostly accessions and configuration, so they
      verify against configs rather than benchmark files.

- [ ] **Paper title.**

- [ ] **Resolve the abstract reference question.** Read
      `Nature_websites/NMI_Content_Types.pdf`. The file header quotes it as
      "up to 150 words, unreferenced" and CONTINUITY records that as settled;
      AW says otherwise. Whichever way it goes the draft is written.

- [ ] **Verify `hoffmann2001girl` and `chen2008gender`.** Cited zero times
      today, so nothing rests on them yet.
      *Unblocks:* Introduction ¶4–6.

- [ ] **Introduction ¶4–6.** 581 words, unfinished. Where the research-neglect
      material goes.
      *Blocked by:* the two references above.

- [ ] **Reporting Summary.** Adobe Reader form.
- [ ] **Cover letter.** The IDAI answers carry the framing.

- [ ] **`[4]` to 118 donors.** Swap the merged-severity figures for the
      whole-corpus ones and the donor count from 34 to 118, 18 to 57.
      *Blocked by:* Run 1, ~2 h.

- [ ] **Results `[6]`** — what the latent needs. D1, D2, D4, D6 settled.
      B2 and B3 need their arms named.
      *Blocked by:* Run 2 for D3 and D5's mixing figures, ~5 h.

- [ ] **Rewrite A1–A6 in `RESULTS_STRUCTURE.md`** on the completed field table.
      *Blocked by:* Run 2, `mix_scfoundation`.

- [ ] **Results `[1]`** — the frontier and the field. 165 words written against
      old-cap mixing numbers, all of which moved.
      *Blocked by:* A1–A6, Run 2, `mix_scfoundation`.

- [ ] **Figure 2 rebuilt** on full-split numbers.
      *Blocked by:* the figure numbering, Run 2, `mix_scfoundation`.

- [ ] **Figures 1 to 4, known defects.** Fig 1: whitespace, clipped boxes,
      spider label, the 0.370 chance line, two Pareto fronts. Fig 2: labels
      collide in c and d. Figs 3 and 4: transparency at 600 dpi.
      *Blocked by:* the figure numbering.

- [ ] **All six legends.**
      *Blocked by:* the figure numbering.

- [ ] **Discussion.** No subheadings, ~1,000 words, currently 397. Carries the
      arguments moved out of Results, C6, F1–F6, the cut Introduction material,
      and the staging argument in full: the scale describes lesions, lesion
      burden has never predicted symptoms, patients have said so for decades,
      and a null across every representation of the public record is evidence
      the field should act on.
      *Blocked by:* `[1]`, `[4]`, `[6]`.

- [ ] **Figure 5, the ablations.** Deferred by AW until after the Discussion.
      *Blocked by:* the Discussion, the figure numbering.

- [ ] **Abstract, final.** 150 words.
      *Blocked by:* everything above.

- [ ] **Extended Data and Supplementary.** 10 items, none built.
      *Blocked by:* the figure numbering.

- [ ] **Foundation models on the whole corpus.** AW wants it; not a blocker.
      Needs one change first: `embed_pretrained.sh` hardcodes its arguments and
      forwards nothing, so `--splits train val test` and a separate `OUT`
      cannot be passed, and the existing val+test latents must not be
      overwritten. Then four GPU jobs, ~24 h each at 1.58M cells, 2 days on two
      cards, and scFoundation's dense intermediate goes from 32 GB to ~120 GB
      of scratch.

- [ ] **Code availability.** 18 words. No public repo, no licence, no tag, no
      DOI. Methods claims predictions were registered before training, which is
      only checkable if the repo is public.
      *Blocked by:* external, a licence choice and a Zenodo deposit.

- [ ] **Backmatter.** 79 words. Author contributions, competing interests,
      acknowledgements, in Nature's order.
      *Blocked by:* the Zenodo DOI.

- [ ] **Cite duempelmann\_2026 and marecko\_2024 for their methods sections**,
      not only as corpus rows, since the severity merge rests on them.

- [ ] **Verify the remaining six references.** `gbd2019asthma`,
      `idf2021diabetes`, `nhs2024noncoding`, `rands2014constrained`,
      `ballard2006delay`, `li2025factors`. All cited zero times. The bib's
      "ALL UNVERIFIED" block header is stale; four inside it are marked
      verified individually.

---

## Word budget, last build

| | words | |
|---|---:|---|
| Abstract | 149 | cap 150 |
| Introduction | 581 | |
| Results | 1,063 | |
| Discussion | 397 | target ~1,000 |
| **main text** | **2,190** | cap 3,500 |
| Methods | 5,718 | own budget |
| Legends | 1,173 | own budget |

21 pages, zero overfull, `audit_numbers.py` and `verify_numbers.py` passing.
