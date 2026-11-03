# IDAI Student Internships 2026/27 — answers for Q12–Q15

---

## 12. Project Title

**AI for Human Biology: Multi-omic foundation model for interpreting biology**

---

## 13. Project Summary & Immediate Objectives (250 max)

The intern has already built an AI-based scRNA disease atlas capable of
interpreting a complex disease like endometriosis. The model, ELAJ, outperforms
benchmarks including four pretrained foundation models with up to 192 times the
embedding width.

This internship would allow the intern to extend it further from one disease to
human biology. Foundation models in biology lag far behind AI research. The
intern's background in AI along with his experience in biology will allow him
to open new avenues in multi-omics foundation model research.

**Objective 1. A multi-omic foundation model with an interpretable coordinate
system.** Train across transcriptomic, proteomic, epigenomic and imaging data,
and across tissues and diseases, so that any measurement of a person lands on
shared axes that correspond to biology. Interpretability is a design
constraint, not something recovered afterwards.

**Objective 2. Make interpretability measurable.** Biological foundation models
are evaluated almost entirely on cell-type label transfer. No accepted test
exists of whether a model's axes carry biology, so the field cannot tell a
large model from a useful one. Build that test and the benchmark around it.

**Objective 3. Re-draw disease classification.** Much of clinical taxonomy is
anatomical or histological rather than molecular. ELAJ already shows that the
surgical staging of endometriosis has no support in transcriptional state.
Extend that to other diseases, and use the model to predict tissue state at
points on a physiological axis that no cohort has sampled.

Delivered on Baskerville.

---

## 14. Alignment with the UK Government Industrial Strategy (IS8) (150 max)

**Life Sciences.** The Life Sciences Sector Plan commits up to £600 million to
a Health Data Research Service so population-scale health data can be used for
research. Data of that size is only useful if something can read it. A model
whose axes correspond to named biology lets a clinical question be put to
pooled data directly, including questions with negative answers, such as
whether a diagnostic category has molecular support. That is a different
capability from prediction, and it is the one the sector plan's data assets
will need.

**Digital and Technologies.** Interpretable representation learning across data
types is a core AI problem, and the work is built on UK national compute.

**UN Sustainable Development Goals.** SDG 3 directly, and SDG 10, since
conditions that need invasive sampling to study stay data-poor and are the
hardest to interpret.

---

## 15. Expected Value & Path Forward (200 max)

**To the research.** This opens a line of work with three separable parts: a
representation shared across measurement types, a result on which biology a
compact latent can carry, and a method for testing whether clinical categories
have molecular support. Each can be published alone and each suits a different
funder.

**To the intern.** A move from a finished MSc project into doctoral research on
a problem already demonstrated at 1.58 million cells, with results in both
biology and methodology, and experience running at scale on national compute.

**Path forward.**

1. *Grants.* Objective 1 suits MRC or Wellcome, since it needs several data
   types from the same people. Objective 2 suits UKRI or EPSRC as foundational
   work on representation. Objective 3 suits NIHR, because it asks whether the
   categories used in clinical decisions hold up. Together they fund the
   intern's PhD.
2. *Collaborations.* Cohorts with several measurement types on the same people
   are the first requirement, and we will use the supervisor's networks to find
   a partner holding one. Biobank and atlas consortia follow.
3. *Compute.* We will apply for Baskerville access.

---

## For the supervisor

1. **Name an external partner in Q15 if you can.** Non-academic engagement is a
   priority criterion in the call. Q15 currently says we will find one through
   your networks.
2. **Baskerville access** to be applied for. Q13 and Q15 both say so.
3. **Training material was removed on request.** It is a priority criterion, so
   this gives up a scoring point.
4. **SDG 5 is not cited.** It would be an easy extra hook, but the project's
   position is that this is a human health problem rather than a gendered one.
   Reinstate only if you want that changed.
5. **"192 times the embedding width"** is the accurate form of the comparison.
   The four pretrained models run at 128, 256, 512 and 3,072 dimensions against
   ELAJ's 16. By parameter count the multiple is 53, so width is both the
   larger number and the correct one.
