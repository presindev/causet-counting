#!/bin/bash
# Held-out N = 800 test of the layered flag (paper Sec. 5; idea 005, session 14): e^{-beta S_BD} (eps = 0.21) chains with sims/n400_crystal.py at N = 800, HOT starts only.
# 28 tasks = 7 betas x 4 seeds, 2000 sweeps each. beta N = 8 ... 560; at N = 400 hot chains turned layered within ~250 sweeps for beta N >= 180 and stayed
# continuum-like at beta N = 120 for 15000 sweeps (session 14 check), so 2000 sweeps give both kinds of state. They are test inputs, not equilibrium samples.
# Laptop N = 800: 1.5 s/sweep, 80 MB (N = 400: 0.18). N = 400 on this cluster ran 0.9-2.6 s/sweep => N = 800 ~8-23 s/sweep => 4.5-13 h; --time 30 h (lesson 22).
# Checkpoint: n400_crystal.py writes <name>.partial.npz to $OUT every 20 records = 400 sweeps.
# Submit from ~/exp/physics:  mkdir -p r27/logs r27/out && sbatch sims/cluster/r27_job.sh
# Test first:                 sbatch -p short --time=00:30:00 --array=0,27 --export=ALL,NSWEEP=20 sims/cluster/r27_job.sh
# Analyse (laptop):           .venv/bin/python sims/r27_n800_detector.py analyse cluster_fetch/r27/out
#SBATCH --job-name=r27
#SBATCH --account=<your-account>
#SBATCH --partition=low
#SBATCH --array=0-27%14
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --exclude=cn04                       # cn04 stalled A1 three times and the first n400 test (compute.md)
#SBATCH --time=30:00:00
#SBATCH --output=r27/logs/%A_%a.out

set -euo pipefail
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1   # one core per task, no hidden threads
N=800
NSWEEP=${NSWEEP:-2000}
EVERY=20
BETAS=(0.01 0.05 0.1 0.2 0.3 0.45 0.7)
I=$SLURM_ARRAY_TASK_ID                       # I = 4*beta_index + seed_index
BETA=${BETAS[$((I / 4))]}
SEED=$((2700 + I))
NAME=r27_n800_b${BETA}_hot_s${SEED}
OUT=$HOME/exp/physics/r27/out

WORK=/tmp/$USER-r27-$SLURM_ARRAY_JOB_ID-$I
mkdir -p "$WORK" "$OUT"
trap 'rm -rf "$WORK"' EXIT
cp $HOME/exp/physics/sims/*.py "$WORK"/
cd "$WORK"
# numpy without a venv: unzip the wheel into node-local /tmp (see a1_job.sh and compute.md).
/usr/bin/python3 -m zipfile -e $HOME/exp/physics/wheels/numpy-1.19.5-cp36-cp36m-manylinux1_x86_64.whl pylib
export PYTHONPATH=$WORK/pylib
export N400_PARTIAL_DIR=$OUT                # checkpoints into r27/out, not n400/out
echo "host $(hostname)  task $I  beta $BETA  start hot  seed $SEED  N $N  sweeps $NSWEEP  $(date)"
/usr/bin/python3 -u n400_crystal.py $N $BETA hot $SEED $NSWEEP $NAME.npz $EVERY
cp $NAME.npz "$OUT"/
echo "done $(date)"
