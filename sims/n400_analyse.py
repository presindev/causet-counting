"""Analyse the N = 400 crystallisation runs (n400_crystal.py): hot vs cold starts per beta.

For each (beta, start): late-time means of S/N, r, layers per seed (last `frac` of each chain), then mean and
seed-to-seed spread across seeds (lesson 8: chains are correlated, so per-sample errors are meaningless).
Hysteresis flag: hot and cold late-time layer means differ by more than 3 x the combined seed spread.
Also checks drift: the last two quarters of each chain should agree, or the chain is still moving.
Sources per task, best first (session 8): final <name>.npz > <name>.partial.npz checkpoint > the 500-sweep log lines of a task
that died (TIMEOUT before checkpoints existed). Logs only carry S/N and layers, so r and acc are NaN for those; "src" says which was used.
Usage: python n400_analyse.py DIR [frac=0.5] [plot.png] [--logs LOGDIR]
"""
import sys, glob, os, re
import numpy as np
import warnings
warnings.filterwarnings("ignore", "Mean of empty slice")   # log-only runs have no r or acc

HEAD = re.compile(r"task (\d+)\s+beta (\S+)\s+start (\w+)\s+seed (\d+)")
LINE = re.compile(r"sweep (\d+) t=\S+ S/N=(\S+) layers=(\d+)")

def from_log(path):
    """One task's progress lines -> a run dict like the npz ones (sweep, S_N, layers; r, acc = NaN)."""
    head, rows = None, []
    for ln in open(path, errors="replace"):
        h = HEAD.search(ln)
        if h:
            head = h.groups()
        m = LINE.search(ln)
        if m:
            rows.append((int(m.group(1)), float(m.group(2)), int(m.group(3))))
    if head is None or len(rows) < 4:
        return None
    ts = np.array(rows)
    nan = np.full(len(ts), np.nan)
    return {"beta": float(head[1]), "start": head[2], "seed": int(head[3]), "sweep": ts[:, 0].astype(int), "S_N": ts[:, 1],
            "layers": ts[:, 2].astype(int), "r": nan, "acc": nan, "src": "log"}

def load(d, logdir=None):
    best = {}                                                # (beta, start, seed) -> run; lower rank wins
    rank = {"final": 0, "partial": 1, "log": 2}
    def offer(z):
        k = (float(z["beta"]), str(z["start"]), int(z["seed"]))
        if k not in best or rank[z["src"]] < rank[best[k]["src"]] or (
                z["src"] == best[k]["src"] and z["sweep"][-1] > best[k]["sweep"][-1]):   # same kind: keep the longest
            best[k] = z
    for f in sorted(glob.glob(d + "/*.npz")):
        z = np.load(f)
        z = {k: z[k] for k in z.files}
        z["src"] = "partial" if f.endswith(".partial.npz") else "final"
        offer(z)
    if logdir:
        for f in sorted(glob.glob(logdir + "/*.out")):
            z = from_log(f)
            if z:
                offer(z)
    runs = {}
    for (b, s, _), z in sorted(best.items()):
        runs.setdefault((b, s), []).append(z)
    return runs

def late(x, frac):
    return x[int(len(x) * (1 - frac)):].mean()

if __name__ == "__main__":
    args = sys.argv[1:]
    logdir = None
    if "--logs" in args:
        i = args.index("--logs"); logdir = args[i + 1]; del args[i:i + 2]
    d = args[0]
    frac = float(args[1]) if len(args) > 1 else 0.5
    runs = load(d, logdir)
    betas = sorted({b for b, _ in runs})
    print("late-time means (last {:.0%} of each chain), mean +- seed spread (sd across seeds), n = seeds".format(frac))
    print(" beta  start  n  sweeps      S/N              r             layers        drift(layers)  acc    sources (final/partial/log)")
    summary = {}
    for b in betas:
        for s in ("hot", "cold"):
            rs = runs.get((b, s))
            if not rs:
                continue
            m = np.array([[late(z["S_N"], frac), late(z["r"], frac), late(z["layers"].astype(float), frac),
                           late(z["layers"].astype(float), 0.25) - late(z["layers"][:int(0.75 * len(z["layers"]))].astype(float), 0.333),
                           np.nanmean(z["acc"][len(z["acc"]) // 2:])] for z in rs])
            src = "/".join(str(sum(z["src"] == k for z in rs)) for k in ("final", "partial", "log"))
            mu = np.nanmean(m, 0) if np.isfinite(m).any() else m.mean(0)
            sd = np.nanstd(m, 0, ddof=1) if len(m) > 1 else np.zeros(m.shape[1])
            summary[(b, s)] = (mu, sd, len(m))
            print("{:5.2f}  {:4s} {:2d} {:6d}  {:7.3f} +- {:5.3f}  {:5.3f} +- {:5.3f}  {:6.1f} +- {:4.1f}  {:+6.1f}        {:.3f}  {}".format(
                b, s, len(m), int(min(z["sweep"][-1] for z in rs)), mu[0], sd[0], mu[1], sd[1], mu[2], sd[2], mu[3], mu[4], src))
    print("\nhot vs cold (layers):")
    for b in betas:
        if (b, "hot") in summary and (b, "cold") in summary:
            (mh, sh, nh), (mc, sc, nc) = summary[(b, "hot")], summary[(b, "cold")]
            diff, err = mh[2] - mc[2], np.sqrt(sh[2]**2 / nh + sc[2]**2 / nc)
            if min(nh, nc) < 2:
                tag = "n/a (need >= 2 seeds per start)"
            else:
                tag = "HYSTERESIS (not equilibrated / metastable)" if abs(diff) > max(3 * err, 2) else "agree"
            print("  beta={:5.2f}: hot {:6.1f}  cold {:6.1f}  diff {:+6.1f}  (seed err {:.1f})  {}".format(b, mh[2], mc[2], diff, err, tag))
    if len(args) > 2:
        import matplotlib; matplotlib.use("Agg")           # laptop only (not on the cluster)
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(2, len(betas), figsize=(3 * len(betas), 5.5), sharex=True, squeeze=False)
        for j, b in enumerate(betas):
            for s, col in (("hot", "C3"), ("cold", "C0")):
                for z in runs.get((b, s), []):
                    ax[0, j].plot(z["sweep"], z["S_N"], col, lw=0.7, alpha=0.7)
                    ax[1, j].plot(z["sweep"], z["layers"], col, lw=0.7, alpha=0.7)
            ax[0, j].set_title("beta = {:g}".format(b))
            ax[1, j].set_xlabel("sweep")
        ax[0, 0].set_ylabel("S/N"); ax[1, 0].set_ylabel("layers")
        fig.suptitle("N = 400: hot (red) vs cold (blue) starts")
        fig.tight_layout(); fig.savefig(args[2], dpi=110)
        print("plot ->", args[2])
