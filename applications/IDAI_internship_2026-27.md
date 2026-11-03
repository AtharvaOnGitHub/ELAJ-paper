# IDAI Student Internships 2026/27 — answers for Q12–Q15

---

## 12. Project Title

**AI for Human Biology: Separating the Person from the Place of Measurement**

*Alternatives:*
- AI for Human Biology: Person-Level Coordinates for Pooled Multi-Omic Data
- AI for Human Biology: Recovering Biology that Looks Like a Batch Effect

---

## 13. Project Summary & Immediate Objectives (250 max)

Pooling human data from many sources means removing the effect of the source.
Each site recruits its own people, so the biology is rarely spread evenly across
sites, and the correction takes some of that biology out with the artefact. This
is documented and holds whatever the measurement technology. The hardest version
is a trait fixed for a person, such as cycle phase, age or disease stage, where
that person appears in one cohort only. The trait and the cohort then have the
same shape and no standard method separates them.

The intern has shown this can be solved in a hard case. Pooling 1,577,728
single-cell profiles from 11 studies and 269 donors, the model recovered the
menstrual cycle as a closed trajectory from donors sampled on a single day, and
the cycle survived the removal of donor and study identity. The cycle was the
right test because it has a known period and an independent physiological
readout, so the answer can be checked. This internship takes that past one
technology and one disease.

**Objective 1.** Learn a person-level coordinate from data other than
transcriptomes. Proteomic, epigenomic and imaging cohorts carry the same
problem, and the coordinate should be recoverable from each and more reliably
from several together.

**Objective 2.** Establish when this is possible, given how many people a site
contributes and how the trait is spread across sites.

**Objective 3.** Ask whether published multi-site findings change when site
correction is done this way instead.

Delivered on Baskerville.

---

## 14. Alignment with the UK Government Industrial Strategy (IS8) (150 max)

**Life Sciences.** The Life Sciences Sector Plan commits up to £600 million to a
Health Data Research Service so population-scale health data can be used for
research. Pooling is the step that makes those assets usable and it is also the
step at which real biology is lost. This project works on that step. The
clinical return is that a result holding in one cohort and failing in another
may be failing for a reason that can be corrected.

**Digital and Technologies.** Telling a person's biology apart from the place
they were measured is a general problem in pooled human data, and the work is
built on UK national compute.

**UN Sustainable Development Goals.** SDG 3 directly. SDG 10 as well, since
conditions that need invasive sampling to study stay data-poor and are the
hardest to pool.

---

## 15. Expected Value & Path Forward (200 max)

**To the research.** This opens a line of work with three separable parts: a
method that transfers across measurement technologies, a result on when
person-level biology can be recovered at all, and a test of whether existing
multi-site conclusions are affected. Each can be published on its own and each
supports a different funder.

**To the intern.** A move from a finished MSc project into doctoral research on
a problem already demonstrated at 1.58 million cells, with results in both
biology and methodology, and experience running at scale on national compute.

**Path forward.**

1. *Grants.* Objective 2 suits a UKRI or EPSRC application on identifiability
   under confounding. Objective 1 suits MRC or Wellcome, since it needs several
   data types from the same people. Objective 3 suits NIHR, because it is about
   whether clinical findings hold between sites. Together they fund the intern's
   PhD.
2. *Collaborations.* Multi-omic cohorts with several measurements per person are
   the first requirement, and we will use the supervisor's networks to find a
   partner holding one. Atlas and biobank consortia follow.
3. *Compute.* We will apply for Baskerville access.

---

## Checklist for the supervisor

1. **Name an external partner in Q15 if you can.** Non-academic engagement is a
   priority criterion. Q15 currently says we will find one through your
   networks.
2. **Baskerville access** to be applied for. Q13 and Q15 both say so.
3. **Training material removed on request.** It is a priority criterion in the
   call, so this gives up a scoring point.
4. **SDG 5 is deliberately not cited.** It would be an easy extra hook, but the
   project's position is that this is a human health problem rather than a
   gendered one, and every document in the body of work is written that way.
   Reinstate only if you want that position changed.

## Claims checked before use

| claim | status |
|---|---|
| batch correction removes real biology when the trait is uneven across batches | Nygaard, Rødland & Hovig, *Biostatistics* **17**(1), 29-39, doi:10.1093/biostatistics/kxv027. Verified on PMC. Add as a citation if the form allows one |
| 1,577,728 cells; 11 studies; 269 donors | the project's own corpus metadata |
| the cycle recovered as a closed trajectory, cycle survives donor and study removal | the project's own whole-corpus embedding and benchmark |
| £600m Health Data Research Service | UK Life Sciences Sector Plan, July 2025 |
| IS8 sector list | UK Modern Industrial Strategy, June 2025 |

**Dropped as false.** An earlier draft opened by claiming human tissue is
observed almost entirely cross-sectionally. That is wrong. Repeat sampling is
routine in blood, vaccination time-courses and pregnancy cohorts. The claim now
made is the defensible one and it is also more general: the problem is uneven
distribution of biology across sources, which holds whatever the technology.
