#!/usr/bin/env python
"""Three candidate layouts for Figure 1a, stacked on one page for comparison.

AW, 11 November: panel a states the OBJECTIVE, not the problem. Both
reference figures do that. The three beats are collect -> compress -> check.

  A  the IBDex spine      sources -> harmonisation box -> composition + proof
  B  scattered to single  separate studies -> model -> one cloud
  C  a mix of the two

OPTION 2, the funnel, WAS BINNED BY AW and he was right: a wedge narrowing
through 15,496 genes, 44 groups and 16 dimensions is the architecture
diagram, which is panel b.

THE "BEFORE" CLOUD IN B AND C IS A STYLISED PLACEHOLDER, NOT DATA. Only the
ELAJ latents are dumped; no PCA or baseline embedding exists on disk. Drawn
as smooth ellipses rather than fake scatter so it cannot be mistaken for a
measurement. If B or C is chosen, that panel needs a real PCA embedding and
a UMAP over the same 400,000 cells.

Everything else is real: donor counts per study, corpus composition and the
frontier all come from the corpus and from table1.collect().
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
TEAL_F, TEAL_E = "#DCEFEC", "#2F8F88"
AMB_F,  AMB_E  = "#FFF3DE", "#D89120"
SC = ["#5BA3A0", "#4C78A8", "#E45756", "#54A24B", "#B279A2", "#F58518",
      "#2E5C8A", "#7B4FA0", "#FF9DA6", "#1B7A6B", "#8C2D3F"]

FS_H, FS_B, FS_T = 6.5, 5.5, 4.8
plt.rcParams.update({"font.family": "Arial", "text.color": INK})


def head(ax, x, y, t, sub, c):
    ax.text(x, y, t, ha="left", va="bottom", fontsize=FS_H,
            fontweight="bold", color=c)
    if sub:
        ax.text(x, y - 2.3, sub, ha="left", va="top", fontsize=FS_T, color=NOTE)


def arrow(ax, x0, x1, y, c="#B9BEC5", lw=2.2):
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="-|>", color=c, lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=8))


def model_box(ax, x, y, w, h, compact=False):
    """The model, as four pictograms. Never words where a picture will do."""
    ax.add_patch(FancyBboxPatch((x, y), w, h, "round,pad=0,rounding_size=1.5",
                                fc=BLUE_F, ec=BLUE_E, lw=.9, zorder=2))
    pw, ph = w * 0.78, 4.4
    ax.add_patch(FancyBboxPatch((x + (w - pw) / 2, y - ph / 2), pw, ph,
                                "round,pad=0,rounding_size=2.2",
                                fc=BLUE_E, ec=BLUE_E, lw=0, zorder=5))
    ax.text(x + w / 2, y + 0.05, "ELAJ", ha="center", va="center",
            fontsize=FS_B, color="#FFFFFF", fontweight="bold", zorder=6)
    n = 2 if compact else 4
    cw = w / n
    cy = y + h * (0.62 if not compact else 0.58)
    # 1. genes bundling into pathway groups
    cx = x + cw * 0.5
    for g, gc in enumerate(("#4C78A8", "#5BA3A0", "#B279A2")):
        for k in range(3):
            ax.add_patch(Circle((cx - 4.2 + g * 4.2 + (k % 2) * 1.1,
                                 cy + 1.6 - k * 1.1), .42, fc=gc, ec="none",
                                zorder=4))
    ax.text(cx, cy - 3.4, "44 pathway\ngroups", ha="center", va="top",
            fontsize=FS_T, color=NOTE, zorder=4, linespacing=1.3)
    # 2. the sentinel: a gene that was never measured
    cx = x + cw * 1.5 if not compact else x + cw * 1.5
    if not compact:
        for k in range(4):
            ax.add_patch(Circle((cx - 2.4 + k * 1.6, cy + 1.2), .42,
                                fc="#4C78A8" if k != 2 else "#FFFFFF",
                                ec="none" if k != 2 else GREY_E, lw=.6, zorder=4))
        ax.plot([cx + 0.8 - 2.4, cx + 0.8 - 2.4], [cy + 1.2, cy + 1.2], zorder=4)
        ax.text(cx, cy - 3.4, "never-measured\ngenes flagged", ha="center",
                va="top", fontsize=FS_T, color=NOTE, zorder=4, linespacing=1.3)
        # 3. per-study normalisation: two offset curves snapping together
        cx = x + cw * 2.5
        t = np.linspace(-1, 1, 60)
        for off, col, al in ((-0.45, GREY_E, .45), (0.45, GREY_E, .45), (0, BLUE_E, 1)):
            ax.plot(cx + t * 3.4 + off * 2.0, cy + 1.0 + np.exp(-(t * 2) ** 2) * 2.2,
                    color=col, lw=.8, alpha=al, zorder=4)
        ax.text(cx, cy - 3.4, "per-study\nnormalisation", ha="center", va="top",
                fontsize=FS_T, color=NOTE, zorder=4, linespacing=1.3)
    # 4. compression to sixteen
    cx = x + cw * (3.5 if not compact else 1.5)
    ax.add_patch(Rectangle((cx - 4.4, cy - 0.3), 3.0, 3.4, fc="#BBD2EC",
                           ec="none", zorder=4))
    for k in range(8):
        ax.add_patch(Circle((cx + 1.0 + (k % 4) * 1.15, cy + 2.2 - (k // 4) * 1.2),
                            .40, fc=AMB_E, ec="none", zorder=4))
    ax.text(cx, cy - 3.4, "16 numbers\nper cell", ha="center", va="top",
            fontsize=FS_T, color=NOTE, zorder=4, linespacing=1.3)


def frontier(ax, x, y, w, h, title=True):
    D = collect(); pts = []
    for m in list(BASELINES) + list(FOUNDATION):
        g = D[m]
        a = g.get(("cross-donor", "menstrual phase"))
        b = g.get(("knn-agreement", "patient_id"))
        if a and b:
            pts.append((float(b), float(a), False))
    for k in ("p1_dab168_kl1", "p1_dab168_kl30"):
        g = D[k]
        pts.append((float(g[("knn-agreement", "patient_id")]),
                    float(g[("cross-donor", "menstrual phase")]), True))
    X = [p[0] for p in pts]; Y = [p[1] for p in pts]
    fx = lambda v: x + w * (0.10 + 0.84 * (v - min(X)) / (max(X) - min(X)))
    fy = lambda v: y + h * (0.14 + 0.78 * (v - min(Y)) / (max(Y) - min(Y)))
    ours = sorted([p for p in pts if p[2]])
    ax.plot([fx(p[0]) for p in ours], [fy(p[1]) for p in ours], "-",
            color=AMB_E, lw=1.2, alpha=.7, zorder=6)
    for bx, by, mine in pts:
        ax.scatter([fx(bx)], [fy(by)], s=18 if mine else 9, zorder=7,
                   c=AMB_F if mine else "#FFFFFF",
                   edgecolors=AMB_E if mine else NOTE, linewidths=.8)
    ax.annotate("", xy=(x, y + h), xytext=(x, y),
                arrowprops=dict(arrowstyle="-|>", color=HAIR, lw=.7,
                                mutation_scale=6), zorder=5)
    ax.annotate("", xy=(x + w, y), xytext=(x, y),
                arrowprops=dict(arrowstyle="-|>", color=HAIR, lw=.7,
                                mutation_scale=6), zorder=5)
    ax.text(x + w / 2, y - 1.4, "donor identity kept", ha="center", va="top",
            fontsize=FS_T, color=NOTE)
    ax.text(x - 1.6, y + h / 2, "cycle kept", ha="center", va="center",
            rotation=90, fontsize=FS_T, color=NOTE)
    ax.text(fx(ours[-1][0]) + 1.6, fy(ours[-1][1]), "ELAJ", ha="left",
            va="center", fontsize=FS_T, color=AMB_E, fontweight="bold")


def study_tiles(ax, x, y, w, per_study):
    """Eleven studies, sized by donors. The scarcity needs no sentence."""
    mx = per_study.max(); step = 3.0
    yy = y
    for i, (s, n) in enumerate(per_study.items()):
        bw = w * 0.52 * n / mx
        ax.add_patch(Rectangle((x, yy), bw, 2.0, fc=SC[i % len(SC)],
                               ec="none", zorder=3))
        nm = STUDY_NAME.get(s, s)
        nm = nm.split()[0] + (nm[-1] if nm[-1] in "ab" else "")
        ax.text(x + bw + 1.0, yy + 1.0, f"{nm}  {n}",
                ha="left", va="center", fontsize=FS_T, color=NOTE)
        yy -= step
    return yy


def blobs_separate(ax, cx, cy, r):
    """STYLISED placeholder for an unintegrated space. Not data."""
    # Scattered irregularly, NOT on a ring. The first version placed them on
    # a circle, which reads as a decorative wreath and implies an ordering
    # that does not exist.
    rng = np.random.default_rng(11)
    placed = []
    for i in range(11):
        for _ in range(400):
            ex = cx + rng.uniform(-r, r) * 0.82
            ey = cy + rng.uniform(-r, r) * 0.82
            if all((ex - px) ** 2 + (ey - py) ** 2 > (r * 0.40) ** 2
                   for px, py in placed):
                placed.append((ex, ey)); break
        else:
            placed.append((ex, ey))
        ax.add_patch(Ellipse(placed[-1], r * 0.38, r * 0.26,
                             angle=float(rng.uniform(0, 180)),
                             fc=SC[i % len(SC)], ec="none", alpha=.85, zorder=3))


def blob_merged(ax, cx, cy, r, xy, studies, m):
    """The real ELAJ latent, coloured by study."""
    k = np.random.default_rng(3).choice(len(xy), 60_000, replace=False)
    p = xy[k]; s = m["study"].to_numpy()[k]
    p = p - p.mean(0); p = p / np.abs(p).max() * r
    for i, st in enumerate(studies):
        sel = s == st
        ax.scatter(cx + p[sel, 0], cy + p[sel, 1], s=.10, color=SC[i % len(SC)],
                   lw=0, rasterized=True, zorder=3)


def main() -> None:
    m = pd.read_csv(ROOT / f"Outputs/cells/{ARM}/metadata.csv.gz",
                    low_memory=False, usecols=["study", "patient_id",
                                               "disease_status", "tissue"])
    per_study = m.groupby("study").patient_id.nunique().sort_values(ascending=False)
    studies = list(m.study.value_counts().index)
    xy = np.load(ROOT / f"Outputs/analysis/umaps/{ARM}/_umap_cache/global_400000.npy")
    idx = np.sort(np.random.default_rng(24).choice(len(m), 400_000, replace=False))
    ms = m.iloc[idx].reset_index(drop=True)

    W, RH = 180.0, 62.0
    H = RH * 3 + 8
    fig = plt.figure(figsize=(W / 25.4, H / 25.4))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H)
    ax.axis("off")

    def band(i):
        return H - 4 - i * RH          # top of band i

    # ══ A ═══════════════════════════════════════════════════════════════
    y0 = band(0)
    ax.text(2, y0 - 1, "OPTION 1   the IBDex spine", fontsize=FS_H,
            fontweight="bold", color=INK, va="top")
    head(ax, 4, y0 - 9, "Collect", "every eligible study", GREY_E)
    study_tiles(ax, 4, y0 - 15, 46, per_study)
    arrow(ax, 52, 60, y0 - 31)
    head(ax, 62, y0 - 9, "Compress", "inductive bias, not scale", BLUE_E)
    model_box(ax, 62, y0 - 46, 62, 30)
    arrow(ax, 126, 134, y0 - 31)
    head(ax, 136, y0 - 9, "Check", "measured, not assumed", AMB_E)
    dis = m.disease_status.value_counts()
    cx = 136
    for k, c in zip(["eutopic", "control", "ectopic", "adenomyosis"],
                    ["#4C78A8", "#5BA3A0", "#E45756", "#B279A2"]):
        bw = 40 * dis[k] / len(m)
        ax.add_patch(Rectangle((cx, y0 - 20), bw, 4.0, fc=c, ec="none", zorder=3))
        if dis[k] / len(m) > .15:
            ax.text(cx + bw / 2, y0 - 18, f"{100*dis[k]/len(m):.0f}%", ha="center",
                    va="center", fontsize=FS_T, color="#FFFFFF", zorder=4)
        cx += bw
    ax.text(136, y0 - 15, "disease status", fontsize=FS_T, color=NOTE, va="bottom")
    frontier(ax, 140, y0 - 50, 34, 24)

    # ══ B ═══════════════════════════════════════════════════════════════
    y1 = band(1)
    ax.text(2, y1 - 1, "OPTION 3   scattered to single", fontsize=FS_H,
            fontweight="bold", color=INK, va="top")
    head(ax, 4, y1 - 9, "11 studies apart", "schematic placeholder", GREY_E)
    blobs_separate(ax, 28, y1 - 33, 20)
    arrow(ax, 52, 62, y1 - 33)
    head(ax, 64, y1 - 9, "ELAJ", "", BLUE_E)
    model_box(ax, 64, y1 - 46, 48, 28, compact=True)
    arrow(ax, 114, 124, y1 - 33)
    head(ax, 126, y1 - 9, "one representation", "studies intermixed", TEAL_E)
    blob_merged(ax, 146, y1 - 33, 17, xy, studies, ms)
    frontier(ax, 168, y1 - 46, 10, 22)

    # ══ C ═══════════════════════════════════════════════════════════════
    y2 = band(2)
    ax.text(2, y2 - 1, "MIX   tiles, then scattered to single", fontsize=FS_H,
            fontweight="bold", color=INK, va="top")
    head(ax, 4, y2 - 9, "Collect", "11 studies, 254 donors", GREY_E)
    study_tiles(ax, 4, y2 - 15, 34, per_study)
    blobs_separate(ax, 56, y2 - 32, 15)
    ax.text(56, y2 - 50, "apart", ha="center", fontsize=FS_T, color=NOTE)
    arrow(ax, 72, 80, y2 - 32)
    head(ax, 82, y2 - 9, "Compress", "inductive bias, not scale", BLUE_E)
    model_box(ax, 82, y2 - 45, 44, 28, compact=True)
    arrow(ax, 128, 136, y2 - 32)
    head(ax, 138, y2 - 9, "Check", "and it holds", AMB_E)
    blob_merged(ax, 149, y2 - 30, 11, xy, studies, ms)
    ax.text(149, y2 - 43, "together", ha="center", fontsize=FS_T, color=NOTE)
    frontier(ax, 164, y2 - 44, 13, 20)

    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "mock_fig1a_options.png",
                dpi=int(os.environ.get("FIGDPI", 300)))
    print(f"wrote {OUT / 'mock_fig1a_options.png'}  ({W:.0f} x {H:.0f} mm)")


if __name__ == "__main__":
    main()
