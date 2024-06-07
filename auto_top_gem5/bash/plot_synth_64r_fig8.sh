#!/bin/bash


infile="synth_outputs/csvs/synth_64r_fig8.csv"
alg="synth_64r_fig8"
memcoh="coh"
n_routers="64"

python3 python_scripts/graph_synth_freqadjusted.py $infile $alg coh uniform $n_routers