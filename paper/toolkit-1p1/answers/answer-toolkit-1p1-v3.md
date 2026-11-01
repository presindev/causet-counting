# Answer to the referee: toolkit-1p1, round 2 (CQG)

**Manuscript:** "Spatial distance and curvature from an exact counting identity in two-dimensional causal sets" (R. Bada).
**This answer** responds to `review-toolkit-1p1-v2.md` and comes with `toolkit-1p1-v3.pdf` and `toolkit-1p1-v3-diff.pdf` (latexdiff against v2).

We thank the referee for the second report, and in particular for the concrete hypothesis in comment 8, which turned out to be right. The three requested computations changed the paper as follows:

- **Comment 8: the sprinkled-pair shortfall is a selection effect, and it goes away.** The nearest-element selection depletes the strips, as the referee suspected. Using all pairs in target windows, the pooled estimator agrees with inserted pairs within the errors. The abstract now states the sprinkled-pair result.
- **Comment 9: the FRW test with the final estimator.** The pooled estimate reproduces the continuum fit on the same elements. However, that continuum fit is about 30 % larger in magnitude than the leading-order prediction of Eq. (12) over realistic windows. The text now says that Eq. (12) gives the direction of the effect, not its size.
- **Comment 10: in realistic use the ordering fraction wins.** On one region, pooling 100 pairs gives a spread between sprinklings 1.0–2.9 times that of the ordering fraction of the same region. The pooled estimate also keeps a low bias within one region. The paper now says plainly that, for the curvature of a given region, the ordering fraction is at least as precise.

All new runs are in `sims/r40_curvature_round2.py` (parts `select`, `convex`, `frw`, `noise`), with outputs in `sims/out/r40_*.txt`. Its `inserted` and `nearest` rows reproduce the v2 Table III numbers seed for seed (same seeds 1–1000, same code path), which checks the new counting code.

---

## New major comments

### Comment 8: sprinkled pairs read low

> A clean test: choose a and b uniformly among the sprinkled elements in a target window. By the Slivnyak–Mecke property this is unbiased, and it is also what a user would do on a real causal set. Alternatively, exclude the elements of the strips within a few ℓ of a and b. If the shortfall disappears, the estimator is unbiased in practice, and the abstract can say so. If it does not, the abstract should report the sprinkled-pair result next to the inserted-pair one.

**Response.** Done. The hypothesis is confirmed and the shortfall disappears. One refinement concerns how the window is used.

*Direct test of the mechanism.* For every c in the window we recorded N_A − ρV_A, N_B − ρV_B and N_C − ρV_C per depth bin. With nearest-element selection, N_A − ρV_A is lower than with inserted pairs by about 0.2 elements at ρ = 4000 and 0.4 at ρ = 10⁴, nearly constant in depth. N_B is shifted down in the same way. This is the fixed deficit at the shallow ends of the strips that the referee predicted. A fixed deficit is a larger fraction of λ_A for shallow c, so it tilts the slope up and reads R low.

*Uniform selection.* We ran two versions of it.
- **One pair per sprinkling, a and b drawn uniformly from the elements in a square window** (half-width 0.025 around each target point, about 2.5ℓ at ρ = 10⁴). This only reduces the shortfall. The reason is that choosing one of the N_W elements in a window weights each configuration by 1/N_W. Conditionally on a's position, the other points then follow the Poisson law reweighted by 1/(1 + N_W), which has about one element fewer in the window. So the Slivnyak–Mecke argument does not apply to a single draw per region.
- **All spacelike pairs (a in window A, b in window B), each kept with a fixed probability** (independent of the configuration, about 20 pairs per sprinkling), all pooled. By the Mecke formula, a sum over all pairs of a Poisson process, with a weight that depends only on the positions of the pair, equals the average over pairs placed by hand at the same positions. This is the version without bias, and it removes the shortfall.

Pooled R over 1000 sprinklings (errors from a bootstrap over sprinklings; box region of v2, count-defined window):

| ρ | geometry | inserted | nearest (v2) | one uniform pair | all window pairs | continuum |
|---|---|---|---|---|---|---|
| 4000 | de Sitter | 1.97 ± 0.11 | 1.70 ± 0.11 | 1.80 ± 0.11 | 1.91 ± 0.10 | 2.07–2.08 |
| 10⁴ | de Sitter | 1.99 ± 0.07 | 1.84 ± 0.07 | 1.90 ± 0.07 | 2.02 ± 0.06 | 2.08 |
| 4000 | flat | −0.03 ± 0.03 | −0.07 ± 0.03 | −0.06 ± 0.02 | 0.00 ± 0.02 | 0 |
| 10⁴ | flat | −0.01 ± 0.02 | −0.04 ± 0.02 | −0.03 ± 0.02 | −0.01 ± 0.01 | 0 |

With all window pairs, the offset from the continuum value is −0.16 ± 0.10 and −0.06 ± 0.06 in de Sitter space, and 0.00 ± 0.02 and −0.01 ± 0.01 in flat space. Each is level with the inserted-pair offset within the errors. The 20 pairs per sprinkling barely lower the error compared with one pair, because they share most of their common past.

We did not run the excision variant: the all-pairs version settles the question and needs no coordinates near a and b. In practice the windows are replaced by any selection that depends only on the pairs themselves, for example all pairs within a range of count-defined separations. The text says this.

**Change:**
- Sec. IV, new paragraph "Sprinkled pairs" (mechanism, counts, Mecke argument, both uniform versions);
- Table III, now with three selections per density;
- abstract: the sprinkled-pair statement next to the inserted-pair one, with the condition on the selection;
- Limitations.

### Comment 9: the FRW test used the superseded estimator

> Please rerun it with the pooled estimator and the count-defined window. Compare with the continuum fit on the same elements. Compare also with the Eq. (12) prediction. The window spans R from −0.4 to −2.8, so this also shows how far the leading-order kernel can be trusted over a realistic window.

**Response.** Done. Setup: p = 1, ρ = 10⁴, a and b inserted 14ℓ apart at η₀ = 1.5, and 1000 sprinklings. We used the pooled estimator and the count-defined window. The region is causally convex (the past of an element at η = 1.55), cut at three depths so that the window ends at η_c ≥ 1.10, 0.92 and 0.75. The middle one is the v2 window.

| window reaches τ = | R at a,b → bottom | pooled R | continuum fit, same c's | Eq. (12), same fit | R at one third of the depth |
|---|---|---|---|---|---|
| 0.52 | −0.40 → −1.37 | −1.03 ± 0.37 | −0.70 | −0.52 | −0.55 |
| 0.70 | −0.40 → −2.79 | −0.88 ± 0.18 | −0.79 | −0.55 | −0.63 |
| 0.84 | −0.40 → −6.32 | −0.93 ± 0.11 | −0.90 | −0.59 | −0.70 |

- **The estimator reproduces the continuum fit within 1σ.** It is no longer biased low as in v2 (−1.25 with the per-pair mean).
- **The continuum fit is about 30 % larger in magnitude than the Eq. (12) prediction.** To see why, we decomposed the middle window: exact volumes with c straight below and d → 0 give −0.67, so the higher orders in τ account for −0.11; the finite separation d = 14ℓ accounts for another −0.13, giving −0.80.
- **So Eq. (12) gives the direction but not the size.** Over a realistic window it says that the drift measures a curvature below the pair, but not its size to better than about 30 %. The v2 sentence "the estimator measures a depth-weighted curvature, as Eq. (12) says" is withdrawn and replaced by this statement.

**Change:**
- Sec. IV, new paragraph "FRW spacetime" (replaces the v2 FRW sentences);
- Limitations ("In FRW spacetime the target exceeds the leading-order prediction … by about 30 %").

### Comment 10: noise comparison as the method would be used

> Please show, on one sprinkled region at given ρ and size: the pooled estimator from P pairs in that region, with P around the ~100 the paper says is needed, its error estimated from the spread between sprinklings, since pairs within one region share elements; the ordering-fraction curvature estimate from the same region.

**Response.** Done, and the result goes against the depth drift.

*Setup.*
- The region is a causal diamond (an interval of the causal set) in de Sitter space, u, v ∈ [−3, −0.95] with H = 1: 2.5×10³ elements at ρ = 4000 and 6.3×10³ at ρ = 10⁴. Each density was sprinkled 400 times.
- In each sprinkling we drew P = 300 spacelike pairs near the top of the diamond, 9ℓ–17ℓ apart at ρ = 10⁴. We pooled the first 10, 30, 100 and 300 of them.
- The ordering fraction f of the whole diamond gives R = 2(f − ½)/(f_cont − ½), calibrated on the exact continuum diamond (f_cont = 0.5173).
- Both errors are the spread between sprinklings.
- A flat diamond of the same coordinate size (8.4×10³ elements at ρ = 4000) is the control.

Values are the mean and the standard deviation between sprinklings:

| | ordering fraction | drift, P = 10 | P = 30 | P = 100 | P = 300 | drift continuum fit |
|---|---|---|---|---|---|---|
| dS, ρ = 4000 | 2.05, 0.80 | 1.61, 2.52 | 1.62, 2.36 | 1.63, 2.25 | 1.63, 2.23 | 2.09 |
| dS, ρ = 10⁴ | 1.99, 0.46 | 1.95, 1.60 | 1.95, 1.38 | 1.92, 1.33 | 1.92, 1.31 | 2.10 |
| flat, ρ = 4000 | 0.01, 0.43 | −0.10, 0.48 | −0.11, 0.45 | −0.10, 0.44 | −0.09, 0.43 | 0 |

- **Spread.** In de Sitter space the ordering fraction has about a third of the spread of the pooled drift. In the flat control, where the diamond holds 3.4 times as many elements, the two spreads are equal.
- **Pooling saturates.** Pooling saturates after a few tens of pairs, because pairs in one region share most of their common pasts.
- **Bias within one region.** The pooled drift keeps a low bias: −0.46 ± 0.11 and −0.18 ± 0.07 in de Sitter space, and −0.10 ± 0.02 in flat space. Pooling within one region removes the ratio bias only to the extent that the pairs are independent, and they are not.

The paper now says this plainly: for the curvature of a given region the ordering fraction is at least as precise and less biased, and the depth drift does not improve on it in precision. What the drift adds is geometric: a curvature measured along a given pair and depth, as the failure of an exact identity, with Eq. (12) saying where it is measured. The v2 comparison of one pair with one diamond is removed. The Benincasa–Dowker numbers are kept, shortened.

**Change:**
- Sec. IV, paragraph "Comparison with other estimators" (rewritten);
- abstract ("For the curvature of a given region it is not more precise than the ordering fraction");
- Limitations.

---

## New minor comments

### Comment 11: Eq. (12) and the triangular weight

> The leading-order result fixes only the first moment of the depth kernel (mean depth τ/3). The triangular weight 2(τ − s)/τ² is one kernel with that mean, not one the expansion determines. Please phrase it as an illustration, or derive the kernel to all orders in the depth if possible.

**Response.** Agreed. The triangular weight is now presented as one illustration with the right mean depth. The next order of the expansion (`sims/out/r38_drift_kernel.txt`, coefficient A4) contains σ₂² ∝ R² and σ₄ ∝ d²R/dτ² terms, so it is not a weighted average of R and no kernel exists beyond the first moment. The text says so. The new FRW test (comment 9) shows the practical consequence: over realistic windows the higher orders matter.

**Change:** Sec. IV, sentence after Eq. (12).

### Comment 12: abstract

> "more accurate than the equal-depth and past–future constructions below about ten discreteness lengths" suggests that the equal-depth estimator wins above 10ℓ. […] At N = 1000 and 2ℓ–10ℓ, ours and HMM are essentially tied in error (0.095 vs 0.098). Please rephrase, and consider whether "unbiased curvature estimator on sprinklings with inserted pairs" should also give the sprinkled-pair result.

**Response.** Rephrased:
- the rectangle estimator is more accurate than equal depth at all separations;
- between 2ℓ and 10ℓ it is "as accurate as or more accurate than" the Hu–Meyer–Meyer construction (tied at N = 1000, 0.059 against 0.099 at N = 4000);
- Hu–Meyer–Meyer is more accurate above that.

The curvature sentence now covers both pair selections (comment 8), and the abstract also states the comparison with the ordering fraction (comment 10).

**Change:** abstract.

### Comment 13: the τ⁴ systematic

> In practice R_fit^cont is not known, so this is a +3–4 % systematic of the method that depends on the size of the region. Please state it as such in Limitations. Alternatively, remove it by adding a τ⁴ term to the fit or by capping the window in units of the counts.

**Response.** Stated as a systematic of the method in Sec. IV and in Limitations. The causally convex region of comment 14 shows that it depends on the region: there the target is 2.03–2.04 instead of 2.07–2.08, so the systematic is +2 to +4 %. We did not adopt a τ⁴ term. In v2's runs (r37, `intrinsic_quad`) a quadratic fit raised the single-pair spread by a factor of about 3 and introduced its own large offset. Capping the window lowers the systematic at the cost of noise, as the existing sensitivity scan shows; the text points to it.

**Change:** Sec. IV, "Window from the order"; Limitations.

### Comment 14: is the window intrinsic?

> "Down to the deepest c whose rectangle lies in the sprinkled region": please say how this condition is decided from the order alone […] Otherwise the window still uses the coordinates.

**Response.** In v2 it was decided from the coordinates, and we say so now. The condition is decided by the order alone when the region is causally convex, for example an interval of the causal set or the past of an element f cut at a spacelike surface. If f is in the common future of a and b, the rectangle of every c in their common past lies in I(c, f) and hence in the region. Every c of the common past is then usable, and the window ends at the deepest one. On a region that is not causally convex the boundary has to be identified first, which in 1+1 dimensions is possible from the order (Cunningham, CQG 35, 094002 (2018), now cited).

We repeated the comment-8 test in such a region: the past of f = (−0.95, 0), cut at η = −3, with no coordinate test, every c of the common past used, and 1000 sprinklings.

| ρ | geometry | inserted | nearest | all window pairs | continuum |
|---|---|---|---|---|---|
| 4000 | de Sitter | 2.10 ± 0.09 | 1.96 ± 0.09 | 2.10 ± 0.08 | 2.03 |
| 10⁴ | de Sitter | 2.03 ± 0.06 | 1.95 ± 0.06 | 2.04 ± 0.06 | 2.04 |
| 4000 | flat | 0.01 ± 0.02 | −0.05 ± 0.02 | 0.00 ± 0.02 | 0 |
| 10⁴ | flat | 0.00 ± 0.01 | −0.02 ± 0.01 | −0.01 ± 0.01 | 0 |

The conclusions of comment 8 hold with the order-only window.

**Change:** Sec. IV, paragraph renamed "Window from the order", with the convexity argument and the convex-region results.

### Comment 15: version history

> "version 1 of this paper could not exclude", "the window of version 1" and "(version 1, before pooling)" refer to a version the reader has not seen.

**Response.** All three are removed. Version 1 is not public, so no footnote is needed. The sentences that carried them were rewritten anyway (pooling paragraph, FRW paragraph).

**Change:** Sec. IV.

### Comment 16: references

> [17] (Glaser, Ising model coupled to 2d orders) appeared in Class. Quantum Grav. 35, issue 8 (2018), DOI 10.1088/1361-6382/aab139. Please add the article number. Please check whether [16] (Glaser–Surya, arXiv:1410.8775) has a journal version.

**Response.** Both are completed from the INSPIRE records:
- Glaser, CQG **35**, 084001 (2018);
- Glaser and Surya, CQG **33**, 065003 (2016).

**Change:** reference list.

### Comment 17: typesetting

> In Sec. V, "What z adds." runs on inside the "Null-pair fraction" paragraph; start a new paragraph.

**Response.** Done.

**Change:** Sec. V.

---

## First-round comments (status)

The referee marked all first-round comments resolved or withdrawn except M3 (partially resolved), m6 (placeholder) and m7 (deferred). For completeness:

| # | Status after v3 |
|---|---|
| M1 Hu–Meyer–Meyer | Resolved in v2. Unchanged, except the abstract wording (comment 12). |
| M2 Ablation | Resolved in v2. Unchanged. |
| M3 Curvature estimator | (a) window: now order-only in a causally convex region (comment 14); (b) benchmark: redone in realistic use (comment 10); (c) offset: resolved in v2; (d) sprinkled pairs: cause found and removed (comment 8); (e) kernel: first moment only, FRW test with the final estimator (comments 9 and 11). |
| M4 Structure | Resolved in v2. Unchanged. |
| M5 Why z | Resolved in v2. Now in its own paragraph (comment 17). |
| M6 e^{−βS} states | Resolved in v2. Unchanged. |
| M7 References | Resolved in v2. [16] and [17] completed (comment 16). |
| m1–m4 | Resolved in v2. Unchanged. |
| m5 HMM citation | Withdrawn by the referee. No reply needed. |
| m6 Persistent DOI | Still a placeholder (below). |
| m7 IOP style | Deferred to the final version, as agreed. |

---

## Other changes

- Table III now gives errors from a bootstrap over sprinklings, which for the one-pair rows is the same as v2's bootstrap over pairs. The flat inserted row at ρ = 4000 reads −0.03 ± 0.03 (v2: ± 0.02) because of rounding.
- The pooled estimator is written −16 Σβ/Σα (identical to −16⟨β⟩/⟨α⟩ for one pair per sprinkling, and the form needed when sprinklings contribute different numbers of pairs).
- Data availability lists `sims/r40_curvature_round2.py`.
- latexdiff PDF against v2 included this round.

## Results still marked as placeholders in v3 (not to be assessed)

- Sec. VI: the N = 800 held-out test of the null-pair flag (cluster job r27). The job ran on the cluster; its output has not yet been fetched.
- The Zenodo DOI in the Data availability statement (on submission).
