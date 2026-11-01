# Answer to the referee: toolkit-1p1, round 3 (CQG)

**Manuscript:** "Spatial distance and curvature from an exact counting identity in two-dimensional causal sets" (R. Bada).
**This answer** responds to `review-toolkit-1p1-v3.md` and comes with `toolkit-1p1-v4.pdf` and `toolkit-1p1-v4-diff.pdf` (latexdiff against v3).

**Placeholder remaining in the manuscript (one):** the **Zenodo DOI** (Data availability, `[Zenodo DOI]`). It will be minted when the repository is made public at submission.

**r27 is filled** (Sec. VI; see comment 23). The held-out N = 800 test found one false positive among 20 continuum-like states, close to the threshold. Sec. VI and Limitations report it.

In addition, the Data availability statement is now a commitment (comment 23): the repository is still private.

We thank the referee for the third report. In summary:
- Comments 18–22 are handled as described in the report.
- Two of them led to new laptop runs, `sims/r41_curvature_round3.py` (summary in `sims/out/r41_noise_matched.txt`):
  - **Comment 19.** The P pairs of the one-region comparison had been drawn one at a time, which is the single-uniform-draw mechanism. We reran the comparison with a position-based selection.
  - **Comment 22.** The flat control is rerun at matched element count.

  The rerun of comment 19 changes the explanation slightly. The in-region low bias is not a selection effect: it is the ratio bias of one region, as v3 said.
- Comment 24 (optional) was not run. The Discussion now says plainly that the curvature result is analytic and conceptual, and states the selection-bias finding as a methodological point.

---

## Comment 18: the abstract is more favourable to the curvature estimator than Sec. IV

> "Pooled over many pairs, a fit of this depth drift reproduces the same fit on the exact continuum volumes … with sprinkled pairs selected independently of their neighbourhoods" is true as an average over 1000 independent sprinklings. Within one region, Sec. IV and Limitations report a low bias […]. The abstract should say so. "Not more precise than the ordering fraction" understates the result. In de Sitter space the ordering fraction's spread is about a third of the drift's […]. Suggested: "for the curvature of a given region it is less precise than the ordering fraction and, within one region, biased low". Separately, at ρ = 4000 the "windows" row (1.91 ± 0.10 against a target of 2.08) is 1.7σ low. That is acceptable, but "reproduces" is then a little generous for that row.

**Response.** All three points are adopted.
- The abstract now says that the agreement holds "on average over independent sprinklings".
- It uses the referee's wording, with the factor of three.
- It qualifies the sprinkled-pair agreement as "within 1.7σ".

The body states each σ.

**Changed text, abstract:**

> A fit of this depth drift, pooled over many pairs, reproduces on average over independent sprinklings the same fit on the exact continuum volumes, for pairs inserted by hand (de Sitter, flat and FRW sprinklings) and for all sprinkled pairs of a position-based selection (de Sitter and flat, within 1.7σ); selecting the elements nearest to given points biases it low. On a sprinkling of a causally convex region, such as an interval of the causal set, its window needs no coordinates. For the curvature of a given region, however, it is less precise than the ordering fraction (in de Sitter space its spread between sprinklings is about three times larger) and, within one region, biased low.

**Where the abstract's numbers come from.**
- "About three times": Sec. IV gives 2.32 against 0.80 at ρ = 4000 and 1.34 against 0.46 at ρ = 10⁴, ratios 2.9 and 2.9.
- "Within 1.7σ": 1.91 ± 0.10 against 2.08 in Table III, offset −0.164 ± 0.097 in `sims/out/r40_select.txt`. The other density is within 1.1σ.

**Changed text, Sec. IV ("Sprinkled pairs"):**

> This removes most of the shortfall: the pooled estimate is 1.91 ± 0.10 and 2.02 ± 0.06 in de Sitter space against continuum values 2.08 (1.7σ and 1.1σ below, against 0.9σ and 1.1σ for inserted pairs), and 0.00 ± 0.02 and −0.01 ± 0.01 in flat space (Table III); in the causally convex region it is 2.10 ± 0.08 and 2.04 ± 0.06 against 2.03 and 2.04.

The "Pooling" paragraph said "within 1.2σ at both densities" for inserted pairs. From `r40_select.txt` the offsets are 0.9σ and 1.1σ, so it now reads "within 1.1σ".

**Changed text, Limitations:**

> Within one region the pairs share elements, so pooling more than a few tens of them gains little and the estimate retains a low ratio bias of 0.05–0.43 at the densities used; for the curvature of a given region the ordering fraction is more precise, by a factor of about three in de Sitter space, and less biased.

---

## Comment 19: scope of the Mecke argument

> The argument covers sums over all pairs with a weight that depends only on the pair's *positions*, independently of the rest of the configuration. Sec. IV then generalizes: "On a causal set without coordinates the windows are replaced by any rule of this kind, for example all pairs within a range of count-defined separations." […] Please either: (a) test it […]; or (b) remove the example and state the condition precisely […]. The abstract's "selected independently of their neighbourhoods" is also loose […]. "Pooled over all pairs of a position-based selection" is the correct condition. Please also state how the P pairs of the one-region comparison were drawn. A fixed number drawn from the qualifying pairs carries a P/N_pairs weight. That is presumably negligible at these sizes, but it is the same mechanism as the single uniform draw.

**Response.** We took route (b), and checked the last point with a rerun.

**(b) The example is removed and the condition stated.**

> The unbiased use of sprinkled pairs follows from the Mecke formula: a sum over all pairs of points of a Poisson process, with a weight that depends only on the positions of the pair and not on the rest of the configuration, equals the average over pairs placed by hand at the same positions. The condition is therefore a sum over all pairs of a selection that does not depend on the counts used by the estimator, optionally thinned at random with a fixed probability; the ratio is formed from the pooled sums. […] In practice, therefore, the estimator is to be pooled over all pairs of a position-based selection, not over a single representative chosen per region. A selection by count-defined separation does not satisfy the condition, because it depends on the same counts as the estimator, and we have not tested it.

The abstract and Limitations now say "all pairs of a position-based selection"; "independently of their neighbourhoods" is gone.

**How the P pairs were drawn, and the rerun.** In v3 the pairs were drawn sequentially:
- a uniformly among the elements of the target region (η ∈ [−1.25, −1.05], |x| ≤ 0.1);
- then b uniformly among the elements spacelike to a at the required offset;
- repeated P times, with replacement.

This is the single-uniform-draw mechanism the paper itself shows to be biased. Because the v3 in-region bias was of the same size as that mechanism's, we did not assume it was negligible. `sims/r41_curvature_round3.py` reruns the comparison on the same 400 sprinklings (same seeds) with a position-based selection:
- every qualifying pair is kept with a fixed probability q_P;
- q_P is the same in every sprinkling, set from ten pilot sprinklings that are not analysed;
- the thinning is nested.

Results:

| de Sitter, P ≈ 100 | ρ = 4000 | ρ = 10⁴ |
|---|---|---|
| continuum fit of the same c's | 2.10 | 2.10 |
| v3 sequential draw: mean ± s.d. | 1.63 ± 2.25 | 1.92 ± 1.33 |
| position-based: mean ± s.d. | 1.67 ± 2.32 | 1.95 ± 1.34 |
| position-based, offset of the per-region mean | −0.43 ± 0.12 | −0.15 ± 0.07 |
| position-based, ratio formed after pooling Σβ, Σα over all 400 sprinklings | 1.96 ± 0.12 | 2.04 ± 0.07 |
| ordering fraction: mean ± s.d. | 2.05 ± 0.80 | 1.99 ± 0.46 |

What the rerun shows:
- **Selection.** It does not explain the in-region bias: the position-based selection gives the same per-region mean within the errors.
- **The ratio.** The bias is the ratio bias of one region. With the same pairs, forming the ratio from sums pooled over all sprinklings brings the estimate back to the level of Table III's windows rows. The flat control shows this more cleanly (comment 22): pooled over sprinklings, the position-based selection gives +0.01 ± 0.04 and +0.01 ± 0.03, but per region −0.16 and −0.05.
- **The sequential draw.** In flat space it keeps an extra −0.10 ± 0.04 and −0.05 ± 0.03 even after pooling over sprinklings. That is the 1/N_W selection effect, here small next to the ratio bias.

The paper now uses the position-based selection for the one-region comparison, describes it, and gives the sequential-draw numbers as a check.

**Changed text, Sec. IV ("Comparison with other estimators"):**

> In each sprinkling we take every spacelike pair with a near the top of the diamond (η_a ∈ [−1.25, −1.05], |x_a| ≤ 0.1) and b at x_b − x_a ∈ [0.1, 0.2], |η_b − η_a| ≤ 0.05 (9ℓ–17ℓ apart at ρ = 10⁴), keep each with a fixed probability, the same in every sprinkling, chosen so that P pairs remain on average (a position-based selection in the sense above), and pool the depth drift over them. […] the pooled drift gives 1.67 ± 2.32 and 1.95 ± 1.34 for P = 100, against continuum values 2.10 of the same fit: its spread is about three times larger. Pooling more pairs barely helps (standard deviation 2.78, 2.50, 2.32, 2.27 for P = 10, 30, 100, 300 at ρ = 4000), because pairs in one region share most of their common pasts. For the same reason the ratio bias is not averaged away within one region: the estimate reads low by 0.43 ± 0.12 and 0.15 ± 0.07. It is the ratio that is biased, not the sums: forming the ratio from Σβ and Σα pooled over all 400 sprinklings gives 1.96 ± 0.12 and 2.04 ± 0.07. Drawing the pairs one at a time instead (a uniformly among the elements near the top, then b uniformly among those at the required offset) gives the same within the errors in de Sitter space (1.63 and 1.92).

---

## Comment 20: the "about 30 %" in the FRW result

> From the numbers in Sec. IV, the continuum target exceeds the Eq. (12) fit by 35 %, 44 % and 53 % […]. Equivalently, Eq. (12) falls short of the target by 26–34 %. […] Please make the two agree. The abstract still says that in any FRW spacetime "the leading failure measures the scalar curvature one third of the way from the pair to c". […] add "to leading order in the depth" or similar.

**Response.** We use the second reading, "falls short of", in both places, and the abstract is qualified.

From the unrounded values in `sims/out/r40_frw.txt` (target −0.699, −0.790, −0.901; Eq. (12) −0.518, −0.557, −0.588), the shortfall is 25.9 %, 29.5 % and 34.7 %, which we quote as 26–35 %. The referee's 26–34 % comes from the rounded values.

**Changed text, Sec. IV ("FRW spacetime"):**

> Over a realistic window Eq. (12) therefore gives the direction of the effect, a curvature measured below the pair, but falls short of its size by 26–35 % in the three windows; the size is set by the exact continuum fit, which the counts reproduce.

**Changed text, Limitations:**

> In FRW spacetime the leading-order prediction of Eq. (12) falls short of this target by 26–35 % over realistic windows.

**Changed text, abstract:**

> […] and in any 1 + 1 FRW spacetime, to leading order in the depth, the failure measures the scalar curvature one third of the way from the pair to c.

---

## Comment 21: "in a causally convex region its window is set by the order alone"

> (a) f is not needed. The estimator counts only A, B and C, which lie in I(c, a) ∪ I(c, b) […]. (b) Convexity is an assumption, not something the order decides. […] Suggested wording: "on a sprinkling of a causally convex region, for example an interval of the causal set, every c in the common past can be used, so the window needs no coordinates; otherwise the boundary must first be inferred [31]". Also, Table III's caption still says "count-defined window" while the paragraph is now "Window from the order".

**Response.** We agree on all three points.
- **(a)** The argument now rests on I(c, a) ∪ I(c, b), and f is dropped.
- **(b)** The referee's wording is used, with convexity stated as an assumption.
- **(c)** The Table III caption is changed.

The window's lower limit is now phrased in terms of I(c, a) and I(c, b) rather than the whole rectangle. This matches what the box tests did: the code checks the outer corners of I(c, a) and I(c, b) (`multi_counts` in `sims/r40_curvature_round2.py`), not the join.

**Changed text, Sec. IV ("Window from the order"):**

> The fit uses every c with N_C ≥ 20, which keeps the factor 1 − e^(−λ_C) of Eq. (4) negligible, down to the deepest c whose intervals I(c, a) and I(c, b) lie in the sprinkled region. Neither limit refers to H. The estimator counts only A, B and C, which lie in I(c, a) ∪ I(c, b); the tile D is never counted. In a causally convex region that contains c, a and b, these intervals lie in the region. On a sprinkling of a causally convex region, for example an interval of the causal set, every c in the common past can therefore be used, so the window needs no coordinates; otherwise the boundary must first be inferred, which in 1 + 1 dimensions is possible from the order [31]. Convexity is an assumption about the sprinkled region: the order decides it only when the causal set is itself defined from the order, as an interval is. Our main tests use a coordinate box, where we decide the condition from the coordinates. We therefore repeated them in a causally convex region, the past of the point (−0.95, 0) cut at η = −3 (convex, although the cut is not defined by the order), with every c of the common past used (1000 sprinklings each).

**Changed text, Table III caption:**

> Pooled curvature estimator R_est = −16Σβ/Σα over 1000 sprinklings (H = 1; window as in Sec. IV: N_C ≥ 20, down to the deepest c with I(c, a) and I(c, b) in the box).

"Count-defined window" was also removed from the FRW paragraph ("the window of the previous paragraphs"), from Limitations ("Because the window reaches Hτ ≈ 1") and from the Data availability description.

---

## Comment 22: the flat control in the one-region comparison is not at equal input

> The flat diamond of the same coordinate size holds 8.4×10³ elements against 2.5×10³ for the de Sitter one at ρ = 4000. […] Either match the element count, or state the difference where the result is quoted.

**Response.** We reran the flat control at matched element count: the same diamond at ρ = 4000 × 2511/8413 = 1194 and ρ = 10⁴ × 6280/21034 = 2986, i.e. 2.5×10³ and 6.3×10³ elements. The result changes: in flat space the two methods are no longer equal. The ordering fraction is slightly more precise.

| flat, P ≈ 100, mean ± s.d. between 400 sprinklings | 2.5×10³ elements | 6.3×10³ elements |
|---|---|---|
| ordering fraction | 0.01 ± 0.80 | 0.03 ± 0.50 |
| depth drift, position-based selection | −0.16 ± 0.89 | −0.05 ± 0.54 |
| depth drift, v3 sequential draw | −0.16 ± 0.84 | −0.08 ± 0.52 |

For comparison, v3 at 8.4×10³ elements (ρ = 4000): ordering fraction 0.01 ± 0.43, drift −0.10 ± 0.44.

**Changed text, Sec. IV:**

> In a flat diamond of the same coordinate size, at a lower density so that it holds the same number of elements as the de Sitter diamond (2.5×10³ and 6.3×10³), the ordering fraction gives 0.01 ± 0.80 and 0.03 ± 0.50, and the pooled drift −0.16 ± 0.89 and −0.05 ± 0.54 (low by 0.16 ± 0.04 and 0.05 ± 0.03). As a curvature estimator for a given region, the ordering fraction is therefore more precise, by a factor of about three in de Sitter space and slightly in flat space, and less biased.

"The two spreads are equal" no longer appears anywhere in the manuscript.

---

## Comment 23: data availability and placeholders

> The statement says the code and notebook "are openly available" at the GitHub URL, while the responses say the repository will be made public on submission. The statement must be true when the paper is submitted, and the same applies to Ref. [46]. The Zenodo DOI remains a placeholder. […] The r27 held-out test has now been a placeholder for three rounds. […] it must be filled, and checked, before submission.

**Response.**
- **Data availability and Ref. [46].** Both are worded as a commitment:

  > The code that produces every number and figure in this paper, and the research notebook in which the work was carried out, will be made openly available at https://github.com/presindev/causet-counting when this paper is submitted, and the version used for this paper archived with a persistent identifier [Zenodo DOI].

  > R. Bada, Two causal-set papers written with an AI research partner: methodology note (2026), to be released with the code at https://github.com/presindev/causet-counting.

- **Zenodo DOI.** A Zenodo DOI for a GitHub release is minted when a public release is made. It will therefore be minted when the repository is made public at submission, and entered in the submitted version. We accept that the editor may make it a condition of acceptance.
- **r27.** Fetched and filled. The output is in `sims/out/r27_n800_heldout.txt` (job cluster 450475, all 28 chains complete). The threshold (z > 0.120, from 50 fresh flat orders; `sims/out/r27_calibrate.txt`) and the classes (≥ 20 layers continuum-like, 4–19 layered) were fixed in `sims/r27_n800_detector.py` on 29 October, before the job ran. Results:
  - **Layered states.** All 8 (14–19 layers) are flagged, z = 0.38–0.57. One of them has stress 0.072, inside the flat band: the embedding spectrum alone would have passed it, and z catches it. This is the blind spot of Sec. V, now on held-out data.
  - **Continuum-like states.** 19 of 20 (27–56 layers) are not flagged, z ≤ 0.107.
  - **The one false positive.** A 27-layer state at β = 0.3 has z = 0.123, just above 0.120. Its acceptance rate is 5 %, against 53–54 % for the other three β = 0.3 chains (43–50 layers), which suggests it is partly layered. By the classes fixed in advance, however, it counts as a false positive, and we report it as one.
  - **Stress.** Three of the 19 unflagged continuum-like states have stress 0.086–0.110, slightly above the N = 800 flat band (mean + 2 s.d. = 0.081). The stress statistic alone would reject them. The flag under test does not.

  **New text, Sec. VI:**

  > […] we ran 28 chains (β ∈ {0.01, 0.05, 0.1, 0.2, 0.3, 0.45, 0.7}, 4 seeds each, random initial orders, 2000 sweeps), with the classes also fixed in advance (at least 20 layers: continuum-like; 4–19 layers: layered). All 8 layered states (14–19 layers) are flagged (z = 0.38–0.57), including one whose stress (0.072) lies in the flat band, which the embedding spectrum alone would have passed. Of the 20 continuum-like states (27–56 layers), 19 are not flagged (z ≤ 0.107). The exception has 27 layers at β = 0.3 and is flagged with z = 0.123, just above the threshold; its acceptance rate (5 %, against 53–54 % for the other three chains at β = 0.3, which reached 43–50 layers) suggests that it is partly layered, but by the classes fixed in advance it is a false positive. Three of the 19 unflagged states have a stress slightly above the flat band at N = 800 (0.086–0.110, against flat mean plus two standard deviations, 0.081), so at this size the stress alone would also reject some continuum-like states.

  **New text, Limitations:**

  > The embedding thresholds are empirical and must be recalibrated at each N; on held-out states at N = 800 the layered flag caught every layered state but also one of 20 continuum-like states, just above its threshold; […]

  The claims that z "lets the test reject layered orders on its own" (abstract, Introduction) stand: 8 of 8 layered states are flagged.

---

## Comment 24 (optional): a locality test

> take an FRW spacetime, or one with spatially varying curvature; compare the pooled drift of pairs at a given location with the ordering fraction of diamonds of matched footprint and element count; report which resolves the variation better. […] If not, the Discussion should say plainly that the curvature result is analytic and conceptual. The Discussion could also mention the selection-bias finding of comment 8 as a methodological point of general use.

**Response.** Not run in this round. We agree it is the one test that could restore a practical use for the estimator, and it is the first item for further work.
- **Why not now.** It needs a design choice we want to make carefully rather than quickly: what "resolves the variation better" means. Candidates are the error on a curvature difference between two locations, or the error on the time derivative in FRW.
- **What we expect.** The noise results of comments 18 and 22 make an advantage uncertain: in de Sitter space the drift's spread at one location is three times the ordering fraction's.

As the referee asks, the Discussion now says this plainly and states the selection-bias point.

**New text, Discussion ("What the curvature result is"):**

> Since the ordering fraction of a region is the more precise estimate of its curvature, the curvature result of this paper is analytic and conceptual: an exact flat-space identity whose depth-dependent failure has a closed form, Eq. (11), and a leading-order meaning, Eq. (12). Whether the locality of the depth drift, a curvature along one pair and one depth, makes it the better estimator where curvature varies across a region is untested. A methodological point is of more general use: estimators evaluated on sprinkled elements chosen as the nearest to given points, or one per window, inherit a Palm-type selection bias, because the choice depends on the neighbourhood that the estimator counts; summing over all elements or pairs of a position-based selection, as the Mecke formula requires, removes it.

---

## Status of earlier comments

| # | Status after round 3 (referee) | v4 |
|---|---|---|
| M1, M2, M4–M7, M3 | resolved | unchanged |
| 8 | resolved in substance; scope → 18, 19 | 18, 19 handled |
| 9 | resolved; one number → 20 | 20 handled |
| 10 | resolved; abstract → 18; flat control → 22 | 18, 22 handled (flat rerun) |
| 11–13, 15–17 | resolved | unchanged |
| 14 | partially resolved → 21 | 21 handled |
| m6 (DOI) | placeholder | still a placeholder (see top) |
| r27 (placeholder since round 1) | must be filled before submission | filled (comment 23) |
| m7 (IOP style) | deferred to the final version | unchanged |

## Other changes

- "Pooling" paragraph: "within 1.2σ" → "within 1.1σ" for inserted pairs (comment 18). The unrounded offsets are 0.9σ and 1.1σ.
- Data availability lists the new script `sims/r41_curvature_round3.py`.
- Header comment of the .tex records the v4 changes. This is a LaTeX comment and does not appear in the PDF.
- Abstract numbers checked against the body and the output files:
  - "two" and "ten discreteness lengths": Tables I–II;
  - the de Sitter closed form: Eq. (11);
  - "about three times": 2.32/0.80 and 1.34/0.46, `sims/out/r41_noise_matched.txt` and `sims/out/r40_noise.txt`;
  - "within 1.7σ": Table III, `sims/out/r40_select.txt`.

## Placeholders

1. Zenodo DOI (Data availability). To be minted at submission, when the repository is made public.

r27 is filled (comment 23).
