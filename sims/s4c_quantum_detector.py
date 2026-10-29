"""Stage S4c (ideas 002, 005): does quantum interference favour manifold-like universes? (pilot, N ~ 100)

Exact sums stop at N ~ 12, where the detector can't tell flat from crystal. Instead, sample random 2D orders
(uniform = the beta = 0 ensemble) and reweight:
    A_r = sum_{universes with record r} e^{i beta S}  ~  N!^2 * mean_uniform[ e^{i beta S} 1_r ]
Record r [ours]: the bin of the detector's stress (quartiles of the uniform ensemble), i.e. "how manifold-like".
Universes with the same record interfere (lesson 3):  P_q(r) = |A_r|^2 / sum_r |A_r|^2.
Classical comparison by reweighting: P_c(r) = sum_r e^{-beta S} / sum e^{-beta S} (unreliable once rare
low-action universes dominate: they are never sampled).
Feasibility: |mean e^{i beta S}| ~ exp(-beta^2 sd_S^2 / 2), sd_S ~ 7 at N = 100, so beta <~ 0.4.
Note: |A_r| <= (number of universes in r). Rare classes can only win by the common ones cancelling.
"""
import sys
import numpy as np
from s3a_mcmc_2d import f_weights, action
from s4b_detector import diagnostics

np.seterr(all="ignore")                           # numpy 2.0 + Accelerate emits spurious matmul warnings

def sample(N, n, eps, seed):
    rng = np.random.default_rng(seed)
    fw = f_weights(N, eps)
    S, stress, rpos = np.empty(n), np.empty(n), np.empty(n)
    for k in range(n):
        u, v = rng.permutation(N), rng.permutation(N)
        S[k], C = action(u, v, eps, fw)
        d = diagnostics(C > 0)
        stress[k], rpos[k] = d[3], d[1]
    return S, stress, rpos

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    n_batch = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    eps, batches = 0.21, [sample(N, n_batch, 0.21, seed) for seed in (1, 2, 3, 4)]
    allstress = np.concatenate([b[1] for b in batches])
    edges = np.quantile(allstress, [0.25, 0.5, 0.75])
    print(f"N = {N}, {len(batches)} x {n_batch} uniform 2D orders; stress quartile edges {edges.round(3)}")
    print("record = stress quartile (Q1 most manifold-like ... Q4 least); beta = 0 gives 0.25 each")
    for beta in (0.0, 0.1, 0.2, 0.3, 0.4):
        Pq, Pc, ph = [], [], []
        for S, stress, _ in batches:
            rec = np.digitize(stress, edges)
            amp = np.exp(1j * beta * S)
            A = np.array([amp[rec == r].sum() for r in range(4)])
            Pq.append(np.abs(A)**2 / (np.abs(A)**2).sum())
            w = np.exp(-beta * (S - S.min()))
            Pc.append(np.array([w[rec == r].sum() for r in range(4)]) / w.sum())
            ph.append(np.abs(amp.mean()))
        Pq, Pc = np.array(Pq), np.array(Pc)
        fq = "  ".join(f"{m:.2f}±{s:.2f}" for m, s in zip(Pq.mean(0), Pq.std(0)))
        fc = "  ".join(f"{m:.2f}" for m in Pc.mean(0))
        print(f"  beta={beta:.1f} |<phase>|={np.mean(ph):.3f}  quantum Q1..Q4: {fq}   classical: {fc}", flush=True)
