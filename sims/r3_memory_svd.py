"""Idea 007 / idea 004 (session 9): classical vs quantum memory of the growth, from the past -> future amplitude matrix.

Same growth sum as a2_future_factor.py (each newborn picks a down-set D, amplitude e^{i beta dS(D)}).
Past p = unlabelled poset after k births; future = unlabelled final poset F at size N (histories ending in the same F interfere).
    B[p, F] = sum over growth continuations p -> F of e^{i beta (S_F - S_p)}            (row sums = F_N(p) of a2_future_factor)
Memory the past must hand to the future:
    classical  C = log2(#distinct rows up to a complex factor)   (pasts with the same row can share a memory slot)
    quantum    Q = log2(rank B)                                    (rows that are linearly dependent need no slot of their own)
    effective  Q_eff = entropy (bits) of s_i^2 / sum s^2, rows normalized to 1 (each past weighted equally)
Ceiling log2(#pasts). Controls: beta = 0 (pure counting) and random phases per transition (no structure).
Finding (first run): dS is path independent (S_F - S_p), so B = diag(e^{-i beta S_p}) Count diag(e^{i beta S_F}) and phases can't change any memory
measure when the future is the full final poset. Phases matter only if the outcome is a coarse RECORD of F (many F interfere in one column):
    B_rec[p, R] = sum_{F in R} B[p, F],   R = (height, #minimal, #maximal, #links) of F.
Usage: python r3_memory_svd.py [N] [cuts, e.g. 3,4,5]
"""
import sys, time
import numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import a2_future_factor as aff
from a2_future_factor import FutureFactor, wl_key
from s3a_mcmc_2d import f_weights

SETTINGS = [(0.21, 0.0), (0.21, 4.0), (0.21, 7.0), (0.21, 8.0), (0.21, 12.0), (0.21, "random")]


class MemoryMatrix(FutureFactor):
    def __init__(self, N, seed=1):
        aff.SETTINGS = [(e, 0.0 if b == "random" else b) for e, b in SETTINGS]
        super().__init__(N)
        self.random = np.array([b == "random" for _, b in SETTINGS])
        self.rng = np.random.default_rng(seed)
        self.vmemo = {}

    def V(self, past, up):
        """Dict final_key -> amplitudes (settings,) of all continuations of this state to size N."""
        key = wl_key(past, up)
        if key in self.vmemo:
            return self.vmemo[key]
        m = len(past)
        if m == self.Nmax:
            out = {key: np.ones(len(SETTINGS), complex)}
        else:
            D, ph = self.children(past, up)
            ph[self.random] = np.exp(2j * np.pi * self.rng.random((self.random.sum(), len(D))))   # fixed once per (state, D): memo makes it consistent
            out, bit = {}, 1 << m
            for c, d in enumerate(D):
                d = int(d)
                up2 = [u | bit if d >> i & 1 else u for i, u in enumerate(up)] + [0]
                for fk, amp in self.V(past + [d], up2).items():
                    out[fk] = out.get(fk, 0) + ph[:, c] * amp
        self.vmemo[key] = out
        return out

    def stems(self, n):
        reps, seen = [], set()
        def rec(past, up):
            if len(past) == n:
                k = wl_key(past, up)
                if k not in seen:
                    seen.add(k); reps.append((past, up))
                return
            D, _ = self.children(past, up)
            bit = 1 << len(past)
            for d in D:
                d = int(d)
                rec(past + [d], [u | bit if d >> i & 1 else u for i, u in enumerate(up)] + [0])
        rec([], [])
        return reps


def record(fkey):
    """(height, #minimal, #maximal, #links) of a final poset, rebuilt from its canonical key (entry j = (colour, positions of its past))."""
    pasts = [set(e[1]) for e in fkey[1]]
    m = len(pasts)
    h = [0] * m
    for j in sorted(range(m), key=lambda j: len(pasts[j])):
        h[j] = max([h[i] + 1 for i in pasts[j]], default=0)
    links = sum(1 for j in range(m) for i in pasts[j] if not any(i in pasts[k] for k in pasts[j]))
    maxi = sum(1 for j in range(m) if not any(j in pasts[k] for k in range(m)))
    return (max(h) + 1, sum(1 for P in pasts if not P), maxi, links)


def distinct_rows(B, tol=1e-8):
    """Number of rows that differ by more than a complex factor."""
    reps = []
    for r in B:
        nr = np.linalg.norm(r)
        if nr < tol:
            continue
        r = r / nr
        r = r * np.exp(-1j * np.angle(r[np.argmax(np.abs(r))]))
        if not any(np.linalg.norm(r - q) < 1e-6 for q in reps):
            reps.append(r)
    return len(reps)


def sectors(B, tol):
    """Pasts that can still interfere: connected components of the graph |<row_i, row_j>| > tol (rows normalized).
    Different sectors have orthogonal futures ("can never interfere again") and each needs its own classical memory slot."""
    Bn = B / np.linalg.norm(B, axis=1, keepdims=True)
    with np.errstate(all="ignore"):          # numpy 2.0 + Accelerate: spurious matmul warnings (as in s3a_mcmc_2d)
        A = np.abs(Bn @ Bn.conj().T) > tol
    seen, n = np.zeros(len(B), bool), 0
    for i in range(len(B)):
        if not seen[i]:
            n += 1
            stack = [i]
            while stack:
                j = stack.pop()
                if not seen[j]:
                    seen[j] = True
                    stack.extend(np.flatnonzero(A[j] & ~seen))
    return n


def measures(B):
    s = np.linalg.svd(B, compute_uv=False)
    rank = int((s > 1e-9 * s[0]).sum())
    Bn = B / np.linalg.norm(B, axis=1, keepdims=True)
    sn = np.linalg.svd(Bn, compute_uv=False) ** 2
    p = sn / sn.sum()
    p = p[p > 1e-15]
    return distinct_rows(B), rank, float(-(p * np.log2(p)).sum()), [sectors(B, t) for t in (1e-12, 1e-3, 1e-1)]


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    cuts = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else [3, 4, 5]
    t0 = time.time()
    MM = MemoryMatrix(N)
    Vroot = MM.V([], [])
    finals = sorted(Vroot, key=str)
    col = {k: i for i, k in enumerate(finals)}
    recs = sorted({record(k) for k in finals})
    rcol = {k: recs.index(record(k)) for k in finals}
    print(f"N={N}: {len(finals)} final universes, {len(MM.vmemo)} states, {time.time() - t0:.1f} s", flush=True)
    # validation: row sums = F_N(stem) of a2_future_factor (same eps, deterministic settings)
    FF = FutureFactor(N)
    for p, u in MM.stems(min(cuts)):
        Fn = FF.G(p, u)[:, N - len(p)]
        Vs = sum(MM.V(p, u).values())
        for s, (_, b) in enumerate(SETTINGS):
            if b != "random":
                assert np.isclose(Vs[s], Fn[s]), (p, s)
    print("validated: row sums = F_N(stem) from a2_future_factor", flush=True)
    for k in cuts:
        reps = MM.stems(k)
        rows = [MM.V(p, u) for p, u in reps]
        print(f"\n== cut after k={k} births: {len(reps)} pasts (ceiling log2 = {np.log2(len(reps)):.2f} bits), {len(finals)} futures ==")
        print(f"   {'setting':>16s}  {'distinct rows':>13s}  {'rank':>5s}  {'C bits':>6s}  {'Q bits':>6s}  {'Q_eff bits':>10s}  sectors (tol 0 / 1e-3 / 0.1)")
        for future, cmap, ncol in (("full F", col, len(finals)), ("record", rcol, len(recs))):
            print(f"   -- future = {future} ({ncol} columns)")
            for s, (e, b) in enumerate(SETTINGS):
                B = np.zeros((len(reps), ncol), complex)
                for i, r in enumerate(rows):
                    for fk, amp in r.items():
                        B[i, cmap[fk]] += amp[s]
                nd, rank, qe, sec = measures(B)
                lab = f"eps={e} beta={b}"
                print(f"   {lab:>16s}  {nd:13d}  {rank:5d}  {np.log2(nd):6.2f}  {np.log2(rank):6.2f}  {qe:10.2f}  {sec[0]:4d} / {sec[1]:4d} / {sec[2]:4d}", flush=True)
    print(f"\ntotal {time.time() - t0:.1f} s")
