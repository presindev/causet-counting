"""Likelihood embedding at large n on the cluster (idea 005, session 12), on the SAME universes as r14 (same seed, same first rng call), paired against its Johnston /
switch numbers. python 3.6 + numpy 1.19 compatible. Start: count-weighted fit K0 = 100 (r19); then r23's likelihood (400 Adam iterations), first with the related-pair Poisson term only
(the session-12 ablation winner, = Casasola 2026's count likelihood), then with both terms.
Saves after the start map and after the fit (lesson 22).
Usage: python r24_cluster_lik.py n seed out.npz     |     python r24_cluster_lik.py analyse <r14 folder> <r24 folder>
"""
import sys
import glob
import time
import numpy as np
from r11_4d_distance import load_table
from r13_mixed import sprinkle
from r15_cheap_far import related_R
from r18_waist_oracle import ours_with_counts
from r19_cluster_wfit import fit_w
from r23_likelihood import Table, setup, fit
from r14_cluster_scale import spatial_dist

np.seterr(all="ignore")

def main(n, seed, out):
    W = load_table(); tab = Table(W)
    rng = np.random.default_rng(seed)
    P, C, rho = sprinkle(n, rng)                                 # identical to r14 (first use of the rng)
    print("n = %d (Poisson %d), seed %d" % (n, len(P), seed), flush=True)
    iu = np.triu_indices(len(P), 1)
    st = spatial_dist(P, iu)
    T, names, a = {}, [], []
    def save():
        np.savez(out, n=n, npts=len(P), seed=seed, names=np.array(names), spatial=np.array(a), timing_keys=np.array(list(T)), timing=np.array(list(T.values())))
    t0 = time.time(); R, t = related_R(C, rho); I, J, s, k = ours_with_counts(C, rho, t, W); T["ours_step"] = time.time() - t0
    t0 = time.time(); Xw, _ = fit_w(R, t, I, J, s, k, 100); T["fit_K100"] = time.time() - t0
    del R, I, J, s, k
    names.append("w_K100"); a.append(np.corrcoef(spatial_dist(Xw, iu), st)[0, 1]); save()
    print("  w_K100 spatial corr %.4f (%.0f s)" % (a[-1], T["fit_K100"]), flush=True)
    S, Rl = setup(C, rho, t, W); del C
    S0 = dict(S); S0["nb"] = np.zeros_like(S["nb"]); S0["nc"] = np.zeros_like(S["nc"])      # binomial term off: related-pair Poisson only (session-12 ablation)
    for name, SS in (("poisson_only", S0), ("likelihood", S)):
        t0 = time.time()
        xl, hist = fit(Xw[:, 1:], t, SS, Rl, rho, tab, 400); T[name] = time.time() - t0
        X = np.column_stack([t, xl])
        names.append(name); a.append(np.corrcoef(spatial_dist(X, iu), st)[0, 1]); save()
        print("  %s spatial corr %.4f (%.0f s); loglik %s" % (name, a[-1], T[name], " ".join("%d:%.0f" % h for h in hist[::2])), flush=True)

def analyse(d14, d24):
    r14 = {(int(z["n"]), int(z["seed"])): z for z in (np.load(f) for f in glob.glob(d14 + "/r14_n*_s*.npz"))}
    r24 = {(int(z["n"]), int(z["seed"])): z for z in (np.load(f) for f in glob.glob(d24 + "/r24_n*_s*.npz"))}
    for n in sorted({kk[0] for kk in r24}):
        keys = sorted(kk for kk in r24 if kk[0] == n and kk in r14)
        if not keys:
            print("n = %d: no matching r14 universes yet" % n); continue
        bad = [kk for kk in keys if int(r14[kk]["npts"]) != int(r24[kk]["npts"])]
        print("n = %d (%d paired universes%s)" % (n, len(keys), "; MISMATCHED UNIVERSES %s" % bad if bad else ""))
        j = np.array([r14[kk]["spatial"][list(r14[kk]["names"]).index("johnston")] for kk in keys])
        rows = [("switch0.25", np.array([r14[kk]["spatial"][list(r14[kk]["names"]).index("switch0.25")] for kk in keys]))]
        for nm in ("w_K100", "poisson_only", "likelihood"):
            ks = [kk for kk in keys if nm in list(r24[kk]["names"])]
            if len(ks) == len(keys):
                rows.append((nm, np.array([r24[kk]["spatial"][list(r24[kk]["names"]).index(nm)] for kk in keys])))
        print("  johnston     spatial %.4f" % j.mean())
        for nm, v in rows:
            d = v - j
            print("  %-12s spatial %.4f   vs johnston %+.4f +- %.4f   (%.0f %% of his residual)" % (nm, v.mean(), d.mean(),
                  d.std(ddof=1) / np.sqrt(len(d)) if len(d) > 1 else np.nan, 100 * d.mean() / (1 - j.mean())))

if __name__ == "__main__":
    if sys.argv[1] == "analyse":
        analyse(sys.argv[2], sys.argv[3])
    else:
        main(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
