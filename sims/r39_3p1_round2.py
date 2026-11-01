"""External referee round 2 on the 3+1 paper (session 18): new comment 7 (is the residual a flat valley or nearly degenerate separate maxima?),
minor 10 (error-location numbers on the Fig. 2 set) and minor 12 (cost of the near-cone variant). Laptop, on the existing r35 outputs.
Universes are rebuilt from their seeds (sprinkle is the rng's first use, as in r35), so the order is exact (the npz holds float32 positions).
Per universe (n = 3000 and 6000, seeds 1001-1010):
  lnl    : the paper's Gaussian lnL (Eq. 5, all related pairs, Johnston's t) recomputed at the saved maps fit_lbfgs (converged intrinsic fit),
           jstart, pstart (the other converged starts) and truth (converged truth-started fit); sign of truth - fit_lbfgs.
  align  : truth map rotated onto fit_lbfgs by the best orthogonal 3x3 matrix about the time axis (no translation: the tips are pinned at x = 0;
           reflections allowed, lnL is invariant under O(3)); rms displacement between the two maps in units of ell, before and after.
  path   : lnL along x(s) = (1 - s) X_fit + s Q X_truth, s in [-0.25, 1.25]; barrier = max over s in [0, 1] of the straight line between the end
           values minus lnL(s); C(s) = spatial correlation with the truth along the path.
  relax  : L-BFGS (r35's, to convergence) started from x(s) at s = 0.25, 0.5, 0.75: which map does each point fall back to (C, lnL, rms distance
           to each end)? If it stays where it starts with an lnL within O(1) of both ends, the ends are joined by a valley that the straight line
           cuts across; if it returns to an end, they are separate maxima.
  extend : L-BFGS continued from fit_lbfgs without a stopping tolerance, 4 x 500 iterations: lnL gain and C after each block.
  errloc : rms position error per element (best orthogonal map with translation, as Fig. 2) for johnston, fit and fit_lbfgs: all elements,
           the tenth with the fewest related partners, the other nine tenths, and the waist t in [0.4, 0.6].
Usage: python r39_3p1_round2.py <r35 folder> <n> <out.npz> [seeds...]   |   python r39_3p1_round2.py near <n> [seed]   (near-cone share and cost per iteration)
"""
import sys
import glob
import time
import numpy as np
from r13_mixed import sprinkle
from r14_cluster_scale import spatial_dist
from r35_referee1_3p1 import gauss, lbfgs

np.seterr(all="ignore")
C4 = np.pi / 24
S_GRID = np.round(np.linspace(-0.25, 1.25, 31), 3)

def setup_rel(C, rho):
    """Related-pair data of r23.setup (only the part Eq. 5 uses)."""
    Cf = C.astype(np.float32)
    N = Cf @ Cf
    A, B = np.nonzero(np.triu(C | C.T, 1))
    Nab = np.maximum(N[A, B], N[B, A]).astype(float)
    t2 = np.sqrt((Nab + 0.5) / (rho * C4))
    return dict(A=A, B=B, t2=t2, sd=t2 / (2 * np.sqrt(Nab + 1)))

def best_orth(X, Y):
    """Orthogonal Q (det +-1) minimizing |X Q - Y| (no translation)."""
    U, _, Vt = np.linalg.svd(X.T @ Y)
    return U @ Vt

def pos_err(X, P):
    A = X - X.mean(0); B = P - P.mean(0)
    U, _, Vt = np.linalg.svd(A.T @ B)
    return np.sqrt(((A @ U @ Vt - B) ** 2).sum(1))

def one(z, out_rows):
    n, seed = int(z["n"]), int(z["seed"])
    t0 = time.time()
    P, C, rho = sprinkle(n, np.random.default_rng(seed))
    assert len(P) == int(z["npts"]) and np.allclose(P, z["P"], atol=1e-5), "universe mismatch"
    ell = rho ** -0.25
    iu = np.triu_indices(len(P), 1)
    st = spatial_dist(P, iu)
    corr = lambda x: np.corrcoef(spatial_dist(np.column_stack([np.zeros(len(x)), x]), iu), st)[0, 1]   # spatial_dist skips column 0
    names = list(z["names"])
    t = z["X_johnston"][:, 0].astype(float)
    Rl = setup_rel(C, rho)
    G = lambda x: gauss(x, Rl, t=t)
    L = lambda x: G(x)[0]
    X = {a: z["X_" + a][:, 1:].astype(float) for a in ("fit", "fit_lbfgs", "jstart", "pstart", "truth")}
    lnl = {a: L(x) for a, x in X.items()}
    rec = {a: float(z["lnl"][names.index(a)]) for a in X}
    row = dict(n=n, seed=seed, ell=ell, related=len(Rl["A"]))
    for a in X:
        row["lnl_" + a] = lnl[a]; row["lnl_rec_" + a] = rec[a]; row["C_" + a] = corr(X[a])
    X1, X2 = X["fit_lbfgs"], X["truth"]
    Q = best_orth(X2, X1)
    X2q = X2 @ Q
    row["det_Q"] = np.linalg.det(Q)
    row["rms_raw"] = np.sqrt(((X2 - X1) ** 2).sum(1).mean()) / ell
    row["rms_aligned"] = np.sqrt(((X2q - X1) ** 2).sum(1).mean()) / ell
    row["lnl_truth_aligned"] = L(X2q)
    path = np.array([L((1 - s) * X1 + s * X2q) for s in S_GRID])
    Cpath = np.array([corr((1 - s) * X1 + s * X2q) for s in S_GRID])
    row["path_lnl"] = path; row["path_C"] = Cpath
    inside = (S_GRID >= 0) & (S_GRID <= 1)
    line = path[S_GRID == 0][0] + S_GRID * (path[S_GRID == 1][0] - path[S_GRID == 0][0])
    row["barrier"] = np.max((line - path)[inside])
    for s in (0.25, 0.5, 0.75):
        x0 = (1 - s) * X1 + s * X2q
        xr, Lr, it = lbfgs(x0, G)
        row[f"relax{s}_lnl"] = Lr; row[f"relax{s}_C"] = corr(xr); row[f"relax{s}_it"] = it
        row[f"relax{s}_d1"] = np.sqrt(((xr - X1) ** 2).sum(1).mean()) / ell
        row[f"relax{s}_d2"] = np.sqrt(((xr - X2q) ** 2).sum(1).mean()) / ell
    # extend: keep optimizing the converged intrinsic fit (no stopping tolerance), 4 x 500 L-BFGS iterations; does it creep along the valley?
    x = X1.copy(); ext = []
    for _ in range(4):
        x, Lx, it = lbfgs(x, G, maxit=500, tol=0.0)
        ext.append((Lx - lnl["fit_lbfgs"], corr(x), it))
    row["ext_dlnl"] = np.array([e[0] for e in ext]); row["ext_C"] = np.array([e[1] for e in ext]); row["ext_it"] = np.array([e[2] for e in ext])
    # error location (Fig. 2 definition)
    k = (C | C.T).sum(1)
    low = np.argsort(np.argsort(k)) < 0.1 * len(k)
    waist = (P[:, 0] > 0.4) & (P[:, 0] < 0.6)
    for a in ("johnston", "fit", "fit_lbfgs"):
        e = pos_err(z["X_" + a][:, 1:].astype(float), P[:, 1:]) / ell
        row[f"err_{a}_all"] = np.sqrt((e ** 2).mean()); row[f"err_{a}_low"] = np.sqrt((e[low] ** 2).mean())
        row[f"err_{a}_rest"] = np.sqrt((e[~low] ** 2).mean()); row[f"err_{a}_waist"] = np.sqrt((e[waist] ** 2).mean())
        row[f"err_{a}_median"] = np.median(e)
    row["secs"] = time.time() - t0
    out_rows.append(row)
    print(f"n {n} seed {seed}: lnL truth - fit_lbfgs {lnl['truth'] - lnl['fit_lbfgs']:+.2f} (recorded {rec['truth'] - rec['fit_lbfgs']:+.2f});"
          f" rms(truth - fit) {row['rms_raw']:.3f} -> aligned {row['rms_aligned']:.3f} ell (det {row['det_Q']:+.0f}); barrier {row['barrier']:.1f};"
          f" path min-end {path[inside].min() - max(path[S_GRID == 0][0], path[S_GRID == 1][0]):.1f};"
          f" relax0.5: C {row['relax0.5_C']:.5f} lnL-fit {row['relax0.5_lnl'] - lnl['fit_lbfgs']:+.2f} d1 {row['relax0.5_d1']:.3f} d2 {row['relax0.5_d2']:.3f}"
          f"; extend: dlnL {row['ext_dlnl'][-1]:+.2f}, C {row['ext_C'][-1]:.5f} ({row['secs']:.0f} s)", flush=True)

def save(rows, out):
    keys = rows[0].keys()
    np.savez(out, s_grid=S_GRID, **{k: np.array([r[k] for r in rows]) for k in keys})

def near(n, seed=1001):
    """Near-cone share of related pairs and the cost of one lnL + gradient evaluation, all pairs vs near-cone (laptop, median of 5)."""
    P, C, rho = sprinkle(n, np.random.default_rng(seed))
    ell = rho ** -0.25
    t0 = time.time(); Rl = setup_rel(C, rho); ts = time.time() - t0
    near = Rl["t2"] < 6 * ell ** 2
    Rn = {k: v[near] for k, v in Rl.items()}
    x = P[:, 1:] + 0.1 * ell * np.random.default_rng(0).standard_normal(P[:, 1:].shape); t = P[:, 0]
    out = []
    for R in (Rl, Rn):
        T = []
        for _ in range(5):
            t1 = time.time(); gauss(x, R, t=t); T.append(time.time() - t1)
        out.append(np.median(T))
    print(f"n {n} (seed {seed}): related pairs {len(near)}, near-cone share {near.mean():.3f}; setup {ts:.1f} s;"
          f" one evaluation: all {out[0]:.3f} s, near {out[1]:.3f} s, ratio {out[1] / out[0]:.3f}", flush=True)

def relaxlong(folder, n, out, seeds, s=0.5):
    """Relaxation from x(s) to convergence (L-BFGS up to 3000 iterations, r35's stopping test), added after the 300-iteration cap of
    'relax' left some runs unfinished; s = 0.5 (midpoint) in session 18, s = 0.25 and 0.75 in session 19 (referee round 3, comment 16)."""
    rows = []
    for seed in seeds:
        z = np.load(f"{folder}/r35_n{n}_s{seed}.npz")
        t0 = time.time()
        P, C, rho = sprinkle(n, np.random.default_rng(seed)); ell = rho ** -0.25
        iu = np.triu_indices(len(P), 1); st = spatial_dist(P, iu)
        corr = lambda x: np.corrcoef(spatial_dist(np.column_stack([np.zeros(len(x)), x]), iu), st)[0, 1]
        t = z["X_johnston"][:, 0].astype(float); Rl = setup_rel(C, rho); G = lambda x: gauss(x, Rl, t=t)
        X1, X2 = z["X_fit_lbfgs"][:, 1:].astype(float), z["X_truth"][:, 1:].astype(float)
        X2q = X2 @ best_orth(X2, X1)
        L1, L2 = G(X1)[0], G(X2q)[0]
        x0 = (1 - s) * X1 + s * X2q
        xr, Lr, it = lbfgs(x0, G, maxit=3000)
        row = dict(seed=seed, dl_fit=Lr - L1, dl_truth=Lr - L2, it=it, C=corr(xr), C_fit=corr(X1), C_truth=corr(X2q),
                   d1=np.sqrt(((xr - X1) ** 2).sum(1).mean()) / ell, d2=np.sqrt(((xr - X2q) ** 2).sum(1).mean()) / ell,
                   d0=np.sqrt(((xr - x0) ** 2).sum(1).mean()) / ell, dl_start=Lr - G(x0)[0])
        rows.append(row)
        print(f"n {n} seed {seed}: relaxed from s = {s} lnL - fit {row['dl_fit']:+.2f}, - truth {row['dl_truth']:+.2f} ({it} it); C {row['C']:.5f}"
              f" (fit {row['C_fit']:.5f}, truth {row['C_truth']:.5f}); distance to fit {row['d1']:.2f}, to truth {row['d2']:.2f} ell; moved {row['d0']:.2f} ell from the start, lnL gain {row['dl_start']:.0f} ({time.time() - t0:.0f} s)", flush=True)
        np.savez(out, **{k: np.array([r[k] for r in rows]) for k in rows[0]})

if __name__ == "__main__":
    if sys.argv[1] == "relaxlong":
        relaxlong(sys.argv[2], int(sys.argv[3]), sys.argv[4], [int(s) for s in sys.argv[5:]] or list(range(1001, 1011)))
        sys.exit()
    if sys.argv[1] == "relaxlong_s":   # relaxlong_s <s> <folder> <n> <out.npz> [seeds...]
        relaxlong(sys.argv[3], int(sys.argv[4]), sys.argv[5], [int(x) for x in sys.argv[6:]] or list(range(1001, 1011)), s=float(sys.argv[2]))
        sys.exit()
    if sys.argv[1] == "near":
        near(int(sys.argv[2]), *(int(s) for s in sys.argv[3:]))
        sys.exit()
    folder, n, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    seeds = [int(s) for s in sys.argv[4:]] or list(range(1001, 1011))
    rows = []
    for s in seeds:
        z = np.load(f"{folder}/r35_n{n}_s{s}.npz")
        one(z, rows)
        save(rows, out)
