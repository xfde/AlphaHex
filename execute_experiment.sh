#!/bin/bash --login
#$ -cwd               # Run the job in the current directory
#$ -l nvidia_v100=1

date
echo "Starting experiment number: $experiment_number."

# Load modules
module load apps/binapps/anaconda3/2021.11
module load libs/cuda
module load libs/intel-18.0/hdf5/1.10.5_mpi              # Intel 18.0.3 compiler, OpenMPI 4.0.1
module load apps/binapps/pytorch/0.4.1-36-gpu
#module load tools/env/proxy

pip install torch==1.4.0 --user

#qsub -l short -terse -hold_jid 1 -M andrei.popescu-3@student.manchester.ac.uk ./bash_scripts/drone_xz.sh exp
python3 ./src/train.py

echo "Experiment $experiment_number complete."
