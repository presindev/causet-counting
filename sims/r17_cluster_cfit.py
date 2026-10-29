"""(c) counts-only map at large n on the cluster (idea 005, session 11), on the SAME universes as r14 (same seed, same first rng call), so it is paired against the
Johnston / switch numbers of r14 without recomputing his min-plus. python 3.6 + numpy 1.19 compatible.
Variants: (c) no detour (zero-count pairs start at the median, weight 0), w_far = 0.1 and 0.2. Records npts to check the universe matches r14.
Usage: python r17_cluster_cfit.py n seed out.npz     |     python r17_cluster_cfit.py analyse <r14 folder> <r17 folder>
"""
import sys
import glob
import time
import numpy as np
from r11_4d_distance import load_table
from r12_johnston_compare import mink
from r13_mixed import ours_spatial, sprinkle
from r15_cheap_far import related_R
from r16_local_fit import fit_c
from r14_cluster_scale import spatial_dist

np.seterr(all="ignore")
VARIANTS = (("c_w0.1", 0.1), ("c_w0.2", 0.2))

def main(n, seed, out):
    W = load_table()
    rng = np.random.default_rng(seed)
    P, C, rho = sprinkle(n, rng)                                 # identical to r14 (first use of the rng)
    print("n = %d (Poisson %d), seed %d" % (n, len(P), seed), flush=True)
    T = {}
    t0 = time.time(); R, t = related_R(C, rho); T["related"] = time.time() - t0
    t0 = time.time(); S = ours_spatial(C, rho, t, W); T["ours_step"] = time.time() - t0
    iu = np.triu_indices(len(P), 1)
    sp = ~np.isfinite(R[iu]); I, J = iu[0][sp], iu[1][sp]
    del C
    maps = {}
    for name, wf in VARIANTS:
        t0 = time.time()
        maps[name] = fit_c(R, S, t, I, J, 0.25, wf, detour_init=False)
        T["fit_" + name] = time.time() - t0
        print("  %s fitted in %.0f s" % (name, T["fit_" + name]), flush=True)
    del R, S, I, J, sp
    st, mt = spatial_dist(P, iu), mink(P)[iu]
    names, a, b = [], [], []
    for k, X in maps.items():
        names.append(k); a.append(np.corrcoef(spatial_dist(X, iu), st)[0, 1]); b.append(np.corrcoef(mink(X)[iu], mt)[0, 1])
        print("  %-8s spatial corr %.4f   Minkowski corr %.4f" % (k, a[-1], b[-1]), flush=True)
    np.savez(out, n=n, npts=len(P), seed=seed, names=np.array(names), spatial=np.array(a), minkowski=np.array(b),
             timing_keys=np.array(list(T)), timing=np.array(list(T.values())))
    print("  timing (s): " + ", ".join("%s %.0f" % kv for kv in T.items()), flush=True)

def analyse(d14, d17):
    r14 = {(int(z["n"]), int(z["seed"])): z for z in (np.load(f) for f in glob.glob(d14 + "/r14_n*_s*.npz"))}
    r17 = {(int(z["n"]), int(z["seed"])): z for z in (np.load(f) for f in glob.glob(d17 + "/r17_n*_s*.npz"))}
    for n in sorted({k[0] for k in r17}):
        keys = sorted(k for k in r17 if k[0] == n and k in r14)
        if not keys:
            print("n = %d: no matching r14 universes yet" % n); continue
        bad = [k for k in keys if int(r14[k]["npts"]) != int(r17[k]["npts"])]
        print("n = %d (%d paired universes%s)" % (n, len(keys), "; MISMATCHED UNIVERSES %s" % bad if bad else ""))
        j = np.array([r14[k]["spatial"][list(r14[k]["names"]).index("johnston")] for k in keys])
        sw = np.array([r14[k]["spatial"][list(r14[k]["names"]).index("switch0.25")] for k in keys])
        rows = [("switch0.25", sw)] + [(nm, np.array([r17[k]["spatial"][list(r17[k]["names"]).index(nm)] for k in keys])) for nm, _ in VARIANTS]
        print("  johnston     spatial %.4f" % j.mean())
        for nm, v in rows:
            d = v - j
            print("  %-12s spatial %.4f   vs johnston %+.4f +- %.4f   (%.0f %% of his residual)" % (nm, v.mean(), d.mean(),
                  d.std(ddof=1) / np.sqrt(len(d)) if len(d) > 1 else np.nan, 100 * d.mean() / (1 - j.mean())))
        tm = np.mean([dict(zip(r17[k]["timing_keys"], r17[k]["timing"]))["fit_c_w0.1"] for k in keys])
        his = np.mean([dict(zip(r14[k]["timing_keys"], r14[k]["timing"])) for k in keys][0]["johnston"])
        print("  time: (c) fit %.0f s (+ our step) vs his johnston() %.0f s (one universe)" % (tm, his))

if __name__ == "__main__":
    if sys.argv[1] == "analyse":
        analyse(sys.argv[2], sys.argv[3])
    else:
        main(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
