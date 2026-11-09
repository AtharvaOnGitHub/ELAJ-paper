# Priority list

**The goal: ELAJ at an NMI reviewer's desk, in the strongest honest shape.**
Rebuilt 9 November 2026. A line with no *blocked by* can be done now.

**The paper is written.** Abstract, Introduction, Results, Discussion and
Methods are all drafted, Figures 1 to 4 and Table 1 are built and wired, and
29 pages build with zero overfull and both auditors green. What remains is
the supervisor's comments, two display items, and the externals.

## Where it stands

| section | words | state |
|---|---:|---|
| Abstract | 160 | written from scratch 7 Nov |
| Introduction | 594 | ¶6 written; two paragraphs cut by the supervisor |
| Results | 2,616 | **done** |
| Discussion | 1,249 | **done** |
| Methods | 5,745 | **done**, zero notes |
| Figures 1--4, Table 1 | | built, wired, legends written |

---

## The supervisor's comments

His Word file is authoritative. Hand AW each change as **location / what it
is / exact text**; he applies them in Word. Do not generate a `.docx`.

**Cleared, 9 of 19.** `[1330]` table legend · `[1077]` BlueBEAR to Methods ·
`[520]` UBERON and MONDO · `[479]` and `[490]` archive references · `[1046]`
accession citations · `[471]` the six anatomical sites · `[3]` affiliation ·
plus his own untracked edits synced into the `.tex`.

**His to clear first** --- AW has replied and is waiting on him:
`[132]` is the ELAJ frontier "characteristics"? · `[467]` what is a
single-nucleus study · `[507]` define "corpus".

- [ ] **`[65]` and `[83]`: the Introduction needs rewriting.** The larger of
      the two. *"This entire section need re written. What other people have
      done in single cell aspects."* He wants a proper related-work
      treatment of single-cell endometriosis work, which the paper currently
      compresses into one sentence of ¶4. `INTRODUCTION_STRUCTURE.md` ¶4 has
      the plan and `Thesis/literature-evidence.md` has the evidence keyed.
- [ ] **`[97]`: rephrase** the "questions that make a pooled corpus worth
      assembling" paragraph.
- [ ] **`[42]`: avoid the abbreviation in the abstract.** Anchored on
      `, ELAJ,`. Either expand on first use or drop the name from the
      abstract.
- [ ] **`[82]`: trials or studies?** "While some clinical trials are still
      ongoing" --- check which it is before answering.
- [ ] **`[503]` and `[511]`:** "A candidate dataset --- record or query?" and
      "The last constraint --- what was the constraint, and which one is
      last?" Both in *Data collection*.

## To be discussed in person, not over comments

AW's call, 8 November. Both are SYNCED INTO THE TEX AS HE MADE THEM; these
are the exact words to put back if the conversation goes that way.

- [ ] **The opening line of the Introduction, cut.** "Pain is a recurring
      date on a calendar for 190 million people worldwide
      (`who2025endometriosis`)." It was the hook the Introduction was built
      on and the sentence the abstract's own opening answers to. Its
      citation is now unused.
- [ ] **The human-health paragraph, cut.** "A subtle but deliberate choice
      in this study is to treat this disease as a human health problem
      rather than a gendered disease. At a scale of hundreds of millions of
      patients, we believe this to be necessary to bring attention to this
      problem." A stated position, and the one place the paper explains a
      convention it follows throughout.

## Display items

- [ ] **Figure 1 panels a and b.** AW will supply his own flowcharts for the
      architecture and PRISMA. The current versions are minimum viable.
      Residual: three method labels crowd in panel c.
- [ ] **Supplementary Figure 1, the ablation UMAPs.** One horizontal figure,
      study-mixing UMAPs for ELAJ$_{B\,hi}$ and all five ablation arms.
      Sources on disk at
      `Outputs/{p_series,a_series}/*/figures/best/latent_umap_epoch*.png`;
      redraw from the latents rather than crop. What it shows: study
      territory grows base 0.7613 < -sentinel 0.7818 < -ECS 0.8340, and both
      ablations develop single-study regions the reported arm does not have.
- [ ] **Extended Data.** Ten slots, none built. Priority order is in
      `06-display-items.tex`.

## References

- [ ] **Two preprint citations for core infrastructure.** `vasilevsky2022mondo`
      and `czi2023cellxgene` are both medRxiv/bioRxiv. Check for journal
      versions; two preprints for ontology and data-platform infrastructure
      is the kind of thing a reviewer notices.
- [ ] **Six references cited zero times**, harmless but they will not appear:
      `gbd2019asthma`, `idf2021diabetes`, `nhs2024noncoding`,
      `rands2014constrained`, `ballard2006delay`, `li2025factors`. The last
      two were planned for the Introduction's delay material and would come
      back with the `[65]`/`[83]` rewrite. `who2025endometriosis` joined them
      when the opening line was cut.
- [ ] **Cite duempelmann\_2026 on `[4]`'s rASRM I--II / III--IV sentence**, so
      the definition is visibly theirs rather than ours.

## Externals, and AW owns all of these

- [ ] Repository URL, licence and a Zenodo DOI. Methods claims predictions
      were registered before training, which is only checkable if the repo
      is public.
- [ ] Funding and grant numbers for Acknowledgements.
- [ ] Final author list, if it is more than the two.
- [ ] **Reporting Summary.** Adobe Reader form, required at submission.
- [ ] **Cover letter.** The IDAI answers carry the framing.
- [ ] bioRxiv preprint, which AW wants alongside the NMI submission.

## Smaller, and none of it blocking

- [ ] **Extend both auditors to Methods.** Results and the Discussion are
      covered; Methods is not. Mostly accessions and configuration.
- [ ] **Abstract against the 150-word limit.** It is 160 after the
      supervisor's edits.
- [ ] **One skipped test** in the suite of 1,945, unnamed because the run did
      not use `-rs`. Not worth a card unless it matters at submission.
