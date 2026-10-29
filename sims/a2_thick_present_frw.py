"""A2, option 2: thick present in closed 2D FRW universes, decelerating vs accelerating (idea 004, session 5).

Any 2D FRW metric is conformally flat: ds^2 = a(eta)^2 (-d eta^2 + dx^2), x on a circle of comoving length W. Causal order
is the static cylinder's in (eta, x); the sprinkling density is a(eta)^2 d eta dx. Criterion to test: the memory closes
(old events retire) iff a light cone can wrap, i.e. iff conformal time left after an event exceeds W/2.
  radiation-like, decelerating:  a ~ t^{1/2}  =>  a ~ eta,       eta in [e0, e1] > 0 (conformal time grows without bound)
  power-law accelerating:        a ~ t^2      =>  a ~ eta^{-2},  eta in [e0, e1] < 0 (conformal time bounded above by 0)
Births in cosmic time (= eta order). Hindsight state as in a2_thick_present.py, n_cut = 10.
Usage: python a2_thick_present_frw.py
"""
import numpy as np
from a2_thick_present_desitter import needed

np.seterr(all="ignore")

def sprinkle(rng, W, e0, e1, power, N):
    """eta with density ~ |eta|^power on [e0, e1] (rejection), x uniform."""
    grid = np.linspace(e0, e1, 20001); dens = np.abs(grid) ** power; cdf = np.cumsum(dens); cdf /= cdf[-1]
    eta = np.sort(np.interp(rng.uniform(0, 1, N), cdf, grid))
    return eta, rng.uniform(0, W, N)

if __name__ == "__main__":
    rng = np.random.default_rng(9)
    W, N = 4.0, 1500
    for name, e0, e1, power in (("decelerating a~eta (radiation)", 1.0, 16.0, 2), ("accelerating a~eta^-2 (a~t^2)", -16.0, -0.3, -4)):
        eta, x = sprinkle(rng, W, e0, e1, power, N)
        last = needed(eta, x, W, 10)
        print("\n{}: conformal time [{}, {}], W = {}, N = {}".format(name, e0, e1, W, N))
        print("  k/N   state/born   first 10% still needed   conformal age of oldest needed event (units of W)")
        for f in (0.3, 0.5, 0.7, 0.9):
            k = int(f * N); alive = (np.arange(N) <= k) & (last > k); old = np.arange(N) <= int(0.1 * N)
            print("  {:.1f}   {:.2f}         {:.2f}                     {:.2f}".format(
                f, alive.sum() / (k + 1), (alive & old).sum() / old.sum(), (eta[k] - eta[alive].min()) / W))
