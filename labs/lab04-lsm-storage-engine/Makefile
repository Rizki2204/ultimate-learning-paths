CXX ?= g++
CXXFLAGS ?= -Wall -Wextra -std=c++14 -O2 -Iinclude
PYTHON ?= python

SRCS = src/wal.cpp src/memtable.cpp src/bloom.cpp src/sstable.cpp src/compaction.cpp src/lsm_engine.cpp src/main.cpp
TARGET = lsm_engine

all: build

build:
	$(CXX) $(CXXFLAGS) $(SRCS) -o $(TARGET)

test: build
	$(PYTHON) run_tests.py

clean:
	rm -f $(TARGET) $(TARGET).exe *.o *.sst *.log test_*.sst test_*.log starter/starter_lsm starter/starter_lsm.exe

.PHONY: all build test clean
