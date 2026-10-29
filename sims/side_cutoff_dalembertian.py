"""Side calculation (idea 001): does the finite-universe rapidity cutoff eta_max survive in the causal-set d'Alembertian?

1+1, units l = 1 (rho = 1). Light-cone coords u = t - x, v = t + x, so tau^2 = u v, and a past event at proper time
tau and rapidity eta sits at (u, v) = -(tau e^{-eta}, tau e^{eta}). Area element tau dtau deta; Alexandrov area V = tau^2/2.
Sorkin's 2D operator, averaged over sprinklings, acting on a plane wave phi = exp(-i(p u + q v)) (box phi = -4 p q phi):
    B(p, q) = 4 [ -1/2 + int deta h(s) ],      s = p e^{-eta} + q e^{eta}
    h(s)    = int_0^inf tau dtau e^{-tau^2/2} (1 - tau^2 + tau^4/8) e^{i s tau}        (layers 1, 2, 3 with weights 1, -2, 1)
    h_link  = same with only the "1" (links only, the raw link sum).
The cutoff restricts eta to |eta| <= eta_max in the cosmic frame; a wave boosted by theta has (p, q) -> (p e^theta, q e^-theta).
"""
import numpy as np

T = np.linspace(0, 14, 200001)
W = T * np.exp(-T**2 / 2)
dT = T[1] - T[0]

def _int(y):
    return dT * (y.sum(-1) - 0.5 * (y[..., 0] + y[..., -1]))

def h(s, links_only=False):
    s = np.atleast_1d(np.asarray(s, float))
    g = W if links_only else W * (1 - T**2 + T**4 / 8)
    out = np.empty(s.shape, complex)
    big = s > 40
    sb = s[big]
    out[big] = -1 / sb**2 - (3 if links_only else 9) / sb**4      # integration by parts: g'(0)/(is)^2 + g'''(0)/(is)^4
    for i in np.flatnonzero(~big):
        out[i] = _int(g * np.exp(1j * s[i] * T))
    return out

def I(p, q, eta_max, links_only=False, n=4001):
    eta = np.linspace(-eta_max, eta_max, n)
    hv = h(p * np.exp(-eta) + q * np.exp(eta), links_only)
    return np.trapezoid(hv, eta)

if __name__ == "__main__":
    print("1) h(s) of the combined operator vanishes at s=0 and s->inf; the link-only kernel -> 1 at s=0:")
    for s in (0.0, 0.01, 0.1, 1, 10, 39.9, 40.1):
        print(f"   s={s:6}: h={h(s)[0]: .5f}   h_link={h(s, True)[0]: .5f}")
    print(f"   predicted small-s slope of h: -i sqrt(2 pi)/16 = {-1j*np.sqrt(2*np.pi)/16:.5f}; numeric {h(0.01)[0]/0.01:.5f}")

    print("2) null wave (p = 0): B = 4(-1/2 + int_0^inf h(s) ds/s) should be 0 (box of a null wave):")
    for em in (10, 20, 40):
        print(f"   eta_max={em}: B = {4 * (-0.5 + I(0, 1.0, em)):.5f}")

    print("3) massive wave, no cutoff (eta_max = 40): B vs -4pq, and boost invariance (p,q) -> (p e^th, q e^-th):")
    for pq in (1e-4, 1e-3, 1e-2):
        for th in (0, 3, 6):
            p, q = np.sqrt(pq) * np.exp(th), np.sqrt(pq) * np.exp(-th)
            B = 4 * (-0.5 + I(p, q, 40))
            print(f"   pq={pq:g} theta={th}: B = {B:.6f}   -4pq = {-4*pq:g}")

    print("4) with the cutoff: massive wave, pq = 1e-3, eta_max = 20, boosted by theta. The long light-cone")
    print("   wavelength in the cosmic frame is 1/p; the cutoff reaches out to e^eta_max. Watch x = p e^eta_max:")
    pq, em = 1e-3, 20
    for th in (0, 10, 14, 16, 17, 18, 19, 20, 22, 25):
        p, q = np.sqrt(pq) * np.exp(-th), np.sqrt(pq) * np.exp(th)
        B = 4 * (-0.5 + I(p, q, em, n=8001))
        Bl = 4 * I(p, q, em, links_only=True, n=8001)
        print(f"   theta={th:2}: x = p e^eta_max = {p*np.exp(em):9.3g}   B = {B.real: .5f}{B.imag:+.5f}i"
              f"   (no cutoff: {4*pq:.5f})   raw link sum = {Bl.real:7.3f}")
