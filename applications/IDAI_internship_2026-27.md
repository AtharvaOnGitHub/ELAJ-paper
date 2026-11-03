# IDAI Student Internships 2026/27 — answers for Q12–Q15

---

## 12. Project Title

**AI for Human Biology: Multi-omic foundation model for interpreting biology**

---

## 13. Project Summary & Immediate Objectives (250 max)

Sixteen numbers per cell. That is the size of the space ELAJ builds from
1,577,728 single-cell profiles pooled across 11 studies and 269 donors, and the
menstrual cycle sits inside it as a closed loop, recovered from donors who were
each sampled on one day. Of ten methods tested, including four pretrained
foundation models with 8 to 192 times the width, ELAJ holds the cycle best.

The compression is not the point. The point is that the space can be read.
Its axes correspond to biology that can be named and checked against
independent physiology, and the model answers questions it was never trained
on. Asked whether the surgical staging of endometriosis corresponds to
anything in transcriptional state, it says no, at a donor count where that
answer is bounded and reportable. A negative result of that kind is useful to
a clinician. Larger biological foundation models do not support the question.

This internship turns that into a multi-omic foundation model for interpreting
biology.

**Objective 1.** One coordinate system across modalities. Proteomic,
epigenomic and imaging measurements from the same people, learned together
rather than embedded separately.

**Objective 2.** A map of what a compact latent can hold. Which biological
axes are representable, which are not, and what that depends on.

**Objective 3.** An audit of clinical taxonomy. Stage, grade and subtype are
categories medicine uses to make decisions. Test which of them correspond to
molecular state and which do not.

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
| sixteen dimensions; 1,577,728 cells; 11 studies; 269 donors | the project's own corpus metadata and model configuration |
| ten methods tested, four of them pretrained foundation models at 8 to 192 times the width | `audit/NUMBERS.md`. Widths 128, 256, 512 and 3,072 against 16 |
| ELAJ holds the cycle best of the ten | stated as an ordering, not a figure, on purpose. The ordering holds in both scoring runs; the exact numbers are being re-scored under one protocol and are not quoted here |
| surgical staging does not correspond to transcriptional state | held-out cross-donor agreement 0.1313 at p 0.3035 over sixteen donors, with the permutation null reaching 0.42. The bounded reading is "not recoverable at this donor count" |
| 1,577,728 cells; 11 studies; 269 donors | the project's own corpus metadata |
| the cycle recovered as a closed trajectory from donors sampled once | the project's own whole-corpus embedding |
| £600m Health Data Research Service | UK Life Sciences Sector Plan, July 2025 |
| IS8 sector list | UK Modern Industrial Strategy, June 2025 |

**Two earlier framings dropped.**

An earlier draft opened by claiming human tissue is observed almost entirely
cross-sectionally. That is false: repeat sampling is routine in blood,
vaccination time-courses and pregnancy cohorts.

The draft after it led on batch effects. Removing them is the first stage of
any analysis, not a result, and leading on it undersold the work. What ELAJ
provides is a readable sixteen-dimensional space, a controllable trade-off
between discarding donor identity and keeping biology, and the ability to
return a bounded negative answer about a clinical category. None of that is
batch correction, so Q13 no longer mentions it.
