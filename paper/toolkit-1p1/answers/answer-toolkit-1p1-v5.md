# Answer to the referee: toolkit-1p1, round 4 (CQG)

**Manuscript:** "Spatial distance and curvature from an exact counting identity in two-dimensional causal sets" (R. Bada).
**This answer** responds to `review-toolkit-1p1-v4.md` (recommendation: accept once comments 25–29 are made) and comes with `toolkit-1p1-v5.pdf` and `toolkit-1p1-v5-diff.pdf` (latexdiff against v4).

**Placeholders and preconditions remaining in the manuscript:**
1. **Zenodo DOI** (Data availability, shown in red as "[Zenodo DOI]"). It has not been minted yet. **It can exist before upload.** Zenodo's GitHub integration mints a DOI when a release is published, and the code is final. So the order is:
   - make the repository public;
   - tag the release;
   - copy the DOI into this paper and into the companion (same release);
   - rebuild.

   The tagged snapshot will contain this file with the placeholder still in it. That is harmless, because the DOI identifies the code, not the PDF. If the DOI is not available by upload, the editor's condition of acceptance applies, as the referee proposed.
2. **Repository public (precondition, not a placeholder).** As comment 29 asks, Data availability and Ref. [47] (the methodology note, Ref. [46] in v4; see "Other changes") are now in the present tense. At the time of writing, `github.com/presindev/causet-counting` is still **private**. The sentences become true only when the author publishes the snapshot (`release/make_public.sh --push`) and switches the repository to public. This must happen **before** upload.

We thank the referee for the fourth report, and in particular for correcting the abstract phrase in comment 25. Comments 25–29 are handled below. One further change, a missing citation, is listed under "Other changes".

New code:
- `sims/r42_flat_height.py` (heights of random 2D orders, for comment 28c; laptop, seconds), output `sims/out/r42_flat_height.txt`.
- A short laptop check of the flat-control geometry for comment 27a, reported below. It is not quoted as a number in the paper beyond "about four times".

---

## Comment 25: abstract, "reproduces on average over independent sprinklings"

> "On average over independent sprinklings" reads naturally as the mean of the per-sprinkling estimates. That mean is biased low: 1.67 against 2.10, Sec. IV […]. What Table III reports, and what Mecke guarantees, is the ratio of fit coefficients summed over the pairs of many sprinklings before the ratio is formed. Suggested: "A fit of this depth drift, with its coefficients summed over the pairs of many independent sprinklings, reproduces the same fit on the exact continuum volumes …". The Limitations sentence "The curvature estimator must be pooled over all pairs of a position-based selection" could add "… and over many independent regions; within one region the ratio stays biased (below)".

**Response.** We agree, and used both suggested wordings.

**Changed text, Abstract** (the rest of the sentence is unchanged):

> A fit of this depth drift, with its coefficients summed over the pairs of many independent sprinklings, reproduces the same fit on the exact continuum volumes, for pairs inserted by hand (de Sitter, flat and FRW sprinklings) and for all sprinkled pairs of a position-based selection (de Sitter and flat, within 1.7σ); selecting the elements nearest to given points biases it low.

**Changed text, Discussion, Limitations:**

> The curvature estimator must be pooled over all pairs of a position-based selection and over many independent regions; within one region the ratio stays biased (below). Single pairs are dominated by noise and their ratio is biased, and selecting the elements nearest to given points, or one element per window, biases it low.

**Search.** "On average" and "average over" now occur only in three places, none of them in the per-region sense:
- the Introduction, on Johnston's sum over chains, "whose average over sprinklings reproduces the Klein–Gordon propagator";
- Sec. II, "contains one element on average";
- Sec. IV, "P pairs remain on average", which describes the thinning.

---

## Comment 26: Sec. IV, "Test on sprinklings" (Fig. 3)

> This paragraph still says "every sprinkled c in their common past whose rectangle lies inside the region". That is the v3 rule […]. If Fig. 3 was made with the interval rule, please update the sentence. If it really uses the stricter rectangle rule, please say that Fig. 3 uses a stricter cut than the fit.

**Response.** We checked the code. **Fig. 3 uses the stricter rule.**
- `sims/fig_part1.py` (`fig_drift`) calls `s4a_desitter.run`.
- At `sims/s4a_desitter.py:69–72`, that function keeps c only if the two corners (u_c, v_j) and (u_j, v_c) lie in the box, where (u_j, v_j) is the join of a and b. That is the rectangle from c to the join, the smallest rectangle containing I(c, a) and I(c, b).
- It also keeps only c with N_C > 0 (no N_C ≥ 20 cut). Fig. 3 bins single-c ratios and fits nothing, so the sentence does not mention that cut.

**Changed text, Sec. IV, "Test on sprinklings":**

> … insert a, b by hand ≈14ℓ apart, and evaluate Eq. (4) for every sprinkled c in their common past such that the smallest rectangle containing I(c, a) and I(c, b) lies in the region. This cut is stricter than the window of the fit below, which requires only the two intervals to lie in the region.

---

## Comment 27 (optional): flat control lever arm; "within 1.1σ"

> The flat diamond is matched in element count, but […] it is not matched in proper depth. With u, v ∈ [−3, −0.95]: the pairs at η ≈ −1.15 see c down to a proper time of ≈ 1.85 in flat space; in de Sitter space the same c are only ≈ ln(3/1.15) ≈ 0.96 below. The lever arm in τ² is therefore ≈ 3.5 times longer in the flat control. […] A short remark would stop readers from attributing the de Sitter vs flat contrast (×3 vs "slightly") to curvature.
>
> Also, the "Pooling" paragraph says "within 1.1σ at both densities" for inserted pairs. From the rounded Table III values the second is (2.08 − 1.99)/0.07 = 1.3σ. Either quote the unrounded entries or say 1.3σ.

**Response (a).** We checked the geometry, and the referee's reading is right.
- **Setup.** `sims/r41_curvature_round3.py` and `r40_curvature_round2.py` use u = η − x, v = η + x ∈ [−3, −0.95]. The flat control uses the same coordinates at a lower density. The pairs have a at η ∈ [−1.25, −1.05] and b offset by 0.1–0.2 in x.
- **Fitted quantity.** For a = (−1.15, 0) and b = (−1.15, 0.15), we computed the quantity the fit uses, τ² = V(I(c, a)) + V(I(c, b)), from the exact volumes.
- **At the deepest c, the bottom tip:** 3.41 in flat space against 0.88 in de Sitter space, a ratio of 3.9.
- **Over the c of the common past,** sampled with each geometry's density: standard deviation 0.75 against 0.19 (ratio 3.9); mean 0.91 against 0.26.
- **Conclusion.** The τ² lever arm is about four times longer in the flat control. The referee's 3.5 is (1.85/0.96)² ≈ 3.7, from the straight-down depth. For comparison, the drift's spread falls from 2.32 to 0.89 (a factor of 2.6).

**Changed text, Sec. IV, after the flat-control numbers:**

> The flat control is matched in element count, not in proper depth: in the same coordinates the deepest c lies about 1.85 below the pairs in flat space, against ln(3/1.15) ≈ 0.96 in de Sitter space, so the range of τ² over which the drift is fitted is about four times longer. That alone makes the flat drift less noisy, so the difference between the two geometries in the factors below largely reflects this lever arm, not curvature.

The sentence that follows is unchanged: "As a curvature estimator for a given region, the ordering fraction is therefore more precise, by a factor of about three in de Sitter space and slightly in flat space, and less biased." The within-geometry comparisons it states are fair, as the referee notes.

**Response (b).** The unrounded entries (`sims/out/r40_select.txt`, inserted pairs) are:
- ρ = 4000: offset −0.095 ± 0.111, i.e. 0.86σ;
- ρ = 10⁴: offset −0.081 ± 0.072, i.e. 1.13σ.

The 1.3σ comes from rounding 2.075 up to 2.08 and 1.994 down to 1.99. The "Sprinkled pairs" paragraph already gave "0.9σ and 1.1σ for inserted pairs". We now say the same in "Pooling" and quote the unrounded values.

**Changed text, Sec. IV, "Pooling":**

> With inserted pairs it agrees with the continuum value of the same fit, in flat space within the errors and in de Sitter space within 0.9σ and 1.1σ (offsets −0.095 ± 0.111 and −0.081 ± 0.072 before rounding).

We also checked the window-pair values: −0.164 ± 0.097 = 1.69σ and −0.065 ± 0.060 = 1.08σ. These match "1.7σ and 1.1σ" in the text and "within 1.7σ" in the abstract.

---

## Comment 28: the N = 800 held-out test

> (a) Limitations is less complete than Sec. VI. […] the embedding test as a whole (spectrum, stress and z) rejects 4 of the 20 continuum-like states, assuming the z false positive's stress is in the band. Please state that state's stress. Sec. V's "this test passes every continuum-like state" is an N = 400 result and should say so. (b) Please give M at N = 800, and say how z > 0.120 was obtained. (c) Context for the false positive […] height of about 2√N ≈ 57 […]. (d) Sample size […] A clause such as "on a small held-out sample" is enough. Only one of the eight layered states (stress 0.072) actually tests the blind spot that z is meant to close. (e) Placement. The sentence that follows ("These states are test inputs …") now reads as if it referred to the N = 800 chains […].

**Response.** All five points are made. The classification fixed in advance is unchanged, and the false positive is still reported as one. Numbers are from `sims/out/r27_n800_heldout.txt` and `sims/out/r27_calibrate.txt`.

**(a)** The z false positive (27 layers, β = 0.3) has stress **0.134**. That is **above** the flat band (≤ 0.081), not in it. The three other states above the band have stress 0.086, 0.092 and 0.110. The full test therefore rejects exactly 4 of the 20 continuum-like states, which matches the summary line of the r27 output ("continuum-like: 16/20 pass").

*Changed text, Discussion, Limitations:*

> … on a small held-out sample at N = 800 (8 layered and 20 continuum-like states) the layered flag caught every layered state but also one of the 20 continuum-like states, just above its threshold; the stress put that state (0.134) and 3 of the 19 unflagged ones above the flat band, so at this size the full embedding test (spectrum, stress and z) rejects 4 of the 20 continuum-like states; the e^{−βS} states used are test inputs, not equilibrium samples.

*Changed text, Sec. V, "Blind spot":*

> Applied to Monte Carlo samples of the e^{−βS} model at N = 400 (Sec. VI), this test passes every continuum-like state at that size (not at N = 800; Sec. VI) and fails orders with 4 and 7 layers, …

*Changed text, Sec. VI* (so that the body also states the false positive's stress):

> Three of the 19 unflagged states have a stress slightly above the flat band at N = 800 (0.086–0.110, against flat mean plus two standard deviations, 0.081), as does the flagged one (0.134), so at this size the stress alone would also reject some continuum-like states.

**(b)** M = 80 (`r27_n800_detector.py`: `N, M, DRAWS = 800, 80, 5`), as for z at N = 400. The threshold is 1.5 times the median z of 50 flat orders (median 0.080, which gives 0.120). This is the rule of Sec. V. A second, independent set of 50 flat orders was the check, and none of them was flagged.

*Changed text, Sec. VI:*

> At N = 800, with M = 80 (as for z at N = 400) and the threshold fixed in advance from flat orders (z > 0.120, 1.5 times the median z = 0.080 of 50 flat orders; none of 50 fresh flat orders and 20 de Sitter diamonds is flagged), we ran 28 chains …

**(c)** We measured the height directly (`sims/r42_flat_height.py`, 2000 random 2D orders per size):
- N = 800: mean 51.8, s.d. 2.5, range 45–62;
- N = 400: mean 35.7, s.d. 2.2, range 29–42.

2√N (57 and 40) overestimates both, because the leading finite-N correction is negative. Against the measured means:
- the 27-layer state has about half the flat height;
- the N = 400 continuum-like states (30–39 layers) were at about the flat height.

*Changed text, Sec. VI, after the false positive:*

> … but by the classes fixed in advance it is a false positive. For context only: random two-dimensional orders of 800 elements have 52 layers on average (standard deviation 2.5), so this state has about half the flat height, whereas the continuum-like states at N = 400 had 30–39 layers against a flat mean of 36.

**(d)** *Changed text, Sec. VI:*

> On this small held-out sample (8 layered and 20 continuum-like states), all 8 layered states (14–19 layers) are flagged (z = 0.38–0.57); only one of them, with stress 0.072, lies in the flat band, the blind spot that z is meant to close, and the embedding spectrum alone would have passed it.

The same clause ("on a small held-out sample …") is in Limitations; see (a).

**(e)** *Changed text, Sec. VI:*

> The N = 400 states are test inputs, not equilibrium samples: chains started from layered orders accept ≤ 0.1 % of the moves.

The abstract claim "lets the test reject layered orders on its own" is unchanged, as the referee allowed.

---

## Comment 29: Data availability and Ref. [46] at submission

> Please make the repository public, mint the Zenodo DOI from the tagged release, and switch the statement and Ref. [46] to the present tense in the file you upload. As in round 3, I would ask the editor to make a working DOI a condition of acceptance.

**Response.** The text is switched to the present tense. The repository and the DOI are the author's steps before upload (see the top of this answer). The DOI can be minted before upload. If it is not filled in by then, we accept the condition of acceptance.

**Changed text, Data availability:**

> The code that produces every number and figure in this paper, and the research notebook in which the work was carried out, are openly available at https://github.com/presindev/causet-counting, and the version used for this paper is archived at doi:[Zenodo DOI]. Figures are produced by … the N = 800 test by sims/r27_n800_detector.py, and the heights of random orders quoted with it by sims/r42_flat_height.py.

**Changed text, Ref. [47]** (Ref. [46] in v4):

> R. Bada, Two causal-set papers written with an AI research partner: methodology note (2026), released with the code at https://github.com/presindev/causet-counting.

---

## Other changes

1. **Citation for the Mecke formula (new Ref. [33]).** Sec. IV uses the Mecke formula for the unbiased use of sprinkled pairs, and v4 gave no reference for it. That is a referencing gap: the CQG criteria include appropriate referencing, and the paper's main methodological point rests on the formula. We added:
   - **Reference:** G. Last and M. Penrose, *Lectures on the Poisson Process* (Cambridge University Press, Cambridge, 2017), Ch. 4. The Mecke equation, including its multivariate form for sums over pairs, is in Sec. 4.1. The reference was verified in session 19.
   - **Where it is cited:** "The unbiased use of sprinkled pairs follows from the Mecke formula [33]: …".
   - **Renumbering:** the new entry follows Ref. [32] (Barton–Borza–Röhrig) in the list, so Refs. [33]–[46] of v4 become [34]–[47]. The methodology note is now Ref. [47].
2. **Data availability** gains the script `sims/r42_flat_height.py`, which produces the height numbers of comment 28c.
3. Comment lines in the LaTeX source record the v5 changes. They do not print.

---

## Checks before delivery

**Abstract against body (every number and claim):**

| Abstract | Body |
|---|---|
| d² = 2V_AV_B/V_C for any c, flat | Eq. (3), Sec. III |
| "unbiased for d² above two discreteness lengths" | Sec. III: "Above 2ℓ the rectangle estimator is unbiased for d² within the uncertainties"; Table I |
| "more accurate than the equal-depth construction … at all separations" | Table II |
| "between two and ten discreteness lengths … as accurate as or more accurate than … Hu, Meyer and Meyer, which is more accurate at larger separations" | Sec. III: "Between 2ℓ and 10ℓ its median error is the smallest … Above 10ℓ the Hu–Meyer–Meyer estimate is unbiased and the most accurate"; Table II |
| tanh²(Hτ/2)/[2 ln cosh(Hτ/2)] = 1 − Rτ²/16 + O(τ⁴) | Eq. (11) |
| FRW: "to leading order in the depth … one third of the way" | Eq. (12) and the sentence after it |
| "with its coefficients summed over the pairs of many independent sprinklings, reproduces the same fit on the exact continuum volumes" (new) | Sec. IV, "Pooling" (R_est = −16Σβ/Σα over 1000 sprinklings, Table III); one-region paragraph ("forming the ratio from Σβ and Σα pooled over all 400 sprinklings gives 1.96 ± 0.12 and 2.04 ± 0.07") |
| "inserted by hand (de Sitter, flat and FRW sprinklings)" | Table III inserted rows (0.9σ, 1.1σ; flat within errors); "FRW spacetime" paragraph (within 1σ) |
| "all sprinkled pairs of a position-based selection (de Sitter and flat, within 1.7σ)" | Table III windows rows: (2.076 − 1.912)/0.097 = 1.69σ; flat 0.00 ± 0.02, −0.01 ± 0.01 |
| "selecting the elements nearest … biases it low" | Table III nearest rows: low by 0.37 ± 0.11 and 0.24 ± 0.07 |
| "its window needs no coordinates" on a causally convex region | Sec. IV, "Window from the order" |
| "less precise … spread … about three times larger" (de Sitter) | Sec. IV: 2.32/0.80 = 2.9 and 1.34/0.46 = 2.9 |
| "within one region, biased low" | Sec. IV: low by 0.43 ± 0.12 and 0.15 ± 0.07 |
| "lets the test reject layered orders on its own" | Sec. VI: 9/9 (N = 400), 18/18 (N = 200), 8/8 (N = 800) layered states flagged |
| Laguerre identity in an appendix | Appendix A, Eq. (A2) |

**Old phrases searched** in the v5 source and in the text extracted from the v5 PDF. None remains:
- "no larger than": 0;
- "rarer only slowly": 0;
- "on average over independent sprinklings": 0;
- "rectangle lies inside": 0;
- "will be made openly available": 0;
- "to be released": 0;
- "within 1.1σ at both": 0.
