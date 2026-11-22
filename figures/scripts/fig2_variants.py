"""Figure 2 variants for AW's 19 Nov review: panel e palettes and contour
weights, panel f in the style of 2c, and the whole figure without panel
titles in a calmer palette. Drafts only, to figures/draft/variants/.

    /Users/atharvawaghmare/miniconda3/envs/elaj/bin/python figures/scripts/fig2_variants.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fig2_panels as P                                              # noqa: E402
import fig2f_prototypes as F                                         # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "draft" / "variants"
OUT.mkdir(parents=True, exist_ok=True)
MM = 1 / 25.4

# A calmer pair: blue and orange differ in lightness as well as hue, so they
# survive colour-blindness and greyscale; both a step below full saturation.
CTL, CAS = "#4F8DA6", "#C7773F"
CTL_D, CAS_D = "#2F6B83", "#9B4F1E"              # darker, for contour lines
SOFT_DIV = LinearSegmentedColormap.from_list("soft", ["#B9D3DF", "#F3F1EC", "#E9BE9C"])
SEQ = LinearSegmentedColormap.from_list("seq", ["#F3F1EC", "#E3B48F", "#B8622C"])

E_OPTS = {
    "e_A_soft_diverging": dict(cmap=SOFT_DIV, vmin=.2, vmax=.8, clw=1.1, ctl=CTL_D, cas=CAS_D),
    "e_B_sequential":     dict(cmap=SEQ, vmin=0, vmax=1, clw=1.1, ctl=CTL_D, cas=CAS_D),
    "e_C_faded_original": dict(cmap="RdBu_r", vmin=.2, vmax=.8, clw=.85, ctl="#1F6F6A", cas="#8E2A26", alpha=.45),
}
for name, kw in E_OPTS.items():
    fig = plt.figure(figsize=(80 * MM, 66 * MM))
    ax = fig.add_axes([.14, .14, .68, .8]); cax = fig.add_axes([.84, .14, .025, .8])
    F.panel_plane(ax, cax, **kw)
    fig.savefig(OUT / f"{name}.png", dpi=300, facecolor="white"); plt.close(fig)
    print("drew", name)

for style in ("strip", "rain"):
    fig = plt.figure(figsize=(80 * MM, 66 * MM))
    axes = [fig.add_axes([.17 + i * .41, .3, .36, .62]) for i in range(2)]
    F.panel_rain(axes, style=style, ctl=CTL, cas=CAS, legend="below")
    fig.savefig(OUT / f"f_{style}_legend_below.png", dpi=300, facecolor="white"); plt.close(fig)
    print("drew f", style)

# ── the whole figure, settled (AW, 19 Nov) ─────────────────────────────
import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402
import supp_figures as S                                             # noqa: E402
from scipy.ndimage import gaussian_filter                            # noqa: E402

CTL, CAS = "#8FA9BC", "#882255"                  # f: blue-grey against wine; worst-case dE 35 under deutan, protan, tritan simulation
# NMI: Arial throughout (other modules reset it on import), editable text in the PDF
plt.rcParams.update({"font.family": "Arial", "pdf.fonttype": 42, "ps.fonttype": 42})
FS, FSS = P.FS_BODY, P.FS_SMALL
W, H = 180.0, 170.0                              # NMI: full page depth is 170 mm
fig = plt.figure(figsize=(W * MM, H * MM))
mm = lambda x, y, w, h: [x / W, y / H, w / W, h / H]


def letter(x, y, l):
    fig.text(x / W, y / H, l, fontsize=P.FS_LETTER, fontweight="bold", va="baseline", color=P.INK)


def tidy(ax):
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color("#B8BDC4"); ax.spines[sp].set_linewidth(.6)
    ax.tick_params(labelsize=FSS, length=2, color="#B8BDC4")


# a, b
ax_a = fig.add_axes(mm(14, 126, 70, 38)); ax_b = fig.add_axes(mm(106, 126, 70, 38))
P.frontier_by_kl(ax_a); P.frontier_by_dab(ax_b)
for _ax in (ax_a, ax_b):                         # NMI: sentence case, no full stop
    _ax.set_xlabel(_ax.get_xlabel()[:1].upper() + _ax.get_xlabel()[1:])
    _ax.set_ylabel(_ax.get_ylabel()[:1].upper() + _ax.get_ylabel()[1:])
letter(4, 166, "a"); letter(96, 166, "b")

# c: the cycle closes. A thick translucent band through the phase centroids,
# each segment in its stage's colour; coarse phases annotate regions, the
# finer stages sit inside the band. Statistic in the caption, not the panel.
Zs, m_, Wc, ev, rng = S._cycle_setup()
_f, _a = plt.subplots(); obs, pcirc, cen, ang = S.cycle_closes(_a, Zs, m_, Wc, ev, rng); plt.close(_f)
ax = fig.add_axes(mm(20, 78, 56, 33))
cm = plt.get_cmap("twilight"); n = len(cen)
cols = [cm(i / n) for i in range(n)]
xs, ys = list(cen.a) + [cen.a.iloc[0]], list(cen.b) + [cen.b.iloc[0]]
for i in range(n):
    ax.plot(xs[i:i + 2], ys[i:i + 2], color=cols[i], lw=9, alpha=.35, solid_capstyle="round", zorder=1)
ax.scatter(cen.a, cen.b, s=10, color=cols, ec="white", lw=.4, zorder=3)
fine = {"secretory_early": "early", "secretory_early_mid": "early-mid", "secretory_mid": "mid",
        "secretory_late": "late"}
for k_, r in cen.iterrows():
    if k_ in fine:
        ax.annotate(fine[k_], (r.a, r.b), xytext=(0, 6), textcoords="offset points", ha="center",
                    fontsize=FSS, color=P.INK)
sec = cen.loc[[k for k in fine]]
ax.text(sec.a.mean() - .15, sec.b.mean(), "secretory", fontsize=FS, color="#6b6b6b",
        style="italic", ha="center", va="center")
# The five stages that crowd together are kept apart (AW): each on its own
# leader line, fanned into the empty space to the right, in cycle order.
crowd = ["menstrual", "proliferative_early", "proliferative", "proliferative_late", "periovulatory"]
x_lab = cen.a.max() + .55
ys_lab = np.linspace(cen.b.max() + .35, cen.b.min() + .2, len(crowd))
# labels in the vertical order of their points, so no two leader lines cross
for k_, yl in zip(sorted(crowd, key=lambda q: -cen.loc[q, "b"]), ys_lab):
    r_ = cen.loc[k_]
    ax.annotate(k_.replace("_", " "), (r_.a, r_.b), xytext=(x_lab, yl), fontsize=FSS, color=P.INK,
                ha="left", va="center", arrowprops=dict(arrowstyle="-", color="#9AA3AE", lw=.45,
                                                          shrinkA=0, shrinkB=2))
ax.margins(.12); ax.set_xlim(ax.get_xlim()[0], x_lab + 1.25)
ax.set_xlabel(f"Cycle axis 1\n({ev[0]:.0%} of phase separation)", fontsize=FS)
ax.set_ylabel(f"Cycle axis 2\n({ev[1]:.0%} of phase separation)", fontsize=FS)
tidy(ax); letter(4, 118, "c")

# d: disease from each family's state, held-out donors, no study step
t = pd.read_csv(P.CLAIMS / "x12_by_family_nostudy.csv").set_index("family")
sp_ = pd.read_csv(P.CLAIMS / "x12_by_family_nostudy_splits.csv"); sp_ = sp_[sp_.kind == "held-out"]
ax = fig.add_axes(mm(106, 80, 66, 31))
for x, f in enumerate(P.FAMS):
    v = sp_.loc[sp_.family == f, "auc"].to_numpy(); med = float(np.median(v))
    vp = ax.violinplot([v], positions=[x], widths=.62, showextrema=False, points=200, bw_method=.35)
    for b in vp["bodies"]:
        b.set_facecolor(P.FAM_C[f]); b.set_edgecolor("none"); b.set_alpha(.75)
    lo, hi = np.percentile(v, [5, 95])
    ax.plot([x, x], [lo, hi], color=P.INK, lw=.8, zorder=3)
    ax.scatter([x], [med], s=14, color="white", ec=P.INK, lw=.8, zorder=4)
    ax.text(x + .07, med, f"{med:.2f}", fontsize=FSS, color=P.INK, va="center", ha="left", zorder=5,
            bbox=dict(boxstyle="square,pad=0.05", fc="white", ec="none", alpha=.8))   # NMI: no type on shading
    ax.text(x, -.07, f"{med - .5:+.2f}\nP = {float(t.loc[f, 'p']):.3f}", transform=ax.get_xaxis_transform(),
            fontsize=FSS, color="#6b6b6b", ha="center", va="top", linespacing=1.3)
ax.axhline(.5, color="#9AA3AE", lw=.7, ls=(0, (3, 2)), zorder=1)
ax.set_ylim(.4, 1.0); ax.set_yticks([.5, .75, 1.0]); ax.set_yticklabels(["0.50\nchance", "0.75", "1.00"])
ax.set_xticks(range(4)); ax.set_xticklabels([]); ax.tick_params(axis="x", length=0)
for x, f in enumerate(P.FAMS):
    ax.text(x, 1.0, f, transform=ax.get_xaxis_transform(), fontsize=FS, ha="center", va="bottom")
ax.set_ylabel("Held-out AUC", fontsize=FS); tidy(ax); letter(92, 118, "d")

# e: immune cells in the plane of the two axes
x, y, ca, li, cos, pid = F._plane_xy()
ax = fig.add_axes(mm(16, 10, 52, 52)); cax = fig.add_axes(mm(70, 10, 2.2, 52))
codes, _u = pd.factorize(pid)
is_case = pd.Series(ca).groupby(codes).first().to_numpy()
def share(c):
    u = np.unique(np.asarray(c, dtype=int)); return is_case[u].mean() if len(u) >= 8 else np.nan
hb = ax.hexbin(x, y, C=codes.astype(float), reduce_C_function=share, gridsize=34, cmap="RdBu_r",
               vmin=.2, vmax=.8, mincnt=8, linewidths=0, zorder=1, alpha=.45)
ex = np.linspace(np.percentile(x, .5), np.percentile(x, 99.5), 70)
ey = np.linspace(np.percentile(y, .5), np.percentile(y, 99.5), 70)
for sel, c, lab in ((~ca, "#4A90C2", "control cells"), (ca, "#7A1F3D", "patient cells")):   # worst-case dE 44.8
    Hh, _, _ = np.histogram2d(x[sel], y[sel], [ex, ey], density=True)
    Hh = gaussian_filter(Hh.T, 1.4)
    ax.contour(ex[:-1], ey[:-1], Hh, levels=np.percentile(Hh[Hh > 0], [80, 95]), colors=c, linewidths=.85, zorder=2)
    ax.plot([], [], color=c, lw=.85, label=lab)
lg = ax.legend(frameon=False, fontsize=FSS, loc="lower right", handlelength=1.4)
ax.text(.97, .17, f"axes' cosine {cos:.2f}", transform=ax.transAxes, fontsize=FSS, color="#6b6b6b", ha="right")
cb = plt.colorbar(hb, cax=cax); cb.outline.set_visible(False); cb.solids.set_alpha(.45)
cb.set_label("Share of donors who are patients", fontsize=FSS); cb.ax.tick_params(labelsize=FSS, length=2)
ax.set_xlabel("Lymphoid to myeloid axis", fontsize=FS); ax.set_ylabel("Control to disease axis", fontsize=FS)
tidy(ax); letter(4, 66, "e")

# f: each donor's held-out position, one shared vertical axis
marks = {"proliferative": "o", "periovulatory": "D", "secretory": "s", "menstrual": "^"}
r = np.random.default_rng(F.SEED)
axes = [fig.add_axes(mm(110, 14, 31, 50)), fig.add_axes(mm(141, 14, 31, 50))]   # stretched
lims, SD_f = [], []
for k, (ax, f) in enumerate(zip(axes, ("immune", "stromal"))):
    D = F.DON[f]; M = D[[f"z{i}" for i in range(F.Z.shape[1])]].to_numpy(); yv = D.case.to_numpy()
    tot, nn = np.zeros(len(yv)), np.zeros(len(yv))
    for _ in range(400):
        tr = r.random(len(yv)) < .7
        if len(set(yv[tr])) < 2:
            continue
        w = M[tr & ~yv].mean(0) - M[tr & yv].mean(0); w = -w / np.linalg.norm(w)
        tot[~tr] += M[~tr] @ w; nn[~tr] += 1
    sc = tot / np.maximum(nn, 1); sc = (sc - sc.mean()) / sc.std(); lims += [sc.min(), sc.max()]
    SD_f.append(pd.DataFrame({"family": f, "donor": np.arange(len(yv)) + 1,
                              "status": np.where(yv, "patient", "control"), "phase_at_biopsy": D.phase.to_numpy(),
                              "held_out_disease_score_sd": sc}))
    for xi, (sel, c) in enumerate(((~yv, CTL), (yv, CAS))):
        v = sc[sel]
        vp = ax.violinplot([v], positions=[xi], widths=.75, showextrema=False)
        for b in vp["bodies"]:
            b.set_facecolor(c); b.set_alpha(.4); b.set_edgecolor("none")
            b.get_paths()[0].vertices[:, 0] = np.clip(b.get_paths()[0].vertices[:, 0], -1e9, xi)
        for ph, mk in marks.items():
            q = sel & (D.phase.to_numpy() == ph)
            ax.scatter(xi + .07 + r.uniform(0, .25, q.sum()), sc[q], s=5, marker=mk, color=c, ec="white", lw=.2, zorder=3)
        md = float(np.median(v))
        ax.plot([xi - .32, xi], [md] * 2, color=c, lw=1.2, zorder=4)
        ax.text(xi - .16, md + .06, f"{md:+.2f}", fontsize=FSS, color=c, ha="center", va="bottom", zorder=5,
                bbox=dict(boxstyle="square,pad=0.05", fc="white", ec="none", alpha=.8))
    ax.set_xticks([0, 1]); ax.set_xticklabels([f"control\n({(~yv).sum()})", f"patient\n({yv.sum()})"], fontsize=FSS)
    ax.tick_params(axis="x", length=0)
    ax.text(.5, 1.0, f, transform=ax.transAxes, fontsize=FS, ha="center", va="bottom")
    tidy(ax)
    if k:
        ax.spines["left"].set_visible(False); ax.tick_params(axis="y", left=False, labelleft=False)
for ax in axes:
    ax.set_ylim(min(lims) - .2, max(lims) + .35)
axes[0].set_ylabel("Held-out disease score (SD)", fontsize=FS)
for ph, mk in marks.items():
    axes[0].scatter([], [], marker=mk, color="#6b6b6b", s=7, label=ph)
axes[0].legend(frameon=False, fontsize=FSS, ncol=4, loc="upper left", bbox_to_anchor=(0, -.12),
               handletextpad=.1, columnspacing=.7)
letter(96, 66, "f")
fig.savefig(OUT / "figure2_v2.png", dpi=int(os.environ.get("FIGDPI", 600)), facecolor="white")
fig.savefig(OUT / "figure2_v2.pdf", dpi=int(os.environ.get("FIGDPI", 600)), facecolor="white")          # NMI: vector, editable text

# ── SOURCE DATA (NMI): every plotted value, one sheet per panel ─────────
SRC = Path("/Users/atharvawaghmare/Endo research/ELAJ/Outputs/supplementary/source_data")
SRC.mkdir(parents=True, exist_ok=True)
with pd.ExcelWriter(SRC / "Figure2_source_data.xlsx") as xw:
    pd.DataFrame([{"adversarial_weight": d_, "information_cost": k_, "study_separation": v[0],
                   "cross_donor_phase_agreement": v[1]} for (d_, k_), v in sorted(P.KNOB.items())]
                 ).to_excel(xw, sheet_name="a_b", index=False)
    cen.reset_index().rename(columns={"ph": "phase", "a": "cycle_axis_1", "b": "cycle_axis_2",
                                      "ord": "biological_order"}).assign(
        mean_resultant_length=obs, permutation_p=pcirc).to_excel(xw, sheet_name="c", index=False)
    sp_.merge(t[["p", "n_donors"]], left_on="family", right_index=True).rename(
        columns={"auc": "held_out_auc", "p": "permutation_p"}).to_excel(xw, sheet_name="d", index=False)
    pd.DataFrame({"lymphoid_to_myeloid_axis": x, "control_to_disease_axis": y,
                  "status": np.where(ca, "patient", "control"), "donor": codes + 1, "lineage": li}
                 ).assign(axes_cosine=cos).to_excel(xw, sheet_name="e", index=False)
    pd.concat(SD_f).to_excel(xw, sheet_name="f", index=False)
print("wrote", SRC / "Figure2_source_data.xlsx")
print("drew figure2_v2")
