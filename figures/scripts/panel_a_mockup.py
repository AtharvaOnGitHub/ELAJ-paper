#!/usr/bin/env python
"""Candidate panel a — the architecture, drawn in IBDex's grammar.

A MOCK-UP FOR AW, 10 November. He asked to see the layout rather than read
it. If he likes it this can become the real panel a; if he prefers to redraw
it in his own tool, the spec is here in executable form.

WHAT IT TAKES FROM IBDex (Acharjee, medRxiv 2026.10.20.26365993, Fig. 1b),
which is the figure his supervisor was happy with:
  * Bold coloured headings over each stage, left-aligned over the group's
    leftmost box. Groups by ROLE, not per box.
  * One hue family per role. Pale tinted fill, saturated border of the same
    hue. Sampled from his figure: blue #3F6FB4, teal #2F8F88, amber #D89120,
    purple #6750A4.
  * Detail pushed OUT of the boxes into grey lines beneath them, so a box
    carries a name and nothing else.
  * Dimensions annotated under each stage. This is the half of IBDex's
    encoder trapezoid that actually transfers: our group stage is 44
    PARALLEL towers, not a narrowing MLP, so the trapezoid shape would
    misrepresent it while the numbers underneath do not.

WHAT IT KEEPS FROM AW'S DRAWING. Every element, in the same order, with the
same reading direction. The decoder conditioning still enters the
reconstruction head alone, which is the thing he had me verify in the code.
"""
from __future__ import annotations
import os
from pathlib import Path

# ARIAL THROUGHOUT, and it is a shared decision rather than a default.
# Panel a is drawn in LucidChart and the rest here, so one typeface has
# to span both. Arial ships on macOS as a .ttf LucidChart can import,
# matplotlib resolves it to the same file, and it is the grotesque the
# Nature family sets its own figures in. It also carries every mark this
# paper needs: Dümpelmann, Marečková, García-Alonso, lambda, subscripts.
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, RegularPolygon, Polygon, Circle

OUT = Path(__file__).resolve().parents[1] / "pinned"

# ── palette, sampled from IBDex ──────────────────────────────────────────
GREY_F, GREY_E, GREY_T = "#EDEFF2", "#6B7380", "#4A5260"
BLUE_F, BLUE_E, BLUE_T = "#E9F2FC", "#3F6FB4", "#2B5894"
AMB_F,  AMB_E,  AMB_T  = "#FFF3DE", "#D89120", "#8A5000"
TEAL_F, TEAL_E, TEAL_T = "#DCEFEC", "#2F8F88", "#1C5F5A"
PURP_F, PURP_E, PURP_T = "#F2EAF7", "#6750A4", "#4A3878"
ROSE = "#C2544E"
NOTE = "#7A818C"

FS_HEAD, FS_BOX, FS_NOTE = 6.5, 6.0, 5.5   # headings / box labels / annotations
plt.rcParams.update({"font.family": "Arial", "text.color": "#2B3038"})


def vdots(ax, x, y, colour):
    """Three dots, drawn. Arial has no U+22EE vertical ellipsis, and a font
    that silently drops a glyph is worse than one that never had it."""
    for dy in (-1.6, 0.0, 1.6):
        ax.add_patch(Circle((x, y + dy), .32, fc=colour, ec="none", zorder=4))


def box(ax, x, y, w, h, label, fc, ec, tc, fs=FS_BOX, rot=0, weight=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, "round,pad=0,rounding_size=1.1",
                                fc=fc, ec=ec, lw=.75, zorder=3))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
            fontsize=fs, color=tc, rotation=rot, zorder=4, linespacing=1.25,
            fontweight=weight or "normal")


def heading(ax, x, y, text, colour):
    ax.text(x, y, text, ha="left", va="bottom", fontsize=FS_HEAD,
            fontweight="bold", color=colour)


def note(ax, x, y, text, ha="center"):
    ax.text(x, y, text, ha=ha, va="top", fontsize=FS_NOTE, color=NOTE,
            linespacing=1.3)


def arrow(ax, x0, y0, x1, y1, c="#8A9099", lw=.7, ls="-", rad=0.0, head=True):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), zorder=2,
                arrowprops=dict(arrowstyle="-|>" if head else "-", color=c,
                                lw=lw, ls=ls, shrinkA=0, shrinkB=0,
                                connectionstyle=f"arc3,rad={rad}",
                                mutation_scale=7))


def main() -> None:
    W, H = 180.0, 56.0
    fig = plt.figure(figsize=(W / 25.4, H / 25.4))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H)
    ax.axis("off")

    HEAD_Y, NOTE_Y = 49.5, 11.0
    MID = 29.0
    rows = (39.5, 31.5, 15.5)            # group 1, group 2, group 44

    # ── Input ───────────────────────────────────────────────────────────
    heading(ax, 3.0, HEAD_Y, "Input", GREY_T)
    box(ax, 3.0, 14.0, 7.0, 32.0, "Cell", GREY_F, GREY_E, GREY_T, rot=90)
    box(ax, 13.5, 14.0, 9.0, 32.0, "Pathway filter\nand DNS sentinel",
        GREY_F, GREY_E, GREY_T, fs=FS_NOTE, rot=90)
    arrow(ax, 10.0, MID, 13.5, MID)
    note(ax, 6.5, NOTE_Y, "30,962\ngenes")
    note(ax, 18.0, NOTE_Y, "15,496\ngenes")

    # ── Gene encoder ────────────────────────────────────────────────────
    heading(ax, 27.0, HEAD_Y, "Gene encoder", BLUE_T)
    for lab, y in zip(("Gene group 1", "Gene group 2", "Gene group 44"), rows):
        box(ax, 27.0, y, 23.0, 6.5, lab, BLUE_F, BLUE_E, BLUE_T)
        arrow(ax, 22.5, MID, 27.0, y + 3.25, rad=0 if y == rows[1] else
              (-.10 if y > MID else .10))
    vdots(ax, 38.5, 25.5, BLUE_E)

    box(ax, 53.5, 14.0, 6.5, 32.0, "Domain-specific\nbatch normalisation",
        BLUE_F, BLUE_E, BLUE_T, fs=FS_NOTE, rot=90)
    for y in rows:
        arrow(ax, 50.0, y + 3.25, 53.5, y + 3.25)

    for lab, y in zip(("Group transformer 1", "Group transformer 2",
                       "Group transformer 44"), rows):
        box(ax, 63.5, y, 27.0, 6.5, lab, BLUE_F, BLUE_E, BLUE_T)
        arrow(ax, 60.0, y + 3.25, 63.5, y + 3.25)
    vdots(ax, 77.0, 25.5, BLUE_E)
    note(ax, 59.0, NOTE_Y, "44 groups, 9 summary tokens each")

    # ── Cell encoder ────────────────────────────────────────────────────
    heading(ax, 95.0, HEAD_Y, "Cell encoder", BLUE_T)
    box(ax, 95.0, 25.5, 13.0, 7.0, "Cell\naggregation",
        BLUE_F, BLUE_E, BLUE_T, fs=FS_NOTE)
    box(ax, 108.0, 25.5, 13.0, 7.0, "Cell\ntransformer",
        BLUE_F, BLUE_E, BLUE_T, fs=FS_NOTE)
    for y in rows:
        arrow(ax, 90.5, y + 3.25, 95.0, MID, rad=-.12 if y > MID else .12)
    note(ax, 108.0, NOTE_Y, "396 tokens, then 64")

    # ── Latent ──────────────────────────────────────────────────────────
    ax.add_patch(RegularPolygon((133.0, MID), 6, radius=8.2, orientation=0,
                                fc=AMB_F, ec=AMB_E, lw=.9, zorder=3))
    ax.text(133.0, MID, "Gaussian\nlatent space", ha="center", va="center",
            fontsize=FS_NOTE, color=AMB_T, zorder=4, linespacing=1.25,
            fontweight="bold")
    arrow(ax, 121.0, MID, 124.8, MID)
    note(ax, 133.0, NOTE_Y, "16 dimensions")

    # ── Training objectives ─────────────────────────────────────────────
    heading(ax, 148.0, HEAD_Y, "Training objectives", TEAL_T)
    heads = (("DAB", "study adversary", 40.0),
             ("Phase CLS", "menstrual phase", 32.0),
             ("ECS", "cell similarity", 24.0),
             ("Reconstruction", "negative binomial", 16.0))
    for lab, gloss, y in heads:
        box(ax, 148.0, y, 29.0, 5.6, lab, TEAL_F, TEAL_E, TEAL_T)
        ax.text(162.5, y - 0.5, gloss, ha="center", va="top",
                fontsize=FS_NOTE, color=NOTE)
        arrow(ax, 141.2, MID, 148.0, y + 2.8,
              rad=-.22 if y > MID else (.22 if y < MID - 4 else 0))

    # ── Decoder conditioning, into reconstruction alone ─────────────────
    box(ax, 95.0, 15.0, 24.0, 5.6, "Decoder conditioning",
        PURP_F, PURP_E, PURP_T, fs=FS_NOTE)
    ax.text(107.0, 14.5, "study  ·  platform  ·  tissue", ha="center",
            va="top", fontsize=FS_NOTE, color=NOTE)
    arrow(ax, 119.0, 17.8, 148.0, 18.8, c=PURP_E, rad=-.06)

    # ── Gradient reversal, the one thing that runs backwards ────────────
    tx, ty = 139.0, 48.0
    ax.add_patch(Polygon([(tx + 3.0, ty + 1.9), (tx + 3.0, ty - 1.9),
                          (tx - 1.1, ty)], closed=True, fc="#FFFFFF",
                         ec=ROSE, lw=.8, zorder=5))
    ax.add_patch(Circle((tx - 1.8, ty), .75, fc="#FFFFFF", ec=ROSE, lw=.8,
                        zorder=5))
    arrow(ax, 162.5, ty, tx + 3.0, ty, c=ROSE, ls=(0, (3, 2)), head=False)
    arrow(ax, 162.5, 45.6, 162.5, ty, c=ROSE, ls=(0, (3, 2)), head=False)
    arrow(ax, tx - 2.6, ty, 133.0, MID + 8.2, c=ROSE, ls=(0, (3, 2)))
    ax.text(tx - 4.2, ty + 2.6, "gradient reversal", ha="right", va="bottom",
            fontsize=FS_NOTE, color=ROSE)

    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "panel_a_mockup.png",
                dpi=int(os.environ.get("FIGDPI", 600)))
    print(f"wrote {OUT / 'panel_a_mockup.png'}  ({W:.0f} x {H:.0f} mm)")


if __name__ == "__main__":
    main()
