PYTHON ?= python

all: test

build:
	@echo "Pure Python module, no native compilation required."

test:
	$(PYTHON) run_tests.py

clean:
	rm -rf __pycache__ */__pycache__ *.pyc */*.pyc

.PHONY: all build test clean
