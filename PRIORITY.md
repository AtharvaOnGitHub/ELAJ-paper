# Priority list

**The goal: ELAJ at an NMI reviewer's desk, in the strongest honest shape.**
Rewritten 14 November against actual state, because the previous version was
stale on four counts: it had the Discussion pending, the subheading question
unresolved, the supplementary as "nothing exists", and two of the four
moved-from-Results items listed as safe when one had been lost.

## The line everything now serves

> In this paper we build a single-cell disease atlas where inductive bias
> replaces pretraining scale, and use that to measure the trade-off between
> removing batch effects and keeping biology on a corpus limited by donors.

A **case study**, deliberately, licensed by `hrovatin2025atlases` saying no
one-size-fits-all atlas protocol exists. CONTINUITY has the four rejected
framings. `REGISTER.md` is the contract for Results prose;
`DISCUSSION_REGISTER.md` for the Discussion, built by reading eight published
Discussions rather than from our own notes.

---

# Where the paper is, 14 November

| section | state |
|---|---|
| Abstract | **stale. Full rewrite.** Must now carry the claims axis |
| Introduction | **stale. Full rewrite** to the supervisor's spine |
| Results | drafted and shipped 13 Nov, **X13 added since**. WITH THE SUPERVISOR UNTIL MONDAY |
| Discussion | written and shipped 14 Nov, **X13 added since** |
| Methods | done, 5,745 words, tweaks only |
| Supplementary | **building.** Own document and build; Note 1 done with both figures; Data packaged and sent; scIB scorecard complete |
| Extended Data | one item, PRISMA. Nine slots open |

**Nothing in Results may be rewritten before his Monday comments arrive**, or
they will land on a version that no longer exists.

**The Discussion subheading question is SETTLED and was never a blocker.**
Eight of eight comparators have none, IBDex included; his four sections are
carried by a topic-sentence ladder. Do not reopen it.

---

# 1. In flight on the HPC

| job | what it unblocks | wall | state |
|---|---|---|---|
| `umap_cache.sh` | every supplementary figure showing a latent | 3 h array | **DONE**, 9 caches at `Outputs/supplementary/umaps_supplementary/` |
| `marker_reproducibility.sh` | **X13** | 8 h CPU | **DONE.** In Results and the Discussion |
| `scib_scfoundation.sh` | the quarantined scIB cell | 6 h CPU | **DONE in substance**, see below |
| `count_params_sweep.py` | N1's figures | seconds | **DONE.** Anchored at 1,883,986 |
| `probe_stages.sh` to `p1_groups` | **X15** | 16 h GPU | **FAILED on the wall. Resubmit with `--only-groups`** |

**On the UMAP caches**: the job ran before the index pin was committed, so it
took the RNG path. That is fine, because HPC numpy 1.26.4 and local 2.2.6 were
checked to produce the identical draw (checksum 315692720845). The pin protects
future runs; it did not make these ones correct.

**X15 failed on the wall and the diagnosis matters.** It spent all sixteen
hours inside ONE stage, `groups/concat`, and never reached the per-group
stages the question needs. That stage is **12,672 wide**, not the 1,408 I
assumed: with the `cls+pool8` readout each group hands on 1 CLS plus 8 pooled
vectors, so 44 x 9 x 32. The cross-donor search is brute force, cells squared
times width. `--only-groups` was added to skip every pipeline stage; the 44
individual stages are 288 wide each and take the shorter two-label battery.

```
cd /rds/homes/a/axw1008/axw1008 && git pull && sbatch data_collation/scripts/probe_stages.sh p1_dab168_kl1 --runs-dir outputs/p_series --splits val test --only-groups --out outputs/probes/p1_groups
```

**Do not cut `--splits` to save time.** The latent row must reproduce the
benchmark's elaj row and that only holds on val+test; that reproduction is
the script's own integrity check. The next lever is `--k-cross-donor`.

**scIB is resolved without a rerun.** Job 61784251 computed every `cell
family` metric, then OOM-died on a second label set we do not use, so it
never wrote its CSV. **silhouette_batch = 0.754**, and all seven metrics it
shares with the original pass reproduce to the printed precision, so it is
comparable. `scib_table.py` parses it out of the log, which is kept where
that CSV would have been, and prefers the CSV if it ever appears. The
scorecard has no empty cell.

---

## What the supplementary is, as of 14 November

**Its own document and its own build**: `supplementary/supplementary.tex`,
`bash build_supp.sh`. S-prefixed numbering, own reference list, contents page
listing every figure and table. Section order Notes, Methods, Tables,
Figures, References, taken from MIDAS. Six pages, zero overfull, zero
undefined references.

`SUPPLEMENTARY_STRUCTURE.md` is the anatomy, read off eight published
supplementaries. `SUPPLEMENTARY_PLAN.md` is the ordering. Neither should be
re-derived.

| | state |
|---|---|
| **Note 1**, gene-group sizing | **done**, AW-edited, with Figures S1 and S2 and Table S2 |
| **Notes 2 to 8** | **drafted 15 Nov, unreviewed by AW.** scIB, limitations, frontier arms, ablations, label transfer, claims axis, marker reproducibility. ~45 pages with 44 figures and 24 tables, every table generated |
| Note 9, X15 | waits on the `--only-groups` probe job |
| **Supplementary Data D1 to D5** | **built and sent.** `Outputs/supplementary/send/` |
| **scIB scorecard** | **complete**, no empty cell |
| Source Data | waits on the figures being final |

**Four formatting rules learned from the comparators, do not re-derive.**
Numbered subsections only where a Note is a list of definitions; elsewhere
unnumbered headings or bold run-ins. The contents lists every figure and
table by title, so every float needs a short `\caption[short]{long}`. The
supplementary carries its own reference list. And `build_supp.sh clean` must
remove the `.bbl`, or a bibliography change survives a clean and citations
stay silently unresolved.

## Notes 2 to 8, and the figure exercise, 15 November

**One generator makes everything:** `figures/scripts/supp_figures.py`.
Every `supplementary/tables/*.tex` fragment and every cited
`supplementary/figures/*.png` comes out of it, reading benchmark files
through `table1.collect()`, the claims CSVs, the metrics files and the
dumps. The notes `\input` the fragments, so a number in a Note's table has
a file behind it. Rerun after any re-score; `--only <group>` for a subset,
`--no-umaps` to skip the 44 UMAP panels.

**The exploratory tier is outside git**:
`Outputs/supplementary/figures_explore/`, ~90 single-panel figures, 11 MB.
AW's instruction was single panels, no multi-panel grouping yet, legends
not yet. The ones a Note cites are copied into `supplementary/figures/`.

**Three things the exercise established that the paper did not know:**

1. **The split leak is not what M1 says.** Commit `7ed19bd` (5 Oct)
   resolves the 30 García-Alonso identifiers to 15 people BEFORE splitting,
   and every reported arm trained after it (p-series from 19 Oct). The
   held-out benchmark counts 70 of 254 people. What survives is narrower:
   `validate_latent.py` keys on the raw `patient_id` (269), so the
   whole-corpus cycle (142 donors) and donor-recovery (269) reads count the
   fifteen twice. N3 is written that way. **The Discussion's wording is
   decision 5 in section 4 below.**
2. ~~**Results points at two Methods subsections that do not exist.**~~
   **RESOLVED, AW 15 November: both go to Supplementary Methods.** So
   `(Methods, \emph{Label transfer})` and `(Methods, \emph{Severity})` in
   Results become `(Supplementary Methods, ...)`, and that section has to
   exist before the pointers resolve. See *Supplementary Methods* below.
3. **Only two scIB metrics are constants** (iLISI, cLISI); kBET is
   near-constant (range 0.04). Where scIB discriminates, no metric tracks
   donor recovery or the cycle (|rho| <= 0.60, none at P < 0.05). ELAJ is
   last of eleven on ARI/NMI and second on graph connectivity; N2 names the
   axes rather than hiding them.
4. **The seed figure: `a1_seed42` is built and ready to submit.** AW,
   15 November: *"We are checking the variance of the model. I don't want
   to combine it with effects of varying data."* So the arm moves `seed`
   24 to 42 and nothing else; `seed` sets model initialisation, batch order
   and the UMAP fit but **not** `data.splits.seed`, so the donor split and
   the scored cells are the base's. Overrides are byte-identical to
   `p1_dab168_kl1` and a new test asserts it. Bands are registered in the
   config before the run, as for every other arm. **Two runs give a range,
   never a standard deviation**, and Note 5's deltas get read against it:
   an ablation whose effect is smaller than the seed difference on the same
   axis must say so. The old r-series reasoning is kept below because it is
   why this arm is needed rather than reused.
   `r2_ref_s7.yaml` is "r2_ref again at seed 7, the error bar for the whole
   wave", and its own header says seed sets model initialisation, batch
   order and the UMAP fit but **not** `data.splits.seed`, so it bounds
   initialisation variability and not split variability. Two cautions
   before it is quoted: the R2 wave is explicitly not comparable to the
   p-series (corrected corpus, corrected circular encoding,
   tissue-stratified split), and **only `Outputs/r2_ref_s7/metrics.csv` is
   on disk locally** -- its partner `r2_ref` is not, so the delta cannot be
   recomputed here. **N3 currently says run-to-run variation "is not
   measured anywhere in the paper" and that needs softening** to: no
   replicate of the *reported* configuration exists, and the r-series pair
   is what bounds initialisation.

**Also done this pass:** `Supplementary Note~X` in the Discussion now reads
`Note~3`; `mcinnes2018umap` added to the bib; `\clearpage` after every
Note so floats stay inside it.

## The register pass on Notes 2 to 8, 15 November

`SUPPLEMENTARY_REGISTER.md` compares the notes against scGPT's twelve,
TIGON's nine and MIDAS's one, read in full, on tone, coverage and
usefulness. Five of the eight comparator papers ship no notes at all, so
the set is small and that is a fact about the field rather than a gap in
the reading.

**Eight surface fixes applied, commit `95f655a`.** No number, table, figure
or argument changed, and a numeric-token diff against the previous commit
confirms it.

| per 100 words | was | now | scGPT | TIGON | N1 (AW-edited) |
|---|---:|---:|---:|---:|---:|
| first person | 0.00 | 1.37 | 1.48 | 1.39 | 0.13 |
| connectives | 0.00 | 0.40 | 0.62 | 0.40 | 0.33 |
| semicolons | 0.80 | 0.11 | 0.06 | 0.00 | 1.06 |
| *rather than* | 0.34 | 0.15 | 0.06 | 0.00 | 0.33 |
| opens *The* | 40% | 24% | 18% | 14% | 36% |
| internal words | 77 | 3 | 0 | 0 | 0 |

Also: a summary paragraph closes every note, which none had and 13 of 14
published notes do; procedure precedes result in N5's five ablation
paragraphs and N7's protocols; N7's subsections are the questions rather
than the X numbers, which are kept in the ledger's third column.

**It got 8% longer, not 10% shorter** (8,491 to 9,170 words). The summary
paragraphs and the procedure sentences cost more than the antithesis cuts
saved. **`arm` was kept** where the main Results already uses it, at much
lower density; eliminating it would put the notes out of step with the
main text, and changing both is AW's call.

# 2. Ready to go now. No dependencies, no compute.

Ordered by what I would do first.

1. **The frontier and ablation UMAP figures.** The nine caches are at
   `Outputs/supplementary/umaps_supplementary/`, each with nine panels and a
   `_umap_cache/global_400000.npy`. These draw locally in seconds per arm.
   Covers `FIGURES_NEEDED.md` F4 and F5, and feeds Notes N4 and N5.
   ⚠ The caches used the RNG path, not the pin, because the job predates the
   pin; they are correct because HPC numpy 1.26.4 and local 2.2.6 were
   checked to draw identically (checksum 315692720845).
2. ~~**Note N1, gene-group sizing.**~~ **DONE.** Written, edited by AW,
   two figures drawn from the measured sweep, in `supplementary/`.
3. **Note N3, the limitations at length.** AW: *"Pour your heart out with all
   the limitations and clawing that you can. Here it makes sense because this
   section is when the reader has gone through the paper and understood the
   good side."* The Discussion's `Supplementary Note~X` resolves to this.
4. **Loss plots for all eleven arms.** `metrics.csv` is local for every arm
   with the full per-epoch breakdown. Feeds N4 and N5.
5. **Supplementary Tables.** The nine claims CSVs plus the benchmark files. A
   table belongs here only if it survives being separated from an argument;
   one that only means something inside a Note stays in that Note.
6. **The pseudocode box.** `docs/walkthrough/06` to `08`, reformatted.
7. **Figure 1's legend.** It describes five panels; there are four, and panel a
   has never been described at all.
8. **The Abstract.** No compute dependency and no blocker. AW's 11 November
   ruling puts it before the Introduction.

---

# 3. Blocked, and on what

| item | waits on |
|---|---|
| Note N9, X15 | the `--only-groups` probe job, outcome unknown |
| **AW's review of Notes 2 to 8** | **in progress**, he is editing N2 and N3 directly |
| The two Results pointers | **Supplementary Methods existing.** Until then they name headings that are nowhere |
| A seed replicate of the reported model | **`a1_seed42` is written and committed** (`axw1008` `ab7586a`), awaiting the GPU run |
| **Source Data** | the figures being final. Sheets are named per panel, so it cannot be written before the panels exist |
| Supplementary Table captions and numbering | the Notes, per the rule above |
| **References, whole paper** | the deferred citation pass below |
| Reporting Summary | pre-submission. AW's, and last |
| Results edits | **his Monday comments** |
| Introduction | nothing technical, but cheapest once the Abstract exists |

---

# 4. Decisions waiting on AW

1. **Is the rho = +0.721 asymmetry cut on purpose?** It left Results for the
   Discussion, then left the Discussion when the metrics paragraph was cut, so
   **it is now nowhere in the paper.** It was importance 9 in the inventory and
   its job was to explain why our cycle advantage cannot be identity leaking
   through. Restore in a clause, move to a Note, or drop deliberately.
2. **F2 and F3: one figure or two?** Two main-text additions take the paper to
   NMI's six-item cap exactly. One two-panel figure keeps it at five and pairs
   the mechanism with its consequence. Undecided.
3. **Figure 2's redesign**, which AW wants discussed before any drawing. It
   competes with the supplementary figures for the same effort.
4. **The dissociation panel's home**, Figure 3 or Extended Data. It surfaces a
   number the paper does not carry: whole-corpus surgical stage $+$0.3320 at
   $p=0.005$ over 58 donors, against the held-out 0.1313 at $p=0.303$. Either
   it goes into Results or the row comes out of the panel.
5. **THE LEAK IS REAL AND MEASURED. `audit/SPLIT_LEAK.md`, 15 November.**
   AW was right and my earlier account was wrong. The donor split is clean
   (no `patient_id` in two splits, no alias pair straddling the wall, no
   duplicate cells), but **the cross-donor estimator discards same-donor
   neighbours by IDENTIFIER**, and fifteen people hold two. So same-person
   relations inside the held-out split are scored as cross-donor. That is
   the cell-level leak AW remembered.
   **Size: 2.83% of cross-donor relations on phase, 2.00% on disease.**
   Every correction moves against us: phase $-$0.0121, disease $-$0.0173,
   donor recovery $+$0.0065 (worse). Cell family, severity, stage and grade
   have **zero** exposure, because both deposits carry a phase label and
   nothing else.
   **The decision, and it is not a wording one.** (a) re-score all eleven
   representations with aliases resolved in the scorer, which needs no
   retraining because the latents are dumped; (b) report as is and state
   the bound in Note 3; (c) drop the four dual-identifier people, losing
   12.3% of the held-out split. **The correction must be applied to all
   eleven or to none** -- a corrected \elaj{} against nine uncorrected
   competitors would be worse than reporting none of it, and on scaled
   numbers our phase lands near Scanorama's. AW's review of the Notes is
   expected to carry his own comment on this; nothing has been edited.

---

# The display items, settled 11 November

**Four, and the order is the argument's order.** AW overruled the supervisor's
"fig 4 becomes fig 2": the model has no credibility on the UMAPs until the
frontier has been explained.

| | what it is | change |
|---|---|---|
| Fig 1 | graphical abstract, architecture, frontier, cell-family latent | none |
| Fig 2 | **the frontier** | stays, but **must stop looking like a benchmark** |
| Fig 3 | **the nine endometriosis UMAPs** | was Fig 4, renumbered |
| Table 1 | every arm | none |
| --- | both latents by family and phase | **was Fig 3, goes to Supplementary** |

- [ ] **The renumbering.** `figure4.py` becomes Figure 3. Script names match
      paper numbers, so this renames files, captions, every `\ref`, and both
      auditors' pins.
- [ ] **Every panel referenced in prose.** Figures 2, 3 and 4 still have panels
      no sentence points at.
- [x] Figure 1 panel c's clipped x-label. An assert now fails the render.
- [ ] Figure 1 is 213.5 mm tall. It fits, but it is close to a full page.

**The figure register is in `FIGURES_NEEDED.md` and is not re-derivable
cheaply:** Arial throughout, 180 mm maximum width, panel letters 10 pt bold,
titles 6.5 pt, body 5.5 pt, nothing below NMI's 5 pt floor once placed.
Okabe-Ito for cell families, eleven study hues with the yellow-olive-brown band
removed. **Size the layout to fit the type, never the type to fit the layout.**

---

# Citations, a whole-paper pass

- [ ] **CITATIONS IN THE SUPERVISOR'S FILE ARE DEFERRED, AW's ruling,
      14 November.** *"We have citations in the right place in our local tex
      files. We will both add all references in the correct and edit the file
      to add citations in the correct place. You'll just have to give me
      pointed changes then."* So it is **one later pass over his whole file**,
      delivered as **pointed find-and-replace changes naming each location and
      its number**, never another wholesale paste. Until then his Results has
      no citations at all, because pandoc dropped every `\citep` from the
      13 Nov batch, and his Discussion carries author-year brackets.
      `sections/*.tex` is the authority on placement.
- [ ] **The paper is under-cited throughout**, AW's own observation. The
      Discussion now cites 18 unique references, up from one. The Introduction,
      Results and Methods have not had that review.
- [ ] **`Supplementary Note~X`** is referenced from the Discussion's
      limitations paragraph and must resolve: overlapping donor identifiers,
      the single cycle-day cohort, the unstratified permutation null.
- [ ] **Two bib entries are incomplete.** `kedzierska2025zeroshot` has no
      pages; `duempelmann2026endometrium` has neither volume nor pages.

---

# Mechanical, none of it blocking

- [ ] Numbered references in the DOCX. `make_draft.sh` is wired for
      `assets/nature.csl` and AW is fetching it.
- [ ] Reference format per NMI: sequential across main text, Methods and Data
      availability; article titles required; URLs parenthetical.
- [ ] Extend both auditors to Methods.
- [ ] `vasilevsky2022mondo` and `czi2023cellxgene` are preprints; check for
      journal versions.
- [ ] Six references cited zero times.
- [ ] One unnamed skipped test in the suite of 1,945.
- [ ] `probe_stages.sh`'s preflight prints no numpy version, which is why the
      index-draw check had to be run by hand. Add it when next touched.
- [ ] **Run documentation in the GitHub repository**, the supervisor's third
      batch. The scripts are committed; what does not exist is a page saying
      how to run them. Bears on Code availability.

---

# The handover workflow

- [ ] **REMINDER FOR AW, 14 November: the guide's Word doc does not yet carry
      the X13 additions to Results and the Discussion.** Both sections were
      shipped as wholesale docx replacements BEFORE X13 landed. The Results
      paragraph (label transfer, "Those two annotations agree.") and the
      Discussion refutation sentence beside the Huang contradiction are only
      in the `.tex`. Supplementary Data on OneDrive IS current (AW, 14 Nov).


1. change the `.tex`
2. build the Word file
3. hand AW the changeset; he applies it in the guide's OneDrive copy

**Shipped:** `ELAJ_results_2026-11-13.docx` and
`ELAJ_discussion_2026-11-14.docx`, both wholesale replacements, both maths-free
so character formatting survives the paste. Batch 2026-11-10 is with AW and not
confirmed applied; Figure 1 has changed since, so the next batch must carry the
new image and legend.

**Supplementary Data for OneDrive is built and sent:**
`Outputs/supplementary/send/ELAJ_Supplementary_Data.xlsx` (D1, D2, D3, D5 as
four sheets) plus `D4_transferred_cell_family_labels.csv.gz` separately,
because 1,577,728 rows exceeds the xlsx cap of 1,048,576.

# The supervisor's comments still ours

`[97]` rephrase the pooled-corpus paragraph, `[42]` the abstract abbreviation,
`[82]` trials or studies, `[503]` and `[511]` in *Data collection*. Most are
absorbed by the Introduction and Abstract rewrites.

**His to clear**: `[132]`, `[467]`, `[507]`.

**To discuss in person**, both synced into the tex as he made them: the "pain is
a recurring date on a calendar" opening, and the human-health paragraph.

**Third batch, 14 November**: run documentation in GitHub; supplementary filled
to the brim; Results reviewed Monday. Verbatim in `REVIEW_FEEDBACK.md`.

# Externals, AW owns all of these

Repository URL, licence, Zenodo DOI, funding and grant numbers, final author
list, Reporting Summary, cover letter, bioRxiv preprint.


# Supplementary Methods, opened 15 November

**AW's ruling: the Methods material Results points at goes here**, not into
the main Methods. Four known items, two of them already written elsewhere.

| item | state | source |
|---|---|---|
| **Label transfer** | **needed**, Results points at it | N6 has the whole procedure; this is a trim, not new writing |
| **Severity** | **needed**, Results points at it | the three-level merge and the two study vocabularies; `groupings.py` holds the maps, D3 ships all three forms |
| The gene-group construction, in full | AW's own request | N1 states the outcome; the cut itself (Reactome first, GO on the residual, 250 to 500) is Methods, *Pathway gene grouping* expanded |
| Training hyperparameters, with a table | AW's own request, moves out of Methods | the six shared configuration files; one generated table like the Notes' |

**Order inside it follows the main Methods**, so a reader can map one onto
the other. Two comparators do the same and both put Supplementary Methods
after the Notes: MIDAS has four subsections there, TIGON folds its
derivations into Note 1 instead.

⚠ **Both Results pointers are wrong until this section exists.** They read
`(Methods, \emph{Label transfer})` and `(Methods, \emph{Severity})` and
must become `(Supplementary Methods, ...)`. That is a two-string change in
`02-results.tex` and it should land in the same commit as the section. 