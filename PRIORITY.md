# Priority list

AW's order, 4 November 2026, rebuilt 5 November with dependencies.
Housekeeping runs behind the main paper so his guide can review a complete
manuscript.

**The goal: ELAJ at an NMI reviewer's desk, in the strongest honest shape.**

---

## Read this first: three things gate almost everything

**G1. The figure numbering is contradictory and must be settled before any
legend or any `Fig.~N` reference is final.** Two schemes are live. The order
AW set on 5 November and which is pinned in `figures/pinned/`:

| | pinned, 5 November |
|---|---|
| 1 | ELAJ as a model and main findings |
| 2 | The ELAJ frontier |
| 3 | Both latents by cell family and cycle phase |
| 4 | What endometriosis looks like in nine UMAPs |
| 5 | Ablations, deferred until after the Discussion |

`sections/06-display-items.tex` still carries the older one: 1 the confound,
2 the frontier, 3 against the field, 4 disease, 5 the cycle, 6 what the latent
needs. Results `[5]` already cites `Fig.~4a`, `4d` and `4g`, which are correct
under the pinned scheme and wrong under the legend file's. **AW's call, and it
is one decision that unblocks six legends and every cross-reference.**

**G2. The HPC round now running settles the whole field table.** Nothing in
`[1]`, `[4]` or Figure 2 can be finalised before it lands. Everything else in
this list can proceed without it.

**G3. The ELAJ arms and the five ablation arms cannot be scored from HPC.**
`--dump-cells` writes `latent.npy` plus `metadata.csv.gz` and no manifest, so
`--external-latent` cannot read them. They need one local script, roughly 80
lines, calling the project's own `study_mixing.measure` and
`cross_group_agreement`. **Not yet approved. Nine rows of the field table and
both of D3 and D5's mixing numbers wait on it.**

---

## Running on the HPC, and what each unblocks

| job | gives | unblocks |
|---|---|---|
| `mix_scgpt` `mix_geneformer` `mix_scfoundation` `mix_scimilarity` | full-split mixing for the four FMs, plus a reproducibility check on every other FM row | Figure 2's two mixing panels · `[1]` |
| `elaj_bench` 60895666 | pca, scvi, scanvi **inductive** at full split, with dumped latents | `[1]`'s protocol-matched baselines · Figure 2 |
| `sev_trans_pca` `sev_trans_harmony` `sev_trans_scanorama` | severity and severity (patients only) for the transductive three | `[4]` |
| `sev_scgpt` `sev_geneformer` `sev_scfoundation` `sev_scimilarity` | the same for the four FMs | `[4]` |
| `sev_ind_*`, chained on 60895666 | the same for the inductive three | `[4]` |
| 4 × `elaj_dump`, ablation arms | their latents; `a1_nophase` already landed | D3 and D5 via G3 · Figure 5 |

**First thing when you are back:** check all of these exited 0, then run the
`sev_ind_*` chain if the dependency did not fire.

---

## 1. Figures

| figure | state | blocked by |
|---|---|---|
| **1** ELAJ as a model | pinned; 4 known defects, incl. the 0.370 chance line | **G1** |
| **2** the frontier | pinned; study column is old-cap, labels collide in c/d | **G1** · **G2** |
| **3** both latents | pinned; transparency noted for the 600 dpi render | **G1** |
| **4** nine UMAPs | pinned; transparency noted for the 600 dpi render | **G1** |
| **5** ablations | deferred by AW until after the Discussion; likely Extended Data | **G1** · **G3** |
| legends | 1,173 words written against the older scheme | **G1** |

Legends cost nothing against the 3,500-word main text.

## 2. Methods — zero dependencies, all of it writable now

| | state |
|---|---|
| *Donor and study recovery* | 0 words |
| *Optimisation* | 0 words |
| *Use of large language models* | 0 words, and NMI requires it |
| *Whole-corpus embedding* | 11 words |
| *Cross-donor agreement* | 837 words, unreviewed. Needs the estimator rewrite and one claim cut: the binding constraint at 16 to 60 donors is the width of the null, not the number of distinct permutations |
| *Study selection* | written, carries a TODO |
| *severity merge* | **new.** One paragraph: rASRM I–II and III–IV from duempelmann\_2026, rASRM I–IV from marecko\_2024, both published, so the merge is sourced and not assumed. Also why `severity (study vocabularies)` is not used: its levels are study-prefixed |

Methods stands at 5,718 words on its own budget.

## 3. Results — in this order

| | subsection | state | blocked by |
|---|---|---|---|
| 1 | **`[6]`** what the latent needs | D1, D2, D4, D6 settled. B2 and B3 need their arms named | D3 and D5 mixing need **G3** |
| 2 | **`[2]`** 1.58M cells as sixteen numbers | fully settled | nothing |
| 3 | **`[4]`** surgical stage and grade | note only. The story is settled: not one of ten methods clears its own null on stage, lowest *p* 0.149 | **G2**, the severity jobs |
| 4 | **`[1]`** the frontier and the field | needs A1–A6 rewritten in `RESULTS_STRUCTURE.md` first | **G2** · **G3** |

`[3]` is drafted and with AW. `[5]` was seeded and approved on 5 November,
subject to the audit, which passes.

Results stands at 996 words.

## 4. Discussion — structure

No subheadings permitted, roughly 1,000 words, currently 397. Carries the
arguments moved out of Results, C6's interpretation, F1–F6, and the cut
Introduction material. **Blocked by:** Results `[1]`, `[4]` and `[6]` landing,
since it is where their interpretation goes.

## 5. Finish the Discussion and Figure 5

## 6. Abstract

150 words, unreferenced. Currently 183. **Blocked by everything above.**

---

## Not previously on the list, and not optional

| | why | blocked by |
|---|---|---|
| **Paper title** | — | nothing |
| **Introduction ¶4–6** | unfinished at 581 words. Where the research-neglect material goes | `hoffmann2001girl` and `chen2008gender` must be verified **before** being cited |
| **Code availability** | no public repo, no licence, no tag, no DOI. Methods claims predictions were registered before training, which is only checkable if the repo is public | external: Zenodo and a licence choice |
| **Backmatter** | author contributions, competing interests, acknowledgements, in Nature's order. 79 words | the DOI, for code availability |
| **Reporting Summary** | published with every accepted manuscript. Adobe Reader form | nothing |
| **Cover letter** | NMI asks for one on the work's importance. The IDAI answers carry the framing | nothing |
| **Extended Data + Supplementary** | 10 items and an uncapped appendix, planned, none built | **G1** |

## Housekeeping, deliberately last

- **References.** 8 entries unverified: `gbd2019asthma`, `idf2021diabetes`,
  `nhs2024noncoding`, `rands2014constrained`, `ballard2006delay`,
  `hoffmann2001girl`, `chen2008gender`, `li2025factors`. All cited **zero**
  times, so nothing in the PDF rests on them. Two of them gate Introduction
  ¶4–6. The bib's "ALL UNVERIFIED" block header is stale; four entries inside
  it are marked verified individually.
- The repo, its licence and its DOI.
- Two new references to add: duempelmann\_2026 and marecko\_2024 are cited in
  the corpus table but the severity merge now rests on their methods sections.

---

## Can be struck off tomorrow without waiting for anything

Ordered by how much they unblock.

1. **G1, the figure numbering.** One decision, six legends.
2. **G3, approve the local scorer.** One file, nine table rows.
3. Methods: *Donor and study recovery*, *Optimisation*, *Use of large
   language models*, *Whole-corpus embedding*. Four sections at zero words.
4. Methods: the *severity merge* paragraph. Fresh, sourced, settled today.
5. Methods: the *Cross-donor agreement* rewrite and the permutation-count cut.
6. Results `[2]`. Fully settled, nothing pending.
7. Paper title.
8. Verify `hoffmann2001girl` and `chen2008gender`, which then unblocks
   Introduction ¶4–6.
9. Reporting Summary and the cover letter.
