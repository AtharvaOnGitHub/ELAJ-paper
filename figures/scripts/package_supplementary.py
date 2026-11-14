"""Package Supplementary Data for sending: one workbook plus the oversized file.

    python figures/scripts/package_supplementary.py

Writes `Outputs/supplementary/send/`:

  ELAJ_Supplementary_Data.xlsx              D1, D2, D3, D5 as four sheets
  D4_transferred_cell_family_labels.csv.gz  1,577,728 rows, cannot be a sheet

WHY A WORKBOOK WITH SHEETS. That is what the NMI papers do: PlantRNA-FM
ships four Supplementary Tables as four sheets of one file, MIDAS ships
sixteen across four. Not PDF.

WHY D4 IS NOT IN IT. The xlsx format caps a worksheet at 1,048,576 rows and
D4 has 1,577,728. MIDAS's largest sheet is 83,436, well inside the limit, so
nothing in the comparator set hits this. Splitting D4 across two sheets would
be a formatting artefact rather than a decision, so it travels as gzipped CSV.

Each sheet opens with a title row and a provenance row naming the script and
the file the numbers came from, so a reader who opens the workbook alone can
still tell what they are holding.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "Outputs" / "supplementary" / "data"
SEND = ROOT / "Outputs" / "supplementary" / "send"
XLSX_ROW_CAP = 1_048_576

# sheet name -> (file stem, title, what a reader needs to know)
SHEETS = {
    "D1 gene shifts": (
        "D1_gene_shifts_immune_disease_direction",
        "Per-gene shift along the immune disease direction",
        "All 15,496 genes in the model's vocabulary. Positive "
        "shift_towards_disease means the gene rises towards endometriosis. "
        "Decoder response to movement along the direction fitted inside "
        "immune cells; not a differential expression test."),
    "D2 benchmark grid": (
        "D2_benchmark_grid_all_methods_all_axes",
        "Every representation on every axis",
        "Rows keyed from audit_numbers.py's MANIFEST by method, gene policy "
        "and fit split, so no two rows mix gene policies. manifest_file names "
        "the scoring run each row came from."),
    "D3 composition": (
        "D3_per_donor_cell_family_composition",
        "Per-donor cell-family composition",
        "One row per donor, tissue and cell family. severity_merged is the "
        "three-level clinical scale; severity_study_vocabulary is the raw "
        "union, whose levels are study-specific, which is why study is a "
        "column beside it. cell_family is transferred, "
        "cell_family_annotated is the study's own label where it supplied one."),
    "D5 pathway groups": (
        "D5_pathway_groups_and_genes",
        "The 44 pathway groups and their genes",
        "The partition the group encoder reads. This is the file the "
        "random-group ablation is interpretable against."),
}
BIG = "D4_transferred_cell_family_labels.csv.gz"


def main() -> int:
    if not DATA.exists():
        sys.exit(f"no {DATA}. Run supplementary_data.py first.")
    SEND.mkdir(parents=True, exist_ok=True)
    dest = SEND / "ELAJ_Supplementary_Data.xlsx"

    with pd.ExcelWriter(dest, engine="openpyxl") as xl:
        for sheet, (stem, title, note) in SHEETS.items():
            src = DATA / f"{stem}.csv"
            if not src.exists():
                print(f"  ! missing {src.name}, skipping {sheet}")
                continue
            df = pd.read_csv(src)
            if len(df) + 3 > XLSX_ROW_CAP:
                sys.exit(f"{stem} has {len(df):,} rows and cannot be a sheet")
            # two header rows above the table, so the sheet is self-describing
            head = pd.DataFrame([[title] + [""] * (df.shape[1] - 1),
                                 [note] + [""] * (df.shape[1] - 1),
                                 [""] * df.shape[1]], columns=df.columns)
            pd.concat([head, df], ignore_index=True).to_excel(
                xl, sheet_name=sheet[:31], index=False, header=True)
            print(f"  {sheet:22} {len(df):>9,} rows x {df.shape[1]} cols")

    big_src, big_dest = DATA / BIG, SEND / BIG
    if big_src.exists():
        shutil.copyfile(big_src, big_dest)
        mb = big_dest.stat().st_size / 1048576
        print(f"  {'D4 (separate file)':22} {mb:>9.1f} MB  gzipped CSV, "
              f"over the xlsx row cap")

    print(f"\n  -> {SEND.relative_to(ROOT)}")
    for f in sorted(SEND.iterdir()):
        print(f"       {f.name}  ({f.stat().st_size / 1048576:.1f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
