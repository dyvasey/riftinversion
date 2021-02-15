#!/bin/bash
#SBATCH -J riftinv
#SBATCH -o log_ri_rift_1cm_100km_base
#SBATCH -e %j
#SBATCH -p skx-normal
#SBATCH -t 48:00:00
#SBATCH -N 1
#SBATCH -n 48
#SBATCH -A TG-EAR080022N

# load modules
module load gcc/7.1.0 

# Aspect executable
ASP="/work/07937/davasey/stampede2/software/aspect/build/./aspect"

# Run model.  Submit job with "sbatch run.sh"
ibrun $ASP XXX


