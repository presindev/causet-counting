"""Is our finite-past result for Sorkin's 1+1 box a special case of Buck-Dowker-Jubb-Surya (arXiv:1502.05388)? (idea 001, session 10)

BDJS: the mean causal-set action of an Alexandrov interval tends to the volume of its codimension-2 corner; in 2D that is the two side corners, <S> -> 2.
Ours (draft v6, Sec. 2): for an event x whose past inside the region is a diamond of volume A (rho = 1), the mean of Sorkin's box on phi = 1 is
  <B1(x)> = 4 [ -1/2 + 1/2 (1 - (1 - A) e^{-A}) ] = -2 (1 - A) e^{-A}.
The 2D BD action (eps = 1) is S = 2 (N - 2 N_link + 4 N_next - 2 N_nextnext) = - sum_x B1(x). Every x in an interval sees the sub-interval
below it, so our formula predicts <S> = 2 rho int (1 - A_x) e^{-A_x} d^2x = 2 (1 - e^{-A}) -> 2: BDJS's corner value.
Checks: (1) numerical quadrature of the integral; (2) direct sprinklings of a diamond, counting intervals by size.
Usage: python r7_corner_check.py [seeds=200]
"""
import sys
import numpy as np

def quad(A, m=4000):
    """2 int (1 - A_x) e^{-A_x} over a diamond of volume A, rho = 1. Light-cone coords a, b in [0, U], volume element da db / 2, A_x = a b / 2."""
    U = np.sqrt(2 * A)
    a = (np.arange(m) + 0.5) * U / m
    ax = a[:, None] * a[None, :] / 2
    return 2 * ((1 - ax) * np.exp(-ax)).sum() * (U / m) ** 2 / 2

def sprinkled_action(n_mean, rng):
    """BD action (eps = 1) of a Poisson sprinkling of mean n_mean into a 2D diamond."""
    n = rng.poisson(n_mean)
    u, v = rng.random(n), rng.random(n)
    C = ((u[:, None] < u[None, :]) & (v[:, None] < v[None, :])).astype(np.float64)
    with np.errstate(all="ignore"):          # numpy + Accelerate: spurious matmul warnings
        K = C @ C                            # K[i, j] = number of events strictly between i and j
    k = K[C > 0].astype(int)
    N0, N1, N2 = (k == 0).sum(), (k == 1).sum(), (k == 2).sum()
    return 2 * (n - 2 * N0 + 4 * N1 - 2 * N2)

if __name__ == "__main__":
    seeds = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    print("quadrature: A, 2 int (1-A_x) e^{-A_x}, prediction 2(1 - e^{-A})")
    for A in (0.5, 2, 8, 50):
        print(f"  A={A:5}: {quad(A):.5f}   {2 * (1 - np.exp(-A)):.5f}")
    rng = np.random.default_rng(3)
    print(f"sprinklings ({seeds} seeds each): mean BD action of a diamond, expected -> 2 (BDJS) with finite-size 2 e^{{-A}}")
    for n_mean in (5, 50, 200, 800):
        S = np.array([sprinkled_action(n_mean, rng) for _ in range(seeds)])
        print(f"  <N>={n_mean:4d}: <S> = {S.mean():+.3f} +- {S.std() / np.sqrt(seeds):.3f}   prediction {2 * (1 - np.exp(-n_mean)):.3f}")
