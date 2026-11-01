# Referee workspace (external referee loop, sessions 17–20)

Snapshot (2026-11-01) of the working files of the separate Claude session that acted as journal referee for both papers.
Its workspace was `~/Desktop/papers/`, one folder per submission track (`3+1 PRD`, `1+1 PRD` — frozen after round 1 —, `1+1 CQG`),
each with `manuscripts/` (writer), `answers/` (writer) and `reviews/` (referee). Roberto carried the files between the two sessions;
the referee never edited a manuscript.

| File | What it is |
|---|---|
| `CLAUDE.md` | The referee session's role, procedure for a round, and rubrics (APS for PRD, IOP for CQG) |
| `REVIEW_MEMORY.md` | Its persistent notes: what it verified, open concerns per round, its own lessons, final advice and odds |
| `history.json` | Every round per track: recommendation, odds, and the status of each numbered comment across rounds |

The reports and answer letters themselves are in `paper/<paper>/reviews/` and `paper/<paper>/answers/` (identical to the Desktop copies,
checked with `cmp` on 2026-11-01). The referee's closing message is `paper/referee-final-2026-10-31.md`. How the loop worked and what it
caught: the methodology note, `paper/methodology-note/`.
