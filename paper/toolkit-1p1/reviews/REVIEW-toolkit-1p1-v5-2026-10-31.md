# Honest review — toolkit-1p1-v5 (2026-10-31, session 20)

**What changed:** referee round 4 (minor; accept once 25–29 are made), comments 25–29 (see `answers/answer-toolkit-1p1-v5.md`), and the missing Mecke citation (Last & Penrose 2017).

**Assessment.**
- **Abstract (25).** It now says what Table III and the Mecke argument support: the ratio of coefficients summed over the pairs of many sprinklings. The old "on average over sprinklings" read as the per-region mean, which is biased (1.67 vs 2.10).
- **Fig. 3 (26).** The figure was made with the stricter rectangle-to-join cut (`s4a_desitter.py:69–72`), and the text now says so. This is a recurrence of lesson 50: after the window rule changed in v4, an older test that used the previous rule was not audited.
- **Flat control (27a).** Checked by computation: the τ² lever arm is ≈3.9× longer in flat space. The "×3 vs slightly" contrast between geometries is mostly lever arm. The paper now says so; the within-geometry comparisons stand.
- **N = 800 test (28).** It is now reported completely.
  - The full embedding test rejects 4/20 continuum-like states at N = 800. The z false positive has stress 0.134, so it would be rejected anyway.
  - Height context: 27 layers against a flat mean of 52.
  - The abstract claim "lets the test reject layered orders on its own" stays. It is true for sensitivity; specificity at N = 800 is weaker, and Limitations now says so plainly.
- **Submission blockers:**
  - the repository must be public before upload (present tense);
  - the Zenodo DOI placeholder remains; the editor will make it a condition of acceptance.
- **Remaining weaknesses,** unchanged:
  - the curvature estimator is not competitive with the ordering fraction for one region;
  - the locality test (comment 24) was not run.
