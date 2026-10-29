#!/bin/bash
# Poisson likelihood on the slab vs the diamond at EQUAL DENSITY (idea 005, session 13; sims/r25_slab_lik.py). One universe per task, seed = 2500 + task id.
# Slab volume = 4 x diamond volume, so pairs are (diamond n, slab n) = (1500, 6000) and (3000, 12000).
# Laptop slab n = 3000 (one universe, 400 iterations): 80 s total (his detour 23 s, our step 5 s, K100 1 s, Poisson fit 17 s, oracle shares 10 s + fit 17 s), peak 4.5 GB.
# Scaling: detour and our step O(n^3), the rest O(n^2); cluster 4-10x slower than the laptop (r14/r24). Estimates and requests (>= 2x, lesson 22):
#   slab 12000: ~3-6 h, ~70 GB  -> --mem=110G --time=20:00:00     slab 6000: ~0.5-1 h, ~18 GB -> --mem=32G --time=05:00:00
#   diamond 3000: ~10-20 min, ~5 GB -> --mem=12G --time=02:00:00   diamond 1500: minutes  -> --mem=6G --time=01:00:00
# Saves after every stage (johnston, switch, w_K100, poisson, oracle_wall) straight to $OUT, so a timeout keeps the arms already done.
# Submit from ~/exp/physics:  mkdir -p r25/logs r25/out && sbatch --array=1-4 --mem=32G --time=05:00:00 --export=ALL,SHAPE=slab,N=6000 sims/cluster/r25_job.sh
#SBATCH --job-name=r25
#SBATCH --account=<your-account>
#SBATCH --partition=low
#SBATCH --cpus-per-task=4
#SBATCH --exclude=cn04                       # cn04 stalled A1 three times and the first n400 test (compute.md)
#SBATCH --output=r25/logs/%A_%a.out

set -euo pipefail
export OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 MKL_NUM_THREADS=4  # BLAS (matmul, eigh) on the 4 cores; the detour is single-threaded numpy
SHAPE=${SHAPE:-diamond}
N=${N:-600}
SEED=$((2500 + SLURM_ARRAY_TASK_ID))
NAME=r25_${SHAPE}_n${N}_s${SEED}
OUT=$HOME/exp/physics/r25/out

WORK=/tmp/$USER-r25-$SLURM_JOB_ID-$SLURM_ARRAY_TASK_ID
mkdir -p "$WORK/out" "$OUT"
trap 'rm -rf "$WORK"' EXIT
cp $HOME/exp/physics/sims/*.py "$WORK"/
cp $HOME/exp/physics/sims/out/r11_lens_table_v2.npz "$WORK"/out/   # without it r11 would rebuild the table (slow)
cd "$WORK"
# numpy without a venv: unzip the wheel into node-local /tmp (see a1_job.sh and compute.md).
/usr/bin/python3 -m zipfile -e $HOME/exp/physics/wheels/numpy-1.19.5-cp36-cp36m-manylinux1_x86_64.whl pylib
export PYTHONPATH=$WORK/pylib
echo "host $(hostname)  shape $SHAPE  n $N  seed $SEED  $(date)"
/usr/bin/python3 -u r25_slab_lik.py one $SHAPE $N $SEED $OUT/$NAME.npz   # five tiny writes to /home (one per stage): a timeout keeps the arms done
echo "done $(date)"   # peak memory: sacct -j <job> --format=JobID%20,State,Elapsed,MaxRSS,NodeList
