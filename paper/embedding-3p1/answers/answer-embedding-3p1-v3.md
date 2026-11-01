# Answer to the referee: embedding-3p1, round 2 (PRD)

**Manuscript:** "Spatial embedding of 3+1 causal sets: low-count spacelike pairs and a likelihood fit to interval counts" (R. Bada).
**This answer** responds to `review-embedding-3p1-v2.md` and comes with `embedding-3p1-v3.pdf` and `embedding-3p1-v3-diff.pdf` (latexdiff against v2).

We thank the referee for the second report. Comment 7 was right, and the new computations sharpen the picture:

- The truth-started fit has the higher log-likelihood in 9 of 10 universes at n = 3000 and in 10 of 10 at n = 6000. The global maximum of Eq. (5) therefore lies on the side of the more accurate map.
- The two maps are joined by a curved valley, not separated by a barrier. The straight line between them (after alignment) crosses a deep dip. Relaxed to convergence from its midpoint, the optimizer finds a map of intermediate accuracy with a log-likelihood within O(1) of both ends.
- Continuing the optimizer from the converged intrinsic fit does not move it along the valley: 2000 further L-BFGS iterations raise lnL by +0.5 (n = 3000) and +2.4 (n = 6000), as much as separates the two maps, and leave the accuracy unchanged.

We adopted the referee's wording: "maps of very different accuracy differ in log-likelihood by only O(1), so the likelihood carries almost no information that would let an optimizer prefer the more accurate one". It is used in the abstract, Sec. V, the Discussion and the Outlook, and every "not by the optimizer" statement is removed.

All new runs are in `sims/r39_3p1_round2.py`, which reuses the r35 outputs and rebuilds each universe from its seed. Summaries are in `sims/out/r39_*.txt` (by `sims/r39_summary.py`).

---

## New major comment

### Comment 7: "not by the optimizer" is stronger than the evidence

> I ask the author to: (a) report in how many of the ten universes the truth-started fit has the higher log-likelihood; (b) evaluate lnL along the straight path between the two converged maps, after aligning them by the best rotation about the time axis, under which Eq. (5) is invariant. This tells whether the two maps are joined by a flat valley or separated by a barrier; (c) rephrase the abstract, Sec. V, Discussion and Outlook accordingly.

**Response.**

**(a) Sign count.** The truth-started fit, converged with L-BFGS, has the higher lnL in **9 of 10 universes at n = 3000** and **10 of 10 at n = 6000**. Its lnL also exceeds the best of the three converged intrinsic-side starts (intrinsic, Johnston's map, displaced intrinsic) in the same universes.

| n | universes with lnL(truth start) > lnL(intrinsic) | ΔlnL per universe | terms |
|---|---|---|---|
| 3000 | 9/10 | +5.37, +1.11, +0.06, −0.09, +0.61, +0.27, +0.40, +0.45, +0.30, +0.59 (mean 0.91) | 4.7×10⁵ |
| 6000 | 10/10 | +6.52, +2.88, +0.18, +1.00, +2.25, +5.36, +0.86, +1.08, +2.38, +0.51 (mean 2.30) | 1.9×10⁶ |

At n = 1000 the count is 4 of 10, and all differences are below 0.8 in magnitude. We recomputed each lnL from the saved maps on universes rebuilt from their seeds, and the values agree with those recorded in r35 to 10⁻³.

**(b) Path between the two maps.** We aligned the truth-started map to the converged intrinsic map by the best orthogonal 3×3 matrix (rotations and reflections about the time axis, no translation since the tips are pinned at x = 0). After alignment the two maps differ by 0.63ℓ rms at n = 3000 and 0.48ℓ at n = 6000.

- **Straight path.** Along x(s) = (1 − s)X_fit + sX_truth, lnL has a deep dip: at the midpoint it is lower by about 5×10³ at n = 3000 (2.7×10³ to 9.6×10³) and about 7×10³ (3.6×10³ to 1.3×10⁴) at n = 6000. Taken at face value this is a barrier. But averaging two maps whose errors are partly independent shortens all distances, so the straight line leaves the valley.
- **Valley test.** To tell a barrier from a curved valley, we started L-BFGS at the midpoint and ran it to convergence (r35's stopping test; 36 to 854 iterations at n = 3000, 88 to 836 at n = 6000).
  - In every universe the relaxed map has an lnL within O(1) of both ends: −0.9 to +5.2 relative to the intrinsic fit and −1.5 to +0.6 relative to the truth-started fit at n = 3000; +0.3 to +6.4 relative to the intrinsic fit and −0.7 to +0.2 relative to the truth-started fit at n = 6000.
  - Its accuracy is intermediate in every universe: it removes 86 % of Johnston's residual at n = 3000 (intrinsic fit 75 %, truth start 92 %) and 89 (intrinsic fit 81 %, truth start 93 %) % at n = 6000.
  - It is equidistant from both ends: 0.35ℓ rms from each at n = 3000 and 0.27ℓ and 0.26ℓ at n = 6000.
  - Relaxations from s = 0.25 and 0.75 (300 iterations) land at correspondingly lower and higher accuracy, also within O(1) in lnL.
- **Conclusion.** The two maps are joined by a curved valley along which lnL changes by O(1) while the removed fraction goes from 75 % to 92 %. There is no barrier, and there are no separate maxima.
- **Continued optimization.** Along the valley the slope points, weakly, toward the more accurate map, so an ideal optimizer would move there. A practical one does not: continuing L-BFGS from the converged intrinsic fit for 2000 iterations without a stopping tolerance raises lnL by +0.53 on average at n = 3000 and +2.39 at n = 6000 (as much as separates the two maps) at n = 6000. The correlation does not increase (0.98855 → 0.98853 at n = 3000, lower in 8 of 10; 0.99544 → 0.99543 at n = 6000, lower in 5 of 10 at n = 6000).

This is the referee's reading. The optimizer is not irrelevant, since the global maximum lies near the better map, but the likelihood gives an O(1) signal out of 10⁵–10⁶ terms, which no practical optimizer follows.

**(c) Rephrasing.** The new text, in each place:
- **Abstract:** "The remaining error lies along a nearly flat valley of the likelihood: maps of very different accuracy differ in log-likelihood by only O(1), so the likelihood carries almost no information that would let an optimizer prefer the more accurate one."
- **Introduction, item 3:** "… that the remaining error lies along a nearly flat valley of the likelihood, which gives an optimizer almost no signal toward more accurate maps."
- **Sec. V:** the paragraph "Is the residual set by the optimizer?" is rewritten as "Is the residual set by the optimizer or by the likelihood?", with (a), (b) and the continued optimization.
- **Discussion:** "… the remaining error lies along a nearly flat valley of the likelihood, in which maps of very different accuracy differ in log-likelihood by only O(1)."
- **Outlook:** "an ideal global optimizer would move toward them, but the signal is too weak for a practical one to follow, and longer optimization did not. In practice the error will therefore be reduced by additional information rather than by more optimization of Eq. (5)."

**Change:** abstract; Introduction item 3; Sec. V, optimizer paragraph; Discussion, "What is new"; Outlook.

---

## New minor comments

### Comment 9: "roughly halves" and "three quarters to four fifths"

> With ten universes […] the median falls 0.33 → 0.20, 0.23 → 0.14 and 0.18 → 0.12ℓ, a reduction of 33–40 %, not a half. The 90th and 99th percentiles do fall by more than half. […] "three quarters to four fifths" is slightly generous for 72–83 %.

**Response.** Agreed on both. The abstract now reads "removes 72–83 % of his residual, lowers the median error of individual spatial distances by a third and more than halves its tail". The same range replaces "three quarters to four fifths" in Introduction item 3. We checked every number in the abstract against Table III and the output files (see "Other changes").

**Change:** abstract; Introduction item 3.

### Comment 10: "Where the error remains" quoted v1 numbers

> Please recompute these numbers on the set shown in Fig. 2. Also, at the printed size the axis labels and legend of Fig. 2 are illegible.

**Response.** Recomputed on the Fig. 2 set: ten universes each at n = 3000 and 6000, converged fit, same per-element definition (best orthogonal map with translation). The old v1 numbers are removed.

| | n = 3000: Johnston | n = 3000: fit | n = 6000: Johnston | n = 6000: fit |
|---|---|---|---|---|
| rms position error, all elements | 0.66 | 0.57 | 0.55 | 0.42 |
| tenth with fewest related partners | 1.83 | 1.69 (1.43–2.14) | 1.57 | 1.24 (0.96–1.51) |
| other nine tenths | 0.32 | 0.20 (0.18–0.25) | 0.24 | 0.17 (0.15–0.19) |
| median | 0.27 | 0.18 | 0.21 | 0.15 |

(units of ℓ; ranges over the ten universes)

The rms improves less than the median, because the weakly constrained tenth dominates it. The text now says this with these numbers. Fig. 2 is now a full-width figure, with fonts at 9–10 pt at print size and larger markers.

**Change:** Sec. V, "Where the error remains"; Fig. 2 (redrawn, full width).

### Comment 11: version history and run labels in the manuscript

> A reader of the published paper has no access to an unpublished v1, so these belong in the response letter. If v1 is public (e.g. on arXiv), one footnote is enough. In either case, replace internal run labels in captions with the set names of Table I.

**Response.** v1 is not public, so every reference to it is removed and no footnote is added:
- Table I caption ("contains the universes of v1") is removed;
- Table III caption: run labels and versions are replaced by the schedule note of comment 12;
- Fig. 1 caption: "a subset of 1, 2, 4, 8, 6 of these universes";
- Sec. V: "Version 1 of this paper attributed …" and "which version 1 of this paper listed as a contribution" are removed.

The Data availability statement still names the scripts, which is where run labels belong.

**Change:** Table I and III captions; Fig. 1 caption; Sec. V.

### Comment 12: which variant to recommend

> Please say explicitly which variant a user should run; give its wall time in Sec. VII […]; state in the Table III caption that all rows use the fixed 400-iteration Adam schedule.

**Response.**

- **Recommendation.** We recommend Casasola's exact Poisson form on the near-cone pairs (τ̂² < 6ℓ²), started from the intrinsic map. On the large-n set it is the best of the variants we ran. It removes 72 %, 76 % and 82 % of Johnston's residual at n = 1000, 3000 and 6000. Paired against the paper's all-pairs Gaussian fit, ΔC is +0.0008 at n = 3000 and +0.0006 at n = 6000, positive in 10 of 10 universes at both sizes (+0.0003, 7 of 10, at n = 1000). The Gaussian form on the same pairs gains less: +0.0002 and +0.0002, 8 and 10 of 10. Table III keeps the pre-specified all-pairs Gaussian form, and Sec. V says so.
- **Cost, measured.** The near-cone share of related pairs on one universe per size is 0.47, 0.37, 0.30 and 0.27 at n = 3000, 6000, 10000 and 15000 (seed 1001), consistent with n^(−1/2). On the laptop, one Gaussian evaluation on the near-cone pairs costs 0.44, 0.37, 0.29 and 0.25 of an all-pairs evaluation. The exact form costs about 1.7 times the Gaussian per pair (Adam timings of r35: 1.76 at n = 3000, 1.69 at n = 6000).
- **Wall times, estimated.** We have not rerun the variant on the exclusive timing node. Sec. VII gives an estimate: the measured likelihood-iteration time of the timing runs, scaled by these ratios, with the other steps kept. This gives about 250, 860, 1900 and 3900 s at n = 3000, 6000, 10000 and 15000, against 44, 525, 2002 and 7691 s for Johnston's pipeline. So the variant is still slower up to n = 6000, comparable at 10000 and about twice as fast at 15000. The extrapolated crossover moves from n ≈ 16000 to about 10000. The text marks these as estimates.
- **Schedule.** The Table III caption now states that every row uses the fixed 400-iteration Adam schedule, which is not fully converged, and that convergence changes C by at most 2×10⁻⁴.

**Change:** Sec. V, end of "Which pairs are needed?"; Sec. VII, new paragraph; Table III caption.

### Comment 13: companion reference

> Companion reference [18] still carries the v1 title of the 1+1 paper.

**Response.** Updated to "Spatial distance and curvature from an exact counting identity in two-dimensional causal sets".

**Change:** reference list.

### Comment 14 (optional): Johnston's Table IV; slab universes

> (a) For Johnston's Table IV, computing two or three candidate statistics would cost little and might settle the question […] (b) The slab comparison in Sec. VI still rests on 3–4 universes per size […].

**Response.**

(a) Done; it did not settle the question. His Table IV is defined as the correlation of "the Minkowski norm distances (P_x − P_y)² and (p(v_x) − p(v_y))² for all pairs […] including distances for spacelike separated points" (his Sec. VII, item iv). On the ten n = 1000 universes of the large-n set, with his map from our implementation, we computed eight candidate statistics; his value is 0.977:

| statistic | ours |
|---|---|
| squared intervals, all pairs (his stated definition) | 0.895 |
| squared intervals, related pairs only | 0.969 |
| signed square roots of the intervals, all pairs | 0.932 |
| rank (Spearman) correlation of squared intervals | 0.916 |
| proper times of related pairs | 0.905 |
| 4D Euclidean distances / squared | 0.880 / 0.855 |
| squared intervals, spacelike pairs only | 0.856 |

The closest is the related-pair statistic (0.969), still below his value and not his stated definition. Sec. III now lists the candidates and says that no conclusion depends on Table IV. As decided in round 2, we have not contacted Johnston.

(b) Not done in this round. The slab comparison at equal density needs Johnston's pipeline at n = 12000, whose cubic step takes about an hour per universe on an exclusive cluster node (7511 s at n = 15000). We could not run it on the cluster in this round. The slab numbers and their spread (±6–9 percentage points on four universes) are reported as they are. The "about 20 percentage points" in Sec. VI is quoted together with those uncertainties. Its explanation, the boundary oracle that brings the slab level with the diamond on the same universes, is a paired comparison and depends less on the number of universes than the size of the gap does.

**Change:** Sec. III (Table IV candidates).

---

## First-round comments (status)

The referee marked all first-round comments resolved, with m5 declined acceptably and m8 withdrawn. Changes in this round that touch them:

| # | Status after v3 |
|---|---|
| M1 Significance | Resolved in v2. Unchanged. |
| M2 Statistics | Resolved in v2. Unchanged. |
| M3 Casasola ablation | Resolved in v2. Now also gives the recommended variant (comment 12). |
| M4 Optimizer | Resolved in substance in v2. The framing is now fixed as asked (comment 7). |
| M5 Time coordinate | Resolved in v2. Unchanged. |
| M6 References | Resolved in v2. Unchanged. |
| m1–m3, m6, m7 | Resolved in v2. Unchanged. |
| m4 Error-location figure | Numbers recomputed and figure enlarged (comment 10). |
| m5 Johnston Table IV | Candidate statistics computed (comment 14a). The mismatch remains. |
| m8 Hu–Meyer–Meyer citation | Withdrawn by the referee. No reply needed. |

---

## Other changes

- **Abstract check against tables and files.**
  - 44 sprinklings: Table I/III, 10 + 10 + 10 + 8 + 6.
  - "in every universe": 44/44 wins, `sims/out/r35_analyse*.txt` and the r24 log.
  - 72–83 %: Table III.
  - Median per-pair errors 0.33/0.23/0.18 → 0.20/0.14/0.12ℓ (−39/−39/−33 %), 90th percentiles −60/−57/−54 % and 99th −54/−77/−80 %: Sec. V and `sims/out/r35_analyse_all.txt` (rerun this round). Correcting one rounding: the fit's 99th percentile at n = 3000 is 0.65ℓ, printed as 0.6 in v2 and now as 0.7.
  - "O(1)": (a) and (b) above, `sims/out/r39_summary_*.txt`.
- Data availability lists `sims/r39_3p1_round2.py` and `sims/r39_summary.py`.
- latexdiff PDF against v2 included this round.

## Results still marked as placeholders in v3

None. As in v2, the manuscript has no placeholders. The Data availability statement points to the repository, which will be made public with a persistent identifier on submission.
