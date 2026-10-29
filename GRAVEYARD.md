# Graveyard: ideas that died, and claims we gave back

Killed ideas are progress (CLAUDE.md). Each entry says **what** the idea was, **when** it died, **what killed it**, and where the details live.
Two kinds of death: **killed** (a calculation, an experiment or a constraint rules it out) and **dropped** (not wrong, but a worse road than another).
A third list records **claims we gave back**: things we called `[ours]` that the literature already had. Created session 10 (2026-10-27).

## Killed

| # | Idea | Died | Killed by | Details |
|---|------|------|-----------|---------|
| K1 | A regular crystal (lattice) of events | S1, 2026-10-24 | Lattice metrics have polygonal light cones and a rest frame (Burago; Weyl's tile argument); conflicts with C4 | idea 001, draft v2 App. A |
| K2 | Quantum blur of event positions | S1 | Blur *in what*? Presupposes a background (C2). An equal superposition over rapidity can't be normalized | idea 001 |
| K3 | Quantum chain as the *source* of blur ("like an atomic linewidth") | S1 | Wrong limit: an isolated point is infinitely blurry and coupling *reduces* blur (lesson 1) | idea 001, `sims/quantum_chain_blur.py` |
| K4 | River model: expansion as a source, gravity as a sink of points | S2, 2026-10-25 | Needs a flowing aether (C2) | idea 002 |
| K5 | Links ↔ Bell non-locality | S1 | Links are timelike; Bell correlations are spacelike | idea 001 |
| K6 | (L/ℓ_P)² ≈ 10¹²² explains Λ | S1 | Numerology: every combination of L and ℓ_P is a power of 10⁶¹ (lesson 7) | idea 001 |
| K7 | η_max as a dispersion correction (testable cutoff) | S4–S5, 2026-10-25 | In 1+1 a finite past keeps Sorkin's □ exact for every wavelength; the "−1/ℓ² jump" was a rapidity-wedge artefact (lesson 18) | idea 001, `sims/side_*` |
| K8 | η_max = Caravelli–Markopoulou long-link suppression | S4 | Different object: spatial lattice, external time, gives a running mass (lesson 16) | idea 001 |
| K9 | Growth rule p = c/n | S2 | Uses birth order as a clock (C2); and no 2D spacetime emerges | idea 002 |
| K10 | Transfer matrix on thick height layers | S5 | Memory must grow to ~40 % of the age; the height truncation breaks clock independence (C5) | idea 004 |
| K11 | A finite-state "film" in an accelerating universe | S5 | The thick present never retires events when there is an event horizon | idea 004 |
| K12 | Per-step normalization of quantum growth | S6 | Breaks covariance, increasingly with N (×10 at N = 22) | idea 004 |
| K13 | "Memory shared with the outside" as the area-law part | S6 | It is 100 %: outside events need old events forever (lesson 21) | idea 004 |
| K14 | A cell macrostate for what a newborn feels (rung 2) | S9 | Shuffling inside light-cone cells scrambles Sorkin's □, worse with N. (Anticipated by Sorkin 2007: fluctuations grow with N, concentrate on the light cone) | idea 004, `sims/r2_*` |
| K15 | "Probabilities are cheaper to store than states" | S9 | The opposite (2ⁿ numbers vs n bits); only *summing* can save memory | idea 007 |
| K16 | Diósi–Penrose collapse with R₀ = discreteness length | S9 | Smaller R₀ means faster collapse and more radiation; Gran Sasso excludes R₀ ≲ 1 Å | idea 007 |
| K17 | Exactly orthogonal futures of birth-order pasts as records | S9 | With an open future, any two small pasts share a common future: one sector always | idea 007, `sims/r3_*` |
| K18 | Endpoint-only phases change the growth memory | S9 | Path-independent ΔS ⇒ phases are a diagonal gauge of the past/future matrix (lesson 25) | idea 007 |
| K19 | "Forget what's recorded" (ii) implies holography (iii) | S9 | Counting: fixed-size cells keep a volume law; area needs cells of size √(Lℓ) (lesson 24) | idea 004 |

## Dropped (not refuted, a worse road)

| # | Idea | Dropped | Why | Details |
|---|------|---------|-----|---------|
| D1 | Manifold detector on exact quantum sums (N ≤ 12) | S3 | Detector unreliable below N ≈ 100; replaced by sampling at N = 200 | idea 005 |
| D2 | Quantum weights at N = 100 on stress quartiles | S4 | The small-sample hint was noise; superseded by N = 200 | idea 005 |
| D3 | A1: uniform sampling of e^{iβS} beyond β ≈ 0.2 at N = 200 | S4 | Average phase ~e^{−β²σ²/2} → sign problem; only the variance effect is visible. Closed. | idea 005 |
| D4 | Lorentz-invariant truncation of memory (escape i) | S9 | Roberto: hand-made | idea 004 |
| D5 | Collapse with a "different enough" threshold | S9 | Roberto dislikes thresholds; Sorkin's quantum measure (one history, no threshold) chosen instead | idea 007 |
| D6 | Steady-state-like creation of events | S2 | Steady-state cosmology is dead (CMB); kept only counting-based growth | idea 002 |
| D8 | J₂ / fixed-n propagator as a new curvature estimator | S10 | It detects curvature only through the related-pair share (same 3σ sample size as c₂ alone): the known chain-abundance route | idea 006, `sims/r6_*` |
| D7 | Bubbles of space (003) as a separate track | S3 | Merged into roadmap B (matter); still a seed, not dead | idea 003 |

## Claims we gave back (found in the literature, session 10 deep review)
Not failures: they mean we were on a real road. The draft must cite these and stop calling them ours.

| Claim | Where it already is |
|---|---|
| MDS spectrum as a manifold/dimension test | Clough & Evans 2016 (arXiv:1602.03103): Lorentzian MDS on causal sets, eigenvalue spectrum for dimension and manifoldness. Ours: count-based inputs and the calibrated statistics vs N. |
| The rapidity-wedge −2 and non-commuting limits for Sorkin's □ | Boguñá & Krioukov 2025 (arXiv:2506.18745). Ours: finite past diamond exact up to e^{−V}; the ½ assembled at the null edges. |
| The age of the universe as the infrared regulator of causal-set non-locality | Sorkin 2007 (gr-qc/0703099), with a cosmic rest frame. Ours: the number η_max ≈ ln(2L/ℓ_P) ≈ 142 and the "frame of the state" framing. |
| 10²⁴⁴ events vs 10¹²² horizon entropy | Sorkin 2007 (arXiv:0710.1675): N ~ 10²⁴⁰, Λ ~ N^{−1/2}. Ours: reading N as memory, Little's law, per patch, "finite iff no event horizon". |
| Two-layer order as the large-β ground state | Cunningham & Surya 2019 (arXiv:1908.11647). |
| Weight (# natural labellings) × e^{iS} for grown causal sets | Surya's Living Review §6.4. |
| Quantum suppression of layered orders as within-class cancellation | Implicit in Loomis–Carlip 2018 and Carlip–Carlip–Surya 2023 (steepest descent on binomial sums). Ours: the Monte Carlo check at N = 200. |
| Coarse cells can't capture what an element feels | In substance Sorkin 2007 (gr-qc/0703099). Ours: the cell-shuffling test. |
| Finite past ⇒ Sorkin's □ on a constant exact up to e^{−A} | Per-event form of Buck–Dowker–Jubb–Surya 2015 (1502.05388): summed over an interval it gives their corner value ⟨S⟩ → 2 (checked, `sims/r7_corner_check.py`). The "½ from the null edges, ¼ each" location claim is dropped: a conditionally convergent integral has no meaningful location. |
| The Laguerre identity itself | Combinatorics (Lifschitz–Pittel 1981; OEIS A002720). Ours: applying it to Johnston's propagator (not found in 99 citing papers). |

## Corrections of our own claims (kept for honesty)
- S1: "coupling produces blur" → coupling reduces it (K3).
- S3: "correction" of 40M–480M universes to poset counts was wrong and reverted (lesson 11b).
- S4: Caravelli–Markopoulou "directly relevant to η_max" → not the same object (K8).
- S4: "abrupt −1/ℓ² for long waves" → wedge artefact (K7).
- S9: "the memory accounting is the same with or without picking" → only per branch (idea 007).
- S10: v5 called the N = 400 result "hysteresis"; the cold chains have acceptance ≤ 0.001, so part of it is a frozen sampler, not physics (idea 005).
