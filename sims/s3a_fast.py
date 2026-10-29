"""S3a with an O(N^2) Metropolis step instead of O(N^3) (same model as s3a_mcmc_2d.py).

A proposal swaps two entries of u (or v), which changes the relations of only the two events a, b involved:
C' = C + E with E nonzero only in rows/columns P = {a, b}. Then
    K' = C' C' = C C + C' E + E C,
and both products are cheap because E is "thin" (split E = E_rows + E_cols, each touching at most 2 rows or
2 columns). The action needs N_n = #related pairs with n events between, read off K' on the related pairs.
"""
import sys
import numpy as np
from s3a_mcmc_2d import f_weights, causal

np.seterr(all="ignore")                           # numpy 2.0 + Accelerate emits spurious matmul warnings

def thin_left(X, E, P):
    """X @ E for E nonzero only in rows P or columns P."""
    out = X[:, P] @ E[P, :]                       # part of E living in rows P
    E2 = E[:, P].copy(); E2[P, :] = 0              # remaining part: columns P, rows outside P
    out[:, P] += X @ E2
    return out

def thin_right(E, X, P):
    """E @ X for E nonzero only in rows P or columns P."""
    out = np.zeros_like(X)
    out[P, :] = E[P, :] @ X
    E2 = E[:, P].copy(); E2[P, :] = 0
    out += E2 @ X[P, :]
    return out

def action_from(C, K, eps, fw):
    Nn = np.bincount(K[C > 0].astype(int), minlength=len(fw))
    return 4 * eps * (C.shape[0] - 2 * eps * np.dot(Nn, fw[:len(Nn)]))

def samples(N, beta, eps, n_samples=10, sweeps_between=20, burn_in=200, seed=1):
    rng = np.random.default_rng(seed)
    u, v = rng.permutation(N), rng.permutation(N)
    fw = f_weights(N, eps)
    C = causal(u, v)
    K = C @ C
    S = action_from(C, K, eps, fw)
    out = []
    total = (burn_in + n_samples * sweeps_between) * N
    for t in range(total):
        w = u if rng.random() < 0.5 else v
        a, b = rng.integers(0, N, 2)
        if a != b:
            w[a], w[b] = w[b], w[a]
            P = np.array([a, b])
            C2 = C.copy()
            C2[P, :] = (u[P, None] < u[None, :]) & (v[P, None] < v[None, :])
            C2[:, P] = (u[:, None] < u[None, P]) & (v[:, None] < v[None, P])
            E = C2 - C
            K2 = K + thin_left(C2, E, P) + thin_right(E, C, P)
            S2 = action_from(C2, K2, eps, fw)
            if np.log(rng.random()) < -beta * (S2 - S):
                C, K, S = C2, K2, S2
            else:
                w[a], w[b] = w[b], w[a]
        if t >= burn_in * N and (t - burn_in * N) % (sweeps_between * N) == 0:
            out.append(C.copy())
    return out

if __name__ == "__main__":
    # correctness check against the full recomputation, then a timing
    import time
    from s3a_mcmc_2d import action
    rng = np.random.default_rng(0)
    N, eps = 40, 0.21
    fw = f_weights(N, eps)
    u, v = rng.permutation(N), rng.permutation(N)
    C = causal(u, v); K = C @ C
    for _ in range(200):
        w = u if rng.random() < 0.5 else v
        a, b = rng.choice(N, 2, replace=False)
        w[a], w[b] = w[b], w[a]
        P = np.array([a, b])
        C2 = C.copy()
        C2[P, :] = (u[P, None] < u[None, :]) & (v[P, None] < v[None, :])
        C2[:, P] = (u[:, None] < u[None, P]) & (v[:, None] < v[None, P])
        E = C2 - C
        K = K + thin_left(C2, E, P) + thin_right(E, C, P)
        C = C2
        assert np.array_equal(K, C @ C) and np.isclose(action_from(C, K, eps, fw), action(u, v, eps, fw)[0])
    print("incremental update matches full recomputation (200 random swaps)")
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    t0 = time.time(); samples(n, 0.1, eps, n_samples=1, sweeps_between=1, burn_in=5); dt = time.time() - t0
    print(f"N = {n}: {dt / 6:.2f} s per sweep")
