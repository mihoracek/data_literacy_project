cmake_minimum_required(VERSION 3.5.1)
project(txt2bin LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")

add_executable(${PROJECT_NAME} txt2bin.cpp)
