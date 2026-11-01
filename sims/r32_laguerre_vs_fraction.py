"""Does the fixed-n Laguerre target add anything to the fixed-n related fraction? (session 15; PRD referee on toolkit-1p1-v1, major item 4)
States: the N = 400 e^{-beta S} final states (runs/cluster_fetch/n400/out, as b_johnston_n400.py); null: 40 random 2D orders of the same size.
Per order, over all related pairs x < y with interval size n = |I(x,y)| >= 2:
    S_K : rms of K(x,y) - L_n(mu/2)/2                       (the paper's statistic, mu = 0.05)
    S_f : rms of c2(x,y)/C(n,2) - 1/2, with c2 = (C^3)[x,y] = related pairs inside the interval; E[c2 | n] = C(n,2)/2 in a random 2D order
Separation of a state from the null: z = (S - mean_null) / sd_null, for each statistic. If z_K is not larger than z_f, the propagator adds nothing
beyond the ordering fraction for telling layered from continuum-like orders.
Usage: python r32_laguerre_vs_fraction.py [runs/cluster_fetch/n400/out]
"""
import sys, glob, os
import numpy as np
from b_johnston_n400 import propagator, laguerre_table

MU = 0.05

def stats(u, v):
    C, n, K = propagator(u, v, MU)
    Cf = C.astype(float)
    c2 = (Cf @ Cf @ Cf)                                  # x < z < w < y: related pairs strictly inside I(x, y)
    m = C & (n >= 2)
    nn, kk, cc = n[m], K[m], c2[m]
    sK = np.sqrt(((kk - 0.5 * laguerre_table(len(u), MU / 2)[nn]) ** 2).mean())
    sf = np.sqrt(((cc / (nn * (nn - 1) / 2) - 0.5) ** 2).mean())
    return sK, sf

if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "../runs/cluster_fetch/n400/out"
    rng = np.random.default_rng(11)
    null = np.array([stats(rng.permutation(400), rng.permutation(400)) for _ in range(40)])
    mu0, sd0 = null.mean(0), null.std(0, ddof=1)
    print(f"null (40 random 2D orders, N = 400): S_K {mu0[0]:.4f} +- {sd0[0]:.4f}   S_f {mu0[1]:.4f} +- {sd0[1]:.4f}")
    print(f"{'state':<34} {'layers':>6} {'S_K':>7} {'z_K':>8} {'S_f':>7} {'z_f':>8}")
    for f in sorted(glob.glob(os.path.join(folder, "*.npz"))):
        if f.endswith(".partial.npz"):
            continue
        z = np.load(f)
        s = np.array(stats(z["u"].astype(int), z["v"].astype(int)))
        zz = (s - mu0) / sd0
        tag = "b={} {} s{}".format(float(z["beta"]), str(z["start"]), int(z["seed"]))
        print(f"{tag:<34} {int(z['layers'][-1]):>6} {s[0]:7.4f} {zz[0]:8.1f} {s[1]:7.4f} {zz[1]:8.1f}", flush=True)
