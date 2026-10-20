CC = gcc
CFLAGS ?= -Wall -Wextra -std=c99 -O2 -Iinclude
PYTHON ?= python

SRCS = src/palloc.c src/mmu.c src/sched.c src/syscall.c src/kernel.c src/main.c
TARGET = mini_kernel

all: build

build:
	$(CC) $(CFLAGS) $(SRCS) -o $(TARGET)

test: build
	$(PYTHON) run_tests.py

clean:
	rm -f $(TARGET) $(TARGET).exe *.o starter/starter_kernel starter/starter_kernel.exe mini_kernel_32.exe

.PHONY: all build test clean
