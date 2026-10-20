CXX ?= g++
CXXFLAGS ?= -Wall -Wextra -std=c++14 -O3 -Iinclude
PYTHON ?= python

SRCS = src/order_book.cpp src/matching_engine.cpp src/benchmark.cpp src/main.cpp
TARGET = hft_engine

all: build

build:
	$(CXX) $(CXXFLAGS) $(SRCS) -o $(TARGET)

test: build
	$(PYTHON) run_tests.py

clean:
	rm -f $(TARGET) $(TARGET).exe *.o starter/starter_matching starter/starter_matching.exe

.PHONY: all build test clean
