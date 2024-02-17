cmake_minimum_required(VERSION 3.8)
project(mypkg_interfaces)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# rosidl_default_generators se utiliza para la generacion de mensajes/interfaces
# personalizados
find_package(rosidl_default_generators REQUIRED)

# Interfaces a generar
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/MyCustom.msg"
)

# El resultado (interfaces) generadas, debe ser exportado para que los
# pueda estar disponible a los demas
ament_export_dependencies(rosidl_default_runtime)

ament_package()
