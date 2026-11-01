# Referee report — Physical Review D (fourth round)

**Manuscript:** "Spatial embedding of 3+1 causal sets: low-count spacelike pairs and a likelihood fit to interval counts" (R. Bada), version v4 (dated October 31, 2026), with the author's response `answer-embedding-3p1-v4.md` and a latexdiff against v3.

**Criteria applied:** the APS referee criteria used across the Physical Review family: scientific soundness and technical correctness; novelty and significance sufficient for this journal (as opposed to a less selective one); whether the conclusions are supported by the results; clarity of presentation; recommendation (accept / minor revision / major revision / reject).

**Scope:** the response lists no placeholders, so all of v4 is assessed. The third report said I would not need to see the paper again if comments 15–18 were handled as described. This round checks whether they were. For each comment I read the clean v4 text, not only the response. I used the diff only to locate changes, and I also searched the whole manuscript for leftover wording.

---

## Summary

v4 changes only Sec. V (second paragraph of "Is the residual set by the optimizer…" and "Which pairs are needed?"), Sec. VII, the Outlook, Data availability and Ref. [32]. The abstract and all tables are unchanged.
- **Comment 15.** The three directional sentences are deleted. The sign counts remain, now including n = 1000, and are presented as not deciding which map the likelihood prefers.
- **Comment 16.** The relaxations from s = 0.25 and 0.75 were rerun to convergence (none hit the cap; 26–1001 iterations) and added to Sec. V. The dip explanation is reworded. "No barrier was found" is stated with its limitation.
- **Comment 17.** The near-cone trend is now stated as measured (n^−0.3), and the recommended variant's schedule (400 Adam iterations) is given.
- **Comment 18.** Data availability and Ref. [32] are now worded as commitments, and "of this version" is removed.

## Assessment

All four comments are handled as I asked. The paper's conclusions now match its evidence: the residual lies along a nearly flat valley of the likelihood, and the paper no longer says which way the valley slopes. I found no new technical problems. The three remaining points (comments 19–21) are wording, and none of them affects a result.

Checks I made on the new material:
- **Directional claims (comment 15).** I searched the full v4 text for "global maximum", "toward", "favour/favor", "slope", "prefer", "ideal", "lies near" and "points". The only hits are:
  - the abstract's "almost no information that would let an optimizer prefer the more accurate one";
  - Introduction item 3, "almost no signal toward more accurate maps".

  Both state the absence of a signal, which is what the evidence supports. The Discussion ("What is new") and the Outlook use only the flat-valley wording. No directional claim remains anywhere.
- **n = 1000 count.** The per-universe differences in the response (+0.03, −0.11, −0.05, −0.66, −0.08, +0.13, +0.73, −0.09, +0.56, −0.03) give 4 positive out of 10, all below 0.8 in magnitude. This matches the text.
- **New relaxation numbers (comment 16), against the response's table:**
  - Removed fractions 78.4/86.2/91.6 % (n = 3000) and 83.4/88.9/92.6 % (n = 6000) round to the quoted 78/86/92 % and 83/89/93 %.
  - The ends, 74.5/92.3 % and 80.7/93.1 %, round to 75/92 % and 81/93 %.
  - The ranges relative to the truth-started fit (−3.77 … +0.61 at n = 3000; −1.06 … +0.65 at n = 6000, taken over the three values of s) round to the quoted "−3.8 to +0.6" and "−1.1 to +0.7".
  - 60 relaxations = 3 values of s × 10 universes × 2 sizes, consistent with "in every universe … increases along the path".
  - The midpoint values reproduce v3 (86 %, 89 %).
  - The measured 0.15ℓ (0.11ℓ at n = 6000) distance of the relaxed midpoint from the straight midpoint agrees with the estimate I made in round 3.
- **Dip explanation.** The new sentence is correct, including the author's refinement "than the average of the two maps". With the time coordinates shared, |(Δx₁+Δx₂)/2| ≤ (|Δx₁|+|Δx₂|)/2, so τ² at the straight midpoint is at least the mean of the two τ² values. Equality requires parallel (and, for τ², equal) separation vectors. "No barrier was found along it, although the segments between the relaxed points were not scanned" is the right strength.
- **Near-cone exponent (comment 17).** A log-log fit of 0.64, 0.47, 0.37, 0.30, 0.27 against n = 1000–15000 gives −0.32, as stated. The schedule is now given in both Sec. V and Sec. VII, and because the accuracy figures and the cost estimate use the same 400-iteration schedule, the estimate stands.
- **7511 s vs 7691 s.** 17 + 7511 + 163 = 7691 s. The response's explanation (min-plus step alone vs whole pipeline) settles it, and the manuscript was already consistent.
- **Abstract numbers.** Unchanged and rechecked against the body:
  - 44 = 10+10+10+8+6 universes, with a win in every universe;
  - 72–83 % (Table III);
  - median per-pair error −39/−39/−33 % ("by a third");
  - 90th percentile −60/−57/−54 % and 99th −55/−76/−79 % ("more than halves its tail");
  - "fewer than ten elements" (Sec. IV, k < 10);
  - "O(1)" (Sec. V).

  One qualitative phrase is not supported by the body (comment 20).

---

## Status of third-round comments

| # | Comment (v3) | Status | Reason (checked in v4 text) |
|---|---|---|---|
| 15 | Directional claims rest on differences at the convergence tolerance | **Resolved** (route b); one sentence slightly mis-stated (comment 19) | All three sentences are gone from Sec. V and the Outlook, and no directional wording remains anywhere (searched). The sign counts are kept as a non-result with n = 1000 added (4/10, \|ΔlnL\| < 0.8). The conclusion drawn, "they do not tell which of the two maps the likelihood prefers", is the right strength. The sentence leading to it says the differences are "no larger than" the continuation gain, which is not quite true (comment 19). |
| 16 | "No barrier": add the s = 0.25/0.75 relaxations; "no barrier was found" | **Resolved** | Rerun to convergence (no run hit the cap), not taken from the capped round-3 runs. The numbers in the text match the response's table, and accuracy increases with s in every universe. "No barrier was found … segments … not scanned" is in the text. The dip explanation is the triangle-inequality statement, correctly restricted to "the average of the two maps", and the measured 0.15ℓ/0.11ℓ distance is quoted. |
| 17 | Near-cone share ~n^−0.3; schedule of the recommended variant | **Resolved** | Sec. VII: "roughly as n^(−0.3)" with the five shares (my fit gives −0.32). Sec. V: "With the same 400-iteration Adam schedule as Table III". The cost estimate uses the same schedule. |
| 18 | Data availability "openly available" vs private repository; "of this version" | **Resolved as worded**; one edit is due at submission (comment 21) | The statement is now true as written ("will be made openly available … when this paper is submitted"). "Of this version" is removed, and Ref. [32] is reworded the same way. |

Earlier comments (M1–M7, m1–m14) remain resolved (m5 declined acceptably, m8 withdrawn). Nothing in v4 reopens them.

---

## New comments (all minor)

19. **Sec. V, sign counts: "These differences are no larger than what further iterations add to the intrinsic fit."** Strictly this is not so:
    - at n = 3000 the mean margin (0.9) exceeds the continuation gain (0.5);
    - the largest margins (5.4 and 6.5) exceed the gain at both sizes.

    The conclusion still follows, but for a slightly different reason: the margins are of the same order as the gain, and the truth-started fit was not continued in the same way, so the two ends are not compared at equal convergence. Suggested wording: "These differences are of the same order as what further iterations add to the intrinsic fit (below), and the two fits were not continued equally, so they do not tell which of the two maps the likelihood prefers."

    In the relaxation paragraph, "within O(1) of both ends" is supported in the text only against the truth-started end. Please also quote the range relative to the intrinsic fit (−0.9 to +5.3 at n = 3000 and +0.3 to +6.7 at n = 6000, from the response).
20. **Abstract: "these pairs concentrate at the waist of the causal diamond and become rarer only slowly with density".** I should have raised this earlier. The body does not show that the low-count pairs become rarer slowly. The only abundance figures (Sec. IV: k < 10 pairs are 50 % of spacelike pairs at n = 1500 and 31 % at n = 3000) fall roughly as n^−0.7. That is not slow. What Sec. IV argues ("Why higher density helps slowly") is that their *errors* decrease slowly, because their τ is set by their position, not by the density. Please either reword ("and their errors decrease only slowly with density") or add the k < 10 share at larger n if it supports the present wording.
21. **Data availability at submission.** The commitment wording is honest for a draft. In the submitted file it will read oddly: "will be made openly available … when this paper is submitted" is either already true or false by the time anyone reads it. Since making the repository public is the step just before upload, please change the sentence to the present tense then ("are openly available at …"), and do the same for Ref. [32]. A Zenodo archive of the tagged release is not required by PRD but would be good practice, as for the companion paper.

Optional, Outlook: "In practice the error will therefore be reduced by additional information rather than by more optimization of Eq. (5)" is a prediction. "is more likely to be reduced" would match the evidence, which is a flat valley rather than a proof that optimization cannot help.

## Recommendation

**Accept.** Comments 15–18 have been handled as described, and I checked each against the v4 text. Comments 19–20 are one-sentence wording changes that the editor can check, or that can be made in proof. Comment 21 is a tense change at the moment of submission. I do not need to see the manuscript again.

---

## Notes for the author (outside the formal report)

What to fix first, by impact:
1. **Comment 20.** The abstract's "become rarer only slowly" is the one phrase a careful referee could contradict from your own Sec. IV (50 % → 31 % between n = 1500 and 3000). Changing "rarer" to "their errors decrease" fixes it.
2. **Comment 21.** Make the repository public, then switch Data availability and Ref. [32] to the present tense in the file you upload. A referee who clicks the link during review must find it live.
3. **Comment 19.** "No larger than" → "of the same order as … and the two fits were not continued equally". Also add the range against the intrinsic end.

An observation you should not turn into a claim: in the new relaxation table, all 30 relaxed maps at n = 6000 have a higher lnL than the converged intrinsic fit (+0.25 to +6.73), under the same stopping test. That is weakly directional. But several margins are below the 2.4 continuation gain, so it is the same situation as comment 15. Route (b) was the right call, and it should stay deleted.

Assessment: this is a solid, carefully hedged PRD paper. The risk that remains is a referee who considers it incremental over Johnston plus Casasola. Nothing in the content has changed that would affect that judgement, so my odds move only slightly, because the last over-claim is gone.

Estimated chance of eventual PRD acceptance: about **75–85 %** as submitted with comments 19–21 fixed, and about the same without them (v3: 70–80 % as it stood, 75–85 % with fixes). This is a judgment call, not data.
