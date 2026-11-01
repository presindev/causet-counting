# Review of embedding-3p1-v6 (language pass), 2026-11-01, session 21

**Scope.** v6 = v5 + a final language pass for the PRD register. No number, equation, citation, table value, result or hedge was meant to change;
`embedding-3p1-v6-diff.pdf` (latexdiff against v5) shows every edit. 9 pages in both v5 and v6.

## What changed (by kind)
- **Long sentences split** where several results were stacked with semicolons and brackets: Sec. III (reproduction of Johnston's Tables III–V;
  the candidate statistics for Table IV now read "0.969 for ..., 0.932 for ..."), item 3 of the contribution list, the slab set-up (four-leg
  fallback), the Outlook.
- **Definitions and referents made explicit:** "We call each sprinkling a universe" (the word was used from the abstract on without a definition);
  "leaves it unchanged" → "leaves $\mathcal C$ unchanged"; "the 99th" → "the 99th percentiles"; "the tail" → "the tail of the error distribution";
  "improves less than the median" → "than the median position error"; "75.4 % instead of 74.5 %" now says it is the fraction of Johnston's residual
  removed; "the detour ..., an upper bound" → "an upper bound on the spatial distance"; the relative error δN/2N is "of τ²".
- **Register:** "Why ... is worth stating" → "Because the benchmark is itself flat, it is worth stating why ..."; "adding them naively hurt" → "made the
  fit worse"; "matched Johnston" → "matched Johnston's embedding"; "For use we recommend" → "For applications ..."; "Retained only as the starting map"
  → full sentence; caveats in Sec. VI numbered "First / Second".
- **Grammar:** "more likely to be reduced by additional information rather than by" → "... than by further optimization"; "as a second-order
  shortening effect would and a barrier would not" → "as expected from a second-order shortening effect and not from a barrier"; "This dip is expected
  without a barrier" → "expected even in the absence of a barrier".
- **Spelling:** American throughout (programme → program, analysed → analyzed).
- **Abstract:** "(Casasola's)" moved in front of the noun; "his residual" → "its residual error"; "more than halves its tail" → "more than halves the upper
  tail of their distribution" (90th and 99th percentiles both fall by more than half, Sec. V).

## One wording change to check
- Sec. V, continued L-BFGS: v5 said the gain of 0.5 / 2.4 is "as much as separates the two maps"; v6 says "of the same order as the difference
  between the two maps". This matches the wording the referee asked for in comment 19 and is not stronger (the mean separation at n = 3000 is 0.9,
  so "as much as" was slightly loose). Revert if Roberto prefers the v5 phrase.

## Substantive points noticed, left unchanged (not language)
1. Sec. IV, last sentence of the estimator paragraph: "bias below 1 % for d ≥ 4ℓ, and 6–8 % below 2ℓ" — unclear whether 6–8 % is the median error or
   the bias. Check `sims/r11_4d_distance.py` output before submission.
2. Sec. IV, "Why higher density helps slowly": "between n = 3000 and 6000 it still halves" — "it" can be read as the overlap residual or Johnston's.
   Probably the overlap residual; confirm from the r35 numbers.
3. Sec. V Results: "The removed fraction rises at most slowly with n, so the gap does not close" — "the gap" is not defined (gap to the oracle? to
   Johnston?). Needs one word once the intended meaning is confirmed.
4. Sec. IV: "The detour is poor for close pairs, where no element lies between them" — "between" for a spacelike pair is informal (presumably: no
   element related to both near the straight line). Left because the precise condition is a content choice.
5. Checks (iv): "the map no longer changes" sits next to Sec. V's "+1–2×10⁻⁴ in C" after convergence; consistent at the stated precision, but a
   pedantic reader may ask.

## Compile
`tectonic -X compile` clean (no errors, no undefined references). Box warnings are the same as v5: Table I is 34–37 pt too wide (pre-existing), the
Data availability paragraph and some bibliography entries are underfull (long `\texttt` paths/URLs). New: one overfull `\vbox` of 2.6 pt in the
bibliography page (harmless). latexdiff ran (it warns that `kpsewhich` is missing; output is fine) and the diff compiles to 9 pages.
