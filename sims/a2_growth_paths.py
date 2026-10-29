"""A2 + C8, first exact test (idea 004, session 6): quantum sequential growth over ALL growth paths.

Each newborn f chooses any down-set D of the existing events as its past (internal temporality, C8: the choice of past is
what carries an amplitude). Per birth: e^{i beta dS_f}, dS_f = 4 eps - 8 eps^2 sum_{x<f} f(n_xf, eps) (clock-free, session 5).
A path's amplitude = e^{i beta S(C)}, independent of birth order (covariant). Paths = naturally labelled posets, so
  A_r = sum_{paths with record r} e^{i beta S}  = sum_C (number of natural labellings of C) e^{i beta S(C)}.
Unnormalized per step: a fixed-N sum, not a growth law with a sum rule (a per-step normalization breaks covariance).
Records (coarse, so different universes interfere; lesson 3): AGE = layers (longest chain), PRESENT = maximal events.
Compared with S3-quantum: 2D orders only, one term per permutation (sprinkling measure).
Usage: python a2_growth_paths.py [N] [eps]
"""
import sys
import numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from s3a_mcmc_2d import f_weights
from s3q_exact_quantum import enumerate_universes, distributions

def grow_all(N, eps, stems=False):
    """stems=True also returns covariant past questions per path: Q1 >= 2 minimal events (more than one origin),
    Q2 a 2-chain stem (an event whose whole past is one event), Q3 a 3-chain stem (whole past is a 2-chain)."""
    fw = f_weights(N, eps)
    S_out, age_out, pres_out, q_out = [], [], [], []
    popc = [bin(m).count("1") for m in range(1 << N)]

    def rec(n, past, up, h, S):
        if n == N:
            maximal = sum(1 for i in range(N) if up[i] == 0)
            S_out.append(S); age_out.append(max(h) + 1); pres_out.append(maximal)
            if stems:
                q1 = sum(1 for D in past if D == 0) >= 2
                q2 = any(popc[D] == 1 for D in past)
                q3 = any(popc[D] == 2 and any(past[i] == D & ~(1 << i) and past[i] for i in range(N) if D >> i & 1) for D in past)
                q_out.append((q1, q2, q3))
            return
        for D in range(1 << n):                        # candidate past of the newborn
            ok = True
            m = D
            while m:
                i = (m & -m).bit_length() - 1
                if past[i] & ~D:
                    ok = False; break
                m &= m - 1
            if not ok:
                continue
            dS = 4 * eps
            hf = 0
            m = D
            while m:
                i = (m & -m).bit_length() - 1
                dS -= 8 * eps ** 2 * fw[popc[D & up[i]]]
                hf = max(hf, h[i] + 1)
                m &= m - 1
            bit = 1 << n
            up2 = [up[i] | bit if D >> i & 1 else up[i] for i in range(n)] + [0]
            rec(n + 1, past + [D], up2, h + [hf], S + dS)

    rec(0, [], [], [], 0.0)
    if stems:
        return np.array(S_out), np.array(age_out), np.array(pres_out), np.array(q_out)
    return np.array(S_out), np.array(age_out), np.array(pres_out)

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    eps = float(sys.argv[2]) if len(sys.argv) > 2 else 0.21
    Sg, ag, pg = grow_all(N, eps)
    S2, a2, p2 = enumerate_universes(N, eps)
    print(f"N={N}, eps={eps}: {len(Sg)} growth paths (all posets); {len(S2)} permutations (2D orders)")
    for name, rg, r2 in [("AGE", ag, a2), ("PRESENT", pg, p2)]:
        print(f"\n record = {name}   (value: P_paths / P_2D-orders)")
        for beta in [0.0, 1.0, 2.0, 4.0, 8.0]:
            rs, Pq, _ = distributions(Sg, rg, beta)
            rs2, Pq2, _ = distributions(S2, r2, beta)
            d2 = dict(zip(rs2, Pq2))
            print(f"  beta={beta:3.1f}  mean {np.dot(rs, Pq):.2f} / {np.dot(rs2, Pq2):.2f}   "
                  + "  ".join(f"{r}:{q:.2f}/{d2.get(r, 0):.2f}" for r, q in zip(rs, Pq)))
