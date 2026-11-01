# Final review: toolkit-1p1-v1 (1+1 paper), 2026-10-29 (session 15)

Bar: a journal submission (PRD register). Source `paper/toolkit-1p1-v1.tex` (split from `counting-full-v2.tex`, kept unchanged).
Four referee rounds (reports in `paper/referee-rounds-2026-10-29/`): major → minor → minor → minor, plateau reached.

**Completion: ~80 %. Target journal: Classical and Quantum Gravity** (PRD acceptable as an alternative). The paper is a set of elementary,
exact two-dimensional kinematic tools — CQG's usual causal-set territory (Rideout–Wallden, Henson, Cunningham, Johnston 2022, Glaser–Surya); two
of the three referee passes that judged venue preferred CQG, one said PRD is reasonable. My recommendation: CQG, unless the 3+1 paper goes to PRD
and Roberto wants both in one journal.

## What the paper now says
Title: "Counting identities in two-dimensional causal sets: spatial distance, depth-drift curvature, and a fixed-size propagator target".
(1) Rectangle identity d² = 2V_AV_B/V_C for any c in the common past; bias-corrected estimator, unbiased for d² above 2ℓ and more accurate than the
equal-depth filter (BK24) and the past–future interval (Brightwell–Gregory, Rideout–Wallden) on the same pairs (new baseline table, r31).
(2) Its violation in curved spacetime: de Sitter closed form tanh²(Hτ/2)/[2 ln cosh(Hτ/2)] = 1 − Rτ²/16 + …, checked in FRW; a curvature estimator
that tells flat from curved but is noisy and reads somewhat low. (3) Laguerre identity E[K|n] = ½L_n(μ/2) for Johnston's propagator; a density-free,
pair-by-pair check of the propagator — and, honestly, no stronger a phase diagnostic than the ordering fraction (r32; it misses one 4-layer crystal).
(4) Calibrated Clough–Evans embedding test with the null-pair fraction; together the diagnostics separate the e^{-βS} phases at N = 200, 400 on held-out samples.

## Strengths
- Every derivation re-derived independently by a referee pass; no errors. All new numbers verified against source files.
- Baselines added; claims softened where the data are thin; negative results stated (Laguerre vs ordering fraction; fixed-n curvature in App. A).

## What a referee may still push on
1. **Little new per page for PRD**: the tools are elementary; the strongest result is the rectangle identity + estimator + drift closed form.
2. **Curvature estimator noise** (~100 pairs for ±20 %) and a possible small negative offset; no equal-density comparison with Benincasa–Dowker or
   chain abundances (stated as a limitation; would take one laptop session to add).
3. **Embedding thresholds are empirical** and recalibrated per N; the e^{-βS} states are test inputs, not equilibrium samples.
4. The title still lists three items; acceptable for CQG.

## Before submission (checklist)
- [ ] r27 (N = 800 held-out flag test, job 450475, second wave finishing ~midday 30 Oct) → Sec. VII `\pending`. If the flag fails at N = 800,
      the abstract's "including on held-out samples" must be restricted to N = 200.
- [ ] Strip `.tex` header comments; bibliography to BibTeX.
- [ ] Optional: curvature-noise comparison with Benincasa–Dowker at equal density (laptop).
- [ ] Verify HMM25 identifiers at submission time; Roberto's language pass.
- [ ] Decide on App. A (deletable with the one Intro pointer sentence).

## What is ours
General-c rectangle identity and estimator with baselines; depth-drift closed form and estimator; application of the Laguerre identity to Johnston's
propagator (identity itself: Pinsky, Lifschitz–Pittel); calibration of the embedding test and the null-pair statistic.
