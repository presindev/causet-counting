# Review — methodology-note-v2 (2026-11-01, session 21)

Honest review by the authoring instance (not independent; the note has never had an external referee of its own).

**What v2 adds over v1.** Sessions 16–20 (timeline to 31 Oct, twenty sessions); a new section "External referee iteration" (setup of the separate
referee session, the per-track folders, rubrics, its notes file and history.json, how files moved between sessions, four rounds + closing check,
Table 3 with recommendations and comment counts from `paper/referee-workspace/history.json`, what the referee caught, corrections in the other
direction, what changed in the papers, lessons 44–51, limits); mistake log 41 → 53 entries with a "since 29 Oct" column; verification rules extended
(pooled ratios, position-based selection, converged optimizers, benchmark every cited competitor, numbers from files); companion titles updated;
Availability points to `paper/<paper>/reviews/`, `answers/`, `paper/referee-workspace/`, the final message.

**Checked against the files.** Comment counts and statuses (history.json: 3+1 14/7/4/3 new, 27 resolved + 1 declined; CQG 14/10/7/5 new, 32 resolved,
m6 n/a, m7 deferred, m14 partial → 21, m24 declined; closing_check resolves m19–21 and m25–29); recommendations per round; shaded odds
(final_assessment); lesson counts (51 numbered + 10b, 11b = 53; 40–51 new); FRW wording "prediction falls short by 26–35 %" matches the 1+1 v5 text;
"median falls 33–40 %" from REVIEW_MEMORY; 82 scripts / ~8000 lines from `sims/*.py`.

**Weak points.**
- The mistake-table classification is mine and coarse (e.g. lesson 50 could be "process"). Stated as such in the caption.
- "For six of the eight, the referee pointed out the error or requested the test that exposed it" is a judgement from the journals; lesson 47 is mixed
  (the referee asked for the path scan; the 300-iteration cap was noticed by the writer, then the referee asked for convergence in round 3).
- The note still contains no measurement (time per round, tokens, human hours). The quantitative case study is ROADMAP §9.
- Availability says the notebook "is public": true only after Roberto makes the repo public (same as the papers' present tense).
- `paper/referee-workspace/` is cited but must actually be copied into the repo (the main session's job); `REVIEW_MEMORY.md` there contains the author's
  e-mail address and the referee's frank odds — Roberto should be fine with publishing both.
- 1+1 comment m7 (IOP style) is described as "deferred to the final version"; if the IOP version is done before release, the sentence can stay.

**Verdict.** Fit for the public repo alongside the papers. 8 pages (v1: 4). Title unchanged, so the papers' [MethodNote] entry stays valid.
