cmake_minimum_required(VERSION 3.4...3.18)
project(orca_graph)

# Find OpenMP package
find_package(OpenMP REQUIRED)

add_subdirectory(pybind11)
pybind11_add_module(_orca src/_orca.cpp)

# Link OpenMP to your target
target_link_libraries(_orca PRIVATE OpenMP::OpenMP_CXX)

# Optional: Set OpenMP flags if needed
if(OpenMP_CXX_FOUND)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
endif()

install(TARGETS _orca DESTINATION src/orca)