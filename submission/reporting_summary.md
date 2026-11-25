# Nature Portfolio Reporting Summary: answers for ELAJ

Answers for each field of the form (`Nature_websites/forms/nr-reporting-summary-flat.pdf`).
The form forbids "n/a" in text fields, so each text answer uses the help
text's wording.

## Statistics (tick "Confirmed" or the n/a box per row)

| item | answer | detail |
|---|---|---|
| Exact n per group | Confirmed | Results and legends give cells and donors for every comparison (e.g. 207 donor records for disease, 57 patients for severity) |
| Distinct samples or repeated measurement | Confirmed | One biopsy per donor, donor-level split; cells from a donor are never treated as independent (Methods, *Data collection*) |
| Test(s) and one- or two-sided | Confirmed | Cross-donor agreement and held-out disease AUC: one-sided permutation tests. Supplementary Note 3: one-sided Mann-Whitney |
| All covariates tested | Confirmed | Study as covariate or permutation stratum (Methods; Supplementary Table 12); stromal score and phase removal (Results, *Per-donor disease axes*) |
| Assumptions and corrections, incl. multiple comparisons | Confirmed | Tests are permutation-based, so no normality is assumed. No correction for multiple comparisons was applied: each test addresses a separately stated question and every P value is reported |
| Central tendency and variation | Confirmed | Point estimates against permutation-null ranges throughout; variation across training runs from a repeat seed (Supplementary Note 5) |
| Test statistic, CI, effect size, df, exact P | Confirmed | Exact P values, effect sizes and statistics are given. In place of confidence intervals, each cross-donor value is reported with its permutation null's 95th percentile, and held-out AUCs by cell family with their 5th to 95th percentile over splits |
| Bayesian priors / MCMC | n/a | No Bayesian analysis (the VAE prior is a model component, not inference) |
| Hierarchical designs | Confirmed | Donor-level split, within-study permutations, donor-mean tests (Methods, *Cross-donor agreement*) |
| Effect sizes and how calculated | Confirmed | Cross-donor excess over chance, AUC, Spearman ρ, fold differences in composition |

## Software and code

**Data collection.** Custom Python scripts queried the Omics Discovery
Index, NCBI GEO, BioStudies and ArrayExpress, CZ CELLxGENE Discover and the
Human Cell Atlas Data Portal APIs; CNGBdb was searched by hand. Code is in
the ELAJ repository (`data_collation/`).

**Data analysis.** ELAJ training and evaluation: Python 3.12, PyTorch
2.7.1 (CUDA 12.6), NumPy 1.26.4, SciPy 1.13.1, pandas 2.2.2, scanpy 1.9.8,
anndata 0.10.9, h5py 3.12.1, scikit-learn 1.9.0 and R 4.5.0. Comparison
methods and integration metrics: scvi-tools 1.2.1 (scVI, scANVI),
harmonypy 0.2.0, Scanorama 1.7.4, scib-metrics 0.5.10, scib 1.1.7 and
umap-learn 0.5.12. Foundation models were run from their published
checkpoints with PyTorch 2.6.0 (CUDA 12.4): scGPT 0.2.5, Geneformer 0.1.0
with transformers 4.57.6, SCimilarity 0.4.1, and scFoundation from its
published repository. ELAJ is available at
https://github.com/AtharvaOnGitHub/ELAJ under the MIT licence; an archived
release will be deposited on Zenodo with a DOI on acceptance.

## Data

Every dataset is public. Accessions are listed in the manuscript's Data
availability statement: GEO GSE266265, GSE247695, GSE214411, GSE218044,
GSE213216, GSE203191 and GSE179640; ArrayExpress E-MTAB-14039; CZ
CELLxGENE Discover collections 9ddea8d9 and 968885c5; CNGBdb CNP0006183.
No restrictions apply beyond each deposit's own terms. Source data are
provided with the paper.

## Research involving human participants, their data, or biological material

**Reporting on sex and gender.** All data come from the source studies'
public deposits. The tissue is endometrial or endometriosis-related, and the
source studies report donors of female sex. Gender was not reported. Sex was
not a variable in the analysis because it does not vary across the corpus.

**Reporting on race, ethnicity, or other socially relevant groupings.** Not
reported consistently by the source studies and not used in the analysis.

**Population characteristics.** 254 donors, deposited as 269 donor
identifiers (one study pair deposits the same fifteen people twice). By
donor record: 108 control, 99 eutopic endometrium from patients, 58 ectopic
lesion, 4 adenomyosis, across six anatomical sites. Age and ancestry are not
available consistently across studies.

**Recruitment.** No participants were recruited for this study. Donors were
recruited by the eleven source studies under their own protocols. Patients
and many controls were undergoing surgery, which is how endometriosis is
diagnosed, so the corpus over-represents surgically managed disease.

**Ethics oversight.** This study is a secondary analysis of publicly
available, de-identified single-cell data, and no new samples were
collected. Each source study reports ethical approval and informed consent
from its donors in its publication. No further ethical approval was
required for this analysis.

## Field-specific reporting

**Life sciences.**

## Life sciences study design

**Sample size.** No sample-size calculation was performed. The corpus is
every eligible public single-cell dataset of endometriosis found by a
systematic search (Extended Data Fig. 1): 1,577,728 cells from 254 donors in
eleven studies.

**Data exclusions.** Of 553 records identified, 11 studies met the three
pre-stated inclusion criteria (single-cell RNA data, biopsied human tissue,
relevance to endometriosis; Methods, *Data collection*). Deposits of
placental tissue and of organoids were excluded. Fifteen people deposited
under two identifiers were merged before splitting. Within each study, genes
detected in fewer than three cells were removed, as were cells with fewer
than 200 counts, fewer than 100 detected genes or more than 25% of counts
from mitochondrial genes. Doublets were not removed.

**Replication.** Each reported configuration is a single training run at
seed 24; one configuration was retrained at a second seed (Supplementary
Note 5). The six frontier models and five ablations reproduce the trade-off
across configurations. Published claims were retested across all studies
that carry the relevant labels.

**Randomization.** There was no experimental allocation. Donors were
assigned to training, validation and test partitions (70/15/15) at random,
with every cell from a donor in a single partition.

**Blinding.** There was no group allocation to blind. The model was never
given disease status, severity, cell family or cell type; only menstrual
phase was supervised, so every biological readout is measured on labels the
model did not see.

## Reporting for specific materials, systems and methods

Tick **n/a** for all: antibodies, eukaryotic cell lines, palaeontology and
archaeology, animals and other organisms, clinical data, dual use research
of concern, plants, ChIP-seq, flow cytometry and MRI-based neuroimaging.
