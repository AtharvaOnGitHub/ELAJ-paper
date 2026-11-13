# R1 — Batch effects and biology have a measurable trade-off

Every number you could use, what it means, and what it will not support.
Nothing here is prose. All values re-derived by `audit_numbers.py`; sources
named so you can check any of them.

**Two axes run through everything below.**

- **Donor recovery** — how well a cell's neighbours from *other* donors still
  betray which person it came from. **Lower is better.** This is the batch
  axis.
- **Cross-donor cycle agreement** — how often a cell's neighbours from other
  donors are at the same menstrual phase. **Higher is better.** This is the
  biology axis.

Both discard same-donor neighbour pairs before scoring, so neither can be won
by simply clustering each person together.

---

## 1. How much donor identity SURVIVES — and this is a bad number, not a good one

**Corrected 13 November. My first version of this block was wrong and AW
caught it.** I described 32.7% against 0.60% as "the size of the problem",
implying it measured uncorrected data. It does not. **It is measured on our
own reported arm's latent**, and `validation.csv` says so in its own note
column: *"high is BAD -- individual identity"*. There is no before-correction
measurement anywhere in that file.

Both figures below are the same estimator, `knn-agreement` on `patient_id`,
on different cell sets:

| | cells | donors | chance | excess | raw | enrichment |
|---|---:|---:|---:|---:|---:|---:|
| whole corpus | 1,577,728 | 269 | 0.0060 | 0.3229 | 0.3270 | **54.5x** |
| held-out, the field table's value | 416,256 | 70 | 0.023 | **0.5188** | 0.5299 | **23.0x** |

Fewer donors raises the chance rate, which is why the two differ. **Quote one
or the other, never both without saying which cell set.**

**Means:** after the adversary has done its work, a cell's neighbours are
still 54.5 times more likely to come from its own donor than chance allows.
**We did not remove the batch effect. We priced it.**

**How to use it, and this is the only honest framing.** Donor identity
persists in every representation tested. \elaj$_{B\,hi}$ retains the least of
the ten, 0.5188 against 0.5421 to 0.7892, and it is still far from
donor-blind. That combination is the paper's position: the trade-off is real,
unsolved, and we report the best available point on it rather than claiming
to have escaped it.

**Will not support:** "the model removes batch effects". It reduces them
further than anything else tested and leaves a great deal behind.

⚠ **Consider whether this belongs in R1 at all.** It invites "your model
memorises donors 54 times over chance", which is true. Against dropping it:
it is the number that makes the frontier matter, and the Discussion needs it
anyway. My view is that it belongs, stated as a cost, immediately beside the
comparative 0.5188 that shows nobody does better.

## 2. Why the two cannot be separated

**Every donor contributed one biopsy.** So menstrual phase is constant within
a donor, and a per-donor offset is the same geometric object as a batch
effect.

**Means:** this is the reason there is a trade-off at all rather than a free
lunch. Any correction treating the donor as nuisance removes cycle with it.

**This is the one fact in R1 with no number attached.** It is the mechanism,
and Hrovatin's review names the problem and prescribes coarsening to dataset
level without measuring what that costs.

## 3. The trade-off itself — six arms, two knobs

Two coefficients: the adversarial weight on the DAB branch, and the KL
coefficient on the latent.

| arm | adversarial weight | KL | donor ↓ | cycle ↑ | study mixing ↓ | cell family ↑ |
|---|---:|---:|---:|---:|---:|---:|
| dab7_kl1 | 7 | 1 | 0.5837 | 0.7337 | 0.8636 | 0.9829 |
| **dab168_kl1 = B$_{hi}$** | 168 | 1 | **0.5188** | **0.7346** | **0.7613** | **0.9820** |
| dab336_kl1 | 336 | 1 | 0.5277 | 0.7146 | 0.8200 | 0.9779 |
| dab7_kl30 | 7 | 30 | 0.5389 | 0.6791 | 0.8587 | 0.9841 |
| **dab168_kl30 = B$_{lo}$** | 168 | 30 | **0.3975** | **0.6033** | **0.6544** | **0.9565** |
| dab336_kl30 | 336 | 30 | 0.4154 | 0.5922 | 0.7190 | 0.9553 |

**Ranges:** donor 0.3975 to 0.5837, cycle 0.5922 to 0.7346.

**Means:** the knobs move the model *along* a curve, not to a better point.
Every arm that removes more donor gives up cycle.

**Will not support:** that one arm is correct. The paper's position is that
the choice is a reporting decision, not an optimisation.

## 4. The knee — adversarial pressure is not uniformly priced

Reading down the KL = 1 column:

| step | donor | cycle |
|---|---|---|
| weight 7 → 168 | 0.5837 → **0.5188**, a real gain | 0.7337 → 0.7346, **unchanged** |
| weight 168 → 336 | 0.5188 → 0.5277, **worse** | 0.7346 → 0.7146, **worse** |

**Means:** the first dose of adversarial pressure is free; the second is
wasted. Past 168 the adversary gives nothing back and the KL coefficient is
the only remaining lever.

**Will not support:** a claim about where the knee sits in general. Six arms
on one corpus.

## 5. The two reported arms, and what separates them

| | cycle ↑ | donor ↓ | study mixing ↓ | cell family ↑ |
|---|---:|---:|---:|---:|
| **B$_{hi}$** | 0.7346 | 0.5188 | 0.7613 | 0.9820 |
| **B$_{lo}$** | 0.6033 | 0.3975 | 0.6544 | 0.9565 |

**Means:** B$_{lo}$ buys better donor-blindness and better study mixing by
giving up 0.13 of cycle agreement. The two bracket the useful range.

**B is for biology**, and in Marathi the pun lands twice.

## 6. The nine competitors — the dominance result

All scored on the identical corpus. **Sorted by cycle agreement.**

| method | width | supervised on | cycle ↑ | donor ↓ | study mixing ↓ | cell family ↑ |
|---|---:|---|---:|---:|---:|---:|
| **\elaj{} B$_{hi}$** | **16** | menstrual phase | **0.7346** | **0.5188** | 0.7613 | 0.9820 |
| scanorama | 100 | — | 0.7303 | 0.7892 | 0.8632 | 0.9866 |
| scVI | 16 | — | 0.7053 | 0.6888 | 0.8776 | 0.9828 |
| scANVI | 16 | cell family | 0.6971 | 0.6893 | 0.8683 | 0.9832 |
| PCA | 16 | — | 0.6457 | 0.6923 | 0.9510 | 0.9866 |
| scFoundation | 3072 | — | 0.6449 | 0.7675 | 0.9272 | 0.9832 |
| SCimilarity | 128 | cell family | 0.6255 | 0.6516 | 0.8669 | 0.9896 |
| Harmony | 50 | — | 0.6186 | 0.6932 | 0.6697 | 0.9823 |
| scGPT | 512 | — | 0.4869 | 0.5630 | 0.7682 | 0.9840 |
| Geneformer | 256 | — | 0.4372 | 0.5421 | 0.7964 | 0.9023 |

**The dominance claim, checked nine times:** every competitor has **both** a
higher donor recovery than 0.5188 **and** a lower cycle agreement than
0.7346. Nine out of nine. Competitor donor range 0.5421 to 0.7892;
competitor cycle range 0.4372 to 0.7303.

**Means:** there is no point below-and-left of us. This is the strongest
single claim in the paper and it is what makes the frontier a frontier rather
than a line we happen to sit on.

**Will not support:** that \elaj{} is better at everything. **Harmony mixes
studies better** (0.6697 against our 0.7613) and **SCimilarity recovers cell
family better** (0.9896 against 0.9820). Say the axes.

⚠ **Cell family is saturated across the whole field**, 0.9023 to 0.9896,
spread 0.0873, against a cycle spread of 0.2974. Nobody's cell-family number
means anything. Worth one clause; it is also an argument that scIB's
biological half cannot discriminate here.

## 7. Size, and this is the NMI credential

| | parameters | latent width | pretraining corpus |
|---|---:|---:|---|
| **\elaj{}** | **1,883,986** | **16** | none; trained on 1,577,728 cells |
| scFoundation | **100,000,000** | 3072 | **over 50 million cells** |
| scGPT | — | 512 | 33 million cells |
| Geneformer | — | 256 | ~30 million cells |

**Sources:** our count is in the training log,
`Outputs/p_series/p1_dab168_kl1/train_57935604.log` line 230, "Model
parameters: 1,883,986". scFoundation's is its own abstract: *"100 million
parameters covering about 20,000 genes, pretrained on over 50 million human
single-cell transcriptomic profiles."*

**Means:** 53× fewer parameters and no pretraining at all, and it beats them
on cycle. The ratio to state is **53×**, or "two orders of magnitude".

**Will not support:** "foundation models are useless." Only that four of them
give no advantage on this corpus. That wording is settled.

## 8. The disease axis is partly a memorisation readout

Spearman across the ten representations, one point per method.

| donor recovery vs | ρ | p |
|---|---:|---:|
| **disease score** | **+0.721** | **0.019** |
| cycle agreement | +0.176 | 0.627 |
| cell family | +0.409 | 0.241 |

**Means:** a method that remembers donors scores better on disease, and does
not score better on cycle. Since control and case are both donor-level
labels, the asymmetry is not explained by the labels. The disease axis as the
field computes it reads out memorisation as well as biology.

**Two uses, and they are different.** As a caveat on *everyone's* disease
numbers including ours. And as the reason our cycle advantage is credible:
we memorise donors *less* than eight of nine competitors and still recover
cycle best, so the advantage cannot be identity leaking through.

**Will not support:** a causal claim. Ten points, one corpus.

---

## What R1 does not need to carry

- **Ablations** — R6.
- **What the latent holds** — R2.
- **Disease, severity, stage** — R4.
- **Anything about pathway groups** — R6.
- **Figure panel numbers** — figures are deferred until Results is done, so
  leave `(Fig. X)` markers and we will fill them.

## The one thing I would not leave out

**Section 2.** It is the only part of R1 with no number, and it is the reason
the rest of the subsection exists. Without it a reader sees two metrics
moving in opposite directions and no reason why they must.
