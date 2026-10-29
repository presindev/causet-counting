"""Per-pair spatial-distance error in discreteness lengths, Johnston 2025 vs the likelihood fit (idea 005, session 15; PRD review item 2).
Same pipeline and universes as r14 + r24 (seed = 1000 + i, sprinkle is the rng's first use; the paper uses the Table II seeds:
n = 3000 s1001-1002, n = 6000 s1001-1004, output in out/r29_tableII/; out/r29/ holds the first run on s1000-1002): Johnston's map, then weighted start K0 = 100, then the
related-pair likelihood (400 iterations, binomial term off). For every pair: |d_emb - d_true| / ell, ell = rho^(-1/4); quantiles over all pairs, over
spacelike pairs, and over close spacelike pairs (true d < 0.2). Also the rms position error after removing the best orthogonal map (Procrustes, space only, reflections allowed; session-15 fix:
the first version allowed rotations only and charged a mirrored map ~4 ell).
Usage: python r29_perpair_error.py n seed out.npz    |    python r29_perpair_error.py analyse <files...>
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
from r23_likelihood import setup, fit, Table
from r14_cluster_scale import spatial_dist

np.seterr(all="ignore")
QS = (0.5, 0.9, 0.99)

def procrustes_rms(X, P, scale=False):
    """rms position error after the best orthogonal map (reflections allowed: a mirror map has the same distances); with scale=True also
    the best global scale factor s (returned), to see whether a uniform scale error dominates the position error."""
    A = X - X.mean(0); B = P - P.mean(0)
    U, S, Vt = np.linalg.svd(A.T @ B)
    s = S.sum() / (A ** 2).sum() if scale else 1.0
    return np.sqrt(((s * A @ U @ Vt - B) ** 2).sum(1).mean()), s

def main(n, seed, out):
    W = load_table(); tab = Table(W)
    rng = np.random.default_rng(seed)
    P, C, rho = sprinkle(n, rng)
    ell = rho ** -0.25
    iu = np.triu_indices(len(P), 1)
    st = spatial_dist(P, iu)
    rel = (C | C.T)[iu]
    t0 = time.time(); _, Xj = johnston(C, rho, 1.0); print("johnston %.0f s" % (time.time() - t0), flush=True)
    t0 = time.time(); R, t = related_R(C, rho); I, J, s, k = ours_with_counts(C, rho, t, W)
    Xw, _ = fit_w(R, t, I, J, s, k, 100); del R, I, J, s, k
    S, Rl = setup(C, rho, t, W); del C
    S["nb"] = np.zeros_like(S["nb"]); S["nc"] = np.zeros_like(S["nc"])          # related-pair term only
    xl, _ = fit(Xw[:, 1:], t, S, Rl, rho, tab, 400); Xl = np.column_stack([t, xl])
    print("start + fit %.0f s" % (time.time() - t0), flush=True)
    res = {}
    for name, X in (("johnston", Xj), ("likelihood", Xl)):
        err = np.abs(spatial_dist(X, iu) - st) / ell
        res[name] = dict(all=np.quantile(err, QS), spacelike=np.quantile(err[~rel], QS), close=np.quantile(err[~rel & (st < 0.2)], QS),
                         rms_pos=procrustes_rms(X[:, 1:], P[:, 1:])[0] / ell,
                         rms_pos_scaled=procrustes_rms(X[:, 1:], P[:, 1:], True)[0] / ell, scale=procrustes_rms(X[:, 1:], P[:, 1:], True)[1], corr=np.corrcoef(spatial_dist(X, iu), st)[0, 1])
        print("%-10s corr %.4f  |dd|/ell q50/q90/q99 all %s  spacelike %s  close %s  rms pos %.2f ell (%.2f after scale %.3f)" % (name, res[name]["corr"],
              np.round(res[name]["all"], 2), np.round(res[name]["spacelike"], 2), np.round(res[name]["close"], 2), res[name]["rms_pos"], res[name]["rms_pos_scaled"], res[name]["scale"]), flush=True)
    np.savez(out, n=n, seed=seed, ell=ell, diam_over_ell=1 / ell,
             **{"%s_%s" % (m, k_): v for m, r in res.items() for k_, v in r.items()})

def analyse(files):
    Z = [np.load(f) for f in files]
    print("%d universes, n = %s, ell = %.4f (diamond height = %.1f ell)" % (len(Z), sorted({int(z["n"]) for z in Z}), Z[0]["ell"], Z[0]["diam_over_ell"]))
    for m in ("johnston", "likelihood"):
        for k_ in ("all", "spacelike", "close"):
            v = np.array([z["%s_%s" % (m, k_)] for z in Z])
            print("  %-10s %-9s |dd|/ell  q50 %.2f  q90 %.2f  q99 %.2f" % ((m, k_) + tuple(v.mean(0))))
        sc = [z[m + "_scale"] for z in Z if m + "_scale" in z]
        print("  %-10s rms position error %.2f ell%s, corr %.4f" % (m, np.mean([z[m + "_rms_pos"] for z in Z]),
              " (%.2f after best global scale %.3f)" % (np.mean([z[m + "_rms_pos_scaled"] for z in Z]), np.mean(sc)) if sc else "",
              np.mean([z[m + "_corr"] for z in Z])))

if __name__ == "__main__":
    if sys.argv[1] == "analyse":
        analyse(sys.argv[2:])
    else:
        main(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
