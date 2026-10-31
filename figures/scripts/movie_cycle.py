import numpy as np, pandas as pd, matplotlib, time
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, to_rgba
from PIL import Image

INK,SOFT="#4A2B35","#8A7078"
CYC=LinearSegmentedColormap.from_list("c",["#8C2F39","#C25B3A","#D9A441","#7E9B४1".replace("४","4"),
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
GCOL=["#D9A441","#3A7D5D","#2F6690","#6D2E46"]

bg = np.random.default_rng(5).choice(n, 150_000, replace=False)   # lighter grey layer
days = np.arange(5, 31)
FPD  = 3                                   # frames per day
frames_total = len(days)*FPD
per_grp = frames_total/len(GRP)

fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.9), dpi=105)
plt.subplots_adjust(left=0.004, right=0.996, top=0.90, bottom=0.055, wspace=0.015)
for ax in axes:
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    ax.scatter(xy[bg,0], xy[bg,1], c="#F2EFEA", s=0.5, lw=0, rasterized=True, zorder=0)
    ax.set_xlim(xy[:,0].min()-1, xy[:,0].max()+1)
    ax.set_ylim(xy[:,1].min()-1, xy[:,1].max()+1)
axes[0].set_title("day of the menstrual cycle", fontsize=11, pad=7)
axes[1].set_title("harmonised phase group", fontsize=11, pad=7)
cap0=axes[0].text(0.5,-0.035,"",transform=axes[0].transAxes,ha="center",fontsize=9.5,color=INK)
cap1=axes[1].text(0.5,-0.035,"",transform=axes[1].transAxes,ha="center",fontsize=9.5,color=INK)
sm=plt.cm.ScalarMappable(cmap=CYC, norm=plt.Normalize(5,30))
cb=fig.colorbar(sm, ax=axes[0], fraction=0.030, pad=0.004, aspect=22)
cb.set_label("day", fontsize=8, color=SOFT); cb.ax.tick_params(labelsize=7)

frames=[]; t0=time.time()
for fi in range(frames_total):
    d = days[fi//FPD]
    arts=[]
    # left: a 3-day window, centre bright
    for off, (sz, al) in zip((-1,0,1), ((1.1,0.22),(2.4,0.95),(1.1,0.22))):
        k = day==(d+off)
        if k.sum():
            arts.append(axes[0].scatter(xy[k,0], xy[k,1], c=[CYC((d+off-5)/25)],
                        s=sz, lw=0, alpha=al, rasterized=True, zorder=3))
    cap0.set_text(f"day {d}")
    # right: slow crossfade between phase groups
    pos = fi/per_grp
    al=np.zeros(len(GRP)); SOLO,FADE=0.34,0.60
    for j in range(len(GRP)):
        dd=abs((pos-j+len(GRP)/2)%len(GRP)-len(GRP)/2)
        if dd<=SOLO:  al[j]=1.0
        elif dd<FADE: al[j]=0.5*(1+np.cos(np.pi*(dd-SOLO)/(FADE-SOLO)))
    gi=int(np.argmax(al)); fade=al[gi]
    for j,(gname,gc) in enumerate(zip(GRP,GCOL)):
        a = al[j]
        if a < 0.03: continue
        k = grp==gname
        arts.append(axes[1].scatter(xy[k,0], xy[k,1], c=gc, s=2.0, lw=0,
                    alpha=0.92*a, rasterized=True, zorder=3))
    cap1.set_text(GRP[gi])
    cap1.set_color(GCOL[gi]); cap1.set_alpha(1.0)
    fig.canvas.draw()
    buf=np.asarray(fig.canvas.buffer_rgba())[:, :, :3]
    frames.append(Image.fromarray(buf.copy()))
    for a_ in arts: a_.remove()
    if fi % 20 == 0: print(f"  frame {fi}/{frames_total}  {time.time()-t0:.0f}s", flush=True)

out="/tmp/claude-501/fig1/cycle.gif"
pal=frames[0].quantize(colors=128, method=Image.MEDIANCUT)
seq=[f.quantize(palette=pal, dither=Image.NONE) for f in frames]*2
seq[0].save(out, save_all=True, append_images=seq[1:], duration=130, loop=0, optimize=True)
import os
print(f"{len(seq)} frames, {time.time()-t0:.0f}s, {os.path.getsize(out)/1e6:.1f} MB -> {out}")
