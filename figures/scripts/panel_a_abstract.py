#!/usr/bin/env python
"""Candidate Figure 1a — the paper in one image.

AW, 11 November: panel a stops being the architecture and becomes what
scGPT's Figure 1a is, which is the paper's claim stated visually. The
architecture moves to 1b.

THE FIGURE IS THE AGREED ONE-LINE STORY, IN ORDER. Every box in the lower
band is one clause of it and nothing appears that is not in it:

  "In this paper we build a single-cell disease atlas where inductive bias
   replaces pretraining scale, and use that to measure the trade-off between
   removing batch effects and keeping biology on a corpus limited by donors."

  corpus limited by donors -> inductive bias not scale -> measure -> frontier

GRAMMAR BORROWED FROM scGPT FIG. 1a (Nat. Methods 21, 1470-1480), read off
the published PDF rather than remembered:
  * rounded group boxes with a coloured outline and a dark pill tab sitting
    ON the bottom border, naming the stage. That tab is their signature.
  * row labels on the far left, set in the row's own colour.
  * chunky grey arrows between groups, so the eye reads stages not wiring.
  * real content inside the boxes rather than abstractions, which is why
    the last box holds the actual frontier rather than a cartoon of one.

THE UPPER BAND IS THE PROBLEM, and it is deliberately wordy and numberless:
a graphical abstract is read in ten seconds, so the numbers all sit in the
lower band where the evidence is.
"""
from __future__ import annotations
import os, sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from table1 import collect, MANIFEST, BASELINES, FOUNDATION   # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "pinned"

INK, NOTE, HAIR = "#2B3038", "#6F7681", "#C9CDD4"
PROB = "#B4463C"                      # the problem band
GREY_F, GREY_E = "#EDEFF2", "#6B7380"
BLUE_F, BLUE_E = "#E9F2FC", "#3F6FB4"
TEAL_F, TEAL_E = "#DCEFEC", "#2F8F88"
AMB_F,  AMB_E  = "#FFF3DE", "#D89120"

FS_PILL, FS_BODY, FS_PROB, FS_OUT = 6.0, 5.5, 5.5, 6.0
plt.rcParams.update({"font.family": "Arial", "text.color": INK})


def group(ax, x, y, w, h, fc, ec, pill, body):
    ax.add_patch(FancyBboxPatch((x, y), w, h, "round,pad=0,rounding_size=1.6",
                                fc=fc, ec=ec, lw=.9, zorder=2))
    ax.text(x + w / 2, y + h - 2.6, body, ha="center", va="top",
            fontsize=FS_BODY, color=INK, zorder=4, linespacing=1.55)
    # the pill sits ON the bottom border, scGPT's device
    pw, ph = w * 0.78, 4.6
    ax.add_patch(FancyBboxPatch((x + (w - pw) / 2, y - ph / 2), pw, ph,
                                "round,pad=0,rounding_size=2.3",
                                fc=ec, ec=ec, lw=0, zorder=5))
    ax.text(x + w / 2, y + 0.05, pill, ha="center", va="center",
            fontsize=FS_PILL, color="#FFFFFF", fontweight="bold", zorder=6)


def arrow(ax, x0, x1, y):
    ax.annotate("", xy=(x1, y), xytext=(x0, y), zorder=1,
                arrowprops=dict(arrowstyle="-|>", color="#B9BEC5", lw=2.4,
                                shrinkA=0, shrinkB=0, mutation_scale=9))


def mini_frontier(ax, x, y, w, h):
    """The real frontier, not a cartoon of one. Same source as Table 1."""
    D = collect()
    pts = []
    for m in list(BASELINES) + list(FOUNDATION):
        g = D[m]
        a = g.get(("cross-donor", "menstrual phase"))
        b = g.get(("knn-agreement", "patient_id"))
        if a and b:
            pts.append((float(b), float(a), False))
    for key in ("p1_dab168_kl1", "p1_dab168_kl30"):
        g = D[key]
        pts.append((float(g[("knn-agreement", "patient_id")]),
                    float(g[("cross-donor", "menstrual phase")]), True))
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    x0, x1 = min(xs), max(xs); y0, y1 = min(ys), max(ys)
    def px(v): return x + w * (0.14 + 0.72 * (v - x0) / (x1 - x0))
    def py(v): return y + h * (0.20 + 0.70 * (v - y0) / (y1 - y0))
    ours = sorted([p for p in pts if p[2]])
    ax.plot([px(p[0]) for p in ours], [py(p[1]) for p in ours], "-",
            color=AMB_E, lw=1.0, alpha=.65, zorder=6)
    for bx, by, mine in pts:
        ax.scatter([px(bx)], [py(by)], s=13 if mine else 7, zorder=7,
                   c=AMB_F if mine else "#FFFFFF",
                   edgecolors=AMB_E if mine else NOTE, linewidths=.7)
    ax.annotate("", xy=(x + w * 0.10, y + h * 0.95), xytext=(x + w * 0.10, y + h * 0.14),
                arrowprops=dict(arrowstyle="-", color=HAIR, lw=.6), zorder=5)
    ax.annotate("", xy=(x + w * 0.95, y + h * 0.14), xytext=(x + w * 0.10, y + h * 0.14),
                arrowprops=dict(arrowstyle="-", color=HAIR, lw=.6), zorder=5)
    ax.text(x + w * 0.52, y + h * 0.02, "donor identity kept", ha="center",
            va="bottom", fontsize=4.8, color=NOTE)
    ax.text(x + w * 0.055, y + h * 0.55, "cycle kept", ha="center", va="center",
            rotation=90, fontsize=4.8, color=NOTE)


def main() -> None:
    W, H = 180.0, 68.0
    fig = plt.figure(figsize=(W / 25.4, H / 25.4))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H)
    ax.axis("off")

    GUT, GAP = 19.0, 5.0
    bw = (W - GUT - 3.0 - 3 * GAP) / 4
    xs = [GUT + i * (bw + GAP) for i in range(4)]
    BY, BH = 13.0, 36.0                      # the solution band
    PY = BY + BH + 4.0                       # the problem band

    ax.text(3.0, PY + 5.0, "Where it\nbreaks", ha="left", va="top",
            fontsize=FS_BODY, color=PROB, fontweight="bold", linespacing=1.4)
    ax.text(3.0, BY + BH - 2.0, "What we\ndid", ha="left", va="top",
            fontsize=FS_BODY, color=INK, fontweight="bold", linespacing=1.4)

    problems = [
        "The record is scattered\nacross four archives",
        "Below pretraining scale.\nPretrained models give\nno advantage here",
        "The batch covariate is\nconfounded with the\nbiology of interest",
        "A single score hides\nwhere on the trade-off\nyou chose to stand",
    ]
    for x, p in zip(xs, problems):
        ax.text(x + bw / 2, PY + 5.2, p, ha="center", va="top",
                fontsize=FS_PROB, color=PROB, linespacing=1.5)

    group(ax, xs[0], BY, bw, BH, GREY_F, GREY_E, "Corpus",
          "Every eligible study,\nassembled once\n\n"
          "11 studies\n1,577,728 cells\n254 donors\n6 anatomical sites")
    group(ax, xs[1], BY, bw, BH, BLUE_F, BLUE_E, "ELAJ",
          "Inductive bias in place\nof pretraining scale\n\n"
          "1.88M parameters\n44 pathway groups\nDNS sentinel\nper-study normalisation")
    group(ax, xs[2], BY, bw, BH, TEAL_F, TEAL_E, "Cross-donor agreement",
          "Count donors, not cells\n\n"
          "same-donor neighbours\ndiscarded\n\n"
          "donor-level\npermutation null")
    group(ax, xs[3], BY, bw, BH, AMB_F, AMB_E, "The frontier",
          "Retrained 11 times,\nso the trade-off is\nmeasured not assumed")
    mini_frontier(ax, xs[3] + bw * 0.06, BY + 2.0, bw * 0.88, BH * 0.52)

    for i in range(3):
        arrow(ax, xs[i] + bw + 0.6, xs[i + 1] - 0.6, BY + BH / 2)

    ax.add_patch(FancyBboxPatch((GUT, 1.6), W - GUT - 3.0, 6.4,
                                "round,pad=0,rounding_size=1.4",
                                fc="#FFFFFF", ec=HAIR, lw=.7, zorder=2))
    ax.text(GUT + (W - GUT - 3.0) / 2, 4.8,
            "Read through the model: a person's disease status is legible in "
            "their own endometrium, their rASRM stage is not",
            ha="center", va="center", fontsize=FS_OUT, color=INK, zorder=3)

    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "panel_a_abstract.png",
                dpi=int(os.environ.get("FIGDPI", 600)))
    print(f"wrote {OUT / 'panel_a_abstract.png'}  ({W:.0f} x {H:.0f} mm)")


if __name__ == "__main__":
    main()
