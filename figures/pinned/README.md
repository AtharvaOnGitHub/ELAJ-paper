# Pinned figures

Frozen on AW's instruction, 5 November 2026: "save fig 1 and fig 2 as they
are so far. We would be improving them as we get closer to submission."

These are **not finished**. They are the agreed structure, saved so the
design decisions behind them are not lost and so later work starts from a
known state rather than a re-derivation.

| file | script | what it is |
|---|---|---|
| `figure1.png` | `../scripts/figure1.py` | ELAJ as a model, and the main findings |
| `figure2.png` | `../scripts/figure2.py` | the ELAJ frontier |
| `figure3.png` | `../scripts/figure3.py` | both models' latents, by cell family and cycle phase |
| `figure4.png` | `../scripts/figure4.py` | this is what endometriosis looks like, in nine UMAPs |

Regenerate any of them with
`python figures/scripts/figureN.py`. Set `FIGDPI=600` for submission: 200 is
for reading on screen, and a rasterised scatter of 400,000 points at 200 dpi
will not survive print.

## The order, and why

AW, 5 November:

> 1. ELAJ as a model and main findings
> 2. The ELAJ frontier
> 3. ELAJ models by cell type and menstrual phase
> 4. This is what endometriosis looks like in 9 UMAPs.

Figure 3 comes before Figure 4 because it is where a reader meets both
latents side by side and can judge for themselves that `ELAJ_B_hi` separates
the space more sharply than `ELAJ_B_lo`. The corpus-wide read only makes
sense once they have.

The scripts were renamed to match, so the file number is the paper number
and nobody has to carry a mapping.

Both write here directly. `figure1.py` previously wrote to `/tmp`, where it
would not have survived a reboot.

---

## Figure 1 — the overview

Decided in an earlier session, recovered from the transcripts on 4 November
after an auto-generated table had replaced it with something else. AW's
words:

> "I don't see how the architecture could be split by panels. Instead I would
> give the architecture a long and wide panel a, give frontier panel b, UMAP
> by cell family panel c, UMAP by study as panel d, and UMAP by cycle day as
> panel e."

> "make the frontier 2 panels… draw the pareto front. Then put all three
> UMAPs in the bottom row. Also the architecture panel would be like a
> butterfly with the latent in the middle, pathway groups expanding on one
> side and heads expanding on the other."

**Known defects, carried deliberately:**

1. Whitespace between rows 1 and 2.
2. The `similarity` and `reconstruction` boxes clip.
3. The spider's `cell type` label is wrong.
4. The spider panel itself is undecided. AW: "I don't think we look that bad
   in the chart, we are high or dominant on all axes… I see the argument that
   we are undersold… Let's explore this panel further."
5. **It draws a chance line at 0.370 on a cross-donor axis.** Cross-donor
   values are already excess over chance, so that line double-counts. Same
   error that was corrected in Results and ABLATIONS.md. **Must come out.**
6. Its frontier panels draw two fronts, baselines and ELAJ arms separately.
   AW ruled on 5 November that there is **one** front over every point.
7. Figure 2 now carries the frontier, so panels b and c may be redundant.

## Figure 2 — the ELAJ frontier

2 × 2 scatters. Columns share an x-axis (the costs), rows share a y-axis (the
biology), **both cost axes reversed so better is up and to the right in every
panel**. One Pareto front over all fifteen points: six ELAJ arms and nine
other methods, nobody exempt.

**The two reported arms are named.** `ELAJ_B_hi` keeps more of the menstrual
cycle and gives up a little study removal; `ELAJ_B_lo` gives up cycle signal
and removes study substantially better. B is for biology.

**The disease row was removed**, 5 November. Across the ten methods a
method's control-vs-eutopic score correlates with its donor recovery at
ρ +0.721 (p 0.019) while menstrual phase does not (+0.176, p 0.63). An axis
whose dominant property is that it reads out donor memorisation is not a
performance axis. The correlation stays as an observation about the metric.

**Known defects:**

1. The `study separation` column uses the **old-cap** mixing numbers, 19,998
   of 416,256 cells. The three CPU jobs replace that column.
2. Labels collide in panels c and d, where nine points sit within 0.005 of
   each other on the saturated cell-family axis. No direction is free. Either
   that row gets its own expanded range, or only front points are labelled.
3. `B_lo` reads as a demotion when it is the better model at the harder task.
   The legend should say what the subscript indexes.


---

## Figure 3 — both latents, by cell family and cycle phase

Two rows, one per reported arm. Column 1 is every labelled cell as the
reference a reader needs to tell a cycle gradient from cell-type structure;
columns 2 to 5 restrict to one family at a time.

Phase is collapsed into the animation's own five groups in cycle order, with
the animation's palette, so the figure and the GIF tell one story in one set
of colours. `menstrual` is 162 cells of 400,000 and folds into
`proliferative` rather than being drawn as a level nobody can see.

**No magnitudes anywhere.** C2 was ruled out of the prose, so this figure is
the finding: which families separate, not by how much.

## Figure 4 — nine UMAPs

One embedding, nine colourings, nothing moving between panels but colour.
Neutral 3 × 3 grid: grouping the panels into "labels that structure the
latent" and "labels that do not" would read better and would state the
conclusion through layout.

**Disease status was an artefact and is fixed.** The corpus is 42% eutopic,
35% control, 20% ectopic, 3% adenomyosis. Drawing one class at a time
alphabetically put `eutopic` on top of everything and the panel looked
uniform. Every panel now shares one shuffled z-order, which is what
`phase_groups.py` was already doing.

Cycle day and serum progesterone are both viridis, so they can be compared
by eye rather than through a colour-map difference. They are not the same:
progesterone's bright band is sharply localised where cycle day's gradient
is broad.

**Panels h and i carry the claim.** AW: "We cannot find any reasonable
biological pattern in endometriosis staging across the entire publicly
available scRNA database. Maybe we need a change."

**Study structure is visible in panel b and that is fine.** It is on the
frontier, it is the paper's subject, and a reviewer who asks gets an answer.
No pre-emption.
