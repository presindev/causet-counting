# Session 9 — 2026-10-27

A thinking session on the quantum-memory question that turned into three quick tests and a new idea (007). Draft v5 written at the end.

## What we discussed
- **Question zero** (is the 10²⁴⁴-event memory per patch the universe's or our clumsy description's?). Roberto: clumsy description; the universe must have a
  compression we haven't found, and it should look like microstate → macrostate as N → ∞.
- **Escapes** for an area law: (i) Lorentz-invariant truncation, dropped by Roberto; (ii) forget what's recorded; (iii) holographic redundancy.
  Correction (mine): (ii) does not imply (iii). Fixed-size coarse cells keep a volume law; an area law needs cells of size √(Lℓ) (CKN scale; numerology warning).
  → **Memory ladder:** events (spacetime volume) → geometry/Cauchy data (spatial volume) → area (needs gravity).
- **Idea 007 (Roberto):** links are undetermined *because* nothing stores them, so QM is the universe's memory saving. Sharpened: storing probabilities costs more,
  so the saving must come from *summing*. It needs one real history. Roberto picked Sorkin's quantum measure (one history, no threshold) over collapse with
  "different enough" (Penrose–Diósi: parameter-free version excluded at Gran Sasso). Record = an alternative that can never interfere again.
  Version: events exist first, links are determined later; events possibly undetermined too.

## What we computed (all laptop, seconds to minutes)
- **Rung 2** (`sims/r2_coarse_vs_micro.py`): shuffling events inside light-cone cells scrambles what a newborn feels. Raw operator: always (even at 0.5 ev/cell).
  Smeared (ε = 0.03): only fine at ≲ 2 ev/cell, worse with N (0.20 → 0.30 → 0.66). **Classical coarse-graining fails.**
- **Past/future matrix** (`sims/r3_memory_svd.py`): ΔS is path independent ⇒ phases are diagonal rescalings ⇒ they can't change memory when the outcome is the full
  universe. With a coarse record, phases *add* effective memory. Exact orthogonal sectors: never form (1 sector) with an open future.
- **Screen test** (`sims/r4_screen.py`): what the last newborn sees. Coarser screens keep more coherence (classical saving); phases *decohere* (make records),
  most at β ≈ 7–8 (the KR-suppression window). QM acts as a record-maker, not a memory-saver, at N ≤ 8.
- On paper: if events see their whole past, records ≈ everything → volume law. A saving needs events with partial views.

## Changes
- Idea 004: quantum-memory definition, ladder, rung-2 result. New idea 007 (seed). Draft v5 + review; v4 archived.

## Mistakes (now in LESSONS)
- Claimed (ii) ⇒ (iii) before counting (lesson 24).
- Built a quantum-vs-classical memory test before checking whether phases could matter at all (lesson 25).
- Said "the memory accounting is the same with or without picking"; it is the same only per branch (corrected in-session).

## Open / next
- Screen test with covariant stems and a fixed per-event view budget; count records per patch vs births (Roberto's "collapses per patch").
- Fetch cluster jobs 449800 (N = 400 tail) and 449812 (F_N at N = 11).
- Gravity / rung 3 discussion (deferred by Roberto).
