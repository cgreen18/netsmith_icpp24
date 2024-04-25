
#!/bin/bash


# usage ./bash/process_topo_mclb.sh <base-name-of-topology> <directory> <number-routers> <allowed-number-escape-vns>
# e.g. "source ./bash/process_topo_mclb.sh ns_l_latop ./topologies_and_routing/topo_maps/20r 20 8"


# generate list of all paths
python3 python_scripts/routing.py --alg all_naive --filename ${2}/${1}.map



./../gurobi/bin/mclb -t ${2}/${1}.map -pl ./topologies_and_routing/allpath_lists/${1}.rallpaths -of ./topologies_and_routing/routepath_lists/${1}_mclb.paths --num_routers ${3}



python3 python_scripts/mclb_pruner.py ./topologies_and_routing/routepath_lists/${1}_mclb.paths
python3 python_scripts/mclb_pruner.py ./topologies_and_routing/routepath_lists/${1}_mclb.paths
python3 python_scripts/mclb_pruner.py ./topologies_and_routing/routepath_lists/${1}_mclb.paths


python3 python_scripts/routing.py --convert_pathlist --pathlist ./topologies_and_routing/routepath_lists/${1}_mclb.paths


python3 python_scripts/vnallocator.py --filename ${2}/${1}.map --min_n_vns ${4} --max_n_vns ${4} --alg_type mclb --lb_type hops --max_retries 50
