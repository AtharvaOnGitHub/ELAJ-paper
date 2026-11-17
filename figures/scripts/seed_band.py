"""The seed band: a1_seed42 against p1_dab168_kl1, and every arm's effect
measured against it. Writes axw1008/docs/paper/seed_band.csv.

    /Users/atharvawaghmare/miniconda3/envs/elaj/bin/python figures/scripts/seed_band.py

a1_seed42 changes ONLY the training seed (24 -> 42); the donor split is the
base's, so this is the variance of the model, not of the data. TWO RUNS GIVE
A RANGE, NOT A STANDARD DEVIATION: quote "the two seeds differ by X", never
"the standard error is X". Its config's reading rule: if an arm's effect is
smaller than the seed difference on the same axis, the paper must say so.
"""
from pathlib import Path
import pandas as pd
import table1

ROOT = Path("/Users/atharvawaghmare/Endo research/ELAJ")
SEED = ROOT / "Outputs/Benchmarks/full_a1_seed42/benchmark.csv"
DEST = ROOT / "axw1008/docs/paper/seed_band.csv"
K = {"cross-donor menstrual phase": ("cross-donor", "menstrual phase"),
     "cross-donor cell family": ("cross-donor", "cell family"),
     "donor recovery": ("knn-agreement", "patient_id"),
     "study separation": ("study-mixing", "all studies"),
     "disease, pooled cross-donor": ("disease-xdonor", "all studies (pooled)")}
# registered in a1_seed42.yaml BEFORE the run
PREDICTED = {"cross-donor menstrual phase": (.70, .77), "cross-donor cell family": (.975, .988),
             "donor recovery": (.48, .56), "disease, pooled cross-donor": (.30, .37)}
ARMS = ["a1_nophase", "a1_clsonly", "a1_randgroups", "a1_nodns", "a1_noecs",
        "p1_dab7_kl1", "p1_dab336_kl1", "p1_dab7_kl30", "p1_dab168_kl30", "p1_dab336_kl30"]

D = table1.collect()
s = pd.read_csv(SEED)
rows = []
for axis, (t, l) in K.items():
    base = float(D["p1_dab168_kl1"][(t, l)])
    seed = float(s[(s.test == t) & (s.label == l)].value.iloc[0])
    lo, hi = PREDICTED.get(axis, (float("nan"), float("nan")))
    rows.append({"axis": axis, "row": "a1_seed42", "base": base, "value": seed,
                 "delta": seed - base, "ratio_to_seed": 1.0,
                 "predicted_lo": lo, "predicted_hi": hi,
                 "inside_prediction": (lo <= seed <= hi) if lo == lo else None})
    for arm in ARMS:
        v = float(D[arm][(t, l)])
        rows.append({"axis": axis, "row": arm, "base": base, "value": v, "delta": v - base,
                     "ratio_to_seed": abs(v - base) / abs(seed - base)})
out = pd.DataFrame(rows)
out.to_csv(DEST, index=False)
print(out.round(4).to_string(index=False))
