#!/usr/bin/env python
"""Candidate Figure 1a — the paper in one image, IBDex's idiom.

AW, 11 November, on the previous attempt: "too literal with too many words.
That is not a graphical abstract." He was right. It was a table of sentences
with boxes drawn round it.

WHAT IBDex FIG. 1a ACTUALLY DOES (Acharjee, medRxiv 2026.10.20.26365993),
read off the PDF rather than remembered:
  * bold coloured headings over each group, and almost no prose anywhere
  * stacked proportional bars with the count AND the percentage set inside
    the coloured block, in white
  * pictograms where a picture will do
  * numbers as the content. Sentences are the caption's job, not the
    figure's.

So this version carries four beats, each a heading, a three-word subtitle
and a picture made of real numbers. The argument is in the comparison of
the pictures, not in text:

  corpus -> donors are the binding constraint -> small model -> the frontier

which is the agreed one-line story, with the prose removed.

THE DONOR COUNT IS 254, NOT THE 269 THE TABLE RETURNS. 269 is the
pre-deduplication count of patient identifiers; fifteen samples are
duplicated across studies. 254 is the settled number everywhere in the
paper and 269 appears only in Data collection where the merge is explained.
The assert below fails loudly if that ever stops being true.
"""
from __future__ import annotations
import os, sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyBboxPatch, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from table1 import collect, MANIFEST, BASELINES, FOUNDATION   # noqa: E402

ROOT = Path("/Users/atharvawaghmare/Endo research/ELAJ")
ARM = "p1_dab168_kl1"
OUT = Path(__file__).resolve().parents[1] / "pinned"

DONORS = 254          # see the docstring
PARAMS_ELAJ, PARAMS_FM = 1.883986, 100.0      # millions

INK, NOTE, HAIR = "#2B3038", "#6F7681", "#C9CDD4"
GREY_E, BLUE_E, TEAL_E, AMB_E = "#6B7380", "#3F6FB4", "#2F8F88", "#D89120"
DIS_C = {"eutopic": "#4C78A8", "control": "#5BA3A0",
         "ectopic": "#E45756", "adenomyosis": "#B279A2"}
TIS_C = ["#2E5C8A", "#5BA3A0", "#E8A23C", "#B279A2", "#CC6677", "#999933"]

FS_HEAD, FS_SUB, FS_NUM, FS_TINY = 6.5, 5.5, 5.5, 4.8
plt.rcParams.update({"font.family": "Arial", "text.color": INK})


def heading(ax, x, y, text, sub, colour):
    ax.text(x, y, text, ha="left", va="bottom", fontsize=FS_HEAD,
            fontweight="bold", color=colour)
    ax.text(x, y - 2.4, sub, ha="left", va="top", fontsize=FS_SUB, color=NOTE)


def stacked(ax, x, y, w, h, parts, colours, total, inside_min=0.10):
    """IBDex's bar: counts and percents set inside the block, in white."""
    cx = x
    for (lab, n), c in zip(parts, colours):
        bw = w * n / total
        ax.add_patch(Rectangle((cx, y), bw, h, fc=c, ec="none", zorder=3))
        if n / total >= inside_min:
            ax.text(cx + bw / 2, y + h * 0.60, lab, ha="center", va="center",
                    fontsize=FS_TINY, color="#FFFFFF", fontweight="bold", zorder=4)
            ax.text(cx + bw / 2, y + h * 0.24, f"{100*n/total:.0f}%",
                    ha="center", va="center", fontsize=FS_TINY,
                    color="#FFFFFF", zorder=4)
        cx += bw


def main() -> None:
    m = pd.read_csv(ROOT / f"Outputs/cells/{ARM}/metadata.csv.gz",
                    low_memory=False,
                    usecols=["study", "tissue", "disease_status", "patient_id"])
    assert m.patient_id.nunique() == 269, "the 269/254 note in the docstring is stale"
    n_cells, n_studies = len(m), m.study.nunique()
    dis = m.disease_status.value_counts()
    tis = m.tissue.value_counts()
    per_study = m.groupby("study").patient_id.nunique().sort_values(ascending=False)

    W, H = 180.0, 60.0
    fig = plt.figure(figsize=(W / 25.4, H / 25.4))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H)
    ax.axis("off")

    GAP = 7.0
    bw = (W - 6.0 - 3 * GAP) / 4
    xs = [3.0 + i * (bw + GAP) for i in range(4)]
    TOP = 54.0

    # ── 1. the corpus ───────────────────────────────────────────────────
    x = xs[0]
    heading(ax, x, TOP, "Corpus", "every eligible study", GREY_E)
    ax.text(x, TOP - 7.0, f"{n_cells:,}", ha="left", va="top",
            fontsize=11, fontweight="bold", color=INK)
    ax.text(x, TOP - 14.0, f"cells  ·  {n_studies} studies", ha="left",
            va="top", fontsize=FS_NUM, color=NOTE)
    stacked(ax, x, 24.0, bw, 5.2,
            [(k, dis[k]) for k in ["eutopic", "control", "ectopic", "adenomyosis"]],
            [DIS_C[k] for k in ["eutopic", "control", "ectopic", "adenomyosis"]],
            n_cells)
    ax.text(x, 30.2, "disease status", ha="left", va="bottom",
            fontsize=FS_TINY, color=NOTE)
    stacked(ax, x, 13.0, bw, 5.2, list(tis.items())[:6], TIS_C, n_cells)
    ax.text(x, 19.2, "anatomical site", ha="left", va="bottom",
            fontsize=FS_TINY, color=NOTE)

    # ── 2. the binding constraint ───────────────────────────────────────
    x = xs[1]
    heading(ax, x, TOP, "Donors", "the binding constraint", BLUE_E)
    ax.text(x, TOP - 7.0, f"{DONORS}", ha="left", va="top",
            fontsize=11, fontweight="bold", color=BLUE_E)
    ax.text(x, TOP - 14.0, "donors in the whole record", ha="left", va="top",
            fontsize=FS_NUM, color=NOTE)
    bh, step = 1.9, 2.9
    y = 30.5
    for s, n in per_study.items():
        ax.add_patch(Rectangle((x, y), bw * 0.62 * n / per_study.max(), bh,
                               fc=BLUE_E, ec="none", alpha=.80, zorder=3))
        ax.text(x + bw * 0.62 * n / per_study.max() + 1.0, y + bh / 2, str(n),
                ha="left", va="center", fontsize=FS_TINY, color=NOTE)
        y -= step
    ax.text(x, 33.0, "donors per study", ha="left", va="bottom",
            fontsize=FS_TINY, color=NOTE)

    # ── 3. the model ────────────────────────────────────────────────────
    x = xs[2]
    heading(ax, x, TOP, "Model", "inductive bias, not scale", TEAL_E)
    ax.text(x, TOP - 7.0, "1.88M", ha="left", va="top",
            fontsize=11, fontweight="bold", color=TEAL_E)
    ax.text(x, TOP - 14.0, "parameters", ha="left", va="top",
            fontsize=FS_NUM, color=NOTE)
    # The ELAJ bar is a sliver and that IS the point, so its number sits
    # outside the bar; scFoundation's fills the column so its number goes
    # inside, in white. The first version put both outside and the 100M
    # label fell off the right edge of the figure.
    for i, (lab, v, c) in enumerate((("ELAJ", PARAMS_ELAJ, TEAL_E),
                                     ("scFoundation, the largest tested",
                                      PARAMS_FM, "#B9BEC5"))):
        yy = 27.0 - i * 9.5
        barw = bw * v / PARAMS_FM
        ax.add_patch(Rectangle((x, yy), barw, 5.2, fc=c, ec="none", zorder=3))
        ax.text(x, yy + 6.2, lab, ha="left", va="bottom", fontsize=FS_TINY,
                color=NOTE)
        if barw > bw * 0.35:
            ax.text(x + barw / 2, yy + 2.6, f"{v:.0f}M", ha="center",
                    va="center", fontsize=FS_NUM, color="#FFFFFF",
                    fontweight="bold", zorder=4)
        else:
            ax.text(x + barw + 1.4, yy + 2.6, f"{v:.2f}M", ha="left",
                    va="center", fontsize=FS_NUM, color=TEAL_E,
                    fontweight="bold", zorder=4)
    ax.text(x, 6.5, "44 pathway groups  ·  16 dimensions", ha="left",
            va="bottom", fontsize=FS_TINY, color=NOTE)

    # ── 4. the frontier, the real one ───────────────────────────────────
    x = xs[3]
    heading(ax, x, TOP, "Frontier", "measured, not assumed", AMB_E)
    D = collect()
    pts = []
    for mm in list(BASELINES) + list(FOUNDATION):
        g = D[mm]
        a = g.get(("cross-donor", "menstrual phase"))
        b = g.get(("knn-agreement", "patient_id"))
        if a and b:
            pts.append((float(b), float(a), False))
    for key in ("p1_dab168_kl1", "p1_dab168_kl30"):
        g = D[key]
        pts.append((float(g[("knn-agreement", "patient_id")]),
                    float(g[("cross-donor", "menstrual phase")]), True))
    px0, py0, pw, ph = x + 3.0, 14.0, bw - 5.0, 26.0
    X = [p[0] for p in pts]; Y = [p[1] for p in pts]
    sx, sy = (max(X) - min(X)), (max(Y) - min(Y))
    fx = lambda v: px0 + pw * (0.06 + 0.88 * (v - min(X)) / sx)
    fy = lambda v: py0 + ph * (0.08 + 0.84 * (v - min(Y)) / sy)
    ours = sorted([p for p in pts if p[2]])
    ax.plot([fx(p[0]) for p in ours], [fy(p[1]) for p in ours], "-",
            color=AMB_E, lw=1.2, alpha=.7, zorder=6)
    for bx, by, mine in pts:
        ax.scatter([fx(bx)], [fy(by)], s=17 if mine else 9, zorder=7,
                   c="#FFDDA6" if mine else "#FFFFFF",
                   edgecolors=AMB_E if mine else NOTE, linewidths=.8)
    ax.annotate("", xy=(px0, py0 + ph), xytext=(px0, py0),
                arrowprops=dict(arrowstyle="-|>", color=HAIR, lw=.7,
                                mutation_scale=6), zorder=5)
    ax.annotate("", xy=(px0 + pw, py0), xytext=(px0, py0),
                arrowprops=dict(arrowstyle="-|>", color=HAIR, lw=.7,
                                mutation_scale=6), zorder=5)
    ax.text(px0 + pw / 2, py0 - 1.6, "donor identity kept", ha="center",
            va="top", fontsize=FS_TINY, color=NOTE)
    ax.text(px0 - 1.8, py0 + ph / 2, "cycle kept", ha="center", va="center",
            rotation=90, fontsize=FS_TINY, color=NOTE)
    ax.text(x, 6.5, "11 arms retrained  ·  every result from a named point",
            ha="left", va="bottom", fontsize=FS_TINY, color=NOTE)

    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "panel_a_abstract.png",
                dpi=int(os.environ.get("FIGDPI", 600)))
    print(f"wrote {OUT / 'panel_a_abstract.png'}  ({W:.0f} x {H:.0f} mm)")


if __name__ == "__main__":
    main()
