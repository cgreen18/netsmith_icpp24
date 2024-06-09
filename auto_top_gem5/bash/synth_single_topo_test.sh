#!/bin/bash

# usage: ./bash/synth_single_topo.sh <map> <nrl> <vn>
# e.g. "source ./bash/synth_single_topo_simple.sh"

python3 python_scripts/run_synth.py -s 1000 --mixedfreq_only --inj_end 0.2 --inj_start 0.02 --inj_step 0.02 --n_evn 4 --tot_vcs 6 --coh_only --sys_clk 4.0 --dir_mult 4 --one_topo ./topologies_and_routing/topo_maps/ns_l_latop.map --nr_list ./topologies_and_routing/nr_lists/ns_l_latop_mclb.nrl --vn_map ./topologies_and_routing/vn_maps/ns_l_latop_mclb_hops_4vns.vn --noi_freq 2.7GHz --n_routers 20 --num_cpus 40