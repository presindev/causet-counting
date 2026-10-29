# 007 — Quantum indeterminacy as the universe's memory saving

**Status:** seed
**Started:** 2026-10-27   **Last touched:** 2026-10-27

## The intuition (in plain words)
Roberto (session 9): if the universe is a computer, storing every link between events is too expensive (10²⁴⁴ events per Hubble patch vs a
10¹²² entropy budget, idea 004). What if the links are *not all determined*, precisely because nothing stores them, and that's why they are quantum?
Quantum mechanics as a "smart memory system": reality doesn't keep positions and velocities of every molecule. It gives a reason for C8 (links are quantum).

## Thought experiment(s)
A storyteller who never decides details nobody will ever ask about: those details stay open (summed over) instead of written down.

## Closest existing physics
- `[established]` Storing a probability distribution (or a wavefunction) over n bits takes ~2ⁿ numbers; one microstate takes n bits. So "probabilities are
  cheaper to store" is false as stated. Holevo: n qubits yield at most n classical bits.
- `[established]` Variables that are summed over (path integral) or integrated out (Wilsonian RG) need no storage: only their net effect survives,
  as an effective action for the coarse variables. This is the precise form of "not determined, therefore not stored".
- `[literature]` Gu–Wiesner–Rieper–Vedral, Nat. Commun. 3, 762 (2012): quantum models of a stochastic process can need less memory than the best classical one.
- `[literature]` Zeilinger, Found. Phys. 29, 631 (1999): "an elementary system carries one bit"; finiteness of information as the root of quantum randomness
  and entanglement (Brukner–Zeilinger programme). It limits what a state says about outcomes, not a storage budget of the universe.
- `[literature]` Spekkens, PRA 75, 032110 (2007): a classical toy with a "knowledge balance" restriction reproduces interference, entanglement-like features,
  no-cloning, teleportation, but not Bell violations or contextuality.
- `[literature]` (abstract-level only) Caticha 2003 (quant-ph/0307121); Zilly 2026 (arXiv 2603.11900, single-author preprint, unreviewed): QM from finite
  information resolution. A web search (2026-10-27, brief) found **no work deriving QM from a storage limit of the universe itself**.

## Simple math
Past–future matrix (`sims/r3_memory_svd.py`, output `sims/out/r3_N7.txt`) `[ours]`: $B_{pF}=\sum_{\text{growths }p\to F}e^{i\beta\Delta S}$, p = unlabelled past
after k births, F = final universe at N. Classical memory C = log₂(#distinct rows), quantum Q = log₂(rank), Q_eff = entropy of normalized singular values (rows unit norm).
Validated: row sums = F_N(p) of `a2_future_factor.py`.
- **Structural result:** $\Delta S=S_F-S_p$ is path independent, so $B={\rm diag}(e^{-i\beta S_p})\,{\rm Count}\,{\rm diag}(e^{i\beta S_F})$. **With an endpoint-only action,
  phases cannot change any memory measure** when the future is the full final universe. Phases matter only if the outcome is a coarse *record* (many F with
  different $S_F$ in one column) or if amplitudes depend on the path.
- **Record = (height, #min, #max, #links) of F**, N = 7 (230 records), ε = 0.21. Rank stays full (= #pasts) for all β. Q_eff (bits):

  | k (pasts) | full F, any β | record β = 0 | β = 4 | β = 7 | β = 8 | β = 12 | random phases |
  |---|---|---|---|---|---|---|---|
  | 3 (5) | 1.99 | 1.45 | 1.47 | 1.52 | 1.54 | 1.62 | 2.10 |
  | 4 (16) | 3.71 | 2.57 | 2.63 | 2.74 | 2.79 | 3.00 | 3.77 |
  | 5 (63) | 5.79 | 3.78 | 3.88 | 4.05 | 4.12 | 4.45 | 5.34 |

  Reading: the coarse record compresses (classically, escape (ii)); the phases then *add* effective memory back, growing with β toward the random ceiling.
  At this size, with this record and an unweighted entropy, quantum interference does not save memory relative to β = 0 counting. Caveats: N = 7; 230 records > #pasts,
  so rank can't drop; β = 0 is counting, not a fitted classical stochastic rival; rows weighted equally.

## Record = collapse (Roberto, session 9) and its consequences
- Roberto: links/chains are undetermined; when they collapse and become determined, *that* is a record. Penrose–Diósi gravity-triggered collapse as the trigger.
- Consequence `[ours]`: memory accounting flips. Undetermined links cost nothing (summed over); every collapse creates a determined fact that must be stored.
  **Memory per patch = number of collapses (records) per patch.** The area-law hope becomes: collapses per Hubble patch ∝ horizon area (not volume).
  Collapse must be rare compared with births (10¹²² records vs 10²⁴⁴ events per patch in 3+1, if ℓ ≈ ℓ_P).
- Needed to avoid circularity: a *rule* for when collapse happens. DP-like candidate: alternatives collapse once they differ by enough (spacetime volume /
  action / number of differently related events); the threshold would be a parameter.
- `[literature]` Diósi–Penrose: superposed branches curve spacetime differently → collapse. Donadi, Piscicchia, Curceanu, Diósi, Laubenstein, Bassi (Gran Sasso,
  Nature Physics; Physics World coverage Oct 2020; arXiv 2111.13490): excludes the parameter-free version (effective mass-density size ≳ 1 Å). Versions
  with a free size parameter survive.
- `[literature]` Tumulka, "A relativistic version of the GRW model", quant-ph/0406094 (J. Stat. Phys. 125, 821 (2006), citation via lecture slides): the
  primitive ontology is a discrete random set of spacetime points where collapses happen ("flashes"); nonlocal but no preferred foliation (C4-friendly).
  Close to us: *events as collapses*. Not yet read beyond the abstract (lesson 16).

## Session 9, round 2: which version, and a trigger without "different enough"
- Roberto prefers **events exist first, some links collapse later**, keeping open that events are undetermined too (that's the full sum over causal sets;
  version 2 is a special case of it).
- Roberto dislikes any trigger of the form "alternatives differ enough". Note: DP is a *rate* (τ ~ ħ/E_G), not a threshold, but it still needs a scale.
  A tempting "discreteness sets DP's size cutoff R₀ ≈ ℓ" `[ours]` is **excluded** if collapse is sourced by ordinary mass density (Gran Sasso: R₀ ≳ 1 Å; a smaller
  R₀ means *faster* collapse and more radiation).
- **Parameter-free candidate** `[ours]`: a link becomes a record when its alternatives can **never interfere again**, i.e. their future rows in $B$ are
  orthogonal. No threshold, and computable in `r3_memory_svd.py`. Memory = number of mutually orthogonal sectors (each needs its own classical slot), while
  overlapping rows can share quantum memory. Closest literature: decoherent / consistent histories (Gell-Mann–Hartle; records) and Sorkin's quantum measure
  theory (decoherence functional, interference term $I_2$) `[literature]` (Sorkin 1994 MPLA details unverified; framework confirmed via 0906.0294).
  Caveats: (1) in practice orthogonality is approximate (exponentially small overlaps), so "enough" can sneak back unless a finite universe (C3) makes it exact;
  (2) this is decoherence (no outcome picked), not collapse. The memory accounting is the same either way; whether an outcome is "picked" is a separate question.
- Does the approach depend on the Gran Sasso result? Only if the trigger is gravitational and sourced by matter's mass density. Any *physical* collapse leaves
  traces (spontaneous heating/radiation) that bound its rate. A decoherence-defined record doesn't (it reproduces QM exactly).

## Test: orthogonal sectors ("can never interfere again"), session 9 `[ours]`
`sims/r3_memory_svd.py` (output `sims/out/r3_N7_sectors.txt`), N = 7. Sector = connected component of pasts whose future rows overlap (|⟨row_i,row_j⟩| > tol).
- **Exact criterion (tol = 0): always 1 sector**, for k = 3–6, every β, random phases, full-F or record futures. No past ever becomes a record: any two small
  pasts can still sit inside a common future universe and interfere there.
- With a tolerance, sectors appear only at k = 6 (one birth left): 32 (full F, tol 0.1), 3 (record). That's the future running out, not record formation, and it
  depends on the tolerance ("enough" sneaks back).
- k = 6, record future: rank 158 (β = 0) → 177 (β = 7, 12) → 190 (random) vs 302–318 distinct rows. Rank < rows only because there are 230 records < 318 pasts;
  phases again *raise* the rank.
- **Reading:** with an open future and "which poset came first" as the alternatives, the parameter-free criterion yields no records; in a finite universe it
  becomes exact only at the end (C3). Two suspects: (1) the alternatives are not covariant (birth order is gauge; the covariant questions are stems, Brightwell et al.);
  (2) with the full final universe as the "screen", covariant alternatives (sets of final universes) are trivially decoherent. **What counts as the screen decides
  everything:** that's lesson 3 again, now the core of idea 007.

## Screen = what events see (session 9) `[ours]`
- **On paper:** if every event sees its whole past exactly, everything inside any future event's past is a record, and only the unseen frontier stays undetermined
  ⇒ volume law, no quantum saving. A saving needs events that see their past *partially*, so the screen is what events actually store.
- **Test** `sims/r4_screen.py` (outputs `sims/out/r4_N7.txt`, `r4_N8.txt`): alternatives = universe after k births; screen = what the last newborn sees of its
  past at three resolutions (full poset / (size, #links) / #links). Decoherence functional, coherence c = mean |G_ij| (0 = records, 1 = undetermined).
  N = 8, k = 5 (63 alternatives):

  | screen | β = 0 | β = 8 | random phases |
  |---|---|---|---|
  | full (2451 views) | 0.55 | 0.21 | 0.15 |
  | coarse (29 views) | 0.75 | 0.38 | 0.22 |
  | links (8 views) | 0.97 | 0.72 | 0.49 |

  Same pattern at N = 7, k = 3–5. Never an exactly decohered pair. Coherence is non-monotonic in β: lowest near β ≈ 7–8 (the session 6 KR-suppression window),
  higher again at β = 12.
- **Reading:** (1) the coarser the screen, the more stays undetermined. That's the main memory saving, and it's classical (β = 0 has no interference).
  (2) **Phases decohere**: interference makes alternatives *more* distinguishable, so it creates records and costs memory (Q_eff rises). So far QM acts as
  a record-*maker*, not a memory-*saver*. Not yet supported: "quantum saves memory". Caveats: N ≤ 8 (≈ 4 layers); alternatives are first-k universes (not
  covariant); one observer (the last newborn); pairs weighted equally.

## Caveat 2: decoherence vs picking (session 9 discussion)
- Correction to the earlier remark ("the accounting is the same either way"): it is the same *per history* (records in one branch) but not *globally*. With no picking
  (many-worlds-like), the universe's state holds all branches, so its memory grows with the branch count. **"QM as memory saving" needs one history to be real**:
  either physical collapse (GRW/DP: modifies QM, needs a rate/scale) or a single-history reading of decoherent histories (Sorkin's quantum measure: no change to
  the dynamics, no threshold). Roberto's instinct (collapse) fits; Sorkin's version is the threshold-free option.
- Open tension: whatever carries the dynamics forward (e.g. the wavefunction in GRW-flash) is itself memory; the saving must show up as a small rank of $B$.

## Predictions / what would distinguish it
-

## Objections & tensions
- Storage vs summation: the saving must come from summing (interference), not from "storing probabilities". Session 9 classical result (idea 004, rung 2):
  with Lorentz-invariant (BD-type) dynamics, coarse cell counts do *not* capture what a newborn feels, and get worse as the universe grows. So classical
  coarse-graining doesn't compress; summing over micro links is the remaining route.
- Quantum phases feel *absolute* micro differences (δS ~ 1 shifts the phase), whereas stat mech only cares about relative fluctuations. Micro details either
  get summed over or they matter. There's no "averaging away" for amplitudes.
- Bell/contextuality: an epistemic-restriction story (Spekkens) can't reproduce them; ours must be genuinely quantum, not ignorance of hidden links.

## Open questions
- Which links are "never asked about"? Needs a definition of record (lesson 3); ties to escape (ii)/(iii) in idea 004.
- Does summing over a newborn's link choices (C8) reduce the singular-value count of M below the classical count?


## Session 10: deeper literature
- Not found as stated (indeterminacy because nothing stores the alternatives). Closest logic: Gisin 1803.06824; Del Santo–Gisin 1909.03697 (finite information density
  ⇒ indeterminism, even classically, but nothing about interference). Halliwell quant-ph/9902008: bits describing decoherent histories ≈ bits sent to the environment, i.e.
  records cost storage. That matches our "QM makes records".
- One real history: Sorkin's co-events / anhomomorphic logic (quant-ph/0610204, quant-ph/0703276; Ghazi-Tabatabai 1303.4729). This is the developed form of what Roberto picked.
- Collapse on causal structure: Dowker–Henson quant-ph/0209051, Dowker–Herbauts quant-ph/0401075 (1+1 null lattice). Never run on random or grown causal sets → ROADMAP N2.
- Area: Bousso–Susskind 1105.3796 (dim H ≤ e^{A/2} per diamond ⇒ decoherence never exact, which is our "no exactly decohered pair" in spirit). Banks' holographic space-time
  (1311.0755): log dim H = A/4 per causal diamond, the closest framework to "area-law memory per diamond" → ROADMAP N3.
- Memory tools: Yang–Binder–Narasimhachar–Gu 1803.08220 (quantum memory = past/future entanglement; MPS optimal). Not yet applied to growth (ROADMAP N5).

## Log
- 2026-10-27 (session 10) — deep literature: Gisin/Del Santo, Halliwell, co-events, Dowker–Henson collapse lattices, Bousso–Susskind, Banks HST.
- 2026-10-27 — screen test: coarser screens keep coherence (classical); phases decohere (make records), strongest at β ≈ 7–8. Roberto: picking via option 3 (Sorkin), maybe 2.
- 2026-10-27 — sectors test: exact orthogonality never happens (1 sector) with an open future; caveat 2 matters globally (needs one real history).
- 2026-10-27 — version 2 chosen (links collapse later); parameter-free record = orthogonal futures (decoherent-histories-like).
- 2026-10-27 — record = collapse (Roberto); memory = number of collapses; DP status (parameter-free excluded); Tumulka flashes.
- 2026-10-27 — first test: endpoint-only phases can't change memory; with a coarse record, phases add effective memory (N = 7).
- 2026-10-27 — seed, from Roberto's reformulation during the quantum-memory discussion (session 9); first literature pass.
