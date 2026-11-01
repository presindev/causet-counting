"""Analysis of r35 (external referee round 1, 3+1 paper): runs/r35/r35_n*_s*.npz, one universe each.
Per n: mean spatial correlation per arm; fraction of Johnston's residual removed, (C - C_J) / (1 - C_J), as the mean over universes of the paired
difference divided by the mean residual (the paper's definition), plus its per-universe spread (min, median, max, s.d.);
lnL of each fixed-t arm minus the truth-started optimum; per-pair distance errors |d_emb - d_true| / ell (quantiles) and causal fidelity for
Johnston, fit and fit_lbfgs; and, for the error-location figure, the rms per-element position error (best orthogonal map) of Johnston and the
fit binned by the element's number of related partners and by its time coordinate.
Usage: python r35_analyse.py <folder> [fig]
"""
import sys
import glob
import numpy as np
from r13_mixed import sprinkle                        # noqa: F401  (documentation: universes are r14's)
from r11_4d_distance import precedes
from r14_cluster_scale import spatial_dist

ARMS = ("start", "fit", "fit_lbfgs", "jstart", "pstart", "truth", "exact_all", "exact_near", "gauss_near", "joint")

def load(folder):
    Z = {}
    for f in sorted(glob.glob(folder + "/r35_n*_s*.npz")):
        z = np.load(f)
        if "X_joint" not in z.files:
            continue                                  # unfinished universe
        Z.setdefault(int(z["n"]), []).append(z)
    return Z

def pos_err(X, P):
    A = X - X.mean(0); B = P - P.mean(0)
    U, _, Vt = np.linalg.svd(A.T @ B)
    return np.sqrt(((A @ U @ Vt - B) ** 2).sum(1))

def fidelity(X, rel, iu):
    dt2 = (X[:, None, 0] - X[None, :, 0]) ** 2
    dx2 = ((X[:, None, 1:] - X[None, :, 1:]) ** 2).sum(-1)
    return np.mean((dt2 > dx2)[iu] != rel)

def summary(Z):
    for n, zs in sorted(Z.items()):
        names = list(zs[0]["names"])
        C = np.array([[z["corr"][list(z["names"]).index(a)] for a in ["johnston"] + list(ARMS)] for z in zs])
        cj = C[:, 0]
        print(f"n = {n}: {len(zs)} universes (seeds {', '.join(str(int(z['seed'])) for z in zs)})")
        print(f"  johnston  C {cj.mean():.4f}  (1 - C = {1 - cj.mean():.4f})")
        for i, a in enumerate(ARMS, 1):
            d = C[:, i] - cj
            frac = d.mean() / (1 - cj.mean())
            per = d / (1 - cj)
            se = d.std(ddof=1) / np.sqrt(len(d)) if len(d) > 1 else np.nan
            print(f"  {a:10s} C {C[:, i].mean():.4f}  gain {d.mean():+.4f} ({se:.4f})  removed {100 * frac:5.1f} %   per universe: min {100 * per.min():5.1f}"
                  f"  median {100 * np.median(per):5.1f}  max {100 * per.max():5.1f}  s.d. {100 * per.std(ddof=1) if len(per) > 1 else np.nan:4.1f}  wins {np.sum(d > 0)}/{len(d)}")
        for a, b in (("exact_near", "exact_all"), ("gauss_near", "fit"), ("exact_all", "fit"), ("fit_lbfgs", "fit"), ("jstart", "fit_lbfgs"),
                     ("joint", "fit_lbfgs")):
            d = C[:, 1 + ARMS.index(a)] - C[:, 1 + ARMS.index(b)]
            print(f"    paired {a} - {b}: {d.mean():+.5f} ({d.std(ddof=1) / np.sqrt(len(d)) if len(d) > 1 else np.nan:.5f}), positive in {np.sum(d > 0)}/{len(d)}")
        L = np.array([[z["lnl"][list(z["names"]).index(a)] for a in ("fit", "fit_lbfgs", "jstart", "pstart", "truth")] for z in zs])
        g = L[:, 4:5] - L[:, :4]
        print("  lnL(truth start) - lnL(arm), mean [min, max]: " + "  ".join(f"{a} {g[:, i].mean():.1f} [{g[:, i].min():.1f}, {g[:, i].max():.1f}]"
              for i, a in enumerate(("fit", "fit_lbfgs", "jstart", "pstart"))))
        best = np.argmax(L[:, 1:4], 1)                                # best of three converged starts by lnL
        Cb = np.array([C[k, 1 + ARMS.index(("fit_lbfgs", "jstart", "pstart")[best[k]])] for k in range(len(zs))])
        print(f"  best-lnL of three starts: C {Cb.mean():.4f}, removed {100 * (Cb - cj).mean() / (1 - cj.mean()):.1f} %")
        print("  near-cone share of related pairs %.2f; time error rms (ell): Johnston %.3f, joint %.3f" % (
              np.mean([z["timing"][list(z["timing_keys"]).index("near_share")] for z in zs]),
              np.mean([z["timing"][list(z["timing_keys"]).index("johnston_time_rms")] for z in zs]),
              np.mean([z["timing"][list(z["timing_keys"]).index("joint_time_rms")] for z in zs])))
        Q, F = {}, {}
        for z in zs:
            P = z["P"].astype(float); ell = float(z["ell"]); iu = np.triu_indices(len(P), 1)
            st = spatial_dist(P, iu); rel = (lambda Cm: (Cm | Cm.T)[iu])(precedes(P, P))
            for a in ("johnston", "fit", "fit_lbfgs"):
                X = z["X_" + a].astype(float)
                Q.setdefault(a, []).append(np.quantile(np.abs(spatial_dist(X, iu) - st) / ell, (0.5, 0.9, 0.99)))
                F.setdefault(a, []).append(fidelity(X, rel, iu))
        for a in Q:
            q = np.mean(Q[a], 0)
            print(f"  {a:10s} |dd|/ell q50 {q[0]:.2f} q90 {q[1]:.2f} q99 {q[2]:.2f};  misclassified pairs {100 * np.mean(F[a]):.2f} % [{100 * np.min(F[a]):.2f}, {100 * np.max(F[a]):.2f}]")

def location(Z, out="../paper/figs/fig_3p1_errloc_v3"):
    """Error-location figure (minor comment of the referee): per-element position error vs number of related partners and vs time."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 10, "axes.labelsize": 10, "xtick.labelsize": 9, "ytick.labelsize": 9, "legend.fontsize": 9})
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 3.0))                    # printed at full page width (figure*), session 18
    for n, mk in ((3000, "o"), (6000, "s")):
        if n not in Z:
            continue
        rows = {"johnston": [], "fit_lbfgs": []}
        for z in Z[n]:
            P = z["P"].astype(float); ell = float(z["ell"])
            Cm = precedes(P, P); k = (Cm | Cm.T).sum(1)
            kq = np.argsort(np.argsort(k)) / (len(k) - 1)             # rank of the element's related-partner count, 0..1
            for a in rows:
                e = pos_err(z["X_" + a][:, 1:].astype(float), P[:, 1:]) / ell
                rows[a].append(np.column_stack([kq, P[:, 0], e]))
        for a, col in (("johnston", "C1"), ("fit_lbfgs", "C0")):
            A = np.vstack(rows[a])
            for ax, j, bins in ((axs[0], 0, np.linspace(0, 1, 11)), (axs[1], 1, np.linspace(0, 1, 11))):
                b = np.digitize(A[:, j], bins[1:-1])
                y = [np.sqrt((A[b == i, 2] ** 2).mean()) for i in range(len(bins) - 1)]
                ax.plot(0.5 * (bins[1:] + bins[:-1]), y, mk + "-", color=col, ms=4, lw=1.3,
                        label=f"{'Johnston' if a == 'johnston' else 'likelihood fit'}, $n={n}$")
    axs[0].set_xlabel("rank of related-partner count (decile)"); axs[1].set_xlabel("true time $t$ (diamond height 1)")
    for ax in axs:
        ax.set_ylabel(r"rms position error / $\ell$"); ax.set_yscale("log")
    axs[0].legend(frameon=False, loc="upper right")
    fig.tight_layout(); fig.savefig(out + ".pdf"); print("wrote", out + ".pdf")

if __name__ == "__main__":
    Z = load(sys.argv[1])
    summary(Z)
    if len(sys.argv) > 2 and sys.argv[2] == "fig":
        location(Z)
