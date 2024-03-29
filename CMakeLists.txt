cmake_minimum_required(VERSION 3.8)
project(gps_imu_node)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-O3 -Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(message_filters REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)
find_package(tf2_eigen REQUIRED)

# system
find_package(Eigen3 REQUIRED)
find_package(GeographicLib REQUIRED)

add_executable(imu_rotate_node
  src/imu_rotate.cpp
  src/imu_rotate_node.cpp)

target_include_directories(imu_rotate_node PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
  ${EIGEN3_INCLUDE_DIR})

ament_target_dependencies(imu_rotate_node PUBLIC
  rclcpp
  sensor_msgs
  tf2_eigen)

target_compile_features(imu_rotate_node PUBLIC c_std_99 cxx_std_17)  # Require C99 and C++17

add_executable(gps_shift_node
  src/gps_shift.cpp
  src/gps_shift_node.cpp)

target_include_directories(gps_shift_node PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
  ${EIGEN3_INCLUDE_DIR})

ament_target_dependencies(gps_shift_node PUBLIC
  rclcpp
  sensor_msgs
  message_filters
  tf2_ros
  tf2
  tf2_geometry_msgs
  tf2_eigen)

target_link_libraries(gps_shift_node PUBLIC
  GeographicLib)

target_compile_features(gps_shift_node PUBLIC c_std_99 cxx_std_17)  # Require C99 and C++17

install(TARGETS imu_rotate_node gps_shift_node
  DESTINATION lib/${PROJECT_NAME})

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME})

install(DIRECTORY rviz
  DESTINATION share/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
