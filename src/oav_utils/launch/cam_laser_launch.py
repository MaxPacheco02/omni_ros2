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

    rviz_config = os.path.join(get_package_share_directory("oav_utils"),'rviz/','cam_laser.rviz')

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
    )

    cam_node = Node(
        package='realsense2_camera',
        executable='realsense2_camera_node',
    )

    lidar_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('rplidar_ros'),
                'launch',
                'rplidar_a2m8_launch.py'
            ])
        ]),
    )

    return LaunchDescription([
        rviz,
        cam_node,
        lidar_launch,
    ])
