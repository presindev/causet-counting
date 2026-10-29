"""Does a depth-spread sample fix the detector's blind spot for ~10-layer universes? (idea 005, session 11)

Session 11 found that at N = 400 the embedding detector (s4b_detector.py, sample = events with the largest pasts) does not reliably flag the
~10-layer Monte Carlo states: stress 0.06-0.31 against a flat band 0.08 +- 0.02, and the verdict flips with the sample size.
Suspected cause: in a layered order the largest pasts are the top one or two layers. Fix tested here: sample="spread", events evenly
spaced in height over the upper 70 % of the order, then a random M of those that share common pasts.
Calibrate first (lessons 4, 10): random 2D orders at N = 100, 200, 400 with the new sample; then the N = 400 Monte Carlo final states
(n400_out, n400_fetch) by layer count, both samples, M = 40 and 80, several random draws per universe for the spread sample.
Part 2 (after part 1 showed the spread sample's stress is noisy but its r+ separates, and that a bilayer gives an all-zero interval
matrix that MDS "fits" perfectly): a combined rule on three numbers per universe,
    stress_top (old sample), r+_spread (median over draws), zero (largest share of zero-length pairs over both samples),
with thresholds set at the maximum over 50 flat N = 400 universes (so the flat false-positive rate is < ~2 % by construction, and
an independent set of 50 measures it). A universe "fails" if any number exceeds its threshold or the pipeline cannot run.
Usage: python r8_detector_spread.py [draws=5]  |  python r8_detector_spread.py holdout
"""
import os, sys, glob
import numpy as np
from s4b_detector import diagnostics

np.seterr(all="ignore")                          # numpy + Accelerate: spurious matmul warnings
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def order(u, v):
    return (u[:, None] < u[None, :]) & (v[:, None] < v[None, :])

def safe(C, **kw):
    try:
        return diagnostics(C, **kw)
    except (IndexError, ValueError):
        return None

def stats(Cs, sample, M, draws, rng):
    """Stress and r+ over universes x draws; also the fraction of runs where the pipeline could not run."""
    out, fails = [], 0
    for C in Cs:
        for _ in range(draws if sample == "spread" else 1):
            d = safe(C, M0=int(1.5 * M), M=M, sample=sample, rng=rng)
            if d is None:
                fails += 1
            else:
                out.append((d[3], d[1], d[4]))
    return np.array(out), fails

def line(label, A, fails, total):
    if len(A) == 0:
        return f"{label:<30} pipeline failed {fails}/{total}"
    return (f"{label:<30} stress {np.median(A[:, 0]):.3f} [{A[:, 0].min():.2f}-{A[:, 0].max():.2f}]  r+ {np.median(A[:, 1]):.3f} "
            f"[{A[:, 1].min():.2f}-{A[:, 1].max():.2f}]  M~{A[:, 2].mean():.0f}  failed {fails}/{total}")

def features(C, M, draws, rng):
    """(stress_top, r+_spread median, zero share max) or None if the pipeline cannot run on either sample."""
    t = safe(C, M0=int(1.5 * M), M=M, sample="top", rng=rng)
    sp = [safe(C, M0=int(1.5 * M), M=M, sample="spread", rng=rng) for _ in range(draws)]
    sp = [d for d in sp if d is not None]
    if t is None or len(sp) < (draws + 1) // 2:
        return None
    return t[3], np.median([d[1] for d in sp]), max([t[5]] + [d[5] for d in sp])

if __name__ == "__main__" and sys.argv[1:2] != ["holdout"]:
    draws = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    M = 80
    rng = np.random.default_rng(11)
    def flat(N):
        return order(rng.permutation(N), rng.permutation(N))
    F = np.array([features(flat(400), M, draws, rng) for _ in range(50)])
    T = F.max(0)
    print(f"thresholds from 50 flat N=400 (M={M}, {draws} spread draws): stress_top {T[0]:.3f}  r+_spread {T[1]:.3f}  zero {T[2]:.3f}")
    print(f"  flat medians: stress_top {np.median(F[:, 0]):.3f}  r+_spread {np.median(F[:, 1]):.3f}  zero {np.median(F[:, 2]):.3f}")
    def verdict(f):
        if f is None:
            return "FAIL(no run)"
        flags = [n for n, x, t in zip(("stress", "r+", "zero"), f, T) if x > t]
        return ("FAIL(" + ",".join(flags) + ")") if flags else "pass"
    G = [features(flat(400), M, draws, rng) for _ in range(50)]
    print(f"independent flat N=400: {sum(verdict(f) != 'pass' for f in G)}/50 false fails")
    from s4b_desitter_stress import desitter_diamond
    for tau in (1.0, 2.0, 4.0):
        V = [verdict(features(desitter_diamond(400, tau, rng), M, draws, rng)) for _ in range(10)]
        print(f"de Sitter N=400 H tau={tau}: {sum(v != 'pass' for v in V)}/10 fail  {sorted(set(V))}")
    fs = sorted({os.path.basename(f): f for f in glob.glob(os.path.join(ROOT, "n400_*", "**", "*.npz"), recursive=True)
                 if "partial" not in f}.values())
    print("N = 400 Monte Carlo final states: layers, stress_top, r+_spread, zero, verdict")
    for f in sorted(fs, key=lambda f: int(np.load(f)["layers"][-1])):
        z = np.load(f)
        ft = features(order(z["u"].astype(int), z["v"].astype(int)), M, draws, rng)
        nums = "      -      -      -" if ft is None else f"{ft[0]:7.3f}{ft[1]:7.3f}{ft[2]:7.3f}"
        print(f"  {int(z['layers'][-1]):3d} {os.path.basename(f):<28}{nums}  {verdict(ft)}")


def holdout(N=200, draws=5, seed=21):
    """Held-out test (the rule above was designed after seeing the N = 400 states): fresh N = 200 Monte Carlo chains (s3a_fast, eps = 0.21),
    thresholds recalibrated on 50 flat N = 200 universes, then 6 samples per beta from 2 chains each."""
    from s3a_fast import samples
    from s2_counting_geometry import causal_from_growth
    from growth_percolation import grow
    M = 60
    rng = np.random.default_rng(seed)
    F = np.array([features(order(rng.permutation(N), rng.permutation(N)), M, draws, rng) for _ in range(50)])
    T = F.max(0)
    print(f"holdout N={N}, M={M}: thresholds stress_top {T[0]:.3f}  r+_spread {T[1]:.3f}  zero {T[2]:.3f}")
    G = [features(order(rng.permutation(N), rng.permutation(N)), M, draws, rng) for _ in range(50)]
    fails = lambda f: f is None or any(x > t for x, t in zip(f, T))
    print(f"  independent flat: {sum(fails(f) for f in G)}/50 false fails")
    for beta in (0.05, 0.3, 0.6, 1.0, 1.5):
        Cs = [C for s in (seed, seed + 1) for C in samples(N, beta, 0.21, n_samples=3, sweeps_between=50, seed=s)]
        fs = [features(C, M, draws, rng) for C in Cs]
        from s4b_detector import height
        L = [height(C).max() + 1 for C in Cs]
        print(f"  beta={beta}: layers {L}  fail {sum(fails(f) for f in fs)}/{len(fs)}  "
              + " ".join("-" if f is None else f"({f[0]:.2f},{f[1]:.2f},{f[2]:.2f})" for f in fs), flush=True)
    for label, kw in [("growth p=0.05", dict(p=0.05)), ("growth p=3/n", dict(p=None, c=3))]:
        Cs = [causal_from_growth(grow(N, seed=s, originary=True, **kw)[0], N) for s in range(1, 7)]
        fs = [features(C > 0, M, draws, rng) for C in Cs]
        print(f"  {label}: fail {sum(fails(f) for f in fs)}/{len(fs)}")


if __name__ == "__main__" and sys.argv[1:2] == ["holdout"]:
    holdout()
