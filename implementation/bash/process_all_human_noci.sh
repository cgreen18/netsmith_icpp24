#!/bin/bash

for b in  "ft_x" "butter_donut_x" "dbl_bfly_x" "kite_large" "kite_medium" "kite_small";
    do
        CMD="source bash/process_human_noci_topo.sh ${b}_noci ./topologies_and_routing/topo_maps/noci"
        echo "${CMD}"
        $CMD
    done