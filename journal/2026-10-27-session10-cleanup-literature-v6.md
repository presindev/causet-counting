# Session 10 — 2026-10-27

A housekeeping and honesty session, run as a self-paced loop: clean up, review the literature deeply, fetch the pending jobs, write v6 and review it against an arXiv bar.

## Roberto's choices (asked at the start)
- Bar for "publishable": a credible **arXiv gr-qc preprint**.
- v6 stays **one draft** with two parts; the review sketches the split.
- Fetch the cluster jobs now (he ran the ssh command).
- Discarded ideas go in **one `GRAVEYARD.md`**, plus `ROADMAP.md` for live, waiting and unexplored lines.

## Literature (three delegated searches; details in `literature.md`, session 10)
- **Given back** (they were in the literature):
  - MDS spectrum as a manifold test (Clough–Evans 2016);
  - wedge −2 and non-commuting limits (Boguñá–Krioukov 2025);
  - the age of the cosmos as the IR regulator (Sorkin 2007);
  - 10²⁴⁴ vs 10¹²² (Sorkin 2007, Λ ~ N^{−1/2});
  - the bilayer ground state (Cunningham–Surya);
  - the labelling weight (Surya's review);
  - the variance mechanism (implicit in Loomis–Carlip and Carlip–Carlip–Surya);
  - rung-2 failure in substance (Sorkin 2007).
- **Survived a deep search:**
  - the Laguerre application (0 of 99 citers of Johnston's papers, full text);
  - the F_N criterion (all QSG models impose a sum rule);
  - the general-c rectangle identity and depth-drift curvature (not among the BK citers);
  - the N = 400 hot/cold data;
  - Little's-law memory reading;
  - records via screens.
- **Useful new neighbours:** Gisin and Del Santo–Gisin; Halliwell (records cost storage); Sorkin's co-events; Dowker–Henson and Dowker–Herbauts (collapse on null lattices);
  Bousso–Susskind (decoherence never exact in a finite diamond); Banks HST (area per diamond); Yang–Binder–Narasimhachar–Gu (MPS memory).
- **Corrections:** Bousso's N-bound is hep-th/0010252; quant-ph/0401075 is "Simulating causal collapse models".

## Computed
- **cluster 449800** (N = 400 tail): all 11 tasks done on cn12 (3.6–7.4 h). Complete picture, same as v5. **But the cold chains' acceptance is ≤ 0.001**, so "never meet" is partly
  a frozen sampler. The literature fit gives β_c ≈ 1.66/(ε²N) = 0.094, inside our (0.05, 0.45).
- **cluster 449812** (F_N, N = 11): 47 min, 6.1 GB, 2.77 M states. q_N = r_N(β)/r_N(0):
  - in the window (β = 7) the 2-stem converges to ≈ 1.87∠π;
  - 3- and 4-stems are still moving;
  - at weak β the magnitudes converge but the phases drift ≈ 0.008π·β per relation in the stem per event (all 20 stems).

## Changes
- New `GRAVEYARD.md` (19 killed, 7 dropped, 9 claims given back, corrections) and `ROADMAP.md` (waiting computations, promising lines, 5 new ideas N1–N5, unexplored by us and by the literature).
- Ideas 001, 004, 005, 006 and 007 updated. `INDEX.md` rewritten as a short map. Draft v6 + `REVIEW-v6`; v5 archived.

## Mistakes (now in LESSONS)
- Three drafts carried "not found in a brief search" claims, one of which (the detector) was a 2016 paper with the same method (lesson 26).
- v5 called the N = 400 result hysteresis without looking at the cold chains' acceptance rate (lesson 27).

## Next
- Submit F_N at N = 12 (`compute.md`, session 10). Mean-field model of the phase drift (ROADMAP N1).
- Decide: write Part I as a methods note (3–4 sessions), or push Part II first.
- Parallel tempering at N = 400. Gravity / rung-3 discussion (deferred).

## Part 2 (after Roberto submitted job 449948, F_N at N = 12)
- **Drift model** (`sims/r5_drift_meanfield.py`): weak-β drift = β × mean future action change; matches the exact N = 11 data to 10 %. d_N ∝ N^{−a}: a ≈ 1 at ε = 0.21 (pre-asymptotic, N ≪ 23),
  a = 1.5–3.3 for ε = 0.35–0.7. Probably not fatal. **This corrects my guess ("I'd expect no")** made before the calculation. Prediction for N = 12: N·d ≈ 0.233.
- **Fixed-n curvature** (`sims/r6_curvature_fixed_n.py`): de Sitter diamonds raise the related-pair share by ≈ 0.027 (Hτ)²; the propagator is no more sensitive than c₂ ⇒ J₂ probe dropped (GRAVEYARD D8).
- v6 updated (Sec. 6 drift paragraph, Sec. 5 fixed-n sentence, Table 2 rows); review addendum.
