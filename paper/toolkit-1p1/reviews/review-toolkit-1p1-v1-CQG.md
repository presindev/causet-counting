# Referee report — Classical and Quantum Gravity

**Manuscript:** "Counting identities in two-dimensional causal sets: spatial distance, depth-drift curvature, and a fixed-size propagator target" (R. Bada), version v1 (dated October 29, 2026)

**Criteria applied:** CQG describes Research Papers as "reports of high-quality original research with conclusions representing a significant advance in the field". The IOP referee assessment covers:
- originality;
- significance;
- scientific soundness;
- whether the conclusions are supported;
- clarity of presentation;
- appropriate referencing;
- suitability for the journal's readership.

The recommendation is one of accept, minor revision, major revision or reject. CQG also publishes Notes ("brief articles that make a short, interesting point"), which matters for one of the comments below.

**Scope note:** the N = 800 held-out test in Sec. VII is still a placeholder in v1 and is not assessed in this report.

---

## Summary

In 1+1 dimensions the author presents:

- (i) a rectangle identity, d² = 2V_A V_B / V_C, which holds for any element c in the common past of two spacelike elements, and a Poisson-bias-corrected distance estimator built on it;
- (ii) its failure in curved spacetime as a function of the depth of c, with a closed form in de Sitter, d²_est/d² = tanh²(Hτ/2)/[2 ln cosh(Hτ/2)] = 1 − Rτ²/16 + O(τ⁴), turned into a curvature estimator;
- (iii) a Laguerre identity, E[K | n] = ½ L_n(μ/2), for the mean of Johnston's propagator in intervals of fixed size;
- (iv) a calibration of the Clough–Evans embedding test, with the fraction of null-separated pairs added to catch layered orders.

These are applied to transitive percolation and to the e^{−βS} model.

## Suitability for CQG

The paper fits CQG's readership well. Much of the work it builds on was published in this journal:
- Johnston's propagator;
- Henson's embedding;
- Rideout–Wallden;
- the 2D-orders papers of Brightwell, Henson and Surya, Surya, and Glaser, O'Connor and Surya;
- Cunningham's work on boundaries;
- Cunningham and Surya.

The causal-set community reads CQG, and that community values careful kinematic tools in 1+1 dimensions more than a general physics readership would. Methodological work of this type is a normal CQG contribution.

## Assessment

**Soundness.** I verified the following and found no errors:
- the rectangle identity;
- the de Sitter volume formula, Eq. (7);
- the closed form, Eqs. (8)–(11), including its small-τ expansion and R = 2H²;
- the FRW curvature formula R = 2(ln a)''/a²;
- the fixed-n chain expectation E[c_k | n] = C(n,k)/k!;
- the Laguerre form and its Poisson average to ½J₀(mτ);
- the Hilb asymptotic.

The numerical work is well controlled. Uncertainties come from the spread between independent sprinklings, and the selection bias in choosing c is identified and removed in Table II. Limitations are stated candidly.

**Originality and significance.** The strongest parts are the general-c rectangle identity with its bias-corrected estimator (Sec. III) and the depth-drift curvature result (Sec. IV). The closed form of Eq. (11) is a clean and, as far as I know, new statement: in 1+1 dimensions, curvature appears as the failure of an exact flat-space identity, as a function of depth. That is a reasonable core for a CQG paper.

The two secondary results are weaker, and the paper says so:
- The propagator target "is not stronger than the ordering fraction" as a diagnostic of manifold-likeness.
- The layering flag was designed after the test states had been seen, and the fixed-n ordering fraction separates the same groups.

The main obstacles to a clear case for a "significant advance" are:
- the curvature estimator is not compared with existing estimators;
- the most relevant competing 1+1 distance construction (Hu–Meyer–Meyer) is missing from the comparison;
- the paper is spread over four loosely connected results.

## Major comments

1. **Comparison with Hu–Meyer–Meyer is missing.** HMM [Ref. 12] give an exact 1+1 reconstruction from one past and one future element, which makes them the most relevant competitor in Table II. It appears only in the outlook. Readers in this community will expect it in Table II, on the same pairs.

2. **Where the estimator's gain comes from.** In the continuum, equal-depth Boguñá–Krioukov coincides with Eq. (3). The paper says their positive bias comes from an uncorrected ratio of small counts. That means the advantage in Table II could come from the Poisson correction, the deeper choice of c, or both. Please add an ablation:
   - (a) equal-depth with the same bias correction;
   - (b) general c without it.

   This is what shows whether the identity itself, and not only the correction, improves the estimator.

3. **The curvature estimator: intrinsic definition and benchmark.** This is the result most likely to interest CQG readers, so it deserves the most care.
   - The fit window, Hτ ∈ [0.2, 0.7], is chosen using H, the quantity being measured. Please define it from counts alone, for example in units of interval size, and show how sensitive the result is to that choice.
   - Compare the noise at equal density with the Benincasa–Dowker operator and with chain-abundance estimators (Roy–Sinha–Surya). Without this, the claim that the method is "geometrically transparent" is its only advantage.
   - The systematic low reading (an offset of about −0.5 "cannot be excluded") should be resolved or modeled. The paper identifies the factor 1 − e^{−λ_C} in the shallowest bins as one candidate.
   - Tests insert a and b by hand. Please also show results for sprinkled pairs.
   - The FRW test finds that the estimator measures a depth-weighted average of R. Deriving the weighting kernel, or at least its leading form, would turn an observation into a result.

4. **Focus and structure.** The paper presents four results of very different strength under one title. For CQG I suggest:
   - building the paper around Secs. III–IV, i.e. exact flat-space identities and how their failure measures curvature;
   - keeping the embedding calibration (Sec. VI) as a supporting diagnostic;
   - reducing the propagator target (Sec. V) to a short section or appendix framed as a density-free check of how the chain sum is implemented.

   If the author prefers to keep the Laguerre identity prominent, it could make a short CQG Note of its own. In that case it should show a concrete use, for example catching a normalization error in an implementation, or testing an ensemble where the ordering fraction is uninformative.

5. **Why the null-pair fraction is needed.** The failure on orders with about 10 layers is attributed partly to sampling only the top one or two layers. Layered orders are also detected easily by height, ordering fraction or Myrheim–Meyer dimension. Explain what the null-pair fraction adds. One answer could be that it repairs the embedding test so the test can be used alone; if that is the argument, make it explicitly.

6. **The e^{−βS} states.** Chains started from layered orders accept ≤ 0.1% of moves, so the states are test configurations, not equilibrium samples. The paper says this, but the abstract's claim that the diagnostics "separate the continuum-like and layered phases" should be worded the same way. The bracket 0.05 < β_c(400) < 0.45 is too loose to count as a consistency check of the finite-size scaling in Glaser, O'Connor and Surya. Present it as a statement of compatibility only.

7. **References.** CQG referees in this field will expect:
   - work on spatial distance and induced geometry in causal sets: Eichhorn, Surya and Versteegen, "Induced spatial geometry from causal structure" (CQG 2019), and Major, Rideout and Surya (2006, 2007);
   - work on curvature and boundary contributions in small causal diamonds, e.g. Khetrapal and Surya (2013), next to Roy–Sinha–Surya;
   - a short discussion of the 2D-orders literature on observables that distinguish the phases, beyond the graph-observables reference [32].

## Minor comments

- Fig. 3: neighbouring depth bins are correlated at the 0.9 level. Show the correlation explicitly, or use bins that do not share elements.
- In Sec. VI, "the map to the true coordinates is a Lorentz transformation to within 3–10%" needs a precise definition: which norm, and which quantity.
- Table I and Table II use different pair selections (late elements vs the middle of the diamond). State this at the start of the tests paragraph rather than in a caption.
- The abstract lists four topics plus applications. Shorten it to lead with the identity, the estimator and the curvature result.
- Check that the citation for Hu, Meyer and Meyer is consistent. The journal year is 2025 (J. Math. Phys. 66, 122502) but the arXiv ID 2601.03280 begins 2601 (January 2026). Also check the arXiv numbers of the 2026 preprints.
- Data availability: in line with IOP's research data policy, archive the code repository with a persistent identifier (e.g. a Zenodo DOI for the tagged version used in the paper), not only a GitHub URL.
- The manuscript is typeset in REVTeX/Physical Review style. Check that the references and front matter follow IOP style for the final version.

## Recommendation

**Major revision.** The results are correct, the topic is central to CQG's readership, and the depth-drift result is a good core for a CQG paper. Before I could recommend acceptance, the paper needs:
- (a) the Hu–Meyer–Meyer comparison and the bias-correction ablation (comments 1–2);
- (b) an intrinsic definition of the curvature estimator and a noise comparison with existing estimators (comment 3);
- (c) a tighter structure that puts Secs. III–IV at the centre (comment 4).

With these, I expect the paper to be acceptable.

---

## Notes for the author (outside the formal report)

**Differences from the PRD report.** The technical comments are the same; how they are weighed differs:
- CQG is the home journal of this subfield, so venue fit and readership are an asset here, not a risk.
- A specialist audience is more willing to accept a methods paper. The biggest risk is no longer "too narrow for the journal". It is that the referee, who will likely be a causal-set specialist, asks for the missing comparisons and literature.
- CQG's Notes format offers a natural home for the Laguerre identity if it is cut from the main paper.

What to fix first, by impact:
1. The Hu–Meyer–Meyer comparison in Table II.
2. A curvature fit window defined from counts, and a noise comparison with Benincasa–Dowker at equal density.
3. The bias-correction ablation against equal-depth Boguñá–Krioukov.
4. Restructuring around Secs. III–IV.
5. The missing references on induced spatial geometry and small diamonds.

Estimated chance of eventual CQG acceptance: about 55–70% as written, and about 75–85% with points 1–4 addressed. This is a judgment call, not data.
