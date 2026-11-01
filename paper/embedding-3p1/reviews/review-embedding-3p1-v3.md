# Referee report — Physical Review D (third round)

**Manuscript:** "Spatial embedding of 3+1 causal sets: low-count spacelike pairs and a likelihood fit to interval counts" (R. Bada), version v3 (dated October 30, 2026), with the author's response `answer-embedding-3p1-v3.md` and a latexdiff against v2.

**Criteria applied:** the APS referee criteria used across the Physical Review family: scientific soundness and technical correctness; novelty and significance sufficient for this journal (as opposed to a less selective one); whether the conclusions are supported by the results; clarity of presentation; recommendation (accept / minor revision / major revision / reject).

**Scope:** the response lists no placeholders, so all of v3 is assessed. I used the diff to locate the changes, but every judgement below is made on the clean v3 PDF.

---

## Summary

v3 answers the second report:
- **Comment 7 (optimizer framing).** The author reports:
  - sign counts for the likelihood difference between the truth-started and the intrinsic fit;
  - the log-likelihood along the straight path between the two maps;
  - relaxations from points on that path;
  - a 2000-iteration L-BFGS continuation of the intrinsic fit.

  The abstract, Introduction, Sec. V, Discussion and Outlook now say the residual lies along "a nearly flat valley of the likelihood: maps of very different accuracy differ in log-likelihood by only O(1)".
- **Minor comments.** The abstract numbers were corrected (72–83 %; median error lowered "by a third", tail "more than halved"). The error-localization paragraph was recomputed on the Fig. 2 set and Fig. 2 redrawn at full width. References to earlier versions were removed. A recommended variant (exact Poisson form on near-cone pairs) is given with estimated wall times. The companion title was updated, and candidate statistics for Johnston's Table IV were computed.

## Assessment

The revision is careful, and the new framing of the optimizer result is the right one. The central new claim, that maps of very different accuracy differ by only O(1) in lnL, is well supported. Relaxed points of intermediate accuracy (86 % and 89 %) lie within O(1) of both ends, and a long continuation moves lnL by O(1) without changing C. I accept the abstract's new wording as it stands.

One sub-claim goes further than the data. Sec. V and the Outlook state that the global maximum lies near the more accurate map, and that the valley slopes toward it. Both rest on likelihood differences of the same size as the residual non-convergence that the paper itself demonstrates (new comment 15). The fix is either one more equal-convergence comparison or deleting two sentences.

Checks I made:
- **Abstract against the text and Table III.**
  - 44 = 10+10+10+8+6 universes, 44/44 wins;
  - 72–83 %;
  - median per-pair error −39/−39/−33 % ("by a third" is fair);
  - 90th percentile −60/−57/−54 % and 99th −55/−76/−79 % ("more than halves its tail" is correct).
- **Recomputed rms values.** Weighting the tenth with the fewest partners by 0.1 and the rest by 0.9: √(0.1·1.69² + 0.9·0.20²) = 0.57ℓ and √(0.1·1.24² + 0.9·0.17²) = 0.42ℓ for the fit, and 0.65 and 0.55ℓ for Johnston. These match the quoted 0.57, 0.42, 0.66 and 0.55ℓ.
- **Recommended variant.** Its numbers are consistent with Table III: 0.9884 + 0.0008 gives 76 %, and 0.9953 + 0.0006 gives 82.6 %.
- **Straight-path dip.** The explanation is right in substance, and the paper's own numbers support it. For each pair, the norm of the average of two separation vectors is at most the average of their norms (triangle inequality), so the straight-line midpoint is uniformly "too timelike". The relaxed midpoint lies 0.35ℓ rms from each end, with the ends 0.63ℓ apart. If rms distances combine as Euclidean distances in the 3n coordinates, it therefore sits only ≈0.15ℓ rms from the straight-line midpoint, yet recovers ~5×10³ in lnL. A small, mostly transverse correction, presumably on the weakly constrained elements, removing a dip of that size is what a second-order shortening effect predicts. A barrier would not behave this way. A rough estimate, with links of width s ≈ ℓ² and weak elements displaced by ~2ℓ, also gives a dip of order 10³–10⁴.
- **Wall times.** The near-cone timings in Sec. VII are clearly marked as estimates: "We did not rerun it on the timing node; … gives an estimated …". Sec. V points to Sec. VII for them.

---

## Status of second-round comments

| # | Comment (v2) | Status | Reason (checked in v3 text) |
|---|---|---|---|
| 7 | "Not by the optimizer" too strong | **Resolved in substance**; one sub-claim remains (new comment 15) | Sign counts, path scan, relaxations and continuation are all reported in Sec. V. The new wording is used consistently in the abstract, Introduction item 3, Discussion and Outlook, and no "not by the optimizer" remains. |
| 9 | "Roughly halves"; "three quarters to four fifths" | **Resolved** | Abstract and Introduction item 3 rewritten; checked above. |
| 10 | Stale v1 numbers in "Where the error remains"; Fig. 2 illegible | **Resolved** | Recomputed on the ten-universe converged set (consistent with Fig. 2 and checked above); Fig. 2 now full width and legible. |
| 11 | Version history in manuscript | **Resolved** (one remnant) | All "version 1" references and run labels are gone from the text and captions. One remnant: Data availability, "the large-n runs **of this version**". |
| 12 | Recommend a variant; time it; schedule note | **Resolved** (two clarifications, comment 17) | Recommendation in Sec. V, estimated wall times in Sec. VII, clearly labelled as estimates; Table III caption states the 400-iteration Adam schedule. |
| 13 | Companion title | **Resolved** | [18] updated. |
| 14 | (Optional) Table IV statistics; slab universes | (a) **Done**, mismatch remains; (b) **declined, acceptable** | Sec. III lists the candidates. No conclusion uses Table IV. The slab uncertainties are quoted as they are. |

First-round comments M1–M6 and m1–m8 remain resolved (m5 declined acceptably, m8 withdrawn). Nothing in v3 reopens them.

---

## New comments

15. **The directional claims rest on differences at the convergence tolerance.** Sec. V states:
    - "The global maximum of Eq. (5) therefore lies near the more accurate map";
    - "Along the valley the slope points weakly toward the more accurate map".

    The Outlook adds "an ideal global optimizer would move toward them". The support is the sign count: the truth-started fit has the higher lnL in 9/10 universes at n = 3000 (mean margin 0.91) and 10/10 at n = 6000 (2.30). But the same paragraph shows that the "converged" intrinsic fit still gains +0.5 and +2.4 under 2000 further L-BFGS iterations. That is as large as the margins. From the per-universe values in the response, several margins (0.06–0.45 at n = 3000; 0.18–1.08 at n = 6000) are smaller than this continuation gain. So the sign count compares points that are converged to different degrees, and the comparison could reverse.
    - **(a)** Either continue the truth-started fit (and the relaxed midpoints) with the same 2000-iteration schedule and recount;
    - **(b)** or delete the three directional sentences.

    The rest of the conclusion does not depend on this: a nearly flat valley in which the likelihood carries almost no information. If the directional claim is kept, also report the n = 1000 count (4 of 10 in the response, all |ΔlnL| < 0.8), which the manuscript currently omits.
16. **"With no barrier between them".** The manuscript reports the relaxation from the midpoint only. The response also has relaxations from s = 0.25 and 0.75, which land at correspondingly lower and higher accuracy. Please add these to the text; they are what makes "valley" more than a single point. Please also say "no barrier was found" rather than "no barrier", since the segments between relaxed points were not scanned.

    In the dip explanation, "because averaging two maps whose errors are partly independent shortens every distance" would be more precise as: the norm of an average of two separation vectors is at most the average of their norms. Then every pair becomes more timelike at the midpoint unless its two separation vectors are parallel. Optionally, the 0.15ℓ figure above could be quoted.
17. **Near-cone share and the recommended variant.**
    - Sec. VII says the near-cone share "falls as n^(−1/2)". The measured shares (0.64, 0.47, 0.37, 0.30, 0.27 at n = 1000–15000) fall more slowly, roughly as n^(−0.3) (0.47 → 0.27 over a factor 5 in n gives an exponent ≈ −0.34). My second-round report gave n^(−1/2) as a rough estimate; the data are the better guide. Please state the measured trend.
    - Please also say which iteration schedule produced the recommended variant's 72/76/82 %. The cost estimate in Sec. VII assumes 400 iterations. If the accuracy figures used a different schedule (e.g. continued to convergence), the estimate should use that one.
18. **Data availability.** The statement says the code and notebook "are openly available" at the GitHub URL. The response says the repository "will be made public with a persistent identifier on submission". The statement must be true when the paper is submitted, and so must Ref. [32], which points to the same repository. Either make the repository public before submission, or word the statement as a commitment. Also remove "of this version" (comment 11).

## Recommendation

**Minor revision; accept once comments 15–18 are addressed.** All substantive concerns from the earlier rounds are resolved, and the paper's conclusions are now supported by its results. Comments 15–18 are textual, apart from the optional recount in comment 15(a). I do not need to see the manuscript again if comment 15 is handled by either route.

---

## Notes for the author (outside the formal report)

What to fix first, by impact:
1. **Comment 15.** This is the only remaining claim a careful referee could pick apart. The quickest route is to delete the three directional sentences: "therefore lies near the more accurate map", "the slope points weakly toward", "an ideal global optimizer would move toward them". The flat-valley conclusion stands without them. If you want to keep them, run the truth-started fits with the same 2000-iteration continuation and recount.
2. **Comment 18.** Make sure the GitHub repository is actually public, or reword, before submission. An editor or referee who clicks a dead link will notice.
3. **Comments 16–17.** Add the s = 0.25 and 0.75 relaxations, "no barrier was found", the measured near-cone trend, and the schedule of the recommended variant.

Small things outside the report:
- The answer, under comment 14(b), quotes Johnston's time at n = 15000 as 7511 s, but the manuscript (and v2) gives 7691 s. The manuscript is self-consistent; only the answer has the slip.
- The extrapolated crossover moving to n ≈ 10000 is in the answer but not the paper. Leaving it out is reasonable, since it is built on estimates.

Assessment: this is now a solid PRD paper. Its contribution is an oracle diagnosis of the benchmark's error, an intrinsic start that makes Casasola's likelihood work at scale, and a clear account of what limits it. The remaining risk is a referee who considers it incremental over Johnston plus Casasola. The candid framing helps against that.

Estimated chance of eventual PRD acceptance: about **70–80 %** as submitted now, about **75–85 %** with comments 15–18 fixed (v2: 65–75 %). This is a judgment call, not data.
