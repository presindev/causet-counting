# Roadmap (session 10, 2026-10-27)

What is alive, what is waiting, and what nobody has looked at. Dead things live in `GRAVEYARD.md`. Status of each idea: `INDEX.md`.
Effort: S = an afternoon on the laptop; M = a session plus a cluster job; L = several sessions or beyond our tools.

## 1. Computations waiting or ready to launch

| What | Where | Status | Effort |
|---|---|---|---|
| F_N at N = 12 (stems 2–4) | cluster, `sims/cluster/fn_job.sh` with NMAX=12 | **Job 449963** (resubmit of 449948 after the lookup-table fix; --mem=200G). Prediction to test: weak-β 2-stem N·d ≈ 0.233 at N = 12 (idea 004, test 4c). N = 11 took 47 min and 6.1 GB on cn12 with 2.77 M states. A000112(12) = 4.9 × 10⁷ states, so expect ~110 GB and ~15–25 h. Needs `--mem=160G`, `--time=48:00:00`, and a fat node (cn01 or any 2 TB node). | M |
| r25: slab vs diamond at EQUAL density, Poisson likelihood (idea 005) | cluster, `sims/cluster/r25_job.sh` | **Jobs 450431 (test) → 450432–450435** (diamond 1500/3000, slab 6000/12000, 4 univ. each; submitted session 13). Fills the slab placeholder in `paper/counting-full-v2.tex` Sec. 9.3 | S |
| Parallel tempering at N = 400 to locate β_c | cluster, new code | Needed: the cold chains are frozen (acceptance ≤ 0.001), so plain Metropolis can't cross. Literature fit β_c ≈ 1.66/(ε²N) = 0.094 is the target to confirm or refute. | M |
| Screen test with covariant stems and a fixed per-event view budget; records per patch vs births | laptop N ≤ 9, then cluster | Designed in session 9, not run | M |
| ~~J₂ curvature probe at fixed n~~ | laptop | **Done (session 10):** K at fixed n is no more sensitive than the related-pair share c₂ (g₂ ≈ 0.027 (Hτ)²); dropped as a claim (GRAVEYARD D8) | — |
| ~~Detector blind spot for ~10-layer states~~ | laptop | **Done (session 11):** zero-length share flags layering (held-out N = 200 test passed); `sims/r8_detector_spread.py` | — |
| Part I note `paper/counting-1p1-v1.tex`: detector at N = 800; code/data release | cluster + repo | Reruns and FRW check done (session 11) | S–M |
| ~~Part I figures~~ | laptop | **Done (session 11):** `sims/fig_part1.py` → `paper/figs/` | — |
| ~~Null-edge ½ vs Buck–Dowker–Jubb–Surya~~ | — | **Done (session 10):** per-event form of their corner result; claim given back (GRAVEYARD) | — |

Already fetched and analysed (session 10): cluster 449800 (N = 400 tail, all 11 tasks complete) and 449812 (F_N, N = 11).

## 2. Promising lines (ours, alive)

1. **Future-factor criterion (branch C).** Not found in the literature: every quantum growth model imposes a sum rule, which makes F_N = 1. At N = 11:
   - inside the window (β = 7), the 2-element stem's ratio relative to counting converges to ≈ 1.87∠π (N = 9–11: 1.91, 1.89, 1.86);
   - 3- and 4-element stems are still moving;
   - at weak β every stem's phase drifts by ≈ 0.008π·β per relation in the stem, per added event, slowly slowing.

   This is the most original thread we have. N = 12 is the next data point; an analytic model of the drift would be better.
2. **Laguerre target for Johnston's propagator.** Survived the full INSPIRE crawl (99 citers, full text). Small, clean and checkable. With the J₂ term it could become a short note.
3. **Depth-drift curvature and the rectangle identity.** Not found; elementary. The open problem in the literature (Surya review §4.3: there is no robust spatial distance in d > 2) is exactly where it would matter, and our identity is 1+1 only. Value: pedagogical, plus a curvature estimator in 2D.
4. **Memory as residence time (Little's law), and "finite memory iff no event horizon".** The number is Sorkin's (√N relation), the mechanism reading isn't. It links to Bousso's N-bound and Banks' holographic space-time.
5. **Calibrated detector statistics (w₂, r±, stress vs N).** It now has to be framed as a calibration of Clough–Evans, not as a new detector.

## 3. Genuine new ideas worth a calculation (not yet tried)

- **N1. ~~The phase-drift rate as an observable.~~ Done (session 10):** to first order the drift is β × the mean future action change; d_N ∝ N^{−a} with a ≈ 1 at ε = 0.21 (N ≤ 10,
  pre-asymptotic) and a = 1.5–3.3 for ε ≥ 0.35 ⇒ the weak-β drift is likely not fatal. Original note: If each relation in a stem shifts later births' ΔS by a fixed amount, then F_N(X) ≈ e^{iβ·c·rel(X)·N}·(…), and the past is stable only if all stems answering one question share the drift. Write the mean-field version: the expected ΔS shift from one extra relation, as a function of N and ε. Effort S.
- **N2. Collapse or co-event dynamics on a *sprinkled or grown* causal set.** Dowker–Henson and Dowker–Herbauts did it on a regular 1+1 null lattice. Nobody has done it on a random causal set, or counted records per region. This is the concrete test of idea 007 ("memory = number of records per patch; area or volume?"). Effort M–L.
- **N3. Bridge to holographic space-time.** Banks: log dim H = A/4 per causal diamond; Bousso–Susskind: decoherence is never exact in a finite diamond, which is our "never exactly decohered" result in spirit. Question: can our past/future matrix B per causal diamond have rank ~ e^{area} when the screen is the diamond's boundary? Effort M (conceptual first).
- **N4. Compact space as the physical regulator.** Boguñá–Krioukov (Oct 2026) propose compact hyperbolic quotients as boundary-free regulators of link observables. Our C3 says the same thing physically. Check Sorkin's □ in a sprinkled cylinder (closed space, finite age) against the diamond result; we already have cylinder code from session 5. Effort S.
- **N5. Computational mechanics of classical sequential growth.** The tools exist (Gu et al.; Yang et al. 1803.08220 MPS = optimal quantum model). Compute the statistical complexity C_μ of transitive percolation vs N. A clean, checkable, publishable-sized calculation outside our quantum speculation. Effort S–M.

## 4. Unexplored, by us
- **3+1 versions of the Part I tools** (assessed session 11, ranked by doability):
  1. ~~Fixed-$n$ propagator target~~ **Tried session 11:** in 3+1 hops go along links, so no closed form; $E[P_2|n]\to3\pi$ reproduces the continuum mass term $m^2/8\pi$
     (MC confirms). A 3+1 target would be a computed table $T(n,\nu)$. Recorded in idea 006 and the note's outlook; not pursued further for now.
  2.+4. **Tried session 11 (idea 005):** 3+1 distance from past sizes: 1–2 % per pair at large N. Johnston 2025 reproduced (Tables III, V). Oracle: spacelike pairs are his
     whole bottleneck. Ours beats him per pair at short/medium range but not after embedding on his benchmark (far pairs near the waist). Next, if pursued: likelihood embedding.
     **Update:** a switch (ours for close pairs, his detours for far) beats him after embedding, held out (+0.007 … +0.021, n = 500–3000). Next: cluster at larger n,
     a cheaper far-pair estimate to keep the speed (ours 3 s vs his 76 s at n = 4000), the Boguñá email. Likelihood embedding stays as the principled follow-up.
     **Update 2 (end of session 11):** cluster n = 6000: switch +0.0049 (20 % of his residual; relative gain grows with n). Counts-only map (c) (SMACOF on related +
     shared-past distances, far pairs weight 0.1, no detours) matches/edges him, held out. Random stepping stones killed; two-pass stones keep ~2/3 of the gain.
     Waiting: r14/r17 at n = 10000–15000. Then: write the 3+1 section (reproduction, oracle, switch, counts-only map, timing).
  3. Depth-drift curvature (L): curvature expansion of lens volumes in Riemann normal coordinates; involves $R$ and $R_{ab}t^at^b$ (as in RSS13). Large sprinklings (cluster).
  4. Embedding test: follows once (2) exists; the zero share carries over.
- Matter as a *source* (backreaction), interactions (Johnston set vertices aside).
- C5 test: matter frame = cosmic frame.
- Idea 003 (bubbles) beyond translation.
- Idea 002 stage 3: amplitudes on link choices (C8) in growth, beyond e^{iβΔS}.

## 5. Unexplored, by the literature (as stated by its authors)
- "The space of quantum sequential growth models is largely unexplored"; the truncated decoherence functional is "an unexplored direction" (Surya, Living Review §6.4). Our F_N lives here.
- No robust spatial distance for d > 2; distances are only "predistances" (Surya §4.3).
- Whether the region near the past light cone contributes to the d'Alembertian in general curved spacetimes (Surya §4.5). Our finite-past calculation touches this.
- Boundary-free regulators (compact hyperbolic quotients) for link observables (Boguñá–Krioukov 2610.03247).
- Matter on 2D orders; exiting the non-manifold phase (Glaser review 2306.09904 §4).
- Collapse or co-event dynamics on random causal sets; records per region vs area (agents' search, session 10).
- Memory and residence time of covariant growth vs the N-bound (agents' search).

## 5. Paper 2 (agreed 2026-10-28, Roberto)
Future work deliberately kept out of the first paper (counting-full). **Not to be confused with the growth-memory line (idea 004, F_N, old draft-v6 Part II),
which is a separate paper/note and does not block counting-full (session 13).**
- **Periodic space** (time × 3-torus): no spatial edges at all, hence no waist pairs; C3 in spirit (finite universe as regulator; N4, Boguñá–Krioukov compact quotients).
  Needs torus overlap tables and a torus-aware embedding (MDS into flat R³ fails). 2+ sessions.
- **Curved backgrounds** (de Sitter, FRW): curved overlap tables, or Madsen-style localization to small charts where flat tables hold to O(ℓ²); our 1+1 depth drift as the
  curvature probe; possibly a 3+1 depth drift.
- ~~Full likelihood embedding~~ (in paper 1 since v2). Joint time + space fit; curved interval volumes in the likelihood (a curvature estimator).

## 6. Status after session 12 (2026-10-28)
- 3+1 distances: best = related-pair Poisson likelihood (Casasola 2026's term) from an intrinsic start, ~75 % of Johnston's residual at n ≤ 3000; large n on the cluster (r24).
  Dropped: binomial overlap term in the likelihood (hurts; possible fix: α, τ_ca from coordinates), Laplacian eigenmaps (capped), Madsen local charts (noise-amplified at n ≤ 3000),
  switch as headline (diamond-specific). Slab at large n / equal density after r24 (agreed).

## 7. Status after session 13 (2026-10-28)
- r24 verdict: Poisson-only likelihood keeps 79–83 % of Johnston's residual at n = 3000–15000 (21/21 universes). Exact Poisson (+ soft relation term) = Gaussian; 1000 iterations = 400 (r26).
- Slab (laptop, n = 1500): +43 % all / +69 % interior; side-wall clipping costs about half (oracle +64 %); no wall correction (Roberto: diagnosis only). cluster r25 pending.
- Paper: `paper/counting-full-v2.tex` (3+1 storyline rewritten; review ~80 %). Off-arXiv literature pass done: BK24 exact-inversion correction, Pellegrin/Rideout–Wallden/Huang credits.
- Remaining before arXiv: r25 numbers; Roberto's items (affiliation details, AI statement, code URL, endorser); optional clean timing run; then the Boguñá email.
