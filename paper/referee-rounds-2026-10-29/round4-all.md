# Round 4 — referee report on both papers and the methodology note (plateau check)

## 3+1 (embedding-3p1-v1.tex): minor revision — no major issues
- Number mismatch: overlap-embedding oracle with truth on k<10 quoted "88 % (n=1500) and 96 % (n=3000)" — r18 gives +96 % (1500) and +88 % (3000); swapped. [writing]
- Verified: r30 (94/97 %, 3/4 %, 97–99 % vs 2 %, shares 0.496/0.314); r29 quantiles; r33 per-element figures; Table II fractions (80/81/79/83 %); Fig. 1 slopes.
- Minor: (1) Toolkit bib title wrong. (2) r33 over-reach: "true time leaves it unchanged" — s1002 rms 0.55→0.49; true t makes the median |dd| worse for s1001 (0.13 vs 0.10); "property of the starting map, not a floor" needs lnL of truth-started vs intrinsic optimum [needs-work, cheap]. (3) n=1000 universe an outlier (C_J = 0.857 vs 0.887/0.903) and the fit does not improve its rms position (0.87 vs 0.88). (4) "halves the median error" holds at n=3000 only. (5) No causal-fidelity metric (spacelike pairs never enter the fit) [needs-work, cheap]. (6) n^−0.4 fitted on 6000–15000 only; 3000→6000 the residual halves. (7) Verify HMM25 (arXiv 2601 vs JMP 2025) and Madsen (2610.36695); Casasola and Pellegrin not peer-reviewed.
- **Plateau:** reached once the swap and the bib title are fixed. **Completion ~90 %. Target: PRD.**

## 1+1 (toolkit-1p1-v1.tex): minor revision — no major issues of weight
- Re-derived the de Sitter closed form, FRW signs, Laguerre/Hilb/Poisson chain, estimator bias: correct. Table III matches r31; r32 counts match.
- Minor: (1) title oversells — the working manifoldlikeness diagnostic is empirical z, not an identity deviation; consider retitling. (2) Curvature results all lean low; abstract "verify in FRW" covers only the continuum ratio. (3) Bracket wording self-contradictory (not used to locate the transition, then 0.05<β_c<0.45): say which chains set each bound. (4) Bias below 2ℓ unmentioned (+37(7) % at N=4000; Table I non-monotonic). (5) The bottom element is never defined. (6) Held-out claim depends on r27.
- **Plateau:** reached. **Completion ~80–85 %. Target: CQG rather than PRD** (elementary 2D kinematic tools; CQG's usual territory).

## Methodology note
1. "The reviews and all earlier drafts are in the public notebook" currently false (no session-15 referee reports, journal or REVIEW files yet).
2. Review process described mostly correctly but understated: claims were weakened/corrected in both papers; say the referees are the same model, prompted by the authoring instance (not blind), and how many rounds.
3. Counts stale (70 scripts, ~6500 lines; drafts not counted; 29 Oct timeline row lacks r29–r33).
4. Mistake log 41 entries = 39 numbered + 2 sub-rules ✔; table sums to 41 ✔; dates ✔.
