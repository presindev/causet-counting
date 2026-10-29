"""Figures for Part I of the draft (session 11): one function per figure, PDFs into paper/figs/.

  distance   rectangle-identity estimate vs true distance, flat 2D sprinklings (s4a_overlap_distance.py)
  drift      d_est^2 / d^2 vs depth of c, de Sitter vs flat, with the exact continuum curve (s4a_desitter.py)
  detector   embedding stress and r+ vs N on flat universes; N = 400 MCMC universes; stress vs H tau (s4b_*.py)
  laguerre   <K> vs interval size n against 1/2 L_n(mu/2): random orders, N = 400 MCMC universes, crystals (b_johnston_n400.py)

Laptop only (matplotlib from the project .venv). Every number printed is also what is plotted.
Usage: .venv/bin/python sims/fig_part1.py [distance|drift|detector|laguerre ...]   (no argument: all four)
"""
import os, sys, glob
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "paper", "figs")

# dataviz reference palette, first three categorical slots (validated all-pairs) + ink for targets
BLUE, ORANGE, AQUA, INK, GREY = "#2a78d6", "#eb6834", "#1baf7a", "#0b0b0b", "#8a8984"
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 0.6,
                     "xtick.major.width": 0.6, "ytick.major.width": 0.6, "lines.linewidth": 1.5,
                     "legend.frameon": False, "savefig.bbox": "tight", "pdf.fonttype": 42})

def save(fig, name):
    os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, name + ".pdf"))
    fig.savefig(os.path.join(OUT, name + ".png"), dpi=150)
    print("wrote", os.path.join(OUT, name + ".pdf"))


def fig_distance():
    import s4a_overlap_distance as od
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.6, 2.7))
    edges = np.array([0.5, 1, 2, 3, 5, 7, 10, 15, 20, 30, 45])
    for n, col, mk in ((1000, BLUE, "o"), (4000, ORANGE, "s")):
        R = []
        for s in (1, 2, 3, 4):
            rows, rho = od.run(n, 300, s)
            R.append(rows)
        R = np.vstack(R)
        ell = rho ** -0.5
        x, y = R[:, 0] / ell, R[:, 2] / ell                       # deepest c
        if n == 4000:
            ax1.scatter(x, y, s=3, color=col, alpha=0.35, lw=0)
        rel = np.abs(y / x - 1)
        idx = np.digitize(x, edges) - 1
        mid, med = [], []
        for i in range(len(edges) - 1):
            m = idx == i
            if m.sum() > 10:
                mid.append(np.sqrt(edges[i] * edges[i + 1])); med.append(np.median(rel[m]))
        ax2.plot(mid, med, marker=mk, ms=4, color=col, label=f"N = {n}")
        print(f"distance N={n}: " + " ".join(f"{a:.1f}:{b:.3f}" for a, b in zip(mid, med)))
    lim = [0.5, 60]
    ax1.plot(lim, lim, color=INK, lw=0.8)
    ax1.set(xscale="log", yscale="log", xlim=lim, ylim=lim, xlabel=r"true distance $d/\ell$", ylabel=r"estimate $d_{\rm est}/\ell$")
    ax1.set_title("(a) N = 4000, 1200 pairs", fontsize=9, loc="left")
    ax2.axvline(2, color=GREY, lw=0.6, ls=":")
    ax2.set(xscale="log", xlabel=r"true distance $d/\ell$", ylabel="median relative error", ylim=(0, None))
    ax2.set_title("(b) error vs distance", fontsize=9, loc="left")
    ax2.legend()
    save(fig, "fig_distance")


def fig_drift():
    import s4a_desitter as ds
    rho, eta0, delta, seeds = 10000.0, -1.05, 0.15, range(1, 401)
    bins = np.array([0.05, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9])
    mid = (bins[1:] + bins[:-1]) / 2
    fig, ax = plt.subplots(figsize=(3.4, 2.7))
    for desitter, col, mk, lab in ((False, BLUE, "o", "flat (control)"), (True, ORANGE, "s", "de Sitter, $H=1$")):
        P, Q = [], []
        for s in seeds:
            tau, r, pred, *_ = ds.run(rho, desitter, eta0, delta, s)
            sel = [(tau >= lo) & (tau < hi) for lo, hi in zip(bins[:-1], bins[1:])]
            P.append([np.mean(r[m]) if m.sum() > 5 else np.nan for m in sel])
            Q.append([np.mean(pred[m]) if m.sum() > 5 else np.nan for m in sel])
        P, Q = np.array(P), np.array(Q)
        m, e = np.nanmean(P, 0), np.nanstd(P, 0) / np.sqrt(np.isfinite(P).sum(0))
        ax.errorbar(mid, m, yerr=e, fmt=mk, ms=4, color=col, capsize=2, lw=1, label=lab + ", sprinkled")
        if desitter:   # continuum averaged over the same c's (each bin holds c's at many x_c, not only straight below)
            ax.plot(mid, np.nanmean(Q, 0), "-", color=INK, lw=1, label="continuum, same $c$'s")
        print(f"drift {lab}: " + " ".join(f"{a:.2f}:{b:.4f}±{c:.4f}(cont {d:.4f})" for a, b, c, d in zip(mid, m, e, np.nanmean(Q, 0))))
    t = np.linspace(0, 0.9, 50)
    ax.plot(t, 1 - t ** 2 / 8, color=INK, lw=0.8, ls="--", label=r"$1-R\tau^2/16$ (small $\tau$)")
    ax.axhline(1, color=GREY, lw=0.6, ls=":")
    ax.set(xlabel=r"depth of $c$ below $a,b$: proper time $\tau$", ylabel=r"$d_{\rm est}^2/d^2$")
    ax.set_ylim(0.83, 1.01)
    ax.legend(fontsize=7, loc="lower left")
    save(fig, "fig_drift")


def order(u, v):
    return (u[:, None] < u[None, :]) & (v[:, None] < v[None, :])


def fig_detector():
    from s4b_detector import diagnostics
    from s4b_desitter_stress import desitter_diamond
    rng = np.random.default_rng(1)
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(7.0, 2.6), gridspec_kw={"width_ratios": [1.1, 1, 1]})
    Ns, reps = (20, 50, 100, 200, 400), 10
    res = {}
    for N in Ns:
        D = []
        for _ in range(reps):
            u, v = rng.permutation(N), rng.permutation(N)
            d = diagnostics((u[:, None] < u[None, :]) & (v[:, None] < v[None, :]))
            if d is not None:
                D.append(d)
        res[N] = np.array(D)
        print(f"detector flat N={N}: stress {res[N][:, 3].mean():.3f}±{res[N][:, 3].std():.3f}  r+ {res[N][:, 1].mean():.3f}±{res[N][:, 1].std():.3f}")
    for k, col, mk, lab in ((3, BLUE, "o", "stress"), (1, ORANGE, "s", r"$r_+$")):
        m = [res[N][:, k].mean() for N in Ns]; e = [res[N][:, k].std() for N in Ns]
        ax1.errorbar(Ns, m, yerr=e, fmt=mk + "-", ms=4, color=col, capsize=2, lw=1, label=lab)
    ax1.set(xscale="log", xlabel="universe size N", ylabel="value (mean ± sd)", ylim=(0, None))
    ax1.set_xticks(Ns); ax1.set_xticklabels([str(n) for n in Ns]); ax1.minorticks_off()
    ax1.set_title("(a) flat universes vs N", fontsize=9, loc="left")
    ax1.legend(fontsize=7.5)
    # (b) the layering flag (r8_detector_spread.py): share of zero-length pairs over a top and a depth-spread sample, N = 400.
    #     Threshold 1.5 x the flat median at the same N. Monte Carlo final states (jobs 449411/449800) by layer count; de Sitter at H tau = 4.
    from r8_detector_spread import features
    zs = lambda Cs: np.array([f[2] for f in (features(C, 80, 3, rng) for C in Cs) if f is not None])
    fs = sorted({os.path.basename(f): f for f in glob.glob(os.path.join(ROOT, "n400_*", "**", "*.npz"), recursive=True)
                 if "partial" not in f}.values())
    load = lambda f: (int(np.load(f)["layers"][-1]), order(np.load(f)["u"].astype(int), np.load(f)["v"].astype(int)))
    states = [load(f) for f in fs]
    groups = {"flat": zs([order(rng.permutation(400), rng.permutation(400)) for _ in range(30)]),
              "de Sitter\n$H\\tau=4$": zs([desitter_diamond(400, 4.0, rng) for _ in range(10)]),
              "MCMC\ncont.": zs([C for nl, C in states if nl > 25]),
              "MCMC\nlayered": zs([C for nl, C in states if 3 < nl <= 25])}
    thr = 1.5 * np.median(groups["flat"])
    for i, (g, vals) in enumerate(groups.items()):
        col = ORANGE if i == 3 else BLUE
        ax2.scatter(i + rng.uniform(-0.15, 0.15, len(vals)), vals, s=12, facecolor="none", edgecolor=col, lw=0.8)
        print(f"detector (b) {g!r}: zero share {vals.min():.3f}-{vals.max():.3f}, above threshold {(vals > thr).sum()}/{len(vals)}")
    ax2.axhline(thr, color=INK, lw=0.6, ls="--")
    ax2.text(3.45, thr * 1.08, "flag", fontsize=7, ha="right")
    ax2.set_xticks(range(len(groups))); ax2.set_xticklabels(list(groups), fontsize=6.5)
    ax2.set(yscale="log", ylabel="share of zero-length pairs", xlim=(-0.5, 3.5))
    ax2.set_title("(b) layering flag, N = 400", fontsize=9, loc="left")
    print(f"detector (b): threshold {thr:.3f}; 2-3-layer states where the pipeline cannot run: {sum(1 for nl, _ in states if nl <= 3)}")
    lo, hi = res[400][:, 3].mean() - res[400][:, 3].std(), res[400][:, 3].mean() + res[400][:, 3].std()
    ax3.axhspan(lo, hi, color=BLUE, alpha=0.15, lw=0)
    taus = (0.05, 0.5, 1.0, 2.0, 3.0, 4.0)
    S = []
    for t in taus:
        D = np.array([diagnostics(desitter_diamond(400, t, rng)) for _ in range(8)])
        S.append((D[:, 3].mean(), D[:, 3].std()))
        print(f"detector dS H tau={t}: stress {S[-1][0]:.3f}±{S[-1][1]:.3f}")
    S = np.array(S)
    ax3.errorbar(taus, S[:, 0], yerr=S[:, 1], fmt="s-", ms=4, color=ORANGE, capsize=2, lw=1)
    ax3.set(xlabel=r"$H\tau$ (curvature $\times$ size)", ylabel="stress", ylim=(0, None))
    ax3.set_title("(c) de Sitter, N = 400", fontsize=9, loc="left")
    fig.tight_layout()
    save(fig, "fig_detector")


def fig_laguerre():
    import b_johnston_n400 as bj
    mu = 0.05
    edges = np.arange(0, 401, 10)
    rng = np.random.default_rng(7)
    fig, ax = plt.subplots(figsize=(6.6, 2.8))
    nn = np.arange(0, 400)
    ax.plot(nn, 0.5 * bj.laguerre_table(400, mu / 2)[:400], color=INK, lw=1, label=r"target $\frac{1}{2} L_n(\mu/2)$", zorder=3)

    def binned(u, v):
        C, n, K = bj.propagator(u, v, mu)
        x, k = n[C], K[C]
        idx = np.digitize(x, edges) - 1
        out = [(x[idx == i].mean(), k[idx == i].mean()) for i in range(len(edges) - 1) if (idx == i).sum() > 5]
        return np.array(out)

    B = binned(rng.permutation(400), rng.permutation(400))
    ax.plot(B[:, 0], B[:, 1], "o", ms=3, color=BLUE, label="random 2D order (sprinkling), N = 400")
    pick = {"n400_b0.01_hot_s2000.npz": (AQUA, "D", "MCMC, continuum-like (38 layers)"),
            "n400_b0.08_cold_s2037.npz": (ORANGE, "s", "MCMC crystal, 7 layers"),
            "n400_b0.08_cold_s2036.npz": (ORANGE, "^", "MCMC crystal, 4 layers (all n < 10)")}
    for name, (col, mk, lab) in pick.items():
        f = glob.glob(os.path.join(ROOT, "n400_*", "**", name), recursive=True)[0]
        z = np.load(f)
        B = binned(z["u"].astype(int), z["v"].astype(int))
        ax.plot(B[:, 0], B[:, 1], mk, ms=3.5, mfc="none" if "4 layers" in lab else col, mec=col, mew=0.8, color=col, label=lab)
        print(f"laguerre {lab}: n_max {B[:, 0].max():.0f}, " + " ".join(f"{a:.0f}:{b:+.3f}" for a, b in B[:8]))
    ax.axhline(0, color=GREY, lw=0.6, ls=":")
    ax.set(xlabel=r"interval size $n$ (events strictly between $x$ and $y$)", ylabel=r"mean propagator $\langle K\rangle$",
           xlim=(0, 400), ylim=(-0.6, 0.8))
    ax.set_title(r"$\mu = m^2/\rho = 0.05$", fontsize=9, loc="left")
    ax.legend(fontsize=7, loc="upper right", ncol=2)
    save(fig, "fig_laguerre")


if __name__ == "__main__":
    np.seterr(all="ignore")                       # numpy + Accelerate: spurious matmul warnings
    which = sys.argv[1:] or ["distance", "drift", "detector", "laguerre"]
    for w in which:
        globals()["fig_" + w]()
