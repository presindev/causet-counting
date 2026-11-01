# Answer to the referee: embedding-3p1, round 3 (PRD)

**Manuscript:** "Spatial embedding of 3+1 causal sets: low-count spacelike pairs and a likelihood fit to interval counts" (R. Bada).
**This answer** responds to `review-embedding-3p1-v3.md` and comes with `embedding-3p1-v4.pdf` and `embedding-3p1-v4-diff.pdf` (latexdiff against v3).

**Placeholders remaining in the manuscript: none.** The Data availability statement is now a commitment, because the repository is still private: the code "will be made openly available … when this paper is submitted" (comment 18). It is not a placeholder, but it becomes true only when the author makes the repository public.

We thank the referee for the third report. All four comments are handled as follows:
- **Comment 15:** route (b). The three directional sentences are deleted. The sign counts stay as a non-result, with n = 1000 added.
- **Comment 16:** the s = 0.25 and 0.75 relaxations are rerun to convergence and added to Sec. V.
- **Comments 17 and 18:** text changes.

New runs: `sims/r39_3p1_round2.py relaxlong_s` (relaxations from s = 0.25, 0.5, 0.75 to convergence, with the distance from the start). Summary: `sims/out/r39_relax_s_round3.txt`.

---

## Comment 15: the directional claims rest on differences at the convergence tolerance

> Sec. V states: "Its log-likelihood is higher than that of the converged intrinsic fit in 9 of 10 universes at n = 3000 and in 10 of 10 at n = 6000 […] but only by 0.9 on average […] and by 2.3 […]. The global maximum of Eq. (5) therefore lies near the more accurate map." The Outlook adds: "an ideal global optimizer would move toward them". […] the same paragraph shows that the "converged" intrinsic fit still gains +0.5 and +2.4 under 2000 further L-BFGS iterations, as large as the margins. […] So the sign count compares points that are converged to different degrees, and the comparison could reverse. (a) Either continue the truth-started fit (and the relaxed midpoints) with the same 2000-iteration schedule and recount; (b) or delete the three directional sentences. […] If the directional claim is kept, also report the n = 1000 count (4 of 10 in the response, all |ΔlnL| < 0.8), which the manuscript currently omits.

**Response.** We agree, and took route (b). The margins are the size of the continuation gain, so they do not show which map the likelihood prefers.
- **Deleted:**
  - "The global maximum of Eq. (5) therefore lies near the more accurate map";
  - "Along the valley the slope points weakly toward the more accurate map, but a practical optimizer does not follow it";
  - in the Outlook, "the more accurate maps are favoured by only O(1) … an ideal global optimizer would move toward them".
- **Kept:** the sign counts, now stated as a non-result, at all three n including n = 1000. We rechecked the n = 1000 count from the saved per-universe lnL: 4 of 10, differences +0.03, −0.11, −0.05, −0.66, −0.08, +0.13, +0.73, −0.09, +0.56, −0.03.

**Changed text, Sec. V ("Is the residual set by the optimizer or by the likelihood?"), second paragraph:**

> Its log-likelihood differs from that of the converged intrinsic fit by only O(1): it is higher in 4 of 10 universes at n = 1000 (all differences below 0.8 in magnitude), in 9 of 10 at n = 3000 (by 0.9 on average, at most 5.4) and in 10 of 10 at n = 6000 (2.3, at most 6.5). These differences are no larger than what further iterations add to the intrinsic fit (below), so they do not tell which of the two maps the likelihood prefers.

> Continuing L-BFGS from the converged intrinsic fit for 2000 iterations without a stopping tolerance raises the log-likelihood by 0.5 at n = 3000 and by 2.4 at n = 6000, as much as separates the two maps, and leaves C unchanged (0.98855 → 0.98853 and 0.99544 → 0.99543).

**Changed text, Outlook:**

> The remaining error lies along a nearly flat valley of the likelihood, in which maps of very different accuracy differ in log-likelihood by only O(1), and longer optimization did not move the fit along it.

**Abstract, Introduction (item 3), Discussion.** These made no directional claim and are unchanged:
- Abstract: "maps of very different accuracy differ in log-likelihood by only O(1), so the likelihood carries almost no information that would let an optimizer prefer the more accurate one";
- Introduction: "gives an optimizer almost no signal toward more accurate maps";
- Discussion: "a nearly flat valley of the likelihood, in which maps of very different accuracy differ in log-likelihood by only O(1)".

We searched v4 for "global maximum", "toward", "favoured" and "slope". The only hits left are the abstract and Introduction sentences above, which state that there is no signal.

---

## Comment 16: "with no barrier between them"

> The manuscript reports the relaxation from the midpoint only. The response also has relaxations from s = 0.25 and 0.75 […]. Please add these to the text […]. Please also say "no barrier was found" rather than "no barrier", since the segments between relaxed points were not scanned. In the dip explanation, […] the norm of an average of two separation vectors is at most the average of their norms. […] Optionally, the 0.15ℓ figure above could be quoted.

**Response.** All three points are done.
- **Reruns.** The s = 0.25 and 0.75 relaxations in the v3 answer were capped at 300 L-BFGS iterations, and 4–8 of 10 hit the cap. We reran them to convergence with the same settings as the v3 midpoint run (L-BFGS up to 3000 iterations, r35's stopping test), and reran the midpoint as a check. No run reached the cap (26–1001 iterations). The midpoint values reproduce v3 universe by universe.
- **Distance to the straight midpoint.** We also recorded each relaxed map's rms distance from its starting point. The relaxed midpoint lies 0.15ℓ rms (0.11–0.21) from the straight midpoint at n = 3000, and 0.11ℓ (0.07–0.16) at n = 6000. It recovers 5.0×10³ and 7.3×10³ in lnL. This is the referee's estimate, now measured.

| n | relaxed from | removed fraction | lnL − intrinsic fit | lnL − truth-started fit | iterations |
|---|---|---|---|---|---|
| 3000 | intrinsic end | 74.5 % | 0 | — | — |
| | s = 0.25 | 78.4 % | +0.06 … +1.61 | −3.77 … +0.22 | 229–689 |
| | s = 0.5 | 86.2 % | −0.90 … +5.23 | −1.49 … +0.61 | 36–854 |
| | s = 0.75 | 91.6 % | +0.02 … +5.30 | −0.07 … +0.55 | 26–533 |
| | truth end | 92.3 % | — | 0 | — |
| 6000 | intrinsic end | 80.7 % | 0 | — | — |
| | s = 0.25 | 83.4 % | +0.31 … +6.01 | −1.06 … +0.65 | 109–1001 |
| | s = 0.5 | 88.9 % | +0.34 … +6.44 | −0.66 … +0.16 | 88–836 |
| | s = 0.75 | 92.6 % | +0.25 … +6.73 | −0.30 … +0.21 | 37–626 |
| | truth end | 93.1 % | — | 0 | — |

In all 60 relaxations, C lies between the two ends, and it increases with s in every universe.

**Changed text, Sec. V:**

> On the straight line between them the log-likelihood drops by 2.7×10³–1.3×10⁴ at the midpoint. This dip is expected without a barrier: for each pair, the norm of the average of two separation vectors is at most the average of their norms (triangle inequality), so at the straight midpoint every related pair is more timelike than the average of the two maps unless its two separation vectors are parallel. Started from the points at a quarter, half and three quarters of the way and run to convergence, L-BFGS reaches in every universe a map whose accuracy lies between those of the two ends and increases along the path: it removes 78 %, 86 % and 92 % of the residual at n = 3000 (83 %, 89 % and 93 % at n = 6000), against 75 % and 92 % (81 % and 93 %) at the ends. Each of these maps has a log-likelihood within O(1) of both ends (−3.8 to +0.6 from the truth-started fit at n = 3000, −1.1 to +0.7 at n = 6000). The relaxed midpoint lies only 0.15ℓ rms from the straight midpoint at n = 3000 (0.11ℓ at n = 6000), yet recovers 5.0×10³ (7.3×10³) in log-likelihood, as a second-order shortening effect would and a barrier would not. The two maps are thus joined by a curved valley along which the log-likelihood changes by O(1) while the removed fraction goes from 75 % to 92 % (81 % to 93 % at n = 6000); no barrier was found along it, although the segments between the relaxed points were not scanned.

We wrote "than the average of the two maps" rather than "than either map": the bound compares the midpoint with the mean of the two separations, not with each of them.

---

## Comment 17: near-cone share and the recommended variant

> Sec. VII says the near-cone share "falls as n^(−1/2)". The measured shares (0.64, 0.47, 0.37, 0.30, 0.27 at n = 1000–15000) fall more slowly, roughly as n^(−0.3) […]. Please also say which iteration schedule produced the recommended variant's 72/76/82 %. The cost estimate in Sec. VII assumes 400 iterations. If the accuracy figures used a different schedule […], the estimate should use that one.

**Response.**
- **Near-cone trend.** Replaced with the measured trend. A log-log fit over n = 1000–15000 gives exponent −0.32, and −0.35 over n = 3000–15000.
- **Schedule.** The recommended variant (`exact_near` in `sims/r35_referee1_3p1.py`, line 147) was run with the same 400-iteration Adam schedule as Table III, with no L-BFGS continuation. The cost estimate in Sec. VII scales that same 400-iteration time, so it stands. Both places now say so.

**Changed text, Sec. VII:**

> The variant we recommend for use (Sec. V), the exact Poisson form on near-cone pairs, is cheaper per iteration, because the share of near-cone pairs falls with n, roughly as n^(−0.3) (0.64, 0.47, 0.37, 0.30, 0.27 at n = 1000, 3000, 6000, 10000, 15000), while the exact form costs about 1.7 times the Gaussian form per pair. We did not rerun it on the timing node; scaling the measured time of the 400 iterations of the timing runs by the ratio of the per-iteration costs measured on a laptop, and keeping the other steps, gives an estimated 250, 860, 1900 and 3900 s […]

**Changed text, Sec. V ("Which pairs are needed?"):**

> For use we therefore recommend the exact Poisson form on the near-cone pairs. With the same 400-iteration Adam schedule as Table III, on the large-n set it removes 72 %, 76 % and 82 % of Johnston's residual at n = 1000, 3000, 6000; […]

---

## Comment 18: data availability

> The statement says the code and notebook "are openly available" at the GitHub URL. The response says the repository "will be made public with a persistent identifier on submission". The statement must be true when the paper is submitted, and so must Ref. [32] […]. Either make the repository public before submission, or word the statement as a commitment. Also remove "of this version" (comment 11).

**Response.** The repository is private today, so both places are now worded as a commitment, and "of this version" is removed. Making the repository public is the author's step at submission (see the note at the top).

**Changed text, Data availability:**

> The code that produces every number in this paper, and the research notebook in which the work was carried out, will be made openly available at https://github.com/presindev/causet-counting when this paper is submitted. […] the large-n runs (ten universes per size up to 6000, ablations, optimizer and joint-fit checks) in sims/r35_referee1_3p1.py […]

**Changed text, Ref. [32] (methodology note):**

> R. Bada, Two causal-set papers written with an AI research partner: methodology note (2026), to be released with the code at https://github.com/presindev/causet-counting.

---

## Notes outside the formal report

- **7511 s against 7691 s.** Both numbers are correct and measure different things (`sims/out/r28_timing.txt`, n = 15000):
  - 7511 s is Johnston's min-plus step alone;
  - 7691 s is his whole pipeline: matrix product 17 s + min-plus 7511 s + eigendecomposition 163 s.

  The manuscript quotes the pipeline, and the v3 answer (comment 14b) quoted the cubic step without saying so. The manuscript is unchanged.
- **Crossover near n ≈ 10000** for the near-cone variant: left out of the paper, as the referee suggests, because it rests on estimated times.

---

## Status of earlier comments

| # | Status after round 3 (referee) | v4 |
|---|---|---|
| M1–M6, m1–m8 | resolved (m5 declined acceptably, m8 withdrawn) | unchanged |
| 7 | resolved in substance; sub-claim → 15 | 15 handled by deletion |
| 9, 10, 13 | resolved | unchanged |
| 11 | resolved, one remnant | remnant "of this version" removed (18) |
| 12 | resolved, two clarifications → 17 | both added |
| 14 | (a) done; (b) declined, acceptable | unchanged |

## Other changes

- Sec. V, "Is the residual set by the optimizer…": the second paragraph is rewritten as quoted under comments 15 and 16. Its first paragraph (Adam vs L-BFGS, three starts) is unchanged.
- Header comment of the .tex records the v4 changes. This is a LaTeX comment and does not appear in the PDF.
- No other changes. The abstract and every table are unchanged. Abstract numbers were checked once more against Table III and `sims/out/r35_analyse_all.txt`:
  - 44 universes = 10 + 10 + 10 + 8 + 6;
  - 72–83 %;
  - median per-pair error −39/−39/−33 %;
  - 90th percentile −60/−57/−54 %;
  - 99th percentile −55/−76/−79 %.

## Placeholders

None in the manuscript. Before submission, the author must make the GitHub repository public, which the Data availability statement now commits to.
