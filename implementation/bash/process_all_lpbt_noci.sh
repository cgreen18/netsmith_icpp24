#!/bin/bash

for b in  "lpbt_s_latop" "lpbt_s_power" "lpbt_m_latop";
    do
        CMD="source bash/process_human_noci_topo.sh ${b}_noci ./topologies_and_routing/topo_maps/noci"
        echo "${CMD}"
        $CMD
    done