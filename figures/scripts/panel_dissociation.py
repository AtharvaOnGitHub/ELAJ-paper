#!/usr/bin/env python
"""Candidate panel — what the latent holds, and where it stops.

TAKEN FROM IBDex FIGURE 2c (Acharjee, medRxiv 2026.10.20.26365993), which AW
flagged as the visualisation his supervisor was happy with: a forest of
held-out effects on the left, the numbers aligned in a table on the right,
non-significant rows greyed and badged. It suits this result because the
paper's own rule is that numbers are shown rather than asserted.

ONE HONEST DIFFERENCE FROM IBDex. Theirs has a single chance line at AUC 0.5.
Ours cannot: the permutation null's width tracks donor count, so every label
is read against its OWN threshold. That is drawn, per row, as the grey bar
from zero. A label carried by few donors has a wide null and a value inside
it is undetectable at that donor count rather than absent.

THE ORDERING IS THE ARGUMENT, and it is Results [4]'s dissociation. Every
contrast that includes control donors clears its null. Neither contrast
restricted to patients does. So the model can say whether a person has
endometriosis and cannot say how severe a surgeon judged it.

WHAT IS DELIBERATELY NOT HERE.
  * Per-study disease tests (0.3433, 0.0697, 1.000 at 16, 18 and 2 donors).
    At that donor count the null reaches 0.42 and the test detects nothing,
    so plotting them would show a power artefact as if it were evidence.
  * The whole-corpus cell family and phase readings quoted in Results. They
    do not resolve to a benchmark row for this arm, so the held-out rows are
    used instead and their donor counts say so.

EVERY NUMBER IS READ FROM THE SAME benchmark.csv FILES THE AUDITORS READ.
Nothing here is typed in.
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
import pandas as pd

ROOT = Path("/Users/atharvawaghmare/Endo research/ELAJ")
BENCH = ROOT / "Outputs/Benchmarks"
OUT = Path(__file__).resolve().parents[1] / "pinned"

HELD = BENCH / "full/full_p1_dab168_kl1/benchmark.csv"
WHOLE = BENCH / "whole_corpus/wholecorpus_p1_dab168_kl1/benchmark.csv"

INK, SOFT, HAIR = "#2B3038", "#6F7681", "#C9CDD4"
AMBER, AMBER_F = "#CC4E00", "#FFDDA6"
SALMON, SALMON_F = "#825252", "#F78D8D"
NULLC = "#DDE0E4"
FS_LETTER, FS_TITLE, FS_BODY = 9.0, 6.5, 5.5
plt.rcParams.update({"font.family": "Arial", "font.size": FS_BODY,
                     "text.color": INK, "mathtext.fontset": "custom",
                     "mathtext.rm": "Arial",
                     "mathtext.it": "Arial:italic",
                     "mathtext.bf": "Arial:bold"})

# (display label, file, test, label-in-file, which block)
ROWS = [
    ("Cell family",                     HELD,  "cross-donor",    "cell family",              "bio"),
    ("Menstrual phase",                 HELD,  "cross-donor",    "menstrual phase",          "bio"),
    ("Disease status",                  HELD,  "disease-xdonor", "all studies (pooled)",     "ctrl"),
    ("Surgical stage, rASRM I–IV",      WHOLE, "cross-donor",    "Endometriosis_stage",      "ctrl"),
    ("Severity, three levels",          WHOLE, "cross-donor",    "severity",                 "ctrl"),
    ("Severity, mild against severe",   WHOLE, "cross-donor",    "severity (patients only)", "pat"),
    ("Endometriosis grade",             WHOLE, "cross-donor",    "EndometriosisGrade",       "pat"),
]
# The group headings ARE the argument: everything whose contrast includes a
# control donor clears its null, and nothing restricted to patients does.
BLOCK = {"bio":  "Cell identity and cycle",
         "ctrl": "Contrast includes control donors",
         "pat":  "Contrast restricted to patients"}


def fields(note: str) -> dict:
    out = {}
    for part in str(note).split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            try: out[k.strip()] = float(v.strip().split()[0])
            except ValueError: pass
        for unit in ("donors", "groups"):
            if part.strip().endswith(unit):
                try: out["n"] = int(part.strip().split()[0])
                except ValueError: pass
    return out


def read_rows():
    cache = {}
    out = []
    for disp, f, test, lab, block in ROWS:
        if f not in cache:
            b = pd.read_csv(f)
            b["mm"] = b.method.astype(str).str.replace("__.*", "", regex=True)
            cache[f] = b
        b = cache[f]
        e = b[(b.mm == "elaj") & (b.test == test) & (b.label == lab)]
        if e.empty:
            raise KeyError(f"{test}/{lab} absent from {f}")
        r = e.iloc[0]; fl = fields(r["note"])
        out.append(dict(label=disp, block=block, value=float(r["value"]),
                        p=fl.get("p"), null95=fl.get("null95"), n=fl.get("n")))
    return out


def main() -> None:
    rows = read_rows()
    W, H = 180.0, 70.0
    fig = plt.figure(figsize=(W / 25.4, H / 25.4))
    axf = fig.add_axes([0.300, 0.125, 0.330, 0.745])
    axt = fig.add_axes([0.645, 0.125, 0.345, 0.745]); axt.axis("off")

    # one y-grid over group headings AND rows, so a heading occupies a slot
    # of its own. The first version drew the headings rotated down the far
    # left, where all three landed on top of one another.
    slots, cur = [], None
    for r in rows:
        if r["block"] != cur:
            cur = r["block"]; slots.append(("head", r["block"]))
        slots.append(("row", r))
    n = len(slots)
    ys = {i: n - 1 - i for i in range(n)}

    axf.set_ylim(-0.8, n - 0.2); axf.set_xlim(-0.10, 1.06)

    for blk, shade, alpha in (("ctrl", AMBER_F, .20), ("pat", SALMON_F, .13)):
        idx = [i for i, (k, v) in enumerate(slots)
               if (k == "head" and v == blk) or (k == "row" and v["block"] == blk)]
        if idx:
            axf.axhspan(ys[idx[-1]] - .5, ys[idx[0]] + .5, color=shade,
                        alpha=alpha, zorder=0)
    axf.axvline(0, color=SOFT, ls=(0, (3, 2)), lw=.6, zorder=1)

    LBLX = -0.035
    for i, (kind, payload) in enumerate(slots):
        y = ys[i]
        if kind == "head":
            axf.text(LBLX, y, BLOCK[payload], ha="right", va="center",
                     fontsize=FS_BODY, color=SOFT, style="italic",
                     transform=axf.get_yaxis_transform(), clip_on=False)
            continue
        r = payload
        sig = r["p"] is not None and r["p"] < 0.05
        col = AMBER if sig else SOFT
        if r["null95"] is not None:
            axf.barh(y, r["null95"], height=.34, color=NULLC, lw=0, zorder=2)
        axf.plot([0, r["value"]], [y, y], color=col, lw=1.3, zorder=3,
                 solid_capstyle="butt", alpha=.55)
        axf.scatter([r["value"]], [y], s=34, zorder=4,
                    c=AMBER_F if sig else "#FFFFFF",
                    edgecolors=col, linewidths=1.0)
        axf.text(LBLX, y, r["label"], ha="right", va="center",
                 fontsize=FS_BODY, color=INK if sig else SOFT,
                 fontweight="bold" if sig else "normal",
                 transform=axf.get_yaxis_transform(), clip_on=False)

    axf.set_yticks([])
    axf.set_xlabel("cross-donor excess agreement over chance",
                   fontsize=FS_BODY, labelpad=2.0)
    axf.tick_params(length=2, pad=2.0, labelsize=FS_BODY, colors=SOFT)
    axf.xaxis.set_major_locator(plt.MaxNLocator(6))
    for s in ("top", "right", "left"):
        axf.spines[s].set_visible(False)
    axf.spines["bottom"].set_color(HAIR)
    axf.grid(axis="x", lw=.35, color=HAIR, alpha=.55)
    axf.set_axisbelow(True)

    # ── the aligned table, IBDex's right-hand half ──────────────────────
    axt.set_xlim(0, 1); axt.set_ylim(-0.8, n - 0.2)
    for x, headtxt in ((0.10, "Excess"), (0.37, "Null 95%"),
                       (0.64, "P"), (0.89, "Donors")):
        axt.text(x, n - 0.55, headtxt, ha="center", va="bottom",
                 fontsize=FS_BODY, fontweight="bold", color=INK)
    for i, (kind, payload) in enumerate(slots):
        if kind == "head":
            continue
        y, r = ys[i], payload
        sig = r["p"] is not None and r["p"] < 0.05
        col = INK if sig else SOFT
        axt.text(0.10, y, f"{r['value']:+.4f}", ha="center", va="center",
                 fontsize=FS_BODY, color=col,
                 fontweight="bold" if sig else "normal")
        axt.text(0.37, y, "\u2014" if r["null95"] is None else f"{r['null95']:.2f}",
                 ha="center", va="center", fontsize=FS_BODY, color=SOFT)
        if sig:
            axt.text(0.64, y, f"{r['p']:.3f}", ha="center", va="center",
                     fontsize=FS_BODY, color=col)
        else:
            axt.text(0.64, y, "ns", ha="center", va="center", fontsize=FS_BODY,
                     color="#FFFFFF", fontweight="bold",
                     bbox=dict(boxstyle="round,pad=0.22", fc=SALMON_F,
                               ec=SALMON, lw=.5))
        axt.text(0.89, y, str(r["n"] or "\u2014"), ha="center", va="center",
                 fontsize=FS_BODY, color=SOFT)

    fig.text(0.012, 0.930, "a", fontsize=FS_LETTER, fontweight="bold",
             ha="left", va="bottom")
    fig.text(0.048, 0.936, "What the latent holds, and where it stops",
             fontsize=FS_TITLE, ha="left", va="bottom", color=INK)

    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "panel_dissociation.png",
                dpi=int(os.environ.get("FIGDPI", 600)))
    print(f"wrote {OUT / 'panel_dissociation.png'}  ({W:.0f} x {H:.0f} mm)")
    for r in rows:
        print(f"  {r['label']:32s} {r['value']:+.4f}  null95 {r['null95']}"
              f"  p {r['p']}  n {r['n']}")


if __name__ == "__main__":
    main()
