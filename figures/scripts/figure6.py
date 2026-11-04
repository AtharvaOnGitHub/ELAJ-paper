"""Figure 6 — what the latent needs. Drafts, for AW to choose a layout.

    /Users/atharvawaghmare/miniconda3/envs/elaj/bin/python figures/scripts/figure6.py

Nature: 180 mm double column, 170 mm maximum depth. Drawn locally, never on
HPC walltime. Every number read from a file at run time; nothing typed in.
"""
from __future__ import annotations
import glob
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.stats import pearsonr, wilcoxon

ROOT = Path("/Users/atharvawaghmare/Endo research/ELAJ")
OUT = Path(__file__).resolve().parents[1] / "draft"
MM = 1 / 25.4
INK, SOFT, GRID = "#1a1a1a", "#6b6b6b", "#dcdcdc"
BASE_C, ABL_C, HI = "#2b4c7e", "#9fb3c8", "#c25b56"
# One hue per ablation, because five bars in one colour make the legend
# decorative. BASE stays dark and apart: it is the thing being changed from.
ARM_C = {"BASE": "#2b4c7e", "\u2212phase head": "#c25b56",
         "\u2212ECS": "#e0a458", "\u2212statistics": "#6a9b7d",
         "\u2212sentinel": "#8d7fb5", "random groups": "#a8846f"}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7,
                     "axes.edgecolor": SOFT, "axes.labelcolor": INK,
                     "xtick.color": SOFT, "ytick.color": SOFT,
                     "axes.linewidth": 0.6, "xtick.major.width": 0.6,
                     "ytick.major.width": 0.6, "text.color": INK})

# ── data ──────────────────────────────────────────────────────────────────
B = ROOT / "Outputs/Benchmarks"
ARMS = {"BASE": B / "p1_dab168_kl1", "−phase head": B / "a_series/a1_nophase",
        "−ECS": B / "a_series/a1_noecs", "−statistics": B / "a_series/a1_clsonly",
        "−sentinel": B / "a_series/a1_nodns",
        "random groups": B / "a_series/a1_randgroups"}
TESTS = {"cell family": ("cross-donor", "cell family", True),
         "menstrual phase": ("cross-donor", "menstrual phase", True),
         "disease": ("disease-xdonor", "all studies (pooled)", True),
         "donor recovery": ("knn-agreement", "patient_id", False),
         "study mixing": ("study-mixing", "all studies", False)}

def val(d: Path, test: str, label: str) -> float:
    b = pd.read_csv(d / "benchmark.csv")
    b["mm"] = b.method.astype(str).str.replace("__.*", "", regex=True)
    s = b[(b.mm == "elaj") & (b.test == test) & (b.label == label)]["value"]
    return float(s.iloc[0]) if len(s) else np.nan

A = pd.DataFrame({k: {ax: val(d, *TESTS[ax][:2]) for ax in TESTS}
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
    if len(d) < 5: continue
    CORR.append(pearsonr(d.val_dab, d.val_patient_knn)[0])
CORR = np.array(CORR)

# ── panels ────────────────────────────────────────────────────────────────
def panel_a(ax):
    axes_n = list(TESTS)
    x = np.arange(len(axes_n)); w = 0.14
    for i, arm in enumerate(A.index):
        vals = [A.loc[arm, a] for a in axes_n]
        ax.bar(x + (i - 2.5) * w, vals, w, color=ARM_C[arm],
               edgecolor="white", linewidth=0.4, label=arm, zorder=3)
    ax.set_xticks(x)
    ax.set_xticklabels([a + ("\n(lower better)" if not TESTS[a][2] else "")
                        for a in axes_n], fontsize=6.2)
    ax.set_ylim(0, 1.05); ax.set_ylabel("cross-donor agreement")
    ax.legend(ncol=3, fontsize=5.8, frameon=False, loc="lower left",
              bbox_to_anchor=(0, 1.0), columnspacing=1.1, handlelength=1.0)
    ax.grid(axis="y", color=GRID, lw=0.5, zorder=0)
    for s in ("top", "right"): ax.spines[s].set_visible(False)

def panel_b(ax):
    base, nohead = A.loc["BASE", "menstrual phase"], A.loc["−phase head", "menstrual phase"]
    kept = nohead / base
    ax.barh([0], [kept * 100], color=BASE_C, height=.5, zorder=3,
            label="architecture")
    ax.barh([0], [(1 - kept) * 100], left=[kept * 100], color=HI, height=.5,
            zorder=3, label="phase head")
    ax.text(kept * 50, 0, f"{kept*100:.1f}%", ha="center", va="center",
            color="white", fontsize=7.5, fontweight="bold")
    ax.text(kept * 100 + (1 - kept) * 50, 0, f"{(1-kept)*100:.1f}%",
            ha="center", va="center", color="white", fontsize=7.5,
            fontweight="bold")
    ax.set_yticks([]); ax.set_xlim(0, 100)
    ax.set_xlabel("share of cross-donor phase agreement")
    ax.set_title(f"{base:.4f} with the head, {nohead:.4f} without",
                 fontsize=6.4, color=SOFT, pad=3)
    ax.legend(fontsize=5.8, frameon=False, ncol=2, loc="lower center",
              bbox_to_anchor=(.5, -1.15), handlelength=1.0)
    for s in ("top", "right", "left"): ax.spines[s].set_visible(False)

def panel_c(ax):
    for arm in ("BASE", "\u2212phase head"):
        m, c = M[arm], ARM_C[arm]
        ax.plot(m.epoch, m.train_nb, "--", color=c, lw=1.0, alpha=.55,
                label=f"{arm}, train")
        ax.plot(m.epoch, m.val_nb, "-", color=c, lw=1.5,
                label=f"{arm}, held out")
        i = int(m.val_nb.idxmin())
        ax.scatter([m.epoch[i]], [m.val_nb[i]], s=18, zorder=4, color=c,
                   edgecolor="white", linewidth=.7)
        ax.annotate(f"best, epoch {int(m.epoch[i])}", (m.epoch[i], m.val_nb[i]),
                    textcoords="offset points", xytext=(4, -9), fontsize=5.6,
                    color=c)
    ax.set_xlabel("epoch"); ax.set_ylabel("NB loss per cell  (lower better)")
    ax.legend(fontsize=5.4, frameon=False, ncol=2, loc="lower left",
              bbox_to_anchor=(0, 1.0), handlelength=1.4, columnspacing=1.0)
    ax.grid(color=GRID, lw=.5)
    for s in ("top", "right"): ax.spines[s].set_visible(False)

def panel_d(ax):
    pts = sorted(FRONT.values())
    ax.plot([p[0] for p in pts], [p[1] for p in pts], "-", color=GRID, lw=1.4,
            zorder=1)
    for name, (dn, ph) in FRONT.items():
        hl = name == "p1_dab168_kl1"
        ax.scatter([dn], [ph], s=30 if hl else 18, zorder=3,
                   color=BASE_C if hl else ABL_C, edgecolor="white", lw=.6)
    ax.scatter([A.loc["−ECS", "donor recovery"]], [A.loc["−ECS", "menstrual phase"]],
               s=34, marker="D", color=HI, zorder=4, edgecolor="white", lw=.6)
    ax.annotate("−ECS", (A.loc["−ECS", "donor recovery"],
                         A.loc["−ECS", "menstrual phase"]),
                textcoords="offset points", xytext=(6, -2), fontsize=6, color=HI)
    ax.annotate("reported arm", (FRONT["p1_dab168_kl1"][0], FRONT["p1_dab168_kl1"][1]),
                textcoords="offset points", xytext=(-8, 8), fontsize=6,
                color=BASE_C, ha="right")
    ax.set_xlabel("donor recovery  (lower better)")
    ax.set_ylabel("cross-donor phase")
    ax.grid(color=GRID, lw=.5)
    for s in ("top", "right"): ax.spines[s].set_visible(False)

def panel_e(ax):
    ax.axvline(0, color=SOFT, lw=.8, zorder=2)
    ax.hist(CORR, bins=np.arange(-0.6, 1.0, 0.1), color=ABL_C,
            edgecolor="white", lw=.5, zorder=3)
    ax.axvline(np.median(CORR), color=HI, lw=1.4, zorder=4)
    ax.annotate(f"median {np.median(CORR):+.2f}", (np.median(CORR), ax.get_ylim()[1]),
                textcoords="offset points", xytext=(4, -9), fontsize=6, color=HI)
    ax.set_xlabel("correlation, adversary loss vs donor recovery")
    ax.set_ylabel("training arms")
    p = wilcoxon(CORR).pvalue
    ax.set_title(f"positive in {int((CORR>0).sum())} of {len(CORR)} arms, "
                 f"$p$ = {p:.1e}", fontsize=6.4, color=SOFT, pad=3)
    ax.grid(axis="y", color=GRID, lw=.5, zorder=0)
    for s in ("top", "right"): ax.spines[s].set_visible(False)

def tag(ax, letter):
    ax.text(-0.075, 1.14, letter, transform=ax.transAxes, fontsize=9,
            fontweight="bold", va="top", ha="right", clip_on=False)

# ── Option A: a across the top, four below ────────────────────────────────
fig = plt.figure(figsize=(180 * MM, 150 * MM))
gs = GridSpec(3, 2, figure=fig, height_ratios=[1.25, 1, 1],
              hspace=.85, wspace=.30,
              left=.085, right=.985, top=.90, bottom=.075)
axa = fig.add_subplot(gs[0, :]); panel_a(axa); tag(axa, "a")
axb = fig.add_subplot(gs[1, 0]); panel_b(axb); tag(axb, "b")
axc = fig.add_subplot(gs[1, 1]); panel_c(axc); tag(axc, "c")
axd = fig.add_subplot(gs[2, 0]); panel_d(axd); tag(axd, "d")
axe = fig.add_subplot(gs[2, 1]); panel_e(axe); tag(axe, "e")
fig.savefig(OUT / "figure6_optionA.png", dpi=240)
plt.close(fig)

# ── Option B: a tall on the left, b-e stacked right ───────────────────────
fig = plt.figure(figsize=(180 * MM, 165 * MM))
gs = GridSpec(4, 2, figure=fig, width_ratios=[1.35, 1],
              hspace=1.0, wspace=.28,
              left=.085, right=.985, top=.92, bottom=.065)
axa = fig.add_subplot(gs[0:2, 0]); panel_a(axa); tag(axa, "a")
axd = fig.add_subplot(gs[2:4, 0]); panel_d(axd); tag(axd, "d")
axb = fig.add_subplot(gs[0, 1]); panel_b(axb); tag(axb, "b")
axc = fig.add_subplot(gs[1:3, 1]); panel_c(axc); tag(axc, "c")
axe = fig.add_subplot(gs[3, 1]); panel_e(axe); tag(axe, "e")
fig.savefig(OUT / "figure6_optionB.png", dpi=240)
plt.close(fig)

print("wrote figure6_optionA.png and figure6_optionB.png")
print(f"\npanel a: {len(A)} arms x {len(TESTS)} axes, from benchmark.csv")
print(f"panel b: {A.loc['BASE','menstrual phase']:.4f} -> "
      f"{A.loc['−phase head','menstrual phase']:.4f} = "
      f"{100*A.loc['−phase head','menstrual phase']/A.loc['BASE','menstrual phase']:.1f}% kept")
print(f"panel c: BASE best ep {int(M['BASE'].val_nb.idxmin())}, "
      f"−phase head best ep {int(M['−phase head'].val_nb.idxmin())}")
print(f"panel d: {len(FRONT)} frontier arms + the −ECS point")
print(f"panel e: {len(CORR)} arms, median {np.median(CORR):+.3f}, "
      f"positive in {int((CORR>0).sum())}")
