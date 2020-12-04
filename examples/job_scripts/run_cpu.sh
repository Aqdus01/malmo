#!/bin/sh
#$ -cwd
#$ -j y
#$ -pe smp 16
#$ -l h_vmem=7.5G
#$ -l h_rt=96:0:0

module load singularity/3.6.1
module load python/3.6.3
module load java/1.8.0_152-oracle
source ~/malmo/venv/bin/activate

# use less workers than CPUs requested
python ../single_agent_training.py --num_workers 14 --checkpoint_freq 20 > output.txt

