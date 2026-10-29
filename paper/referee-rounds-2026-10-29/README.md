# Referee rounds on the split drafts (session 15, 2026-10-29)

`counting-full-v2.tex` was split into `toolkit-1p1-v1.tex` (1+1) and `embedding-3p1-v1.tex` (3+1), plus `methodology-note-v1.tex`.
Each round: separate instances of the same AI system (Claude Opus 5.5) acted as PRD referees. They saw the drafts, the data files and a prompt
written by the authoring instance (which pointed at files and checks; the reviews were therefore not blind), not the author's reasoning.
Then the authoring instance revised. The reports are kept here verbatim in substance (lightly formatted).

| Round | Files | Verdicts | Runs triggered |
|---|---|---|---|
| 1 | `round1-3p1.md`, `round1-1p1.md` | major / major | r30 (low-count oracle on Johnston's detours), r29 (per-pair errors), r31 (1+1 baselines), r32 (Laguerre vs related fraction) |
| 2–3 | `round3-3p1.md`, `round3-1p1-note.md` | minor / minor | r30 on seed 2029 (pairing with r18), r29 on Table II seeds, r33 (position vs time/scale) |
| 4 | `round4-all.md` | minor / minor; plateau reached | r34 (lnL of truth-started optimum; causal fidelity) |

Final reviews: `../REVIEW-embedding-3p1-v1-2026-10-29.md`, `../REVIEW-toolkit-1p1-v1-2026-10-29.md`.
