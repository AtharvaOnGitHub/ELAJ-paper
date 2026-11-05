import numpy as np, pandas as pd, glob, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.gridspec import GridSpec

# berry as the signature, with blues, greens and ochre for range
INK, SOFT, GRID, SPINE = "#4A2B35", "#8A7078", "#EDE4DC", "#D9C8C0"
BERRY, ROSE, CREAM, MUTED = "#6D2E46", "#A26769", "#ECE2D0", "#B3A29C"
BLUE, GREEN, OCHRE, TEAL = "#2F6690", "#3A7D5D", "#D9A441", "#4E7C82"
CAT   = (BERRY, BLUE, OCHRE, GREEN, ROSE, TEAL, "#7A5C8A", "#B87D6A")
STUDY = ("#6D2E46","#A24E5E","#A26769","#B87D6A","#D9A441","#A98C63",
         "#8A9463","#3A7D5D","#4E7C82","#2F6690","#5C6B99","#7A5C8A")
CYCLIC = LinearSegmentedColormap.from_list("cyc", [
    "#6D2E46","#A24E5E","#D9A441","#ECE2D0","#3A7D5D","#4E7C82","#2F6690","#7A5C8A","#6D2E46"])
MM = 1/25.4
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":6.2,
    "axes.edgecolor":SPINE,"axes.labelcolor":INK,"text.color":INK,
    "xtick.color":SOFT,"ytick.color":SOFT,"axes.linewidth":0.5,
    "xtick.major.width":0.5,"ytick.major.width":0.5,"legend.frameon":False})

R = "/Users/atharvawaghmare/Endo research/ELAJ"
lat = np.load(f"{R}/Outputs/cells/p1_dab168_kl1/latent.npy")
meta = pd.read_csv(f"{R}/Outputs/cells/p1_dab168_kl1/metadata.csv.gz", low_memory=False)
n = min(400_000, len(lat))
idx = np.sort(np.random.default_rng(24).choice(len(lat), n, replace=False))
xy = np.load(f"{R}/Outputs/analysis/umaps/p1_dab168_kl1/_umap_cache/global_{n}.npy")
m = meta.iloc[idx].reset_index(drop=True)

def coords(path, method="elaj"):
    b = pd.read_csv(path); b["mm"]=b.method.astype(str).str.replace("__.*","",regex=True)
    e = b[b.mm==method]
    def g(t,l):
        s=e[(e.test==t)&(e.label==l)]["value"]
        return float(s.iloc[0]) if len(s) else np.nan
    return dict(donor=g("knn-agreement","patient_id"), mixing=g("study-mixing","all studies"),
                phase=g("cross-donor","menstrual phase"), family=g("cross-donor","cell family"),
                disease=g("disease-xdonor","all studies (pooled)"))
ARMS = {a.rsplit("/",2)[1]: coords(a) for a in sorted(glob.glob(f"{R}/Outputs/Benchmarks/p1_*/benchmark.csv"))
        if not a.rsplit("/",2)[1].endswith("_train")}
BASE = {}
for f in glob.glob(f"{R}/Outputs/Benchmarks/*/benchmark.csv"):
    b = pd.read_csv(f); b["mm"]=b.method.astype(str).str.replace("__.*","",regex=True)
    for meth in b.mm.unique():
        if meth=="elaj": continue
        c = coords(f, meth)
        if not np.isnan(c["phase"]): BASE.setdefault(meth, c)
REP = ARMS["p1_dab168_kl1"]

def declutter(ax, items, dy=5.2, iters=90):
    """Nudge labels apart in display space. items = [(x, y, text_artist)]."""
    fig.canvas.draw()
    arts=[t for *_ ,t in items]
    for _ in range(iters):
        bbs=[a.get_window_extent() for a in arts]
        moved=False
        for i in range(len(arts)):
            for j in range(i+1, len(arts)):
                if bbs[i].overlaps(bbs[j]):
                    up, dn = (i, j) if bbs[i].y0 > bbs[j].y0 else (j, i)
                    for k, s in ((up, +1), (dn, -1)):
                        ox, oy = arts[k].get_position()
                        arts[k].set_position((ox, oy))
                        arts[k].set_y(arts[k].get_position()[1])
                    xo, yo = arts[up].get_offset() if hasattr(arts[up],"get_offset") else (0,0)
                    arts[up].set_position(arts[up].get_position())
                    moved=True
        if not moved: break
        fig.canvas.draw()

fig = plt.figure(figsize=(180*MM, 170*MM))
gs = GridSpec(3, 6, figure=fig, height_ratios=[0.68, 1.02, 1.06],
              hspace=0.44, wspace=0.80,
              left=0.070, right=0.986, top=0.975, bottom=0.058)
def tag(ax, l, dx=-0.16, dy=1.12):
    ax.text(dx, dy, l, transform=ax.transAxes, fontsize=9, fontweight="bold",
            va="top", ha="left", color=INK)

# ══ a: the pipeline, every stage named ═════════════════════════════════
ax = fig.add_subplot(gs[0, :]); ax.set_axis_off()
ax.set_xlim(0, 96.6); ax.set_ylim(0, 27)
def box(x,y,w,h,label,sub="",fc="#FBF6EF",ec=SPINE,fs=5.5,lw=0.65,tc=None):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.28,rounding_size=0.6",
                                fc=fc,ec=ec,lw=lw,zorder=3))
    ax.text(x+w/2, y+h/2+(0.9 if sub else 0), label, ha="center", va="center",
            fontsize=fs, color=tc or INK, zorder=4)
    if sub: ax.text(x+w/2, y+h/2-1.4, sub, ha="center", va="center",
                    fontsize=4.5, color=SOFT, zorder=4)
def line(a,b,c_,d,col=SPINE,lw=0.5):
    ax.plot([a,c_],[b,d], c=col, lw=lw, zorder=1, solid_capstyle="round")

MID = 13.5
box(0.0,  MID-3.6, 9.6, 7.2, "15,496\ngenes", "counts")
line(9.6, MID, 11.0, MID)
box(11.0, MID-3.6, 10.0, 7.2, "gene tokens", "identity + count\n+ sentinel", fs=5.3)
line(21.0, MID, 22.4, MID)
box(22.4, MID-3.6, 8.6, 7.2, "DSBN", "per-study\nnormalisation", fs=5.3)
gy = np.linspace(1.6, 25.4, 5)
for y in gy: line(31.0, MID, 33.0, y)
for i, y in enumerate(gy):
    box(33.0, y-1.5, 12.4, 3.0, ["group 1","group 2","⋮","group 43","group 44"][i],
        fs=5.0 if i != 2 else 7.0)
    line(45.4, y, 47.4, MID)
ax.text(39.2, 26.4, "44 group attention layers", ha="center", fontsize=5.0,
        color=SOFT, style="italic")
box(47.4, MID-3.6, 10.0, 7.2, "group readout", "CLS + 8 pooled\nstatistics", fs=5.3)
line(57.4, MID, 58.8, MID)
box(58.8, MID-3.6, 9.6, 7.2, "cell attention", "across groups", fs=5.3)
line(68.4, MID, 69.8, MID)
box(69.8, MID-3.6, 8.4, 7.2, "16", "latent", fs=7.0)
hy = np.linspace(2.0, 25.0, 4)
heads=[("reconstruction","15,496 counts",SPINE),("phase head","keeps the cycle",BERRY),
       ("adversary","removes study",BLUE),("similarity","resists collapse",SPINE)]
for (lab,sub,ec), y in zip(heads, hy):
    line(78.2, MID, 79.8, y, col=ec if ec!=SPINE else SPINE, lw=0.75)
    box(79.8, y-2.4, 16.4, 4.8, lab, sub, ec=ec, lw=1.0 if ec!=SPINE else 0.65,
        fc=CREAM if ec==BERRY else ("#E8EFF4" if ec==BLUE else "#FBF6EF"), fs=5.3)
tag(ax, "a", dx=-0.028, dy=1.14)

# ══ b, c: frontiers ════════════════════════════════════════════════════
def front(pts):
    out=[]; best=-np.inf
    for x,y in sorted(pts):
        if y > best: out.append((x,y)); best=y
    return out
def frontier(gpos, key, xlabel, letter):
    ax = fig.add_subplot(gs[gpos])
    pts=[]
    for nm,c in BASE.items():
        if np.isnan(c[key]): continue
        ax.scatter(c[key], c["phase"], s=15, c=MUTED, ec="white", lw=0.4, zorder=3)
        pts.append((c[key], c["phase"], nm))
    # simple vertical declutter: sort by y, push apart in data units
    pts.sort(key=lambda t: t[1])
    span = 0.80-0.345; minsep = span*0.047; last=-9
    for x,y,nm in pts:
        yy = max(y, last+minsep); last = yy
        ax.annotate(nm, (x, y), xytext=(x+ (0.012*(1 if True else 1)), yy),
                    textcoords="data", fontsize=4.3, color=SOFT, va="center",
                    arrowprops=dict(arrowstyle="-", lw=0.3, color=SPINE,
                                    shrinkA=0.5, shrinkB=1.5) if abs(yy-y)>1e-3 else None)
    bf=front([(p[0],p[1]) for p in pts])
    if len(bf)>1: ax.plot(*zip(*bf), lw=0.8, ls=(0,(3,2)), c=MUTED, zorder=2)
    ap=[(c[key], c["phase"]) for c in ARMS.values() if not np.isnan(c[key])]
    ax.plot(*zip(*front(ap)), lw=1.6, c=BERRY, zorder=4, solid_capstyle="round")
    ax.scatter(*zip(*ap), s=20, c=BERRY, ec="white", lw=0.5, zorder=5)
    ax.scatter([REP[key]],[REP["phase"]], s=95, marker="*", c=BERRY, ec="white", lw=0.7, zorder=6)
    ax.annotate("ELAJ", (REP[key], REP["phase"]), textcoords="offset points",
                xytext=(0,7), fontsize=5.6, color=BERRY, fontweight="bold", ha="center")
    ax.axhline(0.370, ls=(0,(2,2)), lw=0.55, c=SPINE, zorder=1)
    ax.text(0.98, 0.374, "chance", fontsize=4.5, color=SOFT, ha="right",
            transform=ax.get_yaxis_transform())
    xs=[p[0] for p in pts]+[p[0] for p in ap]; pad=(max(xs)-min(xs))*0.34
    ax.set_xlim(min(xs)-pad*0.16, max(xs)+pad); ax.set_ylim(0.345, 0.80)
    ax.set_xlabel(xlabel, fontsize=5.9); ax.set_ylabel("cross-donor cycle phase", fontsize=5.9)
    ax.grid(alpha=0.55, lw=0.35, color=GRID); ax.set_axisbelow(True)
    for s in ("top","right"): ax.spines[s].set_visible(False)
    tag(ax, letter)
frontier((1, slice(0,2)), "donor",  "donor recovery  ↓", "b")
frontier((1, slice(2,4)), "mixing", "study mixing  ↓",   "c")

# ══ d: the spider ══════════════════════════════════════════════════════
ax = fig.add_subplot(gs[1, 4:6], projection="polar")
ax.set_position(ax.get_position().shrunk(0.84, 0.84).translated(0.012, 0.004))
AX = [("cell type","family",False), ("cycle phase","phase",False),
      ("disease","disease",False), ("donor\nblindness","donor",True),
      ("study\nmixing","mixing",True)]
ang = np.linspace(0, 2*np.pi, len(AX), endpoint=False)
def vec(c):
    out=[]
    for _,k,inv in AX:
        v=c.get(k, np.nan)
        v=0.0 if np.isnan(v) else v
        out.append(1.0-v if inv else max(v,0.0))
    return out
series=[("ELAJ", REP, BERRY, 1.9, 1.0),
        ("scVI", BASE.get("scvi"), BLUE, 0.9, 0.85),
        ("scANVI", BASE.get("scanvi"), GREEN, 0.9, 0.85),
        ("PCA", BASE.get("pca"), OCHRE, 0.9, 0.85),
        ("scGPT", BASE.get("scgpt"), MUTED, 0.9, 0.85)]
for nm, c, col, lw, al in series:
    if c is None: continue
    v = vec(c); v = v+[v[0]]
    ax.plot(np.r_[ang, ang[0]], v, lw=lw, c=col, alpha=al, zorder=4 if nm=="ELAJ" else 3,
            label=nm, solid_joinstyle="round")
    if nm=="ELAJ": ax.fill(np.r_[ang, ang[0]], v, c=col, alpha=0.12, zorder=2)
ax.set_xticks(ang); ax.set_xticklabels([a[0] for a in AX], fontsize=5.0, color=INK)
ax.set_ylim(0,1); ax.set_yticks([0.25,0.5,0.75,1.0])
ax.set_yticklabels(["","0.5","","1.0"], fontsize=4.4, color=SOFT)
ax.tick_params(axis="x", pad=-3.0)
ax.grid(color=GRID, lw=0.45); ax.spines["polar"].set_color(SPINE)
ax.spines["polar"].set_linewidth(0.5); ax.set_facecolor("white")
lg=ax.legend(loc="center", bbox_to_anchor=(0.5,-0.265), ncol=5, fontsize=4.8,
             handlelength=1.0, columnspacing=0.8, handletextpad=0.35)
for t in lg.get_texts(): t.set_color(SOFT)
ax.text(0.5, 1.185, "all axes higher is better", transform=ax.transAxes,
        ha="center", fontsize=4.7, color=SOFT, style="italic")
tag(ax, "d", dx=-0.19, dy=1.18)

# ══ e, f, g: UMAPs ═════════════════════════════════════════════════════
def umap(gpos, col, letter, title, cols=None, cont=False, legend=True):
    ax = fig.add_subplot(gs[gpos]); v = m[col]
    if cont:
        ok=v.notna().values
        ax.scatter(xy[~ok,0], xy[~ok,1], c="#F3EDE6", s=0.05, lw=0, rasterized=True, zorder=0)
        sc=ax.scatter(xy[ok,0], xy[ok,1], c=v[ok].astype(float), s=0.26, cmap=CYCLIC,
                      lw=0, rasterized=True, zorder=1)
        cb=fig.colorbar(sc, ax=ax, fraction=0.030, pad=0.004, aspect=12, shrink=0.60)
        lo,hi=float(v.min()),float(v.max())
        cb.set_ticks([lo,hi]); cb.set_ticklabels([f"{lo:.0f}",f"{hi:.0f}"])
        cb.ax.tick_params(labelsize=4.5, width=0.35, length=1.6, color=SPINE, pad=1.2)
        cb.outline.set_linewidth(0.35); cb.outline.set_edgecolor(SPINE)
        cb.set_label("day", fontsize=4.8, labelpad=1.2, color=SOFT)
    else:
        for i,lev in enumerate(v.value_counts().index):
            k=(v==lev).values
            ax.scatter(xy[k,0], xy[k,1], c=cols[i%len(cols)], s=0.09, lw=0,
                       rasterized=True, label=str(lev))
        if legend:
            lg=ax.legend(loc="lower left", bbox_to_anchor=(-0.03,-0.03), fontsize=4.4,
                         markerscale=16, handletextpad=0.2, borderpad=0.12, labelspacing=0.16)
            for t in lg.get_texts(): t.set_color(SOFT)
    ax.set_title(title, fontsize=6.1, color=INK, pad=2.0)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    tag(ax, letter, dx=-0.05, dy=1.09)
umap((2, slice(0,2)), "cell family", "e", "cell type", cols=CAT)
umap((2, slice(2,4)), "study", "f", "study of origin  (11 studies)", cols=STUDY, legend=False)
umap((2, slice(4,6)), "CycleDay", "g", "day of the menstrual cycle", cont=True)

import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "pinned")
os.makedirs(OUT, exist_ok=True)
fig.savefig(os.path.join(OUT, "figure1.png"), dpi=340)
print("wrote figures/pinned/figure1.png")
print("saved")
