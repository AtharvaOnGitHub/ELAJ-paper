"""Figure 4 — this is what endometriosis looks like, in nine UMAPs.

RESTRUCTURED 17 NOVEMBER, AW: "Remove 4a. Move b-f up by one. New 4f would
be the phase axis UMAP from C1." Cell family left (Figure 1d already shows
it) and the X16 cycle axis came in at f, beside cycle day and progesterone,
so the three continuous readings of the cycle sit in one row: two the clinic
measured, one the latent holds. The axis is fitted OFF duempelmann by
supp_figures._cycle_setup, imported so the panel and the X16 numbers come
from the same discriminant.

    /Users/atharvawaghmare/miniconda3/envs/elaj/bin/python figures/scripts/figure4.py

ONE embedding, nine colourings. Nothing moves between panels except colour,
which is what makes a grid of UMAPs legible: a reader compares structure, not
layout. They see in one pass which labels organise the latent and which do
not, and that is the whole "what does the latent hold" question at once.

Neutral grid, alphabetical. Grouping the panels into "labels that structure
it" and "labels that do not" would read better and would state the conclusion
through layout, which is the thing a figure must not do.

REPRODUCIBILITY. The subsample is default_rng(24).choice(n, 400_000) then
sorted, and the cache is keyed on sample size alone, so changing the seed or
the count silently invalidates it.
SUBMISSION RESOLUTION. 200 dpi is for reading on screen while the
design is settled. For the manuscript set FIGDPI=600 or higher:
AW does not want blurred or messy images, and a rasterised scatter
of 400,000 points at 200 dpi will not survive print.
"""
from __future__ import annotations
import os
import sys
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT = Path("/Users/atharvawaghmare/Endo research/ELAJ")
ARM = "p1_dab168_kl1"
OUT = Path(__file__).resolve().parents[1] / "pinned"
MM = 1 / 25.4
INK, SOFT = "#1a1a1a", "#6b6b6b"
plt.rcParams.update({"pdf.fonttype": 42, "ps.fonttype": 42,   # NMI: Arial, editable text
                     "font.family": "Arial", "font.size": 6.5,
                     "text.color": INK})

xy = np.load(ROOT / f"Outputs/analysis/umaps/{ARM}/_umap_cache/global_400000.npy")
meta = pd.read_csv(ROOT / f"Outputs/cells/{ARM}/metadata.csv.gz", low_memory=False)
idx = np.sort(np.random.default_rng(24).choice(len(meta), 400_000, replace=False))
m = meta.iloc[idx].reset_index(drop=True)
assert len(m) == len(xy), f"{len(m)} rows against {len(xy)} points"

CAT = plt.get_cmap("tab10").colors

# PHASE IS GROUPED AS THE ANIMATION GROUPED IT. Nine harmonised levels
# collapse to five in cycle order, with the animation's own palette, so the
# two tell the same story in the same colours.
COARSE = {"menstrual": "menstrual",
          "proliferative_early": "proliferative", "proliferative": "proliferative",
          "proliferative_late": "proliferative", "periovulatory": "periovulatory",
          "secretory_early": "secretory early", "secretory_early_mid": "secretory early",
          "secretory_mid": "secretory late", "secretory_late": "secretory late"}
PHASE_ORDER = ["menstrual", "proliferative", "periovulatory",
               "secretory early", "secretory late"]
PHASE_COL = ["#8C2F39", "#D9A441", "#3A7D5D", "#2F6690", "#6D2E46"]
m["phase group"] = m["menstrual phase"].map(COARSE)

# SEVERITY REPLACES GRADE IN PANEL h, AW 6 November: grade is a coarsening of
# stage, so showing both spent a panel on the same clinical scale twice. The
# merge is what Results [4] tests and it carries 641,024 cells across two
# cohorts against grade's 466,176 in one.
#
# IMPORTED, NOT RETYPED. A second copy of the mapping here could drift from
# the one the numbers are computed with, and then the figure and the prose
# would disagree about what "severe" means.
sys.path.insert(0, str(ROOT / "axw1008" / "src"))
from endo_model.evaluation.label_harmonisation import (            # noqa: E402
    SEVERITY, SEVERITY_SOURCE_COLUMNS, merge_columns)
m["severity"] = merge_columns({c: m[c].to_numpy() for c in SEVERITY_SOURCE_COLUMNS},
                              SEVERITY_SOURCE_COLUMNS, SEVERITY)
SEV_ORDER = list(SEVERITY.order)
SEV_COL = ["#5BA3A0", "#FC8D59", "#B30000"]        # control as Figure 1a; mild and severe on the surgical-stage scale

# ONE RANDOM Z-ORDER, SHARED BY EVERY PANEL. Drawing one class at a time
# puts the last class on top of all the others: disease status is 42%
# eutopic, not 100%, and it only looked that way because `eutopic` sorts
# last and painted over control, ectopic and adenomyosis. Interleaving the
# points removes the artefact without touching the data.
SHUF = np.random.default_rng(1).permutation(len(m))

# Raw obs values where they are not self-explaining. Endometriosis_stage is
# stored as a float, so the panel legend read "0.0 1.0 2.0 3.0 4.0"; it is the
# revised ASRM scale and 0 is marecko's coding for its controls, established
# by arithmetic in validate_latent's _union_severity.
LABEL = {"study_fig": None, "Endometriosis_stage": {"0.0": "control", "1.0": "rASRM I",
                                 "2.0": "rASRM II", "3.0": "rASRM III",
                                 "4.0": "rASRM IV"}}

# THE CYCLE AXIS, panel f. One linear discriminant over the 16-d latent,
# fitted on phase labels outside duempelmann_2026 and oriented along rising
# cycle day on duempelmann's donors, exactly as x16() orients it.
from scipy.stats import spearmanr                                   # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parent))
from supp_figures import _cycle_setup                               # noqa: E402
Zs, _meta_full, W, _, _ = _cycle_setup()
proj = Zs @ W[:, 0]
te = ((_meta_full.study == "duempelmann_2026") & _meta_full.CycleDay.notna()).to_numpy()
dn = (pd.DataFrame({"p": proj[te], "d": _meta_full.CycleDay.to_numpy()[te],
                    "pid": _meta_full.patient_id.to_numpy()[te]})
      .groupby("pid").median())
sgn = np.sign(spearmanr(dn.p, dn.d)[0]) or 1.0
print(f"cycle axis vs day over {len(dn)} donors: rho={spearmanr(sgn*dn.p, dn.d)[0]:+.4f}"
      "  (x16_cycle_axis.csv holds 0.7565)")
# shown on phase-labelled cells only, as C1 drew it: the axis is a reading
# of the cycle, and on cells with no cycle annotation it has nothing to say
ax_score = (sgn * proj)[idx]
m["cycle axis"] = np.where(m["menstrual phase"].notna(), ax_score, np.nan)
del Zs, _meta_full

# COLOURS SHARED WITH FIGURE 1 (NMI: one meaning per colour across the
# paper, and colour-blind safe). Study: Figure 1a's palette and names, the
# two Garcia-Alonso deposits merged as there. Disease status: Figure 1a's
# bar. Site: Okabe-Ito. Surgical stage: an ordered scale, control as in 1a.
from fig2_panels import _study_colours                              # noqa: E402
from mock_fig1a_opt8 import DIS_C                                    # noqa: E402
_SC = _study_colours()
m["study_fig"] = m.study.where(~m.study.str.startswith("garcia_alonso"), "garcia_alonso_2021")
STUDY_ORDER = list(_SC); STUDY_COL = [_SC[k][0] for k in STUDY_ORDER]
LABEL_STUDY = {k: v[1] for k, v in _SC.items()}
TIS_ORDER = ["endometrium", "myometrium", "ovary", "peritoneum", "rectum", "urinary bladder"]
TIS_COL = ["#0072B2", "#56B4E9", "#E69F00", "#D55E00", "#CC79A7", "#009E73"]
DIS_ORDER = ["control", "eutopic", "ectopic", "adenomyosis"]
DIS_COL = [DIS_C[k] for k in DIS_ORDER]
STAGE_ORDER = ["0.0", "1.0", "2.0", "3.0", "4.0"]
STAGE_COL = [DIS_C["control"], "#FDBB84", "#FC8D59", "#D7301F", "#7F0000"]

LABEL["study_fig"] = LABEL_STUDY
PANELS = [
    ("study", "study_fig", "cat", (STUDY_ORDER, STUDY_COL)),
    ("tissue", "tissue", "cat", (TIS_ORDER, TIS_COL)),
    ("menstrual phase", "phase group", "cat", (PHASE_ORDER, PHASE_COL)),
    ("cycle day", "CycleDay", "seq", None),
    ("serum progesterone", "ProgesteroneSerum", "seq", None),
    ("cycle axis", "cycle axis", "axis", None),
    ("disease status", "disease_status", "cat", (DIS_ORDER, DIS_COL)),
    ("severity", "severity", "cat", (SEV_ORDER, SEV_COL)),
    ("surgical stage", "Endometriosis_stage", "cat", (STAGE_ORDER, STAGE_COL)),
]

fig, axes = plt.subplots(3, 3, figsize=(180 * MM, 168 * MM))
# right=.955, not .988: the third column carries a colourbar and at .988 its
# tick labels ran off the canvas.
plt.subplots_adjust(left=.012, right=.955, top=.962, bottom=.012,
                    hspace=.26, wspace=.03)

for ax, (title, col, kind, override) in zip(axes.ravel(), PANELS):
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    v = m[col]
    ok = v.notna().to_numpy()
    ax.scatter(xy[~ok, 0], xy[~ok, 1], s=.5, c="#ededed", lw=0, alpha=.55,
               rasterized=True, zorder=1)
    if kind == "cat":
        levels, cols = (override if override else
                        (sorted(v.dropna().unique(), key=str),
                         [CAT[i % 10] for i in range(v.nunique())]))
        from matplotlib.colors import to_rgb
        lut = {lv: to_rgb(cols[i]) for i, lv in enumerate(levels)}
        keep = SHUF[ok[SHUF]]                       # shuffled, labelled only
        rgb = np.array([lut.get(z, lut.get(str(z), (1, 1, 1))) for z in v.to_numpy()[keep]])
        ax.scatter(xy[keep, 0], xy[keep, 1], s=.5, c=rgb, lw=0, alpha=.40,
                   rasterized=True, zorder=2)
        # NOT TRUNCATED. `[:18]` printed garcia_alonso_2021_a and _b as two
        # identical legend entries in different colours, which reads as a
        # rendering bug and hides the one fact the reader needs about them:
        # they are the same fifteen people under thirty identifiers.
        handles = [Line2D([], [], lw=0, marker="o", ms=3, color=lut[lv],
                          label=LABEL.get(col, {}).get(str(lv), str(lv)))
                   for lv in levels]
        ncol = 2 if len(levels) > 5 else 1
        # Ten studies at 5 pt would sit on the cells: that legend goes under
        # its panel in three columns; the short ones stay in the corner.
        many = len(levels) > 6
        ax.legend(handles=handles, fontsize=5.0, frameon=False, ncol=3 if many else ncol,
                  loc="upper left" if many else "lower left",
                  bbox_to_anchor=(0, .02) if many else None, handletextpad=.3,
                  columnspacing=.6, borderpad=.1, labelspacing=.25)
    elif kind == "axis":
        # unitless, so no numbers on the bar: early and late, clipped to the
        # 2nd-98th percentile so a few extreme cells do not flatten the rest
        x = v.to_numpy(dtype=float)
        keep = SHUF[ok[SHUF]]
        lo, hi = np.percentile(x[keep], [2, 98])
        sc = ax.scatter(xy[keep, 0], xy[keep, 1], s=.5, c=x[keep], cmap="viridis",
                        vmin=lo, vmax=hi, lw=0, alpha=.45, rasterized=True, zorder=2)
        cb = fig.colorbar(sc, ax=ax, fraction=.035, pad=.01, ticks=[lo, hi])
        cb.ax.set_yticklabels(["early", "late"])
        cb.ax.tick_params(labelsize=5.0, length=1.5, color=SOFT)
        cb.outline.set_visible(False)
    else:
        # viridis for both continuous panels, perceptually uniform and the
        # same scale shape, so cycle day and progesterone are comparable by
        # eye rather than by a colour-map difference.
        x = pd.to_numeric(v, errors="coerce").to_numpy()
        keep = SHUF[ok[SHUF]]
        sc = ax.scatter(xy[keep, 0], xy[keep, 1], s=.5, c=x[keep],
                        cmap="viridis", lw=0, alpha=.45, rasterized=True,
                        zorder=2)
        cb = fig.colorbar(sc, ax=ax, fraction=.035, pad=.01)
        cb.ax.tick_params(labelsize=5.0, length=1.5, color=SOFT)
        cb.outline.set_visible(False)
    n = int(ok.sum())
    ax.set_title(f"{title[:1].upper() + title[1:]}   ({100*n/len(m):.0f}% of cells labelled)",
                 fontsize=6.4, pad=3, color=INK)

for ax, letter in zip(axes.ravel(), "abcdefghi"):
    ax.text(.012, .985, letter, transform=ax.transAxes, fontsize=9,
            fontweight="bold", va="top", ha="left")

fig.savefig(OUT / "figure4.png", dpi=int(os.environ.get("FIGDPI", 600)))   # NMI: >= 300 dpi
fig.savefig(OUT / "figure4.pdf", dpi=int(os.environ.get("FIGDPI", 600)))   # dpi sets the rasterised UMAP layers
_src = Path("/Users/atharvawaghmare/Endo research/ELAJ/Outputs/supplementary/source_data"); _src.mkdir(parents=True, exist_ok=True)        # NMI Source Data
_sd = pd.DataFrame({"umap_1": xy[:, 0], "umap_2": xy[:, 1]})
for _t, _c, _k, _o in PANELS:
    _sd[_t.replace(" ", "_")] = m[_c].to_numpy()
_sd.to_csv(_src / "Figure4_source_data.csv.gz", index=False)                                              # NMI: vector, editable
print(f"wrote figure4.png — 9 panels, {len(m):,} cells each")
