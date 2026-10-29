"""Side calculation (idea 001): the exact-null-wave puzzle, with a finite past region instead of a rapidity wedge.

Same set-up as side_cutoff_dalembertian.py (1+1, l = 1, Sorkin's 2D operator averaged over sprinklings, plane wave
phi = exp(-i(p u + q v))). A past event is displaced by a >= 0 along u and b >= 0 along v; tau^2 = a b, area element
(1/2) da db, Alexandrov area V = a b / 2. Instead of cutting rapidity at fixed tau (a wedge), the past is the finite
diamond 0 <= a <= U, 0 <= b <= W ("the universe has a finite past"):
    B = 4 [ -1/2 + E ],   E = (1/2) int_0^U da int_0^W db exp(-ab/2) (1 - ab + a^2 b^2 / 8) exp(i(p a + q b))
The b-integral is done exactly (lower incomplete gamma, integer order); the a-integral numerically on a log grid.
"""
import numpy as np
from math import factorial

def lower_gamma(n, z):
    """gamma(n+1, z) = int_0^z t^n e^-t dt for integer n >= 0 and complex z (array)."""
    z = np.asarray(z, complex)
    out = np.empty_like(z)
    small = np.abs(z) < 1.0
    zs = z[small]                                   # series: z^{n+1} sum_k (-z)^k / (k! (n+1+k))
    acc, term = np.zeros_like(zs), np.ones_like(zs)
    for k in range(40):
        acc += term / (n + 1 + k)
        term = term * (-zs) / (k + 1)
    out[small] = zs**(n + 1) * acc
    zb = z[~small]                                  # closed form: n! (1 - e^-z sum_{k<=n} z^k / k!)
    s = sum(zb**k / factorial(k) for k in range(n + 1))
    out[~small] = factorial(n) * (1 - np.exp(-zb) * s)
    return out

def E_diamond(p, q, U, W, n=400001):
    a = np.exp(np.linspace(np.log(U) - 60, np.log(U), n))   # log grid in a, from ~0 to U
    alpha = a / 2 - 1j * q                                   # int_0^W b^k e^{-alpha b} db = gamma(k+1, alpha W) / alpha^{k+1}
    Ik = [lower_gamma(k, alpha * W) / alpha**(k + 1) for k in range(3)]
    inner = Ik[0] - a * Ik[1] + a**2 / 8 * Ik[2]
    f = 0.5 * inner * np.exp(1j * p * a) * a                 # extra a: da = a d(ln a)
    return np.trapezoid(f, np.log(a)) if hasattr(np, "trapezoid") else np.trapz(f, np.log(a))

def B(p, q, U, W):
    return 4 * (-0.5 + E_diamond(p, q, U, W))

if __name__ == "__main__":
    np.seterr(all="ignore")
    L = np.exp(10.0)                                          # past diamond of size ~2e4 Planck lengths (eta_max ~ 10)
    print("1) constant field (p = q = 0): exact answer 4[-1/2 + (1 - (1-A) e^-A)/2], A = UW/2 -> 0")
    for Ls in (3.0, 10.0, L):
        A = Ls * Ls / 2
        print(f"   U=W={Ls:9.3g}: B = {B(0, 0, Ls, Ls).real: .6f}   exact {4*(-0.5 + 0.5*(1-(1-A)*np.exp(-A))): .6f}")
    print("2) massive wave well inside the diamond (1/p, 1/q << L): B should be 4pq (session-4 convention)")
    for pq in (1e-3, 1e-2):
        for th in (0.0, 3.0):
            p, q = np.sqrt(pq) * np.exp(th), np.sqrt(pq) * np.exp(-th)
            print(f"   pq={pq:g} theta={th}: B = {B(p, q, L, L):.5f}   4pq = {4*pq:g}")
    print("3) exact null wave p = 0 (rapidity wedge gave -1):")
    for q in (1e-2, 1e-1, 1.0):
        print(f"   q={q:g}: B = {B(0, q, L, L):.5f}")
    print("4) long light-cone wavelength 1/p beyond the past size L (wedge gave a jump to -1):")
    pq = 1e-3
    for x in (1e-3, 1e-1, 1.0, 10.0, 1e3):                    # x = p L
        p = x / L; q = pq / p
        print(f"   p L = {x:7g}: B = {B(p, q, L, L):.5f}   4pq = {4*pq:g}")
