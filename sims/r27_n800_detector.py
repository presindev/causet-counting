"""Second held-out size for the embedding test's layered flag (paper Sec. 5; idea 005, session 14): N = 800.

The rule (paper): flag a universe as layered when the zero share z > 1.5 x the median z of flat universes (random 2D orders) at the same N;
"is it a flat sheet?" is read from stress_top against the flat band. It was designed after seeing the N = 400 states and held out at N = 200;
the v1 review asked for one more size. Features as in r8_detector_spread.features (M = 80, 5 spread draws), unchanged.
Inputs: final states of e^{-beta S} chains at N = 800 (n400_crystal.py run with N = 800; job sims/cluster/r27_job.sh), hot starts only
(at N = 400 the 4-11-layer states came from hot starts at beta N >= 180; cold starts gave 2-3 layers, which break the pipeline).
Usage: python r27_n800_detector.py calibrate          (laptop: 50 + 50 flat N = 800, de Sitter H tau = 1, 4)
       python r27_n800_detector.py analyse DIR       (DIR holds the r27 .npz files; uses the saved calibration)
"""
import os, sys, glob
import numpy as np
from r8_detector_spread import features, order
from s4b_desitter_stress import desitter_diamond

np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
CAL = os.path.join(HERE, "out", "r27_flat_n800.npz")
N, M, DRAWS = 800, 80, 5

def calibrate(seed=27):
    rng = np.random.default_rng(seed)
    flat = lambda: order(rng.permutation(N), rng.permutation(N))
    F = np.array([features(flat(), M, DRAWS, rng) for _ in range(50)])
    G = [features(flat(), M, DRAWS, rng) for _ in range(50)]
    z_med = np.median(F[:, 2]); thr = 1.5 * z_med
    print(f"flat N={N} (50, M={M}): stress_top median {np.median(F[:, 0]):.3f} (band {F[:, 0].mean():.3f} +- {F[:, 0].std(ddof=1):.3f}), "
          f"r+ median {np.median(F[:, 1]):.3f}, zero share median {z_med:.3f} (range {F[:, 2].min():.3f}-{F[:, 2].max():.3f}) -> flag z > {thr:.3f}")
    nofeat = sum(g is None for g in G)
    print(f"independent flat (50): {sum(g is not None and g[2] > thr for g in G)} flagged layered, {nofeat} pipeline failures")
    for tau in (1.0, 4.0):
        D = [features(desitter_diamond(N, tau, rng), M, DRAWS, rng) for _ in range(10)]
        D = [d for d in D if d is not None]
        print(f"de Sitter N={N} H tau={tau}: stress_top {np.min([d[0] for d in D]):.3f}-{np.max([d[0] for d in D]):.3f}, "
              f"zero {np.min([d[2] for d in D]):.3f}-{np.max([d[2] for d in D]):.3f}, flagged {sum(d[2] > thr for d in D)}/{len(D)}")
    np.savez(CAL, F=F, z_med=z_med, thr=thr)

def analyse(d):
    cal = np.load(CAL); thr, F = float(cal["thr"]), cal["F"]
    band = F[:, 0].mean() + 2 * F[:, 0].std(ddof=1)
    print(f"N={N}: layered flag z > {thr:.3f}; flat-sheet band stress_top <= {band:.3f} (flat mean + 2 sd)")
    fs = sorted(f for f in glob.glob(os.path.join(d, "*.npz")) if "partial" not in f)
    rows = []
    for f in fs:
        z = np.load(f)
        ft = features(order(z["u"].astype(int), z["v"].astype(int)), M, DRAWS, np.random.default_rng(int(z["seed"])))
        L = int(z["layers"][-1])
        verdict = "no run (fail)" if ft is None else ("LAYERED" if ft[2] > thr else ("not flat" if ft[0] > band else "pass"))
        rows.append((L, float(z["beta"]), os.path.basename(f), ft, verdict, int(z["sweep"][-1]), float(z["acc"][-1])))
    print(" layers  beta  sweeps   acc   stress_top  r+_spread  zero   verdict   file")
    for L, b, name, ft, v, sw, acc in sorted(rows):
        nums = "      -          -       -  " if ft is None else f"{ft[0]:9.3f}  {ft[1]:9.3f}  {ft[2]:6.3f}"
        print(f"  {L:4d}  {b:5.3f} {sw:6d}  {acc:.3f}  {nums}   {v:<9} {name}")
    cont = [r for r in rows if r[0] >= 20]; lay = [r for r in rows if 4 <= r[0] < 20]; few = [r for r in rows if r[0] < 4]
    print(f"continuum-like (>= 20 layers): {sum(r[4] == 'pass' for r in cont)}/{len(cont)} pass; "
          f"layered (4-19): {sum(r[4] == 'LAYERED' for r in lay)}/{len(lay)} flagged; 2-3 layers: {len(few)} (pipeline fails by design)")

if __name__ == "__main__":
    if sys.argv[1] == "calibrate":
        calibrate()
    else:
        analyse(sys.argv[2])
