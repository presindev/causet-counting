"""Baselines for the 1+1 rectangle estimator (session 15; PRD referee on toolkit-1p1-v1, major item 2).
Flat sprinklings of the unit (u, v) square as in s4a_overlap_distance.py (rho = 2N), plus a bottom tip at (0, 0) that precedes every element.
Pairs: random spacelike pairs in the MIDDLE band 0.8 < u + v < 1.2, so that both a common past and a common future exist. Per pair:
    rect_deep : 2 N_A N_B / (rho (N_C + 1)) with the deepest c (largest N_C)          -- the paper's estimator; c selected on its own N_C
    rect_tip  : the same with c = the bottom tip (chosen without looking at any count) -- N_A, N_B, N_C independent Poisson
    bk        : Bogun~a-Krioukov's equal-depth filter (their Eq. 34), as in s4a
    direct    : 2 (min_{c < a,b < f} N(c, f) - 2) / rho  (Brightwell-Gregory / Rideout-Wallden: smallest interval holding both, minus a and b)
Reported per bin of d / ell (< 2, 2-10, > 10): mean signed relative error of d and of d^2 +- s.e. from the spread of per-seed means (12 seeds x 100 pairs; pairs in one sprinkling are correlated) and median absolute relative error.
Usage: python r31_rect_baseline.py [N ...]
"""
import sys
import numpy as np
from s4a_overlap_distance import sprinkle, causal, pair_counts, est_bk

BINS = ((0, 2), (2, 10), (10, 1e9))
NAMES = ("rect_deep", "rect_tip", "bk", "direct")

def run(n, n_pairs, seed):
    rng = np.random.default_rng(seed)
    u, v = sprinkle(n, rng)
    u = np.concatenate([[0.0], u]); v = np.concatenate([[0.0], v])          # element 0 = bottom tip
    rho = 2 * n
    C = causal(u, v); C[0, 1:] = 1
    with np.errstate(all="ignore"):
        K = C @ C
    mid = np.flatnonzero((u + v > 0.8) & (u + v < 1.2))
    rows = []
    while len(rows) < n_pairs:
        a, b = rng.choice(mid, 2, replace=False)
        du, dv = u[b] - u[a], v[b] - v[a]
        if du * dv >= 0:
            continue
        d = np.sqrt(-du * dv)
        nA, nB, nC = pair_counts(C, K, a, b)
        cs = np.flatnonzero(C[:, a] * C[:, b])
        k = np.argmax(nC); deep = np.sqrt(2 * nA[k] * nB[k] / (rho * (nC[k] + 1)))
        t = int(np.flatnonzero(cs == 0)[0]); tip = np.sqrt(2 * nA[t] * nB[t] / (rho * (nC[t] + 1)))
        bk, _ = est_bk(nA, nB, nC, rho)
        F = np.flatnonzero(C[a] * C[b])
        direct = np.sqrt(2 * max(K[np.ix_(cs, F)].min() - 2, 0) / rho) if len(F) else np.nan
        rows.append((d, deep, tip, bk, direct))
    return np.array(rows), rho

if __name__ == "__main__":
    for n in [int(x) for x in sys.argv[1:]] or [1000, 2000, 4000]:
        seeds = range(1, 13)
        Rs = [run(n, 100, s)[0] for s in seeds]                    # pairs within one sprinkling are correlated: errors from the seed spread (lesson 8)
        ell = (2 * n) ** -0.5
        print(f"N = {n}: 100 middle-band pairs x {len(Rs)} seeds, ell = {ell:.4f}; mean over seeds of the per-seed mean, +- s.e. from the seed spread")
        for lo, hi in BINS:
            cells = []
            for j, name in enumerate(NAMES, 1):
                m1, m2, md = [], [], []
                for R in Rs:
                    m = (R[:, 0] / ell >= lo) & (R[:, 0] / ell < hi) & np.isfinite(R[:, j])
                    if m.sum() < 3:
                        continue
                    r = R[m, j] / R[m, 0]
                    m1.append(np.mean(r - 1)); m2.append(np.mean(r ** 2 - 1)); md.append(np.median(np.abs(r - 1)))
                se = lambda x: np.std(x, ddof=1) / np.sqrt(len(x))
                cells.append(f"{name} d {np.mean(m1):+.3f}({se(m1):.3f}) d2 {np.mean(m2):+.3f}({se(m2):.3f}) med|.| {np.mean(md):.3f}")
            print(f"  d/ell {lo}-{hi if hi < 1e8 else 'inf'}: " + "  ".join(cells), flush=True)
