# Session 18 — 2026-10-30 (evening): external referee round 2 answered (3+1 PRD, 1+1 CQG)

## What we did
Both round-2 reports recommended minor revision. Every numbered comment answered; v3 PDFs, latexdiff PDFs (latexdiff installed via brew) and
answers delivered to `~/Desktop/papers/{3+1 PRD,1+1 CQG}/`. Copies of the reports in each paper's `reviews/`, honest reviews `REVIEW-*-v3-2026-10-30.md`.

**3+1 (r39, on the r35 outputs, laptop):**
- Truth-started fit has higher lnL in 9/10 (n = 3000) and 10/10 (n = 6000) universes, by 0.9 / 2.3 on average.
- Aligned (O(3) about the time axis) the two maps differ by 0.63 / 0.48 ℓ. The straight path dips 2.7×10³–1.3×10⁴ (averaging shrinks distances), but
  midpoint relaxations converge to intermediate maps (86 % / 89 % removed) within O(1) of both ends: a curved valley, not a barrier.
- Continued L-BFGS (2000 it) gains +0.5 / +2.4 lnL with C unchanged. Wording now the referee's: "maps of very different accuracy differ in lnL by only O(1)".
- Recommended variant: exact Poisson, near-cone (72/76/82 %, 10/10 over the paper's fit at 3000 and 6000); near-cone share 0.47/0.37/0.30/0.27 at
  n = 3000–15000; estimated wall time ≈ Johnston at n = 10000, 2× faster at 15000 (estimate, not a node run).
- Fig. 2 numbers recomputed on its own set; figure full width. Johnston Table IV: 8 candidates, none matches (closest 0.969 vs 0.977).

**1+1 (r40, laptop, 10 workers):**
- Sprinkled-pair shortfall = nearest-element (Palm) selection, as the referee guessed (strip deficit 0.2–0.4 elements). One uniform pair per window only
  halves it (1/N_W weighting); all pairs in windows (Mecke) removes it: 1.91 ± 0.10 / 2.02 ± 0.06 vs 2.08; flat 0.00 / −0.01.
- Order-only window in a causally convex region (past of f cut at η = −3): same conclusions; target 2.03–2.04 (τ⁴ systematic is region-dependent).
- FRW p = 1 pooled: matches its continuum fit within 1σ, but that fit is ~30 % above Eq. (12) (half higher orders, half finite d = 14ℓ).
- Realistic noise: in one dS diamond the ordering fraction has ~1/3 the spread of the pooled drift (flat: equal), and the in-region drift reads low.
  Stated plainly in abstract and Limitations.
- Kernel = first moment only; τ⁴ systematic stated; Glaser refs completed (INSPIRE); version references removed.

## Mistakes
- Lesson 49: `spatial_dist` expects (t, x) columns; fed spatial maps it dropped a coordinate (C = 0.76). Caught against the recorded C.
- Lesson 47: a 300-iteration relaxation cap left one midpoint 7×10³ low and looked like a barrier; reran to convergence.
- Overwrote `fig_3p1_errloc.pdf` (v2's figure) by regenerating it; restored from git, new figure is `fig_3p1_errloc_v3.pdf`.
- v2 printed the fit's 99th percentile at n = 3000 as 0.6 (it is 0.65); now 0.7.

## Open / next
1. Roberto: send round 3 (v3) to the referee sessions.
2. Fetch r27 (job 450475) → 1+1 Sec. VI placeholder (cluster ssh from Claude still not set up).
3. Optional: time the near-cone exact variant on the cluster (replaces the Sec. VII estimate); slab with more universes (3+1 comment 14b).
4. Before submission: repo public + Zenodo DOI; "openly available" wording; Roberto's language pass.
