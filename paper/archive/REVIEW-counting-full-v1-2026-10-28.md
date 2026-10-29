# Honest review: counting-full-v1 (16 pp., 2026-10-28, session 12)

Bar: a credible arXiv gr-qc preprint, now as a full paper (Roberto's decision, session 12). Source `paper/counting-full-v1.tex`; base was
`archive/counting-1p1-v1.tex` (its review, ~85–90 % at the end of session 11, is in `archive/`). New: Sec. 8 ($3+1$), Fig. 6 (`sims/fig_3p1.py`), App. A (paths dropped).

## What it is
Sections 1–7: the $1+1$ note unchanged in substance (rectangle identity, depth-drift curvature with the de Sitter closed form, calibrated embedding test + zero-share flag,
Laguerre target). Section 8: $3+1$ overlap-volume estimator; Johnston 2025 reproduced (Tables III, V) with an oracle showing his error is all in spacelike pairs;
complementary error profiles; the switch (held out, $n$ = 500–15000, a stable 17–20 % of his residual); a counting argument for why ours alone does not win;
counts-only SMACOF map as a fast approximation; cost table. Placeholder subsection 8.9 for a likelihood embedding.

## Strengths
- One storyline: "what counting can read" in 1+1 exactly, then in 3+1 against the state of the art. Dead ends sit in App. A.
- The 3+1 claim is modest and stated as such; it is held out, paired on the same universes, and wins in every universe at every $n$.
- The oracle is a clean, reusable diagnostic: it tells the community where Johnston's method can still improve (0.9999 headroom).
- Reproduction of a recent paper, including a definitional subtlety (strictly-between counts), is useful in itself.

## Weaknesses a moderator or referee would see
1. **Two papers stapled together.** The 1+1 part is exact and elementary; the 3+1 part is numerical benchmarking. The title bridges them, but a referee may ask
   for a split. Mitigation: the intro now frames both as "geometry by counting"; the 3+1 section reuses the overlap regions of Sec. 3. Consider again once 8.9 is decided.
2. **Small absolute gain, thin statistics at large n.** +0.0022 at $n$ = 15000, from 2 universes (± is not meaningful with 2). The *share* (17–20 %) is the claim,
   and it rests on 2/4/4/2 universes. Before submission: 4+ universes at 15000 (one cluster job, ~4 h each).
3. **One benchmark geometry.** Everything is a flat causal diamond; the waist is exactly what makes far pairs hard. A second shape (e.g. a cylinder slab, or late events only)
   would show whether the switch helps generally or only on this benchmark.
4. **The convergence argument is heuristic.** $\kappa$ is not computed; the median slopes come from two sizes (1000, 3000) on pairs with ≥ 20 shared events (a selection);
   the large-$n$ embedding slopes from three sizes. Stated as rough in the text. The waist-pair explanation is supported by Table 2 (far-pair error 12 % vs his 6 %) but
   not yet isolated directly (the waist-pair oracle diagnostic is being run separately, session 12).
5. **Our estimator is biased low by 11–17 % at $n$ = 1500** (Table 2), although late events in large sprinklings show ≤ 1 % bias. The text attributes it to small counts
   near the edges; that is plausible, not shown. A referee will ask.
6. **Johnston Table IV not reproduced.** Stated neutrally; ideally ask Johnston before submission (two questions are recorded in idea 005).
7. **Timing on a shared node.** Our step 208 → 238 s (10000 → 15000) is implausibly flat; the text says so. A clean timing run (exclusive node) would fix the table.
8. **Placeholder 8.9** must be filled or deleted before anything goes out.

## What is ours, and how deep we searched
| Claim | Search depth |
|---|---|
| General-$c$ rectangle identity + Poisson-unbiased estimator (1+1) | BK24 citers, full text (session 10); elementary, may exist in passing |
| Depth-drift curvature, de Sitter closed form | BK24 citers, full text; RSS13 and BBR26 are different observables |
| Embedding-test calibration + zero-share flag | Clough–Evans citers (session 10); flag is a cousin of Glaser–Surya (said) |
| Fixed-$n$ Laguerre target | 99 citers of Johnston 2008/2009, full text |
| 3+1 exact tabulated overlap inversion for a general reference | BK24 citers crawled for the 1+1 claims, **not re-checked for a 3+1 inversion**; Johnston 2025 uses $v_1$ as a reference too (said) |
| Johnston 2025 reproduction, oracle, switch, counting argument | Johnston 2025 has **one** INSPIRE citer (Madsen, arXiv:2610.36695, Riemann tensor from counts; **abstract only**, cited in the outlook as related). Hu–Meyer–Meyer 2025 (exact 1+1) cited. No other spatial-embedding work found in that crawl. |
| SMACOF counts-only map | method is standard (de Leeuw–Mair 2009); only the setup is ours, presented as an approximation |

Lesson 26: before submission, grep the full texts of BK24's citers for "3+1"/"four dimensions" overlap inversions, and read Madsen 2026 beyond the abstract
(its "approximate normal coordinates" could overlap with our embedding).

## Missing before arXiv
- Fill or delete Sec. 8.9 (likelihood embedding), after the waist-pair diagnostic.
- More universes at $n$ = 15000; optionally a second geometry; a clean timing run.
- Explain or fix the 11–17 % low bias at $n$ = 1500 (or show it vanishes with $n$ for whole-diamond pairs).
- Carry-overs from the 1+1 note: N = 800 detector check (cluster), code/data release.

## Roberto's items
- Author line and affiliation (draft says "Independent researcher", TODO).
- AI-use statement wording (draft text present; arXiv: AI cannot be an author; use must be disclosed).
- Endorser in gr-qc. Roberto plans to contact Boguñá once the paper is ready (session 12 decision).
- Code URL / whether the repository (or a cleaned `sims/`) goes public; `cluster_fetch/` data (small npz) would go with it.

## Distance to the bar
The 1+1 half was ~85–90 %. The 3+1 half is a solid draft of a modest result, with 8.9 open and thin statistics at the largest $n$.
Overall: **~70 %**; 2–3 sessions plus one cluster job if 8.9 is dropped, more if the likelihood embedding goes in.
