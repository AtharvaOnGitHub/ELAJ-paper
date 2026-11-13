# What we tested, and what came out

Written 12 November 2026 for AW, plainly, with the jargon explained rather
than skipped. The ledger of published claims is `CLAIMS_LEDGER.md`; the
protocols and exact numbers are `EXPERIMENTS.md`. This file is the reading.

---

## The words, once

**Donor.** One person who gave a sample. Everything is counted in donors, not
cells, because all the labels we test (disease, severity, cycle phase) are
properties of a person and every cell from that person carries the same one.
Counting cells would make 60 people look like 600,000 independent
measurements, which they are not.

**Control / eutopic / ectopic.** Control is a person without endometriosis.
Eutopic is endometrium taken from inside the uterus of a person who *has*
endometriosis. Ectopic is the endometriosis tissue itself, growing somewhere
it should not be. Our main disease contrast is control against eutopic: can
you tell, from endometrium inside the uterus, whether this person has lesions
elsewhere.

**The latent, or "the 16 numbers".** Each cell arrives as about 15,500
measurements, one per gene. ELAJ compresses that to 16 numbers. Everything
the model knows about a cell is in those 16 numbers.

**Cell family.** Four broad categories of cell. *Stromal* is the structural
tissue. *Epithelial* is the lining and glands. *Endothelial* is the lining of
blood vessels. *Immune* is white blood cells of every kind.

**Composition.** What fraction of one person's cells belong to each family.
A headcount of cell types in a sample. **It is not about what is inside any
one cell.** Two samples can have identical composition while every cell in
one of them is behaving differently. X8 measures composition; X12 measures
what the cells are doing. They are the two halves of one statement.

**Cross-donor agreement.** For each cell, find the cells nearest to it in the
16-number space, ignoring every cell from the same person. Then ask what
fraction of those neighbours carry the same label. High means the model has
placed cells with the same label near each other *across different people*,
which is the only version that counts.

**Permutation null, and p.** We shuffle the labels across donors thousands of
times and redo the whole measurement each time. That tells us what the
measurement produces when there is nothing real to find. `p` is the fraction
of shuffles that did as well as the real labels. p = 0.05 means one shuffle
in twenty matched us by chance; p = 0.70 means we are indistinguishable from
chance.

**AUC.** Pick one control person and one disease person. How often does the
method score them in the right order? 0.5 is a coin flip. 0.7 means seven
times in ten.

**Held out.** Donors the method never saw while it was being fitted. Testing
on donors you fitted on always flatters you.

**Direction.** A line through the 16-number space. Moving along it takes you
from "looks like a control" to "looks like a case".

**Decoder.** The half of the model that turns 16 numbers back into gene
levels. It lets us ask: if I move a cell along the disease direction, which
genes change?

**rASRM stage.** A score of 1 to 4 that a surgeon assigns during the
operation, based on how many lesions there are and how deep they go.

---

# 1. X1 — giving every cell a type

**What we did.** Only 2 of our 11 studies came with cell type labels. The
other 9 arrived as raw cells with no identity, which is 937,122 cells and 136
people. For each unlabelled cell we found its 25 nearest neighbours among the
labelled cells, in the 16-number space, and took a majority vote.

**Corresponding claim.** None. This is plumbing, not a finding. But almost
every published claim about "more of cell type X in disease" needs it, so
nothing else in this list could happen without it.

**Verdict: it works, with one named failure.**

It gets 98.6% right when predicting one labelled study from the other, and
96% when scored in a way that gives each of the four families equal weight.
That second number matters because one study is 88% stromal and the other
53%: a method that just guessed "stromal" would score well on the first and
collapse on the second. It does not collapse.

94.3% of the 937,122 votes were unanimous across all 25 neighbours, and 98.8%
of those neighbourhoods drew on more than one person.

**The failure, which is important.** One study, Li, is follicular fluid
rather than endometrium, and it contains 15,056 **granulosa** cells, a type
that exists in ovaries and does not exist in endometrium at all. There is no
right answer available for them. The method labelled 99% of them "stromal",
confidently.

I then tried to build an "I don't know" option, twice, and neither worked.
All 25 neighbours agreed on granulosa just as strongly as on cells it got
right, so confidence tells us nothing. And granulosa cells sat *closer* to
the labelled reference than Li's immune cells did, and the immune ones were
correct, so distance is worse than useless.

**Comment.** The practical consequence: asking "what is this cell" is safe.
**Counting cell types in tissue that may contain types we have never labelled
is not**, because the unknowns are silently added to whichever family they
most resemble. That applies to lesion tissue, which is ovary and peritoneum,
and it is why X9 below carries a warning that X8 does not.

Separately, `garcia_alonso_2021_b` comes out 99.9% epithelial, which suggests
that deposit is an epithelium-sorted sample rather than whole tissue. Worth
knowing before anyone uses it in a composition claim.

---

# 2. X3 — is the menstrual cycle signal weaker in disease?

**What we did.** Measured cross-donor agreement on menstrual cycle phase
separately among control donors and among disease donors, then asked whether
the two differ by more than chance.

**Corresponding claim.** Huang 2023, from 13 people: in healthy donors the
proportions of immune cells change across the menstrual cycle, and **in
endometriosis that variation disappears**. Not a claim that a number goes up
or down, a claim that the disease *flattens the cycle*.

**Verdict: disagree. No difference, measured two ways.**

First pass, on held-out donors only, gave 16 people per side. The difference
was +0.164 in Huang's direction, p = 0.72. Useless: with 16 people spread
across five cycle phases, several phases had a single person, and the
shuffled-label range ran from −0.48 to +0.47.

AW then argued the held-out restriction was unnecessary, because the model's
cycle head is one linear map from the 16 numbers to a phase and cannot
memorise which person had which phase. I checked: train donors score 0.6422,
held-out donors 0.6545. Train is not inflated. He was right, and the
restriction was costing us two thirds of the data.

Redone on all 112 donors: control 0.6825, disease 0.7474, **difference
−0.0650**, p = 0.505.

**Comment.** Two things to notice. The difference **flipped sign** when the
donor count went up, which tells you the first estimate was noise. And the
chance range tightened from ±0.48 to ±0.19, so this run actually had the
power to detect an effect, and there was none.

---

# 3. X3b — the same question, asked the way Huang asked it

**What we did.** Huang's claim is about *proportions*, not about the
16-number space. So: for each person, what fraction of their cells are
immune? Then fit one model over all 101 people:

> immune fraction depends on study + cycle phase + disease + (cycle phase ×
> disease)

That last term is the claim written as arithmetic. It asks whether the effect
of cycle phase is *different* depending on disease status. Study is in the
model as a nuisance term, so differences between cohorts are absorbed rather
than mistaken for biology.

**Corresponding claim.** Huang 2023 again.

**Verdict: disagree. No interaction.** F = 0.263, p = 0.76, where the
shuffled-label 95th percentile is 3.06. Not close.

**Comment.** This one uses no model output at all. Cell family, cycle phase
and disease status all came with the data. That makes it a statement about
the corpus, at 101 people against Huang's 13, which nobody can dismiss by
questioning ELAJ.

An earlier version of this analysis compared the two studies separately and I
read the single-study number as the trustworthy one. AW ruled that wrong:
our power is the pooling, so study belongs in the model, not as a split. The
rebuilt version above is what stands.

---

# 4. X8 — does cell composition differ between healthy and disease?

**What we did.** For each of 194 people across all eleven studies, the
fraction of their cells in each of the four families, using X1's transferred
labels. Then: does disease status change those fractions, after accounting
for which study the person came from?

**Corresponding claim.** Dümpelmann 2026, from 60 people: once you account
for cycle phase, **the mix of cell types barely differs** between people with
and without endometriosis. Of 57 cell types they examined, exactly one changed
notably, a 1.6-fold rise in one kind of blood-vessel support cell.

**Verdict: agree, strongly, at more than three times their donor count.**

| family | control | disease | p |
|---|---:|---:|---:|
| immune | 0.1006 | 0.2302 | 0.619 |
| stromal | 0.5226 | 0.5836 | 0.736 |
| epithelial | 0.3308 | 0.1469 | 0.902 |
| endothelial | 0.0460 | 0.0393 | 0.236 |

Nothing moves. The raw averages look different, but once study is accounted
for, none of it survives.

**Comment.** This is the cleanest positive in the whole set, and it is a
published claim independently confirmed at scale, which is exactly what an
atlas is for.

It is also load-bearing for our own argument. **If you cannot find
endometriosis by counting cell types, then finding it requires reading what
the cells are doing**, which is what the 16 numbers are. X8 is the reason the
later immune result matters.

One caveat on the shape of the test. The four fractions add up to 100%, and
the families were named in advance by the claims being tested, so these are
not four independent attempts at significance.

---

# 5. X8 extended — does composition track how severe the disease is?

**What we did.** Among people who have endometriosis only, split into lower
severity (mild, or rASRM stage 1 to 2) and higher severity (severe, or stage
3 to 4). 51 people. Same composition test.

**Corresponding claim.** None directly. AW asked whether X8 could reach far
enough to support the severity result, and it can.

**Verdict: nothing tracks severity.** Immune p = 0.209, endothelial 0.162,
stromal 0.970, epithelial 0.913.

**Comment.** Put this beside what the 16 numbers already said. Severity as a
merged variable clears its chance threshold at 118 people (p = 0.025), but
mild against severe among patients only does not (p = 0.129 at 57 people).

So **two independent readouts now fail to recover the surgeon's grade**: one
from the model's representation, one from a plain headcount. They are not the
same evidence, and they agree.

The argument that supports: **rASRM staging describes where lesions are and
how extensive they look, not what the tissue is doing.** It is anatomy, not
biology. That is worth saying in a paper, and it matters clinically, because
a person with a tiny lesion and severe symptoms is currently told they have
mild disease.

Both legs are failures to find something at about 55 people each, so the
pairing is the argument rather than either number alone.

---

# 6. X9 — does composition differ between lesions and endometrium?

**What we did.** Same test, but comparing lesion tissue against endometrium
from people with the disease. 151 people.

**Corresponding claim.** Sarsenova 2024, from 4 people with paired samples:
blood-vessel support cells, endothelial cells and immune cells are a larger
share of lesions, and stromal cells a smaller share.

**Verdict: one large effect, which we cannot claim.**

**Epithelial cells are 6.6 times rarer in lesions**, 14.7% against 2.2%, with
p below 0.0001. Everything else is null.

**Comment, and this is the whole result.** The Sarsenova paper names the
problem itself: low epithelial counts in lesions are "most likely due to the
cell loss during the tissue dissociation procedure". Lesion tissue is fibrous
and has to be broken apart more aggressively to release single cells, and
epithelial cells are fragile. So a lower epithelial fraction may be the
protocol rather than the disease, and nothing in our corpus separates the
two.

**This goes in the paper as a limitation of the data, stated with the same
caveat its source paper states.**

One thing in our favour: the absorption error from X1 runs the *opposite*
way. Mesothelial cells line the peritoneum, have no endometrial counterpart,
and would be pushed into epithelial or stromal, which would raise the
epithelial fraction in lesions. It is lower anyway.

---

# 7. X12 step A — where in the 16 numbers does the disease live?

**What we did.** Two stages.

First, globally: is there a single line through the 16-number space that
separates control people from disease people? We fitted it on 70% of donors
and tested on the other 30%, repeatedly.

**It does not exist.** AUC 0.536 against a shuffled-label 0.482, with 28% of
shuffles beating it. A single global disease axis is not there.

That does not contradict our headline disease number of 0.3364. Cross-donor
agreement is a *local* measure: a cell's neighbours from other people can
share its label without any single global line existing.

AW then said: the 16 numbers already separate cells by family, so look for
the disease inside a family. Which is the right move.

**Second stage, inside each family**, using the two studies with real labels,
118 people:

| family | people | AUC | chance | p |
|---|---:|---:|---:|---:|
| all mixed | 114 | 0.605 | 0.503 | 0.155 |
| stromal | 101 | 0.592 | 0.499 | 0.175 |
| epithelial | 98 | 0.466 | 0.490 | 0.590 |
| **immune** | 94 | **0.708** | 0.481 | **0.015** |
| endothelial | 85 | 0.682 | 0.486 | 0.050 |

**Corresponding claim.** Several, from different directions. HECA 2024 used
genetics to predict that macrophages, a kind of immune cell, are among the
cell types disrupted in endometriosis. Dümpelmann's signalling changes are
macrophage-centred. Shih's two largest effects are both immune. Huang's
entire paper is about immune cells.

**Verdict: agree. The disease signal is in immune cells.**

**Comment.** Mixing the families destroys it: 0.605 and not significant.
Inside immune cells it is 0.708 and significant. Epithelial cells carry
nothing at all.

Endothelial being second fits the other thread running through the
literature: Dümpelmann's single composition change is a blood-vessel support
cell, Tan's lesion-specific population is a blood-vessel support cell, and
Sarsenova's largest metabolic change is in the same cells.

**We also ran this at 207 people using X1's transferred labels, and the
signal weakened**: immune 0.596, p = 0.073. It stays the strongest family and
keeps its sign, but it does not strengthen with scale.

**The one-line reason the paper reports 118 and not 207:** beyond the two
annotated studies the cell families are themselves model predictions, so a
disease test on them compounds one prediction with another.

---

# 8. X12 step B — what are those immune cells doing differently?

**What we did.** Took the disease direction from inside immune cells, and
asked the decoder: if I nudge a cell along this line, which of the 15,496
genes change most? This never looks at measured gene counts. It asks the
trained model a question, so the answer is a statement about what ELAJ has
learned.

Safety check first: the answer has to be the same whether you nudge a little
or a lot, or the whole thing is an artefact of step size. The two rankings
agree at 0.997.

**Verdict: the disease end of the line is coherent and interpretable.**

The genes moving towards disease:

- **CCL3** and **CCL13** — signals that macrophages release to call in more
  immune cells
- **ITGAX** — a surface marker of macrophages and dendritic cells
- **SIGLEC7** — a receptor on natural killer and myeloid cells
- **TNFRSF17** — a plasma cell gene; plasma cells are the antibody-producing
  form of B cells
- **MMP3, MMP27, LRRC15** — proteins that break down and rebuild the
  structural scaffolding between cells

That is an inflammatory, macrophage-weighted immune profile. **Dümpelmann
describes exactly that, from a completely different method**: inflammation
enriched, macrophages central to the altered signalling.

**Corresponding claim, specifically.** HECA names four genes with directions.
I originally checked all four and got what looked like one agreement and two
disagreements. That was my error: **three of the four are claims about
stromal cells, not immune cells.** Only IGF1 is reported in macrophages.

**IGF1 agrees.** Our direction has it rising in disease, at the 4th percentile
of 15,496 genes.

The other three would need a stromal direction to test, and step A says
stromal does not generalise, so there is nothing to push through. That goes
in limitations.

**Comment, and one half of this must not be used.** The control end of the
line is topped by epithelial identity genes: WNT7A, LGR5, SOX17, MSLN, TFF3,
VTCN1. I measured why. The immune disease direction is slightly tilted
towards the epithelial part of the space, cosine +0.21. That is modest, and
for scale the two family axes themselves sit at +0.62. But epithelial
identity genes respond more steeply to position than anything else in the
vocabulary, so a small tilt is enough to put them on top.

**So the disease end is a result and the control end is drift.** The
asymmetry is the tell: the disease end is immune-specific and reads
coherently; the control end reads as a different cell type.

**Which of these genes the corpus papers already name**, checked against all
ten PDFs:

| gene | named in a corpus paper? |
|---|---|
| **CCL3** | **yes, and it is a direct hit.** Dümpelmann lists it among "the key genes in the unified PCA, ranked by integrated gradients importance scores" -- the genes *their own neural network* found most important for predicting endometriosis, beside IL1B, CCL4, HLA-DRA, CD74, A2M, ACKR1 |
| **ITGAX** | **yes.** Dümpelmann reports ICAM1-(ITGAX+ITGB2) among the ligand-receptor interactions enhanced in disease |
| MMP3 | yes, Shih and Marečková |
| LRRC15 | Dümpelmann, but only as a figure axis label, so weak |
| IGF1 | Fonseca, García-Alonso, Marečková, Tan |
| **CCL13, SIGLEC7, TNFRSF17, MMP27** | **named by no corpus paper** |

CCL3 is the strongest single line in this whole exercise: **two different
models, two different architectures, two different training objectives, and
the same gene comes out as important for endometriosis.** Theirs is a
supervised classifier told the labels; ours is an unsupervised representation
that never saw them.

**ORTHOGONALISED, 13 November.** The cell-identity component was projected
out of the direction: cosines dropped from +0.211 epithelial, +0.002 stromal,
-0.037 endothelial to residuals of 0.016 or less. Step-size check 0.9984.

The disease side became more coherent, not less, which is the answer to
whether it was identity drift:

    TREM1, IL1B, CCL13, SIGLEC7, ADAMDEC1, SERPINB2,
    MMP19, MMP27, LRRC15, INHBA, SCARA5, CST11, DKK1, KCNH1, ALPK2

**IL1B arrived and it is a direct hit on the primary source.** Dümpelmann
ranked which genes their own neural network relied on to predict
endometriosis: *"The key genes in the unified PCA, ranked by integrated
gradients importance scores, include IL1B, CCL4, CCL3, HLA-DRA, HLA-DPA1,
CD74, A2M, and ACKR1."* **IL1B is first in that list.** Verified in the PDF
text on disk, not from a summary.

**EXTERNAL VALIDATION, verified against primary text saved locally in
`Atharva Papers/Validation/`.** Zhao et al., *Biomedical Reports* 2017
(PMC5449958) sequenced 8 eutopic endometria from endometriosis against 5
controls and published 66 upregulated and 6 downregulated genes. **It is not
in our corpus.**

| our disease side | they report | fold | p |
|---|---|---:|---:|
| **SERPINB2** | upregulated | 72.95 | 1.51e-04 |
| **MMP27** | upregulated | 40.93 | 1.69e-04 |
| **LRRC15** | upregulated | 25.20 | 3.17e-24 |
| **INHBA** | upregulated | 15.33 | 1.19e-15 |

**Four of our top fifteen are in their 66-gene list, all in the same
direction, out of 15,496 genes. Hypergeometric p = 4.0e-07.**

**Not one of our fifteen control-side genes appears anywhere in their table.**
That asymmetry is the strongest evidence that the disease side is real and
the control side is drift.

**Orthogonalisation improved the overlap**, which is independent evidence
that the projection removed noise rather than signal:

| | hits in their up-list | p |
|---|---:|---:|
| before | 3 (LRRC15, MMP27, MMP3) | 3.2e-05 |
| after | 4 (INHBA, LRRC15, MMP27, SERPINB2) | 4.0e-07 |

**TNFRSF17 (BCMA), verified.** Hever et al., *PNAS* 2007: *"Only BCMA was
strongly up-regulated in endometriosis lesions"*, by TaqMan qPCR, endometrium
43 +- 13 (n = 16) against endometriosis 290 +- 89 (n = 13), roughly 6.7-fold.
⚠ That compares **lesions** with control endometrium, not eutopic with
control. TNFRSF17 dropped out of the top fifteen after orthogonalisation.

⚠ **CCL13 is weaker than I first reported and the correction matters.** The
peritoneal-fluid single-cell paper (PMC8157653) says only that CCL13 is
"highly expressed in cluster 3", a macrophage cluster, and names it a
critical chemokine for mononuclear phagocyte migration. **It makes no
endometriosis-versus-control comparison for CCL13.** So CCL13 is expressed by
endometriosis-associated macrophages and is not a reported differential
finding. My earlier line overstated it.

**SIGLEC7** still has no direct report. The surrounding biology is
established, inhibitory NK receptors up and NK cytotoxicity down in
endometriosis, but the gene itself is not reported as differentially
expressed. Candidate, not discovery.

⚠ **TREM1 and ADAMDEC1 are in no corpus paper and were not searched.** Both
are macrophage genes and both are plausible. Search before claiming anything.

**Copies on disk**: `Atharva Papers/Validation/PMC5449958.{xml,txt}` and
`PMC8157653.{xml,txt}`. The PNAS paper could not be downloaded; the publisher
blocks it and Europe PMC has no full text. **Its PDF needs fetching by hand**
if the BCMA line is used.

## The fifteen disease-side genes, lined up

Checked four ways: all ten corpus papers; Zhao et al. *Biomed Rep* 2017
(PMC5449958, 8 eutopic endometriosis against 5 controls, not in our corpus);
**Open Targets Platform**, MONDO_0005133, 3,554 of 3,619 associated genes
retrieved; and **PubMed** co-mention counts via NCBI esearch.

| gene | Zhao 2017 | corpus papers | Open Targets | PubMed | read |
|---|---|---|---:|---:|---|
| **IL1B** | — | **first in Dümpelmann's own classifier importance list**; Marečková | **0.214** | 51 | well established |
| **SERPINB2** | **up 72.95x** | Shih, inflamed/senescent stromal | 0.007 | 5 | established |
| **MMP27** | **up 40.93x** | — | **absent** | 1 | **established, and the databases miss it** |
| **LRRC15** | **up 25.20x** | Dümpelmann, label only | 0.015 | **0** | **established, and PubMed misses it** |
| **INHBA** | **up 15.33x** | Fonseca, label only | 0.009 | 3 | established |
| DKK1 | — | HECA: **down** in case, stromal | 0.020 | 7 | established, opposite direction, other compartment |
| CCL13 | — | — | 0.023 | 1 | thin; present in macrophages, never tested |
| TREM1 | — | — | absent | 2 | thin; present in neutrophils, never tested |
| MMP19 | — | Marečková, label only | absent | 1 | thin |
| CST11 | — | — | 0.007 | 0 | thin |
| SCARA5 | — | Marečková, label only | 0.002 | 0 | thin |
| **SIGLEC7** | — | — | **absent** | **0** | **nothing anywhere** |
| **ADAMDEC1** | — | — | **absent** | **0** | **nothing anywhere** |
| **ALPK2** | — | — | **absent** | **0** | **nothing anywhere** |
| **KCNH1** | — | — | **absent** | **0** | **nothing anywhere** |

**The databases have demonstrable false negatives, and our own verified hits
prove it.** LRRC15 is reported upregulated 25-fold at p = 3.2e-24 and returns
**zero** PubMed hits. MMP27 is reported upregulated 41-fold and is **absent
from Open Targets entirely**. Both appear only in a supplementary table,
which neither PubMed's index nor Open Targets' text mining reaches.

**So "absent from the database" is not evidence of novelty.** It is evidence
that nobody has written it in an abstract. Any novelty wording in the
manuscript has to say what was searched and accept that supplementary tables
are invisible to all of it.

**Four genes return nothing from any of the four checks**: SIGLEC7,
ADAMDEC1, ALPK2, KCNH1.

**AW's ruling, 13 November, and it overturns my recommendation.** I proposed
naming only SIGLEC7 and ADAMDEC1 and treating ALPK2 and KCNH1 as noise. AW:

> "We have checked the entire scRNA database (our corpus), we checked 2 main
> databases, and we checked simple searches. If nothing has turned up yet, I
> think we are in the clear. If there is something that hasn't been made
> publicly available, we are not responsible for that. I would name all of
> the new ones in our paper regardless of how likely you think they are.
> Noise or not can be validated by others that read our paper."

He is right on both counts. Filtering by my hunch substitutes a prior for
evidence, and a reader who has a contrary result cannot check a gene we never
named. **All four go in the paper.**

**The wording, which the false-negative finding shapes rather than blocks:**

> To our knowledge, and searching the eleven studies pooled here, the Open
> Targets Platform (MONDO_0005133) and PubMed, SIGLEC7, ADAMDEC1, ALPK2 and
> KCNH1 have not previously been reported as altered in endometriosis.

That names what was searched, which most papers do not, and it is checkable.
It does not claim priority, which nothing could establish.

**Ship the full ranked list in Supplementary**, not only the top fifteen, so
a reader can look up any gene rather than taking our selection on trust. That
strengthens the novelty wording rather than weakening it.

**No manual lookup needed, both are APIs**, but the human-readable versions
are:

- Open Targets: <https://platform.opentargets.org/disease/MONDO_0005133/associations>
- PubMed, per gene: `("GENE") AND endometriosis` at <https://pubmed.ncbi.nlm.nih.gov/>

**BCMA verified from the PDF itself**, now at
`Atharva Papers/Validation/Hever2007_PNAS_BCMA_endometriosis.pdf`:
*"Only BCMA was strongly up-regulated in endometriosis lesions"*, TaqMan
qPCR, endometrium 43 +- 13 (n = 16) against endometriosis 290 +- 89 (n = 13).
⚠ The tissue is **lesions**, not eutopic endometrium, and TNFRSF17 left the
top fifteen after orthogonalisation.

One more worth a sentence and not a claim: TNFRSF17 is a plasma cell gene,
and Shih reports B cells enriched in cases. We cannot test that claim, since
our copy of Shih's cohort has no controls. One gene on a ranked list is not a
test, but it points the same way.

---

# 9. X14 — does it matter which tissue a cell came from?

**What we did.** Within one cell family, can the 16 numbers tell a cell taken
from a lesion (ovary or peritoneum) from a cell taken from endometrium inside
the uterus? **This is a question about tissue site, not about disease.** It
never compares healthy endometrium to disease endometrium; that contrast is
X8 and X12. 262 people, with each person-and-tissue pair counted
once, and the splits made by person.

**Corresponding claim.** Fonseca 2023: the same cell type is transcriptionally
different depending on which tissue it sits in. A lesion is not endometrium
that has moved; the cells are changed by where they are.

**Verdict: weak support, in two families.**

| family | AUC | chance | p |
|---|---:|---:|---:|
| stromal | 0.623 | 0.495 | 0.078 |
| endothelial | 0.618 | 0.494 | 0.095 |
| immune | 0.562 | 0.502 | 0.240 |
| epithelial | 0.522 | 0.494 | 0.401 |

**Comment, and I had the logic backwards until AW corrected it.** I first
called this test circular, because tissue is fed to the decoder as an input.
The conditioning does the opposite of what I said: **handing tissue to the
decoder removes the latent's need to encode it.** That is the stated purpose
of the covariate. So tissue structure that survives in the 16 numbers is
structure the model had every reason to throw away, and finding it is
evidence rather than an artefact.

Read that way the result is good for us in both halves. Most tissue structure
is gone, which is the design working as intended. What remains is in stromal
and endothelial cells, weakly, which is Fonseca's direction.

Neither clears the usual threshold, and tissue is almost perfectly tangled up
with being a lesion donor here, so this is a companion to X9 rather than an
independent axis.

---

# What we could not test at all

**Shih's four claims.** Uterine natural killer cells almost absent in cases,
decidualised stromal cells reduced, stromal cells more inflamed, B cells
enriched. All four are comparisons against controls, and **our copy of that
cohort has 11 people, all of whom have the disease.** The controls and the
undiagnosed-but-symptomatic group are not in the corpus. These are the
largest effects claimed anywhere in our eleven papers, both at p below
10⁻¹⁶, and we cannot touch them. **The paper should say so plainly.**

**Chen's pain claim.** Pain is not recorded anywhere in the corpus, and that
study is 2 people per group.

**Fonseca's mutation claim.** We have no DNA mutation calls.

**Fonseca's ovarian cancer claim.** We have no cancer samples.

**The progenitor-epithelium claim** (García-Alonso and Tan). Needs epithelial
subtypes finer than our four families, or measured gene expression. We have
neither locally. Future work.

**Sarsenova's metabolic claims.** Our model groups genes into 44 pathway
groups, built by rolling up Reactome and GO. The roll-up merged glycolysis,
HIF-1 signalling and glutathione metabolism into broader buckets; only
oxidative phosphorylation survives as its own group. **The vocabulary is
coarser than the claim**, so we would be answering a weaker question than the
one asked. Skip, and say why.

---

# The short version

| | |
|---|---|
| **Composition does not differ** between healthy and disease endometrium, 194 people | **agrees** with Dümpelmann, at 3× the donors |
| **Immune cells carry a disease signal** that holds on unseen people, AUC 0.708 | **agrees** with HECA, Dümpelmann, Huang, Shih in direction |
| **That signal reads as macrophage-led inflammation** in genes, and IGF1 agrees with HECA | **agrees** |
| **Neither severity readout recovers the surgical grade** | supports an argument **against** rASRM as a biological axis |
| **The cycle is not flattened by disease**, measured two ways | **disagrees** with Huang |
| **Epithelium is far rarer in lesions** | **agrees** with Sarsenova, but cannot be separated from dissociation loss |
| **Tissue structure is mostly absent from the latent**, with a weak residue in stromal and endothelial | the decoder conditioning working; weakly **agrees** with Fonseca |
