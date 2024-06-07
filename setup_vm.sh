#!/bin/bash

sudo apt update

sudo apt install build-essential

# for all
sudo apt install -y python3-pip python3-venv
python3 -m venv venv_netsmith
source venv_netsmith/bin/activate
pip3 install --upgrade pip
pip3 install -r matplotlib

# for dsent
sudo apt install -y python-minimal python-dev
sudo apt install -y cmake make
# add cmake to path
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/usr/bin/cmake:/usr/bin/cmake

