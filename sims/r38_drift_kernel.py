"""Depth-drift kernel in a general 1+1 FRW spacetime (session 17; CQG referee, Major 3, last bullet: 'derive the weighting kernel').
ds^2 = a(eta)^2 (-d eta^2 + dx^2), a = e^sigma. a, b on the slice eta0 at x = -+h (h -> 0), c a coordinate time T straight below.
With s = eta0 - eta (depth in conformal time), from the rectangles of the paper (Fig. 1):
    V_A = V_B = h I1,  I1 = int_0^T e^{2 sigma(eta0 - s/2)} ds,      V_C = (1/2) int_0^T int_0^T e^{2 sigma(eta0 - (s + r)/2)} ds dr,
    d^2 = (2 h e^{sigma0})^2,   ratio = 2 V_A V_B / (V_C d^2) = I1^2 / (2 V_C e^{2 sigma0}),
    proper time tau = int_0^T e^{sigma(eta0 - s)} ds,   R = 2 sigma'' e^{-2 sigma}  (de Sitter check: R = 2 H^2).
Series in T with sigma Taylor-expanded at eta0, then expressed in tau. Output: 1 - ratio = (tau^2 / 16) [R0 + k1 tau dR/dtau + k2 tau^2 (...) ...],
dR/dtau the derivative along the worldline toward the future, so R at depth w tau below a, b is R0 - w tau dR/dtau: the leading kernel weight is w = -k1.
Also checks the result against the exact power-law FRW volumes of r9 (a = eta^p).
Usage: python r38_drift_kernel.py
"""
import sympy as sp
import numpy as np

def trunc(e, x, n):
    """Polynomial e in x truncated at degree n."""
    e = sp.expand(e)
    return sum(e.coeff(x, k) * x ** k for k in range(n + 1))

def exp_series(p, x, n):
    """exp(p(x)) for a polynomial p with p(0) = 0, to degree n."""
    out, term = 1, 1
    for k in range(1, n + 1):
        term = trunc(term * p / k, x, n); out += term
    return trunc(out, x, n)

def inv_series(q, x, n):
    """1 / q(x) for q(0) = 1, to degree n."""
    y = trunc(1 - q, x, n); out, term = 1, 1
    for _ in range(n):
        term = trunc(term * y, x, n); out += term
    return trunc(out, x, n)

def main(order=4):
    T, s, r, d, tau = sp.symbols("T s r d tau")
    sg = sp.symbols("sigma0:6")
    dsig = sum(sg[k] * (-d) ** k / sp.factorial(k) for k in range(1, order + 2))               # sigma(eta0 - d) - sigma0
    E2 = exp_series(2 * dsig, d, order)                                                       # e^{2(sigma - sigma0)} at depth d
    I1 = sp.integrate(E2.subs(d, s / 2), (s, 0, T))
    Vc = sp.Rational(1, 2) * sp.integrate(sp.integrate(sp.expand(E2.subs(d, (s + r) / 2)), (s, 0, T)), (r, 0, T))
    a1 = trunc(sp.expand(I1 / T), T, order); b1 = trunc(sp.expand(2 * Vc / T ** 2), T, order)  # both 1 + O(T)
    ratio = trunc(a1 ** 2 * inv_series(b1, T, order), T, order)
    tauT = sp.integrate(exp_series(dsig, d, order + 1).subs(d, s), (s, 0, T))                  # tau e^{-sigma0}, to T^{order+2}
    Tt = tau                                                                                   # invert by fixed-point iteration
    for _ in range(order + 1):
        Tt = trunc(Tt + tau - tauT.subs(T, Tt), tau, order + 1)
    one_minus = trunc(1 - ratio.subs(T, Tt), tau, order)
    R0 = 2 * sg[2]
    dR = 2 * (sg[3] - 2 * sg[1] * sg[2])                              # e^{3 sigma0} dR/dtau, toward the future
    c2 = sp.factor(one_minus.coeff(tau, 2) * 16)
    c3 = sp.factor(one_minus.coeff(tau, 3) * 16)
    print("16 (1 - ratio) = tau^2 [ A2 ] + tau^3 [ A3 ] + ...   (tau and R in units of e^{sigma0})")
    print("  A2 =", c2, "   R0 =", R0, "   equal:", sp.simplify(c2 - R0) == 0)
    k1 = sp.simplify(c3 / dR)
    print("  A3 =", c3, "   dR/dtau =", sp.expand(dR), "   A3 / (dR/dtau) =", k1)
    print("  A4 =", sp.factor(one_minus.coeff(tau, 4) * 16))
    return c2, c3, k1

def check(k1):
    """Exact power-law FRW (r9): 16 (1 - ratio) / tau^2 against R0 + k1 tau dR/dtau."""
    import r9_drift_fit_frw as r9
    for p, eta0 in ((1.0, 1.5), (-2.0, 1.0), (0.5, 1.0)):
        R0 = r9.R_of(eta0, p)
        dRdeta = 2 * p * (2 + 2 * p) * eta0 ** (-3.0 - 2 * p)
        dRdtau = dRdeta / eta0 ** p                                 # d tau = a d eta
        for t in (0.02, 0.05, 0.1):
            eta_c = r9.eta_at_tau(eta0, t, p)
            exact = 16 * (1 - r9.ratio_frw(eta_c, 0.0, eta0, 1e-6, p)) / t ** 2
            print(f"  p {p:+.1f} tau {t:.2f}: exact {exact:+.5f}   R0 {R0:+.5f}   R0 + k1 tau R' {R0 + k1 * t * dRdtau:+.5f}")

if __name__ == "__main__":
    c2, c3, k1 = main()
    check(float(k1))
