# Honest review — embedding-3p1-v4 (2026-10-31, session 19)

**What changed:** referee round 3, comments 15–18 (see `answers/answer-embedding-3p1-v4.md`). Text only, plus converged relaxations from s = 0.25/0.75.

**Assessment.**
- The valley claim is now stated at the strength the evidence supports: O(1) differences, no direction, "no barrier was found".
- The relaxations are converged (26–1001 iterations, cap 3000). They make the valley a path of four relaxed points, not one.
- Remaining weaknesses, unchanged from v3:
  - the near-cone wall times are estimates (clearly marked);
  - the slab result rests on 3–4 universes;
  - Johnston's Table IV is not reproduced.
- Risk at PRD: "incremental over Johnston + Casasola". The oracle localisation and the intrinsic start are the answer to that.

**Checked before delivery:**
- abstract numbers vs Table III and `sims/out/r35_analyse_all.txt`, unchanged;
- relaxation numbers vs `sims/out/r39_relax_s_round3.txt`;
- n = 1000 count vs the r35 npz.

One wording error, "more timelike than either map", was caught and corrected before delivery (lesson 51).

**Before submission:** make the repository public (the statement now promises it).
