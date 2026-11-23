# ELAJ: key points

**The line.** In this paper we build a single-cell disease atlas where
inductive bias replaces pretraining scale, and use that to measure the
trade-off between removing batch effects and keeping biology on a corpus
limited by donors.

**Why it is framed this way**
- **A case study, not a method or framework.** A method or framework paper
  owes proof on a second dataset. There is no second endometriosis corpus:
  this corpus is the whole field.
- **The review licenses it.** The field's atlas-building review (Hrovatin et
  al., Nat. Methods 2025) says *"no one-size-fits-all protocol for atlas
  building exists"*. Its guidance on batch covariates does not cover a
  phenotype that is constant within a donor. Menstrual phase is that case.
- **The two halves connect.** A 1.88M-parameter model can be retrained 11
  times: six frontier arms and five ablations. A pretrained 100M model gives
  one fixed point. Inductive bias is what makes the trade-off measurable.

**Why NMI.** The atlas is built by machine learning, and its central result
is a measured trade-off between removing batch effects and keeping biology.
That answers the scale-versus-design question on real disease data.

**Novelty**
- Every public endometriosis single-cell study in one atlas: 1.58M cells,
  254 donors, 11 studies, about four times the largest earlier integration.
- The ELAJ frontier beats all nine competitors, four of them foundation
  models, on donor removal and retained cycle signal together.
- Cross-donor agreement: a measure for labels that batch correction can
  erase. scIB's biological half saturates on this corpus.

**Findings**
- Cell identity, cycle day and progesterone emerge without being taught;
  only menstrual phase was supervised.
- Patients separate from controls (P = 0.005).
- Surgical severity is not separable in any of ten representations.
- Cell composition does not differ between patients and controls.
- Cycling persists in disease.

**Do not say**
- "Few donors": say "limited by donors".
- "Foundation models are useless": they give no advantage on this corpus.
- "Framework" or "playbook".
- That scIB is wrong: it is saturated on this corpus.
