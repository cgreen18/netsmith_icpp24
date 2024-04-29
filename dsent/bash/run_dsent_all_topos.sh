#!/bin/bash

rm ./dsent_results/log.txt

cp dsent_results/basic_dsent_headers.csv dsent_results/dsent_stats.csv

for b in "ns_s_latop" "ns_s_scop" "ns_m_latop" "ns_m_scop" "ns_l_latop" "ns_l_scop" "ft_x" "butter_donut_x" "dbl_bfly_x" "kite_large" "kite_medium" "kite_small" "lpbt_s_latop" "lpbt_s_power" "lpbt_m_latop";
    do
        echo "python2 noci_power_area.py ./swaptions_for_dsent_20nov/${b}_noci_picky_cohmem_prioritized_doubley_memory_mclb_hops ./router.cfg ./electrical-link.cfg >> ./dsent_results/log.txt"
        python2 noci_power_area.py ./swaptions_for_dsent_20nov/${b}_noci_picky_cohmem_prioritized_doubley_memory_mclb_hops ./router.cfg ./electrical-link.cfg >> ./dsent_results/log.txt
    done

for b in "mesh";
    do
        echo "python2 noci_power_area.py ./swaptions_for_dsent_20nov/${b}_noci_naive_hops ./router.cfg ./electrical-link.cfg >> ./dsent_results/log.txt"
        python2 noci_power_area.py ./swaptions_for_dsent_20nov/${b}_noci_naive_hops ./router.cfg ./electrical-link.cfg >> ./dsent_results/log.txt
    done
