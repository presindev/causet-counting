"""Idea 006: Johnston's chain-sum propagator on the S1 grown universes (transitive percolation, growth_percolation.py).

Same test as b_johnston_n400.py: for every related pair x < y, n = |interval| and K(x, y) = (1/2) sum_k c_k (-mu/2)^k, compared with the exact
2D-sprinkling target (1/2) L_n(mu/2).  Expanding in mu: K/(1/2) = 1 - (mu/2) n + (mu/2)^2 c_2 - ..., and a 2D interval has E[c_2 | n] = n(n-1)/4,
i.e. ordering fraction 1/2.  So the first order that can fail IS the Myrheim-Meyer dimension of the interval; higher orders bring in longer chains.
The test asks "does a 2D massive particle propagate here?", not "is this a manifold of some dimension".
A2 is not tested: its exact sums stop at N = 8, intervals have <= 6 elements, and one oscillation of J0 needs n ~ 3/mu ~ 60 at mu = 0.05.
For context we print the Myrheim-Meyer dimension of the 20 largest intervals (median).
Usage: python3 sims/b_johnston_grown.py [N] [mu] [seeds]
"""
import sys
import numpy as np
from b_johnston_n400 import laguerre_table
from growth_percolation import grow
from s2_counting_geometry import causal_from_growth, mm_dimension


def test(C, mu, edges):
    C = C.astype(float)
    N = len(C)
    rel = C > 0
    n = (C @ C)[rel].astype(int)
    K = (0.5 * C @ np.linalg.inv(np.eye(N) + mu * 0.5 * C))[rel]
    target = 0.5 * laguerre_table(N, mu / 2)[n]
    d = K - target
    idx = np.digitize(n, edges) - 1
    dev = [d[idx == i].mean() if (idx == i).sum() > 5 else np.nan for i in range(len(edges) - 1)]
    # Myrheim-Meyer dimension of the largest intervals
    big = np.argsort(-(C @ C)[rel])[:20]
    xs, ys = np.nonzero(rel)
    dims = [mm_dimension(C, np.nonzero(C[xs[b]] * C[:, ys[b]])[0]) for b in big]
    return np.array(dev), np.sqrt((d ** 2).mean()), n.max(), (K < 0).mean(), (target < 0).mean(), np.nanmedian(dims), np.abs(K).max()


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
    mu = float(sys.argv[2]) if len(sys.argv) > 2 else 0.05
    seeds = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    edges = np.array([0, 10, 25, 50, 75, 100, 150, 200, 300, 500, 1000, 1500])
    rng = np.random.default_rng(11)
    cases = []
    for s in range(seeds):
        u, v = rng.permutation(N), rng.permutation(N)
        o = np.argsort(u + v)
        u, v = u[o], v[o]
        cases.append(("control: random 2D order", (u[:, None] < u[None, :]) & (v[:, None] < v[None, :])))
    for label, kw in [("S1 fixed p = 0.02", dict(p=0.02)), ("S1 fixed p = 0.05", dict(p=0.05)), ("S1 p = 3/n", dict(p=None, c=3))]:
        for s in range(1, seeds + 1):
            cases.append((label, causal_from_growth(grow(N, seed=s, originary=True, **kw)[0], N)))
    print("N = {}, mu = m^2/rho = {}.  Rows: <K - L_n/2> in bins of interval size n.".format(N, mu))
    print("{:<26}".format("n bins") + " ".join("{:>4}-{:<4}".format(a, b) for a, b in zip(edges[:-1], edges[1:])))
    for label, C in cases:
        dev, rms, nmax, fneg, fneg_t, dmm, kmax = test(C, mu, edges)
        print("{:<26}".format(label) + " ".join("{:+9.3f}".format(x) if np.isfinite(x) else "     -   " for x in dev))
        print("{:<26}rms {:.3g}  n_max {}  K<0 {:.2f} (2D target {:.2f})  max|K| {:.3g}  d_MM(big intervals) {:.2f}"
              .format("", rms, nmax, fneg, fneg_t, kmax, dmm))
