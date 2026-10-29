"""Stage S4a (idea 005): the rectangle distance estimator in curved 2D spacetime (de Sitter), with a flat control.

Continuum prediction [ours] (H = 1, a and b on the same conformal slice, c a proper time tau below them):
    d_est^2 / d^2 = 1 - tau^2 / 8 + O(tau^4, d^2)      i.e.  1 - R tau^2 / 16  with R = 2 H^2.
In flat space the ratio is exactly 1 for every c. So the depth dependence of the estimate measures curvature.

Region: conformal time eta in [ETA_LO, ETA_HI], x in [-X, X]; u = eta - x, v = eta + x.
de Sitter: ds^2 = eta^-2 (-d eta^2 + dx^2), density per coordinate area rho / eta^2.
Flat:      same coordinates with conformal factor 1, density rho per coordinate area.
Test events a, b are inserted by hand (lesson 9) at eta0, x = -+delta/2.
"""
import numpy as np

ETA_LO, ETA_HI, X = -3.0, -1.0, 1.0

def sprinkle(rho, desitter, rng):
    if desitter:
        n = rng.poisson(rho * 2 * X * (1 / -ETA_HI - 1 / -ETA_LO))
        w = 1 / -ETA_LO + (1 / -ETA_HI - 1 / -ETA_LO) * rng.random(n)   # w = -1/eta uniform <=> density ~ eta^-2
        eta = -1 / w
    else:
        n = rng.poisson(rho * 2 * X * (ETA_HI - ETA_LO))
        eta = ETA_LO + (ETA_HI - ETA_LO) * rng.random(n)
    x = X * (2 * rng.random(n) - 1)
    return eta, x

def inside(eta, x):
    return (eta >= ETA_LO) & (eta <= ETA_HI) & (np.abs(x) <= X)

def true_distance(eta0, delta, desitter):
    return np.arccos(1 - delta**2 / (2 * eta0**2)) if desitter else delta

def true_tau(eta1, x1, eta2, x2, desitter):
    if desitter:
        return np.arccosh((eta1**2 + eta2**2 - (x1 - x2)**2) / (2 * eta1 * eta2))
    return np.sqrt((eta2 - eta1)**2 - (x2 - x1)**2)

def rect_volume(u1, u2, v1, v2):
    """Exact de Sitter volume of the (u, v) rectangle: 2 ln(eta_L eta_R / (eta_bottom eta_top)), eta = (u + v) / 2."""
    return 2 * np.log(((u2 + v1) / 2) * ((u1 + v2) / 2) / (((u1 + v1) / 2) * ((u2 + v2) / 2)))

def continuum_ratio(eta_c, x_c, eta0, delta):
    """Continuum d_est^2 / d^2 for c at (eta_c, x_c), a = (eta0, -delta/2), b = (eta0, +delta/2) in de Sitter."""
    ua, va, ub, vb = eta0 + delta / 2, eta0 - delta / 2, eta0 - delta / 2, eta0 + delta / 2
    uc, vc = eta_c - x_c, eta_c + x_c
    VC, VA, VB = rect_volume(uc, ub, vc, va), rect_volume(ub, ua, vc, va), rect_volume(uc, ub, va, vb)
    return 2 * VA * VB / VC / true_distance(eta0, delta, True)**2

def run(rho, desitter, eta0, delta, seed):
    """Returns, for each usable c: true tau from c to the a-b midpoint, d_est^2 / d_true^2, N_A, N_B, N_C."""
    rng = np.random.default_rng(seed)
    eta, x = sprinkle(rho, desitter, rng)
    eta = np.append(eta, [eta0, eta0]); x = np.append(x, [-delta / 2, delta / 2])
    a, b = len(eta) - 2, len(eta) - 1
    u, v = eta - x, eta + x
    # only the rows/columns we need: z in the past of a or b
    past_ab = ((u < u[a]) & (v < v[a])) | ((u < u[b]) & (v < v[b]))
    idx = np.flatnonzero(past_ab)
    uu, vv = u[idx], v[idx]
    Cs = (uu[:, None] < uu[None, :]) & (vv[:, None] < vv[None, :])          # causal matrix on the past set
    to_a = (uu < u[a]) & (vv < v[a]); to_b = (uu < u[b]) & (vv < v[b])
    both = to_a & to_b
    Cf = Cs.astype(np.float32)
    with np.errstate(all="ignore"):
        nIa = Cf @ to_a.astype(np.float32)
        nIb = Cf @ to_b.astype(np.float32)
        nC = Cf @ both.astype(np.float32)
    cs = np.flatnonzero(both)
    # keep c only if the whole rectangle from c to the join of a, b lies inside the sprinkled region
    uj, vj = max(u[a], u[b]), max(v[a], v[b])
    corners_ok = inside((uu[cs] + vj) / 2, (vj - uu[cs]) / 2) & inside((uj + vv[cs]) / 2, (vv[cs] - uj) / 2)
    cs = cs[corners_ok & (nC[cs] > 0)]
    nA, nB, nCc = nIa[cs] - nC[cs], nIb[cs] - nC[cs], nC[cs]
    # N_A, N_B, N_C are counts in disjoint regions => independent Poisson. N_A N_B is unbiased for
    # lambda_A lambda_B; 1/(N_C + 1) has mean (1 - e^-lambda)/lambda, i.e. unbiased for 1/lambda_C up to e^-lambda.
    d2_est = 2 * nA * nB / (rho * (nCc + 1))
    d_true = true_distance(eta0, delta, desitter)
    eta_c, x_c = (uu[cs] + vv[cs]) / 2, (vv[cs] - uu[cs]) / 2
    tau = true_tau(eta_c, x_c, eta0, 0.0, desitter)
    pred = continuum_ratio(eta_c, x_c, eta0, delta) if desitter else np.ones_like(tau)
    return tau, d2_est / d_true**2, pred, nA, nB, nCc

if __name__ == "__main__":
    rho, eta0, delta = 10000.0, -1.05, 0.15
    bins = np.array([0.05, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9])
    seeds = range(1, 101)
    print(f"rho = {rho:.0f} (ell = {rho**-0.5:.4f}), a, b at eta0 = {eta0}, comoving delta = {delta}"
          f" (d = {true_distance(eta0, delta, True):.4f} = {true_distance(eta0, delta, True)*rho**0.5:.1f} ell)")
    for desitter in (False, True):
        per_seed = []
        for s in seeds:
            tau, r, pred, *_ = run(rho, desitter, eta0, delta, s)
            row = []
            for lo, hi in zip(bins[:-1], bins[1:]):
                m = (tau >= lo) & (tau < hi)
                row += [np.mean(r[m]), np.mean(pred[m])] if m.sum() > 5 else [np.nan, np.nan]
            per_seed.append(row)
        P = np.array(per_seed)
        print("de Sitter" if desitter else "flat (control)")
        print(f"  {'tau bin':>11} {'measured d_est^2/d^2':>21} {'s.e. (seeds)':>12} {'continuum':>10}"
              f" {'1 - tau^2/8':>11}")
        for i, (lo, hi) in enumerate(zip(bins[:-1], bins[1:])):
            mid = (lo + hi) / 2
            print(f"  {lo:.2f}-{hi:.2f}   {np.nanmean(P[:, 2*i]):19.4f}   {np.nanstd(P[:, 2*i]) / np.sqrt(len(seeds)):10.4f}"
                  f"   {np.nanmean(P[:, 2*i+1]):9.4f}   {(1 - mid**2 / 8) if desitter else 1.0:9.4f}")
