"""Height (number of layers = longest chain) of random two-dimensional orders at N = 400 and 800 (session 20; 1+1 referee round 4, comment 28c).

A random 2D order (a sprinkled flat diamond) is the dominance order of two random permutations; its longest chain is the longest increasing
subsequence of one random permutation. Context only for the N = 800 held-out flag test (r27): the false positive has 27 layers.
Usage: python3 sims/r42_flat_height.py   (laptop, seconds; writes sims/out/r42_flat_height.txt)
"""
import bisect
import os
import numpy as np

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "r42_flat_height.txt")

def height(p):
    tails = []
    for x in p:
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)

if __name__ == "__main__":
    rng = np.random.default_rng(800)
    lines = []
    for N in (400, 800):
        h = np.array([height(rng.permutation(N)) for _ in range(2000)])
        lines.append(f"N = {N}: height of 2000 random 2D orders: mean {h.mean():.1f}, sd {h.std(ddof=1):.1f}, range {h.min()}-{h.max()} (2 sqrt N = {2 * N ** 0.5:.1f})")
    open(OUT, "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))
