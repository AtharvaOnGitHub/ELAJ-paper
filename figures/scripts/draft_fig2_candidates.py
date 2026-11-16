"""Candidate panels for the new Figure 2, drawn as single drafts for AW to pick from.

    /Users/atharvawaghmare/miniconda3/envs/elaj/bin/python figures/scripts/draft_fig2_candidates.py

AW, 17 November: Figure 2 keeps its old panels b and d and gains the cycle
figure from X16 and three or four panels from "Immune genes identify
endometriosis". "A figure should create intuition without words or numbers."

So every panel here carries no statistic in its body. The numbers live in
the prose and the legend; the panel's job is the shape of the result. Each
is written to figures/draft/fig2_candidates/ as its own PNG and a contact
sheet is assembled at the end. NOTHING here touches figures/pinned/.

Sources are the same files the auditors read (axw1008/docs/paper) plus the
dumped latent, the UMAP cache and the transferred family labels. Two panels
recompute something rather than reading it: the out-of-fold donor scores
(I3) rerun the X12 step A procedure to get a per-donor number the CSV does
not hold, and the external-list rug (I6) looks up Zhao's 66 genes in our
ranking. Both are summaries over files already on disk; if either is
adopted, its numbers go to a CSV in docs/paper so the auditors can see them.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle, Circle, Wedge, FancyBboxPatch
import numpy as np
import pandas as pd
from PIL import Image
from scipy.stats import spearmanr

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figure1 import FAMILY_C, INK, SOFT, HAIR                      # noqa: E402
from supp_figures import (PHASE_ORD, PHASE_C, PHASE_ORDER, PHASE_COARSE,  # noqa: E402
                          FS_TITLE, FS_BODY, FS_LEG, MM, CELLS, CLAIMS, ARM, ROOT)

OUT = Path(__file__).resolve().parents[1] / "draft" / "fig2_candidates"
OUT.mkdir(parents=True, exist_ok=True)
DPI = 300
FAMS = ["stromal", "epithelial", "endothelial", "immune"]
FAM_C = dict(zip(FAMS, FAMILY_C))
AMBER = "#CC4E00"
WINE = "#8C2D3F"
GREY_PT = "#E3E6EA"
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


# ── shared data ──────────────────────────────────────────────────────────
print("loading latent, metadata, umap cache, transferred labels")
Z = np.load(CELLS / ARM / "latent.npy")
m = pd.read_csv(CELLS / ARM / "metadata.csv.gz", low_memory=False)
t = pd.read_csv(CELLS / ARM / "cell_family_transferred.csv.gz")
m["family_t"] = t["cell_family_transferred"].to_numpy()
xy = np.load(ROOT / f"Outputs/analysis/umaps/{ARM}/_umap_cache/global_400000.npy")
SIDX = np.sort(np.random.default_rng(24).choice(len(m), 400_000, replace=False))
assert len(SIDX) == len(xy)
SHUF = rng.permutation(len(SIDX))
Zs = (Z - Z.mean(0)) / Z.std(0)


def umap_base(ax):
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_aspect("equal", adjustable="datalim")


# ═════════════════════════════════════════════════════════════════════════
# CYCLE, from X16
# ═════════════════════════════════════════════════════════════════════════
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA  # noqa: E402
has = m["menstrual phase"].notna().values
fit = has & (m.study != "duempelmann_2026").values
idx = np.random.default_rng(0).choice(np.flatnonzero(fit), 150_000, replace=False)
lda = LDA(solver="eigen", shrinkage="auto").fit(Zs[idx], m["menstrual phase"].values[idx])
W = lda.scalings_[:, :2]
W = W / np.linalg.norm(W, axis=0, keepdims=True)
te = (m.study == "duempelmann_2026").values & m.CycleDay.notna().values
proj1 = Zs @ W[:, 0]
dn = (pd.DataFrame({"proj": proj1[te], "day": m.CycleDay.values[te],
                    "prog": m.ProgesteroneSerum.values[te],
                    "ph": m["menstrual phase"].values[te], "pid": m.patient_id.values[te]})
      .groupby("pid").agg(proj=("proj", "median"), day=("day", "median"),
                          prog=("prog", "median"), ph=("ph", "first")))
sgn = np.sign(spearmanr(dn.proj, dn.day)[0]) or 1.0
dn["proj"] *= sgn
print(f"  cycle axis vs day rho={spearmanr(dn.proj, dn.day)[0]:+.3f}, "
      f"vs progesterone {spearmanr(dn.proj, dn.prog)[0]:+.3f}  (x16 check)")

# ── C1: one axis, not nine labels. UMAP by cycle score beside UMAP by label.
fig, axes = plt.subplots(1, 2, figsize=(150 * MM, 72 * MM))
fig.subplots_adjust(left=.01, right=.99, top=.90, bottom=.02, wspace=.03)
usub = m.iloc[SIDX].reset_index(drop=True)
hs = usub["menstrual phase"].notna().to_numpy()
keep = SHUF[hs[SHUF]]
for ax in axes:
    umap_base(ax)
    ax.scatter(xy[~hs, 0], xy[~hs, 1], s=.4, c=GREY_PT, lw=0, rasterized=True, zorder=1)
ax = axes[0]
coarse = usub["menstrual phase"].map(PHASE_COARSE)
lut = dict(zip(PHASE_ORDER, PHASE_C))
k2 = keep[coarse.to_numpy()[keep] != None]  # noqa: E711  (menstrual maps to None)
rgb = np.array([lut[c] for c in coarse.to_numpy()[k2]])
ax.scatter(xy[k2, 0], xy[k2, 1], s=.4, c=rgb, lw=0, alpha=.5, rasterized=True, zorder=2)
ax.set_title("the labels the model was trained on", fontsize=FS_TITLE, loc="left")
ax.legend(handles=[Line2D([], [], marker="o", lw=0, ms=3.5, color=lut[p], label=p)
                   for p in PHASE_ORDER], loc="lower left", fontsize=FS_LEG,
          handletextpad=.3, borderpad=.2)
ax = axes[1]
sc1 = (sgn * proj1)[SIDX]
sc = ax.scatter(xy[keep, 0], xy[keep, 1], s=.4, c=sc1[keep], cmap="viridis",
                vmin=np.percentile(sc1[keep], 2), vmax=np.percentile(sc1[keep], 98),
                lw=0, alpha=.6, rasterized=True, zorder=2)
ax.set_title("the one axis the latent holds them on", fontsize=FS_TITLE, loc="left")
cax = ax.inset_axes([.03, .06, .25, .025])
cb = fig.colorbar(sc, cax=cax, orientation="horizontal", ticks=[])
cb.outline.set_visible(False)
cax.text(0, 1.6, "early", transform=cax.transAxes, fontsize=FS_LEG, ha="left", color=SOFT)
cax.text(1, 1.6, "late", transform=cax.transAxes, fontsize=FS_LEG, ha="right", color=SOFT)
save(fig, "C1_umap_labels_vs_axis")

# ── C2: the axis orders a cohort it never saw, by day and by hormone ─────
fig, axes = plt.subplots(1, 2, figsize=(120 * MM, 56 * MM))
fig.subplots_adjust(left=.10, right=.99, top=.92, bottom=.20, wspace=.30)
dn["coarse"] = dn.ph.map(PHASE_COARSE)
for ax, col, xl in zip(axes, ("day", "prog"),
                       ("cycle day recorded by the clinic", "serum progesterone (nmol/l)")):
    for p in PHASE_ORDER:
        s = dn[dn.coarse == p]
        ax.scatter(s[col], s.proj, s=18, color=lut[p], lw=.5, edgecolor="white", zorder=3)
    s = dn[dn.coarse.isna()]
    ax.scatter(s[col], s.proj, s=18, color=SOFT, lw=.5, edgecolor="white", zorder=3)
    ax.set_xlabel(xl); ax.set_yticks([])
    clean(ax, keep_y=False)
axes[0].set_ylabel("position on the cycle axis")
axes[0].annotate("", xy=(0, .95), xytext=(0, .05), xycoords="axes fraction",
                 arrowprops=dict(arrowstyle="-|>", color=SOFT, lw=.6))
fig.legend(handles=[Line2D([], [], marker="o", lw=0, ms=4, color=lut[p], label=p)
                    for p in PHASE_ORDER],
           loc="lower center", ncol=4, fontsize=FS_LEG, bbox_to_anchor=(.55, -.01))
save(fig, "C2_axis_orders_unseen_cohort")

# ── C3: the clock. Nine centroids round a ring at their measured angles ──
Pa = Zs[has] @ W
cen = (pd.DataFrame({"a": Pa[:, 0], "b": Pa[:, 1], "ph": m["menstrual phase"].values[has]})
       .groupby("ph").mean())
cen["ord"] = cen.index.map(PHASE_ORD)
cen = cen.sort_values("ord")
ang = (np.degrees(np.arctan2(cen.b, cen.a)) % 360)
# orient the ring so menstrual sits at the top and the cycle runs clockwise
a0 = ang["menstrual"]
rel = (ang - a0) % 360
clockwise = rel["secretory_late"] > 180      # if the loop runs the other way, mirror it
if not clockwise:
    rel = (-rel) % 360
theta = np.radians(90 - rel)                 # 0 at top, clockwise
cm = plt.get_cmap("twilight")
fig, ax = plt.subplots(figsize=(76 * MM, 66 * MM))
fig.subplots_adjust(0, 0, 1, 1)
ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1.9, 2.1); ax.set_ylim(-1.5, 1.95)
ax.add_patch(Circle((0, 0), 1, fc="none", ec=HAIR, lw=.8, zorder=1))
PRO = ["menstrual", "proliferative_early", "proliferative", "proliferative_late"]
SEC = ["periovulatory", "secretory_early", "secretory_early_mid", "secretory_mid", "secretory_late"]
for grp, col in ((PRO, PHASE_C[0]), (SEC, PHASE_C[2])):
    d = np.degrees(theta[grp]); lo, hi = d.min(), d.max()
    ax.add_patch(Wedge((0, 0), 1.0, lo, hi, width=.10, fc=col, ec="none", alpha=.35, zorder=2))
placed_deg: list[float] = []
for i, (k, _) in enumerate(cen.iterrows()):
    x, y = np.cos(theta[k]), np.sin(theta[k])
    ax.plot(x, y, "o", ms=7, color=cm(i / len(cen)), mec="white", mew=.6, zorder=4)
    lab = k.replace("_", " ")
    # three labels sit within a few degrees at the top, which is the 44
    # degree finding itself, so they step outward on leader lines
    d = np.degrees(theta[k]) % 360
    r = 1.18 + 0.24 * sum(1 for q in placed_deg if abs((d - q + 180) % 360 - 180) < 16)
    placed_deg.append(d)
    ha = "left" if x > .15 else ("right" if x < -.15 else "center")
    va = "bottom" if y > .15 else ("top" if y < -.15 else "center")
    if x < -.15 and y > .15:            # the two proliferative labels: one above, one below
        va = "bottom" if r > 1.2 else "top"
    if r > 1.2:
        ax.plot([1.06 * x, (r - .03) * x], [1.06 * y, (r - .03) * y], color=HAIR, lw=.5, zorder=2)
    ax.text(r * x, r * y, lab, ha=ha, va=va, fontsize=FS_LEG, color=INK)
ax.annotate("", xy=(np.cos(np.radians(60)), np.sin(np.radians(60))) ,
            xytext=(np.cos(np.radians(80)), np.sin(np.radians(80))),
            arrowprops=dict(arrowstyle="-|>", color=SOFT, lw=.6,
                            connectionstyle="arc3,rad=-0.2"))
save(fig, "C3_clock")

# ── C4: whose clock. Four family axes against the pooled axis ────────────
fam = m["cell family"].values
both = has & m["cell family"].notna().values
axd = {}
for f in FAMS:
    sel = np.flatnonzero(both & (fam == f) & (m.study != "duempelmann_2026").values)
    sel = rng.choice(sel, min(60_000, len(sel)), replace=False)
    lf = LDA(solver="eigen", shrinkage="auto").fit(Zs[sel], m["menstrual phase"].values[sel])
    v = lf.scalings_[:, 0]; axd[f] = v / np.linalg.norm(v)
cosp = {f: abs(float(axd[f] @ W[:, 0])) for f in FAMS}
print("  family |cos| vs pooled:", {k: round(v, 3) for k, v in cosp.items()})
fig, ax = plt.subplots(figsize=(70 * MM, 44 * MM))
fig.subplots_adjust(0.02, 0.05, .98, .95)
ax.axis("off"); ax.set_xlim(-.05, 1.25); ax.set_ylim(-.08, 1.0); ax.set_aspect("equal")
ax.annotate("", xy=(1.0, 0), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4, mutation_scale=10))
ax.text(1.02, 0, "the pooled cycle axis", va="center", ha="left", fontsize=FS_LEG, color=INK)
angs = {f: np.arccos(cosp[f]) for f in FAMS}
done: list[float] = []
for f in sorted(FAMS, key=lambda q: angs[q]):
    a = angs[f]
    ax.annotate("", xy=(np.cos(a), np.sin(a)), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=FAM_C[f], lw=1.3, mutation_scale=9))
    off = 0.07 if any(abs(a - q) < .08 for q in done) else 0.0
    done.append(a)
    ax.text(1.06 * np.cos(a), 1.06 * np.sin(a) + off, f, color=FAM_C[f], fontsize=FS_LEG,
            ha="left", va="center")
save(fig, "C4_whose_clock")

# ═════════════════════════════════════════════════════════════════════════
# IMMUNE, from X8 and X12
# ═════════════════════════════════════════════════════════════════════════
# ── I1: composition does not change. Every donor, four families, two groups
d3 = pd.read_csv(ROOT / "Outputs/supplementary/data/D3_per_donor_cell_family_composition.csv",
                 low_memory=False)
d3 = d3[(d3.tissue == "endometrium") & d3.disease_status.isin(["control", "eutopic"])]
tot = d3.groupby("patient_id").n_cells.transform("sum")
d3 = d3.assign(frac=d3.n_cells / tot)
fig, axes = plt.subplots(1, 4, figsize=(120 * MM, 50 * MM), sharey=False)
fig.subplots_adjust(left=.08, right=.99, top=.88, bottom=.16, wspace=.45)
for ax, f in zip(axes, FAMS):
    s = d3[d3.cell_family == f]
    for j, (grp, c) in enumerate((("control", CTL_C), ("eutopic", CASE_C))):
        v = s[s.disease_status == grp].frac.to_numpy()
        jit = rng.uniform(-.22, .22, len(v))
        ax.scatter(j + jit, v, s=7, color=c, alpha=.55, lw=0, zorder=2)
        ax.plot([j - .3, j + .3], [np.median(v)] * 2, color=INK, lw=1.1, zorder=3)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["control", "case"], fontsize=FS_LEG)
    ax.set_xlim(-.6, 1.6); ax.set_ylim(0, 1)
    ax.set_title(f, fontsize=FS_TITLE, color=FAM_C[f], loc="left")
    ax.set_yticks([0, .5, 1]); ax.tick_params(labelsize=FS_LEG)
    clean(ax)
axes[0].set_ylabel("share of a donor's cells")
save(fig, "I1_composition_unchanged")

# ── I3: the disease direction, donor by donor, out of fold ───────────────
MIN_CELLS, NSPLIT = 50, 400
keepc = (m.disease_status.isin(["control", "eutopic"]) & m["cell family"].notna()).to_numpy()
mc, Zc = m[keepc].reset_index(drop=True), Z[keepc]
oof = {}
for famname in ["all families"] + FAMS:
    sel = np.ones(len(mc), bool) if famname == "all families" else (mc["cell family"] == famname).to_numpy()
    sub, Zsub = mc[sel], Zc[sel]
    codes, uniq = pd.factorize(sub.patient_id)
    M = np.zeros((len(uniq), 16)); np.add.at(M, codes, Zsub)
    n = np.bincount(codes, minlength=len(uniq)); M /= n[:, None]
    info = sub.groupby("patient_id").first().reindex(uniq)
    ok = n >= MIN_CELLS
    M, study, y = M[ok], info.study.to_numpy()[ok], (info.disease_status == "eutopic").to_numpy()[ok]
    X = M.copy()
    for s in np.unique(study):
        k = study == s; X[k] -= X[k].mean(0)
    acc, cnt = np.zeros(len(y)), np.zeros(len(y))
    r2 = np.random.default_rng(24)
    for _ in range(NSPLIT):
        tr = r2.random(len(y)) < .7
        if len(set(y[tr])) < 2 or len(set(y[~tr])) < 2:
            continue
        w = X[tr & ~y].mean(0) - X[tr & y].mean(0); w /= np.linalg.norm(w)
        sc_ = X[~tr] @ w
        acc[~tr] += sc_; cnt[~tr] += 1
    s_ = -(acc / np.maximum(cnt, 1))          # flip so the case side is positive
    pos, neg = s_[y], s_[~y]
    auc = ((pos[:, None] > neg[None, :]).mean() + .5 * (pos[:, None] == neg[None, :]).mean())
    oof[famname] = (s_, y)
    print(f"  I3 {famname:13s} donors {len(y):3d}  out-of-fold donor AUC {auc:.3f}")
order = ["all families", "stromal", "epithelial", "endothelial", "immune"]
fig, axes = plt.subplots(1, 5, figsize=(150 * MM, 52 * MM), sharey=True)
fig.subplots_adjust(left=.07, right=.99, top=.86, bottom=.16, wspace=.12)
for ax, famname in zip(axes, order):
    s_, y = oof[famname]
    s_ = (s_ - s_.mean()) / s_.std()
    for j, (lab, c) in enumerate(((False, CTL_C), (True, CASE_C))):
        v = s_[y == lab]
        ax.scatter(j + rng.uniform(-.2, .2, len(v)), v, s=8, color=c, alpha=.6, lw=0, zorder=2)
        ax.plot([j - .32, j + .32], [np.median(v)] * 2, color=INK, lw=1.2, zorder=3)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["control", "case"], fontsize=FS_LEG)
    ax.set_xlim(-.6, 1.6)
    col = FAM_C.get(famname, INK)
    ax.set_title(famname, fontsize=FS_TITLE, color=col, loc="left")
    ax.set_yticks([]); clean(ax, keep_y=False)
axes[0].set_ylabel("score along the disease direction,\nfitted on other donors")
save(fig, "I3_direction_donor_by_donor")

# ── I2: the territory that carries disease. UMAP shaded by family AUC excess
auc_t = pd.read_csv(CLAIMS / "x12_by_family_annotated.csv").set_index("family")
exc = {f: float(auc_t.loc[f, "auc"] - auc_t.loc[f, "null"]) for f in FAMS}
print("  I2 AUC excess over null:", {k: round(v, 3) for k, v in exc.items()})
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("sig", ["#D5D9DE", "#F3C98B", AMBER])
norm = matplotlib.colors.Normalize(0, max(exc.values()))
fig, ax = plt.subplots(figsize=(72 * MM, 72 * MM))
fig.subplots_adjust(0.01, 0.01, .99, .92)
umap_base(ax)
ft = usub.family_t.to_numpy()
for f in FAMS:
    k = SHUF[(ft[SHUF] == f)]
    ax.scatter(xy[k, 0], xy[k, 1], s=.4, color=cmap(norm(max(exc[f], 0))), lw=0,
               alpha=.6, rasterized=True, zorder=2)
ax.set_title("where in the latent the disease can be read", fontsize=FS_TITLE, loc="left")
for f in FAMS:
    k = ft == f
    cx, cy = np.median(xy[k, 0]), np.median(xy[k, 1])
    ax.text(cx, cy, f, ha="center", va="center", fontsize=FS_BODY, color=INK,
            fontweight="bold", zorder=5,
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=.7))
cax = ax.inset_axes([.70, .06, .26, .025])
cb = fig.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cax,
                  orientation="horizontal", ticks=[])
cb.outline.set_visible(False)
cax.text(0, 1.6, "none", transform=cax.transAxes, fontsize=FS_LEG, ha="left", color=SOFT)
cax.text(1, 1.6, "disease signal", transform=cax.transAxes, fontsize=FS_LEG, ha="right", color=SOFT)
save(fig, "I2_umap_territory_lit")

# ── I4: the gene spectrum. 15,496 genes as one stripe, the two ends named ─
gs = pd.read_csv(CLAIMS / "x12_gene_shifts_orth.csv")
gs = gs.rename(columns={gs.columns[0]: "gene"})
gs["disease"] = -gs.shift_towards_control
gs = gs.sort_values("disease", ascending=False).reset_index(drop=True)
ext = pd.read_csv(CLAIMS / "replication_external.csv")
hits = set(ext.loc[ext.end == "disease side", "genes"].iloc[0].split(";"))
novel = {"SIGLEC7", "ADAMDEC1", "ALPK2", "KCNH1"}
fig, ax = plt.subplots(figsize=(150 * MM, 48 * MM))
fig.subplots_adjust(left=.03, right=.97, top=.82, bottom=.46)
yv = gs.disease.values; n = len(yv)
ax.fill_between(np.arange(n), 0, yv, where=yv > 0, color=WINE, alpha=.9, lw=0)
ax.fill_between(np.arange(n), 0, yv, where=yv < 0, color="#9AA3AE", alpha=.9, lw=0)
ax.axhline(0, color=HAIR, lw=.5)
ax.set_xlim(-n * .01, n * 1.01); ax.set_yticks([]); ax.set_xticks([])
clean(ax, keep_x=False, keep_y=False)
ax.text(0, 1.04, "towards disease", transform=ax.transAxes, fontsize=FS_BODY, color=WINE, va="bottom")
ax.text(1, 1.04, "towards control", transform=ax.transAxes, fontsize=FS_BODY, color=SOFT,
        va="bottom", ha="right")
top = gs.head(15)
# a bracket under the first 0.1% of the stripe, and the names in three columns beneath it
ax.plot([0, 0, n * .03, n * .03], [-.03, -.06, -.06, -.03], transform=ax.get_xaxis_transform(),
        color=SOFT, lw=.6, clip_on=False)
for i, r in top.iterrows():
    c = WINE if r.gene in hits else (AMBER if r.gene in novel else SOFT)
    col_, row_ = divmod(i, 5)
    ax.text(.01 + col_ * .11, -.14 - row_ * .13, r.gene, transform=ax.transAxes,
            fontsize=FS_LEG, color=c, ha="left", va="top",
            fontweight="bold" if c != SOFT else "normal")
ax.text(.99, -.14, "no gene at this end is\non the external list", transform=ax.transAxes,
        fontsize=FS_LEG, color=SOFT, ha="right", va="top", linespacing=1.4)
ax.legend(handles=[Line2D([], [], marker="s", lw=0, color=WINE, ms=5, label="reported up in an external cohort"),
                   Line2D([], [], marker="s", lw=0, color=AMBER, ms=5, label="no prior endometriosis report"),
                   Line2D([], [], marker="s", lw=0, color=SOFT, ms=5, label="other top-fifteen genes")],
          loc="upper right", bbox_to_anchor=(1, 1.0), fontsize=FS_LEG, ncol=1)
save(fig, "I4_gene_spectrum")

# ── I5: the evidence matrix. Fifteen genes against four places to look ───
# Presence/absence read off CLAIMS_SUMMARY.md's "fifteen disease-side genes,
# lined up" table. Hollow = named in a corpus paper only as a label, never
# tested. If adopted this table becomes a CSV in docs/paper.
EVID = {  # gene: (Zhao 2017 up-list, corpus papers, Open Targets, PubMed)
    "IL1B":     (0, 2, 2, 2), "SERPINB2": (2, 2, 2, 2), "MMP27":   (2, 0, 0, 2),
    "LRRC15":   (2, 1, 2, 0), "INHBA":    (2, 1, 2, 2), "DKK1":    (0, 2, 2, 2),
    "CCL13":    (0, 0, 2, 2), "TREM1":    (0, 0, 0, 2), "MMP19":   (0, 1, 0, 2),
    "CST11":    (0, 0, 2, 0), "SCARA5":   (0, 1, 2, 0), "SIGLEC7": (0, 0, 0, 0),
    "ADAMDEC1": (0, 0, 0, 0), "ALPK2":    (0, 0, 0, 0), "KCNH1":   (0, 0, 0, 0)}
COLS = ["external\ncohort", "pooled\nstudies", "Open\nTargets", "PubMed"]
genes = [g for g in gs.head(15).gene if g in EVID]
assert len(genes) == 15, genes
fig, ax = plt.subplots(figsize=(70 * MM, 78 * MM))
fig.subplots_adjust(left=.26, right=.98, top=.86, bottom=.03)
ax.set_xlim(-.6, 3.6); ax.set_ylim(-.6, 14.6); ax.invert_yaxis()
ax.axis("off")
for j, c in enumerate(COLS):
    ax.text(j, -1.0, c, ha="center", va="bottom", fontsize=FS_LEG, color=INK, linespacing=1.2)
for i, g in enumerate(genes):
    col = WINE if g in hits else (AMBER if g in novel else INK)
    ax.text(-.75, i, g, ha="right", va="center", fontsize=FS_BODY, color=col,
            fontweight="bold" if g in hits | novel else "normal")
    for j, v in enumerate(EVID[g]):
        if v == 2:
            ax.scatter(j, i, s=60, color=INK if j else WINE, lw=0, zorder=3)
        elif v == 1:
            ax.scatter(j, i, s=60, facecolor="white", edgecolor=INK, lw=.8, zorder=3)
        else:
            ax.scatter(j, i, s=7, color=HAIR, lw=0, zorder=2)
    if g in novel:
        ax.add_patch(Rectangle((-.5, i - .45), 4.0, .9, fc=AMBER, ec="none", alpha=.08, zorder=1))
save(fig, "I5_evidence_matrix")

# ── I6: where an external cohort's genes fall in our ranking ─────────────
txt = re.sub(r"\s+", " ", (ROOT.parent / "Atharva Papers" / "Validation" / "PMC5449958.txt").read_text())
up, dnl = set(), set()
for g, d, f in re.findall(r"\b([A-Z0-9orf.-]{2,15})\b ENSG\d+ (Upregulated|Downregulated) ([\d.]+)", txt):
    (up if d == "Upregulated" else dnl).add(g)
rank = pd.Series(np.arange(1, n + 1), index=gs.gene)
ru = rank.reindex(sorted(up)).dropna().astype(int).sort_values()
rd = rank.reindex(sorted(dnl)).dropna().astype(int).sort_values()
print(f"  I6 external up-list: {len(up)} genes, {len(ru)} in our vocabulary; "
      f"down-list {len(dnl)}, {len(rd)} in vocabulary")
print(f"     up-list genes in our top 1%: {(ru <= n * .01).sum()}, top 5%: {(ru <= n * .05).sum()}")
fig, axes = plt.subplots(2, 1, figsize=(120 * MM, 58 * MM), sharex=True,
                         gridspec_kw={"height_ratios": [1, 3.2], "hspace": .08})
fig.subplots_adjust(left=.09, right=.98, top=.90, bottom=.17)
ax = axes[0]
ax.vlines(ru.values, 0, 1, color=WINE, lw=.7, alpha=.9)
ax.set_ylim(0, 1); ax.set_yticks([]); clean(ax, keep_x=False, keep_y=False)
ax.set_title("the external cohort's upregulated genes, placed on our ranking",
             fontsize=FS_TITLE, loc="left")
ax = axes[1]
xs = np.concatenate([[0], ru.values, [n]]); ys = np.concatenate([[0], np.arange(1, len(ru) + 1), [len(ru)]]) / len(ru)
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

# ═════════════════════════════════════════════════════════════════════════
# FIGURE 1a: a new-genes pictogram for the Outcomes column
# ═════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(46 * MM, 14 * MM))
fig.subplots_adjust(0, 0, 1, 1); ax.axis("off"); ax.set_xlim(0, 46); ax.set_ylim(0, 14)
ax.set_aspect("equal")
# a strand of gene tags; four lit, with a small mark above each
xs_ = np.linspace(2.5, 17.5, 8)
lit = {1, 3, 4, 6}
for i, x in enumerate(xs_):
    on = i in lit
    ax.add_patch(FancyBboxPatch((x - .8, 4.2), 1.6, 4.6, boxstyle="round,pad=0.15",
                                fc="#FFF3DE" if on else "#EDEFF2",
                                ec="#D89120" if on else "#6B7380", lw=.9 if on else .6, zorder=3))
    if on:
        ax.plot([x - .25, x, x + .25], [10.0, 10.7, 10.0], color="#D89120", lw=.8, zorder=4)
ax.plot([1.5, 18.5], [6.5, 6.5], color="#6B7380", lw=.6, zorder=1)
ax.text(21, 8.4, "four genes never before", ha="left", va="center", fontsize=5.6, color="#6F7681")
ax.text(21, 5.4, "reported in endometriosis", ha="left", va="center", fontsize=5.6, color="#6F7681")
save(fig, "F1a_new_genes_pictogram")

# ── contact sheet ────────────────────────────────────────────────────────
ims = [Image.open(p) for p in WRITTEN]
cols = 3
wmax = max(i.width for i in ims); hmax = max(i.height for i in ims)
rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (cols * wmax + (cols + 1) * 40, rows * (hmax + 90) + 40), "white")
from PIL import ImageDraw                                                  # noqa: E402
dr = ImageDraw.Draw(sheet)
for k, (p, im) in enumerate(zip(WRITTEN, ims)):
    r, c = divmod(k, cols)
    x0 = 40 + c * (wmax + 40); y0 = 40 + r * (hmax + 90)
    dr.text((x0, y0), p.stem, fill="black")
    sheet.paste(im, (x0, y0 + 60))
sheet.save(OUT / "contact_sheet.png")
print(f"contact sheet: {OUT / 'contact_sheet.png'}")
