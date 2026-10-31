# Figures

Every script here regenerates its output from
`Outputs/cells/p1_dab168_kl1/` and `Outputs/Benchmarks/`, with one command
and no arguments. That is reproducibility item R5.

```
/Users/atharvawaghmare/miniconda3/envs/elaj/bin/python figures/scripts/<name>.py
```

All of them run locally in seconds to under a minute. **None of them needs
the HPC** — the GPU is only required to produce the latent, which is already
dumped.

| script | makes | time |
|---|---|---|
| `figure1.py` | the main Figure 1 composite | ~20 s |
| `movie_cycle.py` | two-panel cycle animation, day + phase | ~11 s |
| `movie_cycle_by_celltype.py` | the same, split by cell type | ~14 s |
| `phase_groups.py` | phase small multiples, all cell types | ~15 s |
| `phase_by_study_stromal.py` | phase within stromal, split by contributing study | ~15 s |
| `donors_discrete.py` | 60 donors, one hue each, ordered by cycle day | ~20 s |
| `panel_d_options.py` | three candidate panels for Figure 1d | ~10 s |

## The trick that makes the animations cheap

The grey background is drawn once as a persistent artist and only the
highlighted cells are redrawn per frame — about 35,000 points instead of
400,000. Rendering 104 frames takes 14 seconds rather than the minutes a
naive redraw would cost, which is why none of this went to the HPC.

## Things learned the hard way

**The UMAP subsample must match the cache.** `np.random.default_rng(24)
.choice(len(latent), 400_000, replace=False)`, then `np.sort`. The cached
embedding at `Outputs/analysis/umaps/<arm>/_umap_cache/global_400000.npy` is
keyed on sample size alone, so a different seed silently pairs cells with
other cells' coordinates.

**Do not put a near-background colour in a cyclic colormap.** The first
cycle animation used our berry map, whose midpoint is cream, and day 15
vanished against the grey background — the middle of the cycle, which is the
most interesting part.

**Check a phase panel against study before believing it.** `periovulatory`
is 100% duempelmann, so its clean region is a study region. The other three
groups span two or more studies and their territories overlap across them,
which is the claim worth making.
