#!/usr/bin/env python
"""Flag any supplementary figure whose placed size shrinks its type below 5 pt.

AW, 17 November: "Fig S3's words are too small", "S31 and S32 are
unreadable", "What is the point of S35/S36? They are illegible." Every one
of those was the same fault and none of them is visible in the source: a
figure authored 260 mm wide, placed at \\textwidth, is scaled to 0.62 and
every 5.5 pt label in it renders at 3.4 pt. LaTeX reports nothing, because
nothing is wrong with the document.

This is the check that makes it visible. Body type in these figures is
FS_BODY = 5.5 pt and NMI's floor is 5 pt, so any placement below 0.91x is a
failure. Run from build_supp.sh.
"""
import re
import sys
from pathlib import Path

from PIL import Image

# The smallest type each generator authors. supp_figures.py's floor is
# FS_LEG; supp_sizing.py, which draws N1's two, uses FS - 0.5.
SMALLEST = {"S1_params_vs_groupsize.png": 6.5, "S2_params_and_deff.png": 6.5}
DEFAULT_SMALLEST, FLOOR = 5.2, 5.0
TEXTWIDTH_MM = 161.0                      # measured from the built PDF

SUPP = Path(__file__).resolve().parents[2] / "supplementary"


def main() -> int:
    notes = "".join(p.read_text() for p in sorted((SUPP / "notes").glob("*.tex")))
    bad = []
    for m in re.finditer(r"includegraphics\[width=([^\]]*)\]\{figures/([^}]+)\}", notes):
        spec, name = m.group(1), m.group(2)
        frac = 1.0 if spec == r"\textwidth" else float(spec.replace(r"\textwidth", ""))
        path = SUPP / "figures" / name
        if not path.exists():
            print(f"  ! {name} is referenced and absent")
            continue
        with Image.open(path) as im:
            px = im.size[0]
            dpi = im.info.get("dpi", (200, 200))[0] or 200
        authored_mm = px / dpi * 25.4
        scale = TEXTWIDTH_MM * frac / authored_mm
        smallest = SMALLEST.get(name, DEFAULT_SMALLEST)
        if smallest * scale < FLOOR:
            bad.append((scale, name, authored_mm, TEXTWIDTH_MM * frac,
                        smallest * scale))
    if not bad:
        print(f"  figure type: every figure clears NMI's {FLOOR:.0f} pt floor"
              " where it is placed")
        return 0
    print(f"  FIGURE TYPE BELOW NMI'S {FLOOR:.0f} pt FLOOR:")
    for scale, name, a, p, pt in sorted(bad):
        print(f"    {name}: authored {a:.0f} mm, placed {p:.0f} mm, "
              f"{scale:.2f}x, body type renders at {pt:.1f} pt")
    print("  Fix by making the FIGURE narrower in supp_figures.py, not by"
          " shrinking its type.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
