# The supplementary, by priority

Written 14 November 2026 on AW's instruction to order the work, HPC first,
because his laptop is needed for edits, reviews, reading other papers and the
number-validation wiring. `SUPPLEMENTARY_STRUCTURE.md` says what a
supplementary is made of; this says what we do and in what order.

**AW's correction, recorded because I had it backwards:** *"IBDex is not the
outlier, it is the reference that matters to us in particular because I
report to my guide and his preference decides what goes to NMI."* So IBDex's
26 tables against 12 cited is the target, not a deviation from one.

---

# The HPC answer is one job, and that is good news

**Almost nothing needs the cluster, because almost everything is already on
disk.** Checked rather than assumed:

| what I expected to need HPC | what is actually local |
|---|---|
| latents for the 6 frontier and 5 ablation arms | **all eleven**, `Outputs/cells/<arm>/latent.npy`, 1,577,728 x 16 each, with `metadata.csv.gz` and `cell_family_transferred.csv.gz` beside them |
| per-epoch losses for the loss plots | **all eleven**, `Outputs/<series>/<arm>/metrics.csv` |
| scIB measurements for the detail note | **all ten representations x all ten scIB metrics**, in the manifest's own comparable files |
| the full benchmark grid | local, and the auditors already read it |

**The one real gap: UMAP coordinates exist for two arms only.**
`Outputs/analysis/umaps/<arm>/_umap_cache/global_400000.npy` is present for
`p1_dab168_kl1` and `p1_dab168_kl30` and absent for the other nine. Every
Supplementary figure showing a latent needs those coordinates, including the
two ablation UMAPs the Discussion already points at.

**It is laptop-hostile and cluster-trivial.** One arm is a UMAP fit over
400,000 points plus a k=25 neighbour search, and `random_state` is set, which
makes umap-learn single-threaded by design. Nine in series is most of a day
with the machine unusable. As an array it is one task each, in parallel.

**`data_collation/scripts/umap_cache.sh` is written, committed and syntax
checked.** Array of nine, bbdefault so it does not touch the bbgpu budget,
64 G by arithmetic rather than by copying benchmark_cpu.sh's 240, idempotent
because `embed()` returns an existing cache.

```
cd /rds/homes/a/axw1008/axw1008 && git pull && sbatch data_collation/scripts/umap_cache.sh
```

⚠ **One thing I cannot check from here:** whether `outputs/cells/<arm>/` is
present on the cluster. The dumps are local; if they were produced locally
and never synced up, the job exits 2 with "no dumped cells at ...", which is
a clean failure rather than a wasted allocation.

## The only other HPC candidates, and neither is blocking

**X15, group embeddings.** AW's own Supplementary idea from 11 November.
Needs the 44 per-group representations, which are intermediate activations,
so it needs a model forward pass and therefore a GPU. **Unscoped**: I do not
yet know what question it answers. Worth a conversation before an sbatch.

**X13, reproducible marker signatures.** Marečková's claim that prior atlases
lack reproducible marker gene signatures. Needs per-family expression across
studies, so it needs the counts rather than the latent. **Unscoped.**

Everything else in the plan below runs locally in seconds or minutes, because
the heavy objects are already dumped.

---

# Answers to the three questions AW asked

## Supplementary Data: yes, we know what it is, and no, it will not change

**It will not change, and the reason is structural**: every item is an output
of the frozen reported arm, and the standing rule is no more edits to the
architecture, parameters or optimiser. Nothing we write changes a dumped
array. The only way this moves is if we decide to ship *more*, which is
additive.

| # | what ships | source | rows |
|---|---|---|---:|
| D1 | **the full per-gene shift along the immune disease direction** | `x12_gene_shifts_orth.csv` | 15,496 |
| D2 | the full benchmark grid, every method x metric x label | the manifest's files | ~2,000 |
| D3 | per-donor cell-family composition | `x8_x9_composition.csv` plus the per-donor frame | 194 donors |
| D4 | transferred cell-family labels per cell | `cell_family_transferred.csv.gz` | 1,577,728 |
| D5 | **the 44 pathway groups and their gene lists** | the vocabulary | 15,496 assignments |

**D1 is the one that must ship.** The Discussion's novelty wording names four
genes with no prior report, and that claim is only checkable if a reader can
look up any of the other 15,492. Shipping the top fifteen alone would be
asking for trust.

**D5 is the one a reproducer needs**, and it is the thing that makes the
inductive bias auditable rather than asserted.

## Supplementary Tables are not Notes, Methods or Data, and here is the line

AW asked whether Tables are a leftovers bin and whether we are separating
tables from prose. **No to both.** The four are distinguished by what they
are *for*, and a Note carries its own tables inline, which is exactly what
scGPT does.

| | what it is | test for belonging |
|---|---|---|
| **Note** | prose that makes one argument, with its own figures and tables inline | *does this argue something?* |
| **Methods** | prose that describes a procedure, arguing nothing | *does this say how, rather than what it shows?* |
| **Table** | a numbered, captioned, typeset table that stands alone and is cited from the main text or a Note | *is this reference material a reader looks up?* |
| **Data** | a spreadsheet nobody reads top to bottom | *is it too big to typeset?* |

MIDAS's Supplementary Tables 9 and 10, patient clinical characteristics, are
the archetype of a Table: nobody argues with them, they are looked up. Its
`SuppData1A` at 83,436 rows is the archetype of Data.

**So a table only makes the Tables section if it survives being separated
from an argument.** A table that only means something inside a Note stays in
that Note.

## The figures concern is correct, and here is the arithmetic

AW: *"Compared to the amount of results we have, our figures are severely
lacking."* He is right.

**30 results in `RESULTS_INVENTORY.md`. Four main display items. Three
supplementary-capable scripts that already exist**: the old Figure 3 (both
latents by family and phase), the pinned dissociation panel, and PRISMA.
Eye2Gene ships 23 supplementary figures, TIGON 17, scGPT 13.

**What the UMAP job unblocks, the moment it lands:** nine arms x the
per-family UMAP panels that `plot_cells_umap.py` already draws, plus any
pairing we want of base against ablation. That is the bulk of the gap closed
by one array job and local drawing.

**What it does not unblock**, and these need drawing from scratch:
label-transfer distance distributions, the training curves, the coverage and
threshold curves for cross-donor agreement, and the two main-text candidates
that are still undesigned, the per-family AUCs against their nulls and the
ranked gene shifts.

---

# The order of work

## Now, in parallel

| | what | where | blocked by |
|---|---|---|---|
| **1** | **`umap_cache.sh`, nine arms** | HPC, array | nothing. One command |
| **2** | **Supplementary Data D1 to D5** | local, scripted | nothing. AW approved kicking it off |
| **3** | the scIB assembly: ten methods x ten metrics into one table plus panels | local | nothing. Data is on disk |
| **4** | loss plots for all eleven arms | local | nothing. `metrics.csv` is on disk |

⚠ **Item 3 has one trap and it is the audit's oldest lesson.** The scIB
values must come from the manifest's files by exact key, never from a glob,
because mixing gene policies across runs is what made the baseline table
invalid for three days. `audit_numbers.py`'s `MANIFEST` is the only source.

## Next, writing, once the above is running

| | Supplementary Note | source already written | gap |
|---|---|---|---|
| **N1** | gene-group sizing, the 250 to 500 bounds and the effective gene space | **`Thesis/appendices/D-gene-grouping.tex`, 2,525 words, eight sections, plus `C-sizing.tex` at 1,238** | trim and re-register the numbers |
| **N2** | scIB in detail, with figures and tables | the measurements, all ten methods | the figures, and the prose |
| **N3** | **limitations one by one, at length** | the limitations cut from the Discussion, `SETTLED.md`, the split-leak audit | writing. AW: *"Pour your heart out"* |
| **N4** | all six frontier arms, their UMAPs and loss curves | `metrics.csv` x6, latents x6 | waits on item 1 |
| **N5** | the ablations, their UMAPs, loss curves and tables | the Results ablation subsection, `ABLATIONS.md` | waits on item 1 |
| **N6** | label transfer and its failure mode | `x1_validation.csv`, written up in `CLAIMS_SUMMARY.md` | the distance distributions |
| **N7** | the claims axis, protocol by protocol | `EXPERIMENTS.md` X1 to X14, `CLAIMS_SUMMARY.md` | formatting |

**N3 is the one that changes how the paper reads.** AW's reasoning, and it is
right: *"Here it makes sense because this section is when the reader has gone
through the paper and understood the good side. Now the clawing reads as
objective analysis rather than hedging."* Everything cut from the Discussion
for being doubt-casting belongs here at full length, and the Discussion's
`Supplementary Note X` placeholder resolves to it.

**Then Supplementary Methods**, which AW ranks after the Notes and wants to
review in detail the way we reviewed Results and the Discussion. Sources:
`CROSS_DONOR_ESTIMATOR.md`, `DATA_PROVENANCE.md`,
`MEASURING_WITHOUT_TRAINING.md`, `docs/walkthrough/01` to `15`, and the four
Methods subsections cut for length which are recoverable from git.

**Then the pseudocode box**, which is `docs/walkthrough/06` to `08` reformatted.

## Pinned until their dependency lands

| what | waits on |
|---|---|
| **Source Data** | the figures being final. Sheets are named per panel, so it cannot be written before the panels exist |
| **Supplementary Tables** captions and numbering | the Notes, since a table that only means something inside a Note stays there |
| **References** | the deferred citation pass, same strategy as the main prose |
| **Reporting Summary** | pre-submission. AW's, and last |

---

# What I am not doing without a conversation

**X13 and X15.** Both are AW's own ideas, both need HPC, and neither is
scoped. The supplementary is complete without them, so they are additions
rather than blockers, and scoping them is a discussion rather than a task.
