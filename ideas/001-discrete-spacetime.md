# 001 — Discrete spacetime that looks continuous from far away

**Status:** exploring — core is **known** (causal sets); our addition = finite-universe cutoff η_max ≈ 142 +
cosmological frame (C3–C5). Crystal and positional blur dropped (see draft v2, App. A).
**Started:** 2026-10-24   **Last touched:** 2026-10-24

## The intuition (in plain words)
A continuous spacetime feels counterintuitive. Maybe spacetime is a discrete set of points plus
some structure such that, "looked at from far away" (a limit / coarse-graining), it behaves like a
smooth Lorentzian manifold: Minkowski when flat, GR in general, with finite signal speed $c$.
Proposed order of work: discrete model whose continuum limit is GR first, *then* quantize it.
The metaphor is Planck's move: "let's assume energy comes in quanta" → "let's assume spacetime does".

## Roberto's choices (session 1)
1. **Spacetime** is discrete: time ticks too.
2. **Regular, crystal-like lattice with some "quantum blurring"**, not a Poisson random sprinkling
   (random sprinkling feels too ad hoc). Likes causal-set ingredients "order" and "counting".
3. **Neighbour = information can pass from one point to the other in one time step.**
4. Fixed vs dynamical: open. If a fixed structure can *look* reshaped by matter from far away, fine.
   Asked: can points be created/destroyed?
5. **Curvature = point density.** A black hole = points packed so densely that information can't escape.
- Angles (and distances) may only make sense "from far away" — emergent, not fundamental.
- Lorentz invariance should be imposed as a *constraint* on the discrete model.

## Thought experiments
- **Crystal → wave equation.** A chain of masses and springs looks, at long wavelengths, like a string.
- **Weyl's tile argument (1949).** On a square grid the diagonal of an $n\times n$ square is $n$ tiles, not $n\sqrt2$.
- **Light cone of a crystal.** With "neighbour = one hop per tick", the set reached after $N$ ticks
  is the *light cone*. On a square lattice it is a diamond $|x|+|y|\le N$ → light along the diagonal
  is $1/\sqrt2$ slower. Hexagonal lattice → hexagon → $c$ varies by $\cos 30^\circ \approx 0.87$ with direction.
  Ruled out by Michelson–Morley-type tests by many orders of magnitude.
- **The boosted crystal.** A lattice has a rest frame → preferred frame (aether).

## Closest existing physics
- `[established]` Continuum mechanics/hydrodynamics as limits of atomic systems.
- `[literature]` **Causal sets** (Bombelli–Lee–Meyer–Sorkin 1987): random sprinkling + causal order. "Order + Number = Geometry".
  Points *are* created: classical sequential growth (Rideout–Sorkin 2000) — time passing = new points being born.
- `[literature]` Regge calculus, CDT, LQG (discreteness derived), graph models.
- `[literature]` **Analog gravity** (Unruh 1981): sound in a flowing fluid obeys a wave equation in a curved
  "acoustic metric"; sonic horizons. A *fixed* medium can look curved to waves — answers Roberto's Q4
  for kinematics, not for Einstein's equations (what makes the medium flow that way?).
- `[literature]` **River model** (Hamilton–Lisle 2008): Schwarzschild = flat space + space flowing inward
  at Newtonian escape velocity $v=\sqrt{2GM/r}$; horizon where $v=c$, i.e. $r=2GM/c^2$. Exact GR (Gullstrand–Painlevé).
- `[literature]` Jacobson 1995: Einstein equation as thermodynamic equation of state.
- `[established]` Weak-field gravity acts on light like a refractive medium, $n\approx 1+2GM/(rc^2)$ (Shapiro delay, lensing).

## Simple math
### 1D lattice → wave equation
$m\ddot u_n=\kappa(u_{n+1}-2u_n+u_{n-1})$; Taylor ⇒ $\ddot u=c^2u''+\tfrac{c^2a^2}{12}u''''+\dots$, $c^2=\kappa a^2/m$.
Exact: $\omega=\tfrac{2c}{a}|\sin\tfrac{qa}{2}|\approx cq[1-(qa)^2/24]$, $v_g=c\cos(qa/2)<c$.

### Regular lattices never give round circles
Burago: any periodic metric on $\mathbb R^n$ (e.g. a lattice with step-counting) rescales to a **norm**;
for word metrics on $\mathbb Z^d$ the unit ball is the convex hull of the generating steps → a polygon.
Random (Poisson–Voronoi/Delaunay) graphs: first-passage limit shape is an exact **Euclidean ball**
(Vahidi-Asl & Wierman) — randomness buys isotropy.

### Why Lorentz-invariant discreteness is nonlocal (1+1D, $c=1$)
"One-step neighbours" of the origin = future points with proper time $0<\tau<\varepsilon$:
$0<t^2-x^2<\varepsilon^2$, $t>0$. Light-cone coords $u=t-x$, $v=t+x$ ⇒ $t^2-x^2=uv$, $dt\,dx=\tfrac12du\,dv$.
$$A=\tfrac12\int_0^\infty du\int_0^{\varepsilon^2/u}dv=\tfrac{\varepsilon^2}{2}\int_0^\infty\frac{du}{u}=\infty$$
(Euclidean analogue: $\pi\varepsilon^2$, finite.) Any uniform density of points ⇒ infinitely many nearest neighbours.

**Visual intuition** (interactive: `viz/neighbour-sliver.html`, https://claude.ai/artifact/TDEMbTo9a6H2j68pXYKBdf):
- Sliver height at distance $x$: $\sqrt{x^2+\varepsilon^2}-x\approx \varepsilon^2/(2x)$ — thins like $1/x$, like the harmonic series.
- Exact area within $|x|\le X$: $X\sqrt{X^2+\varepsilon^2}-X^2+\varepsilon^2\ln\frac{X+\sqrt{X^2+\varepsilon^2}}{\varepsilon}\approx \varepsilon^2/2+\varepsilon^2\ln(2X/\varepsilon)$.
- Coords $(\tau,\eta)$: $u=\tau e^{-\eta}$, $v=\tau e^{\eta}$ ⇒ $dt\,dx=\tau\,d\tau\,d\eta$ ⇒ each unit of rapidity holds area $\varepsilon^2/2$.
  Boosts shift $\eta$, so the sliver is infinitely many boost-copies of one band.

### "Exactly one tick" instead of "at most ε" (Roberto's objection)
The dichotomy survives every reading of "neighbour = one tick":
1. **Random points, exact proper time ε:** the hyperbola has zero area ⇒ almost surely no neighbours.
   Natural discrete version = causal-set **link**: $x$ is a neighbour of the origin if no other point lies
   causally between them (empty Alexandrov interval, area $\tau^2/2$ in 1+1). Poisson ⇒
   $P(\text{link})=e^{-\rho\tau^2/2}$. With $dA=\tau\,d\tau\,d\eta$:
   $$\langle N_{\rm links}\rangle=\int d\eta\int_0^\infty \rho\,\tau\,e^{-\rho\tau^2/2}\,d\tau=\int d\eta\cdot 1=\infty$$
   **Exactly one expected link per unit of rapidity**, no arbitrary ε needed. Infinite valency is standard
   in the causal-set literature.
2. **Square lattice $\mathbb Z^2$, exact:** $t^2-x^2=k$ ⇔ $(t-x)(t+x)=k$ ⇒ finitely many solutions.
   For $k=1$ only $(1,0)$: "stay put". Moving hops $(1,\pm1)$ are null (proper time 0) — cf. Feynman's
   checkerboard (Dirac eq. from a particle zig-zagging at $c$ on a 1+1 lattice). Finite, but no boost symmetry.
3. **Lattice with discrete boost symmetry** (Schild 1948: integral Lorentz transformations of $\mathbb Z^4$).
   2+1 example, metric diag(1,−1,−1): $\Lambda=\begin{pmatrix}3&2&2\\2&1&2\\2&2&1\end{pmatrix}$ preserves
   $t^2-x^2-y^2$ with integer entries ($\cosh\eta=3$). Orbit of $(1,0,0)$: $(3,2,2),(17,12,12),\dots$ ⇒
   infinitely many points at *exactly* one tick. Any boost symmetry, even discrete, ⇒ infinite valency.

### Quantum-blurry points and "exactly one tick" (Roberto, session 1)
Roberto: if points are quantum-blurred, the probability of lying on the hyperbola is not 0.
- With a continuous probability density it still *is* 0 (a curve has zero area — like a dart hitting
  exactly a line). What is nonzero is the *density* on the curve; to turn it into a count one integrates
  over a band ⇒ the blur width σ becomes the band thickness. **Gain:** a physical origin for the ad hoc ε-band.
- Count still diverges: (a) blur round in the lattice frame (not Lorentz-invariant) ⇒ band of fixed
  Euclidean width along an infinitely long curve ⇒ area grows ~linearly in $X$ (worse than log);
  (b) Lorentz-invariant blur (depends only on proper time) ⇒ ≈ $2\varepsilon\sigma$ area per unit rapidity ⇒ log divergence.
- Stronger version `[ours]`: **one** neighbour in superposition over rapidity bands,
  $|\text{nb}\rangle=\sum_k c_k|k\rangle$. Boost invariance ⇒ all $|c_k|$ equal ⇒ $\sum_k|c_k|^2=\infty$: not normalizable.
- **Recurring wall (3rd appearance): normalizable ⟂ boost-invariant.** Rotations compact, boosts not.
- Possible escape `[ours]`/`[literature]`: QM already uses non-normalizable idealizations (plane waves).
  Laws boost-invariant, *state* not ⇒ **spontaneous Lorentz breaking** (crystal analogy: translation-invariant
  laws, non-invariant crystal). Literature: Kostelecký–Samuel 1989; Einstein-aether (Jacobson–Mattingly 2001).
  Natural candidate frame: CMB rest frame. This is option A with a mechanism; must face Lorentz-violation bounds.

### Analogy: atomic absorption and linewidth `[established]`
"Exact energy" absorption would have probability 0, like "exactly on the hyperbola". Nature avoids it because
neither the level nor the photon is sharp. A level with lifetime $\tau$ decays as
$\psi(t)=e^{-i\omega_0 t-\Gamma t/2}$ ($t>0$, $\Gamma=1/\tau$); Fourier transform ⇒
$|\tilde\psi(\omega)|^2\propto \frac{1}{(\omega-\omega_0)^2+\Gamma^2/4}$ (Lorentzian, FWHM $\Gamma$).
Absorption rate $=\int\sigma(\omega)I(\omega)\,d\omega$: a density integrated against a density ⇒ finite.
H 2p: $\tau\approx1.6$ ns ⇒ $\Gamma/2\pi\approx100$ MHz vs $2.5\times10^{15}$ Hz (relative $\sim4\times10^{-8}$).
Extra broadening: Doppler, collisions, finite photon pulse duration.
**Transfer to 001:** blur cures "probability zero" exactly as linewidth does. It does *not* cure the
infinity, because the energy line is a point on a 1D axis (finite after smearing) while the hyperbola is an
infinitely long curve. Note the width comes from *dynamics* (coupling to the radiation continuum), not from
fundamental fuzziness — maybe blur of spacetime points should also come from interactions.

### Finite universe as a cutoff (Roberto, session 1)
A finite universe (size $L$) cuts the rapidity conveyor belt: a link at proper time $\tau$ and rapidity $\eta$
sits at distance $r=\tau\sinh\eta\approx(\tau/2)e^{\eta}\le L$ ⇒ $\eta_{\max}\approx\ln(2L/\tau)$.
With $L\approx4.4\times10^{26}$ m, $\tau\sim\ell_P=1.6\times10^{-35}$ m: $L/\ell_P\approx2.7\times10^{61}$, $\eta_{\max}\approx142$.
- **1+1:** 1 link per unit rapidity ⇒ $\approx2\eta_{\max}\approx 280$ future links per point. Small (log!).
- **3+1:** $d^4x=\tau^3\sinh^2\!\eta\,d\tau\,d\eta\,d\Omega$, Alexandrov volume $\pi\tau^4/24$, $P(\text{link})=e^{-\rho\pi\tau^4/24}$.
  $\int\sinh^2\eta\,d\eta\,d\Omega\approx(\pi/2)e^{2\eta_{\max}}=(\pi/2)(2L/\tau)^2$ ⇒
  $N\approx2\pi\rho L^2\int_0^\infty\tau e^{-\rho\pi\tau^4/24}d\tau=\tfrac{\pi}{2}\sqrt{24}\,(L/\ell)^2\approx7.7\,(L/\ell)^2\sim10^{124}$.
  Finite but huge: exponential growth of the hyperboloid (vs linear in 1+1).
- **Catch 1 — preferred frame again, but cosmological:** a finite (compact) universe has a global rest frame
  (Barrow & Levin 2001, twin paradox in compact spaces); we already have one (CMB / comoving frame).
  Lorentz invariance would hold for rapidities ≪ 142. Highest tested: ~$3\times10^{20}$ eV cosmic-ray proton,
  $\gamma\sim3\times10^{11}$, $\eta\approx27$. `[ours]` reframing: Lorentz symmetry exact up to $\eta\sim\ln(L/\ell_P)$.
  Literature search (session 1, extended) found **no direct statement** of this; neighbours: minimum/maximum-length
  QM, de Sitter relativity (to check). Keep as `[ours]`, search again with other keywords.
- **Catch 2 — finite ≠ local:** the links lie near the light cone, out to cosmological distances. A point here
  is "one tick" from events billions of light-years away along light rays (emission/absorption of a photon are
  nearly null-separated). Nonlocality becomes *light-cone-shaped*, not arbitrary.
- **Numerology warning:** $(L/\ell_P)^2\sim10^{122}$ is also the cosmological-constant ratio — but every
  dimensionless combo of $L$ and $\ell_P$ is a power of $10^{61}$. Not evidence by itself (Sorkin's Λ argument uses
  a related counting, $\Lambda\sim1/\sqrt V$, to verify).

### Toy model: blur generated by coupling (quantum chain) — `sims/quantum_chain_blur.py`
Chain of $N$ masses $m$, springs, spacing $a$, periodic. Normal modes $q_k=2\pi k/(Na)$, $\omega_k=(2c/a)|\sin(q_ka/2)|$.
Each mode = harmonic oscillator; ground state $\langle Q_k^2\rangle=\hbar/(2m\omega_k)$. With $u_n=N^{-1/2}\sum_k Q_ke^{iq_kna}$:
$$\sigma^2\equiv\langle u_n^2\rangle=\frac1N\sum_{k\ne0}\frac{\hbar}{2m\omega_k}\approx\frac{\hbar a}{2\pi mc}\sum_{k=1}^{N/2}\frac1k\approx\frac{\hbar a}{2\pi mc}\ln N$$
(small-$k$ modes dominate; harmonic series again). Numerics (ħ=m=a=c=1): $\sigma^2-\ln N/2\pi\to0.0200$ for
$N=10\ldots10^6$. Relative blur $\langle(u_{n+r}-u_n)^2\rangle\approx\ln r/\pi+0.625$ ($=2/\pi$ at $r=1$).
3D cubic lattice: $\sigma^2$ saturates (≈0.2276) — finite.
- **Correction (later in session 1):** blur is *not* "produced by coupling" in the sense "isolated = sharp". In this
  chain an isolated point is a free particle and is *infinitely* blurry; with an on-site pin $\omega_0$, coupling
  actually *reduces* blur ($\omega_k\ge\omega_0$). What the model shows is weaker: the blur is a **collective**
  property, set by the spectrum of modes the point is coupled to (system size, dimension), as the linewidth is set by
  the field modes the atom is coupled to. The Lorentzian line shape itself is not reproduced. A faithful analogue
  would be a probe point weakly coupled to the chain as a bath (Caldeira–Leggett-type) — not done.
- Neighbours are sharply placed relative to each other; absolute position blur grows ~ $\ln$(system size) in 1+1
  (no true long-range crystalline order in 1D — Peierls/Mermin–Wagner type).
- If $\hbar/(mc)=a=\ell_P$: $\sigma\approx\ell_P\sqrt{\ln(L/\ell_P)/2\pi}\approx4.7\,\ell_P$ for the whole universe.
- `[ours]` same $\ln(L/\ell_P)$ as the rapidity cutoff $\eta_{\max}$; both from the scale-free $1/k$ of massless 1+1 fields.
  Probably no deeper meaning, but noted.
- The zero-point energies $\tfrac12\hbar\omega_k$ here are the same thing that causes the cosmological constant problem.

### Non-locality, causality, Bell (Roberto's questions)
- **Causality is safe by construction:** all links are inside the light cone (timelike). Far away in space,
  but never spacelike. No superluminal signalling.
- **No theorem forbids non-locality;** the demand is that *local* physics (differential equations) re-emerges at
  large scales. Causal sets: Sorkin 2007 nonlocal d'Alembertian (alternating sums over layers cancel the far
  contributions), with possible residual non-locality at an intermediate scale — a potential signature.
- **Bell:** Bell correlations are between *spacelike* events A, B; links never connect them directly. In the link
  graph A and B are 2 links apart via the common past (source S) or the common future (comparison event C).
  Bell rules out classical common-cause stories through the past. Using the future path = retrocausal
  approaches (give up measurement independence). Mainstream "entanglement ↔ connectivity": Van Raamsdonk 2010,
  ER=EPR (Maldacena–Susskind 2013). `[ours]` question: can link-graph distance (2 hops between any two events)
  carry anything Bell-relevant without being plain QM? Open.

### Cosmological constant problem (explained in session 1)
- Measured $\rho_\Lambda\approx6\times10^{-27}$ kg/m³; Planck density $m_P/\ell_P^3\approx5\times10^{96}$ kg/m³ ⇒ ratio $\sim10^{-123}$.
- QFT: every field mode is an oscillator with zero-point $\tfrac12\hbar\omega$; summing to a Planck cutoff gives ~Planck
  density; gravity feels it as Λ ⇒ off by ~120 orders.
- Sorkin (talk 1990, publ. 1991): unimodular gravity, Λ conjugate to spacetime volume $V$; Poisson fluctuations
  $\delta N\sim\sqrt N$ ⇒ $\Lambda\sim1/\sqrt V\sim10^{-120}$ in Planck units — before the 1998 discovery.
  Everpresent Λ (Ahmed–Dodelson–Greene–Sorkin 2004): fluctuating Λ always ~ current $H^2$. Status: heuristic,
  ad hoc elements; Barrow 2006 strong constraint; 2017 fit claims ok; 2023 reviews/tests (Das, Nasiri, Yazdi).

### Why "blurring" can fix rotations but not boosts `[ours]` (toy version of Bombelli–Henson–Sorkin)
Average a lattice over orientations: angle $\theta\in[0,2\pi)$, uniform weight $1/2\pi$ — fine (compact group).
Average over boosts: rapidity $\eta\in(-\infty,\infty)$; a uniform probability density would have to be $0$
— impossible (like a uniform distribution on $\mathbb R$). Any normalizable blurring favours some frame.

## The Lorentz dilemma (central result so far)
**Finite number of neighbours per point ⟺ preferred frame.** Roberto's crystal + one-hop neighbours
has finitely many neighbours ⇒ preferred frame ⇒ clashes with his own Lorentz constraint. Options:
- **A.** Keep the crystal, hide the preferred frame at Planck scale (Hořava–Lifshitz, Volovik-style
  emergent relativity). Must explain why low-energy physics is Lorentz-invariant to extreme precision.
- **B.** Keep Lorentz, accept nonlocality (causal sets). Randomness is what does the Lorentz work;
  "order" and "counting" alone on a crystal don't.
- **C.** Something cleverer that is neither a crystal nor a sprinkling (open).

## Background vs preferred frame (Roberto's distinction, session 1)
Three different things, often conflated:
1. **Fixed background** — non-dynamical structure the laws refer to (Newton's absolute space). To avoid.
2. **Dynamical preferred-frame field** — e.g. Einstein-aether: the aether is itself a field obeying equations.
   Background-independent, but breaks local Lorentz invariance.
3. **Preferred frame of the state** — e.g. CMB rest frame: laws fully invariant, the *content* picks a frame.
Our finite-universe cutoff is type 3. The river-flow point budget needs a congruence → type 1 or 2.

**Does causal-set sprinkling use a background?** Only as kinematics/test: to ask "does this causal set look like
spacetime M?", one sprinkles into M and compares. Fundamentally a causal set is an abstract partial order (no
embedding); dynamics (sequential growth, path sums) should generate it without M, and the manifold should emerge.
Status: (i) **Hauptvermutung** — a causal set faithfully embeddable in two manifolds ⇒ they are approximately
isometric — conjectural (quantitative version for finite sprinklings claimed in a 2026 preprint, arXiv 2607.05840);
(ii) **Kleitman–Rothschild problem** — almost all partial orders are 3-layer, non-manifold-like; no dynamics yet
known to suppress them. So: background-free *in principle*, background-assisted *in practice*. Fair criticism.

**Relational rescue for us** `[ours]`: in the toy chain, absolute blur ($\sim\ln N$) is measured relative to fixed
lattice sites (background); relative blur $\langle(u_{n+r}-u_n)^2\rangle\approx\ln r/\pi+0.625$ is relational and
background-free. Program: restate blur as uncertainty in *relations* (which points are linked), and the point budget
as counts in causal intervals, not velocities.

## Background-free toy model: causal diamond (`sims/causal_diamond.py`)
Sprinkle n points in a 1+1 diamond (= random permutation in light-cone coords), forget coordinates.
- Proper time = longest chain = longest increasing subsequence (Ulam): $\langle\mathcal L\rangle\simeq2\sqrt n-1.77n^{1/6}$,
  Tracy–Widom fluctuations $\simeq0.90\,n^{1/6}$ (Baik–Deift–Johansson 1999). Numerics: $\delta\mathcal L/n^{1/6}\approx0.9$. ⇒ $\delta\tau/\tau\simeq0.45n^{-1/3}$:
  intrinsic, relational fuzziness of counted geometry (replaces positional "quantum blur").
- Links of an event = records of a random permutation ⇒ $\langle N\rangle=H_m\simeq\ln m+0.577$; central event $m\approx n/4$.
  Numerics match to 0.1 up to $n=10^6$. ($\ln n\simeq2\ln(L/\ell_P)=2\eta_{\max}$.) Note: choosing the "most central"
  sprinkled point biases the count; insert the event by hand.
- Rapidity reference values: Earth vs CMB η≈0.0012; LHC 9.6; GZK threshold 25 (genuine kinematic test, Coleman–Glashow);
  OMG particle 27 (if proton; ≈23 if iron); cutoff 142 (γ~10^61, 1−v~10^-123). Robust: factor 10^10 in inputs → ±23.

### Does η_max leave a mark on wave propagation? (session 4, 2026-10-25) `[ours]`, 1+1 only
Code: `sims/side_cutoff_dalembertian.py`. Units $\ell=1$; $u=t-x$, $v=t+x$; past event at $(u,v)=-(\tau e^{-\eta},\tau e^{\eta})$,
area $\tau\,d\tau\,d\eta$, Alexandrov area $V=\tau^2/2$. Plane wave $\phi=e^{-i(pu+qv)}$ (so $pq=m^2/4$ on shell).
Sorkin's 2D operator, averaged over sprinklings `[literature]`:
$\langle B\phi\rangle/\phi = 4\left[-\tfrac12+\int d\eta\,h(s)\right]$, $s=pe^{-\eta}+qe^{\eta}$,
$h(s)=\int_0^\infty\tau\,d\tau\,e^{-\tau^2/2}\,(1-\tau^2+\tau^4/8)\,e^{is\tau}$ (layers 1, 2, 3 with weights 1, −2, 1).
- **Raw link sum** (only the "1"): kernel → 1 at $s=0$, so the sum grows like $2\eta_{\max}$. This is the naive worry, but it isn't the wave operator.
- **Sorkin's combination:** $h(0)=0$ (1 − 2 + 1 per unit rapidity), $h\approx -i\sqrt{2\pi}\,s/16$ for small $s$, and $h\approx-1/s^2$ for large $s$
  ⇒ the rapidity integral converges by itself. Validated: $\langle B\rangle = +4pq$ (Sorkin's sign convention for □) to 0.25 % at $pq=10^{-4}$,
  identical to 6 digits under boosts $\theta=0,3,6$.
- **With the cutoff $|\eta|\le\eta_{\max}$ in the cosmic frame:** nothing changes while both light-cone wavelengths $1/p$, $1/q$ (cosmic frame) are $<e^{\eta_{\max}}\sim L$.
  The correction falls off roughly like $(\lambda_{\rm long}/L)^2$. Once $\lambda_{\rm long}>L$, the result **jumps** to $\approx -1/\ell^2$ (a Planck-size term, not a gentle log).
  Reason: the missing ¼ comes from links stretched out to $u\sim1/p$ along the wave's long direction.
  **Corrected in session 5:** this jump is an artefact of the regulator (a sharp rapidity wedge). With a finite past region it disappears; see below.
- **Threshold for a massive particle:** $\lambda_{\rm long}=4E/m^2>L$ ⇔ $E>m^2L/4$: neutrino (0.05 eV) $1.4\times10^{30}$ eV, electron $10^{44}$ eV,
  proton $5\times10^{50}$ eV. These are unreachable, so **no observable dispersion correction from η_max in 1+1**.
  The "possible prediction" (INDEX side calculation) dies in 1+1 for massive fields.
- **Null-wave puzzle resolved (session 5, 2026-10-25).** `sims/side_nullwave_diamond.py`.
  The averaged sum $\int \tfrac12 da\,db\,e^{-ab/2}(1-ab+a^2b^2/8)\,\phi$ over the infinite past is only *conditionally* convergent: the kernel
  integrates to zero per unit rapidity ($1-2+1$), but the total area is infinite. So the answer depends on how the far past is cut off whenever
  the field does not oscillate along a null direction (constant field, exact null wave, or $1/p$ beyond the cut).
  - Rapidity-first (wedge, integrate $\tau$ to $\infty$ at fixed $\eta$): constant → $B=-2$, exact null wave → $-1$, $1/p>L$ → jump to $\approx-1$.
  - Finite past diamond $0\le a\le U$, $0\le b\le W$ (the physical C3 regulator; $b$-integral exact via incomplete gamma):
    constant → $B=4[-\tfrac12+\tfrac12(1-(1-A)e^{-A})]$, $A=UW/2$, i.e. **0** up to $e^{-A}$ (checked analytically: Frullani/digamma give the ½);
    exact null wave → **0**; massive wave → $4pq$ for every $pL$ from $10^{-3}$ to $10^2$ ($pq=10^{-9}$, $L=e^{10}$), where the wedge gave $-0.6$ to $-1.8$.
  - Mechanism `[ours]`: each null edge of the past region supplies ¼. With an oscillating field the ¼ comes from the interior at $u\sim1/p$;
    with a non-oscillating one it comes from the edge of the region. The wedge has no edge, so it loses the ¼.
  - `[literature]` Aslanbeigi–Saravani–Sorkin 2014 (§2–3, read in full text this session): they define the plane-wave eigenvalue only where the
    integral converges absolutely (Im p timelike, future-directed) and take real momenta as boundary values; the 2D result
    $\rho^{-1}g(p)=-Z e^{Z/2}E_2(Z/2)$, $Z=p\cdot p/\rho$, goes smoothly to 0 at $Z=0$. So null momentum gives 0, as in our diamond.
  - **Consequence:** the η_max cutoff leaves *no* trace in Sorkin's 1+1 □ when the cutoff is a finite past (not just "none until $\lambda>L$").
    The kill of the dispersion prediction stands, now stronger; the "abrupt −1/ℓ²" was a regulator artefact. A 3+1 version is not done.

## Objections & tensions
- Fermi GRB 090510: linear energy dependence of $c$ excluded up to $\sim1.2\,E_{\rm Planck}$.
- Density as curvature: density *relative to what*? If volume is measured by counting points, density
  is 1 by definition → needs an external ruler (a background) or curvature must live in the
  connectivity/order instead (as in causal sets).
- Density → slower hops → refractive index → lensing works qualitatively. A horizon from density alone
  describes the outside; the inside seems to need flow (river model) → points moving / being destroyed.
- Random discrete surfaces don't automatically limit to smooth ones (Brownian map).

## Open questions
- Roberto: A, B or C? Is a hidden preferred frame acceptable?
- Can "density" curvature reproduce the factor 2 in light bending (needs both time and space parts)?
- In a river picture on a lattice: where do the points go at the centre of a black hole?


## Session 10: prior art for the cutoff
- Sorkin 2007 (gr-qc/0703099, full text): recovering locality needs "an infrared scale R, which we may identify with the age of the cosmos", with a cosmic rest frame.
  **That's our C3 in his words.** What stays ours: η_max ≈ ln(2L/ℓ_P) ≈ 142 as a rapidity cap, and "frame of the state".
- Boguñá & Krioukov 2025 (2506.18745): rapidity-first integration gives −2ρφ₀ for a constant, a spatial cut gives 0, and the limits don't commute.
  Their Oct 2026 paper (2610.03247): link count linear in the rapidity cutoff; compact hyperbolic quotients as boundary-free regulators.
  Our finite-past diamond result (exact up to e^{−V}; the ½ assembled at the two null edges) wasn't found. It should be checked against the corner terms of
  Buck–Dowker–Jubb–Surya (1502.05388) and Dowker (2007.13206).


## Session 10: the finite-past result is BDJS per event (`sims/r7_corner_check.py`, `sims/out/r7_corner.txt`)
- Our constant-field formula ⟨B1(x)⟩ = −2(1 − A)e^{−A} (past of x inside the region = a diamond of volume A), summed over an interval with S = −Σ B1, gives
  ⟨S⟩ = 2ρ∫(1 − A_x)e^{−A_x} = 2(1 − e^{−A}) → 2: Buck–Dowker–Jubb–Surya's corner volume (two side points). Quadrature exact (1.72933 at A = 2); sprinklings agree within large
  errors (unsmeared action fluctuations). **Known; given back.** The "½ from the null edges, ¼ each" was a regulator-dependent location claim: dropped.
- What remains: the reading (finite age = physical regulator; exact for every wavelength, matching ASS14's continuation). A consistency result, not a claim.

## Log
- 2026-10-24 — seeded; mapped to literature; 1D lattice derivation; Lorentz problem identified.
- 2026-10-24 — Roberto's choices recorded; polygon-light-cone problem; nonlocality derivation;
  blurring vs boosts; analog gravity & river model for Q4/Q5; Lorentz dilemma stated.
- 2026-10-24 — visualization of the sliver; "exactly one tick" objection → links (1 per unit rapidity),
  square lattice (finite), Schild lattice (infinite). Dichotomy robust.
- 2026-10-24 — toy quantum chain (blur ~ ln N), non-locality/causality/Bell, Λ problem; spun off idea 002.
- 2026-10-24 — quantum-blurry points: blur = physical band thickness; still divergent; superposed single
  neighbour non-normalizable; spontaneous Lorentz breaking as the honest escape (= option A + mechanism).
- 2026-10-27 (session 10) — prior art: Sorkin 2007 (age of the cosmos as IR scale), Boguñá–Krioukov 2025/2026 (−2 and non-commuting limits; compact regulators).
- 2026-10-27 (session 10) — finite-past constant-field result = per-event BDJS corner term (checked); null-edge location claim dropped.
