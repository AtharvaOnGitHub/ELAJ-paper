#!/usr/bin/env python
"""Figure 1 — ELAJ as a model, and the main findings.

REBUILT 10 NOVEMBER against scGPT (Nat. Methods 21, 1470-1480) and
scFoundation (Nat. Methods 21, 1481-1491), whose figure conventions were
measured out of the published PDFs rather than guessed at.

  a  the graphical abstract: data, the model, outcomes
  b  the architecture, AW's own drawing
  c  frontier: cycle against donor recovery
  d  UMAP by cell family

RESTRUCTURED 11 NOVEMBER, on AW's ruling once the paper's story settled.
Panel a is no longer the architecture: following scGPT's own Figure 1a, it
states what the paper DOES, and the architecture moves to b. Two panels
were cut outright. The study UMAP duplicated what Figure 4b already shows,
and the second frontier scatter, cycle against study separation, belongs
with the rest of the frontier in Figure 2. What is left is four panels that
each say something no other panel says.

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
trimmed to its ink. It can only run full width: at 3.24:1 its smallest type
is already 5.1 pt at 180 mm, so narrowing it to two thirds would put that
text near 3.4 pt, under NMI's floor. That constraint sets the whole layout,
so panel a takes the top row and everything else is built beneath it.

ITS TYPE IS MEASURED, NOT ASSUMED: headings 6.9 pt, text in shapes 6.5,
foot annotations 5.1, which is the scale the rest of this figure matches at
6.5 / 6.0 / 5.5. AW draws it in LucidChart at 11 / 10 / 8 pt; that tool
renders at 0.623 of its own point size once the export is placed at 180 mm.

THE FRONTIER PANELS READ THE TABLE'S OWN SOURCES. table1.collect() is
imported rather than copied, so a point here and a row there cannot come
from different runs.
"""
from __future__ import annotations
import os, sys
from pathlib import Path

# ARIAL THROUGHOUT, and it is a shared decision rather than a default.
# Panel a is drawn in LucidChart and the rest here, so one typeface has
# to span both. Arial ships on macOS as a .ttf LucidChart can import,
# matplotlib resolves it to the same file, and it is the grotesque the
# Nature family sets its own figures in. It also carries every mark this
# paper needs: Dümpelmann, Marečková, García-Alonso, lambda, subscripts.
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
ABSTRACT = HERE / "panel_a_abstract.png"
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

# Cell families: Okabe-Ito. Four hues designed to stay separable under
# every common colour-vision deficiency, and they land almost exactly on
# panel a's own hues anyway: its encoder blue, its decoder teal-green and
# its latent amber, plus the vermillion AW asked for. Blue to the largest
# family so the biggest area carries the calmest colour.
FAMILY_C = ["#0072B2",   # stromal      blue
            "#D55E00",   # epithelial   vermillion / burnt sienna
            "#009E73",   # endothelial  bluish green
            "#E69F00"]   # immune       amber

# Studies: distinct hues, with the muddy band removed.
#
# THREE ATTEMPTS, and each failure said something different. Alphabetical
# assignment handed the largest study the darkest ink and the panel read as
# one dark mass, which is the opposite of what e claims. Tol's muted scheme
# fixed the ordering but carries sand and olive, and yellow overplotted
# against everything averages to brown; AW: "very closely resembles vomit".
# Going cool-dominant killed the mud but made eleven studies look like one
# colour, which defeats having a legend at all.
#
# What was actually wrong was the yellow-olive-brown band, not the hue
# spread. So: eleven well-separated hues around the wheel with nothing
# between yellow and olive, ordered so the largest studies take the clean
# mid-tones and the smallest take the deep ones.
STUDY_C = ["#5BA3A0",   # teal         (largest study)
           "#4C78A8",   # blue
           "#E45756",   # red
           "#54A24B",   # green
           "#B279A2",   # mauve
           "#F58518",   # orange
           "#2E5C8A",   # navy
           "#7B4FA0",   # purple
           "#FF9DA6",   # pink
           "#1B7A6B",   # deep teal
           "#8C2D3F"]   # wine         (smallest study)

GREY_PT = "#DCE0E4"      # cells with no label, in both panels

# ── type scale, scGPT's, and nothing outside it ──────────────────────────
FS_LETTER, FS_TITLE, FS_BODY = 10.0, 6.5, 5.5
plt.rcParams.update({"font.family": "Arial", "font.size": FS_BODY,
                     "text.color": INK, "axes.labelcolor": INK,
                     "xtick.color": SOFT, "ytick.color": SOFT,
                     "axes.edgecolor": HAIR, "axes.linewidth": .5,
                     "mathtext.fontset": "custom",
                     "mathtext.rm": "Arial",
                     "mathtext.it": "Arial:italic",
                     "mathtext.bf": "Arial:bold"})


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
    global FRONTIER_PTS
    FRONTIER_PTS = pts

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
    ax.scatter(xy[:, 0], xy[:, 1], s=.05, c=GREY_PT, lw=0, rasterized=True)
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
    n = len(order) + (1 if series.isna().any() else 0)
    step = min(0.072, 0.94 / n)
    y = 0.5 + step * (n - 1) / 2
    # "unlabelled" only where such cells exist. Every cell has a study, so
    # claiming the category in e invented a class with nothing in it; cell
    # family genuinely has unlabelled cells and keeps it.
    entries = list(zip(order, colours))
    if bool(series.isna().any()):
        entries.append(("unlabelled", GREY_PT))
    for lev, c in entries:
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
    L, R, T, B = 3.0, 2.0, 4.0, 8.0
    #                         ^ panel c spends ~6 mm below its axes on
    #                         tick labels and the x-label. At B=4 the
    #                         x-label was clipped by the canvas edge.
    aw = W - L - R
    absm = mpimg.imread(ABSTRACT)
    abh = aw * absm.shape[0] / absm.shape[1]     # each panel's own aspect,
    arch = mpimg.imread(ARCH)                    # exactly, or imshow letterboxes
    ah = aw * arch.shape[0] / arch.shape[1]
    GAP_A = 8.0                                  # air under panel a
    #       ^ less than the other gaps: the drawing already carries
    #       its own foot annotations and their whitespace.
    GAP_COL = 13.0                               # between the two columns
    GAP_ROW = 13.0                               # between the two plot rows
    cw = (aw - GAP_COL) / 2                      # 82 mm per column
    UW, ULG = 54.0, 3.0                          # UMAP square, then its legend
    ph = 54.0                                    # the plot row
    H = T + abh + GAP_A + ah + GAP_ROW + ph + B

    fig = plt.figure(figsize=(W / 25.4, H / 25.4))

    def mm(x, y, w, h):
        return fig.add_axes([x / W, 1 - (y + h) / H, w / W, h / H])

    y_a = T
    y_b = y_a + abh + GAP_A
    y_cd = y_b + ah + GAP_ROW
    x2 = L + cw + GAP_COL

    ax_a = mm(L, y_a, aw, abh)
    # interpolation "none" stops the PDF resampling the image to 100 dpi
    ax_a.imshow(absm, interpolation="none"); ax_a.axis("off")
    ax_b = mm(L, y_b, aw, ah)
    ax_b.imshow(arch, interpolation="none"); ax_b.axis("off")

    # the frontier's y-axis label needs a gutter the UMAP does not
    GUT = 9.0
    ax_c = mm(L + GUT, y_cd, cw - GUT, ph)
    frontier(ax_c, D, "knn-agreement", "patient_id", "donor recovery")
    ax_c.set_ylabel("cross-donor cycle agreement", fontsize=FS_BODY,
                    labelpad=2.0)

    ax_d = mm(x2, y_cd, UW, ph)
    lax_d = mm(x2 + UW + ULG, y_cd, cw - UW - ULG, ph)
    FAM = ["stromal", "epithelial", "endothelial", "immune"]
    umap(ax_d, lax_d, xy, m["cell family"], FAM, FAMILY_C)

    # neither a nor b takes a title: both drawings carry their own headings
    head(ax_a, "a")
    head(ax_b, "b")
    head(ax_c, "c", "Cycle against donor recovery", dx=-GUT / (cw - GUT))
    head(ax_d, "d", "Cell family")

    # the clipped x-label was invisible until a reader found it, so it is
    # now a build failure rather than a defect someone has to spot
    fig.canvas.draw()
    for ax, what in ((ax_c, "panel c x-label"),):
        bb = ax.xaxis.label.get_window_extent()
        assert bb.y0 >= 0, f"{what} is clipped {-bb.y0:.1f} px off the canvas"

    HERE.mkdir(parents=True, exist_ok=True)
    fig.savefig(HERE / "figure1.png", dpi=int(os.environ.get("FIGDPI", 600)))
    # PDF: panel a goes in as its own vector PDF, not as a picture of it.
    # Hide the raster copy, save, then place panel_a_abstract.pdf into the
    # same box. dpi sets the rasterised UMAP layer.
    VEC_A = HERE / "panel_a_abstract.pdf"
    if VEC_A.exists():
        import pymupdf
        box = ax_a.get_position()                      # figure fraction
        ax_a.set_visible(False)
        fig.savefig(HERE / "figure1.pdf", dpi=int(os.environ.get("FIGDPI", 600)))
        ax_a.set_visible(True)
        doc = pymupdf.open(HERE / "figure1.pdf"); pg = doc[0]; R = pg.rect
        rect = pymupdf.Rect(box.x0 * R.width, (1 - box.y1) * R.height, box.x1 * R.width, (1 - box.y0) * R.height)
        src = pymupdf.open(VEC_A)
        pg.show_pdf_page(rect, src, 0, keep_proportion=True)
        doc.save(HERE / "figure1.tmp.pdf", garbage=3, deflate=True); doc.close()
        os.replace(HERE / "figure1.tmp.pdf", HERE / "figure1.pdf")
    else:
        fig.savefig(HERE / "figure1.pdf", dpi=int(os.environ.get("FIGDPI", 600)))   # NMI: vector
    import pandas as _pd
    _src = Path("/Users/atharvawaghmare/Endo research/ELAJ/Outputs/supplementary/source_data"); _src.mkdir(parents=True, exist_ok=True)     # NMI Source Data
    with _pd.ExcelWriter(_src / "Figure1_source_data.xlsx") as xw:
        _g = meta.groupby("study").agg(donors=("patient_id", "nunique"), cells=("patient_id", "size"))
        _g.to_excel(xw, sheet_name="a_studies")
        meta.groupby("disease_status").size().rename("cells").to_frame().to_excel(xw, sheet_name="a_disease_status")
        _pd.DataFrame(FRONTIER_PTS, columns=["donor_recovery", "cross_donor_cycle_agreement", "representation",
                                             "is_elaj"]).to_excel(xw, sheet_name="c", index=False)
        _pd.DataFrame({"umap_1": xy[:, 0], "umap_2": xy[:, 1], "cell_family": m["cell family"].to_numpy()}
                      ).to_excel(xw, sheet_name="d", index=False)
    print(f"wrote {HERE / 'figure1.png'}  ({W:.0f} x {H:.1f} mm)")


if __name__ == "__main__":
    main()
