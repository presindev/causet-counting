"""Stage S4a (idea 005): embed a 2D causal set back into Minkowski space from the order alone (Lorentzian MDS).

1. Pick M sample events. Squared intervals from counts only (rho = density):
     timelike pair x < y:  s = -tau^2 = -2 N(I(x, y)) / rho                (2D: V = tau^2 / 2)
     spacelike pair a, b:  s = +d^2 = 2 N_A N_B / (rho (N_C + 1))           (rectangle identity, deepest c)
2. In Minkowski space s_ij = (x_i - x_j)^T eta (x_i - x_j). Double centering, G = -1/2 J S J with J = I - 11^T/M,
   gives G = X eta X^T for the centred coordinates X.
3. Eigen-decompose G: a 2D Lorentzian set should show one large negative eigenvalue (time), one large positive
   (space), the rest small. Coordinates: t = sqrt(|lambda_-|) e_-,  x = sqrt(lambda_+) e_+.
4. Compare with the truth: least-squares affine map true ~ A rec + b; A should be a Lorentz transformation
   (A^T eta A = eta, up to reflections).
"""
import numpy as np

def sprinkle(n, rng):
    u, v = rng.random(n), rng.random(n)
    order = np.argsort(u + v)
    return u[order], v[order]

def interval_matrix(C, K, S, rho):
    """Squared-interval matrix on the sample S, from the causal matrix C and K = C @ C only."""
    M = len(S)
    sq = np.zeros((M, M))
    Cb = C > 0
    score = K[:, S]                                       # interval sizes N(I(c, s)) for every c and sample s
    for i, a in enumerate(S):
        for j in range(i + 1, M):
            b = S[j]
            if Cb[a, b] or Cb[b, a]:
                lo, hi = (a, b) if Cb[a, b] else (b, a)
                sq[i, j] = -2 * K[lo, hi] / rho
                continue
            common = Cb[:, a] & Cb[:, b]
            if not common.any():
                sq[i, j] = np.nan
                continue
            cands = np.flatnonzero(common)
            c = cands[np.argmax(score[cands, i] + score[cands, j])]   # deepest c: biggest intervals to a and b
            between = Cb[c] & Cb[:, a] & Cb[:, b]
            nC = between.sum()
            nA = K[c, a] - nC
            nB = K[c, b] - nC
            sq[i, j] = 2 * nA * nB / (rho * (nC + 1))
    return sq + sq.T

def lorentz_mds(sq):
    M = len(sq)
    J = np.eye(M) - 1 / M
    with np.errstate(all="ignore"):            # numpy 2.0 + Accelerate emits spurious matmul warnings
        G = -0.5 * J @ sq @ J
    lam, vec = np.linalg.eigh(G)
    i_neg, i_pos = np.argmin(lam), np.argmax(lam)
    t = np.sqrt(-lam[i_neg]) * vec[:, i_neg]
    x = np.sqrt(lam[i_pos]) * vec[:, i_pos]
    return np.column_stack([t, x]), lam

def compare(rec, true):
    """Fit true ~ rec A + b. Return rms residual and how far A is from a Lorentz transformation."""
    X = np.column_stack([rec, np.ones(len(rec))])
    coef, *_ = np.linalg.lstsq(X, true, rcond=None)
    A = coef[:2].T                                      # true_vec = A rec_vec + b
    resid = true - X @ coef
    eta = np.diag([-1.0, 1.0])
    lorentz_err = np.abs(A.T @ eta @ A - eta).max()
    return np.sqrt((resid**2).sum(1).mean()), lorentz_err, A

def run(n, M, seed):
    rng = np.random.default_rng(seed)
    u, v = sprinkle(n, rng)
    rho = 2 * n
    C = ((u[:, None] < u[None, :]) & (v[:, None] < v[None, :])).astype(np.float32)
    with np.errstate(all="ignore"):
        K = C @ C
    central = np.flatnonzero((u > 0.35) & (u < 0.95) & (v > 0.35) & (v < 0.95))
    S = rng.choice(central, M, replace=False)
    sq = interval_matrix(C, K, S, rho)
    rec, lam = lorentz_mds(sq)
    true = np.column_stack([(u[S] + v[S]) / 2, (v[S] - u[S]) / 2])        # (t, x)
    rms, lerr, A = compare(rec, true)
    return rms, lerr, lam, rho, A

if __name__ == "__main__":
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    M = int(sys.argv[2]) if len(sys.argv) > 2 else 150
    out = []
    for seed in (1, 2, 3, 4):
        rms, lerr, lam, rho, A = run(n, M, seed)
        ell = rho ** -0.5
        lam_sorted = np.sort(lam)
        out.append((rms / ell, lerr))
        print(f"seed {seed}: rms position error = {rms:.4f} = {rms/ell:.2f} ell;  |A^T eta A - eta|max = {lerr:.3f}")
        print(f"   eigenvalues: most negative {lam_sorted[:3].round(4)}, most positive {lam_sorted[-3:].round(4)}")
    o = np.array(out)
    print(f"N = {n}, M = {M}: rms error {o[:,0].mean():.2f} +- {o[:,0].std():.2f} ell (sample region ~ {0.6/ell:.0f} ell across)")
