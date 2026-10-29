"""Two cheap checks asked by the round-4 referee (session 15), on the Table II universes (seed = 1000 + i):
  (1) log-likelihood of the fit started from the intrinsic map vs the same fit (Johnston's t) started from the TRUE positions: if the intrinsic optimum
      had the higher lnL, its extra position error would be a property of the likelihood, not of the start;
  (2) causal fidelity: share of pairs whose relation (related vs spacelike) in the embedded map, Delta t^2 > |Delta x|^2, disagrees with the causal order,
      for Johnston's map, the fit, and the truth-started fit; split by true related / spacelike pairs.
Usage: python r34_lnl_causal_fidelity.py n seed
"""
import sys
import numpy as np
from r11_4d_distance import load_table
from r12_johnston_compare import johnston
from r13_mixed import sprinkle
from r15_cheap_far import related_R
from r18_waist_oracle import ours_with_counts
from r19_cluster_wfit import fit_w
from r23_likelihood import setup, fit, loglik, Table

np.seterr(all="ignore")

def fidelity(X, rel, iu):
    dt2 = (X[:, None, 0] - X[None, :, 0]) ** 2
    dx2 = ((X[:, None, 1:] - X[None, :, 1:]) ** 2).sum(-1)
    pred = (dt2 > dx2)[iu]
    return np.mean(pred != rel), np.mean(~pred[rel]), np.mean(pred[~rel])

def main(n, seed):
    W = load_table(); tab = Table(W)
    rng = np.random.default_rng(seed)
    P, C, rho = sprinkle(n, rng)
    iu = np.triu_indices(len(P), 1)
    rel = (C | C.T)[iu]
    _, Xj = johnston(C, rho, 1.0)
    R, t = related_R(C, rho); I, J, s, k = ours_with_counts(C, rho, t, W)
    Xw, _ = fit_w(R, t, I, J, s, k, 100); del R
    S, Rl = setup(C, rho, t, W)
    S["nb"] = np.zeros_like(S["nb"]); S["nc"] = np.zeros_like(S["nc"])          # related-pair term only, as in the paper
    xi, _ = fit(Xw[:, 1:], t, S, Rl, rho, tab, 400)
    xt, _ = fit(P[:, 1:].copy(), t, S, Rl, rho, tab, 400)
    Li = loglik(xi, t, S, Rl, rho, tab, grad=False)[0]; Lt = loglik(xt, t, S, Rl, rho, tab, grad=False)[0]
    print("n = %d seed %d: lnL intrinsic-start optimum %.1f, truth-start optimum %.1f (difference %+.1f over %d related pairs)" % (
          n, seed, Li, Lt, Lt - Li, len(Rl["A"])), flush=True)
    for name, X in (("Johnston", Xj), ("fit", np.column_stack([t, xi])), ("fit from truth", np.column_stack([t, xt]))):
        a, b, c = fidelity(X, rel, iu)
        print("  %-15s misclassified pairs %.4f  (related shown spacelike %.4f, spacelike shown related %.4f)" % (name, a, b, c), flush=True)

if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]))
