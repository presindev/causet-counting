"""Weak-beta phase drift of the future factor (idea 004, session 10; ROADMAP N1).

At small beta, F_N(X) ~ Count_N(X) * exp(i beta m_N(X)), with m_N(X) = <S_N - S_X> over all growth continuations of the stem X
(uniform over growth paths, i.e. the beta = 0 measure). So the phase of F_N(X)/F_N(antichain) is beta * (m_N(X) - m_N(antichain))
to first order, and its drift per added event is beta * d_N with d_N = Delta m_{N+1} - Delta m_N.
m_N is computed exactly as phase(F_N)/beta at beta = 1e-4 (error O(beta * variance)), memoized as in a2_future_factor.py.
Prints, per stem: d_N / pi (to compare with the observed 0.008 pi beta per relation), and N d_N and N^2 d_N per relation (is the decay 1/N or faster?).
Usage: python r5_drift_meanfield.py [Nmax=10] [stem sizes=2,3]
"""
import sys, time
import numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import a2_future_factor as ff

BETA = 1e-4
EPS = float(sys.argv[3]) if len(sys.argv) > 3 else 0.21
ff.SETTINGS = [(EPS, BETA)]

if __name__ == "__main__":
    Nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    sizes = [int(s) for s in (sys.argv[2] if len(sys.argv) > 2 else "2,3").split(",")]
    t0 = time.time()
    ff.FF = ff.FutureFactor(Nmax)
    ff.FF.G([], [])
    print(f"Nmax={Nmax}, eps={EPS}: {time.time() - t0:.1f} s, {len(ff.FF.memo)} states")
    for n in sizes:
        reps = ff.stems(n)
        rows = {}
        for past, up in reps:
            g = ff.FF.G(past, up)[0]                         # g[k] = F_{n+k}
            m = np.angle(g) / BETA                           # mean future action, N = n .. Nmax
            rows[ff.name(past)] = (m, sum(ff.POPC[p] for p in past))
        ref = [k for k, (_, r) in rows.items() if r == 0][0]
        print(f"\n== stems of size {n}, ref {ref}: drift per event d_N/pi (N -> N+1), and d_N per relation, last steps")
        for k, (m, rel) in rows.items():
            if rel == 0:
                continue
            dm = m - rows[ref][0]
            d = np.diff(dm)                                  # d[j]: step N = n+j -> n+j+1
            Ns = np.arange(n + 1, Nmax + 1)                  # N after the step
            sel = slice(-5, None)
            print(f"  {k:18s} rel {rel}  N: " + " ".join(f"{N:7d}" for N in Ns[sel]))
            print(f"  {'':18s}        d/pi:  " + " ".join(f"{x / np.pi:+.4f}" for x in d[sel]))
            print(f"  {'':18s}        N*d/rel:" + " ".join(f"{N * x / rel:+.4f}" for N, x in zip(Ns[sel], d[sel])))
            print(f"  {'':18s}        N^2*d/rel:" + " ".join(f"{N * N * x / rel:+.3f}" for N, x in zip(Ns[sel], d[sel])))
