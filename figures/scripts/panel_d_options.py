import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
INK, SOFT, GRID, SPINE = "#4A2B35", "#8A7078", "#EDE4DC", "#D9C8C0"
BERRY, ROSE, CREAM, MUTED = "#6D2E46", "#A26769", "#ECE2D0", "#B3A29C"
BLUE, GREEN, OCHRE = "#2F6690", "#3A7D5D", "#D9A441"
MM=1/25.4
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":6.2,"axes.edgecolor":SPINE,
 "axes.labelcolor":INK,"text.color":INK,"xtick.color":SOFT,"ytick.color":SOFT,
 "axes.linewidth":0.5,"xtick.major.width":0.5,"ytick.major.width":0.5,"legend.frameon":False})
m=pd.read_csv("Outputs/cells/p1_dab168_kl1/metadata.csv.gz", low_memory=False)

fig,axes=plt.subplots(1,3, figsize=(180*MM, 52*MM))
plt.subplots_adjust(left=0.075,right=0.985,top=0.80,bottom=0.20,wspace=0.42)

# ── option 1: the corpus ───────────────────────────────────────────────
ax=axes[0]
t=(m.groupby("study").agg(cells=("study","size"), donors=("patient_id","nunique"))
     .sort_values("cells"))
y=np.arange(len(t))
ax.barh(y, t.cells/1000, color=BERRY, alpha=0.85, height=0.68)
ax.set_yticks(y); ax.set_yticklabels([s.replace("_"," ") for s in t.index], fontsize=4.6)
for i,(c,d) in enumerate(zip(t.cells, t.donors)):
    ax.text(c/1000+8, i, f"{d}", va="center", fontsize=4.4, color=SOFT)
ax.text(1.0, 1.10, "donors", transform=ax.transAxes, ha="right", fontsize=4.5,
        color=SOFT, style="italic")
ax.set_xlabel("cells (thousands)", fontsize=5.6)
ax.set_title("1  the corpus", fontsize=6.4, color=INK, pad=5)
ax.grid(axis="x", alpha=0.6, lw=0.35, color=GRID); ax.set_axisbelow(True)
for s in ("top","right","left"): ax.spines[s].set_visible(False)
ax.tick_params(left=False)

# ── option 2: the confound, measured ───────────────────────────────────
ax=axes[1]
d=m.dropna(subset=["CycleDay"])
g=d.groupby("patient_id")["CycleDay"].agg(["min","max","size"]).sort_values("min")
x=np.arange(len(g))
ax.vlines(x, 0, g["size"]/g["size"].max()*0, color=SPINE, lw=0)
sc=ax.scatter(x, g["min"], s=np.clip(g["size"]/90, 4, 34), c=g["min"],
              cmap="twilight_shifted", lw=0.25, ec="white", zorder=3)
for xi, (lo,hi) in enumerate(zip(g["min"], g["max"])):
    ax.plot([xi,xi],[lo,hi], c=BERRY, lw=0.8, zorder=2)
ax.set_xlabel("donor  (ordered by cycle day)", fontsize=5.6)
ax.set_ylabel("cycle day", fontsize=5.6)
ax.set_title("2  one donor, one day", fontsize=6.4, color=INK, pad=5)
ax.text(0.03, 0.93, "60 of 60 donors contribute\nexactly one cycle day",
        transform=ax.transAxes, fontsize=4.9, color=BERRY, va="top")
ax.grid(alpha=0.6, lw=0.35, color=GRID); ax.set_axisbelow(True)
for s in ("top","right"): ax.spines[s].set_visible(False)

# ── option 3: cycle displacement by cell type ──────────────────────────
ax=axes[2]
fams=["stromal","epithelial","endothelial","immune"]
disp=[1.07, 0.98, 0.39, 0.34]
cols=[BERRY, BLUE, GREEN, OCHRE]
y=np.arange(len(fams))[::-1]
ax.barh(y, disp, color=cols, alpha=0.88, height=0.6)
for yi,v in zip(y,disp):
    ax.text(v+0.035, yi, f"{v:.2f}", va="center", fontsize=5.2, color=INK)
ax.axvline(1.0, ls=(0,(2,2)), lw=0.6, c=SOFT, zorder=1)
ax.text(1.0, len(fams)-0.35, " one cloud width", fontsize=4.5, color=SOFT, va="bottom")
ax.set_yticks(y); ax.set_yticklabels(fams, fontsize=5.2)
ax.set_xlabel("cycle displacement  (in units of the\ncell type's own scatter)", fontsize=5.4)
ax.set_xlim(0, 1.33)
ax.set_title("3  the cycle moves what it should", fontsize=6.4, color=INK, pad=5)
ax.grid(axis="x", alpha=0.6, lw=0.35, color=GRID); ax.set_axisbelow(True)
for s in ("top","right","left"): ax.spines[s].set_visible(False)
ax.tick_params(left=False)

fig.savefig("/tmp/claude-501/fig1/panel_d_options.png", dpi=340)
print("saved")
