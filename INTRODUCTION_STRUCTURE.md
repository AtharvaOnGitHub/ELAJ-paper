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

Revised 30 October 2026 on AW's ruling: the "integration works elsewhere"
paragraph is **cut** — that claim would rest on atlases in fields with
different confounds and not enough work has been done to assert it. In its
place, the thesis's account of the diagnostic delay, which AW asked for.

| # | what it does | words | source | citations |
|---|---|---:|---|---:|
| 1 | **Pain on a schedule.** The thesis's hook and it should open the paper: a patient can point to the week the pain will arrive, and a condition that announces itself on a calendar ought to be among the easiest to recognise. Prevalence, and the fact that symptoms follow the cycle — so the cycle is not a nuisance variable in this disease, it is the axis the disease moves along. | 120 | Thesis §1.1 + §1.2, opening | 2 |
| 2 | **It takes eleven years, and what those years are made of.** 11.1 years mean from first symptom to diagnosis across 444 surgically confirmed patients. Six and a half of them fall *after* the patient presented and asked for help. Of those misdiagnosed, 49.5% were first told the cause was a mental health disorder — a disease of the pelvis diagnosed as a disease of the mind in about half of cases. Then the general pattern it sits inside: the same complaint draws a sedative for a woman and an analgesic for a man, and misdiagnosis is the single largest clinician contribution to delay. | 180 | Thesis §1.2 — `bontempo2025diagnostic`, `ballard2006delay`, `hoffmann2001girl`, `chen2008gender`, `li2025factors`, all five already in `references.bib` | 5 |
| 3 | **The published record is a record of the believed.** The survey cohort was 85.6% white and 64.5% degree-educated, so eleven years is the delay for the patients best placed to be believed. Every single-cell cohort in existence is drawn from patients who reached laparoscopy, and reaching laparoscopy means having been believed first. Whatever this corpus samples, it is not everyone with the disease. | 90 | Thesis §1.2, closing — **the strongest two paragraphs in the thesis and I had missed them** | 0-1 |
| 4 | **What single-cell work has established, and the ceiling it hit.** Lesions are not simply displaced endometrium; the unaffected endometrium of an affected person is already different; immune involvement recurs across every study. Then the ceiling, which is arithmetic rather than anyone's failure: each result is one cohort of tens of donors, because surgical diagnosis makes every cohort small, expensive and assembled one hospital at a time. Pooling is the only route to the sample size the question needs. | 140 | Thesis §2.2.2-§2.2.6 and §1.3 closing; evidence keyed in `Thesis/literature-evidence.md` | 5-7 |
| 5 | **THE CONFOUND. The intellectual core, and nothing in the paper means anything before a reader has it.** Each donor is biopsied once. Menstrual phase is therefore constant within a donor, and a per-donor offset is geometrically the same object as a batch effect. Batch correction cannot tell them apart, so removing the batch removes the cycle — and a stronger correction removes more of it. Not a caveat: it is why naive integration of endometrial data silently discards the biology people want. | 150 | **NEW.** The thesis has the confound as a data property; it has never been stated as the reason the standard tooling fails | 1-2 |
| 6 | **What we do, and what the paper delivers.** Not "we propose a novel architecture". The trade-off is made explicit and measurable: a frontier between donor-blindness and retained cycle signal, with results reported from a named point on it. One sentence on why a pretrained foundation model is not the answer either. Then the contributions as a short list Results delivers in order. **Flow rule: the last sentence here is the first question Results answers.** | 110 | Thesis §1.5 and §2.4.3 | 1-2 |

**Total 790 words, 14-19 citations.**

### What the delay material is actually doing

Three jobs, and it is worth being deliberate about which:

1. **It earns attention.** "A condition that announces itself on a calendar
   ought to be among the easiest to recognise. It takes eleven years" is the
   best sentence pair the project has.
2. **It is an indictment, and it is cited.** Five references, all in the bib,
   none of them ours. This is not editorialising.
3. **Paragraph 3 is methodological, not rhetorical.** "The published record is
   a record of the believed" is a selection-bias statement about our own
   corpus. It belongs in the paper because it is true and load-bearing, not
   because it is affecting.

"No model recovers a patient who was sent home" is the thesis's line. It is
the right closing sentence for paragraph 3 if we are willing to be that
direct in a Nature-family paper, and I think we should be.

## Citation budget

`Thesis/literature-evidence.md` holds **19 keyed papers** with the claims
already extracted and attributed; `Thesis/references.bib` has 34 entries.

| | |
|---|---|
| Available, keyed and evidenced | 19 |
| Introduction needs | 14-19 |
| Main-text cap | **50** |
| Leaves for Results + Discussion | ~30 |

Note that the delay material adds five references the evidence file does not
cover — `bontempo2025diagnostic`, `ballard2006delay`, `hoffmann2001girl`,
`chen2008gender`, `li2025factors` — all present in `Thesis/references.bib`
and none of them single-cell papers. So the Introduction's citation load is
now split between a clinical half and a single-cell half.

That is workable but not loose. The lever if it tightens: the corpus studies
can be cited once collectively in the Introduction and individually in
Methods, where references are uncapped.

---

## Open questions, which is what this file is for

1. **The standing rule collides with the cited literature, and this is
   yours to settle.** The rule is absolute as written — never refer to a
   donor, patient or person as a woman anywhere in this project, because
   specifying women makes it a women's health problem rather than a human
   health problem. But paragraph 2's pain-bias citations are *about* women
   specifically: `hoffmann2001girl` is "The Girl Who Cried Pain: A Bias
   against Women in the Treatment of Pain", `chen2008gender` measures gender
   disparity in analgesia, `ballard2006delay` studies women's experiences.
   Reporting what those studies found requires naming the groups they
   compared. Two readings are available and I am not going to choose:
   (a) the rule governs how we describe *our* participants, and reporting a
   cited study's own comparison is a different act; or (b) the rule is
   absolute and the finding must be stated without the word, which is
   possible but weaker — "patients whose pain is read as emotional rather
   than physical" loses the measured contrast. The thesis itself uses
   "women" in these sentences, so this has not been faced before.
2. **Does paragraph 3 belong in the Introduction or the Discussion?** "The
   published record is a record of the believed" is both motivation and
   limitation. In the Introduction it sets honesty early and frames what the
   corpus is; in the Discussion it is a limitation among limitations. My
   view: state it in the Introduction, because a reader who meets it at the
   end will wonder why it was withheld, and cross-reference from the
   Discussion. It costs 90 words in the tightest section of the paper.
3. **How much disease background is too much?** The thesis spends roughly
   2,100 words reaching the point paragraph 1 has 120 for, and the delay
   material was 700 of them against 180 here. NMI's readership is
   machine-learning first, which argues thin; the delay material is the most
   distinctive thing in the paper's framing, which argues otherwise. The
   allocation above is already 300 words — 40% of the Introduction — on the
   clinical picture.
4. **Is `who2025endometriosis` carrying too much?** In the thesis it
   supports the 10% prevalence, the 190 million figure, "the causes are
   unknown" and a four-to-twelve-year delay range. Four claims on one
   reference, and paragraph 2 then gives a measured 11.1 years from
   `bontempo2025diagnostic` which sits inside that range but is a different
   kind of number. Decide whether the WHO figure or the measured one leads.
5. **Does the foundation-model sentence survive?** It is now one sentence
   inside paragraph 6 rather than a paragraph of its own, on the same
   reasoning that cut the integration paragraph — it is space spent on what
   we did not do. Against cutting entirely: an NMI readership asks "why not
   fine-tune scGPT" on the first page, and Methods is too late.
6. **"people of reproductive age"** is what the standing instruction
   requires, and the thesis's first sentence says "women of reproductive
   age". That sentence is the one place the project's own rule is broken and
   the paper fixes it — but see question 1, which is the harder version of
   the same problem.
