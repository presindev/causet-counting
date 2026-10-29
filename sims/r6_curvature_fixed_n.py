"""Curvature from Johnston's propagator at fixed interval size (idea 006, session 10; ROADMAP "J2 probe").

One causal diamond in 2D de Sitter (H = 1), apexes on x = 0 at conformal times eta_b < eta_t < 0, proper height tau = ln(eta_b / eta_t).
Light cones are as in flat space (conformal coordinates u = eta - x, v = eta + x); only the density is uneven, rho / eta^2. Conditioned on n events
inside, their positions are i.i.d. with density ~ 1/eta^2 on the diamond, so the order they form depends on (n, H tau) only, not on rho.
Flat target (H tau -> 0): a uniformly random 2D order, E[c_k | n] = C(n,k)/k!, E[K | n] = 1/2 L_n(mu/2).
We measure, per (n, H tau):
  - g_k = E[c_k | n] / (C(n,k)/k!) - 1 for k = 2, 3 (c_2 = related pairs: the ordering fraction, the known chain-abundance route);
  - the propagator deviation  E[K | n] - 1/2 L_n(mu/2)  at a few mu, in units of the flat target's sampling error per interval;
  - the number of intervals needed for a 3-sigma detection of curvature, from K and from c_2 alone.
Errors: standard error over independent intervals (each interval is its own sprinkling, so they are independent).
Usage: python r6_curvature_fixed_n.py [samples=3000] [seed=1]
"""
import sys
import numpy as np
from math import comb, factorial

def diamond_points(n, htau, rng):
    """n points with density ~ 1/eta^2 in the diamond between eta_b and eta_t on x = 0 (H = 1); returns (u, v)."""
    eta_t = -1.0
    eta_b = eta_t * np.exp(htau) if htau > 0 else None
    if htau == 0:                                    # flat control: uniform in a unit diamond
        u, v = rng.random(n), rng.random(n)
        return u, v
    # diamond in (u, v): u, v in [eta_b, eta_t]; weight 1/eta^2 with eta = (u + v)/2 < 0. Rejection sampling.
    out_u, out_v = [], []
    wmax = 1 / eta_t ** 2
    while len(out_u) < n:
        m = 4 * (n - len(out_u)) + 16
        u = eta_b + (eta_t - eta_b) * rng.random(m)
        v = eta_b + (eta_t - eta_b) * rng.random(m)
        w = 1 / ((u + v) / 2) ** 2
        keep = rng.random(m) * wmax < w
        out_u.extend(u[keep]); out_v.extend(v[keep])
    return np.array(out_u[:n]), np.array(out_v[:n])

def chain_counts(u, v, kmax):
    """c_k = number of k-element chains among the points, k = 0..kmax (c_0 = 1)."""
    order = np.argsort(u + v)
    u, v = u[order], v[order]
    C = (u[:, None] < u[None, :]) & (v[:, None] < v[None, :])     # C[i, j]: i precedes j
    n = len(u)
    ends = np.ones(n)                                # chains of length 1 ending at each point
    c = np.zeros(kmax + 1); c[0] = 1; c[1] = n
    for k in range(2, kmax + 1):
        ends = ends @ C                              # chains of length k ending at j
        c[k] = ends.sum()
        if c[k] == 0:
            break
    return c

def run(samples, seed):
    rng = np.random.default_rng(seed)
    MUS = (0.05, 0.2, 0.5)
    print(f"samples per cell {samples}, seed {seed}")
    print(" n  Htau |  g2 (c2: ordering fraction)   g3          | mean K - target (per mu), in units of sd(K)/sqrt(samples) | intervals for 3 sigma: K(mu best)  c2")
    for n in (10, 30, 60):
        kmax = n
        base = np.array([comb(n, k) / factorial(k) for k in range(kmax + 1)])
        target = {mu: 0.5 * base @ (-mu / 2) ** np.arange(kmax + 1) for mu in MUS}   # = 1/2 L_n(mu/2)
        for htau in (0.0, 0.25, 0.5, 1.0, 2.0):
            cs = np.array([chain_counts(*diamond_points(n, htau, rng), kmax) for _ in range(samples)])
            g = cs.mean(0) / base - 1
            ge = cs.std(0) / base / np.sqrt(samples)
            Ks = {mu: 0.5 * cs @ (-mu / 2) ** np.arange(kmax + 1) for mu in MUS}
            devs, need = [], []
            for mu in MUS:
                d = Ks[mu].mean() - target[mu]
                sd = Ks[mu].std()
                devs.append(f"{d:+.4f} ({d / (sd / np.sqrt(samples)):+5.1f}σ)")
                need.append(9 * sd ** 2 / d ** 2 if d != 0 else np.inf)
            sd2 = cs[:, 2].std(); d2 = cs[:, 2].mean() - base[2]
            need2 = 9 * sd2 ** 2 / d2 ** 2 if d2 != 0 else np.inf
            print(f"{n:3d} {htau:4.2f} | {g[2]:+.4f}±{ge[2]:.4f}  {g[3]:+.4f}±{ge[3]:.4f} | " + "  ".join(devs)
                  + f" | {min(need):9.0f}  {need2:9.0f}")

if __name__ == "__main__":
    run(int(sys.argv[1]) if len(sys.argv) > 1 else 3000, int(sys.argv[2]) if len(sys.argv) > 2 else 1)
