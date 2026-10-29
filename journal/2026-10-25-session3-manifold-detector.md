# Session 3 — 2026-10-25 (morning)

## What we did
- **Cluster:** Roberto's access to the cluster recorded in `compute.md` (not in the public copy: internal cluster configuration). SLURM;
  /home over NFS is the bottleneck. Rules: `low` for sweeps, node-local /tmp, one small output file per job.
- **S4a, distances from the order alone:** BK estimator quoted from the paper and re-derived in 1+1. Found the
  **rectangle identity** d² = 2V_A V_B/V_C for any c in the common past (1+1 only) `[ours]`. Flat sprinklings:
  2.5–5 % error, no bias above 2ℓ.
- **de Sitter:** the estimate drifts with the depth of c as 1 − Rτ²/16 `[ours]`. Confirmed by sprinkling against a flat
  control; R from counts is right on average (1.6 ± 0.4 vs 2.13) but noisy per pair.
- **Embedding:** Lorentzian MDS recovers flat positions to 0.4ℓ. The eigenvalue spectrum detects signature and
  dimension (a 2+1 control shows two space directions) ⇒ a **manifold detector**.
- **S4b:** the detector needs N ≳ 100–200. S3a continuum phase passes; crystal fails (extra space direction); S1 grown
  universes fail everything. Fast O(N²) S3a update. de Sitter stress grows only for Hτ ≳ 2.
- **S4c pilot:** quantum amplitudes by sampling random 2D orders (works while β ≲ 0.4 at N = 100). With record =
  stress quartile, classical e^{−βS} drains the most manifold-like quartile; quantum e^{iβS} shows no drift
  (β ≤ 0.3). Fluctuation-level result; needs larger runs and a better record.
- Roberto asked what ℓ and β are. Explained in plain terms: ℓ is the event spacing, β the strength of the
  action weighting, like 1/temperature.
- **Draft v3** written ("Is it spacetime?"), v2 archived, review written.
- Roadmap discussed: A1 quantum at N = 200 (cluster) → A2 layer-by-layer operator dynamics (ours) → B matter in
  2D (incl. matter frame = cosmic frame test) → C1 3+1 kinematics → C2 3+1 gravity (likely beyond us).
- **Literature review** on A2 and C8 (two delegated searches; 3 key abstracts re-checked by Claude). Pieces exist
  separately (Gudder's shells and isometric dynamics, Major–Rideout–Surya thick slices, quantum causal histories,
  Surya–Zalel complex growth; quantum graphity, Caravelli–Markopoulou, indefinite causal order). The combinations we
  want were not found. Quantum graphity stalled (fragments).
- **Decision:** A1 → A2 (transfer matrix on thick height layers vs whole-history sum, clock-swap test) → C8 as
  amplitudes on link choices inside A2 → matter → 3+1. Side idea: η_max ≈ the Caravelli–Markopoulou long-link
  suppression ⇒ possible prediction.

## Mistakes (now in LESSONS)
- "Corrected" the 40M–480M count to poset numbers without opening the code, which enumerates N! orders; reverted (11b).
- Poisson ratio bias (+11 % in the flat control) and a 2–4σ false signal from correlated bins (10b).
- β_c ≈ 35/N extrapolation failed at N = 400.

## Open / next
- **Next session: A1** — the cluster job for quantum sampling at N = 200 (10⁶ samples, record = layer count + stress).
- N = 400 crystallisation; the detector in 2+1 with the general BK estimator.
