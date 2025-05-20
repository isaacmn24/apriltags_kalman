# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "anafi_control: 5 messages, 0 services")

set(MSG_I_FLAGS "-Ianafi_control:/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg;-Igeometry_msgs:/opt/ros/noetic/share/geometry_msgs/cmake/../msg;-Istd_msgs:/opt/ros/noetic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(anafi_control_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/Waypoint.msg" NAME_WE)
add_custom_target(_anafi_control_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "anafi_control" "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/Waypoint.msg" ""
)

get_filename_component(_filename "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistModified.msg" NAME_WE)
add_custom_target(_anafi_control_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "anafi_control" "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistModified.msg" "std_msgs/Header:geometry_msgs/Vector3:geometry_msgs/Vector3Stamped"
)

get_filename_component(_filename "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistStampedModified.msg" NAME_WE)
add_custom_target(_anafi_control_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "anafi_control" "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistStampedModified.msg" "std_msgs/Header:geometry_msgs/Vector3:geometry_msgs/Vector3Stamped:anafi_control/TwistModified"
)

get_filename_component(_filename "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/State.msg" NAME_WE)
add_custom_target(_anafi_control_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "anafi_control" "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/State.msg" "anafi_control/TwistStampedModified:geometry_msgs/PoseStamped:std_msgs/Header:geometry_msgs/Point:geometry_msgs/Quaternion:geometry_msgs/Pose:anafi_control/TwistModified:geometry_msgs/Vector3Stamped:geometry_msgs/Vector3"
)

get_filename_component(_filename "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/MultiRotorRelativeState.msg" NAME_WE)
add_custom_target(_anafi_control_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "anafi_control" "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/MultiRotorRelativeState.msg" "std_msgs/Header"
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(anafi_control
  "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/Waypoint.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/anafi_control
)
_generate_msg_cpp(anafi_control
  "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistModified.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3Stamped.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/anafi_control
)
_generate_msg_cpp(anafi_control
  "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistStampedModified.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3Stamped.msg;/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistModified.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/anafi_control
)
_generate_msg_cpp(anafi_control
  "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/State.msg"
  "${MSG_I_FLAGS}"
  "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistStampedModified.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/PoseStamped.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistModified.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3Stamped.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/anafi_control
)
_generate_msg_cpp(anafi_control
  "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/MultiRotorRelativeState.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/anafi_control
)

### Generating Services

### Generating Module File
_generate_module_cpp(anafi_control
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/anafi_control
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(anafi_control_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(anafi_control_generate_messages anafi_control_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/Waypoint.msg" NAME_WE)
add_dependencies(anafi_control_generate_messages_cpp _anafi_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistModified.msg" NAME_WE)
add_dependencies(anafi_control_generate_messages_cpp _anafi_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistStampedModified.msg" NAME_WE)
add_dependencies(anafi_control_generate_messages_cpp _anafi_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/State.msg" NAME_WE)
add_dependencies(anafi_control_generate_messages_cpp _anafi_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/MultiRotorRelativeState.msg" NAME_WE)
add_dependencies(anafi_control_generate_messages_cpp _anafi_control_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(anafi_control_gencpp)
add_dependencies(anafi_control_gencpp anafi_control_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS anafi_control_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(anafi_control
  "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/Waypoint.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/anafi_control
)
_generate_msg_eus(anafi_control
  "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistModified.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3Stamped.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/anafi_control
)
_generate_msg_eus(anafi_control
  "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistStampedModified.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3Stamped.msg;/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistModified.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/anafi_control
)
_generate_msg_eus(anafi_control
  "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/State.msg"
  "${MSG_I_FLAGS}"
  "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistStampedModified.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/PoseStamped.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistModified.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3Stamped.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/anafi_control
)
_generate_msg_eus(anafi_control
  "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/MultiRotorRelativeState.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/anafi_control
)

### Generating Services

### Generating Module File
_generate_module_eus(anafi_control
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/anafi_control
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(anafi_control_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(anafi_control_generate_messages anafi_control_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/Waypoint.msg" NAME_WE)
add_dependencies(anafi_control_generate_messages_eus _anafi_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistModified.msg" NAME_WE)
add_dependencies(anafi_control_generate_messages_eus _anafi_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistStampedModified.msg" NAME_WE)
add_dependencies(anafi_control_generate_messages_eus _anafi_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/State.msg" NAME_WE)
add_dependencies(anafi_control_generate_messages_eus _anafi_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/MultiRotorRelativeState.msg" NAME_WE)
add_dependencies(anafi_control_generate_messages_eus _anafi_control_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(anafi_control_geneus)
add_dependencies(anafi_control_geneus anafi_control_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS anafi_control_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(anafi_control
  "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/Waypoint.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/anafi_control
)
_generate_msg_lisp(anafi_control
  "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistModified.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3Stamped.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/anafi_control
)
_generate_msg_lisp(anafi_control
  "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistStampedModified.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3Stamped.msg;/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistModified.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/anafi_control
)
_generate_msg_lisp(anafi_control
  "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/State.msg"
  "${MSG_I_FLAGS}"
  "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistStampedModified.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/PoseStamped.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistModified.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3Stamped.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/anafi_control
)
_generate_msg_lisp(anafi_control
  "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/MultiRotorRelativeState.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/anafi_control
)

### Generating Services

### Generating Module File
_generate_module_lisp(anafi_control
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/anafi_control
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(anafi_control_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(anafi_control_generate_messages anafi_control_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/Waypoint.msg" NAME_WE)
add_dependencies(anafi_control_generate_messages_lisp _anafi_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistModified.msg" NAME_WE)
add_dependencies(anafi_control_generate_messages_lisp _anafi_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistStampedModified.msg" NAME_WE)
add_dependencies(anafi_control_generate_messages_lisp _anafi_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/State.msg" NAME_WE)
add_dependencies(anafi_control_generate_messages_lisp _anafi_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/MultiRotorRelativeState.msg" NAME_WE)
add_dependencies(anafi_control_generate_messages_lisp _anafi_control_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(anafi_control_genlisp)
add_dependencies(anafi_control_genlisp anafi_control_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS anafi_control_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(anafi_control
  "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/Waypoint.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/anafi_control
)
_generate_msg_nodejs(anafi_control
  "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistModified.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3Stamped.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/anafi_control
)
_generate_msg_nodejs(anafi_control
  "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistStampedModified.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3Stamped.msg;/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistModified.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/anafi_control
)
_generate_msg_nodejs(anafi_control
  "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/State.msg"
  "${MSG_I_FLAGS}"
  "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistStampedModified.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/PoseStamped.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistModified.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3Stamped.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/anafi_control
)
_generate_msg_nodejs(anafi_control
  "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/MultiRotorRelativeState.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/anafi_control
)

### Generating Services

### Generating Module File
_generate_module_nodejs(anafi_control
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/anafi_control
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(anafi_control_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(anafi_control_generate_messages anafi_control_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/Waypoint.msg" NAME_WE)
add_dependencies(anafi_control_generate_messages_nodejs _anafi_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistModified.msg" NAME_WE)
add_dependencies(anafi_control_generate_messages_nodejs _anafi_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistStampedModified.msg" NAME_WE)
add_dependencies(anafi_control_generate_messages_nodejs _anafi_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/State.msg" NAME_WE)
add_dependencies(anafi_control_generate_messages_nodejs _anafi_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/MultiRotorRelativeState.msg" NAME_WE)
add_dependencies(anafi_control_generate_messages_nodejs _anafi_control_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(anafi_control_gennodejs)
add_dependencies(anafi_control_gennodejs anafi_control_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS anafi_control_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(anafi_control
  "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/Waypoint.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/anafi_control
)
_generate_msg_py(anafi_control
  "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistModified.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3Stamped.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/anafi_control
)
_generate_msg_py(anafi_control
  "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistStampedModified.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3Stamped.msg;/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistModified.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/anafi_control
)
_generate_msg_py(anafi_control
  "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/State.msg"
  "${MSG_I_FLAGS}"
  "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistStampedModified.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/PoseStamped.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose.msg;/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistModified.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3Stamped.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/anafi_control
)
_generate_msg_py(anafi_control
  "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/MultiRotorRelativeState.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/anafi_control
)

### Generating Services

### Generating Module File
_generate_module_py(anafi_control
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/anafi_control
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(anafi_control_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(anafi_control_generate_messages anafi_control_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/Waypoint.msg" NAME_WE)
add_dependencies(anafi_control_generate_messages_py _anafi_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistModified.msg" NAME_WE)
add_dependencies(anafi_control_generate_messages_py _anafi_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/TwistStampedModified.msg" NAME_WE)
add_dependencies(anafi_control_generate_messages_py _anafi_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/State.msg" NAME_WE)
add_dependencies(anafi_control_generate_messages_py _anafi_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/isaac/Downloads/apriltags_kalman/ros_workspace/src/anafi_control/msg/MultiRotorRelativeState.msg" NAME_WE)
add_dependencies(anafi_control_generate_messages_py _anafi_control_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(anafi_control_genpy)
add_dependencies(anafi_control_genpy anafi_control_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS anafi_control_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/anafi_control)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/anafi_control
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_cpp)
  add_dependencies(anafi_control_generate_messages_cpp geometry_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/anafi_control)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/anafi_control
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_eus)
  add_dependencies(anafi_control_generate_messages_eus geometry_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/anafi_control)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/anafi_control
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_lisp)
  add_dependencies(anafi_control_generate_messages_lisp geometry_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/anafi_control)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/anafi_control
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_nodejs)
  add_dependencies(anafi_control_generate_messages_nodejs geometry_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/anafi_control)
  install(CODE "execute_process(COMMAND \"/usr/bin/python3\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/anafi_control\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/anafi_control
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_py)
  add_dependencies(anafi_control_generate_messages_py geometry_msgs_generate_messages_py)
endif()
