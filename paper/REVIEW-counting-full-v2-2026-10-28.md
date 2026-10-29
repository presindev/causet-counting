# Honest review: counting-full-v2 (19 pp., 2026-10-28, session 13)

Bar: a credible arXiv gr-qc preprint. Source `paper/counting-full-v2.tex`; previous draft and review in `archive/` (v1 ~70 %).
Changed: Sec. 9 (3+1) rewritten as one storyline; abstract, intro item (v), timeline, roles, mistakes, discussion, code list, App. A, 6 new references,
Fig. 6 regenerated (`sims/fig_3p1.py` now reads r14 + r24). Secs. 1–8 (1+1) unchanged.

## What the 3+1 part now says
Johnston 2025 reproduced → his error is all spacelike pairs (oracle) and almost all low-count pairs (k < 10 oracle: 88–96 %) → inverted distances cannot
close the gap (counting argument; the tail is geometric) → fit spatial coordinates to related-pair interval counts (Gaussian form of the Poisson likelihood,
= Casasola 2026, credited) from a count-weighted start → **79–83 % of his residual removed at n = 3000–15000, 21/21 universes**; checks: consistency
from the truth (0.966 / 0.991 / 0.9965 at n = 400 / 1000 / 2000), start independence (±1 point), ablation (our binomial term hurts), no tuning on test
universes; slab at n = 1500: +43 % (interior +69 %), the side wall costs about half (oracle +64 %); cost table/figure; limitations.

## Strengths
- One clear storyline; every dead end (switch, weighted map, binomial term, counts-only map, eigenmaps, Madsen charts) is in App. A with numbers.
- The headline gain is large, stable in n, and in every universe. Paired comparisons throughout.
- Credit is explicit: the likelihood is Casasola's, ML coordinates are classical (Ramsay, Hoff, Boguñá 2010, Mercator, Sim). Our share is stated narrowly.
- The ablation, and the episode behind it, are reported in the method section; this is honest and makes the method section stronger.

## Weaknesses a referee would see
1. **"Ours" is now thinner.** The likelihood is Casasola's; our contributions are the diagnosis, the intrinsic start, all related pairs and the benchmark.
   A referee may say "applying an existing likelihood to an existing benchmark". Defence: Casasola never compared with Johnston, started from the truth,
   and used only near-cone pairs; the low-count diagnosis explains *why* it works. Still, say it plainly (done in Sec. 9.3 "Credit" and the discussion).
2. **Casasola is a Research Square preprint**, not arXiv/INSPIRE. Our search beyond those databases was one session deep (lesson 26). Before submission:
   one more pass (Google Scholar, Research Square, SSRN, OpenReview) for interval-count likelihoods in causal sets.
3. **[CLOSED, session 13, r26]** Exact Poisson + soft relation term = Gaussian within 0.0003 (n = 1500, 3000); text updated (check (v)). Original item: **Gaussian form, not the exact Poisson likelihood.** Justified by a gradient problem, not by a comparison. A referee will ask whether the exact form does
   better or worse. One laptop run at n = 1500/3000 would answer it.
4. **[CLOSED, session 13, r26]** 1000 iterations = 400 within 0.0002 at n ≤ 3000; text updated. Original item: **Not converged.** Log-likelihood still rising at iteration 400 (0.01–0.05 % per 100). Stated; gains are a lower bound. A run with 800–1000 iterations
   at n = 3000–6000 would show whether the number moves.
5. **Time coordinate fixed to Johnston's.** The slab used the true time. A joint time+space fit is the obvious next question; not done.
6. **Second shape at one size and 3 universes;** equal-density cluster run (r25: jobs 450431–450435) pending, placeholder in Sec. 9.3. Error bars ±10 points.
7. **Cost claims are on shared nodes.** Johnston's min-plus mean at 15000 is 21 344 s here vs 12 077 s in v1 (2 vs 6 universes, loaded nodes). The fit
   time equal at 10000 and 15000 is unexplained (stated). A clean timing run on an exclusive node would settle the cost paragraph.
8. **n = 1000 has one universe** (67 %); the table starts at 3000 for that reason. n = 3000 has two (± only indicative).
9. Table IV of Johnston still not reproduced (unchanged from v1).

## What is ours, and how deep we searched
| Claim | Search depth |
|---|---|
| 1+1 items (rectangle identity, depth drift, detector calibration, Laguerre target) | as in v1 review (citer crawls, full text) |
| Exact tabulated overlap inversion for a general reference (3+1) | BK24 citers crawled for 1+1; **not re-checked for a 3+1 inversion** (carry-over) |
| Johnston reproduction, oracle, low-count oracle, counting argument | Johnston 2025 has one INSPIRE citer (Madsen 2026, read in full) |
| Likelihood fit from an intrinsic start, all related pairs, Johnston benchmark | session-12 review: INSPIRE/arXiv + ~15 web searches + Crossref; Casasola found outside arXiv. Medium-high confidence for indexed work, medium beyond |
| Binomial overlap term | not found anywhere; but it hurts, so it is in App. A, not a claim |

## Off-arXiv literature pass (session 13, done; details in literature.md)
- Corrected in the text: BK24 already invert the overlap exactly for equal depths (our "small-d approximation" claim was wrong; lesson 38); our 3+1 table is the
  unequal-depth extension. The 3π two-hop count follows from Johnston 2008's normalization (now a consistency check).
- New credits: Pellegrin 2026 (Zenodo: strict-count convention found independently; wall/order-convexity mechanism; a different diagnosis of the fill), Rideout–Wallden
  2009 (tile D = 1+1 naive distance), Huang 2014 / Buschmann 2006 (Euclidean overlap-count distance, incl. MLE + CRLB), Costa–Patwari–Hero 2006, Müller 2025, Clough
  thesis 2017, Aghili–Bombelli–Pilgrim 2018, Eichhorn et al. 2026. Bibliography: 9 entries corrected/completed.
- Nothing found that anticipates: the past-only rectangle identity, the depth-drift curvature, the embedding-test calibration + zero share, the Laguerre target, the
  low-count diagnosis, or the likelihood-from-intrinsic-start vs Johnston. Search depth stated in the Discussion; gaps: Google Scholar, thesis full texts, abstract books.
- Effect on the paper: the "ours" list is narrower in 3+1 (table extension is minor; the wall mechanism is Pellegrin's) and unchanged in 1+1. Honest and defensible.

## Missing before arXiv
- Fill the r25 placeholder (equal-density slab), or drop to "one size" wording.
- ~~Exact-Poisson vs Gaussian comparison; 1000-iteration check~~ (done, null: r26); optionally a clean timing run.
- ~~One more off-arXiv literature pass~~ (done, session 13). Optional: Google Scholar "cited by" for Johnston25, BK24, Clough–Evans when accessible.
- Carry-overs: 3+1 inversion literature check; N = 800 detector check; code/data release; Roberto's items (author line/affiliation details, AI statement wording,
  endorser, code URL). Boguñá email after the paper (session 12 decision).

## Update 2026-10-29 (session 14)
- r25 filled (Sec. 9.3, abstract, limitations): at equal density the slab gives +58 / +65 % (all pairs, n = 6000 / 12000) vs diamond +75 / +80 %; the oracle wall
  correction closes the whole gap; wall cost ~20 points at every n; the gain needs density (one slab universe at n = 600 loses).
- Roberto's items done: author line (SapereIA and ICCUB, Barcelona; roberto@sapereia.com), AI statement kept, code public at github.com/presindev/causet-counting
  (sims/ + job scripts + README + MIT; smoke-tested from the clean copy), no endorser needed (gr-qc author). Date span now 24–29 Oct; mistake log 40 entries.
- 3+1 inversion literature check done: BK24 full text re-read (Eq. 16 any c; exact inversion Eq. 22 only at equal depth; Eqs. 32–34 filter c to equal depth); all 7 INSPIRE
  citers grepped in full (Johnston25, Shuman ×2, HMM25, BK25, Madsen26, Jones 2602.16782 new), BK25 p. 7 read (restates BK24), MG17 abstract, Rideout–Wallden 2008/09
  (different construction: min over w, z). No unequal-depth inversion found. Claim stays as a narrow extension; quote added to the Discussion. Gap: Google Scholar / APS cited-by.
- Still open: optional N = 800 detector check, clean timing run, Google Scholar citers. Then Boguñá email.

## Distance to the bar
The 3+1 half went from "modest switch result with a placeholder" to a coherent, large, well-checked result with honest credit. Remaining items are mostly
single laptop runs plus one pending cluster job. Overall: **~80 %**; 1–2 sessions if the four quick checks come out as expected.
