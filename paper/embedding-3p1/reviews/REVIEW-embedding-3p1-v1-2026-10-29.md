# Final review: embedding-3p1-v1 (3+1 paper), 2026-10-29 (session 15)

Bar: a Physical Review D submission. Source `paper/embedding-3p1-v1.tex` (split from `counting-full-v2.tex`, which is kept unchanged).
Four referee rounds (separate instances of the same model; reports in `paper/referee-rounds-2026-10-29/`): major → minor → minor → minor, plateau reached.

**Completion: ~90 %. Target journal: Phys. Rev. D.** Both the benchmark (Johnston 2025) and the overlap construction (Boguñá–Krioukov 2024) are PRD
papers, and this is a direct head-to-head improvement on the former; the referee rounds agreed on PRD.

## What the paper now says
Johnston's 2025 embedding reproduced → its residual error is all spacelike pairs (oracle) and 94–97 % low-count pairs (k < 10; oracle on his own
detours, r30) → inverted distances improve slowly (scaling argument, Fig. 1) → fit the spatial coordinates to all related-pair interval counts
(Casasola's likelihood, credited) from an intrinsic start → **79–83 % of his residual removed at n = 3000–15000, every one of 20 universes**; at n = 3000
the median spatial-distance error halves (0.22 → 0.11 ℓ) and the 90th percentile drops 0.80 → 0.28 ℓ (r29); causal fidelity improves (0.65–0.69 % of
pairs misclassified vs 1.6–2.1 %, r34); slab at equal density 58–65 %, the timelike boundary sufficient to explain the gap.

## Strengths
- One storyline; every abandoned approach in App. A, deletable (only one pointer sentence in the Intro goes with it).
- Paired comparisons throughout, universe sets labelled; numbers verified against source files by the referees (Table II, r29, r30, r33, slopes, slab).
- Honest credit: likelihood = Casasola; overlap = BK24; ML coordinates standard elsewhere.
- Per-pair, per-element and causal-fidelity metrics added, so the 80 % is physically readable.

## What a PRD referee may still push on
1. **"Ours" is narrow**: diagnosis + intrinsic start + benchmark; the likelihood is someone else's (Research Square preprint, not peer-reviewed). Argued in
   Sec. V; Casasola never compared with Johnston and started from the truth.
2. **Position rms improves less than distances** (0.67 → 0.52 ℓ at n = 3000): dominated by the tenth of elements with fewest related partners; the
   truth-started optimum has higher lnL, so it is the start, not the likelihood (r33, r34). Stated plainly; a better start is an obvious follow-up.
3. **Flat diamond only; time coordinate not refitted; flat interval volume** (Limitations). A curved (de Sitter) 3+1 test would strengthen it
   (cluster work, a few sessions) — not required for a methods paper but likely requested.
4. **Small universe counts** at each n (2–8). Error bars are honest; more universes on the cluster would be cheap.
5. Two non-arXiv references (Casasola, Pellegrin).

## Before submission (checklist)
- [ ] r28 clean timing → Sec. VII (the only `\pending`; job 450476 running). If the timings are thin, fold Sec. VII into the Discussion.
- [ ] r34 at n = 6000 → causal-fidelity sentence (`\pending` inside it; laptop run finishing).
- [ ] Strip the `.tex` header comments (session notes) before arXiv.
- [ ] Verify HMM25 (J. Math. Phys. 66 (2025) with arXiv:2601.03280: recorded as checked in `literature.md`, session 13) and Madsen arXiv:2610.36695
      (verified session 12) once more at submission time.
- [ ] Roberto's language pass; Boguñá's reply (if he comments on the 3+1 part, fold in).
- [ ] Decide whether App. A stays (referees found it acceptable; delete with the one Intro sentence if a referee asks).
- [ ] Bibliography to BibTeX/apsrev4-2 (now a manual `thebibliography`; formatting is APS-like but not generated).

## What is ours (search depth unchanged from the combined draft; see its review)
Tabulated unequal-depth overlap inversion; reproduction + oracle analysis of Johnston 2025 with the low-count localisation; the scaling argument; the
intrinsic start; the large-n comparison, per-pair/per-element/causal metrics; the slab analysis (wall mechanism is Pellegrin's).
