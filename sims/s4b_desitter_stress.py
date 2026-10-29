"""Stage S4b (idea 005): does the flat-embedding misfit (stress) grow with curvature?

de Sitter (H = 1) causal diamonds from p = (eta_p, 0) to q = (eta_q, 0), proper height tau = ln(eta_p / eta_q),
sprinkled with a fixed expected N events (density chosen per diamond), so noise stays constant while H tau grows.
In (u, v) = (eta - x, eta + x) the diamond is the square [eta_p, eta_q]^2 with density proportional to 1 / (u + v)^2.
A diamond is causally closed, so the detector sees a self-contained causal set. Flat control: H tau -> 0.
"""
import numpy as np
from s4b_detector import diagnostics

def desitter_diamond(N, tau, rng):
    eta_q = -1.0
    eta_p = eta_q * np.exp(tau)
    pts = []
    wmax = 1 / (2 * eta_q) ** 2                       # density 1/(u+v)^2 is largest at the top corner
    while sum(len(p) for p in pts) < 50 * N:          # rejection sampling, then thin to a Poisson(N) count
        u, v = eta_p + (eta_q - eta_p) * rng.random((2, 20 * N))
        keep = rng.random(20 * N) < (1 / (u + v) ** 2) / wmax
        pts.append(np.column_stack([u[keep], v[keep]]))
    P = np.concatenate(pts)
    P = P[rng.choice(len(P), rng.poisson(N), replace=False)]
    u, v = P[:, 0], P[:, 1]
    return (u[:, None] < u[None, :]) & (v[:, None] < v[None, :])

if __name__ == "__main__":
    rng = np.random.default_rng(11)
    N, reps = 400, 8
    print(f"de Sitter diamonds, N = {N}, {reps} per height; flat calibration at N = 400: stress 0.10, r+ 0.08")
    for tau in (0.05, 0.5, 1.0, 2.0, 3.0, 4.0):
        D = np.array([diagnostics(desitter_diamond(N, tau, rng)) for _ in range(reps)])
        m, s = D.mean(0), D.std(0)
        print(f"  H tau = {tau:4.2f}: w2 {m[0]:.2f}±{s[0]:.2f}  r+ {m[1]:.2f}±{s[1]:.2f}  r- {m[2]:.2f}±{s[2]:.2f}"
              f"  stress {m[3]:.2f}±{s[3]:.2f}", flush=True)
