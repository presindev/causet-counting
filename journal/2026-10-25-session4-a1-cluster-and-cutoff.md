# Session 4 — 2026-10-25 (midday)

## What we did
- **cluster set-up, step by step (Roberto ran the commands):** node /tmp is a local 7 TB disk and /scratchnvme is mounted. Nodes have
  Python 3.6.8 with no numpy and (apparently) no internet, and there's no Python on the login node. Building a venv on /home hung twice
  (slow NFS), so each job now unzips a numpy 1.19.5 wheel into /tmp. Several jobs stalled or hit NODE_FAIL (cn04, cn05) because of a
  slow /home. The first good job ran on cn12. All recorded in `compute.md`. Scripts: `sims/a1_sample.py`, `sims/cluster/a1_job.sh`.
- **A1 (idea 005):** 10⁶ uniform 2D orders at N = 200 (50 seeds × 2·10⁴, ~11 CPU-h, two waves of 25). Analysis in `sims/a1_analyse.py`,
  jackknife over seeds. Usable up to β ≈ 0.2. Results:
  - The 1,600-sample laptop hint (manifold-like Q1 → 0.42) was noise. Real value: 0.261 ± 0.003.
  - Layer-count record: classical runs toward few-layer (crystal-like) universes. Quantum suppresses them (0.061 → 0.045 ± 0.003 at
    β = 0.2), consistent with our exact sums at N ≤ 9 and with Loomis–Carlip.
  - Mechanism: $P_q(r)\propto n_r^2 e^{-\beta^2\sigma_r^2}$ reproduces everything. It's a variance effect, not structured interference.
    **A1 is closed**: this method is exhausted at β ≈ 0.2.
- **Side calculation (idea 001):** read Caravelli–Markopoulou in full. It's a spatial lattice with external time that gives a running mass,
  so it isn't the same object as our η_max (corrected in `literature.md`). Derived Sorkin's 2D □ on plane waves with a rapidity cutoff
  (`sims/side_cutoff_dalembertian.py`, validated: 4pq, boost-invariant to 6 digits). **The cutoff is invisible** until a light-cone wavelength
  exceeds L, then it fails abruptly (−1/ℓ²). For massive particles that needs E > m²L/4 ≥ 10³⁰ eV. The "possible prediction" is killed in 1+1.
- Bubbles of space (003): Roberto deferred them to the matter step (B).

## Mistakes (now in LESSONS)
- Session 3's note called C–M "directly relevant to η_max" from the abstract alone; it wasn't (16).
- During the session I first said η_max "drops out completely" of □ and guessed a "10⁴⁰" gap. The calculation gave "drops out until λ > L" and 10³⁰.
- Gave cluster instructions before knowing the cluster's Python, and assumed python3 could run on the login node (17).

## Open / next
- **A2:** transfer matrix on thick height layers, exact at small N. First check: reproduce the S3-quantum sums.
- Loose thread: an exact null plane wave gets −1/ℓ² with no cutoff. Read Aslanbeigi–Saravani–Sorkin 2014; think about 3+1 (k⊥ as mass?).
