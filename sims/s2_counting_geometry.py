"""Stage S2 (ideas 002/004): geometry by counting, and the clock-independence test (C5b).

All quantities use only the causal matrix C[i, j] = 1 iff event i precedes event j.

* Curvature: 2D Benincasa-Dowker operator (Dowker-Glaser 2013 form), units rho = 1/l^2 = 1:
      B phi(x) = -2 phi(x) + 4 (sum_{L1} phi - 2 sum_{L2} phi + sum_{L3} phi)
  L_k = past elements y with exactly k-1 elements strictly between y and x.
  For slowly varying phi it approximates  box phi - R phi / 2, so for phi = 1:  R(x) ~ -2 B1(x).
* Dimension: Myrheim-Meyer ordering fraction r = (#comparable pairs) / (n choose 2) of an interval;
      r(d) = Gamma(d+1) Gamma(d/2) / (2 Gamma(3d/2))    (r = 1/2 for d = 2, 1/10 for d = 4).
* Clocks: height (longest chain from the beginning) vs past-volume clock sqrt(2 * #past) (2D normalisation).
"""
import math
import numpy as np

rng = np.random.default_rng(20261025)

# ---------- generators ----------
def sprinkle_flat_diamond(n):
    u, v = rng.random(n), rng.random(n)
    order = np.argsort(u + v)
    return u[order], v[order]

def sprinkle_desitter(n_target, H, eta0, eta1, L):
    """2D de Sitter, conformal patch ds^2 = (H eta)^-2 (-d eta^2 + dx^2), eta in [eta0, eta1] < 0, x in [0, L].
    Density per coordinate area = 1/(H eta)^2 (rho = 1). Returns light-cone coords and conformal time."""
    total = L * (-1 / eta1 + 1 / eta0) / H**2     # integral of (H eta)^-2 over the patch
    n = rng.poisson(total)
    w = -1 / eta0 + (-1 / eta1 + 1 / eta0) * rng.random(n)   # w = -1/eta is uniform for density ~ eta^-2
    eta = -1 / w
    x = L * rng.random(n)
    order = np.argsort(eta)
    eta, x = eta[order], x[order]
    return eta - x, eta + x, eta, total

def causal_from_uv(u, v):
    return ((u[:, None] < u[None, :]) & (v[:, None] < v[None, :])).astype(np.float32)

def causal_from_growth(past_bits, N):
    C = np.zeros((N, N), dtype=np.float32)
    for j, b in enumerate(past_bits):
        while b:
            low = b & -b
            C[low.bit_length() - 1, j] = 1
            b ^= low
    return C

# ---------- observables ----------
def bd_curvature(C):
    with np.errstate(all="ignore"):             # numpy 2.0 + Accelerate emits spurious matmul warnings
        K = C @ C                              # K[i, j] = number of z with i < z < j
    R = np.empty(C.shape[0])
    for j in range(C.shape[0]):
        past = C[:, j] > 0
        k = K[past, j]
        n1, n2, n3 = np.sum(k == 0), np.sum(k == 1), np.sum(k == 2)
        R[j] = -2 * (-2 + 4 * (n1 - 2 * n2 + n3))
    return R

def bd_curvature_smeared(C, eps, K=None):
    """Sorkin's smeared 2D operator (non-locality scale l_k = l / sqrt(eps)); reduces to bd_curvature at eps = 1:
        B_eps 1(x) = 4 eps (-1/2 + eps * sum_{y<x} f(n(x, y), eps)),
        f(n, eps) = (1-eps)^n [1 - 2 eps n/(1-eps) + eps^2 n(n-1) / (2 (1-eps)^2)].
    Returns R(x) ~ -2 B_eps 1(x)."""
    if K is None:
        with np.errstate(all="ignore"):     # numpy 2.0 + Accelerate emits spurious matmul warnings
            K = C @ C
    R = np.empty(C.shape[0])
    for j in range(C.shape[0]):
        n = K[C[:, j] > 0, j].astype(np.float64)
        if eps == 1.0:
            f = np.where(n == 0, 1.0, np.where(n == 1, -2.0, np.where(n == 2, 1.0, 0.0)))
        else:
            q = 1 - eps
            f = q**n * (1 - 2 * eps * n / q + eps**2 * n * (n - 1) / (2 * q**2))
        R[j] = -2 * 4 * eps * (-0.5 + eps * f.sum())
    return R

def mm_dimension(C, idx):
    sub = C[np.ix_(idx, idx)]
    n = len(idx)
    r = sub.sum() / (n * (n - 1) / 2)
    f = lambda d: math.gamma(d + 1) * math.gamma(d / 2) / (2 * math.gamma(3 * d / 2)) - r
    lo, hi = 1.0001, 12.0                      # r(d) decreases with d: bisection
    if f(lo) < 0 or f(hi) > 0:
        return float("nan")
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(mid) > 0 else (lo, mid)
    return (lo + hi) / 2

def heights(C):
    N = C.shape[0]
    h = np.zeros(N, dtype=int)
    for j in range(N):                      # events are in a linear extension (causes before effects)
        p = np.nonzero(C[:j, j])[0]
        h[j] = h[p].max() + 1 if p.size else 0
    return h

def interval(C, i, j):
    return np.nonzero((C[i, :] > 0) & (C[:, j] > 0))[0].tolist() + [i, j]

def clock_disagreement(C, h, nsample=40000, seed=0):
    """Fraction of spacelike pairs that the height clock and the past-volume clock order differently.
    Causally related pairs are ordered identically by any clock that grows along chains, so only spacelike
    pairs (where 'which is earlier' is a convention) can disagree. Pairs tied in height are skipped."""
    r = np.random.default_rng(seed)
    V = C.sum(0)                                  # number of events in the past of each event
    N = C.shape[0]
    i, j = r.integers(0, N, nsample), r.integers(0, N, nsample)
    keep = (i != j) & (C[i, j] == 0) & (C[j, i] == 0) & (h[i] != h[j]) & (V[i] != V[j])
    i, j = i[keep], j[keep]
    dis = np.sign(h[i] - h[j]) != np.sign(V[i] - V[j])
    dh = np.abs(h[i] - h[j])
    return dis.mean(), [(lo, dis[(dh >= lo) & (dh < hi)].mean(), int(((dh >= lo) & (dh < hi)).sum()))
                        for lo, hi in [(1, 2), (2, 4), (4, 8), (8, 16), (16, 10**9)] if ((dh >= lo) & (dh < hi)).sum() > 50]

if __name__ == "__main__":
    import sys
    sys.path.insert(0, __file__.rsplit("/", 1)[0])
    from growth_percolation import grow

    print("A) curvature by counting, validation (smeared BD operator, rho = 1)")
    u, v = sprinkle_flat_diamond(4000)
    C = causal_from_uv(u, v)
    R, pastn = bd_curvature_smeared(C, 0.03), C.sum(0)
    sel = pastn > 1000
    print(f"   flat diamond:  R = {R[sel].mean():+.5f}  (expected 0)")
    for H in [0.05, 0.08]:
        eta0, eta1 = -4 / H, -0.5 / H
        L = 8000 * H / 1.75
        u, v, eta, _ = sprinkle_desitter(None, H, eta0, eta1, L)
        x = (v - u) / 2
        C = causal_from_uv(u, v)
        R, pastn = bd_curvature_smeared(C, 0.03), C.sum(0)
        sel = (pastn > 330) & (x > 0.2 * L) & (x < 0.8 * L)
        print(f"   de Sitter H={H}: R = {R[sel].mean():.5f}  (expected 2H^2 = {2*H*H:.5f})")

    N = 4000
    print("\nB) Myrheim-Meyer dimension of grown universes (interval first event -> event at given layer)")
    r = np.random.default_rng(3)
    for label, kw in [("fixed p=0.02", dict(p=0.02, originary=True)), ("p=3/n", dict(p=None, originary=True, c=3))]:
        past, _ = grow(N, seed=1, **kw)
        C = causal_from_growth(past, N)
        h = heights(C)
        row = []
        for frac in [0.3, 0.5, 0.7, 0.85]:
            layer = int(frac * h.max())
            cand = np.nonzero(h == layer)[0]
            ds = [mm_dimension(C, np.array(interval(C, 0, t))) for t in r.choice(cand, min(8, len(cand)), replace=False)]
            row.append(f"layer {layer}: d={np.nanmean(ds):.2f}")
        print(f"   {label}: " + " | ".join(row))

    print("\nC) clock independence: height vs past-volume ordering of spacelike pairs")
    u, v = sprinkle_flat_diamond(N - 1)
    u, v = np.r_[0, u], np.r_[0, v]
    cases = [("flat 2D diamond", causal_from_uv(u, v))]
    for label, kw in [("fixed p=0.02", dict(p=0.02, originary=True)), ("p=3/n", dict(p=None, originary=True, c=3))]:
        past, _ = grow(N, seed=1, **kw)
        cases.append((label, causal_from_growth(past, N)))
    for label, C in cases:
        tot, by = clock_disagreement(C, heights(C))
        print(f"   {label}: overall {tot:.3f}; by layer separation " + ", ".join(f"{a}+: {b:.3f}" for a, b, _ in by))
