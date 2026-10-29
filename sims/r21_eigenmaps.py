"""Laplacian eigenmaps (the embedding Boguñá–Krioukov 2024 suggest for their overlap distances) vs Johnston 2025 and our count-weighted fit (idea 005, session 12).
Time coordinate: his t (as for every arm). Spatial coordinates from a k-nearest-neighbour graph on our distance matrix (related pairs: his R; spacelike: our overlap
estimate, only pairs with shared count >= 10 may be neighbours), heat-kernel weights exp(-D^2/sigma^2), sigma = median neighbour distance, normalized Laplacian;
eigenvectors 2-4 of D^-1 W [literature: Belkin-Niyogi 2003]. Eigenmaps are not metric, so three readings:
    le_oracle  : best linear map of the eigenvectors to the TRUE spatial coordinates (an upper bound on what the eigenmap shape allows; not a method)
    le_metric  : metric fixed from data only: M = A^T A fitted (linear least squares on squared distances) to our neighbour distances
    le_smacof  : le_metric as the start of a SMACOF that uses only the neighbour pairs (local stress)
Scored like r18 (spatial corr, his Table V metric), paired against johnston and the count-weighted fit (K0 = 30) on the same universes.
Usage: python r21_eigenmaps.py [n reps seed k]
"""
import sys
import numpy as np
from r11_4d_distance import load_table
from r12_johnston_compare import johnston
from r13_mixed import sprinkle
from r16_local_fit import smacof
from r18_waist_oracle import ours_with_counts
from r19_cluster_wfit import fit_w

np.seterr(all="ignore")

def eigenmap(D, ok, k):
    n = len(D)
    Dm = np.where(ok, D, np.inf); np.fill_diagonal(Dm, np.inf)
    nb = np.argsort(Dm, axis=1)[:, :k]
    A = np.zeros((n, n), bool); A[np.repeat(np.arange(n), k), nb.ravel()] = True
    A &= np.isfinite(Dm); A |= A.T
    sig = np.median(D[A])
    W = np.where(A, np.exp(-(D / sig) ** 2), 0.0)
    dg = W.sum(1); dg[dg == 0] = 1.0
    S = W / np.sqrt(dg[:, None] * dg[None, :])
    lam, vec = np.linalg.eigh(S)
    Y = vec[:, ::-1][:, 1:4] / np.sqrt(dg)[:, None]                   # eigenvectors 2-4 of D^-1 W (largest after the trivial one)
    return Y, A

def metric_fit(Y, D, A):
    """M (3x3 PSD) with dy^T M dy ~ D^2 on neighbour pairs: linear least squares in the 6 entries of M, then project to PSD; returns Y @ sqrtm(M)."""
    I, J = np.nonzero(np.triu(A, 1))
    d = Y[I] - Y[J]
    X = np.column_stack([d[:, 0] ** 2, d[:, 1] ** 2, d[:, 2] ** 2, 2 * d[:, 0] * d[:, 1], 2 * d[:, 0] * d[:, 2], 2 * d[:, 1] * d[:, 2]])
    m = np.linalg.lstsq(X, D[I, J] ** 2, rcond=None)[0]
    M = np.array([[m[0], m[3], m[4]], [m[3], m[1], m[5]], [m[4], m[5], m[2]]])
    lam, V = np.linalg.eigh(M)
    return Y @ (V * np.sqrt(np.maximum(lam, 0))) @ V.T

def run(n, reps, seed, k):
    W = load_table()
    rng = np.random.default_rng(seed)
    names = ["johnston", "w_K30", "le_oracle", "le_metric", "le_smacof"]
    rows = []
    for _ in range(reps):
        P, C, rho = sprinkle(n, rng)
        iu = np.triu_indices(len(P), 1)
        st = np.sqrt(((P[:, None, 1:] - P[None, :, 1:]) ** 2).sum(-1))[iu]
        sc = lambda Ysp: np.corrcoef(np.sqrt(((Ysp[:, None, :] - Ysp[None, :, :]) ** 2).sum(-1))[iu], st)[0, 1]
        r_j, Xj = johnston(C, rho, 1.0)
        t = Xj[:, 0]
        I, J, s, kc = ours_with_counts(C, rho, t, W)
        rel = C | C.T
        Rrel = np.where(rel, r_j, np.inf); np.fill_diagonal(Rrel, 0.0)
        Xw, _ = fit_w(Rrel, t, I, J, s, kc, 30)
        D = np.where(rel, r_j, 0.0); ok = rel.copy()
        good = np.isfinite(s)
        D[I[good], J[good]] = s[good]; D[J[good], I[good]] = s[good]
        okp = good & (kc >= 10)
        ok[I[okp], J[okp]] = True; ok[J[okp], I[okp]] = True
        Y, A = eigenmap(D, ok, k)
        Ytrue = P[:, 1:]
        B = np.linalg.lstsq(np.column_stack([Y, np.ones(len(Y))]), Ytrue, rcond=None)[0]
        Yo = np.column_stack([Y, np.ones(len(Y))]) @ B
        Ym = metric_fit(Y, D, A)
        Ys, _ = smacof(Ym.copy(), D, A.astype(float), 300)
        row = [sc(Xj[:, 1:]), sc(Xw[:, 1:]), sc(Yo), sc(Ym), sc(Ys)]
        rows.append(row)
        print("  universe %d: " % len(rows) + "  ".join("%s %.4f" % (a, v) for a, v in zip(names, row)), flush=True)
    A_ = np.array(rows); d = A_ - A_[:, :1]
    print("n = %d (%d univ., seed %d, k = %d neighbours)" % (n, reps, seed, k))
    for a, m, dm, de in zip(names, A_.mean(0), d.mean(0), d.std(0, ddof=1) / np.sqrt(reps) if reps > 1 else np.full(len(names), np.nan)):
        print("  %-10s spatial corr %.4f   vs johnston %+.4f +- %.4f   (%+.0f %% of his residual)" % (a, m, dm, de, 100 * dm / (1 - A_[:, 0].mean())))

if __name__ == "__main__":
    a = sys.argv[1:]
    run(int(a[0]) if a else 1500, int(a[1]) if len(a) > 1 else 3, int(a[2]) if len(a) > 2 else 4040, int(a[3]) if len(a) > 3 else 15)
