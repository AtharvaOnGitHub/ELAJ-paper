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

FS_TITLE, FS_BODY = 6.5, 5.5
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
    rows = []
    for m in SCIB_ORDER:
        d = disc.loc[m]
        verdict = ("constant" if d.degenerate else
                   "near-constant" if d.spread < 0.05 else "discriminates")
        rows.append([SCIB_SHORT[m], SCIB_HALF[m], SCIB_WHAT[m], num(d["min"]),
                     num(d["max"]), num(d.spread), verdict])
    tex("scib_discrimination", tabular("@{}llp{52mm}rrrl@{}",
        ["metric", "half", "rewards", "min", "max", "range", "on this corpus"],
        rows, [5]))

    # heatmap
    fig, ax = fig_ax(120, 62)
    vals = card.values.astype(float)
    im = ax.imshow(vals, cmap="Greys", vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(range(10)); ax.set_xticklabels([SCIB_SHORT[m] for m in SCIB_ORDER],
                                                   rotation=40, ha="right")
    ax.set_yticks(range(11)); ax.set_yticklabels([DISPLAY[r] for r in REP_ORDER])
    for i in range(11):
        for j in range(10):
            v = vals[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                    color="white" if v > 0.6 else INK, fontsize=4.6)
    for j, m in enumerate(SCIB_ORDER):
        if disc.loc[m].degenerate:
            ax.add_patch(plt.Rectangle((j - .5, -.5), 1, 11, fill=False,
                                       ec=AMBER, lw=1.0))
    ax.axvline(4.5, color=INK, lw=.8)
    ax.text(2, -1.1, "batch half", ha="center", fontsize=FS_TITLE)
    ax.text(7, -1.1, "bio half", ha="center", fontsize=FS_TITLE)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    cb = fig.colorbar(im, ax=ax, fraction=.03, pad=.02)
    cb.ax.tick_params(length=2, labelsize=FS_BODY)
    cb.outline.set_visible(False)
    save(fig, "scib_scorecard_heatmap", cite=True)

    # spread per metric
    fig, ax = fig_ax(88, 55)
    y = np.arange(10)[::-1]
    for i, m in enumerate(SCIB_ORDER):
        d = disc.loc[m]
        c = AMBER if d.degenerate else ("#B279A2" if d.spread < .05 else INK)
        ax.plot([d["min"], d["max"]], [y[i], y[i]], color=c, lw=2.2, solid_capstyle="butt")
        ax.plot([card.loc["ELAJ_B_hi", m]], [y[i]], marker="o", ms=3.2, color=AMBER,
                mec="white", mew=.4, zorder=3)
        if d.degenerate:
            ax.plot([d["min"]], [y[i]], marker="|", ms=7, color=AMBER, mew=1.2)
    ax.set_yticks(y); ax.set_yticklabels([SCIB_SHORT[m] for m in SCIB_ORDER])
    ax.axhline(4.5, color=HAIR, lw=.5, ls=":")
    ax.set_xlim(-.02, 1.02); ax.set_xlabel("score across eleven representations")
    ax.text(1.0, 7.3, "batch", ha="right", color=SOFT)
    ax.text(1.0, 2.0, "bio", ha="right", color=SOFT)
    ax.legend(handles=[Line2D([], [], color=INK, lw=2.2, label="range over eleven"),
                       Line2D([], [], color=AMBER, lw=0, marker="o", ms=3.2,
                              label="ELAJ B$_{hi}$"),
                       Line2D([], [], color=AMBER, lw=0, marker="|", ms=7, mew=1.2,
                              label="constant across all eleven")],
              loc="upper center", bbox_to_anchor=(.5, -.18), ncol=3)
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
    bio = [m for m in SCIB_ORDER if SCIB_HALF[m] == "bio" and not disc.loc[m].degenerate]
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
              loc="upper left")
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
        for m in meth:
            ours = m == "p1_dab168_kl1"
            ax.plot(xs[m], ys[m], "o", ms=4.5 if ours else 3.4,
                    color=AMBER if ours else INK, mec="white", mew=.4, zorder=3)
            ax.annotate(name(m), (xs[m], ys[m]), xytext=(3, 2), textcoords="offset points",
                        fontsize=4.8, color=AMBER if ours else SOFT)
        rho, p = spearmanr([xs[m] for m in meth], [ys[m] for m in meth])
        ax.text(.02, .97, f"Spearman $\\rho$ = {rho:+.3f}, $P$ = {p:.3f}, n = {len(meth)}",
                transform=ax.transAxes, va="top", fontsize=FS_BODY, color=SOFT)
        if logx:
            ax.set_xscale("log")
        ax.set_xlabel(xl); ax.set_ylabel(yl)
        save(fig, fname, cite=cite)
        return rho, p

    r1 = scatter(width, phase, "representation width (dimensions, log)",
                 "cross-donor cycle agreement", "field_width_vs_cycle", logx=True, cite=True)
    r2 = scatter(donor, disease, "donor recovery (lower is better)",
                 "cross-donor disease agreement", "field_donor_vs_disease", cite=True)
    r3 = scatter(donor, phase, "donor recovery (lower is better)",
                 "cross-donor cycle agreement", "field_donor_vs_cycle", cite=True)
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
    save(fig, "field_severity_vs_null", cite=True)
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

    # ── registered predictions. READ FROM MARKDOWN, declared here. ──────
    # a-series: axw1008/docs/paper/ABLATIONS.md, "The wave" table (bands in
    # benchmark terms). p-series: RETRAIN_EXPECTATIONS.md lines 145-151.
    A_PRED = {  # arm: {axis: (lo, hi)}
        "a1_nophase": {"phase": (0.45, 0.62), "family": (0.975, 0.985), "donor": (0.48, 0.56)},
        "a1_noecs": {"family": (0.94, 0.975), "donor": (0.48, 0.58)},
        "a1_clsonly": {"family": (0.955, 0.978), "phase": (0.66, 0.73)},
        "a1_nodns": {"donor": (0.50, 0.58), "family": (0.96, 0.98)},
        "a1_randgroups": {"family": (0.93, 0.97), "phase": (0.62, 0.72)},
    }
    P_PRED = {
        "p1_dab7_kl1": {"family": (0.965, 1.0), "phase": (0.62, 1.0), "donor": (0.55, 0.65)},
        "p1_dab168_kl1": {"family": (0.960, 1.0), "phase": (0.58, 0.65), "donor": (0.48, 0.58)},
        "p1_dab7_kl30": {"family": (0.955, 0.970), "phase": (0.55, 0.62), "donor": (0.42, 0.50)},
        "p1_dab336_kl30": {"family": (0.94, 0.96), "phase": (0.0, 0.55), "donor": (0.0, 0.40)},
        "p1_dab168_kl30": {"family": (0.955, 0.967), "phase": (0.55, 0.60), "donor": (0.38, 0.44)},
    }
    AXK = {"phase": ("cross-donor", "menstrual phase"), "family": ("cross-donor", "cell family"),
           "donor": ("knn-agreement", "patient_id")}
    for tag, PRED in (("ablation_predictions", A_PRED), ("arms_predictions", P_PRED)):
        rows, hits, n = [], 0, 0
        for arm, bands in PRED.items():
            for ax_, (lo, hi) in bands.items():
                v = float(D[arm][AXK[ax_]])
                hit = lo <= v <= hi
                hits += hit; n += 1
                band = (f"$\\geq$ {lo:.3f}" if hi >= 1.0 else
                        f"$\\leq$ {hi:.2f}" if lo == 0.0 else f"{lo:.3f} to {hi:.3f}")
                rows.append([ARM_TEX[arm], {"phase": "cycle", "family": "family",
                                            "donor": "donor"}[ax_],
                             band, num(v), "landed" if hit else "missed"])
        tex(tag, tabular("@{}llrrl@{}", ["arm", "axis", "registered band", "observed", ""], rows))
        print(f"       {tag}: {hits} of {n} bands landed")

    # ── loss curves ──────────────────────────────────────────────────────
    for series, arms_, cmap, fname in (("p", P_ARMS, None, "training_loss_pseries"),
                                        ("a", ["p1_dab168_kl1"] + A_ARMS, A_C,
                                         "training_loss_ablations")):
        fig, ax = fig_ax(88, 60)
        for arm in arms_:
            m = metrics(arm)
            c = (A_C.get(arm, AMBER) if series == "a" else
                 KLC[dict((k, w) for k, _, w in table1.P_SERIES)[arm]])
            ls = "-" if series == "a" or arm.endswith("kl1") else "-"
            ax.plot(m.epoch, m.val_nb, color=c, lw=1.1, ls=ls, label=ARM_LABEL[arm])
            ax.plot(m.epoch, m.train_nb, color=c, lw=.7, ls=":", alpha=.9)
            b = m.val_nb.idxmin()
            ax.plot(m.epoch[b], m.val_nb[b], "o", color=c, ms=3.2, mec="white", mew=.4)
        ax.set_xlabel("epoch"); ax.set_ylabel("negative-binomial loss per cell")
        h, l = ax.get_legend_handles_labels()
        h += [Line2D([], [], color=INK, lw=1.1, label="held-out (solid)"),
              Line2D([], [], color=INK, lw=.7, ls=":", label="training (dotted)"),
              Line2D([], [], color=INK, marker="o", lw=0, ms=3.2, label="selected checkpoint")]
        ax.legend(handles=h, loc="upper center", bbox_to_anchor=(.5, -.22), ncol=3,
                  fontsize=4.8)
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
            fig, ax = fig_ax(88, 58)
            for arm in arms_:
                m = metrics(arm)
                c = (A_C.get(arm, AMBER) if series == "a" else
                     KLC[dict((k, w) for k, _, w in table1.P_SERIES)[arm]])
                mk = "o" if series == "a" or arm.endswith("kl1") else "s"
                ax.plot(m.epoch, m[col], color=c, lw=1.0, marker=mk, ms=2.4,
                        mec="white", mew=.3, label=ARM_LABEL[arm])
                b = m.val_nb.idxmin()
                ax.plot(m.epoch[b], m[col][b], marker=mk, ms=5.5, color=c, mfc="none", mew=.9)
            ax.set_xlabel("epoch"); ax.set_ylabel(ylabel)
            h, l = ax.get_legend_handles_labels()
            h.append(Line2D([], [], marker="o", mfc="none", color=INK, lw=0, ms=5.5,
                            label="selected checkpoint (min val$_{nb}$)"))
            ax.legend(handles=h, fontsize=4.8, ncol=3, loc="upper center",
                      bbox_to_anchor=(.5, -.22))
            save(fig, f"{fname}_{fname2}", cite=(col == "val_phase_knn_xdonor"))

    # reliance ratio and hours
    fig, ax = fig_ax(88, 50)
    rel = {a: metrics(a).val_reliance_ratio[metrics(a).val_nb.idxmin()] for a in ALL_ARMS}
    cols = [AMBER if a == "p1_dab168_kl1" else (A_C.get(a) or "#9AA3AD") for a in ALL_ARMS]
    ax.bar(range(len(ALL_ARMS)), [rel[a] for a in ALL_ARMS], color=cols)
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
    save(fig, "training_hours_all_arms", cite=True)

    # ── frontier with the ablations drawn as counterfactuals ─────────────
    fig, ax = fig_ax(88, 66)
    for m, (run, pol, fit, nm) in table1.MANIFEST.items():
        ax.plot(float(D[m][("knn-agreement", "patient_id")]),
                float(D[m][("cross-donor", "menstrual phase")]), "o", color=GREY_PT,
                ms=3.6, mec=SOFT, mew=.4)
        ax.annotate(nm, (float(D[m][("knn-agreement", "patient_id")]),
                         float(D[m][("cross-donor", "menstrual phase")])),
                    xytext=(3, -1), textcoords="offset points", fontsize=4.4, color=SOFT)
    for w in (1, 30):
        pts = [(float(D[k][("knn-agreement", "patient_id")]),
                float(D[k][("cross-donor", "menstrual phase")])) for k, _, ww in table1.P_SERIES if ww == w]
        pts.sort()
        ax.plot(*zip(*pts), color=KLC[w], lw=.9, marker="o", ms=3.6, mec="white", mew=.4,
                label=f"frontier arms, $w_{{kl}}$ {w}")
    bx, by = float(D["p1_dab168_kl1"][("knn-agreement", "patient_id")]), \
        float(D["p1_dab168_kl1"][("cross-donor", "menstrual phase")])
    for a in A_ARMS:
        x_, y_ = float(D[a][("knn-agreement", "patient_id")]), float(D[a][("cross-donor", "menstrual phase")])
        ax.annotate("", (x_, y_), (bx, by), arrowprops=dict(arrowstyle="-|>", color=A_C[a],
                                                             lw=.7, shrinkA=2, shrinkB=2))
        ax.plot(x_, y_, "D", color=A_C[a], ms=3.4, mec="white", mew=.4, label=ARM_LABEL[a])
    ax.set_xlabel("donor recovery (lower is better)")
    ax.set_ylabel("cross-donor cycle agreement")
    ax.legend(fontsize=4.6, loc="lower right")
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
    ax.legend(handles=handles, loc="center left", bbox_to_anchor=(1.0, .5), fontsize=4.8,
              handletextpad=.3, borderaxespad=0)
    save(fig, f"umap_{arm}_{colouring}", cite=cite)


def umaps(cite_only=False):
    cited = {("p1_dab168_kl1", "study"), ("a1_noecs", "study"), ("a1_nodns", "study"),
             ("a1_randgroups", "family"), ("a1_randgroups", "disease"),
             ("p1_dab168_kl1", "disease"), ("a1_nophase", "phase"), ("p1_dab168_kl1", "phase"),
             ("p1_dab7_kl1", "study"), ("p1_dab168_kl30", "study"), ("p1_dab336_kl1", "study"),
             ("p1_dab7_kl30", "study"), ("p1_dab336_kl30", "study")}
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

    # rejection rules, recomputed on the transferred cells
    rows = []
    for cut in (1.5, 2.0, 2.5, 3.0):
        rows.append([f"{cut:.1f}",
                     f"{(t.mean_distance[gran] > cut).mean() * 100:.1f}\\%",
                     f"{(t.mean_distance[li_imm] > cut).mean() * 100:.1f}\\%",
                     f"{(t.mean_distance[tr & ~li] > cut).mean() * 100:.1f}\\%"])
    tex("transfer_rejection", tabular("@{}rrrr@{}",
        ["distance cut", "granulosa rejected", r"\texttt{li\_2025} immune lost",
         "other transferred cells lost"], rows))
    # vote-based rule
    rows = []
    for cut in (1.0, 0.9, 0.8, 0.6):
        rows.append([f"$<$ {cut:.1f}",
                     f"{(t.vote_fraction[gran] < cut).mean() * 100:.1f}\\%",
                     f"{(t.vote_fraction[li_imm] < cut).mean() * 100:.1f}\\%",
                     f"{(t.vote_fraction[tr & ~li] < cut).mean() * 100:.1f}\\%"])
    tex("transfer_vote_rule", tabular("@{}rrrr@{}",
        ["vote fraction", "granulosa rejected", r"\texttt{li\_2025} immune lost",
         "other transferred cells lost"], rows))

    # neighbourhood statistics
    tt = t[tr]
    rows = [["cells labelled by transfer", intc(tr.sum())],
            ["median vote fraction", f"{tt.vote_fraction.median():.3f}"],
            ["vote unanimous across all 25 neighbours", f"{(tt.vote_fraction == 1).mean() * 100:.1f}\\%"],
            ["vote fraction below 0.6", f"{(tt.vote_fraction < .6).mean() * 100:.2f}\\%"],
            ["neighbourhoods drawing on more than one donor", f"{(tt.n_donors_in_neighbourhood > 1).mean() * 100:.1f}\\%"],
            ["neighbourhoods drawing on both annotated studies", f"{(tt.n_studies_in_neighbourhood > 1).mean() * 100:.1f}\\%"],
            ["mean distance to the 25th neighbour, granulosa", f"{t.mean_distance[gran].mean():.3f}"],
            [r"mean distance to the 25th neighbour, \texttt{li\_2025} immune", f"{t.mean_distance[li_imm].mean():.3f}"],
            ["mean distance to the 25th neighbour, all other transferred", f"{t.mean_distance[tr & ~li].mean():.3f}"]]
    tex("transfer_neighbourhood", tabular("@{}lr@{}", ["quantity", "value"], rows))

    # per-study transferred composition
    comp = (pd.crosstab(m.study[tr], t.cell_family_transferred[tr], normalize="index")
            .reindex(columns=FAMS))
    rows = []
    for s in comp.index:
        n = int(tr[m.study.values == s].sum())
        rows.append([f"\\texttt{{{esc(s)}}}", intc(n)] + [f"{comp.loc[s, f] * 100:.1f}" for f in FAMS])
    tex("transfer_composition", tabular("@{}lrrrrr@{}",
        ["study", "cells transferred"] + [f"{f} \\%" for f in FAMS], rows))

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
    save(fig, "transfer_vote_by_group", cite=True)

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
    save(fig, "transfer_composition_by_study", cite=True)

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
    for contrast, a, b, cols, tag in (
            ("control_vs_eutopic", "mean_control", "mean_eutopic", ["control", "eutopic"], "x8_composition"),
            ("eutopic_vs_ectopic", "mean_eutopic", "mean_ectopic", ["eutopic", "ectopic"], "x9_composition"),
            ("severity_low_vs_high", "mean_low", "mean_high", ["low severity", "high severity"], "x8_severity")):
        sub = c[c.contrast == contrast].set_index("family").loc[FAMS]
        rows = [[f, num(sub.loc[f, a], 3), num(sub.loc[f, b], 3), num(sub.loc[f, "F"], 3),
                 num(sub.loc[f, "p"], 4) if sub.loc[f, "p"] > 0 else "$<$ 0.0001"] for f in FAMS]
        tex(tag, tabular("@{}lrrrr@{}", ["family", f"mean share, {cols[0]}",
                                            f"mean share, {cols[1]}", "$F$", "$P$"], rows))
        print(f"       {tag}: {int(sub.n_donors.iloc[0])} donors")

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
    gs = pd.read_csv(CLAIMS / "x12_gene_shifts_orth.csv")
    gs = gs.rename(columns={gs.columns[0]: "gene"})
    gs["shift_towards_disease"] = -gs.shift_towards_control
    gs = gs.sort_values("shift_towards_disease", ascending=False).reset_index(drop=True)
    ext = pd.read_csv(CLAIMS / "replication_external.csv")
    hits = set(ext.loc[ext.end == "disease side", "genes"].iloc[0].split(";"))
    fold = {g_: float(ext.loc[ext.end == "disease side", f"fold_{g_}"].iloc[0]) for g_ in hits}
    novel = {"SIGLEC7", "ADAMDEC1", "ALPK2", "KCNH1"}     # Results names these four
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
    tex("x12_replication", tabular("@{}lrrrrl@{}",
        ["end of the ranking", "genes taken", "external list", "hits", "hypergeometric $P$", "genes"],
        [[r.end, str(int(r.n_top)), f"{int(r.external_n)} {r.external_list}", str(int(r.hits)),
          (lambda m_, e_: f"${m_}\\times10^{{{int(e_)}}}$")(*f"{r.p_hypergeometric:.2e}".split("e"))
          if r.hits else "1.0",
          esc(r.genes).replace(";", ", ") if isinstance(r.genes, str) else "--"]
         for _, r in ext.iterrows()]))

    fig, ax = fig_ax(120, 60)
    x = np.arange(len(gs)); yv = gs.shift_towards_disease.values
    ax.plot(x, yv, color=INK, lw=.8)
    ax.axhline(0, color=HAIR, lw=.5)
    for i, r in gs.head(15).iterrows():
        c = "#8C2D3F" if r.gene in hits else (AMBER if r.gene in novel else SOFT)
        ax.plot(i, r.shift_towards_disease, "o", color=c, ms=3.2, mec="white", mew=.3)
        ax.annotate(r.gene, (i, r.shift_towards_disease), xytext=(4 + (i % 3) * 22, 10 - (i % 5) * 7),
                    textcoords="offset points", fontsize=4.4, color=c,
                    arrowprops=dict(arrowstyle="-", color=HAIR, lw=.4))
    for i, r in gs.tail(15).iterrows():
        ax.plot(i, r.shift_towards_disease, "o", color=SOFT, ms=2.6, mec="white", mew=.3)
    ax.set_xlabel("genes ranked by decoder response to the immune disease direction (15,496)")
    ax.set_ylabel("shift towards disease")
    ax.legend(handles=[Line2D([], [], marker="o", lw=0, color="#8C2D3F", ms=3.2,
                              label="in the external up-regulated list (4 of top 15)"),
                       Line2D([], [], marker="o", lw=0, color=AMBER, ms=3.2,
                              label="no prior endometriosis report (4 of top 15)"),
                       Line2D([], [], marker="o", lw=0, color=SOFT, ms=2.6,
                              label="other top-15 and bottom-15 genes")], loc="upper right")
    save(fig, "x12_gene_ranking", cite=True)

    # per-family AUC figure, both label sources
    for src in ("annotated", "transferred"):
        d = pd.read_csv(CLAIMS / f"x12_by_family_{src}.csv")
        d["name"] = d.family.str.lower().replace({"all families": "all families, pooled"})
        d = d.sort_values("auc")
        fig, ax = fig_ax(88, 50)
        y = np.arange(len(d))
        ax.barh(y, d.auc - .5, left=.5, color=[FAM_C.get(f, "#9AA3AD") for f in d.name], height=.62)
        ax.errorbar(d.auc, y, xerr=[d.auc - d.auc_lo, d.auc_hi - d.auc], fmt="none",
                    ecolor=INK, elinewidth=.6, capsize=1.5)
        ax.plot(d.null, y, "|", color="#8C2D3F", ms=9, mew=1.2, label="shuffled-label AUC")
        for yi, (_, r) in zip(y, d.iterrows()):
            ax.text(.995, yi, f"P = {r.p:.3f}, {int(r.n_donors)} donors", va="center", ha="right",
                    fontsize=4.8, color=SOFT)
        ax.axvline(.5, color=INK, lw=.6)
        ax.set_yticks(y); ax.set_yticklabels(d.name)
        ax.set_xlim(.3, 1.0); ax.set_xlabel("held-out AUC, control against eutopic")
        ax.legend(loc="lower right", bbox_to_anchor=(1.0, -.02))
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

    def strips(df, groupcol, groups, cols, fname, note):
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
                          [Line2D([], [], color=INK, lw=1, label="median")], loc="upper right", fontsize=4.8)
        ax.text(.01, .98, note, transform=ax.transAxes, va="top", fontsize=4.8, color=SOFT)
        save(fig, fname, cite=True)

    strips(per, "disease_status", ["control", "eutopic"], ["#9a8f80", "#b4603e"],
           "composition_control_vs_eutopic", "endometrium; transferred and annotated labels")
    strips(perL, "disease_status", ["eutopic", "ectopic"], ["#b4603e", "#3f7fa6"],
           "composition_eutopic_vs_ectopic", "eutopic endometrium against lesion tissue")
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
        ax.text(.72, yi, f"P = {r.p:.3f}", va="center", fontsize=4.8, color=SOFT)
    ax.axvline(.5, color=INK, lw=.6); ax.set_yticks(y); ax.set_yticklabels(FAMS)
    ax.set_xlim(.4, .8); ax.set_xlabel("AUC, endometrium against lesion tissue, within one family")
    ax.legend(loc="lower right")
    save(fig, "x14_tissue_within_family", cite=True)


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
    for col, xl, fname in (("overlap_n", "genes shared between the two studies' top hundred", "x13_overlap_vs_null"),
                           ("spearman", "rank correlation over 13,034 jointly measured genes", "x13_spearman_vs_null")):
        fig, ax = fig_ax(88, 45)
        y = np.arange(4)
        rng = np.random.default_rng(2)
        for yi, f in zip(y, FAMS):
            n = nul[nul.family == f][col].values
            ax.plot(n, yi + rng.uniform(-.18, .18, len(n)), "o", ms=2.2, color=SOFT, alpha=.7, mec="none")
            ax.plot(obs.loc[f, col], yi, "o", ms=5, color=FAM_C[f], mec="white", mew=.5, zorder=3)
        ax.set_yticks(y); ax.set_yticklabels(FAMS)
        ax.set_xlabel(xl)
        ax.legend(handles=[Line2D([], [], marker="o", lw=0, ms=5, color=INK, label="observed"),
                           Line2D([], [], marker="o", lw=0, ms=2.2, color=SOFT,
                                  label="twenty within-study label shuffles")], loc="center right")
        save(fig, fname, cite=True)


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

    # coverage heatmap
    fig, ax = fig_ax(88, 52)
    M = cov[labs].values.astype(float) / cov.cells.values[:, None]
    ax.imshow(M, cmap="Blues", vmin=0, vmax=1, aspect="auto")
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            if M[i, j] > 0:
                ax.text(j, i, f"{M[i, j] * 100:.0f}%", ha="center", va="center", fontsize=4.4,
                        color="white" if M[i, j] > .6 else INK)
    ax.set_xticks(range(len(labs))); ax.set_xticklabels(labs, rotation=40, ha="right")
    ax.set_yticks(range(len(cov))); ax.set_yticklabels([STUDY_NAME[s] for s in cov.index])
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    save(fig, "label_coverage_heatmap", cite=True)

    fig, ax = fig_ax(88, 50)
    order = cov.index
    ax.barh(range(len(order)), cov.cells / 1e3, color=[STUDY_C[i] for i in range(len(order))], height=.7)
    for i, s in enumerate(order):
        ax.text(cov.cells[s] / 1e3 + 4, i, f"{int(cov.donors[s])} donor ids", va="center", fontsize=4.8, color=SOFT)
    ax.set_yticks(range(len(order))); ax.set_yticklabels([STUDY_NAME[s] for s in order])
    ax.invert_yaxis(); ax.set_xlabel("cells (thousands)"); ax.set_xlim(0, 560)
    save(fig, "corpus_cells_and_donors", cite=True)

    # cycle-day coverage, one cohort
    fig, ax = fig_ax(88, 40)
    cd = m.loc[m.CycleDay.notna(), ["CycleDay", "patient_id"]].drop_duplicates()
    counts = cd.groupby("CycleDay").patient_id.nunique().reindex(range(5, 31), fill_value=0)
    ax.bar(counts.index, counts.values, color=["#9AA3AD" if v else "#E45756" for v in counts.values])
    ax.set_xlabel("cycle day (duempelmann_2026, 60 donors, one day each)")
    ax.set_ylabel("donors"); ax.set_xticks(range(5, 31, 5))
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
    tex("null_widths", tabular("@{}llrrrr@{}",
        ["scope", "label", "donors", "null$_{95}$", "observed", "$P$"],
        [[r.scope, r.label, str(int(r.donors)), num(r.null95, 2), num(r.value), num(r.p, 3)]
         for _, r in nw.iterrows()]))
    fig, ax = fig_ax(88, 55)
    for sc, mk, c in (("held out", "o", INK), ("whole corpus", "s", AMBER),
                      ("whole corpus (validation)", "D", "#2F6690")):
        d = nw[nw.scope == sc]
        ax.plot(d.donors, d.null95, mk, color=c, ms=3.6, mec="white", mew=.4, label=sc)
        for _, r in d.iterrows():
            ax.annotate(r.label, (r.donors, r.null95), xytext=(3, 2), textcoords="offset points",
                        fontsize=4.2, color=SOFT)
    ax.set_xscale("log"); ax.set_xlabel("donors carrying the label (log)")
    ax.set_ylabel("permutation null, 95th percentile (excess scale)")
    ax.legend(loc="upper right")
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
    save(fig, "group_sizes", cite=True)

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
    save(fig, "study_purity_per_study", cite=True)


# ═════════════════════════════════════════════════════════════════════════
GROUPS = {"scib": scib, "field": field, "arms": arms, "transfer": transfer,
          "claims": claims, "x13": x13, "corpus": corpus, "umaps": umaps}


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
