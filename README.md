# Geometry by counting in causal sets — notebook and code

Research notebook and simulation code behind R. Bada, *Geometry by counting in causal sets: exact 1+1 tools, and spatial distances in 3+1*
(arXiv link to be added; the current draft is `paper/counting-full-v2.pdf`).

The work was done in fourteen sessions (24–29 October 2026) by one physicist working with an AI system (Claude, Anthropic) as a research colleague,
through the Claude Code command-line tool. Sec. 2 of the paper describes how. This repository is a snapshot of the whole notebook, kept as it was used,
so that the process can be judged and reused, not only the results.

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
| `paper/` | Current draft and its review; `paper/archive/` holds every earlier draft with its review; `draft-v6` is the growth-memory line (a separate, unfinished paper) |

Left out of the public copy: the notes on the computing cluster's internal configuration (`compute.md`, referred to in the journal).
The notebook covers more than the paper: ideas 001–004, 006 and 007 (discrete spacetime, growth memory, quantum histories) are ongoing work.

## The code: what reproduces what

**1+1 dimensions**
| Paper | Script |
|---|---|
| Figures of Part I | `sims/fig_part1.py` |
| Overlap distance, rectangle identity | `sims/s4a_overlap_distance.py`, `sims/s4a_desitter.py` |
| Depth drift, curvature fit, FRW check | `sims/r9_drift_fit_frw.py` (also `r5_drift_meanfield.py`, `r6_curvature_fixed_n.py`) |
| Embedding-test calibration and the zero-share flag | `sims/s4a_embedding.py`, `sims/s4b_detector.py`, `sims/r8_detector_spread.py` |
| N = 400 Monte Carlo states | `sims/n400_crystal.py` (cluster: `sims/cluster/n400_job.sh`) |
| Chain-sum propagator, Laguerre target | `sims/b_johnston_propagator.py`, `sims/b_johnston_n400.py` |

**3+1 dimensions**
| Paper | Script |
|---|---|
| Overlap table and estimator | `sims/r11_4d_distance.py` (table cached in `sims/out/r11_lens_table_v2.npz`) |
| Reproduction of Johnston (2025), oracle | `sims/r12_johnston_compare.py` |
| Low-count diagnosis | `sims/r18_waist_oracle.py` |
| Weighted start (SMACOF) | `sims/r16_local_fit.py`, `sims/r19_cluster_wfit.py` |
| Likelihood fit | `sims/r23_likelihood.py`; cluster runs `sims/r24_cluster_lik.py`; checks `sims/r26_exact_iters.py` |
| Second shape (slab) | `sims/r22_slab.py`, `sims/r25_slab_lik.py` |
| Switch (App. A) | `sims/r13_mixed.py`, `sims/r14_cluster_scale.py` |
| Fig. 6 | `sims/fig_3p1.py` (reads the cluster outputs of r14 and r24) |

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
Please cite the paper; to point at the notebook or code specifically, cite the repository as well (GitHub's "Cite this repository" button reads `CITATION.cff`).
```bibtex
@misc{Bada2026counting,
  author = {Bada, Roberto},
  title  = {Geometry by counting in causal sets: exact 1+1 tools, and spatial distances in 3+1},
  year   = {2026},
  note   = {arXiv identifier to be added}
}
@misc{Bada2026notebook,
  author       = {Bada, Roberto},
  title        = {Geometry by counting in causal sets: research notebook and code},
  year         = {2026},
  howpublished = {\url{https://github.com/presindev/causet-counting}},
  note         = {Snapshot of 29 October 2026}
}
```

## Licence
Code (`sims/`, `viz/`): MIT (see `LICENSE`). Notes and paper drafts: CC BY 4.0.
