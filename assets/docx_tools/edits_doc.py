"""Smallest-edit change list between AW's guide docx (OLD) and a fresh build (NEW),
for pasting into a file with Track Changes on. Sentence alignment first, then
word-level edits inside sentences that changed a little.
python edits_doc.py OLD.docx NEW.docx OUT.docx"""
import docx, difflib, re, sys
from docx.oxml.ns import qn
from docx.shared import RGBColor, Pt
OLD, NEW, OUT = sys.argv[1:4]
STOP={'Figures','Display items','References','Extended Data'}
THIN='   ⁠'
def style(p):
    s=p.find(qn('w:pPr')+'/'+qn('w:pStyle')); return s.get(qn('w:val')) if s is not None else ''
def ptoks(p):
    chars=[]
    for r in p.iter(qn('w:r')):
        rp=r.find(qn('w:rPr')); va=rp.find(qn('w:vertAlign')) if rp is not None else None
        sup=va is not None and va.get(qn('w:val'))=='superscript'
        it=rp is not None and rp.find(qn('w:i')) is not None
        s=''.join(x.text or '' for x in r.iter(qn('w:t'))).replace('\xa0',' ').replace('\n',' ')
        chars+= [(c,sup,it) for c in s]
    toks=[]; cur=None; sp=False
    for c,sup,it in chars:
        if c in ' \t' and not sup:
            if cur: toks.append(cur); cur=None
            sp=True; continue
        if cur and cur['sup']==sup: cur['t']+=c
        else:
            if cur: toks.append(cur)
            cur={'t':c,'sup':sup,'sp':sp and not sup,'it':it}; sp=False
    if cur: toks.append(cur)
    return toks
def doc(path):
    d=docx.Document(path); paras=[]; h1=h2=''; on=False
    for p in d.element.body.iter(qn('w:p')):
        if p.getparent().tag!=qn('w:body'): continue
        t=''.join(x.text or '' for x in p.iter(qn('w:t'))).strip()
        if not t: continue
        st=style(p)
        if st=='Heading1':
            if t=='Introduction': on=True
            elif t in STOP: on=False
            h1=t; h2=''
        elif st=='Heading2': h2=t
        cap= st in ('ImageCaption','TableCaption')
        if (on or cap) and not st.startswith('Heading') and not t.startswith('['):
            paras.append(('Figure legends' if cap else h1+(' › '+h2 if h2 else ''), ptoks(p)))
    return paras
def sentences(paras):
    S=[]
    for where,toks in paras:
        cur=[]
        for i,t in enumerate(toks):
            cur.append(t)
            nxt=toks[i+1] if i+1<len(toks) else None
            if not t['sup'] and re.search(r'[.?!]["”)]?$',t['t']) and not re.search(r'(Fig|Figs|Supplementary|e\.g|i\.e|al|vs)\.$',t['t']) and not (nxt and nxt['sup']):
                S.append((where,cur)); cur=[]
            elif t['sup'] and i>0 and re.search(r'[.?!]$',toks[i-1]['t']):
                S.append((where,cur)); cur=[]
        if cur: S.append((where,cur))
        S.append((where,[{'t':'¶','sup':False,'sp':False,'it':False}]))
    return S
nk=lambda t:(''.join(c for c in t['t'] if c not in THIN),t['sup'])
plain=lambda s:' '.join(nk(t)[0] for t in s if not t['sup'])
full=lambda s:tuple(nk(t) for t in s)
PO=doc(OLD); PN=doc(NEW)
lk=lambda toks:''.join(t['t'] for t in toks[:6])
lo={lk(t) for w,t in PO if w=='Figure legends'}; ln={lk(t) for w,t in PN if w=='Figure legends'}
PO=[x for x in PO if x[0]!='Figure legends' or lk(x[1]) in ln]; PN=[x for x in PN if x[0]!='Figure legends' or lk(x[1]) in lo]
O=sentences(PO); N=sentences(PN)
sm=difflib.SequenceMatcher(None,[plain(s) for _,s in O],[plain(s) for _,s in N],autojunk=False)
A=[]; B=[]   # (where, kind, before_ctx, old, new)
def last_words(s,k=8):
    w=[t for t in s]; out=[]; c=0
    for t in reversed(w):
        out.insert(0,t); c+= not t['sup']
        if c>=k: break
    return out
def word_edits(where,so,sn,prev):
    prev=[] if not prev or prev[0]['t']=='¶' else prev
    ops=[o for o in difflib.SequenceMatcher(None,[nk(t) for t in so],[nk(t) for t in sn],autojunk=False).get_opcodes() if o[0]!='equal']
    mg=[]
    for o in ops:
        if mg and o[1]-mg[-1][2]<=3: mg[-1]=('replace',mg[-1][1],o[2],mg[-1][3],o[4])
        else: mg.append(o)
    for tag,i1,i2,j1,j2 in mg:
        a,b=so[i1:i2],sn[j1:j2]
        ctx=last_words(prev+so[:i1]) or None
        ent=(where,tag,ctx if ctx else None,a,b, None if ctx else so[i2:i2+8])
        A.append(ent+(('cite',) if all(t['sup'] for t in a+b) else ()))
def rat(a,b): return difflib.SequenceMatcher(None,plain(a).split(),plain(b).split()).ratio()
def flush(w,ctxsent,dels,ins,nextsent):
    k=max([i for i,x in enumerate(ins) if x[0]['t']=='¶'],default=-1)
    if k>0:
        para=[t for x in ins[:k] for t in x]
        anchor=(dels[0] if dels else nextsent)[:8]
        A.append((w,'newpara',None,[],para,anchor)); ins=ins[k+1:]
    so=[t for s in dels for t in s if t['t']!='¶']; sn=[t for s in ins for t in s]
    if not so and not [t for t in sn if t['t']!='¶']: return
    ctx=last_words(ctxsent) if ctxsent and ctxsent[0]['t']!='¶' else None
    tag='insert' if not so else ('delete' if not sn else 'replace')
    A.append((w,tag,ctx,so,sn, None if ctx else (so[:8] if so else nextsent[:8])))
def align_block(i1,i2,j1,j2):
    OB=O[i1:i2]; NB=N[j1:j2]; m,n=len(OB),len(NB)
    R=[[rat(OB[i][1],NB[j][1]) if OB[i][1][0]['t']!='¶' and NB[j][1][0]['t']!='¶' else 0 for j in range(n)] for i in range(m)]
    F=[[0.0]*(n+1) for _ in range(m+1)]
    for i in range(m-1,-1,-1):
        for j in range(n-1,-1,-1):
            F[i][j]=max(F[i+1][j],F[i][j+1],(R[i][j]+F[i+1][j+1]) if R[i][j]>0.5 else -1)
    i=j=0; dels=[]; ins=[]; ctxs=O[i1-1][1] if i1>0 else None
    while i<m or j<n:
        if i<m and j<n and R[i][j]>0.5 and F[i][j]==R[i][j]+F[i+1][j+1]:
            flush(OB[i][0],ctxs,dels,ins,OB[i][1]); dels=[]; ins=[]
            if R[i][j]>0.75: word_edits(OB[i][0],OB[i][1],NB[j][1],ctxs)
            else: flush(OB[i][0],ctxs,[OB[i][1]],[NB[j][1]],OB[i][1])
            ctxs=OB[i][1]; i+=1; j+=1
        elif i<m and (j>=n or F[i][j]==F[i+1][j]):
            if not dels and not ins: pass
            dels.append(OB[i][1]); i+=1
        else:
            ins.append(NB[j][1]); j+=1
    flush((OB[0] if OB else NB[0])[0],ctxs,dels,ins,O[i2][1] if i2<len(O) else [])
for tag,i1,i2,j1,j2 in sm.get_opcodes():
    if tag=='equal':
        for k in range(i2-i1):
            (w,so),(_,sn)=O[i1+k],N[j1+k]
            if full(so)!=full(sn): word_edits(w,so,sn,O[i1+k-1][1] if i1+k else [])
        continue
    align_block(i1,i2,j1,j2)
D=docx.Document(); D.styles['Normal'].font.size=Pt(11)
def runs(p,toks,color=None,strike=False):
    first=True
    for t in toks:
        if t['t']=='¶':
            r=p.add_run(' [paragraph break] '); r.italic=True; r.font.color.rgb=RGBColor(0x88,0x88,0x88); first=True; continue
        txt=t['t'].replace('⁠',' ')
        if t['sp'] and not first: txt=' '+txt
        r=p.add_run(txt); r.font.superscript=t['sup']; r.italic=t['it']; r.font.strike=strike
        if color: r.font.color.rgb=RGBColor.from_string(color)
        first=False
def strip_breaks(toks):
    while toks and toks[0]['t']=='¶': toks=toks[1:]
    while toks and toks[-1]['t']=='¶': toks=toks[:-1]
    return toks
def bold(p,s): p.add_run(s).bold=True
D.add_paragraph().add_run("ELAJ — edits for the guide's file (22 November)").bold=True
D.add_paragraph('In order of appearance. "Find" is text already in his file; search for it, then insert, replace or delete as stated. Superscripts are citation numbers. Items marked [citation number] change only a superscript: new references were added to the Introduction, so later numbers moved. The reference list is replaced whole at the end.').runs[0].italic=True
def emit(L,title):
    D.add_heading(title,level=1); last=None
    for k,e in enumerate(L,1):
        w,tag,ctx,a,b,after=e[:6]; ci=len(e)>6
        a=strip_breaks(a); b=strip_breaks(b)
        if w!=last: D.add_heading(w,level=2); last=w
        p=D.add_paragraph(); bold(p,f'{k}. '+('[citation number] ' if ci else ''))
        if tag=='newpara':
            bold(p,'Find the paragraph beginning: '); runs(p,after+[{'t':'…','sup':False,'sp':True,'it':False}])
            p=D.add_paragraph(); bold(p,'Insert this new paragraph before it: '); runs(p,b,'1F5FBF'); continue
        if ctx: bold(p,'Find: '); runs(p,[{'t':'…','sup':False,'sp':False,'it':False}]+ctx)
        else: bold(p,'Find the sentence beginning: '); runs(p,(after or a)[:10]+[{'t':'…','sup':False,'sp':True,'it':False}])
        if tag=='insert' or not a:
            p=D.add_paragraph(); bold(p,'Insert after it: ' if ctx else 'Insert before it: '); runs(p,b,'1F5FBF')
        elif not b:
            p=D.add_paragraph(); bold(p,'Delete: '); runs(p,a,'B00000',strike=True)
        else:
            p=D.add_paragraph(); bold(p,'Replace: '); runs(p,a,'B00000',strike=True)
            p=D.add_paragraph(); bold(p,'With: '); runs(p,b,'1F5FBF')
emit(A,'Text changes, in order')
D.add_heading('References',level=1)
D.add_paragraph('Every entry from 3 onward has moved and five are new, so replace the whole list with this one.')
for p in docx.Document(NEW).element.body.iter(qn('w:p')):
    if style(p)=='Bibliography': D.add_paragraph(''.join(x.text or '' for x in p.iter(qn('w:t'))))
D.add_heading('Supplementary',level=1)
D.add_paragraph('Not itemised: the renumbering touches almost every caption and cross-reference; a regenerated supplementary file replaces it whole.')
D.save(OUT); print('items',len(A),'of which citation-only',sum(len(e)>6 for e in A))
