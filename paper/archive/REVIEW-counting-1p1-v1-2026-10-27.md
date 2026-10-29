# Honest review: counting-1p1-v1 (Part I as a standalone methods note, 10 pp., 2026-10-27, session 11)

Bar: a credible arXiv gr-qc preprint (agreed session 10). Source: `paper/counting-1p1-v1.tex`; the notebook version stays in `draft-v6.tex`.

## What it is
Four small $1+1$ counting tools, each tested on sprinklings: the general-$c$ rectangle identity with a Poisson-unbiased estimator; depth-drift curvature with a
**new closed form** in de Sitter, $d^2_{\rm est}/d^2=\tanh^2(H\tau/2)/[2\ln\cosh(H\tau/2)]$ (derived and checked this session); the calibrated embedding test with
the zero-share fix; the density-free Laguerre target for Johnston's propagator. No tags, no session language, five figures, a "what is new and what we checked" paragraph.

## Strengths
- Every claim has a test against a known continuum, and the negative results are stated (fixed-$n$ curvature reduces to chain abundances; the detector's blind spot).
- Prior art is credited where it lives: BK24 (regions), Clough–Evans (embedding), Glaser–Surya (interval abundances), combinatorics (Laguerre).
- The closed form makes Sec. 4 a real derivation instead of a quoted expansion.

## Weaknesses a moderator or referee would see
1. **Modest.** Four small tools in $1+1$. Fine for arXiv; a journal (CQG, PRD) would ask for $d>2$ or a sharper application. Say so in the cover letter, not hide it.
2. **Novelty of the rectangle identity is unconfirmed.** It is elementary. Ask Boguñá before submitting (he is also the natural endorser).
3. **Some numbers were not rerun for this draft:** the distance table (session 3), the curvature-fit table (session 3), the MDS recovery numbers (session 3), the classical-growth numbers at
   N = 100 and N = 1500, and the propagator rms values (session 8). The scripts exist; rerun them once with fixed seeds and record the commands before submission.
4. **Monte Carlo states as test inputs.** The N = 400 states come from chains that are partly frozen; the paper says they are test inputs, which is the honest framing,
   but a referee may still ask for equilibrium samples (parallel tempering, roadmap).
5. **Detector thresholds are empirical** ($1.5\times$ flat median). Tested on one held-out size (N = 200). One more size (N = 800, cluster) would make it solid.
6. **Curvature estimator only on de Sitter.** A second geometry (e.g. a 2D FRW patch, already sprinkled in `a2_thick_present_frw.py`) would answer "is the leading term really $-R\tau^2/16$ in general?".
7. **Code and data:** URL missing; the N = 400 final states (small npz files) should be released with the code.

## Practical blockers (Roberto)
- Author line and affiliation; wording of the AI-use statement (arXiv: AI cannot be an author; use must be disclosed).
- Endorser in gr-qc. Email to Boguñá: novelty of the identity + endorsement.
- Decide whether the repository goes public (or a cleaned copy of `sims/`).

## Distance to the bar
**About one session of work plus Roberto's items.** Rerun the old numbers with fixed seeds (S), add an FRW drift check (S), N = 800 detector check (cluster, M),
release code. Then it is a credible arXiv methods note. Estimate: 80 % of the way.

## Addendum (same session: reruns and FRW)
- Weakness 3 closed: every old number was rerun with fixed seeds and reproduced (distance table, curvature-fit table, embedding recovery, detector at N = 100, propagator rms,
  p = 0.02 runaway). Outputs in `sims/out/rerun/` and `sims/out/r9_*.txt`. One reference value was input-dependent ("continuum fit 2.13" → 1.9–2.2), now stated.
- Weakness 6 closed: FRW ($a=\eta^p$, three cases) confirms that the leading term is $-R\tau^2/16$ locally; the sprinkled $p=1$ case follows the continuum. New caveat stated:
  the count-only fit returns a depth-weighted average of $R$.
- New supporting result: the propagator flags the ~10-layer states (rms 5× the continuum).
- Remaining: N = 800 detector check (cluster), code/data release, Roberto's items. Estimate: ~85–90 %.

