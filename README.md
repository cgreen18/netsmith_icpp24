# netsmith_icpp24
Repository for ICPP 2024 artifact submission

Conor Green and Mithuna Thottethodi. Purdue University 2024

## Repository Organization

All paths relative to main netsmith_icpp24 directory

This flow completes
1. Topology generation
2. Routing and deadlock avoidance
3. Synthetic simulation
4. NoCI (full system) conversion, routing, and deadlock avoidance
5. PARSEC simulation
6. DSENT analysis

The repository serves two purposes. First, to reproduce the results given in the submitted paper and second, to give an example of using the software to generate and test topologies.
The first objective is solved by providing the results and scripts to plot for the twentry router topologies utilized in the paper.
The second objective is solved by running through an example simple, twelve router topology. A smaller topology is used for speed.

### Directories

#### 1) ./topology_generation
Code for a) Gurobi and b) open-source generation of topologies. Within directory, README for instructions and bash scripts for examples

a)
inputs:
- ./prob_defs/

outputs:
- ./files/models/
- ./files/running_solutions
- ./files/optimal_solutions

b)
inputs:
- ./models/

outputs:
- ./files/solutions

#### 2) ./implementation
Code for static analysis; routing with MCLB, LPBT, or "no double-back turns;" and deadlock avoidance. Within directory, README for instructions and bash scripts for examples

inputs:
- ./topologies_and_routing/topo_maps/

outputs:
- ./topologies_and_routing/metrics/
- ./topologies_and_routing/nr_lists/
- ./topologies_and_routing/vn_maps/

#### 3) ./auto_top_gem5
Code for synthetic simulation, parsing, and graphing. Within directory, README for instructions and bash scripts for examples and figure generation

inputs:
- ./topologies_and_routing/topo_maps/
- ./topologies_and_routing/nr_lists/
- ./topologies_and_routing/vn_maps/

outputs:
- ./synth_outputs/

#### 4) ./implementation
Code for creating a NoCI topology from a NoI (20r) topology; routing; and deadlock avoidance. Within directory, README for instructions and bash scripts for examples

#### 5) ./auto_top_gem5
Code and resources for full-system PARSEC simulation, parsing, and graphing. Within directory, README for instructions and bash scripts for examples and figure generation

inputs:
- ./topologies_and_routing/topo_maps/
- ./topologies_and_routing/nr_lists/
- ./topologies_and_routing/vn_maps/

outputs:
- ./parsec_outputs/

#### 6) ./dsent
Code for parsing and calculating area/power usage from PARSEC stats. Within directory, README for instructions and bash scripts for examples and figure generation

inputs:
- ./parsec_outputs/

outputs:
- ./dsent_results

### File Types

Within this project, a few custom file types are used
-  .map - these are one-hot maps of router topologies
-  .rallpaths - raw list of all paths between all source, destination pairs
-  .paths - selected list of paths (one path per flow) for all source, destination pairs
-  .nrl - ``next router list'' is a list of 2D routing tables of next hop for each router in the network
-  .vn - ``virtual network'' map is a 2D table of the designated escape virtual network for a source, destination pair

## Paper Figures

#### Figure 5

```
cd auto_top_gem5

# (optional) reparse
source bash/parse_synth_20r_fig5.sh

source bash/plot_synth_20r_fig5.sh
```

#### Figure 6

```
cd auto_top_gem5

# (optional) reparse
source bash/parse_parsec_fig6.sh

source bash/plot_parsec_fig6.sh
```

#### Figure 7

```
cd dsent

# (optional) reparse
source bash/calculate_results_fig7.sh

source bash/plot_figure_fig7.sh
```

#### Figure 8

```
cd auto_top_gem5

# (optional) reparse
source bash/parse_synth_64r_fig8.sh

source bash/plot_synth_64r_fig8.sh
```

## Virtual Machine

A .vdi is available at: TODO

username: netsmith
password: password

## Large Files

Large files on Zenodo
- Full System PARSEC Checkpoints for NetSmith gem5 Simulation : https://zenodo.org/records/11529546
- Full System PARSEC Disk Image and Kernel for NetSmith gem5 Simulation : https://zenodo.org/records/11529766

## All Commands for a Full Run Through


Assuming all tools set up correctly, models were unzipped, and running from netsmith_icpp24 directory. These commands will create a 20 router, 4 port topology as described in the paper. Gurobi will run for 1 minute to create a new topology. Next, the topology will be routed, made deadlock free, and simulated with synthetic traffic. Then create NoI + NoC = NoCI topology, route, deadlock avoid, and simulate PARSEC for 1000 instructions. After, the stats will be read for power/area estimates. 
```
# 1
cd topology_generation/gurobi
source bash/create_netsmith.sh 20 large latency
cp files/optimal_solutions/my_20r_4p_25ll_avg_hops_topo.map ../../implementation/topologies_and_routing/topo_maps/

# 1 (alternative)
cd topology_generation/open_source_solvers
source bash/create_netsmith.sh 20 large latency
cp files/solutions/my_20r_4p_25ll_avg_hops_topo.map ../../implementation/topologies_and_routing/topo_maps/



# 2
cd ../../implementation/
source ./bash/analyze_topo.sh topologies_and_routing/topo_maps/my_20r_4p_25ll_avg_hops_topo.map files/static_metrics/my_20r_4p_25ll_avg_hops_topo.txt
source ./bash/process_topo_mclb.sh my_20r_4p_25ll_avg_hops_topo ./topologies_and_routing/topo_maps/ 20 4
cp ./topologies_and_routing/topo_maps/my_20r_4p_25ll_avg_hops_topo.map ../auto_top_gem5/topologies_and_routing/topo_maps/
cp ./topologies_and_routing/nr_lists/my_20r_4p_25ll_avg_hops_topo_mclb.nrl ../auto_top_gem5/topologies_and_routing/nr_lists/
cp ./topologies_and_routing/vn_maps/my_20r_4p_25ll_avg_hops_topo_mclb_hops_4vns.vn ../auto_top_gem5/topologies_and_routing/vn_maps/

# 3
cd ../auto_top_gem5
python3 python_scripts/run_synth.py --one_topo topologies_and_routing/topo_maps/my_20r_4p_25ll_topo.map --n_routers 20 --nr_list topologies_and_routing/nr_lists/my_20r_4p_25ll_topo_mclb.nrl --vn_map topologies_and_routing/vn_maps/my_20r_4p_25ll_topo_mclb_hops_4vns.vn --inj_end 0.2 --inj_start 0.01 --inj_step 0.01 --n_evn 4 --tot_vcs 6 --coh_only --noi_freq 2.7GHz

# 4
cd ../implementation
python3 python_scripts/gen_NoCI_map.py --filename topologies_and_routing/topo_maps/my_20r_4p_25ll_topo.map
python3 python_scripts/routing.py --alg all_picky --filename ./topologies_and_routing/topo_maps/noci/my_20r_4p_25ll_topo_noci.map
../gurobi/bin/noci_mclb -t ./topologies_and_routing/topo_maps/noci/my_20r_4p_25ll_topo_noci.map -pl topologies_and_routing/allpath_lists/my_20r_4p_25ll_topo_noci_picky.rallpaths --num_routers 84 -of my_20r_4p_25ll_topo_noci_picky_mclb_cohmem_prioritized_doubley_memory --cohmem_prioritized --doubley_memory
python3 python_scripts/mclb_pruner.py ./topologies_and_routing/routepath_lists/my_20r_4p_25ll_topo_noci_picky_mclb_cohmem_prioritized_doubley_memory.paths
python3 python_scripts/routing.py --convert_pathlist --pathlist ./topologies_and_routing/routepath_lists/my_20r_4p_25ll_topo_noci_picky_mclb_cohmem_prioritized_doubley_memory.paths
python3 python_scripts/vnallocator.py --filename ./topologies_and_routing/topo_maps/noci/my_20r_4p_25ll_topo_noci.map --nr_list ./topologies_and_routing/nr_lists/my_20r_4p_25ll_topo_noci_picky_mclb_cohmem_prioritized_doubley_memory.nrl --path_list ./topologies_and_routing/routepath_lists/my_20r_4p_25ll_topo_noci_picky_mclb_cohmem_prioritized_doubley_memory.paths --min_n_vns 6 --max_n_vns 6 --max_retries 50 --alg_type mclb_cohmem_prioritized_doubley_memory --out_vn_name topologies_and_routing/vn_maps/my_20r_4p_25ll_topo_noci_picky_mclb_cohmem_prioritized_doubley_memory_hops_6vns.vn
cp ./topologies_and_routing/topo_maps/noci/my_20r_4p_25ll_topo_noci.map ../auto_top_gem5/topologies_and_routing/topo_maps/noci
cp topologies_and_routing/nr_lists/my_20r_4p_25ll_topo_noci_picky_mclb_cohmem_prioritized_doubley_memory.nrl ../auto_top_gem5/topologies_and_routing/nr_lists
cp topologies_and_routing/vn_maps/my_20r_4p_25ll_topo_noci_picky_mclb_cohmem_prioritized_doubley_memory_hops_6vns.vn ../auto_top_gem5/topologies_and_routing/vn_maps

# 5
cd ../auto_top_gem5
export _TMP_OUTDIR="./parsec_results/noci_32GBxDDR4_6envs_38GHz_2MBl2_allthreads_64lwidth/1kwarmup_1kmsimul/freqmine/my_20r_4p_25ll_topo_noci_picky_cohmem_prioritized_doubley_memory_mclb_hops/"
export _PARSEC_IMG_DIR="/home/yara/mithuna2/green456/netsmith_autotop/auto_top_gem5/parsec_disk_image"
export _PARSEC_CHKPT_DIR="/home/yara/mithuna2/green456/netsmith_autotop/auto_top_gem5/parsec_noci_checkpoints"
export _TMP_FLAGS="-r 1 --checkpoint-dir $_PARSEC_CHKPT_DIR/roi_checkpoint/system_5/freqmine --topology FS_NoCI_EscapeVirtualNetworks --noi_routers 20 --noc_clk 3.8GHz --sys-clock 3.8GHz --cpu-clock 3.8GHz --ruby-clock 3.8GHz --noi_clk 3.0GHz --num-cpus 64 --mem_or_coh mem --num-dirs 32 --caches --num-l2caches 64 --l2_size 2MB --num_chiplets 4 --mem-size 32GB --ruby --network garnet --link-width-bits 64 --kernel $_PARSEC_IMG_DIR/vmlinux-5.4.49 --disk-image $_PARSEC_IMG_DIR/x86-parsec --cpu-type X86O3CPU --routing-algorithm 2 --use_escape_vns --vcs-per-vnet 10 --evn_n_deadlock_free 1 --evn_min_n_deadlock_free 6 --evn_deadlock_partition 4 --mem-type DDR4_2400_16x4"
export _TMP_TOPO="./topologies_and_routing/topo_maps/noci/my_20r_4p_25ll_topo_noci.map"
export _TMP_NRL="./topologies_and_routing/nr_lists/my_20r_4p_25ll_topo_noci_picky_mclb_cohmem_prioritized_doubley_memory.nrl"
export _TMP_VN="./topologies_and_routing/vn_maps/my_20r_4p_25ll_topo_noci_picky_mclb_cohmem_prioritized_doubley_memory_hops_6vns.vn"
./build/X86/gem5.fast -d $_TMP_OUTDIR ./configs/netsmith/netsmith_parsec.py -I 1000 --insts_after_warmup 1000 --benchmark_parsec freqmine --router_map_file $_TMP_TOPO --flat_nr_map_file $_TMP_NRL --flat_vn_map_file $_TMP_VN $_TMP_FLAGS
cp -r $_TMP_OUTDIR ../dsent/freqmine_1kwarmup_1kmsimul_20r_4p_25ll_topo_noci_picky_cohmem_prioritized_doubley_memory_mclb_hops

# 6
cd ../dsent
python2 noci_power_area.py ./freqmine_1kwarmup_1kmsimul_20r_4p_25ll_topo_noci_picky_cohmem_prioritized_doubley_memory_mclb_hops router.cfg electrical-link.cfg >> ./dsent_results/log.txt
```
