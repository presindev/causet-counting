"""Our 3+1 overlap-volume distance (r11_4d_distance.py) against Johnston's 2025 embedding (PRD 111, 106020, arXiv:2502.09701), on the same universes.

Johnston 2025, as implemented here from the paper (eqs. 4, 6, 8, 13-15, 17-20):
    tau(x, y) = (|[x, y]| / (rho c_d))^(1/d)  (|[x,y]| counts the endpoints), c_4 = pi/24;  t(x) = T/2 + (tau(v1, x)^2 - tau(x, vn)^2) / (2T)
    related pairs:  r(x, y) = sqrt| (t(x) - t(y))^2 - tau(x, y)^2 |;   spacelike pairs:  r(x, y) = min_z [ R_xz + R_zy ]  (min-plus, R = r on related pairs, inf otherwise)
    X_xy = (r(v1,x)^2 + r(v1,y)^2 - r(x,y)^2) / 2;  spatial coordinates from the d - 1 largest eigenpairs of X;  p(x) = (t(x), spatial).
Ours: spacelike d from (|I(ref,a)|, |I(ref,b)|, |common|), with ref = v1 (pasts) or vn (futures), whichever side has more events; timelike from the interval count;
then 1+3 Lorentzian MDS.
Compared on: (A) Johnston's set-up (n = 500-1500, all elements); (B) a larger interval (n = 3000), all elements and only the late half.
Metrics: per-pair median relative error of the spacelike distance (raw, before embedding), and correlation of embedded vs true squared intervals.
Usage: python r12_johnston_compare.py
"""
import numpy as np
from r11_4d_distance import load_table, uniform_in_diamond, precedes, squared_intervals_two_refs

np.seterr(all="ignore")
C4 = np.pi / 24

def johnston(C, rho, T):
    n = len(C)
    Cf = C.astype(np.float32)
    N = Cf @ Cf                                                   # elements strictly between
    rel = C | C.T
    tau = np.where(rel, (N / (rho * C4)) ** 0.25, 0.0)             # elements strictly between: reproduces his Tables IV-V (with endpoints, as eq. 4 reads, it does not)
    tau = np.maximum(tau, tau.T)
    t = T / 2 + (tau[0] ** 2 - tau[:, -1] ** 2) / (2 * T)
    t[0], t[-1] = 0.0, T
    R = np.where(rel, np.sqrt(np.abs((t[:, None] - t[None, :]) ** 2 - tau ** 2)), np.inf)
    np.fill_diagonal(R, 0.0)
    r = R.copy()
    sp = ~rel & ~np.eye(n, dtype=bool)
    for x in range(n):                                            # min-plus over z, only needed for spacelike pairs of x
        ys = np.flatnonzero(sp[x])
        if len(ys):
            r[x, ys] = np.min(R[x][:, None] + R[:, ys], axis=0)
    X = 0.5 * (r[0][:, None] ** 2 + r[0][None, :] ** 2 - r ** 2)
    lam, vec = np.linalg.eigh(X)
    o = np.argsort(lam)[::-1][:3]
    sp_coords = vec[:, o] * np.sqrt(np.maximum(lam[o], 0))
    return r, np.column_stack([t, sp_coords])

def ours_embed(sq):
    sq = np.nan_to_num(sq, nan=0.0)
    M = len(sq); J = np.eye(M) - 1 / M
    lam, vec = np.linalg.eigh(-0.5 * J @ sq @ J); o = np.argsort(lam)
    return np.column_stack([np.sqrt(-lam[o[0]]) * vec[:, o[0]]] + [np.sqrt(lam[o[-k]]) * vec[:, o[-k]] for k in (1, 2, 3)])

def mink(X):
    D = X[:, None, :] - X[None, :, :]
    return -D[..., 0] ** 2 + (D[..., 1:] ** 2).sum(-1)

if __name__ == "__main__":
    W = load_table()
    rng = np.random.default_rng(8)
    print("per-pair spacelike distance: median |d_est/d - 1| (raw);  embedding: corr(embedded vs true squared intervals)")
    for n, reps in ((500, 5), (1500, 3), (3000, 2)):
        rows = []
        for _ in range(reps):
            rho = n / C4
            P = uniform_in_diamond(n, 1.0, rng)
            P = np.vstack([np.zeros(4), P, [1, 0, 0, 0]]); P = P[np.argsort(P[:, 0])]
            C = precedes(P, P)
            S = np.arange(1, len(P) - 1)
            true = mink(P[S])
            iu = np.triu_indices(len(S), 1)
            spl = true[iu] > 0
            late = (P[S][iu[0], 0] > 0.5) & (P[S][iu[1], 0] > 0.5) & (P[S][iu[0], 0] < 0.8) & (P[S][iu[1], 0] < 0.8)   # middle-upper band
            r_j, Xj = johnston(C, rho, 1.0)
            dj = r_j[np.ix_(S, S)]                                # Johnston's r is a spatial (Euclidean) distance, not the Minkowski one
            sq_o = squared_intervals_two_refs(C, S, W, len(P) - 1) / rho ** 0.5
            d_true_sp = np.sqrt((((P[S][:, None, 1:] - P[S][None, :, 1:]) ** 2).sum(-1)))[iu]   # Euclidean spatial distance, for Johnston's r
            d_true_mk = np.sqrt(np.where(true[iu] > 0, true[iu], np.nan))                         # Minkowski distance, for ours
            eo = np.sqrt(np.where(sq_o[iu] > 0, sq_o[iu], np.nan))
            ej = dj[iu]
            emb_o, emb_j = mink(ours_embed(sq_o))[iu], mink(Xj[S])[iu]
            def med(e, d, m):
                v = np.abs(e[m] / d[m] - 1); v = v[np.isfinite(v)]
                return np.median(v) if len(v) else np.nan
            rows.append((med(eo, d_true_mk, spl), med(ej, d_true_sp, spl), med(eo, d_true_mk, spl & late), med(ej, d_true_sp, spl & late),
                         np.corrcoef(emb_o, true[iu])[0, 1], np.corrcoef(emb_j, true[iu])[0, 1]))
        m = np.nanmean(rows, 0)
        print(f"  n = {n}: spacelike err all pairs  ours {m[0]:.3f}  Johnston {m[1]:.3f} | band 0.5<t<0.8  ours {m[2]:.3f}  Johnston {m[3]:.3f} | "
              f"embedded corr  ours {m[4]:.4f}  Johnston {m[5]:.4f}", flush=True)


def hybrid(C, rho, T, W, min_count=10, scale=1.0, cap=False, combine=None):
    """Johnston's pipeline (time coordinate, Euclidean spatial MDS anchored at v1) with OUR spacelike estimator: spatial^2 = d_ours^2 + (t_x - t_y)^2,
    d_ours from the overlap-volume inversion with whichever reference (v1 pasts / vn futures) has more events; his min-plus r where both counts < min_count."""
    from r11_4d_distance import dist_from_counts
    n = len(C)
    r_j, Xj = johnston(C, rho, T)
    t = Xj[:, 0]
    Cf = C.astype(np.float32)
    past = Cf.copy(); past[0] = 0; past[-1] = 0                      # past[z, x] = z < x, without v1, vn
    fut = Cf.T.copy(); fut[0] = 0; fut[-1] = 0                       # fut[z, x] = x < z
    cp, cf = past.T @ past, fut.T @ fut
    npst, nfut = past.sum(0), fut.sum(0)
    rel = C | C.T
    r = r_j.copy()
    iu = np.triu_indices(n, 1)
    sp = ~rel[iu]
    I, J = iu[0][sp], iu[1][sp]
    use_p = np.minimum(npst[I], npst[J]) >= np.minimum(nfut[I], nfut[J])
    na = np.where(use_p, npst[I], nfut[I]); nb = np.where(use_p, npst[J], nfut[J]); nc = np.where(use_p, cp[I, J], cf[I, J])
    ok = np.minimum(na, nb) >= min_count
    d = dist_from_counts(W, na[ok], nb[ok], nc[ok], 1.0) / rho ** 0.25   # counts at rho = 1 give d in units of ell = rho^(-1/4)
    sp2 = scale ** 2 * (d ** 2 + (t[I[ok]] - t[J[ok]]) ** 2)           # scale: diagnostic only (match the bias of his related-pair r)
    est = np.sqrt(sp2)
    if cap:                                                            # his r is a triangle-inequality upper bound: never exceed it
        est = np.minimum(est, r_j[I[ok], J[ok]])
    if combine == "mean":                                              # two estimators with partly independent errors: average them
        est = 0.5 * (est + r_j[I[ok], J[ok]])
    elif combine == "geo":
        est = np.sqrt(est * r_j[I[ok], J[ok]])
    r[I[ok], J[ok]] = est; r[J[ok], I[ok]] = est
    X = 0.5 * (r[0][:, None] ** 2 + r[0][None, :] ** 2 - r ** 2)
    lam, vec = np.linalg.eigh(X)
    o = np.argsort(lam)[::-1][:3]
    return np.column_stack([t, vec[:, o] * np.sqrt(np.maximum(lam[o], 0))]), ok.mean()


def multiref(C, rho, T, W, K=10, min_count=5):
    """Johnston's pipeline with our spacelike estimator averaged over many reference events (session 11 fix for element-level, low-rank errors):
    the K deepest elements (smallest pasts, v1 included) used through pasts, the K highest (smallest futures, vn included) through futures.
    For each spacelike pair, d^2 is averaged over every reference in its common past (future) with both interval counts >= min_count;
    spatial^2 = mean d^2 + (t_x - t_y)^2. Pairs with no valid reference keep Johnston's r. Returns the embedding and the share of pairs covered."""
    from r11_4d_distance import invert
    n = len(C)
    r_j, Xj = johnston(C, rho, T)
    t = Xj[:, 0]
    Cb = C.astype(bool)
    Cf = C.astype(np.float32)
    rel = Cb | Cb.T
    iu = np.triu_indices(n, 1)
    sp = ~rel[iu]
    I, J = iu[0][sp], iu[1][sp]
    s2, cnt = np.zeros(len(I)), np.zeros(len(I))
    bottoms = np.argsort(Cf.sum(0))[:K]                             # fewest elements below: deepest
    tops = np.argsort(Cf.sum(1))[:K]                                # fewest elements above: highest
    for refs, M in ((bottoms, Cf), (tops, Cf.T)):                   # M[z, x] = z < x (pasts) or x < z (futures)
        for c in refs:
            sel = M[c] > 0                                          # elements on the far side of c
            B = M * sel[:, None]                                    # B[z, x] = c < z < x
            nn = B.sum(0)
            common = B.T @ B
            ok = sel[I] & sel[J] & (np.minimum(nn[I], nn[J]) >= min_count)
            if not ok.any():
                continue
            from r11_4d_distance import dist_from_counts
            d = dist_from_counts(W, nn[I[ok]], nn[J[ok]], common[I[ok], J[ok]], 1.0) / rho ** 0.25
            s2[ok] += d ** 2; cnt[ok] += 1
    r = r_j.copy()
    have = cnt > 0
    est = np.sqrt(s2[have] / cnt[have] + (t[I[have]] - t[J[have]]) ** 2)
    r[I[have], J[have]] = est; r[J[have], I[have]] = est
    X = 0.5 * (r[0][:, None] ** 2 + r[0][None, :] ** 2 - r ** 2)
    lam, vec = np.linalg.eigh(X)
    o = np.argsort(lam)[::-1][:3]
    return np.column_stack([t, vec[:, o] * np.sqrt(np.maximum(lam[o], 0))]), have.mean(), r


def both_sides(C, rho, T, W, min_count=3, cap=True):
    """Johnston's pipeline with our spacelike estimator using BOTH references for every pair: d^2 from pasts (v1) and from futures (vn), independent
    counts, combined with weights = smaller interval count on each side (Poisson: variance ~ 1/count). Session 11: one-sided estimates lose at large
    separations, where pairs sit near the waist of the diamond and each side holds only ~10 events. Optional cap at his triangle-inequality r."""
    n = len(C)
    r_j, Xj = johnston(C, rho, T)
    t = Xj[:, 0]
    from r11_4d_distance import dist_from_counts
    Cf = C.astype(np.float32)
    past = Cf.copy(); past[0] = 0; past[-1] = 0
    fut = Cf.T.copy(); fut[0] = 0; fut[-1] = 0
    iu = np.triu_indices(n, 1)
    sp = ~(C | C.T)[iu]
    I, J = iu[0][sp], iu[1][sp]
    num, den = np.zeros(len(I)), np.zeros(len(I))
    for M in (past, fut):
        cnt = M.sum(0); common = M.T @ M
        a, b, c = cnt[I], cnt[J], common[I, J]
        w = np.minimum(a, b)
        ok = w >= min_count
        d = dist_from_counts(W, a[ok], b[ok], c[ok], 1.0) / rho ** 0.25
        num[ok] += w[ok] * d ** 2; den[ok] += w[ok]
    have = den > 0
    est = np.sqrt(num[have] / den[have] + (t[I[have]] - t[J[have]]) ** 2)
    if cap:
        est = np.minimum(est, r_j[I[have], J[have]])
    r = r_j.copy()
    r[I[have], J[have]] = est; r[J[have], I[have]] = est
    X = 0.5 * (r[0][:, None] ** 2 + r[0][None, :] ** 2 - r ** 2)
    lam, vec = np.linalg.eigh(X)
    o = np.argsort(lam)[::-1][:3]
    return np.column_stack([t, vec[:, o] * np.sqrt(np.maximum(lam[o], 0))]), have.mean()
