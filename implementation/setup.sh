#!/bin/bash

# purdue ecn server specific
module load gcc/11.2.0
module load gurobi/10.0
#module load gurobi/11.0
export GRB_LICENSE_FILE=/package/gurobi/10.0/license/gurobi.lic
#export GRB_LICENSE_FILE=/package/gurobi/11.0/license/gurobi.lic
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/package/gurobi/10.0/lib
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/package/gurobi/11.0/lib
