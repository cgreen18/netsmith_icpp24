#!/bin/bash

# usage: ./bash/synth_single_topo.sh <map> <nrl> <vn>
# e.g. "source ./bash/synth_inj_sweep_topo.sh ./topologies_and_routing/topo_maps/my_12r_topo.map ./topologies_and_routing/nr_lists/my_12r_topo_mclb.nrl ./topologies_and_routing/vn_maps/my_12r_topo_mclb_hops_4vns.vn 0.02 0.2 0.02 2.7GHz 4 6 12 12 2147483647"

# max cycles = 2147483647

# coh
python3 python_scripts/run_synth.py -s ${13} --mixedfreq_only --inj_end ${11} --inj_start ${10} --inj_step ${12} --n_evn ${5} --tot_vcs ${6} --coh_only --sys_clk 4.0 --dir_mult ${9} --one_topo ${1} --nr_list ${2} --vn_map ${3} --noi_freq ${4} --n_routers ${7} --num_cpus ${8}

# mem
python3 python_scripts/run_synth.py -s ${13} --mixedfreq_only --inj_end ${11} --inj_start ${10} --inj_step ${12} --n_evn ${5} --tot_vcs ${6} --mem_only --sys_clk 4.0 --dir_mult ${9} --one_topo ${1} --nr_list ${2} --vn_map ${3} --noi_freq ${4} --n_routers ${7} --num_cpus ${8}