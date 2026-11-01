"""Depth-drift curvature estimator: the points of external referee round 1 (session 17; toolkit-1p1-v1, Major 3). de Sitter (H = 1, R = 2) and flat
in the same conformal region as s4a_desitter.py (eta in [-3, -1], |x| <= 1), a, b near eta0 = -1.05, 0.15 apart in comoving x (~14 ell at rho = 1e4).
  fit   : R_est = -16 beta / alpha from d2 = alpha + beta tau^2 (+ gamma tau^4 for 'quad'), tau^2 = (N_I(c,a) + N_I(c,b)) / rho, over the c's selected by a rule:
            paper     : tau in [0.2, 0.7] (in units of 1/H: the window the referee objects to)
            intrinsic : N_C >= 20 and tau^2 <= q * max tau^2 over the usable c's (q = 1 by default; scanned), no reference to H
          For each rule the same fit on the exact continuum volumes of the SAME c's (R_cont) is the target; measured - R_cont is the discreteness offset.
          Pairs: 'inserted' (a, b put in by hand, as in the paper) and 'sprinkled' (the sprinkled elements nearest to the two target points).
  noise : at equal density, the spread of single estimates of R:
            ours      : one pair, intrinsic rule;
            BD        : R = -2 B_eps[1](x) at x = (eta0, 0) (Benincasa-Dowker / Sorkin nonlocal 2D operator,
                        B_eps phi(x) = (4 eps rho) [-phi(x)/2 + eps sum_{y<x} f(n_xy, eps) phi(y)],
                        f(n, eps) = (1-eps)^n - 2 eps n (1-eps)^(n-1) + eps^2 n (n-1)/2 (1-eps)^(n-2); its mean -> box phi - R phi / 2);
            chains    : ordering fraction f = C_2 / binom(N, 2) of the interval from c (proper time tau_D straight below x) to x; flat f = 1/2;
                        R_est = 2 (f - 1/2) / (f_dS(tau_D) - 1/2), with f_dS from the exact continuum (Monte Carlo, 2e6 point pairs).
  split : the fix for the offset found by 'fit'. d2 and tau^2 are both built from N_A, N_B, so their noise is correlated and tilts the slope
          (in flat space beta > 0, i.e. R_est < 0). Thinning the sprinkling at random into two independent Poisson halves (density rho/2 each),
          d2 is taken from half 1 and tau^2, and every selection, from half 2 only; rules as above with N_C >= 10 on half 2.
          RESULT (session 17): the split does not remove the offset (it grows at the halved density), so correlated noise is not the cause.
  pooled: the cause tested instead: R_est = -16 beta / alpha is a ratio of two fitted coefficients whose errors are anticorrelated (intercept and
          slope of one least-squares fit), so E[-16 beta / alpha] is biased low, by an amount falling with density. Pooling over the pairs of a
          region first, R_pool = -16 <beta> / <alpha>, removes the first-order term. Bootstrap over pairs for the s.e. (2000 resamples).
Usage: python r37_curvature_referee.py [fit|scan|noise|split|pooled ...]
"""
import sys
import numpy as np
import s4a_desitter as ds

np.seterr(all="ignore")
ETA0, DELTA = -1.05, 0.15

def vol(u1, u2, v1, v2, desitter):
    return ds.rect_volume(u1, u2, v1, v2) if desitter else 0.5 * (u2 - u1) * (v2 - v1)

def counts(rho, desitter, seed, mode="inserted", split=False):
    """Per usable c: N_A, N_B, N_C and the exact continuum volumes V_A, V_B, V_C (region and corner filter as s4a_desitter.run)."""
    rng = np.random.default_rng(seed)
    eta, x = ds.sprinkle(rho, desitter, rng)
    if mode == "inserted":
        eta = np.append(eta, [ETA0, ETA0]); x = np.append(x, [-DELTA / 2, DELTA / 2]); a, b = len(eta) - 2, len(eta) - 1
    else:
        a = np.argmin((eta - ETA0) ** 2 + (x + DELTA / 2) ** 2); b = np.argmin((eta - ETA0) ** 2 + (x - DELTA / 2) ** 2)
    u, v = eta - x, eta + x
    if (u[a] - u[b]) * (v[a] - v[b]) >= 0:
        return None
    if u[a] > u[b]:
        a, b = b, a                                                   # convention: u_a < u_b, v_a > v_b
    to_a = (u < u[a]) & (v < v[a]); to_b = (u < u[b]) & (v < v[b])
    idx = np.flatnonzero(to_a | to_b)
    uu, vv = u[idx], v[idx]
    Cf = ((uu[:, None] < uu[None, :]) & (vv[:, None] < vv[None, :])).astype(np.float32)
    ta, tb = to_a[idx], to_b[idx]
    nIa, nIb, nC = Cf @ ta.astype(np.float32), Cf @ tb.astype(np.float32), Cf @ (ta & tb).astype(np.float32)
    cs = np.flatnonzero(ta & tb)
    uj, vj = u[b], v[a]                                               # join
    ok = ds.inside((uu[cs] + vj) / 2, (vj - uu[cs]) / 2) & ds.inside((uj + vv[cs]) / 2, (vv[cs] - uj) / 2)
    cs = cs[ok & (nC[cs] > 0)]
    uc, vc = uu[cs], vv[cs]
    VC = vol(uc, u[a], vc, v[b], desitter); VA = vol(uc, u[a], v[b], v[a], desitter); VB = vol(u[a], u[b], vc, v[b], desitter)
    K = dict(nA=nIa[cs] - nC[cs], nB=nIb[cs] - nC[cs], nC=nC[cs], VA=VA, VB=VB, VC=VC)
    if split:                                                         # independent thinning (own rng: the sprinkling above is unchanged)
        h1 = np.random.default_rng(10 ** 6 + seed).random(len(idx)) < 0.5
        for tag, h in (("1", h1), ("2", ~h1)):
            ia, ib, ic = (Cf @ (ta & h).astype(np.float32))[cs], (Cf @ (tb & h).astype(np.float32))[cs], (Cf @ (ta & tb & h).astype(np.float32))[cs]
            K["nA" + tag], K["nB" + tag], K["nC" + tag] = ia - ic, ib - ic, ic
    return K

def fit_R(d2, t2, sel, quad=False):
    if sel.sum() < 10:
        return np.nan
    c = np.polyfit(t2[sel], d2[sel], 2 if quad else 1)
    beta, alpha = (c[1], c[2]) if quad else (c[0], c[1])
    return -16 * beta / alpha

def rules(K, rho, q=1.0, kmin=20):
    d2 = 2 * K["nA"] * K["nB"] / (rho * (K["nC"] + 1)); t2 = (K["nA"] + K["nB"] + 2 * K["nC"]) / rho
    d2c = 2 * K["VA"] * K["VB"] / K["VC"]; t2c = K["VA"] + K["VB"] + 2 * K["VC"]       # tau^2 = 2 V, averaged over the two intervals
    paper = (t2 >= 0.04) & (t2 <= 0.49)
    base = K["nC"] >= kmin
    intr = base & (t2 <= q * t2[base].max()) if base.any() else base
    out = {}
    for name, sel, quad in (("paper", paper, False), ("intrinsic", intr, False), ("intrinsic_quad", intr, True)):
        out[name] = (fit_R(d2, t2, sel, quad), fit_R(d2c, t2c, sel, quad))
    return out

def part_fit(seeds=1000):
    print(f"== curvature fit, one pair per sprinkling, {seeds} sprinklings per row; R_cont = same fit on exact volumes of the same c's ==")
    for rho in (4000.0, 1e4):
        for desitter in (False, True):
            for mode in ("inserted", "sprinkled"):
                res = {}
                for s in range(1, seeds + 1):
                    K = counts(rho, desitter, s, mode)
                    if K is None:
                        continue
                    for k, v in rules(K, rho).items():
                        res.setdefault(k, []).append(v)
                for k, v in res.items():
                    v = np.array(v); v = v[np.isfinite(v).all(1)]
                    m, mc, dlt = v[:, 0].mean(), v[:, 1].mean(), v[:, 0] - v[:, 1]
                    print(f"  rho {rho:6.0f} {'dS  ' if desitter else 'flat'} {mode:9s} {k:15s} R_est {m:+.2f} +- {v[:, 0].std() / np.sqrt(len(v)):.2f}"
                          f"  R_cont {mc:+.2f}  offset {dlt.mean():+.2f} +- {dlt.std() / np.sqrt(len(v)):.2f}  spread per pair {v[:, 0].std():.1f}  (n={len(v)})", flush=True)

def part_scan(seeds=400, rho=1e4):
    print(f"== sensitivity of the intrinsic rule (de Sitter, inserted pairs, rho = {rho:.0f}, {seeds} sprinklings): lower cut N_C >= k, upper tau^2 <= q max ==")
    Ks = [counts(rho, True, s) for s in range(1, seeds + 1)]
    for kmin in (5, 20, 50):
        for q in (0.5, 0.75, 1.0):
            v = np.array([rules(K, rho, q, kmin)["intrinsic"] for K in Ks]); v = v[np.isfinite(v).all(1)]
            dlt = v[:, 0] - v[:, 1]
            print(f"  k {kmin:3d} q {q:.2f}: R_est {v[:, 0].mean():+.2f} +- {v[:, 0].std() / np.sqrt(len(v)):.2f}   R_cont {v[:, 1].mean():+.2f}"
                  f"   offset {dlt.mean():+.2f} +- {dlt.std() / np.sqrt(len(v)):.2f}   spread {v[:, 0].std():.1f}", flush=True)

def bd_f(n, eps):
    if eps == 1.0:
        return np.where(n == 0, 1.0, np.where(n == 1, -2.0, np.where(n == 2, 1.0, 0.0)))
    q = 1 - eps
    return q ** n - 2 * eps * n * q ** (n - 1) + 0.5 * eps ** 2 * n * (n - 1) * q ** (n - 2)

def f_cont(tauD, pairs=2_000_000, seed=5):
    """Ordering fraction of the exact continuum dS diamond of height tauD (bottom straight below x = (ETA0, 0)), Monte Carlo over point pairs."""
    rng = np.random.default_rng(seed)
    eb = ETA0 * np.exp(tauD)                                          # proper time along x = 0: tau = ln(eta_bottom / eta_top)
    ut, vt, ub, vb = ETA0, ETA0, eb, eb
    pts = []
    while sum(len(p) for p in pts) < 2 * pairs:
        uu = ub + (ut - ub) * rng.random(4 * pairs); vv = vb + (vt - vb) * rng.random(4 * pairs)
        w = ((ut + vt) / (uu + vv)) ** 2                              # dS density ~ 1/eta^2, normalized by its maximum (top corner, smallest |eta|)
        k = rng.random(4 * pairs) < w
        pts.append(np.column_stack([uu[k], vv[k]]))
    P = np.vstack(pts)[:2 * pairs]
    A, B = P[:pairs], P[pairs:]
    return np.mean(((A[:, 0] < B[:, 0]) & (A[:, 1] < B[:, 1])) | ((A[:, 0] > B[:, 0]) & (A[:, 1] > B[:, 1])))

def noise_one(rho, desitter, seed, epss, tauDs):
    rng = np.random.default_rng(seed)
    eta, x = ds.sprinkle(rho, desitter, rng)
    u, v = eta - x, eta + x
    ux = vx = ETA0
    past = np.flatnonzero((u < ux) & (v < vx))
    uu, vv = u[past], v[past]
    Cf = ((uu[:, None] < uu[None, :]) & (vv[:, None] < vv[None, :])).astype(np.float32)
    n = Cf @ np.ones(len(past), np.float32)                           # elements between y and x = elements of the past of x above y
    bd = [-2 * 4 * eps * rho * (-0.5 + eps * bd_f(n, eps).sum()) for eps in epss]
    ch = []
    for tauD in tauDs:
        ec = ETA0 * np.exp(tauD) if desitter else ETA0 - tauD
        ins = (uu > ec) & (vv > ec)
        N = ins.sum(); C2 = Cf[np.ix_(ins, ins)].sum()
        ch.append((C2 / (N * (N - 1) / 2), N))
    return bd, ch, len(past)

def rules_split(K, rho, q=1.0, kmin=10):
    r = rho / 2
    d2 = 2 * K["nA1"] * K["nB1"] / (r * (K["nC1"] + 1)); t2 = (K["nA2"] + K["nB2"] + 2 * K["nC2"]) / r
    d2c = 2 * K["VA"] * K["VB"] / K["VC"]; t2c = K["VA"] + K["VB"] + 2 * K["VC"]
    paper = (t2 >= 0.04) & (t2 <= 0.49)
    base = K["nC2"] >= kmin
    intr = base & (t2 <= q * t2[base].max()) if base.any() else base
    return {"split_paper": (fit_R(d2, t2, paper), fit_R(d2c, t2c, paper)), "split_intrinsic": (fit_R(d2, t2, intr), fit_R(d2c, t2c, intr))}

def part_split(seeds=1000):
    print(f"== split-sample fit (d2 from one random half, tau^2 and selection from the other), {seeds} sprinklings per row ==")
    for rho in (4000.0, 1e4):
        for desitter in (False, True):
            for mode in ("inserted", "sprinkled"):
                res = {}
                for s in range(1, seeds + 1):
                    K = counts(rho, desitter, s, mode, split=True)
                    if K is None:
                        continue
                    for k, v in rules_split(K, rho).items():
                        res.setdefault(k, []).append(v)
                for k, v in res.items():
                    v = np.array(v); v = v[np.isfinite(v).all(1)]
                    dlt = v[:, 0] - v[:, 1]
                    print(f"  rho {rho:6.0f} {'dS  ' if desitter else 'flat'} {mode:9s} {k:15s} R_est {v[:, 0].mean():+.2f} +- {v[:, 0].std() / np.sqrt(len(v)):.2f}"
                          f"  R_cont {v[:, 1].mean():+.2f}  offset {dlt.mean():+.2f} +- {dlt.std() / np.sqrt(len(v)):.2f}  spread per pair {v[:, 0].std():.1f}  (n={len(v)})", flush=True)

def fit_ba(d2, t2, sel):
    if sel.sum() < 10:
        return np.nan, np.nan
    return tuple(np.polyfit(t2[sel], d2[sel], 1))

def part_pooled(seeds=1000):
    print(f"== pooled estimator R = -16 <beta> / <alpha> over {seeds} pairs (one per sprinkling), against the mean of per-pair R ==")
    for rho in (4000.0, 1e4):
        for desitter in (False, True):
            for mode in ("inserted", "sprinkled"):
                rows = {"paper": [], "intrinsic": []}
                for s in range(1, seeds + 1):
                    K = counts(rho, desitter, s, mode)
                    if K is None:
                        continue
                    d2 = 2 * K["nA"] * K["nB"] / (rho * (K["nC"] + 1)); t2 = (K["nA"] + K["nB"] + 2 * K["nC"]) / rho
                    d2c = 2 * K["VA"] * K["VB"] / K["VC"]; t2c = K["VA"] + K["VB"] + 2 * K["VC"]
                    base = K["nC"] >= 20
                    sels = {"paper": (t2 >= 0.04) & (t2 <= 0.49), "intrinsic": base & (t2 <= t2[base].max()) if base.any() else base}
                    for k, sel in sels.items():
                        rows[k].append(fit_ba(d2, t2, sel) + fit_ba(d2c, t2c, sel))
                rng = np.random.default_rng(0)
                for k, v in rows.items():
                    v = np.array(v); v = v[np.isfinite(v).all(1)]
                    Rp = -16 * v[:, 0].mean() / v[:, 1].mean(); Rc = -16 * v[:, 2].mean() / v[:, 3].mean()
                    bs = [(lambda w: -16 * w[:, 0].mean() / w[:, 1].mean())(v[rng.integers(0, len(v), len(v))]) for _ in range(2000)]
                    per = -16 * v[:, 0] / v[:, 1]
                    print(f"  rho {rho:6.0f} {'dS  ' if desitter else 'flat'} {mode:9s} {k:10s} pooled R {Rp:+.2f} +- {np.std(bs):.2f}   continuum {Rc:+.2f}"
                          f"   offset {Rp - Rc:+.2f}   (mean of per-pair R {per.mean():+.2f}; n={len(v)})", flush=True)

def part_binscorr(seeds=400):
    """Fig. 3 of v1 (minor comment): correlation between depth bins of the drift figure, from the spread of per-sprinkling bin means
    (de Sitter, rho = 1e4, the paper's bins and pairs; s4a_desitter.run as fig_part1.fig_drift)."""
    bins = np.array([0.05, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9])
    for desitter in (True, False):
        M = []
        for s_ in range(1, seeds + 1):
            tau, r, *_ = ds.run(1e4, desitter, ETA0, DELTA, s_)
            M.append([r[(tau >= lo) & (tau < hi)].mean() if ((tau >= lo) & (tau < hi)).sum() > 5 else np.nan for lo, hi in zip(bins[:-1], bins[1:])])
        M = np.array(M); M = M[np.isfinite(M).all(1)]
        print(f"== {'de Sitter' if desitter else 'flat'}: correlation of bin means over {len(M)} sprinklings (bins {list(bins)}) ==")
        print(np.array2string(np.corrcoef(M.T), precision=2, suppress_small=True))

def part_scanpooled(seeds=1000, rho=1e4):
    """Sensitivity of the count-defined rule for the POOLED estimator (the form recommended in v2): lower cut N_C >= k, upper tau^2 <= q max."""
    print(f"== sensitivity, pooled estimator (inserted pairs, rho = {rho:.0f}, {seeds} sprinklings): k = lower cut on N_C, q = upper cut on tau^2 / max ==")
    for desitter in (True, False):
        Ks = [counts(rho, desitter, s_) for s_ in range(1, seeds + 1)]
        for kmin in (5, 20, 50):
            for q in (0.5, 0.75, 1.0):
                v = []
                for K in Ks:
                    d2 = 2 * K["nA"] * K["nB"] / (rho * (K["nC"] + 1)); t2 = (K["nA"] + K["nB"] + 2 * K["nC"]) / rho
                    d2c = 2 * K["VA"] * K["VB"] / K["VC"]; t2c = K["VA"] + K["VB"] + 2 * K["VC"]
                    base = K["nC"] >= kmin
                    if not base.any():
                        continue
                    sel = base & (t2 <= q * t2[base].max())
                    v.append(fit_ba(d2, t2, sel) + fit_ba(d2c, t2c, sel))
                v = np.array(v); v = v[np.isfinite(v).all(1)]
                Rp = -16 * v[:, 0].mean() / v[:, 1].mean(); Rc = -16 * v[:, 2].mean() / v[:, 3].mean()
                rng = np.random.default_rng(0)
                bs = [(lambda w: -16 * w[:, 0].mean() / w[:, 1].mean())(v[rng.integers(0, len(v), len(v))]) for _ in range(1000)]
                print(f"  {'dS  ' if desitter else 'flat'} k {kmin:3d} q {q:.2f}: pooled R {Rp:+.2f} +- {np.std(bs):.2f}   continuum {Rc:+.2f}   offset {Rp - Rc:+.2f}", flush=True)

def part_bdwide(seeds=100):
    """Benincasa-Dowker at larger smearing (eps = 0.003, 0.001), flat and dS, rho = 4000; flat mean = boundary/truncation check."""
    for desitter in (False, True):
        B = np.array([noise_one(4000.0, desitter, s_, (0.003, 0.001), ())[0] for s_ in range(1, seeds + 1)])
        for i, eps in enumerate((0.003, 0.001)):
            print(f"  rho 4000 {'dS  ' if desitter else 'flat'} BD eps={eps}: R_est {B[:, i].mean():+.2f} +- {B[:, i].std() / np.sqrt(seeds):.2f}  spread {B[:, i].std():.1f}", flush=True)

def part_noise(seeds=200):
    epss = (1.0, 0.1, 0.03, 0.01)
    tauDs = (0.5, 0.7)
    fd = {t: f_cont(t) for t in tauDs}
    print("== noise at equal density: single-estimate spread of R (mean +- s.e., spread) ==")
    print("  continuum dS ordering fraction: " + ", ".join(f"tau_D {t}: f = {f:.4f}" for t, f in fd.items()))
    for rho in (4000.0, 1e4):
        for desitter in (False, True):
            B, Ch, npast = [], [], []
            for s in range(1, seeds + 1):
                b, c, n_ = noise_one(rho, desitter, s, epss, tauDs); B.append(b); Ch.append(c); npast.append(n_)
            B = np.array(B); Ch = np.array(Ch)
            lab = f"  rho {rho:6.0f} {'dS  ' if desitter else 'flat'}"
            for i, eps in enumerate(epss):
                print(f"{lab} BD eps={eps:<5} R_est {B[:, i].mean():+8.2f} +- {B[:, i].std() / np.sqrt(seeds):6.2f}  spread {B[:, i].std():8.1f}"
                      f"   (past of x: {np.mean(npast):.0f} elements; effective footprint ~ 1/eps = {1 / eps:.0f})", flush=True)
            for j, t in enumerate(tauDs):
                R = 2 * (Ch[:, j, 0] - 0.5) / (fd[t] - 0.5)
                print(f"{lab} chains tau_D={t} R_est {R.mean():+8.2f} +- {R.std() / np.sqrt(seeds):6.2f}  spread {R.std():8.1f}   (N in interval {Ch[:, j, 1].mean():.0f})", flush=True)

if __name__ == "__main__":
    for w in sys.argv[1:] or ["fit", "scan", "noise"]:
        {"fit": part_fit, "scan": part_scan, "noise": part_noise, "split": part_split, "pooled": part_pooled, "binscorr": part_binscorr, "scanpooled": part_scanpooled, "bdwide": part_bdwide}[w]()
