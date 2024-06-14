#!/bin/bash


# CLAs
warmup_insts=100000000
simul_insts=100000000

if [ $# -eq 1 ]; then
    simul_insts="$1"

elif [ $# -eq 2 ]; then
    simul_insts="$1"
    warmup_insts="$2"

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
        for topo in "kite_small" "lpbt_s_latop" "lpbt_s_power";
            do
                log_file=./parsec_results/logs/${bench}_${topo}_noci_nndbt_picky_none_${warmup_insts}warmup_${simul_insts}simul_38GHz_2MB_allthreads_32GBxDDR4_l2caches_2evns_10vcs_64lwidth_sameflowpriority_lwbufadj.out
                cmd="./build/X86/gem5.fast -d ./parsec_results/noci_32GBxDDR4_2envs_38GHz_2MBl2_allthreads_64lwidth_sameflowpriority_lwbufadj/${warmup_insts}warmup_${simul_insts}simul/${bench}/${topo}_noci_nndbt_picky_none/ configs/netsmith/netsmith_parsec.py -I $warmup_insts --insts_after_warmup $simul_insts --benchmark_parsec ${bench} -r 1 --checkpoint-dir $CHKPTS_DIR/roi_checkpoint/system_5/${bench} --router_map_file ./topologies_and_routing/topo_maps/noci/${topo}_noci.map --flat_vn_map_file topologies_and_routing/vn_maps/${topo}_noci_nndbt_picky_none_2vns.vn --flat_nr_map_file topologies_and_routing/nr_lists/${topo}_noci_nndbt_picky.nrl --topology FS_NoCI_EscapeVirtualNetworks --noi_routers 20 --noc_clk 3.8GHz --sys-clock 3.8GHz --cpu-clock 3.8GHz --ruby-clock 3.8GHz --noi_clk 3.6GHz --num-cpus 64 --mem_or_coh mem --num-dirs 32 --caches --num-l2caches 64 --l2_size 2MB --num_chiplets 4 --mem-size 32GB --ruby --network garnet --link-width-bits 64 --kernel $DISK_IMG_DIR/vmlinux-5.4.49 --disk-image $DISK_IMG_DIR/x86-parsec --cpu-type X86O3CPU --routing-algorithm 2 --use_escape_vns --vcs-per-vnet 10 --evn_n_deadlock_free 1 --evn_min_n_deadlock_free 2 --evn_deadlock_partition 8 --mem-type DDR4_2400_16x4 > $log_file 2>&1"

                echo "Running:"
                echo "$cmd"
                # $cmd
                ./build/X86/gem5.fast -d ./parsec_results/noci_32GBxDDR4_2envs_38GHz_2MBl2_allthreads_64lwidth_sameflowpriority_lwbufadj/${warmup_insts}warmup_${simul_insts}simul/${bench}/${topo}_noci_nndbt_picky_none/ configs/netsmith/netsmith_parsec.py -I $warmup_insts --insts_after_warmup $simul_insts --benchmark_parsec ${bench} -r 1 --checkpoint-dir $CHKPTS_DIR/roi_checkpoint/system_5/${bench} --router_map_file ./topologies_and_routing/topo_maps/noci/${topo}_noci.map --flat_vn_map_file topologies_and_routing/vn_maps/${topo}_noci_nndbt_picky_none_2vns.vn --flat_nr_map_file topologies_and_routing/nr_lists/${topo}_noci_nndbt_picky.nrl --topology FS_NoCI_EscapeVirtualNetworks --noi_routers 20 --noc_clk 3.8GHz --sys-clock 3.8GHz --cpu-clock 3.8GHz --ruby-clock 3.8GHz --noi_clk 3.6GHz --num-cpus 64 --mem_or_coh mem --num-dirs 32 --caches --num-l2caches 64 --l2_size 2MB --num_chiplets 4 --mem-size 32GB --ruby --network garnet --link-width-bits 64 --kernel $DISK_IMG_DIR/vmlinux-5.4.49 --disk-image $DISK_IMG_DIR/x86-parsec --cpu-type X86O3CPU --routing-algorithm 2 --use_escape_vns --vcs-per-vnet 10 --evn_n_deadlock_free 1 --evn_min_n_deadlock_free 2 --evn_deadlock_partition 8 --mem-type DDR4_2400_16x4 > $log_file 2>&1
            done

# med
        for topo in "kite_med" "ft_x" "lpbt_m_latop";
            do
                log_file=./parsec_results/logs/${bench}_${topo}_noci_nndbt_picky_none_${warmup_insts}warmup_${simul_insts}simul_38GHz_2MB_allthreads_32GBxDDR4_l2caches_2evns_10vcs_64lwidth_sameflowpriority_lwbufadj.out
                cmd="./build/X86/gem5.fast -d ./parsec_results/noci_32GBxDDR4_2envs_38GHz_2MBl2_allthreads_64lwidth_sameflowpriority_lwbufadj/${warmup_insts}warmup_${simul_insts}simul/${bench}/${topo}_noci_nndbt_picky_none/ configs/netsmith/netsmith_parsec.py -I $warmup_insts --insts_after_warmup $simul_insts --benchmark_parsec ${bench} -r 1 --checkpoint-dir $CHKPTS_DIR/roi_checkpoint/system_5/${bench} --router_map_file ./topologies_and_routing/topo_maps/noci/${topo}_noci.map --flat_vn_map_file topologies_and_routing/vn_maps/${topo}_noci_nndbt_picky_none_2vns.vn --flat_nr_map_file topologies_and_routing/nr_lists/${topo}_noci_nndbt_picky.nrl --topology FS_NoCI_EscapeVirtualNetworks --noi_routers 20 --noc_clk 3.8GHz --sys-clock 3.8GHz --cpu-clock 3.8GHz --ruby-clock 3.8GHz --noi_clk 3.0GHz --num-cpus 64 --mem_or_coh mem --num-dirs 32 --caches --num-l2caches 64 --l2_size 2MB --num_chiplets 4 --mem-size 32GB --ruby --network garnet --link-width-bits 64 --kernel $DISK_IMG_DIR/vmlinux-5.4.49 --disk-image $DISK_IMG_DIR/x86-parsec --cpu-type X86O3CPU --routing-algorithm 2 --use_escape_vns --vcs-per-vnet 10 --evn_n_deadlock_free 1 --evn_min_n_deadlock_free 2 --evn_deadlock_partition 8 --mem-type DDR4_2400_16x4 > $log_file 2>&1"

                echo "Running:"
                echo "$cmd"
                # $cmd
                ./build/X86/gem5.fast -d ./parsec_results/noci_32GBxDDR4_2envs_38GHz_2MBl2_allthreads_64lwidth_sameflowpriority_lwbufadj/${warmup_insts}warmup_${simul_insts}simul/${bench}/${topo}_noci_nndbt_picky_none/ configs/netsmith/netsmith_parsec.py -I $warmup_insts --insts_after_warmup $simul_insts --benchmark_parsec ${bench} -r 1 --checkpoint-dir $CHKPTS_DIR/roi_checkpoint/system_5/${bench} --router_map_file ./topologies_and_routing/topo_maps/noci/${topo}_noci.map --flat_vn_map_file topologies_and_routing/vn_maps/${topo}_noci_nndbt_picky_none_2vns.vn --flat_nr_map_file topologies_and_routing/nr_lists/${topo}_noci_nndbt_picky.nrl --topology FS_NoCI_EscapeVirtualNetworks --noi_routers 20 --noc_clk 3.8GHz --sys-clock 3.8GHz --cpu-clock 3.8GHz --ruby-clock 3.8GHz --noi_clk 3.0GHz --num-cpus 64 --mem_or_coh mem --num-dirs 32 --caches --num-l2caches 64 --l2_size 2MB --num_chiplets 4 --mem-size 32GB --ruby --network garnet --link-width-bits 64 --kernel $DISK_IMG_DIR/vmlinux-5.4.49 --disk-image $DISK_IMG_DIR/x86-parsec --cpu-type X86O3CPU --routing-algorithm 2 --use_escape_vns --vcs-per-vnet 10 --evn_n_deadlock_free 1 --evn_min_n_deadlock_free 2 --evn_deadlock_partition 8 --mem-type DDR4_2400_16x4 > $log_file 2>&1
            done

#large
        for topo in "butter_donut_x" "dbl_bfly_x" "kite_large";
            do
                log_file=./parsec_results/logs/${bench}_${topo}_noci_nndbt_picky_none_${warmup_insts}warmup_${simul_insts}simul_38GHz_2MB_allthreads_32GBxDDR4_l2caches_2evns_10vcs_64lwidth_sameflowpriority_lwbufadj.out
                cmd="./build/X86/gem5.fast -d ./parsec_results/noci_32GBxDDR4_2envs_38GHz_2MBl2_allthreads_64lwidth_sameflowpriority_lwbufadj/${warmup_insts}warmup_${simul_insts}simul/${bench}/${topo}_noci_nndbt_picky_none/ configs/netsmith/netsmith_parsec.py -I $warmup_insts --insts_after_warmup $simul_insts --benchmark_parsec ${bench} -r 1 --checkpoint-dir $CHKPTS_DIR/roi_checkpoint/system_5/${bench} --router_map_file ./topologies_and_routing/topo_maps/noci/${topo}_noci.map --flat_vn_map_file topologies_and_routing/vn_maps/${topo}_noci_nndbt_picky_none_2vns.vn --flat_nr_map_file topologies_and_routing/nr_lists/${topo}_noci_nndbt_picky.nrl --topology FS_NoCI_EscapeVirtualNetworks --noi_routers 20 --noc_clk 3.8GHz --sys-clock 3.8GHz --cpu-clock 3.8GHz --ruby-clock 3.8GHz --noi_clk 2.7GHz --num-cpus 64 --mem_or_coh mem --num-dirs 32 --caches --num-l2caches 64 --l2_size 2MB --num_chiplets 4 --mem-size 32GB --ruby --network garnet --link-width-bits 64 --kernel $DISK_IMG_DIR/vmlinux-5.4.49 --disk-image $DISK_IMG_DIR/x86-parsec --cpu-type X86O3CPU --routing-algorithm 2 --use_escape_vns --vcs-per-vnet 10 --evn_n_deadlock_free 1 --evn_min_n_deadlock_free 2 --evn_deadlock_partition 8 --mem-type DDR4_2400_16x4 > $log_file 2>&1"

                echo "Running:"
                echo "$cmd"
                # $cmd
                ./build/X86/gem5.fast -d ./parsec_results/noci_32GBxDDR4_2envs_38GHz_2MBl2_allthreads_64lwidth_sameflowpriority_lwbufadj/${warmup_insts}warmup_${simul_insts}simul/${bench}/${topo}_noci_nndbt_picky_none/ configs/netsmith/netsmith_parsec.py -I $warmup_insts --insts_after_warmup $simul_insts --benchmark_parsec ${bench} -r 1 --checkpoint-dir $CHKPTS_DIR/roi_checkpoint/system_5/${bench} --router_map_file ./topologies_and_routing/topo_maps/noci/${topo}_noci.map --flat_vn_map_file topologies_and_routing/vn_maps/${topo}_noci_nndbt_picky_none_2vns.vn --flat_nr_map_file topologies_and_routing/nr_lists/${topo}_noci_nndbt_picky.nrl --topology FS_NoCI_EscapeVirtualNetworks --noi_routers 20 --noc_clk 3.8GHz --sys-clock 3.8GHz --cpu-clock 3.8GHz --ruby-clock 3.8GHz --noi_clk 2.7GHz --num-cpus 64 --mem_or_coh mem --num-dirs 32 --caches --num-l2caches 64 --l2_size 2MB --num_chiplets 4 --mem-size 32GB --ruby --network garnet --link-width-bits 64 --kernel $DISK_IMG_DIR/vmlinux-5.4.49 --disk-image $DISK_IMG_DIR/x86-parsec --cpu-type X86O3CPU --routing-algorithm 2 --use_escape_vns --vcs-per-vnet 10 --evn_n_deadlock_free 1 --evn_min_n_deadlock_free 2 --evn_deadlock_partition 8 --mem-type DDR4_2400_16x4 > $log_file 2>&1
            done
    done
