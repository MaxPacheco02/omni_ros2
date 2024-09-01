import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

from launch.actions import IncludeLaunchDescription, LogInfo, DeclareLaunchArgument
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.substitutions import FindPackageShare

from launch.conditions import IfCondition, UnlessCondition

from launch.substitutions import FindExecutable
from launch.actions import ExecuteProcess


def generate_launch_description():
    grpc_client_node = Node(
        package='oav_utils',
        executable='grpc_client_node.py',
    )

    joy_node = Node(
        package='joy',
        executable='joy_node',
    )

    teleop_control_node = Node(
        package='oav_utils',
        executable='teleop_control_node.py',
    )

    return LaunchDescription([
        grpc_client_node,
        joy_node,
        teleop_control_node,
    ])