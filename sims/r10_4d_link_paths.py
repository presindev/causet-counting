"""3+1 fixed-n target for Johnston's propagator? (idea 006, session 11; Part I note "item 1" of the 3+1 assessment.)

In 3+1 Johnston's particle hops along LINKS only (Johnston 2008): K = Phi (I - b Phi)^{-1}, Phi = a L, a = sqrt(rho)/(2 pi sqrt 6), b = -m^2/rho.
So K(x, y)/a = sum_k (-nu)^{k-1} P_k(x, y), nu = m^2 / (2 pi sqrt(6 rho)), P_k = number of k-hop link paths from x to y.
The 1+1 target (Laguerre) was exact because a chain only needs its points ordered (probability 1/k!). A link path also needs every skipped sub-interval empty,
so E[P_k | n] carries factors (1 - W/V)^(n-k+1): no 1/k!-style closed form. This script measures E[P_k | n] for n points uniform in a 3+1 interval.
Hand estimate (session 11): E[P_2 | n] -> 3 pi ~ 9.42 as n -> oo (points near the waist of the diamond), and then a nu P_2 -> m^2/(8 pi),
the short-distance limit of the continuum mass term -(m / 4 pi tau) J_1(m tau). Dimensional guess for higher k: E[P_k | n] ~ C_k n^((k-2)/2).
Usage: python r10_4d_link_paths.py [reps=200]
"""
import sys
import numpy as np

np.seterr(all="ignore")                          # numpy + Accelerate: spurious matmul warnings

def interval_4d(n, rng):
    """n points uniform in the 3+1 Alexandrov interval between (-1, 0) and (1, 0), plus the two tips (index 0 = bottom, n+1 = top)."""
    pts = []
    while len(pts) < n:
        m = 4 * (n - len(pts)) + 16
        t = 2 * rng.random(m) - 1
        x = 2 * rng.random((m, 3)) - 1
        r = np.sqrt((x ** 2).sum(1))
        ok = r < 1 - np.abs(t)
        pts.extend(np.column_stack([t[ok], x[ok]]))
    P = np.vstack([[-1, 0, 0, 0], np.array(pts[:n]), [1, 0, 0, 0]])
    return P[np.argsort(P[:, 0])]

def link_paths(P, kmax):
    dt = P[None, :, 0] - P[:, None, 0]
    dr2 = ((P[None, :, 1:] - P[:, None, 1:]) ** 2).sum(-1)
    C = ((dt > 0) & (dt ** 2 > dr2)).astype(np.float32)
    L = ((C > 0) & ((C @ C) == 0)).astype(np.float64)           # links: related with nothing in between
    out = np.zeros(kmax + 1)
    v = np.zeros(len(P)); v[0] = 1.0                            # paths from the bottom tip
    for k in range(1, kmax + 1):
        v = v @ L
        out[k] = v[-1]                                          # k-hop link paths ending at the top tip
    return out

if __name__ == "__main__":
    reps = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    rng = np.random.default_rng(1)
    kmax = 6
    print(f"3+1 interval, n uniform points, {reps} samples per n (fewer at large n); mean P_k +- s.e.;  E[P_2|n] predicted -> 3 pi = {3 * np.pi:.3f}")
    print("    n   " + "  ".join(f"{'P_' + str(k):>16}" for k in range(2, kmax + 1)))
    for n in (10, 30, 100, 300, 1000, 2000):
        r = reps if n <= 300 else max(20, reps // 10)
        S = np.array([link_paths(interval_4d(n, rng), kmax) for _ in range(r)])
        m, e = S.mean(0), S.std(0) / np.sqrt(r)
        print(f"{n:6d}  " + "  ".join(f"{m[k]:9.3f}±{e[k]:6.3f}" for k in range(2, kmax + 1)) + f"   ({r} samples)", flush=True)
