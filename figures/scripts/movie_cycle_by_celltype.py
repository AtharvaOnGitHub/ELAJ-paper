import numpy as np, pandas as pd, matplotlib, time, os
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image
INK,SOFT="#4A2B35","#8A7078"
CYC=LinearSegmentedColormap.from_list("c",["#8C2F39","#C25B3A","#D9A441","#7E9B41",
     "#2E7D5B","#2F7F86","#2F6690","#5C4E9E","#8C2F39"])
plt.rcParams.update({"font.family":"DejaVu Sans","text.color":INK})

lat=np.load("Outputs/cells/p1_dab168_kl1/latent.npy")
m=pd.read_csv("Outputs/cells/p1_dab168_kl1/metadata.csv.gz", low_memory=False)
n=400_000
idx=np.sort(np.random.default_rng(24).choice(len(lat), n, replace=False))
xy=np.load(f"Outputs/analysis/umaps/p1_dab168_kl1/_umap_cache/global_{n}.npy")
mm=m.iloc[idx].reset_index(drop=True)
day=mm["CycleDay"].values.astype(float)
COARSE={"menstrual":None,"proliferative_early":"proliferative","proliferative":"proliferative",
 "proliferative_late":"proliferative","periovulatory":"periovulatory","secretory_early":"secretory early",
 "secretory_early_mid":"secretory early","secretory_mid":"secretory late","secretory_late":"secretory late"}
grp=mm["menstrual phase"].map(COARSE).values
GRP=["proliferative","periovulatory","secretory early","secretory late"]
GCOL=["#D9A441","#2E7D5B","#2F6690","#8C2F39"]
FAM=["stromal","epithelial","immune"]
fam=mm["cell family"].values

days=np.arange(5,31); FPD=2
per_cycle=len(days)*FPD
CYCLES=2
rng=np.random.default_rng(5)

SOLO, FADE = 0.34, 0.60      # |d|<SOLO one phase only; fades out by FADE
def overlap_alpha(pos):
    """Mostly one phase at a time, with a brief two-phase handover at each
    boundary. Never three: FADE < 1 - FADE + 1 keeps non-adjacent groups dark."""
    a=np.zeros(len(GRP))
    for j in range(len(GRP)):
        d=abs((pos-j+len(GRP)/2)%len(GRP)-len(GRP)/2)
        if d<=SOLO:   a[j]=1.0
        elif d<FADE:  a[j]=0.5*(1+np.cos(np.pi*(d-SOLO)/(FADE-SOLO)))
    return a

fig,axes=plt.subplots(len(FAM),2, figsize=(7.6,8.1), dpi=122)
plt.subplots_adjust(left=0.085,right=0.93,top=0.950,bottom=0.012,hspace=0.045,wspace=0.02)
bgsets={}
for r,f_ in enumerate(FAM):
    k=(fam==f_)
    sub=np.where(k)[0]
    bg=rng.choice(sub, min(len(sub),45_000), replace=False)
    bgsets[f_]=(k, bg)
    x0,x1=np.percentile(xy[sub,0],[0.2,99.8]); y0,y1=np.percentile(xy[sub,1],[0.2,99.8])
    px,py=(x1-x0)*0.06,(y1-y0)*0.06
    for c in (0,1):
        ax=axes[r,c]
        ax.scatter(xy[bg,0],xy[bg,1],c="#F2EFEA",s=1.1,lw=0,rasterized=True,zorder=0)
        ax.set_xlim(x0-px,x1+px); ax.set_ylim(y0-py,y1+py)
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values(): s.set_visible(False)
    axes[r,0].set_ylabel(f_, fontsize=10.5, color=INK, labelpad=7)
    axes[r,0].text(-0.055,0.5,f"{k.sum():,} cells",transform=axes[r,0].transAxes,
                   rotation=90,va="center",ha="center",fontsize=6.4,color=SOFT)
axes[0,0].set_title("day of the menstrual cycle", fontsize=11, pad=8)
axes[0,1].set_title("harmonised phase group", fontsize=11, pad=8)
cap=fig.text(0.30,0.978,"",ha="center",fontsize=12,color=INK)
cap2=fig.text(0.70,0.978,"",ha="center",fontsize=11)
sm=plt.cm.ScalarMappable(cmap=CYC, norm=plt.Normalize(5,30))
cax=fig.add_axes([0.952,0.28,0.012,0.44])
cb=fig.colorbar(sm, cax=cax)
cb.set_label("day", fontsize=8, color=SOFT); cb.ax.tick_params(labelsize=7)

frames=[]; t0=time.time()
for fi in range(per_cycle):
    d=days[fi//FPD]
    arts=[]
    pos=(fi/per_cycle)*len(GRP)
    al=overlap_alpha(pos)
    for r,f_ in enumerate(FAM):
        k,_=bgsets[f_]
        for off,(sz,a_) in zip((-1,0,1),((1.4,0.25),(3.0,0.95),(1.4,0.25))):
            sel=k&(day==(d+off))
            if sel.sum():
                arts.append(axes[r,0].scatter(xy[sel,0],xy[sel,1],c=[CYC((d+off-5)/25)],
                            s=sz,lw=0,alpha=a_,rasterized=True,zorder=3))
        for j,(g_,gc) in enumerate(zip(GRP,GCOL)):
            if al[j]<0.03: continue
            sel=k&(grp==g_)
            if sel.sum():
                arts.append(axes[r,1].scatter(xy[sel,0],xy[sel,1],c=gc,s=2.6,lw=0,
                            alpha=0.92*al[j],rasterized=True,zorder=3))
    cap.set_text(f"day {d}")
    lead=int(np.argmax(al))
    cap2.set_text(GRP[lead]); cap2.set_color(GCOL[lead])
    fig.canvas.draw()
    frames.append(Image.fromarray(np.asarray(fig.canvas.buffer_rgba())[:,:,:3].copy()))
    for a_ in arts: a_.remove()
    if fi%10==0: print(f"  {fi}/{per_cycle}  {time.time()-t0:.0f}s", flush=True)

out="/tmp/claude-501/fig1/cycle_by_celltype.gif"
pal=frames[0].quantize(colors=128, method=Image.MEDIANCUT)
seq=[f.quantize(palette=pal, dither=Image.NONE) for f in frames]*CYCLES
seq[0].save(out, save_all=True, append_images=seq[1:], duration=150, loop=0, optimize=True)
print(f"{len(seq)} frames ({CYCLES} cycles), {time.time()-t0:.0f}s, {os.path.getsize(out)/1e6:.1f} MB")
