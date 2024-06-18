
#!/bin/bash

# for setting up working directory tools

N_PROCS=$(nproc)

# install python 3.11 from source

sudo apt update
sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev
wget https://www.python.org/ftp/python/3.11.3/Python-3.11.3.tgz
tar -xf Python-3.11.3.tgz
cd Python-3.11.3
./configure --enable-optimizations
make -j $N_PROCS

# for new exe "python3.11"
sudo make altinstall

# replace default
sudo update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.11 1
export PATH="/usr/local/bin:$PATH"

cd ..

# for purdue servers. Let fail
# load python with scipy >= 1.9.0
ml python3/3.11
