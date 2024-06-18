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
The first objective is solved by providing the results and scripts to plot for the 20/64/84 router topologies utilized in the paper.
The second objective is solved by running through an example (new) twenty router topology.

### Computation and Time Requirements

#### Compute Resources
- At least 32GB for gem5 PARSEC simulation
- Multiple CPUs
    - Ability to parallelize workloads
    - Varies greatly depending on resource. Left up to end-user on how to run the provided bash scripts
- Gurobi License
    - Otherwise must use open-source solvers

#### Expected Time
- Compilation of Gurobi takes seconds
- Installation of Python libraries take minutes
- Compilation/building of gem5 simulator(s) (Garnet_standalone and X86) takes hours
- Routing, deadlock avoidance for NoI and/or NoCI take up to ten minutes
- Synthetic simulations for a single injection rate takes ~3 hours
    - For a single topology, to sweep and find saturation point takes 10-20 injection rates
- Longest PARSEC benchmark, swaptions, takes ~3 days per topology/run



### Virtual Machine

A .voa was not able to upload to Zenodo... Kept failing mid-upload after many attempts

username: netsmith
password: password

### Large Files

Large files on Zenodo
- (Full System PARSEC Checkpoints for NetSmith gem5 Simulation : https://zenodo.org/records/11529546
    - use "version 2" since first upload was missing fluidanimate
- Full System PARSEC Disk Image and Kernel for NetSmith gem5 Simulation : https://zenodo.org/records/11529766
- NetSmith and LPBT models for Open-Source Solvers : https://zenodo.org/records/11861900 

## Setup and Installation

For a user first using the repo. First, download all large files (checkpoints, disk image, and models) from above and place all four tars in the main repository directory. In general, requires sudo permissions

```
# opens and moves files
source uncompress.sh

# install system level packages
source install_tools.sh
source setup_vm.sh


# (optional) build gurobi
cd topology_generation/gurobi
source init.sh
make
cd ../..

# build open-source
cd topology_generation/open_source_solvers
source init.sh
cd ../..

# build gem5
cd auto_top_gem5
source build.sh
cd ..

# build dsent
cd dsent
source build.sh
source setup.sh
cd ..
```

Within every directory, when you want to run something...
```
source setup.sh
```

### Directories

#### 1) ./topology_generation
Code for a) Gurobi and b) open-source generation of topologies. Within directory, README for instructions and bash scripts for examples

a)
- inputs:
    - ./prob_defs/

- outputs:
    - ./files/models/
    - ./files/running_solutions
    - ./files/optimal_solutions

b)
- inputs:
    - ./models/

- outputs:
    - ./files/solutions

#### 2) ./implementation
Code for static analysis; routing with MCLB, LPBT, or "no double-back turns;" and deadlock avoidance. Within directory, README for instructions and bash scripts for examples

- inputs:
    - ./topologies_and_routing/topo_maps/

- outputs:
    - ./topologies_and_routing/metrics/
    - ./topologies_and_routing/nr_lists/
    - ./topologies_and_routing/vn_maps/

#### 3) ./auto_top_gem5
Code for synthetic simulation, parsing, and graphing. Within directory, README for instructions and bash scripts for examples and figure generation

- inputs:
    - ./topologies_and_routing/topo_maps/
    - ./topologies_and_routing/nr_lists/
    - ./topologies_and_routing/vn_maps/

- outputs:
    - ./synth_outputs/

#### 4) ./implementation
Code for creating a NoCI (84r = 64r NoC + 20r NoI) topology from a NoI (20r) topology; routing; and deadlock avoidance. Within directory, README for instructions and bash scripts for examples

- inputs:
    - ./topologies_and_routing/topo_maps/20r

- outputs:
    - ./topologies_and_routing/topo_maps/noci
    - ./topologies_and_routing/nr_lists/
    - ./topologies_and_routing/vn_maps/

#### 5) ./auto_top_gem5
Code and resources for full-system PARSEC simulation, parsing, and graphing. Within directory, README for instructions and bash scripts for examples and figure generation

- inputs:
    - ./topologies_and_routing/topo_maps/
    - ./topologies_and_routing/nr_lists/
    - ./topologies_and_routing/vn_maps/

- outputs:
    - ./parsec_outputs/

#### 6) ./dsent
Code for parsing and calculating area/power usage from PARSEC stats. Within directory, README for instructions and bash scripts for examples and figure generation

- inputs:
    - ./parsec_outputs/

- outputs:
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

# (optional) resimulate
source bash/run_synth_20r_prev_test.sh
source bash/run_synth_20r_ns_test.sh

# (optional) reparse
source bash/parse_synth_20r_fig5.sh

source bash/plot_synth_20r_fig5.sh
```

#### Figure 6

```
cd auto_top_gem5

# (optional) resimulate
source bash/run_parsec_prev_test.sh
source bash/run_parsec_ns_test.sh

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

# (optional) resimulate
source bash/run_synth_64r_prev_test.sh
source bash/run_synth_64r_ns_test.sh

# (optional) reparse
source bash/parse_synth_64r_fig8.sh

source bash/plot_synth_64r_fig8.sh
```

## New NoI Topology Generation and Simulation

Assuming all tools set up correctly, models were unzipped, and running from netsmith_icpp24 directory. These commands will create a 20 router, 4 port topology as described in the paper. Gurobi will run for 1 minute to create a new topology. Next, the topology will be routed, made deadlock free, and simulated with synthetic traffic. Then create NoI + NoC = NoCI topology, route, deadlock avoid, and simulate PARSEC for 1000 instructions. After, the stats will be read for power/area estimates. 

#### Topology Generation

Go to ./topology_generation/gurobi or ./topology_generation/open_source_solvers and 

```
# 1
cd topology_generation/gurobi
source bash/create_netsmith.sh 20 large latency
cp files/optimal_solutions/my_20r_4p_25ll_avghops_topo.map ../../implementation/topologies_and_routing/topo_maps/

# 1 (alternative)
cd topology_generation/open_source_solvers
source bash/create_netsmith.sh 20 large latency
cp files/solutions/my_20r_4p_25ll_avghops_topo.map ../../implementation/topologies_and_routing/topo_maps/
```

#### Routing and Deadlock Avoidance

```
# 2
cd ../../implementation/

# get static metrics
source ./bash/analyze_topo.sh topologies_and_routing/topo_maps/my_20r_4p_25ll_avghops_topo.map files/static_metrics/my_20r_4p_25ll_avghops_topo.txt

# route and deadlock avoid (bash for convenience)
# with gurobi
source bash/process_topo_mclb_withgurobi.sh my_20r_4p_25ll_avghops_topo topologies_and_routing/topo_maps/ 20 4


# without gurobi
source bash/process_topo_mclb.sh my_20r_4p_25ll_avghops_topo topologies_and_routing/topo_maps/ 20 4


cp ./topologies_and_routing/topo_maps/my_20r_4p_25ll_avghops_topo.map ../auto_top_gem5/topologies_and_routing/topo_maps/
cp ./topologies_and_routing/nr_lists/my_20r_4p_25ll_avghops_topo_mclb.nrl ../auto_top_gem5/topologies_and_routing/nr_lists/
cp ./topologies_and_routing/vn_maps/my_20r_4p_25ll_avghops_topo_mclb_hops_4vns.vn ../auto_top_gem5/topologies_and_routing/vn_maps/

```

#### Synthetic Simulation

```
# 3
cd ../auto_top_gem5
# sweeps injection rates for coherence and memory traffic
source ./bash/synth_inj_sweep_topo.sh ./topologies_and_routing/topo_maps/my_20r_4p_25ll_avghops_topo.map ./topologies_and_routing/nr_lists/my_20r_4p_25ll_avghops_topo_mclb.nrl ./topologies_and_routing/vn_maps/my_20r_4p_25ll_avghops_topo_mclb_hops_4vns.vn 2.7GHz 4 6 20 40 4 0.01 0.2 0.01 2147483647
```

#### Creation of NoCI
```
# 4
cd ../implementation

python3 python_scripts/gen_NoCI_map.py --filename topologies_and_routing/topo_maps/my_20r_4p_25ll_topo.map
# creates topology "my_20r_4p_25ll_avghops_topo_noci" in topologies_and_routing/topo_maps/noci

# allow 6 escape vns
source bash/process_noci_topo_mclb.sh my_20r_4p_25ll_avghops_topo_noci topologies_and_routing/topo_maps/noci 6


cp ./topologies_and_routing/topo_maps/noci/my_20r_4p_25ll_avghops_topo_noci.map ../auto_top_gem5/topologies_and_routing/topo_maps/noci
cp ./topologies_and_routing/nr_lists/my_20r_4p_25ll_avghops_topo_noci_picky_mclb_cohmem_prioritized_doubley_memory.nrl ../auto_top_gem5/topologies_and_routing/nr_lists
cp ./topologies_and_routing/vn_maps/my_20r_4p_25ll_avghops_topo_noci_picky_mclb_cohmem_prioritized_doubley_memory_hops_6vns.vn ../auto_top_gem5/topologies_and_routing/vn_maps
```

#### Full-System Simulation

```
# 5
cd ../auto_top_gem5


source bash/run_parsec_one_topo.sh my_20r_4p_25ll_avghops_topo_noci my_20r_4p_25ll_avghops_topo_noci_picky_mclb_cohmem_prioritized_doubley_memory my_20r_4p_25ll_avghops_topo_noci_picky_mclb_cohmem_prioritized_doubley_memory_hops_6vns 6 2.7

cp -r ./parsec_results/noci_32GBxDDR4/100000000warmup_100000000simul/swaptions/my_20r_4p_25ll_avghops_topo_noci_picky_mclb_cohmem_prioritized_doubley_memory_hops_6vns/ ../dsent/swaptions_100mwarmup_100msimul_20r_4p_25ll_avghops_topo_noci_picky_cohmem_prioritized_doubley_memory_mclb_hops
```

#### Power Analysis
```
# 6
cd ../dsent

python2 noci_power_area.py ./swaptions_100mwarmup_100msimul_20r_4p_25ll_avghops_topo_noci_picky_cohmem_prioritized_doubley_memory_mclb_hops router.cfg electrical-link.cfg >> ./dsent_results/log.txt
cat ./dsent_results/log.txt
```




