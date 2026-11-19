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
| Abstract | **DONE and AW-edited, 17 Nov.** 188 words. Third rewrite; the first two were thrown out, see CONTINUITY |
| Introduction | **DONE and AW-edited, 17 Nov.** 662 words, 19 citations, against the guide's five pointers |
| Results | drafted 13 Nov, X13 and the X16 cycle paragraph added since. **Not re-read by the supervisor** |
| Discussion | written 14 Nov, X13, the X16 sentence and AW's grouping future-work note added since |
| Methods | done, 5,745 words, tweaks only |
| Supplementary | **six notes, 51 pages**, zero overfull, zero undefined, figure-scale check green. Note 7 (X15/X16) not written |
| Extended Data | one item, PRISMA. Nine slots open |

⚠ **THE MAIN TEXT IS OVER THE CAP.** Introduction 662, Results about 2,190,
Discussion about 1,100, so roughly 3,950 against NMI's 3,500. Results carries
the excess. The abstract sits outside that count.

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

# ⓪ STATE AT COMPACTION, 17 November late — read this first

## The one thing in flight: the gene ranking, redone correctly

**The full record of what went wrong, with job IDs, numbers and commits, is in
CONTINUITY.md, section *THE GENE-DISEASE RANKING: the full record*. Read it
before acting on anything gene-level.**

**Both existing gene rankings are INVALID.** The 12 Nov ranking
(`x12_gene_shifts_orth_MISMATCHED_epoch9_decoder.csv`, macrophage genes,
the Zhao 4/15) decoded the epoch-4 latent with the epoch-9 decoder (the
wrapper took `ls -t | head -1`). The "corrected" epoch-4 ranking now sitting
in `axw1008/docs/paper/x12_gene_shifts_orth.csv` (T/NK genes: XCL1, KLRB1,
CD3D ...) is ALSO invalid: `decode_sanity` (job 62036623) showed the decode
path inverts identity at both epochs, because the script fed the decoder
ALL-ZERO covariates and the reported model NEVER saw that state (covariate
blanking only runs when the drain is enabled; `train_blanked_covariates` is
0.0 every epoch). The decoder is log_mu = gain(cell) x (k(cell).q(gene)) + b,
and gain depends on the covariates, so zeroing them can flip the profile.

**What is running (AW submitted both after `c6d5f79`):**

| job | script | what it writes | what to do |
|---|---|---|---|
| `decode_real` | `axw1008/src/scripts/decode_real.py` | log `logs/decode_real_<id>.log`; six files `src/docs/paper/x12_gene_shifts{,_orth}_realcov_centre-{study,none,controls}_epoch_0004.csv` | read the log: step 3 (encoded vs dumped latent, stops above 0.05), step 4 Test A (>= 5/6 markers per side, stops otherwise), step 5 step-size rho, step 6 gain sign flips. Then see below |
| X17 | `disease_genes_expression.py` (+ `.sh`) | `src/outputs/analysis/x17_pseudobulk/` (groups.csv, pseudobulk.npz, measured_by_study.csv) | copy back; run `python scripts/disease_genes_expression_analysis.py --in <dir>` locally |

`decode_real` encodes ALL 29,355 labelled immune cells (control/eutopic,
duempelmann + marecko, all splits; AW's standing rule: non-input metadata
uses the whole corpus) with their REAL tissue/platform/study/library and
shifts the latent through `model.decode_once(..., z_proj=...)`.

**When `decode_real` passes its checks, in this order:**
1. Copy `x12_gene_shifts_orth_realcov_centre-study_epoch_0004.csv` over
   `axw1008/docs/paper/x12_gene_shifts_orth.csv` (study-centred,
   orthogonalised is the paper's method; AW asked to SEE all six, so show
   the other five side by side, gene by gene, not as summary stats).
2. **Biological sanity check before anything else.** The disease direction
   is essentially the myeloid share of the immune compartment (donor
   position vs lymphoid share, Spearman -0.93; patients have fewer
   lymphoid: Dümpelmann 0.41 -> 0.27, P 0.087; Marečková 0.85 -> 0.73,
   P 0.021). So genes rising towards disease should look MYELOID. If they
   do not, stop and say so.
3. Show AW the top 30 and bottom 20 genes with what each is and whether it
   is known in endometriosis (Open Targets file and X19 corpus-paper file
   are local). AW: "This cannot be glossed over ... Are we discovering new
   genes?"
4. Rerun everything downstream of the ranking: `replication_external.py`,
   `external_references.py` (X18), `supp_figures.py --only claims`,
   `supplementary_data.py`, `figure2_draft.py`, `figure2f_tall.py`.
   Then update Note 6's EndometDB sentence (its rho is from the invalid
   ranking) and check whether Fig 1a's fifth outcome row survives.
5. Run the X17 analysis. Its rule was fixed before data: HELD OUT studies
   (li_2025 excluded, it is follicular fluid), immune cells chosen by
   MEASURED PTPRC > 0 (never ELAJ's transferred labels, AW's point), top 15
   of the canonical ranking, >= 11/15 higher in patients AND sign P < 0.05,
   else NOT SUPPORTED. Transferred-label and FIT cohorts reported beside.
6. Then, and only then, rewrite the gene prose.

**UPDATE 18 Nov: steps 1-5 DONE, the gene prose plan is set (do not write
it until B's decode reports).** Canonical ranking = `x12_gene_ranking.csv`
(`gene_ranking.py`: study-centred, NOT orthogonalised, expression floor 0.1
per 10,000 reads; AW: "Take whatever is recommended"). X17: FIT 14/15, sign
P 0.0005, Spearman +0.69; HELD OUT (lin_2023 + tan_2022, 25 donors) 5/15,
P 0.94, NOT SUPPORTED. Within-lineage directions (B): myeloid AUC 0.7594
P 0.0425; lymphoid 0.7054 P 0.080. B's decode (`decode_real --within`) is
the next cluster job.

**VERIFICATION OF (4) BELOW, 19 Nov, AW asked to be sure. It does NOT hold
as an immune-cell result.** All donors together: stromal RNA is raised in
patients' EPITHELIAL (x1.92, P 0.001) and ENDOTHELIAL (x1.71, P 0.0001)
cells as much as in immune cells (x2.07), and stroma IDENTITY genes
(HOXA10/11, PGR, PDGFRA) rise as much as collagens, so it is a SAMPLE-level
excess of stromal RNA, not an immune state. Not doublets (doublet
percentile unchanged, P 0.40/0.64; excess survives removing the most
doublet-like half). Not the MMT of Zhong et al. 2025 (Mol Hum Reprod,
gaaf051): TGFB1 lower in patients' immune cells (x0.86), myofibroblast
genes weak (x1.45, P 0.038). Removing each cell's stromal score from the
latent: immune held-out AUC 0.763 -> 0.738 (P 0.015, SURVIVES); myeloid
0.725 -> 0.670 (P 0.115); lymphoid 0.679 -> 0.488. Per FAMILY, no study
step (held-out AUC, then with each cell's stromal score removed): immune
0.763 -> 0.738 (P 0.015); stromal 0.710 -> 0.691 (P 0.030); endothelial
0.758 (P 0.010) -> 0.594 (P 0.22); epithelial 0.667 (P 0.062) -> 0.614.
Robust: immune and stromal. Endothelial's separation WAS the stromal RNA.
DRIVERS (disease_axis_drivers.py): immune axis = lymphoid share (rho +0.96;
myeloid genes AIF1, HCK, SPI1, TYROBP vs T/NK TRBC1, KLRB1, KLRD1, RUNX3)
and phase (patients 13/17 periovulatory+proliferative heavy, controls
secretory heavy); phase removed -> AUC 0.680, P 0.080. Stromal axis =
sequencing depth (log library rho +0.69, ribosomal genes on control side)
and phase (P 2e-5); phase removed -> 0.678, P 0.070. Library size itself
does not differ by status (P 0.11 stromal). Decision with AW.

**AW's RULING, 19 Nov, which reframes the whole gene claim.** "The paper
is about that tool." (1) Cell proportions from labels, outside the latent,
are batch-affected and NOT results. (2) Composition read through the latent
(macrophages up, NK/T down) is reliable but bulk-reachable: corroboration,
briefly. (3) The within-myeloid sub-composition (resident macrophage vs
DC/mast) is a proportion statement the studies' finer annotations could
give: not an ELAJ result. (4) **Stromal transcripts in patients' immune
cells, found along a within-lineage latent direction and confirmed in
counts, is the first result only a single-cell atlas could give. It is to
be developed. Not to be hedged as contamination** (measured defence:
epithelial RNA in immune cells x0.95, P 0.63; the excess is x1.6 beyond the
donor's own stroma, P 0.0004). (5) Gene lists are not our job; X17 and the
decoded lists become supporting material.

**B's decode REPORTED, 19 Nov (job 62116534, `decode_real --within`;
all checks passed; files `axw1008/src/docs/paper/
x12_gene_shifts_within-{myeloid,lymphoid}_realcov_epoch_0004.csv`, committed
by AW in `8e4f969`).** Raw top genes in BOTH lineages are stromal
(collagens, SFRP4, POSTN). Measured counts, POOLED ACROSS ALL DONORS
with no study step (AW, 19 Nov: "The method needs to not care about
study"): stromal genes in patients' IMMUNE cells x2.07 (48.8 vs 23.5 per
10k, MWU P < 0.0001, 44 vs 50 donors); in patients' STROMAL cells x1.34
(P 0.0006); immune level divided by the same donor's stromal level 0.168
vs 0.103, P 0.0004. So the excess is NOT explained by the stroma alone:
it is a disease-associated difference in immune cells. AW's point: noise
that is the same in every cell cannot make a disease axis; this is not the
same. Source (contamination that differs with disease, doublets of
interacting cells, or immune-stromal biology) not determinable here. My
earlier "signature of ambient contamination" (from within-study averaging)
is WITHDRAWN. X17's own statistic is within-study weighted (fixed 17 Nov);
raised with AW. Restricted to 794
immune-specific genes (>= 0.1/10k and > 2x every other family):
within-myeloid disease end = resident/lipid macrophage (GPNMB, LYVE1,
SIGLEC1, MAF, LPL, ABCA1), control end = DC/mast/lymphoid (CCR7, HLA-DR,
CCL17, TPSAB1, CD3D, CD79A): sub-composition within the label.
Within-lymphoid control end = activated NK/T (IL1A, XCL1/2, TNF, IFNG,
CCL3/4, GNLY, NKG7, KLRD1, CRTAM), i.e. patients' NK/T less activated;
disease end = macrophage genes in lymphoid-labelled cells (C1Q, CD163,
LYVE1). Awaiting AW's decision on how B is reported.

**How the paper reports A (AW, 18 Nov, verbatim intent):** the paper states
exactly *"From this test alone we cannot tell whether the pattern is
specific to those two cohorts or whether 25 donors is too few to see it."*
Summarised in Results and the Discussion IN PLACE OF the earlier gene
claim, and detailed in the Supplementary (Note 6 and the Supplementary
Methods: the real-covariate decode, the ranking choices, X17's rule and
its amendment, all three cohorts). Then B's within-lineage result beside it.

**TEXT DONE 19 Nov (figures excluded, AW: "we need to finalise all figs
separately").** Results disease subsection, Discussion, Abstract, Results
opening, Note 6 (ledger row, both disease subsections, summary), Tables
S26/S27 columns (measured immune expression, Open Targets), and a new
Supplementary Methods subsection *Decoding a latent direction* with the
measured-count test. STILL STALE, FIGURE WORK: Fig 1a fifth outcome row,
the caption of Supplementary Fig. x12-rank (Zhao and "unindexed" genes),
Fig 2f caption, Fig 2 overall.

**AW's stance on the gene claim, 17 Nov:** "Throwing up your hands and saying
no decoder-based gene claim can be made is equivalent to saying this paper is
useless for the one thing disease atlases are supposed to do. I cannot allow
that. We are doing this again and correctly." Do not propose dropping it.

**Text still quoting the INVALID genes** (rewrite after step 6): the
ABSTRACT, Results E3, Discussion paragraph 3, Note 6 gene subsection prose
and tables S26/S27 (regenerated from the invalid epoch-4 file), Fig 1a fifth
outcome row ("four genes never before reported"), Fig 2f.

## Everything else, in order
1. **Main PDF will not build.** `verify_numbers.py` fails on Results' four
   Zhao numbers (72.95, 40.93, 15.33, 3.95e-7). Correct behaviour; clears
   with the gene prose.
2. **Figure 2** (draft only, `figures/draft/figure2_so_far.png`, script
   `figure2_draft.py` + `fig2_panels.py`; pinned/figure2.png is still the
   OLD figure): a, b SIGNED OFF; c (composition, black labels, no y axes)
   and d (violins of 400 held-out AUCs, median + excess over chance, P
   between plot and name) side by side; e REMOVED; f = curve of the
   component papers' 117 genes (X19) on our ranking with one rug row per
   study, Fig 1a colours; a separate tall single-column f exists
   (`figure2f_tall.py`). f is currently drawn from the invalid ranking.
   AW asked how f works; the ELI5 walk-through was given (ECDF, diagonal =
   null, KS band +-0.126 for 117 genes).
3. **Supplementary Methods WRITTEN, awaiting AW review**
   (`supplementary/methods/supplementary_methods.tex`, after the Notes):
   Severity; Pathway gene grouping in full; **Hyperparameters, every value
   and how it was set** (AW 17 Nov: ALL hyperparameter detail lives here,
   the main Methods is left as it is) with Table S28 generated by
   `figures/scripts/supp_methods.py`; Label transfer. To add when results
   exist: the real-covariate gene decoding, X17.
4. **Main Methods errors to RAISE, not edit (AW: leave Methods as is).**
   (a) groups "253 to 493" and "49.0% on padding": shipped vocabulary is
   247 to 493 and 46.7% (Table S28). (b) Optimisation says equal-size
   buckets reach the flash kernel; in the reported model NO bucket is
   uniform, every bucket is masked. (c) Data section says the split "could
   not detect" the 15 two-ID people and 17,873 held-out cells belong to
   someone also in train; the reported run used `donor_aliasing: True`
   (train log: "30 donor ids resolve to 15 people ... split once"), so
   that sentence describes older arms, not this one. (d) Adversary section
   says the weak discriminator's failure "is described in results"; it is
   not, it is in the SM.
   The main text cites neither Reactome nor GO (supplement now does).
5. **Captions** wait for figures (AW). Fig 1 caption calls the architecture
   panel a; Fig 2 caption describes the old figure; Fig 4 caption is current.
6. Note 7 (X15/X16) not written. Main text ~450 words over cap.
7. Citations, Source Data, Reporting Summary.
8. **Push:** Paper_writing ~45 commits unpushed; axw1008 pushed by AW up
   to c6d5f79. NO `Co-Authored-By` / `Claude-Session` lines in any commit
   (AW's rule; all unpushed history was rewritten, backups on
   `backup-before-trailer-rewrite` in both repos).
9. **Dropped, do not reopen:** the seed study (AW: "I think there is
   something wrong here"); its numbers may not be quoted anywhere.
10. Optional: the Endometriosis Knowledgebase gene list needs AW to
    download it by browser (the site's certificate fails here); it has no
    direction, like Open Targets, which AW kept.

# ⓕ FINAL CHECKLIST, before submission (AW, 18 November)

Run AFTER the gene ranking is redone and its prose rewritten (⓪), because
that changes Abstract, Results E3, Discussion, Note 6, Fig 1a and Fig 2.
Every pass produces findings as **current / proposed / why** for anything
in AW's text; only spelling and grammar are fixed directly. Each pass ends
with a short findings file in `audit/`, so the next session sees what was
checked and what was not.

**Limits that apply** (NMI Article, `Nature_websites/_txt/NMI_Content_Types.txt`):
main text ≤ 3,500 words excluding abstract, Methods, references and legends;
abstract ≤ 150 words, unreferenced; ≤ 6 display items; references ~50 as a
guideline; ≤ 10 Extended Data figures. **Where we are:** abstract 188 words
(over by 38), main text ~3,950 (over by ~450), 41 unique citations in the
main text, 5 display items (Figs 1-4, Table 1).

## F1. Figures review: every main, Extended Data and supplementary figure

For each figure, one row per panel, against six questions:
- [ ] **Readability** at placed size: nothing below NMI's 5 pt floor once
      scaled (titles 6.5 pt, body 5.5 pt, panel letters 10 pt bold, Arial;
      `FIGURES_NEEDED.md`); 180 mm double / 90 mm single column, depth
      ≤ 170 mm; no type over shaded areas, no white-on-colour text; axis
      labels sentence case, no full stop, units with a space, thousands
      with commas (Nature formatting guide).
- [ ] **Importance**: does the panel carry something the text needs?
      Nature: "Unnecessary figures and parts (panels) of figures should be
      avoided ... small tables or histograms ... can generally be stated
      briefly in the text." Anything that fails moves to Supplementary or
      goes.
- [ ] **Correctness**: every plotted value traces to a named CSV; the
      figure script reads that file (no hard-coded numbers, cf. the
      supp_figures novel-genes set); regenerated AFTER the gene redo
      (Fig 1a fifth row, Fig 2f, Note 6 figures); panel content matches
      what the caption and the text say it shows. Check against study and
      cell type before believing a pattern (CONTINUITY, failure mode 3).
- [ ] **Caption completeness** (REGISTER, *Figure legends*; NMI AIP):
      brief title, then each panel in sequence; centre values and error
      bars defined; n stated; statistical test named; P values given;
      keys described in words ("open red triangles"), not symbols; no
      methods detail; under 300 words (Nature guide). Captions wait on AW
      signing each figure off (0a).
- [ ] **NMI guideline violations**: image integrity (no flattened labels on
      raster images, editable text), RGB, resolution, every panel cited in
      the text in order, Extended Data referred to as discrete items,
      Source Data file for every figure with plotted data.
- [ ] **Colour scheme**: Okabe-Ito for cell families and the eleven study
      hues (yellow-olive-brown band removed) used IDENTICALLY in every
      figure, main and supplementary (Fig 1a, Fig 2f rug rows, UMAPs,
      Notes); one meaning per colour across the paper; sequential vs
      diverging scales chosen by the data; check each figure under a
      colour-blind simulation; no red/green-only contrasts.

## F2. Citations review, and additions

- [ ] Every statement about prior work, a dataset, a tool or a method
      carries a citation (main text, Methods, legends, Notes, SM).
      Introduction, Results and Methods have never had this pass (PRIORITY,
      *Citations*); the Discussion went from 1 to 18.
- [ ] **Additions known to be missing:** Reactome and GO in the main
      Methods (the SM cites both); the software the pipeline rests on
      (PyTorch, anndata/scanpy, scikit-learn, scIB, UMAP) with versions;
      every comparison method at the point it is named.
- [ ] Every citation supports the exact claim it is attached to (open the
      paper, not the abstract). Records to fix: `kedzierska2025zeroshot`
      (no pages), `duempelmann2026endometrium` (no volume, pages); the
      preprints `vasilevsky2022mondo`, `czi2023cellxgene` checked for
      journal versions; the six bib entries cited zero times removed.
- [ ] NMI format: numbered, sequential across main text, Methods and Data
      availability; article titles present; ~50 as the guideline;
      Supplementary has its own reference list.
- [ ] **Guide's file**: citations go in as ONE pointed pass of find/replace
      changes naming each location and number (AW, 14 Nov); his Results has
      none and his Discussion has author-year brackets.

## F3. Prose: a full read-through, every section, main and supplementary

- [ ] **Tone**: state the case, then the caveat, never both in one sentence;
      no pre-empting objections nobody made; no clawing at our own work; no
      hedging (CONTINUITY, *My failure modes*; REGISTER §5-6).
- [ ] **Accuracy**: every number through `audit_numbers.py` and
      `verify_numbers.py` (build.sh runs both; extend them to Methods and
      the Notes); every claim against `CLAIMS_LEDGER.md`; the four
      main-Methods errors in ⓪ item 4 raised with AW.
- [ ] **Consistency**: one term per concept, the paper's own (adversarial
      weight = λ_dab, information cost = w_kl, ELAJ_B hi / B lo, donor vs
      patient, study keys as `\texttt{}`); every number identical wherever
      it recurs (abstract, Results, captions, Notes, SM, tables); British
      spelling; tense (past for what was done, present for what a figure
      shows); every Supplementary Note / Table / Fig / Data pointer
      resolves and its number matches after any reordering.
- [ ] **Readability and sharpness**: one point per paragraph, topic
      sentence first; procedure in a clause, never a sentence (REGISTER
      §13); every number lands a conclusion (§3); cut to the limits above,
      cutting Results first (it carries the excess).

## F4. Comparison against the guide's version (his file is the paper)

Protocol (CONTINUITY, *The supervisor is in the loop now*; *Word maths does
not survive a copy*; `make_changeset.py`):
1. AW sends the latest `.docx` from the guide's OneDrive.
2. Read `word/comments.xml` and anchors in `word/document.xml`; diff his
   text against ours paragraph by paragraph (tracked changes are off).
3. Sync HIS edits into the `.tex`, so the two do not drift.
4. For OUR changes: edit the `.tex`, build the Word file, and hand AW a
   changeset from `make_changeset.py`: short maths-free `edit` fragments,
   `maths` entries he inserts with Word's equation tool, `paste` only for
   genuinely new maths-free prose, new references listed in Nature style.
   Never a whole-paragraph paste over a paragraph holding maths.

Known gaps to close in that comparison:
- [ ] Batch 2026-11-10 never confirmed applied; Figure 1 has changed since.
- [ ] X13 additions to Results and the Discussion are only in the `.tex`.
- [ ] Everything since: Abstract and Introduction (AW-edited 17 Nov), the
      gene-claim rewrite, new Figs 2 and 4 with captions, the Supplementary
      Methods.
- [ ] His open comments: `[97]`, `[42]`, `[82]`, `[503]`, `[511]` ours;
      `[132]`, `[467]`, `[507]` his to clear; the two cuts AW raises in
      person.

## F5. Added: things that also have to be true before submission

- [ ] **Both PDFs build green**: `build.sh` (number checks pass) and
      `build_supp.sh`; zero overfull, zero undefined references, figures at
      full resolution (`FIGS=1`).
- [ ] **One checkpoint, one set of numbers**: every figure, table, Note and
      Supplementary Data file regenerated from the final CSVs after the gene
      redo, then nothing re-run.
- [ ] **Source Data** for every main and Extended Data figure; Supplementary
      Data D1-D5 current (D1 depends on the gene ranking).
- [ ] **Reporting Summary**, **Data availability** (every corpus study with
      accession), **Code availability** (repository, licence, Zenodo DOI,
      run documentation in the repository, the supervisor's third batch).
- [ ] Back matter AW owns: author list and contributions, funding, competing
      interests, ethics statement for public data, cover letter, preprint.
- [ ] **Reproducibility**: each reported number regenerable by a named
      command from a committed script; HPC commands recorded in the
      experiment log.
- [ ] Push both repos when AW asks; no `Co-Authored-By` or `Claude-Session`
      trailers in any commit.

# 0d. Figure 2 DONE (19 Nov): pinned, captioned, cited in order, Source Data
`figures/pinned/figure2.{png,pdf}` from `fig2_variants.py`; caption under 300
words in `06-display-items.tex`; colour pairs checked by deutan/protan/tritan
simulation (f worst-case dE 35, e 44.8); Source Data
`Outputs/supplementary/source_data/Figure2_source_data.xlsx`. Figure citation
order across the paper is now 1 -> 2 -> 3 -> 4 with panels in order. OPEN,
for AW: family colours stromal/endothelial (dE 17.0) and epithelial/immune
(18.3) are weak under colour-blindness, paper-wide. NEXT: the same audit for
Figs 1, 3, 4 (Fig 1 pinned image still shows the retired genes row).

# 0c. Figure 2, settled so far (19 Nov)
a, b frontier; **c = the cycle closes** (AW: replaces composition; drawn by
`supp_figures.cycle_closes`, shared with the Supplementary figure); d per-
family AUCs, no study step; e = option C, thinner contours; f = option B.
Letters only, calmer control/patient pair. Script: `fig2_variants.py`
(figure2_v2.png) -- promote to `figure2_draft.py`/pinned when signed off.
TODO: the composition panel (donor spread 4.1-9.5x) needs a Supplementary
figure in Note 6, which Results now cites; d's median markers too faint;
"case" vs "patient" wording across panels.

# 0b. Results against figures: the audit, 19 November (AW asked)

Every Results finding, and what shows it. "--" = nothing in the main figures.
Fig 1, 3 and 4 were cited NOWHERE in Results before today; the four
`Fig.~X` placeholders below are the open integration items.

| subsection | finding | shown by |
|---|---|---|
| trade-off | donor recovery and cycle fall together over six arms | Fig 2a,b (cited) |
| trade-off | B-hi beats all nine competitors on both axes | Fig 1 outcomes row, Table 1 (Fig 1 not cited) |
| emergent biology | supervision is a minority of the cycle signal (phase head ablated) | Table 1 only |
| emergent biology | cycle structure differs by compartment | Fig 3 (NOT cited) |
| emergent biology | the cycle is one linear axis; orders an unseen cohort by day and progesterone | Fig 4d-f (cited 19 Nov) |
| emergent biology | withheld labels recoverable (cell family 0.9807, stage) | Table 1; Fig 4g-i qualitatively (not cited) |
| emergent biology | technical controls (mito, doublet) bound alternatives | -- (Supplementary) |
| severity | disease status legible, severity not, in all ten methods | Fig 4g-i qualitatively (NOT cited); no quantitative panel |
| severity | composition does not track severity | `Fig.~X` placeholder; Supplementary figure exists in figures_explore |
| disease axes | label transfer validated; marker signatures reproduce (X13) | -- (Note 6 figure) |
| disease axes | composition unchanged; donors differ 4.1-9.5x more than patients from controls | Fig 2c (cited 19 Nov) |
| disease axes | per-family held-out AUCs, no study step | Fig 2d (cited) |
| disease axes | stromal RNA in every non-stromal family | -- |
| disease axes | immune axis = lymphoid-to-myeloid (cosine 0.88) | Fig 2e (cited) |
| disease axes | phase sets donor position | Fig 2f (cited) |
| disease axes | X17 measured test | -- (Note 6 tables) |
| ablations | random groups best reconstruction, least disease | Table 1 |
| ablations | phase head's contribution is not phase (epoch trajectory) | -- |
| ablations | ECS and sentinel visible only in the latent | `Fig.~X` x2, placeholders; no figure exists |

# 0a. Figures in flux, 17 November — CAPTIONS ARE A TODO FOR AFTER

**AW, 17 Nov: "Figure captions are a todo for after figures are fixed."**
Do not polish any caption in `sections/06-display-items.tex` until AW
signs off the figure it describes. Known stale meanwhile: Figure 1's caption
still describes panel a as the architecture (it is now b) and does not
mention the fifth Outcomes row; Figure 2's caption describes the OLD
eight-panel knobs figure. Figure 4's caption was rewritten for its new
panels on 17 Nov and is the one current caption.

| figure | state | script |
|---|---|---|
| 1 | 1a gained a fifth outcome, "four genes never before reported" | `mock_fig1a_opt8.py`, `figure1.py` |
| 2 | **being rebuilt.** Draft at `figures/draft/figure2_so_far.png`; `pinned/figure2.png` is still the old one and the manuscript still shows it | `figure2_draft.py` + `fig2_panels.py` |
| 4 | cell family out, b-f up one, X16 cycle axis at f. Done | `figure4.py` |

**New Figure 2, as assembled:** a, b = old 2b and 2d, polished to Figure 1c's
conventions (x NOT reversed, so upper left is better, as in 1c; cell-family
row dropped); c = I1 composition; d = I2b disease signal per family, ONE plot
aligned under c's columns; e = I4b, the disease end of the gene ranking;
f = I6, **PENDING**. When AW signs it off: point `figure2_draft.py` at
`pinned/figure2.png`, retire the old `figure2.py`, then write the caption.

**UPDATE, later 17 Nov.** 2a/2b SIGNED OFF by AW. 2c labels black, 2d
violins with medians, excess over chance and P (X12 split file). 2e: AW chose
option A, measured expression; **X17 is written, needs one scp and one
sbatch** (EXPERIMENTS.md, X17). I6: AW asked for EndometDB and Open Targets
lines; **X18 found EndometDB's rule-based list empty and its unthresholded
statistic ANTI-correlated with our ranking** (EXPERIMENTS.md, X18). ⚠ **That
puts the Zhao sentence in Results and the Discussion at risk**: a reviewer
who checks the largest public cohort sees the opposite direction. Decision
with AW. Do not draw I6 until it is made.

**I6 is blocked on a question AW asked, 17 Nov: "What is special about
Zhao 2017? Why are we comparing against them?"** The answer on file:
bulk mRNA-seq, 8 eutopic endometria against 5 controls, the same contrast as
X12, published with a full per-gene table, and not in the corpus because the
corpus is single-cell. **No selection criterion was ever recorded**, and a
reviewer will read one external list as a chosen one. The prose (Results
E3 paragraph, Discussion paragraph 3) quotes a top-15 overlap only; I6 is a
cutoff-free view of the same list and also shows about nine of their genes
at our control end, which "none at the control end" (a top-15 statement)
does not contradict but invites. Options are with AW in the session of 17
Nov: state the criterion, or test against several external lists chosen by
a written rule, and only then decide whether I6 earns a panel.

# 0. Where this stands, 17 November

**Both HPC jobs landed and one still needs scoring.** The probe is complete
and its integrity row reproduces Table 1 exactly on six axes. **`a1_seed42`
trained but has NO benchmark row**; the two commands are in 1a below, AW
kicked off the first, and nothing in Notes 3 or 5 can quote a seed band
until the second finishes.

**Written this session.** Abstract and Introduction, both AW-edited.
Supplementary notes cut from eight to six. X15 and X16 recorded in all four
tracking files. `check_figure_scale.py` added to `build_supp.sh`.

**Next, in the order I would take them:**

1. **Note 7**, the X15 and X16 note. The material exists: `supp_figures.py
   --only x15,x16` writes five figures and a table, `EXPERIMENTS.md` has
   both protocols with their cautions, `x16_cycle_axis.csv` sources every
   number. **X15's group rankings are DISCARDED** (section 4), so the note
   is mostly X16.
2. **Score `a1_seed42`** when the dump lands, then the seed band into Notes
   3 and 5.
3. **Trim the main text** by about 450 words, which is Results' to give.
4. **Supplementary Methods**, still nothing, and two Results pointers dangle.
5. Citation pass, Source Data, Reporting Summary.

⚠ **THE PROPAGATION DIAGRAM IS PAUSED.** AW, 17 November: *"Pause on the
diagram for now."* The draft is in `supp_figures.py` as `x15_propagation()`
with colliding labels and a legend over the top box. The layout patch that
would have fixed it failed its own assertion and was never written, so the
function sits at its first draft. Nothing depends on it.

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

## The seed arm: SCORED 17 Nov, and it moves the cycle more than predicted

⛔ **DROPPED, AW 17 Nov: "I think there is something wrong here and I don't
think these tests would confirm anything substantially enough. We don't have
time to run a few more seed variability studies."** NOTHING below, and
nothing in `seed_band.csv`, may be quoted in the paper. Notes 3 and 5 keep
their single-run limitation as written. What was found before stopping, for
the record: configs, code and logs match; the local scorer reproduces both
benchmark rows; the phase gap is in the TEST half only (val -0.004, test
-0.054), and all 20 phase-labelled test donors score lower under seed 42.
The untested lead was the checkpoint epoch (seed 42 epoch 2, base epoch 4,
each picked by a val_nb that moves +-0.003 between epochs).

Rescored with `--no-elaj` after 61932543. Landed at
`Outputs/Benchmarks/full_a1_seed42/` (NOT under `full/`, which is fine:
`a1_seed42` is deliberately not in `table1.A_SERIES`). Every number in
`axw1008/docs/paper/seed_band.csv`, written by `figures/scripts/seed_band.py`.
Only the training seed changed; the donor split is the base's.

| axis | seed 24 | seed 42 | difference | predicted band |
|---|---:|---:|---:|---|
| cross-donor phase | 0.7346 | 0.6756 | -0.0590 | 0.70-0.77, **MISSED** |
| cross-donor family | 0.9820 | 0.9812 | -0.0008 | inside |
| donor recovery | 0.5188 | 0.4797 | -0.0391 | 0.48-0.56, **just below** |
| study separation | 0.7613 | 0.7321 | -0.0292 | not predicted |
| disease, pooled | 0.3364 | 0.3164 | -0.0200 | inside |

**The seed moves the model ALONG the trade-off, not off it**: less cycle,
less donor, less study, cell family untouched. Same direction the knobs move.

**What it does to claims, by the arm's own reading rule.**
* "Most cycle signal of anything tested" (Fig 1a, Fig 1 caption, abstract?):
  B_hi's margin over Scanorama is 0.0043, over scVI 0.029, over scANVI
  0.0375; the seed difference is 0.059. **Not seed-robust**: seed 42 sits
  below all three. Must be softened.
* "Better than all nine on both axes at once" (Fig 1a): seed 42 is not
  above scVI, scANVI or Scanorama on cycle. Still on the Pareto front (no
  baseline has donor recovery below 0.5421). Reword to the front.
* "Least donor identity" vs baselines: holds at both seeds (0.5188, 0.4797
  against the best baseline's 0.5421).
* Ablations: no-phase-head exceeds the seed on every axis but disease;
  order statistics cost the cycle 1.6x the seed difference; random grouping
  costs the cycle only 1.0x (INDISTINGUISHABLE) but cell family 27x and
  disease 3.3x; no-DNS and no-ECS are within the seed on cycle. Note 5 must
  say each of these.
* Knobs (Fig 2a/b): the information cost moves the cycle 2.2x the seed;
  lambda 7 vs 168 vs 336 differ on cycle by at most 0.34x the seed, so the
  adversary's effect is on study separation (2.0-3.5x), not on the cycle.

## (history) The seed arm: trained, verified, and still needs its benchmark row

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
cd /rds/homes/a/axw1008/axw1008 && git pull && sbatch data_collation/scripts/benchmark_cpu.sh a1_seed42 --no-elaj --methods none --external-latent /rds/homes/a/axw1008/axw1008/src/outputs/benchmarks/latents_elaj/a1_seed42/elaj__native__train --out outputs/benchmarks/full_a1_seed42
```

CPU on bbdefault, measured 50:51, outside the bbgpu cap.

⚠ **THE FIRST ATTEMPT, job 61932543 (17 Nov), TIMED OUT AT 8 h WITHOUT A
ROW**, because this command was written here without `--no-elaj`.
`_benchmark_args.sh` adds `--include-elaj` unless told not to, so the job
loaded the checkpoint and ran the transformer over the 192,402 val cells on
CPU; the log goes silent at 16:20 after the val split loads. The
`a1_clsonly` reference DID pass `--no-elaj`, which is invisible in its log
because the parser consumes the flag. Fixed above, and `benchmark_cpu.sh`
now refuses an `elaj__*` external latent without `--no-elaj` (`axw1008`,
17 Nov), so the command as first written fails in a second instead of
eight hours. ⚠ **The result has
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