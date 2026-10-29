"""Roadmap B / idea 006: Johnston's chain-sum propagator on the N = 400 MCMC universes (job 449411) as a physical manifold test.

On ANY causal set the propagator is a chain count (b_johnston_propagator.py has the recipe, a = 1/2, b = -m^2/rho):
    K(x, y) = (1/2) sum_k c_k(x, y) (-mu/2)^k,    mu = m^2/rho,   c_k = number of k-element chains strictly inside [x, y].
Only mu enters, so no density has to be fitted.  Intrinsic target [ours, derived session 7]: in a random 2D order (= a sprinkled
diamond) the n elements of an interval are again a random 2D order, k of them form a chain with probability 1/k!, so
    E[c_k | n] = C(n, k) / k!   and   E[K | n] = (1/2) L_n(mu/2)          (Laguerre polynomial; -> (1/2) J0(sqrt(2 mu n)) for n >> 1).
n = |interval| is counted from the causal set itself.  Test: bin all related pairs by n and compare <K> with (1/2) L_n(mu/2).
Control (lesson 10): random 2D orders (beta = 0) generated here, which must pass exactly.
Usage: python3 sims/b_johnston_n400.py [n400_out_dir] [mu ...]
"""
import sys, glob, os
import numpy as np


def laguerre_table(nmax, x):
    """L_0(x) .. L_nmax(x) by the three-term recurrence."""
    L = np.empty(nmax + 1)
    L[0] = 1.0
    if nmax > 0:
        L[1] = 1.0 - x
    for n in range(1, nmax):
        L[n + 1] = ((2 * n + 1 - x) * L[n] - n * L[n - 1]) / (n + 1)
    return L


def propagator(u, v, mu):
    """All K(x, y) and interval sizes n(x, y) for a 2D order given by the permutations u, v."""
    o = np.argsort(u + v)                              # a linear extension: C becomes strictly upper triangular
    u, v = u[o], v[o]
    C = ((u[:, None] < u[None, :]) & (v[:, None] < v[None, :])).astype(float)
    n = C @ C                                          # n[x, y] = number of z with x < z < y
    Phi = 0.5 * C
    K = Phi @ np.linalg.inv(np.eye(len(u)) + mu * Phi)  # K = Phi (I - b Phi)^{-1} with b = -mu per stop (a*b = -mu/2 per extra element)
    return C.astype(bool), n.astype(int), K


def compare(u, v, mu, edges):
    C, n, K = propagator(u, v, mu)
    nn, kk = n[C], K[C]
    target = 0.5 * laguerre_table(len(u), mu / 2)[nn]
    d = kk - target
    idx = np.digitize(nn, edges) - 1
    dev = np.array([d[idx == i].mean() if (idx == i).sum() > 5 else np.nan for i in range(len(edges) - 1)])
    tgt = np.array([target[idx == i].mean() if (idx == i).sum() > 5 else np.nan for i in range(len(edges) - 1)])
    return dev, tgt, np.sqrt((d ** 2).mean()), nn.max(), (kk < 0).mean(), (target < 0).mean()


if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "n400_out"
    mus = [float(m) for m in sys.argv[2:]] or [0.05]
    edges = np.array([0, 10, 25, 50, 75, 100, 150, 200, 300, 400])
    rng = np.random.default_rng(7)
    runs = [("control b=0 #%d" % i, rng.permutation(400), rng.permutation(400)) for i in range(4)]
    for f in sorted(glob.glob(os.path.join(folder, "*.npz"))):
        if f.endswith(".partial.npz"):
            continue
        z = np.load(f)
        tag = "b={} {} s{} S/N={:.2f} layers={}".format(float(z["beta"]), str(z["start"]), int(z["seed"]), z["S_N"][-1], int(z["layers"][-1]))
        runs.append((tag, z["u"].astype(int), z["v"].astype(int)))
    for mu in mus:
        print("\nmu = m^2/rho = {}   columns: <K - L_n/2> in bins of interval size n; target <L_n/2> on the first line".format(mu))
        print("n bins: " + " ".join("{:>3}-{:<3}".format(a, b) for a, b in zip(edges[:-1], edges[1:])))
        for tag, u, v in runs:
            dev, tgt, rms, nmax, fneg, fneg_t = compare(u, v, mu, edges)
            if tag.startswith("control b=0 #0"):
                print("target  " + " ".join("{:+7.3f}".format(t) if np.isfinite(t) else "    -  " for t in tgt))
            print("{:<44} rms {:.3f}  n_max {:3d}  K<0 {:.2f} (target {:.2f})".format(tag, rms, nmax, fneg, fneg_t))
            print("        " + " ".join("{:+7.3f}".format(x) if np.isfinite(x) else "    -  " for x in dev))
