#!/bin/bash

# makefile writes executable here
if [ ! -d ./bin  ]
then
    mkdir ./bin
fi

if [ ! -d ./files  ]
then
    mkdir ./files
fi

# auto_top bin will expect "files/models" to write model definitions
if [ ! -d ./files/models  ]
then
    mkdir ./files/models
fi
# auto_top bin will expect to read problem definition (.dat)
if [ ! -d ./files/prob_defs  ]
then
    mkdir ./files/prob_defs
fi

# auto_top bin expects "files/solutions" to exist for optimal sols (.map)
if [ ! -d ./files/optimal_solutions  ]
then
    mkdir ./files/optimal_solutions
fi

# auto_top bin expects "files/running_solutions" to exist for --use_runsol outputs (.map)
if [ ! -d ./files/running_solutions  ]
then
    mkdir ./files/running_solutions
fi

# auto_top bin expects "files/nodefiles" to exist for --use_nodefiles temp files from gurobi
if [ ! -d ./files/nodefiles  ]
then
    mkdir ./files/nodefiles
fi
