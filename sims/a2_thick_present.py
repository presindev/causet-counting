"""A2, option 2, closure: how big is the "thick present", the set of past events that later births still need? (idea 004, session 5)

Growth under internal temporality (Roberto / Rideout-Sorkin): events of a 2D order are born along a linear extension,
here the time t = e^{-theta} u + e^{theta} v of a frame boosted by theta (theta = 0: the diamond's rest frame).
A new event f needs past event x if n_xf <= n_cut (events strictly between; see a2_causal_memory.py).
Closure: if f needs x, then every z strictly between x and f has n_zf < n_xf, so f needs z too. So the interval [x, f],
and with it f's truncated action change, lies inside the set of needed events: a state holding them is self-contained.
The minimal state after k births, in hindsight: born events that some later birth still needs,
    state(k) = #{x born <= k : x is needed by a birth after k}.
This is a lower bound on any state that works without knowing the future. Size vs N decides whether option 2 is a small
transfer operator. Frame check: the physics (S) doesn't depend on the birth order, but the state size might.
C1-C8: birth order is bookkeeping (C5); the needed-relation is a count (Lorentz-invariant). No record (no quantum sum).
Usage: python a2_thick_present.py
"""
import numpy as np
from s3a_mcmc_2d import causal

np.seterr(all="ignore")

def state_sizes(u, v, n_cut, theta):
    C = causal(u, v)
    K = C @ C
    order = np.argsort(np.exp(-theta) * u + np.exp(theta) * v, kind="stable")
    birth = np.empty(len(u), int)
    birth[order] = np.arange(len(u))
    need = (C > 0) & (K <= n_cut)                          # need[x, f]: f needs x
    last = np.where(need.any(1), (need * birth[None, :]).max(1), -1)   # last birth that needs x
    k = np.arange(len(u))
    # state(k): born at or before k, still needed after k
    return ((birth[None, :] <= k[:, None]) & (last[None, :] > k[:, None])).sum(1)

if __name__ == "__main__":
    rng = np.random.default_rng(11)
    n_cut = 10
    print("n_cut = {}; state size = minimal thick present (hindsight); 2D diamond sprinklings".format(n_cut))
    for theta in (0.0, 1.0):
        print("\nbirth order = time in a frame boosted by theta = {}".format(theta))
        print("    N   max state   state at k=N/2   max/N   max/sqrt(N)")
        for N, reps in ((100, 20), (200, 12), (400, 8), (800, 4), (1600, 2)):
            mx, mid = [], []
            for _ in range(reps):
                s = state_sizes(rng.permutation(N), rng.permutation(N), n_cut, theta)
                mx.append(s.max()); mid.append(s[N // 2])
            mx, mid = np.array(mx), np.array(mid)
            print("  {:5d}   {:6.1f}±{:4.1f}   {:6.1f}±{:4.1f}      {:.3f}   {:.2f}".format(
                N, mx.mean(), mx.std(), mid.mean(), mid.std(), mx.mean() / N, mx.mean() / np.sqrt(N)))

def cylinder(rng, W, T):
    """Sprinkle N = W*T events (density 1) on a cylinder: space a circle of length W, time [0, T].
    x precedes y iff t_y - t_x > circular distance |x_y - x_x| (light cones wrap around space)."""
    N = W * T
    t, x = rng.uniform(0, T, N), rng.uniform(0, W, N)
    dx = np.abs(x[None, :] - x[:, None]); dx = np.minimum(dx, W - dx)
    C = ((t[None, :] - t[:, None]) > dx).astype(np.float64)
    return C, t

def state_sizes_C(C, t, n_cut):
    K = C @ C
    N = len(t)
    birth = np.empty(N, int); birth[np.argsort(t, kind="stable")] = np.arange(N)
    need = (C > 0) & (K <= n_cut)
    last = np.where(need.any(1), (need * birth[None, :]).max(1), -1)
    k = np.arange(N)
    s = ((birth[None, :] <= k[:, None]) & (last[None, :] > k[:, None])).sum(1)
    life = np.sort(t)[np.clip(last, 0, None)] - t                  # how long each event stays needed (in time units)
    return s, life[last >= 0]

if __name__ == "__main__":
    print("\nclosed space (cylinder, circle of length W, density 1), birth order = cylinder time; n_cut = 10")
    print("    W     T      N   state (middle third, mean)   state/W^2   median / 90% 'needed' lifetime in units of W")
    for W in (10, 15, 20):
        for T in (2 * W, 4 * W, 8 * W):
            if W * T > 2500:
                continue
            C, t = cylinder(rng, W, T)
            s, life = state_sizes_C(C, t, 10)
            N = W * T
            mid = s[N // 3: 2 * N // 3].mean()
            print("  {:3d}  {:4d}  {:5d}   {:8.1f}                      {:5.2f}       {:.2f} / {:.2f}".format(
                W, T, N, mid, mid / W**2, np.median(life) / W, np.percentile(life, 90) / W))
