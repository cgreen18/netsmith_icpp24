#!/bin/bash

# max for synthetic traffic (unless you change some source code)
n_cycles=2147483647

if [ $# -gt 0 ]; then
    n_cycles="$1"

fi


# note the noi frequencies passed
# small
for t in "kite_small" "lpbt_s_latop" "lpbt_s_power";
    do
        source ./bash/synth_inj_sweep_topo.sh ./topologies_and_routing/topo_maps/20r/${t}.map ./topologies_and_routing/nr_lists/${t}_nndbt.nrl ./topologies_and_routing/vn_maps/${t}_nndbt_hops_2vns.vn 3.6GHz 2 6 20 40 4 0.01 0.15 0.005 $n_cycles &
    done


# med
for t in "kite_med" "ft_x" "lpbt_s_latop" "lpbt_s_power";
    do
        source ./bash/synth_inj_sweep_topo.sh ./topologies_and_routing/topo_maps/20r/${t}.map ./topologies_and_routing/nr_lists/${t}_nndbt.nrl ./topologies_and_routing/vn_maps/${t}_nndbt_hops_2vns.vn 3.0GHz 2 6 20 40 4 0.01 0.15 0.005 $n_cycles &
    done


# large
for t in "kite_large" "dbl_bfly_x" "butter_donut_x";
    do
        source ./bash/synth_inj_sweep_topo.sh ./topologies_and_routing/topo_maps/20r/${t}.map ./topologies_and_routing/nr_lists/${t}_nndbt.nrl ./topologies_and_routing/vn_maps/${t}_nndbt_hops_2vns.vn 2.7GHz 2 6 20 40 4 0.01 0.15 0.005 $n_cycles &
    done
