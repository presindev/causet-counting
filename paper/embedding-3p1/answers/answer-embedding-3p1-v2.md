# Answer to the referee: embedding-3p1, round 1 (PRD)

**Manuscript:** "Spatial embedding of 3+1 causal sets: low-count spacelike pairs and a likelihood fit to interval counts" (R. Bada).
**This answer** responds to `review-embedding-3p1-v1.md` and comes with `embedding-3p1-v2.pdf` (no latexdiff PDF this round; see "Other changes").

We thank the referee for a careful report. Every point is answered below in the referee's order. Three of the requested checks changed the paper's claims, not only its numbers:

- **The removed fraction is lower at small n.** With ten universes per size up to n = 6000 the fit removes 72 % and 74 % of Johnston's residual at n = 1000 and 3000, and 80 % at n = 6000. v1 claimed 79–83 % at every size.
- **Using all related pairs is no longer claimed as a contribution.** The Casasola ablation shows the near-cone pairs are enough.
- **The optimizer check reversed our explanation of the residual.** It is not a local optimum, as v1 said; it is a flat direction of the likelihood.

All new runs are in `sims/r35_referee1_3p1.py` (one universe per call, every arm on the same universe). Their analysis is `sims/r35_analyse.py`.

---

## Major comments

### Major 1: why it matters physically

> The paper shows that accuracy improves, for example C from 0.9886 to 0.9980, but does not say what a better flat-space embedding makes possible. […] the introduction and discussion should answer this directly.

**Response.** Agreed. A new paragraph in the Introduction (second paragraph after the list of earlier constructions) gives three reasons:

1. Coordinates are the input of most further geometric constructions on a causal set:
   - spatial distances on hypersurfaces (Eichhorn–Surya–Versteegen);
   - local charts from which curvature is reconstructed (Madsen);
   - comparing discrete fields with their continuum counterparts at the positions of elements.
2. Embedding tests of manifoldlikeness can only reject a causal set when the embedding error on a genuine sprinkling is small. A less noisy embedding is therefore a sharper test.
3. Locating the residual tells us which information the order carries poorly: spacelike pairs with few shared elements. These are the same pairs whose distances Eichhorn–Surya–Versteegen find overestimated ("discrete asymptotic silence").

We also say explicitly that the paper does not demonstrate a downstream application. Its claims concern accuracy on the benchmark and the source of the error. We prefer to state this limit rather than overclaim.

**Change:** Introduction, new paragraph "Why the accuracy of a flat embedding matters…". Outlook, first sentences.

### Major 2: statistics

> At n = 3000 there are 2 universes and at n = 1000 only 1 […] I would ask for at least 10 universes per size up to 6000, and for the spread of the removed fraction across universes, not only its mean.

**Response.** Done. The large-n set now has ten universes at each of n = 1000, 3000 and 6000. These are seeds 1001–1010, which include the v1 universes; v1's numbers are reproduced on them: Johnston's C and the starting map exactly, the fit within 2×10⁻⁴. The larger sizes keep v1's eight (n = 10000) and six (n = 15000) universes.

Table III (Table II in v1) now gives the removed fraction with its range over universes:

| n | universes | C_J | C (fit) | removed (mean) | range over universes | wins |
|---|---|---|---|---|---|---|
| 1000 | 10 | 0.8855 | 0.9678 | 72 % | 61–81 % (s.d. 7) | 10/10 |
| 3000 | 10 | 0.9551 | 0.9884 | 74 % | 64–81 % (s.d. 6) | 10/10 |
| 6000 | 10 | 0.9764 | 0.9953 | 80 % | 76–85 % (s.d. 3) | 10/10 |

The v1 headline of 79–83 % at every size rested on two universes at n = 3000 (80 %). With ten universes it is 74 % there, and 80 % at n = 6000. The abstract now says "three quarters to four fifths", and the Results give the value at each size. The fit still improves on Johnston's embedding in every universe.

**Change:** Table III (new rows and columns), Results paragraph, abstract, new Table I (sets of sprinklings), Fig. 1 (n ≤ 6000 from the new runs), Limitations.

### Major 3: what the paper adds over Casasola

> An ablation should show that "all related pairs" matters. One option is to run Casasola's near-cone pseudo-likelihood (τ² < 6ℓ²) from the same intrinsic start and compare it with the full likelihood.

**Response.** Done, and the answer is that it does not matter. We ran Casasola's exact Poisson form, with the soft relation term of check (iv), twice from the same intrinsic start: once on all related pairs and once on the pairs with τ̂² < 6ℓ² only. The near-cone pairs are 64 %, 47 % and 37 % of related pairs at n = 1000, 3000 and 6000.

The near-cone version is slightly *better*:

| Comparison | n = 1000 | n = 3000 | n = 6000 |
|---|---|---|---|
| ΔC, near-cone − all pairs (exact Poisson form) | +0.00016 ± 0.00007 (8/10 universes) | +0.00041 ± 0.00004 (10/10) | +0.00030 ± 0.00003 (10/10) |
| ΔC, near-cone − all pairs (our Gaussian form) | — | +0.0002 ± 0.0001 (8/10) | +0.00024 ± 0.00004 (10/10) |

Distant related pairs therefore add nothing the fit uses. We have removed "the use of all related pairs" from our contributions (Introduction, item 3; "Relation to previous work"; Discussion, "What is new"). The paper now states that the gain is Casasola's likelihood, given an intrinsic start, and that the near-cone set also cuts the cost per iteration by a factor of two to three.

We kept the all-pairs Gaussian form as the reported method. Its settings were fixed before the test universes were run (check iii), and switching to the slightly better variant after seeing the test set would undo that. The ablation is reported next to it.

**Change:** new paragraph "Which pairs are needed?" in Sec. V; Introduction item 3; "Relation to previous work"; Discussion.

### Major 4: the optimizer finds a local optimum

> Please explain why there is no multi-start, annealing or second-order refinement (for example L-BFGS after Adam), and whether the 79–83% figure is limited by the method or by the optimizer.

**Response.** We ran the checks, and they reverse the explanation given in v1. On every universe of the large-n set we did three things:

- continued the Adam fit with L-BFGS to convergence;
- started converged fits from two further points, Johnston's map and the intrinsic map with every coordinate displaced by 0.5ℓ;
- ran the truth-started fit to convergence as well.

The results:

- **Adam was not converged.** L-BFGS raises the log-likelihood by 45 on average at n = 3000 (up to 98) and by 176 at n = 6000 (up to 410). But it changes C by only +1×10⁻⁴ and +2×10⁻⁴. This unconverged gap is what v1 read as a local optimum.
- **Converged, the three intrinsic starts agree.** They reach the same log-likelihood within a few units, out of 4.7×10⁵ terms. Their C agrees within the spread between universes: Johnston's start gives +0.0007 ± 0.0005. Picking whichever start has the highest likelihood gives 75.4 % instead of 74.5 %.
- **The truth-started fit has the same likelihood but a better map.** It removes 92 % of the residual (C = 0.9965 at n = 3000). Yet its log-likelihood exceeds the converged intrinsic fit by only 0.9 on average (at most 5).

The two maps are therefore equally consistent with the counts. The remaining error lies along directions in which the likelihood is nearly flat, mainly the positions of weakly constrained elements. More optimization cannot remove it; only more information can. To the referee's question, the ~75 % figure is limited by the method's information, not by the optimizer. Annealing would not help for the same reason.

v1 said the opposite ("a local optimum … not a floor of the likelihood"). The paper now says that this was wrong and why: Adam had not converged.

At n = 6000 the picture is the same:

- L-BFGS gains 176 in log-likelihood on average (up to 410) and +2×10⁻⁴ in C;
- the three converged starts agree within 10 units out of 1.9×10⁶ terms (Johnston's start: −0.0003 ± 0.0005 in C);
- the truth-started fit removes 93 % of the residual, but its log-likelihood is only 2.3 higher on average (at most 6.5).

**Change:** new paragraph "Is the residual set by the optimizer?" in Sec. V (replaces the last sentences of v1's per-element paragraph); Outlook; abstract (one sentence).

### Major 5: time coordinate held fixed

> Even an exploratory joint fit of time and space, or a clear argument that it would not change the conclusions, would help.

**Response.** Done (exploratory joint fit). We freed all time coordinates except the two tips, with the same likelihood, Adam and then L-BFGS, starting from Johnston's t and the intrinsic map. At n = 3000:

- C changes by +0.0004 ± 0.0001 (9/10 universes);
- the time error does not decrease (0.074 → 0.076ℓ rms).

Johnston's time coordinate is already accurate to a tenth of a discreteness length, and the related-pair counts do not improve it. The conclusions are unchanged. At n = 6000: +0.0002 ± 0.0001 in C (8/10 universes), time error 0.062 → 0.066ℓ.

**Change:** new paragraph "Time coordinate" in Sec. V; Limitations.

### Major 6: missing related work

> Major, Rideout and Surya, "Spatial hypersurfaces in causal set cosmology" (CQG 2006) and "On recovering continuum topology from a causal set" (J. Math. Phys. 2007), and Eichhorn, Surya and Versteegen, "Induced spatial geometry from causal structure" (CQG 2019).

**Response.** Added and discussed, in the Introduction's paragraph on existing constructions. Eichhorn–Surya–Versteegen also enter twice more: in the significance paragraph, and in Sec. IV, where we note that the +40 % bias of Johnston's detour on close pairs (Table II, the per-separation profile) is their "discrete asymptotic silence". All three references were checked against their arXiv and journal records.

**Change:** Introduction, Sec. IV, bibliography (MRS06, MRS07, ESV19).

---

## Minor comments

### Minor 1: notation of s_ab

> The normalization of s_ab, typeset as (2√N_ab+1), is ambiguous; add parentheses, e.g. 2√(N_ab + ½).

**Response.** The definitions are now displayed equations, with s_ab = τ̂²/[2 (N_ab+1)^{1/2}]. A sentence explains the shifts ½ and 1: they keep pairs with N = 0 finite. We kept N+1, which is what the code uses.

**Change:** Sec. V, displayed equation before Eq. (5).

### Minor 2: table of sets of sprinklings

**Response.** Done: new Table I (set, n and number of universes, time coordinate, where used) replaces the (a)/(b)/(b′)/(c) paragraph.

### Minor 3: abstract has too many numbers

**Response.** Rewritten. It keeps the headline results: three quarters to four fifths of the residual removed, per-pair errors roughly halved, the residual set by flat directions of the likelihood, and a smaller gain in the slab.

### Minor 4: figure of where the error is located

**Response.** Added: new Fig. 2. It shows the rms position error per element (after the best orthogonal map) for Johnston's embedding and the converged fit, at n = 3000 and 6000 with ten universes each. The left panel bins by decile of the element's number of related partners, the right panel by true time. In both embeddings the error is concentrated on the elements with the fewest related partners, near the waist; the fit lowers it everywhere.

**Change:** Fig. 2, paragraph "Where the error remains".

### Minor 5: mismatch with Johnston's Table IV

> The mismatch with Johnston's Table IV (0.82/0.90/0.93 vs 0.958/0.977/0.985) should be resolved with him if possible, not left as a "suspected" difference in statistic.

**Response.** Declined: we have not contacted the author. What we have checked:

- Our implementation reproduces his Tables III and V (the spatial correlation we use throughout) to within the spread between sprinklings.
- For the squared-interval correlation of his Table IV we obtain 0.82/0.90/0.93, both with his time coordinate and with the true one.
- So the difference is not in the time coordinate or in the embedding. The most likely explanation is a different statistic, for example a correlation over a different set of pairs or of unsquared intervals. We cannot establish which from the paper.

None of our conclusions uses Table IV, and the text says so. We would welcome the referee's view if another reading is evident.

**Change:** none.

### Minor 6: Johnston's method in the slab

> State explicitly that this modification is needed to make his method applicable there, and that it does not disadvantage him.

**Response.** Done. In the slab there are no tips, and 0.4 % of spacelike pairs at n = 1500 (0.1 % at n = 6000) have no element related to both. For those pairs his two-leg detour does not exist and his method is undefined. The four-leg fallback only completes it: every other pair keeps its two-leg value.

**Change:** Sec. VI, first paragraph.

### Minor 7: unrefereed preprints

**Response.** Done. Both references now say "not peer reviewed" and give their DOIs. The text states what is taken from each:

- **Casasola:** the form of the likelihood and the near-cone set, both reproduced here (Sec. V, "Relation to previous work").
- **Pellegrin:** the remark on endpoint inclusion and the boundary-truncation mechanism, both reproduced here (Secs. III and VI).

### Minor 8: Hu–Meyer–Meyer citation and arXiv numbers

> The journal year is 2025 (J. Math. Phys. 66, 122502) but the arXiv ID 2601.03280 begins 2601 (January 2026). Also check the arXiv numbers of the 2026 preprints.

**Response.** Checked; no change needed (declined), because the citation is correct. The paper appeared in J. Math. Phys. 66, 122502, dated 26 December 2025. It was submitted to arXiv on 31 December 2025 and announced in January 2026, hence the 2601 number. The arXiv record lists the same journal reference. arXiv:2610.36695 (Madsen, submitted 27 October 2026) was also checked against its arXiv record.

---

## Other changes not prompted by the review

- Introduction item 3 and Discussion ("What is new") rewritten to match the ablations (see Majors 3 and 4).
- Starting-map sentence: the start alone removes 23–59 % of Johnston's residual (v1: 23–47 %; the new n = 1000 universes).
- Check (ii), start independence, is now shown on the large-n set (Major 4) instead of the check sets.
- Per-pair errors and causal fidelity are recomputed on the ten-universe sets. Median per-pair error, Johnston → fit: 0.23 → 0.14ℓ at n = 3000 (v1, two universes: 0.22 → 0.11ℓ) and 0.18 → 0.12ℓ at n = 6000. Misclassified pairs: 0.68 % against 1.7 % (n = 3000) and 0.48 % against 1.1 % (n = 6000).
- A new Table I lists the sprinkling sets, so the v1 tables are renumbered (v1 Table I → Table II, v1 Table II → Table III).
- Fig. 1 (residual against n): n ≤ 6000 now from the new runs. The direct-overlap curve keeps v1's universes (that arm was not rerun).
- Data availability lists the new scripts.
- No latexdiff PDF this round.

## Results still marked as placeholders in v2

None.
