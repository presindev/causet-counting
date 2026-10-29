"""Count-weighted embedding at large n on the cluster (idea 005, session 12), on the SAME universes as r14 (same seed, same first rng call), paired against its
Johnston / switch numbers. python 3.6 + numpy 1.19 compatible.
Method (r18 "ours_wsmacof"): our overlap distance for every spacelike pair; SMACOF on the spatial coordinates with weight k/(k + K0) per spacelike pair
(k = shared count on the side used), weight 1 for related pairs (his R), weight 0 where we have no estimate. Start: classical MDS of the ours map, pairs
without an estimate filled with the median (no min-plus anywhere). K0 = 30 was fixed before any test (r18, seeds 2028/2029); 10, 100, 300 are the neighbours (laptop on r14 seed 1001: 100 > 30 > 10).
Usage: python r19_cluster_wfit.py n seed out.npz     |     python r19_cluster_wfit.py analyse <r14 folder> <r19 folder>
"""
import sys
import glob
import time
import numpy as np
from r11_4d_distance import load_table
from r12_johnston_compare import mink
from r13_mixed import embed_from_r, sprinkle
from r15_cheap_far import related_R
from r16_local_fit import smacof
from r18_waist_oracle import ours_with_counts
from r14_cluster_scale import spatial_dist

np.seterr(all="ignore")
K0S = (30, 10, 100, 300)

def fit_w(R, t, I, J, s, k, K0, iters=300):
    have = np.isfinite(s)
    fill = np.where(have, s, np.median(s[have]))
    D = np.where(np.isfinite(R), R, 0.0)
    D[I, J] = fill; D[J, I] = fill
    X0 = embed_from_r(D, t)
    Wt = np.isfinite(R).astype(float); np.fill_diagonal(Wt, 0.0)
    w = np.where(have, k / (k + float(K0)), 0.0)
    Wt[I, J] = w; Wt[J, I] = w
    Y, it = smacof(X0[:, 1:].copy(), D, Wt, iters)
    return np.column_stack([t, Y]), it

def main(n, seed, out):
    W = load_table()
    rng = np.random.default_rng(seed)
    P, C, rho = sprinkle(n, rng)                                 # identical to r14 (first use of the rng)
    print("n = %d (Poisson %d), seed %d" % (n, len(P), seed), flush=True)
    T = {}
    t0 = time.time(); R, t = related_R(C, rho); T["related"] = time.time() - t0
    t0 = time.time(); I, J, s, k = ours_with_counts(C, rho, t, W); T["ours_step"] = time.time() - t0
    del C
    iu = np.triu_indices(len(P), 1)
    st, mt = spatial_dist(P, iu), mink(P)[iu]
    names, a, b = [], [], []
    for K0 in K0S:
        t0 = time.time()
        X, it = fit_w(R, t, I, J, s, k, K0)
        T["fit_K%d" % K0] = time.time() - t0
        names.append("w_K%d" % K0); a.append(np.corrcoef(spatial_dist(X, iu), st)[0, 1]); b.append(np.corrcoef(mink(X)[iu], mt)[0, 1])
        print("  %-6s spatial corr %.4f   Minkowski corr %.4f   (%d iterations, %.0f s)" % (names[-1], a[-1], b[-1], it, T["fit_K%d" % K0]), flush=True)
        np.savez(out, n=n, npts=len(P), seed=seed, names=np.array(names), spatial=np.array(a), minkowski=np.array(b),
                 timing_keys=np.array(list(T)), timing=np.array(list(T.values())))   # partial result after each variant (lesson 22)
    print("  timing (s): " + ", ".join("%s %.0f" % kv for kv in T.items()), flush=True)

def analyse(d14, d19):
    r14 = {(int(z["n"]), int(z["seed"])): z for z in (np.load(f) for f in glob.glob(d14 + "/r14_n*_s*.npz"))}
    r19 = {(int(z["n"]), int(z["seed"])): z for z in (np.load(f) for f in glob.glob(d19 + "/r19_n*_s*.npz"))}
    for n in sorted({kk[0] for kk in r19}):
        keys = sorted(kk for kk in r19 if kk[0] == n and kk in r14)
        if not keys:
            print("n = %d: no matching r14 universes yet" % n); continue
        bad = [kk for kk in keys if int(r14[kk]["npts"]) != int(r19[kk]["npts"])]
        print("n = %d (%d paired universes%s)" % (n, len(keys), "; MISMATCHED UNIVERSES %s" % bad if bad else ""))
        j = np.array([r14[kk]["spatial"][list(r14[kk]["names"]).index("johnston")] for kk in keys])
        rows = [("switch0.25", np.array([r14[kk]["spatial"][list(r14[kk]["names"]).index("switch0.25")] for kk in keys]))]
        for K0 in K0S:
            nm = "w_K%d" % K0
            if all(nm in list(r19[kk]["names"]) for kk in keys):
                rows.append((nm, np.array([r19[kk]["spatial"][list(r19[kk]["names"]).index(nm)] for kk in keys])))
        print("  johnston     spatial %.4f" % j.mean())
        for nm, v in rows:
            d = v - j
            print("  %-12s spatial %.4f   vs johnston %+.4f +- %.4f   (%.0f %% of his residual)" % (nm, v.mean(), d.mean(),
                  d.std(ddof=1) / np.sqrt(len(d)) if len(d) > 1 else np.nan, 100 * d.mean() / (1 - j.mean())))
        tk = [dict(zip(r19[kk]["timing_keys"], r19[kk]["timing"])) for kk in keys]
        his = dict(zip(r14[keys[0]]["timing_keys"], r14[keys[0]]["timing"]))["johnston"]
        print("  time: fit K30 %.0f s + our step %.0f s vs his johnston() %.0f s (one universe)" % (
            np.mean([x["fit_K30"] for x in tk]), np.mean([x["ours_step"] for x in tk]), his))

if __name__ == "__main__":
    if sys.argv[1] == "analyse":
        analyse(sys.argv[2], sys.argv[3])
    else:
        main(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
