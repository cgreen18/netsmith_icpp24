



source ./bash/synth_inj_sweep_topo.sh ./topologies_and_routing/topo_maps/64r/ours/ns_s_latop_64r.map ./topologies_and_routing/nr_lists/ns_s_latop_64r_mclb.nrl ./topologies_and_routing/vn_maps/ns_s_latop_64r_mclb_hops_9vns.vn 3.6GHz 9 12 64 64 4 0.02 0.2 0.02




./build/Garnet_standalone/gem5.fast -d ./synth_outputs/simple/2b/mixed/uniform/9evns_12vcs_64cpus_4xdirs_4.0GHz/coh/ns_s_latop_64r/0_02/ configs/netsmith/netsmith_synth.py --topology EscapeVirtualNetworks --noi_routers 64 --sim-cycles 2147483647 --injectionrate 0.02 --noc_clk 4.0GHz --sys-clock 4.0GHz --ruby-clock 4.0GHz --noi_clk 3.6GHz --router_map_file ./topologies_and_routing/topo_maps/64r/ours/ns_s_latop_64r.map --flat_vn_map_file ./topologies_and_routing/vn_maps/ns_s_latop_64r_mclb_hops_9vns.vn --flat_nr_map_file ./topologies_and_routing/nr_lists/ns_s_latop_64r_mclb.nrl --ruby --mem_or_coh coh --mem-size 320000000 --num-dirs 256 --num-cpus 64 --network garnet --mem-type SimpleMemory --routing-algorithm 2 --use_escape_vns --synth_traffic --vcs-per-vnet 12 --evn_deadlock_partition 3 --evn_n_deadlock_free 1 --evn_min_n_deadlock_free 9
