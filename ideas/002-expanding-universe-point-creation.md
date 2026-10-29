# 002 — Expansion as creation of spacetime points (and matter as a sink)

**Status:** exploring
**Started:** 2026-10-24   **Last touched:** 2026-10-24
**Parent:** [001 — discrete spacetime](001-discrete-spacetime.md)

## The intuition (in plain words)
If spacetime is made of points with a fixed density (Sorkin: Number = Volume), then a growing universe must be
*creating* points. Conversely, where space "flows in" (river model of black holes), points must be *destroyed*.
Maybe expansion, gravity and the finite-universe cutoff of 001 are all aspects of one point budget.

## Thought experiment(s)
- **Hubble flow as a source.** Keep point density ρ fixed. A sphere of radius R grows as $\dot R=HR$, so
  $\dot N=\rho\,4\pi R^2\dot R=3H\,N$: each point "spawns" new ones at rate $3H$.
- **River model as a sink.** Schwarzschild = flat space flowing inward at $v=-\sqrt{2GM/r}$ (Hamilton–Lisle).
  With fixed density, points must vanish wherever the flow converges.

## Closest existing physics
- `[literature]` Causal sets, classical sequential growth (Rideout–Sorkin 2000): time passing = points being born.
- `[literature]` Steady-state cosmology (Bondi–Gold–Hoyle 1948): continuous creation of *matter* to keep density
  constant. Here it would be creation of *spacetime points*. (dates to verify)
- `[literature]` Riemann (c. 1853, unverified source): gravity as an aether flowing into matter, matter as sinks.
- `[literature]` Sorkin's Λ ~ 1/√N: N grows as the universe grows ⇒ Λ decreases over time ("everpresent Λ").
- `[established]` Cosmological horizons (Hubble radius $c/H$, de Sitter event horizon).

## Simple math
### Point budget (continuity equation)
$\partial_t\rho+\nabla\cdot(\rho\mathbf v)=s$ (s = creation rate per volume). With ρ constant: $s=\rho\,\nabla\cdot\mathbf v$.
- Hubble flow $\mathbf v=H\mathbf r$: $\nabla\cdot\mathbf v=3H$ ⇒ creation.
  Numbers: $H_0\approx2.2\times10^{-18}$ s⁻¹; per point per Planck time $3Ht_P\approx3.6\times10^{-61}$.
- River flow $\mathbf v=-\sqrt{2GM}\,r^{-1/2}\hat r$: $\nabla\cdot\mathbf v=\frac1{r^2}\frac{d}{dr}(r^2v)=-\tfrac32\sqrt{2GM/r^3}$ ⇒ destruction.
  At Earth's surface: $\tfrac32 v_{esc}/R_\oplus\approx2.6\times10^{-3}$ s⁻¹ — vastly larger than Hubble creation.
  Distributed sink (total inflow through radius r ∝ $r^{3/2}$), **not** a point sink in matter — differs from Riemann's
  incompressible-fluid picture (which would need $v\propto1/r^2$).

### Horizons as the rapidity cutoff (link to 001)
In 001, $\eta_{\max}\approx\ln(2L/\ell_P)$ with L = size of the universe. In an expanding universe the natural L is a
horizon (Hubble radius or event horizon), which changes with time ⇒ $\eta_{\max}(t)$ grows (slowly, logarithmically)
as the universe grows and points are created.

## Stage-1 toy: classical sequential growth (`sims/growth_percolation.py`, `viz/growing-universe.html`)
Events born one at a time; newborn picks each existing event as a direct cause with probability p ("originary":
at least one cause), inherits their past. Relational observables only.
- **Cosmic time** = height = longest chain back to the first event. Relational analogue of the GR *cosmological
  time function* (Andersson–Galloway–Howard 1998: sup of Lorentzian distance to the past). Its layers define the
  cosmological frame (C5) without any background. `[literature]` concept, `[ours]` use as the CMB-frame candidate.
- **Fixed p:** fast expansion to a fixed layer width, then a steady state (N=4000, p=0.02: ~20–35 per layer).
- **p = c/n** (about c causes per newborn): a single first event, then layers grow 1,2,3,3,5,7,…,~280 (c=3, N=4000) —
  an expanding universe from a "bang". Mean past links ≈ 2–3 (finite, small).
- **Caveat (C2!):** p depending on n uses the birth order as a hidden clock; Rideout–Sorkin covariance forbids that.
  Covariant route to the same effect: cycles of expansion/contraction renormalise the effective p downward
  (Martín–O'Connor–Rideout–Sorkin 2001); Ahmed–Rideout 2010 find de Sitter-like expansion after an origin element.
- "Destruction" of events makes no sense classically (an event, once happened, is part of the past); in a quantum
  growth model it could appear as destructive interference between histories. "Points per cosmic-time layer"
  growing/shrinking = expansion/contraction — that is where C7's creation/destruction lives.

## Answers to Roberto's open questions (session 2, 2026-10-25)
**Q1 Why the geometric and matter frames coincide in FRW** `[established]`. $ds^2=-dt^2+a(t)^2d\vec x^2$.
(i) Comoving worldlines $\vec x=$const are geodesics. (ii) Proper time from the bang along them is $t$; any moving
path has $d\tau=dt\sqrt{1-a^2\dot{\vec x}^2}<dt$, so the cosmological time function equals $t$ and its gradient is the
comoving 4-velocity. (iii) Isotropy forbids a nonzero mean matter velocity in that frame (it would pick a direction)
⇒ matter/CMB frame = comoving frame. Real universe: equal only on average (our 370 km/s dipole = local peculiar
velocity). Why the universe is isotropic at all is a separate question (horizon problem). Discrete task: show the
grown universe is statistically homogeneous/isotropic and that matter (once added) rests on average in the layer frame.

**Q2 Can quantum operators remove the hidden birth clock?** Not automatically: a quantum growth model still needs
a covariance condition (predictions for label-invariant questions independent of birth order); amplitudes could
depend on $n$ just as probabilities can. What *can* change: a coherent sum over all birth orders may make label
independence a symmetry of the sum (like summing over gauge orbits). Classical covariant alternative to test:
couplings that depend on label-invariant data of the chosen past (its size, its number of maximal elements) — the
Rideout–Sorkin $t_k$ family — instead of on $n$.

**Q3 Born later, but earlier in cosmic time.** Example: chain A≺B≺C (cosmic times 0,1,2); newborn D picks only A ⇒
cosmic time 1, spacelike to B and C: "elsewhere, at B's time". Birth order = order in which the map gets painted;
physics depends only on the causal order (cf. coordinate time in GR).

**Q4 Events = spacetime points** $(x^0,\dots,x^3)$: yes. A *place* persisting in time = a chain of events (a worldline).

**Q5 Does GR predict the CMB? Its asymmetries?** (session 2)
- `[established]` CMB = hot big bang: GR expansion (T ∝ 1/a) + atomic/thermal physics (recombination, z≈1100).
  Predicted ~5 K by Alpher–Herman 1948; found 1965. GR supplies expansion, not the radiation itself.
- Dipole (~1e-3): our motion, ~370 km/s. Kinematic, explained.
- Anisotropies ΔT/T ~ 1e-5: statistically isotropic, nearly Gaussian, almost scale invariant (n_s ≈ 0.965);
  origin = inflation-era quantum fluctuations (not GR alone); evolution = GR perturbations + plasma physics.
- Anomalies (low quadrupole, quadrupole–octopole alignment, hemispherical asymmetry ~3σ, cold spot): ~2–3σ,
  mask/foreground dependent, possibly flukes. Do NOT impose them on the model.
- **Cosmic dipole tension** `[literature]`: quasar number-count dipole ~2× the CMB-predicted kinematic dipole
  (Secrest et al. 2021, 4.9σ; Dam et al. 2023, 5.7σ; contested by Abghari et al. 2024 — sky-mask coupling; still open
  2025–26). If real, the matter frame ≠ CMB frame. **Direct test for C5** `[ours]`: our model predicts one
  geometric cosmological frame (longest chain); a genuine matter–radiation frame mismatch would have to be explained.
- What the model must reproduce: statistical isotropy, amplitude ~1e-5 (A_s ≈ 2.1e-9), n_s ≈ 0.965. Speculative
  hook: Poisson fluctuations in event counts as a seed of primordial perturbations (cf. everpresent Λ).

## S2 results (2026-10-25, `sims/s2_counting_geometry.py`)
A) **Curvature by counting works, roughly.** Smeared 2D Benincasa–Dowker operator (Sorkin's ε-version, ε=0.03,
   non-locality scale ℓ/√ε ≈ 6ℓ; unsmeared ε=1 has per-event noise std ≈ 48, useless at these sizes).
   Flat diamond: R ≈ 0 (−0.0001). 2D de Sitter (R=2H²): right sign, right order; ratio to exact 0.5–2.3 across
   runs/sizes (N ≈ 4k–12k). Errors are correlated between events (shared pasts) → quoted sems underestimate.
   Precision needs ≳10^5 events (dense N×N matrices limit us to ~12k).
B) **Grown universes are not 2D spacetimes.** Myrheim–Meyer dimension of intervals from the first event:
   fixed p → 1.7, 1.4, 1.3, 1.2 with scale (a thin tube, ~1D at large scales); p=3/n → 1.6, 2.1, 2.5, 2.8
   (dimension keeps growing; no fixed dimension). So "compare with a 2D GR universe" is not meaningful for these
   rules. Consistent with the known problem that generic growth is not manifold-like.
C) **Clock independence (C5b) passes.** Height clock vs past-volume clock order spacelike pairs differently only
   when the pair is within ~1–3 layers (discreteness fuzz): disagreement 33% (1 layer), 13–15% (2–3), 1–2%
   (4–7), 0% beyond 8 — for a flat sprinkling and both growth rules. The cosmological slicing is clock-independent
   up to discreteness-scale fuzz.
D) **Important limitation for C6:** in 1+1 (and 2+1) dimensions Einstein's equations have no Newtonian limit
   (2D: Einstein tensor ≡ 0). Newton + Einstein can only be tested in 3+1.
Literature path forward: weighting causal sets by the BD action gives a manifold-like phase in 2D (Surya 2012,
"Evidence for a phase transition in 2D causal set quantum gravity"; Brightwell–Henson–Surya 2007; Glaser et al.).

## Computing budget & the quantum weights (session 2 Q&A)
- 100k-event curvature check: dense N×N impossible (~10^10 entries); but the smeared operator only needs pairs with
  few events between them ⇒ ~(1/ε)·ln N pairs per event; in 2D, interval counts are rectangle counts (range-count
  structure). Estimated minutes of runtime after an afternoon of coding. Validation only.
- Three different "rules": (1) classical growth (what S1/S2 used: probabilities, step by step); (2) weights over
  whole universes, e^{iS_BD} (CST's quantum sum over histories); (3) Roberto's operators layer by layer. (2) and (3)
  are two faces of one thing, like Feynman path integral ↔ Schrödinger operator; a preferred slicing (C5) lets us
  write (2) as a transfer matrix between cosmic-time layers = (3).
- Why e^{iS} can't be Monte Carlo sampled: complex phases are not probabilities ("sign problem"); cancellations make
  cost exponential in N. CST workaround: analytic continuation e^{iβS} → e^{−βS}. Exact sums avoid the sign problem
  for tiny universes: number of unlabeled causal sets (posets) = 16,999 (N=8), 183,231 (N=9), 2,567,284 (N=10)
  (OEIS A000112) ⇒ exact quantum sums feasible for N ≲ 9–10. Quantum computers proposed for BD counting
  (Adamson–Wallden 2025).
- Literature sizes: 2D BD-weighted MCMC reaches its asymptotic regime at N ≳ 65 (Glaser–O'Connor–Surya 2018);
  continuum phase has constant negative curvature. So S3a is laptop-feasible.
- 3+1 (needed for C6): kinematic checks with ~10^5–10^6 sprinkled events feasible with smart code; full 4D
  dynamics (MCMC/quantum over 4D causal sets of macroscopic size) is research frontier, beyond us.

## S3a / S3b results (2026-10-25, `sims/s3a_mcmc_2d.py`)
2D orders weighted by e^{−βS_BD} (ε = 0.21), Metropolis with swap moves.
- **Phase transition reproduced:** small β → spacetime-like (ordering fraction ≈ 0.50 ⇒ d ≈ 2; longest chain
  ≈ 0.8·2√N; N=70: ~13–14 layers); above β_c → layered "crystal" (r ≈ 0.6–0.7, 3–7 layers, S/N ≈ −3).
  β_c ≈ 1.2 (N=30), ≈ 0.7 (N=50), ≈ 0.5 (N=70): decreases with N, as in Surya 2012 / Glaser et al. 2018.
  S/N drifts negative before the transition (continuum phase with negative curvature in the literature).
  Acceptance is low (4–8%) in the crystal phase: those numbers are less equilibrated.
- **S3b clock independence** (common first event added = "a beginning"): height vs past-volume clocks disagree only
  for pairs 1–2 layers apart (12%, 2%), 0% beyond 4 layers, in both phases (β=0, 0.3, 1.2; N=70).

## S3-quantum results (`sims/s3q_exact_quantum.py`, exact sums, no sampling)
**Conceptual lesson:** quantum mechanics needs a *record*: histories ending in the same record interfere. If every
whole universe is its own record, phases never matter. Natural records under C5: AGE (number of cosmic-time
layers) or PRESENT (events in the last layer). Different universes with the same record = different pasts of the
same "now" ⇒ interfere. (This is the transfer-matrix / operator view, idea 004.)
- Record = AGE, ε=0.21. Classical e^{−βS}: as β grows, collapses to flat layered universes (N=9, β=8: age 2 with
  76%). **Quantum e^{iβS}: the layered universes are suppressed by destructive interference; probability moves to
  taller universes** (N=9, β=8: age 5 with 62%, age 2 with 0%). Same trend at N=8. Consistent with Surya's claim that
  the continuum phase "survives analytic continuation".
- Caveats: N ≤ 9 is a cartoon; "taller" ≠ proven spacetime-like (dimension not measurable at N=9); results depend on
  the choice of record (PRESENT record shows a different, less clear pattern); ε chosen, not derived.

## Literature matches for C7/C8
- `[literature]` GFT condensate cosmology (Gielen–Oriti–Sindoni 2013–14; Oriti–Sindoni–Wilson-Ewing 2016): quanta of
  geometry created by field operators; universe = condensate; Friedmann eqs. + bounce emerge. ≈ C7 with operators.
- `[literature]` Quantum graphity (Konopka–Markopoulou–Smolin 2006; KMS 2008): each link a qubit on/off; geometry =
  low-energy connectivity ("geometrogenesis"). ≈ C8.
- `[literature]` Quantum sequential growth: Gudder 2012 (amplitude processes, complex percolation); Sorkin–Surya quantum
  measure; Srivastava–Surya 2026 (Bell causality with transition operators). ≈ C7+C8 in causal-set language.
- `[literature]` Benincasa–Dowker 2010: curvature/action of a causal set by counting intervals → route to C6.

## Predictions / what would distinguish it
- (to develop) Λ evolving as $1/\sqrt N$; valency per point growing with cosmic time.

## Objections & tensions
- The sink rate $\nabla\cdot\mathbf v$ depends on the chosen observers (Painlevé "raindrops"). A fixed-density point
  picture needs a preferred family of observers ⇒ preferred frame (an aether) again — compare 001 option A.
- Is creation/destruction of points a dynamical law or bookkeeping of a slicing? Needs a covariant formulation.
- Steady-state cosmology was killed by the CMB; make sure we're not resurrecting its problems.

## Open questions
- Can creation (expansion) and destruction (gravitating matter) balance globally? What would that imply?
- Does point creation have a "temperature"/randomness (Poisson) that gives Sorkin's √N fluctuations naturally?
- Is $\eta_{\max}$ set by the Hubble radius or the event horizon?

## Log
- 2026-10-24 — seeded from 001 (finite universe + point creation + river model).
- 2026-10-25 — river/sink dropped (aether). Stage-1 growth toy; constraint list C1–C8; literature for quantum creation/links.
