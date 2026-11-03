#!/bin/bash
# Build the manuscript PDF.
#
#   bash build.sh          full build
#   bash build.sh clean    remove the aux files and rebuild from scratch
#
# MacTeX installs to /Library/TeX/texbin and does not put itself on the
# PATH of a non-login shell, so it is added here rather than assumed.
# TeX Live 2026 is what built the thesis; same toolchain.

set -euo pipefail
cd "$(dirname "$0")"

export PATH="/Library/TeX/texbin:$PATH"
command -v latexmk >/dev/null || {
    echo "latexmk not found. MacTeX is expected at /Library/TeX/texbin." >&2
    exit 1
}

if [ "${1:-}" = "clean" ]; then
    latexmk -C >/dev/null 2>&1 || true
    rm -f main.bbl main.synctex.gz
fi

# THE NUMBERS ARE CHECKED BEFORE THE PDF EXISTS, not after. On 3 November the
# audit was found to have been drawing baseline rows from whichever benchmark
# file a glob reached first, and the only reason it was caught was a reader
# noticing. A check that runs when someone remembers is not a check, so both
# scripts run here and a failure stops the build.
#
#   SKIP_NUMBER_CHECK=1 bash build.sh   to build anyway, deliberately.
PY=/Users/atharvawaghmare/miniconda3/envs/elaj/bin/python
if [ -z "${SKIP_NUMBER_CHECK:-}" ] && [ -x "$PY" ]; then
    echo "Checking every number in Results against its source..."
    "$PY" figures/scripts/audit_numbers.py >/dev/null || {
        echo "audit_numbers.py FAILED. Run it directly for the detail." >&2
        exit 1
    }
    "$PY" figures/scripts/verify_numbers.py >/dev/null || {
        echo "verify_numbers.py FAILED. Run it directly for the detail." >&2
        exit 1
    }
    echo "  both number checks passed."
fi

# -halt-on-error so a broken macro fails loudly rather than dropping into
# the interactive prompt and hanging. -interaction=nonstopmode for the same
# reason. latexmk handles the bibtex and rerun passes itself.
latexmk -pdf -halt-on-error -interaction=nonstopmode main.tex

# pdfinfo ships with xpdf/poppler, not with MacTeX, so the page count is
# read from the log instead of assuming a binary that is not there.
pages=$(awk -F'[()]' '/Output written on main.pdf/{print $2}' main.log \
        | awk '{print $1}')
echo
echo "  $(pwd)/main.pdf — ${pages} pages, $(wc -c < main.pdf | tr -d ' ') bytes"
