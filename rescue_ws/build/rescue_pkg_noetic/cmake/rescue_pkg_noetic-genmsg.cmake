# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "rescue_pkg_noetic: 1 messages, 1 services")

set(MSG_I_FLAGS "-Irescue_pkg_noetic:/home/john/rescue_ws/src/rescue_pkg_noetic/msg;-Istd_msgs:/opt/ros/noetic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(rescue_pkg_noetic_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/john/rescue_ws/src/rescue_pkg_noetic/msg/Num.msg" NAME_WE)
add_custom_target(_rescue_pkg_noetic_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "rescue_pkg_noetic" "/home/john/rescue_ws/src/rescue_pkg_noetic/msg/Num.msg" ""
)

get_filename_component(_filename "/home/john/rescue_ws/src/rescue_pkg_noetic/srv/AddTwoInts.srv" NAME_WE)
add_custom_target(_rescue_pkg_noetic_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "rescue_pkg_noetic" "/home/john/rescue_ws/src/rescue_pkg_noetic/srv/AddTwoInts.srv" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(rescue_pkg_noetic
  "/home/john/rescue_ws/src/rescue_pkg_noetic/msg/Num.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rescue_pkg_noetic
)

### Generating Services
_generate_srv_cpp(rescue_pkg_noetic
  "/home/john/rescue_ws/src/rescue_pkg_noetic/srv/AddTwoInts.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rescue_pkg_noetic
)

### Generating Module File
_generate_module_cpp(rescue_pkg_noetic
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rescue_pkg_noetic
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(rescue_pkg_noetic_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(rescue_pkg_noetic_generate_messages rescue_pkg_noetic_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/john/rescue_ws/src/rescue_pkg_noetic/msg/Num.msg" NAME_WE)
add_dependencies(rescue_pkg_noetic_generate_messages_cpp _rescue_pkg_noetic_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/john/rescue_ws/src/rescue_pkg_noetic/srv/AddTwoInts.srv" NAME_WE)
add_dependencies(rescue_pkg_noetic_generate_messages_cpp _rescue_pkg_noetic_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rescue_pkg_noetic_gencpp)
add_dependencies(rescue_pkg_noetic_gencpp rescue_pkg_noetic_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rescue_pkg_noetic_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(rescue_pkg_noetic
  "/home/john/rescue_ws/src/rescue_pkg_noetic/msg/Num.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rescue_pkg_noetic
)

### Generating Services
_generate_srv_eus(rescue_pkg_noetic
  "/home/john/rescue_ws/src/rescue_pkg_noetic/srv/AddTwoInts.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rescue_pkg_noetic
)

### Generating Module File
_generate_module_eus(rescue_pkg_noetic
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rescue_pkg_noetic
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(rescue_pkg_noetic_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(rescue_pkg_noetic_generate_messages rescue_pkg_noetic_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/john/rescue_ws/src/rescue_pkg_noetic/msg/Num.msg" NAME_WE)
add_dependencies(rescue_pkg_noetic_generate_messages_eus _rescue_pkg_noetic_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/john/rescue_ws/src/rescue_pkg_noetic/srv/AddTwoInts.srv" NAME_WE)
add_dependencies(rescue_pkg_noetic_generate_messages_eus _rescue_pkg_noetic_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rescue_pkg_noetic_geneus)
add_dependencies(rescue_pkg_noetic_geneus rescue_pkg_noetic_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rescue_pkg_noetic_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(rescue_pkg_noetic
  "/home/john/rescue_ws/src/rescue_pkg_noetic/msg/Num.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rescue_pkg_noetic
)

### Generating Services
_generate_srv_lisp(rescue_pkg_noetic
  "/home/john/rescue_ws/src/rescue_pkg_noetic/srv/AddTwoInts.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rescue_pkg_noetic
)

### Generating Module File
_generate_module_lisp(rescue_pkg_noetic
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rescue_pkg_noetic
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(rescue_pkg_noetic_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(rescue_pkg_noetic_generate_messages rescue_pkg_noetic_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/john/rescue_ws/src/rescue_pkg_noetic/msg/Num.msg" NAME_WE)
add_dependencies(rescue_pkg_noetic_generate_messages_lisp _rescue_pkg_noetic_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/john/rescue_ws/src/rescue_pkg_noetic/srv/AddTwoInts.srv" NAME_WE)
add_dependencies(rescue_pkg_noetic_generate_messages_lisp _rescue_pkg_noetic_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rescue_pkg_noetic_genlisp)
add_dependencies(rescue_pkg_noetic_genlisp rescue_pkg_noetic_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rescue_pkg_noetic_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(rescue_pkg_noetic
  "/home/john/rescue_ws/src/rescue_pkg_noetic/msg/Num.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/rescue_pkg_noetic
)

### Generating Services
_generate_srv_nodejs(rescue_pkg_noetic
  "/home/john/rescue_ws/src/rescue_pkg_noetic/srv/AddTwoInts.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/rescue_pkg_noetic
)

### Generating Module File
_generate_module_nodejs(rescue_pkg_noetic
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/rescue_pkg_noetic
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(rescue_pkg_noetic_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(rescue_pkg_noetic_generate_messages rescue_pkg_noetic_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/john/rescue_ws/src/rescue_pkg_noetic/msg/Num.msg" NAME_WE)
add_dependencies(rescue_pkg_noetic_generate_messages_nodejs _rescue_pkg_noetic_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/john/rescue_ws/src/rescue_pkg_noetic/srv/AddTwoInts.srv" NAME_WE)
add_dependencies(rescue_pkg_noetic_generate_messages_nodejs _rescue_pkg_noetic_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rescue_pkg_noetic_gennodejs)
add_dependencies(rescue_pkg_noetic_gennodejs rescue_pkg_noetic_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rescue_pkg_noetic_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(rescue_pkg_noetic
  "/home/john/rescue_ws/src/rescue_pkg_noetic/msg/Num.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rescue_pkg_noetic
)

### Generating Services
_generate_srv_py(rescue_pkg_noetic
  "/home/john/rescue_ws/src/rescue_pkg_noetic/srv/AddTwoInts.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rescue_pkg_noetic
)

### Generating Module File
_generate_module_py(rescue_pkg_noetic
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rescue_pkg_noetic
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(rescue_pkg_noetic_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(rescue_pkg_noetic_generate_messages rescue_pkg_noetic_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/john/rescue_ws/src/rescue_pkg_noetic/msg/Num.msg" NAME_WE)
add_dependencies(rescue_pkg_noetic_generate_messages_py _rescue_pkg_noetic_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/john/rescue_ws/src/rescue_pkg_noetic/srv/AddTwoInts.srv" NAME_WE)
add_dependencies(rescue_pkg_noetic_generate_messages_py _rescue_pkg_noetic_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rescue_pkg_noetic_genpy)
add_dependencies(rescue_pkg_noetic_genpy rescue_pkg_noetic_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rescue_pkg_noetic_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rescue_pkg_noetic)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rescue_pkg_noetic
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(rescue_pkg_noetic_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rescue_pkg_noetic)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rescue_pkg_noetic
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(rescue_pkg_noetic_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rescue_pkg_noetic)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rescue_pkg_noetic
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(rescue_pkg_noetic_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/rescue_pkg_noetic)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/rescue_pkg_noetic
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(rescue_pkg_noetic_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rescue_pkg_noetic)
  install(CODE "execute_process(COMMAND \"/usr/bin/python3\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rescue_pkg_noetic\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rescue_pkg_noetic
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(rescue_pkg_noetic_generate_messages_py std_msgs_generate_messages_py)
endif()
