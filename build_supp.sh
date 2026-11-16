#!/bin/bash
# Build the Supplementary Information PDF.
#
#   bash build_supp.sh          full build
#   bash build_supp.sh clean    remove aux files and rebuild
#
# Separate from build.sh on purpose: the supplementary is its own
# document with its own numbering, and a change to it must not force a
# rebuild of the manuscript or vice versa.

set -euo pipefail
cd "$(dirname "$0")/supplementary"

export PATH="/Library/TeX/texbin:$PATH"
command -v latexmk >/dev/null || {
    echo "latexmk not found. MacTeX is expected at /Library/TeX/texbin." >&2
    exit 1
}

# latexmk -C alone leaves the .bbl, so a bibliography change can
# survive a "clean" and citations silently stay unresolved.
if [ "${1:-}" = "clean" ]; then
    latexmk -C supplementary.tex >/dev/null 2>&1 || true
    rm -f supplementary.bbl
fi

latexmk -pdf -interaction=nonstopmode -halt-on-error supplementary.tex

echo
# `grep -c` exits 1 when the count is zero, which under `set -euo pipefail`
# killed this script silently after the first line. A clean build is the
# common case, so both counts need `|| true`.
echo "  overfull boxes: $(grep -c "Overfull" supplementary.log || true)"
echo "  undefined references: $(grep -c "undefined" supplementary.log || true)"

# A FIGURE PLACED SMALL ENOUGH TO TAKE ITS TYPE UNDER 5 pt IS A FAILURE
# LATEX CANNOT SEE. Nothing is wrong with the document, so no warning is
# issued; the figure is simply unreadable. AW found four of them by eye on
# 17 November. This is the check that finds the fifth.
PY=/Users/atharvawaghmare/miniconda3/envs/elaj/bin/python
[ -x "$PY" ] && "$PY" ../figures/scripts/check_figure_scale.py || true
echo "  $(pwd)/supplementary.pdf"
