"""Depth-drift curvature estimator: external referee round 2 on the 1+1 paper (session 18; toolkit-1p1-v2, new comments 8, 9, 10 and minor 14).
Same estimator as r37 (pooled, count-defined window: every c with N_C >= 20, down to the deepest usable c), d2 = 2 N_A N_B / (rho (N_C + 1)),
tau^2 = (N_I(c,a) + N_I(c,b)) / rho, R = -16 sum(beta) / sum(alpha) over pairs; R_cont = the same on the exact continuum volumes of the same c's.
Counts are computed for many pairs of one sprinkling at once (row-chunked causal matrix, so flat regions of 4e4 elements fit in memory).

M8  'select' : the sprinkled-pair shortfall. Box region of r37 (eta in [-3, -1], |x| <= 1; c used only if its rectangle is inside the box, from
               the coordinates, as in v2), a, b near eta0 = -1.05, x = -+0.075. Pair selections, on the same seeds 1..1000 as r37:
                 inserted : a, b added by hand at the target points (v2; reproduces r37);
                 nearest  : the sprinkled elements nearest (Euclidean in eta, x) to the target points (v2; reproduces r37);
                 uniform1 : one element drawn uniformly from the elements in a square window of half-size W around each target point;
                 allpairs : every spacelike pair (a in window A, b in window B), each kept with a fixed probability q (independent of the
                            configuration), all pooled. By the Mecke formula sums over all pairs of a Poisson process are exact averages over
                            pairs placed at fixed points, so this is the unbiased way to use sprinkled pairs. (uniform1 weights each
                            configuration by 1 / N_window, which removes about one element from the window: a small Palm bias of its own.)
               Diagnostic: mean of N_A - rho V_A, N_B - rho V_B, N_C - rho V_C per depth bin (the referee's hypothesis: a deficit at the
               shallow ends of the strips for nearest-element selection).
M14 'convex' : the same in a causally convex region, the past of an element f = (eta_f, 0) cut at eta = -3. There the rectangle from c to the
               join of a, b lies in I(c, f) and thus in the region for every c in the common past: the window is set by the order alone.
M9  'frw'    : FRW a = eta (p = 1), R = -2 / eta^4, a, b inserted at eta0 = 1.5, 0.14 apart (r9). Region: past of f = (1.55, 0) cut at
               eta_lo = 0.75 (convex). Windows ending at eta_c >= 1.1, 0.92, 0.75. Pooled estimate, continuum fit on the same c's, and the
               prediction of Eq. (12): the same fit applied to 1 - tau^2/16 [R0 - (tau/3) dR/dtau] with tau^2 from the exact volumes.
M10 'noise'  : one de Sitter causal diamond (interval) u, v in [-3, -0.95], P pairs inside it (a uniform among the elements with
               eta in [-1.25, -1.05], |x| <= 0.1; b uniform among the elements spacelike to a with x_b - x_a in [0.1, 0.2], |eta_b - eta_a| <= 0.05),
               pooled over the first P = 10, 30, 100, 300 pairs; error = spread between sprinklings. Same diamond: ordering fraction
               f = (related pairs) / binom(N, 2), R_chain = 2 (f - 1/2) / (f_cont - 1/2), f_cont from the exact continuum diamond (Monte Carlo).
Usage: python r40_curvature_round2.py select|convex|frw|noise [workers]   (writes runs/r40/<part>.npz and prints the summary)
"""
import os
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1"); os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import sys
import time
import numpy as np
from multiprocessing import Pool
import s4a_desitter as ds
from r9_drift_fit_frw import vol as frw_vol

np.seterr(all="ignore")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "runs", "r40")
ETA0, DELTA, WIN = -1.05, 0.15, 0.025
KMIN = 20
TBINS = np.array([0.0, 0.02, 0.05, 0.1, 0.2, 0.35, 0.5, 0.75, 1.0, 1.5, 9.0])          # bins of tau^2 (continuum) for the depletion diagnostic

# ---------------- geometry ----------------
def density(eta, geom):
    return {"dS": 1 / eta ** 2, "flat": np.ones_like(eta), "frw": eta ** 2}[geom]

def volume(u1, u2, v1, v2, geom):
    if geom == "dS":
        return ds.rect_volume(u1, u2, v1, v2)
    if geom == "flat":
        return 0.5 * (u2 - u1) * (v2 - v1)
    return frw_vol(u1, u2, v1, v2, 1.0)

def sprinkle_region(rho, geom, region, rng, eta_lo, eta_hi, xmax):
    """Poisson sprinkling of density rho * density(eta) in a region given by (eta_lo, eta_hi, xmax) and an optional shape test."""
    if region == "box" and geom in ("dS", "flat"):
        return ds.sprinkle(rho, geom == "dS", rng)                                     # identical to r37 (seed-for-seed)
    dmax = max(density(np.array([eta_lo]), geom)[0], density(np.array([eta_hi]), geom)[0])
    n = rng.poisson(rho * dmax * (eta_hi - eta_lo) * 2 * xmax)
    eta = eta_lo + (eta_hi - eta_lo) * rng.random(n); x = xmax * (2 * rng.random(n) - 1)
    keep = rng.random(n) < density(eta, geom) / dmax
    eta, x = eta[keep], x[keep]
    if region == "cone":                                                               # past of f = (eta_hi, 0)
        m = np.abs(x) < eta_hi - eta
    elif region == "diamond":                                                          # u, v in [eta_lo, eta_hi]
        u, v = eta - x, eta + x
        m = (u > eta_lo) & (v > eta_lo) & (u < eta_hi) & (v < eta_hi)
    else:
        m = np.ones(len(eta), bool)
    return eta[m], x[m]

# ---------------- counts for many pairs at once ----------------
def multi_counts(u, v, pairs, geom, rho, box=False, chunk=2048):
    """For each pair (a, b) (indices, spacelike): arrays over its usable c's (N_C > 0, and rectangle inside the box if box)."""
    E = np.unique(np.array(pairs).ravel())
    toE = (u[None, :] < u[E][:, None]) & (v[None, :] < v[E][:, None])                  # (|E|, n): z in the past of endpoint e
    S = np.flatnonzero(toE.any(0))
    uu, vv = u[S], v[S]
    col = {e: i for i, e in enumerate(E)}
    TE = toE[:, S].T                                                                   # (|S|, |E|)
    TAB = np.column_stack([TE[:, col[a]] & TE[:, col[b]] for a, b in pairs])          # (|S|, P)
    rhs = np.column_stack([TE, TAB]).astype(np.float32)
    M = np.empty((len(S), rhs.shape[1]), np.float32)
    for i in range(0, len(S), chunk):                                                  # M[c] = sum_z [c < z] rhs[z]
        Cs = (uu[i:i + chunk, None] < uu[None, :]) & (vv[i:i + chunk, None] < vv[None, :])
        M[i:i + chunk] = Cs.astype(np.float32) @ rhs
    out = []
    for p, (a, b) in enumerate(pairs):
        if u[a] > u[b]:
            a, b = b, a                                                                # u_a < u_b, v_a > v_b
        cs = np.flatnonzero(TAB[:, p])
        nIa, nIb, nC = M[cs, col[a]], M[cs, col[b]], M[cs, len(E) + p]
        ok = nC > 0
        if box:
            uj, vj = u[b], v[a]
            ok &= ds.inside((uu[cs] + vj) / 2, (vj - uu[cs]) / 2) & ds.inside((uj + vv[cs]) / 2, (vv[cs] - uj) / 2)
        cs, nIa, nIb, nC = cs[ok], nIa[ok], nIb[ok], nC[ok]
        uc, vc = uu[cs], vv[cs]
        out.append(dict(nA=nIa - nC, nB=nIb - nC, nC=nC, VA=volume(uc, u[a], v[b], v[a], geom), VB=volume(u[a], u[b], vc, v[b], geom),
                        VC=volume(uc, u[a], vc, v[b], geom), eta_c=(uc + vc) / 2, ua=u[a], va=v[a], ub=u[b], vb=v[b]))
    return out

def fit_ba(y, t2, sel):
    if sel.sum() < 10:
        return np.nan, np.nan
    return tuple(np.polyfit(t2[sel], y[sel], 1))                                       # (beta, alpha)

def analyse_pair(K, rho, extra_sel=None, pred=None):
    """(beta, alpha, beta_cont, alpha_cont[, beta_pred, alpha_pred]) for the count-defined window, plus depletion sums per tau^2 bin."""
    d2 = 2 * K["nA"] * K["nB"] / (rho * (K["nC"] + 1)); t2 = (K["nA"] + K["nB"] + 2 * K["nC"]) / rho
    d2c = 2 * K["VA"] * K["VB"] / K["VC"]; t2c = K["VA"] + K["VB"] + 2 * K["VC"]
    sel = K["nC"] >= KMIN
    if extra_sel is not None:
        sel &= extra_sel(K)
    res = fit_ba(d2, t2, sel) + fit_ba(d2c, t2c, sel)
    if pred is not None:
        res += fit_ba(pred(K, t2c), t2c, sel)                    # Eq. (12) curve on the same c's
    b = np.clip(np.digitize(t2c, TBINS) - 1, 0, len(TBINS) - 2)
    dep = np.zeros((3, len(TBINS) - 1)); cnt = np.zeros(len(TBINS) - 1)
    for j, (n_, V) in enumerate((("nA", "VA"), ("nB", "VB"), ("nC", "VC"))):
        dep[j] = np.bincount(b[sel], (K[n_] - rho * K[V])[sel], len(TBINS) - 1)
    cnt[:] = np.bincount(b[sel], None, len(TBINS) - 1)
    return np.array(res), dep, cnt

# ---------------- pair selections ----------------
def window(eta, x, cx):
    return np.flatnonzero((np.abs(eta - ETA0) < WIN) & (np.abs(x - cx) < WIN))

def spacelike(u, v, a, b):
    return (u[a] - u[b]) * (v[a] - v[b]) < 0

def task_select(args):
    """One sprinkling, M8 / M14: all selections. region 'box' (coordinate corner test) or 'cone' (convex, past of (-0.95, 0) cut at -3)."""
    seed, rho, geom, region = args
    rng = np.random.default_rng(seed)
    if region == "box":
        eta, x = sprinkle_region(rho, geom, "box", rng, -3.0, -1.0, 1.0)
    else:
        eta, x = sprinkle_region(rho, geom, "cone", rng, -3.0, -0.95, 2.05)
    box = region == "box"
    out = {}
    # inserted (own copy of the set)
    e2, x2 = np.append(eta, [ETA0, ETA0]), np.append(x, [-DELTA / 2, DELTA / 2])
    u2, v2 = e2 - x2, e2 + x2
    K = multi_counts(u2, v2, [(len(e2) - 2, len(e2) - 1)], geom, rho, box)[0]
    out["inserted"] = [analyse_pair(K, rho)]
    u, v = eta - x, eta + x
    sel_rng = np.random.default_rng(10 ** 6 + seed)                                    # selection randomness, independent of the sprinkling
    pairs = {}
    a = np.argmin((eta - ETA0) ** 2 + (x + DELTA / 2) ** 2); b = np.argmin((eta - ETA0) ** 2 + (x - DELTA / 2) ** 2)
    pairs["nearest"] = [(a, b)] if spacelike(u, v, a, b) else []
    WA, WB = window(eta, x, -DELTA / 2), window(eta, x, DELTA / 2)
    if len(WA) and len(WB):
        a, b = sel_rng.choice(WA), sel_rng.choice(WB)
        pairs["uniform1"] = [(a, b)] if spacelike(u, v, a, b) else []
    else:
        pairs["uniform1"] = []
    lam = rho * float(density(np.array([ETA0]), geom)[0]) * (2 * WIN) ** 2             # expected elements per window (fixed, not data-dependent)
    q = min(1.0, 20.0 / lam ** 2)
    allp = [(a, b) for a in WA for b in WB if spacelike(u, v, a, b) and sel_rng.random() < q]
    pairs["allpairs"] = allp
    flat = [p for k in ("nearest", "uniform1", "allpairs") for p in pairs[k]]
    Ks = multi_counts(u, v, flat, geom, rho, box) if flat else []
    i = 0
    for k in ("nearest", "uniform1", "allpairs"):
        out[k] = [analyse_pair(Ks[i + j], rho) for j in range(len(pairs[k]))]
        i += len(pairs[k])
    return seed, out

def summarize_select(results, label):
    print(f"== {label} ==")
    modes = ("inserted", "nearest", "uniform1", "allpairs")
    for mode in modes:
        rows, seeds, dep, cnt = [], [], 0, 0
        for seed, out in results:
            for r, d, c in out[mode]:
                if np.isfinite(r).all():
                    rows.append(r); seeds.append(seed); dep = dep + d; cnt = cnt + c
        if not rows:
            continue
        v = np.array(rows); seeds = np.array(seeds)
        Rp = -16 * v[:, 0].sum() / v[:, 1].sum(); Rc = -16 * v[:, 2].sum() / v[:, 3].sum()
        us = np.unique(seeds); grp = [np.flatnonzero(seeds == s) for s in us]
        rng = np.random.default_rng(0); bs, bd = [], []
        for _ in range(1000):                                                          # cluster bootstrap over sprinklings
            idx = np.concatenate([grp[k] for k in rng.integers(0, len(grp), len(grp))])
            w = v[idx]; bs.append(-16 * w[:, 0].sum() / w[:, 1].sum()); bd.append(bs[-1] + 16 * w[:, 2].sum() / w[:, 3].sum())
        per = -16 * v[:, 0] / v[:, 1]
        dpb = dep / np.maximum(cnt, 1)
        print(f"  {mode:9s} pairs {len(v):6d} in {len(us):4d} sprinklings: pooled R {Rp:+.3f} +- {np.std(bs):.3f}   continuum {Rc:+.3f}"
              f"   offset {Rp - Rc:+.3f} +- {np.std(bd):.3f}   (single-pair s.d. {per.std():.2f})")
        print("            N - rho V per tau^2 bin " + " ".join(f"[{TBINS[j]:.2f},{TBINS[j + 1]:.2f})" for j in range(len(TBINS) - 1) if cnt[j] > 0))
        for j, nm in enumerate(("A", "B", "C")):
            print(f"              {nm}: " + " ".join(f"{dpb[j, k]:+7.3f}" for k in range(len(TBINS) - 1) if cnt[k] > 0))
    sys.stdout.flush()

def run_select(region, workers, seeds=1000):
    os.makedirs(OUT, exist_ok=True)
    cfgs = [(4000.0, "dS"), (1e4, "dS"), (4000.0, "flat"), (1e4, "flat")]
    allres = {}
    for rho, geom in cfgs:
        t0 = time.time()
        with Pool(workers) as pool:
            res = pool.map(task_select, [(s, rho, geom, region) for s in range(1, seeds + 1)], chunksize=4)
        allres[f"{geom}_{int(rho)}"] = res
        summarize_select(res, f"{region}: {geom}, rho = {rho:.0f}, {seeds} sprinklings ({time.time() - t0:.0f} s)")
        np.save(os.path.join(OUT, f"{region}.npy"), np.array([allres], dtype=object), allow_pickle=True)

# ---------------- M9: FRW p = 1 ----------------
P_ETA0, P_ETAF, P_LO = 1.5, 1.55, 0.75
WINDOWS = (1.1, 0.92, 0.75)

def R_frw(eta):
    return -2 / eta ** 4

def task_frw(args):
    seed, rho = args
    rng = np.random.default_rng(seed)
    eta, x = sprinkle_region(rho, "frw", "cone", rng, P_LO, P_ETAF, P_ETAF - P_LO)
    h = 0.14 / (2 * P_ETA0)
    eta, x = np.append(eta, [P_ETA0, P_ETA0]), np.append(x, [-h, h])
    u, v = eta - x, eta + x
    K = multi_counts(u, v, [(len(eta) - 2, len(eta) - 1)], "frw", rho)[0]
    R0, dR = R_frw(P_ETA0), 8 / P_ETA0 ** 6                                           # dR/dtau toward the future at a, b (dtau = a deta)
    pred = lambda K_, t2c: (2 * h * P_ETA0) ** 2 * (1 - t2c / 16 * (R0 - np.sqrt(t2c) / 3 * dR))
    out = []
    for lo in WINDOWS:
        r, _, _ = analyse_pair(K, rho, extra_sel=lambda K_: K_["eta_c"] >= lo, pred=pred)
        out.append(r)
    return seed, np.array(out)

def run_frw(workers, seeds=1000, rho=1e4):
    os.makedirs(OUT, exist_ok=True)
    t0 = time.time()
    with Pool(workers) as pool:
        res = pool.map(task_frw, [(s, rho) for s in range(1, seeds + 1)], chunksize=4)
    V = np.array([r for _, r in res])                                                  # (seeds, windows, 6)
    np.save(os.path.join(OUT, "frw.npy"), V)
    h = 0.14 / (2 * P_ETA0)
    print(f"== FRW p = 1, rho = {rho:.0f}, a, b inserted at eta0 = {P_ETA0} ({0.14 * np.sqrt(rho):.0f} ell apart), {seeds} sprinklings ({time.time() - t0:.0f} s) ==")
    tau_of = lambda e: (P_ETA0 ** 2 - e ** 2) / 2
    for i, lo in enumerate(WINDOWS):
        v = V[:, i]; v = v[np.isfinite(v).all(1)]
        Rp = -16 * v[:, 0].sum() / v[:, 1].sum(); Rc = -16 * v[:, 2].sum() / v[:, 3].sum(); Rq = -16 * v[:, 4].sum() / v[:, 5].sum()
        rng = np.random.default_rng(0)
        bs = [(lambda w: -16 * w[:, 0].sum() / w[:, 1].sum())(v[rng.integers(0, len(v), len(v))]) for _ in range(2000)]
        print(f"  window down to eta_c >= {lo:.2f} (tau <= {tau_of(lo):.2f}; R from {R_frw(P_ETA0):+.2f} at a,b to {R_frw(lo):+.2f};"
              f" R at a third of the depth {R_frw(np.sqrt(P_ETA0 ** 2 - 2 * tau_of(lo) / 3)):+.2f}): pooled R {Rp:+.3f} +- {np.std(bs):.3f}"
              f"   continuum fit {Rc:+.3f}   Eq. (12) {Rq:+.3f}   (mean of single-pair R {np.mean(-16 * v[:, 0] / v[:, 1]):+.2f}; n={len(v)})")

# ---------------- M10: noise in realistic use ----------------
D_LO, D_HI = -3.0, -0.95
PS = (10, 30, 100, 300)

def f_cont_diamond(geom, pairs=40_000_000, seed=7):
    """Ordering fraction of the continuum diamond u, v in [D_LO, D_HI] with the geometry's density (Monte Carlo, chunked)."""
    rng = np.random.default_rng(seed)
    hits = tot = 0
    while tot < pairs:
        m = 4_000_000
        uu = D_LO + (D_HI - D_LO) * rng.random((2, m)); vv = D_LO + (D_HI - D_LO) * rng.random((2, m))
        w = density((uu + vv) / 2, geom) / max(density(np.array([D_LO]), geom)[0], density(np.array([D_HI]), geom)[0])
        k = (rng.random((2, m)) < w).all(0)
        a_u, b_u, a_v, b_v = uu[0, k], uu[1, k], vv[0, k], vv[1, k]
        hits += np.sum(((a_u < b_u) & (a_v < b_v)) | ((a_u > b_u) & (a_v > b_v))); tot += k.sum()
    return hits / tot

def task_noise(args):
    seed, rho, geom = args
    rng = np.random.default_rng(seed)
    eta, x = sprinkle_region(rho, geom, "diamond", rng, D_LO, D_HI, D_HI - D_LO)
    u, v = eta - x, eta + x
    sel = np.random.default_rng(10 ** 6 + seed)
    cand = np.flatnonzero((eta > -1.25) & (eta < -1.05) & (np.abs(x) <= 0.1))
    pairs = []
    while len(pairs) < max(PS):
        a = sel.choice(cand)
        cb = np.flatnonzero((x - x[a] >= 0.1) & (x - x[a] <= 0.2) & (np.abs(eta - eta[a]) <= 0.05))
        cb = cb[(u[cb] - u[a]) * (v[cb] - v[a]) < 0]
        if len(cb):
            pairs.append((a, sel.choice(cb)))
    Ks = multi_counts(u, v, pairs, geom, rho)
    R = np.array([analyse_pair(K, rho)[0] for K in Ks])                               # (P, 4)
    N = len(u); rel = 0
    for i in range(0, N, 2048):
        rel += ((u[i:i + 2048, None] < u[None, :]) & (v[i:i + 2048, None] < v[None, :])).sum()
    return seed, R, rel / (N * (N - 1) / 2), N

def run_noise(workers, seeds=200):
    os.makedirs(OUT, exist_ok=True)
    for geom, rhos in (("dS", (4000.0, 1e4)), ("flat", (4000.0,))):
        fc = f_cont_diamond("dS")
        for rho in rhos:
            t0 = time.time()
            with Pool(workers) as pool:
                res = pool.map(task_noise, [(s, rho, geom) for s in range(1, seeds + 1)], chunksize=2)
            np.save(os.path.join(OUT, f"noise_{geom}_{int(rho)}.npy"), np.array(res, dtype=object), allow_pickle=True)
            f = np.array([r[2] for r in res]); Nn = np.mean([r[3] for r in res])
            Rch = 2 * (f - 0.5) / (fc - 0.5)
            print(f"== noise, {geom} diamond u, v in [{D_LO}, {D_HI}], rho = {rho:.0f} ({Nn:.0f} elements), {seeds} sprinklings ({time.time() - t0:.0f} s);"
                  f" continuum dS ordering fraction {fc:.5f} ==")
            print(f"  ordering fraction (whole diamond): R {Rch.mean():+.3f}, s.d. between sprinklings {Rch.std():.3f}")
            for P in PS:
                Rp, Rc = [], []
                for _, R, _, _ in res:
                    w = R[:P]; w = w[np.isfinite(w).all(1)]
                    Rp.append(-16 * w[:, 0].sum() / w[:, 1].sum()); Rc.append(-16 * w[:, 2].sum() / w[:, 3].sum())
                Rp, Rc = np.array(Rp), np.array(Rc)
                print(f"  depth drift, P = {P:3d} pairs: R {Rp.mean():+.3f}, s.d. between sprinklings {Rp.std():.3f}   (continuum fit of the same c's {Rc.mean():+.3f};"
                      f" rms about it {np.sqrt(((Rp - Rc) ** 2).mean()):.3f})")
            sys.stdout.flush()

if __name__ == "__main__":
    part = sys.argv[1]
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    if part in ("select", "convex"):
        run_select("box" if part == "select" else "cone", workers, *(int(s) for s in sys.argv[3:4]))
    elif part == "frw":
        run_frw(workers, *(int(s) for s in sys.argv[3:4]))
    elif part == "noise":
        run_noise(workers, *(int(s) for s in sys.argv[3:4]))
