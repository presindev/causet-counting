"""Rung 2 of the memory ladder (idea 004, session 9): is the macrostate (cell counts) enough to predict what a newborn feels?

1+1 flat, units l = 1 (rho = 1). Light-cone coords u = t - x, v = t + x (area element du dv / 2). The newborn x sits at the origin;
its past is the diamond u, v in [-a, 0], N ~ Poisson(a^2 / 2) events. For each past event y, n_y = #{z : y < z < x}.
What x feels = Sorkin's 2D operator acting on phi = 1 (mean 0 in flat space):
    raw:      b   = -1/2 + n0 - 2 n1 + n2                     (n_k = #{y : n_y = k})
    smeared:  b_e = -1/2 + e * sum_y f(n_y, e),  f(n, e) = (1-e)^n [1 - 2 e n/(1-e) + e^2 n(n-1) / (2 (1-e)^2)]
              (Sorkin 2007, gr-qc/0703099; non-locality scale l_k = l / sqrt(e)).
Macrostate = counts in an m x m grid of cells in (u, v), cells boosted by rapidity theta relative to x (u-side e^-theta, v-side e^theta).
Test: keep the counts, redraw positions uniformly inside each cell ("shuffle"), recompute b.
    f_micro = E[ Var(b | cell counts) ] / Var(b)        1 = macrostate explains nothing, 0 = macrostate fixes b.
Errors: spread over independent base sprinklings (lesson 8), bootstrap.
"""
import sys
import numpy as np


def interval_counts(u, v, chunk=800):
    n = np.empty(len(u), np.int64)
    for i in range(0, len(u), chunk):
        n[i:i + chunk] = ((u[None, :] > u[i:i + chunk, None]) & (v[None, :] > v[i:i + chunk, None])).sum(1)
    return n


def feel(n, eps_list):
    out = [-0.5 + np.sum(n == 0) - 2 * np.sum(n == 1) + np.sum(n == 2)]
    for e in eps_list:
        nn = n.astype(float)
        f = (1 - e) ** nn * (1 - 2 * e * nn / (1 - e) + e**2 * nn * (nn - 1) / (2 * (1 - e) ** 2))
        out.append(-0.5 + e * f.sum())
    return np.array(out)


def cells_of(u, v, a, m, theta):
    """Cell grid in a frame boosted by theta: coordinates U = e^theta u, V = e^-theta v, cells of side a/m in U and V.
    The diamond is covered by an (extended) grid; returns integer cell ids and the cell boxes in (u, v)."""
    s = a / m
    iu = np.floor(-np.exp(theta) * u / s).astype(np.int64)
    iv = np.floor(-np.exp(-theta) * v / s).astype(np.int64)
    return iu, iv, s


def shuffle(rng, u, v, a, m, theta):
    """Redraw each event uniformly inside its cell, clipped to the diamond (resample until inside)."""
    iu, iv, s = cells_of(u, v, a, m, theta)
    nu, nv = np.empty_like(u), np.empty_like(v)
    todo = np.arange(len(u))
    while len(todo):
        cu = -(iu[todo] + rng.random(len(todo))) * s * np.exp(-theta)
        cv = -(iv[todo] + rng.random(len(todo))) * s * np.exp(theta)
        ok = (cu >= -a) & (cv >= -a)
        nu[todo[ok]], nv[todo[ok]] = cu[ok], cv[ok]
        todo = todo[~ok]
    return nu, nv


def run(N_mean, m, theta, eps_list, n_base, n_shuf, seed):
    rng = np.random.default_rng(seed)
    a = np.sqrt(2 * N_mean)
    within, allv, means = [], [], []
    for _ in range(n_base):
        N = rng.poisson(N_mean)
        u, v = -a * rng.random(N), -a * rng.random(N)
        vals = [feel(interval_counts(u, v), eps_list)]
        for _ in range(n_shuf):
            su, sv = shuffle(rng, u, v, a, m, theta)
            vals.append(feel(interval_counts(su, sv), eps_list))
        vals = np.array(vals)
        within.append(vals.var(0, ddof=1))
        allv.append(vals)
        means.append(vals[0])
    within, allv, means = np.array(within), np.array(allv), np.array(means)
    tot = allv.reshape(-1, allv.shape[-1]).var(0, ddof=1)
    f = within.mean(0) / tot
    boot = []
    for _ in range(200):
        k = rng.integers(0, n_base, n_base)
        boot.append(within[k].mean(0) / allv[k].reshape(-1, allv.shape[-1]).var(0, ddof=1))
    return f, np.std(boot, 0), means.mean(0), means.std(0, ddof=1) / np.sqrt(n_base), np.sqrt(tot)


if __name__ == "__main__":
    eps_list = [0.1, 0.03]
    Ns = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else [500, 2000]
    ms = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else [2, 4, 8, 16]
    thetas = [float(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else [0.0]
    n_base = int(sys.argv[4]) if len(sys.argv) > 4 else 12
    n_shuf = int(sys.argv[5]) if len(sys.argv) > 5 else 8
    labels = ["raw"] + [f"eps={e}" for e in eps_list]
    print(f"bases={n_base} shuffles={n_shuf}; columns: " + " | ".join(labels), flush=True)
    for N in Ns:
        for th in thetas:
            for m in ms:
                f, df, mu, dmu, sd = run(N, m, th, eps_list, n_base, n_shuf, seed=1000 * N + 10 * m + int(10 * th))
                ev = N / m**2
                cells = " | ".join(f"f={f[i]:.2f}±{df[i]:.2f} (mean {mu[i]:+.2f}±{dmu[i]:.2f}, sd {sd[i]:.2f})" for i in range(len(f)))
                print(f"N={N:5d} theta={th:.0f} m={m:3d} ({ev:7.1f} ev/cell): {cells}", flush=True)
