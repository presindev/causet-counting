# Review memory

The persistent notes of the referee session. Update them at the end of every round. History of rounds and comment statuses: `history.json`.

## People & setup
- Author: Roberto Bada (roberto@sapereia.com), SapereIA (Barcelona) + ICCUB. Single author.
- The papers are drafted with an AI writer session (Claude), which the papers disclose in the acknowledgments. A methodology note is in the repo.
- Code and research notebook: https://github.com/presindev/causet-counting
- The papers cite each other as companions: [15] in 3+1 and [22] in 1+1.
- Started 2026-10-30.

## Paper A — `embedding-3p1` (track: `3+1 PRD`)
"Spatial embedding of 3+1 causal sets: low-count spacelike pairs and a likelihood fit to interval counts", 7 pp.
- **Core result:** oracle analysis of Johnston's embedding [PRD 111, 106020 (2025)]. The residual error comes from spacelike pairs whose shared region holds k < 10 elements (94–97%), concentrated at the waist of the diamond. A Poisson/Gaussian likelihood fit to interval counts (Casasola's likelihood), started from an intrinsic weighted-SMACOF overlap map, removes 79–83% of Johnston's residual for n = 3000–15000 (C = 0.9886 → 0.9980 at n = 15000). Median per-pair error halves. In a slab (cylinder) the gain is 58–65%, explained by intervals cut off at the timelike boundary.
- **Universes:** n = 1000/3000/6000/10000/15000 with 1/2/4/8/6 universes.
- **Verified by me:** shell scaling δd/d ~ (κρ d τ³)^(−1/2), giving n^(−1/2); error model δ(τ²)/τ² = δN/2N; the s_ab scale does not affect the maximum-likelihood estimate.
- **Strengths:** paired comparisons, oracles, settings fixed on other universes, start independence, Gaussian vs exact Poisson checked, honest about cost (slower at every size; extrapolated crossover n ≈ 16000).
- **v1 open concerns (major):**
  1. physical significance not argued;
  2. too few universes;
  3. no ablation against Casasola's near-light-cone pseudo-likelihood from the same start;
  4. local optimum (a fit from the truth reaches higher lnL), so try an optimizer upgrade;
  5. time coordinate not refit;
  6. missing references on thickened antichains (Major–Rideout–Surya 2006/2007; Eichhorn–Surya–Versteegen CQG 2019).
- **v1 verdict:** minor-to-major revision; odds 60–75% (higher if comments 1–3 are fixed).
- **v2 (round 2, 2026-10-30):** minor revision, odds 65–75% (70–80% with fixes).
  - **Resolved:** M1–M6, all with new runs.
    - Removed fraction: 72/74/80% at n = 1000/3000/6000 with 10 universes; 44/44 wins.
    - Near-cone pairs do slightly better, so "all pairs" was withdrawn as a contribution.
    - Adam was unconverged; v1's "local optimum" claim was withdrawn.
  - **Verified in v2:** Eq. (4) width; Table III ratios; the near-cone fraction ≈ 3τ₀²/T² (~0.5 at n = 3000, falls as n^−1/2); term counts match the 4D ordering fraction R/n² ≈ 0.05.
  - **Open:**
    - M7: "not by the optimizer". The truth-started fit has HIGHER lnL (+0.9 on average), so the likelihood is near-degenerate rather than flat. Asked for the number of universes with higher truth-start lnL and an lnL scan along the path between the two maps after rotation alignment.
    - m9: the abstract's "roughly halves" is stale (the median falls 33–40%).
    - m10: the error-localization paragraph quotes v1 numbers.
    - m11: references to "version 1" in the manuscript.
    - m12: recommend the near-cone variant and time it.
    - m13: the companion title is outdated.
- **v3 (round 3, 2026-10-30):** minor revision; accept once 15–18 are addressed, no re-review needed. Odds 70–80% (75–85% with fixes).
  - **Resolved:**
    - M7: the "nearly flat valley, O(1)" wording is supported. Relaxed midpoints reach 86/89% within O(1) of both ends, and 2000 L-BFGS iterations move lnL by O(1) with no change in C.
    - m9–m14.
  - **Verified:**
    - abstract numbers (percentile reductions; 44/44);
    - the rms decomposition (0.1·tail² + 0.9·rest²);
    - the recommended variant's 76/82%;
    - the dip explanation (triangle inequality; the relaxed midpoint sits ≈0.15ℓ rms from the straight midpoint, so a small correction recovers ~5e3 in lnL).
  - **Open:**
    - 15: the directional claims ("global max near the accurate map", "slope toward it") rest on sign counts whose margins (0.9/2.3) equal the continuation gain (+0.5/+2.4), i.e. unequal convergence. Recount at equal convergence or delete; n = 1000 (4/10) is omitted.
    - 16: add the s = 0.25/0.75 relaxations; say "no barrier was found".
    - 17: the near-cone share falls as ~n^−0.3, not n^−1/2 (my v2 estimate was crude); state the variant's schedule.
    - 18: Data availability says "openly available" but the repo is not public yet.
- **v4 (round 4, 2026-10-31):** **ACCEPT**, no re-review. Odds 75–85%.
  - **Resolved:** 15 (route b; I searched the whole text and no directional wording is left), 16 (rerun to convergence; numbers verified; 0.15ℓ measured), 17 (fit exponent −0.32 verified; 400-iteration schedule), 18 (commitment wording).
  - **Open (wording only):**
    - 19: "no larger than" the continuation gain is false (mean 0.9 > 0.5; maxima 5.4/6.5). Say "same order" plus unequal continuation, and quote the lnL range against the intrinsic end.
    - 20: the abstract's "become rarer only slowly" is unsupported. The k<10 share goes 50% → 31% (~n^−0.7); it is the *errors* that decrease slowly. I missed this in rounds 1–3.
    - 21: present tense in Data availability at submission.
  - **Noted, not to be claimed:** at n = 6000, all 30 relaxed maps have higher lnL than the intrinsic fit (+0.25…+6.7). This is weakly directional, but some margins are below the 2.4 continuation gain.

## Paper B — `toolkit-1p1` (tracks: `1+1 PRD`, `1+1 CQG`)
"Counting identities in two-dimensional causal sets: spatial distance, depth-drift curvature, and a fixed-size propagator target", 9 pp.
- **Contents:**
  - (i) rectangle identity d² = 2V_A V_B / V_C for any c, and the estimator 2N_A N_B / [ρ(N_C + 1)];
  - (ii) depth drift in de Sitter, d²_est/d² = tanh²(Hτ/2)/[2 ln cosh(Hτ/2)] = 1 − Rτ²/16, giving a curvature estimator R_est = −16β/α (noisy, reads low);
  - (iii) E[K | n] = ½ L_n(μ/2) for Johnston's propagator (the author admits it is no stronger than the ordering fraction);
  - (iv) calibration of the Clough–Evans embedding test plus the null-pair fraction z as a layering flag;
  - applications: transitive percolation and the e^{−βS} model at N = 200 and 400.
- **Placeholder in v1:** the N = 800 held-out test in Sec. VII (`[r27: ...]`). Not assessed.
- **Verified by me:** the rectangle identity; the de Sitter volume, Eq. (7); Eqs. (8)–(11) and R = 2H²; the FRW formula R = 2(ln a)''/a² = −2p η^(−2−2p); E[c_k | n] = C(n,k)/k!; the Laguerre form and its Poisson average to ½J₀(mτ); the Hilb asymptotic. No errors found. The "12" in the text extract is pdftotext's rendering of ½.
- **v1 open concerns (major, same for both tracks):**
  1. no comparison with Hu–Meyer–Meyer in Table II;
  2. ablation needed (bias correction vs general c) against equal-depth Boguñá–Krioukov;
  3. curvature fit window Hτ ∈ [0.2, 0.7] uses H, so it is not intrinsic; no benchmark against Benincasa–Dowker or chain abundances; low offset; a, b inserted by hand; (CQG only) derive the weighting kernel;
  4. structure: four loosely connected results; the propagator target should be demoted (CQG: possibly a separate Note);
  5. why z is needed when height or ordering fraction already detect layering;
  6. e^{−βS} states are not equilibrium samples; the β_c bracket is loose;
  7. missing references (Eichhorn–Surya–Versteegen, Major–Rideout–Surya, Khetrapal–Surya).
- **v1 verdicts:** PRD: major revision with a real chance of rejection, odds 30–45% (50–60% with fixes). CQG: major revision, likely accept after fixes, odds 55–70% (75–85% with fixes). CQG is the subfield's home journal (Johnston 2008, Henson, Rideout–Wallden, 2D orders, Cunningham…).
- **v2 (CQG round 2, 2026-10-30):** retitled "Spatial distance and curvature from an exact counting identity in two-dimensional causal sets". Minor revision, odds 75–85% (85–90% with fixes).
  - **Track change:** the author dropped the 1+1 PRD track; CQG only.
  - **Resolved:**
    - HMM is in Table II; it beats ours above 10ℓ and the claims are restricted.
    - The ablation shows the choice of c gives the accuracy and the correction removes the bias.
    - Restructured; propagator in an appendix.
  - **New results:**
    - curvature window defined from counts;
    - pooled R = −16⟨β⟩/⟨α⟩, which fixes the ratio bias (sign verified);
    - Eq. (12), FRW: 1 − d²est/d² = (τ²/16)[R − (τ/3)dR/dτ]. **Verified by me** with symbolic series (sympy, scratch venv): exact through τ³.
  - **Open:**
    - M8: sprinkled pairs read low (1.70/1.84 vs 2.07). My hypothesis is that nearest-element selection gives a Palm-biased empty neighbourhood that depletes the shallow strip ends; test with uniform selection.
    - M9: the FRW sprinkling test still uses the v1 single-pair estimator.
    - M10: noise comparison in realistic use (pooled pairs in one region vs the ordering fraction).
    - Minor: kernel first moment only; τ⁴ systematic (target 2.07); is the window intrinsic?; version references; complete Glaser [16], [17].
  - **Placeholders skipped:** r27 (N = 800) and the Zenodo DOI.
- **v3 (CQG round 3, 2026-10-30):** minor revision. Odds DOWN to 65–75% (70–80% with fixes), because M10 went against the estimator.
  - **Resolved:**
    - M8: my nearest-element hypothesis was confirmed by the strip counts. Mecke pooling over all position-selected window pairs removes the shortfall; a single uniform draw is biased (1/(1+N_W) reweighting gives λ−1). **Verified.**
    - M9: the pooled FRW result matches the continuum fit; Eq. (12) is downgraded to direction only.
    - M10: the ordering fraction is ~3× more precise in dS, and the in-region drift is biased low by 0.1–0.5.
  - **Significance now rests on:** the identity, the distance estimator and Eqs. (11)–(12). The curvature estimator is not competitive. Secondary: the selection-bias lesson.
  - **Open:**
    - 18: the abstract oversells the estimator (in-region bias; "not more precise" understates ~3×).
    - 19: the Mecke scope. The "count-defined separations" example is configuration-dependent and not covered.
    - 20: "about 30%" is inconsistent. The target exceeds Eq. (12) by 35–53%; Eq. (12) falls short by 26–34%.
    - 21: convexity. f is unnecessary because D is not counted, and convexity is an assumption unless the causal set is an interval.
    - 22: the flat control has 3.4× the elements.
    - 23: repo not public; DOI; r27 still a placeholder after 3 rounds.
    - 24 (optional): a locality test with spatially varying R.
- **v4 (CQG round 4, 2026-10-31):** minor revision; accept once 25–29 are made, no further review. Odds 70–80% (65–75% if 25 is left).
  - **Resolved:**
    - 18 (abstract);
    - 19: route (b) plus a rerun. The v3 P pairs had been drawn sequentially. With a position-based selection the per-region bias is the same, while the ratio of sums pooled over sprinklings is on target. So it is ratio bias, and the argument is sound;
    - 20 (26–35% verified);
    - 21;
    - 22 (matched N; the OF is now slightly better in flat too);
    - 23: r27 filled and reviewed in full. 8/8 layered flagged, 1/20 false positive at z = 0.123 against 0.120, reported fairly;
    - 24: not run; the Discussion fallback ("analytic and conceptual") is met.
  - **Open:**
    - 25: the abstract's "on average over independent sprinklings" (MY v3 wording) reads as the mean of per-region estimates, which is biased. Say "coefficients summed over the pairs of many sprinklings".
    - 26: the Fig. 3 paragraph still says "rectangle lies inside".
    - 27 (optional): the flat control is matched in N but not in proper depth (τ ≈ 1.85 vs 0.96, lever arm ~3.5×); 1.1σ vs 1.3σ.
    - 28: r27 reporting.
      - Limitations should add the stress result: 3/19 continuum-like states are above the band, so the full test rejects ~4/20.
      - Also: M; how 0.120 was derived; flat height 2√N ≈ 57; small-sample caveat; placement of the "test inputs" sentence.
    - 29: present tense in Data availability, plus the DOI.
  - **Placeholder left:** Zenodo DOI only.
  - **Not verified:** [16] Glaser–Surya CQG 33, 065003.

## Issues common to both papers
- ~~Citation to check: Hu–Meyer–Meyer~~ **Settled in round 2:** the arXiv record of 2601.03280 (submitted 31 Dec 2025) lists JMP 66, 122502 (2025), DOI 10.1063/5.0290407. The citation is correct; I withdrew the comment. I could not check Madsen arXiv:2610.36695 (not indexed). Glaser's Ising paper is CQG 35, issue 8 (2018).
- Key prior results come from preprints that are not peer reviewed (Casasola on Research Square, Pellegrin on Zenodo, Madsen).
- Some referees may read a single author with a company affiliation, plus a detailed AI-use disclosure, with more scepticism. The open code helps.

## Lessons / working notes
- `pdftotext -layout` garbles fractions and two-column equations. Render the page before claiming a typo (e.g. s_ab in 3+1 Eq. (4) was only ambiguous, not wrong).
- PRD has no official referee checklist online that I could reach; I used the APS family guidelines. CQG: the IOP "about" page; the IOP Reviewer Guide PDF from 2025 returned 404, and a 2024 version exists.
- The user wants honest odds and a separate section for the author outside the formal report.
- Round 2 lesson: check that the abstract's qualitative claims ("roughly halves") still match the new numbers. Revisions often update the tables but leave stale wording, and paragraphs quoting "version 1" numbers next to new figures.
- Round 2 lesson: when an author reports a "truth-started fit with higher lnL", that cuts against any claim that "the optimizer is not the limit". Read the sign of ΔlnL carefully.
- Round 2 lesson: coordinate-based selection of "nearest sprinkled element" is Palm-biased (empty neighbourhood). Watch for this in any test with "sprinkled pairs".
- Tooling: no sympy in the system python. Use a scratch venv (`python3 -m venv $SCRATCH/venv; pip install sympy`).
- In zsh, `echo =====` fails ("= not found"); use `echo '-----'`.
- Round 3 lesson: when an author adds a "continued optimization" result, compare its gain with the margins of any sign-count claim. Equal-convergence comparisons matter.
- Round 3 lesson: a Mecke/Slivnyak unbiasedness argument covers only position-based selections. Watch for authors extending it to count-based (configuration-dependent) rules.
- Round 3 lesson: check "exceeds by X%" vs "falls short by X%" phrasings against the raw numbers; they differ a lot at the 30–50% level.
- Round 3 lesson: Data availability statements saying "openly available" when the repo is still private. Check against the answer letters.
- 1+1 PRD track: frozen after round 1. Don't touch it.
- Round 4 lesson: check my OWN earlier suggested wording against new results. My v3 phrase "true as an average over independent sprinklings" was adopted into the abstract, and the author's rerun then showed that per-region averages are biased. Distinguish "mean of ratios" from "ratio of pooled sums" everywhere.
- Round 4 lesson: when a sentence says margins are "no larger than" X, check both the means and the maxima against X.
- Round 4 lesson: a matched element count is not matched geometry. For depth-fit estimators the proper-depth lever arm drives the noise.
- Round 4 lesson: for a held-out classifier test, check that Limitations reports every statistic's false positives (not just the new flag's), and that the sample sizes are stated.
- Abstract qualitative phrases ("rarer only slowly") can survive several rounds unchecked. Re-derive each one from body numbers at least once.

## Final advice given to the user/writer (2026-10-31, end of session)
- **Realistic odds** (shaded below the report odds, because the writer and I are the same model and share blind spots):
  - 3+1 → PRD ~65–80%;
  - 1+1 → CQG ~55–75%, higher if the locality test favours the drift.
- **Main risks:**
  - significance/incremental;
  - scepticism toward a single author with a company affiliation and an AI disclosure;
  - the rectangle identity may already be known;
  - unverified refs (Madsen 2610.36695, Glaser–Surya CQG 33 065003, Eichhorn et al. 2605.27514);
  - reproducibility once the repo is public;
  - the small N = 800 sample.
- **Sent to the writer (final message):**
  - fill or drop `[Zenodo DOI]`; make the repo public;
  - hand-check the refs; clean-clone rerun; a human expert read; arXiv at submission.
- **Comment 24 (locality test), CQG only, optional.** It would answer "what is the estimator for?"
  - The drift probably loses: its footprint reaches down to Hτ ≈ 1, and it already lost ×3 to the OF.
  - Design to fix in advance: spatially varying R; error on ΔR between two locations; OF diamonds matched to the drift footprint and N; position-based pairs; decision rule written down; report either way.
  - Timebox 1–2 weeks; otherwise submit and keep it as the reply to a referee.
- **Fallback venues if rejected:** 3+1 → CQG; 1+1 → PRD or a mathematical-physics journal.
- **Next possible requests:**
  - journal referee reports arrive: help draft responses, judging the referee's points independently, not defending by reflex;
  - comment 24 results arrive: check the matching and that the decision rule was applied as fixed in advance.

## Closing check of v5 (2026-10-31): FINAL
- I verified the v5 text of both papers. All changes for 3+1 comments 19–21 and CQG comments 25–29 are in.
  - CQG adds Last–Penrose [33] for Mecke. The renumbered citations are consistent, and the methodology note is now [47].
- No review files were written for v5; it was a confirmation only (`closing_check` in history.json).
- Still to do at upload:
  - make the repository public;
  - fill or drop `[Zenodo DOI]` in both papers.
- The loop is closed unless the editor's referees come back.

## Status at end of round-4 session (2026-10-31)
- Round 4 done: `review-embedding-3p1-v4.md` (ACCEPT) and `review-toolkit-1p1-v4.md` (minor; accept once 25–29 are made, no further review).
- Both reports say no further review is needed. If a v5 arrives, do only a compliance check:
  - 3+1: comments 19–21;
  - CQG: comments 25–29, especially the 25 abstract phrase, 28(a) Limitations stress, and the DOI being real.
- Likely next request: the paste-ready prompt for the writer, as one code block grouped by track and comment number.

## Status at end of round-3 session (2026-10-31, superseded)
- Round-4 prompt sent to the writer (both tracks). It asks for `<slug>-v4.pdf`, `-v4-diff.pdf` and `answer-<slug>-v4.md`, answering 3+1 comments 15–18 and CQG comments 18–24, with placeholders listed at the top.
- Both v3 reports said no re-review is needed if the comments are handled as described. For v4, offer a **quick compliance check** (each comment against the v4 text, plus an abstract-number check) unless the user asks for a full round. Write it as `review-<slug>-v4.md` anyway, so history.json stays consistent.
- Things to watch in v4:
  - 3+1 #15: route (a) recount at equal convergence, or (b) deletion. Either way, check the abstract, Sec. V, Discussion and Outlook all agree.
  - CQG #18: abstract bias and precision wording.
  - CQG #19: the count-defined example was removed or tested.
  - CQG #20: one consistent "exceeds" or "falls short" figure.
  - CQG #21: f dropped; Table III caption fixed.
  - CQG #22: flat-control element count.
  - CQG #23: r27 filled and checked (no longer a placeholder!), repo public, DOI.
  - CQG #24: optional locality test. If it was done, it can raise the CQG odds.
  - The answer's slip of 7511 s vs 7691 s (3+1).
