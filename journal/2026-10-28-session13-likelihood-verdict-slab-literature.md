# Session 13 — 2026-10-28: likelihood verdict at large n, slab, paper v2, off-arXiv literature pass

## What we discussed and did
- **cluster r24/r19 fetched.** Poisson-only likelihood removes **79–83 % of Johnston's residual at n = 3000–15000**, every universe (21/21): the first estimator in this
  line whose share does not shrink with n. Our binomial term costs 15–20 points at every n (lesson 37 holds at scale). Weighted fits (r19) fade. Cost ≈ Johnston's at 15000.
- **Slab (r25, laptop n = 1500):** Poisson likelihood +43 % all pairs / +69 % interior (diamond +79 / +68). Oracle wall correction → +64 / +74 %: intervals clipped by the
  side wall cost about half. Roberto: report the wall as a diagnosis, no shape-dependent correction. cluster r25 submitted at equal density (slab n = 4 × diamond n).
- **Checks (r26):** Poisson-only consistency from the truth 0.966 / 0.991 / 0.9965 (n = 400 / 1000 / 2000). Exact Poisson needs a soft "pair is related" term (else N = 0
  pairs go spacelike for free; that was the real session-12 failure, not the gradient); with it, exact = Gaussian within 0.0003, and 1000 iterations = 400.
- **Paper v2** (`paper/counting-full-v2.tex`, review ~80 %): 3+1 rewritten as one storyline (Johnston reproduced → low-count pairs are the whole error → inverted distances
  cannot fix it → Casasola's likelihood from an intrinsic start → checks, slab, cost); switch, weighted map, binomial term, counts-only map, eigenmaps, Madsen charts → App. A.
  Fig. 6 regenerated from r14 + r24. v1 and its review archived.
- **Off-arXiv literature pass** (4 parallel searches, ~200 queries, ~60 full texts; key quotes checked by me). Changes: BK24 already have the *exact* overlap inversion for
  equal depths (our "small-d approximation" sentence was wrong → lesson 38); Pellegrin 2026 (Zenodo) found the strict-count convention independently and the order-convexity
  wall mechanism; tile D = Rideout–Wallden's 1+1 naive distance; Huang 2014 / Buschmann 2006 = Euclidean overlap-count distance (MLE + Cramér–Rao); the 3π two-hop count
  follows from Johnston 2008's normalization. Bibliography: 9 entries fixed. Nothing anticipates the 1+1 claims or the 3+1 diagnosis + intrinsic-start likelihood vs Johnston.
- **F_N (449963):** 30.5 h, 72 GB ≈ 63 % by memory; ~18 h left. Not part of the counting paper (idea 004 / growth-memory line).

## Decisions (Roberto)
- Wall correction: diagnosis only. cluster r25 at equal density. F_N belongs to the growth-memory paper, not counting-full.

## Mistakes
- Lesson 38: claimed what BK24 does not do from our own old note instead of their text.
- Also corrected in-session: "fit settled by iteration 200–300" (it creeps on; but the map is stable, r26); exact-Poisson failure misattributed to the gradient.

## Next
1. Fetch r25 (and F_N when done); fill the slab placeholder (Sec. 9.3). 2. Roberto's items (affiliation details, AI statement, code URL, endorser). 3. Boguñá email.
4. F_N N = 12: test N·d ≈ 0.233 (idea 004).
