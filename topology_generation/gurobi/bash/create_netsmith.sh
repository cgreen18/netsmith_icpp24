#!/bin/bash

# $1 = n_routers
# $2 = size
# $3 = objective

case $2 in
    ("small") size_str="15" ;;
    ("med") size_str="2" ;;
    ("large") size_str="25" ;;
    (*) echo "Unrecognized size. Options are small, med, large";;
esac


case $3 in
    ("latency") obj_str="avg_hops" ;;
    ("sparsest_cut") obj_str="sc_bw" ;;
    (*) echo "Unrecognized objective. Options are latency, sparsest_cut";;
esac

# 3 day limit
BASE_FLAGS="--use_run_sol --time_limit 4320 --write_model --heuristic_ratio 0.8 --mip_focus 1 --concurrent_mip --model_type w_hop --max_diam 20"

# 5 ports for an extra for node to router conn
CMD="./bin/auto_top -if files/prob_defs/dev_${1}r_5p_${size_str}ll.dat -of my_${1}r_4p_${size_str}ll_${obj_str}_topo -o ${obj_str} ${BASE_FLAGS}"

echo $CMD
$CMD