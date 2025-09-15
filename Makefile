

INCLUDES_PYBIND11 := $(shell .venv/bin/python -m pybind11 --includes)
EXTENSION_PYBIND11 := $(shell .venv/bin/python -m pybind11 --extension-suffix)


*.so : random_utility.cpp
	c++ -O3 -Wall -shared -std=c++11 -fPIC $(INCLUDES_PYBIND11) random_utility.cpp -o random_utility$(EXTENSION_PYBIND11)