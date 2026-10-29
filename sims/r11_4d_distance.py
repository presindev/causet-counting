"""3+1 spacelike distances from past sizes, and a 3+1 embedding test (idea 005, session 11; "2+4" of the 3+1 assessment).

Distance. For c in the common past of spacelike a, b: V_a = V(I(c,a)) = pi tau_ca^4 / 24, V_b likewise, V_C = V(J+(c) & J-(a) & J-(b)) (a lens, not a diamond, in 3+1).
The three volumes fix the three invariants (tau_ca, tau_cb, d). With c at the origin, a = (tau_ca, 0, 0, 0) and b = (t_b, x_b, 0, 0) where
    t_b = (tau_ca^2 + tau_cb^2 + d^2) / (2 tau_ca),   x_b = sqrt(t_b^2 - tau_cb^2),
the fraction w = V_C / V_a depends on (alpha, delta) = (tau_cb / tau_ca, d / tau_ca) only. We tabulate w by Monte Carlo with common random numbers (one fixed
set of uniform points in I(c,a), reused for every grid entry, so the table is smooth), and invert w -> delta at fixed alpha (w decreases with delta).
Counts: tau^4 = 24 N / (pi rho), w = N_C / N_a.

One reference event for everything. In a universe with a first event c (a sprinkled diamond with its bottom tip inserted by hand, lesson 9), I(c,x) is the
past of x, so d(a, b) needs only |past a|, |past b|, |past a & past b|: one matrix product for all pairs.
Timelike pairs: tau^4 = 24 N(I(x,y)) / (pi rho).

Embedding: Lorentzian MDS of the squared intervals of M sampled events; 3+1 should give 1 negative and 3 positive large eigenvalues. Stress = rms misfit of the
best (1 time + k space) embedding; zero share as in s4b_detector.
Usage: python r11_4d_distance.py [table|distance|recover|embed ...]   (no argument: table + distance)
"""
import os, sys
import numpy as np

np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
TABLE = os.path.join(HERE, "out", "r11_lens_table_v2.npz")
# v2 (session 11): a is always the event with the LARGER interval, so alpha = tau_cb / tau_ca <= 1 and delta = d / tau_ca stays small.
# v1 (alpha 0.25-4, delta <= 3) silently clipped 18 % of pairs in whole-interval tests (low events), a per-event bias that wrecked the embedding.
ALPHAS = np.exp(np.linspace(np.log(0.05), 0.0, 61))
DELTAS = np.linspace(0.0, 8.0, 241)

def uniform_in_diamond(n, T, rng, d=4):
    """n points uniform in the d-dim Alexandrov interval between (0, 0) and (T, 0)."""
    out = []
    while sum(len(o) for o in out) < n:
        m = 3 * n
        t = T * rng.random(m)
        x = (T / 2) * (2 * rng.random((m, d - 1)) - 1)
        r = np.sqrt((x ** 2).sum(1))
        ok = r < np.minimum(t, T - t)
        out.append(np.column_stack([t[ok], x[ok]]))
    return np.vstack(out)[:n]

def build_table(nmc=1_000_000, seed=1):
    """w(alpha, delta) = V_C / V_b, with b the event with the SMALLER interval from c (table v2): uniform points in I(c, b) (tau_cb = 1),
    fraction also below a, where tau_ca = 1/alpha >= 1 and d = delta * tau_ca. Normalizing by the smaller interval keeps w in [0, 1] and well resolved."""
    rng = np.random.default_rng(seed)
    Z = uniform_in_diamond(nmc, 1.0, rng)                      # I(c, b), b = (1, 0, 0, 0)
    t, x1, rperp2 = Z[:, 0], Z[:, 1], (Z[:, 2:] ** 2).sum(1)
    W = np.zeros((len(ALPHAS), len(DELTAS)))
    for i, al in enumerate(ALPHAS):
        tca = 1 / al
        for j, de in enumerate(DELTAS):
            d = de * tca
            ta = (1 + tca ** 2 + d ** 2) / 2                     # (a - c)^2 = tca^2, (a - b)^2 = -d^2, (b - c) = (1, 0)
            xa = np.sqrt(max(ta ** 2 - tca ** 2, 0.0))
            dt = ta - t
            W[i, j] = np.mean((dt > 0) & (dt ** 2 > (xa - x1) ** 2 + rperp2))
    os.makedirs(os.path.dirname(TABLE), exist_ok=True)
    np.savez(TABLE, alphas=ALPHAS, deltas=DELTAS, W=W)
    print(f"table: {len(ALPHAS)} x {len(DELTAS)}, {nmc} MC points; w(alpha=1, delta=0) = {W[-1, 0]:.4f} (exact 1); w(1, 1) = {W[-1, 30]:.4f};"
          f" w(0.05, 0) = {W[0, 0]:.4f} (exact 1)")
    return W

def load_table():
    if not os.path.exists(TABLE):
        build_table()
    z = np.load(TABLE)
    return z["W"]

def invert(W, alpha, w):
    """delta with w(alpha, delta) = w; arrays allowed. Linear in log alpha between rows, monotone inversion along delta."""
    la = np.log(np.clip(alpha, ALPHAS[0], ALPHAS[-1]))
    g = (la - np.log(ALPHAS[0])) / (np.log(ALPHAS[1]) - np.log(ALPHAS[0]))
    i0 = np.clip(np.floor(g).astype(int), 0, len(ALPHAS) - 2)
    f = g - i0
    Wm = np.minimum.accumulate(W, axis=1)                       # enforce monotone decrease against MC noise
    shape = np.shape(alpha)
    i0, f, w = i0.ravel(), np.ravel(f), np.ravel(np.broadcast_to(w, shape))
    out = np.empty(len(i0))
    for s in range(0, len(i0), 50_000):                         # vectorized in chunks (session 11: the per-pair loop was too slow for 10^6 pairs)
        sl = slice(s, s + 50_000)
        rows = (1 - f[sl, None]) * Wm[i0[sl]] + f[sl, None] * Wm[i0[sl] + 1]
        k = np.clip((rows > w[sl, None]).sum(1), 1, len(DELTAS) - 1)   # first grid index with row <= w
        hi, lo = rows[np.arange(len(k)), k], rows[np.arange(len(k)), k - 1]
        frac = np.where(lo > hi, (lo - w[sl]) / np.where(lo > hi, lo - hi, 1), 0.0)
        out[sl] = DELTAS[k - 1] + np.clip(frac, 0, 1) * (DELTAS[k] - DELTAS[k - 1])
    return out.reshape(shape)

def dist_from_counts(W, Na, Nb, NC, rho):
    """d from |I(c,a)|, |I(c,b)|, |I(c,a) & I(c,b)| (all excluding the endpoints). Measured from the larger interval (table v2 convention)."""
    Na, Nb = np.maximum(Na, Nb), np.minimum(Na, Nb)
    ta = (24 * Na / (np.pi * rho)) ** 0.25
    tb = (24 * Nb / (np.pi * rho)) ** 0.25
    # w = N_C / N_b over the smaller interval (table v2), regularized: N_C = 0 does not mean zero overlap (session 11: raw zeros ran the inversion
    # to the table edge and gave d up to 6x the true maximum). (N_C + 1/2) / (N_b + 1) never reaches 0 or 1; negligible for large counts.
    return ta * invert(W, tb / ta, (NC + 0.5) / (Nb + 1.0))

def sprinkle_diamond(N, d, rng):
    """Poisson(N) points in a d-dim diamond of volume N (rho = 1), plus the bottom tip c at index 0. Returns coordinates (t, x...)."""
    cd = {2: 0.5, 3: np.pi / 12, 4: np.pi / 24}[d]               # V = cd T^d
    T = (N / cd) ** (1 / d)
    P = uniform_in_diamond(rng.poisson(N), T, rng, d)
    P = np.vstack([np.zeros(d), P])
    return P[np.argsort(P[:, 0])], T

def precedes(P, Q):
    """R[i, j] = P_i < Q_j (strictly in the causal past)."""
    dt = Q[None, :, 0] - P[:, None, 0]
    dr2 = ((Q[None, :, 1:] - P[:, None, 1:]) ** 2).sum(-1)
    return (dt > 0) & (dt ** 2 > dr2)

def part_distance(W):
    print("== 3+1 distance from past sizes (reference = bottom tip of a sprinkled diamond), rho = 1 ==")
    rng = np.random.default_rng(2)
    for N in (5000, 20000, 80000):
        rows = []
        for s in range(3):
            P, T = sprinkle_diamond(N, 4, rng)
            late = np.flatnonzero(P[:, 0] > 0.55 * T)
            S = rng.choice(late, min(200, len(late)), replace=False)
            past = precedes(P, P[S]).astype(np.float32)                 # past[z, i] = z < S_i
            past[0] = 0                                                  # exclude c itself
            common = past.T @ past
            n = past.sum(0)
            rel = precedes(P[S], P[S])
            for i in range(len(S)):
                for j in range(i + 1, len(S)):
                    if rel[i, j] or rel[j, i]:
                        continue
                    dx = P[S[i]] - P[S[j]]
                    dtrue = np.sqrt((dx[1:] ** 2).sum() - dx[0] ** 2)
                    rows.append((dtrue, n[i], n[j], common[i, j]))
        R = np.array(rows)
        est = dist_from_counts(W, R[:, 1], R[:, 2], R[:, 3], 1.0)
        rel_err = est / R[:, 0] - 1
        print(f"  N = {N} (T = {T:.1f} ell), {len(R)} spacelike pairs:")
        for lo, hi in ((0, 2), (2, 4), (4, 8), (8, 16), (16, 64)):
            m = (R[:, 0] >= lo) & (R[:, 0] < hi)
            if m.sum() > 10:
                print(f"    d {lo:2d}-{hi:2d} ell: n={m.sum():5d}  median rel err {np.median(np.abs(rel_err[m])):.3f}   bias (median signed) {np.median(rel_err[m]):+.3f}")

def squared_intervals_from_C(C, S, W):
    """Squared-interval matrix on the sample S from the causal matrix C only (3+1 formulas, rho = 1, element 0 in everyone's past)."""
    Cf = C.astype(np.float32)
    past = Cf[:, S].copy(); past[0] = 0                                # z < S_j, without the reference event
    fut = Cf[S, :]                                                     # S_i < z
    NI = fut @ past                                                    # N(I(S_i, S_j)) for S_i < S_j
    common = past.T @ past
    n = past.sum(0)
    M = len(S)
    sq = np.zeros((M, M))
    for i, j in zip(*np.triu_indices(M, 1)):
        if C[S[i], S[j]] or C[S[j], S[i]]:
            lo, hi = (i, j) if C[S[i], S[j]] else (j, i)
            sq[i, j] = -np.sqrt(24 * NI[lo, hi] / np.pi)              # -tau^2, tau^4 = 24 N / pi
        else:
            sq[i, j] = dist_from_counts(W, np.array(n[i]), np.array(n[j]), np.array(common[i, j]), 1.0) ** 2
    return sq + sq.T

def squared_intervals_two_refs(C, S, W, top):
    """As squared_intervals_from_C, but for spacelike pairs use whichever reference gives more events: element 0 (pasts) or the top element `top`
    (futures, the same inversion time-reversed). Session 11: past-only estimates fail for events just above the bottom (Johnston 2025 benchmark)."""
    Cf = C.astype(np.float32)
    past = Cf[:, S].copy(); past[0] = 0; past[top] = 0
    fut = Cf[S, :].copy(); fut[:, 0] = 0; fut[:, top] = 0
    NI = fut @ past
    cp, cf = past.T @ past, fut @ fut.T
    npst, nfut = past.sum(0), fut.sum(1)
    M = len(S)
    sq = np.zeros((M, M))
    for i, j in zip(*np.triu_indices(M, 1)):
        if C[S[i], S[j]] or C[S[j], S[i]]:
            lo, hi = (i, j) if C[S[i], S[j]] else (j, i)
            sq[i, j] = -np.sqrt(24 * NI[lo, hi] / np.pi)
            continue
        if min(npst[i], npst[j]) >= min(nfut[i], nfut[j]):
            na, nb, nc = npst[i], npst[j], cp[i, j]
        else:
            na, nb, nc = nfut[i], nfut[j], cf[i, j]
        if min(na, nb) < 1:
            sq[i, j] = np.nan                                          # no events on either side: no estimate
        else:
            sq[i, j] = dist_from_counts(W, np.array(na), np.array(nb), np.array(nc), 1.0) ** 2
    return sq + sq.T

def squared_intervals(P, S, W):
    """Same, for a sprinkling given by coordinates (the order is computed from them; only counts enter)."""
    return squared_intervals_from_C(precedes(P, P), S, W)

def embed_stats(sq, kmax=4):
    """Lorentzian MDS: eigenvalues, stress of the best (1 time + k space) embedding for k = 1..kmax, zero share."""
    M = len(sq)
    J = np.eye(M) - 1 / M
    lam, vec = np.linalg.eigh(-0.5 * J @ sq @ J)
    o = np.argsort(lam)
    iu = np.triu_indices(M, 1)
    stress = []
    for k in range(1, kmax + 1):
        X = np.column_stack([np.sqrt(max(-lam[o[0]], 0)) * vec[:, o[0]]] + [np.sqrt(max(lam[o[-q]], 0)) * vec[:, o[-q]] for q in range(1, k + 1)])
        D = X[:, None, :] - X[None, :, :]
        s = -D[..., 0] ** 2 + (D[..., 1:] ** 2).sum(-1)
        stress.append(np.sqrt(np.mean((sq[iu] - s[iu]) ** 2) / np.mean(sq[iu] ** 2)))
    return lam, np.array(stress), np.mean(sq[iu] == 0)

def sample_late(P, T, M, rng, frac=0.55):
    return rng.choice(np.flatnonzero(P[:, 0] > frac * T), M, replace=False)

def kr_order(N, rng):
    """Kleitman-Rothschild-like 3-layer order (N/4, N/2, N/4; neighbouring layers related with probability 1/2; transitive) plus a bottom element 0."""
    n1, n2 = N // 4, N // 2
    C = np.zeros((N + 1, N + 1), bool)
    C[0, 1:] = True
    L1, L2, L3 = np.arange(1, 1 + n1), np.arange(1 + n1, 1 + n1 + n2), np.arange(1 + n1 + n2, N + 1)
    C[np.ix_(L1, L2)] = rng.random((len(L1), len(L2))) < 0.5
    C[np.ix_(L2, L3)] = rng.random((len(L2), len(L3))) < 0.5
    C[np.ix_(L1, L3)] = (C[np.ix_(L1, L2)].astype(np.float32) @ C[np.ix_(L2, L3)].astype(np.float32)) > 0
    return C, L3

def summary(lam, st, z):
    tot = np.abs(lam).sum()
    lp = np.sort(lam[lam > 0])[::-1] / tot
    lp = np.pad(lp, (0, max(0, 4 - len(lp))))[:4]
    return np.concatenate([[np.sum(lam < -0.05 * tot)], lp, st, [z]])

def part_embed(W, M=80, reps=5):
    print(f"== 3+1 embedding test (M = {M} late events, {reps} universes per row; all intervals from counts with 3+1 formulas) ==")
    print(f"   {'universe':<24} #neg  top-4 positive eigenvalues / sum|lam|   stress 1+1   1+2    1+3    1+4   zero share")
    rng = np.random.default_rng(3)
    rows = [(f"{d}D sprinkling N={N}", d, N) for N in (5000, 20000) for d in (4, 3, 2)]
    for label, d, N in rows:
        out = []
        for _ in range(reps):
            P, T = sprinkle_diamond(N, d, rng)
            S = sample_late(P, T, M, rng)
            out.append(summary(*embed_stats(squared_intervals(P, S, W))))
        m = np.array(out).mean(0)
        print(f"   {label:<24} {m[0]:.1f}   " + " ".join(f"{x:.3f}" for x in m[1:5]) + "              " + "  ".join(f"{x:.3f}" for x in m[5:9]) + f"   {m[9]:.3f}", flush=True)
    out = []
    for _ in range(reps):
        C, top = kr_order(5000, rng)
        S = rng.choice(top, M, replace=False)
        out.append(summary(*embed_stats(squared_intervals_from_C(C, S, W))))
    m = np.array(out).mean(0)
    print(f"   {'KR 3-layer N=5000':<24} {m[0]:.1f}   " + " ".join(f"{x:.3f}" for x in m[1:5]) + "              " + "  ".join(f"{x:.3f}" for x in m[5:9]) + f"   {m[9]:.3f}")

def part_recover(W, N=20000, M=100, seed=4):
    """Fit the true coordinates to the 1+3 MDS embedding by an affine map: rms residual (ell) and distance of the linear part from a Lorentz map."""
    rng = np.random.default_rng(seed)
    print(f"== 3+1 position recovery, N = {N}, M = {M} ==")
    for s in range(3):
        P, T = sprinkle_diamond(N, 4, rng)
        S = sample_late(P, T, M, rng)
        sq = squared_intervals(P, S, W)
        J = np.eye(M) - 1 / M
        lam, vec = np.linalg.eigh(-0.5 * J @ sq @ J)
        o = np.argsort(lam)
        X = np.column_stack([np.sqrt(-lam[o[0]]) * vec[:, o[0]]] + [np.sqrt(lam[o[-k]]) * vec[:, o[-k]] for k in (1, 2, 3)])
        A1 = np.column_stack([X, np.ones(M)])
        coef, *_ = np.linalg.lstsq(A1, P[S], rcond=None)
        res = P[S] - A1 @ coef
        A = coef[:4].T
        eta = np.diag([-1.0, 1, 1, 1])
        print(f"  seed {s}: rms position error {np.sqrt((res ** 2).sum(1).mean()):.2f} ell over a region ~{np.ptp(P[S][:, 1]):.0f} ell wide;"
              f"  |A^T eta A - eta|max = {np.abs(A.T @ eta @ A - eta).max():.3f};  eigenvalues {np.round(np.sort(lam)[:2], 1)} ... {np.round(np.sort(lam)[-5:], 1)}", flush=True)

if __name__ == "__main__":
    which = sys.argv[1:] or ["table", "distance"]
    W = build_table() if "table" in which else load_table()
    if "distance" in which:
        part_distance(W)
    if "recover" in which:
        part_recover(W)
    if "embed" in which:
        part_embed(W)
