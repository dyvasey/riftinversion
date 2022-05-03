#!/bin/bash
#SBATCH -J riftinv
#SBATCH -o log_XXX
#SBATCH -e %j
#SBATCH -p skx-normal
#SBATCH -t 48:00:00
#SBATCH -N XXX
#SBATCH -n XXX
#SBATCH -A TG-EAR080022N

# load modules
module load gcc/7.1.0 

# Aspect executable
ASP="/work2/07937/davasey/stampede2/software/gcc-7.1.0/aspect/aspect-2.4.0-pre-nal/aspect/build/./aspect"

# Run model.  Submit job with "sbatch run.sh"
ibrun $ASP XXX


