# How a Supplementary Note is actually written

Built 15 November 2026, before AW reviewed Notes 2 to 8, on his instruction
to compare them against published notes along three axes: **tone, coverage,
usefulness**. The method is the one `DISCUSSION_REGISTER.md` used: read the
published notes in full, quote sentences, and treat the counts as a smoke
alarm rather than a target. AW's warning governs: *"Prose statistics are a
very high level and very blurry interpretation of the paper's tone, voice,
and register."*

**The comparator set is smaller than it was for Discussions, and that is a
fact about the field.** Of the eight papers in the archive, five ship
figures and tables and no notes at all (Eye2Gene, DLVPM, PlantRNA-FM, the
cancer imaging model, IBDex). What exists:

| paper | notes | words | what the notes are |
|---|---:|---:|---|
| **scGPT** (Nat. Methods) | 12 | 237 to 1,165, median 488 | four design-choice justifications, two capability write-ups, a metric critique, a long limitations note, related work, metric definitions |
| **TIGON** (NMI) | 9 | 722 to 1,784 | method derivations with equations, a benchmark against named competitors, five sensitivity and ablation notes |
| **MIDAS** (NMI) | 1 | 138 | one paragraph of pathway interpretation |

All read in full. TIGON's Notes 6 to 8 are the nearest analogues to our
N4 and N5, since each is one design choice tested by removing or varying it.

**N1 is the control.** AW edited it, so wherever N2 to N8 differ from N1
the difference is mine and not the document's.

---

## 1. Tone

### What a published note sounds like

TIGON Note 6, the whole note, 158 words:

> "TIGON offers an optimal strategy that combines short- and long-term
> reconstruction errors to minimize integration errors across various
> temporal scales. **To examine the effects** of long-term reconstruction
> error, **we conducted** an ablation study using simulated data, excluding
> the long-term reconstruction error from the training process. **We then
> evaluated** TIGON's performance in predicting velocity, trajectory, and
> the ratio of transitioning to quiescent cell populations. **Although** the
> inferred trajectory and velocity appeared similar to the ground truth
> (Supplementary Figure 13a), the accuracy of these three metrics, as
> measured by MSEs, increased when the long-term reconstruction error was
> excluded (Supplementary Figure 13b). **This surge in MSEs ... indicates
> the importance of** incorporating long-term reconstruction errors in
> TIGON's training process."

scGPT Note 6, the binning choice:

> "**To verify the effectiveness** of binning, **we conducted** experiments
> with varying settings ... **In both settings, we tested** the number of
> bins in a large range from 3 to 2001, and found the proper settings of
> bins in the range of tens to a few hundred consistently lead to better
> performance. ... **Overall, the experiments empirically demonstrate** that
> the binning approach serves as an effective method for data
> preprocessing."

Five moves, in this order, every time: what the component is; *to examine
X, we did Y*; *we then measured Z*; *although A, B (Figure)*; *this
indicates / overall*. First person throughout. A connective at nearly every
joint. A plain summary sentence to close. No sentence is quotable on its
own.

### What ours sounds like

N5, the random-grouping paragraph, as written:

> "Every gene was reassigned to a random group, with group sizes, each
> gene's position, parameter count, attention cost and effective gene space
> held exactly as in the base. The arm trained for eighteen epochs, the
> longest in the project, selected epoch 12, and reached the best held-out
> reconstruction of any model including the base, 0.3911 against 0.4024.
> Its training and held-out curves descend together with the smallest and
> most stable gap in the wave; a reader shown that curve alone would call it
> the best-regularised model here. Every biological axis fell with it ...
> The decoder's reliance on the latent relative to the covariates fell from
> 7.46 to 2.43: with the pathway structure gone the decoder found a cheaper
> route to the counts through provenance, which is why it reconstructs
> better and encodes less. **That is the inductive-bias claim of the paper
> demonstrated rather than asserted**, and it is also why reconstruction
> loss is not a model-selection criterion for a representation."

The science is better than TIGON's note. The sound is wrong in five
specific ways, and each is measurable.

**(a) Nobody did anything.** Published notes say *we conducted, we
evaluated, we tested, we observed* at 1.4 to 1.5 per hundred words. N2 to
N8 use the first person **zero** times in 8,500 words. N1, as AW left it,
uses it at 0.13, and the main-text Methods uses it freely (*"Instead we
calculate cross-donor agreement"*). The impersonal passive throughout is
what makes the notes read like an audit report rather than authors
explaining what they did.

**(b) No connective tissue.** *Furthermore, Specifically, In addition,
Overall, Thus, However*: scGPT 0.62 per hundred words, TIGON 0.40, **N1
0.33** (AW's own additions: *"Thus, parameter count is the first variable
to optimise"*, *"Notably,"*, *"Consequently,"*, *"In essence,"*). **N2 to
N8: 0.00.** I avoided them as filler. The published notes use them as the
reader's handrail, and so does AW.

**(c) Semicolon chains.** Published notes: scGPT 0.06 per hundred words,
TIGON 0.00. Ours: **0.41 to 1.16**, thirteen times scGPT. A published
sentence ends; ours continues through a semicolon into a second clause that
qualifies the first. N4: *"The per-epoch readout is k = 30 on 19,972
validation cells and is not the benchmark's cross-donor agreement, which is
k = 100 on the full held-out split; it is a trajectory, not a value to
quote."*

**(d) Antithesis as a tic.** *X rather than Y*, *X, not Y*, *which is what
makes*, *and it is*: scGPT 0.06 per hundred words for *rather than*, TIGON
0.00. Ours **0.10 to 0.73**, with N5 and N8 above 0.6. Twenty-five
instances were pulled; a sample:

> "demonstrated rather than asserted" · "a necessity rather than a
> preference" · "undetectable at that donor count, not absent" · "deleted
> rather than deprioritised" · "the panels, not the biology" · "a reading of
> a prediction" · "sliding the model along a trade-off rather than improving
> it" · "computed rather than learned" · "a trajectory, not a value to
> quote" · "reported as unindexed rather than as new"

One of these per note is a point. Five per note is a voice, and it is the
voice AW has flagged before as sounding written by a model.

**(e) The aphoristic close.** scGPT ends seven of eight argued notes with
*"Overall, ..."*, *"In summary, ..."*, *"These results validated ..."* or a
future-work sentence. TIGON ends with *"This indicates ..."* or *"In
conclusion, ..."*. Ours end on the antithesis: N2 *"a necessity rather than
a preference"*, N5 *"deleted rather than deprioritised"*, N6 *"informative
about the deposits rather than the model"*, N8 *"with that half conceded"*.
Paragraphs do the same: *"It is not built."*, *"Nothing here reads disease
status."*, *"None of these is wrong."* The published register never lands a
paragraph on a six-word sentence.

**(f) Sentence openers.** A third of our sentences open with *The*, against
10% in scGPT and 14% in TIGON, where *In*, *For*, *To* and *We* carry a
third of the openings between them. N4 opens half its sentences with
*The/This/That*; N8 57%.

### What is right about the tone

No hedging (0.06 per hundred words; scGPT 0.53, and its hedges are all in
future-facing sentences). No praise words (0.21; scGPT 0.57 with
*notably, significant, robust, remarkable*; TIGON 0.03). Numbers at the
same density as the published notes (4.0 per hundred words against 3.3 and
4.4) and placed the same way, inside the sentence with the figure named.
Those three match and should not be touched.

---

## 2. Coverage

What a published note contains, as moves, against ours:

| move | scGPT | TIGON | N2 to N8 |
|---|---|---|---|
| context: what the component or question is | always, 1 to 2 sentences | always | always, 1 paragraph |
| procedure, first person, **before** the result | always | always | present, passive, and in N5 and N7 often **after** the result |
| result with the figure or table named | always | always | always |
| interpretation or mechanism | 1 to 3 sentences | 1 to 2 sentences | **1 to 2 paragraphs**, the longest element |
| summary sentence | 7 of 8 | 6 of 6 | **0 of 7** |
| what it does not show | only in the limitations note | rarely | **6 of 7** notes close on it |
| future work | 3 of 8 | 1 of 6 | 1 of 7 |
| pre-registered predictions | never | never | **N4, N5** |
| reasons for what was not done | never | never | **N5** (the not-ablated table) |

**Three things ours carry that the published notes do not, and all three
are strengths**: the mechanism at length, the registered predictions
against their outcomes, and the table of what was deliberately not ablated.
No published note shows a prediction that missed. Keep all three.

**Two things ours lack.** The summary sentence, which is the move the
reader uses to leave the note with something in hand; and procedure-first
order, which lets a reader know what was done before being told what came
of it. The closing move on limits is fine in N3, whose subject is limits,
and once in N8, whose claim is a refutation and should say its own bounds;
in N2, N4, N5 and N6 it should follow a summary, not replace it.

**Coverage the comparators have and we do not, outside N2 to N8.** scGPT's
Note 12 defines every metric in one place; TIGON's Note 2 does the same and
its Tables 2 and 3 carry every hyperparameter. We have neither a metric
definitions note nor a hyperparameter table. AW's own comment in
`PRIORITY.md` already asks for hyperparameters to move into Supplementary
Methods with a table; the metric definitions are the companion gap.

---

## 3. Usefulness

**What a reader can take away from ours that a published note rarely
gives**: the full eleven-by-ten scorecard rather than an aggregate; every
arm on every axis with its permutation P; both rejection rules with their
failure rates; a protocol per claim with the model formula written out
(N7's X3b); the null width beside every negative. A reviewer who wants to
check a number in the main text can find its row. That is the supervisor's
*"filled to the brim"* met in substance.

**What reduces it, and each is a wording fix:**

1. **Internal vocabulary.** *arm* (34 uses in N4 and N5), *the wave*, *the
   p-series*, *registered*, *declared*, *the auditors' manifest*,
   *provenance*. A reader has no wave and no auditors. TIGON says *"we
   conducted an ablation study"*, not *"the arm"*. N2's sentence *"One cell
   of the table has a different provenance and it is declared"* is a line
   from our tracking files, not from a paper.
2. **Experiment numbers as headings.** N7's subsections are *"X3: ..."*,
   *"X3b: ..."*, *"X8, extended: ..."*. The X numbers mean nothing outside
   `EXPERIMENTS.md`. scGPT and TIGON title a note by its question.
3. **Length per note.** Ours run 614 to 1,948 words, median 1,229, against
   scGPT's median of 488. TIGON's methodological notes reach 1,784, so
   length alone is not the fault; the antithesis density is what makes
   ours feel long. Cutting (c), (d) and (e) above will shorten every note
   by a tenth without removing a number.
4. **Standalone-ness is fine.** Both published sets point at main-text
   figures and Methods the way ours do, and ours resolve every cross
   reference inside the supplementary.

---

## 4. Per-note diagnosis

Counts per hundred words after stripping tables, captions and markup; N1
included as the control AW edited.

| note | words | semicolons | *rather than* | connectives | opens *The* | internal words | closes on |
|---|---:|---:|---:|---:|---:|---:|---|
| N1 (AW-edited) | 1,505 | 1.06 | 0.33 | **0.33** | 36% | 0 | the ablation that tests it |
| N2 scIB | 1,086 | 0.74 | 0.18 | 0.00 | 35% | 8 | antithesis |
| N3 limitations | 1,948 | 0.41 | 0.10 | 0.05 | 36% | 10 | a limit, which is its subject |
| N4 frontier | 1,016 | 0.89 | 0.20 | 0.00 | **50%** | 24 | a figure pointer |
| N5 ablations | 1,369 | 0.80 | **0.73** | 0.00 | 30% | **33** | antithesis |
| N6 transfer | 739 | 0.54 | 0.27 | 0.00 | 33% | 1 | antithesis |
| N7 claims | 1,731 | **1.16** | 0.58 | 0.00 | 46% | 1 + X-numbers | a caveat |
| N8 markers | 614 | 0.65 | 0.65 | 0.00 | **57%** | 0 | a concession |
| scGPT, 10 notes | 488 median | 0.06 | 0.06 | 0.62 | 10% | 0 | summary |
| TIGON, 6 notes | 946 median | 0.00 | 0.00 | 0.40 | 14% | 0 | summary |

**Read across N1 first.** AW's edited note carries semicolons and *rather
than* at the same density as mine, so those two are partly the document's
voice and he may keep them. What N1 has that N2 to N8 do not: connectives
(0.33 against 0.00) and the occasional *we*. Those two are the cheapest fix
and the one his own edit already made.

**Worst first:** N5 and N7 for antithesis and internal vocabulary; N4 and
N8 for the *The*-opener monotony; N2 for audit language.

---

## 5. Proposed fixes, for AW to accept or reshape

Nothing below has been applied. Ordered by how much of the sound it changes.

1. **First person for procedure.** *"We reassigned every gene to a random
   group"*, *"we scored every representation on all ten metrics"*,
   *"we computed the signature within each study"*. Matches scGPT, TIGON,
   the main Methods and N1. Leaves results and mechanism in the third
   person.
2. **Connectives at the joints**, at N1's density: *Specifically* before a
   detail, *In addition* before a second measurement, *Thus* before a
   consequence, *Overall* before the summary.
3. **A summary sentence closing every note** and every multi-paragraph
   subsection, in the published form: *"Overall, the five ablations ..."*,
   *"In summary, the two cohorts ..."*. The what-it-does-not-show paragraph
   stays in N3 and N8 and moves before the summary elsewhere.
4. **Split the semicolons.** Every semicolon becomes a full stop unless the
   two clauses are a list. Target under 0.3 per hundred words.
5. **One antithesis per note.** Keep the one that is the note's point
   (N5: fits best and holds least; N6: absorbed, not flagged). Rewrite the
   rest as plain statements: *"deleted rather than deprioritised"* becomes
   *"so it was not run"*.
6. **Replace internal words.** *arm* to *model* or *configuration*; *the
   wave* to *the five ablations*; *registered* to *specified before
   training*; delete *declared*, *provenance*, *auditors' manifest*; N7's
   headings become the questions (*"Does disease flatten the cycle in the
   latent?"*).
7. **Procedure before result** in N5's five arm paragraphs and N7's
   protocol paragraphs, TIGON's order: what we did, what we measured, what
   happened, what it indicates.
8. **Vary the openers.** Where a sentence opens *The X ...*, prefer the
   published frames: *To test ..., For each ..., In both ..., Across the
   eleven ..., At the shipped width ...*.

Applying 1 to 8 is a rewrite of surface, not of content: every number,
table, figure and argument stays. Expected effect on the counts: semicolons
and *rather than* to published levels, connectives to N1's, *The*-openers
from a third to a fifth, and each note roughly a tenth shorter.

---

## 6. What the counts cannot tell, so they are last

The counts found (a) to (f) because each is a construction that can be
grepped. They cannot tell whether a mechanism paragraph is too long for its
place, whether the registered-prediction tables read as confidence or as
confession, or whether N3's fourteen limitations at length land as
objective analysis, which was the brief, or as a catalogue. Those three are
reading judgements and they are AW's.
