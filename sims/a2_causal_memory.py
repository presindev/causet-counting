"""A2, option 2: is the influence of the past "causally close" rather than "recent in rows"? (idea 004, session 5)

Growth rule (Roberto; = Rideout-Sorkin internal temporality): a new event f may have any down-set of existing events
as its past, but never becomes a cause of an existing event. Then adding f creates only the pairs (x, f), x in past(f),
and every event strictly between x and f already exists, so the BD action (eps = 0.21, as in s3a_mcmc_2d.py) grows by
    dS_f = 4 eps - 8 eps^2 sum_{x < f} f(n_xf, eps),     n_xf = number of events strictly between x and f,
and S = sum_f dS_f for ANY growth order (a linear extension). Truncation by causal closeness: keep only x with
n_xf <= n_cut. This is the same as dropping related pairs with more than n_cut events between them. n_cut is a count,
so it's Lorentz-invariant and uses no clock (C5 satisfied automatically, unlike the height cut of a2_memory_depth.py).
Error scale: sd over universes of (S - S_cut) in units of sigma_S (a constant shift cancels in record probabilities).
Memory size: mean number of past events kept per new event, and the largest height gap among them ("far in rows").
C1-C8: measures an existing action; the growth order is bookkeeping only (S doesn't depend on it). No record (no quantum sum).
Usage: python a2_causal_memory.py
"""
import numpy as np
from s3a_mcmc_2d import f_weights, causal
from s3a_fast import samples
from a2_memory_depth import heights

np.seterr(all="ignore")
EPS = 0.21
CUTS = (0, 1, 2, 5, 10, 20, 30, 40)

def pair_data(C):
    K = C @ C
    x, y = np.nonzero(C)
    return x, y, K[x, y].astype(int)

def analyse(Cs, fw, sigma):
    """Per universe: S - S_cut for each cut, events kept per new event, max height gap of kept pairs."""
    d, kept, gap = [], [], []
    for C in Cs:
        N = C.shape[0]
        x, y, n = pair_data(C)
        h = heights(C)
        w = fw[n]
        d.append([-8 * EPS**2 * w[n > c].sum() for c in CUTS])
        kept.append([(n <= c).sum() / N for c in CUTS])
        gap.append([(h[y] - h[x])[n <= c].max() for c in CUTS])
    d, kept, gap = map(np.array, (d, kept, gap))
    return d.std(0) / sigma, np.abs(d).mean(0) / sigma, kept.mean(0), gap.mean(0)

def growth_check(rng, N, fw):
    """S summed event by event along a linear extension equals the action."""
    u, v = rng.permutation(N), rng.permutation(N)
    C = causal(u, v)
    order = np.argsort(u + v)                          # a linear extension: x < y implies u_x + v_x < u_y + v_y
    S, born = 0.0, np.zeros(N, bool)
    for f in order:
        past = np.nonzero(C[:, f])[0]
        assert born[past].all()                         # f's past already exists: f is born maximal
        n = (C[past][:, born] @ C[born, f]).astype(int) # events between x and f, all already born
        S += 4 * EPS - 8 * EPS**2 * fw[n].sum()
        born[f] = True
    x, y, n = pair_data(C)
    return S, 4 * EPS * (N - 2 * EPS * fw[n].sum())

if __name__ == "__main__":
    rng = np.random.default_rng(5)
    S1, S2 = growth_check(rng, 60, f_weights(60, EPS))
    print("growth check (N = 60): S summed over births = {:.10f}, action = {:.10f}".format(S1, S2))
    print("cuts n_cut =", CUTS)
    for N, n_univ in ((100, 60), (200, 40), (400, 20)):
        fw = f_weights(N, EPS)
        Cs = [causal(rng.permutation(N), rng.permutation(N)) for _ in range(n_univ)]
        Ss = [4 * EPS * (N - 2 * EPS * fw[pair_data(C)[2]].sum()) for C in Cs]
        sigma = np.std(Ss)
        sd, mabs, kept, gap = analyse(Cs, fw, sigma)
        print("\ncontinuum N = {} ({} universes, sigma_S = {:.1f})".format(N, n_univ, sigma))
        print("  sd(S - S_cut)/sigma : " + "  ".join("{:.3f}".format(a) for a in sd))
        print("  |S - S_cut|/sigma   : " + "  ".join("{:.3f}".format(a) for a in mabs))
        print("  kept per new event  : " + "  ".join("{:.1f}".format(a) for a in kept))
        print("  max row gap kept    : " + "  ".join("{:.1f}".format(a) for a in gap))
    for N, beta, sigma in ((200, 0.6, 12.0),):
        fw = f_weights(N, EPS)
        Cs = samples(N, beta, EPS, n_samples=10, sweeps_between=20, burn_in=300, seed=3)
        sd, mabs, kept, gap = analyse(Cs, fw, sigma)
        print("\ncrystal N = {} beta = {} (sigma_S of the uniform ensemble = {})".format(N, beta, sigma))
        print("  sd(S - S_cut)/sigma : " + "  ".join("{:.3f}".format(a) for a in sd))
        print("  |S - S_cut|/sigma   : " + "  ".join("{:.3f}".format(a) for a in mabs))
        print("  kept per new event  : " + "  ".join("{:.1f}".format(a) for a in kept))
        print("  max row gap kept    : " + "  ".join("{:.1f}".format(a) for a in gap))
