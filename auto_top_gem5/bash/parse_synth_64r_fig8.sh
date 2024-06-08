#!/bin/bash


MCLB_DIR="synth_outputs/simple/2b/mixed/9evns_12vcs_64cpus_4xdirs_4.0GHz/"
MCLB_OUT="synth_outputs/csvs/simple_2b_9evns_12vcs_64cpus_4xdirs_4.0GHz.csv"
python3 python_scripts/parse_synth_results.py $MCLB_DIR $MCLB_OUT

NNDBT_DIR="synth_outputs/simple/2b/mixed/2evns_12vcs_64cpus_4xdirs_4.0GHz/"
NNDBT_OUT="synth_outputs/csvs/simple_2b_2evns_12vcs_64cpus_4xdirs_4.0GHz.csv"
python3 python_scripts/parse_synth_results.py $NNDBT_DIR $NNDBT_OUT

COMBINED_FILE="synth_outputs/csvs/synth_64r_fig8.csv"
cat $MCLB_OUT > $COMBINED_FILE
tail -n +2 $NNDBT_OUT >> $COMBINED_FILE


echo "Completed parsing"
echo "Wrote to ${COMBINED_FILE}"