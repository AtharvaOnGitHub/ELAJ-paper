#!/usr/bin/env python
"""Figure 1 — ELAJ as a model, and the main findings.

LAYOUT FROM AW'S SKETCH, 7 November 2026.
  a  the architecture, one wide strip across the top
  b  PRISMA, a tall column down the left
  c  frontier: cycle against donor recovery        d  against study separation
  e  UMAP by cell family                           f  UMAP by study

PRISMA COUNTS CORRECTED. The thesis diagram is from the r-series era and
ends at twelve included studies; the corpus has eleven. The split is
derived from Data availability rather than guessed: seven GEO accessions,
one ArrayExpress and two CELLxGENE came through the API branch, and
CNP0006183 (li et al.) through the hand search of CNGBdb. So the API branch
includes ten of twenty-two assessed and the manual branch one of forty. The
old diagram also excluded all forty manual reports while still drawing an
arrow into the included box, which cannot both be true.

THE FRONTIER PANELS READ THE TABLE'S OWN SOURCES. table1.collect() is
imported rather than copied, so a point here and a row there cannot come
from different runs.
"""
from __future__ import annotations
import os, sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch, Polygon, Circle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from table1 import collect, MANIFEST, BASELINES, FOUNDATION   # noqa: E402

ROOT = Path("/Users/atharvawaghmare/Endo research/ELAJ")
ARM = "p1_dab168_kl1"
OUT = Path(__file__).resolve().parents[1] / "pinned"
MM = 1 / 25.4

# ── palette ──────────────────────────────────────────────────────────────
# Confident and warm without reading as pink-coded. The prose is careful
# never to frame donors as women, and the figure should not undo that.
INK, SOFT, HAIR = "#1A1A1A", "#6E6A66", "#C9C3BC"
PAPER = "#FBF9F6"
TEAL,  TEAL_F  = "#2A6F8E", "#DCE9F0"      # the encoder path
AMBER, AMBER_F = "#D98C3E", "#F8E7D2"      # the latent
OLIVE, OLIVE_F = "#5B7F3C", "#E2EBD8"      # PRISMA identification
BRICK, BRICK_F = "#9E4A3A", "#F2DFDA"      # exclusions
PLUM,  PLUM_F  = "#5E4B8B", "#E4DFF0"      # the heads
HEADC = {"DAB": PLUM, "Reconstruction": TEAL, "ECS": OLIVE, "Phase": BRICK}

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 6.2,
                     "text.color": INK, "axes.labelcolor": INK,
                     "xtick.color": SOFT, "ytick.color": SOFT,
                     "axes.edgecolor": HAIR, "axes.linewidth": .5})


def box(ax, x, y, w, h, label, fc=PAPER, ec=INK, fs=6.2, lw=.7, weight=None,
        rounding=.6, tc=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, mu := None or
                                f"round,pad=0,rounding_size={rounding}",
                                fc=fc, ec=ec, lw=lw, zorder=2))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
            fontsize=fs, zorder=3, linespacing=1.25,
            color=tc or INK, fontweight=weight or "normal")


def arrow(ax, x0, y0, x1, y1, c=SOFT, lw=.7, head=True, rad=0.0):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), zorder=1,
                arrowprops=dict(arrowstyle="-|>" if head else "-",
                                color=c, lw=lw, shrinkA=0, shrinkB=0,
                                connectionstyle=f"arc3,rad={rad}",
                                mutation_scale=7))


# ═════════════════════════════════════════════════════════════════════════
# a — the architecture
# ═════════════════════════════════════════════════════════════════════════
def panel_a(ax):
    ax.set_xlim(0, 100); ax.set_ylim(0, 27); ax.axis("off")

    box(ax, 1.5, 4.5, 4.2, 17, "cell", fc=TEAL_F, ec=TEAL, fs=6.6)
    ax.text(3.6, 22.4, "15,496 genes", ha="center", fontsize=6, color=SOFT)

    # the 44 pathway groups, then DSBN, then one transformer per group
    gy = [17.6, 13.4, 5.4]
    for i, (lab, y) in enumerate(zip(["group 1", "group 2", "group 44"], gy)):
        box(ax, 8.0, y, 11.5, 3.3, lab, fc=TEAL_F, ec=TEAL)
        arrow(ax, 5.7, 13.0, 8.0, y + 1.65)
    ax.text(13.7, 10.4, "⋮", ha="center", va="center", fontsize=8, color=TEAL)

    box(ax, 21.5, 4.5, 3.6, 16.4, "DSBN", fc="#FFFFFF", ec=TEAL)
    ax.texts[-1].set_rotation(90)
    for y in gy:
        arrow(ax, 19.5, y + 1.65, 21.5, y + 1.65)

    for lab, y in zip(["group\nattention 1", "group\nattention 2",
                       "group\nattention 44"], gy):
        box(ax, 27.5, y - .3, 13.5, 3.9, lab, fc=TEAL_F, ec=TEAL)
        arrow(ax, 25.1, 13.0, 27.5, y + 1.65)
    ax.text(34.2, 10.4, "⋮", ha="center", va="center", fontsize=8, color=TEAL)

    # aggregation, split in two as the sketch has it
    box(ax, 47.0, 10.6, 8.6, 4.8, "aggregation", fc=TEAL_F, ec=TEAL)
    box(ax, 55.6, 10.6, 8.6, 4.8, "cell\nattention", fc=TEAL_F, ec=TEAL)
    for y in gy:
        arrow(ax, 41.0, y + 1.65, 47.0, 13.0, rad=-0.12 if y > 13 else 0.12)

    # the covariates the DECODER is told, which the encoder never sees
    box(ax, 48.5, 3.4, 15.2, 4.4, "decoder conditioning\nstudy · platform · tissue",
        fc="#FFFFFF", ec=SOFT, fs=5.7, tc=SOFT)
    arrow(ax, 63.7, 5.6, 71.0, 11.4, rad=-.18)

    box(ax, 69.5, 10.6, 9.0, 4.8, "latent", fc=AMBER_F, ec=AMBER,
        fs=6.8, weight="bold")
    arrow(ax, 64.2, 13.0, 69.5, 13.0)

    heads = [("DAB", 20.3), ("Reconstruction", 15.4),
             ("ECS", 10.5), ("Phase", 5.6)]
    for lab, y in heads:
        c = HEADC[lab]
        box(ax, 88.0, y, 11.0, 4.0, lab, fc=PAPER, ec=c, fs=6.2, tc=c)
        arrow(ax, 78.5, 13.0, 88.0, y + 2.0, c=HAIR,
              rad=-.22 if y > 13 else .22)

    # the gradient reversal, drawn as an inverter pointing back at the latent
    tx, ty = 84.6, 22.3
    ax.add_patch(Polygon([(tx + 2.6, ty + 1.5), (tx + 2.6, ty - 1.5),
                          (tx - 1.1, ty)], closed=True, fc="#FFFFFF",
                         ec=PLUM, lw=.8, zorder=4))
    ax.add_patch(Circle((tx - 1.75, ty), .62, fc="#FFFFFF", ec=PLUM,
                        lw=.8, zorder=4))
    arrow(ax, tx + 3.4, ty, tx + 2.6, ty, c=PLUM, head=False)
    arrow(ax, tx - 2.4, ty, 78.3, 15.0, c=PLUM, rad=.28)
    ax.text(tx - 3.0, ty + 2.4, "gradient reversal", ha="right",
            fontsize=5.4, color=PLUM)


# ═════════════════════════════════════════════════════════════════════════
# b — PRISMA, in the PRISMA 2020 grammar
# ═════════════════════════════════════════════════════════════════════════
# The convention carries meaning: an amber bar names the identification
# route, a blue spine names the three stages, the main flow runs straight
# down, and exclusions branch sideways into red. A reader who has seen one
# PRISMA reads this one without the legend.
#
# ONE FLOW RATHER THAN TWO. The thesis diagram runs the API and manual
# routes as parallel columns, which needs four sub-columns and does not fit
# a portrait panel at a legible size. The two are therefore combined, and
# the arithmetic reconciles exactly: 455 + 98 identified, less 98
# duplicates, 42 further deposits and the 58 manual records the APIs had
# already returned, leaves 355 screened; 293 excluded leaves 62 sought and
# assessed; 39 not single cell and 12 for other reasons leaves 11.
STAGE_F, STAGE_E, STAGE_T = "#CFE0EF", "#4E7FA6", "#2C5775"

def panel_b(ax):
    ax.set_xlim(0, 100); ax.set_ylim(0, 150); ax.axis("off")
    MX, MW, EX, EW = 11.0, 44.0, 59.0, 40.0

    box(ax, MX, 142.0, MW + EW + 4.0, 6.2,
        "database APIs and manual search",
        fc=AMBER_F, ec=AMBER, fs=5.8, weight="bold", tc="#8A5520")

    for y0, y1, lab in ((122, 140.0, "Identification"),
                        (54, 120, "Screening"),
                        (14, 33, "Included")):
        box(ax, 1.0, y0, 6.0, y1 - y0, "", fc=STAGE_F, ec=STAGE_E, lw=.6)
        ax.text(4.0, (y0 + y1) / 2, lab, ha="center", va="center",
                rotation=90, fontsize=5.8, color=STAGE_T, fontweight="bold")

    rows = [(124, 14.0, "records identified\ndatabase APIs  455\nCNGBdb  98",
                        "removed before\nscreening\nduplicates  98\n"
                        "further deposits  42\nalready found  58"),
            (101, 11.0, "records screened\nn = 355", "excluded\nn = 293"),
            (79,  11.0, "reports sought\nn = 62", "not retrieved\nn = 0"),
            (55,  13.5, "assessed for eligibility\nn = 62",
                        "excluded\nnot single cell  39\nother reasons  12")]
    for y, h, mt, et in rows:
        box(ax, MX, y, MW, h, mt, fc="#FFFFFF", ec=INK, fs=5.5, lw=.6)
        box(ax, EX, y, EW, h, et, fc=BRICK_F, ec=BRICK, fs=5.0, lw=.6)
        arrow(ax, MX + MW, y + h / 2, EX, y + h / 2, c=BRICK, lw=.6)

    box(ax, MX, 16, MW + 22, 15,
        "11 studies included\n1,577,728 cells\n254 donors · 6 anatomical sites",
        fc=AMBER_F, ec=AMBER, fs=6.0, weight="bold")

    x = MX + MW / 2
    for a, b in ((124, 113), (101, 91), (79, 69.5), (55, 32)):
        arrow(ax, x, a, x, b, c=INK, lw=.6)


# ═════════════════════════════════════════════════════════════════════════
# c, d — the frontier over every method, with the Pareto front
# ═════════════════════════════════════════════════════════════════════════
def frontier(ax, D, cost_test, cost_label, xlabel):
    pts = []
    for m in list(BASELINES) + list(FOUNDATION):
        g = D[m]
        y = g.get(("cross-donor", "menstrual phase"))
        x = g.get((cost_test, cost_label))
        if y and x:
            pts.append((float(x), float(y), MANIFEST[m][3], False))
    for key, nm in (("p1_dab168_kl1", "B$_{hi}$"), ("p1_dab168_kl30", "B$_{lo}$")):
        g = D[key]
        pts.append((float(g[(cost_test, cost_label)]),
                    float(g[("cross-donor", "menstrual phase")]), nm, True))

    # Labels collide where methods cluster, so each one is placed in the
    # first of four offsets that no earlier label has taken.
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    sx = (max(xs) - min(xs)) or 1.0
    sy = (max(ys) - min(ys)) or 1.0
    taken: list[tuple[float, float]] = []
    for x, y, nm, ours in sorted(pts, key=lambda p: -p[1]):
        ax.scatter(x, y, s=26 if ours else 14, zorder=4,
                   c=AMBER if ours else "#FFFFFF",
                   edgecolors=AMBER if ours else SOFT,
                   linewidths=.9 if ours else .6)
        for dx, dy, ha in ((0, 5.5, "center"), (0, -9.0, "center"),
                           (5.5, -1.8, "left"), (-5.5, -1.8, "right")):
            cx, cy = x / sx + dx / 90, y / sy + dy / 90
            if all(abs(cx - tx) > .085 or abs(cy - ty) > .055
                   for tx, ty in taken):
                taken.append((cx, cy)); break
        ax.annotate(nm, (x, y), textcoords="offset points",
                    xytext=(dx, dy), ha=ha, fontsize=5.2,
                    color=INK if ours else SOFT,
                    fontweight="bold" if ours else "normal")

    # Pareto: low cost, high phase. Nothing may beat a front point on both.
    front = sorted(p for p in pts
                   if not any(q[0] <= p[0] and q[1] >= p[1] and q[:2] != p[:2]
                              for q in pts))
    ax.plot([p[0] for p in front], [p[1] for p in front], "-",
            color=AMBER, lw=.9, alpha=.55, zorder=2)
    ax.margins(x=.16, y=.10)
    ax.set_xlabel(xlabel, fontsize=6.0)
    ax.tick_params(length=2, labelsize=5.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


# ═════════════════════════════════════════════════════════════════════════
# e, f — the latent
# ═════════════════════════════════════════════════════════════════════════
def umap(ax, xy, series, order, colours, title):
    ax.scatter(xy[:, 0], xy[:, 1], s=.05, c="#E8E4DF", lw=0, rasterized=True)
    for lev, c in zip(order, colours):
        k = (series == lev).to_numpy()
        if k.any():
            ax.scatter(xy[k, 0], xy[k, 1], s=.05, color=c, lw=0, rasterized=True)
    ax.set_title(title, fontsize=6.0, pad=2.5)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color(HAIR)


def main() -> None:
    D = collect()
    xy = np.load(ROOT / f"Outputs/analysis/umaps/{ARM}/_umap_cache/global_400000.npy")
    meta = pd.read_csv(ROOT / f"Outputs/cells/{ARM}/metadata.csv.gz", low_memory=False)
    idx = np.sort(np.random.default_rng(24).choice(len(meta), 400_000, replace=False))
    m = meta.iloc[idx].reset_index(drop=True)
    assert len(m) == len(xy)

    fig = plt.figure(figsize=(180 * MM, 196 * MM))
    gs = fig.add_gridspec(3, 3, height_ratios=[.78, 1, 1],
                          width_ratios=[1.34, 1, 1],
                          left=.035, right=.985, top=.985, bottom=.045,
                          hspace=.30, wspace=.29)

    ax_a = fig.add_subplot(gs[0, :]); panel_a(ax_a)
    ax_b = fig.add_subplot(gs[1:, 0]); panel_b(ax_b)
    ax_c = fig.add_subplot(gs[1, 1])
    ax_d = fig.add_subplot(gs[1, 2])
    ax_e = fig.add_subplot(gs[2, 1])
    ax_f = fig.add_subplot(gs[2, 2])

    frontier(ax_c, D, "knn-agreement", "patient_id", "donor recovery")
    frontier(ax_d, D, "study-mixing", "all studies", "study separation")
    ax_c.set_ylabel("cross-donor cycle agreement", fontsize=5.9, labelpad=1.5)

    FAM = ["stromal", "epithelial", "endothelial", "immune"]
    umap(ax_e, xy, m["cell family"], FAM, [TEAL, AMBER, OLIVE, BRICK],
         "cell family")
    studies = sorted(m["study"].dropna().unique())
    umap(ax_f, xy, m["study"], studies,
         plt.get_cmap("tab20").colors[:len(studies)], "study")

    for ax, lab in ((ax_a, "a"), (ax_b, "b"), (ax_c, "c"),
                    (ax_d, "d"), (ax_e, "e"), (ax_f, "f")):
        ax.text(-.02, 1.015, lab, transform=ax.transAxes, fontsize=8.5,
                fontweight="bold", va="bottom", ha="right")

    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "figure1.png", dpi=int(os.environ.get("FIGDPI", 200)))
    print(f"wrote {OUT / 'figure1.png'}")


if __name__ == "__main__":
    main()
