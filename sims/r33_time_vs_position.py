"""Why does the likelihood fit improve distances (median 0.18 -> 0.11 ell at n = 3000) much more than positions (rms ~0.67 -> 0.52 ell)? (session 15)
Hypothesis: the time coordinate, which the fit takes from Johnston and never refits. Same universe as r24/r29 (seed = 1000 + i). We report
  - rms of Johnston's time error t_J - t_true (after removing the mean), in ell;
  - the fit with Johnston's t (as in the paper) and the same fit with the TRUE t (oracle), each: median |d_emb - d_true|/ell and rms position error
    after the best orthogonal map (space only), in ell.
Usage: python r33_time_vs_position.py n seed [truth]   (truth: the floor, fit started from the true positions)
"""
import sys
import numpy as np
from r11_4d_distance import load_table
from r12_johnston_compare import johnston
from r13_mixed import sprinkle
from r15_cheap_far import related_R
from r18_waist_oracle import ours_with_counts
from r19_cluster_wfit import fit_w
from r23_likelihood import setup, fit, Table
from r14_cluster_scale import spatial_dist
from r29_perpair_error import procrustes_rms

np.seterr(all="ignore")

def main(n, seed):
    W = load_table(); tab = Table(W)
    rng = np.random.default_rng(seed)
    P, C, rho = sprinkle(n, rng)
    ell = rho ** -0.25
    iu = np.triu_indices(len(P), 1)
    st = spatial_dist(P, iu)
    _, Xj = johnston(C, rho, 1.0)
    tJ = Xj[:, 0]
    dt = (tJ - tJ.mean()) - (P[:, 0] - P[:, 0].mean())
    print("n = %d seed %d: Johnston time error rms %.2f ell (median |.| %.2f ell)" % (n, seed, np.sqrt((dt ** 2).mean()) / ell, np.median(np.abs(dt)) / ell), flush=True)
    B = Xj[:, 1:] - Xj[:, 1:].mean(0); Q = P[:, 1:] - P[:, 1:].mean(0); U, _, Vt = np.linalg.svd(B.T @ Q)
    e = np.sqrt(((B @ U @ Vt - Q) ** 2).sum(1)) / ell
    nrel = (C | C.T).sum(1); lo = np.argsort(nrel)[:len(nrel) // 10]
    print("  Johnston's map, per element: median %.2f q90 %.2f q99 %.2f max %.1f ell; rms %.2f (fewest-partner 10%% %.2f, rest %.2f)" % (
          np.median(e), np.quantile(e, .9), np.quantile(e, .99), e.max(), np.sqrt((e ** 2).mean()), np.sqrt((e[lo] ** 2).mean()),
          np.sqrt((np.delete(e, lo) ** 2).mean())), flush=True)
    if len(sys.argv) > 3 and sys.argv[3] == "johnston":
        return
    for name, t in (("Johnston t", tJ), ("true t", P[:, 0])):
        R0, tj = related_R(C, rho)                                  # Johnston's related-pair separations; rebuilt below for the given t
        rel = np.isfinite(R0)
        tau2 = np.where(rel, (tj[:, None] - tj[None, :]) ** 2 - R0 ** 2, 0.0)          # recover tau^2 from his R and t
        R = np.where(rel, np.sqrt(np.abs((t[:, None] - t[None, :]) ** 2 - tau2)), np.inf); np.fill_diagonal(R, 0.0)
        I, J, s, k = ours_with_counts(C, rho, t, W)
        Xw, _ = fit_w(R, t, I, J, s, k, 100)
        S, Rl = setup(C, rho, t, W)
        S["nb"] = np.zeros_like(S["nb"]); S["nc"] = np.zeros_like(S["nc"])
        xl, _ = fit(Xw[:, 1:], t, S, Rl, rho, tab, 400)
        err = np.abs(spatial_dist(np.column_stack([t, xl]), iu) - st) / ell
        A = np.column_stack([xl, np.ones(len(xl))]); M, *_ = np.linalg.lstsq(A, P[:, 1:], rcond=None)
        aff = np.sqrt(((A @ M - P[:, 1:]) ** 2).sum(1).mean()) / ell
        print("  fit with %-10s: |dd|/ell median %.2f q90 %.2f; rms position %.2f ell (%.2f after best affine map)" % (name, np.median(err),
              np.quantile(err, 0.9), procrustes_rms(xl, P[:, 1:])[0] / ell, aff), flush=True)
        B = xl - xl.mean(0); Q = P[:, 1:] - P[:, 1:].mean(0); U, _, Vt = np.linalg.svd(B.T @ Q)
        e = np.sqrt(((B @ U @ Vt - Q) ** 2).sum(1)) / ell                  # per-element position error after the best orthogonal map
        nrel = (C | C.T).sum(1); r = np.sqrt((P[:, 1:] ** 2).sum(1)); lo = np.argsort(nrel)[:len(nrel) // 10]
        print("    per element: median %.2f q90 %.2f q99 %.2f max %.1f ell; rms over the 10%% with fewest related partners %.2f, over the rest %.2f;"
              " corr(error, |x|) %.2f" % (np.median(e), np.quantile(e, .9), np.quantile(e, .99), e.max(), np.sqrt((e[lo] ** 2).mean()),
              np.sqrt((np.delete(e, lo) ** 2).mean()), np.corrcoef(e, r)[0, 1]), flush=True)

def from_truth(n, seed):
    """Floor: the same fit (true t) started from the TRUE positions; also the share of the position error that is smooth (removed by the best
    affine map in space) -- if the floor is ~0.5 ell and mostly smooth, the position error is the likelihood's own long-wavelength noise."""
    W = load_table(); tab = Table(W)
    rng = np.random.default_rng(seed)
    P, C, rho = sprinkle(n, rng)
    ell = rho ** -0.25
    iu = np.triu_indices(len(P), 1)
    st = spatial_dist(P, iu)
    t = P[:, 0]
    S, Rl = setup(C, rho, t, W)
    S["nb"] = np.zeros_like(S["nb"]); S["nc"] = np.zeros_like(S["nc"])
    xl, _ = fit(P[:, 1:].copy(), t, S, Rl, rho, tab, 400)
    err = np.abs(spatial_dist(np.column_stack([t, xl]), iu) - st) / ell
    A = np.column_stack([xl, np.ones(len(xl))]); M, *_ = np.linalg.lstsq(A, P[:, 1:], rcond=None)
    aff = np.sqrt(((A @ M - P[:, 1:]) ** 2).sum(1).mean()) / ell
    print("  fit from TRUE positions (true t): |dd|/ell median %.2f q90 %.2f; rms position %.2f ell (%.2f after best affine map)" % (
          np.median(err), np.quantile(err, 0.9), procrustes_rms(xl, P[:, 1:])[0] / ell, aff), flush=True)

if __name__ == "__main__":
    if len(sys.argv) > 3 and sys.argv[3] == "truth":
        from_truth(int(sys.argv[1]), int(sys.argv[2])); sys.exit()
    # "johnston" as 3rd argument: only the per-element statistics of Johnston's map
    main(int(sys.argv[1]), int(sys.argv[2]))
