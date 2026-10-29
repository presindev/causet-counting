"""Idea 007 (session 9): records relative to what a future event can see (the "screen").

Alternatives: the universe p after k births (as in r3_memory_svd.py). The universe grows to N-1 events; the last newborn (event N) picks its past D.
Screen = what that newborn sees of its past, at three resolutions:
    full    the poset D up to relabelling
    coarse  (|D|, #links of the newborn = #maximal elements of D)
    links   #links only
    B[p, view] = sum over growths p -> N-1 and choices D with that view of e^{i beta dS}.
Decoherence functional between alternatives on this screen: G = Bn Bn^dagger (rows normalized). Coherence c = mean |G_ij| over pairs i != j
(0: every pair is a record, 1: nothing is). Also: fraction of exactly decohered pairs (|G_ij| < 1e-9), rank and Q_eff as in r3.
Question: do the phases (beta > 0) decohere alternatives better than counting (beta = 0)?
Usage: python r4_screen.py [N] [cuts]
"""
import sys, time
import numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from a2_future_factor import wl_key
from r3_memory_svd import MemoryMatrix, SETTINGS

RESOLUTIONS = ("full", "coarse", "links")


def view(past, D, res):
    """What a newborn with past D (bitmask over the current poset) sees."""
    idx = [i for i in range(len(past)) if D >> i & 1]
    pos = {i: j for j, i in enumerate(idx)}
    sub = [sum(1 << pos[i] for i in idx if past[x] >> i & 1) for x in idx]
    maximal = sum(1 for x in idx if not any(past[y] >> x & 1 for y in idx))
    if res == "links":
        return maximal
    if res == "coarse":
        return (len(idx), maximal)
    up = [sum(1 << b for b in range(len(sub)) if sub[b] >> a & 1) for a in range(len(sub))]
    return wl_key(sub, up) if sub else (0, ())


class ScreenMatrix(MemoryMatrix):
    def __init__(self, N, res):
        super().__init__(N)
        self.res = res

    def V(self, past, up):
        key = wl_key(past, up)
        if key in self.vmemo:
            return self.vmemo[key]
        m = len(past)
        D, ph = self.children(past, up)
        ph[self.random] = np.exp(2j * np.pi * self.rng.random((self.random.sum(), len(D))))
        out, bit = {}, 1 << m
        for c, d in enumerate(D):
            d = int(d)
            if m == self.Nmax - 1:
                v = view(past, d, self.res)
                out[v] = out.get(v, 0) + ph[:, c]
            else:
                up2 = [u | bit if d >> i & 1 else u for i, u in enumerate(up)] + [0]
                for fk, amp in self.V(past + [d], up2).items():
                    out[fk] = out.get(fk, 0) + ph[:, c] * amp
        self.vmemo[key] = out
        return out


def coherence(B):
    Bn = B / np.linalg.norm(B, axis=1, keepdims=True)
    with np.errstate(all="ignore"):          # numpy 2.0 + Accelerate: spurious matmul warnings
        G = np.abs(Bn @ Bn.conj().T)
    off = G[~np.eye(len(B), dtype=bool)]
    s = np.linalg.svd(Bn, compute_uv=False) ** 2
    p = s / s.sum()
    p = p[p > 1e-15]
    rank = int((s > 1e-18 * s[0]).sum())
    return off.mean(), (off < 1e-9).mean(), rank, float(-(p * np.log2(p)).sum())


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    cuts = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else [3, 4, 5]
    t0 = time.time()
    for res in RESOLUTIONS:
        SM = ScreenMatrix(N, res)
        views = sorted(SM.V([], []), key=str)
        col = {v: i for i, v in enumerate(views)}
        print(f"\n######## screen = {res}: {len(views)} possible views of the last newborn (N = {N}), {time.time() - t0:.1f} s", flush=True)
        for k in cuts:
            reps = SM.stems(k)
            rows = [SM.V(p, u) for p, u in reps]
            print(f"  -- k = {k}: {len(reps)} alternatives.   setting: coherence | exactly decohered pairs | rank | Q_eff bits")
            for s, (e, b) in enumerate(SETTINGS):
                B = np.zeros((len(reps), len(views)), complex)
                for i, r in enumerate(rows):
                    for v, amp in r.items():
                        B[i, col[v]] += amp[s]
                c, dec, rank, qe = coherence(B)
                print(f"     beta={str(b):>6s}: {c:.3f} | {dec:.3f} | {rank:4d} | {qe:.2f}", flush=True)
    print(f"\ntotal {time.time() - t0:.1f} s")
