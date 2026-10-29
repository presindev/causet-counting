"""A2 memory question (idea 004, session 6): how much memory does ONE observer's de Sitter patch need?

Session 5: in closed accelerating universes the global thick present is the whole past. But an observer only ever sees a static
patch. 2D de Sitter, flat slicing, H = 1: ds^2 = (-d eta^2 + dx^2) / eta^2, x on the real line. Observer at x = 0; their patch is
the past of the future endpoint (eta, x) = (0, 0), i.e. |x| < -eta. The interval between two patch events lies in the patch, so
counts n_xf use patch events only. Patch volume per cosmic time t = -ln(-eta) is 2, so 2 rho events per Hubble time (stationary).
Thick present at cosmic time t_now: patch events born before t_now that some patch event born after t_now still needs
(x < f, n_xf <= n_cut). Hindsight state, lower bound (future cut at t1, checked with a longer buffer).
Scaling with rho = 1/(l H)^2: area law ~ const or ln rho; space-volume ~ sqrt(rho); spacetime-volume ~ rho.
C1-C8: births ordered by cosmic time only for bookkeeping (C5); "needed" is a count of events between (clock-free). No record.
Usage: python a2_memory_static_patch.py
"""
import sys
import numpy as np

def sprinkle(rng, rho, t0, t1):
    # proper density rho; in the patch dN = rho * 2 dt, and x uniform in (-|eta|, |eta|) at each eta
    N = rng.poisson(2 * rho * (t1 - t0))
    t = np.sort(rng.uniform(t0, t1, N))
    eta = -np.exp(-t)
    x = rng.uniform(-1, 1, N) * (-eta)
    return t, eta, x

def last_needed(eta, x, n_cut, block=2048):
    """For each event, index of the latest event that still needs it (-1 if none). Events sorted by t."""
    u, v = eta - x, eta + x
    N = len(eta)
    C = ((u[:, None] < u[None, :]) & (v[:, None] < v[None, :])).astype(np.float32)   # C[i, j] = 1 iff i < j
    last = np.full(N, -1)
    idx = np.arange(N)
    for s in range(0, N, block):
        Cb = C[s:s + block]
        K = Cb @ C                                    # events strictly between
        need = (Cb > 0) & (K <= n_cut)
        last[s:s + block] = np.where(need.any(1), (need * idx[None, :]).max(1), -1)
    return last

def thick_present(t, last, t_now):
    k = np.searchsorted(t, t_now)                    # born: indices < k
    alive = last[:k] >= k
    return alive.sum(), alive

if __name__ == "__main__":
    n_cut = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    rng = np.random.default_rng(11)
    t0, t1 = 0.0, 7.0
    nows = (2.0, 3.0, 4.0)
    print("n_cut = {}; patch events per Hubble time = 2 rho; t in [{}, {}]".format(n_cut, t0, t1))
    print(" rho   N     state at t_now = {}   mean   /rho   /sqrt(rho)  median age of state (Hubble times)".format(nows))
    for rho in (25, 50, 100, 200, 400):
        reps = max(1, 800 // rho)
        S, ages = [], []
        for r in range(reps):
            t, eta, x = sprinkle(rng, rho, t0, t1)
            last = last_needed(eta, x, n_cut)
            for tn in nows:
                n, alive = thick_present(t, last, tn)
                S.append(n)
                ages.append(np.median(tn - t[:len(alive)][alive]) if n else np.nan)
        S = np.array(S, float).reshape(reps, len(nows))
        m = S.mean()
        print("{:4d} {:5d}   {}   {:6.1f}  {:5.2f}  {:6.2f}     {:.2f}".format(
            rho, len(t), "  ".join("{:6.1f}".format(v) for v in S.mean(0)), m, m / rho, m / np.sqrt(rho), np.nanmean(ages)))
