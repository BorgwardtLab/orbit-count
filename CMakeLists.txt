cmake_minimum_required(VERSION 3.4...3.18)
project(orca_graph)

add_subdirectory(pybind11)
pybind11_add_module(_orca src/_orca.cpp)

install(TARGETS _orca DESTINATION src/orca)