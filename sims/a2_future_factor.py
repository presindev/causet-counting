"""A2 branch C, factorization test (idea 004, session 7): does the future factor F_N(stem) become stem-independent?

Same growth sum as a2_growth_paths.py: each newborn picks any down-set D as its past, amplitude e^{i beta dS} per birth,
dS = 4 eps - 8 eps^2 sum_{x in D} f(n_xf, eps). For a grown stem X (size n),
  F_N(X) = sum over all growth continuations X -> size N of e^{i beta (S_N - S_X)},
so the full sum is Z_N = sum over labelled stems X of e^{i beta S_X} F_N(X). F_N depends only on the isomorphism class of X,
so it is memoized over unlabelled posets: G(state)[k] = sum_D e^{i beta dS(D)} G(state + D)[k-1], G[0] = 1.
Isomorphism key: exact canonical form (colour refinement + individualization). Checked: distinct keys per size = A000112,
beta = 0 sums = A006455 (growth paths), and Z_6 = the explicit path sum of a2_growth_paths.py.
Past stability <=> ratios F_N(X)/F_N(Y) converge as N grows.
Usage: python a2_future_factor.py [Nmax] [stem sizes, e.g. 2,3,4] [out.npz]
(out.npz stores, per stem size n, the F_N rows of every stem, the stem names and the reference index, for all SETTINGS.)
"""
import sys, time
import numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from s3a_mcmc_2d import f_weights

A000112 = [1, 1, 2, 5, 16, 63, 318, 2045, 16999, 183231, 2567284, 46749427]     # OEIS b-file, checked 2026-10-27
A006455 = [1, 1, 2, 7, 40, 357, 4824, 96428, 2800472, 116473461]     # naturally labelled posets = growth paths
SETTINGS = [(0.21, b) for b in (0, 2, 4, 6, 7, 8, 12)] + [(0.15, 12), (0.30, 3.5)]
POPC = np.array([bin(m).count("1") for m in range(1 << 16)])     # popcounts for pasts of up to 16 events (was 1 << 10: broke at N = 12, job 449948)

def _refine(col, mem, fut):
    while True:
        new = [hash((col[i], tuple(sorted(col[j] for j in mem[i])), tuple(sorted(col[j] for j in fut[i])))) for i in range(len(col))]
        if len(set(new)) == len(set(col)):
            return new
        col = new

def wl_key(past, up):
    """Exact canonical form: colour refinement + individualization (branching over one element per twin class)."""
    m = len(past)
    mem = [[j for j in range(m) if past[i] >> j & 1] for i in range(m)]
    fut = [[j for j in range(m) if up[i] >> j & 1] for i in range(m)]
    best = [None]

    def search(col):
        col = _refine(col, mem, fut)
        if len(set(col)) == m:
            order = sorted(range(m), key=lambda i: col[i])
            pos = {v: k for k, v in enumerate(order)}
            code = tuple(sorted((col[i], tuple(sorted(pos[j] for j in mem[i]))) for i in range(m)))
            if best[0] is None or code < best[0]:
                best[0] = code
            return
        cells = {}
        for i, c in enumerate(col):
            cells.setdefault(c, []).append(i)
        c0 = min((c for c in cells if len(cells[c]) > 1), key=lambda c: (len(cells[c]), c))
        seen = set()
        for v in cells[c0]:
            twin = (past[v], up[v])
            if twin in seen:
                continue
            seen.add(twin)
            search([hash((c, -1)) if i == v else c for i, c in enumerate(col)])

    search([hash((len(mem[i]), len(fut[i]))) for i in range(m)])
    return (m, best[0])

class FutureFactor:
    def __init__(self, Nmax):
        self.Nmax = Nmax
        self.eps = np.array([e for e, _ in SETTINGS])
        self.beta = np.array([b for _, b in SETTINGS])
        self.fw = np.array([f_weights(Nmax, e) for e in self.eps])          # (settings, Nmax)
        self.memo = {}
        self.keys_by_size = [set() for _ in range(Nmax + 1)]

    def children(self, past, up):
        """All valid pasts D of a newborn and the phase e^{i beta dS(D)} per setting."""
        m = len(past)
        cand = np.arange(1 << m)
        ok = np.ones(1 << m, bool)
        dsum = np.zeros((len(self.eps), 1 << m))
        for i in range(m):
            inD = (cand >> i) & 1 == 1
            ok &= ~inD | ((past[i] & ~cand) == 0)
            n_between = POPC[cand & up[i]]
            dsum += np.where(inD, self.fw[:, n_between], 0.0)
        D = cand[ok]
        dS = 4 * self.eps[:, None] - 8 * self.eps[:, None] ** 2 * dsum[:, ok]
        return D, np.exp(1j * self.beta[:, None] * dS)                     # (ndown,), (settings, ndown)

    def G(self, past, up):
        m = len(past)
        depth = self.Nmax - m
        key = wl_key(past, up)
        if key in self.memo:
            return self.memo[key]
        self.keys_by_size[m].add(key)
        out = np.zeros((len(SETTINGS), depth + 1), complex)
        out[:, 0] = 1
        if depth > 0:
            D, ph = self.children(past, up)
            if depth == 1:
                out[:, 1] = ph.sum(1)
            else:
                bit = 1 << m
                for c, d in enumerate(D):
                    d = int(d)
                    up2 = [u | bit if d >> i & 1 else u for i, u in enumerate(up)] + [0]
                    out[:, 1:] += ph[:, c:c + 1] * self.G(past + [d], up2)[:, :depth]
        self.memo[key] = out
        return out

def stems(n):
    """One labelled representative per unlabelled poset of size n (natural labelling)."""
    reps, seen = [], set()
    def rec(past, up):
        k = wl_key(past, up) if past else (0, ())
        if len(past) == n:
            if k not in seen:
                seen.add(k); reps.append((past, up))
            return
        D, ph = FF.children(past, up)
        bit = 1 << len(past)
        for c, d in enumerate(D):
            d = int(d)
            rec(past + [d], [u | bit if d >> i & 1 else u for i, u in enumerate(up)] + [0])
    rec([], [])
    return reps

def name(past):
    m = len(past)
    rel = sum(POPC[p] for p in past)
    links = sum(1 for i in range(m) for j in range(m) if past[i] >> j & 1 and not any(past[i] >> k & 1 and past[k] >> j & 1 for k in range(m)))
    h = [0] * m
    for i in range(m):
        h[i] = max([h[j] + 1 for j in range(m) if past[i] >> j & 1], default=0)
    mins = sum(1 for p in past if p == 0)
    return f"n{m}:rel{rel},min{mins},h{max(h) + 1}"

if __name__ == "__main__":
    Nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    t0 = time.time()
    FF = FutureFactor(Nmax)
    Z = FF.G([], [])
    print(f"Nmax={Nmax}: {time.time() - t0:.1f} s, {len(FF.memo)} states")
    print("distinct keys per size:", [len(s) for s in FF.keys_by_size[:Nmax]], " A000112:", A000112[:Nmax])
    print("beta=0 Z_N (growth paths):", [int(round(Z[0, k].real)) for k in range(Nmax + 1)], " A006455:", A006455[:Nmax + 1])
    if Nmax >= 6:                                   # validation against the explicit path enumeration
        from a2_growth_paths import grow_all
        for eps in sorted(set(FF.eps)):
            S_paths = grow_all(6, eps)[0]
            for s, (e, b) in enumerate(SETTINGS):
                if e == eps:
                    assert np.isclose(np.exp(1j * b * S_paths).sum(), Z[s, 6]), (e, b)
        print("validated Z_6 against a2_growth_paths.grow_all for all settings")
    sizes = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else [2, 3]
    save = {"settings": np.array(SETTINGS), "Nmax": Nmax, "seconds": time.time() - t0, "nstates": len(FF.memo)}
    for n in sizes:
        reps = stems(n)
        save[f"F_n{n}"] = np.array([FF.memo[wl_key(p, u)][:, :Nmax - n + 1] for p, u in reps])   # (stems, settings, N-n+1): F_N at N = n..Nmax
        save[f"names_n{n}"] = np.array([name(p) for p, _ in reps])
        print(f"\n== stems of size {n} ==")
        for s, (eps, beta) in enumerate(SETTINGS):
            print(f"eps={eps:.2f} beta={beta:4.1f}   (columns N = {n + 1}..{Nmax}; ratio F_N(X)/F_N(ref), ref = antichain; |.| and phase/pi)")
            Fs = [FF.memo[wl_key(p, u)][s] for p, u in reps]
            ref = [i for i, (p, _) in enumerate(reps) if all(x == 0 for x in p)][0]
            for i, (p, u) in enumerate(reps):
                if i == ref:
                    continue
                r = [Fs[i][N - n] / Fs[ref][N - n] for N in range(n + 1, Nmax + 1)]
                print(f"   {name(p):22s} " + "  ".join(f"{abs(x):7.3f}<{np.angle(x) / np.pi:+.2f}" for x in r))
    if len(sys.argv) > 3:
        np.savez_compressed(sys.argv[3], **save)
        print("saved", sys.argv[3])
