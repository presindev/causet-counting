"""A2 branch C test (idea 004, session 6): is the past stable as the universe grows? (Roberto's thermodynamic-limit criterion)

Fixed-N path sum (no per-step normalization; normalize once at the end, Z cancels in ratios). A covariant question about
the past ("stem" questions: once true, true forever) is a two-outcome record (lesson 3: paths with the same answer interfere):
  P_N(Q) = |A_yes|^2 / (|A_yes|^2 + |A_no|^2),   A = sum over growth paths of e^{i beta S}.
Questions: Q1 more than one origin (>= 2 minimal events); Q2 a 2-chain stem; Q3 a 3-chain stem.
Criterion: P_N(Q) should settle as N grows. Under a classical sum-rule growth, P_N of a stem question can only increase
(once true, true forever), so a falling P_N means the "past" is being rewritten by the present.
Usage: python a2_past_stability.py [Nmax]
"""
import sys
import numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from a2_growth_paths import grow_all

def p_quantum(S, yes, beta):
    a = np.exp(1j * beta * S)
    y, n = abs(a[yes].sum()) ** 2, abs(a[~yes].sum()) ** 2
    return y / (y + n) if y + n > 0 else np.nan

if __name__ == "__main__":
    Nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    Ns = range(3, Nmax + 1)
    settings = [(0.21, b) for b in (0, 2, 4, 5, 6, 8, 12)] + [(0.15, b) for b in (6, 12)] + [(0.3, b) for b in (2, 4.5, 8)]
    data = {}
    for N in Ns:
        for eps in sorted({e for e, _ in settings}):
            data[N, eps] = grow_all(N, eps, stems=True)
    for qi, name in enumerate(("Q1 more than one origin", "Q2 2-chain stem", "Q3 3-chain stem")):
        print(f"\n{name}: P_N for N = {list(Ns)}")
        for eps, beta in settings:
            row = [p_quantum(data[N, eps][0], data[N, eps][3][:, qi], beta) for N in Ns]
            print(f"  eps={eps:4.2f} beta={beta:4.1f}   " + "  ".join(f"{v:.3f}" for v in row))
