# Session 19 — 2026-10-31 — external referee round 3

**What happened.** Round-3 reports: both minor revision, no re-review needed if comments are handled as described. Answered 3+1 comments 15–18 and 1+1
comments 18–24; v4 PDFs, latexdiff against v3, answers delivered to `~/Desktop/papers/{3+1 PRD,1+1 CQG}/`. 1+1 PRD track left frozen.

**3+1 (embedding-3p1-v4).**
- 15: route (b), directional claims deleted ("global maximum near the more accurate map", "slope points toward", Outlook "ideal optimizer would move toward");
  sign counts kept as a non-result with n = 1000 (4/10, rechecked from r35 npz).
- 16: relaxations from s = 0.25, 0.5, 0.75 rerun to convergence (`sims/r39_3p1_round2.py relaxlong_s`; v3's 0.25/0.75 were capped at 300 it):
  78/86/92 % and 83/89/93 %, monotone in s, within O(1) of both ends; relaxed midpoint 0.15ℓ / 0.11ℓ from the straight midpoint. Triangle-inequality wording;
  "no barrier was found". Summary `sims/out/r39_relax_s_round3.txt`.
- 17: near-cone share trend ~n^-0.3 (0.64 … 0.27); recommended variant used the 400-iteration Adam schedule (r35 line 147), so the cost estimate stands.
- 18: data availability and the methodology-note reference worded as commitments; "of this version" removed.
- Answer-only: 7511 s = min-plus step, 7691 s = whole pipeline (r28_timing); manuscript was right.

**1+1 (toolkit-1p1-v4).**
- 18: abstract matched to Sec. IV (average over sprinklings; less precise than the ordering fraction, ~3× in dS; biased low within one region; within 1.7σ).
- 19: Mecke condition stated; count-defined example removed. The one-region P pairs had been drawn sequentially (a single-uniform-draw selection) →
  `sims/r41_curvature_round3.py` reruns with a position-based thinning: same in-region bias; pooled over sprinklings it disappears → ratio bias of one region.
- 20: "Eq. (12) falls short by 26–35 %" in Sec. IV and Limitations; abstract "to leading order in the depth".
- 21: convexity argument via I(c,a) ∪ I(c,b), f dropped; convexity stated as an assumption; Table III caption.
- 22: flat control at matched element count: ordering fraction slightly more precise (0.80 vs 0.89; 0.50 vs 0.54). "Spreads are equal" gone.
- 23: commitments; r27 not fetched (needs Roberto's cluster login); DOI at submission.
- 24 (optional): not run; Discussion paragraph "What the curvature result is" (analytic and conceptual; Palm-type selection bias as a general point).

**Lessons.** 50 (audit every test for a bias mechanism once found), 51 (an inequality on an average says nothing about each term).

**Next.** Roberto: fetch r27 (command in INDEX "Next time"), then fill Sec. VI; make the repo public and mint the Zenodo DOI at submission.
Optional: the locality test (1+1 comment 24).

**r27 (later in the session).** Roberto fetched job 450475 (`sims/out/r27_n800_heldout.txt`). Held-out N = 800 test of the null-pair flag, threshold
and classes fixed on 29 Oct before the run: 8/8 layered states (14–19 layers) flagged, one of them inside the flat stress band (z rescues it);
19/20 continuum-like states (27–56 layers) not flagged; one false positive, 27 layers at β = 0.3, z = 0.123 against 0.120 (acceptance 5 % vs 53–54 % for
its sibling chains: probably partly layered, but counted as a false positive by the pre-set classes). Three continuum-like states have stress just above
the N = 800 flat band. Filled into 1+1 v4 Sec. VI and Limitations; v4 PDF, diff and answer redelivered. Only the Zenodo DOI remains a placeholder.
- Wrap-up: Last & Penrose (2017) verified and recorded in literature.md as the missing citation for the Mecke formula in the 1+1 paper (to add in the final version); round-4 referee prompt handed to Roberto.
