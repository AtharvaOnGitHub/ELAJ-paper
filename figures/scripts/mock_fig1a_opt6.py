#!/usr/bin/env python
"""Figure 1a, option 6 — AW's revisions of 11 November.

  * the right beat drops the frontier plot. The UMAP and the frontier are
    already main results elsewhere in Figure 1, so repeating one here spends
    the most valuable space in the paper on a duplicate. Results become
    pictograms like everything else.
  * the middle grows to six: pathway grouping and the DNS sentinel both
    redrawn, plus DSBN, the study adversary, the menstrual-phase head and
    the latent.
  * the middle's heading is now ELAJ and its parameter count, not a verb.

PICTOGRAMS, NOT THUMBNAILS. The test each one has to pass: could a reader
who has never seen the paper guess what it means from the picture before
reading the caption? The sentinel one is the clearest case, because the
whole idea is that a gene never assayed is NOT a zero, and two tiles
showing 0 against a dash say that instantly where a sentence does not.
"""
from __future__ import annotations
import os, sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import (FancyBboxPatch, Rectangle, Ellipse, Circle,
                                Wedge, FancyArrowPatch)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figure1 import STUDY_NAME                                 # noqa: E402

ROOT = Path("/Users/atharvawaghmare/Endo research/ELAJ")
ARM = "p1_dab168_kl1"
OUT = Path(__file__).resolve().parents[1] / "pinned"

INK, NOTE, HAIR = "#2B3038", "#6F7681", "#C9CDD4"
GREY_F, GREY_E = "#EDEFF2", "#6B7380"
BLUE_F, BLUE_E = "#E9F2FC", "#3F6FB4"
AMB_F,  AMB_E  = "#FFF3DE", "#D89120"
TEAL_E, ROSE = "#2F8F88", "#C2544E"
PHASE_C = ["#4C78A8", "#5BA3A0", "#E8A23C", "#B279A2"]
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


def cap(ax, cx, cy, text):
    ax.text(cx, cy, text, ha="center", va="top", fontsize=FS_T, color=NOTE,
            linespacing=1.35, zorder=5)


# ── the six ELAJ pictograms ──────────────────────────────────────────────
def pic_groups(ax, cx, cy):
    """Loose genes pulled into three labelled bundles."""
    rng = np.random.default_rng(2)
    for _ in range(7):
        ax.add_patch(Circle((cx - 7.4 + rng.uniform(-1.1, 1.1),
                             cy + rng.uniform(-2.2, 2.2)), .36,
                            fc=HAIR, ec="none", zorder=4))
    for g, gc in enumerate(("#4C78A8", "#5BA3A0", "#B279A2")):
        bx = cx - 2.6 + g * 3.4
        ax.add_patch(FancyBboxPatch((bx - 1.3, cy - 2.3), 2.6, 4.6,
                                    "round,pad=0,rounding_size=.7",
                                    fc="#FFFFFF", ec=gc, lw=.75, zorder=4))
        for k in range(3):
            ax.add_patch(Circle((bx, cy + 1.3 - k * 1.3), .38, fc=gc,
                                ec="none", zorder=5))
    ax.annotate("", xy=(cx - 4.3, cy), xytext=(cx - 6.0, cy),
                arrowprops=dict(arrowstyle="-|>", color=GREY_E, lw=.8,
                                mutation_scale=6), zorder=4)


def pic_sentinel(ax, cx, cy):
    """A measured zero and a gene never assayed are different things."""
    vals = ["3", "0", "", "7", "1"]
    for k, v in enumerate(vals):
        bx = cx - 7.2 + k * 3.0
        special = v == ""
        ax.add_patch(FancyBboxPatch((bx - 1.2, cy - 1.2), 2.4, 2.4,
                                    "round,pad=0,rounding_size=.5",
                                    fc=AMB_F if special else "#FFFFFF",
                                    ec=AMB_E if special else HAIR,
                                    lw=.9 if special else .6,
                                    linestyle=(0, (1.6, 1.3)) if special else "-",
                                    zorder=4))
        ax.text(bx, cy, "?" if special else v, ha="center", va="center",
                fontsize=FS_T, color=AMB_E if special else INK,
                fontweight="bold" if special else "normal", zorder=5)
    # no sub-labels: "measured" and "never assayed" collided here, and the
    # caption plus the 0-against-? contrast already carry the whole idea


def pic_dsbn(ax, cx, cy):
    """Three studies' distributions brought onto one scale."""
    t = np.linspace(-1, 1, 90)
    bell = np.exp(-(t * 2.2) ** 2)
    for off, col in ((-2.6, "#9FB6D4"), (2.6, "#9FB6D4")):
        ax.plot(cx + t * 3.8 + off, cy - 1.4 + bell * 2.3, color=col, lw=.8,
                zorder=4)
    ax.plot(cx + t * 3.8, cy - 1.4 + bell * 2.9, color=BLUE_E, lw=1.2, zorder=5)
    ax.annotate("", xy=(cx - 0.9, cy + 2.4), xytext=(cx - 3.1, cy + 2.4),
                arrowprops=dict(arrowstyle="-|>", color=GREY_E, lw=.7,
                                mutation_scale=5), zorder=4)
    ax.annotate("", xy=(cx + 0.9, cy + 2.4), xytext=(cx + 3.1, cy + 2.4),
                arrowprops=dict(arrowstyle="-|>", color=GREY_E, lw=.7,
                                mutation_scale=5), zorder=4)


def pic_dab(ax, cx, cy):
    """A discriminator guessing the study, with its gradient reversed."""
    for k, c in enumerate(SC[:3]):
        ax.add_patch(Circle((cx - 7.0, cy + 1.9 - k * 1.9), .52, fc=c,
                            ec="none", zorder=4))
    ax.add_patch(FancyBboxPatch((cx - 3.3, cy - 1.7), 5.2, 3.4,
                                "round,pad=0,rounding_size=.7",
                                fc="#FFFFFF", ec=ROSE, lw=.8, zorder=4))
    ax.text(cx - 0.7, cy, "study?", ha="center", va="center", fontsize=3.9,
            color=ROSE, zorder=5)
    ax.annotate("", xy=(cx - 3.6, cy), xytext=(cx - 6.2, cy),
                arrowprops=dict(arrowstyle="-|>", color=GREY_E, lw=.8,
                                mutation_scale=6), zorder=4)
    ax.add_patch(FancyArrowPatch((cx + 1.9, cy - 1.2), (cx - 6.4, cy - 2.9),
                                 connectionstyle="arc3,rad=0.33",
                                 arrowstyle="-|>", color=ROSE, lw=.9,
                                 linestyle=(0, (2.0, 1.4)), mutation_scale=6,
                                 zorder=5))
    # the dashed back-arrow IS the reversal; an inline label printed on top
    # of the cell's own caption


def pic_phase(ax, cx, cy):
    """The cycle, as a closed ring the model is taught to read."""
    for k in range(4):
        ax.add_patch(Wedge((cx, cy + 0.3), 3.3, 90 - (k + 1) * 90, 90 - k * 90,
                           width=1.25, fc=PHASE_C[k], ec="none", zorder=4))
    ax.add_patch(FancyArrowPatch((cx + 0.1, cy + 4.1), (cx + 1.5, cy + 3.7),
                                 connectionstyle="arc3,rad=-0.5",
                                 arrowstyle="-|>", color=GREY_E, lw=.8,
                                 mutation_scale=6, zorder=5))


def pic_latent(ax, cx, cy):
    """Sixteen numbers."""
    ax.add_patch(Rectangle((cx - 7.4, cy - 1.7), 2.6, 3.4, fc="#BBD2EC",
                           ec="none", zorder=4))
    ax.annotate("", xy=(cx - 3.2, cy), xytext=(cx - 4.4, cy),
                arrowprops=dict(arrowstyle="-|>", color=GREY_E, lw=.8,
                                mutation_scale=6), zorder=4)
    for k in range(16):
        ax.add_patch(Circle((cx - 2.0 + (k % 8) * 1.18,
                             cy + 1.0 - (k // 8) * 1.9), .40, fc=AMB_E,
                            ec="none", zorder=4))


# ── the four result pictograms ───────────────────────────────────────────
def res_dominance(ax, cx, cy):
    """Two faint axes, or "on both axes at once" is not visible at all."""
    ax.annotate("", xy=(cx - 6.6, cy + 4.0), xytext=(cx - 6.6, cy - 3.9),
                arrowprops=dict(arrowstyle="-|>", color=HAIR, lw=.7,
                                mutation_scale=5), zorder=3)
    ax.annotate("", xy=(cx + 7.2, cy - 3.9), xytext=(cx - 6.6, cy - 3.9),
                arrowprops=dict(arrowstyle="-|>", color=HAIR, lw=.7,
                                mutation_scale=5), zorder=3)
    ax.add_patch(Rectangle((cx - 4.0, cy - 3.9), 11.0, 6.2, fc="#F3E7E5",
                           ec="none", zorder=2))
    rng = np.random.default_rng(4)
    for _ in range(9):
        ax.add_patch(Circle((cx + rng.uniform(-2.6, 6.0),
                             cy + rng.uniform(-3.0, 1.6)), .50,
                            fc="#FFFFFF", ec=NOTE, lw=.6, zorder=4))
    ax.add_patch(Circle((cx - 5.2, cy + 3.0), .95, fc=AMB_F, ec=AMB_E,
                        lw=1.1, zorder=5))


def res_donor(ax, cx, cy):
    for k in range(4):
        a = 1.0 - k * 0.27
        bx = cx - 6.2 + k * 4.0
        ax.add_patch(Circle((bx, cy + 1.9), .85, fc=TEAL_E, ec="none",
                            alpha=a, zorder=4))
        ax.add_patch(Ellipse((bx, cy - 0.7), 2.6, 2.4, fc=TEAL_E, ec="none",
                             alpha=a, zorder=4))


def res_cycle(ax, cx, cy):
    t = np.linspace(0, 2 * np.pi, 160)
    ax.plot(cx - 7.0 + t * 2.24, cy + 0.4 + np.sin(t) * 2.5, color=NOTE,
            lw=.8, alpha=.4, zorder=4)
    for k in range(4):
        s = slice(k * 40, (k + 1) * 40 + 1)
        ax.plot(cx - 7.0 + t[s] * 2.24, cy + 0.4 + np.sin(t[s]) * 2.5,
                color=PHASE_C[k], lw=1.5, zorder=5)


def res_dissociation(ax, cx, cy):
    ax.add_patch(Circle((cx - 4.0, cy + 0.4), 2.5, fc="#E3F0E6", ec=TEAL_E,
                        lw=.9, zorder=4))
    ax.plot([cx - 5.1, cx - 4.3, cx - 2.7], [cy + 0.4, cy - 0.5, cy + 1.5],
            color=TEAL_E, lw=1.3, solid_capstyle="round", zorder=5)
    ax.add_patch(Circle((cx + 3.4, cy + 0.4), 2.5, fc="#F7E3E1", ec=ROSE,
                        lw=.9, zorder=4))
    for s in (1, -1):
        ax.plot([cx + 2.3, cx + 4.5][::s], [cy - 0.7, cy + 1.5],
                color=ROSE, lw=1.3, solid_capstyle="round", zorder=5)


def main() -> None:
    m = pd.read_csv(ROOT / f"Outputs/cells/{ARM}/metadata.csv.gz",
                    low_memory=False, usecols=["study", "patient_id"])
    per = m.groupby("study").patient_id.nunique().sort_values(ascending=False)

    W, H = 180.0, 66.0
    fig = plt.figure(figsize=(W / 25.4, H / 25.4))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H)
    ax.axis("off")
    TOP = 60.0

    # ── collect ─────────────────────────────────────────────────────────
    head(ax, 3, TOP, "Collect", "every eligible study, sized by donors", GREY_E)
    rng = np.random.default_rng(5); placed = []
    for i, (s, n) in enumerate(per.items()):
        r = 4.6 * (n / per.max()) ** 0.5
        for _ in range(900):
            ex, ey = 3 + rng.uniform(r, 44 - r), 33 + rng.uniform(r * .7, 16 - r * .7)
            if all((ex - px) ** 2 + ((ey - py) * 1.45) ** 2 > (r + pr) ** 2 * .92
                   for px, py, pr in placed):
                break
        placed.append((ex, ey, r))
        ax.add_patch(Ellipse((ex, ey), r * 2, r * 1.38, fc=SC[i], ec="none",
                             alpha=.92, zorder=3))
    rows = 6
    for i, (s, n) in enumerate(per.items()):
        cx2 = 3 + (i // rows) * 24.5
        cy2 = 27.0 - (i % rows) * 2.7
        ax.add_patch(Circle((cx2 + .8, cy2), .68, fc=SC[i], ec="none", zorder=4))
        ax.text(cx2 + 2.3, cy2, STUDY_NAME.get(s, s), ha="left", va="center",
                fontsize=FS_T, color=NOTE)
        ax.text(cx2 + 22.5, cy2, str(n), ha="right", va="center",
                fontsize=FS_T, color=INK, fontweight="bold")
    ax.add_patch(FancyBboxPatch((3, 3.4), 49, 5.4,
                                "round,pad=0,rounding_size=2.0",
                                fc=GREY_F, ec=GREY_E, lw=.8, zorder=3))
    ax.text(27.5, 6.1, "1,577,728 cells  ·  254 donors  ·  11 studies",
            ha="center", va="center", fontsize=FS_B, color=INK,
            fontweight="bold", zorder=4)

    thick_arrow(ax, 54.0, 33.0)

    # ── ELAJ, six pictograms ────────────────────────────────────────────
    head(ax, 64, TOP, "ELAJ", "1,883,986 parameters", BLUE_E)
    BX, BY, BW, BH = 64.0, 10.0, 56.0, 43.0
    ax.add_patch(FancyBboxPatch((BX, BY), BW, BH,
                                "round,pad=0,rounding_size=1.7",
                                fc=BLUE_F, ec=BLUE_E, lw=.9, zorder=2))
    cw, ch = BW / 2, BH / 3
    cells = [(BX + cw * .5, BY + BH - ch * .5), (BX + cw * 1.5, BY + BH - ch * .5),
             (BX + cw * .5, BY + BH - ch * 1.5), (BX + cw * 1.5, BY + BH - ch * 1.5),
             (BX + cw * .5, BY + ch * .5),       (BX + cw * 1.5, BY + ch * .5)]
    draw = [(pic_groups, "genes read in\n44 pathway groups"),
            (pic_sentinel, "a gene never assayed\nis not a zero"),
            (pic_dsbn, "each study normalised\non its own statistics"),
            (pic_dab, "study identity\npushed out of the latent"),
            (pic_phase, "cycle phase\nthe one label supervised"),
            (pic_latent, "every cell becomes\nsixteen numbers")]
    for (fn, text), (cx, cy) in zip(draw, cells):
        fn(ax, cx, cy + 1.6)
        cap(ax, cx, cy - 3.3, text)

    thick_arrow(ax, 122.0, 33.0)

    # ── results, four pictograms ────────────────────────────────────────
    head(ax, 132, TOP, "Results", "against nine other representations", AMB_E)
    RX, RY, RW, RH = 132.0, 10.0, 45.0, 43.0
    rw, rh = RW / 1, RH / 4
    rcells = [(RX + rw * .5, RY + RH - rh * .5), (RX + rw * .5, RY + RH - rh * 1.5),
              (RX + rw * .5, RY + RH - rh * 2.5), (RX + rw * .5, RY + RH - rh * 3.5)]
    rdraw = [(res_dominance, "better than all nine\non both axes at once"),
             (res_donor, "least donor identity\nof anything tested"),
             (res_cycle, "most cycle signal\nof anything tested"),
             (res_dissociation, "disease status legible,\nrASRM stage not")]
    for (fn, text), (cx, cy) in zip(rdraw, rcells):
        fn(ax, cx - 7.0, cy + 0.4)
        ax.text(cx + 6.0, cy + 0.4, text, ha="left", va="center",
                fontsize=FS_T, color=NOTE, linespacing=1.35)

    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "mock_fig1a_opt6.png",
                dpi=int(os.environ.get("FIGDPI", 400)))
    print(f"wrote {OUT / 'mock_fig1a_opt6.png'}  ({W:.0f} x {H:.0f} mm)")


if __name__ == "__main__":
    main()
