CXX ?= g++
CXXFLAGS ?= -Wall -Wextra -std=c++14 -O2

all: build

build:
	$(CXX) $(CXXFLAGS) -o starter_compiler compiler_starter.cpp

clean:
	rm -f starter_compiler starter_compiler.exe

.PHONY: all build clean
