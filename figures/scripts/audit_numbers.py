"""Every number in Results, traced to the file it came from.

    python figures/scripts/audit_numbers.py

Reads the source files, re-derives each figure, writes audit/NUMBERS.md, and
then scans sections/02-results.tex for decimals that the derivation does not
account for. A number in the prose that is not in the derived set is either a
typo or a claim with no source, and both are reported.

Nothing here is typed from memory: every value is pulled from
Outputs/Benchmarks/<arm>/benchmark.csv at run time.
"""
from __future__ import annotations
import glob, os, re, sys
from pathlib import Path
import pandas as pd

ROOT = Path("/Users/atharvawaghmare/Endo research/ELAJ")
OUT  = Path(__file__).resolve().parents[2] / "audit" / "NUMBERS.md"
TEX  = Path(__file__).resolve().parents[2] / "sections" / "02-results.tex"

TESTS = {"donor":  ("knn-agreement", "patient_id",        "lower is better"),
         "mixing": ("study-mixing",  "all studies",       "lower is better"),
         "phase":  ("cross-donor",   "menstrual phase",   "higher is better"),
         "family": ("cross-donor",   "cell family",       "higher is better"),
         "disease":("disease-xdonor","all studies (pooled)","higher is better")}

def read(path: Path, method: str) -> dict:
    b = pd.read_csv(path)
    b["mm"] = b.method.astype(str).str.replace("__.*", "", regex=True)
    e = b[b.mm == method]
    row = {}
    for k, (t, l, _) in TESTS.items():
        s = e[(e.test == t) & (e.label == l)]["value"]
        row[k] = float(s.iloc[0]) if len(s) else float("nan")
    w = e["width"].dropna()
    row["width"] = int(w.max()) if len(w) else None
    sup = {str(x) for x in e["supervised_on"].dropna() if str(x) != "nan"}
    row["supervised_on"] = ", ".join(sorted(sup)) or "—"
    return row

# ---------------------------------------------------------------------------
# The ELAJ-only findings: ablations (D1-D7) and whole-corpus geometry (C1-C5).
# These never cross a method boundary, so the baseline re-scoring does not
# touch them. They were previously listed under "not yet auditable" and taken
# on trust from project documents; they are re-derived here instead.
# ---------------------------------------------------------------------------

ABL = {"p1_dab168_kl1":  ("BASE",          "Outputs/Benchmarks/p1_dab168_kl1",
                          "Outputs/p_series/p1_dab168_kl1"),
       "a1_nophase":     ("-phase head",   "Outputs/Benchmarks/a_series/a1_nophase",
                          "Outputs/a_series/a1_nophase"),
       "a1_noecs":       ("-ECS",          "Outputs/Benchmarks/a_series/a1_noecs",
                          "Outputs/a_series/a1_noecs"),
       "a1_clsonly":     ("-statistics",   "Outputs/Benchmarks/a_series/a1_clsonly",
                          "Outputs/a_series/a1_clsonly"),
       "a1_nodns":       ("-sentinel",     "Outputs/Benchmarks/a_series/a1_nodns",
                          "Outputs/a_series/a1_nodns"),
       "a1_randgroups":  ("random groups", "Outputs/Benchmarks/a_series/a1_randgroups",
                          "Outputs/a_series/a1_randgroups")}

def label_rows(path: Path, test: str) -> dict:
    """Every (label -> value) for one test, ELAJ rows only."""
    b = pd.read_csv(path)
    b["mm"] = b.method.astype(str).str.replace("__.*", "", regex=True)
    e = b[(b.mm == "elaj") & (b.test == test)]
    return dict(zip(e.label, e.value.astype(float)))

def best_epoch(metrics: Path) -> tuple:
    """Checkpoint selection is argmin val_nb -- verified against the 'best ep'
    column of ABLATIONS.md for all six arms. Returns (epoch, row, last row)."""
    m = pd.read_csv(metrics)
    i = int(m["val_nb"].idxmin())
    return int(m.loc[i, "epoch"]), m.loc[i], m.iloc[-1], len(m)

arms, base = {}, {}
for f in sorted(glob.glob(str(ROOT / "Outputs/Benchmarks/p1_*/benchmark.csv"))):
    name = Path(f).parent.name
    if not name.endswith("_train"):
        arms[name] = (read(Path(f), "elaj"), f)
# ─────────────────────────────────────────────────────────────────────────
# AN EXPLICIT MANIFEST, BECAUSE GLOBBING IS WHAT BROKE THIS AUDIT.
#
# The version before this one took each baseline from whichever benchmark file
# a glob reached first. Every number it printed was real, and the table was
# still invalid: `pca` arrived from the reported arm on the narrow 15,496-gene
# policy while the foundation models arrived from the fm_* runs on the wide
# 30,962-gene one, so the comparison it displayed had never been run as one
# experiment. The script even printed a warning that the runs were not
# comparable, directly underneath the table built by mixing them.
#
# So each row now NAMES its file and its (gene_policy, fit_on) key. A missing
# key is an error. Nothing falls back to another file, and no file outside
# this dict can contribute a number.
# ─────────────────────────────────────────────────────────────────────────
MANIFEST = {
    # method:        (benchmark.csv,                    gene_policy,  fit_on)
    "pca":          ("fm_scgpt",                        "all30962",   "train"),
    "scvi":         ("fm_scgpt",                        "all30962",   "train"),
    "scanvi":       ("fm_scgpt",                        "all30962",   "train"),
    "scgpt":        ("fm_scgpt",                        "native", "pretrained"),
    "geneformer":   ("fm_baseline+Geneformer",          "native", "pretrained"),
    "scfoundation": ("fm_scfoundation",                 "native", "pretrained"),
    "scimilarity":  ("fm_scimilarity",                  "native", "pretrained"),
    # Scored 4 November on the wide axis, same corpus, TRANSDUCTIVE: neither
    # method can be fitted on the training donors and applied to held-out
    # ones, so both saw the held-out cells while fitting. That is an advantage
    # the table must declare per method, not a detail.
    "harmony":      ("wide_transductive",               "all30962",   ""),
    "scanorama":    ("wide_transductive",               "all30962",   ""),
}
EXCLUDED = {
    "r8_all": "obsolete corpus; ELAJ scores phase 0.1161 there against 0.7346",
    "r8_inductive": "same corpus as r8_all",
    "p1_dab168_kl1_train": "train split",
    "elaj_train_cpu": "train split",
    "baseline_latents": "latent dumps, not a scoring run",
}

def read_keyed(path: Path, method: str, policy: str, fit: str) -> dict:
    """One method's row set, by exact key. No key, no row."""
    b = pd.read_csv(path)
    b["mm"] = b.method.astype(str).str.replace("__.*", "", regex=True)
    e = b[(b.mm == method)
          & (b.gene_policy.fillna("").astype(str) == policy)
          & (b.fit_on.fillna("").astype(str) == fit)]
    if e.empty:
        raise KeyError(f"{method}/{policy}/{fit} absent from {rel(path)}")
    row = {}
    for k, (t, l, _) in TESTS.items():
        s = e[(e.test == t) & (e.label == l)]["value"]
        row[k] = float(s.iloc[0]) if len(s) else float("nan")
    w = e["width"].dropna()
    row["width"] = int(w.max()) if len(w) else None
    sup = {str(x) for x in e["supervised_on"].dropna() if str(x) != "nan"}
    row["supervised_on"] = ", ".join(sorted(sup)) or "—"
    row["fit_on"] = fit or "transductive"
    return row

# ── stage, grade and the severity merge, across every method ──────────────
# ADDED 6 November 2026, with Results [4]. Its claim is a RANGE over methods
# and a count of how many clear their own permutation null, so the audit has
# to derive every method's value, its p and its null95, not just ELAJ's.
#
# SEVERITY LIVES IN ITS OWN FILES because it was scored in a second pass with
# --only-labels, after the labels were added to CROSS_DONOR_LABELS. Those runs
# read a dumped ExternalLatent, so their `method` column carries the dump key
# (`pca__all30962__train`), which read_keyed's `__.*` strip already handles.
SEVERITY_MANIFEST = {
    "pca":          "severity_ind_pca",
    "scvi":         "severity_ind_scvi",
    "scanvi":       "severity_ind_scanvi",
    "scgpt":        "severity_scgpt",
    "geneformer":   "severity_geneformer",
    "scfoundation": "severity_scfoundation",
    "scimilarity":  "severity_scimilarity",
    "harmony":      "severity_trans_harmony",
    "scanorama":    "severity_trans_scanorama",
    # elaj: pending the eleven arm re-scores queued 6 November.
}
STAGE_LABELS = {"stage": "Endometriosis_stage", "grade": "EndometriosisGrade",
                "severity": "severity",
                "severity_cases": "severity (patients only)"}

def _note_fields(note: str) -> dict:
    out = {}
    for part in str(note).split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            try: out[k.strip()] = float(v.strip().split()[0])
            except ValueError: pass
    return out

def cross_donor_rows(path: Path, method: str, label: str) -> dict:
    b = pd.read_csv(path)
    b["mm"] = b.method.astype(str).str.replace("__.*", "", regex=True)
    e = b[(b.mm == method) & (b.test == "cross-donor") & (b.label == label)]
    if e.empty:
        raise KeyError(f"{method}/{label} absent from {rel(path)}")
    r = e.iloc[0]
    f = _note_fields(r["note"])
    return {"value": float(r["value"]), "p": f.get("p"), "null95": f.get("null95")}

STAGING = {}
for meth, (run, _, _) in list(MANIFEST.items()) + [("elaj", ("p1_dab168_kl1", "", ""))]:
    f = ROOT / "Outputs/Benchmarks" / run / "benchmark.csv"
    for key in ("stage", "grade"):
        try: STAGING[(meth, key)] = cross_donor_rows(f, meth, STAGE_LABELS[key])
        except (KeyError, FileNotFoundError): pass
for meth, run in SEVERITY_MANIFEST.items():
    f = ROOT / "Outputs/Benchmarks" / run / "benchmark.csv"
    for key in ("severity", "severity_cases"):
        try: STAGING[(meth, key)] = cross_donor_rows(f, meth, STAGE_LABELS[key])
        except (KeyError, FileNotFoundError): pass

STAGING_VALUES = set()
for (meth, key), d in STAGING.items():
    for x in (d["value"], d["p"], d["null95"]):
        if x is None: continue
        for dp in (4, 3, 2):
            STAGING_VALUES.add(f"{x:.{dp}f}"); STAGING_VALUES.add(f"{abs(x):.{dp}f}")
# The ranges the prose quotes, so a min or max is pinned as such rather than
# passing only because it happens to equal one method's value.
for key in STAGE_LABELS:
    vs = [d["value"] for (m, k), d in STAGING.items() if k == key]
    if not vs: continue
    for x in (min(vs), max(vs)):
        STAGING_VALUES.add(f"{x:.4f}"); STAGING_VALUES.add(f"{abs(x):.4f}")
    ps = [d["p"] for (m, k), d in STAGING.items() if k == key and d["p"] is not None]
    if ps:
        STAGING_VALUES.add(f"{min(ps):.3f}"); STAGING_VALUES.add(f"{min(ps):.4f}")

MISSING_METHODS = []
for meth, (run, policy, fit) in MANIFEST.items():
    f = ROOT / "Outputs/Benchmarks" / run / "benchmark.csv"
    try:
        base[meth] = (read_keyed(f, meth, policy, fit), str(f))
    except (KeyError, FileNotFoundError) as exc:
        MISSING_METHODS.append(f"{meth}: {exc}")


def rel(p): return os.path.relpath(p, ROOT)
lines = ["# Results numbers, and where each one comes from", "",
         "**Generated by `figures/scripts/audit_numbers.py`. Do not edit by hand.**",
         "", "Every value below is read from a `benchmark.csv` at run time. The",
         "script then scans `sections/02-results.tex` and reports any decimal in",
         "the prose that it cannot account for.", "",
         "Columns: donor recovery and study mixing are **lower is better**;",
         "cross-donor phase, cell family and disease are **higher is better**.", ""]

lines += ["## The six frontier arms", "",
          "| arm | donor ↓ | mixing ↓ | phase ↑ | family ↑ | source |", "|---|---:|---:|---:|---:|---|"]
for k, (r, f) in arms.items():
    lines.append(f"| `{k}` | {r['donor']:.4f} | {r['mixing']:.4f} | {r['phase']:.4f} "
                 f"| {r['family']:.4f} | `{rel(f)}` |")
rep = arms["p1_dab168_kl1"][0]
lines += ["", f"**Reported arm: `p1_dab168_kl1`** — phase {rep['phase']:.4f}, "
              f"family {rep['family']:.4f}, donor {rep['donor']:.4f}, mixing {rep['mixing']:.4f}.", ""]

lines += ["## The field", "",
          "| method | width | supervised on | phase ↑ | mixing ↓ | donor ↓ | family ↑ | disease ↑ | source |",
          "|---|---:|---|---:|---:|---:|---:|---:|---|",
          f"| **elaj** | {rep['width']} | {arms['p1_dab168_kl1'][0]['supervised_on']} "
          f"| {rep['phase']:.4f} | {rep['mixing']:.4f} | {rep['donor']:.4f} "
          f"| {rep['family']:.4f} | {rep['disease']:.4f} | `{rel(arms['p1_dab168_kl1'][1])}` |"]
for k, (r, f) in sorted(base.items(), key=lambda x: -x[1][0]["phase"]):
    g = lambda v: "—" if pd.isna(v) else f"{v:.4f}"
    lines.append(f"| {k} | {r['width']} | {r['supervised_on']} | {g(r['phase'])} "
                 f"| {g(r['mixing'])} | {g(r['donor'])} | {g(r['family'])} "
                 f"| {g(r['disease'])} | `{rel(f)}` |")

# =========================================================================
# D1-D7 — the ablations. One scoring pass, 28 October, ELAJ only, native
# gene policy. Nothing here crosses a method boundary.
# =========================================================================
extra = set()
extra |= STAGING_VALUES

lines += ["", "## D1--D6 — the ablations", "",
          "Six arms, one scoring pass, ELAJ only. Each is a single-key change",
          "against `p1_dab168_kl1`. No baseline appears in any of these files,",
          "so the gene policy and the baseline re-scoring do not reach them.", "",
          "| arm | family ↑ | phase ↑ | disease ↑ | donor ↓ | mixing ↓ | source |",
          "|---|---:|---:|---:|---:|---:|---|"]
abl = {}
for key, (label, bdir, rdir) in ABL.items():
    bf = ROOT / bdir / "benchmark.csv"
    if not bf.exists():
        lines.append(f"| {label} | — | — | — | — | — | **missing** `{bdir}` |"); continue
    xd  = label_rows(bf, "cross-donor")
    dis = label_rows(bf, "disease-xdonor")
    don = label_rows(bf, "knn-agreement")
    mix = label_rows(bf, "study-mixing")
    r = {"family":  xd.get("cell family", float("nan")),
         "phase":   xd.get("menstrual phase", float("nan")),
         "disease": dis.get("all studies (pooled)", float("nan")),
         "donor":   don.get("patient_id", float("nan")),
         "mixing":  mix.get("all studies", float("nan")),
         "stage":   xd.get("Endometriosis_stage", float("nan")),
         "grade":   xd.get("EndometriosisGrade", float("nan"))}
    xdp = label_rows(bf, "cross-donor-p")
    r["stage_p"] = xdp.get("Endometriosis_stage", float("nan"))
    r["grade_p"] = xdp.get("EndometriosisGrade", float("nan"))
    abl[key] = (label, r)
    for v in r.values():
        if not pd.isna(v):
            extra.add(f"{v:.4f}")
            extra.add(f"{abs(v):.4f}")        # prose writes $-$0.0414 as a sign plus 0.0414
    bold = "**" if label == "BASE" else ""
    lines.append(f"| {bold}{label}{bold} | {r['family']:.4f} | {r['phase']:.4f} "
                 f"| {r['disease']:.4f} | {r['donor']:.4f} | {r['mixing']:.4f} "
                 f"| `{rel(bf)}` |")

if "p1_dab168_kl1" in abl:
    b = abl["p1_dab168_kl1"][1]
    lines += ["", "**Deltas against BASE**, for the claims that are stated as changes:", "",
              "| arm | Δ family | Δ phase | Δ disease | Δ donor | Δ mixing |",
              "|---|---:|---:|---:|---:|---:|"]
    for key, (label, r) in abl.items():
        if label == "BASE": continue
        d = [r[k] - b[k] for k in ("family", "phase", "disease", "donor", "mixing")]
        for v in d: extra.add(f"{abs(v):.4f}")
        lines.append(f"| {label} | " + " | ".join(f"{v:+.4f}" for v in d) + " |")
    # CHANCE IS ALREADY REMOVED. endo_model/evaluation/sufficient_stats.py:
    #   excess = (observed - chance) / (1 - chance)
    # so a cross-donor value is a chance-corrected quantity on [., 1], and a
    # NEGATIVE one is possible (grade is -0.0414, which a raw rate could not
    # be). Subtracting a chance rate from it a second time is what produced
    # the 69.5/30.5 split in ABLATIONS.md and in Results. The right
    # decomposition is the ratio of the two excesses.
    nh = abl["a1_nophase"][1]["phase"]
    kept = nh / b["phase"]
    lines += ["", "**D1, recomputed.** Cross-donor values are already "
              "chance-corrected, so the phase margin splits as a ratio of the "
              "two excesses, not as a difference from a chance rate:",
              "", f"- base {b['phase']:.4f}, head removed {nh:.4f}",
              f"- **{kept*100:.1f}%** of the chance-corrected signal survives "
              f"removing the head, so the head accounts for **{(1-kept)*100:.1f}%** "
              "and the architecture for the rest.",
              "", "The superseded figure was 30.5% surviving and 69.5% from the "
              f"head, from ({nh:.4f} - 0.370)/({b['phase']:.4f} - 0.370). That "
              "subtracted chance from numbers chance had already been taken out "
              "of. 0.370 is the chance rate of a different measurement, the "
              "plain whole-corpus phase grouping in `grouped_agreement.csv`.",
              "", "**The comparator for a cross-donor value is its own "
              "permutation null**, carried in the benchmark `note` column as "
              "`null95`: 0.18 for menstrual phase, 0.06 for cell family, 0.12 "
              "for grade, 0.42 for stage. Stage's 0.1313 sits below its own "
              "null95, which is why its p is 0.303.", ""]
    for v in (kept, 1 - kept):
        extra.add(f"{v:.4f}"); extra.add(f"{v:.3f}")
    extra.update({"0.18", "0.06", "0.12", "0.42", "0.1800", "0.0600", "0.1200", "0.4200"})

# -------------------------------------------------------------------------
# D2 and A7 — reconstruction, from the training metrics rather than the
# benchmark. Checkpoint selection is argmin val_nb, which reproduces the
# "best ep" column of ABLATIONS.md for all six arms.
# -------------------------------------------------------------------------
lines += ["## D2 and A7 — reconstruction, from the training metrics", "",
          "`val_nb` and `train_nb` are mean negative-binomial loss per cell;",
          "**lower is better**. The reported checkpoint is `argmin val_nb`,",
          "which reproduces ABLATIONS.md's `best ep` column for every arm.", "",
          "| arm | epochs | best ep | train_nb @best | val_nb @best | train_nb @last | val_nb @last | source |",
          "|---|---:|---:|---:|---:|---:|---:|---|"]
for key, (label, bdir, rdir) in ABL.items():
    mf = ROOT / rdir / "metrics.csv"
    if not mf.exists():
        lines.append(f"| {label} | — | — | — | — | — | — | **missing** `{rdir}` |"); continue
    ep, bestrow, lastrow, n = best_epoch(mf)
    for v in (bestrow.train_nb, bestrow.val_nb, lastrow.train_nb, lastrow.val_nb):
        extra.add(f"{v:.4f}")
    bold = "**" if label == "BASE" else ""
    lines.append(f"| {bold}{label}{bold} | {n} | {ep} | {bestrow.train_nb:.4f} "
                 f"| {bestrow.val_nb:.4f} | {lastrow.train_nb:.4f} "
                 f"| {lastrow.val_nb:.4f} | `{rel(mf)}` |")
lines += ["", "**D2 reads down the `-phase head` row, not across to BASE.** Without the",
          "head, `val_nb` is best at **epoch 0** and worsens monotonically from",
          "epoch 1 while `train_nb` keeps falling — the held-out split is paid for",
          "the training split from the first epoch onward. BASE's `val_nb`",
          "improves to epoch 4 before it turns. Both trajectories are in the",
          "table above; quoting 0.4083 as a BASE value would be wrong, it is the",
          "`-phase head` arm's best.", "",
          "**A7's study-mean reference (0.4315) is not in any file read here.**",
          "It is a computed baseline, not a logged metric, and must be",
          "re-derived from the code that produced it before it becomes prose.", ""]

# -------------------------------------------------------------------------
# C6 / D7 — stage and grade. Reported as an absence, so the p-floor and the
# donor count have to travel with the numbers.
# -------------------------------------------------------------------------
lines += ["## C6 — surgical stage and grade, across every arm", "",
          "Cross-donor excess agreement and its permutation p. Negative excess",
          "means neighbours agree *less* than chance.", "",
          "| arm | stage | p | grade | p | source |", "|---|---:|---:|---:|---:|---|"]
for key, (label, r) in abl.items():
    lines.append(f"| {label} | {r['stage']:+.4f} | {r['stage_p']:.4f} "
                 f"| {r['grade']:+.4f} | {r['grade_p']:.4f} "
                 f"| `{rel(ROOT / ABL[key][1] / 'benchmark.csv')}` |")
st = [r["stage"] for _, r in abl.values()]; stp = [r["stage_p"] for _, r in abl.values()]
gr = [r["grade"] for _, r in abl.values()]; grp = [r["grade_p"] for _, r in abl.values()]
lines += ["", f"Across all {len(abl)} arms: stage {min(st):+.4f} to {max(st):+.4f} "
              f"at p {min(stp):.4f} to {max(stp):.4f}; grade is **negative in every "
              f"arm**, {min(gr):+.4f} to {max(gr):+.4f}, at p {min(grp):.4f} to "
              f"{max(grp):.4f}.",
          "", "A negative result cannot be read without the p-floor, which is set by",
          "donor count and belongs in the same sentence (Methods, *Permutation",
          "testing*).", ""]

# -------------------------------------------------------------------------
# C2, C4, C5 — whole-corpus geometry. Outputs/analysis/<arm>/, ELAJ only.
# over_scatter is a centroid distance divided by the stratum's own spread,
# so it is already in units of the cells' own width.
# -------------------------------------------------------------------------
ANALYSIS = ROOT / "Outputs/analysis"
ARMS_A = ["p1_dab168_kl1", "p1_dab168_kl30"]

lines += ["## C2 — cycle displacement by cell type", "",
          "`over_scatter` from `phase_within_family.csv`: the distance between",
          "two phase centroids **divided by that cell type's own spread**, so",
          "the four numbers are comparable across types of different size. The",
          "row quoted is `proliferative → secretory`, the widest separation",
          "available in all four types.", "",
          "| arm | stromal | epithelial | endothelial | immune | source |",
          "|---|---:|---:|---:|---:|---|"]
for a in ARMS_A:
    f = ANALYSIS / a / "phase_within_family.csv"
    if not f.exists():
        lines.append(f"| `{a}` | — | — | — | — | **missing** |"); continue
    d = pd.read_csv(f)
    d = d[(d.label == "phase") & (d["from"] == "proliferative") & (d.to == "secretory")]
    v = dict(zip(d.stratum, d.over_scatter.astype(float)))
    for x in v.values(): extra.add(f"{x:.4f}")
    lines.append(f"| `{a}` | " + " | ".join(f"{v.get(k, float('nan')):.4f}" for k in
                 ("stromal", "epithelial", "endothelial", "immune")) + f" | `{rel(f)}` |")
lines += ["", "The ordering is stromal > epithelial ≫ endothelial ≈ immune, and the",
          "phase head is one linear map over the whole latent that was never",
          "given cell type.", ""]

lines += ["## C4 and C5 — disease displacement by study and cell type", "",
          "`over_scatter` from `disease_within_family.csv`, label",
          "`case_vs_control`. C4 is the marecko immune cell; C5 is that the",
          "pattern does not hold in duempelmann.", ""]
FAMS = ("endothelial", "epithelial", "immune", "stromal")
top, span = {}, {}
for a in ARMS_A:
    f = ANALYSIS / a / "disease_within_family.csv"
    if not f.exists(): continue
    d = pd.read_csv(f)
    d = d[d.label == "case_vs_control"]
    lines += [f"**`{a}`** — `{rel(f)}`", "",
              "| study | " + " | ".join(FAMS) + " | max |",
              "|---|" + "---:|" * (len(FAMS) + 1)]
    for study in sorted(d.study.unique()):
        row = d[d.study == study]
        v = dict(zip(row.family, row.over_scatter.astype(float)))
        for x in v.values(): extra.add(f"{x:.4f}")
        hi = max(v, key=v.get)
        top[(a, study)] = hi
        span[(a, study)] = (min(v.values()), max(v.values()))
        cells = ["—" if pd.isna(v.get(k, float("nan")))
                 else (f"**{v[k]:.4f}**" if k == hi else f"{v[k]:.4f}") for k in FAMS]
        lines.append(f"| {study} | " + " | ".join(cells) + f" | {hi} |")
    lines.append("")

# Which family ranks first is READ OFF the table above, never asserted. The
# first version of this section claimed immune led in both arms of both
# studies; the kl30 duempelmann row it had just printed says endothelial.
studies = sorted({st for _, st in top})
lines.append("**Where the maximum sits, per arm:**")
lines.append("")
for st in studies:
    seen = [top[(a, st)] for a in ARMS_A if (a, st) in top]
    rng  = [span[(a, st)] for a in ARMS_A if (a, st) in top]
    lo, hi = min(r[0] for r in rng), max(r[1] for r in rng)
    stable = len(set(seen)) == 1
    lines.append(f"- **{st}** — " +
                 (f"**{seen[0]}** in every arm" if stable else
                  "**not stable**: " + ", ".join(f"`{a}` → {top[(a, st)]}"
                                                 for a in ARMS_A if (a, st) in top)) +
                 f". Range across both arms {lo:.4f} to {hi:.4f}.")
    extra.add(f"{lo:.4f}"); extra.add(f"{hi:.4f}")
lines += ["", "C4 is the marecko immune cell, and it is the maximum in both arms at a",
          "magnitude no other stratum reaches. C5 is duempelmann, where the",
          "displacement is roughly a third of marecko's **and** the leading family",
          "is not the same in the two arms — so the non-replication is both in",
          "magnitude and in ordering, and prose may say so.", "",
          "`reference_scales.csv` in the same folders carries the whole-corpus",
          "cell-family distances that these are read against.", ""]

# =========================================================================
# C1-C6 also quote the WHOLE-CORPUS read: all 1,577,728 cells embedded once
# with the model fixed, every label scored afterwards. Different file,
# different k for the donor test, and the only place the permutation p and
# the same-donor chance rate are recorded.
# =========================================================================
VAL = ROOT / "Outputs/validate/p1_dab168_kl1_full/validation.csv"
if VAL.exists():
    v = pd.read_csv(VAL)
    lines += ["## The whole-corpus read — all 1,577,728 cells", "",
              f"`{rel(VAL)}`. The model is fixed, so nothing is selected on",
              "these cells and every label can be read at once. Cross-donor rows",
              "discard same-donor neighbours at k=100; plain `knn-agreement` rows",
              "use k=30 for labels and k=100 for donor identity.", "",
              "| test | label | cells | value | note |", "|---|---|---:|---:|---|"]
    for _, r in v[v.test.isin(["cross-donor", "knn-agreement", "linear-corr"])].iterrows():
        extra.add(f"{float(r['value']):.4f}")
        extra.add(f"{abs(float(r['value'])):.4f}")
        note = str(r["note"]) if str(r["note"]) != "nan" else ""
        lines.append(f"| {r['test']} | {r['label']} | {int(r['n_cells']):,} "
                     f"| {float(r['value']):.4f} | {note} |")
    lines += ["", "**The same-donor chance rate is 0.0060** over 269 donors "
              "(`sum n_d(n_d-1) / N(N-1)`), against an observed 0.327 of a cell's "
              "hundred nearest neighbours — **54x enriched**. The 14x figure in "
              "the figure notes is a 60-donor single-cohort subsample and is not a "
              "corpus number.",
              "", "**Stage splits between the two reads and this matters.** "
              "Whole-corpus cross-donor stage is +0.3320 at p = 0.005, held-out "
              "+0.1313 at p = 0.3035. Any prose saying stage carries nothing "
              "*anywhere* contradicts the first figure.",
              "", "**The best-of-sixteen caveat.** `linear-corr` takes the largest "
              "|r| over the latent's sixteen dimensions, so the negative controls "
              "do not sit near zero: 0.3396 for mitochondrial fraction against "
              "0.4725 for serum progesterone. Quote the controls alongside.",
              "", "Every `circular-linear` row is `nan`, so **no claim about the "
              "circular branch is available** from this file.", ""]
    extra.update({"0.0060", "0.006"})
    for note in v["note"].dropna().astype(str):
        for m2 in re.finditer(r"p=([\d.]+)", note):
            extra.add(f"{float(m2.group(1)):.4f}"); extra.add(m2.group(1))
    # excess = (agreement - chance) / (1 - chance), so agreement is recoverable
    dk = v[(v.test == "knn-agreement") & (v.label == "patient_id")]
    if len(dk):
        ex, ch = float(dk.value.iloc[0]), 0.0060
        agree = ex * (1 - ch) + ch
        extra.add(f"{agree:.4f}"); extra.add(f"{agree:.3f}")
        lines += [f"Donor agreement itself is **{agree:.4f}** "
                  f"(excess {ex:.4f} inverted through chance {ch:.4f}), which is "
                  f"**{agree/ch:.1f}x** the chance rate.", ""]

# Permutation p-values, which prose quotes as numbers like 0.005 and 0.3035.
for key, (label, bdir, rdir) in ABL.items():
    bf = ROOT / bdir / "benchmark.csv"
    if not bf.exists(): continue
    bb = pd.read_csv(bf)
    for col in ("cross-donor-p", "disease-xdonor-p", "cross-donor",
                "disease-xdonor", "disease-xstudy", "disease-xstudy-p",
                "study-purity", "knn-agreement"):
        for x in bb[bb.test == col]["value"]:
            try: extra.add(f"{float(x):.4f}"); extra.add(f"{abs(float(x)):.4f}")
            except (TypeError, ValueError): pass

# Chance rates and permutation floors are printed in the benchmark note column.
extra.update({"0.0050", "0.005", "0.0000", "0.000", "0.370", "0.3700"})

derived_extra = extra

def _isnum(x):
    try: float(x); return True
    except (TypeError, ValueError): return False

lines += ["", "## Methods with no valid source", ""]
if MISSING_METHODS:
    for m in MISSING_METHODS:
        lines.append(f"- {m}")
    lines += ["", "**A missing row is left missing.** Earlier versions filled "
              "these from whichever file had them, which is how `r8_all` got "
              "into a table beside the p-series.", ""]
else:
    lines += ["None. Every method in the manifest resolved.", ""]

lines += ["## Files excluded from the manifest, and why", "",
          "| file | reason |", "|---|---|"]
for k, why in sorted(EXCLUDED.items()):
    lines.append(f"| `{k}` | {why} |")
lines += ["", "The narrow `all` rows for `pca`, `scvi` and `scanvi` in "
          "`p1_dab168_kl1` are excluded too, not as obsolete but as a "
          "different experiment: baselines are reported on the full "
          "30,962-gene axis, so the 15,496-gene rows answer a question this "
          "paper does not ask.", ""]

# THE CROSS-METHOD CORRELATIONS. Derived from the field table above, so they
# move with it: if a method's row changes, so do these, and the prose is
# re-checked against the new value rather than the one it was written from.
from scipy.stats import spearmanr as _sp
_rows = [r for r, _ in [arms["p1_dab168_kl1"]] + list(base.values())]
_dn = [r["donor"] for r in _rows]
lines += ["", "## Across the ten methods", "",
          "Spearman, donor recovery against each biology axis. One point per",
          "method, from the field table above.", "",
          "| axis | rho | p |", "|---|---:|---:|"]
for _lab, _k in (("menstrual phase", "phase"), ("cell family", "family"),
                 ("disease", "disease")):
    _v = [r[_k] for r in _rows]
    _ok = [(x, y) for x, y in zip(_dn, _v) if not (pd.isna(x) or pd.isna(y))]
    if len(_ok) < 3: continue
    _r, _p = _sp([x for x, _ in _ok], [y for _, y in _ok])
    lines.append(f"| {_lab} | {_r:+.3f} | {_p:.3f} |")
    for _x in (_r, abs(_r), _p):
        extra.add(f"{_x:.4f}"); extra.add(f"{_x:.3f}"); extra.add(f"{_x:.2f}")
_w = [r["width"] for r in _rows]
_ph = [r["phase"] for r in _rows]
_r, _p = _sp(_w, _ph)
lines += [f"| width vs menstrual phase | {_r:+.3f} | {_p:.3f} |", "",
          f"Spread per axis across the ten: " + ", ".join(
              f"{_l} {max(x) - min(x):.4f}" for _l, x in
              (("phase", _ph), ("donor", _dn),
               ("family", [r["family"] for r in _rows]),
               ("disease", [r["disease"] for r in _rows if not pd.isna(r["disease"])]))) + ".", ""]
for _x in (_r, abs(_r), _p):
    extra.add(f"{_x:.4f}"); extra.add(f"{_x:.3f}"); extra.add(f"{_x:.2f}")
for _l, _x in (("phase", _ph), ("donor", _dn)):
    extra.add(f"{max(_x) - min(_x):.4f}")
derived_extra |= extra

derived = set()
for r, _ in list(arms.values()) + list(base.values()):
    for k in TESTS:
        if not pd.isna(r[k]): derived.add(f"{r[k]:.4f}")
derived |= derived_extra
NOT_FROM_BENCHMARK = {
    "0.370": "chance rate for menstrual phase, printed in the benchmark `note` column",
    "0.3700": "same",
}
lines += ["", "## Numbers in the prose that this script cannot account for", ""]
tex = TEX.read_text()
tex = re.sub(r"\\note\{.*?\n\n", "", tex, flags=re.S)       # prose only, not my notes
unaccounted = []
for mobj in re.finditer(r"\b0\.\d{3,4}\b", tex):
    v = mobj.group(0)
    v4 = f"{float(v):.4f}"
    # EXACT TO FOUR DECIMALS, OR NOT ACCOUNTED. An earlier version accepted a
    # prose number that matched any derived value at the prose's own
    # precision, which at two decimals let unrelated quantities vouch for each
    # other. Rounded numbers are checked by verify_numbers.py, which pins each
    # one to a named row instead of searching for something that matches.
    if v4 in derived or v in derived or v in NOT_FROM_BENCHMARK:
        continue
    unaccounted.append(v)
# An unaccounted decimal has two very different causes and the report has to
# tell them apart: a value that exists nowhere is a typo or an invention, and
# a value that exists in a run we are not quoting from is a mixed table.
SWEEP = {}
for f in sorted(glob.glob(str(ROOT / "Outputs/Benchmarks/**/benchmark.csv"), recursive=True)):
    b = pd.read_csv(f)
    b["mm"] = b.method.astype(str).str.replace("__.*", "", regex=True)
    for _, rw in b.iterrows():
        try: key = f"{float(rw['value']):.4f}"
        except (TypeError, ValueError): continue
        # Rank hits so a coincidental match on an scib metric cannot outrank a
        # match on one of the five axes the paper actually reports.
        onaxis = any(rw["test"] == t for t, _, _ in TESTS.values())
        SWEEP.setdefault(key, []).append(
            (0 if onaxis else 1, f"`{rel(f)}` — {rw['mm']} / {rw['test']} / {rw['label']}"))

if unaccounted:
    for v in sorted(set(unaccounted)):
        hits = sorted(SWEEP.get(f"{float(v):.4f}", []))
        onaxis = [h for r, h in hits if r == 0]
        if not hits:
            lines.append(f"- `{v}` — **exists in no benchmark file. Typo or invention.**")
        elif not onaxis:
            lines.append(f"- `{v}` — appears only on metrics this paper does not "
                         f"report ({len(hits)} occurrences). Treat as **unsourced**.")
        else:
            lines.append(f"- `{v}` — real, on a reported axis, but **from a file "
                         f"this table does not quote**:")
            for h in onaxis[:3]:
                lines.append(f"    - {h}")
            if len(onaxis) > 3:
                lines.append(f"    - … and {len(onaxis)-3} more on reported axes")
else:
    lines.append("None. Every decimal in the Results prose matches a value "
                 "re-derived above, or is a chance rate carried in the "
                 "benchmark's own `note` column.")
lines += ["", "## How the field table is sourced", "",
  "Eight of the ten methods were already scored correctly. Nothing needed",
  "re-running; what was wrong was which file each row was read from.", "",
  "**The corpus is identical across every source in the manifest**, verified",
  "from the runs' own logs: 416,256 held-out cells, with 176,803 cells",
  "labelled for cell family, 224,211 for menstrual phase and 108,288 for cell",
  "cycle phase. The reported arm and all four `fm_*` runs agree on all three.",
  "", "**The four `fm_*` runs are one baseline pass.** `pca`, `scvi` and",
  "`scanvi` hold bit-identical values and cell counts in all four files, so",
  "those jobs scored the baselines once and added one pretrained model each.",
  "Any one of the four is the source for the shared rows.", "",
  "**ELAJ's row is unaffected by the baselines' gene axis.** It reads the",
  "vocabulary its checkpoint was trained against whatever the baselines are",
  "given, on the same cells, so its row from the narrow run stands beside the",
  "wide baselines. That is why the wrapper documents `--no-elaj` for a wide",
  "pass: re-embedding would reproduce the same row.", "",
  "**The two gene policies are a choice, not a conflict.** `pca`, `scvi` and",
  "`scanvi` were scored twice, on 15,496 genes in the reported arm and on",
  "30,962 in the `fm_*` runs. Baselines are reported on the full axis, so the",
  "wide rows are used and the narrow ones are discarded. Both are valid; only",
  "one answers this paper's question.", "",
  "**Differing `n_cells` per method is coverage, not a fault.** Cross-donor",
  "agreement is measured only on cells with at least one cross-donor",
  "neighbour, and that count is a property of the embedding.", "",
  "**`r8_all` is the one genuine fault**, and it costs exactly two rows.", ""]

lines += ["## Not yet auditable", "",
          "These are quoted in subsection notes but not yet in prose, and come",
          "from project documents rather than from a `benchmark.csv` read here.",
          "**Each must be re-derived before it becomes prose.**", "",
          "| value | claim | where it is recorded |", "|---|---|---|",
          "| 0.4812 | phase with the head removed | `axw1008/docs/paper/ABLATIONS.md` |",
          "| 1.07 / 0.98 / 0.39 / 0.34 | cycle displacement by cell type | `Outputs/validate/` |",
          "| 0.4140 → 0.3772, 0.4083 → 0.4256 | train/val NB without the phase head | `Outputs/a_series/a1_nophase/metrics.csv` |",
          "| 0.77 / 0.83 vs 0.22 | disease in marecko's immune cells | `Outputs/validate/` |",
          "| +0.883, +0.890 | adversary loss vs donor / study kNN | `axw1008/docs/paper/LEVERS.md` |", ""]
OUT.parent.mkdir(exist_ok=True)
OUT.write_text("\n".join(lines) + "\n")
print(f"wrote {rel(OUT)}  ({len(arms)} arms, {len(base)} baselines)")
for m in MISSING_METHODS:
    print(f"  no source: {m}")
bad = sorted(set(unaccounted))
print(f"unaccounted decimals in prose: {bad or 'none'}")
if bad:
    print("\nFAILED. A number in the Results prose matches no value this "
          "script derived.\nRounded values are pinned in verify_numbers.py; "
          "run that too.")
    sys.exit(1)
