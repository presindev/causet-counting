# Index

Map of the notebook. **Dead ends:** `GRAVEYARD.md`. **What's alive, waiting or unexplored:** `ROADMAP.md`. **Mistakes → rules:** `LESSONS.md`.
History of earlier "next time" notes: the `journal/` entries (session 10 rewrote this file; older notes are in git).

## Ideas
| # | Idea | Status | One-liner |
|---|------|--------|-----------|
| 001 | [Discrete spacetime](ideas/001-discrete-spacetime.md) | exploring | One neighbour per unit rapidity; the age of the universe as IR regulator (Sorkin 2007 had it) caps it at η_max ≈ 142; a finite past keeps Sorkin's 1+1 □ exact (wedge −2 known: Boguñá–Krioukov 2025) |
| 002 | [Expansion as point creation](ideas/002-expanding-universe-point-creation.md) | exploring | A universe that creates its events; cosmic time by counting; classical growth fails the manifold tests |
| 004 | [Positioning vs causal sets](ideas/004-positioning-vs-causal-sets.md) | exploring | Growth memory: per-birth step local in "events between", but a volume law per de Sitter patch (numbers = Sorkin's √N relation; Little's law reading ours). Branch C: F_N exact to N = 12; weak-β drift dies faster than 1/N (prediction N·d ≈ 0.233 confirmed); in the window no stem has converged (2-stem −9 % at N = 12) |
| 005 | [Where is the manifold?](ideas/005-where-is-the-manifold.md) | exploring | 1+1 tools (rectangle identity, depth drift, calibrated embedding test). 3+1: Johnston 2025 reproduced; his error = low-count spacelike pairs; Poisson likelihood of related-pair counts (Casasola 2026) from an intrinsic start removes 79–83 % of it at n = 3000–15000 (cluster r24); slab at equal density +58–65 % (all pairs), the side wall (Pellegrin's mechanism) explains the whole gap to the diamond; N = 800 flag test r27 pending |
| 006 | [Matter as a sum over chains](ideas/006-matter-chain-propagator.md) | exploring | Johnston's chain propagator; Laguerre target ½L_n(μ/2) at fixed n (not found in 99 citers); separates continuum from crystals and grown universes |
| 007 | [Quantum as memory saving](ideas/007-quantum-as-memory-saving.md) | seed | QM as the universe's memory compression (Roberto). At N ≤ 8 phases make records, not savings. Nearest literature: Gisin, Halliwell, co-events, Dowker–Henson collapse lattices, Bousso–Susskind, Banks HST |
| 003 | [Bubbles of space](ideas/003-bubbles-of-space.md) | seed | Space as discrete bubbles, filled or empty; deferred to roadmap B (matter) |

## Papers / checkpoints
- **Split (session 15):** [paper/embedding-3p1-v1.pdf](paper/embedding-3p1-v1.pdf) (3+1, ~90 %, target PRD) and [paper/toolkit-1p1-v1.pdf](paper/toolkit-1p1-v1.pdf)
  (1+1, ~80 %, target CQG), plus [paper/methodology-note-v1.pdf](paper/methodology-note-v1.pdf); final reviews `paper/REVIEW-*-v1-2026-10-29.md`, referee rounds in
  `paper/referee-rounds-2026-10-29/`. These are now the working drafts.
- [paper/counting-full-v2.pdf](paper/counting-full-v2.pdf): combined draft, kept unchanged as the source of the split; was **current** (2026-10-28, session 13; slab, author line, code URL, citations updated session 14; PRD assessment `paper/REVIEW-PRD-2026-10-29.md`). 1+1 counting tools + 3+1 likelihood embedding vs Johnston 2025;
  review `paper/REVIEW-counting-full-v2-2026-10-28.md` (~80 %). F_N / growth memory is NOT in this paper (separate line, idea 004).
- [paper/draft-v6.pdf](paper/draft-v6.pdf): older two-part draft (2026-10-27, session 10); its Part II (growth memory) is the home of F_N. Part I "is it spacetime?" and Part II "what must a growing universe remember?"; Table 2 = what is ours
  after the literature crawl. Review against the arXiv bar: `paper/REVIEW-v6-2026-10-27.md` (Part I ~3–4 sessions from a methods preprint; Part II needs F_N to say something).
- **Methodology case study (future, ROADMAP §9):** turn `paper/methodology-note-v1.tex` into a quantitative case study from the notebook's own record (error provenance, claim history, effort). Not started; after the two physics papers are settled; target: AI-agents-for-physics workshop, April 2027.
- **Public copy:** github.com/presindev/causet-counting (**made PRIVATE 2026-10-30, session 16, by Roberto; make it public again before any arXiv post or submission**: all three drafts say "openly available" there, and the e-mail to Boguñá links it) = snapshot of this notebook, built by `release/make_public.sh --push` after each wrap-up commit (no compute.md;
  cluster named only in the Acknowledgements; README/LICENSE/CITATION.cff live in `release/`).
- `paper/archive/`: v0 ("soup"), v1–v5 and their reviews.

## Waiting computations (details in ROADMAP §1)
- r27 (N = 800 held-out flag test, 1+1 Sec. VII): **job 450475**, 13/28 done at 08:38 on 30 Oct, expected that evening. (F_N N = 12, r25, r28: done.)
- Window question for F_N (β ≈ 7): exact enumeration finished at N = 12; needs sampling or the mean-field model.
- Parallel tempering at N = 400 (code to write).
- Covariant-stem screen test; J₂ fixed-n curvature probe; null-edge ½ vs corner terms.

## Open questions (cross-cutting)
- Normalizable ⟂ boost-invariant: recurring wall (001). Any escape?
- Does unnormalized quantum growth have a stable past (F_N ratios converge)? Does the weak-β phase drift die faster than 1/N?
- Memory per patch is a volume law (C4 forces it, Little's law). Can a quantum state or records per patch be area-law (cf. Banks HST, Bousso–Susskind)?
- QM: memory saver or record maker? What is the screen (what events can see), covariantly?
- Link-graph distance vs entanglement (ER=EPR).

## Roadmap (agreed session 3, status session 10)
1. ~~A1~~ done (variance effect only). 2. **A2** growth with the whole past as state: per-birth step done, memory volume law, F_N in progress.
3. **C8** amplitudes on link choices: only e^{iβΔS} so far. 4. **B** matter in 2D: Johnston propagator done as a probe; source/interactions open.
5. **C1** 3+1 kinematics → **C2** 3+1 gravity (likely beyond us).

## Project constraints (2026-10-25, Roberto + Claude)
C1 discrete spacetime (events + causal order) · C2 no background (no Newtonian space, no aether; relations only) ·
C3 non-locality regulated by the finite size of the universe · C4 local Lorentz invariance for η ≪ η_max ·
C5 a cosmological time/frame computed from the universe's own state (e.g. longest chain to the beginning); usable as a bookkeeping clock for growth, but local laws must not
depend on it (no absolute time); predictions must not depend on which relational clock is used (height vs past-volume); should coincide with matter/CMB frame ·
C6 Newton + Einstein from far away · C7 creation (and maybe destruction) of events drives expansion, possibly via quantum operators · C8 links between events are quantum.
Missing so far: matter (what sources gravity?).

## Next time
- Latest journal: `journal/2026-10-30-session16-fetch-fn12-r28-r34.md`. 3+1 draft has no placeholders left.
- **Fetch r27** (job 450475; command in compute.md, Session 16) → fill the 1+1 Sec. VII `\pending`. If the flag misclassifies at N = 800, the claim changes, not just the number. Then commit + `release/make_public.sh --push` (Roberto runs it: the push is blocked for Claude).
- Roberto: read the two drafts + note; removal candidates (session 15 journal); language pass; Boguñá (the repo link in his e-mail is now a 404: repo is private).
- **Before any submission: make github.com/presindev/causet-counting public again.**
- Later: F_N window (sampling / mean-field); methodology case study (ROADMAP §9), April 2027 workshop; gravity / rung-3 discussion still deferred.
