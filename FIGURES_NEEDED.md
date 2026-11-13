# The five figures the Results prose now assumes

Written 13 November 2026, when Results was drafted and figures were
deliberately deferred. AW: *"Let's leave the figures for after results is
done."* The prose now carries five `(Fig.~X)` placeholders, and this file
says what each one has to show, why prose cannot do it, and roughly what it
might look like. **Nothing here is designed. The nature of each is open.**

The existing display items are in `FIGURES_STRUCTURE.md` and
`figures/scripts/`. These five are additions or panels within them.

---

## F1. Severity does not move composition — R3

**Where:** R3's closing paragraph, "the share of each family was unchanged
between low and high severity".

**Why not prose:** four p-values all above 0.16 is a list of non-results.
A reader cannot see from four numbers that the distributions sit on top of
each other, which is the actual finding.

**Must show:** per-donor family fractions for the 51 patients, low against
high severity, four families. The point is overlap, not a gap.

**Rough shape:** four small paired strip plots or violins, one per family,
with donors as points. Low and high side by side. No stars, no brackets:
the finding is the absence of separation.

⚠ This is the **pinned dissociation panel's** job and that panel already
exists at `figures/pinned/panel_dissociation.png`, built in IBDex Fig 2c's
form. It may need only re-pointing rather than redrawing.

---

## F2. The disease direction exists only inside immune cells — R4

**Where:** R4's third paragraph, after "epithelial cells carry nothing at
all at 0.4663".

**Why not prose:** the finding is a *contrast* between five numbers and
their nulls, and the surprising part is that pooling the families makes it
worse. A reader meeting 0.6048, 0.5920, 0.4663, 0.7084 and 0.6818 in a
sentence cannot see that shape.

**Must show:** held-out AUC per cell family against its shuffled-label null,
with the all-families bar included so the loss from pooling is visible.
Sources: `axw1008/docs/paper/x12_by_family_annotated.csv`.

**Rough shape:** five horizontal bars, one per family plus "all", each with
its null marked as a vertical line or a shaded band, ordered by AUC. A
chance line at 0.5. Immune and the all-families bar are the comparison the
reader needs to make, so they should not be at opposite ends.

---

## F3. The gene ranking, and the asymmetry at its two ends — R4

**Where:** R4's final paragraph, around the replication result.

**Why not prose:** ten gene names and four fold changes is a list. The
finding is that one end of a 15,496-gene ranking replicates an independent
cohort and the other end does not, at p = 3.95e-07. That is a shape.

**Must show:** the ranked per-gene shift along the immune disease direction,
with the four externally replicating genes marked, and the four with no
prior endometriosis report marked differently. Source:
`axw1008/docs/paper/x12_gene_shifts_orth.csv` (15,496 rows) and
`replication_external.csv`.

**Rough shape:** a ranked curve or waterfall across all genes with labelled
points at the extremes, or a volcano-like layout. Both tails must be visible
in one frame, because the control tail replicating nothing is half the
result.

⚠ **This is the figure for the paper's strongest single number** and it does
not exist in any form.

---

## F4. Removing ECS collapses the latent into study territories — R5

**Where:** R5's fourth paragraph, "large single-study territories appearing
that ELAJ_Bhi does not have".

**Why not prose:** the metrics say almost nothing here, 6.4% and 9.5% on the
cost axes. The entire reason ECS is in the model is visible only in the
embedding.

**Must show:** the ELAJ_Bhi latent against the -ECS latent, both coloured by
study. Sources on disk at `Outputs/a_series/a1_noecs/figures/best/` and the
reported arm's own UMAP cache.

**Rough shape:** two UMAPs side by side, coloured by study, same palette and
same axes. The eleven-study palette already exists in `figure1.py`.

---

## F5. The DNS sentinel reorganises the latent — R5

**Where:** R5's fourth paragraph, "there too the reorganisation is visible
rather than measurable".

**Why not prose:** study separation worsens 2.7% and everything else moves
under 1%. The number is small and the effect is not.

**Must show:** the same pairing as F4 for `a1_nodns`. Sources at
`Outputs/a_series/a1_nodns/figures/best/`.

⚠ **F4 and F5 are the same kind of picture** and almost certainly belong in
one Supplementary figure with four panels, not two figures.

---

# Where they go, and the arithmetic

NMI allows **six display items**. Current main set is four: Fig 1, Fig 2 the
frontier, Fig 3 the endometriosis UMAPs, Table 1.

| | likely home | reason |
|---|---|---|
| F2 immune AUCs | **main text** | it is the mechanism behind R4's title |
| F3 gene ranking | **main text** | strongest number in the paper |
| F1 severity composition | Extended Data or a Fig 3 panel | a null, and the panel may already exist |
| F4 + F5 ablation UMAPs | **Supplementary, one figure** | AW's rule: ablations introduced in Results, detailed in Supplementary |

Two main-text additions take the paper to **six, which is the cap exactly.**
That is a decision, not an oversight: it leaves nothing spare if a reviewer
asks for one.

**Open alternative:** F2 and F3 could be two panels of one new figure, which
keeps the count at five and pairs the mechanism with its consequence. That
is probably the better answer and it is AW's call.

---

# The register for drawing these

`figure1.py` carries the settled conventions and they are not re-derivable
cheaply: Arial throughout, 180 mm maximum width, panel letters 10 pt bold,
titles 6.5 pt, body 5.5 pt, **nothing below NMI's 5 pt floor once placed**.
Okabe-Ito for cell families, the eleven-hue study palette with the
yellow-olive-brown band removed. The rule learned the hard way: **size the
layout to fit the type, never the type to fit the layout.**
