#!/bin/bash
#SBATCH -J fastscape_test
#SBATCH --time=00-96:00:00
#SBATCH -p vaseylab
#SBATCH -N XXX
#SBATCH -n XXX
#SBATCH -c 2
#SBATCH --output=test.%j.%N.out
#SBATCH --error=test.%j.%N.err

#Load modules
source ~/vaseylab/shared/software/intel_oneapi/intel/oneapi/setvars.sh

#FASTSCAPE variable
export GFORTRAN_CONVERT_UNIT='big_endian'
echo $GFORTRAN_CONVERT_UNIT

#ASPECT executable
ASPDIR="/cluster/home/dvasey01/vaseylab/shared/software/aspect/v2.6.0-pre-845dd6d/aspect"

#Run model
mpirun -n XXX $ASPDIR/build/./aspect ./XXX


