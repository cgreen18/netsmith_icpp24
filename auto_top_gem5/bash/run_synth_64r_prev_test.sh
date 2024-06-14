#!/bin/bash

n_cycles=2147483647
n_cycles=1000

# small
source ./bash/synth_inj_sweep_topo.sh ./topologies_and_routing/topo_maps/64r/prev/kite_small_64r.map ./topologies_and_routing/nr_lists/kite_small_64r_nndbt.nrl ./topologies_and_routing/vn_maps/kite_small_64r_nndbt_hops_2vns.vn 3.6GHz 2 12 64 64 4 0.01 0.2 0.01 $n_cycles &

# med
source ./bash/synth_inj_sweep_topo.sh ./topologies_and_routing/topo_maps/64r/prev/ft_64r.map ./topologies_and_routing/nr_lists/ft_64r_nndbt.nrl ./topologies_and_routing/vn_maps/ft_64r_nndbt_hops_2vns.vn 3.0GHz 2 12 64 64 4 0.01 0.2 0.01 $n_cycles &
source ./bash/synth_inj_sweep_topo.sh ./topologies_and_routing/topo_maps/64r/prev/kite_med_64r.map ./topologies_and_routing/nr_lists/kite_med_64r_nndbt.nrl ./topologies_and_routing/vn_maps/kite_med_64r_nndbt_hops_2vns.vn 3.0GHz 2 12 64 64 4 0.01 0.2 0.01 $n_cycles &

# large
source ./bash/synth_inj_sweep_topo.sh ./topologies_and_routing/topo_maps/64r/prev/bdonut_64r.map ./topologies_and_routing/nr_lists/bdonut_64r_nndbt.nrl ./topologies_and_routing/vn_maps/bdonut_64r_nndbt_hops_2vns.vn 2.7GHz 2 12 64 64 4 0.01 0.2 0.01 $n_cycles &
source ./bash/synth_inj_sweep_topo.sh ./topologies_and_routing/topo_maps/64r/prev/dbl_bfly_64r.map ./topologies_and_routing/nr_lists/dbl_bfly_64r_nndbt.nrl ./topologies_and_routing/vn_maps/dbl_bfly_64r_nndbt_hops_2vns.vn 2.7GHz 2 12 64 64 4 0.01 0.2 0.01 $n_cycles &