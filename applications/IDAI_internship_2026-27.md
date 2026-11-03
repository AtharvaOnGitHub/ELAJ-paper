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

**Life Sciences.** The Life Sciences Sector Plan commits up to £600 million to a
Health Data Research Service. That buys the data. It does not buy the ability to
read it. A model whose axes correspond to named biology can be asked a clinical
question directly, and can answer that a diagnostic category has no molecular
basis. ELAJ already does this for the surgical staging of endometriosis. Doing
it across omics is how national health data becomes interpretable rather than
merely available, and that capability is the gap between the sector plan's
ambition and its data.

**Digital and Technologies.** Interpretable multi-omic representation learning
is an open problem in AI, not an application of it. The UK holds the data assets
and the compute to lead on it.

**UN Sustainable Development Goals.** SDG 3 directly, and SDG 10, since the
diseases that require surgery to study are the least understood.

---

## 15. Expected Value & Path Forward (200 max)

**To the research.** This starts a programme rather than extending a paper. It
produces a representation shared across measurement types, a standard for
judging whether a biological foundation model carries biology at all, and a
method for testing clinical categories against molecular state. Each stands
alone, each publishes, and together they define a direction the group can own
early.

**To the intern.** The route from a finished MSc project into a funded PhD, on
work already proven at 1.58 million cells, with first-authored results in both
biology and methodology and experience at scale on national compute.

**Path forward.**

1. *Grants.* Objective 1 goes to MRC or Wellcome, since it requires several data
   types from the same people. Objective 2 goes to UKRI or EPSRC as foundational
   work on representation. Objective 3 goes to NIHR, because it asks whether the
   categories clinicians decide with hold up. Three applications, one PhD
   funded.
2. *Collaborations.* The first requirement is a cohort carrying several
   measurement types on the same people, which the supervisor's networks reach.
   Biobank and atlas consortia follow, and they need interpretable models as
   much as we do.
3. *Compute.* Baskerville, applied for on award.

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
