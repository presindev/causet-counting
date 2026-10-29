# Session 14 — 2026-10-29: equal-density slab, paper items, public notebook, last literature checks, Boguñá e-mail

## What we discussed and did
- **r25 fetched (slab vs diamond at equal density).** Poisson fit removes 58 / 65 % of Johnston's residual in the slab (n = 6000 / 12000) vs 75 / 80 % in the diamond
  (1500 / 3000, density-matched); the oracle wall correction brings the slab to 80 / 86 %: at equal density the side wall explains the whole gap (the other half of the
  session-13 gap was density). Wall cost ~20 points at every n (clipped share fixed by the shape). Caveats: shares of a ~10× smaller residual; slab fails at n = 600 (1 universe).
  Sec. 9.3, abstract, limitations rewritten. Diamond rows reproduce r24.
- **Roberto's paper items done:** author line (SapereIA and ICCUB, Barcelona; roberto@sapereia.com), AI statement kept, no endorser needed (gr-qc author).
- **Public notebook + code:** github.com/presindev/causet-counting. The paper promised "the full notebook"; I first offered "sims/ only" (lesson 39). Snapshot without
  compute.md; the cluster is named only in the Acknowledgements (Roberto); history restarted once (force-push by Roberto). `release/make_public.sh` builds and checks it;
  README, LICENSE (MIT code, CC BY 4.0 notes), CITATION.cff and a how-to-cite section live in `release/`. Notebook renames: `sims/cluster/` → `sims/cluster/`, `*_cluster_*` → `*_cluster_*`.
- **Literature:** (1) 3+1 unequal-depth inversion: BK24 re-read (exact inversion only at equal depth, Eq. 22; causal-set filters keep only equal-depth c, Eqs. 32–34);
  7 INSPIRE citers + Rideout–Wallden + MG17 abstract: nothing; quote added. (2) Google Scholar citer lists (pasted by Roberto) for Johnston25, BK24, Clough–Evans,
  Casasola, Johnston08 ("Laguerre"): nothing anticipates our claims. Added citations: Johnston 2022 (missing predecessor), Cunningham 2018 (1+1 boundary inference, in the
  Outlook as an untested route to an intrinsic wall correction).
- **Cluster:** F_N 449963 at ~92 GB of ~115 at 08:34 (finish expected tonight; the `-P` MaxRSS reading was truncated, not a drop). Submitted r27 (N = 800 held-out test of
  the layered flag; threshold fixed beforehand on the laptop: z > 0.120) and r28 (clean timing on exclusive nodes); jobs 450475, 450476 after tests 450473, 450474.
- **Boguñá e-mail sent** (Spanish, by Roberto; record in `correspondence/`, private). Told him: language pass pending, arXiv then maybe PRD.
- **PRD assessment** (`paper/REVIEW-PRD-2026-10-29.md`): 3+1 half could be PRD after refocusing + per-pair error in discreteness lengths + one curved test + method
  section to an appendix; or CQG now with the toolbox. Decide after Boguñá's reply.

## Decisions (Roberto)
- Publish the whole notebook as a snapshot (incl. the growth-memory line), without compute.md; cluster named only in the Acknowledgements.
- Code GitHub without DOI. Wait for Boguñá before choosing the journal.

## Mistakes
- Lesson 39: offered a release option that contradicted the paper's own Availability promise.
- Two shell slips caught in-session: zsh does not word-split `$files` (sed never ran); `grep -c` returning 1 on zero matches stopped an `&&` chain (an edit silently not applied;
  noticed via `git status`). Also a pipefail exit in the release script on a no-match grep (fixed).

## Next
1. Fetch F_N, r27, r28 (compute.md, "Fetch + analyse" under r27/r28); r27 → Sec. 5 (N = 800 flag), r28 → Sec. 9.5 cost; F_N: test N·d ≈ 0.233 (idea 004).
2. Boguñá's reply → corrections; then journal choice (PRD route or CQG).
3. Roberto's language pass; arXiv. After every wrap-up commit: `release/make_public.sh --push`.
