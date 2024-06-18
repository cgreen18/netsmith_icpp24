#!/bin/bash

infile="synth_outputs/csvs/paper_results/synth_20r_fig5.csv"
alg="synth_20r_fig5_22feb24"
n_routers="20"

CMD="python3 python_scripts/graph_synth_freqadjusted.py $infile $alg coh uniform $n_routers"

echo "${CMD}"
$CMD

CMD="python3 python_scripts/graph_synth_freqadjusted.py $infile $alg mem uniform $n_routers"

echo "${CMD}"
$CMD
