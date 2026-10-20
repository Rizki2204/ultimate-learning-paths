CC ?= gcc
CFLAGS ?= -Wall -Wextra -std=c99 -O2

all: build

build:
	$(CC) $(CFLAGS) -o starter_emu cpu_starter.c

clean:
	rm -f starter_emu starter_emu.exe

.PHONY: all build clean
