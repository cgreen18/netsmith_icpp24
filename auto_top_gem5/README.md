# Simulation

Original gem5 README is "README" (no .md)


## Setup and Init

Requires
- linux kernel (public)
- PARSEC disk image (public)
- PARSEC checkpoints (private/custom)
- building gem5

Set environment variables for DISK_IMG_DIR and CHKPT_DIR if not within ./auto_top_gem5
```
export DISK_IMG_DIR="./parsec_disk_image"
export CHKPTS_DIR="./parsec_noci_checkpoints"
```

Build with scons/scons-3 for synthetic (Garnet_standalone) and full-system (X86)
```
export N_PROCS=$(proc)
scons -j $N_PROCS ./build/Garnet_standalone/gem5.fast
scons -j $N_PROCS ./build/X86/gem5.fast
```

## Synthetic


### Simulation


#### Your 12 topo
```
python3 python_scripts/run_synth.py --one_topo topologies_and_routing/topo_maps/my_12r_topo.map --n_routers 12 --nr_list ./topologies_and_routing/nr_lists/my_12r_topo_mclb.nrl --vn_map topologies_and_routing/vn_maps/my_12r_topo_mclb_hops_4vns.vn -s 1000 --mixedfreq_only --inj_end 0.2 --inj_start 0.01 --inj_step 0.01 --n_evn 4 --tot_vcs 6 --coh_only --sys_clk 4.0 --dir_mult 4 --noi_freq 2.7GHz
```

or as bash
```
source ./bash/synth_single_topo.sh topologies_and_routing/topo_maps/my_12r_topo.map ./topologies_and_routing/nr_lists/my_12r_topo_mclb.nrl topologies_and_routing/vn_maps/my_12r_topo_mclb_hops_4vns.vn 2.7 4 6 12 24 2 0.01 0.1 0.01 1000
```

##### Paper simulations

```
source bash/run_synth_20r_prev_test.sh
source bash/run_synth_20r_ns_test.sh

source bash/run_synth_64r_prev_test.sh
source bash/run_synth_64r_ns_test.sh

```

### Parse and Graph

#### Your 12 topo

No graphing provided as it takes lots of formatting
```
python3 python_scripts/parse_synth_results.py synth_outputs/simple/1k/ synth_outputs/csvs/my_topo_1k.csv
```


#### Paper simulations
```
source bash/parse_synth_20r_fig5.sh
source bash/plot_synth_20r_fig5.sh
```


or specfiy number of instructions

## PARSEC

### Simulation


Re-run previous/expert and netsmith topologies as in paper.

##### NOTE: this will run a single simulation at a time (to avoid memory overload) but this will take a long time... Consider how you want to parallelize...
```
source bash/run_parsec_prev_test.sh
source bash/run_parsec_ns_test.sh
```

You can specify the number of instructions (simulation and warmup). For example use 1000 to test configurations and commands
```
source bash/run_parsec_prev_test.sh 1000 1000
```

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