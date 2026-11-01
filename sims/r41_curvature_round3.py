"""Depth-drift curvature estimator: external referee round 3 on the 1+1 paper (session 19; toolkit-1p1-v3, comments 19 and 22).
The one-region comparison of r40 'noise' drew its P pairs one at a time: a uniform among the elements of a small target region, b uniform among
the elements spacelike to a at the required offset. That is the single-uniform-draw selection of r40 'select' (uniform1), which reads low; so the
in-region low bias reported in v3 could be selection, not the sharing of elements between pairs. Here the same diamond, same seeds, with:
  mecke : every pair (a in the target region, b spacelike to a at the same offsets) is kept with a fixed probability q_P, the same in every
          sprinkling (q_P = P / mean number of qualifying pairs over ten pilot sprinklings, seeds 9001-9010, not analysed); nested thinning
          (one uniform number per pair), so the P = 10 set is inside the P = 30 set, etc. By the Mecke formula the pooled sums then have the
          inserted-pair expectations.
  uniform: the r40 selection, rerun for the matched-count flat control only.
Flat control at matched element count (comment 22): the flat diamond of the same coordinate size holds 3.35 x the elements of the de Sitter one,
so the flat runs use rho = 4000 * 2511 / 8413 and 1e4 * 6280 / 21034 (element counts of r40), i.e. the de Sitter element counts.
Usage: python r41_curvature_round3.py [workers] [seeds]   (writes runs/r41/*.npy and prints the summary)
"""
import os
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1"); os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import sys
import time
import numpy as np
from multiprocessing import Pool
from r40_curvature_round2 import sprinkle_region, multi_counts, analyse_pair, f_cont_diamond, D_LO, D_HI, PS

np.seterr(all="ignore")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "runs", "r41")

def qualifying_pairs(eta, x, u, v):
    """All (a, b) with a in the target region and b spacelike to a at offset x_b - x_a in [0.1, 0.2], |eta_b - eta_a| <= 0.05 (r40's rule)."""
    cand = np.flatnonzero((eta > -1.25) & (eta < -1.05) & (np.abs(x) <= 0.1))
    out = []
    for a in cand:
        cb = np.flatnonzero((x - x[a] >= 0.1) & (x - x[a] <= 0.2) & (np.abs(eta - eta[a]) <= 0.05))
        cb = cb[(u[cb] - u[a]) * (v[cb] - v[a]) < 0]
        out += [(a, b) for b in cb]
    return out

def task(args):
    seed, rho, geom, mode, qs = args
    rng = np.random.default_rng(seed)                                        # same sprinkling as r40 'noise' for the same (seed, rho, geom)
    eta, x = sprinkle_region(rho, geom, "diamond", rng, D_LO, D_HI, D_HI - D_LO)
    u, v = eta - x, eta + x
    if mode == "count":
        return seed, len(qualifying_pairs(eta, x, u, v))
    sel = np.random.default_rng(10 ** 6 + seed)
    if mode == "mecke":
        allp = qualifying_pairs(eta, x, u, v)
        r = sel.random(len(allp))
        keep = np.flatnonzero(r < max(qs))
        pairs = [allp[i] for i in keep]; rk = r[keep]
    else:                                                                    # r40's sequential uniform draw
        cand = np.flatnonzero((eta > -1.25) & (eta < -1.05) & (np.abs(x) <= 0.1))
        pairs = []
        while len(pairs) < max(PS):
            a = sel.choice(cand)
            cb = np.flatnonzero((x - x[a] >= 0.1) & (x - x[a] <= 0.2) & (np.abs(eta - eta[a]) <= 0.05))
            cb = cb[(u[cb] - u[a]) * (v[cb] - v[a]) < 0]
            if len(cb):
                pairs.append((a, sel.choice(cb)))
        rk = np.arange(len(pairs))
    Ks = multi_counts(u, v, pairs, geom, rho) if pairs else []
    R = np.array([analyse_pair(K, rho)[0] for K in Ks]).reshape(-1, 4)
    N = len(u); rel = 0
    for i in range(0, N, 2048):
        rel += ((u[i:i + 2048, None] < u[None, :]) & (v[i:i + 2048, None] < v[None, :])).sum()
    return seed, R, rk, rel / (N * (N - 1) / 2), N

def run(workers, seeds):
    os.makedirs(OUT, exist_ok=True)
    fc = f_cont_diamond("dS")
    cases = (("dS", 4000.0, "mecke"), ("dS", 1e4, "mecke"),
             ("flat", 4000.0 * 2511 / 8413, "mecke"), ("flat", 4000.0 * 2511 / 8413, "uniform"),
             ("flat", 1e4 * 6280 / 21034, "mecke"), ("flat", 1e4 * 6280 / 21034, "uniform"))
    for geom, rho, mode in cases:
        t0 = time.time()
        with Pool(workers) as pool:
            qs = None
            if mode == "mecke":
                npil = np.mean([c for _, c in pool.map(task, [(s, rho, geom, "count", None) for s in range(9001, 9011)])])
                qs = {P: min(1.0, P / npil) for P in PS}
            res = pool.map(task, [(s, rho, geom, mode, tuple(qs.values()) if qs else None) for s in range(1, seeds + 1)], chunksize=2)
        np.save(os.path.join(OUT, f"{mode}_{geom}_{int(rho)}.npy"), np.array(res, dtype=object), allow_pickle=True)
        f = np.array([r[3] for r in res]); Nn = np.mean([r[4] for r in res])
        Rch = 2 * (f - 0.5) / (fc - 0.5)
        head = f"qualifying pairs per sprinkling {npil:.0f} (pilot)" if qs else "r40 sequential uniform draw"
        print(f"== {mode}, {geom} diamond u, v in [{D_LO}, {D_HI}], rho = {rho:.0f} ({Nn:.0f} elements), {seeds} sprinklings ({time.time() - t0:.0f} s); {head} ==")
        print(f"  ordering fraction (whole diamond): R {Rch.mean():+.3f}, s.d. between sprinklings {Rch.std():.3f}")
        for P in PS:
            Rp, Rc, npairs = [], [], []
            for _, R, rk, _, _ in res:
                w = R[rk < qs[P]] if qs else R[:P]
                w = w[np.isfinite(w).all(1)]
                npairs.append(len(w))
                if len(w):
                    Rp.append(-16 * w[:, 0].sum() / w[:, 1].sum()); Rc.append(-16 * w[:, 2].sum() / w[:, 3].sum())
            Rp, Rc = np.array(Rp), np.array(Rc)
            print(f"  depth drift, P = {P:3d} (mean {np.mean(npairs):.0f} pairs): R {Rp.mean():+.3f} +- {Rp.std() / np.sqrt(len(Rp)):.3f},"
                  f" s.d. between sprinklings {Rp.std():.3f}   (continuum fit of the same c's {Rc.mean():+.3f}; rms about it {np.sqrt(((Rp - Rc) ** 2).mean()):.3f})")
        sys.stdout.flush()

if __name__ == "__main__":
    run(int(sys.argv[1]) if len(sys.argv) > 1 else 8, int(sys.argv[2]) if len(sys.argv) > 2 else 400)
