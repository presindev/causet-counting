"""Roadmap B, first actor: Johnston's chain-sum propagator on a sprinkled 1+1 causal diamond (idea 006).

Johnston, CQG 25, 202001 (2008), arXiv:0806.3083, eqs. 3.1, 3.5, 3.31:
    a particle goes from x to y by n hops along causal relations (any x < z, not only links) with n - 1 stops in between;
    amplitude a per hop, b per stop.  In 1+1:  a = 1/2,  b = -m^2/rho.
    Phi = a C  (C[x, y] = 1 if x < y),   K = Phi (I - b Phi)^{-1}  (the n >= 1 part of eq. 3.5).
Continuum target (eqs. 3.23-3.24): K(x, y) = (1/2) J0(m tau_xy) for x < y, with (box + m^2) K = delta.
Why it works on average: the expected number of chains x < z1 < ... < z_k < y in 1+1 is (rho tau^2/2)^k / (k!)^2, so
    E[K] = a sum_k (a b rho tau^2/2)^k / (k!)^2 = (1/2) sum_k (-(m tau/2)^2)^k / (k!)^2 = (1/2) J0(m tau).
So m = 0 is exact for every sprinkling (K = a C) and only m > 0 tests anything.

Setup: diamond with tips at proper time 0 and T (light-cone coords u, v in [0, T/sqrt2]), the bottom tip x0 inserted by hand
(lesson 9), N ~ Poisson(rho T^2/2) sprinkled points.  We compute the row K[x0, :] by one triangular solve and compare it with
(1/2) J0(m tau) in tau bins.  Errors: spread of the bin means across independent seeds (lesson 8).  We also quote the
per-element scatter inside a bin: how noisy K is on ONE causal set.
Usage: python3 sims/b_johnston_propagator.py [rho] [T] [m] [seeds]
"""
import sys, time
import numpy as np


def j0(x):
    """Bessel J0 by J0(x) = (1/pi) int_0^pi cos(x sin th) dth (no scipy on the laptop)."""
    th = (np.arange(400) + 0.5) * np.pi / 400
    return np.cos(np.outer(np.atleast_1d(x), np.sin(th))).mean(axis=1)


def sprinkle(rho, T, rng):
    s = T / np.sqrt(2)                                 # side of the diamond in light-cone coordinates
    n = rng.poisson(rho * T * T / 2)
    u, v = rng.random(n) * s, rng.random(n) * s
    u, v = np.concatenate([[0.0], u]), np.concatenate([[0.0], v])   # element 0 = bottom tip, by hand
    o = np.argsort(u + v)                              # time order: C becomes strictly upper triangular
    return u[o], v[o]


def row_from_tip(u, v, m, rho):
    """K[x0, :] with x0 = element 0, by solving k (I - b Phi) = Phi[0, :]."""
    a, b = 0.5, -m * m / rho
    C = ((u[:, None] < u[None, :]) & (v[:, None] < v[None, :])).astype(float)
    Phi = a * C
    A = np.eye(len(u)) - b * Phi
    return np.linalg.solve(A.T, Phi[0])               # row vector k with k A = Phi[0]


def run(rho, T, m, seeds, nbins=16):
    edges = np.linspace(0, T, nbins + 1)
    means, scat = np.full((seeds, nbins), np.nan), np.full((seeds, nbins), np.nan)
    t0 = time.time()
    for s in range(seeds):
        rng = np.random.default_rng(1000 + s)
        u, v = sprinkle(rho, T, rng)
        k = row_from_tip(u, v, m, rho)[1:]
        tau = np.sqrt(2 * u[1:] * v[1:])               # tau^2 = 2 u v from the tip (t = (u+v)/sqrt2, x = (u-v)/sqrt2)
        d = k - 0.5 * j0(m * tau)                      # deviation from the continuum, element by element
        idx = np.digitize(tau, edges) - 1
        for i in range(nbins):
            sel = idx == i
            if sel.sum() > 2:
                means[s, i] = d[sel].mean()
                scat[s, i] = d[sel].std()
    mid = 0.5 * (edges[1:] + edges[:-1])
    print("rho={} T={} m={} (m^2/rho={:.3g}) seeds={}  N~{:.0f}  {:.1f}s".format(rho, T, m, m * m / rho, seeds,
                                                                                rho * T * T / 2, time.time() - t0))
    print(" m*tau   G=J0/2    <K-G> over seeds (sd across seeds)   per-element scatter of K-G on one causet")
    for i in range(nbins):
        print("{:6.2f}  {:+.3f}    {:+.4f} ({:.4f})                     {:.3f}".format(
            m * mid[i], 0.5 * j0(m * mid[i])[0], np.nanmean(means[:, i]), np.nanstd(means[:, i], ddof=1),
            np.nanmean(scat[:, i])))
    return mid, means, scat


if __name__ == "__main__":
    rho = float(sys.argv[1]) if len(sys.argv) > 1 else 100.0
    T = float(sys.argv[2]) if len(sys.argv) > 2 else 8.0
    m = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    seeds = int(sys.argv[4]) if len(sys.argv) > 4 else 8
    run(rho, T, m, seeds)
