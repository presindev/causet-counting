"""Stage-1 toy (ideas 001/002): a universe that creates its own events.

Classical sequential growth by transitive percolation (Rideout-Sorkin 2000): events are born one
at a time; the newborn picks each existing event as a direct ancestor with probability p, and
inherits their whole past. Only the order relation is used afterwards (no background).

Relational observables:
  height h(x)  = length of the longest chain from the beginning to x   -> "cosmic time"
  layer sizes  = number of events per height                          -> "size of the universe" vs cosmic time
  links        = past neighbours (maximal elements of the past)       -> valency, the finite non-locality
  posts        = events comparable to every other event               -> cosmic "bounces"
"""
import sys
import numpy as np

def grow(N, p, seed=1, originary=False, c=None):
    """p: fixed link probability. If c is given, use p_n = min(1, c/n) instead (expanding universe;
    breaks Rideout-Sorkin covariance, see notes). originary=True forces at least one cause per newborn."""
    rng = np.random.default_rng(seed)
    past = [0] * N          # bitsets of ancestors
    height = np.zeros(N, dtype=int)
    for j in range(1 if originary else 0, N):
        pj = min(1.0, c / j) if c is not None else p
        while True:
            parents = np.nonzero(rng.random(j) < pj)[0]
            if parents.size or not originary:
                break
        b, h = 0, -1
        for i in parents:
            b |= past[i] | (1 << int(i))
            h = max(h, height[i])
        past[j] = b
        height[j] = h + 1
    return past, height

def links_of(past, j):
    covered = 0
    b = past[j]
    while b:
        low = b & -b
        i = low.bit_length() - 1
        covered |= past[i]
        b ^= low
    return bin(past[j] & ~covered).count("1")

def posts(past, N):
    full = (1 << N) - 1
    fut = [0] * N
    for j in range(N):
        b = past[j]
        while b:
            low = b & -b
            fut[low.bit_length() - 1] |= 1 << j
            b ^= low
    return [x for x in range(N) if (past[x] | fut[x] | (1 << x)) == full]

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    for label, kw in [("originary, fixed p = 0.02", dict(p=0.02, originary=True)),
                      ("originary, p = 3/n", dict(p=None, originary=True, c=3))]:
        past, h = grow(N, seed=1, **kw)
        layers = np.bincount(h)
        lk = np.array([links_of(past, j) for j in range(1, N)])
        print(f"\n{label}, N = {N}: {len(layers)} layers, mean past links {lk.mean():.2f}")
        print("  layer sizes:", layers.tolist())
    for p in [0.002, 0.01, 0.05]:
        past, h = grow(N, p)
        layers = np.bincount(h)
        lk = np.array([links_of(past, j) for j in range(N)])
        ps = posts(past, N)
        print(f"\np = {p}, N = {N}: {len(layers)} layers, {len(ps)} posts")
        print("  layer sizes (first 25):", layers[:25].tolist())
        late = lk[N // 2:]
        print(f"  past links per event: mean {lk.mean():.2f}, late half {late.mean():.2f}, max {lk.max()}")
