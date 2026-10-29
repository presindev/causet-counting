# Session 6 — 2026-10-25 (evening)

## What we did
- **Memory per observer (idea 004).** Session 5's global "whole past" is a stack of static patches. Per patch, the growth memory (events still needed,
  n_xf ≤ 10) is **finite and stationary**: the horizon bounds it. But it's a **spacetime-volume law** in d = 2, 3, 4 (exponent ≈ 0.97 in ρ = 1/(ℓH)^d over
  ρ = 25–400; area law would be 0 / 1/3 / 1/2). State ≈ 3ρ / 6.3ρ / 9.6ρ. The extra memory near the horizon is volume-law too.
  "Memory shared with the outside" is 100 % (killed as a definition; lesson 21). Reason: Little's law, memory = birth rate × need-lifetime (≈ 1–3 Hubble
  times, ρ-independent because of C4). An area law, if any, must come from the quantum state, i.e. from A2-quantum. Laptop only; cluster not needed.
  Code: `sims/a2_memory_static_patch.py`, `sims/a2_memory_patch_dims.py`.
- **A2 + C8, growth-path sum (idea 004).** Each newborn chooses any down-set; amplitude e^{iβΔS} per birth ⇒ A(C) = (natural labellings) × e^{iβS}: covariant, and
  the counting measure comes out of growth. Exact to N = 8 (2.8 M paths, validated). β = 0: KR-like 3-layer sector P = 0.80; a β window (βε² ≈ 0.3) suppresses it by
  interference (known: Loomis–Carlip, Carlip–Carlip–Surya); PRESENT doesn't become spacetime-like. `sims/a2_growth_paths.py`.
- **Explained (Roberto's questions):** β (≈ 1/ħ, in 3+1 ~ (ℓ/ℓ_P)²) and ε (non-locality, (ℓ/ℓ_k)^d) as model constants, to be fixed by where a continuum
  emerges (lattice-QCD logic, not anthropics); KR entropy; normalization; measure extension; the fork.
- **Branch C** = BD action family + covariance + consistency as the universe grows. Roberto's proposal: no per-step normalization, demand instead that
  **the past stabilises as N grows** (thermodynamic limit).
  - Per-step normalization: covariance violation grows with N (factor ~10 at N = 22), relative spread flat ≈ 2 %, quantum phases across birth orders decohere
    (0.18). **Killed.** `sims/a2_normalization_covariance.py`.
  - Past stability (stem questions, N ≤ 8): stable where KR dominates; swings by ~0.5 inside the window. Following the window (β*(N)) doesn't help: β* is erratic
    at small N. Inconclusive; exact sums can't go far (sign problem). `sims/a2_past_stability.py`, `sims/a2_follow_window.py`.
  - Clean criterion `[ours]`: the past is stable iff the future factor F_N(stem) (sum over continuations) becomes stem-independent as N → ∞: **the future factorizes**.

## Mistakes (now in LESSONS)
- Proposed "memory shared with the outside" as the area-law piece; session 5 already implied it's everything (lesson 21).
- Roberto counted 3 possible next births for {a→b, a→c}; it's 5 (empty past and "after both" were missing). Not a lesson, just recorded.

## Open / next
- **F_N factorization test:** compute F_N(X)/F_N(Y) for small stems X, Y as N grows (one stem's futures at a time).
- **N = 400 analysis** (cluster job 449411, should be done ~14:40 on 2026-10-26).
- Quantum memory: what is the dimension of the quantum state a patch needs? (A2-quantum must deliver a sub-volume law for holography.)
- (β, ε) map of "KR suppressed ∧ manifold-like" vs N; N = 9–10 via unlabelled posets (needs a generator; cluster).
- Draft v4 doesn't include session 6; fold into v5 once branch C has a result.
