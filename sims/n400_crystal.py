"""N = 400 crystallisation check (ideas 002, 005): does e^{-beta S_BD} (eps = 0.21, 2D orders) crystallise at N = 400, and where?

Session 3: N = 400 at beta = 0.3 stayed continuum-like after ~300 sweeps. Either beta_c ~ 35/N is wrong, or the chain
had not equilibrated. To tell these apart, every (beta, seed) is run from two starts:
    hot   random u, v (a sprinkled diamond: continuum-like)
    cold  a layered "crystal": k antichains stacked on top of each other, every event of layer i below every event of
          layer i+1 (u and v blocks both increase from layer to layer; inside a layer u increases while v decreases,
          so the layer is an antichain). k is the layer count with the lowest action, scanned over k = 2..40.
If hot and cold end at the same values, the chain is equilibrated; if they stay apart, that's hysteresis
(metastability, as expected near a first-order transition: Surya 2012, Glaser-O'Connor-Surya 2018).

Same Metropolis swap moves and O(N^2) update as s3a_fast.py. Records every `every` sweeps: S/N, ordering fraction r,
number of layers (longest chain), acceptance since the previous record. Saves the final (u, v) too.
Usage: python n400_crystal.py N beta hot|cold seed n_sweeps outfile.npz [every]
Runs on Python 3.6 + numpy 1.19 (cluster).
"""
import os, sys, time
T0 = time.time()
import numpy as np
from s3a_mcmc_2d import f_weights, causal, observables
from s3a_fast import thin_left, thin_right, action_from

np.seterr(all="ignore")

def layered(N, k):
    """Cold start: k stacked antichains of (almost) equal size."""
    sizes = np.full(k, N // k); sizes[:N % k] += 1
    u, v = np.empty(N, int), np.empty(N, int)
    i = 0
    for s in sizes:
        u[i:i + s] = i + np.arange(s)              # block of u labels, increasing inside the layer
        v[i:i + s] = i + s - 1 - np.arange(s)      # same block of v labels, decreasing: no relations inside a layer
        i += s
    return u, v

def cold_start(N, eps, fw):
    best = None
    for k in range(2, 41):
        u, v = layered(N, k)
        C = causal(u, v)
        S = action_from(C, C @ C, eps, fw)
        if best is None or S < best[0]:
            best = (S, k, u, v)
    return best

def chain(N, beta, start, seed, n_sweeps, every=10, eps=0.21, on_record=None):
    rng = np.random.default_rng(seed)
    fw = f_weights(N, eps)
    if start == "hot":
        u, v, k0 = rng.permutation(N), rng.permutation(N), 0
    else:
        _, k0, u, v = cold_start(N, eps, fw)
    C = causal(u, v)
    K = C @ C
    S = action_from(C, K, eps, fw)
    rows, acc = [], 0
    for t in range(n_sweeps * N + 1):
        if t % (every * N) == 0:
            r, _, layers = observables(C)
            rows.append((t // N, S / N, r, layers, acc / (every * N) if t else np.nan))
            acc = 0
            if len(rows) % 10 == 1:                   # progress line every 10 records (500 sweeps on the cluster): speed shows up early
                print("sweep {} t={:.0f}s S/N={:.3f} layers={}".format(t // N, time.time() - T0, S / N, layers), flush=True)
            if on_record is not None:
                on_record(rows, u, v)
        w = u if rng.random() < 0.5 else v
        a, b = rng.integers(0, N, 2)
        if a == b:
            continue
        w[a], w[b] = w[b], w[a]
        P = np.array([a, b])
        C2 = C.copy()
        C2[P, :] = (u[P, None] < u[None, :]) & (v[P, None] < v[None, :])
        C2[:, P] = (u[:, None] < u[None, P]) & (v[:, None] < v[None, P])
        E = C2 - C
        K2 = K + thin_left(C2, E, P) + thin_right(E, C, P)
        S2 = action_from(C2, K2, eps, fw)
        if np.log(rng.random()) < -beta * (S2 - S):
            C, K, S = C2, K2, S2
            acc += 1
        else:
            w[a], w[b] = w[b], w[a]
    return np.array(rows), u, v, k0

if __name__ == "__main__":
    N, beta, start, seed, n_sweeps, out = (int(sys.argv[1]), float(sys.argv[2]), sys.argv[3], int(sys.argv[4]),
                                           int(sys.argv[5]), sys.argv[6])
    every = int(sys.argv[7]) if len(sys.argv) > 7 else 10
    assert start in ("hot", "cold")
    t0 = time.time()

    def save(path, ts, u, v, k0=-1):
        np.savez_compressed(path, N=N, beta=beta, start=start, seed=seed, eps=0.21, every=every, k0=k0, seconds=time.time() - t0,
                            sweep=ts[:, 0].astype(np.int32), S_N=ts[:, 1], r=ts[:, 2], layers=ts[:, 3].astype(np.int16),
                            acc=ts[:, 4], u=u.astype(np.int16), v=v.astype(np.int16))

    # Session 7: tasks killed by TIMEOUT lost everything (the result was only written at the end, inside /tmp).
    # Every 20 records (1000 sweeps on the cluster, ~15 min) overwrite one small partial file directly in the output folder.
    # k0 isn't known inside chain() yet, so the partial file stores k0 = -1. The CLI is unchanged, so pending array tasks pick this up.
    partial_dir = os.environ.get("N400_PARTIAL_DIR", os.path.expanduser("~/exp/physics/n400/out"))
    partial = os.path.join(partial_dir, os.path.basename(out).replace(".npz", ".partial.npz"))

    def checkpoint(rows, u, v):
        if len(rows) % 20 == 1 and len(rows) > 1 and os.path.isdir(partial_dir):
            save(partial, np.array(rows), u, v)

    ts, u, v, k0 = chain(N, beta, start, seed, n_sweeps, every, on_record=checkpoint)
    dt = time.time() - t0
    save(out, ts, u, v, k0)
    if os.path.exists(partial):
        os.remove(partial)
    print("N={} beta={} {} seed={} sweeps={}: {:.1f} s ({:.3f} s/sweep), cold k0={}; final S/N={:.3f} r={:.3f} layers={}"
          .format(N, beta, start, seed, n_sweeps, dt, dt / n_sweeps, k0, ts[-1, 1], ts[-1, 2], int(ts[-1, 3])), flush=True)
