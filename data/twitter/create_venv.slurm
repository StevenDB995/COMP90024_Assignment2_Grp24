#!/bin/bash

# The name of the job:
#SBATCH --job-name="Virtual Environment Creation"

# The maximum running time of the job in day-hour:min:sec
#SBATCH --time=0-0:1:00

# check that the script is launched with sbatch
if [ "x$SLURM_JOB_ID" == "x" ]; then
   echo "You need to submit your job to the queuing system with sbatch"
   exit 1
fi

# The modules to load:
module load Python/3.10.4

# Create a virtual environment:
virtualenv ./venv
source ./venv/bin/activate
pip install ijson
pip install numpy
pip install mpi4py
deactivate
