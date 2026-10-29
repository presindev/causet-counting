#!/bin/bash
# N = 400 crystallisation check on the cluster: e^{-beta S_BD} (eps = 0.21) on 2D orders, hot vs cold starts (sims/n400_crystal.py).
# 80 tasks = 10 betas x {hot, cold} x 4 seeds, 15000 sweeps each (~1.2 s/sweep on the cluster => ~5 h per task, ~400 CPU-hours total).
# Each task works in node-local /tmp and copies one small .npz to /home at the end (compute.md rules).
# Submit from ~/exp/physics:   sbatch sims/cluster/n400_job.sh
# Test first with:        sbatch -p short --time=00:20:00 --array=0,79 --export=ALL,NSWEEP=200 sims/cluster/n400_job.sh
#SBATCH --job-name=n400
#SBATCH --account=<your-account>
#SBATCH --partition=low
#SBATCH --array=0-79%12                    # at most 12 at once: share the group allocation politely
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --exclude=cn04                       # cn04 stalled A1 three times and the first n400 test (compute.md)
#SBATCH --time=14:00:00                     # session 7: loaded nodes ran 1.1-2.6 s/sweep; 6 h killed 20 tasks (compute.md)
#SBATCH --output=n400/logs/%A_%a.out

set -euo pipefail
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1   # one core per task, no hidden threads
N=400
NSWEEP=${NSWEEP:-15000}
EVERY=50
BETAS=(0.01 0.02 0.03 0.05 0.08 0.12 0.2 0.3 0.45 0.7)
STARTS=(hot cold)
I=$SLURM_ARRAY_TASK_ID                       # I = 8*beta_index + 4*start_index + seed_index
BETA=${BETAS[$((I / 8))]}
START=${STARTS[$(((I / 4) % 2))]}
SEED=$((2000 + I))
NAME=n400_b${BETA}_${START}_s${SEED}
OUT=$HOME/exp/physics/n400/out

WORK=/tmp/$USER-n400-$SLURM_ARRAY_JOB_ID-$I
mkdir -p "$WORK" "$OUT"
trap 'rm -rf "$WORK"' EXIT
cp $HOME/exp/physics/sims/*.py "$WORK"/
cd "$WORK"
# numpy without a venv: unzip the wheel into node-local /tmp (see a1_job.sh and compute.md).
/usr/bin/python3 -m zipfile -e $HOME/exp/physics/wheels/numpy-1.19.5-cp36-cp36m-manylinux1_x86_64.whl pylib
export PYTHONPATH=$WORK/pylib
echo "host $(hostname)  task $I  beta $BETA  start $START  seed $SEED  N $N  sweeps $NSWEEP  $(date)"
/usr/bin/python3 n400_crystal.py $N $BETA $START $SEED $NSWEEP $NAME.npz $EVERY
cp $NAME.npz "$OUT"/
echo "done $(date)"
