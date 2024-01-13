#!/bin/bash
#SBATCH -p compute            # Specify partition [Compute/Memory/GPU]
#SBATCH -N 1 -c 128   	      # Specify number of nodes and processors per task
#SBATCH --ntasks-per-node=1   # Specify tasks per node
#SBATCH -t 20:00:00          # Specify maximum time limit (hour: minute: second)
#SBATCH -A lt200067           # Specify project name
#SBATCH -J preprocess_data            # Specify job name

# run
python preprocess.py

