# Install script for directory: /home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/isaac/Downloads/apriltags_kalman/ros_workspace/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/anafi_control/msg" TYPE FILE FILES
    "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/Waypoint.msg"
    "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistModified.msg"
    "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistStampedModified.msg"
    "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/State.msg"
    "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/MultiRotorRelativeState.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/anafi_control/cmake" TYPE FILE FILES "/home/isaac/Downloads/apriltags_kalman/ros_workspace/build/anafi_control/catkin_generated/installspace/anafi_control-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/isaac/Downloads/apriltags_kalman/ros_workspace/devel/include/anafi_control")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/isaac/Downloads/apriltags_kalman/ros_workspace/devel/share/roseus/ros/anafi_control")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/isaac/Downloads/apriltags_kalman/ros_workspace/devel/share/common-lisp/ros/anafi_control")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/isaac/Downloads/apriltags_kalman/ros_workspace/devel/share/gennodejs/ros/anafi_control")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python3" -m compileall "/home/isaac/Downloads/apriltags_kalman/ros_workspace/devel/lib/python3/dist-packages/anafi_control")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages" TYPE DIRECTORY FILES "/home/isaac/Downloads/apriltags_kalman/ros_workspace/devel/lib/python3/dist-packages/anafi_control")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/isaac/Downloads/apriltags_kalman/ros_workspace/build/anafi_control/catkin_generated/installspace/anafi_control.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/anafi_control/cmake" TYPE FILE FILES "/home/isaac/Downloads/apriltags_kalman/ros_workspace/build/anafi_control/catkin_generated/installspace/anafi_control-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/anafi_control/cmake" TYPE FILE FILES
    "/home/isaac/Downloads/apriltags_kalman/ros_workspace/build/anafi_control/catkin_generated/installspace/anafi_controlConfig.cmake"
    "/home/isaac/Downloads/apriltags_kalman/ros_workspace/build/anafi_control/catkin_generated/installspace/anafi_controlConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/anafi_control" TYPE FILE FILES "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/anafi_control" TYPE PROGRAM FILES "/home/isaac/Downloads/apriltags_kalman/ros_workspace/build/anafi_control/catkin_generated/installspace/anafi_control_waypoint_mpc.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/anafi_control" TYPE PROGRAM FILES "/home/isaac/Downloads/apriltags_kalman/ros_workspace/build/anafi_control/catkin_generated/installspace/anafi_control_cascaded_pid_interface.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/anafi_control" TYPE PROGRAM FILES "/home/isaac/Downloads/apriltags_kalman/ros_workspace/build/anafi_control/catkin_generated/installspace/anafi_control_cascaded_pid_relative_info.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/anafi_control" TYPE PROGRAM FILES "/home/isaac/Downloads/apriltags_kalman/ros_workspace/build/anafi_control/catkin_generated/installspace/trajectory_generator.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/anafi_control" TYPE PROGRAM FILES "/home/isaac/Downloads/apriltags_kalman/ros_workspace/build/anafi_control/catkin_generated/installspace/anafi_control_publish_stability_axes.py")
endif()

