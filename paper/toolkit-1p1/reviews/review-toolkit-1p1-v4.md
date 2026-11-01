# Referee report — Classical and Quantum Gravity (fourth round)

**Manuscript:** "Spatial distance and curvature from an exact counting identity in two-dimensional causal sets" (R. Bada), version v4 (dated October 31, 2026), with the author's response `answer-toolkit-1p1-v4.md` and a latexdiff against v3.

**Criteria applied:** CQG Research Papers are "reports of high-quality original research with conclusions representing a significant advance in the field". The IOP referee assessment covers:
- originality;
- significance;
- scientific soundness;
- whether the conclusions are supported;
- clarity of presentation;
- appropriate referencing;
- suitability for the journal's readership.

The recommendation is one of accept, minor revision, major revision or reject. IOP's research data policy also applies (persistent identifier for code).

**Scope:**
- **Not assessed.** One placeholder remains: the Zenodo DOI in Data availability.
- **Newly assessed.** The N = 800 held-out test in Sec. VI (r27) is now filled. It was out of scope in rounds 1–3, so I review it in full here (comment 23).
- **Method.** The third report said I would not need to see the paper again if comments 18–21 were handled as described, so this round mainly checks that. I used the diff to locate changes and judged the clean v4 PDF.

---

## Summary

v4 answers the third report:
- **Abstract (comment 18).** It now states that the curvature estimator is less precise than the ordering fraction (about three times in de Sitter space) and biased low within one region, and it qualifies the sprinkled-pair agreement as "within 1.7σ".
- **Mecke scope (comment 19).** The count-defined example is removed, and the condition is stated precisely. The author also found that the one-region pairs had been drawn one at a time, which is the biased single-draw mechanism, and reran the comparison with a position-based selection. The in-region low bias persists, and is shown to come from forming the ratio within one region.
- **FRW and window (comments 20–21).** One FRW shortfall figure (26–35 %) is used throughout, "to leading order" is added to the abstract, and the window argument is simplified (no f) with convexity stated as an assumption.
- **Flat control (comment 22).** It is rerun at matched element count. The ordering fraction is now slightly more precise in flat space too, where v3 had the two spreads equal.
- **r27 (comment 23).** Filled: 8 of 8 layered states flagged, 1 of 20 continuum-like states flagged (a false positive, reported as such).
- **Comment 24 (optional).** The locality test was not run. The Discussion now says plainly that the curvature result is analytic and conceptual, and states the selection-bias lesson.

## Assessment

**Soundness.** All the new material is correct, as far as I can check it. Details:
- **The ratio-bias argument (comment 19) is sound.**
  - The per-region estimate is R_r = −16 Σ_r β / Σ_r α. For a position-based selection, Mecke makes E[Σβ] and E[Σα] equal to their inserted-pair values, but E[ratio] ≠ ratio of expectations.
  - The second-order correction is set by the relative variance of the denominator and the covariance of numerator and denominator. Within one region that relative variance is large (the spread, 2.32, exceeds the mean) and does not fall with P, because the pairs share their common pasts.
  - The rerun shows exactly the expected signature:
    - the position-based per-region mean is as low as the sequential one (1.67 vs 1.63; 1.95 vs 1.92), so selection is not the cause;
    - the ratio formed from sums pooled over the 400 sprinklings returns to the target within errors (1.96 ± 0.12 and 2.04 ± 0.07 against 2.10);
    - the bias shrinks with density (0.43 → 0.15) as the relative variance falls.
  - "It is the ratio that is biased, not the sums" is a fair one-line summary.
- **The new Sec. IV paragraph.** Its numbers check:
  - 2.10 − 1.67 = 0.43 and 2.10 − 1.95 = 0.15;
  - the standard errors are 2.32/√400 = 0.12 and 1.34/√400 = 0.07;
  - 2.32/0.80 = 2.9 and 1.34/0.46 = 2.9 give "about three times".
- **The selection described.** A fixed position window for a and for the offset of b, and independent thinning with a probability fixed across sprinklings (set on pilot sprinklings that are not analysed): this is a position-based selection in the Mecke sense.
- **Flat control (comment 22).**
  - The matched densities are 4000 × 2511/8413 = 1194 and 10⁴ × 6280/21034 = 2986.
  - The quoted offsets match the spreads: 0.89/20 = 0.045 and 0.54/20 = 0.027.
  - Stale material removed: the v3 sentence "the two spreads are equal (0.44 and 0.43)" and the 8.4×10³ figure no longer appear anywhere (searched).
  - Limitations' "0.05–0.43" covers the de Sitter (0.43, 0.15) and flat (0.16, 0.05) in-region biases.
- **FRW shortfall (comment 20).** From the unrounded values in the response, 1 − 0.518/0.699 = 25.9 %, 1 − 0.557/0.790 = 29.5 % and 1 − 0.588/0.901 = 34.7 %. "26–35 %" is right, and it is used in both Sec. IV and Limitations.
- **Window and convexity (comment 21).**
  - The argument is correct and now minimal: the estimator counts A, B, C ⊂ I(c, a) ∪ I(c, b), and causal convexity of a region containing c, a, b puts both intervals inside it.
  - In a coordinate box, the diamond I(c, a) lies in the box if and only if its four corners do (the box is convex and the diamond is the convex hull of its corners). The corner check that the response describes is therefore exact.
  - The Table III caption ("N_C ≥ 20, down to the deepest c with I(c, a) and I(c, b) in the box") now matches the Sec. IV rule.
  - One description elsewhere was not updated (comment 26).
- **r27 (comment 23).**
  - **Counts.** 28 = 7 β × 4 seeds, and 8 layered + 20 continuum-like = 28.
  - **Consistency with N = 400.** The 8 layered states are presumably the β ∈ {0.45, 0.7} chains, consistent with Sec. VI's statement that random starts become layered at β ≥ 0.45 at N = 400.
  - **Threshold.** 0.120 at N = 800 against 0.13 at N = 400 fits the decreasing flat median of z.
  - **Fair reporting.** The one false positive is reported as a false positive under classes fixed in advance. The post-hoc reason why it might be partly layered is clearly labelled as such. That is the right way to report a pre-registered test.

**Abstract against body.** Every number and qualitative claim in the abstract traces to the body:
- "two" and "ten discreteness lengths": Tables I–II;
- "at all separations" and the HMM statement: Table II;
- the de Sitter closed form: Eq. (11);
- FRW "one third … to leading order": Eq. (12);
- "within 1.7σ": Table III, (2.08 − 1.91)/0.10;
- "nearest … biases it low": Table III, nearest rows;
- "about three times larger" and "biased low within one region": Sec. IV, one-region comparison;
- "lets the test reject layered orders on its own": Sec. VI, 8/8 at N = 800, 18/18 at N = 200.

One phrase is now imprecise in the light of the author's own rerun (comment 25). The fault is partly mine: the wording comes from my third report.

**Significance.** Unchanged from round 3. The paper stands on:
1. the exact rectangle identity and the distance estimator;
2. the closed-form de Sitter drift and the leading-order FRW form.

The curvature estimator is honestly presented as not competitive with the ordering fraction for one region. The selection-bias lesson is now stated as a general methodological point. The r27 result adds genuine held-out support for the layering flag, with a small sample. The optional locality test (comment 24) was not run, so the practical case for the curvature estimator is not restored. The Discussion now says so plainly, which is what I asked for as the fallback.

For CQG's specialist readership I still judge this sufficient. The margin is the same as in round 3.

---

## Status of third-round comments

| # | Comment (v3) | Status | Reason (checked in v4 text) |
|---|---|---|---|
| 18 | Abstract more favourable to the estimator than Sec. IV | **Resolved**; one phrase now imprecise (comment 25) | The abstract states "less precise than the ordering fraction (… about three times larger) and, within one region, biased low" and "within 1.7σ". The Limitations wording matches. |
| 19 | Mecke scope; "independently of neighbourhoods"; how the P pairs were drawn | **Resolved** (route b, plus a rerun) | The count-defined example is removed. The text says such a selection "does not satisfy the condition … and we have not tested it". The condition is stated as I suggested. "Independently of their neighbourhoods" is gone from the abstract and Limitations. The P pairs are now position-based and described; the sequential draw is kept as a check. The ratio-bias conclusion is sound (see Assessment). |
| 20 | "About 30 %" inconsistent; "to leading order" | **Resolved** | "Falls short … by 26–35 %" in both Sec. IV and Limitations (verified from unrounded values); "to leading order in the depth" is in the abstract. |
| 21 | Convexity: f unnecessary; convexity is an assumption; Table III caption | **Resolved**; one stale description elsewhere (comment 26) | The argument rests on I(c, a) ∪ I(c, b), with f dropped. Convexity is "an assumption about the sprinkled region", decided by the order only for order-defined causal sets. The caption matches the Sec. IV rule. |
| 22 | Flat control at 3.4× the elements | **Resolved** | Rerun at matched element count (2.5×10³ and 6.3×10³). The changed result (ordering fraction "slightly" more precise in flat space) is carried into Sec. IV, and the old "two spreads are equal" no longer appears anywhere. Limitations and the abstract mention only the de Sitter factor, which is correct. One interpretive caveat is optional (comment 27). |
| 23 | Data availability; DOI; r27 | **r27: resolved**, with reporting points (comment 28). **Data availability: resolved as worded**, with an edit due at submission (comment 29). **DOI: placeholder**, out of scope, condition of acceptance | See below. |
| 24 | (Optional) locality test | **Not run; fallback met** | The new Discussion paragraph "What the curvature result is" says the curvature result is "analytic and conceptual", that the locality advantage "is untested", and states the Palm/Mecke selection-bias lesson as a general methodological point. Sec. IV's "What the depth drift adds is geometric …" is consistent with this. |

Earlier comments: M1–M7 and comments 8–17 remain resolved. m6 (DOI) is still a placeholder, and m7 (IOP style) is deferred to the final version, as agreed.

---

## New comments

25. **Abstract: "reproduces on average over independent sprinklings the same fit on the exact continuum volumes".** This wording came from my third report, and the author's own rerun shows it is imprecise. "On average over independent sprinklings" reads naturally as the mean of the per-sprinkling estimates. That mean is biased low: 1.67 against 2.10, Sec. IV, which the next sentence of the abstract also says. What Table III reports, and what Mecke guarantees, is the ratio of fit coefficients summed over the pairs of many sprinklings before the ratio is formed. Suggested: "A fit of this depth drift, with its coefficients summed over the pairs of many independent sprinklings, reproduces the same fit on the exact continuum volumes …". The Limitations sentence "The curvature estimator must be pooled over all pairs of a position-based selection" could add "… and over many independent regions; within one region the ratio stays biased (below)".
26. **Sec. IV, "Test on sprinklings" (Fig. 3).** This paragraph still says "every sprinkled c in their common past whose rectangle lies inside the region". That is the v3 rule; the fit window is now defined by I(c, a) and I(c, b). If Fig. 3 was made with the interval rule, please update the sentence. If it really uses the stricter rectangle rule, please say that Fig. 3 uses a stricter cut than the fit.
27. *(Optional.)* **Flat control.** The flat diamond is matched in element count, but if I read the geometry correctly it is not matched in proper depth. With u, v ∈ [−3, −0.95]:
    - the pairs at η ≈ −1.15 see c down to a proper time of ≈ 1.85 in flat space;
    - in de Sitter space the same c are only ≈ ln(3/1.15) ≈ 0.96 below.

    The lever arm in τ² is therefore ≈ 3.5 times longer in the flat control. That alone would make the flat drift much less noisy, which may explain most of why the drift's spread falls from 2.32 (de Sitter) to 0.89 (flat) while the ordering fraction's stays at 0.80. The within-geometry comparisons that the paper draws are fair. A short remark would stop readers from attributing the de Sitter vs flat contrast (×3 vs "slightly") to curvature.

    Also, the "Pooling" paragraph says "within 1.1σ at both densities" for inserted pairs. From the rounded Table III values the second is (2.08 − 1.99)/0.07 = 1.3σ. Either quote the unrounded entries or say 1.3σ.
28. **The N = 800 held-out test (Sec. VI, Limitations).** It is reported fairly. Please address five points so that a reader can weigh it:
    - **(a) Limitations is less complete than Sec. VI.** Sec. VI reports that three of the 19 unflagged continuum-like states have a stress above the N = 800 flat band (0.086–0.110 against 0.081). Limitations mentions only the z false positive.
      - At this size, then, the embedding test as a whole (spectrum, stress and z) rejects 4 of the 20 continuum-like states, assuming the z false positive's stress is in the band. Please state that state's stress.
      - Sec. V's "this test passes every continuum-like state" is an N = 400 result and should say so.
      - One sentence in Limitations would cover both points.
    - **(b) M and the threshold.** Please give M at N = 800, and say how z > 0.120 was obtained (presumably 1.5 times the median of the 50 fresh flat orders, as at N = 400).
    - **(c) Context for the false positive.** A random two-dimensional order of 800 elements has a height of about 2√N ≈ 57. The 27-layer state is about half that, whereas the N = 400 continuum-like states had 30–39 layers against ≈ 40. Stating this would let a reader judge the post-hoc remark, without changing the classification fixed in advance.
    - **(d) Sample size.** With 8 and 20 states, "all 8" and "1 of 20" carry wide uncertainties: one-sided 95 % lower bound on sensitivity ≈ 0.69; false-positive rate 1/20 with a 95 % interval of roughly 0.1–25 %. Only one of the eight layered states (stress 0.072) actually tests the blind spot that z is meant to close. A clause such as "on a small held-out sample" is enough.
    - **(e) Placement.** The sentence that follows ("These states are test inputs, not equilibrium samples: chains started from layered orders accept ≤ 0.1 % of the moves") now reads as if it referred to the N = 800 chains, which all started from random orders. Please make clear that it refers to the N = 400 states.
29. **Data availability at submission.** The commitment wording is honest for a draft. In the submitted file, "will be made openly available … when this paper is submitted" will already be true or false when anyone reads it. Please make the repository public, mint the Zenodo DOI from the tagged release, and switch the statement and Ref. [46] to the present tense in the file you upload. As in round 3, I would ask the editor to make a working DOI a condition of acceptance.

## Recommendation

**Minor revision. Accept once comments 25–29 are made; no further review needed.** Comments 18–22 are resolved as described, each checked against the v4 text. The r27 held-out test is now filled, checked and fairly reported. The new comments are textual:
- comment 25 corrects one abstract phrase (my own earlier wording);
- comments 26 and 28 are precision and completeness edits;
- comment 27 is optional;
- comment 29 is a tense change plus the DOI at submission.

The editor can verify them without sending the paper back to me.

---

## Notes for the author (outside the formal report)

What to fix first, by impact:
1. **Comment 25 (abstract).** "On average over independent sprinklings" says the opposite of what your rerun found for per-region averages. Replace it with "with its coefficients summed over the pairs of many independent sprinklings". This is my fault from round 3, but it is in your abstract.
2. **Comment 28(a).** Put the N = 800 stress result in Limitations next to the z false positive. A referee who reads Sec. VI carefully will count 4 of 20 continuum-like states rejected by the full test, and should not find that only in the body.
3. **Comment 29.** Make the repository public, mint the DOI, and switch to the present tense before upload.
4. **Comments 26, 27, 28(b–e).** Small edits, about one sentence each.

On the comment 19 rerun: well done. You checked a mechanism you could have waved away, found that the v3 pairs had in fact been drawn the biased way, and still reached the right conclusion with the clean selection. That is the kind of care referees remember.

On r27: one false positive in 20, reported against classes fixed in advance, is a credible result. The post-hoc story about the 27-layer state is plausible, and keeping it out of the classification was right. Do not soften it further.

What changed in my assessment: very little. r27 adds a modest amount of independent support for the diagnostic. Comment 24 was not run, so the practical case for the curvature estimator is still missing. The main risk remains a referee who asks what the curvature estimator is for. The new Discussion paragraph answers that honestly ("analytic and conceptual"), which is the best answer available without the locality test.

Estimated chance of eventual CQG acceptance: about **70–80 %** with comments 25–29 made, and about **65–75 %** if the abstract phrase in comment 25 is left as is (v3: 65–75 % as it stood, 70–80 % with comments 18–23). A locality test showing an advantage would still be the one thing that could move this higher. This is a judgment call, not data.
