# `tello_ros_drone`

This repo is built on top of [`tello_ros`](https://github.com/clydemcqueen/tello_ros) \
For the installation of `tello_ros`, check the original repo.

## Packages

There are 4 ROS packages:
* `tello_driver` is a C++ ROS node that connects to the drone
* `tello_msgs` is a set of ROS messages
* `tello_description` contains robot description (URDF) files
* `tello_gazebo` can be used to simulate a Tello drone in [Gazebo](http://gazebosim.org/),
* `tello_action` can be used to control a Tello drone based on distance.

## My Contiribution
`tello_ros` is devloped with tello SDK 1.3
Therefore, distance based control is not possible.
I have developed distance based service call.

`ros2 service call /tello_action tello_msgs/TelloAction "{cmd: 'takeoff'}"` \
`ros2 service call /drone1/move_cmd tello_interfaces/srv/HexaCmd "{dir: x, dist: 5}"` \
`ros2 service call /tello_action tello_msgs/TelloAction "{cmd: 'land'}"` \
dir is among x, y, z, xy. (xy means z axis rotation)
the unit of dist is m or radian.

