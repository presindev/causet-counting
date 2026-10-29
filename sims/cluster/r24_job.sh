#!/bin/bash
# Likelihood embedding at large n (idea 005, session 12; sims/r24_cluster_lik.py), same universes as r14 (seed = 1000 + task id), paired against its Johnston numbers.
# No min-plus. Laptop n = 3000: ~0.3 s per likelihood iteration x 400; O(pairs) => ~25x at 15000; cluster 2-4x slower. Saves after the start map and after the fit.
# Per n (--mem / --time, generous):
#   N=1000 (test) 2G / 0:15   N=3000 8G / 2:00   N=6000 24G / 6:00   N=10000 48G / 12:00   N=15000 100G / 24:00
# No checkpoint inside a universe (one universe = one task; results are a few numbers).
# Submit from ~/exp/physics:  mkdir -p r24/logs r24/out && sbatch --array=1-4 --mem=12G --time=04:00:00 --export=ALL,N=6000 sims/cluster/r24_job.sh
#SBATCH --job-name=r24
#SBATCH --account=<your-account>
#SBATCH --partition=low
#SBATCH --cpus-per-task=4
#SBATCH --exclude=cn04                       # cn04 stalled A1 three times and the first n400 test (compute.md)
#SBATCH --output=r24/logs/%A_%a.out

set -euo pipefail
export OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 MKL_NUM_THREADS=4  # BLAS (matmul, eigh) on the 4 cores; the min-plus is single-threaded numpy
N=${N:-1000}
SEED=$((1000 + SLURM_ARRAY_TASK_ID))
NAME=r24_n${N}_s${SEED}
OUT=$HOME/exp/physics/r24/out

WORK=/tmp/$USER-r24-$SLURM_JOB_ID-$SLURM_ARRAY_TASK_ID
mkdir -p "$WORK/out" "$OUT"
trap 'rm -rf "$WORK"' EXIT
cp $HOME/exp/physics/sims/*.py "$WORK"/
cp $HOME/exp/physics/sims/out/r11_lens_table_v2.npz "$WORK"/out/   # without it r11 would rebuild the table (slow)
cd "$WORK"
# numpy without a venv: unzip the wheel into node-local /tmp (see a1_job.sh and compute.md).
/usr/bin/python3 -m zipfile -e $HOME/exp/physics/wheels/numpy-1.19.5-cp36-cp36m-manylinux1_x86_64.whl pylib
export PYTHONPATH=$WORK/pylib
echo "host $(hostname)  n $N  seed $SEED  $(date)"
/usr/bin/python3 -u r24_cluster_lik.py $N $SEED $NAME.npz
cp $NAME.npz "$OUT"/
echo "done $(date)"   # peak memory: sacct -j <job> --format=JobID%20,State,Elapsed,MaxRSS,NodeList
