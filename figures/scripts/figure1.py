#!/usr/bin/env python
"""Figure 1 — ELAJ as a model, and the main findings.

LAYOUT FROM AW'S SKETCH, 7 November 2026, rebuilt 10 November.
  a  the architecture, one wide strip across the top
  b  PRISMA, a tall column down the left
  c  frontier: cycle against donor recovery        d  against study separation
  e  UMAP by cell family                           f  UMAP by study

PANEL a IS AW'S OWN DRAWING, not drawn here. `panel_a_architecture.png` is
his ELAJ-2 export, flattened onto white and trimmed to its ink. Measured at
3,274 px it carries 462 dpi at 180 mm and its type runs 5.2 to 6.4 pt, so it
sits inside NMI's 300 dpi and 5-7 pt. It has NO headroom below 180 mm: at
100 mm its smallest labels would fall to about 3 pt. The panel therefore
takes the full text width and the rest of the figure is built around it.

THE PALETTE IS PANEL a's, sampled from the PNG rather than guessed, so the
figure reads as one object. Latent amber carries ELAJ everywhere it appears;
the four head colours carry the cell families; the DAB salmon carries PRISMA
exclusions and the DSBN periwinkle the stage spine.

LAYOUT IS EXPLICIT, IN MILLIMETRES. GridSpec's hspace is a fraction of the
mean axes height, which makes "4 mm of air under panel a" unexpressible when
rows differ in height. Every axes below is placed by `mm()` instead, so the
gaps are the numbers written down and panel a's axes matches its image
aspect exactly, which is what stops imshow letterboxing it.

PRISMA COUNTS CORRECTED. The thesis diagram is from the r-series era and
ends at twelve included studies; the corpus has eleven. The split is
derived from Data availability rather than guessed: seven GEO accessions,
one ArrayExpress and two CELLxGENE came through the API branch, and
CNP0006183 (li et al.) through the hand search of CNGBdb.

THE FRONTIER PANELS READ THE TABLE'S OWN SOURCES. table1.collect() is
imported rather than copied, so a point here and a row there cannot come
from different runs.

NOTE ON TYPE SIZE. Everything is sized for 180 mm, NMI's full text width.
Our own preamble is a4 with 25 mm margins, so \\linewidth is 160 mm and the
local PDF renders this at 89%. Nothing here is set below 5.6 pt, which
still clears 5 pt after that reduction.
"""
from __future__ import annotations
import os, sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from table1 import collect, MANIFEST, BASELINES, FOUNDATION   # noqa: E402

ROOT = Path("/Users/atharvawaghmare/Endo research/ELAJ")
ARM = "p1_dab168_kl1"
HERE = Path(__file__).resolve().parents[1] / "pinned"
ARCH = HERE / "panel_a_architecture.png"

# ── palette, sampled from panel a ────────────────────────────────────────
INK, SOFT, HAIR = "#2B3038", "#6F7681", "#C9CDD4"
AMBER,  AMBER_F  = "#CC4E00", "#FFDDA6"      # the latent, and so ELAJ
TEAL,   TEAL_F   = "#008573", "#00C2A8"      # the encoder path
BLUE,   BLUE_F   = "#1071E5", "#CFE4FF"      # reconstruction
GREEN,  GREEN_F  = "#008A0E", "#C3F7C8"      # ECS
PURPLE, PURPLE_F = "#BA23F6", "#F4D9FF"      # phase
SALMON, SALMON_F = "#825252", "#F78D8D"      # DAB, and so exclusions
PERI,   PERI_F   = "#7D87FA", "#C2C6FA"      # DSBN, and so the stage spine

FAMILY_C = [TEAL_F, AMBER, BLUE, PURPLE]     # stromal, epi, endo, immune
STUDY_C = [TEAL_F, AMBER, BLUE, PURPLE, GREEN, SALMON_F, PERI, "#3A414A",
           "#E8B4B8", "#00806E", "#F2A74B", "#6B5BA6", "#9ACD32"]

FS_MIN = 5.6                                  # 5 pt after the 89% reduction
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": FS_MIN,
                     "text.color": INK, "axes.labelcolor": INK,
                     "xtick.color": SOFT, "ytick.color": SOFT,
                     "axes.edgecolor": HAIR, "axes.linewidth": .5,
                     "mathtext.fontset": "dejavusans"})


def bf(s) -> str:
    """A number in bold, inline. AW: every n and every count is bold."""
    return r"$\mathbf{" + str(s).replace(",", "{,}") + r"}$"


# ═════════════════════════════════════════════════════════════════════════
# a — AW's architecture drawing, placed rather than redrawn
# ═════════════════════════════════════════════════════════════════════════
def panel_a(ax):
    ax.imshow(mpimg.imread(ARCH), interpolation="antialiased")
    ax.axis("off")


# ═════════════════════════════════════════════════════════════════════════
# b — PRISMA, in the PRISMA 2020 grammar
# ═════════════════════════════════════════════════════════════════════════
# The convention carries meaning: an amber bar names the identification
# route, a spine names the three stages, the main flow runs straight down,
# and exclusions branch sideways. A reader who has seen one PRISMA reads
# this one without the legend.
#
# ONE FLOW RATHER THAN TWO, because the thesis's parallel columns need four
# sub-columns and do not fit a portrait panel legibly. The arithmetic
# reconciles exactly: 455 + 98 identified, less 98 duplicates, 42 further
# deposits and the 58 manual records the APIs had already returned, leaves
# 355 screened; 293 excluded leaves 62 sought and assessed; 39 not single
# cell and 12 for other reasons leaves 11.
def tbox(ax, x, y, w, h, label, fc, ec, fs=FS_MIN, lw=.6, weight=None, tc=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, "round,pad=0,rounding_size=0.8",
                                fc=fc, ec=ec, lw=lw, zorder=2))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
            fontsize=fs, zorder=3, linespacing=1.3,
            color=tc or INK, fontweight=weight or "normal")


def arrow(ax, x0, y0, x1, y1, c=SOFT, lw=.6, rad=0.0):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), zorder=1,
                arrowprops=dict(arrowstyle="-|>", color=c, lw=lw,
                                shrinkA=0, shrinkB=0,
                                connectionstyle=f"arc3,rad={rad}",
                                mutation_scale=6))


def panel_b(ax):
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    MX, MW, EX, EW = 10.0, 42.0, 57.0, 42.0

    tbox(ax, MX, 94.4, MW + EW + 2.0, 5.0, "Database APIs and manual search",
         AMBER_F, AMBER, fs=FS_MIN, weight="bold", tc="#8A4000")

    # rows: (bottom, height, main text, exclusion text)
    rows = [(78.5, 12.5,
             "Records identified\nDatabase APIs  " + bf(455) +
             "\nCNGBdb  " + bf(98),
             "Records removed\nbefore screening\nDuplicates  " + bf(98) +
             "\nFurther deposits  " + bf(42) +
             "\nAlready found  " + bf(58)),
            (62.0, 9.0, "Records screened\n" + bf("n = 355"),
                        "Records excluded\n" + bf("n = 293")),
            (47.0, 9.0, "Reports sought\n" + bf("n = 62"),
                        "Reports not retrieved\n" + bf("n = 0")),
            (29.5, 11.5, "Reports assessed\nfor eligibility\n" + bf("n = 62"),
                         "Reports excluded\nNot single cell  " + bf(39) +
                         "\nOther reasons  " + bf(12))]
    for y, h, mt, et in rows:
        tbox(ax, MX, y, MW, h, mt, "#FFFFFF", INK)
        tbox(ax, EX, y, EW, h, et, SALMON_F, SALMON)
        arrow(ax, MX + MW, y + h / 2, EX, y + h / 2, c=SALMON)

    tbox(ax, MX, 8.5, MW + 24.0, 13.0,
         bf(11) + " studies included\n" + bf("1,577,728") + " cells\n" +
         bf(254) + " donors\n" + bf(6) + " anatomical sites",
         AMBER_F, AMBER, fs=FS_MIN, weight="bold")

    # the three-stage spine, keyed to the rows it spans
    for y0, y1, lab in ((78.0, 93.0, "Identification"),
                        (29.0, 72.0, "Screening"),
                        (8.0, 22.0, "Included")):
        tbox(ax, 1.5, y0, 5.2, y1 - y0, "", PERI_F, PERI)
        ax.text(4.1, (y0 + y1) / 2, lab, ha="center", va="center",
                rotation=90, fontsize=FS_MIN, color="#3B43A8", weight="bold")

    x = MX + MW / 2
    for a, b in ((78.5, 71.4), (62.0, 56.4), (47.0, 41.4), (29.5, 22.0)):
        arrow(ax, x, a, x, b, c=INK)


# ═════════════════════════════════════════════════════════════════════════
# c, d — the frontier over every method, with the Pareto front
# ═════════════════════════════════════════════════════════════════════════
def place_labels(ax, fig, pts):
    """Greedy label placement, scored on the label's FOOTPRINT.

    Two earlier versions failed the same way. The first took the first of
    four fixed offsets no earlier label had claimed, which let a label land
    on a DIFFERENT point. The second scored the anchor only, so a long name
    anchored just inside the axes still ran out of it: "Geneformer" sat on
    the x-axis in both panels. This one measures the text box the label will
    actually occupy and rejects any candidate whose box leaves the axes, so
    a point near an edge is labelled inwards instead.
    """
    x0, x1 = ax.get_xlim(); y0, y1 = ax.get_ylim()
    sx, sy = (x1 - x0) or 1.0, (y1 - y0) or 1.0
    pos = ax.get_position()
    aw_pt = pos.width * fig.get_figwidth() * 72.0
    ah_pt = pos.height * fig.get_figheight() * 72.0
    norm = [((p[0] - x0) / sx, (p[1] - y0) / sy) for p in pts]

    cands = [(0, 6.5, "center", "bottom"), (0, -6.5, "center", "top"),
             (6.0, 0, "left", "center"), (-6.0, 0, "right", "center"),
             (4.8, 4.8, "left", "bottom"), (-4.8, 4.8, "right", "bottom"),
             (4.8, -4.8, "left", "top"), (-4.8, -4.8, "right", "top"),
             (0, 11.0, "center", "bottom"), (0, -11.0, "center", "top")]
    placed: list[tuple[float, float, float, float]] = []
    order = sorted(range(len(pts)), key=lambda i: -len(pts[i][2]))
    chosen: dict[int, tuple] = {}
    for i in order:
        x, y, nm, ours = pts[i]
        px, py = norm[i]
        # DejaVu Sans at this size averages ~0.55 em per character; the
        # subscripted B labels render narrower than their source string.
        chars = 2.2 if ours else len(nm)
        w = chars * 0.55 * FS_MIN / aw_pt
        h = 1.15 * FS_MIN / ah_pt
        best, best_score = None, -1e9
        for dx, dy, ha, va in cands:
            cx, cy = px + dx / aw_pt, py + dy / ah_pt
            lx0 = cx if ha == "left" else cx - w if ha == "right" else cx - w / 2
            ly0 = cy if va == "bottom" else cy - h if va == "top" else cy - h / 2
            lx1, ly1 = lx0 + w, ly0 + h
            if not (-.01 <= lx0 and lx1 <= 1.01 and -.01 <= ly0 and ly1 <= 1.01):
                continue
            ccx, ccy = (lx0 + lx1) / 2, (ly0 + ly1) / 2
            dmin = min([(((ccx - ox) * aw_pt) ** 2 + ((ccy - oy) * ah_pt) ** 2) ** .5
                        for j, (ox, oy) in enumerate(norm) if j != i] or [999])
            lmin = min([max(abs(ccx - ox) * aw_pt - (w * aw_pt + ow * aw_pt) / 2,
                            abs(ccy - oy) * ah_pt - h * ah_pt)
                        for ox, oy, ow, _ in placed] or [999])
            score = min(dmin, 26) + 1.5 * min(lmin, 26)
            if score > best_score:
                best_score, best = score, (dx, dy, ha, va, lx0, ly0)
        if best is None:
            best = (0, 6.5, "center", "bottom", px, py)
        dx, dy, ha, va, lx0, ly0 = best
        placed.append((lx0 + w / 2, ly0 + h / 2, w, h))
        chosen[i] = (dx, dy, ha, va)

    for i, (x, y, nm, ours) in enumerate(pts):
        dx, dy, ha, va = chosen[i]
        ax.annotate(nm, (x, y), textcoords="offset points", xytext=(dx, dy),
                    ha=ha, va=va, fontsize=FS_MIN, clip_on=False,
                    color=AMBER if ours else SOFT,
                    fontweight="bold" if ours else "normal")


def frontier(ax, D, cost_test, cost_label, xlabel):
    pts = []
    for m in list(BASELINES) + list(FOUNDATION):
        g = D[m]
        y = g.get(("cross-donor", "menstrual phase"))
        x = g.get((cost_test, cost_label))
        if y and x:
            pts.append((float(x), float(y), MANIFEST[m][3], False))
    for key, nm in (("p1_dab168_kl1", "B$_{hi}$"),
                    ("p1_dab168_kl30", "B$_{lo}$")):
        g = D[key]
        pts.append((float(g[(cost_test, cost_label)]),
                    float(g[("cross-donor", "menstrual phase")]), nm, True))

    front = sorted(p for p in pts
                   if not any(q[0] <= p[0] and q[1] >= p[1] and q[:2] != p[:2]
                              for q in pts))
    ax.plot([p[0] for p in front], [p[1] for p in front], "-",
            color=AMBER, lw=1.1, alpha=.5, zorder=2)
    for x, y, nm, ours in pts:
        ax.scatter(x, y, s=34 if ours else 20, zorder=4,
                   c=AMBER_F if ours else "#FFFFFF",
                   edgecolors=AMBER if ours else SOFT,
                   linewidths=1.0 if ours else .7)

    ax.margins(x=.19, y=.17)
    ax.grid(True, lw=.35, color=HAIR, alpha=.65)
    ax.set_axisbelow(True)
    ax.set_xlabel(xlabel, fontsize=FS_MIN + .4, labelpad=1.5)
    ax.tick_params(length=2, pad=1.5, labelsize=FS_MIN)
    ax.xaxis.set_major_locator(plt.MaxNLocator(5))
    ax.yaxis.set_major_locator(plt.MaxNLocator(6))
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    place_labels(ax, ax.figure, pts)


# ═════════════════════════════════════════════════════════════════════════
# e, f — the latent
# ═════════════════════════════════════════════════════════════════════════
def umap(ax, xy, series, order, colours, title):
    ax.scatter(xy[:, 0], xy[:, 1], s=.05, c="#E6E8EB", lw=0, rasterized=True)
    for lev, c in zip(order, colours):
        k = (series == lev).to_numpy()
        if k.any():
            ax.scatter(xy[k, 0], xy[k, 1], s=.05, color=c, lw=0,
                       rasterized=True)
    # crop to the cloud rather than to stray outliers, which is most of the
    # white space these panels used to carry
    lo = np.percentile(xy, 0.15, axis=0); hi = np.percentile(xy, 99.85, axis=0)
    padx = (hi[0] - lo[0]) * .02; pady = (hi[1] - lo[1]) * .02
    ax.set_xlim(lo[0] - padx, hi[0] + padx)
    ax.set_ylim(lo[1] - pady, hi[1] + pady)
    ax.set_title(title, fontsize=FS_MIN + .4, pad=2.0)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color(HAIR)


# ═════════════════════════════════════════════════════════════════════════
def main() -> None:
    D = collect()
    xy = np.load(ROOT /
                 f"Outputs/analysis/umaps/{ARM}/_umap_cache/global_400000.npy")
    meta = pd.read_csv(ROOT / f"Outputs/cells/{ARM}/metadata.csv.gz",
                       low_memory=False)
    idx = np.sort(np.random.default_rng(24).choice(len(meta), 400_000,
                                                   replace=False))
    m = meta.iloc[idx].reset_index(drop=True)
    assert len(m) == len(xy)

    # ── layout, every number a millimetre ────────────────────────────────
    W = 180.0
    L, R, T, B = 2.5, 2.0, 2.5, 3.5
    aw = W - L - R                                   # panel a, full width
    arch = mpimg.imread(ARCH)
    ah = aw * arch.shape[0] / arch.shape[1]          # its own aspect, exactly
    GAP_A = 3.5                                      # air under panel a
    BW, GAP_B = 56.0, 11.0                           # PRISMA column, then air
    #           ^ GAP_B carries c's y-axis label and its tick labels. At
    #           5.5 mm the label printed on top of panel b's exclusions.
    GAP_C = 6.5                                      # between c|d and e|f
    GAP_R = 12.5                                     # between the two rows
    #       ^ holds c/d's xlabel AND e/f's title, which collided at 9 mm.
    cw = (aw - BW - GAP_B - GAP_C) / 2
    ch, eh = 48.0, 46.0
    H = T + ah + GAP_A + ch + GAP_R + eh + B

    def mm(x, y, w, h):
        """Axes from millimetres, measured from the top left."""
        return fig.add_axes([x / W, 1 - (y + h) / H, w / W, h / H])

    fig = plt.figure(figsize=(W / 25.4, H / 25.4))
    y_a = T
    y_cd = y_a + ah + GAP_A
    y_ef = y_cd + ch + GAP_R

    ax_a = mm(L, y_a, aw, ah);                      panel_a(ax_a)
    ax_b = mm(L, y_cd, BW, ch + GAP_R + eh);        panel_b(ax_b)
    ax_c = mm(L + BW + GAP_B, y_cd, cw, ch)
    ax_d = mm(L + BW + GAP_B + cw + GAP_C, y_cd, cw, ch)
    ax_e = mm(L + BW + GAP_B, y_ef, cw, eh)
    ax_f = mm(L + BW + GAP_B + cw + GAP_C, y_ef, cw, eh)

    frontier(ax_c, D, "knn-agreement", "patient_id", "donor recovery")
    frontier(ax_d, D, "study-mixing", "all studies", "study separation")
    ax_c.set_ylabel("cross-donor cycle agreement", fontsize=FS_MIN + .4,
                    labelpad=1.5)

    FAM = ["stromal", "epithelial", "endothelial", "immune"]
    umap(ax_e, xy, m["cell family"], FAM, FAMILY_C, "cell family")
    studies = sorted(m["study"].dropna().unique())
    umap(ax_f, xy, m["study"], studies, STUDY_C[:len(studies)], "study")

    for ax, lab, dx in ((ax_a, "a", -.004), (ax_b, "b", -.012),
                        (ax_c, "c", -.10), (ax_d, "d", -.10),
                        (ax_e, "e", -.045), (ax_f, "f", -.045)):
        ax.text(dx, 1.012, lab, transform=ax.transAxes, fontsize=8.0,
                fontweight="bold", va="bottom", ha="left")

    HERE.mkdir(parents=True, exist_ok=True)
    fig.savefig(HERE / "figure1.png", dpi=int(os.environ.get("FIGDPI", 600)))
    print(f"wrote {HERE / 'figure1.png'}  ({W:.0f} x {H:.1f} mm)")


if __name__ == "__main__":
    main()
