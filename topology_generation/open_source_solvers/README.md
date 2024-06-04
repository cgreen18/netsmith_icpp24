# Open-Source Solvers (Alternative Topology Generation)

Parses and runs NetSmith and LPBT LP (.lp) models

Currently, the only open-source solver that is written is using Python SCIPY MIP library

## NetSmith (auto_top)

#### Simple/Basic

To test installation, solving a large, 12 router model takes a few minutes (assume 10 minute limit)
```
python3 scipy_mip/run_scipy_mip.py --model_file ../gurobi/files/models/auto_top/autotop_r12_p4_ll25_avghops_simple.lp --time_limit 10
```


#### NoI

Generate large (20r) NetSmith topology optimized for latency
```
python3 scipy_mip/run_scipy_mip.py --model_file ../gurobi/files/models/auto_top/autotop_r20_p4_ll25_avghops_simple.lp --time_limit 4320
```

or equivalently through bash
```
source ./bash/create_netsmith.sh 20 large latency
```


#### Usage

To see CLA options and brief descriptions
```
python3 scipy_mip/run_scipy_mip.py --help
```



## LPBT (auto_top)

#### Simple/Basic

To test installation, solving a large, 12 router model takes a few minutes (assume 10 minute limit)
```
python3 scipy_mip/run_scipy_mip.py --model_file ../gurobi/files/models/lpbt/lpbt_r12_p4_ll25_tothops.lp --time_limit 10
```


#### NoI

Generate large (20r) LPBT topology optimized for latency
```
python3 scipy_mip/run_scipy_mip.py --model_file ../gurobi/files/models/lpbt/lpbt_r20_p4_ll25_tothops.lp --time_limit 4320
```
