"""Figure 2 — the ELAJ frontier.

    /Users/atharvawaghmare/miniconda3/envs/elaj/bin/python figures/scripts/figure2.py

A grid of scatters. Every column shares an x-axis (a cost: something a good
model should fail at), every row shares a y-axis (a biology axis). Both cost
axes are REVERSED, so in every panel better is up and to the right and the
reader never has to re-learn the orientation.

Ten methods as points. The six ELAJ arms as a curve, because the two knobs
sweep a frontier and the field does not: that contrast is the figure.

Pareto front drawn per panel over the ten methods. No callouts, no arrows,
no annotation naming our own arm. The legend identifies; the data argues.
"""
from __future__ import annotations
import glob
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

ROOT = Path("/Users/atharvawaghmare/Endo research/ELAJ")
OUT = Path(__file__).resolve().parents[1] / "draft"
B = ROOT / "Outputs/Benchmarks"
MM = 1 / 25.4
INK, SOFT, GRID = "#1a1a1a", "#6b6b6b", "#e2e2e2"
ELAJ_C, FIELD_C, ARM_C = "#2b4c7e", "#9aa7b4", "#5c7fa8"

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7,
                     "axes.edgecolor": SOFT, "axes.labelcolor": INK,
                     "xtick.color": SOFT, "ytick.color": SOFT,
                     "axes.linewidth": .6, "xtick.major.width": .6,
                     "ytick.major.width": .6, "text.color": INK})

MANIFEST = {"pca": ("fm_scgpt", "all30962", "train"),
            "scvi": ("fm_scgpt", "all30962", "train"),
            "scanvi": ("fm_scgpt", "all30962", "train"),
            "scgpt": ("fm_scgpt", "native", "pretrained"),
            "geneformer": ("fm_baseline+Geneformer", "native", "pretrained"),
            "scfoundation": ("fm_scfoundation", "native", "pretrained"),
            "scimilarity": ("fm_scimilarity", "native", "pretrained"),
            "harmony": ("wide_transductive", "all30962", ""),
            "scanorama": ("wide_transductive", "all30962", "")}
AX = {"phase": ("cross-donor", "menstrual phase"),
      "family": ("cross-donor", "cell family"),
      "disease": ("disease-xdonor", "all studies (pooled)"),
      "donor": ("knn-agreement", "patient_id"),
      "mixing": ("study-mixing", "all studies")}

def grab(path, method, policy, fit):
    b = pd.read_csv(path)
    b["mm"] = b.method.astype(str).str.replace("__.*", "", regex=True)
    e = b[(b.mm == method)
          & (b.gene_policy.fillna("").astype(str) == policy)
          & (b.fit_on.fillna("").astype(str) == fit)]
    out = {}
    for k, (t, l) in AX.items():
        s = e[(e.test == t) & (e.label == l)]["value"]
        out[k] = float(s.iloc[0]) if len(s) else np.nan
    w = e["width"].dropna()
    out["width"] = int(w.max()) if len(w) else None
    return out

F = {"elaj": grab(B / "p1_dab168_kl1/benchmark.csv", "elaj", "native", "train")}
for m, (run, pol, fit) in MANIFEST.items():
    F[m] = grab(B / run / "benchmark.csv", m, pol, fit)

ARMS = {}
for f in sorted(glob.glob(str(B / "p1_dab*/benchmark.csv"))):
    d = Path(f).parent
    if d.name.endswith("_train"): continue
    ARMS[d.name] = grab(f, "elaj", "native", "train")

def pareto(pts):
    """Non-dominated under maximise-y, minimise-x, returned left to right.

    ONE FRONT OVER EVERYTHING. An earlier version drew the front over the ten
    methods only, with our own arms as a separate curve, which decides in
    advance who is allowed to be on it. Every point competes: whatever lies
    on the front, lies on it.
    """
    s = sorted(pts, key=lambda p: (p[0], -p[1]))
    front, best = [], -np.inf
    for x, y in s:
        if y > best:
            front.append((x, y)); best = y
    return front


def declutter(ax, pts, colour, fontsize=4.6):
    """Label every point, pushed apart vertically, leader line where moved.

    The vertical-declutter from figure1.py: sort by y, enforce a minimum
    separation in data units, and draw a hairline back to the point when a
    label had to move.
    """
    lo, hi = ax.get_ylim()
    minsep = (hi - lo) * 0.052
    # Make room BEFORE placing, so a stack of labels cannot climb out of the
    # panel and land on the one above it.
    need = lo + minsep * (len(pts) + 1)
    if need > hi:
        hi = need
        ax.set_ylim(lo, hi)
        minsep = (hi - lo) * 0.052
    last = lo - minsep
    for x, y, nm in sorted(pts, key=lambda t: t[1]):
        yy = min(max(y, last + minsep), hi - minsep * .5); last = yy
        ax.annotate(nm, (x, y), xytext=(x, yy), textcoords="data",
                    fontsize=fontsize, color=colour, va="center", ha="left",
                    zorder=8,
                    arrowprops=dict(arrowstyle="-", lw=.3, color=SOFT,
                                    shrinkA=.5, shrinkB=1.5)
                    if abs(yy - y) > 1e-9 else None)

ROWS = [("phase", "cross-donor menstrual phase"),
        ("family", "cross-donor cell family"),
        ("disease", "control vs eutopic endometrium")]
COLS = [("donor", "donor recovery"), ("mixing", "study separation")]

fig, axes = plt.subplots(len(ROWS), len(COLS), figsize=(180 * MM, 200 * MM))
plt.subplots_adjust(left=.095, right=.985, top=.845, bottom=.075,
                    hspace=.30, wspace=.20)

for r, (ykey, ylab) in enumerate(ROWS):
    for c, (xkey, xlab) in enumerate(COLS):
        ax = axes[r, c]
        # EVERY point: the six p-series arms and the nine other methods.
        labelled = []
        for k, v in ARMS.items():
            if np.isnan(v[xkey]) or np.isnan(v[ykey]): continue
            rep = k == "p1_dab168_kl1"
            ax.scatter([v[xkey]], [v[ykey]], s=44 if rep else 16,
                       color=ELAJ_C if rep else "white",
                       edgecolor="white" if rep else ARM_C,
                       lw=.8, zorder=6 if rep else 4)
            labelled.append((v[xkey], v[ykey],
                             "ELAJ" if rep else k.replace("p1_", "")))
        for m, v in F.items():
            if m == "elaj": continue
            if np.isnan(v[xkey]) or np.isnan(v[ykey]): continue
            ax.scatter([v[xkey]], [v[ykey]], s=20, color=FIELD_C,
                       edgecolor="white", lw=.5, zorder=5)
            labelled.append((v[xkey], v[ykey], m))
        fr = pareto([(x, y) for x, y, _ in labelled])
        ax.plot([p[0] for p in fr], [p[1] for p in fr], "-", color=SOFT,
                lw=1.0, alpha=.8, zorder=2)
        ax.margins(x=.30, y=.12)
        declutter(ax, labelled, SOFT)
        ax.invert_xaxis()                      # cost axes: better to the right
        if r == len(ROWS) - 1: ax.set_xlabel(xlab + "  (lower is better)")
        if c == 0: ax.set_ylabel(ylab)
        ax.grid(color=GRID, lw=.5, zorder=0)
        for s in ("top", "right"): ax.spines[s].set_visible(False)

for ax, letter in zip(axes.ravel(), "abcdef"):
    ax.text(-.10, 1.07, letter, transform=ax.transAxes, fontsize=9,
            fontweight="bold", va="top", ha="right", clip_on=False)

fig.legend(handles=[
    Line2D([], [], lw=0, marker="o", ms=6, color=ELAJ_C, label="ELAJ, reported arm"),
    Line2D([], [], lw=0, marker="o", ms=4.5, color=FIELD_C, label="other methods (9)"),
    Line2D([], [], lw=0, marker="o", ms=4.5, markerfacecolor="white",
           markeredgecolor=ARM_C, color="none", label="other ELAJ arms (5)"),
    Line2D([], [], color=SOFT, lw=1.0, label="Pareto front over every point")],
    ncol=4, fontsize=6.2, frameon=False, loc="upper left",
    bbox_to_anchor=(.085, .975), columnspacing=1.6, handlelength=1.6)
fig.savefig(OUT / "figure2.png", dpi=240)
plt.close(fig)
print(f"wrote figure2.png — {len(ROWS)}x{len(COLS)} scatters, "
      f"{len(F)} methods, {len(ARMS)} ELAJ arms")
