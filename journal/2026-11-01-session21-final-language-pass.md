# Session 21 — 2026-11-01 — final versions: IOP style, language pass, methodology note v2

**Roberto's list:** (1) 1+1 in IOP style; (2) final language pass on both papers (journal register, everything explained); (3) methodology note
updated with the last sessions; (4) referee reviews in the repo, and the note to say how the iteration was done.

**Done (three parallel agents + main session).**
- 3+1 → `embedding-3p1-v6` (9 pp): sentence splitting, terms defined ("universe" = one sprinkling), explicit referents, American spelling. No number,
  claim or hedge changed. One rewording checked by hand: the L-BFGS continuation gain (0.5 / 2.4) is "of the same order as the difference between the
  two maps" (v5: "as much as separates"); the new wording is the accurate one (mean difference 0.9 at n = 3000), consistent with referee comment 19.
  Language-level unclear points left for Roberto are listed in the v6 review (e.g. "6–8 %" bias vs median error; "the gap does not close").
- 1+1 → `toolkit-1p1-v6`: `iopart` class (not in tectonic's bundle; `iopart.cls/.clo` taken from arXiv source bundles, identical copies, LPPL, shipped next
  to the source), IOP references and house style, 22 pp preprint layout; language pass with a script check that every number is unchanged. Diff built with
  table/TikZ markup off.
- Methodology note → v2 (8 pp): new section on the external referee iteration (setup, rounds table from `history.json`, what each side caught, limits:
  same model, odds are judgement). Title unchanged, so the papers' citation stays valid.
- Reviews: every report and answer on the Desktop was already in the repo (checked with `cmp`). Added `paper/referee-workspace/` (the referee session's
  `CLAUDE.md`, `REVIEW_MEMORY.md`, `history.json`, plus a README). These contain the referee's frank odds; the e-mail address is already in the papers.

**Open (Roberto).** CQG abstract word limit (≈ 330 words now); ORCID; DOI + public repo as before. Read the three v6 review files.

**Lessons.** No new rule.
