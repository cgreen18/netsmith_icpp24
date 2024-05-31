#!/bin/bash



case $2 in
    ("small") size_str="15ll" ;;
    ("med") size_str="2ll" ;;
    ("large") size_str="25ll" ;;
    (*) echo "Unrecognized size. Options are small, med, large";;
esac


case $3 in
    ("latency") obj_str="total_hops" ;;
    ("power") obj_str="power" ;;
    (*) echo "Unrecognized objective. Options are latency, power";;
esac


# 3 day limit
BASE_FLAGS="--use_run_sol --time_limit 4320 --write_model --heuristic_ratio 0.8 --mip_focus 1 --concurrent_mip"

# 5 ports for an extra for node to router conn
CMD="./bin/lpbt -if files/prob_defs/dev_${1}r_5p_${size_str}.dat -of my_lpbt_${3}_${1}r_${2}_topo -o ${obj_str} ${BASE_FLAGS}"

echo $CMD
$CMD