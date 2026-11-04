# Priority list

AW's order, 4 November 2026. Housekeeping runs behind the main paper so his
guide can review a complete manuscript.

**The goal: ELAJ at an NMI reviewer's desk, in the strongest honest shape.**

---

## 1. Figures — pin a few down now

| figure | state | blocked by |
|---|---|---|
| **6 — what the latent needs** | build 5 panels | nothing |
| **5 — the cycle** | composite b, c from the GIF frames | nothing |
| **4 — disease** | build c, d | nothing |
| **1 — the confound** | 4 known fixes | nothing |
| **3 — against the field** | build b, e, f | panel d waits on the mixing jobs |
| **2 — the frontier** | select and restyle | mixing panel waits on the 4 GPU dumps |

Legends are written to the 300-word limit and cost nothing against the 3,500.

## 2. Methods — what is left

| | |
|---|---|
| *Donor and study recovery* | 0 words |
| *Optimisation* | 0 words |
| *Use of large language models* | 0 words, and NMI requires it |
| *Whole-corpus embedding* | 11 words |
| *Cross-donor agreement* | 837 words, unreviewed. Needs the estimator rewrite, and one claim cut: the binding constraint at 16–60 donors is the width of the null, not the number of distinct permutations |
| *Study selection* | written, carries a TODO |

## 3. Results — in this order

1. **`[5]`** what the latent needs. D1–D6 settled, B2/B3 need their arms named
2. **`[1]`** the frontier and the field. Needs A1–A6 rewritten in
   `RESULTS_STRUCTURE.md` first, and the mixing jobs landed
3. **`[2]`** reading 1.58M cells as sixteen numbers. **Fully settled today** —
   take this slot ahead of `[1]` if the jobs have not landed

`[3]` and `[4]` are drafted and with AW.

## 4. Discussion — structure

No subheadings permitted. ~1,000 words. Carries: the arguments moved out of
Results, C6's interpretation, F1–F6, and the cut Introduction material.

## 5. Finish Discussion and the remaining figures

## 6. Abstract

150 words, unreferenced.

---

## Also needed, and not previously on the list

| | why it is not optional | lead time |
|---|---|---|
| **Code availability** | no public repo, no licence, no tag, no DOI. Methods claims predictions were registered before training, which is only checkable if the repo is public | external: Zenodo, licence choice |
| **Paper title** | — | none |
| **Introduction ¶4–6** | unfinished at 485 words. Main-text budget. Where the research-neglect material goes | none |
| **Backmatter** | author contributions, competing interests, acknowledgements, in Nature's specified order | none |
| **Reporting Summary** | published with every accepted manuscript. Adobe Reader form | none |
| **Cover letter** | NMI asks for one on the work's importance. The IDAI answers already carry the framing | none |
| **Extended Data + Supplementary** | 10 items and an uncapped appendix, planned, none built | none |

## Housekeeping, deliberately last

- **References.** 8 entries unverified: `gbd2019asthma`, `idf2021diabetes`,
  `nhs2024noncoding`, `rands2014constrained`, `ballard2006delay`,
  `hoffmann2001girl`, `chen2008gender`, `li2025factors`. All cited **zero**
  times today, so nothing in the PDF rests on them. `hoffmann2001girl` and
  `chen2008gender` are the pain-bias citations Introduction ¶4–6 needs, so
  they must be verified **before** they are cited. The bib's
  "ALL UNVERIFIED" block header is stale; four entries inside it are marked
  verified individually.
- Appendices, Extended Data builds, the repo and its DOI.

## Running

| job | gives |
|---|---|
| 3 × CPU, `pca` / `harmony` / `scanorama` | full-split mixing + dumped latents. Unblocks A2 and Figure 3d |
| 4 × GPU dump, the frontier arms | their latents, scored locally. Unblocks Figure 2's mixing panel |

Not running, and carrying no claim: full-split mixing for the four foundation
models. Their latents were deleted and re-embedding is a day of GPU.
