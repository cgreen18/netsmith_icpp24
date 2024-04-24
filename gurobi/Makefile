
# BASE     = /package/gurobi/9.5.1
BASE     = /package/gurobi/10.0
#BASE     = /package/gurobi/11.0
BUILD_HOME	 = /home/min/a/green456/gurobi/build
PLATFORM = linux64
INC      = $(BASE)/include/
# INC      = $(BUILD_HOME)/include/
CC       = gcc
CPP      = g++
# CARGS    = -m64 -DIL_STD -O -fPIC -fno-strict-aliasing -fexceptions -std=c++11 -D_GLIBCXX_USE_CXX11_ABI
CARGS	 = -m64 -g 

# CLIB     = -L$(BASE)/lib -lgurobi95
# CPPLIB   = -L$(BASE)/lib -lgurobi_c++ -lgurobi95
CPPLIB   = -L$(BASE)/lib -lgurobi_c++ -lgurobi100
# CPPLIB   = -L$(BASE)/lib -lgurobi_c++ -lgurobi110


auto_top: src/auto_top.cpp
	$(CPP) $(CARGS) -o bin/auto_top src/auto_top.cpp -I$(INC) $(CPPLIB) -lm

auto_top_db: src/auto_top.cpp
	$(CPP) $(CARGS) -o bin/auto_top_db src/auto_top.cpp -DDEBUG -I$(INC) $(CPPLIB) -lm

clean:
	rm -rf bin/
