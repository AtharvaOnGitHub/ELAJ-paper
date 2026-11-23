# ELAJ: key points

**One line.** A single-cell disease atlas of endometriosis in which
inductive bias replaces pretraining scale. It outperforms foundation models
50 times its size.

**Why NMI**
- A machine-learning method and evaluation, proved on a disease.
- It answers the field's scale-versus-design debate with a result.
- The evaluation problem is general to any donor-limited disease atlas.

**Novelty**
- Every public endometriosis single-cell study in one atlas: 1.58M cells,
  254 donors, 11 studies. Earlier studies had about 60 donors at most.
- 1.88M parameters, against foundation models of up to 100M: genes read in
  44 pathway groups, per-study batch norm, adversarial study removal.
- The ELAJ frontier: it beats all nine competitors, four of them foundation
  models, on donor removal and retained biology together.
- Cross-donor agreement: a new metric for when biology looks like batch.
  The standard scIB metrics fail on this corpus.

**Findings**
- Cell identity, cycle day and progesterone emerge without being taught;
  only menstrual phase was supervised.
- Patients separate from controls (P = 0.005).
- Surgical severity is not separable in any of ten representations.
- Cell composition does not differ between patients and controls.
- Cycling persists in disease.
