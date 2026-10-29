# Session 5 — 2026-10-25 (afternoon)

## What we did
- **Null-wave puzzle (idea 001), resolved.** Sorkin's averaged 1+1 □ is only conditionally convergent: the kernel integrates to 0 per unit rapidity
  over infinitely many units. With a rapidity wedge (session 4) a constant gives −2, an exact null wave −1, and waves longer than L jump to ≈ −1.
  With a finite past diamond (the physical C3 regulator) all three give the right answer (0, 0, 4pq); each null edge of the past supplies ¼
  (digamma check). Aslanbeigi–Saravani–Sorkin 2014 (read §2–3 in full) define the eigenvalue by continuation from absolutely convergent momenta,
  and their g(Z) → 0 at null momentum. **Correction:** session 4's "abrupt −1/ℓ² once λ > L" was a regulator artefact. The cutoff is simply invisible
  in 1+1. `sims/side_nullwave_diamond.py`. New lesson 18.
- **N = 400 crystallisation (idea 002/005), launched on the cluster.** Hot vs cold starts to separate slow equilibration from a shifted transition
  (`sims/n400_crystal.py`, `sims/cluster/n400_job.sh`, `sims/n400_analyse.py`; built by a background helper). Laptop surprise: the two-layer order
  (S/N ≈ −34) is far deeper than the S3a crystal (≈ −6); hot and cold stay apart from β ≈ 0.04 to 1. First test stalled on cn04 (CPU ≈ 10 %).
  Second test on cn05: 0.75–0.89 s/sweep. Full run = job 449411, 80 tasks × 15k sweeps, 12 at a time (Roberto runs other jobs), ~25 h.
- **Draft v4** (v3 archived): cutoff subsection, A1 at N = 200 (variance effect), N = 400 note, and a new Section 5 on A2. Review file written.
- **A2 (idea 004).**
  - Thick height layers fail: 61 % of links skip a layer (N = 200), and the needed memory grows to ~40 % of the age (m ≈ 9 / 10 / 14+ at
    N = 100 / 200 / 400). Truncated exact sums (N ≤ 9) and the clock swap (height vs volume) both fail at the truncation level.
  - Roberto's growth rule (never create an event in the past of an existing one) = Rideout–Sorkin internal temporality. Dates never change, no
    universe is lost, and e^{iβS} doesn't care about birth order.
  - ΔS per birth needs only past events with few events between: n_cut = 10 gives ≈ 0.06 σ_S at every N, clock-free. That's ~ln N events
    per birth, but spread over the whole age.
  - The thick present (events some later birth still needs): ∝ N in a diamond; ≈ 0.5 W², age-independent on a static circle; ≈ W/2 of conformal
    time in decelerating FRW; never retires in accelerating FRW. **Finite memory iff no event horizon.** Option 2 as a finite-state film is killed
    for realistic (accelerating) cosmologies; the cheap clock-free per-birth step survives.
  - Roberto: if the universe is a computing machine it must be efficient, so either something manages that memory or we're on the wrong path.
    Recorded as an open question (cf. Lloyd 2002; holographic bounds).

## Mistakes (now in LESSONS)
- Session 4's regulator: a rapidity wedge instead of a finite past produced a spurious physical claim (18).
- I first framed the thick-layer test as "share of Σf under 1 %"; the right measure is the spread of S − S_m in units of σ_S (shares cancel).
- The diamond's corners inflated the first thick-present result. The cylinder control was needed before interpreting it (lesson 1, check the geometry).

## Open / next
- Analyse N = 400 (job 449411) with `sims/n400_analyse.py`: where is β_c, and is the two-layer order the true crystal?
- A2 → quantum growth with the whole past as state and the clock-free step: amplitudes on each newborn's choice of past (C8) *and* the counting measure.
- Memory efficiency: how much information does the thick present carry? Compare with an area (holographic) bound instead of counting events.
- Literature check for the thick-present / event-horizon criterion (quantum sequential growth, de Sitter causal sets).
