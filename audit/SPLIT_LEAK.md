# The García-Alonso leak: measured, 15 November 2026

AW, 15 November: *"There is in fact a leak. I remember measuring it to
around 5% error overall. I think some cells leaked instead of a donor."*

**He is right on both counts, and my earlier write-up was wrong.** Supplementary
Note 3 and `PRIORITY.md` currently say the identifier problem does not touch
any reported held-out number. It does. This file is the measurement.
**Nothing has been edited in the paper yet**, on AW's instruction.

---

## What is NOT wrong

Three things were checked and all three are clean, so the leak is none of
the obvious ones.

| check | result |
|---|---|
| does any `patient_id` appear in more than one split? | **0 of 269** |
| do the fifteen alias pairs straddle the train/test wall? | **0 of 15.** Every person's two ids are on the same side |
| are the two deposits literally the same cells? | **no.** Nearest-neighbour distance between the paired deposits is 0.236 to 0.352 at the minimum, and **zero** cells fall within 0.1 of a cell in their partner deposit |

So the donor-level split holds, and commit `7ed19bd` did what its message
says. That part of my earlier account stands.

## What IS wrong, and it is a cell-level leak

**The cross-donor estimator discards same-donor neighbours by
IDENTIFIER, and fifteen people hold two identifiers each.** A cell of
person X deposited under `garcia_alonso_2021_a` has neighbours that are
cells of the same person under `garcia_alonso_2021_b`, and the estimator
counts every one of those as a **cross-donor** relation.

That is exactly "some cells leaked instead of a donor": no donor crossed
the wall, but the relations that the estimator was built to discard are
being scored.

It bites inside the held-out split, so re-running the split does not fix
it. The fix is to resolve aliases **in the scorer**, not in the splitter.

### Exposure, held-out split (416,256 cells, 51,200 of them dual-identifier)

| measurement | scored cells | dual-id | share |
|---|---:|---:|---:|
| cross-donor menstrual phase | 224,211 | 51,200 | **22.84%** |
| disease, control vs eutopic | 309,283 | 51,200 | **16.55%** |
| donor recovery | 416,256 | 51,200 | **12.30%** |
| cross-donor cell family | 176,803 | 0 | 0.00% |
| cross-donor severity | 176,896 | 0 | 0.00% |
| cross-donor rASRM stage | 44,544 | 0 | 0.00% |
| cross-donor grade | 132,352 | 0 | 0.00% |

Both deposits are **control endometrium carrying a phase label and no
family, severity, stage or grade**. So the exposure is confined to phase,
to disease, and to anything keyed on donor identity. Four of the seven
cross-donor measurements are untouched, and that is structural rather than
lucky.

## The size of the error

Reproduced locally at k=100 on the dumped latent, each measurement computed
twice in one implementation: once keying on the deposited identifier (what
the benchmark does) and once on the resolved person.

| measurement | by identifier | aliases resolved | delta | leaked relations |
|---|---:|---:|---:|---:|
| cross-donor menstrual phase | 0.6980 | 0.6859 | **−0.0121** | **2.83%** |
| disease, control vs eutopic | 0.3608 | 0.3435 | **−0.0173** | **2.00%** |
| donor recovery *(lower is better)* | 0.4745 | 0.4810 | **+0.0065** | — |
| cross-donor cell family | — | — | **0** | **0.00%** |

**Every correction moves against us.** Phase and disease are inflated
because a same-person neighbour carries the same phase and the same disease
status. Donor recovery is understated, because a cell's twin under the other
identifier counts as a *different* donor, which flatters us on the cost axis.

**2.83% and 2.00% of cross-donor relations are same-person.** AW remembered
"around 5%"; the old cell-share audit said 4.3%, and the disease delta is
4.8% in relative terms. His recollection is the right order.

### ⚠ Three cautions on these numbers

1. **They are a reproduction, not a re-scored benchmark.** My phase figure
   by identifier is 0.6980 where the benchmark reports 0.7346, and my kept
   fraction is 45% where it reports 51%, so the estimator differs in some
   detail (which phase levels enter, how coverage is filtered). **The
   deltas are computed within one consistent implementation and are the
   robust part; the absolute values are not the paper's.**
2. **My cell-family reproduction is invalid and the zero does not depend on
   it.** I assigned each donor one family via `groupby.first()`, which is
   wrong for a label that varies within a donor. The 0.00% stands on the
   exposure count instead: no dual-identifier cell carries a family label.
3. **Scaling the deltas onto the reported values is arithmetic, not
   measurement.** On relative terms it would put phase near 0.722, disease
   near 0.320 and donor recovery near 0.526.

## The whole corpus, measured 16 November

AW asked for the size of the effect on a whole-corpus number, remembering
"around 5%". Measured, on a 60,000-cell random query against the full
reference set (a KD-tree over all 736,312 phase-labelled cells in sixteen
dimensions does not finish; the leaked SHARE is a ratio and a random query
sample estimates it without bias):

| whole-corpus measurement | exposed cells | leaked relations | by identifier | resolved | delta |
|---|---:|---:|---:|---:|---:|
| **cross-donor menstrual phase** | 110,336 of 736,312 (**14.98%**) | **1.54%** | 0.6832 | 0.6761 | **−0.0071** |
| cross-donor cell family | **0** | — | — | — | **0** |
| cross-donor severity | **0** | — | — | — | **0** |

**Only one whole-corpus number is exposed at all**, and the other two were
checked rather than assumed. Both García-Alonso deposits are control
endometrium carrying a phase label and nothing else, so family, severity,
stage and grade have exactly zero dual-identifier cells.

**This reproduction is trustworthy where the held-out one was not.** By
identifier it gives 0.6832 against the reported 0.6796, a gap of 0.0036,
so the implementation is tracking the real estimator closely. The held-out
reproduction was 0.6980 against a reported 0.7346 and should be read only
for its delta.

**The honest summary of size.** Three different quantities can be called
"the leak" and they differ by an order of magnitude: 15% of the
phase-labelled cells belong to a duplicated person; 1.54% of the
cross-donor relations join a person to themselves; and the reported figure
is high by 1.0% of its own value. AW's recollection of "around 5%" sits
between the first two. The number that belongs in the paper is the third,
because it is what a reader would have to change.

## The consequence that needs a decision

**The dominance claim must be re-checked, and the correction has to be
applied to all ten representations or to none.**

Our phase figure scaled by the measured relative error lands near 0.722.
Scanorama is reported at 0.7303. On corrected-against-uncorrected numbers
we would lose the cycle axis. But every baseline was scored on the same
corpus with the same duplicated identifiers, so every baseline is inflated
the same way and would fall too. **Comparing a corrected ELAJ against nine
uncorrected competitors would be worse than reporting none of it.**

So the options are:

| | what it costs |
|---|---|
| **(a) re-score all eleven with aliases resolved in the scorer** | one scoring pass per representation; the latents are dumped, so no re-embedding and no retraining. This is the only option that yields quotable corrected numbers |
| **(b) report as is and state the bound** | free. Note 3 gains a paragraph: the leak is 2.0 to 2.8% of relations, it inflates phase and disease and flatters donor recovery, and it applies to every representation equally so the ranking is unaffected |
| **(c) drop the four dual-identifier people from the held-out scoring** | loses 51,200 held-out cells, 12.3%, and changes every number in Table 1 |

**My reading: (a) if there is time, (b) if there is not.** (b) is honest and
survivable precisely because the leak is common to all eleven; what makes it
survivable is saying so, which is why this cannot simply be left out.

## How to reproduce

Aliases come from the dataset loader's own log line, `one donor '<id>' is
also known as ['<id>']`, which the X13 run printed fifteen times
(`Outputs/analysis/x13_markers/x13_61726250.log`). Everything else is the
dumped latent and metadata at `Outputs/cells/p1_dab168_kl1/`. The scripts
used are in this session's transcript; they are three short blocks and were
not committed, because the real fix belongs in
`endo_model/evaluation/sufficient_stats.py` rather than in a one-off.

**The fix, if (a) is chosen:** resolve `patient_id` through `DonorAliases`
inside the scorer before the donor-by-donor matrix is built. One map
applied in one place, and it corrects every cross-donor measurement at once.
