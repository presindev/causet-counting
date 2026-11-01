"""Figure for the 3+1 section of the full paper (session 12; v2 session 13): Johnston 2025 vs ours alone vs the switch vs the count-weighted fit vs the
Poisson likelihood, from the cluster runs.

  (a) residual 1 - rho (spatial corr, his Table V metric) against n, log-log, mean over universes (error bars: spread / sqrt(#universes))
  (b) time per universe against n: his min-plus, our overlap step, the likelihood pipeline (our step + weighted start + 400 Poisson iterations)

Reads runs/cluster_fetch/r14/out (r14_cluster_scale.py: johnston, ours, switch0.25) and runs/cluster_fetch/r24/out (r24_cluster_lik.py: w_K100, poisson_only),
paired by (n, seed). No simulation. Every number plotted is also printed, with log-log slopes over n = 6000-15000.
Usage: .venv/bin/python sims/fig_3p1.py          (--prd: panel (a) only, without the switch, for the split 3+1 paper -> fig_3p1_prd; session 15)
       --prd --r35: v2 of the 3+1 paper (session 17): for n <= 6000 Johnston, the starting map and the fit come from runs/r35 (ten universes per size;
       r35 "start" = w_K100, "fit" = poisson_only); the direct overlap embedding ("ours") keeps the r14 universes. Writes fig_3p1_prd_v2 (v1 file untouched).
"""
import os, sys, glob
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "paper", "figs")
D14, D24 = os.path.join(ROOT, "runs", "cluster_fetch", "r14", "out"), os.path.join(ROOT, "runs", "cluster_fetch", "r24", "out")

BLUE, ORANGE, AQUA, INK, GREY, PURPLE = "#2a78d6", "#eb6834", "#1baf7a", "#0b0b0b", "#8a8984", "#7a4fc9"
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 0.6,
                     "xtick.major.width": 0.6, "ytick.major.width": 0.6, "lines.linewidth": 1.5,
                     "legend.frameon": False, "savefig.bbox": "tight", "pdf.fonttype": 42})

def load(folder, prefix):
    return {(int(z["n"]), int(z["seed"])): z for z in (np.load(f) for f in glob.glob(os.path.join(folder, prefix + "_n*_s*.npz")))}

def get(z, name, key="spatial"):
    return float(z[key][list(z["names"]).index(name)])

def tget(z, key):
    return float(dict(zip(z["timing_keys"], z["timing"]))[key])

def main():
    r14, r24 = load(D14, "r14"), load(D24, "r24")
    ns = sorted({k[0] for k in r14})
    methods = [("johnston", "Johnston 2025", INK, "o", "-"), ("ours", "ours alone", BLUE, "s", "-"),
               ("switch0.25", "switch ($L=0.25$)", ORANGE, "D", "--"), ("w_K100", "count-weighted fit", GREY, "v", "--"),
               ("poisson_only", "Poisson likelihood", AQUA, "^", "-")]
    if PRD:
        methods = [m for m in methods if m[0] != "switch0.25"]
        relab = {"johnston": "Johnston (2025)", "ours": "overlap distances, direct", "w_K100": "weighted starting map", "poisson_only": "likelihood fit"}
        methods = [(k, relab[k], c, mk, ls) for k, lab, c, mk, ls in methods]
    r35 = {}
    if R35:
        for f in glob.glob(os.path.join(ROOT, "runs", "r35", "r35_n*_s*.npz")):
            z = np.load(f)
            if "X_joint" in z.files:
                r35.setdefault(int(z["n"]), []).append(z)
    res = {m[0]: [] for m in methods}
    times = {"his min-plus": [], "our step": [], "likelihood pipeline": []}
    print("n  #univ  " + "  ".join("%-11s" % m[0] for m in methods) + "   likelihood wins  share of his residual (switch, likelihood)")
    for n in ns:
        keys = sorted(k for k in r14 if k[0] == n and k in r24)
        assert all(int(r14[k]["npts"]) == int(r24[k]["npts"]) for k in keys), "unpaired universes"
        row = {}
        for m in methods:
            src = r24 if m[0] in ("w_K100", "poisson_only") else r14
            v = np.array([1 - get(src[k], m[0]) for k in keys])
            if n in r35 and m[0] != "ours":
                nm = {"johnston": "johnston", "w_K100": "start", "poisson_only": "fit"}[m[0]]
                v = np.array([1 - float(z["corr"][list(z["names"]).index(nm)]) for z in r35[n]])
            row[m[0]] = v
            res[m[0]].append((v.mean(), v.std(ddof=1) / np.sqrt(len(v)) if len(v) > 1 else 0.0))
        wins = int(np.sum(row["poisson_only"] < row["johnston"]))
        keys = keys if n not in r35 else [None] * len(r35[n])
        sh = [1 - row[m].mean() / row["johnston"].mean() if m in row else np.nan for m in ("switch0.25", "poisson_only")]
        print("%5d  %d   " % (n, len(keys)) + "  ".join("%-11.4f" % res[m[0]][-1][0] for m in methods) + "   %d/%d        %.0f %%, %.0f %%" % (wins, len(keys), 100 * sh[0], 100 * sh[1]))
        k14 = sorted(k for k in r14 if k[0] == n and k in r24)
        tj = np.mean([tget(r14[k], "johnston") - tget(r14[k], "CC") - tget(r14[k], "eigh") for k in k14])
        to = np.mean([tget(r14[k], "ours_step") for k in k14])
        tl = np.mean([tget(r24[k], "ours_step") + tget(r24[k], "fit_K100") + tget(r24[k], "poisson_only") for k in k14])
        times["his min-plus"].append(tj); times["our step"].append(to); times["likelihood pipeline"].append(tl)
    print("time (s): " + "; ".join("%s %s" % (k, ", ".join("%.0f" % x for x in v)) for k, v in times.items()))
    big = [i for i, n in enumerate(ns) if n >= 6000]
    lx = np.log([ns[i] for i in big])
    for m in methods:
        y = np.log([res[m[0]][i][0] for i in big])
        print("slope of 1-rho, n = 6000-15000: %-12s %.2f" % (m[0], np.polyfit(lx, y, 1)[0]))
    for k, v in times.items():
        print("slope of time,  n = 6000-15000: %-12s %.2f" % (k, np.polyfit(lx, np.log([v[i] for i in big]), 1)[0]))

    if PRD:
        fig, ax1 = plt.subplots(figsize=(3.4, 2.6)); ax2 = None
    else:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.8, 2.8))
    for key, lab, col, mk, ls in methods:
        mu = np.array([r[0] for r in res[key]]); se = np.array([r[1] for r in res[key]])
        ax1.errorbar(ns, mu, yerr=se, color=col, marker=mk, ms=3.5, ls=ls, lw=1.2, capsize=1.5, label=lab)
    ax1.set_xscale("log"); ax1.set_yscale("log")
    ax1.set_xlabel("number of elements $n$" if PRD else "number of events $n$")
    ax1.set_ylabel(r"residual $1-\mathcal{C}$" if PRD else r"residual $1-\rho$ (spatial)")
    if not PRD:
        ax1.set_title("(a) embedding error", fontsize=9, loc="left")
    ax1.set_ylim(3e-4, 0.5)                                       # room below the curves for the legend
    ax1.legend(fontsize=7, loc="lower left")
    if ax2 is not None:
        for (lab, v), col, mk in zip(times.items(), (INK, BLUE, AQUA), ("o", "s", "^")):
            ax2.plot(ns, v, color=col, marker=mk, ms=3.5, lw=1.2, label=lab)
        ax2.set_xscale("log"); ax2.set_yscale("log")
        ax2.set_xlabel("number of events $n$"); ax2.set_ylabel("time per universe (s)")
        ax2.set_title("(b) cost", fontsize=9, loc="left")
        ax2.legend(fontsize=7, loc="upper left")
    os.makedirs(OUT, exist_ok=True)
    name = ("fig_3p1_prd_v2" if R35 else "fig_3p1_prd") if PRD else "fig_3p1"
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(OUT, name + "." + ext), **({"dpi": 150} if ext == "png" else {}))
    print("wrote", os.path.join(OUT, name + ".pdf"))

PRD = "--prd" in sys.argv
R35 = "--r35" in sys.argv

if __name__ == "__main__":
    main()
