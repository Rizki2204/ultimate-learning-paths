CC ?= gcc
CFLAGS ?= -Wall -Wextra -std=c99 -O2 -Iinclude
PYTHON ?= python

SRCS = src/foc_math.c src/pi_controller.c src/svpwm.c src/kinematics.c src/simulation.c src/main.c
TARGET = foc_controller

all: build

build:
	$(CC) $(CFLAGS) $(SRCS) -o $(TARGET) -lm

test: build
	$(PYTHON) run_tests.py

clean:
	rm -f $(TARGET) $(TARGET).exe *.o starter/starter_foc starter/starter_foc.exe

.PHONY: all build test clean
