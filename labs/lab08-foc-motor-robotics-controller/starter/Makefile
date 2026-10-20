CC ?= gcc
CFLAGS ?= -Wall -Wextra -std=c99 -O2

all: build

build:
	$(CC) $(CFLAGS) -o starter_foc foc_starter.c -lm

clean:
	rm -f starter_foc starter_foc.exe

.PHONY: all build clean
