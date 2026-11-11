# Priority list

**The goal: ELAJ at an NMI reviewer's desk, in the strongest honest shape.**
Rebuilt 9 November 2026 around the register review. The feedback itself is in
`REVIEW_FEEDBACK.md`, verbatim, and that file is the contract.

**The paper is drafted end to end.** Abstract, Introduction, Results,
Discussion and Methods are written, Figures 1 to 4 and Table 1 are built and
wired, 29 pages build with zero overfull and both auditors green. What the
review changes is not coverage. It is register, story and display-item
discipline.

---

## The diagnosis, measured

The supervisor's words were *"too many simplified phrases and overly
simplistic words"* and *"gone too far down the understandable to the lay
reader side."* That is measurable against his own recent paper, IBDex
(`medRxiv 10.64898/2026.10.20.26365993`), which he named as the directive.

| | our mean sentence | IBDex | our words >=9 chars | IBDex |
|---|---:|---:|---:|---:|
| Introduction | 25.8 | 19.0 | 14.7% | **31.5%** |
| Results | 22.0 | 19.4 | 12.2% | **26.6%** |
| Discussion | 18.5 | 17.2 | 12.6% | **27.7%** |

**Our sentences are longer and our words are shorter.** The fix is therefore
not "write more densely" in the sense of longer sentences. It is the opposite:
shorter sentences built out of denser technical terms, with no term explained
that an NMI reader already knows.

IBDex is worth reading in full before any rewriting. It is structurally the
same paper as this one: a conditional VAE with adversarial suppression of
cohort identity, a fixed gene interface, a pathway basis, a sixteen
dimensional latent, pooled across four cohorts, same senior author. It is not
only a register sample. It is how he expects this argument to be told.

---

## Decisions taken, 9 November

Standing until AW overturns them. `REVIEW_FEEDBACK.md` is the contract for the
feedback itself; this is the running record of what we have settled against it.

- **Results interprets.** The settled "flat, no interpretation" rule is
  reversed. Each subsection states its numbers and then carries one precise
  line of reading. The argument still belongs to the Discussion.
- **The eight `\flow{}` transitions in Methods are cut**, and the `\flow{}`
  macro in `preamble.tex` goes dead with them.
- **British English, confirmed.** IBDex is American; we do not follow it there.
- **The register references live in `Atharva Papers/_txt/`**, extracted to
  text with a README recording what each is for. **IBDex is the language
  directive, not the format directive**, because it is submitted to
  Gastroenterology rather than a Nature journal. **scGPT fills the format
  gap.** Images are not in the extracted text; reading a figure is a separate
  task against the PDF.
- **Every change follows one sequence**, AW's, because the guide's OneDrive
  Word file is the authoritative document:
  1. make the change in the `.tex`
  2. build the corresponding Word file
  3. hand AW a changeset of short **maths-free** find-and-replace
     fragments, built by `make_changeset.py`, and he applies them.
     Word maths does not survive a copy, so a paragraph paste would
     destroy equations already correct in his file.
  **This overturns the 8 November rule not to generate a `.docx` each time.**
- **Work order.** Low-hanging fruit first, meaning clear misses that need no
  judgement. Then the story, which then guides the rest of the changes and the
  Supplementary section.

## Tier 0. Decisions needed before rewriting

- [x] **Does Results interpret?** RESOLVED: it does. `CONTINUITY.md` records as settled that
      Results is *"flat. State what was done and what came out. No
      interpretation"*, on Springer Nature's own wording. The new feedback
      says *"Don't leave results or figures to interpretation. Use them and
      discuss them well"*, and IBDex's Results interprets freely
      (*"This negative clustering result was consequential, so the atlas was
      treated as a continuous molecular reference"*). The newer instruction
      should win, but it reverses a settled rule and AW has to say so.
- [x] **Do the `\flow{}` transitions in Methods survive?** RESOLVED: cut. Eight one-line
      rhetorical questions bridging subsections (*"A reconstruction exists.
      What stops it being produced WITHOUT the latent?"*). They are AW's and
      they work, but they are one-sentence paragraphs and they are the single
      most lay-reader device in the paper. Both new rules point at them.
- [x] **British or American spelling?** RESOLVED: British. Ours is British throughout
      (normalisation, labelled). IBDex is American (normalization, behavior,
      analyzed). NMI accepts either if consistent. A switch is mechanical but
      it touches every section.
- [ ] **How far does the story rebuild go?** "The story of the paper is
      unclear" is the deepest comment and it is not a section-local fix. See
      Tier 1.

## Tier 1. The story and the register

This is the spine of the work and the rest is mechanical beside it.

- [x] **The story. SETTLED 11 November**, see CONTINUITY. It is a case
      study, framed against `hrovatin2025atlases`. Everything below now
      has to be re-planned against that line.
- [ ] ~~The story.~~ Stated most strongly of the abstract and Introduction
      but *"has significant reflections in other sections"*. IBDex's own story
      is one sentence long and everything serves it: historical data
      accumulate without becoming a reference, so build a frozen atlas new
      cohorts can use without retraining. Ours needs an equivalent that is
      true, and then abstract, Introduction, Results headers and Discussion
      all have to deliver that one claim in order.
- [ ] **The Introduction, which is also `[65]` and `[83]`.** AW has ruled a
      full restructure with the word overrun carried. Seven paragraphs
      planned, ~940 words against 588 now, with a new related-work paragraph
      naming each single-cell study by what it compared and closing on the
      ceiling as arithmetic. Plan is in the 9 November exchange;
      `INTRODUCTION_STRUCTURE.md` still has to be edited by AW before prose.
      Note IBDex opens on the field's methodological failure rather than on
      the disease's human cost, which is a third option against both the
      current ¶1 and the opening the supervisor cut.
- [ ] **Results: context, then tightness.** *"Results should have some
      context since many things aren't explained till Methods. If too much
      context is required just refer the reader to Methods."* IBDex does this
      in its first Results paragraph, restating corpus, split and gene
      interface before any number. Ours opens cold. Then the other half of
      the instruction: *"Keep the Results section very tight. Don't waste
      words."*
- [ ] **Results subsection headers must state the finding.** Currently
      question-shaped or topic-shaped. IBDex's ten headers are all declarative
      results and are the template: *"Adversarial conditioning removes cohort
      identity"*, *"PACP separates inflammation from disease state"*,
      *"Deep remission attenuates inflammation, not disease state"*. That last
      one is the exact shape our `[4]` dissociation needs.
- [ ] **No paragraphs of one or two sentences.** Results 9, Methods about 15
      once the `\flow{}` transitions are set aside. Introduction, abstract and
      Discussion are already clean.
- [ ] **Lay phrasing to hunt.** *"It is clear that"* and *"It is relevant to
      state that"* are both live in Results `[3]`. They are AW's words and
      were restored once on the tone-is-mine rule, so they come back as
      current / proposed / why, but the new feedback is explicitly about this.

## Pinned, built but unplaced

- [ ] **The dissociation panel**, `figures/scripts/panel_dissociation.py`,
      `pinned/panel_dissociation.png`. IBDex Figure 2c's form applied to the
      cross-donor results: forest on the left against each label's own
      permutation null, the numbers aligned on the right, non-significant
      rows greyed and badged `ns`. Grouped so the argument is visible before
      a number is read: every contrast including control donors clears, and
      neither contrast restricted to patients does. **AW: built, looks right,
      no home yet. Pinned 10 November.** Candidates are Figure 4 or Extended
      Data.
- [ ] **It surfaces a number the paper does not carry.** Surgical stage on
      the whole corpus is $+$0.3320, $p=0.005$ at 58 donors. Results only
      reports the held-out reading, 0.1313 at $p=0.303$ over 16 donors. It
      does not contradict the paper, because stage clears precisely through
      the control contrast and the patients-only tests still fail, but a
      reviewer reading the panel would ask. **Either the number goes into
      Results `[4]` or the row comes out of the panel.**
- [ ] **Panel a mock-up**, `figures/scripts/panel_a_mockup.py`. The
      architecture redrawn in IBDex's grammar: four role headings, one hue
      family each, detail pushed out of the boxes into grey lines, dimensions
      annotated under every stage. Awaiting AW's call on whether it replaces
      his own drawing.

## Tier 2. Display items

- [ ] **Every panel must be referenced in prose, and almost none is.**
      Measured: Figure 1 has 6 panels, Figure 2 has 8, Figure 3 has 10,
      Figure 4 has 9, plus Table 1. **33 panels, 5 referenced.** Figures 1 and
      3 and Table 1 are never referenced anywhere in the prose.
- [ ] **Two live references point at a figure that no longer exists.**
      `Fig.~5a` and `Fig.~5` in Results, from before Table 1 replaced
      Figure 5. And `Fig.~4a` is used for two different claims, one of which
      is a Figure 3 panel.
- [ ] **No figure carries a `\label`.** Every figure number in the prose is
      hardcoded, which is why they went stale. Add labels and `\ref` them.
- [ ] **`(Supplementary figure reference)` is a literal placeholder** in live
      Results prose and would print.
- [ ] **Extended Data and Supplementary are completely missing.** AW's own
      note. Ten Extended Data slots, priority order in
      `06-display-items.tex`; Supplementary Figure 1 is the ablation UMAPs.
      IBDex ships 26 Supplementary Tables and 6 Supplementary Figures, which
      is the scale he is used to.
- [ ] **Figure 1 rebuild.** AW supplying corrected flow charts for panels a
      and b. Remove as much white space as possible.
- [ ] **Resolution and geometry.** NMI's own spec, confirmed from
      `NMI_AIP_and_formatting.pdf`: **300 dpi minimum, maximum width 180 mm**,
      and **5 to 7 pt sans serif for in-panel text labelling**. The review
      said 7 to 8 pt for legends; legend body text is typeset by the journal,
      so check which was meant before changing anything.

## Tier 3. Mechanical and formatting

- [ ] **Number the equations.** NMI: equations referred to in the text take
      parenthetical numbers and are cited as *"equation (1)"*. One equation
      currently carries a label (`eq:token`); the rest are unnumbered. IBDex
      does exactly this with equations (1) to (3).
- [ ] **Use the symbol for lambda.** `\texttt{lambda\_dab}` appears in Results
      prose as the code variable name. It should be the maths symbol
      throughout prose, with the code name confined to Code availability.
- [ ] **Equation display format in Word** should be "current - professional".
      Affects the DOCX conversion, not the `.tex`.
- [ ] **Section numbering is not needed.** Nature does not number sections and
      Methods takes *"short, bold headings"*. Check nothing numbered survives.
- [ ] **References: numbered in the DOCX, not just the PDF.** The `.tex`
      already uses `natbib[numbers,sort&compress]` with `unsrtnat`, so the PDF
      is numbered. **The supervisor reads the Word file, and pandoc renders
      author-year there** (his `[83]` anchor literally shows
      "( Bontempo and Schiff 2025)"). So this comment is a conversion
      artefact. The fix belongs in `make_draft.sh`, with a numeric CSL style.
- [ ] **Reference format and ordering.** NMI numbers sequentially across Main
      Text, then Methods, then Data Availability, then Tables, then Figure
      Legends, then Extended Data. Article titles are required for Articles.
      URLs go parenthetically in the text, never in the reference list. Grants
      may not be numbered references. BibTeX must be flattened from the `.bbl`
      into the `.tex` before submission.
- [ ] **Nine comparison methods are cited nowhere in the paper.** PCA, scVI,
      scANVI, Harmony, Scanorama, Geneformer, SCimilarity and scFoundation
      have no citation in any section, and scGPT is cited only as the source
      of the DSBN idea. There is no baselines subsection in Methods. Free to
      fix, since Methods references are uncapped, and conspicuous if left.
- [ ] **`kedzierska2025zeroshot` is in the bib and cited nowhere.** It is the
      zero-shot evaluation showing Geneformer and scGPT unreliable without
      fine-tuning, and it is the citation that licenses the Introduction's
      claim that a pretrained model is not an alternative. That sentence is
      currently uncited.

---

## Carried over

### The supervisor's comments still ours
`[97]` rephrase the pooled-corpus paragraph (absorbed by the Introduction
rebuild) · `[42]` avoid the abbreviation in the abstract · `[82]` trials or
studies, check before answering (absorbed) · `[503]` and `[511]` in *Data
collection*, "a candidate dataset, record or query?" and "the last constraint,
what was it and which is last?"

**His to clear**: `[132]`, `[467]`, `[507]`. AW has replied and is waiting.

### To be discussed in person, not over comments
Both SYNCED INTO THE TEX AS HE MADE THEM. These are the words to restore if
the conversation goes that way.

- [ ] **The Introduction's opening line, cut.** "Pain is a recurring date on a
      calendar for 190 million people worldwide (`who2025endometriosis`)."
      Its citation is now unused.
- [ ] **The human-health paragraph, cut.** "A subtle but deliberate choice in
      this study is to treat this disease as a human health problem rather
      than a gendered disease. At a scale of hundreds of millions of patients,
      we believe this to be necessary to bring attention to this problem."

### References
- [ ] `vasilevsky2022mondo` and `czi2023cellxgene` are both preprints for core
      infrastructure. Check for journal versions.
- [ ] Six references cited zero times: `gbd2019asthma`, `idf2021diabetes`,
      `nhs2024noncoding`, `rands2014constrained`, `ballard2006delay`,
      `li2025factors`, plus `who2025endometriosis` since the opening was cut.
      The last three come back with the Introduction rebuild.
- [ ] Cite `duempelmann2026endometrium` on the rASRM I--II / III--IV sentence.
- [ ] `hoffmann2001girl` and `chen2008gender` are in the thesis bib but not
      the paper's. Only needed if the delay material returns, and they collide
      with the standing rule against naming donors as women.

### Externals, AW owns all of these
- [ ] Repository URL, licence, Zenodo DOI. Methods claims predictions were
      registered before training, checkable only if the repo is public.
- [ ] Funding and grant numbers. Final author list. Reporting Summary.
      Cover letter. bioRxiv preprint.

### Smaller
- [ ] Extend both auditors to Methods.
- [ ] Abstract is 160 words against the 150 limit, and `[42]` will change it.
- [ ] One unnamed skipped test in the suite of 1,945.
