"""Stage S4a (idea 005): spatial distances from the causal order alone, validated on flat 2D sprinklings.

Setup: N events sprinkled uniformly in the unit square of light-cone coordinates (u, v) in [0, 1]^2
(u = t - x, v = t + x, so dt dx = du dv / 2 and the density is rho = 2N). For spacelike a, b the true
distance is d^2 = |du| |dv|.

For an event c in the common past of a and b (all counts use only the causal matrix):
    A = I(c,a) \\ I(c,b),   B = I(c,b) \\ I(c,a),   C = I(c,a) & I(c,b)      (Boguna-Krioukov regions)

Estimators of d:
  * BK (Boguna-Krioukov 2024, Eqs. 16, 24, 34): keep only c with roughly equal intervals to a and b,
        O = N_C / (min(N_A, N_B) + N_C),   d = tau_c (1 - O) / sqrt(O),   tau_c^2 = 2 V[A u C] (2D volume).
  * Rectangle identity [ours, 2D only]: in 1+1, I(c,a) and I(c,b) are rectangles in (u, v), and the big
    rectangle from c to the join of a and b splits into four: C, A, B and the diamond D spanned by a and b.
    Opposite rectangles have equal products, so V_D = V_A V_B / V_C, i.e.
        d^2 = 2 V_D = 2 N_A N_B / (rho N_C)        for ANY c in the common past (no filtering needed).
"""
import numpy as np

def sprinkle(n, rng):
    u, v = rng.random(n), rng.random(n)
    order = np.argsort(u + v)
    return u[order], v[order]

def causal(u, v):
    return ((u[:, None] < u[None, :]) & (v[:, None] < v[None, :])).astype(np.float32)

def pair_counts(C, K, a, b):
    """For every c in the common past of a and b: N_A, N_B, N_C (events strictly between)."""
    w = C[:, a] * C[:, b]                      # events in the common past of a and b
    with np.errstate(all="ignore"):            # numpy 2.0 + Accelerate emits spurious matmul warnings
        nC = C @ w                             # nC[c] = #z with c < z, z < a, z < b
    cs = np.flatnonzero(w)
    nC = nC[cs]
    nA = K[cs, a] - nC
    nB = K[cs, b] - nC
    return nA, nB, nC

def est_rectangle(nA, nB, nC, rho, min_nC=1):
    """Rectangle identity: median over all c with N_C >= min_nC (robust to shallow c's with tiny counts)."""
    m = nC >= min_nC
    if not m.any():
        return np.nan
    return np.sqrt(np.median(2 * nA[m] * nB[m] / (rho * nC[m])))

def est_rectangle_deepest(nA, nB, nC, rho):
    k = np.argmax(nC)
    return np.sqrt(2 * nA[k] * nB[k] / (rho * (nC[k] + 1)))      # Poisson-unbiased 1/(N_C + 1), as in the Part I note Eq. (4) (session 11)

def est_bk(nA, nB, nC, rho):
    """BK second filter (their Eq. 34) with prefactor 1/2, then average d over the selected c."""
    nAC, nBC = nA + nC, nB + nC
    O = nC / (np.minimum(nA, nB) + nC)
    ok = (np.abs(nAC - nBC) < 0.5 * np.sqrt(nAC + nBC) * np.sqrt(np.clip(1 - O, 0, None))) & (nC > 0)
    if not ok.any():
        return np.nan, 0
    tau = np.sqrt(2 * 0.5 * (nAC[ok] + nBC[ok]) / rho)      # tau^2 = 2 V in 2D
    d = tau * (1 - O[ok]) / np.sqrt(O[ok])
    return np.mean(d), ok.sum()

def run(n, n_pairs, seed):
    rng = np.random.default_rng(seed)
    u, v = sprinkle(n, rng)
    rho = 2 * n
    C = causal(u, v)
    with np.errstate(all="ignore"):
        K = C @ C
    # candidate a, b: late events (big common past), spacelike to each other
    late = np.flatnonzero(u + v > 1.2)
    rows = []
    while len(rows) < n_pairs:
        a, b = rng.choice(late, 2, replace=False)
        du, dv = u[b] - u[a], v[b] - v[a]
        if du * dv >= 0:
            continue                            # timelike (or null): skip
        d_true = np.sqrt(-du * dv)
        nA, nB, nC = pair_counts(C, K, a, b)
        d_bk, n_ok = est_bk(nA, nB, nC, rho)
        rows.append((d_true, est_rectangle(nA, nB, nC, rho, min_nC=10),
                     est_rectangle_deepest(nA, nB, nC, rho), d_bk, n_ok))
    return np.array(rows), rho

if __name__ == "__main__":
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    n_pairs, seeds = 300, [1, 2, 3, 4]
    ell = None
    edges_in_ell = [0, 2, 5, 10, 20, 40, 1000]
    names = ["rect median", "rect deepest", "BK"]
    per_seed = []                              # per seed, per bin: median relative error for each estimator
    for s in seeds:
        R, rho = run(n, n_pairs, s)
        ell = rho ** -0.5
        x = R[:, 0] / ell
        out = []
        for lo, hi in zip(edges_in_ell[:-1], edges_in_ell[1:]):
            m = (x >= lo) & (x < hi)
            out.append([np.nanmedian(np.abs(R[m, k] / R[m, 0] - 1)) if m.sum() > 3 else np.nan
                        for k in (1, 2, 3)] + [m.sum(), np.nanmedian(R[m, 4]) if m.any() else np.nan])
        per_seed.append(out)
    P = np.array(per_seed)                     # seeds x bins x 5
    print(f"N = {n}, rho = {2*n}, ell = rho^-1/2 = {ell:.4f}; {n_pairs} pairs x {len(seeds)} seeds")
    print("median |d_est/d_true - 1| per distance bin; mean +- spread over seeds")
    print(f"{'d / ell':>10} {'pairs':>6} " + " ".join(f"{s:>18}" for s in names) + f" {'BK c kept':>9}")
    for i, (lo, hi) in enumerate(zip(edges_in_ell[:-1], edges_in_ell[1:])):
        cells = []
        for k in range(3):
            col = P[:, i, k]
            cells.append(f"{np.nanmean(col):8.3f} +- {np.nanstd(col):6.3f}")
        print(f"{f'{lo}-{hi}':>10} {int(P[:, i, 3].sum()):>6} " + " ".join(f"{c:>18}" for c in cells)
              + f" {np.nanmean(P[:, i, 4]):>9.1f}")
