#!/bin/bash

python3 python_scripts/static_metrics.py --use_bi_bw --use_sc_bw --filename ${1} > ${2}
