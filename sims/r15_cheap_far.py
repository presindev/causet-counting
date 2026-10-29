"""Cheaper far-pair distances for the switch estimator (idea 005, session 11). The switch (r13) keeps Johnston's full min-plus detour for far pairs, an O(n^3)
step without BLAS (76 s at n = 4000 on the laptop vs 3 s for our step). Two cheaper detours, each O(n^2 K):
    (a) random stepping stones: r(x, y) = min over K random z of R_xz + R_zy;
    (b) two passes: a rough map from our estimate alone, then stepping stones only from the grid cells (in the rough map's space) holding the points at 1/4, 1/2, 3/4
        of the way from x to y. Good stones lie near the segment, so chosen stones should beat random ones at the same count.
Close pairs (our estimate < L = 0.25) always use ours. R = his related-pair spatial separation from t and tau (inf if unrelated), as in Johnston 2025.
Compared with the full switch and full Johnston on the same universes; spatial corr (his Table V metric).
Usage: python r15_cheap_far.py [polish]   (polish: (b) only, with the 27-cell widening)
"""
import sys
import time
import numpy as np
from r11_4d_distance import load_table
from r12_johnston_compare import johnston, C4
from r13_mixed import ours_spatial, embed_from_r, sprinkle

np.seterr(all="ignore")
L = 0.25

def related_R(C, rho, T=1.0):
    """The first half of johnston(): time coordinate t and R (spatial separation of related pairs, inf otherwise), without the min-plus."""
    Cf = C.astype(np.float32)
    N = Cf @ Cf
    rel = C | C.T
    tau = np.where(rel, (N / (rho * C4)) ** 0.25, 0.0)
    tau = np.maximum(tau, tau.T)
    t = T / 2 + (tau[0] ** 2 - tau[:, -1] ** 2) / (2 * T)
    t[0], t[-1] = 0.0, T
    R = np.where(rel, np.sqrt(np.abs((t[:, None] - t[None, :]) ** 2 - tau ** 2)), np.inf)
    np.fill_diagonal(R, 0.0)
    return R, t

def detour(R, I, J, Z, chunk=20000):
    """min over z in Z of R[I, z] + R[z, J], pair by pair (Z: one candidate set shared by all these pairs)."""
    out = np.empty(len(I))
    RZ = R[:, Z]
    for s in range(0, len(I), chunk):
        out[s:s + chunk] = np.min(RZ[I[s:s + chunk]] + RZ[J[s:s + chunk]], axis=1)   # R symmetric: R[z, J] = R[J, z]
    return out

def detour_safe(R, I, J, Z):
    """detour() over Z; pairs with no stone in Z related to both (inf) get the full detour over all events. Returns (estimate, share sent to the full detour)."""
    out = detour(R, I, J, Z)
    bad = ~np.isfinite(out)
    if bad.any():
        out[bad] = detour(R, I[bad], J[bad], np.arange(len(R)), chunk=1000)
    return out, bad.mean() if len(bad) else 0.0

def assemble(R, S, I, J, far_est):
    r = np.where(np.isfinite(R), R, 0.0)
    est = np.where(np.isfinite(S[I, J]) & (S[I, J] < L), S[I, J], far_est)
    r[I, J] = est; r[J, I] = est
    return r

def two_pass(R, S, t, I, J, far, G, rng, widen=True):
    """(b): rough map from ours alone (random-K detour where our counts are zero), then stepping stones from the grid cells around the segment."""
    s_ij = S[I, J]
    miss = ~np.isfinite(s_ij)
    fill = s_ij.copy()
    if miss.any():                                              # ~5 % of pairs (edge events with empty pasts/futures): full detour for these only
        fill[miss] = detour(R, I[miss], J[miss], np.arange(len(R)), chunk=1000)
    Y = embed_from_r(assemble(R, S, I, J, fill), t)[:, 1:]          # rough map: our estimate for every spacelike pair
    lo, hi = np.percentile(Y, 1, axis=0), np.percentile(Y, 99, axis=0)   # robust to a few outliers
    cell = lambda p: tuple(np.clip(((p - lo) / (hi - lo) * G).astype(int), 0, G - 1).T)
    ev_cell = np.ravel_multi_index(cell(Y), (G, G, G))
    If, Jf = I[far], J[far]
    best = np.full(len(If), np.inf)
    ncand = []
    for f in (0.25, 0.5, 0.75):
        pc = np.ravel_multi_index(cell(Y[If] + f * (Y[Jf] - Y[If])), (G, G, G))
        order = np.argsort(pc)
        bounds = np.searchsorted(pc[order], np.arange(G ** 3 + 1))
        for c in range(G ** 3):
            sel = order[bounds[c]:bounds[c + 1]]
            Z = np.flatnonzero(ev_cell == c)
            if len(sel) == 0 or len(Z) == 0:
                continue
            ncand.append((len(sel), len(Z)))
            best[sel] = np.minimum(best[sel], detour(R, If[sel], Jf[sel], Z))
    w = np.array(ncand)
    bad = ~np.isfinite(best)
    nb_share = bad.mean()
    if bad.any() and widen:                                     # polish: no related stone in the three cells -> the 3x3x3 block around the midpoint
        pts = np.clip(((Y[If[bad]] + 0.5 * (Y[Jf[bad]] - Y[If[bad]]) - lo) / (hi - lo) * G).astype(int), 0, G - 1)
        ev = np.clip(((Y - lo) / (hi - lo) * G).astype(int), 0, G - 1)
        bi = np.flatnonzero(bad)
        key = np.ravel_multi_index(tuple(pts.T), (G, G, G))
        for c in np.unique(key):
            sel = bi[key == c]
            cc = np.array(np.unravel_index(c, (G, G, G)))
            Z = np.flatnonzero((np.abs(ev - cc) <= 1).all(1))
            if len(Z) == 0:
                continue
            best[sel] = np.minimum(best[sel], detour(R, If[sel], Jf[sel], Z))
        bad = ~np.isfinite(best)
    if bad.any():
        best[bad] = detour(R, If[bad], Jf[bad], np.arange(len(R)), chunk=1000)
    return best, (w[:, 0] * w[:, 1]).sum() / len(If), bad.mean(), miss.mean(), nb_share            # mean stones tried per far pair (over the three cells)

if __name__ == "__main__":
    W = load_table()
    rng = np.random.default_rng(4242)
    Ks, Gs = (30, 100, 300), (4, 6, 8)
    if len(sys.argv) > 1 and sys.argv[1] == "polish":
        Ks, Gs = (), (4, 6, 8)
    print("Cheap far-pair detours in the switch (L = 0.25). Spatial corr; paired difference vs full Johnston; far-step time; stones per far pair")
    for n, reps in ((1500, 4), (3000, 2)):
        rows, times, stones, fulls = [], [], [], []
        for _ in range(reps):
            P, C, rho = sprinkle(n, rng)
            iu = np.triu_indices(len(P), 1)
            st = np.sqrt(((P[:, None, 1:] - P[None, :, 1:]) ** 2).sum(-1))[iu]
            sc = lambda X: np.corrcoef(np.sqrt(((X[:, None, 1:] - X[None, :, 1:]) ** 2).sum(-1))[iu], st)[0, 1]
            t0 = time.time(); r_j, Xj = johnston(C, rho, 1.0); tj = time.time() - t0
            R, t = related_R(C, rho)
            S = ours_spatial(C, rho, t, W)
            sp = ~np.isfinite(R[iu])
            I, J = iu[0][sp], iu[1][sp]
            far = ~(np.isfinite(S[I, J]) & (S[I, J] < L))
            ss_a = []
            row, tt, ss = [sc(Xj), sc(embed_from_r(assemble(R, S, I, J, r_j[I, J]), t))], [tj], []
            for K in Ks:
                t0 = time.time()
                fe = np.full(len(I), np.nan)
                fe[far], full = detour_safe(R, I[far], J[far], rng.choice(len(P), K, replace=False))
                tt.append(time.time() - t0); ss_a.append(full)
                row.append(sc(embed_from_r(assemble(R, S, I, J, fe), t)))
            for G in Gs:
                t0 = time.time()
                fe = np.full(len(I), np.nan)
                b, m, full, miss, nb = two_pass(R, S, t, I, J, far, G, rng)
                fe[far] = b
                tt.append(time.time() - t0); ss.append((m, full, miss, nb))
                row.append(sc(embed_from_r(assemble(R, S, I, J, fe), t)))
            rows.append(row); times.append(tt); stones.append(ss); fulls.append(ss_a)
        A, Tm, Sm, Fa = np.array(rows), np.mean(times, 0), np.mean(stones, 0), np.mean(fulls, 0)
        d = A - A[:, :1]
        se = lambda k: d[:, k].std(ddof=1) / np.sqrt(reps)
        labels = ["johnston (full min-plus)", "switch, full detour"] + [f"switch, (a) K={K}" for K in Ks] + [f"switch, (b) G={G}" for G in Gs]
        print(f"  n = {n} ({reps} univ.), far pairs {far.mean():.0%} of spacelike")
        for k, lab in enumerate(labels):
            extra = ""
            if k == 0:
                extra = f"   time {Tm[0]:.1f} s"
            elif k >= 2:
                extra = f"   far-step time {Tm[k - 1]:.1f} s"
            if 2 <= k < 2 + len(Ks):
                extra += f"   sent to full detour {Fa[k - 2]:.1%}"
            if k >= 2 + len(Ks):
                m, full, miss, nb = Sm[k - 2 - len(Ks)]
                extra += f"   stones/pair {m:.0f}, no stone in 3 cells {nb:.1%}, after 27-cell block {full:.1%} -> full detour (+ rough-map zero counts {miss:.1%})"
            print(f"    {lab:<26} {A[:, k].mean():.4f}  ({d[:, k].mean():+.4f} +- {se(k):.4f}){extra}", flush=True)
