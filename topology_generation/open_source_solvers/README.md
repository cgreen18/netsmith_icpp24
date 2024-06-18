# Open-Source Solvers (Alternative Topology Generation)

Parses and runs NetSmith and LPBT LP (.lp) models

Currently, the only open-source solver that is written is using Python SCIPY MIP library


The problems are largely defined by three parameters: number of routers, number of ports, and the longest link allowed (e.g. small, medium, large). These parameters are often encoded into the names of generated topologies such as "my_20r_4p_25ll_topology.map". The integer (20) next to the "r" is number of routers, the integer (4) next to the "p" is number of ports, and the integer (25) next to "ll" is longest link.

IMPORTANT: "25ll" was a vestige of old code and signifies that the longest link is 2.5 units long (decimal removed for simple filenames) where each router is assumed to be on a grid with basic length of 1. That is to say, in the small topologies, the longest link is 1.5 units because it corresponds to a (1,1) link; medium is 2.0 for (2,0)/(0,2); and large is 2.5 for (2,1)/(1,2).

## Setup


Need to install libraries. Recommended to use venv


```
source init.sh
source install_tools.sh
source setup.sh
```

On every usage (if you log off)
```
source setup.sh
```

# Running

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
