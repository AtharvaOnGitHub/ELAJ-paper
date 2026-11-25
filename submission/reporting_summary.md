# Nature Portfolio Reporting Summary: draft answers for ELAJ

The form is `Nature_websites/forms/nr-reporting-summary-flat.pdf` (7 pages;
text extracted alongside it). The form says: **never write "n/a" or "not
applicable" in a text field**; use the help text's wording instead. Every
⚠ below is for AW to decide or supply.

## Decisions for AW (everything else below is filled from the paper and code)

| | what | proposed |
|---|---|---|
| D1 | Cell QC is applied but Methods does not say so | add to *Data collection*, after "No correction was applied to the expression values themselves.": "Before pooling, each study was filtered: genes detected in fewer than three cells were removed, as were cells with fewer than 200 counts, fewer than 100 detected genes or more than 25% of counts from mitochondrial genes. Doublets were not removed." |
| D2 | Package versions in the BlueBEAR environments | run the one-line command in the reply on a login node and paste the output |
| D3 | Held-out AUC P is one-sided, not stated | Results, "separated held-out donors at an AUC of ...": add "(one-sided permutation test)" at the first P |
| D4 | No multiple-comparison correction, not stated | add to Methods, end of *Cross-donor agreement*: "No correction for multiple comparisons was applied: each test addresses a separately stated question, and every P value is reported, including those that did not reach significance." |
| D5 | Confidence intervals | tick the item and describe the permutation-null percentiles in its place (as below) |
| D6 | Code availability placeholder | GitHub URL now; licence MIT; Zenodo DOI minted at acceptance |
| D7 | No ethics statement in the manuscript | new Methods subsection *Ethics*: "This study analysed only publicly available, de-identified data. Ethical approval and informed consent were obtained by each source study, as reported in its publication, and no further approval was required." Confirm against the University of Birmingham's rule for secondary analysis of public data |
| D8 | *Use of large language models* names Claude Opus 5, Sonnet 4.8 and Sonnet 4.5 | add Claude Opus 5.5, used from November for the manuscript and code (your text; current/proposed only) |

---

## Statistics (tick "Confirmed" or the n/a box per row)

| item | answer | where in the paper |
|---|---|---|
| Exact n per group | Confirmed | Results and legends give cells and donors for every comparison (e.g. 207 donor records for disease, 57 patients for severity) |
| Distinct samples or repeated measurement | Confirmed | Methods, *Data collection*: one biopsy per donor, donor-level split; cells from a donor are never treated as independent |
| Test(s) and one- or two-sided | Confirmed ⚠ | Cross-donor agreement: one-sided permutation test (Methods). Held-out disease AUC: one-sided permutation test, the share of label-shuffled AUCs at or above the observed (`disease_direction.py`); ⚠ the paper does not say so yet (D3). Note 3: one-sided Mann-Whitney. Kruskal-Wallis is not reported anywhere in the paper |
| All covariates tested | Confirmed | study as covariate or permutation stratum (Methods; Supplementary Table 12 caption); stromal score and phase removal (Results, *Per-donor disease axes*) |
| Assumptions and corrections, incl. multiple comparisons | Confirmed ⚠ | Tests are permutation-based, so no normality assumption. No correction for multiple comparisons; ⚠ Methods needs the sentence in D4 |
| Central tendency and variation | Confirmed ⚠ | Point estimates against permutation-null ranges throughout. Variation across training runs is one repeat seed (Supplementary Note 5) |
| Test statistic, CI, effect size, df, exact P | Confirmed ⚠ | Exact P values, effect sizes and the statistic are given. In place of confidence intervals, each cross-donor value is reported with its permutation null's 95th percentile, and held-out AUCs by family with their 5th-95th percentile over splits (D5) |
| Bayesian priors / MCMC | n/a box | no Bayesian analysis (the VAE prior is a model component, not inference) |
| Hierarchical designs | Confirmed | donor-level split, within-study permutations, donor-mean tests (Methods, *Cross-donor agreement*) |
| Effect sizes and how calculated | Confirmed | cross-donor excess over chance, AUC, Spearman ρ, fold differences in composition |

## Software and code

**Data collection.** Custom Python scripts queried the Omics Discovery
Index, NCBI GEO, BioStudies and ArrayExpress, CZ CELLxGENE Discover and the
Human Cell Atlas Data Portal APIs; CNGBdb was searched by hand. Code is in
the ELAJ repository (`data_collation/`).

**Data analysis.** Training and evaluation on BlueBEAR used Python 3.12
with PyTorch 2.7.1 (CUDA 12.6), scanpy 1.9.8, anndata 0.10.9, h5py 3.12.1,
SciPy-bundle 2024.05 (NumPy 1.26.4, SciPy, pandas) and R 4.5.0
(`src/setup_bluebear.sh`). ⚠ From the environments (D2): scikit-learn,
scvi-tools (scVI, scANVI), scib-metrics, harmonypy, Scanorama, umap-learn.
scGPT, Geneformer, scFoundation and SCimilarity were used through their
published checkpoints. ELAJ: https://github.com/AtharvaOnGitHub/ELAJ
(⚠ licence and archive DOI, D6).

## Data

Every dataset is public. Accessions are in the manuscript's Data
availability: GEO GSE266265, GSE247695, GSE214411, GSE218044, GSE213216,
GSE203191, GSE179640 and GSE276193; ArrayExpress E-MTAB-14039; CZ CELLxGENE
(García-Alonso 2021); CNGBdb CNP0006183. No restrictions apply beyond each
deposit's own terms. Source data are provided with the paper.

## Research involving human participants, their data, or biological material

**Reporting on sex and gender.** All data come from the source studies'
public deposits. The tissue is endometrial or endometriosis-related, and the
source studies report donors of female sex. Gender was not reported. Sex was
not a variable in the analysis because it does not vary across the corpus.

**Race, ethnicity or other socially relevant groupings.** Not reported
consistently by the source studies and not used in the analysis.

**Population characteristics.** 254 donors, deposited as 269 donor
identifiers (one study pair deposits the same fifteen people twice). By
donor record: 108 control, 99 eutopic endometrium from patients, 58 ectopic
lesion, 4 adenomyosis. Six anatomical sites. Age and ancestry are not
available consistently across studies.

**Recruitment.** We recruited no one. Donors were recruited by the eleven
source studies under their own protocols. Patients and many controls were
people undergoing surgery, which is how endometriosis is diagnosed, so the
corpus over-represents surgically managed disease.

**Ethics oversight.** ⚠ Draft: "This study analysed only publicly
available, de-identified data. Each source study obtained ethical approval
and informed consent as reported in its publication; no additional approval
was required." Confirm this with the University of Birmingham's policy on
secondary analysis.
⚠ **The manuscript has no ethics statement at present.** The form says
"full information on the approval of the study protocol must also be
provided in the manuscript", so one sentence needs to go into Methods.

## Field-specific reporting

**Life sciences.**

## Life sciences study design

**Sample size.** No sample-size calculation was made. The corpus is every
eligible public single-cell dataset of endometriosis found by a systematic
search (Extended Data Fig. 1): 1,577,728 cells from 254 donors in eleven
studies.

**Data exclusions.** Of 553 records identified, 11 studies met the three
pre-stated inclusion criteria (single-cell RNA data, biopsied human tissue,
relevance to endometriosis; Methods, *Data collection*). Deposits of
placental tissue and of organoids were excluded. Fifteen people deposited
under two identifiers were merged before splitting. Within each study, genes
detected in fewer than three cells were removed, as were cells with fewer
than 200 counts, fewer than 100 detected genes or more than 25% of counts
from mitochondrial genes; doublets were not removed. ⚠ Methods does not say
this yet (D1).

**Replication.** Each reported configuration is a single training run at
seed 24. One configuration was retrained at a second seed (Supplementary
Note 5). The six frontier models and five ablations reproduce the trade-off
across configurations. Published claims were retested across all studies
that carry the relevant labels.

**Randomization.** There was no experimental allocation. Donors were
assigned to training, validation and test partitions (70/15/15) at random,
with every cell from a donor in a single partition.

**Blinding.** There was no group allocation to blind. The analogue here is
that the model was never given disease status, severity, cell family or cell
type; only menstrual phase was supervised. Every biological readout is
therefore measured on labels the model did not see.

## Reporting for specific materials, systems and methods

Tick **n/a** for all: antibodies, eukaryotic cell lines, palaeontology and
archaeology, animals and other organisms, clinical data (this is not a
clinical trial), dual use research of concern, plants, ChIP-seq, flow
cytometry and MRI-based neuroimaging.
