#!/bin/bash
# Branch C factorization test on the cluster (idea 004, session 8): exact future factors F_N(stem) to N = 11, stems of size 2-4 (sims/a2_future_factor.py).
# Laptop N = 10: 45 s, 0.2 M memo states, 0.48 GB. N = 11: ~2.8 M states => ~7-8 GB, ~15 min laptop, x4 on the cluster, x2 under load => ~2 h.
# One memoized recursion: it can't checkpoint, so --time is generous instead (lesson 22). Session 8 test: N = 9 took 2:58 on the cluster.
# Submit from ~/exp/physics:   mkdir -p fn/logs && sbatch sims/cluster/fn_job.sh   (N = 12: sbatch --mem=200G --time=72:00:00 --export=ALL,NMAX=12 sims/cluster/fn_job.sh)
# Test first with:        sbatch -p short --time=00:10:00 --mem=2G --export=ALL,NMAX=9 sims/cluster/fn_job.sh
#SBATCH --job-name=fn
#SBATCH --account=<your-account>
#SBATCH --partition=low
#SBATCH --cpus-per-task=1
#SBATCH --mem=24G
#SBATCH --exclude=cn04                       # cn04 stalled A1 three times and the first n400 test (compute.md)
#SBATCH --time=24:00:00                     # N=9 test took 3 min vs ~5 s laptop (<= 60x incl. startup): N=11 could need ~15 h
#SBATCH --output=fn/logs/%j.out

set -euo pipefail
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1   # one core, no hidden threads
NMAX=${NMAX:-11}
NAME=fn_N${NMAX}
OUT=$HOME/exp/physics/fn/out

WORK=/tmp/$USER-fn-$SLURM_JOB_ID
mkdir -p "$WORK" "$OUT"
trap 'rm -rf "$WORK"' EXIT
cp $HOME/exp/physics/sims/*.py "$WORK"/
cd "$WORK"
# numpy without a venv: unzip the wheel into node-local /tmp (see a1_job.sh and compute.md).
/usr/bin/python3 -m zipfile -e $HOME/exp/physics/wheels/numpy-1.19.5-cp36-cp36m-manylinux1_x86_64.whl pylib
export PYTHONPATH=$WORK/pylib
echo "host $(hostname)  Nmax $NMAX  $(date)"
/usr/bin/python3 -u a2_future_factor.py $NMAX 2,3,4 $NAME.npz
cp $NAME.npz "$OUT"/
echo "done $(date)"   # peak memory: sacct -j <job> --format=MaxRSS,Elapsed
