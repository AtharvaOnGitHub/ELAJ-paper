"""Figure 2 — how the two knobs move the frontier.

WHAT THIS FIGURE IS FOR, and what Figure 1 does instead. Figure 1 answers
"is ELAJ better": every method, both cost axes, one Pareto front drawn over
the lot. This one answers "how do the knobs work", so it carries the p-series
alone and JOINS the points. No baseline, no ablation, nothing that is not one
of the six arms of the factorial.

WHY LINES RATHER THAN A FRONT. The finding is not where the six arms sit, it
is what happens when you move one knob and hold the other. Joined by
information cost, each line is the adversary sweep at one cost and the
vertical gap between the two lines IS the cost. Joined by adversarial weight,
three near-parallel lines say the cost step does the same thing wherever you
start. Neither reads off a scatter of unconnected points.

PHASE AND CELL FAMILY ARE NOT ON ONE SCALE, AND THE ROWS SAY SO. Phase spans
0.1424 across these arms and cell family 0.0288, five times less. Letting
matplotlib autoscale each row makes the bottom row look as dramatic as the
top, which is a chart that lies by default. The rows are therefore pinned to
0.50-0.80 and 0.95-1.00, labelled once each, so the difference in scale is
read off the ticks. The bottom row is the control: the knobs trade phase
against the confounds and leave cell identity alone.

AW, 6 November: "the scales don't need to be shared but they do need to be
calibrated correctly."

    FIGDPI=1200 python figures/scripts/figure2.py
"""
from __future__ import annotations
import csv, os, re
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path("/Users/atharvawaghmare/Endo research/ELAJ")
B = ROOT / "Outputs/Benchmarks/full"
OUT = Path(__file__).resolve().parents[1] / "pinned"
MM = 1 / 25.4

AX = {"donor":  ("knn-agreement", "patient_id",      "donor recovery"),
      "mixing": ("study-mixing",  "all studies",     "study separation"),
      "phase":  ("cross-donor",   "menstrual phase", "cross-donor menstrual phase"),
      "family": ("cross-donor",   "cell family",     "cross-donor cell family")}
YLIM = {"phase": (0.50, 0.80), "family": (0.95, 1.00)}
# The two reported arms get their names; the other four are knob coordinates.
NAMED = {(168, 1): "B$_{hi}$", (168, 30): "B$_{lo}$"}

def val(arm: str, key: str) -> float:
    test, label, _ = AX[key]
    path = B / f"full_{arm}/benchmark.csv"
    for r in csv.DictReader(open(path)):
        if (re.sub(r"__.*", "", r["method"]) == "elaj"
                and r["test"] == test and r["label"] == label):
            return float(r["value"])
    raise SystemExit(f"{path} has no {test}/{label} row for elaj")

ARMS = [(d, k) for k in (1, 30) for d in (7, 168, 336)]
P = {(d, k): {a: val(f"p1_dab{d}_kl{k}", a) for a in AX} for d, k in ARMS}

KLC  = {1: "#2F6690", 30: "#8C2F39"}
DABC = {7: "#D9A441", 168: "#3A7D5D", 336: "#6D2E46"}
by_kl  = {k: [(d, k) for d in (7, 168, 336)] for k in (1, 30)}
by_dab = {d: [(d, k) for k in (1, 30)] for d in (7, 168, 336)}
INK, SOFT = "#1a1a1a", "#6b6b6b"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 6.4,
                     "text.color": INK})

COLS = [("donor",  by_kl,  KLC,  r"$w_{kl}$ %s"),
        ("mixing", by_kl,  KLC,  r"$w_{kl}$ %s"),
        ("donor",  by_dab, DABC, r"$\lambda_{dab}$ %s"),
        ("mixing", by_dab, DABC, r"$\lambda_{dab}$ %s")]

fig, axes = plt.subplots(2, 4, figsize=(190 * MM, 100 * MM),
                         sharex="col", sharey="row")
plt.subplots_adjust(left=.062, right=.995, top=.885, bottom=.095,
                    hspace=.07, wspace=.045)

def place(ax, x):
    """Push a label inward when its point is against a spine."""
    x0, x1 = ax.get_xlim()
    frac = (x - x0) / (x1 - x0)
    if frac > 0.80:  return -5, -3
    if frac < 0.20:  return 5, 4
    return 4, 4

for r, ykey in enumerate(("phase", "family")):
    for c, (xkey, groups, cols, fmt) in enumerate(COLS):
        ax = axes[r][c]
        for gk, pts in groups.items():
            ax.plot([P[p][xkey] for p in pts], [P[p][ykey] for p in pts],
                    "-o", color=cols[gk], ms=3.8, lw=1.2, label=fmt % gk, zorder=3)
        ax.set_ylim(*YLIM[ykey])
        xs = [P[a][xkey] for a in ARMS]
        pad = 0.11 * (max(xs) - min(xs))
        ax.set_xlim(max(xs) + pad, min(xs) - pad)
        placed: list[tuple[float, float]] = []
        for a in ARMS:
            x, y = P[a][xkey], P[a][ykey]
            dx, dy = place(ax, x)
            # If a label would land on one already written, drop it below.
            for px, py in placed:
                if abs(px - x) < 0.14 * abs(ax.get_xlim()[1] - ax.get_xlim()[0]) \
                        and abs(py - y) < 0.12 * (YLIM[ykey][1] - YLIM[ykey][0]):
                    dy -= 8
            placed.append((x, y))
            ax.annotate(NAMED.get(a, f"{a[0]}/{a[1]}"), (x, y), fontsize=4.4,
                        color=SOFT, xytext=(dx, dy), textcoords="offset points",
                        ha="left" if dx > 0 else "right")
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.tick_params(labelsize=5.4, color=SOFT)
        if r == 1: ax.set_xlabel(AX[xkey][2] + "  (lower is better)", fontsize=6.2)
        if c == 0: ax.set_ylabel(AX[ykey][2], fontsize=6.2)
        if r == 0: ax.legend(fontsize=5.0, frameon=False, loc="lower left",
                             handletextpad=.4, borderpad=.1)

# The two subtitles sit over the pair of columns each describes, centred on
# them rather than left-aligned to one panel.
for (c0, c1), text in (((0, 1), "joined by information cost"),
                       ((2, 3), "joined by adversarial weight")):
    x0 = axes[0][c0].get_position().x0
    x1 = axes[0][c1].get_position().x1
    fig.text((x0 + x1) / 2, .945, text, ha="center", va="bottom",
             fontsize=8.0, fontweight="bold", color=INK)

for ax, letter in zip(axes.ravel(), "abcdefgh"):
    ax.text(.015, .975, letter, transform=ax.transAxes, fontsize=7.5,
            fontweight="bold", va="top", ha="left")

fig.savefig(OUT / "figure2.png", dpi=int(os.environ.get("FIGDPI", 200)))
print(f"wrote figure2.png — 2x4, {len(ARMS)} arms, "
      f"phase span {max(P[a]['phase'] for a in ARMS) - min(P[a]['phase'] for a in ARMS):.4f}, "
      f"family span {max(P[a]['family'] for a in ARMS) - min(P[a]['family'] for a in ARMS):.4f}")
