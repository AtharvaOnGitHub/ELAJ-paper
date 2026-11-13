# How a Discussion is actually written

Built 14 November 2026, because AW asked whether the Discussion inventory
had been checked against published Discussions and it had not. It was built
from our own files. This is the correction.

**Eight Discussions read in full**, chosen so the set is not two data points:

| paper | venue | why it is in the set |
|---|---|---|
| **IBDex** | medRxiv, Acharjee | the supervisor's own paper and the register we already write to |
| **scGPT** | Nat. Methods 2024 | the model we compete with, on disk |
| **TIGON** | **NMI** 2024 | single-cell, generative, closest method shape to ours |
| **DLVPM** | **NMI** 2025 | latent-variable model applied to one disease |
| **Cancer imaging FM** | **NMI** 2024 | a foundation-model paper arguing for its own scale |
| **PlantRNA-FM** | **NMI** 2024 | foundation model plus interpretability |
| **MIDAS** | **NMI** 2026 | disease ML with biology findings, baselines and a long limitations run |
| **Eye2Gene** | **NMI** 2025 | the clinical-diagnosis argument, closest to our staging case |

The six NMI papers were downloaded from Europe PMC as full-text XML and are
kept at `Atharva Papers/NMI_register/`, with each Discussion extracted
beside it as `*_discussion.txt`. Nothing here is from memory.

⚠ **AW's warning governs this file.** Prose statistics are blurry. So the
evidence below is quoted sentences, and the only counts used are ones where
the count **is** a structural fact rather than a measure of style: whether a
Discussion quotes measured values at all, whether it has subheadings, how
long it is against its own Results. Each is flagged.

---

## 1. What a Discussion contains

**Not a summary of findings. A sequence of claims about what the findings
mean**, each one paragraph, each pointing outward: at the design choice that
made the result possible, at the prior work it agrees or disagrees with, at
the mechanism behind it, or at what it cannot support.

The recurring content, present in at least six of the eight:

1. **One opening paragraph naming the contribution** and what the design
   does, not what the numbers were.
2. **A mechanism paragraph: why it worked.** This is the one I would not
   have predicted and it appears everywhere.
3. **Comparison to prior work by name**, often several papers in one
   paragraph.
4. **A conceptual clarification**, explaining what the measurement *is* as
   distinct from what readers will assume it is.
5. **A signposted limitations block**, one to three paragraphs near the end.
6. **Next steps**, concrete and often naming the experiment.
7. **A closing paragraph stating the contribution at its widest.**

**The mechanism move, which is the register's signature.** IBDex on what
PACP is:

> "Its distinction from DE is one of estimand. DE measures observed group
> differences, whereas PACP queries the decoder along a fixed phenotype
> direction under a specified anatomy."

No numbers. It defines the measurement against the thing a reader will
mistake it for. **We have exactly this to do for cross-donor agreement**,
which a reader will read as a clustering metric.

---

## 2. How it contrasts with Results

**It re-traverses the same findings and drops every number.** The cancer
foundation-model paper's first paragraph walks all three of its use cases
again, in words:

> "We showed that our foundation model provided superior performance for
> anatomical lesion site classification on average and across individual
> anatomical sites, even when very few training samples were available for
> that site. Similarly, for malignancy prediction, our model outperformed
> all other baseline approaches."

That is a restatement of the entire Results section with **not one metric in
it.** NMI's "do not restate Results" is not a ban on revisiting the
findings. It is a ban on **re-reporting the measurements.**

**The structural fact, and it is the most important thing in this file.**

| | words | distinct measured values quoted |
|---|---:|---:|
| **our draft** | **1,184** | **25** |
| IBDex | 796 | **0** |
| scGPT | 390 | **0** |
| TIGON | 744 | **0** |
| DLVPM | 763 | **0** |
| MIDAS | 995 | **0** |
| Cancer imaging FM | 1,226 | 1 |
| PlantRNA-FM | 661 | 2 |
| Eye2Gene | 1,466 | 3 |

**Our Discussion quotes more measured values than all eight published
Discussions put together, four times over.** It currently carries 0.3364,
0.7613, 0.9820, 0.6457, 0.4869, ρ = +0.721, ρ = −0.6503, `val_nb` 0.3911 and
0.4024, 34.5%, 4.3%, 2.87%, 0.0076, 0.129, 0.005, 0.019 and more.

**What numbers DO appear in a published Discussion**, and the distinction is
sharp:

- **Data and cohort scale, freely.** "trained on one of the world's largest
  datasets of genotyped individuals with IRD (n = 2,451)"; "we pretrained on
  11,467 lesion volumes... from 5,513 unique CT scans"; "only four previous
  studies... all in much smaller datasets of fewer than 150 patients."
- **A performance value only where it is immediately explained.**
  PlantRNA-FM is the one paper that quotes its own scores, and look what
  happens next: *"achieved the best F1 scores of 0.974 and 0.958... The
  outperformance of our PlantRNA-FM is **probably due to** the combination of
  both RNA sequence and structure information."* The number is a hook for a
  mechanism, not a report.
- **Inside the limitations block, to bound the damage.** Eye2Gene admits
  worse accuracy on some patient groups and then: *"Nonetheless in spite of
  dataset limitations, as it stands, Eye2Gene performance is within the
  anticipated accuracy (<5%)... top-five accuracy is consistently above 70%
  even in the ethnically distinct Tokyo site."*

**So our 1,500 donors, 1,577,728 cells, eleven studies, 254 donors,
1,883,986 parameters and 100 million are all fair game. Our agreement
values, AUCs, rhos and p-values are not**, except where one is the hook for
a mechanism or the bound on a limitation.

---

## 3. How long it is

**The structural fact:** Discussion length tracks Results length, and the
ratio is tight.

| paper | Results | Discussion | ratio |
|---|---:|---:|---:|
| DLVPM | 7,363 | 763 | 10% |
| TIGON | 3,966 | 744 | 19% |
| PlantRNA-FM | 2,217 | 661 | 30% |
| MIDAS | 3,278 | 995 | 30% |
| Cancer imaging FM | 3,165 | 1,226 | 39% |
| **IBDex** | **1,798** | **796** | **44%** |
| Eye2Gene | 2,853 | 1,466 | 51% |

Mean across the six NMI papers: **30%.** IBDex, the shortest Results in the
set and the nearest to ours, sits at 44%.

**Our Results is 1,650 words.** So the range this set licenses is **500
words at the NMI mean, about 730 at IBDex's ratio, and 840 at the most
generous ratio anywhere in the set.**

⚠ **This overturns what I told AW yesterday and the correction matters.** I
said the budget "does not close" and proposed trimming about 250 words from
1,184 while adding 600 of claims-axis material. The real position is that
the draft should land near **750 words**, so it has to **lose about a
third** while absorbing all nine type J items.

**And the two problems solve each other.** The 25 measured values are what
is eating the space. Removing them is not a cut to the argument, it is the
register correction, and it frees roughly the room type J needs.

---

## 4. How it is structured

**Eight out of eight have no subheadings in the Discussion.** Zero `<sec>`
children in all six NMI XMLs, none in IBDex, none in scGPT. This is a
structural fact and it settles the open question.

**What carries the sectioning instead is the first sentence of every
paragraph.** IBDex's ladder, read down:

> Using IBDex as a fixed patient-scale reference revealed that…
> This fixed-reference design remained biologically informative…
> Within this fixed reference, PACP revealed…
> The same fixed coordinate system also transferred beyond…
> IBDex provided the clearest clinical interpretation by showing…
> Applying the same frozen geometry to longitudinal treatment showed…
> Across these applications, anatomical conditioning remained…
> Several limitations define the supported interpretation.
> The decisive next step is prospective validation.
> IBDex establishes a frozen patient-scale atlas that…

**Ten paragraphs, and the opening words alone are a table of contents.**
Each one names its own subject and three of them carry the previous
paragraph's subject forward ("This fixed-reference design", "Within this
fixed reference", "The same fixed coordinate system"). That is how a
Discussion is sectioned without headers, and **it is the supervisor's own
paper doing it.**

**Paragraph size is not uniform across the set and does not need to be.**
IBDex runs 61 to 102 words, ten paragraphs, strikingly even. MIDAS runs
three-sentence paragraphs beside 200-word ones, twelve in total. Eye2Gene
has a 400-word limitation paragraph next to a two-sentence one. So **short
paragraphs are permitted here**, which is not true of our Results.

**Where the limitations sit is consistent:** a signposted block in the last
third, never interleaved with the paragraphs that make the case.

> "Several limitations define the supported interpretation." (IBDex)
> "Despite the versatility and power of DLVPM, several limitations warrant
> careful consideration. First… Another weakness… Another technical issue…"
> "Despite these successes, MIDAS has limitations. First…" then "Second…"
> and "Third…" as three separate paragraphs.
> "Despite the strengths outlined in our study, we recognize several
> limitations that need to be addressed before the clinical applicability."

---

## 5. What a Discussion sentence looks like

Results makes its point with a number. **A Discussion sentence makes its
point with a mechanism, a comparison, or a consequence**, and it is allowed
to hedge in a way Results is not.

**The claim-plus-mechanism pair, the commonest shape in the set:**

> "DLVPM is superior to classical approaches to path modelling in terms of
> the magnitude of associations the method is able to establish between
> different data types. **This is likely because**, in contrast to classical
> approaches, this method is able to model the complex breakdown in
> molecular machinery that underpins carcinogenesis."

A comparative win asserted qualitatively, then a reason, then a hedge. No
metric anywhere near it.

**The generalisation, which closes paragraphs:**

> "**More broadly,** conditional generative models can retain clinically
> meaningful context as an explicit control instead of discarding it as
> nuisance variation." (IBDex)

> "This **suggests** that pathways, rather than individual genes, may be the
> more transportable biological unit across intestinal compartments." (IBDex)

**The flat requirement, stated without apology and pushed to Supplementary:**

> "TIGON requires adequate numbers of cells and time points (Supplementary
> Fig. 15 and Supplementary Note 8)."

**The scale comparison, which is how prior work is beaten here:**

> "So far, only four previous studies have tried to apply AI to IRDs, all in
> much smaller datasets of fewer than 150 patients and across substantially
> fewer genes (Supplementary Table 1)."

**Hedging vocabulary is everywhere and it is not weakness.** "likely
because", "probably due to", "may be", "could indicate", "These data imply",
"is probably driven by", "suggests". MIDAS interprets its own biology almost
entirely in this register. **Results earns the right to be flat because it
shows the number; the Discussion hedges because it is reasoning past the
number.**

⚠ **The one thing our draft already does right.** Its interpretive sentences
are good: *"Cell identity is something every method here recovers and
therefore something that cannot rank methods."* That is the register. It is
the numbers crowded around them that are wrong.

---

## 6. How praiseful, and does it admit bad things

**Confident in words, unflinching about scope.** The praise is qualitative
and unhedged: "superior performance", "robust performance", "strong
potential", "marks an important step forward", "staunchly supports". None of
it is quantified in the Discussion.

**And every one of the eight volunteers something damaging.** This is not a
genre that hides.

- **scGPT, on itself**: *"Notably, the current pretraining does not
  inherently mitigate batch effects, and thus the model's zero-shot
  performance could be constrained on datasets with substantial technical
  variation."* ⚠ **This is a gift and it should be cited.** The model we
  compete with names, in its own Discussion, the exact weakness our corpus
  exposes.
- **Eye2Gene** concedes a competing method is better for some uses:
  *"quantitative analysis of biomarkers with conventional statistical
  approaches… may be preferable to 'black box' deep learning-based
  approaches such as Eye2Gene."* And it reports performing worse on Asian
  and South Asian patients.
- **Cancer imaging FM**: *"our initial biological association analysis, aimed
  at explaining the model's decisions, is preliminary and requires more
  rigorous investigation."*
- **MIDAS** reports that drugs against its own top hit **failed phase II
  trials**, and separately admits an experiment it did not run:
  *"executing a GNN-specific interpretability routine would require
  benchmarking several models, which is computationally prohibitive for our
  main objectives."*
- **MIDAS again**, on the field at large: *"no algorithm achieves
  superiority across all evaluation dimensions, invariably necessitating
  trade-offs."*

**Two techniques make the honesty safe, and both are learnable.**

**Containment.** The admissions sit in the signposted block, after the case
is made. Not one of the eight concedes inside a paragraph that is winning.
**That is exactly AW's "do not claw" rule, correctly stated**: the rule is
not never concede, it is never concede in the paragraph that just won.

**Pairing.** A limitation arrives with its mitigation or its bound in the
same breath.

> "This introduces noise as undiscovered immunotherapy targets are
> mislabelled. **Yet**, using undersampling of negatively labelled nodes,
> repeated CV and fold-model bagging ensured that MIDAS aligned with robust
> ensemble-based positive-unlabelled learning methods."

> "Of course, Eye2Gene predictions will not replace the need for genetic
> testing or counselling… **Therefore, currently, the main anticipated
> application of Eye2Gene is in** facilitating more efficient cost-effective
> genetic diagnosis."

Concede the scope, then immediately state the application that survives.

---

## 7. How standalone it has to be

**It does not have to be standalone, and the set is split on how much it
leans.**

| paper | figure or table refs | Supplementary refs | citations |
|---|---:|---:|---:|
| IBDex | **0** | 0 | 3 |
| DLVPM | 0 | 0 | 12 |
| Cancer imaging FM | 0 | 0 | 24 |
| MIDAS | 0 | 1 | **35** |
| TIGON | 7 | **12** | 16 |
| PlantRNA-FM | 10 | 0 | 3 |
| Eye2Gene | 17 | **13** | 15 |
| **our draft** | **0** | **0** | **1** |

Two things to take from it.

**It must be readable without the figures, and four of the eight never
mention one.** IBDex's Discussion refers to no figure, no table and no
Supplementary item. So the Discussion carries no new evidence of its own,
and anything that needs a picture belongs in Results or Supplementary.

**But it is citation-dense, and ours is not.** Five of the eight cite twelve
or more references; MIDAS cites 35 in 995 words. **Our draft cites one.**
That is the second structural gap after the numbers: a published Discussion
spends most of its length situating the work against named prior work, and
ours spends it re-reporting our own measurements.

**TIGON shows the use of Supplementary that the supervisor's "fill it to the
brim" instruction enables:** twelve pointers in 744 words, every one
carrying a requirement or a robustness check out of the prose.

---

# What this changes about `DISCUSSION_INVENTORY.md`

**The 51 items stand. The three structural problems were wrong in two of
three.**

| | what I wrote | what the register says |
|---|---|---|
| budget | 1,900 candidates against 1,000, trim 250 | **target about 750**, so the draft loses a third while absorbing type J. Removing the 25 measured values is most of the cut |
| subheadings | unresolved, blocking, needs the supervisor | **settled by evidence.** Eight of eight have none, his own paper included. Topic-sentence ladders carry the sectioning |
| four items moved from Results | correct and unchanged | correct and unchanged |

**And three things the inventory did not know to ask for:**

1. **A mechanism paragraph for every comparative claim.** H1 cannot just
   assert that we beat scFoundation; it needs the reason, and H3 is that
   reason already written.
2. **Citations, roughly fifteen to thirty.** The claims axis supplies most of
   them for free, since every type J item names a paper.
3. **An estimand paragraph.** What cross-donor agreement *is*, against what
   a reader will assume it is. IBDex does this for PACP and we have no
   equivalent anywhere.

**One new asset found:** scGPT's own Discussion admits its pretraining does
not mitigate batch effects. Quote it in H1 or H3 and the foundation-model
comparison stops being our assertion and becomes their concession.
