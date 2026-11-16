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

---

# Adding to a section that is already written

Rules 1 to 11 were learned writing Results from nothing. **12 to 16 were
learned on 14 November inserting one paragraph into a finished section and
getting it wrong**, AW: *"completely off the mark... stands out like a sore
thumb. It uses unnecessary words, its too long, it is in a completely
different sounding phrasing."*

**The method that fixed it is the rule behind all five: read the paragraphs
either side and copy their shape before writing a word.** Not the register of
the paper in general, the shape of the specific neighbours. Everything below
was derived by reading the subsection back, not from memory.

## 12. A paragraph opens on a short flat finding

Four to nine words, declarative, no procedure in it.

> "Cell composition does not distinguish case from control."
> "It is a change in what immune cells are doing."
> "Those two annotations agree."

**What failed:** *"Deriving a one-vs-rest signature per family within each
study and comparing them across the 13,034 genes both panels measure, the
top hundred genes overlap by..."* A participial phrase that makes the reader
hold the procedure in mind before any claim arrives. The section never does
this.

## 13. Procedure lives in a clause, never in a sentence

| as the section does it | words |
|---|---:|
| "fitted on 70\% of donors and scored on the remainder" | 10 |
| "with study fitted as a covariate" | 6 |
| "(Methods, \emph{Label transfer})" | 3 |

**What failed:** a 24-word sentence explaining why genes were restricted to
those both panels measure. It became *"Restricting to jointly measured genes
keeps a gene absent from one panel from reading as a non-marker"*, and a
caveat gets the same treatment: **one clause, not a sentence.**

## 14. The number list has a fixed shape, and the unit is named once

> "at \textit{P}~=~0.6186 for immune cells, 0.7360 stromal, 0.9016
> epithelial and 0.2358 endothelial"

Name the quantity on the first item and drop it thereafter. So "76 of its top
hundred genes in stromal cells, 69 epithelial, 69 endothelial and 61 immune",
never "69 in epithelial, 69 in endothelial and 61 in immune".

**Match the neighbourhood's precision too.** That subsection quotes four
decimals throughout, so 0.8256 and 0.7129, not 0.826 and 0.713. The auditor
catches this, but it should not have to.

## 15. Put it where the flow carries it, not where the topic says it belongs

I placed the marker result after *"What follows tests claims each source
study made from tens of donors against the pooled 194"*, then immediately
wrote about two studies. The sentence promised the pooled corpus and the
paragraph delivered a pair.

It belongs inside the transfer paragraph, which is about those two
annotations: **the transfer works, those two annotations agree, neither saw
disease status, and what follows tests the pooled claims.** A subsection
header names its argument; it does not say where a given result sits.

## 16. A source study is named by its key, with its own donor count

> "\texttt{duempelmann\_2026} reports the same from 60 donors, where one cell
> type of 57 shifted."
> "\texttt{marecko\_2024} reports that prior atlases lack reproducible marker
> signatures; read on one gene space, theirs reproduce."

The study key in `\texttt{}`, the claim as they made it, the scale they made
it at, then ours. The citation rides along; the key is what carries it.

## 17. A number the prose quotes must be a value some file holds

Not a statistic computed over a file. I wrote a null as *"0.9 genes and
0.004"*, which are **means of the null table's rows**, and both auditors
rejected them because no cell holds either. Restating it as a bound the file
does hold, *"Twenty within-study label shuffles never share more than
three"*, is auditable **and** a stronger sentence.

**The auditors are a drafting tool here, not a gate at the end.** Both of
these were caught by running `./build.sh`, not by rereading.

## 18. Budget by the neighbour, not by the section

The comparable paragraph is four sentences and about seventy-five words.
The first attempt was five and a hundred and ten. **Count the paragraph you
are sitting next to before writing**, the same way rule 8 closes a subsection
when its claim is proved rather than when the numbers run out.

---

# Figure legends. Read off IBDex and scGPT, 17 November

AW: *"Figure legends are severely lacking. Please check if register.md has
anything on it otherwise, refer to other NMI papers and IBDex to understand
how to write legends."* It had nothing. This is that reading.

Several of ours were one clause long. **"Table S29 drawn."** is not a legend.

## The two registers, measured

| | scGPT, Nat. Methods | IBDex |
|---|---|---|
| title | the **content**: "Model schematic", "Cell type-annotation results" | the **finding**: "The frozen representation suppresses cohort identity while retaining biological signal" |
| length | 90 to 160 words | 150 to 260 words |
| panels | lettered, one to three sentences each | lettered, one to three sentences each |
| numbers | $n$ and the statistical convention only | **every value the panel shows, with its comparator** |
| interpretation | almost none | **one reading per panel** |
| abbreviations | **every one expanded**, in a run at the end | expanded inline |

**Follow IBDex.** It is the reference that decides what goes to NMI, and
its register is the one CONTINUITY already records for our Figure 3:
*the interpretation is from figures the reader sees.* Take scGPT's
abbreviation discipline on top, because that costs nothing and NMI requires
it.

## The shape, in order

1. **A bold title that states the finding**, not the ingredients. "The
   frozen atlas transfers without refitting across three unseen IBD
   cohorts" beats "Transfer results". If the figure genuinely has no single
   finding, a content title is honest; most figures have one.
2. **A sentence of setup** where the reader cannot otherwise parse the
   axes: what the units are, how many there are, what the split was.
3. **Each panel in turn, by letter**, with the numbers that panel shows.
4. **Each number against its comparator.** IBDex never writes a bare
   figure: *"balanced accuracy 0.31 against chance 0.25"*, *"seven-level
   site reached 0.31 against 0.14"*. Ours must carry the null, the chance
   rate or the base rate the same way.
5. **One line of reading per panel**, bounded by what is drawn. IBDex:
   *"indicating that the separation arises from the estimand rather than
   the input data"*, *"although anatomy strongly re-ranks individual
   genes"*.
6. **$n$ wherever a group is named.** Every cohort, arm and subgroup.
7. **Named exemplars where a ranking is drawn**: *"led by DMBT1, DUOXA2,
   OLFM4, NOS2 and CXCL1"*.
8. **The one methodological condition that protects the reading**, if there
   is one: *"Post-training probes were fitted after freezing and did not
   influence model selection"*. One clause, not a paragraph. This is the
   single exception to the no-pre-emption rule, because a legend is read
   away from the Methods.
9. **Every abbreviation expanded**, scGPT's discipline.

## What a legend must never do

- **Point at a table instead of saying something.** "Table S29 drawn" tells
  the reader nothing a glance does not.
- **Repeat the prose sentence that cites it.** The prose makes the
  argument; the legend makes the figure readable on its own. A reader who
  opens the supplementary at that page must be able to read the figure
  without finding the paragraph.
- **Name our own arm as the hero**, or annotate the good news. That rule
  (CONTINUITY, figures settled 4-5 November) is unchanged: the panel shows
  data, the legend defines the axes and gives the reading, the reader draws
  the conclusion.
- **Hedge.** Same register as everything else.

## The short caption is a different object

`\caption[short]{long}` prints the short form in the contents list. That one
is a **title, three to seven words**, and it is the only place a content
label is right.
