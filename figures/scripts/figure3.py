"""Figure 3 — the two models' latents, by cell family and cycle phase.

    /Users/atharvawaghmare/miniconda3/envs/elaj/bin/python figures/scripts/figure3.py

THIRD IN THE PAPER, AND BEFORE THE NINE-UMAP FIGURE, because this is where a
reader meets both latents side by side and can judge for themselves that
ELAJ_B_hi separates the space more sharply than ELAJ_B_lo. Only then does the
corpus-wide read make sense.

C2 was ruled out of the Results prose entirely, so this figure IS the
finding: whether the menstrual-cycle gradient is present in a cell family or
absent from it, read off the embedding rather than off a ratio.

Each row is one frontier arm. Column 1 is every labelled cell, as the
reference a reader needs to judge whether a per-family panel is showing a
cycle gradient or just showing cell-type structure. Columns 2 to 5 are the
same embedding restricted to one family at a time, same colours, same axes.

No magnitudes anywhere. That is the ruling and it is also the honest form:
the claim is which families separate, not by how much.
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
OUT = Path(__file__).resolve().parents[1] / "pinned"
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
# The animation's own five groups and palette, in cycle order. `menstrual`
# is 162 cells of 400,000 and is folded into proliferative rather than drawn
# as a level nobody can see.
# MENSTRUATION IS EXCLUDED, NOT FOLDED IN. groupings.py: "menstrual is
# dropped rather than folded into proliferative. Menstruation is a
# distinct physiological state, not a point on the proliferative-to-
# secretory axis, and it carries under 4,199 cells." This panel folded
# it into proliferative, which is the one thing that note rules out.
# Figure 4 still shows it as its own level, because that figure is a
# description of what the corpus holds rather than a reading of the axis.
COARSE = {"menstrual": None,
          "proliferative_early": "proliferative", "proliferative": "proliferative",
          "proliferative_late": "proliferative", "periovulatory": "periovulatory",
          "secretory_early": "secretory early", "secretory_early_mid": "secretory early",
          "secretory_mid": "secretory late", "secretory_late": "secretory late"}
PH = ["proliferative", "periovulatory", "secretory early", "secretory late"]
COL = dict(zip(PH, ["#D9A441", "#3A7D5D", "#2F6690", "#6D2E46"]))
phase = m["menstrual phase"].map(COARSE)
SHUF = np.random.default_rng(1).permutation(len(m))
print("phase levels kept:",
      {k: int(v) for k, v in phase.value_counts().items()})

fig, axes = plt.subplots(len(ARMS), len(FAMS) + 1,
                         figsize=(180 * MM, 86 * MM))
# top .875 -> .925 and bottom .015 -> .085: the legend moved out from above
# the column titles to a single centred line under both rows, which frees the
# space it used to share with them.
plt.subplots_adjust(left=.055, right=.995, top=.925, bottom=.085,
                    hspace=.10, wspace=.03)

for r, (arm, armlab) in enumerate(ARMS):
    xy = np.load(ROOT / f"Outputs/analysis/umaps/{arm}/_umap_cache/global_400000.npy")
    for c, fam in enumerate(["all labelled cells"] + FAMS):
        ax = axes[r, c]
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values(): s.set_visible(False)
        ax.scatter(xy[:, 0], xy[:, 1], s=.4, c=GHOST, lw=0, alpha=.55,
                   rasterized=True, zorder=1)
        sel = (phase.isin(PH)).to_numpy()
        if c > 0:
            sel &= (m["cell family"] == fam).to_numpy()
        # shuffled z-order, so no phase paints over the one before it
        keep = SHUF[sel[SHUF]]
        rgb = np.array([COL[z] for z in phase.to_numpy()[keep]])
        ax.scatter(xy[keep, 0], xy[keep, 1], s=.5, c=rgb, lw=0, alpha=.45,
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
           ncol=len(PH) + 1, fontsize=6.0, frameon=False, loc="lower center",
           bbox_to_anchor=(.5, -.004), columnspacing=1.6, handletextpad=.4)
fig.savefig(OUT / "figure3.png", dpi=int(os.environ.get("FIGDPI", 200)))
print(f"wrote figure3.png — {len(ARMS)} arms x {len(FAMS) + 1} panels")
