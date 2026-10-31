import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
MM=1/25.4
INK,SOFT,SPINE="#4A2B35","#8A7078","#D9C8C0"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":7,"text.color":INK})
lat=np.load("Outputs/cells/p1_dab168_kl1/latent.npy")
m=pd.read_csv("Outputs/cells/p1_dab168_kl1/metadata.csv.gz", low_memory=False)
n=400_000
idx=np.sort(np.random.default_rng(24).choice(len(lat), n, replace=False))
xy=np.load(f"Outputs/analysis/umaps/p1_dab168_kl1/_umap_cache/global_{n}.npy")
mm=m.iloc[idx].reset_index(drop=True)

ORDER=["menstrual","proliferative_early","proliferative","proliferative_late",
       "periovulatory","secretory_early","secretory_early_mid","secretory_mid","secretory_late"]
COARSE={"menstrual":"menstrual","proliferative_early":"proliferative",
        "proliferative":"proliferative","proliferative_late":"proliferative",
        "periovulatory":"periovulatory","secretory_early":"secretory early",
        "secretory_early_mid":"secretory early","secretory_mid":"secretory late",
        "secretory_late":"secretory late"}
CORDER=["menstrual","proliferative","periovulatory","secretory early","secretory late"]
CCOL  =["#8C2F39","#D9A441","#3A7D5D","#2F6690","#6D2E46"]

ph=mm["menstrual phase"]
co=ph.map(COARSE)
print("coarse groups:", co.value_counts().reindex(CORDER).to_dict())

fig=plt.figure(figsize=(250*MM, 118*MM))
gs=fig.add_gridspec(2, 5, height_ratios=[1.45,1.0], hspace=0.14, wspace=0.03,
                    left=0.005, right=0.995, top=0.925, bottom=0.01)

# top left: all nine levels, cycle-ordered hues
ax=fig.add_subplot(gs[0,0:2])
ax.scatter(xy[:,0],xy[:,1],c="#F2EFEA",s=0.05,lw=0,rasterized=True)
hues=plt.cm.turbo(np.linspace(0.04,0.96,len(ORDER)))
o=np.random.default_rng(1).permutation(len(xy))
for i,lev in enumerate(ORDER):
    k=(ph==lev).values[o]
    if k.sum()==0: continue
    ax.scatter(xy[o][k,0],xy[o][k,1],c=[hues[i]],s=0.24,lw=0,rasterized=True,
               label=f"{lev.replace('_',' ')}  ({(ph==lev).sum():,})")
lg=ax.legend(loc="lower left",fontsize=5.4,markerscale=10,handletextpad=0.3,
             labelspacing=0.26,borderpad=0.2)
for t in lg.get_texts(): t.set_color(SOFT)
ax.set_title("nine harmonised phases, in cycle order", fontsize=8)

# top right: five coarse groups
ax=fig.add_subplot(gs[0,2:4])
ax.scatter(xy[:,0],xy[:,1],c="#F2EFEA",s=0.05,lw=0,rasterized=True)
for c_,col in zip(CORDER,CCOL):
    k=(co==c_).values[o]
    if k.sum()==0: continue
    ax.scatter(xy[o][k,0],xy[o][k,1],c=col,s=0.26,lw=0,rasterized=True,label=c_)
lg=ax.legend(loc="lower left",fontsize=6,markerscale=10,handletextpad=0.3,
             labelspacing=0.28,borderpad=0.2)
for t in lg.get_texts(): t.set_color(SOFT)
ax.set_title("five groups", fontsize=8)

# top far right: where the labels are at all
ax=fig.add_subplot(gs[0,4])
lab=ph.notna().values
ax.scatter(xy[~lab,0],xy[~lab,1],c="#F2EFEA",s=0.05,lw=0,rasterized=True)
ax.scatter(xy[lab,0],xy[lab,1],c="#8A7078",s=0.12,lw=0,rasterized=True)
ax.set_title(f"labelled at all\n{lab.sum():,} of {len(xy):,}", fontsize=7.5)

# bottom: small multiples, one per coarse group
for j,(c_,col) in enumerate(zip(CORDER,CCOL)):
    ax=fig.add_subplot(gs[1,j])
    k=(co==c_).values
    ax.scatter(xy[:,0],xy[:,1],c="#F2EFEA",s=0.04,lw=0,rasterized=True)
    ax.scatter(xy[k,0],xy[k,1],c=col,s=0.30,lw=0,rasterized=True)
    ax.set_title(f"{c_}   {k.sum():,}", fontsize=6.8, color=col, pad=2)

for ax in fig.axes:
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
fig.savefig("/tmp/claude-501/fig1/phase_groups.png", dpi=300)
print("saved")
