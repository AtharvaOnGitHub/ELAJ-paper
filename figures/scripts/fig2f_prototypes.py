"""Figure 2f prototypes, AW 19 Nov. Drafts only, to figures/draft/.

    /Users/atharvawaghmare/miniconda3/envs/elaj/bin/python figures/scripts/fig2f_prototypes.py

1 swing map: each family's disease direction drawn on the UMAP as arrows
  (per tile, the way that family's disease score rises across the map).
2 stacked bar: donor-to-donor latent variation per family, split by known
  factors, the remainder labelled as including disease.
3 the immune disease axis against the myeloid-lymphoid axis, three ways.
4 raincloud: each donor's held-out score on the immune axis.
No study step anywhere. Disease direction = mean(control donors) -
mean(patient donors) of donor-mean latents (>= 50 cells); plotted as its
negative, so "towards patients" is positive.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fig2_panels import FAM_C, FAMS, CTL_C, CASE_C, INK, SOFT, HAIR, clean  # noqa: E402

ROOT = Path("/Users/atharvawaghmare/Endo research/ELAJ")
ARM, MINC, SEED = "p1_dab168_kl1", 50, 24
OUT = Path(__file__).resolve().parents[1] / "draft"
MM = 1 / 25.4
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 6, "text.color": INK})
STROMAL = ["COL1A1", "COL3A1", "COL6A3", "SFRP4", "DCN", "LUM", "POSTN", "COL1A2"]

Z = np.load(ROOT / f"Outputs/cells/{ARM}/latent.npy")
m = pd.read_csv(ROOT / f"Outputs/cells/{ARM}/metadata.csv.gz", low_memory=False,
                usecols=["study", "patient_id", "disease_status", "cell family", "AnnotationMain",
                         "celltype", "menstrual phase", "total_counts"])
pz = np.load(ROOT / "Outputs/analysis/percell_panel/panel.npz")
_g = [str(x) for x in pz["genes"]]
sscore = np.log1p(1e4 * pz["counts"][:, [_g.index(x) for x in STROMAL]].sum(1) / np.maximum(pz["library"], 1))
lab = np.where(m.study == "marecko_2024", m["celltype"], m["AnnotationMain"]).astype(str)
lin = np.where(np.isin(lab, ["lymphocyte", "Immune_Lymphoid"]), "lymphoid",
               np.where(np.isin(lab, ["myeloid", "Immune_Myeloid"]), "myeloid", ""))
cc = m.disease_status.isin(["control", "eutopic"]).to_numpy()
case = (m.disease_status == "eutopic").to_numpy()
fam = m["cell family"].astype(str).to_numpy()
phase = m["menstrual phase"].astype(str).str.replace(r"_.*", "", regex=True).to_numpy()


def donor_frame(k):
    d = pd.DataFrame(Z[k], columns=[f"z{i}" for i in range(Z.shape[1])])
    d["pid"] = m.patient_id.to_numpy()[k]; d["case"] = case[k]; d["s"] = sscore[k]
    d["lym"] = lin[k] == "lymphoid"; d["lib"] = np.log10(m.total_counts.to_numpy()[k].astype(float))
    d["phase"] = phase[k]
    g = d.groupby("pid")
    out = g[[c for c in d.columns if c.startswith("z")] + ["s", "lym", "lib"]].mean()
    out["case"] = g.case.first(); out["n"] = g.size()
    out["phase"] = g.phase.agg(lambda x: x.mode().iloc[0])
    return out[out.n >= MINC]


def direction(D):
    M = D[[f"z{i}" for i in range(Z.shape[1])]].to_numpy()
    w = M[~D.case.to_numpy()].mean(0) - M[D.case.to_numpy()].mean(0)
    return -w / np.linalg.norm(w)            # towards patients


DON = {f: donor_frame(cc & (fam == f)) for f in FAMS}
W = {f: direction(DON[f]) for f in FAMS}


# ── 1. swing map ──────────────────────────────────────────────────────────
def swing():
    xy = np.load(ROOT / f"Outputs/analysis/umaps/{ARM}/_umap_cache/global_400000.npy")
    idx = np.sort(np.random.default_rng(24).choice(len(m), 400_000, replace=False))
    fig, ax = plt.subplots(figsize=(88 * MM, 80 * MM))
    ax.scatter(xy[:, 0], xy[:, 1], s=.05, color="#DADDE2", lw=0, rasterized=True, zorder=1)
    nb = 26
    ex = np.linspace(xy[:, 0].min(), xy[:, 0].max(), nb + 1)
    ey = np.linspace(xy[:, 1].min(), xy[:, 1].max(), nb + 1)
    tile = min(ex[1] - ex[0], ey[1] - ey[0])
    bx = np.clip(np.digitize(xy[:, 0], ex) - 1, 0, nb - 1)
    by = np.clip(np.digitize(xy[:, 1], ey) - 1, 0, nb - 1)
    famk, cck = fam[idx], cc[idx]
    arrows = []
    for i in range(nb):
        for j in range(nb):
            t = (bx == i) & (by == j) & cck
            if t.sum() < 60:
                continue
            fs, cnt = np.unique(famk[t], return_counts=True)
            ok = np.isin(fs, FAMS)
            if not ok.any():
                continue
            f = fs[ok][cnt[ok].argmax()]
            k = t & (famk == f)
            if k.sum() < 40:
                continue
            s = Z[idx[k]] @ W[f]
            A = np.column_stack([np.ones(k.sum()), xy[k, 0] - xy[k, 0].mean(), xy[k, 1] - xy[k, 1].mean()])
            g = np.linalg.lstsq(A, s, rcond=None)[0][1:]
            arrows.append((ex[i] + tile / 2, ey[j] + tile / 2, g, f))
    mag = np.array([np.linalg.norm(a[2]) for a in arrows])
    scale = .9 * tile / np.percentile(mag, 95)
    for (x, y, g, f), mg in zip(arrows, mag):
        L = min(mg * scale, 1.2 * tile)
        u = g / mg * L
        ax.annotate("", (x + u[0] / 2, y + u[1] / 2), (x - u[0] / 2, y - u[1] / 2),
                    arrowprops=dict(arrowstyle="-|>,head_length=.35,head_width=.18",
                                    color=FAM_C[f], lw=.5 + 1.6 * L / (1.2 * tile)), zorder=3)
    for f in FAMS:
        ax.plot([], [], color=FAM_C[f], lw=1.5, label=f)
    ax.legend(frameon=False, fontsize=5.5, loc="lower left", handlelength=1.2)
    ax.text(0, 1.02, "arrows: the way each family's disease score rises across the map;\n"
            "longer = steeper. Families' own directions, no study step.",
            transform=ax.transAxes, fontsize=5.2, color=SOFT, va="bottom")
    ax.set_xticks([]); ax.set_yticks([]); clean(ax, False, False)
    fig.savefig(OUT / "fig2f_proto1_swing.png", dpi=400, bbox_inches="tight"); plt.close(fig)


# ── 2. stacked bar ────────────────────────────────────────────────────────
def r2(M, X):
    X = np.column_stack([np.ones(len(M)), X])
    R = M - X @ np.linalg.lstsq(X, M, rcond=None)[0]
    return 1 - (R ** 2).sum() / ((M - M.mean(0)) ** 2).sum()


def stacked():
    fig, ax = plt.subplots(figsize=(88 * MM, 50 * MM))
    cols = {"stromal RNA": "#B9C3CE", "menstrual phase": "#8E9BAA",
            "composition or depth": "#5E6B7A", "remaining": "white"}
    for yi, f in enumerate(FAMS[::-1]):
        D = DON[f]; M = D[[f"z{i}" for i in range(Z.shape[1])]].to_numpy()
        ph = pd.get_dummies(D.phase).to_numpy(float)[:, 1:]
        third = np.column_stack([D.lym, D.lib]) if f == "immune" else D.lib.to_numpy()[:, None]
        steps = [D.s.to_numpy()[:, None], ph, third]
        cum, prev, x0 = [], 0.0, 0.0
        X = np.empty((len(M), 0))
        for st in steps:
            X = np.column_stack([X, st]); v = r2(M, X); cum.append(v - prev); prev = v
        cum.append(1 - prev)
        for (lab_, c), v in zip(cols.items(), cum):
            ax.barh(yi, v, left=x0, color=c, ec=INK if lab_ == "remaining" else "white",
                    lw=.4, hatch="////" if lab_ == "remaining" else None, height=.62)
            x0 += v
        dis = r2(M, D.case.to_numpy(float)[:, None])
        ax.plot([dis, dis], [yi - .38, yi + .38], color=CASE_C, lw=1.3)
        ax.text(1.01, yi, f"disease alone {dis:.0%}", va="center", fontsize=5.2, color=CASE_C,
                transform=ax.get_yaxis_transform())
    ax.set_yticks(range(4)); ax.set_yticklabels(FAMS[::-1])
    ax.set_xlim(0, 1); ax.set_xlabel("share of donor-to-donor variation in the latent")
    for lab_, c in cols.items():
        ax.barh([], [], color=c, ec=INK if lab_ == "remaining" else "none", lw=.4,
                hatch="////" if lab_ == "remaining" else None,
                label="not explained by these three\n(includes disease, donor biology)" if lab_ == "remaining" else lab_)
    ax.legend(frameon=False, fontsize=5, ncol=4, loc="lower left", bbox_to_anchor=(0, 1.02),
              handlelength=1.2, columnspacing=.8)
    clean(ax)
    fig.savefig(OUT / "fig2f_proto2_stacked.png", dpi=400, bbox_inches="tight"); plt.close(fig)


# ── 3. the immune disease axis against the myeloid-lymphoid axis ─────────
def plane():
    k = cc & (fam == "immune") & (lin != "")
    Zi = Z[k]; li = lin[k]; ca = case[k]; pid = m.patient_id.to_numpy()[k]
    a = Zi[li == "myeloid"].mean(0) - Zi[li == "lymphoid"].mean(0); a /= np.linalg.norm(a)
    x, y = Zi @ a, Zi @ W["immune"]
    print(f"  cosine(disease axis, myeloid-lymphoid axis) {float(W['immune'] @ a):+.3f}")
    fig, axs = plt.subplots(1, 3, figsize=(180 * MM, 58 * MM))
    # (a) contours, patients vs controls
    ax = axs[0]
    ex = np.linspace(np.percentile(x, .5), np.percentile(x, 99.5), 70)
    ey = np.linspace(np.percentile(y, .5), np.percentile(y, 99.5), 70)
    from scipy.ndimage import gaussian_filter
    for sel, c, nm in ((~ca, CTL_C, "control"), (ca, CASE_C, "patient")):
        H, _, _ = np.histogram2d(x[sel], y[sel], [ex, ey], density=True)
        H = gaussian_filter(H.T, 1.4)
        ax.contour(ex[:-1], ey[:-1], H, levels=np.percentile(H[H > 0], [60, 80, 93, 98]), colors=c, linewidths=.7)
        ax.plot([], [], color=c, label=f"{nm} cells")
    ax.legend(frameon=False, fontsize=5)
    ax.set_xlabel("myeloid  ←→  lymphoid axis (myeloid +)"); ax.set_ylabel("disease axis (patient +)")
    ax.set_title("a  cells", loc="left", fontsize=6.5, fontweight="bold"); clean(ax)
    # (b) hexbin by patient share
    ax = axs[1]
    hb = ax.hexbin(x, y, C=ca.astype(float), reduce_C_function=np.mean, gridsize=36, cmap="RdBu_r",
                   vmin=.2, vmax=.8, mincnt=15, linewidths=0)
    cb = fig.colorbar(hb, ax=ax, fraction=.05, pad=.02); cb.set_label("share of cells from patients", fontsize=5)
    cb.ax.tick_params(labelsize=5)
    ax.set_xlabel("myeloid  ←→  lymphoid axis (myeloid +)")
    ax.set_title("b  patient share", loc="left", fontsize=6.5, fontweight="bold"); clean(ax)
    # (c) donors as dumbbells: lymphoid centroid to myeloid centroid, the donor at its mix
    ax = axs[2]
    d = pd.DataFrame({"pid": pid, "lin": li, "x": x, "y": y, "case": ca})
    for p_, t in d.groupby("pid"):
        if len(t) < MINC or t.lin.nunique() < 2:
            continue
        cl = CASE_C if t.case.iloc[0] else CTL_C
        mu = t.groupby("lin")[["x", "y"]].mean()
        ax.plot(mu.x, mu.y, color=cl, lw=.35, alpha=.45, zorder=1)
        ax.scatter([t.x.mean()], [t.y.mean()], s=9, color=cl, ec="white", lw=.3, zorder=3)
    ax.set_xlabel("myeloid  ←→  lymphoid axis (myeloid +)")
    ax.set_title("c  donors: each line spans its lymphoid and myeloid cells;\n    the dot is the donor, set by its mix",
                 loc="left", fontsize=6, fontweight="bold"); clean(ax)
    fig.tight_layout()
    fig.savefig(OUT / "fig2f_proto3_plane.png", dpi=400, bbox_inches="tight"); plt.close(fig)


# ── 4. raincloud of held-out donor scores ────────────────────────────────
def raincloud():
    fig, axs = plt.subplots(1, 2, figsize=(120 * MM, 55 * MM), sharey=False)
    rng = np.random.default_rng(SEED)
    marks = {"proliferative": "o", "periovulatory": "D", "secretory": "s", "menstrual": "^"}
    for ax, f in zip(axs, ("immune", "stromal")):
        D = DON[f]; M = D[[f"z{i}" for i in range(Z.shape[1])]].to_numpy(); y = D.case.to_numpy()
        tot, n = np.zeros(len(y)), np.zeros(len(y))
        for _ in range(400):
            tr = rng.random(len(y)) < .7
            if len(set(y[tr])) < 2:
                continue
            w = M[tr & ~y].mean(0) - M[tr & y].mean(0); w = -w / np.linalg.norm(w)
            tot[~tr] += M[~tr] @ w; n[~tr] += 1
        sc = tot / np.maximum(n, 1); sc = (sc - sc.mean()) / sc.std()
        for xi, (sel, c, nm) in enumerate(((~y, CTL_C, "control"), (y, CASE_C, "patient"))):
            v = sc[sel]
            vp = ax.violinplot([v], positions=[xi], widths=.7, showextrema=False, vert=True)
            for b in vp["bodies"]:
                b.set_facecolor(c); b.set_alpha(.3); b.set_edgecolor("none")
                pth = b.get_paths()[0]; pth.vertices[:, 0] = np.clip(pth.vertices[:, 0], -1e9, xi)
            for ph, mk in marks.items():
                q = sel & (D.phase.to_numpy() == ph)
                ax.scatter(xi + .08 + rng.uniform(0, .22, q.sum()), sc[q], s=7, marker=mk, color=c,
                           ec="white", lw=.25, zorder=3)
            ax.plot([xi - .3, xi], [np.median(v)] * 2, color=c, lw=1.2)
        u = stats.mannwhitneyu(sc[y], sc[~y]).statistic / (y.sum() * (~y).sum())
        ax.set_xticks([0, 1]); ax.set_xticklabels([f"control\n({(~y).sum()})", f"patient\n({y.sum()})"])
        ax.set_title(f"{f}: held-out score, AUC {u:.2f}", loc="left", fontsize=6.5, fontweight="bold")
        ax.set_ylabel("position on the disease axis\n(averaged over splits held out; SD units)")
        clean(ax)
    for ph, mk in marks.items():
        axs[1].scatter([], [], marker=mk, color=SOFT, s=8, label=ph)
    axs[1].legend(frameon=False, fontsize=5, title="phase", title_fontsize=5, loc="upper left",
                  bbox_to_anchor=(1, 1))
    fig.tight_layout()
    fig.savefig(OUT / "fig2f_proto4_raincloud.png", dpi=400, bbox_inches="tight"); plt.close(fig)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for fn in (swing, stacked, plane, raincloud):
        fn(); print("drew", fn.__name__)
