#!/bin/bash



# expect: source bash/run_parsec_one_topo.sh my_20r_4p_25ll_avghops_topo_noci my_20r_4p_25ll_avghops_topo_noci_picky_mclb_cohmem_prioritized_doubley_memory my_20r_4p_25ll_avghops_topo_noci_picky_mclb_cohmem_prioritized_doubley_memory_hops_9vns 9 2.7 1000 1000

if [ $# -lt 5 ]; then
    echo "Must specify topology, nrl list, vn map, # escape vns and noi clk frequency"
    exit 0
fi


tot_vcs=10
deadlock_partition=$(( $tot_vcs - $4 ))


# optional CLAs
warmup_insts=100000000
simul_insts=100000000

if [ $# -eq 6 ]; then
    simul_insts="$6"

elif [ $# -eq 7 ]; then
    simul_insts="$6"
    warmup_insts="$7"

fi



# environment vars
# change as necessary
if [ -z "$DISK_IMG_DIR" ]; then
    echo "DISK_IMG_DIR is not defined. Defaulting to: ./parsec_disk_image"
    export DISK_IMG_DIR="./parsec_disk_image"

fi

if [ -z "$CHKPTS_DIR" ]; then
    echo "CHKPTS_DIR is not defined. Defaulting to: ./parsec_noci_checkpoints"
    export CHKPTS_DIR="./parsec_noci_checkpoints"

fi



# small
for bench in "blackscholes" "bodytrack" "canneal" "dedup" "facesim" "ferret" "fluidanimate" "freqmine" "raytrace" "streamcluster" "swaptions" "x264";
    do
        log_file=./parsec_results/logs/${bench}_${3}_${warmup_insts}warmup_${simul_insts}simul.out
        cmd="./build/X86/gem5.fast -d ./parsec_results/noci_32GBxDDR4/${warmup_insts}warmup_${simul_insts}simul/${bench}/${3}/ configs/netsmith/netsmith_parsec.py -I $warmup_insts --insts_after_warmup $simul_insts --benchmark_parsec ${bench} -r 1 --checkpoint-dir $CHKPTS_DIR/roi_checkpoint/system_5/${bench} --kernel $DISK_IMG_DIR/vmlinux-5.4.49 --disk-image $DISK_IMG_DIR/x86-parsec --router_map_file ./topologies_and_routing/topo_maps/noci/${1}.map --flat_vn_map_file topologies_and_routing/vn_maps/${3}.vn --flat_nr_map_file topologies_and_routing/nr_lists/${2}.nrl --noi_clk ${5}GHz --vcs-per-vnet $tot_vcs --evn_n_deadlock_free 1 --evn_min_n_deadlock_free ${4} --evn_deadlock_partition $deadlock_partition --topology FS_NoCI_EscapeVirtualNetworks --noi_routers 20 --noc_clk 3.8GHz --sys-clock 3.8GHz --cpu-clock 3.8GHz --ruby-clock 3.8GHz --num-cpus 64 --mem_or_coh mem --num-dirs 32 --caches --num-l2caches 64 --l2_size 2MB --num_chiplets 4 --mem-size 32GB --ruby --network garnet --link-width-bits 64 --cpu-type X86O3CPU --routing-algorithm 2 --use_escape_vns --mem-type DDR4_2400_16x4 > $log_file 2>&1"

        echo "Running:"
        echo "$cmd"
        # $cmd
        ./build/X86/gem5.fast -d ./parsec_results/noci_32GBxDDR4/${warmup_insts}warmup_${simul_insts}simul/${bench}/${3}/ configs/netsmith/netsmith_parsec.py -I $warmup_insts --insts_after_warmup $simul_insts --benchmark_parsec ${bench} -r 1 --checkpoint-dir $CHKPTS_DIR/roi_checkpoint/system_5/${bench} --kernel $DISK_IMG_DIR/vmlinux-5.4.49 --disk-image $DISK_IMG_DIR/x86-parsec --router_map_file ./topologies_and_routing/topo_maps/noci/${1}.map --flat_vn_map_file topologies_and_routing/vn_maps/${3}.vn --flat_nr_map_file topologies_and_routing/nr_lists/${2}.nrl --noi_clk ${5}GHz --vcs-per-vnet $tot_vcs --evn_n_deadlock_free 1 --evn_min_n_deadlock_free ${4} --evn_deadlock_partition $deadlock_partition --topology FS_NoCI_EscapeVirtualNetworks --noi_routers 20 --noc_clk 3.8GHz --sys-clock 3.8GHz --cpu-clock 3.8GHz --ruby-clock 3.8GHz --num-cpus 64 --mem_or_coh mem --num-dirs 32 --caches --num-l2caches 64 --l2_size 2MB --num_chiplets 4 --mem-size 32GB --ruby --network garnet --link-width-bits 64 --cpu-type X86O3CPU --routing-algorithm 2 --use_escape_vns --mem-type DDR4_2400_16x4 > $log_file 2>&1
    done
