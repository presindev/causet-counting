# Referee report — Physical Review D

**Manuscript:** "Counting identities in two-dimensional causal sets: spatial distance, depth-drift curvature, and a fixed-size propagator target" (R. Bada), version v1 (dated October 29, 2026)

**Criteria applied:** the APS referee criteria used across the Physical Review family: scientific soundness and technical correctness; novelty and significance sufficient for this journal (as opposed to a less selective one); whether the conclusions are supported by the results; clarity of presentation; recommendation (accept / minor revision / major revision / reject).

**Scope note:** the N = 800 held-out test in Sec. VII is still a placeholder in v1 and is not assessed in this report.

---

## Summary

In 1+1 dimensions the author presents:

- (i) a rectangle identity, d² = 2V_A V_B / V_C, which holds for any element c in the common past of two spacelike elements, and a Poisson-bias-corrected distance estimator built on it;
- (ii) its failure in curved spacetime as a function of the depth of c, with a closed form in de Sitter, d²_est/d² = tanh²(Hτ/2)/[2 ln cosh(Hτ/2)] = 1 − Rτ²/16 + O(τ⁴), turned into a curvature estimator;
- (iii) a Laguerre identity, E[K | n] = ½ L_n(μ/2), for the mean of Johnston's propagator in intervals of fixed size;
- (iv) a calibration of the Clough–Evans embedding test, with the fraction of null-separated pairs added to catch layered orders.

These are applied to transitive percolation and to the e^{−βS} model.

## Assessment

The analysis is correct, clearly derived and candidly qualified. I verified the following and found no errors:
- the rectangle identity;
- the de Sitter volume formula, Eq. (7);
- the closed form, Eqs. (8)–(11), including its small-τ expansion and R = 2H²;
- the FRW curvature formula R = 2(ln a)''/a²;
- the fixed-n chain expectation E[c_k | n] = C(n,k)/k!;
- the Laguerre form and its Poisson average to ½J₀(mτ);
- the Hilb asymptotic.

The problem is significance and coherence. Each of the four parts is modest, and the paper says so itself in several places:
- The identity is a one-line generalization of Boguñá and Krioukov's equal-depth formula in 1+1.
- The curvature estimator is noisy (about 100 pairs for ±20%), reads low, and is not compared with existing estimators.
- The propagator target "is not stronger than the ordering fraction" as a diagnostic of manifold-likeness.
- The layering flag was designed after the test states had been seen.

Taken together, it reads as a collection of tools rather than a single advance. As written, that is the main obstacle to publication in PRD.

## Major comments

1. **Comparison with Hu–Meyer–Meyer is missing.** HMM [Ref. 12] give an exact 1+1 reconstruction from one past and one future element, which makes them the most relevant competitor in Table II. It appears only in the outlook. Please add it to Table II on the same pairs.

2. **Where the estimator's gain comes from.** In the continuum, equal-depth Boguñá–Krioukov coincides with Eq. (3). The paper says their positive bias comes from an uncorrected ratio of small counts. That means the advantage in Table II could come from the Poisson correction, the deeper choice of c, or both. Please add an ablation:
   - (a) equal-depth with the same bias correction;
   - (b) general c without it.

3. **The curvature estimator is not intrinsic and not benchmarked.**
   - The fit window, Hτ ∈ [0.2, 0.7], is chosen using H, the quantity being measured. Please define it from counts alone, for example in units of interval size, and show how sensitive the result is to that choice.
   - Compare the noise at equal density with the Benincasa–Dowker operator and with chain-abundance estimators. Without that comparison it is unclear why anyone would use this estimator.
   - The systematic low reading (an offset of about −0.5 "cannot be excluded") should be resolved or modeled.
   - Tests insert a and b by hand. Please also show results for sprinkled pairs.

4. **The value of the propagator target.** Once Sec. V concedes it does not outperform the ordering fraction, its remaining use is as a density-free check of how the chain sum is implemented. That is a useful remark, but it may belong in an appendix or a short section rather than as one of the paper's main results. Alternatively, demonstrate a concrete use, for example catching an implementation or normalization error in published code, or testing a non-sprinkled ensemble where the ordering fraction is uninformative.

5. **The "blind spot" partly comes from the test setup.** The failure on orders with about 10 layers is attributed partly to sampling only the top one or two layers. Layered orders are also detected easily by height (number of layers), ordering fraction or Myrheim–Meyer dimension, and the paper says the fixed-n ordering fraction separates the same groups. Explain why the null-pair fraction is needed at all, i.e. what it detects that these simpler statistics do not.

6. **The e^{−βS} states are not equilibrium samples.** Chains started from layered orders accept ≤ 0.1% of moves. Claims about telling the two phases apart should be framed as tests on representative configurations, which the paper partly does. The bracket 0.05 < β_c(400) < 0.45 is loose and should not be presented as a consistency check of the finite-size scaling of Glaser, O'Connor and Surya without that caveat.

7. **Missing related work.** Add work on spatial distance and induced geometry in causal sets, such as Eichhorn, Surya and Versteegen, "Induced spatial geometry from causal structure" (CQG 2019), and Major, Rideout and Surya (2006, 2007). Also give more context on curvature from small causal diamonds, for example work on boundary terms for the volume of small diamonds (Khetrapal and Surya, 2013).

## Minor comments

- Consider restructuring around one theme, such as "exact flat-space identities and their violations as diagnostics" (Secs. III–IV), and moving Secs. V–VII into a shorter section, an appendix, or a separate note. The title and abstract currently list four topics.
- Fig. 3: neighbouring depth bins are correlated at the 0.9 level. Show the correlation explicitly, or use bins that do not share elements.
- In Sec. VI, "the map to the true coordinates is a Lorentz transformation to within 3–10%" needs a precise definition: which norm, and which quantity.
- Table I and Table II use different pair selections (late elements vs the middle of the diamond). State this at the start of the tests paragraph rather than in a caption.
- Check that the citation for Hu, Meyer and Meyer is consistent. The journal year is 2025 (J. Math. Phys. 66, 122502) but the arXiv ID 2601.03280 begins 2601 (January 2026). Also check the arXiv numbers of the 2026 preprints.

## Recommendation

**Major revision, with a real chance of rejection on significance.** The results are correct, but as a PRD article the paper needs:
- (a) the Hu–Meyer–Meyer comparison and the bias-correction ablation (comments 1–2);
- (b) an intrinsic, benchmarked curvature estimator (comment 3);
- (c) a tighter structure that puts the distance and curvature results at the centre (comments 4–5).

Classical and Quantum Gravity would also be a suitable venue.

---

## Notes for the author (outside the formal report)

What to fix first, by impact:
1. The Hu–Meyer–Meyer comparison in Table II.
2. The bias-correction ablation against equal-depth Boguñá–Krioukov.
3. A curvature fit window defined from counts, and a noise comparison with Benincasa–Dowker at equal density.
4. Restructuring so that one main result leads, with the propagator target and the layering flag in secondary sections.

Estimated chance of eventual PRD acceptance: about 30–45% as written, rising to about 50–60% with points 1–4 addressed. This is a judgment call, not data. The paper may do better at CQG.
