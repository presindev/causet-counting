# Lessons learnt

Mistakes made in this notebook and the rule that prevents each one. Claude reads this at the start of every session.

## Physics and claims
1. **Don't stretch an analogy past what was calculated.** (Session 1: I said the quantum chain "produces blur by
   coupling, like an atomic linewidth". In fact an isolated point is infinitely blurry, and coupling *reduces* blur.)
   → State exactly what a toy model computes, then separately what it suggests. Check the opposite limit
   (no coupling, zero size, infinite size) before claiming a mechanism.
2. **Check the dimension-specific basics first.** (I proposed testing "Newton and Einstein" in 1+1 before noting
   that 1+1 GR is empty and 2+1 has no Newtonian attraction.) → Before building a toy in d dimensions, list what
   physics exists in d dimensions and what doesn't.
3. **Quantum sums need a record.** (My first exact quantum sum treated every universe as its own outcome, so
   the phases did nothing.) → Before computing |amplitude|², say which histories end in the *same* outcome and
   therefore interfere.
4. **Check that a toy produces the object before measuring properties of it.** (S2 planned to compare curvature
   with GR before checking whether the grown universes were even 2D.) → Check dimension and manifold-likeness
   first, then curvature.
5. **Name hidden assumptions that break our own constraints.** (The p = c/n growth rule used birth order as a
   clock, which violates C2. I flagged it, but only after showing the result.) → Check every rule against C1–C8
   *before* running it.
6. **Keep "background", "preferred frame" and "absolute time" distinct.** Roberto had to separate them.
   → Fixed background (forbidden) ≠ dynamical frame field ≠ frame of the state ≠ a clock computed from
   relations. Say which one is meant.
7. **Numerology isn't evidence.** Any combination of L and ℓ_P is a power of 10⁶¹. Say so whenever a big number
   "matches".

## Statistics and numerics
8. **Correlated samples underestimate errors.** (S2 de Sitter: quoted errors were too small because events share
   pasts.) → Quote run-to-run spread across independent seeds, not per-event standard errors.
9. **Avoid selection bias when picking the "central" event.** (Choosing the most central sprinkled point biased
   the link count.) → Insert test events by hand.
10. **Validate on a known answer first** (flat → 0, de Sitter → 2H²) before applying a tool to unknown universes.
    This worked well; keep doing it.
10b. **Ratios of counts are biased.** (S4a: dividing by a Poisson count N_C gave +11 % in the flat control, and the
    median of ratios added more.) → For independent Poisson counts use N_A·N_B/(N_C+1) and take means. Bins from
    one sprinkling move together: confirm any "2–4 σ" offset with fresh seeds before interpreting it.

18. **Infinite sums that only converge conditionally depend on the cut-off; use the physical one.** (Session 4 cut the past with a rapidity
    wedge and "found" an abrupt −1/ℓ² for long waves; a finite past region gives 0.) → When kernel weights cancel (1 − 2 + 1) over an infinite
    region, try two regulators. Ours is a finite past (C3), not a cap on one variable.

19. **Measure a truncation by the spread it causes, not by the share it drops.** (Session 5: signed shares of Σf cancel, and a constant shift drops
    out of record probabilities.) → Quote sd(S − S_trunc)/σ_S.
20. **Check that a first result isn't the shape of the box.** (Session 5: the diamond's corners made the thick present look ∝ N; the cylinder control
    showed the real rule.) → Before interpreting a size or memory result, rerun it in a second geometry (closed space, different frame).

24. **Count before claiming that one mechanism implies another.** (Session 9: I said "forgetting what's recorded" (ii) produces holography (iii); one line of
    cell counting showed it keeps a volume law.) → Do the scaling arithmetic first.
25. **Before a quantum-vs-classical test, check whether the phases can matter at all.** (Session 9: with an endpoint-only action, phases are diagonal rescalings
    of the past/future matrix and change no memory measure; the first run was wasted.) → Write the amplitude as a function of (start, end, path) first.

21. **Before proposing a measure, check it against what we already know.** (Session 6: I proposed "memory shared with the outside" as the area-law piece;
    session 5 had already shown that outside events need old events forever, so it was 100 %.) → Run the known limit in my head (or a 1-minute check) first.

## Literature
11. **Verify citations; never guess identifiers.** (I wrote a guessed arXiv id and had to remove it.) → Unchecked
    items are marked `(unverified)` and carry no invented numbers.
11b. **Check what the code counts before "correcting" a number.** (Session 3: I "fixed" 40M–480M universes to
    poset counts from OEIS; the code enumerates N! permutations, so the original was right.) → Open the code first.
12. **Search before claiming novelty, and say how deep the search was.** "Not found in a brief search" ≠ "new".
16. **Read the setup of a paper before saying it connects to ours.** (Caravelli–Markopoulou was noted as "directly relevant to η_max"
    from its abstract; in fact it uses spatial links with an external time and gives a running mass.) → Mark abstract-only links as such.

## Working process
13. **Drafts tell one story.** (Draft v0 was a chronological soup.) → Keep only what advanced the thinking; dead
    ends go to a short appendix.
14. **Never pipe a command that waits on stdin** (`cat > file` with no input stalled a run for 10 minutes).
    Use heredocs or the Write tool, and keep laptop runs short (the cluster exists for big jobs).
15. **Tell Roberto when something is wrong as soon as I notice it,** including my own earlier claims, and record
    the correction in the idea file.
17. **Learn the cluster's environment before writing jobs.** (Session 4: assumed numpy on the nodes and Python on the login node; neither
    holds.) → Check the facts in `compute.md` first; anything new runs as a tiny `sbatch` probe, and every job writes to node-local /tmp.
22. **Size cluster jobs for the slowest loaded node, and checkpoint.** (Session 7: N = 400 was timed on a quiet node, got 6 h, ran up to 2× slower
    under load; 20 of 38 tasks died and lost everything because results were saved only at the end.) → `--time` ≥ 2× the quiet-node estimate,
    and any task over ~1 h writes a partial result to the output folder periodically.
23. **Ship a script's whole import tree, and time each code on the cluster.** (Session 8: the F_N test died because `a2_growth_paths.py`, imported only by the
    validation step, was never copied; I sized the job with A1's 4× slowdown, but this pure-Python recursion ran up to ~60× slower, startup included.)
    → Copy all of `sims/*.py` (or grep the imports), run the short test before every new code, size `--time` from that test, and use `python3 -u` so logs show progress.

26. **A "brief search" claim expires; crawl citations before a claim goes into a draft as ours.** (Session 10: the manifold detector was "not found in a brief search" for three
    drafts; Clough–Evans 2016 had the method. Sorkin 2007 had both the IR regulator and the 10²⁴⁰ count.) → Before an item enters a draft's "our additions", pull the INSPIRE
    citation list of the closest paper and grep the citers' full texts. Keep a "what is ours" table with the search depth per claim.
27. **Check the sampler before calling it physics.** (Session 10: v5 reported N = 400 "hysteresis"; the cold chains' acceptance was ≤ 0.001, i.e. frozen.) → Report acceptance
    rates next to any metastability or hysteresis claim; a frozen chain proves nothing about the free energy.
28. **A test at smaller N doesn't exercise the limits of a bigger N.** (Session 10: F_N at N = 12 died in 40 s on a lookup table sized for N ≤ 11; the N = 9 test passed.)
    → Before scaling a run up, grep the code for hard-coded sizes (`1 << k`, fixed lists, dtype ranges) and smoke-test the single largest step on the laptop.
29. **Correlated bins make one fluctuation look like a pattern.** (Session 11: four depth bins in a row 2σ above the continuum; the bins were 0.87 correlated and 300 fresh
    seeds gave 0.000 ± 0.003.) → Before rewriting a claim on a run of deviations, check the correlation between bins and rerun with fresh seeds.
30. **A perfect fit can mean there was nothing to fit.** (Session 11: a bilayer gives an all-zero interval matrix and MDS stress 0.00.) → Next to any goodness-of-fit, report how much
    signal went in (here the share of zero-length pairs). And set thresholds in a gap or from quantiles of a large calibration, not from the max of a small one (it moved 30 % between draws).
31. **Read our own idea file before assessing an extension.** (Session 11: I rated the 3+1 propagator target "easy, via chain abundances"; idea 006 already said 3+1 hops go
    along links, which removes the closed form.) → Before estimating how doable a generalization is, reread the dimension-specific details of the construction.
32. **A lookup table must cover the use case, not the first test.** (Session 11: the 3+1 lens table covered δ ≤ 3 because the late-event test never needed more; whole-interval
    pairs went to δ ≈ 14 and were silently clipped.) → Make out-of-range inputs loud (count and print them), and size tables from the distribution of the actual inputs.
33. **Compare like with like.** (Session 11: "ours 2–3× better per pair" compared our error on the Minkowski distance with his on the spatial distance; on the same quantity
    it was 15–25 %.) → Before claiming a method beats another, put both on the same quantity, the same pairs and the same universes.
34. **Try the dumbest combination first.** (Session 11: after many principled patches failed, Roberto's "use each method where it is good" as a plain switch beat Johnston;
    the clever version, routing through our short estimates, compounded our bias and lost badly.) → When two methods have complementary error profiles, test a hard switch
    on the error-profile variable before blending, averaging or chaining; and hold out the switch point.
35. **Down-weight weak information instead of dropping it.** (Session 11: fitting the 3+1 map to trusted distances only lost to Johnston; keeping our far-pair estimates
    at weight 0.1 beat him, held out.) → When some measurements are noisy, first try a small weight before excluding them; noisy-but-unbiased data still pins the shape.
36. **Never mix other output into a binary stream.** (Session 11: `sacct` printed into the same ssh stdout as `tar czf -`, and the local tar failed.) → In fetch commands,
    write tables to a file and pack it (the compute.md recipe already said so: reread the recipe before improvising, cf. lesson 31).
37. **Ablate a multi-term method before saying which term carries the gain.** (Session 12: I presented the "likelihood embedding" as resting on our new binomial overlap
    term; the ablation showed the related-pair Poisson term alone — already in Casasola 2026 — does better, and our term hurts.) → For every composite method, run each
    term alone and all together on the same universes before writing the claim; pair it with the literature search (lesson 26).

38. **Quote a paper before saying what it does not do.** (Session 13: v2 said Boguñá–Krioukov had only a "small-d, equal-time approximation"; their Eq. 22 is exact and
    used numerically in M³/M⁴. Our literature note from session 2 had kept only the asymptotic formula, and the draft inherited it.) → Every "X does not / only does Y" in a
    draft needs a checked quote or section number from X's full text; reread it at each draft, not from our own notes.
39. **Check what the draft already promises before offering choices about it.** (Session 14: I offered "sims/ only" for the code release; the paper's Availability paragraph
    already promised "the code and the full notebook", and Roberto had to remember it.) → Before asking Roberto to decide anything about a paper's release, data or wording,
    grep the draft for the matching promise (availability, code, data, AI statement) and show it next to the question.
