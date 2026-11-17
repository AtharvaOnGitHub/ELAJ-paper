"""Tables for the Supplementary Methods, generated, never typed.

    /Users/atharvawaghmare/miniconda3/envs/elaj/bin/python figures/scripts/supp_methods.py

Writes supplementary/tables/hyperparameters.tex from the reported model's own
resolved configuration (run_config.json, every value the run actually used)
and its training log (parameter count, selected epoch), so the table cannot
drift from the run. AW, 15 Nov: "Training hyperparameters, with a table".
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path("/Users/atharvawaghmare/Endo research/ELAJ")
RUN = ROOT / "Outputs/p_series/p1_dab168_kl1"
TAB = Path(__file__).resolve().parents[2] / "supplementary" / "tables"


def main() -> None:
    c = json.load(open(RUN / "run_config.json"))
    M, T, D = c["model"], c["training"], c["data"]
    log = (RUN / "train_57935604.log").read_text()
    n_params = re.search(r"Model parameters: ([\d,]+)", log).group(1)
    met = pd.read_csv(RUN / "metrics.csv")
    best = met.loc[met.val_nb.idxmin()]
    assert int(best.epoch) == 4, best.epoch            # the checkpoint every number uses

    def f(x):
        return f"{x:g}" if isinstance(x, float) else str(x)

    rows = [
        ("Input", None),
        ("Count scaling", "log, library size scaled to " + f"{int(M['tokens']['target_sum']):,}".replace(",", "{,}")),
        ("Value encoding", "one learned direction per gene, scaled by its count"),
        ("Token width $d$", f(M["d_token"])),
        ("Genes, groups", f"15{{,}}496 genes in {M['n_groups']} groups"),
        ("Gene encoder", None),
        ("Transformer layers per group", f(M["group_encoder"]["n_layers"])),
        ("Attention heads", f(M["group_encoder"]["n_heads"])),
        ("Dropout", f(M["group_encoder"]["dropout"])),
        ("Summary tokens per group", "9 (1 learned, 8 pooled statistics)"),
        ("Size buckets", f(M["group_encoder"]["n_buckets"])),
        ("Cell encoder", None),
        ("Transformer layers", f(M["aggregation_encoder"]["n_layers"])),
        ("Attention heads", f(M["aggregation_encoder"]["n_heads"])),
        ("Dropout", f(M["aggregation_encoder"]["dropout"])),
        ("Width $d_{\\mathrm{agg}}$", f(M["d_agg"])),
        ("Latent", None),
        ("Gaussian dimensions", f(M["d_gauss"])),
        ("Circular dimensions", f(M["n_circular"])),
        ("Decoder", None),
        ("Width $d_{\\mathrm{dec}}$", f(M["d_dec"])),
        ("Tissue, platform, study embeddings", f"{M['d_tissue']}, {M['d_platform']}, {M['d_study']} dimensions"),
        ("Covariates zeroed per step", f"probability {f(M['drain']['blank_covariates_p'])}"),
        ("Objective", None),
        ("Reconstruction weight $w_{\\mathrm{nb}}$", f(M["loss"]["w_nb"])),
        ("KL weight $w_{\\mathrm{kl}}$", f(M["loss"]["w_kl_gauss"])),
        ("KL ramp", f"0 to {f(T['kl_annealing']['beta_max'])} over the first "
                    f"{int(T['kl_annealing']['warmup_fraction'] * 100)}\\% of steps"),
        ("KL free bits", f(M["loss"]["free_bits"])),
        ("Adversary weight $w_{\\mathrm{dab}}$, reversal $\\lambda_{\\mathrm{dab}}$",
         f"{f(M['loss']['w_dab'])}, {f(M['dab']['lambda_dab'])}"),
        ("Adversary network", f"{M['dab']['n_layers']} layers, {M['dab']['hidden_dim']} hidden units"),
        ("Phase head weight, label smoothing",
         f"{f(M['loss']['w_cls'])}, {f(M['classifier']['label_smoothing'])}"),
        ("Cell-similarity weight, threshold",
         f"{f(M['loss']['w_ecs'])}, {f(M['ecs']['threshold'])}"),
        ("Optimisation", None),
        ("Optimiser", f"{T['optimizer']['name']}, $\\beta = ({T['optimizer']['betas'][0]}, {T['optimizer']['betas'][1]})$"),
        ("Learning rate, weight decay", f"$10^{{-3}}$, $10^{{-4}}$" if (T['optimizer']['lr'], T['optimizer']['weight_decay']) == (0.001, 0.0001)
         else f"{f(T['optimizer']['lr'])}, {f(T['optimizer']['weight_decay'])}"),
        ("Schedule", f"cosine over {T['max_epochs']} epochs"),
        ("Batch size", f(T["batch_size"])),
        ("Gradient clipping", f"norm {f(T['grad_clip_norm'])}"),
        ("Precision", "bf16"),
        ("Early stopping", f"held-out reconstruction, patience {T['early_stop_patience']} "
                           f"after {T['early_stop_warmup_epochs']} epochs"),
        ("Selected epoch", f"{int(best.epoch)} (held-out reconstruction {best.val_nb:.4f})"),
        ("Data", None),
        ("Split", f"by donor, {int(100 - 100 * (D['splits']['val_fraction'] + D['splits']['test_fraction']))}/"
                  f"{int(100 * D['splits']['val_fraction'])}/{int(100 * D['splits']['test_fraction'])}, seed {D['splits']['seed']}"),
        ("Training seed", f(c["experiment"]["seed"])),
        ("Parameters", n_params.replace(",", "{,}")),
    ]
    L = [r"\begin{tabular}{@{}ll@{}}", r"\toprule", r"Setting & Value \\", r"\midrule"]
    first = True
    for k, v in rows:
        if v is None:
            if not first:
                L.append(r"\addlinespace")
            L.append(rf"\multicolumn{{2}}{{@{{}}l}}{{\textit{{{k}}}}} \\")
            first = False
        else:
            L.append(rf"\quad {k} & {v} \\")
    L += [r"\bottomrule", r"\end{tabular}"]
    TAB.mkdir(parents=True, exist_ok=True)
    (TAB / "hyperparameters.tex").write_text(
        "% GENERATED by figures/scripts/supp_methods.py from run_config.json. Do not edit.\n"
        + "\n".join(L) + "\n")
    print(f"wrote {TAB / 'hyperparameters.tex'} ({sum(v is not None for _, v in rows)} settings)")


if __name__ == "__main__":
    main()
