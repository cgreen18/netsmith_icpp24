
#!/bin/bash


# usage: ./bash/process_mclb_noci_topo.sh <base-name-of-topology> <directory> <number-routers> <allowed-number-escape-vns>
# e.g. "source ./bash/process_mclb_noci_topo.sh kite_small ./topologies_and_routing/topo_maps/20r

python3 python_scripts/gen_NoCI_map.py --filename topologies_and_routing/topo_maps/my_20r_4p_25ll_topo.map
python3 python_scripts/routing.py --alg all_picky --filename ./topologies_and_routing/topo_maps/noci/my_20r_4p_25ll_topo_noci.map
../gurobi/bin/noci_mclb -t ./topologies_and_routing/topo_maps/noci/my_20r_4p_25ll_topo_noci.map -pl topologies_and_routing/allpath_lists/my_20r_4p_25ll_topo_noci_picky.rallpaths --num_routers 84 -of my_20r_4p_25ll_topo_noci_picky_mclb_cohmem_prioritized_doubley_memory --cohmem_prioritized --doubley_memory
python3 python_scripts/mclb_pruner.py ./topologies_and_routing/routepath_lists/my_20r_4p_25ll_topo_noci_picky_mclb_cohmem_prioritized_doubley_memory.paths
python3 python_scripts/routing.py --convert_pathlist --pathlist ./topologies_and_routing/routepath_lists/my_20r_4p_25ll_topo_noci_picky_mclb_cohmem_prioritized_doubley_memory.paths
python3 python_scripts/vnallocator.py --filename ./topologies_and_routing/topo_maps/noci/my_20r_4p_25ll_topo_noci.map --nr_list ./topologies_and_routing/nr_lists/my_20r_4p_25ll_topo_noci_picky_mclb_cohmem_prioritized_doubley_memory.nrl --path_list ./topologies_and_routing/routepath_lists/my_20r_4p_25ll_topo_noci_picky_mclb_cohmem_prioritized_doubley_memory.paths --min_n_vns 6 --max_n_vns 6 --max_retries 50 --alg_type mclb_cohmem_prioritized_doubley_memory --out_vn_name topologies_and_routing/vn_maps/my_20r_4p_25ll_topo_noci_picky_mclb_cohmem_prioritized_doubley_memory_hops_6vns.vn