"""Figure 4 — the cycle, and the cell families it separates.

    /Users/atharvawaghmare/miniconda3/envs/elaj/bin/python figures/scripts/figure4.py

C2 was ruled out of the Results prose entirely, so this figure IS the
finding: whether the menstrual-cycle gradient is present in a cell family or
absent from it, read off the embedding rather than off a ratio.

Each row is one frontier arm. Column 1 is every labelled cell, as the
reference a reader needs to judge whether a per-family panel is showing a
cycle gradient or just showing cell-type structure. Columns 2 to 5 are the
same embedding restricted to one family at a time, same colours, same axes.

No magnitudes anywhere. That is the ruling and it is also the honest form:
the claim is which families separate, not by how much.
"""
from __future__ import annotations
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT = Path("/Users/atharvawaghmare/Endo research/ELAJ")
OUT = Path(__file__).resolve().parents[1] / "draft"
MM = 1 / 25.4
INK, SOFT, GHOST = "#1a1a1a", "#6b6b6b", "#ededed"
ARMS = [("p1_dab168_kl1", "ELAJ$_{B\\,hi}$"), ("p1_dab168_kl30", "ELAJ$_{B\\,lo}$")]
FAMS = ["stromal", "epithelial", "endothelial", "immune"]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 6.5,
                     "text.color": INK})

meta = pd.read_csv(ROOT / "Outputs/cells/p1_dab168_kl1/metadata.csv.gz",
                   low_memory=False)
idx = np.sort(np.random.default_rng(24).choice(len(meta), 400_000, replace=False))
m = meta.iloc[idx].reset_index(drop=True)

# THE COLUMN HAS NINE FINE LEVELS, NOT THREE. proliferative_early,
# secretory_mid and the rest are separate values, so matching the three
# coarse names drops most of the labelled cells and makes secretory almost
# vanish. Collapse by prefix into the four cycle stages, in cycle order,
# because the point is a gradient and alphabetical order scrambles it.
PH = ["menstrual", "proliferative", "periovulatory", "secretory"]
COL = dict(zip(PH, ["#8d7fb5", "#4c78a8", "#e0a458", "#c25b56"]))

def coarse(v):
    v = str(v)
    for stage in PH:
        if v.startswith(stage):
            return stage
    return "other"

phase = m["menstrual phase"].map(coarse)
print("phase levels kept:",
      {k: int(v) for k, v in phase.value_counts().items()})

fig, axes = plt.subplots(len(ARMS), len(FAMS) + 1,
                         figsize=(180 * MM, 86 * MM))
plt.subplots_adjust(left=.055, right=.995, top=.90, bottom=.015,
                    hspace=.10, wspace=.03)

for r, (arm, armlab) in enumerate(ARMS):
    xy = np.load(ROOT / f"Outputs/analysis/umaps/{arm}/_umap_cache/global_400000.npy")
    for c, fam in enumerate(["all labelled cells"] + FAMS):
        ax = axes[r, c]
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values(): s.set_visible(False)
        ax.scatter(xy[:, 0], xy[:, 1], s=.4, c=GHOST, lw=0, rasterized=True,
                   zorder=1)
        sel = (phase.isin(PH)).to_numpy()
        if c > 0:
            sel &= (m["cell family"] == fam).to_numpy()
        for p in PH:
            k = sel & (phase == p).to_numpy()
            ax.scatter(xy[k, 0], xy[k, 1], s=.5, c=COL[p], lw=0,
                       rasterized=True, zorder=2)
        if r == 0:
            ax.set_title(fam, fontsize=6.6, pad=3)
        if c == 0:
            ax.text(-.04, .5, armlab, transform=ax.transAxes, fontsize=7.4,
                    rotation=90, va="center", ha="right")
        ax.text(.02, .97, f"{chr(97 + r * (len(FAMS) + 1) + c)}",
                transform=ax.transAxes, fontsize=8, fontweight="bold",
                va="top", ha="left")

fig.legend(handles=[Line2D([], [], lw=0, marker="o", ms=4, color=COL[p],
                           label=p) for p in PH]
                   + [Line2D([], [], lw=0, marker="o", ms=4, color=GHOST,
                             label="unlabelled or other phase")],
           ncol=4, fontsize=6.0, frameon=False, loc="upper left",
           bbox_to_anchor=(.055, .995), columnspacing=1.4, handletextpad=.4)
fig.savefig(OUT / "figure4.png", dpi=200)
print(f"wrote figure4.png — {len(ARMS)} arms x {len(FAMS) + 1} panels")
