# Referee report — Classical and Quantum Gravity (second round)

**Manuscript:** v2 retitled "Spatial distance and curvature from an exact counting identity in two-dimensional causal sets" (R. Bada), dated October 30, 2026 (v1: "Counting identities in two-dimensional causal sets: spatial distance, depth-drift curvature, and a fixed-size propagator target"), with the author's response `answer-toolkit-1p1-v2.md`.

**Criteria applied:** CQG Research Papers are "reports of high-quality original research with conclusions representing a significant advance in the field". The IOP referee assessment covers:
- originality;
- significance;
- scientific soundness;
- whether the conclusions are supported;
- clarity of presentation;
- appropriate referencing;
- suitability for the journal's readership.

The recommendation is one of accept, minor revision, major revision or reject. IOP's research data policy also applies (persistent identifier for code).

**Scope note:** the response lists two placeholders, which are not assessed in this report:
- the N = 800 held-out test of the null-pair flag in Sec. VI (`[r27: …]`);
- the Zenodo DOI in the Data availability statement.

---

## Summary

The paper has been restructured as suggested. It is now built on one exact 1+1 identity, d² = 2V_A V_B / V_C for any c in the common past, and on its use for distance and for curvature:
- The distance estimator is compared on the same pairs with the equal-depth construction of Boguñá–Krioukov, a counting version of Hu–Meyer–Meyer, and the past–future interval, with two ablations.
- The curvature section has:
  - a fit window defined from counts alone;
  - a pooled estimator, R = −16⟨β⟩/⟨α⟩, which removes the v1 low offset;
  - tests with sprinkled as well as inserted pairs;
  - a noise comparison with Benincasa–Dowker and with the ordering-fraction (chain-abundance) route;
  - a new leading-order FRW result, Eq. (12): to first order the drift measures R one third of the way from the pair down to c.
- The embedding test is now a supporting diagnostic.
- The propagator identity is in an appendix.
- The e^{−βS} application is worded as test configurations.

## Assessment

The revision is thorough and honest. Several requested checks went against the paper, and the text now says so plainly:
- Hu–Meyer–Meyer's construction, read from counts, is more accurate above about 10ℓ;
- the curvature estimator is not less noisy than the chain-abundance route at equal density;
- with sprinkled pairs the estimator still reads low in de Sitter space.

The ablation cleanly separates where the gain over Boguñá–Krioukov comes from. The correction removes their bias; the freedom to use the deepest c, which the identity provides, removes their larger error. This is exactly what was needed to show that the identity, not only the correction, matters.

**Soundness.** I checked the new analytic content.
- **Eq. (12).** I re-derived it independently by a symbolic series expansion. Setup: a = e^{σ(η)}, V_A = V_B = h∫₀ᵀ e^{2σ(η₀−s/2)} ds, V_C = ½∬ e^{2σ(η₀−(s+r)/2)}, d = 2he^{σ(η₀)}, τ = ∫₀ᵀ e^{σ(η₀−s)} ds. Result: 1 − d²_est/d² = (τ²/16)[R − (τ/3) dR/dτ] holds exactly through order τ³, with R = 2σ''e^{−2σ}, and the residual begins at τ⁴. The quoted p = 1 numbers also follow from R = −2/η⁴ and dR/dτ = (8/η⁵)/η at η₀ = 1.5: −0.3997, −0.4068, −0.4185, and R = −0.395.
- **Pooling argument.** E[β/α] ≈ E[β]/E[α] − Cov(α,β)/E[α]² + …, so anticorrelated fit errors bias the single-pair R = −16β/α low. This matches the sign of the observed offset, including in flat space.
- **Mean depth.** The mean depth of the weight 2(τ − s)/τ² is τ/3, as stated.
- **Eq. (6).** The conformal weight in light-cone coordinates, dV = 2 du dv/[H²(u+v)²], is correct.
- **Benincasa–Dowker.** R = −2B_ε[1] is the right normalization of the 2D operator acting on a constant field.

I found no errors.

**Significance.** The analytic core, the exact identity together with Eqs. (11) and (12), is a clean and, as far as I know, new statement about how curvature appears as the failure of a flat-space counting identity in 1+1 dimensions. It is a suitable core for a CQG paper. As a practical curvature estimator the method is now honestly shown to be competitive but not superior. That is acceptable for a methods paper in this journal, provided that the remaining tests are run with the final estimator (new comments 8–10).

---

## Status of first-round comments

| # | Comment (v1) | Status | Reason (checked in v2 text) |
|---|---|---|---|
| M1 | Hu–Meyer–Meyer missing from Table II | **Resolved** | A counting version is in Table II on the same pairs; three variants were tried and the best one is reported. The claims are restricted accordingly in the abstract, Sec. III, Limitations and Outlook. |
| M2 | Ablation: correction vs choice of c | **Resolved** | Two ablation rows in Table II; the conclusion in Sec. III follows from them. The equal-depth no-estimate rate (10–30 %) is reported. |
| M3 | Curvature estimator: intrinsic window, benchmark, offset, sprinkled pairs, kernel | **Partially resolved** | (a) Window from counts, with a sensitivity scan: resolved. (b) BD and ordering-fraction comparison: done, with an honest negative result; but see new comment 10. (c) Offset traced to ratio bias and removed by pooling: resolved for inserted pairs (sign verified above). (d) Sprinkled pairs: done, but they still read low by 0.24–0.37 and the cause is not identified; see new comment 8. (e) FRW kernel: resolved, Eq. (12) verified. However, the only FRW sprinkling test still uses the v1 estimator (new comment 9). |
| M4 | Focus and structure | **Resolved** | New title and abstract; Sec. V is "A supporting diagnostic"; the propagator target is in Appendix A, which opens by stating its limited role. Not splitting off a Note is the author's choice and is fine. |
| M5 | Why the null-pair fraction is needed | **Resolved** | "What z adds" says explicitly that z detects nothing the other statistics miss; its role is to make the embedding test usable on its own. |
| M6 | e^{−βS} states, β_c bracket | **Resolved** | Removed from the abstract; "test configurations … not equilibrium samples"; the bracket is "compatible … too loose to test it". |
| M7 | References | **Resolved** (two journal references to complete) | MRS 2006/2007, ESV 2019, Khetrapal–Surya 2013 and the 2D-orders phase literature [16–18, 28, 39] are added and discussed in Sec. V. On completing [16] and [17], see minor comment 16. |
| m1 | Fig. 3 correlated bins | **Resolved** | Correlations are given in the text and the caption warns. Keeping shared bins is justified, and the estimator does not use the bins. |
| m2 | "Lorentz transformation to within 3–10 %" | **Resolved** | Defined as max |(AᵀηA − η)_ij| = 0.03–0.10. |
| m3 | Table I vs II pair selections | **Resolved** | Stated at the start of "Tests" and in the Table I caption. |
| m4 | Shorten abstract | **Resolved** | Leads with the identity, the estimator and the curvature result. It is still long; see minor comment 12. |
| m5 | HMM citation / 2026 arXiv numbers | **Resolved; comment withdrawn** | I checked the arXiv record. arXiv:2601.03280 was submitted on 31 Dec 2025 and lists J. Math. Phys. 66, 122502 (2025), DOI 10.1063/5.0290407. The citation is correct. |
| m6 | Persistent DOI for code | **Placeholder, not assessed** | The author commits to a Zenodo DOI on submission. |
| m7 | IOP style | **Deferred to final version; acceptable** | |

---

## New major comments

8. **Sprinkled pairs read low: a likely cause and a test.** With sprinkled pairs, the pooled estimator reads 1.70 ± 0.11 and 1.84 ± 0.07 against a target of 2.07, and −0.07 and −0.04 in flat space. Since sprinkled pairs are the case that matters in practice, this is the most important open point of the paper. I suggest one candidate cause.
   - **The suspected bias.** a and b are chosen as "the sprinkled elements nearest to the two target points". By construction, this selects elements with an empty neighbourhood, because the nearest point lies at the centre of an excluded region. The strips A and B touch a and b, so their shallow ends are depleted by a roughly fixed number of elements.
   - **Why it would bias R low.** N_A grows with the depth of c, so the relative deficit is largest for shallow c. That lowers d̂² preferentially at small τ, which tilts the fitted slope β upward and therefore gives R = −16β/α low.
   - **Why it fits the data.** The effect would shrink with density, as observed, and would act with the same sign in flat space, as observed.

   A clean test: choose a and b uniformly among the sprinkled elements in a target window. By the Slivnyak–Mecke property this is unbiased, and it is also what a user would do on a real causal set. Alternatively, exclude the elements of the strips within a few ℓ of a and b. If the shortfall disappears, the estimator is unbiased in practice, and the abstract can say so. If it does not, the abstract should report the sprinkled-pair result next to the inserted-pair one. At present it mentions only "inserted pairs".

9. **The FRW sprinkling test uses the superseded estimator.** The p = 1 FRW test (Sec. IV, after Table III) still reports "the window of version 1" and "the mean of single-pair fits (version 1, before pooling)": −1.25 ± 0.30 against −0.81 for the continuum fit. By the paper's own analysis, this estimator is biased low by the ratio bias, which is the same direction as the discrepancy. So the sentence "the estimator measures a depth-weighted curvature, as Eq. (12) says" is not supported by this test.
   - Please rerun it with the pooled estimator and the count-defined window.
   - Compare with the continuum fit on the same elements.
   - Compare also with the Eq. (12) prediction. The window spans R from −0.4 to −2.8, so this also shows how far the leading-order kernel can be trusted over a realistic window.

   This is the only test of Eq. (12) on sprinklings, so it should use the final method.

10. **Noise comparison at equal input, for the estimator as it would be used.** The comparison in Sec. IV is between one pair (s.d. 3.5 / 2.4) and one diamond (3.2 / 2.1). But a single pair is biased (ratio bias) and is not the estimator the paper proposes. The pooled estimator in Table III draws one pair from each of 1000 independent sprinklings, which is not how it would be used either. Please show, on one sprinkled region at given ρ and size:
    - the pooled estimator from P pairs in that region, with P around the ~100 the paper says is needed, its error estimated from the spread between sprinklings, since pairs within one region share elements;
    - the ordering-fraction curvature estimate from the same region.

    This is the comparison a reader needs to choose between the routes. It may well favour the ordering fraction, which the paper can say. As it stands, "not less noisy" is stated for a configuration nobody would use.

## New minor comments

11. **Eq. (12) and the "triangular weight".** The leading-order result fixes only the first moment of the depth kernel (mean depth τ/3). The triangular weight 2(τ − s)/τ² is one kernel with that mean, not one the expansion determines. Please phrase it as an illustration, or derive the kernel to all orders in the depth if possible.
12. **Abstract.**
    - "more accurate than the equal-depth and past–future constructions below about ten discreteness lengths" suggests that the equal-depth estimator wins above 10ℓ. Table II shows the rectangle estimator ahead of it at all separations; only Hu–Meyer–Meyer overtakes it there.
    - At N = 1000 and 2ℓ–10ℓ, ours and HMM are essentially tied in error (0.095 vs 0.098).
    - Please rephrase, and consider whether "unbiased curvature estimator on sprinklings with inserted pairs" should also give the sprinkled-pair result (see comment 8).
13. **The τ⁴ systematic.** With the count-defined window reaching Hτ ≈ 1, the estimator's target is R_fit^cont = 2.07–2.08, not R = 2. In practice R_fit^cont is not known, so this is a +3–4 % systematic of the method that depends on the size of the region. Please state it as such in Limitations. Alternatively, remove it by adding a τ⁴ term to the fit or by capping the window in units of the counts.
14. **Is the window intrinsic?** "Down to the deepest c whose rectangle lies in the sprinkled region": please say how this condition is decided from the order alone, for example by requiring that the join of a and b, or an element in its future, be present. Otherwise the window still uses the coordinates.
15. **Version history in the manuscript.** "version 1 of this paper could not exclude", "the window of version 1" and "(version 1, before pooling)" refer to a version the reader has not seen. Move these to the response, or, if v1 is public, to one footnote.
16. **References.**
    - [17] (Glaser, Ising model coupled to 2d orders) appeared in Class. Quantum Grav. 35, issue 8 (2018), DOI 10.1088/1361-6382/aab139. Please add the article number.
    - Please check whether [16] (Glaser–Surya, arXiv:1410.8775) has a journal version.
17. **Typesetting.** In Sec. V, "What z adds." runs on inside the "Null-pair fraction" paragraph; start a new paragraph.

## Recommendation

**Minor revision.** The first-round comments have been addressed with substance, and the analytic core is correct and sound. The remaining points are:
- the cause of the sprinkled-pair shortfall (comment 8), with a concrete test proposed;
- rerunning the FRW sprinkling test with the final estimator (comment 9);
- a realistic-use noise comparison (comment 10).

All three are computations on existing pipelines. I would like to see the results of comments 8 and 9 before acceptance, but I do not expect them to change the paper's main conclusions.

---

## Notes for the author (outside the formal report)

What to fix first, by impact:
1. **Comment 8: the sprinkled-pair shortfall.** This is the one result that determines whether the curvature estimator is usable as advertised. The nearest-element selection hypothesis is cheap to test: reselect a and b uniformly within a window. If it removes the shortfall, you get a clean "unbiased on sprinkled pairs" claim for the abstract.
2. **Comment 9: rerun the FRW test with the pooled estimator and the count window.** At present the only sprinkling test of Eq. (12) uses the estimator you now say is biased. A specialist referee will notice.
3. **Comment 10: compare in realistic use.** Pool P pairs in one region and compare with the ordering fraction on that region.
4. **Comments 12–15:** abstract wording, the τ⁴ systematic, whether the window is intrinsic, and removing the version-history references. All are one-liners.

On the PRD track: the answer says the 1+1 paper now goes to CQG only. I have recorded the 1+1 PRD track as closed after round 1. I agree with the choice; CQG was the better fit.

What changed in my assessment: the v1 risks for CQG were the missing comparisons and the loose structure. Both are fixed. The honest negatives (HMM better at large d; no noise advantage over chain abundances) cost something in "significant advance". But Eqs. (11)–(12) and the clean ablation carry the paper, and the candour helps with a specialist referee.

Estimated chance of eventual CQG acceptance: about **75–85 %** as submitted now, about **85–90 %** with comments 8–10 done, and higher if comment 8 removes the shortfall (v1: 55–70 % as is). This is a judgment call, not data.
