"""Figure 2 so far: the new Figure 2 as it stands, assembled at print size.

    /Users/atharvawaghmare/miniconda3/envs/elaj/bin/python figures/scripts/figure2_draft.py

Writes figures/draft/figure2_so_far.png, NOT figures/pinned/figure2.png: the
manuscript still \\includegraphics the old knobs figure, and its caption is
written for that one. Captions wait until the panels are settled (AW, 17
Nov), so the swap into pinned/ happens with the caption, not before.

    a  phase against study separation, the adversarial weight swept (old 2b)
    b  the same, the information cost raised (old 2d)
    c  I1   composition by family, control against case
    d  I2b  disease signal by family, aligned under c's columns
    e  I4b  the disease end of the gene ranking
    f  I6   the external list on our ranking  -- PENDING AW's question

180 mm wide, NMI's double column. Every panel is drawn natively here by
fig2_panels.py rather than pasted in as a PNG, so type sizes are true.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fig2_panels as P                                              # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "draft"
W, H = 180.0, 200.0
fig = plt.figure(figsize=(W / 25.4, H / 25.4))


def mm(x, y, w, h):
    """Axes rect from millimetres, origin bottom left."""
    return [x / W, y / H, w / W, h / H]


def letter(x, y, l, title):
    """Every panel heading at a fixed millimetre position: the letters of a
    column then line up exactly, which per-axes offsets never quite did."""
    fig.text(x / W, y / H, l, fontsize=P.FS_LETTER, fontweight="bold",
             va="baseline", color=P.INK)
    fig.text((x + 5) / W, y / H, title, fontsize=P.FS_TITLE, va="baseline",
             color=P.INK)


# ── row 1: the knobs ─────────────────────────────────────────────────────
ax_a = fig.add_axes(mm(14, 140, 70, 50))
ax_b = fig.add_axes(mm(106, 140, 70, 50))
P.frontier_by_kl(ax_a)
P.frontier_by_dab(ax_b)
letter(4, 193, "a", "Turning up the adversary, at each information cost")
letter(96, 193, "b", "Turning up the information cost, at each adversary")

# ── rows 2-3, left: composition over signal, one column per family ───────
c_axes = []
cw, gap, cx0 = 19.5, 2.0, 14.0     # closer, with no y axes (AW, 17 Nov)
for i in range(4):
    c_axes.append(fig.add_axes(mm(cx0 + i * (cw + gap), 82, cw, 34)))
P.i1(c_axes)
letter(4, 122, "c", "How many cells of each family a donor has")

ax_d = fig.add_axes(mm(cx0, 46, 4 * cw + 3 * gap, 24))
# family i sits under the centre of c's column i, in the same figure units
centres = [cx0 + i * (cw + gap) + cw / 2 for i in range(4)]
ax_d.set_xlim(cx0, cx0 + 4 * cw + 3 * gap)
P.i2b(ax_d, xpos=centres)
letter(4, 73, "d", "How well disease can be read from those cells' state")

# ── rows 2-3, right: the genes ───────────────────────────────────────────
e0 = P.i4b(fig, mm(118, 40, 60, 80))
letter(108, 122, "e", "The genes the disease direction moves")

# ── row 4: I6, marked pending ────────────────────────────────────────────
f1, f2 = P.i6(fig, mm(26, 8, 150, 24))
letter(4, 35, "f", "An external cohort's upregulated genes, placed on our ranking")
fig.text(176 / W, 34.7 / H, "PENDING: under discussion", fontsize=P.FS_SMALL,
         va="bottom", ha="right", color="#B03A2E", fontweight="bold")

OUT.mkdir(parents=True, exist_ok=True)
dest = OUT / "figure2_so_far.png"
fig.savefig(dest, dpi=int(os.environ.get("FIGDPI", 300)), facecolor="white")
print(f"wrote {dest}  ({W:.0f} x {H:.0f} mm)")
