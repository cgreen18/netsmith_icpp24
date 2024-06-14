#!/bin/bash

# max for synthetic traffic (unless you change some source code)
n_cycles=2147483647

if [ $# -gt 0 ]; then
    n_cycles="$1"

fi

# note the noi frequencies passed
for t in "ns_s_latop" "ns_s_scop";
    do
        source ./bash/synth_inj_sweep_topo.sh ./topologies_and_routing/topo_maps/20r/${t}.map ./topologies_and_routing/nr_lists/${t}_mclb.nrl ./topologies_and_routing/vn_maps/${t}_mclb_hops_4vns.vn 3.6GHz 4 6 20 40 4 0.01 0.15 0.005 $n_cycles &
    done

for t in "ns_m_latop" "ns_m_scop";
    do
        source ./bash/synth_inj_sweep_topo.sh ./topologies_and_routing/topo_maps/20r/${t}.map ./topologies_and_routing/nr_lists/${t}_mclb.nrl ./topologies_and_routing/vn_maps/${t}_mclb_hops_4vns.vn 3.0GHz 4 6 20 40 4 0.01 0.15 0.005 $n_cycles &
    done

for t in "ns_l_latop" "ns_l_scop";
    do
        source ./bash/synth_inj_sweep_topo.sh ./topologies_and_routing/topo_maps/20r/${t}.map ./topologies_and_routing/nr_lists/${t}_mclb.nrl ./topologies_and_routing/vn_maps/${t}_mclb_hops_4vns.vn 2.7GHz 4 6 20 40 4 0.01 0.15 0.005 $n_cycles &
    done
