#!/bin/bash

# makefile writes executable here
if [ ! -d ./gurobi/bin  ]
then
    mkdir ./gurobi/bin
fi

if [ ! -d ./files  ]
then
    mkdir ./files
fi

if [ ! -d ./gurobi/static_metrics  ]
then
    mkdir ./files/static_metrics
fi

if [ ! -d ./files/graphs  ]
then
    mkdir ./files/graphs
fi

if [ ! -d ./topologies_and_routing  ]
then
    mkdir ./topologies_and_routing
fi

for b in  "allpath_lists"  "nr_lists"  "routepath_lists"  "topo_maps"  "vn_maps";
    do
        CMD="mkdir ./topologies_and_routing/${b}"
        # echo "${CMD}"
        $CMD
    done


for b in "20r" "30r" "48r" "64r" "noci";
    do
        CMD="mkdir ./topologies_and_routing/topo_maps/${b}"
        # echo "${CMD}"
        $CMD
    done
