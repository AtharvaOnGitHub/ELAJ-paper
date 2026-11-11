# Claims ledger

Endometriosis claims from the ten corpus papers, and whether our scale can
settle them. Source PDFs extracted to `Endo research/My paper/Final 10/_txt/`.

**How to read it.** `test?` is can-and-should. `done` is what we have already
measured. `how` names the method; full protocols are in `EXPERIMENTS.md`
under the `X` numbers. `AW` is AW's comment, with a yes/no in brackets.

**Renumbered since the first pass.** Old D2 is now D5, old D3 is now D4.
Non-disease claims were dropped; they are listed at the foot.

---

## Dümpelmann 2026 — `duempelmann_2026` · 60 donors, 25 control / 35 eutopic

| ID | claim | test? | done | how | AW |
|---|---|---|---|---|---|
| D1 | Eutopic endometrium of cases is transcriptionally altered. 427 DEGs; inflammation, adhesion, proliferation, survival, angiogenesis, nervous system. Macrophage-centred ligand-receptor changes. Measured in the proliferative phase only | yes, content only | **existence answered**: disease status 0.3364, p=0.005, 108 control vs 99 eutopic donor records | cell-family and pathway resolution on the same contrast — X8, X10 | "Haven't we already verified this claim through severity?" (partly: via disease status, not severity) |
| D2 | Severity is a dose, not a switch. Severe-ENDO has **5× the DEGs** of mild-ENDO | yes | **measured**: merged severity 0.1286, p=0.025 at 118 donors; mild vs severe 0.0744, p=0.129 at 57 | write the existing numbers against their gradient — X4 | |
| D3 | Composition barely changes. Stratified by phase, the **only** notable case-control abundance difference is a 1.6× rise in secretory mural cells, adj p=0.026 | yes | no | transferred labels, composition per donor, case vs control — X8 | |
| D4 | Bulk at n>200, phase-stratified, found **no** case-control expression difference | no — not our data | no | — | "Is this about control vs disease?" (yes) |
| D5 | 11-gene supervised model predicts severity, median AUC 0.83, not externally validated | no — different object | no | the inverse is worth doing instead — X12 | "Severity claim has been countered, right?... maybe we could do the opposite exercise and find the genes most relevant to classifying control vs endo?" (not countered, it is a dissociation; the inverse is X12) |

## Marečková 2024 (HECA) — `marecko_2024` · 58 donors, 36 control / 22 eutopic

| ID | claim | test? | done | how | AW |
|---|---|---|---|---|---|
| M1 | Decidualised stromal cells and macrophages are the cell types most likely dysregulated in endometriosis. Derived by integrating the atlas with the largest endometriosis GWAS | yes | **partly**: immune-family case-control displacement 0.7732 and 0.8321 in Marečková's own cells, highest of four families in both arms; does **not** replicate in Dümpelmann | extend displacement-by-family to all studies once labels transfer — X6 | "This needs to be tested, right? This seems like the thing an atlas would do" (yes) |
| M2 | Prior atlases lack reproducible marker gene signatures, consensus annotation, and even cycle coverage | yes, the marker half | no | cross-study reproducibility of per-family signatures — X13 | "can we say something about 'marker genes' now that we have scale?" (yes, X13) |

## Fonseca 2023 — `fonseca_2023` · 48 donors, 4 control / 35 ectopic / 9 eutopic

| ID | claim | test? | done | how | AW |
|---|---|---|---|---|---|
| F1 | The same cell type is transcriptionally different depending on which tissue it sits in. Endometrial-type epithelium and stroma differ across endometrioma, lesion, eutopic endometrium, unaffected ovary and clean peritoneum. Read as cellular restructuring and transcriptional reprogramming, not relocation | yes, **with care** | no | ⚠ tissue is a decoder covariate, so a naive test is circular. Must ask whether tissue separates *within* a transferred cell label after study is accounted for — X14 | "What exactly is this claim? This needs to be understood and then tested" |
| F2 | Endometriomas show dysregulated pro-inflammatory pathways and upregulated complement, across epithelium, stroma and proximal mesothelium | yes, if the groups reach complement | no | pathway-group activity, endometrioma donors vs others — X11 | |
| F3 | Somatic ARID1A mutation in epithelial cells drives pro-angiogenic and pro-lymphangiogenic factors and lymphatic endothelial enrichment | no — no mutation calls in the corpus | no | — | |
| F4 | Ciliated epithelial signatures are enriched in ovarian cancers | no — no cancer data | no | — | |

## Tan 2022 — `tan_2022` · 31 donors, 3 control / 19 ectopic / 9 eutopic

| ID | claim | test? | done | how | AW |
|---|---|---|---|---|---|
| T1 | A perivascular mural cell population specific to peritoneal lesions, with dual roles in promoting angiogenesis and trafficking immune cells | yes | no | transferred labels; perivascular abundance and separation, lesion vs eutopic, 58 ectopic donors — X6 | |
| T2 | An immunotolerant peritoneal niche: immunomodulatory macrophages, immunotolerant dendritic cells, tertiary lymphoid structures in some lesions | maybe | no | needs immune subtypes finer than our four families; depends on what transfer recovers — X6 | |
| T3 | A previously unreported progenitor-like epithelial cell subpopulation | yes | no | transferred labels; progenitor-like epithelium in lesion vs eutopic — X7 | |
| T4 | Fundamental differences in eutopic endometrium between cases and controls | yes | **answered**: same number as D1 | — | |

⚠ Most Tan participants were on hormonal treatment, the variable Dümpelmann
excluded by design. Any contrast spanning both inherits the inconsistency.

## Sarsenova 2024 — `ferrero_2024` · 8 donors, 4 ectopic / 4 eutopic, paired

| ID | claim | test? | done | how | AW |
|---|---|---|---|---|---|
| S1 | Lesions are metabolically reprogrammed relative to paired eutopic endometrium. Concentrated in perivascular, stromal and endothelial cells; largest in AMPK signalling, HIF-1 signalling, glutathione metabolism, oxidative phosphorylation, glycolysis | yes | no | pathway-group activity, 58 ectopic vs 99 eutopic donor records — X11 | |
| S2 | Composition differs between lesion and eutopic tissue: perivascular, endothelial and immune larger in lesions, stromal larger in eutopic | yes | no | transferred labels, composition per donor by tissue — X9 | |
| S3 | Metabolic activity is the **same** in eutopic endometrium of cases and controls. ⚠ Measured on an **external dataset**, N=3 vs N=3, proliferative phase, metabolism and steroidogenesis only | yes — and it contradicts D1 | no | pathway-group activity restricted to metabolic groups, 108 control vs 99 eutopic — X10 | |
| S4 | Progesterone resistance and elevated estradiol signalling in lesions; steroidogenic genes lower in ectopic tissue | yes, if the groups reach steroid signalling | no | X11 | |

## Huang 2023 — `lin_2023` · 13 donors, 7 control / 6 eutopic, stage I–II only

| ID | claim | test? | done | how | AW |
|---|---|---|---|---|---|
| H1 | **The cycle variation of immune composition is absent in endometriosis.** In controls, immune cells fall in the secretory phase and total immune, NK and T cells all vary across the cycle; in endometriosis that variation disappears | yes | no | cross-donor cycle agreement split by disease status; our own headline instrument — X3 | |
| H2 | A PAEP+ CXCL14+ epithelial population present in controls is absent in cases at the window of implantation; secretory-phase epithelial cells reduced overall | maybe | no | needs a transferred epithelial label **and** a phase call; Huang supplied neither — X7 + X3 | |
| H3 | Immune cells secrete more IL-10 in the secretory phase in controls and the reverse in endometriosis; pro-inflammatory cytokines higher throughout | maybe | no | gene-level, and a second instance of H1's pattern — X12 | |
| H4 | Findings are specific to minimal and mild disease, rASRM stage I–II | yes | **bears on D2**: if distance from control grows with severity, a stage I–II cohort finding strong immune differences is informative | read alongside X4 | |

## Shih 2022 — `shih_2022` · 11 donors, all eutopic, menstrual effluent

| ID | claim | test? | done | how | AW |
|---|---|---|---|---|---|
| Sh1 | A proliferating uNK subcluster present in controls is almost absent in cases; total uNK reduced, p < 10⁻¹⁶ | **no — blocked** | no | our copy of the cohort has no controls and no symptomatic-undiagnosed arm. Cross-study only, which is a weaker object | |
| Sh2 | IGFBP1+ decidualised stromal cells abundant in controls relative to cases, p < 10⁻¹⁶ | **no — blocked** | no | same | |
| Sh3 | Case stromal cells enriched for pro-inflammatory and senescent phenotypes | **no — blocked** | no | same | |
| Sh4 | B cells enriched in cases, p = 5.8 × 10⁻⁶ | **no — blocked** | no | same | |

⚠ Sh1 and Sh2 are the largest effect sizes claimed anywhere in the corpus,
and we cannot test either. Worth stating in the paper, with the reason.

## Chen 2022 — `wang_2022` · 4 donors, adenomyosis, myometrium

| ID | claim | test? | done | how | AW |
|---|---|---|---|---|---|
| C1 | SFRP4+ IGFBP5-high NKT cells drive differentiation of multipotent stem cells into neural-like cells and cause pain. NEFM tracks pain duration, IGFBP5 tracks pain score | **no — blocked** | no | pain is not a covariate anywhere in the corpus; sequencing is n=2 per group | |

## Li 2025 — `li_2025` · 6 donors, follicular fluid recorded as endometrium

| ID | claim | test? | done | how | AW |
|---|---|---|---|---|---|
| L1 | Iron overload drives senescence and metabolic reprogramming in pre-ovulatory follicular fluid in ovarian endometriosis | maybe, low value | no | pathway groups on 6 donors — X11 | |
| L2 | The disease affects tissue containing no lesions | no — already a Methods argument | no | — | |

⚠ Tissue label is wrong in the data: follicular fluid recorded as
endometrium, corrected in the paper only. Any test touching `li_2025`
compares follicular fluid to endometrium while calling both endometrium.

## García-Alonso 2021 — `garcia_alonso_2021_a` / `_b` · 15 people, 30 IDs, all control

| ID | claim | test? | done | how | AW |
|---|---|---|---|---|---|
| G1 | Lesions have a **less differentiated epithelial phenotype** than normal endometrium, enriched for the SOX9+ LGR5+ progenitor signature. WNT7A and KRT17 at proliferative-endometrium levels; secretory (PAEP, SCGB2A2) and ciliated (PIFO, TP73) markers at clean-peritoneum levels. ⚠ Inferred by **deconvoluting bulk microarray**, no lesion single cells | yes — and it would be the first direct test | no | transferred labels on 58 ectopic donors — X7 | |
| G2 | WNT and NOTCH control secretory and ciliated epithelial commitment | no — normal physiology, not a disease claim | no | retained because both pathways recur in D1 | |

---

## Dropped from this pass

Not claims about endometriosis. Kept here so every paper stays accounted for.

| paper | non-disease contribution |
|---|---|
| Marečková | scale comparator (7 datasets, 313,527 cells, 63 donors); consensus cell-type definitions |
| Fonseca | the five-tissue design; composition breakdown of 370,000 cells |
| Tan | organoid benchmarking; imaging mass cytometry |
| Dümpelmann | cycle-staging reference; 57 annotated cell types |
| García-Alonso | normal endometrial reference; epithelial differentiation across the cycle; spatial maps |
| Shih | menstrual effluent as a non-surgical sampling route |
| Huang | endometrial leukocyte reference across the cycle |
| Chen | the only myometrium and the only adenomyosis in the corpus |
| Li | the only non-uterine site |
| Sarsenova | the only paired within-donor design in the corpus |
