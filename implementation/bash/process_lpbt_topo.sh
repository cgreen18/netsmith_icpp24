
#!/bin/bash


# usage: ./bash/process_human_topo.sh <base-name-of-topology> <directory> <number-routers> <allowed-number-escape-vns>
# e.g. "source ./bash/process_human_topo.sh kite_small ./topologies_and_routing/topo_maps/20r 20 2"

# generate list of all paths
python3 python_scripts/routing.py --alg naive_all --filename ${2}/${1}.map

python3 python_scripts/parse...

python3 python_scripts/vnallocator.py --filename ${2}/${1}.map --min_n_vns 2 --max_n_vns 2 --alg_type nndbt --lb_type none --max_retries 50
python3 python_scripts/vnallocator.py --filename ${2}/${1}.map --min_n_vns ${4} --max_n_vns ${4} --alg_type lpbt --lb_type hops --max_retries 50
