"""A2 steps 2-3: exact quantum sums (N <= 9) with the action truncated to thick layers, under two clocks.

Universes: as in s3q_exact_quantum.py, u = identity and every permutation v gives one 2D order (uniform sprinkling
measure, N! universes). Action S = 4 eps (N - 2 eps sum_{pairs x<y} f(n_xy, eps)), eps = 0.21.
Two relational layerings (C5 clocks):
  height  h(x)  = longest chain ending at x, from the minimal events (h = 0 for minimal events). Related pairs have gap >= 1.
  volume  hv(x) = floor(c sqrt(|J^-(x)|)), |J^-(x)| = number of events in the causal past of x (x excluded). Monotone,
                  so events between x and y lie in layers hv(x)..hv(y) (weakly; related pairs can share a layer, gap >= 0).
                  c is fitted at each N, either so that the mean number of volume layers equals the mean number of height
                  layers (calibration "layers"), or so that the mean layer gap of related pairs is the same for both clocks
                  (calibration "gap"). With few events floor() makes the volume clock coarse, so both are reported, with the
                  share of related pairs each truncation drops.
Truncated action S_m (clock k): keep only pairs with gap_k <= m. This is the action a transfer matrix with a memory of
m layers would see. Only the AMPLITUDE is truncated: the set of allowed universes (2D orders) and their uniform
measure are not themselves layer-Markov, so this tests the amplitude half of a transfer matrix, not the whole thing.
Records (lesson 3: universes with the same record interfere), all from HEIGHT so both truncations are compared on the
same observable:  AGE = number of height layers;  PRESENT = number of maximal events (as in s3q);  LAST = size of the
top height layer;  PRESENT2 = (size of top layer, size of second layer). Secondary: AGE_v = number of volume layers.
    P_q(r) = |A_r|^2 / sum |A|^2,  A_r = sum_{record r} e^{i beta S_m};   TV = (1/2) sum_r |P_q,m - P_q,exact|
C1-C8: uses only the order (C1, C2); the clocks are relational (C5) and the clock-swap test is exactly C5's demand
that predictions not depend on the clock. No new dynamics is introduced.
Usage: python a2_truncated_sums.py N
"""
import sys, itertools, time
import numpy as np
from s3a_mcmc_2d import f_weights

np.seterr(all="ignore")
EPS = 0.21
BETAS = (1.0, 2.0, 4.0, 8.0)
MS = (1, 2, 3, 4, 5)

def batch_quantities(V, fw, N):
    """V: (B, N) permutations. Returns causal matrices' derived data for the batch."""
    u = np.arange(N)
    C = ((u[None, :, None] < u[None, None, :]) & (V[:, :, None] < V[:, None, :])).astype(np.float64)
    K = C @ C
    h = np.zeros(V.shape, dtype=int)
    for j in range(N):                                  # u-order is a linear extension
        h[:, j] = ((h[:, :j] + 1) * C[:, :j, j]).max(1) if j else 0
    past = C.sum(1).astype(int)
    F = fw[K.astype(int)] * C                           # f(n_xy) on related pairs, 0 elsewhere
    return C, F, h, past

def enumerate_all(N, batch=40320):
    fw = f_weights(N, EPS)
    perms = np.array(list(itertools.permutations(range(N))), dtype=np.int8)
    out = {k: [] for k in ("S", "Sh", "AGE", "PRESENT", "LAST", "PRESENT2")}
    Fs, pasts, hs = [], [], []
    for s in range(0, len(perms), batch):
        C, F, h, past = batch_quantities(perms[s:s + batch].astype(int), fw, N)
        G = h[:, None, :] - h[:, :, None]               # height gap h(y) - h(x) for pair (x, y)
        out["S"].append(4 * EPS * (N - 2 * EPS * F.sum((1, 2))))
        out["Sh"].append(np.stack([4 * EPS * (N - 2 * EPS * (F * (G <= m)).sum((1, 2))) for m in MS], 1))
        top = h.max(1)
        out["AGE"].append(top + 1)
        out["PRESENT"].append((C.sum(2) == 0).sum(1))
        last = (h == top[:, None]).sum(1)
        second = (h == (top - 1)[:, None]).sum(1)
        out["LAST"].append(last)
        out["PRESENT2"].append(100 * last + second)
        Fs.append(F); pasts.append(past); hs.append(h)
    res = {k: np.concatenate(v) for k, v in out.items() if v}
    return res, Fs, pasts, hs

def mean_gap(Fs, layers):
    tot = cnt = 0
    for F, L in zip(Fs, layers):
        G = L[:, None, :] - L[:, :, None]
        tot += G[F != 0].sum(); cnt += (F != 0).sum()
    return tot / cnt

def volume_truncation(res, Fs, pasts, N, hs, cal="layers"):
    """Fit c (see docstring); return S_m under volume layering, AGE_v, c, gap check, dropped-pair shares."""
    allpast = np.concatenate(pasts)
    if cal == "layers":
        target = res["AGE"].mean()
        stat = lambda c: (np.floor(c * np.sqrt(allpast)).max(1) + 1).mean()
    else:
        target = mean_gap(Fs, hs)
        stat = lambda c: mean_gap(Fs, [np.floor(c * np.sqrt(p)).astype(int) for p in pasts])
    lo, hi = 0.01, 20.0
    for _ in range(40):
        c = 0.5 * (lo + hi)
        lo, hi = (c, hi) if stat(c) < target else (lo, c)
    Sv, agev, gaps_ok = [], [], True
    drop = np.zeros((2, len(MS))); npairs = 0
    for F, past, h in zip(Fs, pasts, hs):
        hv = np.floor(c * np.sqrt(past)).astype(int)
        G = hv[:, None, :] - hv[:, :, None]
        Gh = h[:, None, :] - h[:, :, None]
        gaps_ok &= bool(np.all(G[F != 0] >= 0))
        rel = F != 0
        npairs += rel.sum()
        drop[0] += [(rel & (Gh > m)).sum() for m in MS]
        drop[1] += [(rel & (G > m)).sum() for m in MS]
        Sv.append(np.stack([4 * EPS * (N - 2 * EPS * (F * (G <= m)).sum((1, 2))) for m in MS], 1))
        agev.append(hv.max(1) + 1)
    return np.concatenate(Sv), np.concatenate(agev), c, gaps_ok, drop / npairs

def pq(S, rec, beta):
    rs = np.unique(rec)
    amp = np.exp(1j * beta * S)
    A = np.array([amp[rec == r].sum() for r in rs])
    return np.abs(A) ** 2 / (np.abs(A) ** 2).sum()

def tv(p, q):
    return 0.5 * np.abs(p - q).sum()

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    cal = sys.argv[2] if len(sys.argv) > 2 else "layers"
    t0 = time.time()
    res, Fs, pasts, hs = enumerate_all(N)
    Sv, agev, c, gaps_ok, drop = volume_truncation(res, Fs, pasts, N, hs, cal)
    res["AGE_v"] = agev
    print(f"N={N}: {len(res['S'])} universes in {time.time()-t0:.1f} s; volume clock ({cal} calibration) c = {c:.4f} "
          f"(mean layers {res['AGE'].mean():.3f} height / {agev.mean():.3f} volume); related pairs have hv-gap >= 0: {gaps_ok}")
    print("  share of related pairs dropped, height / volume: "
          + "  ".join(f"m={m}: {a:.3f}/{b:.3f}" for m, a, b in zip(MS, drop[0], drop[1])))
    for name in ("AGE", "PRESENT", "LAST", "PRESENT2", "AGE_v"):
        rec = res[name]
        print(f"\n record = {name} ({len(np.unique(rec))} values).  TV distance from exact P_q;  'h' = height-truncated, 'v' = volume-truncated")
        print("   beta   " + "   ".join(f"m={m}: h / v / h-v " for m in MS))
        for beta in BETAS:
            ex = pq(res["S"], rec, beta)
            cells = []
            for k, m in enumerate(MS):
                ph, pv = pq(res["Sh"][:, k], rec, beta), pq(Sv[:, k], rec, beta)
                cells.append(f"{tv(ph, ex):.3f}/{tv(pv, ex):.3f}/{tv(ph, pv):.3f}")
            print(f"   {beta:4.1f}   " + "   ".join(cells))
        if name == "AGE":
            for beta in BETAS:
                ex = pq(res["S"], rec, beta)
                print(f"   exact P_q(AGE) beta={beta}: " + "  ".join(f"{r}:{p:.3f}" for r, p in zip(np.unique(rec), ex)))
