"""Low-count oracle on JOHNSTON's own spacelike values (session 15; PRD referee item: r18's k < K oracle replaced OUR distances, so it located the
error of the overlap embedding, not of his). Same universes as r18 (seed 2028 by default). k = shared count on the side the overlap estimator uses.
Arms, all in his pipeline (his t, his related-pair R, classical MDS):
    johnston          : his detours everywhere
    J_truth_lowK      : TRUE distance on the k < K pairs, his detours elsewhere   -> how much of his residual sits on low-count pairs
    J_truth_highK     : TRUE distance on the k >= K pairs, his detours on k < K   -> what is left if only the low-count pairs stay his
    J_truth_all       : TRUE on every spacelike pair (r12's oracle; sanity check, ~0.9999)
Usage: python r30_johnston_lowk_oracle.py [n reps seed]
"""
import sys
import numpy as np
from r11_4d_distance import load_table
from r12_johnston_compare import johnston
from r13_mixed import embed_from_r, sprinkle
from r18_waist_oracle import ours_with_counts, sym

np.seterr(all="ignore")
KS = (10, 30)

def run(n, reps, seed):
    W = load_table()
    rng = np.random.default_rng(seed)
    names = ["johnston"] + [f"{a}_K{K}" for K in KS for a in ("J_truth_lowK", "J_truth_highK")] + ["J_truth_all"]
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
        row = {"johnston": sc(Xj), "J_truth_all": sc(embed_from_r(sym(r_j, I, J, tr), t))}
        sh = []
        for K in KS:
            w = k < K
            sh.append(w.mean())
            row[f"J_truth_lowK_K{K}"] = sc(embed_from_r(sym(r_j, I, J, np.where(w, tr, rj)), t))
            row[f"J_truth_highK_K{K}"] = sc(embed_from_r(sym(r_j, I, J, np.where(w, rj, tr)), t))
        rows.append([row[a] for a in names]); shares.append(sh)
        print(f"  universe {len(rows)}: " + "  ".join(f"{a} {row[a]:.4f}" for a in names), flush=True)
    A = np.array(rows); d = A - A[:, :1]
    print(f"n = {n} ({reps} univ., seed {seed}); low-count share of spacelike pairs for K = {KS}: " + ", ".join(f"{v:.3f}" for v in np.mean(shares, 0)))
    print("  arm                  spatial corr   vs johnston (paired)   share of his residual")
    for a, m, dm, de in zip(names, A.mean(0), d.mean(0), d.std(0, ddof=1) / np.sqrt(reps) if reps > 1 else np.full(len(names), np.nan)):
        print(f"  {a:20s} {m:.4f}         {dm:+.4f} +- {de:.4f}        {dm / (1 - A[:, 0].mean()):+5.0%}")

if __name__ == "__main__":
    a = sys.argv[1:]
    run(int(a[0]) if a else 1500, int(a[1]) if len(a) > 1 else 3, int(a[2]) if len(a) > 2 else 2028)
