# The claims axis — second pass, endometriosis claims only

Rewritten 11 November 2026 after AW rejected the first pass:

> "Some of these are not claims about endo. The idea was to get the claims
> about the disease together as 'work done on endo in scRNA' and then see if
> the claims hold water at our scale."

**What changed.** The first pass was built from `Thesis/literature-evidence.md`,
which is an extraction made for a literature review: it collects whatever
positions the field, including methodological statements, scale comparisons
and corpus descriptions. Half of what it yielded was not a claim about
endometriosis at all. This pass goes back to the papers.

**All ten PDFs are now extracted** to
`Endo research/My paper/Final 10/_txt/`. Two files in that folder are not
corpus studies and have been set aside: `GSE174399` is Zheng 2022 on early
pregnancy loss, and the second `GSE213216` file is Pei et al. reanalysing
Fonseca's data. **The García-Alonso gap from the first pass is closed** — the
paper was on disk the whole time.

**One section per paper, claims explained rather than labelled**, per AW's
note that the complex ones need laying out.

---

# Answers to AW's ten comments on the first pass

**D1, have we already verified this through severity?** Partly, and the part
we have is the important half. Our `disease_status` cross-donor agreement is
**0.3364 at p = 0.005**, measured on 108 control and 99 eutopic donor records.
That is D1's *existence* claim: the eutopic endometrium of a case is
distinguishable from a control's. What it does not give is D1's *content* —
which pathways, which cell types, which direction. Severity is a separate
variable and a separate result; it does not stand in for this one.

**D2, has the severity claim been countered?** No, and this is worth getting
exactly right because the distinction is one we have already fought over.
We never said severity is not biologically relevant. What we found is a
**dissociation**: merged severity clears its null at 118 donors
(**0.1286, p = 0.025**), while mild against severe among patients only does
not (**0.0744, p = 0.129 at 57 donors**). The model can say whether a person
has endometriosis and cannot say how severe a surgeon judged it.

Dümpelmann's severity claim is also a different *kind* of object from ours.
Theirs is supervised prediction of a label the model was given; ours is
unsupervised representation tested against a label the model never saw.
Their AUC and our p-value do not compete.

**Your inverse proposal is the better experiment, and I would take it over
testing their eleven genes.** Deriving the genes that most distinguish
control from case across 254 donors is a result we would own, rather than a
replication of someone else's. It is listed below as **N1**. One caveat to
settle first: the model gives 44 gene *groups*, not per-gene importances, so
a gene-level answer needs either decoder attribution or a straight
differential-expression pass over the corpus. Those are different costs and
different claims.

**D3, is it about control versus disease?** Yes. Bulk RNA sequencing, over
200 donors, stratified by cycle phase, comparing eutopic endometrium of
people with and without endometriosis, finding **no significant expression
differences**. Single-cell at 60 donors found a great deal. The point is
resolution beating sample size, and it pre-empts "why not just use bulk".

**D4 and M1, quote and cite in the Introduction.** Agreed, and the second
pass found a better sentence than either. See *The licence*, below.

**M2, can we say something about marker genes now that we have scale?**
Possibly, and it is a real opportunity, but not cheaply. HECA's complaint is
that prior atlases lacked *reproducible* marker signatures. Reproducibility
across studies is exactly what our corpus can measure and no single cohort
can. The obstacle is that ELAJ does not emit marker genes: it has 44
Reactome/GO gene groups and a decoder. Listed as **N2** with its cost
stated.

**M3, does this need testing, and is it the thing an atlas would do?** Yes
to both, and the second pass makes it much stronger than I had it. See *The
two convergences*.

**M4 and F3, not claims about endometriosis.** Agreed, both dropped from the
ledger proper. Accounted for in the appendix.

**F1 and F2, what exactly is the claim?** Laid out in full under Fonseca
below. The short version is that the same cell type looks different
depending on which tissue it is sitting in, which is a claim about the
disease remodelling cells rather than merely relocating them.

---

# The licence, and it is better than what we had

HECA, in Nature Genetics, states our question as the field's open question
and asks for exactly the thing our corpus is:

> "Conflicting evidence exists about whether and to what extent the
> endometrium itself (that is, the eutopic endometrium) differs between
> those with and without endometriosis. Recently, single-cell studies,
> analyzing small sample sizes, reported dysregulation of the stromal and
> immune compartments in the endometrium of women with endometriosis to
> various degrees. **Larger sample sets are now needed to unpick whether and
> how the endometrium differs in those with and without endometriosis.**"

This is stronger than the "no one-size-fits-all protocol" sentence from
Hrovatin that currently licenses the framing, because it is specific to
endometriosis and it names a quantity rather than a practice. The field's
own reference atlas says larger sample sets are needed; we have 254 donors
and the measurement.

⚠ Note the sentence uses "women". Quoting it verbatim is reporting what the
source says, which is the open question from `INTRODUCTION_STRUCTURE.md`
that is still AW's to settle.

---

# The claims, by paper

## Dümpelmann 2026 — `duempelmann_2026`
*466,176 cells, 60 donors (25 control, 35 eutopic), endometrium*

### D1. The eutopic endometrium of cases is transcriptionally altered

427 differentially expressed genes between non-ENDO and ENDO, with
functional enrichment in **inflammation, cellular adhesion, cell
proliferation and survival, angiogenesis, and the nervous system**.
Ligand-receptor analysis adds enriched TGFβ, IL1, TNF, ICAM, VEGF and WNT
signalling, with macrophages central to the enhanced interactions.

**The design detail that matters to us**: they restricted the comparison to
the proliferative phase, because it is "relatively homogeneous". They
removed the cycle to see the disease. We model the cycle and keep it, which
is the paper's whole argument, so this is a contrast worth drawing
explicitly.

**Testable**: the existence half is already answered at 0.3364, p = 0.005.
The content half needs cell-family or pathway resolution.

### D2. Severity is a dose, not a switch

**Severe-ENDO showed a fivefold increase in DEGs over mild-ENDO.** This is
the claim to engage, not the AUC. It says the distance from control grows
with severity.

**Testable and interesting**, because it sits against our own dissociation.
We find merged severity clears and mild-against-severe does not. Dümpelmann
would predict a graded separation. Our result says the grading is not
recoverable at 57 donors in sixteen dimensions. **Either outcome is
publishable and neither embarrasses us.**

### D3. Composition barely changes, and that is the surprising part

Stratified by cycle phase, **the only notable cell-type abundance difference
between cases and controls was a 1.6-fold increase in secretory mural cells**
(Prv_VSMC secretory, adjusted p = 0.026). One cell type, out of 57.

**This is the most useful claim in the ledger and I under-read it the first
time.** It says you cannot find endometriosis by counting cell types. The
disease is in what cells are doing, not in how many of them there are. That
is a direct argument for a representation-level disease signal, which is
what we report.

**Testable** with transferred labels across 254 donors, and it converges with
two other studies. See below.

### D4. Bulk at n>200 found nothing

Quoted from their introduction, covered in the answer to AW's D3 above.
Introduction material, not a test.

### D5. An 11-gene supervised model reaches median AUC 0.83

Not externally validated, and the authors say so. Different object from our
measurement. Our engagement with it is **N1**, the inverse experiment.

---

## Marečková 2024, HECA — `marecko_2024`
*174,848 cells, 58 donors (36 control, 22 eutopic), endometrium*

### M1. Decidualised stromal cells and macrophages are the cell types most likely dysregulated in endometriosis

HECA's only disease claim, and it is an indirect one: they integrated the
atlas with the largest endometriosis GWAS meta-analysis and asked which cell
types express the genes the risk variants affect. The answer was macrophages
and subsets of decidualised stromal cells.

**Testable, and we are already half way there without having noticed.** Our
`disease_within_family.csv` gives case-versus-control displacement by cell
family per study: in Marečková's own cells the **immune** family carries the
largest displacement in both arms, 0.7732 and 0.8321, well clear of every
other family. In Dümpelmann's cells it does not replicate, and the leading
family is not even stable between arms.

So HECA's GWAS-derived prediction and our latent agree **in Marečková's own
donors and not in Dümpelmann's**. That non-replication is currently recorded
as audit item C5 and treated as a weakness. Read against M1 it becomes a
finding about where the signal lives, which is a far more interesting thing
to write.

### M2. The field lacks reproducible marker gene signatures

Their diagnosis of prior atlases, listed alongside few donors, uneven cycle
coverage and no consensus annotation. Addressed as **N2**.

⚠ The cycle-coverage half of that complaint lands on us too: phase labels
come from three of eleven keys. State it deliberately.

---

## Fonseca 2023 — `fonseca_2023`
*386,560 cells, 48 donors (4 control, 35 ectopic, 9 eutopic), five tissue sites*

### F1. The same cell type is transcriptionally different depending on which tissue it sits in

This is the claim AW asked me to pin down. Fonseca profiled endometrial-type
epithelium and stroma in five places: endometrioma, peritoneal lesion,
eutopic endometrium, unaffected ovary, endometriosis-free peritoneum. The
finding is that **the cellular and molecular signatures of those same cell
types differ across the sites**, which they read as "cellular restructuring
and transcriptional reprogramming".

**Why it matters**: a lesion is not displaced endometrium that happens to be
somewhere else. The cells are changed by where they are. This is the
citation already standing behind our decision to condition the decoder on
tissue.

⚠ **And that makes it partly circular for us.** Tissue is a decoder
covariate in ELAJ, so finding that tissue separates things in our
representation is close to finding what we built in. A clean test has to be
framed carefully, probably as whether tissue differences survive *within* a
transferred cell label after study is accounted for.

### F2. Endometriomas show dysregulated pro-inflammatory pathways and upregulated complement

The specific content of F1 for the ovarian endometrioma subset, across
epithelium, stroma and proximal mesothelium.

**Testable at pathway level** if the 44 groups reach complement and
inflammatory signalling. Needs the vocabulary fetch.

### F3. Somatic ARID1A mutation remodels the endothelial compartment

Epithelial cells carrying somatic ARID1A mutations upregulate pro-angiogenic
and pro-lymphangiogenic factors, with enrichment of lymphatic endothelial
cells.

**Not testable.** We have no mutation calls, and nothing in the corpus
carries them.

### F4. Ciliated epithelial signatures are enriched in ovarian cancers

Supports the epidemiological endometriosis-to-ovarian-cancer link.
**Not testable**, no cancer data in the corpus.

---

## Tan 2022 — `tan_2022`
*114,944 cells, 31 donors (3 control, 19 ectopic, 9 eutopic), three tissue sites*

### T1. A perivascular mural cell population specific to peritoneal lesions

Described as previously unreported, with a dual role in promoting
angiogenesis and trafficking immune cells.

### T2. An immunotolerant peritoneal niche

Immunomodulatory macrophages and immunotolerant dendritic cells specific to
the lesion microenvironment, plus tertiary lymphoid structures in some
lesions. The framing is a coordinated transcriptional programme driving
immunotolerance and angiogenesis across both eutopic and ectopic tissue.

### T3. A progenitor-like epithelial cell subpopulation

Previously unreported, and it recurs in García-Alonso. See the convergences.

### T4. Fundamental differences in eutopic endometrium between cases and controls

Their own phrasing. Same claim as D1, from a cohort of 14 with 3 controls.

⚠ **The caveat Tan volunteers and we must carry**: most of their
participants were on hormonal treatment, which is exactly the variable
Dümpelmann excluded by design. Pooling inherits the inconsistency.

---

## Sarsenova 2024 — `ferrero_2024`
*15,872 cells, 8 donors (4 ectopic, 4 eutopic, paired), endometrium and peritoneum*

### S1. Lesions are metabolically reprogrammed relative to paired eutopic endometrium

Twelve metabolic pathways examined across nine cell types. Differences
concentrate in **perivascular, stromal and endothelial** cells, largest in
AMPK signalling, HIF-1 signalling, glutathione metabolism, oxidative
phosphorylation and glycolysis. They report co-activation of glycolytic and
oxidative metabolism in perivascular and stromal cells of lesions.

**The paired design is the cleanest control structure in the corpus**: both
samples from the same person, so the contrast cannot be donor variation.
**Testable at pathway level** across 58 ectopic donors, which is fourteen
times their four.

### S2. Composition differs between lesion and eutopic endometrium

Perivascular, endothelial and immune populations larger in lesions; stromal
larger in eutopic endometrium.

**Testable with transferred labels.** Note it sits against D3, which found
composition almost unchanged between *case and control eutopic* tissue.
Different contrast, so not a contradiction, but the pair is informative:
composition moves between tissues and barely moves between disease states.

### S3. Metabolic activity is the same in eutopic endometrium of cases and controls

**I got this wrong in the first pass and the correction matters.** I
described it as their own N=3 against N=3 comparison and called it the
strongest test available. In fact they had no controls at all: the
comparison uses an **external dataset**, at N=3 versus N=3, in the
proliferative phase, and it is restricted to **metabolic pathway activity
and steroidogenesis**, not expression in general. Their words: "virtually no
difference".

It is still a real disagreement with D1, and a sharper one than I had it,
because both are proliferative-phase comparisons of case against control
eutopic endometrium. Dümpelmann found 427 DEGs; Sarsenova found nothing in
metabolism on borrowed data at N=3.

**Testable**, and the test is the clean one: 108 control against 99 eutopic
donor records, restricted to metabolic groups.

### S4. Progesterone resistance and elevated estradiol signalling in lesions

Lower expression of steroidogenic genes in ectopic tissue.
**Testable at gene-group level** if the groups reach steroid signalling.

---

## Huang 2023 — `lin_2023`
*140,032 cells, 13 donors (7 control, 6 eutopic), endometrium, stage I–II only*

### H1. The endometrium's immune composition stops varying with the cycle in endometriosis

In controls, the proportion of immune cells falls in the secretory phase,
and total immune cells, NK cells and T cells all vary across the cycle. **In
endometriosis that cycle variation is absent.**

**This is the claim I would put at the top of the list.** It is not a claim
that the disease changes a quantity; it is a claim that the disease
**flattens the cycle itself**. Our paper exists to measure how much cycle
signal survives integration, and the cross-donor cycle agreement is the
number we already report. Asking whether that agreement differs between
control and eutopic donors uses our own headline instrument to test somebody
else's biological claim, at 254 donors instead of 13.

⚠ It is also the claim most exposed to our own confound. Phase is a
supervised head and a per-donor constant, so any disease-by-phase
interaction has to be measured with that in mind, and it is one of the few
places the standing rule on per-study numbers could bite.

### H2. A PAEP+ CXCL14+ epithelial population present in controls is absent in cases

Specifically during the window of implantation, in the secretory phase.
Trajectory analysis adds that secretory-phase epithelial cells are reduced
in endometriosis overall.

**Testable with transferred labels plus a phase call**, which is demanding:
this study supplied neither.

### H3. Immune cells in endometriosis are more inflammatory and lose the IL-10 switch

Controls secrete more IL-10 in the secretory phase than the proliferative;
endometriosis shows the opposite. Pro-inflammatory cytokine levels are
higher in endometriosis throughout.

**Gene-level**, and the IL-10 direction reversal is a second instance of the
H1 pattern: not a level shift but a loss of cycle-dependence.

### H4. Findings are specific to minimal and mild disease

Their cohort is rASRM stage I–II. Reads against D2's dose-response: if the
distance from control grows with severity, a stage I–II cohort finding
strong immune differences is informative.

---

## Shih 2022 — `shih_2022`
*74,496 cells, 11 donors, all eutopic, endometrium from menstrual effluent*

### Sh1. Uterine NK cells are strikingly reduced in cases

A proliferating uNK subcluster present in controls is almost absent in
cases, and total uNK is reduced at **p < 10⁻¹⁶**.

### Sh2. IGFBP1+ decidualised stromal cells are abundant in controls relative to cases

Also at **p < 10⁻¹⁶**, and read by the authors as confirming compromised
decidualisation.

### Sh3. Stromal cells from cases are enriched for pro-inflammatory and senescent phenotypes

### Sh4. B cells are enriched in cases, p = 5.8 × 10⁻⁶

Raising the possibility of chronic endometritis in some cases.

⚠ **All four are blocked in their own cohort.** The corpus holds 11 Shih
donors, all eutopic. The controls and the thirteen symptomatic-undiagnosed
subjects are not here, and every one of these claims is a case-versus-control
contrast. They can only be tested against controls from other studies, which
is a cross-study contrast and a weaker object.

**Sh1 and Sh2 are the largest effect sizes claimed anywhere in the corpus**,
so it is worth saying plainly in the paper that we could not test them and
why.

---

## Chen 2022 — `wang_2022`
*49,152 cells, 4 donors, adenomyosis, myometrium*

### C1. SFRP4+ IGFBP5-high NKT cells drive neural-like differentiation and pain

IGFBP5-high NKT cells promote differentiation of multipotent stem cells into
neural-like cells; NEFM expression correlates with pain duration and IGFBP5
with pain score.

⚠ **Blocked, and permanently.** Pain is not a covariate anywhere in the
corpus, the sequencing is n=2 per group, and this is the only myometrium we
hold. Chen's role is to supply a contrasting related disease, which is why
adenomyosis is a fourth disease status.

**Accounted for, contributes no testable claim.**

---

## Li 2025 — `li_2025`
*45,312 cells, 6 donors, follicular fluid recorded as endometrium*

### L1. Iron overload drives senescence and metabolic reprogramming in follicular fluid in ovarian endometriosis

A single-cell atlas of pre-ovulatory follicular fluid showing iron
metabolism changes and iron-induced senescence, supported by spatial
transcriptomics in iron-overloaded mouse ovaries.

**Testable at pathway level only, on six donors**, and the value is limited.

⚠ **The tissue label is wrong in the data.** Follicular fluid recorded as
endometrium, corrected in the paper only, because tissue is a decoder
covariate and relabelling means retraining. Any test touching `li_2025`
compares follicular fluid against endometrium while calling both
endometrium.

### L2. The disease affects tissue containing no lesions

The reason the corpus spans anatomical sites. Already a Methods argument,
not a test.

---

## García-Alonso 2021 — `garcia_alonso_2021_a` and `_b`
*110,336 cells, 15 people under 30 identifiers, all control endometrium*

The gap from the first pass, now closed. Two CELLxGENE deposits from one
Nature Genetics paper; the third, organoid, deposit was excluded from the
corpus.

### G1. Endometriotic lesions have a less differentiated epithelial phenotype than normal endometrium

Specifically, lesions are enriched for the **SOX9+ LGR5+** progenitor-like
epithelial signature, with proliferative-endometrium markers such as WNT7A
and KRT17 at levels matching proliferative endometrium, while secretory
markers (PAEP, SCGB2A2) and ciliated markers (PIFO, TP73) stay at normal
peritoneum levels.

**The detail that makes this worth testing**: they had no lesion single-cell
data. The claim comes from **deconvoluting bulk microarray data** from
peritoneal biopsies using their atlas as a reference. We hold 58 ectopic
donors with actual single cells. Testing G1 is not a replication, it is the
first direct test of a claim that was only ever inferred.

### G2. WNT and NOTCH control secretory and ciliated epithelial commitment

Established in organoids by downregulating each pathway. A normal-physiology
claim, but it names two pathways that recur in Dümpelmann's disease
signalling, so it is worth carrying.

---

# The two convergences, and this is the atlas story

The single most useful thing to come out of reading the papers properly is
that **independent studies, with different designs, different tissues and
non-overlapping cohorts, keep landing on the same two things.** No one of
them can confirm another, because none of them shares a cell vocabulary or a
cohort. That is precisely what an atlas is for, and it is the direct answer
to AW's M3.

### Convergence 1: perivascular and mural cells

| study | finding | design |
|---|---|---|
| Dümpelmann | the **only** composition change between case and control is a 1.6-fold rise in secretory mural cells | 60 donors, eutopic vs control |
| Tan | a perivascular mural population **specific to peritoneal lesions** | 14 donors, lesion vs eutopic |
| Sarsenova | **perivascular** cells carry the largest metabolic reprogramming in lesions | 4 paired donors |

Three designs, three tissues, one cell type. None of them could test the
others. **We hold 254 donors across all three contrasts.**

### Convergence 2: lesions carry a less differentiated, progenitor-like epithelium

| study | finding | design |
|---|---|---|
| García-Alonso | lesions enriched for SOX9+ LGR5+ progenitor signature, less differentiated | **bulk deconvolution**, no lesion single cells |
| Tan | a previously unreported progenitor-like epithelial subpopulation | 14 donors, lesion single cells |

García-Alonso inferred it without lesion single-cell data and Tan saw it in
fourteen people. We have 58 ectopic donors.

**A third, weaker thread** worth noting: immune dysregulation is claimed by
HECA (macrophages, from GWAS), Huang (loss of cycle variation), Shih (uNK
collapse) and Dümpelmann (macrophage-centred ligand-receptor changes). Four
studies, four different immune claims, no shared vocabulary. HECA's own "to
various degrees" is about this.

---

# What we can already answer today

Worth separating, because these need no new compute at all.

| claim | our number | reading |
|---|---|---|
| D1, T4, and HECA's open question | `disease_status` **0.3364, p = 0.005**, 108 control vs 99 eutopic donor records | the eutopic endometrium of a case is distinguishable. The existence question the field called open |
| D2's dose-response | merged severity **0.1286, p = 0.025**; mild vs severe **0.0744, p = 0.129** at 57 donors | a dissociation, not a null |
| M1, macrophages and stromal cells | immune family displacement **0.7732 / 0.8321** in Marečková, not replicated in Dümpelmann | agrees with HECA's GWAS prediction in one cohort of two |

---

# Triage for step 2, as a recommendation

**Tier A, no new machinery.** Numbers exist or need only a script over
existing latents and metadata.

1. **H1** — does cross-donor cycle agreement differ between control and
   eutopic donors? Uses our headline instrument on somebody else's biology.
2. **D2's dose-response** — already computed, needs writing up against
   Dümpelmann's fivefold claim rather than standing alone.
3. **M1** — already computed, needs reading against HECA's GWAS prediction.

**Tier B, needs label transfer.** kNN from the 118 annotated donors to the
other 136. One script, CPU, no retraining, and it unlocks everything below.

4. **Convergence 1, perivascular and mural cells** — three studies, one cell
   type, 254 donors. The strongest single test available to us.
5. **Convergence 2, progenitor-like epithelium in lesions** — 58 ectopic
   donors against a claim made by bulk deconvolution.
6. **D3** — is composition really almost unchanged between case and control?
7. **S2** — composition differences between lesion and eutopic tissue.

**Tier C, needs the gene groups.** Fetch `vocabulary_v1.json` first.

8. **S3 against D1** — metabolic pathway activity, case against control
   eutopic, 108 vs 99 donor records against their N=3 vs N=3.
9. **S1** — metabolic reprogramming in lesions, 58 ectopic donors against 4.

**Tier D, new work AW proposed.**

- **N1** — the inverse of D5: which genes most distinguish control from case
  across 254 donors. Needs a decision on decoder attribution versus a
  straight differential-expression pass.
- **N2** — reproducible marker signatures across studies, answering HECA's
  M2 complaint. The most expensive item and the most novel.

**Blocked, and worth stating in the paper**: Sh1 to Sh4 (controls absent
from our copy of the cohort), C1 (no pain covariate), F3 (no mutation
calls), F4 (no cancer data).

---

# Appendix: what each paper contributes that is not a disease claim

Kept because AW's condition is that every dataset is accounted for.

| study | non-disease contribution |
|---|---|
| Marečková | scale comparator: 7 datasets, 313,527 cells, 63 donors. Consensus cell-type definitions |
| Fonseca | the five-tissue design, and the composition breakdown of 370,000 cells |
| Tan | organoid benchmarking; imaging mass cytometry spatial validation |
| Dümpelmann | the cycle-staging reference and 57 annotated cell types |
| García-Alonso | the normal endometrial reference: epithelial differentiation across the cycle, WNT and NOTCH control, spatial maps |
| Shih | menstrual effluent as a non-surgical sampling route. The clinical hook |
| Huang | endometrial leukocyte reference across the cycle |
| Chen | the only myometrium and the only adenomyosis in the corpus |
| Li | the only non-uterine site; evidence the disease reaches tissue without lesions |
| Sarsenova | the only paired within-donor design in the corpus |
