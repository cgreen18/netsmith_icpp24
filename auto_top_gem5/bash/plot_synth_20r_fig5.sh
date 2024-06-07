#!/bin/bash


infile="synth_outputs/csvs/synth_20r_fig5.csv"
alg="synth_20r_fig5_22feb24"
memcoh="coh"
n_routers="20"

python3 python_scripts/graph_synth_freqadjusted.py $infile $alg coh uniform $n_routers

python3 python_scripts/graph_synth_freqadjusted.py $infile $alg mem uniform $n_routers