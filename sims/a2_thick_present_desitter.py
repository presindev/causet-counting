"""A2, option 2: the thick present in an expanding closed universe (idea 004, session 5).

Closed 2D de Sitter in flat slicing, H = 1: ds^2 = (-d eta^2 + dx^2) / eta^2, conformal time eta in [eta0, eta1] < 0,
space a circle of comoving length W. Proper (cosmic) time t = -ln(-eta). Light cones are those of the static cylinder in
(eta, x), so x precedes y iff eta_y - eta_x > circular |x_y - x_x|. Sprinkle at density rho: dV = d eta dx / eta^2, so
eta has density ~ 1/eta^2 and x is uniform. A light cone wraps around space after conformal time W/2, but conformal time
left is |eta1 - eta| -> events born late never wrap. Question: do they stay "needed" (n_xf <= n_cut for a later birth f)
forever, or does expansion (many events in between) retire them anyway?
Births in cosmic time (the frame of the state, C5). State and closure as in a2_thick_present.py (hindsight, lower bound).
Reported per cosmic-time checkpoint: state size; events born in the last Hubble time (the "thin present"); share of the state
older than 1 and 2 Hubble times. C1-C8: births ordered by a relational-ish cosmic time (bookkeeping, C5); no record.
Usage: python a2_thick_present_desitter.py
"""
import numpy as np

np.seterr(all="ignore")

def sprinkle(rng, W, eta0, eta1, rho):
    N = rng.poisson(rho * W * (1 / -eta1 - 1 / -eta0))
    w = rng.uniform(1 / -eta0, 1 / -eta1, N)          # 1/|eta| uniform <=> density ~ 1/eta^2
    eta = -1 / w
    x = rng.uniform(0, W, N)
    o = np.argsort(eta)
    return eta[o], x[o]

def needed(eta, x, W, n_cut):
    dx = np.abs(x[None, :] - x[:, None]); dx = np.minimum(dx, W - dx)
    C = ((eta[None, :] - eta[:, None]) > dx).astype(np.float64)
    K = C @ C
    need = (C > 0) & (K <= n_cut)
    N = len(eta)
    last = np.where(need.any(1), (need * np.arange(N)[None, :]).max(1), -1)   # births are already in time order
    return last

if __name__ == "__main__":
    rng = np.random.default_rng(7)
    n_cut = 10
    for W, eta0, eta1, rho in ((4.0, -4.0, -0.1, 40.0), (4.0, -4.0, -0.05, 20.0), (8.0, -16.0, -0.2, 30.0)):
        eta, x = sprinkle(rng, W, eta0, eta1, rho)
        N = len(eta)
        t = -np.log(-eta)
        last = needed(eta, x, W, n_cut)
        print("\nW = {} (comoving), eta in [{}, {}], rho = {}: N = {}, cosmic time t in [{:.2f}, {:.2f}]; light cones of events"
              " born after t = {:.2f} never wrap".format(W, eta0, eta1, rho, N, t[0], t[-1], -np.log(-(eta1 - W / 2)) if eta1 - W / 2 < 0 else np.inf))
        print("  t      state   born in last 1/H   state older than 1/H   older than 2/H   never retired (needed by the last 5% of births)")
        for tc in np.linspace(t[0] + 0.25 * (t[-1] - t[0]), t[-1] - 0.1 * (t[-1] - t[0]), 5):
            k = np.searchsorted(t, tc)
            born = np.arange(N) <= k
            alive = born & (last > k)
            age = tc - t
            late = last >= int(0.95 * N)
            print("  {:5.2f}  {:5d}   {:5d}              {:.2f}                   {:.2f}             {:.2f}".format(
                tc, alive.sum(), (born & (age < 1)).sum(), (alive & (age > 1)).sum() / max(alive.sum(), 1),
                (alive & (age > 2)).sum() / max(alive.sum(), 1), (alive & late).sum() / max(alive.sum(), 1)))
