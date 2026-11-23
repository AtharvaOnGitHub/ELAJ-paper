# ELAJ: key points for the submission

Drafted 23 November 2026 for AW to edit. Every number below is already in the
manuscript.

## Why Nature Machine Intelligence

- **This is a machine-learning paper whose test bed is a disease.** It
  contributes a model architecture and an evaluation measure, and it uses
  them to settle biological questions. NMI publishes this kind of work:
  TIGON, MIDAS, Eye2Gene and PlantRNA-FM are NMI papers that pair a method
  with a domain result.
- **It speaks to a live debate in the field: scale or inductive bias.**
  Single-cell biology is moving towards foundation models. ELAJ shows that on
  a corpus limited by donors, a 1,883,986-parameter model built around the
  disease outperforms four foundation models of up to 100 million
  parameters. NMI readers are the audience for that result.
- **The evaluation problem is general.** In any disease atlas where a
  biological variable is constant within a donor, batch correction and
  biology cannot be told apart by the field's standard metrics. The measure
  we define for that case applies beyond endometriosis.
- **The disease matters.** Endometriosis affects roughly 190 million people,
  has no non-invasive test and needs surgery to diagnose, so every study is
  small. Pooling is the only route to scale.

## Novelty

1. **The first single-cell disease atlas of endometriosis built from every
   public study:** 1,577,728 cells from 254 donors across eleven studies.
   Earlier single-cell work spans tens of donors, up to 63 in the healthy
   endometrium reference atlas (HECA).
2. **Inductive bias in place of pretraining scale.**
   - Genes are read in 44 pathway groups, each by its own transformer.
   - Domain-specific batch normalisation normalises each study by its own
     statistics.
   - An adversarial head removes study identity.
   - A sentinel marks genes a study never measured, which is different from
     a gene measured at zero.
   - Cells are compressed into a sixteen-dimensional latent space.
3. **The ELAJ frontier.** Two coefficients trace a Pareto front between
   donor-blindness and retained cycle signal. ELAJ dominates all nine
   competing representations on both axes: four foundation models, scVI,
   scANVI, Harmony, Scanorama and PCA.
4. **Cross-donor agreement, a new evaluation measure for disease atlases.**
   It scores a label using only neighbours from other donors' cells. We show
   that the standard scIB metrics do not discriminate on this corpus, and
   explain why.
5. **Published claims tested at atlas scale.** Claims made from tens of
   donors are retested on 254. Some hold and some do not, and the tests
   behind each verdict are reported in a claims ledger.

## Main ideas, in the order the paper argues them

1. **The problem.** Every donor was biopsied once, so menstrual phase is
   constant within a donor and looks exactly like a batch effect. Removing
   batch therefore risks removing the cycle, the strongest biology in the
   tissue.
2. **The trade-off is measurable.** Removing donor identity costs cycle
   signal, and ELAJ's two coefficients set the exchange rate. ELAJ's cycle
   agreement reaches 0.7346, against 0.4372 to 0.7303 for the nine
   competitors.
3. **Biology emerges from training.** Cell identity and the menstrual cycle
   were withheld from the model, apart from one supervised phase label. Both
   are recovered in the latent. The cycle appears as one continuous axis
   that orders a held-out study's donors by clinical cycle day and by serum
   progesterone.
4. **What the atlas says about the disease.**
   - Patients separate from controls by cross-donor agreement (0.3364,
     P = 0.005).
   - Each per-donor disease axis traces to cell composition, the menstrual
     cycle or the sample.
   - Surgical severity is not separable in any of ten representations.
   - Cell composition does not differ between patients and controls.
   - Cyclical variation persists in disease.
5. **The design choices are tested.** Ablation studies remove each
   architectural assumption in turn and measure what it was carrying.
