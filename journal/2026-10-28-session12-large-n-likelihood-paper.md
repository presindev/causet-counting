# Session 12 — 2026-10-28: large-n verdict, waist pairs, likelihood embedding, full paper

## What we discussed and did
- **cluster r14/r17 fetched.** Switch removes a flat ~20 % of Johnston's residual at n = 3000–15000 (session-11 "grows with n" corrected). Counts-only map (c) loses at
  n ≥ 6000: killed as competitor. Convergence argument (per-pair median error ∝ n^{-1/2}); like-for-like slopes ours n^{-0.54} vs his n^{-0.42} (an unlike comparison caught).
- **Waist diagnostic (r18):** low-count pairs are the whole gap (oracle on k < 10 pairs: 88–96 % of his residual); count-weighted SMACOF doubles the switch.
- **Roberto's questions → tests:** interior of the diamond (r20, with Madsen local trilateration: validated, not competitive at n ≤ 3000); Laplacian eigenmaps (BK24's
  suggestion, r21: capped ~0.93 even on true distances, killed); slab (r22: Johnston strong there, switch gain 0, weighted K100 +24–33 %).
- **Likelihood embedding (r23):** start-independent, consistent. **Ablation:** related-pair Poisson term alone +74–76 % of his residual at n = 1500/3000; adding our
  binomial overlap term HURTS (+61–64 %). Deep literature review: Casasola 2026 (Research Square, not arXiv) already has the Poisson count likelihood (from true±ℓ starts);
  Sim 2021, Boguñá et al. 2010 / Mercator, Ramsay, Hoff are the general precedents. Ours: intrinsic start, all related pairs, the Johnston benchmark and diagnosis.
- **Madsen 2026 read in full:** local Lorentzian trilateration + profile distance (cite next to our overlap estimator); pure theorems.
- **Paper:** full paper `paper/counting-full-v1.tex` (1+1 + 3+1, review ~70 %); methodology promoted to Sec. 2 (SapereIA + ICCUB affiliations, LVK note, timeline,
  roles, checks, mistakes, limits); stronger Boguñá–Krioukov credit; 1+1 note archived.

## Decisions (Roberto)
- Full paper (not a separate 3+1 note); one storyline rewrite after the cluster results. Methodology section given prominence. Boguñá email after the paper.
- Order: likelihood (done) → r19/r24 verdict → slab at large n and equal density. Periodic space and curved backgrounds → paper 2 (ROADMAP §5).

## Mistakes (now in LESSONS)
- Lesson 37: presented the likelihood gain as resting on our binomial term before ablating; the Poisson term (Casasola's) carries it and ours hurts.
- Also corrected in-session: "relative gain grows with n" (it plateaus), unlike per-pair slopes, "waist pairs are a few" (they are 31–50 %), caveat 3 (empty in flat space),
  macOS tar flag order.

## Waiting on the cluster
r24 450199–450203 (poisson_only + both, 22 universes, n = 3000–15000); r19 450117–450121; extra universes r14 450135/450137, r19 450136/450138; F_N 449963 (N = 12).
Fetch: combined command in compute.md (r24 entry). Then analyse r19 and r24 against r14.

## Next
1. Fetch + verdict at large n (does Poisson-only keep ~75 %?). 2. Slab with a tip-free Poisson likelihood, larger n, equal density. 3. Rewrite the 3+1 storyline
(Johnston reproduced → where his error lives → Poisson likelihood from an intrinsic start, credited → checks; switch, weighted fit, binomial term, eigenmaps, Madsen
charts to "paths dropped"); refresh the review. 4. Roberto's items. 5. Boguñá email.
