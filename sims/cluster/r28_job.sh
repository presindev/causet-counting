#!/bin/bash
# Clean timing run for the paper's cost paragraph (Sec. 9.5, Fig. 6b; idea 005, session 14). The r14/r24 timings came from shared, loaded nodes
# (the fit's time at n = 15000 equalled its time at 10000, unexplained). Here: one EXCLUSIVE node per task, tasks one after another (%1),
# the same 4 BLAS threads as before, the same universe per n (seed 1001, as r14/r24 task 1). Per task: r14 (Johnston's pipeline: C@C, min-plus, eigh;
# also our counting step), then r24 with the Poisson arm only (ours_step, fit_K100, setup, poisson_only: 400 iterations).
# Loaded-node times (r14 + r24, n = 15000): ~2.1e4 + 1.6e4 s ~ 10.5 h; exclusive should be faster. --time 36 h (lesson 22). Memory: whole node (--mem=0).
# Array index -> n: 1 3000, 2 6000, 3 10000, 4 15000.
# Submit from ~/exp/physics:  mkdir -p r28/logs r28/out && sbatch sims/cluster/r28_job.sh
# Test first:                 sbatch -p short --time=00:30:00 --array=0 --export=ALL sims/cluster/r28_job.sh      (index 0 = n 1000)
# Analyse (laptop):           .venv/bin/python sims/r28_timing.py runs/cluster_fetch/r28/out
#SBATCH --job-name=r28
#SBATCH --account=<your-account>
#SBATCH --partition=low
#SBATCH --array=1-4%1
#SBATCH --exclusive
#SBATCH --mem=0
#SBATCH --cpus-per-task=4
#SBATCH --exclude=cn04                       # cn04 stalled A1 three times and the first n400 test (compute.md)
#SBATCH --time=36:00:00
#SBATCH --output=r28/logs/%A_%a.out

set -euo pipefail
export OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 MKL_NUM_THREADS=4  # as r14/r24: BLAS on 4 cores; the min-plus is single-threaded numpy
NS=(1000 3000 6000 10000 15000)
N=${NS[$SLURM_ARRAY_TASK_ID]}
SEED=1001
OUT=$HOME/exp/physics/r28/out

WORK=/tmp/$USER-r28-$SLURM_JOB_ID-$SLURM_ARRAY_TASK_ID
mkdir -p "$WORK/out" "$OUT"
trap 'rm -rf "$WORK"' EXIT
cp $HOME/exp/physics/sims/*.py "$WORK"/
cp $HOME/exp/physics/sims/out/r11_lens_table_v2.npz "$WORK"/out/   # without it r11 would rebuild the table (slow)
cd "$WORK"
/usr/bin/python3 -m zipfile -e $HOME/exp/physics/wheels/numpy-1.19.5-cp36-cp36m-manylinux1_x86_64.whl pylib
export PYTHONPATH=$WORK/pylib
echo "host $(hostname)  n $N  seed $SEED  exclusive  $(date)"; nproc; uptime
/usr/bin/python3 -u r14_cluster_scale.py $N $SEED r28_r14_n${N}.npz
cp r28_r14_n${N}.npz "$OUT"/
R24_ARMS=poisson_only /usr/bin/python3 -u r24_cluster_lik.py $N $SEED r28_r24_n${N}.npz
cp r28_r24_n${N}.npz "$OUT"/
uptime; echo "done $(date)"
