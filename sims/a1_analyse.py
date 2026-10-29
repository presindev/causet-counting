"""A1 analysis (ideas 002, 005): quantum vs classical record probabilities from the raw cluster samples (a1_sample.py).

Uniform 2D orders are the beta = 0 ensemble, so for any record r:
    A_r(beta) ~ sum_{samples in r} e^{i beta S}          (quantum amplitude, up to a common factor)
    P_q(r)    = |A_r|^2 / sum_r |A_r|^2                 (universes with the same record interfere, lesson 3)
    P_c(r)    = sum_{r} e^{-beta S} / sum e^{-beta S}    (classical reweighting; unreliable once a few samples dominate)
Amplitudes are pooled over all seeds (they are plain sums). Errors: jackknife over seeds (delete one seed), so they
are run-to-run errors (lesson 8). Noise floor of a bin with n samples: |A_r|/n ~ 1/sqrt(n).
Baseline: at beta = 0, A_r = n_r (the bin count), so P_q(r) = n_r^2 / sum n^2, not n_r / n. Compare each beta with
the quantum beta = 0 row, not with the classical column (equal for stress quartiles only, by construction).
Records:  stress quartile (Q1 most manifold-like)  and  layer count (AGE), grouped into quartile-like bins.
Usage: python a1_analyse.py dir_with_npz [beta_max]
"""
import sys, glob
import numpy as np

def load(d):
    files = sorted(glob.glob(f"{d}/a1_N*_s*.npz"))
    runs = [np.load(f) for f in files]
    return [(r["S"], r["stress"].astype(float), r["layers"].astype(int)) for r in runs], int(runs[0]["N"])

def probs(S, rec, nrec, beta):
    amp = np.exp(1j * beta * S)
    A = np.array([amp[rec == r].sum() for r in range(nrec)])
    w = np.exp(-beta * (S - S.min()))
    W = np.array([w[rec == r].sum() for r in range(nrec)])
    ess = w.sum()**2 / (w**2).sum()                      # effective sample size of the classical reweighting
    return np.abs(A)**2 / (np.abs(A)**2).sum(), W / W.sum(), ess

def jackknife(runs, recs, nrec, beta):
    S_all, rec_all = np.concatenate([r[0] for r in runs]), np.concatenate(recs)
    Pq, Pc, ess = probs(S_all, rec_all, nrec, beta)
    k = len(runs)
    if k < 3:
        return Pq, np.full(nrec, np.nan), Pc, ess
    jq = np.array([probs(np.concatenate([r[0] for j, r in enumerate(runs) if j != i]),
                         np.concatenate([x for j, x in enumerate(recs) if j != i]), nrec, beta)[0] for i in range(k)])
    return Pq, np.sqrt((k - 1) / k * ((jq - jq.mean(0))**2).sum(0)), Pc, ess

def report(name, runs, recs, labels, betas):
    nrec, n = len(labels), sum(len(r[0]) for r in runs)
    counts = np.bincount(np.concatenate(recs), minlength=nrec)
    print(f"\nrecord = {name}: bins {labels}, counts {counts.tolist()}")
    for beta in betas:
        Pq, eq, Pc, ess = jackknife(runs, recs, nrec, beta)
        ph = np.abs(np.exp(1j * beta * np.concatenate([r[0] for r in runs])).mean())
        fq = "  ".join(f"{m:.3f}±{e:.3f}" for m, e in zip(Pq, eq))
        fc = "  ".join(f"{m:.3f}" for m in Pc)
        print(f"  beta={beta:.2f} |<phase>|={ph:.4f} (floor {1/np.sqrt(n):.4f})  quantum: {fq}   "
              f"classical: {fc}  (ESS {ess:.0f})")

if __name__ == "__main__":
    runs, N = load(sys.argv[1])
    bmax = float(sys.argv[2]) if len(sys.argv) > 2 else 0.3
    betas = np.round(np.arange(0, bmax + 1e-9, 0.05), 2)
    S = np.concatenate([r[0] for r in runs])
    print(f"N = {N}, {len(runs)} seeds, {len(S)} universes; <S> = {S.mean():.2f}, sd_S = {S.std():.2f}; "
          f"expected |<phase>| = exp(-beta^2 sd^2/2)")
    st_all = np.concatenate([r[1] for r in runs])
    edges = np.nanquantile(st_all, [0.25, 0.5, 0.75])
    report("stress quartile (Q1 most manifold-like)", runs, [np.digitize(r[1], edges) for r in runs],
           ["Q1", "Q2", "Q3", "Q4"], betas)
    L_all = np.concatenate([r[2] for r in runs])
    ledges = np.unique(np.quantile(L_all, [0.25, 0.5, 0.75]))
    lab = [f"<={ledges[0] - 1:.0f}"] + [f"{a:.0f}-{b - 1:.0f}" for a, b in zip(ledges[:-1], ledges[1:])] + \
          [f">={ledges[-1]:.0f}"]                       # integer layer counts, inclusive ranges
    print(f"\nlayer count: mean {L_all.mean():.2f}, sd {L_all.std():.2f} (2 sqrt N = {2*np.sqrt(N):.1f})")
    report("layer count (AGE)", runs, [np.digitize(r[2], ledges, right=False) for r in runs], lab, betas)
