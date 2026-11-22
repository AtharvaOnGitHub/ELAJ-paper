import docx, re, pathlib, copy, sys
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
M='{http://schemas.openxmlformats.org/officeDocument/2006/math}'
src,dst,aux,kind=sys.argv[1:5]
lab={m.group(1):m.group(2) for m in re.finditer(r"\\newlabel\{([^}]+)\}\{\{([^}]*)\}",pathlib.Path(aux).read_text())}
d=docx.Document(src); b=d.element.body
def runs_of(p): return [r for r in p.iter(qn('w:r'))]
def set_link(h,txt):
    ts=list(h.iter(qn('w:t')))
    ts[0].text=txt
    for t in ts[1:]: t.text=''
def prefix(p,txt):
    r=OxmlElement('w:r'); rp=OxmlElement('w:rPr'); bb=OxmlElement('w:b'); rp.append(bb); r.append(rp)
    t=OxmlElement('w:t'); t.text=txt; t.set('{http://www.w3.org/XML/1998/namespace}space','preserve'); r.append(t)
    first=next((c for c in p if c.tag!=qn('w:pPr')),None)
    (first.addprevious(r) if first is not None else p.append(r))
nl=0
for h in b.iter(qn('w:hyperlink')):
    a=h.get(qn('w:anchor'))
    if a in lab:
        cur=''.join(t.text or '' for t in h.iter(qn('w:t')))
        if cur!=lab[a]: set_link(h,lab[a]); nl+=1
def style(e):
    s=e.find(qn('w:pPr')+'/'+qn('w:pStyle')) if e is not None and e.tag==qn('w:p') else None
    return s.get(qn('w:val')) if s is not None else None
nf=nt=0
if kind=="supp":
    # Note headings: pandoc drops the \thesection redefinition, so the Word file
    # loses "Supplementary Note N". Put it back as its own line above the title,
    # as NMI supplementaries print it.
    k=0
    for p in list(b.iter(qn('w:p'))):
        if style(p)=='Heading1' and ''.join(t.text or '' for t in p.iter(qn('w:t'))).strip() not in ('Supplementary Methods','References'):
            k+=1
            r=OxmlElement('w:r'); t=OxmlElement('w:t'); t.text=f"Supplementary Note {k}"; r.append(t); r.append(OxmlElement('w:br'))
            first=next((c for c in p if c.tag!=qn('w:pPr')),None)
            (first.addprevious(r) if first is not None else p.append(r))
    for bm in list(b.iter(qn('w:bookmarkStart'))):
        n=bm.get(qn('w:name'))
        if n.startswith('sfig:'):
            tc=bm
            while tc.tag!=qn('w:tc'): tc=tc.getparent()
            caps=[p for p in tc.iter(qn('w:p')) if style(p)=='ImageCaption']
            if not caps:
                tbl=tc
                while tbl.tag!=qn('w:tbl'): tbl=tbl.getparent()
                nx=tbl.getnext(); caps=[nx] if style(nx)=='ImageCaption' else []
            assert len(caps)==1,(n,len(caps))
            prefix(caps[0],f"Supplementary Fig. {lab[n]} | "); nf+=1
        elif n.startswith('stab:'):
            p=bm
            while p.tag!=qn('w:p'): p=p.getparent()
            assert style(p)=='TableCaption',n
            prefix(p,f"Supplementary Table {lab[n]} | "); nt+=1
# equation numbers: wrap each display equation in a borderless 3-column table
eqs=[v for k,v in sorted(((k,v) for k,v in lab.items() if k.startswith('eq:')), key=lambda kv:int(kv[1]))]
paras=[]
for om in b.iter(M+'oMathPara'):
    p=om
    while p.tag!=qn('w:p'): p=p.getparent()
    paras.append(p)
assert len(paras)==len(eqs),(len(paras),eqs)
W=int(d.sections[0].page_width-d.sections[0].left_margin-d.sections[0].right_margin)
for p,num in zip(paras,eqs):
    t=d.add_table(rows=1,cols=3); T=t._tbl
    pr=T.tblPr
    for tag in ('w:tblStyle',):
        for x in pr.findall(qn(tag)): pr.remove(x)
    bd=OxmlElement('w:tblBorders')
    for side in ('top','left','bottom','right','insideH','insideV'):
        e=OxmlElement(f'w:{side}'); e.set(qn('w:val'),'nil'); bd.append(e)
    pr.append(bd)
    ws=[int(W*0.1),int(W*0.8),int(W*0.1)]
    for gc,w in zip(T.tblGrid.findall(qn('w:gridCol')),ws): gc.set(qn('w:w'),str(w//635))
    for c,w in zip(t.rows[0].cells,ws): c.width=w
    for c in t.rows[0].cells:
        va=OxmlElement('w:vAlign'); va.set(qn('w:val'),'center'); c._tc.get_or_add_tcPr().append(va)
    mid=t.rows[0].cells[1]._tc
    for q in mid.findall(qn('w:p')): mid.remove(q)
    p.addprevious(T); mid.append(p)
    rc=t.rows[0].cells[2]; rp=rc.paragraphs[0]; rp.alignment=2; rp.add_run(f"({num})")
    # copy paragraph spacing of the equation paragraph to the number paragraph
    ppr=p.find(qn('w:pPr'))
    if ppr is not None and ppr.find(qn('w:spacing')) is not None:
        rp._p.get_or_add_pPr().append(copy.deepcopy(ppr.find(qn('w:spacing'))))
d.save(dst)
print(f"{dst}: links fixed {nl}, fig captions {nf}, table captions {nt}, equations {len(paras)}")
