from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    ld = LaunchDescription()

    accion1 = Node(
        package='dofbot_ctrl',
        executable='dofbot_node',
    )

    ld.add_action(accion1)


    return ld
