#!/usr/bin/env bash
# Build the clean draft: ELAJ_draft1.pdf and ELAJ_draft1.docx.
#
# Everything this flips, it flips back. Three differences from ./build.sh:
#
#   draftmodefalse   suppresses \note, \todo, \flow and the line numbers.
#   downsampled PNGs the pinned figures are submission resolution and make a
#                    37 MB PDF. The originals are copied to .fullres and
#                    restored at the end, so nothing is lost.
#   plain \elaj      comfortaa with letterspacing does not survive pandoc, so
#                    the DOCX is built against a copy of the preamble where
#                    \elaj is plain text. Calibri comes from
#                    assets/reference.docx, whose theme fonts were set to it.
set -euo pipefail
cd "$(dirname "$0")"
PY=/Users/atharvawaghmare/miniconda3/envs/elaj/bin/python
PANDOC=/Users/atharvawaghmare/miniconda3/envs/elaj/bin/pandoc

restore() {
    [ -f preamble.tex.bak ] && mv preamble.tex.bak preamble.tex
    sed -i '' 's/^\\draftmodefalse$/\\draftmodetrue/' preamble.tex || true
    [ -d figures/pinned/.fullres ] && cp figures/pinned/.fullres/*.png figures/pinned/
    echo "restored: draft mode on, full-resolution figures back"
}
trap restore EXIT

mkdir -p figures/pinned/.fullres
cp figures/pinned/*.png figures/pinned/.fullres/
$PY - <<'EOF'
from PIL import Image
import glob
for f in glob.glob("figures/pinned/*.png"):
    im = Image.open(f); w, h = im.size
    s = min(1.0, 2200 / max(w, h))
    if s < 1.0:
        im.resize((int(w * s), int(h * s)), Image.LANCZOS).save(f, optimize=True)
EOF

sed -i '' 's/^\\draftmodetrue$/\\draftmodefalse/' preamble.tex
FIGS=1 ./build.sh
cp main.pdf ELAJ_draft1.pdf

# \elaj is comfortaa at 88% with 150 units of letterspacing, which pandoc
# cannot carry into Word. For the DOCX it becomes plain capitals.
cp preamble.tex preamble.tex.bak
$PY - <<'EOF'
import pathlib, re
p = pathlib.Path("preamble.tex"); s = p.read_text()
s = re.sub(r"\\newcommand\{\\elaj\}\{\{\\fontfamily\{comfortaa\}%.*?\\xspace\}",
           r"\\newcommand{\\elaj}{ELAJ\\xspace}", s, flags=re.S)
p.write_text(s)
EOF
# Citation style. Pandoc's --citeproc default is Chicago author-date, which is
# why the supervisor's Word copy read "( Bontempo and Schiff 2025)" while the
# PDF was numbered. NMI wants numbered references, so the DOCX needs a numeric
# CSL. Drop the official Nature style at assets/nature.csl and it is used
# automatically; without it the build still runs and says so loudly.
CSL_ARG=""
if [ -f assets/nature.csl ]; then
    CSL_ARG="--csl=assets/nature.csl"
    echo "citations: numbered, assets/nature.csl"
else
    echo "WARNING: assets/nature.csl missing, citations will be author-date."
    echo "         Get it from https://www.zotero.org/styles/nature"
fi

$PANDOC main.tex -o ELAJ_draft1.docx \
    --reference-doc=assets/reference.docx \
    --bibliography=references.bib --citeproc $CSL_ARG --resource-path=.

ls -la ELAJ_draft1.pdf ELAJ_draft1.docx
