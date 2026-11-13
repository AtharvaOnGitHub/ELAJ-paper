# Results — the new structure

**Rewritten 13 November 2026 from `RESULTS_INVENTORY.md` with AW's comments
applied. This overwrites the plan, and the prose it describes overwrites
`sections/02-results.tex` entirely.**

**Edit this file. Nothing gets written as prose until you have.**

---

## The budget, and it is tight

NMI's own spec, from `Nature_websites/NMI_Content_Types.pdf`:

> Main text up to **3,500 words**, excluding abstract, Methods, references
> and figure legends. Display items up to **6**. Results and Methods divided
> by topical subheadings; **the Discussion does not contain subheadings.**

⚠ **Two collisions to settle.**

**NMI forbids Discussion subheadings; the supervisor asked for a sectioned
Discussion.** That is for the Discussion pass, not now, but it will not go
away.

**The arithmetic.** Current Results is **2,314 words** and does not contain
the claims axis at all. With Introduction at ~750 and Discussion at ~1,000,
Results gets **~1,750**. So the section has to **add a whole result type and
lose 550 words**. Every budget below is written to that, and the savings come
from compressing A, C and D, which is exactly what AW's comments direct.

---

## What changed, from AW's comments

| was | now |
|---|---|
| Type A as a subsection | **dissolved.** A1 joins the frontier; A2 becomes a recurring flex; A3 cut; A4 and A5 are one-liners |
| A2 parameter efficiency as a result | **not a result, a flex.** Intro sets up the cost of large models, Results states the numbers pointing at a figure, Discussion carries the passage |
| A3 width vs cycle, ρ −0.650 | **cut.** AW: a weak claim about foundation models on a single disease |
| B1, B2, B3, B5 as separate | **one passage.** B3 is supporting proof, not a finding of its own |
| B4 donor memorisation | **its own paragraph, told slowly**, so the 54× lands |
| C3 disease with C6, C7 severity | **one subsection on disease, severity and stage** |
| C4 immune displacement | **moves into the claims axis** as per-study validation |
| C5 non-replication in Dümpelmann | **Supplementary.** A non-result is not a result |
| C6 held-out stage | **cut.** Whole-corpus only |
| C8 negative controls | **Supplementary**, one line in prose. See the note below |
| D1–D5 ablations | **one paragraph**, detail to Supplementary |
| E as nine findings | **grouped by claim, one paragraph each, as a story that leads somewhere** |
| E9 untestable claims | **Discussion**, under limitations and future work |
| F as four findings | **one dense subsection** |

**On C8, since AW asked what it is.** They are negative controls: three
measures that are purely technical — what fraction of a cell's reads are
mitochondrial, how many reads it got, and how likely it is to be two cells
stuck together. If the latent tracked those as strongly as it tracks biology,
the "biology" could be an artefact of sequencing quality. It does not:
0.3396, 0.2514 and 0.1366 against serum progesterone at 0.4725 and epithelial
pseudotime at 0.5801. **It is a control, not a result**, and it is weakened
by the best-of-sixteen estimator, which stops the controls sitting near zero.
**Supplementary, with one clause in prose.**

---

# The new Results, seven subsections

Headers state the result, per the supervisor's rule. These are working
headers, not final wording.

## [R1] Removing the donor costs cycle signal, and the two knobs trace the trade-off
**~420 words. Figure 2.**

Four paragraphs.

1. **B4, slowly.** The latent puts 32.7% of a cell's hundred nearest
   neighbours in the same donor, against a chance rate of 0.60% across 269
   donors. **Fifty-four times enriched.** This is the problem the paper
   exists to measure, and it needs the arithmetic spelled out rather than
   asserted.
2. **B1 and B2.** Six arms, two knobs. Donor recovery 0.3975 to 0.5837,
   cycle 0.5922 to 0.7346, moving together. The adversary buys
   donor-blindness free up to the middle weight — dab7 to dab168 drops donor
   0.5837 to 0.5188 with cycle flat at 0.7337 to 0.7346 — and buys nothing
   beyond it.
3. **B5 and A1.** The two reported arms, then the comparison: **all nine
   competing representations are worse on both axes at once**, higher donor
   recovery and lower cycle agreement, nine out of nine. **A2's flex lands
   here in one clause**, 1,883,986 parameters against scFoundation's 100M,
   pointing at the figure.
4. **B3 as supporting proof.** Across the ten methods donor recovery predicts
   the disease score (ρ = +0.721, p = 0.019) and does not predict cycle
   (+0.176, p = 0.627). So the trade-off is specific, and an axis that tracks
   memorisation is not a performance axis.

## [R2] Sixteen dimensions carry cell identity and the menstrual cycle
**~180 words. Figure 1d.**

C1, on all 1,577,728 cells: cell family 0.9807 and menstrual phase 0.6796
cross-donor, both at p = 0.005, on 630,689 and 723,599 labelled cells.
One clause for the negative controls pointing at Supplementary.

**This subsection is load-bearing out of proportion to its length.** Nothing
in R3, R4 or R5 means anything unless the latent is first shown to hold
biology at all.

## [R3] The cycle signal concentrates in stromal and epithelial cells
**~200 words. Needs a figure, see below.**

C2. Proliferative to secretory displacement, divided by each cell type's own
spread: stromal 1.0677, epithelial 0.9824, endothelial 0.3918, immune 0.3409.

**AW: an emergent property that deserves a spotlight.** The phase head is a
single linear map over the whole latent and it was never given cell type.
The model was not told that the cycle acts on stroma and epithelium more than
on blood vessels and immune cells. It arrived there.

Discussion carries the matching paragraph.

## [R4] Disease status is recoverable; surgical severity is not
**~320 words. Dissociation panel.**

C3, C6, C7, E5 together, because they are one claim with four measurements.

- **Disease status: 0.3364, p = 0.005.** From endometrium inside the uterus,
  the model distinguishes a person with lesions elsewhere.
- **Merged severity clears its null**, measured twice from two files: 0.2655
  at p = 0.005 and 0.1286 at p = 0.025, both on 118 donors. ⚠ Both stay per
  AW's ruling, and the prose must name which estimator each comes from.
- **Mild against severe, among patients only, does not**: 0.0744, p = 0.129,
  57 donors.
- **Surgical stage on the whole corpus: +0.3320, p = 0.005**, 58 donors.
  Held-out is cut. **Grade is negative in all six arms**, −0.0723 to −0.0227.
- **E5**: composition does not track severity either, 51 donors, all p > 0.16.

**The reading, one line:** the model says whether a person has the disease
and not how severe a surgeon judged it, and two independent measurements
agree on that.

## [R5] The atlas settles claims no single cohort could
**~480 words, the longest subsection, and the one that does not exist yet.
Needs a new figure.**

Four paragraphs that move, and the story leads to the gene list.

1. **Counting fails.** Composition does not differ between control and
   eutopic endometrium: 194 donors, eleven studies, every family p > 0.23.
   Dümpelmann claimed this from 60 donors; it holds at three times that.
   **So the disease is not in how many cells of each kind there are.**
2. **Reading works, and it is immune.** The disease direction does not exist
   globally (held-out AUC 0.536 against a 0.482 null) but does inside the
   immune compartment: **0.708 against 0.481, p = 0.015**, 94 donors.
   Mixing the families destroys it, 0.605 at p = 0.155. **C4 lands here**:
   immune displacement is highest of four families in Marečková, 0.7732 and
   0.8321.
3. **What those cells are doing.** Decoding the direction through the decoder
   gives TREM1, IL1B, CCL13, SIGLEC7, ADAMDEC1, SERPINB2, MMP19, MMP27,
   LRRC15, INHBA — macrophage-led inflammation. **Four of the top fifteen are
   in an external cohort's upregulated list, hypergeometric p = 4.0 × 10⁻⁷**;
   no control-side gene is. **IL1B is first in Dümpelmann's own classifier's
   importance ranking.** Four genes have no prior endometriosis report in the
   corpus, Open Targets or PubMed.
4. **And one published claim does not hold.** Huang's cycle-flattening claim
   fails two ways, at 112 and 101 donors against their 13. E7 gets one
   sentence with its dissociation caveat attached.

## [R6] What the architecture needs
**~160 words. Supplementary figure.**

D1 to D5 as one paragraph. The two that carry weight:

- **Removing the phase head costs cycle 0.7346 → 0.4812, and 65.5% of the
  chance-corrected signal survives.** The head accounts for 34.5%; the
  architecture carries the rest. This is the inductive-bias claim made
  numeric.
- **Random gene groups cost disease 0.3364 → 0.2698 and family 0.9820 →
  0.9606.** Pathway grouping is load-bearing.

ECS, the sentinel and the statistics path get a clause each. Everything
else, including D2's overfitting trajectory, goes to Supplementary.

## [R7] What this says about how integration is measured
**~150 words, dense. No figure.**

F1, F2, F4 in one paragraph. The disease axis as the field scores it is
partly a donor-memorisation readout. Cell family is saturated across every
method, 0.9023 to 0.9896 against a cycle spread of 0.2974, so the metric
cannot discriminate where it is most used. And both gene-disease databases
have false negatives our own verified hits expose.

**This is the subsection that makes the paper a case study rather than a
benchmark.** It is short on purpose.

---

# Totals and what it costs

| | words |
|---|---:|
| R1 frontier | 420 |
| R2 the latent read | 180 |
| R3 cycle by cell type | 200 |
| R4 disease and severity | 320 |
| R5 the claims axis | 480 |
| R6 ablations | 160 |
| R7 measurement | 150 |
| **total** | **1,910** |

Against a 1,750 budget that is **160 over**, which is close enough to seed
and cut. The current 2,314 loses 400 words and gains a 480-word subsection.

---

# What this does to the display items

**This is the detour AW flagged, and it is forced by two things**: A2 now
needs a figure, and R5 has no figure at all.

**Proposed five, against NMI's cap of six:**

| | what | change |
|---|---|---|
| Fig 1 | graphical abstract, architecture, frontier, cell-family latent | none |
| **Fig 2** | **the frontier, plus a parameter-efficiency panel, plus the donor-against-disease scatter** | **A2's figure lands here, and it is also the answer to "Figure 2 must stop looking like a benchmark"** |
| Fig 3 | the nine endometriosis UMAPs | renumbered from 4 |
| **Fig 4** | **NEW: the claims axis.** Per-family AUC against the null, then ranked gene shifts with the replicating genes marked and the four unreported ones marked differently | **new** |
| Table 1 | every arm | none |

**Two panels still have no home** and both are AW's calls:

- **R3's cycle-by-cell-type figure.** Four small panels or one grouped bar.
  Could be a Figure 3 panel, could be Extended Data. AW called this an
  emergent property deserving a spotlight, which argues for the main text.
- **The dissociation panel for R4.** Built, pinned, still unplaced.

If both go into the main text we are at six, which is the cap exactly.

---

# Open questions for AW

1. **Does R3 get a main-text panel or Extended Data?** You called it a
   spotlight result; the budget says Extended Data.
2. **Where does the dissociation panel go?** Figure 3 panel, or Extended Data.
3. **Is five display items right, or do we push to six?** Six is the cap and
   leaves nothing for a reviewer-requested addition.
4. **R2 is 180 words for the result everything else rests on.** Too thin?
5. **Is R7 a subsection or the Discussion's opening?** It is interpretation
   wearing a result's clothes, and the honest answer may be that it belongs
   in the Discussion.
