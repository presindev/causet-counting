# Honest review — toolkit-1p1-v3 (session 18, our own assessment)

**What changed:** answers referee round 2 (comments 8–17). New runs: `sims/r40_curvature_round2.py` (select, convex, frw, noise).

**Gains**
- Comment 8: the sprinkled-pair shortfall was the nearest-element selection (strip deficit 0.2–0.4 elements, measured). Mecke-style all-pairs pooling
  removes it in dS and flat at both densities. The abstract can now claim sprinkled pairs, with the selection condition.
- Comment 14: order-only window in a causally convex region; same conclusions there.

**Losses (stated in the paper)**
- Comment 10: in one region the ordering fraction is ~3× less noisy in de Sitter and equal in flat; the in-region pooled drift keeps a low bias
  (−0.46/−0.18 dS, −0.10 flat). The curvature estimator is a geometric diagnostic, not a better estimator.
- Comment 9: the pooled FRW estimate matches its continuum fit, but that is ~30 % above the leading-order Eq. (12) over realistic windows (half higher
  orders, half finite d). Eq. (12) is a leading-order statement only.

**Weaker spots**
- The CQG "significant advance" now rests on the identity, Eqs. (11)–(12) and the ablation; the curvature estimator's practical value is modest.
- r27 (N = 800 flag test) still a placeholder: needs the fetch from cluster (Roberto).
- Region-dependent τ⁴ systematic (+2 to +4 %) not removed, only stated.

**Number checks done:** Table III, the abstract and the comment-8/9/10/14 tables are from `sims/out/r40_*.txt`; the inserted/nearest rows reproduce v2 (r37) seed for seed.

**Odds (judgment):** CQG 85–90 % if the referee accepts the noise result as an honest negative; r27 must still be filled in before submission.
