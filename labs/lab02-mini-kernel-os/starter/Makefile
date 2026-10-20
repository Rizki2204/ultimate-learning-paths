CC ?= gcc
CFLAGS ?= -Wall -Wextra -std=c99 -O2

all: build

build:
	$(CC) $(CFLAGS) -o starter_kernel kernel_starter.c

clean:
	rm -f starter_kernel starter_kernel.exe

.PHONY: all build clean
