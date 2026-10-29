"""A1 (ideas 002, 005): raw samples of uniform random 2D orders at N ~ 200, for the quantum reweighting of S4c.

One job = one seed. For each universe store the raw numbers; records, quartile edges and the beta grid are chosen
later in the analysis (a1_analyse.py), so the cluster never has to rerun when we change the record (lesson 3).
    S       2D Benincasa-Dowker action, eps = 0.21 (as S3a/S4c)
    layers  number of cosmic-time layers = longest chain (the AGE record of s3q)
    stress  detector stress (0 = perfect 2D Minkowski fit), NaN if the detector had too few events
    r_pos   2nd / 1st positive MDS eigenvalue (large = extra space direction)
Usage: python a1_sample.py N n_samples seed outfile.npz
"""
import sys, time
import numpy as np
from s3a_mcmc_2d import f_weights, action, observables
from s4b_detector import diagnostics

np.seterr(all="ignore")                           # numpy 2.0 + Accelerate emits spurious matmul warnings

if __name__ == "__main__":
    N, n, seed, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    eps = 0.21
    rng = np.random.default_rng(seed)
    fw = f_weights(N, eps)
    S, layers, stress, rpos = (np.full(n, np.nan) for _ in range(4))
    t0 = time.time()
    for k in range(n):
        u, v = rng.permutation(N), rng.permutation(N)
        S[k], C = action(u, v, eps, fw)
        layers[k] = observables(C)[2]
        d = diagnostics(C > 0)
        if d is not None:
            stress[k], rpos[k] = d[3], d[1]
    np.savez_compressed(out, N=N, eps=eps, seed=seed, S=S, layers=layers.astype(np.int16),
                        stress=stress.astype(np.float32), rpos=rpos.astype(np.float32))
    print(f"N={N} n={n} seed={seed}: {time.time() - t0:.1f} s, {(time.time() - t0) / n * 1e3:.2f} ms/universe, "
          f"sd_S={np.std(S):.2f}, NaN stress={np.isnan(stress).sum()}", flush=True)
