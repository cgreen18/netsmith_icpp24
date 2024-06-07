#!/bin/bash


# for building dsent
cd ./ext/dsent
mkdir build
cmake ./
make

cd ../..


# for plotting
source ../venv_netsmith/bin/activate
