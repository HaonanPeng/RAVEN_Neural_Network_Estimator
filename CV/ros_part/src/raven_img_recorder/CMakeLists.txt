cmake_minimum_required(VERSION 2.8.3)
project(raven_img_recorder)

## Find catkin and any catkin packages
find_package(catkin REQUIRED COMPONENTS roscpp rospy std_msgs geometry_msgs message_generation)

## Add in message and service files
#add_message_files(FILES raven_automove.msg raven_state.msg arduino_to_ros.msg)

#add_service_files(FILES Sensor_Distance.srv)

## Generate added messages and services
#generate_messages(DEPENDENCIES std_msgs geometry_msgs)

## Declare a catkin package
catkin_package()

## Build talker and listeneri
include_directories(include ${catkin_INCLUDE_DIRS})

#add_library(recorder_library src/RavenState_Recorder.cpp)

#add_executable(talkerAutoCircle src/talker.cpp  src/Raven_Controller.cpp src/Raven_PathPlanner.cpp)
#target_link_libraries(talkerAutoCircle recorder_library ${catkin_LIBRARIES})
#add_dependencies(talkerAutoCircle AutoCircle_test_generate_messages_cpp)

add_executable(test_turtlesim_random src/test_turtlesim_random.cpp)
target_link_libraries(test_turtlesim_random ${catkin_LIBRARIES})

