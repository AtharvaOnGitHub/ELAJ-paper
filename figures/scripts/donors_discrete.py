import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
MM=1/25.4
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":7})
lat=np.load("Outputs/cells/p1_dab168_kl1/latent.npy")
m=pd.read_csv("Outputs/cells/p1_dab168_kl1/metadata.csv.gz", low_memory=False)
n=400_000
idx=np.sort(np.random.default_rng(24).choice(len(lat), n, replace=False))
xy=np.load(f"Outputs/analysis/umaps/p1_dab168_kl1/_umap_cache/global_{n}.npy")
mm=m.iloc[idx].reset_index(drop=True)
sel=mm["CycleDay"].notna().values
sub=mm[sel].reset_index(drop=True); P=xy[sel]

# donors ordered by their single cycle day, each given its own rainbow hue
g=sub.groupby("patient_id")["CycleDay"].first().sort_values()
order=list(g.index); days=g.values
rain=plt.cm.gist_rainbow(np.linspace(0,0.97,len(order)))
cmap_d={d:rain[i] for i,d in enumerate(order)}
print(f"{len(order)} donors, days {days.min():.0f}-{days.max():.0f}")

fig,axes=plt.subplots(1,3, figsize=(260*MM, 92*MM))
plt.subplots_adjust(left=0.004,right=0.93,top=0.92,bottom=0.015,wspace=0.02)

# 1. discrete, one colour per donor, hue ordered by day
ax=axes[0]
ax.scatter(xy[:,0], xy[:,1], c="#F2EFEA", s=0.05, lw=0, rasterized=True)
cols=np.array([cmap_d[p] for p in sub["patient_id"]])
o=np.random.default_rng(1).permutation(len(P))         # no draw-order artefact
ax.scatter(P[o,0], P[o,1], c=cols[o], s=0.30, lw=0, rasterized=True)
ax.set_title("one discrete colour per donor\n(hue ordered by that donor's cycle day)", fontsize=7.5)

# 2. continuous day, same cells
CYC=LinearSegmentedColormap.from_list("c",["#6D2E46","#A24E5E","#D9A441","#ECE2D0",
      "#3A7D5D","#4E7C82","#2F6690","#7A5C8A","#6D2E46"])
ax=axes[1]
ax.scatter(xy[:,0], xy[:,1], c="#F2EFEA", s=0.05, lw=0, rasterized=True)
sc=ax.scatter(P[o,0], P[o,1], c=sub["CycleDay"].values[o], s=0.30, cmap=CYC, lw=0, rasterized=True)
ax.set_title("the same cells, continuous day", fontsize=7.5)

# 3. zoom on the stromal mass, discrete donors
ax=axes[2]
x0,x1 = np.percentile(P[:,0],[55,100]); y0,y1 = np.percentile(P[:,1],[45,100])
k=(P[:,0]>x0)&(P[:,1]>y0)
ax.scatter(xy[:,0], xy[:,1], c="#F2EFEA", s=0.05, lw=0, rasterized=True)
ax.scatter(P[o,0], P[o,1], c=cols[o], s=0.9, lw=0, rasterized=True)
ax.set_xlim(x0,x1); ax.set_ylim(y0,y1)
ax.set_title("zoom: are donors patches, or interleaved?", fontsize=7.5)

for a in axes:
    a.set_xticks([]); a.set_yticks([])
    for s in a.spines.values(): s.set_visible(False)

sm=plt.cm.ScalarMappable(cmap=plt.cm.gist_rainbow,
                         norm=plt.Normalize(days.min(), days.max()))
cb=fig.colorbar(sm, ax=axes, fraction=0.016, pad=0.008, aspect=26)
cb.set_label("donor's cycle day", fontsize=6.5); cb.ax.tick_params(labelsize=6)
fig.savefig("/tmp/claude-501/fig1/donors_discrete.png", dpi=300)

# does a donor own a patch, or share it?
from sklearn.neighbors import NearestNeighbors
S=lat[idx][sel]
q=np.random.default_rng(3).choice(len(S), 15000, replace=False)
_,ind=NearestNeighbors(n_neighbors=31).fit(S).kneighbors(S[q])
dn=sub["patient_id"].values; dy=sub["CycleDay"].values
print(f"distinct donors among 30 neighbours   : {np.median([len(set(dn[r])) for r in ind[:,1:]]):.0f} of 60")
print(f"distinct days   among 30 neighbours   : {np.median([len(set(dy[r])) for r in ind[:,1:]]):.0f}")
print(f"neighbour day within ±3 of own        : {np.mean(np.abs(dy[ind[:,1:]]-dy[q][:,None])<=3):.3f}")
