# Review feedback, 9 November 2026

**Verbatim, as AW gave it.** Supervisor feedback is broad; the colleague's is
targeted. AW: *"Save this response and use it as a reference for later. Hold
me to these statements unless I specifically overturn something."*

So: this file is the contract. Nothing here is softened, reinterpreted or
quietly dropped. If one of these is overturned, it gets struck through here
with the date and AW's words, not deleted.

---

## Broad strokes

- Read scGPT and other scRNA papers in NMI for "scientific language" and
  "complexity of the phrasing". Our paper has too many simplified phrases and
  overly simplistic words. We have gone too far down the "understandable to
  the lay reader side."
- The "story" of the paper is unclear. (reflects most strongly in abstract and
  introduction but has significant reflections in other sections)
- Results should have some context since many things aren't explained till
  Methods. If too much context is required just refer the reader to Methods.
- No paragraphs with one/two sentences.
- Extended data or Supplementary is completely missing (AW's own note: his
  fault)
- Refer to `Nature_websites/Nature_Writing_and_language_NMI.pdf` loosely for
  register and complexity. Rely more heavily on other NMI papers for
  complexity and level of jargon.
- Keep the Results section very tight. Don't waste words in results. Straight
  to the point and complete in its explanations.
- Don't leave results or figures to interpretation. Use them and discuss them
  well.
- The guide's own recent paper is the directive for the language he prefers:
  <https://www.medrxiv.org/content/10.64898/2026.10.20.26365993v1.full.pdf>
- Any improvements or changes "in the spirit of" or "similar to" any of these
  points are welcome for discussion. **These points are not the full extent of
  the feedback.**

## Specific and targeted

- Numbering the equations. Use the "current - professional" equation display
  format in Word.
- Use the symbol in place of "lambda".
- Section numbering is not needed (see NMI AIP and formatting website PDF).
- Figures should have max width of 180 mm and legend font between 7 and 8 pt.
- Results subsection headers should have the main result detailed in them
  (ideally).
- References should be numbered. Check reference format as well. Check how
  they are supposed to be numbered and how the citations are supposed to be
  referenced.
- Each figure panel should be mentioned in the prose. No panel in any figure
  should go unexplained or unreferenced. Figure space is precious so
  utilisation is very important.
- Figures need to be at a higher resolution.
- Figure 1 changes. AW will supply corrected flow charts. Remove as much white
  space as possible.

---

## Standing interpretation notes

**"Not the full extent of the feedback"** means the list above is a sample of
a register problem, not a checklist to close. Clearing all nineteen items does
not mean the feedback is addressed. The register itself has to change.

**"Too far down the lay reader side" is a reversal of an earlier instruction.**
Up to now the register was set by AW's own voice and by Springer Nature's
"simply state what you found". That still governs *what* Results says. What
changes is the vocabulary and sentence construction: the audience is an NMI
reader who knows what a VAE, a batch effect and a kNN graph are, and does not
need any of them explained in plain words.

---

## Rulings, 9 November

**Results interprets.** AW's call. The settled "flat, no interpretation" rule
is reversed. Each subsection states its numbers and then carries one precise
line of reading; the argument stays in the Discussion. Recorded in
`CONTINUITY.md`, where the old rule is marked reversed rather than deleted.

**The `\flow{}` transitions in Methods are cut.** All nine. The macro in
`preamble.tex` goes dead with them.

**Handovers are maths-free fragments, not paragraph pastes.** AW, 10 November: Word maths does not survive a copy between documents, and a paragraph paste would destroy maths already correct in his file. `make_changeset.py` enforces it and refuses to emit a paste block containing maths.

**Spelling stays British** unless overturned. NMI accepts either if
consistent; IBDex is American.

## The sequence AW set, 9 November

1. **Set up how this is going to work.** AW is specifying this. Nothing starts
   before it.
2. **Cement scGPT and IBDex** as the register reference.
3. **Populate the priority list** properly, after 1 and 2. The list rebuilt on
   9 November is provisional until then.
4. **Then tackle items one at a time.**

Do not run ahead of this order.

---

# Group feedback, 11 November 2026

**Verbatim, as AW gave it.** Presented Figure 1 and Figure 4 to the
supervisor and others in his group. Same contract as above: nothing here is
softened or quietly dropped.

- Fig 1 is good now (the x-axis label in fig 1 c is getting cut off though)
- I presented our current fig 1 and current fig 4. My guide believes that 3
  figures and a table should be enough. I would take that with a grain of
  salt though. He suggested that our current fig 4 should be fig 2.
- There needs to be a lot of supplementary figures and data. Tables, figures
  of all kinds, etc. See IBDex supplementary for reference. Reducing figures
  in the main prose is countered by figures in supplementary. All your crazy
  ideas can fit here.
- Intro needs to clear up the story a little more from the foundations:
  - why scRNA
  - why endometriosis
  - why disease atlas
- Intro also needs to say:
  - what other endometriosis studies have shown (this is partially results
    and discussions because we compare what they have shown and what we are
    able to show. Some work on reproducing individual dataset results on the
    full corpus is needed)
  - what foundation models are capable of saying on a single disease level
    and how having a disease atlas on a study beats foundation model
    approach. (I'd be careful of overreaching here. However, the main message
    of; having a disease atlas is a great thing for a disease, should be very
    evident)
- Results should focus deeply on what is coming out of the model:
  - discuss UMAPs from fig 4 in more detail.
  - Frontier needs to be explained clearly and in detail. It needs to
    highlight the significance of beating everybody, highlight the usefulness
    of having a disease atlas against smaller datasets, etc. This cements the
    paper's place in a journal like NMI. SOTA status is important.
- Discussion needs to be sectioned and should talk about us in comparison to
  3 things: foundation models (how having a disease atlas gives more info
  than a foundation model does), baselines (how building a better
  architecture helps), single datasets (how we can prove or disprove the
  claims made by smaller datasets because of a much larger scale).
- We need to be clear that it is a disease atlas especially because we are
  comparing against foundation models. It is easy for the reader to ask "does
  this translate into a great foundation model" or "what can you say about
  foundation models being shit" or "does that mean it would work on any
  disease". This needs to be future work and limitations.

## What this batch changes, and what it does not

**The one-line story survives intact and is reinforced.** "We need to be
clear that it is a disease atlas" is the first noun of the line AW settled on
11 November. Nothing here reopens the framing; this batch is about making the
framing legible.

**Three rules are overturned or bent by this feedback.** Each is recorded in
`CONTINUITY.md` as settled, so each needs AW's explicit word:

| settled rule | what this batch does to it |
|---|---|
| "Six display items, not eight" | the supervisor says three figures and a table. AW: grain of salt |
| "No further calculation unless a reviewer asks or something is wrong" | reproducing individual-study results on the pooled corpus is new analysis, and a reviewer has in effect now asked |
| my failure mode 1, "do not pre-empt objections nobody has made" | the three reader questions are now named by the supervisor, so answering them is required rather than defensive |

**One instruction is new work, not writing**: *"Some work on reproducing
individual dataset results on the full corpus is needed."* It is the largest
item in this batch by effort and the only one that needs HPC. Scope it with
AW before building anything.

**It also brushes a standing rule.** "No per-study numbers for any metadata
in the latent" stands. Testing a published claim against the pooled corpus
runs the other way, their claim against our 1.58M cells, and is allowed. Any
reproduction that needs a per-study breakdown of a latent metadata test is
not, and has to be redesigned or dropped.

## AW's rulings on the 11 November batch

**1. The current Figure 3 goes to Supplementary.** Both latents by cell
family and phase. Agreed without argument.

**2. Results starts with the frontier, then the UMAPs. This overrules the
supervisor's "fig 4 should be fig 2".** AW's reasons, both of them
structural rather than aesthetic:

> "Without explaining the frontier, the model has no credibility on the
> UMAPs. Plus we need to state why we are only talking about one ELAJ model
> throughout first before displaying its capabilities in the UMAPs."

So the main set is **Fig 1 as it stands, Fig 2 the frontier, Fig 3 the nine
endometriosis UMAPs, Table 1.** Four display items, not three plus a table,
and the order is the argument's order.

**3. Figure 2 has to stop looking like a benchmark.** AW: *"If the frontier
is to become fig 2, it needs to be a little more interesting and less cold
and scientific looking. I might consider supplementing the frontier plots
with some other panels."* **This is a to-do item and a discussion, not a
decision taken.**

**4. The reproduction work is approved and is top priority.** AW:

> "We need to lay out all the major claims of each dataset and see if we can
> support or reject them in our architecture. That is a results axis we
> hadn't considered yet."

**A new results axis**, not a citation-gathering exercise. Every dataset in
the corpus must be accounted for even where its claims go untested.

**5. The Abstract goes before the Introduction.** Reversing the order in
PRIORITY. AW: *"I agree on the intro structure. But now it requires work on
the HPC. I feel like this intro needs an abstract to work better. So I'll
place abstract first this time."*

**6. The Discussion is deferred**, and deliberately. It needs the HPC
results and the figure placement settled before it can be structured.

**7. Supplementary gains an item: analysing the group embeddings.** AW's,
and it may need HPC time of its own.

**The order of work AW set**: claims laid out by paper, then pick what is
most relevant, then scripts and inferences.
