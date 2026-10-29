"""(c) Map from trusted distances only (idea 005, session 11). No detours: every number comes from counting.
Trusted spatial separations:
    related pairs   : R = sqrt|dt^2 - tau^2|, t and tau from interval counts (as in Johnston 2025; the oracle showed these are not the bottleneck);
    close spacelike : our shared-past estimate, when it says < L (0.25; the regime where it beats his detour).
Far spacelike pairs (our estimate >= L, or zero counts) are left out entirely. Time coordinate t is fixed; the 3 spatial coordinates Y are fitted by weighted
stress majorization (SMACOF, Jacobi form): Y_i <- (sum_j w_ij [Y_j + D_ij (Y_i - Y_j)/|Y_i - Y_j|]) / sum_j w_ij, which never increases the weighted stress
sum_ij w_ij (|Y_i - Y_j| - D_ij)^2 [literature: de Leeuw's majorization; this local form is the standard one for sensor-network localization].
Start: the rough map from ours alone (far spacelike pairs from our estimate; full detour only for the ~2 % with zero counts, as in r15).
Weights: w = 1 or 1/D (local pairs count more). Compared with Johnston and the switch on the same universes; spatial corr (his Table V metric).
Usage: python r16_local_fit.py [scan|holdout]   (scan: trust ours to L = 0.35 / 0.5, or keep far pairs with weight 0.1 / 0.3)
"""
import sys
import time
import numpy as np
from r11_4d_distance import load_table
from r12_johnston_compare import johnston
from r13_mixed import ours_spatial, embed_from_r, sprinkle
from r15_cheap_far import related_R, assemble, detour

np.seterr(all="ignore")
L = 0.25
SCAN = len(sys.argv) > 1 and sys.argv[1] == "scan"

def smacof(Y, D, Wt, iters=300, tol=1e-6):
    """Weighted stress majorization on the spatial coordinates; D, Wt dense n x n (Wt = 0 where untrusted)."""
    ws = Wt.sum(1)
    ws[ws == 0] = 1.0
    prev = np.inf
    for k in range(iters):
        sq = (Y ** 2).sum(1)
        dist = np.sqrt(np.maximum(sq[:, None] + sq[None, :] - 2 * Y @ Y.T, 0.0))   # Gram form: no n x n x 3 temporary (cluster, n = 15000)
        B = np.where(dist > 1e-12, Wt * D / np.maximum(dist, 1e-12), 0.0)
        Y = (Wt @ Y + (B.sum(1)[:, None] * Y - B @ Y)) / ws[:, None]
        if k % 10 == 0:
            stress = (Wt * (dist - D) ** 2).sum()
            if prev - stress < tol * prev:
                break
            prev = stress
    return Y, k

def part_main():
    W = load_table()
    rng = np.random.default_rng(99)
    print("(c) fit to trusted distances only (related pairs + our close spacelike pairs < L = 0.25). Spatial corr; paired difference vs Johnston")
    for n, reps in ((1500, 3), (3000, 2)):
        rows, tms, its = [], [], []
        for _ in range(reps):
            P, C, rho = sprinkle(n, rng)
            iu = np.triu_indices(len(P), 1)
            st = np.sqrt(((P[:, None, 1:] - P[None, :, 1:]) ** 2).sum(-1))[iu]
            sc = lambda X: np.corrcoef(np.sqrt(((X[:, None, 1:] - X[None, :, 1:]) ** 2).sum(-1))[iu], st)[0, 1]
            r_j, Xj = johnston(C, rho, 1.0)
            R, t = related_R(C, rho)
            S = ours_spatial(C, rho, t, W)
            sp = ~np.isfinite(R[iu]); I, J = iu[0][sp], iu[1][sp]
            s_ij = S[I, J]
            close = np.isfinite(s_ij) & (s_ij < L)
            switch = sc(embed_from_r(assemble(R, S, I, J, r_j[I, J]), t))
            fill = s_ij.copy(); miss = ~np.isfinite(fill)
            fill[miss] = detour(R, I[miss], J[miss], np.arange(len(R)), chunk=1000)
            X0 = embed_from_r(assemble(R, S, I, J, fill), t)                  # rough map: ours alone
            D = np.where(np.isfinite(R), R, 0.0)
            T = np.isfinite(R).astype(float); np.fill_diagonal(T, 0.0)          # trusted: related pairs ...
            D[I[close], J[close]] = s_ij[close]; D[J[close], I[close]] = s_ij[close]
            T[I[close], J[close]] = 1.0; T[J[close], I[close]] = 1.0            # ... and close spacelike pairs
            row, tt, it = [sc(Xj), switch, sc(X0)], [], []
            variants = [("w=1", T), ("w=1/D", T / np.maximum(D, 0.02))]
            if SCAN:
                variants = []
                for Lc, wfar in ((0.35, 0.0), (0.5, 0.0), (0.25, 0.1), (0.25, 0.3)):
                    D2, T2 = D.copy(), T.copy()
                    ok = np.isfinite(s_ij)
                    tr = ok & (s_ij < Lc)
                    D2[I[ok], J[ok]] = s_ij[ok]; D2[J[ok], I[ok]] = s_ij[ok]
                    wv = np.where(tr, 1.0, wfar)[ok]
                    T2[I[ok], J[ok]] = wv; T2[J[ok], I[ok]] = wv
                    variants.append((f"L={Lc}, far w={wfar}", T2, D2))
            for v in variants:
                wname, Wt = v[0], v[1]
                Dv = v[2] if len(v) > 2 else D
                t0 = time.time()
                Y, k = smacof(X0[:, 1:].copy(), Dv, Wt)
                tt.append(time.time() - t0); it.append(k)
                row.append(sc(np.column_stack([t, Y])))
            rows.append(row); tms.append(tt); its.append(it)
        A = np.array(rows); d = A - A[:, :1]
        se = lambda k: d[:, k].std(ddof=1) / np.sqrt(reps)
        print(f"  n = {n} ({reps} univ.); trusted pairs: related {np.isfinite(R[iu]).mean():.0%} of all, close spacelike {close.mean():.0%} of spacelike")
        labs = ["(c) L=0.35", "(c) L=0.5", "(c) L=.25, far w=0.1", "(c) L=.25, far w=0.3"] if SCAN else ["(c) fit, w=1", "(c) fit, w=1/D"]
        for k, lab in enumerate(["johnston", "switch (full detour)", "ours alone (start)"] + labs):
            ex = f"   fit time {np.mean(tms, 0)[k - 3]:.1f} s, iterations {np.mean(its, 0)[k - 3]:.0f}" if k >= 3 else ""
            print(f"    {lab:<22} {A[:, k].mean():.4f}  ({d[:, k].mean():+.4f} +- {se(k):.4f}){ex}   per universe " + " ".join(f"{x:+.3f}" for x in d[:, k]), flush=True)


def fit_c(R, S, t, I, J, Lc=0.25, wfar=0.1, detour_init=True, iters=300):
    """(c) as adopted after the scan: trusted = related pairs (weight 1) + our spacelike estimate < Lc (weight 1); our far estimates kept with weight wfar;
    zero-count pairs (no estimate): weight 0. Start: the rough map from ours alone; zero-count pairs there get the full detour (detour_init) or, with no
    detour anywhere, the median of our estimates. Returns the (t, Y) map."""
    s_ij = S[I, J]
    ok = np.isfinite(s_ij)
    fill = s_ij.copy()
    if detour_init:
        fill[~ok] = detour(R, I[~ok], J[~ok], np.arange(len(R)), chunk=1000)
    else:
        fill[~ok] = np.median(s_ij[ok])
    X0 = embed_from_r(assemble(R, S, I, J, fill), t)
    D = np.where(np.isfinite(R), R, 0.0)
    T = np.isfinite(R).astype(float); np.fill_diagonal(T, 0.0)
    D[I[ok], J[ok]] = s_ij[ok]; D[J[ok], I[ok]] = s_ij[ok]
    wv = np.where(s_ij[ok] < Lc, 1.0, wfar)
    T[I[ok], J[ok]] = wv; T[J[ok], I[ok]] = wv
    Y, k = smacof(X0[:, 1:].copy(), D, T, iters)
    return np.column_stack([t, Y])

def part_holdout():
    W = load_table()
    rng = np.random.default_rng(2026)
    variants = [("w_far=0.1", 0.1, True), ("w_far=0.2", 0.2, True), ("w_far=0.1, no detour", 0.1, False)]
    print("(c) holdout (fresh seed 2026): fit to related + close ours (w=1) + far ours (w_far). Spatial / Minkowski corr; paired spatial difference vs Johnston")
    from r12_johnston_compare import mink
    for n, reps in ((1500, 5), (3000, 3)):
        rows = []
        for _ in range(reps):
            P, C, rho = sprinkle(n, rng)
            iu = np.triu_indices(len(P), 1)
            st = np.sqrt(((P[:, None, 1:] - P[None, :, 1:]) ** 2).sum(-1))[iu]; mt = mink(P)[iu]
            sc = lambda X: [np.corrcoef(np.sqrt(((X[:, None, 1:] - X[None, :, 1:]) ** 2).sum(-1))[iu], st)[0, 1], np.corrcoef(mink(X)[iu], mt)[0, 1]]
            r_j, Xj = johnston(C, rho, 1.0)
            R, t = related_R(C, rho)
            S = ours_spatial(C, rho, t, W)
            sp = ~np.isfinite(R[iu]); I, J = iu[0][sp], iu[1][sp]
            row = sc(Xj) + sc(embed_from_r(assemble(R, S, I, J, r_j[I, J]), t))
            for _, wf, di in variants:
                row += sc(fit_c(R, S, t, I, J, 0.25, wf, di))
            rows.append(row)
        A = np.array(rows)
        print(f"  n = {n} ({reps} univ.)")
        for k, lab in enumerate(["johnston", "switch"] + [v[0] for v in variants]):
            d = A[:, 2 * k] - A[:, 0]
            print(f"    {lab:<22} {A[:, 2 * k].mean():.4f} / {A[:, 2 * k + 1].mean():.4f}   ({d.mean():+.4f} +- {d.std(ddof=1) / np.sqrt(reps):.4f})"
                  f"   per universe " + " ".join(f"{x:+.3f}" for x in d), flush=True)

if __name__ == "__main__":
    part_holdout() if len(sys.argv) > 1 and sys.argv[1] == "holdout" else part_main()
