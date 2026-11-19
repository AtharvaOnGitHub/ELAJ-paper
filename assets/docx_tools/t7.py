import re,pathlib
root=pathlib.Path("supplementary")
def expand(p):
    s=re.sub(r"(?<!\\)%.*","",p.read_text())
    def inc(m):
        for q in ((p.parent/m.group(1)).with_suffix(".tex"),(root/m.group(1)).with_suffix(".tex")):
            if q.exists(): return expand(q)
        return m.group(0)
    return re.sub(r"\\input\{([^}]*)\}",inc,s)
s=expand(root/"supplementary.tex")
want=["stab:scib-family","stab:coverage","stab:arms-p","stab:abl-bio","stab:x13","stab:buckets","stab:hyperparameters"]
def grp(e,j):
    j=e.index("{",j); depth=0
    for k in range(j,len(e)):
        depth+=(e[k]=="{")-(e[k]=="}")
        if depth==0: return j,k
def strip_resize(e):
    while "\\resizebox" in e:
        i=e.find("\\resizebox"); _,a=grp(e,i); _,b=grp(e,a+1); st,end=grp(e,b+1)
        e=e[:i]+e[st+1:end]+e[end+1:]
    return e
def fix(e):
    e=re.sub(r"\\begin\{tabularx\}\{[^}]*\}",r"\\begin{tabular}",e).replace("\\end{tabularx}","\\end{tabular}")
    def spec(m):
        sp=re.sub(r"@\{[^}]*\}","",m.group(1)); sp=re.sub(r"[pmb]\{[^}]*\}|X","l",sp); sp=re.sub(r"[^lrc]","",sp)
        return "\\begin{tabular}{"+sp+"}"
    e=re.sub(r"\\begin\{tabular\}\{((?:[^{}]|\{[^{}]*\})*)\}",spec,e)
    e=e.replace("\\quad","").replace("\\addlinespace\n","").replace("\\addlinespace","")
    return re.sub(r"\\multicolumn\{(\d+)\}\{(?:[^{}]|\{[^{}]*\})*\}",r"\\multicolumn{\1}{l}",e)
envs={re.search(r"\\label\{(stab:[^}]+)\}",e).group(1):e for e in re.findall(r"\\begin\{table\}.*?\\end\{table\}",s,re.S) if re.search(r"\\label\{(stab:[^}]+)\}",e)}
pre=(root/"supplementary.tex").read_text(); pre=pre[:pre.index("\\begin{document}")]
import sys; sel=sys.argv[1:] or want
(root/"_tables7.tex").write_text(pre+"\\begin{document}\n"+"\n\n".join(fix(strip_resize(envs[w])) for w in sel)+"\n\\end{document}\n")
