"""Stage S3a: 2D causal set "quantum gravity" with positive weights e^{-beta S} (Surya 2012; Glaser-O'Connor-Surya 2018).

Sample space: 2D orders. Each event i has two labels (u_i, v_i), given by two permutations of 0..N-1, and
i precedes j iff u_i < u_j and v_i < v_j. (A random 2D order is the same as N points sprinkled into a diamond.)

Action (2D Benincasa-Dowker with non-locality parameter eps):
    S(C, eps) = 4 eps ( N - 2 eps sum_n N_n f(n, eps) ),
    f(n, eps) = (1-eps)^n [1 - 2 eps n/(1-eps) + eps^2 n(n-1) / (2 (1-eps)^2)],
N_n = number of related pairs with exactly n events strictly between them. Equals -2 sum_x B_eps 1(x).

Metropolis: propose swapping two entries of u or of v; accept with min(1, exp(-beta dS)).
Observables: S/N, ordering fraction r (r = 1/2 for flat 2D), longest chain / (2 sqrt N), number of layers.
"""
import sys
import numpy as np

def f_weights(N, eps):
    n = np.arange(N, dtype=float)
    q = 1 - eps
    return q**n * (1 - 2 * eps * n / q + eps**2 * n * (n - 1) / (2 * q**2))

def causal(u, v):
    return ((u[:, None] < u[None, :]) & (v[:, None] < v[None, :])).astype(np.float64)

def action(u, v, eps, fw):
    C = causal(u, v)
    with np.errstate(all="ignore"):          # numpy 2.0 + Accelerate: spurious matmul warnings
        K = C @ C
    n_between = K[C > 0].astype(int)
    Nn = np.bincount(n_between, minlength=len(fw))
    return 4 * eps * (len(u) - 2 * eps * np.dot(Nn, fw[:len(Nn)])), C

def observables(C):
    N = C.shape[0]
    r = C.sum() / (N * (N - 1) / 2)
    order = np.argsort(C.sum(0))                     # events with smaller pasts first: a linear extension
    h = np.zeros(N, dtype=int)
    for j in order:
        p = np.nonzero(C[:, j])[0]
        h[j] = h[p].max() + 1 if p.size else 0
    return r, (h.max() + 1) / (2 * np.sqrt(N)), h.max() + 1

def run(N, beta, eps, sweeps=600, seed=0):
    rng = np.random.default_rng(seed)
    u, v = rng.permutation(N), rng.permutation(N)
    fw = f_weights(N, eps)
    S, C = action(u, v, eps, fw)
    acc, obs = 0, []
    steps = sweeps * N
    for t in range(steps):
        w = u if rng.random() < 0.5 else v
        a, b = rng.integers(0, N, 2)
        w[a], w[b] = w[b], w[a]
        S2, C2 = action(u, v, eps, fw)
        if np.log(rng.random()) < -beta * (S2 - S):
            S, C = S2, C2
            acc += 1
        else:
            w[a], w[b] = w[b], w[a]
        if t > steps // 3 and t % N == 0:
            obs.append((S / N, *observables(C)))
    o = np.array(obs)
    return o.mean(0), o.std(0), acc / steps

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    eps = float(sys.argv[2]) if len(sys.argv) > 2 else 0.21
    print(f"N={N}, eps={eps}")
    print("  beta    <S>/N   ordering r   chain/2sqrtN   layers   acceptance")
    betas = [float(b) for b in sys.argv[3].split(",")] if len(sys.argv) > 3 else [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 6.0]
    for beta in betas:
        m, s, a = run(N, beta, eps)
        print(f"  {beta:4.1f}  {m[0]:7.3f}   {m[1]:6.3f}       {m[2]:6.3f}       {m[3]:6.1f}    {a:.2f}", flush=True)

def samples(N, beta, eps, n_samples=40, sweeps_between=20, seed=1):
    """Equilibrate, then return causal matrices spaced by sweeps_between sweeps."""
    rng = np.random.default_rng(seed)
    u, v = rng.permutation(N), rng.permutation(N)
    fw = f_weights(N, eps)
    S, C = action(u, v, eps, fw)
    out = []
    total = (200 + n_samples * sweeps_between) * N
    for t in range(total):
        w = u if rng.random() < 0.5 else v
        a, b = rng.integers(0, N, 2)
        w[a], w[b] = w[b], w[a]
        S2, C2 = action(u, v, eps, fw)
        if np.log(rng.random()) < -beta * (S2 - S):
            S, C = S2, C2
        else:
            w[a], w[b] = w[b], w[a]
        if t >= 200 * N and (t - 200 * N) % (sweeps_between * N) == 0:
            out.append(C.copy())
    return out
