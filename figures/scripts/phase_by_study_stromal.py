import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
MM=1/25.4
INK,SOFT="#4A2B35","#8A7078"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":7,"text.color":INK})
lat=np.load("Outputs/cells/p1_dab168_kl1/latent.npy")
m=pd.read_csv("Outputs/cells/p1_dab168_kl1/metadata.csv.gz", low_memory=False)
n=400_000
idx=np.sort(np.random.default_rng(24).choice(len(lat), n, replace=False))
xy=np.load(f"Outputs/analysis/umaps/p1_dab168_kl1/_umap_cache/global_{n}.npy")
mm=m.iloc[idx].reset_index(drop=True)
COARSE={"menstrual":"menstrual","proliferative_early":"proliferative","proliferative":"proliferative",
 "proliferative_late":"proliferative","periovulatory":"periovulatory","secretory_early":"secretory early",
 "secretory_early_mid":"secretory early","secretory_mid":"secretory late","secretory_late":"secretory late"}
mm["grp"]=mm["menstrual phase"].map(COARSE)
GRP=["proliferative","periovulatory","secretory early","secretory late"]
COL=["#D9A441","#3A7D5D","#2F6690","#6D2E46"]

strom=(mm["cell family"]=="stromal").values
S=xy[strom]; g=mm.loc[strom,"grp"]; st=mm.loc[strom,"study"]
print("stromal cells in sample:", strom.sum(), "| with a phase:", g.notna().sum())

fig=plt.figure(figsize=(240*MM, 112*MM))
gs=fig.add_gridspec(2,4, height_ratios=[1.0,1.0], hspace=0.20, wspace=0.03,
                    left=0.005,right=0.995,top=0.90,bottom=0.01)
for j,(grp,col) in enumerate(zip(GRP,COL)):
    k=(g==grp).values
    ns=st[k].nunique(); nd=mm.loc[strom,"patient_id"][k].nunique()
    # row 0: all stromal cells of this phase
    ax=fig.add_subplot(gs[0,j])
    ax.scatter(S[:,0],S[:,1],c="#F2EFEA",s=0.05,lw=0,rasterized=True)
    ax.scatter(S[k,0],S[k,1],c=col,s=0.33,lw=0,rasterized=True)
    ax.set_title(f"{grp}\n{k.sum():,} stromal · {ns} stud{'y' if ns==1 else 'ies'} · {nd} donors",
                 fontsize=7, color=col, pad=3)
    if ns==1:
        ax.text(0.5,0.015,"SINGLE STUDY — region is confounded", transform=ax.transAxes,
                ha="center", fontsize=6.0, color="#8C2F39", fontweight="bold")
    # row 1: the same, split by the contributing studies
    ax=fig.add_subplot(gs[1,j])
    ax.scatter(S[:,0],S[:,1],c="#F2EFEA",s=0.05,lw=0,rasterized=True)
    studies=st[k].value_counts().index.tolist()
    shades=plt.cm.copper(np.linspace(0.18,0.80,max(len(studies),1)))
    for i,s_ in enumerate(studies):
        kk=k & (st==s_).values
        ax.scatter(S[kk,0],S[kk,1],c=[shades[i]],s=0.33,lw=0,rasterized=True,
                   label=f"{s_.replace('_',' ')} ({kk.sum():,})")
    lg=ax.legend(loc="lower left",fontsize=5.0,markerscale=9,handletextpad=0.28,
                 labelspacing=0.2,borderpad=0.15)
    for t in lg.get_texts(): t.set_color(SOFT)
for ax in fig.axes:
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
fig.text(0.004,0.962,"stromal cells only — the cell-type confound removed",
         fontsize=8, color=INK)
fig.text(0.004,0.465,"the same cells, coloured by contributing study",
         fontsize=7.4, color=SOFT)
fig.savefig("/tmp/claude-501/fig1/phase_stromal.png", dpi=300)
print("saved")
