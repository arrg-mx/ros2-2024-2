#!/usr/bin/env python3

import launch
import os
import launch_ros
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # ruta al paquete de ros2
    pkgPath = launch_ros.substitutions.FindPackageShare(package='dofbot_description').find('dofbot_description')
    # ruta a archivo urdf del robot
    urdfModelPath = os.path.join(pkgPath, 'urdf/dofbot_arm.urdf')
    # Leemos el contenido del archivo
    with open(urdfModelPath, 'r') as infp:
        robot_desc = infp.read()

    # Asignamos el contenido del archivo al parametro 'robot_description'
    params = {
        'robot_description': robot_desc
    }

    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        parameters=[params],
        condition=launch.conditions.UnlessCondition(LaunchConfiguration('gui'))
    )

    joint_state_publisher_gui_node = launch_ros.actions.Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        condition=launch.conditions.IfCondition(LaunchConfiguration('gui'))
    )

    rviz_config_file = 'rviz/myconfig.rviz'
    rviz_config = os.path.join(
        get_package_share_directory('dofbot_description'),
        rviz_config_file
    )

    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        arguments=['-d', rviz_config]
    )

    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(
            name='gui',
            default_value='True',
            description='Es una bandera para mostrar joint_state_publisher'
        ),
        launch.actions.DeclareLaunchArgument(
            name='model',
            default_value=urdfModelPath,
            description='Ruta al archivo urdf del modelo'
        ),
        robot_state_publisher_node,
        joint_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node
    ])