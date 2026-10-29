"""Summarize r14 results (fetched from cluster): per n, mean spatial / Minkowski corr per method, paired difference vs Johnston, and timing.
Usage: python r14_analyse.py <folder with r14_n*_s*.npz>
"""
import sys, glob
import numpy as np

files = sorted(glob.glob(sys.argv[1] + "/r14_n*_s*.npz"))
runs = [np.load(f) for f in files]
for n in sorted({int(r["n"]) for r in runs}):
    R = [r for r in runs if int(r["n"]) == n]
    names = list(R[0]["names"])
    S = np.array([r["spatial"] for r in R]); M = np.array([r["minkowski"] for r in R])
    se = lambda x: x.std(ddof=1) / np.sqrt(len(x)) if len(x) > 1 else np.nan
    print("n = %d (%d universes; points %s)" % (n, len(R), ", ".join(str(int(r["npts"])) for r in R)))
    for k, nm in enumerate(names):
        d = S[:, k] - S[:, 0]
        print("  %-12s spatial %.4f  Minkowski %.4f   vs johnston %+.4f +- %.4f" % (nm, S[:, k].mean(), M[:, k].mean(), d.mean(), se(d)))
    keys = list(R[0]["timing_keys"]); Tm = np.array([r["timing"] for r in R]).mean(0); t = dict(zip(keys, Tm))
    print("  timing (s, mean): his min-plus %.0f | our step %.0f | shared C@C %.0f + eigh %.0f | fallback share %.1e"
          % (t["johnston"] - t["CC"] - t["eigh"], t["ours_step"], t["CC"], t["eigh"], np.mean([float(r["fallback"]) for r in R])))
