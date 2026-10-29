# 006 — Matter as a sum over chains (first actor for roadmap B)

**Status:** exploring
**Started:** 2026-10-26   **Last touched:** 2026-10-27

## The intuition (in plain words)
Roberto (session 7) asked what an "event" in our model really is. Is a scattering process one element? Two elements colliding? Two chains
(the trajectories of particles A and B) merging into one element? He also proposed that a classical particle's trajectory x(t) is a chain, and
asked what a wavefunction φ(x, t) is in this picture. It isn't a trajectory. Is it the *memory*, the thing that tells us the possible futures?

## Thought experiment(s)
- A proton–proton collision in a region about 1 fm across, lasting about 1 fm/c. How many elements does it involve?
- A free classical particle between two events: which of the very many chains connecting them is "the" trajectory?

## Closest existing physics
- **An element is not a lab event** `[literature]` (causal set theory). It is an atom of spacetime volume, about one Planck 4-volume. A fm-scale collision
  covers (10⁻¹⁵ / 1.6×10⁻³⁵)⁴ ≈ (6×10¹⁹)⁴ ≈ 10⁷⁹ elements. So a scattering process is none of the three options: particles are excitations of a field
  living *on* the elements, not the elements themselves. Our model so far has the stage (causal order) but no actors.
- **A chain is not special by itself.** Between two related elements there are astronomically many chains. Something extra must single out a
  trajectory.
- **Classical free particle = the longest chain** `[literature]` (Brightwell & Gregory, PRL 66, 260 (1991); idea from Myrheim 1978). The longest chain
  between two elements measures their proper time (× a constant depending on d; 2 in 1+1, per secondary sources). A free particle maximises proper
  time, so the order alone picks out the classical trajectory.
- **Quantum particle = sum over all chains** `[literature]` (Johnston, CQG 25, 202001 (2008), arXiv:0806.3083; thesis arXiv:1010.5514). See Simple math.
  The classical trajectory comes back as the dominant chain (stationary phase), as in Feynman's path integral.
- **ψ is the memory** `[established]`: in standard QM the state ψ(t) is exactly the sufficient statistic of the past for predicting the future. Given
  ψ(t), the rest of the past is irrelevant. Caveats: ψ gives *amplitudes* for futures; probabilities need a record (lesson 3). Sorkin's quantum measure
  approach starts without ψ (amplitudes on whole histories), so there ψ must be derived.
- Correction to the classical picture: a Newtonian particle doesn't need its whole chain. Position + velocity now (about the last two links) is enough.

## Simple math
**Johnston's recipe (1+1)** `[literature]`, eqs. 3.1, 3.5, 3.31 of arXiv:0806.3083:
- A trajectory from x to y with n hops (each along *any* causal relation, not only links) and n − 1 stops has amplitude aⁿ bⁿ⁻¹.
- 1+1: a = 1/2, b = −m²/ρ (ρ = element density, V₀ = 1/ρ). 3+1: hops go along **links** only, a = √ρ/(2π√6), b = −m²/ρ, and agreement holds
  only as ρ → ∞.
- Sum over all trajectories: with Φ = a C (C[x,y] = 1 if x ≺ y), K = Φ + bΦ² + b²Φ³ + … = Φ (I − bΦ)⁻¹ (geometric series; the identity term is dropped).
- Target: the retarded Klein–Gordon propagator, (□ + m²) K = δ, which in 1+1 is K(x,y) = ½ J₀(m τ_xy) for x ≺ y, else 0.

**Why it works, in one line** (our re-derivation, checks the paper): in 1+1 the expected number of chains x ≺ z₁ ≺ … ≺ z_k ≺ y is
(ρ τ²/2)^k / (k!)² (k ordered points in an interval of area τ²/2). So

  E[K] = a Σ_k (a b ρ τ²/2)^k / (k!)² = ½ Σ_k (−(mτ/2)²)^k / (k!)² = ½ J₀(mτ).

This is exactly the power series of J₀. It also shows that m = 0 is trivial (K = a C = ½ for every related pair, on every causal set). Only m > 0 tests
anything.

**Our check** `[ours]` (`sims/b_johnston_propagator.py`, 2026-10-26). We sprinkle a 1+1 diamond, insert the bottom tip by hand (lesson 9), and compute
the row K[tip, ·] by one linear solve. We compare it with ½J₀(mτ) in τ bins. Errors are the spread of bin means across independent seeds (lesson 8).
- m = 0: exact (0 deviation), as expected.
- m = 1, ρ = 100, T = 8 (N ≈ 3200, mτ up to 8, through two zeros of J₀): mean deviation |⟨K − G⟩| ≤ 0.01, within one seed sd (0.002–0.018).
  The curve follows J₀ through its sign changes.
- Fluctuations vs density (m = 1, T = 4, 12 seeds; seed sd near mτ ≈ 2.4): ρ = 25 → 0.035, ρ = 100 → 0.020, ρ = 400 → 0.0075. That's roughly
  ρ^(−1/2) to ρ^(−0.7). Johnston's "fluctuations decrease with density" is confirmed qualitatively.
- Heavier mass (m = 3, ρ = 100, m²/ρ = 0.09, about 11 elements per 1/m²): the mean is still right, but single-causet scatter is 0.03–0.05
  against |G| ≤ 0.15. The propagator needs m²/ρ ≪ 1, i.e. many elements per Compton area.
- Within one causal set the deviation is correlated across elements: the seed spread of bin means is about as big as the per-element scatter. So
  a single causal set's propagator is "off by a smooth shift", not by independent noise.

### Test on the N = 400 MCMC universes (session 7, `sims/b_johnston_n400.py`) `[ours]`
- On any causal set, $K(x,y) = \tfrac12\sum_k c_k(x,y)\,(-\mu/2)^k$ with $\mu = m^2/\rho$ and $c_k$ the number of $k$-element chains strictly inside
  $[x,y]$. Only $\mu$ enters: no density has to be fitted.
- Exact intrinsic target for a random 2D order: the $n$ elements of an interval are again a random 2D order, and $k$ of them form a chain with
  probability $1/k!$, so $E[c_k\,|\,n] = \binom{n}{k}/k!$ and
  $$E[K\,|\,n] = \tfrac12\sum_k \binom{n}{k}\frac{(-\mu/2)^k}{k!} = \tfrac12 L_n(\mu/2) \;\to\; \tfrac12 J_0\!\big(\sqrt{2\mu n}\big)\quad (n\gg1).$$
  ($n$ = interval size, counted from the order; $L_n$ = Laguerre polynomial.) **Literature status (session 8 review):** the pieces are known, but the assembled
  statement was not found. $E[c_k|n]=\binom nk/k!$ is the classical count of increasing subsequences of a random permutation (Pinsky 2006, eq. 1.1;
  Lifschitz–Pittel 1981) `[established]`; $\sum_k\binom nk x^k/k! = L_n(-x)$ is a textbook identity (OEIS A002720 has $x=1$); Johnston only gives the
  fixed-density (Poisson) average. "Laguerre" appears in none of the 13 causal-set full texts searched, and INSPIRE was not used. So: most likely an unremarked
  one-liner, `[ours]`, built from `[established]` parts.
- **Consistency with Johnston** (checked numerically, session 8): averaging over Poisson $n$ with mean $\lambda=\rho\tau^2/2$, the generating function
  $\sum_n L_n(x)z^n/n! = e^z J_0(2\sqrt{xz})$ (DLMF 18.12.14) gives $E_\lambda[\tfrac12 L_n(\mu/2)] = \tfrac12 J_0(2\sqrt{\lambda\mu/2}) = \tfrac12 J_0(m\tau)$
  exactly. Johnston's result is the Poisson average of ours; ours is the finer statement (it uses only the order, not a sprinkling density).
- **Better large-$n$ form** (DLMF 18.11.6, Mehler–Heine/Hilb type): $L_n(\mu/2)\approx e^{\mu/4}J_0\big(\sqrt{2\mu(n+\tfrac12)}\big)$, within $4\times10^{-4}$ for
  $\mu\le0.15$, $n<400$. The naive $\tfrac12J_0(\sqrt{2\mu n})$ is off by up to 0.003 / 0.009 in $K$ at $\mu$ = 0.05 / 0.15 (below our rms but
  systematic). Keep the exact $L_n$ as the target.
- **Other dimensions** `[ours]`, not yet worked out: at fixed $n$, $E[c_k|n]=\binom nk p_k$ still holds, with $p_k$ the probability that $k$ random interval points form a chain
  (from Meyer's closed form). It is Laguerre only in 2D.
- **Curvature** `[literature]`: Nomaan X–Dowker–Surya 2017 (eqs. 52–55) give $\tfrac12[J_0(m\tau)+(R\tau^2/48)J_2(m\tau)]$ in curved 2D. A curved interval is not
  a uniform 2D order, so our Laguerre target is flat-only; a $J_2$-shaped residual at fixed $n$ is a candidate curvature signature.
- Control (4 random 2D orders, N = 400): rms $(K - L_n/2)$ = 0.014–0.017 at $\mu = 0.05$, 0.042–0.049 at $\mu = 0.15$; the fraction of pairs with
  $K<0$ matches the target (0.26–0.28 / 0.46–0.48). Code checked against the explicit series ($10^{-13}$) and integer interval counts.
- **Continuum-like configurations** (hot starts at β ≤ 0.08, cold starts melted at β ≤ 0.05; 14 runs): indistinguishable from the control
  (rms 0.013–0.020 / 0.037–0.050; same $K<0$ fraction). Expected, since S/N ≈ 0 means they are typical random orders: a pass, not news.
- **Crystals** (β = 0.08 cold): s2036 (4 layers) has no interval larger than 9 elements, so $K$ never turns negative: no wave, mass meaningless.
  s2037 (7 layers) has intervals up to 93 and $K$ falls far below the target ($-0.22$ at $n$ = 50–75 for $\mu = 0.05$; $-1.43$ at $\mu = 0.15$):
  too many chains for the interval size.
- Assessment: the propagator separates the two phases, but for these extreme cases the layer count already does. Its value is on borderline
  universes (A2 growth samples, S1 percolation) where geometry is ambiguous. Next: run it there.

### Test on the S1 grown universes (session 7, `sims/b_johnston_grown.py`, N = 1500, μ = 0.05, 3 seeds each) `[ours]`
- Expanding in μ: $K/\tfrac12 = 1 - \tfrac{\mu}{2}n + (\tfrac{\mu}{2})^2 c_2 - \dots$, and a 2D interval has $E[c_2|n] = n(n-1)/4$ (ordering fraction ½).
  So the first order that can fail *is* the Myrheim–Meyer dimension; higher orders add longer chains. The propagator is a resummed tower of chain-count
  dimension tests, and it only asks "does a **2D** massive particle propagate here?".
- Control (random 2D orders): rms 0.024–0.030, $K<0$ fraction 0.47 (target 0.47), $d_{MM}$ of the largest intervals 2.00.
- **All S1 universes fail**, with nearly identical deviations across seeds (systematic, not noise). The deviation appears at n ≈ 25–50, i.e. once
  μn/2 ~ 1 and longer chains matter.
  - fixed p = 0.02 ($d_{MM}$ ≈ 1.5): $K$ falls below target by up to −0.59, then runs away; max|K| = 9–11, twenty times the 2D bound ½. No stable propagation.
  - fixed p = 0.05 ($d_{MM}$ ≈ 1.15, a thin tube): bounded, and $K$ changes sign as often as in 2D (0.47), but with the wrong shape (deviation −0.09 … +0.23).
  - p = 3/n ($d_{MM}$ ≈ 2.6–2.75, still growing): bounded but systematically below target (down to −0.58 at n = 200–500).
- Assessment: confirms S2 (grown universes aren't 2D) with a physical observable; new is the blow-up at p = 0.02. Not tested on A2: exact sums stop at N = 8
  (intervals ≤ 6, one J₀ oscillation needs n ~ 60), where the test reduces to the ordering fraction anyway.
- Limitation: the exact target exists only for 2D (Laguerre). A test in other dimensions needs Johnston's link-based version and its own target.

## Predictions / what would distinguish it
- Nothing new yet: this is a known construction. What's ours would be using it as a **probe of our grown causal sets**. Does a massive particle
  propagate correctly on them? Proposal below.

## Objections & tensions
- Johnston's own limits: only scalars; only the *retarded* propagator (no Feynman propagator, no pair creation); fixed background, no backreaction;
  in 3+1 only the ρ → ∞ limit with rescaled a, is shown; numerical checks preliminary.
- The 1+1 recipe uses all causal relations; the 3+1 one uses links. In 3+1, links from one element are infinite in number for a sprinkling
  (non-locality, our C3). On a finite universe that is regulated, but the amplitude will depend on the cutoff unless the sum cancels (lesson 18).
- C5: the propagator is built from the order alone (no clock), so it respects C2/C5. But it doesn't yet provide a *matter frame*. That needs a
  state (a wavepacket) and its rest frame.

## Open questions
- **Probe on grown causal sets** `[ours]`, intrinsic version: replace τ by the interval count, τ²_xy = 2 n_xy / ρ (n_xy = number of elements strictly
  between x and y), and ρ by N/V (unknown in a grown set → fit ρ as a free parameter, or define it as 1 element per unit volume). Test: does
  K(x,y) depend on (x,y) only through n_xy, and as ½J₀(m√(2n_xy/ρ))? Candidates: (i) N = 400 final 2D orders from job 449411 (hot = continuum,
  cold/crystal = layered); (ii) S1 percolation-grown universes; (iii) A2 growth-path samples. Expected failure modes: in layered (KR-like) sets chains
  have ≤ 3 hops, so K ≈ a(1 + b n + …) never oscillates and "mass" loses meaning. That makes it a *manifold detector with a physical meaning*.
  Percolation-grown sets weren't 2D-manifold-like in S2, so J₀ should fail there too; how it fails is the information.
- Is ψ on a slice (the sum over chains ending on a present antichain) a compressed memory of the past for the *matter* sector? Compare its size
  with session 6's volume-law growth memory (idea 004, quantum memory question).
- Interactions: two chain-sums meeting at an element, summed over elements, as a discrete Feynman vertex `[ours]`. **Session 8:** Johnston's thesis
  §5.4.2 considers exactly this (vertices summed over elements) and sets it aside as ambiguous (coincident vertices, self-loops, which diagrams count).
  §5.5 instead builds an operator theory: a φ⁴ term at each element, a Dyson series with the causal-set Feynman propagator, which he says "in general
  does not converge" `[literature]`. A chain-sum vertex would have to answer his ambiguity objection first.


## Session 10: INSPIRE crawl
All papers citing Johnston 0806.3083 and 0909.0944 (115 records; all 99 with arXiv IDs grepped in full text): no Laguerre form and no conditioning on n.
Hinrichsen–Kastrati 2604.24812 has k!-series without Laguerre. The identity Σ C(n,k)x^k/k! = L_n(−x) is combinatorics (OEIS A002720, Lifschitz–Pittel 1981).
→ Claim it as "a known identity applied to Johnston's propagator". The J₂ term at fixed n as a curvature estimator: not found (25 citers of 1701.07212 grepped).


## Session 10: curvature at fixed interval size (`sims/r6_curvature_fixed_n.py`, output `sims/out/r6_s2000.txt`) `[ours]`
- Setup: one 2D de Sitter diamond (H = 1), conditioned on n events inside. Light cones are flat in conformal coordinates and only the density (∝ 1/η²) is uneven, so the order depends
  on (n, Hτ) only, not on ρ. Flat control (Hτ = 0) reproduces C(n,k)/k! and ½L_n(μ/2) within ~2σ (2000 intervals per cell).
- **Curvature shifts the share of related pairs:** g₂ = E[c₂|n]/(C(n,2)/2) − 1 ≈ +0.027·(Hτ)² (2 × 10⁶ pairs: 0.0271 ± 0.0007 at Hτ = 1, 0.026 ± 0.003 at 0.5), the same for
  n = 10, 30, 60. g₃ ≈ 2.3 g₂. Close to (Hτ)²/36 numerically; not derived.
- **The propagator adds nothing beyond c₂:** intervals for a 3σ detection from K at the best μ vs from c₂ alone: 477 vs 487 (n = 10, Hτ = 1), 175 vs 175 (n = 30), 80 vs 82 (n = 60).
- **Verdict:** the "J₂ probe at fixed n" is the known chain-abundance route to curvature (Roy–Sinha–Surya) in disguise. **Dropped as a claim**; it stays as a consistency check
  (the Laguerre target is the right flat baseline, and curved intervals deviate from it in the expected direction).

## Session 11: is there a 3+1 fixed-$n$ target? (`sims/r10_4d_link_paths.py`, outputs `sims/out/r10_*.txt`)
- In 3+1 hops go along **links** (Johnston 2008): $K/a=\sum_k(-\nu)^{k-1}P_k$, $\nu=m^2/(2\pi\sqrt{6\rho})$, $P_k$ = number of $k$-hop link paths. A link path needs every
  skipped sub-interval empty, so $E[P_k\,|\,n]=\frac{n!}{(n-k+1)!}\,E\big[\mathbf 1_{\rm chain}\,(1-W/V)^{n-k+1}\big]$ ($W$ = total volume of the $k$ sub-intervals):
  a $(k-1)$-point integral, no $1/k!$-style closed form. The Laguerre exactness is a 1+1 fact (there the massless kernel is constant inside the cone, so all relations count).
- **Asymptotics of $P_2$** `[ours]`. Interval between $(\mp1,\vec0)$, $V=2\pi/3$. Large $n$: $z$ must sit near the waist sphere ($t\approx0$, $r=1-\epsilon$). With $p=\epsilon+t$, $q=\epsilon-t$:
  $V(x,z)/V\approx p^2/4$, $V(z,y)/V\approx q^2/4$, point density in $(p,q)$ = $(4\pi/2)/(2\pi/3)=3$. So
  $E[P_2\,|\,n]\approx3n\int_0^\infty\!\!\int_0^\infty e^{-n(p^2+q^2)/4}dp\,dq=3\pi$.
  Then $a\,\nu\,P_2\to\frac{\sqrt\rho}{2\pi\sqrt6}\cdot\frac{m^2}{2\pi\sqrt6\sqrt\rho}\cdot3\pi=\frac{m^2}{8\pi}$: exactly the short-distance limit of the continuum mass term $-(m/4\pi\tau)J_1(m\tau)$.
- **Monte Carlo**: $E[P_2|n]$ = 8.56 ± 0.11 (n = 300), 8.90 ± 0.16 (1000), 8.96 ± 0.23 (2000), 9.23 ± 0.29 (4000): consistent with $3\pi(1-c/\sqrt n)$, $c\approx1.6$.
  Longer paths reach their dimensional scaling $n^{(k-2)/2}$ only at $n\gtrsim10^3$ ($P_3$: ratio 1.40 from 1000 to 2000, expected 1.41).
- **Verdict**: a 3+1 fixed-$n$ target exists only as a computed table $T(n,\nu)$ (plus asymptotics), not a closed form. Not added to the Part I note beyond a corrected outlook sentence.
  My session-11 roadmap assessment ("use chain abundances") was wrong: it ignored that 3+1 uses links, which this file already said (lesson 31).

## Log
- 2026-10-26 — created from Roberto's "what is an event / is ψ the memory" questions (session 7). Johnston recipe extracted, re-derived (E[K] = ½J₀
  via chain counts), and validated on 1+1 sprinklings (`sims/b_johnston_propagator.py`). Proposal: use it as a probe on grown causal sets.
- 2026-10-26 — N = 400 test: continuum-like universes match the exact Laguerre target ½L_n(μ/2); crystals fail (no oscillation / far too many chains).
- 2026-10-27 — literature review (session 8): Laguerre target not found in the literature (pieces known); Poisson average reproduces Johnston's ½J₀ exactly; vertex idea already considered and set aside by Johnston (thesis §5.4.2).
- 2026-10-26 — S1 test: all grown universes fail the 2D propagator test (p = 0.02 runs away, |K| up to 10); μ-expansion = MM dimension at 2nd order.
- 2026-10-27 (session 10) — INSPIRE crawl: Laguerre form not found in 99 citers; present as known identity applied.
- 2026-10-27 (session 10) — fixed-n curvature: g₂ ≈ 0.027 (Hτ)², K no more sensitive than c₂ ⇒ J₂ probe dropped as a claim (known chain-count route).
- 2026-10-27 (session 11) — 3+1 fixed-n target: links break the closed form; $E[P_2|n]\to3\pi$ reproduces the continuum mass term $m^2/8\pi$ (MC confirms, $O(n^{-1/2})$ approach).
