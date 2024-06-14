#!/bin/bash

n_cycles=2147483647
n_cycles=1000

source ./bash/synth_inj_sweep_topo.sh ./topologies_and_routing/topo_maps/64r/ours/ns_s_latop_64r.map ./topologies_and_routing/nr_lists/ns_s_latop_64r_mclb.nrl ./topologies_and_routing/vn_maps/ns_s_latop_64r_mclb_hops_9vns.vn 3.6GHz 9 12 64 64 4 0.01 0.24 0.01 $n_cycles &

source ./bash/synth_inj_sweep_topo.sh ./topologies_and_routing/topo_maps/64r/ours/ns_m_latop_64r.map ./topologies_and_routing/nr_lists/ns_m_latop_64r_mclb.nrl ./topologies_and_routing/vn_maps/ns_m_latop_64r_mclb_hops_9vns.vn 3.0GHz 9 12 64 64 4 0.01 0.24 0.01 $n_cycles &

source ./bash/synth_inj_sweep_topo.sh ./topologies_and_routing/topo_maps/64r/ours/ns_l_latop_64r.map ./topologies_and_routing/nr_lists/ns_l_latop_64r_mclb.nrl ./topologies_and_routing/vn_maps/ns_l_latop_64r_mclb_hops_9vns.vn 2.7GHz 9 12 64 64 4 0.01 0.24 0.01 $n_cycles &