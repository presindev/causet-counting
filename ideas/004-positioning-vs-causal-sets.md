# 004 — Where we stand relative to causal set theory (and CDT, GFT)

**Status:** exploring (positioning note)
**Started:** 2026-10-25   **Last touched:** 2026-10-27

## Shared with causal set theory (CST) `[literature]`
Kinematics: events + causal order (C1), relations only (C2), Number = Volume, links as neighbours, infinite valency
& non-locality, longest chain = proper time, growth = passage of time, matter as fields on elements, BH entropy as
links, Λ ~ 1/√N. Our elementary derivations are re-derivations.

## Where we differ (so far mostly choices, not results)
1. **Finite universe as *the* regulator + a physical cosmological frame (C3, C5).** CST keeps exact Lorentz
   invariance as a principle and treats any frame as emergent/approximate; we promote the cosmological frame to a
   structural ingredient and require it to match the matter frame (testable via the cosmic dipole). `[ours]`
2. **A preferred foliation licenses a Hamiltonian / operator description.** CST avoids foliations and uses
   sum-over-histories (quantum measure). With C5 we may evolve layer by layer with operators that create events
   (C7) — and the birth-order clock is replaced by the physical, relational cosmic time (partial answer to
   Roberto's Q2: not "quantum" per se, but "the cosmological frame provides a legitimate clock"). `[ours]`
   Caveat: layers must be defined during growth (maximal antichains / longest-chain height) — not trivial.
3. **Quantum links (C8)** — each link with an amplitude/qubit, as in quantum graphity; in CST the order is classical
   within each history. `[literature]` elsewhere, hybrid is ours.
4. **Creation operators for events (C7)** — in CST, Fock spaces exist for matter fields on a *fixed* causal set
   (Johnston, Sorkin–Johnston); operators creating *elements* belong to GFT. Search (2026-10-25) found no
   layer-by-layer operator growth of causal sets. `[ours]` niche, possibly unexplored, possibly for good reasons.

## Is the cosmological clock an absolute time / background? (Roberto, session 2)
Distinguish:
- **Newton's absolute time:** given a priori, independent of contents, uniform, universal simultaneity. A background.
- **Our cosmic time** (height = longest chain to the first event): *computed* from the events, changes when they
  change, every observer computes the same value from the order alone, not uniform (layers grow/shrink). Same status
  as FRW cosmic time in GR — a property of the state, not a background.
- Time dilation survives: an observer's own clock = length of their own chain; any chain between two events is
  at most the longest one, so moving observers age less (twin paradox built in).
**Where the danger really is:** if the *laws* (growth operators) are written using cosmic time, the frame moves from
the state into the laws — that is Hořava–Lifshitz territory and the "problem of time" of quantum gravity.
**Safeguards (now in C5):** (a) local rules (what happens between neighbours) must not depend on cosmic time;
(b) clock independence: predictions must not change if another relational clock is used — e.g. the
*cosmological volume function* (number of events in the past) instead of height — except possibly near η_max.
Literature: relational clocks / problem of time (Page–Wootters, deparametrisation) — to verify before citing.

## Uncomfortable neighbour: CDT and Hořava–Lifshitz
A preferred foliation + transfer matrix between slices is exactly CDT (Ambjørn–Jurkiewicz–Loll), and CDT ≈
Hořava–Lifshitz gravity in 2d ("2d CDT is 2d HL quantum gravity", arXiv 1302.6359; "CDT meets HL", 1002.3298).
HL gravity has a fundamental preferred foliation and known problems (extra scalar mode, strong coupling).
Our foliation is *cosmological/emergent* (C5) rather than fundamental — we must make sure that difference is real.

## Honest summary
Kinematics: CST. Quantum dynamics we're leaning toward: CDT-like foliation + GFT-like creation operators +
graphity-like quantum links, with the foliation coming from cosmic time by counting. The differences only become
real when a calculation gives a different answer (e.g. S3 with operators vs quantum measure; dipole for C5).

## Literature review on A2 and C8 (session 3, 2026-10-25; see literature.md)
- **A2 pieces exist separately** `[literature]`: Gudder's shells (height layers + amplitudes, but rigid ⇒ non-manifold),
  Gudder's isometric dynamics (a growth "Hamiltonian"), Major–Rideout–Surya thickened antichains (classical),
  quantum causal histories (states on a fixed causal set), Surya–Zalel complex growth.
  **Not found:** a Hilbert space on thickened height layers with event-creating operators *derived from e^{iS_BD}*;
  a height-vs-past-volume clock-independence test in any growth model; a cosmic-frame vs matter-frame test.
- **C8 pieces exist separately** `[literature]`: quantum graphity (quantum links, but undirected, external time;
  stalled: fragments, needs matter), Caravelli–Markopoulou (Lorentz invariance needs long links suppressed by length),
  indefinite causal order (quantum info, not spacetime), Arrighi–Martiel (superposed graphs, no geometry).
  **Not found:** causal-set links as qubits/amplitudes with a manifold-like dominant sector.
- Obstacles: non-unitarity when layer sizes change (at least for coarse-graining moves), measure extension/covariance,
  Bell causality pushing toward commuting operators, S_BD non-local over ~4 layers, links not independent
  (transitivity), entropy of non-manifold orders.
- Observation `[ours]`: complex percolation (amplitude per link choice at birth) is C8 *inside* growth ⇒ C8 can be a
  variant of A2, not a separate programme. And our cutoff η_max is a concrete version of the long-link suppression that
  Caravelli–Markopoulou require.

## A2, first measurements: does the action split into thick layers? (session 5, 2026-10-25) `[ours]`
Code: `sims/a2_memory_depth.py`, `sims/a2_truncated_sums.py`. Height layers (longest chain from the minimal events). $S_m$ = BD action keeping only
related pairs with height gap ≤ m. Events strictly between x and y lie in intermediate layers (checked), so $S_m$ is a function of
windows of m+1 layers: a transfer matrix with memory m would reproduce $e^{i\beta S_m}$ (only the amplitude; the 2D-order configuration space is not layer-Markov).
- **Links skip layers:** continuum 2D orders, share of links with gap ≥ 2 is 48 / 55 / 61 % at N = 50 / 100 / 200. Max gap 12 / 17 / 23, i.e. nearly the
  whole age. This is the Bombelli–Henson–Sorkin non-locality (one link per unit rapidity) seen along the time direction.
- **Memory needed grows with N** (relevant measure: sd(S − S_m)/σ_S, since a constant shift cancels in P_q; shares of Σf mislead by cancellation):
  ≤ 0.25 σ needs m ≈ 9 (N = 100, ~16 layers), ≈ 10 (N = 200, ~24), ≳ 14 (N = 400, ~36). The error is not monotone in m.
  Crystal phase: m ≈ 4 suffices; two-layer order: exact for m ≥ 1.
- **Exact sums, N = 9:** m = ∞ reproduces S3-quantum (AGE, β = 8: 0.615 at 5 layers). Dropping 4.5 % of pairs (m = 3) shifts P_q by TV 0.1–0.47 at β ≥ 4.
  Harmless (TV ≤ 0.01) only at m ≥ 4 for β ≤ 2. N ≤ 9 universes have ~4 layers, so they can't distinguish "short memory" from "no truncation".
- **Clock swap (N = 9, volume clock hv = ⌊1.51√|past|⌋):** height-truncated and volume-truncated P_q differ as much as each differs from exact
  (AGE, m = 3: TV .01 / .06 / .23 / .38 at β = 1 / 2 / 4 / 8). A truncated transfer matrix violates C5's clock independence at the level of its truncation error.
  The volume clock is coarse at N ≤ 9; indicative only.
- **Reading:** a thick-layer transfer matrix with fixed memory does not exist in the continuum phase. The memory has to be a fixed *fraction of the age*,
  because the same non-locality that the finite universe regulates in space (C3, η_max) appears in time. Options: (i) state = whole past (quantum sequential
  growth, known); (ii) state = something smaller than the past but not "the last m layers", e.g. the present layer plus a coarse summary of the past
  (a few interval counts per present event); (iii) accept memory ∝ age. To discuss with Roberto.

## A2 option 2: causally close, not recent in rows (session 5, 2026-10-25) `[ours]`
Growth rule (Roberto) = Rideout–Sorkin internal temporality `[literature]`: a new event may get any down-set as its past but never becomes a cause
of an existing event. Consequences: heights (dates) never change; every causal set is still reachable (linear extensions), and e^{iβS} doesn't depend
on the growth order, so the rule costs nothing; "now" for growth is the frontier (maximal events), spread over rows.
Adding f changes S only by $\Delta S_f = 4\epsilon - 8\epsilon^2\sum_{x<f} f(n_{xf},\epsilon)$ (checked: sum over births = action to 1e-10).
Truncate by causal closeness: keep x with $n_{xf}\le n_{\rm cut}$ (a count: Lorentz-invariant, no clock, so C5 holds automatically).
Code `sims/a2_causal_memory.py`; continuum = random 2D orders (60/40/20 universes at N = 100/200/400), crystal = S3a β = 0.6, N = 200.

| n_cut | sd(S−S_cut)/σ_S N=100 / 200 / 400 | crystal N=200 | past events kept per new event N=100 / 200 / 400 |
|---|---|---|---|
| 0 (links) | 0.49 / 0.35 / 0.27 | 0.60 | 3.2 / 3.9 / 4.6 |
| 5 | 0.27 / 0.17 / 0.13 | 0.16 | 11 / 15 / 19 |
| 10 | **0.060 / 0.068 / 0.064** | 0.068 | 16 / 22 / 29 |
| 20 | 0.040 / 0.054 / 0.056 | 0.044 | 20 / 31 / 44 |
| 30 | 0.007 / 0.012 / 0.012 | 0.019 | 23 / 37 / 54 |

- **A fixed causal cut works at every N** (n_cut = 10 → error ≈ 0.06 σ_S, flat in N), unlike the height cut (memory ≈ 40 % of the age).
- The kept events are few (grows ~ ln N, ≈ +6.6 per doubling, as expected from a fixed count per unit rapidity) but **far back in rows**: the largest
  row gap among them is ~ the whole age (15 / 22 / 33). Influence is sparse and long-range in time, local in "events between".
- The mean of S − S_cut grows ∝ N (a constant shift per event): it cancels at fixed N; with N varying it renormalises the 4εN term (cosmological-constant-like). Not explored.
- Caveats: σ_S from few universes (7.4 / 14.5 / 24.3, vs 7.0 / 12.5 / 18.6 from larger samples in session 3); only the amplitude is truncated, the counting
  measure is untouched; the "state" (frontier + causally close past) hasn't been shown to close under growth yet.
- Next: define the state = frontier events + their pasts within n_cut, and check that a new event's ΔS (to n_cut) is computable from the state alone, and that the
  new state is too (Markov closure).

## A2 option 2, closure: the thick present (session 5, 2026-10-25) `[ours]`
Code `sims/a2_thick_present.py`. State after k births (in hindsight) = born events still needed (n_xf ≤ 10) by some later birth. Closure is automatic:
if f needs x, every z between x and f is needed too, so f's truncated ΔS is computable inside the state. The question is its size.
- **Diamond (open space with corners):** state ≈ 0.63 N (rest-frame order) or 0.80 N (θ = 1), i.e. ∝ N. Cause: an event's longest links run along its light
  cone to the diamond's side corners, born half-way through. Per newborn the memory is small (≈ ln N), but over all newborns almost every old event is still needed.
- **Closed space (cylinder: circle of length W, duration T, density 1, births in cylinder time):** state ≈ **0.5–0.58 W², independent of the age T**
  (T = 2W–8W, W = 10–20). An event stays needed for ≈ **0.5–0.6 W**, about the time its two null rays take to meet around the circle; after that every later
  event has many events between.
- **Reading:** the film has a finite state only in a closed universe, and its thickness is set by the **size of space**: the thick present is about half a
  light-crossing time. This is C3 again, now in time: the finite universe regulates the memory, as it regulates the rapidity (η_max).
  For our universe (age ~ size) the state is still most of the universe; the reduction pays only for a universe much older than its size.
- Open: n_cut dependence (only 10 tried); expanding universes, where light cones may never wrap (event horizons) — then the memory might not close at all;
  whether a state that doesn't use hindsight is much bigger; the counting measure.

## A2 option 2 in an expanding closed universe: the memory never closes (session 5, 2026-10-25) `[ours]`
Code `sims/a2_thick_present_desitter.py`. Closed 2D de Sitter in flat slicing (H = 1, circle of comoving length W, conformal time η ∈ [η0, η1]),
births in cosmic time t = −ln(−η). Light cones wrap only if conformal time W/2 remains, so events born after an early time never wrap.
- State / events born so far = **0.90–0.98** at every checkpoint (N ≈ 1,200–1,600, W = 4 and 8). Of the first 10 % of events, **76–90 % are still needed**
  by late births. Almost nothing retires.
- It *looks* thin (state ≈ 1.5 × the events born in the last Hubble time) only because the population grows like e^{t}: most of the past is recent.
- **Verdict:** a finite-state film (option 2 as a transfer operator) exists only for a closed, non-expanding universe. With open space or with acceleration
  (our universe has Λ) the state is the whole past, forever. Option 2 as a finite state is **killed** for realistic cosmologies; the per-birth rule
  (local in events-between, clock-free) survives as a cheap growth step inside option 1 (whole-past state = quantum sequential growth).
- Consistent with Roberto's intuition that the state is "the whole universe / one wavefunction".

## The rule behind it: memory lasts half a conformal light-crossing (session 5, 2026-10-25) `[ours]`
Code `sims/a2_thick_present_frw.py`: closed 2D FRW, ds² = a(η)²(−dη² + dx²), W = 4, N = 1,500, n_cut = 10.
- **Decelerating** (a ∝ t^{1/2}, a ∝ η): the first 10 % of events are all retired by k = 0.3 N; the oldest needed event is always ≈ **0.50–0.52 W** of conformal
  time back; state/born falls 0.51 → 0.34. The memory closes, as on the static cylinder.
- **Accelerating** (a ∝ t², a ∝ η⁻²): state/born = 0.90–1.00; nearly all events sit within W/2 of the end of conformal time, so they never retire.
- **Rule:** an event stays needed for ≈ W/2 of *conformal* time (until its light cone wraps). The film has a finite memory iff the universe has unbounded
  conformal future, i.e. **no event horizon**. Accelerating universes (de Sitter, a ∝ t^{p>1}, our ΛCDM future) have one ⇒ the state is the whole past.
- Thickness in cosmic time = W/2 in conformal time; in a decelerating universe that is a growing stretch of cosmic time (∝ a·W/2 locally).

## The memory question, per observer: the static patch (session 6, 2026-10-25) `[ours]`
Roberto (session 5): an accelerating universe's growth state is its whole past. Is something managing that memory? Code `sims/a2_memory_static_patch.py`.
2D de Sitter (H = 1), flat slicing; observer's static patch = past of the future endpoint, $|x| < -\eta$. The interval between two patch events lies inside
the patch, so the patch's memory is well defined on its own. Patch births = $2\rho$ per Hubble time (stationary). State at $t_{\rm now}$ = patch events born
before $t_{\rm now}$ that a later patch birth still needs ($n_{xf} \le 10$). Validated: float matmul counts exact; stable when the past or future is extended by 3 e-folds.
| $\rho = 1/(\ell H)^2$ | 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| patch state (events) | 85 | 160 | 316 | 598 | 1186 |
| state / $\rho$ | 3.4 | 3.2 | 3.2 | 3.0 | 3.0 |
Fit $\approx 2.8\rho + 2.8\sqrt\rho$.
- **Finite and stationary per patch:** the horizon *does* manage the memory. The global "whole past" of session 5 is just ~$e^{t}$ patches, each with a bounded memory.
- **But it's a spacetime-volume law** ($\propto \rho$, ≈ 1.5 Hubble times of patch births), not an area law. In 1+1 the horizon "area" is a point, so a
  holographic memory would be O(1) or ~ln ρ. We measure ρ: excluded.
- Where it sits: all events younger than 0.5/H are needed, 45 % of those aged 1–2/H, 11 % older than 2/H. The old tail leans to the horizon (state share at
  r > 0.8: 36 % vs 20 % for recent births), but the bulk dominates. Memory reaches back ≈ 1 Hubble time: the light cone has to leave the patch, as on the
  cylinder it had to wrap (session 5: half a light-crossing).
- **Reading.** If the 1+1 law carries over to 3+1 (unchecked; the near-null non-locality is worse with more directions), the memory per Hubble patch is
  ~ $(H\ell)^{-4} \sim 10^{244}$ events at $\ell = \ell_P$, versus de Sitter entropy / Bousso's N-bound ~ $10^{122}$. Caveat: events are not bits of
  independent quantum entropy. The Poisson randomness of *any* sprinkled spacetime is already volume-law data; the bound is on observable entropy.
  So the tension is with "discrete spacetime as stored data" in general, not with our growth rule in particular. Counting the *quantum*
  information (the dimension of the state space the patch needs) is the right test, and it needs A2's quantum version.
- Literature: Dou–Sorkin 2003 count links crossing a *horizon* → area `[literature]`; Rideout–Zohren 2006 get the spherical entropy bound from counting
  on a Cauchy horizon `[literature]`. Our count crosses a *time slice* of the patch, so the volume law doesn't contradict them: the horizon-crossing piece of
  our memory may be the area-law part. Not checked.

## A2 + C8, first exact test: amplitudes on the newborn's choice of past (session 6, 2026-10-25) `[ours]`
Code `sims/a2_growth_paths.py`. Each newborn chooses **any** down-set as its past (all posets, not only 2D orders). Per birth $e^{i\beta\Delta S_f}$ (clock-free).
- **Covariance and the counting measure.** A path's amplitude is $e^{i\beta S(C)}$ whatever the birth order, so summing paths gives
  $A(C) = L_{\rm nat}(C)\,e^{i\beta S(C)}$ ($L_{\rm nat}$ = number of natural labellings): covariant, and the counting measure comes out of growth by itself.
  **Normalizing per step** (choices sum to 1, CSG-style) **breaks covariance**: for $\{a<b,\ c\}$ one order passes through a 2-chain (3 possible pasts),
  another through a 2-antichain (4), so the normalizers differ. Normalized rules must have the percolation form (Rideout–Sorkin; Surya–Zalel complex).
  So our rule is a fixed-N sum, not a growth law with a sum rule (measure-extension problem, as listed in the obstacles).
- Validated: path counts 1, 2, 7, 40, 357, 4824, 96428, 2800472 (naturally labelled posets); antichain $S = 4\epsilon N$; 2D-order actions all recovered.
- **Results, N = 8, records AGE / PRESENT (coarse, so universes interfere):**
  - β = 0: the path measure prefers 3 layers (P = 0.80; Kleitman–Rothschild-like), versus 0.37 for the 2D-order (sprinkling) measure. With $|A|^2$ the entropy
    is squared, so it's sharper than classical counting.
  - A **β window suppresses the 3-layer sector to ≈ 0** by interference: ε = 0.15: β ≈ 10–16; ε = 0.21: β ≈ 5–8; ε = 0.3: β ≈ 4–5 (roughly βε² ≈ 0.3).
    There mean AGE ≈ 4.1 (paths) vs 4.2–4.7 (2D orders). Outside the window it comes back (small-N phases are quasi-periodic).
  - PRESENT doesn't follow: at ε = 0.21, β = 8 the path sum puts 0.98 on 2 maximal events (2D orders: spread over 1–4). Matching AGE ≠ manifold-like.
- **Known:** this is the Loomis–Carlip / Carlip–Carlip–Surya suppression of layered orders by $e^{iS}$ `[literature]`, here seen with the growth-path measure.
  New to us only in that the measure is natural labellings (growth) rather than unlabelled posets, which makes the entropy to beat larger.
- N ≤ 8 has 3–5 layers, so "3-layer" = KR-like is only suggestive. Next: N = 9 (~10⁸ paths, count unverified; needs a faster code or cluster), and the S4 manifold detector on the
  dominant posets within the window.

## Memory per patch in 2+1 and 3+1, and the horizon surplus (session 6, 2026-10-25) `[ours]`
Code `sims/a2_memory_patch_dims.py` (d = 2 reproduces the table above). Future cut checked (t1 = 6 → 8: d = 3 shifted 7 %, so t1 = 8 used).
| ρ = 1/(ℓH)^d | 25 | 50 | 100 | 200 | 400 | exponent (25→400) | area law would be |
|---|---|---|---|---|---|---|---|
| d = 2: state | 86 | 159 | 321 | 598 | 1203 | 0.95 | 0 (or log) |
| d = 3: state | 171 | 334 | 655 | 1258 | 2506 | 0.97 | 1/3 |
| d = 4: state | 264 | 509 | 1000 | 1899 | 3857 | 0.97 | 1/2 |
- **Volume law in every dimension** (state/ρ ≈ 3, 6.3, 9.6 for d = 2, 3, 4, drifting down ~10 % over the range). At ρ = 400, d = 4, the Hubble radius is only
  ~4.5 ℓ, so asymptotics are not proven, but the area exponent (0.5) is far away.
- **Horizon surplus** (memory depth rises from ≈ 1–1.3 Hubble times in the bulk to ≈ 3 near r → 1): surplus = 25 → 451 (d = 2), 51 → 1062 (d = 3),
  79 → 1669 (d = 4), exponent ≈ 1.1. Also volume law: it's not an area-law piece, it's the bulk near the horizon (cosmic-time slices are boosted there).
- **"Shared with the outside" is not a usable measure:** in 2D, 100 % of patch events born before now are needed by some outside event later (future cut
  T = 3, 4, 5). Light rays leave the patch and run on forever outside (session 5's global result). Killed as a definition.
- **Why (Little's law, as in queues):** memory = birth rate × how long each event stays needed. Birth rate ∝ ρ × Hubble 4-volume per Hubble time; lifetime ≈
  1–3 Hubble times, independent of ρ (its light cone must leave the patch). So memory ∝ ρ. An area law would need bulk events to be forgotten after a few ℓ,
  i.e. "only the recent past matters", which needs a preferred frame and contradicts C4. **With Lorentz-invariant non-locality, the classical event memory
  is a volume law.** An area law, if any, must come from the quantum state (redundancy of the past), i.e. from A2-quantum.

## Branch C: normalization and the stability of the past (session 6, 2026-10-25)
Framing (Roberto + Claude): we want (1) the BD action family, (2) consistency as the universe grows, (3) covariance (non-negotiable, C2/C5).
Branch A = fixed-N sum (mainstream CST path integral `[literature]`); B = complex percolation (sum rule, no action); **C** = all three. Roberto's proposal:
skip per-step normalization (Z cancels in ratios, as in stat mech) and demand instead that **questions about the past stabilise as N grows**
(a thermodynamic-limit criterion replacing the sum rule; `[ours]`, literature not searched).

**Test 1: does per-step normalization's covariance violation wash out?** `sims/a2_normalization_covariance.py`. Random 2D orders, 60 random growth orders each.
Hand check: {a<b, c}: 1/6 vs 1/8 along two orders (β = 0).
| N | 6 | 10 | 14 | 18 | 22 |
|---|---|---|---|---|---|
| β = 0: sd log∣∏Z∣ over growth orders | 0.30 | 0.52 | 0.87 | 1.33 | 2.30 |
| β = 0: sd / mean | 0.032 | 0.024 | 0.020 | 0.020 | 0.023 |
| β = 6 (ε = 0.21): phase coherence across orders | 0.96 | 0.57 | 0.42 | 0.25 | 0.18 |
- No washing out: the absolute spread grows (at N = 22 two orders of the same universe differ by a factor ~10 in weight), the relative spread stays ≈ 2 %
  (an extensive quantity's relative fluctuations would fall like 1/√N; these don't). Quantum: the phases of different orders decohere (0.18 at N = 22),
  so birth order becomes physical. **Per-step normalization with the BD action: killed.**

**Test 2: past stability in the fixed-N path sum.** `sims/a2_past_stability.py` (records = two-outcome stem questions; N = 3–8).
- Outside the window (small β) P_N settles smoothly: "more than one origin" → 1, "3-chain stem" → 0.18 (β = 0). That is the KR-dominated regime.
- **Inside the KR-suppression window the past is not stable:** "more than one origin", ε = 0.21, β = 6: 0.53, 0.36, 0.27, 0.40, 0.66, 0.87; ε = 0.15, β = 12:
  0.57, 0.32, 0.04, 0.10, 0.48, 0.81. Non-monotone swings of ~0.5 (a classical sum-rule growth can only increase a stem question's probability).
- "2-chain stem" is ≈ 0.99 almost everywhere (uninformative).
- **Reading:** at N ≤ 8 the past is stable where the universe is junk and unstable where interference suppresses the junk. Caveats: tiny N; at fixed β the
  window probably drifts with N (as β_c does classically), so a scaled β(N) may be the fair comparison. Not a kill; a warning. Needs N = 9–10 (enumeration
  over unlabelled posets weighted by natural labellings: 183 k / 2.6 M posets at N = 9 / 10, A000112 per compute.md; needs a poset generator).

**Test 3: follow the window** (`sims/a2_follow_window.py`). β*(N, ε) = β ∈ [0, 16] where the growth sum's AGE distribution is closest (TV) to a sprinkled 2D
spacetime's; evaluate the stem questions there.
- β*(N) jumps instead of drifting smoothly: ε = 0.21: 13.0, 13.6, 4.9, 9.1, 10.3 (N = 4–8). At these sizes the β landscape is quasi-periodic with several
  near-equal minima, so "the window" is not a well-defined path.
- Along β* the past still swings: ε = 0.3, "more than one origin": 0.74, 0.97, 0.20, 0.44, 0.63; ε = 0.21, "3-chain stem": 0.32, 0.38, 0.52, 0.24, 0.16.
- Matching AGE does not make PRESENT spacetime-like: TV(PRESENT) at β* is often worse than at β = 0 (ε = 0.3, N = 6: 0.58 vs 0.23).
- **Verdict:** inconclusive at N ≤ 8, and N = 9–10 won't change that much (the sign problem caps exact sums near N ≈ 12). Branch C needs an analytic handle.
- **What past stability requires, stated cleanly** `[ours]`: the amplitude of a past question at size N is Σ over its stems of e^{iβS(stem)} × F_N(stem), where
  F_N(stem) = sum over all continuations of the growth from that stem. A classical sum rule makes F_N = 1. In the fixed-N quantum sum, the past is stable iff
  F_N(stem) becomes the same for all stems (up to a common factor) as N → ∞: **"the future factorizes"**. Roberto's stat-mech intuition is exactly this
  hope. Next: compute F_N(stem) directly for small stems and watch whether the ratios F_N(X)/F_N(Y) converge (cheaper than full sums: one stem at a time).

**Test 4: the future factor directly (2026-10-26, session 7)** `[ours]`. `sims/a2_future_factor.py`: F_N(stem) memoized over unlabelled posets
(exact canonical form), all settings at once. Reaches **N = 10** in 45 s on the laptop (N = 9 in 3 s). Validated: distinct states per size = A000112
(1 … 183 231), β = 0 sums = number of growth paths (A006455, … 116 473 461, 6 855 780 268), Z_6 = explicit path sum of `a2_growth_paths.py`.
Ratio r_N = F_N(X)/F_N(antichain) for stems of size 2 (X = 2-chain) and 3 (all 4 others), written |r|∠phase/π.
- **β = 0 (counting only):** r_N(2-chain) = 3/(N+1) exactly for N = 3–10 (observed, not proved); 3-chain stem 0.50 → 0.046 (≈ 1/N²). Real, monotone →
  0: the counting measure makes "the first events were unrelated" certain. Stable, but in the KR direction.
- **Small β (ε = 0.21, β = 2, 4):** the same 1/N decay plus a phase that grows steadily with N (β = 4, 2-chain: 0.08 → 0.48 π over N = 3–10). Stable only because |r| → 0.
- **Inside the window (ε = 0.21, β = 6–8; ε = 0.15, β = 12; ε = 0.30, β = 3.5), 2-element stem:** big swings at N = 4–7 (|r| up to 5–8, phase turning by
  ~π), then the phase **locks** at N ≈ 8–10 and |r| decays slowly: β = 7: 0.75∠−0.99, 0.57∠+0.98, 0.51∠+0.99; β = 8: 0.58∠−0.88, 0.59∠−0.89, 0.56∠−0.86;
  ε = 0.30: 0.67∠−0.96, 0.52∠−0.97, 0.43∠−0.97 (N = 8, 9, 10). Step-to-step change ≈ 10 %, the same rate as the classical 1/N drift.
- **Inside the window, 3-element stems:** still moving at N = 10 (20–50 % per step, phases drifting 0.1–0.3 π per step at β = 6; at β = 8 one stem goes
  0.34 → 0.59 in |r|). Note the phase ≈ π for the 2-chain: chain stems interfere *destructively* against the antichain in the window.
- **Above the window (ε = 0.21, β = 12):** erratic at all N (|r| jumps 0.19 ↔ 0.78 for the 2-chain). No sign of factorization.
- **Reading:** the session-6 swings of P_N at N ≤ 8 are the N = 4–7 transient seen here. For the smallest stem, the window's future factor starts to
  behave like a stable ratio by N ≈ 10 (phase locked near π, slow magnitude drift); larger stems haven't reached that regime yet. **Inconclusive, leaning
  hopeful for 2-element stems.** Caveats: N ≤ 10; the window drifts with N, so fixed (β, ε) may leave it; "r → nonzero constant" vs "r → 0 like the
  classical case" can't be separated from 3 points. N = 11 would need ~2.7 M memo states (laptop memory, ~10 min) — feasible on the cluster; N = 12 (63 M posets
  of size 11) needs a non-Python generator.

**Literature status of Test 4 (session 8 review, 2026-10-27)** `[literature]`: no paper computes our ratio. Gudder, Dowker–Johnston–Surya 2010 and
Surya–Zalel 2020 build in a sum rule (amplitudes out of each node sum to 1), so there F_N = 1 automatically and the open problem becomes extending the
measure to N → ∞ (bounded variation). Surya–Zalel Thm 3.1: extension succeeds when the outgoing amplitudes become phase-aligned as n grows, which resembles
our 2-element stem's phase locking (resemblance only, not a proof). Brightwell et al. 2003: stem sets generate the covariant questions classically, so stem
ratios are the right observables; the quantum version "has not been worked out". Before claiming anything in a draft: INSPIRE citation crawl of Surya–Zalel
and DJS (not done). N = 11 with stems of size 2–4 submitted on the cluster (job 449812).

**Quantum memory: area or volume law? (session 8 pointer)** `[literature]`: causal-set entanglement entropy of a field (Sorkin–Yazdi 2018; Belenchia et al.
2018; Surya–Nomaan X–Yazdi 2021 for de Sitter horizons) is a volume law without truncation and an area law only after truncating the Pauli–Jordan spectrum.
That parallels our volume-law growth memory (session 6), but it measures a field state, not information stored in the growth history; the analogy is in how they
scale only. Mathur–Surya–Nomaan X 2022 suggest the volume law reflects causal-set nonlocality.

## Quantum memory: how to define it, and which escape (session 9, 2026-10-27) `[ours]` unless marked
- **Stakes.** In 3+1 with $\ell\approx\ell_P$ the classical memory per Hubble patch is $\sim(L_H/\ell_P)^4\approx10^{244}$ events vs the de Sitter
  entropy $A/4\ell_P^2\approx10^{122}$ (scale comparison, not a match). The gap is a crisis only if the memory we counted is the *smallest possible summary*
  of the past (like position + velocity summarizing an orbit). Session 6 counted events newborns can still link to, not the minimal summary.
- **Definition.** Amplitude per labelled history $\psi(h)=e^{i\beta S(h)}$. Cut after $k$ births: past $p$, continuation $c$,
  $M_{pc}=\psi(p\,c)$ (0 if $c$ can't follow $p$). SVD $M=\sum_k s_k u_k v_k^\dagger$; memory $=\log D$, $D$ = number of non-negligible $s_k$
  (or the entropy of $s_k^2/\sum s^2$). This is the bond dimension of sequential generation (Schön et al. 2005) `[literature]`; quantum models can store less
  than classical ones (Gu–Wiesner–Rieper–Vedral 2012) `[literature]`. **Link to branch C:** $F_N(p)=\sum_c M_{pc}$ = row sums of the same matrix.
- **Prior: volume law** unless a new ingredient: non-local $S$ gives random-like phases (Page); Sorkin–Yazdi volume law; area laws need local gapped ground states `[established]`.
- **Escapes:** (i) Lorentz-invariant truncation: dropped by Roberto (hand-made). (ii) forget what is already recorded (Roberto's favourite). (iii) holographic
  redundancy (Roberto: maybe).
- **Objection to (ii) as stated:** decoherence copies information, it doesn't delete it; records are stored information too. What (ii) can do is make the
  coherent part classical (keep the branch label, drop the phases), which lands back on the classical volume law. (ii) gives compression only if many
  microscopic pasts lead to the same record *and* the future depends only on the record: then (ii) becomes a form of (iii) (cf. quantum Darwinism, Zurek
  `(unverified reference)`). In our growth rule newborns link to individual events, so the rule itself would have to couple to records. "Record" isn't yet
  defined in the toy (lesson 3).
- **Possible calculation:** singular values of $M$ at N ≤ 9 (laptop) / 11 (cluster), controls β = 0, β > 0, random phases. Small N can't tell area from volume
  law; it can only tell whether phases compress.
- **Roberto's position (question zero):** the 10²⁴⁴ is the "clumsy simulation", not the universe; we're missing the compression the universe uses.
  He frames it as microstate → macrostate: the N → ∞ limit should give a "thermodynamic memory".
- **Correction (same session): (ii) does not imply (iii).** Coarse-graining into cells of size $\xi$ keeps a *volume* law with a smaller coefficient,
  $(L/\xi)^d$ cells. In $d$ = 4 an area law $(L/\ell)^2$ needs $\xi=\sqrt{L\ell}$, a cell that grows with the universe, which nothing in a local coarse-graining
  provides. (Lesson 7: this is the Cohen–Kaplan–Nelson 1999 UV/IR scale `[literature]`, near the dark-energy scale; numerology risk.)
- **Memory ladder** (proposed):
  1. events (microstate): spacetime-volume law (session 6, measured);
  2. macrostate = geometry + fields, future needs only Cauchy data on a slice: *spatial*-volume law `[established]` for GR as an initial-value problem; this is
     what (ii) can deliver, *if* our growth has a continuum limit that is Markov in the geometry;
  3. spatial volume → area: needs gravity (states that would collapse into black holes are excluded, CKN-style) or constraints (Gauss-law-like) = (iii) proper.
- **Toy test of rung 2 (1+1):** does a coarse summary of a recent slice (cell counts at scale $\xi$) predict what newborns feel (their layer counts / BD
  contribution) as well as the full past? Prediction: mean yes (local curvature), fluctuations no (Sorkin 2007: the discrete □ has fluctuations that grow with density;
  the smeared version with a mesoscale is the fix `[literature]`). Memory would scale like $L/\xi$ (1D slice), not $\rho$.
- **Result (session 9, `sims/r2_coarse_vs_micro.py`, outputs `sims/out/r2_*.txt`)** `[ours]`. Flat 1+1 diamond, newborn at the top, "what it feels" = Sorkin's
  2D operator on $\phi=1$ (raw and smeared, $\epsilon$ = 0.1, 0.03). Shuffle events inside each light-cone cell keeping the counts;
  $f_{\rm micro}=E[{\rm Var}(b\,|\,{\rm cells})]/{\rm Var}(b)$. Validation: means ≈ 0 in all runs. 16–24 independent bases × 8 shuffles, bootstrap errors.

  | events/cell | raw (N = 500 / 2000 / 8000) | ε = 0.03 (N = 500 / 2000 / 8000) |
  |---|---|---|
  | ≥ 31 | ≈ 1 / ≈ 1 / ≈ 1 | ≈ 1 / 0.90 / 0.99 |
  | 7.8 | 1.02 / 0.92 / – | 0.62 / 0.86 / – |
  | 2 | 0.99 / 1.07 / 0.95 | 0.20 / 0.30 / 0.66 |
  | 0.5 | 0.92 / 0.94 / – | 0.07 / 0.12 / – |

  - **Raw operator: no macrostate at all.** Shuffling within cells holding *half an event* already scrambles b; links are pure microstate.
  - **Smeared: a macrostate only at ≲ 2 events per cell, and it gets worse as the universe grows** (0.20 → 0.30 → 0.66 at fixed cell size). Cells boosted by θ = 2
    are worse at small N (0.74 vs 0.20 at N = 500). Reading: the dependence sits along the newborn's light cone (near-null non-locality again), where fixed cells
    can't resolve the hyperbola $uv$ = const.
  - **Rung 2 in its "local cells" form fails** for BD-type dynamics: classical coarse-graining compresses by at most a small constant factor, shrinking with N.
    Caveats: one newborn's quantity (no sum over many newborns); flat space only; cells tied to one frame (a Lorentz-invariant coarse-graining isn't known to us).
    Quantum phases care about absolute differences, so averaging over newborns wouldn't save the amplitude. This motivates idea 007 (sum over micro, don't store it).


## Test 4b: future factor at N = 11 (session 10, cluster job 449812: 47 min, 6.1 GB, 2.77 M states = A000112) `[ours]`
Compare each quantum ratio with the counting ratio: q_N = r_N(β)/r_N(0) (r_N(0) = 3/(N+1) for the 2-stem). If the past stabilises like counting, q_N converges.
- **β = 7 (window), 2-stem:** |q| = 2.25, 1.91, 1.89, 1.86 at N = 8–11, phase ≈ π throughout. **The smallest stem converges.** Same at β = 6 (|q| ≈ 1.8, phase drifting 0.85π slowly) and ε = 0.30, β = 3.5 (≈ 1.6∠π).
- **3- and 4-element stems:** |q| still falls by 20–40 % per step and the phases move by 0.05–0.3π per step in the window. Not converged.
- **β = 12 (above the window):** erratic. **β = 2–4 (weak):** |q| has converged, but the phase drifts *linearly*: Δphase/N ≈ 0.008π·β per relation in the stem
  (all 20 stems; slowly decreasing with N). A per-relation phase velocity: each relation in the past shifts later births' ΔS by a roughly fixed amount.
  The past is stable only if stems answering the same question share the drift. That isn't the case for "is the first pair related?" (1 vs 0 relations).
- **Verdict:** still inconclusive, sharper than at N = 10. Next: N = 12 on the cluster (~110 GB, ~20 h) and a mean-field model of the drift (ROADMAP N1).
- Literature (session 10 crawl): F_N not found; every QSG model imposes the Markov sum rule (F_N ≡ 1). Labelling weight known (Surya review §6.4).


## Test 4c: a model of the weak-β drift (session 10, `sims/r5_drift_meanfield.py`, outputs `sims/out/r5_N10_eps*.txt`) `[ours]`
- **Model:** to first order in β, F_N(X) ≈ Count_N(X)·e^{iβ m_N(X)}, with m_N(X) = ⟨S_N − S_X⟩ over all growth continuations (the β = 0 measure). The relative phase drift per
  added event is β·d_N, with d_N = Δm_{N+1} − Δm_N. m_N is computed exactly as phase(F_N)/β at β = 10⁻⁴.
- **Check against the exact N = 11 cluster data** (ε = 0.21, β = 2, 2-stem): exact N·d = 0.237, 0.244, 0.246, 0.244, 0.239 (N = 7–11); model (β → 0) N·d = 0.210–0.217 (N = 6–10).
  The ~10 % gap is the β³ cumulant. **The model explains the drift.**
- **How fast it dies** (2-stem; effective exponent a in d_N ∝ N^{−a}, from successive ratios over N = 6–10):
  ε = 0.21: a ≈ 0.95 (N·d flat, ≈ 0.21 per relation); ε = 0.35: 1.5 → 1.8; ε = 0.5: 2.2 → 2.6; ε = 0.7: ≈ 3.3. The exponent grows with ε and with N.
  The 3-stems behave the same way (N·d per relation 0.19–0.27 at ε = 0.21, slowly falling).
- **Reading:** the BD weights f(n, ε) ~ (1−ε)ⁿ die as the number of events between a stem relation and a newborn grows with N. Once N ≫ the non-locality scale, a > 1,
  so the accumulated relative phase converges and **the weak-β drift is not fatal**. At ε = 0.21 (scale ~1/ε² ≈ 23 events), N ≤ 11 is pre-asymptotic.
  The exact β = 2 data already turn over at N = 11 (0.246 → 0.239).
- **Correction (lesson 15):** before this calculation I told Roberto I expected the drift to be fatal ("I'd expect the answer to be no"). The data say the opposite is more likely.
- **Falsifiable prediction for job 449948 (N = 12):** at ε = 0.21, β = 2, the 2-stem's N·d keeps falling, to ≈ 0.233 ± 0.003 at N = 12. Flat or rising would mean 1/N, i.e. log-divergent.
- Not answered by this: the window (β ≈ 7), where the first-order model doesn't apply. There the 2-stem converges and the 3- and 4-stems don't yet.

## Test 4d: F_N at N = 12 (session 16, cluster job 449963: 56.9 h, 49.5 M memo states; `sims/fn_N12_check.py` → `sims/out/fn_N12_check.txt`) `[ours]`
- **Prediction of Test 4c confirmed.** ε = 0.21, β = 2, 2-stem: N·d = 0.2455, 0.2437, 0.2390, **0.2322** (N = 9–12), against the predicted 0.233 ± 0.003.
  Effective exponent a (d ∝ N^−a) 1.20 (N = 10→11), 1.33 (11→12): above 1 and growing, so the weak-β relative phase converges if the trend holds. The N = 12 file
  reproduces the N = 11 run's values to four digits.
- **The window (β ≈ 7) is not converged, against the N = 11 reading.** 2-stem |q| = 1.904, 1.889, 1.863, **1.701** (N = 9–12): −9 % in the last step after
  −1 % steps. β = 6 keeps falling ~5 % per step (1.769 → 1.682); ε = 0.30, β = 3.5 jumps 1.641 → 2.123. Test 4b's "the smallest stem converges" was premature:
  three points of slow change were a plateau, not a limit. 3- and 4-stems at β = 7: median per-step |Δln|R|| 0.2–0.3 and 0.1–2.0, erratic.
- **Weak β, larger stems:** median phase change per step falls slowly (3-stems 0.030 → 0.023π, 4-stems 0.061 → 0.046π, N = 10 → 12); |R| static.
- **Verdict:** weak coupling: the drift is understood and dies faster than 1/N (first-order model, now tested by a prediction). Window: open, and N = 13 is out of
  reach (~2.5 TB). Exact enumeration is finished for this question; any further step needs sampling or the mean-field model.

## Log
- 2026-10-25 (session 3) — literature review on A2 and C8.
- 2026-10-25 — written after Roberto asked "have we fallen into full causal set theory?"
- 2026-10-25 (session 5) — A2 steps 1–3: links span most of the age; fixed-memory thick layers fail in the continuum phase; clock swap fails at the truncation level.
- 2026-10-25 (session 5) — option 2: truncating by events-between (n_cut = 10) gives 0.06 σ_S at N = 100–400; kept events ~ ln N but span the whole age.
- 2026-10-25 (session 5) — thick present: ∝ N in a diamond; ≈ 0.5 W² and age-independent in a closed space (memory ≈ half a light-crossing time).
- 2026-10-25 (session 5) — expanding closed universe: 90–98 % of the past stays needed; finite-state film killed for open or accelerating universes.
- 2026-10-25 (session 5) — FRW check: memory = W/2 of conformal time; finite iff no event horizon (decelerating yes, accelerating no).
- 2026-10-25 (session 6) — memory per static patch: finite and stationary, but ∝ ρ (spacetime-volume law, ≈ 3ρ events), not area law.
- 2026-10-25 (session 6) — A2 growth paths (all posets, N ≤ 8): covariant only unnormalized; KR-like 3-layer sector dominates at β = 0 and is suppressed in a β window (known result, new measure).
- 2026-10-25 (session 6) — memory per patch in d = 2, 3, 4: volume law (exponent ≈ 0.97); horizon surplus also volume law; 'shared with outside' diverges. Area law must be quantum, if anywhere.
- 2026-10-25 (session 6) — branch C: per-step normalization killed (violation grows, phases decohere); past stability fails inside the KR window at N ≤ 8 (warning).
- 2026-10-25 (session 6) — following the window: β*(N) erratic, past still unstable, PRESENT not matched; past stability ⇔ future factor F_N(stem) factorizes (next test).
- 2026-10-26 (session 7) — future factor F_N(stem) to N = 10 (exact, memoized): β = 0 ratio 3/(N+1); in the window the 2-element stem's ratio locks its phase (≈ π) by N ≈ 8–10, 3-element stems still moving; above the window erratic. Inconclusive, leaning hopeful.
- 2026-10-27 (session 8) — literature status of the F_N test (no one computes it; sum-rule models make it trivial; Surya–Zalel phase alignment); entanglement-entropy pointer for the quantum memory question; N = 11 submitted.
- 2026-10-27 (session 9) — quantum memory: SVD definition (bond dimension; F_N = row sums), stakes 10²⁴⁴ vs 10¹²², escape (i) dropped, objection to (ii); (ii) ⇏ (iii), memory ladder events → Cauchy data → area.
- 2026-10-27 (session 9) — rung-2 test: shuffling within light-cone cells scrambles what a newborn feels (raw: always; smeared: unless ≲ 2 ev/cell, worse with N). Classical coarse-graining fails.
- 2026-10-27 (session 10) — F_N at N = 11: the 2-stem converges in the window (|q| ≈ 1.87∠π); larger stems not; weak-β phase drift ∝ β × relations. Literature: F_N not found; 10²⁴⁴ vs 10¹²² is Sorkin's √N relation (0710.1675); rung 2 anticipated by Sorkin 2007.
- 2026-10-27 (session 10) — drift model: first-order mean future action explains the weak-β drift; decays faster than 1/N once N exceeds the non-locality scale (a = 1.5–3.3 for ε ≥ 0.35); prediction for N = 12.
- 2026-10-30 (session 16) — F_N at N = 12: weak-β drift prediction confirmed (N·d = 0.232 vs 0.233 ± 0.003); window 2-stem not converged after all.
