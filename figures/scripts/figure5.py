"""Figure 5 — what each component is load-bearing for.

    /Users/atharvawaghmare/miniconda3/envs/elaj/bin/python figures/scripts/figure5.py

THE QUESTION: remove one piece of the model at a time, and what breaks?
Five single-key changes against the full model, each scored on the same five
axes as the full model. 25 numbers before anything else, which is why this is
a figure and not a paragraph.

a, b   the 25 changes, SPLIT BY DIRECTION. Three axes where higher is better
       and two where lower is, on separate panels, because one y-axis for
       both means a negative bar changes meaning between groups.
c      the training trajectory. Without the phase head the held-out split is
       paid for the training split from the first epoch.
d      the five changes placed in Figure 2a's plane, so a reader sees which
       travel the frontier and which leave it.
e      one adversarial-loss correlation per trained arm, 28 arms, drawn as 28
       marks rather than as a histogram of mostly empty bins.
"""
from __future__ import annotations
import glob
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D
from scipy.stats import pearsonr

ROOT = Path("/Users/atharvawaghmare/Endo research/ELAJ")
OUT = Path(__file__).resolve().parents[1] / "draft"
B = ROOT / "Outputs/Benchmarks"
MM = 1 / 25.4
INK, SOFT, GRID = "#1a1a1a", "#6b6b6b", "#e2e2e2"
C = {"full model": "#2b4c7e", "−phase head": "#c25b56", "−ECS": "#e0a458",
     "−statistics": "#6a9b7d", "−sentinel": "#8d7fb5", "random groups": "#a8846f"}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7,
                     "axes.edgecolor": SOFT, "axes.labelcolor": INK,
                     "xtick.color": SOFT, "ytick.color": SOFT,
                     "axes.linewidth": .6, "xtick.major.width": .6,
                     "ytick.major.width": .6, "text.color": INK})

ARMS = {"full model": B / "p1_dab168_kl1", "−phase head": B / "a_series/a1_nophase",
        "−ECS": B / "a_series/a1_noecs", "−statistics": B / "a_series/a1_clsonly",
        "−sentinel": B / "a_series/a1_nodns",
        "random groups": B / "a_series/a1_randgroups"}
UP = {"cell\nfamily": ("cross-donor", "cell family"),
      "menstrual\nphase": ("cross-donor", "menstrual phase"),
      "disease": ("disease-xdonor", "all studies (pooled)")}
DOWN = {"donor\nrecovery": ("knn-agreement", "patient_id"),
        "study\nseparation": ("study-mixing", "all studies")}

def val(d, t, l):
    b = pd.read_csv(d / "benchmark.csv")
    b["mm"] = b.method.astype(str).str.replace("__.*", "", regex=True)
    s = b[(b.mm == "elaj") & (b.test == t) & (b.label == l)]["value"]
    return float(s.iloc[0]) if len(s) else np.nan

A = pd.DataFrame({k: {ax: val(d, *(UP | DOWN)[ax]) for ax in (UP | DOWN)}
                  for k, d in ARMS.items()}).T
ABL = [a for a in A.index if a != "full model"]
M = {k: pd.read_csv(ROOT / p) for k, p in
     (("full model", "Outputs/p_series/p1_dab168_kl1/metrics.csv"),
      ("−phase head", "Outputs/a_series/a1_nophase/metrics.csv"))}
FRONT = {}
for f in sorted(glob.glob(str(B / "p1_dab*/benchmark.csv"))):
    d = Path(f).parent
    if d.name.endswith("_train"): continue
    FRONT[d.name] = (val(d, "knn-agreement", "patient_id"),
                     val(d, "cross-donor", "menstrual phase"))
CORR = []
for f in sorted(glob.glob(str(ROOT / "Outputs/*_series/*/metrics.csv"))):
    m = pd.read_csv(f)
    if "val_dab" not in m or "val_patient_knn" not in m: continue
    d = m[["val_dab", "val_patient_knn"]].dropna()
    if len(d) >= 5: CORR.append(pearsonr(d.val_dab, d.val_patient_knn)[0])
CORR = np.array(sorted(CORR))

def spines(ax):
    for s in ("top", "right"): ax.spines[s].set_visible(False)

def deltas(ax, axes_n, note):
    x = np.arange(len(axes_n)); w = .16
    for i, arm in enumerate(ABL):
        ax.bar(x + (i - 2) * w, [A.loc[arm, a] - A.loc["full model", a] for a in axes_n],
               w, color=C[arm], edgecolor="white", lw=.4, label=arm, zorder=3)
    ax.axhline(0, color=C["full model"], lw=1.0, zorder=4)
    ax.set_xticks(x); ax.set_xticklabels(axes_n, fontsize=6.2)
    ax.set_ylabel(note, fontsize=6.4)
    ax.grid(axis="y", color=GRID, lw=.5, zorder=0); spines(ax)

fig = plt.figure(figsize=(180 * MM, 165 * MM))
gs = GridSpec(3, 2, figure=fig, height_ratios=[1, 1, .78], hspace=.95,
              wspace=.26, left=.10, right=.985, top=.855, bottom=.085)

axa = fig.add_subplot(gs[0, 0])
deltas(axa, list(UP), "change from the full model\n(higher is better)")
axb = fig.add_subplot(gs[0, 1])
deltas(axb, list(DOWN), "change from the full model\n(lower is better)")

axc = fig.add_subplot(gs[1, 0])
for arm in ("full model", "−phase head"):
    m = M[arm]
    axc.plot(m.epoch, m.train_nb, "--", color=C[arm], lw=1.0, alpha=.6)
    axc.plot(m.epoch, m.val_nb, "-", color=C[arm], lw=1.5)
    i = int(m.val_nb.idxmin())
    axc.scatter([m.epoch[i]], [m.val_nb[i]], s=20, zorder=4, color=C[arm],
                edgecolor="white", lw=.7)
axc.set_xlabel("epoch"); axc.set_ylabel("negative binomial loss per cell")
axc.legend(handles=[Line2D([], [], color=SOFT, lw=1.0, ls="--", label="training split"),
                    Line2D([], [], color=SOFT, lw=1.5, label="held-out split"),
                    Line2D([], [], color=SOFT, lw=0, marker="o", ms=4,
                           label="selected checkpoint")],
           ncol=3, fontsize=5.8, frameon=False, loc="lower left",
           bbox_to_anchor=(0, 1.0), handlelength=1.4, columnspacing=1.0)
axc.grid(color=GRID, lw=.5); spines(axc)

axd = fig.add_subplot(gs[1, 1])
for suf, ls in (("kl1", "-"), ("kl30", "--")):
    p = sorted(v for k, v in FRONT.items() if k.endswith(suf))
    axd.plot([q[0] for q in p], [q[1] for q in p], ls, color=SOFT, lw=1.0,
             alpha=.6, zorder=1)
    axd.scatter([q[0] for q in p], [q[1] for q in p], s=14, facecolor="white",
                edgecolor=SOFT, lw=.8, zorder=3)
axd.scatter([A.loc["full model", "donor\nrecovery"]],
            [A.loc["full model", "menstrual\nphase"]], s=44,
            color=C["full model"], edgecolor="white", lw=.8, zorder=6)
for arm in ABL:
    axd.scatter([A.loc[arm, "donor\nrecovery"]], [A.loc[arm, "menstrual\nphase"]],
                s=30, marker="D", color=C[arm], edgecolor="white", lw=.6, zorder=5)
axd.invert_xaxis()
axd.set_xlabel("donor recovery  (lower is better)")
axd.set_ylabel("cross-donor menstrual phase")
axd.grid(color=GRID, lw=.5); spines(axd)

axe = fig.add_subplot(gs[2, :])
y = np.zeros_like(CORR)
axe.axvline(0, color=INK, lw=.9, zorder=2)
axe.scatter(CORR, y + np.linspace(-.28, .28, len(CORR)), s=22,
            color="#9aa7b4", edgecolor="white", lw=.5, zorder=3)
axe.set_yticks([]); axe.set_ylim(-.65, .65)
axe.set_xlabel("correlation across epochs between adversarial loss and donor "
               "recovery,\none mark per trained arm")
axe.grid(axis="x", color=GRID, lw=.5, zorder=0)
for s in ("top", "right", "left"): axe.spines[s].set_visible(False)

fig.legend(handles=[Line2D([], [], lw=0, marker="s", ms=6, color=C[a], label=a)
                    for a in A.index],
           ncol=6, fontsize=6.2, frameon=False, loc="upper left",
           bbox_to_anchor=(.095, .975), columnspacing=1.3, handlelength=1.0)
for ax, letter in ((axa, "a"), (axb, "b"), (axc, "c"), (axd, "d"), (axe, "e")):
    ax.text(-.085, 1.16, letter, transform=ax.transAxes, fontsize=9,
            fontweight="bold", va="top", ha="right", clip_on=False)
fig.savefig(OUT / "figure5.png", dpi=240)
print(f"wrote figure5.png — 5 panels, {len(ABL)} changes, {len(CORR)} arms")
