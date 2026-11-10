#!/usr/bin/env python
"""Build a copy-and-paste changeset for the supervisor's Word file.

WHY THIS EXISTS. The authoritative document is a Word file on the supervisor's
OneDrive. AW applies our changes there by hand, and a list of find-and-retype
instructions is no simpler than editing the file freehand. So this emits one
short Word document holding only the changed paragraphs, formatted from the
same reference.docx as the full draft, so a block can be copied out of it and
pasted straight over the matching paragraph in his file.

HOW TO USE IT. Declare the batch in CHANGES below, one entry per paragraph
touched, then run:

    ./make_changeset.py 2026-11-09

Each entry needs the anchor to match exactly one paragraph of the .tex, and
the script fails loudly rather than guessing.
"""
import re, subprocess, sys, pathlib

PANDOC = "/Users/atharvawaghmare/miniconda3/envs/elaj/bin/pandoc"
FILES = {"intro": "sections/01-introduction.tex",
         "res":   "sections/02-results.tex",
         "meth":  "sections/04-methods.tex",
         "disp":  "sections/06-display-items.tex"}

# Resolved cross-references. The .tex uses \ref; Word needs the literal number.
REFS = {"fig:model": "1", "fig:knobs": "2", "fig:latents": "3", "fig:endo": "4",
        "tab:field": "1", "eq:token": "1", "eq:decoder": "2", "eq:objective": "3"}

CHANGES = [
 dict(f="intro", a="This paper proposes that the trade-off can be measured",
      w='Introduction, the final paragraph, beginning "This paper proposes"',
      d="Replace the whole paragraph",
      y="Adds a cited clause so the foundation-model claim is no longer "
        "unsupported. New citation: Kedzierska et al. 2025."),
 dict(f="res", a="Raising the information cost from 1 to 30",
      w='Results, "The ELAJ frontier", paragraph beginning "Raising the information cost"',
      d="Replace the whole paragraph",
      y="lambda_dab becomes the maths symbol, three times."),
 dict(f="res", a="Adversarial weight was found to have an optima",
      w='Results, "The ELAJ frontier", paragraph beginning "Adversarial weight was found"',
      d="Replace the whole paragraph",
      y="w_kl_gauss becomes the symbol three times, lambda_dab once."),
 dict(f="res", a="Of the withheld variables, cell identity",
      w='Results, "Reading 1.58 million cells as sixteen numbers", paragraph beginning "Of the withheld variables"',
      d="Replace the whole paragraph",
      y="A sentence opened on a bracket. Now reads \"Anatomical site (Fig. 4c) hints at\"."),
 dict(f="res", a="Cycle day, recorded for 466",
      w='Results, "The menstrual cycle through ELAJ", paragraph beginning "Cycle day, recorded for"',
      d="Replace the whole paragraph",
      y="Cited Fig. 5a, which no longer exists. Now Fig. 4e, the cycle-day panel."),
 dict(f="res", a="This indicates that whether a person has endometriosis",
      w='Results, "Surgical stage and grade", the last paragraph',
      d="Replace the whole paragraph",
      y="Cited the severity panels for a cell-family and phase claim. Now "
        "compares Fig. 4a,d against 4h,i, which is what the sentence argues."),
 dict(f="res", a="Cell family and menstrual phase, measured under the same",
      w='Results, "What the disease axis measures", the last paragraph',
      d="Replace the whole paragraph",
      y="Panel list style, Fig. 4a,d rather than Fig. 4a, 4d."),
 dict(f="res", a="The phase head was ablated",
      w='Results, "What the latent needs in order to work", paragraph beginning "The phase head was ablated"',
      d="Replace the whole paragraph",
      y="Cited Fig. 5, which no longer exists. The ablation evidence is Table 1."),
 dict(f="meth", a="By using the gene identity vector",
      w='Methods, "Gene tokens", paragraph beginning "By using the gene identity vector"',
      d="Replace the whole paragraph",
      y="Refers to equation (1) by number, as NMI requires."),
 dict(f="meth", a="The cell context is read into two things",
      w='Methods, "Reconstruction head", paragraph beginning "The cell context is read into two things"',
      d="Replace the whole paragraph AND the equation inside it",
      y="The equation is now numbered (2), ends in a full stop, and the "
        "sentence after it refers to it by number."),
 dict(f="meth", a="The four heads are trained together",
      w='Methods, "Composite objective", paragraph beginning "The four heads are trained together"',
      d="Replace the whole paragraph AND the equation inside it",
      y="The equation is now numbered (3), ends in a full stop, and the "
        "sentence after it refers to it by number."),
 dict(f="meth", a="The price on the latent is the usual one",
      w='Methods, "Composite objective", paragraph beginning "The price on the latent"',
      d="Replace the whole paragraph",
      y="DELETION. The line \"information cost and is described next.\" was a "
        "stray fragment left by an earlier edit and is not a sentence."),
 dict(f="meth", a="is absent from equation",
      w='Methods, "Composite objective", paragraph beginning "lambda_dab is absent from this sum"',
      d="Replace the whole paragraph",
      y="Refers to equation (3) by number instead of \"this sum\"."),
 dict(f="meth", a="Nine representations were computed on this corpus",
      w='Methods: INSERT a new subsection immediately BEFORE "Optimisation"',
      d="Insert all four paragraphs under the heading Comparison methods",
      y="Nine comparison methods were cited nowhere in the paper. Methods "
        "references are uncapped, so this costs nothing against the 50."),
 dict(f="meth", a="The remaining settings are AdamW",
      w='Methods, "Optimisation", paragraph beginning "The remaining settings are AdamW"',
      d="Replace the whole paragraph",
      y="FACTUAL CORRECTION. It said the KL weight ramps to its full value "
        "over the first 20% of steps. The reported arm's own config has "
        "warmup_fraction 0.05 and beta_max 0.5, and Composite objective "
        "already states it correctly 160 lines earlier. Two statements of one "
        "hyperparameter disagreed and this was the wrong one."),
 dict(f="disp", a="Arms are labelled by their two knob values",
      w="Figure 2's legend",
      d="Replace the whole legend",
      y="lambda_dab/w_kl_gauss become the symbols, matching the axis labels "
        "already drawn in the panels."),
]

def paragraphs(path):
    t = pathlib.Path(path).read_text()
    t = re.sub(r"(?<!\\)%.*$", "", t, flags=re.M)
    t = re.sub(r"\\note\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}", "", t)
    return re.split(r"\n\s*\n", t)

def to_markdown(s):
    """LaTeX to pandoc markdown. Maths spans are held out of the prose
    cleanup, because stripping a backslash inside maths silently corrupts it:
    \\; became a bare ; on the first version of this script and turned the
    decoder equation into nonsense."""
    s = s.strip()
    # figure environment scaffolding is not part of a legend
    s = re.sub(r"\\begin\{figure\*?\}(\[[^\]]*\])?", "", s)
    s = re.sub(r"\\end\{figure\*?\}", "", s)
    s = re.sub(r"\\includegraphics(\[[^\]]*\])?\{[^}]*\}", "", s)
    s = s.replace(r"\centering", "")
    s = re.sub(r"\\(?:sub)*section\*\{([^}]*)\}", r"## \1", s)
    s = re.sub(r"\\begin\{(equation|equation\*)\}(.*?)\\end\{\1\}",
               lambda m: "\n$$" + re.sub(r"\\label\{[^}]*\}", "", m.group(2)).replace("\n", " ") + "$$\n",
               s, flags=re.S)

    # hold every maths span aside under a placeholder no LaTeX would produce
    held = []
    def hold(m):
        held.append(m.group(0))
        return f"\x00{len(held)-1}\x00"
    s = re.sub(r"\$\$.*?\$\$|\$[^$]*\$", hold, s, flags=re.S)

    s = re.sub(r"\\label\{[^}]*\}", "", s)
    s = re.sub(r"\\ref\{([^}]*)\}", lambda m: REFS.get(m.group(1), "??" + m.group(1)), s)
    s = re.sub(r"\\citep\{([^}]*)\}",
               lambda m: "[" + "; ".join("@" + k.strip() for k in m.group(1).split(",")) + "]", s)
    s = re.sub(r"\\citet\{([^}]*)\}",
               lambda m: "; ".join("@" + k.strip() for k in m.group(1).split(",")), s)
    s = re.sub(r"\\cite\{([^}]*)\}",
               lambda m: "[" + "; ".join("@" + k.strip() for k in m.group(1).split(",")) + "]", s)
    s = re.sub(r"\\textbf\{([^}]*)\}", r"**\1**", s)
    s = re.sub(r"\\textit\{([^}]*)\}", r"*\1*", s)
    s = re.sub(r"\\texttt\{([^}]*)\}", r"`\1`", s)
    s = re.sub(r"\\caption\{", "", s)
    s = s.replace(r"\elaj", "ELAJ").replace("{,}", ",")
    s = s.replace(r"\\", "\n\n").replace(r"\%", "%").replace("~", " ")
    s = s.replace(r"\,", " ").replace("--", "\u2013")
    s = re.sub(r"\\(?![a-zA-Z])", "", s)
    s = re.sub(r"[ \t]+", " ", s)
    s = s.strip().rstrip("}").strip()

    # put the maths back exactly as it was
    s = re.sub(r"\x00(\d+)\x00", lambda m: held[int(m.group(1))], s)
    return s

def main():
    tag = sys.argv[1] if len(sys.argv) > 1 else "changeset"
    cache = {k: paragraphs(v) for k, v in FILES.items()}
    out = [f"# Changes to paste into the supervisor's file", "",
           f"Batch {tag}. {len(CHANGES)} blocks. For each one: find the named "
           "paragraph in his file, select it whole, and paste the replacement "
           "text below over it. The replacement text is everything between the "
           "rules.", ""]
    for i, c in enumerate(CHANGES, 1):
        hits = [p for p in cache[c["f"]] if c["a"] in p]
        if len(hits) != 1:
            sys.exit(f"ERROR change {i}: anchor {c['a']!r} matched {len(hits)} paragraphs")
        out += [f"## {i} of {len(CHANGES)}", "",
                f"**Where:** {c['w']}", "",
                f"**Do:** {c['d']}", "",
                f"**Why:** {c['y']}", "", "---", "",
                to_markdown(hits[0]), "", "---", ""]
    src = pathlib.Path(f"changesets/changes-{tag}.md")
    src.write_text("\n".join(out))
    dst = f"changesets/ELAJ_changes_{tag}.docx"
    cmd = [PANDOC, str(src), "-o", dst, "--reference-doc=assets/reference.docx",
           "--bibliography=references.bib", "--citeproc", "--resource-path=."]
    if pathlib.Path("assets/nature.csl").exists():
        cmd.insert(-1, "--csl=assets/nature.csl")
    subprocess.run(cmd, check=True)
    print(f"{len(CHANGES)} blocks -> {dst}\n              -> {src}")

if __name__ == "__main__":
    main()
