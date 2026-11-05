"""Figure 4 — this is what endometriosis looks like, in nine UMAPs.

    /Users/atharvawaghmare/miniconda3/envs/elaj/bin/python figures/scripts/figure4.py

ONE embedding, nine colourings. Nothing moves between panels except colour,
which is what makes a grid of UMAPs legible: a reader compares structure, not
layout. They see in one pass which labels organise the latent and which do
not, and that is the whole "what does the latent hold" question at once.

Neutral grid, alphabetical. Grouping the panels into "labels that structure
it" and "labels that do not" would read better and would state the conclusion
through layout, which is the thing a figure must not do.

REPRODUCIBILITY. The subsample is default_rng(24).choice(n, 400_000) then
sorted, and the cache is keyed on sample size alone, so changing the seed or
the count silently invalidates it.
SUBMISSION RESOLUTION. 200 dpi is for reading on screen while the
design is settled. For the manuscript set FIGDPI=600 or higher:
AW does not want blurred or messy images, and a rasterised scatter
of 400,000 points at 200 dpi will not survive print.
"""
from __future__ import annotations
import os
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT = Path("/Users/atharvawaghmare/Endo research/ELAJ")
ARM = "p1_dab168_kl1"
OUT = Path(__file__).resolve().parents[1] / "pinned"
MM = 1 / 25.4
INK, SOFT = "#1a1a1a", "#6b6b6b"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 6.5,
                     "text.color": INK})

xy = np.load(ROOT / f"Outputs/analysis/umaps/{ARM}/_umap_cache/global_400000.npy")
meta = pd.read_csv(ROOT / f"Outputs/cells/{ARM}/metadata.csv.gz", low_memory=False)
idx = np.sort(np.random.default_rng(24).choice(len(meta), 400_000, replace=False))
m = meta.iloc[idx].reset_index(drop=True)
assert len(m) == len(xy), f"{len(m)} rows against {len(xy)} points"

CAT = plt.get_cmap("tab10").colors

# PHASE IS GROUPED AS THE ANIMATION GROUPED IT. Nine harmonised levels
# collapse to five in cycle order, with the animation's own palette, so the
# two tell the same story in the same colours.
COARSE = {"menstrual": "menstrual",
          "proliferative_early": "proliferative", "proliferative": "proliferative",
          "proliferative_late": "proliferative", "periovulatory": "periovulatory",
          "secretory_early": "secretory early", "secretory_early_mid": "secretory early",
          "secretory_mid": "secretory late", "secretory_late": "secretory late"}
PHASE_ORDER = ["menstrual", "proliferative", "periovulatory",
               "secretory early", "secretory late"]
PHASE_COL = ["#8C2F39", "#D9A441", "#3A7D5D", "#2F6690", "#6D2E46"]
m["phase group"] = m["menstrual phase"].map(COARSE)

# ONE RANDOM Z-ORDER, SHARED BY EVERY PANEL. Drawing one class at a time
# puts the last class on top of all the others: disease status is 42%
# eutopic, not 100%, and it only looked that way because `eutopic` sorts
# last and painted over control, ectopic and adenomyosis. Interleaving the
# points removes the artefact without touching the data.
SHUF = np.random.default_rng(1).permutation(len(m))

# Raw obs values where they are not self-explaining. Endometriosis_stage is
# stored as a float, so the panel legend read "0.0 1.0 2.0 3.0 4.0"; it is the
# revised ASRM scale and 0 is marecko's coding for its controls, established
# by arithmetic in validate_latent's _union_severity.
LABEL = {"Endometriosis_stage": {"0.0": "control", "1.0": "rASRM I",
                                 "2.0": "rASRM II", "3.0": "rASRM III",
                                 "4.0": "rASRM IV"}}

PANELS = [
    ("cell family", "cell family", "cat", None),
    ("study", "study", "cat", None),
    ("tissue", "tissue", "cat", None),
    ("menstrual phase", "phase group", "cat", (PHASE_ORDER, PHASE_COL)),
    ("cycle day", "CycleDay", "seq", None),
    ("serum progesterone", "ProgesteroneSerum", "seq", None),
    ("disease status", "disease_status", "cat", None),
    ("surgical stage", "Endometriosis_stage", "cat", None),
    ("grade", "EndometriosisGrade", "cat", None),
]

fig, axes = plt.subplots(3, 3, figsize=(180 * MM, 168 * MM))
# right=.955, not .988: the third column carries a colourbar and at .988 its
# tick labels ran off the canvas.
plt.subplots_adjust(left=.012, right=.955, top=.962, bottom=.012,
                    hspace=.20, wspace=.03)

for ax, (title, col, kind, override) in zip(axes.ravel(), PANELS):
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    v = m[col]
    ok = v.notna().to_numpy()
    ax.scatter(xy[~ok, 0], xy[~ok, 1], s=.5, c="#ededed", lw=0, alpha=.55,
               rasterized=True, zorder=1)
    if kind == "cat":
        levels, cols = (override if override else
                        (sorted(v.dropna().unique(), key=str),
                         [CAT[i % 10] for i in range(v.nunique())]))
        lut = {lv: cols[i] for i, lv in enumerate(levels)}
        keep = SHUF[ok[SHUF]]                       # shuffled, labelled only
        rgb = np.array([lut.get(z, (1, 1, 1)) for z in v.to_numpy()[keep]])
        ax.scatter(xy[keep, 0], xy[keep, 1], s=.5, c=rgb, lw=0, alpha=.40,
                   rasterized=True, zorder=2)
        # NOT TRUNCATED. `[:18]` printed garcia_alonso_2021_a and _b as two
        # identical legend entries in different colours, which reads as a
        # rendering bug and hides the one fact the reader needs about them:
        # they are the same fifteen people under thirty identifiers.
        handles = [Line2D([], [], lw=0, marker="o", ms=3, color=lut[lv],
                          label=LABEL.get(col, {}).get(str(lv), str(lv)))
                   for lv in levels]
        ncol = 2 if len(levels) > 5 else 1
        ax.legend(handles=handles, fontsize=4.0, frameon=False, ncol=ncol,
                  loc="lower left", handletextpad=.3, columnspacing=.6,
                  borderpad=.1, labelspacing=.25)
    else:
        # viridis for both continuous panels, perceptually uniform and the
        # same scale shape, so cycle day and progesterone are comparable by
        # eye rather than by a colour-map difference.
        x = pd.to_numeric(v, errors="coerce").to_numpy()
        keep = SHUF[ok[SHUF]]
        sc = ax.scatter(xy[keep, 0], xy[keep, 1], s=.5, c=x[keep],
                        cmap="viridis", lw=0, alpha=.45, rasterized=True,
                        zorder=2)
        cb = fig.colorbar(sc, ax=ax, fraction=.035, pad=.01)
        cb.ax.tick_params(labelsize=4.2, length=1.5, color=SOFT)
        cb.outline.set_visible(False)
    n = int(ok.sum())
    ax.set_title(f"{title}   ({100*n/len(m):.0f}% of cells labelled)",
                 fontsize=6.4, pad=3, color=INK)

for ax, letter in zip(axes.ravel(), "abcdefghi"):
    ax.text(.012, .985, letter, transform=ax.transAxes, fontsize=9,
            fontweight="bold", va="top", ha="left")

fig.savefig(OUT / "figure4.png", dpi=int(os.environ.get("FIGDPI", 200)))
print(f"wrote figure4.png — 9 panels, {len(m):,} cells each")
