# Honest review — embedding-3p1-v3 (session 18, our own assessment)

**What changed:** answers referee round 2 (comments 7, 9–14). New runs: `sims/r39_3p1_round2.py` (on the r35 outputs).

**Main point (comment 7) — now correct and sharper.** The truth-started fit has higher lnL in 9/10 (n = 3000) and 10/10 (n = 6000) universes, by O(1).
The two maps are joined by a curved valley: the straight path dips by 10³–10⁴ (shrinkage of averaged maps), but midpoint relaxations converge to
intermediate-accuracy maps within O(1) of both ends. Continued L-BFGS gains as much lnL as separates the maps (n = 6000: +2.4) with no change in C.
The paper now uses the referee's wording. Risk: a referee may ask for a proper minimum-energy path (nudged elastic band); the relaxation test is
convincing but not a full path.

**Weaker spots that remain**
- Novelty is narrower than v1 (likelihood = Casasola's, near-cone set = Casasola's; the recommended variant is his exact form). The contribution is the
  oracle diagnosis, the intrinsic start, the benchmark, and the likelihood-geometry finding. PRD significance remains the main risk.
- Cost of the recommended variant is an *estimate* (laptop per-iteration ratios applied to node timings). A real timing run on the cluster would be cheap.
- Slab comparison still rests on 3–4 universes per size (comment 14b declined for lack of cluster access this session).
- Johnston's Table IV still unexplained.

**Number checks done:** abstract vs Table III and `sims/out/r35_analyse_all.txt` (one rounding fixed: 99th percentile 0.65 → 0.7, v2 had 0.6);
r39 recomputed lnL agrees with the r35-recorded values to 10⁻³; errloc numbers from `sims/out/r39_summary_n*.txt`.

**Odds (judgment, not data):** PRD acceptance roughly as the referee's 70–80 % after these fixes; the remaining risk is "incremental over Johnston + Casasola".
