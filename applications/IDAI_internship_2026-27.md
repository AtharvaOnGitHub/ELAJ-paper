# IDAI Student Internships 2026/27 — answers for Q12–Q15

Redrafted 3 November 2026 at the altitude IDAI actually funds. The past-projects
list sets the register: *"Towards a Foundation Model for Cross-Species Molecular
Perturbations"*, *"AI-Driven Accelerated Qualification of Fusion Reactor
Materials"*, *"From Ambulatory Data to Clinical Prediction"*. These are
direction-setting proposals, not eight-week work plans, and one 2025 project is
recorded as having unlocked £62k of industrial funding. The first draft of this
form was scoped to what was already finished; this one is not.

**Biology leads. The AI is the instrument, not the subject.**

---

## 12. Project Title

**AI for Endometriosis: Towards a Transferable Molecular Clock for a Cyclical
Disease Sampled Once**

*Alternatives:*
- AI for Endometriosis: Recovering the Menstrual Cycle from Single-Snapshot Cohorts
- AI for Endometriosis *(plain, if the form prefers it)*
- AI for Human Biology: Reading Time from Cross-Sectional Tissue Atlases *(if a
  broader framing is wanted)*

---

## 13. Project Summary & Immediate Objectives (250 max)

Endometriosis is a cyclical disease that medicine only ever measures
acyclically. Diagnosis requires surgery, so every tissue sample is one day of a
roughly month-long process, and each donor is sampled once. Two questions
central to the disease are therefore unanswered: whether the menstrual cycle
itself is altered in endometriosis, and why candidate biomarkers repeatedly fail
to replicate between cohorts.

The intern has pooled 1,577,728 single-cell profiles from 11 studies and 269
donors and trained a model in which menstrual-cycle structure survives the
removal of donor and study identity. That representation is the instrument. This
internship uses it to ask the biology.

**Objective 1 — a molecular clock.** Cycle day is recorded for one cohort only
(466,176 cells, 60 donors, days 5–30). We will learn to infer cycle position
from transcriptome alone and transfer it to the remaining ten cohorts, placing
every donor on a common timeline for the first time.

**Objective 2 — is the diseased cycle a different cycle?** With all donors on
one clock, test whether affected tissue is phase-shifted, flattened, or
decoupled from circulating progesterone. This is a transcriptome-scale test of
progesterone resistance, a long-standing clinical observation never examined at
this scale.

**Objective 3 — is biomarker failure a timing artefact?** Test whether published
endometriosis signatures are phase-dependent in this corpus.

Interdisciplinary, data-intensive, and delivered on Baskerville. Ambitious by
design: each objective is a grant, and the clock is a reusable asset.

---

## 14. Alignment with the UK Government Industrial Strategy (IS8) (150 max)

**Life Sciences.** The Life Sciences Sector Plan commits up to £600 million to a
Health Data Research Service to make population-scale health data usable for
research. Endometriosis is exactly the case that investment must serve and
currently cannot: around 190 million people affected worldwide, no non-invasive
diagnostic test, and a mean interval from first symptom to surgical diagnosis of
11.1 years. Fragmented surgical cohorts cannot be pooled usefully while the
biology of interest is confounded with the cohort. A transferable molecular
clock would let any future biopsy be positioned in cycle time from its
transcriptome, which is a precondition for a phase-aware diagnostic.

**Digital and Technologies.** Recovering a temporal process from subjects each
observed once is a general AI capability, applicable wherever human data is
pooled across sites, and it is being built here on UK national compute.

---

## 15. Expected Value & Path Forward (200 max)

**To the research.** The project currently has a representation; this internship
turns it into an instrument that answers clinical questions. Each objective is
independently publishable, and together they establish a new line of work on
cycle-resolved disease biology rather than extending an existing paper.

**To the intern.** A route from MSc project to funded doctoral research, first-
authored biological results rather than only methodological ones, and experience
at scale on national compute.

**Path forward.**

1. *Grants.* Objective 2 is designed as pilot data for an MRC or Wellcome
   application on cycle dysregulation in endometriosis, and Objective 1 for a
   UKRI methodology application on recovering temporal structure from
   cross-sectional atlases. Both are routes to funding the intern's PhD.
2. *Collaborations.* The clock's natural next experiment needs prospectively
   cycle-dated samples, which requires a clinical partner. We will use the
   supervisor's networks to secure one, and will approach the authors of the
   eleven source cohorts, with whom there is already a concrete basis.
3. *Compute.* We will apply for Baskerville access for delivery.

---

## Must be confirmed before submission

1. **External partner.** Still the single biggest available uplift, and still
   unnamed. Q15 commits to securing one through the supervisor's networks, which
   is honest. If anyone can be named now, name them there.
2. **Baskerville.** Q13 and Q15 commit to it and Q15 says access will be applied
   for, which matches the position.
3. **Removed on request:** the training-material commitment. It is a priority
   criterion in the call, so dropping it gives up a scoring point — flagging
   that, not arguing it.

## Sources for the figures used

| figure | source |
|---|---|
| 1,577,728 cells; 11 studies; 269 donors | the project's own corpus metadata |
| 466,176 cells, 60 donors, days 5–30, one cohort | the project's own corpus metadata |
| 190 million people worldwide | WHO endometriosis fact sheet, updated 15 Oct 2025 |
| 11.1 years to diagnosis | Bontempo & Schiff 2025, *BMJ Open Quality* 14, e003121 |
| £600m Health Data Research Service | UK Life Sciences Sector Plan, July 2025 |
| IS8 sector list | UK Modern Industrial Strategy, June 2025 |

Progesterone resistance is described as a long-standing clinical observation
rather than cited, because the claim here is only that it is well known and
untested at this scale. If a reference is wanted in the form, one should be
added.
