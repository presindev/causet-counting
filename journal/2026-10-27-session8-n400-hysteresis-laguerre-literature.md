# Session 8 — 2026-10-27

A cluster-and-library session: check the cluster jobs, analyse N = 400, prepare the F_N test at N = 11, and run a literature review in parallel.

## What we did
- **N = 400 hot/cold (idea 005)** `[ours]`. 31 of 80 tasks had died of TIMEOUT. That's the 20 known from session 7 plus 38–46, 48, 49, which were still on the
  old 6 h limit. `sims/n400_analyse.py` now combines final results, partial checkpoints and the log lines of dead tasks (a "sources" column shows which).
  - **Result:** hysteresis from β = 0.08 to at least 0.7, so hot and cold starts never meet. Cold crystals melt at β ≤ 0.05; hot starts leave the continuum only
    at β ≥ 0.45, and then stick in a ~10-layer, r ≈ 0.7 state. So β_c(400) is only bracketed, 0.05 < β_c < 0.45 (35/N ≈ 0.09 sits inside).
  - The cold crystal thins with β: 5 → 3 → 2 layers at β = 0.08 / 0.12 / ≥ 0.2. This corrects session 7's "3–7 layers". The 2-layer order has by far the lowest
    action (S/N ≈ −34 vs −12), so it is very likely the large-β ground state.
  - β = 0.12 hot is log-only. The 11 decisive lost tasks were resubmitted (job 449800).
- **Literature review** (subagent, 13 full texts; key formulas re-checked numerically):
  - The Laguerre target ½L_n(μ/2): its pieces are known (C(n,k)/k! increasing subsequences, Pinsky / Lifschitz–Pittel; the Laguerre identity), but the
    assembled statement was not found in causal-set papers (INSPIRE not searched). Its Poisson average is exactly Johnston's ½J₀(mτ), so ours is the finer,
    density-free statement. Better large-n form: e^{μ/4}J₀(√(2μ(n+½))).
  - Curved 2D (Nomaan X–Dowker–Surya 2017) adds (Rτ²/48)J₂: a candidate curvature probe at fixed n.
  - Vertex idea (chain sums meeting at an element): Johnston's thesis §5.4.2 considered and set it aside as ambiguous.
  - F_N: nobody computes it; sum-rule growth models make F_N = 1 by construction. Surya–Zalel Thm 3.1 (phase alignment ⇒ the measure extends) resembles our
    2-stem phase locking.
  - Entanglement entropy on causal sets: volume law without truncation, area law with it (Sorkin–Yazdi). It parallels our volume-law memory, but in scaling only.
- **F_N at N = 11 (idea 004):** `a2_future_factor.py` now also takes stems of size 4 and saves an `.npz`. The N = 9 test passed on the cluster after copying two missing
  modules; it ran up to ~60× slower than the laptop, so the N = 11 job (449812) asks 24 h.

## Mistakes (now in LESSONS)
- Lesson 23: didn't ship the full import tree to cluster, and sized the F_N job with another code's speed factor.

## Open / next
- Fetch job 449800 (N = 400, β = 0.08–0.2) and job 449812 (F_N to N = 11, stems 2–4); rerun `n400_analyse.py --logs`; read the F_N ratios for sizes 2–4.
- β_c(400) needs a barrier-crossing method (parallel tempering in β) if we still care about it.
- Possible next thinking topics: the J₂ curvature probe at fixed n (flat Laguerre target vs curved 2D); the quantum memory question.
- Before any draft claims about F_N or the Laguerre target: INSPIRE citation crawl (Surya–Zalel, DJS, Johnston 2008).
