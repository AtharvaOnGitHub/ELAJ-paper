"""Figure 2's panels as functions, so the standalone drafts and the assembled
figure are drawn by the same code and cannot drift.

    a, b  the knobs' frontier, polished from old Figure 2's b and d
    c     I1   composition does not change with disease
    d     I2b  where the disease can be read, one plot (AW, 17 Nov)
    e     I4b  the disease end of the gene ranking
    f     I6   the external list on our ranking (pending AW's question)

THE FRONTIER PANELS (AW, 17 Nov: "These should be the new panels a and b.
They do need some polishing though. They look very 'we made it for internal
review and not publication'"). What changed from old figure2.py, and why:
  * Figure 1's conventions, not their own: Arial on scGPT's type scale,
    hairline spines, soft ticks, a light grid, ELAJ's two reported arms in
    Figure 1c's amber. The two figures sit next to each other in print.
  * The x axis is NOT reversed. Figure 1c puts lower cost on the left with
    the goal at upper left; reversing it here made the same reader learn two
    orientations on facing pages.
  * Knob coordinates like "336/30" are gone. Each line is labelled once at
    its end, each point carries only the value of the knob that varies
    along its line, and arrows say which way that knob is turned.
  * The cell-family row is dropped: the old figure's second row was the
    control, and Results quotes it in one sentence. Calibrated row limits
    existed only to compare the rows, so the phase axis now fits its data.
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figure1 import (FAMILY_C, INK, SOFT, HAIR, AMBER, AMBER_F,    # noqa: E402
                     FS_LETTER, FS_TITLE, FS_BODY)
from supp_figures import CLAIMS, ROOT                               # noqa: E402

FS_SMALL = 5.2
FAMS = ["stromal", "epithelial", "endothelial", "immune"]
FAM_C = dict(zip(FAMS, FAMILY_C))
WINE, VERM = "#8C2D3F", "#CC4E00"
NEUTRAL = "#9AA3AE"
CTL_C, CASE_C = "#5BA3A0", "#C2544E"


def clean(ax, keep_x=True, keep_y=True):
    for s, k in (("top", False), ("right", False), ("bottom", keep_x), ("left", keep_y)):
        ax.spines[s].set_visible(k)


def head(ax, letter, title=None, x=0.0, y=1.06):
    """Figure 1's heading: bold letter, title on the same line."""
    ax.text(x, y, letter, transform=ax.transAxes, fontsize=FS_LETTER,
            fontweight="bold", va="bottom", ha="left", color=INK)
    if title:
        ax.text(x + .055 * (1 if ax.get_position().width > .3 else 2.2), y + .006,
                title, transform=ax.transAxes, fontsize=FS_TITLE, va="bottom",
                ha="left", color=INK)


# ═════════════════════════════════════════════════════════════════════════
# a, b — the knobs
# ═════════════════════════════════════════════════════════════════════════
BENCH = ROOT / "Outputs/Benchmarks/full"
DABS, KLS = (7, 168, 336), (1, 30)
NAMED = {(168, 1): r"B$_{hi}$", (168, 30): r"B$_{lo}$"}
# AW, 17 Nov: "Colours need some work." One hue per knob, so a reader knows
# from colour alone which knob a line holds fixed: slate blue for the
# information cost, violet for the adversary, each light to dark with its
# value. Neither hue is a cell family's (Figure 2c/d sit beside these) and
# neither is ELAJ's amber, which stays on B_hi and B_lo as in Figure 1c.
KL_C = {1: "#22406E", 30: "#8EA6C9"}
DAB_C = {7: "#B49FDB", 168: "#7752C0", 336: "#3D2283"}


def _val(arm, test, label):
    for r in csv.DictReader(open(BENCH / f"full_{arm}/benchmark.csv")):
        if re.sub(r"__.*", "", r["method"]) == "elaj" and r["test"] == test and r["label"] == label:
            return float(r["value"])
    raise SystemExit(f"{arm}: no {test}/{label} row for elaj")


KNOB = {(d, k): (_val(f"p1_dab{d}_kl{k}", "study-mixing", "all studies"),
                 _val(f"p1_dab{d}_kl{k}", "cross-donor", "menstrual phase"))
        for d in DABS for k in KLS}


def _frontier_axes(ax):
    xs = [v[0] for v in KNOB.values()]; ys = [v[1] for v in KNOB.values()]
    ax.set_xlim(min(xs) - .035, max(xs) + .035)
    ax.set_ylim(min(ys) - .03, max(ys) + .03)
    ax.grid(True, lw=.35, color=HAIR, alpha=.6); ax.set_axisbelow(True)
    ax.xaxis.set_major_locator(plt.MultipleLocator(.05))
    ax.yaxis.set_major_locator(plt.MultipleLocator(.05))
    ax.tick_params(length=2, pad=2, labelsize=FS_BODY)
    ax.set_xlabel("study separation (lower is better)", fontsize=FS_BODY, labelpad=2)
    ax.set_ylabel("cross-donor menstrual phase", fontsize=FS_BODY, labelpad=2)
    clean(ax)


def _point(ax, key, colour):
    x, y = KNOB[key]
    if key in NAMED:
        ax.scatter(x, y, s=46, c=AMBER_F, edgecolors=AMBER, linewidths=1.1, zorder=5)
    else:
        ax.scatter(x, y, s=22, c="white", edgecolors=colour, linewidths=1.0, zorder=5)


def _arrow(ax, p, q, colour, lw):
    """A line from p to q with an arrowhead at its middle."""
    ax.plot([p[0], q[0]], [p[1], q[1]], color=colour, lw=lw, zorder=3,
            solid_capstyle="round")
    m = (.5 * (p[0] + q[0]), .5 * (p[1] + q[1]))
    d = (q[0] - p[0], q[1] - p[1])
    ax.annotate("", xy=(m[0] + .06 * d[0], m[1] + .06 * d[1]),
                xytext=(m[0] - .06 * d[0], m[1] - .06 * d[1]),
                arrowprops=dict(arrowstyle="-|>,head_length=.7,head_width=.35",
                                color=colour, lw=0, shrinkA=0, shrinkB=0,
                                mutation_scale=7), zorder=4)


def _name_points(ax):
    for key, nm in NAMED.items():
        x, y = KNOB[key]
        dy = 7 if key[1] == 1 else -7
        ax.annotate(nm, (x, y), xytext=(0, dy), textcoords="offset points",
                    ha="center", va="bottom" if dy > 0 else "top",
                    fontsize=FS_BODY, color=AMBER, fontweight="bold", zorder=6)


def _key(ax, text):
    """The varying knob and its values, bottom right (AW, 17 Nov). Same size
    and weight as every other label in the panel; only colour varies."""
    ax.text(.97, .04, text, transform=ax.transAxes, ha="right", va="bottom",
            fontsize=FS_BODY, color=SOFT)


def frontier_by_kl(ax):
    """a: the adversarial weight swept at each information cost."""
    _frontier_axes(ax)
    for k in KLS:
        pts = [KNOB[(d, k)] for d in DABS]
        for p, q in zip(pts, pts[1:]):
            _arrow(ax, p, q, KL_C[k], 1.3)
        for d in DABS:
            _point(ax, (d, k), KL_C[k])
    _name_points(ax)
    _key(ax, r"$\lambda$ 7  $\rightarrow$  $\lambda$ 168  $\rightarrow$  $\lambda$ 336")
    # each line named once, beside it, in its own colour
    bx, by = KNOB[(168, 1)]
    ax.annotate(r"$w_{kl}$ 1", (bx, by), xytext=(-9, 0), textcoords="offset points",
                ha="right", va="center", fontsize=FS_BODY, color=KL_C[1])
    (x1, y1), (x2, y2) = KNOB[(168, 30)], KNOB[(7, 30)]
    xm = x1 + .30 * (x2 - x1); ym = y1 + .30 * (y2 - y1)
    ax.annotate(r"$w_{kl}$ 30", (xm, ym), xytext=(-2, 6), textcoords="offset points",
                ha="right", va="bottom", fontsize=FS_BODY, color=KL_C[30])


def frontier_by_dab(ax):
    """b: the information cost raised at each adversarial weight."""
    _frontier_axes(ax)
    for d in DABS:
        _arrow(ax, KNOB[(d, 1)], KNOB[(d, 30)], DAB_C[d], 1.3)
        for k in KLS:
            _point(ax, (d, k), DAB_C[d])
    lab = {7: (5, -10, "left"), 168: (-8, 4, "right"), 336: (6, -8, "left")}
    for d, (dx, dy, ha) in lab.items():
        p, q = KNOB[(d, 1)], KNOB[(d, 30)]
        m = (.5 * (p[0] + q[0]), .5 * (p[1] + q[1]))
        ax.annotate(rf"$\lambda$ {d}", m, xytext=(dx, dy), textcoords="offset points",
                    ha=ha, va="center", fontsize=FS_BODY, color=DAB_C[d])
    _name_points(ax)
    _key(ax, r"$w_{kl}$ 1  $\rightarrow$  $w_{kl}$ 30")


# ═════════════════════════════════════════════════════════════════════════
# c — I1, composition
# ═════════════════════════════════════════════════════════════════════════
def _d3():
    d3 = pd.read_csv(ROOT / "Outputs/supplementary/data/D3_per_donor_cell_family_composition.csv",
                     low_memory=False)
    d3 = d3[(d3.tissue == "endometrium") & d3.disease_status.isin(["control", "eutopic"])]
    return d3.assign(frac=d3.n_cells / d3.groupby("patient_id").n_cells.transform("sum"))


def i1(axes):
    d3 = _d3()
    for ax, f in zip(axes, FAMS):
        s = d3[d3.cell_family == f]
        for j, (grp, c) in enumerate((("control", CTL_C), ("eutopic", CASE_C))):
            v = s[s.disease_status == grp].frac.to_numpy()
            jit = np.random.default_rng(j).uniform(-.22, .22, len(v))
            ax.scatter(j + jit, v, s=5, color=c, alpha=.55, lw=0, zorder=2)
            ax.plot([j - .3, j + .3], [np.median(v)] * 2, color=INK, lw=1.0, zorder=3)
        ax.set_xticks([0, 1]); ax.set_xticklabels(["control", "case"], fontsize=FS_SMALL)
        ax.set_xlim(-.6, 1.6); ax.set_ylim(0, 1)
        # NO y axis (AW, 17 Nov): the claim is that the two clouds sit at the
        # same height, which needs no scale to read
        ax.set_yticks([])
        ax.tick_params(length=2, pad=2, labelsize=FS_SMALL)
        ax.text(.5, 1.02, f, transform=ax.transAxes, fontsize=FS_BODY, color=FAM_C[f],
                va="bottom", ha="center")
        clean(ax, keep_y=False)


# ═════════════════════════════════════════════════════════════════════════
# d — I2b, one plot (AW: "It could just be one plot though instead of 4
# different y-axis lines")
# ═════════════════════════════════════════════════════════════════════════
def i2b(ax, xpos=None, labels=True):
    """Violins of the 400 held-out donor AUCs per family, one chance line.

    AW, 17 Nov: "Rethink this as one chance line against how much the 4 cell
    families explain disease status. Can we try violin plots here? If not,
    we need numbers in the figure." Both: the violins are the split
    distributions X12 now writes (x12_by_family_annotated_splits.csv, whose
    5th-95th percentiles ARE the table's interval), and each carries its
    mean AUC. The chance line is drawn at 0.5; the per-family permutation
    nulls sit at 0.48-0.50 and live in the table, not the figure.
    """
    t = pd.read_csv(CLAIMS / "x12_by_family_annotated.csv").set_index("family")
    sp = pd.read_csv(CLAIMS / "x12_by_family_annotated_splits.csv")
    sp = sp[sp.kind == "held-out"]
    xpos = list(xpos) if xpos is not None else [0, 1, 2, 3]
    wid = .62 * (xpos[1] - xpos[0])
    ax.axhline(.5, color=SOFT, lw=.7, ls=(0, (3, 2)), zorder=1)
    for x, f in zip(xpos, FAMS):
        v = sp.loc[sp.family == f, "auc"].to_numpy()
        vp = ax.violinplot([v], positions=[x], widths=wid, showextrema=False,
                           points=200, bw_method=.35)
        for b in vp["bodies"]:
            b.set_facecolor(FAM_C[f]); b.set_edgecolor("none"); b.set_alpha(.55)
        lo, hi = np.percentile(v, [5, 95])
        ax.plot([x, x], [lo, hi], color=INK, lw=.8, zorder=3)
        ax.scatter([x], [t.loc[f, "auc"]], s=14, color="white", ec=INK, lw=.8, zorder=4)
        ax.text(x, v.max() + .025, f"{t.loc[f, 'auc']:.2f}", fontsize=FS_BODY,
                color=INK, va="bottom", ha="center")
    ax.text(ax.get_xlim()[0] if xpos[0] > 0 else xpos[0] - .5 * wid, .505, "chance",
            fontsize=FS_BODY, color=SOFT, va="bottom", ha="left")
    ax.set_ylim(.2, 1.05)
    ax.set_yticks([.25, .5, .75, 1.0])
    ax.tick_params(length=2, pad=2, labelsize=FS_SMALL)
    if labels:
        ax.set_xticks(xpos); ax.set_xticklabels(FAMS, fontsize=FS_BODY)
        for tl, f in zip(ax.get_xticklabels(), FAMS):
            tl.set_color(FAM_C[f])
        ax.tick_params(axis="x", length=0)
    else:
        ax.set_xticks([])
    ax.set_ylabel("disease status from held-out\ndonors (AUC)", fontsize=FS_BODY, labelpad=2)
    clean(ax, keep_x=False)


# ═════════════════════════════════════════════════════════════════════════
# e — I4b, the disease end
# ═════════════════════════════════════════════════════════════════════════
def _ranking():
    gs = pd.read_csv(CLAIMS / "x12_gene_shifts_orth.csv")
    gs = gs.rename(columns={gs.columns[0]: "gene"})
    gs["disease"] = -gs.shift_towards_control
    return gs.sort_values("disease", ascending=False).reset_index(drop=True)


def i4b(fig, rect):
    """rect = (x0, y0, w, h) in figure fractions. Returns the list axes."""
    gs = _ranking()
    ext = pd.read_csv(CLAIMS / "replication_external.csv")
    hits = set(ext.loc[ext.end == "disease side", "genes"].iloc[0].split(";"))
    novel = {"SIGLEC7", "ADAMDEC1", "ALPK2", "KCNH1"}
    top = gs.head(15)
    x0, y0, w, h = rect
    lx = x0 + .30 * w; lw_ = .66 * w
    ax0 = fig.add_axes([lx, y0 + .90 * h, lw_, .03 * h])
    ax0.add_patch(plt.Rectangle((0, 0), 1, 1, fc="#E6E8EC", ec="none"))
    ax0.add_patch(plt.Rectangle((0, 0), .012, 1, fc=WINE, ec="none"))
    ax0.set_xlim(0, 1); ax0.set_ylim(0, 1); ax0.axis("off")
    ax0.text(0, 1.6, "every gene, ranked by shift towards disease", fontsize=FS_SMALL,
             color=SOFT, va="bottom", transform=ax0.transAxes)
    ax = fig.add_axes([lx, y0 + .20 * h, lw_, .66 * h])
    fig.add_artist(Line2D([lx, lx], [y0 + .90 * h, y0 + .86 * h], color=HAIR, lw=.5))
    fig.add_artist(Line2D([lx + lw_ * .012, lx + lw_], [y0 + .90 * h, y0 + .86 * h],
                          color=HAIR, lw=.5))
    def col(g):
        return WINE if g in hits else (VERM if g in novel else NEUTRAL)
    for i, r in top.iterrows():
        c = col(r.gene)
        ax.plot([0, r.disease], [i, i], color=c, lw=1.3, solid_capstyle="butt", zorder=2)
        ax.scatter([r.disease], [i], s=13, color=c, lw=0, zorder=3)
        ax.text(-.004, i, r.gene, ha="right", va="center", fontsize=FS_BODY,
                color=INK if c != NEUTRAL else SOFT,
                fontweight="bold" if c != NEUTRAL else "normal")
    ax.set_ylim(len(top) - .4, -.6); ax.set_xlim(0, top.disease.max() * 1.05)
    ax.set_xticks([]); ax.set_yticks([]); clean(ax, keep_x=False, keep_y=False)
    ax.axvline(0, color=HAIR, lw=.6)
    lg = fig.add_axes([x0, y0, w, .16 * h]); lg.axis("off")
    for j, (c, t) in enumerate(((WINE, "reported up in an external cohort"),
                                (VERM, "no prior endometriosis report"),
                                (NEUTRAL, "linked to endometriosis before"))):
        yy = .85 - j * .33
        lg.scatter([.06], [yy], s=12, color=c, lw=0, clip_on=False)
        lg.text(.11, yy, t, fontsize=FS_SMALL, color=SOFT, va="center")
    lg.set_xlim(0, 1); lg.set_ylim(0, 1)
    return ax0


# ═════════════════════════════════════════════════════════════════════════
# f — I6, pending
# ═════════════════════════════════════════════════════════════════════════
def i6(fig, rect):
    gs = _ranking(); n = len(gs)
    txt = re.sub(r"\s+", " ", (ROOT.parent / "Atharva Papers" / "Validation" / "PMC5449958.txt").read_text())
    up = {g for g, d, _ in re.findall(
        r"\b([A-Z0-9orf.-]{2,15})\b ENSG\d+ (Upregulated|Downregulated) ([\d.]+)", txt)
        if d == "Upregulated"}
    rank = pd.Series(np.arange(1, n + 1), index=gs.gene)
    ru = rank.reindex(sorted(up)).dropna().astype(int).sort_values()
    x0, y0, w, h = rect
    a1 = fig.add_axes([x0, y0 + .74 * h, w, .14 * h])
    a2 = fig.add_axes([x0, y0, w, .70 * h], sharex=a1)
    a1.vlines(ru.values, 0, 1, color=WINE, lw=.6, alpha=.9)
    a1.set_ylim(0, 1); a1.set_yticks([]); clean(a1, keep_x=False, keep_y=False)
    a1.tick_params(labelbottom=False, bottom=False)
    xs = np.concatenate([[0], ru.values, [n]])
    ys = np.concatenate([[0], np.arange(1, len(ru) + 1), [len(ru)]]) / len(ru)
    a2.step(xs, ys, where="post", color=WINE, lw=1.2, zorder=3)
    a2.plot([0, n], [0, 1], color=HAIR, lw=.8, ls="--", zorder=2)
    a2.set_xlim(0, n); a2.set_ylim(0, 1.02)
    a2.set_yticks([0, .5, 1]); a2.set_yticklabels(["0", "half", "all"], fontsize=FS_SMALL)
    a2.set_xticks([1, n]); a2.set_xticklabels(["most towards disease", "most towards control"],
                                              fontsize=FS_SMALL)
    a2.get_xticklabels()[0].set_ha("left"); a2.get_xticklabels()[1].set_ha("right")
    a2.tick_params(length=2, pad=2)
    a2.set_ylabel("share of their\nlist reached", fontsize=FS_BODY, labelpad=2)
    a2.text(n * .58, .36, "if their list were spread evenly", fontsize=FS_SMALL,
            color=SOFT, rotation=12)
    clean(a2)
    return a1, a2
