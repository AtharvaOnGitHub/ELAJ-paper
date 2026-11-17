"""Candidate panels for the new Figure 2, second round, after AW's comments.

    /Users/atharvawaghmare/miniconda3/envs/elaj/bin/python figures/scripts/draft_fig2_candidates.py

AW, 17 November: Figure 2 keeps its old panels b and d and gains panels from
"Immune genes identify endometriosis". "A figure should create intuition
without words or numbers." Every panel here carries no statistic in its body.

ROUND ONE'S VERDICTS (AW, 17 November), and where each went:
  C1  the cycle-axis UMAP        -> main-text Figure 4f (figure4.py)
  C2  the axis on an unseen cohort -> Supplementary Note 3 (supp_figures.x16)
  C3  the clock                  dropped: "doesn't convey any number"
  C4  whose clock                dropped: "too abstract and could mean anything"
  I1  composition unchanged      KEPT as a Figure 2 panel, redrawn here unchanged
  I2  UMAP lit by disease signal REDRAWN without a UMAP: "we already have 10
                                 UMAPs in the main figures"  -> I2b
  I3  direction donor by donor   dropped: "too much figure for too little information"
  I4  the gene spectrum          REDRAWN: "the 'towards control' side raises more
                                 questions than the intuition it creates" and
                                 "a little too wide"  -> I4b
  I5  the evidence matrix        dropped: "not needed"
  I6  external list on our ranking  KEPT pending: AW wants to understand it first
  F1  new-genes pictogram        -> Figure 1a Outcomes (mock_fig1a_opt8.py)
Round one's code is in git at 01a52d6; its PNGs are in _superseded/.

NOTHING here touches figures/pinned/.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figure1 import FAMILY_C, INK, SOFT, HAIR                      # noqa: E402
from supp_figures import FS_TITLE, FS_BODY, FS_LEG, MM, CLAIMS, ROOT  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "draft" / "fig2_candidates"
OUT.mkdir(parents=True, exist_ok=True)
DPI = 300
FAMS = ["stromal", "epithelial", "endothelial", "immune"]
FAM_C = dict(zip(FAMS, FAMILY_C))
AMBER = "#CC4E00"
WINE = "#8C2D3F"
CTL_C, CASE_C = "#5BA3A0", "#C2544E"      # control teal, case rose, as Fig 1a
rng = np.random.default_rng(0)

plt.rcParams.update({"font.family": "Arial", "font.size": FS_BODY,
                     "text.color": INK, "axes.labelcolor": INK,
                     "xtick.color": SOFT, "ytick.color": SOFT,
                     "axes.edgecolor": HAIR, "axes.linewidth": .5,
                     "legend.frameon": False})

WRITTEN: list[Path] = []


def save(fig, name):
    p = OUT / f"{name}.png"
    fig.savefig(p, dpi=DPI, facecolor="white")
    plt.close(fig)
    WRITTEN.append(p)
    print(f"  wrote {p.name}")


def clean(ax, keep_x=True, keep_y=True):
    for s, k in (("top", False), ("right", False), ("bottom", keep_x), ("left", keep_y)):
        ax.spines[s].set_visible(k)


# ── I1: composition does not change. Every donor, four families, two groups
d3 = pd.read_csv(ROOT / "Outputs/supplementary/data/D3_per_donor_cell_family_composition.csv",
                 low_memory=False)
d3 = d3[(d3.tissue == "endometrium") & d3.disease_status.isin(["control", "eutopic"])]
tot = d3.groupby("patient_id").n_cells.transform("sum")
d3 = d3.assign(frac=d3.n_cells / tot)


def draw_i1(axes):
    for ax, f in zip(axes, FAMS):
        s = d3[d3.cell_family == f]
        for j, (grp, c) in enumerate((("control", CTL_C), ("eutopic", CASE_C))):
            v = s[s.disease_status == grp].frac.to_numpy()
            jit = np.random.default_rng(j).uniform(-.22, .22, len(v))
            ax.scatter(j + jit, v, s=7, color=c, alpha=.55, lw=0, zorder=2)
            ax.plot([j - .3, j + .3], [np.median(v)] * 2, color=INK, lw=1.1, zorder=3)
        ax.set_xticks([0, 1]); ax.set_xticklabels(["control", "case"], fontsize=FS_LEG)
        ax.set_xlim(-.6, 1.6); ax.set_ylim(0, 1)
        ax.set_title(f, fontsize=FS_TITLE, color=FAM_C[f], loc="left")
        ax.set_yticks([0, .5, 1]); ax.tick_params(labelsize=FS_LEG)
        clean(ax)
    axes[0].set_ylabel("share of a donor's cells")


fig, axes = plt.subplots(1, 4, figsize=(120 * MM, 50 * MM))
fig.subplots_adjust(left=.08, right=.99, top=.88, bottom=.16, wspace=.45)
draw_i1(axes)
save(fig, "I1_composition_unchanged")

# ── I2b: where the disease can be read, without a UMAP ───────────────────
# The same four families as I1, one column each, so the two can stack: I1
# says how MANY of each family a donor has (unchanged), I2b says how well a
# donor's disease status can be read from the STATE of that family's cells.
# Dot = donor-level AUC, whisker = its bootstrap interval, the dashed line =
# the permutation null. The axis is labelled in words only, per the brief;
# the AUCs live in the legend and in x12_by_family_annotated.csv.
auc_t = pd.read_csv(CLAIMS / "x12_by_family_annotated.csv").set_index("family")


def draw_i2b(axes, with_ylabel=True):
    lo_all = min(auc_t.loc[FAMS, "auc_lo"].min(), .30)
    for ax, f in zip(axes, FAMS):
        r = auc_t.loc[f]
        ax.axhline(r.null, color=SOFT, lw=.7, ls=(0, (3, 2)), zorder=1)
        ax.plot([0, 0], [r.auc_lo, r.auc_hi], color=FAM_C[f], lw=1.6,
                solid_capstyle="round", alpha=.45, zorder=2)
        ax.scatter([0], [r.auc], s=46, color=FAM_C[f], ec="white", lw=.8, zorder=3)
        ax.set_xlim(-1, 1); ax.set_ylim(lo_all - .02, 1.0)
        ax.set_xticks([])
        # one tick, "perfect", on the first column only; the dashed null is
        # named where it starts rather than by a tick that would sit a hair
        # off it (the permutation null is 0.48-0.50, not exactly 0.5)
        ax.set_yticks([1.0])                  # same on every column: y may be shared
        ax.set_yticklabels(["perfect"], fontsize=FS_LEG)
        if ax is axes[0]:
            ax.text(-1, r.null + .015, "chance", fontsize=FS_LEG, color=SOFT,
                    ha="left", va="bottom")
        if ax is not axes[0]:                 # shared y: hide, do not unset
            ax.tick_params(labelleft=False, left=False)
        clean(ax, keep_x=False)
    if with_ylabel:
        axes[0].set_ylabel("disease read from\nthe cells' state", fontsize=FS_BODY)


fig, axes = plt.subplots(1, 4, figsize=(120 * MM, 40 * MM), sharey=True)
fig.subplots_adjust(left=.13, right=.99, top=.86, bottom=.08, wspace=.45)
draw_i2b(axes)
for ax, f in zip(axes, FAMS):
    ax.set_title(f, fontsize=FS_TITLE, color=FAM_C[f], loc="left")
save(fig, "I2b_family_signal")

# ── I1 over I2b: the pair as it would sit in Figure 2 ────────────────────
# Same columns, so a reader reads down each family: its numbers do not move
# with disease, its cells' state does, and most of all in immune.
fig, axes = plt.subplots(2, 4, figsize=(120 * MM, 82 * MM),
                         gridspec_kw={"height_ratios": [1.25, 1], "hspace": .32})
fig.subplots_adjust(left=.13, right=.99, top=.93, bottom=.05, wspace=.45)
draw_i1(axes[0])
for ax in axes[1][1:]:
    ax.sharey(axes[1][0])
draw_i2b(axes[1])
save(fig, "I1_I2b_stacked")

# ── I4b: the disease end only, and narrow ────────────────────────────────
# Round one drew all 15,496 genes as a two-sided spectrum. The control side
# made a reader ask what lives there, which is not the result. So: the
# fifteen genes that shift most towards disease, ranked, coloured by what is
# known about them. A slim bar above the list shows where they sit in the
# full ranking: the tip, and nothing more is said about the rest.
gs = pd.read_csv(CLAIMS / "x12_gene_shifts_orth.csv")
gs = gs.rename(columns={gs.columns[0]: "gene"})
gs["disease"] = -gs.shift_towards_control
gs = gs.sort_values("disease", ascending=False).reset_index(drop=True)
n = len(gs)
ext = pd.read_csv(CLAIMS / "replication_external.csv")
hits = set(ext.loc[ext.end == "disease side", "genes"].iloc[0].split(";"))
novel = {"SIGLEC7", "ADAMDEC1", "ALPK2", "KCNH1"}
top = gs.head(15)


def gene_colour(g):
    return WINE if g in hits else (AMBER if g in novel else "#9AA3AE")


fig = plt.figure(figsize=(64 * MM, 80 * MM))
ax0 = fig.add_axes([.30, .885, .66, .028])          # the whole ranking, as a sliver
ax0.add_patch(plt.Rectangle((0, 0), 1, 1, fc="#E6E8EC", ec="none"))
ax0.add_patch(plt.Rectangle((0, 0), .012, 1, fc=WINE, ec="none"))
ax0.set_xlim(0, 1); ax0.set_ylim(0, 1); ax0.axis("off")
ax0.text(0, 1.5, "every gene, ranked by shift towards disease", fontsize=FS_LEG,
         color=SOFT, va="bottom", transform=ax0.transAxes)
ax = fig.add_axes([.30, .19, .66, .66])
fig.add_artist(Line2D([.30, .30], [.885, .85], color=HAIR, lw=.5))
fig.add_artist(Line2D([.30 + .66 * .012, .96], [.885, .85], color=HAIR, lw=.5))
y = np.arange(len(top))
for i, r in top.iterrows():
    c = gene_colour(r.gene)
    ax.plot([0, r.disease], [i, i], color=c, lw=1.4, solid_capstyle="butt", zorder=2)
    ax.scatter([r.disease], [i], s=16, color=c, lw=0, zorder=3)
    ax.text(-.004 * top.disease.max() / .07, i, r.gene, ha="right", va="center",
            fontsize=FS_BODY, color=INK if c != "#9AA3AE" else SOFT,
            fontweight="bold" if c != "#9AA3AE" else "normal")
ax.set_ylim(len(top) - .4, -.6)
ax.set_xlim(0, top.disease.max() * 1.05)
ax.set_xticks([]); ax.set_yticks([])
clean(ax, keep_x=False, keep_y=False)
ax.axvline(0, color=HAIR, lw=.6)
fig.legend(handles=[Line2D([], [], marker="o", lw=0, color=WINE, ms=4,
                           label="reported up in an external cohort"),
                    Line2D([], [], marker="o", lw=0, color=AMBER, ms=4,
                           label="no prior endometriosis report"),
                    Line2D([], [], marker="o", lw=0, color="#9AA3AE", ms=4,
                           label="linked to endometriosis before")],
           loc="lower left", bbox_to_anchor=(.04, .01), fontsize=FS_LEG,
           handletextpad=.2, labelspacing=.35)
save(fig, "I4b_disease_end")

# ── I6: where an external cohort's genes fall in our ranking (unchanged) ──
txt = re.sub(r"\s+", " ", (ROOT.parent / "Atharva Papers" / "Validation" / "PMC5449958.txt").read_text())
up, dnl = set(), set()
for g, d, f in re.findall(r"\b([A-Z0-9orf.-]{2,15})\b ENSG\d+ (Upregulated|Downregulated) ([\d.]+)", txt):
    (up if d == "Upregulated" else dnl).add(g)
rank = pd.Series(np.arange(1, n + 1), index=gs.gene)
ru = rank.reindex(sorted(up)).dropna().astype(int).sort_values()
print(f"  I6 external up-list: {len(up)} genes, {len(ru)} in our vocabulary; "
      f"in our top 1%: {(ru <= n * .01).sum()}, top 5%: {(ru <= n * .05).sum()}, "
      f"top half: {(ru <= n * .5).sum()}")
fig, axes = plt.subplots(2, 1, figsize=(120 * MM, 58 * MM), sharex=True,
                         gridspec_kw={"height_ratios": [1, 3.2], "hspace": .08})
fig.subplots_adjust(left=.09, right=.98, top=.90, bottom=.17)
ax = axes[0]
ax.vlines(ru.values, 0, 1, color=WINE, lw=.7, alpha=.9)
ax.set_ylim(0, 1); ax.set_yticks([]); clean(ax, keep_x=False, keep_y=False)
ax.set_title("the external cohort's upregulated genes, placed on our ranking",
             fontsize=FS_TITLE, loc="left")
ax = axes[1]
xs = np.concatenate([[0], ru.values, [n]])
ys = np.concatenate([[0], np.arange(1, len(ru) + 1), [len(ru)]]) / len(ru)
ax.step(xs, ys, where="post", color=WINE, lw=1.3, zorder=3)
ax.plot([0, n], [0, 1], color=HAIR, lw=.8, ls="--", zorder=2)
ax.set_xlim(0, n); ax.set_ylim(0, 1.02)
ax.set_yticks([0, .5, 1]); ax.set_yticklabels(["0", "half", "all"], fontsize=FS_LEG)
ax.set_xticks([1, n]); ax.set_xticklabels(["most towards disease", "most towards control"], fontsize=FS_LEG)
ax.get_xticklabels()[0].set_ha("left"); ax.get_xticklabels()[1].set_ha("right")
ax.set_ylabel("share of their list\nreached", fontsize=FS_BODY)
clean(ax)
ax.text(n * .55, .30, "if their list were spread evenly", fontsize=FS_LEG, color=SOFT, rotation=23)
save(fig, "I6_external_list_on_our_ranking")

# ── contact sheet ────────────────────────────────────────────────────────
ims = [Image.open(p) for p in WRITTEN]
cols = 2
wmax = max(i.width for i in ims); hmax = max(i.height for i in ims)
rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (cols * wmax + (cols + 1) * 40, rows * (hmax + 90) + 40), "white")
dr = ImageDraw.Draw(sheet)
for k, (p, im) in enumerate(zip(WRITTEN, ims)):
    r, c = divmod(k, cols)
    x0 = 40 + c * (wmax + 40); y0 = 40 + r * (hmax + 90)
    dr.text((x0, y0), p.stem, fill="black")
    sheet.paste(im, (x0, y0 + 60))
sheet.save(OUT / "contact_sheet.png")
print(f"contact sheet: {OUT / 'contact_sheet.png'}")
