"""The scIB scorecard: ten representations, every metric, one table.

    python figures/scripts/scib_table.py

Writes `Outputs/supplementary/scib/scib_scorecard.csv` and a LaTeX table at
`sections/supp_scib.tex`, and prints which metrics discriminate and which do
not. The figures that go with it are drawn separately.

WHY THIS IS NOT A GLOB. Every row is keyed out of `audit_numbers.py`'s
MANIFEST by method, gene policy and fit split. The baseline table was invalid
for three days because a glob reached whichever benchmark file came first and
mixed the narrow gene policy with the wide one. The MANIFEST is parsed from
the auditor rather than copied, so the two cannot drift.

WHAT THE NOTE THIS FEEDS HAS TO BE FAIR ABOUT. Hrovatin's group wrote scIB.
The claim is that its axes do not discriminate ON THIS CORPUS, never that the
framework is wrong.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
PAPER = Path(__file__).resolve().parents[2]
BENCH = ROOT / "Outputs" / "Benchmarks"
OUT = ROOT / "Outputs" / "supplementary" / "scib"
TEX = PAPER / "sections" / "supp_scib.tex"

# Which half of the scorecard each metric belongs to. scIB's own division:
# batch-correction metrics reward mixing cohorts, bio-conservation metrics
# reward keeping biological structure.
HALF = {
    "scib-ilisi_knn": "batch", "scib-kbet": "batch",
    "scib-pcr_batch": "batch", "scib-silhouette_batch": "batch",
    "scib-graph_connectivity": "batch",
    "scib-clisi_knn": "bio", "scib-ari": "bio", "scib-nmi": "bio",
    "scib-silhouette_bio": "bio", "scib-isolated_labels": "bio",
}
OURS = {"full_p1_dab168_kl1": "ELAJ_B_hi", "full_p1_dab168_kl30": "ELAJ_B_lo"}


def manifest() -> dict:
    src = (PAPER / "figures" / "scripts" / "audit_numbers.py").read_text()
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and any(
                getattr(t, "id", "") == "MANIFEST" for t in node.targets):
            return ast.literal_eval(node.value)
    sys.exit("MANIFEST not found in audit_numbers.py")


def rows() -> pd.DataFrame:
    out = []
    for method, (fname, policy, fit) in manifest().items():
        p = BENCH / fname / "benchmark.csv"
        if not p.exists():
            print(f"  ! {method}: missing {fname}")
            continue
        b = pd.read_csv(p)
        k = b[(b["method"] == method) & (b["gene_policy"] == policy)]
        if fit:
            k = k[k["fit_on"].fillna("") == fit]
        k = k[k["test"].isin(HALF)]
        for _, r in k.iterrows():
            out.append({"representation": method, "metric": r["test"],
                        "half": HALF[r["test"]], "label": r.get("label"),
                        "value": float(r["value"]), "n_cells": r.get("n_cells"),
                        "source": fname})
    for fname, label in OURS.items():
        p = BENCH / fname / "benchmark.csv"
        if not p.exists():
            print(f"  ! {label}: missing {fname}")
            continue
        b = pd.read_csv(p)
        for _, r in b[b["test"].isin(HALF)].iterrows():
            out.append({"representation": label, "metric": r["test"],
                        "half": HALF[r["test"]], "label": r.get("label"),
                        "value": float(r["value"]), "n_cells": r.get("n_cells"),
                        "source": fname})
    return pd.DataFrame(out)


# EVERY scIB METRIC HERE IS BOUNDED. The silhouette variants are normalised
# to [0, 1] by scib-metrics and the rest are proportions or indices in the
# same range, so anything outside [-1, 1] is not a measurement. scFoundation's
# full-split pass was OOM-killed inside silhouette_batch after fifteen hours
# (see audit_numbers.py's MANIFEST note) and wrote -2.95e24 before it died.
# Shipping that in a supplementary table would be a fabricated row.
PLAUSIBLE = (-1.0, 1.0)

# THE ONE RECOVERED VALUE, read from the rerun's log rather than typed.
# Job 61784251 rescored scFoundation with --stages scib over the same dumped
# latent. It computed every `cell family` metric, then OOM-died on the second
# label set (AnnotationRefined), which we do not use, so it never wrote its
# benchmark.csv. The log is the only artefact, and it is kept beside where
# that CSV would have been.
#
# THE RERUN IS COMPARABLE AND THIS IS CHECKED, not assumed: all seven
# metrics it shares with the original pass reproduce to the printed
# precision (ilisi 0.000, clisi 1.000, kbet 0.001, graph_connectivity 0.805,
# pcr_batch 0.769, nmi 0.345, ari 0.233). A silhouette_batch read off a run
# whose other seven values had drifted would not be usable.
RERUN_LOG = BENCH / "scib_scfoundation_rerun" / "scib_scf_61784251.log"
RERUN_CSV = BENCH / "scib_scfoundation_rerun" / "benchmark.csv"


def recovered_silhouette() -> float | None:
    """scFoundation's silhouette_batch, from the CSV if it exists, else the log."""
    if RERUN_CSV.exists():                      # prefer a real scoring file
        b = pd.read_csv(RERUN_CSV)
        hit = b[(b.method == "scfoundation")
                & (b.test == "scib-silhouette_batch")
                & (b.label == "cell family")]
        if not hit.empty:
            return float(hit.value.iloc[0])
    if not RERUN_LOG.exists():
        return None
    import re
    for line in RERUN_LOG.read_text().splitlines():
        if "scib" in line and "cell family" in line and "silhouette_batch=" in line:
            m = re.search(r"silhouette_batch=([\d.]+)", line)
            if m:
                return float(m.group(1))
    return None


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    long = rows()
    if long.empty:
        sys.exit("no scIB rows found")

    bad = long[(long["value"] < PLAUSIBLE[0]) | (long["value"] > PLAUSIBLE[1])
               | long["value"].isna()]
    if not bad.empty:
        bad.to_csv(OUT / "scib_quarantined.csv", index=False)
        print("QUARANTINED, outside the metric's own bounds and therefore "
              "not a measurement:")
        for _, r in bad.iterrows():
            print(f"    {r['representation']:14} {r['metric']:26} "
                  f"{r['value']:.4g}   from {r['source']}")
        print()
        rec = recovered_silhouette()
        if rec is not None:
            mask = ((long["representation"] == "scfoundation")
                    & (long["metric"] == "scib-silhouette_batch")
                    & (long["label"] == "cell family"))
            long.loc[mask, "value"] = rec
            long.loc[mask, "source"] = RERUN_LOG.parent.name
            bad = bad[~bad.index.isin(long[mask].index)]
            print(f"RECOVERED scfoundation silhouette_batch = {rec:.4f} "
                  f"from {RERUN_LOG.parent.name}\n")
        long = long.drop(bad.index)

    long.to_csv(OUT / "scib_scorecard_long.csv", index=False)

    # ONE LABEL SET PER TABLE, and this was a bug worth catching. These files
    # score every scIB metric against TWO label sets: `cell family` over
    # 176,803 cells and `AnnotationRefined` over 132,261. The first version of
    # this script pivoted without `label` and let aggfunc="first" pick
    # whichever row the file happened to hold first, so two different
    # measurements landed in one cell and the spreads mixed them. The paper
    # reports cell family, so that is the scorecard; AnnotationRefined gets
    # its own file. Three batch metrics exist only for cell family.
    counts = long.groupby("label")["value"].size().sort_values(ascending=False)
    print(f"  label sets present: "
          f"{', '.join(f'{k} ({v} rows)' for k, v in counts.items())}\n")

    PRIMARY = "cell family"
    for lab, tag in ((PRIMARY, "scib_scorecard"),
                     ("AnnotationRefined", "scib_scorecard_annotationrefined")):
        sub = long[long["label"] == lab]
        if sub.empty:
            continue
        w = (sub.pivot_table(index="representation", columns="metric",
                             values="value", aggfunc="first")
                .reindex(columns=[m for m in sorted(HALF, key=lambda x: (HALF[x], x))
                                  if m in set(sub["metric"])]))
        w.to_csv(OUT / f"{tag}.csv")
        if lab != PRIMARY:
            print(f"  {lab}: {w.shape[0]} x {w.shape[1]} -> {tag}.csv")

    long = long[long["label"] == PRIMARY]
    wide = (long.pivot_table(index="representation", columns="metric",
                             values="value", aggfunc="first")
                .reindex(columns=sorted(HALF, key=lambda m: (HALF[m], m))))

    print(f"scIB scorecard: {wide.shape[0]} representations x "
          f"{wide.shape[1]} metrics -> {OUT.relative_to(ROOT)}\n")
    print("  metric                     half    min      max      spread  discriminates?")
    verdict = []
    for m in wide.columns:
        v = wide[m].dropna()
        if v.empty:
            continue
        spread = v.max() - v.min()
        # A metric that assigns every representation the same value cannot
        # rank them. The threshold is not a convention, it is the point at
        # which the spread is smaller than the rounding the paper reports.
        flat = spread < 0.01
        verdict.append({"metric": m, "half": HALF[m], "n": len(v),
                        "min": v.min(), "max": v.max(), "spread": spread,
                        "degenerate": flat})
        print(f"  {m:26} {HALF[m]:6} {v.min():8.4f} {v.max():8.4f} "
              f"{spread:8.4f}  {'NO' if flat else 'yes'}")
    pd.DataFrame(verdict).to_csv(OUT / "scib_discrimination.csv", index=False)

    near = [v for v in verdict if not v["degenerate"] and v["spread"] < 0.05]
    if near:
        print("\n  near-degenerate, spread under 0.05 and worth saying so "
              "rather than moving the threshold:")
        for v in near:
            print(f"      {v['metric']}  spread {v['spread']:.4f} "
                  f"({v['half']} half)")

    dead = [v["metric"] for v in verdict if v["degenerate"]]
    print(f"\n  {len(dead)} of {len(verdict)} metrics do not discriminate "
          f"on this corpus:")
    for m in dead:
        print(f"      {m}  ({HALF[m]} half)")
    halves = {h for m in dead for hh, h in [(m, HALF[m])]}
    if {"batch", "bio"} <= halves:
        print("  Both halves of the scorecard are represented among them.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
