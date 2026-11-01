"""Summary of r39 (3+1 referee round 2): python r39_summary.py runs/r39/r39_n3000.npz  |  python r39_summary.py relaxlong runs/r39/relaxlong_n3000.npz C_J"""
import sys
import numpy as np
def main(path):
    z = np.load(path); s = z["s_grid"]; i0, i1 = np.flatnonzero(s == 0)[0], np.flatnonzero(s == 1)[0]
    g = z["lnl_truth"] - z["lnl_fit_lbfgs"]
    best3 = np.max([z["lnl_fit_lbfgs"], z["lnl_jstart"], z["lnl_pstart"]], 0)
    print(f"n {int(z['n'][0])}: {len(g)} universes; lnL truth - fit_lbfgs: {np.round(g, 2)}; higher in {np.sum(g > 0)}/{len(g)}; mean {g.mean():.2f}, max {g.max():.2f};"
          f" truth > best of three converged starts in {np.sum(z['lnl_truth'] > best3)}")
    print(f"  C fit_lbfgs {z['C_fit_lbfgs'].mean():.5f}, truth {z['C_truth'].mean():.5f}; related pairs {z['related'].mean():.3g}")
    print(f"  rms(truth - fit) raw {z['rms_raw'].mean():.2f} ell; after best O(3) about the time axis {z['rms_aligned'].mean():.2f} ell [{z['rms_aligned'].min():.2f}, {z['rms_aligned'].max():.2f}]")
    dip = z["path_lnl"] - z["path_lnl"][:, [i0]]
    print(f"  straight path: barrier (line minus path, max in [0,1]) mean {z['barrier'].mean():.0f} [{z['barrier'].min():.0f}, {z['barrier'].max():.0f}];"
          f" lnL(0.5) - lnL(0) mean {dip[:, np.flatnonzero(s == 0.5)[0]].mean():.0f}")
    for t in (0.25, 0.5, 0.75):
        dl = z[f"relax{t}_lnl"] - z["lnl_fit_lbfgs"]
        print(f"  relaxed from s = {t}: C {z[f'relax{t}_C'].mean():.5f}; lnL - fit_lbfgs mean {dl.mean():+.2f} [{dl.min():+.2f}, {dl.max():+.2f}];"
              f" distance to fit {z[f'relax{t}_d1'].mean():.2f}, to truth {z[f'relax{t}_d2'].mean():.2f} ell; hit max iterations {np.sum(z[f'relax{t}_it'] >= 300)}/{len(dl)}")
    print(f"  continued L-BFGS (2000 it): dlnL {z['ext_dlnl'][:, -1].mean():+.2f} [{z['ext_dlnl'][:, -1].min():+.2f}, {z['ext_dlnl'][:, -1].max():+.2f}],"
          f" C {z['C_fit_lbfgs'].mean():.5f} -> {z['ext_C'][:, -1].mean():.5f} (lower in {np.sum(z['ext_C'][:, -1] < z['C_fit_lbfgs'])}/{len(g)})")
    for a in ("johnston", "fit", "fit_lbfgs"):
        print(f"  errloc {a:9s}: rms all {z[f'err_{a}_all'].mean():.2f}, lowest-decile {z[f'err_{a}_low'].mean():.2f} [{z[f'err_{a}_low'].min():.2f}, {z[f'err_{a}_low'].max():.2f}],"
              f" rest {z[f'err_{a}_rest'].mean():.2f} [{z[f'err_{a}_rest'].min():.2f}, {z[f'err_{a}_rest'].max():.2f}], waist {z[f'err_{a}_waist'].mean():.2f}, median {z[f'err_{a}_median'].mean():.2f} ell")

def relaxlong(path, CJ):
    """python -c 'import r39_summary as s; s.relaxlong(path, C_J)': converged midpoint relaxations; CJ = Johnston's mean C (Table III)."""
    z = np.load(path)
    rem = lambda c: 100 * (c.mean() - CJ) / (1 - CJ)
    print(f"  {len(z['seed'])} universes: relaxed midpoint lnL - fit [{z['dl_fit'].min():+.2f}, {z['dl_fit'].max():+.2f}] mean {z['dl_fit'].mean():+.2f};"
          f" - truth [{z['dl_truth'].min():+.2f}, {z['dl_truth'].max():+.2f}] mean {z['dl_truth'].mean():+.2f}; iterations {z['it'].min()}-{z['it'].max()}")
    print(f"  C fit {z['C_fit'].mean():.5f} ({rem(z['C_fit']):.1f} %), midpoint {z['C'].mean():.5f} ({rem(z['C']):.1f} %), truth {z['C_truth'].mean():.5f} ({rem(z['C_truth']):.1f} %);"
          f" C midpoint between the two in {np.sum((z['C'] > z['C_fit']) & (z['C'] < z['C_truth']))}/{len(z['C'])}; distance to fit {z['d1'].mean():.2f}, to truth {z['d2'].mean():.2f} ell")

if __name__ == "__main__":
    if sys.argv[1] == "relaxlong":
        relaxlong(sys.argv[2], float(sys.argv[3]))
    else:
        main(sys.argv[1])
