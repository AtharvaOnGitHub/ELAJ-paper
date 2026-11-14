"""Supplementary Figures S1 and S2 — the sizing argument, drawn.

    python figures/scripts/supp_sizing.py

Reads `Outputs/analysis/param_sweep.csv`, which is MEASURED: every row is a
real model built at that configuration and counted. The shipped row must read
1,883,986 or the sweep is not of our model and nothing here is valid.

S1 is AW's original Image 1, parameter count against group size across gene
counts and token widths, with the four-million ceiling drawn on it.

S2 is the argument. Panel (a) is his Image 2, cost and capacity on twin axes,
which shows the two moving together in G. Panel (b) is the part the memo did
not have: the band of group sizes each token width actually permits, with
both constraints applied, and the shipped configuration marked inside it.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
SWEEP = ROOT / "Outputs/analysis/param_sweep.csv"
OUT = Path(__file__).resolve().parents[2] / "supplementary" / "figures"

D_SHIPPED, K_SHIPPED, d_SHIPPED, P_SHIPPED = 15496, 44, 32, 1_883_986
G_SHIPPED = 352                      # the mean; the median is 342
P_CEILING = 4e6
DEFF_FLOOR = 512

FS = 7.0
INK, SOFT = "#22223B", "#8D99AE"
# Okabe-Ito, colourblind-safe by construction, same family as Figure 1
DCOL = {16: "#0072B2", 32: "#E69F00", 48: "#009E73", 64: "#CC79A7"}

plt.rcParams.update({
    "font.family": "Arial", "font.size": FS,
    "axes.edgecolor": INK, "axes.labelcolor": INK,
    "xtick.color": INK, "ytick.color": INK,
    "axes.linewidth": 0.6, "xtick.major.width": 0.6,
    "ytick.major.width": 0.6, "legend.frameon": False,
})


def dress(ax, xlabel=None, ylabel=None, title=None):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=2, pad=2, labelsize=FS)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=FS, labelpad=2)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=FS, labelpad=2)
    if title:
        ax.set_title(title, fontsize=FS, color=INK, pad=3, loc="left")


def letter(ax, ch):
    ax.text(-0.02, 1.06, ch, transform=ax.transAxes, fontsize=FS + 2.5,
            fontweight="bold", va="bottom", ha="right", color=INK)


def fit(df, D, d):
    """P = a + b/G for this (D, d). The form is the architecture's, not a
    curve chosen to fit: a = D*d + C(d) and b = D*E(d)."""
    g = df[(df.D == D) & (df.d == d)].drop_duplicates("G").sort_values("G")
    x, y = 1.0 / g.G.values, g.parameters.values.astype(float)
    A = np.vstack([np.ones_like(x), x]).T
    (a, b), *_ = np.linalg.lstsq(A, y, rcond=None)
    return a, b


def feasible_band(a, b, D, d):
    """The G range where P < 4e6 and d_eff > 512 both hold."""
    g_lo = b / (P_CEILING - a)          # P(G) < ceiling
    g_hi = d * D / DEFF_FLOOR           # d*D/G > 512
    return g_lo, g_hi


def main() -> int:
    if not SWEEP.exists():
        sys.exit(f"no sweep at {SWEEP}. Run scripts/count_params_sweep.py.")
    df = pd.read_csv(SWEEP)
    ship = df[df.is_shipped == 1]
    if ship.empty or int(ship.parameters.iloc[0]) != P_SHIPPED:
        sys.exit("the sweep does not contain the shipped model; refusing to draw")
    OUT.mkdir(parents=True, exist_ok=True)
    dims = sorted(df.d.unique())

    # ── S1: his Image 1, with the ceiling ─────────────────────────────────
    Ds = [D for D in sorted(df.D.unique()) if D != D_SHIPPED]
    fig, axes = plt.subplots(1, len(Ds), figsize=(180 / 25.4, 55 / 25.4),
                             sharey=True)
    for ax, D in zip(np.atleast_1d(axes), Ds):
        for d in dims:
            g = df[(df.D == D) & (df.d == d)].drop_duplicates("G").sort_values("G")
            ax.plot(g.G, g.parameters / 1e6, "-", lw=1.1, color=DCOL[d],
                    label=f"$d$ = {d}")
        ax.axhline(P_CEILING / 1e6, color=SOFT, lw=0.8, ls=(0, (4, 3)))
        ax.set_ylim(0, 11)
        dress(ax, "group size $G$ (genes per group)",
              "model parameters (millions)" if D == Ds[0] else None,
              f"$D$ = {D:,} genes")
    np.atleast_1d(axes)[0].text(2500, P_CEILING / 1e6 + 0.25, "4 M ceiling",
                                fontsize=FS - 0.5, color=SOFT, ha="right")
    np.atleast_1d(axes)[-1].legend(fontsize=FS - 0.5, loc="upper right",
                                   handlelength=1.4, labelspacing=0.3)
    fig.tight_layout(pad=0.4)
    fig.savefig(OUT / "S1_params_vs_groupsize.png", dpi=600,
                bbox_inches="tight")
    plt.close(fig)

    # ── S2: the argument ──────────────────────────────────────────────────
    fig = plt.figure(figsize=(180 / 25.4, 68 / 25.4))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1.0], wspace=0.42)

    ax = fig.add_subplot(gs[0, 0])
    ax2 = ax.twinx()
    ax2.spines["top"].set_visible(False)
    for d in dims:
        g = df[(df.D == D_SHIPPED) & (df.d == d)].drop_duplicates("G").sort_values("G")
        ax.plot(g.G, g.parameters / 1e6, "-", lw=1.1, color=DCOL[d],
                label=f"$d$ = {d}")
        ax2.plot(g.G, g.d_effective, ls=(0, (3, 2)), lw=1.0, color=DCOL[d])
    ax.axhline(P_CEILING / 1e6, color=SOFT, lw=0.8, ls=(0, (1, 2)))
    ax2.axhline(DEFF_FLOOR, color=SOFT, lw=0.8, ls=(0, (1, 2)))
    ax.set_ylim(0, 6.2)
    ax2.set_ylim(0, 3100)
    dress(ax, "group size $G$ (genes per group)", "model parameters (millions)")
    ax2.set_ylabel("effective gene-space dimension  $d\\,D/G$", fontsize=FS,
                   labelpad=3)
    ax2.tick_params(length=2, pad=2, labelsize=FS)
    ax.set_title("cost and capacity move together in $G$", fontsize=FS,
                 color=INK, pad=3, loc="left")
    ax.text(0.98, P_CEILING / 1e6 / 6.2 + 0.015, "4 M", transform=ax.transAxes,
            fontsize=FS - 0.5, color=SOFT, ha="right", va="bottom")
    # left-hand side: at the right the floor line runs under the d=48 curve
    ax2.text(0.015, DEFF_FLOOR / 3100 + 0.015, "512", transform=ax2.transAxes,
             fontsize=FS - 0.5, color=SOFT, ha="left", va="bottom")
    ax.plot([], [], "-", color=INK, lw=1.0, label="parameters")
    ax.plot([], [], ls=(0, (3, 2)), color=INK, lw=1.0, label="$d_{eff}$")
    ax.legend(fontsize=FS - 0.5, loc="upper center", ncol=3,
              handlelength=1.4, columnspacing=1.0, labelspacing=0.25)
    letter(ax, "a")

    axb = fig.add_subplot(gs[0, 1])
    for i, d in enumerate(dims):
        a, b = fit(df, D_SHIPPED, d)
        lo, hi = feasible_band(a, b, D_SHIPPED, d)
        axb.plot([lo, hi], [i, i], lw=5.5, color=DCOL[d], solid_capstyle="butt",
                 alpha=0.85)
        axb.text(hi + 40, i, f"{lo:,.0f} to {hi:,.0f}", fontsize=FS - 0.5,
                 va="center", ha="left", color=SOFT)
    axb.axvspan(250, 500, color=INK, alpha=0.06, lw=0)
    axb.axvline(250, color=SOFT, lw=0.6, ls=(0, (2, 2)))
    axb.axvline(500, color=SOFT, lw=0.6, ls=(0, (2, 2)))
    axb.scatter([G_SHIPPED], [dims.index(d_SHIPPED)], s=26, zorder=5,
                facecolor="white", edgecolor=INK, linewidth=1.0)
    axb.annotate("ELAJ\n$G=D/K=$ 352, $d$ = 32",
                 (G_SHIPPED, dims.index(d_SHIPPED)),
                 textcoords="offset points", xytext=(0, -24), ha="center",
                 fontsize=FS - 0.5, color=INK)
    axb.set_yticks(range(len(dims)))
    axb.set_yticklabels([f"$d$ = {d}" for d in dims])
    axb.set_xlim(0, 2150)
    axb.set_ylim(-0.75, len(dims) - 0.35)
    axb.text(375, len(dims) - 0.55, "build bounds\n250 to 500", fontsize=FS - 0.5,
             color=SOFT, ha="center", va="top")
    dress(axb, "group size $G$ (genes per group)", None,
          "what each token width permits")
    letter(axb, "b")

    fig.savefig(OUT / "S2_params_and_deff.png", dpi=600, bbox_inches="tight")
    plt.close(fig)

    print(f"wrote {OUT/'S1_params_vs_groupsize.png'}")
    print(f"wrote {OUT/'S2_params_and_deff.png'}")
    print("\nfeasible bands at D = 15,496:")
    for d in dims:
        a, b = fit(df, D_SHIPPED, d)
        lo, hi = feasible_band(a, b, D_SHIPPED, d)
        E, C = b / D_SHIPPED, a - D_SHIPPED * d
        print(f"  d={d:>3}  G in [{lo:7.0f}, {hi:7.0f}]   "
              f"E(d)={E:>9,.0f}  C(d)={C:>9,.0f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
