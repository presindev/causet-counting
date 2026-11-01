# Honest review — embedding-3p1-v5 (2026-10-31, session 20)

**What changed:** referee round 4 (accept), comments 19–21 (see `answers/answer-embedding-3p1-v5.md`). Text only; no new runs.

**Assessment.**
- The sign-count sentence now gives the right reason: the margins are of the same order as the continuation gain, and the two fits were not continued equally. The old reason, "no larger than", was false at n = 3000.
- The "within O(1) of both ends" claim is now backed against both ends. The intrinsic-end ranges come from `sims/out/r39_relax_s_round3.txt`. No directional reading was added, although every n = 6000 relaxation lies above the intrinsic fit.
- The abstract no longer claims a slow abundance trend that the body contradicts (50 % → 31 % ≈ n^−0.7). It now states the error claim of Sec. IV.
- Submission blockers:
  - the repository must be public before upload, because Data availability and Ref. [32] are now in the present tense;
  - the optional Zenodo DOI is a red placeholder (delete the clause if no DOI).
- Remaining weaknesses, unchanged from v4:
  - the near-cone wall times are estimates;
  - the slab result rests on 3–4 universes;
  - Johnston's Table IV is not reproduced.
