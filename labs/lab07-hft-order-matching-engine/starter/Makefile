CXX ?= g++
CXXFLAGS ?= -Wall -Wextra -std=c++14 -O3

all: build

build:
	$(CXX) $(CXXFLAGS) -o starter_matching matching_engine_starter.cpp

clean:
	rm -f starter_matching starter_matching.exe

.PHONY: all build clean
