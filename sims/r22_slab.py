"""Second benchmark shape: a slab (cylinder t in [0, 1], |x| <= R) vs the diamond, through ONE tip-free pipeline (idea 005, session 12).
A slab has no event related to all others, so the diamond pipeline (time from the two tips, MDS centred on v1, our reference c = v1 or vn) does not apply.
Common pipeline, both shapes, all arms:
  - time coordinate: the TRUE t for every arm (isolates the spatial-distance question; Johnston's own t needs the tips; the oracle showed related pairs are not
    the bottleneck). Related pairs: spatial separation R = sqrt(dt^2 - tau^2), tau from the strictly-between interval count (his convention).
  - johnston : his two-leg detour (min-plus over related R) for spacelike pairs.
  - ours     : overlap inversion with a per-pair reference: among K_REF deepest events (largest futures) and K_REF highest (largest pasts), the one in the
               common past (future) of both events with the largest min(|I(c,a)|, |I(c,b)|). Same table (valid for any c while the intervals are not clipped).
  - switch   : ours if < 0.25, else johnston.     - w_K30, w_K100 : count-weighted SMACOF (as r19), k = overlap count of the chosen reference.
  - embedding: classical MDS of the spatial distances with double centring (no reference event), 3 dimensions; SMACOF arms start from it.
Scored by spatial-distance correlation (his Table V metric) on all pairs and on the "interior" (events in the top quartile of min(|past|, |future|)).
Wall diagnosis (uses the truth, diagnosis only): median relative error of ours for pairs with both events farther than 0.1 from the side wall vs the rest.
Equal n in both shapes (equal cost); the slab (R = 0.5) has 4x the volume, so ell is 4^(1/4) = 1.41x larger there.
Usage: python r22_slab.py [n reps seed]
"""
import sys
import time
import numpy as np
from r11_4d_distance import load_table, dist_from_counts, uniform_in_diamond, precedes
from r16_local_fit import smacof

np.seterr(all="ignore")
C4 = np.pi / 24
R_SLAB = 0.5
K_REF = 32

def sprinkle(shape, n, rng):
    m = rng.poisson(n)
    if shape == "diamond":
        P = np.vstack([np.zeros(4), uniform_in_diamond(m, 1.0, rng), [1, 0, 0, 0]]); V = C4   # with its two tips, as in his benchmark (without them
                                                                   # 21 % of pairs share no past or future event at n = 800 and rim events are isolated)
    else:
        out = []
        while sum(len(o) for o in out) < m:
            x = R_SLAB * (2 * rng.random((3 * m, 3)) - 1)
            out.append(x[(x ** 2).sum(1) < R_SLAB ** 2])
        P = np.column_stack([rng.random(m), np.vstack(out)[:m]]); V = 4 / 3 * np.pi * R_SLAB ** 3
    P = P[np.argsort(P[:, 0])]
    return P, precedes(P, P), m / V

def mds3(D):
    n = len(D); J = np.eye(n) - 1.0 / n
    lam, vec = np.linalg.eigh(-0.5 * J @ (D ** 2) @ J)
    o = np.argsort(lam)[::-1][:3]
    return vec[:, o] * np.sqrt(np.maximum(lam[o], 0))

def related_R(C, rho, t):
    Cf = C.astype(np.float32)
    N = Cf @ Cf
    rel = C | C.T
    tau = np.where(rel, (np.maximum(N, N.T) / (rho * C4)) ** 0.25, 0.0)
    return np.where(rel, np.sqrt(np.abs((t[:, None] - t[None, :]) ** 2 - tau ** 2)), np.inf), Cf

def detour(R, sp):
    """His two-leg detour; without tips some pairs have none, so those get the shortest route of <= 4 legs (one more min-plus pass)."""
    r = R.copy(); np.fill_diagonal(r, 0.0)
    for x in range(len(R)):
        ys = np.flatnonzero(sp[x])
        if len(ys):
            r[x, ys] = np.min(R[x][:, None] + R[:, ys], axis=0)
    r = np.minimum(r, r.T)
    bad = ~np.isfinite(r)
    for x in np.flatnonzero(bad.any(1)):
        ys = np.flatnonzero(bad[x])
        r[x, ys] = np.min(r[x][:, None] + r[:, ys], axis=0)
    r = np.minimum(r, r.T)
    fin = np.isfinite(r)
    return np.where(fin, r, r[fin].max())                          # isolated events (none in the slab or tipped diamond): largest finite value

def ours_multiref(C, Cf, rho, t, W, I, J, rng):
    """Per spacelike pair (I, J): best reference among K_REF events on each side. Candidates (counts only): the 4 events with the largest future
    (past) plus random events from the quartile with the smallest past (future), i.e. spread along the lower (upper) boundary. Returns spatial
    estimate s and overlap count k (nan / 0 if no reference serves the pair)."""
    n = len(C)
    best = np.full(len(I), -1.0); na = np.zeros(len(I)); nb = np.zeros(len(I)); nc = np.zeros(len(I))
    for side in ("past", "future"):
        M = Cf if side == "past" else Cf.T                          # M[c, x] = c < x (past refs) or x < c (future refs)
        size = M.sum(1); other = M.sum(0)                           # far-side size; near-side size (past size for past refs)
        low = np.flatnonzero(other <= np.quantile(other, 0.25))
        refs = np.unique(np.concatenate([np.argsort(size)[::-1][:4], rng.choice(low, min(K_REF - 4, len(low)), replace=False)]))
        for c in refs:
            mask = M[c]                                              # events on the far side of c
            Ni = mask @ M                                            # Ni[a] = #{x: c<x<a} (past side; mirrored for future)
            ok = (M[c, I] > 0) & (M[c, J] > 0)
            if not ok.any():
                continue
            O = (M.T * mask) @ M                                     # O[a, b] = #{x: c<x, x<a, x<b}
            m = np.minimum(Ni[I], Ni[J])
            upd = ok & (m > best)
            best[upd] = m[upd]; na[upd] = Ni[I][upd]; nb[upd] = Ni[J][upd]; nc[upd] = O[I[upd], J[upd]]
    s = np.full(len(I), np.nan)
    good = best >= 1
    d = dist_from_counts(W, na[good], nb[good], nc[good], 1.0) / rho ** 0.25
    s[good] = np.sqrt(d ** 2 + (t[I[good]] - t[J[good]]) ** 2)
    return s, np.where(good, nc, 0.0)

def sym(M, I, J, v):
    M = M.copy(); M[I, J] = v; M[J, I] = v
    return M

def run(n, reps, seed):
    W = load_table()
    rng = np.random.default_rng(seed)
    names = ["johnston", "ours", "switch", "w_K30", "w_K100"]
    for shape in ("diamond", "slab"):
        allr, inr, walls = [], [], []
        for _ in range(reps):
            t0 = time.time()
            P, C, rho = sprinkle(shape, n, rng)
            t = P[:, 0]
            iu = np.triu_indices(len(P), 1)
            Dt = np.sqrt(((P[:, None, 1:] - P[None, :, 1:]) ** 2).sum(-1))
            v = np.minimum(C.sum(0), C.sum(1))
            core = v >= np.quantile(v, 0.75)
            incore = (core[:, None] & core[None, :])[iu]
            R, Cf = related_R(C, rho, t)
            rel = C | C.T
            sp = ~rel & ~np.eye(len(P), dtype=bool)
            I, J = np.nonzero(np.triu(sp, 1))
            rj = detour(R, sp)
            s, k = ours_multiref(C, Cf, rho, t, W, I, J, rng)
            have = np.isfinite(s)
            ours = np.where(have, s, rj[I, J])
            base = np.where(rel, R, 0.0)
            maps = {"johnston": mds3(np.where(sp, rj, base)),
                    "ours": mds3(sym(base, I, J, ours)),
                    "switch": mds3(sym(base, I, J, np.where(have & (s < 0.25), s, rj[I, J])))}
            fill = np.where(have, s, np.median(s[have]))
            D = sym(base, I, J, fill); X0 = mds3(D)
            for K0 in (30, 100):
                Wt = sym(rel.astype(float), I, J, np.where(have, k / (k + K0), 0.0)); np.fill_diagonal(Wt, 0.0)
                maps["w_K%d" % K0], _ = smacof(X0.copy(), D, Wt, 300)
            def sc(Y, sel):
                e = np.sqrt(((Y[:, None] - Y[None]) ** 2).sum(-1))[iu]
                return np.corrcoef(e[sel], Dt[iu][sel])[0, 1]
            allr.append([sc(maps[a], np.ones(len(iu[0]), bool)) for a in names]); inr.append([sc(maps[a], incore) for a in names])
            rr = np.sqrt((P[:, 1:] ** 2).sum(1))
            far = (R_SLAB - rr > 0.1) if shape == "slab" else (np.minimum(t, 1 - t) - rr > 0.1)
            e = np.abs(s / Dt[I, J] - 1)
            inner = far[I] & far[J] & have
            walls.append([np.median(e[inner]), np.median(e[have & ~inner]), inner.mean(), 1 - have.mean()])
            print("  %s universe %d (%d events, %.0f s): " % (shape, len(allr), len(P), time.time() - t0) +
                  "  ".join("%s %.4f/%.4f" % (a, x, y) for a, x, y in zip(names, allr[-1], inr[-1])), flush=True)
        for lab, A in (("all pairs", np.array(allr)), ("interior pairs", np.array(inr))):
            d = A - A[:, :1]
            print("%s n = %d (%d univ., seed %d), %s:" % (shape, n, reps, seed, lab))
            for a, m, dm, de in zip(names, A.mean(0), d.mean(0), d.std(0, ddof=1) / np.sqrt(reps)):
                print("  %-9s corr %.4f   vs johnston %+.4f +- %.4f   (%+.0f %% of his residual)" % (a, m, dm, de, 100 * dm / (1 - A[:, 0].mean())))
        w = np.mean(walls, 0)
        print("  ours median rel. error: away from the boundary %.3f, near it %.3f (share of pairs away %.2f; no estimate %.3f)" % tuple(w), flush=True)

if __name__ == "__main__":
    a = sys.argv[1:]
    run(int(a[0]) if a else 1500, int(a[1]) if len(a) > 1 else 3, int(a[2]) if len(a) > 2 else 6060)
