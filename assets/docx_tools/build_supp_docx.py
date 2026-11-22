"""Fresh supplementary .docx for the guide, captions only.
python assets/docx_tools/build_supp_docx.py <out.docx> <styles-from.docx>
Run from Paper_writing after building supplementary.pdf (needs supplementary.aux)."""
import copy, pathlib, re, shutil, subprocess, sys, tempfile, zipfile
import docx
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
OUT, STY = sys.argv[1:3]
PD = str(pathlib.Path.home() / "miniconda3/envs/elaj/bin/pandoc")
PY = sys.executable
T = pathlib.Path(tempfile.mkdtemp())
BROKEN = ["stab:arms-p", "stab:scib-family", "stab:x13", "stab:abl-bio", "stab:coverage", "stab:buckets", "stab:hyperparameters"]
pre = pathlib.Path("preamble.tex"); keep = pre.read_text()
try:
    pre.write_text(re.sub(r"\\newcommand\{\\elaj\}\{\{\\fontfamily\{comfortaa\}%.*?\\xspace\}", r"\\newcommand{\\elaj}{ELAJ\\xspace}", keep, flags=re.S))
    common = ["--reference-doc=../assets/reference.docx", "--lua-filter=../assets/docx_captions_only.lua", "--resource-path=.:.."]
    subprocess.run([PD, "supplementary.tex", "-o", str(T/"raw.docx"), "--bibliography=../references.bib", "--citeproc", "--csl=../assets/nature.csl"] + common, cwd="supplementary", check=True)
    subprocess.run([PY, "assets/docx_tools/t7.py"] + BROKEN, check=True)
    subprocess.run([PD, "_tables7.tex", "-o", str(T/"t7.docx")] + common, cwd="supplementary", check=True)
finally:
    pre.write_text(keep); pathlib.Path("supplementary/_tables7.tex").unlink(missing_ok=True)
lab = {m.group(1): m.group(2) for m in re.finditer(r"\\newlabel\{([^}]+)\}\{\{([^}]*)\}", pathlib.Path("supplementary/supplementary.aux").read_text())}
d = docx.Document(T/"raw.docx"); b = d.element.body
src = list(docx.Document(T/"t7.docx").element.body)
text = lambda e: ''.join(t.text or '' for t in e.iter(qn('w:t')))
def style(e):
    s = e.find(qn('w:pPr')+'/'+qn('w:pStyle')) if e.tag == qn('w:p') else None
    return s.get(qn('w:val')) if s is not None else None
caps = [(i, e) for i, e in enumerate(src) if style(e) == 'TableCaption']; assert len(caps) == len(BROKEN)
blocks = {}
for k, (nm, (i, e)) in enumerate(zip(BROKEN, caps)):
    tbl = next(x for x in src[i+1:] if x.tag == qn('w:tbl'))
    cap = copy.deepcopy(e)
    for x in list(cap.iter(qn('w:bookmarkStart'))) + list(cap.iter(qn('w:bookmarkEnd'))): x.getparent().remove(x)
    bm = OxmlElement('w:bookmarkStart'); bm.set(qn('w:id'), str(9000+k)); bm.set(qn('w:name'), nm)
    be = OxmlElement('w:bookmarkEnd'); be.set(qn('w:id'), str(9000+k))
    first = next(c for c in cap if c.tag != qn('w:pPr')); first.addprevious(bm); first.addprevious(be)
    blocks[nm] = (cap, copy.deepcopy(tbl))
for marker, nm in [("@lrrrr@", "stab:buckets"), ("@lX@", "stab:hyperparameters")]:
    start = next(p for p in b if p.tag == qn('w:p') and text(p).startswith(marker))
    cur = start; dead = []
    while cur is not None and cur.tag == qn('w:p') and '&' in text(cur): dead.append(cur); cur = cur.getnext()
    cap, tbl = blocks.pop(nm); start.addprevious(cap); start.addprevious(tbl)
    for x in dead: b.remove(x)
for nm, (cap, tbl) in blocks.items():   # pandoc dropped these: place after the first paragraph citing them
    num = lab[nm]
    p = next(p for p in b if p.tag == qn('w:p') and style(p) not in ('TableCaption', 'ImageCaption') and re.search(rf"Tables?[^.]*?\b{num}(?!\d)", text(p)))
    p.addnext(tbl); p.addnext(cap)
d.save(T/"tables.docx")
subprocess.run([PY, "assets/docx_tools/number.py", str(T/"tables.docx"), str(T/"num.docx"), "supplementary/supplementary.aux", "supp"], check=True)
# tables cited together ("Tables 1, 2 and 3") can land out of order: put every table after its predecessor if so
d = docx.Document(T/"num.docx"); b = d.element.body
def cap_of(n): return next((p for p in b if p.tag == qn('w:p') and text(p).startswith(f"Supplementary Table {n} |")), None)
n = 1
while cap_of(n+1) is not None:
    a, c = cap_of(n), cap_of(n+1)
    if list(b).index(c) < list(b).index(a):
        ta, tc = a.getnext(), c.getnext(); ta.addnext(tc); ta.addnext(c)
    n += 1
d.save(T/"num.docx")
# AW's styles and page setup
zo, zn = zipfile.ZipFile(STY), zipfile.ZipFile(T/"num.docx")
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zt:
    for it in zn.infolist():
        zt.writestr(it, zo.read("word/styles.xml") if it.filename == "word/styles.xml" else zn.read(it.filename))
d = docx.Document(OUT); b = d.element.body
so = docx.Document(STY).element.body.find(qn('w:sectPr')); sn = b.find(qn('w:sectPr'))
if sn is not None: b.remove(sn)
b.append(copy.deepcopy(so)); d.save(OUT)
seq = [re.match(r"Supplementary (Fig\.|Table) (\d+) \|", text(p)) for p in b if p.tag == qn('w:p')]
print(OUT, ' '.join(m.group(1)[0]+m.group(2) for m in seq if m))
