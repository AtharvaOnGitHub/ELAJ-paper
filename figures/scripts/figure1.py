#!/usr/bin/env python
"""Figure 1 — ELAJ as a model, and the main findings.

REBUILT 10 NOVEMBER against scGPT (Nat. Methods 21, 1470-1480) and
scFoundation (Nat. Methods 21, 1481-1491), whose figure conventions were
measured out of the published PDFs rather than guessed at.

  a  the architecture, one wide strip across the top
  b  frontier: cycle against donor recovery    c  against study separation
  d  UMAP by cell family                       e  UMAP by study

WHAT CHANGED AND WHY. The six-panel version was crowded, and AW was right
about the cause: it carried three different column structures at once and no
air anywhere. PRISMA has moved to Extended Data Figure 1, which is reporting
apparatus rather than a finding, leaving a clean 2x2 under panel a.

THE TYPE SCALE IS scGPT's, and it is three levels deep with nothing outside
it. Measured by character count across its figure pages: panel letters 9.3,
panel titles 6.5, secondary labels 5.5, the bulk of in-panel text 4.5. Note
the direction of the surprise: published Nature-family figures run SMALLER
than NMI's stated 5-7 pt, because that guidance governs submitted artwork and
typesetting reduces it. 5.5 pt is therefore generous, not risky, and it is
what AW's own panel a uses for its annotations.

FOUR CONVENTIONS TAKEN FROM scGPT, all of which the old version broke.
  * UMAPs carry no frame, no ticks and no box. Bare scatter on white.
  * A panel title sits ABOVE the panel on the letter's own line, regular
    weight beside the bold letter. What goes below a panel in scGPT is a
    condition label, not a title.
  * A categorical colouring gets a titled dot-list legend beside it. The old
    panel f coloured eleven studies and named none of them.
  * Blocks are separated by real space, not by the minimum that fits.

PANEL a IS AW'S OWN DRAWING, not drawn here, flattened onto white and
trimmed to its ink. At 3.87:1 it can only run full width: narrowed to two
thirds its type would fall to about 3.4 pt. That constraint sets the whole
layout, so panel a takes the top row and everything else is built beneath it.

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
import matplotlib.image as mpimg
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from table1 import collect, MANIFEST, BASELINES, FOUNDATION   # noqa: E402

ROOT = Path("/Users/atharvawaghmare/Endo research/ELAJ")
ARM = "p1_dab168_kl1"
HERE = Path(__file__).resolve().parents[1] / "pinned"
ARCH = HERE / "panel_a_architecture.png"

# ── palette ──────────────────────────────────────────────────────────────
# SAMPLED FROM PANEL a so the figure reads as one object. If AW redraws the
# architecture in a new scheme, this block is the only thing to change.
INK, SOFT, HAIR = "#2B3038", "#6F7681", "#C9CDD4"
AMBER = "#CC4E00"; AMBER_F = "#FFDDA6"       # the latent, and so ELAJ
TEAL = "#00A896"; BLUE = "#1071E5"
GREEN = "#008A0E"; PURPLE = "#BA23F6"; SALMON_F = "#F78D8D"; PERI = "#7D87FA"

# ── study display names ──────────────────────────────────────────────────
# THE CORPUS'S INTERNAL KEYS NAME THE WRONG AUTHOR FOR FOUR STUDIES, and the
# figure must not print them. The chain is checkable at both ends:
# `src/configs/data/study_platform.csv` maps each key to its accession, and
# Methods, Data availability maps each accession to its citation.
#
#   ferrero_2024  -> GSE247695     -> sarsenova2024metabolic
#   lin_2023      -> GSE214411     -> huang2023immune
#   wang_2022     -> GSE218044     -> chen2022adenomyosis
#   marecko_2024  -> E-MTAB-14039  -> mareckova2024heca   (missing "va")
#
# The keys are a pipeline artefact; the citations are the fact. Renaming the
# data would mean re-deriving everything keyed on it, so the map lives here.
STUDY_NAME = {
    "duempelmann_2026":     "Dümpelmann 2026",
    "ferrero_2024":         "Sarsenova 2024",
    "fonseca_2023":         "Fonseca 2023",
    "garcia_alonso_2021_a": "García-Alonso 2021a",
    "garcia_alonso_2021_b": "García-Alonso 2021b",
    "li_2025":              "Li 2025",
    "lin_2023":             "Huang 2023",
    "marecko_2024":         "Marečková 2024",
    "shih_2022":            "Shih 2022",
    "tan_2022":             "Tan 2022",
    "wang_2022":            "Chen 2022",
}

FAMILY_C = [TEAL, AMBER, BLUE, PURPLE]       # stromal, epi, endo, immune
STUDY_C = [TEAL, AMBER, BLUE, PURPLE, GREEN, SALMON_F, PERI, "#3A414A",
           "#E8B4B8", "#00806E", "#F2A74B", "#6B5BA6", "#9ACD32"]

# ── type scale, scGPT's, and nothing outside it ──────────────────────────
FS_LETTER, FS_TITLE, FS_BODY = 9.0, 6.5, 5.5
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": FS_BODY,
                     "text.color": INK, "axes.labelcolor": INK,
                     "xtick.color": SOFT, "ytick.color": SOFT,
                     "axes.edgecolor": HAIR, "axes.linewidth": .5,
                     "mathtext.fontset": "dejavusans"})


def head(ax, letter, title=None, dx=0.0):
    """scGPT's heading: bold letter, then the title on the same line."""
    ax.text(dx, 1.022, letter, transform=ax.transAxes, fontsize=FS_LETTER,
            fontweight="bold", va="bottom", ha="left")
    if title:
        ax.text(dx + 0.052, 1.028, title, transform=ax.transAxes,
                fontsize=FS_TITLE, va="bottom", ha="left", color=INK)


# ═════════════════════════════════════════════════════════════════════════
# b, c — the frontier over every method, with the Pareto front
# ═════════════════════════════════════════════════════════════════════════
def place_labels(ax, fig, pts):
    """Greedy placement scored on the label's FOOTPRINT, not its anchor.

    Two earlier versions failed the same way. The first took the first of
    four fixed offsets no earlier label had claimed, which let a label land
    on a DIFFERENT point. The second scored the anchor only, so a long name
    anchored just inside the axes still ran out of it and "Geneformer" sat
    on the x-axis in both panels. This one measures the box the text will
    occupy and rejects any candidate leaving the axes.
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
    chosen: dict[int, tuple] = {}
    for i in sorted(range(len(pts)), key=lambda i: -len(pts[i][2])):
        x, y, nm, ours = pts[i]
        px, py = norm[i]
        chars = 2.2 if ours else len(nm)
        w = chars * 0.55 * FS_BODY / aw_pt
        h = 1.15 * FS_BODY / ah_pt
        best, best_score = None, -1e9
        for dx, dy, ha, va in cands:
            cx, cy = px + dx / aw_pt, py + dy / ah_pt
            lx0 = cx if ha == "left" else cx - w if ha == "right" else cx - w / 2
            ly0 = cy if va == "bottom" else cy - h if va == "top" else cy - h / 2
            if not (-.01 <= lx0 and lx0 + w <= 1.01
                    and -.01 <= ly0 and ly0 + h <= 1.01):
                continue
            ccx, ccy = lx0 + w / 2, ly0 + h / 2
            dmin = min([(((ccx - ox) * aw_pt) ** 2
                         + ((ccy - oy) * ah_pt) ** 2) ** .5
                        for j, (ox, oy) in enumerate(norm) if j != i] or [999])
            lmin = min([max(abs(ccx - ox) * aw_pt - (w + ow) * aw_pt / 2,
                            abs(ccy - oy) * ah_pt - h * ah_pt)
                        for ox, oy, ow, _ in placed] or [999])
            score = min(dmin, 30) + 1.5 * min(lmin, 30)
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
                    ha=ha, va=va, fontsize=FS_BODY, clip_on=False,
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
        ax.scatter(x, y, s=36 if ours else 20, zorder=4,
                   c=AMBER_F if ours else "#FFFFFF",
                   edgecolors=AMBER if ours else SOFT,
                   linewidths=1.0 if ours else .7)

    ax.margins(x=.16, y=.15)
    ax.grid(True, lw=.35, color=HAIR, alpha=.6)
    ax.set_axisbelow(True)
    ax.set_xlabel(xlabel, fontsize=FS_BODY, labelpad=2.0)
    ax.tick_params(length=2, pad=2.0, labelsize=FS_BODY)
    ax.xaxis.set_major_locator(plt.MaxNLocator(5))
    ax.yaxis.set_major_locator(plt.MaxNLocator(6))
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    place_labels(ax, ax.figure, pts)


# ═════════════════════════════════════════════════════════════════════════
# d, e — the latent. No frame, no ticks: scGPT does this in every UMAP.
# ═════════════════════════════════════════════════════════════════════════
def umap(ax, lax, xy, series, order, colours, names=None):
    ax.scatter(xy[:, 0], xy[:, 1], s=.05, c="#E6E8EB", lw=0, rasterized=True)
    for lev, c in zip(order, colours):
        k = (series == lev).to_numpy()
        if k.any():
            ax.scatter(xy[k, 0], xy[k, 1], s=.05, color=c, lw=0,
                       rasterized=True)
    lo = np.percentile(xy, 0.15, axis=0); hi = np.percentile(xy, 99.85, axis=0)
    px, py = (hi - lo) * .02
    ax.set_xlim(lo[0] - px, hi[0] + px); ax.set_ylim(lo[1] - py, hi[1] + py)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

    # the titled dot-list beside the panel, scGPT's form
    # the dot-list beside the panel, scGPT's form. No title on it: the
    # panel heading already names the variable and repeating it reads as
    # two labels for one thing.
    lax.set_xlim(0, 1); lax.set_ylim(0, 1); lax.axis("off")
    n = len(order) + 1
    step = min(0.072, 0.94 / n)
    y = 0.5 + step * (n - 1) / 2
    for lev, c in list(zip(order, colours)) + [("unlabelled", "#E6E8EB")]:
        lax.scatter([0.035], [y], s=7, color=c, lw=0, clip_on=False)
        lax.text(0.12, y, (names or {}).get(lev, str(lev)),
                 fontsize=FS_BODY, va="center", ha="left", color=SOFT)
        y -= step


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
    L, R, T, B = 3.0, 2.0, 4.0, 4.0
    aw = W - L - R
    arch = mpimg.imread(ARCH)
    ah = aw * arch.shape[0] / arch.shape[1]      # panel a's own aspect, exactly
    GAP_A = 11.0                                 # air under panel a
    GAP_COL = 13.0                               # between the two columns
    GAP_ROW = 13.0                               # between the two plot rows
    cw = (aw - GAP_COL) / 2                      # 82 mm per column
    UW, ULG = 54.0, 3.0                          # UMAP square, then its legend
    bh, dh = 52.0, 54.0
    H = T + ah + GAP_A + bh + GAP_ROW + dh + B

    fig = plt.figure(figsize=(W / 25.4, H / 25.4))

    def mm(x, y, w, h):
        return fig.add_axes([x / W, 1 - (y + h) / H, w / W, h / H])

    y_a = T
    y_bc = y_a + ah + GAP_A
    y_de = y_bc + bh + GAP_ROW
    x2 = L + cw + GAP_COL

    ax_a = mm(L, y_a, aw, ah)
    ax_a.imshow(mpimg.imread(ARCH), interpolation="antialiased")
    ax_a.axis("off")

    # the y-axis label needs a gutter the UMAP row does not
    GUT = 9.0
    ax_b = mm(L + GUT, y_bc, cw - GUT, bh)
    ax_c = mm(x2 + GUT, y_bc, cw - GUT, bh)
    frontier(ax_b, D, "knn-agreement", "patient_id", "donor recovery")
    frontier(ax_c, D, "study-mixing", "all studies", "study separation")
    ax_b.set_ylabel("cross-donor cycle agreement", fontsize=FS_BODY,
                    labelpad=2.0)

    ax_d = mm(L, y_de, UW, dh);  lax_d = mm(L + UW + ULG, y_de, cw - UW - ULG, dh)
    ax_e = mm(x2, y_de, UW, dh); lax_e = mm(x2 + UW + ULG, y_de, cw - UW - ULG, dh)

    FAM = ["stromal", "epithelial", "endothelial", "immune"]
    umap(ax_d, lax_d, xy, m["cell family"], FAM, FAMILY_C)
    studies = sorted(m["study"].dropna().unique())
    umap(ax_e, lax_e, xy, m["study"], studies, STUDY_C[:len(studies)],
         names=STUDY_NAME)

    head(ax_a, "a", "The model")
    head(ax_b, "b", "Cycle against donor recovery", dx=-GUT / (cw - GUT))
    head(ax_c, "c", "Cycle against study separation", dx=-GUT / (cw - GUT))
    head(ax_d, "d", "Cell family")
    head(ax_e, "e", "Study")

    HERE.mkdir(parents=True, exist_ok=True)
    fig.savefig(HERE / "figure1.png", dpi=int(os.environ.get("FIGDPI", 600)))
    print(f"wrote {HERE / 'figure1.png'}  ({W:.0f} x {H:.1f} mm)")


if __name__ == "__main__":
    main()
