# Session 11 — Part I figures (2026-10-27)

**Asked:** "do the figures" (Part I of draft v6).

**Done**
- `sims/fig_part1.py` (matplotlib from a project `.venv`, gitignored): four figures into `paper/figs/` and draft v6 —
  distance estimator vs truth, depth drift vs the continuum, detector calibration (vs N / N = 400 universes / de Sitter), propagator vs ½L_n(μ/2).
- **Found while plotting:** the embedding detector is ambiguous on the ~10-layer N = 400 Monte Carlo states (stress 0.06–0.31; the verdict flips with
  the sample size). Probably because the sample takes the largest pasts = the top layers. Stated in the draft; fix (depth-spread sample) on the roadmap. Idea 005.
- Depth drift: seeds 1–100 looked ~2σ high in four bins; bins are 0.87 correlated and 300 fresh seeds gave 0.000 ± 0.003. Claim stands (lesson 29).
  Figure uses 400 seeds; shallowest bin is biased low in both geometries (near-empty tiles), stated in the caption.

**Detector fix (Roberto: "do the fix")**
- Depth-spread sample alone: stress noisier, does not separate; $r_+$ separates but its thresholds are unstable.
- Real second failure: layered orders give mostly zero-length pairs; MDS fits an all-zero matrix perfectly (bilayer: stress 0.00).
- Adopted the share of zero-length pairs as a layering flag: N = 400 flat/continuum ≤ 0.103 vs layered ≥ 0.55; curvature does not move it. Held-out fresh N = 200 chains:
  all classified correctly. A cousin of Glaser–Surya interval abundances (said so in the draft). Figure 3(b) now shows it. Lesson 30.

**Writing (Roberto: "do the writing")**
- Part I rewritten as a standalone methods note: `paper/counting-1p1-v1.tex` (10 pp., 5 figures, no tags), review `paper/REVIEW-counting-1p1-v1-2026-10-27.md` (~80 %).
- New while writing: closed form of the de Sitter depth drift, $\tanh^2(H\tau/2)/[2\ln\cosh(H\tau/2)]$, checked to $10^{-5}$ (idea 005).
- Checked: grown universes at N = 200 fail on stress (0.64–0.78), not on zero share; journal refs verified where arXiv has them (BHS08), others kept as in v6.

**Reruns + FRW (Roberto: "rerun old numbers and do the check")**
- All old Part I numbers rerun with fixed seeds and reproduced; session-3 curvature fit reimplemented (exact match). Deepest-c distance now uses $N_C+1$.
- FRW $a=\eta^p$: drift leading term = $R$ locally (three cases, right sign); sprinkled $p=1$ follows continuum; count-only fit = depth-weighted $R$.
- Propagator flags ~10-layer states (rms 0.07–0.10 vs 0.012–0.020).
- 3+1 assessed (ROADMAP §4): propagator target easiest; distance doable without the product form; curvature drift hard.

**3+1 propagator target (Roberto: "let's try 1")**
- 3+1 hops are along links ⇒ no closed form (emptiness factors). $E[P_2|n]\to3\pi$ (hand calculation), reproducing the continuum mass term $m^2/8\pi$; MC confirms with $O(n^{-1/2})$ approach.
- My earlier assessment was wrong (lesson 31). Note's outlook corrected; not added as a result.

**3+1 distance + embedding (Roberto: "let's try 2+4")**
- Overlap-volume inversion for any $c$ (tabulated lens volume); with the first event as reference, distances from three past sizes. 1–2 % at large N; embedding counts dimension; KR fails.
- Prior art Johnston 2025 (same reference idea; triangle-inequality distances). Head-to-head: ours better per pair, worse after embedding (heavy tails). Robust embedding next.

**Johnston reproduction + embedding (Roberto: "the objective is a paper")**
- Johnston 2025 reproduced (Tables III, V exactly, with strictly-between counts; Table IV not). Oracle: his spacelike pairs are the whole bottleneck.
- Our estimator: three bugs fixed (table range, normalization, zero overlap). Per pair better at short/medium range; embedding still below his on his benchmark.
- Lessons 32–33. Next decision for Roberto: likelihood embedding (several sessions) vs ship the 1+1 note.

**Mixed method + timing (Roberto: "do 1 and 2")**
- Switch (ours if our estimate says close, $L=0.25$; his detour otherwise) beats Johnston at n = 500–3000, held out on fresh seeds: +0.021/+0.015/+0.012/+0.007 spatial corr.
- Chaining our estimates as detour legs: much worse (bias compounds). Timing: his min-plus 76 s vs our step 3.3 s at n = 4000; the switch keeps his cost.
- Lesson 34. Next: cluster run at larger n; cheaper far-pair estimate; Boguñá email now has a concrete positive result.

**cluster + cheaper far pairs (Roberto: "prepare 1", "try (a) and (b)")**
- r14 submitted on the cluster: test 450016, then 450017–450020 (n = 3000, 6000, 10000, 15000): Johnston vs ours vs ours capped vs switch, with timing.
- (a) random stepping stones: killed. (b) two passes: about half the gain kept, far step 3× faster at n = 3000, 17–28 % still fall back. (c) local maps + stitching: next.
- Roberto's seed: distance as a large-N quantity like temperature (idea 005).
- (b) polished: 27-cell widening, fallbacks ~1 %, keeps ~2/3 of the switch gain at 3000.
- cluster n = 3000, 6000 back: switch +0.0049 at 6000 = 20 % of his residual error (relative gain grows with n); pure ours not overtaking; his min-plus 898 s vs our 65 s.
- (c) counts-only fit (SMACOF on related + shared-past distances, far pairs at weight 0.1, no detours): held out, on par with/edging Johnston (+0.004 ± 0.002 at 3000).

**State at wrap-up (23:30)**
- 3+1 embedding story for the paper: Johnston reproduced; oracle (spacelike pairs are his bottleneck); switch beats him (held out; 20 % of his residual at n = 6000);
  counts-only map (c) matches/edges him without detours (held out at n ≤ 3000); cheap two-pass far pairs (b); timing (his ~$n^{3.2}$, ours ~$n^{2.2}$). Lessons 34–36.
- Running on the cluster: r14 n = 10000 (450019), 15000 (450020); r17 (c) test 450031, then 450032–450035 (n = 3000–15000, paired with r14 universes).

**Waiting:** job 449963 (F_N, N = 12).

**Next:** fetch r14 + r17 + F_N N = 12 (one command, compute.md / idea 005); large-N verdict for switch and (c); Boguñá email (Roberto, next session); decide how the 3+1 results enter the paper (Part I note becomes a regular paper, or a separate 3+1 note).
