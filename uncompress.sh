#!/bin/bash

tar -xvzf lpbt_model.tar.gz
cp -r lpbt topology_generation/gurobi/files/models/

tar -xvzf netsmith_models.tar.gz
cp netsmith_models/auto_top_avghops_lp/* topology_generation/gurobi/files/models/
cp netsmith_models/auto_top_scbw_lp/* topology_generation/gurobi/files/models/


tar -xvzf parsec_disk_image.tar.gz
cp -r parsec_disk_image ./auto_top_gem5

tar -xvzf parsec_noci_checkpoints
cp -r parsec_noci_checkpoints ./auto_top_gem5
