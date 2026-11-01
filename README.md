# Geometry by counting in causal sets — notebook and code

Research notebook and simulation code behind two papers by R. Bada:

- *Spatial embedding of 3+1 causal sets: low-count spacelike pairs and a likelihood fit to interval counts* (prepared for Phys. Rev. D;
  source and PDF in `paper/embedding-3p1/`, current version v6);
- *Spatial distance and curvature from an exact counting identity in two-dimensional causal sets* (prepared for Class. Quantum Grav.;
  `paper/toolkit-1p1/`, current version v6).

arXiv identifiers will be added here. The work was done in twenty-one sessions (24 October – 1 November 2026) by one physicist working with an AI system
(Claude, Anthropic) as a research colleague, through the Claude Code command-line tool; both papers were then revised over four rounds with a second AI
session acting as an external referee. The methodology note (`paper/methodology-note/methodology-note-v2.pdf`) describes both. This repository is a
snapshot of the whole notebook, kept as it was used, so that the process can be judged and reused, not only the results.

## The notebook
| File | What it is |
|---|---|
| `CLAUDE.md` | The working charter given to the AI at the start of every session: roles, honesty rules (no flattery; label claims established / literature / ours), session protocol |
| `LESSONS.md` | The mistake log: every error caught, and the working rule it produced |
| `INDEX.md`, `ROADMAP.md` | Map of all ideas with status; what is alive, waiting or unexplored |
| `GRAVEYARD.md` | Dead ends, with the reason each died |
| `ideas/` | One file per idea, with derivations, numbers and a dated log |
| `journal/` | One entry per session: what was discussed, decided and corrected |
| `literature.md` | Every reference touched, why it matters, and how deeply it was checked |
| `notation.md` | Symbols and conventions |
| `paper/` | One folder per paper (`embedding-3p1/`, `toolkit-1p1/`, `methodology-note/`): every version with its latexdiff, the referee reports in `reviews/` and the author's answers in `answers/`; `referee-workspace/` holds the referee session's instructions, memory and comment-by-comment history; `counting-full-v2.pdf` is the combined draft the two papers were split from; `paper/archive/` holds every earlier draft with its review; `archive/draft-v6` is the growth-memory line (a separate, unfinished paper) |

Left out of the public copy: the notes on the computing cluster's internal configuration (`compute.md`, referred to in the journal).
The notebook covers more than the papers: ideas 001–004, 006 and 007 (discrete spacetime, growth memory, quantum histories) are ongoing work.

## The code: what reproduces what
Each paper's Data availability statement lists the script behind every number; in short:

**1+1 paper (`toolkit-1p1`)**
| Result | Script |
|---|---|
| Figures | `sims/fig_part1.py` |
| Distance estimator: baseline; Hu–Meyer–Meyer comparison and ablations | `sims/r31_rect_baseline.py`; `sims/r36_rect_ablation_hmm.py` |
| Curvature estimator: window, pooled form, Benincasa–Dowker and chain abundances | `sims/r37_curvature_referee.py` |
| Sprinkled-pair selection, convex region, FRW, one-region comparison | `sims/r40_curvature_round2.py`, `sims/r41_curvature_round3.py` |
| Drift kernel (FRW equation); curvature fit and FRW check | `sims/r38_drift_kernel.py`; `sims/r9_drift_fit_frw.py` |
| Null-pair fraction; N = 800 test; heights of random orders | `sims/r8_detector_spread.py`; `sims/r27_n800_detector.py`; `sims/r42_flat_height.py` |
| e^{−βS} states (N = 400) | `sims/n400_crystal.py` (cluster: `sims/cluster/n400_job.sh`) |
| Propagator (appendix) | `sims/b_johnston_n400.py`, `sims/r32_laguerre_vs_fraction.py` |

**3+1 paper (`embedding-3p1`)**
| Result | Script |
|---|---|
| Overlap table | `sims/r11_4d_distance.py` (table cached in `sims/out/r11_lens_table_v2.npz`) |
| Reproduction of Johnston (2025), oracles | `sims/r12_johnston_compare.py`, `sims/r18_waist_oracle.py`, `sims/r30_johnston_lowk_oracle.py` |
| Starting map (weighted SMACOF) | `sims/r19_cluster_wfit.py` |
| Likelihood fit; large-n runs | `sims/r23_likelihood.py`; `sims/r24_cluster_lik.py` |
| Per-pair and per-element errors, likelihood comparison | `sims/r29_perpair_error.py`, `sims/r33_time_vs_position.py`, `sims/r34_lnl_causal_fidelity.py` |
| Slab | `sims/r22_slab.py`, `sims/r25_slab_lik.py` |
| Ten universes per size, ablations, optimizer and joint-fit checks; error-location figure | `sims/r35_referee1_3p1.py`, `sims/r35_analyse.py` |
| Likelihood path and valley, near-cone variant cost | `sims/r39_3p1_round2.py`, `sims/r39_summary.py` |
| Main figure | `sims/fig_3p1.py --prd` |

Small result files are in `sims/out/`; large cluster outputs are not included (rerun with the job scripts).

## Running
```
python3 -m venv .venv && .venv/bin/pip install numpy matplotlib
cd sims && ../.venv/bin/python r23_likelihood.py      # likelihood fit, n = 1500, 3 universes (a few minutes)
```
Scripts take optional arguments, read in the `if __name__ == "__main__"` block at the bottom of each file.
The figure scripts read the cluster outputs from `cluster_fetch/` and `n400_*` folders next to `sims/`. Tested with Python 3.9, numpy 2.0, matplotlib 3.9;
the cluster runs used numpy 1.19 on Python 3.6. Large runs (n ≥ 6000) were done on a SLURM cluster with the job scripts in `sims/cluster/`; each script's header
gives the submit line, time and memory. Set `--account` to your own.

## How the code was written
The code was written by the AI system working with the author; the author did not review it line by line, so the results rest on the checks reported
in the paper (known answers, fresh seeds, ablations) and logged in `LESSONS.md`. Please report problems as GitHub issues.

## How to cite
Please cite the papers; to point at the notebook or code specifically, cite the repository as well (GitHub's "Cite this repository" button reads `CITATION.cff`).
```bibtex
@misc{Bada2026embedding,
  author = {Bada, Roberto},
  title  = {Spatial embedding of $3+1$ causal sets: low-count spacelike pairs and a likelihood fit to interval counts},
  year   = {2026},
  note   = {Prepared for Phys. Rev. D; arXiv identifier to be added}
}
@misc{Bada2026toolkit,
  author = {Bada, Roberto},
  title  = {Spatial distance and curvature from an exact counting identity in two-dimensional causal sets},
  year   = {2026},
  note   = {Prepared for Class. Quantum Grav.; arXiv identifier to be added}
}
@misc{Bada2026notebook,
  author       = {Bada, Roberto},
  title        = {Geometry by counting in causal sets: research notebook and code},
  year         = {2026},
  howpublished = {\url{https://github.com/presindev/causet-counting}},
  doi          = {DOI to be added},
  note         = {Zenodo archive of the version used for the papers}
}
```

## Licence
Code (`sims/`, `viz/`): MIT (see `LICENSE`). Notes and paper drafts: CC BY 4.0.
