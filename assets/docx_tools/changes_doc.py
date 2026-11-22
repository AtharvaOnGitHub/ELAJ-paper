import docx, difflib, copy, re, sys
from docx.oxml.ns import qn
OLD, NEW, OUT = sys.argv[1:4]
def txt(p): return ''.join(x.text or '' for x in p.iter(qn('w:t'))).strip()
def plain(p):  # text without superscript runs (citation numbers)
    s=''
    for r in p.iter(qn('w:r')):
        rp=r.find(qn('w:rPr')); va=rp.find(qn('w:vertAlign')) if rp is not None else None
        if va is not None and va.get(qn('w:val'))=='superscript': continue
        s+=''.join(t.text or '' for t in r.iter(qn('w:t')))
    return re.sub(r'\s+',' ',s).strip()
def style(p):
    s=p.find(qn('w:pPr')+'/'+qn('w:pStyle')); return s.get(qn('w:val')) if s is not None else ''
def body_paras(d):
    out=[]; h1=h2=''
    for p in d.element.body.iter(qn('w:p')):
        if p.getparent().tag!=qn('w:body'): continue   # skip tables
        t=txt(p)
        if not t: continue
        st=style(p)
        if st=='Heading1': h1=t; h2=''
        elif st=='Heading2': h2=t
        out.append(dict(p=p,t=t,pl=plain(p),st=st,h1=h1,h2=h2))
    return out
do=docx.Document(OLD); dn=docx.Document(NEW)
o=body_paras(do); n=body_paras(dn)
STOP={'Figures','Display items','References','Extended Data'}
def cut(L):
    for i,x in enumerate(L):
        if x['st']=='Heading1' and x['t'] in STOP: return L[:i]
    return L
ob=cut(o); nb=cut(n)
# legends: match by first 60 chars, anywhere after the cut
def legends(L): return {re.sub(r'\s+',' ',x['t'].replace('\xa0',' '))[:40]:x for x in L if x['st'] in ('ImageCaption','TableCaption')}
key=lambda x:x['t'][:40]
sm=difflib.SequenceMatcher(None,[key(x) for x in ob],[key(x) for x in nb],autojunk=False)
entries=[]; intro_new=[x for x in nb if x['h1']=='Introduction' and x['st']!='Heading1']
for tag,i1,i2,j1,j2 in sm.get_opcodes():
    for jj in range(j1,j2):
        x=nb[jj]
        if x['h1'] in ('Introduction','') or x['st'].startswith('Heading') or x['t'].startswith('['): continue
        if tag=='equal':
            if x['t']==ob[i1+jj-j1]['t']: continue
            y=ob[i1+jj-j1]
            kind='text' if x['pl']!=y['pl'] else 'cite'
            entries.append((x,y,kind))
        elif tag=='replace' and (i2-i1)==(j2-j1):
            y=ob[i1+jj-j1]
            if x['t']==y['t']: continue
            kind='text' if x['pl']!=y['pl'] else 'cite'
            entries.append((x,y,kind))
        else:
            entries.append((x,None,'new'))
# build output on the new doc's styles
out=docx.Document(NEW); B=out.element.body
sect=B.find(qn('w:sectPr'))
for c in list(B):
    if c is not sect: B.remove(c)
def add(text,bold=False,italic=False,color=None,size=None,style=None):
    p=out.add_paragraph(style=style); r=p.add_run(text); r.bold=bold; r.italic=italic
    if color: r.font.color.rgb=docx.shared.RGBColor.from_string(color)
    if size: r.font.size=docx.shared.Pt(size)
    return p
def paste(x): B.insert(len(B)-1 if sect is not None else len(B), copy.deepcopy(x['p']))
def words(s,n=12): w=s.split(); return ' '.join(w[:n])+(' …' if len(w)>n else '')
add('ELAJ — changes to copy into the guide\'s file (22 November)',bold=True,size=14)
add('In order of appearance. Each item says where, then gives the text to paste. Paste with "Keep Source Formatting" so citation superscripts and italics carry over. '
    '“Citation numbers only” means the wording is unchanged but the reference numbers have shifted, because new references were added to the Introduction.',italic=True)
k=0
k+=1; add(f'{k}. Introduction — replace all of it',bold=True,style='Heading 2')
intro_old=[x for x in ob if x['h1']=='Introduction' and x['st']!='Heading1']
add('Select the whole Introduction: from the paragraph beginning “'+words(intro_old[0]['t'],8)+'” to the end of the paragraph beginning “'+words(intro_old[-1]['t'],8)+'”. Paste these six paragraphs over it:',italic=True,color='555555')
for x in intro_new: paste(x)
for x,y,kind in entries:
    k+=1
    loc=x['h1']+(' › '+x['h2'] if x['h2'] else '')
    lab={'text':'wording changed','cite':'citation numbers only','new':'new paragraph'}[kind]
    add(f'{k}. {loc} — {lab}',bold=True,style='Heading 2')
    if y is not None:
        add('Find the paragraph beginning: “'+words(y['t'],14)+'”. Replace the whole paragraph with:',italic=True,color='555555')
    else:
        add('Insert this new paragraph here (after the previous item):',italic=True,color='555555')
    paste(x)
# legends
lo=legends(o); ln=legends(n)
for kk,x in ln.items():
    y=lo.get(kk)
    if y and y['t']!=x['t']:
        k+=1; kind='wording changed' if x['pl']!=y['pl'] else 'citation numbers only'
        add(f'{k}. Figure legends — {kind}',bold=True,style='Heading 2')
        add('Find the legend beginning: “'+words(y['t'],14)+'”. Replace the whole legend with:',italic=True,color='555555')
        paste(x)
# references
k+=1; add(f'{k}. References — replace the whole list',bold=True,style='Heading 2')
add('Delete the existing reference list and paste this one. It has five new entries and every number from 3 onward has moved.',italic=True,color='555555')
refs=[p for p in dn.element.body.iter(qn('w:p')) if style(p) in ('Bibliography',)]
for p in refs: B.insert(len(B)-1, copy.deepcopy(p))
k+=1; add(f'{k}. Supplementary file',bold=True,style='Heading 2')
add('Not listed item by item: the renumbering (S prefix dropped, Notes reordered, numbered Note headings, new Supplementary Table 12) touches almost every caption and cross-reference. A regenerated supplementary file replaces the old one whole.',italic=True,color='555555')
out.save(OUT)
print('items',k,'body entries',len(entries),'legends checked',len(ln),'refs',len(refs))
for x,y,kind in entries: print(kind,'|',x['h1'],'|',x['h2'],'|',x['t'][:50])

if len(sys.argv)>4:
    for x,y,kind in entries:
        if kind=='text' and y:
            a=y['pl'].split(); b=x['pl'].split()
            for tag,i1,i2,j1,j2 in difflib.SequenceMatcher(None,a,b).get_opcodes():
                if tag!='equal': print('  ',x['t'][:25],'|',' '.join(a[i1:i2]),'=>',' '.join(b[j1:j2]))
    # legends with citations in new doc
    for x in n:
        if 'mcinnes' in x['t'].lower() or ('UMAP' in x['t'] and len(x['t'])>200): print('LEG',x['st'],x['t'][:80])
