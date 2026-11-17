"""Figure 2f on its own, tall and narrow (AW, 17 Nov: "this figure would look
more impressive if it is less wide ... the difference between the chance line
and our model would look more significant in a taller diagram").

    /Users/atharvawaghmare/miniconda3/envs/elaj/bin/python figures/scripts/figure2f_tall.py

88 mm, NMI's single column. Drawn by fig2_panels.i6, the same function the
assembled draft uses, so the two cannot disagree. Writes to figures/draft/.
"""
import os, sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fig2_panels as P

W, H = 88.0, 120.0
fig = plt.figure(figsize=(W / 25.4, H / 25.4))
P.i6(fig, [30 / W, 10 / H, 55 / W, 100 / H])
fig.text(2 / W, 114 / H, "f", fontsize=P.FS_LETTER, fontweight="bold", va="baseline", color=P.INK)
fig.text(7 / W, 114 / H, "Genes the corpus's papers report, on our ranking",
         fontsize=P.FS_TITLE, va="baseline", color=P.INK)
dest = Path(__file__).resolve().parents[1] / "draft" / "figure2f_tall.png"
fig.savefig(dest, dpi=int(os.environ.get("FIGDPI", 300)), facecolor="white")
print("wrote", dest)
