"""Poisson likelihood on the slab (idea 005, session 13): does the large-n winner of the diamond (r24, related-pair Poisson term only) survive a shape
without tips? The related-pair term needs no reference event, so it is tip-free as it stands. Same pipeline as r22 (true t for every arm, his 2-leg detour
with 4-leg fallback, our multi-reference overlap step, double-centred MDS, count-weighted SMACOF K0 = 100 as the start).
Gauge: no pinned events; the gradient's mean is removed (translations), rotations are irrelevant to the score.
Known bias to watch: an interval between two slab events can poke out of the side wall (|x| <= R), so its count is low and tau is underestimated near the
wall; the diamond has no such clipping (it is causally convex). Diagnosed by the interior score (r22's core pairs) and by the share of clipped related pairs
(truth used for the diagnosis only).
Equal density on the cluster: the slab (R = 0.5) has 4x the diamond's volume, so slab n = 4 x diamond n (sims/cluster/r25_job.sh); one universe per task.
Usage: python r25_slab_lik.py [n reps seed iters]  |  python r25_slab_lik.py one <shape> n seed out.npz [iters]  |  python r25_slab_lik.py analyse <folder>
       python r25_slab_lik.py check
"""
import glob
import sys
import time
import numpy as np
from r11_4d_distance import load_table, uniform_in_diamond
from r16_local_fit import smacof
from r22_slab import sprinkle, mds3, related_R, detour, ours_multiref, sym, R_SLAB

np.seterr(all="ignore")
C4 = np.pi / 24

def rl_setup(Cf, C, rho):
    """Related pairs and their strictly-between counts, Gaussian form for tau^2 (as r23)."""
    N = Cf @ Cf
    A, B = np.nonzero(np.triu(C | C.T, 1))
    Nab = np.maximum(N[A, B], N[B, A]).astype(float)
    t2 = np.sqrt((Nab + 0.5) / (rho * C4))
    return dict(A=A, B=B, t2=t2, sd=t2 / (2 * np.sqrt(Nab + 1)))

def inside_share(a, b, rng, m=256, chunk=10000):
    """ORACLE (truth used, diagnosis only): share of the interval I(a, b) inside the slab, by m uniform points per pair: rest-frame diamond samples
    boosted to the lab (boosts preserve 4-volume, so uniform stays uniform)."""
    U = uniform_in_diamond(m, 1.0, rng)                               # unit-height rest-frame diamond, from the origin
    f = np.empty(len(a))
    for lo in range(0, len(a), chunk):
        A, B = a[lo:lo + chunk], b[lo:lo + chunk]
        dt = B[:, 0] - A[:, 0]; dx = B[:, 1:] - A[:, 1:]
        tau = np.sqrt(np.maximum(dt ** 2 - (dx ** 2).sum(1), 1e-12))
        v = dx / dt[:, None]; sp = np.sqrt((v ** 2).sum(1)); g = 1 / np.sqrt(1 - sp ** 2)
        nh = v / np.maximum(sp, 1e-12)[:, None]
        s0 = tau[:, None] * U[None, :, 0]; y = tau[:, None, None] * U[None, :, 1:]
        vy = (y * v[:, None]).sum(2); ny = (y * nh[:, None]).sum(2)
        x = A[:, None, 1:] + y + (((g - 1)[:, None] * ny + (g * sp)[:, None] * s0)[:, :, None]) * nh[:, None]
        f[lo:lo + chunk] = ((x ** 2).sum(2) <= R_SLAB ** 2).mean(1)
    return f

def loglik(x, t, Rl):
    n = len(x)
    dx = x[Rl["B"]] - x[Rl["A"]]
    tau2 = (t[Rl["B"]] - t[Rl["A"]]) ** 2 - (dx ** 2).sum(1)
    r = (tau2 - Rl["t2"]) / Rl["sd"]
    gv = (2 * r / Rl["sd"])[:, None] * dx
    g = np.column_stack([np.bincount(Rl["B"], gv[:, k], n) - np.bincount(Rl["A"], gv[:, k], n) for k in range(3)])
    return -0.5 * (r ** 2).sum(), g - g.mean(0)

def fit(x0, t, Rl, iters=400):
    """Adam ascent, as r23.fit but without pinned tips."""
    x = x0.copy(); lr = 0.01 * np.std(x0)
    m = np.zeros_like(x); v = np.zeros_like(x); hist = []
    for k in range(1, iters + 1):
        L, g = loglik(x, t, Rl)
        m = 0.9 * m + 0.1 * g; v = 0.999 * v + 0.001 * g ** 2
        x += lr * (m / (1 - 0.9 ** k)) / (np.sqrt(v / (1 - 0.999 ** k)) + 1e-12)
        if k % 50 == 0 or k == 1:
            hist.append((k, L))
        if k == iters // 2:
            lr *= 0.3
    return x, hist

def check():
    """Gradient vs finite differences on a small slab."""
    rng = np.random.default_rng(12)
    P, C, rho = sprinkle("slab", 300, rng)
    t = P[:, 0]; Rl = rl_setup(C.astype(np.float32), C, rho)
    x = P[:, 1:] + 0.02 * rng.standard_normal((len(P), 3))
    L, g = loglik(x, t, Rl)
    out = []
    for (i, k) in [(5, 0), (50, 1), (200, 2)]:
        h = 1e-6; xp = x.copy(); xp[i, k] += h; xm = x.copy(); xm[i, k] -= h
        num = (loglik(xp, t, Rl)[0] - loglik(xm, t, Rl)[0]) / (2 * h)
        out.append((g[i, k] + g[:, k].mean(), num))                  # undo the gauge projection for the comparison
    print("gradient check (analytic, numeric):", ", ".join("%.5g/%.5g" % o for o in out))

NAMES = ["johnston", "switch", "w_K100", "poisson", "oracle_wall"]

def universe(shape, n, rng, W, iters, save=lambda **k: None):
    """One universe through every arm. Returns scores (all pairs, interior pairs) per arm, timings, wall diagnosis; calls save() after each stage."""
    T, res = {}, {}
    t0 = time.time()
    P, C, rho = sprinkle(shape, n, rng)
    t = P[:, 0]
    iu = np.triu_indices(len(P), 1)
    Dt = np.sqrt(((P[:, None, 1:] - P[None, :, 1:]) ** 2).sum(-1))[iu]
    v = np.minimum(C.sum(0), C.sum(1))
    core = v >= np.quantile(v, 0.75)
    incore = (core[:, None] & core[None, :])[iu]
    def sc(Y):
        e = np.sqrt(((Y[:, None] - Y[None]) ** 2).sum(-1))[iu]
        return np.corrcoef(e, Dt)[0, 1], np.corrcoef(e[incore], Dt[incore])[0, 1]
    def done(name, Y):
        res[name] = sc(Y); save(npts=len(P), res=res, T=T)
        print("  %-11s %.4f / %.4f   (%.0f s so far)" % (name, res[name][0], res[name][1], time.time() - t0), flush=True)
    R, Cf = related_R(C, rho, t)
    rel = C | C.T
    sp = ~rel & ~np.eye(len(P), dtype=bool)
    I, J = np.nonzero(np.triu(sp, 1))
    t1 = time.time(); rj = detour(R, sp); T["detour"] = time.time() - t1
    base = np.where(rel, R, 0.0)
    done("johnston", mds3(np.where(sp, rj, base)))
    t1 = time.time(); s, k = ours_multiref(C, Cf, rho, t, W, I, J, rng); T["ours_multiref"] = time.time() - t1
    have = np.isfinite(s)
    done("switch", mds3(sym(base, I, J, np.where(have & (s < 0.25), s, rj[I, J]))))
    del rj, sp
    D = sym(base, I, J, np.where(have, s, np.median(s[have]))); X0 = mds3(D)
    Wt = sym(rel.astype(float), I, J, np.where(have, k / (k + 100), 0.0)); np.fill_diagonal(Wt, 0.0)
    del R, base, I, J, s, k, have
    t1 = time.time(); Xw, _ = smacof(X0.copy(), D, Wt, 300); T["fit_K100"] = time.time() - t1
    del D, Wt
    done("w_K100", Xw)
    Rl = rl_setup(Cf, C, rho)
    del Cf, C
    t1 = time.time(); Xp, hist = fit(Xw, t, Rl, iters); T["poisson"] = time.time() - t1
    print("  loglik " + " ".join("%d:%.0f" % h for h in hist[::2]), flush=True)
    done("poisson", Xp)
    clip = [np.nan] * 3
    if shape == "slab":                                                   # ORACLE: divide each count by the true share of its interval inside the slab
        t1 = time.time(); f = inside_share(P[Rl["A"]], P[Rl["B"]], rng); T["inside_share"] = time.time() - t1
        clip = [np.mean(f < 0.99), np.mean(f < 0.8), np.mean(f)]
        Nab = (Rl["t2"] ** 2 * rho * C4 - 0.5) / np.maximum(f, 0.05)
        t2 = np.sqrt((Nab + 0.5) / (rho * C4))
        Ro = dict(Rl, t2=t2, sd=t2 / (2 * np.sqrt(Nab + 1)))
        t1 = time.time(); Xo, _ = fit(Xw, t, Ro, iters); T["oracle_wall"] = time.time() - t1
    else:
        Xo = Xp                                                           # the diamond is causally convex: nothing to correct
    done("oracle_wall", Xo)
    save(npts=len(P), res=res, T=T, clip=clip)
    return [res[a] for a in NAMES], T, clip

def summary(label, rows, inr, clip):
    for lab, A in (("all pairs", np.array(rows)), ("interior pairs", np.array(inr))):
        d = A - A[:, :1]
        reps = len(A)
        print("%s, %s:" % (label, lab))
        for a, m, dm, de in zip(NAMES, A.mean(0), d.mean(0), d.std(0, ddof=1) / np.sqrt(reps) if reps > 1 else np.full(len(NAMES), np.nan)):
            print("  %-11s corr %.4f   vs johnston %+.4f +- %.4f   (%+.0f %% of his residual)" % (a, m, dm, de, 100 * dm / (1 - A[:, 0].mean())))
    c = np.array(clip, float)
    if len(c) and np.isfinite(c).all():
        print("  related pairs with interval share inside the slab < 0.99: %.3f, < 0.8: %.3f; mean share %.3f (oracle)" % tuple(c.mean(0)), flush=True)

def run(n, reps, seed, iters):
    W = load_table()
    rng = np.random.default_rng(seed)
    for shape in ("diamond", "slab"):
        allr, inr, clip = [], [], []
        for _ in range(reps):
            sc, T, cl = universe(shape, n, rng, W, iters)
            allr.append([x[0] for x in sc]); inr.append([x[1] for x in sc])
            if shape == "slab":
                clip.append(cl)
            print("  %s universe %d timings: %s" % (shape, len(allr), " ".join("%s %.0f s" % kv for kv in T.items())), flush=True)
        summary("%s n = %d (%d univ., seed %d, %d iterations)" % (shape, n, reps, seed, iters), allr, inr, clip)

def one(shape, n, seed, out, iters=400):
    W = load_table()
    rng = np.random.default_rng(seed)
    print("%s n = %d seed %d" % (shape, n, seed), flush=True)
    def save(npts, res, T, clip=(np.nan,) * 3):
        names = [a for a in NAMES if a in res]
        np.savez(out, shape=shape, n=n, npts=npts, seed=seed, names=np.array(names), scores=np.array([res[a] for a in names]),
                 timing_keys=np.array(list(T)), timing=np.array(list(T.values())), clip=np.array(clip))
    universe(shape, n, rng, W, iters, save)

def analyse(folder):
    Z = [np.load(f) for f in sorted(glob.glob(folder + "/r25_*.npz"))]
    for shape in ("diamond", "slab"):
        for n in sorted({int(z["n"]) for z in Z if str(z["shape"]) == shape}):
            zs = [z for z in Z if str(z["shape"]) == shape and int(z["n"]) == n]
            full = [z for z in zs if len(z["names"]) == len(NAMES)]
            if len(full) < len(zs):
                print("%s n = %d: %d of %d universes incomplete (left out)" % (shape, n, len(zs) - len(full), len(zs)))
            if not full:
                continue
            tm = {k: np.median([dict(zip(z["timing_keys"], z["timing"]))[k] for z in full]) for k in full[0]["timing_keys"]}
            summary("%s n = %d (%d univ., mean %d events)" % (shape, n, len(full), np.mean([int(z["npts"]) for z in full])),
                    [z["scores"][:, 0] for z in full], [z["scores"][:, 1] for z in full], [z["clip"] for z in full] if shape == "slab" else [])
            print("  median timings: " + " ".join("%s %.0f s" % kv for kv in tm.items()))

if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "check":
        check()
    elif a and a[0] == "one":
        one(a[1], int(a[2]), int(a[3]), a[4], int(a[5]) if len(a) > 5 else 400)
    elif a and a[0] == "analyse":
        analyse(a[1])
    else:
        run(int(a[0]) if a else 1500, int(a[1]) if len(a) > 1 else 3, int(a[2]) if len(a) > 2 else 6060, int(a[3]) if len(a) > 3 else 400)
