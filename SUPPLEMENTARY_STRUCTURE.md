# The supplementary: what it is made of

Written 14 November 2026, after reading the supplementary files of eight
papers. AW: *"I did not know we had to write what is essentially another full
paper."* It is less than that, and this file says how much less.

**The sources are real, not inferred.** Page-by-page structure read from
TIGON's 38-page and MIDAS's 31-page supplementary PDFs, their contents pages
quoted verbatim, plus scGPT, Eye2Gene, DLVPM, PlantRNA-FM, the cancer imaging
foundation model and IBDex. Archives and inventory at
`Atharva Papers/NMI_supplementary/`.

**This is the structure of the supplementary itself.** Which of our results
goes where is a separate exercise and is not in this file.

---

# 1. It is four files, not one document

This is the part that was not obvious and it changes the size of the job.

| file | what it is | who does it |
|---|---|---|
| **Supplementary Information** | one PDF: notes, methods, tables, figures, references | us, and it is the writing job |
| **Supplementary Data** | spreadsheets of large machine-readable output | us, mostly packaging |
| **Source Data** | spreadsheets, one sheet per plotted figure panel | us, a script |
| **Reporting Summary** | a 2 to 5 page Nature checkbox form | AW |

Every NMI paper in the set ships a Reporting Summary. Two of eight ship
Source Data. One of eight ships Supplementary Data at scale, and it is MIDAS,
the closest analogue to our paper.

---

# 2. Inside the Supplementary Information PDF

Seven sections appear across the set. **Nobody uses all seven**, and the
order of the middle three varies.

| | section | role |
|---|---|---|
| 1 | **Cover page** | journal, DOI, "Article", title, "In the format provided by the authors and unedited". Nature generates it |
| 2 | **Contents** | a list of every item with its page. MIDAS uses a formal table of contents with dot leaders; TIGON opens with "This file includes the following subsections" |
| 3 | **Supplementary Methods** | method detail too long for the main Methods. MIDAS has four subsections here |
| 4 | **Supplementary Notes** | prose analyses. Each is a short self-contained argument with its own figures and tables |
| 5 | **Pseudocode or algorithm box** | the training or inference loop as numbered steps. TIGON gives this its own numbered section |
| 6 | **Supplementary Tables** | formatted tables, each with a caption |
| 7 | **Supplementary Figures** | one per page typically, figure plus a full legend |
| 8 | **References** | the supplementary's own reference list, numbered separately from the main paper |

**Two real orderings, both valid:**

**TIGON:** cover, contents, 17 Figures, pseudocode, 9 Notes, 3 Tables,
references.
**MIDAS:** cover, contents, 1 Note, Supplementary Methods, 11 Tables,
11 Figures, references.

---

# 3. What a Supplementary Note is, because this is the load-bearing idea

Not an appendix of raw output. **A short prose section that makes one
argument**, with its own figures and tables, on something the main text
could not fit. scGPT's twelve, by kind:

| kind | scGPT's examples | count |
|---|---|---:|
| **design-choice justification** | speed and memory in fine-tuning; influence of pretraining data size; context-specific pretraining; choice of number of bins | **4** |
| capability write-up | reference mapping; benchmarking on downstream tasks | 2 |
| an analysis that did not fit | attention-based gene interactions; perturbation prediction with external validation | 2 |
| **critique of the field's own metric** | revisiting evaluation metrics for perturbation response | **1** |
| **the long version of the limitations** | discussion about future prospects and limitations | **1** |
| related work at length | comparison to existing approaches | 1 |
| **definitions** | evaluation metric calculations | **1** |

**The main text carries a pointer and the supplementary carries the
argument.** scGPT's Discussion concedes its pretraining does not mitigate
batch effects in two sentences and points at Note 10, where the honest
version lives. That is the sentence we now cite them for.

---

# 4. How much we have, by section

**Low-hanging** means the content exists and the work is formatting or
writing from something already written. **Significant** means it does not
exist yet.

| section | role | typically contains | low-hanging for us | needs significant work |
|---|---|---|---|---|
| **Cover page** | identifies the file | title block, "unedited" line | **all of it.** Nature generates it | nothing |
| **Contents** | navigation | every item, numbered, with pages | **all of it.** LaTeX generates it once the items exist | nothing |
| **Supplementary Methods** | method detail too long for Methods | derivations, estimator definitions, preprocessing, architecture detail | **most of it.** `CROSS_DONOR_ESTIMATOR.md`, `DATA_PROVENANCE.md`, `MEASURING_WITHOUT_TRAINING.md` and `docs/walkthrough/01-15` already exist as prose. Four Methods subsections were cut for length and are recoverable from git | trimming 16 walkthrough files to publishable length. Editing, not research |
| **Supplementary Notes** | one argument each, in prose | design justifications, metric critiques, the long limitations, capability write-ups | **the content of six or seven.** The claims axis is written up in `CLAIMS_SUMMARY.md` and `EXPERIMENTS.md`; the ablation mechanisms are in `ABLATIONS.md` and the Results section; the label-transfer validation and its failure mode are measured and written; the database false negatives are documented | **two notes are unscoped experiments**, X13 reproducible marker signatures and X15 group embeddings. Both need HPC work before a word can be written |
| **Pseudocode** | the loop as numbered steps | training or inference algorithm | **all of it.** `docs/walkthrough/06-08` describe the forward pass, losses and training loop step by step | formatting into an algorithm box |
| **Supplementary Tables** | enumerate what prose summarises | full benchmark grids, hyperparameters, cohort characteristics, ranked outputs | **almost all of it.** Nine claims-axis CSVs in `axw1008/docs/paper/`, the full benchmark files behind Table 1, the 44 pathway groups, the eleven-study provenance table, the gene provenance table. Both auditors already pin every number to a named file | the cohort characteristics table needs assembling from metadata, and captions need writing |
| **Supplementary Figures** | show what prose cannot | benchmark panels, UMAPs, training curves, distributions, ablation comparisons | **three exist as scripts**: the old Figure 3 (both latents by family and phase), the pinned dissociation panel, PRISMA | **this is the expensive section.** The two ablation UMAPs, label-transfer distance distributions, training curves, the coverage and threshold curves, and per-study panels are all undrawn. Eye2Gene ships 23 figures, TIGON 17, scGPT 13 |
| **References** | supplementary's own list | numbered separately from the main paper | the `.bib` already holds every entry | tied to the deferred citation pass |

## And the three non-PDF files

| file | low-hanging | needs significant work |
|---|---|---|
| **Supplementary Data** | **almost all of it.** `x12_gene_shifts_orth.csv` is 15,496 rows and must ship; the per-donor composition for 194 donors, the full benchmark grid and the transferred labels all exist as CSVs | deciding what is too large to ship, and one packaging script |
| **Source Data** | the numbers all exist and are already pinned by the auditors | one script, and **it cannot be written until the figures are final**, because the sheets are named per panel |
| **Reporting Summary** | AW's, a form | nothing for me |

---

# 5. The honest summary of the size of the job

**Five of the eight sections are mostly done and need editing rather than
research.** Methods, Notes, Pseudocode, Tables and Data all have their
content on disk already, in `axw1008/docs/`, the nine claims CSVs, the
benchmark files and the walkthrough.

**One section is genuinely expensive and it is the figures.** Three of
perhaps twelve exist. That is the work.

**Two Notes are blocked on experiments that have never been scoped**, X13 and
X15. Neither blocks anything else, and the supplementary is complete without
them.

**One file cannot start until the figures are finished**, which is Source
Data.

So the order that falls out of this is: tables and data first because they
are nearly free, then the notes and methods as writing, then the figures,
then source data last.

---

# 6. The one discipline worth adopting now

In the NMI papers almost everything shipped is cited from the main text.
Eye2Gene points at 22 of its 23 figures, TIGON at 15 of 17 and 7 of 9 notes,
MIDAS at 10 of 11 and 9 of 11. **IBDex is the outlier**, citing 12 of its 26
tables.

So a supplementary built to the NMI pattern is large **because the main text
points at all of it**. Every item should have a sentence in the main text
that needs it. The supervisor's instinct and the journal's norm differ here,
and it is better to know that before the proposal than after.
