#!/bin/bash


N_PROCS=$(nproc)

echo "Building with $N_PROCS processors"

scons-3 -j $N_PROCS build/Garnet_standalone/gem5.fast
scons-3 -j $N_PROCS build/X86/gem5.fast

# for purdue servers. let it fail otherwise
# ml gcc

