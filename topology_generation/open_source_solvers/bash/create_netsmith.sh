#!/bin/bash



case $2 in
    ("small") size_str="15" ;;
    ("med") size_str="2" ;;
    ("large") size_str="25" ;;
    (*) echo "INPUT ERROR: Unrecognized size. Options are small, med, large";;
esac


case $3 in
    ("latency") obj_str="avghops" ;;
    ("sparsest_cut") obj_str="scbw" ;;
    (*) echo "INPUT ERROR: Unrecognized objective. Options are latency, sparsest_cut";;
esac

# 3 day limit
BASE_FLAGS="--time_limit 4320"
BASE_FLAGS="--time_limit 5"

# 5 ports for an extra for node to router conn
CMD="python3 scipy_mip/run_scipy_mip.py --model_file ../gurobi/files/models/autotop_r${1}_p4_ll${size_str}_${obj_str}_simple.lp --out_map_name my_netsmith_${1}r_4p_${size_str}ll_${obj_str}_topo.map ${BASE_FLAGS}"

echo $CMD
$CMD