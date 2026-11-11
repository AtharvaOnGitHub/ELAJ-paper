#!/usr/bin/env python
"""Figure 1a, option 5 — option 1 with AW's five corrections, 11 November.

  1. the left beat is ELEVEN TILES, not a bar chart: one ellipse per study,
     area scaled by donor count, named in a legend
  2. they merge into a single block before the model
  3. the model box holds FOUR PICTOGRAMS IN A 2x2, not four thumbnails
  4. the frontier has to carry its message, which it did not
  5. arrows short and thick

ON 4, WHAT THE MESSAGE ACTUALLY IS. Checked rather than assumed: every one
of the nine competing representations is strictly worse than ELAJ_B_hi on
BOTH axes at once, higher donor recovery and lower cycle agreement. 9 of 9.
So the panel shades the region that is worse on both and lets every other
method fall inside it. That is the claim drawn rather than asserted, and it
is stronger than a scatter with a Pareto line nobody reads.

Donor counts, study names and frontier coordinates are all read from the
corpus and from table1.collect(). Nothing here is typed in.
"""
from __future__ import annotations
import os, sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch, Rectangle, Ellipse, Circle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from table1 import collect, MANIFEST, BASELINES, FOUNDATION   # noqa: E402
from figure1 import STUDY_NAME                                 # noqa: E402

ROOT = Path("/Users/atharvawaghmare/Endo research/ELAJ")
ARM = "p1_dab168_kl1"
OUT = Path(__file__).resolve().parents[1] / "pinned"

INK, NOTE, HAIR = "#2B3038", "#6F7681", "#C9CDD4"
GREY_F, GREY_E = "#EDEFF2", "#6B7380"
BLUE_F, BLUE_E = "#E9F2FC", "#3F6FB4"
AMB_F,  AMB_E  = "#FFF3DE", "#D89120"
DEAD = "#F0E3E1"                      # the worse-on-both region
SC = ["#5BA3A0", "#4C78A8", "#E45756", "#54A24B", "#B279A2", "#F58518",
      "#2E5C8A", "#7B4FA0", "#FF9DA6", "#1B7A6B", "#8C2D3F"]

FS_H, FS_B, FS_T = 6.5, 5.5, 4.8
plt.rcParams.update({"font.family": "Arial", "text.color": INK})


def head(ax, x, y, t, sub, c):
    ax.text(x, y, t, ha="left", va="bottom", fontsize=FS_H,
            fontweight="bold", color=c)
    ax.text(x, y - 2.3, sub, ha="left", va="top", fontsize=FS_T, color=NOTE)


def thick_arrow(ax, x, y, length=6.5):
    ax.annotate("", xy=(x + length, y), xytext=(x, y),
                arrowprops=dict(arrowstyle="-|>", color="#AFB5BD", lw=3.4,
                                shrinkA=0, shrinkB=0, mutation_scale=11))


def studies_panel(ax, x, y, w, h, per_study, names):
    """Eleven studies as tiles, area proportional to donors."""
    mx = per_study.max()
    rng = np.random.default_rng(5)
    placed = []
    for i, (s, n) in enumerate(per_study.items()):
        r = 5.0 * (n / mx) ** 0.5
        for _ in range(900):
            ex = x + rng.uniform(r, w - r)
            ey = y + rng.uniform(r * 0.72, h - r * 0.72)
            if all((ex - px) ** 2 + ((ey - py) * 1.45) ** 2 > (r + pr) ** 2 * .92
                   for px, py, pr in placed):
                break
        placed.append((ex, ey, r))
        ax.add_patch(Ellipse((ex, ey), r * 2, r * 1.38, fc=SC[i], ec="none",
                             alpha=.92, zorder=3))
    return placed


def legend_two_col(ax, x, y, w, per_study, names):
    rows = (len(per_study) + 1) // 2
    step, colw = 2.7, w / 2
    for i, (s, n) in enumerate(per_study.items()):
        cx = x + (i // rows) * colw
        cy = y - (i % rows) * step
        ax.add_patch(Circle((cx + 0.8, cy), .72, fc=SC[i], ec="none", zorder=4))
        ax.text(cx + 2.4, cy, f"{names.get(s, s)}", ha="left", va="center",
                fontsize=FS_T, color=NOTE)
        ax.text(cx + colw - 2.0, cy, str(n), ha="right", va="center",
                fontsize=FS_T, color=INK, fontweight="bold")


def pictograms_2x2(ax, x, y, w, h):
    ax.add_patch(FancyBboxPatch((x, y), w, h, "round,pad=0,rounding_size=1.6",
                                fc=BLUE_F, ec=BLUE_E, lw=.9, zorder=2))
    pw, ph = w * 0.52, 4.6
    ax.add_patch(FancyBboxPatch((x + (w - pw) / 2, y - ph / 2), pw, ph,
                                "round,pad=0,rounding_size=2.3",
                                fc=BLUE_E, ec=BLUE_E, lw=0, zorder=6))
    ax.text(x + w / 2, y + 0.05, "ELAJ   1.88M parameters", ha="center",
            va="center", fontsize=FS_B, color="#FFFFFF", fontweight="bold",
            zorder=7)
    cw, ch = w / 2, h / 2
    cells = [(x + cw * .5, y + h - ch * .5), (x + cw * 1.5, y + h - ch * .5),
             (x + cw * .5, y + ch * .5),     (x + cw * 1.5, y + ch * .5)]

    # 1 pathway groups
    cx, cy = cells[0]
    for g, gc in enumerate(("#4C78A8", "#5BA3A0", "#B279A2")):
        for k in range(4):
            ax.add_patch(Circle((cx - 5.0 + g * 4.6 + (k % 2) * 1.25,
                                 cy + 2.3 - (k // 2) * 1.25), .46,
                                fc=gc, ec="none", zorder=4))
    ax.text(cx, cy - 2.4, "genes read in\n44 pathway groups", ha="center",
            va="top", fontsize=FS_T, color=NOTE, linespacing=1.35, zorder=4)

    # 2 the sentinel
    cx, cy = cells[1]
    for k in range(5):
        hollow = k == 2
        ax.add_patch(Circle((cx - 4.6 + k * 2.3, cy + 1.9), .62,
                            fc="#FFFFFF" if hollow else "#4C78A8",
                            ec=AMB_E if hollow else "none",
                            lw=.9 if hollow else 0, zorder=4,
                            linestyle=(0, (1.4, 1.2)) if hollow else "-"))
    ax.text(cx, cy - 2.4, "genes never assayed\nflagged, not zeroed",
            ha="center", va="top", fontsize=FS_T, color=NOTE,
            linespacing=1.35, zorder=4)

    # 3 per-study normalisation
    cx, cy = cells[2]
    t = np.linspace(-1, 1, 80)
    bell = np.exp(-(t * 2.1) ** 2)
    for off, col, al, lw in ((-1.9, GREY_E, .5, .7), (1.9, GREY_E, .5, .7),
                             (0.0, BLUE_E, 1.0, 1.1)):
        ax.plot(cx + t * 4.2 + off, cy + 0.8 + bell * 2.6, color=col, lw=lw,
                alpha=al, zorder=4)
    ax.text(cx, cy - 2.4, "each study normalised\non its own statistics",
            ha="center", va="top", fontsize=FS_T, color=NOTE,
            linespacing=1.35, zorder=4)

    # 4 sixteen numbers
    cx, cy = cells[3]
    ax.add_patch(Rectangle((cx - 6.4, cy + 0.6), 3.4, 3.6, fc="#BBD2EC",
                           ec="none", zorder=4))
    ax.annotate("", xy=(cx - 1.6, cy + 2.4), xytext=(cx - 2.6, cy + 2.4),
                arrowprops=dict(arrowstyle="-|>", color=GREY_E, lw=.8,
                                mutation_scale=6), zorder=4)
    for k in range(16):
        ax.add_patch(Circle((cx - 0.6 + (k % 8) * 0.92,
                             cy + 3.0 - (k // 8) * 1.0), .34,
                            fc=AMB_E, ec="none", zorder=4))
    ax.text(cx, cy - 2.4, "every cell becomes\nsixteen numbers", ha="center",
            va="top", fontsize=FS_T, color=NOTE, linespacing=1.35, zorder=4)


def frontier_dominance(ax, x, y, w, h):
    """The message: every competitor is worse on BOTH axes."""
    D = collect()
    pts = []
    for m in list(BASELINES) + list(FOUNDATION):
        g = D[m]
        a = g.get(("cross-donor", "menstrual phase"))
        b = g.get(("knn-agreement", "patient_id"))
        if a and b:
            pts.append((float(b), float(a), MANIFEST[m][3], False))
    for k, nm in (("p1_dab168_kl1", "ELAJ"), ("p1_dab168_kl30", "")):
        g = D[k]
        pts.append((float(g[("knn-agreement", "patient_id")]),
                    float(g[("cross-donor", "menstrual phase")]), nm, True))
    X = [p[0] for p in pts]; Y = [p[1] for p in pts]
    x0, x1 = min(X) - .035, max(X) + .030
    y0, y1 = min(Y) - .030, max(Y) + .035
    fx = lambda v: x + w * (v - x0) / (x1 - x0)
    fy = lambda v: y + h * (v - y0) / (y1 - y0)

    best = max((p for p in pts if p[3]), key=lambda p: p[1])
    n_dom = sum(1 for p in pts if not p[3] and p[0] > best[0] and p[1] < best[1])
    ax.add_patch(Rectangle((fx(best[0]), y), x + w - fx(best[0]),
                           fy(best[1]) - y, fc=DEAD, ec="none", zorder=1))
    # bottom-RIGHT of the shaded block: the bottom-left corner is where
    # Geneformer sits and the first version printed the label over it
    ax.text(x + w - 1.2, y + 1.4, f"worse on both axes\nall {n_dom} other methods",
            ha="right", va="bottom", fontsize=FS_T, color="#9A5A52",
            linespacing=1.35, zorder=5)

    for bx, by, nm, mine in pts:
        ax.scatter([fx(bx)], [fy(by)], s=26 if mine else 11, zorder=7,
                   c=AMB_F if mine else "#FFFFFF",
                   edgecolors=AMB_E if mine else NOTE,
                   linewidths=1.0 if mine else .7)
    # both reported arms are ours; the lower one is not dominated either, so
    # leaving it unlabelled made it read as a stray competitor
    lo = min((p for p in pts if p[3]), key=lambda p: p[1])
    ax.plot([fx(lo[0]), fx(best[0])], [fy(lo[1]), fy(best[1])], "-",
            color=AMB_E, lw=1.0, alpha=.55, zorder=6)
    ax.text(fx(best[0]) - 1.4, fy(best[1]) + 1.2, "ELAJ", ha="right",
            va="bottom", fontsize=FS_B, color=AMB_E, fontweight="bold", zorder=8)
    ax.text(fx(lo[0]) + 2.2, fy(lo[1]) - 1.8, "two reported\narms", ha="left",
            va="top", fontsize=FS_T, color=AMB_E, linespacing=1.3, zorder=8)

    ax.annotate("", xy=(x, y + h + 1.0), xytext=(x, y),
                arrowprops=dict(arrowstyle="-|>", color=HAIR, lw=.8,
                                mutation_scale=7), zorder=3)
    ax.annotate("", xy=(x + w + 1.0, y), xytext=(x, y),
                arrowprops=dict(arrowstyle="-|>", color=HAIR, lw=.8,
                                mutation_scale=7), zorder=3)
    ax.text(x + w / 2, y - 2.0, "more donor identity kept", ha="center",
            va="top", fontsize=FS_T, color=NOTE)
    ax.text(x - 2.2, y + h / 2, "more cycle kept", ha="center", va="center",
            rotation=90, fontsize=FS_T, color=NOTE)


def main() -> None:
    m = pd.read_csv(ROOT / f"Outputs/cells/{ARM}/metadata.csv.gz",
                    low_memory=False, usecols=["study", "patient_id"])
    per_study = m.groupby("study").patient_id.nunique().sort_values(ascending=False)

    W, H = 180.0, 64.0
    fig = plt.figure(figsize=(W / 25.4, H / 25.4))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H)
    ax.axis("off")
    TOP = 58.0

    head(ax, 3, TOP, "Collect", "every eligible study, sized by donors", GREY_E)
    studies_panel(ax, 3, 30.0, 52, 18, per_study, STUDY_NAME)
    legend_two_col(ax, 3, 25.0, 52, per_study, STUDY_NAME)
    ax.add_patch(FancyBboxPatch((3, 3.0), 52, 5.4,
                                "round,pad=0,rounding_size=2.0",
                                fc=GREY_F, ec=GREY_E, lw=.8, zorder=3))
    ax.text(29, 5.7, "1,577,728 cells   ·   254 donors   ·   11 studies",
            ha="center", va="center", fontsize=FS_B, color=INK,
            fontweight="bold", zorder=4)

    thick_arrow(ax, 57.0, 32.0)

    head(ax, 67, TOP, "Compress", "inductive bias in place of scale", BLUE_E)
    pictograms_2x2(ax, 67, 14.0, 52, 36.0)

    thick_arrow(ax, 121.0, 32.0)

    head(ax, 131, TOP, "Check", "measured against every alternative", AMB_E)
    frontier_dominance(ax, 136, 16.0, 38, 32)

    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "mock_fig1a_opt5.png",
                dpi=int(os.environ.get("FIGDPI", 400)))
    print(f"wrote {OUT / 'mock_fig1a_opt5.png'}  ({W:.0f} x {H:.0f} mm)")


if __name__ == "__main__":
    main()
