"""Likelihood embedding (idea 005, session 12): fit spatial positions to ALL the counts at once, each with its own counting noise, instead of turning
small counts into distances first. Diamond benchmark (his t, tips v1 / vn as references, as in r18/r19). Times are fixed (his t) for every arm.
Model, given spatial positions x_i (tips at x = 0):
  spacelike a, b (reference c = v1 or vn, the side with more events; b = the smaller interval from c):
      n_C | n_b ~ Binomial(n_b, w),  w = table(alpha, d / tau_ca),  alpha = tau_cb / tau_ca from the counts, d^2 = |x_a - x_b|^2 - (t_a - t_b)^2 from the positions
      (an event of I(c, b) lies in the overlap with probability V_C / V_b = w: the table of r11, valid for any c);
  related a < b:  N_ab (strictly between) ~ Poisson(rho * pi/24 * tau^4), used in its Gaussian form for tau^2 = (t_b - t_a)^2 - |x_b - x_a|^2.
Maximize the total log-likelihood over the 3n spatial coordinates with Adam (analytic gradients), from the count-weighted fit (K0 = 100).
Validation: on a small universe the analytic gradient is checked against finite differences; started from the TRUE positions the fit must stay close to them.
Usage: python r23_likelihood.py [n reps seed iters]   |   python r23_likelihood.py check
"""
import sys
import time
import numpy as np
from r11_4d_distance import load_table, ALPHAS, DELTAS
from r12_johnston_compare import johnston
from r13_mixed import embed_from_r, sprinkle
from r18_waist_oracle import ours_with_counts
from r19_cluster_wfit import fit_w

np.seterr(all="ignore")
C4 = np.pi / 24
EPS = 1e-9

class Table:
    """w(alpha, delta) and dw/ddelta, bilinear in (log alpha, delta) on the monotone table."""
    def __init__(self, W):
        self.W = np.minimum.accumulate(W, axis=1)
        self.la0, self.dla = np.log(ALPHAS[0]), np.log(ALPHAS[1]) - np.log(ALPHAS[0])
        self.dd = DELTAS[1] - DELTAS[0]
    def __call__(self, alpha, delta):
        g = (np.log(np.clip(alpha, ALPHAS[0], ALPHAS[-1])) - self.la0) / self.dla
        i = np.clip(np.floor(g).astype(int), 0, len(ALPHAS) - 2); f = g - i
        h = np.clip(delta, 0, DELTAS[-1] - 1e-9) / self.dd
        j = np.clip(np.floor(h).astype(int), 0, len(DELTAS) - 2); e = h - j
        W = self.W
        w0 = (1 - f) * W[i, j] + f * W[i + 1, j]
        w1 = (1 - f) * W[i, j + 1] + f * W[i + 1, j + 1]
        return (1 - e) * w0 + e * w1, (w1 - w0) / self.dd

def setup(C, rho, t, W):
    """Count data: spacelike pairs (I, J, n_b, n_C, alpha, tau_ca) and related pairs (A, B, N)."""
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
    big, small = np.maximum(na, nb), np.minimum(na, nb)
    ok = small >= 1
    tca = (big / (rho * C4)) ** 0.25                                    # the larger interval, from counts
    alpha = (np.maximum(small, 0.5) / big) ** 0.25
    S = dict(I=I[ok], J=J[ok], nb=small[ok].astype(float), nc=np.minimum(nc[ok], small[ok]).astype(float), alpha=alpha[ok], tca=tca[ok])
    N = Cf @ Cf
    A, B = np.nonzero(np.triu(C | C.T, 1))
    Nab = np.maximum(N[A, B], N[B, A]).astype(float)
    t2 = np.sqrt((Nab + 0.5) / (rho * C4))
    Rl = dict(A=A, B=B, t2=t2, sd=t2 / (2 * np.sqrt(Nab + 1)))
    return S, Rl

def loglik(x, t, S, Rl, rho, tab, grad=True):
    n = len(x)
    g = np.zeros_like(x)
    # spacelike: binomial
    dx = x[S["I"]] - x[S["J"]]
    dt = t[S["I"]] - t[S["J"]]
    d2 = (dx ** 2).sum(1) - dt ** 2
    d = np.sqrt(np.maximum(d2, EPS))
    w, dw = tab(S["alpha"], d / S["tca"])
    w = np.clip(w, 1e-6, 1 - 1e-6)
    L = (S["nc"] * np.log(w) + (S["nb"] - S["nc"]) * np.log(1 - w)).sum()
    if grad:
        dl_dw = S["nc"] / w - (S["nb"] - S["nc"]) / (1 - w)
        coef = dl_dw * dw / S["tca"] / d * (d2 > EPS)                  # dl/d(dx) = coef * dx  (d d / d dx = dx / d)
        gv = coef[:, None] * dx
        for k in range(3):
            g[:, k] += np.bincount(S["I"], gv[:, k], n) - np.bincount(S["J"], gv[:, k], n)
    # related: Poisson count, in its Gaussian form for tau^2 (smooth also where trial positions make the pair spacelike):
    # tau2_hat = sqrt((N + 1/2) / (rho C4)), sd = tau2_hat / (2 sqrt(N + 1))  (delta tau^2 / tau^2 = delta N / 2N)
    dx = x[Rl["B"]] - x[Rl["A"]]
    tau2 = (t[Rl["B"]] - t[Rl["A"]]) ** 2 - (dx ** 2).sum(1)
    r = (tau2 - Rl["t2"]) / Rl["sd"]
    L += -0.5 * (r ** 2).sum()
    if grad:
        dl_dtau2 = -r / Rl["sd"]                                       # d tau2 / d dx = -2 dx
        gv = (-2 * dl_dtau2)[:, None] * dx
        for k in range(3):
            g[:, k] += np.bincount(Rl["B"], gv[:, k], n) - np.bincount(Rl["A"], gv[:, k], n)
    g[0] = 0; g[-1] = 0                                               # tips pinned at x = 0 (gauge)
    return L, g

def fit(x0, t, S, Rl, rho, tab, iters=400, lr=None):
    """Adam ascent on the log-likelihood; step scale ~ 1 % of the typical spatial spread."""
    x = x0.copy(); x[0] = 0; x[-1] = 0
    lr = lr or 0.01 * np.std(x0)
    m = np.zeros_like(x); v = np.zeros_like(x)
    hist = []
    for k in range(1, iters + 1):
        L, g = loglik(x, t, S, Rl, rho, tab)
        m = 0.9 * m + 0.1 * g; v = 0.999 * v + 0.001 * g ** 2
        x += lr * (m / (1 - 0.9 ** k)) / (np.sqrt(v / (1 - 0.999 ** k)) + 1e-12)
        if k % 50 == 0 or k == 1:
            hist.append((k, L))
        if k == iters // 2:
            lr *= 0.3
    return x, hist

def scorer(P, iu):
    st = np.sqrt(((P[:, None, 1:] - P[None, :, 1:]) ** 2).sum(-1))[iu]
    return lambda Y: np.corrcoef(np.sqrt(((Y[:, None] - Y[None]) ** 2).sum(-1))[iu], st)[0, 1]

def check():
    """Gradient vs finite differences; fit started from the truth stays near the truth."""
    W = load_table(); tab = Table(W)
    rng = np.random.default_rng(11)
    P, C, rho = sprinkle(400, rng)
    t = P[:, 0]
    S, Rl = setup(C, rho, t, W)
    x = P[:, 1:] + 0.02 * rng.standard_normal((len(P), 3)); x[0] = 0; x[-1] = 0
    L, g = loglik(x, t, S, Rl, rho, tab)
    errs = []
    for (i, k) in [(5, 0), (50, 1), (200, 2), (300, 0)]:
        h = 1e-6; xp = x.copy(); xp[i, k] += h; xm = x.copy(); xm[i, k] -= h
        num = (loglik(xp, t, S, Rl, rho, tab, False)[0] - loglik(xm, t, S, Rl, rho, tab, False)[0]) / (2 * h)
        errs.append((g[i, k], num))
    print("gradient check (analytic, numeric):", ", ".join("%.4g/%.4g" % e for e in errs))
    iu = np.triu_indices(len(P), 1); sc = scorer(P, iu)
    xt = P[:, 1:].copy()
    xf, hist = fit(xt, t, S, Rl, rho, tab, 300)
    print("from the truth (true t): corr %.4f -> %.4f; loglik %s" % (sc(xt), sc(xf), " ".join("%d:%.1f" % h for h in hist[::2])))

def run(n, reps, seed, iters):
    W = load_table(); tab = Table(W)
    rng = np.random.default_rng(seed)
    names = ["johnston", "switch", "w_K100", "likelihood"]
    rows = []
    for _ in range(reps):
        t0 = time.time()
        P, C, rho = sprinkle(n, rng)
        iu = np.triu_indices(len(P), 1); sc = scorer(P, iu)
        r_j, Xj = johnston(C, rho, 1.0)
        t = Xj[:, 0]
        I, J, s, kc = ours_with_counts(C, rho, t, W)
        have = np.isfinite(s); rj = r_j[I, J]
        sw = r_j.copy(); v = np.where(have & (s < 0.25), s, rj); sw[I, J] = v; sw[J, I] = v
        rel = C | C.T
        Rrel = np.where(rel, r_j, np.inf); np.fill_diagonal(Rrel, 0.0)
        Xw, _ = fit_w(Rrel, t, I, J, s, kc, 100)
        S, Rl = setup(C, rho, t, W)
        xl, hist = fit(Xw[:, 1:], t, S, Rl, rho, tab, iters)
        row = [sc(Xj[:, 1:]), sc(embed_from_r(sw, t)[:, 1:]), sc(Xw[:, 1:]), sc(xl)]
        rows.append(row)
        print("  universe %d (%.0f s): " % (len(rows), time.time() - t0) + "  ".join("%s %.4f" % (a, r) for a, r in zip(names, row)) +
              "   loglik " + " ".join("%d:%.0f" % h for h in hist[::2]), flush=True)
    A = np.array(rows); d = A - A[:, :1]
    print("n = %d (%d univ., seed %d, %d iterations)" % (n, reps, seed, iters))
    for a, m, dm, de in zip(names, A.mean(0), d.mean(0), d.std(0, ddof=1) / np.sqrt(reps) if reps > 1 else np.full(len(names), np.nan)):
        print("  %-10s spatial corr %.4f   vs johnston %+.4f +- %.4f   (%+.0f %% of his residual)" % (a, m, dm, de, 100 * dm / (1 - A[:, 0].mean())))

if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "check":
        check()
    else:
        run(int(a[0]) if a else 1500, int(a[1]) if len(a) > 1 else 3, int(a[2]) if len(a) > 2 else 7070, int(a[3]) if len(a) > 3 else 400)
