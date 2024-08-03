from os.path import join

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node, SetParameter
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    bag_exec = ExecuteProcess(
        cmd=['ros2', 'bag', 'play', '-r', '1.0',
             '/data/kitti/raw/2011_09_29_drive_0071_sync_bag', '--clock']
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', join(get_package_share_directory('gps_imu_node'), 'rviz', 'gps_shift.rviz')]
    )

    gps_shift_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gps_imu_node'), 'launch', 'gps_shift_launch.py'
            ])
        ])
    )

    trajectory_server_node = Node(
        package='trajectory_server',
        executable='trajectory_server_node',
        name='trajectory_server_node',
        namespace='oxts',
        parameters=[{
            'target_frame_name': 'map',
            'source_frame_name': 'oxts_link',
            'trajectory_update_rate': 10.0,
            'trajectory_publish_rate': 10.0
        }]
    )

    return LaunchDescription([
        SetParameter(name='use_sim_time', value=True),
        bag_exec,
        rviz_node,
        gps_shift_launch,
        TimerAction(
            period=1.0,  # delay these nodes for 1.0 seconds.
            actions=[
                trajectory_server_node
            ]
        )
    ])
