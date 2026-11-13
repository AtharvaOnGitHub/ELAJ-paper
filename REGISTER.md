# The Results register, and how to reproduce it

Written 13 November 2026, after R1 and R2 were drafted, rejected, and
rewritten four times between them. **Everything here was learned by being
corrected, and each rule carries the correction that produced it.** The
reference is IBDex, the supervisor's own paper, extracted at
`Atharva Papers/_txt/IBDex.txt`, Results beginning at line 496.

**AW's warning, and read it before the measurements below:**

> "The stats about prose are less important than how it actually reads.
> Those stats are a very high-level, very blurry view of the prose. Stop
> relying on them for everything."

The numbers in section 9 are a smoke alarm, not a target. Writing to them
produced prose that scored well and read badly.

---

## 1. The subsection header states the result

The supervisor, 9 November: *"Results subsection headers should have the main
result detailed in them (ideally)."* AW, 13 November: *"It is more of a
courtesy than a requirement but my guide likes it so we're doing it."*

IBDex: "Adversarial conditioning removes cohort identity". "Frozen pathway
coordinates recover tissue biology". "PACP separates inflammation from
disease state".

The header is the subsection's contract. **Every paragraph must do work
toward it**, and when the claim is proved the subsection ends.

| rejected | why |
|---|---|
| What the architecture needs | names a topic |
| The atlas settles claims no single cohort could | names an activity |
| Sixteen dimensions carry cell identity and the menstrual cycle | states a result, but AW replaced it with **Biology is an emergent property of training**, which is a stronger claim and reorganised the whole subsection |

**When AW renames a header, re-derive the subsection from it.** The rename
from "Removing the donor costs cycle signal" to "Batch effects and biology
have a measurable trade-off" made my opening paragraph redundant, and I did
not notice until he asked what it was for.

## 2. The first paragraph gives context, because Methods comes later

The supervisor: *"Results should have some context since many things aren't
explained till Methods. If too much context is required just refer the reader
to Methods."*

AW wrote R1's opening himself and then had to tell me R2 was missing one:

> "The subsection starts abruptly. The reader hasn't read methods yet. They
> don't know heads or tails about the model. Results needs to give context,
> remember?"

**The context paragraph does four things and then stops**: names what is
being measured, says what the model was and was not given where that matters,
defines the estimator in one clause, and points at Methods for the rest. It
is not a summary of the findings.

Worked example, R2's opener: what ELAJ sees, the one supervised label, the
withheld list, then "each is tested on the trained model across all 1,577,728
cells, discarding same-donor neighbours so that no label can be recovered
trivially (Methods, *Cross-donor agreement*)."

## 3. Every number must land a conclusion

**This is the rule I broke most.** AW:

> "IBDex always tries to make a point with the numbers. You seem to be
> stating them to no conclusion. Numbers are not the point. Numbers for the
> sake of it is not the point."

And the formulation he singled out as the one to keep:

> "It quotes the value the claim turns on, with its comparator and its
> significance, and nothing else."

| before | after |
|---|---|
| "ELAJ carries 1,883,986 parameters across sixteen latent dimensions, against scFoundation's 100 million across 3,072." | same, **plus** "Pretraining scale conferred no advantage on this corpus." |

Six numbers and no conclusion became six numbers and a finding. **Test every
numeric sentence by deleting it: if no claim weakens, the numbers were
decoration.**

## 4. A short opening sentence is fine if it is a finding

AW asked me to remove them and believed IBDex does not use them. **IBDex uses
them constantly**, and showing him that was the right move:

> "Reliability was coordinate- and compartment-specific." (5 words)
> "PACP separated biological processes that marginal comparison conflated." (8)
> "Held-out probes showed that provenance suppression preserved biology." (8)

Every one states a finding. The rule is therefore not *avoid short openers*
but **an opener must be a result, never a description of the experiment**.

"Six arms spanned the two coefficients" was the one that failed: it describes
what was run. "No competing representation reached that frontier" passes.

## 5. Adjectives carry judgement, not manner

AW: *"use adjectives, adverbs, and tonality instead"* of setting up a result
before stating it.

IBDex: "extensive cohort-associated behavior", "weakly separated", "this
negative clustering result was **consequential**", "Hallmark bile acid
metabolism was **unreliable** at 0.271".

My first pass used "monotonically", "uniformly", "simultaneously" — manner
adverbs that evaluate nothing. The rewrite used "a **substantial** reduction",
"**simply wasteful**", "**cheap** until it saturates", "the **dominant**
structure".

## 6. Do not claw at our own work

AW, cutting a whole paragraph: *"What is the point of the last para? Why are
we clawing at our own work? IBDex never did that."*

The paragraph conceded a limitation immediately after the paragraph that won
the comparison. **Conceding is sometimes necessary; conceding straight after
winning is self-harm.** If a caveat belongs anywhere it is usually the
Discussion, or the subsection whose subject it actually is.

Related, from the same exchange: **a fold-enrichment against a chance rate
set by sample size is not a quantity worth reporting.** 54.5× over a 0.60%
baseline sounds dramatic, but the baseline is a function of donor count, so
the number describes the corpus, not the model. AW: *"vague at best and
misleading if I'm honest."*

## 7. Prose quotes, tables enumerate

AW asked what prose is for when Table 1 holds everything. The answer from
IBDex: **it cites Table 1 twice and never reads it out.** Not one sentence
anywhere has the form "method A scored X, method B scored Y".

| prose | table |
|---|---|
| our own values | every row |
| competitor **ranges**, because a range is a summary | the individual competitors |
| one named exemplar where a name is needed | the rest |
| which comparison matters and why | nothing; a table cannot say this |

**Repetition is fine, recitation is not.** A number in both the prose and the
table is normal.

## 8. Close early

AW: *"Please look for any other points we need to make in para 3, otherwise
close the subsection early."*

R1 ended at 235 words against IBDex's nearest analogue at 325. **A subsection
ends when its header's claim is proved, not when the available numbers run
out.**

Measured IBDex Results subsection lengths: 325, 184, 619, and one long
compound section. There is no target length.

## 9. The measurements, as a smoke alarm only

Taken from IBDex Results, line 496 onward, against our prose:

| | IBDex | our old Results | R1 as shipped |
|---|---:|---:|---:|
| mean sentence | 17.0 words | 20.5 | 16.2 |
| longest sentence | 34 | 52 | 26 |
| decimals per 100 words | 5.5 | 5.6 | — |
| **words of 9+ characters** | **23.1%** | **11.5%** | 15.2% |

**What this diagnosed correctly:** number density was never the problem, and
sentence length and vocabulary were. Our words were half as technical as his.

**What it got wrong:** optimising the long-word share pushed me toward
nominalisation, and a hedging paragraph scores exactly as well as a good one.
Use it to catch a 52-word sentence. Do not use it to decide whether a
paragraph earns its place.

Reproduce with the snippet in `figures/scripts/` history or inline: strip
comments and macros, split on sentence boundaries, count tokens of 9+
alphabetic characters.

## 10. Register, in one line

The reader is an NMI reader who knows what a VAE, a batch effect and a kNN
graph are. **Explain none of them.** Everything I wrote for AW in chat during
this period — composition means the mix of cell types, AUC means how often it
ranks them correctly — is the register his supervisor rejected.

## 11. The working loop that produced R1 and R2

1. AW sets or renames the header.
2. I produce a **numbers sheet** (`R1_NUMBERS.md`, `R2_NUMBERS.md`): every
   relevant value, what it means, and **what it will not support**. No prose.
3. AW writes the opening paragraph, or tells me to write it.
4. I write the rest against the header.
5. AW edits in the tex directly. I fix spelling, grammar and tense only.
6. `./build.sh` must leave zero overfull boxes and both auditors green
   before the subsection is considered done.

**The numbers sheet is the part that earns its keep.** Both times, writing it
caught something the prose would have got wrong: that cell family and disease
status cannot support an emergence claim because other methods beat us on
both, and that the 0.2655 severity figure is readable off study identity.
