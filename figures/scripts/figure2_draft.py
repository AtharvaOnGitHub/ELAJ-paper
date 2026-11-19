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
W, H = 180.0, 222.0
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
ax_a = fig.add_axes(mm(14, 160, 70, 48))
ax_b = fig.add_axes(mm(106, 160, 70, 48))
P.frontier_by_kl(ax_a)
P.frontier_by_dab(ax_b)
letter(4, 214, "a", "Turning up the adversary, at each information cost")
letter(96, 214, "b", "Turning up the information cost, at each adversary")

# ── row 2: composition beside signal (AW, 17 Nov: e removed, c and d side
# by side, "a little bit of squishing may be needed") ─────────────────────
cw, gap, cx0 = 17.0, 1.5, 12.0
c_axes = [fig.add_axes(mm(cx0 + i * (cw + gap), 98, cw, 38)) for i in range(4)]
P.i1(c_axes)
letter(4, 145, "c", "How many cells of each family a donor has")
ax_d = fig.add_axes(mm(104, 98, 62, 38))
P.i2b(ax_d)
ax_d.set_xlim(-.55, 3.95)
letter(92, 145, "d", "How well disease can be read from those cells' state")

# ── row 3 (AW, 19 Nov): e, immune cells in the plane of the two axes;
# f, every donor's held-out position on the immune and stromal axes ───────
import fig2f_prototypes as F                                         # noqa: E402
ax_e = fig.add_axes(mm(14, 12, 62, 62)); cax_e = fig.add_axes(mm(78, 12, 2.2, 62))
F.panel_plane(ax_e, cax_e)
letter(4, 82, "e", "Immune cells: the disease axis follows the lymphoid-to-myeloid axis")
f_axes = [fig.add_axes(mm(108 + i * 30, 16, 24, 58)) for i in range(2)]
F.panel_rain(f_axes)
letter(96, 82, "f", "Every donor, held out: where it sits on the axis")
fig.text(176 / W, 4 / H, "DRAFT", fontsize=P.FS_SMALL, va="baseline", ha="right",
         color="#B03A2E", fontweight="bold")

OUT.mkdir(parents=True, exist_ok=True)
dest = OUT / "figure2_so_far.png"
fig.savefig(dest, dpi=int(os.environ.get("FIGDPI", 300)), facecolor="white")
print(f"wrote {dest}  ({W:.0f} x {H:.0f} mm)")
