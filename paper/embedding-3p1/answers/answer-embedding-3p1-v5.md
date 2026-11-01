# Answer to the referee: embedding-3p1, round 4 (PRD)

**Manuscript:** "Spatial embedding of 3+1 causal sets: low-count spacelike pairs and a likelihood fit to interval counts" (R. Bada).
**This answer** responds to `review-embedding-3p1-v4.md` (recommendation: accept) and comes with `embedding-3p1-v5.pdf` and `embedding-3p1-v5-diff.pdf` (latexdiff against v4).

**Placeholders and preconditions remaining in the manuscript:**
1. **Zenodo DOI** (Data availability, shown in red as "[Zenodo DOI]"). It is the optional archive of comment 21, and the same tagged release as the companion paper, so one DOI fills both. It can exist before upload. Zenodo's GitHub integration mints a DOI when a release is published, and the code is final. So: make the repository public, tag the release, copy the DOI into both papers, and rebuild. If the DOI is not available in time, delete the clause ", and the version used for this paper is archived at doi:[Zenodo DOI]". The rest of the sentence stands without it.
2. **Repository public (precondition, not a placeholder).** As comment 21 asks, Data availability and Ref. [32] are now in the present tense ("are openly available at …", "released with the code at …"). At the time of writing, `github.com/presindev/causet-counting` is still **private**. Both sentences become true only when the author publishes the snapshot (`release/make_public.sh --push`) and switches the repository to public. This must happen **before** the file is uploaded.

We thank the referee for the fourth report and the recommendation. Only the points listed in comments 19–21 have changed (plus the version note in the LaTeX source comments, which does not print).

---

## Comment 19: sign counts, and the range against the intrinsic fit

> **Sec. V, sign counts: "These differences are no larger than what further iterations add to the intrinsic fit."** Strictly this is not so: at n = 3000 the mean margin (0.9) exceeds the continuation gain (0.5); the largest margins (5.4 and 6.5) exceed the gain at both sizes. […] Suggested wording: "These differences are of the same order as what further iterations add to the intrinsic fit (below), and the two fits were not continued equally, so they do not tell which of the two maps the likelihood prefers."
>
> In the relaxation paragraph, "within O(1) of both ends" is supported in the text only against the truth-started end. Please also quote the range relative to the intrinsic fit (−0.9 to +5.3 at n = 3000 and +0.3 to +6.7 at n = 6000, from the response).
>
> Optional, Outlook: "In practice the error will therefore be reduced by additional information rather than by more optimization of Eq. (5)" is a prediction. "is more likely to be reduced" would match the evidence.

**Response.** We agree with all three parts and used the suggested wording.

**(a) Changed text, Sec. V, second paragraph of "Is the residual set by the optimizer or by the likelihood?":**

> These differences are of the same order as what further iterations add to the intrinsic fit (below), and the two fits were not continued equally, so they do not tell which of the two maps the likelihood prefers.

**(b) Changed text, same paragraph (relaxations):**

> Each of these maps has a log-likelihood within O(1) of both ends (−3.8 to +0.6 from the truth-started fit and −0.9 to +5.3 from the intrinsic fit at n = 3000; −1.1 to +0.7 and +0.25 to +6.7 at n = 6000).

The ranges are taken over the three starting points s = 0.25, 0.5, 0.75 and the ten universes, from `sims/out/r39_relax_s_round3.txt`:
- n = 3000, "lnL − fit": [+0.06, +1.61], [−0.90, +5.23] and [+0.02, +5.30], which gives −0.90 to +5.30.
- n = 6000: [+0.31, +6.01], [+0.34, +6.44] and [+0.25, +6.73], which gives +0.25 to +6.73.

We quote the n = 6000 lower end as +0.25 rather than +0.3, because one decimal would round it ambiguously.

As the referee advised, we draw **no** directional conclusion from these ranges. The fact that every n = 6000 relaxation lies above the intrinsic fit is not stated. Several margins are below the 2.4 continuation gain, so it is the same situation as comment 15.

**(c) Changed text, Outlook:**

> In practice the error is therefore more likely to be reduced by additional information rather than by more optimization of Eq. (5): …

---

## Comment 20: abstract, "become rarer only slowly with density"

> The body does not show that the low-count pairs become rarer slowly. The only abundance figures (Sec. IV: k < 10 pairs are 50 % of spacelike pairs at n = 1500 and 31 % at n = 3000) fall roughly as n^−0.7. That is not slow. What Sec. IV argues ("Why higher density helps slowly") is that their *errors* decrease slowly […]. Please either reword ("and their errors decrease only slowly with density") or add the k < 10 share at larger n if it supports the present wording.

**Response.** We agree, and took the first option. We have no k < 10 shares beyond n = 3000, and the two we have do not support "rarer only slowly". The abstract now says what Sec. IV argues.

**Changed text, Abstract:**

> … almost all of the residual error of that method comes from spacelike pairs whose shared causal regions contain fewer than ten elements; these pairs concentrate at the waist of the causal diamond, and their errors decrease only slowly with density.

**Consistency checked:**
- Introduction, item 2 (unchanged) already reads "give a scaling argument for why their errors decrease only slowly with density".
- Sec. IV, "Why higher density helps slowly" (unchanged), argues exactly this: typical errors fall as n^−1/2, but the tail is geometric.
- Sec. IV, "Low-count pairs" (unchanged), gives the abundances 50 % and 31 % without describing their trend.

The three now agree.

---

## Comment 21: Data availability and Ref. [32] at submission

> Since making the repository public is the step just before upload, please change the sentence to the present tense then ("are openly available at …"), and do the same for Ref. [32]. A Zenodo archive of the tagged release is not required by PRD but would be good practice, as for the companion paper.

**Response.** Done in the file to be uploaded. As listed at the top, the repository must be made public before upload. We also added the optional Zenodo DOI. It is the same release as the companion paper's, so one DOI serves both.

**Changed text, Data availability:**

> The code that produces every number in this paper, and the research notebook in which the work was carried out, are openly available at https://github.com/presindev/causet-counting, and the version used for this paper is archived at doi:[Zenodo DOI]. The overlap table is in …

**Changed text, Ref. [32]:**

> R. Bada, Two causal-set papers written with an AI research partner: methodology note (2026), released with the code at https://github.com/presindev/causet-counting.

---

## Checks before delivery

**Abstract against body (every number and claim):**

| Abstract | Body |
|---|---|
| "fewer than ten elements"; "almost all of the residual" | Sec. IV, "Low-count pairs": the k < 10 oracle removes 97 % (n = 1500) and 94 % (n = 3000) of Johnston's residual |
| "concentrate at the waist" | Sec. IV: "most of them straddle the waist"; Sec. V, "Where the error remains" (time t ≈ 1/2) |
| "their errors decrease only slowly with density" (new) | Sec. IV, "Why higher density helps slowly": tail set by position; overlap residual ~n^−0.4 between n = 6000 and 15000 |
| "44 sprinklings with 1000–15000 elements" | Table I (10 + 10 + 10 + 8 + 6) and Sec. V, "Results" |
| "improves … in every universe" | Sec. V: "in each of the 44 universes" |
| "removes 72–83 %" | Sec. V: 72 % (n = 1000), 74 %, 80 %, 79–83 % (n = 10000, 15000) |
| "lowers the median error … by a third" | Sec. V: median 0.33/0.23/0.18 → 0.20/0.14/0.12, i.e. −39 %, −39 %, −33 % |
| "more than halves its tail" | Sec. V: 90th percentile 1.14/0.76/0.59 → 0.46/0.33/0.27 (−60 %, −57 %, −54 %); 99th 3.1/2.9/2.4 → 1.4/0.7/0.5 |
| "differ in log-likelihood by only O(1)" | Sec. V: sign counts (≤ 6.5), relaxations (−3.8 … +6.7), continuation (+0.5, +2.4) |
| "almost no information that would let an optimizer prefer" | Sec. V, last sentence of the paragraph (same wording) |
| "in a region without a waist the gain is smaller … truncated at its timelike boundary" | Sec. VI (slab) |

**Old phrases searched** in the v5 source and in the text extracted from the v5 PDF. None remains:
- "no larger than": 0;
- "rarer only slowly": 0;
- "on average over independent sprinklings": 0;
- "rectangle lies inside": 0;
- "will be made openly available": 0;
- "to be released": 0;
- "will therefore be reduced": 0.

**Other changes:** none. The only other edit is a comment line in the LaTeX source recording the v5 changes, which does not print.
