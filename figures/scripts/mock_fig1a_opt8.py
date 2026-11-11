#!/usr/bin/env python
"""Figure 1a, option 8 — AW's revisions of 11 November, second pass.

THE DONOR ARITHMETIC WAS WRONG AND IS NOW RIGHT. Eleven tiles taken from
`patient_id` sum to 269, while the corpus is 254 people. Methods, Data
collection: "One study pair deposits the same fifteen people under two sets
of identifiers, so the 269 identifiers in the corpus resolve to 254 people."
The pair is García-Alonso 2021a and 2021b, two CELLxGENE collections of one
study, and no `patient_id` is shared between them because each collection
relabelled its own. So the two are merged into one tile of 15 donors and
the ten tiles now sum to 254. Eleven STUDIES, ten donor groups.

Also this pass: no bold in the captions, every caption anchored at the same
height inside its cell, the frontier pictogram unsquashed, the phase
pictogram redrawn around what the supervision is FOR, and the dead band at
the foot of the Data beat given the corpus composition.
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
                                FancyArrowPatch)

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
SC = ["#5BA3A0", "#4C78A8", "#E45756", "#54A24B", "#B279A2",
      "#2E5C8A", "#7B4FA0", "#FF9DA6", "#1B7A6B", "#8C2D3F"]
DIS_C = {"eutopic": "#4C78A8", "control": "#5BA3A0",
         "ectopic": "#E45756", "adenomyosis": "#B279A2"}
TIS_C = ["#2E5C8A", "#5BA3A0", "#E8A23C", "#B279A2", "#CC6677", "#999933"]

# NOTHING BELOW 5.6 pt. This panel is authored at 180 mm and placed at
# 175 mm inside Figure 1, a 97% reduction, so an authored 5.0 renders at
# 4.86 and an authored 4.0 at 3.89 — both under NMI's 5 pt floor. The
# earlier sizes were chosen to fit content, which is the wrong way round:
# the floor is fixed and the layout has to give.
FS_H, FS_B, FS_T, FS_S = 6.8, 5.8, 5.6, 5.6
plt.rcParams.update({"font.family": "Arial", "text.color": INK})


def head(ax, x, y, t, sub, c):
    ax.text(x, y, t, ha="left", va="bottom", fontsize=FS_H,
            fontweight="bold", color=c)
    ax.text(x, y - 2.3, sub, ha="left", va="top", fontsize=FS_T, color=NOTE)


def thick_arrow(ax, x, y, length=6.0):
    ax.annotate("", xy=(x + length, y), xytext=(x, y),
                arrowprops=dict(arrowstyle="-|>", color="#AFB5BD", lw=3.4,
                                shrinkA=0, shrinkB=0, mutation_scale=11))


def stacked(ax, x, y, w, h, parts, colours, total):
    """One bar, naming its levels. Percentages told the reader nothing they
    could use; the level names say what the corpus actually contains."""
    cx = x
    spill = []
    for (lab, n), c in zip(parts, colours):
        bw = w * n / total
        ax.add_patch(Rectangle((cx, y), bw, h, fc=c, ec="none", zorder=3))
        if bw >= len(lab) * 1.05:
            ax.text(cx + bw / 2, y + h / 2, lab, ha="center", va="center",
                    fontsize=FS_S, color="#FFFFFF", zorder=4)
        else:
            spill.append((lab, c, cx + bw / 2))   # keep where it actually is
        cx += bw
    # a level too narrow to hold its name is labelled BENEATH ITS OWN
    # SEGMENT with a leader, not parked at the far left where the reader
    # has to match it back by colour
    for lab, c, sx in spill:
        ax.plot([sx, sx], [y, y - 1.5], color=c, lw=.7, zorder=4)
        ax.text(min(sx + 0.8, x + w), y - 2.0, lab, ha="right", va="top",
                fontsize=FS_S, color=c, zorder=4)


# ── the six pictograms. Each draws around (cx, cy); captions are placed
#    by the caller at one fixed height, so they never drift. ─────────────
def pic_groups(ax, cx, cy):
    rng = np.random.default_rng(2)
    for _ in range(7):
        ax.add_patch(Circle((cx - 7.6 + rng.uniform(-1.1, 1.1),
                             cy + rng.uniform(-2.2, 2.2)), .36,
                            fc=HAIR, ec="none", zorder=4))
    for g, gc in enumerate(("#4C78A8", "#5BA3A0", "#B279A2")):
        bx = cx - 2.4 + g * 3.4
        ax.add_patch(FancyBboxPatch((bx - 1.3, cy - 2.3), 2.6, 4.6,
                                    "round,pad=0,rounding_size=.7",
                                    fc="#FFFFFF", ec=gc, lw=.75, zorder=4))
        for k in range(3):
            ax.add_patch(Circle((bx, cy + 1.3 - k * 1.3), .38, fc=gc,
                                ec="none", zorder=5))
    ax.annotate("", xy=(cx - 4.1, cy), xytext=(cx - 5.8, cy),
                arrowprops=dict(arrowstyle="-|>", color=GREY_E, lw=.8,
                                mutation_scale=6), zorder=4)


def pic_sentinel(ax, cx, cy):
    for k, v in enumerate(["3", "0", "", "7", "1"]):
        bx = cx - 6.8 + k * 3.0
        sp = v == ""
        ax.add_patch(FancyBboxPatch((bx - 1.2, cy - 1.2), 2.4, 2.4,
                                    "round,pad=0,rounding_size=.5",
                                    fc=AMB_F if sp else "#FFFFFF",
                                    ec=AMB_E if sp else HAIR,
                                    lw=.9 if sp else .6,
                                    linestyle=(0, (1.6, 1.3)) if sp else "-",
                                    zorder=4))
        ax.text(bx, cy, "?" if sp else v, ha="center", va="center",
                fontsize=FS_T, color=AMB_E if sp else INK,
                fontweight="bold" if sp else "normal", zorder=5)


def pic_dsbn(ax, cx, cy):
    t = np.linspace(-1, 1, 90)
    bell = np.exp(-(t * 2.2) ** 2)
    for off in (-2.6, 2.6):
        ax.plot(cx + t * 3.8 + off, cy - 1.8 + bell * 2.3, color="#9FB6D4",
                lw=.8, zorder=4)
    ax.plot(cx + t * 3.8, cy - 1.8 + bell * 3.0, color=BLUE_E, lw=1.3, zorder=5)


def pic_dab(ax, cx, cy):
    """Back to the simpler shape AW preferred, tidied.

    The crossed-circle version packed a strike, a ring, a filled disc and
    two arrow pairs into 26 mm and read as noise. This is the earlier one:
    study-coloured cells in, a discriminator asked which study, grey cells
    out, and the reversed gradient as the single thing below the line.
    """
    for k, c in enumerate(SC[:3]):
        ax.add_patch(Circle((cx - 7.8, cy + 2.2 - k * 1.7), .52, fc=c,
                            ec="none", zorder=4))
    ax.annotate("", xy=(cx - 3.3, cy + 0.5), xytext=(cx - 6.6, cy + 0.5),
                arrowprops=dict(arrowstyle="-|>", color=GREY_E, lw=.9,
                                mutation_scale=6), zorder=4)
    ax.add_patch(FancyBboxPatch((cx - 3.4, cy - 1.1), 6.4, 3.2,
                                "round,pad=0,rounding_size=.7",
                                fc="#FFFFFF", ec=ROSE, lw=.9, zorder=4))
    ax.text(cx - 0.2, cy + 0.5, "study?", ha="center", va="center",
            fontsize=FS_S, color=ROSE, zorder=5)
    ax.annotate("", xy=(cx + 5.4, cy + 0.5), xytext=(cx + 3.3, cy + 0.5),
                arrowprops=dict(arrowstyle="-|>", color=GREY_E, lw=.9,
                                mutation_scale=6), zorder=4)
    for k in range(3):
        ax.add_patch(Circle((cx + 6.6, cy + 2.2 - k * 1.7), .52, fc="#C9CDD4",
                            ec="none", zorder=4))
    ax.annotate("", xy=(cx - 6.8, cy - 2.6), xytext=(cx + 1.4, cy - 2.6),
                arrowprops=dict(arrowstyle="-|>", color=ROSE, lw=1.5,
                                mutation_scale=7), zorder=5)
    ax.text(cx - 2.7, cy - 3.2, "reversed gradient", ha="center", va="top",
            fontsize=FS_S, color=ROSE, zorder=5)


def pic_phase(ax, cx, cy):
    """WHY the cycle is supervised: endometrium remodels around it.

    The ring was vague and the four-boxes-with-a-tick said "a choice" but
    not "a cycle". This draws the thing the supervision exists for: the
    same tissue at four points of one closed loop, visibly different at
    each, with the loop closing back on itself.
    """
    R = 3.4
    for k in range(4):
        a = np.pi / 2 - k * np.pi / 2
        px, py = cx + R * np.cos(a), cy + 0.3 + R * np.sin(a)
        ax.add_patch(Ellipse((px, py), 2.5 + k * 0.35, 2.1 + k * 0.30,
                             fc=PHASE_C[k], ec="none", alpha=.95, zorder=5))
    for k in range(4):
        a0 = 90 - k * 90
        ax.add_patch(FancyArrowPatch(
            (cx + R * np.cos(np.deg2rad(a0 - 22)),
             cy + 0.3 + R * np.sin(np.deg2rad(a0 - 22))),
            (cx + R * np.cos(np.deg2rad(a0 - 68)),
             cy + 0.3 + R * np.sin(np.deg2rad(a0 - 68))),
            connectionstyle="arc3,rad=-0.35", arrowstyle="-|>",
            color=GREY_E, lw=.7, mutation_scale=5, zorder=4))


def pic_latent(ax, cx, cy):
    ax.add_patch(FancyBboxPatch((cx - 8.4, cy - 1.6), 4.2, 3.3,
                                "round,pad=0,rounding_size=.7",
                                fc="#BBD2EC", ec=BLUE_E, lw=.7, zorder=4))
    ax.text(cx - 6.3, cy + 0.05, "cell", ha="center", va="center",
            fontsize=FS_S, color=INK, zorder=5)
    ax.annotate("", xy=(cx - 2.9, cy + 0.05), xytext=(cx - 3.9, cy + 0.05),
                arrowprops=dict(arrowstyle="-|>", color=GREY_E, lw=.8,
                                mutation_scale=6), zorder=4)
    for k in range(16):
        ax.add_patch(FancyBboxPatch((cx - 2.3 + (k % 8) * 1.28,
                                     cy + 0.6 - (k // 8) * 1.55), .95, .95,
                                    "round,pad=0,rounding_size=.22",
                                    fc=AMB_E, ec="none", zorder=4))


# ── outcomes ────────────────────────────────────────────────────────────
def res_dominance(ax, cx, cy):
    """Unsquashed: the axes are the point, so give them room."""
    w, h = 15.0, 10.0
    x0, y0 = cx - w / 2, cy - h / 2
    ax.add_patch(Rectangle((x0 + w * .34, y0), w * .66, h * .66,
                           fc="#F3E7E5", ec="none", zorder=2))
    rng = np.random.default_rng(4)
    for _ in range(9):
        ax.add_patch(Circle((x0 + w * rng.uniform(.40, .94),
                             y0 + h * rng.uniform(.10, .58)), .52,
                            fc="#FFFFFF", ec=NOTE, lw=.6, zorder=4))
    ax.add_patch(Circle((x0 + w * .18, y0 + h * .86), 1.0, fc=AMB_F,
                        ec=AMB_E, lw=1.2, zorder=5))
    ax.annotate("", xy=(x0, y0 + h + .6), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=HAIR, lw=.7,
                                mutation_scale=5), zorder=3)
    ax.annotate("", xy=(x0 + w + .6, y0), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=HAIR, lw=.7,
                                mutation_scale=5), zorder=3)


def res_donor(ax, cx, cy):
    for k in range(4):
        a = 1.0 - k * 0.27
        bx = cx - 5.6 + k * 3.8
        ax.add_patch(Circle((bx, cy + 1.7), .80, fc=TEAL_E, ec="none",
                            alpha=a, zorder=4))
        ax.add_patch(Ellipse((bx, cy - 0.8), 2.4, 2.2, fc=TEAL_E, ec="none",
                             alpha=a, zorder=4))


def res_cycle(ax, cx, cy):
    t = np.linspace(0, 2 * np.pi, 160)
    for k in range(4):
        s = slice(k * 40, (k + 1) * 40 + 1)
        ax.plot(cx - 6.6 + t[s] * 2.1, cy + np.sin(t[s]) * 2.4,
                color=PHASE_C[k], lw=1.6, zorder=5)


def res_dissociation(ax, cx, cy):
    ax.add_patch(Circle((cx - 3.6, cy), 2.4, fc="#E3F0E6", ec=TEAL_E,
                        lw=.9, zorder=4))
    ax.plot([cx - 4.7, cx - 3.9, cx - 2.3], [cy, cy - 0.9, cy + 1.1],
            color=TEAL_E, lw=1.3, solid_capstyle="round", zorder=5)
    ax.add_patch(Circle((cx + 3.4, cy), 2.4, fc="#F7E3E1", ec=ROSE, lw=.9,
                        zorder=4))
    for s in (1, -1):
        ax.plot([cx + 2.3, cx + 4.5][::s], [cy - 1.1, cy + 1.1],
                color=ROSE, lw=1.3, solid_capstyle="round", zorder=5)


def main() -> None:
    m = pd.read_csv(ROOT / f"Outputs/cells/{ARM}/metadata.csv.gz",
                    low_memory=False,
                    usecols=["study", "patient_id", "disease_status", "tissue"])
    per = m.groupby("study").patient_id.nunique()
    # the one merge the corpus cannot do for itself
    ga = [s for s in per.index if s.startswith("garcia_alonso")]
    assert len(ga) == 2 and per[ga].sum() == 30, "the 15/15 pair has changed"
    per = per.drop(ga)
    per["garcia_alonso_2021"] = 15
    per = per.sort_values(ascending=False)
    assert per.sum() == 254, f"tiles sum to {per.sum()}, not 254"
    names = dict(STUDY_NAME); names["garcia_alonso_2021"] = "García-Alonso 2021"

    W, H = 180.0, 78.0
    fig = plt.figure(figsize=(W / 25.4, H / 25.4))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H)
    ax.axis("off")
    TOP = 72.0

    # ── Data ────────────────────────────────────────────────────────────
    head(ax, 3, TOP, "Data", "every eligible study, sized by donors", GREY_E)
    rng = np.random.default_rng(5); placed = []
    for i, (s, n) in enumerate(per.items()):
        r = 5.6 * (n / per.max()) ** 0.5
        for _ in range(900):
            ex, ey = 3 + rng.uniform(r, 49 - r), 46 + rng.uniform(r * .7, 17 - r * .7)
            if all((ex - px) ** 2 + ((ey - py) * 1.5) ** 2 > (r + pr) ** 2 * .95
                   for px, py, pr in placed):
                break
        placed.append((ex, ey, r))
        ax.add_patch(Ellipse((ex, ey), r * 2, r * 1.4, fc=SC[i], ec="none",
                             alpha=.92, zorder=3))
    rows = 5
    for i, (s, n) in enumerate(per.items()):
        cx2 = 3 + (i // rows) * 28.5
        cy2 = 38.0 - (i % rows) * 3.3
        ax.add_patch(Circle((cx2 + .8, cy2), .68, fc=SC[i], ec="none", zorder=4))
        nm = names.get(s, s)
        # 0.55 em per character is DejaVu/Arial's rough average; the count
        # is right-aligned at +25.0, so anything past ~21 mm would overlap
        assert len(nm) * 0.55 * FS_T / 72 * 25.4 < 21.0, f"legend name too long: {nm}"
        ax.text(cx2 + 2.3, cy2, nm, ha="left", va="center",
                fontsize=FS_T, color=NOTE)
        ax.text(cx2 + 25.0, cy2, str(n), ha="right", va="center",
                fontsize=FS_T, color=INK)
    # ONE bar, not two. The anatomical-site bar was a second chart saying
    # nothing the disease bar did not, in a beat that is about the corpus.
    dis = m.disease_status.value_counts()
    stacked(ax, 3, 11.0, 49, 5.2,
            [(k, dis[k]) for k in DIS_C], list(DIS_C.values()), len(m))
    ax.text(3, 16.6, "disease status", fontsize=FS_S, color=NOTE, va="bottom")
    ax.text(27.5, 2.6, "1,577,728 cells   ·   254 donors   ·   11 studies",
            ha="center", va="bottom", fontsize=FS_T, color=INK,
            fontweight="bold")

    thick_arrow(ax, 56.0, 46.0)

    # ── The Model ───────────────────────────────────────────────────────
    head(ax, 62, TOP, "The Model", "inductive bias in place of scale", BLUE_E)
    BX, BY, BW, BH = 62.0, 5.0, 58.0, 59.0
    ax.add_patch(FancyBboxPatch((BX, BY), BW, BH,
                                "round,pad=0,rounding_size=1.7",
                                fc=BLUE_F, ec=BLUE_E, lw=.9, zorder=2))
    pw, ph = BW * 0.62, 4.8
    ax.add_patch(FancyBboxPatch((BX + (BW - pw) / 2, BY + BH - ph / 2), pw, ph,
                                "round,pad=0,rounding_size=2.4",
                                fc=BLUE_E, ec=BLUE_E, lw=0, zorder=6))
    ax.text(BX + BW / 2, BY + BH + 0.05, "ELAJ   ·   1,883,986 parameters",
            ha="center", va="center", fontsize=FS_B, color="#FFFFFF",
            fontweight="bold", zorder=7)

    # 5.5 reserves the pill's band at the top; the row pitch then has
    # to leave two caption lines inside the box, which it did not before
    cw, ch = BW / 2, (BH - 5.5) / 3
    draw = [(pic_groups,   ["genes read into", "pathway groups"]),
            (pic_sentinel, ["a gene never assayed is a", "Did Not Sample sentinel"]),
            (pic_dsbn,     ["DSBN normalises study", "by its own statistics"]),
            (pic_dab,      ["DAB removes study", "identity adversarially"]),
            (pic_phase,    ["the endometrium remodels", "around the menstrual cycle"]),
            (pic_latent,   ["every cell becomes a", "16 dimensional latent"])]
    for i, (fn, lines) in enumerate(draw):
        col, row = i % 2, i // 2
        ccx = BX + cw * (col + .5)
        ctop = BY + BH - 5.5 - row * ch
        fn(ax, ccx, ctop - ch * 0.33)          # pictogram, fixed offset
        for j, txt in enumerate(lines):        # caption, fixed anchor
            ax.text(ccx, ctop - ch * 0.68 - j * 2.3, txt, ha="center",
                    va="top", fontsize=FS_T, color=NOTE, zorder=5)

    thick_arrow(ax, 122.5, 46.0)

    # ── Outcomes ────────────────────────────────────────────────────────
    head(ax, 131, TOP, "Outcomes", "what they hold, and how they compare", AMB_E)
    RX, RY, RW, RH = 131.0, 5.0, 46.0, 59.0
    rh = RH / 4
    rdraw = [(res_dominance, ["better than all nine", "on both axes at once"]),
             (res_donor, ["least donor identity", "of anything tested"]),
             (res_cycle, ["most cycle signal", "of anything tested"]),
             (res_dissociation, ["disease status legible,", "rASRM stage not"])]
    for i, (fn, lines) in enumerate(rdraw):
        cy = RY + RH - rh * (i + .5)
        fn(ax, RX + 9.0, cy)
        for j, txt in enumerate(lines):
            ax.text(RX + 20.0, cy + 1.2 - j * 2.3, txt, ha="left", va="center",
                    fontsize=FS_T, color=NOTE)

    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "mock_fig1a_opt8.png",
                dpi=int(os.environ.get("FIGDPI", 400)))
    print(f"wrote {OUT / 'mock_fig1a_opt8.png'}  ({W:.0f} x {H:.0f} mm)")
    print(f"  tiles: {len(per)} donor groups summing to {per.sum()}")


if __name__ == "__main__":
    main()
