"""Depth-drift curvature beyond de Sitter, and the count-only curvature fit with fixed seeds (idea 005, session 11; Part I note Sec. 4).

1. fit  : the session-3 fit, reimplemented (its script was not kept). For one pair a, b and every sprinkled c in their common past:
          d2 = 2 N_A N_B / (rho (N_C + 1)),  tau^2 = (N_I(c,a) + N_I(c,b)) / rho  (counts only),  fit d2 = alpha + beta tau^2 over tau in [0.2, 0.7],
          R_est = -16 beta / alpha.  de Sitter (H = 1, R = 2) and flat, rho = 4000 and 1e4, 100 sprinklings each (seeds 1..100), via s4a_desitter.run.
2. frw-analytic : 2D FRW  ds^2 = a(eta)^2 (-d eta^2 + dx^2),  a = eta^p  (eta > 0).  Conformally flat, so the tiles are the same rectangles as in flat space.
          Curvature R = 2 (ln a)'' / a^2 = -2 p eta^(-2 - 2p)  (check: de Sitter a = -1/(H eta) gives 2 H^2).
          Rectangle volume  V = (1/2) int int a((u+v)/2)^2 du dv = (1/2) [G(u2+v2) - G(u2+v1) - G(u1+v2) + G(u1+v1)],  G'' (s) = (s/2)^(2p),
          G(s) = 4 (s/2)^(2p+2) / ((2p+1)(2p+2)).  a, b at (eta0, -+h), c straight below at eta_c, h -> 0.  Question: is 1 - ratio = R tau^2 / 16 + O(tau^3),
          and with R evaluated where?  We print 16 (1 - ratio) / tau^2 against R at a, b (eta0), at c, and at the midpoint in proper time.
3. frw-sprinkle : p = 1 (R < 0, ratio > 1), rho = 1e4, a, b inserted by hand ~14 ell apart at eta0 = 1.5; Poisson sprinkling of the past cone of the join of a, b
          (so every rectangle from c to the join is inside). Measured ratio per depth bin vs the exact continuum for the same c's; then the count-only fit.
Usage: python r9_drift_fit_frw.py [fit|frw-analytic|frw-sprinkle ...]   (no argument: all)
"""
import sys
import numpy as np
import s4a_desitter as ds

np.seterr(all="ignore")                          # numpy + Accelerate: spurious matmul warnings

def fit_one(nA, nB, nC, rho, lo=0.2, hi=0.7):
    d2 = 2 * nA * nB / (rho * (nC + 1))
    t2 = (nA + nB + 2 * nC) / rho                # N_I(c,a) + N_I(c,b), each tau^2 = 2 N / rho, averaged
    m = (t2 >= lo ** 2) & (t2 <= hi ** 2)
    if m.sum() < 10:
        return np.nan
    beta, alpha = np.polyfit(t2[m], d2[m], 1)
    return -16 * beta / alpha

def part_fit():
    print("== count-only curvature fit, one pair per sprinkling, seeds 1..100 ==")
    eta0, delta = -1.05, 0.15
    for rho in (4000.0, 10000.0):
        for desitter in (False, True):
            R = np.array([fit_one(*ds.run(rho, desitter, eta0, delta, s)[3:], rho) for s in range(1, 101)])
            R = R[np.isfinite(R)]
            print(f"  rho={rho:6.0f} {'de Sitter (R=2)' if desitter else 'flat (R=0)':<16} R_est = {R.mean():+.2f} +- {R.std() / np.sqrt(len(R)):.2f}"
                  f"   spread per pair {R.std():.1f}   (n={len(R)})", flush=True)
    # continuum fit in the same window (exact de Sitter volumes, c straight below, tau from the exact volumes as the counts would give)
    taus = np.linspace(0.2, 0.7, 60)
    ratio = np.array([ds.continuum_ratio(eta0 * np.exp(t), 0.0, eta0, 1e-4) for t in taus])
    beta, alpha = np.polyfit(taus ** 2, ratio, 1)
    print(f"  continuum (c straight below, true tau) in this window: R_fit = {-16 * beta / alpha:.2f}")

# ---------- FRW a = eta^p ----------
def G(s, p):
    return 4 * (s / 2) ** (2 * p + 2) / ((2 * p + 1) * (2 * p + 2))

def vol(u1, u2, v1, v2, p):
    return 0.5 * (G(u2 + v2, p) - G(u2 + v1, p) - G(u1 + v2, p) + G(u1 + v1, p))

def ratio_frw(eta_c, x_c, eta0, h, p):
    """Exact continuum d_est^2 / d^2 for a = (eta0, -h), b = (eta0, +h), c = (eta_c, x_c); d = a(eta0) 2h (slice distance, exact as h -> 0)."""
    ua, va, ub, vb = eta0 + h, eta0 - h, eta0 - h, eta0 + h          # u = eta - x, v = eta + x
    uc, vc = eta_c - x_c, eta_c + x_c
    VC = vol(uc, ub, vc, va, p)                                      # [uc, min u] x [vc, min v]
    VA = vol(ub, ua, vc, va, p)                                      # strip seen only by a
    VB = vol(uc, ub, va, vb, p)                                      # strip seen only by b
    return 2 * VA * VB / VC / (eta0 ** p * 2 * h) ** 2

def tau_down(eta_c, eta0, p):
    return (eta0 ** (p + 1) - eta_c ** (p + 1)) / (p + 1)

def R_of(eta, p):
    return -2 * p * eta ** (-2.0 - 2 * p)

def eta_at_tau(eta0, tau, p):
    return (eta0 ** (p + 1) - (p + 1) * tau) ** (1 / (p + 1))

def part_frw_analytic():
    print("== FRW a = eta^p, exact volumes, h -> 0: 16 (1 - ratio) / tau^2 vs R at a,b / at the proper-time midpoint / at c ==")
    for p, eta0 in ((1.0, 1.5), (-2.0, 1.0), (0.5, 1.0)):
        print(f"  p = {p}, eta0 = {eta0}: R(eta0) = {R_of(eta0, p):+.4f}")
        for tau in (0.01, 0.03, 0.1, 0.2, 0.4):
            eta_c = eta_at_tau(eta0, tau, p)
            r = ratio_frw(eta_c, 0.0, eta0, 1e-5, p)
            eta_mid = eta_at_tau(eta0, tau / 2, p)
            print(f"    tau={tau:5.2f}: 16(1-ratio)/tau^2 = {16 * (1 - r) / tau ** 2:+.4f}   R(ab) {R_of(eta0, p):+.4f}"
                  f"   R(mid) {R_of(eta_mid, p):+.4f}   R(c) {R_of(eta_c, p):+.4f}")
    # sanity: the same code with the de Sitter weight reproduces Eq. (drift)
    print("  check vs de Sitter closed form (s4a_desitter.continuum_ratio): tau=0.5:",
          round(ds.continuum_ratio(-1.05 * np.exp(0.5), 0.0, -1.05, 1e-5), 6), "closed form",
          round(np.tanh(0.25) ** 2 / (2 * np.log(np.cosh(0.25))), 6))

def part_frw_sprinkle(seeds=200, rho=1e4, p=1.0, eta0=1.5, eta_lo=0.55):
    print(f"== FRW p = {p} sprinkling, rho = {rho:.0f}, a,b at eta0 = {eta0}, {seeds} sprinklings ==")
    h = 0.14 / (2 * eta0 ** p)                                       # proper separation 0.14 = 14 ell
    eta_j = eta0 + h                                                 # join of a and b, at x = 0
    L = eta_j - eta_lo
    bins = np.array([0.05, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9])
    P, Q, Rfit = [], [], []
    for s in range(1, seeds + 1):
        rng = np.random.default_rng(s)
        n = rng.poisson(rho * eta_j ** (2 * p) * L * 2 * L)           # candidates in the box [eta_lo, eta_j] x [-L, L] at the max density
        eta = eta_lo + L * rng.random(n); x = L * (2 * rng.random(n) - 1)
        keep = (np.abs(x) < eta_j - eta) & (rng.random(n) < (eta / eta_j) ** (2 * p))   # thin to density rho a^2, inside the join's past cone
        eta, x = np.append(eta[keep], [eta0, eta0]), np.append(x[keep], [-h, h])
        u, v = eta - x, eta + x
        a, b = len(u) - 2, len(u) - 1
        to_a = (u < u[a]) & (v < v[a]); to_b = (u < u[b]) & (v < v[b])
        idx = np.flatnonzero(to_a | to_b)
        uu, vv = u[idx], v[idx]
        Cf = ((uu[:, None] < uu[None, :]) & (vv[:, None] < vv[None, :])).astype(np.float32)
        ta, tb = to_a[idx], to_b[idx]
        nIa, nIb, nC = Cf @ ta.astype(np.float32), Cf @ tb.astype(np.float32), Cf @ (ta & tb).astype(np.float32)
        cs = np.flatnonzero(ta & tb)
        cs = cs[nC[cs] > 0]
        nA, nB, nCc = nIa[cs] - nC[cs], nIb[cs] - nC[cs], nC[cs]
        r = 2 * nA * nB / (rho * (nCc + 1)) / (eta0 ** p * 2 * h) ** 2
        ec, xc = (uu[cs] + vv[cs]) / 2, (vv[cs] - uu[cs]) / 2
        pred = ratio_frw(ec, xc, eta0, h, p)
        tau = tau_down(ec, eta0, p)                                  # proper time up to the a-b slice (exact for x_c = 0; a depth label otherwise)
        sel = [(tau >= lo) & (tau < hi) for lo, hi in zip(bins[:-1], bins[1:])]
        P.append([r[m].mean() if m.sum() > 5 else np.nan for m in sel])
        Q.append([pred[m].mean() if m.sum() > 5 else np.nan for m in sel])
        Rfit.append(fit_one(nA, nB, nCc, rho))
    P, Q, Rfit = np.array(P), np.array(Q), np.array(Rfit)
    m, e, q = np.nanmean(P, 0), np.nanstd(P, 0) / np.sqrt(np.isfinite(P).sum(0)), np.nanmean(Q, 0)
    for i, (lo, hi) in enumerate(zip(bins[:-1], bins[1:])):
        print(f"  tau {lo:.2f}-{hi:.2f}: measured {m[i]:.4f} +- {e[i]:.4f}   continuum {q[i]:.4f}   diff {(m[i] - q[i]) / e[i]:+.1f} sigma")
    Rfit = Rfit[np.isfinite(Rfit)]
    print(f"  count-only fit: R_est = {Rfit.mean():+.2f} +- {Rfit.std() / np.sqrt(len(Rfit)):.2f} (spread per pair {Rfit.std():.1f}); "
          f"R at a,b = {R_of(eta0, p):+.3f}; R over the window: {R_of(eta_at_tau(eta0, 0.2, p), p):+.3f} .. {R_of(eta_at_tau(eta0, 0.7, p), p):+.3f}")

if __name__ == "__main__":
    which = sys.argv[1:] or ["frw-analytic", "fit", "frw-sprinkle"]
    for w in which:
        {"fit": part_fit, "frw-analytic": part_frw_analytic, "frw-sprinkle": part_frw_sprinkle}[w]()
