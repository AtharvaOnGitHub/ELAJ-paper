# ELAJ: key points

**One-line overview.** 

In this paper we build a single-cell disease atlas where
inductive bias replaces pretraining scale, and use that to measure the
trade-off between removing batch effects and keeping biology on a corpus
limited by donors.

**Framing and positioning**
- **We are not a method or framework paper.** A method or framework paper
  requires reproducibility on a second dataset. The model can be adapted for
  any size, but this paper takes an endometriosis disease atlas as a case study.
- **Atlases need to be tailored.** The field's atlas-building review (Hrovatin et
  al., Nat. Methods 2025) says *"no one-size-fits-all protocol for atlas
  building exists"*. The paper also doesn't cover our case, where a biological
  variable looks a lot like a batch effect.
- **Size.** Our model is up to 50 times smaller than the foundation models we beat. 
- **Biological inductive bias.** We make assumptions about the data that 
  others try to solve using more parameters and more data. The assumptions 
  are based in biology.


**Why NMI.** 
- **The main contribution is in ML.** The model and its characteristics are
  the main contribution. Biological data is the use case.
- **Methods is unbounded.** The architecture and how it works are the
  contribution, and Methods is the place to explain it. NMI does not restrict
  the Methods section, so NMI is a good fit.
-[Add 1-2 points based on what NMI says they want/look for in a paper]

**Novelty**
- **Every public endometriosis single-cell study in one atlas**: 1.58M cells,
  254 donors, 11 studies, about four times the largest earlier integration. 
- **Validating claims on a larger scale.** Because the data are collated, we
  can test claims made by smaller studies on a much larger scale, with
  more statistical power.
- **Gene grouping.** Representing a cell in groups of genes is novel, efficient
  and effective, and a new approach to representing cells for any AI model.
- **Cross-donor agreement:** a measure for labels that batch correction can
  erase. scIB's biological half saturates on this corpus.
  

**Findings**
- Cell identity, cycle day and progesterone emerge without being taught;
  only menstrual phase was supervised.
- Patients separate from controls (P = 0.005).
- Surgical severity is not separable in any of ten representations.
- Cell composition does not differ between patients and controls. Factors
  determining disease existence are measured and reported.
- The menstrual cycle creates a cyclic behaviour in disease.