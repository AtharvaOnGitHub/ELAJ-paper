"""Supplementary figures and tables for Notes 2 to 8, every number read from a file.

    /Users/atharvawaghmare/miniconda3/envs/elaj/bin/python figures/scripts/supp_figures.py
    ... --only scib,transfer          a subset, by group name
    ... --no-umaps                    skip the forty-four UMAP panels

TWO OUTPUT TIERS, and the split is deliberate.

  Outputs/supplementary/figures_explore/   EVERY figure this script draws.
                                           Exploratory, single panels, outside
                                           git, about 60 MB with the UMAPs.
  supplementary/figures/                   the figures a Note actually cites,
                                           copied there by name.
  supplementary/tables/                    LaTeX tabular fragments the Notes
                                           \\input, so a number in a Note's
                                           table is never typed.

AW, 14 November: "I recommend NOT doing panels yet. We can group figures into
multi-panel diagrams later. This exercise is exploratory." So one claim per
file, no panel letters, and the register from figure1.py: Arial, scGPT's type
scale, the Okabe-Ito family palette and the eleven-hue study palette.

THE SOURCES ARE THE AUDIT'S SOURCES. Benchmark rows come through
table1.collect(), which reads audit_numbers.py's manifest by exact key, so a
value here and the same value in Table 1 cannot come from different files.
The three things read from markdown rather than CSV are declared where they
are read: the a-series and p-series registered prediction bands, and the
seven-sample overlap table from the donor-overlap audit.

NOTHING HERE IS A NEW EXPERIMENT. Every statistic is either a file's own cell
or a summary over one file's rows (a range, a Spearman across methods, a
histogram), which is the same licence the rho = +0.721 asymmetry already has.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

sys.path.insert(0, str(Path(__file__).resolve().parent))
import table1                                                     # noqa: E402
from figure1 import STUDY_NAME, FAMILY_C, STUDY_C, INK, SOFT, HAIR  # noqa: E402

ROOT = Path("/Users/atharvawaghmare/Endo research/ELAJ")
PAPER = Path(__file__).resolve().parents[2]
OUT = ROOT / "Outputs" / "supplementary"
EXPLORE = OUT / "figures_explore"
FIG = PAPER / "supplementary" / "figures"
TAB = PAPER / "supplementary" / "tables"
BENCH = ROOT / "Outputs" / "Benchmarks"
CELLS = ROOT / "Outputs" / "cells"
CLAIMS = ROOT / "axw1008" / "docs" / "paper"
ARM = "p1_dab168_kl1"
MM = 1 / 25.4
DPI = 200

# NMI'S 5 pt FLOOR IS ON THE PLACED FIGURE, NOT THE AUTHORED ONE.
# FS_LEG was being written as 4.2 to 4.8 by eye, which renders below the
# floor even at 1:1, and check_figure_scale.py now fails the build if a
# figure is placed small enough to take FS_LEG under 5 pt as well.
FS_TITLE, FS_BODY, FS_LEG = 6.5, 5.5, 5.2
plt.rcParams.update({"font.family": "Arial", "font.size": FS_BODY,
                     "text.color": INK, "axes.labelcolor": INK,
                     "xtick.color": SOFT, "ytick.color": SOFT,
                     "axes.edgecolor": HAIR, "axes.linewidth": .5,
                     "xtick.major.width": .5, "ytick.major.width": .5,
                     "xtick.major.size": 2, "ytick.major.size": 2,
                     "legend.frameon": False, "legend.fontsize": FS_BODY,
                     "mathtext.fontset": "custom", "mathtext.rm": "Arial",
                     "mathtext.it": "Arial:italic", "mathtext.bf": "Arial:bold"})

FAMS = ["stromal", "epithelial", "endothelial", "immune"]
FAM_C = dict(zip(FAMS, FAMILY_C))
AMBER, AMBER_F = "#CC4E00", "#FFDDA6"
ABL_C = "#7D87FA"          # counterfactual arms, never a colour we report in
GREY_PT = "#DCE0E4"

DISPLAY = {m: v[3] for m, v in table1.MANIFEST.items()}
DISPLAY.update({"ELAJ_B_hi": "ELAJ B$_{hi}$", "ELAJ_B_lo": "ELAJ B$_{lo}$",
                "elaj": "ELAJ B$_{hi}$"})
TEX_DISPLAY = {m: v[3] for m, v in table1.MANIFEST.items()}
TEX_DISPLAY.update({"ELAJ_B_hi": r"\elaj\,B\textsubscript{hi}",
                    "ELAJ_B_lo": r"\elaj\,B\textsubscript{lo}"})
ARM_LABEL = {k: f"$\\lambda$ {d}, $w_{{kl}}$ {w}" for k, d, w in table1.P_SERIES}
ARM_LABEL["p1_dab168_kl1"] += " (B$_{hi}$)"
ARM_LABEL["p1_dab168_kl30"] += " (B$_{lo}$)"
ARM_LABEL.update({"a1_randgroups": "random groups", "a1_nophase": "no phase head",
                  "a1_noecs": "no ECS", "a1_nodns": "no DNS sentinel",
                  "a1_clsonly": "no order statistics"})
ARM_TEX = {k: f"$\\lambda_{{\\mathrm{{dab}}}}$ {d}, $w_{{\\mathrm{{kl}}}}$ {w}"
           for k, d, w in table1.P_SERIES}
ARM_TEX.update({k: v for k, v in table1.A_SERIES})
P_ARMS = [k for k, _, _ in table1.P_SERIES]
A_ARMS = [k for k, _ in table1.A_SERIES]
ALL_ARMS = P_ARMS + A_ARMS
KLC = {1: "#2F6690", 30: "#8C2F39"}
DABC = {7: "#D9A441", 168: "#3A7D5D", 336: "#6D2E46"}
A_C = {"a1_randgroups": "#B279A2", "a1_nophase": "#E45756", "a1_noecs": "#54A24B",
       "a1_nodns": "#F58518", "a1_clsonly": "#4C78A8"}

WRITTEN: list[Path] = []


# ── helpers ──────────────────────────────────────────────────────────────
def label_lines(ax, items, dx=2.0, fontsize=FS_LEG, pad=None):
    """Write each line's name at its own right-hand end, pushed apart.

    AW, 17 November: "None of the loss curves are legible because the lines
    have no labels. 3 lines of the same colour identify different models.
    Please add model call outs to the lines. Leave the colours as they
    are." Colour encodes the knob and has to stay ambiguous between the
    three arms that share it, so the arm's name has to be ON the line.

    `items` is (x_end, y_end, text, colour). Labels are placed at the y of
    their own line and then separated downwards in y-order by at least
    `pad` data units, which is the minimum that keeps 5 pt type from
    overlapping at this axes height.
    """
    if not items:
        return
    lo, hi = ax.get_ylim()
    if pad is None:
        pad = (hi - lo) * 0.072
    order = sorted(range(len(items)), key=lambda i: -items[i][1])
    ys = {}
    prev = None
    for i in order:
        y = items[i][1]
        if prev is not None and prev - y < pad:
            y = prev - pad
        ys[i] = y
        prev = y
    for i, (x, y0, text, c) in enumerate(items):
        ax.annotate(text, xy=(x, y0), xytext=(x + dx, ys[i]),
                    textcoords="data", fontsize=fontsize, color=c,
                    va="center", ha="left",
                    arrowprops=dict(arrowstyle="-", color=c, lw=.4,
                                    shrinkA=1, shrinkB=0, alpha=.7))
    ax.set_xlim(ax.get_xlim()[0], ax.get_xlim()[1] + dx * 4.2)


def label_points(ax, items, fontsize=FS_LEG, gap=5.0):
    """Annotate scatter points, pushing colliding labels apart vertically.

    Works in DISPLAY points, so it is correct on a log axis where a fixed
    data offset is not. Points whose labels would overlap are separated
    downwards in y-order; a point in the right-hand third of the axes gets
    its label on the left so it cannot run off the edge.
    """
    if not items:
        return
    fig = ax.figure
    fig.canvas.draw()
    xs = [ax.transData.transform((x, y))[0] for x, y, _, _ in items]
    ys = [ax.transData.transform((x, y))[1] for x, y, _, _ in items]
    x0, x1 = ax.transAxes.transform((0, 0))[0], ax.transAxes.transform((1, 0))[0]
    order = sorted(range(len(items)), key=lambda i: -ys[i])
    placed, prev = {}, None
    for i in order:
        yy = ys[i]
        if prev is not None and prev - yy < gap:
            yy = prev - gap
        placed[i] = yy
        prev = yy
    for i, (x, y, text, c) in enumerate(items):
        right = xs[i] > x0 + (x1 - x0) * 0.66
        dy = placed[i] - ys[i]
        ax.annotate(text, (x, y), xytext=(-4 if right else 4, dy + 0.5),
                    textcoords="offset points", fontsize=fontsize, color=c,
                    ha="right" if right else "left", va="center")


def fig_ax(w=88, h=60):
    fig, ax = plt.subplots(figsize=(w * MM, h * MM))
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    return fig, ax


def save(fig, name: str, cite: bool = False):
    """Every figure to the explore tier; cited ones also into supplementary/."""
    EXPLORE.mkdir(parents=True, exist_ok=True)
    dest = EXPLORE / f"{name}.png"
    fig.savefig(dest, dpi=DPI, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    WRITTEN.append(dest)
    if cite:
        FIG.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(dest, FIG / f"{name}.png")
    print(f"  fig  {name}{'  (cited)' if cite else ''}")


def tex(name: str, body: str):
    TAB.mkdir(parents=True, exist_ok=True)
    p = TAB / f"{name}.tex"
    p.write_text("% GENERATED by figures/scripts/supp_figures.py. Do not edit by hand.\n"
                 + body.rstrip() + "\n")
    print(f"  tab  {name}")


def esc(s) -> str:
    return (str(s).replace("\\", r"\textbackslash{}").replace("&", r"\&")
            .replace("%", r"\%").replace("_", r"\_").replace("#", r"\#"))


def num(v, nd=4, dash="--") -> str:
    if v is None or (isinstance(v, float) and np.isnan(v)) or v == "":
        return dash
    v = float(v)
    s = f"{v:.{nd}f}"
    return s.replace("-", "$-$")


def intc(v) -> str:
    return f"{int(v):,}".replace(",", "{,}")


def tabular(cols: str, header: list[str], rows: list[list[str]],
            midrules: list[int] | None = None) -> str:
    L = [r"\begin{tabular}{" + cols + "}", r"\toprule",
         " & ".join(header) + r" \\", r"\midrule"]
    for i, r in enumerate(rows):
        if midrules and i in midrules:
            L.append(r"\midrule")
        L.append(" & ".join(r) + r" \\")
    L += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(L)


def bench_rows(path: Path, method: str = "elaj"):
    """Every row of one benchmark file for one method, note included."""
    out = {}
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh):
            if re.sub("__.*", "", r["method"]) != method:
                continue
            out[(r["test"], r["label"])] = r
    return out


def note_field(note: str, key: str):
    m = re.search(key + r"=([-\d.]+)", note or "")
    return float(m.group(1)) if m else None


def note_donors(note: str):
    m = re.search(r"(\d+) donors", note or "")
    return int(m.group(1)) if m else None


_META = None
_IDX = None


def meta() -> pd.DataFrame:
    global _META
    if _META is None:
        _META = pd.read_csv(CELLS / ARM / "metadata.csv.gz", low_memory=False)
    return _META


def sample_index() -> np.ndarray:
    """The pinned 400,000-cell index every UMAP cache was drawn on."""
    global _IDX
    if _IDX is None:
        pin = ROOT / "axw1008/src/scripts/umap_sample_N1577728_n400000_s24.npy"
        _IDX = np.load(pin).astype(np.int64)
        assert len(_IDX) == 400_000 and _IDX.max() < 1_577_728
    return _IDX


def umap_cache(arm: str) -> Path:
    if arm in ("p1_dab168_kl1", "p1_dab168_kl30"):
        return ROOT / f"Outputs/analysis/umaps/{arm}/_umap_cache/global_400000.npy"
    return OUT / f"umaps_supplementary/umaps/{arm}/_umap_cache/global_400000.npy"


# ═════════════════════════════════════════════════════════════════════════
# 1. scIB
# ═════════════════════════════════════════════════════════════════════════
SCIB_HALF = {"scib-graph_connectivity": "batch", "scib-ilisi_knn": "batch",
             "scib-kbet": "batch", "scib-pcr_batch": "batch",
             "scib-silhouette_batch": "batch", "scib-ari": "bio",
             "scib-clisi_knn": "bio", "scib-isolated_labels": "bio",
             "scib-nmi": "bio", "scib-silhouette_bio": "bio"}
SCIB_SHORT = {"scib-graph_connectivity": "graph conn.", "scib-ilisi_knn": "iLISI",
              "scib-kbet": "kBET", "scib-pcr_batch": "PCR batch",
              "scib-silhouette_batch": "silhouette batch", "scib-ari": "ARI",
              "scib-clisi_knn": "cLISI", "scib-isolated_labels": "isolated labels",
              "scib-nmi": "NMI", "scib-silhouette_bio": "silhouette bio"}
# What each metric rewards, in one clause. Definitions are scib-metrics' own;
# the clause is ours and is the only hand-written content in this table.
SCIB_WHAT = {
    "scib-graph_connectivity": "each label's cells form one connected kNN component",
    "scib-ilisi_knn": "neighbourhoods draw on many studies",
    "scib-kbet": "local study mix matches the global mix",
    "scib-pcr_batch": "variance explained by study after, against before",
    "scib-silhouette_batch": "within a label, studies do not separate",
    "scib-ari": "Leiden clusters coincide with the label",
    "scib-clisi_knn": "neighbourhoods draw on one label",
    "scib-isolated_labels": "the rarest-across-studies label stays separable",
    "scib-nmi": "Leiden clusters share information with the label",
    "scib-silhouette_bio": "labels separate with a margin",
}
SCIB_ORDER = [m for m in SCIB_HALF if SCIB_HALF[m] == "batch"] + \
             [m for m in SCIB_HALF if SCIB_HALF[m] == "bio"]
REP_ORDER = ["ELAJ_B_hi", "ELAJ_B_lo", "pca", "scvi", "scanvi", "harmony",
             "scanorama", "scgpt", "geneformer", "scimilarity", "scfoundation"]


def scib():
    card = pd.read_csv(OUT / "scib/scib_scorecard.csv", index_col=0)
    card = card.loc[REP_ORDER, SCIB_ORDER]
    disc = pd.read_csv(OUT / "scib/scib_discrimination.csv").set_index("metric")
    ann = pd.read_csv(OUT / "scib/scib_scorecard_annotationrefined.csv", index_col=0)

    # tables
    rows = [[TEX_DISPLAY[r]] + [num(card.loc[r, m]) for m in SCIB_ORDER]
            for r in REP_ORDER]
    tex("scib_cellfamily", tabular("@{}l" + "r" * 10 + "@{}",
        ["representation"] + [SCIB_SHORT[m] for m in SCIB_ORDER], rows, [2, 7]))
    ann_cols = [m for m in SCIB_ORDER if m in ann.columns]
    rows = [[TEX_DISPLAY[r]] + [num(ann.loc[r, m]) for m in ann_cols] for r in REP_ORDER]
    tex("scib_annotationrefined", tabular("@{}l" + "r" * len(ann_cols) + "@{}",
        ["representation"] + [SCIB_SHORT[m] for m in ann_cols], rows, [2, 7]))
    # tables/scib_discrimination.tex is DELIBERATELY NOT WRITTEN any more.
    # AW, 16 November: "Remove table S5." Its four columns now sit beside
    # the bars in scib_metric_range, and what each metric rewards moved into
    # the note's own prose, where it primes the reader before the numbers.

    # THE HEATMAP IS GONE. AW, 16 November: "Fig S4 is just the table in
    # colours. Keep the table, remove the figure." Table S3 carries all 110
    # values already, so drawing them a second time in grey added nothing.
    #
    # AND TABLE S5 IS GONE WITH IT, folded into the figure below. The table
    # held min, max, range and a verdict per metric; the figure held the
    # same ranges as bars. Printing both was the same redundancy one level
    # up, so the numbers now sit in aligned columns beside the bars, which
    # is IBDex Fig. 2c's device: the reader sees the shape and reads the
    # value without looking anything up.
    # SIZED SO THE TYPE SURVIVES. AW, 17 November: "Fig S3's words are too
    # small. There is also a lot of whitespace in the figure." Both are one
    # fault. The numeric columns run out to axes fraction 1.52, so a 150 mm
    # axes made a 250 mm figure, which \textwidth then scaled to 0.64 and
    # took every label to 3.5 pt. A 95 mm axes puts the whole figure near
    # 160 mm, so it is placed at roughly 1:1 and FS_BODY stays FS_BODY.
    fig, ax = plt.subplots(figsize=(95 * MM, 70 * MM))
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    y = np.arange(10)[::-1]
    XMAX = 1.02
    for i, m in enumerate(SCIB_ORDER):
        d = disc.loc[m]
        flat = d.degenerate or d.spread < 0.05
        c = AMBER if d.degenerate else ("#B279A2" if d.spread < .05 else INK)
        ax.plot([d["min"], d["max"]], [y[i], y[i]], color=c, lw=2.6,
                solid_capstyle="round", zorder=2)
        if flat:                       # a range too short to see gets a tick
            ax.plot([d["min"]], [y[i]], marker="|", ms=8, color=c, mew=1.4, zorder=3)
        ax.plot([card.loc["ELAJ_B_hi", m]], [y[i]], marker="o", ms=4.2,
                color="white", mec=c, mew=1.1, zorder=4)
    ax.set_yticks(y); ax.set_yticklabels([SCIB_SHORT[m] for m in SCIB_ORDER])
    ax.set_xlim(-.02, XMAX); ax.set_xlabel("score across the eleven representations")
    ax.axhline(4.5, color=HAIR, lw=.5, ls=":")
    # No "batch half" / "bio half" text: it collided with the graph
    # connectivity bar wherever it was placed, and the dotted divider plus
    # the caption already say which half is which.
    # the aligned numeric columns, in axes-fraction space to the right
    cols = [(1.09, "min"), (1.21, "max"), (1.34, "range"), (1.52, "on this corpus")]
    for x, head in cols:
        ax.text(x, 1.045, head, transform=ax.transAxes, fontsize=FS_BODY,
                fontweight="bold", ha="center" if head != "on this corpus" else "left",
                color=INK)
    for i, m in enumerate(SCIB_ORDER):
        d = disc.loc[m]
        yy = (y[i] + 0.5) / 10
        verdict = ("constant" if d.degenerate else
                   "near-constant" if d.spread < .05 else "separates them")
        vc = AMBER if d.degenerate else ("#B279A2" if d.spread < .05 else SOFT)
        for x, val in ((1.09, f"{d['min']:.4f}"), (1.21, f"{d['max']:.4f}"),
                       (1.34, f"{d['spread']:.4f}")):
            ax.text(x, yy, val, transform=ax.transAxes, fontsize=FS_BODY,
                    ha="center", va="center", color=INK)
        ax.text(1.52, yy, verdict, transform=ax.transAxes, fontsize=FS_BODY,
                ha="left", va="center", color=vc,
                fontweight="bold" if vc != SOFT else "normal")
    ax.legend(handles=[Line2D([], [], color=INK, lw=2.6, label="range over the eleven"),
                       Line2D([], [], color="white", mec=INK, mew=1.1, lw=0,
                              marker="o", ms=4.2, label="ELAJ B$_{hi}$"),
                       Line2D([], [], color=AMBER, lw=0, marker="|", ms=8, mew=1.4,
                              label="one value for all eleven")],
              loc="upper center", bbox_to_anchor=(.33, -.17), ncol=3)
    save(fig, "scib_metric_range", cite=True)

    # correlation of each scIB metric with donor recovery and with phase
    D = table1.collect()
    key = {"ELAJ_B_hi": "p1_dab168_kl1", "ELAJ_B_lo": "p1_dab168_kl30"}
    donor = {r: float(D[key.get(r, r)][("knn-agreement", "patient_id")]) for r in REP_ORDER}
    phase = {r: float(D[key.get(r, r)][("cross-donor", "menstrual phase")]) for r in REP_ORDER}
    rows = []
    fig, ax = fig_ax(88, 55)
    for i, m in enumerate(SCIB_ORDER):
        v = card[m].values.astype(float)
        if disc.loc[m].degenerate:
            rows.append([SCIB_SHORT[m], SCIB_HALF[m], "--", "--", "--", "--"])
            continue
        rd, pd_ = spearmanr(v, [donor[r] for r in REP_ORDER])
        rp, pp = spearmanr(v, [phase[r] for r in REP_ORDER])
        rows.append([SCIB_SHORT[m], SCIB_HALF[m], num(rd, 3), num(pd_, 3), num(rp, 3), num(pp, 3)])
        ax.plot(rd, y[i], "o", color="#8C2D3F", ms=3.4, mec="white", mew=.3)
        ax.plot(rp, y[i], "s", color="#2F6690", ms=3.2, mec="white", mew=.3)
    tex("scib_correlations", tabular("@{}llrrrr@{}",
        ["metric", "half", r"$\rho$ donor recovery", "$P$", r"$\rho$ cycle", "$P$"], rows, [5]))
    ax.axvline(0, color=HAIR, lw=.6)
    ax.set_yticks(y); ax.set_yticklabels([SCIB_SHORT[m] for m in SCIB_ORDER])
    ax.set_xlim(-1.05, 1.05); ax.set_xlabel("Spearman $\\rho$ across eleven representations")
    ax.legend(handles=[Line2D([], [], color="#8C2D3F", marker="o", lw=0, ms=3.4,
                              label="with donor recovery"),
                       Line2D([], [], color="#2F6690", marker="s", lw=0, ms=3.2,
                              label="with cross-donor cycle agreement")],
              loc="lower left")
    save(fig, "scib_vs_donor_and_cycle", cite=True)

    # the two ELAJ arms on the bio half: a prior-strength effect on clustering metrics
    fig, ax = fig_ax(88, 50)
    # AW's order, 16 November: ARI, NMI, isolated labels, silhouette bio.
    bio = [m for m in ("scib-ari", "scib-nmi", "scib-isolated_labels",
                       "scib-silhouette_bio") if not disc.loc[m].degenerate]
    x = np.arange(len(bio))
    for k, (r, c) in enumerate([("ELAJ_B_hi", AMBER), ("ELAJ_B_lo", "#8C2F39")]):
        ax.bar(x + (k - .5) * .36, card.loc[r, bio], .34, color=c, label=DISPLAY[r])
    for m_i, m in enumerate(bio):
        others = card.loc[[r for r in REP_ORDER if not r.startswith("ELAJ")], m]
        ax.plot([m_i - .45, m_i + .45], [others.median()] * 2, color=INK, lw=.8)
    ax.set_xticks(x); ax.set_xticklabels([SCIB_SHORT[m] for m in bio])
    ax.set_ylabel("score"); ax.set_ylim(0, 1)
    ax.legend(handles=ax.get_legend_handles_labels()[0] +
              [Line2D([], [], color=INK, lw=.8, label="median of the nine others")],
              loc="upper center", bbox_to_anchor=(.5, -.16), ncol=3)
    save(fig, "scib_bio_half_two_arms", cite=True)


# ═════════════════════════════════════════════════════════════════════════
# 2. the field: width, donor recovery, disease
# ═════════════════════════════════════════════════════════════════════════
def field():
    D = table1.collect()
    meth = list(table1.MANIFEST) + ["p1_dab168_kl1"]
    name = lambda m: "ELAJ B$_{hi}$" if m == "p1_dab168_kl1" else DISPLAY[m]
    width = {m: int(float(D[m]["width"])) for m in meth if D[m].get("width")}
    width["p1_dab168_kl1"] = 16
    width.setdefault("scfoundation", 3072)
    g = lambda m, t, l: float(D[m][(t, l)])
    phase = {m: g(m, "cross-donor", "menstrual phase") for m in meth}
    donor = {m: g(m, "knn-agreement", "patient_id") for m in meth}
    disease = {m: g(m, "disease-xdonor", "all studies (pooled)") for m in meth}
    family = {m: g(m, "cross-donor", "cell family") for m in meth}

    def scatter(xs, ys, xl, yl, fname, logx=False, cite=False):
        fig, ax = fig_ax(88, 62)
        pts = []
        for m in meth:
            ours = m == "p1_dab168_kl1"
            ax.plot(xs[m], ys[m], "o", ms=4.5 if ours else 3.4,
                    color=AMBER if ours else INK, mec="white", mew=.4, zorder=3)
            pts.append((xs[m], ys[m], name(m), AMBER if ours else SOFT))
        if logx:
            ax.set_xscale("log")
        ax.margins(.12)
        # LABELS BEFORE THE STATS BOX, and de-collided: four of the ten
        # representations are sixteen dimensions wide, so their labels
        # stack on one x.
        label_points(ax, pts)
        rho, p = spearmanr([xs[m] for m in meth], [ys[m] for m in meth])
        # THE STATS GO IN A BOX, IN THE EMPTIEST CORNER. AW, 17 November:
        # "S9 is very jumbled at the top left." Four of the ten points sit
        # at width 16, so their labels stack in exactly the corner the
        # statistics were written into. IBDex's device is a boxed inset;
        # here it goes bottom-left, which every one of these scatters
        # leaves empty, and the box keeps it off any point it does meet.
        ax.text(.02, .03, f"Spearman $\\rho$ = {rho:+.3f}\n$P$ = {p:.3f}, n = {len(meth)}",
                transform=ax.transAxes, va="bottom", ha="left", fontsize=FS_BODY,
                color=INK, linespacing=1.5,
                bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=HAIR, lw=.5))
        ax.set_xlabel(xl); ax.set_ylabel(yl)
        save(fig, fname, cite=cite)
        return rho, p

    r1 = scatter(width, phase, "representation width (dimensions, log)",
                 "cross-donor cycle agreement", "field_width_vs_cycle", logx=True, cite=True)
    # NOT CITED. AW, 16 November: "Fig 10 and 11 are not needed. The table
    # makes the point effectively." Both are still drawn to the exploratory
    # tier, because the correlation table is read off them.
    r2 = scatter(donor, disease, "donor recovery (lower is better)",
                 "cross-donor disease agreement", "field_donor_vs_disease")
    r3 = scatter(donor, phase, "donor recovery (lower is better)",
                 "cross-donor cycle agreement", "field_donor_vs_cycle")
    r4 = scatter(donor, family, "donor recovery (lower is better)",
                 "cross-donor cell-family agreement", "field_donor_vs_family")
    rows = [["width", "cycle agreement", num(r1[0], 3), num(r1[1], 3)],
            ["donor recovery", "disease agreement", num(r2[0], 3), num(r2[1], 3)],
            ["donor recovery", "cycle agreement", num(r3[0], 3), num(r3[1], 3)],
            ["donor recovery", "cell-family agreement", num(r4[0], 3), num(r4[1], 3)]]
    tex("field_correlations", tabular("@{}llrr@{}",
        ["x", "y", r"Spearman $\rho$", "$P$"], rows))

    # severity among patients, every representation, against its own null
    rows = []
    fig, ax = fig_ax(88, 58)
    order = sorted(meth, key=lambda m: -g(m, "cross-donor", "severity"))
    y = np.arange(len(order))[::-1]
    for i, m in enumerate(order):
        src = (BENCH / "full/full_p1_dab168_kl1/benchmark.csv" if m == "p1_dab168_kl1"
               else BENCH / table1.SEVERITY[m] / "benchmark.csv")
        rr = bench_rows(src, "elaj" if m == "p1_dab168_kl1" else m)
        sev, sevp = rr[("cross-donor", "severity")], rr[("cross-donor-p", "severity")]
        pat, patp = rr[("cross-donor", "severity (patients only)")], \
            rr[("cross-donor-p", "severity (patients only)")]
        rows.append([name(m).replace("$_{hi}$", r"\textsubscript{hi}").replace("ELAJ", r"\elaj"),
                     num(sev["value"]), num(note_field(sev["note"], "null95"), 2),
                     num(sevp["value"], 3), num(pat["value"]),
                     num(note_field(pat["note"], "null95"), 2), num(patp["value"], 3)])
        c = AMBER if m == "p1_dab168_kl1" else INK
        for k, (r_, off) in enumerate([(sev, .18), (pat, -.18)]):
            n95 = note_field(r_["note"], "null95")
            ax.barh(y[i] + off, n95, height=.3, color=GREY_PT, left=0)
            ax.plot(float(r_["value"]), y[i] + off, "o" if k == 0 else "s", color=c,
                    ms=3.4, mec="white", mew=.3, zorder=3)
    ax.axvline(0, color=INK, lw=.6)
    ax.set_yticks(y); ax.set_yticklabels([name(m) for m in order])
    ax.set_xlabel("cross-donor agreement, excess over chance")
    ax.legend(handles=[Line2D([], [], marker="o", lw=0, color=INK, ms=3.4,
                              label="merged severity, 34 held-out donors"),
                       Line2D([], [], marker="s", lw=0, color=INK, ms=3.4,
                              label="mild against severe, patients only, 18"),
                       plt.Rectangle((0, 0), 1, 1, color=GREY_PT,
                                     label="each row's own permutation null (95th pct.)")],
              loc="lower right")
    # NOT CITED. AW, 17 November: "A lot of figures don't seem to have
    # references. Why are we keeping the figure?" No note inputs this one,
    # because Results carries the severity result in full, so it stays in
    # the exploratory tier. The FRAGMENT is still written: it and
    # tables/corpus.tex are the two held for the Supplementary Tables
    # section, which does not exist yet. Those two are the only tables/
    # files no note inputs, and that is deliberate.
    save(fig, "field_severity_vs_null")
    tex("field_severity", tabular("@{}lrrrrrr@{}",
        ["representation", "severity", "null$_{95}$", "$P$",
         "patients only", "null$_{95}$", "$P$"], rows))


# ═════════════════════════════════════════════════════════════════════════
# 3. the frontier arms and the ablations: tables, curves, trajectories
# ═════════════════════════════════════════════════════════════════════════
def metrics(arm: str) -> pd.DataFrame:
    return pd.read_csv(ROOT / "Outputs" / table1.METRICS[arm] / "metrics.csv")


def arm_table_rows(arms, D, with_delta=False):
    axes = [("cross-donor", "menstrual phase"), ("cross-donor", "cell family"),
            ("knn-agreement", "AnnotationRefined"), ("knn-agreement", "cell cycle phase"),
            ("disease-xdonor", "all studies (pooled)"), ("cross-donor", "severity"),
            ("cross-donor", "Endometriosis_stage"), ("cross-donor", "EndometriosisGrade"),
            ("knn-agreement", "patient_id"), ("study-mixing", "all studies")]
    base = {a: float(D["p1_dab168_kl1"][a]) for a in axes}
    rows = []
    for arm in arms:
        g = D[arm]
        vals = []
        for a in axes:
            v = float(g[a])
            s = num(v)
            if with_delta and arm != "p1_dab168_kl1":
                d = v - base[a]
                s += f" ({'+' if d >= 0 else '$-$'}{abs(d):.4f})"
            vals.append(s)
        rows.append([ARM_TEX[arm]] + vals)
    return rows


def arms():
    D = table1.collect()
    # p-series: biology axes and cost axes as two tables
    hdr_bio = ["arm", "cycle", "family", "cell type", "cell cycle", "disease",
               "severity", "stage", "grade"]
    hdr_cost = ["arm", "donor", "study sep.", "val$_{nb}$", "epochs", "best", "hours"]
    rows_bio, rows_cost = [], []
    for arm in P_ARMS + A_ARMS:
        r = arm_table_rows([arm], D)[0]
        rows_bio.append(r[:9])
        m = metrics(arm); b = m.val_nb.idxmin()
        hours = (m.train_epoch_time_s.sum() + m.val_epoch_time_s.sum()) / 3600
        rows_cost.append([r[0], r[9], r[10], num(m.val_nb[b]), str(len(m)),
                          str(int(m.epoch[b])), f"{hours:.1f}"])
    tex("arms_biology", tabular("@{}l" + "r" * 8 + "@{}", hdr_bio, rows_bio, [6]))
    tex("arms_cost", tabular("@{}l" + "r" * 6 + "@{}", hdr_cost, rows_cost, [6]))
    # ablations with deltas
    rows = arm_table_rows(["p1_dab168_kl1"] + A_ARMS, D, with_delta=True)
    rows[0][0] = r"\elaj\,B\textsubscript{hi} (base)"
    tex("ablation_axes_bio", tabular("@{}l" + "r" * 5 + "@{}",
        ["arm", "cycle", "family", "cell type", "disease", "severity"],
        [[r[0], r[1], r[2], r[3], r[5], r[6]] for r in rows]))
    tex("ablation_axes_cost", tabular("@{}l" + "r" * 4 + "@{}",
        ["arm", "stage", "grade", "donor", "study sep."],
        [[r[0]] + r[7:11] for r in rows]))

    # p-values and null widths for every cross-donor label, every arm
    rows = []
    labels = [("menstrual phase", "cycle"), ("cell family", "family"), ("severity", "severity"),
              ("severity (patients only)", "patients only"),
              ("Endometriosis_stage", "stage"), ("EndometriosisGrade", "grade")]
    for arm in P_ARMS + A_ARMS:
        rr = bench_rows(BENCH / "full" / f"full_{arm}" / "benchmark.csv")
        cells = [ARM_TEX[arm]]
        for lab, _ in labels:
            v = rr[("cross-donor", lab)]; p = rr[("cross-donor-p", lab)]
            cells.append(f"{num(v['value'])} ({float(p['value']):.3f})")
        rows.append(cells)
    tex("arms_pvalues", tabular("@{}l" + "r" * 6 + "@{}",
        ["arm"] + [l for _, l in labels], rows, [6]))

    # training summary for ablations
    rows = []
    for arm in ["p1_dab168_kl1"] + A_ARMS:
        m = metrics(arm); b = m.val_nb.idxmin(); last = len(m) - 1
        rows.append([r"\elaj\,B\textsubscript{hi} (base)" if arm == "p1_dab168_kl1" else ARM_TEX[arm],
                     str(len(m)), str(int(m.epoch[b])), num(m.train_nb[b]), num(m.val_nb[b]),
                     num(m.train_nb[last]), num(m.val_nb[last]), f"{m.val_reliance_ratio[b]:.2f}"])
    tex("ablation_training", tabular("@{}lrrrrrrr@{}",
        ["arm", "epochs", "best", "train$_{nb}$", "val$_{nb}$",
         "train$_{nb}$ last", "val$_{nb}$ last", "reliance"], rows))

    # ── THE REGISTERED PREDICTION BANDS ARE GONE. ───────────────────────
    # AW, 17 November: "Remove prediction bands. That was internal." They
    # were an honest record of what we expected before each run, and they
    # are a record of our own process rather than a property of the models,
    # which is not what a supplementary note is for. Both band tables and
    # every mention of them left Notes 4 and 5 in the same pass.

    # ── loss curves ──────────────────────────────────────────────────────
    for series, arms_, cmap, fname in (("p", P_ARMS, None, "training_loss_pseries"),
                                        ("a", ["p1_dab168_kl1"] + A_ARMS, A_C,
                                         "training_loss_ablations")):
        fig, ax = fig_ax(104, 62)
        tips = []
        for arm in arms_:
            m = metrics(arm)
            c = (A_C.get(arm, AMBER) if series == "a" else
                 KLC[dict((k, w) for k, _, w in table1.P_SERIES)[arm]])
            ax.plot(m.epoch, m.val_nb, color=c, lw=1.1, label=ARM_LABEL[arm])
            ax.plot(m.epoch, m.train_nb, color=c, lw=.7, ls=":", alpha=.9)
            b = m.val_nb.idxmin()
            ax.plot(m.epoch[b], m.val_nb[b], "o", color=c, ms=3.2, mec="white", mew=.4)
            # the call-out goes on the HELD-OUT line, which is the one the
            # argument is about; the dotted training line below it shares
            # the colour and needs no second name.
            tips.append((float(m.epoch.iloc[-1]), float(m.val_nb.iloc[-1]),
                         ARM_LABEL[arm], c))
        ax.set_xlabel("epoch"); ax.set_ylabel("negative-binomial loss per cell")
        label_lines(ax, tips, dx=0.25)
        ax.legend(handles=[
            Line2D([], [], color=INK, lw=1.1, label="held-out (solid)"),
            Line2D([], [], color=INK, lw=.7, ls=":", label="training (dotted)"),
            Line2D([], [], color=INK, marker="o", lw=0, ms=3.2,
                   label="selected checkpoint")],
            loc="upper center", bbox_to_anchor=(.5, -.16), ncol=3, fontsize=FS_LEG)
        save(fig, fname, cite=True)

    # ── per-epoch validation trajectories ────────────────────────────────
    for col, ylabel, fname in (("val_phase_knn_xdonor", "validation cross-donor cycle (k=30)",
                                "trajectory_cycle"),
                               ("val_family_knn_xdonor", "validation cross-donor family (k=30)",
                                "trajectory_family"),
                               ("val_patient_knn", "validation donor recovery (k=100)",
                                "trajectory_donor"),
                               ("val_study_knn", "validation study recovery (k=30)",
                                "trajectory_study")):
        for series, arms_, fname2 in (("p", P_ARMS, "pseries"),
                                      ("a", ["p1_dab168_kl1"] + A_ARMS, "ablations")):
            fig, ax = fig_ax(104, 60)
            tips = []
            for arm in arms_:
                m = metrics(arm)
                c = (A_C.get(arm, AMBER) if series == "a" else
                     KLC[dict((k, w) for k, _, w in table1.P_SERIES)[arm]])
                mk = "o" if series == "a" or arm.endswith("kl1") else "s"
                ax.plot(m.epoch, m[col], color=c, lw=1.0, marker=mk, ms=2.4,
                        mec="white", mew=.3, label=ARM_LABEL[arm])
                b = m.val_nb.idxmin()
                ax.plot(m.epoch[b], m[col][b], marker=mk, ms=5.5, color=c, mfc="none", mew=.9)
                tips.append((float(m.epoch.iloc[-1]), float(m[col].iloc[-1]),
                             ARM_LABEL[arm], c))
            ax.set_xlabel("epoch"); ax.set_ylabel(ylabel)
            label_lines(ax, tips, dx=0.25)
            ax.legend(handles=[Line2D([], [], marker="o", mfc="none", color=INK,
                                      lw=0, ms=5.5,
                                      label="selected checkpoint (min val$_{nb}$)")],
                      fontsize=FS_LEG, loc="upper center", bbox_to_anchor=(.5, -.16))
            save(fig, f"{fname}_{fname2}", cite=(col == "val_phase_knn_xdonor"))

    # reliance ratio and hours
    # COLOUR ENCODES THE KNOB, NOT THE ARM. AW, 16 November: "Fig S13
    # colouring is fucked. Colours should mean something here." It did not:
    # the six frontier models shared one grey while the five ablations each
    # took an arbitrary hue. Now the frontier models are coloured by their
    # information cost, which is the variable that separates them, and the
    # ablations share one counterfactual colour, which is what they are.
    def arm_colour(a):
        if a in dict((k, w) for k, _, w in table1.P_SERIES):
            return KLC[dict((k, w) for k, _, w in table1.P_SERIES)[a]]
        return ABL_C
    bar_legend = [Line2D([], [], marker="s", lw=0, ms=5, color=KLC[1],
                         label="frontier model, $w_{kl}$ 1"),
                  Line2D([], [], marker="s", lw=0, ms=5, color=KLC[30],
                         label="frontier model, $w_{kl}$ 30"),
                  Line2D([], [], marker="s", lw=0, ms=5, color=ABL_C,
                         label="ablation (counterfactual)")]
    fig, ax = fig_ax(88, 50)
    rel = {a: metrics(a).val_reliance_ratio[metrics(a).val_nb.idxmin()] for a in ALL_ARMS}
    cols = [arm_colour(a) for a in ALL_ARMS]
    ax.bar(range(len(ALL_ARMS)), [rel[a] for a in ALL_ARMS], color=cols)
    ax.axhline(rel["p1_dab168_kl1"], color=INK, lw=.7, ls=":")
    ax.text(len(ALL_ARMS) - .4, rel["p1_dab168_kl1"], " reported model",
            fontsize=FS_BODY, color=SOFT, va="center")
    ax.legend(handles=bar_legend, loc="upper center", bbox_to_anchor=(.5, -.42),
              ncol=3, fontsize=FS_LEG)
    ax.set_xticks(range(len(ALL_ARMS)))
    ax.set_xticklabels([ARM_LABEL[a] for a in ALL_ARMS], rotation=40, ha="right")
    ax.set_ylabel("decoder reliance, latent / provenance")
    save(fig, "reliance_ratio_all_arms", cite=True)

    fig, ax = fig_ax(88, 45)
    hrs = {a: (metrics(a).train_epoch_time_s.sum() + metrics(a).val_epoch_time_s.sum()) / 3600
           for a in ALL_ARMS}
    ax.bar(range(len(ALL_ARMS)), [hrs[a] for a in ALL_ARMS], color=cols)
    ax.set_xticks(range(len(ALL_ARMS)))
    ax.set_xticklabels([ARM_LABEL[a] for a in ALL_ARMS], rotation=40, ha="right")
    ax.set_ylabel("wall-clock hours, one A100")
    ax.axhline(np.mean(list(hrs.values())), color=INK, lw=.6, ls=":")
    ax.text(len(ALL_ARMS) - .4, np.mean(list(hrs.values())), " mean",
            fontsize=FS_BODY, color=SOFT, va="bottom", ha="right")
    ax.legend(handles=bar_legend, loc="upper center", bbox_to_anchor=(.5, -.52),
              ncol=3, fontsize=FS_LEG)
    save(fig, "training_hours_all_arms", cite=True)

    # ── the ablations as counterfactuals from the base, and NOTHING ELSE ─
    # AW, 17 November: "Fig S19 is very crowded. If the objective is showing
    # ablations keep only ELAJ_B_hi and remove the rest." The nine
    # comparison methods and the five other frontier arms were answering a
    # different question, which Fig. 2 of the main text already answers.
    # What is left is one base point with five arrows off it, so the length
    # and direction of each arrow is the whole figure.
    fig, ax = fig_ax(92, 68)
    bx = float(D["p1_dab168_kl1"][("knn-agreement", "patient_id")])
    by = float(D["p1_dab168_kl1"][("cross-donor", "menstrual phase")])
    tips = []
    for a in A_ARMS:
        x_ = float(D[a][("knn-agreement", "patient_id")])
        y_ = float(D[a][("cross-donor", "menstrual phase")])
        ax.annotate("", (x_, y_), (bx, by),
                    arrowprops=dict(arrowstyle="-|>", color=A_C[a], lw=.9,
                                    shrinkA=3, shrinkB=3))
        ax.plot(x_, y_, "D", color=A_C[a], ms=4.2, mec="white", mew=.5, zorder=3)
        tips.append((x_, y_, ARM_LABEL[a], A_C[a]))
    ax.plot(bx, by, "o", color=INK, ms=6, mec="white", mew=.6, zorder=4)
    ax.annotate(ARM_LABEL["p1_dab168_kl1"], (bx, by), xytext=(0, 8),
                textcoords="offset points", fontsize=FS_LEG, color=INK,
                ha="center", fontweight="bold")
    # the base sits mid-field, so call-outs go to whichever side has room
    for x_, y_, txt, c in tips:
        ha = "left" if x_ >= bx else "right"
        ax.annotate(txt, (x_, y_), xytext=(4 if ha == "left" else -4, -4),
                    textcoords="offset points", fontsize=FS_LEG, color=c, ha=ha,
                    va="top")
    ax.set_xlabel("donor recovery (lower is better)")
    ax.set_ylabel("cross-donor cycle agreement")
    ax.margins(.18)
    save(fig, "frontier_with_ablations", cite=True)


# ═════════════════════════════════════════════════════════════════════════
# 4. UMAPs, one colouring per file
# ═════════════════════════════════════════════════════════════════════════
PHASE_COARSE = {"menstrual": None, "proliferative_early": "proliferative",
                "proliferative": "proliferative", "proliferative_late": "proliferative",
                "periovulatory": "periovulatory", "secretory_early": "secretory early",
                "secretory_early_mid": "secretory early", "secretory_mid": "secretory late",
                "secretory_late": "secretory late"}
PHASE_ORDER = ["proliferative", "periovulatory", "secretory early", "secretory late"]
PHASE_C = ["#D9A441", "#3A7D5D", "#2F6690", "#6D2E46"]
DIS_ORDER = ["control", "eutopic", "ectopic", "adenomyosis"]
DIS_C = ["#9a8f80", "#b4603e", "#3f7fa6", "#8a5a86"]


def umap_panel(arm: str, colouring: str, cite=False):
    xy = np.load(umap_cache(arm))
    m = meta().iloc[sample_index()].reset_index(drop=True)
    assert len(m) == len(xy)
    studies = list(m.study.value_counts().index)       # largest first, as figure1
    if colouring == "study":
        vals, order, cols = m.study, studies, STUDY_C
        names = [STUDY_NAME[s] for s in order]
    elif colouring == "family":
        vals, order, cols = m["cell family"], FAMS, FAMILY_C
        names = order
    elif colouring == "disease":
        vals, order, cols = m.disease_status, DIS_ORDER, DIS_C
        names = order
    elif colouring == "phase":
        vals, order, cols = m["menstrual phase"].map(PHASE_COARSE), PHASE_ORDER, PHASE_C
        names = order
    else:
        raise ValueError(colouring)
    fig, ax = plt.subplots(figsize=(88 * MM, 72 * MM))
    rng = np.random.default_rng(1)
    perm = rng.permutation(len(m))
    grey = vals.isna().values
    ax.scatter(xy[grey, 0], xy[grey, 1], s=.25, c=GREY_PT, lw=0, rasterized=True)
    cmap = dict(zip(order, cols))
    colour = vals.map(cmap)
    keep = ~grey
    ax.scatter(xy[perm][keep[perm], 0], xy[perm][keep[perm], 1], s=.25,
               c=colour.values[perm][keep[perm]], lw=0, rasterized=True)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title(f"{ARM_LABEL[arm]}, by {colouring}", fontsize=FS_TITLE, loc="left")
    handles = [Line2D([], [], marker="o", lw=0, ms=3.5, color=cmap[o], label=f"{n}")
               for o, n in zip(order, names) if (vals == o).any()]
    if grey.any():
        handles.append(Line2D([], [], marker="o", lw=0, ms=3.5, color=GREY_PT, label="unlabelled"))
    ax.legend(handles=handles, loc="center left", bbox_to_anchor=(1.0, .5), fontsize=FS_LEG,
              handletextpad=.3, borderaxespad=0)
    save(fig, f"umap_{arm}_{colouring}", cite=cite)


def umap_panels():
    """One figure per model: cell family, study, menstrual phase, disease.

    AW, 16 November: "For each model's UMAPs I want to show the following.
    So let's make panelled figures by model", and on 17 November, "Add
    disease status UMAP to all multi-panel UMAPs". Four colourings of ONE
    embedding is a comparison a reader can actually make, because nothing
    moves between the panels except the colour. The four are the paper's
    four questions of a cell: what it is, where it came from, when in the
    cycle it was taken, and whether that person has the disease.

    THE REPORTED ARM IS DRAWN AND NOT CITED. AW, 17 November: "Remove UMAPs
    of ELAJ_B_hi from supplementary. All its UMAPs are available in the main
    prose. Reference those." Main-text Fig. 4 is that latent under nine
    colourings, these four among them, so a supplementary copy is the same
    picture twice. It still lands in the exploratory tier.
    """
    idx = sample_index()
    m_all = meta().iloc[idx].reset_index(drop=True)
    studies = list(m_all.study.value_counts().index)        # largest first
    SPEC = [
        ("cell family", m_all["cell family"], FAMS, FAMILY_C, 2),
        ("study", m_all.study, studies, STUDY_C, 2),
        ("menstrual phase", m_all["menstrual phase"].map(PHASE_COARSE),
         PHASE_ORDER, PHASE_C, 2),
        ("disease status", m_all.disease_status, DIS_ORDER, DIS_C, 2),
    ]
    rng = np.random.default_rng(1)
    perm = rng.permutation(len(m_all))
    for arm in ALL_ARMS:
        cache = umap_cache(arm)
        if not cache.exists():
            print(f"  ! no UMAP cache for {arm}")
            continue
        xy = np.load(cache)
        assert len(xy) == len(m_all), f"{arm}: {len(xy)} points, {len(m_all)} cells"
        # ONE ROW OF FOUR. AW, 17 November: "UMAP panels should be 1x4 not
        # 2x2. All UMAPs are squished, please fix." Two fixes, because the
        # squish and the layout are separate faults: the row is 1x4, and
        # every axes is set to an equal aspect with adjustable="datalim",
        # which widens the data limits to fill the box instead of
        # stretching the embedding to fit it. A UMAP drawn on unequal axes
        # is a different shape from the one the reader is asked to compare.
        fig, axes = plt.subplots(1, 4, figsize=(180 * MM, 70 * MM))
        for pl, (ax, (title, vals, order, cols, ncol)) in zip(
                "abcd", zip(axes.ravel(), SPEC)):
            ax.set_aspect("equal", adjustable="datalim")
            # PANEL LETTERS, because the legends refer to panels by letter,
            # which is what IBDex and scGPT both do and what NMI expects.
            # The title is drawn as text rather than set_title so it can be
            # indented clear of the letter; at loc="left" the two overlap
            # and print "acell family".
            ax.text(-.02, 1.13, pl, transform=ax.transAxes, fontsize=8,
                    fontweight="bold", va="top", ha="left", color=INK)
            cmap = dict(zip(order, cols))
            grey = vals.isna().values
            ax.scatter(xy[grey, 0], xy[grey, 1], s=.18, c=GREY_PT, lw=0, rasterized=True)
            colour = vals.map(cmap)
            keep = (~grey)[perm]
            ax.scatter(xy[perm][keep, 0], xy[perm][keep, 1], s=.18,
                       c=colour.values[perm][keep], lw=0, rasterized=True)
            ax.set_xticks([]); ax.set_yticks([])
            for sp in ax.spines.values():
                sp.set_visible(False)
            ax.text(.09, 1.10, title, transform=ax.transAxes,
                    fontsize=FS_TITLE, va="top", ha="left", color=INK)
            names = ([STUDY_NAME[o] for o in order] if title == "study" else order)
            handles = [Line2D([], [], marker="o", lw=0, ms=3.2, color=cmap[o], label=n)
                       for o, n in zip(order, names) if (vals == o).any()]
            if grey.any():
                handles.append(Line2D([], [], marker="o", lw=0, ms=3.2,
                                      color=GREY_PT, label="unlabelled"))
            ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(.5, -.02),
                      ncol=ncol, fontsize=FS_LEG, handletextpad=.2,
                      columnspacing=.6, borderaxespad=0)
        fig.suptitle(ARM_LABEL[arm], fontsize=FS_TITLE + 1, fontweight="bold",
                     x=.012, ha="left", y=.995)
        fig.subplots_adjust(bottom=.26, top=.86, wspace=.04)
        save(fig, f"umap_panel_{arm}", cite=(arm != ARM))


def umaps(cite_only=False):
    # THE PANELS REPLACED THESE, AND NOW ALL FOUR OF THEM. umap_panels()
    # ships one figure per model carrying family, study, phase AND disease
    # together, so no single-colouring version is cited anywhere and these
    # exist for the exploratory tier alone.
    cited: set[tuple[str, str]] = set()
    for arm in ALL_ARMS:
        if not umap_cache(arm).exists():
            print(f"  ! no UMAP cache for {arm}")
            continue
        for colouring in ("study", "family", "disease", "phase"):
            c = (arm, colouring) in cited
            if cite_only and not c:
                continue
            umap_panel(arm, colouring, cite=c)


# ═════════════════════════════════════════════════════════════════════════
# 5. label transfer
# ═════════════════════════════════════════════════════════════════════════
def transfer():
    t = pd.read_csv(CELLS / ARM / "cell_family_transferred.csv.gz")
    m = meta()
    assert len(t) == len(m)
    tr = t.source == "transferred"
    li = (m.study == "li_2025").values
    gran = li & m.celltype.fillna("").str.startswith("Granulosa").values
    li_imm = li & m.celltype.isin(["Neutrophils", "Macro/Mono", "T/NKT", "DC", "B"]).values

    # validation table, from x1_validation.csv plus the Li rows recomputed here
    v = pd.read_csv(CLAIMS / "x1_validation.csv")
    rows = []
    for _, r in v.iterrows():
        if "->" in r.test:
            a, b = [s.strip() for s in r.test.split("->")]
            rows.append([f"\\texttt{{{esc(a)}}} $\\rightarrow$ \\texttt{{{esc(b)}}}",
                         num(r.accuracy), num(r.balanced), num(r.majority_baseline)])
    gran_strom = (t.cell_family_transferred[gran] == "stromal").mean()
    imm_imm = (t.cell_family_transferred[li_imm] == "immune").mean()
    rows.append([r"\texttt{li\_2025} immune, out of tissue, called immune",
                 num(imm_imm), "--", "--"])
    rows.append([r"\texttt{li\_2025} granulosa, no counterpart, called stromal",
                 num(gran_strom), "--", "--"])
    tex("transfer_validation", tabular("@{}lrrr@{}",
        ["test", "accuracy", "balanced", "majority baseline"], rows, [2]))

    # ── THE REJECTION-RULE AND NEIGHBOURHOOD TABLES ARE GONE. ───────────
    # AW, 17 November, folding this note into Note 3: "Keep one figure and
    # one table that is relevant to the limitation, get rid of the rest."
    # The limitation is that a cell type absent from the reference is
    # absorbed silently, so the table that stays is the validation (it
    # carries both the accuracy and the granulosa failure) and the figure
    # that stays is the distance distribution (it shows why no threshold
    # rescues it). The numbers the folded paragraph quotes are printed
    # here instead, so each one still has a derivation behind it.
    tt = t[tr]
    comp = (pd.crosstab(m.study[tr], t.cell_family_transferred[tr], normalize="index")
            .reindex(columns=FAMS))
    print("       transfer, quoted in Note 3:")
    print(f"         transferred cells                     {int(tr.sum()):,}")
    print(f"         unanimous vote across 25 neighbours   {(tt.vote_fraction == 1).mean() * 100:.1f}%")
    print(f"         mean distance, granulosa              {t.mean_distance[gran].mean():.3f}")
    print(f"         mean distance, li_2025 immune         {t.mean_distance[li_imm].mean():.3f}")
    print(f"         mean distance, other transferred      {t.mean_distance[tr & ~li].mean():.3f}")
    for lab, mask in (("granulosa rejected", gran), ("li_2025 immune lost", li_imm),
                      ("other transferred lost", tr & ~li)):
        print(f"         unanimity rule, {lab:<22} {(t.vote_fraction[mask] < 1.0).mean() * 100:.1f}%")
    print(f"         garcia_alonso_2021_b epithelial       "
          f"{comp.loc['garcia_alonso_2021_b', 'epithelial'] * 100:.1f}%")
    print(f"         li_2025 immune / stromal              "
          f"{comp.loc['li_2025', 'immune'] * 100:.1f}% / {comp.loc['li_2025', 'stromal'] * 100:.1f}%")

    # figures
    fig, ax = fig_ax(88, 55)
    bins = np.linspace(0, 6, 90)
    for mask, c, lab in ((tr & ~li, INK, "all other transferred cells"),
                         (li_imm, FAM_C["immune"], "li_2025 immune (correct)"),
                         (gran, "#8C2D3F", "li_2025 granulosa (no counterpart)")):
        ax.hist(t.mean_distance[mask], bins=bins, density=True, histtype="step", lw=1.1,
                color=c, label=lab)
    ax.set_xlabel("mean distance to the 25 nearest annotated cells")
    ax.set_ylabel("density"); ax.legend(loc="upper right")
    save(fig, "transfer_distance_by_group", cite=True)

    fig, ax = fig_ax(88, 50)
    bins = np.linspace(0.2, 1.0, 21)
    for mask, c, lab in ((tr & ~li, INK, "all other transferred cells"),
                         (li_imm, FAM_C["immune"], "li_2025 immune"),
                         (gran, "#8C2D3F", "li_2025 granulosa")):
        ax.hist(t.vote_fraction[mask], bins=bins, density=True, histtype="step", lw=1.1,
                color=c, label=lab)
    ax.set_xlabel("vote fraction of the winning family among 25 neighbours")
    ax.set_ylabel("density"); ax.set_yscale("log"); ax.legend(loc="upper left")
    save(fig, "transfer_vote_by_group")

    fig, ax = fig_ax(88, 55)
    order = comp.loc[comp.index.isin(m.study.unique())].index
    order = sorted(order, key=lambda s: -tr[m.study.values == s].sum())
    left = np.zeros(len(order))
    for f in FAMS:
        vals = np.array([comp.loc[s, f] for s in order])
        ax.barh(range(len(order)), vals, left=left, color=FAM_C[f], label=f, height=.7)
        left += vals
    ax.set_yticks(range(len(order))); ax.set_yticklabels([STUDY_NAME[s] for s in order])
    ax.invert_yaxis(); ax.set_xlim(0, 1); ax.set_xlabel("share of transferred cells")
    ax.legend(loc="lower right", ncol=4, bbox_to_anchor=(1, 1.0))
    save(fig, "transfer_composition_by_study")

    fig, ax = fig_ax(88, 50)
    frac = pd.Series({s: (tt.n_studies_in_neighbourhood[m.study[tr].values == s] > 1).mean()
                      for s in order})
    ax.barh(range(len(order)), frac[order].values, color="#4C78A8", height=.7)
    ax.set_yticks(range(len(order))); ax.set_yticklabels([STUDY_NAME[s] for s in order])
    ax.invert_yaxis(); ax.set_xlabel("share of neighbourhoods drawing on both annotated studies")
    save(fig, "transfer_two_study_neighbourhoods")


# ═════════════════════════════════════════════════════════════════════════
# 6. the claims axis
# ═════════════════════════════════════════════════════════════════════════
def claims():
    # X3 from its log
    log = (CLAIMS / "x3_all_run.log").read_text().splitlines()
    g = lambda pat: re.search(pat, "\n".join(log))
    ctl = g(r"control\s+donors\s+(\d+)\s+cells\s+(\d+)\s+phases\s+(\d+)\s+agreement\s+([\d.]+)\s+chance\s+([\d.]+)\s+excess\s+([\d.]+)")
    eut = g(r"eutopic\s+donors\s+(\d+)\s+cells\s+(\d+)\s+phases\s+(\d+)\s+agreement\s+([\d.]+)\s+chance\s+([\d.]+)\s+excess\s+([\d.]+)")
    diff = g(r"control - eutopic excess = ([-\d.]+)")
    null = g(r"null\s+mean\s+([+-][\d.]+)\s+sd\s+([\d.]+)\s+95%\s+\[([-+\d.]+),\s*([-+\d.]+)\]")
    pval = g(r"two-sided p = ([\d.]+)\s+\((\d+) permutations\)")
    rows = [["control", ctl.group(1), intc(ctl.group(2)), ctl.group(3), num(ctl.group(4)),
             num(ctl.group(5)), num(ctl.group(6))],
            ["eutopic", eut.group(1), intc(eut.group(2)), eut.group(3), num(eut.group(4)),
             num(eut.group(5)), num(eut.group(6))]]
    tex("x3_cycle_by_disease", tabular("@{}lrrrrrr@{}",
        ["donors", "n", "cells", "phases", "agreement", "chance", "excess"], rows))
    tex("x3_difference", tabular("@{}lr@{}", ["quantity", "value"],
        [["control minus eutopic, excess", num(diff.group(1))],
         ["null mean", num(null.group(1))], ["null s.d.", num(null.group(2))],
         [r"null 95\% interval", f"{num(null.group(3))} to {num(null.group(4))}"],
         ["two-sided $P$", num(pval.group(1), 3)], ["permutations", intc(pval.group(2))]]))

    # X3b
    x3b = pd.read_csv(CLAIMS / "x3b_results.csv")
    # THE INTERACTION ROW IS SHIFTED ONE COLUMN LEFT in x3b_results.csv: the
    # script wrote eight fields under nine headers, so from `eta2_eutopic`
    # onward the values are F, null mean, null 95th percentile, P and the
    # permutation count. EXPERIMENTS.md records the same five numbers.
    inter = x3b[x3b.eta2_control == "pooled_interaction"].iloc[0]
    tex("x3b_interaction", tabular("@{}lr@{}", ["quantity", "value"],
        [["donors", str(int(inter.n_donors))], ["interaction $F$, phase $\\times$ disease",
                                                  num(float(inter.eta2_eutopic), 3)],
         ["null mean $F$", num(float(inter.difference), 3)],
         ["null 95th percentile", num(float(inter.null_mean), 3)],
         ["$P$", num(float(inter.null_sd), 3)],
         ["permutations", intc(int(inter.p_one_sided))]]))

    # X8 / X9 / severity composition
    c = pd.read_csv(CLAIMS / "x8_x9_composition.csv")
    # ONLY THE LESION CONTRAST KEEPS A TABLE. AW, 17 November: "The claims
    # axis note is about the claims not discussed in the main prose. Remove
    # the stuff about severity. Also remove any other claims discussed in
    # detail in the prose." Results gives the control-against-eutopic test
    # and the severity test with all four P values each, so both fragments
    # and both figures went; the eutopic-against-lesion contrast appears
    # nowhere in the main text and stays. The two dropped contrasts are
    # still PRINTED here, so the claims ledger's outcome column has a
    # derivation behind it.
    for contrast, a, b, cols, tag in (
            ("control_vs_eutopic", "mean_control", "mean_eutopic", ["control", "eutopic"], None),
            ("eutopic_vs_ectopic", "mean_eutopic", "mean_ectopic", ["eutopic", "ectopic"], "x9_composition"),
            ("severity_low_vs_high", "mean_low", "mean_high", ["low severity", "high severity"], None)):
        sub = c[c.contrast == contrast].set_index("family").loc[FAMS]
        rows = [[f, num(sub.loc[f, a], 3), num(sub.loc[f, b], 3), num(sub.loc[f, "F"], 3),
                 num(sub.loc[f, "p"], 4) if sub.loc[f, "p"] > 0 else "$<$ 0.0001"] for f in FAMS]
        if tag:
            tex(tag, tabular("@{}lrrrr@{}", ["family", f"mean share, {cols[0]}",
                                             f"mean share, {cols[1]}", "$F$", "$P$"], rows))
        else:
            print(f"       {contrast} (no fragment, Results carries it): "
                  + ", ".join(f"{f} P={sub.loc[f, 'p']:.4f}" for f in FAMS))
        print(f"       {contrast}: {int(sub.n_donors.iloc[0])} donors")

    # X12 step A, both label sources
    for src, tag in (("annotated", "x12_auc_annotated"), ("transferred", "x12_auc_transferred")):
        d = pd.read_csv(CLAIMS / f"x12_by_family_{src}.csv")
        rows = [[r.family.lower() if r.family != "ALL FAMILIES" else "all families, pooled",
                 str(int(r.n_donors)), f"{int(r.n_control)} / {int(r.n_case)}",
                 num(r.auc), f"{r.auc_lo:.3f} to {r.auc_hi:.3f}", num(r.null), num(r.p, 3)]
                for _, r in d.iterrows()]
        tex(tag, tabular("@{}lrrrrrr@{}",
            ["compartment", "donors", "ctl / case", "held-out AUC", r"95\% interval",
             "shuffled AUC", "$P$"], rows))
    q = pd.read_csv(CLAIMS / "x12_direction_quality.csv").iloc[0]
    tex("x12_global", tabular("@{}lr@{}", ["quantity", "value"],
        [["donor records", str(int(q.n_donors))], ["held-out AUC, global direction", num(q.auc_heldout)],
         ["shuffled-label AUC", num(q.auc_null)], ["share of shuffles above observed", num(q.share_null_above, 2)],
         ["cosine stability of the direction across splits", num(q.cosine_stability)]]))

    # X12 step B: ranked shifts and external replication
    gs = pd.read_csv(CLAIMS / "x12_gene_ranking.csv")
    gs = gs.rename(columns={gs.columns[0]: "gene"})
    gs["shift_towards_disease"] = -gs.shift_towards_control
    gs = gs.sort_values("shift_towards_disease", ascending=False).reset_index(drop=True)
    ext = pd.read_csv(CLAIMS / "replication_external.csv")
    hits = set(str(ext.loc[ext.end == "disease side", "genes"].fillna("").iloc[0]).split(";")) - {""}
    fold = {g_: float(ext.loc[ext.end == "disease side", f"fold_{g_}"].iloc[0]) for g_ in hits}
    # EMPTY until re-established. The four "never reported" genes (SIGLEC7,
    # ADAMDEC1, ALPK2, KCNH1) came from the ranking decoded with the epoch-9
    # decoder against epoch-4 latents (decode_dx_61604807, found 17 Nov); none
    # is in the top 15 of the corrected ranking, and novelty for the new top
    # 15 has not been checked.
    novel: set[str] = set()
    top = gs.head(15)
    rows = []
    for i, r in top.iterrows():
        rows.append([str(i + 1), r.gene, num(r.shift_towards_disease),
                     (f"{fold[r.gene]:.2f}" if r.gene in hits else "--"),
                     ("none found" if r.gene in novel else "")])
    tex("x12_top_genes", tabular("@{}rlrrl@{}",
        ["rank", "gene", "shift towards disease", "external up-list, fold",
         "indexed report"], rows))
    bottom = gs.tail(15).iloc[::-1]
    tex("x12_bottom_genes", tabular("@{}rlr@{}", ["rank", "gene", "shift towards control"],
        [[str(len(gs) - i), r.gene, num(-r.shift_towards_disease)] for i, r in bottom.iterrows()]))
    # NO FRAGMENT. AW, 17 November: "What point is Table S28 supposed to
    # make?? There are barely any numbers there." Two rows under six
    # headings, four of them dashes. The four values that matter are now in
    # the note's own sentence and in the figure's legend, and they are
    # printed here so each still has a derivation.
    for _, r in ext.iterrows():
        print(f"       replication, {r.end}: {int(r.hits)} of {int(r.n_top)} "
              f"on a {int(r.external_n)}-gene list, P={r.p_hypergeometric:.2e}")

    # THE CURVE, NOT THE GENE NAMES. AW, 17 November: "S33 is very messy."
    # It was: fifteen labels fanned out of one corner on leader lines that
    # crossed each other, because all fifteen sit inside the first 0.1% of
    # the x axis. The names are already in Tables S26 and S27, and drawing
    # them again is the table-in-colours fault one more time. What only a
    # figure can say here is the SHAPE: the decoder's response is flat
    # across fourteen thousand genes and turns hard at both ends, and the
    # external replication is entirely on one of those ends.
    fig, ax = fig_ax(110, 58)
    x = np.arange(len(gs)); yv = gs.shift_towards_disease.values
    ax.plot(x, yv, color=INK, lw=.9, zorder=2)
    ax.axhline(0, color=HAIR, lw=.5)
    for i, r in gs.head(15).iterrows():
        c = "#8C2D3F" if r.gene in hits else (AMBER if r.gene in novel else SOFT)
        ax.plot(i, r.shift_towards_disease, "o", color=c, ms=3.4, mec="white",
                mew=.35, zorder=3)
    for i, r in gs.tail(15).iterrows():
        ax.plot(i, r.shift_towards_disease, "o", color=SOFT, ms=3.0, mec="white",
                mew=.35, zorder=3)
    # one bracket per end, carrying the count that is the whole point
    lo, hi = ax.get_ylim()
    n_top = int(ext.loc[ext.end == "disease side", "hits"].iloc[0])
    n_bot = int(ext.loc[ext.end == "control side", "hits"].iloc[0])
    word = lambda k: "none replicates" if k == 0 else f"{k} replicate{'s' if k == 1 else ''} externally"
    ax.annotate(f"top 15, Table S26\n{word(n_top)}", xy=(0, yv[0]),
                xytext=(len(gs) * .10, yv[0] - (hi - lo) * .04),
                fontsize=FS_BODY, color="#8C2D3F", va="top", ha="left",
                linespacing=1.4,
                arrowprops=dict(arrowstyle="-", color="#8C2D3F", lw=.5))
    ax.annotate(f"bottom 15, Table S27\n{word(n_bot)}", xy=(len(gs) - 1, yv[-1]),
                xytext=(len(gs) * .90, yv[-1] + (hi - lo) * .04),
                fontsize=FS_BODY, color=SOFT, va="bottom", ha="right",
                linespacing=1.4,
                arrowprops=dict(arrowstyle="-", color=SOFT, lw=.5))
    ax.set_xlabel("genes ranked by decoder response to the immune disease direction (15,496)")
    ax.set_ylabel("shift towards disease")
    ax.legend(handles=[Line2D([], [], marker="o", lw=0, color="#8C2D3F", ms=3.4,
                              label="on the external up-regulated list"),
                       Line2D([], [], marker="o", lw=0, color=AMBER, ms=3.4,
                              label="no prior endometriosis report"),
                       Line2D([], [], marker="o", lw=0, color=SOFT, ms=3.0,
                              label="other end-of-ranking genes")],
              loc="upper center", bbox_to_anchor=(.5, -.20), ncol=3, fontsize=FS_LEG)
    save(fig, "x12_gene_ranking", cite=True)

    # PER-FAMILY AUC, AS A FOREST PLOT WITH ITS NUMBERS ALIGNED BESIDE IT.
    # The form is IBDex Fig. 2c, which AW named as the visualisation his
    # supervisor responded to: the effect and its interval on the left, the
    # values in columns on the right, and the rows that do not clear their
    # null greyed and badged rather than silently left to the reader. It
    # suits this result because the finding is a CONTRAST between five
    # compartments and their own shuffled-label nulls, not one number.
    for src in ("annotated", "transferred"):
        d = pd.read_csv(CLAIMS / f"x12_by_family_{src}.csv")
        d["name"] = d.family.str.lower().replace({"all families": "all families, pooled"})
        d = d.sort_values("auc").reset_index(drop=True)
        # SIZED SO THE TYPE SURVIVES, as for scib_metric_range. AW, 17
        # November: "S31 and S32 are unreadable." The columns run to axes
        # fraction 1.65, so a 155 mm axes made a 264 mm figure that
        # \textwidth scaled to 0.61, putting every number at 3.4 pt.
        fig, ax = plt.subplots(figsize=(88 * MM, 58 * MM))
        for sp in ("top", "right", "left"):
            ax.spines[sp].set_visible(False)
        y = np.arange(len(d))
        for yi, r in d.iterrows():
            sig = r.p < 0.05
            c = FAM_C.get(r["name"], "#6F7681") if sig else "#B9BEC6"
            ax.plot([r.auc_lo, r.auc_hi], [yi, yi], color=c, lw=1.6,
                    solid_capstyle="round", zorder=2)
            ax.plot(r.auc, yi, "o", ms=6, color=c, mec="white", mew=.8, zorder=3)
            ax.plot(r.null, yi, "|", ms=10, color="#8C2D3F", mew=1.3, zorder=4)
        ax.axvline(.5, color=INK, lw=.7)
        ax.set_yticks(y); ax.set_yticklabels(d.name)
        ax.set_xlim(.28, .92)
        ax.set_xlabel("held-out AUC, control against eutopic")
        cols = [(1.06, "AUC"), (1.21, "95% interval"), (1.40, "shuffled"),
                (1.52, "$P$"), (1.65, "donors")]
        for x, head in cols:
            ax.text(x, 1.06, head, transform=ax.transAxes,
                    fontsize=FS_BODY, fontweight="bold", ha="center", color=INK)
        for yi, r in d.iterrows():
            yy = (yi + 0.5) / len(d)
            grey = r.p >= 0.05
            tc = SOFT if grey else INK
            for x, val in ((1.06, f"{r.auc:.4f}"),
                           (1.21, f"{r.auc_lo:.3f} to {r.auc_hi:.3f}"),
                           (1.40, f"{r.null:.4f}"),
                           (1.65, f"{int(r.n_donors)}")):
                ax.text(x, yy, val, transform=ax.transAxes, fontsize=FS_BODY,
                        ha="center", va="center", color=tc)
            # THE VALUE IS ALWAYS PRINTED. IBDex replaces P with an "ns"
            # badge, but endothelial sits at exactly 0.050 here and hiding
            # that behind a badge is the one case where a badge misleads.
            # The badge marks the row; the number stays readable.
            ax.text(1.52, yy, f"{r.p:.3f}", transform=ax.transAxes,
                    fontsize=FS_BODY, ha="center", va="center", color=tc,
                    fontweight="normal" if grey else "bold")
            if grey:
                ax.text(1.567, yy, "ns", transform=ax.transAxes, fontsize=FS_LEG,
                        ha="left", va="center", color="white", fontweight="bold",
                        bbox=dict(boxstyle="round,pad=0.18", fc="#C2777C", ec="none"))
        ax.legend(handles=[Line2D([], [], marker="o", lw=0, ms=6, color="#6F7681",
                                  label="held-out AUC, with its 95% interval"),
                           Line2D([], [], marker="|", lw=0, ms=10, mew=1.3,
                                  color="#8C2D3F", label="shuffled-label AUC"),
                           Line2D([], [], marker="o", lw=0, ms=6, color="#B9BEC6",
                                  label="does not clear its null")],
                  loc="upper center", bbox_to_anchor=(.33, -.22), ncol=3, fontsize=FS_LEG)
        save(fig, f"x12_auc_by_family_{src}", cite=True)

    # composition strips, three contrasts, from D3
    d3 = pd.read_csv(OUT / "data/D3_per_donor_cell_family_composition.csv", low_memory=False)
    endo = d3[d3.tissue == "endometrium"]
    # dropna=False, or every control donor vanishes: severity_cases_only is
    # NaN for controls and pandas drops NaN grouping keys by default.
    per = (endo.groupby(["patient_id", "disease_status", "severity_cases_only", "cell_family"],
                        dropna=False).n_cells.sum().reset_index())
    tot = per.groupby("patient_id").n_cells.transform("sum")
    per["fraction"] = per.n_cells / tot
    lesion = d3[d3.disease_status.isin(["eutopic", "ectopic"])]
    perL = lesion.groupby(["patient_id", "disease_status", "cell_family"]).n_cells.sum().reset_index()
    perL["fraction"] = perL.n_cells / perL.groupby(["patient_id", "disease_status"]).n_cells.transform("sum")

    def strips(df, groupcol, groups, cols, fname, note, cite=False):
        fig, ax = fig_ax(88, 55)
        rng = np.random.default_rng(3)
        for fi, f in enumerate(FAMS):
            for gi, g_ in enumerate(groups):
                v = df[(df.cell_family == f) & (df[groupcol] == g_)].fraction.values
                x0 = fi + (gi - .5) * .36
                ax.plot(x0 + rng.uniform(-.1, .1, len(v)), v, "o", ms=1.6, color=cols[gi],
                        alpha=.55, mec="none")
                ax.plot([x0 - .14, x0 + .14], [np.median(v)] * 2, color=INK, lw=1.0)
        ax.set_xticks(range(4)); ax.set_xticklabels(FAMS)
        ax.set_ylabel("share of a donor's cells"); ax.set_ylim(-.02, 1.02)
        ax.legend(handles=[Line2D([], [], marker="o", lw=0, color=c, label=f"{g_} ({int(df[df[groupcol]==g_].patient_id.nunique())} donors)")
                           for g_, c in zip(groups, cols)] +
                          [Line2D([], [], color=INK, lw=1, label="median")], loc="upper right", fontsize=FS_LEG)
        ax.text(.01, .98, note, transform=ax.transAxes, va="top", fontsize=FS_LEG, color=SOFT)
        save(fig, fname, cite=cite)

    strips(per, "disease_status", ["control", "eutopic"], ["#9a8f80", "#b4603e"],
           "composition_control_vs_eutopic", "endometrium; transferred and annotated labels")
    strips(perL, "disease_status", ["eutopic", "ectopic"], ["#b4603e", "#3f7fa6"],
           "composition_eutopic_vs_ectopic", "eutopic endometrium against lesion tissue",
           cite=True)
    sev = per[per.severity_cases_only.notna()].copy()
    strips(sev, "severity_cases_only", sorted(sev.severity_cases_only.unique()),
           ["#8fc2d6", "#9e3b25"], "composition_by_severity", "patients only, endometrium")

    # X14
    x14 = pd.read_csv(CLAIMS / "x14_tissue_within_family.csv").set_index("family").loc[FAMS]
    tex("x14_tissue", tabular("@{}lrrrrrr@{}",
        ["family", "(donor, tissue) units", "endometrium", "lesion", "AUC", "shuffled AUC", "$P$"],
        [[f, str(int(r.units)), str(int(r.n_endometrium)), str(int(r.n_lesion)), num(r.auc),
          num(r.null), num(r.p, 3)] for f, r in x14.iterrows()]))
    fig, ax = fig_ax(88, 40)
    y = np.arange(4)
    ax.barh(y, x14.auc - .5, left=.5, color=[FAM_C[f] for f in FAMS], height=.62)
    ax.plot(x14.null, y, "|", color="#8C2D3F", ms=9, mew=1.2, label="shuffled-label AUC")
    for yi, (f, r) in zip(y, x14.iterrows()):
        ax.text(.72, yi, f"P = {r.p:.3f}", va="center", fontsize=FS_LEG, color=SOFT)
    ax.axvline(.5, color=INK, lw=.6); ax.set_yticks(y); ax.set_yticklabels(FAMS)
    ax.set_xlim(.4, .8); ax.set_xlabel("AUC, endometrium against lesion tissue, within one family")
    ax.legend(loc="lower right")
    save(fig, "x14_tissue_within_family")


# ═════════════════════════════════════════════════════════════════════════
# 7. X13
# ═════════════════════════════════════════════════════════════════════════
def x13():
    obs = pd.read_csv(CLAIMS / "x13_marker_reproducibility.csv").set_index("family").loc[FAMS]
    nul = pd.read_csv(CLAIMS / "x13_marker_reproducibility_null.csv")
    rows = []
    for f in FAMS:
        n = nul[nul.family == f]
        rows.append([f, str(int(obs.loc[f, "n_shared_genes"])), str(int(obs.loc[f, "overlap_n"])),
                     num(obs.loc[f, "overlap_jaccard"], 3), num(obs.loc[f, "spearman"]),
                     str(int(n.overlap_n.max())), f"{n.spearman.min():+.3f} to {n.spearman.max():+.3f}".replace("-", "$-$")])
    tex("x13_reproducibility", tabular("@{}lrrrrrr@{}",
        ["family", "shared genes", "top-100 overlap", "Jaccard", r"Spearman $\rho$",
         "null max overlap", r"null $\rho$ range (20 shuffles)"], rows))
    # ONE FIGURE, TWO PANELS. AW, 17 November: "What is the point of
    # S35/S36? They are illegible. Either improve them or remove them."
    # They were two separate figures in the same layout saying the same
    # thing on two scales, each drawn at 88 x 45 mm with grey type. The
    # point is worth keeping: the observed agreement does not sit at the
    # edge of the null, it sits nowhere near it, and that gap is what a
    # table of two numbers cannot show. So they become one wider figure
    # with both scales side by side, in ink rather than grey.
    fig, axes = plt.subplots(1, 2, figsize=(165 * MM, 56 * MM))
    y = np.arange(4)
    rng = np.random.default_rng(2)
    for pl, (ax, (col, xl)) in zip("ab", zip(axes, (
            ("overlap_n", "genes shared between the two\nstudies' top hundred"),
            ("spearman", "rank correlation over the 13,034\njointly measured genes")))):
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        ax.text(-.14, 1.10, pl, transform=ax.transAxes, fontsize=8,
                fontweight="bold", va="top", ha="left", color=INK)
        for yi, f in zip(y, FAMS):
            n = nul[nul.family == f][col].values
            ax.plot(n, yi + rng.uniform(-.16, .16, len(n)), "o", ms=2.6, color=SOFT,
                    alpha=.75, mec="none")
            ax.plot(obs.loc[f, col], yi, "o", ms=6, color=FAM_C[f], mec="white",
                    mew=.6, zorder=3)
        ax.set_yticks(y); ax.set_yticklabels(FAMS, fontsize=FS_BODY, color=INK)
        ax.tick_params(axis="x", labelcolor=INK, labelsize=FS_BODY + .5)
        ax.set_xlabel(xl, fontsize=FS_BODY, color=INK, linespacing=1.5)
        ax.margins(y=.22)
    axes[0].legend(handles=[
        Line2D([], [], marker="o", lw=0, ms=6, color=INK,
               label="observed, coloured by family"),
        Line2D([], [], marker="o", lw=0, ms=2.6, color=SOFT,
               label="twenty within-study label shuffles")],
        loc="upper center", bbox_to_anchor=(1.12, -.46), ncol=2, fontsize=FS_BODY)
    fig.subplots_adjust(wspace=.22, bottom=.40)
    save(fig, "x13_vs_null", cite=True)


# ═════════════════════════════════════════════════════════════════════════
# 8. the corpus, its labels, and the null widths
# ═════════════════════════════════════════════════════════════════════════
def corpus():
    m = meta()
    g = m.groupby("study")
    cov = pd.DataFrame({
        "cells": g.size(), "donors": g.patient_id.nunique(),
        "family": g["cell family"].apply(lambda s: s.notna().sum()),
        "phase": g["menstrual phase"].apply(lambda s: s.notna().sum()),
        "cycle day": g.CycleDay.apply(lambda s: s.notna().sum()),
        "progesterone": g.ProgesteroneSerum.apply(lambda s: s.notna().sum()),
        "pseudotime": g["epithelial.pseudotime"].apply(lambda s: s.notna().sum()),
        "rASRM stage": g.Endometriosis_stage.apply(lambda s: s.notna().sum()),
        "grade": g.EndometriosisGrade.apply(lambda s: s.notna().sum()),
        "cell cycle": g.phase.apply(lambda s: s.notna().sum()),
    }).sort_values("cells", ascending=False)
    labs = ["family", "phase", "cycle day", "progesterone", "pseudotime", "rASRM stage", "grade", "cell cycle"]
    rows = []
    for s, r in cov.iterrows():
        rows.append([f"\\texttt{{{esc(s)}}}", intc(r.cells), str(int(r.donors))] +
                    [intc(r[l]) if r[l] else "--" for l in labs])
    rows.append([r"\textbf{all}", intc(cov.cells.sum()), str(int(m.patient_id.nunique()))] +
                [intc(cov[l].sum()) for l in labs])
    tex("label_coverage", tabular("@{}lrr" + "r" * len(labs) + "@{}",
        ["study", "cells", "donor ids"] + labs, rows, [len(rows) - 1]))

    # corpus composition
    dis = g.apply(lambda d: d.groupby("disease_status").patient_id.nunique())
    dis = dis.unstack(fill_value=0) if isinstance(dis, pd.Series) else dis.fillna(0)
    rows = []
    for s in cov.index:
        tissues = ", ".join(sorted(m.tissue[m.study == s].unique()))
        plat = ", ".join(sorted(m.platform[m.study == s].unique()))
        dd = " / ".join(f"{int(dis.loc[s, c])}" for c in ["control", "eutopic", "ectopic", "adenomyosis"]
                        if c in dis.columns)
        rows.append([f"\\texttt{{{esc(s)}}}", STUDY_NAME[s], intc(cov.loc[s, "cells"]),
                     str(int(cov.loc[s, "donors"])), dd, esc(tissues), esc(plat).replace("′", "$'$")])
    tex("corpus", tabular("@{}llrrlp{30mm}l@{}",
        ["key", "study", "cells", "donor ids", "ctl / eut / ect / adeno",
         "tissues", "platform"], rows))

    # REDESIGNED 16 November. AW: "Figure S7 makes no sense. The information
    # is worth conveying but the way it has been presented is misleading."
    # He is right. The old panel drew each label as a SHARE OF ITS OWN
    # STUDY, so every filled cell read 100% and a cohort of 10,240 cells
    # looked exactly as well covered as one of 466,176. The quantity a
    # reader needs is the opposite: how much of the CORPUS carries each
    # label, and how few studies that comes from. One stacked bar per
    # label, segmented by study, says both at once.
    order_by_size = list(cov.index)
    colour = {sname: STUDY_C[i] for i, sname in enumerate(order_by_size)}
    fig, ax = plt.subplots(figsize=(135 * MM, 62 * MM))
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    TOTAL = int(cov.cells.sum())
    ypos = np.arange(len(labs))[::-1]
    for yi, lab in zip(ypos, labs):
        left = 0
        for sname in order_by_size:
            v = int(cov.loc[sname, lab])
            if not v:
                continue
            ax.barh(yi, v / 1e6, left=left / 1e6, height=.62,
                    color=colour[sname], edgecolor="white", lw=.4)
            left += v
        n_studies = int((cov[lab] > 0).sum())
        ax.text(left / 1e6 + .02, yi,
                f"{left/1e6:.2f} M  ({100*left/TOTAL:.0f}% of cells), "
                f"{n_studies} stud{'y' if n_studies == 1 else 'ies'}",
                va="center", fontsize=FS_BODY, color=INK)
    ax.axvline(TOTAL / 1e6, color=INK, lw=.7, ls=":")
    ax.text(TOTAL / 1e6, len(labs) - .3, " the whole corpus", fontsize=FS_BODY,
            color=SOFT, va="top")
    ax.set_yticks(ypos); ax.set_yticklabels(labs)
    ax.set_xlim(0, TOTAL / 1e6 * 1.12)
    ax.set_xlabel("cells carrying the label (millions), coloured by the study that supplied them")
    ax.legend(handles=[Line2D([], [], marker="s", lw=0, ms=4, color=colour[sname],
                              label=STUDY_NAME[sname]) for sname in order_by_size
                       if (cov.loc[sname, labs] > 0).any()],
              loc="upper center", bbox_to_anchor=(.5, -.20), ncol=4, fontsize=FS_LEG)
    save(fig, "label_coverage_by_study", cite=True)

    fig, ax = fig_ax(88, 50)
    order = cov.index
    ax.barh(range(len(order)), cov.cells / 1e3, color=[STUDY_C[i] for i in range(len(order))], height=.7)
    for i, s in enumerate(order):
        ax.text(cov.cells[s] / 1e3 + 4, i, f"{int(cov.donors[s])} donor ids", va="center", fontsize=FS_LEG, color=SOFT)
    ax.set_yticks(range(len(order))); ax.set_yticklabels([STUDY_NAME[s] for s in order])
    ax.invert_yaxis(); ax.set_xlabel("cells (thousands)"); ax.set_xlim(0, 560)
    save(fig, "corpus_cells_and_donors")        # no note inputs it; exploratory tier

    # cycle-day coverage, one cohort
    fig, ax = fig_ax(88, 40)
    cd = m.loc[m.CycleDay.notna(), ["CycleDay", "patient_id"]].drop_duplicates()
    counts = cd.groupby("CycleDay").patient_id.nunique().reindex(range(5, 31), fill_value=0)
    ax.bar(counts.index, counts.values, color="#5BA3A0")
    # A DAY WITH NO DONOR HAS A ZERO-HEIGHT BAR, so the old caption's "red
    # marks the four absent days" marked something invisible. The gaps are
    # the point, so they are drawn rather than coloured.
    missing = [int(d) for d, v in counts.items() if v == 0]
    for d in missing:
        ax.axvspan(d - .45, d + .45, color="#F2D7D5", zorder=0)
        ax.plot(d, 0.12, marker="x", ms=4, mew=1.2, color="#8C2D3F", zorder=3)
    ax.set_xlabel("cycle day (duempelmann_2026, 60 donors, one sample each)")
    ax.set_ylabel("donors"); ax.set_xticks(range(5, 31, 5))
    ax.set_ylim(0, max(counts.values) + .6)
    ax.legend(handles=[Line2D([], [], marker="x", lw=0, ms=4, mew=1.2,
                              color="#8C2D3F", label=f"no donor sampled ({len(missing)} days)")],
              loc="upper right")
    save(fig, "cycle_day_coverage", cite=True)

    # null widths against donor count, every cross-donor row of the reported arm
    rows_ = []
    for scope, path in (("held out", BENCH / "full/full_p1_dab168_kl1/benchmark.csv"),
                        ("whole corpus", BENCH / "whole_corpus/wholecorpus_p1_dab168_kl1/benchmark.csv")):
        rr = bench_rows(path)
        for (t, l), r in rr.items():
            if t != "cross-donor":
                continue
            p = rr.get(("cross-donor-p", l))
            rows_.append(dict(scope=scope, label=l, donors=note_donors(r["note"]),
                              null95=note_field(r["note"], "null95"), value=float(r["value"]),
                              p=float(p["value"]) if p else np.nan))
    wc = ROOT / "Outputs/validate/p1_dab168_kl1_full/validation.csv"
    for r in csv.DictReader(open(wc)):
        if r["test"] == "cross-donor":
            rows_.append(dict(scope="whole corpus (validation)", label=r["label"],
                              donors=note_donors(r["note"]), null95=note_field(r["note"], "null95"),
                              value=float(r["value"]), p=note_field(r["note"], "p")))
    nw = pd.DataFrame(rows_).dropna(subset=["donors"])
    # severity (study vocabularies) agrees on a level by agreeing on a study
    # (NUMBERS.md: DO NOT QUOTE); the validation pass repeats stage and grade.
    nw = nw[~((nw.label == "severity (study vocabularies)")
              | ((nw.scope == "whole corpus (validation)") & nw.label.isin(["Endometriosis_stage", "EndometriosisGrade"])))]
    nw["null95"] = nw.null95.abs()
    pretty = {"menstrual phase": "cycle", "cell family": "family", "severity": "severity (merged)",
              "severity (patients only)": "severity, patients only", "Endometriosis_stage": "rASRM stage",
              "EndometriosisGrade": "grade", "severity (study vocabularies)": "severity (study vocabularies)"}
    nw["label"] = nw.label.map(pretty).fillna(nw.label)
    nw = nw.sort_values(["scope", "donors"])
    # NO TABLE HERE. AW, 17 November: "Remove table S8." The null widths
    # were a table and a figure of the same numbers, and the figure is the
    # one that carries the point, which is the shape of the narrowing. `nw`
    # is still built because the figure below is drawn from it.
    # ONE LINE PER LABEL, ACROSS ITS SCOPES. AW, 16 November: "Can figure 9
    # have held-out, whole corpus, and whole corpus validation connected by
    # a line for each variable? It would perform the job a visualisation is
    # supposed to do over a table: helping numbers become interpretable at
    # scale." Every label is measured twice, on few held-out donors and on
    # many whole-corpus ones, so each line is one label's null narrowing as
    # donors arrive. The table gives the values; this gives the shape.
    fig, ax = plt.subplots(figsize=(110 * MM, 66 * MM))
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    SCOPE_C = {"held out": "#8C2D3F", "whole corpus": AMBER,
               "whole corpus (validation)": "#2F6690"}
    for lab, g in nw.groupby("label"):
        g = g.sort_values("donors")
        if len(g) > 1:
            ax.plot(g.donors, g.null95, "-", color=HAIR, lw=1.0, zorder=1)
        for _, r in g.iterrows():
            ax.plot(r.donors, r.null95, "o", ms=5, color=SCOPE_C[r.scope],
                    mec="white", mew=.6, zorder=3)
        # LABEL THE HELD-OUT END. The whole-corpus points pile into a band
        # under 0.12 and their labels overlapped; the held-out ends are
        # spread from 0.06 to 0.42, which is the spread the figure is about.
        first = g.iloc[0]
        ax.annotate(lab, (first.donors, first.null95), xytext=(-7, 0),
                    textcoords="offset points", fontsize=FS_BODY, color=INK,
                    va="center", ha="right")
    ax.set_xscale("log")
    ax.set_xlim(7, 260)
    ax.set_xticks([10, 20, 40, 70, 120, 200])
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.minorticks_off()
    ax.set_xlabel("donors carrying the label (log scale)")
    ax.set_ylabel("permutation null, 95th percentile")
    ax.legend(handles=[Line2D([], [], marker="o", lw=0, ms=5, color=c, label=k)
                       for k, c in SCOPE_C.items()] +
                      [Line2D([], [], color=HAIR, lw=1.0, label="the same label, both scopes")],
              loc="upper right", fontsize=FS_LEG)
    save(fig, "null_width_vs_donors", cite=True)

    # the seven-sample overlap table, parsed from the donor-overlap audit
    md = (CLAIMS / "salvage/donor_overlap_58542096/donor_overlap.md").read_text().splitlines()
    rows = []
    for line in md:
        mm = re.match(r"\| `(\S+)` \| (\w+) ([\d,]+) \| (\w+) ([\d,]+) \|", line)
        if mm:
            rows.append([f"\\texttt{{{esc(mm.group(1))}}}", f"{mm.group(2)} ({mm.group(3)})",
                         f"{mm.group(4)} ({mm.group(5)})"])
    tex("split_overlap", tabular("@{}lll@{}",
        ["sample", r"in \texttt{garcia\_alonso\_2021\_a}", r"in \texttt{garcia\_alonso\_2021\_b}"], rows))

    # gene-group sizes
    d5 = pd.read_csv(OUT / "data/D5_pathway_groups_and_genes.csv")
    # D5's `group_idx` is a gene's position inside its group; the group is `group`.
    sizes = d5.groupby("group").size()
    assert len(sizes) == 44 and sizes.min() == 247 and sizes.max() == 493, sizes.describe()
    fig, ax = fig_ax(88, 42)
    ax.hist(sizes, bins=np.arange(240, 510, 10), color="#4C78A8")
    ax.axvline(250, color=INK, lw=.6, ls=":"); ax.axvline(500, color=INK, lw=.6, ls=":")
    ax.set_xlabel("genes in group (44 groups; dotted lines at the 250 and 500 construction bounds)")
    ax.set_ylabel("groups")
    save(fig, "group_sizes")        # no note inputs it; exploratory tier

    # per-study purity for the reported arm
    rr = bench_rows(BENCH / "full/full_p1_dab168_kl1/benchmark.csv")
    pur = {l: (float(r["value"]), note_field(r["note"], "mixed")) for (t, l), r in rr.items()
           if t == "study-purity" and l != "all studies"}
    order = sorted(pur, key=lambda s: -pur[s][0])
    fig, ax = fig_ax(88, 50)
    ax.barh(range(len(order)), [pur[s][0] for s in order], color="#9AA3AD", height=.7,
            label="own-study share of 30 neighbours")
    ax.plot([pur[s][1] for s in order], range(len(order)), "|", color="#8C2D3F", ms=9, mew=1.2,
            label="perfectly mixed share (study's size)")
    ax.set_yticks(range(len(order))); ax.set_yticklabels([STUDY_NAME[s] for s in order])
    ax.invert_yaxis(); ax.set_xlim(0, 1); ax.set_xlabel("study purity, held-out cells, ELAJ B$_{hi}$")
    ax.legend(loc="lower right")
    save(fig, "study_purity_per_study")        # no note inputs it; exploratory tier


# ═════════════════════════════════════════════════════════════════════════
# ═════════════════════════════════════════════════════════════════════════
# 9. X15, the pathway groups: what each one carries on its own
# ═════════════════════════════════════════════════════════════════════════
PROBE = ROOT / "Outputs/probes/p1_groups/stages.csv"
D5 = ROOT / "Outputs/supplementary/data/D5_pathway_groups_and_genes.csv"
CHANCE = {"cell family": 0.673, "menstrual phase": 0.370}


def group_short(name: str) -> str:
    """`reactome_complement_cascade_plus_9_more` -> `complement cascade (+9)`.

    The group keys are built from the Reactome or GO term they were cut
    from plus a count of what was merged in, and some run to 140
    characters. A figure needs the term and the merge count and nothing
    else.
    """
    n = re.sub(r"^(reactome|go)_", "", name)
    n = re.sub(r"_r_hsa_\d+", "", n)
    n = re.sub(r"_go_\d+", "", n)
    m = re.search(r"_plus_(\d+)_more$", n)
    extra = f" (+{m.group(1)})" if m else ""
    n = re.sub(r"_plus_\d+_more$", "", n)
    m2 = re.search(r"_(\d+)_pathways(_\d+)?$", n)
    if m2:
        extra = f" ({m2.group(1)} pathways)" + (f" {m2.group(2)[1:]}" if m2.group(2) else "")
        n = re.sub(r"_\d+_pathways(_\d+)?$", "", n)
    return n.replace("_", " ") + extra


def x15_read():
    """The probe, with a stable G01..G44 id per group and its gene count.

    IDS ARE THE MODEL'S OWN ORDER, not the score order. A group's id has to
    mean the same thing in every figure and every sentence, and a
    score-ordered id would change the moment the model is re-scored.
    """
    d = pd.read_csv(PROBE)
    g = d[d.method.str.startswith("group/")].copy()
    g["grp"] = g.method.str.replace("group/", "", regex=False)
    p = g.pivot_table(index="grp", columns="label", values="value")
    p.columns = ["family", "phase"]
    d5 = pd.read_csv(D5)
    p["n_genes"] = d5.groupby("group").size()
    order = d5.groupby("group").global_idx.min().sort_values()
    p["gid"] = [f"G{list(order.index).index(k) + 1:02d}" for k in p.index]
    p["short"] = [group_short(k) for k in p.index]
    assert len(p) == 44 and p.n_genes.notna().all(), "44 groups with sizes"
    lat = d[d.method == "latent"]
    L = {l: float(lat[(lat.test == "knn-agreement") & (lat.label == l)].value.iloc[0])
         for l in ("cell family", "menstrual phase")}
    return p.sort_values("gid"), L


def x15():
    p, L = x15_read()
    lf, lp = L["cell family"], L["menstrual phase"]

    # ── the table the note reads from ────────────────────────────────────
    rows = [[r.gid, esc(r.short), str(int(r.n_genes)), num(r.family), num(r.phase)]
            for _, r in p.iterrows()]
    tex("x15_groups", tabular("@{}llrrr@{}",
        ["id", "pathway group", "genes", "cell family", "menstrual phase"], rows))

    # ── FIGURE 1. every group ranked, with the latent drawn through them ──
    # AW asked for a Pareto. A Pareto needs the parts to SUM to the whole
    # and these do not: each value is how well one group recovers the label
    # on its own, and the groups overlap heavily, so the top 20% of them
    # hold 24.5% of the sum on both labels and the cumulative curve is a
    # straight line. The question behind the request is answerable and this
    # is the shape that answers it: how many single groups come close to
    # what the whole latent does.
    fig, axes = plt.subplots(1, 2, figsize=(170 * MM, 96 * MM))
    for ax, (col, lv, title, pl) in zip(axes, (
            ("family", lf, "cell family", "a"),
            ("phase", lp, "menstrual phase", "b"))):
        q = p.sort_values(col, ascending=False)
        y = np.arange(len(q))
        ax.hlines(y, 0, q[col].values, color="#C3C8CF", lw=1.0, zorder=1)
        ax.scatter(q[col].values, y, s=11, color=FAM_C["immune"] if col == "phase"
                   else FAM_C["stromal"], zorder=3, lw=0)
        ax.axvline(lv, color=INK, lw=1.1, zorder=4)
        ax.text(lv, -1.6, f"the 16-number latent, {lv:.3f}", fontsize=FS_LEG,
                color=INK, ha="right", va="bottom", rotation=0)
        ax.set_yticks(y); ax.set_yticklabels(q.gid, fontsize=4.4)
        ax.invert_yaxis()
        ax.set_xlim(0, 1.0); ax.set_xlabel(f"{title}, excess over chance")
        ax.set_title(f"{pl}  {title}", fontsize=FS_TITLE, loc="left",
                     fontweight="bold")
        n80 = int((q[col] >= lv * 0.8).sum())
        ax.text(.02, .02, f"{n80} of 44 groups reach 80%\nof the latent on their own",
                transform=ax.transAxes, fontsize=FS_LEG, va="bottom",
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=HAIR, lw=.5))
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    fig.subplots_adjust(wspace=.30, bottom=.11, top=.93)
    save(fig, "x15_groups_ranked", cite=True)

    # ── FIGURE 2. identity against time, which is where the biology is ───
    # Phase regressed on family. The residual is the phase signal a group
    # carries BEYOND its general informativeness, which is the only way to
    # name a cycle-carrying pathway given the two correlate at +0.665.
    b_, a_ = np.polyfit(p.family, p.phase, 1)
    p = p.assign(resid=p.phase - (a_ + b_ * p.family))
    fig, ax = fig_ax(120, 84)
    xs = np.linspace(p.family.min() - .03, p.family.max() + .03, 50)
    ax.plot(xs, a_ + b_ * xs, color=SOFT, lw=.9, ls="--", zorder=1)
    above = p.resid > 0
    ax.scatter(p.family[above], p.phase[above], s=22, color=FAM_C["immune"],
               lw=.4, edgecolor="white", zorder=3)
    ax.scatter(p.family[~above], p.phase[~above], s=22, color=GREY_PT,
               lw=.4, edgecolor="white", zorder=3)
    lab = pd.concat([p.nlargest(4, "resid"), p.nsmallest(3, "resid")])
    # short enough that a label never runs off the axes; the id carries the
    # identification and the table carries the full name.
    def tag(r):
        w = r.short.split(" (")[0].split()
        n = 2 if len(" ".join(w[:2])) > 11 else 3
        return f"{r.gid} " + " ".join(w[:n])
    pts = [(r.family, r.phase, tag(r),
            FAM_C["immune"] if r.resid > 0 else SOFT) for _, r in lab.iterrows()]
    ax.margins(.16)
    label_points(ax, pts, fontsize=FS_LEG, gap=7.0)
    ax.set_xlabel("cell family, excess over chance")
    ax.set_ylabel("menstrual phase, excess over chance")
    r2 = np.corrcoef(p.family, p.phase)[0, 1] ** 2
    ax.text(.02, .97, f"$R^2$ = {r2:.3f}\nslope {b_:.2f}", transform=ax.transAxes,
            va="top", fontsize=FS_BODY, color=INK, linespacing=1.5,
            bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=HAIR, lw=.5))
    ax.legend(handles=[
        Line2D([], [], marker="o", lw=0, ms=4.5, color=FAM_C["immune"],
               label="more cycle than its identity score predicts"),
        Line2D([], [], marker="o", lw=0, ms=4.5, color=GREY_PT,
               label="less"),
        Line2D([], [], color=SOFT, lw=.9, ls="--", label="least-squares fit")],
        loc="lower right", fontsize=FS_LEG)
    save(fig, "x15_identity_vs_time", cite=True)

    # ── the readings the prose quotes, printed so each has a derivation ──
    print("       X15, quoted in the note:")
    for col, lv, nm in (("family", lf, "cell family"), ("phase", lp, "menstrual phase")):
        ch = CHANCE[nm]
        raw = lambda x: ch + x * (1 - ch)
        print(f"         {nm}: latent {lv:.4f} (raw {raw(lv):.3f}), best group "
              f"{p[col].max():.4f} (raw {raw(p[col].max()):.3f}), "
              f"median {p[col].median():.4f}, min {p[col].min():.4f}")
        for f in (0.95, 0.9, 0.8):
            print(f"           {int((p[col] >= lv * f).sum()):2d} of 44 reach {f:.0%} of the latent")
    print(f"         phase >= family in {int((p.phase >= p.family).sum())} of 44 groups")
    print(f"         size vs score: family rho={spearmanr(p.family, p.n_genes)[0]:+.3f} "
          f"P={spearmanr(p.family, p.n_genes)[1]:.3f}; "
          f"phase rho={spearmanr(p.phase, p.n_genes)[0]:+.3f} "
          f"P={spearmanr(p.phase, p.n_genes)[1]:.3f}")
    print(f"         phase-on-family R2={r2:.3f}")
    print("         cycle-specific (top residual): "
          + ", ".join(f"{r.gid} {r.short}" for _, r in p.nlargest(4, "resid").iterrows()))
    print("         identity-only (bottom residual): "
          + ", ".join(f"{r.gid} {r.short}" for _, r in p.nsmallest(3, "resid").iterrows()))
    x15_propagation()



def x15_propagation():
    """Where cell identity and the cycle appear as a cell moves through.

    AW asked for a diagram of how the phase and family signal propagates.
    Everything annotated on it is measured: the group-stage spreads come
    from the X15 probe, the latent-stage values from the same probe's
    integrity row, and the dimensionality of each label at the latent from
    the X16 discriminant decomposition.
    """
    p_, L = x15_read()
    fig, ax = plt.subplots(figsize=(170 * MM, 86 * MM))
    ax.set_xlim(0, 100); ax.set_ylim(0, 54); ax.axis("off")
    box = dict(boxstyle="round,pad=0.45", lw=.9)
    FAMC, PHC = FAM_C["stromal"], FAM_C["immune"]

    def stage(x, w, title, sub):
        ax.add_patch(plt.Rectangle((x, 30), w, 14, fc="#F2F4F6", ec=HAIR, lw=.8,
                                   zorder=1))
        ax.text(x + w / 2, 40.5, title, ha="center", va="center",
                fontsize=FS_TITLE, fontweight="bold", color=INK)
        ax.text(x + w / 2, 35.0, sub, ha="center", va="center",
                fontsize=FS_LEG, color=SOFT, linespacing=1.4)

    stage(2, 20, "15,496 genes", "one measurement\nper gene, per cell")
    stage(32, 26, "44 pathway groups", "247 to 493 genes each\n288 numbers out of each")
    stage(70, 26, "16 dimensions", "everything the model\nkeeps about a cell")
    for x0, x1 in ((22.6, 31.4), (58.6, 69.4)):
        ax.annotate("", (x1, 37), (x0, 37),
                    arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.3))
    ax.text(27, 39.4, "sorted by\npathway", ha="center", fontsize=FS_LEG,
            color=SOFT, linespacing=1.3)
    ax.text(64.5, 39.4, "combined", ha="center", fontsize=FS_LEG, color=SOFT)

    # ── what each stage can tell you, measured ───────────────────────────
    ax.text(1, 25.5, "what you could read off, at each stage:", fontsize=FS_BODY,
            color=INK, fontweight="bold")
    for i, (lab, c, gmed, gmin, gmax, lv, reach, dims) in enumerate((
            ("cell family", FAMC, p_.family.median(), p_.family.min(), p_.family.max(),
             L["cell family"], 17, "3 balanced axes"),
            ("menstrual phase", PHC, p_.phase.median(), p_.phase.min(), p_.phase.max(),
             L["menstrual phase"], 2, "1 axis, 63% of it"))):
        y = 18.5 - i * 11
        ax.text(1, y + 3.0, lab, fontsize=FS_BODY, color=c, fontweight="bold")
        # group-stage range bar, drawn on a 0..1 scale mapped into the column
        gx0, gw = 32, 26
        ax.plot([gx0 + gmin * gw, gx0 + gmax * gw], [y, y], color=c, lw=3,
                solid_capstyle="round", alpha=.45, zorder=2)
        ax.plot([gx0 + gmed * gw], [y], "o", ms=6, color=c, mec="white", mew=.8, zorder=3)
        ax.text(gx0 + gmax * gw + 1.0, y, f"best {gmax:.2f}", fontsize=FS_LEG,
                color=SOFT, va="center")
        ax.text(gx0, y - 3.4, f"median {gmed:.2f} across the 44", fontsize=FS_LEG, color=SOFT)
        lx0, lw_ = 70, 26
        ax.plot([lx0 + lv * lw_], [y], "D", ms=7, color=c, mec="white", mew=.8, zorder=3)
        ax.text(lx0 + lv * lw_ + 1.2, y, f"{lv:.2f}", fontsize=FS_BODY, color=c,
                va="center", fontweight="bold")
        ax.text(lx0, y - 3.4, f"{dims};  {reach} of 44 groups get\nthis far on their own",
                fontsize=FS_LEG, color=SOFT, linespacing=1.3)
    ax.text(1, 2.2, "Bars are the range across the 44 groups and the circle is their median, "
                    "on the scale each column spans (0 to 1,\nexcess over chance). Diamonds "
                    "are the finished latent. Identity is already there group by group; the "
                    "cycle is not in any of them.",
            fontsize=FS_LEG, color=INK, linespacing=1.5)
    ax.legend(handles=[
        Line2D([], [], color=INK, lw=3, alpha=.45, label="range over the 44 groups"),
        Line2D([], [], marker="o", lw=0, ms=6, color=INK, label="median group"),
        Line2D([], [], marker="D", lw=0, ms=7, color=INK, label="the 16-dimensional latent")],
        loc="upper right", bbox_to_anchor=(1.0, .60), fontsize=FS_LEG, frameon=False)
    save(fig, "x15_propagation", cite=True)

# ═════════════════════════════════════════════════════════════════════════
# 10. X16, the cycle as one continuous axis, and whose axis it is
# ═════════════════════════════════════════════════════════════════════════
PHASE_ORD = {"menstrual": 0, "proliferative_early": 1, "proliferative": 2,
             "proliferative_late": 3, "periovulatory": 4, "secretory_early": 5,
             "secretory_early_mid": 6, "secretory_mid": 7, "secretory_late": 8}


def _cycle_setup():
    """The latent, z-scored, with the cycle axes fitted OFF duempelmann.

    THE FIT NEVER SEES THE TEST COHORT. Cycle day and serum progesterone
    exist only in duempelmann_2026, so the discriminant is fitted on the
    phase labels of marecko_2024 and the two garcia_alonso deposits alone.
    Everything measured against day or progesterone is therefore out of
    cohort as well as out of sample, and neither variable was ever an input
    to the model: phase was supervised as a label, the day behind it and the
    hormone behind that were not.
    """
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
    rng = np.random.default_rng(0)
    Z = np.load(CELLS / ARM / "latent.npy")
    m = pd.read_csv(CELLS / ARM / "metadata.csv.gz", low_memory=False)
    Zs = (Z - Z.mean(0)) / Z.std(0)
    has = m["menstrual phase"].notna().values
    fit = has & (m.study != "duempelmann_2026").values
    idx = rng.choice(np.flatnonzero(fit), 150_000, replace=False)
    lda = LDA(solver="eigen", shrinkage="auto").fit(Zs[idx], m["menstrual phase"].values[idx])
    W = lda.scalings_[:, :2]
    W = W / np.linalg.norm(W, axis=0, keepdims=True)
    return Zs, m, W, lda.explained_variance_ratio_, rng


def x16():
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
    Zs, m, W, ev, rng = _cycle_setup()
    has = m["menstrual phase"].notna().values
    te = (m.study == "duempelmann_2026").values & m.CycleDay.notna().values
    pr = Zs[te] @ W[:, 0]
    dn = pd.DataFrame({"proj": pr, "day": m.CycleDay.values[te],
                       "prog": m.ProgesteroneSerum.values[te],
                       "ph": m["menstrual phase"].values[te],
                       "pid": m.patient_id.values[te]}).groupby("pid").median(numeric_only=True)
    # orientation is arbitrary in a discriminant; point it along rising day
    sgn = np.sign(spearmanr(dn.proj, dn.day)[0]) or 1.0
    dn["proj"] *= sgn
    r_day, p_day = spearmanr(dn.proj, dn.day)
    r_pg, p_pg = spearmanr(dn.proj, dn.prog)
    ph_first = (pd.DataFrame({"pid": m.patient_id.values[te],
                              "ph": m["menstrual phase"].values[te]})
                .groupby("pid").ph.first())
    dn["coarse"] = ph_first.reindex(dn.index).map(PHASE_COARSE)

    # ── FIGURE a/b: the axis against two variables the model never saw ───
    fig, axes = plt.subplots(1, 2, figsize=(165 * MM, 68 * MM))
    for ax, (col, xl, r_, p_, pl) in zip(axes, (
            ("day", "cycle day recorded by the clinic", r_day, p_day, "a"),
            ("prog", "serum progesterone (nmol/l)", r_pg, p_pg, "b"))):
        # COLOURED BY THE DONOR'S OWN PHASE LABEL (AW, 17 Nov: this is
        # Figure 2 candidate C2, moved to Note 3), so a reader sees the axis
        # resolve order inside a label as well as across labels
        for ph_, c_ in zip(PHASE_ORDER, PHASE_C):     # not p_: that is the P value
            s_ = dn[dn.coarse == ph_]
            ax.scatter(s_[col], s_.proj, s=16, color=c_, lw=.4,
                       edgecolor="white", zorder=3)
        s_ = dn[dn.coarse.isna()]
        ax.scatter(s_[col], s_.proj, s=16, color="#9AA3AE", lw=.4,
                   edgecolor="white", zorder=3)
        ax.set_xlabel(xl); ax.set_ylabel("position on the cycle axis")
        ax.text(.03, .97, f"Spearman $\\rho$ = {r_:+.3f}\n$P$ = {p_:.1e}, n = {len(dn)} donors",
                transform=ax.transAxes, va="top", fontsize=FS_BODY, linespacing=1.5,
                bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=HAIR, lw=.5))
        ax.set_title(f"{pl}", fontsize=FS_TITLE, loc="left", fontweight="bold")
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    fig.legend(handles=[Line2D([], [], marker="o", lw=0, ms=4, color=c_, label=ph_)
                        for ph_, c_ in zip(PHASE_ORDER, PHASE_C)],
               loc="lower center", ncol=len(PHASE_ORDER), fontsize=FS_LEG,
               bbox_to_anchor=(.5, .0), frameon=False)
    fig.subplots_adjust(wspace=.28, bottom=.24)
    save(fig, "x16_cycle_axis_external", cite=True)

    # ── FIGURE: the cycle closes ─────────────────────────────────────────
    # NO SIGN FLIP IN THIS FRAME. `sgn` orients the 1-D projection so the
    # scatters above read left to right with the cycle; applying it to one
    # of two axes would MIRROR the plane, which reverses the direction of
    # rotation and destroys the very ordering this test is about. That bug
    # took the resultant from 0.80 to 0.26 before it was caught.
    Pa = Zs[has] @ W
    cen = (pd.DataFrame({"a": Pa[:, 0], "b": Pa[:, 1],
                         "ph": m["menstrual phase"].values[has]})
           .groupby("ph").mean())
    cen["ord"] = cen.index.map(PHASE_ORD)
    cen = cen.sort_values("ord")
    ang = np.degrees(np.arctan2(cen.b, cen.a)) % 360

    def resultant(a_rad, o):
        """Reflection-invariant: a cycle traced clockwise is still a cycle.

        The statistic is the mean resultant length of the phase angles
        minus an evenly spaced ramp in label order. Taking the better of
        the ramp and its reverse makes it blind to which way round the
        loop runs, and the null below takes the same maximum, so nothing
        is gained by the extra degree of freedom.
        """
        k = 2 * np.pi * np.asarray(o) / len(o)
        return max(float(np.abs(np.mean(np.exp(1j * (a_rad - k))))),
                   float(np.abs(np.mean(np.exp(1j * (a_rad + k))))))

    ar = np.radians(ang.values)
    obs = resultant(ar, cen["ord"].values)
    null = [resultant(ar, rng.permutation(cen["ord"].values)) for _ in range(20000)]
    pcirc = float(np.mean(np.array(null) >= obs))

    fig, ax = fig_ax(104, 92)
    cm = plt.get_cmap("twilight")
    ax.plot(list(cen.a) + [cen.a.iloc[0]], list(cen.b) + [cen.b.iloc[0]],
            color=SOFT, lw=.9, ls="-", zorder=1, alpha=.8)
    for i, (k, r) in enumerate(cen.iterrows()):
        ax.scatter(r.a, r.b, s=70, color=cm(i / len(cen)), lw=.6,
                   edgecolor="white", zorder=3)
    pts = [(r.a, r.b, k.replace("_", " "), INK) for k, r in cen.iterrows()]
    label_points(ax, pts, fontsize=FS_LEG, gap=7.5)
    ax.axhline(0, color=HAIR, lw=.4); ax.axvline(0, color=HAIR, lw=.4)
    ax.margins(.22)
    ax.set_xlabel(f"cycle axis 1 ({ev[0]:.0%} of phase separation)")
    ax.set_ylabel(f"cycle axis 2 ({ev[1]:.0%})")
    ax.text(.03, .97, f"labels advance round the circle in\nbiological order: "
                      f"resultant {obs:.2f}, $P$ = {pcirc:.4f}",
            transform=ax.transAxes, va="top", fontsize=FS_BODY, linespacing=1.5,
            bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=HAIR, lw=.5))
    save(fig, "x16_cycle_closes", cite=True)

    # ── per family: whose cycle axis is it? ──────────────────────────────
    fam = m["cell family"].values
    both = has & m["cell family"].notna().values
    axd = {}
    for f in FAMS:
        sel = np.flatnonzero(both & (fam == f) & (m.study != "duempelmann_2026").values)
        if len(sel) < 4000:
            continue
        sel = rng.choice(sel, min(60_000, len(sel)), replace=False)
        lf = LDA(solver="eigen", shrinkage="auto").fit(Zs[sel], m["menstrual phase"].values[sel])
        v = lf.scalings_[:, 0]
        axd[f] = v / np.linalg.norm(v)
    ks = list(axd)
    M = np.array([[abs(float(axd[x] @ axd[y])) for y in ks] for x in ks])
    fig, ax = fig_ax(78, 70)
    im = ax.imshow(M, cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks(range(len(ks))); ax.set_xticklabels(ks, rotation=35, ha="right")
    ax.set_yticks(range(len(ks))); ax.set_yticklabels(ks)
    for i in range(len(ks)):
        for jj in range(len(ks)):
            ax.text(jj, i, f"{M[i, jj]:.2f}", ha="center", va="center",
                    fontsize=FS_BODY, color="white" if M[i, jj] > .6 else INK)
    ax.set_title("alignment between each family's own cycle axis",
                 fontsize=FS_TITLE, loc="left")
    for sp in ax.spines.values():
        sp.set_visible(False)
    save(fig, "x16_family_cycle_axes", cite=True)

    # ── THE NUMBERS GO TO A FILE BOTH AUDITORS READ. ────────────────────
    # A number the prose quotes must be a value some file holds. X16 is
    # computed here rather than on the cluster, so without this the
    # auditors see 0.757 and 0.844 in Results and have nothing to check
    # them against, which is exactly the hole audit_numbers.py exists to
    # close. Same destination as the X13 and X14 outputs.
    # does the axis resolve cycle day INSIDE one phase label?
    within = []
    for ph, sub in pd.DataFrame({"proj": pr, "day": m.CycleDay.values[te],
                                 "ph": m["menstrual phase"].values[te],
                                 "pid": m.patient_id.values[te]}).groupby("ph"):
        dsub = sub.groupby("pid").median(numeric_only=True)
        if len(dsub) >= 8 and dsub.day.nunique() > 3:
            rr, pp = spearmanr(dsub.proj, dsub.day)
            within.append((f"cycle axis vs cycle day within the {ph} label",
                           abs(rr), pp, len(dsub)))
    out = pd.DataFrame([
        ("cycle axis vs cycle day, donor medians", r_day, p_day, len(dn)),
        ("cycle axis vs serum progesterone, donor medians", r_pg, p_pg, len(dn)),
        ("phase separation on cycle axis 1", ev[0], np.nan, int(has.sum())),
        ("phase separation on cycle axis 2", ev[1], np.nan, int(has.sum())),
        ("phase centroids advance in biological order, resultant", obs, pcirc, len(cen)),
    ] + within, columns=["quantity", "value", "p", "n"])
    _sec = ["periovulatory", "secretory_early", "secretory_early_mid",
            "secretory_mid", "secretory_late"]
    _pro = ["menstrual", "proliferative_early", "proliferative", "proliferative_late"]
    out.loc[len(out)] = ("secretory arc span, degrees",
                         round(float(ang[_sec[-1]] - ang[_sec[0]])), np.nan, len(_sec))
    _pa = np.array([ang[k] for k in _pro])
    _pa = np.where(_pa > 180, _pa - 360, _pa)
    out.loc[len(out)] = ("proliferative arc span, degrees",
                         round(float(_pa.max() - _pa.min())), np.nan, len(_pro))
    for f, v in zip(ks, [abs(float(axd[k] @ W[:, 0])) for k in ks]):
        out.loc[len(out)] = (f"{f} cycle axis vs the pooled cycle axis, abs cosine",
                             v, np.nan, 0)
    for i, x in enumerate(ks):
        for y in ks[i + 1:]:
            out.loc[len(out)] = (f"{x} vs {y} cycle axis, abs cosine",
                                 abs(float(axd[x] @ axd[y])), np.nan, 0)
    dest = CLAIMS / "x16_cycle_axis.csv"
    out.to_csv(dest, index=False)
    print(f"  csv  {dest.name}  ({len(out)} rows)")

    print("       X16, quoted in the note:")
    print(f"         cycle axis vs cycle day, 60 donors:  rho={r_day:+.3f} P={p_day:.1e}")
    print(f"         cycle axis vs serum progesterone:    rho={r_pg:+.3f} P={p_pg:.1e}")
    print(f"         phase separation on axis 1 / axis 2: {ev[0]:.3f} / {ev[1]:.3f}")
    print(f"         the loop closes: resultant {obs:.3f}, permutation P={pcirc:.4f}")
    sec = ["periovulatory", "secretory_early", "secretory_early_mid",
           "secretory_mid", "secretory_late"]
    print(f"         secretory arm spans {ang[sec[-1]] - ang[sec[0]]:.0f} degrees, "
          f"strictly ordered: {all(ang[sec[i]] < ang[sec[i+1]] for i in range(4))}")
    for i, x in enumerate(ks):
        for y in ks[i + 1:]:
            print(f"         |cos| {x} vs {y}: {abs(float(axd[x] @ axd[y])):.3f}")
    for k, v in axd.items():
        print(f"         |cos| {k} vs pooled axis: {abs(float(v @ W[:, 0])):.3f}")



GROUPS = {"scib": scib, "field": field, "arms": arms, "transfer": transfer,
          "claims": claims, "x13": x13, "corpus": corpus, "umaps": umaps,
          "umap_panels": umap_panels, "x15": x15, "x16": x16}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", default="", help="comma-separated group names")
    ap.add_argument("--no-umaps", action="store_true")
    ap.add_argument("--umaps-cited-only", action="store_true",
                    help="draw only the UMAP panels a Note cites")
    a = ap.parse_args()
    groups = [g for g in a.only.split(",") if g] or list(GROUPS)
    for g in groups:
        if g == "umaps" and a.no_umaps:
            continue
        print(f"[{g}]")
        if g == "umaps":
            umaps(cite_only=a.umaps_cited_only)
        else:
            GROUPS[g]()
    mb = sum(p.stat().st_size for p in WRITTEN) / 1048576
    print(f"\n{len(WRITTEN)} figures, {mb:.0f} MB -> {EXPLORE}")
    print(f"cited figures -> {FIG};  tables -> {TAB}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
