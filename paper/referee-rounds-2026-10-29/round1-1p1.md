# Round 1 — referee report on toolkit-1p1-v1.tex (first split draft)

**Recommendation: major revision.** The individual results appear correct (every listed derivation re-derived by hand, no errors), but as written the paper is four loosely coupled tools with a list-title, list-abstract and list-introduction. **Journal fit:** as it stands, CQG fits better (the paper's own lineage is mostly CQG); PRD is fine if restructured. **Coherence fix:** "In 1+1, conformal flatness and 2D-order combinatorics give exact counting identities; deviations from them are diagnostics (depth drift → curvature; Laguerre and null-pair deviations → non-manifoldlikeness)." Reorder so the e^{-βS} application comes after the propagator.

## Major (ranked)
1. **[writing] Framing and ordering** as above; the embedding calibration has no exact identity behind it — present it as an empirical companion.
2. **[needs-work] No baseline for the rectangle estimator.** Compare with the direct N_D count (Brightwell–Gregory/Rideout–Wallden) and with BK24 at equal time; "no measurable bias above 2ℓ" is asserted but not shown (give mean signed error ± SE); choosing the deepest c (largest N_C) makes N_C non-independent — discuss or use a count-independent rule.
3. **[needs-work] "Unbiased on average" (Sec. IV) unsupported** — every entry sits 0.5–1.5σ low; v2 said "right on average". Soften, derive the depth-weighting kernel, compare noise with Benincasa–Dowker.
4. **[needs-work] Show the Laguerre target adds beyond the ordering fraction**; rms over pairs is not a test statistic (give a null distribution); Fig. 5 lacks the ~10-layer states; "K never becomes negative" is τ reasoning, not fixed-n.
5. **[writing] Embedding claims exceed data**: abstract "fails to flag layered orders" (only ~10 layers missed); 2–3-layer states unprocessable ⇒ make "unprocessable ⇒ flagged" formal; undefined "fraction of spectrum"; 2+1 claim feeds a 1+1 formula a 2+1 density.
6. **[writing] Sequential growth**: p_n = 3/n is not a Rideout–Sorkin rule; N = 100 is at the calibration edge; present as a sanity check.

## Minor
Notation (elements/events/universes; null-pair fraction vs "share of zero-length pairs"); |K| bound applies to ⟨K⟩; cite Myrheim and Meyer; Laguerre–Bessel asymptotic needs Szegő; verify HMM25; companion and MethodNote status; MDS eigenvalue normalization; "exact as d→0" requires c below the midpoint; Fig. 3 solid curve vs closed form; shallow bin = residual (1−e^{−λ_C}); "drift" vs ratio; unit-dependent windows; condense novelty-search paragraph; declarative section title.

## Rules (2)/(3)
Intro pointer to App. A; Sec. V "below N≈50 a flat universe scores as badly as a crystal" rests on the abandoned small-N ensembles; "(Without the +1 … 11 % high)" borderline; Intro pointer to the methodology note (rule 3: acknowledgment only); 3π outlook lost its "consistency check, not a new result" qualifier.

## Math and numbers
All derivations correct (rectangle identity, Poisson correction, de Sitter volumes and series, FRW curvature values, Laguerre and its Poisson average, β_c = 0.094). Cosmetic: ln of negative η in V_A; "R = 1.88" is a continuum-fit value. Changes in the split: Table III lost "(β≤0.3)" and "(β≥0.6, 8–13 layers)"; "right on average" → "unbiased"; 3π qualifier dropped; abstract dropped "at N = 200 and 400".
