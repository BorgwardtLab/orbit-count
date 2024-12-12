# Require CMake 3.15+ (matching scikit-build-core) Use new versions of all
# policies up to CMake 3.27
cmake_minimum_required(VERSION 3.15...3.27)

# Scikit-build-core sets these values for you, or you can just hard-code the
# name and version.
project(
  ${SKBUILD_PROJECT_NAME}
  VERSION ${SKBUILD_PROJECT_VERSION}
  LANGUAGES CXX)

# Find the module development requirements (requires FindPython from 3.17 or
# scikit-build-core's built-in backport)
find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)
find_package(pybind11 CONFIG REQUIRED)          # add_subdirectory(pybind11)


# Find OpenMP package
find_package(OpenMP REQUIRED)

# Add a library using FindPython's tooling (pybind11 also provides a helper like
# this)
python_add_library(_orca MODULE src/_orca.cpp WITH_SOABI)
target_link_libraries(_orca PRIVATE pybind11::headers)

# Link OpenMP to your target
target_link_libraries(_orca PRIVATE OpenMP::OpenMP_CXX)

# Optional: Set OpenMP flags if needed
if(OpenMP_CXX_FOUND)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
endif()


# This is passing in the version as a define just as an example
target_compile_definitions(_orca PRIVATE VERSION_INFO=${PROJECT_VERSION})

# The install directory is the output (wheel) directory
install(TARGETS _orca DESTINATION orbit_count)