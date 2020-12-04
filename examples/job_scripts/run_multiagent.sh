#!/bin/sh
#$ -cwd
#$ -j y
#$ -pe smp 8
#$ -l h_vmem=8G
#$ -l h_rt=96:0:0
#$ -l gpu_type=kepler
#$ -l gpu=1

module load singularity/3.6.1
module load python/3.6.3
module load java/1.8.0_152-oracle
source ~/malmo/venv/bin/activate
module load cudnn/7.6.5-cuda-10.0

python ../multi_agent_training.py --num_gpus 1 --num_envs 3 --checkpoint_freq 20 > output.txt
