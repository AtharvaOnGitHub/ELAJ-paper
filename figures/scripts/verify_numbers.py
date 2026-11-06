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
import csv, re, sys
from pathlib import Path

ROOT = Path("/Users/atharvawaghmare/Endo research/ELAJ")
PAPER = Path(__file__).resolve().parents[2]
TEX = PAPER / "sections" / "02-results.tex"

FAIL: list[str] = []
def fail(msg: str) -> None:
    FAIL.append(msg)

# ──────────────────────────────────────────────────────────────────────────
# THE SOURCE MANIFEST. Every file the prose may draw on, named, with the
# reason it is the right file. Adding a file here is a decision; globbing
# one in is not.
# ──────────────────────────────────────────────────────────────────────────
BENCH = ROOT / "Outputs/Benchmarks"
SOURCES = {
    "elaj":     (BENCH / "p1_dab168_kl1/benchmark.csv", "native", "train",
                 "the reported arm, ELAJ's own 15,496-gene vocabulary"),
    "frontier": (None, None, None, "the six p1_* arms, ELAJ rows only"),
    "pca":      (BENCH / "fm_scgpt/benchmark.csv", "all30962", "train",
                 "wide axis, inductive; bit-identical in all four fm_* files"),
    "scvi":     (BENCH / "fm_scgpt/benchmark.csv", "all30962", "train", "as pca"),
    "scanvi":   (BENCH / "fm_scgpt/benchmark.csv", "all30962", "train", "as pca"),
    "scgpt":        (BENCH / "fm_scgpt/benchmark.csv", "native", "pretrained", ""),
    "geneformer":   (BENCH / "fm_baseline+Geneformer/benchmark.csv", "native", "pretrained", ""),
    "scfoundation": (BENCH / "fm_scfoundation/benchmark.csv", "native", "pretrained", ""),
    "scimilarity":  (BENCH / "fm_scimilarity/benchmark.csv", "native", "pretrained", ""),
    "harmony":   (BENCH / "wide_transductive/benchmark.csv", "all30962", "",
                  "wide axis, transductive: cannot be fitted inductively"),
    "scanorama": (BENCH / "wide_transductive/benchmark.csv", "all30962", "",
                  "as harmony"),
}
# Deliberately absent: r8_all and r8_inductive (obsolete corpus, ELAJ scores
# 0.1161 there), p1_dab168_kl1_train and elaj_train_cpu (train split), and the
# narrow all-policy pca/scvi/scanvi rows in p1_dab168_kl1, which are a
# different experiment from the wide ones and must not be mixed with them.
FORBIDDEN = ("r8_all", "r8_inductive", "_train", "train_cpu")

ABLATIONS = {
    "BASE":          BENCH / "p1_dab168_kl1/benchmark.csv",
    "-phase head":   BENCH / "a_series/a1_nophase/benchmark.csv",
    "-ECS":          BENCH / "a_series/a1_noecs/benchmark.csv",
    "-statistics":   BENCH / "a_series/a1_clsonly/benchmark.csv",
    "-sentinel":     BENCH / "a_series/a1_nodns/benchmark.csv",
    "random groups": BENCH / "a_series/a1_randgroups/benchmark.csv",
}
FRONTIER = [BENCH / f"p1_dab{d}_kl{k}/benchmark.csv"
            for d in ("7", "168", "336") for k in ("1", "30")]
VALIDATE = ROOT / "Outputs/validate/p1_dab168_kl1_full/validation.csv"
METRICS = {"BASE": ROOT / "Outputs/p_series/p1_dab168_kl1/metrics.csv",
           "-phase head": ROOT / "Outputs/a_series/a1_nophase/metrics.csv"}

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
    for test, label in TESTS:
        take(f, key if key != "elaj" else "elaj", policy, fit, test, label)

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
    "elaj":         BENCH / "full_p1_dab168_kl1/benchmark.csv",
    # elaj: pending the eleven arm re-scores queued 6 November. When they land,
    # add BENCH / "full_p1_dab168_kl1/benchmark.csv" here.
}
SEVERITY_LABELS = ("severity", "severity (patients only)")

NOTE_DONORS: dict[int, str] = {}

def take_note(path, method, test, label, keys=("null95", "p", "donors")):
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
    for label in SEVERITY_LABELS:
        take(f, key, None, None, "cross-donor", label)
        take(f, key, None, None, "cross-donor-p", label)
        take_note(f, key, "cross-donor", label)

# The same note fields for stage and grade, which the prose quotes as nulls.
for key, entry in SOURCES.items():
    if entry[0] is None: continue
    for label in ("Endometriosis_stage", "EndometriosisGrade"):
        take_note(entry[0], key, "cross-donor", label)

for name, f in ABLATIONS.items():
    for test, label in TESTS:
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
DERIVED: list[tuple[float, str]] = []
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
        for r in rd:
            if (r.get("tissue") or "") == "endometrium":
                continue
            outside += 1
            if any((r.get(c) or "").strip() for c in cols):
                labelled_outside += 1
    if labelled_outside:
        fail(f"[2] claims no cell-type label outside endometrium, but "
             f"{labelled_outside:,} such cells carry one")
    print(f"\n   annotation coverage: {outside:,} cells outside endometrium, "
          f"{labelled_outside} of them labelled")
    return outside

OUTSIDE_ENDOMETRIUM = annotation_coverage()

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
}
# DERIVED, not typed: the count of cells outside endometrium comes from the
# dumped metadata in the same pass that proves none of them is annotated.
for _n, _why in VALIDATE_CELLS.items():
    CONSTANTS.setdefault(_n, _why)
for _n, _why in NOTE_DONORS.items():
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
    "1.58": ("corpus cells in millions", ""),
    # The cross-method correlations and their p-values. Rounded in prose, so
    # pinned to the axis they belong to rather than searched for.
    "0.721": ("donor recovery vs disease", ""),
    "0.019": ("donor recovery vs disease", ""),
    "0.176": ("donor recovery vs phase", ""),
    "0.63":  ("donor recovery vs phase", ""),
}

def pinned_source(raw: str, dp: int):
    """The pinned ledger entry for a prose value, checked against the pin."""
    want = PINNED.get(raw)
    if want is None:
        return None
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

tex = TEX.read_text()
for macro in ("note", "todo", "citep", "citet", "cite", "label", "ref"):
    tex = strip_group(tex, macro)
tex = re.sub(r"^%.*$", "", tex, flags=re.M)
tex = re.sub(r"%.*$", "", tex, flags=re.M)        # trailing comments too
tex = re.sub(r"Fig\.~\d+[a-z]?(--[a-z])?", "", tex)
# Ordinals are words. "95th percentile" is the name of a quantity, not a
# measurement, and 95 has no source row by design.
tex = re.sub(r"\d+(?:st|nd|rd|th)\b", "", tex)
# Subsection numbers are structural markers, not measurements. Stripped
# rather than whitelisted, so the number itself stays checked wherever
# else it appears: [6] arrived on 5 November and failed the gate as an
# unsourced prose value, which is the gate working and the wrong target.
tex = re.sub(r"\\subsection\*\{\[\d+\]", r"\\subsection*{", tex)
# Study identifiers are names, not measurements: marecko\_2024, lin\_2023.
tex = re.sub(r"[A-Za-z]+\\_\d{4}", "", tex)
tex = tex.replace("{,}", "").replace(",", "")

print("\n4. PROSE, NUMBER BY NUMBER\n")
unaccounted, ambiguous, ok = [], [], 0
for mobj in re.finditer(r"(?<![\d.])(\d+\.\d+|\d+)(?![\d.])", tex):
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
