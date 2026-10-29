"""Stage S4b (idea 005): the 2D manifold detector applied to S3a phases and to S1 grown universes.

Pipeline (from S4a, counts only, rho = 1 since only shapes matter): squared intervals on a sample of events
(timelike -2 N(I); spacelike rectangle identity), Lorentzian MDS. Intrinsic diagnostics, no true coordinates:
  w2     = (|lambda_min| + lambda_max) / sum |lambda|   share of the spectrum in one time + one space direction
  r_pos  = 2nd largest positive / largest positive      (a 2D manifold: small; extra space dimensions: large)
  r_neg  = 2nd most negative / most negative            (a 2D manifold: small; extra "time" directions: large)
  stress = rms(s - s_2D) / rms(s), s_2D the squared intervals of the 2D embedding (0 = perfect 2D Minkowski fit)
  zero   = share of sampled pairs whose squared interval is exactly 0 (session 11: a bilayer gives an all-zero matrix, which MDS
           "fits" perfectly, so a low stress means nothing without this)

Calibration first (lessons 4, 10): random 2D orders (beta = 0, exactly a flat sprinkling) at the same N.
"""
import sys
import numpy as np
from s4a_embedding import interval_matrix, lorentz_mds
from s3a_mcmc_2d import samples as s3a_samples
from s2_counting_geometry import causal_from_growth
from growth_percolation import grow

def clean_sample(C, K, M0, M, sample="top", rng=None):
    """Pick M0 events, drop events until no pair lacks a common past, keep M.
    sample="top":    the M0 events with the largest pasts (sessions 3-11). In a layered order these are the top layer or two.
    sample="spread": M0 events evenly spaced in height (longest chain below the event) over the upper 70% of the heights,
                     then a random M of the survivors (session 11 fix: the sample must see the order's depth, not only its top)."""
    if sample == "top":
        S = np.argsort(C.sum(0))[-M0:]
    else:
        h = height(C)
        cand = np.flatnonzero(h >= 0.3 * h.max())
        cand = cand[np.lexsort((rng.random(len(cand)), h[cand]))]          # by height, random order inside a height
        S = cand[np.unique(np.linspace(0, len(cand) - 1, min(M0, len(cand))).round().astype(int))]
    sq = interval_matrix(C, K, S, 1.0)
    keep = np.ones(len(S), bool)
    while np.isnan(sq[np.ix_(keep, keep)]).any():
        bad = np.isnan(sq[np.ix_(keep, keep)]).sum(1)
        keep[np.flatnonzero(keep)[np.argmax(bad)]] = False
    idx = np.flatnonzero(keep)
    idx = idx[-M:] if sample == "top" else np.sort(rng.choice(idx, min(M, len(idx)), replace=False))
    return sq[np.ix_(idx, idx)]

def height(C):
    """Longest chain ending at each event (0 for minimal events), from the causal matrix alone."""
    Cb = C > 0
    order = np.argsort(Cb.sum(0))                     # past size is a linear extension: x < y => |past(x)| < |past(y)|
    h = np.zeros(len(C), int)
    for y in order:
        p = np.flatnonzero(Cb[:, y])
        if len(p):
            h[y] = h[p].max() + 1
    return h

def diagnostics(C, M0=60, M=40, sample="top", rng=None):
    C = C.astype(np.float32)
    with np.errstate(all="ignore"):              # numpy 2.0 + Accelerate emits spurious matmul warnings
        K = C @ C
    sq = clean_sample(C, K, M0, M, sample, rng)
    if len(sq) < 10:
        return None
    rec, lam = lorentz_mds(sq)
    neg, pos = np.sort(lam[lam < 0]), np.sort(lam[lam > 0])[::-1]
    if len(neg) == 0 or len(pos) == 0:
        return None                              # no time or no space direction at all: not a 1+1 spacetime
    w2 = (-neg[0] + pos[0]) / np.abs(lam).sum()
    r_pos = pos[1] / pos[0] if len(pos) > 1 else 0.0
    r_neg = neg[1] / neg[0] if len(neg) > 1 else 0.0
    dt = rec[:, 0][:, None] - rec[:, 0][None, :]
    dx = rec[:, 1][:, None] - rec[:, 1][None, :]
    s2d = -dt**2 + dx**2
    iu = np.triu_indices(len(sq), 1)
    stress = np.sqrt(np.mean((sq[iu] - s2d[iu])**2) / np.mean(sq[iu]**2))
    zero = np.mean(sq[iu] == 0)                  # share of pairs with no measurable length (linked, or an empty strip)
    return w2, r_pos, r_neg, stress, len(sq), zero

def report(label, Cs):
    D = np.array([d for d in (diagnostics(C) for C in Cs) if d is not None])
    m, s = D.mean(0), D.std(0)
    print(f"{label:<34} w2 {m[0]:.2f}±{s[0]:.2f}  r_pos {m[1]:.2f}±{s[1]:.2f}  r_neg {m[2]:.2f}±{s[2]:.2f}"
          f"  stress {m[3]:.2f}±{s[3]:.2f}  (M≈{m[4]:.0f}, {len(D)} universes)", flush=True)

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    eps, n_univ = 0.21, 10
    rng = np.random.default_rng(1)
    def rand2d():
        u, v = rng.permutation(N), rng.permutation(N)
        return (u[:, None] < u[None, :]) & (v[:, None] < v[None, :])
    print(f"N = {N}")
    report("random 2D order (= beta 0)", [rand2d() for _ in range(n_univ)])
    for beta in (0.3, 1.5):
        report(f"S3a beta = {beta} (eps {eps})", s3a_samples(N, beta, eps, n_samples=n_univ, sweeps_between=20, seed=2))
    for label, kw in [("S1 growth, fixed p = 0.05", dict(p=0.05)), ("S1 growth, p = 3/n", dict(p=None, c=3))]:
        Cs = [causal_from_growth(grow(N, seed=s, originary=True, **kw)[0], N) for s in range(1, n_univ + 1)]
        report(label, Cs)
