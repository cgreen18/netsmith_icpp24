



## 3) Implementation Details

### NoI

#### Static Metrics

```
python3 implementation/python_scripts/static_metrics.py --filename 
```

#### Visualizer

```
python3 implementation/python_scripts/visualizer.py --directed --filename topologies_and_routing/topo_maps/
```


#### Route

MCLB

```
./bin/mclb -t ../implementation/topologies_and_routing/topo_maps/64r/ours/ns_l_latop_64r.map --num_routers 64 -pl ../implementation/topologies_and_routing/allpath_lists/ns_l_latop_64r.rallpaths -of ns_l_latop_64r

python3 python_scripts/mclb_pruner.py ./topologies_and_routing/routepath_lists/ns_l_latop_64r_mclb.paths
python3 python_scripts/routing.py --convert_pathlist --pathlist ./topologies_and_routing/routepath_lists/ns_l_latop_64r_mclb.paths
```


#### Escape VNs

```
python3 python_scripts/vnallocator.py --filename topologies_and_routing/topo_maps/64r/ours/ns_l_latop_64r.map --min_n_vns 4 --max_n_vns 4 --alg_type mclb --lb_type hops --max_retries 50

```




### NoC + NoI = NoCI

```
python_scripts/gen_NewNoCI_map.py
```


```
python3 python_scripts/routing.py --alg all_picky --filename topologies_and_routing/topo_maps/noci/my_20r_topo_noci.map

./bin/noci_mclb -t ./files/paper_solutions/noci/ns_l_latop_noci.map -pl ./files/route_allpathslists4/ns_l_latop_noci.rallpaths --num_routers 84 -of mclb_noci_ns_l_latop_noci_cohmem_prioritized_doubley_memory --cohmem_prioritized --doubley_memory

```
Writing to files/route_pathlists_noci_mclb/my_20r_4p_25ll_topo_noci_mclb_cohmem_prioritized_doubley_memory_mclb.paths


#### MCLB (NS and LPBT)


#### Convert
```

```

#### Reroute




#### NNDBT (human)

# ndbt_picky and select random => nndbt_picky
```
python3 python_scripts/routing.py --alg naive_ndbt_picky --filename topologies_and_routing/topo_maps/noci/kite_large_noci.map

```

output:
Wrote to ./topologies_and_routing/routepath_lists/kite_large_noci_nndbt_picky.paths
constructing nr map for # routers 84
Wrote to ./topologies_and_routing/nr_lists/kite_large_noci_nndbt_picky.nrl

```
python3 python_scripts/vnallocator_ndbt.py --filename topologies_and_routing/topo_maps/noci/kite_large_noci.map --alg_type nndbt_picky --lb_type none --skip_verification
```

