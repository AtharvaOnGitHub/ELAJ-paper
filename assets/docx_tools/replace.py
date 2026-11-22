"""Replace text in a docx even when Word has split it across runs.
python replace.py file.docx 'old' 'new' ['old2' 'new2' ...]"""
import sys, docx
def replace_in_par(par, old, new):
    runs=par.runs; full=''.join(r.text for r in runs); i=full.find(old); n=0
    while i>=0:
        pos=0
        for r in runs:
            a,b=pos,pos+len(r.text); pos=b
            if b<=i or a>=i+len(old): continue
            s,e=max(i,a)-a,min(i+len(old),b)-a
            r.text=r.text[:s]+(new if a<=i<b else '')+r.text[e:]
        n+=1; full=''.join(r.text for r in runs); i=full.find(old, i+len(new))
    return n
f=sys.argv[1]; pairs=list(zip(sys.argv[2::2],sys.argv[3::2])); d=docx.Document(f); tot={o:0 for o,_ in pairs}
pars=list(d.paragraphs)+[p for t in d.tables for row in t.rows for c in row.cells for p in c.paragraphs]
for p in pars:
    for o,nw in pairs: tot[o]+=replace_in_par(p,o,nw)
d.save(f); print(tot)
