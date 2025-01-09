cmake_minimum_required(VERSION 3.10)
project(CarSimulator)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/bin)
include_directories(${PROJECT_SOURCE_DIR}/include)

add_executable(car_simulator
    src/main.cpp
    src/Server.cpp
)

target_link_libraries(car_simulator PRIVATE pthread)
