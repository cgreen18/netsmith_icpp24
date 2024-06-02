#!/bin/bash

# $1 is topology name

CMD="python3 mclb_scipy_mip.py --allpath_list ../topologies_and_routing/allpath_lists/${1}.rallpaths --out_name files/solutions/${1}.paths"

echo $CMD
$CMD