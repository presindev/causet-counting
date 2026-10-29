#!/bin/bash
# Johnston 2025 vs ours vs the switch at larger n (idea 005, session 11; sims/r14_cluster_scale.py). One universe per array task, seed = 1000 + task id.
# Laptop n = 3000: 25 s total (his min-plus 16 s), 2.8 GB peak; memory ~ n^2, min-plus ~ n^3 (worse beyond n = 3000 on the laptop: 17.8 s -> 76 s for 3000 -> 4000).
# cluster ~4x slower per core, x2 under load (lesson 22). Per n:  --mem / --time
#   N=1000 (test)  2G / 0:10      N=3000  8G / 2:00      N=6000  24G / 8:00      N=10000  64G / 24:00      N=15000  144G / 96:00
# No checkpoint inside a universe (one universe = one task; results are a few numbers).
# Submit from ~/exp/physics:  mkdir -p r14/logs r14/out && sbatch --array=1-4 --mem=24G --time=08:00:00 --export=ALL,N=6000 sims/cluster/r14_job.sh
#SBATCH --job-name=r14
#SBATCH --account=<your-account>
#SBATCH --partition=low
#SBATCH --cpus-per-task=4
#SBATCH --exclude=cn04                       # cn04 stalled A1 three times and the first n400 test (compute.md)
#SBATCH --output=r14/logs/%A_%a.out

set -euo pipefail
export OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 MKL_NUM_THREADS=4  # BLAS (matmul, eigh) on the 4 cores; the min-plus is single-threaded numpy
N=${N:-1000}
SEED=$((1000 + SLURM_ARRAY_TASK_ID))
NAME=r14_n${N}_s${SEED}
OUT=$HOME/exp/physics/r14/out

WORK=/tmp/$USER-r14-$SLURM_JOB_ID-$SLURM_ARRAY_TASK_ID
mkdir -p "$WORK/out" "$OUT"
trap 'rm -rf "$WORK"' EXIT
cp $HOME/exp/physics/sims/*.py "$WORK"/
cp $HOME/exp/physics/sims/out/r11_lens_table_v2.npz "$WORK"/out/   # without it r11 would rebuild the table (slow)
cd "$WORK"
# numpy without a venv: unzip the wheel into node-local /tmp (see a1_job.sh and compute.md).
/usr/bin/python3 -m zipfile -e $HOME/exp/physics/wheels/numpy-1.19.5-cp36-cp36m-manylinux1_x86_64.whl pylib
export PYTHONPATH=$WORK/pylib
echo "host $(hostname)  n $N  seed $SEED  $(date)"
/usr/bin/python3 -u r14_cluster_scale.py $N $SEED $NAME.npz
cp $NAME.npz "$OUT"/
echo "done $(date)"   # peak memory: sacct -j <job> --format=JobID%20,State,Elapsed,MaxRSS,NodeList
