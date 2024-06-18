#!/bin/bash

sudo apt update

sudo apt install -y build-essential vim

# for all
sudo apt install -y python3-pip python3-venv


# for dsent
sudo apt install -y python-minimal python-dev
sudo apt install -y cmake make
# add cmake to path
export PATH=$PATH:/usr/bin/cmake

# for gem5
sudo apt install -y scons zlib1g zlib1g-dev
sudo apt install m4 libprotobuf-dev protobuf-compiler libprotoc-dev libgoogle-perftools-dev libboost-all-dev python-six libpng-dev swig


python3 -m venv venv_netsmith
source venv_netsmith/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
