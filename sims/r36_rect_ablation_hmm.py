"""1+1 distance estimators: ablation and the Hu-Meyer-Meyer construction (session 17; external referee round 1 on toolkit-1p1-v1, Majors 1-2).
Same universes and pairs as r31 (same seed, same rng calls: sprinkle, then the pair draws), so the r31 columns reproduce exactly. Per pair, d from:
  rect_deep      2 N_A N_B / (rho (N_C + 1)), deepest c (the paper's Eq. 4)                   [r31]
  rect_deep_raw  2 N_A N_B / (rho N_C), same c, NO Poisson correction                        <- ablation (b): general c without the correction
  bk             Bogun~a-Krioukov equal-depth filter (their Eq. 34) and overlap formula     [r31]
  bk_c_rect      the SAME equal-depth c's, our corrected formula, d averaged over them      <- ablation (a): equal depth with the correction
  bk_c_raw       the same c's, uncorrected 2 N_A N_B / (rho N_C)                           <- isolates the formula (BK's overlap form vs the rectangle form)
  direct         smallest past-future interval (Brightwell-Gregory, Rideout-Wallden)          [r31]
  hmm_best       Hu-Meyer-Meyer (J. Math. Phys. 66, 122502, Sec. 2): p < a, b < q with all four proper times equal to s gives
                 d^2 = tau_pq^2 - 4 s^2. On the causal set tau^2 = 2 N / rho (N strictly between; N_pq minus a and b); p from the common past,
                 q from the common future, the pair (p, q) whose four counts N_pa, N_pb, N_aq, N_bq agree best (chi^2 = sum (N_i - mean)^2 / mean);
                 s^2 from the mean of the four.
  hmm_avg        d^2 averaged over every (p, q) whose four counts agree within Poisson noise (chi^2 < 3, three degrees of freedom); hmm_best if none.
  hmm_shallow    among the same Poisson-matched (p, q), the one with the smallest mean count (smallest s: B^2 - 4 s^2 is a difference of two
                 noisy numbers whose variance grows with s); hmm_best if none.
d^2 can come out negative for hmm (difference of noisy counts): d = sign * sqrt|d^2| kept for the bias of d^2, |.| for the median error.
Usage: python r36_rect_ablation_hmm.py [N ...]
"""
import sys
import numpy as np
from s4a_overlap_distance import sprinkle, causal, pair_counts

BINS = ((0, 2), (2, 10), (10, 1e9))
NAMES = ("rect_deep", "rect_deep_raw", "bk", "bk_c_rect", "bk_c_raw", "direct", "hmm_best", "hmm_avg", "hmm_shallow")

def bk_filter(nA, nB, nC):
    """BK's second filter (their Eq. 34), as s4a.est_bk; returns the mask and BK's own d per selected c (times sqrt(rho) still to apply)."""
    nAC, nBC = nA + nC, nB + nC
    O = nC / (np.minimum(nA, nB) + nC)
    ok = (np.abs(nAC - nBC) < 0.5 * np.sqrt(nAC + nBC) * np.sqrt(np.clip(1 - O, 0, None))) & (nC > 0)
    return ok, O, nAC, nBC

def run(n, n_pairs, seed):
    rng = np.random.default_rng(seed)
    u, v = sprinkle(n, rng)
    u = np.concatenate([[0.0], u]); v = np.concatenate([[0.0], v])          # element 0 = bottom tip, as r31
    rho = 2 * n
    C = causal(u, v); C[0, 1:] = 1
    with np.errstate(all="ignore"):
        K = C @ C
    Kf = K.astype(float)
    mid = np.flatnonzero((u + v > 0.8) & (u + v < 1.2))
    rows = []
    sq = lambda d2: np.sign(d2) * np.sqrt(np.abs(d2))
    while len(rows) < n_pairs:
        a, b = rng.choice(mid, 2, replace=False)
        du, dv = u[b] - u[a], v[b] - v[a]
        if du * dv >= 0:
            continue
        d = np.sqrt(-du * dv)
        nA, nB, nC = pair_counts(C, K, a, b)
        nA, nB, nC = nA.astype(float), nB.astype(float), nC.astype(float)
        cs = np.flatnonzero(C[:, a] * C[:, b])
        k = np.argmax(nC)
        deep = np.sqrt(2 * nA[k] * nB[k] / (rho * (nC[k] + 1)))
        raw = np.sqrt(2 * nA[k] * nB[k] / (rho * nC[k])) if nC[k] > 0 else np.nan
        ok, O, nAC, nBC = bk_filter(nA, nB, nC)
        if ok.any():
            tau = np.sqrt(2 * 0.5 * (nAC[ok] + nBC[ok]) / rho)
            bk = np.mean(tau * (1 - O[ok]) / np.sqrt(O[ok]))
            bkr = np.mean(np.sqrt(2 * nA[ok] * nB[ok] / (rho * (nC[ok] + 1))))
            bkw = np.mean(np.sqrt(2 * nA[ok] * nB[ok] / (rho * nC[ok])))
        else:
            bk = bkr = bkw = np.nan
        F = np.flatnonzero(C[a] * C[b])
        direct = np.sqrt(2 * max(K[np.ix_(cs, F)].min() - 2, 0) / rho) if len(F) else np.nan
        hb = ha = hs = np.nan
        if len(F):
            P4 = np.stack(np.broadcast_arrays(Kf[cs, a][:, None], Kf[cs, b][:, None], Kf[a, F][None, :], Kf[b, F][None, :]))   # (4, |past|, |future|)
            m = P4.mean(0)
            chi = ((P4 - m) ** 2).sum(0) / np.maximum(m, 1)
            Npq = np.maximum(Kf[np.ix_(cs, F)] - 2, 0)                     # a and b lie inside I(p, q)
            d2 = 2 * Npq / rho - 4 * 2 * m / rho
            good = m >= 1
            if good.any():
                i = np.argmin(np.where(good, chi, np.inf))
                hb = sq(d2.flat[i])
                sel = good & (chi < 3)
                ha = sq(d2[sel].mean()) if sel.any() else hb
                hs = sq(d2.flat[np.argmin(np.where(sel, m, np.inf))]) if sel.any() else hb
        rows.append((d, deep, raw, bk, bkr, bkw, direct, hb, ha, hs))
    return np.array(rows), rho

if __name__ == "__main__":
    for n in [int(x) for x in sys.argv[1:]] or [1000, 4000]:
        Rs = [run(n, 100, s)[0] for s in range(1, 13)]                    # r31's seeds; errors from the seed spread (lesson 8)
        ell = (2 * n) ** -0.5
        print(f"N = {n}: 100 middle-band pairs x {len(Rs)} seeds, ell = {ell:.4f}; bias of d^2 in % (s.e. over seeds), median |rel. error of d|, share of pairs with an estimate")
        for lo, hi in BINS:
            print(f"  d/ell {lo}-{hi if hi < 1e8 else 'inf'}:")
            for j, name in enumerate(NAMES, 1):
                m2, md, cov = [], [], []
                for R in Rs:
                    inb = (R[:, 0] / ell >= lo) & (R[:, 0] / ell < hi)
                    m = inb & np.isfinite(R[:, j])
                    if m.sum() < 3:
                        continue
                    r = R[m, j] / R[m, 0]
                    m2.append(np.mean(np.sign(r) * r ** 2 - 1)); md.append(np.median(np.abs(np.abs(r) - 1))); cov.append(m.sum() / max(inb.sum(), 1))
                se = np.std(m2, ddof=1) / np.sqrt(len(m2)) if len(m2) > 1 else np.nan
                print(f"    {name:14s} d2 bias {100 * np.mean(m2):+6.1f} ({100 * se:4.1f})   median err {np.mean(md):.3f}   coverage {np.mean(cov):.2f}", flush=True)
