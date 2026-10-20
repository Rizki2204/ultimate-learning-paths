CC ?= gcc
CFLAGS ?= -Wall -Wextra -std=c99 -O2 -Iinclude
PYTHON ?= python

SRCS = src/mmu.c src/instructions.c src/cpu.c src/main.c
TARGET = riscv_emu

all: build

build:
	$(CC) $(CFLAGS) $(SRCS) -o $(TARGET)

test: build
	$(PYTHON) run_tests.py

clean:
	rm -f $(TARGET) $(TARGET).exe *.o starter/starter_emu starter/starter_emu.exe

.PHONY: all build test clean
