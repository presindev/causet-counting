"""Clean timing table for the paper's cost paragraph (Sec. 9.5; idea 005, session 14), from r28 (exclusive node, one universe per n, seed 1001).
Johnston's pipeline (r14): his min-plus = johnston - CC - eigh, as r14 prints it. Ours: counting step (r14 ours_step). Likelihood pipeline (r24, Poisson arm):
ours_step + fit_K100 + setup + poisson_only. Exponents: log-log slope over n = 6000-15000.
Usage: python r28_timing.py DIR
"""
import sys, glob, os
import numpy as np

def timing(f):
    z = np.load(f)
    return int(z["n"]), dict(zip([str(k) for k in z["timing_keys"]], z["timing"]))

def main(d):
    r14 = dict(timing(f) for f in glob.glob(os.path.join(d, "r28_r14_n*.npz")))
    r24 = dict(timing(f) for f in glob.glob(os.path.join(d, "r28_r24_n*.npz")))
    ns = sorted(set(r14) & set(r24))
    rows = []
    print("     n   C@C  min-plus  eigh  | ours_step  fit_K100  setup  poisson_only  pipeline | pipeline / min-plus")
    for n in ns:
        a, b = r14[n], r24[n]
        mp = a["johnston"] - a["CC"] - a["eigh"]
        pipe = b["ours_step"] + b["fit_K100"] + b["setup"] + b["poisson_only"]
        rows.append((n, mp, a["ours_step"], pipe))
        print(f"{n:6d} {a['CC']:5.0f} {mp:9.0f} {a['eigh']:5.0f}  | {b['ours_step']:9.0f} {b['fit_K100']:9.0f} {b['setup']:6.0f} {b['poisson_only']:13.0f} {pipe:9.0f} | {pipe / mp:5.2f}")
    R = np.array([r for r in rows if r[0] >= 6000])
    if len(R) >= 2:
        sl = lambda y: np.polyfit(np.log(R[:, 0]), np.log(y), 1)[0]
        print(f"slopes n = 6000-15000: min-plus n^{sl(R[:, 1]):.2f}, our counting step n^{sl(R[:, 2]):.2f}, likelihood pipeline n^{sl(R[:, 3]):.2f}")

if __name__ == "__main__":
    main(sys.argv[1])
