# Simulation

Original gem5 README is "README" (no .md)


## Setup and Init

Requires
- linux kernel (public) : 
- PARSEC disk image (public) :
- PARSEC checkpoints 
- 

## Synthetic


### Simulation

```
python3 python_scripts/run_synth.py --one_topo topologies_and_routing/topo_maps/my_12r_topo.map --n_routers 12 --nr_list ./topologies_and_routing/nr_lists/my_12r_topo_mclb.nrl --vn_map topologies_and_routing/vn_maps/my_12r_topo_mclb_hops_4vns.vn -s 1000 --mixedfreq_only --inj_end 0.2 --inj_start 0.01 --inj_step 0.01 --n_evn 4 --tot_vcs 6 --coh_only --sys_clk 4.0 --dir_mult 4 --noi_freq 2.7GHz
```

or for a single injection rate
```
export _TMP_OUTDIR="./gem5/synth_outputs/simple/2b/mixed/uniform/mclb_hops_4_6_40cpus_4xdirs_4.0GHz/coh/ns_m_scop/0_095/"
export _TMP_FLAGS="--noc_clk 4.0GHz --sys-clock 4.0GHz --ruby-clock 4.0GHz --noi_clk 3.0GHz --ruby --mem_or_coh coh --mem-size 320000000 --num-dirs 160 --num-cpus 40 --network garnet --mem-type SimpleMemory --routing-algorithm 2 --use_escape_vns --synth_traffic --vcs-per-vnet 6 --evn_deadlock_partition 2 --evn_n_deadlock_free 1 --evn_min_n_deadlock_free 4 --topology EscapeVirtualNetworks --noi_routers 20"
export _TMP_TOPO="./topologies_and_routing/topo_maps/20r/ns_l_latop.map"
export _TMP_NRL="./topologies_and_routing/nr_lists/20r/ns_m_latop_mclb.nrl"
export _TMP_VN="./topologies_and_routing/vn_maps/20r/ns_m_latop_mclb_hops_4vns.vn"

./gem5/build/Garnet_standalone/gem5.fast -d $_TMP_OUTDIR ./gem5/configs/auto_top/auto_top_synth.py --sim-cycles 2147483647 --injectionrate 0.095  --router_map_file $_TMP_TOPO --flat_nr_map_file $_TMP_NRL --flat_vn_map_file $_TMP_VN $_TMP_FLAGS
```


### Parse and Graph

```
python3 python_scripts/parse_synth_results.py synth_outputs/simple/1k/ synth_outputs/csvs/my_topo_1k.csv

python3 python
```



## PARSEC

### Simulation

```
export _TMP_OUTDIR="./parsec_results/100mwarmup_100msimul/freqmine/ns_m_scop_noci_picky_cohmem_prioritized_doubley_memory_mclb_hops/"
export _TMP_FLAGS="-r 1 --checkpoint-dir ./parsec_noci_checkpoints/roi_checkpoint/system_5/freqmine --topology FS_NoCI_EscapeVirtualNetworks --noi_routers 20 --noc_clk 3.8GHz --sys-clock 3.8GHz --cpu-clock 3.8GHz --ruby-clock 3.8GHz --noi_clk 3.0GHz --num-cpus 64 --mem_or_coh mem --num-dirs 32 --caches --num-l2caches 64 --l2_size 2MB --num_chiplets 4 --mem-size 32GB --ruby --network garnet --link-width-bits 64 --kernel parsec_disk_image/vmlinux-5.4.49 --disk-image parsec_disk_image/x86-parsec --cpu-type X86O3CPU --routing-algorithm 2 --use_escape_vns --vcs-per-vnet 10 --evn_n_deadlock_free 1 --evn_min_n_deadlock_free 6 --evn_deadlock_partition 4 --mem-type DDR4_2400_16x4"
export _TMP_TOPO="./topologies_and_routing/topo_maps/noci/ns_l_latop_noci.map"
export _TMP_NRL="./topologies_and_routing/nr_lists/noci/ns_l_latop_noci_picky_cohmem_prioritized_doubley_memory_mclb.nrl"
export _TMP_VN="./topologies_and_routing/vn_maps/noci/ns_l_latop_noci_picky_cohmem_prioritized_doubley_memory_mclb_hops_6vns.vn"

./gem5/build/X86/gem5.fast -d $_TMP_OUTDIR ./gem5/configs/netsmith/netsmith_parsec.py -I 100000000 --insts_after_warmup 100000000 --benchmark_parsec freqmine --router_map_file $_TMP_TOPO --flat_nr_map_file $_TMP_NRL --flat_vn_map_file $_TMP_VN $_TMP_FLAGS
```




## Paper figures

### Fig. 5

20r synth

### Fig. 6

PARSEC

### Fig. 8

64r synth