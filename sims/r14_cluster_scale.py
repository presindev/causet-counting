"""Johnston 2025 vs ours vs the switch at larger n, for cluster (idea 005, session 11). One universe per call; python 3.6 + numpy 1.19 compatible.

Laptop (r13_mixed.py, n = 500-3000): the switch (ours if our estimate < L, his min-plus detour otherwise) beats him by +0.021 ... +0.007 in spatial corr,
held out, with the gain shrinking with n. Question for cluster: at n = 6000-15000, does the gain survive, and does pure ours catch up with him?
Methods, all in his pipeline (his time coordinate, Euclidean MDS anchored at v1), differing only in the spacelike r:
    johnston : min-plus detour over related z (r12.johnston)
    ours     : our overlap estimate for every spacelike pair (his r only where a count is 0; the share is reported). The only variant without his min-plus.
    ours_capped : min(ours, his r) (his r is a triangle-inequality upper bound; best "ours" variant in session 11)
    switchL  : ours if our estimate < L, his r otherwise (L = 0.2, 0.25, 0.3; half-width of the diamond is 0.5)
Metrics: corr of embedded vs true spatial distances (his Table V) and of embedded vs true squared Minkowski intervals (his Table IV), all pairs.
Timing of each step (one node, threads as given by the job).
Usage: python r14_cluster_scale.py n seed out.npz   (summary: r14_analyse.py <folder>)
"""
import sys
import time
import numpy as np
from r11_4d_distance import load_table
from r12_johnston_compare import johnston, mink
from r13_mixed import ours_spatial, embed_from_r, sprinkle

np.seterr(all="ignore")
LS = (0.2, 0.25, 0.3)

def spatial_dist(X, iu):
    D2 = np.zeros((len(X), len(X)))
    for k in range(1, X.shape[1]):
        D2 += (X[:, None, k] - X[None, :, k]) ** 2
    return np.sqrt(D2[iu])

def main(n, seed, out):
    W = load_table()
    rng = np.random.default_rng(seed)
    T = {}
    t0 = time.time()
    P, C, rho = sprinkle(n, rng)
    T["sprinkle"] = time.time() - t0
    print("n = %d (Poisson %d), seed %d, sprinkled in %.1f s" % (n, len(P), seed, T["sprinkle"]), flush=True)
    t0 = time.time()
    Cf = C.astype(np.float32); _ = Cf @ Cf; del Cf
    T["CC"] = time.time() - t0
    t0 = time.time()
    r_j, Xj = johnston(C, rho, 1.0)                             # C @ C + min-plus + eigh
    T["johnston"] = time.time() - t0
    t = Xj[:, 0]
    print("  johnston %.1f s" % T["johnston"], flush=True)
    t0 = time.time()
    S = ours_spatial(C, rho, t, W)
    T["ours_step"] = time.time() - t0
    rel = C | C.T
    sp = ~rel & ~np.eye(len(C), dtype=bool)
    fallback = (sp & ~np.isfinite(S)).sum() / max(sp.sum(), 1)
    t0 = time.time()
    X_o = embed_from_r(np.where(sp & np.isfinite(S), S, r_j), t)
    T["eigh"] = time.time() - t0
    print("  ours step %.1f s, eigh %.1f s, fallback share %.2e" % (T["ours_step"], T["eigh"], fallback), flush=True)
    emb = {"johnston": Xj, "ours": X_o,
           "ours_capped": embed_from_r(np.where(sp & np.isfinite(S), np.minimum(S, r_j), r_j), t)}
    for L in LS:
        emb["switch%.2f" % L] = embed_from_r(np.where(sp & (S < L), S, r_j), t)
    del S, r_j, rel, sp, C
    iu = np.triu_indices(len(P), 1)
    st, mt = spatial_dist(P, iu), mink(P)[iu]
    names, sc_sp, sc_mk = [], [], []
    for k, X in emb.items():
        names.append(k)
        sc_sp.append(np.corrcoef(spatial_dist(X, iu), st)[0, 1])
        sc_mk.append(np.corrcoef(mink(X)[iu], mt)[0, 1])
        print("  %-12s spatial corr %.4f   Minkowski corr %.4f" % (k, sc_sp[-1], sc_mk[-1]), flush=True)
    np.savez(out, n=n, npts=len(P), seed=seed, names=np.array(names), spatial=np.array(sc_sp), minkowski=np.array(sc_mk),
             timing_keys=np.array(list(T)), timing=np.array(list(T.values())), fallback=fallback)
    print("  timing (s): " + ", ".join("%s %.1f" % kv for kv in T.items()) + "  -> his min-plus ~ %.1f s" % (T["johnston"] - T["CC"] - T["eigh"]), flush=True)

if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
