"""Stage S3-quantum: exact quantum sum over all 2D orders of N events (no sampling, so no sign problem).

Fix u = identity (label events by their u-order); every permutation v gives one 2D order, i.e. one possible
universe, with the uniform measure of a sprinkling. Each universe gets amplitude exp(i beta S), S = 2D BD action.
Quantum mechanics needs a "record": histories that end in the same record interfere, different records do not.
Lesson (session 2): if every whole universe is its own record, phases never matter (|e^{i beta S}|^2 = 1). We use
two relational records, both in the spirit of C5 (cosmic time):
  AGE     = number of cosmic-time layers (longest chain)
  PRESENT = number of events in the last layer (maximal events): "the size of the universe now"
  quantum:   P_q(r) = |A_r|^2 / sum_r |A_r|^2,   A_r = sum_{universes with record r} exp(i beta S)
  classical: P_c(r) = sum_{record r} exp(-beta S) / sum exp(-beta S)       (the e^{-beta S} version of S3a)
"""
import itertools
import sys
import numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from s3a_mcmc_2d import f_weights, action

def enumerate_universes(N, eps):
    fw = f_weights(N, eps)
    u = np.arange(N)
    S, age, present = [], [], []
    for perm in itertools.permutations(range(N)):
        v = np.array(perm)
        s, C = action(u, v, eps, fw)
        h = np.zeros(N, dtype=int)
        for j in range(N):                       # u-order is a linear extension
            p = np.nonzero(C[:j, j])[0]
            h[j] = h[p].max() + 1 if p.size else 0
        S.append(s)
        age.append(h.max() + 1)
        present.append(int((C.sum(1) == 0).sum()))   # maximal events: no future
    return np.array(S), np.array(age), np.array(present)

def distributions(S, rec, beta):
    rs = np.unique(rec)
    amp = np.exp(1j * beta * S)
    A = np.array([amp[rec == r].sum() for r in rs])
    Pq = np.abs(A) ** 2 / (np.abs(A) ** 2).sum()
    w = np.exp(-beta * (S - S.min()))
    Pc = np.array([w[rec == r].sum() for r in rs]) / w.sum()
    return rs, Pq, Pc

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    eps = float(sys.argv[2]) if len(sys.argv) > 2 else 0.21
    S, age, present = enumerate_universes(N, eps)
    print(f"N={N}, eps={eps}: {len(S)} universes; action range [{S.min():.2f}, {S.max():.2f}]")
    for name, rec in [("AGE (layers)", age), ("PRESENT (events in last layer)", present)]:
        print(f"\n record = {name}")
        for beta in [0.0, 1.0, 2.0, 4.0, 8.0]:
            rs, Pq, Pc = distributions(S, rec, beta)
            print(f"  beta={beta:3.1f}  mean quantum={np.dot(rs, Pq):.2f}  classical={np.dot(rs, Pc):.2f}   "
                  + "  ".join(f"{r}:{q:.2f}/{c:.2f}" for r, q, c in zip(rs, Pq, Pc)))
