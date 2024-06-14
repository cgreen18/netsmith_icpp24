
#!/bin/bash


# usage: ./bash/process_noci_topo_mclb.sh <base-name-of-topology> <directory> <number-routers> <allowed-number-escape-vns>
# e.g. "source ./bash/process_noci_topo_mclb.sh my_20r_4p_25ll_avghops_topo_noci ./topologies_and_routing/topo_maps/noci 9



python3 python_scripts/routing.py --alg all_picky --filename ${2}/${1}

../gurobi/bin/noci_mclb -t ${2}/${1} -pl topologies_and_routing/allpath_lists/${1}_picky.rallpaths --num_routers 84 -of ${1}_picky_mclb_cohmem_prioritized_doubley_memory --cohmem_prioritized --doubley_memory
python3 python_scripts/mclb_pruner.py ./topologies_and_routing/routepath_lists/${1}_picky_mclb_cohmem_prioritized_doubley_memory.paths
python3 python_scripts/routing.py --convert_pathlist --pathlist ./topologies_and_routing/routepath_lists/${1}_picky_mclb_cohmem_prioritized_doubley_memory.paths
python3 python_scripts/vnallocator.py --filename ./topologies_and_routing/topo_maps/noci/${1}.map --nr_list ./topologies_and_routing/nr_lists/${1}_picky_mclb_cohmem_prioritized_doubley_memory.nrl --path_list ./topologies_and_routing/routepath_lists/${1}_picky_mclb_cohmem_prioritized_doubley_memory.paths --min_n_vns ${3} --max_n_vns ${3} --max_retries 50 --alg_type mclb_cohmem_prioritized_doubley_memory --out_vn_name topologies_and_routing/vn_maps/${1}_picky_mclb_cohmem_prioritized_doubley_memory_hops_${3}vns.vn


