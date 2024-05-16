# netsmith_icpp24
Repository for ICPP 2024 artifact submission

Purdue University
Conor Green and Mithuna Thottethodi

# General Flow

All paths relative to main netsmith_icpp24 directory


Assuming all tools set up correctly and running from netsmith_icpp24 directory, this will create, route, avoid deadlocks, and simulate a simple (twelve router, four port) topology...
```
cd gurobi
source setup.sh
./bin/auto_top -of my_12r_topo
cp files/optimal_solutions/my_12r_topo.map ../implementation/topologies_and_routing/topo_maps/
cd ../implementation/
source ./bash/analyze_topo.sh topologies_and_routing/topo_maps/my_12r_topo.map files/static_metrics/my_12r_topo_rpt.txt
source ./bash/process_topo_mclb.sh my_12r_topo ./topologies_and_routing/topo_maps/ 12 4
cp ./topologies_and_routing/topo_maps/my_12r_topo.map ../gem5/topologies_and_routing/topo_maps/
cp ./topologies_and_routing/nr_lists/my_12r_topo_mclb.nrl ../gem5/topologies_and_routing/nr_lists/
cp ./topologies_and_routing/vn_maps/my_12r_topo_mclb_hops_4vns.vn ../gem5/topologies_and_routing/vn_maps/
cd ../gem5

```



% \begin{itemize}
%     \item .map - these are one-hot maps of router topologies
%     \item .rallpaths - raw list of all paths between all source, destination pairs
%     \item .paths - selected list of paths (one path per flow) for all source, destination pairs
%     \item .nrl - ``next router list'' is a list of 2D routing tables of next hop for each router in the network
%     \item .vn - ``virtual network'' map is a 2D table of the designated escape virtual network for a source, destination pair
% \end{itemize}




#### 1) Gurobi

Write and/or solve model

inputs:
- ./gurobi/prob_defs/

outputs:
- ./gurobi/files/models/
- ./gurobi/files/running_solutions
- ./gurobi/files/optimal_solutions

#### 2) Open Source Solvers

Use open source solver(s) to read and solve models

inputs:
- ./gurobi/files/models/

outputs:
- ./open_source_solvers/files/solutions

#### 3) Implementation Details

Analyze, route, and allocate escape VNs

inputs:
- ./topologies_and_routing/topo_maps/

outputs:
- ./topologies_and_routing/metrics/
- ./topologies_and_routing/nr_lists/
- ./topologies_and_routing/vn_maps/

#### 4) Simulate

Simulate synthetic and real workloads in gem5

inputs:
- ./topologies_and_routing/topo_maps/
- ./topologies_and_routing/nr_lists/
- ./topologies_and_routing/vn_maps/

outputs:
- ./gem5/synth_outputs/
- ./gem5/parsec_outputs/


## 1) Gurobi

Generate Large (20r) NetSmith topology
```
./gurobi/bin/auto_top -if ./files/prob_defs/dev_20r_4p_25ll.dat -of ns_l_latop --model_type w_hop --max_diam 20 --uni_links -o avg_hops --use_run_sol --concurrent_mip --heuristic_ratio 0.8 --mip_focus 1
```

If completes optimal the map will be in ./files/optimal_solutions and/or running solutions (--use_run_sol) in ./files/runnings_solutions

Generate Large (20r) NetSmith model file (.lp) that doesn't use any general or SOS constraints
```
./gurobi/bin/auto_top -if ./files/prob_defs/dev_20r_4p_25ll.dat --max_diam 20 --uni_links -o avg_hops --simple_model --no_solve --use_lp_model
```

Script to make a lot of models
```
python3 python_scripts/make_all_models.py
```

If more problem defintions need to be made then
```
python3 python_scripts/write_prob_defs.py
```


## 2) Open Source Solvers

GLPK
```
glpsol -h
```

## 3) Implementation Details

### NoI

#### Static Metrics

```
python3 implementation/python_scripts/static_metrics.py --filename 
```

#### Visualizer

```
python3 implementation/python_scripts/visualizer.py --directed --filename open_source_solvers/SYMPHONY/outputs/20r_4p_l_ulinks.map
```


#### Route

MCLB

```
./bin/mclb -t ../implementation/topologies_and_routing/topo_maps/64r/ours/ns_l_latop_64r.map --num_routers 64 -pl ../implementation/topologies_and_routing/allpath_lists/ns_l_latop_64r.rallpaths -of ns_l_latop_64r
```


#### Escape VNs
```

```




### NoC + NoI = NoCI...

#### Convert
```

```

#### Reroute


## 4) Simulation

#### Synthetic

```
python3 python_scripts/run_synth.py -s 2147483647 --mixedfreq_only --mclb_only --inj_end 0.2 --inj_start 0.005 --inj_step 0.005 --n_evn 4 --tot_vcs 6 --hops_lb_only --coh_only --sys_clk 4.0 --dir_mult 4
```

or individually...
```
export _TMP_OUTDIR="./gem5/synth_outputs/simple/2b/mixed/uniform/mclb_hops_4_6_40cpus_4xdirs_4.0GHz/coh/ns_m_scop/0_095/"
export _TMP_FLAGS="--noc_clk 4.0GHz --sys-clock 4.0GHz --ruby-clock 4.0GHz --noi_clk 3.0GHz --ruby --mem_or_coh coh --mem-size 320000000 --num-dirs 160 --num-cpus 40 --network garnet --mem-type SimpleMemory --routing-algorithm 2 --use_escape_vns --synth_traffic --vcs-per-vnet 6 --evn_deadlock_partition 2 --evn_n_deadlock_free 1 --evn_min_n_deadlock_free 4 --topology EscapeVirtualNetworks --noi_routers 20"
export _TMP_TOPO="./topologies_and_routing/topo_maps/20r/ns_l_latop.map"
export _TMP_NRL="./topologies_and_routing/nr_lists/20r/ns_m_latop_mclb.nrl"
export _TMP_VN="./topologies_and_routing/vn_maps/20r/ns_m_latop_mclb_hops_4vns.vn"

./gem5/build/Garnet_standalone/gem5.fast -d $_TMP_OUTDIR ./gem5/configs/auto_top/auto_top_synth.py --sim-cycles 2147483647 --injectionrate 0.095  --router_map_file $_TMP_TOPO --flat_nr_map_file $_TMP_NRL --flat_vn_map_file $_TMP_VN $_TMP_FLAGS
```



#### PARSEC

```
export _TMP_OUTDIR="./gem5/parsec_results/noci_32GBxDDR4_6envs_38GHz_2MBl2_allthreads_64lwidth_sameflowpriority_lwbufadj/100mwarmup_100msimul/freqmine/ns_m_scop_noci_picky_cohmem_prioritized_doubley_memory_mclb_hops/"
export _TMP_FLAGS="-r 1 --checkpoint-dir ./parsec_noci_checkpoints/roi_checkpoint/system_5/freqmine --topology FS_NoCI_EscapeVirtualNetworks --noi_routers 20 --noc_clk 3.8GHz --sys-clock 3.8GHz --cpu-clock 3.8GHz --ruby-clock 3.8GHz --noi_clk 3.0GHz --num-cpus 64 --mem_or_coh mem --num-dirs 32 --caches --num-l2caches 64 --l2_size 2MB --num_chiplets 4 --mem-size 32GB --ruby --network garnet --link-width-bits 64 --kernel parsec_disk_image/vmlinux-5.4.49 --disk-image parsec_disk_image/x86-parsec --cpu-type X86O3CPU --routing-algorithm 2 --use_escape_vns --vcs-per-vnet 10 --evn_n_deadlock_free 1 --evn_min_n_deadlock_free 6 --evn_deadlock_partition 4 --mem-type DDR4_2400_16x4"
export _TMP_TOPO="./topologies_and_routing/topo_maps/noci/ns_l_latop_noci.map"
export _TMP_NRL="./topologies_and_routing/nr_lists/noci/ns_l_latop_noci_picky_cohmem_prioritized_doubley_memory_mclb.nrl"
export _TMP_VN="./topologies_and_routing/vn_maps/noci/ns_l_latop_noci_picky_cohmem_prioritized_doubley_memory_mclb_hops_6vns.vn"

./gem5/build/X86/gem5.fast -d $_TMP_OUTDIR ./gem5/configs/auto_top/auto_top_fs_v3.py -I 100000000 --insts_after_warmup 100000000 --benchmark_parsec freqmine --router_map_file $_TMP_TOPO --flat_nr_map_file $_TMP_NRL --flat_vn_map_file $_TMP_VN $_TMP_FLAGS
```



## 5) Analysis

#### Parse Synthetic

#### Graph Synthetic

#### Parse PARSEC

#### Graph PARSEC


#### DSENT

```
cd ./ext/dsent
cmake ./
make
```
