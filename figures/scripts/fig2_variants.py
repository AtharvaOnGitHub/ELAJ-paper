"""Figure 2 variants for AW's 19 Nov review: panel e palettes and contour
weights, panel f in the style of 2c, and the whole figure without panel
titles in a calmer palette. Drafts only, to figures/draft/variants/.

    /Users/atharvawaghmare/miniconda3/envs/elaj/bin/python figures/scripts/fig2_variants.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fig2_panels as P                                              # noqa: E402
import fig2f_prototypes as F                                         # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "draft" / "variants"
OUT.mkdir(parents=True, exist_ok=True)
MM = 1 / 25.4

# A calmer pair: blue and orange differ in lightness as well as hue, so they
# survive colour-blindness and greyscale; both a step below full saturation.
CTL, CAS = "#4F8DA6", "#C7773F"
CTL_D, CAS_D = "#2F6B83", "#9B4F1E"              # darker, for contour lines
SOFT_DIV = LinearSegmentedColormap.from_list("soft", ["#B9D3DF", "#F3F1EC", "#E9BE9C"])
SEQ = LinearSegmentedColormap.from_list("seq", ["#F3F1EC", "#E3B48F", "#B8622C"])

E_OPTS = {
    "e_A_soft_diverging": dict(cmap=SOFT_DIV, vmin=.2, vmax=.8, clw=1.1, ctl=CTL_D, cas=CAS_D),
    "e_B_sequential":     dict(cmap=SEQ, vmin=0, vmax=1, clw=1.1, ctl=CTL_D, cas=CAS_D),
    "e_C_faded_original": dict(cmap="RdBu_r", vmin=.2, vmax=.8, clw=.85, ctl="#1F6F6A", cas="#8E2A26", alpha=.45),
}
for name, kw in E_OPTS.items():
    fig = plt.figure(figsize=(80 * MM, 66 * MM))
    ax = fig.add_axes([.14, .14, .68, .8]); cax = fig.add_axes([.84, .14, .025, .8])
    F.panel_plane(ax, cax, **kw)
    fig.savefig(OUT / f"{name}.png", dpi=300, facecolor="white"); plt.close(fig)
    print("drew", name)

for style in ("strip", "rain"):
    fig = plt.figure(figsize=(80 * MM, 66 * MM))
    axes = [fig.add_axes([.17 + i * .41, .3, .36, .62]) for i in range(2)]
    F.panel_rain(axes, style=style, ctl=CTL, cas=CAS, legend="below")
    fig.savefig(OUT / f"f_{style}_legend_below.png", dpi=300, facecolor="white"); plt.close(fig)
    print("drew f", style)

# ── the whole figure: no panel titles (NMI figures carry letters only),
# the calmer pair throughout, family colours kept (they are the paper's)
# but quieter in d ────────────────────────────────────────────────────────
P.CTL_C, P.CASE_C = CTL, CAS
F.CTL_C, F.CASE_C = CTL, CAS
W, H = 180.0, 214.0
fig = plt.figure(figsize=(W * MM, H * MM))
mm = lambda x, y, w, h: [x / W, y / H, w / W, h / H]


def letter(x, y, l):
    fig.text(x / W, y / H, l, fontsize=P.FS_LETTER, fontweight="bold", va="baseline", color=P.INK)


ax_a = fig.add_axes(mm(14, 154, 70, 52)); ax_b = fig.add_axes(mm(106, 154, 70, 52))
P.frontier_by_kl(ax_a); P.frontier_by_dab(ax_b)
letter(4, 208, "a"); letter(96, 208, "b")
cw, gap, cx0 = 17.0, 1.5, 12.0
c_axes = [fig.add_axes(mm(cx0 + i * (cw + gap), 92, cw, 44)) for i in range(4)]
P.i1(c_axes); letter(4, 142, "c")
ax_d = fig.add_axes(mm(104, 92, 64, 44)); P.i2b(ax_d); ax_d.set_xlim(-.55, 3.95); letter(92, 142, "d")
for b in ax_d.collections:
    try:
        b.set_alpha(.35); b.set_edgecolor("#7d8590"); b.set_linewidth(.4)
    except Exception:
        pass
ax_e = fig.add_axes(mm(14, 14, 62, 62)); cax_e = fig.add_axes(mm(78, 14, 2.2, 62))
F.panel_plane(ax_e, cax_e, **E_OPTS["e_C_faded_original"]); letter(4, 80, "e")   # AW 19 Nov: C, thinner lines
f_axes = [fig.add_axes(mm(108 + i * 32, 22, 28, 54)) for i in range(2)]
F.panel_rain(f_axes, style="rain", ctl=CTL, cas=CAS, legend="below"); letter(96, 80, "f")   # AW 19 Nov: B
fig.savefig(OUT / "figure2_v2.png", dpi=300, facecolor="white")
print("drew figure2_v2")
