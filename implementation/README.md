# Implementation

To calculate graph metrics of topologies, route, avoid deadlocks, and extend NoI to NoCI (NoC + NoI)



#### Initialization and Setup

First time using this directory
```
source init.sh

python3 -m venv venv_implementation
source venv_implementation/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

To set up Python libraries
```
source venv_implementation/bin/activate
```

Make MCLB for Gurobi and setup licenses
```
cd gurobi
make mclb
cd ..
source setup.sh
```

## Normal Graphs (non-NoCI)

Use an example graph in topologies_and_routing/topo_maps/autotop_r12_p4_ll25_avghops.map

#### Static Metrics

Measure values such as diameter and average hops
```
python3 python_scripts/static_metrics.py --filename topologies_and_routing/topo_maps/autotop_r12_p4_ll25_avghops.map
```

#### Visualizer

```
python3 python_scripts/visualizer.py --directed --filename topologies_and_routing/topo_maps/autotop_r12_p4_ll25_avghops.map
```

### Route

#### Route MCLB

```
./bin/mclb -t topologies_and_routing/topo_maps/autotop_r12_p4_ll25_avghops.map --num_routers 12 -pl topologies_and_routing/allpath_lists/autotop_r12_p4_ll25_avghops.rallpaths -of autotop_r12_p4_ll25_avghops

python3 python_scripts/mclb_pruner.py ./topologies_and_routing/routepath_lists/autotop_r12_p4_ll25_avghops.paths
python3 python_scripts/routing.py --convert_pathlist --pathlist ./topologies_and_routing/routepath_lists/autotop_r12_p4_ll25_avghops.paths
```


#### Route NNDBT (human/expert heuristic)

ndbt and select random => nndbt
```
python3 python_scripts/routing.py --alg naive_ndbt --filename topologies_and_routing/topo_maps/kite_large.map
```


### Deadlock Avoidance

#### Escape VNs (~DFSSSP)

```
python3 python_scripts/vnallocator.py --filename topologies_and_routing/topo_maps/64r/ours/ns_l_latop_64r.map --min_n_vns 4 --max_n_vns 4 --alg_type mclb --lb_type hops --max_retries 50

```


#### "No Double-Back Turns"

```
python3 python_scripts/vnallocator_ndbt.py --filename topologies_and_routing/topo_maps/noci/kite_large_noci.map --alg_type nndbt_picky --lb_type none --skip_verification
```





## NoC + NoI = NoCI

Will use example NoI topologies of ns_l_latop and kite_large. As stated in paper, we restrict paths to those that do not cross over the CDC between NoC and NoI unnecessarily and label this "picky".


#### Create NoCI from NoI

```
python_scripts/gen_NoCI_map.py --filename 
```


### Route

#### MCLB Picky

```
python3 python_scripts/routing.py --alg all_picky --filename topologies_and_routing/topo_maps/noci/ns_l_latop_noci.map

./bin/noci_mclb -t topologies_and_routing/topo_maps/noci/ns_l_latop_noci.map -pl ./files/route_allpathslists/ns_l_latop_noci.rallpaths --num_routers 84 -of ns_l_latop_noci_mclb_cohmem_prioritized_doubley_memory --cohmem_prioritized --doubley_memory
```


#### NNDBT Picky ndbt_picky and select random => nndbt_picky

```
python3 python_scripts/routing.py --alg naive_ndbt_picky --filename topologies_and_routing/topo_maps/noci/kite_large_noci.map
```

### Deadlock Avoidance


#### Escape VNs

```
python3 python_scripts/vnallocator --filename topologies_and_routing/topo_maps/noci/ns_l_latop_noci.map --min_n_vns 6 --max_n_vns 6 --alg_type mclb --lb_type hops --max_retries 50 --skip_verification
```

#### NDBT

```
python3 python_scripts/vnallocator_ndbt.py --filename topologies_and_routing/topo_maps/noci/kite_large_noci.map --alg_type nndbt_picky --lb_type none --skip_verification
```