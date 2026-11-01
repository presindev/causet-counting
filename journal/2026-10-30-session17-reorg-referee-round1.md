# Session 17 — 2026-10-30 (afternoon): folder reorganization; external referee round 1 answered (3+1 PRD, 1+1 CQG)

## What we did
- **Reorganization** (Roberto: "too messy"): one folder per paper, `paper/{embedding-3p1,toolkit-1p1,methodology-note}/` with `reviews/`
  (and now `answers/`); old drafts and reviews → `paper/archive/`; fetched/ignored output → `runs/` (gitignored); paths fixed in sims scripts,
  compute.md, INDEX, ROADMAP, idea 005, CLAUDE.md, release/README.md. Map: `paper/README.md`. All moves by `git mv` / `mv`, nothing deleted.
- **External referee** = a Claude session in `~/Desktop/papers/<track>/{manuscripts,reviews,answers}` (Roberto's setup). Round 1: three reports
  (3+1 PRD, 1+1 PRD, 1+1 CQG); copies in each paper's `reviews/`. Decisions (Roberto): 1+1 → CQG only; Laguerre → appendix; Johnston not contacted;
  repo + Zenodo DOI public after submission; no latexdiff for now.
- **3+1 (r35, `sims/r35_referee1_3p1.py`, `r35_analyse.py`; 10 universes each at n = 1000/3000/6000, laptop):** fit removes 72/74/80 % of Johnston's
  residual (10/10 wins at each size; start alone 59/43/33 %). The residual is a **flat direction** of the likelihood, not a local optimum:
  L-BFGS and multi-start do not close it, and the truth start beats the converged intrinsic fit by only 0.9 / 2.3 lnL units (n = 3000/6000).
  v1's "local optimum" sentence retracted in v2. Near-cone pairs only slightly *better* than all related pairs (10/10) → "all pairs" dropped as a
  contribution. Joint time+space fit: negligible gain, time error unchanged. New Fig. 2 (where the error remains), Table I of sets, Table III likelihood.
- **1+1 (r36–r38):** HMM construction implemented from counts: best above 10ℓ, ours best at 2–10ℓ; ablation shows the gain over BK comes from the
  deepest c, the correction fixes BK's bias (r36). FRW drift kernel derived (sympy, r38): R is read one third of the way down,
  1 − d²_est/d² = (τ²/16)[R − (τ/3)dR/dτ + …]. Curvature estimator: the offset was a **ratio bias**, not correlated regressor noise (split test failed);
  pooling R = −16⟨β⟩/⟨α⟩ removes it for inserted pairs (−0.03 / 1.97 vs 2.07 at ρ = 4000); sprinkled shortfall 0.37 → 0.24 with density, unexplained.
  Benchmarked against Benincasa–Dowker and chain abundances: ours is **not** less noisy (3.5/2.4 vs chains 3.2/2.1). New title, Sec. V demoted to
  "a supporting diagnostic", phases wording softened.
- **Drafts and answers:** `embedding-3p1-v2.tex/pdf` (no placeholders), `toolkit-1p1-v2.tex/pdf` (placeholders: r27, Zenodo DOI);
  `answers/answer-<slug>-v2.md` point by point. Delivered to `~/Desktop/papers/3+1 PRD/` and `1+1 CQG/` for round 2.
- **Assessment (asked by Roberto):** headline claims weaker, papers more robust; 1+1 improved more; 3+1's main risk at PRD is significance.

## Mistakes
- Lesson 44: v1 read a likelihood gap as a local optimum before the optimizer had converged.
- Lesson 45: per-pair ratio estimator biased; pool numerator and denominator first.
- Lesson 46: Hu–Meyer–Meyer sat in the 1+1 outlook unbenchmarked; implemented, it beats ours above 10ℓ. Same pattern for the noise claim vs chain abundances.
- Lesson 42 recurrence: quoted the truth gap (46, up to 104) as the L-BFGS gain; corrected to 45 (up to 98) from the output file.
- First sympy derivation hung >10 min (full series); rewritten with polynomial truncation (19 s).
- de Sitter density normalization in `f_cont` was wrong (max at the bottom); fixed.
- cluster SSH from Claude denied (publickey); not needed this session.

## Open / caveats
- `r37_split.txt` is partial (job stopped for CPU contention; its conclusion — hypothesis fails — was already clear).
- v2 drafts still say the code is "openly available"; repo stays private until after submission → wording to settle before submitting.

## Next
1. Roberto runs referee round 2 on both tracks; answer as `answer-<slug>-v3.md` with v3 PDFs.
2. Fetch r27 (job 450475) → 1+1 Sec. VI `\pending`.
3. Before submission: "openly available" wording, make repo public, Zenodo DOI; Roberto's language pass; Boguñá.
