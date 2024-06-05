# DSENT


#### Installation/Setup

Requires python2

```
sudo apt install -y python-minimal
```

Must make DSENT
```
cd ./ext/dsent
cmake ./
make
```


## Calculate Area and Power

Given an example (short simulation) PARSEC stats in "my_20r_4p_25ll_topo_noci_picky_cohmem_prioritized_doubley_memory_mclb_hops"

```
python2 noci_power_area.py ./my_20r_4p_25ll_topo_noci_picky_cohmem_prioritized_doubley_memory_mclb_hops ./router.cfg ./electrical-link.cfg
```


## Paper figures

### Fig. 7

```
source bash/calculate_results_fig7.sh
source bash/plot_figure_fig7.sh
```