# Review of toolkit-1p1-v6 (2026-11-01, session 21): IOP style and final language pass

**What v6 is.** v5 (accepted by the external referee after round 4) put into the IOP preprint class for CQG, with a final language pass.
The content is unchanged. Files: `toolkit-1p1-v6.tex/.pdf` and `toolkit-1p1-v6-diff.tex/.pdf` (latexdiff against v5).
v5 is untouched.

## Style conversion (done)
- **Class.** `\documentclass[12pt]{iopart}`. Tectonic's bundle does not ship `iopart.cls`. The class came from arXiv source bundles: the
  same file (40451 bytes, "Current Maintainer: IOP Publishing Ltd", LPPL) was in two independent arXiv sources (2104.09331, 2407.00378).
  `iopart.cls`, `iopart10.clo` and `iopart12.clo` were copied next to the source.
  - Not done: a check against the copy on IOP's own support page (publishingsupport.iopscience.iop.org), which I could not fetch here.
  - IOP says the class is optional ("we accept submissions using all common LaTeX class and style files").
- **amsmath.** Loaded after iopart, with iopart's `equation*` removed first. All equations compile: `aligned` and `gathered`.
  The `gathered` environment in equation (1) became one line, because it fits in a single column.
- **Front matter.**
  - `\title` with a running head ("Spatial distance and curvature from a counting identity").
  - `\author`, two `\address` entries with superscripts, and `\ead`.
  - Abstract, Keywords (6), `\submitto{\CQG}` and `\maketitle`.
  - `\maketitle` gives a separate title page, which is normal for the iopart preprint.
- **Sections.**
  - `\ack` gives Acknowledgments.
  - "Data availability statement" is an unnumbered section.
  - Appendices use `\appendix` + `\section`, which gives "Appendix A/B" and equation (A.1).
  - References are an unnumbered "References" section.
- **Cross-references (IOP house style).**
  - "Eq. (n)" → "equation (n)" (`\eref`).
  - "Fig." → "figure".
  - "Sec." → "section".
  - "Table" → "table" mid-sentence.
  - "Ref. [n]" → "[n]", or the authors' names.
  - Roman d and e for differentials and exponentials (`\rmd`, `\rme`).
- **Tables.** revtex's `ruledtabular` was replaced by the iopart form: caption first, `indented`, `\br`/`\mr`. Table 2 gets a `\mr` between the two N blocks.
- **Figures.** Single-column widths:
  - distance: 0.8 textwidth;
  - drift and Laguerre: 0.6;
  - detector: full width, was `figure*`;
  - TikZ: scale 0.8.
- **References.** IOP numeric format: surname and initials, year, title, *journal* **volume** page, (arXiv:…). Same entries and the same
  order as v5, with no content changed. A script confirms that the bibliography holds the same numbers.
- **Spelling.** US with -ize, the majority in v5 (and IOP's recommended -ize):
  - neighbourhood → neighborhood;
  - programme → program.
- **Length.** 22 pages in the 12pt preprint layout; v5 was 9 two-column pages.
- **Build.** No overfull boxes. The Data availability paragraph is set `\sloppy` because of the long file names.

## Language pass (categories, with examples)
Rules followed:
- no number, equation, citation, claim or hedge changed;
- a script compared every numeric token of v5 and v6. The only differences are layout parameters, the affiliation superscripts, one
  explicit `d^2_est/d^2`, and the year moved in the references.

1. **Number-dense sentences split.**
   - v5: "Two pair selections are used, and the difference matters for the size of the errors: Table I and Fig. 2 use … ; Table II uses …"
   - v6: "We use two pair selections, which differ in the size of the errors. Table 1 and figure 2 use … Table 2 uses … In both cases, c is the deepest element for each pair."
   - The same was done to the N = 800 held-out paragraph, the convex-region results, the FRW test, the one-region comparison
     (now three paragraphs) and Limitations.
2. **Quantities defined before use.**
   - "the pooled estimate (defined below)" and "all pairs in the windows (see below)" in the convex-region paragraph. That paragraph
     precedes "Pooling" and "Sprinkled pairs".
   - "N_X is the number of elements in the region X".
   - "for a Poisson variable N with mean λ".
3. **Ambiguous pronouns made explicit.**
   - "for R<0 the ratio exceeds 1" → "the ratio d²_est/d² exceeds 1".
   - "At finite depth it measures" → "the drift measures".
   - Abstract: "it is less precise than the ordering fraction" → "the fit is less precise than the ordering fraction".
4. **Connectives and structure.**
   - "Two effects are responsible. The sample contains … And in a layered order …" → "First, … Second, …".
   - "Two choices need care." → "Two choices need care: the fit window and the way pairs are combined."
   - "The condition is therefore a sum over all pairs of a selection …; the ratio is formed from the pooled sums." → "The requirement
     is therefore to sum over all pairs of a selection …, optionally thinned …, and to form the ratio from the pooled sums."
5. **Register.**
   - "This, not 2, is the value the estimator reproduces; since it is not known in practice, the difference is a systematic of the
     method" → "The estimator reproduces this value, not 2. Since the value is not known in practice, the difference is a systematic
     error of the method".
   - "is to be pooled" → "must be pooled", the same modality as Limitations.

**Referee-accepted wording, checked word for word:**
- abstract: "with its coefficients summed over the pairs of many independent sprinklings"; "within one region, biased low";
  "about three times larger";
- Limitations: "the full embedding test (spectrum, stress and z) rejects 4 of the 20 continuum-like states";
- Fig. 3 cut: "This cut is stricter than the window of the fit below, which requires only the two intervals to lie in the region";
- the Mecke condition and its position-based selection;
- the Last & Penrose citation;
- "The N = 400 states are test inputs".

No bound was strengthened (lessons 50/51). One clause was deliberately left as it is: "the flat drift less noisy, so the difference …
in the precision factors quoted next largely reflects this lever arm". Only "factors below" became "precision factors quoted next".

## Open items for the author (Roberto)
- **Zenodo DOI** is still the red `\pending` placeholder (same release as the 3+1).
- **ORCID / submission metadata.** IOP collects ORCID in the submission system. Not in the source; supply it at upload.
- **Abstract length.** About 330 words. I did not verify a CQG word limit. If the system enforces one (often 200–300 words at IOP
  journals), shorten it there, but not the referee-fixed phrases.
- **Class file provenance.** Optionally replace the three class files with the copies from IOP's support page before upload. They should be identical.
- **cluster** still appears in the Acknowledgments. This is intended: the public release script allows it only there.
- **The diff.** `toolkit-1p1-v6-diff.pdf` uses the v6 preamble (iopart), with markup suppressed inside `tabular` and `tikzpicture`. The
  tables changed only "Eq." → "equation" and their rules. Because of the class change, every reference line shows as changed.

## Substantive points left (not touched, out of scope)
- None new. The paper's open scientific items are the ones in the round-4 report: the optional locality test, and the small N = 800
  sample, which is already stated.

## Warnings
- Equation numbers are unchanged, (1)–(12) in the body. The appendix equation changes only in style: (A1) → (A.1). Table and figure
  numbers are unchanged; the Laguerre figure is now "figure A1" (IOP numbers appendix figures by appendix).
- The answer files and the referee correspondence refer to v5 page and column layout. They are history and were not changed.
