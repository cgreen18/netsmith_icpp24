#!/bin/bash

MCLB_OUT="synth_outputs/csvs/2b_mixed_mclb_hops_4_6_40cpus_4xdirs_4.0GHz.csv"
NNDBT_OUT="synth_outputs/csvs/2b_mixed_nndbt_none_2_6_40cpus_4xdirs_4.0GHz.csv"

python3 python_scripts/parse_synth_results.py synth_outputs/simple/2b/mixed/mclb_hops_4_6_40cpus_4xdirs_4.0GHz/ $MCLB_OUT
python3 python_scripts/parse_synth_results.py synth_outputs/simple/2b/mixed/nndbt_none_2_6_40cpus_4xdirs_4.0GHz/ $NNDBT_OUT


COMBINED_FILE="synth_outputs/csvs/synth_20r_fig5.csv"

cat $MCLB_OUT > $COMBINED_FILE
tail -n +2 $NNDBT_OUT >> $COMBINED_FILE

echo "Completed parsing"
echo "Wrote to ${COMBINED_FILE}"
