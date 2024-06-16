#!/bin/bash

# python3 python_scripts/parse_parsec_results.py parsec_results/noci_32GBxDDR4_6envs_38GHz_2MBl2_allthreads_64lwidth_sameflowpriority_lwbufadj/100mwarmup_100msimul/ parsec_results/csvs/noci_mclb_$mydate.csv

# python3 python_scripts/parse_parsec_results.py parsec_results/noci_32GBxDDR4_2envs_38GHz_2MBl2_allthreads_64lwidth_sameflowpriority_lwbufadj/100mwarmup_100msimul/ parsec_results/csvs/noci_nndbt_$mydate.csv

mydate=$(date +'%d%b%y')



python3 python_scripts/parse_parsec_results.py parsec_results/noci_32GBxDDR4_6envs_38GHz_2MBl2_allthreads_64lwidth_sameflowpriority_lwbufadj/100000000warmup_100000000simul/ parsec_results/csvs/noci_mclb_$mydate.csv

python3 python_scripts/parse_parsec_results.py parsec_results/noci_32GBxDDR4_2envs_38GHz_2MBl2_allthreads_64lwidth_sameflowpriority_lwbufadj/100000000warmup_100000000simul parsec_results/csvs/noci_nndbt_$mydate.csv


outfile="parsec_results/csvs/noci_mclb_and_nndbt_$mydate.csv"

# cat parsec_results/csvs/noci_mclb_$mydate.csv | grep "picky\|mesh\|bench" > $outfile
# tail -n +2 parsec_results/csvs/noci_nndbt_$mydate.csv | grep "injej" >> $outfile

cat parsec_results/csvs/noci_mclb_$mydate.csv > $outfile
tail -n +2 parsec_results/csvs/noci_nndbt_$mydate.csv >> $outfile

echo "Wrote to $outfile"