# paper/ — map

| Folder / file | What it is |
|---|---|
| `embedding-3p1/` | 3+1 paper (likelihood embedding vs Johnston 2025), `embedding-3p1-v1.tex/.pdf`; target PRD |
| `toolkit-1p1/` | 1+1 paper (counting tools, manifold flag), `toolkit-1p1-v1.tex/.pdf`; target CQG |
| `methodology-note/` | How the work was done with an AI colleague, `methodology-note-v1.tex/.pdf` |
| `*/reviews/` | Every review and referee report of that paper (our final review, the session-15 referee rounds, and new reports from the referee session) |
| `referee-workspace/` | Snapshot of the external referee session's working files (role/procedure, persistent memory, `history.json` of every comment across rounds), sessions 17–20 |
| `referee-rounds-2026-10-29/` | Session-15 referee loop: its README and round 4, which covered all three drafts at once |
| `figs/` | Figures shared by all drafts (`\graphicspath{{../figs/}}`); made by `sims/fig_part1.py`, `sims/fig_3p1.py` |
| `counting-full-v2.tex/.pdf` | Combined draft the split came from. Kept here, not in `archive/`, because the Boguñá e-mail (29 Oct) points to `paper/counting-full-v2.pdf` |
| `archive/` | Every earlier draft with its review (v0–v6, counting-1p1-v1, counting-full-v1, the v2 reviews) |

Compile from inside the paper's folder: `cd paper/embedding-3p1 && tectonic -X compile embedding-3p1-v1.tex`.
New referee reports: `paper/<paper>/reviews/`, named `referee-YYYY-MM-DD-<round or topic>.md`.

Current versions (session 21, 2026-11-01): `embedding-3p1-v6` (PRD, language pass), `toolkit-1p1-v6` (CQG, IOP `iopart` class, shipped next to the source; language pass), `methodology-note-v3` (v2 added the external referee iteration; v3 the final preparation). Final reading of both papers: `final-reading-2026-11-01.md`.
