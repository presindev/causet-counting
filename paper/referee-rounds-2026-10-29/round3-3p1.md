# Round 3 — referee report on embedding-3p1-v1.tex (after revision 2)

**Recommendation: minor revision**, conditional on the \pending items and fixing universe-set bookkeeping. Done properly: low-count oracle on Johnston's own detours; \mathcal C throughout; start-map range 23–47 %; 20 vs 21 universes consistent; slab wording softened.

## Major
- **M1 [writing] "Diagnostic set" at n=3000 is two different sets.** "31 % at n=3000" is from r18 (seed 2029); the 96 %/4 % oracle from r30 (seed 2028; k<10 share 0.356). Several numbers sit outside sets (a)–(c): Sec. III oracle 0.903→0.9999 at n=1000, the reproduction (ten sprinklings), per-pair medians 0.112/0.132 at n=1000, check (i), Johnston's 0.915 at n=1500.
- **M2 [needs-work, cheap] Per-pair paragraph says "Set (a) seeds" but r29 ran s1000–s1002**; set (a) uses s1001+ and has no n=1500; r29's n=3000 Johnston correlation 0.9575 ≠ Table II 0.9515.
- **M3 [writing] Preliminary r29: distance errors improve clearly** (median ~0.18→0.11 ℓ, q90 ~0.69→0.28, q99 ~2.6→0.6) **but rms position barely moves** (0.60/0.63 → 0.53/0.49 ℓ). A referee will ask why; don't let the abstract pick only the flattering metric.

## Minor
Abstract "counts stay small at any density" vs falling share (50 %→36 %); "as a scaling argument explains" → "consistent with"; contribution 2 "any embedding" overclaims; "79–83 % … in every universe" reads per-universe; start independence: one alternative start only; check (iii) K0 "by (ii)" does not follow; start share not monotonic in n; detour cap rigorous only for true R; slab abstract vs body; "88–96 %" overlap oracle from a different set than r30 next to it.

## Rules
No AI language in main text; strip the .tex header comments before submission; the one Intro pointer to App. A must go with it; direct overlap embedding framed as diagnostic — acceptable.

## Numbers
r30 97/96 %, 3/4 % ✔; "(99 % vs 2 % with k<30)" only at n=1500 (n=3000: 98 %); "31 % at n=3000" ✘ vs r30 (0.356); Table II ✔; 67 % at n=1000 ✔; overlap direct 0.18 vs 0.049 ✔ (unlabelled); slopes ✔; slab numbers ✔; check (iv) ✔; 12 ℓ height ✔.

**Bottom line:** no major issue needs new physics; M1 and M3 are writing; M2 a relabel or a few minutes of reruns.
