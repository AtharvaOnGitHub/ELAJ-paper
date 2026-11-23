# Supplementary Methods: Note or main Methods? (guide's comment 1)

NMI's guidance on supplementary items allows Supplementary Notes but has no
"Supplementary Methods" type: *"if additional information is needed, e.g. for
algorithm description, step-by-step protocol… they can be included as a
Supplementary Note."* Main-text Methods sits outside the 3,500-word cap, which
excludes the online Methods; ours is about 5,750 words.

## What the section holds (2,929 words in the source file, two tables, one equation)

| subsection | about | what points to it | where it fits |
|---|---|---|---|
| **Severity** (~270 w) | how rASRM stage and grade are merged into one severity variable | Results, *Endometriosis severity…*: "(Supplementary Methods, *Severity*)" | **main Methods**: it defines a quantity Results reports |
| **Pathway gene grouping** (~540 w) | how the 44 groups were cut from Reactome and GO | Note 6 and Note 5 | Note: main Methods already has a *Pathway gene grouping* subsection; this is the detail behind it |
| **Size buckets** (~390 w, Supplementary Table 29, 1 equation) | padding and bucketing of groups for speed | main Methods *Optimisation*: "(Supplementary Table 29)" | Note: engineering detail |
| **Hyperparameters** (~510 w, Supplementary Table 30) | every setting, how it was set | main Methods: "(Supplementary Table 30)" and the weak-discriminator sentence | Note: you ruled on 17 Nov that hyperparameters stay out of the main Methods |
| **Decoding a latent direction** (~460 w) | moving cells along a latent direction and decoding which genes it carries | Note 3 | Note: only the supplementary uses it |
| **Label transfer** (~380 w) | transferring cell family from the two annotated studies to the other nine (K = 25) | Results, *Per-donor disease axes…*: "(Supplementary Methods, *Label transfer*)" | **main Methods**: it defines labels Results reports |

## Options

**A. Rename the whole section "Supplementary Note 7: Supplementary methods".**
This is the least work: one heading, plus pointer text changed from
"Supplementary Methods, *X*" to "Supplementary Note 7, *X*" in five places.
Two of them are main Results, one is main Methods and two are Notes.
Supplementary Tables 29 and 30 keep their numbers.

**B. Split the section (recommended).** Severity and Label transfer, about
650 words, move into the main Methods as two subsections. The other four
become Supplementary Note 7. Results then points at "(Methods, *Severity*)"
and "(Methods, *Label transfer*)", the same way it points at every other
Methods subsection. NMI's own line is *"We encourage all methodological
information to be included in the main text."* Moving these two satisfies
that for the parts a reader of Results needs, and leaves engineering detail
in the Note, as you ruled on 17 Nov. The word cap is unaffected.

Your call. Either is a small edit once you choose.
