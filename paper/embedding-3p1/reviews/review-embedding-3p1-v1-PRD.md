# Referee report — Physical Review D

**Manuscript:** "Spatial embedding of 3+1 causal sets: low-count spacelike pairs and a likelihood fit to interval counts" (R. Bada), version v1 (dated October 30, 2026)

**Criteria applied:** the APS referee criteria used across the Physical Review family: scientific soundness and technical correctness; novelty and significance sufficient for this journal (as opposed to a less selective one); whether the conclusions are supported by the results; clarity of presentation; recommendation (accept / minor revision / major revision / reject).

---

## Summary

The author reproduces Johnston's 3+1 embedding benchmark [PRD 111, 106020 (2025)]. Using oracle substitutions, they show that almost all of its remaining error comes from spacelike pairs whose shared causal regions contain fewer than about 10 elements, and that these pairs sit mostly at the waist of the diamond. They then fit spatial coordinates to the interval counts of all related pairs, using a Poisson likelihood (Casasola's) started from a weighted SMACOF map of causal-overlap distances. On 21 sprinklings from n = 3000 to 15000, the fit improves on Johnston in every universe and removes 79–83% of his residual. A cylinder region with no waist shows a smaller gain, which the author traces to intervals cut off at the timelike boundary.

## Assessment

The work is careful and honest. The comparison is paired on the same universes, and the oracles separate cleanly where the error comes from. Settings were fixed on separate universes, the result does not depend on the starting map, and the Gaussian and exact Poisson forms were compared. The cost section admits the method is slower than Johnston's at every size tested. The improvement is clear and consistent, not marginal. PRD published the benchmark paper, so the venue fits. My main concerns are the case for physical significance and the small number of universes. Neither is fatal.

I checked the scaling argument of Eq. (3): a shell of thickness ~d on a null cone of height τ has 4-volume ~dτ³, and at fixed shape this gives δd/d ∝ n^(−1/2). I also checked the error model behind Eq. (4): N ∝ τ⁴ gives δ(τ²)/τ² = δN/2N. I found no errors.

## Major comments

1. **Why it matters physically.** The paper shows that accuracy improves, for example C from 0.9886 to 0.9980, but does not say what a better flat-space embedding makes possible. Possible answers include tests of whether a causal set is manifold-like, the induced geometry on spatial hypersurfaces, or a route to measuring curvature. PRD referees weigh significance, so the introduction and discussion should answer this directly. As written, a referee could call the paper a numerical-methods improvement on one benchmark.

2. **Statistics.** At n = 3000 there are 2 universes and at n = 1000 only 1, and Table II itself says its errors are "only indicative." Runs at n ≤ 6000 are cheap. I would ask for at least 10 universes per size up to 6000, and for the spread of the removed fraction across universes, not only its mean.

3. **What the paper adds over Casasola.** The claimed additions are the intrinsic starting map, the use of all related pairs, and the large-n comparison. An ablation should show that "all related pairs" matters. One option is to run Casasola's near-light-cone pseudo-likelihood (τ² < 6ℓ²) from the same intrinsic start and compare it with the full likelihood.

4. **The optimizer finds a local optimum.** Fits started from the true positions reach higher log-likelihoods (by 105–109 at n = 3000 and by 228–549 at n = 6000), so the remaining error comes partly from optimization and not from the likelihood itself. Please explain why there is no multi-start, annealing or second-order refinement (for example L-BFGS after Adam), and whether the 79–83% figure is limited by the method or by the optimizer.

5. **Time coordinate held fixed.** Not refitting the time coordinate is a natural limitation. Even an exploratory joint fit of time and space, or a clear argument that it would not change the conclusions, would help. The paper does note that using the true time coordinate changes the result little.

6. **Missing related work.** Researchers in this area will probably expect work on spatial distance and induced spatial geometry from thickened antichains to be cited and discussed. Examples are Major, Rideout and Surya, "Spatial hypersurfaces in causal set cosmology" (CQG 2006) and "On recovering continuum topology from a causal set" (J. Math. Phys. 2007), and Eichhorn, Surya and Versteegen, "Induced spatial geometry from causal structure" (CQG 2019).

## Minor comments

- The normalization of s_ab, typeset as `(2√N_ab+1)`, is ambiguous; add parentheses, e.g. `2√(N_ab + ½)`. A constant rescaling does not change the fitted maximum, but the notation should be unambiguous.
- The labels for the sets of sprinklings, (a)/(b)/(b′)/(c), plus separate development sprinklings, make the paper hard to follow. A small table listing each set (seeds, sizes, number of universes, time coordinate used, sections where it is used) would help.
- The abstract has too many numbers. Keep the headline result: errors roughly halve and about 80% of the residual is removed.
- Add a figure showing where the error is located (by position in the diamond, or by k) and per-pair error histograms for Johnston versus the fit. The paper's main diagnostic claim (low-count pairs at the waist) currently has no figure.
- The mismatch with Johnston's Table IV (0.82/0.90/0.93 vs 0.958/0.977/0.985) should be resolved with him if possible, not left as a "suspected" difference in statistic.
- Sec. VI changes Johnston's method (four-leg fallback detours in the slab). State explicitly that this modification is needed to make his method applicable there, and that it does not disadvantage him.
- Key prior results come from preprints that have not been peer reviewed (Casasola on Research Square, Pellegrin on Zenodo). This is acceptable, but give stable identifiers and state which results are taken from them.
- Check that the citation for Hu, Meyer and Meyer is consistent. The journal year is 2025 (J. Math. Phys. 66, 122502) but the arXiv ID 2601.03280 begins 2601 (January 2026). Also check the arXiv numbers of the 2026 preprints (e.g. arXiv:2610.36695).

## Recommendation

**Minor-to-major revision.** The results are sound and the improvement over the current benchmark is clear. I would expect a positive outcome if the significance case is strengthened (major comment 1), more universes are added (2), and the contribution relative to Casasola is shown by an ablation (3).

---

## Notes for the author (outside the formal report)

What to fix first, by impact:
1. More universes, at least 10 per size for n ≤ 6000.
2. A paragraph on why the embedding matters physically, in the introduction and discussion.
3. The Casasola ablation, to show that using all related pairs matters.
4. An optimizer check: multi-start or second-order refinement.
5. The missing references on thickened antichains.

Estimated chance of eventual PRD acceptance: about 60–75% as written, higher with points 1–3 addressed. This is a judgment call, not data.
