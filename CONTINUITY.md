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
| **Results** | **flat. State what was done and what came out. No interpretation.** Springer Nature: *"simply state what you found, but do not interpret the results or discuss their implications."* |
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
- **Results `[2]` is deleted.** Merged into `[1]` on 2 November; its
  material lives in `[1]`'s note. Subsections are now `[1]`–`[5]`.

---

## Live, as of 2 November

**The unified benchmark run** is the blocker. Every baseline comparison in
the paper is currently invalid: runs used different gene policies, so the
same PCA scores 0.6906 in one and 0.6457 in another. One job fixes it.
First thing to check in its log: **416,256 cells**.

**The threshold sweep.** Cross-donor agreement depends on how donor-mixed a
cell's neighbourhood is — 0.8728 for cells with 1–10 cross-donor
neighbours, 0.4246 for 76–100. That gradient is larger than the gaps we
report. The plan is to sweep the threshold and report the curve, with
coverage beside every scalar. AW's framing, which is right: coverage is a
separate axis, like mean and variance, not something to fold into one
number.

**Results `[2]` is gone**, merged into `[1]`. Its six suspended figures and
the audit's verdict on each are in `[1]`'s note.

**The ablations and the whole-corpus geometry are writable now.** D1–D6 and
C1–C6 cross no method boundary, so the unified run does not touch them, and
`audit/NUMBERS.md` re-derives all of them from the files. AW's words:
*"the ablations are non-questionables… that means we could write the
ablation and model-understanding parts of the results. Good to keep in mind
as the immediate low hanging fruit."* That is subsections `[4]` and `[5]`.

**Open question nobody has answered:** where E3 goes — the scIB batch
metrics being degenerate on this corpus.

---

## Two things about tone

**Argue.** His instruction: *"You hold a vast set of information from code,
commits, docs, results. It is your job to be true to the code and the work.
Your argument doesn't take away from my ability to edit. You should argue,
I can rebut, we can discuss and conclude."* Folding immediately is the
failure, not disagreement.

**This is a "get it to the reviewer's desk" draft**, not a
hold-on-for-dear-life Nature submission. Scale criticality accordingly. He
has said this twice.
