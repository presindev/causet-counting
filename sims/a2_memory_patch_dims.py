"""A2 memory question in d = 2, 3, 4 (idea 004, session 6): static-patch memory and its horizon surplus.

de Sitter, flat slicing, H = 1: ds^2 = (-d eta^2 + dx^2) / eta^2, x in R^{d-1}. Static patch of the observer at x = 0:
|x| < -eta. Patch volume per cosmic time t = -ln(-eta) is V_ball(d-1) (2, pi, 4 pi / 3), so V_ball * rho births per Hubble time.
State at t_now = patch events born before t_now that a later patch birth still needs (x < f, n_xf <= n_cut); as in
a2_memory_static_patch.py (d = 2 reproduces it).
Scalings with rho = 1/(l H)^d: area ~ rho^{(d-2)/d} (log in d = 2), space volume ~ rho^{(d-1)/d}, spacetime volume ~ rho.
Horizon surplus: shells in the static radius r = |x|/|eta| (1 = horizon). In each shell, memory depth = state / births in the
last Hubble time. Surplus = sum over shells of (depth - bulk depth) * births per Hubble time, bulk = mean depth for r < 0.5.
Usage: python a2_memory_patch_dims.py d [rho ...]
"""
import sys
import numpy as np
from math import gamma, pi

def vball(n):
    return pi ** (n / 2) / gamma(n / 2 + 1)

def sprinkle(rng, d, rho, t0, t1):
    N = rng.poisson(vball(d - 1) * rho * (t1 - t0))
    t = np.sort(rng.uniform(t0, t1, N))
    eta = -np.exp(-t)
    g = rng.normal(size=(N, d - 1))
    g /= np.linalg.norm(g, axis=1)[:, None]
    r = rng.uniform(0, 1, N) ** (1 / (d - 1))                  # uniform in the ball of radius |eta|
    return t, eta, g * (r * -eta)[:, None], r

def last_needed(eta, x, n_cut, block=1024):
    N = len(eta)
    last = np.full(N, -1)
    idx = np.arange(N)
    C = np.zeros((N, N), dtype=np.float32)
    for s in range(0, N, block):
        dx = np.linalg.norm(x[s:s + block, None, :] - x[None, :, :], axis=2)
        C[s:s + block] = (eta[None, :] - eta[s:s + block, None]) > dx
    for s in range(0, N, block):
        Cb = C[s:s + block]
        with np.errstate(all="ignore"):                         # spurious Accelerate matmul warnings
            K = Cb @ C
        need = (Cb > 0) & (K <= n_cut)
        last[s:s + block] = np.where(need.any(1), (need * idx[None, :]).max(1), -1)
    return last

if __name__ == "__main__":
    d = int(sys.argv[1])
    rhos = [float(a) for a in sys.argv[2:]] or [25, 50, 100, 200, 400]
    n_cut, t0, t1, nows = 10, 0.0, 8.0, (2.5, 3.0, 3.5)
    edges = np.array([0, 0.5, 0.8, 0.9, 0.95, 0.98, 1.0])
    rng = np.random.default_rng(100 + d)
    print(f"d = {d}, n_cut = {n_cut}, t in [{t0}, {t1}], now = {nows}; births per Hubble time = {vball(d - 1):.3f} rho", flush=True)
    print("  rho      N   state  state/rho  depth(bulk)  surplus  depth by shell r =", edges[1:], flush=True)
    for rho in rhos:
        reps = max(1, int(round(400 / rho)))
        st, sh_state, sh_born = [], np.zeros(len(edges) - 1), np.zeros(len(edges) - 1)
        for _ in range(reps):
            t, eta, x, r = sprinkle(rng, d, rho, t0, t1)
            last = last_needed(eta, x, n_cut)
            for tn in nows:
                k = np.searchsorted(t, tn)
                alive = last[:k] >= k
                st.append(alive.sum())
                sh_state += np.histogram(r[:k][alive], edges)[0]
                sh_born += np.histogram(r[:k][t[:k] > tn - 1], edges)[0]
        n = reps * len(nows)
        depth = sh_state / np.maximum(sh_born, 1)
        bulk = depth[0]
        surplus = ((depth - bulk) * sh_born).sum() / n
        print(f"{rho:6.0f} {len(t):6d} {np.mean(st):7.1f}  {np.mean(st) / rho:7.2f}    {bulk:6.2f}     {surplus:7.1f}   "
              + " ".join(f"{v:.2f}" for v in depth), flush=True)
