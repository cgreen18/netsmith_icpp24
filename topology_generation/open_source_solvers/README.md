# Alternative Topology Generation


Generate NoI (20r/4p), large (25ll) NetSmith topology

```
python3 scipy_mip/run_scipy_mip.py --model_file ../gurobi/files/models/auto_top/autotop_r20_p4_ll2_avghops_simple.lp --time_limit 10
```

If completes optimal the map will be in ./files/optimal_solutions