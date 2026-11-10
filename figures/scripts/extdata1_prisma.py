#!/usr/bin/env python
"""Extended Data Figure 1 — record selection, following PRISMA 2020.

MOVED OUT OF FIGURE 1 on AW's ruling of 10 November. It had been panel b,
a tall column down the left of a six-panel figure, and it was the reason
that figure had three different column structures in it and no air anywhere.
PRISMA is reporting apparatus rather than a finding, so it earns a page of
its own in Extended Data and Figure 1 gets to breathe.

The convention carries meaning: an amber bar names the identification route,
a spine names the three stages, the main flow runs straight down, and
exclusions branch sideways. A reader who has seen one PRISMA reads this one
without the legend.

ONE FLOW RATHER THAN TWO, because the thesis's parallel columns need four
sub-columns and do not fit a portrait panel legibly. The arithmetic
reconciles exactly: 455 + 98 identified, less 98 duplicates, 42 further
deposits and the 58 manual records the APIs had already returned, leaves 355
screened; 293 excluded leaves 62 sought and assessed; 39 not single cell and
12 for other reasons leaves 11.

COUNTS CORRECTED against the thesis diagram, which is from the r-series era
and ends at twelve included studies where the corpus has eleven. The split is
derived from Data availability rather than guessed: seven GEO accessions, one
ArrayExpress and two CELLxGENE came through the API branch, and CNP0006183
(li et al.) through the hand search of CNGBdb.
"""
from __future__ import annotations
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = Path(__file__).resolve().parents[1] / "pinned"

INK = "#2B3038"
AMBER, AMBER_F = "#CC4E00", "#FFDDA6"
SALMON, SALMON_F = "#825252", "#F78D8D"
PERI, PERI_F = "#7D87FA", "#C2C6FA"

# The type scale is Figure 1's, measured off scGPT and scFoundation:
# panel letter 9, title 6.5, body 5.5. Extended Data has no panel letter.
FS_BODY = 5.5
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": FS_BODY,
                     "text.color": INK, "mathtext.fontset": "dejavusans"})


def bf(s) -> str:
    """A number in bold, inline. AW: every n and every count is bold."""
    return r"$\mathbf{" + str(s).replace(",", "{,}") + r"}$"


def tbox(ax, x, y, w, h, label, fc, ec, weight=None, tc=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, "round,pad=0,rounding_size=0.8",
                                fc=fc, ec=ec, lw=.6, zorder=2))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
            fontsize=FS_BODY, zorder=3, linespacing=1.35,
            color=tc or INK, fontweight=weight or "normal")


def arrow(ax, x0, y0, x1, y1, c=INK):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), zorder=1,
                arrowprops=dict(arrowstyle="-|>", color=c, lw=.6,
                                shrinkA=0, shrinkB=0, mutation_scale=6))


def prisma(ax):
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    MX, MW, EX, EW = 10.0, 42.0, 56.0, 43.0

    tbox(ax, MX, 94.4, MW + EW + 1.0, 5.0, "Database APIs and manual search",
         AMBER_F, AMBER, weight="bold", tc="#8A4000")

    rows = [(78.5, 12.5,
             "Records identified\nDatabase APIs  " + bf(455) +
             "\nCNGBdb  " + bf(98),
             "Records removed\nbefore screening\nDuplicates  " + bf(98) +
             "\nFurther deposits  " + bf(42) +
             "\nAlready found  " + bf(58)),
            (62.0, 9.0, "Records screened\n" + bf("n = 355"),
                        "Records excluded\n" + bf("n = 293")),
            (47.0, 9.0, "Reports sought\n" + bf("n = 62"),
                        "Reports not retrieved\n" + bf("n = 0")),
            (29.5, 11.5, "Reports assessed\nfor eligibility\n" + bf("n = 62"),
                         "Reports excluded\nNot single cell  " + bf(39) +
                         "\nOther reasons  " + bf(12))]
    for y, h, mt, et in rows:
        tbox(ax, MX, y, MW, h, mt, "#FFFFFF", INK)
        tbox(ax, EX, y, EW, h, et, SALMON_F, SALMON)
        arrow(ax, MX + MW, y + h / 2, EX, y + h / 2, c=SALMON)

    tbox(ax, MX, 8.5, MW + 24.0, 13.0,
         bf(11) + " studies included\n" + bf("1,577,728") + " cells\n" +
         bf(254) + " donors\n" + bf(6) + " anatomical sites",
         AMBER_F, AMBER, weight="bold")

    for y0, y1, lab in ((78.0, 93.0, "Identification"),
                        (29.0, 72.0, "Screening"),
                        (8.0, 22.0, "Included")):
        tbox(ax, 1.5, y0, 5.2, y1 - y0, "", PERI_F, PERI)
        ax.text(4.1, (y0 + y1) / 2, lab, ha="center", va="center",
                rotation=90, fontsize=FS_BODY, color="#3B43A8", weight="bold")

    x = MX + MW / 2
    for a, b in ((78.5, 71.4), (62.0, 56.4), (47.0, 41.4), (29.5, 22.0)):
        arrow(ax, x, a, x, b)


def main() -> None:
    W, H = 130.0, 150.0          # Extended Data runs one item to a page
    fig = plt.figure(figsize=(W / 25.4, H / 25.4))
    ax = fig.add_axes([0.01, 0.01, 0.98, 0.98])
    prisma(ax)
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "extdata1_prisma.png",
                dpi=int(os.environ.get("FIGDPI", 600)))
    print(f"wrote {OUT / 'extdata1_prisma.png'}  ({W:.0f} x {H:.0f} mm)")


if __name__ == "__main__":
    main()
