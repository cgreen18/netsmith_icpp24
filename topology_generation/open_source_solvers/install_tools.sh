
#!/bin/bash

# for setting up working directory tools


# install python 3.11 from source

sudo apt update
sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev
wget https://www.python.org/ftp/python/3.11.3/Python-3.11.3.tgz
tar -xf Python-3.11.3.tgz
cd Python-3.11.3
./configure --enable-optimizations
make -j 12

# for new exe "python3.11"
sudo make altinstall

# load python with scipy >= 1.9.0
ml python3/3.11

# create venv
python3 -m venv venv_scipymilp_py311

source venv_scipymilp_py311/bin/activate

pip3 install --upgrade pip


# for 3.11 issues with cbclib wo this
pip3 install wsl
pip3 install scipy
pip3 install mip
# cbc 0.0.5 for issues with glibc 2.27+ (ecn has 2.17)
pip3 install cbc


pip3 install ortools