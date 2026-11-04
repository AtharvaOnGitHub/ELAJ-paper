# Figures — panel by panel

**Edit this file. A panel does not get drawn until its row is agreed.**

Six main display items, which is NMI's cap for an Article. Extended Data is
capped at ten separately and Supplementary Information is uncapped.

Every number in the "supports" column is traceable through
`audit/NUMBERS.md`. Nothing in this file is typed from memory.

---

## Why panels, and why legends are written long

NMI, *Content Types*: main text is up to **3,500 words, excluding abstract,
Methods, references and figure legends**. Nature's formatting guide: legends
"should be fewer than **300 words each**", and a multi-panel composite
"usually needs to take about half a page".

So six figures carry up to **1,800 words of legend that cost nothing against
the 3,500**. A finding that lives in a panel and its legend costs zero
main-text words; the same finding enumerated in prose costs around 125. With
roughly twenty findings and ~2,000 words of Results, the figures are not
illustrations of the prose. They carry findings the prose points at.

Consequence: every main figure is a composite, panels are used generously,
and legends are written to the 300-word limit rather than kept brief.

**Each figure must be regenerable by one command from a committed script.**

**Every cross-donor value in this file is an excess over chance**, computed
as `(agreement − chance) / (1 − chance)` in
`endo_model/evaluation/sufficient_stats.py`. Zero is chance, one is perfect,
and a negative value is possible. **Never subtract a chance rate from one of
them.** The comparator a panel should draw is the permutation null's 95th
percentile, carried per row in the benchmark's own `note` column.

---

## Status vocabulary

| | |
|---|---|
| **exists** | the asset is on disk and is publication-shaped |
| **asset** | the data is drawn but the panel needs compositing or restyling |
| **build** | the data exists, the panel does not |
| **blocked** | waiting on the unified scoring run |
| **draw** | no data, a schematic to be drawn by hand |

---

## The mapping, and why it is a mapping

Six figures, twenty-odd findings, ~2,000 words of Results. A finding that
lives in a panel and its legend costs **zero** main-text words; enumerated in
prose it costs about 125. So the figures are not illustrations of the prose.
They are where the findings that prose cannot hold are gathered.

**What a figure is for here.** Each one clumps the evidence for something the
Results cannot say succinctly, usually because the claim is about *structure*
across many methods or arms rather than about one number. A reader should be
able to reach the conclusion from the panel. They should not be told it
inside the panel.

**What that forbids.** No callouts, no arrows pointing at the good news, no
annotation naming our own arm as the hero, no title that states the result.
The legend defines the axes and the symbols. The data does the rest, and it
stays open to a reader who disagrees with us.

**AW's reading of NMI convention**, from going through the journal's papers:

- Fig 1 is always the overview: *what did we do*. Not the biggest challenge,
  not the most critical datapoint. Absolute terms.
- Fig 2 is a result or the architecture, depending on whether Fig 1 carried
  architecture.
- Figs 3 and 4 are results, often multi-panelled. One had ten panels.
- Often Fig 1 is architecture in the first panels and headline results in the
  last, a dumbed-down representation of the model.
- "I would stray away from study here. At most I'd say we squeeze in one
  graph for study in fig 1."

**Figure 1 is decided. Figures 2–6 are not.** What follows for 2–6 is a
proposal written by Claude, never ruled on. It is kept because the panels in
it exist or are costed, not because it is agreed.

---

## Figure 1 — decided, in AW's words

> "I don't see how the architecture could be split by panels. Instead I would
> give the architecture a long and wide panel a, give frontier panel b, UMAP
> by cell family panel c, UMAP by study as panel d, and UMAP by cycle day as
> panel e."

> "Okay let's try this: make the frontier 2 panels. Choose 2 good plots and
> draw the pareto front. Then put all three UMAPs in the bottom row. Also the
> architecture panel would be like a butterfly with the latent in the middle,
> pathway groups expanding on one side and heads expanding on the other."

| panel | what it is |
|---|---|
| **a** | the architecture, one long wide panel across the top. **Butterfly**: the latent in the middle, the pathway groups expanding on one side, the heads expanding on the other. Shows the main architectural choices we made, **not only the ones ablated** |
| **b, c** | the frontier, two panels, two chosen plots, **Pareto front drawn** |
| **d, e, f** | three UMAPs on the bottom row: **cell family**, **study**, **cycle day** |

**Why the architecture gets a whole panel and not a corner:** "for any AI
paper, the architecture is our baby… I don't wish to squeeze the architecture
into a single section of a panel in an AI paper."

**Open on this figure:**

1. **The spider chart.** Proposed as "one spider chart showing how ELAJ does
   against some baselines", drawn, and left undecided: "I don't think we look
   that bad in the chart, we are high or dominant on all axes… I see the
   argument that we are undersold because it shows the gap being smaller…
   Let's explore this panel further." Alternatives were invited and none was
   chosen.
2. **Whitespace between the first two rows**, unresolved.

**Status:** `figures/scripts/figure1.py` exists and renders. Known defects
carried from the last session: the whitespace above, the clipped
`similarity` and `reconstruction` boxes, and the spider's `cell type` label.

---

## Figures 2 onward — planned from scratch, 4 November

Figure 1 is fixed and absorbs the frontier (b, c) and three UMAPs (d, e, f).
Everything after it is planned by one test, which is the test AW set:

> **what needs to be shown that has too many numbers or claims to be
> explained in prose?**

Results has ~2,000 words across five subsections, so a subsection can carry
roughly eight numbers before it becomes a list. Anything denser than that is
a figure. The count below is the argument for each figure's existence.

| | figure | numbers or claims it holds | prose can hold | so the figure carries |
|---|---|---:|---:|---:|
| **2** | against the field | 10 methods × 5 axes, + 3 correlations = **53** | ~8 | **45** |
| **3** | the cycle by cell type | 4 families × 2 arms, read visually. **No magnitudes in prose at all**, by ruling | 0 | **all of it** |
| **4** | disease and staging | stage and grade × 2 readings × 7 arms, + their nulls = **~30** | ~8 | **22** |
| **5** | what the latent needs | 5 arms × 5 axes = 25, + 2 trajectories, + 28 arm correlations = **~55** | ~6 | **49** |

Four figures after Figure 1. Five of six display items used, one spare.

### Figure 2 — against the field

The venue-justifying figure, and the one the claims changed under. A1 is now
a **joint** claim and a bar chart cannot show a joint claim: the reader has to
see that every other method trades one axis against the other and that one
point sits in the corner. So: the same ten methods, plotted in the planes the
claims live in.

- phase against donor recovery — A1, and the trade-off shape
- study mixing against phase — A2, where Harmony's position is the argument
- disease against donor recovery — A6, the trend is the finding
- phase against embedding width, log axis — A4
- all five axes on a shared range — A5, saturation shown not argued

Carries **A1, A2, A4, A5, A6**. E3 is one sentence of prose and needs no panel.

### Figure 3 — the cycle, by cell type

C2 was ruled out of prose entirely, so this figure *is* the finding. The
embedding split per cell family and coloured by phase, for both frontier
arms, so a reader sees the gradient in stromal and epithelial cells and its
absence in endothelial and immune ones without being given a ratio.

Carries **C2**. C3's closure is Figure 1f; whether it is repeated here is a
layout question, not a content one.

### Figure 4 — disease and staging

Stage and grade, on held-out donors and on the whole corpus, across the
reported arm and the six ablated ones, each against its own permutation null.
That is the comparison C6 rests on and prose can only state two rows of it.

Carries **C6**. **Open: whether C4 and C5 belong here at all.** AW on
4 November: "we made it clear that the model mixes studies so any per-study
metric is irrelevant." That argument reaches the figure as well as the prose.
If it holds, the marecko/duempelmann panels go and this figure is staging
only. **AW to rule.**

### Figure 5 — what the latent needs

Five single-key changes across five axes is 25 numbers before anything else.
Add the training trajectory that shows the held-out split being paid for the
training split, and one correlation per trained arm across 28 arms, and
nothing here fits in prose.

Carries **D1–D6, B2, B3**.

### Mapping back to the Results subsections

| subsection | figures |
|---|---|
| `[1]` the frontier and the field | Fig 1b, 1c; Fig 2 |
| `[2]` the corpus as sixteen numbers | Fig 1d, 1e, 1f |
| `[3]` the cycle | Fig 3 |
| `[4]` disease, and where it is not | Fig 4 |
| `[5]` what the latent needs | Fig 5 |

### Discarded

The Figure 6 drawn on 4 November. Its panels were sound but it was numbered
against a list AW never ruled on, and its content is now Figure 5.

---

