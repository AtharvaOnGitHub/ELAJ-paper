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

[ "${1:-}" = "clean" ] && latexmk -C supplementary.tex >/dev/null 2>&1 || true

latexmk -pdf -interaction=nonstopmode -halt-on-error supplementary.tex

echo
grep -c "Overfull" supplementary.log 2>/dev/null | \
    xargs -I{} echo "  overfull boxes: {}"
echo "  $(pwd)/supplementary.pdf"
