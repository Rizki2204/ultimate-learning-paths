CXX ?= g++
CXXFLAGS ?= -Wall -Wextra -std=c++14 -O2 -Iinclude
PYTHON ?= python

SRCS = src/lexer.cpp src/parser.cpp src/bytecode.cpp src/vm.cpp src/main.cpp
TARGET = minilang_compiler

all: build

build:
	$(CXX) $(CXXFLAGS) $(SRCS) -o $(TARGET)

test: build
	$(PYTHON) run_tests.py

clean:
	rm -f $(TARGET) $(TARGET).exe *.o starter/starter_compiler starter/starter_compiler.exe

.PHONY: all build test clean
