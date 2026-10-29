"""Waist-pair diagnostic (idea 005, session 12): is our embedding loss to Johnston 2025 caused by the few spacelike pairs whose shared past AND shared
future are both small (far pairs straddling the waist), and is it the distances or the embedding (classical MDS gives every pair the same voice)?

Per spacelike pair, k = shared count on the side we use (v1 pasts or vn futures, whichever has more events, as in r13.ours_spatial). "Waist" = k < K.
Arms, all in his pipeline (his t, his related-pair R, classical MDS via embed_from_r unless stated); spatial corr (his Table V metric):
    johnston      : his detours for every spacelike pair
    switch        : ours if our estimate < 0.25, else his detour (the published-candidate method)
    ours          : ours for every spacelike pair (his detour where we have no estimate)
    oracle_waist  : ours, but TRUE distance on waist pairs        -> if this beats him, the waist pairs' distances are the whole problem
    oracle_rest   : TRUE distance on non-waist pairs, ours on waist -> how much the waist pairs alone cost
    kswitch       : ours, but his detour on waist pairs (switch on the count, the error-profile variable; lesson 34)
    ours_wsmacof  : ours everywhere, embedding by SMACOF with weights k/(k + 30) (related pairs weight 1), started from the ours map
                    -> if this closes the gap, the embedding (not the distances) was the problem
Usage: python r18_waist_oracle.py [n reps seed]
"""
import sys
import numpy as np
from r11_4d_distance import load_table, dist_from_counts
from r12_johnston_compare import johnston
from r13_mixed import embed_from_r, sprinkle
from r16_local_fit import smacof

np.seterr(all="ignore")
KS = (10, 30, 100)

def ours_with_counts(C, rho, t, W):
    """As r13.ours_spatial (min_count = 1), but also returns k (shared count on the side used) for every spacelike pair."""
    n = len(C)
    Cf = C.astype(np.float32)
    past = Cf.copy(); past[0] = 0; past[-1] = 0
    fut = Cf.T.copy(); fut[0] = 0; fut[-1] = 0
    cp, cf = past.T @ past, fut.T @ fut
    npst, nfut = past.sum(0), fut.sum(0)
    iu = np.triu_indices(n, 1)
    sp = ~(C | C.T)[iu]
    I, J = iu[0][sp], iu[1][sp]
    use_p = np.minimum(npst[I], npst[J]) >= np.minimum(nfut[I], nfut[J])
    na = np.where(use_p, npst[I], nfut[I]); nb = np.where(use_p, npst[J], nfut[J]); nc = np.where(use_p, cp[I, J], cf[I, J])
    ok = np.minimum(na, nb) >= 1
    s = np.full(len(I), np.nan)
    d = dist_from_counts(W, na[ok], nb[ok], nc[ok], 1.0) / rho ** 0.25
    s[ok] = np.sqrt(d ** 2 + (t[I[ok]] - t[J[ok]]) ** 2)
    return I, J, s, nc

def sym(M, I, J, v):
    M = M.copy(); M[I, J] = v; M[J, I] = v
    return M

def run(n, reps, seed):
    W = load_table()
    rng = np.random.default_rng(seed)
    names = ["johnston", "switch", "ours"] + [f"{a}_K{K}" for K in KS for a in ("oracle_waist", "oracle_rest", "kswitch")] + ["ours_wsmacof"]
    rows, shares = [], []
    for _ in range(reps):
        P, C, rho = sprinkle(n, rng)
        iu = np.triu_indices(len(P), 1)
        Dtrue = np.sqrt(((P[:, None, 1:] - P[None, :, 1:]) ** 2).sum(-1))
        st = Dtrue[iu]
        sc = lambda X: np.corrcoef(np.sqrt(((X[:, None, 1:] - X[None, :, 1:]) ** 2).sum(-1))[iu], st)[0, 1]
        r_j, Xj = johnston(C, rho, 1.0)
        t = Xj[:, 0]
        I, J, s, k = ours_with_counts(C, rho, t, W)
        rj, tr = r_j[I, J], Dtrue[I, J]
        have = np.isfinite(s)
        ours = np.where(have, s, rj)
        row = {"johnston": sc(Xj),
               "switch": sc(embed_from_r(sym(r_j, I, J, np.where(have & (s < 0.25), s, rj)), t)),
               "ours": sc(embed_from_r(sym(r_j, I, J, ours), t))}
        sh = []
        for K in KS:
            w = k < K
            sh.append(w.mean())
            row[f"oracle_waist_K{K}"] = sc(embed_from_r(sym(r_j, I, J, np.where(w, tr, ours)), t))
            row[f"oracle_rest_K{K}"] = sc(embed_from_r(sym(r_j, I, J, np.where(w, ours, tr)), t))
            row[f"kswitch_K{K}"] = sc(embed_from_r(sym(r_j, I, J, np.where(w, rj, ours)), t))
        X0 = embed_from_r(sym(r_j, I, J, ours), t)
        D = sym(np.where(np.isfinite(r_j), r_j, 0.0), I, J, ours)
        Wt = sym(np.ones_like(r_j), I, J, np.where(have, k / (k + 30.0), 0.0)); np.fill_diagonal(Wt, 0.0)
        Y, _ = smacof(X0[:, 1:].copy(), D, Wt, 300)
        row["ours_wsmacof"] = sc(np.column_stack([t, Y]))
        rows.append([row[a] for a in names]); shares.append(sh)
        print(f"  universe {len(rows)}: johnston {row['johnston']:.4f}  ours {row['ours']:.4f}", flush=True)
    A = np.array(rows); d = A - A[:, :1]
    print(f"n = {n} ({reps} univ., seed {seed}); waist share of spacelike pairs for K = {KS}: " +
          ", ".join(f"{v:.3f}" for v in np.mean(shares, 0)))
    print("  arm                  spatial corr   vs johnston (paired)   share of his residual")
    for a, m, dm, de in zip(names, A.mean(0), d.mean(0), d.std(0, ddof=1) / np.sqrt(reps) if reps > 1 else np.full(len(names), np.nan)):
        print(f"  {a:20s} {m:.4f}         {dm:+.4f} +- {de:.4f}        {dm / (1 - A[:, 0].mean()):+5.0%}")

if __name__ == "__main__":
    a = sys.argv[1:]
    run(int(a[0]) if a else 1500, int(a[1]) if len(a) > 1 else 3, int(a[2]) if len(a) > 2 else 2028)
