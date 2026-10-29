"""Interior benchmark (idea 005, session 12): score the 3+1 maps only on pairs deep inside the diamond, plus a Madsen-style trilateration chart.

Core: Madsen's own count criterion (arXiv:2610.36695, Sec. 3.1): v(p) = min(|past|, |future|) >= f N (counts inside the diamond, strictly), f = 0.02, 0.04
(continuum: proper time to both tips >= f^{1/4}; at t = 1/2 that is r <= 0.33 / 0.22 of the waist radius 0.5).
Every arm embeds ALL events (as before); the score is the spatial-distance correlation (his Table V metric) over pairs with both events in the core.
Arms: johnston, switch (L = 0.25), ours alone, count-weighted fit K0 = 30, 100 (r19, no detours), and
    madsen  [literature: Madsen 2026, Sec. 3.2-3.3; our implementation]. ONE chart for the whole core is impossible (the common past of the f = 0.02 core is
            empty at n = 500), so, as in his paper, LOCAL charts: base event p in the core, chart = the M nearest events by his profile distance
            d_C(p,c) = |past p xor past c| + |future p xor future c| (counts only), by Lorentzian trilateration from d + 1 = 5 anchors
            a0 < a1 < ... < a4, each timelike to every chart event, all five from the chart's common past / common future (tips allowed: long baselines), chosen
            (from the counts only) for the best Gram conditioning among random chained candidates. Squared intervals D = -(N/(rho C4))^{1/2}, N = elements strictly between
            (the convention that reproduces Johnston's tables; Madsen counts the endpoints too). G_ij = (D(a0,ai) + D(a0,aj) - D(ai,aj))/2,
            w_i(c) = (G_ii - D(ai,c) + D(a0,c))/2, X(c) = B(G) G^{-1} w(c), B from Madsen's Schur/Cholesky factorization (B^T eta B = G).
            Frame: the chart is defined up to a Lorentz map; we boost to the rest frame of the diamond's tips (X of both tips computed by the same
            trilateration; the frame the other maps live in, since their time comes from the tips). No truth is used to align.
            Scored on within-chart pairs, pooled over charts; every other arm is scored on exactly the same pairs (its global map).
    madsen_avg: spatial distances averaged over the 10 best-conditioned anchor sets (distances are rotation/translation invariant after the boost).
Fairness: Madsen's chart uses only timelike intervals between anchors and core events (5 per event); the other arms use all pairs of all events.
Validation: madsen with TRUE squared intervals must reproduce the core (corr = 1).
Usage: python r20_interior.py n reps seed [M]
"""
import sys
import time
import numpy as np
from r11_4d_distance import load_table
from r12_johnston_compare import johnston, C4, mink
from r13_mixed import sprinkle, embed_from_r
from r18_waist_oracle import ours_with_counts
from r19_cluster_wfit import fit_w

np.seterr(all="ignore")
FS = (0.02, 0.04)   # v <= N/16 everywhere (the centre's past is a height-1/2 diamond), so f = 0.1, 0.2 are empty; 0.02 / 0.04 = 32 % / 64 % of the maximum
ETA = np.diag([-1.0, 1, 1, 1])

def B_of_G(G):
    """Madsen Sec. 3.3: B = [[a*, t^T], [0, R]] with B^T eta B = G (G11 < 0, one negative eigenvalue)."""
    a = np.sqrt(-G[0, 0]); t = -G[0, 1:] / a
    S = G[1:, 1:] - np.outer(G[1:, 0], G[0, 1:]) / G[0, 0]
    R = np.linalg.cholesky(S).T                                   # upper triangular, R^T R = S
    B = np.zeros_like(G); B[0, 0] = a; B[0, 1:] = t; B[1:, 1:] = R
    return B

def chart(Dfun, anchors, pts, tips=None):
    """Trilateration chart. Dfun(i_array, j_array) -> squared intervals. Returns X for pts (rows), boosted to the rest frame of tips (default a0, a4);
    None if G is bad. The tips must be timelike to all anchors."""
    a = np.asarray(anchors)
    DA = Dfun(a[:, None], a[None, :])                               # 5 x 5
    G = 0.5 * (DA[0, 1:][:, None] + DA[0, 1:][None, :] - DA[1:, 1:])
    if not np.all(np.isfinite(G)):
        return None, np.inf
    lam = np.linalg.eigvalsh(G)
    if not (G[0, 0] < 0 and (lam < 0).sum() == 1 and (lam > 0).sum() == 3):
        return None, np.inf
    try:
        B = B_of_G(G)
    except np.linalg.LinAlgError:
        return None, np.inf
    Gi = np.linalg.inv(G)
    allp = np.concatenate([pts, a[[0, 4]] if tips is None else np.asarray(tips)])
    Dc = Dfun(a[1:, None], allp[None, :])                           # 4 x m
    D0 = Dfun(np.full(1, a[0])[:, None], allp[None, :])[0]
    w = 0.5 * (np.diag(G)[:, None] - Dc + D0[None, :])
    X = (B @ Gi @ w).T
    u = X[-1] - X[-2]                                              # upper tip - lower tip
    if u[0] < 0:
        X[:, 0] *= -1; u[0] *= -1
    tau = np.sqrt(u[0] ** 2 - (u[1:] ** 2).sum())
    g = u[0] / tau; b = u[1:] / u[0]; b2 = (b ** 2).sum()
    L = np.eye(4); L[0, 0] = g; L[0, 1:] = -g * b; L[1:, 0] = -g * b
    if b2 > 0:
        L[1:, 1:] += (g - 1) * np.outer(b, b) / b2
    return (L @ X[:-2].T).T, np.abs(lam).max() / np.abs(lam).min()

def pick_anchors(C, core, rng, Dfun, tries=400, keep=10):
    """Five chained anchors from events related to all chart events (common past: below all; common future: above all; the tips included)."""
    n = len(C)
    below = np.flatnonzero(C[:, core].all(1))                     # includes the bottom tip (related to everything)
    above = np.flatnonzero(C[core][:, :].all(0))                  # includes the top tip
    def chain(pool, k):
        """k events of pool forming a chain, built as a random walk upward (empty if stuck)."""
        out = []
        cur = pool
        for _ in range(k):
            if len(cur) == 0:
                return None
            x = rng.choice(cur)
            out.append(x)
            cur = cur[C[x, cur]]
        return out
    cands = []
    for _ in range(tries):
        k = rng.integers(1, 3)                                     # Madsen's ideal set: a0 below, the rest above; also try two below
        lo, hi = chain(below, k), chain(above, 5 - k)
        if lo is None or hi is None:
            continue
        an = [int(x) for x in lo + hi]
        X, cond = chart(Dfun, an, np.array([], int), tips=[0, n - 1])
        if np.isfinite(cond):
            cands.append((cond, an))
    cands.sort(key=lambda z: z[0])
    return [an for _, an in cands[:keep]], len(below), len(above)

def run(n, reps, seed, n_charts=20, M=20):
    W = load_table()
    rng = np.random.default_rng(seed)
    garms = ["johnston", "switch", "ours", "w_K30", "w_K100"]
    larms = garms + ["madsen", "madsen_avg"]
    res = {f: [] for f in FS}
    loc = []
    print(f"n = {n}, {reps} universes, seed {seed}. (A) spatial corr on core pairs; (B) local charts: {n_charts} per universe, M = {M} nearest by profile "
          f"distance, base events in the f = {FS[0]} core; every arm scored on the same within-chart pairs. Paired vs Johnston.", flush=True)
    for u in range(reps):
        t0 = time.time()
        P, C, rho = sprinkle(n, rng)
        N = len(P)
        Cf = C.astype(np.float32); Nb = Cf @ Cf
        Dest = lambda i, j: np.where(i == j, 0.0, np.where(C[i, j] | C[j, i], -np.sqrt(np.maximum(Nb[i, j], Nb[j, i]) / (rho * C4)), np.nan))
        Dtrue = lambda i, j: -(P[i, 0] - P[j, 0]) ** 2 + ((P[i, 1:] - P[j, 1:]) ** 2).sum(-1)
        r_j, Xj = johnston(C, rho, 1.0); tj = time.time() - t0
        t = Xj[:, 0]
        I, J, s, k = ours_with_counts(C, rho, t, W)
        rj = r_j[I, J]; have = np.isfinite(s); ours = np.where(have, s, rj)
        def sym(v):
            M_ = r_j.copy(); M_[I, J] = v; M_[J, I] = v
            return M_
        maps = {"johnston": Xj,
                "switch": embed_from_r(sym(np.where(have & (s < 0.25), s, rj)), t),
                "ours": embed_from_r(sym(ours), t)}
        R = np.where(C | C.T, r_j, np.inf); np.fill_diagonal(R, 0.0)   # his related-pair R (same as related_R)
        for K0 in (30, 100):
            maps[f"w_K{K0}"], _ = fit_w(R, t, I, J, s, k, K0)
        tg = time.time() - t0
        npst = C[1:-1].sum(0); nfut = C[:, 1:-1].sum(1)                   # past / future sizes inside the diamond, tips excluded
        v = np.minimum(npst, nfut)
        sd = lambda X, a, b: np.sqrt(((X[a, 1:] - X[b, 1:]) ** 2).sum(-1))
        # (A) global maps scored on core pairs
        for f in FS:
            core = np.flatnonzero(v >= f * N)
            if len(core) < 20:
                print(f"  univ {u + 1} f = {f}: core has {len(core)} events, skipped", flush=True); continue
            a_, b_ = np.triu_indices(len(core), 1); a_, b_ = core[a_], core[b_]
            dtrue = sd(P, a_, b_)
            row = {a: np.corrcoef(sd(maps[a], a_, b_), dtrue)[0, 1] for a in garms}
            rc = np.sqrt((P[core, 1:] ** 2).sum(1))
            res[f].append((row, len(core), rc.max(), P[core, 0].min(), P[core, 0].max()))
            print(f"  univ {u + 1} f = {f}: core {len(core)}/{N} (r <= {rc.max():.2f}, t in [{P[core, 0].min():.2f}, {P[core, 0].max():.2f}]): " +
                  " ".join(f"{a} {row[a]:.4f}" for a in garms), flush=True)
        # (B) Madsen local charts
        t1 = time.time()
        cp = Cf.T @ Cf; cfu = Cf @ Cf.T
        npa, nfa = C.sum(0).astype(float), C.sum(1).astype(float)
        core = np.flatnonzero(v >= FS[0] * N)
        bases = rng.choice(core, min(n_charts, len(core)), replace=False)
        crng = np.random.default_rng(seed * 1000 + u)
        pairs, est = [], {a: [] for a in larms}
        vals, conds, nfail = [], [], 0
        for p in bases:
            dC = (npa[p] + npa - 2 * cp[p]) + (nfa[p] + nfa - 2 * cfu[p])      # Madsen's profile distance, in counts
            ch = np.argsort(dC)[:M]
            sets, nb, na = pick_anchors(C, ch, crng, Dest, tries=1500)
            if not sets:
                nfail += 1; continue
            Xm, cond = chart(Dest, sets[0], ch, tips=[0, N - 1])
            if Xm is None or not np.all(np.isfinite(Xm)):
                nfail += 1; continue
            Xv, _ = chart(Dtrue, sets[0], ch, tips=[0, N - 1])
            a_, b_ = np.triu_indices(M, 1)
            dt = sd(P[ch], a_, b_)
            vals.append(np.corrcoef(sd(Xv, a_, b_), dt)[0, 1]); conds.append(cond)
            pairs.append(dt)
            est["madsen"].append(sd(Xm, a_, b_))
            Ds = [sd(X_, a_, b_) for X_ in (chart(Dest, an, ch, tips=[0, N - 1])[0] for an in sets) if X_ is not None and np.all(np.isfinite(X_))]
            est["madsen_avg"].append(np.mean(Ds, 0))
            for a in garms:
                est[a].append(sd(maps[a][ch], a_, b_))
        if pairs:
            dt = np.concatenate(pairs)
            lrow = {a: (np.corrcoef(np.concatenate(est[a]), dt)[0, 1], np.median(np.abs(np.concatenate(est[a]) / dt - 1))) for a in larms}
            ext = np.concatenate([[sd(P, np.array([c]), np.array([c2]))[0] for c, c2 in [(ch[0], ch[-1])]] for ch in [np.argsort(
                (npa[p] + npa - 2 * cp[p]) + (nfa[p] + nfa - 2 * cfu[p]))[:M] for p in bases[:3]]])
            loc.append((lrow, np.min(vals), np.median(conds), nfail, np.median(dt)))
            print(f"  univ {u + 1} local: {len(pairs)} charts ok, {nfail} without anchors; validation (true D) min corr {np.min(vals):.6f}; "
                  f"Gram cond median {np.median(conds):.0f}; median true pair distance {np.median(dt):.3f}; " +
                  " ".join(f"{a} {lrow[a][0]:.3f}/{lrow[a][1]:.3f}" for a in larms) + "  (corr/median rel. err)", flush=True)
        print(f"  universe {u + 1}: {time.time() - t0:.0f} s (Johnston {tj:.0f} s, all global maps {tg:.0f} s, local charts {time.time() - t1:.0f} s)", flush=True)
    for f in FS:
        rows = res[f]
        if not rows:
            continue
        A = np.array([[r[0][a] for a in garms] for r in rows]); d = A - A[:, :1]
        jres = 1 - A[:, 0].mean()
        print(f"\n(A) n = {n}, f = {f}: {len(rows)} universes; core size {np.mean([r[1] for r in rows]):.0f} of ~{n} (max radius {np.mean([r[2] for r in rows]):.2f} "
              f"of 0.5; t {np.mean([r[3] for r in rows]):.2f}-{np.mean([r[4] for r in rows]):.2f})")
        print("  arm          core spatial corr   vs johnston (paired)   share of his core residual")
        for kk, a in enumerate(garms):
            se = d[:, kk].std(ddof=1) / np.sqrt(len(d)) if len(d) > 1 else np.nan
            print(f"  {a:12s} {A[:, kk].mean():.4f}              {d[:, kk].mean():+.4f} +- {se:.4f}       {d[:, kk].mean() / jres:+5.0%}")
    if loc:
        A = np.array([[r[0][a][0] for a in larms] for r in loc]); E = np.array([[r[0][a][1] for a in larms] for r in loc]); d = A - A[:, :1]
        jres = 1 - A[:, 0].mean()
        print(f"\n(B) n = {n}, local charts (M = {M}, pooled within-chart pairs, {len(loc)} universes): Madsen validation with true intervals min corr "
              f"{min(r[1] for r in loc):.6f}; Gram cond median {np.median([r[2] for r in loc]):.0f}; charts without anchors {sum(r[3] for r in loc)}; "
              f"median true pair distance {np.mean([r[4] for r in loc]):.3f}")
        print("  arm          local corr   vs johnston (paired)   share of his local residual   median rel. error")
        for kk, a in enumerate(larms):
            se = d[:, kk].std(ddof=1) / np.sqrt(len(d)) if len(d) > 1 else np.nan
            print(f"  {a:12s} {A[:, kk].mean():.4f}       {d[:, kk].mean():+.4f} +- {se:.4f}       {d[:, kk].mean() / jres:+5.0%}                   {E[:, kk].mean():.3f}")

if __name__ == "__main__":
    a = sys.argv[1:]
    run(int(a[0]) if a else 1500, int(a[1]) if len(a) > 1 else 2, int(a[2]) if len(a) > 2 else 3030, M=int(a[3]) if len(a) > 3 else 20)
