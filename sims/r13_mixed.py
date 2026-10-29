"""Mixed spacelike distances: our overlap estimate for close pairs, Johnston's detours (min-plus) for far pairs, with our close-pair estimates allowed
as detour legs (idea 005, session 11; Roberto's suggestion). Plus a timing comparison of the two pipelines.

Why it could work (r12_err_by_distance.txt): his 2-leg detour x -> z -> y (z related to both) is good for far pairs (many z near the straight line,
err 6 %) and bad for close ones (no z between them, err 34-48 %); our overlap estimate is the reverse (16-21 % close, 12 % far, biased low).
Edges: related pairs -> his R (spatial separation from t and tau); spacelike pairs whose estimated spatial distance is < L -> ours.
    final r = ours for spacelike pairs with est < L ("short"), shortest route over the edge graph otherwise; routes of up to 2 or 4 legs (min-plus once / twice).
Risk: the shortest of many noisy routes is biased low; our legs are already ~10-15 % low.
Usage: python r13_mixed.py [bench|timing|holdout]
"""
import sys
import time
import numpy as np
from r11_4d_distance import uniform_in_diamond, precedes, load_table, dist_from_counts
from r12_johnston_compare import johnston, mink, C4

np.seterr(all="ignore")

def minplus_rows(A, B):
    """(A (x) B)[x, y] = min_z A[x, z] + B[z, y], row by row (n x n temporaries only)."""
    out = np.empty((len(A), B.shape[1]))
    for x in range(len(A)):
        out[x] = np.min(A[x][:, None] + B, axis=0)
    return out

def ours_spatial(C, rho, t, W, min_count=1):
    """Our spacelike spatial distance for every spacelike pair: d from (|I(ref,a)|, |I(ref,b)|, common) with ref = v1 or vn (side with more events),
    spatial = sqrt(d^2 + dt^2). Returns the n x n matrix (nan where not spacelike or counts < min_count)."""
    n = len(C)
    Cf = C.astype(np.float32)
    past = Cf.copy(); past[0] = 0; past[-1] = 0
    fut = Cf.T.copy(); fut[0] = 0; fut[-1] = 0
    cp, cf = past.T @ past, fut.T @ fut
    npst, nfut = past.sum(0), fut.sum(0)
    iu = np.triu_indices(n, 1)
    sp = ~(C | C.T)[iu]
    I, J = iu[0][sp], iu[1][sp]
    use_p = np.minimum(npst[I], npst[J]) >= np.minimum(nfut[I], nfut[J])
    na = np.where(use_p, npst[I], nfut[I]); nb = np.where(use_p, npst[J], nfut[J]); nc = np.where(use_p, cp[I, J], cf[I, J])
    ok = np.minimum(na, nb) >= min_count
    d = dist_from_counts(W, na[ok], nb[ok], nc[ok], 1.0) / rho ** 0.25
    S = np.full((n, n), np.nan)
    est = np.sqrt(d ** 2 + (t[I[ok]] - t[J[ok]]) ** 2)
    S[I[ok], J[ok]] = est; S[J[ok], I[ok]] = est
    return S

def embed_from_r(r, t):
    X = 0.5 * (r[0][:, None] ** 2 + r[0][None, :] ** 2 - r ** 2)
    lam, vec = np.linalg.eigh(X)
    o = np.argsort(lam)[::-1][:3]
    return np.column_stack([t, vec[:, o] * np.sqrt(np.maximum(lam[o], 0))])

def mixed(C, r_j, t, S, L, legs=2, keep_short=True):
    """r_j, t from johnston(); S from ours_spatial. Edges: related -> his R; spacelike with S < L -> S. Spacelike pairs: shortest route of <= legs legs
    (legs = 2 or 4); pairs with S < L keep S itself if keep_short, else min(S, route)."""
    rel = C | C.T
    E = np.where(rel, r_j, np.inf)
    short = ~rel & (S < L)                                          # nan < L is False
    E[short] = S[short]
    np.fill_diagonal(E, 0.0)
    sp = ~rel & ~np.eye(len(C), dtype=bool)
    rows = np.flatnonzero(sp.any(1))
    D = E.copy()
    D[rows] = np.minimum(E[rows], minplus_rows(E[rows], E))         # <= 2 legs
    if legs == 4:
        D = np.minimum(D, minplus_rows(D, D))                      # <= 4 legs
    r = np.where(sp, D, r_j)
    if keep_short:
        r[short] = S[short]
    return r

def sprinkle(n, rng):
    P = uniform_in_diamond(rng.poisson(n), 1.0, rng)
    P = np.vstack([np.zeros(4), P, [1, 0, 0, 0]]); P = P[np.argsort(P[:, 0])]
    return P, precedes(P, P), n / C4

def part_bench():
    W = load_table()
    rng = np.random.default_rng(31)
    variants = [("switch L=.25", .25, 0), ("switch L=.35", .35, 0),
                ("mix2 L=.25", .25, 2), ("mix2 L=.35", .35, 2), ("mix4 L=.25", .25, 4)]
    print("Mixed spacelike distances in Johnston's pipeline (diamond T = 1, half-width 0.5). Spatial corr (his Table V metric);"
          " paired difference vs Johnston on the same universes (mean +- s.e.)")
    print("  switch: ours if est < L else his r;  mixK: ours if est < L, else shortest route of <= K legs over his related edges + our short edges")
    for n, reps in ((500, 6), (1000, 6), (1500, 4), (3000, 2)):
        rows = []
        for _ in range(reps):
            P, C, rho = sprinkle(n, rng)
            iu = np.triu_indices(len(P), 1)
            st = np.sqrt(((P[:, None, 1:] - P[None, :, 1:]) ** 2).sum(-1))[iu]
            sc = lambda X: np.corrcoef(np.sqrt(((X[:, None, 1:] - X[None, :, 1:]) ** 2).sum(-1))[iu], st)[0, 1]
            r_j, Xj = johnston(C, rho, 1.0)
            t = Xj[:, 0]
            S = ours_spatial(C, rho, t, W)
            row = [sc(Xj)]
            for name, L, legs in variants:
                if legs == 0:
                    r = np.where((C | C.T) | ~(S < L), r_j, S)
                else:
                    r = mixed(C, r_j, t, S, L, legs)
                row.append(sc(embed_from_r(r, t)))
            rows.append(row)
        A = np.array(rows)
        dif = A[:, 1:] - A[:, :1]
        print(f"  n = {n} ({reps} univ.): Johnston {A[:, 0].mean():.4f} | " +
              " | ".join(f"{v[0]} {A[:, k + 1].mean():.4f} ({dif[:, k].mean():+.4f}+-{dif[:, k].std(ddof=1) / np.sqrt(reps):.4f})"
                         for k, v in enumerate(variants)), flush=True)

def part_timing():
    """Wall-clock of the pieces. Shared by both: causal matrix, interval counts (C @ C), time coordinate, final eigendecomposition.
    Johnston only: min-plus over z (numpy, row by row, as in r12). Ours only: two more matrix products (common pasts, futures) + table inversion."""
    W = load_table()
    rng = np.random.default_rng(5)
    print("Timing (laptop, numpy + Accelerate BLAS, one universe per n), seconds")
    print("      n         C@C   his min-plus   ours (2 matmul + inversion)   eigh")
    for n in (500, 1000, 2000, 3000, 4000):
        P, C, rho = sprinkle(n, rng)
        Cf = C.astype(np.float32)
        t0 = time.perf_counter(); _ = Cf @ Cf; t1 = time.perf_counter()
        r_j, Xj = johnston(C, rho, 1.0); t2 = time.perf_counter()
        S = ours_spatial(C, rho, Xj[:, 0], W); t3 = time.perf_counter()
        M = rng.random(C.shape); _ = np.linalg.eigh(M + M.T); t4 = time.perf_counter()
        his = (t2 - t1) - (t1 - t0) - (t4 - t3)                      # johnston() = C@C + min-plus + eigh
        print(f"  {len(P):6d}   {t1 - t0:9.3f}   {his:12.3f}   {t3 - t2:27.3f}   {t4 - t3:6.3f}", flush=True)

def part_holdout():
    """The switch won in part_bench with L = .25 and .35 chosen by hand. Fresh seeds, an L scan, both of his metrics (Tables IV and V)."""
    W = load_table()
    rng = np.random.default_rng(777)
    Ls = (0.15, 0.2, 0.25, 0.3)
    print("Holdout (fresh seeds): switch = ours if est < L else his r. Spatial corr / Minkowski corr; paired spatial difference vs Johnston")
    for n, reps in ((500, 10), (1000, 8), (1500, 6), (3000, 3)):
        rows = []
        for _ in range(reps):
            P, C, rho = sprinkle(n, rng)
            iu = np.triu_indices(len(P), 1)
            st = np.sqrt(((P[:, None, 1:] - P[None, :, 1:]) ** 2).sum(-1))[iu]; mt = mink(P)[iu]
            sc = lambda X: [np.corrcoef(np.sqrt(((X[:, None, 1:] - X[None, :, 1:]) ** 2).sum(-1))[iu], st)[0, 1], np.corrcoef(mink(X)[iu], mt)[0, 1]]
            r_j, Xj = johnston(C, rho, 1.0)
            S = ours_spatial(C, rho, Xj[:, 0], W)
            row = sc(Xj)
            for L in Ls:
                row += sc(embed_from_r(np.where((C | C.T) | ~(S < L), r_j, S), Xj[:, 0]))
            rows.append(row)
        A = np.array(rows)
        print(f"  n = {n} ({reps} univ.): Johnston {A[:, 0].mean():.4f}/{A[:, 1].mean():.4f} | " + " | ".join(
            f"L={L} {A[:, 2 + 2 * k].mean():.4f}/{A[:, 3 + 2 * k].mean():.4f} ({(A[:, 2 + 2 * k] - A[:, 0]).mean():+.4f}"
            f"+-{(A[:, 2 + 2 * k] - A[:, 0]).std(ddof=1) / np.sqrt(reps):.4f})" for k, L in enumerate(Ls)), flush=True)

if __name__ == "__main__":
    which = sys.argv[1:] or ["bench", "timing"]
    for w in which:
        {"bench": part_bench, "timing": part_timing, "holdout": part_holdout}[w]()
