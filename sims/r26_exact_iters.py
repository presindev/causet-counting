"""Two checks of the likelihood fit (idea 005, session 13; review of counting-full-v2, items 3 and 4), on the session-12 ablation universes
(r23: seed 7070 n = 1500 x 3, seed 7071 n = 3000 x 2; Johnston's t; start = count-weighted map K0 = 100), related-pair term only:
  gauss   : r23's Gaussian form for tau^2 (what the paper uses)
  exact   : the exact Poisson log-likelihood  sum [N ln mu - mu],  mu = rho pi/24 (tau^2_+)^2,  tau^2_+ = s softplus(tau^2 / s), s = 0.1 ell^2
            (softplus keeps mu smooth where a trial position makes the pair spacelike; Casasola 2026's likelihood, over all related pairs)
            plus a soft wall for the relation itself, + sum log sigmoid(tau^2 / s): without it an N = 0 pair is best fitted spacelike (tau^2 <= 0 costs
            nothing), and the fit started from the truth drifts away (corr 0.899 / 0.971 / 0.990 at n = 400 / 1000 / 2000; Gaussian 0.966 / 0.991 / 0.9965).
each at 400 and 1000 Adam iterations (same schedule shape: lr x 0.3 at half way).
Usage: python r26_exact_iters.py check   |   python r26_exact_iters.py [n reps seed]
"""
import sys
import time
import numpy as np
from r11_4d_distance import load_table
from r12_johnston_compare import johnston
from r13_mixed import sprinkle
from r18_waist_oracle import ours_with_counts
from r19_cluster_wfit import fit_w
from r23_likelihood import Table, setup, scorer, loglik as loglik_gauss

np.seterr(all="ignore")
C4 = np.pi / 24

def loglik_exact(x, t, Rl, rho, s, wall=True):
    n = len(x)
    dx = x[Rl["B"]] - x[Rl["A"]]
    u = (t[Rl["B"]] - t[Rl["A"]]) ** 2 - (dx ** 2).sum(1)
    up = s * np.logaddexp(0.0, u / s)
    sig = 0.5 * (1 + np.tanh(0.5 * u / s))                            # d up / d u
    mu = rho * C4 * up ** 2 + 1e-300
    N = Rl["N"]
    L = (N * np.log(mu) - mu).sum()
    dl_du = (N / mu - 1) * rho * C4 * 2 * up * sig
    if wall:                                                          # the order says a < b: log P(timelike) ~ log sigmoid(u / s)
        L += -np.logaddexp(0.0, -u / s).sum()
        dl_du = dl_du + (1 - sig) / s
    gv = (-2 * dl_du)[:, None] * dx                                   # d u / d dx = -2 dx
    g = np.column_stack([np.bincount(Rl["B"], gv[:, k], n) - np.bincount(Rl["A"], gv[:, k], n) for k in range(3)])
    g[0] = 0; g[-1] = 0                                               # tips pinned (gauge), as r23
    return L, g

def fit(x0, grad, iters):
    """Adam ascent as r23.fit (tips at x = 0, lr 1 % of the spread, x 0.3 half way); grad(x) -> (L, g)."""
    x = x0.copy(); x[0] = 0; x[-1] = 0
    lr = 0.01 * np.std(x0)
    m = np.zeros_like(x); v = np.zeros_like(x); hist = []
    for k in range(1, iters + 1):
        L, g = grad(x)
        m = 0.9 * m + 0.1 * g; v = 0.999 * v + 0.001 * g ** 2
        x += lr * (m / (1 - 0.9 ** k)) / (np.sqrt(v / (1 - 0.999 ** k)) + 1e-12)
        if k % 100 == 0 or k == 1:
            hist.append((k, L))
        if k == iters // 2:
            lr *= 0.3
    return x, hist

def counts(C, Rl):
    N = C.astype(np.float32) @ C.astype(np.float32)
    return np.maximum(N[Rl["A"], Rl["B"]], N[Rl["B"], Rl["A"]]).astype(float)

def check():
    W = load_table()
    rng = np.random.default_rng(11)
    P, C, rho = sprinkle(400, rng); t = P[:, 0]
    _, Rl = setup(C, rho, t, W); Rl["N"] = counts(C, Rl)
    s = 0.1 / np.sqrt(rho)
    x = P[:, 1:] + 0.02 * rng.standard_normal((len(P), 3)); x[0] = 0; x[-1] = 0
    L, g = loglik_exact(x, t, Rl, rho, s)
    out = []
    for (i, k) in [(5, 0), (50, 1), (200, 2), (300, 0)]:
        h = 1e-6; xp = x.copy(); xp[i, k] += h; xm = x.copy(); xm[i, k] -= h
        out.append((g[i, k], (loglik_exact(xp, t, Rl, rho, s)[0] - loglik_exact(xm, t, Rl, rho, s)[0]) / (2 * h)))
    print("gradient check (analytic, numeric):", ", ".join("%.5g/%.5g" % o for o in out))
    iu = np.triu_indices(len(P), 1); sc = scorer(P, iu)
    for n_, seed in ((400, 11), (1000, 12), (2000, 13)):                # consistency from the truth, as the Gaussian check (r25 consistency file)
        rng = np.random.default_rng(seed)
        P, C, rho = sprinkle(n_, rng); t = P[:, 0]
        _, Rl = setup(C, rho, t, W); Rl["N"] = counts(C, Rl)
        sc = scorer(P, np.triu_indices(len(P), 1))
        for wall in (False, True):
            xf, _ = fit(P[:, 1:].copy(), lambda y: loglik_exact(y, t, Rl, rho, 0.1 / np.sqrt(rho), wall), 400)
            print("n = %d: exact Poisson%s from the truth: corr 1.0000 -> %.4f" % (n_, " + wall" if wall else "", sc(xf)), flush=True)

def run(n, reps, seed):
    W = load_table(); tab = Table(W)
    rng = np.random.default_rng(seed)
    names = ["johnston", "w_K100", "gauss400", "gauss1000", "exact400", "exact1000"]
    rows = []
    for _ in range(reps):
        t0 = time.time()
        P, C, rho = sprinkle(n, rng)                                    # identical draws to r23.run (same seed, same call order)
        iu = np.triu_indices(len(P), 1); sc = scorer(P, iu)
        r_j, Xj = johnston(C, rho, 1.0)
        t = Xj[:, 0]
        I, J, s_, kc = ours_with_counts(C, rho, t, W)
        rel = C | C.T
        Rrel = np.where(rel, r_j, np.inf); np.fill_diagonal(Rrel, 0.0)
        Xw, _ = fit_w(Rrel, t, I, J, s_, kc, 100)
        S, Rl = setup(C, rho, t, W); Rl["N"] = counts(C, Rl)
        S0 = dict(S); S0["nb"] = np.zeros_like(S["nb"]); S0["nc"] = np.zeros_like(S["nc"])
        sg = lambda y: loglik_gauss(y, t, S0, Rl, rho, tab)
        se = lambda y: loglik_exact(y, t, Rl, rho, 0.1 / np.sqrt(rho))
        row = [sc(Xj[:, 1:]), sc(Xw[:, 1:])]
        hists = []
        for gfun in (sg, se):
            for it in (400, 1000):
                x, h = fit(Xw[:, 1:], gfun, it); row.append(sc(x)); hists.append(h)
        rows.append(row)
        print("  universe %d (%.0f s): " % (len(rows), time.time() - t0) + "  ".join("%s %.4f" % (a, r) for a, r in zip(names, row)), flush=True)
        for lab, h in zip(names[2:], hists):
            print("    %-9s loglik %s" % (lab, " ".join("%d:%.1f" % e for e in h)), flush=True)
    A = np.array(rows); d = A - A[:, :1]
    print("n = %d (%d univ., seed %d)" % (n, reps, seed))
    for a, m, dm, de in zip(names, A.mean(0), d.mean(0), d.std(0, ddof=1) / np.sqrt(reps) if reps > 1 else np.full(len(names), np.nan)):
        print("  %-9s spatial corr %.4f   vs johnston %+.4f +- %.4f   (%+.0f %% of his residual)" % (a, m, dm, de, 100 * dm / (1 - A[:, 0].mean())))
    dd = A[:, 2:] - A[:, 2:3]
    print("  paired vs gauss400: " + "  ".join("%s %+.4f +- %.4f" % (a, x, y) for a, x, y in zip(names[3:], dd.mean(0)[1:], (dd.std(0, ddof=1) / np.sqrt(reps))[1:])))

if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "check":
        check()
    else:
        run(int(a[0]) if a else 1500, int(a[1]) if len(a) > 1 else 3, int(a[2]) if len(a) > 2 else 7070)
