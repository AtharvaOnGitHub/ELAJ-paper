# Introduction — paragraph map for review

**Edit this file. Nothing gets written as prose until you have.**

Same contract as `METHODS_STRUCTURE.md`: this is the plan, you change it, and
only then does prose happen. Columns are what the paragraph does, its word
allocation, where the text comes from, and what it costs in citations.

---

## What the guidelines actually say

Three things matter here and two of them are not what an ML paper expects.

| source | says |
|---|---|
| **Nature**, *Formatting guide* | "Articles start with a **fully referenced summary paragraph**... **Sections are separated with subheadings to aid navigation.** Subheadings may be up to 40 characters" |
| **Nature**, *Formatting guide* | "The typical length of an **8-page article with 5-6 modest display items is 4,300 words**" (summary plus body). "A 'modest' display item is one that, with its legend, occupies about a quarter of a page (equivalent to ~270 words)" |
| **Nature**, *Formatting guide* | "As a guideline, articles typically have **no more than 50 references**. There is no such constraint on any additional references associated with Methods or Supplementary Information" |

### Hard rules, not guidelines

- **There is no "Introduction" heading.** Nature Articles run summary
  paragraph → untitled body text → first subheading. Our
  `sections/01-introduction.tex` currently carries `\section*{Introduction}`,
  which is scaffolding and comes out before submission. The Introduction is
  simply the text before the first Results subheading.
- **The 50-reference cap is on the main text**, and the Introduction is where
  most of them go. Budget it here or discover it at the end.
- **Methods references are free.** A claim that needs a citation is cheaper
  in Methods than anywhere else, so anything that can defensibly live there
  should.

### The length arithmetic, because it is tighter than it looks

4,300 words covers summary + Introduction + Results + Discussion at **5-6**
display items. The figure list allocates **eight**. At ~270 words of page
equivalent each, two or three extra items cost roughly 540-810 words of text,
which puts the real body budget near **3,500-3,800**.

| | words |
|---|---:|
| Summary paragraph | 200 |
| **Introduction** | **750** |
| Results | ~1,800 |
| Discussion | ~1,000 |
| **total** | **3,750** |

So 750 is the allocation below, and the Introduction is the section with the
most thesis material and therefore the easiest place to overrun.

---

## The six paragraphs

| # | what it does | words | source | citations |
|---|---|---:|---|---:|
| 1 | **The disease, as a problem rather than a topic.** Prevalence (10% of people of reproductive age, 190 million), no known cause, no cure, diagnosis by surgery and lesions read by eye. The one thing a reader outside the field must hold: symptoms follow the menstrual cycle, so the cycle is not a nuisance variable in this disease, it is the axis the disease moves along. | 130 | Thesis §1.1 *Endometriosis* + §1.2 *Pain on a schedule* — **compress hard, the thesis spends 1,400 words getting here** | 2-3 |
| 2 | **What single-cell work has established, and the ceiling it hit.** Lesions are not simply displaced endometrium; the unaffected endometrium of an affected person is already different; immune involvement recurs across every study. Then the ceiling: each of those is one cohort of tens of donors, and the largest published single-cell study of this disease is small. | 150 | Thesis §2.2.2, §2.2.3, §2.2.4, §2.2.6 — the evidence is already assembled in `Thesis/literature-evidence.md`, keyed to bibtex | 5-7 |
| 3 | **Pooling is the only route to scale, and integration is a solved problem elsewhere.** Atlases in other fields work and the integration is measurable. State plainly that this is the standard move, so that the next paragraph is a surprise rather than a complaint. | 110 | Thesis §2.4.1, §2.4.2 | 3-4 |
| 4 | **THE CONFOUND. The intellectual core, and nothing in the paper means anything before a reader has it.** Each donor is biopsied once. Menstrual phase is therefore constant within a donor, and a per-donor offset is geometrically the same object as a batch effect. Batch correction cannot tell them apart, so removing the batch removes the cycle. Not a caveat: it is why naive integration of endometrial data silently discards the biology people want. | 150 | **NEW.** The thesis has the confound as a data property; it has never been stated as the reason the standard tooling fails | 1-2 |
| 5 | **Why the obvious alternatives do not escape it.** A stronger batch correction removes more cycle. A pretrained single-cell foundation model is not an answer either, and an NMI readership will ask within the first page, so it is answered here rather than in Methods. | 110 | Thesis §2.4.3 *Foundation models, and why not simply use one* | 3-4 |
| 6 | **What we do, and what the paper delivers.** Not "we propose a novel architecture". The trade-off is made explicit and measurable: a frontier between donor-blindness and retained cycle signal, with results reported from a named point on it. Then the contributions as a short list that Results then delivers in order. **Flow rule: the last sentence here is the first question Results answers.** | 100 | Thesis §1.5 *Contributions* — three contributions, reframed around the frontier | 0-1 |

**Total 750 words, 14-21 citations.**

---

## Citation budget

`Thesis/literature-evidence.md` holds **19 keyed papers** with the claims
already extracted and attributed; `Thesis/references.bib` has 34 entries.

| | |
|---|---|
| Available, keyed and evidenced | 19 |
| Introduction needs | 14-21 |
| Main-text cap | **50** |
| Leaves for Results + Discussion | ~30 |

That is workable but not loose. Two levers if it tightens: the corpus studies
can be cited once collectively in the Introduction and individually in
Methods, where references are uncapped; and the integration-works paragraph
(#3) can carry two exemplars instead of four.

---

## Open questions, which is what this file is for

1. **Six paragraphs or five?** The existing notes in
   `sections/01-introduction.tex` plan five and have no equivalent of #5,
   foundation models. My argument for keeping it: NMI's readership is
   machine-learning first, "why not fine-tune scGPT" is the first question
   they will ask, and answering it in Methods is too late. Against: it is 110
   words spent on what we did *not* do.
2. **Does #3 belong at all?** It says integration works elsewhere, which a
   reviewer may already believe. It exists to set up #4 — the surprise lands
   harder if the standard move has just been endorsed. But it is the
   paragraph I would cut first under pressure.
3. **How much disease background is too much?** The thesis spends 1,400
   words. Paragraph 1 has 130. A clinician reader will find that thin; an ML
   reader will find anything more an obstacle. NMI's readership makes me lean
   thin, but you know the audience you want.
4. **Where do the 10% and 190 million numbers come from?** `who2025endometriosis`
   in the thesis. Still the right source for a Nature-family paper, or does
   this want a primary epidemiology citation?
5. **"people of reproductive age"** is the wording the standing instruction
   requires, and the thesis says "women of reproductive age" in its first
   sentence. That sentence is the one place the project's own rule is broken,
   and the paper fixes it.
