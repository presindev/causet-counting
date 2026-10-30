"""F_N at N = 12 (cluster job 449963) against the session-10 prediction (idea 004, Test 4c/4d; session 16).
(a) weak-beta drift, eps = 0.21, beta = 2, 2-stem: N*d with d_N = [dphi_N - dphi_{N-1}] / beta, dphi = arg F_N(rel1) - arg F_N(rel0).
    Prediction (Test 4c): N*d falls to 0.233 +- 0.003 at N = 12; flat or rising => 1/N (log-divergent).
(b) 2-stem quantum/counting ratio q_N = [F(rel1)/F(rel0)](beta) / same at beta = 0, all settings, N = 8-12 (Test 4b convention).
(c) 3- and 4-stems: median per-step change of ln|R| and of the phase, R = stem ratio to stem 0, divided by the beta = 0 ratio.
Usage: python fn_N12_check.py cluster_fetch/fn/out/fn_N12.npz
"""
import sys
import numpy as np

def main(f):
    z = np.load(f, allow_pickle=True)
    S = z["settings"]
    print(f"{f}: Nmax {int(z['Nmax'])}, {int(z['nstates'])} memo states, {float(z['seconds']) / 3600:.1f} h")
    F = z["F_n2"]; Ns = np.arange(2, int(z["Nmax"]) + 1)
    dphi = np.unwrap(np.angle(F[1, 1]) - np.angle(F[0, 1]))
    Nd = Ns[1:] * np.diff(dphi) / S[1, 1]
    print("(a) eps 0.21 beta 2, 2-stem N*d:", " ".join(f"{N}:{x:.4f}" for N, x in zip(Ns[1:], Nd)))
    for k in range(-2, 0):
        print(f"    effective exponent a (d ~ N^-a), N = {Ns[k - 1]}->{Ns[k]}: {1 - np.log(Nd[k] / Nd[k - 1]) / np.log(Ns[k] / Ns[k - 1]):.2f}")
    r0 = F[1, 0] / F[0, 0]
    print("(b) 2-stem q_N = |q|<phase/pi, N = 8-12")
    for i, (e, b) in enumerate(S):
        q = (F[1, i] / F[0, i]) / r0
        print(f"    eps {e:.2f} beta {b:4.1f}: " + " ".join(f"{N}:{abs(x):.3f}<{np.angle(x) / np.pi:+.2f}" for N, x in zip(Ns[-5:], q[-5:])))
    print("(c) median per-step |d ln|R|| and |d phase|/pi, steps ending at N = 10, 11, 12")
    for key, k in (("F_n3", 3), ("F_n4", 4)):
        G = z[key]
        for i in (1, 4):
            R = (G[1:, i] / G[0:1, i]) / (G[1:, 0] / G[0:1, 0])
            lm = np.abs(np.diff(np.log(np.abs(R)), axis=1))[:, -3:]
            ph = np.abs(np.diff(np.unwrap(np.angle(R), axis=1), axis=1))[:, -3:] / np.pi
            print(f"    {key} ({len(G)} stems) beta {S[i, 1]:.0f}: ln|R| {np.round(np.median(lm, axis=0), 3)}  phase {np.round(np.median(ph, axis=0), 3)}")

if __name__ == "__main__":
    main(sys.argv[1])
