# 005 — Where is the manifold? (reconstructing space from events)

**Status:** exploring (S4a, S4b done in 2D)
**Started:** 2026-10-25   **Last touched:** 2026-10-25

## Roberto's question
"This event thing is ok, but I'm still missing where is the manifold."

## Answer in one paragraph `[literature]`
The causal set does not *contain* a manifold. A manifold M is said to *approximate* the causal set C if C could
plausibly have come from scattering points into M at density ρ (faithful embedding). The manifold is a
large-scale *description* of C, like a fluid description of molecules. To find it from C alone one needs:
1. **dimension** — ordering fraction / Myrheim–Meyer (done, S2), or ball-volume growth;
2. **time** — proper time between related events = longest chain (done), or volume of the interval;
3. **space** — distances between unrelated events: Boguñá–Krioukov causal overlaps (2024);
4. **embedding** — put the events into ℝ^d so that distances match: MDS-style (Johnston 2025) or Laplacian
   eigenmaps (proposed by Boguñá–Krioukov). If the embedding works with small distortion, that IS the manifold.
In our 2D toys the manifold was hidden in plain sight: the two permutations (u, v) are light-cone coordinates;
the test is whether we can recover them (up to Lorentz transformations) from the order alone.

## Plan (S4)
- S4a: implement BK overlaps + MDS/eigenmap embedding; validate on 2D (and 3D) sprinklings: compare reconstructed
  coordinates with the true ones.
- S4b: apply to S3a continuum-phase universes (should reconstruct a 2D patch) and to the crystal phase (should
  fail) — a "manifold detector".
- S4c: apply to the growing universes of S1 (expected to fail: not manifold-like).
- Cluster (Roberto has access): S4 at 10^4–10^5 events, the 100k curvature check, S3a at larger N, exact quantum
  sums up to N ≈ 11–12 (40M–480M 2D orders = N! permutations, as enumerated in s3q; a brief "correction" to poset counts on 2026-10-25 was wrong and reverted), 3+1 kinematic tests at ~10^6 events.

## S4a — distances from the order, flat 2D (2026-10-25, `sims/s4a_overlap_distance.py`)
**BK estimator, quoted** `[literature]` (Boguñá–Krioukov 2024, Eqs. 16–24, 34): for $c$ in the common past of
spacelike $a,b$, with $A = I(c,a)\setminus I(c,b)$, $B = I(c,b)\setminus I(c,a)$, $C = I(c,a)\cap I(c,b)$:
$$O = \frac{V_C}{\min(V_A,V_B)+V_C},$$
with $c$ chosen (by a filter) at equal proper time $\tau_c$ from $a$ and $b$; in 1+1 exactly
$d = \tau_c\,(1-O)/\sqrt{O}$ (re-derived by us: symmetric $c$ gives $O = (t-d/2)/(t+d/2)$).

**Rectangle identity** `[ours]` (1+1 only; not in BK, who require equidistant $c$; wider literature not searched).
Light-cone coords $u=t-x$, $v=t+x$, so $dt\,dx = du\,dv/2$. Put $c$ at the origin, $u_a<u_b$, $v_a>v_b$ (spacelike).
1. $I(c,a)=[0,u_a]\times[0,v_a]$, $I(c,b)=[0,u_b]\times[0,v_b]$ — rectangles.
2. $C = [0,u_a]\times[0,v_b]$, $A = [0,u_a]\times[v_b,v_a]$, $B=[u_a,u_b]\times[0,v_b]$.
3. These are three of the four tiles of the rectangle from $c$ to the join $j=(u_b,v_a)$; the fourth is
   $D=[u_a,u_b]\times[v_b,v_a]$, the causal diamond with $a$ and $b$ as its left/right corners.
4. Opposite tiles have equal products: $C\cdot D = u_a v_b\,\Delta u\,\Delta v = A\cdot B$.
5. $D$'s $(u,v)$-area is $\Delta u\,\Delta v = d^2$ (since $d^2 = \Delta x^2-\Delta t^2 = -\Delta u\,\Delta v$), so $V_D = d^2/2$.
$$\boxed{d^2 = \frac{2\,V_A V_B}{V_C} \approx \frac{2\,N_A N_B}{\rho\,N_C}}\quad\text{for any } c \text{ in the common past.}$$
Intuition: the thin strips $A$, $B$ are long, so they hold many events even when $d\sim\ell$ — same reason BK
beats naive diamond counting. Equidistant-$c$ BK is the special case $V_A=V_B$. Fails in $d>2$: intersections
of diamonds are not diamonds there (lesson 2).

**Results** `[ours]` — flat unit $(u,v)$ square, $\rho=2N$, $\ell=\rho^{-1/2}$; pairs among late events; median
$|d_\mathrm{est}/d_\mathrm{true}-1|$, spread over 4 seeds:

| N | $d<2\ell$ | $2\ell$–$10\ell$ | $>10\ell$ |
|---|---|---|---|
| 1000 | 0.23 ± 0.14 | 0.065 ± 0.014 | 0.052 ± 0.008 |
| 2000 | 0.15 ± 0.04 | 0.050 ± 0.011 | 0.034 ± 0.008 |
| 4000 | 0.19 ± 0.10 | 0.051 ± 0.008 | 0.025 ± 0.002 |

(rectangle identity with the deepest $c$). No significant bias for $d>2\ell$; the large-$d$ error falls roughly as
$N^{-1/2}$. BK (with their Eq. 34 filter) and the median-over-$c$ rectangle estimator are similar or slightly worse.
Below $2\ell$, ~20 % error that doesn't shrink with $N$ — this is the discreteness scale itself.

## S4a — de Sitter 2D: depth dependence = curvature (2026-10-25, `sims/s4a_desitter.py`)
**Continuum prediction** `[ours]`. dS₂ conformal patch $ds^2 = (H\eta)^{-2}(-d\eta^2+dx^2)$, $u=\eta-x$, $v=\eta+x$.
1. Volume element: $dV = d\eta\,dx/(H\eta)^2 = 2\,du\,dv/(H^2(u+v)^2)$.
2. Integrate over a rectangle $[u_1,u_2]\times[v_1,v_2]$: inner $\int dv\,(u+v)^{-2} = \frac{1}{u+v_1}-\frac{1}{u+v_2}$; outer gives logs:
$$V_\square = \frac{2}{H^2}\ln\frac{\eta_L\,\eta_R}{\eta_\mathrm{bottom}\,\eta_\mathrm{top}}\quad(\eta \text{ at the four corners}).$$
3. Light cones are the same as in flat space (conformal flatness), so $A$, $B$, $C$, $D$ are still the same rectangles,
   but the volumes are weighted ⇒ $C\cdot D = A\cdot B$ no longer holds exactly.
4. Put $a,b$ on one slice ($\eta_0$, $x=\mp\delta/2$), $c$ straight below at conformal depth $T$; expand in $\delta\to 0$
   and then in $T$; convert $T$ to proper time ($T/|\eta_0| = e^{H\tau_c}-1$):
$$\frac{d_\mathrm{est}^2}{d^2} = 1 - \frac{(H\tau_c)^2}{8} + O(\tau_c^4, d^2) = 1 - \frac{R\,\tau_c^2}{16} + \dots,\qquad R = 2H^2 .$$
   **Closed form (session 11)** `[ours]`. With $a,b$ at $(\eta_0,\mp h)$ and $c$ straight below at $\eta_0-T$, for $h\to0$: $V_A=V_B\to hT/(\eta_0(\eta_0-T/2))$,
   $V_C\to-2\ln(1-x)$ with $x=T^2/(4(\eta_0-T/2)^2)=\tanh^2(H\tau_c/2)$, so
   $$\frac{d_\mathrm{est}^2}{d^2}=\frac{\tanh^2(H\tau_c/2)}{2\ln\cosh(H\tau_c/2)}\quad(\text{exact as }d\to0,\ \text{any depth, independent of }\eta_0).$$
   Checked against the exact volumes to $10^{-5}$ at $H\tau$ = 0.1–3. Small $\tau$: $1-(H\tau)^2/8$. Only dS shown; that the leading term is $-R\tau^2/16$ locally
   in any 2D spacetime is expected (2D is conformally flat) but not shown.
   Checked numerically from the exact volumes (coefficient 0.1252 at small $\tau$); sideways offset of $c$ barely
   matters; finite $d$ adds a roughly $\tau$-independent shift (absorbed into the intercept of a fit).
   Intuition: in flat space every $c$ gives the same answer; curvature makes the answer depend on how deep you look.

**Bias lesson.** $N_A, N_B, N_C$ are counts in disjoint regions ⇒ independent Poisson. $N_AN_B$ is unbiased;
$1/N_C$ is not ($E[1/N] > 1/E[N]$); use $1/(N_C+1)$, whose mean is $(1-e^{-\lambda})/\lambda$. Use means, not medians,
of ratios. (Before the fix the flat control read 1.11 at shallow $c$.)

**Results** `[ours]` ($H=1$, $\rho=10^4$, $\ell=0.01$, $a,b$ inserted by hand at $\eta_0=-1.05$, $d=14\ell$; flat control in the
same code). Measured − continuum per $\tau$ bin ($0.3$–$0.9$), 200 fresh seeds: consistent with 0 in all bins for both
flat and dS (all within ~1.5 σ). (A first 100-seed run showed a 2–4 σ offset in dS; it vanished with fresh seeds —
bins share a sprinkling, so they fluctuate together.)

**Curvature from counts only:** fit $d_\mathrm{est}^2 = \alpha + \beta\,\tau^2$ over $c$ with $\tau \in [0.2, 0.7]$, $\tau^2 = (N_{I(c,a)}+N_{I(c,b)})/\rho$;
$R_\mathrm{est} = -16\beta/\alpha$. 100 runs, one pair each:

| $\rho$ | flat ($R=0$) | dS ($R=2$; continuum fit in this window 2.13) | spread per pair |
|---|---|---|---|
| 4000 | −0.7 ± 0.6 | 1.3 ± 0.7 | ~6–7 |
| 10⁴ | 0.3 ± 0.4 | 1.6 ± 0.4 | ~4 |

Honest reading: right on average and distinguishes flat from dS, but a *single pair* is useless (spread ≫ signal).
Needs averaging over many pairs (≈ 100 pairs ⇒ ±0.4). Comparable in spirit to BD curvature (S2: also noisy).

**Literature status** (checked 2026-10-25, three web searches — not exhaustive): BK (Sec. VI) only remark that the
method should work locally in curved spacetimes; they don't extract curvature, and no de Sitter / curvature /
rectangle version turned up. Known relatives `[literature]`: curvature from the volume of small causal diamonds
(Gibbons–Solodukhin 2007, agreeing with Myrheim) and from chain abundances in one diamond (Roy–Sinha–Surya 2013).
Our observable (drift of the spacelike-distance estimate with the depth of $c$) was not found; status `[ours]`,
"not found in a brief search".

## S4a — embedding by Lorentzian MDS, flat 2D (2026-10-25, `sims/s4a_embedding.py`)
Method `[literature]` (classical MDS with a Lorentzian Gram matrix; cf. Johnston 2025 for causal sets):
1. Sample $M$ events; squared intervals from counts only: timelike $s=-\tau^2=-2N(I)/\rho$; spacelike
   $s=+d^2=2N_AN_B/(\rho(N_C+1))$ (rectangle identity, deepest $c$).
2. Minkowski: $s_{ij}=(x_i-x_j)^T\eta(x_i-x_j)$. Double centring $G=-\tfrac12 JSJ$, $J=I-\mathbf{1}\mathbf{1}^T/M$ ⇒ $G = X\eta X^T$.
3. Spectrum of $G$: 2D Lorentzian ⇒ one large negative (time) + one large positive (space) eigenvalue, rest ≈ 0.
   Coordinates $t=\sqrt{|\lambda_-|}\,e_-$, $x=\sqrt{\lambda_+}\,e_+$, up to Lorentz transformation + translation.
4. Check: least-squares affine map to the true $(t,x)$; its matrix $A$ should satisfy $A^T\eta A=\eta$.

**Results** `[ours]` ($N=2000$, $\rho=4000$, $M=150$ events in the central region $u,v\in[0.35,0.95]$, ~38 ℓ across; 4 seeds):
- rms position error **0.43 ± 0.07 ℓ** — positions recovered to better than one event spacing (averaging over 150
  points beats the ~1 ℓ error of single distances).
- $\max|A^T\eta A-\eta|$ = 0.03–0.10: the map to the truth is a Lorentz transformation to a few %.
- Spectrum: $\lambda_- \approx -2.2$, $\lambda_+ \approx 2.2$; next largest $|\lambda| \lesssim 0.1$ (gap ~25×).
- **Control, 2+1 sprinkling through the same 2D pipeline:** one large negative ($-0.60$) and **two** large positive
  ($1.19$, $0.75$) eigenvalues, rest $\lesssim 0.18$. The spectrum counts the spatial dimensions even with the
  (wrong) 2D distance formula; the gap is smaller (~4×) and the distances themselves are miscalibrated there.

**Status:** manifold detector for 2D exists: (i) eigenvalue spectrum = signature + dimension, (ii) embedding residual.

## S4b — the detector on S3a phases and S1 universes (2026-10-25, `sims/s4b_detector.py`)
Intrinsic diagnostics (no true coordinates needed), on $M\approx 40$ late events of $N=100$, 10 universes each:
$w_2$ = spectral share of one time + one space direction; $r_+$, $r_-$ = 2nd/1st positive and negative eigenvalue;
stress = rms misfit of the squared intervals by the best 2D Minkowski embedding.
Phase check first (lesson 4): β = 0, 0.3 give ordering fraction 0.49, ~16 layers (continuum-like); β = 0.5, 1.5
give 0.58–0.64, 7–9 layers (crystal). So $\beta_c(N{=}100) \in (0.3, 0.5)$, consistent with $\beta_c \approx 35/N$.

| universes | $w_2$ | $r_+$ | $r_-$ | stress |
|---|---|---|---|---|
| random 2D order (β = 0) — **calibration** | 0.65 ± 0.05 | 0.18 ± 0.08 | 0.19 ± 0.05 | 0.19 ± 0.05 |
| S3a β = 0.3 (continuum phase) | 0.65 ± 0.04 | 0.16 ± 0.07 | 0.31 ± 0.13 | 0.19 ± 0.04 |
| S3a β = 1.5 (crystal phase) | 0.80 ± 0.04 | **0.45 ± 0.12** | 0.09 ± 0.02 | 0.21 ± 0.06 |
| S1 growth, fixed $p$ = 0.05 | **0.32 ± 0.05** | 0.56 ± 0.14 | 0.44 ± 0.10 | **0.65 ± 0.08** |
| S1 growth, $p = 3/n$ | **0.35 ± 0.04** | 0.61 ± 0.16 | 0.34 ± 0.10 | **0.66 ± 0.08** |
(± = spread over universes.)

Reading `[ours]`:
- Continuum phase is indistinguishable from a flat sprinkling at this size — passes.
- Crystal phase: the spectrum wants a **second space direction** ($r_+$ 0.45 vs 0.18) and almost no secondary time
  direction: a few thick layers whose "space" doesn't fit a line. Flagged as not-2D, but only via $r_+$; its stress
  is normal. (Distances there come from the 2D rectangle formula, so read this as "not 2D Minkowski", not as "is 3D".)
- S1 grown universes fail on every diagnostic (stress 0.65, spectrum spread out) — consistent with S2's verdict.
- Small-N caveat: at $N=100$ even the calibration only reaches $w_2 = 0.65$, stress 0.19. Thresholds must be set
  against the calibration at the same $N$; larger $N$ (cluster) would sharpen everything.


## S4b continued (2026-10-25)
**Detector vs N** (flat, 10 universes, sample ≈ 40): stress 0.22 / 0.33 / 0.20 / 0.11 / 0.08 and $r_+$ 0.42 / 0.41 /
0.16 / 0.08 / 0.05 at N = 20 / 50 / 100 / 200 / 400. **Reliable only for N ≳ 100–200**; at N ≲ 50 a flat universe
looks like a crystal. ⇒ exact quantum sums (N ≤ 12) can't be fed to the detector.

**Fast S3a** (`sims/s3a_fast.py`): swap moves change only rows/cols $P=\{a,b\}$ of $C$, so
$K' = C'C' = CC + C'E + EC$ with thin $E$ — O(N²) per step; verified equal to full recomputation (200 swaps);
0.03 s/sweep at N = 200.
| | r | layers | $w_2$ | $r_+$ | stress |
|---|---|---|---|---|---|
| N=200 flat calibration | 0.50 | 24 | 0.75 | 0.07 | 0.10 |
| N=200 β=0.05 | 0.51 | 24 | 0.74 | 0.10 | 0.11 |
| N=200 β=0.6 (crystal) | 0.59 | 9 | 0.82 | **0.39** | **0.28** |
| N=400 β=0.3 | 0.49 | 31 | 0.77 | 0.07 | 0.09 |
At N=200 both $r_+$ and stress flag the crystal. N=400, β=0.3 did **not** crystallise: the $\beta_c\approx 35/N$
extrapolation fails or 300 sweeps don't equilibrate — unresolved.

**N = 400 hot/cold on the cluster** (session 8, jobs 449411 + 449596, `sims/n400_analyse.py`; 4 seeds per point, 15 000 sweeps; 31 of 80 tasks died
of TIMEOUT and enter through their 500-sweep log lines only; the decisive 11 resubmitted as job 449800) `[ours]`:

| β | 0.01–0.05 | 0.08 | 0.12 | 0.2 | 0.3 | 0.45 | 0.7 |
|---|---|---|---|---|---|---|---|
| hot: layers (S/N) | 35–36 (≈0) | 34.9 (−0.07) | 34.5 (−0.11)* | 33.2 (−0.22) | 31.9 (−0.41) | 10.4 (−13.1) | 9.9 (−11.9) |
| cold: layers (S/N) | 35–36 (melted) | 5.1 (−31.8) | 3.2 (−34.1)* | 2.1 (−34.4) | 2.0 (−34.4) | 2.0 (−34.4) | 2.0 (−34.4)† |

\* mostly log-only; † 2000 sweeps (partial). Seed spreads ≤ 0.5 layers except β=0.7 hot (1.0).
- Hysteresis from β = 0.08 to at least 0.7: hot and cold never meet. Cold crystals melt at β ≤ 0.05; hot starts leave the continuum only at
  β ≥ 0.45, and then get stuck in a ~10-layer, r ≈ 0.7 state (the small-N crystal shape) with acceptance ≈ 0.4 %, not in the 2-layer order.
- So β_c(400) is only bracketed: between the two spinodals, 0.05 < β_c < 0.45. Old extrapolation 35/N ≈ 0.09 sits inside; not a measurement.
- The cold crystal's layer count falls with β: 5 (0.08) → 3 (0.12) → 2 (≥ 0.2). The 2-layer (KR-like) order has by far the lowest action (S/N ≈ −34 vs −12
  for the stuck hot crystals), so at large β it is very likely the true ground state; at β = 0.08–0.12 the crystal is thicker. Corrects session 7's
  "3–7 layers" (that was the β = 0.08–0.12 end only).
- To locate β_c one needs a method that crosses the barrier (parallel tempering in β, or a free-energy comparison); single chains cannot.

**de Sitter diamonds** (`sims/s4b_desitter_stress.py`, N=400 fixed, height Hτ): stress 0.09 / 0.11 / 0.09 / 0.14 /
0.17 / 0.21 at Hτ = 0.05 / 0.5 / 1 / 2 / 3 / 4. Curvature is invisible to the flat embedding below one Hubble time
(correction ~ (Hτ)²/8 < noise); the depth estimator (S4a) is the sensitive curvature probe; MDS is a "sheet or not" test.

## S4c — quantum interference vs manifold-likeness, pilot (2026-10-25, `sims/s4c_quantum_detector.py`)
Idea `[ours]`: $A_r = \sum_{r} e^{i\beta S} \propto \langle e^{i\beta S}\,1_r\rangle_\text{uniform}$ — estimate by sampling random 2D orders
(uniform = β=0). Feasible while $|\langle e^{i\beta S}\rangle| \approx e^{-\beta^2\sigma_S^2/2}$ is not tiny; $\sigma_S$ = 4.1, 7.0, 12.5, 18.6 at
N = 50, 100, 200, 400 ⇒ β ≲ 0.4 (N=100), ≲ 0.24 (N=200). Record = stress quartile of the uniform ensemble.
Structural point `[ours; likely known]`: $|A_r| \le \#r$ — in the quantum sum rare classes (crystals) can only win if
the common classes cancel; in $e^{-\beta S}$ they win by weight.

N = 100, 4 × 5000 samples (errors = spread over batches):
| β | $|\langle\text{phase}\rangle|$ | quantum Q1 (most manifold-like) … Q4 | classical Q1 … Q4 |
|---|---|---|---|
| 0.1 | 0.77 | 0.25 0.25 0.25 0.25 (±0.01) | 0.25 0.25 0.25 0.25 |
| 0.2 | 0.37 | 0.26 0.26 0.25 0.24 (±0.02) | 0.23 0.26 0.27 0.24 |
| 0.3 | 0.11 | 0.25 0.25 0.27 0.22 (±0.03–0.06) | **0.16** 0.27 0.35 0.23 |
| 0.4 | 0.03 | noise (±0.13–0.20) | **0.08** 0.29 0.41 0.23 |
Reading: classically, raising β drains the most manifold-like quartile (drift toward the crystal, just below
the N=100 transition). Quantum: no drift within errors up to β = 0.3 — interference does not follow the classical
drift; consistent with the N ≤ 9 exact sums (crystal suppressed). Caveats: all samples are genuine sprinklings, so
stress quartiles are fluctuation-level differences; classical reweighting misses rare low-action universes;
β = 0.4 is noise-limited. **Cluster job:** N = 200, 10⁶ samples (≈ 2–3 core-hours) to sharpen β ≤ 0.24.

## A1 — quantum reweighting at N = 200 on the cluster (2026-10-25, session 4; `sims/a1_sample.py`, `sims/a1_analyse.py`)
10⁶ uniform 2D orders (50 seeds × 2·10⁴, ε = 0.21), raw data in `data/a1/`. σ_S = 12.0, so the mean phase is $e^{-72\beta^2}$
(measured 0.487 at β = 0.1, 0.059 at β = 0.2). Usable up to β ≈ 0.2. Errors: jackknife over seeds.
- **Stress quartile record:** the quantum weight drifts a little toward manifold-like Q1: at β = 0.15, Q1 0.261 ± 0.003 vs Q4 0.242 ± 0.003.
  Classical drifts about the same amount (0.258 / 0.237). The 1,600-sample laptop hint (Q1 → 0.42) was **noise** (lesson 10b confirmed).
- **Layer-count record:** classical runs toward *few* layers (≤ 22 layers: 0.13 → 0.41 at β = 0.2, ESS 1,022). That's the approach to the layered
  phase (S3a). Quantum goes the other way: few-layer universes are suppressed (0.061 → 0.045 ± 0.003 at β = 0.2; 0.022 ± 0.007 at 0.25).
  This is consistent with S3-quantum's exact sums (N ≤ 9) and with Loomis & Carlip 2018 `[literature]`, now at N = 200.
- **Mechanism (checked):** within each record S is nearly Gaussian, and $P_q(r)\propto n_r^2\,e^{-\beta^2\sigma_r^2}$ reproduces the exact numbers to 0.001
  for β ≤ 0.15 (0.005 at 0.2). So in the reachable range, "quantum suppression" is only **"records with a larger action spread cancel more"**:
  few-layer bins have σ = 11.73 vs 11.48 for the rest, and the stress quartiles barely differ (11.96–12.07). This is a second-order, variance effect,
  not a structured interference pattern.
- **Verdict:** A1 is closed. The uniform-sampling method can't reach β ≳ 0.25 at N = 200 (the phase drowns in noise), and up to there it only
  sees Gaussian variance effects. Real interference structure needs other tools: exact/transfer-matrix (A2), or analytic continuation in β
  as in Glaser–O'Connor–Surya.


## Session 10: N = 400 complete, and the detector's prior art
- **N = 400 complete** (job 449800: all 11 resubmitted tasks done, 3.6–7.4 h on cn12). Every decisive (β, start) now has 4 final seeds. Layers, hot/cold:
  0.05: 35.4/35.3 · 0.08: 34.9/5.3 · 0.12: 34.3/3.4 · 0.2: 33.3/2.1 · 0.3: 31.9/2.0 · 0.45: 10.4/2.0 · 0.7: 10.0/2.0. Same picture as v5.
- **Caveat (new):** the cold chains' acceptance is 0.001 at β = 0.08 and 0.000 above. So "hot and cold never meet" is partly a frozen sampler, not only metastability.
  The hot chains (acceptance 0.59–0.90 below 0.45) are sound. To locate β_c we need parallel tempering. The literature fit (Glaser–O'Connor–Surya, ε = 0.21) gives
  β_c ≈ 1.66/(ε²N) = 0.094 at N = 400, inside our bracket (0.05, 0.45). The bilayer ground state is known (Cunningham–Surya 1908.11647).
- **Detector prior art:** Clough & Evans 2016 (arXiv:1602.03103) already do Lorentzian MDS on causal sets, using the eigenvalue spectrum to read dimension and manifoldness.
  Ours are the inputs (interval volumes and the rectangle identity, not chains and naive distance) and the calibrated statistics vs N.
  Depth-drift curvature: not found (only BK's remark that their method extends locally).

## Session 11: figures, and a hole in the detector at N = 400 (2026-10-27, `sims/fig_part1.py`)
- **Detector on the N = 400 Monte Carlo final states** [ours]. Same pipeline ($M_0=60$, $M=40$, events with the largest pasts). Flat band (random orders, N = 400): stress $0.081\pm0.020$.
  - Continuum-like states (30–39 layers, 22 states): stress 0.05–0.15, all pass.
  - 4- and 7-layer crystals: 0.45, 0.84, clear fails.
  - **~10-layer states (7): 0.06, 0.31, 0.12, 0.11, 0.18, 0.18, 0.22 — ambiguous.** With $M=80$ two of them drop to 0.03 (flatter than flat) and others rise. The verdict depends on the sample.
  - 2–3-layer crystals (13 states): the pipeline does not run (no pair sample with common pasts, or no negative eigenvalue). A failure flag, uncalibrated.
  - Likely cause: the sample takes the events with the largest pasts, i.e. the top one or two layers of a layered order. **Fix to try:** a sample spread across depths. Untested.
  - The N = 200 result ("crystal fits badly", $\beta=0.6$, 9 layers) still holds; it was one state.
- **Depth drift rechecked with 400 seeds.** Seeds 1–100 put de Sitter ~2σ above the continuum in four bins in a row; 300 fresh seeds give residuals $0.000\pm0.003$ in the deep bins. Neighbouring bins are 0.87 correlated, so it was one fluctuation. The shallowest bin (τ ≈ 0.1) reads low in flat and de Sitter alike ($-0.09$, $-0.05$): small-count bias when the tiles are nearly empty.
- **de Sitter stress** (8 diamonds per height, new rng): 0.084, 0.110, 0.090, 0.142, 0.182, 0.244 at $H\tau$ = 0.05, 0.5, 1, 2, 3, 4. Leaves the flat band only for $H\tau\gtrsim2$.

- **Fix (same session, `sims/r8_detector_spread.py`, outputs `sims/out/r8_*.txt`).** Two failures, not one:
  1. the "largest pasts" sample sees only the top layers;
  2. in a layered order most sampled pairs have **zero** squared interval (linked, or an empty strip), and MDS fits an all-zero matrix perfectly (the bilayer case: stress 0.00 with a spread sample).
  - Tried: a sample evenly spread in height over the upper 70 % (`s4b_detector.clean_sample(sample="spread")`). Its stress is noisier on flat (0.06–0.22) and does not separate; its $r_+$ does (~10 layers 0.5–0.96 vs flat ≤ 0.34) but max-of-50 thresholds on $r_+$ were unstable (a second draw failed 6/22 continuum states).
  - **Adopted: the share of zero-length pairs** (new 6th output of `diagnostics`), max over the top and spread samples. N = 400: flat 0.075–0.103 (100 universes), continuum MCMC 0.080–0.103 (22), de Sitter $H\tau=4$ 0.08–0.11 (curvature does not move it), layered 0.55–1.0 (9). N = 200: flat 0.10–0.15, growth 0.17–0.19, MCMC β = 0.3 0.12–0.13, β = 0.6 0.39–0.48. N = 100 flat 0.14–0.24. Rule: flag if > 1.5 × flat median at that N.
  - **Held-out test** (rule designed after seeing the N = 400 states): fresh N = 200 chains, continuum 12/12 pass, layered (β 0.6–1.5) 18/18 flagged, growth 12/12 fail (on stress), flat 1/50 false fail with the earlier max-rule.
  - [literature] The zero share is a cousin of interval abundances (Glaser–Surya 2013, 1309.3403). Ours: the embedding detector needs it; its calibration. The detector now asks two questions: layered? (zero share), flat sheet? (stress).
  - 2–3-layer crystals still break the pipeline; counted as a fail.

- **FRW check and reruns (session 11, `sims/r9_drift_fit_frw.py`, outputs `sims/out/r9_*.txt`, `sims/out/rerun/`).**
  - 2D FRW $a=\eta^p$: $R=2(\ln a)''/a^2=-2p\,\eta^{-2-2p}$; rectangle volumes closed form via $G(s)=4(s/2)^{2p+2}/((2p+1)(2p+2))$. For $p=1,-2,\tfrac12$:
    $16(1-\text{ratio})/\tau^2\to R(a,b)$ as $\tau\to0$ (1 % at $\tau=0.01$), right sign. At finite depth: between $R(a,b)$ and $R$(proper-time midpoint) — a depth-weighted average.
  - Sprinkled $p=1$ ($\rho=10^4$, 200 seeds): bins within 1σ of continuum for τ ≥ 0.15 (shallowest bin low, as in dS). Count-only fit $-1.25\pm0.30$ vs same-fit continuum $-0.81$;
    $R$ runs −0.4 … −2.8 over the window.
  - Count-only fit reimplemented (session-3 script lost): reproduces the old table exactly. Reference "continuum fit 2.13" is input-dependent: 1.88 (true τ) … 2.2 (τ² from volumes).
  - Reruns with fixed seeds: distance table, embedding recovery, detector N = 100, propagator rms, p = 0.02 runaway all reproduced. Deepest-c distance now uses $N_C+1$ (no visible change).
  - New: ~10-layer states have propagator rms 0.07–0.10 vs 0.012–0.020 continuum — the propagator flags what the unpatched detector missed.

## Session 11: 3+1 distances and embedding ("2+4"; `sims/r11_4d_distance.py`, `sims/r12_johnston_compare.py`, outputs `sims/out/r11_*`, `r12_*`)
- **Estimator** `[ours]`. For $c$ in the common past of spacelike $a,b$ in 3+1, $(V_a,V_b,V_C)$ fix $(\tau_{ca},\tau_{cb},d)$; $V_C/V_a=w(\tau_{cb}/\tau_{ca},d/\tau_{ca})$ tabulated
  by Monte Carlo (common random numbers, 41×151 grid) and inverted. BK24's regions, exact (tabulated) inversion for **any** $c$; with $c$ = the first event, $d(a,b)$ needs only
  $|{\rm past}\,a|$, $|{\rm past}\,b|$, $|{\rm past}\,a\cap{\rm past}\,b|$.
- **Accuracy** (late events, reference = bottom tip): median error 1–2 % for $d\ge4\ell$ at $N$ = 20,000–80,000, bias ≤ 1 %; 10–20 % below $2\ell$.
- **Embedding** (late events, $M$ = 80–100): positions to 0.3–0.5 ℓ over ~15 ℓ; Lorentz map to 2–3 % (one seed 19 %); spectrum counts dimension (4D: 3 large positive, 3D: 2, 2D: 1);
  stress drops at the right $k$ (4D: 1+3 fits with 0.03–0.07); KR 3-layer order fails (stress ≈ 0.9–0.98).
- **Prior art**: Johnston 2025 (PRD 111, 106020, arXiv:2502.09701) also uses the bottom element $v_1$ (and top $v_n$) as references; time from volumes; spacelike spatial distance by
  the triangle inequality (min over common past/future, min-plus); Euclidean MDS; d = 2, 3, 4. Ours differs: spacelike distance from an exact volume inversion (an estimator, not a bound).
- **Head-to-head** (same universes, whole interval with both tips, n = 500/1500/3000): per-pair spacelike error ours 23/15/9 % vs Johnston 37/30/23 %; but embedded correlation
  ours 0.30/0.58/0.60 vs Johnston 0.61/0.79/0.95. Our errors are heavy-tailed (pairs near the tips have tiny counts) and wreck MDS. My reimplementation of Johnston gives 0.61–0.95,
  below his reported 0.96–0.99: not reproduced exactly (to resolve).
- **Next**: robust embedding (weight pairs by counts; or embed a well-measured core, then place the rest); fix the Johnston reproduction; then decide whether it is a note.

## Session 11 (cont.): reproducing Johnston 2025 and the embedding problem (`sims/r12_johnston_compare.py`, outputs `sims/out/r12_*.txt`)
- **Reproduction.** Tables III (time coordinate) and V (spatial distances) reproduced exactly (d = 4: spatial 0.786/0.887/0.923 vs 0.789/0.887/0.928) **only if** $\tau$ is
  computed from the elements *strictly* between (his eq. 4 reads inclusive $\preceq$; inclusive gives 0.72 at n = 1000). Table IV (Minkowski) not reproduced: 0.82/0.90/0.93 vs
  0.958/0.977/0.985, and plugging in the true time coordinate doesn't change it ⇒ his Table IV uses a statistic the paper doesn't specify. Two questions for Johnston.
- **Oracle.** True spacelike distances + his related-pair values → 0.9999; true related + his spacelike → unchanged. **Spacelike pairs are the whole bottleneck** of his method.
- **Our estimator in his pipeline** (spatial² = d² + Δt² with his t). Bugs found and fixed on the way:
  1. table v1 range (α 0.25–4, δ ≤ 3) silently clipped 18 % of whole-interval pairs (low events) ⇒ per-event bias. v2: measure from the larger interval, α ∈ [0.05, 1], δ ≤ 8;
  2. normalize the overlap by the **smaller** interval (w = V_C/V_b ∈ [0,1]), else small-α rows are unresolved;
  3. Poisson regularization $w=(N_C+\frac12)/(N_b+1)$: raw $N_C=0$ ran the inversion to the edge (d up to 6× the true maximum).
  Late-event accuracy after fixes: 1–2 % at d ≥ 4ℓ, and 6–8 % below 2ℓ (was 11–20 %).
- **Still losing on his benchmark** (spatial corr, whole interval, n = 500/1000/1500/3000): Johnston 0.80/0.90/0.91/0.95; ours capped (min count 5) 0.66/0.82/0.86/0.93;
  averaging ours with his: worse than his alone (paired −0.07 … −0.006); multi-reference averaging: no gain (deep references see the same region); both sides (past+future,
  min count 3): worse. **By separation** (n = 1500): ours better for |dx| < 0.35 (err 16–21 % vs 34–48 % below 0.2), worse for far pairs (12 % vs 6 % above 0.5, bias −11…−17 %).
  Far pairs sit near the waist/edge where each side holds ~10 events; correlations over all pairs are dominated by them.
- **Honest status**: our per-pair estimator is better at short/medium range and scales (one matrix product vs his O(n³) min-plus), but does not improve his embedding on his benchmark.
  Principled next route: a likelihood embedding (Poisson model of all interval/overlap counts given coordinates), which uses all information consistently. Several sessions.

- **Mixed estimator beats Johnston (session 11, Roberto's idea; `sims/r13_mixed.py`).** Switch rule: for a spacelike pair use our overlap estimate if it says
  the spatial distance is $< L$, else his min-plus detour $r$. On his benchmark (spatial corr, his Table V metric), paired against him on the same universes:
  bench (seed 31, $L$ chosen by hand) $L=0.25$: +0.028/+0.017/+0.010/+0.005 at n = 500/1000/1500/3000. **Holdout** (fresh seed 777, $L$ scan 0.15–0.3, both metrics):
  $L=0.25$: spatial 0.812/0.906/0.931/0.972 vs his 0.791/0.891/0.920/0.965 (+0.021±0.004, +0.015±0.001, +0.012±0.001, +0.007±0.001); Minkowski corr improves by the same.
  Plateau at $L$ = 0.25–0.3 (half-width 0.5); $L$ = 0.15 still positive. Gain shrinks with n (his close-pair error matters less there).
  - **Chaining our short estimates into detours fails** (routes of ≤ 2 or ≤ 4 legs over his related edges + our short edges: −0.06 … −0.29). Our legs are 10–15 % low and the
    minimum over many routes picks the lowest: bias compounds. Killed.
  - **Timing** (`sims/out/r13_timing.txt`, laptop, numpy): his min-plus 0.06/0.43/3.7/17.8/76 s at n = 500/1000/2000/3000/4000; our step 0.08/0.22/0.83/1.9/3.3 s (two BLAS
    matrix products + an $O(n^2)$ table inversion). His is a numpy row loop; a compiled min-plus would be ~10× faster but still $O(n^3)$ without BLAS. The switch keeps his
    min-plus for far pairs, so it buys accuracy, not speed.
  - Status: **a genuine, held-out improvement on the published state of the art**, modest (+0.007 to +0.021). Open: cheaper far-pair estimate (to keep the speed),
    larger n on the cluster, other shapes than the diamond, and why exactly our far-pair bias is −11…−17 %.

- **Likelihood embedding [ours: setup; literature: maximum likelihood] (session 12, `sims/r23_likelihood.py`, `sims/out/r23/`).** Unknowns: spatial positions (his t fixed, tips at
  x = 0). Spacelike pairs: $n_C | n_b \sim$ Binomial$(n_b, w)$, $w$ = overlap table at $(\alpha$ from counts, $d/\tau_{ca}$ from positions$)$. Related pairs: interval count in Gaussian
  form for $\tau^2$ (the exact Poisson term with a clamp broke the gradient). Adam, analytic gradient (checked against finite differences), start = weighted fit K100.
  - Consistency: started from the TRUE positions it settles at 0.973 / 0.979 / 0.985 (n = 400 / 1000 / 2000): the finite-n optimum, approaching the truth with n.
  - **Fresh universes, paired:** n = 1500 (3 univ., seed 7070): Johnston 0.9235, switch +13 %, K100 +59 %, **likelihood 0.9728 = +64 %** (+0.049 ± 0.003);
    n = 3000 (2 univ., seed 7071): Johnston 0.9571, switch +17 %, K100 +48 %, **likelihood 0.9834 = +61 %** (+0.026 ± 0.0001). Beats K100 in 5/5 universes. No hand-set constant.
  - Start independence: from Johnston's map instead: 0.970 / 0.970 / 0.975 vs 0.969 / 0.971 / 0.978 (log-lik equal to ~1e-5; one start better in each direction).
  - Cost: ~0.3 s per iteration at n = 3000 (laptop), 400 iterations; O(pairs) per iteration. Next: cluster at n = 6000–15000 paired with r14 (r24), slab version (tip-free references).
  - **ABLATION (same universes, two starts) — changes the claim.** Share of Johnston's residual removed, n = 1500 / 3000:
    **Poisson (related pairs) only: +74–76 % / +74–76 %**; both terms: +63–64 % / +61–64 %; binomial (overlap) only: +19–25 % / +14–25 %.
    ⇒ Our binomial overlap term HURTS when added; the gain is the related-pair Poisson likelihood (= Casasola 2026's count likelihood, there near-cone only and from
    true±ℓ starts) started from an intrinsic map (his stated outlook). Probable cause of the harm (untested): systematic error of the binomial model (table bias at far
    pairs, α and τ_ca taken from noisy counts, pairs treated as independent) with very large weights. Possible fix to test: α, τ_ca from the coordinates (self-consistent).
    Honest claim now: "Casasola's Poisson likelihood, given an intrinsic start, removes ~75 % of Johnston's error" — ours is the intrinsic start + all related pairs +
    the benchmark, not the binomial term. Lesson 37.
  - **Large n on the cluster (r24, session 13; `sims/r24_cluster_lik.py`, `cluster_fetch/r24/out`, paired with r14/r19 universes, 1/2/4/8/6 universes at n = 1000/3000/6000/10000/15000).**
    Share of Johnston's residual removed: **Poisson only +67 / +80 / +81 / +79 / +83 %** (+0.0386 ± 0.0024 … +0.0094 ± 0.0002; spatial corr 0.9980 at 15000 vs his 0.9886);
    both terms +59 / +64 / +64 / +58 / +63 % (binomial term costs ~15–20 points at every n); K100 +58 / +47 / +38 / +23 / +26 % (fades); switch flat ~19 %.
    r19 weighted fits: K300 61 → 36 %, K10/K30 fade to noise by n = 10000. ⇒ The Poisson likelihood's share does **not** shrink with n (first estimator in this
    line that holds its share); it is the 3+1 method. Cost (median, cluster): Poisson fit 0.1 / 0.8 / 3.1 h at n = 3000 / 6000 / 10000–15000 (400 iterations; the
    15000 cost equal to 10000 is unexplained, check pair subsampling/node) + ~0.4 h start, vs Johnston 0.02 / 0.24 / 1.3 / 3.8 h at 3000 / 6000 / 10000 / 15000.
- **Second shape: slab (session 12, `sims/r22_slab.py`, `sims/out/r22/`; seeds 6060 (n = 1500, 3 univ.), 6061 (3000, 2 univ.)).** Cylinder t ∈ [0,1], |x| ≤ 0.5, no tips;
  tip-free pipeline for every arm (true t; related R from interval counts; his 2-leg detour, 4-leg fallback; ours with a per-pair reference among 32 boundary events per side;
  double-centred MDS). Diamond control through the same pipeline (with its tips) reproduces the ranking: K100 +59 % / +31 %, switch +15 % / +20 %, ours alone far below.
  - **Slab: Johnston is strong** (0.984 / 0.991; diamond 0.926 / 0.956): no waist, far pairs always have related events above and below. **Switch gain = 0** (diamond-specific).
  - Weighted fit: K0 = 100: **+0.0038 ± 0.0008 (+24 %)** at 1500, +0.0030 ± 0.0022 (+33 %, 2 univ., not significant) at 3000; K0 = 30 (the pre-registered value): −3 %, +2 % (≈ 0).
    K0 = 100 was preferred on earlier, different universes (r19 laptop, r20), so this is out-of-sample for it, but on 2–3 universes. Interior pairs: same picture, larger errors.
  - Ours alone per pair: worse in the slab (equal n ⇒ 4× lower density; ℓ 1.41× larger) and biased near the side wall (median error 0.080 away vs 0.116 near, n = 3000):
    intervals that poke out of a non-causally-convex region are clipped.
  - Reading: Johnston's weak spot is the diamond's waist; in a slab he is near the oracle's ceiling. Our weighted fit still edges him there only with strong down-weighting
    of small counts (K0 = 100), i.e. the result depends on a hand-set constant: an argument for the principled (likelihood) weights. Next if pursued: slab at larger n (cluster),
    equal-density comparison.
- **Laplacian eigenmaps (BK24's suggestion) — killed for this benchmark (session 12, `sims/r21_eigenmaps.py`, seed 4040).** BK24 (§ on reference frames) propose embedding their
  distance matrix with "any embedding method … like Laplacian Eigenmaps", for events on one spatial slice, "developed in a forthcoming publication" (not found: two web searches,
  Oct 2026). Validation first: eigenmaps on the TRUE spatial distances, best linear map to the truth: corr 0.91 (n = 1000), 0.92–0.93 (3000), k = 15 or 50; density-normalized
  diffusion map (Coifman–Lafon α = 1): 0.92 / 0.93. Johnston gets 0.87 / 0.955 and our weighted fit 0.94 / 0.97 from counts. The eigenmap shape itself is warped
  (eigenfunctions of a ball are not linear coordinates, worst at the rim), so it is capped below the competition whatever the distances. With our distances (n = 1000, 2 univ.):
  0.66–0.67, after local SMACOF 0.74. Paper: one line in "paths dropped" (it is BK's own suggestion; say why it is capped).
- **Seed (Roberto, session 11) [ours]: distance as a large-N quantity, like temperature.** The overlap distance is a count ratio whose fluctuations shrink like
  $1/\sqrt{N}$; it may only be meaningful at large N (3000 events in 3+1 is only $\sim 3000^{1/4}\approx 7$ ℓ across). Consistent with the standard view [literature]
  (Sorkin's "order + number = geometry"; Brightwell–Gregory for timelike distance; Boguñá–Krioukov's errors vanish with density). Speculative part: a count-defined
  spacelike distance might be the right object for the quantum questions later. Practical consequence: judge methods by convergence with N, not only at n = 500–3000.

- **Cheaper far pairs (session 11, `sims/r15_cheap_far.py`, seed 4242).** Goal: keep the switch's gain without his $O(n^3)$ min-plus. Full switch: +0.0136 / +0.0076
  over Johnston at n = 1500 / 3000.
  - (a) K random stepping stones: **killed.** Far pairs need a stone related to *both* events, i.e. high above or deep below the midpoint; random stones rarely qualify
    (21–79 % of far pairs found none and went to the full detour), and the result was at or below Johnston (−0.008 … −0.033 at n = 3000).
  - (b) two passes: a rough map from ours alone (full detour only for the ~3 % of pairs with zero counts), then stones from the grid cells around the 1/4, 1/2, 3/4 points.
    Keeps about half to two-thirds of the gain: +0.007 (1500), +0.005 (3000), all grid sizes. Far step 5.5 s vs ~16 s full min-plus at n = 3000, but 17–28 % of far
    pairs still found no stone and paid the full detour (spatial cells include all times; only stones far enough in time relate to both). Share falls with n.
  - (b) polished (`r15_cheap_far.py polish`, `sims/out/r15_polish.txt`): pairs with no related stone in the three cells search the 3×3×3 block around the midpoint
    before the full detour. Fallback share 17 % → 0.7 % (n = 3000, G = 4), 28 % → 2 % (n = 1500). Gain kept: +0.006 of the switch's +0.009 at n = 3000, but only
    +0.004 of +0.013 at n = 1500 (block stones lie off the segment, so their detours are longer). Far step 4.5 s vs ~16 s full min-plus at n = 3000.
    Scaling: stones per pair ~ n/G³, so G must grow like $n^{1/3}$ to make the step $O(n^2K)$; at fixed G it is still $n^3$, just smaller. A modest speed-up, not a new method.

- **cluster r14, n = 3000 and 6000 (jobs 450017, 450018; `sims/out/r14/`).** Switch L = 0.25 vs Johnston: +0.0084 ± 0.0014 (3000, 2 univ.), **+0.0049 ± 0.0004 (6000, 4 univ.)**.
  In terms of his remaining error $1-\rho$: the switch removes 10 % (n = 500), 14 % (1000–1500), 17 % (3000), **20 % (6000)**: the relative gain *grows* with n.
  Pure ours: $1-\rho$ = 0.18 (3000), 0.088 (6000) vs his 0.049, 0.025: both roughly halve per doubling, ratio ~3.6 stays: pure ours is not overtaking him.
  Timing on the cluster (cn05, 4 cores): his min-plus 101 s → 898 s (×8.9 for ×2 n, ~$n^{3.2}$); our step 14 s → 65 s (~$n^{2.2}$); eigh 4 → 30 s. Memory 3.2 GB at 6000.

- **(c) Map from counts only: fit to trusted distances (session 11, `sims/r16_local_fit.py`).** Time coordinate fixed (interval counts); 3 spatial coordinates fitted by weighted
  stress majorization (SMACOF, Jacobi form) [literature: method; ours: setup] to related-pair separations (weight 1) and our shared-past estimates (weight 1 if < 0.25,
  weight $w_{far}$ otherwise); start from the ours-alone map.
  - Dropping far pairs ($w_{far}=0$): 85 % of the ours-alone gap closed but below Johnston (−0.012 at n = 3000; erratic at 1500). Trusting ours further (L = 0.35, 0.5): worse.
  - Scan (same universes, seed 99): $w_{far}$ = 0.1: +0.012 (1500), +0.005 (3000).
  - **Holdout** (seed 2026, 5 + 3 universes): **no detour anywhere** (zero-count pairs start at the median and get weight 0): +0.008 ± 0.007 (1500), **+0.004 ± 0.002 (3000)**;
    with the detour start: +0.006, +0.002. Minkowski corr about equal to his. The switch stays best and steadiest (+0.014, +0.005).
  - Status: **a method built only from counting (no detours) that matches Johnston and edges him at n = 3000**, noisier per universe. Cost $O(n^2)$ per iteration,
    ~100–250 iterations (10–20 s at 3000). Next: test at n = 6000–15000 (cluster), where his min-plus costs ~$n^{3.2}$; per-universe failures at small n (one of five at 1500).

- **cluster large n (session 12, 2026-10-28; r14 jobs 450019–20, r17 jobs 450032–35; `cluster_fetch/`).** Universes: 4 at 6000 and 10000, only 2 at 15000 (± from 2 is fragile, lesson 8).
  - **Switch L = 0.25:** +0.0049 (6000), +0.0033 (10000), +0.0022 (15000). Share of his residual $1-\rho$ removed: 17 %, 20 %, 20 %, 19 % (3000–15000).
    **Correction:** the session-11 line "the relative gain grows with n" was wrong past 6000: it **plateaus at ~20 %**. The absolute gain shrinks because his error shrinks.
    The switch wins in every universe at every n. At 15000, L = 0.30 is marginally better (+0.0024); the optimal L may drift up slowly with n.
  - **Pure ours** $1-\rho$: 0.088, 0.076, 0.064 vs his 0.025, 0.016, 0.011: the ratio grows (3.5 → 4.7 → 5.6), i.e. pure ours falls further behind. Capped: ratio ~2.5, flat.
  - **(c) counts-only map: killed as "matches Johnston".** Share of his residual: +13 % (1000), +2 % (3000), then **−14 %, −31 %, −25 %** (6000, 10000, 15000). Its edge was a
    small-n effect. What survives: within 0.002–0.005 of him at 1/4–1/8 of his time (1776 s vs 13657 s at 15000). A fast approximation, not a competitor.
  - **Timing (cn05, shared node):** his min-plus 898 → 4457 → 12077 s (~$n^{2.8}$ over 6000–15000); our step 65 → 238 s (~$n^{1.4}$); eigh 30 → 295 s; (c) fit ~$n^{2.3}$.
    The switch costs his time plus ours, so its selling point is accuracy, not speed.
  - **Is the overlap estimator consistent as N → ∞? (session 12, back-of-envelope) [ours].** The distance information is in the deficit $D$ = events in past $b$ but not in past $a$:
    for small $d$, $\rho V_D \approx \kappa\,\rho\, d\,\tau^3$ (a shell of thickness ~$d$ around a cone of height $\tau$; $\kappa = O(1)$, not computed). Poisson ⇒ $\delta d/d \approx 1/\sqrt{\kappa\rho d\tau^3}$.
    At fixed shape all lengths scale as $n^{1/4}$ ⇒ $\delta d/d \propto n^{-1/2}$. Measured per-pair error 23/15/9 % at n = 500/1500/3000: exponent ≈ −0.52; Johnston's 37/30/23 %: ≈ −0.27. **CORRECTED (same session, lesson 33): those two series measure different quantities (ours Minkowski d, his spatial r). Like for like (`sims/out/r12_perpair_fair.txt`, spatial |dx|, pairs with count ≥ 20): ours 0.112 → 0.062, his 0.132 → 0.083 at n = 1000 → 3000: slopes n^{−0.54} vs n^{−0.42}. Ours still faster, by much less.**
    Order of magnitude at n = 3000 ($\tau\sim4$, $d\sim2$ in ℓ): ~9 %, as measured (order of magnitude only). Caveats: (i) events hugging the lower light cone have small pasts at any N,
    so the heavy tail shrinks slowly; embedding-level $1-\rho$ of ours alone falls only ~$n^{-0.35}$ (6000–15000) vs his ~$n^{-0.9}$; (ii) the table is flat-space: in curved
    spacetime the past volumes carry $O(R\tau^2)$ corrections (cf. the depth drift), a bias that grows with depth and does not vanish as N → ∞.
    Corrections (same session): the per-pair numbers are **medians** (`r12_johnston_compare.py`), so the $n^{-1/2}$ slope is the typical pair; the embedding is set by the tail.
    "Ours" already uses whichever side (past via $v_1$ / future via $v_n$) has more events, so the bad tail = far pairs straddling the waist, whose shared past and shared
    future are both small *by geometry*. A third caveat ("which limit") was empty in flat space: only size/ℓ matters there; it only bites when curvature adds a second scale (= caveat ii).
    Ours alone overtaking him as N → ∞: not supported (error ratio 3.5 → 4.7 → 5.6 over 6000–15000).
- **Waist-pair diagnostic (session 12, `sims/r18_waist_oracle.py`, `sims/out/r18/`; seeds 2028 (n = 1500, 3 univ.), 2029 (n = 3000, 2 univ.)).** k = shared count on the side used.
  - Low-count pairs are not a handful: k < 10 is 50 % (1500) / 31 % (3000) of spacelike pairs; k < 30: 75 % / 56 %.
  - Oracle on k < 10 pairs only (true distance there, ours elsewhere): 0.9965 / 0.9948 = **88–96 % of his residual removed**; oracle on all *other* pairs: barely moves ours.
    ⇒ ours is fine wherever k ≥ 10; **the low-count pairs are the whole problem**.
  - His detour on the low-count pairs (switch on k): ≈ Johnston (−1 … +1 %): his detours are no better there; the r13 switch gains on close pairs.
  - **Count-weighted embedding** (SMACOF, weight k/(k+30) per spacelike pair, related pairs 1; K0 = 30 fixed before testing): +0.037 (1500), +0.019 (3000) = **45 %, 42 % of his residual**,
    twice the switch on the same universes (15 %, 20 %). Answer to Roberto's question: it is *both* — the low-count distances are bad, and classical MDS gives them full voice.
    This is a crude likelihood (weight ≈ Poisson information). Unlike (c), the weight follows the count (the error-profile variable, lesson 34), not our distance estimate.
  - No-detour version on the r14 universes (`sims/r19_cluster_wfit.py`, median fill for missing pairs): seed 1001, n = 1000 / 3000: K0 = 30 → 50 % / 35 %; K0 = 100 → 58 % / 46 %; K0 = 10 lower.
    Fit 4 s vs his 87 s at 3000. **Warning: (c) also looked good at n ≤ 3000 and lost at 6000+.** cluster r19 (n = 3000–15000, K0 = 30, 10, 100, 300) is the test; K0 picked there must be
    confirmed on fresh seeds.

- **Interior benchmark + Madsen comparator (session 12, `sims/r20_interior.py`, `sims/out/r20/`; seeds 3030 (n = 1500, 4 univ.), 3031 (n = 3000, 3 univ.)).**
  Core = Madsen's count criterion min(|past|, |future|) ≥ fN. Note: v ≤ N/16 everywhere (the centre's past is a height-½ diamond), so f = 0.02 / 0.04
  (core ≈ 10 % / 1–1.5 % of events; r ≤ 0.33 / 0.21 of the waist radius 0.5, t ≈ 0.39–0.60 / 0.45–0.54). All maps global; scored on core pairs only. [ours]
  - (A) Core pairs, share of Johnston's core residual removed: f = 0.02: weighted fit K0 = 100 +64 % (1500), +13 % (3000); K0 = 30 +54 %, −8 %; switch ≈ 0 (−1 %, −6 %);
    ours alone −405 %, −229 %. f = 0.04 (tiny cores, 31–42 events): K0 = 100 +88 % (1500, 2 univ.), +53 % (3000); switch +2–4 %.
    Johnston is already good in the core (0.972 / 0.993 at f = 0.02): the switch's gain lives near the rim, not in the interior; the weighted fit gains in both.
  - (B) Madsen local charts [literature: Madsen 2026 Sec. 3.2–3.3; implementation ours]: one chart for the core is impossible (common past of the core empty at n = 500);
    charts = M = 20 or 40 nearest events by his profile distance (radius ≈ 0.12–0.16), 5 chained anchors timelike to the whole chart (tips allowed), best Gram conditioning
    from counts, boosted to the tips' rest frame (no truth used). **Validation with true intervals: corr 1.000000 (exact).** With counts: Gram condition number ~800,
    local corr 0.40–0.52 vs Johnston 0.91–0.97 on the same pairs; median relative error 30–42 % (Johnston 6–15 %, K0 = 100 6–7 %). Averaging 10 anchor sets: no better.
    20–63 of 60–80 charts found no valid anchor set. Weighted fit on the same local pairs: +25 % / +44 % (3000, M = 20 / 40), +77 % (1500).
  - Reading: trilateration amplifies count noise (squared intervals of long baselines, ill-conditioned Gram); at n ≤ 3000 (diamond ≈ 7 ℓ across) there is no room for
    charts that are small compared with well-separated anchors. Madsen's construction is asymptotic (his rate is ρ^{−1/32} for curvature); not competitive here. Fair-comparison
    caveat: his chart uses 5 timelike intervals per event; the other arms use all pairs of all events.
  - Caveats: 3–4 universes; f changed from 0.1/0.2 (infeasible, not tuned on results); M = 20 chosen from anchor availability on seed 5 (not the test seeds); K0 = 100 was the
    better of the laptop r19 seed-1001 runs (different universes).

- **Consistency of the Poisson-only fit (session 13, `sims/out/r25/consistency_poisson_only.txt`; true t, start = true positions, 400 iterations, seeds 11–13):**
  corr 0.966 / 0.991 / 0.9965 at n = 400 / 1000 / 2000 (both terms, session 12: 0.973 / 0.979 / 0.985): approaches the truth with n, better than both terms for n ≥ 1000.
  cluster r24 logs: log-likelihood still rising 0.01–0.05 % per 100 iterations at 400, i.e. not fully converged (gains are a lower bound).
- **Exact Poisson and 1000 iterations (session 13, `sims/r26_exact_iters.py`, `sims/out/r25/r26_*`; ablation universes seeds 7070 (1500 × 3), 7071 (3000 × 2)).**
  Exact $\sum[N\ln\mu-\mu]$ over all related pairs needs a soft relation term $\sum\ln\sigma(\tau^2/s)$ ($s$ = 0.1 ℓ²): without it N = 0 pairs go spacelike for free and the
  fit from the truth drifts (0.899 / 0.971 / 0.990 at n = 400 / 1000 / 2000); with it 0.973 / 0.993 / 0.997 (Gaussian 0.966 / 0.991 / 0.9965). That, not "the gradient",
  is why the session-12 clamp failed. Share of Johnston's residual, gauss400 / gauss1000 / exact400 / exact1000: **76 / 77 / 77 / 77 % (1500), 74 / 74 / 75 / 74 % (3000)**;
  paired differences ≤ 0.0003. ⇒ Neither the form of the likelihood nor more iterations matters; the 400-iteration Gaussian numbers stand.
- **Slab with the Poisson likelihood (session 13, `sims/r25_slab_lik.py`, `sims/out/r25/`; seed 6060, n = 1500, 3 univ. per shape, equal n, 400 iterations).**
  The related-pair Poisson term needs no reference event, so it is tip-free as it stands (gauge: mean gradient removed, nothing pinned; gradient checked).
  Start = r22's count-weighted SMACOF K100. Share of Johnston's residual removed, all / interior pairs:
  diamond control: Poisson +79 / +68 %, K100 +59 / +51 %; **slab: Poisson +43 ± 10 / +69 ± 9 %**, K100 +22 / +13 %, switch 0 / −3 %.
  - **Wall diagnosis (oracle, truth used):** in the slab an interval can leave the side wall, so its count is low (45 % of related pairs have < 99 % of their interval
    inside, 14 % < 80 %; mean share 0.93). Dividing each count by the true inside share: slab **+64 / +74 %**. ⇒ The wall explains about half of the slab's
    all-pairs loss; the interior is already near the diamond's level. The rest of the gap is untested (slab ℓ is 1.41× larger at equal n; equal density next).
  - Not yet intrinsic: a usable correction needs the inside share from the map itself (e.g. self-consistent: fit the region's boundary from the current positions,
    recompute the shares every ~50 iterations). It assumes a known shape class (a cylinder), so it is a benchmark fix, not a general method.
- **Slab at equal density (session 14, cluster r25, jobs 450431–450435; seed 2500 + task; 4 univ. per row; ± = s.e. over universes, as share of his residual).**
  Slab n = 6000 / 12000 has the density of diamond n = 1500 / 3000. Share of Johnston's residual removed by the Poisson fit, all / interior pairs:
  diamond 1500: **+75 ± 5 / +69 ± 10 %**; diamond 3000: **+80 ± 6 / +71 ± 14 %** (agrees with r24's 79–83 %).
  slab 6000: **+58 ± 9 / +80 ± 12 %**; slab 12000: **+65 ± 6 / +86 ± 2 %**. Oracle wall: slab 6000 **+80 / +84 %**, slab 12000 **+86 / +88 %**.
  - ⇒ At equal density the oracle closes the whole all-pairs gap to the diamond (80 vs 75, 86 vs 80). The other half of the session-13 equal-n gap was density.
  - Wall cost ≈ 21–22 points at n = 1500, 6000, 12000 alike: the clipped share is set by the shape (45 % of related pairs < 99 % inside, 13.5 % < 80 %, at every n), so it does not shrink with n.
  - Interior pairs: slab ≥ diamond (80–86 vs 69–71 %). Not interpreted yet (interior = top quartile of min(|past|,|future|), which in a slab selects by time, not by distance from the wall).
  - Density matters: slab all pairs −92 % (n = 600, 1 universe, interior +21 %) → +43 % (1500) → +58 % (6000) → +65 % (12000). The n = 600 failure is a single universe, but it is a failure.
  - Scale: his slab residual is ~10× smaller than in the diamond (1 − ρ = 0.0069 / 0.0047 vs 0.079 / 0.044); ours too (0.0029 / 0.0016 vs 0.020 / 0.0088). The shares are of a small residual.
  - Switch 0 to +3 % (all), −6 to −7 % (interior); K100 +12–13 % / −10 to −15 %: both fade in the slab, as at equal n.
  - Cost at slab 12000 (median): Poisson fit 1291 s, his detours 10137 s, oracle 1018 s. All 450435 tasks fit in 110 G (MaxRSS not reported with `-X`).
## Log
- 2026-10-25 — created after Roberto's question and his reading of Boguñá–Krioukov 2024.
- 2026-10-25 (session 3) — S4a flat 2D: BK estimator quoted and checked; rectangle identity; distances to 3–5 %.
- 2026-10-25 (session 3) — S4a de Sitter: depth dependence of the estimate = curvature, $1-R\tau^2/16$; confirmed by sprinkling.
- 2026-10-25 (session 3) — S4a embedding: Lorentzian MDS recovers flat 2D positions to 0.4 ℓ; spectrum detects 2+1.
- 2026-10-25 (session 3) — S4b: detector passes S3a continuum phase, flags crystal (extra space direction) and S1 growth.
- 2026-10-25 (session 3) — detector needs N ≳ 100–200; fast S3a; dS stress; S4c pilot: quantum weights show no drift away from manifold-like universes (β ≤ 0.3, N = 100), classical does.
- 2026-10-25 (session 4) — A1 on the cluster: 10⁶ samples at N = 200; quantum suppresses few-layer universes (opposite to classical), fully explained by per-record action variance; pilot hint was noise; method exhausted at β ≈ 0.2.
- 2026-10-27 (session 8) — N = 400 hot/cold on the cluster: hysteresis from β = 0.08 to ≥ 0.7, β_c bracketed in (0.05, 0.45); cold crystal 5 → 2 layers with β; hot starts stick at ~10 layers.
- 2026-10-27 (session 10) — N = 400 complete (cold chains frozen: a sampler caveat); detector prior art Clough–Evans 2016; β_c(400) literature fit 0.094 inside our bracket.
- 2026-10-27 (session 11) — Part I figures; detector ambiguous on ~10-layer N = 400 states (sample from the top layers); depth drift confirmed with 400 seeds.
- 2026-10-27 (session 11) — detector fix: zero-length share flags layering at N = 200 and 400 (held-out test passed); a cousin of interval abundances.
- 2026-10-27 (session 11) — FRW check: drift leading term = R locally (3 FRW cases); count-only fit = depth-weighted R; Part I numbers rerun and reproduced.
- 2026-10-27 (session 11) — 3+1: overlap-volume distance from past sizes (1–2 % at large N), embedding counts dimension; per pair beats Johnston 2025, embedding does not yet.
- 2026-10-27 (session 11) — Johnston 2025 reproduced (Tables III, V; not IV); oracle: spacelike pairs are his bottleneck; three estimator bugs fixed; still below his embedding.
- 2026-10-27 (session 11) — mixed estimator (ours for close pairs, his detours for far): beats Johnston 2025 on his benchmark at n = 500–3000, held out; chained routes fail; timing.
- 2026-10-27 (session 11) — cheaper far pairs: random stones killed; two-pass chosen stones keep about half the switch's gain at 1/3 the far-step time.
- 2026-10-27 (session 11) — cluster: switch gain holds at 6000 (20 % of his residual). (c) counts-only fit (no detours) matches/edges Johnston, held out.
- 2026-10-28 (session 12) — cluster n = 10000, 15000: switch removes a flat ~20 % of his residual (not growing; session-11 claim corrected). (c) loses at n ≥ 6000: killed as competitor, kept as fast approximation.
- 2026-10-28 (session 12) — waist diagnostic: low-count pairs are the whole gap (oracle 88–96 %); count-weighted SMACOF removes 42–45 % of his residual at n ≤ 3000 (switch 15–20 %). cluster r19 prepared.
- 2026-10-28 (session 12) — Laplacian eigenmaps (BK24 suggestion): capped at ~0.93 even on true distances (warped shape); killed for the distance benchmark.
- 2026-10-28 (session 12) — interior benchmark (r20): weighted fit keeps winning in the core (K0 = 100: +13…+88 % of his core residual), switch gain vanishes there; Madsen local trilateration validated exactly but 30–42 % per-pair error at n ≤ 3000 (not competitive).
- 2026-10-28 (session 12) — slab benchmark: Johnston strong (no waist), switch gain 0, weighted K100 +24–33 % (2–3 univ.), K30 ≈ 0; diamond control reproduces the ranking.
- 2026-10-28 (session 12) — likelihood embedding: +61–64 % of Johnston's residual at n = 1500/3000 (5/5 universes beat the weighted fit), start-independent, no constant.
- 2026-10-28 (session 12) — ablation: Poisson related-pair term alone +75 % (Casasola 2026's likelihood, intrinsic start); our binomial term hurts. Literature review found Casasola.
- 2026-10-28 (session 13) — r24 large n: Poisson-only likelihood keeps +79–83 % of Johnston's residual at n = 3000–15000 (no decay); binomial term costs 15–20 points; weighted fits fade.
- 2026-10-28 (session 13) — slab: Poisson likelihood +43 % all pairs / +69 % interior (diamond +79 / +68); oracle wall correction → +64 / +74 %: the clipped intervals at the side wall cost about half.
- 2026-10-29 (session 14) — r25 equal density: slab Poisson +58 / +65 % (all, n = 6000 / 12000) vs diamond +75 / +80 %; the oracle wall correction closes the whole gap (+80 / +86 %). Wall cost ~21 points, independent of n; slab at n = 600 fails (−92 %, 1 universe).
