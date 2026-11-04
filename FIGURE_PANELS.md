# Figures, panel by panel

Drafted 4 November 2026 for AW to rule on. Figure 1 is fixed and not
re-opened here. Everything else is specified to the panel: what it shows,
which file the data comes from, the visualisation, the point, and the
options.

**The rule these are written under:** the panel shows data, the legend
defines the axes and symbols, the reader draws the conclusion. No callouts,
no arrows at the good news, no title stating the result.

**Shared assets.** One UMAP of 400,000 cells, cached at
`Outputs/analysis/umaps/p1_dab168_kl1/_umap_cache/global_400000.npy`, drawn
from the whole-corpus latent with `default_rng(24)` then sorted. Every UMAP
panel below is that same embedding with a different colour, which is what
makes a grid of them legible: nothing moves between panels except colour.

---

# Figure 2 — The ELAJ frontier

AW: "It has to be a total show of dominance."

The organising idea is not "we beat them on five axes". It is that **our two
knobs sweep a frontier, and every other method is a single point below it.**
That is a stronger claim than any per-axis win and it is what the data says.

### Panel a — the dominance plane

| | |
|---|---|
| **data** | 10 methods × (cross-donor phase, donor recovery). `audit/NUMBERS.md`, field table |
| **viz** | scatter. x = donor recovery, **axis reversed so better is right**. y = cross-donor phase |
| **point** | A1. ELAJ is the only point that is both highest on phase and lowest on donor recovery |
| **options** | (i) plain scatter with the Pareto front drawn; (ii) **shade the rectangle ELAJ dominates**, so all nine other methods fall visibly inside one box; (iii) both |
| **recommend** | (ii). Nine points inside one shaded rectangle needs no caption to be understood, and it is literally what dominance means |

### Panel b — the frontier itself, with the field on it

| | |
|---|---|
| **data** | the 6 `p1_*` arms as a curve + the same 10 methods as points, same axes as a |
| **viz** | two connected curves (one per information-cost setting) + scattered points |
| **point** | **B1 and A1 in one object.** The knobs generate a frontier; the field sits below it |
| **options** | (i) both knob families as separate curves; (ii) Pareto front across all six arms as one curve; (iii) shade the region above the frontier as unreached |
| **recommend** | (i). The two families *are* the two knobs, which is the finding, and merging them hides it |
| **note** | **this panel is the figure's argument.** If only one panel survives, this one |

### Panel c — mixing against phase

| | |
|---|---|
| **data** | 10 methods × (study mixing, phase). Mixing is **pending** the three CPU jobs |
| **viz** | scatter, x = study mixing (reversed), y = phase |
| **point** | A2. Harmony reaches the best mixing in the table and sits low on phase; PCA sits high on mixing and higher on phase than Harmony does |
| **options** | (i) scatter; (ii) scatter with PCA→Harmony joined by a line, since they are the same data with correction on and off |
| **recommend** | (ii), if and only if a line between two points reads as a comparison and not as an arrow of approval. Otherwise (i) |

### Panel d — disease against donor recovery

| | |
|---|---|
| **data** | 10 methods × (disease, donor recovery) |
| **viz** | scatter, with the rank correlation stated **in the legend, not on the panel** |
| **point** | A6, ρ +0.721. The methods scoring highest on disease are the ones from which a donor is most identifiable |
| **options** | (i) scatter alone; (ii) scatter + a second faint series for phase against donor recovery, which is flat, as the control |
| **recommend** | (ii). The control is what makes A1 safe and it costs one series |

### Panel e — phase against width

| | |
|---|---|
| **data** | 10 methods × (embedding width, phase) |
| **viz** | scatter, **log x** (16 to 3,072) |
| **point** | A4, ρ −0.650 |

### Panel f — every axis at once

| | |
|---|---|
| **data** | the whole field table, 10 methods × 5 axes = 50 numbers |
| **viz** | **parallel coordinates**, one line per method, each axis oriented so better is up |
| **point** | A5 falls out: cell family's axis is a flat bundle, phase and donor fan wide. And the whole table is in one panel |
| **options** | (i) parallel coordinates; (ii) a strip plot per axis; (iii) a heatmap of ranks |
| **recommend** | (i), with the orientation stated in the legend. It is the densest honest view and ELAJ's line reads top on phase, bottom on donor, without being coloured specially |
| **risk** | re-orienting two axes so "better is up" is a transformation. It must be said in the legend or it is a quiet lie |

**Six panels is probably one too many.** The core is **b, a, d, f**. Panels
c and e are each one claim and could go to Extended Data.

---

# Figure 3 — the latent, read by every label

AW: "clump a bunch of UMAPs together… not just cycle but the main ones…
disease and staging could come in here as well."

One embedding, nine colourings. Nothing moves between panels. A reader sees
in one pass which labels structure the latent and which do not, and that is
C1, C3, C6 and the study claim at once.

| panel | colour by | coverage | what a reader sees |
|---|---|---|---|
| a | **cell family**, 4 levels | 45.8% | the latent's primary structure |
| b | **study**, 11 levels | 100% | no island per study |
| c | **menstrual phase**, 4 levels | 50.7% | a gradient within the mass |
| d | **cycle day**, 5–30, cyclic map | 33.4% | the same gradient as a closed loop |
| e | **tissue**, 4 levels | 100% | stromal cells from five tissues together |
| f | **disease status**, 4 levels | 100% | weak, diffuse |
| g | **stage**, 3 levels | 12.4% | no structure |
| h | **grade**, 3 levels | 33.4% | no structure |
| i | **serum progesterone**, continuous | 33.4% | tracks the phase gradient, and was never an input |

**Layout options**

1. **Neutral 3×3 grid**, all equal size, alphabetical by panel letter. Makes
   no claim through arrangement.
2. **Grouped rows:** row 1 the labels that structure the latent (family,
   tissue, phase, day), row 2 those that do not (study, disease, stage,
   grade). Communicates the finding through arrangement.
3. **One large reference panel** (cell family) with eight small ones beside it.

**Recommend 1.** Option 2 states the conclusion through layout, which is the
thing we agreed figures must not do. A reader who disagrees with us should be
able to look at this grid and reach their own view; grouping takes that away.

**Open:** nine panels at 180 mm wide gives each about 55 mm. Legible for
four-level categoricals, tight for eleven studies. May need b's legend
outside the panel.

**Existing:** all nine already render as individual crops in
`Outputs/analysis/umaps/p1_dab168_kl1/`. This is compositing, not new
computation.

---

# Figure 4 — the cycle, and the cells it moves

C2 was ruled out of the prose entirely, so this figure **is** the finding.

| panel | |
|---|---|
| a | all cells, coloured by phase. The reference |
| b–e | the same embedding **split by cell family**, one panel each: stromal, epithelial, endothelial, immune, each coloured by phase |
| f–i | the same four, from the second frontier arm |

**Viz:** small multiples, shared axes, shared colour map.
**Point:** the gradient is visible in stromal and epithelial and absent in
endothelial and immune, and it reproduces at a different information cost.
**No magnitude appears anywhere**, which is the ruling.

**Options**

1. 2 × 4, both arms, no reference panel.
2. 1 + 4 + 4 as above, reference included.
3. Drop endothelial, per the earlier animation ruling, giving 2 × 3.

**Recommend 2.** The reference panel is what lets a reader judge whether the
per-family panels are showing a gradient or showing cell-type structure.

**Existing:** `figures/scripts/movie_cycle_by_celltype.py` renders these
facets as animation frames. Compositing stills is a small job.

---

# Figure 5 — what each component is load-bearing for

This is the ablation figure, and the thing I failed to explain. The question
it answers: **remove one piece at a time, and what breaks?** Five single-key
changes against the full model, scored on the same five axes.

| panel | data | viz | point |
|---|---|---|---|
| a | 5 changes × 5 axes = 25 values, as **change from the full model** | grouped bars, zero line | which component carries which axis. Removing the phase head costs 0.25 of phase and nothing of cell family |
| b | 2 arms × 2 splits × ~10 epochs of NB loss | line plot, training dashed, held-out solid, selected checkpoints marked | D2. Without the phase head the held-out split is paid for the training split from epoch 1 |
| c | the 5 changes placed in **Figure 2a's plane** | scatter over the frontier curves | D3. Which changes travel the frontier and which leave it. `−ECS` lands on the curve; `−phase head` leaves both |
| d | 28 trained arms, one correlation each | histogram against zero | B2. A defeated adversary is not evidence of a study-free latent |

**Options for a:** (i) grouped bars of deltas; (ii) a 5×5 heatmap of deltas;
(iii) absolute values with the full model as a reference line.
**Recommend (i)**, but **split into two panels** — three axes where higher is
better, two where lower is — because one y-axis for both directions means a
negative bar changes meaning between groups.

**Options for d:** (i) histogram; (ii) a dot per arm on a number line, which
shows 28 arms as 28 marks rather than as bins.
**Recommend (ii).** 28 is few enough to show individually, and a histogram of
28 is mostly empty.

---

# Where C4 and C5 go

AW, 4 November: "C4 and C5 are observations about the latent space. They are
not cherry-picked per-study observations."

Accepted. They are a property of the embedding, not a per-study metric dug
out to find fault. They belong with the other latent observations, which
means **Figure 3**, as two crops of panel f: the disease colouring restricted
to marecko\_2024 and to duempelmann\_2026, side by side.

That makes Figure 3 eleven panels. The alternative is a tenth and eleventh
panel in the grid, or moving them to Figure 4.

**Open for AW.**

---

# What this leaves

| figure | status |
|---|---|
| 1 | fixed. Known defects: whitespace between rows 1 and 2, clipped `similarity` and `reconstruction` boxes, spider `cell type` label, and the spider panel itself undecided |
| 2 | spec above. Panel c blocked on the three CPU mixing jobs |
| 3 | spec above. All nine crops exist |
| 4 | spec above. Frames exist |
| 5 | spec above. All data settled |
| 6 | **unused.** One display item spare |

**AW's note that Figure 2 weakens Figure 1's panels is right** and is not
addressed here: Figure 1 carries the frontier at b and c, and Figure 2 is now
the frontier figure. Figure 1's b and c may become something else, or Figure
2's panel b may be the only frontier in the paper. Deferred, as agreed.
