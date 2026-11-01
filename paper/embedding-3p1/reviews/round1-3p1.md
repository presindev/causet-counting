# Round 1 — referee report on embedding-3p1-v1.tex (first split draft)

**Recommendation: major revision.** The likelihood fit vs Johnston's own benchmark is a solid, fairly-credited result (79–83 % residual removal, robust across universes, paired). But (i) the headline diagnostic claim about *where Johnston's error lives* is not demonstrated by the oracle actually run, (ii) the only quality metric is a Pearson correlation and the per-pair errors are still pending, so the 80 % figure lacks physical meaning, (iii) several numbers are internally inconsistent (start range, universe counts), and the main body silently uses a method listed as abandoned in App. A. The "cannot remove at any density" argument is a scaling heuristic presented as proof.

## Major (ranked)
1. **[needs-work] The low-count claim is not tested on Johnston's method.** Abstract: "the residual error of the method [Johnston's] comes … almost entirely from pairs whose shared causal regions contain fewer than ten elements". The k<10 oracle (r18, `oracle_waist`) replaces *overlap* distances by the truth — it shows the low-count pairs ruin the *overlap* embedding, not Johnston's. Fix: run Johnston's r with truth on k<10 only (and truth on k≥10 only), or rewrite the claim.
2. **[needs-work] Per-pair errors pending.** Pearson ρ_s near 1 is dominated by far pairs and insensitive to global rescaling. Give a scale-sensitive metric (rms after Procrustes incl. scale) at every n.
3. **[writing] Overclaims.** "cannot remove this error at any density"; "Small counts should not be inverted into distances at all" — Eq. (5) is an order-of-magnitude scaling; the k<10 share itself falls with n (50 % → 31 %). "does not depend on the starting map" (3+2 universes, n ≤ 3000). Exponents fitted to three points without uncertainties.
4. **[writing] Sec. IV contradicts Table I.** "The overlap distances are accurate wherever k≥10" vs Table I median bias −0.11 to −0.17 in every separation bin.
5. **[writing] Three different universe sets give three diamond percentages without labels** (n=3000: 80 % Table II; 74–75 % check iv; 74–76 % start independence; 75/80 % Sec. VI with true times).
6. **[writing] Sec. VI "entire difference" too strong** for ±9 % errors on 4 universes; abstract omits that the gain falls to 43 % at n=1500 and is negative at n=600.

## Minor
ρ symbol clash (density vs correlation; σ_ab vs logistic σ; N vs n); figure legend vs text ("ours alone", "Poisson likelihood", "events"); Table I "capped by detour bound" vs App. A; Sec. VII placeholder only, "≈ n²" is wall time; literature-search paragraph not PRD register; Table IV mention invites a request; whether n includes tips; reference formatting (DOIs, years; verify HMM25 and Madsen26 identifiers); "30–50 % at a few thousand elements".

## Rule (2) (abandoned approaches only in App. A)
Intro pointer to App. A must go if the appendix is deleted; "Overlap estimate capped by the detour bound" listed as abandoned but used in Table I; "direct embedding of overlap distances" kept in main body — defensible as a diagnostic; App. A item 2 duplicates and conflicts with the start-map numbers.

## Number consistency
Start-map range is 23–47 % (Table II), not 26–47 %; App. A "42–45 % at n≤3000" vs 47 % in Table II; "21 universes" for n=3000–15000 is 20 (21 includes n=1000); overlap exponent ≈ n^−0.4 (v2) vs n^−0.43; "fading with n" dropped. Unchanged and correct: Table I, Table II core values, oracle values, reproduction numbers, checks (i)/(iv), slab numbers, appendix percentages.
