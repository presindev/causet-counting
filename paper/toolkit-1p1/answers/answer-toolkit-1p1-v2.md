# Answer to the referee: toolkit-1p1, round 1 (CQG)

**Manuscript:** v1 "Counting identities in two-dimensional causal sets: spatial distance, depth-drift curvature, and a fixed-size propagator target"; v2 retitled "Spatial distance and curvature from an exact counting identity in two-dimensional causal sets" (R. Bada).
**This answer** responds to `review-toolkit-1p1-v1.md` in the CQG track and comes with `toolkit-1p1-v2.pdf`. The 1+1 paper goes to CQG only; we do not continue the PRD track.

We thank the referee for a detailed report. Every point is answered below in the referee's order. The requested checks changed several claims:

- **Distance estimator:** Hu–Meyer–Meyer's construction, read from counts, is more accurate than ours above about ten discreteness lengths. Our accuracy claim is now restricted to shorter separations.
- **Curvature offset:** the low reading that v1 "could not exclude" is real for the v1 estimator. We traced it to a ratio bias, and pooling removes it.
- **Noise:** our curvature estimator is not less noisy than the chain-abundance route at equal density.

New scripts:
- `sims/r36_rect_ablation_hmm.py`: Majors 1–2.
- `sims/r37_curvature_referee.py`: Major 3 and the Fig. 3 minor.
- `sims/r38_drift_kernel.py`: the FRW kernel.

---

## Major comments

### Major 1: comparison with Hu–Meyer–Meyer is missing

> HMM give an exact 1+1 reconstruction from one past and one future element […] Readers in this community will expect it in Table II, on the same pairs.

**Response.** Added to Table II, on the same pairs and sprinklings. HMM state their construction as exact geometry:

- if p ≺ a, b ≺ q and all four proper times equal s, then d² = τ_pq² − 4s².

They do not give a causal-set estimator, so we built the natural counting version:

- read every τ² from a count, τ² = 2N/ρ;
- take p from the common past and q from the common future;
- keep the (p, q) pairs whose four counts agree within Poisson noise (χ² < 3);
- use the one with the smallest counts, which has the smallest variance.

We also tried two other choices: the single best-matched (p, q), and an average over all matched pairs. Both are less accurate, and the script reports them.

Result (Table II; N = 1000 and 4000, 12 sprinklings × 100 middle-band pairs):

| Separation | Bias of d², HMM | Bias of d², ours | Median error of d, HMM | Median error of d, ours | Better |
|---|---|---|---|---|---|
| 2ℓ–10ℓ, N = 1000 | +23 % | +1 % | 0.098 | 0.095 | ours |
| 2ℓ–10ℓ, N = 4000 | +22 % | 0 % | 0.099 | 0.059 | ours |
| > 10ℓ, N = 1000 | +4 % | −4 % | 0.028 | 0.082 | HMM |
| > 10ℓ, N = 4000 | 0 % | −2 % | 0.015 | 0.039 | HMM |

- **Between 2ℓ and 10ℓ** our estimator is more accurate and unbiased. HMM is biased high by about 20 %, because τ_pq² − 4s² is a small difference of two noisy terms.
- **Above 10ℓ** HMM is unbiased and clearly the most accurate. There the tile between a and b is large, and a direct count of it, corrected exactly by the four equal intervals, beats reading the same volume from the strips. This is consistent with the variance argument already in Sec. III.

We have changed the claims accordingly. The abstract, Sec. III and the Discussion now say that our estimator is the more accurate one below about ten discreteness lengths, and HMM's above. The Outlook suggests a combined estimator. We moved HMM from the outlook into the main comparison.

**Change:** Table II (new rows), Sec. III "Tests" (new second paragraph), abstract, Discussion ("What is new", Limitations, Outlook).

### Major 2: where the estimator's gain comes from

> Please add an ablation: (a) equal-depth with the same bias correction; (b) general c without it.

**Response.** Done; both ablations are now rows of Table II.

| | Bias of d² (2ℓ–10ℓ), N = 1000 / 4000 | Median error of d, N = 1000 / 4000 |
|---|---|---|
| Ours (deepest c, corrected) | +1 % / 0 % | 0.095 / 0.059 |
| (b) Deepest c, no correction | +3 % / 0 % | 0.097 / 0.059 |
| BK equal depth (their formula) | +10 % / +6 % | 0.131 / 0.106 |
| (a) BK's equal-depth c, our corrected formula | +1 % / +2 % | 0.129 / 0.104 |

- **(b) General c without the correction.** With the deepest c, N_C is large and the correction makes no difference.
- **(a) Equal depth with the correction.** The correction removes Boguñá–Krioukov's bias but not their larger error.

So the two ingredients do different things:

- **The bias of BK on the causal set** comes from the uncorrected ratio of small counts (at their equal-depth elements N_C is small).
- **The accuracy gain** comes from the freedom to use the deepest c, which the identity provides. As the referee asked, this shows that the identity itself, and not only the correction, improves the estimator.

We also report that the equal-depth filter returns no estimate for 10–30 % of pairs.

**Change:** Table II, Sec. III "Tests" second paragraph.

### Major 3: the curvature estimator, intrinsic definition and benchmark

**(a) Window defined from counts.**

> The fit window, Hτ ∈ [0.2, 0.7], is chosen using H […] define it from counts alone […] and show how sensitive the result is to that choice.

**Response.** Done. The window is now every c with N_C ≥ 20, down to the deepest c whose rectangle lies in the sprinkled region. N_C ≥ 20 keeps the factor 1 − e^{−λ_C} negligible. No reference to H remains.

Because the window reaches Hτ ≈ 1, the τ⁴ term contributes. The target is therefore the value of the same fit on the exact continuum volumes of the same elements, R_fit^cont = 2.07–2.08 in de Sitter space, not 2. The text says so.

Sensitivity: varying the lower cut (N_C ≥ 5, 20, 50) and the upper cut (50, 75, 100 % of the largest τ²) changes the pooled de Sitter result only between 1.91 and 2.01 at ρ = 10⁴ (flat: −0.01 to 0.00). Each value is within 0.06–0.28 of that rule's continuum target; the largest offset belongs to the shortest window, which is also the noisiest.

**(b) Comparison with Benincasa–Dowker and chain abundances.**

> Compare the noise at equal density with the Benincasa–Dowker operator and with chain-abundance estimators (Roy–Sinha–Surya).

**Response.** Done, on the same de Sitter and flat sprinklings.

| Estimator (ρ = 4000) | Standard deviation of one estimate | Mean |
|---|---|---|
| Benincasa–Dowker, nonlocal 2D form, R = −2 B_ε[1], at the pair's midpoint, ε = 0.1 | ≈ 1.2×10³ | |
| same, ε = 0.03 | 160 | |
| same, ε = 0.01 | 23–30 | |
| same, ε = 0.003 | 2.7–4.5 | +0.7 (flat), +4.7 (dS): dominated by the truncated past light cone |
| Ordering fraction of one diamond of height 0.7 (about 10³ elements), curvature correction calibrated on the exact de Sitter continuum | 3.2 | 2.06 ± 0.22 (dS), −0.10 ± 0.23 (flat): unbiased |
| Depth drift of one pair (ours; common past of comparable size) | 3.5 | |

At ρ = 10⁴: chain abundance 2.1 (mean 1.87 ± 0.15 in de Sitter, −0.05 ± 0.13 in flat); our depth drift 2.4; Benincasa–Dowker 72–82 at ε = 0.01 (larger, as expected at fixed ε).

The honest conclusion, now in the paper: our estimator is **not** less noisy than the chain-abundance route at equal density. It is much less noisy than the local or weakly smeared Benincasa–Dowker operator, but that operator is built for the action, not for pointwise curvature. With stronger smearing (ε = 0.003) the Benincasa–Dowker spread comes down to ours, but its mean is then dominated by the truncation of the past light cone at the edge of our sprinkled region. A fair comparison at small ε needs a much larger region, which we have not run; the paper says so. Our estimator's distinctive features are geometric: curvature appears as the failure of an exact flat-space identity, and the new Eq. (12) says where in the region it is measured. We removed the v1 phrasing that leaned on "geometrically transparent" as an advantage without a benchmark.

**(c) The systematic low reading.**

> The systematic low reading (an offset of about −0.5 "cannot be excluded") should be resolved or modeled.

**Response.** Resolved for inserted pairs. With 1000 sprinklings per configuration (v1: 100), the offset is real for the v1 estimator. In flat space, with the v1 window, the mean of single-pair values is −1.94 ± 0.23 at ρ = 4000 and −0.52 ± 0.13 at ρ = 10⁴.

We tested two explanations:

1. **The factor 1 − e^{−λ_C} named in v1.** Negligible: λ_C ≳ 30 in the window.
2. **Correlated noise.** The regressor τ² and the response d² share N_A and N_B. We refitted after thinning each sprinkling at random into two independent halves, one for d² and one for τ². The offset did not disappear; it grew at the halved density. This is not the cause.

The cause is the form of the estimator. R = −16β/α is a ratio of the slope and intercept of one least-squares fit, whose errors are anticorrelated, so the mean of single-pair ratios is biased low. The bias shrinks with density, as observed.

The fix is to pool the fit coefficients over pairs before forming the ratio, R = −16⟨β⟩/⟨α⟩. With the count-defined window and inserted pairs, the pooled estimator agrees with the continuum target:

| | flat | de Sitter (target) |
|---|---|---|
| ρ = 4000, inserted pairs | −0.03 ± 0.02 | 1.97 ± 0.11 (2.07) |
| ρ = 10⁴, inserted pairs | −0.01 ± 0.02 | 1.99 ± 0.07 (2.08) |

v1 had already said that about 100 pairs are needed, so pooling costs nothing in practice. Table III now reports the pooled estimator with bootstrap errors.

**(d) Sprinkled pairs.**

> Tests insert a and b by hand. Please also show results for sprinkled pairs.

**Response.** Done (Table III, "sprinkled" rows): a and b are the sprinkled elements nearest to the two target points. Here a residual low reading remains:

| | de Sitter (target 2.07) | flat |
|---|---|---|
| ρ = 4000, sprinkled pairs | 1.70 ± 0.11 | −0.07 ± 0.02 |
| ρ = 10⁴, sprinkled pairs | 1.84 ± 0.07 | −0.04 ± 0.02 |

In de Sitter space the shortfall is 0.37 ± 0.11 at ρ = 4000 and 0.24 ± 0.07 at ρ = 10⁴, so it decreases with density. We have not identified its cause, and the paper says so (Sec. IV and Limitations).

**(e) The FRW weighting kernel.**

> Deriving the weighting kernel, or at least its leading form, would turn an observation into a result.

**Response.** Derived. For any 1+1 FRW metric a = e^{σ(η)}, expanding the three rectangle volumes in the depth of c gives a new equation, Eq. (12), with the derivation in Sec. IV:

1 − d²_est/d² = (τ²/16) [R − (τ/3) dR/dτ + O(τ²)].

Here R and its derivative along the worldline are evaluated at a, b. To leading order the drift measures R one third of the way down from a, b to c. That is the mean depth of a triangular weight 2(τ − s)/τ² on depths s ∈ [0, τ].

The derivation is done symbolically in `sims/r38_drift_kernel.py` and checked against the exact power-law volumes. For p = 1 the exact values at τ = 0.02, 0.05, 0.1 are −0.3982, −0.4073, −0.4200; the two-term formula gives −0.3997, −0.4068, −0.4185. The other two values of p agree equally well.

**Change for Major 3:** Sec. IV, new paragraphs "Window from counts", "Pooling" and "Comparison with other estimators at equal density"; new Eq. (12) and its derivation; Table III rebuilt; abstract; Limitations.

### Major 4: focus and structure

> Building the paper around Secs. III–IV […] keeping the embedding calibration (Sec. VI) as a supporting diagnostic; reducing the propagator target (Sec. V) to a short section or appendix.

**Response.** Done as suggested.

- **Main line.** The title, abstract and introduction now present one identity and its use for distance and curvature: "Spatial distance and curvature from an exact counting identity in two-dimensional causal sets".
- **Propagator target.** Moved to Appendix A. Its opening sentence states its limited role: an exact, density-free check of implementations of the chain sum, not a stronger manifoldlikeness diagnostic.
- **Embedding test.** Sec. V is titled "A supporting diagnostic".
- **No separate Note.** We did not split the Laguerre identity into a CQG Note.

**Change:** title, abstract, Introduction (rewritten list of contents), Sec. V title, Appendix A.

### Major 5: why the null-pair fraction is needed

> Explain what the null-pair fraction adds. One answer could be that it repairs the embedding test so the test can be used alone; if that is the argument, make it explicitly.

**Response.** That is the argument, and it is now explicit (Sec. V, new paragraph "What z adds"):

- **It detects nothing new.** On our states the fixed-size ordering fraction separates the same groups; height, Myrheim–Meyer dimension, interval abundances and graph observables also detect layered orders.
- **Its role is to make the embedding test usable on its own.** Without it the test passes some 10-layer orders. With it the test needs no second statistic, and z uses only quantities the embedding already computes.

**Change:** Sec. V, last paragraph before Fig. 4.

### Major 6: the e^{−βS} states

> The abstract's claim that the diagnostics "separate the continuum-like and layered phases" should be worded the same way. The bracket 0.05 < β_c(400) < 0.45 is too loose […] Present it as a statement of compatibility only.

**Response.** Done.

- **Abstract.** The phase-separation claim is removed (the e^{−βS} application is no longer in the abstract).
- **Sec. VI.** It now opens the N = 400 paragraph by calling the states "test configurations, representative of the two phases, not equilibrium samples".
- **Bracket.** It now reads: "compatible with the finite-size scaling … of Ref. [GOS18]; it is too loose to test it".

### Major 7: references

**Response.** Added, after checking each against its arXiv record (and journal record where available):

- **Spatial distance and induced geometry:**
  - Major, Rideout and Surya, CQG 23, 4743 (2006) and J. Math. Phys. 48, 032501 (2007);
  - Eichhorn, Surya and Versteegen, CQG 36, 105005 (2019).
- **Curvature and boundary terms in small diamonds:** Khetrapal and Surya, CQG 30, 065005 (2013), next to Roy–Sinha–Surya.
- **2D orders and the observables that distinguish the phases:**
  - Glaser–O'Connor–Surya (already cited);
  - Glaser–Surya, arXiv:1410.8775;
  - Glaser, "The Ising model coupled to 2d orders", doi:10.1088/1361-6382/aab139;
  - Glaser, "Computer simulations of causal sets", arXiv:2306.09904.

  These are discussed in Sec. V ("What z adds"), with the observables used there: the action, ordering fraction, height and interval abundances. For two of them we could not confirm the journal reference, so they are cited by arXiv number.

**Change:** Introduction, Sec. V, bibliography.

---

## Minor comments

### Minor 1: Fig. 3, correlated depth bins

> Neighbouring depth bins are correlated at the 0.9 level. Show the correlation explicitly, or use bins that do not share elements.

**Response.** Shown explicitly. We computed the full correlation matrix of the bin means from the spread over the 400 sprinklings (`sims/out/r37_binscorr.txt`):

- adjacent bins in de Sitter space: 0.80, 0.81, 0.90, 0.94, 0.96, from shallow to deep;
- adjacent bins in flat space: 0.80–0.97;
- bins two apart: still 0.5–0.9.

The text gives these values. The caption of Fig. 3 warns that the error bars are not independent. We kept bins that share elements: disjoint sets of sprinklings per bin would multiply the error bars by about 2.5. The curvature estimate does not use the bins at all; it fits all elements c of each pair directly.

**Change:** Sec. IV, "Test on sprinklings"; caption of Fig. 3.

### Minor 2: "Lorentz transformation to within 3–10%"

**Response.** Defined. The best affine map from the reconstructed to the true coordinates, x_true ≈ A x_rec + b, satisfies max_ij |(AᵀηA − η)_ij| = 0.03–0.10.

**Change:** Sec. V, "Embedding".

### Minor 3: Tables I and II use different pair selections

**Response.** Now stated at the start of the Tests paragraph. Table I and Fig. 2 use late elements, which have large common pasts; Table II uses the middle of the diamond, where both a common past and a common future exist but are smaller.

### Minor 4: abstract

**Response.** Rewritten to lead with the identity, the estimator and the curvature result. The embedding test is one sentence; the Laguerre identity is one sentence, as an appendix.

### Minor 5: Hu–Meyer–Meyer citation and arXiv numbers

> The journal year is 2025 (J. Math. Phys. 66, 122502) but the arXiv ID 2601.03280 begins 2601 (January 2026). Also check the arXiv numbers of the 2026 preprints.

**Response.** Checked; no change needed (declined), because the citation is correct. The article is J. Math. Phys. 66, 122502, dated 26 December 2025. It was submitted to arXiv on 31 December 2025, which gives the 2601 number, and the arXiv record carries the same journal reference. We also checked the 2026 preprints against their arXiv records: 2606.04910 (Barton, Borza, Röhrig) and 2605.27514 (Eichhorn, Mack, Le, Wagner).

### Minor 6: data availability, persistent identifier

**Response.** Agreed. The repository will be made public, and the tagged version used for the paper archived on Zenodo with a DOI, after submission. v2 keeps a placeholder for the DOI in the Data availability statement.

### Minor 7: IOP style

**Response.** Agreed. The final version will be typeset in the IOP class with IOP reference style. v2 keeps the current format so that the referee can compare versions.

---

## Other changes not prompted by the review

- The FRW sprinkling test is kept but relabelled: the number quoted (−1.25 ± 0.30) is the mean of single-pair fits, as in v1, before pooling.
- Data availability lists the new scripts.
- The appendix of other approaches is now Appendix B.
- No latexdiff PDF this round.

## Results still marked as placeholders in v2 (not to be assessed)

- Sec. VI: the N = 800 held-out test of the null-pair flag (cluster job r27, still running), as in v1.
- The Zenodo DOI in the Data availability statement.
