#!/bin/bash
# Created by the University of Melbourne job script generator for SLURM
# Thu Mar 07 2024 20:28:21 GMT+1100 (Australian Eastern Daylight Time)

# Partition for the job:
#SBATCH --partition=cascade

# The name of the job:
#SBATCH --job-name="Cluster and Cloud Computing Assignment 1 – Social Media Analytics"

# Maximum number of tasks/CPU cores used by the job:
#SBATCH --nodes=2
#SBATCH --ntasks=16

# The maximum running time of the job in days-hours:mins:sec
#SBATCH --time=0-6:0:00

# check that the script is launched with sbatch
if [ "x$SLURM_JOB_ID" == "x" ]; then
   echo "You need to submit your job to the queuing system with sbatch"
   exit 1
fi

# Run the job from the directory where it was launched (default)

# run programe
module load Python/3.10.4
source ./venv/bin/activate

# The job command(s):
echo "1 node 8 cores using twitter-100gb.json"
time srun --nodes 1 --ntasks 8 python3 twitter_doi.py twitter-100gb.json

deactivate

##DO NOT ADD/EDIT BEYOND THIS LINE##
##Job monitor command to list the resource usage
my-job-stats -a -n -s
