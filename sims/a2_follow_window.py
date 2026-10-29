"""A2 branch C (idea 004, session 6): past stability along the window, beta = beta*(N).

beta*(N, eps) = the beta in [0, 16] where the quantum growth-path sum's AGE distribution is closest (total variation, TV)
to the AGE distribution of a sprinkled 2D spacetime (uniform 2D orders, classical, beta = 0): "the growth sum looks most
like spacetime here". At beta*(N) report: TV(AGE), TV(PRESENT) against the same reference (a check that AGE alone isn't
fooling us), and P_N of the stem questions (Q1 more than one origin, Q3 3-chain stem) as in a2_past_stability.py.
Usage: python a2_follow_window.py [Nmax]
"""
import sys
import numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from a2_growth_paths import grow_all
from s3q_exact_quantum import enumerate_universes
from a2_past_stability import p_quantum

def dist_q(S, rec, beta, vals):
    a = np.exp(1j * beta * S)
    A = np.array([abs(a[rec == r].sum()) ** 2 for r in vals])
    return A / A.sum()

def dist_c(rec, vals):
    return np.array([(rec == r).mean() for r in vals])

if __name__ == "__main__":
    Nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    betas = np.arange(0, 16.01, 0.1)
    for eps in (0.15, 0.21, 0.3):
        print(f"\neps = {eps}")
        print("  N  beta*   TV(AGE)  TV(PRESENT)  TV(PRESENT) at beta=0   P(Q1 >1 origin)  P(Q3 3-chain stem)")
        for N in range(4, Nmax + 1):
            S, age, pres, q = grow_all(N, eps, stems=True)
            S2, a2, p2 = enumerate_universes(N, eps)
            vals = np.arange(1, N + 1)
            ref_a, ref_p = dist_c(a2, vals), dist_c(p2, vals)
            tv = [0.5 * abs(dist_q(S, age, b, vals) - ref_a).sum() for b in betas]
            b = betas[int(np.argmin(tv))]
            tvp = 0.5 * abs(dist_q(S, pres, b, vals) - ref_p).sum()
            tvp0 = 0.5 * abs(dist_q(S, pres, 0, vals) - ref_p).sum()
            print(f" {N:2d}  {b:5.1f}   {min(tv):.3f}     {tvp:.3f}        {tvp0:.3f}             "
                  f"{p_quantum(S, q[:, 0], b):.3f}            {p_quantum(S, q[:, 2], b):.3f}", flush=True)
