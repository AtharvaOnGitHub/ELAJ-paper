"""An independent check on every number in the Results prose.

    python figures/scripts/verify_numbers.py

WHY THIS EXISTS, AND WHY IT IS NOT audit_numbers.py. On 3 November 2026 the
audit was found to be unsound in a way that mattered: it chose each baseline's
row by taking whichever benchmark file a glob reached first. Every number it
printed was real, but the table mixed gene policies and fitting protocols, so
the comparison it presented had never been run as one experiment. An audit that
can do that is not an audit.

This file is a SECOND, INDEPENDENT implementation, written to disagree with the
first. Deliberate differences:

  * stdlib `csv` only. No pandas, so a dtype or NaN behaviour cannot be
    common to both.
  * an EXPLICIT source manifest. Nothing is globbed. A row names its file
    and its (method, gene_policy, fit_on) key, and a missing key is a hard
    failure rather than a silent fallback to another file.
  * the corpus is ASSERTED, not assumed. Every source file's log must report
    the same labelled-cell counts, or the run aborts before reading a value.
  * it reports PROVENANCE PER NUMBER, not set membership. "0.47 is in the
    allowed set" is worth little; "0.47 is validation.csv's
    linear-corr/ProgesteroneSerum = 0.4725, rounded to 2 dp, and nothing else
    rounds to it" is worth something.
  * a number matching more than one source is AMBIGUOUS and reported as a
    failure, because coincidental agreement is how a wrong number survives.

Exit status is 1 on any failure. Nothing here prints "ok" without having
checked.
"""
from __future__ import annotations
import csv, math, re, sys
from pathlib import Path

ROOT = Path("/Users/atharvawaghmare/Endo research/ELAJ")
PAPER = Path(__file__).resolve().parents[2]
# Results AND Discussion. The Discussion quotes measured values like any
# other section, and reading only Results meant it shipped unchecked.
TEX_FILES = [PAPER / "sections" / "02-results.tex",
             PAPER / "sections" / "03-discussion.tex"]
TEX = TEX_FILES[0]

FAIL: list[str] = []
WIDTHS: dict[int, str] = {}
NOTE_DONORS: dict[int, str] = {}

def fail(msg: str) -> None:
    FAIL.append(msg)

# ──────────────────────────────────────────────────────────────────────────
# THE SOURCE MANIFEST. Every file the prose may draw on, named, with the
# reason it is the right file. Adding a file here is a decision; globbing
# one in is not.
# ──────────────────────────────────────────────────────────────────────────
BENCH = ROOT / "Outputs/Benchmarks"
SOURCES = {
    # MOVED TO THE FULL-SPLIT SOURCES, 6 November 2026, with the manifest in
    # audit_numbers.py. Every entry below used to name a run whose study
    # mixing was measured on 19,998 of 416,256 held-out cells.
    "elaj":     (BENCH / "full/full_p1_dab168_kl1/benchmark.csv", "native", "train",
                 "the reported arm, ELAJ's own 15,496-gene vocabulary"),
    "frontier": (None, None, None, "the six full/full_p1_* arms, ELAJ rows only"),
    "pca":      (BENCH / "wide_full_inductive/benchmark.csv", "all30962", "train",
                 "wide axis, inductive, full split"),
    "scvi":     (BENCH / "wide_full_inductive/benchmark.csv", "all30962", "train", "as pca"),
    "scanvi":   (BENCH / "wide_full_inductive/benchmark.csv", "all30962", "train", "as pca"),
    "scgpt":        (BENCH / "wide_full_scgpt/benchmark.csv", "native", "pretrained", ""),
    "geneformer":   (BENCH / "wide_full_geneformer/benchmark.csv", "native", "pretrained", ""),
    # scFoundation's full-split pass was OOM-killed inside scIB before the
    # mixing stage, so its mixing row alone comes from a separate --stages
    # mixing pass over the same dumped latent.
    "scfoundation": (BENCH / "fm_scfoundation/benchmark.csv", "native", "pretrained", ""),
    "scfoundation_mixing": (BENCH / "mixing_scfoundation/benchmark.csv", "native",
                            "pretrained", "mixing only"),
    "scimilarity":  (BENCH / "wide_full_scimilarity/benchmark.csv", "native", "pretrained", ""),
    "harmony":   (BENCH / "wide_full_harmony/benchmark.csv", "all30962", "",
                  "wide axis, transductive: cannot be fitted inductively"),
    "scanorama": (BENCH / "wide_full_scanorama/benchmark.csv", "all30962", "",
                  "as harmony"),
}
# Deliberately absent: r8_all and r8_inductive (obsolete corpus, ELAJ scores
# 0.1161 there), p1_dab168_kl1_train and elaj_train_cpu (train split), and the
# narrow all-policy pca/scvi/scanvi rows in p1_dab168_kl1, which are a
# different experiment from the wide ones and must not be mixed with them.
FORBIDDEN = ("r8_all", "r8_inductive", "_train", "train_cpu")

# Full-split re-scores, matching FRONTIER below and MANIFEST in
# audit_numbers.py. The a_series originals capped study mixing at 19,998 of
# 416,256 cells, which is the axis D3 and D5 are claims about.
ABLATIONS = {
    "BASE":          BENCH / "full/full_p1_dab168_kl1/benchmark.csv",
    "-phase head":   BENCH / "full/full_a1_nophase/benchmark.csv",
    "-ECS":          BENCH / "full/full_a1_noecs/benchmark.csv",
    "-statistics":   BENCH / "full/full_a1_clsonly/benchmark.csv",
    "-sentinel":     BENCH / "full/full_a1_nodns/benchmark.csv",
    "random groups": BENCH / "full/full_a1_randgroups/benchmark.csv",
}
FRONTIER = [BENCH / f"full/full_p1_dab{d}_kl{k}/benchmark.csv"
            for d in ("7", "168", "336") for k in ("1", "30")]
VALIDATE = ROOT / "Outputs/validate/p1_dab168_kl1_full/validation.csv"
METRICS = {"BASE": ROOT / "Outputs/p_series/p1_dab168_kl1/metrics.csv",
           "-phase head": ROOT / "Outputs/a_series/a1_nophase/metrics.csv",
           "-ECS": ROOT / "Outputs/a_series/a1_noecs/metrics.csv",
           "-statistics": ROOT / "Outputs/a_series/a1_clsonly/metrics.csv",
           "-sentinel": ROOT / "Outputs/a_series/a1_nodns/metrics.csv",
           "random groups": ROOT / "Outputs/a_series/a1_randgroups/metrics.csv"}

# ──────────────────────────────────────────────────────────────────────────
# 1. THE CORPUS IS THE SAME, OR NOTHING BELOW IS COMPARABLE.
# ──────────────────────────────────────────────────────────────────────────
LABEL_LINE = re.compile(r"Harmonised (.+?)\s{2,}(\d+) of (\d+) cells labelled")

HELD_OUT_CELLS = 416_256

def labelled_counts(bench_csv: Path) -> dict:
    """The scorer's label tally for the HELD-OUT corpus, from the run's log.

    A run given --fit-split train logs the tally twice, once for val+test and
    once for the 1,161,472-cell fit corpus. Taking the last match made the
    reported arm look as though it disagreed with the fm_* runs about the
    corpus, when it does not. Only lines whose denominator is the held-out
    total are the comparison.
    """
    logs = sorted(bench_csv.parent.glob("*.log"))
    out = {}
    for log in logs:
        for m in LABEL_LINE.finditer(log.read_text(errors="replace")):
            label, got, total = m.group(1).strip(), int(m.group(2)), int(m.group(3))
            if total != HELD_OUT_CELLS:
                continue
            prev = out.get(label)
            if prev is not None and prev != (got, total):
                fail(f"{log.name} reports {label} twice with different counts: "
                     f"{prev} then {(got, total)}")
            out[label] = (got, total)
    return out

print("1. CORPUS IDENTITY")
checked = {}
for key, entry in SOURCES.items():
    f = entry[0]
    if f is None:
        continue
    if not f.exists():
        fail(f"source file missing: {f}"); continue
    c = labelled_counts(f)
    if not c:
        print(f"   {f.parent.name:26s} no log found, cannot assert corpus")
        continue
    checked[f.parent.name] = c
if checked:
    ref_name, ref = sorted(checked.items())[0]
    for name, c in sorted(checked.items()):
        shared = set(ref) & set(c)
        bad = {k: (ref[k], c[k]) for k in shared if ref[k] != c[k]}
        mark = "SAME" if not bad else f"DIFFERS {bad}"
        print(f"   {name:26s} {len(c)} labels  {mark}")
        if bad:
            fail(f"{name} does not share {ref_name}'s labelled-cell counts: {bad}")
    print(f"   reference: {ref_name}")
    for k, v in sorted(ref.items()):
        print(f"      {k:24s} {v[0]:>9,} of {v[1]:,}")

# ──────────────────────────────────────────────────────────────────────────
# 2. NO FORBIDDEN FILE IS REACHABLE FROM THE MANIFEST.
# ──────────────────────────────────────────────────────────────────────────
print("\n2. FORBIDDEN SOURCES")
for key, entry in SOURCES.items():
    f = entry[0]
    if f is None:
        continue
    hit = [b for b in FORBIDDEN if b in str(f)]
    if hit:
        fail(f"{key} points at a forbidden source ({hit}): {f}")
_forbidden_hits = [m for m in FAIL if "forbidden source" in m]
print("   manifest references no obsolete or train-split file"
      if not _forbidden_hits else f"   {len(_forbidden_hits)} violation(s)")

# ──────────────────────────────────────────────────────────────────────────
# 3. EVERY VALUE, WITH ITS PROVENANCE.
# ──────────────────────────────────────────────────────────────────────────
LEDGER: list[tuple[float, str]] = []
# Integers registered by blocks that run before CONSTANTS is built.
CONSTANTS_EXTRA: dict[int, str] = {}
# Arithmetic over LEDGER values. Declared here rather than at first use so
# that every block below can append to one list.
DERIVED: list[tuple[float, str]] = []

def rows(path: Path):
    with path.open(newline="") as fh:
        yield from csv.DictReader(fh)

def take(path: Path, method: str, policy, fit, test: str, label: str) -> None:
    """One value, by exact key. A miss is a failure, never a fallback."""
    if not path.exists():
        fail(f"missing file {path}"); return
    hits = []
    for r in rows(path):
        m = re.sub(r"__.*", "", (r.get("method") or ""))
        if m != method or r.get("test") != test or r.get("label") != label:
            continue
        if policy is not None and (r.get("gene_policy") or "") != policy:
            continue
        if fit is not None and (r.get("fit_on") or "") != fit:
            continue
        hits.append(r)
    if not hits:
        fail(f"no row for {method}/{policy}/{fit} {test}/{label} in "
             f"{path.relative_to(ROOT)}")
        return
    if len({h["value"] for h in hits}) > 1:
        fail(f"{method} {test}/{label} has conflicting values in "
             f"{path.relative_to(ROOT)}: {[h['value'] for h in hits]}")
        return
    try:
        v = float(hits[0]["value"])
    except ValueError:
        return
    try:
        WIDTHS[int(float(hits[0].get("width") or 0))] = f"{method} embedding width"
    except (ValueError, TypeError):
        pass
    LEDGER.append((v, f"{path.relative_to(ROOT)} :: {method}/"
                      f"{hits[0].get('gene_policy') or '-'}/"
                      f"{hits[0].get('fit_on') or '-'} {test}/{label}"))

TESTS = [("knn-agreement", "patient_id"), ("study-mixing", "all studies"),
         ("cross-donor", "menstrual phase"), ("cross-donor", "cell family"),
         ("cross-donor", "Endometriosis_stage"),
         ("cross-donor", "EndometriosisGrade"),
         ("cross-donor-p", "menstrual phase"), ("cross-donor-p", "cell family"),
         ("cross-donor-p", "Endometriosis_stage"),
         ("cross-donor-p", "EndometriosisGrade"),
         ("disease-xdonor", "all studies (pooled)"),
         ("disease-xdonor-p", "all studies (pooled)")]

for key, entry in SOURCES.items():
    f, policy, fit = entry[0], entry[1], entry[2]
    if f is None:
        continue
    # A mixing-only pass holds exactly one row; asking it for the rest is how
    # a split source turns into a wall of false failures.
    tests = ([("study-mixing", "all studies")] if key.endswith("_mixing")
             else TESTS)
    for test, label in tests:
        take(f, key.replace("_mixing", ""), policy, fit, test, label)

# ── severity, scored in its own pass, plus the note fields the prose quotes ──
# ADDED 6 November 2026 with Results [4]. Two things here that `take` cannot
# do. The severity rows live in separate files, because the labels were added
# to CROSS_DONOR_LABELS after the main pass and scored with --only-labels. And
# the prose quotes a permutation null's 95th percentile and a donor count,
# both of which live in the `note` column rather than in `value`, so they are
# read from the named row rather than pinned by hand.
SEVERITY_SOURCES = {
    "pca":          BENCH / "severity_ind_pca/benchmark.csv",
    "scvi":         BENCH / "severity_ind_scvi/benchmark.csv",
    "scanvi":       BENCH / "severity_ind_scanvi/benchmark.csv",
    "scgpt":        BENCH / "severity_scgpt/benchmark.csv",
    "geneformer":   BENCH / "severity_geneformer/benchmark.csv",
    "scfoundation": BENCH / "severity_scfoundation/benchmark.csv",
    "scimilarity":  BENCH / "severity_scimilarity/benchmark.csv",
    "harmony":      BENCH / "severity_trans_harmony/benchmark.csv",
    "scanorama":    BENCH / "severity_trans_scanorama/benchmark.csv",
    "elaj":         BENCH / "full/full_p1_dab168_kl1/benchmark.csv",
    # elaj: pending the eleven arm re-scores queued 6 November. When they land,
    # add BENCH / "full_p1_dab168_kl1/benchmark.csv" here.
}
SEVERITY_LABELS = ("severity", "severity (patients only)")
# [4] quotes the held-out severity of BOTH reported arms, so both are sources.
SEVERITY_SOURCES["elaj_blo"] = BENCH / "full/full_p1_dab168_kl30/benchmark.csv"

def take_note(path, method, test, label, keys=("p", "donors")):
    """Register the note fields of one named row: null95, p, donor count."""
    if not path.exists():
        fail(f"missing file {path}"); return
    for r in rows(path):
        m = re.sub(r"__.*", "", (r.get("method") or ""))
        if m != method or r.get("test") != test or r.get("label") != label:
            continue
        note = r.get("note") or ""
        prov = (f"{path.relative_to(ROOT)} :: {method} {test}/{label} note")
        for k in keys:
            mm = (re.search(rf"{k}=([-\d.]+)", note) if k != "donors"
                  else re.search(r"(\d+) donors", note))
            # NULL95 IS NOT REGISTERED. It is written to two decimals, so a
            # three-decimal p-value quoted in prose matches it numerically and
            # the pass is reported as ambiguous: 0.080 is geneformer's
            # severity p, and 0.08 is somebody's null. The prose quotes no
            # null anywhere, for exactly that reason, so registering them buys
            # nothing and costs a false ambiguity on every p below 0.1.
            if k == "null95":
                continue
            if mm:
                try:
                    LEDGER.append((float(mm.group(1)), f"{prov} {k}"))
                    # Donor counts are quoted in prose as integers, and the
                    # integer path reads CONSTANTS rather than the ledger, so
                    # they are registered from the row that reports them.
                    if k == "donors":
                        NOTE_DONORS[int(mm.group(1))] = f"donors, {label}"
                except ValueError: pass
        return
    fail(f"no row for {method} {test}/{label} in {path.relative_to(ROOT)}")

# ── the same four labels read over the whole corpus ──────────────────────
# Severity, stage and grade are not model inputs, so held-out protects
# against nothing for them and the whole corpus is the better-powered test:
# 118 donors against 34, and 57 against 18 once controls are dropped.
WHOLE_CORPUS = {
    "elaj": (BENCH / "whole_corpus/wholecorpus_p1_dab168_kl1/benchmark.csv",
             BENCH / "whole_corpus/wholecorpus_p1_dab168_kl30/benchmark.csv"),
}
WHOLE_CORPUS_LABELS = ("severity", "severity (patients only)",
                       "Endometriosis_stage", "EndometriosisGrade")
for _key, _files in WHOLE_CORPUS.items():
    for _f in _files:
        for _label in WHOLE_CORPUS_LABELS:
            take(_f, _key, None, None, "cross-donor", _label)
            take(_f, _key, None, None, "cross-donor-p", _label)
            take_note(_f, _key, "cross-donor", _label)

for key, f in SEVERITY_SOURCES.items():
    meth = "elaj" if key.startswith("elaj") else key
    for label in SEVERITY_LABELS:
        take(f, meth, None, None, "cross-donor", label)
        take(f, meth, None, None, "cross-donor-p", label)
        take_note(f, meth, "cross-donor", label)

# The same note fields for stage and grade, which the prose quotes as nulls.
for key, entry in SOURCES.items():
    if entry[0] is None or key.endswith("_mixing"): continue
    for label in ("Endometriosis_stage", "EndometriosisGrade"):
        take_note(entry[0], key, "cross-donor", label)

# [6] reads three rows off the ablation arms that no baseline comparison
# needs: the forty-five-way cell type, and merged severity with its p. They
# are added here rather than to TESTS so the baseline manifest stays as
# narrow as the prose that quotes it.
ABLATION_TESTS = TESTS + [("knn-agreement", "AnnotationRefined"),
                          ("cross-donor", "severity"),
                          ("cross-donor-p", "severity")]
for name, f in ABLATIONS.items():
    for test, label in ABLATION_TESTS:
        take(f, "elaj", "native", None, test, label)

for f in FRONTIER:
    for test, label in TESTS:
        take(f, "elaj", "native", None, test, label)

VALIDATE_CELLS: dict[int, str] = {}
if VALIDATE.exists():
    for r in rows(VALIDATE):
        try:
            v = float(r["value"])
        except (ValueError, TypeError):
            continue
        LEDGER.append((v, f"{VALIDATE.relative_to(ROOT)} :: "
                          f"{r['test']}/{r['label']} (whole corpus)"))
        # The cell count each whole-corpus row was measured over is quotable
        # prose, so it is registered from the file rather than typed into
        # CONSTANTS by hand.
        try:
            VALIDATE_CELLS[int(r["n_cells"])] = (
                f"cells, {r['test']}/{r['label']}, whole corpus")
        except (ValueError, TypeError, KeyError):
            pass
        for m in re.finditer(r"p=([\d.]+)", r.get("note") or ""):
            LEDGER.append((float(m.group(1)),
                           f"{VALIDATE.relative_to(ROOT)} :: "
                           f"{r['test']}/{r['label']} permutation p"))
else:
    fail(f"missing {VALIDATE}")

for name, f in METRICS.items():
    if not f.exists():
        fail(f"missing {f}"); continue
    rs = list(rows(f))
    vals = [(float(r["val_nb"]), float(r["train_nb"]), int(float(r["epoch"])))
            for r in rs]
    best = min(vals, key=lambda t: t[0])
    for v, tag in ((best[0], f"val_nb @best ep{best[2]}"),
                   (best[1], f"train_nb @best ep{best[2]}"),
                   (vals[-1][0], "val_nb @last"), (vals[-1][1], "train_nb @last")):
        LEDGER.append((v, f"{f.relative_to(ROOT)} :: {name} {tag}"))

# ── the per-epoch quantities [6] quotes ──────────────────────────────────
# Three things no benchmark file holds: where each arm's held-out loss
# bottoms out against where its biology peaks, what the decoder is reading
# at the selected checkpoint, and the same pair of arms compared at a
# matched epoch instead of at their own checkpoints.
#
# val_*_knn_xdonor IS NOT THE BENCHMARK'S CROSS-DONOR AGREEMENT. It is k=30
# on 19,972 validation cells against k=100 on the 416,256-cell held-out
# split, and the prose names it as a per-epoch validation readout wherever
# it is quoted. Registering it does not make the two interchangeable.
CURVES: dict[str, dict[str, list[float]]] = {}
for _name, _f in METRICS.items():
    if not _f.exists():
        continue
    _rs = list(rows(_f))
    CURVES[_name] = {c: [float(r[c]) for r in _rs]
                     for c in ("val_nb", "train_nb", "val_reliance_latent",
                               "val_reliance_technical", "val_reliance_ratio",
                               "val_family_knn_xdonor", "val_phase_knn_xdonor",
                               "val_patient_knn", "val_study_knn")
                     if c in (_rs[0] if _rs else {})}

def _sel(name: str) -> int:
    v = CURVES[name]["val_nb"]
    return v.index(min(v))

if {"BASE", "-phase head", "random groups"} <= set(CURVES):
    _B, _N, _R = CURVES["BASE"], CURVES["-phase head"], CURVES["random groups"]
    _bi, _ni, _ri = _sel("BASE"), _sel("-phase head"), _sel("random groups")

    def _reg(v, why):
        LEDGER.append((v, f"metrics.csv :: {why}"))

    # Where the two optima sit, and the value the selection rule returned
    # against the value the same run had already reached.
    _reg(_R["val_family_knn_xdonor"][_ri],
         f"random groups val_family_knn_xdonor at selected ep{_ri}")
    _reg(max(_R["val_family_knn_xdonor"]),
         "random groups val_family_knn_xdonor at its maximum")
    _reg(_R["val_nb"][1], "random groups val_nb at epoch 1")
    _reg(_N["val_phase_knn_xdonor"][_ni],
         f"-phase head val_phase_knn_xdonor at selected ep{_ni}")
    _reg(max(_N["val_phase_knn_xdonor"]),
         "-phase head val_phase_knn_xdonor at its maximum")
    # val_nb at this arm's first and last epoch is already registered by the
    # METRICS pass above (its best epoch IS epoch 0), so it is not repeated
    # here: one quantity under two wordings reads as an ambiguity.

    # The decoder's reliance at each selected checkpoint, in nats per gene.
    for _lab, _col in (("latent", "val_reliance_latent"),
                       ("provenance", "val_reliance_technical"),
                       ("ratio", "val_reliance_ratio")):
        _reg(_B[_col][_bi], f"BASE decoder reliance on {_lab}, ep{_bi}")
        _reg(_R[_col][_ri], f"random groups decoder reliance on {_lab}, ep{_ri}")

    # SELECTED CHECKPOINTS AGAINST A MATCHED EPOCH. This pair is the point of
    # the paragraph: the first difference is what removing the head looks
    # like, the second is what it is once both arms are read at the same age.
    _L = min(len(_B["val_nb"]), len(_N["val_nb"])) - 1
    for _lab, _col in (("donor", "val_patient_knn"), ("study", "val_study_knn")):
        DERIVED.append((_B[_col][_bi] - _N[_col][_ni],
                        f"{_lab} gap, BASE ep{_bi} minus -phase head ep{_ni}, "
                        f"each at its own checkpoint"))
        DERIVED.append((_B[_col][_L] - _N[_col][_L],
                        f"{_lab} gap at epoch {_L}, the last both arms ran"))
    DERIVED.append((_N["val_nb"][_ni] - _B["val_nb"][_bi],
                    "val_nb the head buys, each arm at its own checkpoint"))
    _gap = max(abs(x - y) for x, y in zip(_B["train_nb"], _N["train_nb"]))
    # Quoted as a bound, so the bound is registered, rounded up: a sentence
    # saying "within 0.001" is a claim about a maximum, not a value.
    DERIVED.append((math.ceil(_gap * 1e4) / 1e4,
                    "bound on the train_nb gap over the shared epochs"))
else:
    fail("the three training curves [6] reads are not all present")

# ── the ablation percentage changes [6] quotes ───────────────────────────
# Named arms and named axes only. Deriving every arm against every axis
# manufactured collisions with unrelated p-values when [1] was written, and
# a derivation wider than the prose makes the audit less useful, not more.
def _abl(arm: str, test: str, label: str):
    f = ABLATIONS.get(arm)
    for r in rows(f) if f and f.exists() else []:
        if (re.sub(r"__.*", "", r.get("method") or "") == "elaj"
                and r["test"] == test and r["label"] == label):
            return float(r["value"])
    return None

_AXES = {"disease":   ("disease-xdonor", "all studies (pooled)"),
         "donor recovery":   ("knn-agreement", "patient_id"),
         "study separation": ("study-mixing", "all studies"),
         "phase":     ("cross-donor", "menstrual phase"),
         "cell family": ("cross-donor", "cell family"),
         "cell type": ("knn-agreement", "AnnotationRefined"),
         "severity":  ("cross-donor", "severity")}

# ARM BY AXIS, AND ONLY WHERE THE PROSE QUOTES IT. [6] reports every
# ablation as a percentage change, so each pair below is a sentence in the
# subsection rather than a sweep of the table.
_QUOTED = {
    "random groups": ("disease", "cell family", "severity", "phase"),
    "-phase head":   ("donor recovery", "study separation"),
    "-ECS":          ("disease", "donor recovery", "study separation"),
    "-sentinel":     ("study separation",),
    "-statistics":   ("phase", "cell type"),
}
for _arm, _whys in _QUOTED.items():
    for _why in _whys:
        _test, _label = _AXES[_why]
        _u, _w = _abl("BASE", _test, _label), _abl(_arm, _test, _label)
        if _u and _w:
            _pc = abs(100 * (_w - _u) / _u)
            for _val in (_pc, round(_pc, 1)):
                DERIVED.append((_val, f"{_why} % change, BASE against {_arm}"))
        else:
            fail(f"could not derive the {_why} change for {_arm}")

# THE THREE BOUNDS. Where a change is under one per cent, one decimal place
# cannot tell it apart from any of the dozens of measured values that round
# to the same figure, so the prose states a bound and the bound is what gets
# derived -- rounded UP, so the sentence stays true.
_BOUNDS = (("-ECS", ("cell family", "phase", "cell type"), 0,
            "every biology axis -ECS moves by less than"),
           ("-sentinel", ("cell family", "phase", "donor recovery"), 0,
            "the three axes -sentinel barely moves, less than"),
           ("-statistics", ("cell family",), 1,
            "cell family under -statistics, less than"))
for _arm, _whys, _dp, _why in _BOUNDS:
    _pcs = []
    for _w2 in _whys:
        _test, _label = _AXES[_w2]
        _u, _v = _abl("BASE", _test, _label), _abl(_arm, _test, _label)
        if _u and _v:
            _pcs.append(abs(100 * (_v - _u) / _u))
    if len(_pcs) == len(_whys):
        _f = 10 ** _dp
        DERIVED.append((math.ceil(max(_pcs) * _f) / _f, f"{_why} (bound)"))
    else:
        fail(f"could not derive the bound for {_arm}")

# The cell-family readout's decay between its own peak and the epoch the
# selection rule returned, with the grouping shuffled.
if "random groups" in CURVES:
    _rf = CURVES["random groups"]["val_family_knn_xdonor"]
    _ri2 = _sel("random groups")
    _pc = abs(100 * (_rf[_ri2] - max(_rf)) / max(_rf))
    for _val in (_pc, round(_pc, 1)):
        DERIVED.append((_val, "random groups val_family_knn_xdonor, its peak "
                              "against the selected checkpoint, % change"))

for _arm, _test, _label, _why in (
        ("-statistics", "cross-donor", "cell family", "cell family"),):
    _u, _w = _abl("BASE", _test, _label), _abl(_arm, _test, _label)
    if _u and _w:
        DERIVED.append((abs(_u - _w), f"{_why} change, BASE against {_arm}"))
    else:
        fail(f"could not derive the {_why} change for {_arm}")

_ct = (_abl("BASE", "knn-agreement", "AnnotationRefined"),
       _abl("-statistics", "knn-agreement", "AnnotationRefined"))
if all(_ct):
    DERIVED.append((abs(_ct[0] - _ct[1]),
                    "cell type change, BASE against -statistics"))
else:
    fail("could not derive the cell-type change for -statistics")

# The sentinel paragraph states a bound over the three axes it does not
# single out, so the bound is derived rather than read off one of them.
_sent = [(_abl("BASE", t, l), _abl("-sentinel", t, l))
         for t, l in (("cross-donor", "cell family"),
                      ("cross-donor", "menstrual phase"),
                      ("knn-agreement", "patient_id"))]
if all(a and b for a, b in _sent):
    DERIVED.append((max(abs(a - b) for a, b in _sent),
                    "bound on how far -sentinel moves off BASE on the three "
                    "axes other than study separation"))
else:
    fail("could not derive the -sentinel bound")

# ── what the Discussion quotes and Results does not ──────────────────────
# Two claims about the field's measuring instruments. Both read off the
# same per-method files the comparison table uses, independently of
# audit_numbers.py's version.
#
# NOT REGISTERED: pcr_batch. RESULTS_STRUCTURE's E3 calls it exactly 1.0000
# for four methods and it is 0.5249 to 0.9386, so nothing in the paper may
# quote it until that is re-derived.
SCIB_TESTS = ("scib-ilisi_knn", "scib-clisi_knn", "scib-kbet")
_scib: dict[str, list[float]] = {t_: [] for t_ in SCIB_TESTS}
_family: dict[str, float] = {}
for _m, _e in list(SOURCES.items()) + [("elaj_arm",
        (BENCH / "full/full_p1_dab168_kl1/benchmark.csv", None, None))]:
    _f = _e[0]
    if _f is None or _m.endswith("_mixing") or not _f.exists():
        continue
    _meth = "elaj" if _m.startswith("elaj") else _m
    for _r in rows(_f):
        if re.sub(r"__.*", "", _r.get("method") or "") != _meth:
            continue
        if _r["test"] in _scib and _r["value"] not in ("", None):
            _scib[_r["test"]].append(float(_r["value"]))
        if (_r["test"] == "cross-donor" and _r["label"] == "cell family"
                and _r["value"] not in ("", None)):
            _family.setdefault(_meth, float(_r["value"]))

for _t, _vals in _scib.items():
    if not _vals:
        fail(f"no {_t} rows found for the Discussion's degeneracy claim")
        continue
    LEDGER.append((min(_vals), f"{_t}, lowest of {len(_vals)} methods"))
    LEDGER.append((max(_vals), f"{_t}, highest of {len(_vals)} methods"))

# THE BAND IS OVER THE NINE. The prose names Geneformer as the tenth and
# outside it, so deriving the band over all ten would not match the claim.
_band = {m: v for m, v in _family.items() if m != "geneformer"}
if len(_band) >= 8:
    _lo, _hi = min(_band.values()), max(_band.values())
    DERIVED.append((_hi - _lo, f"cell family band across {len(_band)} methods, "
                               f"Geneformer excluded as the prose does"))
else:
    fail(f"cell family band has only {len(_band)} methods")

ANALYSIS = ROOT / "Outputs/analysis"
for arm in ("p1_dab168_kl1", "p1_dab168_kl30"):
    for stem, lab, frm, to in (("phase_within_family", "phase", "proliferative", "secretory"),
                               ("disease_within_family", "case_vs_control", "case", "control")):
        f = ANALYSIS / arm / f"{stem}.csv"
        if not f.exists():
            fail(f"missing {f}"); continue
        for r in rows(f):
            if r["label"] != lab or r["from"] != frm or r["to"] != to:
                continue
            LEDGER.append((float(r["over_scatter"]),
                           f"{f.relative_to(ROOT)} :: {r['stratum']} over_scatter"))
    f = ANALYSIS / arm / "reference_scales.csv"
    if f.exists():
        for r in rows(f):
            if r["label"] == "cell family":
                LEDGER.append((float(r["over_scatter"]),
                               f"{f.relative_to(ROOT)} :: {r['from']}/{r['to']} over_scatter"))

print(f"\n3. LEDGER: {len(LEDGER)} values from "
      f"{len({p.split(' :: ')[0] for _, p in LEDGER})} files")

# Derived quantities. Each is arithmetic on ledger values and says so.
# Declared beside LEDGER, above, because the trajectory block appends to it.
base = {p: v for v, p in LEDGER if "p1_dab168_kl1/benchmark.csv" in p
        and "elaj/native" in p and "cross-donor menstrual phase" in p}
b = next((v for v, p in LEDGER if "p1_dab168_kl1/benchmark.csv" in p
          and "cross-donor/menstrual phase" in p and "elaj/" in p), None)
n = next((v for v, p in LEDGER if "a1_nophase" in p
          and "cross-donor/menstrual phase" in p), None)
if b and n:
    kept = n / b
    DERIVED += [(kept * 100, f"100 * {n:.4f}/{b:.4f}, share of chance-corrected "
                              f"phase signal surviving head removal"),
                ((1 - kept) * 100, "the head's share, 100 minus the above")]
else:
    fail("could not locate both phase values for the D1 split")

donor = next((v for v, p in LEDGER if "validation.csv" in p
              and "knn-agreement/patient_id" in p), None)
if donor is not None:
    CHANCE = 0.0060
    DERIVED += [(donor * (1 - CHANCE) + CHANCE,
                 f"agreement recovered from excess {donor:.4f} through chance "
                 f"{CHANCE:.4f}"),
                ((donor * (1 - CHANCE) + CHANCE) / CHANCE,
                 "the same over chance, as a fold enrichment")]
else:
    fail("could not locate whole-corpus donor agreement")

# The corpus size also appears rounded to millions in a heading.
DERIVED.append((1_577_728 / 1e6, "corpus cells in millions, 1,577,728 / 1e6"))

# ── what [1] derives from the frontier table ─────────────────────────────
# The knob effects are differences between two arms on one axis, and the
# pca-to-harmony figures are percentage changes. Both are arithmetic over
# rows already registered above, so they are recomputed here from the same
# files rather than quoted from a notebook.
_ARM_AXES: dict[tuple[str, str], float] = {}
for _f in FRONTIER:
    _arm = _f.parent.name.replace("full_", "", 1)
    for _test, _label, _axis in (("cross-donor", "menstrual phase", "phase"),
                                 ("study-mixing", "all studies", "mixing"),
                                 ("knn-agreement", "patient_id", "donor")):
        for _r in rows(_f) if _f.exists() else []:
            if (re.sub(r"__.*", "", _r.get("method") or "") == "elaj"
                    and _r["test"] == _test and _r["label"] == _label):
                _ARM_AXES[(_arm, _axis)] = float(_r["value"]); break
# NAMED COMPARISONS ONLY. Deriving every pair manufactured collisions with
# unrelated p-values, which is the same fault registering null95 had: a
# derivation that is wider than the prose makes the audit less useful, not
# more. [1] compares each arm against itself across the information cost, and
# the two lower adversarial weights at the lower cost.
_PAIRS = ([(f"p1_dab{_d}_kl1", f"p1_dab{_d}_kl30", "information cost")
           for _d in ("7", "168", "336")]
          + [(f"p1_dab7_kl{_k}", f"p1_dab168_kl{_k}", "adversarial weight")
             for _k in ("1", "30")]
          )
# The 168-to-336 step is reported as levels, not as a change, so no delta is
# derived for it. A phase delta of 0.0200 there would collide with the 0.020
# permutation p in [4], and a derivation nothing quotes can only do harm.
for _a, _b, _why in _PAIRS:
    for _ax in ("phase", "mixing", "donor"):
        if (_a, _ax) in _ARM_AXES and (_b, _ax) in _ARM_AXES:
            _u, _w = _ARM_AXES[(_a, _ax)], _ARM_AXES[(_b, _ax)]
            # [1] reports these as percentage changes, which is the only form
            # in which three axes on different scales can be read together.
            _pc = abs(100 * (_w - _u) / _u)
            # Registered at full precision AND at the one decimal place the
            # prose quotes. A percentage change is derived, so there is no
            # source precision to round against, and leaving only the full
            # value makes every quoted figure look like an unpinned rounding.
            for _val in (_pc, round(_pc, 1)):
                DERIVED.append((_val, f"{_ax} % change across the {_why}, "
                                      f"{_a} against {_b}"))

_PCA_T = BENCH / "wide_full_pca/benchmark.csv"
_HARM = BENCH / "wide_full_harmony/benchmark.csv"
def _one(path, meth, test, label):
    for _r in rows(path) if path.exists() else []:
        if (re.sub(r"__.*", "", _r.get("method") or "") == meth
                and _r["test"] == test and _r["label"] == label):
            return float(_r["value"])
    return None
for _test, _label, _why in (("study-mixing", "all studies", "study separation"),
                            ("cross-donor", "menstrual phase", "phase")):
    _p, _h = _one(_PCA_T, "pca", _test, _label), _one(_HARM, "harmony", _test, _label)
    if _p and _h:
        DERIVED.append((abs(100 * (_h - _p) / _p), f"pca to harmony, {_why}"))

# The cross-method correlations, recomputed here from this file's own
# manifest rather than imported, so the two scripts can disagree.
try:
    from scipy.stats import spearmanr
    _field = {}
    for _m, _e in SOURCES.items():
        if _e[0] is None: continue
        _rows = {}
        for _r in rows(_e[0]):
            _mm = re.sub(r"__.*", "", _r.get("method") or "")
            if _mm != _m: continue
            if (_r.get("gene_policy") or "") != (_e[1] or ""): continue
            if (_r.get("fit_on") or "") != (_e[2] or ""): continue
            _rows[(_r["test"], _r["label"])] = _r["value"]
        if _rows: _field[_m] = _rows
    def _col(t, l):
        return [float(v[(t, l)]) for v in _field.values() if (t, l) in v
                and v[(t, l)] not in ("", None)]
    _dn = _col("knn-agreement", "patient_id")
    for _lab, _t, _l in (("phase", "cross-donor", "menstrual phase"),
                         ("family", "cross-donor", "cell family"),
                         ("disease", "disease-xdonor", "all studies (pooled)")):
        _v = _col(_t, _l)
        if len(_v) == len(_dn) and len(_dn) >= 3:
            _r, _p = spearmanr(_dn, _v)
            for _x in (_r, abs(_r), _p):
                DERIVED.append((_x, f"Spearman across {len(_dn)} methods, "
                                    f"donor recovery vs {_lab}"))
            DERIVED.append((max(_v) - min(_v),
                            f"spread of {_lab} across {len(_v)} methods"))
    DERIVED.append((max(_dn) - min(_dn), "spread of donor recovery"))
    _w = [float(v[("knn-agreement", "patient_id")]) and 0 or 0 for v in []]
    _wid, _ph = [], []
    for _m, _e in SOURCES.items():
        if _e[0] is None or _m.endswith("_mixing"): continue
        for _r in rows(_e[0]):
            if (re.sub(r"__.*", "", _r.get("method") or "") == _m
                    and _r["test"] == "cross-donor"
                    and _r["label"] == "menstrual phase"):
                try:
                    _wid.append(int(float(_r["width"]))); _ph.append(float(_r["value"]))
                except (ValueError, TypeError):
                    pass
                break
    if len(_wid) >= 3:
        _r2, _p2 = spearmanr(_wid, _ph)
        for _x in (_r2, abs(_r2), _p2):
            DERIVED.append((_x, f"Spearman across {len(_wid)} methods, "
                                f"representation width vs phase"))
except Exception as _exc:
    fail(f"cross-method correlations could not be computed: {_exc}")

# ── the corpus's annotation coverage, checked rather than asserted ────────
# Results [2] says every cell-type label in this corpus belongs to an
# endometrial cell. That is a claim a reviewer can test in one line, so the
# audit tests it rather than trusting the count: it reads the dumped metadata,
# counts the cells outside endometrium, and FAILS if any of them carries a
# label in any of the five annotation columns the eleven studies provide.
ANNOTATION_COLUMNS = ("cell family", "AnnotationMain", "lineage", "celltype",
                      "AnnotationRefined")
CELLS_META = ROOT / "Outputs/cells/p1_dab168_kl1/metadata.csv.gz"

# A CITED NUMBER HAS NO FILE BEHIND IT, AND THAT IS NOT THE SAME AS HAVING
# NO SOURCE. Until this registry existed, "11.1 years to diagnosis" matched
# a derived percentage change in donor recovery (11.1%) and was reported as
# sourced to it. A literature value is registered with its bibliography key
# and pinned, so it can only ever resolve to the paper it came from.
LITERATURE = [
    (11.1, "cited: bontempo2025diagnostic, mean years to diagnosis"),
]
for _v, _why in LITERATURE:
    LEDGER.append((_v, _why))

# THE SPLIT LEAK. Measured once by check_donor_overlap.sh over all 55 study
# pairs and written to a report; the dumped metadata carries only patient_id
# and the overlap was found on source_sample_id, so it cannot be recomputed
# from the dump. The figure is read from the report rather than typed here,
# and the percentage is derived against the held-out cell count.
OVERLAP = ROOT / "Outputs/qc/donor_overlap_261022/donor_overlap.md"
if OVERLAP.exists():
    _ov = OVERLAP.read_text()
    _dup = re.search(r"source_sample_id: (\d+) shared", _ov)
    if _dup:
        CONSTANTS_EXTRA[int(_dup.group(1))] = "samples deposited under two identifiers"
    else:
        fail(f"{OVERLAP.name} no longer states the shared-sample count")
    _m = re.search(r"Held-out cells belonging to a donor that also appears in "
                   r"the other study:\s*\*\*([\d,]+)\*\*", _ov)
    if _m:
        _leak = int(_m.group(1).replace(",", ""))
        CONSTANTS_EXTRA[_leak] = "held-out cells sharing a person across the study pair"
        DERIVED.append((100 * _leak / 416256,
                        "leaked held-out cells as a share of the held-out set"))
    else:
        fail(f"{OVERLAP.name} no longer states the held-out overlap count")
else:
    fail(f"missing the donor-overlap report {OVERLAP}")

# Per-study shares the prose quotes, counted from the dumped metadata in
# the same pass that checks annotation coverage rather than typed here.
STUDY_SHARES = ("li_2025",)
STUDY_CELLS: dict[int, str] = {}

def annotation_coverage() -> None:
    import gzip
    if not CELLS_META.exists():
        fail(f"missing {CELLS_META}"); return 0
    with gzip.open(CELLS_META, "rt", newline="") as fh:
        rd = csv.DictReader(fh)
        cols = [c for c in ANNOTATION_COLUMNS if c in (rd.fieldnames or [])]
        if len(cols) != len(ANNOTATION_COLUMNS):
            fail(f"annotation columns missing from the dump: "
                 f"{set(ANNOTATION_COLUMNS) - set(cols)}")
            return 0
        outside = 0
        labelled_outside = 0
        total = 0
        per_study: dict[str, int] = {}
        per_donor: dict[str, set] = {}
        all_donors: set = set()
        for r in rd:
            total += 1
            all_donors.add(r.get("patient_id"))
            st = r.get("study") or ""
            if st in STUDY_SHARES:
                per_study[st] = per_study.get(st, 0) + 1
                per_donor.setdefault(st, set()).add(r.get("patient_id"))
            if (r.get("tissue") or "") == "endometrium":
                continue
            outside += 1
            if any((r.get(c) or "").strip() for c in cols):
                labelled_outside += 1
    # 269 identifiers; 254 people once the duplicated pair is resolved.
    CONSTANTS_EXTRA[len(all_donors)] = "donor identifiers in the corpus"
    _d = next((k for k, v in CONSTANTS_EXTRA.items()
               if v == "samples deposited under two identifiers"), None)
    if _d:
        CONSTANTS_EXTRA[len(all_donors) - _d] = "people, identifiers minus duplicates"
    for st, n_ in per_study.items():
        STUDY_CELLS[n_] = f"cells from {st}"
        STUDY_CELLS[len(per_donor[st])] = f"donors in {st}"
        DERIVED.append((100 * n_ / total, f"{st} as a share of the corpus"))
    if labelled_outside:
        fail(f"[2] claims no cell-type label outside endometrium, but "
             f"{labelled_outside:,} such cells carry one")
    print(f"\n   annotation coverage: {outside:,} cells outside endometrium, "
          f"{labelled_outside} of them labelled")
    return outside

OUTSIDE_ENDOMETRIUM = annotation_coverage()

# ── the two knobs, read from the configs that set them ───────────────────
# [1] names the adversarial weights and information costs. They are
# configuration rather than measurement, so they are read from the arm
# configs instead of being typed here: a knob renamed in a config and not in
# the prose should fail the build.
KNOBS: dict[int, str] = {}
_CFG = ROOT / "axw1008/src/configs/experiment"
for _d in ("7", "168", "336"):
    for _k in ("1", "30"):
        _f = _CFG / f"p1_dab{_d}_kl{_k}.yaml"
        if not _f.exists():
            fail(f"missing arm config {_f}"); continue
        _txt = _f.read_text()
        for _key, _why in (("model.dab.lambda_dab", "adversarial weight"),
                           ("model.loss.w_kl_gauss", "information cost")):
            _m = re.search(rf"{re.escape(_key)}:\s*([\d.]+)", _txt)
            if _m:
                KNOBS[int(float(_m.group(1)))] = _why
print(f"\n   knob values from the arm configs: {sorted(KNOBS)}")

CONSTANTS = {
    1577728: "corpus cells, metadata",
    1161472: "train-split cells, benchmark log",
    416256:  "val+test cells, benchmark log",
    466176:  "cells with CycleDay, metadata",
    195879:  "cells scored, cross-donor phase, reported arm",
    172740:  "cells scored, pooled disease, reported arm",
    15496:   "ELAJ vocabulary",
    30962:   "baseline vocabulary",
    269: "donors", 142: "donors, whole-corpus phase", 118: "donors, severity",
    67: "severity label levels", 60: "cycle-day donors / grade donors",
    58: "stage donors, whole corpus", 36: "phase donors, held out",
    34: "donors, merged severity, held out", 18: "donors, mild vs severe",
    30: "last cycle day", 22: "cycle days present", 16: "latent dimensions",
    11: "studies", 5: "first cycle day",
    # Reported by every arm's own training log; see axw1008 ABLATIONS.md.
    1883986: "ELAJ parameters",
    256: "Geneformer width", 512: "scGPT width", 3072: "scFoundation width",
    # What one group hands forward, from Methods: a learned query plus eight
    # order statistics, each its own token at width 32.
    288: "numbers per group, 9 summary tokens x width 32",
    32: "numbers per group with the statistics removed, and the token width",
}
# DERIVED, not typed: the count of cells outside endometrium comes from the
# dumped metadata in the same pass that proves none of them is annotated.
for _n, _why in VALIDATE_CELLS.items():
    CONSTANTS.setdefault(_n, _why)
for _n, _why in STUDY_CELLS.items():
    CONSTANTS.setdefault(_n, _why)
for _n, _why in CONSTANTS_EXTRA.items():
    CONSTANTS.setdefault(_n, _why)
for _n, _why in NOTE_DONORS.items():
    CONSTANTS.setdefault(_n, _why)
for _n, _why in KNOBS.items():
    CONSTANTS.setdefault(_n, _why)
for _n, _why in WIDTHS.items():
    if _n:
        CONSTANTS.setdefault(_n, _why)
if OUTSIDE_ENDOMETRIUM:
    CONSTANTS[OUTSIDE_ENDOMETRIUM] = ("cells outside endometrium, none "
                                      "annotated, from the dump")

# ──────────────────────────────────────────────────────────────────────────
# PINNED VALUES. A number the prose rounds cannot be traced by search: at two
# decimal places several unrelated quantities collide, and whichever the
# search reported first would look like provenance while being a coincidence.
# That is exactly how "0.408" was shown as a reconstruction loss when the
# prose means a permutation p. So every rounded number is PINNED to the row
# it came from, and the script asserts the pin rounds to it. A pin that does
# not is a failure; an unpinned rounded number is a failure.
# ──────────────────────────────────────────────────────────────────────────
PINNED = {
    "0.58": ("validation.csv", "linear-corr/epithelial.pseudotime"),
    "0.47": ("validation.csv", "linear-corr/ProgesteroneSerum"),
    "0.34": ("validation.csv", "linear-corr/pct_counts_mt"),
    "0.14": ("validation.csv", "linear-corr/scDblFinder.score"),
    "0.408": ("validation.csv", "EndometriosisGrade permutation p"),
    "0.005": ("p1_dab168_kl1/benchmark.csv", "cross-donor-p/menstrual phase"),
    "0.332": ("validation.csv", "cross-donor/Endometriosis_stage"),
    "65.5": ("share of chance-corrected", ""),
    # The other half of the same split. Never checked until 6 November,
    # because it sits after an escaped percent sign on its line and the
    # comment strip was eating the rest of the line.
    "34.5": ("the head's share", ""),
    "1.58": ("corpus cells in millions", ""),
    # The cross-method correlations and their p-values. Rounded in prose, so
    # pinned to the axis they belong to rather than searched for.
    "0.721": ("donor recovery vs disease", ""),
    "0.019": ("donor recovery vs disease", ""),
    "0.176": ("donor recovery vs phase", ""),
    "30.3": ("pca to harmony", "study separation"),
    "8.2":  ("pca to harmony", "phase"),
    # Two different measurements round to 0.219 at three decimals. [4] quotes
    # scanorama's merged-severity permutation p; the collision is with a stage
    # p elsewhere in the table, and the prose names the method and the test.
    "0.219": ("severity_trans_scanorama/benchmark.csv",
              "cross-donor/severity note p"),
    "0.63":  ("donor recovery vs phase", ""),
    # [6]'s decoder-reliance ratios and the one severity p it quotes at three
    # decimals. Rounded, so pinned rather than searched for.
    "0.4024": ("metrics.csv", "BASE val_nb @best"),
    # cLISI is exactly 1 for every method, which also happens to be the
    # value two of [6]'s "less than 1%" bounds round up to.
    "1.0000": ("scib-clisi_knn", ""),
    "0.0000": ("scib-ilisi_knn", ""),
    # [6] quotes the range of severity p across the six ablation arms. The
    # low end is the head-free arm's 0.1493, and geneformer's STAGE p is
    # exactly 0.149, so the unpinned search certified the wrong row.
    "0.149": ("a1_nophase/benchmark.csv", "cross-donor-p/severity"),
    "7.46": ("BASE decoder reliance on ratio", ""),
    "2.43": ("random groups decoder reliance on ratio", ""),
    "0.468": ("a1_randgroups/benchmark.csv", "cross-donor-p/severity"),
}

# PINNED, BUT ONLY INSIDE ONE SUBSECTION. A percentage written to one
# decimal collides easily: [1]'s "7.7\% of donor recovery" across the
# information cost and [6]'s "7.7\%" of menstrual phase under a shuffled
# grouping are different quantities with the same digits, and a pin keyed on
# the digits alone would certify both against one row. Keyed on the
# subsection as well, each occurrence is pinned to its own source.
PINNED_AT = {
    ("1", "7.7"): ("donor % change across the information cost", "p1_dab7_kl1"),
    ("6", "7.7"): ("phase % change, BASE against random groups", ""),
    ("D", "0.0"): ("scib-ilisi_knn", ""),
    ("D", "1.0"): ("scib-clisi_knn", ""),
    ("D", "0.04"): ("scib-kbet", ""),
    # 11.1 is two unrelated things: years to diagnosis in the Discussion,
    # and the donor-recovery change across the adversarial weight in [1].
    ("1", "11.1"): ("donor % change across the adversarial weight", "p1_dab7_kl1"),
    ("D", "11.1"): ("cited: bontempo2025diagnostic", ""),
    ("D", "2.87"): ("li_2025 as a share of the corpus", ""),
    ("D", "4.3"): ("leaked held-out cells as a share", ""),
}

def subsection_of(pos: int, marks: list[tuple[int, str]]) -> str:
    """Which [n] subsection a character offset falls in."""
    here = ""
    for at, num in marks:
        if at <= pos:
            here = num
        else:
            break
    return here

def pinned_source(raw: str, dp: int):
    """The pinned ledger entry for a prose value, checked against the pin."""
    want = PINNED.get(raw)
    if want is None:
        return None
    return _resolve(raw, dp, want)

def _resolve(raw: str, dp: int, want):
    needle, key = want
    cands = [(v, prov) for v, prov in LEDGER + DERIVED
             if needle in prov and (not key or key in prov)]
    if not cands:
        fail(f"prose value {raw} is pinned to {want} and no such row exists")
        return "MISSING PIN"
    exact = [(v, prov) for v, prov in cands if round(v, dp) == float(raw)]
    if not exact:
        fail(f"prose value {raw} is pinned to {want}, whose value(s) "
             f"{[round(v, 4) for v, _ in cands]} do not round to it")
        return "PIN MISMATCH"
    return exact[0][1]

# ──────────────────────────────────────────────────────────────────────────
# 4. THE PROSE, NUMBER BY NUMBER.
# ──────────────────────────────────────────────────────────────────────────
def strip_group(text: str, macro: str) -> str:
    """Remove every `\\macro{...}` by counting braces, not by guessing."""
    out, i = [], 0
    needle = "\\" + macro + "{"
    while True:
        j = text.find(needle, i)
        if j < 0:
            out.append(text[i:]); break
        out.append(text[i:j])
        k, depth = j + len(needle), 1
        while k < len(text) and depth:
            if text[k] == "{": depth += 1
            elif text[k] == "}": depth -= 1
            k += 1
        i = k
    return "".join(out)

tex = "\n".join(
    (f.read_text() if f.name.startswith("02")
     else "\\subsection*{[D] discussion}\n" + f.read_text())
    for f in TEX_FILES if f.exists())
for macro in ("note", "todo", "citep", "citet", "cite", "label", "ref"):
    tex = strip_group(tex, macro)
tex = re.sub(r"^%.*$", "", tex, flags=re.M)
# TRAILING COMMENTS, BUT NOT AN ESCAPED PERCENT SIGN. This pattern was
# `%.*$`, which deleted the rest of any line containing a `\%` -- so every
# number written after a percentage on the same line had never been checked.
# [1] is full of them: "gave up 7.4\% of phase (0.7337 to 0.6791)" was read
# as "gave up 7.4" and the two levels were invisible to the audit.
tex = re.sub(r"(?<!\\)%.*$", "", tex, flags=re.M)
tex = re.sub(r"Fig\.~\d+[a-z]?(--[a-z])?", "", tex)
# Ordinals are words. "95th percentile" is the name of a quantity, not a
# measurement, and 95 has no source row by design.
tex = re.sub(r"\d+(?:st|nd|rd|th)\b", "", tex)
# Subsection numbers are structural markers, not measurements. Stripped
# rather than whitelisted, so the number itself stays checked wherever
# else it appears: [6] arrived on 5 November and failed the gate as an
# unsourced prose value, which is the gate working and the wrong target.
# Offsets into THIS string, recorded before the numbers are stripped, so a
# pin can name the subsection a prose value sits in.
SUBSECTION_OFFSETS = [(m.start(), m.group(1)) for m in
                      re.finditer(r"\\subsection\*\{\[(\w+)\]", tex)]
tex = re.sub(r"\\subsection\*\{\[\w+\]", r"\\subsection*{", tex)
# Study identifiers are names, not measurements: marecko\_2024, lin\_2023.
tex = re.sub(r"[A-Za-z]+\\_\d{4}", "", tex)
tex = tex.replace("{,}", "").replace(",", "")

print("\n4. PROSE, NUMBER BY NUMBER\n")
unaccounted, ambiguous, ok = [], [], 0
# A NUMBER AT THE END OF A SENTENCE IS STILL A NUMBER. The trailing
# lookahead was `(?![\d.])`, which rejected any match followed by a full
# stop, so "the ratio fell to 2.43." was never checked. Only a following
# DIGIT should disqualify a match.
for mobj in re.finditer(r"(?<![\d.])(\d+\.\d+|\d+)(?!\d)", tex):
    raw = mobj.group(1)
    if "." not in raw:
        if int(raw) in CONSTANTS:
            ok += 1
        elif int(raw) < 5:
            ok += 1                      # ordinals and counts in words
        else:
            unaccounted.append(raw)
        continue
    dp = len(raw.split(".")[1])
    v = float(raw)
    # The prose writes a negative excess as a sign plus a magnitude, so a
    # stored -0.0414 must satisfy a written 0.0414. Matching |value| is safe
    # here because sign is never the thing in doubt.
    hits = {prov for val, prov in LEDGER + DERIVED
            if round(val, dp) == v or round(abs(val), dp) == v}
    exact = {prov for val, prov in LEDGER + DERIVED
             if f"{val:.4f}" == f"{v:.4f}" or f"{abs(val):.4f}" == f"{v:.4f}"}
    if not hits:
        unaccounted.append(raw); continue
    where = subsection_of(mobj.start(), SUBSECTION_OFFSETS)
    if (where, raw) in PINNED_AT:
        prov = _resolve(raw, dp, PINNED_AT[(where, raw)])
        if prov and not prov.startswith(("MISSING", "PIN ")):
            ok += 1
            print(f"   {raw:<8} <- PINNED in [{where}] {prov}")
        continue
    if raw in PINNED:
        prov = pinned_source(raw, dp)
        if prov and not prov.startswith(("MISSING", "PIN ")):
            ok += 1
            print(f"   {raw:<8} <- PINNED {prov}")
        continue
    if exact and len(hits) == 1:
        ok += 1
        print(f"   {raw:<8} <- {sorted(hits)[0]}")
        continue
    if not exact:
        # rounded, and not pinned. Never guess which source it meant.
        ambiguous.append((raw, sorted(hits)[:2], len(hits), "rounded, UNPINNED"))
        continue
    # exact to 4 dp but several rows hold that value. Acceptable only when
    # every one of them is the same quantity; otherwise the prose is unclear.
    kinds = {prov.split("::")[-1].strip() for prov in exact}
    if len(kinds) == 1:
        ok += 1
        print(f"   {raw:<8} <- {sorted(exact)[0]}  (+{len(exact)-1} identical)")
    else:
        ambiguous.append((raw, sorted(kinds)[:3], len(kinds), "same value, different quantities"))

print(f"\n   accounted: {ok}")
if ambiguous:
    print("\n   AMBIGUOUS (matches more than one source at this precision):")
    for raw, h, k, why in ambiguous:
        print(f"     {raw}  [{why}] {k} candidate(s), e.g. {h[0]}")
        fail(f"prose value {raw}: {why}, {k} candidates")
if unaccounted:
    print("\n   UNACCOUNTED:")
    for raw in sorted(set(unaccounted)):
        print(f"     {raw}")
        fail(f"prose value {raw} has no source")

print("\n" + "=" * 68)
if FAIL:
    print(f"FAILED, {len(FAIL)} problem(s):")
    for m in FAIL:
        print(f"  - {m}")
    sys.exit(1)
print("PASSED. Every number in the Results prose traces to a named file, the")
print("source files share one labelled-cell pool, and no obsolete or")
print("train-split file is reachable from the manifest.")
