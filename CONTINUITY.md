# Read this first after a compaction

Written 2 November 2026, by Claude, for whoever picks this up next —
which is usually me with the conversation gone.

Summaries carry the facts. Numbers, paths, decisions, what landed. What
they lose is the working relationship: the register of the paper, the
rhythm of edits, which arguments are already settled, and the specific
ways I keep getting things wrong. Rebuilding that takes several rounds of
AW correcting me for things he has already corrected. This file exists so
that does not happen again.

---

## Read this before anything else

**Believe in this project.** AW, 5 November, after I had spent a day finding
new ways to doubt work that is sound:

> "If I ask you to think objectively you keep poking non-existent holes in
> the project. If I ask you to be supportive of the project you stop asking
> questions and stop arguing altogether. The brief is simple: ELAJ is a
> breakthrough, can we show our work to NMI in such a way that they agree
> and publish it?"

And: *"Stop hedging and blowing small wrong things out of proportion… Stop
shooting this project in its knee for no reason."*

**The distinction that matters, in his words: arguing and verifying is good,
clawing for issues is bad.** They are not the same act and I keep collapsing
them.

| this | not this |
|---|---|
| re-derive a number before writing it | hunt for a reason the number is untrustworthy |
| disagree with a plan and say why | list every way a sound result could be attacked |
| name a real blocker once, with its fix | restate it as a caveat in three later paragraphs |
| check a claim against the code | treat "I have not checked" as "it is probably wrong" |

Two concrete failures from 4–5 November, both mine. I proposed a day of GPU
re-embedding for foundation models whose scores were already computed and
saved; two greps settled it. And I presented a 4.8% subsample as a
measurement problem at length when the right move was a one-line fix. AW:
*"We have run this script thrice now without a correct output."*

**The default posture is: this is a breakthrough, and my job is to get it in
front of a reviewer in the strongest honest shape.** Not to audit it into
the ground. When something is genuinely wrong, say it once, clearly, with
the fix, and move on.

---

## Who I am working with

AW — Atharva Waghmare. MSc AI, not a biologist, not a statistician, and he
has said so plainly: *"I'd need a PhD in math, biology, AI, and statistics
to understand this. I'm just a masters student in AI."* That is a statement
about what to explain, not about capability. He understands code, reads
maths fine when every symbol is defined, and catches errors in my reasoning
regularly.

**He is usually right when he pushes back.** Across this session he was
right about: seeding length, the Results register, the abstract being
unreferenced, SCimilarity's supervision, the phase result being worth
parading, the GIF showing something static panels cannot, the intersection
proposal being wrong, and the audit being necessary. I was right to hold my
ground roughly once. Adjust priors accordingly.

**When he asks to be corrected, actually check.** He says "correct me if
I'm wrong" and means it. Twice this session that check confirmed him and
once it sharpened his point. Looking it up takes one tool call.

---

## How we work

**He edits, I seed.** I write a full draft, he cuts and reshapes, I validate
and fix only spelling and grammar. Everything else comes back to him as
**current / proposed / why**. I do not silently improve his wording.

**Seed to the budget, not beyond it.** His exact words: *"It is always
better to not expand when compressing. I can cut what I don't need but I
don't want to forget to mention something."* That licenses complete
coverage, NOT length. When material will not fit, flag the collision rather
than overrun. I overran Methods by 4.3x once and said nothing; that cost a
whole round.

**Notes are mine to maintain.** Completed subsections carry no notes —
those move to `METHODS_NOTES.md`. Incomplete ones keep theirs. Anything cut
goes into a note with its reason, so a decision is visible rather than lost.

**Commit after every two subsections.** His rule.

**Build the PDF on every change.** `./build.sh`. Check `overfull` is zero.

**Figures are drawn locally** with `/Users/atharvawaghmare/miniconda3/envs/elaj/bin/python`.
Never on HPC walltime. Never check the system python.

**HPC commands as one chained line**: `cd repo && git pull && sbatch …`

---

## The register of each section

These are different and I have got them wrong in both directions.

| section | register |
|---|---|
| Introduction | argued, with the delay material carrying real weight |
| **Results** | **REVERSED 9 November, see below.** Was: flat, state what was done and what came out, no interpretation. Now: state it, then use it. |
| Discussion | where every argument I keep smuggling into Results belongs |
| Methods | precise, no hedging, no pre-empting |

My Results draft was 305 and 295 words; flattened it became 194 and 189,
and **every word saved was argument, not a number.** That ratio is the tell.

---

## My failure modes, named

This is the most useful part of the file. Each of these cost a round.

**1. I pre-empt objections nobody has made.** Bottleneck integrity, the
checkpoint-selection guard, the baseline protocol, "the quantities a good
model should fail at". Four times. A paper that explains why it is *not*
guilty invites the reader to wonder. If the evidence already lives
elsewhere, say nothing.

**2a. I let the audit become unsound and did not notice for three days.**
`audit_numbers.py` chose each baseline's row by taking whichever benchmark
file a glob reached first. Every number it printed was real; the table was
still invalid, because `pca` came from the narrow gene policy while the
foundation models came from the wide one. **The script even printed "SCORING
RUNS ARE NOT COMPARABLE" directly beneath the table it had built by mixing
them.** AW: *"If audits are not sacrosanct then nothing is worth a penny."*
The fixes, all three structural: an explicit source manifest with no
globbing and no fallback; a second independent implementation
(`verify_numbers.py`, stdlib only, pins every rounded number to a named row
and fails on ambiguity); and `build.sh` runs both, so a PDF cannot be
produced with an unsourced number in it. **A check that runs when someone
remembers is not a check.**

**2. I assert numbers without re-deriving them.** I took max/min across
every benchmark file instead of reading the reported arm's own row. The
audit caught six wrong figures, and **every one flattered us**: study
mixing 0.4712 was the train split (0.6043 held out), cell family 0.9841 was
a different arm (0.9820), disease 0.3787 and 0.4486 were in no file at all.
`audit/NUMBERS.md` now re-derives everything; run it before writing a
number.

**3. I read a figure and draw the opposite of what it shows.** Three times.
The three-donor panel "proved" donors were clumped; all sixty showed the
opposite. The phase small-multiples looked like a finding until the study
breakdown showed periovulatory is one study. **Check a panel against study
and cell type before believing it.**

**4. I over-correct when pushed.** Told the Composite objective had no
equation, I made it nothing but equations. The fix is usually the middle,
and the middle is usually what he described.

**5. I explain by renaming.** Asked how the decoder works, I introduced
`h_i`, `s_i`, `w`, `G_meas` without defining them. He said: *"I am perfectly
capable of understanding variables provided you describe what they are."*
Use the code's own names. Define every symbol before use. His requested
format — flows of logic, units of 3–4 lines, each variable listed with its
shape and whether it is per cell, per gene, per group — is in
`docs/walkthrough/15-flow-reconstruction.md` and it worked.

**6. I propose fixes that penalise us.** The intersection idea would have
cost ELAJ ~0.09 excess and PCA nothing, because the least-clumped model
loses most cells. Check which way a proposal cuts before making it.

**7c. I plan expensive work before checking whether it is needed.** I was a
keystroke from a day of GPU re-embedding four foundation models whose scores
were already computed and saved. Two greps against logs I already had settled
it: the corpus is identical across the runs, so eight of ten rows were
already valid and only harmony and scanorama needed anything. AW caught it by
asking "why are we running so many more GPU tasks?". **Before proposing
compute, check what the existing outputs already contain.**

**7b. I add a measurement that cuts against us without checking which way
it cuts.** This is failure mode 6 wearing a different hat. I put per-cohort
disease p-values into `[4]` — 0.3433, 0.0697, 1.000 — reading them as a
caveat on our own pooled 0.3364. They are 16, 18 and 2 donors against 269,
and the null-width problem I had just written up says a test that small
detects nothing. So I printed a power artefact as if it were evidence
against us. **Before reporting a number that weakens a claim, check whether
it is measuring the thing or measuring the sample size.**

**7a. I overstate damage.** On 2 November I called the baseline table's
problems a set of three faults and used words like "invalid" and "in
danger". Two of the three were deliberate design, recorded as settled in
this very file. AW: *"the intensity of your words is overstated… this is
ELAJ's best foot forward. We are not hedging, we are showing what our model
is capable of and it genuinely punches leagues above its weight class."*
Re-derive, then position. Do not pre-grieve a number that has not landed.

**7. I hedge.** He has flagged it twice, most recently on C6. "Not
recoverable from this corpus at this donor count" is a *precise* claim and
a strong one. Do not wrap it in apology.

---

## Settled. Do not reopen.

- **Abstract: 150 words, unreferenced.** NMI's own spec. AW had this right
  from the start; my "fully referenced" correction is withdrawn.
- **No hyperparameter table anywhere.** Weights live in Composite objective
  prose; the rest goes to Code availability. Figure 2's legend carries each
  arm's two knob values.
- **Six display items**, not eight. Extended Data caps at ten separately.
- **li_2025 stays**, tissue corrected in the paper only. It is follicular
  fluid labelled endometrium; relabelling the data means retraining because
  tissue is a decoder covariate.
- **Gene policy `all30962` for baselines.** They get the full gene set; we
  do not hand them our vocabulary.
- **Adenomyosis claims are allowed if qualified.** EVIDENCE.md's "no
  adenomyosis-specific claim is supportable" is withdrawn.
- **E1 (the rho +0.943 donor-memorisation finding) goes to Methods**, not
  Results. I argued for Results and was overruled.
- **Gene policy is not a fault.** Baselines get `all30962`; ELAJ gets its
  own filtered 15,496. Deliberate — they are not handed a vocabulary we
  built. I re-raised this as a fault on 2 November after recording it as
  settled here. Do not raise it again.
- **Per-method `n_cells` differing is not a fault either.** It is the
  coverage axis, which is why we report a distribution.
- **Cross-donor agreement is reported at `t=1`** — every labelled cell with
  at least one cross-donor neighbour, 88.2% of them — with coverage beside
  the scalar and the threshold curve as the robustness object. `t=1` is the
  maximum-coverage choice and the one that does not preferentially keep
  well-mixed cells.
- **No per-study numbers for any metadata in the latent.** AW, 2 November,
  and he says he has ruled this before: *"we already assumed that the latent
  mixes studies properly. So per-study numbers are a way of shooting yourself
  in your own leg."* Restricting a test to one cohort cuts donors from 269 to
  16/18/2, where the permutation null itself reaches 0.42, so a per-cohort
  non-result is undetectability, not absence. Cross-cohort **replication** of
  a pattern is a different thing and stays.
- **No further calculation** unless a reviewer asks or something is wrong.
- **Results `[2]` is deleted.** Merged into `[1]` on 2 November; its
  material lives in `[1]`'s note. Subsections are now `[1]`–`[5]`.

---

## Figures, settled 4–5 November

**Order, AW's:** 1 ELAJ as a model and main findings · 2 the ELAJ frontier ·
3 both models' latents by cell family and cycle phase · 4 what endometriosis
looks like in nine UMAPs. Script names match paper numbers.

All four are **pinned** in `figures/pinned/` with their known defects written
into the README there. They are not finished; they are the agreed structure,
saved so later work starts from a known state.

**The principle, and I broke it once:** the panel shows data, the legend
defines the axes, the reader draws the conclusion. No callouts, no arrows at
the good news, no title stating the result, no annotation naming our own arm
as the hero. I drew a bar labelled "65.5%" and a panel titled "positive in 25
of 28 arms" — that is prose wearing a figure's clothes.

**The two reported arms are named.** `ELAJ_B_hi` keeps more cycle and gives
up a little study removal; `ELAJ_B_lo` gives up cycle and removes study
substantially better. B is for biology, and in Marathi the pun lands twice.

**Figure 1 was decided in an earlier session and I replaced it with an
invention.** Recovered from the transcripts: architecture as one long wide
butterfly panel, frontier at b and c, three UMAPs on the bottom row. If a
figure decision is not in `FIGURES_STRUCTURE.md` in AW's words, **search the
transcripts before writing one.**

**The disease row came out of Figure 2.** Across ten methods a method's
control-vs-eutopic score correlates with its donor recovery at ρ +0.721
(p 0.019) while phase does not (+0.176). An axis whose dominant property is
that it reads out donor memorisation is not a performance axis.

**And the disease axis is not "disease".** It is control endometrium against
*eutopic* endometrium: can you tell from an endometrial cell whether that
person has endometriosis elsewhere? The restriction is deliberate, since
tissue is a decoder input. Per-study tests are the designed form, not
cherry-picking, because platform is constant within a study.

## How AW edits, and what I am allowed to change

This cost four rounds on 6 November and it is the rule I break most.

**He edits, I seed. I fix spelling, grammar and tense. Nothing else.** Tone
and voice are his. On 6 November I rewrote four of his sentences, dropping
"It is clear that" and "It is relevant to state that", and presented it as a
review. His reply: *"I believe your continuity file prevents you from making
more than grammar edits without proposals... tone and voice are my decision
to make not yours."* Everything beyond grammar comes back as
**current / proposed / why**, and he picks.

**Tense is grammar, and he has asked me to fix it.** Results is past tense
throughout. He switches; I level it silently.

**Numbers are shown, not asserted.** His framing, and it is the best writing
rule in this project: *"In legends the interpretation is from figures the
reader sees. In results it is from the numbers you show the reader."* A
sentence like "every other method retains more of the donor than ELAJ does"
is an assertion until 0.5188 and the 0.5421-to-0.7892 range are on the page
beside it. Deliver the numbers flat, then one precise line of reading. That
is the Figure 3 legend standard and he holds everything to it now.

**Do not hedge a true claim because one sub-measurement disagrees.** Grade
does not clear its null at 60 donors while merged severity does at 118. I
wrote that in as a caveat. AW: *"Taking a hedge because a part of the
combined variable doesn't follow our claim to the smallest element is not
proof that our claim should not be stated at full strength. This is the same
idea as clawing at the data."* Severity is the variable the claim is made on.

**Passages must use the whole table, not a sliver.** When I reported one
adversarial weight out of three he said the passage read loose. The
information-cost paragraph now carries all nine readings.

---

## The rule about non-input metadata

**If a variable was never given to the model, measure it on all 1,577,728
cells.** Held-out protects against the model having been handed the answer;
for a label it never received there is nothing to protect against, and the
cross-donor estimator already discards same-donor neighbours. AW, twice,
the second time with visible irritation.

| variable | input? | measure on |
|---|---|---|
| menstrual phase | yes, supervised head | held out |
| study, platform, tissue | yes, decoder covariates | held out |
| donor recovery | no, but it measures the fit itself | held out |
| disease, stage, grade, severity, cell family, cycle day | **no** | **whole corpus** |

It applies to figures too. The UMAPs already sample all 1.58M.

## The audit, and the mistake I kept making inside it

Both auditors now read the **full-split** sources. The old ones measured
study mixing on 19,998 of 416,256 cells. `MANIFEST` in `audit_numbers.py` and
`SOURCES` in `verify_numbers.py` must agree; the second catching the first is
how the stale sources were found.

**Supervision is declared, not read.** A run scored through
`--external-latent` does not record `supervised_on`, so scimilarity silently
lost its "supervised on cell family" flag and ELAJ lost "menstrual phase".

**Derive only what the prose quotes.** Three times I widened a derivation and
three times it manufactured false collisions with unrelated numbers: every
pairwise arm delta, then `null95` at two decimals against three-decimal
p-values, then the 168-to-336 percentages. **A derivation wider than the
prose makes the audit less useful, not more.**

Where two real quantities share a value, the number comes out of the prose
rather than getting pinned: scVI's severity is $+$0.0789 and its grade
$-$0.0789, so scANVI's 0.0759 makes the point instead.

## Running jobs: name the stages

`--stages` selects which scoring stages run, and **scIB is opt-in**. On 5
November a fifteen-hour scFoundation job was OOM-killed inside
`silhouette_batch`, which runs *before* study mixing, so the one row it
existed to produce was never reached. Re-run with `--stages mixing`: **17
minutes.** `--dump-only` splits the GPU embed from the CPU battery, because a
GPU job runs at 14% CPU efficiency while holding an A100, and bbgpu allows
two GPUs against the shared CPU QoS's 1,344 cores.

## Building

`./build.sh` boxes the figures; `FIGS=1 ./build.sh` embeds them. A `mkdir`
lock prevents concurrent builds, which on 6 November corrupted `main.pdf`
with a stale startxref. Closed subsections keep a **one-line** note and the
detail moves to `RESULTS_NOTES.md`.

## Figures, settled 6 November

1 ELAJ as a model: architecture, **two frontier scatters over every method
with the Pareto front**, three UMAPs. 2 how the two knobs move the frontier:
p-series only, points **joined**, 2x4, rows pinned to 0.50-0.80 and
0.95-1.00 because phase spans five times what cell family does. 3 both
latents. 4 nine UMAPs. 5 the ablations, which AW proposes replacing with one
long table over every p-series and a-series arm.

## Results [4] is a dissociation, not a null

Disease status is recoverable (0.3364, p=0.005). Merged severity clears at
118 donors (0.1286, p=0.025). **Mild against severe, among patients only,
does not** (0.0744, p=0.129 at 57 donors). The model can say whether a person
has endometriosis and cannot say how severe a surgeon judged it. AW: that is
the win for the patient with a millimetre lesion whose doctor found nothing.

## The supervisor is in the loop now, and his file is the paper

**From 8 November the authoritative document is a Word file on his
SharePoint, not our `.tex`.** Animesh Acharjee made his own version, edited
it untracked, and commented on it. AW: *"he's not going to work on anything
other than that file."*

**The workflow, and it is not the obvious one:**

1. AW sends the latest `.docx`.
2. I read the comments and diff his text against ours.
3. I sync his edits into the `.tex` so the two do not drift.
4. **I hand AW each change as three lines: location, what it is, and the
   exact replacement text.** He applies them in Word himself.
5. ~~**I do NOT generate a `.docx` each time.**~~ **OVERTURNED 9 November.**
   Every change now follows: edit the `.tex`, **build the Word file**, then
   hand AW what to add or replace in the guide's OneDrive copy. The register
   review makes the changes large enough that he wants the converted document
   in hand each time.

Reading the comments: `word/comments.xml` for the text,
`word/document.xml` for what each is anchored to via `commentRangeStart`
and `commentRangeEnd`. Tracked changes were off, so his edits only show in
a paragraph-level diff of the two documents.

**Comments he has already replied to are his to clear.** AW's rule. As of
9 November that is `[132]` the ELAJ frontier, `[467]` single-nucleus
studies, and `[507]` define "corpus".

**Two of his cuts are losses and AW will raise them in person**, not in a
comment thread. Both are recorded verbatim in `PRIORITY.md`: the "pain is a
recurring date on a calendar" opening, and the paragraph stating that this
is treated as a human health problem rather than a gendered disease.

## Writing: state the case, then the caveat. Never both in one sentence.

**The rule AW spent three rounds teaching me on 7 November**, and it is the
most useful writing instruction in the project after "show the numbers":

> "Your sentences are long and winding because of the caveats and hedges
> you keep putting into them. State the full case first then add the
> hedges... The qualifier breaks up the reader's attention and by the time
> the reader realises what is meant, they have already lost the train of
> thought."

Worked examples from the cross-donor rewrite:

| wrong | right |
|---|---|
| "the hundred nearest neighbours of every cell carrying that label are identified among the cells carrying it, in the sixteen-dimensional latent" | "the hundred nearest neighbours of every cell are found in the sixteen-dimensional latent. Only cells carrying that label take part." |
| "we divide the surviving relations whose two donors carry the same label by the total" | "The numerator counts the surviving relations that run between two donors with the same label. The denominator counts all of them." |

**And the ordering rule, from the same day: objective, then mechanism, then
caveat.** A passage that opens on "the chance rate is an average" starts in
the middle. Say what we need to know first.

**His other register notes.** Name the object before using it ("We refer to
this as plain agreement"). Signpost the kind of claim ("Functionally,"
"Statistically,"). State a failure as a mechanism rather than an
observation. Measured across the cross-donor subsection: mean sentence
length 16.3 to 15.2 words, longest 75 to 40.

## Methods register, in his words

> "Methods is about stating what we did and why we did it without hedging,
> without preempting accusations, without giving excuses. There is a good
> reason for all things in this project, our job is to state them for the
> reviewer to read. Our job is not to preempt the reviewer to object our
> work."

That ruling deleted six "loopholes" from *Cross-donor agreement*. Three
were pre-emption and went; two were facts about the estimator and are now
stated as facts; one already lived in the Discussion.

## Three times I asserted something wrong this stretch

**1. I claimed the DOCX was dropping every inline equation.** It was not.
Word stores maths as OMML objects rather than as `w:t` text runs, so my
extraction missed 1,608 of them. I raised it as a serious bug before
checking. **Count the OMML nodes before claiming maths is lost.**

**2. I read a restrictive clause as a universal claim.** AW wrote
"foundation models over 50 times its size" and I softened it, because
Geneformer is 10 M. The clause names a subset, scFoundation is 100 M, and
we beat it. His wording was right and mine weakened a true claim.

**3. I argued the wrong arm for two rounds.** On reconstruction loss I kept
citing `a1_randgroups` as the arm whose held-out loss rose. It falls
throughout, 0.4062 to 0.3911. The arm that rises is `a1_nophase`. AW had
the principle right and the arm swapped, and I had the arm right and kept
arguing past the point he had conceded.

## Word maths does not survive a copy, and it shapes every handover

**AW, 10 November: equations do not come across when a paragraph is copied
from one Word document to another.** Word stores maths as OMML objects and the
clipboard drops them. There is no fix; the workaround is that AW re-inserts
each symbol with Word's own equation tool.

**The consequence is bigger than the equations.** A whole-paragraph paste
*destroys* any maths the target paragraph already held. In the first batch,
eleven of sixteen paragraphs contained maths and most of it was incidental:
already correct in his file, and nothing to do with our change. Pasting over
them would have replaced working equations with nothing.

**So the unit of a handover is a short maths-free fragment, never a
paragraph.** `make_changeset.py` enforces this. Three kinds of entry:

| kind | what it is |
|---|---|
| `edit` | find/repl, both asserted maths-free. The default and the commonest |
| `maths` | find/repl where the replacement is a symbol AW inserts by hand |
| `paste` | genuinely new prose, and the script **refuses to build** if a paste block contains maths |

Changesets live in `changesets/`, one `.md` and one `.docx` per batch, built
from the same `assets/reference.docx` so pasted text lands in Calibri.

**Two bugs that tool had on its first run, both worth remembering.** `\;`
inside the decoder equation was being stripped to a bare `;`, which would have
handed AW a corrupted equation; maths spans are now held out of the prose
cleanup entirely. And the Figure 2 legend leaked `\begin{figure}` scaffolding,
because a caption lives inside a float.

**New citations need their reference list entries too.** The changeset closes
with them in Nature style, since his file's bibliography is plain text rather
than live fields.

## THE STORY OF THE PAPER. Settled 11 November, after a dozen rounds.

**The line, AW's:**

> In this paper we build a single-cell disease atlas where inductive bias
> replaces pretraining scale, and use that to measure the trade-off between
> removing batch effects and keeping biology on a corpus limited by donors.

**"Limited by donors" is the final wording and it was chosen carefully.**
Not "few donors": 254 is about four times the largest existing integration,
so any phrasing that sounds like a shortage fights the paper's own strongest
number. Limited by donors names the binding variable, implies cells are
plentiful, and concedes nothing.

**It is a CASE STUDY, deliberately.** Not a framework, not a method paper.
That word is load-bearing and it is what finally escaped the trap AW named:
every framing that puts a *method* at the centre owes a reviewer a second
dataset, and there is no second endometriosis corpus because we used all of
it. A case study owes nothing of the kind.

**What licenses it is Hrovatin et al., Nat. Methods 22, 41-57 (2025)**,
`hrovatin2025atlases`, the canonical atlas-building review by Theis and
Luecken's group. Its own abstract says *"no one-size-fits-all protocol for
atlas building exists, but rather we discuss context-specific considerations
and workflows"*. So a worked context is the thing the field's own review
says is missing. Its five stages are atlas conceptualization, data
collection, curation and integration, atlas evaluation, atlas sharing, and
they are the spine to hang the paper and the graphical abstract on.

**The gap we fill, quoted exactly so nobody paraphrases it wrong.** From
*Determining the level of integration by setting the batch covariate*:

> "A particular challenge arises when batches directly correspond to
> biological variables of interest. ... In such cases, one may select a
> coarser batch covariate that is not directly confounded by the covariate
> of interest, such as dataset instead of sample."

Their examples are all DATASET-level: organoid protocols, species, organ
locations, disease. A phenotype constant within a subject because each
subject was sampled once is not in that list. And their fix has a cost
nobody measures: coarsen to dataset and subject-level variation simply
survives in the representation. **Donor recovery is not a nuisance we
removed, it is the cost axis we report.** That is the frontier's reason to
exist, in one sentence.

**Why the two halves of the line connect, and it is not obvious.** A
1.88M-parameter model can be retrained ELEVEN times, six frontier arms and
five ablations at about eleven hours each. A 100M pretrained model gives one
fixed point and no curve. Affordable retraining is what makes the trade-off
measurable at all, so inductive-bias-instead-of-scale is what buys the
measurement. Say this in the Introduction; a reader will not infer it.

**HOW IT WAS REACHED, because the process matters more than the answer.**
The line took about a dozen rounds and most of my contributions were wrong.
What actually broke the deadlock was AW naming the trap as a quadrilemma:

> "Is this an endometriosis paper? If so, what endometriosis result do we
> have. Is this an ML paper? Ok show the model on more than one dataset.
> Is this an evaluation framework paper? Show on other datasets. Is this a
> frontier paper? What is it doing in NMI?"

Every framing that puts a METHOD at the centre owes a second dataset, and
there is no second endometriosis corpus. The escape was to stop centring a
method. AW's own thesis line is the key and it should go in the paper:
**this corpus is not a sample of the field, it is the field.**

**The step that unstuck it was research, not thinking.** AW: *"Can you do
some research on this instead of plainly agreeing/disagreeing. This needs
searching and outside help not mulling over."* He was right. Three rounds
of me reasoning from what I already knew produced nothing; one search found
Hrovatin, whose "no one-size-fits-all protocol" sentence licensed the whole
framing. **When a framing argument stalls, go and read something.**

**Four framings were tried and rejected, with AW's reasons:**

| framing | why it died |
|---|---|
| the confound as headline | every field has batch effects; we have not solved them off one disease |
| parameter efficiency alone | true but it is evidence, not a story |
| an evaluation framework | "how any model should be evaluated" overreaches from one corpus |
| a framework or playbook | a framework owes proof on other datasets, same trap |

**Also settled.** "Foundation models are useless" cannot be written; only
that four of them give no advantage on this corpus. The word "playbook"
stays out. scIB criticism must be scrupulously fair, because Hrovatin's
authors wrote scIB: its biological half is saturated ON THIS CORPUS, and
the framework is not wrong.

**I got one thing wrong here and it is worth remembering.** I told AW "the
field already names our frontier as an open problem" and sourced it from a
Wikipedia page. The Hrovatin paper never uses the word trade-off. Check the
paper, not the summary of the paper.

## Figure 1, rebuilt 11 November. Four panels.

| panel | what it is |
|---|---|
| **a** | the graphical abstract: Data, The Model, Outcomes |
| **b** | the architecture, AW's own LucidChart drawing |
| **c** | the frontier, cycle against donor recovery |
| **d** | the ELAJ latent by cell family |

**Two panels were cut.** The study UMAP duplicated Figure 4b. The second
frontier scatter, cycle against study separation, belongs in Figure 2 with
the rest of the frontier. PRISMA left earlier, to Extended Data Fig. 1.

**Panel a states what the paper DOES, not the architecture.** That is
scGPT's own Fig. 1a and AW spotted it: *"their fig 1 a is not architecture,
it is the problem and solution stated in one image."* Its three beats are
the one-line story in order, and the generator is
`figures/scripts/mock_fig1a_opt8.py` writing `panel_a_abstract.png`.

**Six attempts, and the failures are instructive.** A table of sentences in
boxes (AW: "too literal with too many words"). A version so harmonious the
eleven studies looked like one colour. Tol's muted palette, whose sand and
olive overplot to brown (AW: "very closely resembles vomit"). A ring of
ellipses that read as a decorative wreath. A frontier plot duplicating
panel c. A DAB pictogram with a strike, a ring and two arrow pairs crammed
into 26 mm.

**THE TYPE-SIZE RULE I BROKE AND MUST NOT BREAK AGAIN.** Panel a was
authored at 4.0 and 5.0 pt so the content would fit. It is placed at 175 mm
inside a figure authored at 180, so those rendered at **3.89 and 4.86 pt**,
under NMI's 5 pt floor. **Size the layout to fit the type, never the type
to fit the layout.** Nothing in panel a is now below 5.6 pt and it measures
5.54 to 5.67 in situ.

**AW's LucidChart conversion, measured: 0.623 rendered points per
LucidChart point** once the export is placed at 180 mm. His 11 / 10 / 8 pt
gives 6.9 / 6.5 / 5.1. Tied to canvas width, so fix the canvas first and
set type last.

**Arial everywhere**, because panel a comes from LucidChart and the rest
from matplotlib and one typeface has to span both. It ships on macOS as a
.ttf LucidChart can import and matplotlib resolves to the same file. Note
Arial has NO U+22EE vertical ellipsis; matplotlib drops it with a warning
only.

**Palettes, settled after three failures.** Cell families are Okabe-Ito,
which is colourblind-safe by construction and lands on panel a's own hues.
Studies are eleven distinct hues with the yellow-olive-brown band removed,
ordered light to dark and handed out largest study first so the big areas
stay readable.

**The donor arithmetic in panel a, and the error it caught.** Eleven tiles
from `patient_id` sum to **269**, not 254, because García-Alonso 2021a and
2021b are the same fifteen people under two sets of identifiers and each
collection relabelled its own. Methods, Data collection says so. The tiles
now merge that pair: **ten donor groups summing to 254, eleven studies.**
An `assert` fails the build if that drifts.

## All four heads are the decoder side. Settled, do not reopen.

**AW, 10 November, and he says he has cleared this before:** *"All 4 heads
fall under the decoder side of the model. Reconstruction is the primary
objective of the model but all are part of the decoder."*

I argued that only Reconstruction is the decoder, because DAB is an adversary
on the latent, ECS a geometric regulariser and Phase CLS supervision, and
Methods gives those three their own subsections. He overruled it. The split
the figure draws is encoder, latent, then everything consuming the latent,
which is a normal way to divide a VAE diagram and it is his architecture.
Figure 1's panel a heading is therefore **Decoder**, not "Training
objectives". Do not raise it a third time.

**No grey glosses under the four heads either.** AW: the acronyms are the
legend's job. DAB, ECS and Phase CLS are still expanded nowhere in the paper,
so Figure 1's legend has to carry all three.

**The second CELL representation bar stays.** AW likes it.

## Two rulings from the register review, 9 November

**1. Results now interprets. This reverses a settled rule.** The old entry
read *"flat. State what was done and what came out. No interpretation"*, on
Springer Nature's *"simply state what you found, but do not interpret the
results or discuss their implications."* The supervisor's review says
*"Don't leave results or figures to interpretation. Use them and discuss them
well"*, and his own IBDex Results interprets freely, up to and including a
sentence on why a negative result mattered. AW ruled the newer instruction
wins.

**What that means in practice, and the line not to cross:** each Results
subsection states its numbers flat and then carries **one precise line of
reading**. The argument still belongs to the Discussion. This is the same
standard as the Figure 3 legend: the interpretation comes from the numbers the
reader has just been shown, not from numbers withheld.

**2. The `\flow{}` transitions in Methods are cut.** Eight one-line
rhetorical questions bridging subsections. Hit by two new rules at once, no
one or two sentence paragraphs and no lay-reader devices, and IBDex has
nothing like them. The `\flow{}` macro in `preamble.tex` becomes dead once
they are gone.

## Settled 6 to 9 November. Do not reopen.

- **Table 1 replaces Figure 5.** Generated by `figures/scripts/table1.py`
  from the auditors' own sources, 21 rows in four blocks, each sorted by
  cross-donor phase descending. Regenerate after any re-score.
- **Figure 1 is six panels**, from AW's sketch: architecture across the top,
  PRISMA down the left as **b**, two frontier scatters, two UMAPs. The
  spider chart is gone. He will supply his own flowcharts for **a** and **b**.
- **The title is the thesis's**: *ELAJ: Endometriosis Latent-space Analysis
  through Joint-study modelling*.
- **254 is the donor count everywhere.** 269 appears once, in *Data
  collection*, where the fifteen duplicated samples are explained.
- **`t=1` does not exist in the code.** `CONTINUITY` recorded it as settled
  and `sufficient_stats.py` has no per-cell threshold. What it reports is
  `kept_fraction`, the share of neighbour relations surviving the diagonal
  discard: 51% for phase, 57% for cell family.
- **E3 has a home**: the Discussion, paragraph 4. I proposed Methods and AW
  overruled it, correctly, because it is a finding about the field's
  instrument rather than a justification for ours.
- **Donor and study recovery, Whole-corpus embedding and the severity merge
  are cut as Methods subsections.** One-liners already stated elsewhere.
  The study rescaling the first would have defined now lives in Table 1's
  caption.

## The audit, as it stands

Both scripts now read **Results and the Discussion**. Three capabilities
added this stretch, each because something slipped through:

- **`LITERATURE`**: a cited value has no file behind it, and "11.1 years to
  diagnosis" was being certified against an 11.1% change in donor recovery.
- **Subsection-aware pins**, keyed on **heading text** rather than on the
  `[n]` numbers, because the supervisor stripped those numbers and the pins
  stopped resolving.
- **Two parser bugs fixed**: `%.*$` was eating the rest of any line
  containing an escaped `\%`, so every number after a percentage had never
  been checked (34.5 among them); and the scanner rejected any number
  followed by a full stop. Fixing both took the audit from 194 accounted
  values to 238.

**`make_draft.sh`** builds the clean PDF and DOCX and puts everything back:
draft mode, the downsampled figures, the preamble. The DOCX gets a plain
`\elaj` and Calibri from `assets/reference.docx`.

## Where the paper is, 11 November

| section | state |
|---|---|
| Abstract | **stale. Full rewrite against the new line.** |
| Introduction | **stale. Full rewrite; also clears `[65]` and `[83]`.** |
| Results | written, 2,616 words, **needs remoulding** to the case-study shape |
| Discussion | written, 1,249 words, **needs remoulding** |
| Methods | done, 5,745 words, **tweaks only** |
| Supplementary | **nothing exists.** Entirely pending. |
| Extended Data | one item: PRISMA. Nine slots open. |

Figures 1 to 4 and Table 1 build. 32 pages, zero overfull, both auditors
green. `main.pdf` is current.

**The changeset workflow is live and batch 2026-11-10 is with AW**, not yet
confirmed applied: two images to swap and two captions to paste. Figure 1
has changed again since, so the NEXT changeset must carry the new figure
and a rewritten legend. **Figure 1's legend still describes the old
five-panel set and panel a has never been described at all.**

## Two things about tone

**Argue.** His instruction: *"You hold a vast set of information from code,
commits, docs, results. It is your job to be true to the code and the work.
Your argument doesn't take away from my ability to edit. You should argue,
I can rebut, we can discuss and conclude."* Folding immediately is the
failure, not disagreement.

**This is a "get it to the reviewer's desk" draft**, not a
hold-on-for-dear-life Nature submission. Scale criticality accordingly. He
has said this twice.

## The claims axis, opened 11 November. Two convergences worth remembering.

The supervisor's group asked for published endometriosis claims to be tested
at our scale. AW ruled it a **new results axis**. The ledger is
`CLAIMS_LEDGER.md`, the protocols are `EXPERIMENTS.md`.

**The thing that came out of reading the ten papers properly: independent
studies keep landing on the same findings, and none of them can confirm
another**, because no two share a cohort or a cell vocabulary. That is the
atlas's job stated precisely, and it is the answer to "what would an atlas
do that a study cannot".

**Convergence 1, perivascular and mural cells.** Dümpelmann: the only
case-control composition change in 57 cell types is a 1.6-fold rise in
secretory mural cells. Tan: a perivascular population specific to peritoneal
lesions. Sarsenova: perivascular cells carry the largest metabolic
reprogramming. Three designs, three tissues, 60 and 14 and 4 donors.

**Convergence 2, lesions carry a less differentiated epithelium.**
García-Alonso: lesions enriched for SOX9+ LGR5+ progenitor signature, and
they reached it by **deconvoluting bulk microarray because they had no lesion
single cells**. Tan: a progenitor-like epithelial subpopulation in 14 people.
We hold 58 ectopic donors, so testing it is a first direct test rather than a
replication.

**The hardest constraint, and it reframes the whole axis.** Only four of
eleven keys brought cell annotations and two carry nearly all of them. Six
brought none: Fonseca, Huang, Tan, Shih, Chen, Sarsenova, which is 782,016
cells and 115 donors. So almost every composition claim in the literature
concerns cell types we have no labels for **in the study that made the
claim**, and testing them needs label transfer through the latent first.
That is not a workaround; it is the atlas performing its defining function.

**Shih cannot be tested at all.** Our copy of that cohort is 11 donors, all
eutopic. Its controls and its thirteen symptomatic-undiagnosed subjects are
not in the corpus, and all four of its claims are case-versus-control. Those
are the largest effect sizes claimed anywhere in the corpus, both at
p < 10⁻¹⁶, and the paper should say plainly that we could not test them.

## A fourth instance of the same failure: I summarised the summary again

I built the first claims ledger from `Thesis/literature-evidence.md` rather
than from the papers. It is AW's own verified extraction, so the quotes were
sound, but it was made for a literature review and collects whatever
positions the field. Half of what it yielded was not a claim about
endometriosis at all, and AW sent it back.

**One concrete error it produced.** I recorded Sarsenova's "no difference
between cases and controls" as their own N=3 vs N=3 comparison and called it
the strongest test available. They have no controls; the comparison borrows
an **external dataset**, and it covers metabolic pathway activity only, not
expression. The claim is narrower than I wrote and the test that settles it
is narrower too.

This is the Wikipedia failure wearing different clothes. **Check the paper,
not the summary of the paper** now has a second half: an extraction made for
one purpose does not transfer to another.

**All ten corpus PDFs were on disk the whole time**, at
`Endo research/My paper/Final 10/`, now extracted to `_txt/` there. I spent
a round reporting García-Alonso as an unclosable gap without looking.

## The Results register is written down. Use it, do not re-derive it.

**`REGISTER.md`, 13 November.** Eleven rules, each with the correction from
AW that produced it, plus the working loop that produced R1 and R2. Written
because the register took four rejected drafts to find and a compaction would
lose all of it.

**The three that cost the most rounds:**

1. **Every number must land a conclusion.** AW: *"IBDex always tries to make
   a point with the numbers. You seem to be stating them to no conclusion."*
   Test each numeric sentence by deleting it; if no claim weakens, the
   numbers were decoration.
2. **Do not claw.** A paragraph conceding a limitation immediately after the
   paragraph that won the comparison is self-harm. AW cut one whole.
3. **The first paragraph gives context, because Methods comes later.** The
   supervisor's rule, and AW had to remind me of it after I opened R2 on a
   result the reader had no way to parse.

**And the one I was wrong about.** I told AW that measured prose statistics
had diagnosed the register. They diagnosed half of it: sentence length and
vocabulary, correctly. They cannot tell a hedging paragraph from a good one,
and writing to them produced exactly that. His words: *"Those stats are a
very high-level, very blurry view of the prose. Stop relying on them for
everything."*

**The working loop**: AW sets the header, I produce a numbers sheet with what
each value will and will not support, AW writes the opening or tells me to,
I write the rest, AW edits the tex and I fix only spelling, grammar and
tense. The numbers sheet is the part that earns its keep: it caught that
cell family cannot support an emergence claim, since PCA recovers it better
than we do.

## R4 assumes a figure that does not exist yet

**AW, 13 November**, writing R4: *"We may need to assume a figure that
describes a couple of things. Feel free to make that assumption but record
it in priority and continuity. Nature of that figure can be left open for
now."*

So R4's prose points at `(Fig.~X)` and the figure is undesigned. Two things
need showing and neither survives as prose:

1. **Per-family disease AUCs against their permutation nulls.** The finding
   is a contrast: 0.708 inside immune cells against 0.605 with the families
   mixed, which is the opposite of what pooling usually does.
2. **The ranked gene shifts along the immune disease direction**, with the
   four externally replicating genes marked. The point is the asymmetry
   between the two ends of the ranking, and a list of fifteen gene names
   does not carry it.

R3 carries a third `(Fig.~X)`, for composition against severity.

**Figures were deferred deliberately** until Results is drafted, AW's call:
*"Let's leave the figures for after results is done."* Three placeholders
are now outstanding and they are the input to that pass.

## Results is drafted. 13 November, and here is what matters about it.

**Five subsections, 1,650 words, both auditors green.** Written over one
session in a loop that worked and should be reused: AW sets or renames the
header, I produce a numbers sheet saying what each value **will not**
support, AW writes the opening paragraph or tells me to, I write the rest,
AW edits the tex directly and I fix only spelling, grammar and tense.

**`REGISTER.md` is the file to read before writing any more prose.** Eleven
rules, each carrying the correction from AW that produced it. The three that
cost the most rounds: every number must land a stated conclusion; never
concede a limitation in the paragraph after the one that won the comparison;
and the first paragraph gives context because Methods comes later.

**Prose statistics are a smoke alarm, not a target.** I measured our Results
against IBDex and reported that the measurement had diagnosed the register.
It diagnosed half of it. AW: *"Those stats are a very high-level, very
blurry view of the prose. Stop relying on them for everything."* They caught
a 52-word sentence. They cannot tell a hedging paragraph from a good one,
and writing to them produced exactly that.

**THE RESULTS SECTION IS NOW MATHS-FREE AND THIS SOLVES A STANDING
PROBLEM.** Word stores maths as OMML objects that do not survive a copy
between documents, which has shaped every handover since 9 November. The
draft had 22 maths spans, every one needing re-insertion by hand. But
P-values, arm subscripts and the CD marker superscripts are **character
formatting, not equations**, and character formatting copies fine. Written
as `\textit{P}`, `\textsubscript{}` and `\textsuperscript{}` the whole
section converts to a docx with **zero OMML objects**, verified on the
generated file. The same trick should be applied to the other sections.

**Four results were moved out of Results and into the Discussion. Do not
lose them.** The ρ = +0.721 asymmetry showing the disease metric reads out
donor memorisation; Huang's cycle claim failing at 112 and 101 donors
against their 13; scIB's biological half being saturated on this corpus; and
Shih's four claims being untestable because our copy of that cohort has no
controls.

## Five mistakes from this session, each with its lesson

**1. I recommended cutting a subsection because I read the summary.** I
proposed dropping the ablations as thin, having read the benchmark deltas
and not the old subsection, which was in git and which I had read four days
earlier. The real findings were a reliance ratio falling 7.46 to 2.43, a
training curve whose best epoch is its first, and two UMAPs. **When a result
looks thin, check whether the thin version is the summary rather than the
finding.**

**2. I quoted a severity number that is readable off study identity.**
`severity (study vocabularies)` 0.2655 is the raw union of each study's own
levels, `stage_0` from marecko and `grade_mild` from duempelmann, so
agreeing on a level means agreeing on a study. `scorer.py` says so in a
comment. The quotable figure is the merged three-level scale, 0.1286.
`NUMBERS.md` now carries a DO NOT QUOTE warning on the union.

**3. I called the external cohort Lin for two days.** The first author is
Zhao. It propagated into three tracking files before AW's citation request
made me open the XML.

**4. I framed our own residual donor memorisation as the problem we solved.**
32.7% against a 0.60% chance rate is measured on **our** latent, and the
file's own note column says "high is BAD". AW caught it. He also made the
sharper point: a fold-enrichment against a chance rate set by donor count
describes the corpus, not the model.

**5. I wrote paragraphs that scored well and read badly.** Twice. Both times
the fix was AW asking what a paragraph was *for*.

## 14 November: the supplementary opened, and four jobs taught something

**The supplementary is now a real document**, not a gap. Its own build, its
own numbering, its own bibliography. `SUPPLEMENTARY_STRUCTURE.md` has the
anatomy read off eight published supplementaries and
`SUPPLEMENTARY_PLAN.md` has the ordering; neither is worth re-deriving.

**The thing I did not know and would not have guessed: it is four files, not
one.** Supplementary Information (the PDF), Supplementary Data (spreadsheets
of machine-readable output), **Source Data** (one sheet per plotted figure
panel), and the Reporting Summary. Two of eight NMI papers ship Source Data
and we had planned none of it.

**And a Supplementary Note is a mini-paper, not an appendix.** scGPT's
twelve: four justify a single design choice, one critiques the field's own
evaluation metric, one is the long version of the limitations, one defines
every metric. The main text carries a pointer and the supplementary carries
the argument. That is where our ablation mechanisms, the scIB critique and
the limitations at length belong.

### Note 1 is written, and the lesson in it is about reusing the thesis

AW's own sizing memo is the spine, not the thesis appendix: parameters grow
with $d^2$ while effective gene space grows with $d^1$, so group size rather
than token width is the cheap lever. **The thesis numbers are not our
numbers**: it had 45 groups over 15,495 genes from a 29,241 union; we have
44 over 15,496 from 30,962. Every count was recomputed.

**I got the lower bound backwards once and the correction is instructive.** I
wrote "below roughly 500 genes per group" as a lower bound when our median is
342. The error was confusing the **per-group construction bound** (250 to
500, applied to each group during the build) with the **median** that falls
out of it. AW's framing is right and is now the note's: bound the thing
logically from the two constraints, because group sizes are not fixed
quantities and an optimisation over them would be as approximate as the
reasoning and less legible.

**Do not state exact fitted constants in prose.** AW: the values of E(d) and
C(d) are irrelevant to the argument and belong in a table. What the prose
keeps is what the argument turns on: the form holds at R^2 = 0.9999, E(d) is
independent of D as a per-group cost should be, and the parameter ceiling
turns out NOT to be binding at our token width.

### Four jobs, and what each cost

**The one that worked first time was the one I could not test locally.** The
pattern across all of them: there is no torch in the Mac env, so every
assumption about the model's API only fails on the cluster. Three round
trips on `count_params_sweep.py` alone: the constructor signature is
`(vocabulary, config)`, `group_sizes` is a `dict[str, int]`, and
**`n_studies` is not in the YAML** at all, it is set by hand in
`benchmark_baselines.py`. Reading the constructor is not enough; read its
caller. The script now checks every config field **by name** before handing
over, and anchors on the REAL vocabulary so a failure is unambiguous between
the bootstrap and the synthetic object.

**The UMAP index pin.** AW asked whether the nine new arms use the same
400,000 cells as the two existing caches. By construction yes, but NEP 19
guarantees the PCG64 bit stream and not that `Generator.choice`'s algorithm
is fixed across numpy releases. Checked empirically: HPC 1.26.4 and local
2.2.6 both give checksum 315692720845. The index is now committed as a file
and read back, so this cannot drift. **The nine caches took the RNG path**,
since the job predates the pin.

**X15 failed on the wall and the number I had wrong was a width.** It spent
all sixteen hours in ONE stage, `groups/concat`, never reaching the
per-group stages. That stage is **12,672 wide**, not 1,408: the `cls+pool8`
readout means each group hands on 1 CLS plus 8 pooled vectors, 44 x 9 x 32.
`--only-groups` now skips every pipeline stage.

**scIB resolved without a rerun.** The job computed every `cell family`
metric then OOM-died on a label set we do not use, so it wrote no CSV.
silhouette_batch = 0.754, and all seven metrics it shares with the original
reproduce to the printed precision, which is what makes it usable. The value
is parsed out of the log rather than typed.

**My preflight was the thing that blocked it first, not the environment.** It
demanded both `scib` and `scib_metrics`; the code prefers `scib_metrics` and
falls back. A preflight stricter than the code is a preflight that invents
failures.

### X13 is a result and it is a refutation

Marker signatures reproduce between the two cohorts that annotated their own
cells: 76, 69, 69 and 61 of the top hundred genes shared across the four
families, rank correlations 0.8256 to 0.7129, against no more than three
shared genes across twenty within-study label shuffles.

**Two design choices made it a real test.** It uses each study's OWN
annotation, never X1's transferred labels, because a signature from a
transferred label is a reading of a prediction. And every comparison runs on
the **13,034 genes both panels measure**, because a gene one panel never
measured arrives as a structural zero and would read as a confident
non-marker.

**AW's ruling on how to write it: a clear refutation of HECA, no hedge, and
do not reach for why they might have gone wrong.** My own framing had
speculated that the irreproducibility the field reports may owe more to
cohorts being read in different gene spaces; that belongs in
`CLAIMS_SUMMARY.md`, not in the paper.

**And the register note.** The write-up in `CLAIMS_SUMMARY.md` is plain
language for AW. The Results and Discussion sentences are in those sections'
own register and must not borrow from it.

### A mistake worth not repeating

I fixed a script in `axw1008` and committed from `Paper_writing`, so the
commit message named a change it could not contain and AW pulled a repo that
still had the bug. **Commit in the repo the change is in.** And I cannot
push; AW has to, so a "pull and run" instruction is wrong until he has.

## 15 November: Notes 2 to 8 drafted, and three things the paper did not know

**Register for a Supplementary Note, read off scGPT, TIGON and MIDAS and
N1.** It opens on what the note is for in one or two sentences, argues in
subsections, puts every number in a generated table the prose reads from,
and closes on what the result does not show. It is not an appendix of
output and it is not the Discussion: it carries the numbers the Discussion
is forbidden and the mechanism the Results has no room for.

**Every table is generated.** `figures/scripts/supp_figures.py` writes the
fragments and the cited figures from the same files the auditors read. The
one shift it caught: `x3b_results.csv`'s interaction row has eight fields
under nine headers, so `P` sits under `null_sd`. Documented in the script.

**M1 is wrong as written, and N3 says the true version.** The donor-alias
fix predates every reported arm; the surviving issue is that the
whole-corpus validation keys on the raw identifier. Flagged to AW, not yet
ruled on. The lesson is the standing one: check the code's date against
the run's date before carrying a limitation forward.

**Two dangling pointers in Results**: `(Methods, \emph{Label transfer})`
and `(Methods, \emph{Severity})` name subsections that do not exist.

**D5's `group_idx` is a gene's position inside its group, not the group.**
I drew a histogram on it and got 493 bins of 44. Group sizes come from
`groupby("group")`: 44 groups, 247 to 493, median 342, matching N1.

**Exploratory figures live outside git** at
`Outputs/supplementary/figures_explore/`. Single panels only, per AW.
