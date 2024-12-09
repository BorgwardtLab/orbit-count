cmake_minimum_required(VERSION 3.4...3.18)
project(orca_graph)

add_subdirectory(pybind11)
pybind11_add_module(_orca src/_orca.cpp)

install(TARGETS _orca DESTINATION src/orca)


# EXAMPLE_VERSION_INFO is defined by setup.py and passed into the C++ code as a
# define (VERSION_INFO) here.
#target_compile_definitions(orca_graph
#                           PRIVATE VERSION_INFO=${EXAMPLE_VERSION_INFO})