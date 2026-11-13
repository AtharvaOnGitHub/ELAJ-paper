# Everything worth putting in the Discussion

Built 14 November 2026, the same way `RESULTS_INVENTORY.md` was built and
for the same reason: lay out every candidate before deciding the shape.

**IDs continue from the Results inventory**, which ended at F. So A1 always
means the dominance result and G1 always means a Discussion item, and the
two files can cite each other without collision.

**Strength** is how defensible the argument is if a reviewer pushes.
**Importance** is how much the paper needs it. **Rests on** names the
evidence, by Results-inventory ID where one exists.

The section already written is 1,285 words from 6 November, to the old
framing and before the claims axis. `DISCUSSION_STRUCTURE.md` records what
each of its eight paragraphs was for and what was cut from each.

**The supervisor's spine, 11 November**, which is the organising constraint:
compare us to **foundation models**, to **baselines**, and to **single
datasets**, then **limitations and future work**. Types H, I, J and M/N
below are those four. G, K, L and O are the material that does not fit the
spine and has to be placed inside it.

---

## Type G. What the work establishes, at altitude

The opening. AW's ruling from 6 November: state the full claim elaborately
here rather than summarising it, even though Results has already stated it.

| # | what we say | str | imp | rests on |
|---|---|---:|---:|---|
| **G1** | Eleven studies and 1,577,728 cells read as sixteen numbers that are the hardest of ten representations to recover a donor from and the best of ten at holding the menstrual cycle, **on a corpus where phase is geometrically indistinguishable from a batch effect** | **9** | **10** | A1, B1 |
| **G2** | The careful cycle claim, and the loose one must not be used: the phase head supplies 34.5% of the margin, so "the cycle was recovered" overstates it. **"The cell-type structure of the cycle was recovered" is what holds**, because the head is one linear map over all sixteen dimensions that was never given cell family, yet displacement splits stromal 1.07, epithelial 0.98, endothelial 0.39, immune 0.34, which is the order those compartments actually remodel in | 8 | **9** | D1, C2 |
| **G3** | **The single-biopsy confound is not an endometriosis problem.** Wherever tissue is hard to obtain, each donor gives one timepoint, and whatever varies with that moment becomes collinear with the donor. This is the generalisation and it carries no number | **9** | **10** | the mechanism, R1 §2 |
| **G4** | The case study is the licensed form, not a fallback. Hrovatin et al. say no one-size-fits-all atlas protocol exists, and their prescribed fix, coarsening the batch covariate to dataset, has a cost nobody measures. **We measured it** | 8 | **9** | `hrovatin2025atlases` |

⚠ **G4 must not claim the field names our frontier.** Hrovatin never uses
the word trade-off. I sourced that from a Wikipedia page once and it was
wrong. Quote the coarsening passage, not a characterisation of it.

---

## Type H. Against foundation models (his section 1)

| # | what we say | str | imp | rests on |
|---|---|---:|---:|---|
| **H1** | **1,883,986 parameters and sixteen dimensions, no pretraining, against scFoundation's 100 million over 50 million cells.** 53× fewer parameters and it recovers the cycle better | **9** | **10** | A2 |
| **H2** | Width is **negatively** associated with cycle recovery across the ten: ρ = −0.650, p = 0.042. A 16-component PCA beats scGPT at 512 dimensions, 0.6457 against 0.4869 | 8 | 8 | A3 |
| **H3** | **The answer to "what can a foundation model say at single-disease level", and it is the connective argument of the whole paper.** A 1.88M model can be retrained eleven times, six frontier arms and five ablations at about eleven hours each. A 100M pretrained model gives one fixed point and no curve. **Affordable retraining is what makes the trade-off measurable at all.** A reader will not infer this | **9** | **10** | B1 plus the training logs |
| **H4** | The honest boundary: we do not win on cell family (SCimilarity 0.9896 against our 0.9820), and cell family is saturated field-wide in any case. Framed as efficiency, never as conquest | 8 | 7 | A4, A5 |

⚠ **The wording is settled and is not negotiable.** *"Foundation models are
useless"* cannot be written. Only that four of them give no advantage on
this corpus. And the supervisor's own warning attaches here: *"I'd be
careful of overreaching."*

---

## Type I. Against baselines and the field's correction practice (his section 2)

| # | what we say | str | imp | rests on |
|---|---|---:|---:|---|
| **I1** | **One correction strength is not a description of the operation.** The adversarial weight moves the achievable front and then stops: 7 → 168 buys donor 0.5837 → 0.5188 at no cycle cost, and 168 → 336 gives nothing back. The information cost slides a model **along** the front without moving it. Two knobs, two different behaviours, and the field reports one scalar | 8 | **10** | B1, B2 |
| **I2** | So the prescription is: state the trade-off, measure both axes, report the point on the frontier the model occupies. **This is the methodological contribution at its proper altitude**, and it is a way of working rather than a framework | 8 | **9** | I1 |
| **I3** | **Reconstruction loss is not a model-selection criterion for a representation.** The arm with the best held-out `val_nb` in this project, 0.3911, holds less biology than the reported arm at 0.4024. One line, AW's ruling, inside I1's paragraph | 7 | 7 | the a-series logs |
| **I4** | Harmony mixes studies better than we do, 0.6697 against 0.7613, and SCimilarity recovers cell family better. **Say the axes.** A dominance claim on two axes is strengthened, not weakened, by naming the axes it does not cover | 8 | 7 | A1's caveat |

⚠ **I5, the dominance result itself, is deliberately NOT in this table.**
Nine of nine on both axes is Results' headline and NMI's guidance is that
the Discussion must not restate Results. It can be *used* (I1 and I2 both
lean on it) and it must not be re-reported.

---

## Type J. Against single datasets, which is the claims axis (his section 3)

The newest material and the group with the most items. All nine type E
results surface here, plus two convergences that are findings about the
literature rather than about our model.

| # | what we say | str | imp | rests on |
|---|---|---:|---:|---|
| **J1** | **The structural point, and it is the best single answer to "what does an atlas do that a study cannot".** Eleven independent studies keep landing on the same findings and not one can confirm another, because no two share a cohort or a cell vocabulary | **9** | **10** | the ledger |
| **J2** | **Convergence 1, vessel support cells.** Dümpelmann's only composition change in 57 cell types is a 1.6× rise in secretory mural cells; Tan's lesion-specific population is perivascular; Sarsenova's largest metabolic reprogramming is perivascular. Three designs, three tissues, 60 and 14 and 4 donors. **And endothelial is our second-strongest family at 0.682, p = 0.050** | 7 | **9** | the ledger, E2 |
| **J3** | **Convergence 2, lesions carry a less differentiated epithelium.** García-Alonso reached it by deconvoluting bulk microarray **because they had no lesion single cells**; Tan saw a progenitor-like subpopulation in 14 donors. We hold 58 ectopic donors, so this is a **first direct test** available and not taken. Future work, named | 7 | 8 | the ledger, N4 |
| **J4** | **Confirmed at scale:** composition does not differ between control and eutopic endometrium, 194 donors against Dümpelmann's 60, every family p > 0.23. **And it is load-bearing:** if the disease cannot be found by counting cell types, finding it requires reading what the cells are doing | 8 | **9** | E1 |
| **J5** | **Overturned:** Huang's claim that disease flattens the cycle fails two ways, 112 donors in the latent (−0.065, p = 0.505) and 101 donors on proportions (F = 0.263, p = 0.76) against their 13. **The proportions test uses no model output at all**, so it cannot be dismissed by questioning ELAJ | 8 | **9** | E6 |
| **J6** | **Replicated outside the corpus:** four of our fifteen disease-side genes are in Zhao 2017's 66-gene up-list, same direction, hypergeometric p = 4.0 × 10⁻⁷, **and zero control-side genes appear anywhere in it.** IL1B is first in Dümpelmann's own classifier's importance ranking | **9** | **10** | E3 |
| **J7** | **Untestable, stated plainly:** Shih's four claims are the largest effects anywhere in the corpus, two at p < 10⁻¹⁶, and our copy of that cohort is 11 donors who all have the disease. The controls are not in the corpus | n/a | 8 | E9 |
| **J8** | **Untestable for a vocabulary reason**, which is a different and more interesting failure: Sarsenova's metabolic claims need glycolysis, HIF-1 signalling and glutathione metabolism, and our 44-group roll-up merged all three into broader buckets. Only oxidative phosphorylation survives as its own group. **We would be answering a weaker question than the one asked** | 7 | 6 | the group vocabulary |
| **J9** | **The caveat that bounds every composition claim in this group.** Label transfer is accurate across studies and fails silently on cell types absent from the reference. It belongs here because it says what the atlas can and cannot be asked | 8 | 7 | F3 |

---

## Type K. What we found out about the field's instruments

**This group is why the paper is a case study and not a benchmark**, and it
is the group with no home in the supervisor's four sections. My view is that
it distributes: K1, K2 and K4 into the baselines section, K3 into it as well,
K5 and K6 into limitations or future work.

| # | what we say | str | imp | rests on |
|---|---|---:|---:|---|
| **K1** | **The standard scorecard is degenerate here in both halves.** `ilisi_knn` is exactly 0.0000 for all ten representations and `clisi_knn` exactly 1.0000 for all ten; `kbet` spans 0.0000 to 0.0400 | 8 | 8 | the benchmark files |
| **K2** | **And where it is not degenerate it is saturated.** Cross-donor cell family puts nine of ten methods within 0.0076 of each other, 0.9820 to 0.9896, with only Geneformer outside at 0.9023, against a cycle spread of 0.2974. A benchmark that ranks representations on cell-type conservation cannot rank anything on a corpus of this shape | 8 | 8 | A4, F2 |
| **K3** | **A disease score on pooled single-cell data is partly a memorisation score.** Across the ten, agreement on disease tracks donor recovery at ρ = +0.721, p = 0.019, while phase does not, +0.176. Disease is donor-constant, so a representation that remembers donors is handed the label free. **Two uses and they are different:** a caveat on everyone's disease numbers including ours, and the reason our cycle advantage is credible, since we memorise donors less than eight of nine and still recover cycle best | 7 | **9** | B3, F1 |
| **K4** | The fairness constraint, and it is not optional: **Hrovatin's authors wrote scIB.** The claim is that its biological half is saturated **on this corpus**, never that the framework is wrong | n/a | 8 | settled 11 Nov |
| **K5** | **Both gene-disease databases have demonstrable false negatives.** LRRC15 is reported up 25× at p = 3.2 × 10⁻²⁴ and returns zero PubMed hits; MMP27 is up 41× and is absent from Open Targets entirely. Both live only in supplementary tables, which neither index reaches. **So absence from a database is not evidence of novelty**, and that shapes how anyone can word one | 7 | 6 | F4 |
| **K6** | **Transferring labels through a latent fails silently and no rejection rule catches it.** 98.9% of granulosa cells confidently called stromal, confidence 1.00, and distance *closer* than correct calls. A warning worth giving the field, since label transfer is becoming routine | 8 | 6 | F3 |

---

## Type L. Endometriosis, and the clinic

The paper's disease argument, and the longest paragraph in the current
draft. AW's instruction from 6 November stands: talk freely here about what
staging has meant.

| # | what we say | str | imp | rests on |
|---|---|---:|---:|---|
| **L1** | **Whether a person has endometriosis is legible in their own uterine lining**, 0.3364 at p = 0.005, on cells that are all eutopic endometrium. So the answer is present in tissue that can be sampled **without laparoscopy** | 8 | **10** | C3 |
| **L2** | And it is specifically **immune, and reads as macrophage-led inflammation**. The signal is not spread through the tissue: pooling the families destroys it | 8 | **9** | E2, E3 |
| **L3** | **The scale comes apart under measurement.** Disease status is recoverable; merged severity clears its null at 118 donors, 0.1286 at p = 0.025; mild against severe among patients only does not, 0.0744 at p = 0.129 over 57. **And two independent readouts agree**, one from the latent and one a plain headcount with no model in it | 7 | **9** | C7, E5 |
| **L4** | **The argument that justifies the venue's attention.** rASRM scores lesion size, depth and adhesion as a surgeon sees them at one operation. It was built to predict fertility outcomes, it is what every cohort records and what trials stratify on, and it is the number a patient is handed to account for their pain. It has never tracked how much a person hurts, and patients have been saying so for decades. **The staging worth building is graded by what the affected tissue distinguishes** | 8 | **10** | L3 |
| **L5** | **The negative stated precisely, and this is where overreach would be fatal.** The permutation p has a floor set by donor count, so the claim is **not recoverable from this corpus at this donor count**, never "not biologically real" | **9** | **9** | the null widths |
| **L6** | Diagnosis takes 11.1 years and ends in laparoscopy. The case for changing both the scale and the route rests on every patient told a millimetre lesion could not account for their pain | 7 | 8 | `bontempo2025diagnostic` |

⚠ **L6 is where the supervisor cut a paragraph** and AW is raising it in
person rather than in a comment thread. Also the standing rule binds hardest
here: human health problem, never a gendered one.

---

## Type M. Limitations (his section 4a)

Plainly, not defensively, and only the ones that bite. The order is
deliberate: M1 first because it touches the headline measurements.

| # | what we say | str | imp | rests on |
|---|---|---:|---:|---|
| **M1** | **The split leaks, and it is the first limitation.** One study pair deposits the same fifteen people under two sets of identifiers, which a donor-level split cannot detect. 17,873 held-out cells, 4.3%, belong to such a person, and the estimator discards a neighbour by **identifier**, so a same-person neighbour counts as cross-donor. Phase, disease and severity are donor-constant, so it inflates them. **4.3% is the ceiling**, and 3,942 of those cells share a person with the held-out set rather than with training, which is the more direct problem | n/a | **10** | the split audit |
| **M2** | Width is not matched, sixteen against 256 to 3,072. **One clause, not a confession**, because H2 bounds how much it can matter | n/a | 7 | H2 |
| **M3** | Cycle-day continuity rests on one cohort of 60 donors. No other study here records the day, so the closed trajectory is replicated nowhere in this corpus | n/a | 7 | metadata |
| **M4** | `li_2025` is a follicular-fluid aspirate that entered labelled as endometrium and was conditioned accordingly: 45,312 cells, 2.87%, 6 of 254 donors. Its eutopic/control marks follicular fluid from an ovarian endometriosis patient against a male-factor infertility control, **so 2.87% of the disease axis carries different semantics.** It contributes no cell-family and no phase labels | n/a | 7 | settled 30 Oct |
| **M5** | **The permutation null is unstratified.** Reassigning the donor-to-label map across all eleven studies at once breaks the label-to-cohort link, so the null never sees whatever study structure survives in the latent. Bounded by our own 0.7613. A within-study permutation is the correct fix and is not built | n/a | 8 | the scorer |
| **M6** | The corpus holds only a subset of the metadata that matters. **No cohort records cycle day, progesterone, stage, grade and treatment together** | n/a | 7 | metadata |
| **M7** | **NEW, from the claims axis.** The stromal disease direction does not generalise, so three of HECA's four gene-level claims cannot be tested at all; only IGF1 is a macrophage claim and only IGF1 was testable | n/a | 7 | E2, E3 |
| **M8** | **NEW.** Beyond the two annotated studies the cell families are themselves model predictions, which is why the immune result is reported at 118 donors and not 207. Compounding one prediction with another is the thing being avoided | n/a | 8 | E2 |
| **M9** | **NEW.** Epithelial depletion in lesions is 6.6× at p < 0.0001 and **inseparable from dissociation loss**, which the source paper names itself. Stated with its source's own caveat | n/a | 6 | E7 |
| **M10** | **NEW.** Hormonal treatment is inconsistent across the corpus: most of Tan's participants were treated and Dümpelmann excluded treatment by design. Any contrast spanning both inherits it | n/a | 7 | the ledger |
| **M11** | Single runs, roughly 4% seed variability. The smallest of the set; keep only if there is room | n/a | 4 | the logs |

---

## Type N. Future work, and the three questions he predicts (his section 4b)

**This is the one licensed exception to "do not pre-empt objections nobody
has made",** because the supervisor has made all three.

| # | what we say | str | imp | rests on |
|---|---|---:|---:|---|
| **N1** | **"Does this become a good foundation model?"** His first predicted question | n/a | **9** | — |
| **N2** | **"Are foundation models bad?"** Answered with H3's settled wording and no more | n/a | **9** | H3 |
| **N3** | **"Would it work on any disease?"** The honest answer names the conditions rather than claiming the generalisation: scarce data and severe batch structure, which hold wherever diagnosis requires surgery. **We have not shown it, and a case study owes nothing more** | n/a | **9** | G3 |
| **N4** | The direct tests this corpus can now support and we have not run: the progenitor-epithelium claim on 58 ectopic donors, finer cell types than four families, reproducible marker signatures across studies (X13), and the group embeddings (X15) | n/a | 8 | J3, the ledger |
| **N5** | **What a sixteen-number cell is for.** A common coordinate system: a new cohort placed beside the eleven without being corrected into them, a pattern reported in one study looked for in another rather than argued about, and a model small enough to retrain so the next cohort does not wait on anyone repeating a pretraining run | 8 | **9** | H3 |
| **N6** | The fixes we name and did not build: a within-study stratified permutation, and a second corpus if one ever exists | n/a | 6 | M5 |

---

## Type O. The close

| # | what we say | str | imp | rests on |
|---|---|---:|---:|---|
| **O1** | Endometriosis research has been held back by cohorts that cannot be read together. **This is a way to read them together.** Already the last line of the written draft and it should survive | 8 | **9** | — |

---

# The three structural problems

## 1. The word budget: the target is about 750 words

**Corrected 14 November against eight published Discussions.** See
`DISCUSSION_REGISTER.md`; my first analysis of this was wrong in both
direction and size.

Discussion length tracks Results length at **30% across six NMI papers** and
**44% in IBDex**, whose Results is the nearest in size to ours. Our Results
is 1,650 words, so the licensed range is **500 to 840 words** and the draft
is already **1,184**.

So the section has to **lose about a third while absorbing all nine type J
items.** The two problems solve each other: the draft quotes **25 measured
values** and the eight published Discussions quote **six between them**.
Stripping the metrics is the register correction and it frees most of the
room type J needs.

## 2. The subheading question is settled by evidence, not by his ruling

**Eight of eight have no subheadings**, IBDex and scGPT included. What
carries his four sections is a topic-sentence ladder: every paragraph opens
by naming its own subject, and several carry the previous subject forward.
IBDex's ten opening clauses read as a table of contents on their own.

**So he can have his sectioned Discussion and NMI's format at once**, and
his own paper is the demonstration. This no longer needs a decision from
him.

## 3. Four things left Results for here and must not be lost

All four are in the tables above, and this is the checklist: the ρ = +0.721
asymmetry (**K3**), Huang's overturned cycle claim (**J5**), scIB's
saturation on this corpus (**K2**), and Shih's untestable claims (**J7**).

---

# What the written draft already covers, and what it does not

| group | in the 6 November draft? |
|---|---|
| G, I, K1, K2, K3, L, M1 to M6, N5, O1 | **yes**, and most of it well |
| H1, H2, H4 | yes, as one short paragraph on scale |
| **H3** | **no.** The connective argument of the paper is not in it |
| **all of J** | **no.** The claims axis did not exist |
| K5, K6 | **no** |
| M7 to M10 | **no** |
| **N1, N2, N3** | **no.** The three predicted questions are unanswered |
| J8, N4, N6 | **no** |

**So the draft is roughly half of what the section now has to carry**, and
the half it is missing is the half the supervisor's feedback asked for.
Remoulding it is the right move rather than rewriting: types G, I, K and L
are largely written and good.

---

# Proposed order, for AW to accept or reshape

1. **G1 to G4.** What this establishes, and the single-biopsy generalisation.
2. **H1 to H4**, led by **H3**. Foundation models, and why small buys the
   measurement.
3. **I1 to I4**, carrying **K1, K2, K3, K4**. Baselines, and what the
   field's instruments do on a corpus of this shape.
4. **J1 to J9.** Single datasets. Opens on J1, which is the altitude line,
   then confirmed, overturned, replicated, untestable.
5. **L1 to L6.** The clinic, and staging.
6. **M1 to M11.** Limitations.
7. **N1 to N6.** The three questions, then what the corpus can now be asked.
8. **O1.**

Eight beats, which is what the written draft has, against four sections he
asked for. **Sections 2, 3 and 4 above are his three comparisons**, and
1, 5, 8 are the frame around them.
