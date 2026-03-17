
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.substitutions import FindPackageShare
import os


def generate_launch_description():

    pkg = "ma_robo"

    robot_description = Command([
        "xacro ",
        os.path.join(
            FindPackageShare(pkg).find(pkg),
            "urdf",
            "robo.xacro"
        )
    ])

    gazebo = ExecuteProcess(
        cmd=["gazebo", "--verbose", "-s", "libgazebo_ros_factory.so"],
        output="screen"
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}]
    )

    spawn_robot = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=[
            "-topic", "robot_description",
            "-entity", "ma_robo"
        ],
        output="screen"
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_robot
    ])

