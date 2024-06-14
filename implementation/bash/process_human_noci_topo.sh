
#!/bin/bash


# usage: ./bash/process_human_topo.sh <base-name-of-topology> <directory> <number-routers> <allowed-number-escape-vns>
# e.g. "source ./bash/process_human_topo.sh kite_small_noci ./topologies_and_routing/topo_maps/noci

# generate list of all paths
python3 python_scripts/routing.py --alg naive_ndbt_picky --filename ${2}/${1}.map

python3 python_scripts/vnallocator_ndbt.py --filename ${2}/${1}.map --alg_type nndbt_picky --lb_type none --skip_verification
