"""External referee round 1 on the 3+1 paper (session 17): one universe per call, every arm on the same universe, maps saved for laptop analysis.
Same universes as the large-n set (r14 / r24: seed = 1000 + i, sprinkle is the rng's first use), so seeds 1001-1010 extend Table II to 10 per size.
python 3.6 + numpy 1.19 compatible (no scipy on the cluster: L-BFGS written here).
Arms (all with Johnston's t unless stated; start = count-weighted map K0 = 100, r19):
  fit            Gaussian related-pair likelihood (Eq. 3 of the paper), 400 Adam iterations          <- the paper's method (Major 2: more universes)
  fit_lbfgs      fit, then L-BFGS to convergence                                                      <- Major 4: optimizer-limited?
  jstart         Adam 400 + L-BFGS from Johnston's map                                                <- Major 4: multi-start
  pstart         Adam 400 + L-BFGS from the start map + N(0, (0.5 ell)^2) per coordinate               <- Major 4: multi-start
  truth          Adam 400 + L-BFGS from the TRUE positions (Johnston's t)                              <- reference optimum
  exact_all      exact Poisson sum[N ln mu - mu] + soft relation wall (r26), all related pairs, Adam 400
  exact_near     the same restricted to near-cone pairs, tau_hat^2 < 6 ell^2 (Casasola 2026's set)     <- Major 3: does "all pairs" matter?
  gauss_near     the paper's Gaussian form restricted to the same near-cone pairs                       <- Major 3, same form as the paper
  joint          Gaussian, time AND space free (tips fixed), Adam 400 + L-BFGS from (t_J, start map)   <- Major 5
Every fixed-t arm is also scored with the paper's Gaussian lnL (all pairs, Johnston's t), so lnL values are comparable across arms.
Usage: python r35_referee1_3p1.py n seed out.npz   |   python r35_referee1_3p1.py check
"""
import sys
import time
import numpy as np
from r11_4d_distance import load_table
from r12_johnston_compare import johnston
from r13_mixed import sprinkle
from r15_cheap_far import related_R
from r18_waist_oracle import ours_with_counts
from r19_cluster_wfit import fit_w
from r23_likelihood import setup
from r26_exact_iters import loglik_exact, counts
from r14_cluster_scale import spatial_dist

np.seterr(all="ignore")
C4 = np.pi / 24

def gauss(X, Rl, joint=False, t=None):
    """Paper's Gaussian related-pair lnL. X: spatial (n, 3) with fixed t, or (n, 4) = (t, x) if joint. Tips pinned (gradient zero)."""
    n = len(X)
    if joint:
        t, x = X[:, 0], X[:, 1:]
    else:
        x = X
    A, B = Rl["A"], Rl["B"]
    dx = x[B] - x[A]; dt = t[B] - t[A]
    r = (dt ** 2 - (dx ** 2).sum(1) - Rl["t2"]) / Rl["sd"]
    L = -0.5 * (r ** 2).sum()
    dl = -r / Rl["sd"]                                                  # dL / d tau^2
    gv = (-2 * dl)[:, None] * dx                                        # d tau^2 / d x_B = -2 dx
    cols = [np.bincount(B, gv[:, k], n) - np.bincount(A, gv[:, k], n) for k in range(3)]
    if joint:
        gt = 2 * dl * dt                                                # d tau^2 / d t_B = 2 dt
        cols = [np.bincount(B, gt, n) - np.bincount(A, gt, n)] + cols
    g = np.column_stack(cols); g[0] = 0; g[-1] = 0
    return L, g

def adam(x0, grad, iters=400, lr=None):
    """r23's schedule (lr 1 % of the spatial spread, x 0.3 half way); tips stay where x0 puts them (their gradient is zero)."""
    x = x0.copy()
    lr = lr or 0.01 * np.std(x0[:, -3:])
    m = np.zeros_like(x); v = np.zeros_like(x)
    for k in range(1, iters + 1):
        L, g = grad(x)
        m = 0.9 * m + 0.1 * g; v = 0.999 * v + 0.001 * g ** 2
        x += lr * (m / (1 - 0.9 ** k)) / (np.sqrt(v / (1 - 0.999 ** k)) + 1e-12)
        if k == iters // 2:
            lr *= 0.3
    return x

def lbfgs(x0, grad, maxit=300, m=10, tol=1e-10):
    """Maximize L with L-BFGS (two-loop recursion, Armijo backtracking). Returns x, L, iterations used."""
    x = x0.copy(); L, g = grad(x)
    S, Y = [], []
    for it in range(1, maxit + 1):
        q = -g.ravel().copy(); al = []                                  # minimize f = -L, gradient -g
        for s, y in zip(reversed(S), reversed(Y)):
            a = (s @ q) / (y @ s); al.append(a); q -= a * y
        q *= (S[-1] @ Y[-1]) / (Y[-1] @ Y[-1]) if S else 1e-3 * np.std(x) / (np.abs(q).max() + 1e-300)
        for (s, y), a in zip(zip(S, Y), reversed(al)):
            q += s * (a - (y @ q) / (y @ s))
        d = -q.reshape(x.shape)                                         # ascent direction for L
        slope = (g * d).sum()
        if slope <= 0:
            S, Y = [], []; d = g * (1e-3 * np.std(x) / (np.abs(g).max() + 1e-300)); slope = (g * d).sum()
        step = 1.0
        while True:
            xn = x + step * d; Ln, gn = grad(xn)
            if Ln >= L + 1e-4 * step * slope or step < 1e-8:
                break
            step *= 0.5
        if Ln < L:
            break
        s_, y_ = (xn - x).ravel(), (g - gn).ravel()                     # y for f = -L
        if s_ @ y_ > 1e-12:
            S.append(s_); Y.append(y_)
            if len(S) > m:
                S.pop(0); Y.pop(0)
        dL = Ln - L
        x, L, g = xn, Ln, gn
        if dL < tol * abs(L):
            break
    return x, L, it

def subset(Rl, keep):
    return {k: v[keep] for k, v in Rl.items()}

def main(n, seed, out):
    W = load_table()
    rng = np.random.default_rng(seed)
    P, C, rho = sprinkle(n, rng)                                        # identical to r14 / r24 (first use of the rng)
    ell = rho ** -0.25
    print("n = %d (Poisson %d), seed %d" % (n, len(P), seed), flush=True)
    iu = np.triu_indices(len(P), 1)
    st = spatial_dist(P, iu)
    T, res, maps = {}, {}, {}
    def save():
        np.savez(out, n=n, npts=len(P), seed=seed, ell=ell, P=P.astype(np.float32), names=np.array(list(res)),
                 corr=np.array([r[0] for r in res.values()]), lnl=np.array([r[1] for r in res.values()]), own=np.array([r[2] for r in res.values()]),
                 timing_keys=np.array(list(T)), timing=np.array(list(T.values())),
                 **{"X_" + k: v.astype(np.float32) for k, v in maps.items()})
    def record(name, X, lnl=np.nan, own=np.nan, t0=None):
        maps[name] = X
        res[name] = (np.corrcoef(spatial_dist(X, iu), st)[0, 1], lnl, own)
        if t0 is not None:
            T[name] = time.time() - t0
        save()
        print("  %-11s corr %.5f  lnL(paper) %.1f  own %.1f  (%.0f s)" % (name, res[name][0], lnl, own, T.get(name, 0)), flush=True)

    t0 = time.time(); _, Xj = johnston(C, rho, 1.0); record("johnston", Xj, t0=t0)
    t = Xj[:, 0]
    t0 = time.time(); R, tr = related_R(C, rho); I, J, s, k = ours_with_counts(C, rho, t, W)
    Xw, _ = fit_w(R, t, I, J, s, k, 100); del R, I, J, s, k; record("start", Xw, t0=t0)
    _, Rl = setup(C, rho, t, W); Rl["N"] = counts(C, Rl); del C
    near = Rl["t2"] < 6 * ell ** 2                                      # Casasola's near-cone set, judged from the counts (true tau unknown)
    T["near_share"] = near.mean(); T["related_pairs"] = len(near)
    print("  related pairs %d, near-cone (tau_hat^2 < 6 ell^2) %.3f" % (len(near), near.mean()), flush=True)
    G = lambda x: gauss(x, Rl, t=t)
    lnl = lambda x: G(x)[0]
    s0 = 0.1 * ell ** 2
    tipfix = lambda x: np.vstack([np.zeros(3), x[1:-1], np.zeros(3)])

    t0 = time.time(); x = adam(Xw[:, 1:], G); record("fit", np.column_stack([t, x]), lnl(x), lnl(x), t0)
    t0 = time.time(); x2, L2, it = lbfgs(x, G); T["fit_lbfgs_iters"] = it; record("fit_lbfgs", np.column_stack([t, x2]), L2, L2, t0)
    for name, x0 in (("jstart", tipfix(Xj[:, 1:])), ("pstart", tipfix(Xw[:, 1:] + 0.5 * ell * rng.standard_normal(Xw[:, 1:].shape))),
                     ("truth", tipfix(P[:, 1:]))):
        t0 = time.time(); x, L, it = lbfgs(adam(x0, G), G); T[name + "_iters"] = it
        record(name, np.column_stack([t, x]), L, L, t0)
    Rn = subset(Rl, near)
    for name, fun in (("exact_all", lambda y: loglik_exact(y, t, Rl, rho, s0)), ("exact_near", lambda y: loglik_exact(y, t, Rn, rho, s0)),
                      ("gauss_near", lambda y: gauss(y, Rn, t=t))):
        t0 = time.time(); x = adam(tipfix(Xw[:, 1:]), fun); record(name, np.column_stack([t, x]), lnl(x), fun(x)[0], t0)
    GJ = lambda X: gauss(X, Rl, joint=True)
    t0 = time.time(); X4, L4, it = lbfgs(adam(np.column_stack([t, tipfix(Xw[:, 1:])]), GJ), GJ); T["joint_iters"] = it
    terr = (X4[:, 0] - X4[:, 0].mean()) - (P[:, 0] - P[:, 0].mean()); tje = (t - t.mean()) - (P[:, 0] - P[:, 0].mean())
    T["joint_time_rms"] = np.sqrt((terr ** 2).mean()) / ell; T["johnston_time_rms"] = np.sqrt((tje ** 2).mean()) / ell
    record("joint", X4, np.nan, L4, t0)
    print("  time error rms: Johnston %.3f ell, joint fit %.3f ell" % (T["johnston_time_rms"], T["joint_time_rms"]), flush=True)

def check():
    """Gradients against finite differences (fixed t and joint), and an L-BFGS sanity run, n = 400."""
    W = load_table()
    rng = np.random.default_rng(11)
    P, C, rho = sprinkle(400, rng); t = P[:, 0]
    _, Rl = setup(C, rho, t, W)
    X = P.copy(); X[1:-1] += 0.02 * rng.standard_normal(X[1:-1].shape)
    for joint in (False, True):
        Y = X if joint else X[:, 1:]
        f = lambda y: gauss(y, Rl, joint, t)
        g = f(Y)[1]; out = []
        for (i, k) in [(5, 0), (50, 1), (200, 2), (300, 0)]:
            h = 1e-6; yp = Y.copy(); yp[i, k] += h; ym = Y.copy(); ym[i, k] -= h
            out.append((g[i, k], (f(yp)[0] - f(ym)[0]) / (2 * h)))
        print("gradient check joint=%s (analytic/numeric):" % joint, ", ".join("%.5g/%.5g" % o for o in out))
    G = lambda y: gauss(y, Rl, t=t)
    xa = adam(X[:, 1:], G); xb, Lb, it = lbfgs(xa, G)
    print("Adam 400: lnL %.2f; + L-BFGS (%d it): %.2f" % (G(xa)[0], it, Lb))

if __name__ == "__main__":
    if sys.argv[1] == "check":
        check()
    else:
        main(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
