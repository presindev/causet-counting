# Referee report — Physical Review D (second round)

**Manuscript:** "Spatial embedding of 3+1 causal sets: low-count spacelike pairs and a likelihood fit to interval counts" (R. Bada), version v2 (dated October 30, 2026), with the author's response `answer-embedding-3p1-v2.md`.

**Criteria applied:** the APS referee criteria used across the Physical Review family: scientific soundness and technical correctness; novelty and significance sufficient for this journal (as opposed to a less selective one); whether the conclusions are supported by the results; clarity of presentation; recommendation (accept / minor revision / major revision / reject).

**Scope:** the response lists no placeholders, so all of v2 is assessed. I checked every point against the revised manuscript, not only against the response.

---

## Summary

The revision answers every first-round comment with new computations:
- ten universes per size up to n = 6000;
- an ablation against Casasola's near-light-cone likelihood;
- an optimizer study (L-BFGS continuation, three converged starts, a converged truth-started fit);
- an exploratory joint fit of the time coordinate;
- a new figure locating the per-element error.

Several of these changed the paper's claims, and the author has changed the text to match:
- the removed fraction is now 72 %, 74 % and 80 % at n = 1000, 3000 and 6000 (79–83 % above), not 79–83 % at every size;
- using all related pairs is withdrawn as a contribution, because the near-cone pairs do slightly better;
- the v1 explanation of the residual as a local optimum is withdrawn.

## Assessment

This is a good revision. It is unusually candid: three requested checks went against the v1 claims, and in each case the text now follows the data rather than defending the earlier wording. The statistical basis is now adequate. Paired comparisons on 44 universes give 44/44 wins, with the spread across universes reported. The fixed-before-testing protocol is kept even where a better variant was found afterwards, which I respect.

I re-checked the new and changed technical content:
- **Eq. (4):** with τ² ∝ N^{1/2}, δ(τ²)/τ² = δN/2N, so s_ab = τ̂²/[2(N+1)^{1/2}] is the right Gaussian width. The shifts are now unambiguous.
- **Table III:** each "removed" entry agrees with gain/(1 − C_J) to rounding, e.g. 0.0823/0.1145 = 72 % and 0.0094/0.0114 = 82.5 %.
- **Near-cone fractions:** for an element at height T below the top, the 4-volume between its light cone and the hyperboloid τ = τ₀ is ≈ πT²τ₀², against πT⁴/3 for the whole cone. The fraction is ≈ 3τ₀²/T², i.e. ≈ 0.5 for τ₀² = 6ℓ² and T ≈ 6ℓ (n = 3000), and it falls as n^{−1/2}. The quoted 47 % and 37 % (and 64 %) are consistent with this.
- **Term counts:** 4.7×10⁵ and 1.9×10⁶ related pairs agree with the 4D Myrheim–Meyer ordering fraction (R/n² ≈ 0.05).

I found no errors in these. The significance case (first-round comment 1) is now argued rather than demonstrated, and the paper says so explicitly. For PRD I find this acceptable: the oracle localization of the residual is a result in its own right, independent of the fit.

The main remaining issue is how the optimizer result is phrased in the abstract and outlook. The data support a weaker statement than the one made (new comment 7). There is also a stale claim in the abstract ("roughly halves") that the new ten-universe numbers no longer support (new minor comment 9).

---

## Status of first-round comments

| # | Comment (v1) | Status | Reason (checked in v2 text) |
|---|---|---|---|
| M1 | Physical significance not argued | **Resolved** (argued, not demonstrated) | New Introduction paragraph gives three reasons: coordinates as input to further constructions, sharper embedding tests, and localizing what the order carries poorly. It states plainly that no downstream application is shown. Adequate for PRD. |
| M2 | Too few universes | **Resolved** | 10 universes at n = 1000, 3000, 6000 (seeds include v1's), range and s.d. per size in Table III, 44/44 wins. The headline was lowered accordingly. |
| M3 | Ablation against Casasola's near-cone likelihood | **Resolved** | "Which pairs are needed?" in Sec. V: same start, exact Poisson form, all pairs vs τ̂² < 6ℓ². The near-cone set is slightly better (10/10 universes at n = 3000 and 6000). The all-pairs contribution is withdrawn in the Introduction, in "Relation to previous work" and in the Discussion. This narrows the novelty, honestly. |
| M4 | Local optimum / optimizer | **Resolved in substance**; new concern on framing (M7 below) | L-BFGS continuation, three converged starts and a converged truth-started fit, at both n = 3000 and 6000. The v1 explanation is withdrawn in the text. |
| M5 | Time coordinate held fixed | **Resolved** | Joint fit: ΔC = +0.0004 ± 0.0001 (n = 3000) and +0.0002 ± 0.0001 (n = 6000); the time error is not reduced. Stated in Sec. V and Limitations. |
| M6 | Missing references (MRS 2006/2007, ESV 2019) | **Resolved** | Cited and discussed in the Introduction. The link between the +40 % short-distance bias of the detour and ESV's "discrete asymptotic silence" (Sec. IV) is a nice addition. |
| m1 | s_ab notation | **Resolved** | Displayed Eq. (4); checked above. |
| m2 | Table of sprinkling sets | **Resolved** | New Table I. |
| m3 | Abstract too number-dense | **Resolved**, but see new m9 | Much leaner. One sentence ("roughly halves") is now out of date. |
| m4 | Figure of error localization | **Resolved**, but see new m10 | New Fig. 2. The surrounding paragraph still quotes v1 numbers, and the figure is too small to read. |
| m5 | Johnston Table IV mismatch | **Declined; acceptable** | The author has not contacted Johnston, but shows that the mismatch does not come from the time coordinate and that no conclusion uses Table IV. Optional suggestion below. |
| m6 | Slab four-leg fallback | **Resolved** | Sec. VI now explains that the method is undefined for 0.4 % / 0.1 % of pairs and that every other pair keeps its two-leg value. |
| m7 | Unrefereed preprints | **Resolved** | "Not peer reviewed" plus DOIs, and the text states what is taken from Casasola and from Pellegrin. |
| m8 | Hu–Meyer–Meyer citation / 2026 arXiv numbers | **Resolved; comment withdrawn** | I checked the arXiv record. arXiv:2601.03280 was submitted on 31 December 2025 and carries the journal reference J. Math. Phys. 66, 122502 (2025), DOI 10.1063/5.0290407. The citation is correct. I could not independently check arXiv:2610.36695 (too recent to be indexed where I looked). |

---

## New major comment

7. **"Not by the optimizer" is stronger than the evidence.** The abstract says the remaining error "is set by directions in which the likelihood is nearly flat, not by the optimizer". The Outlook adds that it "can only be reduced by additional information, not by a better optimizer". The Discussion calls it "a flat direction of the likelihood rather than an optimization failure". The numbers in Sec. V show something a little different:
   - The converged truth-started fit removes 92–93 % of the residual. Its log-likelihood is **higher** than the converged intrinsic fit's, by 0.9 on average (at most 5) at n = 3000 and by 2.3 (at most 6.5) at n = 6000.
   - If that is true in most or all universes, the global maximum of Eq. (5) lies near the much better map. An ideal global optimizer would then remove more of the residual than 75 %. The optimizer is not irrelevant; rather, the likelihood gives almost no signal (ΔlnL of order 1 out of 10⁵–10⁶ terms) that would guide any practical optimizer there.
   - "Flat direction" and "nearly degenerate separate maxima" are also different pictures. The data shown do not distinguish them.

   I ask the author to:
   - (a) report in how many of the ten universes the truth-started fit has the higher log-likelihood;
   - (b) evaluate lnL along the straight path between the two converged maps, after aligning them by the best rotation about the time axis, under which Eq. (5) is invariant. This tells whether the two maps are joined by a flat valley or separated by a barrier;
   - (c) rephrase the abstract, Sec. V, Discussion and Outlook accordingly. A wording I could accept: "maps of very different accuracy differ in log-likelihood by only O(1), so the likelihood carries almost no information that would let an optimizer prefer the more accurate one".

   The practical conclusion, that more optimization of this likelihood will not help in practice and more information is needed, survives either way. This is mainly a wording fix, but it concerns a sentence in the abstract.

## New minor comments

9. **Abstract: "roughly halves the typical error of individual spatial distances".** This was true of the two universes in v1 (0.22 → 0.11ℓ). With ten universes (Sec. V, "Per-pair errors"), the median falls 0.33 → 0.20, 0.23 → 0.14 and 0.18 → 0.12ℓ, a reduction of 33–40 %, not a half. The 90th and 99th percentiles do fall by more than half. Please say, for example, "lowers the median per-pair error by about a third and more than halves its tail".
   - Similarly, "three quarters to four fifths" is slightly generous for 72–83 %. Giving the range itself would be cleaner.
10. **"Where the error remains" quotes v1 numbers next to a v2 figure.** The paragraph quotes 0.67 → 0.52ℓ, "in the two universes of this size analysed in version 1", with 1.4–1.6ℓ for the bottom decile and 0.18–0.19ℓ for the rest. Fig. 2 shows ten universes and the converged fit. Please recompute these numbers on the set shown in Fig. 2. Also, at the printed size the axis labels and legend of Fig. 2 are illegible; enlarge it to full width or increase the font sizes.
11. **Version history in the manuscript.** The text refers to its own earlier version several times:
    - "version 1 of this paper attributed…", "which version 1 of this paper listed as a contribution";
    - Table I caption: "contains the universes of v1 of this paper";
    - Table III caption: "runs of this version (r35); n ≥ 10000: version 1";
    - Fig. 1 caption: "the 1, 2, 4, 8, 6 universes of version 1".

    A reader of the published paper has no access to an unpublished v1, so these belong in the response letter. If v1 is public (e.g. on arXiv), one footnote is enough. In either case, replace internal run labels in captions with the set names of Table I.
12. **Which variant do you recommend?** Keeping the pre-specified all-pairs Gaussian form as the reported method is the right call methodologically. But the near-cone variant is both slightly better and two to three times cheaper per iteration, and its share of pairs falls as n^{−1/2}. Please:
    - say explicitly which variant a user should run;
    - give its wall time in Sec. VII, since this may move the extrapolated crossover with Johnston's pipeline (n ≈ 16000) considerably;
    - state in the Table III caption that all rows use the fixed 400-iteration Adam schedule, which Sec. V now shows is not converged (the effect on C is ≤ 2×10⁻⁴).
13. **Companion reference [18]** still carries the v1 title of the 1+1 paper. That paper has been retitled ("Spatial distance and curvature from an exact counting identity in two-dimensional causal sets").
14. *Optional.* (a) For Johnston's Table IV, computing two or three candidate statistics would cost little and might settle the question: the correlation of unsquared intervals, timelike pairs only, or a different pair set. (b) The slab comparison in Sec. VI still rests on 3–4 universes per size, while Sec. V now uses ten. Extending it would make the "about 20 percentage points" figure as solid as the rest.

## Recommendation

**Minor revision.** All six major comments of the first round have been addressed with new computations, and the claims were corrected where the results required it. What remains is the phrasing of the optimizer conclusion (comment 7), which needs one additional number and a path scan, and a set of consistency fixes (9–13). I do not need to see the manuscript again if comment 7 is handled as described. I would be glad to check the revised wording if the editor prefers.

---

## Notes for the author (outside the formal report)

What to fix first, by impact:
1. **Comment 7 (optimizer framing).** It is in the abstract and a careful referee will catch it. Report how many universes have truth-start lnL > intrinsic lnL, run the interpolation scan, and soften "not by the optimizer". This takes a day or less on existing outputs.
2. **Comment 9 ("roughly halves").** A one-line fix, but it is a stale claim in the abstract that your own Sec. V contradicts. That is the kind of inconsistency that costs credibility with a referee.
3. **Comment 10.** Recompute the stale v1 numbers in "Where the error remains", and make Fig. 2 legible.
4. **Comment 11.** Strip the "version 1" references and run IDs from the manuscript.
5. **Comments 12–13.** Recommend a variant, time it, and fix the companion title.

Your note about correcting the L-BFGS gain (45, up to 98) before delivery: the v2 text and the answer are consistent on this, and the corrected figure is the one I assessed.

What changed in my assessment: the revision fixed exactly the issues that drove the v1 uncertainty (statistics, the Casasola ablation, the optimizer). The cost is a narrower novelty claim. The likelihood is Casasola's and the near-cone pairs suffice, so the contribution is now the oracle diagnosis, the intrinsic start and the benchmark comparison. I think that is still enough for PRD, especially with the honest framing. The main residual risk is a referee who calls it incremental over Johnston + Casasola.

Estimated chance of eventual PRD acceptance: about **65–75 %** as submitted now, about **70–80 %** with comments 7 and 9–11 fixed (v1: 60–75 %). This is a judgment call, not data.
