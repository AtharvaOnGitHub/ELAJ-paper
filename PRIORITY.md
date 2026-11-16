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
| `probe_stages.sh` to `p1_groups` | **X15**, now Note 7 | 2 d GPU | **DONE 16 Nov**, job 61861150, exit 0, 13:26:46 of the 2-day wall. All 44 groups scored and the integrity row is exact |
| `train.sh a1_seed42` | the seed band for Notes 3 and 5 | ~10 h GPU | **TRAINED 16 Nov**, job 61860514, exit 0, 8:44:23. **NOT YET SCORED**, see below |

**On the UMAP caches**: the job ran before the index pin was committed, so it
took the RNG path. That is fine, because HPC numpy 1.26.4 and local 2.2.6 were
checked to produce the identical draw (checksum 315692720845). The pin protects
future runs; it did not make these ones correct.

**X15 timed out twice and the second diagnosis is the one that matters.**
The first run spent sixteen hours inside `groups/concat` (12,672 wide, not
the 1,408 I assumed), which `--only-groups` now skips. The second ran
sixteen hours and scored 38 of 44 groups of the FIRST of three reference
families, with not one row about the model. Two causes, both fixed in
`axw1008` `a99d052`:

1. **A bug.** `group_battery` emptied `cross_donor_labels` and `scib_labels`
   but left `settings.stages` at its default, and `mixing` and `disease` are
   dispatched from `stages` and read `corpus.study_id` and `disease_status`
   directly. Every per-group stage ran the eleven-study purity sweep and the
   three-way disease contrast: **25 rows where the function intends 2.**
   Measured: the two kNN labels took 5.5 of each stage's 24 minutes.
   Now `stages=("knn",)`, with a regression test.
2. **`--no-references` was not passed.** The flag's own help says the two
   per-group PCA reference families are two thirds of the cost and say what
   the baseline table already says. They run first and ate the wall.

Also: `--only-groups` now keeps the `latent` row, the script's own integrity
check against the benchmark's elaj row, 16 wide against the group stages'
288. Wall 16 h to 2 days: 44 stages at 288 wide is roughly 36 hours.

```
cd /rds/homes/a/axw1008/axw1008 && git pull && sbatch data_collation/scripts/probe_stages.sh p1_dab168_kl1 --runs-dir outputs/p_series --splits val test --only-groups --no-references --out outputs/probes/p1_groups
```

**Do not cut `--splits` to save time**, and **move the old `p1_groups`
directory first** if the 38 `counts_raw` rows are wanted: the new run writes
to the same path, and only their `knn-agreement` rows are comparable to what
the fixed battery produces.

**scIB is resolved without a rerun.** Job 61784251 computed every `cell
family` metric, then OOM-died on a second label set we do not use, so it
never wrote its CSV. **silhouette_batch = 0.754**, and all seven metrics it
shares with the original pass reproduce to the printed precision, so it is
comparable. `scib_table.py` parses it out of the log, which is kept where
that CSV would have been, and prefers the CSV if it ever appears. The
scorecard has no empty cell.

---

# 1a. Both jobs landed, 16 November

## The probe: done, clean, and its integrity check is exact

`Outputs/probes/p1_groups`, job 61861150. All 44 groups scored on cell
family and menstrual phase, at width 288 each. **The `latent` row matches
the benchmark's \elaj{} B\textsubscript{hi} row to the last digit on all
six axes** (cycle 0.7346, family 0.9820, donor 0.5188, $k$NN family 0.9864,
disease 0.3364, study mixing 0.7613), which is the whole reason that row is
computed: it proves the probe is scoring the same cells with the same
estimator as Table 1.

**What it found.**

| | |
|---|---|
| cell family across the 44 groups | 0.3305 to 0.9695, median 0.7748 |
| menstrual phase across the 44 groups | 0.3051 to 0.7341, median 0.5690 |
| groups beating the 16-dim latent | **0 of 44 on either label**, though each group is 288 numbers wide |
| best group on both | `reactome_complement_cascade_plus_9_more` |
| worst group on both | `reactome_sensory_perception`, which is the sanity check |

**The headline is the third row.** The latent is sixteen numbers and every
group is 288, so the comparison favours the groups, and the latent still
wins on both labels. The latent is therefore not a copy of its best group;
the compression across 44 of them adds something.

⚠ **One caution to write into the note rather than discover later.** Family
and phase excess correlate across the groups at $\rho = +0.665$,
$P < 0.0001$. The ordering is not label-specific, so part of what this
measures is how much transcriptional signal a group carries at all rather
than anything pathway-specific. Say so.

⚠ **`counts_raw`, `counts_log` and every `delta` column are empty**, because
`--no-references` was passed and the two per-group PCA reference families
are what fill them. That was the deliberate trade that let the job finish
inside the wall. So the note can say what the groups carry and **cannot**
say what tokenisation costs against raw counts. Filling them is roughly two
thirds of the job's cost again, and is AW's call.

## The seed arm: trained, verified, and still needs its benchmark row

`Outputs/a_series/a1_seed42`, job 61860514. Eight epochs, early stopping,
best epoch 2 against the base's epoch 4 of 10.

**It is a clean pure-seed replicate, checked two ways.** All 46 keys in the
YAML `overrides` block are identical to `p1_dab168_kl1`'s, and seed is 24
against 42. `run_config.json` appears to differ on
`model.tokens.dns_embedding`, `None` against `True`, and that is a
**recording artefact, not a model difference**: the key is in neither
YAML, `ModelConfig` defaults it to `True`, and `a1_noecs` records `True`
for the same reason. Both runs ran with the sentinel on.

**The training curves nearly superimpose.** `train_nb` is within 0.0008 of
the base at every shared epoch (0.4129/0.4137, 0.3868/0.3871, 0.3824/0.3824,
0.3801/0.3800, 0.3786/0.3785, 0.3777/0.3778, 0.3771/0.3770, 0.3767/0.3768).

**But there is no benchmark row for it anywhere**, verified by search. What
`metrics.csv` holds is the per-epoch validation readout at $k = 30$ on
19{,}972 cells, which is a trajectory and not quotable. Notes 3 and 5 need
the $k = 100$ cross-donor battery on the full 416{,}256-cell held-out
split, and that is two jobs, both measured from the identical pair that
produced `full_a1_clsonly`:

```
cd /rds/homes/a/axw1008/axw1008 && git pull && sbatch data_collation/scripts/benchmark_baselines.sh a1_seed42 --runs-dir outputs/a_series --methods none --dump-latent outputs/benchmarks/latents_elaj/a1_seed42 --dump-only --out outputs/benchmarks/_emb_ho_a1_seed42
```

GPU, measured 20:40 on the same step for `a1_clsonly`, 2 h wall. **Then**,
once it has written the latent:

```
cd /rds/homes/a/axw1008/axw1008 && sbatch data_collation/scripts/benchmark_cpu.sh a1_seed42 --runs-dir outputs/a_series --methods none --external-latent /rds/homes/a/axw1008/axw1008/src/outputs/benchmarks/latents_elaj/a1_seed42/elaj__native__train --out outputs/benchmarks/full_a1_seed42
```

CPU on bbdefault, measured 50:51, outside the bbgpu cap. ⚠ **The result has
to land locally at `Outputs/benchmarks/full/full_a1_seed42/benchmark.csv`**,
which is where `table1.collect()` reads the a-series from.

⚠ **`a1_seed42` is deliberately NOT in `table1.A_SERIES`.** It is an error
bar, not an arm, and adding it would put a twelfth row in Table 1. If AW
wants it in the table that is his call and a separate change.

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
| **Notes 2 to 6** | **EIGHT NOTES ARE NOW SIX**, AW's 17 Nov review applied in full. N2 is "okay" in his words. See the section below |
| Note 7, X15 | waits on the `--only-groups` probe job. It is **Note 7** now, not Note 9 |
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

## AW's review of Notes 2 and 3, applied 16 November (`2f517e5`)

**N2.** A primer on what the ten metrics ask, before any number. The
constant-metric subsection rebuilt as the process: columns constant, we
suspected the implementation, we checked the definitions, the cause was the
corpus. cLISI separated from cross-donor cell family, which he found
confusing and which are genuinely different tests. The batch-metric
paragraph reordered to mechanism, then the failure the design permits, then
this corpus, then cross-donor. Fig S5's legend is his wording.

**N3.** The whole-corpus paragraph carries the measurement. Donor chance
rate corrected: **70 identifiers held out, not 269**, and the chance rate is
not where the error is -- the agreement is. Label coverage and null width
make their point rather than restating their tables. His cycle-day query
resolved: **duempelmann supplies its own phase column, so no day-to-phase
conversion happens anywhere**; the paragraph keeps the real point, that
cycle length varies and endometriosis alters it. His two `[reference]`
placeholders filled. He had already cut the four-families paragraph; its
echo in the closing summary went too.

**Figures.** scIB heatmap removed and Table S5's columns folded into the
range figure (⚠ his two bullets on this conflict; the reading taken is in
the commit message and needs his confirmation). Label coverage redrawn
against the corpus rather than against each study. Null widths connect each
label across its scopes. S10 and S11 dropped. Bar colour encodes the knob.
Per-family AUC is now an IBDex Fig. 2c forest plot with aligned numbers.
**UMAP panels: one figure per model, cell family / study / menstrual
phase**, replacing seven single-colouring figures.

**Two bugs a render caught and no build error would.** `\thesection`
already expands to the whole phrase, so "Supplementary Note~\ref{}" printed
it twice, 16 times. And a caption said red marked the absent cycle days,
which are zero-height bars.

## AW's second supplementary review, applied 17 November

**His one-line rule, and it is the heading for all of it:** *"Prose is for
observations, tables are for numbers, figures are for intuition."*

**Eight notes are six.** Files track Note numbers, so N7 became
`N6-claims-axis.tex` and the X15 note is Note 7 when it lands.

| | what changed |
|---|---|
| **N2** | one dead reference repointed. AW: "Note 2 looks okay" |
| **N3** | Table S8, the null widths, removed; the figure makes the point and the caption now stands alone. **Note 6 folded in**: the label transfer is three paragraphs under *Limits of the claims axis* with ONE table (validation) and ONE figure (distance by group), the four other transfer tables gone. *Every configuration is a single run* rewritten off the prediction bands and onto what a seed replicate would bound |
| **N4** | *Every arm on every axis* was a readout of its own table; now *The two coefficients do different things*, which states the two patterns and leaves every value in the tables. Table S13 and all prediction-band prose gone. The \elaj{} B\textsubscript{hi} UMAP figure gone |
| **N5** | prediction bands and *what we did not ablate* gone, prose and tables. Two standalone disease UMAPs gone, since disease is now a panel. Every base-model comparison points at main-text Fig.~4 |
| **N6** (was N7) | **Note 8 folded in** as *Do marker signatures reproduce across cohorts?* |

**Every multi-panel UMAP now carries disease status**, four colourings in a
2x2 at 180 x 208 mm, one full page each. Ten figures, the reported arm drawn
into the exploratory tier only.

**Counts**: 38 tables to 30, 41 figures to 36, 58 pages, zero overfull, zero
undefined. Both main-text auditors still green.

⚠ **Still needs AW's confirmation, carried over from the 16 Nov review:**
the Fig S4 / Table S5 reading, where his two bullets conflicted.

⚠ **One fact left the document with Note 6** and may be worth a sentence
somewhere: `garcia_alonso_2021_b` transfers 99.9% epithelial, which
identifies it as an epithelium-sorted deposit rather than whole tissue.
`supp_figures.py --only transfer` still prints it.

---

## The figure pass, AW's second review, 17 November

**His rule, and it governed the prose pass too:** *"Prose is for
observations, tables are for numbers, figures are for intuition."*

| his comment | what was done |
|---|---|
| UMAP panels 1x4, not 2x2, "all UMAPs are squished" | 1x4 at 180 x 70 mm, and every axes set to `aspect="equal", adjustable="datalim"` so the embedding is never stretched to fit the box. Panel letters **a**-**d** added |
| loss curves illegible, three lines share a colour | every line now carries its model's name at its own right-hand end, de-collided by `label_lines()`. Colours unchanged, as he asked. Applied to the trajectories too |
| S9 jumbled top left | the Spearman inset moved to a boxed bottom-left corner, and point labels de-collided in display space by `label_points()` |
| S3 words too small, whitespace | the fault was the aspect: a 150 mm axes with numeric columns to fraction 1.52 made a 250 mm figure that `\textwidth` scaled to 0.64. Axes now 95 mm |
| S5 not referenced | ⚠ **IT IS**, at N2's "The two \elaj{} models make that mechanism visible". **Not removed; see the question below** |
| S19 crowded, keep only \elaj{} B\textsubscript{hi} | the nine comparison methods and five other frontier arms are gone. One base point, five arrows |
| S31, S32 unreadable | same aspect fault as S3; axes 88 mm and placed at `\textwidth` instead of 0.65 |
| S33 messy | the fifteen labels are gone, because Tables S26 and S27 already name those genes. What stays is the shape of the ranking, which only a figure can give |
| S29, what point | removed with the whole severity subsection |
| S34 hard to interpret | removed. Table S26 makes the point |
| S35/S36 illegible | merged into one two-panel figure at 165 mm, in ink rather than grey |
| Table S28, barely any numbers | removed. Two rows under six headings, four of them dashes. Its four values are in the sentence and the legend, and the script prints them |
| figures with no reference | audited with captions excluded; four UMAP panels and three tables were orphans, all now cited. Eight orphan PNGs deleted from `supplementary/figures/` |
| legends severely lacking | `REGISTER.md` has a new section read off IBDex and scGPT. **Every figure legend rewritten**, 100 to 200 words, panel by letter, each number against its comparator |

**A NEW CHECK, and it catches a fault LaTeX cannot see.**
`figures/scripts/check_figure_scale.py` runs from `build_supp.sh` and fails
on any figure whose smallest type would land under NMI's 5 pt floor **where
it is placed**. Every one of AW's four "illegible" complaints was this. It
also found nineteen font literals between 4.2 and 5.0 pt in
`supp_figures.py` that are under the floor even at 1:1; there is now a named
`FS_LEG = 5.2`.

**Claims note.** AW: *"The claims axis note is about the claims not
discussed in the main prose."* The severity subsection is gone, and so is
*Does composition differ between patients and controls?*, since Results
gives all four of its $P$ values. **Both dropped contrasts are still
computed and printed** by the generator, so the ledger's outcome column has
a derivation. ⚠ **Two more subsections may fall under the same rule; see the
question below.**

**State:** 51 pages, zero overfull, zero undefined, figure-scale check
green, both main-text auditors green. 30 tables to 26, 36 figures to 32.

### ⚠ Two questions for AW, both blocking nothing

1. **Fig S5.** It is referenced, at N2's *"The two \elaj{} models make that
   mechanism visible"*. It is also the only place the two arms are shown
   against the nine others' median, which the prose does not give. **Left
   in, legend rewritten. Remove it and the sentence, or keep?**
2. **How far does "claims not discussed in the main prose" reach?** Taken
   literally it also removes *Where in the latent does the disease live?*,
   *Which genes does the immune direction move?* and *Do marker signatures
   reproduce across cohorts?*, since Results gives each in full. **They were
   kept**, because the same message asked to fix S31, S32, S33 and S35/S36,
   which are those subsections' figures, and because Note 8 was folded into
   this note one message earlier.

---

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
| **AW's review of Notes 4 to 8** | his read. N2 and N3 are done |
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

1. ~~**Is the rho = +0.721 asymmetry cut on purpose?**~~ **NOT A DECISION. It
   is in the paper.** Supplementary Note 3, *Disease agreement is partly a
   readout of donor memorisation*, states it at rho = +0.721, P = 0.019 with
   the cycle's +0.176 beside it and Table S8 under it. AW, 17 November: *"Are
   you sure rho is not in supplementary?"* I had claimed it was nowhere
   without grepping. The only live question is whether it also wants a clause
   in the main-text Discussion, which is AW's call and is not a blocker.
2. **F2 and F3: one figure or two?** Two main-text additions take the paper to
   NMI's six-item cap exactly. One two-panel figure keeps it at five and pairs
   the mechanism with its consequence. Undecided.
3. **Figure 2's redesign**, which AW wants discussed before any drawing. It
   competes with the supplementary figures for the same effort.
4. **WHERE THE CYCLE-AXIS FIGURE GOES.** AW, 17 November: *"The cycle axis
   figure needs to be in the paper. Not sure where yet."* It is drawn and
   cited from Results (`figures/x16_cycle_axis_external.png` and
   `x16_cycle_closes.png`, generated by `supp_figures.py --only x16`), and
   Results carries a `(Fig.~X)` placeholder for it. **The constraint: NMI
   caps display items at six and the paper currently has four**, so one
   figure of two panels fits without touching the cap, two separate figures
   take it to six and close it. My reading is one figure, the external
   validation beside the closed loop, since they are one argument. The
   alternative is Extended Data, which has nine slots open, but the result
   is strong enough that it belongs in the main text.

5. **The dissociation panel's home**, Figure 3 or Extended Data. It surfaces a
   number the paper does not carry: whole-corpus surgical stage $+$0.3320 at
   $p=0.005$ over 58 donors, against the held-out 0.1313 at $p=0.303$. Either
   it goes into Results or the row comes out of the panel.
6. **THE LEAK IS REAL AND MEASURED. `audit/SPLIT_LEAK.md`, 15 November.**
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
   **Measured on both scopes, 16 November.** Held out: 2.83% of relations
   on phase ($-$0.0121), 2.00% on disease ($-$0.0173), donor recovery
   $+$0.0065 worse. Whole corpus: 1.54% on phase, $-$0.0071, which is about
   **1% of the reported figure's own value**. Family, severity, stage and
   grade have **zero** exposure on both scopes, structurally, because both
   deposits are control endometrium carrying a phase label and nothing else.
   Every correction moves against us. **Note 3 states this as a measured
   bound, in AW's own edited wording, down to "the error is smaller than any
   inter-representation difference". Option (b) is TAKEN, not provisional,
   and the paper is complete without anything further.** AW, 17 November:
   *"Didn't you add split leak info to the supplementary note on
   limitations? Why the pending question?"* He was right to ask; I had
   reported the document's state without reading it.
   **The one thing still open is whether to spend (a): re-score all eleven
   with aliases resolved in the scorer** -- no retraining, the latents are
   dumped. It is an upgrade, not a repair. It must
   be all eleven or none: a corrected \elaj{} against nine uncorrected
   competitors is worse than reporting none of it, and on scaled numbers our
   phase lands near Scanorama's.

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
      auditors' pins. ⚠ **AND `supplementary/notes/`**: since 17 November the
      supplementary points at main-text Fig.~4 in nine places, because every
      \elaj{} B\textsubscript{hi} UMAP was removed from it in favour of the
      main-text figure. `grep -rn 'Fig.~4' supplementary/notes/` finds them.
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