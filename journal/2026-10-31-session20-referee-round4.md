# Session 20 — 2026-10-31 — external referee round 4 (last edits before submission)

**What happened.** Round-4 reports: 3+1 PRD **accept**; 1+1 CQG **minor, accept once 25–29 are made**. Neither goes back to the referee. v5 of both, latexdiff
against v4, answers in `answers/answer-<slug>-v5.md`; delivered to `~/Desktop/papers/{3+1 PRD,1+1 CQG}/`. 1+1 PRD track untouched. Reports copied into
each paper's `reviews/` (`review-<slug>-v4.md`).

**3+1 (embedding-3p1-v5), comments 19–21.**
- 19: sign-count sentence → "of the same order as … and the two fits were not continued equally"; relaxation range against the intrinsic fit added
  (−0.9 to +5.3 at n = 3000; +0.25 to +6.7 at n = 6000, from `sims/out/r39_relax_s_round3.txt`; +0.25 kept unrounded). No directional reading added.
  Outlook "is more likely to be reduced".
- 20: abstract "their errors decrease only slowly with density" (the k < 10 share falls ~n^−0.7, so "rarer only slowly" was wrong); Intro item 2 and Sec. IV already agreed.
- 21: present tense ("are openly available"; Ref. [32] "released with"), optional Zenodo DOI as placeholder (same release as the 1+1).

**1+1 (toolkit-1p1-v5), comments 25–29.**
- 25: abstract "with its coefficients summed over the pairs of many independent sprinklings"; Limitations "and over many independent regions; within one
  region the ratio stays biased".
- 26: Fig. 3 (`fig_part1.py` → `s4a_desitter.run`, lines 69–72) uses the stricter rectangle-to-join cut; the text now says so (recurrence of lesson 50).
- 27a: flat-control lever arm checked: τ² = V(c,a)+V(c,b) at the deepest c is 3.41 (flat) vs 0.88 (dS), std over c 0.75 vs 0.19 → ≈ 3.9×; remark added.
  27b: unrounded inserted offsets −0.095 ± 0.111 (0.86σ), −0.081 ± 0.072 (1.13σ) quoted (`r40_select.txt`).
- 28: M = 80; threshold 1.5 × median z 0.080 of 50 flat orders; z false positive has stress 0.134 (above the band) → full test rejects 4/20 continuum-like at
  N = 800 (now in Limitations); flat height measured with new `sims/r42_flat_height.py` (N = 800: 51.8 ± 2.5; N = 400: 35.7 ± 2.2; 2√N overestimates);
  "small held-out sample"; "The N = 400 states are test inputs".
- 29: present tense; Zenodo DOI still a placeholder (needs Roberto: public repo + tagged release).
- Other change: Last & Penrose (2017) cited for the Mecke formula (new Ref. [33]; later refs renumbered, methodology note now [47]).

**Not done (Roberto's steps):** the repo is still private (checked with `gh repo view`: PRIVATE, no release). Both v5 files are now in the present tense, so
the repo must be public before upload. Then tag a release with Zenodo on, fill the DOI, rebuild.

**Lessons.** No new rule; lesson 50 recurred (Fig. 3's cut not audited when the window rule changed in v4).

**Next.** Submission steps in INDEX "Next time".

**Referee final message (later).** The loop is closed for both papers (v5 confirmed, renumbering checked). Saved as `paper/referee-final-2026-10-31.md`. The three
references the referee could not confirm (Madsen 2026, Eichhorn et al. 2026, Glaser–Surya 2016) were verified on arXiv / INSPIRE. Still open (Roberto):
DOI + public repo; fresh-clone rerun; human reader; arXiv; optional locality test (design recorded, pre-register before running).
