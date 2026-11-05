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
OUT = Path(__file__).resolve().parents[1] / "pinned"
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

# THE TWO REPORTED ARMS ARE NAMED. B is for biology: B_hi keeps more of the
# menstrual cycle and gives up a little study removal, B_lo gives up cycle
# signal and removes study substantially better. The other four arms are the
# factorial sweep and stay as coordinates.
ARM_NAME = {"p1_dab168_kl1": "ELAJ$_{B\\,hi}$",
            "p1_dab168_kl30": "ELAJ$_{B\\,lo}$"}

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


# Eight directions, tried in order of preference. Each is (dx, dy) in axes
# fractions, with the text alignment that keeps the label on the far side of
# the anchor from the point.
DIRS = [(1, 0, "left", "center"), (-1, 0, "right", "center"),
        (.75, .75, "left", "bottom"), (-.75, .75, "right", "bottom"),
        (.75, -.75, "left", "top"), (-.75, -.75, "right", "top"),
        (0, 1, "center", "bottom"), (0, -1, "center", "top")]

def declutter(ax, pts, colour, fontsize=4.6, pad=.030):
    """Place each label in the best free direction around its point.

    A purely vertical push stacks every label into one column, which is what
    collapsed panels c and d: on a saturated axis every point has nearly the
    same y, so every label wanted the same slot. So each label now tries
    right, left, the four diagonals, then up and down, and takes the first
    direction whose box overlaps nothing already placed, no data point, and
    no panel edge. If every direction collides it takes the least bad one and
    a hairline leader is drawn.

    Geometry is done in axes fractions, where a character is about 0.0062
    wide and a line about 0.030 tall at this font size, so the boxes do not
    distort with the panel's aspect or its data range.
    """
    inv = ax.transAxes.inverted()
    def to_ax(x, y):
        return inv.transform(ax.transData.transform((x, y)))
    CW, LH = 0.0062 * (fontsize / 4.6), 0.030 * (fontsize / 4.6)
    anchors = [to_ax(x, y) for x, y, _ in pts]
    placed, out = [], []
    order = sorted(range(len(pts)), key=lambda i: -anchors[i][1])
    for i in order:
        ax_, ay_ = anchors[i]
        nm = pts[i][2]
        w, h = len(nm) * CW, LH
        best, best_cost = None, np.inf
        for dx, dy, ha, va in DIRS:
            cx, cy = ax_ + dx * pad, ay_ + dy * pad
            x0 = cx if ha == "left" else cx - w if ha == "right" else cx - w / 2
            y0 = cy if va == "bottom" else cy - h if va == "top" else cy - h / 2
            box = (x0, y0, x0 + w, y0 + h)
            cost = 0.0
            if box[0] < 0 or box[2] > 1 or box[1] < 0 or box[3] > 1:
                cost += 10.0
            for b in placed:
                ox = max(0, min(box[2], b[2]) - max(box[0], b[0]))
                oy = max(0, min(box[3], b[3]) - max(box[1], b[1]))
                cost += (ox * oy) * 400
            for px, py in anchors:
                if box[0] - .004 < px < box[2] + .004 and box[1] - .004 < py < box[3] + .004:
                    cost += 2.0
            cost += DIRS.index((dx, dy, ha, va)) * 0.05     # prefer the earlier ones
            if cost < best_cost:
                best_cost, best = cost, (cx, cy, ha, va, box)
        cx, cy, ha, va, box = best
        placed.append(box)
        out.append((i, cx, cy, ha, va, best_cost))
    for i, cx, cy, ha, va, cost in out:
        x, y, nm = pts[i]
        ax.annotate(nm, xy=(x, y), xycoords="data", xytext=(cx, cy),
                    textcoords=ax.transAxes, fontsize=fontsize, color=colour,
                    ha=ha, va=va, zorder=8,
                    arrowprops=dict(arrowstyle="-", lw=.3, color=SOFT,
                                    shrinkA=.5, shrinkB=2.0))

# THE DISEASE ROW IS GONE, and the reason is a measurement we already made.
# Across the ten methods, a method's score on control-vs-eutopic correlates
# with its donor recovery at rho +0.721 (p 0.019) while menstrual phase does
# not (+0.176, p 0.63). A row whose dominant property is that it reads out
# donor memorisation is not a performance axis, and putting it beside phase
# and cell family implies it is one. The correlation itself stays as an
# observation about the metric; it just is not a column of the scoreboard.
ROWS = [("phase", "cross-donor menstrual phase"),
        ("family", "cross-donor cell family")]
COLS = [("donor", "donor recovery"), ("mixing", "study separation")]

fig, axes = plt.subplots(len(ROWS), len(COLS), figsize=(180 * MM, 135 * MM))
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
            labelled.append((v[xkey], v[ykey], ARM_NAME.get(k, k.replace("p1_", ""))))
        for m, v in F.items():
            if m == "elaj": continue
            if np.isnan(v[xkey]) or np.isnan(v[ykey]): continue
            ax.scatter([v[xkey]], [v[ykey]], s=20, color=FIELD_C,
                       edgecolor="white", lw=.5, zorder=5)
            labelled.append((v[xkey], v[ykey], m))
        fr = pareto([(x, y) for x, y, _ in labelled])
        ax.plot([p[0] for p in fr], [p[1] for p in fr], "-", color=SOFT,
                lw=1.0, alpha=.8, zorder=2)
        # INVERT FIRST. declutter freezes label positions in axes fractions,
        # so inverting afterwards flips the points out from under their own
        # labels and every leader line stretches across the panel.
        ax.margins(x=.22, y=.16)
        ax.invert_xaxis()                      # cost axes: better to the right
        declutter(ax, labelled, SOFT)
        if r == len(ROWS) - 1: ax.set_xlabel(xlab + "  (lower is better)")
        if c == 0: ax.set_ylabel(ylab)
        ax.grid(color=GRID, lw=.5, zorder=0)
        for s in ("top", "right"): ax.spines[s].set_visible(False)

for ax, letter in zip(axes.ravel(), "abcdef"):
    ax.text(-.10, 1.07, letter, transform=ax.transAxes, fontsize=9,
            fontweight="bold", va="top", ha="right", clip_on=False)

fig.legend(handles=[
    Line2D([], [], lw=0, marker="o", ms=6, color=ELAJ_C, label="ELAJ$_{B\\,hi}$, reported"),
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
