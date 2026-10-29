# Session 15 — 2026-10-29 (evening): split into two PRD-style papers + methodology note, four referee rounds

## What we discussed and did
- **Cluster status (20:48):** F_N 449963 at 52 h, 113 GB of ~115 (finish expected within hours, 72 h limit at ~16:40 on 30 Oct); r27 first wave on cn02
  (tasks 11–13 done in ~9.7 h, ~17 s/sweep; second wave ends ~midday 30 Oct); r28 on exclusive cn03 (n = 3000 / 6000 / 10000 in 0:06 / 0:33 / 1:40;
  15000 running, ~4 h total, far below the 10.5 h loaded-node estimate). Not fetched yet.
- **Split (Roberto's decision, following the PRD assessment):** `paper/toolkit-1p1-v1.tex` (1+1), `paper/embedding-3p1-v1.tex` (3+1), both RevTeX/PRD
  register; `paper/methodology-note-v1.tex` (the old "How this work was done", expanded; both papers cite it from the acknowledgments). Failed attempts
  only in App. A. `counting-full-v2.tex` untouched.
- **/loop, author vs referee, four rounds** (referees = separate instances of the same model; reports in `paper/referee-rounds-2026-10-29/`):
  major/major → minor/minor → minor/minor → plateau. Runs triggered by referees (all laptop):
  - **r30** — low-count oracle on Johnston's OWN detours (the paper's claim had only been shown for our overlap estimator): truth on k < 10 pairs
    removes 97 % (n = 1500) / 94 % (n = 3000, seed 2029 = r18's universes) of his residual; truth on all other pairs 3–4 %. Claim holds.
  - **r29** — per-pair errors on the Table II universes (`sims/out/r29_tableII/`): median spatial-distance error 0.22 → 0.11 ℓ, q90 0.80 → 0.28 ℓ at n = 3000.
  - **r33** — positions improve less (rms 0.67 → 0.52 ℓ): not time (Johnston's t is good to 0.07 ℓ), not scale/affine; a tenth of elements with few
    related partners (rms ~1.5 ℓ) dominate; median per element 0.16 ℓ vs 0.24–0.30 ℓ.
  - **r34** — truth-started optimum has higher lnL (+105–109 at n = 3000, +549 at 6000) ⇒ the residual is the start's local optimum, not the likelihood;
    causal fidelity: fit misclassifies 0.65–0.69 % of pairs (n = 3000), 0.49 % (n = 6000, 1 universe) vs Johnston 1.6–2.1 % / 1.29 %.
  - **r31** — 1+1 baselines on the same mid-diamond pairs: the rectangle estimator is unbiased for d² above 2ℓ and beats BK's equal-depth filter and the
    Brightwell–Gregory / Rideout–Wallden past–future interval (biased high +14–86 %).
  - **r32** — Laguerre statistic vs fixed-n related fraction: as a phase diagnostic the propagator target is NOT stronger than its first term; it misses one
    4-layer crystal. 1+1 paper reframed and retitled accordingly.
- **Final reviews:** 3+1 ~90 %, target **PRD**; 1+1 ~80 %, target **CQG** (PRD possible). Files `paper/REVIEW-*-v1-2026-10-29.md`.
- **Methodology note:** mistake-log table (41 entries in five groups), honest description of the referee loop (same model, prompted by the authoring
  instance, not blind). Venue if posted: arXiv cs.CY + cs.AI (needs an endorser). **Future task (ROADMAP §9):** a quantitative case study from the
  notebook's record, after the two papers are settled; target an AI-agents-for-physics workshop in April 2027.

## Decisions (Roberto)
- Split into 1+1 and 3+1 papers; AI methodology out of the papers into a note in the public repo, cited by both.
- Laptop runs < 1 h allowed in the loop; r27/r28 as placeholders. Journal for 1+1 decided by the final review (CQG recommended).
- **Don't delete files**; rerun into new folders; removal candidates are listed for him (memory saved).
- Case study after the two papers, aimed at the April 2027 workshop.

## Mistakes
- Lesson 40: claimed a property of Johnston's method from an oracle run on our own estimator (r18); referee caught it, r30 fixed it.
- Lesson 41: Procrustes without reflections charged a mirror-image map ~4 ℓ; caught because the result contradicted the distance errors.
- Lesson 42: wrote a normalization ("in units of the trace of |G|") and swapped two oracle percentages from memory/grep order; check against the file.
- zsh word-splitting slip again (`for job in "1500 1000"`; same as session 14); runs now go through `bash -c`. Tried to `rm` old outputs before a rerun;
  Roberto stopped it (memory: no deleting files).

## Next (session 16 — the laptop was switched off tonight)
1. **Re-run the interrupted r34 universe**: `cd sims && ../.venv/bin/python -u r34_lnl_causal_fidelity.py 6000 1002 | tee -a out/r34_lnl_causal_fidelity.txt`
   (~20 min; check first whether the file already has the n = 6000 seed 1002 block), then fill the `\pending` in the 3+1 causal-fidelity sentence.
2. Fetch F_N, r27, r28 (compute.md, "Fetch + analyse" under r27/r28): r27 → 1+1 Sec. VII `\pending`; r28 → 3+1 Sec. VII `\pending`; F_N → idea 004 (N·d ≈ 0.233).
3. Roberto: read both drafts and the note; decide on the removable-files list (below); language pass; Boguñá's reply.
4. After the wrap-up commit: `release/make_public.sh --push`.
Removal candidates (not deleted): `sims/out/r29/` (first r29 run, wrong seeds, superseded by `r29_tableII/`); `sims/out/r30_n3000.txt` (seed 2028, superseded by
the seed-2029 pairing); `paper/figs/fig_3p1.*` (old two-panel figure, still used by counting-full-v2 — keep while v2 exists).
