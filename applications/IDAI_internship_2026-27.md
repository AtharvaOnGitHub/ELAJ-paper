# IDAI Student Internships 2026/27 — answers for Q12–Q15

Register taken from the projects IDAI funds: *"Towards a Foundation Model for
Cross-Species Molecular Perturbations"*, *"AI-Driven Accelerated Qualification
of Fusion Reactor Materials"*, *"Networked Instability: Quantifying Genomic
Disorder"*. Direction-setting, year-scale, domain-led.

---

## 12. Project Title

**AI for Human Biology: Towards Physiological Coordinates for Human Tissue**

*Alternatives:*
- AI for Human Biology: Recovering Dynamic Biology from Static Human Data
- AI for Human Biology: Reading Time out of Human Tissue

---

## 13. Project Summary & Immediate Objectives (250 max)

Human tissue is observed almost entirely cross-sectionally: one donor, one
timepoint, once. Yet almost everything clinically important about tissue is
dynamic — how it changes across the menstrual cycle, across gestation, with
age, with disease progression, under treatment. Standard analysis destroys
precisely that information, because a quantity constant within a donor is
geometrically identical to a batch effect and is removed along with it. The
dynamics of human biology are being discarded as noise, at scale, across the
field.

This project builds the capability to read dynamic human biology out of static
human data.

The existence proof is in place. Pooling 1,577,728 single-cell profiles from 11
studies and 269 donors, the intern recovered the menstrual cycle as a closed
trajectory from donors each sampled on a single day, with cycle structure
surviving the removal of donor and study identity. The cycle is the decisive
test case: a periodic process with a known period and external physiological
ground truth. It works. The internship generalises it.

**Objective 1 — physiological coordinates.** Infer a donor's position on a
biological axis from transcriptome alone and transfer it across cohorts and
tissues. Chronological age, gestational age and disease stage are all
donor-constant and all currently confounded.

**Objective 2 — identifiability.** Map the donor counts, cohort structures and
axis geometries under which donor-constant biology is separable from batch at
all. This is an open foundational question.

**Objective 3 — diagnostic consequence.** Test whether correcting for inferred
physiological position rescues biomarkers that fail to replicate between sites.

Delivered on Baskerville.

---

## 14. Alignment with the UK Government Industrial Strategy (IS8) (150 max)

**Life Sciences.** The Life Sciences Sector Plan commits up to £600 million to a
Health Data Research Service to make population-scale health data usable. The
obstacle that investment meets is that pooled human cohorts cannot be compared
while the biology of interest is confounded with the cohort that measured it.
Physiological coordinates remove that obstacle, and the clinical prize is
direct: biomarkers that fail to replicate between sites may be failing because
subjects are compared at different points in a moving process.

**Digital and Technologies.** Recovering a temporal process from subjects each
observed once is a general AI capability, built on UK national compute and
applicable to any multi-site human dataset.

**UN Sustainable Development Goals.** SDG 3 directly, and SDG 10: conditions
whose study requires surgery stay data-poor, and this work makes such data
usable.

---

## 15. Expected Value & Path Forward (200 max)

**To the research.** This establishes a new line of work with three independent
strands: a transferable model of physiological position, a theory of when
donor-constant biology is recoverable, and a diagnostic principle for
cross-site replication. Each is separately publishable and separately fundable.

**To the intern.** A route from MSc project into funded doctoral research on a
programme he has already proven at 1.58 million cells, with first-authored
biological and methodological results and experience at scale on national
compute.

**Path forward.**

1. *Grants.* Objective 2 is pilot data for a UKRI or EPSRC application on
   identifiability under confounding; Objective 1 for an MRC or Wellcome
   application on cycle- and age-resolved tissue biology; Objective 3 for NIHR
   on cross-site diagnostic reliability. Together they fund the intern's PhD.
2. *Collaborations.* Validating physiological coordinates requires prospectively
   dated samples, so a clinical partner is the first ask and we will secure one
   through the supervisor's networks. Public atlas consortia are the second,
   since the method's value grows with the number of tissues it spans.
3. *Compute.* We will apply for Baskerville access for delivery.

---

## Checklist for the supervisor

1. **Name an external partner in Q15 if one can be named.** Evidence of
   non-academic engagement is a priority criterion. Q15 currently commits to
   securing a clinical partner through your networks.
2. **Baskerville access** to be applied for; Q13 and Q15 both say so.
3. **Training material was removed on request.** It is a priority criterion in
   the call, so this gives up a scoring point.
4. **SDG 5 is deliberately not cited.** It is available and would be an easy
   additional hook, but this project's stated position is that endometriosis is
   a human health problem rather than a gendered one, and the whole body of work
   is written that way. Reinstate only if you want that position changed.

## Sources for the figures used

| figure | source |
|---|---|
| 1,577,728 cells; 11 studies; 269 donors | the project's own corpus metadata |
| the cycle recovered as a closed trajectory | the project's own whole-corpus embedding |
| £600m Health Data Research Service | UK Life Sciences Sector Plan, July 2025 |
| IS8 sector list | UK Modern Industrial Strategy, June 2025 |
