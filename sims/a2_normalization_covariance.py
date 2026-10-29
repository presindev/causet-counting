"""A2 (idea 004, session 6): does per-step normalization's covariance violation wash out as N grows? (Roberto's idea)

Rule: newborn chooses a down-set D of the current universe with amplitude e^{i beta dS(D)} / Z(stem), Z = sum over all D.
A universe's amplitude along a growth order = e^{i beta S} / prod_k Z(stem_k). Covariance needs prod_k Z to be the same for
every growth order (linear extension) of the same universe. beta = 0 is the classical "uniform choice of past" rule (Z = number
of down-sets). Measure: over random linear extensions of one universe, sd of log|prod Z| (size) and of arg prod Z (phase).
Covariant would be 0 at every N. Washing out would mean the spread shrinks (relative to log|prod Z| itself) as N grows.
Universes: random 2D orders (sprinkled diamond, manifold-like) of N = 6..20, each with 200 random linear extensions.
Usage: python a2_normalization_covariance.py
"""
import numpy as np
from s3a_mcmc_2d import f_weights

def downsets(past, n):
    """All down-sets of events 0..n-1 (0..n-1 is a linear extension: past[i] only has indices < i)."""
    out = [0]
    for i in range(n):
        out += [D | 1 << i for D in out if past[i] & ~D == 0]
    return out

def log_Z(past, up, n, eps, beta, fw):
    z = 0j
    for D in downsets(past, n):
        dS = 4 * eps
        m = D
        while m:
            i = (m & -m).bit_length() - 1
            dS -= 8 * eps ** 2 * fw[bin(D & up[i]).count("1")]
            m &= m - 1
        z += np.exp(1j * beta * dS)
    return np.log(z)

def random_2d_order(rng, N):
    u, v = rng.permutation(N), rng.permutation(N)
    return (u[:, None] < u[None, :]) & (v[:, None] < v[None, :])     # C[i, j]: i precedes j

def random_extension(rng, C):
    N = len(C)
    order, done = [], np.zeros(N, bool)
    indeg = C.sum(0).astype(int)
    while len(order) < N:
        ready = np.nonzero((indeg == 0) & ~done)[0]
        k = rng.choice(ready)
        order.append(k); done[k] = True
        indeg -= C[k].astype(int)
    return order

def path_log_Z(C, order, eps, beta, fw):
    pos = {e: i for i, e in enumerate(order)}
    total = 0j
    past, up = [], []
    for n, e in enumerate(order):
        total += log_Z(past, up, n, eps, beta, fw)
        D = 0
        for x in range(len(C)):
            if C[x, e]:
                D |= 1 << pos[x]
        up = [up[i] | (1 << n) if D >> i & 1 else up[i] for i in range(n)] + [0]
        past.append(D)
    return total

if __name__ == "__main__":
    rng = np.random.default_rng(4)
    eps = 0.21
    print("Per-step normalization: spread of log prod Z over growth orders of the SAME universe (0 = covariant)")
    print("  N   beta   mean log|prodZ|   sd log|prodZ|   sd/mean   phase coherence (1 = same phase for all orders)")
    for N in (6, 10, 14, 18, 22):
        fw = f_weights(N + 1, eps)
        for beta in (0.0, 6.0):
            sds, means, phs = [], [], []
            for _ in range(4):
                C = random_2d_order(rng, N)
                L = np.array([path_log_Z(C, random_extension(rng, C), eps, beta, fw) for _ in range(60)])
                sds.append(L.real.std()); means.append(L.real.mean())
                ph = np.angle(np.exp(1j * L.imag)); phs.append(abs(np.mean(np.exp(1j * ph))))
            print(f" {N:3d}  {beta:4.1f}   {np.mean(means):10.2f}       {np.mean(sds):8.3f}      {np.mean(sds) / np.mean(means):.3f}"
                  f"           {np.mean(phs):.2f}", flush=True)
