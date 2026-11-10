#!/usr/bin/env python
"""Build a changeset the supervisor's Word file can be updated from by hand.

WHY THIS EXISTS. The authoritative document is a Word file on his OneDrive and
AW applies our changes there himself.

THE CONSTRAINT THAT SHAPES THIS FILE. Word stores maths as OMML objects, and
OMML does not survive a copy between documents (AW, 10 November). So:

  * A whole-paragraph paste DESTROYS any maths the paragraph already held.
    Eleven of the first batch's sixteen paragraphs contained maths and most of
    it was incidental, correct already, and nothing to do with our change.
  * Therefore the unit of change is a short maths-free fragment, not a
    paragraph. Find it, replace it, leave everything around it alone.
  * Where a symbol IS the change, it is marked MATHS and AW inserts it with
    Word's own equation tool. Nothing else can be done about that.

Three kinds of entry:

  edit   find/repl, both maths-free. The default and by far the commonest.
  maths  find/repl where the replacement is a symbol to insert by hand.
  paste  whole blocks of genuinely new prose, only valid when maths-free.

Run:  ./make_changeset.py 2026-11-09
"""
import re, subprocess, sys, pathlib

PANDOC = "/Users/atharvawaghmare/miniconda3/envs/elaj/bin/pandoc"
FILES = {"intro": "sections/01-introduction.tex",
         "res":   "sections/02-results.tex",
         "meth":  "sections/04-methods.tex",
         "disp":  "sections/06-display-items.tex"}
REFS = {"fig:model": "1", "fig:knobs": "2", "fig:latents": "3", "fig:endo": "4",
        "tab:field": "1", "eq:token": "1", "eq:decoder": "2", "eq:objective": "3"}

BATCHES = {}

BATCHES["2026-11-09"] = [
 # ---- symbols. The replacement is maths, so it goes in by hand. ----------
 dict(k="maths", w='Results, "The ELAJ frontier", the two paragraphs beginning '
                   '"Raising the information cost" and "Adversarial weight was found"',
      find="lambda_dab", repl="lambda with dab as a subscript", n=4,
      y="The code variable name was standing in for the symbol. Methods and "
        "Table 1 already use the symbol, and Figure 2's own axes are drawn "
        "with it, so the paper disagreed with its own figure."),
 dict(k="maths", w='Results, "The ELAJ frontier", paragraph beginning '
                   '"Adversarial weight was found"',
      find="w_kl_gauss", repl="w with kl as a subscript", n=3,
      y="Same reason. Table 1 already uses this form."),
 dict(k="maths", w="Figure 2's legend, near the end",
      find="lambda_dab/w_kl_gauss", repl="the two symbols, separated by a slash", n=1,
      y="The legend named the code variables while the panels it describes "
        "are labelled with the symbols."),

 # ---- figure references. All maths-free. ---------------------------------
 dict(k="edit", w='Results, "Reading 1.58 million cells as sixteen numbers"',
      find="are not labelled. (Fig. 4c) hints at",
      repl="are not labelled. Anatomical site (Fig. 4c) hints at",
      y="A sentence opened on a bracket."),
 dict(k="edit", w='Results, "The menstrual cycle through ELAJ"',
      find="closed in the latent space (Fig. 5a).",
      repl="closed in the latent space (Fig. 4e).",
      y="Figure 5 stopped existing when Table 1 replaced it. The cycle-day "
        "panel is Figure 4e."),
 dict(k="edit", w='Results, "Surgical stage and grade", the last sentence',
      find="Fig. 4h, 4i).",
      repl="compare Fig. 4a,d with 4h,i).",
      y="It cited the severity and stage panels for a claim about cell family "
        "and phase, which are 4a and 4d. The sentence compares the two pairs, "
        "so it should cite all four."),
 dict(k="edit", w='Results, "What the disease axis measures", the last sentence',
      find="(Fig. 4a, 4d).", repl="(Fig. 4a,d).",
      y="Panel list style, matching Nature's own."),
 dict(k="edit", w='Results, "What the latent needs in order to work", the '
                  'paragraph beginning "The phase head was ablated"',
      find="retention in general (Fig. 5).",
      repl="retention in general (Table 1).",
      y="Figure 5 no longer exists. The ablation evidence is Table 1."),

 # ---- equations. Numbering is manual; the prose around it is not. --------
 dict(k="maths", w="Methods: the three display equations, in Gene tokens, "
                   "Reconstruction head and Composite objective",
      find="the three unnumbered equations",
      repl="the same equations numbered (1), (2) and (3) at the right margin, "
           "in the current-professional display format. The content of all "
           "three is unchanged. Equations (2) and (3) end in a full stop "
           "rather than a comma", n=3,
      y="NMI: equations referred to in the text take parenthetical numbers "
        "and are cited as \"equation (1)\"."),
 dict(k="edit", w='Methods, "Gene tokens", the paragraph after equation (1)',
      find="projecting gene expression values we are able to avoid a trivial",
      repl="projecting gene expression values, equation (1) avoids a trivial",
      y="Refers to the equation by its number."),
 dict(k="edit", w='Methods, "Reconstruction head", the sentence immediately '
                  'after equation (2), which begins "where"',
      find="where  (that sentence's first word, nothing else)",
      repl="In equation (2),",
      y="Refers to the equation by its number. Change only that first word; "
        "the symbols after it are untouched."),
 dict(k="edit", w='Methods, "Composite objective", the sentence immediately '
                  'after equation (3), which begins "with"',
      find="with  (that sentence's first word, nothing else)",
      repl="In equation (3),",
      y="Refers to the equation by its number. Then insert the word \"is\" "
        "after the first symbol, so it reads \"In equation (3), w_kl is 1\"."),
 dict(k="edit", w='Methods, "Composite objective", the last paragraph',
      find="is absent from this sum, which is deliberate.",
      repl="is absent from equation (3), which is deliberate.",
      y="Names the equation instead of gesturing at it."),

 # ---- corrections -------------------------------------------------------
 dict(k="edit", w='Methods, "Composite objective", the paragraph beginning '
                  '"The price on the latent"',
      find="information cost and is described next.", repl="",
      y="DELETE this line entirely. It is a stray fragment left by an earlier "
        "edit, sitting after a complete sentence, and is not a sentence."),
 dict(k="edit", w='Methods, "Optimisation", the paragraph beginning "The '
                  'remaining settings are AdamW"',
      find="ramped from zero to its full value over the first 20% of steps.",
      repl="ramped from zero to 0.5 over the first 5% of steps, as above.",
      y="FACTUAL CORRECTION. The reported arm's config has warmup_fraction "
        "0.05 and beta_max 0.5, and Composite objective already states it "
        "correctly 160 lines earlier. Two statements of one hyperparameter "
        "disagreed and this was the wrong one."),
 dict(k="edit", w="Introduction, the final paragraph",
      find="arrives with no reason to have separated the two.",
      repl="arrives with no reason to have separated the two; zero-shot, "
           "these models are in any case unreliable (Kedzierska et al. 2025).",
      y="The claim that a foundation model is not an alternative stood "
        "uncited. This is the paper that evaluates exactly that."),

 # ---- genuinely new prose, the only paste in the batch -------------------
 dict(k="paste", f="meth", a="Nine representations were computed on this corpus",
      w='Methods: INSERT a new subsection immediately BEFORE "Optimisation"',
      y="Nine comparison methods were cited nowhere in the paper. Methods "
        "references are uncapped, so this costs nothing against the 50."),
]

BATCHES["2026-11-10"] = [
 dict(k="figure", w="Figure 1, the image itself",
      find="the current Figure 1 image",
      repl="figures/pinned/figure1.png",
      y="Rebuilt. It is now FIVE panels, a to e, not six: the PRISMA diagram "
        "has moved out to Extended Data Figure 1. a is your architecture "
        "drawing, b and c the two frontier scatters, d and e the UMAPs. "
        "180 x 185.6 mm at 600 dpi, so it is placed at full text width."),
 dict(k="paste_tex", f="disp", a="The architecture, in five stages",
      w="Figure 1's caption, all of it",
      y="Rewritten for the new panel a and the new panel lettering. It is "
        "also now the only place in the paper that expands DAB, ECS and "
        "Phase CLS, since the glosses stayed out of the drawing.",
      maths=["ELAJ B-hi, twice: subscript the \u2018B hi\u2019 after ELAJ"]),
 dict(k="figure", w="A NEW Extended Data Figure 1, after the main figures",
      find="(nothing, this is an insertion)",
      repl="figures/pinned/extdata1_prisma.png",
      y="PRISMA, moved out of Figure 1. Place it at about 72% of text width."),
 dict(k="paste_tex", f="disp", a="Record selection, following PRISMA 2020",
      w="The caption for that new Extended Data Figure 1",
      y="Carries the arithmetic that used to sit in Figure 1's caption."),
]

NEW_REFERENCES = [
 "Wolf, F. A., Angerer, P. & Theis, F. J. SCANPY: large-scale single-cell "
 "gene expression data analysis. Genome Biol. 19, 15 (2018).",
 "Xu, C. et al. Probabilistic harmonization and annotation of single-cell "
 "transcriptomics data with deep generative models. Mol. Syst. Biol. 17, "
 "e9620 (2021).",
 "Korsunsky, I. et al. Fast, sensitive and accurate integration of "
 "single-cell data with Harmony. Nat. Methods 16, 1289-1296 (2019).",
 "Hie, B., Bryson, B. & Berger, B. Efficient integration of heterogeneous "
 "single-cell transcriptomes using Scanorama. Nat. Biotechnol. 37, 685-691 "
 "(2019).",
 "Heimberg, G. et al. A cell atlas foundation model for scalable search of "
 "similar human cells. Nature 638, 1085-1094 (2025).",
 "Hao, M. et al. Large-scale foundation model on single-cell "
 "transcriptomics. Nat. Methods 21, 1481-1491 (2024).",
 "Kedzierska, K. Z., Crawford, L., Amini, A. P. & Lu, A. X. Zero-shot "
 "evaluation reveals limitations of single-cell foundation models. Genome "
 "Biol. 26, 101 (2025).",
]

def paragraphs(path):
    t = pathlib.Path(path).read_text()
    t = re.sub(r"(?<!\\)%.*$", "", t, flags=re.M)
    t = re.sub(r"\\note\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}", "", t)
    return re.split(r"\n\s*\n", t)

def demath(m: str) -> str:
    """Inline maths as plain readable text, for a paste that cannot carry it.

    Deleting the span (the behaviour this replaces) silently turned
    "ELAJ$_{B hi}$" into "ELAJ", so the reader could not see where the
    subscript belonged.
    """
    s = m.strip("$")
    s = re.sub(r"\\text(?:rm|bf|it)?\{([^}]*)\}", r"\1", s)
    s = re.sub(r"[_^]\{([^}]*)\}", r" \1", s)
    s = re.sub(r"[_^]", " ", s)
    s = s.replace(r"\,", " ").replace(r"\;", " ").replace(r"\!", "")
    s = re.sub(r"\\[a-zA-Z]+", "", s)
    return re.sub(r"\s+", " ", s.replace("{", "").replace("}", "")).strip()


def to_markdown(s, keep_maths=True):
    """LaTeX to pandoc markdown.

    MATHS IS HELD ASIDE during the prose cleanup and only then restored or
    flattened. Two regressions have come from getting this wrong. Stripping
    a backslash inside maths turned \; into a bare ; and corrupted the
    decoder equation. Then a later rewrite of this very function silently
    dropped both the maths guard AND the \caption strip, which went unseen
    because that batch happened to have no maths in its one paste.
    """
    s = s.strip()
    s = re.sub(r"\\begin\{figure\*?\}(\[[^\]]*\])?", "", s)
    s = re.sub(r"\\end\{figure\*?\}", "", s)
    s = re.sub(r"\\includegraphics(\[[^\]]*\])?\{[^}]*\}", "", s)
    s = s.replace(r"\centering", "")
    s = re.sub(r"\\begin\{(equation\*?)\}(.*?)\\end\{\1\}",
               lambda m: "\n$$" + re.sub(r"\\label\{[^}]*\}", "",
                                         m.group(2)).replace("\n", " ") + "$$\n",
               s, flags=re.S)

    held = []
    def hold(m):
        held.append(m.group(0))
        return f"\x00{len(held) - 1}\x00"
    s = re.sub(r"\$\$.*?\$\$|\$[^$]*\$", hold, s, flags=re.S)

    s = re.sub(r"\\(?:sub)*section\*\{([^}]*)\}", r"## \1", s)
    s = re.sub(r"\\caption\{", "", s)
    s = re.sub(r"\\label\{[^}]*\}", "", s)
    s = re.sub(r"\\ref\{([^}]*)\}", lambda m: REFS.get(m.group(1), "??"), s)
    for cmd in ("citep", "cite"):
        s = re.sub(r"\\" + cmd + r"\{([^}]*)\}",
                   lambda m: "[" + "; ".join("@" + k.strip()
                                             for k in m.group(1).split(",")) + "]", s)
    s = re.sub(r"\\citet\{([^}]*)\}",
               lambda m: "; ".join("@" + k.strip() for k in m.group(1).split(",")), s)
    s = re.sub(r"\\textbf\{([^}]*)\}", r"**\1**", s)
    s = re.sub(r"\\textit\{([^}]*)\}", r"*\1*", s)
    s = re.sub(r"\\texttt\{([^}]*)\}", r"`\1`", s)
    s = s.replace(r"\elaj", "ELAJ").replace("{,}", ",")
    s = s.replace(r"\\", "\n\n").replace(r"\%", "%").replace("~", " ")
    s = s.replace(r"\,", " ").replace("--", "\u2013")
    s = re.sub(r"\\(?![a-zA-Z])", "", s)
    s = re.sub(r"[ \t]+", " ", s)
    s = s.strip().rstrip("}").strip()

    def restore(m):
        raw = held[int(m.group(1))]
        if keep_maths:
            return raw
        flat = demath(raw)
        # a subscript flattened to text has to keep a word boundary, or
        # "ELAJ$_{B hi}$" comes out as "ELAJB hi"
        before = s[m.start() - 1] if m.start() else " "
        return (" " if before.isalnum() and flat[:1].isalnum() else "") + flat
    s = re.sub("\x00(\\d+)\x00", restore, s)
    return s


def main():
    tag = sys.argv[1] if len(sys.argv) > 1 else "changeset"
    CHANGES = BATCHES[tag]
    cache = {k: paragraphs(v) for k, v in FILES.items()}
    out = ["# Changes for the supervisor's file", "",
           f"Batch {tag}. {len(CHANGES)} changes.", "",
           "**Word maths does not survive a copy between documents.** Every "
           "FIND and REPLACE string below is free of maths, so nothing here "
           "can destroy an equation already in his file. Where a whole block "
           "has to be pasted, any maths inside it is written out in plain "
           "words and flagged under \"re-apply by hand\".", ""]

    for i, c in enumerate(CHANGES, 1):
        kind = c["k"]
        out += [f"## {i} of {len(CHANGES)}  \u2014  {kind.upper()}", "",
                f"**Where:** {c['w']}", ""]
        if kind == "figure":
            out += [f"**Do:** replace the image.", "",
                    f"**New file:** `{c['repl']}`", "",
                    f"**Why:** {c['y']}", ""]
        elif kind in ("paste", "paste_tex"):
            src = cache[c["f"]]
            hits = [p for p in src if c["a"] in p]
            if len(hits) != 1:
                sys.exit(f"ERROR {i}: anchor matched {len(hits)} paragraphs")
            body = to_markdown(hits[0], keep_maths=not c.get("maths"))
            if "$" in body and not c.get("maths"):
                sys.exit(f"ERROR {i}: a paste block contains maths and declares "
                         f"no `maths` note. Either split it into edits or say "
                         f"what has to be re-applied by hand.")
            body = re.sub(r"\$[^$]*\$", "", body)
            out += ["**Do:** paste everything between the rules below.", ""]
            if c.get("maths"):
                out += ["**Then re-apply by hand (maths will not copy):** "
                        + "; ".join(c["maths"]), ""]
            out += [f"**Why:** {c['y']}", "", "---", "", body, "", "---", ""]
        else:
            times = f", {c['n']} times" if c.get("n", 1) > 1 else ""
            verb = ("Insert by hand with Word's equation tool" + times
                    if kind == "maths" else "Find and replace" + times)
            out += [f"**Do:** {verb}.", "",
                    f"**Find:** {c['find']}", ""]
            out += [f"**Replace with:** {c['repl'] or '(nothing, delete it)'}", "",
                    f"**Why:** {c['y']}", ""]
            for s in (c["find"], c["repl"]):
                assert "$" not in s, f"ERROR {i}: maths in a find/replace string"
        out += [""]

    out += ["## References to add to the reference list", "",
            "Nature style, in the order they are first cited.", ""]
    out += [f"{n}. {r}" for n, r in enumerate(NEW_REFERENCES, 1)]
    src = pathlib.Path(f"changesets/changes-{tag}.md")
    src.write_text("\n".join(out) + "\n")
    dst = f"changesets/ELAJ_changes_{tag}.docx"
    cmd = [PANDOC, str(src), "-o", dst, "--reference-doc=assets/reference.docx",
           "--bibliography=references.bib", "--citeproc", "--resource-path=."]
    if pathlib.Path("assets/nature.csl").exists():
        cmd.insert(-1, "--csl=assets/nature.csl")
    subprocess.run(cmd, check=True)
    kinds = {}
    for c in CHANGES:
        kinds[c["k"]] = kinds.get(c["k"], 0) + 1
    print(f"{len(CHANGES)} changes ({kinds}) -> {dst}")

if __name__ == "__main__":
    main()
