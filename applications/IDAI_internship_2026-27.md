# IDAI Student Internships 2026/27 — answers for Q12–Q15

Drafted 3 November 2026. Every figure here is from the project's own
audited outputs or a verified public source; nothing is estimated.
**Three things need the supervisor's confirmation before submission —
see "Must be confirmed" at the end.**

---

## 12. Project Title

**Biology that looks like batch: an open framework for pooling single-cell
cohorts, built on 1.58 million endometriosis cells**

*Alternatives if a shorter title is wanted:*
- Telling biology from batch effect in pooled single-cell health data
- Donor-confounded signal: measuring what batch correction removes

---

## 13. Project Summary & Immediate Objectives (250 max)

In human tissue studies each donor is normally sampled once. Any trait that is
constant within a donor — menstrual-cycle phase, disease stage, treatment
history — is then geometrically identical to a batch effect, so the correction
methods that make pooled atlases usable can remove the biology along with the
artefact. No standard metric distinguishes the two.

The intern has built and trained ELAJ, a 1.9-million-parameter conditional
variational autoencoder, on 1,577,728 single-cell profiles pooled from 11
endometriosis studies and 269 donors, and has shown this trade-off can be
traced as an explicit, controllable frontier rather than assumed away. A
manuscript is in preparation.

This sprint converts that project's methodological core into a reusable asset.
Three immediate objectives:

1. **Release** an open, documented, installable evaluation package implementing
   the donor-level permutation estimator the project developed, including three
   corrections identified during write-up: study-stratified permutation,
   explicit coverage reporting, and comparability across labels with few donors.
2. **Quantify where standard batch metrics fail** on donor-confounded data. On
   this corpus several widely used scIB metrics are exactly degenerate across
   four different methods — a transferable negative result the package will
   detect automatically.
3. **Demonstrate transfer** on one public atlas outside endometriosis sharing
   the one-sample-per-donor design.

This is interdisciplinary, data-intensive research with AI as the core
discipline and reproducible measurement as the contribution, delivered on
Baskerville and released openly for reuse.

---

## 14. Alignment with the UK Government Industrial Strategy (IS8) (150 max)

**Life Sciences, primarily.** The Life Sciences Sector Plan commits up to
£600 million to a Health Data Research Service to make population-scale data
assets usable by academic and industrial researchers. Making fragmented
cohorts poolable without destroying the biology inside them is precisely the
bottleneck that investment confronts, and this project delivers a measurement
framework for it. The clinical need is acute: endometriosis affects around 190
million people worldwide, has no non-invasive diagnostic test, and the mean
interval from first symptom to surgical diagnosis is 11.1 years.

**Digital and Technologies, secondarily.** The deliverable is foundational AI
methodology — an open, reusable evaluation standard for confounded
representation learning — rather than a single-disease result, and it is
applicable wherever human-subject data is pooled across sites.

---

## 15. Expected Value & Path Forward (200 max)

**To the research.** The project's transferable contribution is currently
locked inside one paper. This sprint releases it as tooling other groups can
apply, and the cross-disease demonstration provides the pilot data a
methodology grant requires. Both strengthen the manuscript under preparation.

**To the intern.** A first-authored software and methods release, experience
running at scale on national compute, and a direct route from MSc project to
funded doctoral research.

**Path forward.** Three concrete routes, in order of readiness.

1. *Grant applications.* The generalisation result is designed as pilot data
   for an EPSRC/UKRI methodology application on measurement under confounding,
   and for an MRC or Wellcome application on endometriosis — a condition whose
   research funding is widely recognised as disproportionate to its burden.
2. *Collaborations.* The eleven source cohorts are an existing, concrete basis
   for approaching their authors; and we will approach third-sector partners
   in this disease area as co-sponsors, which the scheme explicitly invites.
3. *Training material.* The donor-confounding problem is general and poorly
   known. We will produce an IDAI tutorial and notebook on it, reusable across
   the University's health-data community.

---

## Must be confirmed before submission

1. **Baskerville.** The scheme gives priority to proposals using the
   Baskerville NCR. The project's training to date has run on BlueBEAR, not
   Baskerville. Q13 and Q15 as written commit the sprint to Baskerville — only
   keep that if the access is in place or obtainable.
2. **External partner.** Evidence of non-academic engagement is a priority
   criterion and we have none to name. Q15 says we *will approach* third-sector
   partners, which is honest. If a partner can be named now, say so there
   instead — it is the single biggest available uplift to the score.
3. **Training-material commitment.** Also a priority criterion, and Q15
   commits to it. Only keep it if it will be delivered.

## Sources for the figures used

| figure | source |
|---|---|
| 1,577,728 cells; 11 studies; 269 donors | the project's own corpus metadata |
| 1.9M parameters, 16 latent dimensions | the project's model configuration |
| scIB metrics exactly degenerate across four methods | `Outputs/Benchmarks/p1_dab168_kl1/benchmark.csv` |
| 190 million people worldwide | WHO, endometriosis fact sheet |
| 11.1 years to diagnosis, 444 patients | Bontempo 2025, cited in the manuscript |
| £600m Health Data Research Service | UK Life Sciences Sector Plan, July 2025 |
| IS8 sector list | UK Modern Industrial Strategy, June 2025 |
