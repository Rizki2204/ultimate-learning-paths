CXX ?= g++
CXXFLAGS ?= -Wall -Wextra -std=c++14 -O2

all: build

build:
	$(CXX) $(CXXFLAGS) -o starter_lsm lsm_starter.cpp

clean:
	rm -f starter_lsm starter_lsm.exe

.PHONY: all build clean
