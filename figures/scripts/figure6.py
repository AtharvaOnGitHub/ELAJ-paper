"""Figure 6 — what each component is load-bearing for.

    /Users/atharvawaghmare/miniconda3/envs/elaj/bin/python figures/scripts/figure6.py

Nature: 180 mm double column, 170 mm maximum depth. Drawn locally. Every
number read from a file at run time.

WHAT THIS FIGURE IS FOR, AND WHAT THAT FORBIDS. The question is what each
component carries, across five single-key changes and five axes. Prose cannot
hold a 5x5 comparison plus a training trajectory plus a distribution over 28
arms, so the figure holds them and the Results points here.

So: no callouts, no arrows, no annotation naming our own arm, no title that
states a result. Axes and legend define what is plotted. A reader reaches the
conclusion, or disagrees with it, from the data. An earlier draft had a bar
labelled "65.5%" and a panel titled "positive in 25 of 28 arms" -- that is
prose wearing a figure's clothes, and it tells a reader what to think.
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
MM = 1 / 25.4
INK, SOFT, GRID = "#1a1a1a", "#6b6b6b", "#dcdcdc"
ARM_C = {"BASE": "#2b4c7e", "−phase head": "#c25b56", "−ECS": "#e0a458",
         "−statistics": "#6a9b7d", "−sentinel": "#8d7fb5",
         "random groups": "#a8846f"}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7,
                     "axes.edgecolor": SOFT, "axes.labelcolor": INK,
                     "xtick.color": SOFT, "ytick.color": SOFT,
                     "axes.linewidth": .6, "xtick.major.width": .6,
                     "ytick.major.width": .6, "text.color": INK})

B = ROOT / "Outputs/Benchmarks"
ARMS = {"BASE": B / "p1_dab168_kl1", "−phase head": B / "a_series/a1_nophase",
        "−ECS": B / "a_series/a1_noecs", "−statistics": B / "a_series/a1_clsonly",
        "−sentinel": B / "a_series/a1_nodns",
        "random groups": B / "a_series/a1_randgroups"}
TESTS = {"cell\nfamily": ("cross-donor", "cell family"),
         "menstrual\nphase": ("cross-donor", "menstrual phase"),
         "disease": ("disease-xdonor", "all studies (pooled)"),
         "donor\nrecovery": ("knn-agreement", "patient_id"),
         "study\nmixing": ("study-mixing", "all studies")}

def val(d, test, label):
    b = pd.read_csv(d / "benchmark.csv")
    b["mm"] = b.method.astype(str).str.replace("__.*", "", regex=True)
    s = b[(b.mm == "elaj") & (b.test == test) & (b.label == label)]["value"]
    return float(s.iloc[0]) if len(s) else np.nan

A = pd.DataFrame({k: {ax: val(d, *TESTS[ax]) for ax in TESTS}
                  for k, d in ARMS.items()}).T
M = {k: pd.read_csv(ROOT / p) for k, p in
     (("BASE", "Outputs/p_series/p1_dab168_kl1/metrics.csv"),
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
CORR = np.array(CORR)

ABL = [a for a in A.index if a != "BASE"]

def spines(ax, keep=("left", "bottom")):
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(s in keep)

# a — change from BASE, five arms, five axes. Direction is the content.
def panel_a(ax):
    axes_n = list(TESTS); x = np.arange(len(axes_n)); w = .16
    for i, arm in enumerate(ABL):
        d = [A.loc[arm, a] - A.loc["BASE", a] for a in axes_n]
        ax.bar(x + (i - 2) * w, d, w, color=ARM_C[arm], edgecolor="white",
               linewidth=.4, label=arm, zorder=3)
    ax.axhline(0, color=ARM_C["BASE"], lw=1.0, zorder=4)
    ax.set_xticks(x); ax.set_xticklabels(axes_n, fontsize=6.2)
    ax.set_ylabel("change from the full model")
    ax.legend(ncol=5, fontsize=5.8, frameon=False, loc="lower left",
              bbox_to_anchor=(0, 1.01), columnspacing=1.0, handlelength=.9)
    ax.grid(axis="y", color=GRID, lw=.5, zorder=0); spines(ax)

# b — the training trajectory. Minima marked, defined in the legend.
def panel_b(ax):
    for arm in ("BASE", "−phase head"):
        m, c = M[arm], ARM_C[arm]
        ax.plot(m.epoch, m.train_nb, "--", color=c, lw=1.0, alpha=.6)
        ax.plot(m.epoch, m.val_nb, "-", color=c, lw=1.5)
        i = int(m.val_nb.idxmin())
        ax.scatter([m.epoch[i]], [m.val_nb[i]], s=20, zorder=4, color=c,
                   edgecolor="white", lw=.7)
    ax.set_xlabel("epoch"); ax.set_ylabel("negative binomial loss per cell")
    ax.legend(handles=[Line2D([], [], color=ARM_C["BASE"], lw=1.5, label="full model"),
                       Line2D([], [], color=ARM_C["−phase head"], lw=1.5, label="−phase head"),
                       Line2D([], [], color=SOFT, lw=1.0, ls="--", label="training split"),
                       Line2D([], [], color=SOFT, lw=1.5, label="held-out split"),
                       Line2D([], [], color=SOFT, lw=0, marker="o", ms=4,
                              label="selected checkpoint")],
              ncol=2, fontsize=5.6, frameon=False, loc="lower left",
              bbox_to_anchor=(0, 1.01), handlelength=1.4, columnspacing=1.0)
    ax.grid(color=GRID, lw=.5); spines(ax)

# c — the ablations placed in the frontier's own plane, two knob families.
def panel_c(ax):
    kl1 = sorted(v for k, v in FRONT.items() if k.endswith("kl1"))
    kl30 = sorted(v for k, v in FRONT.items() if k.endswith("kl30"))
    for pts, ls in ((kl1, "-"), (kl30, "--")):
        ax.plot([p[0] for p in pts], [p[1] for p in pts], ls, color=SOFT,
                lw=1.0, alpha=.55, zorder=1)
        ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=16,
                   facecolor="white", edgecolor=SOFT, lw=.8, zorder=3)
    ax.scatter([A.loc["BASE", "donor\nrecovery"]], [A.loc["BASE", "menstrual\nphase"]],
               s=34, color=ARM_C["BASE"], edgecolor="white", lw=.7, zorder=5)
    for arm in ABL:
        ax.scatter([A.loc[arm, "donor\nrecovery"]], [A.loc[arm, "menstrual\nphase"]],
                   s=26, marker="D", color=ARM_C[arm], edgecolor="white",
                   lw=.6, zorder=4)
    ax.set_xlabel("donor recovery"); ax.set_ylabel("cross-donor menstrual phase")
    ax.legend(handles=[Line2D([], [], color=SOFT, lw=1.0, label="lower information cost"),
                       Line2D([], [], color=SOFT, lw=1.0, ls="--", label="higher information cost"),
                       Line2D([], [], color=SOFT, lw=0, marker="o", ms=4,
                              markerfacecolor="white", label="trained arm"),
                       Line2D([], [], color=SOFT, lw=0, marker="D", ms=4,
                              label="single-key change")],
              ncol=2, fontsize=5.6, frameon=False, loc="lower left",
              bbox_to_anchor=(0, 1.01), handlelength=1.4, columnspacing=1.0)
    ax.grid(color=GRID, lw=.5); spines(ax)

# d — one correlation per trained arm. The spread is the content.
def panel_d(ax):
    ax.hist(CORR, bins=np.arange(-.6, 1.01, .1), color="#b9c6d4",
            edgecolor="white", lw=.5, zorder=3)
    ax.axvline(0, color=INK, lw=.9, zorder=4)
    ax.set_xlabel("correlation across epochs, adversarial loss\n"
                  "against donor recovery, one point per trained arm")
    ax.set_ylabel(f"arms (n = {len(CORR)})")
    ax.grid(axis="y", color=GRID, lw=.5, zorder=0); spines(ax)

def tag(ax, letter):
    ax.text(-.085, 1.26, letter, transform=ax.transAxes, fontsize=9,
            fontweight="bold", va="top", ha="right", clip_on=False)

fig = plt.figure(figsize=(180 * MM, 140 * MM))
gs = GridSpec(2, 2, figure=fig, hspace=1.0, wspace=.26,
              left=.085, right=.985, top=.88, bottom=.115)
for (r, c), fn, letter in (((0, 0), panel_a, "a"), ((0, 1), panel_b, "b"),
                           ((1, 0), panel_c, "c"), ((1, 1), panel_d, "d")):
    ax = fig.add_subplot(gs[r, c]); fn(ax); tag(ax, letter)
fig.savefig(OUT / "figure6.png", dpi=240)
plt.close(fig)
print("wrote figure6.png — 4 panels, no callouts, no result-stating titles")
