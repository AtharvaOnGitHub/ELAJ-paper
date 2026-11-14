# Priority list

**The goal: ELAJ at an NMI reviewer's desk, in the strongest honest shape.**
Rewritten 14 November against actual state, because the previous version was
stale on four counts: it had the Discussion pending, the subheading question
unresolved, the supplementary as "nothing exists", and two of the four
moved-from-Results items listed as safe when one had been lost.

## The line everything now serves

> In this paper we build a single-cell disease atlas where inductive bias
> replaces pretraining scale, and use that to measure the trade-off between
> removing batch effects and keeping biology on a corpus limited by donors.

A **case study**, deliberately, licensed by `hrovatin2025atlases` saying no
one-size-fits-all atlas protocol exists. CONTINUITY has the four rejected
framings. `REGISTER.md` is the contract for Results prose;
`DISCUSSION_REGISTER.md` for the Discussion, built by reading eight published
Discussions rather than from our own notes.

---

# Where the paper is, 14 November

| section | state |
|---|---|
| Abstract | **stale. Full rewrite.** Must now carry the claims axis |
| Introduction | **stale. Full rewrite** to the supervisor's spine |
| Results | **drafted, 1,650 words, shipped 13 Nov.** WITH THE SUPERVISOR UNTIL MONDAY |
| Discussion | **written, 838 words, 10 paragraphs, shipped 14 Nov** |
| Methods | done, 5,745 words, tweaks only |
| Supplementary | **in progress.** Data done, scIB done, 9 UMAP caches in, 3 jobs running |
| Extended Data | one item, PRISMA. Nine slots open |

**Nothing in Results may be rewritten before his Monday comments arrive**, or
they will land on a version that no longer exists.

**The Discussion subheading question is SETTLED and was never a blocker.**
Eight of eight comparators have none, IBDex included; his four sections are
carried by a topic-sentence ladder. Do not reopen it.

---

# 1. In flight on the HPC

| job | what it unblocks | wall | state |
|---|---|---|---|
| `umap_cache.sh` | every supplementary figure showing a latent | 3 h array | **DONE**, 9 caches at `Outputs/supplementary/umaps_supplementary/` |
| `probe_stages.sh` to `p1_groups` | **X15**, which pathway groups carry which signal | 16 h GPU | running |
| `marker_reproducibility.sh` | **X13**, cross-study marker reproducibility | 8 h CPU | running |
| `scib_scfoundation.sh` | one quarantined cell in the scIB scorecard | 6 h CPU | running |

**On the UMAP caches**: the job ran before the index pin was committed, so it
took the RNG path. That is fine, because HPC numpy 1.26.4 and local 2.2.6 were
checked to produce the identical draw (checksum 315692720845). The pin protects
future runs; it did not make these ones correct.

**X15 is already at its sensible operating point.** `--no-references` removes
what the flag's own help calls two thirds of the cost. The residue is a
brute-force cross-donor search, quadratic in cells. The only further safe lever
is `--permutations`. **Do not cut `--splits`**: the latent row must reproduce
the benchmark's elaj row, and that only holds on val+test.

**If `scib_scfoundation` dies on memory again**, the next move is subsampling
the silhouette and reporting the cell count it was computed on, not more
memory. 360 G was already chosen because 240 G is what failed.

---

# 2. Ready to go now. No dependencies, no compute.

Ordered by what I would do first.

1. **The frontier and ablation UMAP figures.** The nine caches just landed, so
   these draw locally in seconds per arm. The newly unblocked item, and it
   closes the biggest hole in the supplementary. Covers `FIGURES_NEEDED.md`
   F4 and F5, and feeds Supplementary Notes N4 and N5.
2. **Note N1, gene-group sizing.** `Thesis/appendices/D-gene-grouping.tex` is
   2,525 words over eight sections; `C-sizing.tex` is 1,238. Trimming and
   re-registering numbers, not writing.
3. **Note N3, the limitations at length.** AW: *"Pour your heart out with all
   the limitations and clawing that you can. Here it makes sense because this
   section is when the reader has gone through the paper and understood the
   good side."* The Discussion's `Supplementary Note~X` resolves to this.
4. **Loss plots for all eleven arms.** `metrics.csv` is local for every arm
   with the full per-epoch breakdown. Feeds N4 and N5.
5. **Supplementary Tables.** The nine claims CSVs plus the benchmark files. A
   table belongs here only if it survives being separated from an argument;
   one that only means something inside a Note stays in that Note.
6. **The pseudocode box.** `docs/walkthrough/06` to `08`, reformatted.
7. **Figure 1's legend.** It describes five panels; there are four, and panel a
   has never been described at all.
8. **The Abstract.** No compute dependency and no blocker. AW's 11 November
   ruling puts it before the Introduction.

---

# 3. Blocked, and on what

| item | waits on |
|---|---|
| Note N2, scIB in detail | the scorecard is **built**; one cell waits on `scib_scfoundation` |
| Note on X13 | the X13 job |
| Note on X15 | the X15 job |
| **Source Data** | the figures being final. Sheets are named per panel, so it cannot be written before the panels exist |
| Supplementary Table captions and numbering | the Notes, per the rule above |
| **References, whole paper** | the deferred citation pass below |
| Reporting Summary | pre-submission. AW's, and last |
| Results edits | **his Monday comments** |
| Introduction | nothing technical, but cheapest once the Abstract exists |

---

# 4. Decisions waiting on AW

1. **Is the rho = +0.721 asymmetry cut on purpose?** It left Results for the
   Discussion, then left the Discussion when the metrics paragraph was cut, so
   **it is now nowhere in the paper.** It was importance 9 in the inventory and
   its job was to explain why our cycle advantage cannot be identity leaking
   through. Restore in a clause, move to a Note, or drop deliberately.
2. **F2 and F3: one figure or two?** Two main-text additions take the paper to
   NMI's six-item cap exactly. One two-panel figure keeps it at five and pairs
   the mechanism with its consequence. Undecided.
3. **Figure 2's redesign**, which AW wants discussed before any drawing. It
   competes with the supplementary figures for the same effort.
4. **The dissociation panel's home**, Figure 3 or Extended Data. It surfaces a
   number the paper does not carry: whole-corpus surgical stage $+$0.3320 at
   $p=0.005$ over 58 donors, against the held-out 0.1313 at $p=0.303$. Either
   it goes into Results or the row comes out of the panel.

---

# The display items, settled 11 November

**Four, and the order is the argument's order.** AW overruled the supervisor's
"fig 4 becomes fig 2": the model has no credibility on the UMAPs until the
frontier has been explained.

| | what it is | change |
|---|---|---|
| Fig 1 | graphical abstract, architecture, frontier, cell-family latent | none |
| Fig 2 | **the frontier** | stays, but **must stop looking like a benchmark** |
| Fig 3 | **the nine endometriosis UMAPs** | was Fig 4, renumbered |
| Table 1 | every arm | none |
| --- | both latents by family and phase | **was Fig 3, goes to Supplementary** |

- [ ] **The renumbering.** `figure4.py` becomes Figure 3. Script names match
      paper numbers, so this renames files, captions, every `\ref`, and both
      auditors' pins.
- [ ] **Every panel referenced in prose.** Figures 2, 3 and 4 still have panels
      no sentence points at.
- [x] Figure 1 panel c's clipped x-label. An assert now fails the render.
- [ ] Figure 1 is 213.5 mm tall. It fits, but it is close to a full page.

**The figure register is in `FIGURES_NEEDED.md` and is not re-derivable
cheaply:** Arial throughout, 180 mm maximum width, panel letters 10 pt bold,
titles 6.5 pt, body 5.5 pt, nothing below NMI's 5 pt floor once placed.
Okabe-Ito for cell families, eleven study hues with the yellow-olive-brown band
removed. **Size the layout to fit the type, never the type to fit the layout.**

---

# Citations, a whole-paper pass

- [ ] **CITATIONS IN THE SUPERVISOR'S FILE ARE DEFERRED, AW's ruling,
      14 November.** *"We have citations in the right place in our local tex
      files. We will both add all references in the correct and edit the file
      to add citations in the correct place. You'll just have to give me
      pointed changes then."* So it is **one later pass over his whole file**,
      delivered as **pointed find-and-replace changes naming each location and
      its number**, never another wholesale paste. Until then his Results has
      no citations at all, because pandoc dropped every `\citep` from the
      13 Nov batch, and his Discussion carries author-year brackets.
      `sections/*.tex` is the authority on placement.
- [ ] **The paper is under-cited throughout**, AW's own observation. The
      Discussion now cites 18 unique references, up from one. The Introduction,
      Results and Methods have not had that review.
- [ ] **`Supplementary Note~X`** is referenced from the Discussion's
      limitations paragraph and must resolve: overlapping donor identifiers,
      the single cycle-day cohort, the unstratified permutation null.
- [ ] **Two bib entries are incomplete.** `kedzierska2025zeroshot` has no
      pages; `duempelmann2026endometrium` has neither volume nor pages.

---

# Mechanical, none of it blocking

- [ ] Numbered references in the DOCX. `make_draft.sh` is wired for
      `assets/nature.csl` and AW is fetching it.
- [ ] Reference format per NMI: sequential across main text, Methods and Data
      availability; article titles required; URLs parenthetical.
- [ ] Extend both auditors to Methods.
- [ ] `vasilevsky2022mondo` and `czi2023cellxgene` are preprints; check for
      journal versions.
- [ ] Six references cited zero times.
- [ ] One unnamed skipped test in the suite of 1,945.
- [ ] `probe_stages.sh`'s preflight prints no numpy version, which is why the
      index-draw check had to be run by hand. Add it when next touched.
- [ ] **Run documentation in the GitHub repository**, the supervisor's third
      batch. The scripts are committed; what does not exist is a page saying
      how to run them. Bears on Code availability.

---

# The handover workflow

1. change the `.tex`
2. build the Word file
3. hand AW the changeset; he applies it in the guide's OneDrive copy

**Shipped:** `ELAJ_results_2026-11-13.docx` and
`ELAJ_discussion_2026-11-14.docx`, both wholesale replacements, both maths-free
so character formatting survives the paste. Batch 2026-11-10 is with AW and not
confirmed applied; Figure 1 has changed since, so the next batch must carry the
new image and legend.

**Supplementary Data for OneDrive is built and sent:**
`Outputs/supplementary/send/ELAJ_Supplementary_Data.xlsx` (D1, D2, D3, D5 as
four sheets) plus `D4_transferred_cell_family_labels.csv.gz` separately,
because 1,577,728 rows exceeds the xlsx cap of 1,048,576.

# The supervisor's comments still ours

`[97]` rephrase the pooled-corpus paragraph, `[42]` the abstract abbreviation,
`[82]` trials or studies, `[503]` and `[511]` in *Data collection*. Most are
absorbed by the Introduction and Abstract rewrites.

**His to clear**: `[132]`, `[467]`, `[507]`.

**To discuss in person**, both synced into the tex as he made them: the "pain is
a recurring date on a calendar" opening, and the human-health paragraph.

**Third batch, 14 November**: run documentation in GitHub; supplementary filled
to the brim; Results reviewed Monday. Verbatim in `REVIEW_FEEDBACK.md`.

# Externals, AW owns all of these

Repository URL, licence, Zenodo DOI, funding and grant numbers, final author
list, Reporting Summary, cover letter, bioRxiv preprint.
