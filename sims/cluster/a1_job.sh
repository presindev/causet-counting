#!/bin/bash
# A1 on the cluster: 50 independent seeds x 2*10^4 uniform 2D orders at N = 200 (10^6 in total, ~11 CPU-hours at 39 ms each on the cluster).
# Each task works in node-local /tmp and copies one small .npz to /home at the end (compute.md rules).
# Submit from ~/exp/physics:   sbatch sims/cluster/a1_job.sh
# Test first with:        sbatch -p short --array=1-2 --export=ALL,NSAMP=200 sims/cluster/a1_job.sh
#SBATCH --job-name=a1
#SBATCH --account=<your-account>
#SBATCH --partition=low
#SBATCH --array=1-50%25
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=01:00:00
#SBATCH --output=a1/logs/%A_%a.out

set -euo pipefail
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1   # one core per task, no hidden threads
N=200
NSAMP=${NSAMP:-20000}
SEED=$((1000 + SLURM_ARRAY_TASK_ID))
OUT=$HOME/exp/physics/a1/out

WORK=/tmp/$USER-a1-$SLURM_ARRAY_JOB_ID-$SLURM_ARRAY_TASK_ID
mkdir -p "$WORK" "$OUT"
trap 'rm -rf "$WORK"' EXIT
cp $HOME/exp/physics/sims/*.py "$WORK"/
cd "$WORK"
# numpy without a venv: unzip the wheel into node-local /tmp (one 13 MB read from /home, no small-file NFS traffic).
# Nodes have Python 3.6.8, no numpy, no internet; numpy 1.19.5 is the last release for 3.6.
/usr/bin/python3 -m zipfile -e $HOME/exp/physics/wheels/numpy-1.19.5-cp36-cp36m-manylinux1_x86_64.whl pylib
export PYTHONPATH=$WORK/pylib
echo "host $(hostname)  seed $SEED  N $N  n $NSAMP"
/usr/bin/python3 a1_sample.py $N $NSAMP $SEED a1_N${N}_s${SEED}.npz
cp a1_N${N}_s${SEED}.npz "$OUT"/
