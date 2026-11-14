"""Supplementary Data D1-D5, the machine-readable tier.

    python figures/scripts/supplementary_data.py

Writes to `Outputs/supplementary/data/`, which is outside both git repos
because these are regenerable artefacts and D4 is 1.6 million rows.

WHAT THIS IS NOT. Supplementary Data is the tier nobody reads top to bottom.
Typeset tables that a reader looks up go in Supplementary Tables, and a table
that only means something inside an argument stays in its Note. See
SUPPLEMENTARY_STRUCTURE.md.

NOTHING HERE CAN CHANGE AS THE PAPER IS WRITTEN. Every item is an output of
the frozen reported arm, and the standing rule is no more edits to the
architecture, parameters or optimiser. The only way this moves is if we ship
more, which is additive.
"""
from __future__ import annotations

import ast
import gzip
import json
import shutil
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
PAPER = Path(__file__).resolve().parents[2]
CLAIMS = ROOT / "axw1008" / "docs" / "paper"
BENCH = ROOT / "Outputs" / "Benchmarks"
CELLS = ROOT / "Outputs" / "cells"
VOCAB = ROOT / "axw1008" / "src" / "data" / "vocabulary_v1.json"
ARM = "p1_dab168_kl1"
OUT = ROOT / "Outputs" / "supplementary" / "data"


def manifest() -> dict:
    """The comparable-run manifest, read from the auditor rather than copied.

    Copying it is how the baseline table was invalid for three days: a glob
    reached whichever benchmark file came first and mixed gene policies across
    methods. `audit_numbers.py` executes on import, so the literal is parsed
    out with ast instead of imported.
    """
    src = (PAPER / "figures" / "scripts" / "audit_numbers.py").read_text()
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                getattr(t, "id", "") == "MANIFEST" for t in node.targets):
            return ast.literal_eval(node.value)
    sys.exit("MANIFEST not found in audit_numbers.py")


def d1_gene_shifts() -> tuple[str, pd.DataFrame]:
    """Every gene's shift along the immune disease direction."""
    df = pd.read_csv(CLAIMS / "x12_gene_shifts_orth.csv")
    # the source CSV writes the gene symbol into an unnamed index column, and
    # a shipped file cannot have one: a reader loading it gets "Unnamed: 0".
    if df.columns[0].startswith("Unnamed") or df.columns[0] == "":
        df = df.rename(columns={df.columns[0]: "gene"})
    # positive values move towards disease, which the column name alone does
    # not say, so the sign convention travels with the file
    df = df.assign(shift_towards_disease=-df["shift_towards_control"])
    return "D1_gene_shifts_immune_disease_direction", df


def d2_benchmark_grid() -> tuple[str, pd.DataFrame]:
    """Every method on every axis, from the manifest's files by exact key."""
    man = manifest()
    frames = []
    for method, (fname, policy, fit) in man.items():
        p = BENCH / fname / "benchmark.csv"
        if not p.exists():
            print(f"  ! {method}: no {p.relative_to(ROOT)}")
            continue
        b = pd.read_csv(p)
        keep = b[(b["method"] == method) & (b["gene_policy"] == policy)]
        if fit:
            keep = keep[keep["fit_on"].fillna("") == fit]
        keep = keep.assign(manifest_file=fname)
        frames.append(keep)
    # our own arms are not in the baseline manifest; they are their own files
    for arm in ("full_p1_dab168_kl1", "full_p1_dab168_kl30"):
        p = BENCH / arm / "benchmark.csv"
        if p.exists():
            frames.append(pd.read_csv(p).assign(manifest_file=arm))
    df = pd.concat(frames, ignore_index=True)
    return "D2_benchmark_grid_all_methods_all_axes", df


def d3_composition() -> tuple[str, pd.DataFrame]:
    """Per-donor cell-family fractions, the frame behind the composition tests."""
    meta = pd.read_csv(CELLS / ARM / "metadata.csv.gz", low_memory=False)
    fam = pd.read_csv(CELLS / ARM / "cell_family_transferred.csv.gz")
    col = next((c for c in fam.columns if "family" in c.lower()), fam.columns[-1])
    donor = next(c for c in ("patient_id", "donor_id", "donor") if c in meta.columns)
    # THE REAL COLUMN NAMES, checked against the dump rather than guessed.
    # `severity (study vocabularies)` is deliberately excluded: scorer.py
    # documents it as readable off study identity alone, so it must not travel
    # in a shipped file where someone could contrast on it. The merged scale
    # is the valid one. See NUMBERS.md.
    keys = [k for k in (donor, "study", "tissue", "disease_status", "phase")
            if k in meta.columns]
    frame = meta[keys].copy()
    frame["cell_family"] = fam[col].values
    # the ground-truth label where a study supplied one, so a reader can see
    # which rows rest on transfer and which do not
    if "cell family" in meta.columns:
        frame["cell_family_annotated"] = meta["cell family"].values
        keys = keys + ["cell_family_annotated"]
    counts = (frame.groupby(keys + ["cell_family"], dropna=False)
                   .size().rename("n_cells").reset_index())
    tot = counts.groupby(keys, dropna=False)["n_cells"].transform("sum")
    counts["fraction"] = counts["n_cells"] / tot
    return "D3_per_donor_cell_family_composition", counts


def d4_transferred_labels() -> tuple[str, Path]:
    """The transferred cell-family label for every cell. Copied, not rebuilt."""
    src = CELLS / ARM / "cell_family_transferred.csv.gz"
    dest = OUT / "D4_transferred_cell_family_labels.csv.gz"
    shutil.copyfile(src, dest)
    with gzip.open(dest, "rt") as fh:
        rows = sum(1 for _ in fh) - 1
    return "D4_transferred_cell_family_labels", dest, rows  # type: ignore[return-value]


def d5_groups() -> tuple[str, pd.DataFrame]:
    """The 44 pathway groups and the genes in each.

    This is the file a reproducer needs. It is what makes the inductive bias
    auditable rather than asserted, since the random-group ablation is only
    interpretable against the real partition.
    """
    v = json.loads(VOCAB.read_text())
    rows = [{"gene": g, "group": d.get("group"), "group_idx": d.get("group_idx"),
             "global_idx": d.get("global_idx"), "chromosome": d.get("chromosome")}
            for g, d in v.items()]
    df = pd.DataFrame(rows).sort_values(["group_idx", "gene"], kind="stable")
    return "D5_pathway_groups_and_genes", df


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    print(f"Supplementary Data -> {OUT.relative_to(ROOT)}\n")

    for fn in (d1_gene_shifts, d2_benchmark_grid, d3_composition, d5_groups):
        name, df = fn()
        dest = OUT / f"{name}.csv"
        df.to_csv(dest, index=False)
        print(f"  {name:48} {len(df):>9,} rows x {df.shape[1]} cols")

    name, dest, rows = d4_transferred_labels()
    print(f"  {name:48} {rows:>9,} rows  (gzip, copied)")

    groups = pd.read_csv(OUT / "D5_pathway_groups_and_genes.csv")
    n_groups = groups["group"].nunique()
    print(f"\n  D5 check: {n_groups} groups, "
          f"{groups['gene'].nunique():,} genes assigned")
    if n_groups != 44:
        print(f"  ! expected 44 groups, found {n_groups}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
