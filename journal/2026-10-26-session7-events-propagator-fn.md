# Session 7 — 2026-10-26

## What we did
- **What is an event? (Roberto, new idea 006.)** An element is a Planck-volume atom of spacetime, not a lab event: a fm-scale collision spans
  ~10⁷⁹ elements. Particles are excitations living on the elements, not the elements themselves. Classical free particle = longest chain
  (Brightwell–Gregory 1991) `[literature]`; quantum particle = sum over all chains (Johnston 2008) `[literature]`. ψ as "the memory" = the standard
  notion of state (a sufficient summary of the past for predicting the future) `[established]`; for us it restates the quantum-memory / factorization question.
- **Johnston's propagator** (`sims/b_johnston_propagator.py`): K = Φ(I − bΦ)⁻¹, a = ½, b = −m²/ρ in 1+1; reproduces ½J₀(mτ) on sprinklings.
  New `[ours]`: K depends only on μ = m²/ρ; in a random 2D order E[K | n] = ½Lₙ(μ/2) exactly (Laguerre), with n = interval size, so no fit is needed;
  at order μ² the test is the Myrheim–Meyer dimension.
  - N = 400 MCMC universes (`sims/b_johnston_n400.py`): continuum-like ones match the random controls; crystals fail (no oscillation / far too many chains).
  - S1 percolation (`sims/b_johnston_grown.py`, N = 1500): all fail 2D; p = 0.02 runs away (|K| up to 10). A2 is untestable at N ≤ 8.
- **F_N factorization test (branch C, idea 004, Test 4)** (`sims/a2_future_factor.py`, exact to N = 10 by memoizing unlabelled posets):
  β = 0 ratio is exactly 3/(N+1) → 0 (KR wins). Inside the window, the 2-element stem's ratio locks its phase near π by N ≈ 8–10 with ~10 % drift;
  3-element stems still move 20–50 %. **Inconclusive.** Genetic algorithms discussed and set aside: F_N is an oscillating sum (sign problem);
  a genetic search could only find stationary-phase configurations.
- **N = 400 on the cluster:** 20 of 38 tasks hit TIMEOUT (6 h limit, nodes 1.1–2.6 s/sweep under load) and lost everything (save only at the end).
  Fixed: periodic `.partial.npz` checkpoints and a 14 h limit; tasks 50–79 resubmitted by Roberto (`%6`). Preliminary physics from completed runs + logs:
  **hysteresis at β = 0.08 and 0.12** (hot stays continuum, cold stays crystal); cold crystals melt at β ≤ 0.05; the surviving crystal has 3–7 layers, not 2.

## Mistakes (now in LESSONS)
- Sized the cluster job from a quiet-node timing and saved results only at the end (lesson 22).

## Open / next
- N = 400: fetch the resubmitted tasks (β = 0.2–0.7) and the logs of the running 38–49; run `sims/n400_analyse.py` (extend it to read log lines for the lost tasks).
- F_N at N = 11 on the cluster (single task, ~2.7 M states); N = 12 needs a faster poset generator.
- Propagator: a test beyond 2D needs Johnston's link-based version (3+1) and its own target. Is the Laguerre result known? (not searched)
- Fold sessions 6–7 into draft v5 once branch C or N = 400 has a result.
