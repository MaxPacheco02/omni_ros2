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
    cam_node = Node(
        package='realsense2_camera',
        executable='realsense2_camera_node',
        parameters=[{
        'rgb_camera.color_profile': '640x480x30',
        'depth_module.depth_profile': '640x480x30',
        }]    
    )

    grpc_client_node = Node(
        package='oav_utils',
        executable='grpc_client_node.py',
    )


    return LaunchDescription([
        cam_node,
        grpc_client_node,
    ])
