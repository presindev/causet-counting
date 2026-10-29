"""A2 step 1: memory depth of the Benincasa-Dowker action across height layers (ideas 002, 004).

Question: can e^{i beta S} be written as a product over thick height layers? Only if pairs of events many layers apart
contribute little to S. Set-up (same model as s3a_mcmc_2d.py, eps = 0.21):
    S = 4 eps ( N - 2 eps sum_{related pairs x<y} f(n_xy, eps) ),   n_xy = number of events strictly between x and y.
Height h(x) = length of the longest chain ending at x, counted from the minimal events (minimal events: h = 0).
Layer k = events with h = k. Every z strictly between x and y has h(x) < h(z) < h(y), so the term of a pair depends
only on layers h(x)..h(y) (checked below). Truncated action S_m: keep only pairs with gap h(y) - h(x) <= m.
    S - S_m = -8 eps^2 sum_{gap > m} f
Scale: phases e^{i beta S} only care about differences of order 1/beta, and the reachable beta is ~1/sigma_S, so the
truncation error is measured in units of sigma_S (the spread of S over uniform 2D orders at that N).
Ensembles: continuum = uniform random 2D orders (beta = 0); crystal = e^{-beta S} samples above beta_c (s3a_fast.py);
two-layer order (trivial: every gap is 1). C1-C8: this only measures an existing action; no new rule or clock is used
(height is the C5 bookkeeping clock, and only for the bookkeeping). No record is involved (no quantum sum here).
Usage: python a2_memory_depth.py
"""
import numpy as np
from s3a_mcmc_2d import f_weights, causal
from s3a_fast import samples

np.seterr(all="ignore")
EPS = 0.21
MS = range(1, 9)

def heights(C):
    """Longest chain ending at each event; events sorted by past size give a linear extension."""
    N = C.shape[0]
    h = np.zeros(N, dtype=int)
    for j in np.argsort(C.sum(0), kind="stable"):
        p = np.nonzero(C[:, j])[0]
        h[j] = h[p].max() + 1 if p.size else 0
    return h

def pair_data(C, fw):
    """For every related pair: interval size n, height gap, weight f(n)."""
    K = C @ C
    h = heights(C)
    i, j = np.nonzero(C > 0)
    n = K[i, j].astype(int)
    gap = h[j] - h[i]
    return n, gap, fw[n], h, i, j, K

def check_between(C, h, i, j):
    """Every z strictly between x and y has h(x) < h(z) < h(y)."""
    for a, b in zip(i[:300], j[:300]):
        z = np.nonzero((C[a] > 0) & (C[:, b] > 0))[0]
        if z.size and not (np.all(h[z] > h[a]) and np.all(h[z] < h[b])):
            return False
    return True

def stats(Cs, fw, sigma):
    rows, links = [], []
    ok = True
    for C in Cs:
        n, gap, f, h, i, j, _ = pair_data(C, fw)
        ok &= check_between(C, h, i, j)
        tot, tot_abs = f.sum(), np.abs(f).sum()
        rows.append([[f[gap > m].sum() / tot, np.abs(f[gap > m]).sum() / tot_abs,
                      abs(8 * EPS**2 * f[gap > m].sum()) / sigma] for m in MS])
        links.append(gap[n == 0])
    return np.array(rows), np.concatenate(links), ok

def report(label, Cs, fw, sigma):
    R, lg, ok = stats(Cs, fw, sigma)
    mu, sd = R.mean(0), R.std(0, ddof=1) if len(R) > 1 else np.zeros_like(R[0])
    print(f"\n{label}: {len(Cs)} universes, sigma_S = {sigma:.2f}; 'between' check: {'ok' if ok else 'FAILED'}")
    print("   m   share of sum f (gap>m)   share of sum|f| (gap>m)   |S - S_m| / sigma_S      (mean +- run-to-run sd)")
    for k, m in enumerate(MS):
        print(f"  {m:2d}   {mu[k,0]: .4f} +- {sd[k,0]:.4f}      {mu[k,1]:.4f} +- {sd[k,1]:.4f}         {mu[k,2]:.4f} +- {sd[k,2]:.4f}")
    g, c = np.unique(lg, return_counts=True)
    print("   link height gaps: " + "  ".join(f"{a}:{b/len(lg):.3f}" for a, b in zip(g, c))
          + f"   (mean {lg.mean():.2f}, max {lg.max()}, links per event {len(lg)/len(Cs)/Cs[0].shape[0]:.2f})")

def sigma_uniform(N, n=400, seed=7):
    rng = np.random.default_rng(seed)
    fw = f_weights(N, EPS)
    S = []
    for _ in range(n):
        C = causal(rng.permutation(N), rng.permutation(N))
        K = C @ C
        S.append(4 * EPS * (N - 2 * EPS * fw[K[C > 0].astype(int)].sum()))
    return np.std(S)

if __name__ == "__main__":
    rng = np.random.default_rng(11)
    for N in (50, 100, 200):
        fw = f_weights(N, EPS)
        sig = sigma_uniform(N)
        Cs = [causal(rng.permutation(N), rng.permutation(N)) for _ in range(40)]
        report(f"N={N} continuum (uniform 2D orders)", Cs, fw, sig)
        if N in (100, 200):
            beta = 0.6
            Cx = []
            for s in range(4):                      # 4 independent chains x 3 samples, spread over chains
                Cx += samples(N, beta, EPS, n_samples=3, sweeps_between=30, burn_in=400, seed=100 + s)
            report(f"N={N} crystal (e^-beta S, beta={beta})", Cx, fw, sig)
        if N == 100:
            k = N // 2                              # complete two-layer order
            u = np.r_[np.arange(k), np.arange(k, N)]
            v = np.r_[np.arange(k)[::-1], np.arange(k, N)[::-1]]
            report(f"N={N} two-layer order", [causal(u, v)], fw, sig)
