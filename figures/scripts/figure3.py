"""Figure 3 — the latent, read by every label we have.

    /Users/atharvawaghmare/miniconda3/envs/elaj/bin/python figures/scripts/figure3.py

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
"""
from __future__ import annotations
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT = Path("/Users/atharvawaghmare/Endo research/ELAJ")
ARM = "p1_dab168_kl1"
OUT = Path(__file__).resolve().parents[1] / "draft"
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
PANELS = [
    ("cell family", "cell family", "cat"),
    ("study", "study", "cat"),
    ("tissue", "tissue", "cat"),
    ("menstrual phase", "menstrual phase", "cat"),
    ("cycle day", "CycleDay", "cyc"),
    ("serum progesterone", "ProgesteroneSerum", "seq"),
    ("disease status", "disease_status", "cat"),
    ("surgical stage", "Endometriosis_stage", "cat"),
    ("grade", "EndometriosisGrade", "cat"),
]

fig, axes = plt.subplots(3, 3, figsize=(180 * MM, 168 * MM))
plt.subplots_adjust(left=.012, right=.988, top=.962, bottom=.012,
                    hspace=.20, wspace=.03)

for ax, (title, col, kind) in zip(axes.ravel(), PANELS):
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    v = m[col]
    ok = v.notna().to_numpy()
    # unlabelled cells stay, in near-white, so every panel shows the same mass
    ax.scatter(xy[~ok, 0], xy[~ok, 1], s=.6, c="#ededed", lw=0,
               rasterized=True, zorder=1)
    if kind == "cat":
        levels = sorted(v.dropna().unique(), key=str)
        for i, lv in enumerate(levels):
            k = (v == lv).to_numpy()
            ax.scatter(xy[k, 0], xy[k, 1], s=.6, c=[CAT[i % 10]], lw=0,
                       rasterized=True, zorder=2)
        handles = [Line2D([], [], lw=0, marker="o", ms=3, color=CAT[i % 10],
                          label=str(lv)[:18]) for i, lv in enumerate(levels)]
        ncol = 2 if len(levels) > 5 else 1
        ax.legend(handles=handles, fontsize=4.0, frameon=False, ncol=ncol,
                  loc="lower left", handletextpad=.3, columnspacing=.6,
                  borderpad=.1, labelspacing=.25)
    else:
        x = pd.to_numeric(v, errors="coerce").to_numpy()
        cmap = "twilight" if kind == "cyc" else "viridis"
        sc = ax.scatter(xy[ok, 0], xy[ok, 1], s=.6, c=x[ok], cmap=cmap, lw=0,
                        rasterized=True, zorder=2)
        cb = fig.colorbar(sc, ax=ax, fraction=.035, pad=.01)
        cb.ax.tick_params(labelsize=4.2, length=1.5, color=SOFT)
        cb.outline.set_visible(False)
    n = int(ok.sum())
    ax.set_title(f"{title}   ({100*n/len(m):.0f}% of cells labelled)",
                 fontsize=6.4, pad=3, color=INK)

for ax, letter in zip(axes.ravel(), "abcdefghi"):
    ax.text(.012, .985, letter, transform=ax.transAxes, fontsize=9,
            fontweight="bold", va="top", ha="left")

fig.savefig(OUT / "figure3.png", dpi=200)
print(f"wrote figure3.png — 9 panels, {len(m):,} cells each")
