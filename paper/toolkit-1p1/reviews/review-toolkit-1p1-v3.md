# Referee report — Classical and Quantum Gravity (third round)

**Manuscript:** "Spatial distance and curvature from an exact counting identity in two-dimensional causal sets" (R. Bada), version v3 (dated October 30, 2026), with the author's response `answer-toolkit-1p1-v3.md` and a latexdiff against v2.

**Criteria applied:** CQG Research Papers are "reports of high-quality original research with conclusions representing a significant advance in the field". The IOP referee assessment covers:
- originality;
- significance;
- scientific soundness;
- whether the conclusions are supported;
- clarity of presentation;
- appropriate referencing;
- suitability for the journal's readership.

The recommendation is one of accept, minor revision, major revision or reject. IOP's research data policy also applies (persistent identifier for code).

**Scope note:** the response lists two placeholders, which are not assessed:
- the N = 800 held-out test in Sec. VI (`[r27: …]`; the response says the job has run but its output is not yet fetched);
- the Zenodo DOI in the Data availability statement.

I used the diff to locate changes and judged the clean v3 PDF.

---

## Summary

v3 reports the three computations requested in the second round, and all three changed the paper:
- **Sprinkled pairs (comment 8).** The low reading came from selecting the elements nearest to target points; the strip counts confirm this. Pooling all spacelike pairs from position-defined windows removes it, by the Mecke formula. Drawing a single uniform pair does not, and the paper explains why.
- **FRW (comment 9).** With the final estimator, the pooled result reproduces the same fit on the exact continuum volumes. That target exceeds the leading-order Eq. (12) prediction substantially. Eq. (12) is now presented as giving the direction of the effect, not its size.
- **Realistic use (comment 10).** On one sprinkled region, the ordering fraction of that region is about three times more precise than the pooled drift in de Sitter space and less biased. The pooled drift retains a low bias of 0.1–0.5 within one region, because its pairs share elements. The paper says so.

In addition:
- the window is shown to be order-only on a causally convex region, and the tests are repeated in such a region;
- the τ⁴ systematic is stated as a systematic of the method;
- Eq. (12) is now said to fix only the first moment of the depth weighting;
- the references are completed.

## Assessment

**Soundness.** I checked the new arguments.
- **Mecke formula (comment 8).** The pooled estimator is −16Σβ/Σα over all spacelike pairs with a and b in fixed windows, each kept with a fixed probability. By the second-order Mecke formula, E[Σ_{pairs} f(a, b, Φ)] = ρ²∬ E[f(a, b, Φ∪{a, b})] da db, provided the weight depends only on the positions of the pair. So Σβ and Σα have exactly the inserted-pair expectations. The argument is correct. It applies to the sums, which is why the pooled form must be the ratio of sums, as now written.
- **Single uniform draw.** Under the 1/(1+N_W) reweighting, the expected count in the window becomes λ/(1 − e^(−λ)) − 1 ≈ λ − 1. "Removes about one element" is correct, and it explains the intermediate values in Table III.
- **Next order of the expansion.** The claim that the next order is not a weighted average of R agrees with my second-round series: the τ⁴ coefficient contains σ''² ∝ R² and σ'''' terms.
- **Convexity argument (comment 14).** It is correct as a sufficient condition, but see comment 21.
- **Comment 9 decomposition.** The steps are additive and plausible: −0.55 (Eq. 12) → −0.67 (exact volumes, d → 0) → −0.80 (d = 14ℓ) → −0.79 (same c's).

I found no technical errors. The problems are in how three results are stated (comments 18–21).

**Significance, reassessed under the CQG rubric.** The paper now stands on:
1. the exact rectangle identity and a bias-corrected distance estimator. It beats Boguñá–Krioukov's equal-depth construction at all separations, ties or beats a counting version of Hu–Meyer–Meyer between 2ℓ and 10ℓ, and loses to it beyond. The ablation cleanly attributes the gain to the free choice of c;
2. the exact de Sitter closed form, Eq. (11), and the leading-order FRW form, Eq. (12): curvature as the depth-dependent failure of an exact flat-space identity;
3. a pooled curvature estimator that is unbiased as an ensemble average under the right selection. But on a single region it is less precise than the ordering fraction and retains a low bias;
4. two supporting items: the embedding-test diagnostic and the Laguerre appendix.

The practical half of the title, curvature as an estimator, has turned out not to be competitive. I respect that the paper says this plainly. What remains as a "significant advance" is mainly analytic and conceptual: items 1 and 2. A secondary, transferable contribution is the identification and repair of a Palm-type selection bias in tests with "sprinkled pairs". Other kinematic studies that pick the elements nearest to target points share this bias.

For CQG's specialist readership, I judge this still sufficient. Exact counting identities in 2D causal sets, with a closed-form curvature effect, are the kind of kinematic result this journal publishes. But the margin is thinner than in round 2, and the abstract should not present the curvature estimator more favourably than Sec. IV does (comment 18). A test where locality matters, i.e. where the drift's pair-and-depth specificity is an advantage over a whole-region ordering fraction, would restore much of the practical case (comment 24, optional).

---

## Status of second-round comments

| # | Comment (v2) | Status | Reason (checked in v3 text) |
|---|---|---|---|
| 8 | Sprinkled pairs read low | **Resolved in substance**; scope and abstract issues remain (comments 18, 19) | Mechanism shown in the strip counts (−0.2 to −0.4 elements); Mecke-based pooling removes the shortfall (Table III "windows" rows; convex-region repeat). |
| 9 | FRW test used the superseded estimator | **Resolved**; one number mis-stated (comment 20) | Rerun with the pooled estimator in a causally convex region at three depths; matches the continuum fit within 1σ; Eq. (12) downgraded in Sec. IV and Limitations. |
| 10 | Noise comparison in realistic use | **Resolved** (negative result reported); the abstract understates it (comment 18); flat control not at equal input (comment 22) | One-region comparison with P = 10–300 pairs against the ordering fraction, 400 sprinklings. |
| 11 | Eq. (12) fixes only the first moment | **Resolved** | Text after Eq. (12) now says so and notes the R² and d²R/dτ² terms at the next order (consistent with my series). |
| 12 | Abstract wording on accuracy ranges | **Resolved** | Equal-depth beaten at all separations; tie or better against HMM at 2ℓ–10ℓ; HMM better above. |
| 13 | τ⁴ systematic | **Resolved** | Stated as +2 to +4 %, region-dependent, in Sec. IV and Limitations; the τ⁴ fit was declined with a reason (noise ×3). |
| 14 | Is the window intrinsic? | **Partially resolved** (comment 21) | Correct sufficient condition. "Set by the order alone" holds only when the causal set is itself order-defined. The element f is not needed. |
| 15 | Version history | **Resolved** | No references to earlier versions remain. |
| 16 | References | **Resolved** | [17] CQG 35, 084001 (2018), consistent with the DOI I found earlier. [16] CQG 33, 065003 (2016): the author cites INSPIRE; I could not confirm it independently. |
| 17 | "What z adds" paragraph | **Resolved** | |

First-round comments: M1, M2 and M4–M7 remain resolved. M3 is now **resolved**: window (a), benchmark (b), offset (c), sprinkled pairs (d) and kernel (e) are all addressed, with the wording issues below. m6 (DOI) is still a placeholder; m7 (IOP style) is deferred to the final version, as agreed.

---

## New comments

18. **The abstract is more favourable to the curvature estimator than Sec. IV.**
    - "Pooled over many pairs, a fit of this depth drift reproduces the same fit on the exact continuum volumes … with sprinkled pairs selected independently of their neighbourhoods" is true as an average over 1000 *independent* sprinklings. Within one region, Sec. IV and Limitations report a low bias of 0.46 ± 0.11 and 0.18 ± 0.07 in de Sitter space and 0.10 ± 0.02 in flat space. The abstract should say so.
    - "Not more precise than the ordering fraction" understates the result. In de Sitter space the ordering fraction's spread is about a third of the drift's (0.80 against 2.25 at ρ = 4000; 0.46 against 1.33 at ρ = 10⁴), and it is less biased. Suggested: "for the curvature of a given region it is less precise than the ordering fraction and, within one region, biased low".
    - Separately, at ρ = 4000 the "windows" row (1.91 ± 0.10 against a target of 2.08) is 1.7σ low. That is acceptable, but "reproduces" is then a little generous for that row.
19. **Scope of the Mecke argument.** The argument covers sums over all pairs with a weight that depends only on the pair's *positions*, independently of the rest of the configuration. Sec. IV then generalizes: "On a causal set without coordinates the windows are replaced by any rule of this kind, for example all pairs within a range of count-defined separations." A count-defined separation depends on the configuration. If it is computed from the same N_A, N_B, N_C as the estimator, the selection is correlated with the intercept α. Mecke does not cover it, and such a selection could bias the ratio. Please either:
    - (a) test it: rerun the windows comparison with an additional cut on the count-defined d̂;
    - or (b) remove the example and state the condition precisely: a sum over all pairs (optionally thinned at random with a fixed probability) of a selection that does not depend on the counts used by the estimator.

    The abstract's "selected independently of their neighbourhoods" is also loose: a single uniform draw is independent of the neighbourhood in the everyday sense, yet biased. "Pooled over all pairs of a position-based selection" is the correct condition. Please also state how the P pairs of the one-region comparison were drawn. A fixed number drawn from the qualifying pairs carries a P/N_pairs weight. That is presumably negligible at these sizes, but it is the same mechanism as the single uniform draw.
20. **The "about 30 %" in the FRW result.** Limitations says that "the target exceeds the leading-order prediction of Eq. (12) by about 30 %". From the numbers in Sec. IV, the continuum target exceeds the Eq. (12) fit by 35 %, 44 % and 53 % (−0.70/−0.52, −0.79/−0.55, −0.90/−0.59). Equivalently, Eq. (12) falls short of the target by 26–34 %. Sec. IV ("not its size to better than about 30 %") is consistent with the second reading; Limitations states the first. Please make the two agree.

    The abstract still says that in any FRW spacetime "the leading failure measures the scalar curvature one third of the way from the pair to c". That is correct as a leading-order statement. Given the downgrade in Sec. IV, add "to leading order in the depth" or similar, so that a reader does not take it as a property of the estimator over a realistic window.
21. **"In a causally convex region its window is set by the order alone".** The argument (f in the common future of a, b; the rectangle lies in I(c, f) ⊂ region) is correct but stronger than needed, and the claim it supports is not quite what it shows.
    - **(a) f is not needed.** The estimator counts only A, B and C, which lie in I(c, a) ∪ I(c, b), and these lie in any causally convex region that contains c, a and b. The tile D, the only part of the rectangle beyond those intervals, is never counted.
    - **(b) Convexity is an assumption, not something the order decides.** Whether the region is causally convex is a property of the continuum region the causal set was sprinkled into. The order decides it only when the causal set is itself defined from the order, e.g. an interval I(p, q) or the past of an element. The past of an element "cut at a spacelike surface", as used in the tests, is causally convex, but the cut is not defined by the order.

    Suggested wording: "on a sprinkling of a causally convex region, for example an interval of the causal set, every c in the common past can be used, so the window needs no coordinates; otherwise the boundary must first be inferred [31]". Also, Table III's caption still says "count-defined window" while the paragraph is now "Window from the order".
22. **The flat control in the one-region comparison is not at equal input.** The flat diamond of the same coordinate size holds 8.4×10³ elements against 2.5×10³ for the de Sitter one at ρ = 4000. "The two spreads are equal" therefore compares the methods at a different number of elements than the de Sitter case. Either match the element count, or state the difference where the result is quoted.
23. **Data availability and placeholders.**
    - The statement says the code and notebook "are openly available" at the GitHub URL, while the responses say the repository will be made public on submission. The statement must be true when the paper is submitted, and the same applies to Ref. [46].
    - The Zenodo DOI remains a placeholder. As I understand IOP's research data policy, this need not block acceptance, provided the accepted version contains a working persistent identifier for the tagged code and the repository is public. I would ask the editor to make this a condition of acceptance.
    - The r27 held-out test has now been a placeholder for three rounds. It supports the only claim about the null-pair flag that was not tuned on the test states, so it must be filled, and checked, before submission.
24. *(Optional, for significance.)* The paper's remaining argument for the depth drift is that it measures curvature "along a specific pair and depth rather than over a whole diamond". That advantage would show only where curvature varies across the region. One test that would make it concrete:
    - take an FRW spacetime, or one with spatially varying curvature;
    - compare the pooled drift of pairs at a given location with the ordering fraction of diamonds of matched footprint and element count;
    - report which resolves the variation better.

    If the drift wins there, the paper regains a practical use. If not, the Discussion should say plainly that the curvature result is analytic and conceptual. The Discussion could also mention the selection-bias finding of comment 8 as a methodological point of general use.

## Recommendation

**Minor revision.** The work is technically sound, and every requested computation has been done and reported honestly, including three outcomes that went against the paper. Comments 18–23 are about how results are stated, plus one optional check (19a). With them, the conclusions in the abstract will match those of the body. My significance assessment is lower than in round 2, because the curvature estimator turned out not to be competitive in realistic use. I still consider the exact identity, the distance estimator and the closed-form depth drift a sufficient contribution for CQG. I do not need to see the manuscript again if comments 18–21 are handled as described. The DOI and r27 must be completed before acceptance.

---

## Notes for the author (outside the formal report)

What to fix first, by impact:
1. **Comment 18 (abstract).** This matters most. A CQG referee reading the abstract, and then Sec. IV's one-region comparison, will feel the abstract oversold. State the in-region bias and "less precise than the ordering fraction".
2. **Comment 19 (Mecke scope).** Delete "for example all pairs within a range of count-defined separations", or test it. As written, it recommends a selection that the paper's own argument does not cover, and it is exactly the rule a user would adopt.
3. **Comments 20–21.** Fix the 30 % so Sec. IV and Limitations agree (35–53 % "exceeds", or 26–34 % "falls short"). Simplify the convexity argument (no f needed), and say that convexity is an assumption unless the causal set is an interval.
4. **Comment 23.** Make the repository public, fetch and check r27, and mint the DOI before submission.
5. **Comment 24 (optional).** A locality test, i.e. curvature varying across the region, is the one experiment that could turn the curvature estimator back into a practical tool. If you have cluster time, it is the best use of it for this paper.

What changed in my assessment: round 2's odds assumed the realistic-use comparison might favour the drift, and it did not. The paper is more honest and more correct than in round 2, but its "significant advance" now rests on the analytic results and the distance estimator. The main risk is a referee who asks what the curvature estimator is for if the ordering fraction does better. Comment 24 is the answer to that question, if it can be given.

Estimated chance of eventual CQG acceptance: about **65–75 %** as submitted now, about **70–80 %** with comments 18–23 fixed, and higher if comment 24 shows an advantage from locality (v2: 75–85 %). This is a judgment call, not data.
