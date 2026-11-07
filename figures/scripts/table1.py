#!/usr/bin/env python
"""Table 1 — every representation on every axis, generated not typed.

REPLACES FIGURE 5. AW, 6 November 2026: the ablations figure becomes one
long table carrying p-series, a-series, baselines and foundation models on
all the relevant axes. NMI counts a table as a display item, so this keeps
the paper at five of six.

THE SOURCES ARE THE AUDIT'S SOURCES. Every path below also appears in
audit_numbers.py's MANIFEST or verify_numbers.py's SOURCES, so a cell in
this table and the same number in the prose cannot come from different
files. Severity is the one axis scored in a separate pass, for the reason
recorded in both auditors: the labels were added to CROSS_DONOR_LABELS
after the main battery had run.

ORDERING IS THE ARGUMENT. Four blocks, and inside each one the rows are
sorted by cross-donor menstrual phase, descending, so a reader meets every
group at its best rather than in the order we happened to run things. The
ablations are the exception: the base sits first because every other row in
that block is a change against it.
"""
from __future__ import annotations
import csv, os, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BENCH = ROOT / "Outputs/Benchmarks"
OUT = Path(__file__).resolve().parents[2] / "sections" / "table1.tex"

AXES = [("phase",   "cross-donor",    "menstrual phase"),
        ("family",  "cross-donor",    "cell family"),
        ("ctype",   "knn-agreement",  "AnnotationRefined"),
        ("disease", "disease-xdonor", "all studies (pooled)"),
        ("sev",     "cross-donor",    "severity"),
        ("donor",   "knn-agreement",  "patient_id"),
        ("mix",     "study-mixing",   "all studies")]

def rows(p: Path):
    with open(p, newline="") as fh:
        yield from csv.DictReader(fh)

def grab(path: Path, meth: str, policy=None, fit=None) -> dict:
    out: dict = {}
    if not path.exists():
        sys.exit(f"missing source {path}")
    for r in rows(path):
        if re.sub("__.*", "", r.get("method") or "") != meth:
            continue
        if policy is not None and (r.get("gene_policy") or "") != policy:
            continue
        if fit is not None and (r.get("fit_on") or "") != fit:
            continue
        out.setdefault((r["test"], r["label"]), r["value"])
        if r.get("width"):
            out["width"] = r["width"]
    return out

# ── the field, from the audit's own manifest ─────────────────────────────
MANIFEST = {
    "pca":          ("wide_full_inductive",   "all30962", "train",      "PCA"),
    "scvi":         ("wide_full_inductive",   "all30962", "train",      "scVI"),
    "scanvi":       ("wide_full_inductive",   "all30962", "train",      "scANVI"),
    "harmony":      ("wide_full_harmony",     "all30962", "",           "Harmony"),
    "scanorama":    ("wide_full_scanorama",   "all30962", "",           "Scanorama"),
    "scgpt":        ("wide_full_scgpt",       "native",   "pretrained", "scGPT"),
    "geneformer":   ("wide_full_geneformer",  "native",   "pretrained", "Geneformer"),
    "scimilarity":  ("wide_full_scimilarity", "native",   "pretrained", "SCimilarity"),
    "scfoundation": ("fm_scfoundation",       "native",   "pretrained", "scFoundation"),
}
BASELINES = ("pca", "scvi", "scanvi", "harmony", "scanorama")
FOUNDATION = ("scgpt", "geneformer", "scimilarity", "scfoundation")
# scFoundation's full-split pass was OOM-killed inside scIB before the
# mixing stage, so that one row comes from a --stages mixing re-run over
# the same dumped latent. Same arrangement the auditors use.
MIXING_OVERRIDE = {"scfoundation": "mixing_scfoundation"}
SEVERITY = {"pca": "severity_ind_pca", "scvi": "severity_ind_scvi",
            "scanvi": "severity_ind_scanvi", "scgpt": "severity_scgpt",
            "geneformer": "severity_geneformer", "scfoundation": "severity_scfoundation",
            "scimilarity": "severity_scimilarity", "harmony": "severity_trans_harmony",
            "scanorama": "severity_trans_scanorama"}
SUPERVISION = {"scanvi": "cell family", "scimilarity": "cell family"}
# Fitted on the cells they are scored on, which is an advantage and is
# declared rather than left for a reader to infer from the method name.
TRANSDUCTIVE = {"harmony", "scanorama"}

# ── ELAJ, from the full-split re-scores ──────────────────────────────────
P_SERIES = [("p1_dab7_kl1",    7,   1), ("p1_dab7_kl30",   7,  30),
            ("p1_dab168_kl1",  168, 1), ("p1_dab168_kl30", 168, 30),
            ("p1_dab336_kl1",  336, 1), ("p1_dab336_kl30", 336, 30)]
NAMED = {"p1_dab168_kl1": r"\,(B\textsubscript{hi})",
         "p1_dab168_kl30": r"\,(B\textsubscript{lo})"}
A_SERIES = [("a1_randgroups", "random gene grouping"),
            ("a1_nophase",    "no phase head"),
            ("a1_noecs",      "no ECS"),
            ("a1_nodns",      "no DNS sentinel"),
            ("a1_clsonly",    "no order statistics")]
METRICS = {"p1_dab7_kl1": "p_series/p1_dab7_kl1", "p1_dab7_kl30": "p_series/p1_dab7_kl30",
           "p1_dab168_kl1": "p_series/p1_dab168_kl1", "p1_dab168_kl30": "p_series/p1_dab168_kl30",
           "p1_dab336_kl1": "p_series/p1_dab336_kl1", "p1_dab336_kl30": "p_series/p1_dab336_kl30",
           "a1_nophase": "a_series/a1_nophase", "a1_noecs": "a_series/a1_noecs",
           "a1_clsonly": "a_series/a1_clsonly", "a1_nodns": "a_series/a1_nodns",
           "a1_randgroups": "a_series/a1_randgroups"}

def val_nb(key: str) -> str:
    f = ROOT / "Outputs" / METRICS[key] / "metrics.csv"
    if not f.exists():
        return "--"
    v = [float(r["val_nb"]) for r in rows(f)]
    return f"{min(v):.4f}"

def collect() -> dict:
    out = {}
    for m, (run, pol, fit, _) in MANIFEST.items():
        g = grab(BENCH / run / "benchmark.csv", m, pol, fit)
        if m in MIXING_OVERRIDE:
            g.update({k: v for k, v in
                      grab(BENCH / MIXING_OVERRIDE[m] / "benchmark.csv", m).items()
                      if k[0] == "study-mixing"})
        g.update({k: v for k, v in
                  grab(BENCH / SEVERITY[m] / "benchmark.csv", m).items()
                  if k == ("cross-donor", "severity")})
        out[m] = g
    for key, _, _ in P_SERIES:
        out[key] = grab(BENCH / "full" / f"full_{key}" / "benchmark.csv", "elaj")
    for key, _ in A_SERIES:
        out[key] = grab(BENCH / "full" / f"full_{key}" / "benchmark.csv", "elaj")
    return out

def cell(g: dict, test: str, label: str) -> str:
    v = g.get((test, label))
    return "--" if v in (None, "") else f"{float(v):.4f}"

def line(name: str, g: dict, width: str, sup: str, nb: str, bold=False) -> str:
    vals = [cell(g, t, l) for _, t, l in AXES]
    if bold:
        name = r"\textbf{" + name + "}"
        vals = [r"\textbf{" + v + "}" for v in vals]
    return " & ".join([name, width, sup] + vals + [nb]) + r" \\"

def main() -> None:
    D = collect()
    L = [r"% GENERATED by figures/scripts/table1.py. Do not edit by hand.",
         r"\begin{table*}[p]\centering\footnotesize",
         r"\setlength{\tabcolsep}{3pt}",
         r"\caption{\textbf{Every representation on every axis.} "
         r"Cross-donor agreement, reported as excess over chance, for "
         r"menstrual phase, cell family and merged severity; $k$-nearest-"
         r"neighbour agreement for the forty-five-way cell type and for "
         r"donor identity; pooled control-against-eutopic agreement for "
         r"disease; and $k$NN study purity for study separation, rescaled "
         r"so that 0 is perfectly mixed and 1 fully separated. "
         r"$\uparrow$ marks an axis where more is better and $\downarrow$ "
         r"one where less is. Held-out split throughout. "
         r"\texttt{val\_nb} is held-out negative-binomial reconstruction "
         r"loss per cell at the selected checkpoint, which only the "
         r"\elaj\ arms have. Rows are ordered within each block by "
         r"cross-donor menstrual phase, except the ablations, where the "
         r"base arm leads because the rest are single-key changes against "
         r"it. $\lambda$ is the adversarial weight and $w_{kl}$ the "
         r"information cost.}",
         r"\label{tab:field}",
         r"\begin{tabular}{l r l rrrrr rr r}",
         r"\toprule",
         r" & & & \multicolumn{5}{c}{\textbf{biology} $\uparrow$}"
         r" & \multicolumn{2}{c}{\textbf{cost} $\downarrow$} & \\",
         r"\cmidrule(lr){4-8}\cmidrule(lr){9-10}",
         r"model & dims & super- & phase & cell & cell "
         r"& disease & sever- & donor & study & \texttt{val\_nb} \\",
         r" & & vised on & & family & type & & ity & & & $\downarrow$ \\",
         r"\midrule",
         r"\multicolumn{11}{l}{\textit{\elaj, the two knobs}} \\"]

    ps = sorted(P_SERIES, key=lambda t: -float(D[t[0]][("cross-donor", "menstrual phase")]))
    for key, dab, kl in ps:
        nm = (rf"$\lambda$ {dab}, $w_{{kl}}$ {kl}" + NAMED.get(key, ""))
        L.append(line(nm, D[key], "16", "phase", val_nb(key),
                      bold=key in NAMED))

    L += [r"\midrule",
          r"\multicolumn{11}{l}{\textit{\elaj, one key changed against "
          r"B\textsubscript{hi}}} \\"]
    base = "p1_dab168_kl1"
    L.append(line(r"B\textsubscript{hi}, unchanged", D[base], "16",
                  "phase", val_nb(base)))
    for key, nm in sorted(A_SERIES,
                          key=lambda t: -float(D[t[0]][("cross-donor", "menstrual phase")])):
        L.append(line(nm, D[key], "16",
                      "--" if key == "a1_nophase" else "phase", val_nb(key)))

    for title, block in ((r"integration and dimension reduction", BASELINES),
                         (r"pretrained foundation models", FOUNDATION)):
        L += [r"\midrule", rf"\multicolumn{{11}}{{l}}{{\textit{{{title}}}}} \\"]
        for m in sorted(block, key=lambda m: -float(D[m][("cross-donor", "menstrual phase")])):
            nm = MANIFEST[m][3] + (r"$^{\dagger}$" if m in TRANSDUCTIVE else "")
            L.append(line(nm, D[m], D[m].get("width", "--"),
                          SUPERVISION.get(m, "--"), "--"))

    L += [r"\bottomrule",
          r"\end{tabular}",
          r"\\[2pt]\footnotesize $^{\dagger}$ fitted transductively on the "
          r"cells it is scored on; every other method was fitted on the "
          r"training donors and applied to held-out ones.",
          r"\end{table*}"]
    OUT.write_text("\n".join(L) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)}  ({len(ps)+len(A_SERIES)+1+len(BASELINES)+len(FOUNDATION)} rows)")

if __name__ == "__main__":
    main()
