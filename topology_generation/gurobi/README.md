

## 1) Gurobi

Generate Large (20r) NetSmith topology
```
./gurobi/bin/auto_top -if ./files/prob_defs/dev_20r_4p_25ll.dat -of ns_l_latop --model_type w_hop --max_diam 20 --uni_links -o avg_hops --use_run_sol --concurrent_mip --heuristic_ratio 0.8 --mip_focus 1
```

If completes optimal the map will be in ./files/optimal_solutions and/or running solutions (--use_run_sol) in ./files/runnings_solutions

Generate Large (20r) NetSmith model file (.lp) that doesn't use any general or SOS constraints
```
./gurobi/bin/auto_top -if ./files/prob_defs/dev_20r_4p_25ll.dat --max_diam 20 --uni_links -o avg_hops --simple_model --no_solve --use_lp_model
```

Script to make a lot of models
```
python3 python_scripts/make_all_models.py
```

If more problem defintions need to be made then
```
python3 python_scripts/write_prob_defs.py
```
