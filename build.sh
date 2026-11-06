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
# FIGURES ARE BOXES BY DEFAULT, and the full images only with FIGS=1.
#
# WHY. The submission renders are 1200 dpi, which is 36 MB of PDF and most of
# the build time, and during drafting nobody reads them. graphicx's own draft
# option substitutes a labelled frame of the right size, so the layout and the
# page count stay honest while the bytes do not.
#
# This is NOT why main.pdf was unreadable on 6 November. That was two
# concurrent latexmk runs writing the same file: one backgrounded build and one
# started before it finished, which left a stale startxref and undecodable
# streams. One build at a time; the lock below enforces it.
PRETEX=""
if [ -z "${FIGS:-}" ]; then
    PRETEX="-pretex=\\PassOptionsToPackage{draft}{graphicx} -usepretex"
    echo "Figures: boxed (set FIGS=1 for the real images)"
else
    echo "Figures: full resolution"
fi

# ONE BUILD AT A TIME. Two latexmk processes on one main.pdf corrupt it: on 6
# November a backgrounded build and a second one started before it finished
# left a stale startxref and undecodable streams, and the file would not open.
# flock is a Linux utility and is NOT on macOS, so this is a mkdir lock, which
# is atomic everywhere.
LOCK=.build.lock
if ! mkdir "$LOCK" 2>/dev/null; then
    echo "another build holds $LOCK. Wait for it, or remove $LOCK if stale." >&2
    exit 1
fi
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

# shellcheck disable=SC2086
latexmk -pdf -halt-on-error -interaction=nonstopmode $PRETEX main.tex

# pdfinfo ships with xpdf/poppler, not with MacTeX, so the page count is
# read from the log instead of assuming a binary that is not there.
pages=$(awk -F'[()]' '/Output written on main.pdf/{print $2}' main.log \
        | awk '{print $1}')
echo
echo "  $(pwd)/main.pdf — ${pages} pages, $(wc -c < main.pdf | tr -d ' ') bytes"
