# Gurobi

Runs both NetSmith and LPBT formulations

## NetSmith (auto_top)

#### Simple/Basic

To test installation, creating a large, 12 router topology takes seconds
```
./bin/auto_top
```


#### NoI

Generate large (20r) NetSmith topology optimized for latency
```
./bin/auto_top -if ./files/prob_defs/dev_20r_4p_25ll.dat -of ns_l_latop --model_type w_hop --max_diam 20 -o avg_hops --use_run_sol --concurrent_mip --heuristic_ratio 0.8 --mip_focus 1
```

or equivalently through bash
```
source ./bash/create_netsmith.sh 20 large latency
```

If completes optimal the map will be in ./files/optimal_solutions and/or running solutions (--use_run_sol) in ./files/runnings_solutions


#### Model Generation (for Open-Source Solvers)

Generate Large (20r) NetSmith model file (.lp) that doesn't use any general or SOS constraints. (This will generate the model that is run in above commands.)
```
./bin/auto_top -if ./files/prob_defs/dev_20r_4p_25ll.dat --max_diam 20 -o avg_hops --simple_model --no_solve --use_lp_model
```

#### Usage

To see CLA options and brief descriptions
```
./bin/auto_top --help
```


## LPBT

#### Simple/Basic

To test installation, creating a large, 12 router topology takes a few hours
```
./bin/lpbt
```

#### NoI

Generate large (20r) LPBT topology optimized for latency
```
./bin/lpbt -if ./files/prob_defs/dev_20r_5p_25ll.dat -of lpbt_l_latop -o total_hops --use_run_sol --time_limit 4320 --write_model --heuristic_ratio 0.8 --mip_focus 1 --concurrent_mip
```

or equivalently through bash
```
source ./bash/create_lpbt.sh 20 large latency
```

If completes optimal the map will be in ./files/optimal_solutions and/or running solutions (--use_run_sol) in ./files/runnings_solutions

#### Model Generation (for Open-Source Solvers)

Generate Large (20r) LPBT model file (.lp) that doesn't use any general or SOS constraints. (This will generate the model that is run in above commands.)
```
./bin/lpbt -if ./files/prob_defs/dev_20r_4p_25ll.dat -o total_hops --no_solve --use_lp_model --wrtie_model
```

#### Usage

To see CLA options and brief descriptions
```
./bin/lpbt --help
```

## Extra scripts

Script to make a lot of models
```
python3 python_scripts/make_all_models.py
```

If more problem defintions need to be made then
```
python3 python_scripts/write_prob_defs.py
```
